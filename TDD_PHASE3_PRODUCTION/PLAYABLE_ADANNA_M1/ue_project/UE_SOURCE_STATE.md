# UE SOURCE STATE — Playable Adanna M1

**Classification:** new provisional runtime-procedural Unreal source state, not a recovered existing project, not a compiled/cooked/packaged build, and not a verified UE real-time integration test.

**Date:** 2026-11-19  
**Recovered engine project/version:** none. Targeted recovery found no `.uproject`, `.uasset`, `.umap`, engine binary, version record, native character mesh, skeleton/rig, animation, gameplay system, Forbidden Forest 3D asset/layout or packaged build.  
**`EngineAssociation`:** `5.4` provisional only. It is a source-file placeholder until the owner/studio supplies the actual UE version and hardware profile. Do not report it as the recovered project version.

## What exists

| Path | Purpose |
| --- | --- |
| `TDD_GAME.uproject` | Minimal runtime module project descriptor. |
| `Config/DefaultEngine.ini` | Default game mode, renderer and gravity settings. |
| `Config/DefaultInput.ini` | Legacy axis/action mappings: movement, look, jump, sprint, interact. |
| `Config/DefaultGame.ini` | Project identity/version metadata. |
| `Source/TDD_GAME.Target.cs`, `Source/TDD_GAMEEditor.Target.cs` | Game and editor target rules. |
| `Source/TDD_GAME/TDD_GAME.Build.cs` | Runtime module dependencies: Core, CoreUObject, Engine, InputCore. |
| `Source/TDD_GAME/TDD_GAME.cpp`, `TDD_GAME.h` | Primary game module. |
| `Source/TDD_GAME/TDDForbiddenForestGameMode.h/.cpp` | Spawns the runtime Forbidden Forest level and sets the proxy pawn. |
| `Source/TDD_GAME/TDDAdannaProxyCharacter.h/.cpp` | `ACharacter` technical proxy: capsule collision, CharacterMovement walking/running/jump/landing, camera boom with collision test, interaction, route HUD, and rigid-part locomotion. |
| `Source/TDD_GAME/TDDForbiddenForestLevel.h/.cpp` | Runtime instanced-static-mesh Forbidden Forest blockout: ground, laterite path, trunks, buttress roots, canopy, rocks, understory, white cloth, boundary posts, pots, interaction rings and Great Root Mother. |
| `Source/TDD_GAME/TDDWorldData.h` | Generated from the shared `../world.json`; regenerate with `python3 ../scripts/generate_ue_world_data.py`. Contains 7 waypoints, 46 obstacles and 2 interactables. |
| `Tools/TDD_M1_Unreal_Setup_macOS.py` | **PRODUCED — NOT YET VERIFIED** owner-side macOS/UE 5.8 helper. Records engine/host facts, creates and saves `/Game/TDD/Maps/PLAYABLE_FOREST_M1` from a template, repoints `GameDefaultMap`/`EditorStartupMap` after backing up the config, imports the three labelled technical files, writes `Saved/TDD_M1/tdd_m1_setup_report.json`. Never overwrites an existing map or asset. It does not verify compile, PIE, cook or package. |
| `Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py` | Preserved original helper for audit. Do not execute: uses removed `EditorLevelLibrary`, leaves no saved `.umap`, never loads the project map. |
| `Tools/tdd_m1_macos_audit.json` | **COMPLETED AND VERIFIED** static compatibility audit for macOS/UE 5.8: engine and build-setting alignment, no Windows-only tokens, INI section correctness, UHT include order, `TObjectPtr` usage, no invented blade geometry. Static inspection only. |
| `README_MACOS_UE58.md` | Exact macOS command sequence: verify toolchain, compile, run the helper, import checks, PIE, cook, package, launch, evidence naming. |
| `../model/adanna_m1_ue_import_manifest.json` | **COMPLETED AND VERIFIED** local technical import handoff: UV GLB, atlas, material slots, collision proxy, scale/axis notes and explicit owner/Creative Director blockers. |

## Shared-world alignment

`../scripts/generate_ue_world_data.py` compiles the browser/Node `world.json` into `TDDWorldData.h`. This is deliberate: the UE runtime source, browser `game.js` simulation, Node integration test and CPU replay captures all refer to the same gameplay/collision route. It avoids a second invented level layout. The generated header is a C++ source artefact, not an Unreal JSON asset and not an imported `.uasset`.

## What is deliberately not claimed

- No `.uasset`, `.umap`, imported GLB, SkeletalMesh, AnimSequence, Animation Blueprint, NavMesh, lighting build, cooked content or packaged build exists here.
- No compile, editor launch, PIE, cook, package or device test was run: this sandbox has no Unreal binary and no access to the owner's Mac. The owner environment is known (M4 / 16 GB / macOS 27.2.1 / UE 5.8) but has not executed this project yet.
- The UE character is a **RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER**. It uses runtime primitive parts and procedural limb motion, not the skinned 21-joint browser GLB and not an approved final Adanna model.
- The forest is a gameplay/collision blockout of Art Bible/approved-source rules and the shared PROPOSED route. It is not final environment art, canon geography, botanical sign-off or final lighting.
- `/Engine/Maps/Entry` is the current default map and is temporary. `Tools/TDD_M1_Unreal_Setup_macOS.py` creates and saves the project-owned `/Game/TDD/Maps/PLAYABLE_FOREST_M1.umap` and only then repoints `GameDefaultMap`/`EditorStartupMap`.

## Target environment

**Owner baseline:** Apple M4 Mac, 16 GB RAM, macOS 27.2.1, ARM64, Unreal Engine 5.8. `EngineAssociation` is `5.8`; both targets use `BuildSettingsVersion.V7` and `EngineIncludeOrderVersion.Unreal5_8`. No Windows target is assumed and no Windows-only tokens remain in the project files.

Toolchain requirement: Xcode 26.0 minimum, 26.1.1 recommended; **Xcode 26.4 is not compatible with Unreal Engine**. Metal 1.2 class GPU required and satisfied by M4.

## Owner/studio verification sequence

1. Verify the installed engine and Xcode versions against `README_MACOS_UE58.md` section 0.
2. Compile the `TDD_GAME` module with `Engine/Build/BatchFiles/Mac/Build.sh TDD_GAMEEditor Mac Development -project=... -architecture=arm64`.
3. Run `Tools/TDD_M1_Unreal_Setup_macOS.py` inside the Editor: it creates and saves the project-owned `.umap`, repoints the map config and imports the handoff. Confirm `ATDDForbiddenForestGameMode` spawns the runtime forest and proxy pawn.
4. Verify movement, run/turn/jump/land, camera collision, obstacle collision, ground detection, interaction and route progress in PIE.
5. Import the labelled browser GLB/rig or replace it with an approved production Adanna asset; import a production forest kit; add navigation/lighting/performance work.
6. Only then run cook/package and record device-level real-time integration results.

## Required status classification

| Deliverable | Status |
| --- | --- |
| UE source scaffold, Config, Targets, Build.cs and C++ classes | **PRODUCED — NOT YET VERIFIED** |
| `TDDWorldData.h` generated from shared `world.json` | **COMPLETED AND VERIFIED** |
| `Tools/TDD_M1_Unreal_Setup_macOS.py` owner-side map/import helper | **PRODUCED — NOT YET VERIFIED** |
| macOS/UE 5.8 static compatibility audit (69 checks) | **COMPLETED AND VERIFIED** (static inspection only) |
| Browser/Node shared gameplay and replay captures | **TECHNICALLY DEMONSTRATED — NOT INTEGRATED** |
| Adanna UV/material/collision import handoff | **PROVISIONAL — AWAITING CREATIVE APPROVAL** |
| Project-owned `.umap`, import, compile, PIE, cook, package and runnable build | **BLOCKED — OWNER-STUDIO DEPENDENCY** |
| Final Adanna and Forbidden Forest production assets | **BLOCKED — CREATIVE APPROVAL** |
| M3/M4 gameplay | **NOT STARTED** |

Fix any compile/runtime errors from that verification in this source tree. Until then, the browser live preview and deterministic simulation/capture outputs are the only executed real-time integration evidence.
