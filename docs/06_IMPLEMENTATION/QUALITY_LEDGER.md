# Quality Ledger — The Disobedient Daughter

**Document ID:** TDD-IMPL-QUALITY-001  
**Maintained by:** Engineering / daily test train  
**Rule:** append-only for run records; corrections are new rows/notes, never silent rewrites.  
**Status semantics:** `GREEN` means every required step in the named train ran and passed. A pure-only sandbox run is reported as `PARTIAL` and is not an M-gate exit.

## Current verification boundary

The agent sandbox has g++ and Python, but no Unreal Engine installation or owner Mac/Windows hardware. Host-compiled, engine-independent tests and static content checks can be verified here. Unreal compile, automation, PIE, cook, package, input-device parity, performance, and all world/physics-dependent acceptance criteria remain unverified until the daily owner-platform train runs and records evidence.

## Run log

| UTC | Train | Platform | Commit under test | Pure suites | UE automation/build | Status | Evidence |
|---|---|---|---|---:|---|---|---|
| 2026-11-20 | W1 D1 sandbox verification | Linux sandbox / g++ 12.2 | `0f39cbb` | 6/6; 887 assertions | NOT EXECUTED — Unreal unavailable | PARTIAL | `evidence/20261120T-W1D1/` |
| 2026-11-20 | W1 D2 integration-start verification | Linux sandbox / g++ 12.2 | `f7ce9ef` | 6/6; 884 assertions | NOT EXECUTED — Mac/Windows runners returned exit 2 on Linux; static readiness only | PARTIAL | `evidence/20261120T-W1D2/` |
| 2026-11-20 | W1 D8 pure-core + character-asset verification | Linux sandbox / g++ 12.2 + Blender 4.2.23 headless | `ab45856` | 6/6; 883 assertions | NOT EXECUTED — UE runtime absent; V3/V2 FBX independently verified in Blender (skeleton/materials/scale/deformation PASS) | PARTIAL | `evidence/20261120T-W1D8/`; `W1D7_CHARACTER_INTEGRATION_MANIFEST.md`; `VERIFY_INTEGRATION.json` |
| 2026-11-20 | **W1 D8 owner-Mac engine verification (STAGE A — first genuine)** | Owner Mac / UE 5.8.4 | `712ee22` | 6/6; 883 assertions | **Unreal Mac build PASS; 4/4 TDD automation tests PASS, 0 failures; runner + Windows CI safety + ledger regression contracts PASS** | **GREEN** | Owner machine: `Saved/BuildEvidence/20261120T174909Z` |
| 2026-11-20 | W1 D8 owner-Mac engine verification (ninth train) | Owner Mac / UE 5.8.4 | `095629d` | 6/6; 883 assertions | Unreal Mac build FAILED — 20 C++ compile errors (three UE 5.8.4 API/type mistakes); no automation executed | RED | Owner-reported diagnostics; fixes committed `6f66819` |
| 2026-11-20 | W1 D8 owner-Mac engine verification (tenth train) | Owner Mac / UE 5.8.4 | `6f66819` | 6/6; 883 assertions | Unreal Mac build FAILED — 19 C++ compile errors (protected-member access violations in the three M1 test files plus their cascade diagnostics); no automation executed | RED | Owner-reported diagnostics; root-cause accounting + fixes + guards committed; see `DEFECT_REGISTER.md` D-W1D8-011 |
| 2026-11-20 | W1 D8 owner-Mac engine verification (eleventh train) | Owner Mac / UE 5.8.4 | `e3c7eb4` | 6/6; 883 assertions | Unreal Mac build FAILED — 10 C++ compile errors (UE 5.8.4 API signature mistakes in production + tests, and one Unity-build symbol collision); no automation executed | RED | Owner-reported diagnostics; complete root-cause table + fixes + guards committed; see `DEFECT_REGISTER.md` D-W1D8-012 |
| 2026-11-20 | W1 D8 owner-Mac engine verification (twelfth train) | Owner Mac / UE 5.8.4 | `89cdf61` | 6/6; 883 assertions | Unreal Mac build PASS (Editor + game targets); automation FAILED — `TDD.M1.GameMode.EncounterFlow` all 8 assertions false (roster 1→0 as first causal failure; `WorldContext requested with invalid context object.`); pure-core 6/6 PASS; ledger regression 10/10 PASS | RED | Owner-reported diagnostics; root cause = test world never registered with the engine nor initialized for play (canonical `FWorldFixture` pattern now applied + teardown); fix + regression guard committed; see `DEFECT_REGISTER.md` D-W1D8-013 |
| 2026-11-20 | W1 D8 owner-Mac engine verification (thirteenth train) | Owner Mac / UE 5.8.4 | `5a0daaf` | 6/6; 883 assertions | Unreal Mac build FAILED — `fatal error: 'Engine/WorldContext.h' file not found` at `TDDGameModeEncounterTests.cpp:8`; build stopped before automation discovery (0 discovered/0 started/0 completed) | RED | Owner-reported diagnostics; no `Engine/WorldContext.h` header exists in UE 5.8.4 — `FWorldContext` is declared in `Engine/Engine.h` (Epic API reference); invalid include removed, fixture API audit clean, regression guard added; see `DEFECT_REGISTER.md` D-W1D8-014 |
| 2026-11-20 | W1 D8 owner-Mac engine verification (fourteenth train) | Owner Mac / UE 5.8.4 | `76f9c38` | 6/6; 883 assertions | Unreal Mac build PASS (Editor + game targets); automation FAILED — `TDD.M1.GameMode.EncounterFlow` all 8 assertions false (roster 1→0 as first causal failure; `WorldContext requested with invalid context object.`); pure-core 6/6 PASS; ledger regression 10/10 PASS | RED | Owner-reported diagnostics; root cause = `TActorIterator` default `OnlyActiveLevels` flags silently yield zero actors on the `UWorld::CreateWorld` fixture in UE 5.8.4 (level not in the active-collection state the gate requires); production iterators now pass explicit `EActorIteratorFlags::AllActors` (matches documented "every ATDDTrainingEnemy" intent), PlayerStart assertion added, temporary diagnostics in the test, two regression guards; see `DEFECT_REGISTER.md` D-W1D8-015 |
| 2026-11-20 | W1 D8 owner-Mac engine verification (fifteenth train) | Owner Mac / UE 5.8.4 | `79ef5fa` | 6/6; 883 assertions | Unreal Mac build FAILED — `TDDGameModeEncounterTests.cpp:94,96`: `UWorld` has no member `IsActorsInitialized` / `GetPersistentLevel` (temporary D-W1D8-015 diagnostics); both UnrealEditor and UnrealGame builds failed; no automation executed | RED | Owner-reported diagnostics; verified against UE 5.6.1 engine source: correct accessors are `AreActorsInitialized()` and `GetLevel(0)` (`UWorld::PersistentLevel` is private — the proposed direct-member replacement rejected); diagnostics corrected, guards added; see `DEFECT_REGISTER.md` D-W1D8-016 |

This row verifies pure-core behavior only. It does **not** certify M1/M2/M3 milestone exit, a playable Unreal build, or the Chapter 1 release candidate.

## Evidence and change-control rules

1. Every daily train stores unedited `TDD_RESULT` lines and build/automation output under `Saved/BuildEvidence/<UTC>/` (owner machine) or the committed, scoped sandbox evidence directory.
2. A test that fails to compile is a failure, not a skip. A missing platform/toolchain is `NOT EXECUTED`, never `PASS`.
3. A milestone AC is complete only when its named measurement and committed evidence exist. Pure-core tests are supporting evidence when an AC also requires Unreal/runtime conditions.
4. Defects and blockers are tracked in [`DEFECT_REGISTER.md`](DEFECT_REGISTER.md). AC-to-evidence mapping is in [`AC_TRACEABILITY_W1D1.md`](AC_TRACEABILITY_W1D1.md).
5. The append-only row generator is `Tools/engine/ledger_update.py`; the owner daily train is `Tools/engine/run_daily_train.sh`.
