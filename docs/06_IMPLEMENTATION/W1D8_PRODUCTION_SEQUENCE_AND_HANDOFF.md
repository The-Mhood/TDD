# W1 D8 — PRODUCTION SEQUENCE & HANDOFF (towards Week 3)

**Date:** 2026-11-20  **Branch:** `arena/553fb02d-tdd`  **Commit:** `ab45856`
**Type:** Coordination of the next executable stages. Updates existing production
controls (ROADMAP v2.0, QUALITY_LEDGER, DEFECT_REGISTER); **not** a new roadmap.
**Rule set honored:** no work disrupted, no responsibilities changed, no stages skipped,
no ACs lowered, no milestone declared without deliverables + evidence.

---

## 1. Actual position against the roadmap (W1 D8, end of week 1)

### Completed and validated

| Item | Evidence | Status |
|---|---|---|
| M0 foundation | `M0_VERIFICATION_RECORD_V1.md`; owner Mac build 2026-11-18 | **Done, verified** |
| Pure C++ core (6 suites, 883 assertions) | `evidence/20261120T-W1D8/pure-run.txt`; state machine 658, AI 111, combat 39, movement 48, dodge 18, route 9 | **Green** (agent-side, ADR-0012 boundary) |
| Pure runner + Windows CI safety contracts | `evidence/20261120T-W1D8/` | **Green** |
| Character assets — Adanna V3 + Guard V2 FBX | `W1D7_CHARACTER_INTEGRATION_MANIFEST.md`; independent Blender verification `VERIFY_INTEGRATION.json` | **Validated, import-ready** |
| Blender 4.2.23 headless execution | Reproducible route in handoff update | **Working in sandbox** |
| UE project scaffold (uproject, targets, module, proxy char, gamemode, level, config) | `Source/`, `Config/`, `TDD_PHASE3_PRODUCTION/.../ue_project/` | **In tree, not compiled** |
| Chapter 1 greybox parametric builder + source | `Tools/unreal/build_chapter1_greybox.py`; source preflight pass | **Prepared, not executed in UE** |
| Tooling (daily train, pure runner, Windows CI helper, GLB validators, ledger updater, V3 import script) | `Tools/`; all Python syntax-clean | **Ready for owner run** |

### Remaining in the current stage (W1 → W2)

- **UE C++ compile (UHT/UBT) has never run.** The full module (movement, traversal,
  combat, AI, boss, player character, controllers) is written but uncompiled
  (blocker `B-W1D2-001`). This is the single item that gates all engine verification.
- **No UE native FBX import** of V3/V2 yet (`B-W1-002`, `B-W1D2-003`). Assets are
  import-ready; the production import script is prepared.
- **No UMAP generated, no PIE, no gameplay** (`B-W1-003`, `B-W1D2-002`).
- **No Windows CI** (`B-W1D2-004`).

### What blocks the next stage

The **owner's Mac daily test train** (DA-01, ROADMAP §4.4) is the #1 commitment and the
critical path. Until it produces the first real UE build + automation evidence, every
UE-dependent AC (all of M1/M2/M3 gates, Checkpoint A) is queued. Pure-core suites are
already green and do not depend on it.

### Deliverables required to enter / progress through Week 3

- **W2 exit:** M1 candidate AC-01…13 evidence; Windows suite parity run 1; Windows CI live.
- **W3 exit:** **M1 gate** — AC-01…31 + M1.32…35 in 3 cold runs on the owner Mac.
- These require: first green Mac train → V3 import → greybox UMAP → PIE movement/camera →
  M1 automation tests discovered and green.

---

## 2. Coordinated next sequence (executable stages)

Each stage states: completion, owner, dependencies, Design deliverable, PM coordination,
implementation, tests/gates, milestone enabled. Stages run in parallel where dependencies permit.

### STAGE A — Unblock the critical path: first owner Mac daily train *(immediate)*

| Field | Detail |
|---|---|
| **Complete** | **DONE — first genuine owner-Mac engine verification PASS at `712ee22`** (2026-11-20T17:49:09Z). Unreal Mac build PASS; 4/4 TDD automation tests PASS (0 failures); runner + Windows CI safety + ledger regression contracts PASS; ledger GREEN. Evidence: `Saved/BuildEvidence/20261120T174909Z` (owner machine). UHT/UBT blockers D-W1D8-001/002/003/004 fixed and re-verified on the Mac. **Stage A blocker CLOSED.** |
| **Owner** | Owner (Mac, UE 5.8.4) executed `Tools/engine/run_daily_train.sh` at `712ee22`; PM prepared the path |
| **Depends on** | Owner Mac + UE 5.8.4; committed tree (`712ee22`) |
| **Design deliverable** | None — this is engineering verification |
| **PM coordination** | Verified all owner-run scripts are syntax-clean and one-command; committed the tree; gives owner the exact invocation: `Tools/engine/run_daily_train.sh` (~60 min) |
| **Implementation** | UE module already in tree; first compile surfaces any UHT/UBT errors → fix, re-commit, re-run |
| **Tests / gates** | Pure suites green (✅ already); UE build + `TDD` automation green (pending); runner + CI-safety contracts green (✅ already) |
| **Enables** | Everything UE-dependent: V3 import, UMAP, PIE, all M-gates |

**This is the immediate handoff.** PM has done everything it can without the Mac; the
owner's one train command is the next action on the critical path.

### STAGE B — Design parallel visual development *(continuous, parallel to A/C/D)*

| Field | Detail |
|---|---|
| **Complete** | Ongoing visual production per existing responsibilities |
| **Owner** | Design (CD-led) |
| **Depends on** | Existing visual-dev lanes; no dependency on Stage A |
| **Design deliverable** | (1) **Combat anim set** retargeted to the `HUMAN_BASE_PROPOSED` skeleton (V3/V2 share it — direct retarget, no bone mapping); (2) **Environment kit v1** (core modular pieces); (3) **VFX combat set**; (4) sculpt milestone 2 (elliptical garment, brow/jaw softening, Guard one-shoulder, sash width, hem thickness) |
| **PM coordination** | Confirm anim-set delivery target aligns with M3 integration (W3–W4); flag any identity-lock changes to the frozen skeleton/materials |
| **Implementation** | None — Design-owned |
| **Tests / gates** | Design internal visual approval; identity locks (M1 art spec, ADR-0008 canon); CD sign-off where required |
| **Enables** | M3 combat integration (anim set), M5 look-dev (env kit + Adanna), M5.5 production-Adanna identity validation |

**Parallelism note:** Design does not wait for Stage A. Anim set and env kit proceed on
their own cadence. The shared skeleton guarantees the retarget is drop-in when Stage A
unblocks engine work.

### STAGE C — W2: M1 candidate implementation + V3 production import *(PM/impl, parallel to B)*

| Field | Detail |
|---|---|
| **Complete** | M1 candidate AC-01…13 evidence; V3 production asset imported; greybox UMAP built |
| **Owner** | PM (TL) coordinates; implementation on the integration line |
| **Depends on** | **Stage A first green train** (UE compile must succeed before any in-engine work) |
| **Design deliverable** | Combat anim set (from Stage B) if available for import/retarget testing |
| **PM coordination** | Run `Tools/unreal/import_adanna_production_v3.py` (prepared, hash-verified) → import V3 SkeletalMesh + wire player BP; run `Tools/unreal/build_chapter1_greybox.py` → build `Ch01_Greybox` UMAP; assign GameMode/PlayerStart; capture import + map reports |
| **Implementation** | M1-S1/S2 (dodge-sweep world test + floor validation), S4 (collision edges), S5 (third-person camera), S6 (Enhanced Input) — each landing as a verified commit; automation test naming per `M1_EXECUTION_SCOPE_AND_GATE_V1` §4 |
| **Tests / gates** | M1 candidate AC-01…13 via Mac train; test-map S7 zones present; `TDD.Movement.*` discovered and green; V3 FBX SHA + skeleton verified in-engine |
| **Enables** | **STAGE D — M1 gate (W3)** |

### STAGE D — W3: M1 gate *(the integrity checkpoint)*

| Field | Detail |
|---|---|
| **Complete** | M1 gate exited: AC-01…31 + M1.32…35 in 3 cold runs |
| **Owner** | PM/TL runs the gate; owner Mac is the verification authority |
| **Depends on** | **Stage C** (M1 candidate evidence + green train) |
| **Design deliverable** | Combat anim set delivered (retargeted) — supports M3, not a M1 blocker |
| **PM coordination** | Assemble 3 cold-run evidence bundles; ledger rows; gate report; if any AC fails → triage (spec bug → review+ADR; impl bug → fix), never weaken ACs (Rule 2) |
| **Implementation** | Fix any M1 failures surfaced by the gate; pure-core M2-01/02 traversal logic starts in parallel (frozen contract, parallel-safe) |
| **Tests / gates** | 31/31 + M1.32…35; 3 cold runs, full bundles committed; `TDD_RESULT` lines |
| **Enables** | M2 traversal gate (W4) → **Checkpoint A (W4)** |

### STAGE E — W3–4: M2 traversal + Checkpoint A *(after D)*

| Field | Detail |
|---|---|
| **Complete** | M2 gate (E1–E7, streaming data) + Checkpoint A 8-point report |
| **Owner** | PM/TL |
| **Depends on** | **Stage D** (M1 gate) |
| **Design deliverable** | Environment kit v2 (chapter-appropriate scale); Adanna model already delivered (V3) |
| **PM coordination** | Traversal integration (M2-03/04); World Partition on forest slice + PCG scatter (M2-05/06); streaming measurements; Checkpoint A go/no-go on W5–8 scope (SA register) |
| **Implementation** | `ResolveAbortFallback` two-phase, traversal suites, WP/PCG |
| **Tests / gates** | E1–E7 green ×3; streaming budget within B-12 caps; Checkpoint A AC-A1…A6 |
| **Enables** | W5–8: M3 combat, M4 AI/boss, ch.1 content, M8 perf, M9 QA → Checkpoint B (W8 RC) |

### Visual batch 1 (Design @ `1e56daf`) — integrated into the existing stages

Design's roadmap visual batch 1 is received and integrated (full mapping + decisions in
`W1D8_VISUAL_BATCH1_INTEGRATION_RECORD.md`). It slots into existing stages; no stage is
reordered or skipped, and it does not divert the UHT/Mac-verification critical path.

| Visual deliverable | Slots into | Owner / action |
|---|---|---|
| Adanna 6 unarmed poses | **Stage C/D** — shared-skeleton retarget test + first anim set | PM coordinates; impl produces retarget test + anim set (depends on Stage A) |
| Environment Kit V1 (compound + construction) | **Stage E** — CH01 settlement swap, pairs with existing W1 D7 KIT modules | PM coordinates swap; **follow smoother plaster correction**; stays provisional, never canon |
| Physical VFX board (dust/impact/rain/fire) | **Stage D/E + M5** — combat feel + ambience | PM coordinates VFX; physical base only, no ability VFX until gameplay defines abilities |
| Guard animation set — **CONFIRMED by PM** | **Stage B** → Design produces Guard pose board → Stage C/D | PM confirms set: idle, patrol, alert, hit-react, defeat |
| Enemy/encounter classes | **Stage B hold** | **BLOCKED** until story supplies class list; no classes invented visually |

Integration baseline unchanged: milestone-1 FBX pair (Adanna V3 / Guard V2) remains the
PM integration target until the V5/V3 Mac run lands; V2/V1 remain rollback fallbacks.
Nothing in this batch is visually integrated or engine-verified PASS until implementation
+ Mac evidence exist.

---

## 3. Immediate handoffs (what happens next, in order)

1. **PM → Owner (critical path):** tree committed at `5ea2997` (UHT fix + ledger fix
   applied); all owner-run scripts syntax-clean and one-command. **Owner runs
   `Tools/engine/run_daily_train.sh`** on the Mac to rerun the build + automation that
   failed at the UHT error. This is the single next action that unblocks all engine
   verification.
2. **PM → Design (parallel):** **Guard animation set CONFIRMED** — idle, patrol, alert,
   hit-react, defeat (PM decision, executed). Design proceeds to produce the Guard pose
   board next. The shared `HUMAN_BASE_PROPOSED` skeleton makes the retarget
   drop-in (no bone mapping). Design continues its visual-dev lanes without waiting.
3. **PM (now, no owner input needed):** V3 production import script prepared and
   hash-verified (`import_adanna_production_v3.py`); greybox builder ready; ledger updated
   with the W1 D8 pure-run evidence. These execute in-engine once Stage A is green.
4. **PM (now):** visual batch 1 (`1e56daf`) integrated into the sequence — Adanna poses
   queued for the Stage C retarget test, Env Kit V1 queued for the Stage E CH01 swap
   (smoother plaster correction carried), VFX board queued for VFX/TD, enemy classes
   held. Pure-core M2-01/02 traversal logic can also be developed agent-side in parallel
   (frozen contract, parallel-safe per ROADMAP §4.5) — does not wait for the Mac.

## 4. Execution discipline (preserved, not relaxed)

- No milestone declared complete without its deliverables + committed evidence
  (ROADMAP Rule 3). Pure-core green ≠ engine-verified (QUALITY_LEDGER semantics).
- No ACs lowered, no tests removed, no defects ignored (Rule 6).
- `NOT EXECUTED` / `BLOCKED` is never reported as `PASS`.
- Design and PM proceed in parallel; neither waits for the other to finish its whole
  workload. Dependencies are respected: engine work waits for Stage A; pure-core and
  Design visual work do not.

## 5. Open blockers carried forward (unchanged)

- **B-W1-001 / B-W1D2-001:** UE runtime absent from sandbox → owner Mac train required.
- **B-W1-002 / B-W1D2-003:** V3/V2 native UE import not yet executed → Stage C.
- **B-W1-003 / B-W1D2-002:** no UMAP/PIE yet → Stage C.
- **B-W1D2-004:** Windows CI not run → reference PC from W2.
- Capsule dimensions, AD-02 signature, minimum-anim-set ruling: pending owner/TD/CD
  decisions per existing OPEN_QUESTIONS and RISK register.
