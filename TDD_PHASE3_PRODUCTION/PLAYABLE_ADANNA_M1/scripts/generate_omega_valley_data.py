#!/usr/bin/env python3
"""Generate a C++ source header from the Ọmà-valley Phase-1 blockout JSON.

Mirrors the PLAYABLE_ADANNA_M1 world.json -> TDDWorldData.h pipeline so the
Phase-1 valley level reads Design-editable geometry data (region bounds, route,
river, forest, settlement screen positions) from a generated header rather than
hard-coded constants. The authoritative settlement/population/calendar/market
logic stays in TDDWorldLogic.h; this header is the blockout-geometry data asset.
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
WORLD = BASE / "omega_valley.json"
OUT = BASE / "ue_project" / "Source" / "TDD_GAME" / "Public" / "TDDOmegaValleyData.h"


def f(value: object) -> str:
    return "{:.6f}f".format(float(value))


def cpp_text(value: object) -> str:
    return 'TEXT(' + json.dumps(str(value), ensure_ascii=False) + ')'


MARKET_DAY_ENUM = {"Eke": "EMarketDay::Eke", "Orie": "EMarketDay::Orie",
                   "Afo": "EMarketDay::Afo", "Nkwo": "EMarketDay::Nkwo"}


def main() -> None:
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    region = world["region"]
    route = world["route"]
    river = world["river"]
    forest = world["forest"]

    lines: list[str] = []
    lines.append("// GENERATED FILE — do not hand-edit. Source: PLAYABLE_ADANNA_M1/omega_valley.json")
    lines.append("// Regenerate with: python3 scripts/generate_omega_valley_data.py")
    lines.append("// worldVersion: " + world["worldVersion"])
    lines.append("// Classification: Phase-1 Ọmà-valley core blockout data; neutral gameplay/collision proxy.")
    lines.append("#pragma once")
    lines.append("")
    lines.append('#include "CoreMinimal.h"')
    lines.append('#include "TDDWorldLogic.h"')
    lines.append("")
    lines.append("namespace TDDOmegaValleyData")
    lines.append("{")
    lines.append("static constexpr float MetresToCm = 100.0f;")
    lines.append("static constexpr float RegionMinXCm = " + f(float(region["minX"]) * 100.0) + ";")
    lines.append("static constexpr float RegionMaxXCm = " + f(float(region["maxX"]) * 100.0) + ";")
    lines.append("static constexpr float RegionMinYCm = " + f(float(region["minY"]) * 100.0) + ";")
    lines.append("static constexpr float RegionMaxYCm = " + f(float(region["maxY"]) * 100.0) + ";")
    lines.append("static constexpr float RouteWidthCm = " + f(float(route["pathWidth"]) * 100.0) + ";")
    lines.append("static constexpr float RiverXCm = " + f(float(river["x"]) * 100.0) + ";")
    lines.append("static constexpr float RiverTopYCm = " + f(float(river["topY"]) * 100.0) + ";")
    lines.append("static constexpr float RiverBottomYCm = " + f(float(river["bottomY"]) * 100.0) + ";")
    lines.append("static constexpr float RiverWidthCm = " + f(float(river["width"]) * 100.0) + ";")
    lines.append("static constexpr float ForestCentreXCm = " + f(float(forest["centreX"]) * 100.0) + ";")
    lines.append("static constexpr float ForestCentreYCm = " + f(float(forest["centreY"]) * 100.0) + ";")
    lines.append("static constexpr float ForestSizeCm = " + f(float(forest["size"]) * 100.0) + ";")
    lines.append("static constexpr int32 ForestTreeCount = " + str(int(forest["treeCount"])) + ";")
    lines.append("static constexpr int32 ForestSeed = " + str(int(forest["seed"])) + ";")
    lines.append("")
    lines.append("struct FValleyRoutePoint { float XCm; float YCm; const TCHAR* Label; };")
    lines.append("static const FValleyRoutePoint RoutePoints[] = {")
    for wp in route["waypoints"]:
        lines.append("    { " + f(float(wp["x"]) * 100.0) + ", " + f(float(wp["y"]) * 100.0)
                     + ", " + cpp_text(wp["label"]) + " },")
    lines.append("};")
    lines.append("static constexpr int32 RoutePointCount = " + str(len(route["waypoints"])) + ";")
    lines.append("")
    lines.append("struct FValleySettlement { const TCHAR* Id; const TCHAR* Name; float XCm; float YCm; EMarketDay MarketDay; };")
    lines.append("static const FValleySettlement Settlements[] = {")
    for s in world["settlements"]:
        enum = MARKET_DAY_ENUM[s["marketDay"]]
        lines.append("    { " + cpp_text(s["id"]) + ", " + cpp_text(s["name"])
                     + ", " + f(float(s["x"]) * 100.0) + ", " + f(float(s["y"]) * 100.0)
                     + ", " + enum + " },")
    lines.append("};")
    lines.append("static constexpr int32 SettlementCount = " + str(len(world["settlements"])) + ";")
    lines.append("")
    lines.append("static const TCHAR* ObjectiveText = "
                 + cpp_text("Explore the Ọmà-valley core: Ahanwụ and Ọmà Ukwu, the market and the seasons.") + ";")
    lines.append("} // namespace TDDOmegaValleyData")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote " + str(OUT) + " (" + str(len(lines)) + " lines)")


if __name__ == "__main__":
    main()
