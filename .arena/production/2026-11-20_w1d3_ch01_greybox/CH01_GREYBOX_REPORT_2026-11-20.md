# CH01 PROVISIONAL GREYBOX — BUILD REPORT (2026-11-20 W1 D3)
**Authorization:** owner 2026-11-20 (C-01): provisional greybox construction authorized immediately; §9 modules binding; dimensions = engineering assumptions, NOT canon; PM/TD may adjust for function; no final architecture/materials/props approved.

## Deliverables on disk
- `build_ch01_greybox.py` — full parametric builder (Blender 4.2+/5.x API, bpy). Constructs terrain, stream strip, roads (fork L23, gate→square, square→stream, palace axis), perimeter wall ring w/ gate gap, GATE_MOD (posts+leaves), 8 hut/store masses (HUT_A/B/C incl. flagged proposed subjects), interior blockouts (Smithy/Healer/Weaver/Potter*/Kitchen/Backrooms/Bedroom), palace complex (courtyard plate, portal block, hall block, 8 verandah posts on 3.0 m rhythm, throne massing), 6 market stalls (hipped), square (tree blocker, well, ekwe massing), farm tiles, pen, compound wall, gate-guard shelter (flagged), and 15 gameplay anchor empties (SPAWN, GATE_ENTRY trigger, RG patrol A–D, backroom doors, palace/throne approach, ekwe zone, wading entries, farm fork). Objects prefixed by token; proposed subjects on GRY_FLAG_PROPOSED material. Saves .blend, exports FBX (cm, apply_unit_scale, -Y/Z axes), writes manifest JSON.
- `render_plan.py` + `CH01_GREYBOX_PLAN.png` — 1350×1350 m-grid top-down engineering schematic (labels, anchors, legend; visually verified 2026-11-20). **A layout aid — not art, not a render.**
- `CH01_GREYBOX_MANIFEST.json` — machine-readable inventory + anchors + exclusions. **ABSENT on disk** (written by the builder at run time) — regenerate on first successful build.
- `CH01_RESEARCH_NOTES_2026-11-20.md` — Igbo vernacular architecture seed; generation NOT READY; recorded sources + uncertainty.

## Execution status — HONEST
**The .blend/FBX were NOT produced in this environment.** `pip install bpy` succeeded (5.0.1) but import fails: missing system libraries `libXrender.so.1`, `libSM.so.6`, `libICE.so.6`, `libGL.so.1`, `libGLX.so.0`, `libOpenGL.so.0`, `libXt.so.6`, `libXi.so.6`, `libXfixes.so.3`, `libxkbcommon.so.0`. No root/apt access; PyPI wheels bundling mesa/X11 were hunted and none exists (wxPython sdist-only; PySide6-Essentials bundles no GL/X11). System has no mesa anywhere on disk. This is an environment limitation, not a script defect: the blocker is reproducible and the fix is known.
**Script correctness:** carefully reviewed; not executed end-to-end. Treat as v0.1 — first run on a capable machine is the test.

## To produce the actual greybox (any one of)
1. Workstation with Blender ≥4.2 GUI: open `build_ch01_greybox.py` in Scripting workspace → Run Script. Outputs land beside the script (blend+fbx+manifest).
2. Headless Linux box with system libs: `apt install libxrender1 libsm6 libice6 libgl1 libxt6 libxi6 libxfixes3 libxkbcommon0` then `python3 build_ch01_greybox.py` (needs bpy pip module or system Blender python).
3. CI/container: any image based on `blender:4.x` docker image running `blender -b -P build_ch01_greybox.py`.
Then: import FBX into UE 5.8.4 (cm), verify axis/scale on first import, PM walkthrough per §9.4 step 6, log deviations, THEN final-asset requests may be drafted.

## Verification done honestly
Layout coherence checked on the PIL schematic (wall ring closed with gate gap; palace axis linear from gate→square→throne; stream south; farms west outside wall; compounds SE; anchors placed at functional points). Collision = primitives only. NOTHING approved; no boards stood in for; no canon claims. Ch01 design-board reviews (C-01/CD/Research) proceed independently and are NOT blocked by this greybox; the greybox also must not block them.
