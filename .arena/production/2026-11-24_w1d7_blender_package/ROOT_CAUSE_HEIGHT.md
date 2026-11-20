# ROOT CAUSE — `FINISHER FAIL: height 0.52 m outside 1.6-2.0` (Mac run, Blender 4.2.23 LTS)
## Finding: incorrect measurement method in the finisher. Source geometry, import units and transforms are all correct.
### Diagnostic (measured from the shipped GLBs' accessor min/max + finisher logic)
| Quantity | Adanna AD-03 V2 | Guard V1 |
|---|---|---|
| Tallest **single part** object (what v1.0/v1.1 measured) | `shin_foot.L` = **0.521 m** | `shin_sandal.L` = **0.521 m** |
| **Combined world-space height (correct)** | **1.837 m** (z 0.004→1.841, incl. hair knot; body target 1.80 m) | **1.771 m** (z 0.002→1.773) |
| 1.6–2.0 m gate on corrected measure | PASS | PASS |
The reported "0.52 m" matches the shin segment to the millimetre in both files — the finisher computed `max(o.dimensions.z)` over 29 (Adanna) / 17 (Guard) separate part objects. No single part spans the body, so the maximum is a limb segment, not the character.
### Ruled out
- **Import-unit issue:** a m/cm error would read 183.7 m or 0.018 m, not 0.52 m. GLB positions are metres (accessor ranges above); Blender scene unit scale is recorded in the new QC (`scene_units`).
- **Unapplied transform:** GLB nodes carry no scale/rotation on mesh nodes; the importer converts Y-up→Z-up. The finisher now records `armature_transform` (location/scale) in QC for the rerun record.
- **Incorrectly scaled source:** combined bbox = 1.837 m vs the 1.80 m production target (hair knot accounts for the excess); Guard 1.771 m on the same skeleton. Both in gate.
- **Guard:** same method bug, same correction — the shared finisher measures both identically.
## Correction (finisher v1.2)
Height = **combined world-space bounding box** (bound-box corners × `matrix_world`) across all **skinned** part meshes — the same world-space method the pose test already used. The **1.6–2.0 m requirement is unchanged** and now applied to the correct quantity. QC additionally records `world_bbox_m`, `height_m_combined_world`, the legacy single-part figure as `diagnostic_legacy_max_single_part_z_m`, armature transform and scene units, so the rerun output itself proves the diagnosis. Strict weight validation (0 unweighted), pose-deformation tests, helper classification (v1.1) and FBX export are untouched.
**Exact transformation applied to the assets: none.** No geometry was scaled; only the ruler changed.
## Owner rerun (repo root, after `git pull` on `arena/6e649a9b-tdd`)
```bash
cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
```
Expected QC per character: `height_m_combined_world` ≈ 1.84 (Adanna) / 1.77 (Guard), `helper_objects` lists the Icosphere, `verdict: "PASS"`, `.blend` + `.fbx` + 4 previews in `output/<NAME>/`. Commit `output/` back to the branch.
*Sandbox note: Blender cannot execute in the Design environment (no binary); the corrected measurement was verified against the GLBs' declared accessor bounds above, and the Mac rerun is the qualification execution.*
