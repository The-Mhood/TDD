#!/usr/bin/env python3
"""Validate every clip keyframe through the project's own skinning test."""
import json, sys, os
sys.path.insert(0, os.path.abspath("../../../2026-11-23_w1d7_production/pipeline"))
import test_deformation as td
clips = json.load(open("GUARD_ANIMATION_CLIPS_V1.json"))["clips"]
poses = {}
for cname, clip in clips.items():
    for i, k in enumerate(clip["keys"]):
        poses[f"{cname}_{i}"] = {j: (v[0], v[1]) for j, v in k["pose"].items()}
td.POSES = poses
ok = True
for glb in ("../../../2026-11-25_w1d9_sculpt2/out/GUARD_CLASS_V3.glb", "../../../2026-11-26_w1d10_definitive_adanna/out/ADANNA_AD03_V5.glb"):
    rc = td.run(os.path.abspath(glb)); print(os.path.basename(glb), "rc", rc)
    ok &= rc == 0
json.dump({"clips": list(clips), "keyframe_poses_tested": len(poses), "verdict": "PASS" if ok else "FAIL"}, open("GUARD_ANIMATION_CLIPS_V1_VALIDATION.json","w"), indent=2)
sys.exit(0 if ok else 1)
