#pragma once

#include "CoreMinimal.h"

class AActor;
class ACharacter;

namespace TDD
{
namespace Movement
{

enum class EDodgeSweepStatus : uint8
{
    ClearanceResolved,
    InvalidSpecification,
    InvalidDirection,
    MissingWorld,
    MissingCapsule,
    StartingPenetration,
    NoClearance
};

// Result of the pre-movement clearance query. The CharacterMovementComponent
// remains responsible for moving the capsule; callers must still perform the
// M1-specified destination-floor validation before executing the dodge.
struct FDodgeSweepResult
{
    EDodgeSweepStatus Status = EDodgeSweepStatus::InvalidSpecification;
    FVector Direction = FVector::ZeroVector;
    float ResolvedDistanceCm = 0.0f;
    FHitResult BlockingHit;
    bool bWasBlocked = false;

    bool HasPositiveClearance() const
    {
        return Status == EDodgeSweepStatus::ClearanceResolved && ResolvedDistanceCm > 0.0f;
    }
};

// Performs the specified horizontal capsule sweep only. It does not move the
// character and does not consume cooldown/state; those belong to the eventual
// character/state-machine integration.
FDodgeSweepResult ResolveDodgeSweep(
    const ACharacter& Character,
    const FVector& DesiredDirection,
    float AuthoredDistanceCm,
    float SafetyMarginCm,
    const AActor* LockedTargetActor);

} // namespace Movement
} // namespace TDD
