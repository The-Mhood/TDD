# C-05 tranche 1 — implementation and test mapping

**Document ID:** `TDD-IMPL-C05-TRANCHE1-001`
**Date:** 2026-11-18 UTC
**Author:** Agent 1 (implementation lead)
**Status:** **mapping only — `NOT IMPLEMENTED`, `NOT RUN`.** 0 of 67 acceptance cases executed. Every case below keeps its contract status `PROPOSED / NOT RUN`.

---

## 1. The tranche, as directed

**17 cases:** `T-C05-01` … `T-C05-10` (suites A and B) and `T-C05-21` … `T-C05-27` (suite E).
**Deferred:** `T-C05-11` — held until **TD-06** (B-1) resolves the clock axis, because the case compares timestamped values on an axis that is not yet owned.

The case identities, suites and obligation references below are transcribed from `A1-C05-S4.3.11` §13.2's catalogue; **no case text was amended.**

## 2. Implementation mapping

| Case | Suite | Obligation | What the case must show | Proposed home module | Test kind | Automation name (proposed) | Blocked by |
|---|---|---|---|---|---|---|---|
| `T-C05-01` | A | `TN-P-12` | deterministic fixture: identical inputs produce an identical sequence | `TDDCore` (types) + `TDDTests` (harness) | functional | `TDD-Functional.C05.Determinism` | **B-1 (clock)** for the time component; ordering component unblocked |
| `T-C05-02` | A | `TN-C-01` | equal revision is discarded | `TDDCore` | unit | `TDD-Unit.C05.Revision.Equal` | **B-4** (value-type freeze) |
| `T-C05-03` | A | `TN-C-01` | lower revision discarded; the consumer never moves backwards | `TDDCore` | unit | `TDD-Unit.C05.Revision.Monotonic` | **B-4** |
| `T-C05-04` | A | `TN-R-02` | `false` for a closed instance | `TDDCore` | unit | `TDD-Unit.C05.ReadSurface.Closed` | **B-4** |
| `T-C05-05` | A | `TN-R-02` | `false` for an instance never opened | `TDDCore` | unit | `TDD-Unit.C05.ReadSurface.NeverOpened` | **B-4** |
| `T-C05-06` | A | `TN-P-11` | pull answers from live state at call time | `TDDWorld` (state) + `TDDCore` (interface) | unit | `TDD-Unit.C05.Pull.LiveState` | **B-4** |
| `T-C05-07` | B | `TN-P-01` | `Opened` precedes every other message | `TDDAI` (producer) + `TDDCore` (message) | unit | `TDD-Unit.C05.Lifecycle.OpenedFirst` | **B-4** |
| `T-C05-08` | B | `TN-C-02` | baseline fires no entry | `TDDCore` | unit | `TDD-Unit.C05.Entry.BaselineSilent` | **B-4** |
| `T-C05-09` | B | `TN-C-02` | pull-derived baseline and `Opened` baseline are the same case | `TDDCore` | unit | `TDD-Unit.C05.Entry.BaselineEquivalence` | **B-4** |
| `T-C05-10` | B | `TN-C-03` | entry at most once per phase | `TDDCore` | unit | `TDD-Unit.C05.Entry.OncePerPhase` | **B-4**, **B-11** if the phase set includes status priority |
| `T-C05-21` | E | `TN-P-03` | exactly one `Closed`, terminal | `TDDCore` + `TDDAI` | unit | `TDD-Unit.C05.Closure.Single` | **B-4** |
| `T-C05-22` | E | `TN-P-04` | every cancellation path closes | `TDDCore` + `TDDAI` | unit | `TDD-Unit.C05.Closure.CancellationPaths` | **B-4** |
| `T-C05-23` | E | `TN-P-05` | teardown invalidates before the producer dies | `TDDCore` + `TDDWorld` | functional | `TDD-Functional.C05.Teardown.InvalidatesFirst` | **B-4** |
| `T-C05-24` | E | `TN-P-06` | stream-out is scoped to its own instances | `TDDWorld` | functional | `TDD-Functional.C05.StreamOut.Scoped` | **B-4**, **B-1** (world-time scoping) |
| `T-C05-25` | E | `TN-C-06` | removal is closure, not an error | `TDDCore` | unit | `TDD-Unit.C05.Removal.IsClosure` | **B-4** |
| `T-C05-26` | E | `TN-P-02` | ids are never reused | `TDDCore` | unit | `TDD-Unit.C05.Ids.NoReuse` | **B-4** |
| `T-C05-27` | E | `TN-P-09` | no message for a closed or never-opened instance | `TDDCore` + `TDDAI` | unit | `TDD-Unit.C05.Lifecycle.NoMessage` | **B-4** |

**Count check:** 10 (suite A: `01`–`06`; suite B: `07`–`10`) + 7 (suite E: `21`–`27`) = **17**. `T-C05-11` excluded as deferred. **0 implemented, 0 compiled, 0 executed.**

## 3. Why the tranche is mapped but not written

**The public surface these cases test is exactly what B-4 (TD-12) has not frozen.** `TN-C-01`, `TN-C-02`, `TN-C-03`, `TN-C-06`, `TN-R-02`, `TN-P-01`…`TN-P-06`, `TN-P-09`, `TN-P-11`, `TN-P-12` are all assertions about *value types, the resynchronisation type and the read interface* — the three things the contract says cannot be frozen until the contract-layer owner is named. Writing those structs now would mean choosing a shape and calling it the contract.

**What is genuinely unblocked and was done instead:** the project itself (`TDD.uproject`, 9 modules, targets, config), the module boundaries that the obligations will live inside, the automation-test foundation, and the static verifiers. **What is blocked** is behaviour that encodes a contract decision: the clock axis, the revision type, the message type and the resynchronisation routing.

## 4. Fixtures — designed, not yet coded

| Fixture | Purpose | Depends on |
|---|---|---|
| `FTDDC05FixtureClock` | deterministic, manually-advanced time source so every timing assertion is reproducible | **B-1 (TD-06)** — cannot be written against an axis nobody owns |
| `FTDDC05FixtureRevisions` | monotonic / equal / lower revision sequences for `T-C05-02`, `-03` | **B-4** |
| `FTDDC05FixtureInstance` | opened / never-opened / closed / streamed-out lifecycle states for `TN-R-02`, `TN-P-03`…`-06`, `TN-C-06` | **B-4** |
| `FTDDC05FixtureMessages` | captures the ordered message log so `Opened`-first and no-message-after-close are assertable | **B-4** |
| Float tolerance constant | `INV-2` comparisons (B-14) — proposal recorded in the dependency matrix, outside this tranche | **B-14** |

## 5. Traceability and discipline

- **Test naming** follows MEAD §15 (`TDD-Unit.*`, `TDD-Functional.*`); unit tests live in their module behind `#if WITH_DEV_AUTOMATION_TESTS`, functional tests in `TDDTests` (MEAD §3.2).
- **Every case keeps `PROPOSED / NOT RUN`** until a build executes it. The repository's own rule is that a case is marked executed only with machine evidence attached; there is no engine here, so there is none to attach.
- **No obligation, suite or case identity changes.** 43 obligations, 18 suites, 67 cases remain exactly as `A1-C05-S4.3.11` states them; this document adds a mapping, not a catalogue entry.
- **`T-C05-11` stays deferred** and is not renumbered, re-scoped or dropped.
