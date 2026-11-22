# W2 Implementation Assignments — Engineering Execution Plan

**Document ID:** TDD-IMPL-W2ASG-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM. **Purpose:** Convert the W2-R1–R8 audit into explicit implementation assignments. **Move from identifying missing work to producing it.**
**Status definitions:** NOT STARTED → IN PROGRESS → DELIVERED / AWAITING REVIEW → ACCEPTED. Plus BLOCKED, TECHNICALLY VERIFIED.
**Execution split:** the **agent** authors all code, maps, scripts, test definitions and assets wherever its environment permits. The **owner Mac** supplies the Unreal execution environment, runs the required procedures, reviews results and returns evidence. **Implementation responsibility does not transfer to the owner merely because Unreal cannot run in the agent sandbox** — Engineering authors everything; only final UE build/run/verification is owner-Mac.

---

## Assignment summary

| Item | Required execution | Responsible | Status |
|---|---|---|---|
| W2-R1 | Create + validate `L_TDD_Test_Movement` | Engineering | NOT STARTED |
| W2-R2 | Implement functional movement suite (AC-01–13) | Engineering | NOT STARTED |
| W2-R3 | Implement functional combat tests | Engineering | NOT STARTED |
| W2-R4 | Import Adanna V3 → establish `BP_Adanna_ProductionV3` | Engineering / Technical Art | NOT STARTED (in-engine) |
| W2-R5 | Produce playable CH01 greybox | Design / Engineering | NOT STARTED (in-engine) |
| W2-R6 | Execute Windows CI + resolve failures | Engineering | IMPLEMENTED, NOT VERIFIED |
| W2-R7 | Integrate required content into Unreal | Engineering | NOT STARTED |
| W2-R8 | Implement movement + camera metrics recorders | Engineering | NOT STARTED |

**W2 acceptance is a prerequisite for W3 M1-gate readiness.** Do not skip; do not re-scope.

---

## W2-R1 — Test map: `L_TDD_Test_Movement`
1. **Required execution:** Author the test-movement level `L_TDD_Test_Movement` — a flat/gentle-terrain map with the movement-test affordances the M1 spec requires (§7 test map): flat ground for distance-accuracy (AC-19), a step ramp at 45 cm (AC-07, AC-08), an obstruction for dodge-geometry (AC-21), and defined floors for the floor-distance correction (AC-21). Build actor / world logic as C++ (or a Blueprint-less level) so the functional tests can run against a real world.
2. **Responsible:** Engineering (agent authors the map + world script; owner builds/runs in UE).
3. **What the agent authors now (in-sandbox):** the level geometry via the project's automation-friendly build path; `L_TDD_Test_Movement.uasset`/level authoring script; `Config/DefaultEngine.ini` entry (`GameDefaultMap` / test-map override) as appropriate; a build-readiness check that the map is listed.
4. **Owner-Mac step (verification only):** open UE 5.8.4, build, and confirm the map loads and is the default test world.
5. **Acceptance criteria:** Map builds and loads in UE 5.8.4; contains the four affordances above; functional tests can target it.
6. **Evidence:** map asset + `DefaultEngine.ini` diff; owner-Mac load screenshot/log.

## W2-R2 — Functional movement suite (AC-01–13)
1. **Required execution:** Implement the **actual** `TDD-Functional.Movement.*` test suite that the M1 spec (v1.4 §4, §5) defines — the automation tests M-01a etc. covering AC-01–13 (latency L1, input→intent, movement modes, dodge distance/radius, collision, state transitions, buffering/coyote, camera stability where applicable). This is the W3 gate's movement core; author it now so W3 builds on it.
2. **Responsible:** Engineering (agent authors tests + any production-movement wiring; owner runs).
3. **What the agent authors now:** the functional test cases in `Source/TheDisobedientDaughter/Private/Tests/` (extend the existing `TDD*Tests.cpp` set with `TDD-Functional.Movement.*`); wire the ATDD player character CMC movement per the spec (Enhanced Input, state machine, dodge) so the tests have a real subject; build-readiness gate.
4. **Owner-Mac step (verification only):** build + run the `TDD-Functional.Movement.*` suite; capture pass/fail per AC.
5. **Acceptance criteria:** AC-01–13 each have a named automation test; suite passes in UE.
6. **Evidence:** test files + owner-Mac test output (per-AC results).
7. **Note:** `TDD.Movement.DodgeDistanceMath` exists (pure) — it is a subset, not the suite. Build the full functional suite.

## W2-R3 — Functional combat tests
1. **Required execution:** Implement `TDD-Functional.Combat.*` — combat-flow tests covering encounter/damage/stagger behaviours. Reuse the `TDDDamagableCharacter` + combat math foundation already present (`TDDAIIntegrationTests.cpp`, CombatMath 39/39 pure) and extend to functional combat against a real world/encounter.
2. **Responsible:** Engineering (agent authors; owner runs).
3. **What the agent authors now:** functional combat test cases; wiring of the combat state machine / damage requests against the real encounter fixture; build-readiness.
4. **Owner-Mac step:** build + run `TDD-Functional.Combat.*`; capture results.
5. **Acceptance criteria:** functional combat suite passes in UE.
6. **Evidence:** test files + owner-Mac output.

## W2-R4 — Adanna V3 import → `BP_Adanna_ProductionV3`
1. **Required execution:** Import the prepared Adanna V3 FBX into the UE project and establish `BP_Adanna_ProductionV3` (the production character Blueprint) with the shared `HUMAN_BASE_PROPOSED` skeleton wired to the character/animation/material setup.
2. **Responsible:** Engineering / Technical Art.
3. **What the agent authors now (in-sandbox):** the import script / FBX import mapping (skeleton retarget, material/texture binding, slot setup) as a reproducible automation-friendly import step; the `BP_Adanna_ProductionV3` skeleton/animation/material configuration in code or a scripted asset pipeline. The Adanna V3 FBX exists at `.arena/production/2026-11-24_w1d7_blender_package/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` (prepared, Blender-QC-passed).
4. **Owner-Mac step (verification only):** execute the import in UE, confirm `BP_Adanna_ProductionV3` spawns and is playable; capture import + spawn evidence.
5. **Acceptance criteria:** `BP_Adanna_ProductionV3` exists and spawns; skeleton/animation/material bound; no import errors.
6. **Evidence:** import log; BP spawn screenshot; skeleton mapping confirmation.

## W2-R5 — Playable CH01 greybox
1. **Required execution:** Produce the **actual** playable CH01 greybox map (not just a plan) — the CH01 compound greybox from `.arena/production/2026-11-20_w1d3_ch01_greybox/` (plan/report exist; the map itself was not built in-engine). Assemble the greybox into a playable level wired to `BP_Adanna_ProductionV3`.
2. **Responsible:** Design (layout) / Engineering (engine wiring, spawn, collision).
3. **What the agent authors now:** the greybox level layout + world script; spawn point; collision/volume setup; build-readiness. The design brief/report already exists to drive it.
4. **Owner-Mac step (verification only):** build + play the CH01 greybox; confirm traversability + spawn.
5. **Acceptance criteria:** CH01 greybox builds, loads, is playable (Adanna spawns + moves through it).
6. **Evidence:** level asset; owner-Mac play capture/log.

## W2-R6 — Windows CI execution + failure resolution
1. **Required execution:** **Execute** `Tools/engine/windows_ci.sh` (Windows) and resolve any failures. The script exists (IMPLEMENTED); it has **not** been executed to GREEN.
2. **Responsible:** Engineering.
3. **What the agent authors now:** ensure `windows_ci.sh` + `build_readiness.py` are correct and idempotent; fix any static blockers the CI would surface; document the exact Windows execution command + expected output.
4. **Owner-Mac step (or a Windows runner):** actually run Windows CI; capture the log. (If only the Mac is available, run the equivalent Mac CI path and note the Windows-specific gap explicitly — do not claim Windows CI passed without Windows execution.)
5. **Acceptance criteria:** Windows CI runs GREEN; failures resolved; evidence logged.
6. **Evidence:** CI log saved to `Saved/BuildEvidence/<ts>/windows-ci/`.

## W2-R7 — Content integration
1. **Required execution:** Integrate the required content into Unreal — Adanna V3 BP (W2-R4), CH01 greybox (W2-R5), movement/combat/test content (W2-R2/R3) into a coherent playable content set. This is the assembly that makes the M1 candidate.
2. **Responsible:** Engineering.
3. **What the agent authors now:** the content-integration wiring (BP/asset references, content lists, integration manifest) as reproducible scripts/config.
4. **Owner-Mac step (verification only):** verify the integrated content loads and runs together.
5. **Acceptance criteria:** integrated content loads + runs in UE without missing-asset errors.
6. **Evidence:** integration manifest + owner-Mac run log.

## W2-R8 — Movement + camera metrics recorders
1. **Required execution:** Implement `TDD.Movement.Report` and `TDD.Camera.Report` — metrics recorders that emit CSV (movement distances/timings; camera stability metrics), per the M1 spec instrumentation requirements (§6, AC-28–31). The harness must not change what it measures (AC-30 on/off delta ≤ 0.05 ms), must be a no-op in Shipping, and must record frame-rate cap + vsync state in the CSV header.
2. **Responsible:** Engineering.
3. **What the agent authors now:** the recorder actor/subsystem + CSV writer + Shipping no-op guard + the frame-rate/vsync header; the recorder test assertions.
4. **Owner-Mac step (verification only):** run with recorders on/off; capture CSVs; verify the on/off delta assertion.
5. **Acceptance criteria:** recorders emit CSV; on/off delta ≤ 0.05 ms; Shipping no-op verified.
6. **Evidence:** recorder code + sample CSVs + owner-Mac run output.

---

## Dependency sequence

```
W2-R1 (test map) ──┬─→ W2-R2 (movement suite) ─→ W2-R8 (metrics)
                   ├─→ W2-R3 (combat tests)
W2-R4 (Adanna BP) ─┴─→ W2-R5 (CH01 greybox) ─→ W2-R7 (content integration)
W2-R6 (Windows CI) ───────────────────────────→ (independent, parallel)
```

- **W2-R1 first** (movement/combat/greybox tests need the test world).
- **W2-R4 before W2-R5** (greybox needs the playable character to be playable).
- **W2-R6 independent** — runs in parallel.
- **W2-R8 after W2-R2** (recorders instrument the movement suite).

## Parallel work
- **Design** continues CH01 environment completion, ST05–ST07, character animation and other independent visual production **while W2 engineering runs** — a blocked W2 integration does not block Design production.
- **Facial PoC** (owner-Mac) runs in parallel with W2.

## PM tracking
PM reconciles each assignment's actual implementation + integration into the authoritative register. Every result — agent-authored or owner-verified — is incorporated with evidence, status, owner and date. **W2 acceptance is declared only when all eight items are ACCEPTED with evidence.**
