# STAGE GATES — entry criteria, exit criteria, evidence

**Document:** TDD-PROD-002 · Version 1.0 · 2026-11-16
**Authority:** `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` §14. The directive mandates the stage order;
this document defines what "done" means at each gate. **A stage is not complete because the work was done;
it is complete when the evidence exists and the Technical Director accepts it.**

## Universal rules

1. **No stage may begin before the previous gate is ACCEPTED** (or an explicit written waiver exists in
   `Docs/evidence/waivers/`).
2. Every gate produces: an evidence bundle, an agent report using the status tags, a list of known gaps,
   and a regression run of all previous gates.
3. A gate that regresses a previous gate is failed, regardless of its own results.
4. Performance is measured at every gate from Stage 3 onward. Discovering the frame budget at Stage 9 is a
   process failure.
5. Canon rules (`Tools/canon`) must be green at every gate.

## Status tags (from the architecture document)

`ESTABLISHED` · `PARTIAL` · `SPEC` · `STUB` · `EXPERIMENTAL` · `MOCKED` · `BLOCKED` · `UNAVAILABLE`

## Stage 0 — Architecture and technical foundation

| | |
|---|---|
| **Entry** | Nothing |
| **Scope** | Master Engineering Architecture Document; ADRs; canon index + validators; module skeleton; repo hygiene; interfaces frozen; RACI |
| **Deliverables** | `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, `Docs/adr/*`, `Docs/CANON_INDEX.md`, `Tools/canon/*`, `Docs/production/*` |
| **Automated tests** | `python3 -m unittest discover -s Tools/canon/tests` — all green |
| **Evidence** | `Docs/evidence/stage0/L0_canon_index_validation.json` |
| **Exit criteria** | Architecture ratified by TD; D-01/D-02/D-04/D-10 raised; interfaces signed off by all three agents; L0 green |
| **Known limits** | No engine code exists. Everything runtime is SPEC. |

**Current status: COMPLETE pending TD ratification** (2026-11-16).

## Stage 1 — Project and build foundation

| | |
|---|---|
| **Entry** | Stage 0 accepted |
| **Scope** | `TDD.uproject`; module targets (`TDD`, `TDDEditor`, `TDDTests`); `Build.cs`/`Target.cs`; ini baseline; Gameplay Tag registry; save schema v1; evidence harness; CI script; **first headless build** |
| **Exit criteria** | (a) Headless editor builds with zero warnings-as-errors on our modules; (b) `-nullrhi` editor boots an empty map; (c) ≥1 automation test runs and passes; (d) automation report parses into our evidence format; (e) `.gitignore`/`.gitattributes` landed; (f) tag registry validated |
| **Evidence** | `Docs/evidence/stage1/build_log.txt`, `automation_report.xml`, `boot_smoke.md` |
| **Known limits** | Requires an engine-equipped machine. **UNAVAILABLE in the current sandbox.** |

## Stage 2 — Movement and character laboratory

| | |
|---|---|
| **Entry** | Stage 1 accepted (real build + tests) |
| **Scope** | `UTDDCharacterMovementComponent`; Enhanced Input; orbit/spring camera with combat + exploration profiles; `FTDDLocomotionState`; vault/ledge/drop traversal; gym map; Adanna placeholder capsule rig |
| **Automated tests** | Sprint speed applied; strafe locks rotation to camera; dodge displacement and i-frame window; vault completes or cleanly aborts; camera never clips through test walls; locomotion state delegate fires on transition |
| **Manual evidence** | Session video: run → sprint → vault → dodge → camera orbit; written feel notes |
| **Exit criteria** | All automation green; no sliding-feet observation at jog/sprint in gym; camera collision acceptable in 3 test rooms; frame time in gym ≤ budget |
| **Known limits** | Placeholder anim is acceptable here and is tagged MOCKED; combat anim arrives Stage 4 |

## Stage 3 — Combat foundation

| | |
|---|---|
| **Entry** | Stage 2 accepted |
| **Scope** | `UTDDHitArbiter`; ability layer (light/heavy/special); weapon Data Asset + sheathed socket; dodge/block/parry; poise; damage feedback; hit-stop; audio hooks; combat gym |
| **Automated tests** | Hit arbitration deterministic under fixed seed; only arbiter applies damage; i-frames block damage; poise break triggers stagger exactly once; parry window edges (±1 frame) produce expected results; second weapon slot is unavailable (canon guard) |
| **Evidence** | Determinism report, combat gym video, tuning sheet (CSV) |
| **Exit criteria** | 60 fps in combat gym; 3-hit combo with no register loss; damage feedback readable at 1080p; audio hooks confirmed by A2 |
| **Known limits** | One enemy dummy only; real AI is Stage 5 |

## Stage 4 — Character behaviour and animation

| | |
|---|---|
| **Entry** | Stage 3 accepted |
| **Scope** | Locomotion ABP (motion matching if D-07 approves, else blend space); combat layers; hit reactions; foot IK; turn-in-place; facial/cinematic hooks |
| **Automated tests** | Animation contract: every `ETDDLocomotionState` has a resolvable animation; no montage missing from the ability set; foot-slide metric within threshold; Adanna identity invariants (single weapon socket on left hip, no mirror scale, ornaments on left) |
| **Manual evidence** | Side-by-side locomotion video; foot-plant check on uneven laterite test terrain |
| **Exit criteria** | D-07 resolved and documented; foot-slide metric passes; combat animation reads clearly at gameplay distance |
| **Known limits** | Final art anim is a production dependency, not an engineering one |

## Stage 5 — Enemy and boss architecture

| | |
|---|---|
| **Entry** | Stage 3 and 4 accepted |
| **Scope** | `ATDDEnemyBase` + StateTree; perception; 2 archetypes; `UTDDBossPhaseGraph` + controller; **Great Root Mother** playable; Iron Elephant as data-only proof; perf capture |
| **Automated tests** | Phase graph reachability; every transition target exists; no non-terminal dead ends; Iron Elephant asset validates with zero new code; enemy perception respects occlusion; no snake-type spawn possible in CH04 manifests |
| **Manual evidence** | Great Root Mother fight recording (all phases); perf trace in arena |
| **Exit criteria** | Boss fight completable; arena frame time within budget; phase graph proven extensible by data |
| **Known limits** | Arenas are PROPOSED layouts (OAD-21); use blockout geometry only |

## Stage 6 — World simulation, exploration and traversal

| | |
|---|---|
| **Entry** | Stage 5 accepted |
| **Scope** | Chapter 1 (Forbidden Forest) integration: persistent level + World Partition, vistas, streaming, interactables, **Memory 1 end-to-end**, NPC/crowd baseline, canon rule enforcement in content |
| **Automated tests** | Great Root Mother tree visible from every major clearing; CH01 manifest violates no rules; Memory 1 passes all M1–M10 invariants; streaming budget within ceiling; interaction prompts resolve |
| **Manual evidence** | Full Chapter 1 playthrough recording incl. Memory 1 discovery sequence |
| **Exit criteria** | Chapter 1 playable start-to-boss; Memory 1 discoverable without markers; no canon-rule violations; performance within budget |
| **This is the vertical slice.** |

## Stage 7 — Progression and narrative systems

| | |
|---|---|
| **Entry** | Stage 6 accepted |
| **Scope** | Campaign graph; memory ledger + all seven definitions; ending eligibility; save/load v1→v2; codex; cinematic glue; audio states; credits + fictionality statement |
| **Automated tests** | Save round-trip; migration fixture; corrupt-save fallback to chapter start; Ending 3 requires all seven with current hashes; missing-one reports which; no blueprint object graph in save; codex entries carry `bFictionalMythology` |
| **Exit criteria** | Endings 1–3 all reachable in a test harness; save integrity proven; audio state machine covers all states |
| **Known limits** | Ending content (OAD-23) still to be defined by CD |

## Stage 8 — Campaign and chapter production

| | |
|---|---|
| **Entry** | Stage 7 accepted |
| **Scope** | Chapters 2–8 production; all bosses; environments per canon; cutscenes; audio; memories 2–7 (pending approval) |
| **Exit criteria** | Per-chapter acceptance matrix green; all canonical rules validated per chapter; all 7 memories discoverable; 3 endings playable |
| **Known limits** | Blocked by D-05 (ending content), D-06 (Ch08 design), D-10 (cultural review) |

## Stage 9 — Polish, optimisation, testing, release preparation

| | |
|---|---|
| **Entry** | Stage 8 accepted |
| **Scope** | Performance passes; LOD/streaming tuning; packaging; platform readiness; full regression; localisation readiness |
| **Exit criteria** | Perf report vs §13.1 budgets; packaged build smoke; regression suite green; cert checklist |
| **Known limits** | Console certification UNAVAILABLE in this environment |

---

## Performance gate (applies from Stage 3)

Measured per gate, against `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` §13.1. A missed budget is reported
with: the metric, the measured value, the target, the scene, the hardware, and a proposed fix. It is never
omitted.

## Canon gate (applies to every gate)

- `Tools/canon` tests green.
- No asset marked `Shippable` while any approval axis is false.
- Any new location/character ID present in the mirror with a correct `source`.
- Cultural review gates respected for: deity depictions, mask concepts, shrine/oath-ground designs.
