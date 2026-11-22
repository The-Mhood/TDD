# Planning Set Index — The Disobedient Daughter (fast-track)

**Updated:** 2026-11-20 (owner review pass) · **Owner:** Takeover Technical Lead
**Status of the set:** PROPOSED — awaiting owner ratification (P-01) via DECISION_RATIFICATION_REPORT. No gameplay implementation before ratification.

| Document | ID | Version | Status | Read first if you want… |
|---|---|---|---|---|
| **DECISION_RATIFICATION_REPORT.md** | TDD-PLAN-RAT-001 | 1.0 | Proposed (the P-01 package) | to ratify / ask questions — start here |
| **MASTER_PROJECT_ROADMAP.md** | TDD-PLAN-ROADMAP-001 | **2.0** (accelerated) | Proposed | the 4–8-week execution model: weekly plan, daily protocol, resources, critical path, SA scope register |
| **MASTER_WORK_BREAKDOWN.md** | TDD-PLAN-WBS-001 | **2.0** | Proposed | task-level detail with week/track assignments + post-RC waves |
| **MILESTONE_ACCEPTANCE_CRITERIA.md** | TDD-PLAN-MAC-001 | 1.1 | Proposed | what must be true (measurable) at each milestone, Checkpoint A (W4) and B (W8/RC) |
| **TECHNICAL_RESEARCH_REGISTER.md** | TDD-PLAN-TRR-001 | 1.1 | Proposed | why each technical choice (TR-01…TR-19: 16 domains + hardware + **claims audit**) |
| **SYSTEM_REQUIREMENTS.md** | TDD-PLAN-SYSREQ-001 | 1.1 | Proposed | the complete feature inventory (S01–S24, accepted vs new) |
| **SYSTEM_DEPENDENCY_MAP.md** | TDD-PLAN-SDM-001 | 1.1 | Proposed | what depends on what; frozen contracts; milestone names (authority); critical path |
| **RISK_AND_BLOCKER_REGISTER.md** | TDD-PLAN-RISK-001 | 1.2 | Proposed | what can kill the plan: B-01…B-12 (re-assessed) + R-13…R-22 + **DA-01…DA-10 (deadline risks)** |
| **QUALITY_ENGINEERING_PLAN.md** | TDD-PLAN-QUAL-001 | 1.1 | Proposed | measurable quality bars + the 10 dedicated gates (combat/AI/physics batteries, screenshots, soaks) |
| **RELEASE_READINESS_PLAN.md** | TDD-PLAN-RRP-001 | 1.1 | Proposed | Phase 6: validation matrix, 8 QA disciplines, defect register, 11 release gates, final report |

**Related (outside this folder, referenced by the set):**
- `docs/00_GOVERNANCE/T00_TAKEOVER_ASSESSMENT_AND_EXECUTION_STRATEGY.md` — takeover record + D-01…D-09 + owner asks D-10…D-18 (superseded *only* where RAT-001 v1.0 says so; T00 §9 defaults still apply).
- `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` v1.4 — the accepted movement/traversal/combat-contract gate (AC-01…31). **Unchanged.**
- `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` (TDD-MEAD-001) — governing architecture (modules, budgets, test tiers). **Unchanged.**
- `docs/03_DECISIONS/ADR-0001…0013, 0101…0109` — the decision record. ADR-0109 (this pass) records the accelerated-model technical decisions; becomes Accepted at P-01.
- `docs/06_IMPLEMENTATION/QUALITY_LEDGER.md` (created at P-07, W0) — the single progress/evidence record.

## Change log (review pass, 2026-11-20)

1. **Inconsistencies fixed (owner point 1):** milestone names unified (M7 = content integration, M8 = optimization/stability, M9 = full QA, M10 = packaging/release — the dep-map graph was wrong, corrected); RRP G-02 corrected from "11 M1 ACs" to **AC-01…AC-31**; reference-PC timing reconciled to **one authoritative date: order at P-01 (Day 0)** — TR-18 (T00's "Phase 3 entry", TR-15's "M6 entry", ROADMAP v1.0's "M2 exit/M5 entry" all superseded; dependency explained in TR-18/dep-map §5).
2. **Accelerated model (owner point 2):** ROADMAP v2.0 + WBS v2.0 replace the 13–14-month schedule with the 4–8-week plan (Checkpoint A W4, Checkpoint B W8/RC); DA-01…DA-10 deadline risks added; scope adjustments made explicit as SA-1…SA-8 (owner approval required — nothing silently cut).
3. **Reference hardware revalidated (owner point 4):** TR-18 — min vs recommended spec, cost, alternatives, purchase timing, and the 1440p/60 validation procedure; the RTX 3060 Ti anchor is a *budget target, unproven until benchmarked*.
4. **Technical claims audited (owner point 5):** TR-19 — 15 claims reclassified ([DS-G]/[BUD]/[EN-V]/[ST]/[UNV]) with AC + named verification method; over-claims corrected at source (notably: determinism is a verified design property, not an engine guarantee; in-workspace testing applies only to UE-independent pure cores, per ADR-0012 + g++ 12.2 verified 2026-11-20).
5. **Baseline preserved (owner point 5/6):** AC-01…31, all 21 accepted ADRs, narrative decisions, and traversal/combat contracts are **unchanged**; the only new ADR (0109) records the execution model, not a spec change.
