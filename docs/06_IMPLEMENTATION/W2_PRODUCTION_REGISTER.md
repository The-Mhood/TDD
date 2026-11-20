# W2 Production Register — The Disobedient Daughter

**Status: ACTIVE** (2026-11-20). Stage A closed on the owner Mac at `712ee22` (first genuine engine verification PASS, evidence `Saved/BuildEvidence/20261120T174909Z`). W2 / Stage C is the active production phase. Existing roadmap dates and dependencies are preserved; this register tracks W2 execution only.

## W2 deliverables and current status

| # | Deliverable | Status | Evidence / next step |
|---|---|---|---|
| 1 | **M1 playable candidate** | IN PROGRESS | Encounter + restart flow committed (`3fde1f4`), camera pitch clamp committed (`4712b0a`); both pending owner-Mac engine verification. Greybox map build is the Mac critical path. |
| 2 | **Adanna production import + character integration** | PREPARED | V3 import script hash-verified (`import_adanna_production_v3.py`, Adanna V3 FBX `40f1c83d…`). Mac step: run import, wire `BP_Adanna_ProductionV3`, verify skeleton/bone mapping against the movement clips. V2/V1 rollback intact. |
| 3 | **Actual CH01 greybox map** | PREPARED | `build_chapter1_greybox.py` + `world.json` validated agent-side (7 waypoints, 46 obstacles, spawn in bounds). Mac step: run builder → `/Game/Maps/Ch01_Greybox`; W1D13 compound assembly script prepared (`import_ch01_compound_v2.py`). |
| 4 | **Functional movement, combat, encounter flow** | IN PROGRESS | Combat/state/traversal/AI foundations in tree; encounter flow + camera clamp implemented. Functional movement automation (`TDD-Functional.Movement.*`, AC-04…AC-13) requires the Mac-authored test map zones. |
| 5 | **Required test map + functional automation** | BLOCKED ON MAC | M1 spec §7 `L_TDD_Test_Movement` (Z_Flat, Z_Dodge, Z_Steps, Z_Corridor1/2) must be authored in the editor on the Mac; automation suites follow. In-engine tests in tree: GameMode foundation, playable character defaults, dodge math, AI adapter, encounter flow, camera clamp. |
| 6 | **Continuous Design asset integration** | IN PROGRESS | W1D12 batch (guard clips, env kit V2, VFX sprites) and W1D13 batch (`50fdd16`: compound V2, lighting keys, movement clips) integrated. Design work order `W1D8_DESIGN_WORK_ORDER.md` active; V5/Guard V3 qualification pending the Mac Blender run. |

## Integration status vocabulary (used throughout)

- **Imported** — asset is in the tree/content pipeline, structure validated.
- **Integrated** — wired into the project (import script run, assembly/BP wiring done).
- **Qualified** — passed its source-level gate (QC JSON, checksums, validation).
- **Verified** — passed its in-engine/acceptance check with evidence.

## Asset ledger (W1D12/W1D13 batches)

| Asset | Batch | Imported | Integrated | Qualified | Verified (engine) |
|---|---|---|---|---|---|
| Adanna AD-03 V3 FBX | W1D7 | yes | script prepared | yes (Blender QC) | pending Mac import |
| Guard Class V2 FBX | W1D7 | yes | script prepared | yes (Blender QC) | pending Mac import |
| CH01 Compound Assembled V2 (OBJ) | W1D13 | yes | script prepared | yes (agent-side validation) | pending Mac assembly |
| ST01 DAWN / ST03 DUSK / ST04 NIGHT keys | W1D13 | yes | lighting switcher implemented | approved provisional | pending Mac lighting build |
| Adanna movement clips V1 (6 clips) | W1D13 | yes | import script prepared | yes (46/46 source PASS) | pending Mac animation integration |
| Guard animation clips (5 states) | W1D12 | yes | — | yes (36/36 source PASS) | pending Mac animation integration |
| Env Kit V2 modular OBJs | W1D12 | yes | compound assembly uses them | yes | pending Mac import |
| VFX physical sprites | W1D12 | yes | — | yes | pending in-engine assembly |

## Gates preserved

- V3/V2 remain the integration baseline; V2/V1 remain rollback fallbacks until V5/V3 passes its Mac qualification gate.
- Enemy classes, abilities and supernatural VFX remain HELD until story/gameplay definitions exist.
- No AC is weakened to pass a gate; failed builds/runs never produce GREEN (ledger rule).
