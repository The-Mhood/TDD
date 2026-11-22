# W-M2.23 — Independent verification of the L-1 correction (`6ddc8ed`)

| | |
|---|---|
| **Report ID** | `TDD-A2-VERIFY-C05-L1-001` |
| **Version** | 1.0 |
| **Subject** | `S4.3.11-L1: correct the L-1 DV-22 result cell (documentation only)` |
| **Commit verified** | **`6ddc8ed740b37d271cf2417a483c3408b1a41623`** |
| **Predecessor** | `06a4a8b47ab67d1525e738bd998000cb63dd4809` (S4.3.11) |
| **Verified by** | Agent 2 |
| **Method** | Clean `git archive 6ddc8ed` into `/tmp/a311l1`; no file edited |
| **Verdict** | **PASS** |

---

## 1. Bottom line

**PASS on all six requested checks.** The correction is exactly what it claims to be: four figures in
one result cell, plus an honest retraction of the "does not recur" inference in §2.26.5, the provenance
register and the status ledger. The instruments are **byte-identical**, no test case, expected verdict,
`F-1b` record or implemented behaviour moved, and C-05 is still `DESIGN_ONLY`, unsigned and unfrozen.

The four corrected figures are **the archived validator's own output** — I reproduced them from the
archived validator against the archived document, and they match to the digit.

---

## 2. Exact commit and blob hashes

### 2.1 Commit

| Field | Value |
|---|---|
| Commit | **`6ddc8ed740b37d271cf2417a483c3408b1a41623`** |
| Parent | `06a4a8b47ab67d1525e738bd998000cb63dd4809` — **direct parent, fast-forward lineage** |
| Ancestry | `06a4a8b` **is an ancestor** of `6ddc8ed` — nothing rewritten, nothing force-pushed |
| Files changed | **3** (all `docs/`) — no file outside `docs/` touched |

### 2.2 Blobs at `6ddc8ed`

| Path | Blob |
|---|---|
| `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md` | **`d9c3016cbd50d119721a1d09941bf69d31bc2527`** (2,587 lines) |
| `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11_PROVENANCE.md` | **`88d9167c581bf57cc26380d6d8171baa7f1ab033`** |
| `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` | **`828b00e4583c609dcfb0a6456b826c48ffacb01e`** |
| `docs/validation/dv_c05.py` | **`9e88c5a44c09788646198cbd77c4259c82534efe`** |
| `docs/validation/test_dv_c05_regressions.py` | **`ca0a4f902de74180fbf165013462a728130ddb07`** |

### 2.3 Superseded blobs, preserved intact at `06a4a8b`

| Path | Blob at `06a4a8b` | Status |
|---|---|---|
| `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md` | **`1929551681d6f6852076606384e22ad1424e266e`** | **intact, unmodified, still reachable** |
| `docs/validation/dv_c05.py` | `9e88c5a44c09788646198cbd77c4259c82534efe` | unchanged at both commits |
| `docs/validation/test_dv_c05_regressions.py` | `ca0a4f902de74180fbf165013462a728130ddb07` | unchanged at both commits |
| `docs/AGENT1_C05_F1B_CLOSURE_RECORD_V1.md` | `243c70b9b4f16fe318a9612f87c96c90e67ae4d5` | **unchanged at both commits** |

---

## 3. Check 1 — the four corrected DV-22 figures match the archived validator

**PASS.** Reproduced from the archived validator against the archived document; nothing was taken from
the commit message or the provenance register.

| Figure | `06a4a8b` cell (stale) | `6ddc8ed` cell | Archived validator prints | Match |
|---|---|---|---|---|
| Exempt lines | 343 | **432** | **432** | ✅ |
| — fenced | 201 | **228** | **228** | ✅ |
| — quoted table | 139 | **201** | **201** | ✅ |
| Audio mentions evaluated | 146 | **169** | **169** | ✅ |
| — marked block | 3 | 3 | 3 | ✅ (was already correct) |
| Scan offenders | 0 | 0 | **0** | ✅ |

The full sentence now reads, in the document and in the runner respectively:

```
DOC:    exempt lines 432 (fenced 228, quoted table 201, marked block 3);
        live sections unexempted True; audio mentions evaluated 169; scan offenders 0
RUNNER: exempt lines 432 (fenced 228, quoted table 201, marked block 3);
        live sections unexempted True; audio mentions evaluated 169; scan offenders 0
```

Programmatic comparison of the whole tuple `(432, 228, 201, 3, 169, 0)` from cell and runner:
**identical**.

I also confirmed the stale figures are now confined to the **corrective disclosure** at §2.26.5, which
quotes them deliberately to record what was wrong. No live claim carries 343/201/139/146 any more.

---

## 4. Check 2 — document validation passes 27/27

**PASS.**

```
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md
→ 27/27 checks passed
→ DV-22 PASS — ... exempt lines 432 (fenced 228, quoted table 201, marked block 3);
              ... audio mentions evaluated 169; scan offenders 0 []
```

27/27 both before and after the correction, which is the point: **the check never read the cell.**
`DV-22` computes its own counts and prints them. The run was always right; the transcription was wrong.
That is why `L-1` could persist under a green check, and the document says so explicitly at §2.26.5.

---

## 5. Check 3 — instruments byte-identical to `06a4a8b`

**PASS.** Confirmed by blob comparison, not by reading a diff:

| Instrument | `06a4a8b` | `6ddc8ed` | Result |
|---|---|---|---|
| `dv_c05.py` | `9e88c5a44c09788646198cbd77c4259c82534efe` | `9e88c5a44c09788646198cbd77c4259c82534efe` | **byte-identical** |
| `test_dv_c05_regressions.py` | `ca0a4f902de74180fbf165013462a728130ddb07` | `ca0a4f902de74180fbf165013462a728130ddb07` | **byte-identical** |

`git diff 06a4a8b..6ddc8ed` over either path is empty.

---

## 6. Check 4 — no cases, verdicts, F-1b records or behaviour changed

**PASS**, on five independent measures:

| Measure | Result |
|---|---|
| Files changed overall | **3**, all documentation — no instrument, no test, no record |
| Regression suite | **164/164** behave as required (unchanged blob, unchanged result) |
| Assessment probes | **12/14** — identical to `06a4a8b`; the two not moved are `R-4`/`R-4b` |
| Required controls | **26/26** — every one keeps its required verdict |
| `--compare` vs S4.3.10 | **exactly 8 moves**, `TD-122`…`TD-124` FAIL→PASS, `TD-125`…`TD-129` PASS→FAIL — the same 8 S4.3.11 made |

Additional checks:

- **Obligation and case rows:** all **237** lines matching `| **TN-…` or containing `T-C05-` are
  **byte-identical** between the two commits. No obligation, suite or case specification moved.
- **`F-1b`:** the closure record blob is `243c70b9…` at **both** commits; no file with `F-1B` or
  `closure` in its name appears in the diff. `F-1b` is untouched and remains `CLOSED`.
- **Deferred pins:** `TD-137` and `TD-138` still assert the **current, still-missed** verdict for
  `R-4`/`R-4b`. Deferred `D-c` behaviour did not drift into the correction.
- **Whole-file diff:** 14 changed lines, all in §2.26.5 and the one `DV-22` row. Nothing else.

Within the `DV-22` row itself, the diff is **four characters-groups only** — `343→432`, `201→228`,
`139→201`, `146→169` — with the row's entire descriptive text identical.

---

## 7. Check 5 — provenance register and STATUS_AND_CLAIMS.md accurate

**PASS.** Every factual claim in both documents was tested against the repository.

### 7.1 Provenance register

| Claim | Verified |
|---|---|
| Document blob `d9c3016c…` | ✅ `git rev-parse 6ddc8ed:…` matches |
| Document 2,587 lines | ✅ `wc -l` = 2587 |
| Earlier blob `19295516…` at `06a4a8b`, preserved intact | ✅ matches, commit reachable |
| Validator `9e88c5a4…`, suite `ca0a4f90…` | ✅ both match |
| §13.1 cell was `343 / 201 / 139 / 3 / 146` | ✅ matches `06a4a8b`'s text |
| Corrected to `432 / 228 / 201 / 3 / 169` | ✅ matches the run |
| Instruments byte-identical before/after | ✅ table is correct |
| 27/27, 164/164, 12/14, 26/26, 0 executed identical | ✅ all re-measured |
| `--compare` shows exactly 8 moves | ✅ counted 8, same case IDs |
| `L-2` did not recur; suite stated as 164 in §13 and §17 | ✅ confirmed |

The register also **explicitly preserves `06a4a8b` as "intact and unmodified; nothing was amended or
force-pushed"** — I confirmed that by ancestry, not by assertion.

### 7.2 `STATUS_AND_CLAIMS.md`

The `L-1`/`L-2` row was rewritten and is **now accurate**. Critically, it **retracts the previous
inference**: the old row asserted *"S4.3.11's own text is re-measured from its finished form, so the two
items do not recur in it"*. The new row states `L-1` **recurred** and is **`CORRECTED at S4.3.11-L1`**,
while `L-2` **remains `OPEN — parked`** against the unmodified S4.3.10 text. That is exactly the
correction my `W-M2.22` record required, and it is recorded in the right place.

One documentation nit, **not a finding against this commit**: the row's trailing column still carries the
original `L-1` description ("…vs runner 401/221/177/165…"), which describes **S4.3.10's** figures and is
correct in that context — but it now sits beside S4.3.11 text and reads as though it were current. It is
unambiguous to a careful reader and does not affect any claim. Recording it, not failing on it.

---

## 8. Check 6 — C-05 remains DESIGN_ONLY, unsigned, unfrozen

**PASS.** Asserted in all three documents and true in the repository:

| Statement | Location | Verified |
|---|---|---|
| `DESIGN_ONLY`; text `PROPOSED — NOT FROZEN` | document line 26 | ✅ |
| "Contracts signed / frozen: **None** — C-05 remains proposed and unsigned" | document line 2536 | ✅ |
| "C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD is selected." | document line 2587 | ✅ |
| `DESIGN_ONLY` classification retained on the `v4.3.11` row | `STATUS_AND_CLAIMS.md` | ✅ |
| "this is not contract approval, not MEAD completion and not closure of C-05" | `STATUS_AND_CLAIMS.md` | ✅ |

I searched for any affirmative `signed` / `frozen` / `approved` claim attaching to C-05: **none found**.
`U-07` remains open, **no MEAD** is selected, and `PROPOSED / NOT RUN` with **0 executed** is unchanged
(17 occurrences of `0 executed`, 75 of `PROPOSED / NOT RUN`).

**Governance state is unchanged by this commit.**

---

## 9. Result summary

| # | Check | Result |
|---|---|---|
| 1 | Four corrected DV-22 figures match the archived validator | **PASS** — 432/228/201/169, digit-exact |
| 2 | Document validation 27/27 | **PASS** |
| 3 | `dv_c05.py` and suite byte-identical to `06a4a8b` | **PASS** — both blobs identical |
| 4 | No cases, verdicts, `F-1b` records or behaviour changed | **PASS** — 164/164, 12/14, 26/26, 8 moves, 237 rows identical |
| 5 | Provenance register and `STATUS_AND_CLAIMS.md` accurate | **PASS** — all claims verified; retraction correctly recorded |
| 6 | C-05 `DESIGN_ONLY`, unsigned, unfrozen | **PASS** — asserted and true |

**Overall: PASS.**

**`L-1` is now CLOSED.** The correction is honest about its own cause — it records that the figures were
S4.3.8's snapshot inherited through S4.3.10, that the discrepancy was documentary only, and that the
check never read the cell. **`L-2` remains `OPEN — parked`** against the unmodified S4.3.10 text, which
is correct: it was never S4.3.11's to fix.

**This verification changes nothing.** No file was edited; `7662926`, `50578ed`, `f0f80b9`, `91fbf97`,
`06a4a8b` and `6ddc8ed` are all preserved as published. **0 of 67 acceptance cases executed** — the
164 suite cases test a document checker, not contract behaviour.

---

*End of report. `TDD-A2-VERIFY-C05-L1-001` v1.0. `6ddc8ed` — PASS on all six checks. Instruments
byte-identical, behaviour unchanged, `F-1b` untouched, `L-1` closed, `L-2` still parked, C-05 still
`DESIGN_ONLY`, unsigned, unfrozen.*
