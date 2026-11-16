# DEPENDENCY AND BLOCKER REGISTER

**Document ID:** TDD-DEP-001
**Version:** 2.0.0
**Date:** 2026-11-16
**Author:** Agent 2 (world structure / level architecture)
**Status:** Current.

Supersedes the dependency section of `Docs/WORLD_ASSESSMENT.md`. Kept here because dependencies now span four parties and a decision log, which outgrew a section.

---

## 1. Decision log — what the TD decided and what it binds

| ID | Decision | Outcome | What it binds on Agent 2 |
|---|---|---|---|
| **CD-5** | Greybox for pending content | **APPROVED WITH RESTRICTIONS** | May represent PENDING APPROVAL content as blockout **for technical evaluation only**: labelled `PENDING APPROVAL — BLOCKOUT ONLY`; spatial/navigation/streaming/sightline tests only; no final art; no shrine/mask/ritual decoration; no story dependency; removable without breaking progression; never changes approval status. |
| **CD-3** | Enemy archetype roster | **NOT RATIFIED** | All six archetypes stay PROPOSED. Submit review doc with role/chapter/behaviour/capabilities/narrative relationship/cultural-visual deps. Invent no mythology. |
| **CD-2** | Shrine / mask / ritual content | **OPEN** | Consultant gate holds. Nothing in that vocabulary may be designed, only blocked out (and see CD-5's exclusion) or omitted. |
| **TR-1** | Traceable population budget | Directed | Register category → tier → named actor / Mass crowd / scripted / background-only. Do not assume ambient activity needs a simulated NPC. |
| **TR-2** | Entity relationship / anti-double-count | Directed | Document how 142 / 46 / 135 / 40 relate. Preserve register IDs. |
| **TR-3** | Reproducible mirror | Directed | Document source versions, parsing assumptions, unsupported formats, validation failures, regeneration. |
| **TR-4** | Traceability | Directed | `verified_against_register` names precise register + version + result. Never represent unverified as verified. |
| **TR-5** | Vocabulary and labels | Directed | Preserve exact canon and environment-design vocabularies. Keep PROPOSED archetypes, unapproved locations, unverified memories labelled. |

---

## 2. Blockers, by severity

### 2.1 Hard blockers — nothing downstream can proceed

| # | Blocker | Blocks | Owner | Notes |
|---|---|---|---|---|
| **B-01** | **No Unreal project exists** | Every runtime system | TD / Agent 3 | All world systems are `SPEC`. No C++ has been compiled. No streaming, Mass, AI or navigation has run. This is the dominant blocker. |
| **B-02** | **CD-3 not ratified** | Enemy archetypes, boss encounter design | TD / Creative Director | Six archetypes are documented but unratified. Interface design may proceed; content may not. |
| **B-03** | **CD-2 consultant gate open** | Shrine, mask, ritual content | TD / consultant | Blocks Maskbearer entirely; constrains Rootwarden, Thrall, Thunder Aspirant. |
| **B-04** | **Traversal contract undefined** | Climbing, route requirements, exploration reachability | Agent 1 + TD | Requested (`Docs/AGENT1_TRAVERSAL_CONTRACT_REQUEST.md`). Provisional ids only until answered. |

### 2.2 Data blockers — work proceeds only within known limits

| # | Blocker | Blocks | Owner | Notes |
|---|---|---|---|---|
| **B-05** | Chapters 2–8 not ingested | Any per-chapter claim beyond Ch1 | Agent 2 | Only Ch1 locations (partial) and scenes (complete) are captured. Fabricating Ch2–8 numbers is prohibited. |
| **B-06** | 11 of 46 Ch1 scenes lack detail blocks | Accurate NPC counts | Agent 2 | **Reduced from 41 to 11 by W-M2.2.** The 11 remaining are all SCRIPTED or NONE tier, whose cost does not depend on the count, so this now blocks *provenance*, not accuracy. A further 7 scenes have prose the register does not reduce to an integer (ranges/alternatives/conditions); they are bounded, not resolved. `CH01-SCN-014` states no number at all and leaves the cost band OPEN. |
| **B-07** | Memories 2–7 unverified | Full memory director | Agent 2 + narrative | Only memory 1 has a verified scene/location binding. |
| **B-08** | No retired-ID tracking | Canon hygiene | Agent 2 + register owner | A retired ID would parse as active. |

### 2.3 Process risks — not blocking today, will bite later

| # | Risk | Trigger | Mitigation |
|---|---|---|---|
| **B-09** | Mirror staleness — no Drive sync | Register updated, fixtures not refreshed | Manual process documented; no automated signal (**R-06**) |
| **B-10** | Silent parse failure on format change | Register reformatted | Consumers assert expected row counts; a new consumer could miss it |
| **B-11** | Word-list NPC parsing undercounts | Register uses nouns outside the lists | Flagged only when count lands at zero |
| **B-12** | Access budgets unvalidated | First playable build | ≤12 resident locations, ≤20 scenes, ≤14 AI agents, ≤8 s stream-in are **unmeasured** |

---

## 3. Cross-agent dependencies

### 3.1 On Agent 1 — gameplay, character, combat

| # | Need | Status | Blocks |
|---|---|---|---|
| A1-1 | Traversal capability enum | **REQUESTED** | Climbing, route validation |
| A1-2 | Route requirements: data or code? | **REQUESTED** | Offline reachability validation |
| A1-3 | Traversal failure semantics | **REQUESTED** | Hint volumes in scene data |
| A1-4 | `ITDDInteractable` implementation | Not started | All environment interaction |
| A1-5 | Enemy base class + combat interface | Not started | Any enemy work |
| A1-6 | Capsule dimensions confirmed | SPEC only (r42/h90) | Scene metric validation |

### 3.2 On Agent 3 — integration, technical quality

| # | Need | Status | Blocks |
|---|---|---|---|
| A3-1 | Unreal project + module skeleton | **Not started** | Everything runtime |
| A3-2 | CI able to run `-nullrhi` automation | Not started | Engine-level test evidence |
| A3-3 | Perf capture harness | Not started | Validating any budget |

### 3.3 On Creative Director

| # | Need | Status |
|---|---|---|
| CD-A | Ratify or reject CD-3 archetypes | **Open** |
| CD-B | Close CD-2 consultant gate | **Open** |
| CD-C | Confirm memory 1 scene/location binding | Verified in register; needs no action |
| CD-D | Decide whether Ch1 needs a creature at all | Open (§6 of enemy review) |

---

## 4. What unblocks what

```
B-01 Unreal project
  └─> A3-2 CI automation ──> engine-level evidence for everything below
  └─> A1-5 enemy base ──> enemy archetypes (after B-02)
  └─> A1-1 traversal enum (B-04) ──> route requirements ──> exploration validation
  └─> Streaming ──> B-12 budget validation

B-05 chapters 2-8 ingested
  └─> per-chapter population budget
  └─> per-chapter manifests
  └─> B-07 memory bindings for 2-7

B-02 CD-3 ratified
  └─> archetype implementation (still needs A1-5)

B-03 CD-2 closed
  └─> Maskbearer (still needs B-02)
  └─> any shrine/mask/ritual content
```

Note the shape: **B-01 blocks almost everything**, and CD decisions block content but not interface design. That is why this milestone produced interfaces, schemas and validators rather than systems — it is the maximum progress available given the blockers, not a substitute for the blocked work.

---

## 5. Honest status of this milestone's deliverables

| Deliverable | Functional | Partial | Mocked | Experimental | Unavailable |
|---|---|---|---|---|---|
| Canon mirror + drift detection | **yes** | | | | |
| Register parsers (locations, scenes, details) | **yes** | | | | chapters 2–8 |
| Population budget derivation | **yes** | | | | per-scene accuracy (11 policy defaults, all count-independent; band OPEN at `CH01-SCN-014`) |
| Count reconciliation | **yes** | | | | chapters 2–8 |
| Greybox restriction validator | **yes** | | | | nothing to validate (no geometry exists) |
| Enemy archetype review | | **yes** (doc only) | | | any implementation |
| Traversal contract | | **yes** (request only) | | | any agreement |
| Streaming / Mass / AI / nav / bosses | | | | | **all — no engine** |

"Functional" means: runs, tested, and the tests would fail if it broke. It does **not** mean anything runs in an engine — nothing does.

---

## 6. Change log

| Version | Date | Change |
|---|---|---|
| 2.0.0 | 2026-11-16 | Restructured around CD-5/CD-3/CD-2 outcomes and TR-1..5. 12 blockers ranked by severity. Cross-agent needs itemised. Added honest capability table. |
| 1.0.0 | — | Superseded: dependencies were a section inside WORLD_ASSESSMENT.md. |
