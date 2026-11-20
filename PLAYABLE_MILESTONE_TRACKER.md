# PLAYABLE MILESTONE TRACKER — TDD

**Branch:** `arena/8efaa23f-tdd`  
**Base:** `5e3d1da4eee42ad8255760530291ff91cdfb39b2`  
**Last updated:** 2026-11-20, after the macOS / UE 5.8 environment correction  
**Status:** ACTIVE — directly launchable real-time gameplay integration proof delivered; full production/commercial M1 acceptance is **not** complete.  
**Controlling task:** M1 — first playable Adanna inside a real Forbidden Forest game environment, as a production continuation, not a new project and not a Phase 2 repeat.  
**Path key:** `PLAY = TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1` relative to repository root.

## Boundary

Hall of Posts M1 is preserved unchanged and remains an H2/H3 technical blockout. It is **not** the first playable milestone. Phase 1 verdicts/restrictions remain authoritative. `RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER` applies to all Adanna geometry in this tracker. No rejected/restricted/unapproved artwork, turnaround, canon detail, or exploratory board was promoted.

## Owner environment — confirmed

**Apple M4 Mac · 16 GB RAM · macOS 27.2.1 · ARM64 / Apple Silicon · Unreal Engine 5.8 installed.**
No Windows target is assumed anywhere in the project. `EngineAssociation` is `5.8`; both targets
use `BuildSettingsVersion.V7` and `EngineIncludeOrderVersion.Unreal5_8`; `TargetPlatforms` is `Mac`.

Toolchain requirement: Xcode 26.0 minimum, 26.1.1 recommended — **Xcode 26.4 is not compatible
with Unreal Engine 5.8**. Metal 1.2 class GPU required; M4 satisfies it.

Still unexecuted: compile, project-owned `.umap`, import, PIE, cook, package, launch. Those are
**BLOCKED — OWNER-STUDIO DEPENDENCY** and are gated on the owner running
`PLAY/ue_project/README_MACOS_UE58.md`.

## Required status classification

| Deliverable group | Status |
| --- | --- |
| Targeted production-state recovery and Hall of Posts M1 preservation | **COMPLETED AND VERIFIED** |
| Shared `game.js` simulation, Node integration test and 120-frame replay captures | **COMPLETED AND VERIFIED** |
| Browser static/live HTTP delivery and local ES-module graph | **COMPLETED AND VERIFIED** |
| Browser gameplay feature set relative to Unreal integration | **TECHNICALLY DEMONSTRATED — NOT INTEGRATED** |
| Adanna UV0/material-atlas/collision import handoff, local file/GLB validation | **COMPLETED AND VERIFIED** |
| Adanna final appearance, dimensions, groom, costume, facial design and final UV/texture authority | **BLOCKED — CREATIVE APPROVAL** |
| UE `.uproject`, Config, Targets, Build.cs, C++ source and owner-side setup helper | **PRODUCED — NOT YET VERIFIED** |
| Project-owned `.umap`, native `.uasset` import, compile, PIE, cook, package and runnable build | **BLOCKED — OWNER-STUDIO DEPENDENCY** |
| Final Forbidden Forest canon, botanical, landmark and production environment assets | **BLOCKED — CREATIVE APPROVAL** |
| M3/M4 gameplay foundation and vertical slice | **NOT STARTED** |

## Acceptance matrix

| Area | Required | Delivered now | Status / precise gap |
| --- | --- | --- | --- |
| Existing Unreal project/version recovery | Recover current UE project/version and playable project state | Targeted recovery found no `.uproject`, `.uasset`, `.umap`, playable build, native character/rig/animation/gameplay system, forest 3D asset/layout or package. The **owner's installed engine is UE 5.8 on M4 macOS**, supplied directly, so no engine version is outstanding | Recovery completed. Existing project state: none. Engine/target environment: known. |
| Working Unreal project state / verified continuation | UE source state or verified continuation | Source state retargeted to macOS/UE 5.8: `.uproject` (`EngineAssociation` 5.8, Mac, Python plugin), Targets (`BuildSettingsVersion.V7`, `Unreal5_8`), Build.cs, game mode, runtime forest level, proxy character, generated `TDDWorldData.h`; 69/69 static compatibility audit | **Source only, statically audited.** No compile, PIE, cook, package or launch. Owner must run `ue_project/README_MACOS_UE58.md`. |
| Approved Adanna identity/proportions | Approved identity/proportions; no invented design/canon | Approved master reference used only for recorded identity locks and sampled skin palette; no unapproved turnaround, dimensions, costume or canon invented | Approved detail retained; final turnaround/dimensions/groom/costume technical interpretation still require CD/Research authority. |
| Production-quality 3D Adanna | Production topology, UVs, materials, hair/clothing, optimisation | Labelled technical proxy: `model/adanna_m1_technical_proxy.glb` (1 skin, 21 joints, 5 clips, 870 vertices / 1,584 triangles), OBJ, rig JSON, rigid-part markers for approved identity features | **Not met as production character.** No final sculpt, retopology, UVs, calibrated PBR maps, groom, facial rig or commercial mesh. |
| Functional skeleton / animation | Walking, running, turning, jumping, landing | Shared `game.js` simulation drives `idle/walk/run/jump/land`; browser GLB contains 21-joint skin and clips; rigid-part UE source proxy uses procedural limb motion | Technical function proven in browser/Node simulation; no final imported UE SkeletalMesh/Animation Blueprint. |
| Gameplay | Third-person movement, run/turn/jump/land, camera follow/collision, character collision/ground detection, interaction | `game.js` shared simulation; Node integration report `overallPass: true`, 11/11 checks; UE C++ source implements equivalent CharacterMovement/spring-arm/interaction/route logic | Browser/Node executed. UE real-time execution unverified. |
| Forbidden Forest environment | Playable level, terrain/path, trees/roots/rocks/vegetation/assets, collision/navigation, lighting/atmosphere, coherent route | `model/forbidden_forest_m1.glb` (12 named nodes, 8,008 vertices / 13,238 triangles), OBJ, six module GLBs; `world.json` with 7 route waypoints, 46 obstacles, 2 interactables; laterite path, canopy, trunks, roots, rocks, understory, boundary posts, white cloth, Great Root Mother; browser fog/lights; UE runtime instanced blockout | Playable technical blockout delivered. No final art, navigation bake, botanical/canon sign-off, final atmosphere or UE lighting build. |
| Integration | Import into UE, real-time test, packaged or directly launchable build | Directly launchable browser build: `web_build/index.html`, `main.js`, `styles.css`, `server.mjs`, local vendored Three.js/GLTFLoader; live preview on `0.0.0.0:8001`; same `world.json`/`game.js` shared by browser, Node test and replay. For Unreal: macOS runbook, config-derived map repointing, skeletal-mesh import helper | **Browser delivery verified; Unreal not integrated.** No `.umap`, import, compile, PIE, cook, package or launch on the Mac. |
| Visual proof | Screenshots/video demonstrating actual result | 120 CPU-rendered simulation-state PNG frames, `playable_replay.gif`, `playable_replay.mp4`, hero/HUD stills, contact sheet, `PLAYABLE_M1_REVIEW_SHEET.png`, `capture_manifest.json` | Moving captures from actual fixed-step simulation states, not Blender render/GLB viewer/static screenshot. Automated WebGL screenshot not run because no browser binary is installed. |
| Reporting | Concise progress report, durable progress, dedicated tracker | `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/PLAYABLE_MILESTONE_REPORT.md`, this tracker, updated root `PHASE_2_PROGRESS.md`, `production_manifest.json`, `ue_project/UE_SOURCE_STATE.md` | Delivered. |

## Current work cycle — macOS / UE 5.8 adaptation and scaffold repair

The target environment changed from "unknown, assumed Windows-ish" to a verified Apple M4 /
16 GB / macOS 27.2.1 / UE 5.8. The scaffold was inspected and repaired rather than assumed
compatible. Defects found and fixed, all of which would have blocked or silently broken the
first owner build:

1. **Wrong INI section (silent, serious).** `GameDefaultMap`, `EditorStartupMap` and
   `GlobalDefaultGameMode` sat under `/Script/Engine.Engine`. UE reads them from
   `/Script/EngineSettings.GameMapsSettings`, so the game mode would never have applied and
   the forest/proxy would never have spawned. Fixed.
2. **Removed editor API in the setup helper.** The original used `unreal.EditorLevelLibrary`,
   deprecated since UE 5.0 and removed from the default path in UE 5.7+, and `new_level()`,
   which leaves no saved `.umap` on disk. Replaced with `LevelEditorSubsystem`,
   `new_level_from_template`, `save_current_level`, `save_asset`. Original preserved as
   `Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py`.
3. **Map never loaded even if created.** Nothing repointed `GameDefaultMap`. The macOS helper
   now rewrites those two keys after a successful save, backing the config up first.
4. **Collision silently missing.** Runtime instanced-mesh pools were created and instances
   added before `RegisterComponent()`, so UE5 built no physics state and every tree, root and
   boundary post would have been walk-through. Registration order fixed.
5. **No PlayerStart.** A generated map with no `APlayerStart` cannot possess a pawn in PIE.
   The forest level now spawns one at the world spawn when none exists.
6. **Input path.** `DefaultInput.ini` used hand-authored `AxisMappings`/`ActionMappings`, which
   UE5 serialises as map keys and cannot be reliably authored by hand. Replaced with
   code-registered key bindings using correct `BindKey` (parameterless) and `BindAxisKey`
   (`float`) signatures.
7. **Deprecated raw UPROPERTY pointers.** Converted to `TObjectPtr`, required under
   `BuildSettingsVersion.V7`.
8. **Invented blade geometry in the UE proxy.** A steel blade box contradicted the Phase 1
   restriction against inventing blade design. Removed; only the approved LEFT-hip cross-draw
   leather mount marker remains.
9. **Broken pendant transform (asset defect).** The spiral pendant was rotated about the world
   origin *after* being lifted to chest height, throwing it 1.3 m in front of the body at knee
   height. It passed every UV check. Fixed and now covered by a geometry-envelope regression test.
10. **Engine/build-settings mismatch.** `EngineAssociation: 5.4` with `BuildSettingsVersion.V5`
    and `Unreal5_4` include order against a 5.8 install. Now `5.8` / `V7` / `Unreal5_8`.

New verification: `scripts/audit_ue_macos.py` → **69/69** static compatibility checks
(`ue_project/Tools/tdd_m1_macos_audit.json`). This is source inspection, **not** a compile.

## Current work cycle — Adanna technical import handoff

A new independent production task was executed without waiting for owner-studio UE access or locking unresolved creative decisions. The preserved `model/adanna_m1_technical_proxy.glb` was **not** overwritten; its hash is recorded in the new import manifest.

- **Produced:** `PLAY/model/adanna_m1_technical_proxy_uv.glb` — face-corner UV0 GLB with embedded 8-slot provisional base-colour atlas, 21-joint skin and `idle/walk/run/jump/land` clips retained. Reopened in Trimesh: 4,752 face-corner vertices / 1,584 triangles.
- **Produced:** `PLAY/model/adanna_m1_uv_atlas.png`, `PLAY/model/adanna_m1_uv_layout.png`, plus browser-review copies at `PLAY/web_build/captures/adanna_m1_uv_atlas.png` and `PLAY/web_build/captures/adanna_m1_uv_layout.png`.
- **Produced:** `PLAY/model/adanna_m1_collision_proxy.obj` — neutral 0.34 m radius / 1.76 m height gameplay capsule; explicitly **not approved character dimensions**.
- **Produced:** `PLAY/model/adanna_m1_ue_import_manifest.json` and `PLAY/model/adanna_m1_uv_validation.json` — scale/axis notes, material slots, skeleton/collision metadata, exact status classifications and 33/33 local checks.
- **Produced:** root `OWNER_STUDIO_UNREAL_REQUEST.md` — concise owner request containing only the UE version/build/path/access, hardware and execution evidence required.
- **Produced:** `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup.py` — owner-side Unreal Python helper for engine-version capture, project-owned `/Game/TDD/Maps/PLAYABLE_FOREST_M1` creation/save and labelled technical asset import attempts. Status: **PRODUCED — NOT YET VERIFIED**; it has not been run because no Unreal binary exists in this sandbox.
- **Reproducible script:** `PLAY/scripts/build_adanna_uv_handoff.py`.

Local validation status: **COMPLETED AND VERIFIED** for file/GLB/UV/collision checks only. Final Adanna/forest appearance remains **BLOCKED — CREATIVE APPROVAL**. UE import, compile, PIE, cook, package and runnable build remain **BLOCKED — OWNER-STUDIO DEPENDENCY**.

## Executed verification

- `web_build/test/integration_report.json`: 11/11 checks passed; 60 Hz shared simulation; 120 replay frames at 15 fps. Checks cover camera collision, walk/run, turning, jump/land, interaction, route progress and obstacle collision.
- `web_build/test/live_build_report.json`: 67/67 static/live HTTP delivery, recursive local ES-module graph, generated JSON/GLB integrity, capture presence, UE source-file presence and durable-record checks passed. This is **not** an automated WebGL render test or UE compile/cook/package test.
- `web_build/captures/capture_manifest.json`: MP4 written; 120 frames; hero, HUD, contact sheet and review sheet present.
- `PLAY/scripts/render_replay.py` was executed successfully in 150.1 s. The frames are rendered from `web_build/test/replay_frames.json`, which stores actual `game.js` simulation states.
- `python3 PLAY/scripts/generate_ue_world_data.py` generated `TDDWorldData.h` from `world.json`: 7 waypoints, 46 obstacles, 2 interactables.
- `PLAY/model/adanna_m1_uv_validation.json`: 33/33 local checks passed. Scope: GLB binary/accessor integrity, UV0 range and all 8 atlas patches, embedded PNG, preserved skin/clips, material texture reference, atlas/layout images, collision OBJ reopen, import manifest, macOS helper/runbook presence, 2 m humanoid envelope and pendant placement. It is **not** an Unreal import/compile/PIE/cook/package test.
- Browser live preview process: `PORT=8001 node server.mjs` from `web_build/`, bound to `0.0.0.0`.

## Preserved outputs

- `TDD_PHASE3_PRODUCTION/HALL_OF_POSTS_M1/` — unchanged. Current M1 classification and outstanding approval dependencies retained.
- `PHASE_2_SUCCESSOR_HANDOVER.md`, `TDD_PHASE2_PRODUCTION_READINESS_AUDIT_v1/`, `OUR_EYES_CD_FINAL_VERDICTS_v1/`, `CONTINUATION_MAP.md`, `PHASE_2_PROGRESS.md` — retained; progress updated with this playable milestone.
- Phase 1 restrictions: V003 BACK/LEFT_SIDE unapproved, V013 item 5 not done, H3 visual-release restriction, CQ-9/SCN028/SCN030/E53/E54, external-authority restrictions, rejected/superseded/failed/limited-study assets all remain controlling.

## Current dependencies / blockers

1. **UE verification blocker:** the engine version and machine are now known (UE 5.8, M4 macOS 27.2.1, 16 GB), but this sandbox has no Unreal binary and no access to the Mac, so compile, `.umap` creation, import, PIE, cook, package and launch are unexecuted. Execution steps: `PLAY/ue_project/README_MACOS_UE58.md`. Helper: `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py`. Access/evidence request: root `OWNER_STUDIO_UNREAL_REQUEST.md`.
2. **Automated browser rendering blocker:** no browser binary/Playwright/Selenium/Puppeteer in sandbox. The static/live build is verified by HTTP/module/asset checks and a live preview is exposed to the user's browser; WebGL visual rendering is not automatically screenshot-verified here.
3. **Adanna final-asset blocker:** CD/Research authority is needed for final turnaround, exact dimensions, hair/groom, costume technical interpretation, facial rig and production topology/UVs/materials. Restricted views cannot be inferred.
4. **Forest final-production blocker:** CD film/game canon, consultant review, shared spatial/metric/camera interpretation, botanical species check and final landmark approval remain outstanding. Exploratory boards are reference only.
5. **Commercial standards remaining:** final modelling/sculpting, retopology/UVs, PBR textures, rig/skin weights, animation set, world composition, navigation, lighting, performance profiling, versioned binary assets and reproducible UE packaging.

## Exact next action

On the M4 Mac, in this order: (1) confirm `xcodebuild -version` is 26.0–26.3 and record `Build.version`; (2) compile with `Engine/Build/BatchFiles/Mac/Build.sh TDD_GAMEEditor Mac Development -project=<repo>/.../TDD_GAME.uproject -architecture=arm64`; (3) run `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py` in the Editor Python console to create and save `/Game/TDD/Maps/PLAYABLE_FOREST_M1.umap`, repoint the map config and import the technical handoff; (4) verify the GLB arrives as a **Skeletal Mesh** with 21 bones and 5 sequences; (5) PIE-check movement, camera, collision, interaction and route; (6) cook, package a Mac arm64 `.app`, launch it, and record everything into `ue_project/Saved/TDD_M1/Evidence/`. Then obtain the CD/Research approvals and replace the labelled proxy with approved production assets. **Do not claim full M1 completion, a final commercial character, UE real-time integration or a UE packaged build until those gates actually pass and are recorded.**

## Production sequence retained

- **M1 (current priority):** first playable Adanna in playable Forbidden Forest — technical real-time integration proof delivered; full production acceptance pending.
- **M2:** approved game-ready character/environment production quality; final topology/UVs/materials, groom/clothing, rig/animation, environment kit, collision/navigation and performance pass.
- **M3:** gameplay foundation — interaction, traversal, basic combat, enemy behaviour, UI and audio.
- **M4:** first vertical slice — objective, exploration, combat, encounter resolution and save/load foundation.
