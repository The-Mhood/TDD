# CANON INDEX — engineering mirror of the Art Bible registers

**Document:** TDD-CANON-001 · **Version:** 1.0.0 · **Date:** 2026-11-16

## What this is, and what it is not

`Tools/canon/data/canon_index.json` is a **machine-readable mirror of a subset** of the Google Drive
Production Art Bible. It exists so that engineering can:

1. validate that the IDs used in code and data are canonical (ADR-0006),
2. enforce canon *rules* (python rule, no flame, no remains, no stilt houses, masks are invented, etc.)
   as automated tests rather than as art-team discipline,
3. generate the seven-memory DataTable without hand-copying prose.

**It is not canon.** The Drive registers are authoritative:

| Register | Drive ID | Authority |
|---|---|---|
| `CHARACTER_DESIGN_REGISTER.md` | `1naNn0D7jAXOVc01Xvnl4YYEvS_zwcTjH` | visual + identity canon |
| `ENVIRONMENT_DESIGN_REGISTER.md` | `1WxQeJ7Hnac4gUnOR9EF156ClSTZebpsx` | environment design + per-chapter rules |
| `OPEN_ART_DECISIONS.md` | `1c6SaYn1U2JLX0wu6sg-fpvPX5T1LAb0Q` | art + canon decisions (OAD-01…OAD-59) |
| `NNEKA_MEMORIES_AND_TIMELINE.md` | `1CzvUvsYgFOX5FAbha0lGs4Fj0NKnexgq` | memory sequence, timeline, concealment |

If this mirror and a register disagree, **the register wins and the mirror is wrong.** Fix the mirror; if the
register itself is ambiguous, raise it to the register owner. Never edit the mirror to make a test pass.

## How it is validated

```bash
python3 -m unittest discover -s Tools/canon/tests -v
```

Four validator groups run against the index (architecture doc §13.3):

| Validator | Checks |
|---|---|
| Structure + schema | Required keys; hand-rolled JSON-Schema subset (no third-party dependency); schema uses only supported keywords (so validation cannot silently skip a constraint) |
| Chapters + bosses | Exactly 8 chapters, indexes 1–8, names and bosses match the directive; every chapter has exactly one boss entry; boss IDs match chapter prefixes |
| Approvals | **The three approval axes are independent** (OAD-47/48): `design`, `canon`, `shippable`. Nothing may be shippable before canon approval. Chapter 8 locations must be design-approved-but-not-canon (current true state) |
| Memories | Exactly 7; one each in CH01–CH07; scene and location IDs match the published table; every discovery location is registered; all four fragments (place/object/sound/interaction) non-empty; no duplicate IDs |
| Chapter rules | Every rule names how it is enforced; exclusion rules list what they exclude; no duplicate rule IDs; canonical rules present (pythons, no flame, no remains, ember not stone, Okwu hood, Adanna's side rules, cultural fictionality) |

Current status: **58 tests, all passing.** Evidence: `Docs/evidence/stage0/L0_canon_index_validation.json`.

## ID scheme

```
CHxx                    chapter 01..08
CHxx-SCN-yyy            scene
CHxx-SUB-yyy            sublocation / microlocation
CHxx-INT-yyy            interior
CHxx-BOSS-<Name>        boss encounter          (engineering extension)
<id>-P                  engineering proposal    (NOT canon)
```

Examples verified in the registers: `CH01-SCN-046`, `CH01-SUB-018`, `CH02-SUB-003`, `CH03-INT-001`,
`CH04-SUB-002`, `CH05-SUB-002`, `CH06-INT-003`, `CH07-INT-005`, `CH08-SUB-005`, `CH08-SUB-006`,
`CH08-SUB-007`, `CH08-INT-001`, `CH08-INT-003`.

## The three approval axes (OAD-47 / OAD-48)

This is the rule most likely to be violated under production pressure, so it is enforced in code:

| Axis | Meaning | Consequence if false |
|---|---|---|
| `design` | The *visual design* has been reviewed and accepted | Cannot be used for composition/character work downstream |
| `canon` | The place/character is an **established story** element | Cannot ship; cannot be referenced in narrative or save data as established |
| `shippable` | Passes all gates including cultural review | Cannot appear in a release build |

Approving a design does **not** approve canon. OAD-45 approved four Chapter 8 environment designs *for
composition work*; OAD-47/48 confirmed those locations remain `canon_status: Proposed`. That is why the
Chapter 8 entries in the index are `design: true, canon: false`.

## Chapter rules currently encoded

| Rule ID | Chapter | Rule |
|---|---|---|
| `RULE-CH01-GREAT-TREE` | 1 | Great Root Mother tree visible from every major clearing (navigation landmark) |
| `RULE-CH01-SILK-COTTON` | 1 | The tree is a living kapok with plank buttresses; approach V003 governs the model |
| `RULE-CH02-NO-FLAME` | 2 | No living flame until the boss; the kingdom is cold |
| `RULE-CH03-NO-REMAINS` | 3 | No remains ever shown; objects put down, not thrown; palace faces scraped away |
| `RULE-CH03-ASH-NOT-SNOW` | 3 | Ash must not read as snow |
| `RULE-CH04-PYTHONS` | 4 | Pythons are never enemies and never loot (OAD-14) |
| `RULE-CH04-NO-LIGHTNING` | 4 | No lightning; reserved for Amadioha |
| `RULE-CH04-NO-STILTS` | 4 | Houses stand on the ground, never on stilts |
| `RULE-CH04-SHRINE-NO-COMBAT` | 4 | No combat at the shrine; deity never depicted by image or face |
| `RULE-CH05-WHITE-LIGHTNING` | 5 | Lightning is white only; nothing is built on the mountain |
| `RULE-CH05-NO-ALPINE` | 5 | West African granite dome; no snow, no conifers, no alpine peak |
| `RULE-CH06-MASK-INVENTED` | 6 | All face coverings invented and featureless; consultant review required |
| `RULE-CH06-BLANK-VARIANTS` | 6 | No round discs or nose ridges; nothing monstrous |
| `RULE-CH07-EARTH-NOT-STONE` | 7 | Earth/timber/cloth burnt hard, never stone castle; ember in cracks, never flame; no ferryman, no figures, no remains; starless sky |
| `RULE-OKWU-HOOD` | — | Okwu's hood is darkness only, in every light, always (OAD-12) |
| `RULE-ADANNA-NO-MIRROR` | — | Adanna's features are never mirrored; right side plain (OAD-51) |
| `RULE-ADANNA-ONE-WEAPON` | — | One short iron sword, left hip; no spear, no second weapon (OAD-09/37) |
| `RULE-CULTURAL-FICTIONALITY` | — | Invented mythology never presented as authentic Igbo tradition |

## Maintenance workflow

1. Register owner updates a Drive register.
2. Engineering updates the mirror in the same change window, incrementing `meta.version`.
3. `python3 -m unittest discover -s Tools/canon/tests` must pass.
4. If a new ID is needed before the register exists, use the `-P` suffix and record it in the mirror's
   `source` as `engineering-proposal`. It stays Proposed.
5. Evidence file is regenerated by the test suite (`Docs/evidence/stage0/L0_canon_index_validation.json`).

## Known gaps in the mirror (deliberately out of scope for v1.0.0)

- The full location and scene registers (534 KB / 278 KB) are **not** mirrored; only locations that
  engineering actively keys on. Expanding this is a Stage 6 task as chapters become real.
- **No memory content is canon-approved yet** — all seven are `content_status: Proposed` with
  "proposed content and implementation PENDING APPROVAL" (OAD-32). Engineering builds the *mechanism*
  and one playable memory (Memory 1) for the vertical slice; the other six definitions are data-complete
  but blocked on approval.
- Boss **arena** designs are all `Proposed` (OAD-21). Only encounter *existence* is established.
- Supporting-cast names are approved (OAD-15) but are not yet mirrored; they are not runtime keys.
