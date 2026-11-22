# PLAYABLE MILESTONE REPORT — concise handover

**Date:** 2026-11-20  
**Branch:** `arena/8efaa23f-tdd`  
**Status:** directly launchable real-time gameplay integration proof delivered; **full production/commercial M1 is not complete**.  
**Classification:** `RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER`; Forbidden Forest is a neutral gameplay/collision blockout, not final art or canon.  
**Owner target:** Apple M4 Mac · 16 GB · macOS 27.2.1 · ARM64 · **Unreal Engine 5.8**. No Windows target.  
**Runbook:** `PLAY/ue_project/README_MACOS_UE58.md`  
**Path key:** `PLAY = TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1` relative to repository root.

## Completed work

1. **Targeted game-state recovery retained.** No existing Unreal project/version, playable project, native Adanna mesh, skeleton/rig/animation, gameplay system, Forbidden Forest 3D asset/layout, packaged build or UE integration test was recovered. Hall of Posts M1 and all Phase 1 restrictions remain unchanged and authoritative. See `PLAY/source_authority.json` and `PLAYABLE_MILESTONE_TRACKER.md`.
2. **Shared playable world and assets generated.** `PLAY/world.json` and `PLAY/web_build/world.json` define 7 route waypoints, 46 collision obstacles, 2 interactables and the spawn/camera/gameplay constants. Generated GLB/OBJ assets: `PLAY/model/forbidden_forest_m1.glb/.obj`, `PLAY/model/adanna_m1_technical_proxy.glb/.obj`, `PLAY/model/adanna_m1_character_rig.json`, `PLAY/model/modules/*.glb`, `PLAY/materials.json`, `PLAY/ASSET_REOPEN_REPORT.json`.
3. **Rigged technical Adanna proxy.** Browser GLB has 1 skin, 21 joints and `idle/walk/run/jump/land` clips; 870 vertices / 1,584 triangles. Identity markers derive only from the approved Adanna master reference. Source: `PLAY/scripts/gltf_skin.py`; metadata: `PLAY/production_manifest.json`.
4. **Shared real-time simulation.** `PLAY/web_build/game.js` runs in browser and Node. It implements third-person camera-relative movement, walk/run/turn, jump/land, ground/obstacle collision, camera boom occlusion, interaction, route progress and HUD state.
5. **Directly launchable browser build.** `PLAY/web_build/index.html`, `main.js`, `styles.css`, `server.mjs`, `package.json`, local vendored Three.js 0.187.0 (`vendor/three.module.js`, `vendor/three.core.js`, `vendor/jsm/...`), and local GLB assets. Start with `cd PLAY/web_build && npm run serve` (`PORT=8001 node server.mjs` is currently running for Arena live preview on `0.0.0.0:8001`). No CDN dependency.
6. **Provisional Unreal source state.** `PLAY/ue_project/TDD_GAME.uproject`, Config, Targets, Build.cs and C++ runtime classes for a procedural Forbidden Forest level, game mode and technical proxy character. `PLAY/ue_project/Source/TDD_GAME/Public/TDDWorldData.h` is generated from the same `world.json` by `PLAY/scripts/generate_ue_world_data.py`. Read `PLAY/ue_project/UE_SOURCE_STATE.md` before treating this as a project.
7. **Real-time integration tests executed.** `PLAY/web_build/test/integration_test.mjs` passed 11/11 checks at 60 Hz and wrote 120 replay frames at 15 fps. `PLAY/web_build/test/live_build_verification.mjs` verified live HTTP delivery, recursive local ES-module resolution, JSON/GLB integrity, capture presence and UE source-file presence. Reports: `PLAY/web_build/test/integration_report.json`, `replay_frames.json`, `live_build_report.json`.
8. **Moving visual proof from actual simulation states.** `PLAY/scripts/render_replay.py` executed successfully: 120 PNG frames, `playable_replay.gif`, `playable_replay.mp4`, hero/HUD stills, `playable_contact_sheet.png`, `PLAYABLE_M1_REVIEW_SHEET.png`, `capture_manifest.json` under `PLAY/web_build/captures/`. These are not Blender renders, GLB viewer screenshots or static concept images.
9. **Durable records.** Root `PLAYABLE_MILESTONE_TRACKER.md`, root `PHASE_2_PROGRESS.md`, this report, `PLAY/production_manifest.json` and `PLAY/ue_project/UE_SOURCE_STATE.md` record state, classification, decisions, blockers and next action.

10. **Current independent production cycle — Adanna technical import handoff.** `PLAY/scripts/build_adanna_uv_handoff.py` produced `PLAY/model/adanna_m1_technical_proxy_uv.glb` with face-corner UV0 and an embedded 8-slot provisional material atlas while preserving the original GLB, 21-joint skin and five clips. Also produced `adanna_m1_uv_atlas.png`, `adanna_m1_uv_layout.png`, `adanna_m1_collision_proxy.obj`, `adanna_m1_ue_import_manifest.json` and `adanna_m1_uv_validation.json`; review copies are under `PLAY/web_build/captures/`. Root `OWNER_STUDIO_UNREAL_REQUEST.md` contains the exact owner information/access request. `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup.py` is a source-only owner-side Editor helper for engine-version capture, project-owned `.umap` creation/save and labelled technical import attempts; it has not been executed because no UE binary exists here. Status: **COMPLETED AND VERIFIED** for local file/GLB validation; **PROVISIONAL — AWAITING CREATIVE APPROVAL**; UE integration remains **BLOCKED — OWNER-STUDIO DEPENDENCY**.

11a. **Same compile, next blocker: three Clang `-Werror` loops.** With the shared environment
fixed, compilation started and failed at `TDDForbiddenForestLevel.cpp:209`,
`TDDForbiddenForestGameMode.cpp:18`, `TDDAdannaProxyCharacter.cpp:192` — all
`loop will run at most once (loop increment never executed) [-Werror,-Wunreachable-code-loop-increment]`.
Each loop set a flag (or took the actor) then `break`-ed immediately, so `++It` could never run.
The iterator is positioned on the first match by its constructor, so the loop was never needed.
Replaced with `static_cast<bool>(TActorIterator<T>(World))` for pure presence tests and
`if (TActorIterator<T> It(World); It)` where the actor is used. Zero-, one- and many-actor cases
behave as before. No suppression, no `-Werror` change. Audit gained an unreachable-increment
detector plus anti-suppression checks (**113/113**, negative controls verified).

11. **First owner-machine compile — UBT rejected the target rules (2026-11-19).** No C++ was
compiled. UBT stopped with `TDD_GAMEEditor modifies the values of properties:
[UndefinedIdentifierWarningLevel: Off != Error, UnreachableCodeWarningLevel: Off != Error,
ReturnTypeWarningLevel: Off != Error, DanglingWarningLevel: Off != Error] ... has build products
in common with UnrealEditor`. Cause: `Source/TDD_GAMEEditorTarget.cs` carried the V7/Unreal5_8 edit
but does not match UBT's `*.Target.cs` pattern, so it was never loaded; the live
`Source/TDD_GAMEEditor.Target.cs` still held `V5`/`Unreal5_4`. V5 leaves those four warning levels
`Off` while the engine's shared environment builds them `Error`. Fixed by `V7`/`Unreal5_8` in both
live targets, deleting the dead file, and fixing the audit and live verifier that had certified the
dead copy. `BuildEnvironment = Unique` was rejected as the fix: an installed engine refuses it.
Audit **113/113** with negative controls. No compile has been proven.

12. **Earlier work cycle — macOS / UE 5.8 retarget and scaffold repair.** The owner environment is known, so the scaffold was retargeted and machine-audited instead of assumed compatible. `EngineAssociation` → `5.8`, `BuildSettingsVersion.V7`, `EngineIncludeOrderVersion.Unreal5_8`, `TargetPlatforms: ["Mac"]`, `PythonScriptPlugin` enabled. Ten defects were found and fixed, including one that would have silently prevented the game mode ever applying (map/game-mode keys under a section UE ignores), instanced-mesh pools registered too late to build collision, a missing `APlayerStart`, removed `EditorLevelLibrary` calls in the setup helper, an invented steel blade contradicting Phase 1 restrictions, and a pendant transform that displaced geometry 1.3 m outside the body. New: `ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py` (original preserved for audit), `ue_project/README_MACOS_UE58.md`, and `scripts/audit_ue_macos.py` → **113/113** static compatibility checks.

## macOS / UE 5.8 compatibility findings

- **Version requirement:** the project now requires UE **5.8** (`EngineAssociation`), with `BuildSettingsVersion.V7` and `EngineIncludeOrderVersion.Unreal5_8`. Earlier V5/`Unreal5_4` settings against a 5.8 install would trigger an upgrade prompt or stale-include-order build.
- **Toolchain:** Xcode **26.0 minimum, 26.1.1 recommended**; **Xcode 26.4 is not compatible with Unreal Engine**. macOS SDK via `xcrun`, Metal 1.2 class GPU (M4 satisfies).
- **macOS project support:** no Windows-only modules, paths or binaries remain; `Build.cs` depends only on `Core`, `CoreUObject`, `Engine`, `InputCore`. `Mac` is the only declared target platform.
- **Plugins required:** `PythonScriptPlugin` (enabled in the `.uproject`), plus the default `Interchange Framework` and `Editor Scripting Utilities` used by the import helper.
- **Not verified:** whether it actually compiles, imports, plays, cooks or packages on the M4. Static inspection only.

## Verification summary

- Node shared-simulation integration: **11/11 checks passed**; camera collision, movement, jump/land, interaction, route and obstacle collision covered.
- Live/static browser-build verification: **67/67 checks passed**; recursive local ES-module graph resolved, no external CDN script, local GLBs valid, captures present, UE source files and durable records present.
- Live server: `node server.mjs`, `0.0.0.0:8001` in the current sandbox; Hall of Posts review remains on `0.0.0.0:8000`.
- Adanna technical import handoff: **33/33 local checks passed** (`PLAY/model/adanna_m1_uv_validation.json`); the UV GLB was also reopened in Trimesh with 4,752 face-corner vertices / 1,584 triangles. This validates local files only.
- **Not verified:** automated WebGL rendering in a headless browser, UE compile, UE PIE/cook/package, device performance, final asset import, final topology/UVs/materials/groom/facial rig, or final navigation/lighting.

## Remaining work

- Supply the exact UE installation/version, hardware profile and execution access in root `OWNER_STUDIO_UNREAL_REQUEST.md`; retarget `EngineAssociation`, generate project files, compile `TDD_GAME`, run the owner-side `Tools/TDD_M1_Unreal_Setup.py` in the Editor to create/save a project-owned `.umap` and attempt labelled imports, verify PIE movement/camera/collision/interaction/route, then cook/package.
- Replace the technical proxy with an approved, production-quality Adanna: final sculpt/retopology/UVs, calibrated materials/textures, hair/groom, clothing, skeleton/skin weights, animation set, facial rig and optimisation.
- Convert forest blockout into production environment kit and final level: approved geography/canon, landmarks, botanical sign-off, collision/navigation, world composition, lighting/atmosphere and performance profiling.
- Build M3 gameplay foundation (interaction depth, traversal, basic combat, enemy behaviour, UI, audio) and M4 vertical slice (objective, exploration, combat, encounter resolution, save/load foundation).
- Perform reproducible owner-hardware build, versioned binary asset management and device-level integration testing.

## Dependencies / blockers

1. No UE binary, recovered engine version or owner-studio hardware/licence profile in sandbox; UE real-time and package claims are blocked. The exact request is `OWNER_STUDIO_UNREAL_REQUEST.md`; the owner-side setup script is `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup.py` and remains unexecuted.
2. No browser binary/headless automation in sandbox; live preview is available to the user's browser, but automated WebGL screenshot verification is not.
3. CD/Research authority needed for final Adanna turnaround, dimensions, hair/groom, costume technical interpretation and facial rig. V003 BACK/LEFT_SIDE and other Phase 1 restrictions remain unapproved.
4. CD film/game canon, consultant review, shared Forbidden Forest spatial/metric/camera interpretation, botanical check and final landmark approval remain outstanding. Exploratory boards are reference only.
5. No creative/approval/canon/gate change, remote write, rejected-asset promotion or unapproved design invention was made.

## Exact next action

Open the live preview on port 8001 and visually confirm browser WebGL play. Then, on owner/studio hardware, compile the provisional UE source against the supplied UE version, run `PLAY/ue_project/Tools/TDD_M1_Unreal_Setup.py` inside the Editor to capture engine facts and create/save the project map, verify PIE, and only after successful execution replace the labelled proxies with approved production assets and record cook/package results. Until then, call this a **playable technical integration milestone toward M1**, not a completed final commercial first-playable milestone.
