# ADDENDUM A1 TO `TDD-A2-REVIEW-A1C05-S4-1-001`

**Addendum ID:** `TDD-A2-REASSESS-A1C05-S4-1-ADDENDUM-A1` · **Version:** 1.0
**Amends:** `Docs/AGENT2_REASSESSMENT_A1C05_S4_1_V1.md` (W-M2.13, commit `eee9401`)
**Status:** `DESIGN_REVIEW_ONLY` — no signature, no freeze, no merge, no implementation, no MEAD
selection, no M0 authorisation. **C-05 and U-07 remain open.**
**Scope:** closure taxonomy, and two corrections arising from it. Nothing else.

---

## 0. What this addendum is, and what it is not

The subject review is accepted as useful evidence, but it is not yet a clean final review record
because three of its statements do not agree with each other. This addendum fixes them.

**Explicitly out of scope, and unchanged by this document:**

| Item | Status here |
|---|---|
| **D-4** (§8 preamble assigns audio to Agent 1) | **Finding unchanged.** Verdict, evidence, fix and blocking status all stand exactly as written |
| **C4c-N1** (§3.6 reason (b) falsified by `PO-5`) | **Finding unchanged.** §6.2 stands |
| **D-6a** (`DV-11` count) | **Remains RESOLVED.** §3 stands; nothing here reopens it |
| **The reviewed blob** | Unchanged — `d54e194affeaee98b1030e2b83b4c34e234fa382` |
| **S4.1 as a document** | Not reopened or re-reviewed |
| **W-M2.13** | Preserved unmodified at `eee9401`; this addendum is a separate artifact |
| **Architecture** | No new architecture review is undertaken |

**One in-scope technical correction** is required, at §2 below: the review's **D-1a was itself
understated**, and correcting the closure taxonomy forced that into view. I would rather record it
than leave a mild misstatement standing in a document I am otherwise tidying. It **reduces** no
finding and **adds** no new architecture; it corrects my own severity assessment of a defect S4.1
already contains. Per the instruction not to reopen the S4.1 assessment, I state it as a
**correction to my own review**, not as a fresh finding against S4.1.

---

## 1. Closure taxonomy — the defect this addendum exists to repair

### 1.1 The inconsistency, stated exactly

The review used three different closure vocabularies in three places, and they contradict:

| Location | Says | Implies |
|---|---|---|
| §6.1, closing line | *"Both minor, both wording, **neither gating**."* | D-1a, D-1b may remain open |
| §6.3, closing line | *"**Cosmetic, non-gating.**"* | D-6b may remain open |
| §7, `Blocks?` column | D-1a *"No (minor)"*, D-1b *"No (minor)"*, D-6b *"No (cosmetic)"* | none blocks |
| §9 | *"**What would move me to `PASS`:** D-4's … widened `DV-22`; C4c-N1's one-sentence rewrite; **D-1a/D-1b/D-6b wording**."* | all three are required |

**Both cannot be true.** Either D-1a/D-1b/D-6b are PASS conditions, in which case §6 and §7 are
wrong; or they are advisory, in which case §9 is wrong. **§9 is the one that is wrong** — see §1.3.

### 1.2 Why this is not a pedantic distinction

A reader of the review has to answer one operational question: *may Agent 1's next revision close
without touching D-1a/D-1b/D-6b?* Under §6.1/§6.3/§7 the answer is **yes**. Under §9 the answer is
**no**. Those lead to different work. A review whose closure criteria depend on which section you
read last is not a closure criterion.

### 1.3 The taxonomy, now used throughout

Four closure classes, mutually exclusive, defined by **who may accept the residual**:

| Class | Meaning | May close with this open? |
|---|---|---|
| **`PASS-BLOCKING`** | Wrong contract text that an implementer would act on, or an instrument that reports `PASS` over it | **No** |
| **`PASS-CONDITION`** | Correct contract text whose stated justification, guarantee or classification is false or unenforceable — misleads without mis-assigning work | **No** — but only a wording edit |
| **`ADVISORY`** | Imprecision with no implementation consequence; a reader would not do anything differently | **Yes** — recorded, tracked, not required |
| **`RESOLVED`** | Fixed and verified | n/a |

**The rule that decides the boundary:** if two conforming teams could read the document and
legitimately build different things, the item is `PASS-BLOCKING` or `PASS-CONDITION`. If every
reader would build the same thing and only the prose is untidy, it is `ADVISORY`.

### 1.4 The corrected assignment

| Finding | Class | Rationale in one line |
|---|---|---|
| **D-4** — §8 preamble assigns audio to Agent 1 | **`PASS-BLOCKING`** | Two teams build different ownership splits **from the document as written** (§1.5) |
| **D-22-scope** — `DV-22` blind to §8's preamble | **`PASS-BLOCKING`** | An instrument that certifies a document violating its own purpose |
| **D-1a** — `TN-C-14`'s bound does not follow from its requirement | **`PASS-CONDITION`** | The obligation is right; the claimed guarantee **and the reason given for it** are both wrong |
| **C4c-N1** — §3.6 reason (b) falsified by `PO-5` | **`PASS-CONDITION`** | `PO-3` is correct; its stated justification is wrong |
| **D-1b** — `TN-C-14`'s consumer split | **`ADVISORY`** (reclassified — §2.1) | The clause already supplies an operational criterion; both readings coincide |
| **D-6b** — §5.4 tallies (19 vs 23, 11 vs 12) | **`ADVISORY`** | No reader changes what they build from a summary tally |
| **D-6a** — §1 row 6 "6 observed" | **`RESOLVED`** | Verified twice, independently |

**Final PASS criteria: five items** — D-4, D-22-scope, D-1a, C4c-N1 (of which D-4 and D-22-scope are
one atomic change), plus re-issue of the blob.

**Advisory, may remain open: two** — D-1b, D-6b.

### 1.5 Why D-4 is `PASS-BLOCKING` and not a wording nit

I am not splitting a hair here, so the reason needs stating. §8's preamble is the **only sentence in
the document that summarises implementer assignment for consumers**, and it is the first sentence of
the section that contains all fifteen consumer obligations. **Agent 3's independent review of the
same blob reached the same reading** — that a team following §8's introduction assigns audio to both
agents — and reports it as blocking. Independently, from the same text, the same split. That is what
"two conforming teams build different things" looks like in practice, and it is the definition of
`PASS-BLOCKING` used above.

I note this as **corroboration of the observable text**, not as borrowing Agent 3's findings. §5
below records why that boundary is load-bearing.

---

## 2. D-1b reclassified, and a correction to D-1a

Item 2 asked whether D-1b is genuinely normative and, if so, how that squares with non-gating. **On
re-reading the clause rather than my summary of it, D-1b is not normative — I mislabelled it.** The
reclassification below is the fix. Checking it exposed a second, larger problem in my D-1a, which I
record in §2.2.

### 2.1 D-1b — `ADVISORY`, not a normative gap (reclassified)

`TN-C-14`'s operative clause, verbatim:

> *"**A consumer whose behaviour depends on remaining time — it acts on `TN-C-10`'s output —**
> re-pulls every open instance it holds at least once per frame…"*

The em-dash parenthetical **is a definition**, and it is operational: the discriminator is *"acts on
`TN-C-10`'s output"*, and `TN-C-10`'s output is *"remaining local seconds"*, produced by
`R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)`.

**My §6.1 said "nothing defines which consumer is which." That is wrong.** The clause defines it.
What is true is narrower: the definition is stated **inline rather than in a glossary or a named
`DF-` term**, so a reader must read the parenthetical to apply it. That is untidy, not undefined.

**It is not normative for a stronger reason:** the two readings have **identical compliance sets**.

| Reading | Applies `TN-C-14` to | Sanction if disobeyed | Effect on pass/fail |
|---|---|---|---|
| Inline parenthetical | callers that act on aged remaining time | staleness → any diagnostic or timing assertion | identical |
| Agent-level taxonomy (my proposed fix) | every timing-consuming agent | same | identical |

A consumer that does not act on `TN-C-10`'s output has nothing to be stale *about*: its behaviour
does not read the value, so no pull changes it. Both readings therefore require the same pulls and
forbid the same omissions. **A classification that cannot change the verdict is not a normative
gap** — it is documentation debt. Hence **`ADVISORY`**.

**I withdraw my §6.1 recommendation to re-specify it as a call-site property.** It would have
entailed a `DF-` term and a clause edit for a specification that already resolves correctly. The
only genuinely useful residue: state the definition once as a named term so it is findable.

**Reclassification:** `Normative specification gap` → **`Observational/definitional — ADVISORY`**.
This also removes the §7/§9 conflict at its root: D-1b is not a normative defect, so it is not a
PASS condition, so §9 was wrong to include it and §6/§7 were right.

### 2.2 D-1a — my own finding was understated (`PASS-CONDITION`)

Reviewing D-1b took me back to the clause, and there I have to correct myself.

**My §6.1 said the bound "holds as an upper bound; not a same-frame guarantee, because
frame-internal ordering is unspecified."** The second half is true but **irrelevant**, and the first
half is **false**.

**The "not a same-frame guarantee" argument is empty**, though it was not empty when I wrote it.
Given `PO-5`, a consumer that pulls at time *t* in frame *F* either sees frame *F*'s changes or —
if it pulled before the producer published them — sees them at its next pull. Either way adoption is
complete within one frame of its own pulls. **Assuming the bound, it holds.** So that argument
cannot falsify it.

**The real defect is the arithmetic, and it is fatal to the stated reason.** *"At least once per
frame"* constrains a **count**, not an **interval**. A legal schedule under the rule:

| Frame | Permitted pull | Legal? |
|---|---|---|
| 0 | t = 0.99 | yes — one pull |
| 1 | t = 1.99 | yes — one pull |
| 2 | t = 2.99 | yes — one pull |

Every frame has exactly one pull; nothing is skipped; the requirement is satisfied. **The largest gap
between consecutive pulls is 1.98 frames.** Over all placements in `[0,1)` the worst case is just
under **2 frames**, the best case exactly **1**. A retime lost immediately after the frame-0 pull is
therefore not observed until t = 1.99 — **rate-stale for almost two frame durations**, not one.

So:

| Claim | Where | Status |
|---|---|---|
| *"Staleness is then bounded by one frame, **by construction**"* | `TN-C-14` failure column | **False as stated.** The construction does not deliver it |
| *"bounds rate staleness to one frame"* | §1 row 2 | Same |
| *"rate-stale for **at most one frame**"* | `T-C05-64` assertion | Same — the case cannot pass as written |
| *"that one frame is a …"* | §14.2 D-1 row | Same |

**`T-C05-64` is the sharp end.** It asserts the timing-dependent consumer is stale *"for at most one
frame"* while `TN-C-14` permits 1.98. **The test as written cannot pass against the obligation as
written.** That is not cosmetic; it is a contract/test mismatch that would surface on first execution.

**Correction to my own review:** D-1a is **not** *"minor, wording, non-gating"*. It is
**`PASS-CONDITION`**, and the sharpest of the three PASS conditions, because it is the only one whose
defect is arithmetic rather than prose.

**Smallest correct fix — make the bound follow from the rule.** Either:

- **(i) interval-based (preferred).** *"re-pulls every open instance it holds at least once per
  frame **on a schedule whose interval between consecutive successful pulls never exceeds one
  frame**"* — the bound then follows by construction, as the note already claims; **or**
- **(ii) publish-relative.** require a pull after each publication, which is the only placement that
  actually certifies a one-frame age; **or**
- **(iii) weaken the claim.** if 1.98 frames is the intended tolerance, say so, and change
  `T-C05-64`'s assertion to match.

**Any of the three makes §1, `TN-C-14`, `T-C05-64` and §14.2 consistent.** (i) is smallest.
**Condition D-1a-i: whichever is chosen, the four locations must state the same number.** The defect
is not that one of them is wrong, it is that all four assert a bound none of them establishes.

**I flag one thing without adopting a position:** Agent 3's independent review of this same blob
also concludes the one-frame bound does not follow from *"at least once per frame"*, by a
poll-placement argument. **I reached this myself from the clause's arithmetic** (§2.2's count-vs-
interval point) and I state it here because a defect that two reviewers derive separately is worth
recording as such — not because Agent 3's review is being folded into mine. §5 governs that.

---

## 3. The reconciled statements

### 3.1 §7's summary sentence — corrected

**Original (review §7):**

> *"**No defect in a normative clause remains open.** Every open item is framing, rationale,
> instrumentation or count."*

**Corrected:**

> *"**No defect remains open in how the contract assigns work.** Every obligation in §7–§9 correctly
> states who does what; the `TN-C-14` obligation, the `PO-3`/`PO-5` ordering rules and the
> `TN-C-15` audio ownership are all correctly specified. What remains open is of three kinds:
> **two `PASS-BLOCKING` defects** in framing and instrumentation (D-4, `DV-22`), **two
> `PASS-CONDITION` defects** in the justification attached to correct rules (D-1a's bound
> arithmetic, C4c-N1's observability premise), and **two `ADVISORY` items** (D-1b, D-6b).*
>
> *This is deliberately **not** phrased as "no normative defect remains open": D-1a is a defect in a
> normative clause's own failure column, and calling it non-normative would repeat the error
> corrected in §2.2. The accurate statement is narrower and is the one above: no normative clause
> **mis-assigns work**."*

The distinction being drawn: a clause can be **normatively correct in what it requires** while
**wrong in the guarantee it advertises**. D-1a is in that second category. My original sentence
collapsed the two, which is why §7 and §9 disagreed.

### 3.2 §7's `Blocks?` column — restated with the new taxonomy

| # | Defect | Class (§1.3) | Blocks `PASS`? |
|---|---|---|---|
| **D-4** | §8 preamble assigns audio to Agent 1 | `PASS-BLOCKING` | **Yes** |
| **D-22-scope** | `DV-22` blind to §8's preamble | `PASS-BLOCKING` | **Yes** (atomic with D-4) |
| **D-1a** | `TN-C-14`'s one-frame bound does not follow; `T-C05-64` cannot pass | `PASS-CONDITION` | **Yes** — wording only |
| **C4c-N1** | §3.6 reason (b) falsified by `PO-5` | `PASS-CONDITION` | **Yes** — wording only |
| **D-1b** | consumer definition inline rather than named | `ADVISORY` | **No** |
| **D-6b** | §5.4 tallies under-report (19/23, 11/12) | `ADVISORY` | **No** |
| **D-6a** | §1 row 6 "6 observed" | `RESOLVED` | n/a |
| *(mine)* | my "no V4_1 exists" claim | `CORRECTED` (review §1) | n/a |

### 3.3 §9's PASS criteria — corrected

**Original (review §9):**

> *"**What would move me to `PASS`:** D-4's two-word deletion and widened `DV-22`; C4c-N1's
> one-sentence rewrite; D-1a/D-1b/D-6b wording. **All six are closable…**"*

**Corrected — four changes, two of them atomic:**

1. **D-4 + D-22-scope.** Delete *"and audio"* from §8's preamble (2 words), **and** widen `DV-22` to
   scan all ownership prose, not only §5.2 rows 5/6 and `TN-C-15`.
2. **D-1a.** Make the one-frame bound follow from `TN-C-14`'s requirement (§2.2: interval-based,
   publish-relative, or weaken claim + `T-C05-64`), and make §1 row 2, `TN-C-14`, `T-C05-64` and
   §14.2 state the same number.
3. **C4c-N1.** Rewrite §3.6 reason (b) so its premise matches `PO-5`, keeping the conclusion and
   `PO-3`.
4. **Re-issue the blob** so the reviewed artifact matches the corrections.

**May remain open as advisory, and I would not withhold `PASS` for either:** D-1b (name the consumer
definition once), D-6b (state full cell counts or drop the tally column).

**Closable inside existing clauses. None reopens a settled requirement. No new normative content is
required beyond D-1a's choice among three already-drafted options.**

---

## 4. Agent 3's S4.1 review — status, kept independent

Recorded here because the review's §5 asserted this work was outstanding, and it no longer is.

| Field | Value |
|---|---|
| Artifact | `docs/AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md`, 114 lines |
| Commit / branch | `34b035b` · `refs/heads/arena/c64fc525-tdd` · committed `2026-11-17 18:21:50 +0000` |
| **Reviewed blob** | **`d54e194affeaee98b1030e2b83b4c34e234fa382`** — **the same blob I reviewed** |
| Publishing commit named | `95918268ed5b20b878fef3ee0a7855ad18e6eeb6` — the same commit |
| Predecessor use | S4.0 `424d2c69…` used **only** for a byte-diff check, explicitly not as a review target |
| Its own outcome | `TARGETED REVISION` |

**Verified independently of its conclusions:** it names the correct blob and commit, it states it
used S4.0 only as a diff baseline, and it records that its earlier S3 material was untracked and
unpublished. **It targets the right object.**

**Kept independent — and this is deliberate:**

- **I have not used Agent 3's findings as evidence for mine.** Where our conclusions coincide (the
  §8 preamble; the `TN-C-14` bound), it is recorded as **independent corroboration of the text**, and
  I state separately in §2.2 how I derived the D-1a arithmetic. Coincidence of conclusion is not
  transfer of proof.
- **I have not assessed Agent 3's cluster 1 finding** (§5.2 row 5's *"parry/block/dodge evaluation
  from the pull"* against the `TN-A` arbitration boundary). It is a distinct claim about a clause I
  did not examine; whether it is sound is for a review of Agent 3's review, which this is not.
- **Agent 3 has not reviewed my review**, and nothing here characterises its verdict on D-1b, D-6b
  or the taxonomy above. Its closure criteria are its own.
- **This addendum does not close Agent 3's review, adopt its findings, or speak for it**, and Agent 3
  has not endorsed anything in this document.

**Where the two reviews genuinely differ is not for me to adjudicate.** Both name the same blob, both
report `TARGETED REVISION`, and each sets its own conditions. **A reader comparing them should use
both, not either.**

---

## 5. Reproducible checks for this addendum

Document and arithmetic checks only. **No contract behaviour is exercised; 0 of 67 acceptance cases
are run.**

| # | Check | Method | Result |
|---|---|---|---|
| 1 | §9 and §6/§7 disagreed | read both, compare required-item lists | **contradiction found** ✔ |
| 2 | D-1b's definition is in the clause | read `TN-C-14` cell 2 verbatim | `"it acts on TN-C-10's output"` present ✔ |
| 3 | D-1b's readings coincide | trace compliance sets for both readings | identical → **not normative** ✔ |
| 4 | `TN-C-10`'s output is remaining time | read `TN-C-10` cell 2 | `R(t)=max(0, R0−(Axis(t)−AxisNow)×ProducerRate)` ✔ |
| 5 | `TN-C-14` constrains count, not interval | read cell 5 | `"at least once per frame, per held open instance"` ✔ |
| 6 | 1.98-frame gap is legal | schedule table §2.2 | **legal** ✗ bound fails |
| 7 | The bound is asserted in 4 places | grep `per frame`/`one frame` on blob `d54e194a` | §1 row 2, `TN-C-14`, `T-C05-64`, §14.2 ✔ |
| 8 | `T-C05-64` asserts the bound it cannot meet | read `T-C05-64` cell 3 | *"at most one frame"* ✗ |
| 9 | Agent 3 reviewed the same blob | `git ls-tree` + grep hashes in its artifact | `d54e194a` ×2, `95918268` ×3 ✔ |
| 10 | Agent 3's artifact is published | `git log 1eb613f3..origin/a3branch` | `34b035b`, 114 lines ✔ |
| 11 | Audio finding unchanged | re-read §8 preamble in blob `d54e194a` | still `"camera and audio"` ✔ |
| 12 | Reviewed blob unchanged | `git rev-parse 95918268:docs/…V4_1.md` | `d54e194a…` ✔ |
| 13 | W-M2.13 preserved | `git log -1 -- Docs/AGENT2_REASSESSMENT_A1C05_S4_1_V1.md` | `eee9401` ✔ |

---

## 6. What changed, stated plainly

| Item | Before (W-M2.13) | After (this addendum) |
|---|---|---|
| Closure vocabulary | three conflicting | **one taxonomy, four classes** |
| **D-1a** | minor / non-gating | **`PASS-CONDITION`** — *my finding was understated; bound fails arithmetically* |
| **D-1b** | "normative specification gap", non-gating | **`ADVISORY`** — the clause already defines it; readings coincide |
| **D-6b** | cosmetic / non-gating | **`ADVISORY`** — unchanged |
| §9 PASS list | six items incl. two advisory | **four changes, two atomic; two items explicitly advisory** |
| §7 summary | "no normative defect remains open" | **"no defect remains open in how work is assigned"** |
| D-4, C4c-N1, D-6a | — | **unchanged** |
| Reviewed blob | `d54e194a` | **`d54e194a`** |
| W-M2.13 | `eee9401` | **preserved unmodified** |

**Two self-corrections, both against my own severity assessments:** D-1b was over-classified and is
downgraded; D-1a was under-classified and is upgraded. **Neither changes a technical finding about
S4.1's text** — both change what I said that text costs.

---

## 7. What I did and did not do

**Did:** reconciled §6, §7 and §9 onto one four-class taxonomy; re-read `TN-C-14` and reclassified
D-1b from the clause rather than from my summary of it; derived the count-versus-interval
arithmetic showing `TN-C-14`'s stated bound does not follow and `T-C05-64` cannot pass as written;
corrected D-1a upward; restated §7's summary and §9's criteria; verified Agent 3's S4.1 review exists,
targets blob `d54e194a`, and is kept independent; verified the reviewed blob is unchanged.

**Did not:** change any technical finding on D-4, C4c-N1 or D-6a; reopen the S4.1 assessment or
review a different blob; undertake a new architecture review; alter W-M2.13; use Agent 3's findings as
evidence for mine; assess Agent 3's cluster-1 arbitration finding; speak for Agent 3; sign, freeze,
merge, select a MEAD, authorise M0, or close C-05/U-07; or claim any acceptance case executed.

**Still not signing v4.1.**

---

*End of addendum. `TDD-A2-REASSESS-A1C05-S4-1-ADDENDUM-A1` v1.0. Amends W-M2.13 (`eee9401`) without
altering it.*
