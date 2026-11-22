# W3 Delivery Plan — The Disobedient Daughter

**Document ID:** TDD-IMPL-W3PLAN-001 · **Version:** 1.1 (W2-sequencing correction) · **Date:** 2026-11-21
**Author:** PM (project management) + Design Lead, jointly. Coordinated by the Takeover Lead (this session).
**Checkpoint of record:** commit `9bf189f` on branch `arena/553fb02d-tdd` — **owner-Mac daily train GREEN** (evidence `Saved/BuildEvidence/20261121T170504Z`). This is the latest known-good checkpoint and the base for all work.
**Milestone:** **W3 = the M1 gate** (ROADMAP v2.0 §4.2; MAC M1: AC-01…31 + M1.32–35, **three cold runs**). This document is the executable plan to exit that gate. It adds no new ACs and weakens none.
**v1.1 correction (W2 exit audit):** This plan does **not** treat W3 as the current execution stage. A W2 (Stage C) exit audit (`W2_EXIT_AUDIT.md`) found that **W2 is not complete and not accepted**: M1 candidate preparation (AC-01…13), Adanna V3 in-engine import, CH01 greybox map build, combat functional integration, and Windows CI are all PREPARED / IN PROGRESS / NOT EXECUTED, with the actual Mac-side verification steps not run. The owner-Mac GREEN at `9bf189f` verifies only a subset (7 in-engine tests). **Remaining W2 work is the immediate priority; W2 must be accepted before the W3 M1 gate is approached.** Sequencing and status reporting below are corrected accordingly. No W2 deliverable is renamed as W3 work, removed, or accepted on code-presence/build-pass alone.

**Verification-scope statement (read first):** The agent sandbox has g++ and Python but **no Unreal Engine installation and no owner Mac/Windows hardware**. Therefore, in this document: *static checks* (agent-side pure-core suites, `build_readiness.py`, runner-contract/CI-safety/ledger checks) are **verified in-sandbox**; *Unreal compilation and runtime* are **NOT verified in-sandbox** — they are reported only from the owner-Mac train at `9bf189f` (GREEN). A GREEN daily train is **not** the M1 gate; the M1 gate requires three cold runs of AC-01…31 + M1.32–35, which is **not yet exited**. The GREEN train is also **not** W2 acceptance — see `W2_EXIT_AUDIT.md`.

---

## A. W3 Gap Assessment

### A.1 What is already complete (verified)

| Area | State | Evidence / basis |
|---|---|---|
| M0 foundation | **Done** (2026-11-18, owner Mac) | `M0_VERIFICATION_RECORD_V1.md`; `TDD.Foundation.GameModeClass` green |
| Pure-core logic layer (UE-independent C++) | **Done, 6/6 suites, 883 assertions** | `Tests/Standalone/` — `TDDStateMachineTests` 658, `TDDAIPureCoreTests` 111, `TDDMovementCoreTests` 48, `TDDCombatMathTests` 39, `TDDDodgeDistanceMathTests` 18, `TDDChapterRouteTests` 9 |
| Production code present in tree | **Present** | `TDDAdannaCharacter` (CMC + spring-arm camera + pitch clamp + legacy input + combat/traversal/state hooks), `TDDGameMode` (encounter flow + restart), `TDDLightingStateSwitcher`, `TDDDodgeSweep`, `TDDTraversalComponent`, `TDDCombatComponent`, `TDDCharacterStateComponent`, AI (`TDDCombatBrainComponent`, `TDDCombatDirectorSubsystem`, `TDDTrainingBoss`, `TDDTrainingEnemy`, `TDDBossPhaseComponent`), pure-core headers (`TDDStateRules.h`, `TDDInputBuffer.h`, `TDDTraversalFallback.h`, `TDDDamageMath.h`, `TDDGaitMath.h`, `TDDSeededRandom.h`, `TDDCombatTiming.h`, `TDDChapterRoute.h`, `TDDAIPureCore.h`, `TDDDodgeDistanceMath.h`) |
| In-engine automation (7 tests) | **All GREEN at `9bf189f`** | `TDD.Foundation.GameModeClass`, `TDD.M1.GameMode.EncounterFlow`, `TDD.M1.Lighting.StateSwitcher`, `TDD.M1.Player.CameraPitchClamp`, `TDD.M1.Player.PlayableCharacterDefaults`, `TDD.Movement.DodgeDistanceMath`, `TDD.W1D2.AI.BossPhaseAssetAdapter` |
| D-W1D8-024 (camera pitch clamp) | **RESOLVED & CLOSED** | Owner-Mac GREEN at `9bf189f`; audit #3 root cause (frozen `GFrameCounter` → `HasBeenVisited` suppression) fixed in the fixture; `DEFECT_REGISTER.md` Evidence cell + `QUALITY_LEDGER.md` closure row committed |
| Daily-train + tooling infrastructure | **Operational** | `Tools/engine/run_daily_train.sh`, `parse_automation_report.py`, `build_readiness.py` (with UHT/UBT/engine-header guards), `Tools/tests/pure/*`, ledger + defect register |

### A.2 What remains (the W3 gap — the M1 gate is NOT yet met)

The M1 gate requires **AC-01…31 + M1.32–35**. Mapping the gate against the tree, the verified in-engine tests cover only a **small fraction** of AC-01…31. The dominant gap is the **functional movement test layer + its test map**, which does not yet exist.

| Gate element | Required | Exists in tree? | Gap |
|---|---|---|---|
| `L_TDD_Test_Movement` test map (§7, 11 zones: `Z_Flat`, `Z_Slope`, `Z_Steps`, `Z_StepDown`, `Z_SprintRun`, `Z_Corner`, `Z_Corridor1/2`, `Z_Drop`, `Z_Dodge`, `Z_SpawnPoints`) | M1.34, and the map that all `TDD-Functional.Movement.*` tests drive | **NO** — default map is `/Engine/Maps/Entry`; no test map referenced anywhere | **BLOCKED ON MAC** — must be authored in the UE editor (cannot be produced headlessly). Task P-09 / M1-S7. **This is the single hard blocker for the M1 gate.** |
| `TDD-Functional.Movement.*` (AC-01…13, 19–21, 27, 29: LatencyL1/L2/L3, AcceleratesToMaxSpeed, StopsWithinDistance, Turn180Degrees, StepUp*, StepDown*, StepAngledApproach, SprintOverStep, CornerStability, SlopeLimits, CameraPenetration/AngularStability/Displacement/Recovery/AcquisitionSlew, DodgeDistanceRepeatable/DodgeIFrames/DodgeRespectsCollision, InputDeviceParity, NoPermanentInputLock) | AC-01…13, 19–21, 27, 29 | **NO** — none registered | All functional movement ACs are unverified. Depends on the test map. Task M1-S1, M1-S5. |
| `TDD-Unit.Movement.*` in-engine (StateRulesComplete, StateSemantics, InputBuffer, CoyoteWindow, RootMotionAppliesToCapsule, RootMotionRestoresMovementMode, DodgeSpecMath) | AC-22…26, 19 | **PARTIAL** — pure-core logic exists (`TDDStateRules.h`, `TDDInputBuffer.h`, `TDDDodgeDistanceMath.h`) and is tested agent-side, but the **in-engine named tests do not exist** | In-engine unit tests for state semantics / input buffer / coyote / root-motion restoration not written. Task M1-S3/S6. |
| Enhanced Input (actions/contexts, buffering, coyote window, device parity) | AC-20…23, AC-27 (M1-S6; spec §3.4) | **NO** — character uses the **legacy Input Component** (`BindAxis`/`BindAction`); `EnhancedInput` is **not** in `TheDisobedientDaughter.Build.cs` and is used nowhere | **Input-system migration gap.** The `TDDInputBuffer.h` pure-core exists, but the Enhanced Input integration is not implemented. Task M1-S6. |
| Metrics harness `TDD.Movement.Report` (frame-stamped CSV: L1–L3, M-02…04, step results, camera criteria, dodge distance) | M1.32, AC-28, AC-30 (M1-S7) | **NO** | No metrics CSV/dashboard. Task M1-S7. |
| Camera 5-criteria recorder + `TDD.Camera.Report` + rig table | AC-14…18 (M1-S5) | **NO** — `TDD.M1.Player.CameraPitchClamp` verifies the pitch clamp only; it is **not** the 5-criteria corridor sweep recorder | Camera stability ACs unverified. Task M1-S5. |
| M1-P1…P6 first-playable record (launch, control, environment, navigate, interact, metrics overlay) | M1.32 (M1-S9) | **NO** — needs a packaged build + the test map | Task M1-S9. |
| Agent 2 defects ①②③ closure + test-name traceability + floor-validation guard in every state exit | M1.33 | **PARTIAL** — state machine tested (658), but `TDD-Functional.Movement.*` test-name traceability and the floor-validation guard are not in place | Task M1-S1/M1-S2. |
| Performance AC-28 (player frame cost ≤ 0.30 ms Development) | AC-28 | **NO** — no Insights capture | Task M1-S7 + owner Insights run. |
| Three consecutive cold runs (identical results, metrics within tolerance) | AC-31, M1.35 (M1-S10) | **NO** — not executed for M1 | Task M1-S10. |
| Mannequin animation set for M1 (labelled interim) | AC-26 (root-motion), M1-S8 | **PREPARED** — `import_adanna_production_v3.py` + movement clips V1 (46/46 source PASS) prepared; Mac import/integration pending | Content-side; gates root-motion AC-26. |

### A.3 What is blocked

1. **`L_TDD_Test_Movement` map authoring — BLOCKED ON MAC (hard blocker).** All `TDD-Functional.Movement.*` ACs (AC-01…13, 19–21, 27, 29) and the camera corridor sweeps (AC-14…18) drive off this map's zones. It must be authored in the UE editor on the owner's Mac. **Until it exists, the M1 gate cannot be approached.** This is the #1 blocker.
2. **Reference PC / Windows CI (B-03 / DA-03)** — Windows parity evidence is not yet in the loop; not a W3-M1 blocker (M1 gate is Mac-side) but a Checkpoint-A (W4) dependency.
3. **M1-S8 mannequin animation import** — Mac step pending; gates root-motion AC-26 verification.

### A.4 What must be done before W3 (M1 gate) can be accepted

A closed, ordered set — see §B. In summary: author the test map → implement the functional/unit movement test layer → migrate to Enhanced Input → build the metrics + camera recorders → run the three cold Mac runs → record the gate. **No AC is waived; no test is removed.**

---

## B. W3 Execution Breakdown

Ordered work packages (WP). Task IDs align with `MASTER_WORK_BREAKDOWN.md` (WBS v2.0) and the M1 spec. Owner codes: **T1** = core/movement track, **T2** = combat/AI, **T3** = systems/world, **TL** = Takeover Lead, **OW** = owner (Mac), **CT** = content team.

### WP-1 — Author the controlled test map (BLOCKER RESOLUTION) — *sequential, first*

| Task | Owner | Depends | Acceptance | Verification |
|---|---|---|---|---|
| **P-09** Author `L_TDD_Test_Movement` with all §7 zones (`Z_Flat`, `Z_Slope`, `Z_Steps`, `Z_StepDown`, `Z_SprintRun`, `Z_Corner`, `Z_Corridor1/2`, `Z_Drop`, `Z_Dodge`, `Z_SpawnPoints`), grey materials, named `PlayerStart` per zone, blockout dimensions per spec §4 | **OW** (Mac editor) + T1 spec support | M0 (done) | Map loads; every zone present with spec dimensions; `PlayerStart` per zone | Map-load automation assertion + dimension check (M1.34). **Mac-only.** |
| Commit map + a `TDD.M1.Map.TestMapLoads` automation test asserting load + zone presence | T1 | P-09 | Test green in train | Owner-Mac train |

### WP-2 — Movement functional test layer (the AC-01…13/19–21/27/29 body) — *after WP-1, parallelizable internally*

| Task | Owner | Depends | Acceptance | Verification |
|---|---|---|---|---|
| **M1-S3** Confirm/complete character + CMC + state-machine wiring to the spec (196 pairs, coyote, step smoothing, slope overrides) | T1 | P-08 (contracts) | Character moves per spec; state machine exhaustive | Pure-core (agent-side) + in-engine named tests |
| **M1-S1** Implement `TDD-Functional.Movement.*`: LatencyL1/L2/L3, AcceleratesToMaxSpeed, StopsWithinDistance, Turn180Degrees (AC-01…06); 100-run determinism + variance + failure classification (AC-24…26 support, M1.33 ①) | T1 | WP-1 | Each named test green | Owner-Mac train (3 runs for the 100-run suite) |
| **M1-S2** Floor/ground validation + floating-capsule guard in every state exit (AC-29, M1.33 ③) | T1 | M1-S3 | Guard assertion green in every exit | Owner-Mac train |
| **M1-S4** Collision edge cases: 45° step-up, ledge hold, narrow gaps, blocked-dodge clamp (AC-07…13, 21, 22) | T1 | M1-S3, WP-1 | Edge-case tests green | Owner-Mac train |
| **M1-S5** Camera 5-criteria recorder + `TDD.Camera.Report` + rig table; corridor sweeps (AC-14…18) | T1 | M1-S3, WP-1 (corridors) | All five camera criteria green over 60 s sweeps, both corridors | Owner-Mac train + capture |
| **M1-S6** **Enhanced Input migration**: actions/contexts, buffering, coyote window, remappable actions, device parity (AC-20…23, 27) | T1 | M1-S3 | AC-20…23, 27 green; parity ≤ 1 frame | Owner-Mac train + device matrix |
| **M1-S7** Metrics harness `TDD.Movement.Report` CSV (L1–L3, M-02…04, steps, camera criteria, dodge distance) + dashboard (AC-28, 30, M1.32) | T1 | M1-S1…S6 | CSV per run committed; harness overhead ≤ 0.05 ms | Owner-Mac train + Insights (AC-28) |

### WP-3 — In-engine unit movement tests (AC-22…26, 19) — *can start before WP-1 (logic-only)*

| Task | Owner | Depends | Acceptance | Verification |
|---|---|---|---|---|
| `TDD-Unit.Movement.StateRulesComplete` + `.StateSemantics` (AC-22, 23) | T1 | M1-S3 | 196-pair exhaustive + semantics green | Owner-Mac train (pure-core already agent-side green) |
| `TDD-Unit.Movement.InputBuffer` + `.CoyoteWindow` (AC-24, 25) | T1 | M1-S6 | Buffer/coyote assertions green | Owner-Mac train |
| `TDD-Unit.Movement.RootMotionAppliesToCapsule` + `.RootMotionRestoresMovementMode` (AC-26) | T1 | M1-S3, M1-S8 (anim) | Capsule displaced + mode restored on all exits | Owner-Mac train + M1-S8 import |
| `TDD-Unit.Movement.DodgeSpecMath` (AC-19 unit) | T1 | M1-S3 | Radius-once assertion green | Owner-Mac train (pure math already agent-side green) |

### WP-4 — First-playable record + gate — *sequential, last*

| Task | Owner | Depends | Acceptance | Verification |
|---|---|---|---|---|
| **M1-S9** First-playable pass: interaction volume, checkpoint marker, metrics overlay; produce M1-P1…P6 record with metric values | T1 + OW | WP-1…WP-3 | M1-P1…P6 record complete (M1.32) | Packaged-build launch log + `TDD.Movement.Report` CSVs |
| **M1-S10** **M1 GATE**: three consecutive cold Mac runs; full bundles (build, tests, `TDD_RESULT`, CSVs); diff review vs spec v1.4; ledger entry | **OW + TL** | all WP-1…WP-4 | **31/31 + M1.32…35**, three cold runs identical within tolerance (AC-31, M1.35) | Three committed evidence bundles |

### Parallel execution map

- **WP-1 (map) is the gating serial block** — owner-Mac editor. Start immediately.
- **WP-3 (in-engine unit tests, logic-only) can proceed in parallel with WP-1** — these test state/buffer/coyote/dodge logic and do not require the full map. Start now.
- **WP-2 (functional tests) is gated on WP-1** for the zone-driven tests (AC-01…13, 19–21, 27, 29, 14…18). The Enhanced Input migration (M1-S6) and metrics harness (M1-S7) skeleton can begin during map authoring.
- **WP-4 (gate) is strictly last** and sequential.
- **Single-owner surfaces** (no parallel conflicts): movement/camera/input = T1 sole owner; the test map = OW+T1; merge batches reviewed by TL (DA-02 cap ~25/week).

### Complete sequence — remaining W2 work → W2 acceptance → W3 M1 gate → Checkpoint A

Per the W2 exit audit (`W2_EXIT_AUDIT.md`), W2 (Stage C) has not exited. The WP-1…WP-4 above are the **W3 M1-gate** work packages; they sit **after** the remaining W2 work and **after W2 acceptance**. The corrected full sequence is:

```
[REMAINING W2 WORK — parallel, immediate priority]        (W2-EXIT-AUDIT §"Remaining W2 work")
  OW (Mac):    W2-R1 L_TDD_Test_Movement map   ─┐
               W2-R4 Adanna V3 import+BP       │  Mac sessions (batched)
               W2-R5 CH01 greybox build        │
               W2-R6 Windows CI bring-up        │  (reference PC)
               W2-R7 content in-engine import   │
  T1 (agent):  W2-R2 TDD-Functional.Movement.* ┐│  agent-side, parallel
               W2-R8 metrics + camera recorders ││
  T2 (agent):  W2-R3 TDD-Functional.Combat.*   ┘│
        │                                         │
        ▼                                         ▼
[W2 ACCEPTANCE] — every W2 deliverable verified with evidence:
   M1 candidate AC-01…13 evidence · Adanna V3 imported+verified ·
   CH01 greybox built+verified · combat/Windows/content integration verified ·
   Windows parity run 1
        │   (W2 / Stage C EXITS — ledger row + 8-point note; no acceptance on code-presence/build-pass)
        ▼
[W3 — M1 GATE] — three cold Mac runs: AC-01…31 + M1.32–35
   WP-1 (map, if not already done in W2-R1) · WP-2 (functional movement) ·
   WP-3 (in-engine unit movement) · WP-4 (first-playable M1-P1…P6 + 3 cold runs)
        │   (M1 EXITS — ledger row)
        ▼
[CHECKPOINT A (end W4)] — M1 + M2 gates exited · playable core loop
   (movement → traversal → combat vs dummy/archetype → death → respawn) ·
   2-machine verification (Mac + Windows CI) · save/load smoke ·
   no P0/P1 · 8-point report · owner go/no-go on W5–8 scope
```

**Sequencing rule:** W2 acceptance is a **hard gate** before the W3 M1 gate. WP-1 (test map) is shared between W2-R1 and the W3 gate — authoring it in the W2 phase satisfies both. No W2 deliverable is renamed as W3 work, removed, or accepted without Unreal verification evidence. No AC is weakened.

---

## C. Immediate Execution Queue

The next highest-priority tasks, who starts each, what "done" means, and the required evidence.

| # | Task | Starter (owner) | Completion definition | Required evidence |
|---|---|---|---|---|
| 1 | **P-09 — Author `L_TDD_Test_Movement` (11 zones) on the Mac** | **OW** (Mac editor), T1 spec support | Map committed with all §7 zones + `PlayerStart`s + spec dimensions; loads clean | Map asset + `TDD.M1.Map.TestMapLoads` green in train |
| 2 | **WP-3 — `TDD-Unit.Movement.*` in-engine tests (AC-22…26, 19)** | **T1** (starts now, no map needed) | State/buffer/coyote/root-motion/dodge-math unit tests written and green | Owner-Mac train `TDD_RESULT` lines |
| 3 | **M1-S6 — Enhanced Input migration (AC-20…23, 27)** | **T1** (starts during map authoring) | Character on Enhanced Input actions/contexts; buffer/coyote/parity green | Owner-Mac train + device-parity matrix |
| 4 | **M1-S7 — Metrics harness `TDD.Movement.Report`** | **T1** | CSV schema + recorder + dashboard; overhead ≤ 0.05 ms | Committed CSV per run; AC-28 Insights capture |
| 5 | **WP-2 — `TDD-Functional.Movement.*` (AC-01…13, 19–21, 27, 29)** | **T1** (gated on #1) | Each named test green against the map zones | Owner-Mac train `TDD_RESULT` + 100-run CSV |
| 6 | **M1-S5 — Camera 5-criteria recorder (AC-14…18)** | **T1** (gated on #1 corridors) | All five criteria green over corridor sweeps | Owner-Mac train + `TDD.Camera.Report` capture |
| 7 | **M1-S2/M1-S4 — Floor validation + collision edges (AC-08, 21, 22, 29; M1.33)** | **T1** | Guard + edge-case tests green | Owner-Mac train |
| 8 | **M1-S8 — Mannequin/movement-clip import (Mac)** | **OW/CT** | Clips in tree; root-motion AC-26 unblocked | Import inventory + QC |
| 9 | **M1-S9 — M1-P1…P6 first-playable record** | **T1 + OW** | Record complete with metric values | Packaged-launch log + CSVs |
| 10 | **M1-S10 — M1 GATE (3 cold runs)** | **OW + TL** | 31/31 + M1.32–35, three cold runs | Three committed evidence bundles |

**Starting now (this cycle):** #2, #3, #4 (agent/T1, no map dependency) and the owner action #1 (map). #5–#10 follow as dependencies clear.

---

## D. Risk Register (W3-specific delta)

Carries forward the project `RISK_AND_BLOCKER_REGISTER.md` (B-01…B-12, R-13…R-22, DA-01…DA-10). New/embodied W3 risks below. L/I = Likelihood/Impact.

| ID | Risk | L | I | Deadline impact | Mitigation / response | Owner | Trigger & monitoring | Exit criteria |
|---|---|---|---|---|---|---|---|---|
| W3-R1 | **Test-map authoring is Mac-editor-only and on the critical path** — the single hard blocker; if the owner cannot author `L_TDD_Test_Movement` promptly, the entire M1 gate slips 1:1 | H | H | M1 gate (W3) slips entirely | Author the map **immediately** (top of queue #1); T1 pre-specifies exact zone dimensions/PlayerStarts so the owner authors once, correctly; grey materials, no art pass (it is a measuring instrument). If the map slips > 2 days, escalate to owner with the explicit schedule impact; do not substitute a weaker map | OW (author) + T1 (spec) | Map-authoring start date; map-load test | Map committed + `TDD.M1.Map.TestMapLoads` green |
| W3-R2 | **Enhanced Input migration regresses the working camera/encounter flow** — reworking input touches the character that currently passes 7/7 | M | H | Working tests break; rework consumes T1 time | Migrate incrementally behind the existing legacy bindings; keep the camera-clamp/encounter tests green as regression guards at every step; TL diff-reviews the input migration; do not land Enhanced Input and functional tests in the same batch | T1 + TL | Any of the 7 GREEN tests turning red on the migration commit | All 7 prior tests green + new Enhanced Input ACs green |
| W3-R3 | **M1 spec edge-case overrun** (196 state pairs, E1–E7 two-phase abort, 40-cell taxonomy) — the largest serial engineering block (DA-09 restated for W3) | H | M | M1 gate slips past W3; downstream 1:1 | Pure-core test-first (already agent-side green for state/buffer/dodge logic); implement `TDD-Unit.Movement.*` before world tests; TL daily review of T1; the spec's own enumerated tests are the acceptance set (no scope growth) | T1 + TL | M1-S3/WP-2 progress in ledger | M1 gate green in 3 cold runs |
| W3-R4 | **Daily-train bandwidth (DA-01)** — the Mac is the sole UE verification authority; the map + the new functional suites all queue on the owner's 60 min/day | H | H | Every new suite queues; W3 slips | Keep the train one-command; batch the new `TDD-Functional.Movement.*` tests so they run in one train pass; pre-triage failures; if a day is lost, no new work enters until green | OW | Daily train status line | Queue depth ≤ 1 day through the M1 gate |
| W3-R5 | **Root-motion AC-26 blocked on the mannequin/clip import (M1-S8)** — content-side, Mac step pending | M | M | AC-26 unverifiable; M1 gate blocked on one AC | Import movement clips V1 (46/46 source PASS) on the Mac in parallel with WP-2; labelled interim per Rule 5; if import slips, record the specific AC blocked (no waiver) | OW/CT | M1-S8 import status | Clips in tree + `RootMotionAppliesToCapsule` green |
| W3-R6 | **Reproducibility (AC-31)** — three cold runs must be identical within tolerance; flaky timing/camera tests fail the gate | M | M | M1 gate fails on a flaky run, not a real defect | Pin the test map + deterministic inputs (gauntlet CSV, F-02); record frame-rate cap/vsync in CSV headers (spec §3.8); classify any flake (timing vs real) before re-running; never lower tolerance to pass | T1 + OW | Variance across the 3 cold runs | 3 runs identical within tolerance |
| W3-R7 | **Scope-creep pressure mid-W3** (adding content/features "to use the window") | M | H | Critical path erodes while looking green | SA register is the only scope-change mechanism (ROADMAP Rule 9); TL refuses unregistered scope in merge review; W3 is strictly the M1 gate — no M2+ work enters the integration line until M1 exits | TL | Scope items in merge reviews | Zero unregistered scope merged into the M1 gate |
| W3-R8 | **Quality-erosion pressure (DA-10)** — schedule pressure to cut feel/edge-case verification | M | H | M1 gate "passes" but is mediocre | Rule 6 enforced at merge; all ACs + manual P1–P6 feel criteria retained; no test removed; the gate is the spec's enumerated set | TL/OW/CD | Gate results + defect count | All ACs green with evidence; zero waived ACs |

**Top-3 W3 risks:** W3-R1 (map blocker), W3-R2 (input migration regression), W3-R4 (train bandwidth).

---

## E. Progress Reporting

### E.1 Actual completed work (this cycle)

- **D-W1D8-024 CLOSED.** Owner-Mac complete train at `9bf189f` GREEN: both Mac targets built; automation **7/7 PASS** including `TDD.M1.Player.CameraPitchClamp` (the audit #3 frozen-`GFrameCounter` fixture fix is verified — the pawn ticks and clamps on every tick). Pure suites 6/6 (883 assertions) PASS; PureRunnerContract + WindowsCISafety + LedgerStatusTests 10/10 PASS. Evidence `Saved/BuildEvidence/20261121T170504Z`. `DEFECT_REGISTER.md` Evidence cell + `QUALITY_LEDGER.md` closure row committed.
- **W2 (Stage C) exit audit performed** (`W2_EXIT_AUDIT.md`). Audited all four W2 deliverables against the original roadmap with commit evidence and actual Unreal verification status. **Verdict: W2 is NOT complete and NOT accepted.** M1 candidate preparation (AC-01…13), Adanna V3 in-engine import, CH01 greybox map build, combat functional integration, and Windows CI are PREPARED / IN PROGRESS / NOT EXECUTED; the Mac-side verification steps have not run. The remaining W2 work (W2-R1…R8) is now the immediate priority.
- **W3 delivery plan produced + sequencing corrected** (this document, v1.1), grounded in the W2 audit, the WBS v2.0, and the M1 spec v1.4 (AC-01…31 + M1.32–35).

### E.2 Current blockers

1. **W2 is not accepted — remaining W2 work is the immediate priority** (see `W2_EXIT_AUDIT.md`). The Mac-side W2 steps (Adanna V3 import + BP wiring, CH01 greybox map build, content in-engine integration) and the agent-side functional test suites (`TDD-Functional.Movement.*`, `TDD-Functional.Combat.*`) are not yet executed/verified.
2. **`L_TDD_Test_Movement` map authoring (W2-R1 / W3-R1)** — Mac-editor-only, hard blocker for all `TDD-Functional.Movement.*` ACs. Shared between W2 and the W3 gate; author once in the W2 phase. **Owner action required: author the map.**
3. **Reference PC / Windows CI (B-03/DA-03, W2-R6)** — Windows CI bring-up + parity run 1 not executed; a W2 acceptance item and a Checkpoint-A (W4) dependency.

### E.3 Verification evidence (actual verification level)

| Level | Status | Basis |
|---|---|---|
| Static checks (agent-side pure-core, build_readiness, runner contract, CI safety, ledger) | **VERIFIED in-sandbox** | `Tools/tests/pure/*`, `Tools/engine/build_readiness.py` — 6/6 suites (883 assertions), 0 blockers |
| Unreal compilation | **NOT verified in-sandbox** — reported from owner-Mac | `9bf189f` GREEN: both Mac targets built (owner-Mac authority, ADR-0012) |
| Runtime / automation | **NOT verified in-sandbox** — reported from owner-Mac | `9bf189f` GREEN: automation 7/7 PASS |
| W2 (Stage C) acceptance | **NOT accepted** | `W2_EXIT_AUDIT.md`: 3 of 4 W2 deliverables PREPARED/NOT-IMPLEMENTED; combat functional + Windows CI + content NOT verified in-engine |
| M1 gate (AC-01…31 + M1.32–35, three cold runs) | **NOT exited** | No test map; functional/unit movement test layer not yet implemented; three cold runs not executed |

**Honest statement:** static checks are not Unreal compilation; compilation is not runtime; a single GREEN train is not the three-cold-run M1 gate, and it is **not** W2 acceptance. The M1 gate remains the open W3 objective, and **W2 acceptance is a hard prerequisite gate before it.**

### E.4 Remaining distance (corrected: W2 first, then W3)

**W2 is not accepted; it is the immediate priority.** The remaining distance, in order:

1. **Remaining W2 work (W2-R1…R8, parallel):** author `L_TDD_Test_Movement` + build CH01 greybox + Adanna V3 import/BP/skeleton verification + content in-engine integration (Mac sessions, batched); implement `TDD-Functional.Movement.*` and `TDD-Functional.Combat.*` + metrics/camera recorders (agent-side, T1/T2, parallel); Windows CI bring-up + parity run 1 (T3/OW).
2. **W2 acceptance:** every W2 deliverable verified with Unreal evidence; W2/Stage C exits (ledger row).
3. **W3 M1 gate:** WP-1 (map, if not already done in W2-R1) → WP-2 (functional movement) → WP-3 (in-engine unit movement) → WP-4 (first-playable M1-P1…P6 + three cold runs). Enhanced Input migration (M1-S6) and metrics skeleton parallelisable during map authoring.
4. **Checkpoint A (W4):** M1 + M2 gates exited, playable core loop, 2-machine verification, save/load smoke, no P0/P1, 8-point report.

Critical path: **W2 work → W2 acceptance → W3 gate → Checkpoint A**. No AC is waived, no W2 deliverable is renamed as W3 work, and no test is removed to shorten this path.

### E.5 Next status cadence

- **Daily:** owner-Mac train one-liner (auto-posted) per `run_daily_train.sh`; TL triages failures (focused root-cause, consolidated correction — no speculative patching).
- **Per merge batch:** ledger row (TL).
- **At M1 gate:** three-cold-run evidence bundles + 8-point checkpoint report; owner go/no-go for the W4/Checkpoint-A scope.

---

*This plan is the single authoritative W3 execution record. It changes no AC, removes no test, and weakens no quality gate. GitHub (this branch) is the source of truth; the owner Mac remains the Unreal build/runtime verification authority.*
