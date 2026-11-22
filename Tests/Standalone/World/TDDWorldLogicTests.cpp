// TDD World logic core tests — Igbo calendar, market-day, population density,
// route/distance and wet/dry weather model. Agent-side verification of the
// engine-agnostic Phase-1 world logic (no Unreal required).
#include "TDDWorldLogic.h"

#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iostream>

namespace
{
int Assertions = 0;
int Failures = 0;
void Check(bool Condition, const char* Description)
{
    ++Assertions;
    if (!Condition)
    {
        ++Failures;
        std::cerr << "FAIL: " << Description << '\n';
    }
}

} // namespace

int main()
{
    using namespace TDDWorld;

    // --- Market-day / calendar ---
    Check(MarketDayFromDay(0) == EMarketDay::Eke, "world day 0 is Eke");
    Check(MarketDayFromDay(1) == EMarketDay::Orie, "world day 1 is Orie");
    Check(MarketDayFromDay(2) == EMarketDay::Afo, "world day 2 is Afo");
    Check(MarketDayFromDay(3) == EMarketDay::Nkwo, "world day 3 is Nkwo");
    Check(MarketDayFromDay(4) == EMarketDay::Eke, "4-day week wraps back to Eke");
    Check(MarketDayFromDay(-1) == EMarketDay::Nkwo, "negative days wrap correctly");
    Check(MarketDayFromDay(8) == EMarketDay::Eke, "8-day cycle returns to Eke");
    Check(std::string(MarketDayName(EMarketDay::Nkwo)) == "Nkwo", "market day names are stable");

    // --- Settlement data & market-day assignment ---
    Check(OmegaValleySettlements().size() == 3, "Phase-1 core has three settlements");
    const FSettlement* Ahanwu = FindSettlement("W-SET-AHANWU");
    const FSettlement* OmaUkwu = FindSettlement("W-SET-OMA-UKWU");
    const FSettlement* Ihiala = FindSettlement("W-SET-IHIALA");
    Check(Ahanwu && OmaUkwu && Ihiala, "all three core settlements resolve by id");
    Check(Ahanwu && Ahanwu->MarketDay == EMarketDay::Afo, "Ahanwụ (CH01 home) market day is Afo");
    Check(OmaUkwu && OmaUkwu->MarketDay == EMarketDay::Eke, "Ọmà Ukwu regional hub market day is Eke");
    Check(Ihiala && Ihiala->MarketDay == EMarketDay::Nkwo, "Ihiala market day is Nkwo");
    Check(OmaUkwu && OmaUkwu->Kind == ESettlementKind::Town, "Ọmà Ukwu is a Town");

    // Phase 1 constructs ONLY Ahanwụ + Ọmà Ukwu; Ihiala is registry data, not a scope change.
    const std::vector<FSettlement>& Constructed = TDDWorld::OmegaValleyPhase1ConstructedSettlements();
    Check(Constructed.size() == 2, "Phase 1 constructs exactly two settlements");
    Check(Constructed[0].Id == "W-SET-AHANWU" && Constructed[1].Id == "W-SET-OMA-UKWU",
          "Phase-1 construction set is Ahanwụ then Ọmà Ukwu");
    Check(std::find_if(Constructed.begin(), Constructed.end(),
            [](const FSettlement& S) { return S.Id == "W-SET-IHIALA"; }) == Constructed.end(),
          "Ihiala is NOT constructed in Phase 1 (registry data only)");
    Check(std::find_if(OmegaValleySettlements().begin(), OmegaValleySettlements().end(),
            [](const FSettlement& S) { return S.Id == "W-SET-IHIALA"; }) != OmegaValleySettlements().end(),
          "Ihiala remains present in the regional registry data");
    Check(Ahanwu && Ahanwu->Kind == ESettlementKind::Village, "Ahanwụ is a Village");

    // --- Travel / route distances (believable, not 2-minute) ---
    const std::vector<FRoutePoint> Route = RoadRouteAhanwuToOmaUkwu();
    Check(Route.size() == 5, "road route has five authored waypoints");
    const float RouteLen = RouteLength(Route);
    Check(RouteLen > 3900.0f && RouteLen < 4100.0f,
          "Ahanwụ->Ọmà Ukwu route is ~4 km of real travel");
    Check(DistanceMetres(*Ahanwu, *OmaUkwu) > 3500.0f, "straight-line distance is believable");
    Check(DistanceMetres(*Ahanwu, *Ihiala) > 2500.0f, "Ihiala is a real distance from Ahanwụ");

    // --- Seasonal model (wet/dry, not 4-season) ---
    Check(SeasonForDay(0) == ESeason::Rainy, "early year is rainy");
    Check(SeasonForDay(7 * DaysPerMonth) == ESeason::Dry, "after month 6 the season is dry");
    Check(DayOfYear(0) == 0 && DayOfYear(DaysPerMonth) == DaysPerMonth, "day-of-year is cyclic");
    Check(MonthOfYear(DaysPerMonth) == 1, "month index advances with the 28-day month");

    // --- Weather consequences (not just a sky change) ---
    const FWeatherState Rain = ComputeWeather(2 * DaysPerMonth); // peak rainy
    Check(Rain.Season == ESeason::Rainy, "peak-rainy day is rainy");
    Check(Rain.MudLevel > 0.5f, "rainy weather produces mud (path consequence)");
    Check(Rain.WaterLevel > 0.5f, "rainy weather swells the river (crossing consequence)");
    Check(Rain.VegetationGreenness > 0.9f, "rainy weather is lush green");

    const FWeatherState Dry = ComputeWeather(9 * DaysPerMonth); // dry season
    Check(Dry.Season == ESeason::Dry, "late year is dry");
    Check(Dry.MudLevel < 0.1f, "dry weather has firm paths");
    Check(Dry.WaterLevel < Rain.WaterLevel, "dry weather lowers the river below rainy");
    Check(Dry.VegetationGreenness < Rain.VegetationGreenness, "dry weather browns vegetation");
    Check(Dry.OutdoorActivitySuppression < Rain.OutdoorActivitySuppression,
          "dry weather suppresses less outdoor activity than rain");

    // --- Population: logical population is independent of rendering ---
    const int32_t Logical = RegionalLogicalPopulation();
    Check(Logical >= 3000, "regional logical population is populated (not empty)");
    Check(Ahanwu && Ahanwu->Residential == 900, "Ahanwụ residential population recorded");
    Check(OmaUkwu && OmaUkwu->Residential == 2200, "Ọmà Ukwu residential population recorded");

    // Logical population is the full figure regardless of render inputs.
    FDensityInputs FarInputs;
    FarInputs.SettlementKind = ESettlementKind::Town;
    FarInputs.TimeOfDay = 0.0f; // night, far from any activation
    const FActiveTierCounts Far = ComputeActivePopulation(*OmaUkwu, FarInputs);
    Check(Logical > (Far.Named + Far.Crowd + Far.Scripted + Far.Background),
          "logical population exceeds rendered actors (sim independent of render)");

    // --- Density scaling: market day is genuinely busier than ordinary day ---
    FDensityInputs Ordinary;
    Ordinary.SettlementKind = OmaUkwu->Kind;
    Ordinary.bIsMarketDay = false;
    Ordinary.TimeOfDay = 0.5f;
    Ordinary.Weather = ComputeWeather(2 * DaysPerMonth);
    const FActiveTierCounts OrdinaryDay = ComputeActivePopulation(*OmaUkwu, Ordinary);

    FDensityInputs Market;
    Market.SettlementKind = OmaUkwu->Kind;
    Market.bIsMarketDay = true;
    Market.TimeOfDay = 0.5f;
    Market.Weather = ComputeWeather(2 * DaysPerMonth);
    const FActiveTierCounts MarketDay = ComputeActivePopulation(*OmaUkwu, Market);

    Check(MarketDay.Crowd > OrdinaryDay.Crowd, "market day swells the crowd tier");
    Check(MarketDay.Background > OrdinaryDay.Background, "market day swells the background tier");
    Check(MarketDay.Scripted > 0 && OrdinaryDay.Scripted == 0,
          "market day adds scripted performers (stalls) only on market day");
    const int32_t OrdinaryTotal =
        OrdinaryDay.Named + OrdinaryDay.Crowd + OrdinaryDay.Scripted + OrdinaryDay.Background;
    const int32_t MarketTotal =
        MarketDay.Named + MarketDay.Crowd + MarketDay.Scripted + MarketDay.Background;
    Check(MarketTotal > OrdinaryTotal * 2, "market day is more than twice as populated");

    // Market-day surge is bounded (sane rendered budget at HIGH density).
    Check(MarketDay.Crowd <= 90, "market crowd stays within the AI render budget");
    // Background is instanced/no-AI; the HIGH profile ceiling is ~700, kept high
    // enough that weather suppression remains observable on a market day.
    Check(MarketDay.Background <= 700, "market background stays within the HIGH instanced budget");

    // --- Market system: correct settlement active on its assigned day ---
    // Ọmà Ukwu is Eke => active on world days 0, 4, 8...
    const FMarketState OmaOnEke = ComputeMarketState(*OmaUkwu, 0, 0.5f);
    Check(OmaOnEke.bActive, "Ọmà Ukwu market is active on Eke");
    const FMarketState OmaOnOrie = ComputeMarketState(*OmaUkwu, 1, 0.5f);
    Check(!OmaOnOrie.bActive, "Ọmà Ukwu market is inactive on Orie");
    // Ahanwụ is Afo => active on world day 2.
    const FMarketState AhanwuOnAfo = ComputeMarketState(*Ahanwu, 2, 0.5f);
    Check(AhanwuOnAfo.bActive, "Ahanwụ market is active on Afo");
    const FMarketState AhanwuOnEke = ComputeMarketState(*Ahanwu, 0, 0.5f);
    Check(!AhanwuOnEke.bActive, "Ahanwụ market is inactive on Eke");

    // --- Time-of-day: market peaks midday, disperses at dawn ---
    const FMarketState Midday = ComputeMarketState(*OmaUkwu, 0, 0.5f);
    const FMarketState Dawn = ComputeMarketState(*OmaUkwu, 0, 0.05f);
    Check(Midday.ActivePopulation.Crowd >= Dawn.ActivePopulation.Crowd,
          "market crowd peaks at midday vs dawn");

    // --- Weather affects market (market-in-rain vs market-in-dry) ---
    const FSettlement& Oma = *OmaUkwu;
    FDensityInputs RainMarket;
    RainMarket.SettlementKind = Oma.Kind;
    RainMarket.bIsMarketDay = true;
    RainMarket.TimeOfDay = 0.5f;
    RainMarket.Weather = ComputeWeather(2 * DaysPerMonth);
    FDensityInputs DryMarket = RainMarket;
    DryMarket.Weather = ComputeWeather(9 * DaysPerMonth);
    const FActiveTierCounts RainMkt = ComputeActivePopulation(Oma, RainMarket);
    const FActiveTierCounts DryMkt = ComputeActivePopulation(Oma, DryMarket);
    Check(RainMkt.Background < DryMkt.Background,
          "a rainy market is less populated than a dry-season market");

    if (Failures)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; "
                  << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
