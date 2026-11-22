# TDD Production Reconciliation & W3 Readiness Report

**Document ID:** TDD-IMPL-RECON-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM. **Basis:** actual repository audit (git + `Source/` + `Tools/` + evidence), Drive assets, and prior audits (`W2_EXIT_AUDIT.md`, `W3_DELIVERY_PLAN.md`).
**Status definitions:** NOT STARTED → IN PROGRESS → DELIVERED / AWAITING REVIEW → ACCEPTED. Plus BLOCKED, REJECTED, REWORK REQUIRED, TECHNICALLY VERIFIED. A delivered asset is not automatically accepted; an accepted asset is not automatically integrated.
**Rule:** No milestone is marked complete because its documentation exists. Syntax checks are not functional tests. Pure-core tests are not Unreal/engine verification.

---

## Executive summary

**Overall schedule assessment: BEHIND.** Evidence: W2 (Stage C) is **not complete** — W2-R1–R8 are overwhelmingly NOT STARTED or only partially implemented, with no in-engine Adanna V3 import, no in-engine CH01 greybox, no functional movement/combat test suites, Windows CI unexecuted, and no metrics recorders. **W2 acceptance is a prerequisite for W3 M1-gate readiness and is not met.** W3 (Stage D) has **not started**: AC-01–31 are unmet (no `TDD-Functional.Movement.*` suite), the three cold runs have **not been executed**, and M1.32–35 are not evidenced. The **latest owner-Mac daily train at `9bf189f` is GREEN** (7/7 Unreal automation tests, 883/883 pure assertions, ledger GREEN, D-W1D8-024 closed), following the earlier `79ef5fa` compile failure — but these are **foundation/smoke tests, not the W3 M1 gate, and not cold runs**. The facial-likeness PoC pipeline is repaired (v2.1) and syntax-verified, but the **actual Blender face has not been built** — that is the single required owner-Mac step. Recovery is possible but requires focused W2 closure before any W3 claim.

**Corrections to the v1.0 report (this revision):** (1) DP-15 resolved — Research commit `41252e5` **exists** (owner-verified) and has been cherry-picked into the canonical branch (`0b30cdf`); the "does not exist" finding is withdrawn. (2) The W1 baseline preserves the `79ef5fa` failure → `9bf189f` GREEN progression accurately. (3) Future-dated production paths are explained (provenance note below). The **BEHIND** assessment is unchanged — the seven foundation tests do not promote to W3 acceptance.

**Critical action:** close W2 (test map → functional movement suite → Adanna V3 in-engine import → CH01 greybox → Windows CI → metrics) on the owner Mac, then run the facial PoC v2.1, before W3 M1-gate work is declared.

## Provenance note on production paths

Production artifact directories named `2026-11-24_w1d7_*` and `2026-11-25_w1d8_*` appear "future-dated" relative to the 2026-11-21 report date. **Provenance verified:** these directory names embed forward-looking **schedule slots** (planned W1-D7/D8 run dates), but the **commit timestamps are 2026-11-20** (`a2942de` W1D7 Blender integration, `ab45856` W1D8 promotion). The content is genuine committed production output (Adanna V3 / Guard V2 Blender packages, QC JSONs, previews), not future-dated fabrication. They are referenced here as prepared assets only; the W1D7 Blender package remains **prepared, not in-engine-imported** (W2-R4 open).

---

## 1. W1–W8 roadmap versus actual progress

| Period | Milestone | Required outcome | Actual status | Variance |
|---|---|---|---|---|
| **W1** | Stage A — Engine foundation | Owner-Mac Unreal build + daily train verification | **COMPLETE.** UE 5.8.4 foundation built; latest owner-Mac daily train at `9bf189f` **GREEN** (7/7 Unreal automation tests, 883/883 pure assertions, ledger GREEN, D-W1D8-024 camera fixture closed), following the `79ef5fa` compile failure and the iterative audit fixes (`a5858e9`→`9bf189f`). Daily train infrastructure present (`Tools/engine/mac_build.sh`, `run_daily_train.sh`). **Scope:** daily train, not the M1 gate. | On plan — W1 foundation is the one milestone genuinely delivered |
| **W2** | Stage C — M1 candidate | M1 candidate, Adanna V3 import, playable CH01 greybox | **NOT COMPLETE.** Adanna V3 FBX exists (W1D7, `.arena/`) but **not imported in-engine** (no `BP_Adanna_ProductionV3`). **CH01 greybox not built in-engine** (plan only). Movement/combat test suites not implemented. Windows CI not executed. | **BEHIND** — W2 does not exit (per `W2_EXIT_AUDIT.md`); none of the required W2 deliverables are accepted |
| **W3** | Stage D — M1 gate | AC-01–31, M1.32–35, three cold runs | **NOT STARTED.** No `TDD-Functional.Movement.*` suite; AC-01–31 unmet; three cold runs **not executed**; M1.32–35 not evidenced. | **BEHIND** — W3 gate cannot be claimed; W2 prerequisite unmet |
| **W3–W4** | Stage E — Checkpoint A | M2 traversal + Checkpoint A | **NOT STARTED.** Depends on W3 M1 gate. | **BEHIND** — downstream of unmet W3 |
| **W5–W8** | Production integration | Integrated production vs Ch.1 scope | **NOT STARTED.** Depends on W2/W3 completion. | **BEHIND** — downstream |
| **W8** | Chapter 1 RC | Release-candidate readiness by evidence | **NOT STARTED.** Far downstream. | **BEHIND** — downstream |

**Original planned deliverables vs actual** for W2 and W3 are detailed in §2 and §3. No milestone has been re-scoped, reduced, or moved to make progress appear better.

---

## 2. W2-R1–R8 detailed reconciliation

Audited against the current repository (`Source/`, `Tools/`, evidence, `.arena/`).

| # | Item | Status | Evidence / location | Acceptance |
|---|---|---|---|---|
| **W2-R1** | Test map (`L_TDD_Test_Movement`) | **NOT STARTED** | No test-map level found in `Source/` or `Config/`. `Config/DefaultEngine.ini` has `GameDefaultMap=/Engine/Maps/Entry` (no test map set). | Map must exist and load |
| **W2-R2** | Movement test suite (`TDD-Functional.Movement.*`, AC-01–13) | **PARTIALLY IMPLEMENTED** | `TDDDodgeDistanceMathTests.cpp` exists = `TDD.Movement.DodgeDistanceMath` (pure math, one test). **No `TDD-Functional.Movement.*` suite.** | AC-01–13 must pass via functional tests |
| **W2-R3** | Combat test suite (`TDD-Functional.Combat.*`) | **NOT STARTED** | No `TDD-Functional.Combat.*` tests found in `Source/`. | Combat suite must pass |
| **W2-R4** | Adanna V3 in-engine import (`BP_Adanna_ProductionV3`) | **NOT STARTED (in-engine)** | Adanna V3 FBX/blend exist in `.arena/production/2026-11-24_w1d7_blender_package/` (W1D7 outputs, Blender QC PASS). **No `BP_Adanna_ProductionV3` in `Source/`.** Asset prepared, not integrated. | BP must exist and spawn |
| **W2-R5** | CH01 playable greybox | **NOT STARTED (in-engine)** | CH01 greybox **plan/report** exists in `.arena/production/2026-11-20_w1d3_ch01_greybox/`. **No in-engine `Ch01_Greybox` map / `/Game/Maps`.** | Map must build and be playable |
| **W2-R6** | Windows CI | **IMPLEMENTED, NOT VERIFIED** | `Tools/engine/windows_ci.sh` exists. Evidence: `evidence/20261120T-W1D2/windows-ci-not-executed.txt`, `evidence/20261120T-W1D4/windows-ci-attempt.txt`. **Not executed to GREEN.** | CI must pass on Windows |
| **W2-R7** | Content integration | **NOT STARTED** | No in-engine content integration (no Adanna BP, no greybox map, no content import). | Content integrated and rendering |
| **W2-R8** | Metrics + camera recorders (`TDD.Movement.Report`, `TDD.Camera.Report`) | **NOT STARTED** | No `TDD.Movement.Report` / `TDD.Camera.Report` found in `Source/`. | Reporters must emit CSV |

**Progress since previous audit:** none of the W2-R1–R8 items has advanced to accepted. The audit verdict stands: **W2 does not exit.**

**Parallel work that can proceed without compromising the sequence:** Design visual production (environments, characters, animations, the facial PoC pipeline) proceeds independently of the W2 test/integration sequence — a blocked W2 integration does not block Design's asset production.

---

## 3. W3 AC-01–31 and M1.32–35 gate assessment

**W3 M1 gate = AC-01–31 + M1.32–35 + three cold runs.** Audited against actual evidence.

### AC-01–31 (M1 movement acceptance criteria)
The M1 movement specification (`M1_MOVEMENT_SPECIFICATION.md` v1.4) defines AC-01–31 with named automation tests (M-01a etc.). **The `TDD-Functional.Movement.*` test suite does not exist.** Only `TDD.Movement.DodgeDistanceMath` (a pure-math dodge test) exists.

| AC group | Status | Evidence |
|---|---|---|
| AC-01 (latency L1) | **NOT MET** | No `TDD-Functional.Movement.LatencyL1` test |
| AC-02–13 (input/state/movement core) | **NOT MET** | No functional movement suite; only pure dodge math |
| AC-14–18 (camera stability) | **PARTIAL** | `TDDCameraTests.cpp` has `TDD.M1.Player.CameraPitchClamp` (pitch clamp verified) — but the five stability criteria are not all tested |
| AC-19–23 (dodge/collision/state) | **NOT MET** | No `TDD-Functional.Movement.*`; dodge math only |
| AC-24–27 (input/Enhanced Input) | **NOT MET** | Enhanced Input not implemented on the production character (legacy Input only) |
| AC-28–31 (instrumentation/metrics) | **NOT MET** | No `TDD.Movement.Report` |

**AC-01–31 verdict: NOT MET.** The functional movement implementation and its test suite are absent.

### M1.32–35 (M1 gate extensions)
M1.32–35 extend the M1 gate. **No evidence of implementation or tests for M1.32–35** in the repository. **NOT MET.**

### Three cold runs
A **cold run** = a clean-build, from-scratch Unreal build + test execution on the owner Mac (not a warm/incremental build, and not a pure-core test). **Three cold runs are a W3 requirement.**

| Cold run | Status | Evidence |
|---|---|---|
| Cold run 1 | **NOT EXECUTED** | No cold-run build/test evidence in the repo. The 7 verified tests at `9bf189f` are a warm/incremental owner-Mac run, **not** a cold run. |
| Cold run 2 | **NOT EXECUTED** | None |
| Cold run 3 | **NOT EXECUTED** | None |

**Important distinction:** the **7 verified tests at `9bf189f` are GREEN** (latest owner-Mac daily train: 7/7 automation, 883/883 pure assertions, D-W1D8-024 closed) — but they are **foundation/smoke tests, not the W3 M1 gate, and not cold runs.** The earlier `79ef5fa` compile failure has been superseded by the `9bf189f` GREEN run. They do not constitute W3 readiness, and the BEHIND assessment holds until AC-01–31 + M1.32–35 + the three cold runs are actually passed.

### W3 readiness assessment (direct)
- **Are we on schedule for W3?** **No.**
- **W3 deliverables already achieved:** none of the gate items (AC-01–31, M1.32–35, three cold runs).
- **W3 deliverables in progress:** none at gate level; the M1 movement spec exists (design), but implementation/tests are absent.
- **W3 deliverables not started:** AC-01–31 functional suite, M1.32–35, three cold runs.
- **W2 dependencies preventing W3 acceptance:** W2-R1 (test map), W2-R2 (movement suite), W2-R4 (Adanna V3 import), W2-R5 (CH01 greybox) — the M1 gate requires a playable character + test map + movement suite, all W2.
- **Actual gap:** the full W2 Stage C deliverables + the entire W3 Stage D gate. The project is ~one full stage (W2) behind, plus the unstarted W3 gate.
- **Recovery sequence:** (see §11) close W2 on the owner Mac in dependency order, then run W3.

---

## 4. Three cold-run status and evidence

| # | Required | Status | Evidence | Notes |
|---|---|---|---|---|
| 1 | Clean Unreal build + M1 test execution, owner Mac | **NOT EXECUTED** | No cold-run artifact | Must be a from-scratch build, not incremental |
| 2 | Clean Unreal build + M1 test execution, owner Mac | **NOT EXECUTED** | No cold-run artifact | Repeatability check |
| 3 | Clean Unreal build + M1 test execution, owner Mac | **NOT EXECUTED** | No cold-run artifact | Determinism check |

**Evidence rule:** a cold run is evidenced by the build log + test output saved to `Saved/BuildEvidence/<timestamp>` on the owner Mac. The existing `9bf189f` evidence is a warm run and does **not** satisfy the cold-run requirement. Pure-core tests (`pure/`) are not Unreal/engine verification and do not count.

---

## 5. Full Design production inventory and W3–W8 schedule

### 5a. Visual production inventory (by category)
Grounded in `CHARACTER_DESIGN_REGISTER.md` (Drive), the directive's reported baseline, and the repository. Where exact quantity is not yet defined, the missing scope definition is flagged (not invented).

| Category | Req | Created | Accepted | Provisional/Awaiting review | Rejected/Rework | Awaiting integration | Not started | Location | Owner | Next |
|---|---|---|---|---|---|---|---|---|---|---|
| **Main characters (7)** | 7 | 7 (design boards) | 1 (Adanna master APPROVED) | 6 (Ezeani, Nneka, Okwu, Amadioha master approved/turnaround, Idemili, Hollow King — REVIEW REQUIRED) | 0 | 0 | 0 (models not built except Adanna) | Drive `CHARACTER_DESIGN_REGISTER.md` | Character Art | Adanna facial PoC → others |
| **Supporting characters (13)** | 13 | 13 (boards) | 0 (names approved OAD-15; visuals REVIEW REQUIRED) | 13 | 0 (Mgborie BLOCKED/not generated) | 0 | 0 (models not built) | Drive register | Character Art | Boards → review → models |
| **Character models/likeness** | 20 | 1 (Adanna AD-03 V3 modelled) | 0 (in-engine) | 1 (Adanna V3 FBX prepared, not imported) | 0 | 1 (awaiting UE import W2-R4) | 19 | `.arena/...w1d7.../ADANNA_AD03_V3.fbx`; Source (BP missing) | Character Art/Tech Art | Adanna V3 in-engine import |
| **Facial likeness (Adanna)** | 1 | 0 (actual face not built) | 0 | 0 | 0 | 0 | 1 (pipeline v2.1 ready, not executed) | `pipeline/facial_poc/` | PM/Character Art/owner | **Owner runs v2.1 → face** |
| **Clothing/accessories/variations** | TBD (scope def missing) | Several (Adanna costume states, palace/rebel badges) | 0 | Several | 0 | 0 | TBD | Drive register | Character Art | Establish scope with PM |
| **Enemy archetypes (6, reconciled)** | 6 | 0 | 0 | 0 | 0 (Maskbearer mask identity rejected) | 0 | 6 (CD-3 unratified) | `ENEMY_DECISION_PACKAGE.md` | Agent 2 | Owner ratification → design |
| **Environments/kits by chapter** | 8 chapters | CH01 compound V2 (1,058 tris, assembled) + kits | 0 (provisional) | CH01 kits (provisional, never canon) | 3 rejected attempts | 0 | Ch.2–8 kits | Drive + `.arena/...ch01_assembly...` | Design | CH01 → Ch.2+ |
| **Props/interactive objects** | TBD | Some (Adanna scabbard, etc.) | 0 | Some | 0 | 0 | TBD | Drive | Design | Scope with PM |
| **Character movement/combat anims** | 6+ (Adanna) | 6 (idle, walk, run, dodge-L, crouch-recover, look-back) | 0 | 6 | 0 | 0 | Combat anims | `.arena/...w1d13...adanna_animation...` | Character Art/Eng | Integrate + combat anims |
| **Deformation checks** | 46 | 46 | 46 (PASS) | 0 | 0 | 0 | 0 | W1D7 QC JSON | Tech Art | — |
| **Enemy anims/combat behaviours** | TBD | 0 | 0 | 0 | 0 | 0 | TBD (CD-3 unratified) | — | Agent 2/Eng | After enemy ratification |
| **VFX/environmental effects** | TBD | Some (white lightning direction) | 0 | Some | 0 | 0 | TBD | Drive | Design/Eng | Scope |
| **Lighting/atmosphere** | CH01 keys | 3 (dawn, dusk, night) | 0 | 3 (REVIEW) | 0 | 0 | Ch.2–8 | Drive `ch01_states/` | Design | CH01 → chapters |
| **Cinematic/narrative assets** | TBD | 0 | 0 | 0 | 0 | 0 | TBD | — | Design/Story | Scope |
| **UI/gameplay visuals** | TBD | 0 | 0 | 0 | 0 | 0 | TBD | — | Design/Eng | Scope |

**Flagged missing scope definitions (do not invent quantities):** clothing/accessory variation count, props count, enemy animation count, VFX count, cinematic count, UI count. PM + Design to establish these.

### 5b. Design weekly execution plan (W3–W8)

| Week | What Design produces | Deliverables | Refine/complete | Handover for integration | Needs from | Risk |
|---|---|---|---|---|---|---|
| **W3** | Adanna facial PoC (run v2.1 on Mac → renders/QC); CH01 environment kit refinement; Adanna movement clip integration support | 1 facial PoC bundle; CH01 kit updates | CH01 compound V2 | Facial FBX → Eng; CH01 kit → Eng | Owner (Mac run), Tech Art (QC) | Owner-Mac availability |
| **W4** | Adanna V3 full-body in-engine import support; supporting-cast board reviews; CH01 lighting keys review | Adanna integration asset; board review verdicts | Adanna V3 | Adanna V3 → Eng | Eng, owner | W2-R4 blocker |
| **W5** | Supporting-cast model production (batch); CH02 environment kit | ~3–5 supporting models; CH02 kit | — | Models → Eng | Character Art capacity | Cast scope |
| **W6** | Enemy visual design (post-ratification); Ch.3/Ch.4 kits | Enemy design boards; 2 chapter kits | — | → Eng | Owner (CD-3), Story | CD-3/CD-2 |
| **W7** | Combat/enemy animations; VFX direction | Animation sets; VFX boards | — | → Eng | Eng, Story | Depends on ratification |
| **W8** | Ch.1 RC visual integration support; cinematic/UI scoping | RC visual checklist; scope docs | All Ch.1 assets | → Eng for RC | Eng, owner | Scope definition |

**Design-to-PM reporting:** Design reports at agreed checkpoints; PM reconciles against game requirements, the visual register, chapter asset needs, Drive/repo outputs, and Tech Art/Eng integration status.

---

## 6. Character and environment production status

- **Characters:** Adanna is the only character with a modelled asset (AD-03 V3, integration-verified headless; facial PoC v2.1 pipeline ready). All other 19 named characters are at design-board stage. Amadioha/Idemili masters approved; others REVIEW REQUIRED. Mgborie BLOCKED (not generated).
- **Environments:** CH01 compound V2 assembled (1,058 tris); CH01 kit provisional (never canon); 3 rejected attempts retained. CH02–Ch.8 kits not started. ST05–ST07 (Rain/Market/Gathering) approved for production.
- **Animations:** 6 Adanna movement clips created (not integrated); 46/46 deform checks PASS. Combat/enemy animations not started.
- **Integration status:** Adanna V3 FBX **prepared, not imported** (W2-R4). No in-engine content integration yet (W2-R7).

## 7. Research catalogue integration and naming progress

**DP-15 — RESOLVED (corrected).** An earlier finding in this report stated that Research commit `41252e5` did not exist in the repository. **That finding was incorrect and is withdrawn.** The owner independently verified, and PM re-confirmed by fetching `arena/b2c58152-tdd`:

- **Commit:** `41252e5aada69d390b6342943d0f769a27c624a5` (research-agent, 2026-11-21)
- **Branch:** `arena/b2c58152-tdd`
- **File:** `docs/IGBO_NAME_CATALOGUE.md` (single file, 341 insertions)
- **Not in canonical branch** prior to reconciliation (branches had diverged)

**Reconciliation (PM + Repository Management, completed):** Cherry-picked the **single commit** `41252e5` onto canonical `arena/553fb02d-tdd` (commit `0b30cdf`). The entire Research branch was **not** merged blindly. `docs/IGBO_NAME_CATALOGUE.md` is now present in the canonical production branch, verified byte-identical to the Research commit content. The PM-authored `docs/06_IMPLEMENTATION/IGBO_NAME_CATALOGUE.md` (`1de0111`) is **preserved** (distinct path, distinct purpose).

**Distinct purposes (the two catalogues):**
- **`docs/IGBO_NAME_CATALOGUE.md`** (Research, `41252e5`) — the **authoritative sourced name resource**: a comprehensive catalogue of Igbo historical, folklore, deity, title and expression names with meaning, origin, sources, confidence ratings and sensitivity flags. **Supplies names + evidence only; does not assign names to characters.**
- **`docs/06_IMPLEMENTATION/IGBO_NAME_CATALOGUE.md`** (PM, `1de0111`) — the **PM working catalogue**: documents the names already established in the game (canon reconciliation) plus candidate names flagged for specialist verification, tied directly to the naming plan and identity records. Complements, not duplicates, the Research resource.

**Naming reconciliation (20 vs 48):**
- Existing character audit: **20 named characters** (7 main + 13 supporting), all names retained, reconciled against the storyline (Nneka–Ezeani–Adanna relationship unchanged).
- Research's "48 named characters" is a **recommendation, not an approved requirement**.
- **PM position:** retain the **20-character baseline** unless the story audit justifies a change. The cast is **not** expanded just to use the catalogue. Canon names are not casually replaced. Story reviews narrative fit; owner retains final authority. Specialist verification continues for disputed/sensitive meanings.
- **DP-15 closed** — Research catalogue present in the production branch and its contents verified.

## 8. Facial PoC and owner-Mac requirements

**Status:** pipeline **v2.1 repaired + functionally reviewed + syntax-verified**; **actual Blender face NOT yet built** (Blender cannot run in the agent environment — this is the single required owner-Mac step, not a convenience handoff). PM owns driving this to a finished PoC.

**What has been done (agent environment, complete):**
- v2.1 pipeline: portrait-guided facial base block, portrait loaded as reference, full `HUMAN_BASE_PROPOSED` skeleton, consistent binding, corrected QC.
- **[v2.1 bug fixes]** verifier now opens the saved `.blend` (was checking an empty scene → would always FAIL); backdrop excluded from FBX.
- Runbook, checklist, orchestrator staged. Syntax-verified (py_compile + bash -n PASS).

**What the owner-Mac step produces (the actual deliverable):** `ADANNA_FACIAL_POC_V2.fbx`, `.blend`, `previews/*.png` (front/side/three-quarter/back), `turntable/frame_*.png`, `evidence/BUILD_MANIFEST.json`, `evidence/QC_RESULT.json`, `evidence/EVIDENCE_BUNDLE_<ts>.txt`. Then visual comparison vs the approved portrait, then UE import + acceptance.

**Owner-Mac requirement is explicit and bounded** — see §10 (Owner action A1). PM escalates if the run fails; corrections iterate.

## 9. All incomplete, untouched and blocked work

**Incomplete (started, not finished):**
- W2-R2 movement suite (only pure dodge math); W2-R6 Windows CI (script only, not run)
- Facial PoC v2.1 (pipeline ready, not executed)
- Adanna V3 (FBX prepared, not in-engine)
- Design boards (6 main + 13 supporting REVIEW REQUIRED)

**Not started:**
- W2-R1 test map, W2-R3 combat suite, W2-R5 CH01 greybox (in-engine), W2-R7 content integration, W2-R8 metrics
- W3 entire gate (AC-01–31, M1.32–35, three cold runs)
- Ch.2–Ch.8 environment kits; enemy visual/animation; combat/enemy animations; cinematic/UI scope
- 19 of 20 character models

**Blocked:**
- W3 M1 gate — blocked on W2 acceptance (prerequisite)
- Enemy production — blocked on CD-3 ratification + CD-2 cultural review
- Mgborie (palace servant) — BLOCKED (not generated)
- Maskbearer — mask identity REJECTED (CD-2); needs replacement-name decision
- Research catalogue merge — blocked on `41252e5` being pushed to the shared remote

## 10. Owner action list with executable instructions

### A1 — Run the Adanna facial-likeness PoC v2.1 on the Mac (CRITICAL — produces the actual face)
1. **Why:** The facial PoC must reach an actual finished face; this is the single step that produces it. PM owns driving it; the owner executes the Mac build.
2. **Prerequisites:** Blender 4.2.23 LTS installed; the approved portrait placed at `pipeline/facial_poc/reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg` (or note its path). Branch `arena/553fb02d-tdd`, commit `1de0111` (or latest).
3. **Repo/branch/commit:** `The-Mhood/TDD`, branch `arena/553fb02d-tdd`, latest commit.
4. **Application:** Terminal + Blender 4.2.23 LTS (headless). No UE needed for this step.
5. **Commands (in order):**
   ```bash
   cd /path/to/TDD
   cd pipeline/facial_poc
   chmod +x run_facial_poc.sh
   # point at the portrait if not in reference/:
   export PORTRAIT_PATH="/path/to/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg"
   ./run_facial_poc.sh
   ```
6. **Expected output:** exit 0; `output/ADANNA_FACIAL_POC_V2.fbx`, `.blend`, `previews/*.png`, `turntable/frame_*.png`, `evidence/BUILD_MANIFEST.json`, `evidence/QC_RESULT.json` (verdict QUALIFIED), `evidence/EVIDENCE_BUNDLE_<ts>.txt`. Console shows each QC check PASS.
7. **If it differs:** capture `output/evidence/RUN_<ts>.log`; if QC_RESULT = FAILED, read the failing check; if the build errors, send the log to PM for correction (PM owns the fix + re-iteration). Do not mark the face reviewed/qualified.
8. **Evidence to return:** the entire `pipeline/facial_poc/output/` directory (FBX, blend, previews, turntable, QC_RESULT.json, EVIDENCE_BUNDLE) + your visual comparison of `previews/ADANNA_FACIAL_POC_V2_front.png` against the approved portrait (PASS/FAIL + notes).
9. **Save location:** copy `output/` to the project evidence store (e.g. `Saved/BuildEvidence/<timestamp>/facial_poc/` on the Mac) and return it to PM.
10. **Unlocks:** the facial PoC technical qualification → UE import + integration acceptance → the facial-likeness deliverable is closed (not at pipeline completion, but at a reviewed, qualified face).

### A2 — Close W2 on the Mac (prerequisite for W3)
1. **Why:** W2 acceptance is required before W3 M1-gate readiness can be claimed.
2. **Prerequisites:** UE 5.8.4 project open; owner Mac.
3. **Repo/branch/commit:** `arena/553fb02d-tdd`, latest.
4. **Application:** Unreal Engine 5.8.4 + Xcode.
5. **Commands/sequence (owner-executed, in dependency order):** (a) author `L_TDD_Test_Movement` map; (b) build + run `TDD-Functional.Movement.*` (AC-01–13); (c) build + run `TDD-Functional.Combat.*`; (d) import Adanna V3 → `BP_Adanna_ProductionV3`; (e) build CH01 greybox map; (f) run `Tools/engine/windows_ci.sh` (or the Mac equivalent) to GREEN; (g) content integration; (h) metrics/camera recorders.
6. **Expected output:** W2-R1–R8 each GREEN with evidence.
7. **If it differs:** record the failure; PM tracks in the defect register; iterate.
8. **Evidence:** `Saved/BuildEvidence/<timestamp>/` per item (build logs, test output, screenshots).
9. **Save location:** `Saved/BuildEvidence/<timestamp>/W2/`.
10. **Unlocks:** W2 acceptance → W3 M1 gate can be attempted.

### A3 — Run the three W3 cold runs (after W2 closes)
1. **Why:** Three cold runs are a W3 gate requirement (repeatability/determinism).
2. **Prerequisites:** W2 accepted; clean checkout.
3. **Commands:** from a clean state, `Tools/engine/mac_build.sh` + automated test execution, three times, capturing each log.
4. **Expected output:** three clean-build + test logs, all GREEN.
5. **If differs:** record; PM tracks.
6. **Evidence:** three `Saved/BuildEvidence/<ts>/coldrun_<n>/` bundles.
7. **Unlocks:** W3 M1 gate (with AC-01–31 + M1.32–35).

### A4 — Ratify the enemy roster + Maskbearer-replacement name
1. **Why:** CD-3 ratification unblocks enemy production.
2. **Input:** `ENEMY_DECISION_PACKAGE.md` v2 (reconciled with Story dispositions).
3. **Action:** per-archetype KEEP/REVISE/REJECT/APPROVE; approve the Maskbearer-replacement name.
4. **Unlocks:** enemy visual/animation production.

### A5 — Approve the character naming allocation
1. **Why:** Finalizes the 20-character cast (no inflation).
2. **Input:** `CHARACTER_NAMING_PLAN.md` + `CHARACTER_IDENTITY_RECORDS.md` (+ Research catalogue once `41252e5` is merged).
3. **Action:** approve the 20 retain allocation; decide the named-character target (PM proposes 20).
4. **Unlocks:** character model production scope.

### A6 — Provide/push Research's commit `41252e5`
1. **Why:** The commit is not present in the shared repo; PM cannot incorporate it without it being visible.
2. **Action:** push Research's branch/commit to the shared remote `The-Mhood/TDD`, or provide the correct hash.
3. **Unlocks:** PM merges Research's catalogue + the three research/assessment documents into `arena/553fb02d-tdd` (no-overwrite).

## 11. Recovery plan (accountable owners and dates)

| # | Action | Owner | Dependency | Target | Evidence |
|---|---|---|---|---|---|
| 1 | Run facial PoC v2.1 on Mac → face + QC | Owner (Mac) / PM (coord) | Portrait provided (A1) | This cycle | output/ evidence bundle |
| 2 | Author `L_TDD_Test_Movement` map | Eng (owner Mac) | — | W2-R1 | map + load evidence |
| 3 | Implement + run `TDD-Functional.Movement.*` (AC-01–13) | Eng | map (2) | W2-R2 | test GREEN |
| 4 | Implement + run `TDD-Functional.Combat.*` | Eng | movement | W2-R3 | test GREEN |
| 5 | Import Adanna V3 → `BP_Adanna_ProductionV3` | Eng | Adanna FBX | W2-R4 | BP spawns |
| 6 | Build CH01 greybox map | Eng | — | W2-R5 | map playable |
| 7 | Run Windows CI to GREEN | Eng/owner | build | W2-R6 | CI log |
| 8 | Content integration + metrics recorders | Eng | 5,6 | W2-R7/R8 | integration evidence |
| 9 | **W2 acceptance** | PM/owner | 2–8 | — | acceptance record |
| 10 | W3 M1 gate: AC-01–31 + M1.32–35 + 3 cold runs | Eng/owner | W2 accepted | W3 | cold-run bundles |
| 11 | UE import + acceptance for facial PoC | Eng/owner | A1 | — | UE acceptance bundle |
| 12 | Merge Research `41252e5` | PM | A6 | — | merge commit |
| 13 | Enemy ratification + naming approval | Owner/CD | A4/A5 | — | decision records |

**Realistic recovery sequence:** A1 (facial PoC, parallel) + W2-R1→R8 (sequential on Mac) → W2 acceptance → W3 gate → UE facial integration. The facial PoC and W2 closure can proceed in parallel (different tools/steps).

## 12. Overall schedule assessment

**BEHIND.**

**Supporting evidence:**
- W2 (Stage C) **not complete**: W2-R1–R8 are NOT STARTED or only partially implemented; no in-engine Adanna V3 import, no in-engine CH01 greybox, no functional movement/combat suites, Windows CI unexecuted, no metrics recorders (§2). Assignments issued — see `W2_IMPLEMENTATION_ASSIGNMENTS.md`.
- **W2 acceptance (prerequisite for W3) not met** (§2, §3).
- W3 (Stage D) **not started**: AC-01–31 unmet (no `TDD-Functional.Movement.*`), M1.32–35 not evidenced, **three cold runs not executed** (§3, §4).
- The 7 verified tests (`9bf189f` GREEN) are foundation/smoke tests, **not** the W3 M1 gate, and **not** cold runs (§4).
- The facial-likeness PoC is a repaired, syntax-verified pipeline; the **actual face has not been built** (§8). Owner-Mac procedure issued — see `pipeline/facial_poc/FACIAL_POC_OWNER_EXECUTION_PROCEDURE.md`.
- **DP-15 RESOLVED:** Research's `41252e5` **exists** and is now cherry-picked into the canonical branch (`0b30cdf`); the earlier "not present" finding was incorrect and is withdrawn (§7).

**No milestone has been re-scoped, reduced, or retroactively moved.** The original W1–W8 targets stand. The gap is one full stage (W2) plus the unstarted W3 gate. Recovery is achievable via the §11 sequence, with the owner-Mac execution as the critical path.

**Objective:** visibility and execution — knowing exactly how much of the game exists (W1 foundation + design assets + Adanna V3 FBX prepared), how much remains (W2 closure, the W3 gate, 19 character models, Ch.2–8 environments, enemy production), and what every department must deliver next.
