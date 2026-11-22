# Foundation reconciliation — Agent 1's skeleton vs the project on `arena/5dde91a4-tdd`

**Document ID:** `TDD-IMPL-RECONCILE-001`
**Date:** 2026-11-18 UTC
**Author:** Agent 1 (architecture and implementation lead)
**Branch of this document:** `arena/3bc206a0-tdd` @ `b7aff63`
**Addressed to:** Agent 3 (design/governance, traceability) and the Technical Director
**Status:** reconciliation record. **No project was created here, nothing on the other branch was modified, and no branch was merged.** Both foundations remain unbuilt.

---

## 1. What this is, and what I did not do

TD instructed: *work with Agent 3 to reconcile your foundation with the project created on the authorized branch; do not independently create another project or overwrite existing work.*

I therefore did exactly three things: **read** the other project, **compared** the two mechanically (with a committed tool), and **wrote this record** with a proposed non-destructive composition and the questions Agent 3 must settle. I did not create a second project, did not force-push, did not merge, did not cherry-pick another agent's files, and did not edit a single file that belongs to the other foundation.

## 2. Where the two foundations actually are — one correction to the directive

| Claim | Reality, pinned |
|---|---|
| "the project created on the authorized branch" (`arena/c64fc525-tdd`) | **That branch contains no Unreal project.** At `c800bf0` it holds 26 files, zero `.uproject`, zero `Source/`. |
| Where the other project actually is | **`arena/5dde91a4-tdd` @ `33aa8cc73a80600f0af1a1ed1c69d8c42d9502a4`** — the project landed in `e95c238 "Stage 0: architecture foundation, canon index and validators"`. 141 files, 3 modules. |
| My foundation | **`arena/3bc206a0-tdd` @ `b7aff63`** — 113 files, 9 modules. |

This is worth correcting before anyone composes anything: the reconciliation target TD names and the branch that actually holds the other project are not the same branch.

## 3. Inventory, pinned

| | **A — Agent 1** (`3bc206a0` @ `b7aff63`) | **B — project on `5dde91a4`** (@ `33aa8cc`) |
|---|---|---|
| Descriptor | `TDD.uproject`, blob `d6d44cbc…` | ``TDD.uproject``, blob `4e1c1148…` |
| Engine association | `5.8` | `5.8` — **agree** |
| Declared modules | 9: `TDD`, `TDDCore`, `TDDWorld`, `TDDGameplay`, `TDDAI`, `TDDNarrative`, `TDDUI`, `TDDEditor`, `TDDTests` | 3: `TDDRuntime`, `TDDEditor`, `TDDTests` |
| Module architecture | MEAD §3.2 graph, downward-only, `TDDCore` a leaf | one primary runtime module (`TDDRuntime`) with internal folders, per **its own** architecture document |
| Module implementations | 9 / 9 have `IMPLEMENT_*_MODULE` | **1 / 3** — `TDDEditor` and `TDDTests` have a `Build.cs` but **no translation unit** |
| Runtime code of substance | engine-pin constants, `LogTDD`, one automation test | `Framework/TDDIds.h/.cpp` — canonical ID types (ADR-0006), real content |
| Targets | `TDD.Target.cs`, `TDDEditor.Target.cs`; `BuildSettingsVersion.Latest`, `EngineIncludeOrderVersion.Latest` | `TDD.Target.cs`, `TDDEditor.Target.cs`; `BuildSettingsVersion.V5`, `EngineIncludeOrderVersion.Unreal5_6` |
| Config | `DefaultEngine.ini`, `DefaultGame.ini`, `DefaultInput.ini` | `DefaultGameplayTags.ini` only |
| Plugins | 1 (`EnhancedInput`) | 13 (`CommonUI`, `StateTree`, `GameplayAbilities`, `Niagara`, `MetaSound`, `PCG`, `Water`, `IKRig`, `ControlRig`, `MVVM`, `GeometryScripting`, `ModelingToolsEditorMode`, `EditorScriptingUtilities`) |
| Automation tests | 1 (`TDD-Unit.Canon.EnginePin`), naming `TDD-Unit.*` / `TDD-Functional.*` | none; naming `TDD.<Area>.<Behaviour>` in `TDDTests.Build.cs` |
| Documentation root | `docs/` (lowercase) — 13-code ADR series `ADR-0001…0013` in `docs/03_DECISIONS/` | `Docs/` (capital) — 8-code ADR series `ADR-0001…0008` in `Docs/adr/` |
| Verification tooling | `Tools/engine/preflight.sh`, `verify_project_structure.py`, **`reconcile_foundations.py`** (new) | ~40 Python tools/tests: canon index, world manifest, evidence generation, contract-review suites |
| Built? | no | no |

**The two projects are not variants of one design.** They are two different architecture documents materialised as two different module graphs: mine follows `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` §3.2; theirs follows `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, which prescribes a single primary module. That divergence **is the TD-12 / B-4 question made concrete** — "canonical MEAD and the contract-layer owner" — not a matter of taste that two agents can settle between themselves.

## 4. The mechanical comparison

Committed tool: `python3 Tools/engine/reconcile_foundations.py <tree-a> <tree-b> --name-a … --name-b … [--json out.json]`. It reads each `.uproject`, each module's `Build.cs`, both targets, the config inventory, automation tests, the documentation root and the ADR identifiers, and prints only where the two differ. It writes to neither tree.

Run for this document (`git archive` of each branch head into `/tmp`, no working-tree changes):

```
engine association      both '5.8'                       =
target platforms        A: None         B: ['Windows']   ≠
module set              A: 9 modules    B: 3 modules     ≠
unimplemented modules   A: none         B: ['TDDEditor', 'TDDTests']   ≠
TDD.Target.cs           A: Latest/Latest B: V5/Unreal5_6             ≠
config                  A: Engine/Game/Input  B: GameplayTags only    ≠
plugins                 A: 1            B: 13             ≠
automation tests        A: 1            B: 0              ≠
doc root                A: docs/        B: Docs/          ≠  (case collision)
ADR ids                 A: 0001-0013    B: 0001-0008      ≠  (8 colliding identifiers)
differing fields: 12
```

**My structural verifier applied to B** (as a comparison instrument, not a verdict — it encodes *my* MEAD's graph, so a module-graph mismatch is expected and is not a defect on their side): **17/25 checks pass**. The failures that are real gaps rather than architecture differences are: `TDDEditor` and `TDDTests` have no implementation TU; `DefaultEngine.ini`, `DefaultGame.ini`, `DefaultInput.ini` are absent; no automation test exists. Applied to A it remains **58/58**.

## 5. Findings, in the order that blocks

### 5.1 Hard blockers — need a decision, not a patch

| # | Blocker | Why it cannot be decided between agents |
|---|---|---|
| **R-1** | **`docs/` vs `Docs/` case collision.** | A single checkout on Windows or macOS (case-insensitive) cannot hold both trees. Whichever root survives is a repository-structure decision with governance consequences (every existing link in both documentation sets points at its own root). |
| **R-2** | **Canonical MEAD → module architecture.** 9 modules vs 1 + editor/tests. | This is **TD-12 / B-4**. Composing the graphs by renaming would decide it silently. If the 9-module graph wins, `TDDRuntime`'s content moves into `TDDCore`/`TDDWorld`/`TDDGameplay`; if the single-module design wins, my seven gameplay modules collapse and MEAD §3.2 is rewritten. Both are one-way doors for the code. |
| **R-3** | **Two ADR series using the same identifiers for different decisions.** A: `ADR-0001` = pin UE 5.8, `ADR-0002` = …; B: `ADR-0001` = automation harness, `ADR-0002` = engine baseline UE 5.8. **8 colliding IDs.** | ADR identity is governance. A single renumbering must be authorised and applied to one series only, with the other's documents untouched (**ADR-0004** in B is `PROPOSED — blocked on CD/infra`, so its status matters too). |

### 5.2 Defects to hand to the other foundation — cheap, and only visible at first build

| # | Finding | Effect | Recommended fix |
|---|---|---|---|
| **R-4** | `TDDEditor` and `TDDTests` are declared in `TDD.uproject` but contain **no `IMPLEMENT_MODULE` translation unit** | the project **cannot link** as declared; the descriptor promises modules that do not exist | add one `.cpp` per module (`IMPLEMENT_MODULE(FDefaultModuleImpl, …)`) — I already have equivalents on my branch and will not copy them across without Agent 3's agreement |
| **R-5** | `TDDTests` is declared **`Type: Runtime`, `LoadingPhase: PostEngineInit`**, but its `Build.cs` depends on `UnrealEd` (editor-only) and its own comment says *"Automation tests are editor-run only"* | a Runtime module with an `UnrealEd` dependency **fails to build for a Game target**; if changed to Editor type, the descriptor and the comment agree | make it `Type: Editor`, or drop `UnrealEd` and the editor-only assumptions — the two must match |
| **R-6** | `EngineIncludeOrderVersion.Unreal5_6` on a project pinned to **5.8** | legal but pins include order one minor behind the engine; surprises arrive at upgrade time | either `Latest`, or an explicit 5.8 value once a build verifies it (`BuildSettingsVersion.Latest` avoids the same trap) |
| **R-7** | No `DefaultEngine.ini`, `DefaultGame.ini`, `DefaultInput.ini` | the project has no renderer/physics/input baseline; `DefaultGameplayTags.ini` alone will not boot a configured map | compose: keep `DefaultGameplayTags.ini`, add the three config files (mine are a starting point, not an authority) |

### 5.3 Where the other foundation is ahead of mine, and should be adopted

| # | Theirs is better | Why |
|---|---|---|
| **R-8** | `TargetPlatforms: ["Windows"]` declared in the descriptor | makes the platform explicit rather than implied. **I adopted this on my branch in this commit** (see §7) |
| **R-9** | 13 plugins enabled, each traceable to an ADR (GAS scope ADR-0003, StateTree, PCG, Water…) | plugin enablement is a design decision my descriptor simply lacks. Mine should adopt *their list after ADR review*, not invent one |
| **R-10** | `Framework/TDDIds.h` — canonical ID types tied to ADR-0006 and `Docs/CANON_INDEX.md` | real contract-adjacent content that survives **any** module architecture: it belongs wherever `TDDCore`/`TDDRuntime` ends up, unchanged |
| **R-11** | ~40 Python tools with tests (canon index, world manifest, evidence generation) | orthogonal to the Unreal tree; nothing on my side conflicts with `Tools/canon/` or `Tools/world/` — they should be carried over whole |

## 6. Non-destructive composition — two routes, both preserving everything

Neither route creates a third project. In both, the losing branch keeps its history; nothing is force-pushed; the composition lands as one additive commit on **one** integration branch chosen by TD.

**Route A — `arena/5dde91a4-tdd` becomes the integration branch** (it holds the richer tooling and the Agent 2 evidence):
1. Agent 3 renumbers its ADR series **or** mine (R-3), by decision.
2. My `Source/` tree arrives as an **additive** commit: `TDDCore/TDDWorld/TDDGameplay/TDDAI/TDDNarrative/TDDUI` added; `TDDRuntime`'s `Framework/TDDIds.*` moves into `TDDCore/Public/Framework/` unchanged; `TDDRuntime`'s `Build.cs` plugin list is folded into `TDDEditor`/`TDDAI`/`TDDGameplay` deps.
3. `docs/` → merged under one root (R-1), links rewritten **only in the moved set**.
4. My config triad added; `DefaultGameplayTags.ini` kept.
5. `Tools/engine/` added beside `Tools/canon/` and `Tools/world/`.
6. One `.uproject`: `TargetPlatforms: Windows`, 9 modules (or the single-module design if TD-12 says so), their plugin list, my `BuildSettingsVersion.Latest`.

**Route B — `arena/3bc206a0-tdd` becomes the integration branch**: the same six steps with the directions swapped; their `Docs/` content and `Tools/canon`, `Tools/world`, `Config/DefaultGameplayTags.ini` arrive additively here.

**Route C — TD-12 unresolved**: declare a *holding* state (both projects stand, no integration commit), and record which branch engineering will use for the first tranche. **This is the only route that requires no guess**, and it is what the current evidence supports: without the canonical-MEAD answer, any composition chooses the architecture by file layout.

## 7. What I changed on my own branch in this commit

| Change | Why it is not an overwrite |
|---|---|
| Added `Tools/engine/reconcile_foundations.py` | new tool; reads any tree, writes nothing |
| Generalised `verify_project_structure.py` to report an unknown module instead of crashing, and to compare dependencies **over project modules only** | bug fix; it crashed on a foreign tree (`KeyError: 'TDDRuntime'`) and mis-flagged engine modules as policy violations. Re-verified: my tree still **58/58** |
| Adopted `TargetPlatforms: ["Windows"]` in `TDD.uproject` (R-8) | aligning with both the MEAD's Windows-primary statement and the other descriptor; additive |
| This document, and the ledger/index rows that reference it | record only |

Nothing else on my side was touched; their branch was not modified, and no file of theirs was copied into my tree.

## 8. Questions for Agent 3 — numbered, answerable, with my recommendation

| # | Question | My recommendation |
|---|---|---|
| **Q1** | Which documentation root survives: `docs/` or `Docs/`? | `docs/` (lowercase) — it is the root the majority of existing documents and every link in the C-05 series already use; rename B's root in a single dedicated commit that only moves files |
| **Q2** | Which MEAD is canonical, and does its module architecture stand? (TD-12) | **TD must answer.** Until then, Route C. If mine is canonical, `TDDRuntime` folds into the 9-module graph; if theirs is, MEAD §3.2 is superseded by an ADR and I will rewrite my Source tree |
| **Q3** | Which ADR series keeps `0001…0013`, and which renumbers? | keep **A**'s numbering (13 codes, more history), renumber B's eight into `0014…0021` in one mechanical commit, leaving B's ADR bodies untouched except the ID line |
| **Q4** | Does `TDDTests` become Editor-type (R-5), and does `TDDEditor`/`TDDTests` get its missing translation units (R-4)? | yes to both; R-5 is a build-breaking inconsistency today, R-4 guarantees a link failure the moment an engine exists |
| **Q5** | Is `BuildSettingsVersion.Latest` / `EngineIncludeOrderVersion.Latest` acceptable until a verified 5.8 build pins them? | yes; explicit values should be pinned **from** a passing build, not before one |
| **Q6** | Which branch is the integration branch (Route A, B or C)? | Route C until Q2 is answered; then A or B as TD directs |
| **Q7** | Is `Framework/TDDIds.*` to be relocated under the surviving core module unchanged? | yes — it is the only code in either foundation with contract meaning, and it is architecture-neutral |
| **Q8** | Does Agent 3 accept `Tools/engine/*` as the project-level verification entry point, beside `Tools/canon` and `Tools/world`? | yes; `preflight.sh` and `verify_project_structure.py` are the only artefacts that can report "this machine cannot build this project" honestly |

## 9. Status, restated

- **Both foundations remain unbuilt.** No engine exists on either side; neither branch claims a compile, an editor launch or a test result.
- **C-05 remains `DESIGN_ONLY`, unsigned and unfrozen**; 43 obligations, 18 suites and 67 case identities untouched; `F-1b` closed; `D-c` deferred; `D-d` refused; **0 of 67 acceptance cases executed**.
- **`A1-C05-S4.3.10` and its 147/147 evidence are untouched** (blob `857778e1…`), and so is everything on `arena/5dde91a4-tdd`.
- This document is a proposal for reconciliation, **not** a merge, an approval, or a new foundation.
