# W1 D2 Integration Traceability

**Snapshot:** 2026-11-20 UTC
**Purpose:** record connected Unreal source and the exact execution boundary. Every UE-dependent row remains `NOT EXECUTED` until owner-platform evidence is attached.

| WS / owner priority | Connected source / deliverable | Verification performed | Still required for acceptance |
|---|---|---|---|
| WS1 — player movement/state/camera/traversal | `ATDDAdannaCharacter` binds walk/run/jump to CMC values from D1; `UTDDCharacterStateComponent` owns the pure state machine and observes CMC falling/landing; existing spring arm/follow camera remains attached. Pure rules now allow `Airborne -> Land` and guard-release exits. | Pure state suite 659/659; enhanced Unreal CDO automation assertions added to `TDD.M1.Player.PlayableCharacterDefaults`; static source readiness passes. | UE compile/UHT; PIE movement/landing/camera obstruction tests. Traversal execution itself is not yet integrated; D1 fallback core remains unchanged and requires M2-level runtime work. |
| WS2 — combat/damage actors | `UTDDCombatComponent` performs a pawn-channel light-attack sweep, applies pure damage outcomes, health/posture, guard chip, parry-to-attacker-stagger and dead/stagger transitions. | Pure combat suite 39/39; Unreal actor/automation source added. | UE compile; real actor hit/miss and block/parry/stagger/death runs in PIE; balance/animation/feedback review. |
| WS3 — AI/boss phases | World token director adapts the pure cap/cooldown/fairness policy; training enemy brain follows player and attacks only when granted; editable boss asset/component bridge to pure selector and damage events. | Pure AI suite 111/111; multi-translation-unit link check passed; `TDD.W1D2.AI.BossPhaseAssetAdapter` added but UE automation not run in this sandbox. | UHT/UBT, automation; 6-enemy functional concurrency test; actual nav/perception/StateTree and boss phase presentation remain future work. |
| WS4 — Adanna integration | Soft-mesh hook on the player class; editor script checks manifest SHA-256, imports technical GLB, and attempts new labelled player/GameMode Blueprint children. | D1 static audit remains 22 nodes/1 skin/5 clips; D2 asset validation 9/9 and 2 manifest hashes; script syntax compiled. | Run glTF importer on UE 5.8; inspect created assets, assign/verify AnimBP or retarget; PIE and creative approval. No native import is claimed. |
| WS5 — Chapter 1 greybox | UE editor script creates a new UMAP from route/world data, with bounds floor, connected route pieces, primitives, markers, PlayerStart and a training enemy. | Offline source preflight: 7 waypoints, 69.315 m path, 3.4 m width, 46 obstacles, 2 interactables; script syntax compiled. | Run editor script, inspect saved UMAP/collision, play end-to-end in PIE; streaming/nav/culture/art criteria remain open. |
| WS6 — build/CI | Windows job checks host, current branch, clean state and exact remote SHA; destructive checkout/reset removed. Daily and Windows trains run runner and CI safety contracts. | Static Mac/Windows readiness: 0 blockers/0 warnings; shell syntax + branch-safety regression pass; Mac and Windows runners correctly return `NOT EXECUTED` on Linux. | Owner Mac UE build/automation; actual Windows PC build/automation; evidence bundles and ledger updates from those machines. |
| WS7 — regression/evidence | Added UE automation coverage for player defaults and boss asset adapter; W1 D2 host evidence bundle, this traceability sheet and integration runbook. | 6 pure suites 884/884; runner contract and Windows safety contract pass; asset and route preflights committed. | Run new Unreal automation and attach logs/captures; no integration milestone is closed until its engine/runtime evidence exists. |

## Host run totals

- `TDD-Pure.TDDAIPureCoreTests`: 111/111
- `TDD-Pure.TDDChapterRouteTests`: 9/9
- `TDD-Pure.TDDCombatMathTests`: 39/39
- `TDD-Pure.TDDMovementCoreTests`: 48/48
- `TDD-Pure.TDDStateMachineTests`: 659/659
- `TDD-Pure.TDDDodgeDistanceMathTests`: 18/18
- **6 suites; 884 assertions; all passed.** The state total is six fewer than D1 because newly legal Airborne/Land and Block-release pairs require fewer refusal assertions in the full matrix; two explicit accepted-transition checks were added.
- `TDD-Tool.PureRunnerContract` and `TDD-Tool.WindowsCISafety` both pass.

Evidence directory: [`evidence/20261120T-W1D2/`](evidence/20261120T-W1D2/). Build readiness and script syntax checks are static, not engine builds.
