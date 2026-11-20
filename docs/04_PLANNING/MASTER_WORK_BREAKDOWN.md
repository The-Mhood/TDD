# Master Work Breakdown Structure (WBS)

**Document ID:** TDD-PLAN-WBS-001 · **Version:** 2.0 (accelerated) · **Date:** 2026-11-20
**v2.0 change note (owner review pass):** re-timed to the 4–8-week fast-track (ROADMAP v2.0 §4.2) with **Week** and **Track** columns; new F-tasks (fast-track infrastructure); verification assignments corrected per TR-19 T13 (agent-side g++ for UE-independent pure cores only; all UE-dependent verification via the daily Mac train + Windows CI); new §11 "what does not fit in-window" (post-RC waves). Task IDs from v1.0 are preserved for traceability; effort estimates unchanged where the work is unchanged.
**Conventions:** Every task is a verifiable unit with named completion evidence. Owner: **AG-T1/T2/T3** = agent tracks, **TL** = Takeover Lead, **OW** = owner (Mac machine, decisions), **CD** = creative direction, **CT** = content team (Scenario A, W0 start). Effort = agent-weeks (aw) unless marked (CT). A task is DONE only when its evidence is committed or the ledger row exists.

## 0. Foundation, Day-0 & fast-track infrastructure (W0–W1)

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| P-01 | Owner ratification: D-10…D-18, D-19…D-25, SA register, D-26 (AI content policy), D-27 (capacity/commitments) | 0 | OW | — | — | Written ratification (Issue #1 / ADR) |
| P-02 | Archive existing M0 evidence bundle (T00 §9 commands) | 0 | OW | 0.1 h | P-01 | `Saved/BuildEvidence/20261118T202235Z.zip` + sha256 in `evidence/m0_archive/` |
| P-03 | M0′ consolidated Mac run on the takeover branch | 0 | OW | 0.5 h | P-01 | New `TDD_RESULT` bundle committed |
| P-04 | **Reference PC: order Day 0 (TR-18 spec, tier per D-12); on arrival: Windows 11 + UE 5.8.4 install + toolchain gate + bring-up run (RG-05)** | 0–1 | OW/AG | 0.5 aw + OW 1 h setup | P-01 | PC identity (OS/GPU/driver/CPU/RAM/UE CL) in ledger; bring-up log |
| P-05 | LFS provisioning: `.gitattributes` + first LFS push rehearsal | 0 | OW/AG | 0.5 aw | P-01 | `git lfs ls-files` non-empty |
| P-06 | `pack_mac.sh` (RunUAT) + packaging runbook + first packaged-launch log (Gate D) | 1 | AG-T3 | 1 aw | P-03 | Committed packaging log; launch record in ledger |
| P-07 | ADR-0109: planning decisions D-19…D-25 + accelerated model + pure-core convention + daily protocol | 0 | TL | 0.25 aw | P-01 | ADR committed (status: Proposed → Ratified at P-01) |
| P-08 | **Core contracts: tags, `FTDDDamageRequest`, provider interfaces, log categories, state-table schema — frozen at W1 d2** (dep map §3 checklist signed) | 1 d1–2 | AG-T3 | 1 aw | P-03 | Compilation + `TDD-Unit.Canon.*`; contract checklist in ledger |
| P-09 | Test map S7 (movement/traversal blockout per spec §4 + reference-scene seed geometry) | 1 | AG-T1 | 1.5 aw | P-03 | Map loads; blockout dimensions verified |
| F-01 | **Daily test train: `run_daily_train.sh` (build + queued suites + gauntlets + evidence bundle + auto ledger row + auto issue one-liner) + queue management** | 1 | AG-T3/TL | 1 aw | P-03 | First train run green with committed evidence; one-liner posted |
| F-02 | **Gauntlet framework: deterministic input-script runner (key/timeline CSV → replayed via Automation) + result diffing (baseline vs current, byte-compare)** | 1–2 | AG-T3 | 1.5 aw | F-01 | E-path + combat-battery replays produce diffable logs |
| F-03 | **Data-content importers v1: encounter, population, event-map (VFX/audio), quest CSV/JSON → data assets (boss graphs per ADR-0107 already specified)** | 2–3 | AG-T3 | 1.5 aw | P-08 | Importer tests (valid + invalid inputs); one live content set per importer |
| F-04 | **Windows CI runner on the reference PC: auto build + full suite on integration push; evidence archive; failure alert to issue** | 2 | AG-T3 | 1 aw | P-04 | CI run on a real push, evidence committed |
| F-05 | **Pure-core harness: g++ test runner in-repo (`Tools/tests/pure/`), CI-equivalent per-commit check for T1/T2; UE-header ban on pure files enforced at merge review** (TR-19 T13) | 1 | AG-T3 | 0.5 aw | P-08 | Harness runs one contract suite; ban rule in merge criteria |
| F-06 | Quality ledger v1 + defect register scaffold + progress one-liner format (D-07) | 0–1 | TL | 0.25 aw | — | Files committed; M0 row present |
| F-07 | Content mobilization (Scenario A): team contracted, GLB pipeline + exchange standard (D-25) briefed, W4 hard dates agreed (Adanna model, combat anim set) | 0 | OW/CD | — | P-01 | Production plan with named capacity + dates in ledger |

## 1. M1 — Core movement (gate: AC-01…31) — **W1–W3, Track T1**

Agent 1 execution scope S1–S6 remains the authoritative detail; WBS rows are the ledger view. Pure-logic portions (state-transition table, buffer logic, slope rules) are written UE-independent first and pass agent-side (F-05) before UE integration.

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M1-S3 | Character + `UTDDCharacterMovementComponent` + `UTDDCharacterStateMachine` (196 pairs, coyote, step smoothing, slope overrides) — **critical path, starts W1 d2** | 1–2 | T1 | 3 aw | P-08, P-09 | All `TDD-Unit.Movement.*` green (pure core agent-side; world tests via train) |
| M1-S1 | World-sweep integration tests, all `TDD-Functional.Movement.*` (100-run determinism, variance, failure classification; Agent 2 ① closed) | 2 | T1 | 1.5 aw | M1-S3 | 100-run CSV + `TDD_RESULT` in train |
| M1-S2 | Floor/ground validation + Agent 2 ③ (floating-capsule guard in every state exit) | 2 | T1 | 0.5 aw | M1-S1 | Named tests green |
| M1-S4 | Collision edge cases (45° step-up, ledge hold, narrow gaps) per spec §3.3 | 2 | T1 | 1 aw | M1-S3 | Edge-case tests green |
| M1-S5 | Camera: five-criteria recorder + `TDD.Camera.Report` + rig table (exploration/first-person) | 3 | T1 | 2.5 aw | M1-S3 | AC-14…18 evidence; sweep capture |
| M1-S6 | Enhanced Input: bindings, buffer, device parity (AC-27), remappable actions | 3 | T1 | 1.5 aw | M1-S3 | AC-20…23, AC-27 evidence |
| M1-S7 | Metrics harness: `TDD.Movement.Report` CSV (frame-stamped) + dashboard for P1–P3 | 3 | T1 | 1 aw | M1-S3 | CSV per run committed |
| M1-S8 | Mannequin animation set for M1 (labelled interim) | 0–1 | CT | 2 wks | P-01 | Clips in tree (LFS) + inventory |
| M1-S9 | First-playable pass: interaction volume (T36), checkpoint marker, metrics overlay | 3 | T1 | 1 aw | M1-S6 | M1-P1…P6 record with metrics |
| M1-S10 | **M1 gate: 3 cold Mac runs, evidence bundles, diff review vs spec v1.4, ledger entry** | 3 | OW/TL | 1 aw | all | 31/31 `TDD_RESULT` + M1.32–35 |

## 2. M2 — Traversal + forest slice — **W3–W5, Tracks T1 + T3**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M2-01 | Traversal candidate detection + `FTDDTraversalCandidate` data asset (pure core first) | 3 | T1 | 1 aw | M1 gate | Unit tests agent-side green |
| M2-02 | **`ResolveAbortFallback()` / `ResolveHold()` — pure-logic, all spec §3.2.2–3.2.3 assertions** (highest edge-case density in plan) | 3 | T1 | 1.5 aw | M2-01 | `TDD-Unit.Movement.FallbackResolution` (5+ assertions) agent-side + train |
| M2-03 | Motion Warping + placeholder traversal clips (CT: 8–10 clips) | 4 | T1/CT | 1.5 aw + 1 wk | M2-01, M1-S8 | Warp convergence tests; inventory |
| M2-04 | E1–E7 functional suite (TraversalExitRevalidation + TraversalAbortPaths: lethal+staggering precedence, cinematic no-drop, 4a/4b/4c, mid-abort failure, budget-0, kill-plane) | 4 | T1 | 1.5 aw | M2-02/03 | All named tests green in train |
| M2-05 | World Partition on forest slice + data layers (time-of-day scaffold) | 4–5 | T3 | 1.5 aw | M1 gate | Streaming traversal gauntlet (no holes) |
| M2-06 | PCG seeded scatter (foliage/rocks, ≤ 60k HISM) | 5 | T3 | 1 aw | M2-05 | Recorded seed; budget measured |
| M2-07 | Navigation volumes + reproducible bake | 5 | T1 | 1 aw | M2-05 | Bake hash compare + coverage test |
| M2-08 | Forest slice blockout v2 (in-tree GLB) + traversal camera rig | 4 | T1 | 1.5 aw | M2-05 | P7 record (first playable in real environment) |
| M2-09 | **M2 gate + streaming measurements (B-12 closure data)** | 4 | OW/TL | 1 aw | M2-04…08 | Evidence bundle + streaming report (M2.6/2.7/2.8/2.9) |

## 3. M3 — Combat foundation — **W1 (pure) + W4–W5 (integration), Track T2**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M3-01 | Attack data model: hit windows, cancel rules (light 4-chain, heavy), notify sampling — **pure core, agent-side from W1** | 1 | T2 | 1.5 aw | P-08 | `TDD-Unit.Combat.CancelRules` green agent-side |
| M3-03 | Attribute set + damage math (health/stamina/posture, taxonomy mapping, ADR-0004) — pure core | 1 | T2 | 1 aw | M3-01 | `TDD-Unit.Combat.DamageMath` agent-side |
| M3-04 | Pipeline arbitration: same-frame posture promotion, Dead>Stagger, cinematic freeze, restoration→entry exactly once — **pure core** | 1–2 | T2 | 1.5 aw | M3-03 | Taxonomy matrix 100% agent-side (all 40 cells) |
| M3-02 | Hit detection: custom channels, dedup, registration → `FTDDDamageRequest` (UE integration) | 2–4 | T2 | 1.5 aw | M3-01, P-08 | `TDD-Unit.Combat.HitDedup` + train runs |
| M3-05 | Block/parry: guard-ready 0.08 s, parry 0.15 s → attacker stagger (integration) | 4 | T2 | 1.5 aw | M3-04 | `TDD-Functional.Combat.ParryStaggers` green |
| M3-06 | Reactions/stagger/hitstop data + ragdoll death + flow handoff | 4–5 | T2 | 2 aw | M3-04 | Stagger/Death taxonomy rows green |
| M3-07 | Lock-on (soft/hard) + combat camera rig | 6 | T2 | 1 aw | M3-02 | Acquisition + hysteresis tests |
| M3-08 | Combat training room + dummy | 4 | T2 | 1 aw | M3-05 | Room playable; loop documented |
| M3-09 | Combat animation set (~12 attacks + 10 reactions + stagger/death, provider-agnostic) | 1–4 | CT | 4–6 wks | M1-S8 | Inventory; provider switch test |
| M3-10 | MM spike (RG-03): corpus feasibility + foot-slide baseline | 5 | T2 | 1 aw | M3-09 (partial) | Spike report; adopt/defer decision |
| M3-11 | **M3 gate: player-vs-dummy full loop + deterministic case battery (QUALITY §4) × 3 runs** | 5 | OW/TL | 1 aw | M3-01…10 | Bundle + battery CSV + ledger |

## 4. M4 — Enemy AI + boss — **W2 (pure) + W5–W6 (integration), Track T2 (+T1 boss)**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M4-01 | Combat director token policy (pure, seeded) — **agent-side from W1–W2** | 1–2 | T2 | 1 aw | P-08 | `TDD-Unit.AI.TokenPolicy` agent-side (1000-iter sweep) |
| M4-02 | Phase selector (declarative, seeded, pure) | 1–2 | T2 | 1 aw | M4-01 | `TDD-Unit.AI.PhaseSelectorWeights` agent-side |
| M4-03 | Perception (sight/hearing/damage) + StateTree scaffolding (placeholder archetypes) | 3–4 | T2 | 2 aw | M4-01 | Scaffolding compiles; aggro smoke in train |
| M4-04 | Pilot encounter: 6 enemies, token caps, 60 s concurrent-attack measurement | 5 | T1 | 2.5 aw | M4-03, M3 | `TDD-Functional.AI.TokenLimitsSimultaneousAttackers` × 3 |
| M4-05 | Boss phase graph importer + validator | 5 | T2 | 1.5 aw | M4-02 | Importer tests; invalid graph rejected |
| M4-06 | Pilot boss (Great Root Mother): 3 phases, all transitions, deterministic (seeded) | 6 | T1 | 3 aw | M4-05, M3 | Pilot gauntlet (all paths) + seeded tests |
| M4-07 | NPC tier data model + register parser (TR-1…TR-5, mirrors Agent 2 fixtures) | 4 | T3 | 1.5 aw | P-08 | Parser tests vs in-repo evidence JSONs |
| M4-08 | Mass setup tiers 4–5 (budgeted) | 6 | T3 | 1.5 aw | M4-07 | Crowd budget measured |
| M4-09 | Archetype content (3 ratified archetypes) — **gated on CD-3 (by W3)** | 2–6 | CT | 6+ wks | CD-3 | Per-archetype inventory + design sign-off |
| M4-10 | **M4 gate: scenario battery (QUALITY §5) + AI perf scope report** | 6 | OW/TL | 1 aw | M4-04…08 | Bundle + scenario CSV + ledger |

## 5. M5 — Graphics & ch. 1 slice — **W4–W7, T3-led + CT**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M5-01 | Reference PC calibrated (part of P-04); **1440p/60 validation per TR-18 (3 × 10-min, reference scene)** | 2 + 7 | OW/TL | 0.5 aw | P-04, M8-01 scene | Calibration + first budget report in ledger (machine named) |
| M5-02 | Lighting pipeline + first look-dev on forest slice (Lumen HWRT; Mac = DEV-HW, PC = sign-off) | 5–7 | T3/CD | 3 aw | P-04, M2 | Controlled capture set A vs boards |
| M5-03 | Material library + PBR standards (TR-02) | 7 | T3 | 3 aw | M5-02 | Library inventory + standards doc |
| M5-04 | Niagara VFX set: combat + environment, per-emitter budgets | 5–7 | T3/CT | 3 aw | M3, M5-03 | VFX inventory; per-emitter budget table |
| M5-05 | Character import pipeline (GLB standard) + **production Adanna in (CT model, W4 hard date)** + identity-lock validation | 6–7 | T3/CT | 1 aw | M5-02, CT model | Pipeline runbook; MEAD §8.5 technical validation report |
| M5-06 | Adanna production character (model/rig/textures/groom/costume per M1 art spec + approved refs) | 0–4 | CT | 8+ wks | CD identity approval | Technical validation report + turnaround capture |
| M5-07 | ch. 1 slice integration: forest → first encounter → memory → checkpoint → transition | 6–7 | T3 | 2 aw | M4, M5-04 | Loop gauntlet; streaming-ready |
| M5-08 | Vertical-slice gate: captures vs boards (CD sign-off) + perf gate (reference HW) | 7 | OW/CD/TL | 1 aw | M5-02…07 | Slice gate record with actual evidence |

## 6. M6 — Systems integration — **W6–W7, all tracks**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M6-01 | Narrative core: flags/conditions (pure, agent-side from W1), ending resolver truth table, memory FSM, quest flow | 1–6 | T3 | 5.5 aw | P-08 | All `TDD-Unit.Narrative.*` agent-side + train |
| M6-02 | Cinematic subsystem + skip/streaming tests | 6 | T3 | 3 aw | M5-07 | Named tests green |
| M6-03 | Audio service + submixes + combat feedback set (event-mapped) | 6–7 | T3 | 4 aw | M3 | Feedback-completeness audit (event-fire) |
| M6-04 | UI framework: HUD, pause, map, settings/rebinding (gamepad-verified), codex/journal | 7 | T1 | 7 aw | M1 | MEAD P6 loop: all screens all inputs |
| M6-05 | Flow subsystem: chapter transitions, loading + failure path, respawn integration | 6 | T3 | 2 aw | M6-01 | Transition gauntlet green |
| M6-06 | Persistence: subsystem + round-trip + atomic-write-interrupt + 2-version migration | 6 | T3 | 4.5 aw | M6-01/05 | All `TDD-Unit.Persistence.*` green |
| M6-07 | Pseudo-loc build + String Table pipeline | 7 | T1 | 1 aw | M6-04 | Pseudo-loc build runs |
| M6-08 | **Windows build bring-up on reference PC (RG-05): build + tests + package → CI live** | 2 | T3 | 2 aw | P-04 | Windows evidence bundle; CI (F-04) operational |
| M6-09 | Accessibility options + input parity matrix automation | 7 | T1 | 3 aw | M6-04 | Parity automation green |
| M6-10 | **M6 verification: integrated loop (menu → world → combat → save → load), both platforms** | 7 | OW/TL | 1 aw | M6-01…09 | Bundles × 2 platforms + ledger |

## 7. M7 — Content integration (ch. 1 in-window; ch. 2–8 post-RC, SA-1)

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M7-00 | **Content staffing: Scenario A confirmed at W0 (F-07) — no separate M7-00 decision point under the fast-track** | 0 | OW/CD | — | P-01 | Production plan in ledger |
| M7-01 | ch. 1 content wave: environment (CT modular + PCG), lighting (T3), encounters + archetypes (CT), pilot boss content (T2 + CT), 1–2 memories (CD + T3), audio SFX/beds (CT), UI pass (CT), population wiring (T3) | 5–8 | all | ~12 aw + 4–6 wks CT | M6-10 partial; CD-3/CD-2 by W3 | Per-system inventories + gate record |
| M7-02 | **Chapter 1 gate record** (MAC M7.c.1…c.7: perf, completeness, visual sign-off, narrative state, save × 3, population, cultural) | 8 | OW/CD/TL | 1 aw | M7-01 | Gate record with evidence |
| **Post-RC waves (W9+)** | ch. 2–8 waves: per-chapter content + per-chapter gate records (MAC M7.c identical); remaining 6 bosses (M7-03, data-driven per ADR-0107); endings 2–6 cinematics (M7-04); memories 3–7 (M7-05); full score (M7-06) | 9+ | all | ~9 aw/ch + ~5 wks CT/ch | ch. 1 gate + capacity sustained | 8 chapter gate records total |

## 8. M8 — Optimization & stability — **W7, Track T3**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M8-01 | Reference scene + capture automation (`TDD-Perf.ReferenceScene.CH01_Encounter`) + TR-18 1440p/60 validation | 7 | T3/OW | 2 aw | M6-08, M5-04 | Baseline .utrace + CSV archived; machine named |
| M8-02 | Scope instrumentation audit (Insights scopes vs MEAD §15.2 buckets) | 7 | T3 | 1 aw | M8-01 | All budget buckets measurable |
| M8-03 | Optimization passes — measured-only, before/after .utrace per fix (Rule 7) | 7–8 | T3 | 6 aw | M8-02 | Per-fix ledger rows |
| M8-04 | Regression rule live: > 5 % frame-time or > 100 MB VRAM blocks merges (MEAD §15.4) | 7 | T3 | 0.5 aw | M8-01 | Rule enforced in merge criteria |
| M8-05 | 2-h soak on reference HW (hitches, memory growth, crashes) | 8 | OW/TL | 1 aw | M8-03 | Soak log (hitches ≤ 1/10 min; zero crashes; no growth) |
| M8-06 | Full gauntlet (start → ch. 8 boundary → one ending, scripted) × 3 unattended | 8 | T3 | 2 aw | M8-03 | 3 gauntlet reports |

## 9. M9 — Full validation & QA (scoped to approved RC scope, SA-1) — **W8**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M9-01 | Validation matrix (RRP §2) scoped to RC: all rows executed with linked evidence | 8 | all | 3 aw | M8 | Matrix 100% linked |
| M9-02 | 8 QA disciplines (RRP §3) with defect register | 8 | all | 6 aw | M9-01 | Per-discipline reports |
| M9-03 | Defect fix loop: P0/P1 closed with evidence; P2 by owner decision | 7–8 | T1/T2 | 6 aw | M9-02 | Register entries closed |
| M9-04 | Save/load soak: 100 cycles, checksum-verified | 8 | T3 | 1 aw | M9-01 | Soak report |
| M9-05 | Regression: full TDD suite × 3 cold runs × 2 platforms | 8 | OW | 1 aw | M9-03 | 6 bundles |

## 10. M10 — Packaging & release (RC) — **W8**

| ID | Task | Wk | Trk | Effort | Depends | Completion evidence |
|---|---|---|---|---|---|---|
| M10-01 | Release packaging: Windows (primary) + Mac; versioned; clean-machine install → launch → 30-min play | 8 | T3/OW | 2 aw | M9 | Per-platform install/launch/play logs |
| M10-02 | Platform compliance: crash reporting (Q-22 → ADR), licensing audit (ADR-0104), store requirements | 8 | OW/T3 | 2 aw | M10-01 | Compliance checklists + audit report |
| M10-03 | Store assets: icons, screenshots, description, age-rating materials | 7–8 | CD/OW | 2 wks | M5-08 | Asset set |
| M10-04 | **Final release-readiness report (RRP §8): 11 gates with actual evidence + 20-path audit** | 8 | TL | 2 aw | M10-01…03 | The report itself |
| M10-05 | Release decision (owner) | 8 | OW | — | M10-04 | Version tag + decision record |

## 11. Effort summary, parallelism & what does NOT fit in-window

| Block | Agent effort (aw) | Content (CT) | Weeks |
|---|---|---|---|
| W0–W1 (P-*, F-*) | 8.5 | 1 wk (mobilization + mannequin) | 0–1 |
| M1 (S1–S10) | 13 | M1-S8 | 1–3 |
| M2 (01–09) | 9.5 | 1 wk clips | 3–5 |
| M3 (01–11) | 13 | 4–6 wks combat anims | 1 (pure) + 4–5 (integration) |
| M4 (01–10) | 15.5 | 6+ wks archetypes (CD-3) | 1–2 (pure) + 5–6 |
| M5 (01–08) | 14 | 8+ wks Adanna + env kit | 2, 5–7 |
| M6 (01–10) | 28.5 | — | 6–7 |
| M7 ch. 1 wave | 12 + 1 gate | 4–6 wks (CT) | 5–8 |
| M8 (01–06) | 12.5 | — | 7–8 |
| M9 (01–05) | 17 | — | 8 |
| M10 (01–05) | 7 | 2 wks assets | 8 |
| **In-window total** | **~140 aw across 3 tracks + TL** | **Scenario A: 2.5–4 FTE × 8 wks** | **8** |

**Parallelism math (why 3 tracks + TL is the ceiling):** ~140 aw ÷ 8 weeks = ~17.5 aw/week required; 3 tracks at ~1.5 aw/track-week of *merged* output (net of review/conflict overhead) ≈ 4.5–6 aw/week merged + TL infra/review work — the gap is closed by (a) pure-core work counting double (agent-side tested, no train queue) and (b) content running on its own human clock. A 4th engineering track adds < 1 aw/week merged at this review capacity (§4.4 of the roadmap) — adding it is not throughput-neutral, it is review-negative.

**Does NOT fit in-window (post-RC waves, same gates/bar):** ch. 2–8 environments + content (~45+ aw + ~40 wks CT); bosses 2–7 (~24 aw + content); endings 2–6 cinematics; memories 3–7; full score; PS5 (SA-7); MM adoption if spike defers. These are *deferred*, not *deleted* — each re-enters through the identical per-chapter/per-content gates.

**Prohibited accelerators (Rule 6, restated):** removing tests, ignoring defects, lowering ACs, claiming placeholder content as production, optimizing without profiling evidence.
