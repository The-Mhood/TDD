# W-M2.3 — TECHNICAL DIRECTOR CORRECTION

**Document:** TDD-WCOR-001 · **Version:** 1.0 · **Date:** 2026-11-16
**Author:** Agent 2 — World, Systems and Gameplay Simulation
**Supersedes:** nothing. **Amends:** W-M2.2 (`64adc9f`), which is preserved.
**Status:** `PROVISIONAL` — corrections to a projected estimate. Nothing here is measured.

---

## 1. Scope

Two corrections and one modelling decision from the Technical Director, on review of
`64adc9fb274cbf7e16bb607332874aef96dda05d`.

| # | Item | Effect |
|---|---|---|
| 1 | Exact dozen | `CH01-SCN-018` reclassified from UNRESOLVED to a register count of **12** |
| 2 | Measured provenance | `npcs_is_measured` is now **false for every row**, including `REGISTER_DATA` |
| — | Range budgeting | Both endpoints preserved with the original register wording; upper endpoint governs capacity |

W-M2.2's commit is not rewritten and its fixture is not edited in a way that changes any
verbatim register text. The correction is a new commit on the same branch.

---

## 2. CORRECTION 1 — Exact dozen

### 2.1 The defect

`parse_npc_count()` refused `"A dozen people."` because `dozen` appeared in
`_VAGUE_WORDS`. That list conflated two different words:

| Word | Meaning | Correct handling |
|---|---|---|
| `a dozen` | **exactly 12** | parse as 12 |
| `dozens` | an indefinite plurality | refuse |

They differ by one letter and by whether the register has pinned the number down. The
W-M2.2 parser already derived `(12, 12)` in `parse_npc_band()`, so the two functions
disagreed about the same sentence — the band said twelve, the point estimate said
"unreadable". The TD's correction resolves the disagreement in favour of the register.

This was a **false negative of the same family** as the original `"six to ten" → 16`
error, pointing the other way: rather than inventing precision, it discarded precision
that was actually present, and thereby understated a scene the register pins down.

### 2.2 The fix

`dozen` is removed from `_VAGUE_WORDS`; `dozens` stays. A dedicated resolution step runs
*before* the refusal gates and handles the variants separately, because they are not all
twelve:

| Input | Point count | Band | Reasoning |
|---|---|---|---|
| `A dozen people.` | **12** | 12–12 | definite |
| `A dozen.` | **12** | 12–12 | definite |
| `Half a dozen women.` | **6** | 6–6 | explicit half |
| `Two dozen men.` | **24** | 24–24 | explicit multiplier |
| `A dozen or so.` | refused | none | an approximation, not a count |
| `Dozens of people.` | refused | none | indefinite |
| `Several dozen farmers.` | refused | none | indefinite |

A loose regex would have reported 12 for four of these and been wrong twice. The point
count and the band are asserted to agree on every one of these inputs by
`test_point_count_and_band_never_disagree`.

### 2.3 Corrected classification

The TD's four figures sum to **47**, not 46, so one of them cannot be right. The evidence:

| Class | TD stated | **Actual** | Difference |
|---|---|---|---|
| Exact register count | 29 | **29** ✓ | — |
| Bounded, not exact | 6 | **5** | −1 |
| Unbounded | 1 | **1** ✓ (`CH01-SCN-014`) | — |
| Uncaptured | 11 | **11** ✓ | — |
| **Total** | **47** | **46** ✓ | |

The arithmetic isolates the discrepancy to the bounded class. The bounded set is
`{CH01-SCN-005 (0–1), SCN-017 (6–10), SCN-020 (4–5), SCN-021 (0–1), SCN-034 (0–1)}` — five
scenes, each verified against its verbatim register wording. If `SCN-018` were still
counted as bounded the class would read 6, but then the exact class would read 28, which
contradicts the TD's own figure of 29. **Both of the TD's numbers cannot hold
simultaneously.** I have implemented 29 exact / 5 bounded / 1 unbounded / 11 uncaptured
= 46, and am flagging the discrepancy rather than adjusting a scene to fit.

### 2.4 Effect on the figures

`CH01-SCN-018` is **`SCRIPTED`** tier (`WORLD ACTIVITY SCENE`). A scripted scene costs a
flat **0.3** per scene regardless of how many people it depicts — it animates on a loop
with no AI, no perception and no navigation. **Resolving its count from "unreadable" to
12 therefore cannot move any cost figure.** This was verified rather than assumed:

| Field | Before | After | Moved |
|---|---|---|---|
| `total_cost_units` | 30.38 | 30.38 | no |
| `simulated_npcs_lower / upper` | 23 / 42 | 23 / 42 | no |
| `crowd_peak_estimate` | 22 | 22 | no |
| `band_cost_units_low / high` | 38.38 / 42.37 | 38.38 / 42.37 | no |
| `npcs_provenance_summary` | `{REGISTER_DATA: 28, UNPARSED: 7}` | `{REGISTER_DATA: 29, UNPARSED: 6}` | **yes** |

I am stating plainly that the recalculation was performed and produced no change, rather
than implying the numbers were re-derived and happened to land identically. A reader is
entitled to know which figures are load-bearing.

---

## 3. CORRECTION 2 — Measured provenance

### 3.1 The defect

```python
npcs_is_measured = (npcs_source == "register")   # WRONG
```

This conflated **provenance** with **measurement**. They answer different questions:

| Question | Field |
|---|---|
| Where did this number come from? | `npcs_provenance` = `REGISTER_DATA` |
| Was it observed in a running build? | `npcs_is_measured` = `False` |

A count authored in the register is **data transcribed from a design document**. It
records what the designer wrote, not what happens at runtime. No build has been executed,
no NPC has been spawned, and no frame has been profiled. Marking a register count as
"measured" would let a downstream consumer cite it as empirical evidence for a
performance claim — which is precisely the failure mode ADR-0005 exists to prevent.

### 3.2 The fix

```python
npcs_is_measured = False   # always; no engine has run
```

`npcs_provenance` is **unchanged**: the 29 register rows still read `REGISTER_DATA`. The
correction strips an overclaim without weakening traceability.

The field is deliberately not derived from `npcs_source` any more, because any derivation
reintroduces the same category error the moment a new source is added.

### 3.3 Enforcement

The previous L0 check *required* `REGISTER_DATA` to have `is_measured=True` — it enforced
the bug. It is now inverted and, importantly, **blind to provenance**: `REGISTER_DATA`
gets no exemption, because that exemption was the defect.

Three independent checks now cover it:

| Layer | Test | Catches |
|---|---|---|
| Scene records | `test_no_scene_claims_to_be_measured` | in-memory model |
| Generated JSON | `test_generated_json_carries_false_not_null` | serialisation (`null` ≠ `false`) |
| L0 gate | `test_gate_rejects_a_row_claiming_to_be_measured` | artifact tampering |
| Evidence run | `check_measurement_claims()` | pre-publication |

The evidence generator performs its **own** direct inspection of the artifact rather than
delegating to the gate. A run that only asserts "the gate passed" is evidence about the
gate, not about the data.

### 3.4 Proof the checks are not vacuous

Each was verified to fail when the condition it guards is broken:

| Injected fault | Result |
|---|---|
| `npcs_is_measured=True` on a `REGISTER_DATA` row, then L0 | **exit 1**, 13/14 |
| Same, then `gen_evidence.py` | **exit 1**, `measurement_claims` FAIL, `all_passed: False` |
| Gate check disabled in source, then the gate test | **test fails** (proving the test reads the gate's behaviour, not a constant) |
| Restore | **14/14**, `all passed: True`, exit 0 |

---

## 4. MODELLING DECISION — Range budgeting

The TD establishes the endpoint semantics. This is now encoded in the data, not only in
prose, so a consumer cannot misread one endpoint as the other.

| Rule | Implementation |
|---|---|
| Lower endpoint for lower scenarios | `cost_band[0]`, `band_cost_units_low` |
| Upper endpoint for conservative capacity planning | `cost_band[1]`, `band_cost_units_high` |
| Preserve both endpoints | Neither is collapsed; both are emitted per scene |
| Preserve the original register wording | `register_wording` on every band row |
| Never substitute a midpoint silently | `midpoint_used: false` per row; no midpoint exists anywhere in the code |
| Keep point estimate distinct from conservative capacity | Separate fields, separate labels, never summed |
| Do not describe cost units as measured runtime performance | Cost units are relative arithmetic; no ms, no frame time, no profiling |

Band rows now carry the verbatim source string, so a reader can check the endpoints
against the register without opening the fixture:

| Scene | Band | Register wording | Cost band |
|---|---|---|---|
| `CH01-SCN-005` | 0–1 | "Sometimes one cook." | 0.3–0.3 |
| `CH01-SCN-017` | 6–10 | "Six to ten adults; Unoka (storyteller) some days." | 5.0–8.0 |
| `CH01-SCN-020` | 4–5 | "Four or five men." | 3.0–4.0 |
| `CH01-SCN-021` | 0–1 | "Occasional passer-by." | 0.0–0.0 |
| `CH01-SCN-034` | 0–1 | "Sometimes a traveller." | 0.0–0.0 |

### 4.1 A consequence the rule forced

Applying the decision exposed an inconsistency in my own W-M2.2 work. The ceiling headroom
was computed from the **point** figure, which bills unresolved scenes at zero and is
therefore neither endpoint. Under the TD's rule, capacity must be planned around the upper
endpoint, so the headline headroom changes:

| Measure | W-M2.2 | W-M2.3 |
|---|---|---|
| Headroom (upper endpoint, capacity planning) | — | **11.63** |
| Headroom previously reported (point, understates) | 26.62 | 26.62 (retained, relabelled) |

**The W-M2.2 headroom of 26.62 overstated the margin by 15 units.** It was not a rounding
error; it was the wrong statistic for the stated purpose. Both are now reported, labelled,
with a basis string on each. The `ceiling` block also carries
`is_a_floor_not_a_ceiling: true`, because the band is open at `CH01-SCN-014` — so even
11.63 is a floor on the true cost, not a ceiling on it.

### 4.2 `CH01-SCN-014` remains unbounded

"A line of women and girls filling pots and lifting them onto head-pads, talking." No
numeral. No count has been invented, and the authoritative register has not been amended.
It is the single reason the band cannot close.

---

## 5. Recalculated results

| Metric | W-M2.2 | W-M2.3 | Note |
|---|---|---|---|
| Exact register counts | 28 | **29** | +`SCN-018` |
| Bounded, not exact | 7 | **5** | −`SCN-018`, −1 unexplained TD figure |
| Unbounded | 1 | **1** | `SCN-014` |
| Uncaptured | 11 | **11** | all SCRIPTED/NONE |
| Point cost | 30.38 | **30.38** | unchanged: `SCN-018` is flat-cost |
| Band (cost units) | 38.38–42.37 | **38.38–42.37** | unchanged |
| Band complete | no | **no** | `SCN-014` open |
| Simulated NPCs (lower/upper) | 23 / 42 | **23 / 42** | unchanged |
| Crowd peak | 22 | **22** | unchanged |
| `expected_npcs` elasticity | 0.000 | **0.000** | still dead by design |
| Pattern spread | 1.4× | **1.4×** | unchanged |
| Headroom (upper endpoint) | *not computed* | **11.63** | corrected basis |
| Headroom (point) | 26.62 | **26.62** | relabelled as understating |
| `npcs_is_measured=true` rows | 28 | **0** | correction 2 |

### 5.1 Scenarios

| Scenario | `expected_npcs` | ratio | Point | Band (capacity) |
|---|---|---|---|---|
| LOW-DENSITY | 1 | 0.50 | 24.38 | 29.38–32.38 |
| LOW-COUNT | 1 | 0.75 | 30.38 | 38.38–42.37 |
| **BASELINE** | 2 | 0.75 | **30.38** | **38.38–42.37** |
| HIGH-COUNT | 3 | 0.75 | 30.38 | 38.38–42.37 |
| HIGH-DENSITY | 4 | 1.00 | 33.38 | 43.37–48.37 |

LOW-COUNT and HIGH-COUNT remain identical to baseline. That is the W-M2.2 finding
unchanged: the ambient default is inert because every CROWD scene has register prose.

---

## 6. Previous reproduction still passes

The W-M2.1 world is reproduced from the preserved abridged fixture:

```bash
python3 Tools/world/sensitivity.py --previous --out /tmp/prev.json
```

```
LOW-DENSITY    point=23.38   band=23.38-23.38
LOW-COUNT      point=25.38   band=25.38-25.38
BASELINE       point=36.58   band=36.58-36.58
HIGH-COUNT     point=47.77   band=47.77-47.77
HIGH-DENSITY   point=58.97   band=58.97-58.97
HEADROOM (upper endpoint, capacity planning): 1.03 of 60.0
```

All five figures and the 1.03 headroom match W-M2.1 exactly. The abridged fixture is
still byte-for-byte identical, pinned by sha256 in the test suite.

---

## 7. Verification

Run from the repository root. All exit codes captured directly, not through a pipe.

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/canon/tests` | **114 tests OK** | **0** |
| `python3 -m unittest discover -s Tools/world/tests` | **231 tests OK** | **0** |
| `python3 Tools/ci/l0_checks.py` | **14/14 passed** | **0** |
| `python3 Tools/world/gen_evidence.py` | **10/10 checks, all passed** | **0** |
| `python3 Tools/world/sensitivity.py --previous` | W-M2.1 reproduced exactly | **0** |

### 7.1 Tamper proof

| Fault injected | Detection | Exit |
|---|---|---|
| `npcs_is_measured=True` on a REGISTER_DATA row → L0 | 13/14, scene named | **1** |
| Same → `gen_evidence.py` | `measurement_claims` FAIL | **1** |
| Gate check removed from source → gate test | test fails | n/a |
| Restore → both | 14/14, 10/10 | **0** |

---

## 8. What this does not establish

- **No measurement.** No engine, no build, no NPC spawned, no frame profiled. Every figure
  is projected arithmetic over authored data. `npcs_is_measured` is false for all 46 rows
  and that is the correct value.
- **Cost units are not milliseconds.** They are relative budget arithmetic with no runtime
  meaning. Any sentence that reads them as performance is wrong.
- **Chapter 1 only.** No extrapolation to Chapters 2–8, which are not ingested.
- **The band is open.** `CH01-SCN-014` states no number, so the true cost exceeds the upper
  endpoint by an unknown amount. 11.63 is a floor on the headroom, not a guarantee.
- **The TD's classification sums to 47.** Explained in §2.3; implemented as 46.

---

## 9. Open items

| Item | Needs | Owner |
|---|---|---|
| `CH01-SCN-014` unbounded | Directorate ruling: amend the register, or accept the open term | Creative Director |
| Bounded-class count (5 vs 6) | Confirmation of which figure is intended | Technical Director |
| `crowd_concurrency_ratio` (+0.55), `crowd_cost_unit` (+1.07) | A measurement, which needs an engine | Agent 2, blocked |
| 11 uncaptured scenes | No register prose exists; tier makes it moot for cost | — |
| Locations 13 of 57 | Separate capture pass | Agent 2 |
