# PM HANDOFF — W1 D6 (2026-11-22) — EXACT LOCATIONS, VERSIONS, TIERS
Branch `arena/6e649a9b-tdd`. Tiers: C=concept · RC=reviewed candidate · PR=production-ready · UI=Unreal-integrated. **Nothing below is PR or UI.**

## Decisions (CD — staged, NOT issued by Design)
- `CD_DECISION_INBOX_2026-11-22.md` (this folder; also Drive PENDING `1F2c6hQmsv0Qumx7RpLdFLpf8VB59XGLl`, starred) — AD-02 (rec. A), FP-10 tally, RG REVISE/V003, KIT-HUT nod.
- AD-02 one-page brief: Drive `1zjRiSzw5iXd-zQ3NX1JuPkSVv-GaQYkn`; contact sheet Drive `1B6sevPtqMmFhhM8Ozb6uhF0JS7bNiDQf`. Branch copies: `.arena/production/2026-11-21_w1d5_adanna/`.
- On CD SELECT(A): reference freezes at FRONT V004 `1HP2m8e0z8Ug7_4_yeJal3zVvj18luRa6` / TQ V004 `1JWX8z0UcLpqUXouXMJzSyWvMsVxTjxPI` / BACK V003 `1ne1I9N4HyEmEpAKmD1UNVmpMvP6RHEL0` / LEFT_SIDE V003 `1GcfptqCp9Qg4z7LA0SEejlwbYqiZozbu` (sha256 in `ADANNA_REFERENCE_CHECKSUMS_2026-11-21.txt`). V005 excluded (internal-study chrome).

## Adanna AD-03 (production start staged behind CD SELECT)
- `adanna/AD03_PRODUCTION_BUILD_bpy.py` v0.1 — Blender 4.2+ script: LOD0 base profile mesh, identity-lock empties, HUMAN_BASE-proposed armature stub, 5 material slots (v1 base maps), FBX export x100, QC JSON. **Refuses production export until STATUS=CD_SELECTED** (placeholder only with `--force-placeholder`). Requires a Blender-capable runner — sandbox has none (verified: no bpy module, no binary).
- Blockout OBJ (W1 D5): `.arena/production/2026-11-21_w1d5_adanna/blockout/ADANNA_BLOCKOUT_PLACEHOLDER_m.obj` — 856 tris, budget PASS. Placeholder only.
- Textures pending TD ratification: `.arena/production/2026-11-20_w1d4_research/textures/` (8× 2048²).
- PM asks (unchanged): minimum gameplay anim set ruling; capsule dims. Blade/scabbard: **none, deferred CQ-9, non-blocking.**

## CH01 KIT-HUT (new geometry this turn)
- `kit_hut/build_kit_hut.py` → `kit_hut/out/`: WALL_3M (24 tris), WALL_DOOR_3M (60), CORNER (60), ROOF_HIP_4x3 (54), DOORFRAME (48) + `kit_hut.mtl` + `KIT_HUT_MANIFEST.json`. **All 5 budget_checker PASS** (0 degenerate, 0 NaN).
- **NEW `kit_hut/out/CH01_HUT_ASSEMBLED_V1.obj`** — full assembled house (158 verts, height 4.105 m incl. roof), budget PASS. Provisional; TD/PM dimension sign-off before Unreal import. Target: `.arena/production/2026-11-21_w1d5_ch01/CH01-SUBJ-001_FAMILY_HOUSE_TARGET_SHEET.jpg`.

## Royal Guard
- **NEW `rg/RG_V003_GUARD_CLASS_TARGET.jpg`** (owner-selected, verified vs correction order — `rg/VERIFIED_RG_V003_2026-11-22.md`). Unnamed guard-class, unarmed, no disc/coral mark. 3D route: HUMAN_BASE body + costume meshes. PM anim/AI minimums still requested (not blocking visual lane).

## PM actions requested
1. Provide/confirm Blender 4.2+ runner (workstation or `blender:4.x` container) — this unblocks AD-03 FBX, greybox build, and kit build in one move.
2. Rule minimum animation set (Adanna + guard HUMAN_BASE proposal).
3. Confirm capsule dims + first-import axis/scale check (x100) when runner exists.
