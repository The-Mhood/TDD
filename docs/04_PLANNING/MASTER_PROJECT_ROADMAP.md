# Master Project Roadmap — The Disobedient Daughter

**Document ID:** TDD-PLAN-ROADMAP-001 · **Version:** 1.0 · **Date:** 2026-11-20
**Status:** PROPOSED FOR REVIEW — no uncontrolled implementation starts until this plan (with its dependencies and initial architecture) is reviewed and ratified (owner instruction; P-01).
**Companions:** SYSTEM_REQUIREMENTS.md (S01–S24) · SYSTEM_DEPENDENCY_MAP.md · MASTER_WORK_BREAKDOWN.md (P/M1…M10 tasks) · MILESTONE_ACCEPTANCE_CRITERIA.md · RISK_AND_BLOCKER_REGISTER.md · TECHNICAL_RESEARCH_REGISTER.md · QUALITY_ENGINEERING_PLAN.md · RELEASE_READINESS_PLAN.md
**Accountable:** Takeover Lead (TL), the agent on branch `arena/553fb02d-tdd`. Owner = the project owner (Mac build machine, decisions, CD authority).

## 1. What this roadmap is (and is not)

- It is a **reconciliation** of the owner-proposed M0–M10 groupings with the **accepted baseline** (M1 spec v1.4 with AC-01…AC-31, MEAD TDD-MEAD-001 phases P0–P8, the 21 ADRs (ADR-0001…0013, ADR-0101…0108), the Agent 1/2/3/4 deliverables). Per the owner's instruction, the M0–M10 list is treated as *proposed groupings, not permission to discard existing milestone definitions*: every accepted AC and contract survives verbatim and is mapped to a milestone below.
- It is **dependency-aware**: nothing is scheduled before its prerequisites; the critical path is explicit (§8).
- It is **evidence-first**: every exit gate requires a committable evidence bundle in the `TDD_RESULT` format (D-07) and a quality-ledger entry. "Looks right" is not an exit.

## 2. Baseline reconciliation (owner M0–M10 → accepted definitions)

| Owner phase (proposed) | Content as proposed | Accepted-baseline mapping (what it actually contains) |
|---|---|---|
| M0 foundation | Canonical project, toolchain, compile, tests, evidence | **Already done and verified** (M0 record, 2026-11-18, owner Mac). Kept as the project's foundation milestone; WBS §0 adds the residual hygiene (LFS, packaging script, evidence archive, contracts). |
| M1 core movement | Movement, camera, input, first playable | **= M1 spec v1.4**: AC-01…AC-31 + M1-P1…P6 + first-playable gate. This is the gate that defines the rest of the project; it is not compressible. |
| M2 traversal & environment | Vault/mantle/climb, forest slice | M1 spec §3.7 contract (E1–E7) + MEAD P1/P2 environment start (World Partition on the forest slice, first real map). |
| M3 combat | Attacks, hits, damage, stagger, death | MEAD §5 + ADR-0004 + M1 spec §3.2.1–3.2.3 (damage pipeline, posture, taxonomy) + combat training room. |
| M4 enemies & AI | Archetypes, perception, encounters | ADR-0006 (StateTree + perception + combat director) + ADR-0107 (boss phase graphs) + MEAD P4; placeholder archetypes until CD-3 ratification. |
| M5 graphics & vertical slice | Lighting, materials, VFX, ch.1 slice | MEAD §15 budgets become **law** here; Lumen/Nanite/VSM look-dev (TR-01/TR-02); vertical slice = the first CD-sign-off gate with real evidence on reference HW. |
| M6 systems integration | Audio, UI, narrative, flow, save, Windows | MEAD P6 (menu loop, pseudo-loc, persistence across 2 versions) + Windows bring-up (R-21) + accessibility (Q-10). |
| M7 content & chapters | Chapters 1 → 8 | Content waves (content-dominated — the dominant cost, R-15); boss content (ADR-0107 data), narrative (MEAD §9, ADR-0108), population (WORLD_ARCHITECTURE §5), per-chapter gates. |
| M8 optimization | Profiling, tuning, stability | MEAD §15.4 regression rules; reference-scene gauntlet; soak tests; **no optimization without profiling evidence** (owner rule). |
| M9 QA & hardening | Full validation, defect management | RELEASE_READINESS_PLAN Phases 6A/6B: validation matrix + 8 QA disciplines + defect register. |
| M10 packaging & release | Builds, store, launch | RELEASE_READINESS_PLAN Phases 6C/6D: perf sign-off, platform compliance, 11 release gates, final readiness report. |

**MEAD P0–P8 mapping:** P0 = M0 (done); P1 (first playable) = M1; P2 (combat loop) = M3; P3 (animation integration) spans M3/M5; P4 (AI) = M4; P5 (world streaming) = M2/M5; P6 (menu/save loop) = M6; P7 (optimization) = M8; P8 (polish/release) = M9/M10. M2 and M7 are the two milestones the MEAD phase list did not name explicitly (traversal-as-its-own-gate and content-as-its-own-gate) — they are *additions*, and both are required by the accepted M1 spec (traversal) and the owner's scope (8 chapters).

## 3. Rules of the road (binding from P-01)

1. **No uncontrolled implementation** until this roadmap + dependencies + initial architecture are reviewed (owner instruction). Pure-logic contract tasks (P-08) are the only pre-review work and they touch no gameplay behaviour.
2. **M1 spec v1.4 AC-01…AC-31 are unchanged** (owner instruction). Any necessary change requires a documented review (MEAD §13.3 contract-change process) and an ADR — never a silent edit.
3. **No milestone exit on unproven work.** Each exit = evidence bundle (D-07) + ledger entry + the named ACs green on the owner's Mac (and Windows from M6). A NOT EXECUTED / BLOCKED run is not a pass.
4. **No silent simplification** of traversal/combat contracts (owner instruction): the E-paths, damage taxonomy, and restoration rules are implemented exactly as specified, with the spec's enumerated tests.
5. **No placeholder asset may be presented as production-ready** (owner instruction; QUALITY_ENGINEERING_PLAN §7 enforces it).
6. **Never accelerate by removing tests, ignoring defects, or lowering acceptance standards** (owner instruction, Phase 5E).
7. **No optimization claim without profiling evidence** (owner instruction, Phase 6C).
8. **Single source of truth:** this plan set + the ledger. Conflicting or duplicate architecture is prohibited (owner instruction, Part 4); the TL verifies all delegated work before it enters the integration branch (roadmap §6).

## 4. Milestones (entry → scope → exit)

### M0 — Foundation [DONE 2026-11-18; residual hygiene in WBS §0]
- **Exit (as verified):** canonical project identity; reproducible toolchain gate; clean compile (Mac + Windows); 2/2 automation; evidence bundle at `e71401b6`-era commit.
- **Residual (WBS P-01…P-08):** ratification, M0 archive + M0′ run, LFS, packaging script, contracts, ledger.
- **Exit:** P-01…P-09 done; ledger live.

### M1 — Core movement (weeks 1–5)
- **Entry:** M0 residual done; mannequin clips in tree.
- **Scope:** WBS M1-S1…S10. Player movement + camera + input + test map + first playable.
- **Exit:** **AC-01…AC-31 in 3 cold runs** + M1-P1…P6 + Agent 2 defects ①②③ closed + evidence archived. *This gate is the project's integrity checkpoint — if it fails, we stop and fix the process, not the ACs.*

### M2 — Traversal + forest slice (weeks 5–8)
- **Entry:** M1 exit.
- **Scope:** WBS M2-01…M2-09. Traversal E1–E7 exact; World Partition on forest slice; PCG scatter; navigation; P7 (first playable in a real environment).
- **Exit:** all E-paths green (restoration checklist exactly once each, no floating capsule, no teleport-into-geometry); streaming measurements recorded (B-12 data); **reference PC ordered** (R-16).

### M3 — Combat foundation (weeks 8–12)
- **Entry:** M1 exit (state machine + damage contract exist).
- **Scope:** WBS M3-01…M3-11. Player combat kit + damage pipeline + training room + combat anim set + MM spike.
- **Exit:** MEAD P2 exit (player-vs-dummy full loop, no double-hits, complete feedback) + taxonomy matrix 100% + deterministic case battery + MM spike decision (R-14).

### M4 — Enemy AI + world simulation (weeks 12–16)
- **Entry:** M3-02 (hit→damage path).
- **Scope:** WBS M4-01…M4-10. Token director, perception, StateTree archetypes (placeholder until CD-3), pilot encounter, pilot boss (phase graphs), NPC tier model.
- **Exit:** MEAD P4 exit (3 archetypes distinct, token caps hold, pilot boss 3 phases deterministic, seeded tests) + scenario battery (QUALITY_PLAN §5).

### M5 — Graphics & vertical slice (weeks 16–20)
- **Entry:** M4 engineering exit; reference PC delivered + calibrated (M5-01); CD identity approval for production Adanna (content gate).
- **Scope:** WBS M5-01…M5-08. Lumen/Nanite/VSM look-dev, material library, VFX set, production Adanna import, ch.1 slice (forest → encounter → memory → checkpoint → transition).
- **Exit:** **Vertical-slice gate (the first full CD sign-off):** controlled captures vs approved boards (QUALITY_PLAN §1), perf gate on reference HW (MEAD §15 budgets), streaming-ready cinematics, **M7-00 content staffing decision made** (R-15 — forced by this gate, not later).

### M6 — Systems integration (weeks 20–25)
- **Entry:** M5 gate.
- **Scope:** WBS M6-01…M6-10. Narrative core + endings, cinematics, audio, UI/rebinding, flow/transitions, persistence (2-version migration), pseudo-loc, Windows build, accessibility, parity.
- **Exit:** MEAD P6 exit (full menu loop on gamepad, settings/rebinding work, save/load + migration verified) + Windows evidence bundle (R-21 closed) + both platforms in every gate from here.

### M7 — Content integration, chapters 1 → 8 (weeks 25–45, content-dominated)
- **Entry:** M6 exit + M7-00 content capacity in place + CD canon gates (CD-2 consultant for sacred vocabulary; OAD-48 for ch. 8; Q-14 boss mechanics).
- **Scope:** WBS M7-01…M7-09. Three waves: ch.1–3, ch.4–6, ch.7–8. Per chapter: environment, lighting, enemies/NPCs, boss, narrative, audio, cinematics, population wiring.
- **Exit:** 8 chapter gate records (same format as the slice gate, per chapter: perf on reference HW + CD sign-off + save/narrative verified).

### M8 — Optimization & stability (weeks 45–50)
- **Entry:** M7 ch.1 complete (optimization runs against a real game, not a slice) + all budgets baselined (M8-01).
- **Scope:** WBS M8-01…M8-06. Reference-scene automation, scope audit, measured-only optimizations, regression rule enforcement, 2-h soak, full gauntlet.
- **Exit:** all MEAD §15 budgets met on reference HW; soak clean (hitches ≤ 1 × > 50 min⁻¹, no memory growth, zero crashes); regression rule live.

### M9 — Full validation & QA (weeks 50–54)
- **Entry:** M8 exit.
- **Scope:** WBS M9-01…M9-05 per RELEASE_READINESS_PLAN 6A/6B: validation matrix, 8 QA disciplines, defect register with severity/owner/resolution evidence, 100-cycle save soak, 3 cold regression runs × 2 platforms.
- **Exit:** P0/P1 defects closed (P2 by documented decision); matrix 100% executed with evidence.

### M10 — Packaging & release (weeks 54–56)
- **Entry:** M9 exit.
- **Scope:** WBS M10-01…M10-05: release pipeline (Windows primary, Mac, PS5 iff D-16), platform compliance (Q-22 crash reporting, licensing audit), store assets, final readiness report.
- **Exit:** **all 11 release gates (RRP §6) pass with actual evidence** + final release-readiness report delivered + owner release decision.

## 5. Workstreams (Phase 5 — single source of truth, eight specialists)

Each workstream owns its systems end-to-end (design → implementation → its tests → its evidence). The TL (this agent) owns cross-workstream contracts, integration, and the ledger; the owner owns machine, decisions, and CD sign-off.

| WS | Name | Owns (systems) | Primary tasks | Entry contracts |
|---|---|---|---|---|
| WS-1 | Core & Movement | S02 S03 S04 S05 | P-08, M1-S1…S7, M2-01…04 | M1 spec v1.4 (accepted); MEAD §4 |
| WS-2 | Combat & Damage | S06 S07 | M3-01…08 | damage contract (P-08), state-machine API |
| WS-3 | AI & Boss | S08 S09 | M4-01…06 | ADR-0006/0107, damage pipeline |
| WS-4 | World & Streaming | S10 S11 S12 | M2-05…08, M4-07/08, M5-06 (import) | MEAD §6, WORLD_ARCHITECTURE §5, `ITDDInteractable` |
| WS-5 | Narrative & Progression | S13 S14 S18 S21 | M6-01/02/05/06, M7 narrative waves | MEAD §9, ADR-0007/0108 |
| WS-6 | Graphics & VFX | S19 | M5-02…04, M7 lighting waves | TR-01/02, MEAD §15 budgets |
| WS-7 | Audio, UI & Accessibility | S16 S17 S22 | M6-03/04/07/09, M7 audio waves | ADR-0009, MEAD §11/§12 |
| WS-8 | Build, Perf & Release | S01 S15 S23 S24 | P-04/05, M6-08, M8-*, M9-*, M10-* | D-07 evidence format, MEAD §15 |

**Assignment rule:** one workstream per system (no duplicate ownership); a task may be *helped* across WS boundaries but has exactly one owner. Contract changes (dep map §3) are TL-only via ADR.

## 6. Integration management (Phase 5)

- **Integration line:** `arena/553fb02d-tdd` (this session's branch) is the protected integration branch. Feature work lands on `feat/<ws>-<task>` branches cut from it.
- **Merge criteria (all required):**
  1. Compiles clean on Mac (Windows from M6) — build evidence committed.
  2. The task's named TDD tests exist and pass; the task's WS regression suite passes.
  3. No regression: the shared suite (all `TDD-Unit.*` in-sandbox tests) passes; from M5, the reference-scene perf regression rule applies (> 5 % frame-time or > 100 MB VRAM blocks the merge — MEAD §15.4).
  4. Evidence bundle or ledger entry for the task exists (D-07 format).
  5. No change to a frozen contract (dep map §3) without an ADR cited in the merge message.
  6. TL verification: the TL reviews the diff for contract compliance and duplicate-architecture (owner instruction, Part 4) before merging — delegated work is never merged unverified.
- **Automated regression:** in-sandbox pure-logic suites run on every feature commit (fast, no Mac); full TDD suite + named functional suites run on the owner's Mac at every merge batch and every gate (evidence committed). From M6: same on the reference PC (Windows).
- **Conflict rule:** two tasks touching the same frozen contract go through the TL, who sequences them; no parallel ownership of one surface.
- **Ledger:** `docs/06_IMPLEMENTATION/QUALITY_LEDGER.md` — one row per merged batch and per gate: date, branch, commit, task IDs, test summary (passed/failed/skipped with reasons), evidence paths, perf deltas, defects opened/closed, risks changed, decisions. The ledger is the single progress record (Phase 5).

## 7. Progress reports (Phase 5 — 8 points, per milestone and on request)

1. **Milestone & date** — which milestone, which WBS tasks, dates.
2. **Scope delivered** — task IDs done vs planned, ACs now green (count + IDs).
3. **Evidence** — bundle paths, test counts (passed/failed/skipped), named `TDD_RESULT` lines, perf deltas vs previous gate.
4. **Defects** — opened/closed with severities (register link); nothing hidden.
5. **Risks** — register deltas (new/closed/changed) with the top-3 active.
6. **Decisions** — ADRs created, owner decisions obtained, contract changes.
7. **Blockers** — what is needed from the owner (machine time, decisions, content), with impact if unaddressed.
8. **Next** — next milestone's entry checklist + critical-path status (on track / at risk / behind, with the specific reason).

A report that cannot fill point 3 with real paths is not a report — it is a claim, and it will not be made.

## 8. Critical path & parallelism

```
P-01 ratification (owner) ──► P-02…P-09 ──► M1 (WS-1, 5 wks) ──► M2 (WS-1+4, 3 wks)
                                                              │
                                                              ├──► M3 (WS-2, 4 wks) ──► M4 (WS-3, 4 wks)
                                                              │            ▲
   M2 exit: ORDER REFERENCE PC (R-16)                         │            │
   M5-08: FORCE M7-00 content decision (R-15)                 │            │
   CD-2/CD-3/OAD-48: owner-gated, long-lead — start early     │            │
                                                              ▼            ▼
                                     M5 (WS-6 + slice, 4 wks) ◄── M4 exit
                                                              │
                                                              ▼
                                    M6 (WS-5+7+8, 5 wks, 3 parallel tracks)
                                                              │
                                                              ▼
                                    M7 (content waves, ~20 wks, CT-dominated)
                                                              │
                                                              ▼
                                    M8 (4 wks) ──► M9 (4 wks) ──► M10 (2 wks)
```

**Parallel tracks (contract-gated, not milestone-gated):** WS-3 pure logic (token policy, phase selector) starts at P-08; WS-5 narrative core + persistence start at M3-04; WS-7 UI framework starts at M1-S6; WS-6 material standards drafting starts at M2. Content (CT) runs on its own clock from M5: mannequin (M1) → combat set (M3) → Adanna production (M5) → chapter waves (M7).

**The three long-lead owner actions (do these first, they gate everything):** (1) P-01 ratification; (2) reference PC order at M2 exit; (3) M7-00 content capacity decision at M5-08.

## 9. Change management

- **Scope/AC changes:** documented review → ADR → owner ratification. M1 ACs require the same bar (Rule 2).
- **Architecture changes:** ADR + TL verification + ledger entry; frozen contracts only via MEAD §13.3.
- **Schedule changes:** re-baseline in the WBS with the delta explained in the progress report; the only permitted "accelerators" are parallelism and early owner actions (WBS §11) — never test/defect/standard removal (Rule 6).
- **Research changes:** new findings go to TECHNICAL_RESEARCH_REGISTER as new TR entries; verdicts that affect architecture require an ADR.

## 10. Success definition (end-state, Phase 6)

A commercial-quality, single-player action-adventure on Windows (primary), Mac (demo-capable), optionally PS5: 8 chapters, seven bosses, six endings, full validation matrix executed, 11 release gates passed **with actual evidence in the repository**, and a final release-readiness report that a stranger could audit against the committed bundles. Measured, not claimed.
