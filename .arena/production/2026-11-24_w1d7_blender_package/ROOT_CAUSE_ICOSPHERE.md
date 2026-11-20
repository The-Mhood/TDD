# ROOT CAUSE — `FINISHER FAIL: Icosphere: no vertex groups` (Mac run, Blender 4.2.23 LTS, 2026-11-24)
## Finding: category 1 — importer helper/test mesh. NOT a character mesh, NOT a rigid accessory, NOT missing skinning.
Evidence:
1. The `Icosphere` object does **not exist in either input GLB** (parsed directly: Adanna = 29 named part meshes, Guard = 17; no Icosphere node/mesh). It is created at import time, inside Blender.
2. Blender 4.2 source (`io_scene_gltf2/blender/imp/gltf2_blender_node.py`, `BlenderNode.armature_display()`, lines 145–153): after building the armature the importer calls `bpy.ops.mesh.primitive_ico_sphere_add(...)`, links the result into the special collection **`glTF_not_exported`** (hide_viewport + hide_render; "Content of this collection will not be exported"), and stores it as `gltf.bone_shape`, later assigned as each pose bone's `custom_shape`. Its sole purpose is the viewport bone-shape gizmo.
3. It therefore correctly has no vertex groups and must never be skinned, weighted, deformed, exported, or counted in character geometry.
## Why the finisher failed
v1.0 collected *every* `MESH` object post-import and demanded vertex groups from all of them — an over-broad assumption: an imported scene contains importer-owned helpers as well as character meshes.
## Fix (finisher v1.1, no validation weakening)
- Objects are **classified before validation**: `HELPER` = in `glTF_not_exported` collection **or** referenced as a pose-bone `custom_shape` → recorded in QC `checks.helper_objects`, excluded from geometry/weight/deformation checks and from FBX selection. `SKINNED` = has an Armature modifier → **the original strict validation applies unchanged** (vertex groups required; every vertex weight-sum ≥ 0.001; 0 unweighted or hard fail). Anything else unskinned → **hard FAIL by name** (a future rigid accessory must get a deliberate bone-parent attachment decision, never silent/arbitrary weights).
- Deformation pose test and evaluated-bbox are computed over skinned meshes only (unchanged criteria).
- The helper stays in the saved `.blend` (provenance; it's the importer's own bone-shape object) but is never selected for FBX export and lives in a render-hidden collection, so previews are unaffected.
## Independent verification (Design sandbox, pre-rerun)
- GLB-level weight audit (`evidence/GLB_WEIGHT_AUDIT.json`): Adanna 4,346 verts / Guard 2,898 verts across all part meshes — **0 unweighted vertices**; every deforming mesh carries valid weights.
- Pure-Python LBS deformation suite on both GLBs: **PASS** (rest identity 0.000 m; shoulder/elbow/forearm/hip-knee/neck/torso/combined) — preserved, re-run by `run_all.sh` step 4 on the Mac as well.
- `finish_character.py` v1.1 byte-compiles clean. **Blender-internal execution cannot be repeated in the Design sandbox (no Blender binary — Linux GL dead end, unchanged); the Mac rerun below is the qualification run.**
## Exact owner rerun command (from repo root, after `git pull` on `arena/6e649a9b-tdd`)
```bash
cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
```
Expected: both characters PASS; `output/{ADANNA_AD03_V2,GUARD_CLASS_V1}/` each contain `.blend`, `.fbx`, `*_BLENDER_QC.json` (with `helper_objects: [{name: "Icosphere", …}]` and `verdict: "PASS"`), and 4 preview PNGs. Commit `output/` back to the branch.
