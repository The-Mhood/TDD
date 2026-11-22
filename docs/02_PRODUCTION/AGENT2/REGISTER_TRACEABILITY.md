# REGISTER → WORLD TRACEABILITY

**Document ID:** TDD-TRACE-001
**Version:** 1.0.0
**Date:** 2026-11-16
**Author:** Agent 2 (world structure / level architecture)
**Status:** Current for Chapter 1. Chapters 2–8 not ingested — see §7.

Honours Technical Directive TR-4: *`verified_against_register` must name the precise source register and version, and its result; never represent unverified as verified.*

---

## 1. The two status axes, and why they are never merged

A single status field cannot express this project's situation, and merging the two axes is the error that already occurred once in this repository (canon v1.0.0 used an invented approval triplet).

| Axis | Values | Decides | Does **not** decide |
|---|---|---|---|
| **Canon status** | `ESTABLISHED` · `PROPOSED` · `PENDING APPROVAL` | Whether a thing is a story fact | Whether any art exists or is approved |
| **Environment design status** | `NOT STARTED` · `EXPLORATORY` · `IN REVIEW` · `REQUIRES REVISION` · `CONDITIONAL` · `APPROVED` · `REJECTED` | Whether a board/design exists and where its review stands | Whether the thing is canon |

The register states the rule plainly: *"Approving a design does not change canon status and establishes no story fact."* And the converse, which matters just as much: **an ESTABLISHED story fact does not mean any design exists.** The eight boss encounters are ESTABLISHED; every boss **arena** is PROPOSED.

Consequences that are easy to get wrong:

- `ESTABLISHED` + `NOT STARTED` is a normal, expected combination (canon is settled, no art yet).
- `PENDING APPROVAL` + `IN REVIEW` is normal (a board exists, and the proposal implies story).
- `PROPOSED` + `APPROVED` would mean approved art for something that makes no story claim — legal, and common for set dressing.
- **`APPROVED` never appears as a canon status, and `ESTABLISHED` never appears as a design status.**

---

## 2. Vocabulary preserved exactly

IDs are permanent and never reused. Categories:

| Category | Meaning | Is a location entry |
|---|---|---|
| `ENV` | Major environment (one per chapter) | yes |
| `SUB` | Sub-location | yes |
| `SET` | Settlement | yes |
| `INT` | Interior | yes |
| `LMK` | Landmark | yes |
| `TRV` | Traversal area | yes |
| `EXP` | Exploration area | yes |
| `BOS` | Boss arena | yes |
| `SCN` | Scene or micro-location | **no** |

Scene categories (10, all preserved verbatim from the scene register): `MAIN STORY SCENE`, `SECONDARY STORY SCENE`, `INCIDENTAL SCENE`, `AMBIENT NPC SCENE`, `ENTERABLE INTERIOR`, `EXTERIOR MICRO-LOCATION`, `ENVIRONMENTAL STORYTELLING`, `EXPLORATION SCENE`, `WORLD ACTIVITY SCENE`, `ATMOSPHERIC SCENE`.

Access levels (4 + open ground): `FULLY ENTERABLE`, `PARTIALLY ENTERABLE`, `VISUALLY ACCESSIBLE`, `BACKGROUND ENVIRONMENT`, `OPEN EXTERIOR`.

These are not engineering conveniences to be tidied. Renaming `ATMOSPHERIC SCENE` to `ATMOSPHERE` would break the mapping from register to budget and make every derived count unverifiable.

---

## 3. The register's six counts are six different things

Full derivation and the anti-double-counting rules live in `Tools/world/count_reconciliation.py` and `Docs/REGISTER_INGESTION.md`. Summary:

| Register column | Value | Counts as |
|---|---|---|
| Major environments | 8 | location entry |
| Other locations (not interiors) | 142 | location entry |
| Interiors (location entries) | 46 | location entry |
| Scenes and micro-locations | 135 | **not** a location |
| — of which not main/secondary story | 122 | subset of the 135 |
| Environment-state references | 40 | **not** a location; a variant of one |

**Location entries = 8 + 142 + 46 = 196.** This corrects the figure of 191 that was recorded in `canon_index.json` v2.0.0; the arithmetic was simply wrong, and it is now guarded by a regression test that scans the repository for the stale value.

**13 scenes are main or secondary story** (135 − 122). This is independently corroborated by the scene register's own category counts (MAIN STORY 4 + SECONDARY STORY 9 = 13). Two registers agreeing on a number derived from different columns is the strongest verification available in this repository.

---

## 4. Traceability table — Chapter 1

Every row names the register, version, and the verification result. `VERIFIED` means the value was read from the register and checked by a test. `UNVERIFIED` means it is recorded but has not been confirmed against the source.

### 4.1 Environment scope

| Item | Value | Source | Result |
|---|---|---|---|
| Chapter 1 major environment | `CH01-ENV-001` The Forbidden Forest | LOC 2.9 §Ch1 summary | VERIFIED — canon ESTABLISHED |
| Location entries, Ch1 | 57 published (1 ENV + 40 other + 16 INT) | LOC 2.9 count table | VERIFIED by arithmetic |
| Location entries parsed | 13 | fixture excerpt | PARTIAL CAPTURE — documented, not a defect |
| Scenes, Ch1 | 46 | SCN 1.9 | VERIFIED — 46/46 parsed, matches register total |
| Non-story scenes, Ch1 | 45 | LOC 2.9 count table + SCN 1.9 categories | VERIFIED — two sources agree |
| Environment states, Ch1 | 14 referenced; 2 transcribed verbatim | LOC 2.9 state table | PARTIAL |

### 4.2 Canon status distribution, Chapter 1 (46 scenes)

| Status | Count | Note |
|---|---|---|
| `PROPOSED` | 45 | no story claim |
| `PENDING APPROVAL` | 1 | `CH01-SCN-046` — implies story |
| `ESTABLISHED` | 0 | — |

No Chapter 1 scene is established. **This is why the whole chapter is greybox territory**: there is essentially no established scene content to build against.

### 4.3 The seven memories

Each is tracked individually. The hidden third ending requires **all seven**. Missing **one** closes that ending only (OAD-32) — it does not block the main story.

| # | Scene | Parent location | Scene status | Verification |
|---|---|---|---|---|
| 1 | `CH01-SCN-046` | `CH01-SUB-018` The Wayside Offering Place | PENDING APPROVAL | **VERIFIED** against SCN 1.9 + LOC 2.9 |
| 2 | `CH02-SCN-011` | `CH02-SUB-003` | — | **UNVERIFIED** — chapter 2 not ingested |
| 3 | `CH03-SCN-012` | `CH03-INT-001` | — | **UNVERIFIED** |
| 4 | `CH04-SCN-012` | `CH04-SUB-002` | — | **UNVERIFIED** |
| 5 | `CH05-SCN-011` | `CH05-SUB-002` | — | **UNVERIFIED** |
| 6 | `CH06-SCN-010` | `CH06-INT-003` | — | **UNVERIFIED** |
| 7 | `CH07-SCN-015` | `CH07-INT-005` | — | **UNVERIFIED** |

Only memory 1 has a verified scene and location. The other six are recorded so the memory director's interface can be designed, but **no system may treat them as confirmed**. The manifest validator rejects any memory not present in the canon mirror, and the mirror marks unverified entries explicitly rather than omitting them — omission would be indistinguishable from "no memory here".

### 4.4 Boss encounters

| Chapter | Encounter | Arena id | Encounter canon | Arena design |
|---|---|---|---|---|
| 1 | Great Root Mother | `CH01-BOS-001` | ESTABLISHED | IN REVIEW |

The register's own rule: *"the encounter is ESTABLISHED. The arena's environment, layout, architecture, lighting, hazards and mechanics are PROPOSED."* `CH01-BOS-001` carries a dual status for exactly this reason. Sample counts must read the **canon** field, not assume the arena is approved because the encounter is.

Chapters 2–8 boss arenas exist as IDs only. No boss has been designed, built, or tested. See §7 on CD-3.

---

## 5. What is proposed and must stay labelled

| Item | Status | Why it matters |
|---|---|---|
| All six enemy archetypes | **PROPOSED** | CD-3 was **NOT RATIFIED**. All six stay PROPOSED. Invent no mythology. |
| Chapters 2–8 locations | PROPOSED / PENDING APPROVAL (per register) | Not ingested; not designed |
| Memories 2–7 scene bindings | **UNVERIFIED** | Recorded for interface design only |
| Chapter 8 material | EXPLORATORY | The register itself says Chapter 8 is not yet approved |
| Any greybox geometry | **PENDING APPROVAL — BLOCKOUT ONLY** | Technical evaluation only, never art |

Engineering convenience must never become canon. Concretely, that means:

- A scene-parent location inferred by a generator is written `UNVERIFIED`, never `ESTABLISHED`.
- Ambient content is not assumed to be NPC-free merely because the category sounds atmospheric. The register contradicts this: `CH01-SCN-025` "Goats at Dusk" depicts *one boy*; `CH01-SCN-032` depicts nobody.
- A population budget number is an **engineering assumption**, labelled as such in `population_policy.json`, never presented as register data.
- An unknown or unparseable register value raises a validation failure rather than defaulting to something convenient.

---

## 6. Verification mechanism

Traceability is enforced, not asserted:

| Guarantee | Enforced by |
|---|---|
| Every manifest id resolves to a real location | `Tools/world/world_manifest.py` |
| Manifest status agrees with the register mirror | same |
| The mirror matches its source, bit for bit | `Tools/ci/l0_checks.py::check_canon_mirror_drift` |
| The register's counts sum correctly | `Tools/ci/l0_checks.py::check_register_counts_reconcile` |
| Chapter 1 parses exactly 46 scenes | `Tools/world/count_reconciliation.py` |
| CD-5 greybox restrictions hold | `Tools/ci/l0_checks.py::check_greybox_restrictions` |
| Greybox status agrees with the register | `Tools/world/tests/test_greybox.py` |

Drift detection was proved by injection: setting `CH01-SUB-018` to `ESTABLISHED` in the mirror fails the gate. The register-counts gate was proved by injecting a wrong published total. Both were restored afterwards.

---

## 7. Blockers

| Blocker | Effect | Owner |
|---|---|---|
| **CD-3 not ratified** | Six enemy archetypes usable for interface design only | TD / Creative Director |
| **CD-2 open (consultant gate)** | Shrine, mask, ritual content cannot be designed, only blocked out or omitted | TD / consultant |
| Chapters 2–8 not ingested | Any per-chapter claim beyond Chapter 1 would be fabricated | Agent 2 |
| Memories 2–7 unverified | Memory director interface is provisional | Agent 2 + narrative |
| No Unreal project | Everything here is `SPEC`; nothing is executable gameplay | TD |

The last one governs how everything in this document should be read: **no system described here has been compiled or run in an engine.** What has been run is Python validation over register-derived data, and the evidence artifacts record exactly that.

---

## 8. Change log

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-11-16 | First issue. Two status axes separated; six counts discriminated; Chapter 1 traced row by row; 191 → 196 correction recorded; memories 1 verified, 2–7 marked unverified. |
