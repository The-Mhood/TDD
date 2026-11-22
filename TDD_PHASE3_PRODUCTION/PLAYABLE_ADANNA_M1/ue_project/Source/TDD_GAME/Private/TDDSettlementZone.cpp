// TDDSettlementZone.cpp — Phase 1 settlement anchor actor.
#include "TDDSettlementZone.h"

#include "Components/SceneComponent.h"

#include "TDDPopulationActor.h"
#include "TDDMarketStall.h"
#include "TDDWorldPopulationSubsystem.h"
#include "TDDCalendarSubsystem.h"
#include "Engine/World.h"

ATDDSettlementZone::ATDDSettlementZone()
{
    PrimaryActorTick.bCanEverTick = false;
    ZoneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("ZoneRoot"));
    SetRootComponent(ZoneRoot);
}

void ATDDSettlementZone::BeginPlay()
{
    Super::BeginPlay();

    // Resolve the settlement from the shared logic core and record its FULL
    // logical population. This figure exists regardless of how many actors we
    // actually spawn below.
    const TDDWorld::FSettlement* S = nullptr;
    for (const TDDWorld::FSettlement& Candidate : TDDWorld::OmegaValleySettlements())
    {
        if (FName(Candidate.Id.c_str()) == SettlementId)
        {
            S = &Candidate;
            break;
        }
    }
    if (!S)
    {
        UE_LOG(LogTemp, Warning, TEXT("TDD SettlementZone: unknown settlement id '%s'"), *SettlementId.ToString());
        return;
    }
    SettlementName = S->Name.c_str();
    LogicalPopulation = S->Residential + S->Economic;

    RefreshPopulation(0, 0.25f);
    UE_LOG(LogTemp, Display,
           TEXT("TDD SettlementZone '%s': logical population %d (rendered subset %d)."),
           *SettlementName, LogicalPopulation, SpawnedPopulation.Num());
}

void ATDDSettlementZone::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
}

void ATDDSettlementZone::RefreshPopulation(int64 WorldDay, float TimeOfDay)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    UTDDWorldPopulationSubsystem* Population = World->GetSubsystem<UTDDWorldPopulationSubsystem>();
    if (!Population)
    {
        return;
    }

    // Market-day presence is determined by the calendar/market subsystems.
    bool bMarket = false;
    if (UTDDCalendarSubsystem* Calendar = World->GetSubsystem<UTDDCalendarSubsystem>())
    {
        bMarket = Calendar->IsMarketDayFor(SettlementId);
    }

    // Clear and respawn toward the density model for the current state.
    ClearPopulation();
    ClearMarketStalls();

    const FTDDActiveTierCounts Counts =
        Population->ComputeActivePopulation(SettlementId, WorldDay, TimeOfDay, bMarket, /*bIsFestival=*/false);

    bMarketActive = bMarket;
    // SpawnPopulationTiers consumes the pure-logic TDDWorld::FActiveTierCounts;
    // map the reflected FTDDActiveTierCounts field-by-field (same values).
    TDDWorld::FActiveTierCounts LogicCounts;
    LogicCounts.Named = Counts.Named;
    LogicCounts.Crowd = Counts.Crowd;
    LogicCounts.Scripted = Counts.Scripted;
    LogicCounts.Background = Counts.Background;
    SpawnPopulationTiers(LogicCounts);

    if (bMarket)
    {
        // Stalls appear on the settlement's market day.
        SpawnMarketStalls(MarketStallCount);
    }

    UE_LOG(LogTemp, Display,
           TEXT("TDD SettlementZone '%s' (%s): logical %d, spawned %d (named %d, crowd %d, scripted %d, background %d)."),
           *SettlementName, bMarket ? TEXT("market day") : TEXT("ordinary"),
           LogicalPopulation, SpawnedPopulation.Num(),
           Counts.Named, Counts.Crowd, Counts.Scripted, Counts.Background);
}

void ATDDSettlementZone::SpawnPopulationTiers(const TDDWorld::FActiveTierCounts& Counts)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const auto SpawnOne = [&](ENPCTier Tier, int32 Count) {
        for (int32 i = 0; i < Count; ++i)
        {
            const int32 OffsetIndex = i % 8;
            const FVector Location = ZoneRoot->GetComponentLocation() +
                                     PopulationSpawnOffsetsCm[OffsetIndex];
            FActorSpawnParameters Info;
            Info.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
            if (ATDDPopulationActor* Actor =
                    World->SpawnActor<ATDDPopulationActor>(Location, FRotator::ZeroRotator, Info))
            {
                Actor->SetTier(Tier);
                // FString has no ToString(); SetOccupation takes the FString directly.
                Actor->SetOccupation(SettlementName);
                SpawnedPopulation.Add(Actor);
            }
        }
    };

    SpawnOne(ENPCTier::Named, Counts.Named);
    SpawnOne(ENPCTier::Crowd, Counts.Crowd);
    SpawnOne(ENPCTier::Scripted, Counts.Scripted);
    SpawnOne(ENPCTier::Background, Counts.Background);
}

void ATDDSettlementZone::SpawnMarketStalls(int32 Count)
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }
    // TODO(Phase1): stall count from market subsystem per settlement product identity.
    for (int32 i = 0; i < Count; ++i)
    {
        const FVector Location = ZoneRoot->GetComponentLocation() + FVector(i * 120.0f, 0.0f, 0.0f);
        FActorSpawnParameters Info;
        Info.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
        if (ATDDMarketStall* Stall = World->SpawnActor<ATDDMarketStall>(Location, FRotator::ZeroRotator, Info))
        {
            Stall->SetOpen(true);
            SpawnedStalls.Add(Stall);
        }
    }
}

void ATDDSettlementZone::ClearPopulation()
{
    for (ATDDPopulationActor* Actor : SpawnedPopulation)
    {
        if (Actor)
        {
            Actor->Destroy();
        }
    }
    SpawnedPopulation.Reset();
}

void ATDDSettlementZone::ClearMarketStalls()
{
    for (ATDDMarketStall* Stall : SpawnedStalls)
    {
        if (Stall)
        {
            Stall->Destroy();
        }
    }
    SpawnedStalls.Reset();
}
