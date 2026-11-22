// TDDPopulationActor.cpp — Phase 1 population NPC actor.
#include "TDDPopulationActor.h"

#include "Math/RandomStream.h"

ATDDPopulationActor::ATDDPopulationActor()
{
    PrimaryActorTick.bCanEverTick = true;
    // Background tier actors carry no AI and need no per-frame simulation.
    bSimulates = (Tier != ENPCTier::Background);
}

void ATDDPopulationActor::BeginPlay()
{
    Super::BeginPlay();
    bSimulates = (Tier != ENPCTier::Background);
    PrimaryActorTick.bCanEverTick = bSimulates;
    if (bSimulates)
    {
        PickNewWanderTarget();
    }
}

void ATDDPopulationActor::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (!bSimulates)
    {
        return;
    }

    WanderTimer += DeltaSeconds;
    if (WanderTimer >= 4.0f)
    {
        PickNewWanderTarget();
        WanderTimer = 0.0f;
    }

    if ((Tier == ENPCTier::Crowd || Tier == ENPCTier::Scripted) &&
        (WanderTargetCm - GetActorLocation()).Length() > 20.0f)
    {
        const FVector Dir = (WanderTargetCm - GetActorLocation()).GetSafeNormal();
        // Simplified crowd/scripted motion toward the wander target; no nav, no perception.
        const float Speed = Tier == ENPCTier::Crowd ? 28.0f : 18.0f;
        SetActorLocation(GetActorLocation() + Dir * Speed * DeltaSeconds, /*bSweep=*/false);
    }
}

void ATDDPopulationActor::PickNewWanderTarget()
{
    // FMath has no GetRandInteger: seed the stream from FMath::Rand(), the
    // same source the engine's own FRandomStream::GenerateNewSeed() uses.
    FRandomStream Rng(FMath::Rand());
    const FVector Offset = FVector(
        Rng.FRandRange(-150.0f, 150.0f),
        Rng.FRandRange(-150.0f, 150.0f),
        0.0f);
    WanderTargetCm = GetActorLocation() + Offset;
}
