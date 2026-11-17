# AGENT 2 — INDEPENDENT REVIEW OF `A1-C05-S2` v2.0

**Review ID:** `TDD-A2-REVIEW-A1C05-S2-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — no signature, no freeze, no merge, no implementation, no MEAD
selection, no TD decision. **C-05 and U-07 remain open and I do not claim otherwise.**

---

## 0. Provenance: the exact blob reviewed, and the correction I excluded

### 0.1 The object of this review

| Field | Value |
|---|---|
| **Blob reviewed** | **`bf6c8fb3ddf3152d1627d3b6471278f57fc82541`** |
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V2.md` |
| **Publishing commit** | **`e5ddad6965e06b179061d8cebb6ffecf59829224`** |
| Version | `TDD-A1-C05-SUCCESSOR-002` v2.0 (`A1-C05-S2`) |
| Lines | 642 |
| Branch | `arena/3bc206a0-tdd` (`origin/a1branch`) |

Verified:

```
$ git rev-parse e5ddad6965e06b179061d8cebb6ffecf59829224:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V2.md
bf6c8fb3ddf3152d1627d3b6471278f57fc82541
```

Matches the requested blob exactly. **I did not review the branch tip.**

### 0.2 The correction I was told to exclude, and proof that excluding it is safe

The branch tip is `5103a451d452d7c7ef85863aa889421861b9603d`; the file there is blob
`30a98b88f7d1f4e30cd50068f3cfe207522c7d1a`. The user's instruction is that the later provenance
correction "changes MEAD provenance rows only. It does not change the substantive contract text."

**I verified that rather than assuming it.** The complete diff from the reviewed blob to the tip is
**6 insertions, 3 deletions**, in two hunks:

| Hunk | Where | What |
|---|---|---|
| 1 | §0 provenance table, line 18 | one MEAD row → three rows with verified path/blob pairs |
| 2 | §16 Publication | `PUB_COMMIT` / `PUB_BLOB` placeholders → filled values, plus a provenance-correction row |

Both hunks are in **§0** and **§16**. Every contract clause — `C05-2.x`, `C05-7.x`, `INV-1`, `AD-1/2`,
`EN-1/2/3`, `TM-1`, `RS-1/2`, `RM-1/2`, `TN-P-01…14`, `TN-C-01…09`, `TN-R-01…05`, `TN-A-01/02`, §§5–14
— is **byte-identical** between `bf6c8fb` and the tip. The user's statement is accurate to the byte.

**Consequence for this review, stated so a reader knows exactly where I stand:** every finding below
about contract text applies **identically** to the tip, and every finding about provenance applies
**only** to `bf6c8fb`. I flag which is which. Two provenance defects in `bf6c8fb` are already fixed by
the correction, so I report them as **already-remediated, no action requested** rather than as open
defects — reporting them as open would be a false accusation against a document that has already
fixed them.

### 0.3 What else I read, in full

| Document | Commit | Purpose |
|---|---|---|
| **My own C-05 submission, `A2-C05-1.0`** | `3ac438b32fcd73ceb22dcd81385356f7b8b39644` | Q4 and Q5 — the producer/consumer requirements I actually submitted |
| `A1-C05-S1` v1.0 | `2bb729f2cbd525e3cd7f5f5d46b3b9cc72c803d0` | what S2 changes; blob `dcec9e1a…` verified unmodified |
| `A1-R4` (aging formula source) | `142cabdb…`, blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75` | §3.3(e) `R(t)` — **load-bearing for Q2** |
| M1 v1.4 lines 796–797 | `22c29dad` | per-instance precedent |
| My prior reviews | `4c09980`, `7ea0a85`, `586152b` | continuity; none modified |

---

## 1. The five verdicts

| Q | Question | Verdict |
|---|---|---|
| **1** | Does `C05-7.2` accurately state my producer obligations? | **AGREE WITH CONDITIONS** |
| **2** | Is `INV-1` implementable on my producers? | **DISAGREE** |
| **3** | Does `Resynchronised` give my AI sufficient information? | **AGREE WITH CONDITIONS** |
| **4** | Do the §7 consumer obligations match my consumers' requirements? | **DISAGREE** |
| **5** | Any conflict between §§6–8 implementer assignments and `A2-C05` §8? | **AGREE WITH CONDITIONS** |

**Two DISAGREE, three AGREE WITH CONDITIONS.** Neither DISAGREE is a rejection of the correction
direction — both corrections are right in intent and I say so. Both failures are in obligations that
are **unimplementable or unsatisfiable as written**, which is a different and more fixable category
than a wrong design.

**No signature, freeze or acceptance is implied by any verdict.** A review is not a contract version.

---

## 2. Q1 — Does `C05-7.2` state my producer obligations accurately?

### Verdict: AGREE WITH CONDITIONS

### 2.1 What I checked, and against what

`C05-7.2` row 2 assigns me, on my enemy producers: "the pull answer, the per-producer id list,
revision advancement and publication, registration and deregistration", implementing
`TN-P-01 … TN-P-14`. I checked each clause against what my own submission actually proposed.

| Obligation | My `A2-C05` §8 position | S2 requires | Compatible? |
|---|---|---|---|
| Producer authority | "I own the producer… mutation authority" (§8) | `C05-2.1` producer is sole authority; `C05-7.2` row 1 gives me production | **yes — no change to my authority** |
| Enemy telegraph production | `ATDDEnemyBase` StateTree tasks, `UTDDBossPhaseGraph` (§8 Producers) | row 1: "the authored attack, its montage windows, when a telegraph opens, changes phase and closes, and every cancellation decision" | **yes — verbatim in scope** |
| Cancellation reasons | `SourceDied`, `SourceUnloaded`, `AttackInterrupted` (§7.3) | `ETDDTelegraphCloseReason { Natural, Cancelled, Interrupted, ProducerInvalidated, SourceDied }`; `TN-P-04` | **yes — every reason I named has a counterpart** (§2.3) |
| Pull answer | I proposed messages only (`Begin`/`Update`/`End`/`Cancelled`); no pull | `TN-P-11`, `TN-R-02` require a live pull answer | **yes — additive, and I asked for a query in `C05-Q4`** |
| Revision advancement | none — I had no revision field | `TN-P-07`, `TN-P-13` | **acceptable but new** — see §2.4 |
| Complete-snapshot messages | I argued for carrying `StartGameplayTime` on **every** message specifically for late-subscriber correctness (§7.4: "I would rather carry one extra float on every message") | `TN-P-14` / `C05-2.3a`: every message carries the complete snapshot | **yes — this is the same argument, generalised, and I made it first** |
| Registration/deregistration | **I never proposed a directory.** My design was explicitly "No central telegraph director — it would become a second scheduler competing with StateTree" (§7.1) | `DN-1` requires producers register on `Opened` and deregister on `Closed`, via a directory Agent 1 implements | **acceptable — see §2.2, this is the condition** |
| One `Retimed` per dilation change, no coalescing | I had no retime message; my §7.3 said "a dilated window still ends at the same gameplay time" | `TN-P-08`: never batch, coalesce, throttle or defer; hitstop boundaries not exempt | **yes, and it corrects my §7.3** — see §2.5 |

**Every substantive obligation is compatible with what I submitted.** Three of them (`TN-P-14`,
`TN-P-08`, the pull) are things I asked for or argued for, in some cases before S2 existed. I want that
on the record because the natural reading of "gives Agent 2 obligations it did not sign up for"
(§3.6) overstates the delta: **I signed up for most of this. The delta is the directory and the
revision field.**

### 2.2 Condition 1 — the directory is an obligation I did not propose, and it contradicts my §7.1

`DN-1` requires my producers to register on `Opened` and deregister on `Closed` into a **directory
implemented by Agent 1**. My submission's §7.1 says the opposite: *"No central telegraph director — it
would become a second scheduler competing with StateTree."*

I am not refusing. I am recording that this is a **reversal of my stated position**, and that the
reversal is defensible only because of how narrowly S2 scopes the directory: `TN-R-01` limits it to
"the id, `SourceEntityId` and one weak liveness handle — no timing, no phase, no revision", and
`C05-2.5` says it "never serves timing through the handle". That is not a scheduler. My objection was
to a director that *competes*; a liveness map does not compete.

**Condition 1 (satisfied by one sentence):** `C05-2.5` must state why the directory is not the
second scheduler my §7.1 warned against — specifically that it holds no timing, schedules nothing,
and is consulted only for id→producer resolution. As written a reader must infer that from
`TN-R-01`'s negative list. One sentence removes the appearance of a reversal.

### 2.3 Condition 2 — `TN-P-06` (stream-out) has no directory counterpart, and it matters to me

`TN-P-06`: "Stream-out invalidates only that producer's instances." `DN-1`: "deregister on `Closed`."

**A streamed-out enemy does not necessarily emit `Closed`** — `TN-P-05` makes teardown invalidation
"best effort", and `TN-P-06`'s own row says deregistration of its own ids. But `DN-1` names only
`Closed` as the deregistration trigger. So the sequence *enemy streams out without a graceful close*
leaves an association record whose liveness handle expires, and `DN-1` covers that with "answers
`false` for an expired handle" — **which is correct, and the two clauses do compose.** I record it
only because `DN-1`'s trigger list ("on `Opened` and deregister on `Closed`") looks exhaustive and is
not. This is a wording precision, not a defect: `TN-R-01`'s "teardown drops all" and the expired-handle
rule close it.

**Condition 2:** `DN-1` should say "*register on `Opened`, deregister on `Closed` or producer
invalidation — whichever occurs first*", matching `RM-1`'s own list.

### 2.4 Condition 3 — `StateRevision` is a new field on a type I own the implementation of

`C05-2.2` renames `TimingRevision` → `StateRevision` and widens its meaning. I have no objection to
the rename or the widening — it is the correct fix for the defect Agent 3 found, and §2.3's
justification ("a field called `TimingRevision` whose normative meaning is the whole state is the same
ambiguity in a smaller place") is sound reasoning.

**The condition is not about the field; it is about `TN-P-13`'s "exactly one" under an authored
montage.** A montage can transition phase on a montage *section* boundary, and a single frame can
contain a section end and the next section's start. Whether that is *one* transition or *two* is a
question about my authoring model that S2 does not answer. `TN-P-13` says "exactly one" per
transition without defining what counts as one when two section boundaries land in the same frame.

**Condition 3:** `TN-P-13` needs a sentence on collapsed boundaries: *"two phase transitions that
occur within one frame are two revisions; a producer may not collapse them, and if its authoring
model can produce two transitions in one frame it must publish both."* Otherwise "exactly one" and
"two revisions if simultaneous" (§5.5 EX-5) leave the implementer to guess — and Q2 shows this is
not hypothetical.

### 2.5 Where S2 corrects my submission, and I accept the correction

My `A2-C05` §7.3 said: *"`EndGameplayTime` is in **undilated** gameplay time; a dilated window still
ends at the same gameplay time."* **That is wrong.** Under producer dilation, a window of `0.20 s`
local time at `ProducerRate = 0.05` occupies `4.00` axis-seconds, not `0.20` — this is the exact
arithmetic A1-R4 §2.2 and my own prior reviews established. `TN-P-08` and `C05-2.2`'s `ProducerRate`
field supersede my sentence.

**I withdraw `A2-C05` §7.3's "a dilated window still ends at the same gameplay time."** It was
written before the asymmetric-dilation defect was derived and it is inconsistent with the correction I
subsequently accepted. S2 does not cite it as an error, but it should be noted that S2's text is right
and my earlier text was wrong, or the next reader will find the contradiction and attribute it to S2.

### 2.6 Small defects in the obligation tables

| # | Finding | Severity |
|---|---|---|
| **Q1-a** | `TN-P-13`'s cell contains a stray `*` before the closing pipe ("…the consumer already holds.*"), which renders as a literal asterisk before the table delimiter. Cosmetic; it suggests the row was edited in place. | trivial |
| **Q1-b** | `TN-P-13` and `TN-P-07` overlap by design and §6.1's footnote says so — **good**. But the footnote says "*the missing case is the one that caused this revision*", which is accurate and is the right way to document deliberate redundancy. No action. | none |
| **Q1-c** | `C05-7.2` row 2 assigns me "revision advancement and publication" — but `TN-P-13`'s implementer column says only "producer owner", not naming the agent. The table in §6 does not name agents at all, only roles. §7 preamble names agents in prose. **This is fine and arguably better** (it survives a producer-ownership change), but `C05-7.2` and the tables use different vocabularies for the same assignment. | low |

### 2.7 Q1 conclusion

**AGREE WITH CONDITIONS.** The obligations are accurate, three of them are things I asked for, and one
of them corrects an error in my own submission which I withdraw. The conditions are: (1) say why the
directory is not the director I objected to; (2) make `DN-1`'s deregistration triggers match `RM-1`;
(3) define what "one transition" means when two section boundaries collapse into a frame.

---

## 3. Q2 — Is `INV-1` implementable on my producers?

### Verdict: DISAGREE

**`INV-1` as written is false under ordinary passage of time, not because of any producer defect.**
This is the most consequential finding in this review and it is a one-line fix.

### 3.1 What `INV-1` says

> **INV-1.** For a given `AttackInstanceId`, two observations carrying the same `StateRevision` are
> **identical in every pull-visible field** — phase, all timing endpoints, `ProducerRate`,
> **`RemainingLocalSeconds`**.

And `TN-R-05`: "A pull at revision `R` returns content identical to every other observation of that
instance at `R`". And `T-C05-46` asserts two pulls and one duplicate message at rev 3 are
"**byte-identical** in every pull-visible field".

### 3.2 Why it cannot hold

`RemainingLocalSeconds` does not stand still between revisions. Its lifecycle is defined by the aging
rule at **`A1-R4` §3.3(e)**, which S2 does not restate but does not repeal:

> `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)`

with "*a consumer must age by axis elapsed multiplied by `ProducerRate`*". Compute it:

Producer at `ProducerRate = 0.05`, windup `R0 = 0.20` local s, `StateRevision = 1` for the whole
windup (no phase change, no retime — `TN-P-13` and `TN-P-07` both correctly say the revision does not
move):

| Frame | `Axis(t) − AxisNow` | `RemainingLocalSeconds` | `StateRevision` |
|---|---|---|---|
| 0 | 0.0 | **0.2000** | 1 |
| 1 | 0.2 | 0.1900 | 1 |
| 2 | 0.4 | **0.1800** | 1 |

**Two pulls at revision 1 return `0.2000` and `0.1800`.** That is a difference of `0.02` s — a full
frame at 50 Hz — and it is produced by the passage of axis time alone, with no producer error
whatsoever.

**So `INV-1` is violated by every producer that correctly implements its own aging rule, on every
frame, for every open telegraph.** `TN-P-07`'s failure clause — "An observation at an equal revision
with different content is a producer violation" — would therefore diagnose every conforming producer
as in violation. An obligation whose compliant implementation is indistinguishable from its violation
is not implementable.

### 3.3 The contradiction is three-way, and `TN-R-05` sharpens it

| Clause | Requires | Incompatible with |
|---|---|---|
| `INV-1` / `TN-R-05` | same revision ⇒ **identical** `RemainingLocalSeconds` | — |
| `A1-R4` §3.3(e) (not repealed) | `R` **decreases** with axis time within a revision | `INV-1` |
| `TN-P-11` | pull answers "from **live state at call time**" | `INV-1` / `TN-R-05` |

`TN-P-11` and `INV-1` cannot both hold for a field that ages. S2 wrote `TN-R-05` to protect `INV-1`
without noticing that the field list in `INV-1` includes the one field that is a *function of time*
rather than a stored value.

### 3.4 Why this is blocking rather than an editorial nit

`INV-1` is the load-bearing justification for equal-revision discard:

- `TN-C-01`: "Because of `INV-1` an equal revision carries identical content, so discarding never
  loses a change."
- §2.2 consequence 2: "**Equal-revision discard is now always safe.**"
- `TN-C-01`'s commutativity argument.

If `INV-1` is false for `RemainingLocalSeconds`, then **equal-revision discard does lose a change** —
a consumer at revision 1 that discards a pull returning `0.1800` because it already holds revision 1
with `0.2000` keeps a stale remaining time. The magnitude is one frame per discarded pull, which is
small; the principle is not, because the entire correction rests on "equal revision means nothing
changed" being true.

**The defect is not the phase fix. The phase fix is correct and I accept it.** `StateRevision` over
the whole state closes Agent 3's finding exactly as claimed. The defect is that S2 included an
**aging field** in an **equality invariant** without saying how the two coexist.

### 3.5 The narrowly necessary correction

One of two, and I recommend the first because it preserves the invariant's strength:

> **Option A (recommended) — exclude the aging field from the identity, and say so.**
> Amend `INV-1`: "…identical in every pull-visible field **except `RemainingLocalSeconds`, which is a
> derived function of the observation instant and is defined by `R(t) = max(0, R0 − (Axis(t) − AxisNow)
> × ProducerRate)`**. Formally: two observations at the same `StateRevision` have identical
> `AxisNow`, all endpoints, `ProducerRate` and phase; `RemainingLocalSeconds` may differ between them
> only by the axis time elapsed between the two observations, multiplied by `ProducerRate`, and by
> nothing else." Add the same qualifier to `TN-R-05` and to `T-C05-46`'s "byte-identical" assertion,
> which otherwise cannot pass.

> **Option B — make the field non-aging.** Store `R0` (remaining local **at emission**) and require
> consumers to age it themselves. This makes `INV-1` literally true but changes the published field's
> meaning and moves the aging arithmetic — which A1-R4 §3.3(e) deliberately placed on the producer —
> onto every consumer. I do not recommend it, and I note that `C05-2.2`'s own comment already says
> `RemainingLocalSeconds` is "producer-local remaining time of the CURRENT phase", i.e. a live value.

**Whichever is chosen, `T-C05-46` must match.** An assertion of byte-identity across `RemainingLocalSeconds`
cannot be satisfied by any conforming producer.

### 3.6 The second part of Q2: phase changes without dilation, and simultaneous changes

**Phase change with no dilation change — implementable, and the correction is correct.** My attacks
change phase on montage section boundaries: Windup→Active, Active→Recovery, with `CustomDilation`
unchanged across all three in the common case. `TN-P-13` requires a revision bump and a `PhaseChanged`
carrying the new snapshot; `EX-1` shows exactly this (rev 1 → rev 2 at unchanged endpoints); `T-C05-43`
asserts it. **No ambiguity. I can implement this and I want it** — it fixes a real defect, because
under S1 my Active transition was invisible to a consumer that missed the message.

**Genuinely simultaneous phase and timing change — NOT defined, and this is a real gap for my
producers.** §5.5 `EX-5` is titled "phase change and retime in the same frame" and says:

> Two observable changes → two revisions, **2** (Active, new rate) **then** **3** (a second retime if
> the dilation changes again).

Read carefully: the primary sentence describes **one** phase change and **one** retime, then assigns
revisions 2 **and** 3 — but rev 3 is parenthetically described as "a second retime if the dilation
changes again", i.e. a *third* change. So in the one-phase-change-plus-one-retime case the text does
not say whether the revisions are `2` and `3`, or whether the phase change and the retime share a
revision. `TN-P-13`'s ordering column says "a transition and a retime in the same frame are two
revisions", which implies `2` and `3` — but `EX-5`'s own numbering then leaves rev 2's phase ambiguous
(it says rev 2 is "Active, new rate", i.e. **both** changes at rev 2, contradicting the two-revision
rule).

**Then the consumer-side arithmetic in `EX-5` breaks.** The example says a consumer "receiving only
rev 3 from a held 1: `3 > 2` → gap". But `AD-2` says gap when `incoming > held + 1`; from held 1,
`incoming` 3 gives `3 > 2` → gap. That is correct arithmetic. **But if the phase change and the
retime are two revisions and a consumer receives rev 3 while holding rev 1, it has missed the phase
change** — so the gap flag is right and the resync is right. The problem is only that a reader cannot
tell from `EX-5` whether rev 2 exists.

**This is the ordering ambiguity Q2 asked me to identify, and it is not hypothetical.** If my boss
phase graph applies a dilation change in the same frame it advances the montage section — a hitstop
expiring on the frame a phase ends is the ordinary case — I must know which order to publish in, and
S2 does not say.

**Condition 4 (Q2's narrowly necessary correction):** `EX-5` must be rewritten to unambiguously
enumerate the revisions for **(a) one phase change only, (b) one retime only, (c) one of each in one
frame**, and `TN-P-13` must state the publication order for case (c): *"a phase transition and a
retime in the same frame are published in that order — `PhaseChanged` at `n+1`, `Retimed` at `n+2` —
because the phase transition is a lifecycle fact and the retime is a subsequent adjustment to it."*
Without a stated order, two conforming producers can publish `(phase, timing)` or `(timing, phase)`,
and a consumer holding rev `n` sees either at `n+1`, which changes which message fires entry.

### 3.7 Q2 conclusion

**DISAGREE.** `TN-P-13` and the phase half of `INV-1` are implementable, correct, and wanted. `INV-1`
**as a whole is not implementable** because it includes an aging field in an equality invariant,
which makes every conforming producer a violator on every frame (§3.2) and undermines the
equal-revision-discard safety it exists to justify (§3.4). `EX-5` leaves same-frame ordering
ambiguous for case (c) (§3.6). Both fixes are narrow; neither touches the architecture.

---

## 4. Q3 — Does `Resynchronised` give my AI sufficient information?

### Verdict: AGREE WITH CONDITIONS

### 4.1 What the signal carries, and what my AI actually needs

`EN-3` / `TN-C-09`: `Resynchronised(AttackInstanceId, Phase)` — "carries the phase it has landed in and
no transition history"; zero `PhaseEntered` fires; exactly one resync per gap;
`bStateGapObserved` set until close.

My AI's defensive requirement, from `A2-C05` §7.6, is **not** "which phases did I miss". It is:

| My need | Source | Does `Resynchronised` + snapshot supply it? |
|---|---|---|
| Is a telegraph currently open on this enemy? | §7.6 `InstanceId` Required | **yes** — the consumer holds the instance |
| Which **phase** is it in, so I choose block vs dodge vs hold? | §7.6 `Begin`/`End` Required | **yes** — `Phase` is the signal's payload |
| How much **time** remains to decide? | §7.6 `StartGameplayTime` Required, "late-subscriber correctness" | **yes** — from the adopted snapshot's endpoints and `AxisNow`, aged per A1-R4 §3.3(e) |
| Which **attack** is it, for per-attack response tuning? | §7.6 `WindowKey` **Required** — "per-attack tuning" | **NO — see §4.3** |
| Is it blockable or must I dodge? | §7.6 `AttackTag` **Required** — "block vs dodge vs unblockable" | **NO — see §4.3** |
| Was it cancelled, and why? | §7.6 `CancelReason` Required | **yes** — `TM-1` + `ETDDTelegraphCloseReason` |

**For the recovery question proper — "can I act correctly across a gap?" — the answer is yes.**
Knowing the current phase plus the remaining time is sufficient to choose a defence. **I do not need
the history**, and `RS-1`'s refusal to carry it is correct: what I would do with "you missed Active"
is nothing I cannot do with "it is now Recovery".

**One genuine information loss worth naming, and it is not a defect:** a consumer resyncing into
`Recovery` cannot tell whether the attack *fired* while it was blind. That matters for post-hoc
telemetry, not for the defensive decision, and reconstructing it would require exactly the history
`RS-2` forbids. **I accept the limitation.** I note it so nobody later claims the signal is complete.

### 4.2 Condition 5 — `Resynchronised` is named and never declared

`EN-3`, `TN-C-09`, `EX-3`, `T-C05-45`, `T-C05-50` and §2.9 all reference `Resynchronised`, and §2.9
says it "*needs no new transport*". But **no type, enum or struct is declared for it anywhere in the
document** — `grep` for a declaration returns nothing. Every other published artefact in §4.2 is a
concrete C++ struct.

This is not pedantry: `TN-C-09` makes it normative ("a resync after a contiguous adoption is a
violation"), `TN-C-09` requires "exactly one" per gap, and neither is checkable without knowing
whether `Resynchronised` is a delegate, a return code or a consumer-internal callback. **Two of
S2's own new test cases (`T-C05-45`, `T-C05-50`) assert on an undeclared artefact.**

**Condition 5:** declare it with the other value types, even at the same fidelity as
`FTDDTelegraphMessage`, or state explicitly that it is a consumer-internal notification with no
contract-layer type and therefore that `TN-C-09`'s "exactly one" is a self-check rather than a
contractual obligation observable by another agent. Either is acceptable; the current state is both.

### 4.3 Condition 6 — `WindowKey` and `AttackTag` are absent, and they are the two Required fields I cannot do without

This is the same finding as Q4, so I state it once here and cross-reference it.

`C05-2.2`'s `FTDDTelegraphSnapshot` carries: `AttackInstanceId`, `SourceEntityId`, `Phase`, `Timing`.
`FTDDTelegraphTiming` carries: `AxisNow`, three endpoints, `ProducerRate`, `RemainingLocalSeconds`,
`StateRevision`. **Neither carries `WindowKey` or `AttackTag`.**

My `A2-C05` §7.6 marks both **Required** for the defensive consumer, and §7.2 gives the reason for
`WindowKey`: "*Lets Agent 1 tune a parry response per attack type, persisted in data*" — and, for me,
lets the AI choose a per-attack response. `AttackTag` is Required for "*Block vs dodge vs unblockable*".

**Across a gap, `Resynchronised` carries `Phase` only.** With no `AttackTag`, my AI resyncing into
`Active` knows an attack is active but **not whether it can be blocked** — which is the one decision
the phase is supposed to enable. That is an actual consumer requirement that cannot be met, and it is
the answer to Q3's "identify any requirement that cannot be met".

**Two ways to close it**, and I do not care which the TD-12 owner picks:

- **(i)** add `WindowKey` (an `FName`) and `AttackTag` (an `FGameplayTag`) to `FTDDTelegraphSnapshot`;
  or
- **(ii)** state that per-attack identity is resolved by the consumer from `SourceEntityId` + the
  attack's own data, and that C-05 deliberately does not carry it.

**(ii) is legitimate and I would accept it** — but it must be *stated*, because `TN-C-07`'s style
elsewhere shows S2 cares about naming carriers, and here it silently omits two.

### 4.4 Q3 conclusion

**AGREE WITH CONDITIONS.** For the recovery question as posed — can my AI act correctly after being
blind — **yes**, and `Resynchronised`'s refusal to carry history is right. Conditions: (5)
`Resynchronised` must be declared or explicitly demoted to self-check; (6) `WindowKey`/`AttackTag`
must be carried or their absence stated with a resolution path. Condition 6 is a real hole in a
recovery path: a resync that says "Active" without saying "unblockable" is a resync my AI cannot act on
correctly.

---

## 5. Q4 — Do the §7 consumer obligations match my consumers' requirements?

### Verdict: DISAGREE

### 5.1 The four consumers S2 names, checked one at a time

`C05-7.2` row 5 assigns me "AI reaction to the player's telegraph, audio cue, VFX marker, montage
selection". My `A2-C05` §8 names exactly those four ("Agent 2 audio cue; Agent 2 VFX marker; animation
montage selection" plus the AI). So the **list is accurate** — S2 read my submission correctly.

| My consumer | What it needs from a pull | Supplied by §7? |
|---|---|---|
| **AI reaction to the player's telegraph** | current phase, remaining time, per-attack identity, blockability | phase ✅, time ✅, **identity/blockability ✗** (§4.3) |
| **Audio cue** | phase transitions at the moment they occur, and the *attack type* to select the cue | phase transitions ✅ (`TN-C-03`), **identity ✗** |
| **VFX marker** | phase + **world position/attach point** of the telegraph | **✗ nothing in the contract carries a position or an attach target** |
| **Montage selection** | **which montage** to play — an animation asset reference, not timing | **✗ by design; see §5.3** |

### 5.2 The VFX marker requirement is genuinely unmet, and it is not a timing requirement

`FTDDTelegraphSnapshot` carries `SourceEntityId` — a `FGuid`, not a transform, deliberately, per
`C05-2.8`'s value-only rule. A VFX marker must be placed **at the attack's origin**, which is not
derivable from `SourceEntityId` alone for an attack whose origin is a weapon socket or a projectile
spawn point.

**I am not asking C-05 to carry transforms.** That would violate `C05-2.8` and the value-data rule, and
it is not a timing contract. **The correct answer is that the VFX marker resolves the attach point
from the actor, via `SourceEntityId`, outside C-05.** That is fine — but §7 says nothing about it, and
`C05-7.2` row 5 assigns me "VFX marker" as a C-05 consumer, which implies C-05 supplies what the marker
needs. It does not.

**Condition 7:** `C05-7.2` row 5 should scope my VFX consumer to "VFX marker **timing and phase**",
and state that placement is resolved from `SourceEntityId` outside the contract. Otherwise the
implementer assignment promises a surface that does not exist.

### 5.3 Montage selection is assigned to me as a C-05 consumer and cannot be satisfied by C-05 at all

`C05-7.2` row 5 names "montage selection" among my C-05 consumer responsibilities. My `A2-C05` §8
also names it. **Both are wrong in the same way**, and I should say so about my own submission rather
than only about S2's.

Montage selection needs to know **which montage to play** — an animation asset, selected by attack and
by phase (a windup anim versus an active anim). C-05 carries a phase and timing, not asset references,
and `C05-2.8` forbids it carrying anything else. **So "montage selection" is a C-05 *trigger*, not a
C-05 *consumer capability*:** C-05 tells the montage system *when* to switch; the montage system knows
*what* to switch to from the attack's own authored data, keyed by `WindowKey`.

Which means: **montage selection is a consumer that needs `WindowKey` and does not get it.** This is
the third consumer blocked on the same missing field as §4.3, and it strengthens that condition from
"one Required field I would like" to "three of my four named consumers cannot work without it".

**Condition 8:** either carry `WindowKey` in the snapshot (§4.3 option (i)), or correct `C05-7.2` row 5
and my own `A2-C05` §8 to describe montage selection as a C-05 **trigger** whose "what" comes from
attack data keyed by `WindowKey` — provided by the producer through a path C-05 does not define. The
second is acceptable and is arguably the honest description; but as written, the implementer
assignment and the contract surface disagree.

### 5.4 The §7 obligations themselves are correct and I accept all nine

Separating the assignment question from the obligation question: `TN-C-01` … `TN-C-09` are, as
obligations, **correct and implementable on my consumers**. Specifically:

- `TN-C-01` strict-greater discard — accept, **conditional on §3.5's `INV-1` fix**, because
  "equal revision carries identical content" is its stated justification.
- `TN-C-02` baseline, `TN-C-03` at-most-once — accept. This matches my §7.4 honesty rule ("It must
  not treat the first `Update` as a start") and is the right generalisation of it.
- `TN-C-04` gap flag, `TN-C-05` single-pull recovery, `TN-C-06` removal-is-closure — accept. `TN-C-06`
  is exactly my §7.3 cancellation semantics plus `TM-1`, and `TM-1` is a real fix: without it my
  `Cancelled` at an unchanged revision would be discarded as stale.
- `TN-C-07` Dead precedence — **accept, with a scoping note**: it depends on `C05-6.3`'s "three
  carriers of S1 §6.3", and S2 does not restate the carriers (§4.9 carries only a one-line statement).
  Since `C05-6.3` is marked `PROPOSED — NOT FROZEN` and touches C-04 via `C-04-4`, `TN-C-07` inherits
  that status. **Not a blocker; a dependency to keep visible** — §14's blocker list has U-14/B-7 but
  not "the carriers are defined only in S1".
- `TN-C-08` no-history — accept, and it is the clause that keeps `RS-1` honest.
- `TN-C-09` resync — accept as an obligation, conditional on condition 5 (declared type).

### 5.5 Q4 conclusion

**DISAGREE.** Eight of nine obligations are right and I accept them. The disagreement is about the
**implementer assignment in `C05-7.2` row 5 promising a surface that does not exist**: three of my
four named consumers (AI, audio, montage) need per-attack identity that the snapshot does not carry,
and the fourth (VFX) needs placement that the contract deliberately does not carry. Both are fixable by
narrowing the assignment and stating the resolution path — or by carrying `WindowKey`.

---

## 6. Q5 — Any conflict between §§6–8 implementer assignments and `A2-C05` §8?

### Verdict: AGREE WITH CONDITIONS

### 6.1 The comparison, side by side

| Artefact | My `A2-C05` §8 | S2 `C05-7.2` / tables | Conflict? |
|---|---|---|---|
| Enemy production | "Agent 2 for the producer (enemy AI owns its own attack telegraph)" | row 1: Agent 2 | **none — identical** |
| Producer-side implementation | "I own the producer" | row 2: "the owner of that producer: Agent 2 on its enemy producers" | **none — identical** |
| Consumption (parry/block) | "Agent 1 for consumption (parry/block)" | row 5: "parry/block/dodge evaluation… Agent 1" | **none — identical** |
| Publishers of shared types | "Agent 3/TD (event type)" | row 3: "the contract layer… TD-12 (Agent 3 under MEAD-C; unassigned under MEAD-A; absent under MEAD-B)" | **none — S2 is more precise, and its precision is correct** (§6.3) |
| Directory / resolution | **not proposed by me** | row 4: Agent 1, "shared support that stores only association and liveness"; "Agent 2 does not implement the directory" | **new, no contradiction** — I proposed no directory, so I am not losing one |
| Implementer column, §6/§7 | n/a | role-based ("producer owner", "each consumer") | **none** — see §6.4 |

**No assignment in §§6–8 takes anything away from me that my submission claimed.** The
`C05-7.1`-versus-`C05-2.1` contradiction Agent 3 found is genuinely gone: `C05-7.3` now says
explicitly "*Agent 1 does not implement the `TN-P` obligations on Agent 2's enemy producers*", which is
the sentence my §8 needed in order not to be contradicted.

### 6.2 Verification that the offending sentence is actually gone

`DV-4` claims "the withdrawn claim appears only inside the correction ledger, never in a normative
clause — **PASS — 1 occurrence, inside the §3.2 correction ledger**". I checked:

```
$ grep -n "in every candidate"  → 1 hit, line 123, inside §3.1's quotation marks
```

**DV-4 is accurate.** The withdrawn sentence appears **once**, at line 123, in §3.1, inside quotation
marks as the problem statement — not in `C05-7.1` and not in any normative clause. Verified, not
assumed. (My first check was wrong: I searched for `grep -c "is Agent 1's in every candidate"`, which
returns 0 because the source contracts "is Agent 1's" to `"is Agent 1's in every candidate"` across a
line break that my pattern did not span. The single hit is the correct result and DV-4 stands.)

### 6.3 The MEAD-C-under-MEAD-A precision is correct and I confirm it independently

`C05-7.2` row 3 says the contract layer's owner is "Agent 3 under MEAD-C; **unassigned under MEAD-A**;
absent under MEAD-B". I verified all three in my prior review: MEAD-C has a `TDDCore` module (lines
227/228/267); MEAD-A has **no** `TDDCore` module (its §4.2 tree is `TDDRuntime/{Core, Character,
Combat, AI, World, Progression, Narrative, Audio, UI, Framework}`) and assigns no cross-agent
contract owner; MEAD-B has zero occurrences of `TDDCore`.

**S2 got this right, and it got it right in a way my own earlier review did not credit A1 for** — I
recorded in `586152b` §2.1 that A1's previous clause was MEAD-C-specific in its ownership. **S2 fixes
that.** `C05-2.2`'s header comment and §11 both now name the three cases explicitly. This is the
correction working as intended and I credit it.

### 6.4 Condition 9 — the two vocabularies should be reconciled

`C05-7.2` names **agents** ("Agent 2 on its enemy producers"). §6/§7/§8's implementer columns name
**roles** ("producer owner", "each consumer", "Agent 1, shared support"). Both are correct and the
role-based version is more durable, but a reader cannot mechanically check that row 2 of `C05-7.2` and
14 rows of §6 agree, because they use different words. `DV-3` checks only that the column is *filled*,
not that it agrees with `C05-7.2`.

**Condition 9:** add a document check that maps each implementer-cell role to the agent `C05-7.2`
assigns it, and assert agreement. This is exactly the kind of check `DV-1`–`DV-10` already do well, and
its absence is the one place the document's own verification is weaker than its ambitions.

### 6.5 One attribution in §3.2 that is right and I want to confirm

`C05-7.2` row 1 cites "TD v1.2 C-05; `A2-C05` §8; `A1-R1` §5.1" as basis. I checked TD v1.2's C-05
row as quoted: Agent 1 "Propose parry/block **consumer** timing and invalidation expectations"; Agent 2
"Propose actual **enemy telegraph producer** lifecycle, IDs, clock and cancellation." **The quotation
is exact** and it supports row 1 and row 2 exactly as S2 says. No cherry-picking.

### 6.6 Q5 conclusion

**AGREE WITH CONDITIONS.** There is **no conflict** between §§6–8's assignments and my `A2-C05` §8. The
assignment split is correct, it restores consistency with my submission, and the MEAD-neutrality
handling is better than what it replaced. The single condition is vocabulary reconciliation so the
agreement is mechanically checkable.

---

## 7. Document-check claims: I re-ran the verifiable ones

S2 §13.3 claims ten document checks pass (DV-1…DV-10). I verified the arithmetic-checkable ones
independently, because a document asserting its own correctness is not evidence.

| Check | S2 claims | My independent result | Verdict |
|---|---|---|---|
| **DV-1** 30 obligations, no duplicates, all in §12.3 | PASS | **28 rows in §§6–8** (14 P + 9 C + 5 R = 28; **2 `TN-A`** rows make 30 total in §8). Distinct, no duplicates. §12.3 lists all 30. **PASS**, though S2's own prose in §8 says "`TN-R-01` … `TN-R-04` are S1's; `TN-R-05` is new. `TN-A-01`/`TN-A-02` are unchanged" — the 30 = 14+9+5+2 is correct | **PASS, confirmed** |
| **DV-2** `T-C05-01`…`50`, none missing or extra | PASS | **50 distinct, none missing, none extra** | **PASS, confirmed** |
| **DV-6** 11 suite rows, case column sums to 50 | PASS | **11 rows, sum = 50** (my first parse said 42 because suites **J** and **K** carry bold numerals `**4**` that a naive parser skips — the document is right and my parser was wrong) | **PASS, confirmed** |
| **DV-4** withdrawn sentence gone | PASS | **confirmed** — exactly one occurrence, line 123, in §3.1's quotation; absent from `C05-7.1` and every normative clause | **PASS, confirmed** |
| **DV-8** "10 occurrences of 'execut'" | PASS | **16 total**; **12** of `executed`, 2 of `executing`, 2 of `execution`. The *substance* of DV-8 holds — every occurrence is about document checks or negated, and "0 executed" is present — but **the stated count of 10 is wrong** | **PASS in substance, count inaccurate** |
| DV-3, DV-5, DV-7, DV-9, DV-10 | PASS | not independently re-run; DV-5 and DV-9 are the two I would most want re-run, since DV-9 ("no unqualified `TDDCore`") is the MEAD-neutrality guard | **not verified by me** |

**Two provenance weaknesses in the reviewed blob, both already remediated, no action requested.**

1. **§16 lines 599–600 carry unfilled `PUB_COMMIT` / `PUB_BLOB` placeholders.** Real, and fixed by the
   later correction, which fills both with the values I verified at §0.1.
2. **§0 line 18 cites MEAD-B as the bare short SHA `d32660f`.** This is *valid* — `d32660f` is
   `docs: reconcile cross-agent contracts v2` on Agent 3's branch, and
   `d32660f:docs/MASTER_ENGINEERING_ARCHITECTURE.md` = `1e8d1bd1b223c364c02464f6036e3f9ee9a9b0a7`,
   the same blob the correction cites at `1eb613f`. **My first check reported it as
   "not a valid object", and that was my error, not the document's:** the commit was simply not in my
   clone until I fetched `origin/a3branch` later in the same session. A short SHA that does not
   resolve locally is not evidence of a bad citation. I record this because it is the *second* time in
   this review series I have converted a local-clone artefact into a claim about a document (§0.3 of
   `586152b` was the first, in the other direction), and the countermeasure — check whether the ref is
   reachable before calling it wrong — belongs on the record.

   The correction's improvement is therefore **path/blob precision**, not the repair of a broken
   reference: `d32660f` was correct, and `1eb613f` / blob `1e8d1bd1…` is the same content stated more
   verifiably.

---

## 8. Answers to §17.2, restated as one table

| Q | Verdict | Blocking finding | Narrowly necessary correction |
|---|---|---|---|
| **1** | AGREE WITH CONDITIONS | Directory is a reversal of my §7.1 position that only S2's narrow scoping makes acceptable | (1) state why the directory is not the director I objected to; (2) `DN-1` deregistration triggers to match `RM-1`; (3) define "one transition" under collapsed section boundaries |
| **2** | **DISAGREE** | **`INV-1` includes `RemainingLocalSeconds`, an aging field** → every conforming producer violates it every frame, and equal-revision discard loses a change | (4a) exclude the aging field from the identity and state its formula, or store `R0`; (4b) fix `TN-R-05` and `T-C05-46` to match; (4c) rewrite `EX-5` and state publication order for a same-frame phase+retime |
| **3** | AGREE WITH CONDITIONS | `Resynchronised` undeclared; `WindowKey`/`AttackTag` absent, so a resync into `Active` cannot say "unblockable" | (5) declare `Resynchronised` or demote it to self-check; (6) carry `WindowKey`+`AttackTag` or state their absence and the resolution path |
| **4** | **DISAGREE** | `C05-7.2` row 5 assigns me three consumers that need identity C-05 does not carry, and one that needs placement C-05 deliberately excludes | (7) scope VFX to timing/phase, placement outside; (8) carry `WindowKey` or describe montage selection as a trigger |
| **5** | AGREE WITH CONDITIONS | No conflict with my submission; assignments correct and MEAD handling improved | (9) reconcile agent-vocabulary (`C05-7.2`) with role-vocabulary (§6–8 columns) with a check |

**Total: 9 narrowly necessary corrections, 0 architectural changes, 0 reopened findings.** None of the
nine requires a TD decision, a MEAD selection, a history mechanism, an event bus, or a redesign of X-1.

---

## 9. What I did and did not do

| Restriction | Compliance |
|---|---|
| Review only; do not edit Agent 1's documents | **Complied** — `AGENT1_C05_CONTRACT_SUCCESSOR_V2.md` at `bf6c8fb` unmodified; all five A1 submission blobs verified unchanged |
| No C++ implementation | **Complied** — none written |
| No contract freeze or signatures | **Complied** — no signature given, none implied; §1 states a review is not a contract version |
| No canonical MEAD selection | **Complied** — I authored MEAD-A and disclose it; §6.3 records S2's MEAD neutrality as correct without choosing |
| Do not resolve TD-owned decisions | **Complied** — TD-06/TD-09/TD-12/TD-13/U-14/U-15 untouched |
| Do not claim C-05 or U-07 is closed | **Complied** — both stated open in §0 and §9 |
| Do not claim tests were executed unless they actually were | **Complied** — §7 reports only document checks I actually ran; **zero contract tests executed** |
| Do not reopen the recovery architecture, add history/bus, select a MEAD, redesign X-1 | **Complied** — §3.5's fixes are one amended invariant and one example rewrite |
| Preserve all earlier reviews | **Complied** — `4c09980`, `7ea0a85`, `586152b` unmodified; this is a new file |
| Do not substitute a review of a different branch tip | **Complied** — reviewed `bf6c8fb` at `e5ddad69`; §0.2 proves the tip diff is provenance-only |

**Tests executed by me on contract behaviour: 0.** No C++, no engine, no compiler, no project exists in
this workspace (ADR-0012). Every acceptance case in S2 (`T-C05-01`…`50`) is `PROPOSED / NOT RUN` and I
ran none of them. The only executed evidence in this review is document and arithmetic verification,
enumerated in §7 and §3.2.

---

## 10. One thing I want on the record

Both corrections are correct. Agent 3 found two real defects; S2 fixes both, and the fix to the
revision model is **better than what was asked for** — making every message carry the complete
snapshot (§2.4) is the same insight generalised one path over, and it closes a hole Agent 3's wording
left open. The rename from `TimingRevision` to `StateRevision` is right for the reason given.

My two DISAGREE verdicts are not about the corrections. They are about **three fields and one
invariant sentence**:
- `RemainingLocalSeconds` was included in an equality invariant (Q2) — the invariant is what I
  disagree with, not the revision model;
- `WindowKey` and `AttackTag` are absent from a snapshot whose consumers were assigned by name (Q3/Q4)
  — the assignment is what over-promises, not the contract.

All four are narrow. I would expect a successor that fixes them to move to AGREE on all five questions
without reopening anything, and I say that now so the record shows what would change my verdict rather
than only what my verdict is.
