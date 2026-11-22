# TDD — World Scale & Living World Blueprint

**Document ID:** TDD-IMPL-WORLD-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM (world-production owner). **Status:** PLAN — the authoritative world-production blueprint. **This supersedes the MEDIUM_6 populated-compound density assumption as the overall world-production target.**
**Scope:** The complete pre-colonial Igbo world of *The Disobedient Daughter* — geography, settlements, population, economy, calendar, weather, wildlife, story integration, engineering architecture and phased execution.
**Companion documents (this directory):** `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md`, `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md`, `STORY_TO_WORLD_INTEGRATION.md`, `EXPLORERS_REPORT_TO_THE_QUEEN.md`, `ENGINEERING_WORLD_SPECIFICATION_AND_EVIDENCE.md`.
**Production direction:** ZERO production cost — maximum achievable quality. No paid tools assumed; no essential tool rejected without investigation.

---

## Executive summary

The world of *The Disobedient Daughter* is the **Ọmà Ala** — a fictional, geographically coherent pre-colonial Igbo region in the forest–savanna transition of southeastern Nigeria, centred on the **Ọmà River** and its tributaries. It is not an expanded Compound V2. It is a populated, traversable, seasonally changing region of towns, villages, kindred compounds, farmland, forest, river and market network, in which every chapter, scene, character and location belongs to the same geography and society.

The world is built on the existing Agent-2 `WORLD_ARCHITECTURE.md` hierarchy (World → Chapter → Major Environment → Locations → Scenes; 8 chapters, 135 scenes) and **expands** the MEDIUM_6 populated-compound assumption into a full regional population model. The 3-tier NPC fidelity model (named actors / crowd / background) is retained and scaled to the regional population.

**Core scale (proposed, to be confirmed with Story/owner):**
- Explorable region: **~18 × 14 km** (~250 km²), with believable travel distances (a 4–7 km foot journey between neighbouring settlements; a half-day river trip to the town).
- **1 regional town**, **8 villages**, **3 market settlements**, **dispersed kindred compounds**, plus wilderness (forest, river, hill, farmland).
- **Regional population ~7,000–9,000** across the settlement hierarchy, with a persistent underlying population and event-driven surges (markets, festivals, story events).
- **4 market days** (Eke, Orie, Afo, Nkwo) distributed across settlements so the player can travel to a market on its scheduled day.
- **13-month Igbo calendar** (Ọgụàfọ̀) with 4-day market weeks, rainy/dry seasonal progression, and agricultural cycles.

**Canon protected (non-negotiable):** Adanna/Nneka/Ezeani family history (Ezeani killed Nneka; Adanna was six; concealment of memories); the Ancestral Realm retains its narrative status; Chapter 2's dead industrial compounds retain the no-living-flame restriction; all established character/environment identities. The world serves the story; it does not rewrite it.

**Honest status:** This is the **complete world plan** (deliverables 1–12 below). **Implementation, integration and playable evidence are the acceptance standard** — this blueprint is not completion. Phased execution begins with one fully-worked region proving the systems, then expands.

---

## The 12 required deliverables (status)

| # | Deliverable | Status | Location |
|---|---|---|---|
| 1 | Research-backed regional map & geographical references | **DONE (plan)** | `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` §2–4 |
| 2 | Explorable world boundaries & scale, with distance estimates | **DONE (plan)** | `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` §5 |
| 3 | Settlement hierarchy & population estimates | **DONE (plan)** | `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` §6; `..._POPULATION.md` §3 |
| 4 | Residential / economic / public population distribution | **DONE (plan)** | `..._POPULATION.md` §4–5 |
| 5 | Market locations, schedules & trading relationships | **DONE (plan)** | `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` §2–3 |
| 6 | Calendar & seasonal model | **DONE (plan)** | `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` §4–5 |
| 7 | Weather & environmental progression model | **DONE (plan)** | `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` §6 |
| 8 | Travel & exploration system design | **DONE (plan)** | `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` §7 |
| 9 | NPC simulation & performance architecture | **DONE (plan)** | `ENGINEERING_WORLD_SPECIFICATION_AND_EVIDENCE.md` §2 |
| 10 | ST05–ST07 integration plan | **DONE (plan)** | `STORY_TO_WORLD_INTEGRATION.md` §4 |
| 11 | Production breakdown (deliverables, owners, dependencies, acceptance) | **DONE (plan)** | §"Production breakdown" below |
| 12 | Phased implementation plan (into Unreal, playable) | **DONE (plan)** | §"Phased execution" below |

---

## World identity: the Ọmà Ala

**Name:** Ọmà Ala — "the land of the Ọmà" (Ọmà = the region's principal river; Ala = earth/land). The people call their world by the river that threads through it.
**Geographical basis:** The forest–savanna transition of the Igbo homeland (southeastern Nigeria), centred on a river system analogous to the Anambra/Idemili/Niger riverine ecology — rainforest and derived savanna, fertile plains, wetlands, low hills, and a major river that is the region's trade and transport spine. (See `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` for the documented references and the creative adaptations.)
**Why this region:** It supports every worldbuilding requirement the story needs — river transport and fishing, forest resources and danger, fertile yam/cassava/palm farmland, craft specialisation, a 4-day market network, a documented calendar, and the ecological variety for weather/seasonal change. It is a region, not a compound.

---

## Production breakdown (deliverables, owners, dependencies, acceptance)

| Deliverable | Owner | Depends on | Acceptance criteria |
|---|---|---|---|
| Regional map (master + settlement maps) | Design / World-Level | Research, canon reconciliation | Map places all settlements, routes, water, forest, story locations; coherent distances; reviewed by Story |
| Geographical atlas (IDs, coords, elevation, biome) | Design | Master map | Every location has ID, coords, elevation, biome, access, neighbours |
| Settlement & landmark register | Design | Master map | Every settlement/landmark has population, occupation, routes, market day |
| Population model & NPC categories | Design + Eng | Settlement register | Persistent population with homes/occupations/routines; 3-tier fidelity budget defined |
| Market network & schedules | Research + Design | Calendar, settlements | Each market has a day, products, attendees, identity; 4-day cycle verified |
| Calendar & seasonal model | Research | Market network, climate research | 13-month calendar; market-day progression; rainy/dry model internally consistent |
| Weather system | Eng | Seasonal model | Rain/storm/cloud/mud/vegetation/water-level change; NPC routine response |
| Travel & exploration | Design + Eng | Map, distances | Believable routes/distances; journeys with reasons; no "2-minute" world |
| NPC simulation & streaming | Eng | Population model, perf budget | Named/crowd/background tiers; streaming; crowd density by location/time/event |
| ST05–ST07 integration | Story + Design | Population, calendar, weather | Scenes emerge from the world, not isolated crowds |
| Story-to-world integration register | PM + Story | All above | Every chapter/scene/character/location placed; contradictions flagged |
| Engineering world specification | Eng | All | Coordinate system, streaming zones, systems, perf targets; usable by Eng |
| Source & evidence register | Research | All | Every decision tagged documented/adapted/fictional/unresolved with citations |

## Phased execution (get the world into Unreal and playable)

**Phase 0 — World plan (this blueprint).** Complete. Approved world specification, maps, registers.

**Phase 1 — First playable region (proves the architecture).** Build **one coherent geographical region** — the **Ọmà valley core** (Ahanwụ village + Ọmà Ukwu town + the connecting river/road + one forest + one market day) — fully in Unreal. Must demonstrate: connected settlements, believable travel, a working population (persistent + event surges), a working market-day cycle with real activity, weather/seasonal change, interconnected economy, and story locations integrated. **This is the gate:** the world systems must actually work playably before expansion. Owner-Mac playable evidence required.

**Phase 2 — Regional expansion.** Apply the proven architecture to the remaining settlements, markets, forest/river biomes and chapter locations, region by region.

**Phase 3 — Full world integration.** All 8 chapters placed in the coherent geography; Ancestral Realm integrated as its established narrative space; full population/calendar/weather live across the region.

**Phasing is NOT permission to shrink the world.** The complete Ọmà Ala plan is the target; phasing is the order of construction. The first playable region must demonstrate the intended systems at full ambition, not a reduced version.

## LOW / MEDIUM / HIGH density

These are offered **only as technical performance comparisons**, not as permission to reduce world ambition. The world ambition is the **HIGH** profile (a genuinely populated region). Engineering solves the technical problem (streaming, LOD, instancing, background simulation) to deliver the HIGH profile within performance budgets — performance is not a reason to design an empty world.

| Profile | Population density | Use |
|---|---|---|
| LOW | Sparse — minimum to avoid emptiness | Performance fallback / debug only |
| MEDIUM | Moderate — believable but reduced | Intermediate build / weak hardware |
| **HIGH (target)** | Full regional population with event surges | The intended world |

## Department responsibilities (one game, one world)

- **PM:** owns this blueprint; reconciles with the roadmap; assigns deliverables/owners/dependencies; sets acceptance criteria; prevents undersized assumptions; maintains the central world canon & decision register.
- **Research / Cultural Review:** geographical, cultural, historical, architectural, agricultural, economic evidence; verify market-day arrangements & seasonal patterns; distinguish documented vs adapted; flag items needing cultural review (especially sacred places, deities, masquerade).
- **Design / World-Level:** actual regional map, settlement layouts, world scale, environment composition, populated settlements/markets/roads/public spaces; real maps and production-ready layouts, not only descriptions.
- **Engineering:** world streaming, population simulation, crowd management, time, calendar, market activity, weather; reuse existing Unreal project where appropriate; realistic performance targets; **prove systems in a playable environment**.
- **Story:** geographical/character/activity/event consistency with canon; where world systems support storytelling without inventing unsupported lore.

## Acceptance standard (the world must be playable, not just documented)

Completion requires **implementation, integration and playable evidence** — not a map document, an NPC count, or a weather description. The world is accepted when, in a real playable build:
1. Entering a settlement reads as a place people actually live (persistent population, routines, homes).
2. Travelling to a market on its scheduled day yields a genuinely busy market (traders, stalls, goods, activity).
3. Settlements differ in identity, size, economy and activity.
4. The environment changes as time, weather and seasons progress.
5. The player has reasons to explore beyond the immediate mission.
6. Every chapter/scene is placed in the coherent geography and feels part of one world.

**Status of this document:** Plan complete (deliverables 1–12 authored). **Implementation: NOT STARTED.** The next action is Phase 1 — build the first playable Ọmà-valley region in Unreal with owner-Mac playable evidence.
