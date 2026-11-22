# TDD Phase 1 — Ọmà-valley Core: First Report

**Document ID:** TDD-IMPL-PHASE1-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM / Engineering. **Status:** **FIRST REPORT — audit, architecture, files, dependencies, sequence.** Implementation follows this report.
**Parent plan:** `docs/06_IMPLEMENTATION/WORLD/WORLD_SCALE_AND_LIVING_WORLD_BLUEPRINT.md` (TDD-IMPL-WORLD-001).
**Acceptance gate:** integrated build launchable/playable on owner Mac — NOT "assets authored."

---

## 1. Existing-project audit (actual repository state)

Two real Unreal projects exist. **The Phase-1 integration target is the Phase-3 `TDD_GAME` playable project** — it is the project the owner builds and plays, and it already contains the reusable scaffold the world systems must extend.

### 1.1 Root project — `TheDisobedientDaughter.uproject` (module `TheDisobedientDaughter`, UE 5.8, Mac+Windows)

Real systems present (single module):
- **Player/character:** `TDDAdannaCharacter`, `TDDPlayerController`, `TDDCharacterStateComponent`.
- **GameMode:** `ATDDGameMode` — encounter state machine (Active→Victory/Defeat→restart).
- **Traversal:** `UTDDTraversalComponent` (capsule-safe vault/drop; Agent 1 movement authority).
- **AI/Combat:** `TDDCombatBrainComponent`, `TDDBossPhaseComponent`, `TDDCombatDirectorSubsystem`, `TDDTrainingEnemy/Boss`, `TDDCombatComponent`.
- **Lighting:** `TDDLightingStateSwitcher`.
- **Engine-agnostic core headers:** `TDDChapterRoute.h` (chapter-layout validation, pure C++ stdlib), `TDDCombatTiming.h`, `TDDDamageMath.h`, `TDDGaitMath.h`, `TDDInputBuffer.h`, `TDDSeedRandom.h`, `TDDStateRules.h`, `TDDTraversalFallback.h`.
- **Tests:** `TDDProjectFoundationTests`, `TDDPlayableCharacterTests`, `TDDGameModeEncounterTests`, `TDDCameraTests`, `TDDAIIntegrationTests`, `TDDDodgeDistanceMathTests`, `TDDLightingStateTests`.
- **Tools/unreal:** `build_chapter1_greybox.py`, `import_ch01_compound_v2.py`, `build_ch01_lighting_states.py`, `create_root_mother_phase_asset.py`, etc.
- **Agent-side pure-logic test runner:** `Tools/tests/pure/run_pure.sh` (compiles `Tests/Standalone/**/*Tests.cpp` with `g++ -std=c++20`, no UE).

**No `.umap` in the root project** — it is the code-foundation project, not the playable build target.

### 1.2 Phase-3 project — `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/TDD_GAME.uproject` (module `TDD_GAME`, UE 5.8, Mac, PythonScriptPlugin)

**The playable project the owner builds.** Reusable scaffold:
- **World-data pipeline:** `scripts/generate_ue_world_data.py` reads `world.json` → emits `Source/TDD_GAME/Public/TDDWorldData.h` (waypoints/obstacles/interactions). **This is the pattern Phase 1 reuses.**
- **Runtime procedural level:** `ATDDForbiddenForestLevel` — builds a route/forest/landmarks blockout with `UInstancedStaticMeshComponent` + engine basic shapes, deterministic seed. **This is the level-construction pattern Phase 1 reuses.**
- **GameMode:** `ATDDForbiddenForestGameMode` — sets `DefaultPawnClass`, spawns the level.
- **Proxy character:** `ATDDAdannaProxyCharacter` — rigid-part technical proxy (CharacterMovement, spring-arm camera, input, route progress).
- **Build:** `TDD_GAME.Build.cs` (Core, CoreUObject, Engine, InputCore); `TDD_GAME.Target.cs` (V7, Unreal5_8, Mac).

### 1.3 World-architecture spec (`WORLD_ARCHITECTURE.md`, TDD-WARCH-001)

The contract classes (`UTDDLocationRegistry`, `UTDDEnvironmentStateSubsystem`, `ATDDNamedNPC`, `UTDDCrowdSubsystem`, `ETDDAccessLevel`, `FTDDStreamingBudget`, five-tier NPC model NAMED/CROWD/SCRIPTED/BACKGROUND/NONE) are **specified but explicitly "None of these are implemented."** Phase 1 begins their implementation against the playable project.

### 1.4 What is reused vs. created

| Reuse | Why |
|---|---|
| `TDDWorldData.h` generator pattern (`world.json → header`) | Authored, deterministic world data |
| `ATDDForbiddenForestLevel` instancing/blockout pattern | Builds the Ọmà-valley geography without hand-placed assets |
| `ATDDAdannaProxyCharacter` | Playable character for playable evidence |
| `ATDDForbiddenForestGameMode` GameMode pattern | Wires subsystems + spawns the level |
| `run_pure.sh` + `Tests/Standalone/` pattern | Agent-side logic verification without UE |
| WORLD_ARCHITECTURE contracts (class names, tiers, budgets) | Implement against the established spec |

| Create | Why |
|---|---|
| Engine-agnostic world-logic core `TDDWorldLogic.h` | Calendar, market-day, population density, route, weather logic — testable in-sandbox, consumed by UE |
| UE subsystems (location registry, population, calendar, market, weather) | The WORLD_ARCHITECTURE systems, implemented |
| NPC/market/settlement actors | The living-world visual + behavioural layer |
| `ATDDOmegaValleyLevel` + `ATDDOmegaValleyGameMode` | The Phase-1 Ọmà-valley core |

---

## 2. Proposed Unreal implementation architecture

**Design principle: logic is data + pure computation; the UE layer is a thin, streaming, render-aware shell over a logical simulation that is independent of how many NPCs are rendered.**

### 2.1 Two-layer architecture

```
┌─────────────────────────────────────────────────────────────┐
│  LOGICAL LAYER  (TDDWorldLogic.h — pure C++, UE-free)        │
│  Igbo calendar · market-day · population density model ·     │
│  route/distance · wet/dry weather model · settlement data    │
│  → TESTED in-sandbox via run_pure.sh (g++)                   │
└─────────────────────────────────────────────────────────────┘
                            │ consumed by
┌─────────────────────────────────────────────────────────────┐
│  UE LAYER  (TDD_GAME module)                                 │
│  UTDDLocationRegistry · UTDDWorldPopulationSubsystem         │
│  UTDDCalendarSubsystem · UTDDMarketSubsystem · UTDDWeather   │
│  Subsystem · ATDDNamedNPC · ATDDPopulationActor              │
│  ATDDMarketStall · ATDDSettlementZone · ATDDOmegaValleyLevel │
│  ATDDOmegaValleyGameMode                                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Logical population independent of rendering

- `UTDDWorldPopulationSubsystem` maintains the **full logical population** (every household/occupation/routine/destination for every settlement) as data + computation. This population **exists whether or not its actors are rendered**.
- Rendering activation is a separate, distance-based concern: the subsystem computes, per settlement and per event, the **target active tiers** (NAMED / CROWD / SCRIPTED / BACKGROUND counts) from the density model; the level spawns/despawns actors to match. **Demonstration: the logical population is queryable/loggable at full regional scale while only a budgeted subset of actors is spawned.**
- Density scales by **location, date (market day), time-of-day, and event** — computed in the logic layer, applied by the UE layer.

### 2.3 Market cycle

- `UTDDCalendarSubsystem` advances the Igbo 4-day week (Eke/Orie/Afo/Nkwo) and computes each settlement's market day.
- `UTDDMarketSubsystem` activates the correct settlement's market on its day: spawns traders/stalls/goods, applies the density surge, sets goods/prices. **No silent market-day assignments** — the Ọmà-Ukwu=Eke assignment is the proposed regional arrangement from the blueprint; flagged for Story/Research confirmation (the source register already marks it `[A]` adaptive).

### 2.4 Weather & seasonal consequences

- `UTDDWeatherSubsystem` drives wet/dry progression and observable consequences (mud/path condition, river water level/crossing, visibility, vegetation state, NPC clothing/activity). **Not just a sky change.**

### 2.5 Story/canon integration

- CH01 Home Settlement = **Ahanwụ**; ST05 (rain) / ST06 (market day) / ST07 (gathering) draw from the world weather/market/population systems, not isolated crowds.
- Canon (Adanna/Nneka/Ezeani, Ancestral Realm narrative status, Ch.2 no-living-flame) is preserved; the world layer does not alter it.

---

## 3. Exact files / assets / systems to create or modify

### Create — engine-agnostic logic core (testable in-sandbox)
| File | System |
|---|---|
| `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Source/TDD_GAME/Public/TDDWorldLogic.h` | Igbo calendar, market-day, population-density model, route/distance, weather/season model, settlement data — pure C++20, UE-free |
| `Tests/Standalone/TDDWorldLogicTests.cpp` | Agent-side tests for the logic core (g++ via `run_pure.sh`) |

### Create — UE subsystems (TDD_GAME)
| File | System |
|---|---|
| `Public/TDDLocationRegistry.h` + `Private/TDDLocationRegistry.cpp` | `UTDDLocationRegistry` (UWorldSubsystem) — settlement/location registry |
| `Public/TDDWorldPopulationSubsystem.h` + `.cpp` | `UTDDWorldPopulationSubsystem` — logical population sim + tier density |
| `Public/TDDCalendarSubsystem.h` + `.cpp` | `UTDDCalendarSubsystem` — Igbo calendar + market-day progression |
| `Public/TDDMarketSubsystem.h` + `.cpp` | `UTDDMarketSubsystem` — market-day activation + density surge |
| `Public/TDDWeatherSubsystem.h` + `.cpp` | `UTDDWeatherSubsystem` — wet/dry seasonal model + consequences |

### Create — actors & level (TDD_GAME)
| File | System |
|---|---|
| `Public/TDDNamedNPC.h` + `.cpp` | `ATDDNamedNPC` (Tier NAMED — routine/dialogue hook) |
| `Public/TDDPopulationActor.h` + `.cpp` | `ATDDPopulationActor` (Tier CROWD/SCRIPTED/BACKGROUND, parameterised) |
| `Public/TDDMarketStall.h` + `.cpp` | `ATDDMarketStall` (stall + goods) |
| `Public/TDDSettlementZone.h` + `.cpp` | `ATDDSettlementZone` (settlement footprint/anchor) |
| `Public/TDDOmegaValleyLevel.h` + `.cpp` | `ATDDOmegaValleyLevel` — builds Ahanwụ + Ọmà Ukwu + river/road + forest + market |
| `Public/TDDOmegaValleyGameMode.h` + `.cpp` | `ATDDOmegaValleyGameMode` — wires subsystems, spawns level |

### Create — world data
| File | System |
|---|---|
| `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/omega_valley.json` | Ọmà-valley core data (settlements, routes, markets, population, calendar) |
| `scripts/generate_omega_valley_data.py` | `omega_valley.json → TDDOmegaValleyData.h` |
| `ue_project/Source/TDD_GAME/Public/TDDOmegaValleyData.h` | Generated world data header |

### Modify
| File | Change |
|---|---|
| `ue_project/Source/TDD_GAME/TDD_GAME.Build.cs` | No new module deps required (logic core is header-only; subsystems use Engine). Verified unchanged unless Mass is adopted — Phase 1 uses instancing, not Mass. |
| `Tools/tests/pure/run_pure.sh` | Add the Phase-3 `Public` include path so the world-logic tests compile under the existing runner. |

---

## 4. Dependencies

| Dependency | Status | Resolution |
|---|---|---|
| WORLD_ARCHITECTURE contract (class names/tiers/budgets) | Present (spec) | Implement against it |
| Phase-3 playable project scaffold | Present | Reuse |
| Pure-logic test runner | Present | Extend include path |
| Market-day assignments (Ọmà Ukwu=Eke etc.) | **Proposed [A]** | Flagged for Story/Research confirmation — not silently fixed; data-driven so it can change without code change |
| Sacred-place specifics | **Unresolved [U]** | No sacred sites authored in Phase 1 core beyond a restrained shrine-grove reference; cultural review before any sacred content |
| UE 5.8 compile/run | Owner Mac | Sole build/runtime authority; agent authors, owner builds/plays |
| g++ for pure-logic tests | Present in sandbox | Agent-side verification |

## 5. Sequenced execution plan

1. **Logic core** (`TDDWorldLogic.h`) + **pure tests** → compile + run green in-sandbox (calendar, market-day, density, route, weather).
2. **World data** (`omega_valley.json` + generator + `TDDOmegaValleyData.h`) for the Ọmà-valley core.
3. **UE subsystems** (registry, population, calendar, market, weather) consuming the logic core.
4. **Actors + level + GameMode** — build the Ọmà-valley core (Ahanwụ, Ọmà Ukwu, river/road, forest, market) and wire the subsystems.
5. **Integration pass** — subsystems drive the level; market/population/weather observable.
6. **Evidence** — pure-test results (in-sandbox, real) + a build/run procedure + known-limitations list for owner-Mac acceptance.

**Honest status:** This report is the pre-implementation plan. Logic-core tests will be real, executed in-sandbox. UE C++ is authored but **not compiled here** (no UE in sandbox) — it is `IMPLEMENTED_UNVERIFIED` until owner-Mac builds/plays. No planned or stubbed system will be reported as completed.
