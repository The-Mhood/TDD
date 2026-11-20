#!/usr/bin/env python3
"""Offline preflight for the Chapter 1 UE greybox source and its authoring script."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORLD = ROOT / "TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/world.json"
BUILDER = ROOT / "Tools/unreal/build_chapter1_greybox.py"


def main():
    data = json.loads(WORLD.read_text(encoding="utf-8"))
    bounds, route = data["bounds"], data["route"]
    points = route["waypoints"]
    assert len(points) == 7, f"expected 7 authored route points, got {len(points)}"
    assert route["pathWidth"] > 0
    labels = [p["label"] for p in points]
    assert len(labels) == len(set(labels)), "duplicate route labels"
    assert len(data["obstacles"]) == 46, "unexpected M1 obstacle inventory"
    assert len({x["id"] for x in data["obstacles"]}) == len(data["obstacles"]), "duplicate obstacle IDs"
    assert len(data["interactables"]) == 2
    for point in points:
        assert bounds["minX"] <= point["x"] <= bounds["maxX"]
        assert bounds["minY"] <= point["y"] <= bounds["maxY"]
    length = sum(math.hypot(b["x"] - a["x"], b["y"] - a["y"])
                 for a, b in zip(points, points[1:]))
    source = BUILDER.read_text(encoding="utf-8")
    for token in ("MAP_PACKAGE", "PlayerStart", "TDDTrainingEnemy", "save_current_level",
                  "EditorStartupMap", "GameDefaultMap"):
        assert token in source, f"greybox editor script missing integration hook {token}"
    report = {
        "source_preflight": "PASS",
        "waypoint_count": len(points),
        "route_length_m": round(length, 3),
        "path_width_m": route["pathWidth"],
        "obstacle_count": len(data["obstacles"]),
        "interactable_count": len(data["interactables"]),
        "unreal_map_created": False,
        "note": "Offline source-data validation only; editor map generation and PIE remain unexecuted.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
