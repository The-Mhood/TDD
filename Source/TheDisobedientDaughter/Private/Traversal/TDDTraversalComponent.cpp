#include "Traversal/TDDTraversalComponent.h"

#include "Components/CapsuleComponent.h"
#include "Core/TDDStateRules.h"
#include "Core/TDDTraversalFallback.h"
#include "Engine/World.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Player/TDDCharacterStateComponent.h"

UTDDTraversalComponent::UTDDTraversalComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

bool UTDDTraversalComponent::FindLandingFloor(ACharacter* Character, const FVector& Direction,
                                                FVector& OutFloorPoint, float& OutHeightDelta) const
{
    if (Character == nullptr || GetWorld() == nullptr)
    {
        return false;
    }
    const UCapsuleComponent* Capsule = Character->GetCapsuleComponent();
    if (Capsule == nullptr)
    {
        return false;
    }
    const float HalfHeight = Capsule->GetScaledCapsuleHalfHeight();
    const float BaseZ = Capsule->GetComponentLocation().Z - HalfHeight;
    const FVector LandingXY = Capsule->GetComponentLocation() + Direction * ForwardReach;
    const FVector TraceStart(LandingXY.X, LandingXY.Y, BaseZ + MaxVaultHeight + 100.0f);
    const FVector TraceEnd(LandingXY.X, LandingXY.Y, BaseZ - MaxDropHeight - 100.0f);

    FCollisionQueryParams Params(SCENE_QUERY_STAT(TDDTraversalFloor), false, Character);
    FHitResult Hit;
    if (!GetWorld()->LineTraceSingleByChannel(Hit, TraceStart, TraceEnd, ECC_Visibility, Params) ||
        Hit.bStartPenetrating || Hit.ImpactNormal.Z < FMath::Cos(FMath::DegreesToRadians(35.0f)))
    {
        return false;
    }
    OutFloorPoint = Hit.ImpactPoint;
    OutHeightDelta = Hit.ImpactPoint.Z - BaseZ;
    return true;
}

bool UTDDTraversalComponent::IsVaultPathClear(ACharacter* Character, const FVector& Direction,
                                               const FVector& LandingCenter) const
{
    if (Character == nullptr || GetWorld() == nullptr || Character->GetCapsuleComponent() == nullptr)
    {
        return false;
    }
    constexpr float LaunchVerticalSpeed = 500.0f;
    constexpr int32 ArcSamples = 12;
    const UCapsuleComponent* Capsule = Character->GetCapsuleComponent();
    const UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
    if (Movement == nullptr)
    {
        return false;
    }
    const float Gravity = FMath::Abs(GetWorld()->GetGravityZ() * Movement->GravityScale);
    const float DeltaZ = LandingCenter.Z - Capsule->GetComponentLocation().Z;
    const float Discriminant = LaunchVerticalSpeed * LaunchVerticalSpeed - 2.0f * Gravity * DeltaZ;
    if (!FMath::IsFinite(Gravity) || Gravity <= KINDA_SMALL_NUMBER || Discriminant < 0.0f)
    {
        return false;
    }
    const float FlightTime = (LaunchVerticalSpeed + FMath::Sqrt(Discriminant)) / Gravity;
    const float HorizontalSpeed = ForwardReach / FlightTime;
    const FVector Start = Capsule->GetComponentLocation() + FVector(0.0f, 0.0f, 2.0f);
    const FCollisionShape Shape = FCollisionShape::MakeCapsule(
        Capsule->GetScaledCapsuleRadius(), Capsule->GetScaledCapsuleHalfHeight());
    FCollisionQueryParams Params(SCENE_QUERY_STAT(TDDTraversalVaultPath), false, Character);
    const FQuat Rotation = Capsule->GetComponentQuat();
    FVector Previous = Start;
    for (int32 Index = 1; Index <= ArcSamples; ++Index)
    {
        const float T = FlightTime * static_cast<float>(Index) / ArcSamples;
        const float Height = LaunchVerticalSpeed * T - 0.5f * Gravity * T * T;
        FVector Next = Start + Direction * (HorizontalSpeed * T) + FVector(0.0f, 0.0f, Height);
        if (Index == ArcSamples)
        {
            Next = LandingCenter + FVector(0.0f, 0.0f, 2.0f);
        }
        if (GetWorld()->SweepTestByChannel(Previous, Next, Rotation, ECC_Pawn, Shape, Params))
        {
            return false;
        }
        Previous = Next;
    }
    return true;
}

bool UTDDTraversalComponent::TryTraverse()
{
    ACharacter* Character = Cast<ACharacter>(GetOwner());
    if (Character == nullptr)
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNotCharacter;
        return false;
    }
    UWorld* World = GetWorld();
    UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
    UCapsuleComponent* Capsule = Character->GetCapsuleComponent();
    UTDDCharacterStateComponent* State = Character->FindComponentByClass<UTDDCharacterStateComponent>();
    if (World == nullptr || Movement == nullptr || Capsule == nullptr || State == nullptr)
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNotCharacter;
        return false;
    }
    if (!Movement->IsMovingOnGround())
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNotGrounded;
        return false;
    }

    const float Now = World->GetTimeSeconds();
    if (Now - LastAttemptTime < CooldownSeconds)
    {
        LastResult = ETDDTraversalAttemptResult::RejectedCooldown;
        return false;
    }
    LastAttemptTime = Now;

    FVector Direction = Character->GetActorForwardVector();
    Direction.Z = 0.0f;
    if (!Direction.Normalize())
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
        return false;
    }

    const float HalfHeight = Capsule->GetScaledCapsuleHalfHeight();
    const float BaseZ = Capsule->GetComponentLocation().Z - HalfHeight;
    const FVector CapsuleCenter = Capsule->GetComponentLocation();
    const FVector ProbeEnd(CapsuleCenter.X + Direction.X * ForwardReach,
                           CapsuleCenter.Y + Direction.Y * ForwardReach, 0.0f);
    const FVector LowStart(CapsuleCenter.X, CapsuleCenter.Y, BaseZ + 45.0f);
    const FVector LowEnd(ProbeEnd.X, ProbeEnd.Y, BaseZ + 45.0f);
    const FVector HighStart(CapsuleCenter.X, CapsuleCenter.Y, BaseZ + MaxVaultHeight);
    const FVector HighEnd(ProbeEnd.X, ProbeEnd.Y, BaseZ + MaxVaultHeight);
    const FCollisionShape Probe = FCollisionShape::MakeSphere(12.0f);
    FCollisionQueryParams Params(SCENE_QUERY_STAT(TDDTraversalProbe), false, Character);
    FHitResult LowHit;
    FHitResult HighHit;
    const bool bLowBlocked = World->SweepSingleByChannel(LowHit, LowStart,
        LowEnd, FQuat::Identity, ECC_Visibility, Probe, Params);
    const bool bHighBlocked = World->SweepSingleByChannel(HighHit, HighStart,
        HighEnd, FQuat::Identity, ECC_Visibility, Probe, Params);

    FVector FloorPoint = FVector::ZeroVector;
    float HeightDelta = 0.0f;
    const bool bFloorFound = FindLandingFloor(Character, Direction, FloorPoint, HeightDelta);
    const FVector LandingCenter = FloorPoint + FVector(0.0f, 0.0f, HalfHeight + 3.0f);
    const bool bVaultCandidate = bFloorFound && bLowBlocked && !bHighBlocked &&
        HeightDelta <= MaxVaultHeight && HeightDelta >= -MaxDropHeight &&
        IsVaultPathClear(Character, Direction, LandingCenter);
    const bool bDropCandidate = bFloorFound && !bLowBlocked &&
        HeightDelta < -25.0f && HeightDelta >= -MaxDropHeight;

    TDD::Traversal::FTDDFallbackInput FallbackInput;
    FallbackInput.AttemptBudget = 3;
    FallbackInput.bPhase1AttemptSucceeds = bVaultCandidate;
    FallbackInput.Phase1AttemptTime = bVaultCandidate ? 0.15f : 0.30f;
    FallbackInput.bPhase2OptionAvailable = bDropCandidate;
    FallbackInput.Phase2AttemptTime = 0.12f;
    const TDD::Traversal::FTDDFallbackOutput Fallback = TDD::Traversal::ResolveFallback(FallbackInput);
    UE_LOG(LogTemp, Verbose, TEXT("Traversal fallback: %s"), UTF8_TO_TCHAR(Fallback.Log.c_str()));

    if (!Fallback.bTraversed)
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
        return false; // pure 4b contract: no state or movement write on failure
    }
    FVector LaunchVelocity = FVector::ZeroVector;
    const float Gravity = FMath::Abs(World->GetGravityZ() * Movement->GravityScale);
    if (!FMath::IsFinite(Gravity) || Gravity <= KINDA_SMALL_NUMBER)
    {
        LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
        return false;
    }
    if (Fallback.bPhase1)
    {
        constexpr float LaunchVerticalSpeed = 500.0f;
        const float DeltaZ = LandingCenter.Z - Capsule->GetComponentLocation().Z;
        const float Discriminant = LaunchVerticalSpeed * LaunchVerticalSpeed - 2.0f * Gravity * DeltaZ;
        if (Discriminant < 0.0f)
        {
            LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
            return false;
        }
        const float FlightTime = (LaunchVerticalSpeed + FMath::Sqrt(Discriminant)) / Gravity;
        LaunchVelocity = Direction * (ForwardReach / FlightTime) + FVector(0.0f, 0.0f, LaunchVerticalSpeed);
    }
    else
    {
        // A controlled step-off has no upward impulse. Solve the fall time to
        // the measured landing floor, then ensure the character can cover the
        // probe reach without an implausible launch speed or an obstructed path.
        const float DeltaZ = LandingCenter.Z - Capsule->GetComponentLocation().Z;
        if (DeltaZ >= 0.0f)
        {
            LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
            return false;
        }
        const float FlightTime = FMath::Sqrt(-2.0f * DeltaZ / Gravity);
        const float HorizontalSpeed = ForwardReach / FlightTime;
        if (!FMath::IsFinite(HorizontalSpeed) || HorizontalSpeed > 500.0f)
        {
            LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
            return false;
        }
        LaunchVelocity = Direction * HorizontalSpeed;
        constexpr int32 DropArcSamples = 12;
        const FCollisionShape Shape = FCollisionShape::MakeCapsule(
            Capsule->GetScaledCapsuleRadius(), Capsule->GetScaledCapsuleHalfHeight());
        FCollisionQueryParams PathParams(SCENE_QUERY_STAT(TDDTraversalDropPath), false, Character);
        const FQuat Rotation = Capsule->GetComponentQuat();
        const FVector Start = Capsule->GetComponentLocation() + FVector(0.0f, 0.0f, 2.0f);
        FVector Previous = Start;
        for (int32 Index = 1; Index <= DropArcSamples; ++Index)
        {
            const float T = FlightTime * static_cast<float>(Index) / DropArcSamples;
            FVector Next = Start + Direction * (HorizontalSpeed * T)
                - FVector(0.0f, 0.0f, 0.5f * Gravity * T * T);
            if (Index == DropArcSamples)
            {
                Next = LandingCenter + FVector(0.0f, 0.0f, 2.0f);
            }
            if (World->SweepTestByChannel(Previous, Next, Rotation, ECC_Pawn, Shape, PathParams))
            {
                LastResult = ETDDTraversalAttemptResult::RejectedNoSafeRoute;
                return false;
            }
            Previous = Next;
        }
    }

    // All geometry and launch feasibility checks complete before mutating the
    // authoritative state machine: a rejected traversal is side-effect free.
    if (!State->RequestState(static_cast<int32>(TDD::State::ETDDPlayerState::Traversal),
                             TEXT("safe vault/drop")))
    {
        LastResult = ETDDTraversalAttemptResult::RejectedState;
        return false;
    }
    Character->LaunchCharacter(LaunchVelocity, true, true);
    LastResult = Fallback.bPhase1 ? ETDDTraversalAttemptResult::VaultStarted
                                  : ETDDTraversalAttemptResult::DropStarted;
    return true;
}
