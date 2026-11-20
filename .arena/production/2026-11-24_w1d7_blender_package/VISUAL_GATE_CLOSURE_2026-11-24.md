# VISUAL GATE — CORRECTED RERUN INSPECTION (Mac commit `a341f33`, inspected 2026-11-24)
All 8 NEW PNGs read directly (file sizes differ from pre-fix set; not the old previews). Checked against D1–D11 of `VISUAL_INSPECTION_2026-11-24.md`. Mac evidence: both characters QC PASS — Adanna 8,660 tris / 1.837 m, Guard (pre-sash-fix build) 6,344 tris / 1.771 m, 0 unweighted, FBX+BLEND exported, deformation re-checks filed.

## Defect-by-defect verdict (from the renders)
| Check | Result | Visible evidence |
|---|---|---|
| 1. Camera orientation (D1) | **RESOLVED** | Adanna front shows chest/baldric/pendant; back shows plain back + coils on anatomical left. Guard front shows wrap face; back is the back. Labels now true. |
| 2. Armlet/armband rings (D2) | **RESOLVED** | Adanna: three distinct bronze rings stacked on the left upper arm (front + back views). Guard: single ring on the right upper arm. No strips anywhere. |
| 3. Pendant forward (D2b) | **RESOLVED** | Ring faces camera in front/three-quarter, hangs from the V cord at chest centre; edge profile correct in side view. |
| 4. Necks connected (D4) | **RESOLVED** | Both heads sit on a visible neck column; no floating gap in any view. |
| 5. Guard shoulders (D3) | **RESOLVED** | Shoulder volumes bridge torso→arm in front/three-quarter/back; no air gap. |
| 6. Indigo visible (D5) | **RESOLVED** | Deep indigo with woven check texture on wrap/skirt (both characters); sash undyed tan; bronze readable. Cultural colour identity present in renders. |
| 7. Braids seated (D6) | **RESOLVED** (at tier) | Thin dark strands lie on the back of the head (Adanna back view); no rigid bars, nothing across the face. |
| 8. Guard sash (D11) | **NOT RESOLVED in these renders** | Circular torus still protrudes as a horizontal disc (side view: sticks out front+back beyond the skirt; front: halo wider than skirt). Root cause: circle vs the skirt's elliptical cross-section (~0.171×0.115 m at sash height). **Fixed after inspection:** sash is now a flattened ellipsoid band (0.188×0.138×0.038 m, ~0.02 m uniform stand-off = wrapped cloth). Guard GLB rebuilt (3,190 v / 6,296 tris; deformation PASS; weight audit 0 unweighted; new sha256 `a3161490…`). Requires one Guard visual rerun to close. |

## Remaining (unchanged, sculpt phase — not gate blockers at this tier)
D7 wrap/skirt ellipsoid construction ("swimsuit" cut, scalloped wrap seam), D8 knee/elbow ridges, D9 blunt hands/disc feet/featureless heads, D10 mannequin proportions. These are the Blender sculpt-pass work list on the returned `.blend` files.

## Gate verdict
- **ADANNA AD-03 V2: PASS** — visual gate closed at production-intent tier (not final character approval).
- **GUARD CLASS V1: CONDITIONAL PASS** — everything resolved except D11, whose fix is built and sandbox-verified but not yet visually re-rendered. One Mac rerun of the package (Guard outputs change; Adanna's are regenerated identically) closes it.
- Mac execution evidence is committed (`a341f33`: `.blend`, `.fbx`, QC JSONs, deformation re-checks, 8 previews; no `.DS_Store`/`.blend1` included). The qualified-output folder becomes fully current when the sash rerun lands.
