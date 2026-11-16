# REGISTER INGESTION — SOURCES, PARSING, REGENERATION

**Document ID:** TDD-RINGEST-001
**Version:** 1.0.0
**Date:** 2026-11-16
**Author:** Agent 2 (world structure / level architecture)
**Status:** Current. Describes tools that have been run and tested, and limits that have been measured.

Honours Technical Directive TR-3: *keep the world mirror reproducible from the authoritative registers — document source versions, parsing assumptions, unsupported table formats, validation failures, and the regeneration procedure.*

---

## 1. Authority

Google Drive is authoritative. Everything in this repository under `Tools/canon/data/` and `Tools/world/data/` is a **mirror** derived from it.

```
Google Drive registers  ──(read, transcribe)──>  fixtures (.md in repo)
                                                        │
                                          ┌─────────────┴─────────────┐
                                          │  registers.py (parser)    │
                                          └─────────────┬─────────────┘
                                                        │
                        ┌───────────────┬───────────────┼───────────────┬──────────────┐
                        ▼               ▼               ▼               ▼              ▼
                 canon_index.json  world_manifest  population_budget  count_recon  L0 checks
```

No tool in the chain decides canon. `canon_index.py` reports drift; it does not resolve it. A disagreement between the mirror and Drive is always resolved in Drive's favour, by a human, and recorded as a register revision.

---

## 2. Source versions

| Register | Version | Drive file ID | Dated | What we use it for |
|---|---|---|---|---|
| `LOCATION_MASTER_REGISTER.md` | **2.9** | `1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5` | 2026-11-15 | Location entries, canon status, environment design status, access level, environment states, the published count table |
| `SCENE_AND_MICROLOCATION_MASTER_REGISTER.md` | **1.9** | `1EYQl5eMZx8PGElDSPHojKcEVWGvU2-UW` | — | Scene entries, parent locations, categories, access, NPC prose |
| `CHARACTER_DESIGN_REGISTER` | — | `1naNn0D7jAXOVc01Xvnl4YYEvS_zwcTjH` | — | Character canon (not consumed by world tools) |
| `ENVIRONMENT_DESIGN_REGISTER` | — | `1WxQeJ7Hnac4gUnOR9EF156ClSTZebpsx` | — | Board status (not consumed by world tools) |
| `OPEN_ART_DECISIONS` | — | `1c6SaYn1U2JLX0wu6sg-fpvPX5T1LAb0Q` | — | Design-status semantics (OAD-48) |
| `NNEKA_MEMORIES` | — | `1CzvUvsYgFOX5FAbha0lGs4Fj0NKnexgq` | — | Memory 1 verified; memories 2–7 unverified |

**A version bump in either** of the first two **invalidates every derived number in this repo** until re-ingested. `Tools/world/count_reconciliation.py` will fail loudly if the published totals stop summing to the per-chapter rows.

---

## 3. Ingestion status — what is actually captured

| Chapter | Locations | Scenes | State refs | Status |
|---|---|---|---|---|
| CH01 | **partial** (13 of 57 location entries) | **complete** (46/46) | 2 of 14 | Usable for scene-derived work. Location-derived work is partial. |
| CH02–CH08 | none | none | none | **NOT INGESTED.** Only their published counts are transcribed, for arithmetic checks. |

This is the single most important caveat in this document. Anything computed per-location for Chapters 2–8 would currently be fabricated. Do not do it.

Fixtures:

- `Tools/canon/tests/fixtures/location_register_ch01_excerpt.md` — 13 location rows + hierarchy excerpt
- `Tools/canon/tests/fixtures/scene_register_ch01_full.md` — 46 scene rows + 5 verbatim detail blocks
- `Tools/world/data/register_counts.json` — the register's published count table, transcribed verbatim

The scene register is fully captured because the population budget depends on the NPC prose, which only appears in the detail blocks. Five detail blocks were captured; the other 41 scenes are budgeted from **policy defaults**, and the budget says so per scene (`npcs_source: "policy_default"`).

---

## 4. Parsing assumptions

These are the format assumptions `Tools/canon/registers.py` makes. Each was verified against the fixtures and, where noted, against deliberately malformed input.

### 4.1 Summary tables

| Assumption | Consequence if violated |
|---|---|
| A table starts at a header row containing a recognisable ID column (`Scene ID`, `Location ID`) | Table silently skipped, **0 rows parsed** |
| A separator row (`\|---\|---\|`) follows the header | Table silently skipped, **0 rows parsed** |
| Rows begin `\|` and end `\|` | Row dropped |
| Cells contain no escaped `\|` | Cell boundaries shift; wrong values |
| Column names match exactly (case-sensitive) | Header not recognised; **0 rows parsed** |
| Extra columns are tolerated | — |
| Too few columns yields empty fields, not an error | Downstream validation must catch it |

Verified failure modes (all silent, all return 0 rows rather than raising):

```
missing separator row       -> 0 rows
missing trailing pipe       -> 0 rows
missing leading pipe        -> 0 rows
header renamed "Scene ID"->"ID" -> 0 rows
header case changed          -> 0 rows
```

**This is the main hazard in the pipeline:** a format change produces an empty result, not an exception. Every consumer therefore asserts an expected row count. `count_reconciliation.py` fails Chapter 1 if it parses anything other than 46 scenes.

### 4.2 Detail blocks

Each scene/location detail block is `### <ID> · <Name>` followed by a `| Field | Value |` table and then bulleted fields (`- **Field.** value`).

| Assumption | Consequence if violated |
|---|---|
| The `\| Field \| Value \|` table **terminates at the first blank line** | Every bulleted field below it is silently dropped |
| Bulleted fields use `- **Label.** value` | Field not mapped; silently ignored |
| Labels match `_FIELD_MAP` exactly | Field silently ignored |
| Emphasis (`**`, backticks) wraps values only | Stripped by `_strip_emphasis` |

The blank-line table terminator was a **real bug in this repository**. The original parser only treated `**` or `- **` as terminators, so the blank line between the table and the bullets left the parser in table mode, and it dropped all five detail blocks' bulleted fields (0 of 5 parsed). It is now fixed and regression-tested.

### 4.3 The `·` separator

Headings use U+00B7 MIDDLE DOT. Writing fixtures through a shell heredoc mangles it. **Fixtures containing `·` must be written with `write_file` or Python, never a shell heredoc.** This already corrupted one fixture attempt.

### 4.4 NPC prose

`parse_npc_count()` returns `(people, has_child, parsed)`. It is word-list arithmetic, not language understanding.

Verified behaviour:

| Register prose | Result | Note |
|---|---|---|
| `None.` / `No one.` / `Nobody` / `Empty` | `(0, False, True)` | Stated absence is a successful parse of a real answer |
| `One boy` | `(1, True, True)` | |
| `One woman, one child.` | `(2, True, True)` | |
| `Three men and two women` | `(5, False, True)` | |
| `A family of six.` | `(6, False, True)` | Collective noun; article adds nobody |
| `Two old men, a girl, and a dog` | `(3, True, True)` | Article-introduced person counted; animal excluded |
| `Two goats` | `(0, False, True)` | Animals are ambience, not performers |
| `One woman, two goats and a child` | `(2, True, True)` | |
| `twelve dancers` | `(12, False, True)` | |
| `A crowd` | `(0, False, False)` | **UNPARSEABLE — flag, never budget zero** |
| `A gathering of unspecified size.` | `(0, False, False)` | **UNPARSEABLE — flag** |

Two bugs were found and fixed here, both of which would have corrupted later chapters:

1. `No one.` parsed as **1**, because `one` was matched as a numeral before the absence check ran.
2. `Two old men, a girl, and a dog` parsed as **2**, because a person introduced by an article rather than a numeral was never counted.

`parsed=False` is the contract that prevents the remaining class of error. `parse_npc_count` cannot resolve `several`, `a crowd`, `many`, or `a score`. When it cannot resolve the text it says so, and `population_budget.validate_budget` **fails** on any scene containing an unparsed description rather than letting a zero pass as data.

Known limitation: the person-noun and animal lists are finite. A register using a noun not on the list (say, `tapper` or `hawker`) with an article instead of a numeral will undercount. This is caught only if the count lands at zero; between 1 and 10 it will not be caught. Treat budgeted NPC numbers as **estimates requiring human review**, which is how every derived figure in this milestone is labelled.

---

## 5. Validation failures and what each means

| Check | Input | Expected | Failure means |
|---|---|---|---|
| `validate_scenes()` | parsed scene rows | 0 problems | Parent references a non-existent location; duplicate ID; unknown category |
| `validate_scene_details()` | parsed detail blocks | 0 problems | Missing `NPCs present`; unknown canon status or scene category |
| `count_reconciliation.check_published_consistency()` | count table | 0 problems | **Register contradicts itself** — escalate to the register owner, do not "fix" the mirror |
| `count_reconciliation.check_derived_totals()` | count table | 0 problems | Derived arithmetic wrong, or subset column exceeds its parent |

A **partial capture is not a validation failure.** Chapter 1 parses 13 of 57 location entries by design. The reconciliation labels the shortfall `INGESTION GAP` and passes. It reserves `REGISTER OR PARSER INCONSISTENCY` for the case where the supposedly complete scene capture disagrees with the register.

---

## 6. Unsupported formats

Explicitly **not** handled. Each will fail silently or wrongly, so do not feed them in:

- Tables without a leading and trailing pipe on every row
- Tables without a separator row
- Column-order changes within a recognised header (fields are read positionally by header name; a reordered header is fine, a renamed header is not)
- Escaped pipes (`\|`) inside cells
- Cells containing newlines
- HTML tables, or markdown tables pasted from a rich-text editor with non-ASCII vertical bars (`│`, `¦`)
- Google Docs native tables pasted without conversion to markdown
- Numbered-word quantities below `one` or above `twelve` (see §4.4)
- Duplicate-ID detection across *different* chapters (each chapter is validated independently)
- Retired IDs — the register keeps retired IDs and never reuses them; the parser has no concept of a retired ID and will happily parse one as active. `canon_index.json` has no retired-ID list. **Outstanding issue.**

---

## 7. Regeneration procedure

Run from the repository root. All commands are tested.

```bash
# 1. Regenerate the canon mirror from the fixtures.
#    Writes Tools/canon/data/canon_index.json.
python3 Tools/canon/gen_world_data.py

# 2. VALIDATE the Chapter 1 world manifest against the canon mirror.
#    This tool does not generate the manifest - the manifest is authored
#    (a hand-made vertical-slice slice), and this checks every id in it
#    resolves to a real location and every status agrees with the mirror.
python3 Tools/world/world_manifest.py Tools/world/data/CH01_manifest.json

# 3. Regenerate the population budget and its evidence artifact.
python3 Tools/world/population_budget.py --chapter CH01 \
        --out Docs/evidence/agent2/CH01_population_budget.json

# 4. Reconcile the register's published counts.
python3 Tools/world/count_reconciliation.py \
        --out Docs/evidence/agent2/CH01_count_reconciliation.json

# 5. Run the full test suite.
python3 -m unittest discover -s Tools/canon/tests
python3 -m unittest discover -s Tools/world/tests

# 6. Run the L0 gate (includes mirror-drift detection).
python3 Tools/ci/l0_checks.py
```

Expected current state:

```
canon:  114 tests OK
world:   85 tests OK
L0:     10/10 passed
manifest: 6 locations, 2 scenes, 0 violations
reconciliation: RESULT PASS, location entries 196, CH01 46/46 scenes, 45 non-story
population budget: 46 scenes, 29-48 simulated NPCs, 35.58 cost units, validation PASS
```

### 7.1 What must never be regenerated by hand

- Do **not** hand-edit `Tools/canon/data/canon_index.json`. `l0_checks.check_canon_mirror_drift` compares it against a fresh parse and fails on any difference. Drift detection was proved by injecting `CH01-SUB-018 → ESTABLISHED`; the gate failed as designed.
- Do **not** edit `register_counts.json` to make an assertion pass. If the register changes, update `register_version` and re-derive.

### 7.2 Adding a chapter

1. Create `Tools/canon/tests/fixtures/location_register_chNN_excerpt.md` and `scene_register_chNN_full.md` from Drive.
2. Confirm the parsed counts equal that chapter's row in `register_counts.json`. If they do not, stop — the capture is wrong or the format changed.
3. Only then extend `gen_world_data.py` and `world_manifest.py` to the new chapter.
4. Add the chapter to `REGISTER_PUBLISHED` if the count table has been re-read.

---

## 8. Outstanding issues

| # | Issue | Severity | Owner |
|---|---|---|---|
| R-01 | Only Chapter 1 captured. Chapters 2–8 unparsed. | High — blocks per-chapter work | Agent 2, per chapter |
| R-02 | 41 of 46 Chapter 1 scenes have no captured detail block, so their NPC counts are policy defaults, not register data. | Medium — budget is an estimate | Agent 2 |
| R-03 | No retired-ID tracking; a retired ID would parse as active. | Medium — canon hygiene | Agent 2 + register owner |
| R-04 | Word-list NPC parsing undercounts nouns outside its lists (§4.4). | Medium — understates budget | Agent 2 |
| R-05 | Format changes fail silently with 0 rows rather than raising. Consumers assert expected counts, but a new consumer could miss it. | Medium — tooling | Agent 2 |
| R-06 | No automated re-read from Drive. Fixtures are refreshed by hand, so the mirror can be stale without any signal. | High — staleness | Agent 2 + TD decision on a Drive sync job |

R-06 is the one that matters most. Every number in this repository is only as current as the fixture date. There is no mechanism that notices when Drive changes.

---

## 9. Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-11-16 | First issue. Documents CH01 ingestion, the six silent-failure modes measured against the parser, two fixed NPC-parsing bugs, the blank-line table-terminator bug, and the regeneration procedure. |
