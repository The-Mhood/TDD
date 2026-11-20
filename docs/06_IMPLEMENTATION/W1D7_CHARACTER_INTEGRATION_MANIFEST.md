# W1 D7 — CHARACTER INTEGRATION MANIFEST
**Date:** 2026-11-20  
**Branch:** `arena/553fb02d-tdd`  
**Design source:** `arena/6e649a9b-tdd` @ `98317f3` (Visual gate CLOSED)

## Integrated Assets (Approved — V2/V1, NOT V3/V2)

Per user directive: continue with qualified **Adanna AD-03 V2** and **Guard Class V1**. Hold Adanna V3 / Guard V2 pending Mac Blender regeneration and visual gate at commit `07ba79f`.

### 1. Adanna AD-03 V2

| Property | Value |
|---|---|
| **FBX path** | `.arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` |
| **GLB source** | `.arena/production/2026-11-23_w1d7_production/adanna/out/ADANNA_AD03_V2.glb` |
| **Blender project** | `ADANNA_AD03_V2.blend` (2,427,240 B) |
| **FBX size** | 637,436 B |
| **FBX format** | Binary FBX 7.400 (Kaydara) |
| **Skeleton** | `HUMAN_BASE_PROPOSED` (11 joints) |
| **Skinned mesh objects** | 29 |
| **Triangles** | 8,660 |
| **Verts (skinned)** | 4,404 |
| **Height** | 1.837 m (world bbox z: 0.004 → 1.841) |
| **BBox (m)** | X: [-0.364, 0.364] Y: [-0.142, 0.153] Z: [0.004, 1.841] |
| **Armature transform** | Location (0,0,0), Scale (1,1,1) |
| **Scene units** | METRIC, scale_length 1.0 |
| **Weight sum** | min 1.0, max 1.0, unweighted 0 |
| **Materials** | 8 slots: skin_base_v1, cloth_indigo_plain_v1, leather_baldric_v1, bronze_armlet_plain_v1, pendant_spiral_FICTIONAL_v1, coral_bead_v1, hair_v1, scar_marker_v1 |
| **Embedded textures** | 4 (cloth_indigo, leather_baldric, bronze_armlet, pendant_spiral) |
| **Verdict** | **PASS** |

**Joint names (skeleton hierarchy):**
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

### 2. Guard Class V1

| Property | Value |
|---|---|
| **FBX path** | `.arena/production/2026-11-24_w1d7_blender_package/output/GUARD_CLASS_V1/GUARD_CLASS_V1.fbx` |
| **GLB source** | `.arena/production/2026-11-23_w1d7_production/guard/out/GUARD_CLASS_V1.glb` |
| **Blender project** | `GUARD_CLASS_V1.blend` (1,880,116 B) |
| **FBX size** | 411,292 B |
| **FBX format** | Binary FBX 7.400 (Kaydara) |
| **Skeleton** | `HUMAN_BASE_PROPOSED` (11 joints — identical to Adanna) |
| **Skinned mesh objects** | 17 |
| **Triangles** | 6,296 |
| **Verts (skinned)** | 3,190 |
| **Height** | 1.771 m (world bbox z: 0.002 → 1.773) |
| **BBox (m)** | X: [-0.449, 0.449] Y: [-0.15, 0.16] Z: [0.002, 1.773] |
| **Armature transform** | Location (0,0,0), Scale (1,1,1) |
| **Scene units** | METRIC, scale_length 1.0 |
| **Weight sum** | min 1.0, max 1.0, unweighted 0 |
| **Materials** | 5 slots: skin_guard_v1, cloth_indigo_plain_v1, cloth_sash_undyed_v1, bronze_plain_v1, leather_baldric_v1 |
| **Embedded textures** | 3 (cloth_indigo, bronze_plain, leather_baldric) |
| **Verdict** | **PASS** |

**Joint names:** identical 11-joint `HUMAN_BASE_PROPOSED` skeleton, same bone names as Adanna → retarget shared animation set.

## Skeleton Compatibility Verification

| Check | Adanna V2 | Guard V1 | Result |
|---|---|---|---|
| Skeleton name | HUMAN_BASE_PROPOSED | HUMAN_BASE_PROPOSED | ✅ Identical |
| Joint count | 11 | 11 | ✅ Identical |
| Joint names | pelvis, spine, head, upperarm.L/R, forearm.L/R, thigh.L/R, shin.L/R | same | ✅ Identical |
| Bone hierarchy | pelvis→spine→head, pelvis→limbs | same | ✅ Identical |
| Armature transform | (0,0,0), scale (1,1,1) | (0,0,0), scale (1,1,1) | ✅ Identical |
| Scene units | METRIC, scale 1.0 | METRIC, scale 1.0 | ✅ Identical |
| FBX bone names | All 11 found in FBX tokens | All 11 found in FBX tokens | ✅ Verified |

**Conclusion:** Both characters share the same skeleton, bone names, hierarchy, and scale. Animation retargeting between Adanna and Guard requires zero bone-mapping changes. Shared animation set is directly compatible.

## Deformation Test Results (Independent LBS Verification)

### Adanna AD-03 V2 — PASS
| Pose | Finite | Max Displacement (m) | Height (m) | Pass |
|---|---|---|---|---|
| rest | ✅ | 0.000 | 1.837 | ✅ |
| shoulder_raise_L | ✅ | 0.851 | 1.837 | ✅ |
| elbow_bend_L | ✅ | 0.344 | 1.837 | ✅ |
| forearm_twist_R | ✅ | 0.073 | 1.837 | ✅ |
| hip_knee_bend_R | ✅ | 0.503 | 1.837 | ✅ |
| neck_turn | ✅ | 0.080 | 1.837 | ✅ |
| torso_twist | ✅ | 0.198 | 1.837 | ✅ |
| combined | ✅ | 0.902 | 1.837 | ✅ |

### Guard Class V1 — PASS
| Pose | Finite | Max Displacement (m) | Height (m) | Pass |
|---|---|---|---|---|
| rest | ✅ | 0.000 | 1.771 | ✅ |
| shoulder_raise_L | ✅ | 0.900 | 1.835 | ✅ |
| elbow_bend_L | ✅ | 0.392 | 1.771 | ✅ |
| forearm_twist_R | ✅ | 0.168 | 1.771 | ✅ |
| hip_knee_bend_R | ✅ | 0.466 | 1.771 | ✅ |
| neck_turn | ✅ | 0.071 | 1.771 | ✅ |
| torso_twist | ✅ | 0.244 | 1.771 | ✅ |
| combined | ✅ | 0.893 | 1.817 | ✅ |

## Blender Execution Environment

| Item | Value |
|---|---|
| **Engine** | Blender 4.2.23 LTS (headless, `import bpy`) |
| **Route** | PyPI `bpy==4.2.23` wheel (cp311, manylinux_2_28_x86_64) |
| **Python** | 3.11.2 |
| **Stub libraries** | 12 X11/GL/HIP/oneAPI stubs built with gcc (headless, no GPU/display) |
| **numpy** | 2.4.6 (required by FBX export) |
| **Smoke test** | Cube build → `.blend` save → FBX export: **PASS** |
| **Finisher run** | Both characters: import GLB → validate → pose-test → save `.blend` → export FBX → render previews → write QC JSON: **PASS** |

## UE Import Settings (Recommended)

| Setting | Value |
|---|---|
| **Import path** | `Content/Characters/ADANNA_AD03_V2/` and `Content/Characters/GUARD_CLASS_V1/` |
| **Scale** | FBX unit scale = cm (Blender exported with metres→cm conversion). UE import: scale ×1.0 |
| **Skeletal mesh** | Import as Skeletal Mesh with armature |
| **Skeleton** | Shared `HUMAN_BASE_PROPOSED` skeleton — create one UE Skeleton asset from either FBX, assign to both |
| **Animation** | Retarget one test clip across both characters to validate shared skeleton |
| **Materials** | UE Material instances from imported material slots; 4 embedded textures for Adanna, 3 for Guard |
| **Collision** | Capsule: Adanna r=0.32 m, h=1.80 m; Guard r=0.30 m, h=1.77 m (pending TD capsule ruling) |

## Capsule Dimensions (Proposed, pending TD ruling)

| Character | Radius (m) | Half-Height (m) | Full Height (m) | Basis |
|---|---|---|---|---|
| Adanna AD-03 V2 | 0.32 | 0.90 | 1.80 | Body target 1.80 m, width 0.73 m |
| Guard Class V1 | 0.30 | 0.87 | 1.77 | Measured height 1.77 m |

## Integration Architecture Compatibility

The integration architecture is designed to accept subsequent mesh upgrades (Adanna V3, Guard V2) **without** skeleton, bone-name, or scale changes:
- Skeleton `HUMAN_BASE_PROPOSED` and 11 joint names are frozen as the shared standard.
- FBX import uses the armature as the skeleton source; mesh upgrades replace only the mesh data.
- Animation retargeting between characters uses the identical bone hierarchy.
- No scale changes: all assets are in metres, METRIC, scale 1.0.
