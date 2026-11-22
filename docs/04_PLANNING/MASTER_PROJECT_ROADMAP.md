# Master Project Roadmap — The Disobedient Daughter

**Document ID:** TDD-PLAN-ROADMAP-001 · **Version:** 2.0 (accelerated) · **Date:** 2026-11-20
**Status:** PROPOSED FOR REVIEW — no gameplay implementation until this plan is ratified (P-01), per owner instruction.
**v2.0 change note (owner review pass):** v1.0's 13–14-month execution model is **replaced** by the owner-directed **4–8-week fast-track** (owner: "Our target is to deliver the game within approximately 4–8 weeks… Develop a credible accelerated execution model. Do not simply shorten the dates"). What does NOT change: milestone definitions and ACs (MILESTONE_ACCEPTANCE_CRITERIA), the accepted M1 spec v1.4 (AC-01…31), the 21 ADRs, frozen contracts (dep map §3), the evidence rules, and the quality bar. The fast-track is a change of *execution model* (parallelism, daily integration, verification distribution, scope ladder), not of standards. v1.0 inconsistencies fixed in this pass: milestone names (M8 = optimization, M9 = QA, M10 = release — the dep-map graph was wrong, now corrected), reference-PC timing (now one authoritative date: **Day 0**, TR-18), RRP G-02 (now correctly AC-01…31).
**Companions:** INDEX.md (set overview) · TECHNICAL_RESEARCH_REGISTER.md (TR-01…TR-19) · SYSTEM_REQUIREMENTS.md (S01–S24) · SYSTEM_DEPENDENCY_MAP.md · MASTER_WORK_BREAKDOWN.md v2.0 · MILESTONE_ACCEPTANCE_CRITERIA.md v1.1 · RISK_AND_BLOCKER_REGISTER.md v1.2 · QUALITY_ENGINEERING_PLAN.md v1.1 · RELEASE_READINESS_PLAN.md v1.1 · DECISION_RATIFICATION_REPORT.md (D-10…D-25 + new).
**Accountable:** Takeover Lead (TL), the agent on branch `arena/553fb02d-tdd`. Owner = project owner (Mac build machine, decisions, CD authority).

## 1. What this roadmap is (and is not)

- A **reconciliation** of the owner's M0–M10 groupings with the **accepted baseline** (M1 spec v1.4 with AC-01…31, MEAD TDD-MEAD-001 P0–P8, the 21 ADRs, Agent 1/2/3/4 deliverables). Groupings honored; nothing discarded.
- An **accelerated execution model** organized around a 4–8-week window: **Checkpoint A at week 4** (verified playable core) and **Checkpoint B at week 8** (Chapter 1 release candidate within the approved scope ladder, §5).
- **Dependency-aware and evidence-first**: every exit requires a committable `TDD_RESULT` evidence bundle + ledger entry. "Looks right" is not an exit.
- **Honest about what fits:** the complete 8-chapter commercial game does not fit 8 weeks at the required quality bar under any staffing level this plan can assume (the content production alone is the dominant cost — WBS v2.0 §11). The plan maximizes *complete, quality, shippable* scope inside the window and submits every scope adjustment explicitly (§5) for owner approval — no silent cuts, no lowered ACs (Rule 6).

## 2. Baseline reconciliation (unchanged from v1.0 — retained for traceability)

| Owner phase | Accepted-baseline mapping |
|---|---|
| M0 foundation | **Done and verified** (2026-11-18, owner Mac) + residual hygiene (WBS §0) |
| M1 core movement | M1 spec v1.4: AC-01…31 + M1-P1…P6 + first-playable gate — the integrity gate |
| M2 traversal & environment | M1 spec §3.7 contract (E1–E7) + World Partition on forest slice |
| M3 combat | MEAD §5 + ADR-0004 + M1 spec §3.2.1–3.2.3 + training room |
| M4 enemies & AI | ADR-0006 + ADR-0107 + MEAD P4; placeholders until CD-3 |
| M5 graphics & vertical slice | MEAD §15 budgets become law; look-dev + perf baseline on reference PC |
| M6 systems integration | MEAD P6 (menu loop, pseudo-loc, 2-version persistence) + Windows + accessibility |
| M7 content & chapters | Content waves; under fast-track, **ch. 1 in-window (SA-1), ch. 2–8 post-RC** |
| M8 optimization | MEAD §15.4 regression rules; profiling-evidence-only (owner rule) |
| M9 QA & hardening | RRP 6A/6B: validation matrix + 8 disciplines + defect register |
| M10 packaging & release | RRP 6C/6D: perf sign-off, compliance, 11 gates, final report |

Milestone **names and ACs are fixed**: M7 = content integration, M8 = optimization/stability, M9 = full QA, M10 = packaging/release (dep map §2 is the authority). MEAD P0–P8 mapping: P0 = M0 (done); P1 = M1; P2 = M3; P3 spans M3/M5; P4 = M4; P5 spans M2/M5; P6 = M6; P7 = M8; P8 = M9/M10.

## 3. Rules of the road (binding from P-01)

1. **No uncontrolled implementation** until this roadmap + dependencies + architecture are reviewed (owner instruction).
2. **M1 spec v1.4 AC-01…31 unchanged.** Necessary changes require documented review + ADR — never a silent edit.
3. **No milestone exit on unproven work.** Exit = evidence bundle (D-07) + ledger entry + named ACs green on the owner's Mac (and Windows from W2). NOT EXECUTED/BLOCKED ≠ pass.
4. **No silent simplification** of traversal/combat contracts (owner instruction).
5. **No placeholder asset presented as production-ready** (owner instruction; QUALITY §7). Anything shipped must be production-ready *or not shipped*.
6. **Never accelerate by removing tests, ignoring defects, or lowering acceptance standards** (owner instruction, Phase 5E).
7. **No optimization claim without profiling evidence** (owner instruction, Phase 6C).
8. **Single source of truth:** this plan set + the ledger. No duplicate/conflicting architecture; TL verifies all delegated work before merge (§7).
9. **Scope adjustments only via the SA register (§5)** — each explicitly identified, impact-stated, owner-approved. This is the *only* mechanism that changes what ships in-window.
10. **Claim discipline (TR-19):** engine-behaviour statements are classified [DS-G]/[BUD]/[EN-V]/[ST]/[UNV]; no [UNV] claim may be reported as fact.

## 4. The accelerated execution model (4–8 weeks)

### 4.1 Shape of the target (what the window buys)

| Point | Deliverable | Quality bar |
|---|---|---|
| **W1–2** | Core contracts frozen; movement + state machine + camera in and verified daily; combat/AI **pure cores** (no-UE C++) written and passing agent-side; test map S7; Windows CI live (W2); content team producing (character rig, combat anim set, modular env kit) | Every merge batch verified by the daily train; pure-core evidence per commit |
| **W3–4** | **M1 gate (W3): AC-01…31 in 3 cold runs.** M2 traversal (E1–E7 exact) + forest slice (World Partition, PCG scatter). Combat data model + hit detection integrated; training room. **CHECKPOINT A (W4): verified playable core** — movement + traversal + combat vs dummy + 1 archetype, save/load smoke, on Mac (3 cold runs) + Windows CI green. Dev assets explicitly labelled interim | Milestone gates M1/M2 exit on their real ACs; nothing waived |
| **W5–8** | M3 combat complete (W5): full player kit + damage pipeline + taxonomy 100%. M4 AI + pilot boss (W6). ch. 1 content integration (W5–W7): production modular environment, look-dev vs boards, production Adanna, VFX/audio feedback, UI/settings/save/flow, 1–2 memories. M8 perf baseline + optimization (W7) on reference HW. M9 QA + defect closure (W8). M10 packaging + **CHECKPOINT B (W8): Chapter 1 RELEASE CANDIDATE** — 11 release gates evaluated, final readiness report delivered | RC scope production-ready within SA-approved scope; all 11 gates with real evidence; zero unlabelled interim in the package |
| **W8 →** | Post-RC waves (ch. 2–8, remaining 6 bosses, remaining endings/memories, full score) at the **same gate definitions and quality bar** | Each wave exits through the identical per-chapter gates (MAC M7.c) |

**What genuinely does NOT fit 8 weeks at this quality bar** (stated up front, not discovered late): 8 chapters of production environment; 7 full boss sets; 6 full ending cinematics; the complete musical score; all 7 memories. These are the SA-adjusted post-RC items. If the owner requires all of them in-window, the alternatives are: (a) more human content capacity than Scenario A (estimate in §4.4), or (b) accepting labelled interim content in the shipped build — which violates Rule 5 and is therefore not a plan option, only a documented trade-off the owner may choose.

### 4.2 Weekly plan (deliverables, priorities, checkpoints)

**W0 (ratification week, days 0–2):** P-01 ratified (incl. SA register, D-12 tier, D-26, D-27). **Day-0 orders: reference PC, content team mobilized, NVMe (D-18).** M0 evidence archived + M0′ run (owner, 1 command). LFS live. ADR-0109 committed. CD-3 / Q-14 / CD-2 approval kickoffs started (needed by W3). Pure-core convention + gauntlet framework designed.
**W1:** Contracts (P-08) d1–d2. Track T1: state machine + CMC + movement (M1-S3) + test map S7 (P-09). Track T2: combat pure core (M3-01/03/04) + AI pure core (M4-01/02) — passing agent-side under g++ daily. Track T3 (TL): daily train script, gauntlet framework, ledger, merge pipeline. Owner: **daily Mac test train (60 min, fixed time)** starts d1. PC in transit. Content: Adanna rig + base anim set; modular env kit v0. *W1 exit: all 9 frozen contracts live; movement visibly working on the train; 6+ pure-core suites green.*
**W2:** T1: M1-S1/S2 (world sweep 100-run + floor validation), S4 (collision edges). T2: hit detection + damage integration vs contract (M3-02), block/parry logic (M3-05 core). T3: Windows bring-up on the arrived PC (M6-08 pulled forward) → **Windows CI node live W2**. Content: combat anim set in progress; env kit v1 (core modular pieces). *W2 exit: M1 candidate AC-01…13 evidence; Windows suite parity run 1 (expect green + known Metal-delta list).*
**W3:** T1: camera (M1-S5) + input (M1-S6) + metrics (M1-S7) → **M1 gate W3 (3 cold runs, AC-01…31 + M1.32–35)**. T2: traversal pure core (M2-01/02: candidate detection + `ResolveAbortFallback` two-phase, all spec assertions). T3: M4-03 perception + StateTree scaffolding starts; training room layout. Content: combat anim set delivered (retargeted); Adanna production model in progress. *W3 exit: M1 milestone GATE — the project's integrity checkpoint. If it fails, we stop and fix process, not ACs.*
**W4:** T1: traversal integration (M2-03/04: warp + E1–E7 suites) → **M2 gate W4**. T2: M3-05/06 world integration (block/parry/death on live dummy). T3: M2-05/06 (WP on forest slice + PCG scatter) + streaming measurements. **CHECKPOINT A (W4):** verified playable core — 8-point report; owner go/no-go for W5–8 scope (SA register confirmation in practice). *Content: Adanna production model delivered (W4 hard date — gates M5 look-dev); env kit v2 (chapter-appropriate scale).*
**W5:** T1: M2-07 (navigation) + slice polish (M2-08). T2: **M3 gate W5** (full kit, taxonomy 100%, training room loop, case battery). T3: M4-04 pilot encounter (token caps measured) + M4-05 boss graph importer. **M5 look-dev starts** on reference PC (M5-02) against delivered Adanna + env kit. *Content: ch. 1 environment assembly from modular kit (PCG-seeded); VFX combat set; SFX set.*
**W6:** T1: M4-06 pilot boss full loop (3 phases, seeded transitions). T2: M3-07 lock-on + combat camera rig; M5-04 VFX integration. T3: M6-01 narrative core (pure) + M6-06 persistence (round-trip/migration) on live world; M6-05 flow (transitions/loading/failure path). **M4 gate W6.** *Content: ch. 1 encounter + boss arena content; 1–2 memory anchors; UI art direction pass.*
**W7:** T1: M6-04 UI (HUD/pause/settings/rebinding/codex) + M6-07 pseudo-loc + M6-09 accessibility/parity. T2: M5-03 material library + M5-05 import pipeline (production Adanna in) + M5-04 audio feedback map. T3: M8-01 reference-scene baseline + **1440p/60 validation (TR-18 procedure)** + M8-03 optimization passes (measured-only) + Windows parity (all suites, both platforms). *Content: ch. 1 lighting look-dev vs boards; audio beds; boss presentation.*
**W8:** T1+T2: M9-01…04 (validation matrix scoped to RC, 8 QA disciplines, defect closure, save soak). T3: M8-05 2-h soak + M8-06 full gauntlet × 3 + M10-01 packaging (Windows + Mac) + M10-04 **final readiness report** (11 gates). **CHECKPOINT B (W8): ch. 1 RC.** Owner: release decision (release / hold / extend window to W10–12 for additional scope). *Content: ch. 1 final pass; store asset kit (M10-03).*

### 4.3 Daily execution protocol (integration + evidence, every day)

- **08:00 — Sync (15 min):** TL posts the day's plan (per-track task IDs); blockers flagged; owner confirms train time.
- **Continuous — Agent tracks:** write code + pure-core suites (g++, evidence per commit); feature branches only (`feat/tN-task`); **no work on the integration line directly**; contract-touching changes require TL review before merge.
- **12:00 & 17:00 — Merge batches (TL):** each batch = compile + pure-core suites + contract-compliance diff review (TL, ~10 min/branch) → merge to `arena/553fb02d-tdd` (integration line). Merge criteria as §7. Ledger row per batch.
- **18:00 — Mac test train (owner, 60 min, one command):** `run_daily_train.sh` = build (Mac + queue Windows) + all TDD suites queued since last green + gauntlets for the day's systems + evidence bundle auto-archived → ledger row + one-line status posted to Issue #1 (parser-driven). **The train is the project's heartbeat; a failed train blocks merges next morning until triaged.**
- **Night — Windows CI (from W2):** reference PC auto-runs build + full suite on each integration push; evidence archived; failures triaged in morning sync.
- **Friday — Checkpoint report (8-point, §8)** + risk/defect triage + next-week plan; owner 30-min review call (or written).

**Why this removes the old bottleneck:** v1.0 integrated at milestone ends (a 2–4 week queue of unverified code, one verification at the gate). v2.0 verifies daily, per track, on two machines plus agent-side pure cores — the verification loop shrinks from *weeks to hours*, which is the actual source of the acceleration (not "more agents").

### 4.4 Resources (what the plan requires)

| Resource | Requirement | Consequence if missing |
|---|---|---|
| **Agent tracks (3 additional Arena sessions + TL = this session)** | T1 core/movement/traversal (WS-1); T2 combat/AI (WS-2/3); T3 systems/UI/world-integration (WS-4/5/7); TL = integration, review, ledger, gates | Throughput halves per missing track; critical path (T1) unaffected until W5, then slips 1:1 |
| **Owner: 60 min daily test train + 30 min Friday review + 24 h decision SLA** | The Mac is the UE verification authority (ADR-0012: agents cannot compile UE code) | Without the train, everything queues → the plan is not executable; this is the #1 owner commitment (DA-01) |
| **Content team (Scenario A): 1 environment artist, 1 character/animation artist, 0.5–1 VFX, 0.5 audio — 2.5–4 FTE from W0** | The only way ch. 1 reaches *production* quality by W8 (modular kit → assembly, Adanna + combat anims by W4 hard date) | Scenario B: W8 deliverable becomes a labelled **dev-quality core milestone** — no release claim (Rule 5). The RC simply does not exist; Checkpoint A still stands as a real, verified deliverable |
| **Reference PC (D-12, Day-0 order; min $750 / recommended ~$1,500 — TR-18)** | Windows CI from W2; all perf/visual sign-off; min-spec validation | Without it: no Windows CI (Mac-only, single-threaded verification), no perf sign-off, RC unshippable on primary platform |
| **External NVMe (D-18)** | Mac build/DDC speed | Slower train, not blocking |
| **CD approvals by W3:** CD-3 archetypes, Q-14 boss mechanics, CD-2 consultant engaged | Real content in ch. 1 (else SA-2/SA-5 deepen: pilot boss with labelled mechanics, archetype stays placeholder) | Scope deepens, not quality lowers |

**Capacity honesty (owner: "Do not assume that adding agents automatically increases throughput"):** 3 tracks + TL is the ceiling for safe parallelism at this integration discipline. Rationale: (a) **review capacity** — the TL reviews every merge batch; > ~25 merge batches/week degrades review quality and becomes the bottleneck; (b) **shared dependencies** — the state machine, damage pipeline, and camera are single-owner surfaces (dep map §3 contracts); more agents on them means more conflicts, not more progress; (c) **one Mac + one CI** — verification is a serial resource per machine, so the marginal value of a 4th engineering track is near zero until W6; (d) **content** is the true parallel frontier and it is human-led — adding agents there does not produce approved art. The throughput lever is therefore: *verification distribution (3 surfaces: agent-side g++ / Mac train / Windows CI) + contract freeze (parallel-safe work) + content team*, in that order.

### 4.5 Parallelization map (what runs simultaneously, and why it is safe)

| Weeks | Track T1 | Track T2 | Track T3 | Content (human) | Safety basis |
|---|---|---|---|---|---|
| W1 | M1-S3, P-09 | M3-01/03/04, M4-01/02 (pure cores) | P-08, F-01/F-02 (train/gauntlet), ledger | Adanna rig + anims; env kit v0 | Pure cores test against **frozen contracts (P-08)**; no two tracks touch one surface |
| W2 | M1-S1/S2/S4 | M3-02, M3-05 core | M6-08 Windows bring-up → CI live | Combat anim set; env kit v1 | Same; T3 isolated (tooling) |
| W3 | M1-S5/S6/S7 → **M1 gate** | M2-01/02 (pure) | M4-03 (scaffold) | Combat anims delivered; Adanna model | M2 pure core starts pre-M2 because the contract is M1 spec §3.7 (accepted, frozen) |
| W4 | M2-03/04 → **M2 gate** + **Checkpoint A** | M3-05/06 integration | M2-05/06 (WP + PCG) | Adanna model **delivered (hard date)**; env kit v2 | Traversal = T1 sole owner; WP = T3 sole owner |
| W5 | M2-07/08 | **M3 gate** | M4-04/05; M5-02 look-dev | ch.1 env assembly; VFX combat set | Combat complete before AI consumes it (damage pipeline) |
| W6 | M4-06 pilot boss | M3-07; M5-04 VFX | M6-01/05/06 (narrative/flow/save) | ch.1 encounters; 1–2 memories; UI direction | Narrative core is pure (agent-side tested) — parallel-safe from W1 contracts |
| W7 | M6-04/07/09 (UI/pseudo-loc/accessibility) | M5-03/05 (materials/Adanna import) | M8-01/03 (baseline/opt) + Windows parity | ch.1 lighting vs boards; audio; boss presentation | UI/audio/materials are separate surfaces; perf baseline only after content lands |
| W8 | M9 all (QA) | M9 all + defect fixes | M8-05/06, M10-01/04 | ch.1 final pass; store assets | QA is deliberately serial (whole game) — parallel QA fragments evidence |

**Contract safety rule:** the parallelism above is legal *only* because dep map §3 contracts freeze at P-08 (W1 d2). From W1 d2 onward, a track may build against a contract but may not change it (contract-change process, MEAD §13.3 + ADR).

### 4.6 Automation & AI-assisted levers (what is actually used, and limits)

1. **Daily test train (F-01):** one command → build + queued suites + gauntlets + auto-archived evidence + auto ledger row + auto one-line issue update. Turns 60 min of owner time into a mechanical, auditable step.
2. **Gauntlet automation (F-02):** deterministic input scripts (key/timeline CSV) replayed by Automation Framework — all E-paths, combat battery, AI scenarios, traversal marathon, full-game run. Regression = replay + diff, no manual play (manual play reserved for feel checks, recorded).
3. **Agent-side pure cores (TR-19 T13):** all arbitration/policy/transition/condition/serialization logic in UE-independent C++ (g++ 12.2 verified in-workspace 2026-11-20; precedent: dodge math 18/18 in-sandbox, TR-14) → tested on every agent commit, zero Mac queue for the logic layer. **Limit:** UE-dependent code is agent-unverifiable (ADR-0012) and always goes through the train/CI.
4. **Windows CI node (W2+):** reference PC auto-builds/tests on integration pushes — doubles machine capacity, runs while the Mac is free for look-dev/editor work.
5. **Content automation:** PCG seeded scatter + procedural dressing (TR-02), modular environment kit (1 kit → 8 chapters by variation), data-driven content importers (boss graphs ADR-0107; encounter/population/quest/event-map CSV→asset importers, F-03), material library auto-assignment, string-table pipeline, LFS, packaging scripts. Designers/agents author *data*; code is written once.
6. **Evidence automation:** `TDD_RESULT` parser → ledger + issue one-liner per train (extends existing `parse_automation_report.py`).
7. **AI-assisted (honest limits):** AI code + test generation (this workflow; every output still gated by the suites — no bypass). AI-assisted content generation (texture/prop variations, draft VFX, temp music beds) is permitted **only as labelled interim** under Rule 5 and ADR-0104 provenance rules, **and only if the owner approves the AI-content policy (D-26)**; shipped hero assets (Adanna, boss models, combat animation, final score) require human production quality + CD sign-off — AI does not substitute for them in this plan. AI-assisted QA (defect triage, test-case suggestion) used throughout, human-verified.
8. **Bottleneck removals (explicit):** milestone-end integration → daily (F-01); approval delays → 24 h decision SLA + SA register batch-approved at P-01 (one approval, not per-item); duplicated work → one contract list, one defect register, one ledger, C-05 stays parked (no duplicate telegraph implementation); Mac queue → split three ways (agent-side / Mac / Windows).

## 5. Scope adjustment register (SA — the only mechanism that changes what ships in-window)

Each SA is **proposed, not applied**: it takes effect only when ratified at P-01 (DECISION_RATIFICATION_REPORT §3). Impact: H = player-visible loss vs the full 8-chapter design; M = partial; L = minor. All are reversible by post-RC waves at the same quality bar.

| SA | Adjustment (vs v1.0 full-scope plan) | Impact | Why it is required for 8 weeks | Reversibility |
|---|---|---|---|---|
| **SA-1** | **RC scope = Chapter 1 complete + verified core loop; chapters 2–8 ship as post-RC waves** (same per-chapter gates) | H (vs full game) | 8 production environments × (modeling, lighting, content, QA) does not fit 8 weeks at quality under any available staffing; ch. 1 is the complete demonstration of every system | Waves 2–8 continue W9+; nothing is discarded |
| **SA-2** | **Bosses in RC: 1** (pilot Great Root Mother; real mechanics if Q-14 ratified by W3, else labelled pilot mechanics + post-RC rework) | M | 7 full boss sets = 7 × (design, content, tuning, QA); the ADR-0107 framework ships complete so the other 6 are data+content, not re-engineering | Other 6 in waves (data-driven, cheap) |
| **SA-3** | **Endings in RC: resolver + truth table verified (unit level); one playable ending sequence; remaining 5 ending cinematics post-RC** | M | Ending cinematics are content-heavy; the deterministic resolver (which is the game's promise) is fully shipped | 5 sequences in waves |
| **SA-4** | **Memories in RC: 1–2 (ch. 1) with full persistence; remaining 5 post-RC** | M | Memory content = set-dressing + narrative + QA each | Waves |
| **SA-5** | **Cinematics in RC: checkpoint/memory beats + ending teaser; full shot list post-RC** | M | Sequencer shots are CD-paced content | Waves |
| **SA-6** | **If Scenario B (no content team): W8 deliverable = verified dev-quality core milestone (labelled interim assets), NOT a release candidate** — no release claim is made (Rule 5) | H (no RC) | Stated so the schedule never implies production quality that human content did not produce | RC materializes when content team lands |
| **SA-7** | **PS5 excluded from RC** (D-16 option kept; Sony application post-RC if confirmed) | L (in-window) | Sony onboarding lead time (entity + GDD + devkit) is months; devkit-gated work cannot start in-window | Post-RC if D-16 = yes |
| **SA-8** | **Audio in RC: full SFX + functional adaptive music beds (production-mixed); full original score post-RC** | M | Original score composition/mixing is CD-paced; gameplay feedback (which the player *hears on every action*) is complete | Score in waves |

**Explicit non-SA (no owner approval needed — these are engineering, not scope):** Windows parity from W2 (was M6); Windows CI from W2; look-dev starting W5 (was M5); pure-core agent-side testing; daily train. These are execution changes consistent with the frozen contracts.

## 6. Workstreams & tracks

Ownership is unchanged from v1.0 (one workstream per system, single owner — no duplicate ownership), now mapped to the 4 parallel tracks:

| Track | Workstreams owned | Primary tasks (WBS v2.0) | Entry contracts |
|---|---|---|---|
| **T1 — Core & Movement** | WS-1 (S02 S03 S04 S05) + WS-4 (S10) | P-08 (shared d1–d2), P-09, M1-S1…S7, M2-01…08 | M1 spec v1.4; MEAD §4 |
| **T2 — Combat, AI & Boss** | WS-2 (S06 S07) + WS-3 (S08 S09) | M3-01…08, M4-01…06, M3-07 | P-08 contracts; damage pipeline |
| **T3 — Systems, World & Quality** | WS-5 (S13 S14 S18 S21) + WS-7 (S16 S17 S22) + WS-8 (S01 S15 S23 S24) | P-01…P-07, F-01…F-03, M2-05/06, M5-02…05, M6-*, M8-*, M9-*, M10-* | All (TL track) |
| **TL — Takeover Lead (this session)** | Integration, contracts, ledger, gates, review | Merge batches, train triage, gate evidence, reports | — |
| **Content (human, Scenario A)** | Character/animation, environment, VFX, audio, narrative content | Per §4.2 weekly content column | GLB standard (D-25), identity locks (M1 art spec), ADR-0008 canon |

WS-6 (Graphics & VFX, S19) is T3-led from W5 with the content team producing (look-dev is a shared T3+CD activity).

## 7. Integration management (daily, not end-of-milestone)

- **Integration line:** `arena/553fb02d-tdd` (protected). Feature branches `feat/tN-<task>` cut from it; **no direct commits to the line.**
- **Merge criteria (unchanged from v1.0, enforced per batch):** (1) compiles (Mac; Windows via CI from W2); (2) task's named TDD tests exist + pass; track regression suite passes; (3) no regression — pure-core suites green; from W5 the perf regression rule applies (> 5 % frame-time or > 100 MB VRAM blocks, MEAD §15.4); (4) evidence/ledger row exists; (5) no frozen-contract change without cited ADR; (6) **TL diff review** for contract compliance + duplicate architecture before merge (owner instruction, Part 4).
- **Automated regression:** agent-side pure-core suites per commit; Mac daily train (all world suites + gauntlets, 60 min); Windows CI per integration push from W2; gauntlets at checkpoints and gates.
- **Conflict rule:** two tracks touching the same frozen surface → TL sequences; never parallel ownership of one surface.
- **Ledger:** one row per merge batch + per train + per gate (date, branch, commit, task IDs, test summary, evidence paths, perf deltas, defects, risks, decisions). The ledger is the single progress record.

## 8. Progress reports

- **Daily (auto):** one line to Issue #1 per train — `TRAIN <date> <commit> <passed>/<total> <gauntlets> <evidence-path> <defects-open>` (parser-generated).
- **Friday / checkpoint (8-point, full format):** (1) milestone & date; (2) scope delivered (task IDs, ACs green); (3) evidence (bundle paths, test counts, `TDD_RESULT` lines, perf deltas); (4) defects (opened/closed, severities); (5) risks (register deltas, top-3); (6) decisions (ADRs, owner decisions); (7) blockers (what is needed, impact if unaddressed); (8) next (entry checklist + critical-path status: on track / at risk / behind, with the specific reason).
- A report that cannot fill point 3 with real paths is not a report.

## 9. Critical path & the exact tasks that threaten the deadline

```
P-01 ratification + Day-0 orders (PC, content, NVMe)
  → P-08 contracts (W1 d2)
  → M1-S3 state machine + CMC (W1–W2, 3 aw — LARGEST serial engineering block)
  → M1 gate (W3: 3 cold runs) ── integrity gate; failure = process fix, not AC change
  → M2-02 ResolveAbortFallback (W3, 1.5 aw — highest edge-case density, E3–E7)
  → M2 gate (W4) ──► CHECKPOINT A
  → M3-02/04 hit detection + arbitration (W4–W5, 3 aw)
  → M3 gate (W5)
  → M4-04/06 pilot encounter + pilot boss (W5–W6, 5.5 aw)
  → M4 gate (W6)
  → ch.1 content integration (W5–W7 — content-team-paced; Adanna model W4 hard date)
  → M8-01/TR-18 1440p@60 validation + M9 QA (W7–W8)
  ──► CHECKPOINT B: ch.1 RC (W8)
```

**Deadline threats (exact tasks → mitigation):**
1. **M1-S3** (state machine/CMC, 196 pairs) — largest serial block. Mitigation: pure-core transition table first (agent-side tested), TL daily review, scope of world tests batched for the train.
2. **M2-02** (`ResolveAbortFallback` two-phase, E3–E7) — highest bug density in the whole plan. Mitigation: pure-logic first with all spec §3.2.2–3.2.3 budget assertions before any montage work; fuzz placement gate.
3. **Daily train bandwidth (owner 60 min)** — if the train slips, the queue compounds. Mitigation: DA-01; the train command is one-click; if a day is genuinely lost, the next day's batch is pre-triaged (nothing new enters until green).
4. **Reference PC shipping delay (used market)** — loses Windows CI (W2) and/or look-dev (W5). Mitigation: Day-0 order, TR-18 spec pre-selected; fallback = order the recommended tier new (2–3 days) — cost delta is small against the schedule risk.
5. **Adanna production model + combat anim set (W4 hard date)** — content critical path; gates M5 look-dev and M3 integration. Mitigation: content team from W0; mannequin retargeting pipeline (D-14) as labelled interim; if W4 slips, SA-6 activates (dev milestone, no RC claim) — the schedule never hides it.
6. **TL review capacity** — single reviewer, 3 tracks. Mitigation: merge batches capped (~25/week), pure-core evidence reduces review surface, contract freeze reduces conflict surface.
7. **CD-3 / Q-14 / CD-2 approvals after W3** — ch. 1 content reverts to placeholders → SA-2/SA-5 deepen. Mitigation: kickoffs at W0; the 24 h decision SLA applies to CD approvals routed through the owner.

## 10. Change management

- **Scope/AC changes:** documented review → ADR → owner ratification (Rule 2). **In-window scope changes: SA register only** (§5), owner-approved at P-01; mid-flight SA changes require a new owner approval + re-baselined WBS delta in the Friday report.
- **Architecture changes:** ADR + TL verification + ledger; frozen contracts only via MEAD §13.3.
- **Schedule changes:** re-baseline in WBS with the delta explained; permitted accelerators = the four levers in §4.6 + capacity adds in §4.4 (with the §4.4 capacity-honesty checks); **prohibited** = test removal, defect ignoring, AC lowering (Rule 6).
- **Research changes:** new TR entries; architecture-affecting verdicts → ADR.

## 11. Success definition (end-state)

By **W8**: a **Chapter 1 release candidate** — verified core loop (movement/traversal/combat per AC-01…31 + E1–E7 + combat kit), one pilot boss, 1–3 archetypes, 1–2 memories, checkpoints/save, UI/audio feedback, production modular environment with CD-signed look-dev, Windows + Mac builds, 11 release gates evaluated with actual evidence, and a final release-readiness report a stranger could audit. **By W8 + n waves**: the complete 8-chapter game, each chapter through the identical gates. Measured, not claimed — and if a wave slips, the report says so with the specific reason (Rule: a report with no limitations is not believed).
