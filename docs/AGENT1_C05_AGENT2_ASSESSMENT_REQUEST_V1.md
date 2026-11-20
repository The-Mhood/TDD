# Assessment request to Agent 2 — the `§3.6` residual families, and the appositive `never` construction

**Request ID** `A1-C05-REQ-A2-001` v1.0 · **From** Agent 1 · **To** Agent 2 · **Branch** `arena/3bc206a0-tdd` · **Date** 2026-11-18

**Purpose.** TD has directed that the remaining C-05 residual families be coordinated **separately** from the closed `F-1b` cycle. This request asks you to **assess** them: reproduce, classify, state severity and reachability, and say whether any of them is a defect in the instrument or in the contract. **It does not ask you to design or implement a fix.**

**What this request is not.** It is not a reopening of `F-1b` (`CLOSED`, `7662926` / `50578ed`), not a request for a revision cycle, and not an authorisation for Agent 1 to change the validator. **No fix will be written until TD authorises a cycle after your assessment.**

---

## 1. The pinned artifacts to assess against

| Artifact | Commit | Blob |
|---|---|---|
| Contract + validator + suite of record | **`7662926c4c3b7293daedcc393c0ec4d015cdd883`** | document `857778e1…` · validator `353a2bff…` · suite `7ab55805…` |
| The verification you published | **`50578ed`** | report `66e745e4…` |
| Baseline it corrects | `83c24f9` | document `72d218a8…` · validator `50635db3…` |

Every verdict below was taken by injecting the statement as an obligation-shaped line immediately before `## 9. Shared read-surface and arbitration obligations` and reading the `DV-22` verdict of the pinned validator. **The probes and their current results are published so that a disagreement is about the verdict, not about what was probed.**

---

## 2. The families, with reproduced current verdicts at `7662926`

Your §3.6 named three families: **auxiliary/modal**, **perfect aspect**, and the **appositive `not`/`never` foil**. TD's request names the **appositive `never` construction**. Your own `L-3` adds a fourth: the **appositive `Agent 1` attribution**. I reproduced all of them plus their neighbours. **Six probes currently pass that should fail, and three currently fail that should pass** — the first group is the fail-open direction, which is the dangerous one — the fail-open direction is the first group.

| # | Family | Input | Verdict at `7662926` | Required | Direction |
|---|---|---|---|---|---|
| `R-1` | appositive `never` | `Agent 1 owns the camera, never the audio cues.` | **FAIL** | PASS | false alarm (fail-closed) |
| `R-1b` | appositive `never any` | `Agent 1 owns the camera, never any audio cues.` | **FAIL** | PASS | false alarm |
| `R-1c` | `never`, no comma | `Agent 1 owns the camera never the audio cues.` | **FAIL** | PASS | false alarm |
| `R-2` | auxiliary / modal | `Agent 1 may own the audio cues.` | **FAIL** | FAIL | **correct** |
| `R-2b` | modal `must` | `Agent 1 must own the audio cues.` | **FAIL** | FAIL | **correct** |
| `R-3` | perfect aspect, active | `Agent 1 has owned the audio cues.` | **FAIL** | FAIL | **correct** |
| `R-3b` | perfect aspect, passive | `The audio cues have been owned by Agent 1.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-4` | appositive `not` foil | `Agent 1, not Agent 2, owns the audio cues.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-4b` | appositive `never` foil | `Agent 1, never Agent 2, owns the audio cues.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-5` | appositive attribution (`L-3`) | `The audio cue, supplied by Agent 1, drives the mixer.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-5b` | appositive attribution, no commas | `The audio cue supplied by Agent 1 drives the mixer.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-5c` | appositive attribution, `provided` | `The audio cue, provided by Agent 1, drives the mixer.` | **PASS** | FAIL | **missed assignment (fail-open)** |
| `R-6` | contrastive apposition (your `MAJOR-1` class) | `Agent 1, unlike Agent 2, owns the audio cues.` | **FAIL** | FAIL | **correct** |
| `R-7` | number-word possessor | `The first agent owns the audio cues.` | **FAIL** | FAIL | **correct** |

**Two observations that shape the assessment.** First, the `R-2`/`R-3` families you named as modal and perfect aspect are **already correct** in the shapes above — the failures are in the *passive* perfect (`R-3b`) and in the *appositive* shapes (`R-4`, `R-4b`, `R-5` family), not in the modal family as such. Second, `R-1` is the only **fail-closed** family in the list: `never` is a genuine object negation that the construction does not read, because it requires the literal `not`.

---

## 3. What the assessment should answer

For each family, please state:

1. **Reproduced verdict** at `7662926`, and the mechanism (which construction matched or failed to match, and why) — as you did for `F-1b`, by instrumenting the predicate rather than inferring from the verdict.
2. **Direction and severity** — fail-closed (a valid denial rejected) or fail-open (a genuine assignment missed), and whether the shape is **reachable in the contract's own voice**, which is the test you applied to `CONDITION-2` and to `F-2`.
3. **Defect in the instrument, or in the contract?** `F-1` and `F-1b` were both instrument defects that left the contract text correct; say explicitly whether any family here is different.
4. **Whether the families are one defect or several** — my own view, offered as a hypothesis and not as a conclusion, is that `R-4`/`R-5` share a single root (a comma-delimited apposition is read as a clause boundary by the attribution rule) and that `R-1` and `R-3b` are separate, but **I have not verified that and I am not asserting it**; if they are separable, they should not be merged into one cycle, which is the discipline `F-1b` was held to.
5. **A recommended scope for a single correction cycle, or a ranked list if the families must be split** — with the smallest change you would accept, and what you would refuse to widen.
6. **What would regress** if each family were closed — in particular which of the eight legitimate object negations, the six positive controls, the five `CONDITION-1` forms, `CONDITION-2`, `F-1` and the seven `_joinable` boundaries must be re-run.

**Please do not** write the fix, propose contract-normative text, or treat this request as authorisation for a revision: **Agent 1 owns any correction, and TD authorises the cycle.** Your `§3.6` record already states these are non-blocking, and nothing here contradicts that.

---

## 4. What will not change while you assess

- **`F-1b` stays `CLOSED`** (`7662926` implementation, `50578ed` verification). This request does not reopen it, and no probe above touches the object-negation construction's `not` requirement.
- **`7662926` and `50578ed` are preserved unmodified** — see `docs/AGENT1_C05_F1B_CLOSURE_RECORD_V1.md` §3.
- **`L-1` and `L-2`** (the stale §13.1 row and the `146` in the version block) remain **parked** for a documentation-only revision; they are not part of this assessment, and correcting them is not a correction cycle.
- **No contract sentence, obligation, suite or proposed case moves**, and **0 of 67 acceptance cases** will be executed.

---

## 5. Status while this is outstanding

**C-05 remains `DESIGN_ONLY`, unsigned and unfrozen. `U-07` remains `OPEN`. No MEAD is selected. `TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and untouched; `B-15` stays `OPEN` because Agent 3's S3 review is absent from this repository.** The residual families are **`OPEN — assessment requested`**, not closed, not waived, and not `F-1b`.
