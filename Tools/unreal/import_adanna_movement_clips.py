#!/usr/bin/env python3
"""Import the W1 D13 Adanna movement clips V1 into Unreal content and validate
the clip data for the animation workflow. Run from Unreal Editor's Python
console or -ExecutePythonScript.

The clips are production animation DATA (JSON keyframes on the shared
HUMAN_BASE_PROPOSED 11-joint skeleton, joint -> [axis, angle_rad]). This
script writes the clip JSON into Content as a raw asset and emits the joint
list so the production skeleton import can be checked for bone-name mapping.
It does NOT create AnimSequences: the in-engine playback path (data-driven
clip player) and skeleton mapping are the animation integration steps that
follow, verified in-engine.
"""
import hashlib
import json
import os
from pathlib import Path

import unreal

REPO = Path(unreal.Paths.project_dir())
SOURCE_JSON = REPO / ".arena/production/2026-11-29_w1d13_production/adanna_animation/ADANNA_MOVEMENT_CLIPS_V1.json"
SOURCE_VALIDATION = REPO / ".arena/production/2026-11-29_w1d13_production/adanna_animation/ADANNA_MOVEMENT_CLIPS_V1_VALIDATION.json"
DEST_DIR = "/Game/Animation"
DEST_NAME = "ADANNA_MOVEMENT_CLIPS_V1.json"
EXPECTED_CLIPS = ["idle", "walk", "run", "dodge_left", "crouch_recover", "look_back"]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    require(SOURCE_JSON.is_file(), "Clip JSON not found at " + str(SOURCE_JSON))
    raw = SOURCE_JSON.read_bytes()
    actual_hash = hashlib.sha256(raw).hexdigest()
    clips = json.loads(raw)

    require(clips.get("skeleton") == "HUMAN_BASE_PROPOSED",
            "Clip skeleton is not HUMAN_BASE_PROPOSED: " + str(clips.get("skeleton")))
    clip_data = clips.get("clips", {})
    require(sorted(clip_data.keys()) == sorted(EXPECTED_CLIPS),
            "Clip set mismatch: " + str(sorted(clip_data.keys())))
    total_keys = 0
    joints = set()
    for name, clip in clip_data.items():
        require(clip.get("loop") is not None or name in ("dodge_left", "crouch_recover", "look_back"),
                "Loop flag missing for clip " + name)
        require(len(clip.get("keys", [])) >= 1, "Clip " + name + " has no keyframes")
        total_keys += len(clip["keys"])
        for key in clip["keys"]:
            for joint in key.get("pose", {}):
                joints.add(joint)

    validation = json.loads(SOURCE_VALIDATION.read_text(encoding="utf-8"))
    require(validation.get("verdict") == "PASS", "Source validation verdict is not PASS")

    # Write the clip JSON into Content as a raw asset.
    unreal.EditorAssetLibrary.make_directory(DEST_DIR)
    dest_path = unreal.EditorAssetLibrary.generate_package_path(DEST_DIR, DEST_NAME)
    require(not unreal.EditorAssetLibrary.does_asset_exist(dest_path),
            "Refusing to replace existing content: " + dest_path)
    with open(dest_path, "wb") as handle:
        handle.write(raw)

    report = {
        "status": "CLIPS_IMPORTED",
        "source_sha256": actual_hash,
        "content_path": dest_path,
        "skeleton": clips.get("skeleton"),
        "clips": sorted(clip_data.keys()),
        "keyframes_total": total_keys,
        "joints": sorted(joints),
        "joint_count": len(joints),
        "source_validation": validation.get("verdict"),
        "note": "Raw data import only; AnimSequence authoring, skeleton bone mapping, "
                "transition/root-motion testing are the in-engine animation integration steps",
    }
    out = REPO / "Saved/BuildEvidence/W2/movement-clips-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W2 movement clips import: " + json.dumps(report))


main()
