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

This row verifies pure-core behavior only. It does **not** certify M1/M2/M3 milestone exit, a playable Unreal build, or the Chapter 1 release candidate.

## Evidence and change-control rules

1. Every daily train stores unedited `TDD_RESULT` lines and build/automation output under `Saved/BuildEvidence/<UTC>/` (owner machine) or the committed, scoped sandbox evidence directory.
2. A test that fails to compile is a failure, not a skip. A missing platform/toolchain is `NOT EXECUTED`, never `PASS`.
3. A milestone AC is complete only when its named measurement and committed evidence exist. Pure-core tests are supporting evidence when an AC also requires Unreal/runtime conditions.
4. Defects and blockers are tracked in [`DEFECT_REGISTER.md`](DEFECT_REGISTER.md). AC-to-evidence mapping is in [`AC_TRACEABILITY_W1D1.md`](AC_TRACEABILITY_W1D1.md).
5. The append-only row generator is `Tools/engine/ledger_update.py`; the owner daily train is `Tools/engine/run_daily_train.sh`.
