// TDDCalendarSubsystem.cpp — Phase 1 Igbo calendar.
#include "TDDCalendarSubsystem.h"

#include "Subsystems/WorldSubsystem.h"

UTDDCalendarSubsystem::UTDDCalendarSubsystem()
{
    // UTickableWorldSubsystem is the UE 5.8 base for world subsystems that need
    // per-frame ticking: the engine calls Tick every frame only for tickable
    // world subsystems. The calendar advances the market-day clock from Tick.
}

void UTDDCalendarSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    WorldDay = 0;
    DayTimer = 0.0f;
    UE_LOG(LogTemp, Display,
           TEXT("TDD CalendarSubsystem: world day 0 = %s, season %s."),
           *GetCurrentMarketDayName(), *FString(TDDWorld::SeasonName(GetCurrentSeason())));
}

void UTDDCalendarSubsystem::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    DayTimer += DeltaSeconds;
    if (DayTimer >= SecondsPerMarketDay)
    {
        DayTimer -= SecondsPerMarketDay;
        AdvanceDay();
    }
}

TStatId UTDDCalendarSubsystem::GetStatId() const
{
    // Cycle-stat declaration for the profiler/stats system. RETURN_QUICK_DECLARE_CYCLE_STAT
    // both declares and returns the TStatId that identifies this tickable subsystem.
    return RETURN_QUICK_DECLARE_CYCLE_STAT(UTDDCalendarSubsystem, STATGROUP_Tickables);
}

void UTDDCalendarSubsystem::AdvanceDay()
{
    ++WorldDay;
    UE_LOG(LogTemp, Display,
           TEXT("TDD CalendarSubsystem: advanced to world day %lld = %s (%s)."),
           WorldDay, *GetCurrentMarketDayName(), *FString(TDDWorld::SeasonName(GetCurrentSeason())));
}

void UTDDCalendarSubsystem::AdvanceDays(int32 Days)
{
    WorldDay += Days;
}

FString UTDDCalendarSubsystem::GetCurrentMarketDayName() const
{
    return FString(TDDWorld::MarketDayName(GetCurrentMarketDay()));
}

bool UTDDCalendarSubsystem::IsMarketDayFor(const FName& SettlementId) const
{
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        if (FName(S.Id.c_str()) == SettlementId)
        {
            return GetCurrentMarketDay() == S.MarketDay;
        }
    }
    return false;
}
