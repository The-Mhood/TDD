# AGENT 2 — REQUIRED REASSESSMENT OF `A1-C05-S4.1` v4.1

**Review ID:** `TDD-A2-REVIEW-A1C05-S4-1-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — no signature, no freeze, no merge, no implementation, no MEAD
selection, no TD decision, no M0 authorisation. **C-05 and U-07 remain open.**
**Outcome:** **`TARGETED REVISION`** (§9).

This is an independent reassessment. It **corrects my own previous provenance statement** (§1),
which is now known to be wrong at its date of publication, and it does **not** carry forward
findings that S4.1 has fixed.

---

## 1. Correction to my previous provenance statement

### 1.1 What I published, and what is true

In `TDD-A2-REVIEW-A1C05-S4-001` §0.1 I wrote:

> *"The instruction names `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md` … **No file by that name
> exists on any remote branch**, and no commit message mentions a 4.1"*

**That statement is false, and I withdraw it.** The file exists, at the exact commit and blob named
in this instruction:

```
$ git rev-parse 95918268ed5b20b878fef3ee0a7855ad18e6eeb6:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md
d54e194affeaee98b1030e2b83b4c34e234fa382
```

Matches the requested blob exactly. **I was wrong, and the correction is not a matter of
interpretation.**

### 1.2 How the error arose — established from commit metadata, not guesswork

I reconstructed the timeline from commit timestamps rather than from memory or local file mtimes:

| Time (UTC, 2026-11-17) | Commit | Event |
|---|---|---|
| 13:48:21 | `a345354` | S4.0 tip recorded — the branch head I observed |
| **14:09:47** | `9591826` | **S4.1 first commit** |
| 14:09:50 | `04a9e2f` | S4.1 provenance fill |
| 14:10:35 | `3784949` | S4.1 tip |
| **14:15:02** | `d60981b` | **my review committed** |

And S4.1 descends from the S4.0 tip I reviewed:

```
$ git merge-base --is-ancestor a3453548 95918268 && echo YES
YES: S4.1 descends from S4.0 tip a345354
```

**What this establishes:**

1. When I ran `git ls-remote`, the branch head I saw was `a3453548`. My *observation* was accurate
   at the moment I made it.
2. **My review was committed 4 minutes 35 seconds after S4.1's tip was pushed.** The remote had
   changed between my inspection and my publication.
3. I did not re-run `git ls-remote` before committing a sentence asserting a **repository-wide
   negative in the present tense**.

**So the precise defect in my work is this: a stale-remote observation was promoted into a
publication-time claim.** Not fabrication — I reported what I saw, and I reported it accurately. Not
substitution — I reviewed the newest successor that existed when I looked, and said explicitly that
a later v4.1 would not be covered. But `"no file by that name exists on any remote branch"` is a
claim about the state of the repository *at the reader's moment of reading*, and I checked it once,
early, and never again.

### 1.3 The process lesson, stated so it binds future reviews

**A negative existence claim must be re-verified immediately before publication, not only at
inspection time.** For any review I publish that asserts "does not exist", "no branch contains",
"absent from all heads", the check must be run as the **last** action before `git commit`, and the
command's timestamp must belong to the same minute as the commit.

This is the **third** citation-class error in this engagement — the `d32660f` retraction (W-M2.10),
the `80060de6` hash transcription (W-M2.12), and now this. All three share one cause: **a fact
captured once and carried forward without re-derivation at the point of use.** The hash case is now
test-enforced. This case will be too (§8.2).

### 1.4 What part of my previous review survives

My S4.0 review remains a valid review **of S4.0**. Its findings were derived from blob `424d2c69`,
and I have re-verified against S4.1 that every one of them still applies (§5). What does not survive
is the **framing** — the claim that no S4.1 existed, and with it any implication that Agent 1 had
not responded. S4.1 is a real, published, narrow correction, and this document assesses it.

---

## 2. Verification that the reviewed content is S4.1

| Field | Value |
|---|---|
| **Reviewed blob** | **`d54e194affeaee98b1030e2b83b4c34e234fa382`** |
| **Publishing commit** | **`95918268ed5b20b878fef3ee0a7855ad18e6eeb6`** |
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md` |
| Version | `A1-C05-S4.1` v4.1 — `TDD-A1-C05-SUCCESSOR-004.1` |
| Lines | 1,185 |
| Branch | `arena/3bc206a0-tdd` |
| **Branch tip** | `3784949595d2d62944f712e7345be69118aa14d9` → blob `cc056a4854…` |
| **Immediate predecessor** | `A1-C05-S4` v4.0, blob `424d2c69…` at `4692e973` — **preserved, verified** |

### 2.1 It is genuinely S4.1, not S4.0 renamed

```
$ git diff 424d2c69 d54e194a
header:  A1-C05-S4 v4.0          -> A1-C05-S4.1 v4.1
ID:      SUCCESSOR-004           -> SUCCESSOR-004.1
+ §0.5 "S4.1 — the single correction, stated exactly"  (new section)
§1 row 6:  "7 declared, 6 observed" -> "7 declared, 5 observed"  [CORRECTED at S4.1 ...]
§17, §18: provenance + handoff retargeted to this file
```

Every one of those is a version, provenance or count line. **No normative clause changes.**

### 2.2 The reviewed blob is not the branch tip, and the difference is immaterial

```
$ git diff d54e194a cc056a48   ->  5 insertions, 5 deletions
  §0.5 verification row reworded (the "scan stated so it cannot drift" sentence)
  §17 Publishing commit / Blob: S41_COMMIT/S41_BLOB -> 9591826… / d54e194a…
  §18.1 and §18.2 handoff blob references filled
```

The two later commits are `04a9e2f` (provenance fill) and `3784949` (§0.5 wording). **Neither
touches a normative clause, an obligation row, a test, or a count.** I reviewed the blob named in
the instruction, as instructed, and verified by diff that no finding here changes at the tip.

### 2.3 §0.5's "what did not change" claim — verified, not accepted

S4.1 asserts that nothing but one cell changed. **I checked that claim against S4.0 rather than
taking it, because it is exactly the kind of claim that hides a second edit.**

| Object | Identical to S4.0? |
|---|---|
| `TN-P-18`, `TN-P-19` | **yes** |
| `TN-C-11`, `TN-C-14`, `TN-C-15` | **yes** |
| `TN-A-02`, `TN-A-03` | **yes** |
| Whole §7 Producer obligations | **yes** |
| Whole §8 Consumer obligations | **yes** |
| Whole §9 Shared read-surface and arbitration | **yes** |
| §4.9 `C05-2.9` (contains `PO-5`) | **yes** |
| §5.4 `C05-7.4` (token table) | **yes** |
| §9.2 `C05-6.4` (arbitration boundary) | **yes** |

**§0.5's claim is accurate.** S4.1 is a genuinely targeted, single-cell correction, and the
documentation of it is honest — including its own admission of *how* the error arose
(*"§1's cell was written from a draft estimate made before the checker was first run … this one cell
was missed"*). That is the correct form of disclosure and I record it as such.

---

## 3. D-6a — `DV-11` count · **RESOLVED**

**S4.1 §1 row 6; §0.5; §13.1 `DV-11`; §5.4.**

### 3.1 The correction is present and correct

S4.1 §1 row 6 now reads:

> *"…reports declared vs observed tokens separately **(7 declared, 5 observed)** `[CORRECTED at
> S4.1: the summary cell said 6; the instrument says 5 …]`"*

### 3.2 Verified against the token table and the instrument, not against the summary

I re-derived the count from the S4.1 text by parsing the 7th cell of all 43 obligation rows:

| Token | Cells | Family breakdown |
|---|---|---|
| `producer owner` | 23 | 19 `TN-P` + 4 `TN-R` |
| `each consumer` | 12 | 12 `TN-C` |
| `Agent 2, C-05 consumer` | 3 | 3 `TN-C` |
| `Agent 1, subject to TD-09` | 3 | 3 `TN-A` |
| `Agent 1, shared support` | 2 | 2 `TN-R` |

**7 declared in §5.4, 5 observed across 43 cells, 2 declared-but-unused by design.** This matches
§13.1's `DV-11` output exactly.

I also re-implemented `DV-11`'s stated rule — token declared in §5.4; token's row ∩ allowed-row set
for the obligation's prefix (`TN-P`→{2}, `TN-C`→{5,6}, `TN-R`→{2,4}, `TN-A`→{8}); row owner matches —
and ran it over all 43 cells:

```
declared=7 observed=5 cells=43 failures=0
```

**Clean, independently of S4.1's own claim.**

### 3.3 §0.5's own scan claim — verified

§0.5 claims *"a text scan for every declared/observed claim in the document finds **5** in every case
that describes S4/S4.1, and 6 only inside the verbatim quotation."* I scanned for every
`N declared … M observed` pattern and classified each occurrence by context:

| Occurrence | Scope | Correct? |
|---|---|---|
| `7 declared, 5 observed` ×8 | S4/S4.1 statements | ✔ |
| `7 declared / 5 observed` ×several | `DV-11` output, §2, §5.4, §18.1 | ✔ |
| `7 declared, 6 observed` ×2 | **inside §0.5's own description of the defect it fixes** | ✔ correctly quoted, not asserted |
| `6 declared / 5 observed` | S3 tamper proof (`dv4.py` output on `a6b4e22`) | ✔ correctly S3-scoped |
| `6 declared against 5 observed` | §13.2 narrative about S3 | ✔ correctly S3-scoped |

**Zero non-S3, non-historical statements report an observed count other than 5.** The scan claim is
true.

### 3.4 Disposition: **D-6a RESOLVED. The obsolete S4.0 finding is withdrawn.**

I explicitly **do not carry forward** the "6 observed" finding. It is fixed, the fix is verified by
two independent methods, and S4.1 documents its own root cause honestly.

### 3.5 Condition D-6a-i — the root cause is acknowledged and deliberately left in place

§0.5 states:

> *"**Instrument added:** none. A permanent check that every declared/observed sentence equals the
> checker's output would be a new validation instrument (DV-24) and would change §13's count of 23 —
> outside a targeted documentation correction."*

**That reasoning is defensible for a targeted correction, and I accept it as sufficient *for
S4.1*.** But the reasoning also names the mechanism by which this keeps recurring: the figure is
hand-restated in prose and only one instrument computes it. This is now the **third** revision
(S2 DV-8: 10 vs 16; S3 DV-11: 6 vs 5; S4.0 §1: 6 vs 5) where a hand-copied count diverged from the
instrument beside it.

**Condition (non-blocking, for any future substantive revision):** when S4.1's next substantive
successor opens §13 for any other reason, add `DV-24` — *every declared/observed sentence equals
`DV-11`'s computed output* — so the class closes rather than the instance. **This is advisory and
must not gate S4.1.** I record it because the recurrence pattern is itself evidence, not because
S4.1 owes it.

---

## 4. D-4 — audio ownership · **DISAGREE — NOT RESOLVED**

**§8 preamble (line 566); §5.2 row 5 (line 459); §6.1 audio row; `TN-C-15` (line 584); `DV-22` (line 981).**

### 4.1 The defect is present in S4.1, unchanged from S4.0

**§8's preamble still assigns audio to Agent 1.** Verbatim, S4.1 line 566:

> *"**Each obligation is implemented by each consuming agent in its own code** — Agent 1 for defence,
> dodge, camera **and audio**; Agent 2 for AI reaction, audio cue, montage trigger and VFX timing."*

### 4.2 Compared against the three clauses that contradict it

| Location | Says | Assignment |
|---|---|---|
| **§8 preamble** (566) | "Agent 1 for defence, dodge, camera **and audio**" | **Agent 1** |
| **§5.2 row 5** (459) | "camera response and framing … **Agent 1 owns no audio responsibility in C-05**" | **Agent 1: none** |
| **§6.1 audio row** (484) | "**Audio cue** (**Agent 2** — the only owner, `C05-7.2` row 6; `TN-C-15`)" | **Agent 2** |
| **`TN-C-15`** (584) | "a C-05 consumer responsibility of **Agent 2 alone**" | **Agent 2** |

Three clauses assign audio to Agent 2 or to no one. **One clause, 107 lines above `TN-C-15` in the
same section, assigns it to Agent 1.**

### 4.3 Is it contractually material? — **Yes, and precisely why**

I want to be exact about this, because "an inconsistency" is not by itself a defect.

- **It is not a normative clause.** `TN-C-15` is normative and says Agent 2 alone. The obligation
  table is correct.
- **It *is* the implementation instruction for §8.** The preamble's function is to tell a reader who
  implements §8's fifteen obligations. It is the first sentence of the section and the only sentence
  in the document that summarises implementer assignment for consumers.
- **It is materially wrong in a way an implementer would act on.** A reader who follows the preamble
  builds an Agent 1 cue path — the exact duplicate ownership `TN-C-15`'s *"Agent 2 alone"* forbids.
  `DV-22`'s own intent (*"audio has exactly one owner"*) is violated by the document that contains
  it.

**Material, but narrow**: one phrase, no normative text, no obligation, no test. It does not require
reopening any requirement. It is a documentation defect with an implementation consequence.

**Classification (§8 of this review): a defect in explanatory/implementation framing, not in a
normative clause.** `TN-C-15` remains correct and I do not ask for it to change.

### 4.4 Does `DV-22` detect this class? — **No, and S4.1 already predicted that**

`DV-22`'s stated method, verbatim:

> *"row 5 contains no audio claim and says Agent 1 owns none; row 6 owns audio cue selection;
> `TN-C-15` exists and its implementer is `Agent 2, C-05 consumer`"* → **PASS**

**It checks three objects: §5.2 row 5, §5.2 row 6, and `TN-C-15`.** §8's preamble is none of the
three. So `DV-22` reports `PASS` on a document that still contains the defect it exists to prevent.

**This is not a new observation — S4.0 named the exact risk itself.** §14.2's D-4 row says:

> *"**Uncertainty** … that no other row or clause still implies Agent 1 owns a cue |
> **If another assignment survives, `DV-22` was scoped too narrowly.**"*

**Another assignment survives. `DV-22` was scoped too narrowly.** S4 anticipated this failure mode in
its own risk column and then did not widen the check. That is the most useful thing I can say about
it: the gap is not a surprise to the document, it is an accepted-in-advance risk that materialised.

**This is the same structural failure as S3's `DV-11`** — an instrument scoped to the clauses the
author was thinking about, reporting PASS over a document that violates its own stated purpose.
S4 fixed that instance of the pattern in `DV-11` and left the pattern itself in `DV-22`.

### 4.5 Exact correction required

**Two changes, both minimal.**

**(i) §8 preamble, line 566 — delete two words.** Replace:

> `— Agent 1 for defence, dodge, camera and audio; Agent 2 for AI reaction, audio cue, montage
> trigger and VFX timing.`

with:

> `— Agent 1 for defence, dodge and camera; Agent 2 for AI reaction, audio cue, montage trigger and
> VFX timing.`

**(ii) `DV-22` — widen the scan so the class cannot recur.** Add to its method: *"and a
whole-document scan finds no clause outside a quoted correction that assigns audio to any agent
other than Agent 2."* A grep for `Agent 1` within ±120 characters of `audio`, excluding the three
historical/quotation sites (§5.2 row 5's correction note, §14.2 D-4's finding text, §15.3) would
have caught this and would pass on the corrected text.

**Both are required.** (i) alone fixes this instance and leaves the instrument blind; (ii) alone
would make the check fail without fixing the text. **Closure condition: both, and re-issue the blob
since the text changes.**

---

## 5. Reassessment of D-1 … D-7 against S4.1

Because S4.1 changed no normative clause, my S4.0 verdicts **carry over unchanged in substance** —
and I re-verified rather than assumed that, by checking the clause bodies listed in §2.3 above.

| # | Finding | S4.1 verdict | Genuinely resolved? | Notes |
|---|---|---|---|---|
| **D-1** | Lost retime / stale rate | **AGREE WITH CONDITIONS** | **Yes** | `TN-C-14` bound + stated residual unchanged. Conditions D-1a (upper-bound wording), D-1b (classification) **remain open** — see §6.1 |
| **D-2** | Ordering / per-message content | **AGREE** | **Yes** | `PO-5` + `TN-P-18` + `T-C05-51`/`T-C05-65` unchanged. But see **C4c-N1**, §6.2 |
| **D-3** | Identity constancy | **AGREE** | **Yes** | `TN-P-19`, `TN-P-07`, `T-C05-66` unchanged; consistent across all four locations |
| **D-4** | Audio ownership | **DISAGREE** | **No** | §4 above. Unchanged in S4.1 |
| **D-5** | Implementer-token mapping | **AGREE** | **Yes** | New row-6 token, both re-mapped, 0 failures over 43 cells |
| **D-6** | `DV-11` not row-level | **AGREE** | **Yes** | Row-level rule verified by independent re-implementation. Count defect **now also fixed** (§3) |
| **D-7** | `INV-2` precondition | **AGREE** | **Yes** | Precondition in the clause; `TN-C-10` echoes it |

| Condition | S4.1 verdict | Resolved? |
|---|---|---|
| **C4a-1** | AGREE | Yes |
| **C4a-2** | AGREE | Yes — `DV-12` three-home set equality |
| **C4c-1** | AGREE WITH CONDITIONS | Yes, with D-1a/D-1b |
| **C4c-2** | AGREE | Yes — `PO-5` |
| **C6-1** | AGREE | Yes |
| **C6-2** | **DISAGREE** | **No** — same defect as D-4 |
| **C9** | **AGREE** | **Yes** — count corrected in S4.1; row-level check verified |

**Tally over seven defects and seven conditions: 10 AGREE, 3 AGREE WITH CONDITIONS, 1 DISAGREE.**
(Previous S4.0 tally was 8 / 4 / 2. **D-6a moves from DISAGREE-with-conditions to AGREE**, and C9
likewise.)

---

## 6. The remaining findings

### 6.1 D-1a and D-1b — carried forward, unchanged (minor)

**D-1a — upper-bound wording.** `TN-C-14`'s failure column says *"Staleness is then bounded by one
frame, by construction."* True as an **upper** bound; not a same-frame guarantee, because
frame-internal ordering is unspecified and a pull landing before the producer's publication in F
sees the stale revision. **Recommended:** add *"The bound is 'at most one frame', measured from the
publication of the missed revision to the next successful pull; `TN-C-14` does not require the pull
to land after the producer's publication within the same frame."*

**D-1b — undefined classification.** `TN-C-14` splits *"a consumer whose behaviour depends on
remaining time"* from *"a consumer that only reacts to phase transitions"*, and nothing defines which
consumer is which. **Recommended:** make it a property of the **call site** — any call site that
reads `RemainingLocalSeconds` must satisfy `TN-C-14` — which removes the need for a per-agent
taxonomy.

**Both minor, both wording, neither gating.**

### 6.2 C4c-N1 — `PO-5` and §3.6 reason (b) · **CONFIRMED, unresolved in S4.1**

**§3.6 rationale (b), S4.1 line 242, verbatim:**

> *"(b) Within one frame the producer's internal application order is **not observable** at frame
> granularity, so leaving it to the producer would let two conforming producers emit different
> sequences for identical gameplay — the exact non-determinism a contract exists to remove."*

**Which premise is contradicted, precisely.** Not the conclusion, and not `PO-3`. The contradicted
premise is the **first clause of (b)**: *"the producer's internal application order is **not
observable** at frame granularity."*

`PO-5` (S4.1 line 430), verbatim:

> *"**PO-5 (new).** Publication is **interleaved with application**. Each message carries exactly the
> state at its own revision … **A pull taken between two publications of the same frame returns the
> earlier revision's `VF` exactly.**"*

And `T-C05-65` **observes the application order directly**: a pull after the transition returns
Active at the **old** `ProducerRate` under `n+1`; a pull after the dilation returns the **new** rate
under `n+2`.

**The reasoning is straightforward.** If a pull can land between the two publications and returns the
earlier revision exactly, then an observer distinguishes "phase applied, dilation not yet" from
"both applied." That distinction *is* the internal application order. It is observable by
construction — that is the entire purpose of `PO-5`. So (b)'s premise is **false**, and it is false
*because of a rule S4 added*.

**Does `PO-3` remain necessary for (a) and (c)? — Yes, and it must not be discarded.**

- **(a) survives untouched.** *"a retime published first would describe the timing of a phase the
  consumer has not been told about."* This is a content/lifecycle argument about what a message
  *means*. `PO-5` says nothing about it. **Valid.**
- **(c) survives.** It argues the first message of a pair should be the one whose loss is cheaper.
  Loss behaviour is unchanged by `PO-5`. **Valid.**
- **`PO-3` is not made redundant by `PO-5`.** `PO-5` constrains **when** publication happens relative
  to application. `PO-3` constrains **which order** the two changes are applied-and-published in. A
  producer could satisfy `PO-5` perfectly and still apply the dilation **first**, publishing
  `Retimed@n+1` then `PhaseChanged@n+2` — fully `PO-5`-conformant, and `PO-3`-violating. **The two
  rules constrain orthogonal things.**

**Smallest technically correct resolution — one clause of one bullet, nothing discarded.**

Replace only the false premise in (b), keeping its conclusion:

> **(b)** Within one frame the internal application order **is observable through a mid-frame pull
> once `PO-5` is in force**, so leaving the order to the producer would let two conforming producers
> expose different revision sequences for identical gameplay — the exact non-determinism a contract
> exists to remove. `PO-5` therefore requires the application order to follow the publication order
> `PO-3` fixes, not merely to interleave publication with application.

**This preserves `PO-3`, `PO-5`, `TN-P-15`, `TN-P-18`, `T-C05-51` and `T-C05-65` exactly as written,
discards no valid `PO-3` requirement, and removes the contradiction.** It is a one-sentence edit to
an explanatory bullet, not a normative change.

**Classification: a defect in explanatory rationale.** The normative clauses (`PO-3`, `PO-5`,
`TN-P-15`, `TN-P-18`) are consistent with each other; only the justification attached to `PO-3`
states a premise the contract now contradicts. It matters because an implementer reading (b) could
conclude the application order is unconstrained — which `PO-5` forbids.

### 6.3 D-6b — §5.4 "Used by" tallies · **still imprecise (cosmetic)**

Unchanged in S4.1. The two tallies omit rows:

| Token | §5.4 "Used by" | Actual cells |
|---|---|---|
| `producer owner` | "19 `TN-P` rows" | **23** (19 `TN-P` **+ 4 `TN-R`**) |
| `each consumer` | "11 `TN-C` rows` | **12** `TN-C` cells |

The mappings are correct; the tallies under-report. **Recommended:** state full cell counts
(*"23 cells (19 `TN-P`, 4 `TN-R`)"*, *"12 cells"*) or drop the column and let `DV-11` print it.
**Cosmetic, non-gating.** Note this is a *third* hand-restated count diverging from the instrument —
the same class as D-6a.

### 6.4 New defects introduced by S4.1 — **none found**

I scanned S4.1 for regressions across four categories:

| Category | Check | Result |
|---|---|---|
| **Normative clauses** | §7/§8/§9 bodies, `PO-5`, `TN-P-18/19`, `TN-C-11/14/15`, `TN-A-02/03`, `C05-6.4` vs S4.0 | **byte-identical** — no new defect possible |
| **Counts** | 43 obligations (19/15/6/3), 67 cases, 18 suites, 23 DV rows, 43 cells | **all reconcile** |
| **Instruments** | `DV-11` re-implemented → 7/5/43/0 failures; `DV-22` scope unchanged | `DV-11` correct; `DV-22` gap is **pre-existing**, not introduced |
| **Provenance** | §17/§18 targets, predecessor row, `PUB_*` → `S41_*` → filled | **correct at the tip**; the reviewed blob carries `S41_COMMIT`/`S41_BLOB` placeholders, which the later `04a9e2f` fills — **same pattern as S3 and S4.0, correctly disclosed** |

**S4.1 introduced no new defect.** Its one edit is correct, verified, and honestly documented. The
two surviving findings (D-4, C4c-N1) and two carried conditions (D-1a, D-1b) plus one cosmetic
(D-6b) are all **pre-existing in S4.0 and untouched by S4.1**.

---

## 7. Defect classification, as required

Separating the four kinds, because they carry different weight and different closure routes.

| # | Defect | Category | Normative effect | Blocks? |
|---|---|---|---|---|
| **D-4** | §8 preamble assigns audio to Agent 1 | **Implementation framing** (not normative; `TN-C-15` is correct) | Duplicate-ownership instruction to implementers | **Yes** |
| **C4c-N1** | §3.6 (b) premise falsified by `PO-5` | **Explanatory rationale** (normative rules consistent) | Misleads on whether application order is constrained | **Material, not blocking** |
| **D-22-scope** | `DV-22` cannot see §8's preamble | **Validation instrument** | Reports PASS on a document violating its purpose | **Yes** (with D-4) |
| **D-6b** | §5.4 tallies 19 vs 23, 11 vs 12 | **Validation/instrumentation prose** | None on contract; misstates the token table | No (cosmetic) |
| **D-1a** | "bounded by one frame, by construction" | **Explanatory** | Reads as a stronger guarantee than holds | No (minor) |
| **D-1b** | timing-dependent vs message-only undefined | **Normative specification gap** | Classification is unenforceable as written | No (minor) |
| **D-6a** | §1 row 6 "6 observed" | **Validation instrument summary** | **FIXED in S4.1** | Resolved |
| *(mine)* | My "no V4_1 exists" claim | **Provenance** | Misdirected the review target | Corrected §1 |

**No defect in a normative clause remains open.** Every open item is framing, rationale,
instrumentation or count. That is what makes the outcome a targeted revision rather than a redesign.

---

## 8. Reproducible checks

Every conclusion above is reproducible from the repository. **These are document-text and arithmetic
checks, not acceptance tests.**

### 8.1 The checks I ran

| # | Check | Command (abridged) | Result |
|---|---|---|---|
| 1 | Reviewed blob is the named one | `git rev-parse 9591826:docs/…V4_1.md` | `d54e194a…` ✔ |
| 2 | Reviewed blob ≠ tip; diff is placeholder + one §0.5 row | `git diff d54e194a cc056a48` | 5 ins / 5 del ✔ |
| 3 | S4.1 descends from the S4.0 tip I reviewed | `git merge-base --is-ancestor a3453548 9591826` | true ✔ |
| 4 | S4.1 published before my review commit | commit timestamps | 14:10:35 vs 14:15:02 ✔ |
| 5 | §0.5 "nothing else changed" | compare §7/§8/§9/§4.9/§5.4/§9.2 bodies vs S4.0 | all identical ✔ |
| 6 | Token counts | parse 7th cell of 43 rows | 7 declared / 5 observed ✔ |
| 7 | `DV-11` row-level rule | re-implement + run over 43 cells | 0 failures ✔ |
| 8 | §0.5's scan claim | classify every `N declared … M observed` by scope | 0 non-S3 statements ≠ 5 ✔ |
| 9 | §8 preamble still assigns audio to Agent 1 | grep line 566 | **present** ✗ |
| 10 | `DV-22` scope | read its method cell | row 5 / row 6 / `TN-C-15` only ✗ |
| 11 | §3.6 (b) premise | compare against `PO-5` + `T-C05-65` | **contradicted** ✗ |
| 12 | §5.4 tallies | per-token breakdown | 23 vs 19, 12 vs 11 ✗ |
| 13 | Structural totals | parse obligations / cases / suites / DVs | 43 / 67 / 18 / 23 ✔ |
| 14 | No acceptance-test claim | scan for pass claims | `0 executed`, all `PROPOSED / NOT RUN` ✔ |
| 15 | **Existence re-check as the last action before publication** (rule §1.3) | `git ls-remote origin` | **run at `2026-11-17T18:17:29Z`** — `arena/3bc206a0-tdd` still `378494959…`; reviewed blob still resolves to `d54e194a…` ✔ |

### 8.2 Tests added by this reassessment

A test module `Tools/world/tests/test_review_a1c05_s4_1.py` locks this reassessment, including:

- **Provenance regression:** the reviewed blob resolves from the named commit via `git rev-parse`,
  and the tip blob differs only by placeholder fill — so a mis-transcribed hash fails a test.
- **Existence-claim regression:** a test asserting this review does **not** claim V4_1 is absent, so
  the withdrawn §0.1 statement cannot be reintroduced.
- **D-4:** asserts §8's preamble currently assigns audio to Agent 1 (fails when fixed → re-issue),
  and that `DV-22`'s method does not mention a whole-document scan.
- **C4c-N1:** asserts (b)'s "not observable" premise and `PO-5`'s "pull between two publications"
  both survive — i.e. the contradiction still stands.
- **D-6a closure:** asserts every non-S3 statement of the count is 5, and that "6 observed" appears
  only inside §0.5's description of the fixed defect.
- **`DV-11`:** independent re-implementation over 43 cells, 0 failures.

**Tamper proofs:** each finding's test was run against a mutated copy of the S4.1 text in which the
defect is fixed; each correctly failed, confirming the tests bind the findings rather than passing
vacuously.

---

## 9. Outcome

# `TARGETED REVISION`

**What changed since my S4.0 review:**

| | S4.0 | S4.1 |
|---|---|---|
| **D-6a** (`DV-11` count) | DISAGREE with conditions | **RESOLVED — verified twice independently** |
| **C9** | AGREE WITH CONDITIONS | **AGREE** |
| **D-4 / C6-2** (audio) | DISAGREE | **DISAGREE — unchanged** |
| **C4c-N1** | not reported | **CONFIRMED — unchanged** |
| Tally | 8 / 3 / 2 | **10 / 3 / 1** |

**Why not `PASS`.** Two things remain, and one is material to an implementer:

1. **D-4 — §8's preamble still assigns audio to Agent 1**, 107 lines above `TN-C-15`'s *"Agent 2
   alone"*, and `DV-22` reports `PASS` on it. S4.0 predicted this exact failure in its own risk
   column. **Two-word deletion plus a widened check.**
2. **C4c-N1 — §3.6 (b) states a premise `PO-5` falsifies.** `PO-3` remains correct and necessary;
   only its stated justification is stale. **One sentence.**

Plus **D-1a, D-1b** (wording) and **D-6b** (cosmetic tally).

**Why not `BLOCKED BY DEPENDENCY`.** None of the four open items requires a TD decision. B-11 (C-04),
B-12 (resync routing), B-13 (tag registry) and B-15 (Agent 3's wording) are correctly recorded in
S4.1 and none gates any of them. The blockers are real; they do not gate this verdict.

**What would move me to `PASS`:** D-4's two-word deletion and widened `DV-22`; C4c-N1's one-sentence
rewrite; D-1a/D-1b/D-6b wording. **All six are closable inside existing clauses, none reopens a
settled requirement, and no new normative content is needed.** I would then review the next blob on
its own terms — a fresh review, not a carry-forward of this one.

**On my own error, restated so it is not buried:** my previous review's central provenance claim was
false when published, because I checked the remote once early and asserted a repository-wide negative
four and a half minutes after the repository had changed. **I withdraw that claim.** The finding
set was unaffected — S4.1 changed no normative clause — but a review that misdirects the reader away
from the correct object has failed at the first thing a review must get right. The binding process
change is §1.3: **re-verify any negative existence claim as the last action before publication.**

---

## 10. What I did and did not do

**Did:** fetched `3784949`; verified blob `d54e194a` resolves from commit `9591826`; diffed the
reviewed blob against both S4.0 and the tip; verified S4.1 descends from the S4.0 tip I reviewed;
established the publication timeline from commit metadata; verified §0.5's "nothing else changed"
against six section bodies; re-derived the token counts and re-implemented `DV-11`; verified §0.5's
own scan claim by classifying every count statement; re-checked D-4, C4c-N1 and `DV-22`'s scope;
checked for new S4.1 defects across four categories; classified every remaining defect by type.

**Did not:** sign, freeze, implement, merge, select a MEAD, authorise M0, or close C-05/U-07; review a
branch tip or S4.0 **as a substitute** for the named S4.1 blob; carry forward the obsolete "6
observed" finding; accept §0.5's self-description without checking it; claim any of the 67
acceptance cases ran; or defend my earlier review — **I withdrew its central provenance claim.**

**Still not signing v4.1.**

---

*End of reassessment. `TDD-A2-REVIEW-A1C05-S4-1-001` v1.0.*
