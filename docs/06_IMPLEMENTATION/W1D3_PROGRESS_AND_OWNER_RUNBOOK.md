# W1 D3 Progress and Owner-Platform Runbook

**Date:** 2026-11-20 UTC
**Branch:** `arena/553fb02d-tdd`
**Status:** source integration advanced; pure/source checks pass; Unreal build, Editor, import, map generation and PIE remain **NOT EXECUTED** in this Linux sandbox.

## Assertion-count investigation

The reported D1-to-D2 change is explained by the test sources; it is not a missing suite or removed test file:

| Suite | W1 D1 | W1 D2 | Source-level reason |
|---|---:|---:|---|
| `TDDAIPureCoreTests` | 108 | 111 | D2 added three token-roster synchronization assertions. |
| `TDDStateMachineTests` | 665 | 659 | D2 made four additional state pairs legal (Airborne→Land plus three Block exits). In the exhaustive 14×14 matrix, each changed pair goes from three refusal/state-preservation assertions to one successful-transition assertion: −8. Two explicit event-transition assertions were added: +2. Net −6. |
| Other four suites | 114 | 114 | No assertion-count change. |
| **Total** | **887** | **884** | **+3 AI −6 state = −3.** |

The complete 196-pair state matrix remains exercised. The count reduction is the expected consequence of checking newly permitted transitions as success rather than refusal plus two invariants; it is not lost coverage. D3 additionally permits `Traversal→Airborne` for the Character Movement takeoff event, adds one semantic assertion, and changes one matrix case from three refusal checks to one accepted transition. The current pure total is therefore **883** (AI 111; route 9; combat 39; movement 48; state 658; dodge 18), not evidence that a test suite disappeared.

## D3 implementation progress

- Added `UTDDTraversalComponent` with forward obstacle, overhead clearance, landing-floor and capsule-path probes; it uses the existing pure two-phase fallback and starts motion through `LaunchCharacter`.
- Attached traversal to `ATDDAdannaCharacter`, bound **E** and Gamepad **Y** to `Traverse`, and extended the playable-character automation source to require the component.
- Corrected the traversal arc to match the checked vault launch and changed controlled drops to solve the measured fall-time/horizontal-speed pair. All route/state/launch checks now precede the authoritative Traversal state write.
- Added the traversal takeoff edge to the state rules and its exhaustive matrix/semantic checks. CMC remains the authority for airborne and landing transitions.
- Added a training boss actor with the boss phase component; damage is rejected during a graph phase marked invulnerable, and death disables character movement/input. The Chapter 1 generator now includes a vault obstacle, a measured 1 m stream drop fixture, a training enemy, and the phase-graph boss when native classes/assets exist.
- `Tools/tools/validate_chapter1_greybox_source.py` and the Python sources pass syntax/source preflight. These checks do not execute Unreal.

## Verification performed here

- Pure C++: **6/6 suites, 883/883 assertions passed**.
- Runner contract and Windows CI safety checks passed.
- Chapter 1 source preflight passed: 7 waypoints, 69.315 m route, 3.4 m width, 46 obstacles, 2 interactables; `unreal_map_created=false`.
- Captured outputs: `docs/06_IMPLEMENTATION/evidence/20261120T-W1D3/` (`pure-run.txt`, runner/CI contracts, source-preflight JSON, and diff check).
- **No** UnrealHeaderTool/UnrealBuildTool compile, Editor launch, automation execution, native import, UMAP creation, PIE, package, or platform build occurred. Do not treat the above as in-engine verification.

## Owner-platform execution and evidence

Run from the project root on the UE 5.8 owner Mac (or the configured reference Windows PC where noted):

1. Record the exact branch/commit and start with a clean tree. Build the project and run the automation train with `Tools/engine/run_daily_train.sh`. Resolve UHT/UBT errors first; preserve the full log and test XML/text output. The Linux host's `NOT EXECUTED` result is not a substitute.
2. In Unreal Editor, run `Tools/unreal/import_adanna_proxy.py` first. Inspect imported mesh, skeleton, all five expected clips, collision/scale/orientation, and the technical Blueprint/GameMode. Confirm the report and manually inspect the asset; keep it explicitly technical/unapproved.
3. Run `Tools/unreal/build_chapter1_greybox.py`. Inspect `Ch01_Greybox` bounds, route continuity, obstacle collision, PlayerStart forward direction, training enemy and boss phase-asset assignment. Save the generated report and a viewport screenshot. The script refuses to overwrite the map; resolve existing asset conflicts deliberately rather than deleting production content.
4. PIE traversal checks: move to the vault fixture and press **E**; verify clear vault, blocked/too-high rejection, safe landing, and no traversal state on rejection. At the stream edge, verify controlled drop reaches the lower floor without clipping. Repeat with keyboard and Gamepad **Y**, capture before/during/after screenshots, and inspect `GetLastResult`/state transitions.
5. PIE locomotion checks: walk, sprint, jump, short/long landings, camera collision, guard/release, attack hit/miss, parry, posture break, stagger and death. Record numeric health/posture/state before and after each interaction; verify dead actors stop moving and the player cannot continue input.
6. Encounter checks: exercise the trainer and phase-test boss in the generated map. Confirm token cap, approach/turn/attack, hit/block/parry reactions, boss graph entry/threshold transitions, invulnerable-phase rejection, defeat/death. Capture logs and encounter video/screenshots; do not infer from source or spawn reports.
7. Run the safe Windows CI helper on the reference PC at the same commit and attach its complete build/automation result. Add actual platform results to `QUALITY_LEDGER.md` and the D3 evidence folder; distinguish failures, skips, and not-run checks.

Until these steps have actual logs and PIE evidence, D3 gameplay remains **PARTIAL / NOT ENGINE-VERIFIED**.
