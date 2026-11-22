#include "AI/TDDCombatBrainComponent.h"

#include "AI/TDDCombatDirectorSubsystem.h"
#include "Combat/TDDCombatComponent.h"
#include "GameFramework/Character.h"
#include "Kismet/GameplayStatics.h"
#include "Player/TDDCharacterStateComponent.h"

UTDDCombatBrainComponent::UTDDCombatBrainComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UTDDCombatBrainComponent::BeginPlay()
{
    Super::BeginPlay();
    if (UWorld* World = GetWorld())
    {
        if (UTDDCombatDirectorSubsystem* Director = World->GetSubsystem<UTDDCombatDirectorSubsystem>())
        {
            UTDDCombatComponent* Combat = GetOwner()
                ? GetOwner()->FindComponentByClass<UTDDCombatComponent>() : nullptr;
            if (Combat != nullptr)
            {
                Director->RegisterEnemy(Combat);
                bRegisteredWithDirector = true;
            }
        }
    }
}

void UTDDCombatBrainComponent::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    if (bRegisteredWithDirector)
    {
        if (UWorld* World = GetWorld())
        {
            if (UTDDCombatDirectorSubsystem* Director = World->GetSubsystem<UTDDCombatDirectorSubsystem>())
            {
                Director->UnregisterEnemy(GetOwner() ? GetOwner()->FindComponentByClass<UTDDCombatComponent>() : nullptr);
            }
        }
        bRegisteredWithDirector = false;
    }
    Super::EndPlay(EndPlayReason);
}

void UTDDCombatBrainComponent::TickComponent(const float DeltaTime, const ELevelTick TickType,
                                               FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    ACharacter* Character = Cast<ACharacter>(GetOwner());
    if (Character == nullptr || DeltaTime <= 0.0f)
    {
        return;
    }
    UTDDCombatComponent* Combat = Character->FindComponentByClass<UTDDCombatComponent>();
    if (Combat == nullptr)
    {
        return;
    }
    if (Combat->IsDead())
    {
        if (bRegisteredWithDirector)
        {
            if (UTDDCombatDirectorSubsystem* Director = GetWorld()
                    ? GetWorld()->GetSubsystem<UTDDCombatDirectorSubsystem>() : nullptr)
            {
                Director->UnregisterEnemy(Combat);
            }
            bRegisteredWithDirector = false;
        }
        return;
    }

    AActor* Player = UGameplayStatics::GetPlayerCharacter(this, 0);
    if (Player == nullptr || Player == Character)
    {
        return;
    }

    FVector ToTarget = Player->GetActorLocation() - Character->GetActorLocation();
    ToTarget.Z = 0.0f;
    const float Distance = ToTarget.Size();
    if (FMath::IsNearlyZero(Distance))
    {
        return;
    }
    const FVector Direction = ToTarget / Distance;
    const FRotator DesiredRotation = Direction.Rotation();
    Character->SetActorRotation(FMath::RInterpTo(Character->GetActorRotation(), DesiredRotation,
        DeltaTime, 8.0f));

    const bool bShouldClose = Distance > StopDistance;
    if (bShouldClose)
    {
        Character->AddMovementInput(Direction, 1.0f);
    }
    if (UTDDCharacterStateComponent* State = Character->FindComponentByClass<UTDDCharacterStateComponent>())
    {
        State->SetLocomotionIntent(bShouldClose, false);
    }
}
