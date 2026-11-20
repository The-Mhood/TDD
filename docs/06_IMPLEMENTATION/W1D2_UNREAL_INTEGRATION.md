# W1 D2 — Unreal Integration Start

**Date:** 2026-11-20 UTC
**Branch:** `arena/553fb02d-tdd`
**Status:** source integration started; engine build/PIE not available in the Linux agent sandbox.
**Non-goal:** replace or rewrite any W1 D1 pure-core contracts.

## What is now connected in source

### Player movement, state and camera

- `ATDDAdannaCharacter` now owns `UTDDCharacterStateComponent` and `UTDDCombatComponent`.
- A thin state adapter wraps the existing `FTDDPureStateMachine`, publishes state changes and observes `UCharacterMovementComponent::IsFalling()` for Airborne/Land events.
- The CMC receives the pure gait values (Walk: 220 cm/s, 1200 cm/s² acceleration, 1800 cm/s² braking, 450°/s turn; jump: 500 cm/s; gravity scale adapted to 1500 cm/s² against UE's nominal 980 cm/s²).
- Existing spring-arm/follow-camera ownership is unchanged. Legacy input now maps movement/look, jump, sprint, light attack and guard for keyboard/mouse and gamepad.
- Traversal execution is **not yet integrated**: the D1 two-phase fallback remains a pure contract; obstacle detection, capsule-safe vault/drop execution and E1–E7 PIE evidence are still M2 work.
- Two integration blockers exposed by connecting the runtime state path were fixed additively: grounded physics must permit `Airborne -> Land`, and releasing Block must permit Idle/Locomotion/Sprint. The 196-pair state matrix was updated and explicit tests added.

### Combat/damage actors

- `UTDDCombatComponent` traces a light attack against `ECC_Pawn`, applies the D1 `EvaluateDamage` result to actor health/posture, and routes Dead/Stagger to the owner's state authority.
- Guard uses the D1 0.08 s guard-ready / 0.15 s parry windows. A successful parry negates the incoming hit and forces Stagger on the attacker; a held guard applies explicitly provisional chip damage (20% health, 50% posture).
- The component forwards boss health/posture-break events to an attached `UTDDBossPhaseComponent`.
- The temporary integration tuning is deliberately exposed as component properties; it is not a signed-off combat balance pass or animation implementation.

### AI and boss data

- `UTDDCombatDirectorSubsystem` adapts `FTDDAttackTokenPolicy` to the world. `UTDDCombatBrainComponent` registers training enemies, tracks the player, closes distance, and requests attacks through the concurrency-limited director.
- `ATDDTrainingEnemy` is an explicitly labelled greybox/test actor using the shared state and combat components; it is not a production enemy archetype.
- `UTDDBossPhaseGraphAsset` and `UTDDBossPhaseComponent` adapt editable Unreal data to the existing pure graph validator/selector. Runtime inputs include health, poise break, elapsed time, distance, player ability, memories and events.
- Added `TDD.W1D2.AI.BossPhaseAssetAdapter` to the Unreal automation suite. `Tools/unreal/create_root_mother_phase_asset.py` creates a separate Great Root Mother data asset after the module builds; no boss-specific controller branch is introduced.

### Adanna and Chapter 1

- Player class now has an editor-assignable soft skeletal-mesh property. `Tools/unreal/import_adanna_proxy.py` checks the source GLB against the handoff SHA-256, imports to a new technical-only content folder, and attempts separate player/GameMode Blueprint children. It refuses asset overwrites and reports failure rather than silently passing.
- `Tools/unreal/build_chapter1_greybox.py` creates a new `/Game/Maps/Ch01_Greybox` from the committed seven-point route and neutral M1 world data: floor, connected route strips, 46 primitive obstacles, 2 markers, PlayerStart and training enemy. It refuses to overwrite an existing map and updates startup-map config only when actually run in the editor.
- `Tools/tools/validate_chapter1_greybox_source.py` verifies the input data and script hooks offline. It does not claim that a UMAP was created.

### Build and regression pipeline

- Windows CI now refuses a non-Windows shell, dirty tree, wrong branch or stale checkout; it no longer checks out another branch or uses `reset --hard`.
- Added a Windows-CI branch-safety contract check to the daily train and Windows job.
- Static project-readiness checks pass on the Linux sandbox for both Mac and Windows configurations. These are descriptor/preflight checks, not C++ compilation.

## How to run on the owner UE 5.8 machine

1. Build/test the C++ integration first: `Tools/engine/run_daily_train.sh` on the owner Mac. Resolve UHT/UBT or automation failures before opening PIE.
2. In the Editor Python console, run `Tools/unreal/build_chapter1_greybox.py` to create the map. Then run `Tools/unreal/import_adanna_proxy.py` to import and wire the labelled technical proxy. The importer requires a working glTF importer; inspect its JSON report and do not infer success from script completion alone.
3. Run `Tools/unreal/create_root_mother_phase_asset.py` after the module loads. Run Automation filter `TDD` and retain the actual report/log.
4. Open `Ch01_Greybox` in PIE. Record movement stop/acceleration/turn, jump/landing, camera obstruction/recovery, light attack hit/miss, block, parry, stagger/death, and 2+ simultaneous enemies. Capture the map, PIE input sequence, automation report and machine/build identity under `Saved/BuildEvidence/<UTC>/`.
5. On the reference Windows PC, run `Tools/engine/windows_ci.sh arena/553fb02d-tdd` only after that branch is fetched/checked out cleanly. The runner will refuse to synchronize by destructive reset.

## Verification boundary today

**Verified here:** six host-compiled pure suites pass (884 assertions); runner-failure and Windows-CI-safety contracts pass; route input preflight passes (7 points, 69.315 m polyline, 3.4 m path, 46 obstacles, 2 interactables); 9/9 GLBs validate and both manifest-listed Adanna GLBs have verified SHA-256; Mac/Windows project-readiness static checks report 0 blockers/0 warnings; Unreal editor scripts pass Python syntax compilation.

**Not verified here:** any UE C++/UHT build, the new Unreal automation tests, editor Python execution, native GLB import, Blueprint creation, map save, PIE movement/traversal/camera/combat/AI, Mac build, Windows build, cook, or package. This sandbox has no Unreal executable and is Linux, so `mac_build.sh` and `windows_ci.sh` both correctly returned `NOT EXECUTED` with exit code 2. No playable-game or PIE pass is claimed.
