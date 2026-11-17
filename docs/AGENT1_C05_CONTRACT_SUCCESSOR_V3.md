# Agent 1 — C-05 Successor `A1-C05-S3`

**Response ID:** `TDD-A1-C05-SUCCESSOR-003`
**Version:** 3.0 — successor to `A1-C05-S2` v2.0; current C-05 position
**Date:** 2026-11-17 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Scope:** **Agent 2's nine review conditions and the eleven numbered corrections addressed to me** — no other change. No history mechanism, no event bus, no central scheduler, no new architecture layer, no alternative telegraph architecture.
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no C++, no Unreal project, no API or contract freeze, **no MEAD selection**, no signature, no merge, no M0 claim. **C-05 remains proposed, unsigned and unfrozen; U-07 remains open.**

---

## 0. Provenance and scope lock

### 0.1 What this revision answers

| Field | Value |
|---|---|
| **Review answered** | `TDD-A2-REVIEW-A1C05-S2-001` v1.0, Agent 2 — `Docs/AGENT2_REVIEW_A1C05_S2_V1.md`, 686 lines, read in full |
| Review commit | `ac498cee9e1c9bfa051008633978f943a6360826` (`arena/5dde91a4-tdd`) |
| **Blob reviewed by Agent 2** | **`bf6c8fb3ddf3152d1627d3b6471278f57fc82541`** — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V2.md` at `e5ddad6965e06b179061d8cebb6ffecf59829224` |
| My predecessor | `A1-C05-S2` v2.0 — same blob, same commit; **preserved unmodified** |
| Predecessor of that | `A1-C05-S1` v1.0 at `2bb729f2cbd525e3cd7f5f5d46b3b9cc72c803d0`, blob `dcec9e1ae3efd4651c290636e8a4d6623603dc83`; **preserved unmodified** |
| Agent 2's submission (requirements source for the consumer analysis) | `A2-C05-1.0` at `3ac438b32fcd73ceb22dcd81385356f7b8b39644`, §7.1, §7.3, §7.6 |
| Aging formula source | `A1-R4` §3.3(e) — `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md`, blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75`, lines 143–167 |
| MEAD-A — `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **not selected**; at `586152b` (`arena/5dde91a4-tdd`), blob `bd0f3afdf24736349f2045bf0ee423ee0b4e1a78`, read only |
| MEAD-B — `docs/MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **not selected**; at `1eb613f` (`arena/c64fc525-tdd`), blob `1e8d1bd1b223c364c02464f6036e3f9ee9a9b0a7`, read only |
| MEAD-C — `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **none selected**; this branch, blob `f49354631c86601e9311865901bf1fcd44846d89`, read only |

### 0.2 Agent 3's S2 reassessment is **not available**, and I do not pretend otherwise

The instruction names `docs/AGENT3_A1_C05_S2_BOUNDED_REASSESSMENT_V1.md` on `arena/c64fc525-tdd`. **That file does not exist at that branch's tip `1eb613f`.** Checked three ways at the time of writing:

```
$ git ls-remote origin refs/heads/arena/c64fc525-tdd
1eb613f3cff8556c911af2b77eb3af73f3361ea4
$ git ls-tree -r --name-only origin/arena/c64fc525-tdd | grep -i c05
docs/AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md
docs/AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md
$ gh api repos/The-Mhood/TDD/contents/docs?ref=arena/c64fc525-tdd --jq '.[].name' | grep -i A3
AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md
AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md
```

**Consequences, stated plainly:** this revision is driven by Agent 2's review only. I do not claim that Agent 3's findings against S2 — whatever they are — are addressed, closed, or even known. Two of Agent 2's nine conditions (`5` and `6`) touch areas Agent 3 also assessed in the S1 round (resync semantics, MEAD neutrality); my changes there are made against **Agent 2's** statement of the problem, and Agent 3 may assess them independently. **Requesting that reassessment is part of the handoff (§18.2), not something this document can substitute for.**

### 0.3 What Agent 2 found, and what I am doing about it

Agent 2 returned **two DISAGREE and three AGREE WITH CONDITIONS**, with **nine narrowly necessary corrections** and 0 architectural objections. Their own summary of the delta is one sentence, and it is the frame for this revision: *"My two DISAGREE verdicts are not about the corrections. They are about three fields and one invariant sentence."*

They are right about both. `INV-1` as I wrote it in S2 put an **aging field inside an equality invariant**, which makes every conforming producer a violator on every frame; and I assigned four consumers to a snapshot that does not carry the two identity fields three of them need. Both are my errors, both are narrow, and neither requires reopening the recovery model.

**What I am not doing:** I am not re-arguing the verdicts, not treating the review as a rejection of the S2 corrections (Agent 2 states they are correct, and calls the complete-snapshot rule *"the same insight generalised one path over"*), and not converting any condition into a TD decision. One condition has a dependency I cannot close myself and is marked `BLOCKED BY DEPENDENCY` (§14.2, B-11).

### 0.4 Scope lock — what is preserved verbatim

| Preserved | Where |
|---|---|
| Per-instance, no-history pull recovery | `C05-2.4`, `C05-2.6` `RS-1`/`RS-2`/`RS-3`, §4.4, §4.6 |
| `StateRevision` and complete-snapshot messages | `C05-2.2`, `C05-2.3`, `TN-P-07`, `TN-P-13`, `TN-P-14` |
| `TM-1` terminal close, `EN-3` resync, lifecycle semantics | §4.6, §4.7 |
| MEAD neutrality — no module, no class, no candidate selected | `C05-2.2` header, §5, §13 DV-9 |
| Arbitration separated from telegraph production | `C05-6.1`, `TN-A-01`, `TN-A-02`, §9.2 |
| Conditional X-1 — global enumeration still out of scope | `TN-R-03`, §14.1 B-5 |
| The ownership split, **except** the wording Agent 2's conditions 7–9 require | `C05-7.2` rows 5–6, `C05-7.4` |
| Every earlier document, byte for byte | §17 |

**Not introduced, at all:** a history buffer, a revision log, a replay path, an event bus, a central scheduler, a new layer, a second query surface, a MEAD choice, a signature, a freeze, C++ code, or any claim of runtime validation.

---

## 1. The eleven corrections at a glance

Agent 2 grouped their findings into **nine conditions**; the instruction to me numbers **eleven corrections** and adds two that are implied by the same findings. Each row below is expanded in §2.

| # | Correction | Agent 2 condition | Clause affected |
|---|---|---|---|
| **1** | `INV-1` no longer requires `RemainingLocalSeconds` to be identical at equal revision — it is a derived, time-dependent value | C4a | `C05-2.6` `INV-1` |
| **2** | The aging formula `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` is stated in the contract, and the field classes are enumerated | C4a | `C05-2.6` `INV-1`, `INV-2` |
| **3** | `TN-R-05` aligned to the corrected invariant | C4b | `TN-R-05` |
| **4** | `T-C05-46` no longer demands byte-identical aging values | C4b | `T-C05-46` |
| **5** | Simultaneous phase + retime changes: deterministic publication order, revisions `n+1` then `n+2`; `EX-5` rewritten as three explicit cases | C4c | `C05-2.9` `PO-1…PO-4`, `TN-P-15`, `EX-5` |
| **6** | The directory is explicitly not a scheduler — no timing, no scheduling, id→producer and liveness only | C1 | `C05-2.5` `DN-1`, `TN-R-06` |
| **7** | `DN-1` deregistration covers `Closed` **and** producer invalidation, whichever occurs first | C2 | `C05-2.5` `DN-1` |
| **8** | Two phase transitions within one frame: two transitions, two revisions, two messages, in authored order; never collapsed | C3 | `C05-2.9` `PO-4`, `TN-P-16` |
| **9** | `WindowKey` and `AttackTag` carried in the snapshot with a per-consumer justification; `Resynchronised` declared as a contract type; montage selection defined as a trigger | C5, C6, C8 | `C05-2.2`, `C05-2.6` `EN-3`, `C05-7.2` row 5, `TN-C-11`…`TN-C-13`, §6 |
| **10** | VFX responsibility scoped to timing and phase; world placement/attachment resolved outside C-05 | C7 | `C05-7.2` row 5, `TN-C-12`, §6.2 |
| **11** | Agent-named assignments in `C05-7.2` reconciled with role-named implementer columns; a document check verifies the mapping rather than mere population | C9 | `C05-7.4`, §13 DV-11 |

**Three non-condition defects Agent 2 also reported, all fixed:** the stray `*` in `TN-P-13`'s cell (Q1-a); the inaccurate count in DV-8's result cell (§13, DV-8 now reports a count produced by a stated command); and the missing dependency on `C05-6.3`'s carriers being defined only in S1 (§14.2, B-11). Two provenance remarks they raised (§16 placeholders, the `d32660f` citation) were **already remediated** before their review was written and are recorded in §2 as closed, not reopened.

---

## 2. Correction ledger — every finding, its clause, its reason, its tests

Traceability runs both ways: Agent 2's condition, the instruction's correction number, the clause changed, the nature of the change, why, and the acceptance cases that move.

| A2 | Instr. | Finding (Agent 2's words, abridged) | Clause changed | Nature of correction | Why | Tests affected |
|---|---|---|---|---|---|---|
| **C1** | 6 | *"`C05-2.5` must state why the directory is not the second scheduler my §7.1 warned against"* | `C05-2.5` `DN-1`, new `TN-R-06` | **Added** a four-part negative definition to `DN-1` and a read-surface obligation forbidding the directory from holding timing, ordering, scheduling or emitting | Their §7.1 said "no central telegraph director — it would become a second scheduler competing with StateTree". A reader should not have to infer the rebuttal from a negative field list | T-C05-61, T-C05-28, T-C05-29 |
| **C2** | 7 | *"`DN-1` should say register on `Opened`, deregister on `Closed` or producer invalidation — whichever occurs first, matching `RM-1`'s own list"* | `C05-2.5` `DN-1` | **Rewritten** trigger list; explicitly composes with `TN-P-06`, `TN-P-05` and expired-handle liveness | A streamed-out enemy need not emit `Closed`; the trigger list looked exhaustive and was not | T-C05-61, T-C05-23, T-C05-24 |
| **C3** | 8 | *"`TN-P-13` needs a sentence on collapsed boundaries: two phase transitions within one frame are two revisions… it must publish both"* | `C05-2.9` `PO-4`, `TN-P-16` | **New clause and obligation** | Montage section boundaries can collide in one frame; "exactly one" per transition did not say what one transition is in that case | T-C05-52, T-C05-53 |
| **C4a** | 1, 2 | *"`INV-1` as written is false under ordinary passage of time… it includes an aging field in an equality invariant"* | `C05-2.6` `INV-1` (rewritten), new `INV-2`, `TN-P-17`, `TN-C-10` | **Rewrote** the invariant over an explicitly enumerated **versioned** field set; added the aging law as `INV-2`; stated the observation-instant field set and how it is evaluated | Their §3.2 is decisive: two pulls at one revision returned `0.2000` and `0.1800`. An obligation whose compliant implementation is indistinguishable from its violation is not implementable | T-C05-46, T-C05-54, T-C05-55, T-C05-56, T-C05-62 |
| **C4b** | 3, 4 | *"fix `TN-R-05` and `T-C05-46` to match"* | `TN-R-05`, `T-C05-46` | **Both corrected** to assert versioned-field identity plus formula consistency, not byte identity | A byte-identity assertion across an aging field cannot be satisfied by any conforming producer | T-C05-46, T-C05-49 |
| **C4c** | 5 | *"`EX-5` leaves same-frame ordering ambiguous for case (c)… two conforming producers can publish `(phase, timing)` or `(timing, phase)`"* | new `C05-2.9` `PO-1…PO-3`, `TN-P-15`, `EX-5` rewritten | **New ordering clause** fixing the canonical sequence; three-case example | Without a stated order the same frame yields two different observable sequences, and which message lands at `n+1` decides whether entry fires | T-C05-51, T-C05-44 |
| **C5** | 9 | *"`Resynchronised` is named and never declared… neither is checkable without knowing whether it is a delegate, a return code or a consumer-internal callback"* | `C05-2.2` (new type), `C05-2.6` `EN-3`, `TN-C-09` | **Declared** as a contract-layer value type plus delegate signature; delivery explicitly consumer-local, no transport | Two S2 cases asserted on an undeclared artefact; the tests were unbuildable as specified | T-C05-45, T-C05-50, T-C05-57 |
| **C6** | 9 | *"`WindowKey` and `AttackTag` are absent, and they are the two Required fields I cannot do without… a resync that says Active without saying unblockable is a resync my AI cannot act on"* | `C05-2.2` (two fields added to `FTDDTelegraphSnapshot`), `TN-C-11`, §6.1 | **Carried**, after a per-consumer necessity analysis (§6.1) that also rejects the two alternatives | Three of four named consumers need identity; blockability is the one decision a resync into `Active` exists to enable | T-C05-57, T-C05-58 |
| **C7** | 10 | *"scope my VFX consumer to 'VFX marker timing and phase', and state that placement is resolved from `SourceEntityId` outside the contract"* | `C05-7.2` row 5, `TN-C-12`, §6.2 | **Narrowed** the assignment; placement declared outside C-05 | The assignment promised a surface the contract deliberately does not carry (no transforms, `C05-2.8`) | T-C05-59 |
| **C8** | 9 | *"montage selection is a C-05 trigger, not a C-05 consumer capability"* | `C05-7.2` row 5, `TN-C-13`, §6.2 | **Split** the responsibility: trigger in C-05, asset selection outside, keyed by `WindowKey` | C-05 carries phase and timing, not asset references; the assignment and the surface disagreed | T-C05-60 |
| **C9** | 11 | *"add a document check that maps each implementer-cell role to the agent `C05-7.2` assigns it, and assert agreement"* | new `C05-7.4` role vocabulary, §13 DV-11 | **Reconciled** the two vocabularies with an explicit role→agent table and a mechanical check | `DV-3` checked that the column was filled, not that it agreed with the ownership table | all 38 obligation rows (DV-11) |
| Q1-a | — | stray `*` in `TN-P-13`'s cell | `TN-P-13` | **Removed** | cosmetic, renders as a literal asterisk | — |
| Q1-b | — | `TN-P-07`/`TN-P-13` deliberate redundancy | — | **No action** — Agent 2 marked it good | the footnote documents the redundancy on purpose | — |
| Q1-c | — | `C05-7.2` names agents, §6–§8 name roles | `C05-7.4`, DV-11 | **Merged into C9** | same finding, one fix | as C9 |
| — | — | DV-8's stated count (10) was wrong; actual 16 occurrences | §13 DV-8 | **Corrected** — the check now prints the count its command produces | A check that misreports its own instrument is worse than no check | — |
| — | — | `TN-C-07` depends on `C05-6.3`'s carriers, defined only in S1 | §14.2 B-11 | **Added** as a visible dependency | It inherits `PROPOSED — NOT FROZEN` and the `C-04-4` coupling | T-C05-35 … 39 |
| — | — | §16 `PUB_COMMIT`/`PUB_BLOB` placeholders; `d32660f` citation | §17 | **Already remediated** before the review was written; verified at `d24546d`; nothing reopened | Agent 2 verified the tip diff as provenance-only | — |

**Nothing in this ledger reopens a resolved finding.** `F1`–`F6` of `A1-C05-S1`, `X-1`, the arbitration boundary and the no-history recovery model are untouched; `A2R-31`…`A2R-35` keep their S1 dispositions.

---

## 3. The corrected revision model

### 3.1 The defect Agent 2 found, restated exactly

S2's `INV-1` said two observations at the same `StateRevision` are *"identical in every pull-visible field — phase, all timing endpoints, `ProducerRate`, `RemainingLocalSeconds`"*. But `RemainingLocalSeconds` is not a stored field; it is a **function of the observation instant**, defined by the aging rule at `A1-R4` §3.3(e). Agent 2's arithmetic:

| Frame | `Axis(t) − AxisNow` | `RemainingLocalSeconds` | `StateRevision` |
|---|---|---|---|
| 0 | 0.0 | 0.2000 | 1 |
| 1 | 0.2 | 0.1900 | 1 |
| 2 | 0.4 | 0.1800 | 1 |

Two pulls at revision 1 return `0.2000` and `0.1800`. **The producer is conforming; the invariant was wrong.** The same error propagated to `TN-R-05` and `T-C05-46`, and it collided with `TN-P-11` ("pull answers from live state at call time"), which no correct implementation can reconcile with a frozen `RemainingLocalSeconds`.

### 3.2 Two field classes, named so the invariant can be stated over one of them

> **VF — versioned fields.** The fields a `StateRevision` versions, and the only fields `INV-1` constrains: **`Phase`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`, `ProducerRate`, `WindowKey`, `AttackTag`.** Instance identity (`AttackInstanceId`, `SourceEntityId`) is fixed for the instance's lifetime and cannot vary at all.

> **OF — observation-instant fields.** The fields that describe **when** the snapshot was taken, not **what** the state is: **`AxisNow`, `RemainingLocalSeconds`.** They are determined by the observation instant and the versioned fields, by `INV-2`, and by nothing else.

**The split is not a convenience, it is the contract's own semantics.** A versioned field is authored or applied by the producer under `RM-1`'s lifecycle; an observation-instant field is computed from the axis at the moment of the pull or the emission. Grouping them was the S2 defect. The division is exhaustive: every field of `FTDDTelegraphTiming` and `FTDDTelegraphSnapshot` is in exactly one class, and `StateRevision` itself is in neither — it is the counter that indexes `VF`.

### 3.3 `INV-1`, corrected

> **C05-2.6 INV-1 (corrected).** For a given `AttackInstanceId`, two observations carrying the same `StateRevision` are **identical in every versioned field** (`VF`: phase — `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis` — `ProducerRate`, `WindowKey`, `AttackTag`). They are **not** required to be identical in the observation-instant fields (`OF`): `AxisNow` and `RemainingLocalSeconds` describe the instant of observation and are governed by `INV-2`. A producer that publishes or answers at a revision with different `VF` content is in violation (`TN-P-07`).

**What is preserved:** `Phase` is a versioned field, so Agent 3's original defect stays closed — a phase change at an unchanged revision is still unrepresentable, and equal-revision discard still cannot lose a phase change.
**What is fixed:** a producer that ages its own remaining time correctly is no longer diagnosed as a violator on every frame.

### 3.4 `INV-2` — the aging law, stated in the contract

> **C05-2.6 INV-2 (new).** Within one snapshot, the observation-instant fields are consistent with the versioned fields at that snapshot's own `AxisNow`:
>
> ```
> RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)
> ```
>
> where `PhaseEndAxis` is the endpoint of the current phase (`WindupEndAxis` in `Windup`, `ActiveEndAxis` in `Active`, `RecoveryEndAxis` in `Recovery`). A consumer holding a snapshot ages it by the same law in the form established at `A1-R4` §3.3(e):
>
> ```
> R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)
> ```
>
> with `R0` the snapshot's `RemainingLocalSeconds` and `AxisNow` its `AxisNow` stamp. **Never by wall-clock elapsed, never by the consumer's own `CustomDilation`.**

**These two forms are the same function, and that is the consistency proof the instruction asks for.** Substituting the snapshot's own value, `R0 = (PhaseEndAxis − AxisNow) × Rate`, into the consumer form gives `(PhaseEndAxis − AxisNow) × Rate − (Axis(t) − AxisNow) × Rate = (PhaseEndAxis − Axis(t)) × Rate` — algebraically identical to producer form. So the producer's obligation (`TN-P-17`) and the consumer's obligation (`TN-C-10`) are two views of one equation, not two independent rules that could drift. The identity holds exactly while `ProducerRate` and `PhaseEndAxis` are fixed, which is precisely what one revision guarantees; a rate change is a `Retimed` (`TN-P-08`) and a phase change is a `PhaseChanged` (`TN-P-13`), and each re-anchors both forms at a new revision.

### 3.5 Why equal-revision discard still loses nothing

This is the property S2's `INV-1` existed to justify, and it must survive the correction. It does, and the argument is now explicit rather than assumed:

1. A discarded equal-revision observation can differ from what the consumer holds **only** in `OF` — `AxisNow` and `RemainingLocalSeconds` (by `INV-1`).
2. `OF` carries no state: it is a deterministic function of `VF` and the observation instant (`INV-2`).
3. A consumer holding revision `n` can compute the `OF` values for any instant from its own snapshot by `R(t)`, using the shared axis it is already granted (`A1-R4` §3.3(a)).
4. Therefore discarding the later observation and aging the earlier one yields the **same** numbers, and the only thing discarded is a redundant recomputation.

**Contrapositive, which is the operative rule:** if the observation differs in any `VF` field — phase, an endpoint, `ProducerRate`, `WindowKey`, `AttackTag` — then the revision differs (`TN-P-07`), so the discard rule never applies to it. **A genuine state change cannot arrive at an unchanged revision.** `T-C05-62` enumerates the complete change table and asserts the correspondence; `T-C05-56` asserts the discard-then-age path is observationally equivalent, with a wall-clock-aging negative control that must diverge.

### 3.6 Simultaneous phase and retime: one canonical order

> **C05-2.9 `PO-1`.** A frame containing **only** phase transitions publishes one `PhaseChanged` per transition, in authored order, revisions `n+1`, `n+2`, … (§3.7).
> **`PO-2`.** A frame containing **only** dilation changes publishes one `Retimed` per change, in the order applied, revisions `n+1`, `n+2`, … No coalescing (`TN-P-08`).
> **`PO-3`.** A frame containing **both** publishes **all phase transitions first, in authored order, then all dilation changes, in the order applied.** One phase change plus one retime is therefore `PhaseChanged` at `n+1` followed by `Retimed` at `n+2` — never one message, never the reverse order, never a shared revision.

**Why this order, and not the other one:** (a) the phase transition is a **lifecycle fact** — the state the retime adjusts is the state the phase names; a retime published first would describe the timing of a phase the consumer has not been told about. (b) Within one frame the producer's internal application order is **not observable** at frame granularity, so leaving it to the producer would let two conforming producers emit different sequences for identical gameplay — the exact non-determinism a contract exists to remove. (c) It is the safer order under loss: the first message of a same-frame pair already carries the correct phase, so a consumer that loses the second is phase-correct and merely needs a resync; the reverse order would leave it timing-correct and phase-wrong.

**Consequence for consumers, spelled out because it decides entry:** a consumer holding `n` that receives both messages sees a contiguous run (`n+1`, `n+2`), adopts both, fires entry once for the new phase and none for the retime. A consumer holding `n` that receives only `n+2` — the retime — sees `n+2 > n+1`, records a gap, fires no entry and raises exactly one `Resynchronisation` (`AD-2`, `EN-3`, `TN-C-09`). Both behaviours are correct and both are tested (`T-C05-51`, `T-C05-44`).

### 3.7 Two phase transitions inside one frame

> **C05-2.9 `PO-4`.** Two phase transitions occurring within one frame are **two transitions**: two increments of `StateRevision`, two `PhaseChanged` messages, published in authored order and never collapsed into one revision or one message. A producer whose authoring model can produce two transitions in one frame — montage section boundaries landing in the same tick — **must publish both**. It may not drop the intermediate phase, merge the pair, or publish only the resulting phase.

Two consequences worth stating because they are what an implementer will hit:

- **A phase can begin and end inside one frame.** Such a phase is published twice and may never be observable through a pull at all: a pull taken after the frame returns the later phase. Consumers must not infer "this phase never happened" from a pull — a pull is current state, not history (`RS-1`, `TN-C-08`).
- **The consumer rules do not need a special case.** Receiving both messages from `n` is a contiguous run: both phases are adopted and each fires entry at most once (`EN-2`). Receiving only the second is a gap: no entry, one resync. This is `PO-3`'s arithmetic with a different number of increments, which is exactly why the ordering rule is stated as a sequence of revisions rather than as a special case per frame.

### 3.8 What the identity fields add — and what they do not

`WindowKey` and `AttackTag` are **versioned fields**, authored at `Opened` and constant for the instance's lifetime. They do not age, so they cannot repeat S2's mistake. §6.1 carries the per-consumer necessity analysis that justifies carrying them rather than resolving identity outside the contract, including the two alternatives that were considered and rejected. `AttackTag` is transported as a gameplay-tag **value**; C-05 defines no tags and registers none (`C05-2.8`).

### 3.9 What this section did not change

`AD-1` (strict-greater adoption), `AD-2` (gap flag), `EN-1` (baseline), `EN-2` (at most once per phase), `TM-1` (terminal close outside the freshness rule), `RS-1`/`RS-2`/`RS-3` (current-state recovery, no revision log, one snapshot per instance), `RM-1`/`RM-2` (removal semantics), the pull surface, the directory's content, and the producer/consumer boundary. **The correction is confined to how the invariant is stated over two field classes, and to the publication order of a frame that contains more than one change.**

---

## 4. The complete revised contract

Readable without either predecessor. `[UNCHANGED]` means the S2 text stands; `[CORRECTED]` and `[NEW]` mark this revision's edits. Every clause is `PROPOSED — NOT FROZEN`.

### 4.1 C05-2.1 — What the contract is about `[UNCHANGED]`

Telegraph timing is published by the **producer** — Agent 2 for enemy attacks, Agent 1 for the player's own attack — as an ordered message stream plus a per-instance pull, and consumed by defence and feedback consumers on both sides. The producer is the sole authority for the values it publishes. **No component in this contract retains a copy of another producer's timing block.** Producer and consumer responsibilities are allocated by activity in `C05-7.2` / `C05-7.3`, and the vocabulary of that allocation is fixed in `C05-7.4`.

### 4.2 C05-2.2 — Value types (contract-layer types; owner pending TD-12) `[CORRECTED]`

```cpp
// PROPOSED — NOT FROZEN. Owner: the cross-agent contract layer of the canonical
// architecture (TDDCore under MEAD-C; no TDDCore module under MEAD-A or MEAD-B,
// whose nearest home is a framework area with no assigned owner). See §5.
// Engine types only: FGuid, FName, FGameplayTag. No candidate-specific module.

struct FTDDTelegraphTiming
{
    // ---- OF: observation-instant fields (INV-2; differ between observations at one revision)
    double  AxisNow;                 // shared axis at this observation (emission, or the pull's call time)
    float   RemainingLocalSeconds;   // = max(0, (PhaseEndAxis - AxisNow) * ProducerRate)   [INV-2]

    // ---- VF: versioned fields (INV-1; identical for one revision)
    double  WindupEndAxis;
    double  ActiveEndAxis;
    double  RecoveryEndAxis;
    float   ProducerRate;            // ProducerRate == CustomDilation(producer) at this revision
    uint32  StateRevision;           // the counter that indexes VF. 1 on Opened; +1 on every
                                     // phase transition and every retime (PO-1..PO-4).
                                     // Renamed from TimingRevision at S2; supersedes A1-R3 §3.2
                                     // on this field only.
};

enum class ETDDTelegraphPhase : uint8 { Windup, Active, Recovery };   // closed is terminal

enum class ETDDTelegraphCloseReason : uint8
{
    Natural, Cancelled, Interrupted, ProducerInvalidated, SourceDied
};

struct FTDDTelegraphSnapshot      // what a pull returns and what EVERY message carries
{
    // identity: fixed for the instance's lifetime
    FGuid               AttackInstanceId;
    FGuid               SourceEntityId;

    // VF: versioned fields (INV-1)
    ETDDTelegraphPhase  Phase;
    FName               WindowKey;    // NEW: stable per attack definition; authored at Opened
    FGameplayTag        AttackTag;    // NEW: block / dodge / unblockable; a transported value,
                                      // never defined or registered by this contract
    FTDDTelegraphTiming Timing;       // carries StateRevision and the OF pair

    // -- equality classes used by INV-1: {identity, Phase, WindowKey, AttackTag, Timing.VF}
    // -- observation-instant: {Timing.AxisNow, Timing.RemainingLocalSeconds}
};

struct FTDDTelegraphMessage       // one struct, complete state, plus the event kind
{
    enum class EKind : uint8 { Opened, PhaseChanged, Retimed, Closed };
    EKind                  Kind;
    FTDDTelegraphSnapshot  Snapshot;      // the complete pull-visible state at emission
    ETDDTelegraphCloseReason CloseReason; // meaningful only when Kind == Closed
};

struct FTDDTelegraphResynchronisation   // NEW: declared, because TN-C-09 is normative
{
    FTDDTelegraphSnapshot LandedState;    // the state adopted across the gap; no history (RS-1/RS-2)
};

DECLARE_DELEGATE_OneParam(FTDDTelegraphOnResynchronised, const FTDDTelegraphResynchronisation&);
```

**`Resynchronised`'s status, stated once and unambiguously:** it is a **contract-layer type with normative semantics and consumer-local delivery**. C-05 fixes what it carries, when it fires and how often; C-05 defines **no transport, no subscription registry, no queue and no cross-agent delivery** — each consumer raises it in its own code, on its own delegate, for its own gap. It is therefore checkable (a delegate's invocation count is observable inside the consumer) without becoming the event bus this contract has repeatedly refused to be. Cross-agent routing, if anyone ever wants it, is a TD decision and is not proposed here (§14.2, B-12).

### 4.3 C05-2.3 — The message stream `[UNCHANGED, plus PO-3/PO-4 ordering]`

Four kinds — `Opened`, `PhaseChanged`, `Retimed`, `Closed` — each carrying the **complete snapshot** (`C05-2.3a`). `Closed` additionally carries an `ETDDTelegraphCloseReason` and is **terminal** (`TM-1`). `Opened` establishes revision 1. Ordering within a frame is fixed by `C05-2.9`.

> **C05-2.3a.** No message carries a partial aspect of the state. A consumer that receives any message holds the whole state at that revision and therefore never needs a follow-up pull to complete it — including the identity fields a per-attack consumer needs to act (`WindowKey`, `AttackTag`).

### 4.4 C05-2.4 — The pull surface `[UNCHANGED]`

```cpp
class ITDDTelegraphSource
{
public:
    // Live read of one instance the caller can name. False if not open, never opened
    // by this producer, or this producer is shutting down. Answers from live state at
    // call time (TN-P-11): AxisNow is the call's axis instant and RemainingLocalSeconds
    // satisfies INV-2 at that instant, while VF fields match the instance's current
    // revision exactly (INV-1).
    virtual bool TryGetOpenTelegraph(FGuid AttackInstanceId, FTDDTelegraphSnapshot& Out) const = 0;

    // Instances this producer currently holds open. Per-producer, bounded by that
    // producer's own concurrency. NOT global enumeration and must not be aggregated.
    virtual void GetOpenTelegraphIds(TArray<FGuid>& Out) const = 0;
};
```

There is no third method, no descriptor query and no identity lookup: `WindowKey` and `AttackTag` travel **inside** the snapshot (§6.1 explains why a second call was rejected).

### 4.5 C05-2.5 — Resolution through the directory `[CORRECTED: C1, C2]`

> **DN-1.** The contract layer exposes a resolution function mapping `AttackInstanceId` to the producer that opened it. The directory stores per instance only: the id, `SourceEntityId`, and one **weak liveness handle**. Producers **register on `Opened`** and **deregister on `Closed` or on any invalidation of that producer's instances — whichever occurs first** (`RM-1`: `Closed`, producer invalidation, unload or stream-out, death-cancel, world teardown). An entry whose handle has expired answers `false`; world teardown drops every entry. The "no actor pointers" rule applies to published value structs, not to this private liveness record. **Implementation: Agent 1, as shared support; see `C05-7.2` and `C05-7.3`.**
>
> **DN-1a — why this is not a second scheduler.** The directory holds **no timing, no phase, no revision, no window and no queue**; it **schedules nothing**, orders nothing, emits nothing and wakes nothing; it is consulted **only** to map an `AttackInstanceId` to the producer that opened it and to answer whether that producer is still alive. A component that could schedule work would need a clock and an order; this one has neither, and `TN-R-06` forbids it acquiring either. It is therefore not the central director that `A2-C05` §7.1 rejected, and Agent 2's own words are the test: their objection was to a director that *competes*, and a liveness map does not compete.

### 4.6 C05-2.6 — Adoption, entry, invariants and terminal rules `[CORRECTED: C4a, C4b, C5]`

> **INV-1 (corrected).** Two observations of one instance carrying the same `StateRevision` are **identical in every versioned field** — `Phase`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`, `ProducerRate`, `WindowKey`, `AttackTag` — and in instance identity. They are **not** required to be identical in the observation-instant fields `AxisNow` and `RemainingLocalSeconds`, which `INV-2` governs.

> **INV-2 (new).** Within any snapshot, `RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)`. A consumer ages a held snapshot as `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)`, using the shared axis and its own `ProducerRate` — never wall-clock elapsed and never the consumer's own `CustomDilation`.

> **AD-1.** A consumer adopts a snapshot only if its `StateRevision` is **strictly greater** than the revision it holds. Equal or lower is discarded silently. This applies identically to messages and pulls. **Discarding an equal-revision observation loses no state change:** by `INV-1` it can differ only in `OF`, and `OF` is recomputable by `INV-2` (§3.5).

> **AD-2.** If an incoming revision is **greater than held + 1**, the consumer records a revision gap, sets `bStateGapObserved` for that instance and keeps it set until the instance closes. The flag means: *at least one observable state change — phase, retime, or both — was missed.*

> **EN-1.** The **first** observation of an instance by a consumer establishes the baseline: the current phase is recorded as already held and **no entry hook fires** for it. An `Opened` and a pull-derived first observation are the same case.

> **EN-2.** After the baseline, a phase transition is observable **at most once** per consumer per `(AttackInstanceId, phase)`. A `Retimed` never re-fires entry — it changes timing, not phase identity. A duplicate `PhaseChanged` fires nothing.

> **EN-3 (corrected).** A snapshot adopted **across a revision gap** fires **no** phase entry for any phase not observed. The consumer raises exactly one **`FTDDTelegraphResynchronisation`** for that gap, carrying the landed snapshot (`LandedState`) and no transition history, on its own `FTDDTelegraphOnResynchronised` delegate; it must not synthesise entries for phases it did not see. The type is declared at `C05-2.2`; delivery is consumer-local, with no transport (§4.2).

> **TM-1.** `Closed` is **terminal** and is **not** subject to `AD-1`. A `Closed` whose revision equals or precedes the held revision still closes the instance. A producer does not advance `StateRevision` to announce a close.

> **RS-1.** A pull recovers the **current** snapshot of a known instance. It never reconstructs an intermediate revision.
> **RS-2.** No component retains more than one snapshot per instance. The revision counter is not a log.
> **RS-3.** A phase that opens and closes within a single frame is published as two transitions (`PO-4`) and may be unobservable through a pull. Absence from a pull is not evidence that a phase did not occur.

### 4.7 C05-2.7 — Removal `[UNCHANGED]`

> **RM-1.** An instance ceases to exist on `Closed`, on producer invalidation, on producer unload or stream-out, on producer death-cancel and on world teardown. Invalidation and teardown are not messages: they are observed as a pull returning `false` and a directory entry that no longer resolves. **Removal emits no synthesised message.**
> **RM-2.** A consumer holding state for an instance that returns `false` or no longer resolves **must** treat it as closed, release its block, fire no further entry, and raise no error.

### 4.8 C05-2.8 — What this contract explicitly does not do `[CORRECTED: C7, C8]`

No retained copy of another producer's state; no global enumeration (X-1 only); no arbitration, parry/block decision or damage application; no clock ownership (TD-06) or contract-layer home (TD-12); no MEAD selection, tag definition or registration, erratum or freeze; **no phase history, revision log or replay**; **no transform, position, attach point or socket** (world placement is resolved from `SourceEntityId` outside the contract, `TN-C-12`); **no animation asset, montage or cue reference** (asset selection is resolved from attack data keyed by `WindowKey`, outside the contract, `TN-C-13`); no second query surface for attack identity (§6.1).

### 4.9 C05-2.9 — Publication order within a frame `[NEW: C3, C4c]`

> **PO-1.** A frame containing **only** phase transitions publishes one `PhaseChanged` per transition, in authored (montage) order, at consecutive revisions `n+1`, `n+2`, ….
>
> **PO-2.** A frame containing **only** dilation changes publishes one `Retimed` per change, in the order applied, at consecutive revisions `n+1`, `n+2`, …. Never batched, coalesced, throttled or deferred (`TN-P-08`).
>
> **PO-3.** A frame containing **both** publishes **all phase transitions first, in authored order, then all dilation changes, in the order applied.** One phase change plus one retime is `PhaseChanged` at `n+1` followed by `Retimed` at `n+2`: two revisions, two messages, this order, never a shared revision and never the reverse.
>
> **PO-4.** Two phase transitions within one frame are **two transitions**: two revisions, two `PhaseChanged` messages, in authored order. A producer may not collapse them, drop the intermediate phase, merge the pair, or publish only the resulting phase. Where an authoring model can produce two section boundaries in one tick, both are published.

### 4.10 Referenced clauses carried forward unchanged `[UNCHANGED]`

Referenced by §9.2 and §10; listed so every clause reference resolves inside this document.

| Id | Statement, carried forward | Full text | Status |
|---|---|---|---|
| `C05-6.1` | Parry succeeds only when, in the frame the hit is resolved, the defender's parry window is active **and** the attacker's phase for that instance is `Active`: a same-frame phase-overlap test against live state, never timestamp subtraction, cross-entity clock comparison or tolerance for a late check. First stated at `A1-R3` §3.4. | S1 §6.1 | `PROPOSED — NOT FROZEN` |
| `C05-6.3` | `Dead > Cinematic > Staggered` over three carriers, priority order, first match wins, carriers never compared. Touches C-04 through the proposed amendment `C-04-4`; the carriers are stated in full only in S1 §6.3 (see §14.2 B-11). | S1 §6.3 | `PROPOSED — NOT FROZEN`, coupled to `C-04-4` |
| `C05-7.1` | The contract names no module and no class; its types are contract-layer types of the canonical architecture, owned by whoever TD-12 designates, implementable in a single-module layout. **Its second sentence remains withdrawn** and replaced by `C05-7.2`. | S1 §7.1, §5.1 here | `PROPOSED — NOT FROZEN` |

---

## 5. Ownership `[CORRECTED: C7, C8, C9]`

### 5.1 C05-7.1 — the neutrality rule `[UNCHANGED]`

The contract names **no module** and **no class**. Its value types, message structs, resynchronisation type and read interface are contract-layer types of the canonical architecture; their owner is whoever the TD designates when TD-12 settles which candidate is canonical. The interface must be implementable in a single-module layout, which holds under all three candidates. **No MEAD is selected by this document.**

### 5.2 C05-7.2 — the split, by activity `[CORRECTED: rows 5 and 6]`

> | Activity | Owner | Basis |
> |---|---|---|
> | **Gameplay production** — the authored attack, its montage windows, when a telegraph opens, changes phase and closes, and every cancellation decision | **Agent 2** for enemy attacks; **Agent 1** for the player's own attack | TD v1.2 C-05; `A2-C05` §8; `A1-R1` §5.1 |
> | **Producer-side implementation of `TN-P-01` … `TN-P-17`** — the pull answer, the per-producer id list, revision advancement, publication and ordering | **the owner of that producer**: Agent 2 on its enemy producers, Agent 1 on the player producer | follows from production ownership: an obligation about a producer's own state can only be implemented by the code that owns that state |
> | **Shared contract artefacts** — the value types, the message struct, `FTDDTelegraphResynchronisation`, the delegate signature and `ITDDTelegraphSource` | the **contract layer** of the canonical architecture; owner designated by TD-12 (Agent 3 under MEAD-C; unassigned under MEAD-A; absent under MEAD-B) | TD v1.2 C-05 "publisher: Agent 3/TD (event type)"; MEAD-C line 228 |
> | **Shared read-surface support** — the directory of `C05-2.5` and the resolution helper | **Agent 1**, as shared support that stores only association and liveness; Agent 1 does not implement any part of an Agent 2-owned producer, and Agent 2 does not implement the directory | one world-scoped home; holds nothing a producer owns |
> | **Consumer integration (Agent 1)** — parry/block/dodge evaluation from the pull; camera and audio cues | **Agent 1**, in its own code | TD v1.2 C-05; `A2-C05` §8 consumer list |
> | **Consumer integration (Agent 2)** — **AI reaction**; **audio cue selection**; **montage switch trigger**; **VFX marker timing and phase** | **Agent 2**, in its own code, from the snapshot and the messages | `A2-C05` §8; `C05-7.4` |
> | **Resolved outside C-05 (Agent 2, in its own systems)** — **VFX world placement and attachment**, **montage and cue asset selection**, **per-attack response tuning data** | **Agent 2**, from `SourceEntityId` and from attack data keyed by `WindowKey`. **C-05 supplies neither placement nor assets and promises neither** | `C05-2.8`; `TN-C-12`, `TN-C-13`; Agent 2's review C7 and C8 |
> | **Arbitration** — the parry/block decision for hits involving the player | **Agent 1**, subject to the TD-09 erratum and unchanged by this document | TD integration decision; `A1-R3` §3.4; `C05-6.1` |

**What rows 5–7 fix.** S2 named "AI reaction to the player's telegraph, audio cue, VFX marker, montage selection" as one row of C-05 consumers, which implied C-05 supplies what all four need. It does not: the VFX marker needs a world position the contract deliberately excludes, and montage selection needs an asset reference it also excludes. **The row is now split three ways** — C-05 consumer, outside-C-05 resolution, and the trigger/asset distinction — and `TN-C-11`…`TN-C-13` make each half testable. Agent 2's own submission carries the same overstatement ("animation montage selection" among C-05 consumers); this document corrects **both**, and §15.3 records theirs as withdrawn-by-agreement rather than as a defect of theirs alone.

### 5.3 C05-7.3 — what "Agent 1 implements" means `[UNCHANGED]`

Agent 1 implements: (a) every `TN-P` obligation **on the player's own producer**; (b) the shared read-surface support — directory and resolution — for all producers; (c) every `TN-C` obligation in Agent 1's own consumers; (d) every `TN-A` obligation in the arbitration path, subject to TD-09. **Agent 1 does not implement the `TN-P` obligations on Agent 2's enemy producers**; those are Agent 2's, on Agent 2's code, against the shared interface.

### 5.4 C05-7.4 — role vocabulary, and the mapping check `[NEW: C9]`

The obligation tables name **roles**; `C05-7.2` names **agents**. Both are deliberate — role vocabulary survives a change of producer ownership, agent vocabulary answers "who does it" — but the two must be mechanically comparable. This table is the bridge, and **DV-11** checks every implementer cell against it and against `C05-7.2`.

| Role token used in §7–§9 | Agent | `C05-7.2` row it derives from |
|---|---|---|
| `producer owner` | Agent 2 on enemy producers; Agent 1 on the player producer | row 2 |
| `each consumer` | Agent 1 in Agent 1's consumers; Agent 2 in Agent 2's consumers | rows 5–6 |
| `Agent 1, shared support` | Agent 1 | row 4 |
| `Agent 1, subject to TD-09` | Agent 1 | row 8 |
| `Agent 2, in its own systems` | Agent 2 | row 7 (outside-C-05 resolution) |
| `contract layer, owner pending TD-12` | designated by TD-12 | row 3 |

**Rule:** no other role token may appear in an implementer cell. A cell whose token is absent from this table, or whose agent contradicts its `C05-7.2` row, fails DV-11 — which is precisely the check Agent 2 asked for, and it replaces the weaker "the cell is non-empty" test.

---

## 6. Consumer information paths `[NEW: C6, C7, C8]`

### 6.1 `WindowKey` and `AttackTag` — who needs them, and why they are carried

The instruction is explicit that the snapshot must not grow automatically. So the case is made consumer by consumer, against the requirements Agent 2 actually submitted (`A2-C05` §7.6 marks both **Required**), and then against the alternatives.

| Consumer | Needs | Without the field | Verdict |
|---|---|---|---|
| **AI reaction** (Agent 2) | which attack, and whether it is blockable, **after a gap** | A resync into `Active` says an attack is active but not whether it can be blocked — the one decision the resync exists to enable. Agent 2's words: *"a resync that says Active without saying unblockable is a resync my AI cannot act on"* | **needs both** |
| **Audio cue** (Agent 2) | which attack, at the moment of the phase transition, to select the cue | The transition is observable but anonymous: every attack's windup sounds the same, or the consumer invents its own identity path | **needs `WindowKey`** |
| **Montage switch trigger** (Agent 2) | *when* to switch (from C-05) and *which* asset (from attack data) | The trigger works; the asset lookup has no key, so the montage system must re-derive identity through a path C-05 does not define | **needs `WindowKey`** |
| **Per-attack tuning** (Agent 1 and Agent 2) | stable key for authored response data | Tuning cannot be persisted per attack | **needs `WindowKey`** |
| **VFX marker** (Agent 2) | phase and timing (C-05); world placement (not C-05) | — | **needs neither**: placement resolves from `SourceEntityId` through the owning actor. `TN-C-12` |
| **Parry/block** (Agent 1) | phase, from live producer state off the arbitration path | — | **needs neither** on the arbitration path (`TN-A-01`); identity is not part of the parry test |

**Three of four named consumers need identity; none of them can supply it from C-05's existing fields.** `AttackInstanceId` is unique per firing, so it cannot key authored data (the same attack fired twice has two ids); `SourceEntityId` names the entity, not the attack (an enemy has several attacks). Neither substitutes.

**Alternatives, considered and rejected:**

1. **State that C-05 does not carry identity and let consumers resolve it.** Rejected: the only holder of "which attack is this instance" is the producer, so every consumer would need its own path back to it. Three bespoke paths is three chances to diverge, and the divergence would be invisible — one consumer treats an attack as blockable while another dodges. It also cannot work after a gap for the same reason the pull was needed in the first place.
2. **Add a descriptor query to `ITDDTelegraphSource`** (`TryGetTelegraphDescriptor(Id, Out)`). Rejected: it is a **second read surface over the same instance**, with its own availability, liveness and staleness questions — the class of problem `DN-1`'s expired handle exists to solve. It also breaks `C05-2.3a`: a message would no longer carry the whole state, reintroducing a follow-up call on the message path, which is the defect S2 closed.
3. **Carry them in the snapshot.** **Chosen.** Both are authored at `Opened`, constant for the instance's lifetime, and therefore **versioned fields** that cannot age and cannot repeat the `INV-1` error. `FName` (8 bytes) and `FGameplayTag` (8 bytes) per snapshot; no serialisation, no allocation, no new dependency beyond the engine's own GameplayTags module, which every candidate has.

**Boundary, stated so it cannot erode:** C-05 **transports** `AttackTag`; it does not define the tag, register it, or require a registry to exist. If no tag is authored, the field is empty and consumers behave as they would have without it. Tag **ownership and registration** stay where they are (registry/TD, U-14 adjacent) and are listed as a visible, non-blocking dependency at §14.2 B-13.

### 6.2 What stays outside C-05, and the path that resolves it

| Concern | Owner | Resolution path | Why not C-05 |
|---|---|---|---|
| **VFX world placement and attachment** | Agent 2, in its own systems | the owning actor, via `SourceEntityId`, and the attack's own attach data | C-05 carries values only; a transform is not timing, and `C05-2.8` excludes it |
| **Montage and cue asset selection** | Agent 2, in its own systems | attack data keyed by `WindowKey` | an asset reference is not timing; C-05 supplies the **trigger** and the **key** |
| **Per-attack response tuning** | the consuming agent | authored data keyed by `WindowKey` | data, not contract |
| **Damage and hit resolution** | C-03 | — | `A2-C05` §7.5; unchanged |

### 6.3 `Resynchronised` — status

Declared as `FTDDTelegraphResynchronisation` at `C05-2.2`, normative in `EN-3` and `TN-C-09`, delivered consumer-locally on `FTDDTelegraphOnResynchronised` with no transport, no registry and no queue (§4.2). It is **not** demoted to a self-check: the type is contract-layer, the firing rule is a contract obligation, and `T-C05-45`, `T-C05-50` and `T-C05-57` assert on the declared artefact.

---

## 7. Producer obligations

Seventeen. `TN-P-01` … `TN-P-14` are S2's, with `TN-P-07` corrected; `TN-P-15`, `TN-P-16` and `TN-P-17` are new. **Every row is implemented by the owner of that producer** — Agent 2 on its enemy producers, Agent 1 on the player producer (`C05-7.2` row 2). All tests are `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-P-01** | Publish `Opened` before the first frame the wind-up is observable to a stream consumer, with revision 1 and the complete snapshot. | authored window → `Opened` | A pull consumer that missed `Opened` is not in error; its first pull is a baseline (EN-1). For a stream consumer a missed open is a producer violation. | `Opened` precedes every other message for the instance | T-C05-07 | producer owner |
| **TN-P-02** | `AttackInstanceId` is unique per open instance and never reused. | allocation → `FGuid` | A reused id is a producer violation; consumers and the directory treat it as a new instance and diagnose in Test/Development. | n/a | T-C05-26 | producer owner |
| **TN-P-03** | Exactly one `Closed` per instance, carrying a close reason; no message at all for that instance afterwards. | close event → `Closed` | A second close is a duplicate (rejected); a post-close message is rejected and diagnosed. | after every other message for the instance | T-C05-21 | producer owner |
| **TN-P-04** | Every cancellation path closes: ability cancel, montage abort, interruption, forced transition, requirement change, the producer's own death. | cancel source → `Closed` with the matching reason | An unclosed cancelled instance remains pullable — a producer violation the consumer cannot detect, which is why it is normative. | same frame as the cancel | T-C05-22 | producer owner |
| **TN-P-05** | Invalidate open instances in the teardown path, before the producer stops being valid. | `EndPlay` → deregistration and `Closed(ProducerInvalidated)` | Best effort; the pull's `false` and directory liveness are the fail-safe (`TN-R-02`), not a substitute. | before removal from the world | T-C05-23 | producer owner |
| **TN-P-06** | Stream-out invalidates only that producer's instances; it neither requires nor implies world teardown, and it deregisters them from the directory even when no `Closed` can be emitted. | unload → deregistration of its own ids | Other producers are untouched; world teardown removes everything because the world-scoped owner is destroyed. | n/a | T-C05-24 | producer owner |
| **TN-P-07** | **Corrected.** `StateRevision` strictly increases on **every change to a versioned field** — every phase transition, every retime, and every change to `WindowKey` or `AttackTag` — and two observations at the same revision never differ in any `VF` field (`INV-1`). Changes to `OF` fields do not advance it. | state change → revision + 1 | An observation at an equal revision with different `VF` content is a producer violation and is never applied; an equal revision with different `OF` content is normal aging, not a violation. | monotone per instance | T-C05-16, T-C05-62 | producer owner |
| **TN-P-08** | One `Retimed` per `CustomDilation` change, published in the frame of the change, reflected in live state no later than that frame; ordered after any phase transition in the same frame (`PO-3`). **Never batch, coalesce, throttle or defer.** | dilation change → `Retimed` + live-state update | A batched retime is a violation; `UTDDHitStopSubsystem` boundaries are explicitly not exempt. | publish and live-state update in the same frame | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | producer owner |
| **TN-P-09** | Publish no message for an instance that is closed or was never opened. | stray publish → rejected | Rejected with a diagnostic; no directory entry is created and no held state changes. | n/a | T-C05-27 | producer owner |
| **TN-P-10** | All axis values come from the shared axis of `A1-R3` §3.3(a); never wall-clock, frame count or another entity's local time. | engine time → axis value | Any other domain is a violation, detected by a wall-clock fixture. | n/a | T-C05-15 | producer owner |
| **TN-P-11** | `TryGetOpenTelegraph` answers from live state at call time: `AxisNow` is the call's axis instant, `RemainingLocalSeconds` satisfies `INV-2` at that instant, and every `VF` field equals the instance's current revision exactly. Never a cached copy older than the last completed update. | id → snapshot or `false` | A stale `VF` copy is a violation; a caught-up `OF` pair is not. `false` for an open instance is a violation except during teardown (`TN-P-05`). | as of the last completed update before the call | T-C05-06, T-C05-40, T-C05-42 | producer owner |
| **TN-P-12** | No frame deltas, random seeds or tick-order dependence in any published or pulled value. | deterministic inputs → identical outputs | Non-determinism makes every suite flaky; treated as a producer defect. | n/a | T-C05-01 | producer owner |
| **TN-P-13** | Every phase transition advances `StateRevision` by exactly one, even when the timing block and every other value are unchanged, and publishes one `PhaseChanged` carrying the new snapshot. A phase change may not be published at the revision the consumer already holds. | phase transition → revision + 1 and `PhaseChanged` with the new snapshot | A phase change at an unchanged revision is the defect this obligation forbids; diagnosed in Test/Development. | one revision per transition | T-C05-43, T-C05-44, T-C05-45, T-C05-62 | producer owner |
| **TN-P-14** | Every message carries the complete snapshot at emission (`C05-2.3a`), identity fields included; no message carries a partial aspect. | state → `FTDDTelegraphMessage` with full snapshot | A partial message is a violation: it can advance the revision while leaving another aspect stale. | n/a | T-C05-49 | producer owner |
| **TN-P-15** | **New.** Within one frame, publish in the canonical order of `C05-2.9`: all phase transitions in authored order, then all dilation changes in the order applied. One phase change plus one retime is `PhaseChanged` at `n+1` then `Retimed` at `n+2` — never one message, never the reverse order, never a shared revision. | frame contents → ordered message sequence | Any other order or any merged revision is a violation, and it is detectable because the resulting message sequence differs from the canonical one. | canonical, total, per frame | T-C05-51 | producer owner |
| **TN-P-16** | **New.** Two phase transitions within one frame are two transitions: two revisions, two `PhaseChanged`, authored order, never collapsed or merged; a section-boundary pair is published in full (`PO-4`). | collapsed boundary → two messages | Collapsing, dropping the intermediate phase, or publishing one message for two transitions is a violation. | authored order within the frame | T-C05-52, T-C05-53 | producer owner |
| **TN-P-17** | **New.** Every published snapshot satisfies `INV-2` at its own `AxisNow`: `RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)`, so that a consumer's aging rule reproduces the producer's own value exactly. | snapshot → internally consistent `OF` pair | An inconsistent snapshot makes the consumer's aging diverge from the producer's; diagnosed at emission in Test/Development. | evaluated at the snapshot's own `AxisNow` | T-C05-54 | producer owner |

`TN-P-07` and `TN-P-13` overlap by design: one states monotonicity for all versioned changes, the other that phase changes are among them. The duplication is deliberate — the missing case is the one that produced Agent 3's finding.

---

## 8. Consumer obligations

Thirteen. `TN-C-01` … `TN-C-09` are S2's, corrected where Agent 2's findings require; `TN-C-10` … `TN-C-13` are new. **Each obligation is implemented by each consuming agent in its own code** — Agent 1 for defence, dodge, camera and audio; Agent 2 for AI reaction, audio cue, montage trigger and VFX timing. Tests `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-C-01** | Adopt only on strictly greater `StateRevision`; discard equal or lower silently, for messages and pulls alike. | snapshot, held revision → adopt or discard | **Corrected justification:** an equal-revision observation can differ only in `OF`, which the consumer re-derives by `INV-2`, so discarding loses no state change (§3.5). A `VF` difference always arrives with a revision bump. | commutative — outcome independent of arrival order | T-C05-02, T-C05-03, T-C05-46, T-C05-56, T-C05-62 | each consumer |
| **TN-C-02** | First observation of an instance establishes the baseline; record the phase as held and fire no entry for it. | first observation → baseline | Firing entry on a baseline double-fires on every subscribe. | baseline before any entry evaluation | T-C05-08, T-C05-09, T-C05-47 | each consumer |
| **TN-C-03** | After the baseline, entry at most once per `(AttackInstanceId, phase)`; a retime never re-fires; a duplicate `PhaseChanged` fires nothing. | phase transition → at most one entry | A second entry for the same phase is detectable by counting. | per consumer, per phase | T-C05-10, T-C05-11 | each consumer |
| **TN-C-04** | On `incoming > held + 1`, record a gap and set `bStateGapObserved` until the instance closes. Never interpolate or extrapolate. | gap → flag | Clearing the flag before close is a violation. | on adoption of the post-gap snapshot | T-C05-12, T-C05-13 | each consumer |
| **TN-C-05** | After a gap, recover with **one** pull; if it is unavailable or not newer, report timing as unknown and diagnose rather than guess. | id → current snapshot or unknown | "Unknown" is a legitimate terminal state for that instance. | once per gap | T-C05-14, T-C05-19, T-C05-44 | each consumer |
| **TN-C-06** | Removal is closure: a pull returning `false`, an unresolvable id, or a `Closed` message means closed — release the block, fire no further entry, raise no error. **A `Closed` closes regardless of its revision (`TM-1`).** | false, unresolvable id, or `Closed` → closure | Treating "not found" as an error is a defect; so is discarding a `Closed` because its revision is not newer. | immediate on observation | T-C05-25, T-C05-48 | each consumer |
| **TN-C-07** | Evaluate `Dead > Cinematic > Staggered` in priority order over the three carriers of `C05-6.3`; never compare carriers. | published state → one effective value | Comparing an enum to a tag is a violation. **Inherits `C05-6.3`'s `PROPOSED — NOT FROZEN` status and its `C-04-4` coupling (§14.2 B-11).** | priority order, first match wins | T-C05-35, T-C05-36, T-C05-37, T-C05-38, T-C05-39 | each consumer |
| **TN-C-08** | Never treat a pull as revision history; a post-gap block is current state, not a substitute for what was missed, and a phase absent from a pull is not a phase that did not occur (`RS-3`). | pull result → current value | A consumer that assumes full recovery makes telemetry and AI timings silently wrong. | n/a | T-C05-20, T-C05-50, T-C05-53 | each consumer |
| **TN-C-09** | A snapshot adopted across a gap fires no phase entry; the consumer raises exactly **one** `FTDDTelegraphResynchronisation` per gap, on its own delegate, carrying the landed snapshot and no history, and synthesises no entries for phases it did not observe. | gap adoption → zero entries, one resynchronisation | A fabricated entry is a violation; more than one resynchronisation per gap is a violation; a resynchronisation after a contiguous adoption is a violation. | immediately on gap adoption, before any further entry evaluation | T-C05-45, T-C05-50, T-C05-53, T-C05-57 | each consumer |
| **TN-C-10** | **New.** Age a held snapshot by `INV-2` — `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` — and never treat a difference confined to `OF` as a state change, a gap, or a diagnostic. Never age by wall-clock elapsed or by the consumer's own dilation. | held snapshot, axis now → remaining local seconds | Wall-clock aging is wrong across any pause or dilation change; treating `OF` drift as a change produces a false gap on every frame. | continuously, per consumer | T-C05-54, T-C05-55, T-C05-56 | each consumer |
| **TN-C-11** | **New.** Take attack identity and blockability from the adopted snapshot's `WindowKey` and `AttackTag` — including after a resynchronisation — and from no other source. No consumer may add a second lookup surface for identity. | snapshot → attack identity, blockability | A consumer that re-derives identity through its own path will disagree with another consumer's; that divergence is the failure this obligation forbids. | on adoption, before any defensive decision | T-C05-57, T-C05-58 | each consumer |
| **TN-C-12** | **New.** For VFX, consume **timing and phase only**; resolve world placement and attachment from `SourceEntityId` through the owning actor, outside this contract. No contract type carries a transform, and none may be added. | snapshot + `SourceEntityId` → marker start/stop and placement | A marker placed from anything in C-05 is a violation of `C05-2.8`; the contract supplies no position and must not be asked to. | on the phase transition that starts or stops the marker | T-C05-59 | Agent 2, in its own systems |
| **TN-C-13** | **New.** Montage selection is a **trigger-and-key** relationship: C-05 supplies **when** to switch (the phase transition and its phase) and **which attack** (`WindowKey`); the montage asset is selected from attack data keyed by `WindowKey`, outside this contract. C-05 carries no animation asset reference. | phase transition + `WindowKey` → montage switch request | Selecting an asset from anything in C-05 is a violation; so is switching on a retime (a retime is not a switch trigger). | on the phase transition, in the same frame | T-C05-60 | Agent 2, in its own systems |

---

## 9. Shared read-surface and arbitration obligations

Six read-surface obligations (`TN-R-01` … `TN-R-06`) and two arbitration obligations (`TN-A-01`, `TN-A-02`). Tests `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-R-01** | The directory stores per instance only the id, `SourceEntityId` and one weak liveness handle — no timing, no phase, no revision — and never serves timing through the handle. **Register on `Opened`; deregister on `Closed` or producer invalidation, whichever first.** | registration → association record | A record carrying timing is a violation detectable by structure. An expired handle resolves `false`; teardown drops all. | registration completes before a pull by id can succeed | T-C05-28, T-C05-29, T-C05-61 | Agent 1, shared support |
| **TN-R-02** | `TryGetOpenTelegraph` returns `false` for closed instances, instances the producer never opened, and instances during teardown; never a partial or stale-filled record. | id → snapshot or `false` | `false` is never an error (`RM-2`); `true` for a closed instance is a violation. | n/a | T-C05-04, T-C05-05 | producer owner |
| **TN-R-03** | `GetOpenTelegraphIds` reports only the calling producer's own instances; not a world query, not aggregated in this version, not X-1. | producer → its ids | Answering with other producers' ids would silently re-create custody. | n/a | T-C05-30 | producer owner |
| **TN-R-04** | A pull returns a value copy, is callable from any consumer phase without re-entrancy, reflects the producer's last completed update, and mutates nothing the caller can see. | call → copy | A returned reference into producer storage or a re-entrant marshal is a violation. | as of the last completed update | T-C05-31 | producer owner |
| **TN-R-05** | **Corrected.** A pull at revision `R` returns **`VF` content identical to every other observation at `R`** (`INV-1`) and an `OF` pair consistent with `INV-2` at its own call instant. It may never manufacture a `VF` state the revision does not cover, and it is never required to reproduce an earlier observation's `OF` values. | id, held revision → snapshot | A `VF` difference at equal revision is a violation; an `OF` difference is expected aging and is not a diagnosable event. | n/a | T-C05-46, T-C05-49 | producer owner |
| **TN-R-06** | **New.** The directory performs no scheduling: it holds no clock, no queue, no ordering, no phase, no revision and no window; it emits nothing and wakes nothing; it answers id→producer and liveness only. | query → producer handle or `false` | Any added timing field, any ordering or deferral behaviour, or any emission from the directory is a violation — it would make the directory the director `A2-C05` §7.1 rejected. | n/a | T-C05-61 | Agent 1, shared support |
| **TN-A-01** | Parry is `C05-6.1`: same-frame phase overlap. The attacker's phase is read on the hit-resolution path from the component that owns the attack instance — never from the pull, the directory or a published block; no timestamp subtraction, no late tolerance. | hit data, defence state, attacker live phase → parry outcome | Any C-05 value influencing the outcome is a violation; a wrong timing block must not change the result. | in the frame the hit is resolved | T-C05-32, T-C05-33 | Agent 1, subject to TD-09 |
| **TN-A-02** | No arbitration decision depends on any value produced by the C-05 contract. | as above → outcome plus diagnostic | An observed read of the telegraph surface on the arbitration path is a violation, detectable with a spy. | n/a | T-C05-34 | Agent 1, subject to TD-09 |

---

## 10. Worked transitions

Ten examples. `rev` is `StateRevision`; "held" is what a given consumer holds; each scenario is a candidate acceptance case (§12).

### 10.1 EX-1 — a phase-only transition, observed in order

| t | Producer event | Message | Snapshot |
|---|---|---|---|
| 1 | wind-up begins, `ProducerRate` 0.05 | `Opened` | Windup, rev **1** |
| 2 | wind-up ends; **no dilation change, endpoints unchanged** | `PhaseChanged` | Active, rev **2** |

Consumer holds rev 1, receives rev 2: `2 == 1 + 1` → contiguous, adopt, phase differs → **entry fires once**.

### 10.2 EX-2 — the transition is missed, and a pull recovers it

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | **message lost** |
| 3 | nothing changes | pulls: Active, rev **2**; `2 > 1` → adopt; `2 == 1+1` → **not** a gap → entry fires once |

The pull's `OF` pair is later than it would have been at t=2; that difference is aging (`INV-2`), not a state change, and it is not diagnosed (`TN-C-10`).

### 10.3 EX-3 — several transitions missed (gap)

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | lost |
| 3 | `PhaseChanged` Recovery, rev 3 | lost |
| 4 | nothing changes | pulls: Recovery, rev **3**; `3 > 1+1` → **gap** |

Adopt Recovery; **no entry** for Active or Recovery; exactly one `FTDDTelegraphResynchronisation` carrying the landed Recovery snapshot; `bStateGapObserved` set until close.

### 10.4 EX-4 — a retime only

`Retimed`, rev 3, `ProducerRate` 0.2, endpoints recomputed, `OF` re-anchored at the new `AxisNow`. Contiguous → adopt, no entry, no resynchronisation. `TN-P-08` still forbids batching: two boundaries in one frame are revisions 3 and 4 (`PO-2`).

### 10.5 EX-5 — the three same-frame cases, enumerated `[REWRITTEN: C4c]`

S2's version of this example described one phase change and one retime in a frame and then assigned revisions to a *different* scenario. It is replaced, and the ordering it now states is normative (`C05-2.9`).

| Case | What the frame contains | Message sequence | Revisions | Consumer holding `n` |
|---|---|---|---|---|
| **(a)** phase only | Windup→Active, dilation unchanged | one `PhaseChanged` | `n+1` | adopt, entry once, no gap |
| **(b)** retime only | one `CustomDilation` change, phase unchanged | one `Retimed` | `n+1` | adopt, no entry, no gap |
| **(c)** one of each | Windup→Active **and** a dilation change | `PhaseChanged` then `Retimed` | `n+1` then `n+2` | both received: adopt both, entry once, no gap. Only `n+2` received: `n+2 > n+1` → **gap**, no entry, one resynchronisation |
| **(c′)** one of each, received out of order | the two messages arrive `Retimed` first | consume in revision order: `n+2` alone → gap and resync; `n+1` later → stale (`n+1 < n+2`) → discarded | see left | phase and timing are never wrong, but the entry is not fired — the consumer resyncs instead |

**The order is normative, not advisory** (`PO-3`, `TN-P-15`): two conforming producers may not publish (c) in different orders, because which message lands at `n+1` decides whether entry fires or a resync is raised.

### 10.6 EX-6 — repeated pulls and duplicate messages (with aging)

Consumer at rev 3 pulls twice with no producer change, one frame apart. Both returns carry **identical `VF`**: same phase, same endpoints, same `ProducerRate`, same `WindowKey`, same `AttackTag`. Their `OF` pairs differ: `AxisNow` is one frame later and `RemainingLocalSeconds` is lower by exactly one frame × `ProducerRate` (`INV-2`). The second pull is **discarded** (`AD-1`) — and nothing is lost, because the consumer's own aging of its held snapshot yields the same remaining time (§3.5). No entry, no resynchronisation, no diagnostic. **A change of phase at an unchanged revision remains unrepresentable.**

### 10.7 EX-7 — late subscriber, then a real transition

A consumer subscribes mid-Active and pulls Active at rev 5: baseline (`EN-1`), **no entry**, and it now holds `WindowKey` and `AttackTag` for that attack — so its first defensive decision is already informed. The producer then enters Recovery at rev 6: contiguous, phase differs → **exactly one entry**. Miss rev 6 and pull rev 7 Recovery later → gap: no entry, one resynchronisation, and the landed snapshot still carries identity, so the resync is actionable (`TN-C-11`).

### 10.8 EX-8 — terminal close at an unchanged revision

Consumer holds rev 3. The producer publishes `Closed(Natural)` carrying rev 3, because a close does not advance the state revision. `TM-1` applies: the instance closes, the consumer releases state, fires nothing further, raises no error. Without `TM-1`, `AD-1` would have discarded the close as an equal revision.

### 10.9 EX-9 — aging and the clamp `[NEW: C4a]`

Producer opens Windup with `PhaseEndAxis = 4.0`, `AxisNow = 0.0`, `ProducerRate = 0.05`, so `R0 = (4.0 − 0.0) × 0.05 = 0.20` local s.

| Axis now | `RemainingLocalSeconds` by `INV-2` | Consumer aging from the t=0 snapshot | Agree? |
|---|---|---|---|
| 0.0 | 0.2000 | `0.20 − (0 − 0) × 0.05 = 0.2000` | yes |
| 0.2 | 0.1900 | `0.20 − 0.2 × 0.05 = 0.1900` | yes |
| 2.0 | 0.1000 | `0.20 − 2.0 × 0.05 = 0.1000` | yes |
| 4.0 | **0.0000** | `0.20 − 4.0 × 0.05 = 0.0000` | yes |
| 8.0 | **0.0000** (clamped) | `max(0, 0.20 − 8.0 × 0.05) = 0.0000` | never negative |

The phase is complete when `Axis(t) − AxisNow ≥ R0 / ProducerRate` (here `0.20 / 0.05 = 4.0` axis s), which is `A1-R4` §3.3(e)'s equivalent condition and the same equation as `INV-2`. **A wall-clock consumer diverges at the first pause** — the negative control in `T-C05-55`.

### 10.10 EX-10 — two transitions in one frame, and what a consumer can still see `[NEW: C3]`

A montage section boundary pair lands in one tick: Windup ends and Active begins, then Active ends and Recovery begins, both before the frame ends. `PO-4` requires **two** messages: `PhaseChanged(Active)` at `n+1`, `PhaseChanged(Recovery)` at `n+2`.

| Consumer | What it receives | Result |
|---|---|---|
| Attentive | both | contiguous; entry once for Active, once for Recovery (`EN-2`), no gap |
| Late by one | only `n+2` | `n+2 > n+1` → gap; no entry; one resynchronisation landing in Recovery |
| Pull-based only | a pull after the frame | returns **Recovery at `n+2`**; Active is not observable at all — a legitimate outcome (`RS-3`), not a missing state |

The producer may not collapse the pair into one revision "because the frame only shows Recovery". A phase that a consumer never observes is not a phase that never happened, and the AI's audit trail must be able to tell those apart.

---

## 11. Traceability

### 11.1 The instruction's validation requirements → clause → check → test

| # | Validation requirement (instruction §4) | Clause | Document check | Test |
|---|---|---|---|---|
| 1 | Equal-revision identity excludes legitimate aging without weakening phase, endpoint or rate consistency | `INV-1`, §3.2, §3.3 | DV-12 | T-C05-46, T-C05-54 |
| 2 | Aging formula consistent across producer and consumer obligations | `INV-2`, `TN-P-17`, `TN-C-10`, §3.4 | DV-13 | T-C05-54, T-C05-55 |
| 3 | Equal-revision discard cannot lose a genuine state change | `AD-1`, `TN-P-07`, `TN-C-01`, §3.5 | DV-12 | T-C05-56, T-C05-62 |
| 4 | Simultaneous phase/retime publication is deterministic | `C05-2.9` `PO-3`, `TN-P-15` | DV-14 | T-C05-51 |
| 5 | Multiple phase transitions within one frame are unambiguous | `C05-2.9` `PO-4`, `TN-P-16`, `RS-3` | DV-14 | T-C05-52, T-C05-53 |
| 6 | Directory registration, deregistration, invalidation and liveness compose | `DN-1`, `TN-R-01`, `TN-R-06`, `RM-1`, `TN-P-05`, `TN-P-06` | DV-16 | T-C05-61 |
| 7 | AI, audio, VFX and montage responsibilities have implementable information paths | §6.1, §6.2, `TN-C-11`…`TN-C-13` | DV-17 | T-C05-57 … T-C05-60 |
| 8 | `Resynchronised` has an unambiguous normative status | `C05-2.2`, `EN-3`, `TN-C-09`, §6.3 | DV-18 | T-C05-45, T-C05-50, T-C05-57 |
| 9 | All implementer assignments agree with the ownership table | `C05-7.4`, §7–§9 | DV-11 | all 38 rows |
| 10 | Every test maps to an obligation and every obligation to one or more tests | §11.2, §12.1 | DV-15 | all 62 cases |
| 11 | Agent 2's nine conditions are individually traceable | §2 | DV-19 | — |

### 11.2 Obligation → test coverage

| Obligation | Cases | Obligation | Cases |
|---|---|---|---|
| TN-P-01 | T-C05-07 | TN-C-01 | T-C05-02, T-C05-03, T-C05-46, T-C05-56, T-C05-62 |
| TN-P-02 | T-C05-26 | TN-C-02 | T-C05-08, T-C05-09, T-C05-47 |
| TN-P-03 | T-C05-21 | TN-C-03 | T-C05-10, T-C05-11 |
| TN-P-04 | T-C05-22 | TN-C-04 | T-C05-12, T-C05-13 |
| TN-P-05 | T-C05-23 | TN-C-05 | T-C05-14, T-C05-19, T-C05-44 |
| TN-P-06 | T-C05-24 | TN-C-06 | T-C05-25, T-C05-48 |
| TN-P-07 | T-C05-16, T-C05-62 | TN-C-07 | T-C05-35 … T-C05-39 |
| TN-P-08 | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | TN-C-08 | T-C05-20, T-C05-50, T-C05-53 |
| TN-P-09 | T-C05-27 | TN-C-09 | T-C05-45, T-C05-50, T-C05-53, T-C05-57 |
| TN-P-10 | T-C05-15 | TN-C-10 | T-C05-54, T-C05-55, T-C05-56 |
| TN-P-11 | T-C05-06, T-C05-40, T-C05-42 | TN-C-11 | T-C05-57, T-C05-58 |
| TN-P-12 | T-C05-01 | TN-C-12 | T-C05-59 |
| TN-P-13 | T-C05-43, T-C05-44, T-C05-45, T-C05-62 | TN-C-13 | T-C05-60 |
| TN-P-14 | T-C05-49 | TN-R-01 | T-C05-28, T-C05-29, T-C05-61 |
| TN-P-15 | T-C05-51 | TN-R-02 | T-C05-04, T-C05-05 |
| TN-P-16 | T-C05-52, T-C05-53 | TN-R-03 | T-C05-30 |
| TN-P-17 | T-C05-54 | TN-R-04 | T-C05-31 |
| TN-R-05 | T-C05-46, T-C05-49 | TN-R-06 | T-C05-61 |
| TN-A-01 | T-C05-32, T-C05-33 | TN-A-02 | T-C05-34 |

**38 obligations, every one covered; 62 cases, every one assigned** (verified by DV-15 in both directions).

---

## 12. Acceptance-test catalogue

**62 cases, 15 suites, every case `PROPOSED / NOT RUN`, 0 executed.** No code exists to run them against and no Unreal project exists in this workspace (ADR-0012).

### 12.1 The suites

| # | Suite | Covers | Cases | Case ids |
|---|---|---|---|---|
| A | `TDD-Contract.Combat.TelegraphPullRecovery` | TN-P-12, TN-C-01, TN-R-02, TN-P-11 | 6 | T-C05-01 … 06 |
| B | `TDD-Contract.Combat.TelegraphEntryBaseline` | TN-P-01, TN-C-02, TN-C-03 | 5 | T-C05-07 … 11 |
| C | `TDD-Contract.Combat.TelegraphRevisionGapDetection` | TN-C-04, TN-C-05, TN-P-10, TN-P-07 | 5 | T-C05-12 … 16 |
| D | `TDD-Contract.Combat.TelegraphHitstopRevisionBurst` | TN-P-08, TN-C-05, TN-C-08 | 4 | T-C05-17 … 20 |
| E | `TDD-Contract.Combat.TelegraphProducerLossPull` | TN-P-03, TN-P-04, TN-P-05, TN-P-06, TN-C-06, TN-P-02, TN-P-09 | 7 | T-C05-21 … 27 |
| F | `TDD-Contract.Combat.TelegraphResolutionAndDirectory` | TN-R-01, TN-R-03, TN-R-04 | 4 | T-C05-28 … 31 |
| G | `TDD-Contract.Combat.TelegraphArbitrationIndependence` | TN-A-01, TN-A-02 | 3 | T-C05-32 … 34 |
| H | `TDD-Contract.Combat.TelegraphDeadPrecedenceEvaluation` | TN-C-07 | 5 | T-C05-35 … 39 |
| I | `TDD-Contract.Combat.TelegraphSameFrameCoherence` | TN-P-08, TN-P-11, TN-C-01 | 3 | T-C05-40 … 42 |
| J | `TDD-Contract.Combat.TelegraphPhaseRevisionAdvancement` | TN-P-13, TN-C-05, TN-C-09, TN-R-05 | 4 | T-C05-43 … 46 |
| K | `TDD-Contract.Combat.TelegraphResyncTerminalAndLateSubscriber` | TN-C-02, TN-C-06, TN-P-14, TN-C-09 | 4 | T-C05-47 … 50 |
| **L** | **`TDD-Contract.Combat.TelegraphSameFramePublicationOrder`** | **TN-P-15, TN-P-16, TN-C-08** | **3** | **T-C05-51 … 53** |
| **M** | **`TDD-Contract.Combat.TelegraphAgingAndObservationInstant`** | **TN-P-17, TN-C-10, TN-C-01** | **3** | **T-C05-54 … 56** |
| **N** | **`TDD-Contract.Combat.TelegraphAttackIdentityResolution`** | **TN-C-09, TN-C-11, TN-C-12, TN-C-13** | **4** | **T-C05-57 … 60** |
| **O** | **`TDD-Contract.Combat.TelegraphDirectoryComposition`** | **TN-R-01, TN-R-06** | **2** | **T-C05-61 … 62** |

### 12.2 The twelve cases added or rewritten by this revision, specified

| Case | Setup | Assertion |
|---|---|---|
| **T-C05-51** `[NEW: C4c]` | A frame contains one phase transition (Windup→Active) and two dilation changes; consumer holds `n` | the message sequence is exactly `PhaseChanged`@`n+1`, `Retimed`@`n+2`, `Retimed`@`n+3` — phase first, retimes in applied order, no coalescing, no shared revision; the consumer adopts all three contiguously, fires entry once, records no gap |
| **T-C05-52** `[NEW: C3]` | Two phase transitions in one frame (montage section boundary pair); consumer holds `n` | two `PhaseChanged` messages at `n+1` (Active) and `n+2` (Recovery), authored order, neither collapsed; the consumer fires entry once for Active and once for Recovery and records no gap |
| **T-C05-53** `[NEW: C3]` | Same producer, consumer receives only the second message (`n+2`) | `n+2 > n+1` → gap; no entry for the unobserved Active; exactly one `FTDDTelegraphResynchronisation` landing in Recovery; a subsequent pull returns Recovery at `n+2` and never the intermediate phase (`RS-3`, `TN-C-08`) |
| **T-C05-54** `[NEW: C4a]` | Two pulls at the same revision, Δ axis apart, no producer change | identical `VF` on both (phase, three endpoints, `ProducerRate`, `WindowKey`, `AttackTag`); `AxisNow` differs by Δ; `RemainingLocalSeconds` differs by exactly Δ × `ProducerRate`; both satisfy `INV-2`, and the second equals `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` evaluated from the first (`TN-P-17`, `TN-C-10`) |
| **T-C05-55** `[NEW: C4a]` | Aging past the end of the phase, and across a pause | `RemainingLocalSeconds` reaches 0 at `Axis(t) − AxisNow = R0 / ProducerRate`, is clamped at 0 and never negative; across a pause the axis does not advance and neither does `R`; a wall-clock-aging consumer diverges and is the negative control |
| **T-C05-56** `[NEW: C4a]` | Consumer at `n` discards an equal-revision pull, then receives `n+1` with a changed endpoint | the discarding consumer's `VF` state after adopting `n+1` equals that of a consumer that never discarded; the discarded observation's only difference was `OF`; a fixture in which the equal-revision pull carries a `VF` change is rejected as a producer violation, not silently adopted |
| **T-C05-57** `[NEW: C6, C5]` | Consumer resyncs into Active across a gap, `AttackTag` = unblockable | exactly one `FTDDTelegraphResynchronisation` carrying the landed snapshot; the consumer reads `WindowKey` and `AttackTag` from that snapshot and selects dodge rather than block with no second lookup; the delegate fires once and is not re-raised for the same gap |
| **T-C05-58** `[NEW: C6]` | Two attacks with different `WindowKey` and different `AttackTag` reach the audio consumer | the phase transition alone (snapshot identity included) selects two different cue ids; no additional query is issued; a consumer that instead derives identity from `SourceEntityId` fails the assertion |
| **T-C05-59** `[NEW: C7]` | A VFX marker consumes the telegraph for one attack | the marker starts and stops on phase transitions from C-05 timing only; its world placement is resolved from `SourceEntityId` through the owning actor; no contract type carries a transform, position, socket or attach point (compile-time and structural assertion) |
| **T-C05-60** `[NEW: C8]` | A montage consumer observes a phase transition, then a retime | the phase transition raises exactly one montage switch request carrying `WindowKey`; the asset is resolved from attack data keyed by `WindowKey`, outside C-05; the retime raises **no** switch request; no asset reference appears in any contract type |
| **T-C05-61** `[NEW: C1, C2]` | Five producer fates: natural close, cancellation, stream-out with no graceful close, producer death, world teardown | each deregisters the association; `TryGetOpenTelegraph` and the resolution helper answer `false` in every case; no entry survives teardown; the directory emits nothing, orders nothing and defers nothing throughout (`TN-R-01`, `TN-R-06`) |
| **T-C05-62** `[NEW: C4a]` | The complete change table — open, phase transition, retime, `WindowKey` change, `AttackTag` change, close, plus pure `OF` drift | every `VF` change arrives with a revision bump (`TN-P-07`, `TN-P-13`); pure `OF` drift arrives with no bump and triggers no diagnosis; no `VF` change can be observed only through an `OF` difference |

**T-C05-46 is rewritten** (Agent 2's C4b): it asserts **versioned-field** identity across two pulls and one duplicated message at rev 3, plus `INV-2` consistency of each `OF` pair — it no longer demands byte-identical `RemainingLocalSeconds`, which no conforming producer could deliver.

### 12.3 Complete case catalogue

`Status` is `PROPOSED / NOT RUN` for every row without exception; the column is repeated rather than stated once because this catalogue is the artefact Agent 2 asked to be complete.

| Case | Suite | Obligation(s) | Intent | Status |
|---|---|---|---|---|
| T-C05-01 | A | TN-P-12 | deterministic fixture: identical inputs, identical sequence | `PROPOSED / NOT RUN` |
| T-C05-02 | A | TN-C-01 | equal revision discarded | `PROPOSED / NOT RUN` |
| T-C05-03 | A | TN-C-01 | lower revision discarded, consumer never moves backwards | `PROPOSED / NOT RUN` |
| T-C05-04 | A | TN-R-02 | `false` for a closed instance | `PROPOSED / NOT RUN` |
| T-C05-05 | A | TN-R-02 | `false` for an instance never opened | `PROPOSED / NOT RUN` |
| T-C05-06 | A | TN-P-11 | pull answers from live state at call time | `PROPOSED / NOT RUN` |
| T-C05-07 | B | TN-P-01 | `Opened` precedes every other message | `PROPOSED / NOT RUN` |
| T-C05-08 | B | TN-C-02 | baseline fires no entry | `PROPOSED / NOT RUN` |
| T-C05-09 | B | TN-C-02 | pull-derived baseline and `Opened` baseline are the same case | `PROPOSED / NOT RUN` |
| T-C05-10 | B | TN-C-03 | entry at most once per phase | `PROPOSED / NOT RUN` |
| T-C05-11 | B | TN-C-03 | duplicate `PhaseChanged` fires nothing; retime re-fires nothing | `PROPOSED / NOT RUN` |
| T-C05-12 | C | TN-C-04 | gap flagged on `incoming > held + 1` | `PROPOSED / NOT RUN` |
| T-C05-13 | C | TN-C-04 | gap flag persists until close | `PROPOSED / NOT RUN` |
| T-C05-14 | C | TN-C-05 | a single pull recovers, never an iteration | `PROPOSED / NOT RUN` |
| T-C05-15 | C | TN-P-10 | axis domain, not wall clock or frame count | `PROPOSED / NOT RUN` |
| T-C05-16 | C | TN-P-07 | revision monotone on every versioned change | `PROPOSED / NOT RUN` |
| T-C05-17 | D | TN-P-08 | one `Retimed` per dilation boundary, no batching | `PROPOSED / NOT RUN` |
| T-C05-18 | D | TN-P-08 | hitstop boundaries are not exempt | `PROPOSED / NOT RUN` |
| T-C05-19 | D | TN-P-08, TN-C-05 | burst then recovery, no coalescing | `PROPOSED / NOT RUN` |
| T-C05-20 | D | TN-C-08 | a pull is not history | `PROPOSED / NOT RUN` |
| T-C05-21 | E | TN-P-03 | exactly one `Closed`, terminal | `PROPOSED / NOT RUN` |
| T-C05-22 | E | TN-P-04 | every cancellation path closes | `PROPOSED / NOT RUN` |
| T-C05-23 | E | TN-P-05 | teardown invalidates before the producer dies | `PROPOSED / NOT RUN` |
| T-C05-24 | E | TN-P-06 | stream-out scoped to its own instances | `PROPOSED / NOT RUN` |
| T-C05-25 | E | TN-C-06 | removal is closure, not an error | `PROPOSED / NOT RUN` |
| T-C05-26 | E | TN-P-02 | ids never reused | `PROPOSED / NOT RUN` |
| T-C05-27 | E | TN-P-09 | no message for a closed or never-opened instance | `PROPOSED / NOT RUN` |
| T-C05-28 | F | TN-R-01 | registration precedes resolution | `PROPOSED / NOT RUN` |
| T-C05-29 | F | TN-R-01 | expired handle answers `false` | `PROPOSED / NOT RUN` |
| T-C05-30 | F | TN-R-03 | per-producer ids only, never aggregated | `PROPOSED / NOT RUN` |
| T-C05-31 | F | TN-R-04 | value copy, no re-entrancy, no visible mutation | `PROPOSED / NOT RUN` |
| T-C05-32 | G | TN-A-01 | parry from live phase, not from C-05 | `PROPOSED / NOT RUN` |
| T-C05-33 | G | TN-A-01 | corrupted timing block does not change the parry result | `PROPOSED / NOT RUN` |
| T-C05-34 | G | TN-A-02 | spy shows no telegraph read on the arbitration path | `PROPOSED / NOT RUN` |
| T-C05-35 … 39 | H | TN-C-07 | `Dead > Cinematic > Staggered`, priority order, carriers never compared | `PROPOSED / NOT RUN` |
| T-C05-40 | I | TN-P-11, TN-P-08 | message and pull agree within one frame | `PROPOSED / NOT RUN` |
| T-C05-41 | I | TN-P-08 | two boundaries in one frame are two revisions | `PROPOSED / NOT RUN` |
| T-C05-42 | I | TN-P-11 | pull never returns an older revision than the last message | `PROPOSED / NOT RUN` |
| T-C05-43 | J | TN-P-13 | phase-only transition advances the revision by one | `PROPOSED / NOT RUN` |
| T-C05-44 | J | TN-P-13, TN-C-05 | dropped `PhaseChanged` recovered by one pull, contiguous, entry fires | `PROPOSED / NOT RUN` |
| T-C05-45 | J | TN-P-13, TN-C-09 | two transitions missed: gap, no entry, one resynchronisation | `PROPOSED / NOT RUN` |
| T-C05-46 | J | TN-C-01, TN-R-05 | **rewritten:** versioned-field identity at one revision, `INV-2` consistency of the `OF` pairs | `PROPOSED / NOT RUN` |
| T-C05-47 | K | TN-C-02 | late subscriber baseline mid-phase, no entry | `PROPOSED / NOT RUN` |
| T-C05-48 | K | TN-C-06 | `Closed` at an equal revision still closes (`TM-1`) | `PROPOSED / NOT RUN` |
| T-C05-49 | K | TN-P-14, TN-R-05 | complete payload on all four message kinds | `PROPOSED / NOT RUN` |
| T-C05-50 | K | TN-C-09, TN-C-08 | one resynchronisation per gap, none afterwards | `PROPOSED / NOT RUN` |
| T-C05-51 | L | TN-P-15 | same-frame phase + retimes: canonical order, no shared revision | `PROPOSED / NOT RUN` |
| T-C05-52 | L | TN-P-16 | two transitions in one frame: two messages, two revisions | `PROPOSED / NOT RUN` |
| T-C05-53 | L | TN-P-16, TN-C-09, TN-C-08 | receiving only the second transition: gap, resync, no fabricated entry | `PROPOSED / NOT RUN` |
| T-C05-54 | M | TN-P-17, TN-C-10 | `VF` identical, `OF` ages by exactly Δ × rate, `INV-2` holds | `PROPOSED / NOT RUN` |
| T-C05-55 | M | TN-C-10 | clamp at zero, pause freezes, wall-clock negative control | `PROPOSED / NOT RUN` |
| T-C05-56 | M | TN-C-01, TN-C-10 | discard-then-age is observationally equivalent | `PROPOSED / NOT RUN` |
| T-C05-57 | N | TN-C-09, TN-C-11 | resync into Active is actionable: blockability from `AttackTag` | `PROPOSED / NOT RUN` |
| T-C05-58 | N | TN-C-11 | audio cue selected from identity carried in the snapshot | `PROPOSED / NOT RUN` |
| T-C05-59 | N | TN-C-12 | VFX timing from C-05, placement from `SourceEntityId`, no transform in any type | `PROPOSED / NOT RUN` |
| T-C05-60 | N | TN-C-13 | montage trigger + key from C-05, asset from attack data, retime is not a trigger | `PROPOSED / NOT RUN` |
| T-C05-61 | O | TN-R-01, TN-R-06 | five producer fates compose; directory schedules and emits nothing | `PROPOSED / NOT RUN` |
| T-C05-62 | O | TN-P-07, TN-P-13, TN-C-01 | complete change table: every `VF` change bumps, `OF` drift never does | `PROPOSED / NOT RUN` |

**62 cases, 0 executed.** Case rows `T-C05-35 … 39` are grouped because the suite distinguishes them by carrier and priority order, not by obligation; DV-2 range-expands them so the count is 62, not 58.

### 12.4 What this catalogue is not

It is not evidence that any obligation holds, that any suite compiles, or that the contract behaves as written. **Acceptance tests executed: 0 — not by me, not by Agent 2, not by Agent 3, in this workspace or any other I can see.** Written against Agent 1 code: 0. Engine available: none (ADR-0012). The document checks in §13 are the only executed evidence in this document, and they are statements about text.

---

## 13. Document validation — executed

Nineteen checks on **this document's text**, run with `python3` over the published file. They are not tests of contract behaviour, and passing them says nothing about whether any obligation holds. Every result below is the actual output of the check listed; the check list is reproducible from the method column.

Command used for all checks: `python3 /tmp/dv3.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md`

| Check | Method | Result |
|---|---|---|
| **DV-1** obligations declared once and all covered | extract every obligation id (`TN-P-nn`, `TN-C-nn`, `TN-R-nn`, `TN-A-nn`) from §§7–9, dedupe, compare with the expected declared sets (17 P, 13 C, 6 R, 2 A) and with §11.2 | **PASS** — (38 rows; P17 C13 R6 A2) |
| **DV-2** case ids complete | extract `T-C05-nn`, range-expand `T-C05-35 … 39`, compare with `01…62`, report missing and extra | **PASS** — (62 distinct; missing []; extra []) |
| **DV-3** obligation rows well formed | every row of the four obligation tables has exactly 7 cells with a non-empty requirement and implementer cell | **PASS** — (38 rows, 7 cells each, implementer non-empty) |
| **DV-4** withdrawn ownership sentence absent | count occurrences of the withdrawn claim; must be 0 outside a quotation, and 0 in total in this revision | **PASS** — (0 occurrences of the withdrawn claim) |
| **DV-5** clause ids resolve | every `C05-x.y` reference resolves to a heading in §4 or a row in the §4.10 carried-forward table | **PASS** — (16 referenced, 16 defined, unresolved []) |
| **DV-6** suite arithmetic | count suite rows, sum the `Cases` column, compare with the stated totals (15, 62) | **PASS** — (15 suites, case sum 62) |
| **DV-7** external blockers still open | `TD-06`, `TD-09`, `TD-12` each appear in §14 with status `OPEN` | **PASS** — TD-06, TD-09, TD-12 present in §14.1, each still **OPEN** |
| **DV-8** execution honesty | enumerate every line containing `execut`; print the count; assert every mention concerns document checks or is negated, and that `0 executed` appears for acceptance tests | **PASS** — 8 lines contain `execut`; every one concerns a document check or is negated; `0 executed` present for acceptance tests |
| **DV-9** MEAD neutrality guard | every line containing `TDDCore` also names a MEAD | **PASS** — 2 lines mention `TDDCore`, both MEAD-qualified |
| **DV-10** tables well formed | every table block has a constant cell count per row | **PASS** — 29 tables, 0 malformed rows |
| **DV-11** implementer ↔ ownership mapping | extract every implementer-cell token, require membership in the six-token vocabulary of `C05-7.4`, and require each token's mapped agent to appear in the corresponding `C05-7.2` row | **PASS** — (6 role tokens, 38 cells checked, unknown tokens []) |
| **DV-12** field-class consistency | `VF` and `OF` blocks exist; `AxisNow` and `RemainingLocalSeconds` appear in `OF` and not in `VF`; `INV-1` names the versioned class; S2's equality assertion over `RemainingLocalSeconds` appears in no normative clause (only in the §3.1 quotation of the defect) | **PASS** — (VF/OF split ok; old phrase occurrences 1; INV-1 names versioned class ok) |
| **DV-13** aging-formula consistency | the `R(t)` form appears in `INV-2`, `TN-C-10` and T-C05-54; the endpoint form `(PhaseEndAxis − AxisNow) × ProducerRate` appears in `INV-2` and `TN-P-17` | **PASS** — (R(t) form in INV-2/TN-C-10/T-C05-54: [True, True, True]; endpoint form in INV-2 and TN-P-17: True, True) |
| **DV-14** publication-order determinism | `PO-3` names `n+1` and `n+2` in the phase-then-retime order; `TN-P-15` names the canonical order; EX-5 carries the (a)/(b)/(c) case markers | **PASS** — (PO-3 order phase→retime n+1→n+2; TN-P-15 canonical; EX-5 (a)(b)(c)) |
| **DV-15** bidirectional coverage | every obligation appears in §11.2 with ≥1 case; inverting §11.2 covers every case id 01…62 | **PASS** — (38 obligations mapped, cases covered 62, missing cases []) |
| **DV-16** directory composition | `DN-1` contains `whichever occurs first`, `Closed` and `invalidation`; `TN-R-06` exists and forbids timing, scheduling and emission | **PASS** — `DN-1` carries all three trigger strings; `TN-R-06` present and forbids timing, scheduling and emission |
| **DV-17** consumer information paths | §6.1 names AI, audio, montage and VFX with a verdict each; §6.2 has a row for VFX placement and a row for montage asset selection | **PASS** — four consumer rows with verdicts; §6.2 has the VFX-placement and montage-asset rows |
| **DV-18** resynchronisation status | `FTDDTelegraphResynchronisation` is declared in the §4.2 code block, referenced by `EN-3` and `TN-C-09`, and defined in §6.3 | **PASS** — `struct FTDDTelegraphResynchronisation` in §4.2; referenced by `EN-3`, `TN-C-09` and §6.3 |
| **DV-19** Agent 2's nine conditions traceable | the ledger carries rows for `C1`, `C2`, `C3`, `C4a`, `C4b`, `C4c`, `C5`, `C6`, `C7`, `C8`, `C9` (C4 splits into its three sub-corrections); the §1 table carries 11 correction rows; each condition id maps to at least one clause and one test id | **PASS** — (11 ledger rows covering C1-C9 (C4 as C4a/C4b/C4c); §1 table rows 11) |

**What this section proves: that the document is internally consistent as text.** It does not prove the contract is correct, implementable, or agreed. Those require review, code and an engine, in that order, and none of the three exists yet.

---

## 14. Dependencies and blockers

### 14.1 External blockers — unchanged, and not resolved by this revision

| ID | Dependency | Blocks | Status |
|---|---|---|---|
| **B-1** | **TD-06** — clock ownership and the shared axis | any code that stamps or ages timing | **OPEN** — TD |
| **B-2** | **TD-09** — parry-authority location and the MEAD-C/MEAD-A erratum | implementing the arbitration path | **OPEN** — TD |
| **B-3** | No engine, compiler or project in this workspace (ADR-0012) | executing any of the 62 cases | **OPEN** — Phase 0 |
| **B-4** | **TD-12** — canonical MEAD and the contract-layer owner | freezing the value types, the resynchronisation type and the read interface | **OPEN** — TD |
| **B-5** | U-07 / global enumeration (X-1 only) | nothing in C-05 | **OPEN**, conditional |
| **B-6** | U-15 damage-request spelling | C-03 only | **OPEN** — TD |
| **B-7** | U-14 `Status.Dead` grant | C-04 only | **OPEN** — registry |
| **B-8** | TD-13 save inventory | C-07 only | **OPEN** — Agent 3 |

### 14.2 Dependencies this revision makes visible

| ID | Dependency | Why it is visible now | Status |
|---|---|---|---|
| **B-9** | Agent 2's re-review of this exact blob | nine conditions are addressed in their words; consistency is not agreement | **OPEN** — requested in §18.1 |
| **B-10** | Agent 3's bounded reassessment of S2 **and** S3 | the S2 reassessment does not exist at `arena/c64fc525-tdd` (§0.2), so no A3 finding against S2 is known to be closed | **OPEN** — requested in §18.2 |
| **B-11** | `C05-6.3`'s three carriers are stated in full only in `A1-C05-S1` §6.3, and the clause is proposed rather than frozen and coupled to `C-04-4` | Agent 2's §5.4; it makes `TN-C-07` inherit both statuses | **`BLOCKED BY DEPENDENCY`** — the decision required is C-04's (`C-04-4` plus the registry's `Status.Dead` grant, B-7). `TN-C-07` remains implementable only once that decision exists; nothing else in C-05 depends on it |
| **B-12** | Cross-agent routing of the resynchronisation signal | the type is declared and normative, but delivery is consumer-local; routing it would need the contract layer's owner (TD-12) and a transport C-05 refuses | **OPEN, not proposed** |
| **B-13** | Ownership and registration of the `AttackTag` values | C-05 transports a tag value and defines/registers nothing; with no tag authored the field is empty and behaviour is unchanged | **OPEN** — registry/TD, non-blocking |
| **B-14** | Float comparison tolerance for `INV-2` assertions | `T-C05-54`/`T-C05-55` compare derived values; the tolerance is a test-fixture decision, not a contract one | **OPEN** — implementation-time, non-blocking |

**No status in §14.1 has changed since S1.** This revision claims no closure of TD-06, TD-09, TD-12, U-07, C-05 or any registry item. One dependency (B-11) is marked **`BLOCKED BY DEPENDENCY`** rather than resolved, per the instruction's stop condition: the correction it touches cannot be completed without a C-04 decision that is not mine to make, and every other correction proceeded independently of it.

---

## 15. Response to Agent 2's five questions — how each verdict should change

Concise, question by question. **No verdict here is mine to award**; this states what changed and why a reviewer could move from the S2 verdict, and it is Agent 2's to accept or refuse.

| Q | S2 verdict | What changed | Why it should move | Proposed verdict |
|---|---|---|---|---|
| **1** — does `C05-7.2` state your producer obligations accurately? | AGREE WITH CONDITIONS (C1, C2, C3) | `DN-1a` now says why the directory is not the second scheduler, in their own terms (holds no timing, schedules nothing, id→producer and liveness only) plus `TN-R-06` making it enforceable; `DN-1` deregisters on `Closed` **or** invalidation, whichever first, matching `RM-1` and covering stream-out without a graceful close; `PO-4`/`TN-P-16` define two transitions in one frame as two revisions, two messages, authored order, never collapsed — and `EX-10` shows the montage section-boundary case | All three conditions are text in the contract, not intentions, and each has a check (DV-16) and a test (T-C05-61, T-C05-23/24, T-C05-52/53) | **AGREE** |
| **2** — is `INV-1` implementable on your producers? | **DISAGREE** (C4a, C4b, C4c) | `INV-1` is now stated over an explicit **versioned field** set; `RemainingLocalSeconds` and `AxisNow` are the **observation-instant** class, governed by the new `INV-2` with the `A1-R4` §3.3(e) formula written into the contract; `TN-R-05` and `T-C05-46` corrected to match; `PO-3`/`TN-P-15` fix the same-frame order and `EX-5` is rewritten as cases (a)(b)(c) | Two pulls at one revision now return identical `VF` and `OF` values that differ by exactly Δ × `ProducerRate`; the compliant implementation is distinguishable from the violation again; and no two conforming producers can publish different sequences for the same frame | **AGREE** |
| **3** — does `Resynchronised` give your AI sufficient information? | AGREE WITH CONDITIONS (C5, C6) | `FTDDTelegraphResynchronisation` is declared with normative semantics and consumer-local delivery; `WindowKey` and `AttackTag` are carried as versioned fields, so a resync into `Active` now says whether the attack is blockable; §6.1 records the three-consumer necessity analysis and the two rejected alternatives | The signal is a type with a firing rule rather than an undeclared name, and it is actionable on arrival | **AGREE** |
| **4** — do the §7 consumer obligations match your consumers' requirements? | **DISAGREE** (C7, C8) | `C05-7.2` row 5 is split: AI, audio, montage-trigger and VFX-timing are C-05 consumers; VFX **placement** and montage **asset selection** are named as outside-C-05 resolution via `SourceEntityId` and `WindowKey`, with `TN-C-12` and `TN-C-13` making each half testable; `C05-2.8` now excludes transforms and asset references by name | The assignment no longer promises a surface the contract does not carry, and the three consumers blocked on identity are unblocked by fields that cannot age | **AGREE** |
| **5** — any conflict between §§6–8 implementer assignments and `A2-C05` §8? | AGREE WITH CONDITIONS (C9) | `C05-7.4` fixes a six-token role vocabulary mapping each token to an agent and to its `C05-7.2` row; DV-11 checks every implementer cell against that mapping and against the ownership table, not merely that the cell is populated | The two vocabularies are now mechanically comparable, which is the condition, and the check is stronger than the one it replaces | **AGREE** |

### 15.3 What I am correcting in my own earlier text, and what Agent 2 corrected in theirs

- **Mine:** S2's `INV-1` (Agent 2, C4a) — an aging field in an equality invariant; S2's `TN-R-05` and `T-C05-46` (C4b); S2's `EX-5` and the missing ordering rule (C4c); S2's `C05-7.2` row 5 (C7, C8); S2's silent omission of `WindowKey`/`AttackTag` (C6); S2's undeclared `Resynchronised` (C5); S2's DV-8 count (misreported instrument); S2's missing dependency on `C05-6.3`'s carriers (B-11).
- **Theirs, by their own account, and recorded rather than argued:** `A2-C05` §7.3 — *"a dilated window still ends at the same gameplay time"* — is withdrawn by Agent 2 in their §2.5 as inconsistent with the asymmetric-dilation correction; and `A2-C05` §8's listing of "animation montage selection" as a C-05 consumer capability is overstated in exactly the way their C8 finding says mine was. **Both are their corrections to make; I record them here only so the next reader does not find the contradiction and attribute it to this contract.**

---

## 16. Change log and supersession

### 16.1 Exactly what changed from `A1-C05-S2`

| Artefact | Change |
|---|---|
| `C05-2.2` | `FTDDTelegraphTiming` split into `OF` and `VF` blocks with the assignment written in comments; `FTDDTelegraphSnapshot` gains **`WindowKey`**, **`AttackTag`**; new **`FTDDTelegraphResynchronisation`** and `FTDDTelegraphOnResynchronised`; equality classes stated in the struct |
| `C05-2.3a` | Complete payload now explicitly includes identity fields |
| `C05-2.4` | Pull comment states the `VF`/`OF` behaviour of a pull answer; "no third method, no descriptor query" stated |
| `C05-2.5` `DN-1` | Deregistration triggers rewritten (`Closed` **or** invalidation, whichever first); **`DN-1a`** added — why the directory is not a scheduler |
| `C05-2.6` | **`INV-1` rewritten** over the versioned class; **`INV-2` added** (aging law and equivalence); `AD-1` justification corrected; `EN-3` retyped; **`RS-3` added** (a phase inside one frame may be unobservable) |
| `C05-2.8` | Adds "no transform, position, attach point or socket" and "no animation asset, montage or cue reference" |
| **`C05-2.9`** | **New** — `PO-1`…`PO-4`, the canonical publication order within a frame |
| `C05-7.2` | Row 5 split into rows 5, 6 and 7: C-05 consumers (Agent 1), C-05 consumers (Agent 2), outside-C-05 resolution (Agent 2) |
| **`C05-7.4`** | **New** — six-token role vocabulary, agent mapping, and the rule DV-11 enforces |
| `TN-P-07` | Corrected: monotonicity over **versioned-field** changes; `OF` drift does not bump |
| `TN-P-08`, `TN-P-11` | Cross-referenced to `PO-3` and `INV-2`; `TN-P-11` states what a live pull must and must not change |
| **`TN-P-15`**, **`TN-P-16`**, **`TN-P-17`** | **New** — same-frame order, collapsed boundaries, snapshot self-consistency |
| `TN-C-01`, `TN-C-08` | Justification corrected to the two field classes; `RS-3` added to `TN-C-08` |
| `TN-C-09` | Retyped to `FTDDTelegraphResynchronisation` |
| **`TN-C-10`**…**`TN-C-13`** | **New** — aging, identity/blockability consumption, VFX scoping, montage trigger-and-key |
| `TN-R-01` | Registration/deregistration triggers restated to match `DN-1` |
| `TN-R-05` | Corrected to `VF` identity plus `OF` consistency |
| **`TN-R-06`** | **New** — the directory schedules nothing |
| §10 | EX-5 rewritten as three named cases; EX-6 corrected for aging; EX-9 and EX-10 added |
| §12 | 15 suites, **62 cases**; T-C05-46 rewritten, 51–62 added, full catalogue with status |
| §13 | 19 document checks, including DV-11 (ownership mapping), DV-12/13 (field classes and formula), DV-14 (ordering), DV-15 (bidirectional coverage) |
| §14 | B-11 marked `BLOCKED BY DEPENDENCY`; B-12, B-13, B-14 added |
| Every obligation table | 38 obligations (17 P, 13 C, 6 R, 2 A), each with an implementer token from `C05-7.4` |

### 16.2 What did not change

The per-instance no-history pull recovery; `TM-1`; `EN-1`/`EN-2`; `AD-2`; `RS-1`/`RS-2`; `RM-1`/`RM-2`; the directory's content; `C05-2.1`; `C05-2.4`'s surface; the arbitration boundary and `TN-A-01`/`TN-A-02`; X-1's conditional status and its evidence bar; the ownership split except the wording C7–C9 required; every blocker's status; every earlier document.

### 16.3 Supersession

`A1-C05-S3` supersedes `A1-C05-S2` **by statement, not by edit**. S2 remains at `e5ddad6` / blob `bf6c8fb3…`, unmodified, as the record of what Agent 2 assessed; the S2 provenance-correction commits (`d24546d`, `5103a45`) remain in history and are not rewritten. Where S3 and S2 differ, S3 is the current C-05 text; where S3 is silent, S2 stands, and S2's silence defers to S1 only through `C05-7.1` and the §4.10 carried-forward table.

**Field-level supersessions worth naming:** `A1-R3` §3.2's `TimingRevision` (renamed at S2, meaning restated at S3); `A1-R4` §3.3(e) (now embedded as `INV-2` rather than referenced, with the same equation and the same prohibition on wall-clock aging); `A2-C05` §7.3's dilation sentence (withdrawn by Agent 2 themselves).

---

## 17. Publication and provenance record

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md` — **new file** |
| Version | 3.0 (`A1-C05-S3`) |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `a6b4e22999c7f8622c7c67e9cdc39e2f57565c20` |
| Blob at that commit | `077232368c42b2cd910be2c9642ba05cd7faa382` |
| Superseded | `A1-C05-S2` v2.0 at `e5ddad6`, blob `bf6c8fb3ddf3152d1627d3b6471278f57fc82541` — **unmodified** |
| Superseded (older) | `A1-C05-S1` v1.0 at `2bb729f`, blob `dcec9e1ae3efd4651c290636e8a4d6623603dc83` — **unmodified** |
| `A1-R1` / `A1-R2` / `A1-R3` / `A1-R4` / C-05-3 response | `25ab47c2…` / `5ee2769…` / `109331f3…` / `2cc548fa…` / `a94b49ef…` — **unmodified** |
| Agent 2's review answered | `ac498ce`, `Docs/AGENT2_REVIEW_A1C05_S2_V1.md` — **not modified** |
| Agent 2's other reviews and submission | `4c09980`, `7ea0a85`, `586152b`, `3ac438b` — read only, not modified |
| Agent 3's documents | `1eb613f` (S1 assessment), `58ec7fd` (recommendation), `docs/AGENT3_C05_3_…` — read only, not modified; **no S2 reassessment exists** (§0.2) |
| MEAD-A / MEAD-B / MEAD-C | read only; none moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| Contracts signed / frozen | **None** — C-05 remains proposed and unsigned |
| Code, Core types, project, merge, M0 | **None** |
| Acceptance tests | 62 cases `PROPOSED / NOT RUN`, **0 executed**; 19 document checks executed (§13) |

---

## 18. Handoff

### 18.1 To Agent 2 — targeted re-review of the nine conditions

Review **this exact blob**, not the branch tip: `077232368c42b2cd910be2c9642ba05cd7faa382` at `a6b4e22999c7f8622c7c67e9cdc39e2f57565c20`, path `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md`. Confirm or refuse **each condition individually** — C1 through C9 — and then give one overall verdict:

1. **C1** — is `DN-1a` plus `TN-R-06` an adequate answer that the directory is not the director your §7.1 rejected?
2. **C2** — do `DN-1`'s deregistration triggers now match `RM-1`, including stream-out without a graceful close?
3. **C3** — does `PO-4` / `TN-P-16` / EX-10 define "one transition" for collapsed montage section boundaries well enough to implement?
4. **C4a** — is `INV-1` over the versioned class, with `INV-2` carrying the aging law, the correction you specified — and is the two-class split acceptable to you in place of your Option A wording (the aging field is excluded *and* the formula is now in the contract)?
5. **C4b** — do `TN-R-05` and `T-C05-46` now assert what a conforming producer can actually deliver?
6. **C4c** — is the canonical order (phase at `n+1`, retime at `n+2`) the order your producers can publish, and is EX-5 unambiguous?
7. **C5** — is `FTDDTelegraphResynchronisation` declared at a fidelity that makes `TN-C-09` checkable, with consumer-local delivery acceptable?
8. **C6** — does carrying `WindowKey` and `AttackTag` as versioned fields give your AI, audio and montage consumers what they need, and is §6.1's rejection of the two alternatives sound?
9. **C7, C8** — are the VFX scoping and the montage trigger-and-key split stated correctly?
10. **C9** — does DV-11 check the mapping you asked for?

**No signature, freeze or acceptance is requested, and none is implied by a verdict.** A review is not a contract version.

### 18.2 To Agent 3 — targeted regression reassessment

Two jobs, and the first is a fact I cannot supply myself: **there is no S2 reassessment on `arena/c64fc525-tdd`** (§0.2). Please state what your S2 findings are, then reassess S3 against **this exact blob**:

1. Are your **previously closed** findings (`F1`–`F6` of S1, X-1's conditional status) still closed?
2. Does the **two-field-class split** (`INV-1`/`INV-2`) weaken the phase guarantee you originally required? My claim is that it does not, because phase is a versioned field — please test that claim rather than accept it.
3. Does carrying `WindowKey` and `AttackTag` disturb MEAD neutrality, the value-only rule, or any tag-ownership boundary you consider TD-owned?
4. Does `PO-3`/`PO-4` introduce any non-determinism, or any second source of truth about phase?
5. Does declaring `FTDDTelegraphResynchronisation` cross the line into an event bus, or is consumer-local delivery the right reading?

### 18.3 Status

`DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD is selected. TD-06, TD-09 and TD-12 are untouched and remain external blockers (B-1, B-2, B-4). B-11 is `BLOCKED BY DEPENDENCY` on a C-04 decision, and nothing else in this revision depends on it.** 62 acceptance cases are proposed and unexecuted; 19 document checks pass and prove nothing about behaviour. **No C++ was written, no runtime validation was performed, and none is claimed.**
