# W2 (Stage C) Exit Audit — The Disobedient Daughter

**Document ID:** TDD-IMPL-W2AUDIT-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Purpose:** Establish, against the original production roadmap, whether every W2 (Stage C) deliverable is complete and accepted **before** treating W3 (Stage D, the M1 gate) as the current execution stage. This audit does not assume a deliverable is complete because related production code exists or because a build passes.
**Checkpoint of record:** commit `9bf189f` (owner-Mac daily train GREEN, evidence `Saved/BuildEvidence/20261121T170504Z`). Full history read from `origin/arena/553fb02d-tdd` (101 commits).
**Roadmap definition (ROADMAP v2.0 §4.2, Stage C = W2):** M1 candidate preparation · Adanna V3 import · CH01 greybox · associated integration and validation. **Stage D = W3:** the M1 gate (AC-01…31 + M1.32–35, three cold runs).

**Verification-scope statement:** The agent sandbox has no Unreal Engine and no owner Mac/Windows hardware. "Unreal verification status" below is reported **only** from owner-Mac evidence (the GREEN train at `9bf189f`) and the committed agent-side evidence under `docs/06_IMPLEMENTATION/evidence/`. Owner-Mac bundles live outside the repo (`Saved/BuildEvidence/…`, gitignored). Agent-side static checks are **not** Unreal verification.

---

## Audit summary (verdict)

**W2 (Stage C) is NOT complete and NOT accepted.** Four of the four W2 deliverables are **PREPARED** or **IN PROGRESS**; the actual Mac-side verification steps (in-engine import, map build, functional test execution, Windows CI) are **NOT EXECUTED** or only partially verified. The owner-Mac GREEN at `9bf189f` verifies a **subset** — 7 in-engine tests covering the encounter flow, camera pitch clamp, lighting switcher, playable-character defaults, dodge math, AI asset adapter, and GameMode foundation — but **not** the W2 deliverable set as defined by the roadmap. W3 must not be treated as the current stage until the remaining W2 work below is completed and accepted.

The verified subset (GREEN at `9bf189f`):
`TDD.Foundation.GameModeClass` · `TDD.M1.GameMode.EncounterFlow` · `TDD.M1.Lighting.StateSwitcher` · `TDD.M1.Player.CameraPitchClamp` · `TDD.M1.Player.PlayableCharacterDefaults` · `TDD.Movement.DodgeDistanceMath` · `TDD.W1D2.AI.BossPhaseAssetAdapter`

---

## Deliverable 1 — M1 candidate preparation

**Roadmap W2 exit criterion:** "M1 candidate AC-01…13 evidence" (ROADMAP §4.2 W2; WBS M1-S1/S2/S4; M1 spec §4 AC-01…13).

| # | Required field | Finding |
|---|---|---|
| 1 | **Original requirement** | Produce M1 candidate evidence for AC-01…13: the `TDD-Functional.Movement.*` world-sweep suite (latency L1–L3, accel/stop/turn, step-up/down, angled approach, sprint-over-step, corner stability, slope limits), 100-run determinism + variance + failure classification (M1-S1), floor/ground validation + floating-capsule guard in every state exit (M1-S2), collision edge cases (M1-S4). Driven by the `L_TDD_Test_Movement` test map (M1 spec §7 zones). |
| 2 | **Current implementation status** | **NOT IMPLEMENTED.** No `TDD-Functional.Movement.*` test exists in the tree (0 functional movement test TUs). The pure-core movement/state logic exists and passes agent-side (`TDDMovementCoreTests` 48, `TDDStateMachineTests` 658), but the in-engine functional movement suite required for AC-01…13 is absent. The character/CMC/state-machine foundation is present (`TDDAdannaCharacter`, `TDDCharacterStateComponent`, `TDDDodgeSweep`). |
| 3 | **GitHub commit / implementation evidence** | Foundation commits: `a6c830e` (pure movement/state core — AC-22/23/24/25/02–05/10), `8d0ae82` (pure combat core). Stage C: `3fde1f4` (encounter flow), `4712b0a` (camera pitch clamp). **No commit implements `TDD-Functional.Movement.*`.** |
| 4 | **Actual Unreal verification status** | **NOT VERIFIED.** The 7 GREEN tests include `TDD.Movement.DodgeDistanceMath` (pure math, AC-19 unit only) — **not** the AC-01…13 functional movement suite. No owner-Mac run has exercised AC-01…13. |
| 5 | **Acceptance status** | **NOT ACCEPTED.** The W2 exit criterion "M1 candidate AC-01…13 evidence" is **not met**. |
| 6 | **Outstanding dependencies / blockers** | **`L_TDD_Test_Movement` test map (M1 spec §7, 11 zones) — BLOCKED ON MAC** (must be authored in the UE editor; cannot be produced headlessly). All `TDD-Functional.Movement.*` tests depend on it. Also: `TDD-Functional.Movement.*` suite not yet written; metrics harness `TDD.Movement.Report` not built. |

---

## Deliverable 2 — Adanna V3 import + character integration

**Roadmap W2 deliverable:** "Adanna V3 import" (W2 register row 2; WBS M5-05/CT).

| # | Required field | Finding |
|---|---|---|
| 1 | **Original requirement** | Import the Adanna V3 production character into the UE project, wire `BP_Adanna_ProductionV3`, and verify skeleton/bone mapping against the movement clips. V2/V1 remain rollback fallbacks until V5/V3 passes its qualification gate. |
| 2 | **Current implementation status** | **PREPARED — NOT IMPORTED.** The import script `import_adanna_production_v3.py` is hash-verified; the Adanna V3 FBX is `40f1c83d…`. **No `BP_Adanna_ProductionV3` exists anywhere in `Source/` or `Config/`.** The in-engine import + BP wiring + skeleton/bone verification has **not** been run. |
| 3 | **GitHub commit / implementation evidence** | `ab45856` "Promote Adanna V3 / Guard V2 to integration targets (gate CLOSED at 2a4a88e)" — the **Blender QC/promotion**, not the in-engine import. `a2942de` "Character integration executed — Blender 4.2.23 headless, both characters PASS" — **Blender QC only**. The import script is committed but the UE import step is not. |
| 4 | **Actual Unreal verification status** | **NOT VERIFIED.** No in-engine test verifies the Adanna V3 skeleton/bone mapping. `TDD.M1.Player.PlayableCharacterDefaults` verifies defaults, not the V3 import. The W1 D4 report (WS4) explicitly recorded "Blender/UE import **not run**" → Unreal: **No**, runtime: **No**. |
| 5 | **Acceptance status** | **NOT ACCEPTED.** Import + BP wiring + skeleton verification pending. |
| 6 | **Outstanding dependencies / blockers** | **Mac step:** run the import script, create/wire `BP_Adanna_ProductionV3`, verify skeleton/bone mapping against the movement clips V1 (46/46 source PASS, Mac animation integration pending). V5/Guard V3 qualification (D-5) pending the Mac Blender run. |

---

## Deliverable 3 — CH01 greybox map

**Roadmap W2 deliverable:** "CH01 greybox" (W2 register row 3; WBS M2-08 / P-09; M1 spec §7).

| # | Required field | Finding |
|---|---|---|
| 1 | **Original requirement** | Build the actual CH01 greybox map at `/Game/Maps/Ch01_Greybox` from `build_chapter1_greybox.py` + `world.json` (7 waypoints, 46 obstacles, spawn in bounds), then run the W1D13 compound assembly (`import_ch01_compound_v2.py`). |
| 2 | **Current implementation status** | **PREPARED — NOT BUILT.** The builder script + `world.json` are validated agent-side (greybox-source-preflight.json). **No `Ch01_Greybox` map reference exists in `Source/` or `Config/`; the default map remains `/Engine/Maps/Entry`.** The in-engine map build has **not** been run. |
| 3 | **GitHub commit / implementation evidence** | `67f3745` "W2 integration: CH01 compound/lighting/clip **import scripts** + lighting state switcher" — the **scripts**, not the built map. `096163d` (WS5 W1D2: generate native Chapter 1 greybox from route data — agent-side). `0f6e4fa` (W1 D4: import Design greybox deliverables). The W1 D4 report (WS5) explicitly recorded "Blender `.blend`/FBX/manifest **not produced**" → Unreal: **No**, runtime: **No**. |
| 4 | **Actual Unreal verification status** | **NOT VERIFIED.** No map-load test for CH01 greybox exists. The agent-side greybox-source-preflight is a static preflight, not an in-engine map load. |
| 5 | **Acceptance status** | **NOT ACCEPTED.** The map is not built in-engine. |
| 6 | **Outstanding dependencies / blockers** | **Mac step:** run the builder in the UE editor → `/Game/Maps/Ch01_Greybox`; add PlayerStart/GameMode/encounter actors; validate doorway clearances, FBX scale/axes/collision/navigation; run the W1D13 compound assembly. Overlaps with the `L_TDD_Test_Movement` test-map blocker (Deliverable 1). |

---

## Deliverable 4 — Associated integration and validation

**Roadmap W2 deliverable:** "associated integration and validation" (W2 register row 4/5/6; ROADMAP §4.2 W2: combat/damage integration M3-02, block/parry M3-05, Windows CI node live W2, content).

| Sub-deliverable | Original requirement | Status | Commit evidence | Unreal verification | Acceptance | Outstanding / blockers |
|---|---|---|---|---|---|---|
| **4a. Combat integration (M3-02 hit detection, M3-05 block/parry)** | Integrate hit detection (custom channels, dedup → `FTDDDamageRequest`) and block/parry (guard-ready 0.08 s, parry 0.15 s → attacker stagger) into a live world. | **CODE PRESENT, NOT FUNCTIONALLY VERIFIED.** `TDDCombatComponent` exists; pure combat core passes agent-side (39/39). **No `TDD-Functional.Combat.*` test exists** (0 functional combat test TUs). | `8d0ae82` (pure combat core), `72ec2d9` (combat director), `4142de2` (player state/attack/defence). No functional combat test commit. | **NOT VERIFIED.** No owner-Mac run exercises hit detection / block / parry against a live dummy. W1 D4 (WS3) recorded "UE source/automation **not compiled/run**" → No/No. | **NOT ACCEPTED.** | Functional combat test suite (`TDD-Functional.Combat.*`) not written; combat training room + dummy not built. |
| **4b. Encounter + restart flow** | Greybox encounter flow + restart in `TDDGameMode` (playable M1). | **IMPLEMENTED + VERIFIED.** | `3fde1f4` (Stage C: greybox encounter flow + restart). | **VERIFIED.** `TDD.M1.GameMode.EncounterFlow` GREEN at `9bf189f`. | **ACCEPTED** (this sub-item). | — |
| **4c. Camera pitch clamp (M1-S5 control side)** | Third-person camera pitch clamp (M1 spec S5, AC-14..18 control side). | **IMPLEMENTED + VERIFIED** (after D-W1D8-024 audit #3 fix). | `4712b0a` (Stage C); D-W1D8-024 series `1fe778a`…`9bf189f`. | **VERIFIED.** `TDD.M1.Player.CameraPitchClamp` GREEN at `9bf189f`. | **ACCEPTED** (this sub-item — the pitch clamp; the full AC-14..18 5-criteria recorder is still not built, see Deliverable 1). | Full camera 5-criteria recorder `TDD.Camera.Report` not built. |
| **4d. Lighting state switcher** | Lighting preset state switcher (Dawn/Dusk/Night) + cooking-fire flicker. | **IMPLEMENTED + VERIFIED** (after D-W1D8-008/009/010 fixes). | `67f3745` (W2 integration), `2f460bf`, `095629d`, `b819620`, `c4b6ff0`. | **VERIFIED.** `TDD.M1.Lighting.StateSwitcher` GREEN at `9bf189f`. | **ACCEPTED** (this sub-item). | — |
| **4e. Windows CI node (F-04, ROADMAP W2)** | Windows bring-up on the reference PC → Windows CI node live W2; Windows suite parity run 1. | **NOT EXECUTED.** `Tools/engine/windows_ci.sh` exists; evidence `windows-ci-not-executed.txt` records "NOT EXECUTED — must run in the Windows reference-PC shell; host is Linux." No Windows build/automation has run. | `700f2c6` (WS6 W1D2: safe Windows CI preflight). The preflight exists; the CI run does not. | **NOT VERIFIED.** No Windows evidence bundle. W1 D4 (WS6) recorded "Mac, Win Development/automation and Win Shipping **not executed**" → No/No. | **NOT ACCEPTED.** W2 exit criterion "Windows suite parity run 1" **not met**. | **Reference PC (B-03/DA-03) not provisioned/arrived.** Windows CI bring-up (M6-08) not run. |
| **4f. Content integration (combat anim set, env kit v1)** | Integrate combat animation set + environment kit v1 (core modular pieces) into the project. | **PREPARED — NOT INTEGRATED IN-ENGINE.** W1D12/W1D13 batches integrated as scripts/assets; movement clips V1 (46/46 source PASS), guard clips (36/36), env kit V2 prepared. Mac import/integration pending (W2 register asset ledger: "pending Mac import/integration"). | `9f36558` (visual batch 1), `0354853` (Design batch 50fdd16), `67f3745` (clip import scripts). | **NOT VERIFIED.** No in-engine animation/content integration test. | **NOT ACCEPTED.** | Mac steps: run Adanna V3 + clip imports, wire BPs, verify skeleton/bone mapping (overlaps Deliverable 2). |

---

## W2 Exit Verdict

| Deliverable | Implementation | Unreal verification | Acceptance |
|---|---|---|---|
| 1. M1 candidate preparation (AC-01…13) | NOT IMPLEMENTED (no `TDD-Functional.Movement.*`) | NOT VERIFIED | **NOT ACCEPTED** |
| 2. Adanna V3 import + integration | PREPARED (no `BP_Adanna_ProductionV3`) | NOT VERIFIED | **NOT ACCEPTED** |
| 3. CH01 greybox map | PREPARED (no in-engine map) | NOT VERIFIED | **NOT ACCEPTED** |
| 4. Integration & validation | PARTIAL (encounter/camera/lighting verified; combat functional + Windows CI + content NOT) | PARTIAL | **NOT ACCEPTED** |

**W2 (Stage C) does not exit.** The owner-Mac GREEN at `9bf189f` is a real, verified milestone for the subset it covers, but it does not constitute W2 acceptance. The remaining W2 work must be completed and accepted before W3 (the M1 gate) is the current execution stage.

## Remaining W2 work (to accelerate, not remove)

| ID | Remaining W2 work | Track / owner | Blocks |
|---|---|---|---|
| W2-R1 | Author `L_TDD_Test_Movement` test map (11 zones) on the Mac | OW (Mac editor) + T1 spec | Deliverable 1 (all AC-01…13 functional tests) |
| W2-R2 | Implement `TDD-Functional.Movement.*` (AC-01…13) + 100-run determinism | T1 | Deliverable 1 |
| W2-R3 | Implement `TDD-Functional.Combat.*` (M3-02 hit detection, M3-05 block/parry) | T2 | Deliverable 4a |
| W2-R4 | Adanna V3 in-engine import + `BP_Adanna_ProductionV3` + skeleton/bone verification | OW/CT (Mac) + T3 | Deliverable 2 |
| W2-R5 | CH01 greybox map build + W1D13 compound assembly + PlayerStart/GameMode/encounter actors | OW (Mac) + T1 | Deliverable 3 |
| W2-R6 | Windows CI bring-up (reference PC) + Windows parity run 1 | OW/T3 | Deliverable 4e |
| W2-R7 | Content in-engine integration (Adanna V3, combat anims, env kit) | OW/CT (Mac) + T3 | Deliverable 4f |
| W2-R8 | Metrics harness `TDD.Movement.Report` + camera 5-criteria recorder `TDD.Camera.Report` | T1 | Deliverable 1 (AC-28/30, AC-14..18) |

**Parallelisation (safe):** W2-R1/R4/R5/R6/R7 are Mac-side owner actions — batch them into coordinated Mac sessions. W2-R2/R3/R8 are agent-side (T1/T2) and proceed in parallel with the Mac steps, writing tests against the frozen M1 spec contracts. No two tracks touch one surface (movement/camera = T1, combat = T2, world/content/CI = T3). W2-R1 (test map) and W2-R5 (CH01 greybox) are both Mac-editor map work — sequence them in one Mac session to avoid duplicate editor overhead.

## Complete sequence: remaining W2 work → W2 acceptance → W3 M1 gate → Checkpoint A

```
[REMAINING W2 WORK — parallel]
  OW (Mac):  W2-R1 test map  ─┐
             W2-R4 Adanna V3  │  Mac sessions (batched)
             W2-R5 CH01 grey  │
             W2-R6 Windows CI ─┤ (reference PC)
  T1 (agent): W2-R2 Movement.*  ┐
              W2-R8 metrics/    │  agent-side, parallel
               camera recorders  │
  T2 (agent): W2-R3 Combat.*    ┘
        │
        ▼
[W2 ACCEPTANCE] — every W2 deliverable verified with evidence:
   M1 candidate AC-01…13 evidence · Adanna V3 imported+verified ·
   CH01 greybox built+verified · combat/Windows/content integration verified ·
   Windows parity run 1
        │  (W2 / Stage C exits; ledger row + 8-point note)
        ▼
[W3 — M1 GATE] — three cold Mac runs: AC-01…31 + M1.32–35
   (functional movement + unit movement + camera 5-criteria + input + metrics
    + first-playable M1-P1…P6 + 3 cold runs)
        │  (M1 exits; ledger row)
        ▼
[CHECKPOINT A (end W4)] — M1 + M2 gates exited · playable core loop
   (movement → traversal → combat vs dummy/archetype → death → respawn) ·
   2-machine verification (Mac + Windows CI) · save/load smoke ·
   no P0/P1 · 8-point report · owner go/no-go on W5–8 scope
```

**Rule:** W2 acceptance is a hard gate before the W3 M1 gate. No W2 deliverable is renamed as W3 work, removed, or accepted on code-presence/build-pass alone. No AC is weakened.
