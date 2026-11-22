# TDD — Explorer's Report: Reconciliation & Review Status

**Document ID:** TDD-IMPL-WORLD-009-R1 · **Date:** 2026-11-22
**Subject document:** `EXPLORERS_REPORT_TO_THE_QUEEN.md` (TDD-IMPL-WORLD-009, v1.0)
**Purpose:** Reconcile the Explorer's Report against the authoritative regional atlas
and the source/evidence register; record which sections are approved, which need
revision, and which remain unresolved; define the route to a reviewed, consistent,
approved version. **The report is NOT rewritten from scratch — its first-person
expedition-journal voice and framing are preserved.**

## 1. Reconciliation sources (authoritative)

| Source | Role |
|---|---|
| `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` (TDD-IMPL-WORLD-002) | Authoritative regional atlas: settlement names, classifications, market days, geography, distances, sacred-place bounds. |
| `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` (TDD-IMPL-WORLD-006) | Source/evidence tier for every claim ([H] research-supported, [R] regionally documented, [A] provisional/adaptive). |
| `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` (TDD-IMPL-WORLD-003) | Calendar, market network, seasons. |
| `STORY_TO_WORLD_INTEGRATION.md` (TDD-IMPL-WORLD-004) | Canon: Adanna/Nneka/Ezeani, CH01 = Ahanwụ, Ancestral Realm status. |
| `TDDWorldLogic.h` / `omega_valley.json` | Runtime settlement data (3 Phase-1 settlements). |

## 2. Settlement reconciliation (names, classifications, geography)

All eight named settlements in the report reconcile with the atlas:

| Settlement | Atlas classification | Atlas market day | Report section | Verdict |
|---|---|---|---|---|
| Ọmà Ukwu | Town | Eke | §3 | ✅ matches |
| Ịbe | Town | Orie | §4 | ✅ matches (hill town, smiths) |
| Ahanwụ | Village | Afo | §5 | ✅ matches (farming village) |
| Ihiala | Village | Nkwo | §5 | ✅ matches (between Ọmà & Ụmụ) |
| Ụkwụ | Village | — (no major market) | §5 | ✅ matches (river village) |
| Ezimmiri | Village | — (no major market) | §5 | ✅ matches (potters) |
| Ọnịcha | Market settlement | Orie | §8, §13 | ✅ matches (fish market, weaving) |
| Ọba | Market settlement | Afo | §8 | ✅ matches (cassava/grain market) |

**Geography** reconciles: Ọmà River (centre, §2), Ụmụ River (east, §7), Nkwụ Stream
(west, §7), Ahioma hills (east, §4), Ezi-na-Oke forest (southwest, §12). All match the
atlas water/landmark table.

**Craft specialisation** reconciles: Ịbe=iron/smiths (§4, §13; atlas "Awka-style
smithing"), Ezimmiri=pottery (§5, §13; atlas "pottery-specialised"), Ọnịcha=weaving
(§13; atlas "weaving"), Ụkwụ=fish-drying (§13; atlas "fishing, reeds").

## 3. Sacred places & cultural practices — review against the evidence register

- **§15 Shrine-groves and their bounds:** the report describes shrine-groves with
  restraint, records that the explorer "did not enter them" and "did not ask what is
  done within," and explicitly states "I have not invented their rites." This aligns
  with the atlas (Ahanwụ Shrine-grove = access-restricted, "specific rules need
  Research + cultural review — **not invented**") and with the canon-protection
  directive (no invented deities/rituals/prohibitions). **Verdict: ✅ restraint
  preserved; no invented rites.**
- **§14 Council and the square:** acephalous governance (no single king; decisions by
  elders in the `ama`). This aligns with the canon directive (no unified Igbo
  empire/universal king) and the research basis (segmentary lineage, acephalous).
  **Verdict: ✅ aligns with canon.**
- **§6 Compounds / obi / ezi:** matches the atlas household→compound→kindred hierarchy.
  **Verdict: ✅ research-supported.**
- **§10 Seasons / Iri Ji:** two seasons (rain/dry), Iri Ji new-yam festival. Matches
  the calendar blueprint. **Verdict: ✅ research-supported.**
- **Ancestral Realm (§18):** referenced only as "a narrative space, kept as the people
  hold it" — not an ordinary place, not mapped. Matches the canon directive (Ancestral
  Realm keeps narrative status). **Verdict: ✅ canon-consistent.**

## 4. Items requiring revision or flagging

### 4a. Market-day assignments — PROVISIONAL [A] (needs Story/Research approval)
The report §8 states the per-settlement market days as observed fact:
Ọmà Ukwu=Eke, Ọnịcha=Orie, Ịbe=Orie, Ọba=Afo. These **match the atlas**, but per
`WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` the **specific per-settlement day assignments
are provisional creative adaptation `[A]`** — the four-day system and "each
settlement keeps its own day" are research-supported `[H]`, but the exact mapping
requires **Story/Research approval** before being treated as canon.

**Action:** The report's market-day statements are technically accurate against the
provisional data, but must not be treated as canon until Story/Research approves the
assignments. Route to Research + Story for sign-off; on approval, the assignments
become canon and the report needs no further change. **Status: UNRESOLVED — pending
Research/Story approval of the `[A]` market-day assignments.**

### 4b. Distance wording (§16) — REVISED
The report originally stated Ahanwụ→Ọmà Ukwu is "about half a day." The atlas gives
~4 km / ~50–70 min. **Corrected in this revision** to "some four kilometres — an hour
or a little more." **Status: REVISED (this commit).**

### 4c. Omissions (not errors)
§8 does not name Ahanwụ's (Afo) or Ihiala's (Nkwo) market day. These are omissions,
not contradictions. Optional: add them for completeness once the `[A]` assignments are
approved. **Status: OPTIONAL — defer to the approval outcome.**

## 5. Section-by-section status

| Section | Status | Notes |
|---|---|---|
| 1 Commission | ✅ Approved | Voice and framing sound. |
| 2 First sight of the river | ✅ Approved | Geography matches atlas. |
| 3 Towns upon the water (Ọmà Ukwu) | ✅ Approved | Classification, market, craft match. |
| 4 Hill town of Ịbe | ✅ Approved | Smiths/hill-town match atlas + research. |
| 5 Villages along the water | ✅ Approved | All four villages match. |
| 6 Compounds and the obi | ✅ Approved | Research-supported. |
| 7 Ụmụ and Nkwụ | ✅ Approved | Tributary geography matches. |
| 8 Market days | ⚠️ Needs approval | Text matches atlas, but assignments are `[A]` provisional — needs Story/Research sign-off to become canon. |
| 9 Market in the rain | ✅ Approved | Weather-consequence alignment. |
| 10 Seasons | ✅ Approved | Research-supported. |
| 11 Fields and the yam | ✅ Approved | Research-supported. |
| 12 Forest and its giving | ✅ Approved | Ezi-na-Oke matches. |
| 13 Craft of the hands | ✅ Approved | Craft specialisation matches atlas. |
| 14 Council and the square | ✅ Approved | Acephalous; canon-consistent. |
| 15 Shrine-groves and their bounds | ✅ Approved (cultural review) | Restraint preserved; no invented rites. Cultural Review to confirm. |
| 16 Road and the journey | ✅ Approved (revised) | Distance corrected to match atlas. |
| 17 The people | ✅ Approved | Voice and framing sound. |
| 18 Things I could not reach | ✅ Approved | Ancestral Realm narrative status preserved. |
| 19 Conclusion | ✅ Approved | Shape of the land matches atlas. |
| Glossary | ✅ Approved | Terms consistent with atlas glossary. |

## 6. Route to a reviewed, consistent, approved version

1. **Research:** verify the `[A]` market-day assignments (Ọmà Ukwu=Eke, Ọnịcha=Orie,
   Ịbe=Orie, Ọba=Afo, Ahanwụ=Afo, Ihiala=Nkwo) against regional market-day evidence;
   confirm the 8-day major/minor cycle note if the report later references it.
2. **Story:** confirm narrative fit of the market-day assignments and the
   settlement-to-craft mapping; confirm no canon contradiction (Adanna/Nneka/Ezeani,
   CH01=Ahanwụ untouched).
3. **Cultural Review:** review §15 (shrine-groves) and any sacred-place bounds for
   cultural accuracy and restraint; confirm no invented rites/deities/prohibitions.
4. **On approval:** the market-day assignments become canon; mark §8 `[A]`→approved;
   optionally add Ahanwụ/Ihiala market days to §8 for completeness.
5. **PM:** record the approval in `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` and bump the
   report version to v1.1 (approved).

**Owner note:** This reconciliation is agent-side and static. Research/Story/Cultural
Review sign-off is a human decision this agent cannot make — it is flagged here as the
required next step, not assumed.
