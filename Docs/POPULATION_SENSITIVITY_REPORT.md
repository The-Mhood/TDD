# POPULATION BUDGET — SENSITIVITY REPORT

**Document:** TDD-WSENS-001 · **Version:** 2.0 · **Date:** 2026-11-16
**Author:** Agent 2 — World, Systems and Gameplay Simulation
**Status:** `PROVISIONAL` — sensitivity of a **derived estimate**, not a measurement.
**Scope:** Chapter 1 only. Does **not** extrapolate to Chapters 2–8.
**Evidence:** `Docs/evidence/agent2/CH01_population_sensitivity.json` (generated, not hand-written)

---

## 1. What changed in this revision

Version 1.0 of this report described a world in which **5 of 46** Chapter 1 scenes had
register NPC prose. The remaining 41 rested on policy defaults, and the ambient
`expected_npcs` parameter alone drove the estimate.

That is no longer true. This revision reports a capture of the register's ambient-scene
detail blocks: **35 of 46 Chapter 1 scenes now have verbatim `NPCs present` prose.**

The earlier figures are not withdrawn. They are **reproduced exactly** from a preserved
abridged fixture with `Tools/world/sensitivity.py --previous`, so both the old and new
models remain auditable side by side. The old fixture was not edited; a superseding
capture was written to a new file, because editing it in place would have made the
previous milestone's published numbers unreproducible.

---

## 2. Facts

Values read from the register. Every row traces to a scene id.

| Metric | Value |
|---|---|
| Chapter 1 scenes | 46 |
| Scenes with verbatim NPC prose | **35** (76% of the chapter) |
| — reducing to an exact head-count | 29 |
| — stating a range, alternative or condition | 6 |
| Scenes with no captured prose | 11 |
| Location entries captured | 13 of 57 (**partial**) |

**Point coverage is 63% (29 of 46). Prose coverage is 76% (35 of 46).** The difference
is deliberate and is explained in §3.

The 7 unresolved scenes are not parser failures. The register genuinely does not state a
number for them:

| Scene | Register wording | Bound derived |
|---|---|---|
| `CH01-SCN-017` | "Six to ten adults" | 6–10 |
| `CH01-SCN-018` | "A dozen" | 12–12 |
| `CH01-SCN-020` | "Four or five men" | 4–5 |
| `CH01-SCN-005` | conditional, singular person | 0–1 |
| `CH01-SCN-021` | conditional, singular person | 0–1 |
| `CH01-SCN-034` | conditional, singular person | 0–1 |
| `CH01-SCN-014` | "a line of women and girls" | **none — OPEN** |

A parser that turns "six to ten" into `16`, or "family of eight across three generations"
into `11`, is not being helpful; it is fabricating. A previous revision of this tool did
exactly that. Both are now regression-tested.

---

## 3. Why the point figure and the band are different claims

The **point** figure (30.38 cost units) bills every scene whose count it cannot reduce to
one integer as **zero**. That understates, and it is not the number to quote as a floor.

The **band** (38.38–42.37) replaces those zeros with the bounds the register itself
states, and is the honest floor for the chapter. It remains **OPEN** because
`CH01-SCN-014` "Fetching Water" names a collective with no numeral at all — nothing
bounds it — so even the upper figure is a *lower* bound on the true cost.

| Measure | Value | Meaning |
|---|---|---|
| Point cost | 30.38 | What the flat model bills; **understates** |
| Band low | 38.38 | Zeros replaced by register-stated lower bounds |
| Band high | 42.37 | Register-stated upper bounds; **still a floor** |
| Band complete | **no** | `CH01-SCN-014` is unbounded |

---

## 4. Assumptions

The policy file, not the register. These have no register basis.

| Parameter | Baseline | Why it matters |
|---|---|---|
| `crowd_concurrency_ratio` | 0.75 | Multiplies every CROWD scene's head-count |
| `crowd_cost_unit` | 1.0 | Price of a simulated crowd actor |
| `expected_npcs_for_ambient` | 2 | **Now inert — see §5** |
| access multipliers | 1.0 / 0.6 / 0.2 / 0.05 | Per-scene discount by reachability |

Cost units are **relative budget arithmetic, not milliseconds.** No simulation has run.

---

## 5. The headline result: the ambient default is dead

`expected_npcs_for_ambient` was the dominant assumption in v1.0, with an elasticity of
**+0.88**. It is now **0.000**.

That is not a bug and it is not a coincidence. Only a `CROWD` scene is priced per NPC;
`SCRIPTED` is a flat per-scene cost and `NONE` is zero. **All 14 CROWD scenes now have
register prose**, so no CROWD scene consults the default any more. Sweeping the parameter
across 1–5 produces a completely flat line, by construction.

The 11 remaining uncaptured scenes are all `SCRIPTED` or `NONE` tier. Varying a count on
any of them was measured to add **+0.00**. They carry *provenance debt* — the budget
cannot say where their count came from — but **no numeric exposure**.

| Parameter | Elasticity, v1.0 | Elasticity, now |
|---|---|---|
| `expected_npcs_for_ambient` | **+0.88** | **0.00** |
| `crowd_concurrency_ratio` | +0.55 | +0.55 |
| `crowd_cost_unit` | +1.07 | +1.07 |
| `expected_npcs_for_scripted` | 0.00 | 0.00 |

What still moves the total is the **concurrency ratio** and the **cost unit** — both pure
assumptions with no register basis, and both unaddressed by this capture. The estimate is
not assumption-free; it is assumption-scoped differently.

---

## 6. Scenarios

Four policy parameters swept from pessimistic to permissive.

| Scenario | `expected_npcs` | ratio | Cost | Simulated NPCs | vs baseline |
|---|---|---|---|---|---|
| LOW-DENSITY | 1 | 0.50 | 24.38 | 36 | −20% |
| LOW-COUNT | 1 | 0.75 | 30.38 | 42 | +0% |
| **BASELINE** | **2** | **0.75** | **30.38** | **42** | — |
| HIGH-COUNT | 3 | 0.75 | 30.38 | 42 | +0% |
| HIGH-DENSITY | 4 | 1.00 | 33.38 | 45 | +10% |

**LOW-COUNT and HIGH-COUNT are identical to baseline.** That is §5 restated as a table:
the ambient count no longer does anything. A reader who expects those rows to differ is
reading the old model.

| Metric | v1.0 | Now |
|---|---|---|
| Baseline cost | 36.58 | **30.38** |
| Baseline simulated NPCs | 49 | **42** |
| Crowd peak | 29 | **22** |
| Scenario spread | 2.5× | **1.4×** |
| Worst case | 58.97 | **33.38** |
| Headroom below the 60-unit ceiling (upper endpoint) | 1.03 | **11.63** |
| — point-estimate headroom (understates) | — | 26.62 |
| Share of cost on policy-default scenes | 75% | **4.6%** |

Under the TD's range-budgeting rule, capacity is planned around the **upper** endpoint,
not the point figure. On that basis the worst scenario leaves **11.63** units of headroom,
not 26.62. The 26.62 figure is the point estimate, which bills unresolved scenes at zero
and therefore overstates headroom; it is retained only for continuity with v1.0.

The v1.0 worst case sat 1.03 units below the ceiling, which was the finding that
justified the capture. The margin is now larger, but it is still a floor: the band is
open at `CH01-SCN-014`.

---

## 7. What this does not establish

- **No simulation has run.** Cost units are relative arithmetic.
- **Chapter 1 only.** Chapters 2–8 are not ingested; any per-chapter figure for them
  would be fabricated.
- **Locations are 13 of 57.** This report says nothing about the other 44 entries.
- **The band is open.** `CH01-SCN-014` states no number, so the true cost is above the
  upper band figure, by an unknown amount.
- **The capture is of one register version.** v1.9. A register revision invalidates it,
  and nothing currently detects that automatically.

---

## 8. Recommendation

The capture removed the assumption that dominated the estimate. The remaining large
assumptions are `crowd_concurrency_ratio` and `crowd_cost_unit`, and **neither can be
resolved by reading a register** — they are engineering parameters that need a
measurement, which requires an engine. That is the honest blocker.

`CH01-SCN-014` needs a **directorate ruling**, not more parsing: either the register is
amended to state a number, or the project accepts an unbounded term in the chapter
budget and says so wherever the figure is quoted.

---

## Reproducing this report

```bash
python3 Tools/world/sensitivity.py \
    --out Docs/evidence/agent2/CH01_population_sensitivity.json

# the previous milestone, reproduced exactly from the preserved fixture
python3 Tools/world/sensitivity.py --previous
```
