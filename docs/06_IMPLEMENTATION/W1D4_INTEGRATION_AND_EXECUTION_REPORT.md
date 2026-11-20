# W1 D4 — Design integration and first-playable execution report

**PM branch:** `arena/553fb02d-tdd`
**PM W1 D3 source commit:** `8721a97cbb0f85a2a7b952a29e515276725730e9`
**Design source commit reviewed/imported:** `d50658a346a9cda4ba851aa24979f1b9d9cddc70` (`arena/6e649a9b-tdd`, parent `57b81bd52ce153ed7a6c54643677629db927fa8f`)
**Result:** controlled Design-file integration and build-pipeline improvement are prepared in the PM working branch. No Blender/Unreal build or gameplay was possible in this host; status below is explicit.

## Feature evidence matrix

| Workstream / feature | Implemented / integrated in source | Built / compiled | Executed in Unreal | Verified in gameplay | Known defects / next evidence |
|---|---|---|---|---|---|
| WS1 — Adanna movement, jump, landing, traversal | D3 `UTDDTraversalComponent` is attached and bound to E / Gamepad Y; D3 state rules allow CMC-driven traversal takeoff/landing. | Pure C++ rules pass; UE module **not compiled**. | **No** | **No** | Must UHT/UBT build, then PIE-test vault, drop, rejection/no-side-effect, walk/run/jump/landing and both inputs. Current provisional proxy still is not an approved production character. |
| WS2 — Combat | Existing actor-facing attack/damage/guard/parry/stagger/death source plus D3 invulnerability/death handling. | Pure combat math passes 39/39; UE module **not compiled**. | **No** | **No** | Hit trace is currently resolved synchronously at attack invocation rather than a measured animation active window; verify actual collision and timing. PIE hit/miss/chip/posture/parry/stagger/death matrix remains outstanding. |
| WS3 — Training enemy / boss | Enemy, token director and phase graph source already present; D3 added a training boss actor and phase-invulnerability damage gate. | Pure AI 111/111; UE source/automation **not compiled/run**. | **No** | **No** | Enemy currently finds the player through direct player-character lookup, not a verified UE Perception/StateTree pipeline. Test token cap, range/attack, reactions, graph entry/transitions/invulnerability and defeat in the actual level. |
| WS4 — Adanna production/import | Design workbook §11 and controlled-batch brief imported. They preserve identity locks, keep blade/scabbard deferred, and leave V003/V004 selection gated. PM technical proxy remains unchanged. | Blender/UE import **not run**. | **No** | **No** | No approved production mesh or usable approved animation set is supplied by this Design commit. Do not promote the technical proxy; complete exact-version Our Eyes/Research review and delegated CD selection, then import/build and inspect. |
| WS5 — Chapter 1 greybox | Imported the Design §9 spec, parametric Blender builder, render script, report, research notes and plan PNG. Preserved the original Design schematic; PM D4 source patch swings gate leaves open and creates doorway shells for huts/interiors/palace. Existing PM forest builder remains separate and unchanged. | Patched schematic renderer executed and produced a new 1350×1350 plan (the original renderer output matched the original Design PNG byte-for-byte); builder Python syntax passes. Blender `.blend`/FBX/manifest **not produced**. | **No** | **No** | Patch still needs Blender/UE execution. Validate doorway clearances, FBX scale/axes/collision/navigation and add PlayerStart/GameMode/encounter actors in UE. |
| WS6 — Platform builds | Windows CI now includes a separate `TheDisobedientDaughter Win64 Shipping` UBT stage with dedicated evidence log. | Static shell/safety checks pass. Mac, Win Development/automation and Win Shipping **not executed**. | **No** | **No** | Run on the actual Apple Silicon UE 5.8.4 owner Mac and reference Windows PC. Shipping compilation is not a cook/package claim. |
| WS7 — Tests / evidence | D1–D3 source preserved; Design source blobs are hash-checked against the exact imported Git objects. | 6 pure suites, 883/883 assertions; runner and Windows CI safety tests pass; Blender/UE script syntax checks pass. | **No** | **No** | These are host checks only; no UE automation or visual/gameplay evidence. D4 outputs are stored under `docs/06_IMPLEMENTATION/evidence/20261120T-W1D4/` and Design integration evidence under `.arena/production/2026-11-20_w1d3_ch01_greybox/evidence/`. |

## Design integration scope

Design's `d50658a` was reviewed in place and imported file-by-file. See `.arena/production/2026-11-20_w1d3_ch01_greybox/PM_INTEGRATION_RECORD_2026-11-20_W1D4.md` for the exact 13-file list, source hashes, review notes, and separate-vs-integrated scope. No branch switch, reset, rebase, wholesale merge, or overwrite was performed. The Design branch/history and unlisted Design work remain separate.

Integrated items include the CH01 provisional layout schematic (PNG), actual parametric builder source, §9 engineering layout spec, owner/production records, FP-10 scope, and Adanna/FP-07 D3 updates. The imported Design report itself explicitly states that its `.blend`, FBX and manifest were absent; the schematic is not those deliverables.

## Execution attempts and exact results

- PyPI `bpy==4.5.16` installed under `/tmp/tdd-bpy`; importing it failed before builder execution: `ImportError: libXrender.so.1: cannot open shared object file`. `ldd` additionally reports missing `libGL.so.1`, `libICE.so.6`, `libSM.so.6`, `libXfixes.so.3`, `libXi.so.6`, and `libxkbcommon.so.0`. Full output: `.arena/production/2026-11-20_w1d3_ch01_greybox/evidence/EXECUTION_BLOCKER_LINUX.txt`.
- `blender`, `UnrealEditor`, and `UnrealEditor-Cmd` are not installed/discoverable in this Linux x86_64 host. UE 5.8.4 build, Editor import, map generation, navigation build, PIE and automation therefore did not run.
- `Tools/engine/mac_build.sh` returned the explicit macOS host gate: NOT EXECUTED; no build.
- `Tools/engine/windows_ci.sh arena/553fb02d-tdd` returned the explicit MINGW/MSYS/CYGWIN host gate: NOT EXECUTED; no checkout or build.
- Pure tests: **6/6 suites, 883/883 assertions**. Runner contract and updated Windows safety/Shipping-stage source test pass. Logs are in `docs/06_IMPLEMENTATION/evidence/20261120T-W1D4/`.

## Reproducible owner-platform sequence

1. **Blender:** use the authorized workstation installation (Blender 4.2+; align actual version with TD's production pin), run the command in the imported integration record, and verify the three expected outputs: `CH01_GREYBOX.blend`, `CH01_GREYBOX.fbx`, `CH01_GREYBOX_MANIFEST.json`. Open the `.blend` in GUI Blender. First fix the closed gate and solid interior shells; inspect the wall ring, roads, stream, square, palace axis, market and anchors at the stated metre scale. Capture the Blender version, stdout, output hashes, and screenshots.
2. **Unreal:** on the owner Mac, set `UE_ROOT` to the installed 5.8.4 engine and run `Tools/engine/run_daily_train.sh`. Import the FBX as a scene into a new technical-only content folder, never over existing production assets. Verify cm scale, +Z/up and -Y/forward conversion, actor hierarchy, collision and navigation; build a new map from the scene, add the correct GameMode/PlayerStart and encounter actors, and save it. Capture import/build/automation logs and screenshots.
3. **PIE:** verify gate passage and closure behavior; interior entry; Adanna movement/sprint/jump/landing/traversal (E and Gamepad Y); attacks, hit/miss, health/posture, guard/parry/stagger/death; trainer token cap and reactions; boss phase transitions/invulnerability. Record actual values, logs, screenshots and a short gameplay recording; fix failed checks and repeat.
4. **Windows x64:** from a clean, synced PM branch on the reference PC, run `Tools/engine/windows_ci.sh arena/553fb02d-tdd`. Preserve the Win64 Editor Development and automation logs plus the new `02b-build-win64-shipping.log`. Verify the Shipping executable exists. If release package validation is required, separately run the project's approved `RunUAT BuildCookRun` profile and retain cook/package logs; this helper only proves target compilation.

No major feature is marked built, Unreal-executed, or gameplay-verified without that platform evidence.
