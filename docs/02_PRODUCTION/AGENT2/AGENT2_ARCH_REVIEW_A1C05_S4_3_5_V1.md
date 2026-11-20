# AGENT 2 — INDEPENDENT ARCHITECTURE REVIEW OF `A1-C05-S4.3.5`

**Review ID:** `TDD-A2-ARCH-REVIEW-A1C05-S4-3-5-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — review only. Nothing signed, frozen, merged or approved. **No MEAD
selected. U-07 remains open. C-05 remains proposed.** **0 of 67 acceptance cases executed.**
**Outcome:** **`PASS WITH CONDITIONS`** (§9).

One MAJOR condition. It is confined to a single instrument predicate and does not touch the
contract, the obligations, the ownership model or the timing semantics. **The architecture is sound
and I would accept it as a baseline once that predicate is closed.**

---

## 1. Exact review target

Verified **before** reading, and re-verified after writing this report.

```
$ git rev-parse baa31db3c631f0fc3e69a82b6d71207ad8061218:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md
a0b46f46c81e85cea5d04b940aaf9aee46c19deb          <- matches the instruction exactly
```

| Field | Value |
|---|---|
| Repository | `The-Mhood/TDD` |
| Branch | `arena/3bc206a0-tdd` |
| **Reviewed commit** | **`baa31db3c631f0fc3e69a82b6d71207ad8061218`** |
| **Reviewed document blob** | **`a0b46f46c81e85cea5d04b940aaf9aee46c19deb`** |
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md`, 1,779 lines / 270,088 bytes |
| **Same-commit provenance blob** | **`0dba4a7c6eddd3ba0a3d61b408c2d3ee005a88cb`** |
| Provenance path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5_PROVENANCE.md`, 83 lines |
| Validator at that commit | `docs/validation/dv_c05.py`, blob read from `baa31db`, 645 lines |
| Regression suite at that commit | `docs/validation/test_dv_c05_regressions.py`, 284 lines |

**The commit is the current head of `arena/3bc206a0-tdd`.** I therefore cannot fall into the
blob-versus-tip trap I hit at S4.1: at this instant `baa31db` *is* the tip. I re-verified this at
commit time (§10).

**This is not a working-tree copy and not another branch's version.** I read the blob from
`baa31db` only. I did not review S4.3.4, S4.3.3, S4.3.2, S4.3.1, S4.3, S4.2 or any earlier successor
as the target; where I cite them it is to establish that a delta claim is true, or to check whether
an instrument discriminates.

**S4.3.5 is a metadata revision.** Its own claim (§0.7.5) is that it changes exactly three things —
one Scope-line figure, the §2.14 audit, and the §18.3 revision stamp — and nothing normative. **I
verified that claim rather than accepting it** (§3.5): all 43 obligation rows, the §5.2/§5.4/§9.2
clauses, §4.9, §3.6, §4.2 and all 17 case-specification rows are **byte-identical to S4.3.4**.
Because the substantive corrections were made at S4.3–S4.3.4, my review is necessarily of *the
accumulated contract as published at S4.3.5*, not only of the delta.

---

## 2. Methodology, and what these checks are

I read all 1,779 lines and the 83-line register. Beyond reading, I ran six kinds of check:

| Kind | What it establishes |
|---|---|
| **Independent re-derivation** | Every count, tally and structural total re-parsed from the blob rather than read from Agent 1's summary |
| **Executed validator** | Ran `dv_c05.py` on **this blob and on S4.3.4, S4.3.3, S4.3.2, S4.3.1, S4.3, S4.2, S4.1, S4.0, S3** |
| **Executed regression suite** | Ran `test_dv_c05_regressions.py` in clean `git archive` extractions of `40d29cc`, `90971e0` and `baa31db` |
| **Adversarial injection** | **24 audio-assignment forms** and **3 count-contradiction forms** injected into the reviewed text to test whether the predicates fire |
| **Prescription test** | **Implemented and executed my own two candidate fixes** for MAJOR-1 rather than asserting that they would work. **One was wrong and is recorded as rejected (§4.2).** The surviving fix was run against the clean document and the full 67-case suite |
| **Delta verification** | Byte-compared obligation rows, clauses and test specs against S4.3.4 to test the "nothing normative changed" claim |
| **False-existence checking** | Re-ran `git ls-remote` and searched every head for the Agent 3 artifacts §0.2/§0.8 claims do not exist |

**What none of this establishes — and I want this unambiguous.** I executed **zero** acceptance
tests. There is no engine, no compiler and no project in this workspace (B-3). The 67 proposed cases
`T-C05-01`…`T-C05-67` are **specifications**, every one `PROPOSED / NOT RUN`. The 67 *instrument
regression* cases are tests of the checker, **not** of the contract, and I do not treat them as
acceptance evidence — that distinction is the one S4.3.5 itself draws (§2.14, §13) and it is correct.
Every judgement below about C-05's behaviour is a judgement about **text**, and text cannot execute.

---

## 3. Verdict summary

| | Count |
|---|---|
| Review-scope areas assessed (§2 of assignment) | **10 of 10** |
| Previous D-1…D-7 and condition dispositions | **7 defects + 7 conditions, all CLOSED** |
| **MAJOR** findings | **1** |
| **MINOR** findings | **4** |
| **OBSERVATION** findings | **4** |
| **BLOCKER** findings | **0** |
| Regressions against a previously closed finding | **0** |
| Overall | **`PASS WITH CONDITIONS`** |

**The MAJOR finding is not an architectural defect.** It is one predicate in `DV-22` that still
admits two false negatives. The contract text is correct; the instrument that certifies one property
of it is not yet complete.

---

## 4. Findings

### 4.1 BLOCKERS — none

No finding blocks the contract. I checked the four ways a blocker would arise and none did:

- **Does any clause contradict another?** No. I traced §5.2 rows 5–8 against `TN-C-11`,
  `TN-C-15`, `TN-A-01`–`TN-A-03`, `C05-6.4` and §6.1 and found no pair asserting incompatible
  duties.
- **Is any obligation unsatisfiable?** No. Every `TN-` row has a defined producer, input, output and
  invalidation, and the ownership token of each maps to a permitted `C05-7.2` row (verified: 43
  cells, 0 failures).
- **Is any responsibility ownerless?** No. The two tokens with zero cells are `Agent 2, in its own
  systems` and `contract layer, owner pending TD-12`, both **explicitly outside C-05 by design**, and
  the second is TD-12's open decision (B-4), not a gap in this document.
- **Is any hidden dependency secret?** No. §14.1 and §14.2 disclose fifteen blockers including the
  one I care most about — **B-13, `AttackTag` ownership and registration, OPEN**, with the honest
  statement that "with no tag authored the field is empty and behaviour is unchanged".

### 4.2 MAJOR-1 — `DV-22`'s agent attribution admits two false negatives

**Severity: MAJOR.** **Location:** `docs/validation/dv_c05.py` lines 378 and 485–497, as published
at `baa31db`; asserted as passing in the document at **line 1345** (`DV-22` row) and demonstrated at
**§13.3.1, line 1410**.

**What I did.** `DV-22` is the instrument that enforces audio single-ownership across all ownership
prose. It is also the instrument my own `N-1` finding was against, and S4.3 rewrote it from a
keyword allowlist to a grammar-and-position predicate. **I attacked the new predicate with 24
injection forms.** 22 were classified correctly. **Two were not:**

| Injected line (into live text, immediately before §9) | `DV-22` verdict | Correct verdict |
|---|---|---|
| `Agent 1, unlike Agent 2, owns the audio cues.` | **PASS** — 0 offenders | **FAIL** |
| `The first agent owns the audio cues.` | **PASS** — 0 offenders | **FAIL** |

**Both mutated documents scored a clean `27/27 checks passed`.** No other check catches either line.
These are not near-misses of a threshold; they are outright false negatives on the exact property
`DV-22` exists to certify.

**Root cause, precisely.** Both failures come from one design choice: the predicate attributes a
mention to **the nearest agent reference before it** (line 495, `before[-1].group(1) == '1'`), and
`AGENT_REF` (line 378) recognises **only the literal forms `Agent 1` / `Agent-1` / `Agent 2`**.

1. *Contrastive phrasing.* In `Agent 1, unlike Agent 2, owns the audio cues`, the nearest agent
   reference before the mention is **`Agent 2`** — inside the contrastive `unlike` clause. The
   predicate therefore attributes the mention to Agent 2 and passes the line. The true subject is
   Agent 1. **The sentence already appears in natural English and the predicate reads it backwards.**
2. *Synonyms.* `The first agent` contains no `Agent <digit>` token, so `AGENT_REF` matches nothing,
   no attribution is made, and the line passes. This one matters more than it might look, because
   **this document uses "the first agent" as a synonym for Agent 1 seventeen times** (lines 162,
   203, 220, 422, 469, 1614 and others) — including at line 220, where it defines the `DV-22`
   acceptance criterion in exactly those words: *"the denial **names the first agent**"*. **The
   predicate cannot recognise the term the specification uses to describe it.**

**Why this is MAJOR and not MINOR.** `DV-22`'s stated purpose is that audio has exactly one owner
**in all ownership prose**. An instrument that certifies that property while passing two reachable
counterexamples overstates what has been tested (§2.14's limitation, §13's claim). This is the same
class of defect as the three `DV-22` false-negative rounds already recorded at S4.3.1, S4.3.2 and
S4.3.4 — **a check that is a function of the wording it happens to recognise rather than of the
property it claims.** Each earlier round was closed by adding recognised phrasings; this round needs
the attribution rule itself to be fixed, or the class will keep recurring in a fourth dialect.

**It is not a BLOCKER**, and I want to be explicit about why, because it would be easy to inflate.
The *contract text* is correct: §5.2 row 5 states Agent 1 owns no C-05 audio, §8's preamble states
it again, `TN-C-15` assigns cue selection to Agent 2 alone, and I verified **zero unmarked
Agent-1-audio assignments in the reviewed blob**. The defect is in the certificate, not the thing
certified. It matters because a later revision could reintroduce the defect in either of these two
dialects and `DV-22` would report PASS.

**Exact required change — and I tested my own prescription rather than asserting it.**

I first recommended two options. **I then implemented and ran both, and one of them is wrong.** I
record that rather than quietly deleting it, because the wrong one is the intuitive fix and the
next author is likely to reach for it.

- **(b) "Deny-by-default on appearance" — REJECTED on measurement.** The obvious fix is: in a live
  line with an audio mention and no recognised agent reference, fail. **Implemented and run, it
  produces 13–43 false positives on the clean document** (variance depending on how narrowly
  "assignment" is defined), because the authority, disposition and audit tables legitimately
  discuss audio without naming an agent — e.g. line 24, *"a second `DV-22` false-negative class —
  `no problem owning audio cues`"*, and line 83, *"Row 5 loses audio; row 6 keeps it"*. A narrow
  "positive ownership verb" guard still leaves **13**. It also misfires on `Agent 1 owns no audio
  cues` via seam artefacts. **Do not implement (b) as stated.**
- **(a) Fix attribution — VERIFIED.** Two changes to `dv_c05.py`:

  1. Recognise the synonym: extend `AGENT_REF` with `the first agent`, and read which agent a match
     designates from a **named group**, not `group(1)`. *(A naive `|the first agent` alternative
     without this leaves `group(1)` as `None`, never equals `'1'`, and the escape survives — I
     tested that too; it does not work.)*
  2. Resolve the subject past contrastive foils: drop any candidate reference preceded by
     `unlike`, `as opposed to`, `rather than`, `whereas` or `but not`, then take the nearest
     survivor.

  **Measured result.** Clean document: **`27/27`, 0 offenders** (unchanged). `The first agent owns
  the audio cues.` → **`DV-22 FAIL`, 1 offender**. `Agent 1, unlike Agent 2, owns the audio cues.`
  → **`DV-22 FAIL`, 1 offender**. Controls preserved: `Agent 1 owns no audio cues`,
  `Agent 1 has no C-05 audio responsibility`, `Audio is not owned by Agent 1`,
  `Agent 1, unlike Agent 2, owns no audio cues` → **all still PASS at 0 offenders**. And the
  **full 67-case regression suite passes 67/67 against the patched predicate — zero collateral
  damage.** *(Artefacts: `/tmp/mkfixa.py`, `/tmp/fixa.py`; not committed, since I do not modify
  Agent 1's instrument.)*

**I therefore recommend (a) only,** specified as above, and lift option (b).

**Acceptance criterion for closure:** both injected lines must yield `DV-22 FAIL`, added as
regression cases alongside `TD-31`…`TD-41`; the clean document must still score 27/27 with 0
offenders; the existing 67 must still pass; and the suite total restated wherever it appears
(§4.4).

### 4.3 MINOR-1 — the suite-count audit is a recorded table, and the document says so

**Severity: MINOR (acknowledged, not concealed).** **Location:** §2.14, line 502 ff.

The TD asked for a check of every suite-count claim. S4.3.5 delivers an **eleven-row audit table**
and states plainly: *"The audit is therefore a **recorded table**, reviewed by eye, not a guarantee
enforced by code — and that limitation is stated rather than implied."*

**I verified the audit rather than trusting it.** The claim that S4.3.4 said *74* is true. The claim
that the suite is 67 is true — I ran the suite in a clean archive of each commit:

| Commit | Suite total (executed by me) |
|---|---|
| `40d29cc` (S4.3.3) | **56/56** |
| `90971e0` (S4.3.4) | **67/67** |
| `baa31db` (S4.3.5) | **67/67** |

So 56 → 67 is confirmed independently, `+11` is confirmed, and the `74` was a drafting error.

**Why it is still MINOR rather than closed.** This is the **fourth** hand-restated count in this
document family to drift from its computed value (S2's DV-8, S3/S4's DV-11, S4.1's §1 row 6, S4.3.4's
Scope line). `DV-2` counts case ids in §11/§12; `DV-6` checks the 18 suites; **neither reads the
front matter**. The class is now recorded rather than suffered, which is genuine progress, but it
remains unenforced and the document correctly declines to claim otherwise.

**Required change:** none for this revision — TD explicitly scoped S4.3.5 to a correction and an
audit, and the limitation is honestly stated. **Recommended for a future revision:** a `DV-28` that
extracts every suite-total-shaped number from prose and compares it with the runner's count, which
is what would turn the recorded table into an enforced one.

### 4.4 MINOR-2 — closing MAJOR-1 will change the suite total, which §2.14's audit would then contradict
**Severity: MINOR, consequential on MAJOR-1.** **Location:** §2.14 (eleven-row audit), §13
introduction, §17 instrument-suite row.

If MAJOR-1 is closed by adding two regression cases, the suite goes from **67 to 69**, and the
eleven audit rows that state 67 — plus the §13 introduction, the §17 rows and the Scope line — all
become stale **in the same revision**, reproducing exactly the defect S4.3.5 was published to
correct. That is not a prediction, it is arithmetic on the audit's own contents.

**Required change:** when MAJOR-1 is closed, the audit table must be **re-derived**, not
incrementally patched — and the two new rows added to it. This is the strongest practical argument
for §4.3's recommended `DV-28`.

### 4.4b MINOR-3 — the obvious fix for MAJOR-1 does not work, and would look like it did

**Severity: MINOR (a trap, not a defect in the reviewed text).** This is a note for whoever closes
C-1, derived from my own failed attempt. Both of these *look* like fixes and neither is:

| Attempt | Why it looks right | What actually happens |
|---|---|---|
| `AGENT_REF = re.compile(r'agent[-\s]?([12])\b\|the first agent', re.I)` | adds the synonym | Match succeeds, but `group(1)` is **`None`** for the new alternative, so `group(1) == '1'` is never true. **The escape still passes.** |
| "fail on any un-attributable audio mention in live text" | deny-by-default, the right instinct | **13–43 false positives on the clean document**, because authority/disposition/audit tables discuss audio without naming an agent. The clean document stops scoring 27/27. |

**The lesson generalises** and is why I am recording it: `DV-22`'s history is four rounds of closing
a false-negative class by widening recognition, and the *widening* move is exactly the one that
recursively reintroduces a false-*positive* class. **Any fix must be demonstrated on three
populations at once — the clean document (27/27, 0 offenders), the two escapes (FAIL), and the
existing 67 regression cases (67/67)** — and nothing less should be accepted as closure for C-1.
That three-population test is what §4.2 option (a) passed and what both rows above failed.

### 4.4c MINOR-4 — my own W-M2.15 test module bound its instrument to a moving branch tip

**Severity: MINOR, against my own prior artifact, found during this review.** I record it because
I would rather find it than have someone else find it, and because it is the same class of error I
criticise elsewhere.

`Tools/world/tests/test_review_a1c05_s4_2.py` read the validator from
`origin/arena/3bc206a0-tdd:docs/validation/dv_c05.py` — a **branch tip**, not the reviewed commit.
While Agent 1's branch head stayed at `a788f95`, that happened to be correct. **The moment Agent 1
published S4.3, the test silently began scoring the S4.2 document with the S4.3.5 validator**, and
`TestValidatorExecuted.test_27_of_27_on_reviewed_blob` started reporting **24/27** — three checks
(`DV-22`, `DV-24`, `DV-27`) that S4.2 legitimately cannot satisfy, because they were added or
rewritten after S4.2 shipped. **My W-M2.15 evidence went stale without any change on my side.**

**Fixed in this revision.** The module now pins `S42_COMMIT:docs/validation/dv_c05.py`
(blob `381be714…`), and I added `TestInstrumentIsPinned`, which fails if any branch-tip read of
`dv_c05.py` returns. **A review of a pinned blob must be reproducible with the instrument that
shipped with that blob** — otherwise the review is a moving target that decays as the other agent
works, which is exactly the failure mode I have a standing rule against. *The rule was in my
process and not in my code; now it is in both.*

**This does not affect any S4.2 conclusion.** Every W-M2.15 number was correct at the time and
remains correct under the pinned instrument: **27/27**, verified again after the fix, 73/73 tests
passing.

### 4.5 OBSERVATIONS

**OBS-1 — the `N-2` identity collision is resolved by declaration, with a residual that requires a
push I may not make.** `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` resolves which artifact
`…-004.2` denotes, names the other `…-004.2-D`, declines to merge, and declines to review the other.
Its grounds are checkable and I checked the two that are load-bearing: the authoritative artifact
**is** the one TD pinned and the only one independently reviewed, and the axis measure **is** the one
closed against `D-1a`. The residual — line 3 of the file on `arena/c64fc525-tdd` still reads
`…-004.2` — is stated, scoped and correctly assigned to TD. **I confirm the collision was real and is
now dispositioned; I do not treat the residual as a defect in this document, and I note that my
`N-2` condition is satisfied in the only way available to a branch that may read but not write the
other.** *(Downgraded from blocking to observation because the ambiguity is now resolved by a
recorded decision with published grounds, not because the duplicate line is gone.)*

**OBS-2 — §13.3 documents my own attacks, and reproduces them as failing.** §13.3.1 lists my A2-1…A2-6
and P1–P7 injections with the verdict under S4.2's predicate and under S4.3's. **I verified that
claim by running the suite** and found the `keyword-prefixed injection is caught (the defect N-1
named)` case passing with `DV-22 expected FAIL, got FAIL`. Citing the reviewer's own counterexample
as a permanent regression case is the correct response and I record it as such — but it is precisely
why MAJOR-1 is disappointing: the instrument was hardened against **the sixteen forms I published**,
and two forms I did not publish still escape.

**OBS-3 — the arbitration boundary is correctly held, and the Agent 3 conflict is honestly
represented.** §9.2's three-domain split (creation / selection / outcome) is coherent: the producer
authors `AttackTag`, the consumer may use it to select, and **nothing** may use it to decide a hit.
`TN-A-02` is *extended, not weakened* — it now names `AttackTag` so "no value produced by C-05" cannot
be read as excluding the tag — and `TN-A-03` gives the boundary a positive, failable form. `C05-6.1`
and `TN-A-01` are byte-identical to S1 and S3. Critically, the document **states** that Agent 3's
review is not in the repository (§0.2, §0.8), that this is **S4's own resolution and not Agent 3's
proposed wording** (§9.2), and it asks Agent 3 to confirm or substitute. **That is an accurate
representation of an unresolved cross-agent disagreement, not a suppressed one.** TD-09 remains
OPEN and the ownership of the unblockable determination is untouched — correctly, since it is not
C-05's to settle.

**OBS-4 — the document distinguishes specification from execution throughout, and the
representative test specifications are genuinely well-formed.** `T-C05-63` combines a *held*
snapshot with an *in-place adversarial* `AttackTag` mutation and asserts on the resolver's
**input/use path** with a dataflow instrument — so *"a cached read cannot hide behind the absence of
a surface call"* — plus a separate positive assertion that the selection call site **does** consume
the tag. That is a falsifiable specification, not a restatement of the clause. `T-C05-64` encodes
three schedules including Agent 3's counterexample and two negative controls, and asserts the bound
**in the stated measure**. Every one of the 67 rows carries `PROPOSED / NOT RUN`; I searched §11–§12
for any execution claim and found **none**.

---

## 5. Assignment scope, item by item

The ten numbered areas in §2 of the assignment, each answered from the text.

| # | Area | Finding |
|---|---|---|
| 1 | **Ownership model coherent, implementable, internally consistent** | **Yes.** 43 obligations, 19 P / 15 C / 6 R / 3 A. Each carries a role token whose `C05-7.2` row is in the prefix's allowed set (`TN-P`→{2}, `TN-C`→{5,6}, `TN-R`→{2,4}, `TN-A`→{8}): **43 cells, 7 declared, 5 observed, 0 failures**. Ownerless responsibility is confined to the two tokens declared outside C-05 by design |
| 2 | **Responsibilities and authority boundaries correctly assigned** | **Yes.** §5.2's eight rows separate production, producer implementation, shared artefacts, read-surface support, two consumer integrations, out-of-C-05 systems, and arbitration. `C05-7.3` scopes "Agent 1 implements" to four disjoint areas. The arbitration row states **"C-05 supplies no input to it"** |
| 3 | **Message ownership, audio ownership, state transitions, timing semantics sufficiently precise** | **Yes, with one caveat.** `PO-3`/`PO-5` fix publication order *and* per-message content; `PO-4` fixes two-in-one-frame; `TN-C-14`'s five rules define the timing measure as **one frame on the shared axis** with a derived bound; `TN-C-15` makes cue selection Agent 2's alone. **Caveat:** the axis measure is only meaningful once **TD-06 (B-1, clock ownership) is decided** — the document says so, and it is a disclosed external dependency, not a hidden one |
| 4 | **Normative clauses agree with architecture, obligations, ownership tables, proposed cases** | **Yes.** `DV-12` keeps the seven `VF` names equal across three homes; `DV-11` keeps tokens equal to rows; §12.2 traces obligations to cases and back. **17 case specifications re-checked as byte-identical to S4.3.4** |
| 5 | **Contradictions, ambiguous responsibilities, impossible requirements, hidden dependencies** | **None found.** Fifteen dependencies disclosed in §14.1/§14.2. **B-13 (`AttackTag` ownership) is OPEN**, and the document states the field is empty and behaviour unchanged without it — honest, and the right disposition |
| 6 | **Preserves identity and scope decisions without silently changing the architecture** | **Yes.** `D-3` constancy stands (`fixed for the instance's lifetime`, 9 occurrences, `TN-P-04` names the change path, `T-C05-66` present). `C4a-2`'s `VF` list has one normative home. **No `TN-` row, no case specification and no §5.2/§5.4/§9.2 clause differs from S4.3.4** — verified byte-wise |
| 7 | **D-1…D-7 and conditions genuinely resolved** | **All 7 + 7 CLOSED** (§6) |
| 8 | **Agent 3 `TN-C-11`/`TN-A-01`/`TN-A-02` conflict accurately represented and unresolved where appropriate** | **Yes** — OBS-3. Resolved on its own terms, credited as S4's own, Agent 3 asked to confirm or substitute, TD-09 untouched |
| 9 | **New architectural defect or regression** | **No regression.** One instrument defect (MAJOR-1), two consequences (MINOR-1, MINOR-2), no contract defect |
| 10 | **Sufficiently precise to serve as a stable baseline** | **On the contract: yes**, once MAJOR-1 is closed. The remaining instabilities are external (TD-06, TD-09, TD-12) and are disclosed rather than papered over |

---

## 6. D-1 … D-7 and condition dispositions

Each verified against the text, not against the document's own status column.

| Finding | Disposition | Evidence I checked myself |
|---|---|---|
| **D-1** lost retime / stale rate | **CLOSED** | `TN-C-14` carries five rules; the bound is **derived**, and rule (iii) measures intervals on the shared axis. I brute-forced 400,000 legal schedules at S4.2 and found max staleness **0.999772 < 1**, matching the text's "approaches but never reaches one frame". `TN-C-14` is **byte-identical** to S4.2 here |
| **D-2** ordering / per-message content | **CLOSED** | `PO-5` present, interleaving stated in four places (`§3.6`, §4.9, `TN-P-18`, `EX-11`); reading B is the only legal reading. `TN-P-18` byte-identical to S4.2 |
| **D-3** identity constancy | **CLOSED** | `TN-P-19` and `TN-P-04` byte-identical; `fixed for the instance's lifetime` ×9; zero unquoted uses of the rejected phrase |
| **D-4** audio ownership | **CLOSED** | §8 preamble contains *"Agent 1 has no C-05 audio responsibility"* and **not** `camera and audio`; §5.2 row 5 clean; `TN-C-15` implementer = `Agent 2, C-05 consumer`. **My own whole-document sweep found 0 unmarked Agent-1-audio assignments** in the reviewed blob |
| **D-5** implementer-token mapping | **CLOSED** | 7 declared tokens, 5 observed over 43 cells; `TN-C-12`/`TN-C-13`/`TN-C-15` all on `Agent 2, C-05 consumer` → row 6 |
| **D-6** row-level `DV-11` | **CLOSED** | Re-implemented the allowed-row rule independently: **0 failures**. `DV-11` still fails on S3's blob, naming both mis-mapped rows |
| **D-7** `INV-2` precondition | **CLOSED** | Precondition in the clause, echoed in `TN-C-10`; `TN-C-10` byte-identical to S4.2 |
| **C4a-1** `INV-2` precondition | **CLOSED** | as D-7 |
| **C4a-2** `VF` list three homes | **CLOSED** | `DV-12` extracts all three; set equality asserted |
| **C4c-1** `EX-5` case (d) | **CLOSED** | present; `TN-C-14`(v) states the message-only residual as accepted |
| **C4c-2** `PO-3` order not content | **CLOSED** | `PO-5` + `TN-P-18` + `T-C05-51` extended + `T-C05-65` |
| **C6-1** constancy contradiction | **CLOSED** | as D-3 |
| **C6-2** audio owned twice | **CLOSED** | as D-4 |
| **C4c-N1** `PO-3` rationale (my S4.1 finding) | **CLOSED** | §3.6(b) states the order **is** observable through a mid-frame pull and records that the old premise was falsified; the two surviving "not observable" strings are a **quotation** in the disposition table and an unrelated `RS-3` statement — neither asserts it. `DV-26` fails on S4.1, passes here |
| **C9 / §3.11.1** 6 declared / 5 used | **CLOSED** | §5.4 declares **7** and states two carry no row by design; `DV-24` deny-by-default over the whole document |
| **C9 / §3.11.2** agent-level check | **CLOSED** | `DV-11` row-level |
| **`N-2`** duplicate `…-004.2` identity | **CLOSED** (by decision + residual) | OBS-1 |
| **`N-1`** `DV-22` keyword escape | **CLOSED for the published forms, but reopened in a new dialect** | §4.2. My `D-4 note:` attack is now **caught**; two un-published dialects still escape |

**Tally: 7 defects CLOSED · 7 conditions CLOSED · `N-2` CLOSED by decision · `N-1` PARTIALLY
CLOSED** (published forms closed, new dialects open → MAJOR-1).

---

## 7. Validator and evidence assessment

Required by §3 of the assignment. **Document validation is not architectural correctness, and I keep
them apart deliberately.**

### 7.1 What I reproduced

| Evidence claim | Reproduced? |
|---|---|
| `dv_c05.py` → **27/27** on the reviewed blob | **Yes**, in a clean `git archive` of `baa31db` |
| `test_dv_c05_regressions.py` → **67/67** | **Yes**, 67 PASS lines, **0** expectation mismatches |
| Suite is **67** at S4.3.4 and S4.3.5, **56** at S4.3.3 | **Yes** — ran each commit's suite in isolation |
| `74` was wrong in S4.3.4 | **Yes** — S4.3.4's Scope line says `from **56** to **74**` |
| Checker discriminates on earlier blobs | **Yes** — every score below is the **S4.3.5** checker run against an **older** document: S4.3.4/S4.3.3/S4.3.2/S4.3.1/S4.3 → 26/27, S4.2 → 24/27, S4.1 → 21/27, S4.0 → 21/27, S3 → 10/27. **This measures the checker's growth, not those documents' quality** — each earlier document scored **27/27 under the checker that shipped with it**. A lower number here means the check set expanded after that blob was published |
| `DV-22` fails on S4.1 **via the scan**, naming line 566 | **Yes** — the scan now reports offenders on S4.1 rather than 0 |
| `DV-24` catches second contradictory pairs, number words, and a mid-document pair | **Yes** — all three of my attacks caught |
| No Agent 3 S2/S3/S4.2 review exists | **Yes at review time** — three Agent 3 files exist, none mentioning `7d03e1df` or `a0b46f46` |
| Clean-archive reproduction | **Yes** — I used the same method independently |

### 7.2 Evidence claims I could NOT reproduce, or that overstate

**One.** `DV-22`'s own claim, at line 1345 and §13.3.1, that audio has exactly one owner **in all
ownership prose** with "no keyword escape". The keyword escape is genuinely gone — that is real
progress — but the **attribution** rule admits the two dialects in §4.2. The word "all" is doing more
work than the predicate can support. **This is MAJOR-1 and it is the only overstated claim I found.**

**The suite-count audit is not an enforced check**, and the document says so in terms. I record that
as **accurate disclosure, not overstatement** — the difference matters, and S4.3.5 gets it right.

### 7.3 The 27 checks as structural evidence

Are they adequate? **For structure, yes** — they cover obligation counts, row-level token mapping,
`VF` set equality across three homes, `INV-2` equivalence, `PO-3`/`PO-5` retention, identity
constancy, the audio property, the declared/observed class, and provenance/placeholders. Each is
shown failing on a blob that contains the defect it was built for. That is stronger than most
document checkers and I credit it.

**What they do not do**, stated because the assignment asks me not to confuse the two: they prove the
document is internally consistent and that the instruments reach their intended defects. **They prove
nothing about whether a telegraph, producer or consumer would behave correctly.** No engine exists
(B-3), and **0 of 67 acceptance cases have run.**

---

## 8. New defects and regressions

| # | Kind | Severity | Status |
|---|---|---|---|
| **MAJOR-1** | `DV-22` attribution admits two false negatives | MAJOR | **New** (a residual of the `N-1` class, not a regression) |
| **MINOR-1** | suite-count audit is a recorded table, not enforced | MINOR | Acknowledged in-document |
| **MINOR-3** | the obvious fixes for MAJOR-1 both fail; a naive synonym add is silently ineffective | MINOR | Trap for the next author |
| **MINOR-4** | my own W-M2.15 test bound its validator to a branch tip and went stale on S4.3 | MINOR | **Fixed in this revision** |
| **MINOR-2** | closing MAJOR-1 will stale eleven audit rows | MINOR | Consequential |
| **OBS-1…4** | identity residual; my attacks recorded; arbitration held; specs well-formed | OBSERVATION | — |
| — | **Architectural regression** | — | **None found** |

**No previously resolved issue regressed.** I verified the ten clauses most at risk of silent
regression (`TN-P-18`, `TN-P-19`, `TN-C-10`, `TN-C-11`, `TN-C-14`, `TN-C-15`, `TN-A-02`, `TN-A-03`,
`PO-5`, `C05-6.4`) and all are byte-identical to S4.2 or earlier as appropriate.

---

## 9. Overall verdict

# `PASS WITH CONDITIONS`

**On the contract: PASS.** The ownership model is coherent and implementable, the authority
boundaries are correctly drawn and held, the timing semantics are derived rather than asserted, the
arbitration boundary does not permit a C-05 value to decide a hit, and every one of my seven prior
defects and seven conditions is genuinely closed — **verified against the text and by executing the
instruments, not by reading the status column.**

**On the evidence: PASS WITH CONDITIONS**, because one instrument overstates what it certifies.

**The single condition:**

> **C-1 (required).** `DV-22` must fail on both of these, added as regression cases:
> `Agent 1, unlike Agent 2, owns the audio cues.` and `The first agent owns the audio cues.`
> Fix the subject-resolution rule per **§4.2 option (a) as measured there** — extend `AGENT_REF`
> with a *named group* for `the first agent`, and drop contrastive foils (`unlike`, `as opposed to`,
> `rather than`, `whereas`, `but not`) before taking the nearest prior reference. **Option (b) in
> §4.2 is rejected on measurement — do not implement it.** Then **re-derive** §2.14's audit rather
> than patch it (MINOR-2), and restate the suite total wherever it appears.
>
> **Verified closure test:** the clean document still scores **27/27 with 0 offenders**, both
> injected lines score `DV-22 FAIL`, and the existing regression suite still passes **67/67** (then
> 69/69 with the two new cases). I have run this configuration; it satisfies all three.

**Why `PASS WITH CONDITIONS` and not `TARGETED REVISION`:** the change is confined to one predicate
in one file plus the audit rows that depend on it. It touches **no clause, no obligation, no ownership
row, no test specification and no count of the contract**. A revision is not required to re-open
anything; it is required to complete one instrument. **If C-1 is closed I would move to `PASS`
without re-reviewing the contract text**, and I would want to see only the new predicate, its two
regression cases, and the re-derived audit.

**Why not `REJECT`:** nothing in the architecture is wrong. The defects I found are in the
certificate, and I say so plainly rather than letting a MAJOR finding imply a contract problem.

---

## 10. What I did and did not do

**Did.** Verified the exact commit and blob by hash before reading, and re-verified at commit time;
read all 1,779 lines plus the 83-line register; re-derived the 43/67/18/27 structural totals; verified
S4.3.5's three-change claim by byte-comparing 43 obligation rows, six clauses and 17 case
specifications against S4.3.4; re-implemented `DV-11`'s rule; ran the validator on **nine** blobs and
the regression suite in **three** clean archives; attacked `DV-22` with **24 injection forms** and
`DV-24` with **3**; verified the suite arithmetic 56 → 67 by execution; checked the arbitration
three-domain split against `TN-C-11`/`TN-A-01`–`03`/`C05-6.4`/§6.1; confirmed the `N-2` decision's
load-bearing grounds; re-checked the §0.2/§0.8 negative existence claims against every remote head;
and **implemented three candidate repairs to `DV-22` in a scratch directory and measured each one**
against the clean document, both escapes and the 67-case suite — rejecting two of them on evidence.

**Did not.** Modify Agent 1's S4.3.5 artifact, its validator or its regression suite — every repair I
tested was built in `/tmp` against a throwaway `git archive` extraction and **none was committed**;
review the unreviewed `…-004.2-D`
copy or assess its drafting quality; assert which of the two `…-004.2` artifacts is authoritative;
implement C++, Unreal systems, APIs or runtime code; build a new validator or add implementation;
execute or claim any of the 67 acceptance cases; treat the 67 instrument regressions as contract
acceptance tests; freeze, sign, merge or approve C-05; select a canonical MEAD; close U-07; consult,
coordinate with, or wait for Agent 3; or adjust this verdict to match any other agent's.

**C-05 remains proposed, unsigned and unfrozen. U-07 remains open. 0 of 67 acceptance cases
executed. B-1/TD-06, B-2/TD-09, B-4/TD-12 and B-13 remain OPEN.**

---

## 11. Provenance of this review

| Field | Value |
|---|---|
| Review ID | `TDD-A2-ARCH-REVIEW-A1C05-S4-3-5-001` v1.0 |
| Author | Agent 2 — World Structure and Level Architecture |
| Branch | `arena/5dde91a4-tdd` |
| **Reviewed commit** | `baa31db3c631f0fc3e69a82b6d71207ad8061218` |
| **Reviewed document blob** | `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` |
| **Provenance blob** | `0dba4a7c6eddd3ba0a3d61b408c2d3ee005a88cb` |
| Test-basis blobs | S4.3.4 `41df692d` · S4.3.3 `d827e017` · S4.2 `7d03e1df` · S4.1 `d54e194a` · S4.0 `424d2c69` · S3 `07723236` |
| Prior Agent 2 artifacts | `TDD-A2-REVIEW-A1C05-S4-1-001` (`eee9401`) · `ADDENDUM-A1` (`e434dbe`) · `TDD-A2-REASSESS-A1C05-S4-2-001` (`c8e9f2a`) — **all preserved unmodified** |
| Test module | `Tools/world/tests/test_review_a1c05_s4_3_5.py` |
| Engine | **NONE** — no Unreal, no GPU, no compiled code |
| Acceptance tests executed | **0 of 67** |

**Provenance rule applied.** My W-M2.13 §1.3 rule — *re-verify any negative existence claim as the
last action before publication* — was applied to the one repository-wide negative in this review
(the §0.2/§0.8 claim that no Agent 3 S2/S3/S4.2 review exists). `git ls-remote` was re-run
immediately before this report was committed, and the result is recorded in the commit message.

**Independence.** I did not read Agent 3's S4.2 or S4.3 assessment, did not wait for it, and did not
coordinate with Agent 3. Where this report describes Agent 3's conflict or its counterexample it is
quoting **Agent 1's** description of them in the reviewed text, and I make no independent claim about
Agent 3's conclusions. **My verdict is mine.**

---

*End of review. `TDD-A2-ARCH-REVIEW-A1C05-S4-3-5-001` v1.0. `PASS WITH CONDITIONS` — one condition,
C-1, confined to `DV-22`'s attribution rule and the audit rows that depend on it.*
