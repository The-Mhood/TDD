# Defect Register — W1 D1 Baseline

**Document ID:** TDD-IMPL-DEFECTS-001  
**Snapshot date:** 2026-11-20 UTC  
**Scope:** confirmed implementation/tool defects and verification blockers. Not a claim that the full project has no defects.

## Open confirmed defects

| ID | Severity | Area | Description | Owner | State | Closure evidence |
|---|---|---|---|---|---|---|
| — | — | — | No confirmed open defects recorded in the W1 D1 sandbox slice. | — | — | — |

## Resolved during W1 D1

| ID | Area | Finding | Resolution | Evidence |
|---|---|---|---|---|
| D-W1-001 | GLB manifest validator | `validate_glb.py` only searched for literal filenames in hash-map keys, while the Adanna handoff manifest stores semantic aliases in `files` and matching digests under `sha256`; reports therefore said “not listed” despite a correct digest being present. | Resolve alias → asset path → matching digest; unlisted assets now fail an explicitly requested manifest check. | `Tools/tools/validate_glb.py`; source and UV GLB SHA-256 checks in `evidence/20261120T-W1D1/asset-validation-final.jsonl`. |
| D-W1-002 | AI token policy draft | Initial draft referenced an undefined grant-count array and did not size per-roster counts. | Replaced with policy-owned roster, initialized count vector in `SetRoster`, and added TTL/cooldown/reset tests. | `TDDAIPureCoreTests` 108/108 (including closed-cycle and invalid-weight cases). |
| D-W1-003 | Pure test runner | A piped `while` loop ran in a subshell, so compile/runtime failures could be printed while the runner returned success; the documented `--evidence-dir` argument was also ignored. | Keep the suite loop in the current shell, parse the evidence argument, and add a fake-compiler regression contract invoked by the daily train. | `TDD-Tool.PureRunnerContract PASS`; deliberately failed all six compiles and verified runner exit was non-zero. |

## Verification blockers (not product defects)

| ID | Blocker | Impact | Required action | State |
|---|---|---|---|---|
| B-W1-001 | Unreal Engine and owner-platform hardware are absent from the agent sandbox. | UE C++ wrappers, Mac build/automation, Windows CI, PIE/cook/package and runtime acceptance cannot be claimed here. | Run `Tools/engine/run_daily_train.sh` on owner Mac; start reference-PC CI in W2; append actual evidence to the ledger. | Open / owner-platform dependent |
| B-W1-002 | Adanna GLB is a technical proxy pending creative approval; native UE import is not verified. | Static skeleton/clip audit is not production character approval or Unreal integration evidence. | Follow the handoff manifest/runbook and record creative approval plus owner UE import/build evidence. | Open / approval + owner-platform dependent |
| B-W1-003 | Chapter 1 route data currently represents a neutral M1 blockout fixture, not a project-owned Unreal map or final level. | Route validation does not prove streaming, navigation, traversal, art/cultural sign-off, or full chapter completeness. | Integrate in the owner Unreal project and execute M2/chapter acceptance checks when those workstreams are scheduled. | Open / future integration |

Severity convention for subsequent entries: P0 = release blocker/data loss; P1 = major core path broken; P2 = significant but bounded; P3 = minor. Never convert a missing measurement into a zero-defect claim.
