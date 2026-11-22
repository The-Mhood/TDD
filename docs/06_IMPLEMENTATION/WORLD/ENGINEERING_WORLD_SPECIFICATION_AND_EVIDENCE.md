# TDD — Engineering World Specification & Evidence

**Document ID:** TDD-IMPL-WORLD-005 · **Version:** 1.0 · **Date:** 2026-11-21
**Companion to:** `WORLD_SCALE_AND_LIVING_WORLD_BLUEPRINT.md` (TDD-IMPL-WORLD-001), `WORLD_GEOGRAPHY_SETTLEMENTS_POPULATION.md` (TDD-IMPL-WORLD-002), `WORLD_CALENDAR_ECONOMY_WEATHER_WILDLIFE.md` (TDD-IMPL-WORLD-003)
**Owner:** Engineering (build) — PM (acceptance). **Sole build/runtime verification:** owner Mac (UE).

> **Standing constraint:** Performance limits are **NOT** an excuse for an empty world. The HIGH population profile is the target; the technical problem is solved. This document defines how.

---

## 1. Coordinate system & world data

- **World frame:** a single global coordinate space for the ~18×14 km region. Origin at the Ọmà River crossing below Ahanwụ. Units: centimeters (Unreal standard); the map's "km" distances map to real traversal distances.
- **Settlement anchors:** each settlement has a fixed world anchor (the `ama` square / dock / gate) used as its streaming center and population spawn root.
- **World data:** all geography, settlements, landmarks, routes, markets, calendar and population data stored in **data assets / tables** (not hardcoded), editable by Design. IDs follow the `TDD-WORLD-*` scheme; existing chapter/location IDs (Drive registers) are preserved and mapped to world coords.
- **Reuse:** reuse the existing Unreal project foundation (`docs/06_IMPLEMENTATION/UNREAL_PROJECT_FOUNDATION_V1.md`); world systems are added on the existing hierarchy (`ETDDChapter`, `UTDDLocationRegistry`, `UTDDEnvironmentStateSubsystem`).

## 2. NPC simulation & performance architecture

### 2.1 The three-tier NPC model (from `WORLD_ARCHITECTURE.md`, scaled to region)

A settlement's population is **NOT** 68+ hand-placed full-AI actors. It is a **population simulation** with three tiers:

| Tier | What it is | AI/animation cost | Count basis |
|---|---|---|---|
| **Tier 1 — Named actors** | High-fidelity, individual NPCs with names, personalities, relationships, full AI + animation | Full AI, full animation | Curated set (hand-authored key NPCs per settlement + story-relevant) |
| **Tier 2 — Crowd** | Medium-fidelity NPCs forming crowds; simplified AI, shared/instanced animation | Simplified AI, instancing | Generated per settlement population; surge on market/event |
| **Tier 3 — Background** | Background actors needing **no AI**; ambient life (cooking, sweeping, sitting, walking simple loops) | No AI, minimal animation | Largest count; scales with population |

**Population simulation is independent of rendering.** The simulated population (who lives where, their routines, destinations) runs as a **logical population system**; rendering activates only the tiers within activation range. The population exists whether or not actors are rendered.

### 2.2 Streaming & spatial activation

- **Settlement streaming zones:** the region is divided into streaming zones (one per settlement + wilderness chunks). Actors activate/deactivate based on the player's position and the active zone.
- **Distance-based AI/animation LOD:**
  - Tier 1 (named): full AI + full animation when near; reduced tick / abstracted state when far.
  - Tier 2 (crowd): simplified AI when near; frozen/abstracted when far.
  - Tier 3 (background): no AI; animation LOD (full → simplified → static billboard/instancing) by distance.
- **Spatial activation:** actor activation radius scales with population density and the active event (market day expands the market-zone activation radius).

### 2.3 Crowd instancing & background population sim

- **Crowd instancing:** Tier 2 crowd actors rendered via **instancing** (hierarchical instanced static mesh / instancing) for stalls, queues, market groups; the crowd is authored as instanced groups that spawn/densify on market days.
- **Background population sim:** Tier 3 background actors run a **background population simulation** — they follow routines (go to field, go to well, sit, cook, sweep, walk loops) as lightweight logic, with no AI decision-making and minimal animation cost. The number and activity of background actors reflect the settlement's population and the time of day.

### 2.4 Crowd density scaling

Crowd density scales by **location, date, time, and events**:

| Factor | Effect |
|---|---|
| **Location** | Ọmà Ukwu market-town = high baseline; dispersed hamlets = low |
| **Date (market day)** | On the settlement's market day, market-zone density surges (Tier 2/3 influx) |
| **Time of day** | Dawn set-up → midday peak → evening dispersal for markets; routines shift |
| **Event** | Festival (Iri Ji), gatherings, story events add targeted surges |

The population system computes the target density for the active location/time and spawns/despawns tiers accordingly. This is the mechanism that makes "travel to a scheduled market and find a genuinely busy market" true, without spawning 8,850 full-AI actors.

### 2.5 Performance budgets (technical comparison — not a quality limit)

The target is the **HIGH** profile. Budgets are set to achieve HIGH within the target hardware (owner Mac M4/16GB as the reference; lower-end as fallback).

| Metric | LOW (fallback) | MEDIUM | HIGH (target) |
|---|---|---|---|
| Visible NPC actors (Tier1+2) near player | ~30 | ~80 | ~150–200 |
| Background actors (Tier3, instanced) | ~60 | ~200 | ~500–700 |
| Simulated population (logical, all tiers) | full regional (~8,850) | full regional | full regional |
| Crowd instancing | on | on | on |
| AI ticks (tiered/LOD) | aggressive | standard | standard+ |

**The simulated population is always the full regional figure** regardless of profile; only the *rendered/activated* actor count differs. This is how the world is "genuinely populated" at HIGH while remaining performant.

## 3. Time, calendar & market systems

- **World clock:** drives the Ọgụàfọ̀ calendar (Eke/Orie/Afo/Nkwo 4-day week; 13-month year), the day/night cycle, and the seasonal model. The clock is the single source of truth; weather and markets read from it.
- **Calendar system:** data-driven; computes the current `ubochi`, the market day per settlement, the season, and the agricultural phase.
- **Market system:** when the player is near a settlement on its market day, the market-zone activates: stalls populate, traders/customers spawn (tiered density), goods/prices are set, events/info available. On a non-market day, the same zone shows ordinary stalls/routines. Market identity (products, layout, scale) is per-settlement data.
- **Market-in-rain vs market-in-dry:** the market system reads the weather system to alter stalls (cover), ground (mud), crowd behaviour, and goods protection — so the same market day differs by weather.

## 4. Weather & environment system

- **Weather system:** a data-driven seasonal/weather model. Rainfall, clouds, storms, mud, water levels, vegetation state, and NPC clothing/activity all derive from it.
- **Seasonal progression:** rainy/dry model drives river/floodplain water levels, farm growth, visibility, path conditions, and vegetation.
- **Environment state subsystem:** reuse `UTDDEnvironmentStateSubsystem` (existing) for environment-state refs; weather/season drive environment state changes.
- **Persistence:** weather and season progress with the world clock; the environment visibly changes between visits.

## 5. Travel & exploration systems

- **Routes & distances:** routes (footpaths, canoe routes) authored as navigation data; traversal distances from the atlas. Navigation mesh per settlement and per route.
- **Travel gameplay:** movement follows real routes; weather affects traversability (mud slows, high water breaks crossings → canoe required); no instant teleport between settlements.
- **Journey life:** routes carry ambient NPC traffic (farmers, traders, hunters) from the population system, so the journey is part of the world.

## 6. Story-world integration hooks

- **Scene placement:** every scene/location maps to a world coordinate + settlement catchment; scenes read the active population/calendar/weather state.
- **ST05/ST06/ST07:** Ahanwụ's village square population driven by the world systems (weather for ST05, market-day surge for ST06, assembly gathering for ST07) — not isolated crowds.
- **Environment-state & location registry:** reuse `UTDDLocationRegistry` / `ATDDChapterDirector`; chapters placed in the geography via the world data.
- **Protected domains:** Ch.2 dead-industrial compounds (no-living-flame), Ch.4 river deity domain, Ch.5 thunder domain, Ch.7 boundary place — separate environment states with their identities/restrictions preserved.

## 7. Phased implementation (playable evidence)

**Phase 0 — Plan (complete).** This specification + maps/registers.
**Phase 1 — First playable region (the gate).** Build the **Ọmà-valley core** (Ahanwụ + Ọmà Ukwu + connecting river/road + one forest + one market day) fully in Unreal. **Playable proof required:** connected settlements, believable travel, persistent+surge population, working market-day cycle, weather/seasonal change, interconnected economy, story locations. Owner-Mac playable evidence.
**Phase 2 — Regional expansion.** Apply the proven architecture to all settlements/markets/biomes/chapter locations, region by region.
**Phase 3 — Full integration.** All 8 chapters in the geography; Ancestral Realm as its narrative space; full population/calendar/weather live across the region.

**Playable evidence checklist (acceptance, real build):**
- [ ] Enter Ahanwụ → persistent population, routines, homes (believe people live there)
- [ ] Travel to Ọmà Ukwu on Eke → genuinely busy market (traders, stalls, goods, activity)
- [ ] Enter Ịbe / Ọnịcha / Ọba → distinct identity, size, economy, activity
- [ ] Observe environment change across weather/seasons; market-in-rain ≠ market-in-dry
- [ ] Travel a real route with journey life; destination reached by genuine traversal
- [ ] Chapters/scenes placed in the geography; ST05–ST07 draw from world systems
- [ ] Performance: HIGH profile holds within budget on reference hardware

**Status:** Specification complete. **Implementation NOT STARTED.** Owner-Mac is the sole build/runtime verification authority.

*End of TDD-IMPL-WORLD-005.*
