# DEFINITIVE ADANNA — DELIVERY REPORT (2026-11-26)

Owner directive executed end-to-end by Design under delegated authority: approved concept → internal approval → 3D built from the concept → source-level qualification → Mac package prepared. **Blender qualification is NOT claimed** — it runs on the Mac package below; the sandbox has no Blender. Blender `.blend`/FBX deliverables are produced by that run (same finisher pipeline that qualified V1–V3); until then the GLB/OBJ are the delivered model files.

## 1. Definitive concept (INTERNALLY APPROVED — see `CONCEPT_APPROVAL_AND_RESEARCH_RECORD.md`)
Folder `concept/`: full-body FRONT / LEFT SIDE / BACK / THREE-QUARTER, detailed PORTRAIT, accessory CLOSE-UPS (temple beads+scar, armlet, pendant, baldric), MATERIAL & COLOUR reference, and the composite REFERENCE SHEET. One woman, one costume, verified per view against every identity lock (left-side beads/scar/armlet, baldric L→R front and back, no gold, no weapon). Face anchored on the OAD-02-approved master portrait; the unapproved V001 turnaround was not used.

## 2. The 3D character — ADANNA_AD03_V5
Built from the concept, not continued from V4's appearance (V4/V3 kept as fallbacks):
- **Costume reworked to the concept:** cropped bandeau wrap top with bare midriff (V4's full-length wrap removed); wrapped skirt with folded waistband roll; leather sandals (new); baldric now crosses the **back** as well as the front and tucks at the skirt waistband; spiral pendant re-seated on the chest **above** the wrap (concept portrait/close-up), cord to the neck.
- Identity exact per lock: scar LEFT cheekbone marker, exactly 3 bronze + 2 coral at LEFT temple, 3 plain coils LEFT armlet, knot + braids, plain indigo, no blade/scabbard.
- Stats: 38 parts, 6,588 verts, **12,736 tris**, **1.840 m** — budget PASS (≤30k, 1.7–1.9 m). Skeleton `HUMAN_BASE_PROPOSED` unchanged (11 joints/names/scale); UV/material slots and textures carried from the qualified pipeline.
- Files: `model/build_adanna_v5.py`; `out/ADANNA_AD03_V5.glb` (SHA-256 `7d8ff32070b42b113ad5a1da36b2d537e5e83dfa6b3ef557bdada174fff2d0f6`), `.obj/.mtl`, `out/AD03_V5_QC.json`, `out/ADANNA_AD03_V5_DEFORM.json`.

## 3. QC / deformation evidence (sandbox, source level)
- `test_joint_influence.py`: **PASS** (dead-bone regression guard).
- `test_deformation.py`: **PASS** (JSON in `out/`).
- Builder budget check: **PASS**. Mac package `run_all.sh` verified to fail-safe exit 3 here (no Blender) with checksums OK for V5 + Guard V3.

## 4. Concept vs 3D — honest comparison (`compare/ADANNA_CONCEPT_VS_3D_V5.jpg`, `previews/`)
Matches: silhouette and 7.5-head proportion; cropped wrap + midriff + waistband skirt; baldric L→R front and back; pendant position/scale; armlet, beads (exactly 3+2), scar side, knot, sandals; indigo/bronze/coral/leather palette.
**Remaining gap, stated plainly:** the 3D face is a low-poly stylised representation (nose/brow/lips/eyes/scar marker at a 12.7k-tri production-intent tier) — it carries Adanna's identity markers and proportions but is **not** a photoreal likeness of the concept portrait. Skin/hair shading is flat material colour; the Blender finisher + textures on the Mac run improve this, and a future sculpt/texture milestone (owner's call on tri budget) is where true likeness is achieved. Identity is recognisable and consistent; facial realism is the known next step, not a hidden defect.

## 5. Mac qualification (exact)
```sh
git fetch && git checkout arena/6e649a9b-tdd && git pull
cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh
```
Now finishes **ADANNA_AD03_V5** (definitive) + GUARD_CLASS_V3 (milestone 2). It must verify: pose deltas at every joint; the 8 Blender previews against the definitive concept (midriff, waistband, pendant, back baldric); then commit `output/ADANNA_AD03_V5/` + `output/GUARD_CLASS_V3/` back. Those outputs add the native `.blend` + FBX to this delivery. PM: previously qualified V3/V2 FBX remain the integration assets until Design closes the V5 gate on that evidence.
