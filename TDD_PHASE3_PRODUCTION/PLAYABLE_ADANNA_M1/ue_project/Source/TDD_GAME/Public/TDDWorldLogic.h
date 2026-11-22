// TDDWorldLogic.h — Engine-agnostic world logic core for the Ọmà Ala (Phase 1).
//
// PURE C++20. No Unreal headers, no allocation, no I/O. This header holds the
// logical world model that the UE layer (TDD_GAME subsystems) consumes AND that
// the agent-side pure-logic tests (Tests/Standalone/TDDWorldLogicTests.cpp)
// compile against with g++. Keeping the calendar, market-day, population-density,
// route and weather models here means they are verifiable without Unreal while
// remaining the single source of truth the runtime uses.
//
// Design principle: the LOGICAL population (households, occupations, routines,
// destinations) is modelled independently of how many NPCs are rendered. Render
// activation is a distance/budget concern applied on top of these numbers.
//
// Research basis: Igbo 4-day market week (Eke/Orie/Afo/Nkwo), 13-month year,
// wet/dry tropical seasons, settlement hierarchy, occupational craft economy.
// See docs/06_IMPLEMENTATION/WORLD/WORLD_SOURCE_AND_EVIDENCE_REGISTER.md.

#pragma once

#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

// UENUM is provided by the engine (CoreMinimal.h) when this header is compiled
// under Unreal. Provide an empty fallback so the pure-C++ g++ logic tests still
// compile. The UENUM annotations make these enums reflectable by UHT for the
// UPROPERTY/UFUNCTION members that expose them to Blueprint.
#ifndef UENUM
#define UENUM(x)
#endif

// UHT requires the ENGINE typedef (uint8) as a UENUM enum underlying type, not
// the C++ stdint alias (uint8_t). Provide a portable fallback so the pure-C++
// g++ logic tests still compile (uint8 == unsigned char == uint8_t; identical
// size and behaviour, so no serialization/reflection change).
#ifndef uint8
typedef unsigned char uint8;
#endif

// UENUM-annotated enums live at GLOBAL scope (UHT requires UENUM enums to be
// global, not nested in a namespace). They remain accessible from within
// namespace TDDWorld via unqualified name lookup.
UENUM(BlueprintType)
enum class EMarketDay : uint8
{
    Eke = 0,
    Orie = 1,
    Afo = 2,
    Nkwo = 3,
    Count
};

UENUM(BlueprintType)
enum class ESettlementKind : uint8
{
    Village,
    MarketTown,
    Town
};

UENUM(BlueprintType)
enum class ENPCTier : uint8
{
    Named,       // Tier 1: full AI + animation, dialogue/quest hooks
    Crowd,       // Tier 2: simplified AI, instanced, bark only
    Scripted,    // Tier 3: fixed loop, no AI/perception/nav
    Background,  // Tier 4: instanced, no tick, ambient life
    Count
};

UENUM(BlueprintType)
enum class ESeason : uint8
{
    Rainy,
    Dry,
    Count
};

namespace TDDWorld
{

// ---------------------------------------------------------------------------
// Market days — the Igbo 4-day week (Eke -> Orie -> Afo -> Nkwo).
// ---------------------------------------------------------------------------


inline const char* MarketDayName(EMarketDay Day)
{
    switch (Day)
    {
    case EMarketDay::Eke:  return "Eke";
    case EMarketDay::Orie: return "Orie";
    case EMarketDay::Afo:  return "Afo";
    case EMarketDay::Nkwo: return "Nkwo";
    default:               return "?";
    }
}

// World Day 0 == Eke. The 4-day week repeats indefinitely.
inline EMarketDay MarketDayFromDay(int64_t WorldDay)
{
    const int64_t Wrapped = WorldDay < 0 ? ((WorldDay % 4) + 4) % 4 : WorldDay % 4;
    return static_cast<EMarketDay>(Wrapped);
}

// ---------------------------------------------------------------------------
// Settlement & location data (the Ọmà-valley Phase-1 core).
// Coordinates are world-space metres (XY plane), origin = Ọmà crossing below
// Ahanwụ. Distances are traversal metres.
// ---------------------------------------------------------------------------



struct FSettlement
{
    std::string Id;
    std::string Name;         // native Igbo name
    ESettlementKind Kind;
    EMarketDay MarketDay;     // assigned main market day ([A] adaptive — see source register)
    float X = 0.0f;           // world-space metres
    float Y = 0.0f;
    int32_t Residential = 0;    // persistent household population
    int32_t Economic = 0;       // occupation-driven working population
    // Craft/product identity for settlement differentiation.
    std::string PrimaryProduct;
};

// The Phase-1 Ọmà-valley core settlements. Ọmà Ukwu = Eke (regional hub),
// Ahanwụ = CH01 home settlement (market-day surge Afo), Ihiala village.
inline const std::vector<FSettlement>& OmegaValleySettlements()
{
    static const std::vector<FSettlement> Data = {
        { "W-SET-AHANWU", "Ahanwụ", ESettlementKind::Village, EMarketDay::Afo,
          0.0f, 0.0f, 900, 260, "yam" },
        { "W-SET-OMA-UKWU", "Ọmà Ukwu", ESettlementKind::Town, EMarketDay::Eke,
          4000.0f, 0.0f, 2200, 640, "trade/river-port" },
        { "W-SET-IHIALA", "Ihiala", ESettlementKind::Village, EMarketDay::Nkwo,
          3000.0f, 2500.0f, 750, 210, "fish/palm" },
    };
    return Data;
}

// The settlements actually CONSTRUCTED in Phase 1 (the Ọmà-valley core build
// target): Ahanwụ and Ọmà Ukwu. Ihiala is regional registry data (present in
// OmegaValleySettlements above and in the market network) but is NOT constructed
// in Phase 1 — it is future-facing data, not a Phase-1 scope change.
inline const std::vector<FSettlement>& OmegaValleyPhase1ConstructedSettlements()
{
    static const std::vector<FSettlement> Data = {
        OmegaValleySettlements()[0], // Ahanwụ
        OmegaValleySettlements()[1], // Ọmà Ukwu
    };
    return Data;
}

inline const FSettlement* FindSettlement(const std::string& Id)
{
    for (const FSettlement& S : OmegaValleySettlements())
    {
        if (S.Id == Id)
        {
            return &S;
        }
    }
    return nullptr;
}

// ---------------------------------------------------------------------------
// Route & travel — believable distances, traversal metres.
// ---------------------------------------------------------------------------

struct FRoutePoint
{
    std::string Label;
    float X = 0.0f;
    float Y = 0.0f;
};

inline float RouteSegmentLength(const FRoutePoint& A, const FRoutePoint& B)
{
    const float DX = B.X - A.X;
    const float DY = B.Y - A.Y;
    return std::sqrt(DX * DX + DY * DY);
}

inline float RouteLength(const std::vector<FRoutePoint>& Route)
{
    float Length = 0.0f;
    for (std::size_t i = 1; i < Route.size(); ++i)
    {
        Length += RouteSegmentLength(Route[i - 1], Route[i]);
    }
    return Length;
}

// Straight-line distance between two world points (metres).
inline float DistanceMetres(const FSettlement& A, const FSettlement& B)
{
    return RouteSegmentLength(FRoutePoint{ A.Id, A.X, A.Y }, FRoutePoint{ B.Id, B.X, B.Y });
}

// A road route between two settlements (footpath/canoe spine). Phase-1 core:
// Ahanwụ -> Ọmà Ukwu along the Ọmà river/road.
inline std::vector<FRoutePoint> RoadRouteAhanwuToOmaUkwu()
{
    return {
        { "Ahanwụ gate", 0.0f, 0.0f },
        { "farmland edge", 1000.0f, 0.0f },
        { "Ọmà crossing", 2000.0f, 0.0f },
        { "river bank", 3000.0f, 0.0f },
        { "Ọmà Ukwu market gate", 4000.0f, 0.0f },
    };
}

// ---------------------------------------------------------------------------
// Calendar & seasonal model.
// ---------------------------------------------------------------------------


inline const char* SeasonName(ESeason Season)
{
    switch (Season)
    {
    case ESeason::Rainy: return "Rainy";
    case ESeason::Dry:   return "Dry";
    default:             return "?";
    }
}

// 13-month Igbo year (afọ). Month index 0..12; month 12 is the intercalary.
// Each month is 7 four-day weeks = 28 days. The rainy/dry boundary is a
// seasonal mapping (researched/adapted — see source register).
constexpr int32_t DaysPerMonth = 28;
constexpr int32_t MonthsPerYear = 13;
constexpr int32_t DaysPerYear = DaysPerMonth * MonthsPerYear; // 364 + intercalary

inline int32_t DayOfYear(int64_t WorldDay)
{
    const int64_t Wrapped = WorldDay < 0 ? ((WorldDay % DaysPerYear) + DaysPerYear) % DaysPerYear
                                         : WorldDay % DaysPerYear;
    return static_cast<int32_t>(Wrapped);
}

inline int32_t MonthOfYear(int64_t WorldDay)
{
    return DayOfYear(WorldDay) / DaysPerMonth;
}

// Season from the day-of-year. Months 0..6 = rainy (wet), 7..12 = dry.
// Researched/adapted: the Igbo homeland has a wet season and a dry season.
inline ESeason SeasonForDay(int64_t WorldDay)
{
    return MonthOfYear(WorldDay) <= 6 ? ESeason::Rainy : ESeason::Dry;
}

// ---------------------------------------------------------------------------
// Weather model — wet/dry with observable gameplay consequences.
// Not a sky-only model: it drives path condition, water level, visibility,
// vegetation and NPC activity.
// ---------------------------------------------------------------------------

struct FWeatherState
{
    ESeason Season = ESeason::Rainy;
    // 0.0 (bone dry) .. 1.0 (peak rain). Derived from season + intra-season phase.
    float RainIntensity = 0.0f;
    // 0.0 (paths firm) .. 1.0 (deep mud). Consequence of rain.
    float MudLevel = 0.0f;
    // 0.0 (river low) .. 1.0 (river flooded; crossing may break).
    float WaterLevel = 0.0f;
    // 0.0 (clear) .. 1.0 (heavy cloud/haze, low visibility).
    float VisibilityFalloff = 0.0f;
    // 0.0 (dry/brown) .. 1.0 (dense lush green).
    float VegetationGreenness = 0.0f;
    // 0.0 (normal outdoor activity) .. 1.0 (activity suppressed; shelter).
    float OutdoorActivitySuppression = 0.0f;
};

// Compute the full weather state for a world day. Pure function of the calendar.
inline FWeatherState ComputeWeather(int64_t WorldDay)
{
    FWeatherState W;
    W.Season = SeasonForDay(WorldDay);

    const int32_t Doy = DayOfYear(WorldDay);
    // Intra-season phase within the ~7-month season (0..~28 days granularity).
    const int32_t InSeasonDay = W.Season == ESeason::Rainy ? Doy : (Doy - 7 * DaysPerMonth);
    const int32_t SeasonDays = W.Season == ESeason::Rainy ? 7 * DaysPerMonth : 6 * DaysPerMonth + 1;
    const float Phase = SeasonDays > 0
                            ? static_cast<float>(InSeasonDay) / static_cast<float>(SeasonDays)
                            : 0.0f;

    if (W.Season == ESeason::Rainy)
    {
        // Rain builds to a mid-season peak, then eases toward the dry transition.
        const float Triangle = 1.0f - std::abs(2.0f * Phase - 1.0f);
        W.RainIntensity = Triangle;
        W.MudLevel = Triangle;                 // rain turns paths to mud
        // River stays high through the rainy season (recharged by rain), peaking mid-season.
        W.WaterLevel = 0.60f + 0.40f * Triangle;
        W.VisibilityFalloff = Triangle * 0.6f;
        W.VegetationGreenness = 1.0f;          // rainy = lush
        W.OutdoorActivitySuppression = Triangle * 0.5f;
    }
    else
    {
        // Dry season: river falls and is drawn down through the dry, land dries,
        // visibility clears, vegetation browns.
        const float DryPhase = std::min(1.0f, Phase);
        W.RainIntensity = 0.0f;
        W.MudLevel = 0.0f;
        W.WaterLevel = 0.40f - 0.30f * DryPhase; // river recedes through the dry season
        W.VisibilityFalloff = 0.05f;            // a little dry haze
        W.VegetationGreenness = 1.0f - DryPhase * 0.55f; // dries/browns
        W.OutdoorActivitySuppression = 0.0f;     // dry = full activity
    }
    return W;
}

// ---------------------------------------------------------------------------
// Population density model.
//
// The LOGICAL population is the settlement's residential + economic figures.
// RENDERED population (active actors) is a budgeted subset computed here from
// density factors: location, market-day, time-of-day, event, weather.
// This is the mechanism that makes a scheduled market genuinely busy without
// spawning the whole regional population as full-AI actors.
// ---------------------------------------------------------------------------

struct FDensityInputs
{
    ESettlementKind SettlementKind = ESettlementKind::Village;
    bool bIsMarketDay = false;          // is today this settlement's market day?
    float TimeOfDay = 0.25f;           // 0..1 across the day (market peaks midday)
    bool bIsFestival = false;           // Iri Ji / gathering / story event
    FWeatherState Weather = FWeatherState{};
};

struct FActiveTierCounts
{
    int32_t Named = 0;
    int32_t Crowd = 0;
    int32_t Scripted = 0;
    int32_t Background = 0;
};

// Relative cost units per actor (WORLD_ARCHITECTURE five-tier model).
inline int32_t TierCostUnits(ENPCTier Tier)
{
    switch (Tier)
    {
    case ENPCTier::Named:       return 4;
    case ENPCTier::Crowd:       return 1;
    case ENPCTier::Scripted:    return 0; // handled per-scene, not per-actor here
    case ENPCTier::Background:  return 0;
    default:                    return 0;
    }
}

// Compute the active (rendered) tier counts for a settlement given the inputs.
// The logical population is passed in; the returned counts are a budgeted,
// distance-independent SNAPSHOT that the UE layer spawns toward.
inline FActiveTierCounts ComputeActivePopulation(
    const FSettlement& Settlement,
    const FDensityInputs& In)
{
    const int32_t Residential = Settlement.Residential;
    const int32_t Economic = Settlement.Economic;
    const int32_t LogicalTotal = Residential + Economic;

    // Base rendered population is a fraction of the logical population, scaled
    // by settlement kind. Towns render more; villages less.
    float BaseFraction = 0.0f;
    switch (Settlement.Kind)
    {
    case ESettlementKind::Town:       BaseFraction = 0.12f; break;
    case ESettlementKind::MarketTown: BaseFraction = 0.10f; break;
    case ESettlementKind::Village:    BaseFraction = 0.08f; break;
    default:                          BaseFraction = 0.08f; break;
    }

    // Market-day surge: a busy market draws traders/customers from the region.
    float MarketMultiplier = 1.0f;
    if (In.bIsMarketDay)
    {
        MarketMultiplier = 3.2f;
    }
    // Festival/gathering adds a focused public surge.
    float EventMultiplier = In.bIsFestival ? 1.8f : 1.0f;

    // Time-of-day curve: market activity peaks midday, disperses at dawn/dusk.
    // For ordinary days, a gentler daytime curve.
    float TimeCurve = 0.0f;
    if (In.bIsMarketDay)
    {
        // Triangular peak at 0.5.
        TimeCurve = 1.0f - std::abs(2.0f * In.TimeOfDay - 1.0f);
    }
    else
    {
        // Daytime presence, low at night.
        TimeCurve = std::max(0.0f, 1.0f - std::abs(2.0f * In.TimeOfDay - 1.0f) * 0.4f);
    }

    // Weather suppresses outdoor activity in heavy rain.
    float WeatherCurve = 1.0f - In.Weather.OutdoorActivitySuppression;

    const float DensityFactor = BaseFraction * MarketMultiplier * EventMultiplier *
                                TimeCurve * WeatherCurve;
    const float ActiveTotal = static_cast<float>(LogicalTotal) * DensityFactor;

    // Tier split: a small named core, a crowd body, scripted performers, and a
    // background layer. The background tier carries the ambient "people live
    // here" feel at near-zero AI cost.
    FActiveTierCounts Out;
    Out.Named = static_cast<int32_t>(ActiveTotal * 0.04f);            // ~4% named
    Out.Crowd = static_cast<int32_t>(ActiveTotal * 0.30f);            // ~30% crowd
    Out.Scripted = In.bIsMarketDay ? static_cast<int32_t>(ActiveTotal * 0.06f) : 0;
    Out.Background = static_cast<int32_t>(ActiveTotal * 0.60f);        // ~60% background

    // Floors/caps so a tiny settlement still reads as populated, and a huge
    // settlement on market day stays within a sane rendered budget.
    Out.Named = std::max(1, Out.Named);
    Out.Crowd = std::max(2, Out.Crowd);
    if (In.bIsMarketDay)
    {
        // Crowd is the AI-costly tier: keep it tightly budgeted. Background is
        // instanced with no AI, so it can carry the populated-market feel at a
        // higher ceiling — but high enough that weather suppression remains
        // observable (a rainy market stays visibly thinner than a dry one).
        Out.Crowd = std::min(Out.Crowd, 90);
        Out.Background = std::min(Out.Background, 700);
    }
    else
    {
        Out.Background = std::min(Out.Background, 90);
    }
    return Out;
}

// Total simulated (logical) population across the region — independent of rendering.
inline int32_t RegionalLogicalPopulation()
{
    int32_t Total = 0;
    for (const FSettlement& S : OmegaValleySettlements())
    {
        Total += S.Residential + S.Economic;
    }
    return Total;
}

// ---------------------------------------------------------------------------
// Market system — which settlement's market is active on a given world day,
// and its density surge.
// ---------------------------------------------------------------------------

struct FMarketState
{
    const FSettlement* Settlement = nullptr;
    bool bActive = false;
    FActiveTierCounts ActivePopulation{};
};

inline FMarketState ComputeMarketState(
    const FSettlement& Settlement,
    int64_t WorldDay,
    float TimeOfDay)
{
    FMarketState Out;
    const EMarketDay Today = MarketDayFromDay(WorldDay);
    Out.bActive = (Today == Settlement.MarketDay);
    Out.Settlement = &Settlement;

    FDensityInputs In;
    In.SettlementKind = Settlement.Kind;
    In.bIsMarketDay = Out.bActive;
    In.TimeOfDay = TimeOfDay;
    In.Weather = ComputeWeather(WorldDay);
    Out.ActivePopulation = ComputeActivePopulation(Settlement, In);
    return Out;
}

} // namespace TDDWorld
