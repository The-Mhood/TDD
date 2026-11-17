# AGENT 2 — TARGETED REVIEW OF `A1-C05-S3` v3.0

**Review ID:** `TDD-A2-REVIEW-A1C05-S3-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — no signature, no freeze, no merge, no implementation, no MEAD
selection, no TD decision. **C-05 and U-07 remain open and I do not claim otherwise.**
**Outcome:** **`TARGETED REVISION`** (§11).

---

## 0. Provenance: the exact blob reviewed

### 0.1 The object of this review

| Field | Value |
|---|---|
| **Blob reviewed** | **`077232368c42b2cd910be2c9642ba05cd7faa382`** |
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md` |
| **Publishing commit** | **`a6b4e22999c7f8622c7c67e9cdc39e2f57565c20`** |
| Version | `A1-C05-S3` v3.0 |
| Lines | 946 |
| Branch | `arena/3bc206a0-tdd` (`origin/a1branch`) |

Verified:

```
$ git rev-parse a6b4e22999c7f8622c7c67e9cdc39e2f57565c20:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md
077232368c42b2cd910be2c9642ba05cd7faa382
```

Matches the requested blob exactly. **I did not review the branch tip.**

### 0.2 The tip, and why the difference is immaterial

The branch tip is `ec3c2af7455db614f7c9090fbe3c7033cd2fcaf8`; the file there is blob
`80060dea6685f2f17cae1128ef1a4532eed4e316`. I diffed the two blobs rather than assuming:

```
$ git diff 07723236 80060dea --stat
 docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md | 6 +++---
```

**3 insertions, 3 deletions**, and they are exactly the `PUB_COMMIT` / `PUB_BLOB` placeholder fill in
the §17 provenance table and the §18.1 handoff sentence. Every normative clause — `C05-2.x`,
`C05-7.x`, `INV-1`, `INV-2`, `PO-1…PO-4`, `AD-1/2`, `EN-1/2/3`, `TM-1`, `RS-1/2/3`, `RM-1/2`,
`TN-P-01…17`, `TN-C-01…13`, `TN-R-01…06`, `TN-A-01/02`, §§7–9, §11, §12, §13, §14 — is
**byte-identical**. Every finding below therefore applies to both `07723236` and the tip; only
§0.3's placeholder remark applies to `07723236` alone, and it is already remediated at the tip.

### 0.3 What I read

| Document | Commit | Purpose |
|---|---|---|
| **`A1-C05-S3`** (reviewed) | `a6b4e22`, blob `07723236…` | the object of this review |
| **My own review of S2** | `ac498ce`, `Docs/AGENT2_REVIEW_A1C05_S2_V1.md` | the nine conditions C1–C9 this review must adjudicate |
| **My own C-05 submission, `A2-C05-1.0`** | `3ac438b` | §7.6 `WindowKey`/`AttackTag` **Required**; §8 ownership list |
| `A1-C05-S2` | `e5ddad69`, blob `bf6c8fb3…` | what S3 changes; verified unmodified |
| `A1-C05-S1` | `2bb729f`, blob `dcec9e1a…` | `C05-6.3` carriers, `C05-7.1` withdrawal |
| `A1-R4` | `2cc548fa…` | §3.3(e) `R(t)` — the pre-existing source of `INV-2` |
| MEAD-A / MEAD-B / MEAD-C | `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` (mine), MEAD-B 247 lines, blob `f4935463…` | MEAD neutrality, TD-12 status |

I read all 946 lines. I re-ran every document check I could reproduce and report the results in §9.

---

## 1. Summary of verdicts

| # | Condition | Verdict | Section |
|---|---|---|---|
| **C1** | Directory is not a second scheduler | **AGREE** | §3.1 |
| **C2** | Deregistration matches `RM-1` incl. stream-out | **AGREE** | §3.2 |
| **C3** | `PO-4`/`TN-P-16` define two transitions in one frame | **AGREE** | §3.3 |
| **C4a** | `INV-1` over versioned class; `INV-2` carries aging | **AGREE WITH CONDITIONS** | §3.4 |
| **C4b** | `TN-R-05`/`T-C05-46` assert what a producer can deliver | **AGREE** | §3.5 |
| **C4c** | Canonical same-frame order; `EX-5` unambiguous | **AGREE WITH CONDITIONS** | §3.6 |
| **C5** | `FTDDTelegraphResynchronisation` normative and checkable | **AGREE** | §3.7 |
| **C6** | `WindowKey`/`AttackTag` carried; necessity sound | **AGREE WITH CONDITIONS** | §3.8 |
| **C7** | VFX scoping | **AGREE** | §3.9 |
| **C8** | Montage trigger vs asset split | **AGREE** | §3.10 |
| **C9** | `DV-11` checks the mapping I asked for | **DISAGREE** | §3.11 |

**Tally over the eleven corrections the document itself numbers (§1): 7 AGREE, 3 AGREE WITH
CONDITIONS, 1 DISAGREE.** Seven are fully resolved; three (C4a, C4c, C6) are resolved in substance
with residual defects; **C9 is not resolved as claimed**, and the three conditions I accept with
conditions carry the six remaining defects that must close before I would sign a successor (§10).

**I am not signing v3.0.** No verdict here is a signature, and none may be read as one later.

---

## 2. What S3 actually fixed — verified, not assumed

I checked each claim mechanically rather than accepting the §1 table. Results in §9. The short form:

| Claim | Verified |
|---|---|
| 38 obligations = 17 P + 13 C + 6 R + 2 A | **yes** — 38 rows, exactly that split |
| 62 cases, 15 suites | **yes** — case sum 62 over 15 suite rows; ids 01–62 complete, none extra |
| Every obligation → ≥1 case; every case → ≥1 obligation | **yes** — §11.2 inverts exactly onto 01–62, no orphans either way |
| `INV-2` producer form ≡ consumer form | **yes** — algebraically and numerically (§3.4) |
| `EX-9` table arithmetic | **yes** — all five rows reproduce exactly |
| DV-8's own count | **yes** — 8 lines contain `execut`, this time correctly |
| DV-4's zero-occurrence claim | **yes** — 0 |
| 6 role tokens, 38 cells | **NO** — see §3.11. 6 declared, **5 used** |

Three of my previous complaints were about instruments that reported their own numbers wrong
(S2's DV-8 claimed 10 where 16 lines matched). **S3's instruments report correctly, with the one
exception in §3.11**, and I record that as a real improvement rather than a courtesy.

---

## 3. C1–C9, individually

### 3.1 C1 — the directory is not a second scheduler · **AGREE**

**Clause:** `C05-2.5` `DN-1`, `DN-1a`; `TN-R-06`.

`DN-1a` states four separate negatives — *no timing, no phase, no revision, no window and no queue*;
*schedules nothing, orders nothing, emits nothing and wakes nothing*; consulted only to map an id
to its producer and answer liveness; and the observation that *a component that could schedule work
would need a clock, and the directory has none*. `TN-R-06` turns that into an obligation with a
failure mode rather than a disclaimer.

**My original defect:** in S2 the directory carried `SourceEntityId` and a liveness handle and the
document asserted only that it "holds no timing". That is a claim about the present, not a
constraint on the future. `TN-R-06` is the constraint. **Genuinely resolved.**

**The one thing I checked and did not find:** whether the directory could still become a
de-facto scheduler by being *polled* on a timer. `DN-1a` closes this — it emits nothing and wakes
nothing, so a poller learns nothing a direct map lookup would not. No remaining defect.

### 3.2 C2 — deregistration matches `RM-1` · **AGREE**

**Clause:** `C05-2.5` `DN-1`; `TN-R-01`; `RM-1` (§4.7).

`DN-1` now reads *"deregister on `Closed` **or on any invalidation of that producer's instances —
whichever occurs first**"*, and the §14.2 B-11 note plus §16.1 confirm the trigger list was rewritten
to mirror `RM-1` verbatim: `Closed`, producer invalidation, producer unload or stream-out, producer
death-cancel, world teardown. `TN-P-06` states the stream-out case explicitly — *"deregisters them
from the directory even when no `Closed` can be emitted"* — which was the exact hole. `TN-R-01`'s
timing cell now reads *"registration completes before a pull by id can succeed"*, which is the
ordering guarantee the old text lacked.

**Genuinely resolved.** I checked the reverse direction too: no clause still says deregistration
happens *only* on `Closed`. There is none.

### 3.3 C3 — two transitions in one frame · **AGREE**

**Clause:** `C05-2.9` `PO-4`; `TN-P-16`; `EX-10`.

`PO-4` is a genuine prohibition, not a description: *"may not collapse them, drop the intermediate
phase, merge the pair, or publish only the resulting phase"*, with the authoring-model escape hatch
closed (*"Where an authoring model can produce two section boundaries in one tick, both are
published"*). `TN-P-16` gives each violation a detection surface — the resulting message sequence
differs. `EX-10` runs the three consumer cases and correctly names `RS-3` for the pull-only
consumer: it sees Recovery at `n+2` and Active was never observable, which is a legitimate outcome
and not a lost state.

**One consequence I verified rather than accepted:** `RS-3` says a phase that opens and closes
within a frame *may be unobservable through a pull*. That is honest — it is a limit the contract
admits rather than hides, and it is consistent with `TN-C-08`'s instruction that a phase absent
from a pull is not a phase that did not occur. **Genuinely resolved.**

### 3.4 C4a — `INV-1` over versioned fields, `INV-2` carries the aging law · **AGREE WITH CONDITIONS**

**Clause:** `C05-2.6` `INV-1`, `INV-2`; `TN-P-17`; `TN-C-10`; `T-C05-54/55/56`.

This was my strongest finding and it is substantially fixed. `INV-1` is now stated over an
enumerated versioned set — `Phase`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`,
`ProducerRate`, `WindowKey`, `AttackTag` — plus instance identity, and explicitly excludes
`AxisNow` and `RemainingLocalSeconds`. `INV-2` puts the `A1-R4` §3.3(e) formula into the contract
instead of referencing it.

**I verified the consistency proof myself, two ways.**

Algebraically: substituting `R0 = (PhaseEndAxis − AxisNow) × Rate` into
`R(t) = R0 − (Axis(t) − AxisNow) × Rate` gives
`(PhaseEndAxis − AxisNow) × Rate − (Axis(t) − AxisNow) × Rate = (PhaseEndAxis − Axis(t)) × Rate`,
which is the producer form. Identical.

Numerically, the §10.9 `EX-9` table with `PhaseEndAxis = 4.0`, `AxisNow = 0.0`,
`ProducerRate = 0.05`, `R0 = 0.20`:

| Axis | Producer form | Consumer form | `EX-9` states | Match |
|---|---|---|---|---|
| 0.0 | 0.2000 | 0.2000 | 0.2000 / 0.2000 | ✔ |
| 0.2 | 0.1900 | 0.1900 | 0.1900 / 0.1900 | ✔ |
| 2.0 | 0.1000 | 0.1000 | 0.1000 / 0.1000 | ✔ |
| 4.0 | 0.0000 | 0.0000 | 0.0000 / 0.0000 | ✔ |
| 8.0 | 0.0000 | 0.0000 | 0.0000 / 0.0000, clamped | ✔ |

The identity survives the clamp at both ends. **The two-class split is acceptable to me in place of
my Option A wording** — the aging field is excluded from `INV-1` *and* the formula is normative in
`INV-2`, which is strictly stronger than what I asked for, because a formula can be tested where an
exclusion cannot.

`T-C05-55`'s wall-clock negative control and `T-C05-56`'s "a fixture in which the equal-revision
pull carries a `VF` change is rejected as a producer violation, not silently adopted" are both
correctly constructed.

#### Condition C4a-1 — `INV-2`'s equivalence is conditional on "within one revision"; state that as a precondition

**Defect.** `INV-2` is written unconditionally: *"Within any snapshot, `RemainingLocalSeconds =
max(0, (PhaseEndAxis − AxisNow) × ProducerRate)`"*. The algebra in §3.4 is correct **only while
`PhaseEndAxis` and `ProducerRate` are fixed**, which §3.4 itself says (*"The identity holds exactly
while `ProducerRate` and `PhaseEndAxis` are fixed, which is precisely what one revision
guarantees"*). But that qualifier is in the *rationale prose*, not in `INV-2`, and `INV-2` is the
clause that `TN-P-17` and `TN-C-10` both cite. A consumer ages a held snapshot across a `Retimed`
if it has not yet adopted the retime; `INV-2` as drafted tells it the aged value is still correct,
and it is not — the producer's own `RemainingLocalSeconds` will have been re-anchored at the new
rate.

This is not hypothetical: it is the ordinary case of a consumer holding `n` when `Retimed` at `n+1`
is in flight. `AD-1`/`TN-C-01` correctly *bumps* the revision, so the consumer will adopt `n+1`
when it arrives — but between the producer's retime and the consumer's adoption, `INV-2`'s
unconditional form asserts a value the producer no longer publishes.

**Closure condition.** Insert one sentence into `INV-2` itself: *"`INV-2` holds within a single
revision. When `ProducerRate` or any phase endpoint changes, the revision advances (`TN-P-07`) and
both forms re-anchor at the new `R0`; a consumer aging a snapshot across a revision change it has
not yet adopted is aging with stale `VF`, and `TN-C-10`'s rule applies only to the revision it
holds."* `TN-C-10` should echo the last clause. No structural change; one sentence in each of two
clauses.

#### Condition C4a-2 — the `VF` list has three homes and they must not drift

`INV-1` enumerates the seven versioned fields; §3.2 enumerates them again with the comment *"the
fields a `StateRevision` versions, and the only fields `INV-1` constrains"*; `FTDDTelegraphSnapshot`
(§4.2) carries them as `Phase`, `WindowKey`, `AttackTag` and the composed `Timing` sub-struct, with
the equality classes in a comment. Today all three agree — I checked field by field. That is a
maintenance hazard, not a present defect, and `DV-12` checks only that `AxisNow` and
`RemainingLocalSeconds` are in `OF` and not in `VF`, which would not catch a disagreement in the
other five.

**Closure condition (advisory, not blocking):** extend `DV-12` to extract the `VF` set from all
three locations and require set equality, printing the three sets. If the document prefers one
normative list and two references, say so and make the other two pointers rather than repetitions.

### 3.5 C4b — `TN-R-05` and `T-C05-46` · **AGREE**

**Clause:** `TN-R-05`, `T-C05-46`.

`TN-R-05` now reads *"returns `VF` content identical to every other observation at `R` (`INV-1`)
and an `OF` pair consistent with `INV-2` at its own call instant … it is never required to reproduce
an earlier observation's `OF` values."* `T-C05-46` was rewritten to assert versioned-field identity
across two pulls and one duplicated message at rev 3, plus `INV-2` consistency of each `OF` pair.

This is exactly the correction I specified, and it removes the contradiction with `TN-P-11`
(*"pull answers from live state at call time"*), which no conforming producer could have satisfied
while also reproducing a frozen `RemainingLocalSeconds`. **Genuinely resolved**, with the C4a-1
precondition as its only dependency — `TN-R-05`'s "consistent with `INV-2`" inherits whatever
`INV-2` says, so fixing `INV-2` fixes both.

### 3.6 C4c — canonical same-frame order, `EX-5` unambiguous · **AGREE WITH CONDITIONS**

**Clause:** `C05-2.9` `PO-1…PO-4`; `TN-P-15`; `EX-5` cases (a)(b)(c)(c′).

The order is now normative and total: all phase transitions in authored order, then all dilation
changes in applied order, one revision per message, never shared, never reversed. `EX-5` enumerates
(a) phase only, (b) retime only, (c) one of each, and adds (c′) out-of-order arrival, which I had
not asked for and which is correct. The rationale (b) — that the producer's internal application
order is *not observable at frame granularity*, so leaving it to the producer would let two
conforming producers emit different sequences — is the right reason and is the reason I gave.
**The ordering defect I raised is resolved.**

Two residual defects, both in the `EX-5` case (c) enumeration and its interaction with `PO-3`.

#### Condition C4c-1 — `EX-5` (c) omits the one loss case that is dangerous

`EX-5` case (c) enumerates *both received* and *only `n+2` received*. It does not enumerate
**only `n+1` received**. That is not a symmetric omission; it is the one case where the consumer
silently keeps aging a stale rate.

Worked through with the contract's own rules:

| | Consumer holds `n`, receives `PhaseChanged`@`n+1` only |
|---|---|
| `AD-1` | `n+1 > n` → adopt |
| `AD-2` | `n+1 == held + 1` → **no gap recorded** |
| `TN-C-09` | no gap → **no `Resynchronisation`** |
| `TN-C-10` | ages the held snapshot at the **pre-retime `ProducerRate`** |
| Detection | none — the retime at `n+2` never arrives, so nothing contradicts the stale rate |

The consumer is phase-correct and rate-wrong, indefinitely, with no diagnostic. Worse, §3.6's
rationale (c) asserts this case is safe: *"the first message of a same-frame pair already carries
the correct phase, so a consumer that loses the second is phase-correct and merely needs a
resync"* — but **nothing obliges a resync**, because `AD-2`'s trigger is an incoming revision
greater than `held + 1`, and no further revision ever arrives. The rationale names a resync the
contract does not require.

This is not confined to one frame. Any retime that is dropped in transport produces the same state,
and `PO-3`'s reordering makes it worse rather than better: for a frame containing
phase→retime→phase, the canonical sequence is both phases then the retime, so the `n+2` snapshot
*already contains a retime that was applied before the second phase transition*. A consumer
adopting `n+1` and `n+2` contiguously is then timing-correct but was briefly aged at the wrong rate,
and the document does not say which `ProducerRate` the intermediate `n+1` snapshot carries.

**Closure condition.** Add case **(d)** to `EX-5`: *"only `n+1` received — the consumer adopts, fires
entry once, records no gap, and ages at the `n+1` rate. It is phase-correct and, if the retime was
lost, rate-correct only until the next revision arrives."* Then state the **frame-boundary
guarantee** that makes this acceptable or close it: either (i) an obligation that a consumer
re-pulls once per frame while it holds any open instance, which bounds the staleness to one frame
and makes `TN-C-05`'s "one pull per gap" the wrong recovery path for this case, or (ii) a
producer obligation that a `Retimed` is never published in the same frame as a `PhaseChanged`
unless both are delivered over a channel with the same ordering guarantee, or (iii) an explicit
statement that the contract accepts one-frame rate staleness on message loss and that it is
undesirable-but-not-incorrect. **Any of the three closes it; silence does not.** Option (iii) is
the cheapest and I would accept it, but it must be written and `TN-C-10` must acknowledge it.

#### Condition C4c-2 — `PO-3` fixes the sequence but not the content of each message

`PO-3` and `TN-P-15` fix the *order* of messages within a frame. They do not say what `VF` content
the earlier message carries when the producer has already applied the later change.

Consider a frame containing Windup→Active **and** `CustomDilation` 0.05→0.20. Two readings are
available and the document permits both:

| | `n+1` carries | `n+2` carries | Consequence |
|---|---|---|---|
| **A** | new rate 0.20 | new rate 0.20 | `n+1` and `n+2` share `VF`, differ only in `StateRevision` — legal, but two revisions for one `VF` change is unusual |
| **B** | old rate 0.05 | new rate 0.20 | natural reading of "phase first, then the retime", and `n+2` is the message that announces the rate |

Reading **B** collides with `TN-P-11`: a pull taken between the two publications returns *live
state* with `VF` equal to *the instance's current revision*. If the producer has already applied
the dilation internally, the live state at revision `n+1` carries rate 0.20, while the published
`PhaseChanged`@`n+1` carries 0.05 — **the same revision with two different `ProducerRate` values**,
which is `INV-1` violated by a conforming producer. Reading A avoids this only if the producer also
withholds the internal rate change from live state until `n+2`, which nothing requires.

`T-C05-51` asserts the sequence `PhaseChanged@n+1, Retimed@n+2, Retimed@n+3` and that the consumer
adopts all three — it says nothing about the `VF` content of each message, so it cannot discriminate
A from B.

**Closure condition.** Add to `PO-3`, or as `PO-5`: *"Each message carries the complete snapshot at
its own revision. A message published before a later same-frame change reflects only the changes at
or before its revision, and the producer's live state must not contain a `VF` change not yet
covered by a published revision (`TN-P-11`)."* Then extend `T-C05-51` to assert the `ProducerRate` in
each of the three messages, so A and B are distinguishable by test. **This is one sentence plus one
assertion**, and without it `TN-P-11` and `PO-3` are jointly unsatisfiable under reading B while
`PO-3` never rules B out.

### 3.7 C5 — `FTDDTelegraphResynchronisation` normative and checkable · **AGREE**

**Clause:** `C05-2.2` struct declaration; `EN-3`; `TN-C-09`; §6.3.

The type is declared in the §4.2 code block with `LandedState` and the *no history* comment, is
referenced by `EN-3` and `TN-C-09`, and §6.3 defines its semantics. `TN-C-09` now has
`FTDDTelegraphResynchronisation` in the obligation text rather than the bare word
"`Resynchronised`", so the obligation names a type a compiler can see.

Delivery is consumer-local on `FTDDTelegraphOnResynchronised`, per consumer, with no transport — and
`B-12` records routing as a TD decision rather than pretending it is settled. **Genuinely
resolved**, and consumer-local delivery is acceptable to me: my AI needs to *know*, not to
*broadcast*, and a delegate it owns satisfies that.

**One note, not a defect:** `EN-3` says "exactly one resynchronisation per gap" but a gap is a
consumer-local notion with no identity in the type. `TN-C-09` carries the operational rule
(*"immediately on gap adoption, before any further entry evaluation"*) and `T-C05-57` tests
*"not re-raised for the same gap"*, which together are sufficient. I record the looseness so a
successor does not mistake it for precision.

### 3.8 C6 — `WindowKey` / `AttackTag` carried, necessity sound · **AGREE WITH CONDITIONS**

**Clause:** §6.1; `C05-2.2` struct; `TN-C-11`; `C05-7.4`.

The necessity analysis is done consumer by consumer against the requirements I actually submitted —
`A2-C05` §7.6 marks both **Required** — and the argument is correct: `AttackInstanceId` is unique per
firing so it cannot key authored data, `SourceEntityId` names the entity rather than the attack, and
three of the four named consumers need identity the snapshot previously did not carry. Both
rejected alternatives are rejected for the right reasons, and rejecting the descriptor query is
correct on my own submission's logic: it would be a second read surface with its own staleness
question, which is the problem `DN-1`'s expired handle already exists to solve.

**Two residual defects.**

#### Condition C6-1 — "constant for the lifetime" and "revision advances on every change" cannot both hold

Three clauses, mutually inconsistent as written:

| Clause | Says |
|---|---|
| §3.8 | "authored at `Opened` and **constant for the instance's lifetime**" |
| §6.1 alternative 3 | "Both are authored at `Opened`, **constant for the instance's lifetime**, and therefore versioned fields that cannot age" |
| `TN-P-07` | revision strictly increases on "**every change to `WindowKey` or `AttackTag`**" |
| `T-C05-62` | setup includes "`WindowKey` change, `AttackTag` change" |

If they are truly constant, `TN-P-07`'s clause can never fire — a dead norm — and `T-C05-62`'s
`WindowKey`-change and `AttackTag`-change rows are **unrepresentable scenarios that cannot be
tested**, so the case as specified cannot pass. If they can change, §3.8 and §6.1 are false, and
§6.1's justification ("constant, therefore versioned, therefore cannot age") loses its first
premise.

This matters beyond tidiness, because the whole answer to my C6 rests on the constancy: it is what
makes carrying identity in the snapshot safe rather than a second staleness surface.

**Closure condition.** Choose one and make all four agree.
*(i) Constant* — delete `TN-P-07`'s "and every change to `WindowKey` or `AttackTag`", and remove the
`WindowKey`/`AttackTag` change rows from `T-C05-62`, noting that identity is fixed at `Opened` and
therefore has no change transition to test. *(ii) Mutable* — replace "constant for the instance's
lifetime" with "fixed while the instance is open under one attack definition; a change of attack
identity closes the instance and opens a new one" in both §3.8 and §6.1, and state which revision
carries the new value. **I recommend (ii)**, because it also closes the case where a re-authored
attack definition changes the tag mid-instance, and because (i) makes `T-C05-62` partially
vacuous. Either is acceptable; the contradiction is not.

#### Condition C6-2 — audio ownership is stated twice with two different owners

| Location | Says |
|---|---|
| `C05-7.2` row 5 | **Agent 1** — "parry/block/dodge evaluation from the pull; camera and **audio cues**" |
| `C05-7.2` row 6 | **Agent 2** — "AI reaction; **audio cue selection**; montage switch trigger; VFX marker" |
| §6.1 consumer table | **Audio cue (Agent 2)** — "needs `WindowKey`" |

Row 5 is stale S2 text that the row-split did not clean: §5.2's own preamble says rows 5–7 were
split to fix exactly this overstatement, yet row 5 still claims audio. `TN-C-11` names Audio in the
`C05-7.4` mapping, but no obligation row says who *selects* the cue, and `TN-C-12`/`TN-C-13` do not
cover audio at all. **This is precisely the ambiguity area G asks about** — shared ownership between
two agents on one responsibility.

**Closure condition.** Amend row 5 to remove "and audio cues", leaving Agent 1 camera and
parry/block/dodge. If Agent 1 genuinely owns a distinct audio responsibility — for example
*camera-relative* audio occlusion, which is a level/world concern and plausibly mine — name it
explicitly in its own row with its own scope, so the split is by responsibility rather than by
splitting one noun. Silence in row 5 is not acceptable: as written, two agents own one thing.

### 3.9 C7 — VFX scoping · **AGREE**

**Clause:** `C05-2.8`; §6.2; `TN-C-12`; `T-C05-59`.

Timing and phase are C-05's; world placement and attachment resolve from `SourceEntityId` through
the owning actor, outside the contract; `C05-2.8` excludes "transform, position, attach point or
socket" by name. `T-C05-59`'s structural assertion that *no contract type carries a transform,
position, socket or attach point* is the right shape — it is a property of the type set, not of one
usage. **Genuinely resolved.**

### 3.10 C8 — montage trigger vs asset selection · **AGREE**

**Clause:** `TN-C-13`; `C05-2.8`; `T-C05-60`.

The split is correctly drawn: C-05 supplies *when* (the phase transition and its phase) and *which
attack* (`WindowKey`); the asset is selected from attack data keyed by `WindowKey`, outside the
contract. `TN-C-13` also states the negative — *"so is switching on a retime (a retime is not a
switch trigger)"* — which is the half that makes the split testable, and `T-C05-60` asserts the
retime raises **no** switch request. **Genuinely resolved.**

I note in passing that §15.3 records my own `A2-C05` §8 overstatement of "animation montage
selection" as withdrawn. That is accurate and I accept it; it belongs in the record.

### 3.11 C9 — `DV-11` checks the mapping I asked for · **DISAGREE**

**Clause:** `C05-7.4`; `DV-11`; `TN-C-12`, `TN-C-13` implementer cells.

My C9 asked for a check that maps each implementer-cell role to the agent `C05-7.2` assigns it.
`DV-11` does that. **It is nonetheless not the check the condition required, for two independent
reasons.**

#### 3.11.1 The check's own reported figure is wrong: 6 tokens declared, 5 used

`DV-11` reports *"6 role tokens, 38 cells checked, unknown tokens []"* and §5.4, §15, §16.1 and §18.1
all call it a **six-token** vocabulary. I extracted the implementer cell from all 38 obligation rows:

| Token | Declared in §5.4 | Appears in cells |
|---|---|---|
| `producer owner` | yes | 17 |
| `each consumer` | yes | 11 |
| `Agent 1, shared support` | yes | 2 |
| `Agent 1, subject to TD-09` | yes | 2 |
| `Agent 2, in its own systems` | yes | 2 |
| `contract layer, owner pending TD-12` | **yes** | **0** |

Five tokens are used; **`contract layer, owner pending TD-12` is declared and never used**, which is
consistent — the contract layer owns the types, not an obligation row, and `C05-7.2` row 3 covers it
— but it makes "6 role tokens, 38 cells checked" a misstatement of what the check found. A check
that prints the number of distinct tokens *observed* would print **5**. This is the same class of
error as S2's DV-8, which claimed 10 where 16 lines matched, and it is the reason I re-run claimed
instrument output instead of trusting it.

**This is a reporting defect, not a correctness defect**: `unknown tokens []` is true and the rule
in §5.4 is sound. It is nonetheless a defect in a document whose entire §13 exists to demonstrate
that its instruments are honest.

#### 3.11.2 The check is agent-level where the condition was row-level, so it cannot fail on the defect it was written for

`DV-11`'s stated test is *"require each token's mapped agent to appear in the corresponding
`C05-7.2` row"*. Rows 6 and 7 have the **same owner**:

| Row | Scope | Owner |
|---|---|---|
| 6 | Consumer integration — AI, audio cue selection, montage switch trigger, VFX marker timing | **Agent 2** |
| 7 | Resolved outside C-05 — VFX placement, montage and cue **asset** selection, tuning data | **Agent 2** |

`TN-C-12` (VFX timing) and `TN-C-13` (montage trigger) are C-05 **consumer obligations** and belong
to **row 6** — both are responsibilities the contract delivers, which is the entire point of the
C7/C8 split. Both are assigned the token `Agent 2, in its own systems`, which §5.4 maps to
**row 7 — outside C-05**. `DV-11` passes them, because row 7's owner is Agent 2 and the token's
mapped agent is Agent 2. Had they been mapped to row 6, it would also pass, because row 6's owner is
also Agent 2.

**The check cannot distinguish the two rows for any Agent-2 obligation.** That is not a stronger
version of "the cell is non-empty" for the two rows C9 was raised about — it is the same
non-discriminating outcome with more machinery. `TN-C-12` and `TN-C-13` are mis-mapped to the
outside-C-05 row while being the obligations that make the inside/outside distinction real, and the
document's own answer to my C7/C8 (that these halves are now testable) rests on that distinction
being recorded correctly.

**Closure condition.** Two changes, both small:
1. **Re-map `TN-C-12` and `TN-C-13` to row 6.** The token vocabulary needs no new entry if
   `Agent 2, in its own systems` is re-pointed to rows 6–7 jointly — but that reintroduces the same
   blindness, so add a distinct token, e.g. **`Agent 2, C-05 consumer`** → rows 6 (inside C-05),
   and keep `Agent 2, in its own systems` → row 7 (outside C-05) for the placement/asset half. Then
   the two rows are distinguishable by token, which is what makes the mapping checkable.
2. **Make `DV-11` row-level, not agent-level.** The test should be: *the token's mapped
   `C05-7.2` row index appears in the obligation's expected row set, and that row's owner matches.*
   Then a `TN-C-13` cell carrying the outside-C-05 token fails, which is the behaviour C9 asked for.
   Also print the count of **distinct tokens observed** as well as declared.

I would accept either the re-mapping with a row-level check, or a documented argument for why the
inside/outside split is carried by prose rather than by token — but not the present state, where the
document claims the mechanism enforces a distinction the mechanism cannot see.

---

## 4. Mandatory areas A–I

| Area | Verdict | Where |
|---|---|---|
| **A** — `VF`/`OF`, `INV-1`, `INV-2`, equal-revision discard, `TN-R-05`/`T-C05-46` | **PASS with 2 conditions** | §5.1 |
| **B** — `WindowKey`/`AttackTag` necessity, resync recoverability, ownership, duplicated truth | **PASS with 2 conditions** | §5.2 |
| **C** — `PO-1…PO-4` determinism, separate revisions, two-in-one-frame, sufficiency | **PASS with 2 conditions** | §5.3 |
| **D** — directory scope, not-a-scheduler, `Closed`/invalidation, destruction/unload | **PASS** | §5.4 |
| **E** — `FTDDTelegraphResynchronisation` sufficiency, consumer-local, no invented entries | **PASS** | §5.5 |
| **F** — AI/audio/montage/VFX responsibilities, trigger vs asset, dependent consumers | **FAIL (1 defect)** | §5.6 |
| **G** — `C05-7.2` vs `C05-7.4`, six tokens, 38 cells, shared ownership | **FAIL (2 defects)** | §5.7 |
| **H** — no silent MEAD selection, arbitration separate, no assumed-closed C-04/`Status.Dead` | **PASS** | §5.8 |
| **I** — 62 cases / 15 suites, missing, contradictory, untested obligations | **PASS with 2 conditions** | §5.9 |

### 5.1 Area A

`VF`/`OF` split verified field by field against `INV-1`, §3.2 and the §4.2 struct. `INV-1` now
constrains only versioned fields; `AxisNow` and `RemainingLocalSeconds` are in `OF` and in neither
`INV-1`'s list nor the struct's `VF` block — I checked the struct, not just the prose. Equal-revision
discard is safe: §3.5's four-step argument is correct, and its contrapositive (*"if the observation
differs in any `VF` field, then the revision differs"*) is the rule that makes `AD-1` sound rather
than lucky. `TN-R-05` and `T-C05-46` now assert what a producer can deliver. **The defect S2 had is
gone.** Conditions: C4a-1 (`INV-2` precondition) and C4a-2 (`VF` list in three places).

### 5.2 Area B

Necessity is argued per consumer and both alternatives are rejected for stated reasons; the
snapshot is the single source of truth for identity and `TN-C-11` forbids a second lookup surface,
which is the right obligation. Post-resync recoverability holds: `EX-7` shows a resync landing with
identity intact, and `T-C05-57` asserts the AI reads `WindowKey` and `AttackTag` from the landed
snapshot with no second lookup. No duplicated source of truth for identity exists. Conditions:
C6-1 (constancy contradiction) and C6-2 (audio ownership).

### 5.3 Area C

`PO-1…PO-4` are total over the three frame-content cases and deterministic — no case is left to the
producer, which was the defect. Separability of revisions is explicit (*"never a shared revision"*)
and `TN-P-13` requires every phase transition to advance by exactly one even when nothing else
changed. Two-in-one-frame is `PO-4`/`TN-P-16`/`EX-10` and I accept it. Sufficiency fails only at the
edges: C4c-1 (the unenumerated only-`n+1` loss case) and C4c-2 (`PO-3` fixes order not content).

### 5.4 Area D

`DN-1`/`DN-1a` limit the directory to association plus liveness and prove the negative four ways;
`TN-R-06` makes it an obligation; `TN-R-01`'s timing cell orders registration before a resolvable
pull. `Closed` and invalidation both deregister, whichever first, and `TN-P-06` covers stream-out
with no graceful close. Destruction: `TN-P-05` invalidates before the producer stops being valid,
`RM-1` makes teardown a non-message observed as a `false` pull and an unresolvable id, and `RM-2`
tells the consumer to treat that as closed without error. **No defect found.**

### 5.5 Area E

The type is declared, normatively referenced by two clauses, and defined in §6.3; delivery is
consumer-local on a delegate each consumer owns, with no transport and no bus. `EN-3` and `TN-C-09`
forbid synthesising entries for unobserved phases and `TN-C-09` bounds it to one per gap, raised
before any further entry evaluation. `T-C05-57` tests single-fire and non-re-raise. No invented
phase-entry events anywhere: `EN-1` covers baseline with no entry, `EN-2` bounds entry to once per
`(instance, phase)`, and `EX-10` explicitly declines to invent Active for a consumer that only saw
Recovery. **No defect found.**

### 5.6 Area F — **FAIL**

AI, montage and VFX are correctly scoped and their consumers are not dependent on a field the
contract excludes: VFX placement resolves from `SourceEntityId`, montage assets from attack data
keyed by `WindowKey`, and `C05-2.8` excludes transforms and asset references by name. The trigger
vs asset-selection split is right for montage.

**Audio fails.** Row 5 assigns "audio cues" to Agent 1, row 6 assigns "audio cue selection" to
Agent 2, and §6.1's consumer table puts the audio consumer under Agent 2 and says it needs
`WindowKey`. There is no obligation row covering audio cue selection, so `TN-C-12`/`TN-C-13`'s
guarantee that each half is testable does not extend to audio at all. A reader implementing audio
cannot tell from `C05-7.2` which agent owns it. See C6-2 for the closure condition.

### 5.7 Area G — **FAIL**

`C05-7.2` has 9 rows; `C05-7.4` declares 6 tokens and specifies 38 obligation cells. The vocabulary
is a real improvement over S2, where implementer cells mixed agent names and roles freely. But:
**5 tokens are used and 1 is declared-but-unused** while the document reports 6 (§3.11.1), and
**`DV-11` is agent-level where the condition required row-level**, so it cannot fail on the
`TN-C-12`/`TN-C-13` mis-mapping it was written to catch (§3.11.2). On conflicting or ambiguous
shared ownership: rows 6 and 7 share the owner Agent 2 with different scopes, which is legible in
prose but not encoded in the token, and row 5/row 6 share the noun "audio" with different owners,
which is not legible at all.

### 5.8 Area H — **PASS**

No MEAD is selected: `C05-7.1` states the neutrality rule, `DV-9` guards it, the two `TDDCore`
mentions are both MEAD-qualified, and §18.3 says *"No MEAD is selected"*. `C05-7.2` row 3 names the
three candidates with their three different consequences (Agent 3 under MEAD-C, unassigned under
MEAD-A, absent under MEAD-B) rather than picking one — accurate, and it is where my own MEAD-A keeps
no `TDDCore` module. Arbitration is separate: `TN-A-01` reads the attacker's phase on the
hit-resolution path from live producer state, off the arbitration path, and `TN-A-02` keeps the
telegraph out of it; `C05-6.1` is carried forward unchanged and `C05-2.8` excludes arbitration by
name. No unresolved C-04 or `Status.Dead` dependency is assumed closed: `C05-6.3`'s carriers are
carried forward marked *"`PROPOSED — NOT FROZEN`, coupled to `C-04-4`"*, `B-7` records the U-14
`Status.Dead` grant as **OPEN — registry**, `B-11` is marked **`BLOCKED BY DEPENDENCY`** with the
required decision named as C-04's, and §14.1 states *"No status in §14.1 has changed since S1"*.
`TN-C-07`'s implementer cell is `each consumer`, and `B-11` explains that nothing else in C-05
depends on it. **The one thing I looked hard for and did not find is a claim of closure anywhere in
§14 or §18.** The document claims none.

### 5.9 Area I

62 cases over 15 suites, verified by parse: suite case-sum 62, ids 01–62 complete with none extra,
no case in two suites, no case in no suite. Obligation coverage is genuinely bidirectional: 38
obligations all appear in §11.2 with at least one case, and inverting §11.2 covers all 62 — I had to
fix my own range regex twice (the `T-C05-35 … T-C05-39` form is prefixed on both ends) before the
count reconciled, which is a note on how easy this is to get wrong rather than a defect. All 62 are
`PROPOSED / NOT RUN`, 0 executed, and §12 says so at the head and per row. No obligation without a
test. Two conditions: the ordinary ones from C4c-1 (case (d) is missing) and C4c-2 (`T-C05-51` does
not assert message content), plus the untestable rows of `T-C05-62` under C6-1.

---

## 6. The ten §18.1 questions, answered

| # | Question | Answer |
|---|---|---|
| **1** | Is `DN-1a` + `TN-R-06` adequate that the directory is not my §7.1 director? | **Yes.** Four independent negatives plus an enforceable obligation. The defect was a description of the present; this is a constraint on the future. |
| **2** | Do `DN-1`'s triggers match `RM-1`, including stream-out with no graceful close? | **Yes.** The trigger list mirrors `RM-1` verbatim, `TN-P-06` states the stream-out case explicitly, and `TN-R-01` orders registration before a resolvable pull. |
| **3** | Does `PO-4` / `TN-P-16` / EX-10 define "one transition" well enough to implement? | **Yes.** `PO-4` prohibits collapse in four phrasings and closes the authoring-model escape; `EX-10`'s three consumer rows are correct, including the honest `RS-3` admission. |
| **4** | Is `INV-1` over the versioned class with `INV-2` carrying the law the correction I specified — and is the two-class split acceptable in place of my Option A wording? | **Yes to the split, with two conditions.** The split is strictly stronger than my wording because a formula is testable and an exclusion is not. Conditions C4a-1 (`INV-2`'s precondition is unstated) and C4a-2 (`VF` list in three places). |
| **5** | Do `TN-R-05` and `T-C05-46` assert what a conforming producer can deliver? | **Yes.** `VF` identity plus `INV-2` consistency, no byte identity, and the contradiction with `TN-P-11` is gone. Inherits C4a-1 through `INV-2`. |
| **6** | Is the canonical order (phase `n+1`, retime `n+2`) the order my producers can publish, and is `EX-5` unambiguous? | **Order: yes, and it is the order I asked for.** `EX-5`: **no, not unambiguous** — case (d), only `n+1` received, is missing and is the dangerous one (C4c-1); and `PO-3` fixes sequence but not the `VF` content of each message (C4c-2). |
| **7** | Is `FTDDTelegraphResynchronisation` declared at a fidelity that makes `TN-C-09` checkable, with consumer-local delivery acceptable? | **Yes and yes.** A named type with `LandedState`, referenced from the obligation, tested by three cases. Consumer-local is right for my AI: it needs to know, not to broadcast. |
| **8** | Do `WindowKey`/`AttackTag` as versioned fields give my AI, audio and montage consumers what they need, and is §6.1's rejection of the two alternatives sound? | **The fields: yes** — identity is what my AI lacked after a resync and what audio and montage need to key assets. **The rejection: sound**, including rejecting the descriptor query. **But two defects remain**: C6-1 (constancy contradicts `TN-P-07`/`T-C05-62`) and C6-2 (audio has two owners). |
| **9** | Are the VFX scoping and montage trigger-and-key split stated correctly? | **Yes, both.** `TN-C-12` with `SourceEntityId` for placement and a structural assertion on the type set; `TN-C-13` with the retime-is-not-a-trigger negative and `T-C05-60` asserting no switch on retime. |
| **10** | Does `DV-11` check the mapping I asked for? | **No.** It checks agent agreement where I asked for row agreement, and because rows 6 and 7 share the owner it cannot fail on the mis-mapping of `TN-C-12`/`TN-C-13`. It also reports six tokens where five are used. See §3.11. |

---

## 7. Correction ledger — resolved vs unresolved

| Condition | S3's claim | My verdict | Residual |
|---|---|---|---|
| C1 | resolved | **resolved** | — |
| C2 | resolved | **resolved** | — |
| C3 | resolved | **resolved** | — |
| C4a | resolved | **resolved in substance** | C4a-1, C4a-2 |
| C4b | resolved | **resolved** | via C4a-1 |
| C4c | resolved | **partly resolved** | C4c-1, C4c-2 |
| C5 | resolved | **resolved** | — |
| C6 | resolved | **partly resolved** | C6-1, C6-2 |
| C7 | resolved | **resolved** | — |
| C8 | resolved | **resolved** | — |
| C9 | resolved | **NOT resolved** | §3.11.1, §3.11.2 |

**Seven of eleven corrections are fully resolved (C1, C2, C3, C4b, C5, C7, C8). Three are resolved
in substance with residual defects (C4a, C4c, C6), and C9 is not resolved as claimed.** Seven
distinct defects, six of them closable by wording changes in existing clauses and one (the `PO-3`
content rule) needing one added sentence plus one test assertion.

**Nothing here reopens a settled requirement.** Every condition above is a gap in a clause that
already exists, in the direction the clause was already going. I am not asking for C-05 to be
redesigned and I do not think it needs to be.

---

## 8. What S3 got right that I want on the record

Three things, because a review that lists only defects misrepresents the work.

1. **The `INV-2` correction is better than what I asked for.** I asked for the aging field to be
   excluded from `INV-1`. S3 excluded it *and* wrote the aging law into the contract as a normative
   formula with a consistency proof. An exclusion cannot be tested; a formula can. `T-C05-55`'s
   wall-clock negative control follows directly from that and would not have been possible under my
   wording.
2. **`EX-5` case (c′) is a case I did not ask for and should have.** Out-of-order arrival of a
   same-frame pair is the realistic transport outcome and the document handles it correctly
   (consume in revision order; the stale `n+1` is discarded).
3. **The document is honest about its own limits.** `RS-3` admits a phase can be invisible to a
   pull. `B-11` is marked `BLOCKED BY DEPENDENCY` instead of being quietly absorbed. §13 says in
   terms that passing 19 document checks *"does not prove the contract is correct"*. And this time
   **the instruments report their own counts correctly** — I verified DV-2, DV-4, DV-6, DV-8, DV-9,
   DV-15 and the §11.2 inversion independently, and all reconcile, with the single exception in
   §3.11.1. That is a real improvement over S2 and it is the reason my remaining findings are about
   substance rather than about arithmetic.

---

## 9. Document claims I independently re-verified

Everything below I ran myself against blob `07723236`. Where a check's claim and my result differ,
the difference is reported in §3.11.1 and nowhere else.

| Claim | My method | Result |
|---|---|---|
| 38 obligations, 17 P / 13 C / 6 R / 2 A | parse `| **TN-x-nn` rows from §§7–9 | **38**, split exact |
| 62 cases, 15 suites, sum 62 | parse suite rows, sum `Cases` | **62**, 15 suites |
| Case ids 01–62 complete | regex all `T-C05-nn` | 62 distinct, no gaps, none extra |
| §11.2 bidirectional | invert mapping both ways | 38 obligations covered, 62 cases covered, no orphans |
| No case in two suites | build case→suite map | none |
| `INV-2` equivalence | algebra + numeric at 5 axis values | identical, incl. both clamps |
| `EX-9` table | recompute all 5 rows | all 5 match |
| DV-8 count | count lines containing `execut` | **8** — matches |
| DV-4 zero-occurrence | count withdrawn claim | **0** — matches |
| DV-9 `TDDCore` neutrality | count lines, check MEAD qualifier | 2 lines, both qualified — matches |
| DV-11 six tokens | extract 7th cell of 38 rows | **5 used, 1 declared-only — does NOT match** |
| `VF`/`OF` membership in the struct | read §4.2 block | correct; `OF` fields absent from `VF` |
| `PhaseEndAxis` defined | search all uses | derived selector, defined at §3.3 — sound |

**These are document-text checks, not acceptance tests.** No contract behaviour is exercised by
this review or by the test file that accompanies it. **None of the 62 cases is run, and I do not
claim any passed.**

---

## 10. Remaining defects and their closure conditions

Consolidated, in the order I would fix them. **Six are wording; one needs a sentence plus an
assertion.**

| # | Defect | Clause | Closure condition |
|---|---|---|---|
| **D-1** | `EX-5` (c) omits only-`n+1`; §3.6 rationale (c) names a resync nothing obliges | `EX-5`, §3.6, `TN-C-10` | Add case (d) and one of options (i)/(ii)/(iii) in C4c-1 |
| **D-2** | `PO-3` fixes message order but not message content; readings A and B both permitted, B violates `INV-1` via `TN-P-11` | `PO-3`, `TN-P-15`, `T-C05-51` | Add the content rule (C4c-2) and assert `ProducerRate` per message in `T-C05-51` |
| **D-3** | `WindowKey`/`AttackTag` "constant for the lifetime" contradicts `TN-P-07` and `T-C05-62` | §3.8, §6.1, `TN-P-07`, `T-C05-62` | Choose constancy or mutability and make all four agree (C6-1) |
| **D-4** | Audio owned by Agent 1 in row 5 and Agent 2 in rows 6/§6.1; no obligation covers cue selection | `C05-7.2` row 5, row 6, §6.1 | Remove "audio cues" from row 5, or give Agent 1 a named distinct responsibility (C6-2) |
| **D-5** | `TN-C-12`/`TN-C-13` mapped to row 7 (outside C-05) while being C-05 consumer obligations of row 6 | `C05-7.4`, `TN-C-12`, `TN-C-13` | Add a distinct inside-C-05 token and re-map both (C9) |
| **D-6** | `DV-11` is agent-level, cannot fail on rows 6 vs 7; reports 6 tokens where 5 are used | `DV-11` | Row-level check; report distinct tokens observed (C9) |
| **D-7** | `INV-2` states its equivalence unconditionally; the one-revision precondition is only in rationale prose | `INV-2`, `TN-C-10` | Insert the precondition sentence into `INV-2` (C4a-1) |

**None of D-1…D-7 requires reopening a settled requirement or changing the architecture.** D-3 and
D-4 are the two that change what an implementer would do, and both are resolved by picking one of
two readings the document already contains. D-1 is the only one with a behavioural consequence I
consider material: a consumer can silently age at a stale rate with no diagnostic.

**D-5 and D-6 are the same defect seen twice** and must be fixed together — re-mapping the tokens
without making `DV-11` row-level would leave the check unable to confirm the fix.

---

## 11. Overall outcome

# `TARGETED REVISION`

**What that means here, precisely:** seven of the eleven corrections are fully resolved and I accept
them without reservation; three more (C4a, C4c, C6) are resolved in substance and carry six named
conditions. **C9 is not resolved.** **Every one of the seven is closable without reopening a settled requirement** — six
by wording changes inside existing clauses, one by a sentence plus a test assertion. That is a
targeted revision, not a redesign, and not a dependency block.

**Why not `PASS`:** I cannot say all nine conditions are resolved when C9 is not, when `EX-5`
asserts a resync the contract does not require, and when `WindowKey`'s constancy is contradicted by
two clauses that depend on it.

**Why not `BLOCKED BY DEPENDENCY`:** nothing I have found requires a TD decision. `B-11` is
genuinely blocked on C-04 and S3 correctly says so and correctly contains it — but none of D-1…D-7
touches `TN-C-07` or `C05-6.3`. `B-12` (resync routing) and `B-13` (tag ownership) are marked open
and are non-blocking to every obligation in this contract as drafted: consumer-local delivery needs
no routing decision, and C-05 transports a tag value while defining and registering nothing, so an
empty tag leaves behaviour unchanged. **The blockers are real and correctly recorded; they do not
gate this verdict.**

**What would move me to `PASS`:** D-1…D-7 closed, plus `DV-11` made row-level with the token
re-mapping. Then I would review the next blob on its own terms and say so — but that will be a
fresh review, not a carry-forward of this one. **Agreement is not inferred from the direction of
travel and my earlier "would sign" language, if any, does not bind this verdict.**

---

## 12. What I did and did not do

**Did:**
- Reviewed exactly blob `07723236…` at `a6b4e229`, verified by `git rev-parse`, and diffed it to the
  tip to prove the 3/3-line difference is placeholder fill only.
- Read all 946 lines.
- Re-derived `INV-2` algebraically and numerically rather than accepting §3.4's proof.
- Re-ran 13 document claims; reported the one that does not reconcile (§3.11.1).
- Extracted all 38 implementer cells and all 62 case ids by parse, not by eye.
- Answered all ten §18.1 questions individually.

**Did not:**
- Edit `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md` or any A1 document. All seven are byte-identical
  to what I was given.
- Merge, sign, freeze or implement C-05. **I am not signing v3.0.**
- Select a MEAD or make any TD decision. My own MEAD-A is disclosed where it is relevant (§5.8) and
  I selected nothing.
- Close U-07. It remains open.
- Run, or claim to have run, any of the 62 acceptance cases. **0 executed, by me, as by A1.**
- Overwrite or amend any prior review. `Docs/AGENT2_REVIEW_A1C05_S2_V1.md` is untouched at `ac498ce`.
- Reopen a settled requirement. Every condition here is a gap inside a clause that already exists.
- Infer agreement from the fact that A1 accepted my nine findings. I re-derived every claim I
  accepted, and where my re-derivation disagreed with A1's instrument, I said so (§3.11.1).

**Status:** `DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD
is selected.** TD-06, TD-09 and TD-12 remain external blockers and are untouched by this review.

---

*End of review. `TDD-A2-REVIEW-A1C05-S3-001` v1.0.*
