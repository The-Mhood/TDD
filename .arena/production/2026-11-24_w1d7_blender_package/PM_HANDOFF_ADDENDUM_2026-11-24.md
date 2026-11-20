# PM HANDOFF ADDENDUM — BLENDER EXECUTION PACKAGE (2026-11-24)
For PM/owner: the only outstanding infrastructure action from W1 D7 is now a packaged, single-command run.
- Package: `.arena/production/2026-11-24_w1d7_blender_package/` — `README.md` (full procedure), `run_all.sh`, `blender/finish_character.py`, `INPUT_CHECKSUMS.sha256`.
- Owner/PM action: on any Apple Silicon Mac with Blender 4.2 LTS in /Applications: `cd .arena/production/2026-11-24_w1d7_blender_package && ./run_all.sh` (~2 min hands-on, 2–5 min machine), eyeball 8 previews, commit `output/` back to `arena/6e649a9b-tdd`.
- PM receives from that run: 2× `.blend` (native editable), 2× FBX (Unreal-ready), 2× Blender QC JSONs, 8 preview PNGs, 2 deformation re-checks — completing the W1 D7 §4 export package for Adanna + guard.
- Parallel lanes unaffected: CH01 settlement modules and both GLB models are already importable today (see W1 D7 handoff); this package adds the Blender-native projects/FBX, it does not gate anything else.
- If the run errors: README §8 maps each message to one action; QC JSON + log return to Design for a script-side fix. No owner troubleshooting beyond §8.

## UPDATE — Mac qualification evidence (2026-11-24)
- Mac runs completed (Blender 4.2.23 LTS): first run `6999ea7`, corrected rerun `a341f33` — `.blend` + FBX + QC JSONs + deformation re-checks + 8 previews committed in `output/`. Visual gate: **Adanna PASS**; **Guard conditional** (sash fix rebuilt, one rerun outstanding) — see `VISUAL_GATE_CLOSURE_2026-11-24.md`.
- PM can integrate NOW: `output/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` and `output/GUARD_CLASS_V1/GUARD_CLASS_V1.fbx` — **both visually gate-passed** (sash rerun `3fd912a` closed the Guard; same skeleton/materials throughout). Remaining character work is the sculpt phase (D7–D10), which iterates on these `.blend` files without changing rig or scale.

## UPDATE — Sculpt milestone 1 qualified (2026-11-25)
Adanna AD-03 V3 + Guard Class V2 both passed their sculpt-milestone visual gates (Mac commits `38a0377`, `4fb1c6d`; Design inspections filed in `2026-11-25_w1d8_sculpt/SCULPT_MILESTONE_1_REPORT.md`). **PM: integrate `output/ADANNA_AD03_V3/ADANNA_AD03_V3.fbx` and `output/GUARD_CLASS_V2/GUARD_CLASS_V2.fbx`** (shared 11-joint skeleton, unchanged names/scale). V2/V1 qualified builds remain in their folders as fallback.
