#!/usr/bin/env python3
"""Generate a C++ source header from the shared playable-world JSON.

This keeps the provisional Unreal source state aligned with the browser/Node
simulation without adding an Unreal JSON runtime dependency.
"""
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
WORLD = BASE / "world.json"
OUT = BASE / "ue_project" / "Source" / "TDD_GAME" / "TDDWorldData.h"


def f(value: object) -> str:
    return f"{float(value):.6f}f"


def cpp_text(value: object) -> str:
    return "TEXT(" + json.dumps(str(value), ensure_ascii=False) + ")"


def main() -> None:
    world = json.loads(WORLD.read_text(encoding="utf-8"))
    route = world["route"]["waypoints"]
    obstacles = world["obstacles"]
    interactables = world["interactables"]
    character = world["character"]
    camera = world["camera"]
    spawn = world["spawn"]["position"]
    bounds = world["bounds"]

    lines: list[str] = [
        "// GENERATED FILE — do not hand-edit. Source: PLAYABLE_ADANNA_M1/world.json",
        "// Regenerate with: python3 scripts/generate_ue_world_data.py",
        f"// worldVersion: {world['worldVersion']}",
        "// Classification: neutral gameplay/collision proxy; not approved story dimensions or final level art.",
        "#pragma once",
        "",
        '#include "CoreMinimal.h"',
        "",
        "namespace TDDWorldData",
        "{",
        "struct FWaypoint { float XCm; float YCm; const TCHAR* Label; };",
        "struct FObstacle",
        "{",
        "    const TCHAR* Id; const TCHAR* Type;",
        "    float XCm; float YCm; float RadiusCm; float HeightCm;",
        "    float TrunkRadiusCm; float CanopyRadiusCm; int32 Seed;",
        "};",
        "struct FInteraction { const TCHAR* Id; float XCm; float YCm; float RadiusCm; bool bFinal; const TCHAR* Message; };",
        "",
        "static constexpr float MetresToCm = 100.0f;",
        f"static constexpr float BoundsMinXCm = {f(float(bounds['minX']) * 100.0)};",
        f"static constexpr float BoundsMaxXCm = {f(float(bounds['maxX']) * 100.0)};",
        f"static constexpr float BoundsMinYCm = {f(float(bounds['minY']) * 100.0)};",
        f"static constexpr float BoundsMaxYCm = {f(float(bounds['maxY']) * 100.0)};",
        f"static constexpr float SpawnXCm = {f(float(spawn['x']) * 100.0)};",
        f"static constexpr float SpawnYCm = {f(float(spawn['y']) * 100.0)};",
        "static constexpr float SpawnZCm = 92.0f; // capsule half-height above flat collision ground",
        f"static constexpr float RouteWidthCm = {f(float(world['route']['pathWidth']) * 100.0)};",
        f"static constexpr float CharacterRadiusCm = {f(float(character['radius']) * 100.0)};",
        "static constexpr float CharacterHalfHeightCm = 88.0f; // neutral collision capsule half-height; NOT an approved character dimension",
        f"static constexpr float WalkSpeedCmS = {f(float(character['walkSpeed']) * 100.0)};",
        f"static constexpr float RunSpeedCmS = {f(float(character['runSpeed']) * 100.0)};",
        f"static constexpr float JumpVelocityCmS = {f(float(character['jumpVelocity']) * 100.0)};",
        f"static constexpr float CameraDistanceCm = {f(float(camera['distance']) * 100.0)};",
        f"static constexpr float CameraCollisionPaddingCm = {f(float(camera['collisionPadding']) * 100.0)};",
        "",
        "static const FWaypoint Waypoints[] = {",
    ]
    for wp in route:
        lines.append(
            f"    {{ {f(float(wp['x']) * 100.0)}, {f(float(wp['y']) * 100.0)}, {cpp_text(wp['label'])} }},"
        )
    lines.extend([
        "};",
        f"static constexpr int32 WaypointCount = {len(route)};",
        "",
        "static const FObstacle Obstacles[] = {",
    ])
    for o in obstacles:
        lines.append(
            "    { " + ", ".join([
                cpp_text(o["id"]),
                cpp_text(o["type"]),
                f(float(o["x"]) * 100.0),
                f(float(o["y"]) * 100.0),
                f(float(o["radius"]) * 100.0),
                f(float(o["height"]) * 100.0),
                f(float(o.get("trunkRadius", 0.0)) * 100.0),
                f(float(o.get("canopyRadius", 0.0)) * 100.0),
                str(int(o.get("seed", 0))),
            ]) + " },"
        )
    lines.extend([
        "};",
        f"static constexpr int32 ObstacleCount = {len(obstacles)};",
        "",
        "static const FInteraction Interactions[] = {",
    ])
    for it in interactables:
        lines.append(
            "    { " + ", ".join([
                cpp_text(it["id"]),
                f(float(it["x"]) * 100.0),
                f(float(it["y"]) * 100.0),
                f(float(it["radius"]) * 100.0),
                "true" if it.get("final") else "false",
                cpp_text(it["message"]),
            ]) + " },"
        )
    lines.extend([
        "};",
        f"static constexpr int32 InteractionCount = {len(interactables)};",
        "",
        'static const TCHAR* ObjectiveText = TEXT("Follow the white cloth to the Great Root Mother");',
        "} // namespace TDDWorldData",
        "",
    ])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(BASE)}: {len(route)} waypoints, {len(obstacles)} obstacles, {len(interactables)} interactions")


if __name__ == "__main__":
    main()
