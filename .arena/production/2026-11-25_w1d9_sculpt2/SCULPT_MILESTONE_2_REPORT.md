# SCULPT MILESTONE 2 REPORT — Adanna AD-03 V4 / Guard Class V3 (2026-11-25)

Status: **BUILT + source-level QA PASS. Blender qualification NOT yet claimed** — Mac rerun required (instructions §6). Milestone-1 deliverables (Adanna V3 `697f365f…`, Guard V2 `d4d5b060…`) remain the PM integration assets and the rollback fallback; do not replace them until the M2 Mac run passes and Design inspects the Blender previews.

## 1. What changed (owner M2 items 1–5)

Shared pipeline: `2026-11-23_w1d7_production/pipeline/charbuild.py` — `lathe()` now accepts elliptical plan profiles `(rx, ry, z)` per row and a `slant` parameter (top-edge height varies as `slant·cos θ` around the ring); cap-centre indexing fixed for 3-tuple profiles. 2-tuple circular profiles unchanged (backward compatible; milestone-1 builders untouched).

### Adanna AD-03 V4 (`adanna/build_adanna_v4.py`, from the V3 builder)
1. Garments: wrap + skirt rebuilt as elliptical lathes following torso/hip proportions (depth < width); wrap bottom (z 1.128) overlaps skirt top (z 1.20) — waist gap eliminated; hem rows pulled inward (folded hem lips) instead of paper-thin open edges.
2. Face: brow ellipsoid smaller/flatter, jaw/chin softened; approved identity, scar, hairstyle (bun + braids + 3 bronze/2 coral LEFT-temple beads) unchanged.
3. Baldric: surface-following strap rebuilt against the elliptical chest surface, 9 segments (was 5 — stair-stepping corrected); pendant + cord re-seated on the elliptical garment surface (pendant y 0.148/0.150, cord top y 0.115). No blade/scabbard (CQ-9 unchanged).

### Guard Class V3 (`guard/build_guard_v3.py`, from the V2 builder)
1. Wrap: genuine one-shoulder construction — elliptical lathe with `slant=-0.075`, top edge rising over the anatomical LEFT shoulder (−X), bare right shoulder/chest; elliptical skirt with hem lip and waist overlap.
2. Sash: narrowed to a 72 mm elliptical band (z 1.022–1.094, rx 0.230–0.233, ry 0.174–0.176), sitting proud of the skirt with no intersection.
3. Face: brow and jaw softened as Adanna. Still unarmed, emblem-free.

## 2. Geometry statistics (before → after)

| Asset | Parts | Verts | Tris | Height | Budget (≤30k tris, 1.7–1.9 m) |
|---|---|---|---|---|---|
| Adanna V3 (M1) | 36 | ~7,004 | 13,668 | 1.837 m | PASS |
| **Adanna V4 (M2)** | 36 | 6,472 | 12,520 | 1.837 m | **PASS** |
| Guard V2 (M1) | 23 | ~5,690 | ~11,000 | 1.772 m | PASS |
| **Guard V3 (M2)** | 23 | 5,184 | 10,020 | 1.772 m | **PASS** |

Skeleton: `HUMAN_BASE_PROPOSED` unchanged — 11 joints, same bone names, same scale, both assets. UVs/materials/texture assignments carried over from the milestone-1 builders.

Checksums (SHA-256):
- `1b077d44e6ae1682016df2943890400dd96eeb4a9efae674ed0ce3e153faf892` — `out/ADANNA_AD03_V4.glb`
- `70bd81fe1f247bed350540939218038dc768bc59a30221ffb84b1718c791264a` — `out/GUARD_CLASS_V3.glb`

## 3. Regression results (sandbox, source level)
- `test_joint_influence.py`: **PASS both** (every joint ≥25 verts >0.5 weight; limb leverage ≥0.15 m — the dead-bone regression guard).
- `test_deformation.py`: **PASS both** (posed heights within bound; no weight blow-ups).
- Builder QC JSONs: `out/AD03_V4_QC.json`, `out/GUARD_V3_QC.json`; deformation JSONs alongside the GLBs.

## 4. Preview inspection (Design, sandbox renders — `previews/`, 4 views each)
Inspected directly. Adanna: elliptical wrap/skirt reads as cloth volume, no waist gap, baldric smooth diagonal L→R on the garment surface, pendant at chest centre, coils anatomical-left, back clean. Guard: one-shoulder slant covers the left shoulder and leaves the right shoulder bare front and back, 72 mm sash seated proud all round, no garment intersections visible, back clean. Known residual (unchanged from M1, not an M2 regression): low-poly faceting on limbs/face at this tri budget; cloth is still a rigid lathe (no drape folds) — acceptable at this tier, revisit only if the owner raises the budget.

## 5. Remaining defects / open items
- Blender-side pose deltas, FBX export, and Blender-rendered previews are unverified until the Mac run — the sandbox has no Blender.
- Elliptical garment + slanted wrap skinning under extreme shoulder poses can only be confirmed by the Blender finisher pose test in the Mac run.

## 6. Exact Mac rerun instructions
```sh
git fetch && git checkout arena/6e649a9b-tdd && git pull
cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
```
The script verifies the two M2 checksums, runs the joint-influence gate, finishes both characters in Blender 4.2 LTS, and re-checks deformation. **The Mac run must verify:** (a) finisher pose deltas move every joint (esp. forearm.L, shin.L, and the Guard's covered LEFT shoulder under the slanted wrap); (b) the 8 Blender previews show the one-shoulder coverage, sash seating, waist overlap, and Adanna's baldric/pendant on the garment surface; (c) commit `output/ADANNA_AD03_V4/` + `output/GUARD_CLASS_V3/` back to this branch. Design then inspects those previews and closes (or reopens) the M2 gate. PM: keep integrating the milestone-1 FBX pair until that closure is recorded.
