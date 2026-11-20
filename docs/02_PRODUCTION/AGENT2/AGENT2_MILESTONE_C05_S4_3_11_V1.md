# W-M2.22 — S4.3.11 implementation milestone record

| | |
|---|---|
| **Record ID** | `TDD-A2-MILESTONE-C05-S4-3-11-001` |
| **Version** | 1.0 |
| **Milestone** | S4.3.11 (`A1-C05-S4.3.11`), commit **`06a4a8b`** |
| **Recorded by** | Agent 2 |
| **Milestone type** | Independent verification accepted, **implementation milestone** |
| **Status** | `IMPLEMENTED — VERIFIED — RECORDED` |
| **Not claimed** | **Not contract approval. Not MEAD completion. Not closure of C-05.** |

---

## 1. What this record is, and what it is not

This records S4.3.11 as a **successful implementation milestone** — the correction cycle Agent 1 was
authorised to run against Agent 2's assessment `TDD-A2-ASSESS-C05-RESIDUAL-001` v1.0 (`f0f80b9`) is
implemented, independently verified, and its results measured and preserved.

**It is not a design approval and it settles nothing about the contract.** The instrument got better.
The obligations did not change. Specifically, and per standing governance:

- **This is not contract approval.** C-05 remains `DESIGN_ONLY`, **unsigned**, **unfrozen**.
- **This is not MEAD completion.** No MEAD has been selected.
- **This is not closure of C-05.** `U-07` remains **`OPEN`**. `B-15` remains **`OPEN`**.
  `TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and untouched.
- **`0 of 67` acceptance cases executed.** The 164 suite cases are tests of a **document checker**,
  not acceptance tests. Nothing here demonstrates that any contract obligation holds.

---

## 2. The artifact of record

| Item | Value |
|---|---|
| Commit | **`06a4a8b`** |
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md` — blob **`1929551681d6f6852076606384e22ad1424e266e`**, 2581 lines |
| Provenance register | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11_PROVENANCE.md` — blob `9b4edc0d75de34f45997df27ec56b9256cd75742` |
| Validator | `docs/validation/dv_c05.py` — blob **`9e88c5a44c09788646198cbd77c4259c82534efe`** |
| Suite | `docs/validation/test_dv_c05_regressions.py` — blob **`ca0a4f902de74180fbf165013462a728130ddb07`** |
| Predecessor | S4.3.10 at `7662926` — doc `857778e1…`, validator `353a2bff…`, suite `7ab55805…` — **preserved unmodified** |

Verified from a clean `git archive 06a4a8b` tree at `/tmp/a311`; committed blob hashes compared against
the working copy before any measurement.

---

## 3. Measured results

All figures below are **re-measured at `06a4a8b`**, not restated from Agent 1's report.

| Axis | Result | Note |
|---|---|---|
| Document checks | **27/27** | `dv_c05.py` over the S4.3.11 text |
| Suite | **164/164** | 147 carried + **17 new** (`TD-122`…`TD-138`); no pre-existing case edited |
| Assessment probes | **12/14** | the two not moved are the **deferred** `R-4`/`R-4b` |
| Required controls | **26/26** | 4 object negations, 5 positive, 4 `CONDITION-1`, 3 `F-1`, 3 `CONDITION-2`, 7 `_joinable` |
| Independent edge cases | **17/17** | the 17 new suite cases, all passing |
| Acceptance cases executed | **0/67** | unchanged, and must stay so |

### 3.1 Probe-by-probe, at `06a4a8b`

| Probe | Required | Baseline `7662926` | `06a4a8b` | State |
|---|---|---|---|---|
| `R-1` `never the audio cues` | PASS | FAIL | **PASS** | ✅ closed by `D-a` |
| `R-1b` `never any audio cues` | PASS | FAIL | **PASS** | ✅ closed by `D-a` |
| `R-1c` `never`, no comma | PASS | FAIL | **PASS** | ✅ closed by `D-a` |
| `R-3b` `have been owned by` | FAIL | PASS | **FAIL** | ✅ closed by `D-b` |
| `R-5` `, supplied by Agent 1,` | FAIL | PASS | **FAIL** | ✅ closed by `D-b` |
| `R-5b` `supplied by` (no commas) | FAIL | PASS | **FAIL** | ✅ closed by `D-b` |
| `R-5c` `, provided by Agent 1,` | FAIL | PASS | **FAIL** | ✅ closed by `D-b` |
| `R-4` `, not Agent 2,` | FAIL | PASS | *PASS* | ⏸ **DEFERRED** — `D-c` |
| `R-4b` `, never Agent 2,` | FAIL | PASS | *PASS* | ⏸ **DEFERRED** — `D-c` |
| `R-2` `may` / `R-2b` `must` / `R-3` `has owned` | FAIL | FAIL | FAIL | ✅ unchanged |
| `R-6` `unlike` / `R-7` `The first agent` | FAIL | FAIL | FAIL | ✅ unchanged |

**Seven of nine closed. The two that did not move are exactly the two that were deferred.**

### 3.2 What was implemented, and one authorised deviation

The cycle was authorised as `A+D` — the two closed-set widenings Agent 2 measured as safe. What
shipped is `A` verbatim plus a **hardened** `D`:

- **`D-a`** — the object-negation negator set takes `never` as well as `not`, at that site only.
  `never` does **not** enter `NEG_AFTER` and does **not** enter `_FOIL_ANY`. Implemented as specified.
- **`D-b`** — the passive is read through its **auxiliary chain** (simple copula, `has|have|had been`,
  and a **guarded** zero-copula appositive), **on the attribution and on its quantified denial alike**.

The deviation is deliberate and it is the right call. Agent 2's `D` made the copula *merely*
optional; applied literally, that also reads a **negated** passive (`are not provided by Agent 1`) as an
assignment. Agent 1 measured **eight** new false alarms on legitimate denials and added three negative
lookbehinds (`not`/`never`/`been` before the participle) plus the denial-side widening to remove all
eight. The deviation is disclosed in §2.26.2 rather than absorbed.

**This closes the caveat Agent 2 raised in the assessment at §5.3** — that a bare optional copula left
`attributed=True` on genuine denials, one ordering decision away from a false alarm. Re-measured at
`06a4a8b`: the denial-side predicate is now clean, not merely order-saved.

| Denial | `negated` | `attributed` | Verdict |
|---|---|---|---|
| `Audio is not owned by Agent 1.` | True | **False** | PASS ✅ |
| `Audio is not provided by Agent 1.` | False | **False** | PASS ✅ |
| `No audio cue has been owned by Agent 1.` | True | True (saved by `negated`) | PASS ✅ |
| `None of the audio cues have been owned by Agent 1.` | True | True (saved by `negated`) | PASS ✅ |
| `Audio has never been owned by Agent 1.` | False | **False** | PASS ✅ |

---

## 4. What was correctly *not* done

Recorded so the exclusions are deliberate, not oversights:

- **`C` is unimplemented.** `_FOIL_ANY` at `06a4a8b` is byte-identical to `7662926`:
  `\b(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\b` — no `not`, no `never`. Verified.
  The assessment's two measured reasons to refuse it both still hold at `06a4a8b`:
  `Not only does Agent 1 own the audio cues.` is still **FAIL** (not re-opened as a false negative),
  and the `C+D` interaction that broke eight controls was never entered.
- **`D-c` (`R-4`/`R-4b`) remains DEFERRED** — unchanged, still missed, and now **pinned** so it cannot
  drift silently: `TD-137` and `TD-138` assert the current (still-wrong) verdict. These are
  *characterisation* tests, not approvals; when `D-c` is fixed they must move together, and moving them
  is the signal that the deferred item was taken up.
- **`D-d` remains REFUSED.** `_FO_PART` is still
  `(?:owned|claimed|carried|held|supplied|provided|selected|chosen)` — no `assigned`, `managed`,
  `controlled`, `authored`, `approved`, `commissioned`, `mixed`, `routed`. The taxonomy was not widened.
- **`F-1b` was not reopened.** `TD-104`…`TD-121` carried unchanged and all pass.

---

## 5. Outstanding documentation requirement — `L-1` recurs at S4.3.11

**This is the one defect found in the record, and it is documentary, not behavioural.** No probe,
control, check or case is affected.

S4.3.11's §13.1 `DV-22` row publishes the tallies of an **older document**:

| | §13.1 row asserts | Runner prints | Difference |
|---|---|---|---|
| Exempt lines | 343 | **432** | +89 |
| — fenced | 201 | **228** | +27 |
| — quoted table | 139 | **201** | +62 |
| Audio mentions evaluated | 146 | **169** | +23 |
| Scan offenders | 0 | 0 | ✅ |

The string is **byte-identical across S4.3.10 and S4.3.11** — `343 (fenced 201, quoted table 139,
marked block 3) … 146`. For S4.3.10 the row is `L-1`, already recorded and **parked**, because
correcting it would edit a verified artifact. S4.3.11 **carried it forward verbatim**, so the number now
describes **S4.3.9**'s text (401/221/177/165 was S4.3.10's real figure; 343/201/139/146 is older still)
and describes neither S4.3.10 nor S4.3.11.

**This contradicts an explicit claim in the document.** §2.26 states, at line 1138:

> *"This revision's own text is re-measured from its finished form: §13.1's `DV-22` row states this
> document's actual counts, and §17 states the suite as 164. `L-1` and `L-2` therefore remain open
> **on S4.3.10 only**."*

The second half is true — **§17 does state 164**. The first half is not: §13.1's `DV-22` row does **not**
state this document's actual counts. And the governance record (`STATUS_AND_CLAIMS.md`) propagates the
same inference — *"S4.3.11's own text is re-measured from its finished form, so the two items do not
recur in it."*

**Therefore, as a documentation requirement:**

- **`L-2` is genuinely closed at S4.3.11** (no stale `146`-suite claim survives in its prose; §17 says 164).
- **`L-1` is NOT closed. It recurs, unmodified, at S4.3.11.** It should be recorded as
  **`OPEN — recurs at S4.3.11 (§13.1 DV-22 row) — documentation-only`**, not as closed by construction.
  The "closed by construction" argument requires the row to actually carry the measured value; it does not.
- The correction is a **documentary edit to §13.1's `DV-22` cell only** (343→432, 201→228, 139→201,
  146→169). It needs a TD-authorised documentation cycle, because it modifies a published contract
  document. **I have not made it** — this is an assessment record, and no implementation change is
  requested from me at this stage.

**Nothing else is outstanding against S4.3.11.** The instrument, the suite and the probe results are all
consistent, and I found no other discrepancy.

---

## 6. Standing state after this milestone

| Item | State |
|---|---|
| S4.3.11 (`06a4a8b`) | **IMPLEMENTED — VERIFIED — RECORDED** |
| `D-a`, `D-b` (`R-1`, `R-1b`, `R-1c`, `R-3b`, `R-5`, `R-5b`, `R-5c`) | **CLOSED** |
| `D-c` (`R-4`, `R-4b`) | **DEFERRED** — unchanged, pinned by `TD-137`/`TD-138` |
| `D-d` | **REFUSED** |
| `C` | **UNIMPLEMENTED** — `_FOIL_ANY` byte-identical |
| `F-1b` | **CLOSED**, not reopened |
| `L-1` | **OPEN — recurs at S4.3.11**; documentary only |
| `L-2` | **CLOSED at S4.3.11** |
| C-05 | `DESIGN_ONLY`, **unsigned**, **unfrozen**, **not closed** |
| `U-07` | **OPEN** |
| MEAD | **none selected** |
| `B-15` | **OPEN** |
| `TN-C-11` / `TN-A-01` / `TN-A-02` | unresolved, untouched |
| Acceptance cases executed | **0 of 67** |

**Status: implementation milestone achieved. No further implementation changes are requested from
Agent 2 at this stage. The single open item is the documentary `L-1` correction at S4.3.11 §13.1.**

---

*End of record. `TDD-A2-MILESTONE-C05-S4-3-11-001` v1.0. Seven of nine residual probes closed by an
authorised two-site correction; the deferred pair unchanged and pinned; `C` unimplemented; `D-d`
refused; `F-1b` not reopened. Measured 27/27, 164/164, 12/14, 26/26, 17/17, 0/67. One documentary
requirement outstanding: `L-1` recurs at S4.3.11 and is not closed by construction.*
