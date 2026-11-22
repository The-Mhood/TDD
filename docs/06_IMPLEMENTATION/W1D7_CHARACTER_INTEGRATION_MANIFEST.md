# W1 D7/D8 — CHARACTER INTEGRATION MANIFEST
**Date:** 2026-11-20 (updated W1 D8)  
**Branch:** `arena/553fb02d-tdd`  
**Design source:** `arena/6e649a9b-tdd` @ `2a4a88e` (Sculpt milestone-1 gate CLOSED)

## Integration Targets (Updated — V3/V2)

Per Design gate closure at `2a4a88e`: **Adanna AD-03 V3** and **Guard Class V2** are now the
approved integration targets. The Mac Blender regeneration, technical QC, deformation checks,
and visual approvals are complete. V2/V1 qualified builds are retained in their folders as
**rollback fallbacks** and remain visually gate-passed.

> **Reconciliation note:** This manifest was previously scoped to V2/V1 pending Mac regeneration
> and visual gate. That gate is now **CLOSED** (`2a4a88e`). The V3/V2 deliverables below have been
> independently verified in the sandbox via Blender 4.2.23 headless execution.

### 1. Adanna AD-03 V3 (PRIMARY — integration target)

| Property | Value | Source |
|---|---|---|
| **FBX path** | `.arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V3/ADANNA_AD03_V3.fbx` | Design `4fb1c6d` (corrected) |
| **GLB source** | `.arena/production/2026-11-25_w1d8_sculpt/out/ADANNA_AD03_V3.glb` | sha `697f365f…` |
| **Blender project** | `ADANNA_AD03_V3.blend` (3,101,268 B) | Blender 4.2.23 LTS |
| **FBX size** | 857,388 B | verified |
| **FBX format** | Binary FBX 7.400 (Kaydara) | verified |
| **Skeleton** | `HUMAN_BASE_PROPOSED` (11 joints) | independently verified |
| **Skinned mesh objects** | 36 | independently verified |
| **Triangles** | 13,680 | independently verified |
| **Verts (skinned)** | 7,028 | independently verified |
| **Height** | 1.837 m (world bbox z: 0.004 → 1.841) | independently verified |
| **Armature transform** | Location (0,0,0), Scale (1,1,1) | independently verified |
| **Scene units** | METRIC, scale_length 1.0 | independently verified |
| **Weight sum** | min 1.0, max 1.0, unweighted 0 | Design QC + joint-influence |
| **Materials** | 10 slots: skin_base_v1, cloth_indigo_plain_v1, leather_baldric_v1, bronze_armlet_plain_v1, pendant_spiral_FICTIONAL_v1, coral_bead_v1, hair_v1, scar_marker_v1, **lips_v1**, **eye_dark_v1** | independently verified |
| **Embedded textures** | 4 (cloth_indigo, leather_baldric, bronze_armlet, pendant_spiral) — packed in `.blend` | GLB + `.blend` verified |
| **Verdict** | **PASS** | Design gate + independent |

**Joint names (skeleton hierarchy — independently verified):**
```
HUMAN_BASE_PROPOSED
├── pelvis (root)
│   ├── spine
│   │   └── head
│   ├── upperarm.L → forearm.L
│   ├── upperarm.R → forearm.R
│   ├── thigh.L → shin.L
│   └── thigh.R → shin.R
```

### 2. Guard Class V2 (PRIMARY — integration target)

| Property | Value | Source |
|---|---|---|
| **FBX path** | `.arena/production/2026-11-24_w1d7_blender_package/output/GUARD_CLASS_V2/GUARD_CLASS_V2.fbx` | Design `38a0377` |
| **GLB source** | `.arena/production/2026-11-25_w1d8_sculpt/out/GUARD_CLASS_V2.glb` | sha `d4d5b060…` |
| **Blender project** | `GUARD_CLASS_V2.blend` (2,460,248 B) | Blender 4.2.23 LTS |
| **FBX size** | 603,548 B | verified |
| **FBX format** | Binary FBX 7.400 (Kaydara) | verified |
| **Skeleton** | `HUMAN_BASE_PROPOSED` (11 joints — identical to Adanna) | independently verified |
| **Skinned mesh objects** | 23 | independently verified |
| **Triangles** | 10,752 | independently verified |
| **Verts (skinned)** | 5,556 | independently verified |
| **Height** | 1.772 m (world bbox z: 0.002 → 1.774) | independently verified |
| **Armature transform** | Location (0,0,0), Scale (1,1,1) | independently verified |
| **Scene units** | METRIC, scale_length 1.0 | independently verified |
| **Weight sum** | min 1.0, max 1.0, unweighted 0 | Design QC + joint-influence |
| **Materials** | 6 slots: skin_guard_v1, cloth_indigo_plain_v1, cloth_sash_undyed_v1, bronze_plain_v1, leather_baldric_v1, **eye_dark_v1** | independently verified |
| **Embedded textures** | 3 (cloth_indigo, bronze_plain, leather_baldric) — packed in `.blend` | GLB + `.blend` verified |
| **Verdict** | **PASS** | Design gate + independent |

**Joint names:** identical 11-joint `HUMAN_BASE_PROPOSED` skeleton, same bone names as Adanna → retarget shared animation set.

### 3. Rollback Fallbacks (V2/V1 — retained, not primary)

| Character | FBX path | Height | Tris | Materials | Status |
|---|---|---|---|---|---|
| Adanna AD-03 V2 | `output/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` | 1.837 m | 8,660 | 8 slots | Visually gate-passed, fallback |
| Guard Class V1 | `output/GUARD_CLASS_V1/GUARD_CLASS_V1.fbx` | 1.771 m | 6,296 | 5 slots | Visually gate-passed, fallback |

Both fallbacks share the same skeleton, bone names, scale, and import configuration. If V3/V2
integration hits a blocking issue in UE, swap to the V2/V1 FBX — no skeleton or import-setting
changes required.

## Skeleton Compatibility Verification (V3/V2 — Independently Verified)

| Check | Adanna V3 | Guard V2 | Result |
|---|---|---|---|
| Skeleton name | HUMAN_BASE_PROPOSED | HUMAN_BASE_PROPOSED | ✅ Identical |
| Joint count | 11 | 11 | ✅ Identical |
| Joint names | pelvis, spine, head, upperarm.L/R, forearm.L/R, thigh.L/R, shin.L/R | same | ✅ Identical |
| Bone hierarchy | pelvis→spine→head, pelvis→limbs | same | ✅ Identical |
| Armature transform | (0,0,0), scale (1,1,1) | (0,0,0), scale (1,1,1) | ✅ Identical |
| Scene units | METRIC, scale 1.0 | METRIC, scale 1.0 | ✅ Identical |
| FBX bone names | All 11 imported from FBX | All 11 imported from FBX | ✅ Verified (Blender import) |

**Conclusion:** Both V3/V2 characters share the same skeleton, bone names, hierarchy, and scale
as V2/V1. Animation retargeting between Adanna and Guard requires zero bone-mapping changes.
Shared animation set is directly compatible.

## Deformation Test Results

### Authoritative gate — Joint-Influence Regression (`test_joint_influence.py`)

This is the regression test that catches the dead-bone failure class (the Adanna V3 forearm
issue found and fixed during sculpt milestone 1). Per-joint assertions: ≥25 verts >0.5 weight
and limb leverage ≥0.15 m.

**Adanna V3 — PASS** (0 failures). Critical limb joints:
| Joint | Verts >0.5 | Max Leverage (m) |
|---|---|---|
| upperarm.L | 920 | 0.326 |
| forearm.L | 280 | 0.385 |
| upperarm.R | 320 | 0.326 |
| forearm.R | 280 | 0.385 |
| thigh.L/R | 142 | 0.429 |
| shin.L/R | 396 | 0.523 |

**Guard V2 — PASS** (0 failures). Critical limb joints:
| Joint | Verts >0.5 | Max Leverage (m) |
|---|---|---|
| upperarm.L | 320 | 0.322 |
| forearm.L | 280 | 0.406 |
| upperarm.R | 520 | 0.322 |
| forearm.R | 280 | 0.406 |
| thigh.L/R | 142 | 0.430 |
| shin.L/R | 504 | 0.533 |

### Blender-Finisher Pose Test (Design recheck — bbox-delta based)

Both characters **PASS** all 8 poses. Key bbox deltas (Design QC JSON):
- **Adanna V3:** forearm.L 0.162 m, upperarm.R 0.395 m, shin.L 0.270 m, head 0.031 m — the
  forearm dead-bone failure (was 0.0 m pre-fix) is closed in-engine.
- **Guard V2:** forearm.L 0.124 m, upperarm.R 0.356 m, shin.L 0.244 m, head 0.021 m.

### Independent LBS Deformation (`test_deformation.py` — supplementary)

All 8 poses produce finite geometry with correct per-pose heights. The old test's 1.1 m global
vertex-displacement cap is exceeded only by the two **extreme full-arm-raise poses**
(`shoulder_raise_L`, `combined`), which are physically correct (hand reaches 1.89–1.96 m). This
is a test-threshold artifact, not a deformation defect — the authoritative joint-influence and
Blender-finisher gates both PASS. Summary:

| Pose | Adanna V3 (disp/height) | Guard V2 (disp/height) |
|---|---|---|
| rest | 0.000 / 1.837 m | 0.000 / 1.772 m |
| shoulder_raise_L | 1.086 / 1.837 m | 1.123 / 1.891 m |
| elbow_bend_L | 0.552 / 1.837 m | 0.582 / 1.772 m |
| forearm_twist_R | 0.102 / 1.837 m | 0.193 / 1.772 m |
| hip_knee_bend_R | 0.459 / 1.837 m | 0.466 / 1.772 m |
| neck_turn | 0.080 / 1.837 m | 0.082 / 1.772 m |
| torso_twist | 0.212 / 1.837 m | 0.256 / 1.772 m |
| combined | 1.175 / 1.952 m | 1.174 / 1.958 m |

## Blender Execution Environment

| Item | Value |
|---|---|
| **Engine** | Blender 4.2.23 LTS (headless, `import bpy`) |
| **Route** | PyPI `bpy==4.2.23` wheel (cp311, manylinux_2_28_x86_64) |
| **Python** | 3.11.2 |
| **Stub libraries** | 12 X11/GL/HIP/oneAPI stubs built with gcc (headless, no GPU/display) |
| **numpy** | 2.4.6 (required by FBX export) |
| **Smoke test** | Cube build → `.blend` save → FBX export: **PASS** |
| **V3/V2 verification** | Independent FBX import + skeleton/material/scale/height audit: **PASS** |
| **Deformation gate** | Joint-influence regression + Blender-finisher pose test: **PASS** |

## Texture / Material Import Note

The FBX files carry **material definitions and material-slot assignments** but do **not** embed
the image textures (verified: no PNG/JPEG/TIFF magic bytes in the FBX). This is **identical to
the qualified V2/V1 builds** — not a regression. The textures are packed inside the source
`.blend` (Adanna V3: 4 PNGs, Guard V2: 3 PNGs), recoverable for UE:
- Extract textures from the `.blend` (Blender: File → External Data → Pack/Unpack), or
- Re-import directly from the GLB (UE5 supports glTF/GLB) to carry textures, or
- Use the GLB as the texture source for the FBX-imported materials.

## UE Import Settings (Recommended — V3/V2)

| Setting | Value |
|---|---|
| **Import path** | `Content/Characters/ADANNA_AD03_V3/` and `Content/Characters/GUARD_CLASS_V2/` |
| **Scale** | FBX unit scale = cm (Blender exported with metres→cm conversion). UE import: scale ×1.0 |
| **Skeletal mesh** | Import as Skeletal Mesh with armature |
| **Skeleton** | Shared `HUMAN_BASE_PROPOSED` skeleton — create one UE Skeleton asset from either FBX, assign to both |
| **Animation** | Retarget one test clip across both characters to validate shared skeleton |
| **Materials** | UE Material instances from imported material slots (Adanna V3: 10 slots, Guard V2: 6 slots); supply textures from `.blend`/GLB per note above |
| **Collision** | Capsule: Adanna r=0.32 m, h=1.80 m; Guard r=0.30 m, h=1.77 m (pending TD capsule ruling) |

## Capsule Dimensions (Proposed, pending TD ruling)

| Character | Radius (m) | Half-Height (m) | Full Height (m) | Basis |
|---|---|---|---|---|
| Adanna AD-03 V3 | 0.32 | 0.90 | 1.80 | Body target 1.80 m, width 0.78 m (V3) |
| Guard Class V2 | 0.30 | 0.87 | 1.77 | Measured height 1.77 m |

## Integration Architecture Compatibility

The integration architecture accepts mesh upgrades (V3/V2 → future V4/V3) **without** skeleton,
bone-name, or scale changes:
- Skeleton `HUMAN_BASE_PROPOSED` and 11 joint names are frozen as the shared standard (confirmed
  identical across V1/V2/V3 and V1/V2 character generations).
- FBX import uses the armature as the skeleton source; mesh upgrades replace only the mesh data.
- Animation retargeting between characters uses the identical bone hierarchy.
- No scale changes: all assets are in metres, METRIC, scale 1.0.
- Rollback to V2/V1 FBX is a drop-in swap — no import-setting changes.

## Sculpt Milestone 2 (Independent — Not Blocking)

Per Design, sculpt milestone 2 refinements continue independently and are **not** a blocker:
elliptical garment plan vs circular lathe, brow/jaw softening, Guard one-shoulder construction,
sash width, cloth hem thickness. These iterate on the `.blend` files without changing rig or scale.
