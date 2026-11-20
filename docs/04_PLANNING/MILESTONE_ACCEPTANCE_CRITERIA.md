# Milestone Acceptance Criteria

**Document ID:** TDD-PLAN-MAC-001 · **Version:** 1.0 · **Date:** 2026-11-20
**Conventions:** ACs marked **[A]** are inherited from accepted specifications (M1 spec v1.4, MEAD TDD-MEAD-001) and are unchanged. ACs marked **[N]** are new takeover criteria. Every AC has a measurement method. A milestone exits when ALL of its ACs have committed evidence (bundle path + `TDD_RESULT`/report in the ledger). "3 cold runs" = 3 separate process launches, no warm cache reuse, on the owner's Mac (both platforms from M6).

## M0 — Foundation [PASSED 2026-11-18; residual ACs below]

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M0.1 | Canonical project identity established (1 uproject, 1 module, 2 targets) | `TheDisobedientDaughter.uproject` builds `TheDisobedientDaughterEditor/Mac` + `.../Windows` | M0 record (committed) |
| M0.2 | Toolchain gate reproducible | `verify_toolchain.sh` passes on owner Mac (UE 5.8.4 CL 58902052, Xcode 27.2, macOS 27.2.1, M4/16 GB) | BuildEvidence bundle 20261118T202235Z (archive pending P-02) |
| M0.3 | Clean compile both targets, 0 errors/0 new warnings vs baseline | Build logs, exit status 0 | M0 record §3 |
| M0.4 | Project-owned automation 2/2 pass | `TDD_RESULT` lines, 2 passed | M0 record |
| M0.5 **[N]** | Evidence bundle schema operational: index.json + SHA256, committable text | Schema file + one archive | P-02 |
| M0.6 **[N]** | LFS live for content (first LFS push succeeds; `.gitattributes` covers content extensions) | `git lfs ls-files` non-empty | P-04 |
| M0.7 **[N]** | Packaging pipeline exists and launches: `pack_mac.sh` → packaged app starts to title/test map, clean exit | Package log + launch log | P-05 (Gate D) |
| M0.8 **[N]** | Core contracts compile and are unit-tested (tags, `FTDDDamageRequest`, provider declarations) | `TDD-Unit.Canon.*` green | P-08 |
| M0.9 **[N]** | Quality ledger live with M0 row | `QUALITY_LEDGER.md` committed | P-07 |

## M1 — Core movement (the integrity gate)

All 31 ACs of **M1 spec v1.4 §5** [A], unchanged: timing (AC-01…AC-04: 180° turn ≤ 0.5 s, acceleration ≤ 0.35 s, stop ≤ 0.20 s / 50 cm), slopes (AC-05…AC-09: 15/30/45° climbs ok, 50° blocked; slope 40° ok / 50° blocked), camera (AC-14…AC-18: penetration, angular stability, displacement, recovery, acquisition slew), input (AC-20…AC-23: buffering, remapping, devices), determinism (AC-24…AC-26: seed-reproducible, 100-run σ ≤ 5 cm, no state leaks), parity (AC-27: mouse+keyboard+gamepad), performance (AC-28: player frame cost ≤ 0.30 ms Development), stability (AC-29…AC-31: no floating capsule, no teleport-into-geometry, 3 cold runs clean).

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M1.32 **[N]** | M1-P1…P6 first-playable record complete (movement feel, camera, interaction volume, checkpoint, metrics overlay, 3 cold runs) | Manual record with metric values from `TDD.Movement.Report` CSV | Ledger + CSVs |
| M1.33 **[N]** | Agent 2 defects ①②③ closed: 100-run determinism with per-run variance + failure classification; test-name traceability (every `TDD-Functional.Movement.*` named in spec §5 exists); floor validation guard in every state exit | Named tests green in all 3 runs | Ledger diff review note |
| M1.34 **[N]** | Test map S7 in tree, blockout matches spec §4 dimensions | Map load test + dimension check | Map + test |
| M1.35 **[N]** | Evidence discipline proven: 3 cold runs, each with full bundle (build, tests, `TDD_RESULT`, CSVs), committed | 3 bundle paths in ledger | Ledger |

**Gate rule:** 31/31 + M1.32…35. If any AC-01…31 fails, M1 does not exit; the failure is triaged (spec bug → documented review + ADR; implementation bug → fix). No AC is weakened to pass the gate (Roadmap Rule 2).

## M2 — Traversal + forest slice

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M2.1 **[A]** | E1/E2 exit revalidation (TraversalExitRevalidation) — exit re-checked before commitment; failed exit = abort path, never a silent drop | `TDD-Functional.Movement.TraversalExitRevalidation` green × 3 runs | Ledger |
| M2.2 **[A]** | E3–E7 abort paths per spec §3.2.2, incl. lethal+staggering precedence (Dead > Stagger), cinematic no positional fallback (E6), hold phase H0/4a ≤ 5 cm, 4b `MOVE_Falling`, mid-abort placement failure, mid-resolution forced transitions, budget-0 case, kill-plane (`FellOutOfWorld`) | `TDD-Functional.Movement.TraversalAbortPaths` green × 3 runs | Ledger |
| M2.3 **[A]** | `ResolveAbortFallback()` two-phase (relocation clamp [0,3] → hold), resolution ≤ 1 frame, no async | `TDD-Unit.Movement.FallbackResolution` (5+ spec assertions) green | Ledger |
| M2.4 **[A]** | Restoration exactly once per completed traversal (no double-restore, no skip); posture restored per taxonomy | Restoration-checklist test (per traversal type) green | Ledger |
| M2.5 **[N]** | No floating capsule after any traversal abort; no teleport into geometry (extends AC-29/30 to traversal) | Floor-trace assertion in every traversal exit; zero violations in 3 runs | Test + ledger |
| M2.6 **[N]** | Forest slice: World Partition streams a full traversal loop end-to-end with zero visible holes | Traversal gauntlet script on the slice; streaming log | Gauntlet report |
| M2.7 **[N]** | Streaming budget measurements recorded (B-12 data): stream-in time, resident locations, hitch count on slice | Streaming report vs B-12 caps (≤ 8 s, ≤ 12 locations, ≤ 1/10 min hitches) | Report in ledger |
| M2.8 **[N]** | PCG scatter seeded + reproducible; foliage ≤ 60k HISM instances in slice | Seed recorded; instance count measured | Report |
| M2.9 **[N]** | Navigation: bake reproducible from map data; AI-reachable volume covers the slice play area | Bake hash compare + coverage test | Report |

## M3 — Combat foundation

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M3.1 **[A]** | MEAD P2 exit: full player-vs-dummy loop — light 4-chain (cancel from frame after active), heavy (no cancel after commit), block (guard-ready 0.08 s), parry (0.15 s window → attacker stagger), dodge (i-frames 0.11–0.44 s verified against AC), stagger, death | Training-room loop executed; every action observed with correct outcome | Capture + ledger |
| M3.2 **[A]** | No double-hits on any attack (dedup) | `TDD-Unit.Combat.HitDedup` + 10-hit-per-attack gauntlet | Ledger |
| M3.3 **[A]** | Every hit produces complete feedback (VFX placeholder + audio placeholder + camera + hitstop) — feedback map 100% | Feedback-completeness audit table (event → cue) with zero gaps | Audit in ledger |
| M3.4 **[A]** | Damage taxonomy 100%: non-staggering / staggering / lethal / lethal+staggering / posture-promotion (same-frame, Dead > Stagger) all resolve per M1 spec §3.2.1 | Taxonomy matrix suite green (all rows × all defender states) | Ledger |
| M3.5 **[A]** | Deterministic combat cases: seeded 10-case battery (attack sequences with exact input timestamps) reproduces byte-identical outcome logs | Battery CSV committed; 3-run compare | Ledger |
| M3.6 **[N]** | Combat frame cost within budget: combat component ≤ 1.5 ms game thread in reference scene (MEAD §15.2) | Insights scope report | Ledger |
| M3.7 **[N]** | MM spike decision recorded: foot-slide baseline ≤ 5 cm on lab set (or documented deferral with reason) | Spike report | Ledger |
| M3.8 **[N]** | Lock-on: soft/hard acquisition per MEAD §4.3 with hysteresis; no target flicker in 60 s combat loop | Acquisition test + loop capture | Ledger |

## M4 — Enemy AI + world simulation

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M4.1 **[A]** | MEAD P4 exit: 3 archetypes behaviourally distinct (attack style, spacing, reaction) | Archetype behaviour table + encounter captures | Ledger |
| M4.2 **[A]** | Concurrent-attacker caps hold: 6 enemies, 60 s, concurrent attacks ≤ 1 (measured, not assumed) | `TDD-Functional.AI.TokenLimitsSimultaneousAttackers` green × 3 | Ledger |
| M4.3 **[A]** | Token policy deterministic under seed; phase selector weighted per ADR-0006 (pure, seeded) | `TDD-Unit.AI.TokenPolicy/PhaseSelectorWeights` green (1000-iteration seed sweep) | Ledger |
| M4.4 **[A]** | Aggro: sight/hearing/damage perception fires correct state transitions; de-aggro after 8 s out-of-range (data) | `TDD-Functional.AI.AggroOnSight` + de-aggro test | Ledger |
| M4.5 **[A]** | Pilot boss (Great Root Mother, placeholder mechanics): 3 phases, all transitions reachable, deterministic | Phase graph gauntlet (all transition paths) + seeded tests | Ledger |
| M4.6 **[N]** | Scenario battery (QUALITY_PLAN §5): 8 scripted scenarios (ambush, flanking, player death mid-aggro, boss arena entry, checkpoint respawn during aggro, 8-enemy room, cinematic during aggro, save during aggro) — all pass with expected end states | Scenario CSV + end-state assertions | Ledger |
| M4.7 **[N]** | AI perf: AI ≤ 2.0 ms game thread in 8-enemy encounter (MEAD §15.2); ≤ 14 AI agents active (B-12) | Insights scope report | Ledger |
| M4.8 **[N]** | NPC tier model: Ch.1 population asserts exactly against the 29-scene register (TR-3 mirror), zero double-counts (TR-2) | Count reconciliation report | Ledger |

## M5 — Graphics & vertical slice

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M5.1 **[A]** | Budgets become law: `TDD-Perf.ReferenceScene.CH01_Encounter` at 60 fps on reference HW — frame buckets (game ≤ 6.0 ms, GPU ≤ 16.0 ms), ≤ 10 M visible Nanite tris, ≤ 3,000 non-Nanite draws, VRAM ≤ 8 GB, RAM ≤ 10 GB | Baseline .utrace + CSV on reference HW (identity recorded) | Ledger |
| M5.2 **[N]** | Controlled screenshot set vs approved boards: 10 fixed camera positions in the forest slice, captured on reference HW, presented to CD for sign-off (per QUALITY_PLAN §1 method) | Capture set + CD sign-off record | Ledger + captures |
| M5.3 **[N]** | Material library: 100% of slice surfaces use library materials (no ad-hoc); PBR standards doc committed | Material inventory + doc | Ledger |
| M5.4 **[N]** | VFX: every combat event has its effect; per-emitter particle budget measured; no frame-time regression vs M3 baseline (regression rule) | VFX inventory + budget table + perf delta | Ledger |
| M5.5 **[N]** | Production Adanna imported via GLB pipeline; identity locks verified (25, LEFT-temple cuffs/coral beads, LEFT-cheek scar, no gold/mirroring — M1 art spec); technical validation per MEAD §8.5 | Validation report + turnaround capture | Ledger |
| M5.6 **[N]** | Slice loop: forest → first encounter → memory anchor → checkpoint → chapter transition, streaming-ready (≤ 2 s stream, no pop) | Loop gauntlet + streaming log | Ledger |
| M5.7 **[N]** | Windows + Mac parity of visuals: same capture set on both platforms, differences documented (Metal = dev-level per D-19) | 2 capture sets + delta notes | Ledger |
| M5.8 **[N]** | **M7-00 content staffing decision recorded** (owner) with named capacity and a 4-week production rhythm plan | Decision record (issue comment / ADR) | Ledger |

## M6 — Systems integration

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M6.1 **[A]** | MEAD P6 menu loop: title → options → load → pause → title, all screens reachable by mouse+keyboard+gamepad; rebinding persists through save/load | `TDD-Unit.Narrative.*` + UI parity automation; manual loop on gamepad | Ledger |
| M6.2 **[A]** | Persistence: round-trip byte-identical (`TDD-Unit.Persistence.RoundTrip`); atomic-write interrupt → no corruption; migration across 2 schema versions works | Named suites green × 3 | Ledger |
| M6.3 **[A]** | Six endings resolve correctly per truth table (incl. "truth known does not absolve"); memory discovery persists through death + reload | `TDD-Unit.Narrative.ConditionEval/MemoryCounting` + death/reload scenario | Ledger |
| M6.4 **[A]** | Cinematics: skip leaves state consistent; every shot streaming-ready | `TDD-Functional.Cinematic.*` green × 3 | Ledger |
| M6.5 **[N]** | Audio: feedback map 100% (every combat/world/UI event emits its mapped cue — automation asserts event fire); submix hierarchy per ADR-0009; no pop/click in 20-min soak | Audit table + event-fire report + soak log | Ledger |
| M6.6 **[N]** | Pseudo-loc build: all UI strings via String Tables; pseudo-loc build runs without overflow/cut-off in 20 sample strings | Build + visual check | Ledger |
| M6.7 **[N]** | Windows: full evidence bundle on reference PC (build + all TDD suites + package) — R-21 closed | Windows bundle committed | Ledger |
| M6.8 **[N]** | Accessibility: shake scale, motion blur off, FOV slider, camera assist all functional + persisted; parity matrix 100% bound on 3 devices | Options tests + parity automation | Ledger |
| M6.9 **[N]** | Flow: chapter transition with loading screen + failure path (load fails → clean error, no softlock); respawn from fell-out-of-world | Transition gauntlet + fault-injection test | Ledger |

## M7 — Content, chapters 1 → 8

Per chapter c (c = 1…8), the chapter gate record contains:

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M7.c.1 **[A]** | Performance: chapter reference encounter at 60 fps on reference HW within MEAD §15.2/15.3 budgets | Per-chapter .utrace + CSV | Ledger |
| M7.c.2 **[N]** | Content completeness: every designed element (encounters, boss, memories, checkpoints, lore) present per chapter design doc; inventory reconciled 100% | Content inventory vs design doc, zero unexplained gaps | Ledger |
| M7.c.3 **[N]** | Visual sign-off: controlled capture set vs approved boards (QUALITY_PLAN §1), CD sign-off recorded | Captures + sign-off | Ledger |
| M7.c.4 **[N]** | Narrative state: quest flags, memory counts, ending-relevant conditions verified at chapter entry/exit (deterministic) | State dump compare (expected vs actual flag set) | Ledger |
| M7.c.5 **[N]** | Save/load at 3 points in the chapter: byte-identical world state restore (position, flags, world objects, aggro reset policy) | 3 × restore-compare tests | Ledger |
| M7.c.6 **[N]** | Population exact against register (TR-4); zero double-counts (TR-2) | Count reconciliation report | Ledger |
| M7.c.7 **[N]** | Cultural compliance: sacred vocabulary per consultant sign-off (CD-2); canon status fields validated (TR-17) | Validator report + sign-off | Ledger |

Chapter wave exits: wave 1 (ch.1–3) → wave 2 (ch.4–6) → wave 3 (ch.7–8, OAD-48 gate for ch. 8).

## M8 — Optimization & stability

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M8.1 **[A]** | All MEAD §15 budgets met on reference HW in the reference scene + worst chapter: 60 fps sustained, 1% lows ≥ 50, VRAM ≤ 8 GB, RAM ≤ 10 GB, hitches > 50 ms ≤ 1/10 min, chapter load ≤ 15 s cold / 5 s warm | Full budget report per location | Ledger |
| M8.2 **[N]** | Zero unmeasured optimizations: every optimization commit carries before/after .utrace evidence (owner rule 7) | Commit → evidence link audit, 100% | Ledger |
| M8.3 **[N]** | 2-hour soak on reference HW: zero crashes, zero memory growth > 100 MB over 2 h, hitch rate within budget | Soak log + memory curve | Ledger |
| M8.4 **[N]** | Full gauntlet (start → ch. 8 → one ending, scripted) passes unattended on reference HW × 3 | 3 gauntlet reports | Ledger |
| M8.5 **[A]** | Regression rule enforced for the duration: any merge breaching > 5 % frame-time or > 100 MB VRAM is blocked (MEAD §15.4) | Merge log audit | Ledger |

## M9 — Full validation & QA

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M9.1 **[N]** | Validation matrix (RRP §2) 100% executed with linked evidence per row | Matrix with 100% evidence links | RRP report |
| M9.2 **[N]** | Eight QA disciplines complete (RRP §3): each with scenarios executed + defect register entries | Per-discipline report | Ledger |
| M9.3 **[N]** | Defects: all P0/P1 closed with resolution evidence; P2 either closed or in a documented deferral list with player-impact rationale (no silent deferrals) | Defect register final state | Ledger |
| M9.4 **[N]** | Save/load soak: 100 cycles, checksum-verified, zero corruption | Soak report | Ledger |
| M9.5 **[N]** | Regression: full TDD suite × 3 cold runs × 2 platforms, zero failures | 6 bundles | Ledger |

## M10 — Packaging & release

| AC | Criterion [A/N] | Measurement | Evidence |
|---|---|---|---|
| M10.1 **[N]** | All 11 release gates (RRP §6) pass with actual evidence (no gate may be "waived" without an owner-ratified ADR) | Gate table in final report | RRP report |
| M10.2 **[N]** | Release builds on all confirmed platforms (Windows primary; Mac; PS5 iff D-16): versioned, installed from clean machine, launched, played 30 min | Install/launch/play logs per platform | Ledger |
| M10.3 **[N]** | Crash reporting per Q-22 decision (ADR): opt-in implemented + tested, or documented opt-out with store-compliance check | Implementation test / compliance note | Ledger |
| M10.4 **[N]** | Licensing audit: 100% of content assets conform to ADR-0104 rules (provenance recorded); no unlicensed content | Audit report | Ledger |
| M10.5 **[N]** | Final release-readiness report (RRP §8) delivered: every claim carries an evidence path; auditable by a stranger | The report itself | RRP report |
