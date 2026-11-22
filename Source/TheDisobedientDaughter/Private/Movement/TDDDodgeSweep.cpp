#include "Movement/TDDDodgeSweep.h"

#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "GameFramework/Character.h"
#include "Movement/TDDDodgeDistanceMath.h"

namespace TDD
{
namespace Movement
{

FDodgeSweepResult ResolveDodgeSweep(
    const ACharacter& Character,
    const FVector& DesiredDirection,
    const float AuthoredDistanceCm,
    const float SafetyMarginCm,
    const AActor* LockedTargetActor)
{
    FDodgeSweepResult Result;

    if (!FMath::IsFinite(AuthoredDistanceCm) || AuthoredDistanceCm <= 0.0f ||
        !FMath::IsFinite(SafetyMarginCm) || SafetyMarginCm < 0.0f)
    {
        Result.Status = EDodgeSweepStatus::InvalidSpecification;
        return Result;
    }

    FVector Direction(DesiredDirection.X, DesiredDirection.Y, 0.0f);
    if (!FMath::IsFinite(Direction.X) || !FMath::IsFinite(Direction.Y) || !Direction.Normalize())
    {
        Result.Status = EDodgeSweepStatus::InvalidDirection;
        return Result;
    }

    UWorld* World = Character.GetWorld();
    if (World == nullptr)
    {
        Result.Status = EDodgeSweepStatus::MissingWorld;
        return Result;
    }

    const UCapsuleComponent* Capsule = Character.GetCapsuleComponent();
    if (Capsule == nullptr)
    {
        Result.Status = EDodgeSweepStatus::MissingCapsule;
        return Result;
    }

    const float Radius = Capsule->GetScaledCapsuleRadius();
    const float HalfHeight = Capsule->GetScaledCapsuleHalfHeight();
    if (!FMath::IsFinite(Radius) || !FMath::IsFinite(HalfHeight) || Radius <= 0.0f || HalfHeight < Radius)
    {
        Result.Status = EDodgeSweepStatus::MissingCapsule;
        return Result;
    }

    const FVector Start = Capsule->GetComponentLocation();
    const FVector End = Start + Direction * AuthoredDistanceCm;
    const FCollisionShape Shape = FCollisionShape::MakeCapsule(Radius, HalfHeight);

    FCollisionQueryParams QueryParams(SCENE_QUERY_STAT(TDDDodgeSweep), false);
    QueryParams.AddIgnoredActor(&Character);
    if (LockedTargetActor != nullptr)
    {
        QueryParams.AddIgnoredActor(LockedTargetActor);
    }

    FHitResult Hit;
    const bool bBlocked = World->SweepSingleByChannel(
        Hit,
        Start,
        End,
        FQuat::Identity,
        ECC_Pawn,
        Shape,
        QueryParams);

    if (bBlocked && Hit.bStartPenetrating)
    {
        Result.Status = EDodgeSweepStatus::StartingPenetration;
        Result.BlockingHit = Hit;
        Result.bWasBlocked = true;
        return Result;
    }

    float ResolvedDistanceCm = 0.0f;
    const float SweptCentreDistanceCm = bBlocked ? (Hit.Location - Start).Size2D() : 0.0f;
    if (!ResolveDodgeDistance(
            AuthoredDistanceCm,
            bBlocked,
            SweptCentreDistanceCm,
            SafetyMarginCm,
            ResolvedDistanceCm))
    {
        Result.Status = EDodgeSweepStatus::InvalidSpecification;
        return Result;
    }

    Result.Direction = Direction;
    Result.ResolvedDistanceCm = ResolvedDistanceCm;
    Result.bWasBlocked = bBlocked;
    Result.BlockingHit = Hit;
    Result.Status = ResolvedDistanceCm > 0.0f
        ? EDodgeSweepStatus::ClearanceResolved
        : EDodgeSweepStatus::NoClearance;
    return Result;
}

} // namespace Movement
} // namespace TDD
