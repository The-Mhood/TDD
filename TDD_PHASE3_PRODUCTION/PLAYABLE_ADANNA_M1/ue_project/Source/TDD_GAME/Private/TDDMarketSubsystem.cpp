// TDDMarketSubsystem.cpp — Phase 1 market-day system.
#include "TDDMarketSubsystem.h"

#include "Subsystems/WorldSubsystem.h"

UTDDMarketSubsystem::UTDDMarketSubsystem()
{
    // UWorldSubsystem has no PrimaryComponentTick toggle; this subsystem
    // does not override Tick, so the empty base Tick incurs no per-frame cost.
}

void UTDDMarketSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    SettlementIds.Reset();
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        SettlementIds.Add(FName(S.Id.c_str()));
    }
    UE_LOG(LogTemp, Display, TEXT("TDD MarketSubsystem: %d settlements in the market network."), SettlementIds.Num());
}

FTDDMarketState UTDDMarketSubsystem::ComputeMarketState(
    const FName& SettlementId,
    int64 WorldDay,
    float TimeOfDay) const
{
    FTDDMarketState Out;
    Out.SettlementId = SettlementId;

    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        if (FName(S.Id.c_str()) != SettlementId)
        {
            continue;
        }

        const TDDWorld::FMarketState Market = TDDWorld::ComputeMarketState(S, WorldDay, TimeOfDay);
        Out.SettlementName = S.Name.c_str();
        Out.bActive = Market.bActive;
        Out.MarketDay = S.MarketDay;
        Out.CrowdPopulation = Market.ActivePopulation.Crowd;
        Out.BackgroundPopulation = Market.ActivePopulation.Background;

        if (Market.bActive)
        {
            // Traders and stalls scale with the market crowd; the regional hub
            // (town) runs the largest market. ESettlementKind is a global-scope
            // UENUM, so it is referenced unqualified.
            Out.Traders = FMath::Max(6, Market.ActivePopulation.Crowd * 2);
            Out.Stalls = S.Kind == ESettlementKind::Town ? 24 : 14;
        }
        break;
    }
    return Out;
}

FName UTDDMarketSubsystem::GetActiveMarketToday(int64 WorldDay, float TimeOfDay) const
{
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        if (TDDWorld::ComputeMarketState(S, WorldDay, TimeOfDay).bActive)
        {
            return FName(S.Id.c_str());
        }
    }
    return FName();
}
