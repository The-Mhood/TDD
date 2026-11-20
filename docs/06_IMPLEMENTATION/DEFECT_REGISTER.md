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
| D-W1-002 | AI token policy draft | Initial draft referenced an undefined grant-count array and did not size per-roster counts. | Replaced with policy-owned roster, initialized count vector in `SetRoster`, preserved absolute-time cooldowns across roster changes, and added edge-case tests. | `TDDAIPureCoreTests` 111/111. |
| D-W1-003 | Pure test runner | A piped `while` loop ran in a subshell, so compile/runtime failures could be printed while the runner returned success; the documented `--evidence-dir` argument was also ignored. | Keep the suite loop in the current shell, parse the evidence argument, and add a fake-compiler regression contract invoked by the daily train. | `TDD-Tool.PureRunnerContract PASS`; deliberately failed all six compiles and verified runner exit was non-zero. |
| D-W1D2-001 | Player state integration contract | Connecting CMC physics exposed that Airborne could not request Land, and Block could not exit on guard release, leaving runtime state stuck in those states. | Add only the two event/interruption edges and expand the exhaustive 14×14 matrix assertions. | `TDDStateMachineTests` 659/659, including direct grounded/guard-release assertions. |

## Resolved during W1 D8 (build defects)

| ID | Area | Finding | Resolution | Evidence |
|---|---|---|---|---|
| D-W1D8-001 | UHT (header tool) | `TDDAdannaCharacter.h:72` — `CharacterMeshAsset` was `BlueprintReadOnly` on a private member without `AllowPrivateAccess`, failing UHT. | Added `meta=(AllowPrivateAccess="true")`, matching adjacent private Blueprint-readable properties; `EditDefaultsOnly, BlueprintReadOnly` contract unchanged. | Owner Mac train 1 (commit `181ccbe`); scan confirmed 0 other private `BlueprintReadOnly` members missing the metadata. |
| D-W1D8-002 | UBT (incomplete-type) | `TDDTrainingEnemy.cpp:29` — `GreyboxVisual->SetupAttachment(GetCapsuleComponent())` used `UCapsuleComponent` with only a forward declaration (missing `Components/CapsuleComponent.h`), failing compilation. | Added `#include "Components/CapsuleComponent.h"` (matching `TDDAdannaCharacter.cpp`). | Owner Mac train 2 (commit `9f36558`); `build_readiness.py` IWYU guard now catches this class pre-UBT. Engine verification pending Mac rerun. |
| D-W1D8-003 | UBT (engine header not found) | `TDDCombatDirectorSubsystem.h:4` — `#include "Subsystems/TickableWorldSubsystem.h"` no longer exists in UE 5.8.4: in 5.8 both `UWorldSubsystem` and `UTickableWorldSubsystem` are defined in `Subsystems/WorldSubsystem.h`; the separate `TickableWorldSubsystem.h` header was removed. | Changed the include to `#include "Subsystems/WorldSubsystem.h"`. Base class `UTickableWorldSubsystem` retained — it is the intended tickable world-scoped subsystem (verified in the official UE 5.8 API docs); no less-capable base used. Tick/GetStatId/IsTickable overrides verified compatible. | Owner Mac train 3 (commit `a57dc67`); `build_readiness.py` engine-subsystem header guard now catches removed engine headers pre-UBT. Engine verification pending Mac rerun. |

## Verification blockers (not product defects)

| ID | Blocker | Impact | Required action | State |
|---|---|---|---|---|
| B-W1-001 | Unreal Engine and owner-platform hardware are absent from the agent sandbox. | UE C++ wrappers, Mac build/automation, Windows CI, PIE/cook/package and runtime acceptance cannot be claimed here. | Run `Tools/engine/run_daily_train.sh` on owner Mac; start reference-PC CI in W2; append actual evidence to the ledger. | Open / owner-platform dependent |
| B-W1-002 | Adanna GLB is a technical proxy pending creative approval; native UE import is not verified. | Static skeleton/clip audit is not production character approval or Unreal integration evidence. | Follow the handoff manifest/runbook and record creative approval plus owner UE import/build evidence. | Open / approval + owner-platform dependent |
| B-W1-003 | Chapter 1 route data currently represents a neutral M1 blockout fixture, not a project-owned Unreal map or final level. | Route validation does not prove streaming, navigation, traversal, art/cultural sign-off, or full chapter completeness. | Run the D2 editor map generator; inspect and verify the saved UMAP in PIE; execute M2/chapter checks later. | Open / editor execution required |
| B-W1D2-001 | New Unreal adapters/components have not been compiled by UHT/UBT. | API/reflection/link compatibility of state, combat, AI, and boss data adapters is unknown until UE build. | Owner Mac `Tools/engine/run_daily_train.sh`; resolve build/automation errors and commit machine evidence. | Open / UE 5.8 required |
| B-W1D2-002 | No PIE has run for movement, camera, traversal, combat, or AI. | Source wiring and CDO tests do not demonstrate real world interactions; traversal execution is still not integrated. | Create the greybox map, run the input/encounter matrix in PIE, attach captures and logs. | Open / UE editor required |
| B-W1D2-003 | Adanna import and Blueprint handoff script has not executed; glTF skeletal import support is not proven in the target editor. | No native SkeletalMesh, AnimSequence, AnimBP, or playable-child asset is verified. | Run `Tools/unreal/import_adanna_proxy.py`, inspect report and resulting assets, then verify in PIE; keep proxy label. | Open / UE editor/plugin required |
| B-W1D2-004 | Windows CI cannot run in this sandbox. | No Win64 UBT build or automation result exists. | Run safe `Tools/engine/windows_ci.sh` on the reference PC at the exact pushed commit. | Open / Windows host required |

Severity convention for subsequent entries: P0 = release blocker/data loss; P1 = major core path broken; P2 = significant but bounded; P3 = minor. Never convert a missing measurement into a zero-defect claim.
