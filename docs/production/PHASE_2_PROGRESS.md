# PHASE 2 PROGRESS — durable continuation record

**Last updated:** 2026-11-20, after macOS / UE 5.8 environment correction and scaffold repair  
**Branch:** `arena/8efaa23f-tdd`  
**Base:** `5e3d1da4eee42ad8255760530291ff91cdfb39b2`  
**Status:** ACTIVE — first directly launchable playable integration proof and provisional import handoff delivered; old Phase 2 audit remains halted; full production/commercial M1 remains blocked

## Recovered state retained

1. Recovered the Google Drive `PHASE 2 CONTINUATION.md` workspace patch and applied its 923 text-file records to the local checkout; preserved the 32 binary-only patch references without fabricating their missing bytes.
2. Read only the controlling progress records needed to establish the continuation point: `PHASE_2_SUCCESSOR_HANDOVER.md`, `RESUME_PLAN.json`, `PROGRESS_METRICS.json`, `VALIDATION.json`, `UNREGISTERED_PARTIAL_NOTES.md`, Phase 2 README, next-actions boundary, opportunities, blockers, pipeline, and software/hardware guidance.
3. Exact prior stopping point: STOP/handover after Batch 20; Batch 21 had 84 reconstructed targets but zero registered additions; 20 draft notes were unverified. No Phase 2 audit restart or bulk re-inspection was performed.
4. All Phase 1 verdicts and restrictions remain controlling. No rejected, superseded, external-authority, failed-correction, limited-study, Adanna-unapproved-view, or V013-restricted asset was promoted.
5. Five design-approved Chapter 8 environments were identified; **Hall of Posts V004** was selected as the first production target. Its local approved board was copied into the milestone's `references/` folder and source-hashed in the manifest.

## Completed visible milestone — Hall of Posts M1

Built an actual source-derived H2/H3 modular technical blockout and CPU look-development proof under `TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/`. It is a labelled production stage proxy, not a finished film set.

- **Source:** `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_HALL_OF_POSTS_V004.jpg`, Drive ID `1MHCd25z3x-cfBUf-eoCJvDLqwvYj9Ins`; client-approved 2026-11-15 / OAD-45; canon pending; consultant review still noted.
- **Geometry:** named GLB scene with nine nodes, 45,670 vertices / 72,246 triangles, 36 hardwood post instances and one stool; matching OBJ; five reusable module GLBs. GLB and OBJ were reopen-tested.
- **Look-dev:** exact seven-colour board palette; material-intent JSON; low central one-point hero, three-quarter, side/overview and eight-frame turntable renders; source-vs-render, contact sheet, and review sheet.
- **Verification:** `M1_EVALUATION.md` records approved reads present, Art Bible/restriction pass, deliberate proxy deviations, and outstanding limitations. `production_manifest.json` records source ID/hash, geometry, cameras, render method, evaluation, and next gate. `index.html` is a local static review site.
- **Toolchain:** reproducible Python 3 + NumPy + trimesh + Pillow CPU pipeline, chosen for the measured sandbox (about 4 GB RAM, no GPU, no Blender binary). This is a portable stage proof, not a claim about owner-studio hardware or a purchase recommendation. H0–H11 and the benchmark-first scale-up toolchain remain in `PRODUCTION_WORKFLOW.md`.

## Current milestone — Playable Adanna M1 real-time integration proof

The production handover's first playable target was advanced under `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/`. Hall of Posts M1 was preserved unchanged and is not the first playable milestone. This is a **directly launchable technical gameplay integration proof**, not a final commercial character, final environment, canon approval, UE cook/package or completed full-commercial M1.

- **Game-state recovery:** retained from targeted recovery: no existing UE project/version, playable project, native 3D Adanna, skeleton/rig/animation, gameplay system, Forbidden Forest 3D asset/layout or package. Phase 1 restrictions unchanged; no restricted/unapproved reference promoted. `source_authority.json` records the precise UE blocker.
- **Shared world/assets:** `world.json` and `web_build/world.json` contain 7 route waypoints, 46 obstacles, 2 interactables and gameplay constants. Generated/reopened forest GLB/OBJ, rigged technical Adanna GLB/OBJ/rig JSON, six module GLBs, materials and asset reports. Forest: 8,008 vertices / 13,238 triangles; proxy: 870 vertices / 1,584 triangles, 1 skin / 21 joints, `idle/walk/run/jump/land`.
- **Browser real-time build:** `web_build/index.html`, `main.js`, `styles.css`, `server.mjs`, `package.json`, local vendored Three.js 0.187.0 (`three.module.js`, `three.core.js`, GLTFLoader and utility modules), local GLB assets, and a relative import map. `game.js` is shared by the browser, Node integration test and CPU replay. Live server runs from `web_build/` on `0.0.0.0:8001`; Hall review remains on `0.0.0.0:8000`.
- **Provisional UE source state:** `ue_project/TDD_GAME.uproject`, Config, Targets, Build.cs, C++ game mode, runtime instanced Forbidden Forest level and technical Adanna proxy character. `Source/TDD_GAME/TDDWorldData.h` is generated from the same `world.json`; `ue_project/UE_SOURCE_STATE.md` explicitly records that no engine binary/version, compile, PIE, `.uasset/.umap` import, cook, package or UE real-time test exists.
- **Verification:** `web_build/test/integration_test.mjs` passed 11/11 fixed-step simulation checks and produced 120 replay frames at 15 fps. `web_build/test/live_build_verification.mjs` passed 67/67 static/live HTTP, recursive local ES-module, JSON/GLB integrity, capture, UE source-file and durable-record checks. `scripts/render_replay.py` executed to 120 PNG frames, GIF, MP4, hero/HUD stills, contact sheet, review sheet and `capture_manifest.json`. These moving captures use actual `game.js` simulation states, not Blender/GLB-viewer/static concept output.
- **Dedicated tracker/report:** root `PLAYABLE_MILESTONE_TRACKER.md` and `PLAYABLE_MILESTONE_REPORT.md` record the acceptance matrix, executed verification, dependencies and exact next action. `production_manifest.json` was corrected so `project_source_state_created` is derived from actual UE source files, while `compile_verified`, `real_time_ue_test_verified`, `native_uasset_umap_import_verified`, `package_verified` and `automated_webgl_render_verified` remain false.

## Current work cycle — macOS / UE 5.8 adaptation

Owner environment is now known and recorded: **Apple M4 Mac, 16 GB RAM, macOS 27.2.1, ARM64,
Unreal Engine 5.8**. The project was retargeted and inspected rather than assumed compatible.

Retargeted: `EngineAssociation` 5.4 → **5.8**; `TargetPlatforms` Windows/Linux → **Mac**;
`PythonScriptPlugin` enabled for the owner-side helper.

**Compile reached C++ (2026-11-19).** Past the target-rules rejection, UBT began compiling the
module and Clang failed on three `TActorIterator` loops that broke on their first iteration
(`-Werror,-Wunreachable-code-loop-increment`). V7 promotes `UnreachableCodeWarningLevel` to
`Error`, which is what turned a latent defect into a hard error: the loops were always pointless,
not newly wrong. Replaced with the iterator's own bool (`static_cast<bool>(TActorIterator<...>(World))`
where only presence is needed, `if (TActorIterator<...> It(World); It)` where the actor is used).
No warning was disabled.

**Correction (2026-11-19, after the first owner-machine compile).** The earlier claim that
`BuildSettingsVersion`/`IncludeOrderVersion` had been retargeted was **false**. The edit landed in
`Source/TDD_GAMEEditorTarget.cs`, which UBT never loads: the launcher engine loads only
`Source/*.Target.cs`, and the live `TDD_GAMEEditor.Target.cs` still said `V5`/`Unreal5_4`. The
audit read the dead file too, so 79 green checks certified settings that were not in force. UBT
stopped before any C++ with `TDD_GAMEEditor modifies the values of properties: [... Off != Error
...] ... build products in common with UnrealEditor`. Fixed by setting both live targets to
`V7`/`Unreal5_8`, deleting the dead file, and re-pointing the audit and the live verifier at
`TDD_GAMEEditor.Target.cs`; the audit now rejects any unloadable `TargetRules` file. No compile has
been executed.

Ten defects found and repaired (details in root `PLAYABLE_MILESTONE_TRACKER.md`): map/game-mode
keys in a section UE ignores; removed `EditorLevelLibrary` API and non-saving `new_level` in the
setup helper; no config repointing to the project map; instanced-mesh pools registered after
instances were added (collision lost); no `APlayerStart`; hand-authored input mappings that UE5
cannot deserialise; raw `UPROPERTY` pointers instead of `TObjectPtr`; invented steel blade
geometry contradicting Phase 1 restrictions; a broken pendant transform that displaced geometry
1.3 m outside the body; and the engine/build-settings mismatch.

New artefacts: `ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py` (original preserved as
`..._WINDOWS_ASSUMPTION_PRESERVED.py`), `ue_project/README_MACOS_UE58.md`,
`scripts/audit_ue_macos.py` → `ue_project/Tools/tdd_m1_macos_audit.json` (79/79 static checks).

Status: static compatibility **COMPLETED AND VERIFIED**; compile/`.umap`/import/PIE/cook/
package/launch remain **BLOCKED — OWNER-STUDIO DEPENDENCY**.

## Current independent work cycle — Adanna technical import handoff

To continue production while owner-studio UE access and Creative Director approvals remain outstanding, a labelled technical UV/material/collision import handoff was produced under `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/model/`. The preserved rigged technical GLB was not overwritten.

- `scripts/build_adanna_uv_handoff.py` produced `model/adanna_m1_technical_proxy_uv.glb` with face-corner UV0, an embedded eight-slot provisional base-colour atlas, preserved 21-joint skin and `idle/walk/run/jump/land` clips. It reopens in Trimesh with 4,752 face-corner vertices / 1,584 triangles.
- New visual/technical evidence: `model/adanna_m1_uv_atlas.png`, `model/adanna_m1_uv_layout.png`, `model/adanna_m1_collision_proxy.obj`, `model/adanna_m1_ue_import_manifest.json`, `model/adanna_m1_uv_validation.json`, plus `web_build/captures/adanna_m1_uv_atlas.png` and `web_build/captures/adanna_m1_uv_layout.png`.
- Local validation: **33/33 checks passed**. Scope is GLB binary/accessor integrity, UV range/all atlas patches, embedded PNG, preserved skin/clips, material texture reference, atlas/layout images, collision OBJ reopen, import manifest, owner request and UE setup helper. It is **not** UE import/compile/PIE/cook/package.
- Root `OWNER_STUDIO_UNREAL_REQUEST.md` records only the owner information/access needed. `ue_project/Tools/TDD_M1_Unreal_Setup.py` is an owner-side Unreal Python helper for engine-version capture, project-owned `/Game/TDD/Maps/PLAYABLE_FOREST_M1.umap` creation/save and labelled technical import attempts. Status: **PRODUCED — NOT YET VERIFIED**; it has not been run because no Unreal binary exists in this sandbox.
- Required status classification is maintained in root `PLAYABLE_MILESTONE_TRACKER.md`. The handoff is **COMPLETED AND VERIFIED** for local file/GLB validation, **PROVISIONAL — AWAITING CREATIVE APPROVAL** for final use, and **BLOCKED — OWNER-STUDIO DEPENDENCY** for UE execution.

## Files created or modified

- `CONTINUATION_MAP.md` — concise continuation map.
- `PHASE_2_PROGRESS.md` — this file, now updated after M1.
- `TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/PRODUCTION_BRIEF.md`, `SOURCE_AUTHORITY.md`, `PRODUCTION_WORKFLOW.md`, `M1_EVALUATION.md`.
- `TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/scripts/build_hall_of_posts_m1.py` — deterministic reproducible build script.
- `TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/references/`, `model/`, `model/modules/`, `renders/`, `renders/turntable_frames/`, `production_manifest.json`, `materials.json`, `index.html`.
- `google_drive/PHASE 2 CONTINUATION.md` — downloaded workspace patch, ignored by Git.
- Recovered prior directories: `TDD_PHASE2_PRODUCTION_READINESS_AUDIT_v1/`, `OUR_EYES_CD_FINAL_VERDICTS_v1/`, `PHASE_2_SUCCESSOR_HANDOVER_FILES/`, `PHASE_2_SUCCESSOR_HANDOVER_SUPPORT/`, and root `PHASE_2_SUCCESSOR_HANDOVER.md`.
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/` — playable milestone scaffold, source authority, generated GLB/OBJ/module assets, materials, world, reports, browser build, captures and provisional UE source state.
- Root `PLAYABLE_MILESTONE_TRACKER.md` — dedicated acceptance/status tracker; `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/PLAYABLE_MILESTONE_REPORT.md` — concise handover report.
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/scripts/build_assets.py`, `gltf_skin.py`, `generate_ue_world_data.py`, `render_replay.py` — reproducible asset/world/replay/UE-data pipeline.
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/web_build/game.js`, `index.html`, `main.js`, `styles.css`, `server.mjs`, `package.json`, `test/integration_test.mjs`, `test/live_build_verification.mjs`, `vendor/` — directly launchable browser build and verification.
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/` — `.uproject`, Config, Target/Build.cs, C++ gameplay/level/character classes, generated shared world header, owner-side `Tools/TDD_M1_Unreal_Setup.py` and `UE_SOURCE_STATE.md`.
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/model/adanna_m1_*` — newly added UV GLB, provisional atlas, UV layout, neutral collision proxy, UE import manifest and local validation report.
- Root `OWNER_STUDIO_UNREAL_REQUEST.md` — concise owner-studio UE/hardware/access request; no credentials requested.

## Decisions and dependencies

- **Selection:** Hall of Posts V004 has exact approved visual information, strong Chapter 8 film importance, modular reusability, no active restricted-asset dependency, and establishes an environment pipeline. It was not selected merely for ease.
- **Final-production gate:** CD film-use/canon selection and one approved common Chapter 8 spatial/metric/camera interpretation (P2-G09 / P2-CD04). Consultant review noted on the board also remains outstanding.
- **M1 boundary:** no approved dimensions, canon, final topology/UVs, calibrated PBR maps, carved iconography, exterior geography, rig, animation, VFX, compositing, or finished film set is claimed. Neutral exposure cards are render aids only.
- **Restrictions retained:** no V013 item-5 claim, no Adanna body/blade interpretation, no CQ-9 fit, no H3 visual release, no six visual-only passes as production authority, no rejected/superseded artwork, no failed corrections, and no limited internal studies as production designs.
- **Audit boundary:** M1 does not close the old Phase 2 audit, add a global readiness verdict, or alter the 84-target Batch 21 queue.
- **Playable classification:** current playable work is a real-time technical integration milestone toward the first playable character, not a completed final commercial M1. The browser build is directly launchable; the UE state is source-only. No UE compile/cook/package or automated headless WebGL render is claimed.
- **Shared-world decision:** browser, Node integration, CPU replay and provisional UE source all derive from the same `world.json`; UE uses a generated C++ header rather than a second invented layout. GLB assets are labelled technical proxies; no `.uasset/.umap` import or final skeleton/animation Blueprint is claimed.
- **Playable dependencies:** owner-studio UE version/binary/hardware profile; CD/Research final Adanna turnaround/dimensions/groom/costume/facial authority; CD film/game canon, consultant review, shared forest spatial/metric/camera interpretation and botanical check. Exploratory boards, restricted Adanna views and rejected/superseded/failed/limited-study assets remain non-authoritative.
- **Required status classification:** root `PLAYABLE_MILESTONE_TRACKER.md` now assigns exact `COMPLETED AND VERIFIED`, `PRODUCED — NOT YET VERIFIED`, `TECHNICALLY DEMONSTRATED — NOT INTEGRATED`, `PROVISIONAL — AWAITING CREATIVE APPROVAL`, `BLOCKED — OWNER-STUDIO DEPENDENCY`, `BLOCKED — CREATIVE APPROVAL` and `NOT STARTED` statuses to each deliverable group. Technical file validation is never treated as UE integration or creative approval.

## Current blockers

- **Playable M1 / UE verification:** no Unreal Engine binary, recovered engine version, or owner-studio hardware/licence profile is available in this sandbox. UE compile, `.uasset/.umap` import, PIE, cook, package and device-level real-time test are blocked. Root `OWNER_STUDIO_UNREAL_REQUEST.md` names the exact missing information/access; `ue_project/Tools/TDD_M1_Unreal_Setup.py` is a produced-but-unverified owner-side helper. No automated headless browser/WebGL screenshot is available either; the live preview is exposed to the user's browser instead.
- **Playable M1 / final assets:** CD/Research authority for final Adanna turnaround/dimensions/groom/costume/facial rig, and CD film/game canon plus consultant review/shared forest spatial/metric/camera interpretation/botanical check remain outstanding.
- **Hall of Posts final production (retained):** CD approval of film use/canon plus one shared spatial/metric/camera interpretation; consultant review also remains required. Hall M2 is not the primary task unless it directly supports the larger game production schedule or the Creative Director authorises it.

## Exact next action

1. Open the Playable Adanna M1 live preview on port 8001 and visually confirm browser WebGL play.
2. On the M4 Mac follow `ue_project/README_MACOS_UE58.md`: confirm Xcode 26.0–26.3 and record `Build.version`; compile with `Engine/Build/BatchFiles/Mac/Build.sh TDD_GAMEEditor Mac Development -project=... -architecture=arm64`; run `ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py` in the Editor to create/save the project-owned `.umap` and import the handoff; verify the GLB lands as a Skeletal Mesh with 21 bones and 5 sequences; PIE-verify movement/camera/collision/interaction/route; then record cook, package and packaged-app launch.
3. Obtain the precise CD/Research approvals above, replace labelled technical proxies with approved game-ready Adanna and production forest kit, and proceed into M2 character/environment quality, M3 gameplay foundation and M4 first vertical slice.
4. Do not restart the old Phase 2 audit, repeat Hall M1, promote restricted assets, or claim a final commercial character/UE package from the current technical proof.
