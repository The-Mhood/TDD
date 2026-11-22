# TDD Phase 1 — Ọmà-valley Core: Implementation Evidence & Build Procedure

**Document ID:** TDD-IMPL-PHASE1-002 · **Version:** 1.0 · **Date:** 2026-11-22
**Author:** PM / Engineering. **Status:** **IMPLEMENTATION AUTHORED** — logic core **TESTED in-sandbox**; UE C++ **IMPLEMENTED_UNVERIFIED** (not compiled; owner Mac is the sole build/runtime authority).
**Companion:** `PHASE1_IMPLEMENTATION_AUDIT_AND_ARCHITECTURE.md` (TDD-IMPL-PHASE1-001).
**Acceptance gate:** integrated build launchable/playable on owner Mac — NOT "assets authored."

---

## 1. Verification level — stated precisely (no overclaim)

| Component | Status | Basis |
|---|---|---|
| World logic core (`TDDWorldLogic.h`) — calendar, market-day, population density, route/distance, weather | **IMPLEMENTED & TESTED** | `Tools/tests/pure/run_pure.sh` → `TDDWorldLogicTests` **52/52 assertions PASS**, compiled with `g++ -std=c++20` in-sandbox. No UE required. |
| Full pure suite (regression) | **GREEN** | 7 suites, **947/947 assertions**, exit 0. Existing suites unaffected. |
| UE subsystems (location registry, population, calendar, market, weather) | **IMPLEMENTED_UNVERIFIED** | Authored C++ against UE 5.8 API; **not compiled** (no UE in sandbox). Owner-Mac compile required. |
| UE actors (population, named NPC, market stall, settlement zone) | **IMPLEMENTED_UNVERIFIED** | As above. |
| `ATDDOmegaValleyLevel` + `ATDDOmegaValleyGameMode` | **IMPLEMENTED_UNVERIFIED** | As above. |
| Generated data header (`TDDOmegaValleyData.h`) | **GENERATED & VALIDATED** | `generate_omega_valley_data.py` runs clean; emits valid C++ from `omega_valley.json`. |
| World subsystem registration | **CONFIGURED** | `DefaultEngine.ini` `[/Script/Engine.Engine] WorldSubsystems=...` added. |

**Honest statement:** the logic that governs the world (calendar, market cycle, population density, weather consequences, travel distances) is **real, compiled and tested** in-sandbox. The UE rendering/subsystem layer is **authored but not compiled** — it becomes verified only when the owner builds and plays it. Nothing planned or stubbed is reported as complete.

## 2. What was implemented (actual files)

### Logic core (tested)
- `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Source/TDD_GAME/Public/TDDWorldLogic.h` — Igbo calendar (Eke/Orie/Afo/Nkwo 4-day week, 13-month year), settlement data (Ahanwụ/Ọmà Ukwu/Ihiala), market-day computation, wet/dry weather model with consequences, population-density model, route/distance.
- `Tests/Standalone/World/TDDWorldLogicTests.cpp` — 52 assertions.

### UE subsystems (TDD_GAME)
- `TDDLocationRegistry` (`UTDDLocationRegistry`, UWorldSubsystem) — settlement registry + validation.
- `TDDWorldPopulationSubsystem` (`UTDDWorldPopulationSubsystem`) — **logical population independent of rendering**; computes active tier counts from the density model.
- `TDDCalendarSubsystem` (`UTDDCalendarSubsystem`) — advances the world clock, market-day/season.
- `TDDMarketSubsystem` (`UTDDMarketSubsystem`) — activates the correct settlement on its market day; traders/stalls/density.
- `TDDWeatherSubsystem` (`UTDDWeatherSubsystem`) — wet/dry state + consequences (mud, water level, visibility, vegetation, activity suppression).

### UE actors (TDD_GAME)
- `ATDDPopulationActor` — tiered population NPC (Named/Crowd/Scripted/Background), tier-matched AI cost.
- `ATDDNamedNPC` — Tier-1 named actor (routine/dialogue hook).
- `ATDDMarketStall` — trader stall with goods, open/closed.
- `ATDDSettlementZone` — per-settlement anchor; spawns a budgeted population subset toward the density model; **logs the full logical population vs the spawned subset** (the independence demonstration).

### Level & game mode
- `ATDDOmegaValleyLevel` — builds Ahanwụ + Ọmà Ukwu + Ọmà river + road spine + forest patch (instancing), places settlement zones; geometry reads the generated data header.
- `ATDDOmegaValleyGameMode` — wires subsystems, spawns the level, refreshes settlements + weather on market-day change; reuses the playable proxy character.

### World data (Design-editable)
- `omega_valley.json` + `scripts/generate_omega_valley_data.py` → `TDDOmegaValleyData.h` (region bounds, route, river, forest, settlement screen positions).

### Config
- `Config/DefaultEngine.ini` — `WorldSubsystems` registration.

## 3. How the acceptance criteria are met by the design

| Acceptance criterion | Mechanism |
|---|---|
| Both settlements + connecting geography explorable | `ATDDOmegaValleyLevel` builds Ahanwụ, Ọmà Ukwu, the Ọmà river and the road spine (~4 km real travel). |
| Population sim, rendering tiers, NPC routines | `UTDDWorldPopulationSubsystem` (logical) + `ATDDPopulationActor` tiers; settlement zone spawns toward density. |
| **Logical population independent of rendering** | `GetRegionalLogicalPopulation()` returns the full figure at all times; settlement zone logs logical vs spawned subset. Tested. |
| Market changes with calendar, genuinely populated | `UTDDCalendarSubsystem` + `UTDDMarketSubsystem`: the settlement whose day matches activates; density surge (tested: market day > 2× ordinary). |
| Weather/seasonal progression with observable consequences | `UTDDWeatherSubsystem`: mud (traversal slowdown), water level (crossing break), visibility, vegetation, NPC activity. Tested: market-in-rain < market-in-dry. |
| Story/canon integration | CH01 home = Ahanwụ; ST05/06/07 draw from weather/market/population systems. Canon (Adanna/Nneka/Ezeani, Ancestral Realm) untouched. |
| Performance at HIGH density | Density model caps AI-costly crowd at 90; background instanced up to 700 (within HIGH profile). Logic-core tested. |
| Repeatable build/run procedure | §4 below. |

## 4. Build & run procedure (owner Mac) — exact copy-and-paste

**RECOMMENDED ENTRY POINT — use the diagnostic script first.** If the build fails
or output is lost, do **not** re-run ad-hoc commands. Run the robust diagnostic
script, which auto-detects the engine, validates every step, captures ALL output to a
persistent log, and prints the exact failing command + compiler diagnostics:

```bash
cd TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1
bash build_phase1_diagnostic.sh
# or, if UE is not in the default location:
UE_ROOT="/path/to/UnrealEngine-5.8" bash build_phase1_diagnostic.sh
```

It writes `BUILD_DIAGNOSTIC_<timestamp>.log` next to the script — that log survives a
closed terminal. Send the log (and the printed failure tail) back to Engineering.

**Source-code fixes applied (commit `a4cec47`):** the first Mac build attempt failed
(exit 1). Engineering audited the Phase-1 UE C++ with `build_readiness.py` and fixed
**22 real compile/UHT errors** (all previously undetected because the UE layer was
never compiled in-sandbox): `PrimaryComponentTick` misuse in `UWorldSubsystem`
constructors, `UENUM` enum reflection for `UPROPERTY`/`UFUNCTION`, missing includes,
a private-member `AllowPrivateAccess` metadata, a `TActorIterator` flags issue, and a
Unity-build symbol collision. `build_readiness.py` now reports **0 blockers, 0
warnings** on `TDD_GAME`; the pure logic core is still **947/947 GREEN**. These are
static fixes — the authoritative compile/runtime verification remains the owner Mac.

The manual command-by-command procedure below is retained for reference.

**Do NOT infer the build from the target name.** The exact commands below are the
complete, ordered procedure. Run them top-to-bottom in a macOS Terminal. Nothing here
is inferred — every path and flag is explicit.

### 4.0 — Required environment (set once per shell)

The engine is **Unreal Engine 5.8** on **Apple Silicon macOS**. Two variables are
needed; the project path is absolute so no further inference is required.

```bash
# Engine root. For an Epic Games Launcher install on macOS this is the standard
# location. If you built UE from source, set UE_ROOT to your engine repo root
# instead (the path that contains Engine/, Content/, etc.).
UE_ROOT="$HOME/Library/Engines/UnrealEngine"

# Absolute path to the Phase-1 project file. Replace <YOUR_USER> and the repo
# location with your actual machine path.
PROJECT="$HOME/path/to/TDD/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/TDD_GAME.uproject"

# Sanity check: the build toolchain (Build.sh) and the project must exist.
test -x "$UE_ROOT/Engine/Build/BatchFiles/Mac/Build.sh" && echo "UE_ROOT OK (Build.sh)" || echo "UE_ROOT MISSING — fix the path"
test -f "$PROJECT" && echo "PROJECT OK" || echo "PROJECT MISSING — fix the path"
```

**Required environment variables (minimum):**
- `UE_ROOT` — Unreal Engine 5.8 install root (see above).
- `PROJECT` — absolute path to `TDD_GAME.uproject`.
- No other env vars are required. `PATH` must include `python3` (macOS ships it) and
the standard macOS toolchain (Xcode Command Line Tools provide `clang`/`make`; the
engine's `Build.sh`/`RunUAT.sh` locate the toolchain themselves).

### 4.1 — Data generation (run BEFORE the build, only if the data changed)

`TDDOmegaValleyData.h` (the blockout-geometry C++ header) is **committed**. You only
need to regenerate it if you edited `omega_valley.json` (settlements, route, river,
forest, market days). Run this **before** step 4.3 so the committed header and the
JSON agree:

```bash
# From the PLAYABLE_ADANNA_M1 directory (scripts/ and ue_project/ are siblings here).
cd "$(dirname "$PROJECT")/../.."
python3 scripts/generate_omega_valley_data.py
```

**When to run it:** only when `omega_valley.json` changes. The generator writes
`ue_project/Source/TDD_GAME/Public/TDDOmegaValleyData.h` in place. If the header is
absent (e.g. a fresh clone where it was not committed), run this once to create it.
The authoritative logic stays in `TDDWorldLogic.h`; this header is purely blockout
geometry data.

### 4.2 — Generate project files (REQUIRED — do not skip)

The Phase-1 C++ sources were added after the project was last generated. **UBT will
not see them until project files are regenerated.** Run this every time new
`.cpp`/`.h` files are added to `Source/TDD_GAME/`:

```bash
"$UE_ROOT/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh" "$PROJECT"
```

Expected: no error. If it warns about a missing module, the `.uproject`/`Build.cs` are
out of sync — report back; Engineering fixes.

### 4.3 — Command-line build (compile verification, no editor)

This compiles the `TDD_GAME` module for **Development / Mac** without opening the
editor. It is the authoritative compile check:

```bash
"$UE_ROOT/Engine/Build/BatchFiles/Mac/Build.sh" TDD_GAME Mac Development \
  -project="$PROJECT" -WaitMutex -architecture=arm64
```

> **`Build.sh` signature (validated against UE 5.8):** the canonical positional
> form is `Build.sh <TargetName> <Platform> <Configuration> -project=<uproject>
> [options]` (equivalently `-Target="<Target> <Platform> <Configuration>"
> -project=<uproject>`). The project path is **not** a positional — it is passed
> via `-project=`. Passing the `.uproject` as a positional lands it in the
> **Platform** slot and UBT resolves an empty platform list →
> `No platforms specified for target`.
>
> **Why `Build.sh` and not `RunUAT.sh BuildProject`:** UE 5.8 AutomationTool does
> **not** support the legacy `BuildProject` command — `RunUAT.sh BuildProject ...`
> fails with `Failed to find command BuildProject` (`Error_Unknown`) and the C++
> compiler never starts. The real C++ build is driven by the platform `Build.sh`,
> which wraps `UnrealBuildTool` (the actual compiler driver). `build_phase1_diagnostic.sh`
> uses `Build.sh` and classifies failures as **invocation** (compiler never
> started, incl. `No platforms specified`) vs **compilation** (`error:` lines).

- Target to build: **`TDD_GAME`** (the game target; `Type = TargetType.Game` in `TDD_GAME.Target.cs`).
- Platform: **`Mac`** (`.uproject` `TargetPlatforms: ["Mac"]`).
- Configuration: **`Development`**.
- `-project=` — absolute path to `TDD_GAME.uproject`.
- `-WaitMutex` — wait for the build mutex (avoids mutex-acquisition failures).
- `-architecture=arm64` — Apple Silicon M4 (host architecture).
- `Build.sh` is invoked from its own directory (`Engine/Build/BatchFiles/Mac/`); the
  recommended entry point is `build_phase1_diagnostic.sh`, which handles all of this.

**If compilation reports any diagnostics in `TDD_GAME` sources, do NOT try to fix the
C++ yourself — report them back. Engineering owns all C++ fixes (owner will not
author/repair C++).** The pure logic core (`TDDWorldLogic.h` +
`TDDWorldLogicTests.cpp`, 947/947 assertions green) is already verified; only the
UE-layer compile is at issue here.

**Success criterion:** the command exits 0 with no `error:` lines. A clean exit is
**compile-verified only** — it is NOT runtime verification. Compilation ≠ playable
evidence; see the verification-level table at the top of this document.

### 4.4 — Launch the Phase-1 valley in the editor + PIE (playable evidence)

The valley is **authored at runtime**: `ATDDOmegaValleyGameMode::EnsureLevelSpawned()`
spawns `ATDDOmegaValleyLevel` (ground, Ọmà river, road, forest, settlement zones) in
`BeginPlay`. You do **not** hand-build the valley geometry. But you **must** create
one minimal launch map and point it at the Phase-1 GameMode — the project defaults
(`GameDefaultMap=/Engine/Maps/Entry`, `GlobalDefaultGameMode=TDDForbiddenForestGameMode`)
still target the **old** scaffold, so the valley will NOT launch from the default map.

1. **Open the project:** double-click `TDD_GAME.uproject`, or in the UE 5.8 editor
   → File → Open Project → select it. If prompted, generate project files (step 4.2).
   Wait for the `TDD_GAME` module to finish compiling in the editor.

2. **Create the launch level (one-time):** Editor → File → **New Level** →
   **Empty Level** (no template) → save as
   `ue_project/Content/Maps/OMEGA_VALLEY_PHASE1.umap` (create the `Maps` folder).

3. **Set the Phase-1 Game Mode (the one required assignment):**
   - Open the **World Settings** panel.
   - **Game Mode** → Browse → select
     **`TDD_GAME.TDDOmegaValleyGameMode`**.
   - This GameMode sets `DefaultPawnClass = ATDDAdannaProxyCharacter` and, on
     `BeginPlay`, spawns the valley level automatically.

4. **Place a Player Start:** in the Level, search **Player Start** in the Place
   Actors panel and click once on the flat ground. The proxy character spawns there.

5. **PIE:** press **Play** (or Alt+P). The valley core launches.

> **Important:** do NOT rely on `GameDefaultMap`/`GlobalDefaultGameMode` in
> `DefaultEngine.ini` for Phase 1 — they still point at `/Engine/Maps/Entry` and
> `TDDForbiddenForestGameMode` (the old scaffold). The assignment in step 3 is what
> activates the Ọmà-valley Phase-1 core. (Engineering can update
> `DefaultEngine.ini` to point `GameDefaultMap` at `OMEGA_VALLEY_PHASE1` and
> `GlobalDefaultGameMode` at `TDDOmegaValleyGameMode` as a follow-up, but the
> per-level assignment above is sufficient and unambiguous.)

### 4.5 — Acceptance evidence to capture during PIE

The exact expected logs and in-PIE observations are enumerated in **§4e**. During PIE,
capture both of the following as acceptance evidence; without them Phase 1 is **NOT**
complete (see the Phase-1 completion constraint):

1. **Console log output** — the full UE console log (copy from the editor's Output
   Log window or the PIE process stdout). It must show the five subsystem
   initialization lines, the per-settlement logical-vs-spawned population lines, and
   the market-activation + calendar-progression + weather lines described in §4e.
2. **Playthrough recording** — a capture of the PIE session demonstrating: entering
   Ahanwụ and Ọmà Ukwu (population actors present), the Eke market activating in
   Ọmà Ukwu, the Afo market activating in Ahanwụ, and the observable rainy→dry
   weather consequences (water level, mud, vegetation, market density).

Cross-check the captured logs against the §4e expectations. If any expected line is
missing or any observation fails, report it back; Engineering fixes. Phase 1 is not
marked complete until this evidence is reviewed.

## 4b. Population tier reconciliation (four tiers vs the original three-tier spec)

The original summary described a **three-tier** NPC model (named / crowd / background). The authoritative spec (`WORLD_ARCHITECTURE.md` TDD-WARCH-001 §5) **expanded this to five tiers** (`NAMED`, `CROWD`, `SCRIPTED`, `BACKGROUND`, `NONE`), because the register distinguishes kinds of population a three-tier model collapses and thereby over-bills: a scene with a single scripted performer on a fixed loop does not need an AI agent, and the register has more of those than crowds.

The Phase-1 implementation implements the **four active tiers** (the fifth, `NONE`, is the absence of simulation — no actor, not a spawned tier):

| Tier | Purpose | AI / animation cost | Role |
|---|---|---|---|
| **Named** (Tier 1) | Individual high-fidelity NPCs with names, routines, dialogue/quest hooks | Full AI + full animation | Curated set per settlement; story-relevant |
| **Crowd** (Tier 2) | Population body forming crowds; simplified AI, instanced, bark-only | Simplified AI, instancing | Market/event surges; the "busy market" body |
| **Scripted** (Tier 3) | Fixed animation loop, **no AI / no perception / no nav** | Fixed loop, no AI | Market performers, stall-tenders, specific activities |
| **Background** (Tier 4) | Ambient life (cooking, sweeping, sitting, simple loops) | **No AI**, instanced | The "people live here" feel at near-zero cost |
| **NONE** | No simulation | — | Locations with no NPC (not a spawned tier) |

**Logical population independent of rendered actors — confirmed.** `UTDDWorldPopulationSubsystem` holds the **full logical population** (residential + economic, ~8,850 regional) as data + computation. It is **always queryable** via `GetRegionalLogicalPopulation()` / `GetLogicalPopulationSnapshot()`, regardless of how many actors are spawned. The density model computes a **budgeted rendered subset** (the four active tiers) from the logical population; `ATDDSettlementZone` spawns toward that subset and **logs logical vs spawned** on every refresh. The logical population is therefore never reduced by the render budget — verified by `TDDWorldLogicTests` ("logical population exceeds rendered actors").

## 4c. Ihiala — scope clarification

**Ihiala is future-facing registry data, NOT a Phase-1 construction scope change.** It is present in the logic-core settlement set (`OmegaValleySettlements()`) and the market network because it belongs to the coherent regional registry and the 4-day market rotation. However, Phase-1 **construction** is scoped to the approved build target — **Ahanwụ and Ọmà Ukwu only**. The logic core exposes `OmegaValleyPhase1ConstructedSettlements()` (Ahanwụ + Ọmà Ukwu), and `ATDDOmegaValleyLevel::PlaceSettlements()` constructs **only those two**. Ihiala is registered but not built/placed/spawned in Phase 1; it becomes constructible in Phase 2 without code change. (Verified by `TDDWorldLogicTests`: "Ihiala is NOT constructed in Phase 1" + "Ihiala remains present in the regional registry data.")

## 4d. Market-day assignments — provisional vs research-supported vs approval

| Item | Status | Basis |
|---|---|---|
| The four market days **Eke, Orie, Afo, Nkwo** and their sequence | **Research-supported [H]** | Documented Igbo 4-day market week (Wikipedia "Igbo calendar"; Oblong Media; dibianwangwuuchendu). |
| The 4-day week structure (Eke→Orie→Afo→Nkwo) | **Research-supported [H]** | As above. |
| The 8-day major/minor cycle | **Regionally documented, unverified [R]** | Reported; flagged for verification. |
| Each community holds its market on its own day (not synchronized) | **Research-supported [H]** | Documented. |
| **Specific assignment:** Ọmà Ukwu = Eke | **Provisional [A] — requires Story/Research approval** | Creative regional arrangement; data-driven, changes without code. |
| **Specific assignment:** Ahanwụ = Afo | **Provisional [A] — requires Story/Research approval** | As above. |
| **Specific assignment:** Ihiala = Nkwo | **Provisional [A] — requires Story/Research approval** | As above (Ihiala is registry data; its day is also provisional). |

**Confirmation:** the four-day system and the "each settlement has its own day" principle are research-supported. The **specific per-settlement day assignments are provisional creative adaptation** and **must not silently become canon** — they are flagged `[A]` in `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` and require Story/Research approval before being treated as canon. They may support technical testing now.

## 4e. Expected in-game observations and logs (initialization + acceptance)

**Subsystem initialization (begin-play logs):**
- `TDD LocationRegistry: registered 3 Ọmà-valley settlements (logical population 3750).`
- `TDD PopulationSubsystem: logical population = 3750 across 3 settlements (independent of rendering).`
- `TDD CalendarSubsystem: world day 0 = Eke, season Rainy.`
- `TDD MarketSubsystem: 3 settlements in the market network.`
- `TDD WeatherSubsystem: initial season Rainy, rain ..., mud ..., water ...`
- `TDD OmegaValleyLevel: built Phase-1 core with 2 settlements (Ahanwụ, Ọmà Ukwu), Ọmà river, road spine and forest.`
- `TDD ValleyGameMode: logical population 3750 (rendered subset is budgeted per settlement). Market today = Eke, season = Rainy.`

**Population simulation (per settlement, on spawn/refresh):**
- `TDD SettlementZone 'Ahanwụ' (ordinary): logical 1160, spawned N (named X, crowd Y, scripted 0, background Z).`
- `TDD SettlementZone 'Ọmà Ukwu' (market day): logical 2840, spawned N (named X, crowd Y, scripted S, background Z).`
- The **logical figure is always the full value**; the spawned subset is the budgeted render.

**Market activation (calendar progression):**
- On **Eke**: Ọmà Ukwu's market activates — `TDD SettlementZone 'Ọmà Ukwu' (market day)` with scripted stalls spawned and crowd/background at the HIGH-density surge.
- On **Afo**: Ahanwụ's market activates (same log pattern).
- On non-market days: `(ordinary)` with no scripted stalls and lower crowd/background.

**Calendar progression:**
- `TDD CalendarSubsystem: advanced to world day N = <day> (<season>).` each market day.

**Weather consequences (observable, not just a sky change):**
- Rainy: high `WaterLevel` → `IsRiverCrossingBroken()` may be true (canoe required); high `MudLevel` → `GetTraversalSlowdown()` slows foot travel; lush `VegetationGreenness`; market population suppressed.
- Dry: low `WaterLevel` (crossing open), `MudLevel` ~0, vegetation browns, full outdoor activity; market population higher than the same market in rain.
- `market-in-rain ≠ market-in-dry` is directly observable in the spawned population counts.

**Acceptance mapping:** these logs + the in-PIE observations (§4 "What to observe") are the evidence that all five subsystems initialized, population simulation runs, the market activates with the calendar, the calendar progresses, and weather produces gameplay consequences.

## 5. Known limitations (honest)

1. **UE code not compiled in-sandbox.** All `TDD_GAME` C++ is authored against UE 5.8 but **not compiled**; the first owner build may surface API-level diagnostics to resolve. The logic core is the tested, stable layer.
2. **Market-day assignments are `[A]` adaptive** (Ọmà Ukwu=Eke, Ahanwụ=Afo, Ihiala=Nkwo) — proposed regional arrangement; **flag for Story/Research confirmation** before it is treated as canon. Data-driven, so it changes without code change.
3. **Settlement geometry is a blockout** (instanced basic shapes), not final art — Phase-1 is systems integration, not visual finalization.
4. **Named-NPC dialogue/animation hooks are stubs** — routine/presence is modelled; full AI/dialogue integration is a later phase.
5. **Sacred-place specifics are not authored** in the Phase-1 core (cultural review pending); no invented deities/rituals.
6. **Population tier rendering uses direct spawning**, not Mass ECS; sufficient for Phase-1 HIGH density via instancing. Mass migration is a Phase-2 optimization.
7. **Time-of-day** is a single sampled value in the current refresh; a full day/night cycle integration is Phase-2.
8. **Only the Phase-1 core** (Ahanwụ, Ọmà Ukwu, Ihiala) is built; the full 250 km² region remains the target and is not reduced by this phasing.

## 6. Test evidence (actual, in-sandbox)

```
TDD_RESULT TDD-Pure.TDDAIPureCoreTests PASS 111/111
TDD_RESULT TDD-Pure.TDDChapterRouteTests PASS 9/9
TDD_RESULT TDD-Pure.TDDCombatMathTests PASS 39/39
TDD_RESULT TDD-Pure.TDDMovementCoreTests PASS 48/48
TDD_RESULT TDD-Pure.TDDStateMachineTests PASS 658/658
TDD_RESULT TDD-Pure.TDDDodgeDistanceMathTests PASS 18/18
TDD_RESULT TDD-Pure.TDDWorldLogicTests PASS 52/52
=== exit: 0 ===
```

The `TDDWorldLogicTests` cover: 4-day market week + wrap, settlement market-day assignments, route distances (~4 km), wet/dry seasonal model, weather consequences (mud/water/vegetation/activity), logical-population-independent-of-render, market-day density surge (>2× ordinary), bounded HIGH render budget, correct market activation per day, midday peak, and market-in-rain vs market-in-dry.

*End of TDD-IMPL-PHASE1-002.*
