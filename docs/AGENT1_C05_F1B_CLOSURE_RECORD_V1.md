# Closure record — `F-1b` (C-05), and the accepted independent verification

**Record ID** `A1-C05-F1B-CLOSURE-001` v1.0 · **Branch** `arena/3bc206a0-tdd` · **Date** 2026-11-18

**Purpose.** To record, in one place: that the independent verification published as `50578ed` on `arena/5dde91a4-tdd` is **accepted as PASS**; that **`F-1b` is CLOSED**; which commits and blobs are the implementation and verification records of record; and the three unrelated limitations that verification disclosed, recorded here **without reopening the fix**.

**What this record is not.** It is not a revision of the contract, the validator or the suite; it is not a signature, a freeze, an implementation authorisation or an acceptance claim; and it does not move any count, clause, obligation or proposed case. **It adds files and updates the status ledger. It edits nothing that was verified** — see §3.

---

## 1. The verification, and its acceptance

| Field | Value |
|---|---|
| Review | `TDD-A2-FINAL-VERIFY-C05-003` v1.0 — *Independent Final Verification — S4.3.10 (F-1b)* |
| Reviewer | Agent 2 |
| **Verdict, verbatim** | **`PASS WITH UNRELATED LIMITATIONS`** — recorded here as **PASS** |
| Commit | **`50578edaeed998dc683f00875c4814c8e8c6bf84`** on `arena/5dde91a4-tdd`, parent `0769248` (W-M2.19), dated `2026-11-18 10:22:46 +0000` |
| Report | `Docs/AGENT2_FINAL_VERIFY_C05_S4_3_10_V1.md`, 345 lines, blob **`66e745e43e47c5974121014726117a3d5fe48663`** |
| Evidence | `Docs/evidence/agent2/W-M2.20_evidence.json`, blob **`7222ebcd80a4b26b4618c211f794de0e453117c5`** |
| Reviewer's tests | `Tools/world/tests/test_review_a1c05_s4_3_10.py`, blob **`abfb8d64b548d5c17444c20f68db19599da8de3a`**; harness `Tools/world/gen_evidence.py`, blob **`e105c30a39c05535cedda28ecd5b18fae314e7b7`** |
| Status | **read only, not modified** — no file on that branch was edited by Agent 1 |

**Scope of what was verified, as the reviewer states it.** The reviewer pinned `7662926` and `83c24f9`, worked from `git archive` extractions of both, reproduced the four register blobs, and verified F-1b by **instrumenting the predicate** rather than reading a verdict: at S4.3.9 `NEG_BEFORE[10]` matched the literal `', the audio'` at span `(36, 47)`, `negated_mention` returned True and excused the second mention; at S4.3.10 no pattern spans it, `negated_mention` returns False and the `belongs to` attribution records the offence. It reproduced `27/27` and `147/147`, parsed all 147 `--compare` rows, found **exactly five moves, all `PASS → FAIL`**, and `0` rows disagreeing with their own expectation.

**Acceptance.** Recorded as **PASS**. The reviewer's own three limitations are accepted as *disclosed and unrelated* (§4) — they are documentary or explicitly out of scope, none affects a verdict, and the reviewer explicitly requests no further revision.

---

## 2. `F-1b` — CLOSED

| Field | Value |
|---|---|
| **Status** | **`CLOSED`** — reproduced, corrected, independently verified, accepted |
| Defect | The S4.3.6 object-negation construction read `(?:\bnot\|,)`, so a **bare comma** matched `, the audio` with no negator present and — because a denial excuses a mention only when its match spans it — negated the object of a clause that asserts Agent 1's ownership |
| Reproduction | `No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.` — `PASS` at S4.3.8 and S4.3.9; **`FAIL` at S4.3.10**, for the intended reason |
| Implementation | **`7662926c4c3b7293daedcc393c0ec4d015cdd883`** (S4.3.10) — see §3 |
| Verification | **`50578edaeed998dc683f00875c4814c8e8c6bf84`** — §1 |
| Other forms confirmed closed | `…, the audio cue is owned by Agent 1.` · `…, the audio cue is Agent 1's.` · `…, the audio cue belongs to the first agent.` · `Agent 1 owns the camera, the audio cues.` (all `PASS → FAIL`) |
| Legitimate forms confirmed preserved | 8 object negations, including `not any`, `but not`, the no-comma form, `,not` with no space, the longer-list control and `not the C-05 audio cues` — all `PASS` at both revisions |
| Positive controls confirmed still caught | 6 forms, including `The audio cues belong to Agent 1.`, `Agent 1 owns the audio cues.`, `Audio: Agent 1.` — all `FAIL` at both revisions |

**Duration of the defect, stated plainly.** `F-1b` was present from **S4.3.6** to **S4.3.9** — four published revisions — and it is the second fail-open found in this instrument by the reviewer chain rather than by the suite. It was surfaced at S4.3.9 as a separate defect with its rule and measurement, **not merged into the `F-1` correction**, and corrected only when TD authorised it as its own cycle. That sequence is recorded because it is the reason the class was not silently absorbed into an unrelated fix.

**What "CLOSED" does and does not mean.** It means the reproduced statement now fails `DV-22` for the intended reason, the equivalent forms fail with it, and nothing legitimate or previously verified was weakened. It does **not** mean `DV-22` is complete: the residual families in §5 remain open, some in the fail-open direction, and one of them is the same sentence shape as `L-3`.

---

## 3. Records of record — preserved, and provably unmodified

| Record | Commit | Blobs |
|---|---|---|
| **Implementation** (S4.3.10) | `7662926c4c3b7293daedcc393c0ec4d015cdd883` | document `857778e18a35b35b1a5420905ec5f1482fddf868` · register `675014ec84852d92ffe37769802ae97ac86796e3` · validator `353a2bff220d4daa4c176daafc941256098959ed` · suite `7ab55805c27a271706f16e9295f1f503dc5a6c94` |
| **Verification** (W-M2.20) | `50578edaeed998dc683f00875c4814c8e8c6bf84` | report `66e745e4…` · evidence `7222ebcd…` · tests `abfb8d64…` · harness `e105c30a…` |
| Predecessor preserved | `83c24f9ce974c8194d5788d62c28043cc7511974` (S4.3.9) | document `72d218a865b6713f78cb22308fa3dea81c74ac39` |

**Commands a reviewer can run to confirm this record changed no implementation:**

```bash
git rev-parse 7662926:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md   # 857778e1…
git rev-parse 7662926:docs/validation/dv_c05.py                       # 353a2bff…
git rev-parse 7662926:docs/validation/test_dv_c05_regressions.py      # 7ab55805…
git rev-parse 83c24f9:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md    # 72d218a8…
git diff 7662926 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md docs/validation/
# expected: no output — the verified tree is untouched by this record
```

**Files this record adds:** this file and `docs/AGENT1_C05_AGENT2_ASSESSMENT_REQUEST_V1.md`; it also appends to `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` and `docs/README.md`. **No validator predicate, no regression case, no contract sentence and no provenance register is edited.**

---

## 4. The three unrelated limitations — recorded, not reopened

Each was reproduced by me before being recorded; none is a defect in `F-1` or `F-1b`, none affects a verdict, and **fixing either documentary item would modify the verified document**, which the directive forbids. They are therefore parked, with the decision named.

### `L-1` — §13.1's `DV-22` result row is a stale snapshot (documentary, pre-existing)

| Measurement | Value |
|---|---|
| S4.3.10 §13.1, line **1846**, states | `exempt lines 343 (fenced 201, quoted table 139, marked block 3) … audio mentions evaluated 146; scan offenders 0` |
| The runner prints for the same document | `exempt lines 401 (fenced 221, quoted table 177, marked block 3) … audio mentions evaluated **165**; scan offenders **0**` |
| Where the stale numbers came from | `343 / 201 / 139 / 146` is **S4.3.8's** own row, where those values were correct; the row was inherited verbatim while the prose grew from 2,242 to 2,441 lines |
| Effect on verdicts | **none** — `DV-22` passes on this document either way; the offenders figure (0) is correct in both |
| Class | the same class as `MINOR-1`: a hand-carried tally that stopped tracking its computed value |

**Disposition: `OPEN — parked`.** Not fixed here, because the fix belongs in the S4.3.10 text, which is the verified artifact. **It requires a documentation-only revision** (re-measure the one cell, or head §13.1 as a snapshot of the revision that produced it) **on TD authorisation**.

### `L-2` — the version block states the suite as 146, not 147 (documentary)

| Line | Text | Correct? |
|---|---|---|
| 331 | `**The instrument suite grows 129 → 147**, eighteen cases in §5j` | yes |
| **2353** (§17, Version row) | `… the suite grows 129 → **146**` | **no** — the suite is **147**, as `147/147` in the same document states |
| §13 intro, §13.3.10 and this register | `147` throughout | yes |

**Disposition: `OPEN — parked`**, same reason and same route as `L-1`: a one-digit correction inside the verified document, to be made in a documentation-only revision. **It is not a second defect class** — it is the same drift as `L-1` in one digit. **Recorded in full at `docs/AGENT1_C05_L2_COUNT_ADDENDUM_V1.md`** (`A1-C05-ADDENDUM-L2-001`, documentation only): it confirms lines 331 and 2353 as the conflict, adds the further concordant statements at lines 1812, 1818 and 2192, and fixes the historical reading as `129 → 147 (+18)`. The artifact itself is still unmodified.

### `L-3` — the appositive `Agent 1` family is still accepted (out of scope, by directive)

| Input | S4.3.9 | S4.3.10 | Direction |
|---|---|---|---|
| `The audio cue, supplied by Agent 1, drives the mixer.` | PASS | **PASS** | missed assignment (**fail-open**) |
| `The audio cue, provided by Agent 1, drives the mixer.` | PASS | **PASS** | same |
| `The audio cue supplied by Agent 1 drives the mixer.` | PASS | **PASS** | same |

**Disposition: `OPEN` — referred to the separate assessment in §5.** It was out of scope for this cycle by the directive, it is unchanged by the correction, and it is **not** `F-1b`. Reopening `F-1b` to reach it would be the scope expansion the directive forbids.

---

## 5. Next unresolved C-05 items

| # | Item | Status | Owner / next action |
|---|---|---|---|
| 1 | **§3.6 residual families + the appositive `never` construction** — incl. the appositive `Agent 1` family (`L-3`) | **`PARTIALLY CLOSED at S4.3.11`** — assessed at `f0f80b9` (`TDD-A2-ASSESS-C05-RESIDUAL-001` v1.0); `D-a` + `D-b` closed, `D-c` (`R-4`/`R-4b`) deferred, `D-d` refused (see `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md` §2.26). Originally: `OPEN — assessment requested` | Agent 2, per `docs/AGENT1_C05_AGENT2_ASSESSMENT_REQUEST_V1.md`; `F-1b` stays closed while it is assessed |
| 2 | `L-1` and `L-2` (documentary, **S4.3.10 text only**) | **`OPEN — parked` on S4.3.10**; **do not recur in S4.3.11**, whose own text is re-measured from its finished form (§2.26.5) | Agent 1, documentation-only revision of S4.3.10 if TD authorises one; no action needed for S4.3.11 |
| 3 | `TN-C-11` / `TN-A-01` / `TN-A-02` (tag vs arbitration authority) | **`OPEN`** — unresolved, `B-15` stays `OPEN` because Agent 3's S3 review is absent | TD / Agent 3 |
| 4 | `U-07` | **`OPEN`** | TD |
| 5 | `TD-06`, `TD-09`, `TD-12` | **`OPEN`** — external blockers `B-1`, `B-2`, `B-4` | TD |
| 6 | `B-11` | **`BLOCKED BY DEPENDENCY`** on a C-04 decision | TD |
| 7 | Signature, freeze, canonical MEAD selection | **none** — `C-05` is `DESIGN_ONLY`, unsigned, unfrozen | TD |
| 8 | The 67 acceptance cases | **`PROPOSED / NOT RUN`, 0 executed** | nobody until authorised; the 147 regression cases are tests of the checker, **not acceptance evidence** |
| 9 | Agent 3's S4.2 … S4.3.10 reviews | **absent from this repository** — `OPEN — ARTIFACT ABSENT`; nothing attributed to Agent 3 | Agent 3 |

---

## 6. Status statement

**`F-1b` is `CLOSED`, on an accepted independent verification.** `F-1`, `CONDITION-1`, `CONDITION-2`, `MINOR-1`'s class and the seven `_joinable` boundaries remain closed and were re-verified by the reviewer at both revisions. **`7662926` and `50578ed` are preserved unmodified as the implementation and verification records.**

**C-05 remains `DESIGN_ONLY`, unsigned and unfrozen; `U-07` remains `OPEN`; no MEAD is selected; no normative clause moved; 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`, 0 executed; and the 147 regression cases are tests of the checker, not acceptance evidence.**
