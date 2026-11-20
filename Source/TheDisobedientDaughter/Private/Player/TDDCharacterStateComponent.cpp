#include "Player/TDDCharacterStateComponent.h"

#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"

using TDD::State::ETDDPlayerState;
using TDD::State::ETDDRefusalReason;

UTDDCharacterStateComponent::UTDDCharacterStateComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UTDDCharacterStateComponent::BeginPlay()
{
    Super::BeginPlay();
    LastPublishedState = Machine.Current();
}

void UTDDCharacterStateComponent::TickComponent(
    const float DeltaTime,
    const ELevelTick TickType,
    FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    Machine.Tick(DeltaTime);

    // World physics remains authoritative for airborne/landing state. The pure
    // recovery clock is intentionally not used to infer a landing from time.
    if (const ACharacter* Character = Cast<ACharacter>(GetOwner()))
    {
        const UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
        if (Movement != nullptr)
        {
            if (Movement->IsFalling() && Machine.Current() != ETDDPlayerState::Airborne)
            {
                Machine.RequestState(ETDDPlayerState::Airborne, "CMC falling");
            }
            else if (!Movement->IsFalling() && Machine.Current() == ETDDPlayerState::Airborne)
            {
                Machine.RequestState(ETDDPlayerState::Land, "CMC landed");
            }
        }
    }
    PublishIfChanged();
}

bool UTDDCharacterStateComponent::RequestState(const int32 TargetState, const FName Reason)
{
    if (TargetState < 0 || TargetState >= static_cast<int32>(ETDDPlayerState::Count))
    {
        return false;
    }
    const ETDDRefusalReason Result = Machine.RequestState(
        static_cast<ETDDPlayerState>(TargetState), TCHAR_TO_UTF8(*Reason.ToString()));
    PublishIfChanged();
    return Result == ETDDRefusalReason::Accepted;
}

bool UTDDCharacterStateComponent::ForceState(const int32 TargetState)
{
    if (TargetState < 0 || TargetState >= static_cast<int32>(ETDDPlayerState::Count))
    {
        return false;
    }
    const ETDDRefusalReason Result = Machine.ForceState(static_cast<ETDDPlayerState>(TargetState));
    PublishIfChanged();
    return Result == ETDDRefusalReason::Accepted;
}

int32 UTDDCharacterStateComponent::GetCurrentState() const
{
    return static_cast<int32>(Machine.Current());
}

float UTDDCharacterStateComponent::GetTimeInState() const
{
    return Machine.TimeInCurrent();
}

void UTDDCharacterStateComponent::SetLocomotionIntent(const bool bIsMoving, const bool bWantsSprint)
{
    ETDDPlayerState Target = ETDDPlayerState::Idle;
    if (bIsMoving)
    {
        Target = bWantsSprint ? ETDDPlayerState::Sprint : ETDDPlayerState::Locomotion;
    }
    if (Machine.Current() == Target || Machine.Current() == ETDDPlayerState::Airborne ||
        Machine.Current() == ETDDPlayerState::Land)
    {
        return;
    }
    Machine.RequestState(Target, "locomotion intent");
    PublishIfChanged();
}

void UTDDCharacterStateComponent::PublishIfChanged()
{
    const ETDDPlayerState Current = Machine.Current();
    if (Current != LastPublishedState)
    {
        OnStateChanged.Broadcast(static_cast<int32>(LastPublishedState), static_cast<int32>(Current));
        LastPublishedState = Current;
    }
}
