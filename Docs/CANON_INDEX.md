# CANON INDEX — engineering mirror of the Art Bible registers

**Document:** TDD-CANON-001 · **Version:** 2.0.0 · **Date:** 2026-11-16
**Revision 2.0.0:** corrects the canon model after reading `LOCATION_MASTER_REGISTER.md` v2.9 in full excerpt.
See §7 for what v1.0.0 got wrong.

## 1. What this is, and what it is not

`Tools/canon/data/canon_index.json` is a **machine-readable mirror of a subset** of the Google Drive Production
Art Bible. It exists so that engineering can:

1. validate that IDs used in code and data are canonical (ADR-0006),
2. enforce canon *rules* as automated tests rather than art-team discipline,
3. generate engine data (memory table, world inventory) instead of retyping 812 KB of registers,
4. detect when a register changes underneath the project.

**It is not canon.** The Drive registers are authoritative:

| Register | Drive ID | Version | Authority |
|---|---|---|---|
| `CHARACTER_DESIGN_REGISTER.md` | `1naNn0D7jAXOVc01Xvnl4YYEvS_zwcTjH` | 2026-11-15 | visual + identity canon |
| `ENVIRONMENT_DESIGN_REGISTER.md` | `1WxQeJ7Hnac4gUnOR9EF156ClSTZebpsx` | V002 | environment design + per-chapter rules |
| `OPEN_ART_DECISIONS.md` | `1c6SaYn1U2JLX0wu6sg-fpvPX5T1LAb0Q` | through OAD-59 | art + canon decisions |
| `NNEKA_MEMORIES_AND_TIMELINE.md` | `1CzvUvsYgFOX5FAbha0lGs4Fj0NKnexgq` | 1.2 | memory sequence, timeline |
| **`LOCATION_MASTER_REGISTER.md`** | `1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5` | **2.9** | location identity, canon status, design status, access levels |
| **`SCENE_AND_MICROLOCATION_MASTER_REGISTER.md`** | `1EYQl5eMZx8PGElDSPHojKcEVWGvU2-UW` | **1.9** | scene identity, parent location, scene category, access |

If this mirror and a register disagree, **the register wins and the mirror is wrong.**

## 2. The two independent status axes (OAD-48)

This is the rule most likely to be violated under production pressure, so it is enforced in code.

### Canon status — exactly three values

| Value | Meaning | Engineering may |
|---|---|---|
| `ESTABLISHED` | Confirmed by the Creative Director. The eight chapters, the eight boss encounters, the forest entry, the great tree, and the 19 home settlement subjects. | Build canon-bearing content |
| `PROPOSED` | An art director proposal with no story claim | Build greybox; gameplay only as `blockout` |
| `PENDING APPROVAL` | A proposal that also implies story, belief or cultural practice | Greybox only, and **only with Creative Director approval** (CD-5) |

`UNVERIFIED` is an **engineering-only** marker meaning "not yet read from the register". It is not a canon
status and **cannot be presented as one**; the validator enforces this.

### Environment design status — seven values, a separate axis

`NOT STARTED` · `EXPLORATORY` · `IN REVIEW` · `REQUIRES REVISION` · `CONDITIONAL` · `APPROVED` · `REJECTED`

**Approving a design establishes no story fact.** The registers say so explicitly, and OAD-47/48 confirmed it.
Chapter 8's `Sealed Quarter`, `Nneka's House` (exterior and interior) and `Hall of Posts` are design-approved
but not canon.

## 3. ID scheme (verified against the registers)

```
CHxx                        chapter 01..08
CHxx-ENV-001                major environment      (one per chapter)
CHxx-SUB-nnn                sub-location
CHxx-SET-nnn                settlement
CHxx-INT-nnn                interior
CHxx-LMK-nnn                landmark
CHxx-TRV-nnn                traversal area
CHxx-EXP-nnn                exploration area
CHxx-BOS-nnn                boss arena
CHxx-SCN-nnn                scene or micro-location
```

**Corrections from v1.0.0:**
- Boss arenas are `BOS`, **not** `BOSS`. `CH01-BOSS-GreatRootMother` was wrong; the register's
  `CH01-BOS-001 Great Root Mother Arena` is right.
- `ENV`, `SET`, `LMK`, `TRV`, `EXP` were missing entirely.
- `SUB`/`INT`/`SCN` were correct.

**IDs are permanent.** Retired IDs stay in the register and are never reused.

## 4. World scale (from the registers)

| Quantity | Count |
|---|---|
| Major environments | 8 |
| Other locations | 142 |
| Interiors (location entries) | 46 |
| Scenes and micro-locations | 135 |
| Environment-state references | 40 |

Per-chapter scenes: CH01 **46**, CH02 11, CH03 12, CH04 12, CH05 11, CH06 10, CH07 15, CH08 18.

**Only 4 main story scenes and 9 secondary story scenes exist in the entire game.** The overwhelming majority
of the world is ambient life, exploration and atmosphere. This directly sizes the quest system: it is small by
design, and building a large quest network would be inventing content the game does not have.

## 5. How it is validated

```bash
python3 -m unittest discover -s Tools/canon/tests    # 101 tests
python3 -m unittest discover -s Tools/world/tests    #  33 tests
python3 Tools/ci/l0_checks.py                        #  10 checks
```

Fourteen validator groups, including:

| Validator | Checks |
|---|---|
| Structure + schema | Required keys; hand-rolled JSON-Schema subset; schema uses only supported keywords so no constraint is silently skipped; booleans rejected where integers are expected |
| Status axes | Closed vocabularies for both axes; the two axes are disjoint; `UNVERIFIED` consistent with `verified_against_register` |
| Chapters + bosses | 8 chapters; one boss each; boss IDs are `BOS`; every boss's arena location is registered |
| Memories | Exactly 7; one each in CH01–CH07; scene/location IDs match the published table; discovery locations registered; all four fragments non-empty |
| Location IDs | Pattern, category prefix agreement, chapter agreement, no duplicates |
| Chapter rules | Every rule names its enforcement; exclusion rules list their exclusions; canonical rules present |
| **Register parsing** | Real Chapter 1 excerpts parse; vocabularies closed; annotations separated from statuses; hierarchy nesting |
| **World manifests** | Locations registered; final art only on approved designs; non-canon locations cannot be presented as canon; gameplay on non-canon needs `blockout`; child combat targets rejected; snakes rejected in Ch04; routines valid |
| **Mirror drift** | Regenerating from the register excerpt must be a no-op, so the mirror cannot silently diverge |

The drift check was verified by injecting deliberate canon tampering (marking the Wayside Offering Place
`ESTABLISHED`) and confirming CI fails.

## 6. Chapter rules currently encoded

| Rule ID | Chapter | Rule |
|---|---|---|
| `RULE-CH01-GREAT-TREE` | 1 | Great Root Mother tree visible from every major clearing |
| `RULE-CH01-SILK-COTTON` | 1 | The tree is a living kapok with plank buttresses |
| `RULE-CH02-NO-FLAME` | 2 | No living flame until the boss; the kingdom is cold |
| `RULE-CH03-NO-REMAINS` | 3 | No remains ever shown; objects put down, not thrown |
| `RULE-CH03-ASH-NOT-SNOW` | 3 | Ash must not read as snow |
| `RULE-CH04-PYTHONS` | 4 | Pythons never enemies, never loot (OAD-14) |
| `RULE-CH04-NO-LIGHTNING` | 4 | No lightning; reserved for Amadioha |
| `RULE-CH04-NO-STILTS` | 4 | Houses stand on the ground, never on stilts |
| `RULE-CH04-SHRINE-NO-COMBAT` | 4 | No combat at the shrine; deity never depicted by image or face |
| `RULE-CH05-WHITE-LIGHTNING` | 5 | Lightning white only; nothing built on the mountain |
| `RULE-CH05-NO-ALPINE` | 5 | West African granite dome; no snow, conifers, alpine peak |
| `RULE-CH06-MASK-INVENTED` | 6 | Face coverings invented and featureless; consultant review required |
| `RULE-CH06-BLANK-VARIANTS` | 6 | No round discs or nose ridges; nothing monstrous |
| `RULE-CH07-EARTH-NOT-STONE` | 7 | Earth/timber/cloth burnt hard; ember in cracks, never flame; no ferryman, no figures, no remains; starless sky |
| `RULE-NPC-CHILDREN-NO-COMBAT` | — | Children appear only in the home settlement and are never combat targets |
| `RULE-OKWU-HOOD` | — | Okwu's hood is darkness only, in every light (OAD-12) |
| `RULE-ADANNA-NO-MIRROR` | — | Adanna's features never mirrored; right side plain (OAD-51) |
| `RULE-ADANNA-ONE-WEAPON` | — | One short iron sword, left hip (OAD-09/37) |
| `RULE-CULTURAL-FICTIONALITY` | — | Invented mythology never presented as authentic Igbo tradition |

## 7. What v1.0.0 got wrong (kept as a record)

| v1.0.0 | Registers | Correction |
|---|---|---|
| Invented `{design, canon, shippable}` boolean triplet | Three canon statuses + a separate seven-value design status | Two independent fields with closed vocabularies |
| Boss IDs `CHxx-BOSS-<Name>` | `CHxx-BOS-nnn` | ID scheme corrected |
| Only `SUB`, `INT`, `SCN` categories | Nine categories including `ENV`, `SET`, `LMK`, `TRV`, `EXP`, `BOS` | All recognised and validated |
| Memory content status as a single `content_status` | Scene status and location status are separate register rows | Both tracked per memory |
| No distinction between "read from the register" and "assumed" | — | `verified_against_register` flag added; `UNVERIFIED` cannot be presented as canon |

This is recorded deliberately. The failure mode it represents — a plausible engineering abstraction quietly
diverging from canon — is the most dangerous one in this project, and it was caught only by reading the
authoritative document instead of trusting the mirror.

## 8. Known gaps

- **Only Chapter 1 has been captured** from the location and scene registers (fixtures under
  `Tools/canon/tests/fixtures/`). Chapters 2–8 remain `UNVERIFIED`.
- **Six of seven memory discovery locations are `UNVERIFIED`**: `CH02-SUB-003`, `CH03-INT-001`,
  `CH04-SUB-002`, `CH05-SUB-002`, `CH06-INT-003`, `CH07-INT-005`. Only `CH01-SUB-018` has been read.
  They must be read from their chapter register sections before Stage 7 memory work.
- **All memory content is still `PENDING APPROVAL`** at the scene level. Only Memory 1 has been read;
  its scene `CH01-SCN-046` is `PENDING APPROVAL`.
- Boss **arena designs** are `IN REVIEW` (Ch01) or `UNVERIFIED` (Ch02–08). Only encounter *existence* is
  established (OAD-21).
- Supporting-cast names are approved (OAD-15) but are not yet mirrored; they are not runtime keys.
- `CH01-SUB-012` and `CH01-INT-007` were read directly from the register table but are not in the fixture;
  they are marked `verified_against_register: true` with a note. Add them to the fixture on the next capture
  pass so generation reproduces them.
