# TDD Phase 1 — PIE Acceptance Checklist (B2 / B3)

**Document ID:** TDD-IMPL-PHASE1-PIE-001 · **Version:** 1.0 · **Date:** 2026-11-22
**Author:** PM / Engineering. **Branch:** `arena/553fb02d-tdd`. **Build commit:** `995caf9`.
**Purpose:** the exact owner-side editor actions, the Output Log lines to expect, and the
recording acceptance checklist for the Phase-1 runtime gate. **B1 (build) is CLEARED;
this checklist gates B2 (runtime/PIE) and B3 (launch-map).**
**Companion:** `PHASE1_IMPLEMENTATION_EVIDENCE_AND_BUILD_PROCEDURE.md` §4.4–4.5 and §4e
(the authoritative source for the expected logs).

**Standing rule:** this is a procedure, not evidence. Nothing here counts until the owner
runs PIE on the Mac and the captured Output Log + recording are reviewed. No status is
upgraded without the actual evidence.

---

## 1. Preconditions (all must be true before PIE)

- [ ] Owner-Mac UE 5.8 **Mac ARM64 Development** build of `995caf9` succeeded (B1 CLEARED,
      `BUILD_DIAGNOSTIC_20261122T134346Z.log`) — **already satisfied 2026-11-22**.
- [ ] The editor opens the project cleanly (no recompile on open).
- [ ] The five world subsystems are registered (`DefaultEngine.ini`
      `[/Script/Engine.Engine] WorldSubsystems=...` includes the TDD subsystems).
- [ ] The executable/editor reference the **same commit** `995caf9` that built clean.

## 2. Owner editor actions — exact order (the ONLY actions the owner performs)

1. **Create the launch map:** Content Browser → Add New → **Map** → name it
   **`OMEGA_VALLEY_PHASE1.umap`**. Save.
2. **Assign the Game Mode:** Open the map → World Settings panel → **Game Mode Override**
   → set to **`TDDOmegaValleyGameMode`**.
3. **Place a Player Start:** Content Browser → Add New → **Player Start** → drop it into
   the valley (on the road spine / near a settlement).
4. **PIE:** press **Play** (or **Alt+P**). The Ọmà-valley core launches.
5. **Capture evidence:** while PIE runs, copy the full **Output Log** (editor Output Log
   window or the PIE process stdout) and record a playthrough video.

> The owner performs **only these documented editor actions**. If PIE fails, do **not**
> edit C++ — send the Output Log to Engineering.

## 3. Expected Output Log checks (copy/verify each line against §4e)

### 3a. Subsystem initialization (begin-play) — all five must appear

- [ ] `TDD LocationRegistry: registered 3 Ọmà-valley settlements (logical population 3750).`
- [ ] `TDD PopulationSubsystem: logical population = 3750 across 3 settlements (independent of rendering).`
- [ ] `TDD CalendarSubsystem: world day 0 = Eke, season Rainy.`
- [ ] `TDD MarketSubsystem: 3 settlements in the market network.`
- [ ] `TDD WeatherSubsystem: initial season Rainy, rain ..., mud ..., water ...`
- [ ] `TDD OmegaValleyLevel: built Phase-1 core with 2 settlements (Ahanwụ, Ọmà Ukwu), Ọmà river, road spine and forest.`
- [ ] `TDD ValleyGameMode: logical population 3750 (rendered subset is budgeted per settlement). Market today = Eke, season = Rainy.`

### 3b. Population simulation (per settlement, on spawn/refresh)

- [ ] `TDD SettlementZone 'Ahanwụ' (ordinary): logical 1160, spawned N (named X, crowd Y, scripted 0, background Z).`
- [ ] `TDD SettlementZone 'Ọmà Ukwu' (market day): logical 2840, spawned N (named X, crowd Y, scripted S, background Z).`
- [ ] **Logical figure is always the full value**; the spawned subset is the budgeted render (the independence demonstration).

### 3c. Market activation (calendar progression)

- [ ] On **Eke**: Ọmà Ukwu's market activates — `TDD SettlementZone 'Ọmà Ukwu' (market day)` with scripted stalls spawned and crowd/background at the HIGH-density surge.
- [ ] On **Afo**: Ahanwụ's market activates (same log pattern).
- [ ] On non-market days: `(ordinary)` with no scripted stalls and lower crowd/background.

### 3d. Calendar progression

- [ ] `TDD CalendarSubsystem: advanced to world day N = <day> (<season>).` each market day.

### 3e. Weather consequences (observable, not just a sky change)

- [ ] **Rainy:** high `WaterLevel` → `IsRiverCrossingBroken()` may be true (canoe required); high `MudLevel` → `GetTraversalSlowdown()` slows foot travel; lush `VegetationGreenness`; market population suppressed.
- [ ] **Dry:** low `WaterLevel` (crossing open), `MudLevel` ~0, vegetation browns, full outdoor activity; market population higher than the same market in rain.
- [ ] `market-in-rain ≠ market-in-dry` is directly observable in the spawned population counts.

> If any expected line is **missing**, record it and send the full Output Log to Engineering.
> Do not mark B2/B3 cleared on partial logs.

## 4. Recording acceptance checklist (playthrough video)

The recording must demonstrate, at minimum:

- [ ] Entering **Ahanwụ** and **Ọmà Ukwu** with **population actors present**.
- [ ] The **Eke market activating in Ọmà Ukwu** (stalls + crowd surge visible).
- [ ] The **Afo market activating in Ahanwụ** (stalls + crowd surge visible).
- [ ] The observable **rainy→dry weather consequences**: water level / river crossing,
      mud / traversal slowdown, vegetation change, market-density difference.
- [ ] Calendar progression observable (market day advancing).

## 5. Acceptance decision

- **B2 (runtime/PIE) CLEARED** when: all §3 Output Log checks pass **and** the §4
  recording checklist is complete **and** the evidence is reviewed.
- **B3 (launch-map) CLEARED** when: the `OMEGA_VALLEY_PHASE1.umap` launch map builds and
  the §2 actions complete end-to-end (map + game mode + player start + PIE).
- **Phase 1 is NOT complete** until B2 and B3 are cleared. B1 (build) is already cleared.

**Evidence to return to PM/Engineering:** the full Output Log (text) + the playthrough
recording + the completed checklist (marked). Engineering diagnoses any missing/failed line.
