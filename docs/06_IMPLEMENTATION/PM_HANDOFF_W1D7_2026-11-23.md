# PM HANDOFF — W1 D7 (2026-11-23) — INTEGRATE NOW (all paths on branch `arena/6e649a9b-tdd`)
Base folder: `.arena/production/2026-11-23_w1d7_production/`

## Adanna AD-03 V2 (refined, supersedes V1)
- `adanna/out/ADANNA_AD03_V2.glb` (948 KB, sha in report) — Y-up, metres (Unreal import: scale ×100), skinned, embedded 512px indigo/leather/bronze base-colour textures.
- `adanna/out/ADANNA_AD03_V2.obj/.mtl` — Z-up interchange. Source: `adanna/build_adanna_v2.py` (native editable = script + `adanna/AD03_PRODUCTION_BUILD_bpy.py` Blender finisher, STATUS now CD_SELECTED).
- QC: `adanna/out/AD03_V2_QC.json` — 29 parts, 4,346 verts / 8,548 tris; budget PASS; **deformation test PASS** (`ADANNA_AD03_V2_DEFORM.json`: rest identity 0.000 m; shoulder/elbow/forearm/hip-knee/neck/torso/combined within limb-length bound).
- Skeleton: HUMAN_BASE_PROPOSED, 11 joints (`pipeline/charbuild.py` JOINTS). Materials: 8 slots; full-res maps remain `.arena/production/2026-11-20_w1d4_research/textures/` (TD ratification still open).
- Collision: use capsule (suggest r=0.32 m, h=1.80 m) until PM confirms dims. No blade/scabbard (CQ-9).

## Royal Guard V1 (new, real model)
- `guard/out/GUARD_CLASS_V1.glb/.obj/.mtl` + `GUARD_V1_QC.json` — 17 parts, 2,898 verts / 5,728 tris, **same skeleton/joint names as Adanna** → retarget shared animation set. Deformation PASS (`GUARD_CLASS_V1_DEFORM.json`). Unarmed, no emblems/markings.
- PM ask (unchanged, now the only guard blocker): confirm minimum unarmed animation set (proposal: idle, patrol, alert, hit-react, defeat).

## CH01 settlement (provisional — NOT canon, NOT production-ready)
- New modules `ch01/out/`: KIT_COMPOUND_WALL_3M (36 tris), KIT_GATE_2M (72), KIT_STALL_2x2 (78) + `CH01_COMPOUND_ASSEMBLED_V1.obj` (558 tris; house + wall ring + gate, 7.3×7.3 m) — all budget PASS; one box collision proxy per module (bounds) for PM to validate in-engine. These replace greybox HUT/wall placeholders 1:1 at matching scale (wall height 2.0 m, house ridge 4.1 m).
- Sources: `ch01/build_settlement_modules.py`, `ch01/assemble_compound.py`; KIT-HUT sources in W1 D6 folder.

## Integration order PM can run today
1. Import both GLBs → check cm scale + capsule fit. 2. Retarget one test clip across both characters (validates shared skeleton). 3. Swap compound assembly into the greybox blockout. Report any axis/scale fault back to Design — fixes are script-side and same-day.
