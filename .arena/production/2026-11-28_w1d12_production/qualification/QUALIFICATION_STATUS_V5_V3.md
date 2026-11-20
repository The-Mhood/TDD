# QUALIFICATION STATUS — Adanna AD-03 V5 / Guard Class V3 (2026-11-28)

## What is DONE (evidence in-repo)
- Source-level checks (rerun for animation validation this cycle): joint-influence PASS both; deformation PASS both; budget PASS both (V5 12,736 tris/1.840 m; Guard V3 10,020 tris/1.772 m).
- Animation data validation: all 18 keyframe poses of the 5 Guard clips skinned through the project's own deformation code on BOTH skeletons - 36/36 PASS (`assets/guard_animation/GUARD_ANIMATION_CLIPS_V1_VALIDATION.json`).
- Mac package verified fail-safe in sandbox (`run_all.sh` exit 3 = Blender not found here) with checksums OK for both GLBs.

## What STILL requires owner-Mac validation (not claimed, not substitutable in this sandbox)
1. Native `.blend` projects for V5 and Guard V3 - produced only by `blender/finish_character.py` on the Mac.
2. FBX exports (Unreal) - same run.
3. Blender-rendered preview PNGs (8) and the Blender finisher pose test (per-joint deltas) - the official qualification gate Design inspects to close V5/V3.
Exact run:
```sh
git pull && cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
```
No identity change is needed or permitted to complete this; any Blender-side failure returns to Design as a script fix (precedent: dead-bone fix, sculpt M1).
