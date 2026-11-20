# Agent 1 — C-05 addendum: the S4.3.10 historical count statement (`L-2`)

**Addendum ID:** `A1-C05-ADDENDUM-L2-001`
**Version:** 1.0 — **documentation only**
**Date:** 2026-11-16 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Subject:** `A1-C05-S4.3.10` — the instrument suite's case count, as the published document states it
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no signature, no merge, no MEAD selection, no M0 claim. **C-05 remains proposed, unsigned and unfrozen; U-07 remains open.**

---

## 1. What this addendum is, and what it is not

**It records a discrepancy inside the published S4.3.10 text and states the consistent historical reading of it.** It is a documentation artifact: it adds no clause, obligation, count, case, verdict or mechanism, and it changes nothing in any implementation.

**The discrepancy is a historical documentation inconsistency — not a validator defect and not a contract defect.** One restated number in a version summary disagrees with the same document's scope statement, execution record and arithmetic; no predicate, verdict, obligation or case is implicated (§6).

**Four things it explicitly does not do**, because a reader should not have to infer them:

1. **The instrument suite was not rerun during this assessment.** No test command was executed as evidence for the figures below. Every number quoted here is quoted **as published**, not as re-measured.
2. **It does not claim independent execution or independent verification of the historical count.** The figure `147` is established from **the artifact's own internal statements**, three of which agree and one of which does not. That is an argument about a document, not a test result, and it is labelled as such throughout.
3. **It does not modify `A1-C05-S4.3.10`.** That artifact is preserved completely unchanged, byte for byte, as published at `7662926` — including the one statement this addendum identifies as wrong. Correcting it is not authorised here and is not performed here (§8).
4. **It does not characterise the discrepancy as a validator defect or a contract defect.** It is a **historical documentation inconsistency**: one restated number in a version summary, in a document whose other statements, and whose arithmetic, contradict it (§6).

---

## 2. The artifact examined

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md` |
| Version | `A1-C05-S4.3.10` v4.3.10 — the targeted closure of `F-1b` |
| Commit | **`7662926c4c3b7293daedcc393c0ec4d015cdd883`** |
| Blob | **`857778e18a35b35b1a5420905ec5f1482fddf868`** |
| Lines | 2,441 |
| Its instruments at that commit | validator `353a2bff220d4daa4c176daafc941256098959ed`, suite `7ab55805c27a271706f16e9295f1f503dc5a6c94` |
| State after this addendum | **unmodified** — `git diff 7662926 HEAD -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md` remains empty |

**How the artifact was read.** As text: the lines below were read from the file at that blob and are quoted verbatim, with their line numbers. No checker, suite or acceptance case was run to produce or support any statement in this addendum.

---

## 3. The exact conflicting sections [QUOTED]

**Four statements give the suite as 147; one gives it as 146.** The five are listed in document order so the disagreement is visible without cross-referencing anything outside this page.

| Line | Section | Verbatim statement | Figure |
|---|---|---|---|
| 331 | §0.7.10 — *What S4.3.10 changes* | `**The instrument suite grows 129 → 147**, eighteen cases in §5j` | **147** |
| 1812 | §13 — introduction | `plus **one hundred and forty-seven** regression cases on the checker itself` | **147** |
| 1818 | §17 — commands for all checks, inline expectation | `python3 docs/validation/test_dv_c05_regressions.py                              # 147/147` | **147** |
| 2192 | §13.3.10 — *What was run* | `**What was run.** The S4.3.10 suite (147 cases) …` | **147** |
| **2353** | **§17 — *The artifact to review*, the `Version` row** | `No other predicate, count or clause changes; the suite grows 129 → **146**` | **146 — the conflicting statement** |

**The conflict is confined to one cell.** Line 2353 is the `Version` row of §17's provenance table — a summary restatement of the revision. It is the only place in the document where the suite's size is given as 146. No other section repeats it, and nothing else in the document depends on it.

**What each location is for, so the conflict is not mistaken for a dispute between equals.** Line 331 is the revision's own scope statement, where the change itself is described and counted. Lines 1812 and 1818 are the §13 introduction and the §17 command block — the *execution record*, which state the expectation attached to the command that was run. Line 2192 is §13.3.10's account of what was executed for the cycle. Line 2353 is a one-line summary carried into the provenance table beside the document's other identifiers.

---

## 4. The corrected historical interpretation

**`129 → 147`, an increase of 18.**

| Element | Value | Where it comes from |
|---|---|---|
| Baseline suite at S4.3.9 | **129** cases | stated at line 2163 (§13.3.9: *"The S4.3.9 suite (129 cases)"*) and at line 317, S4.3.9's own change row; the two agree |
| Cases added at S4.3.10 | **18** | line 331, *"eighteen cases in §5j"*; the section it names, §5j, holds `TD-104`…`TD-121` — 18 cases |
| Resulting suite | **147** cases | 129 + 18 = 147; stated as 147 at lines 331, 1812, 1818 and 2192 |

**The arithmetic in the document is self-consistent in four places and broken in one.** The same sentence that gives the count also gives the number of cases added (*"… grows 129 → 147, eighteen cases in §5j"*), and 129 + 18 = 147. The conflicting statement, `129 → 146`, implies **17** additions and contradicts the `eighteen` printed beside it in §0.7.10 and the 18 cases actually enumerated in §5j. A reader who resolves the conflict by arithmetic gets 147 without needing any execution at all — which is precisely why this is classed as a documentation inconsistency rather than an unverifiable claim.

**The consistent historical reading is therefore `129 → 147 (+18)`.** The `146` at line 2353 is the *outlier*, not the correction: it is one restatement of four, and it is the only one that disagrees with the document's own addition.

---

## 5. Basis of the figures, stated without overclaiming

| Statement | Basis |
|---|---|
| S4.3.9 held 129 cases | as published at lines 317 and 2163 |
| S4.3.10 added 18 cases (`TD-104`…`TD-121`) | as published at line 331 and in §5j |
| S4.3.10's suite was 147 cases | as published at lines 331, 1812, 1818 and 2192 |
| §17's `Version` row states 146 | as published at line 2353 |
| That 146 is wrong and 147 is correct | **the document's own arithmetic and internal agreement** — not a run performed here |

**No execution was performed for this addendum.** Where the document says *"what was run"*, this addendum quotes it; it does not reproduce it, repeat it, or vouch for it. **The suite was not rerun during this assessment**, so no claim of independent execution or independent verification of the historical count is made anywhere in this document — and none should be read into it.

**A note on why the present-day instruments are not used as evidence.** They have since grown, under S4.3.11, to 164 cases (`TD-122`…`TD-138` added). A run of *today's* suite says nothing about what S4.3.10's suite contained, so it cannot arbitrate a digit in S4.3.10's text and is not cited for that purpose here.

---

## 6. Classification

| Question | Answer |
|---|---|
| Is this a validator defect? | **No.** The predicate's behaviour, thresholds, denial set and exemption rules are untouched, and no verdict depends on the digit. `DV-22`, `DV-24`, `DV-11` and the rest read the document's content, not a restated suite size in a provenance row |
| Is this a contract defect? | **No.** No clause, obligation, count, identity decision, measure or publication mechanism refers to the suite's size |
| Is this a test defect? | **No.** The suite at `7662926` is preserved with blob `7ab55805…`; nothing about its cases or expectations is implicated |
| Then what is it? | **A historical documentation inconsistency** — one restated number in a version summary, contradicted by the same document's scope statement, execution record and arithmetic |
| Does it change any result? | **No.** No verdict, acceptance result or governance status changes. The 67 acceptance cases remain `PROPOSED / NOT RUN`, 0 executed |

---

## 7. Relationship to `L-1`, to S4.3.11, and to the earlier record of `L-2`

**This is the second of the two documentary limitations raised at `6a7da5b`.** Both were found inside the verified S4.3.10 text; neither was a defect in what the document *does*.

| Item | Status before this addendum | Status after |
|---|---|---|
| **`L-1`** — §13.1's `DV-22` result cell was S4.3.8's stale snapshot | recorded at `6a7da5b`; recurred in the published S4.3.11 artifact | **corrected for S4.3.11's own text at `6ddc8ed`** (documentation-only). The same cell inside S4.3.10 remains stale, because S4.3.10 may not be modified (`L-1` is parked against it) |
| **`L-2`** — §17's `Version` row states the suite as `129 → 146` | recorded at `6a7da5b`, §`L-2` of the `F-1b` closure record, with lines 331 and 2353 already identified | **recorded here in full**, with all five statements, the arithmetic and the corrected reading. **`OPEN — parked` against S4.3.10**, which stays unmodified |
| **`L-2` in S4.3.11** | — | **does not recur**: S4.3.11's §13 and §17 both state the suite as **164**, consistently, and its `L-1` correction at `6ddc8ed` touched only the `DV-22` cell |
| Original S4.3.11 commit `06a4a8b` | published | **intact, unamended** — no force-push, no rewrite |

**Nothing here reopens `F-1b`,** which stays `CLOSED`, or the residual families: `D-c` remains **deferred**, `D-d` remains **refused**, `C` remains **not implemented**.

---

## 8. Disposition, and what would be needed to change the artifact

**Disposition of the discrepancy: identified, explained, and left in place.** `A1-C05-S4.3.10` is a verified artifact under independent verification (`TDD-A2-FINAL-VERIFY-C05-003` v1.0 at `50578ed`, accepted as `PASS WITH UNRELATED LIMITATIONS`). Editing a single digit inside it would invalidate the blob that verification pinned, so the inconsistency is corrected **by record, not by edit** — this page states what the document should be read as saying.

**If TD later authorises a documentation-only correction of S4.3.10 itself**, the change required is exactly one digit at line 2353 — `129 → **146**` to `129 → **147**` — with the artifact's blob and its verification pinned to the superseding commit, in the same way the `L-1` correction was handled for S4.3.11 at `6ddc8ed`. **That authorisation does not exist at the time of writing, and this addendum does not perform the change.**

---

## 9. Non-claims

This addendum is **not** a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. It is **not** independent verification of anything, and it is **not** a statement that S4.3.10's suite ever ran in the presence of its author of record. **C-05 remains `DESIGN_ONLY`, unsigned and unfrozen; U-07 remains open; 0 of 67 acceptance cases have been executed.**

---

## 10. Provenance of the artifacts this addendum names

Full hashes, so a reviewer resolves nothing by hand:

```bash
git rev-parse 7662926:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md
# 857778e18a35b35b1a5420905ec5f1482fddf868   (the artifact examined; unmodified)
git rev-parse 7662926:docs/validation/dv_c05.py                      # 353a2bff220d4daa4c176daafc941256098959ed
git rev-parse 7662926:docs/validation/test_dv_c05_regressions.py     # 7ab55805c27a271706f16e9295f1f503dc5a6c94
git diff 7662926 HEAD -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md   # empty, by requirement
```

**This file's own blob is not recorded inside it** — the same mechanism every register in this repository uses, for the same reason: a document cannot contain its own hash without a post-publication edit. It is pinned by the commit that publishes it, and indexed in `docs/README.md` beside the revision it annotates.
