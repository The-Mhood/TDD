#include "Combat/TDDCombatComponent.h"

#include "AI/TDDBossPhaseComponent.h"
#include "Components/CapsuleComponent.h"
#include "Core/TDDCombatTiming.h"
#include "Core/TDDDamageMath.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Player/TDDCharacterStateComponent.h"

namespace
{
constexpr int32 StateIdle = static_cast<int32>(TDD::State::ETDDPlayerState::Idle);
constexpr int32 StateLocomotion = static_cast<int32>(TDD::State::ETDDPlayerState::Locomotion);
constexpr int32 StateAttack = static_cast<int32>(TDD::State::ETDDPlayerState::Attack);
constexpr int32 StateBlock = static_cast<int32>(TDD::State::ETDDPlayerState::Block);
constexpr int32 StateParry = static_cast<int32>(TDD::State::ETDDPlayerState::Parry);
constexpr int32 StateStagger = static_cast<int32>(TDD::State::ETDDPlayerState::Stagger);
constexpr int32 StateDead = static_cast<int32>(TDD::State::ETDDPlayerState::Dead);
}

UTDDCombatComponent::UTDDCombatComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UTDDCombatComponent::TickComponent(const float DeltaTime, const ELevelTick TickType,
                                         FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    UTDDCharacterStateComponent* State = FindStateComponent();
    if (State == nullptr)
    {
        bGuardReleasePending = false;
        bGuarding = false;
        return;
    }
    const int32 Current = State->GetCurrentState();
    if (bGuarding && Current != StateBlock && Current != StateParry)
    {
        bGuarding = false;
        GuardStartedAt = -1.0f;
    }
    if (!bGuardReleasePending)
    {
        return;
    }
    if (Current == StateParry)
    {
        return; // Parry recovers to Block; finish the pending release next tick.
    }
    if (Current != StateBlock)
    {
        bGuardReleasePending = false;
        return;
    }
    if (State->RequestState(StateLocomotion, TEXT("deferred guard release")) ||
        State->RequestState(StateIdle, TEXT("deferred guard release")))
    {
        bGuardReleasePending = false;
    }
}

void UTDDCombatComponent::BeginPlay()
{
    Super::BeginPlay();
    Health = FMath::Max(1.0f, MaxHealth);
    Posture = 0.0f;
}

UTDDCharacterStateComponent* UTDDCombatComponent::FindStateComponent() const
{
    return GetOwner() ? GetOwner()->FindComponentByClass<UTDDCharacterStateComponent>() : nullptr;
}

bool UTDDCombatComponent::PerformLightAttack()
{
    AActor* Owner = GetOwner();
    UWorld* World = GetWorld();
    UTDDCharacterStateComponent* State = FindStateComponent();
    if (Owner == nullptr || World == nullptr || State == nullptr || IsDead() || bGuarding)
    {
        return false;
    }
    if (!State->RequestState(StateAttack, TEXT("light attack")))
    {
        return false;
    }

    const UCapsuleComponent* Capsule = Owner->FindComponentByClass<UCapsuleComponent>();
    const FVector Origin = Capsule ? Capsule->GetComponentLocation() : Owner->GetActorLocation();
    const FVector Start = Origin + FVector(0.0f, 0.0f, 25.0f);
    const FVector End = Start + Owner->GetActorForwardVector() * LightAttackRange;
    FCollisionQueryParams Params(SCENE_QUERY_STAT(TDDLightAttack), false, Owner);
    FHitResult Hit;
    if (!World->SweepSingleByChannel(Hit, Start, End, FQuat::Identity, ECC_Pawn,
            FCollisionShape::MakeSphere(36.0f), Params))
    {
        return true; // attack state still owns its committed recovery window
    }

    UTDDCombatComponent* Target = Hit.GetActor()
        ? Hit.GetActor()->FindComponentByClass<UTDDCombatComponent>() : nullptr;
    if (Target != nullptr && Target != this)
    {
        Target->ReceiveAttack(LightHealthDamage, LightPostureDamage, false, this);
    }
    return true;
}

bool UTDDCombatComponent::SetGuarding(const bool bNewGuarding)
{
    if (IsDead())
    {
        return false;
    }
    UTDDCharacterStateComponent* State = FindStateComponent();
    if (State == nullptr)
    {
        return false;
    }
    if (bNewGuarding)
    {
        if (!State->RequestState(StateBlock, TEXT("guard pressed")))
        {
            return false;
        }
        bGuarding = true;
        bGuardReleasePending = false;
        GuardStartedAt = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
        return true;
    }
    if (!bGuarding)
    {
        return true;
    }
    bGuarding = false;
    GuardStartedAt = -1.0f;
    const int32 Current = State->GetCurrentState();
    if (Current == StateBlock)
    {
        // Block-release is a legal requested transition in the pure state rules.
        const bool bReleased = State->RequestState(StateLocomotion, TEXT("guard released")) ||
                               State->RequestState(StateIdle, TEXT("guard released"));
        bGuardReleasePending = !bReleased;
    }
    else if (Current == StateParry)
    {
        bGuardReleasePending = true; // Parry's authored recovery returns to Block.
    }
    return true;
}

bool UTDDCombatComponent::ReceiveAttack(const float InHealthDamage, const float InPostureDamage,
                                         const bool bCausesStagger, UTDDCombatComponent* Attacker)
{
    if (IsDead() || !FMath::IsFinite(InHealthDamage) || !FMath::IsFinite(InPostureDamage) ||
        InHealthDamage <= 0.0f || InPostureDamage < 0.0f)
    {
        return false;
    }
    if (const UTDDBossPhaseComponent* BossPhases = GetOwner()
            ? GetOwner()->FindComponentByClass<UTDDBossPhaseComponent>() : nullptr)
    {
        if (BossPhases->IsCurrentPhaseInvulnerable())
        {
            return false;
        }
    }

    const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.0f;
    const float GuardAge = bGuarding ? FMath::Max(0.0f, Now - GuardStartedAt) : -1.0f;
    if (bGuarding && TDD::Combat::IsInParryWindow(GuardAge))
    {
        if (UTDDCharacterStateComponent* State = FindStateComponent())
        {
            State->RequestState(StateParry, TEXT("successful parry"));
        }
        if (Attacker != nullptr)
        {
            Attacker->ReceiveSuccessfulParry();
        }
        return false;
    }

    TDD::Combat::FTDDDamageRequest Request;
    Request.HealthDamage = InHealthDamage;
    Request.PostureDamage = InPostureDamage;
    Request.bCausesStagger = bCausesStagger;
    if (bGuarding && TDD::Combat::IsGuardReady(GuardAge))
    {
        Request.HealthDamage *= 0.2f; // provisional chip damage while guarding
        Request.PostureDamage *= 0.5f;
        Request.bCausesStagger = false;
    }

    TDD::Combat::FTDDDefenderState Defender;
    Defender.Health = Health;
    Defender.Posture = Posture;
    Defender.MaxPosture = MaxPosture;
    const TDD::Combat::FTDDDamageOutcome Outcome = TDD::Combat::EvaluateDamage(Request, Defender);
    ApplyOutcome(Outcome);
    return Outcome.Classification != TDD::Combat::ETDDDamageClassification::None;
}

void UTDDCombatComponent::ReceiveSuccessfulParry()
{
    if (UTDDCharacterStateComponent* State = FindStateComponent())
    {
        State->ForceState(StateStagger);
    }
}

void UTDDCombatComponent::ResetForRestart()
{
    Health = MaxHealth;
    Posture = 0.0f;
    GuardStartedAt = -1.0f;
    bGuarding = false;
    bGuardReleasePending = false;
}

void UTDDCombatComponent::ApplyOutcome(const TDD::Combat::FTDDDamageOutcome& Outcome)
{
    if (Outcome.Classification == TDD::Combat::ETDDDamageClassification::None)
    {
        return;
    }
    Health = Outcome.NewHealth;
    Posture = Outcome.NewPosture;
    if (UTDDBossPhaseComponent* BossPhases = GetOwner()
            ? GetOwner()->FindComponentByClass<UTDDBossPhaseComponent>() : nullptr)
    {
        BossPhases->SetHealthPercent(MaxHealth > 0.0f ? Health / MaxHealth : 0.0f);
        if (Outcome.bPostureBroken)
        {
            BossPhases->NotifyPoiseBreak();
        }
    }
    if (UTDDCharacterStateComponent* State = FindStateComponent())
    {
        if (Outcome.bEnteredDead)
        {
            State->ForceState(StateDead);
            if (ACharacter* DeadCharacter = Cast<ACharacter>(GetOwner()))
            {
                DeadCharacter->GetCharacterMovement()->DisableMovement();
                if (APlayerController* PlayerController = Cast<APlayerController>(DeadCharacter->GetController()))
                {
                    DeadCharacter->DisableInput(PlayerController);
                }
            }
        }
        else if (Outcome.bEnteredStagger)
        {
            State->ForceState(StateStagger);
        }
    }
}
