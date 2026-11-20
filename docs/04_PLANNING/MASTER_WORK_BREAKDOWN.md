# Master Work Breakdown Structure (WBS)

**Document ID:** TDD-PLAN-WBS-001 · **Version:** 1.0 · **Date:** 2026-11-20
**Conventions:** Every task is a verifiable unit of work with named completion evidence. Owner = **AG** (agent), **OW** (owner, Mac machine), **CD** (creative direction/owner), **CT** (content production — external, Q-18). Effort = agent-weeks (aw) estimate; content tasks marked (CT) are excluded from the agent critical path and tracked separately. A task is DONE only when its evidence is committed or the ledger entry exists — never when the work "feels finished". Task IDs are stable; the ROADMAP references them.

## 0. Pre-M1 / foundation hygiene (immediately after ratification)

| ID | Task | M | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| P-01 | Owner ratification of D-10…D-18 + D-19…D-25 (comments on Issue #1 / ADR 0109+) | — | OW/CD | — | — | Written ratification (issue comment or ADR) |
| P-02 | Archive the existing M0 evidence bundle per T00 §9 commands | M0 | OW | 0.1 h | P-01 | `Saved/BuildEvidence/20261118T202235Z.zip` + sha256 in `docs/06_IMPLEMENTATION/evidence/m0_archive/` |
| P-03 | M0′ consolidated Mac run (build + tests + evidence) after takeover commit | M0 | OW | 0.5 h | P-01 | New `TDD_RESULT` bundle committed |
| P-04 | LFS provisioning: `.gitattributes` for content extensions + first LFS push rehearsal | M0 | OW/AG | 0.5 aw | P-01 | LFS files in tree; `git lfs ls-files` non-empty |
| P-05 | `pack_mac.sh` (RunUAT Cook+Package) + packaging runbook + first packaged-launch log (Gate D) | M0 | AG | 1 aw | P-01 | Committed packaging log; packaged app launch record in ledger |
| P-06 | ADR-0109: planning decisions D-19…D-25 recorded as ADR | M0 | AG | 0.25 aw | P-01 | ADR committed |
| P-07 | Quality ledger v1: ledger file + `TDD_RESULT` ingestion convention (D-07 format) | M0 | AG | 0.25 aw | — | `docs/06_IMPLEMENTATION/QUALITY_LEDGER.md` with M0 row |
| P-08 | Core contracts (S02): tags, `FTDDDamageRequest`, provider interface declarations, log categories | M0 | AG | 1 aw | P-03 | Compilation + `TDD-Unit.Canon.*` + contract checklist in ledger (dep map §3) |
| P-09 | Test map S7 (movement/traversal blockout; `TDD-Perf.ReferenceScene` seed geometry) | M0→M1 | AG | 1.5 aw | P-03 | Map loads; blockout matches spec §4 dimensions |

## 1. M1 — Core movement (gate: AC-01…AC-31)

Agent 1 execution scope S1–S6 (docs/06_IMPLEMENTATION/M1_EXECUTION_SCOPE) is the authoritative detail; WBS rows are the ledger view.

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M1-S1 | World-sweep integration tests for every `TDD-Functional.Movement.*` (Agent 2 defect ① closed: 100-run determinism, per-run variance, failure classification) | AG | 1.5 aw | P-08, P-09 | 100-run CSV + `TDD_RESULT` lines committed |
| M1-S2 | Floor/ground validation tests + Agent 2 defect ③ (floating-capsule guard, floor-trace assertion in every state exit) | AG | 0.5 aw | M1-S1 | Named tests green |
| M1-S3 | Character + `UTDDCharacterMovementComponent` + `UTDDCharacterStateMachine` (196 pairs, coyote, step smoothing, slope overrides) | AG | 3 aw | M1-S2 | All `TDD-Unit.Movement.*` green; AC-01…AC-13 candidate evidence |
| M1-S4 | Collision edge cases (step-up 45°, ledge hold, narrow gaps) — spec §3.3 rules | AG | 1 aw | M1-S3 | Edge-case tests green; AC-05…AC-09 evidence |
| M1-S5 | Camera system: five stability criteria recorder + `TDD.Camera.Report` + rig table (exploration/first-person) | AG | 2.5 aw | M1-S3 | AC-14…AC-18 evidence; sweep capture |
| M1-S6 | Enhanced Input: bindings, buffer, device parity (AC-27), remappable actions | AG | 1.5 aw | M1-S3 | AC-20…AC-23, AC-27 evidence |
| M1-S7 | Metrics harness: `TDD.Movement.Report` CSV (frame-stamped), metrics dashboard for P1–P3 | AG | 1 aw | M1-S3 | CSV per run committed |
| M1-S8 | Mannequin animation set for M1 (run/jump/dodge/mantle placeholders, labelled interim) | CT | 2 wks | P-01 | Clips in tree (LFS), clip inventory in ledger |
| M1-S9 | First-playable pass: test environment (P-09), one interaction volume (T36), checkpoint marker, metrics overlay | AG | 1 aw | M1-S6 | M1-P1…P6 record with metrics |
| M1-S10 | M1 verification: 3 cold Mac runs, evidence bundles, diff review vs spec v1.4, ledger entry | OW/AG | 1 aw | M1-S1…S9 | 31/31 `TDD_RESULT` + bundle + ledger entry |

**M1 gate:** AC-01…AC-31 all green in 3 cold runs + M1-P1…P6 + evidence archived. Nothing else may start "for real" until this passes (roadmap §3 rule 3).

## 2. M2 — Traversal + first real slice (forest)

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M2-01 | Traversal candidate detection + `FTDDTraversalCandidate` data asset (vault/mantle/ledge/drop/climb-ladder) | AG | 1 aw | M1 gate | Unit tests (pure) green |
| M2-02 | `ResolveAbortFallback()` / `ResolveHold()` — pure-logic implementation of spec §3.2.2–3.2.3 incl. all budget assertions | AG | 1.5 aw | M2-01 | `TDD-Unit.Movement.FallbackResolution` (5+ assertions per spec) green |
| M2-03 | Motion Warping + placeholder traversal clips (CT: 8–10 clips) | AG/CT | 1.5 aw / 1 wk | M2-01, M1-S8 | Warp convergence tests; clip inventory |
| M2-04 | E1–E7 functional suite (TraversalExitRevalidation + TraversalAbortPaths; incl. lethal+staggering precedence, cinematic no-drop, 4a/4b/4c, mid-abort failure, budget-0, kill-plane) | AG | 1.5 aw | M2-02, M2-03 | All named tests green in Mac run |
| M2-05 | World Partition setup on forest slice + data layers (time-of-day scaffold) | AG | 1.5 aw | M1 gate | Streaming traversal gauntlet (no holes) |
| M2-06 | PCG seeded scatter pass on forest (foliage/rocks within 60k HISM budget) | AG | 1 aw | M2-05 | Scatter with recorded seed; budget measured |
| M2-07 | Navigation volumes + bake pipeline for the slice | AG | 1 aw | M2-05 | Bake reproducible; coverage test |
| M2-08 | Forest slice blockout v2 (using in-tree GLB), camera rig table for traversal mode | AG | 1.5 aw | M2-05 | P7 record (first playable in real environment) |
| M2-09 | M2 verification + streaming measurements (B-12 closure data) | OW/AG | 1 aw | M2-04…08 | Evidence bundle + streaming report in ledger |

## 3. M3 — Combat foundation

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M3-01 | Attack data model: hit windows, cancel rules (light 4-chain, heavy), notify sampling — pure C++ | AG | 1.5 aw | M1 gate | `TDD-Unit.Combat.CancelRules` green (in-sandbox: no Mac needed) |
| M3-02 | Hit detection: custom channels, dedup, hit registration → `FTDDDamageRequest` | AG | 1.5 aw | M3-01, P-08 | `TDD-Unit.Combat.HitDedup` green |
| M3-03 | Attribute set + damage GAS effects (health/stamina/posture) + taxonomy mapping (ADR-0004) | AG | 1 aw | M3-02 | `TDD-Unit.Combat.DamageMath` green |
| M3-04 | Pipeline arbitration: same-frame posture promotion, Dead>Stagger, cinematic freeze, restoration→entry exactly once | AG | 1.5 aw | M3-03 | Taxonomy matrix 100% (spec §3.2.1) |
| M3-05 | Block/parry: guard-ready 0.08 s, parry 0.15 s window → attacker stagger | AG | 1.5 aw | M3-04 | `TDD-Functional.Combat.ParryStaggers` green |
| M3-06 | Reactions/stagger/hitstop data + death presentation (ragdoll) + flow handoff | AG | 2 aw | M3-04 | Stagger/Death rows of taxonomy green |
| M3-07 | Lock-on (soft/hard) + combat camera rig | AG | 1 aw | M3-02 | Acquisition + hysteresis tests green |
| M3-08 | Combat training room + dummy (per-chapter reference) | AG | 1 aw | M3-05 | Room playable; encounter loop documented |
| M3-09 | Combat animation set (CT: ~12 attacks + 10 reactions + stagger/death; provider-agnostic) | CT | 4–6 wks | M1-S8 | Clip inventory; provider switch test passes |
| M3-10 | MM spike (RG-03): corpus feasibility on the combat set, foot-slide baseline | AG | 1 aw | M3-09 (partial) | Spike report; decision: MM at M3 exit or deferred |
| M3-11 | M3 verification: player-vs-dummy full loop, deterministic case battery (QUALITY_PLAN §4) | OW/AG | 1 aw | M3-01…10 | Evidence bundle + case battery CSV + ledger |

## 4. M4 — Enemy AI + world simulation

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M4-01 | Combat director token policy (pure, seeded tests) | AG | 1 aw | M3-01 | `TDD-Unit.AI.TokenPolicy` green (in-sandbox) |
| M4-02 | Phase selector (declarative, seeded tests) | AG | 1 aw | M4-01 | `TDD-Unit.AI.PhaseSelectorWeights` green |
| M4-03 | Perception (sight/hearing/damage) + StateTree scaffolding for placeholder archetypes | AG | 2 aw | M4-01 | Scaffolding compiles; aggro smoke test |
| M4-04 | Pilot encounter: 6 placeholder enemies, token caps, 60 s concurrent-attack measurement | AG | 2.5 aw | M4-03 | `TDD-Functional.AI.TokenLimitsSimultaneousAttackers` green |
| M4-05 | Boss phase graph importer + validator (CSV/JSON → data asset) | AG | 1.5 aw | M4-02 | Importer tests; invalid graph rejected |
| M4-06 | Pilot boss (Great Root Mother, placeholder mechanics): 3 phases, deterministic transitions | AG | 3 aw | M4-05, M3 | Pilot gauntlet; seeded transition tests |
| M4-07 | NPC tier data model + register parser (mirrors Agent 2 fixtures; TR-1…TR-5) | AG | 1.5 aw | M2 gate | Parser tests against in-repo evidence JSONs |
| M4-08 | Mass setup for tiers 4–5 (budgeted) | AG | 1.5 aw | M4-07 | Crowd budget measured |
| M4-09 | Archetype content (CT): 3 ratified archetypes' animation/behaviour content — **gated on CD-3** | CT | 6+ wks | CD-3 | Per-archetype inventory + design sign-off |
| M4-10 | M4 verification: scenario battery (QUALITY_PLAN §5), AI perf scope report | OW/AG | 1 aw | M4-04…08, 09 (placeholders ok) | Evidence bundle + scenario CSV + ledger |

## 5. M5 — Graphics & vertical slice (ch. 1)

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M5-01 | **Reference PC build (D-12) + DX12 bring-up (RG-05) + calibration captures** | OW | order lead 1–2 wks | P-01 (decision), M2 | Calibration report: reference HW identity in ledger |
| M5-02 | Lighting pipeline + first look-dev on forest slice (Lumen HWRT) | AG | 3 aw | M5-01 | Controlled screenshot set A (dev) vs board |
| M5-03 | Material library + PBR standards (TR-02) | AG | 3 aw | M5-02 | Material library inventory; standards doc |
| M5-04 | Niagara VFX set: combat (hits/stagger/death/block/parry) + environment (fire/water/ambience) with per-emitter budgets | AG | 3 aw | M3, M5-03 | VFX inventory; budget measurement per emitter |
| M5-05 | Character import pipeline (proxy → mannequin → production, same code path; GLB standard TR-17) | AG | 1 aw | M3-09 | Pipeline runbook; production Adanna (CT content) imported with identity-lock validation |
| M5-06 | Adanna production character (CT: model/rig/textures/groom/costume per M1 art spec + approved refs) | CT | 8+ wks | CD identity approval | Technical validation report (MEAD §8.5) |
| M5-07 | Chapter 1 slice integration: forest → first encounter → memory → checkpoint → transition | AG | 2 aw | M4, M5-04 | P7 loop in real slice; streaming-ready |
| M5-08 | Vertical-slice gate: controlled captures vs approved boards (QUALITY_PLAN §1), perf gate on reference HW, CD sign-off | OW/CD/AG | 1 aw | M5-02…07 | Slice gate record with actual evidence |

## 6. M6 — Systems integration (audio, UI, narrative, flow, save, Windows)

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M6-01 | Narrative core: flags/conditions (pure), ending resolver truth table, memory FSM, quest flow | AG | 5.5 aw | M3 | All `TDD-Unit.Narrative.*` green (in-sandbox) |
| M6-02 | Cinematic subsystem + skip/streaming tests | AG | 3 aw | M5-07 | Named tests green |
| M6-03 | Audio service + submixes + combat feedback set (event-mapped) | AG | 4 aw | M3 | Feedback-completeness audit passes |
| M6-04 | UI framework: HUD, pause, map, settings/rebinding (gamepad-verified), codex/journal | AG | 7 aw | M1 | MEAD P6 loop: all screens all inputs |
| M6-05 | Flow subsystem: chapter transitions, loading + failure path, respawn integration | AG | 2 aw | M6-01 | Transition gauntlet green |
| M6-06 | Persistence: subsystem + round-trip + atomic-write-interrupt + migration (2 versions) | AG | 4.5 aw | M6-01, M6-05 | All `TDD-Unit.Persistence.*` green |
| M6-07 | Pseudo-loc build + String Table pipeline | AG | 1 aw | M6-04 | Pseudo-loc build runs |
| M6-08 | Windows build bring-up on reference PC (RG-05): build, test, package | OW/AG | 2 aw | M5-01 | Windows evidence bundle committed |
| M6-09 | Accessibility options + input parity matrix automation | AG | 3 aw | M6-04 | Parity automation green |
| M6-10 | M6 verification: integrated loop (menu → world → combat → save → load), both platforms | OW/AG | 1 aw | M6-01…09 | Evidence bundles (both platforms) + ledger |

## 7. M7 — Content integration, chapters 1 → 8 (content-dominated)

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M7-00 | **Content staffing/pipeline decision (Q-18/19) — the dominant schedule input; owner decision, not agent work** | OW/CD | decision | M5-08 | Production plan with named capacity |
| M7-01..08 | Per-chapter content waves: environments (CT), lighting (AG T61), enemy/NPC content (CT), boss content (AG T28 + CT), narrative content (AG T43 + CD), audio content (AG T50a + CD), cinematics (AG T46 + CD), population wiring (AG T35 + T57) | AG/CT/CD | ~21 aw agent + ~40+ wks content (CT, parallel) | M6-10; CD canon gates (CD-2, OAD-48 for ch.8) | Per-chapter gate record (same format as slice gate) |
| M7-09 | Chapter gate process: per chapter — perf gate (reference HW), CD sign-off, save/load + narrative state verified | OW/CD/AG | 1 aw/ch | M7-01..08 | 8 chapter gate records |

**M7 rule:** chapters stream in waves (1→2→3, then 4–6, then 7–8) once the ch.1 gate passes; content for later chapters is produced in parallel against frozen contracts — no re-architecture between chapters.

## 8. M8 — Optimization & stability

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M8-01 | Reference scene + capture automation on reference HW (`TDD-Perf.ReferenceScene.CH01_Encounter` full) | AG | 2 aw | M6-08 | Baseline .utrace + CSV archived |
| M8-02 | Per-system scope instrumentation audit (Insights scopes vs MEAD §15.2 buckets) | AG | 1 aw | M8-01 | All budget buckets measurable |
| M8-03 | Optimization passes: only against measured exceedances; each fix carries before/after evidence | AG | 6 aw | M8-02 | Per-fix evidence in ledger (no unmeasured "optimizations") |
| M8-04 | Regression rule enforcement: > 5 % frame-time or > 100 MB VRAM blocks merges into integration branch | AG | 0.5 aw | M8-01 | Rule in merge criteria (roadmap §6) |
| M8-05 | Soak: 2 h full-game play on reference HW (hitches, memory growth, crashes) | OW/AG | 1 aw | M8-03 | Soak log: hitches ≤ 1 × > 50 ms / 10 min; no memory growth; zero crashes |
| M8-06 | Gauntlet automation (full run: start → ch.8 → ending, scripted) | AG | 2 aw | M8-03 | Gauntlet script + pass report |

## 9. M9 — Full validation & QA

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M9-01 | Full validation matrix execution (Phase 6A — RELEASE_READINESS_PLAN §2) | AG/OW | 3 aw | M8 | Matrix 100% executed, evidence linked |
| M9-02 | Eight QA disciplines (Phase 6B — RRP §3): gameplay/camera/animation/combat/AI/save/visual/audio — with defect register | AG/OW/CD | 6 aw | M9-01 | Defect register with resolutions or justified deferrals (gate 11) |
| M9-03 | Defect fix loop: P0/P1 closed with evidence; P2 by decision | AG | 6 aw | M9-02 | Register entries closed with resolution evidence |
| M9-04 | Save/load soak: 100 cycles, checksum-verified | AG | 1 aw | M9-01 | Soak report |
| M9-05 | Regression: full TDD suite × 3 cold runs on both platforms | OW | 1 aw | M9-03 | 3 bundles |

## 10. M10 — Packaging & release

| ID | Task | Owner | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|
| M10-01 | Release packaging pipeline (Windows primary; Mac; PS5 only if D-16): versioned builds, installers, update path | AG | 2 aw | M9 | Packaging logs; clean-machine install tests |
| M10-02 | Platform compliance: store requirements, crash reporting (Q-22), licensing audit (ADR-0104 content rules) | OW/AG | 2 aw | M10-01 | Compliance checklists |
| M10-03 | Store assets: icons, screenshots, descriptions (CD), age rating materials | CD/OW | 2 wks | M5-08 | Asset set |
| M10-04 | Final release-readiness report (RRP §8): all 11 gates with actual evidence | AG | 2 aw | M10-01…03 | The report itself |
| M10-05 | Release candidate → release (owner decision) | OW | — | M10-04 | Version tag + announcement |

## 11. Effort summary & parallelism

| Milestone | Agent effort (aw) | Content (CT) | Calendar (with 2 parallel agent tracks + owner runs) |
|---|---|---|---|
| Pre-M1 | 4.5 | — | week 0–1 (after P-01) |
| M1 | 13 | 2 wks mannequin | weeks 1–5 |
| M2 | 9.5 | 1 wk clips | weeks 5–8 |
| M3 | 13 | 4–6 wks combat anim | weeks 8–12 (anim parallel) |
| M4 | 15.5 | 6+ wks archetypes (CD-3 gated) | weeks 12–16 (AI code ∥ ch.2 content) |
| M5 | 14 | 8+ wks Adanna production | weeks 16–20 (content ∥) |
| M6 | 28.5 | — | weeks 20–25 (3 tracks: UI / narrative / persistence) |
| M7 | 21 + 8 aw/ch gates | ~40+ wks (CT team) | weeks 25–45 (content-dominated, 3-wave) |
| M8 | 12.5 | — | weeks 45–50 |
| M9 | 17 | — | weeks 50–54 |
| M10 | 6 | 2 wks assets | weeks 54–56 |
| **Total** | **~160 aw** | **~60+ wks CT** | **~13–14 months from ratification** |

**Acceleration plan (Phase 2F):** the only safe accelerators are (a) parallel tracks — AI pure-logic (M4-01/02), narrative core (M6-01), persistence (M6-06), UI (M6-04) can each start as soon as their contract exists, not their parent milestone (contracts frozen per dep map §3); (b) content pipeline started at M5 with named capacity (M7-00 decision — the single biggest lever); (c) reference PC ordered at M2 exit, not M5 entry. **Prohibited accelerators** (Phase 5E): cutting tests, deferring defects, lowering ACs, skipping evidence.
