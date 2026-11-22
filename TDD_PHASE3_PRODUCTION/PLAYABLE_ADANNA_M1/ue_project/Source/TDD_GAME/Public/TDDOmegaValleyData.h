// GENERATED FILE — do not hand-edit. Source: PLAYABLE_ADANNA_M1/omega_valley.json
// Regenerate with: python3 scripts/generate_omega_valley_data.py
// worldVersion: OMEGA_VALLEY_PHASE1_2026-11-22
// Classification: Phase-1 Ọmà-valley core blockout data; neutral gameplay/collision proxy.
#pragma once

#include "CoreMinimal.h"
#include "TDDWorldLogic.h"

namespace TDDOmegaValleyData
{
static constexpr float MetresToCm = 100.0f;
static constexpr float RegionMinXCm = -50000.000000f;
static constexpr float RegionMaxXCm = 500000.000000f;
static constexpr float RegionMinYCm = -120000.000000f;
static constexpr float RegionMaxYCm = 350000.000000f;
static constexpr float RouteWidthCm = 360.000000f;
static constexpr float RiverXCm = 0.000000f;
static constexpr float RiverTopYCm = 220000.000000f;
static constexpr float RiverBottomYCm = -120000.000000f;
static constexpr float RiverWidthCm = 16000.000000f;
static constexpr float ForestCentreXCm = 180000.000000f;
static constexpr float ForestCentreYCm = 250000.000000f;
static constexpr float ForestSizeCm = 120000.000000f;
static constexpr int32 ForestTreeCount = 40;
static constexpr int32 ForestSeed = 20261121;

struct FValleyRoutePoint { float XCm; float YCm; const TCHAR* Label; };
static const FValleyRoutePoint RoutePoints[] = {
    { 0.000000f, 0.000000f, TEXT("Ahanwụ gate") },
    { 100000.000000f, 0.000000f, TEXT("farmland edge") },
    { 200000.000000f, 0.000000f, TEXT("Ọmà crossing") },
    { 300000.000000f, 0.000000f, TEXT("river bank") },
    { 400000.000000f, 0.000000f, TEXT("Ọmà Ukwu market gate") },
};
static constexpr int32 RoutePointCount = 5;

struct FValleySettlement { const TCHAR* Id; const TCHAR* Name; float XCm; float YCm; EMarketDay MarketDay; };
static const FValleySettlement Settlements[] = {
    { TEXT("W-SET-AHANWU"), TEXT("Ahanwụ"), 0.000000f, 0.000000f, EMarketDay::Afo },
    { TEXT("W-SET-OMA-UKWU"), TEXT("Ọmà Ukwu"), 400000.000000f, 0.000000f, EMarketDay::Eke },
    { TEXT("W-SET-IHIALA"), TEXT("Ihiala"), 300000.000000f, 250000.000000f, EMarketDay::Nkwo },
};
static constexpr int32 SettlementCount = 3;

static const TCHAR* ObjectiveText = TEXT("Explore the Ọmà-valley core: Ahanwụ and Ọmà Ukwu, the market and the seasons.");
} // namespace TDDOmegaValleyData
