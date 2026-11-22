// TDDWorldPopulationSubsystem.cpp — Phase 1 world population simulation.
#include "TDDWorldPopulationSubsystem.h"

#include "Subsystems/WorldSubsystem.h"

UTDDWorldPopulationSubsystem::UTDDWorldPopulationSubsystem()
{
    // UWorldSubsystem has no PrimaryComponentTick toggle; this subsystem
    // does not override Tick, so the empty base Tick incurs no per-frame cost.
}

void UTDDWorldPopulationSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    SettlementIds.Reset();
    SettlementLogicalPopulation.Reset();
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        SettlementIds.Add(FName(S.Id.c_str()));
        SettlementLogicalPopulation.Add(FName(S.Id.c_str()), S.Residential + S.Economic);
    }

    UE_LOG(LogTemp, Display,
           TEXT("TDD PopulationSubsystem: logical population = %d across %d settlements (independent of rendering)."),
           TDDWorld::RegionalLogicalPopulation(), SettlementIds.Num());
}

int32 UTDDWorldPopulationSubsystem::GetRegionalLogicalPopulation() const
{
    return TDDWorld::RegionalLogicalPopulation();
}

int32 UTDDWorldPopulationSubsystem::GetSettlementLogicalPopulation(const FName& SettlementId) const
{
    // TMap has no ValueOrDefault: look up the key and fall back to 0.
    const int32* Found = SettlementLogicalPopulation.Find(SettlementId);
    return Found ? *Found : 0;
}

int32 UTDDWorldPopulationSubsystem::GetLogicalPopulationSnapshot() const
{
    // The full logical population is always available, regardless of how many
    // actors are currently spawned/rendered. This is the demonstration that the
    // simulation is independent of the render budget.
    return TDDWorld::RegionalLogicalPopulation();
}

FTDDActiveTierCounts UTDDWorldPopulationSubsystem::ComputeActivePopulation(
    const FName& SettlementId,
    int64 WorldDay,
    float TimeOfDay,
    bool bIsMarketDay,
    bool bIsFestival) const
{
    const TDDWorld::FSettlement* Settlement = nullptr;
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        if (FName(S.Id.c_str()) == SettlementId)
        {
            Settlement = &S;
            break;
        }
    }

    FTDDActiveTierCounts Out;
    if (!Settlement)
    {
        UE_LOG(LogTemp, Warning, TEXT("TDD PopulationSubsystem: unknown settlement '%s'"), *SettlementId.ToString());
        return Out;
    }

    TDDWorld::FDensityInputs In;
    In.SettlementKind = Settlement->Kind;
    In.bIsMarketDay = bIsMarketDay;
    In.bIsFestival = bIsFestival;
    In.TimeOfDay = TimeOfDay;
    In.Weather = TDDWorld::ComputeWeather(WorldDay);

    const TDDWorld::FActiveTierCounts Counts = TDDWorld::ComputeActivePopulation(*Settlement, In);
    Out.Named = Counts.Named;
    Out.Crowd = Counts.Crowd;
    Out.Scripted = Counts.Scripted;
    Out.Background = Counts.Background;
    return Out;
}
