#!/usr/bin/env python3
"""Apply a CH01 lighting state (ST01 DAWN / ST03 DUSK / ST04 NIGHT) to the
current level, build lighting and save. Run from Unreal Editor's Python
console or -ExecutePythonScript:  build_ch01_lighting_states.py ST01_DAWN

The three keys are APPROVED PROVISIONAL lighting references (W1 D13,
50fdd16). Values below are provisional starting points for the TD lighting
pass; the reference JPEGs are the visual authority. ST02 DAY is the Kit V1
reference; ST05 MARKET and ST06/ST07 remain excluded. No market, ritual or
festival states are created. Architecture and dressing are not modified.
"""
import json
import math
import os
import sys
from pathlib import Path

import unreal

REPO = Path(unreal.Paths.project_dir())
REFERENCES = REPO / ".arena/production/2026-11-29_w1d13_production/ch01_states"

# Provisional state table: sun elevation/azimuth (deg), intensity, colour,
# ambient sky/ground, firelight intensity (night cooking fire only).
STATES = {
    "ST01_DAWN": {
        "sun_elevation_deg": 12.0, "sun_azimuth_deg": 70.0,
        "sun_intensity": 2.0, "sun_colour": (1.0, 0.82, 0.62),
        "ambient_sky": (0.45, 0.50, 0.60), "ambient_ground": (0.22, 0.18, 0.14),
        "fire_intensity": 0.0,
    },
    "ST03_DUSK": {
        "sun_elevation_deg": 6.0, "sun_azimuth_deg": 285.0,
        "sun_intensity": 1.6, "sun_colour": (1.0, 0.55, 0.28),
        "ambient_sky": (0.40, 0.32, 0.42), "ambient_ground": (0.20, 0.14, 0.12),
        "fire_intensity": 0.0,
    },
    "ST04_NIGHT": {
        "sun_elevation_deg": -24.0, "sun_azimuth_deg": 200.0,
        "sun_intensity": 0.35, "sun_colour": (0.55, 0.62, 0.80),
        "ambient_sky": (0.06, 0.08, 0.14), "ambient_ground": (0.04, 0.04, 0.05),
        "fire_intensity": 8.0,
    },
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vec(t):
    return unreal.Vector(t[0], t[1], t[2])


def col(t):
    return unreal.LinearColor(t[0], t[1], t[2])


def main():
    requested = sys.argv[1] if len(sys.argv) > 1 else "ST01_DAWN"
    require(requested in STATES, "Unknown state: " + requested + " (use ST01_DAWN/ST03_DUSK/ST04_NIGHT)")
    ref = REFERENCES / (requested + ".jpg")
    require(ref.is_file(), "Reference key missing: " + str(ref))
    s = STATES[requested]

    world = unreal.EditorLevelLibrary.get_editor_world()
    require(world is not None, "No editor world open")

    # Direction light: find an existing one or create one owned by this run.
    directional = None
    for actor in unreal.GameplayStatics.get_all_actors_with_tag(world, "TDD_LightingState"):
        comp = actor.get_component_by_class(unreal.DirectionalLightComponent)
        if comp is not None:
            directional = comp
            break
    if directional is None:
        light_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.DirectionalLightActor, unreal.Vector(0.0, 0.0, 600.0), unreal.Rotator(0.0, 0.0, 0.0))
        require(light_actor is not None, "Could not spawn directional light")
        light_actor.set_actor_label("TDD_LightingState_Sun", mark_dirty=True)
        directional = light_actor.directional_light_component

    elevation = math.radians(s["sun_elevation_deg"])
    azimuth = math.radians(s["sun_azimuth_deg"])
    directional.set_editor_property("intensity", s["sun_intensity"])
    # UE 5.8.4: LightColor is FColor; use the set_light_color setter, which
    # takes a LinearColor (matches the C++ SetLightColor(FLinearColor, bSRGB)
    # contract used by the switcher).
    directional.set_light_color(col(s["sun_colour"]))
    directional.set_editor_property("rotation", unreal.Rotator(
        elevation * 57.2957795, azimuth * 57.2957795, 0.0))

    # Ambient via sky light: sky/upper colour is LightColor, ground colour is
    # LowerHemisphereColor (UE 5.8.4 has no UpperHemisphereColor member).
    hemi = None
    for actor in unreal.GameplayStatics.get_all_actors_with_tag(world, "TDD_LightingState"):
        comp = actor.get_component_by_class(unreal.SkyLightComponent)
        if comp is not None:
            hemi = comp
            break
    if hemi is None:
        hemi_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.SkyLight, unreal.Vector(0.0, 0.0, 300.0), unreal.Rotator(0.0, 0.0, 0.0))
        require(hemi_actor is not None, "Could not spawn sky light")
        hemi_actor.set_actor_label("TDD_LightingState_Ambient", mark_dirty=True)
        hemi = hemi_actor.sky_light_component
    hemi.set_editor_property("intensity", 0.4)
    hemi.set_light_color(col(s["ambient_sky"]))
    hemi.set_lower_hemisphere_color(col(s["ambient_ground"]))

    # Firelight (night cooking fire only — matches the approved VFX direction).
    fire = None
    for actor in unreal.GameplayStatics.get_all_actors_with_tag(world, "TDD_LightingState"):
        comp = actor.get_component_by_class(unreal.PointLightComponent)
        if comp is not None:
            fire = comp
            break
    if fire is None:
        fire_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.PointLightActor, unreal.Vector(0.0, 0.0, 120.0), unreal.Rotator(0.0, 0.0, 0.0))
        require(fire_actor is not None, "Could not spawn firelight")
        fire_actor.set_actor_label("TDD_LightingState_Fire", mark_dirty=True)
        fire = fire_actor.point_light_component
    fire.set_editor_property("intensity", s["fire_intensity"])

    require(unreal.EditorLevelLibrary.save_current_level(), "Could not save level after lighting state")

    report = {
        "status": "LIGHTING_STATE_APPLIED",
        "state": requested,
        "reference": str(ref),
        "sun": {"intensity": s["sun_intensity"], "colour": list(s["sun_colour"]),
                "elevation_deg": s["sun_elevation_deg"], "azimuth_deg": s["sun_azimuth_deg"]},
        "ambient_sky": list(s["ambient_sky"]),
        "ambient_ground": list(s["ambient_ground"]),
        "firelight_intensity": s["fire_intensity"],
        "provisional": True,
    }
    out = REPO / "Saved/BuildEvidence/W2/lighting-" + requested + "-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W2 lighting state: " + json.dumps(report))


main()
