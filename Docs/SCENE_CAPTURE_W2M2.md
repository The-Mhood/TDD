# W-M2.2 — AMBIENT SCENE DATA CAPTURE

**Document:** TDD-WCAP-001 · **Version:** 1.0 · **Date:** 2026-11-16
**Author:** Agent 2 — World, Systems and Gameplay Simulation
**Status:** `PROVISIONAL` — capture record. The figures produced from it are projected,
not measured.
**Trigger:** TD instruction *"AMBIENT SCENE DATA CAPTURE"* — capture the uncaptured
Chapter 1 ambient-scene detail blocks and **replace policy assumptions with register
data**.

---

## 1. What was asked

The Chapter 1 population budget rested on a policy assumption for most of its scenes.
The register contains the real values, but only five detail blocks had ever been read
into a fixture. The instruction was to go and get the rest, rather than continue
reasoning about how sensitive the estimate might be to a guess.

Secondary requirement, stated explicitly: **do not destroy the previous milestone's
reproducibility to do it.**

---

## 2. Source

| Field | Value |
|---|---|
| Register | `SCENE_AND_MICROLOCATION_MASTER_REGISTER.md` |
| Version | **v1.9** (2026-11-15) |
| Drive file id | `1EYQl5eMZx8PGElDSPHojKcEVWGvU2-UW` |
| Read on | 2026-11-16 |
| Field captured | `NPCs present` only |
| Blocks captured | **35 of 46** Chapter 1 scenes |

**Extraction method.** The Drive text extractor truncates structurally: it keeps a fixed
head of roughly 11k characters and a trailing window whose position advances as
`max_chars` increases, dropping everything between. The register's tail was therefore
walked in successive windows and each `NPCs present` string read directly from the
rendered text. No content search or download API was available; this is a limitation of
the tool, recorded here so a future reader does not assume a clean bulk export.

The harvest record, including every verbatim string and the windows it came from, is
kept at `Tools/world/data/_harvest_progress.json`.

---

## 3. The divergence that forced a new file

The existing fixture `scene_register_ch01_full.md` is **not verbatim.** Its detail blocks
were abridged when first transcribed:

| Scene | Abridged fixture says | Register actually says |
|---|---|---|
| `CH01-SCN-017` | "Three adults." | "Six to ten adults; Unoka (storyteller) some days." |

This is not cosmetic. "Three adults" is a point value; "six to ten" is a range. Reading
the abridged text would have produced a confident integer that the register never states
— the exact failure mode the capture was meant to eliminate.

### 3.1 What was done about it

`scene_register_ch01_full.md` is **preserved unchanged**, byte for byte. Git shows an
empty diff for it, and a test asserts the file still hashes to its committed content.

A new file carries the capture:

```
Tools/canon/tests/fixtures/scene_register_ch01_v19_verbatim.md
```

The alternative — editing the old fixture in place — was rejected because it would have
made W-M2.1's published figures (36.58 cost units, 30/49 NPCs, peak 29, headroom 1.03)
unreproducible, and "the numbers changed and we can't show you the old ones" is not an
acceptable answer to a directorate that already reviewed them.

`sensitivity.py --previous` recomputes the old world from the old fixture and reproduces
**23.38 / 25.38 / 36.58 / 47.77 / 58.97 with headroom 1.03 — exactly.** This is checked
in the test suite, so the reproduction is a standing guarantee, not a claim.

---

## 4. What the capture found

Of the 35 verbatim blocks, **28 reduce to an exact head-count** and **7 do not.**

The 7 are not parser failures. The register genuinely states a range, an alternative, or
a condition:

| Scene | Verbatim register wording | Bound |
|---|---|---|
| `CH01-SCN-005` | "Sometimes one cook." | 0–1 |
| `CH01-SCN-017` | "Six to ten adults; Unoka (storyteller) some days." | 6–10 |
| `CH01-SCN-018` | "A dozen people." | 12–12 |
| `CH01-SCN-020` | "Four or five men." | 4–5 |
| `CH01-SCN-021` | "Occasional passer-by." | 0–1 |
| `CH01-SCN-034` | "Sometimes a traveller." | 0–1 |
| `CH01-SCN-014` | "A line of women and girls filling pots and lifting them onto head-pads, talking." | **none — OPEN** |

The remaining **11 scenes have no captured prose.** They are marked UNCAPTURED and
budgeted from a policy default. They are never treated as zero.

---

## 5. Refusing to invent a number

Two parser bugs were found and fixed during the capture. Both had been silently
producing confident wrong answers:

| Input | Old (fabricated) | Now |
|---|---|---|
| "Six to ten adults…" | `16` (numbers summed) | UNPARSED, band 6–10 |
| "Family of eight across three generations." | `11` (8 + 3) | `8` |

The rule is now: **each number binds to the noun it governs.** A number attached to a
person or a collective of people is a head-count; a number attached to an animal or an
abstract quantity is not. `Name (role)` counts as one. Ranges, alternatives, conditions
and unbindable multiples are **refused**, and carry the reason.

Refusing is the correct behaviour. A budget that says "we cannot read this" is usable by
a reviewer. A budget that says "16" when the register says "six to ten" is not, because
nothing downstream can tell it was invented.

The first attempt at the fix refused whenever a string contained more than one number,
which was also wrong — "Four or five men" has two numbers and describes five people at
most, not two. The classification is per-number, by noun, not global.

---

## 6. Result

| Metric | Before (W-M2.1) | After (W-M2.2) |
|---|---|---|
| Scenes with exact register count | 5 | **28** |
| Scenes with register prose, unresolved to an integer | 0 | **7** |
| Scenes uncaptured | 41 | **11** |
| Baseline cost units (point) | 36.58 | **30.38** |
| Simulated NPCs | 49 | **42** |
| Crowd peak | 29 | **22** |
| Scenario spread | 2.5× | **1.4×** |
| Worst-case headroom below the 60-unit ceiling | 1.03 | **26.62** |
| Share of cost on policy-default scenes | 75% | **4.6%** |
| Elasticity of `expected_npcs_for_ambient` | **+0.88** | **0.00** |

### 6.1 The headline

**The ambient NPC default is now a dead parameter.** Elasticity fell from +0.88 to
exactly 0.000. This is not a coincidence and must not be "fixed": only a `CROWD` scene is
priced per NPC, and **all 14 CROWD scenes now have register prose.** No CROWD scene
consults the default, so sweeping it produces a flat line by construction.

The 11 remaining uncaptured scenes are all `SCRIPTED` or `NONE` tier. Varying their count
was measured to add **+0.00**. They carry **provenance debt** — the budget cannot say
where their count came from — but **no numeric exposure**.

### 6.2 What still moves the number

`crowd_concurrency_ratio` (+0.55) and `crowd_cost_unit` (+1.07). Both are engineering
parameters with no register basis. **Neither can be resolved by reading a register**, and
that is the honest blocker: they need a measurement, which needs an engine.

The estimate is not assumption-free. It is assumption-scoped differently, and the report
says so.

---

## 7. Honesty constraints honoured

- The **point** figure (30.38) is never quoted as a floor. It bills unresolved scenes at
  zero and therefore understates.
- The **band** (38.38–42.37) carries the register's own stated bounds and is the honest
  floor — but it is **OPEN** at `CH01-SCN-014`, so even the upper figure is a lower bound
  on the true cost.
- `band_is_complete=False` is surfaced wherever the band is printed, including in the
  report's "what this does not establish" section.
- No figure is described as measured. Every artifact states `PROVISIONAL`.

---

## 8. Verification

| Check | Result |
|---|---|
| Canon tests | **114 OK** |
| World tests | **215 OK** (incl. `test_scene_capture.py`, 36 cases) |
| L0 gate | **14/14 passed** |
| Evidence run | **9/9 checks pass** |
| Abridged fixture untouched | `git diff` empty; hash pinned by test |
| W-M2.1 reproduction | `--previous` → 23.38 / 25.38 / 36.58 / 47.77 / 58.97, headroom 1.03 |

### 8.1 Tamper proof

The provenance gate was proved to fail, not assumed to:

| Injected fault | Gate result |
|---|---|
| Promote a `POLICY_DEFAULT` scene to `REGISTER_DATA` without giving it prose | **exit 1** |
| Give an `UNPARSED` scene a fabricated integer and strip its basis | **exit 1** |
| Restore the artifact | **14/14, exit 0** |

The gate re-derives provenance from the fixture rather than trusting the artifact's own
flags, because an artifact validated against its own self-reported fields can never fail.
That principle was established after an earlier version of this gate was found to be
vacuous.

---

## 9. Unresolved, and what is needed

| Item | Needs | Owner |
|---|---|---|
| `CH01-SCN-014` "Fetching Water" states a collective with no numeral | Directorate ruling: amend the register, or accept an unbounded term and say so wherever the figure is quoted | Creative Director |
| 7 scenes state bounds, not counts | A ruling on **how a range is budgeted** — a modelling decision, not a parsing one | Agent 2 + TD |
| 11 scenes remain uncaptured | Register prose does not exist for them; their tier makes it moot for cost | — |
| Locations still 13 of 57 | A separate capture pass | Agent 2 |
| Chapters 2–8 not ingested | A separate capture pass | Agent 2 |

---

## 10. Files

| Path | Role |
|---|---|
| `Tools/canon/tests/fixtures/scene_register_ch01_v19_verbatim.md` | **new** — the capture, 35 verbatim blocks |
| `Tools/canon/tests/fixtures/scene_register_ch01_full.md` | **preserved unchanged** — W-M2.1 reproduction basis |
| `Tools/world/data/_harvest_progress.json` | raw harvest record: every string, source id, method |
| `Tools/canon/registers.py` | `parse_npc_count()` fixed; `parse_npc_band()` added |
| `Tools/world/population_budget.py` | band model, fixture selection, warnings |
| `Tools/world/sensitivity.py` | capture-aware report, `--previous` |
| `Tools/world/tests/test_scene_capture.py` | **new** — 36 tests |
| `Docs/POPULATION_SENSITIVITY_REPORT.md` | rewritten against the new artifact |
| `Docs/evidence/agent2/CH01_population_{budget,sensitivity}.json` | regenerated |
| `Docs/evidence/agent2/W-M2.2_evidence.json` | **new** — evidence run |
