# System Dependency Map

**Document ID:** TDD-PLAN-SDM-001 · **Version:** 1.1 · **Date:** 2026-11-20
**v1.1 (review pass):** fixed milestone-name inconsistency in the graph (M8 = optimization/stability, M9 = full QA, M10 = packaging/release; content integration is M7 — matching ROADMAP and MAC); S21 hardening is M6 (soak M9), matching SYSTEM_REQUIREMENTS S21; reference-PC timing reconciled to a single authoritative date (order at P-01/Day-0 — see §5); critical path updated to the accelerated model (ROADMAP v2.0).
**Companion to:** MASTER_PROJECT_ROADMAP.md. IDs: S## = systems in SYSTEM_REQUIREMENTS.md; M# = milestones in MILESTONE_ACCEPTANCE_CRITERIA.md; D-## = owner decisions (T00 §9 / research register D-19…D-25); B-## = blocker register (RISK_AND_BLOCKER_REGISTER.md).

## 1. System dependency graph

```
                        ┌────────────────────────────────────────────────────────┐
                        │ M0 foundation (project, build loop, test harness)     │  [DONE — verified 2026-11-18]
                        └───────────────┬────────────────────────────────────────┘
                                        │
        ┌───────────────┬───────────────┼────────────────┬─────────────────┐
        ▼               ▼               ▼                ▼                 ▼
   S02 Core        S03 Movement     S05 Camera       S15 Build/Pipeline   S24 Perf budgets
   (state machine,  (CMC, input,    (five criteria)  (runbook, evidence,  (MEAD §15 — law
    tags, config)    buffering)                    LFS, packaging)         from M1)
        │               │               │                │                 │
        │               ▼               │                │                 │
        │         S03b Dodge (sweep,    │                │                 │
        │         floor validation)     │                │                 │
        │               │               │                │                 │
        └───────┬───────┘               │                │                 │
                ▼                       │                │                 │
         S04 Traversal (E1–E7)          │                │                 │
                │                       │                │                 │
        ┌───────┴────────┐              │                │                 │
        ▼                ▼              │                │                 │
   S06 Combat kit   S07 Damage/         │                │                 │
   (states, hits)   posture/death       │                │                 │
        │                │              │                │                 │
        └───────┬────────┘              │                │                 │
                ▼                       │                │                 │
        S08 Enemy AI (archetypes,       │                │                 │
        tokens, perception)             │                │                 │
                │                       │                │                 │
                ▼                       ▼                ▼                 │
        S09 Boss (phase graphs)   S10 World streaming   S12 Interaction    │
                │                 + environment physics ─┘                  │
                │                       │                │                 │
                └───────────┬───────────┘                │                 │
                            ▼                            ▼                 │
                     S11 NPC population          S13 Narrative/quests/     │
                     (five-tier model)           memories/endings          │
                            │                            │                 │
                            └────────────┬───────────────┘                 │
                                         ▼                                 │
                     S16 Audio · S17 UI/UX · S18 Progression/chapter flow  │
                                         │                                 │
        S19 Rendering/VFX (W3→; look-dev on Mac, sign-off on reference PC) │
        S20 Character art/animation pipeline (from W0, content-gated)      │
                                         │                                 │
                                         ▼                                 ▼
            S21 Save/persistence (contracts M0; hardening M6; soak M9)     │
                                         │
                                         ▼
  M7 content integration → M8 optimization/stability → M9 full QA → M10 release
```

## 2. Milestone prerequisites (the critical path)

| Milestone | Hard prerequisites | Soft (parallel-safe) prerequisites |
|---|---|---|
| M0 (done) | owner Mac + UE install (done 2026-11-16) | — |
| M1 (movement, AC-01…31) | M0 ✓; test map S7 (authored on Mac); mannequin clips (stock — no content gate); D-15 evidence archive | D-10…D-13 ratification; S02 core types can start before S7 |
| M2 (traversal + forest slice) | M1 exit; traversal contract = M1 spec §3.7 (accepted ✓); forest blockout GLB (in-tree ✓) | S10 WP scaffolding can start against the blockout |
| M3 (combat foundation) | M1 state machine; placeholder attack clips (mannequin); D-13 (bCausesStagger — done) | S06 data model (pure C++) can be written against the contract immediately |
| M4 (enemy AI + world sim) | M3 damage pipeline; CD-3 archetype ratification (content gate — placeholders until then); CD-2 consultant gate for shrine/mask vocabulary | AI data structures (pure) start now; StateTree authoring needs a test encounter |
| M5 (graphics/vertical slice) | M2 forest slice; **reference PC (D-12)** for sign-off captures; art content pipeline producing chapter-1 assets | VFX/audio design (data) parallel; PCG scatter can run on Mac |
| M6 (audio/UI/progression) | M4 world events; save contracts (M0 ✓); D-17 (consultant) for cultural content in UI/codex | UI framework + pseudo-loc parallel from M4 |
| M7 (content integration, ch. 1 → 8) | M5 + M6 gated; **content production capacity** (dominant cost); ch. 8 environments canon approval (OAD-48) | Per-chapter waves once ch. 1 gates |
| M8 (optimization/stability) | M7 ch. 1 complete (approved RC scope, SA-1) + reference PC | — |
| M9 (full QA) | M8 perf gate | — |
| M10 (packaging/release) | M9; platform decisions final; legal/licensing audit | store assets parallel from M8 |

**Milestone names are fixed** (this table is the authority, matching MASTER_PROJECT_ROADMAP and MILESTONE_ACCEPTANCE_CRITERIA): M7 = content integration, M8 = optimization/stability, M9 = full QA, M10 = packaging/release. Under the accelerated model (ROADMAP v2.0) these gates are reached in W1–W8 *within the owner-approved release scope* (SA-1: ch. 1); chapters 2–8 become post-RC waves with the same gate definitions.

## 3. Interface contracts that gate parallel work (MEAD §13.2 frozen surfaces)

Parallel workstreams may start the moment these contracts exist (frozen until an ADR changes them):

| Contract | Defined in | Unblocks (in parallel) |
|---|---|---|
| `UTDDCharacterStateMachine` request/force API + state table schema | M1 spec §3.2 | Combat states, AI reactions, cinematics takeover, UI state display |
| `FTDDDamageRequest` (incl. `bCausesStagger`) + damage pipeline entry | M1 spec §3.2.1, D-03, MEAD §5.4 | Enemy attacks, player defence, boss phases, VFX/audio feedback hooks |
| `ITDDInteractable` | MEAD §4.5 | All world objects, UI prompts, quest anchors |
| `ITDDLocomotionAnimProvider` | ADR-0005 | Animation content pipeline (corpus can be built without engine work) |
| `ITDDSaveProvider` + `FTDDSaveHeader` | ADR-0007 | Every persisting system (quests, world state, memory flags) |
| `ITDDAudioService` | ADR-0009 | All feedback (combat, world, UI) without audio implementation |
| Combat director token policy (pure function) | ADR-0006 | Encounter design, boss phase data, AI tuning — all data |
| Boss phase graph schema | ADR-0107 | Boss content authoring (CSV/JSON) before the controller exists |
| `TDD_RESULT` line format + evidence bundle schema | M1 spec §5, D-07 | Every workstream's completion evidence |

**Rule:** no workstream may define its own version of any contract above; changes go through the contract-change process (MEAD §13.3) recorded in the quality ledger.

## 4. Content gates (not engineering — owner/CD authority)

| Gate | Blocks | Status |
|---|---|---|
| CD-3 — enemy archetype ratification | Real enemy content (placeholders until ratified) | OPEN |
| CD-2 — cultural consultant | Shrine/mask/ritual vocabulary (Maskbearer fully; Rootwarden/Thrall/Thunder Aspirant partly) | OPEN (D-17) |
| OAD-48 — Chapter 8 canon approval | Chapter 8 content (Hall of Posts V004 is design-approved, canon PENDING) | OPEN |
| Q-14 — boss mechanics | Real boss movesets (pilot uses placeholder) | OPEN |
| Q-15/Q-16 — memories/endings content | Memory/ending presentation assets | OPEN |
| Q-18/Q-19 — animation/art pipeline staffing | All final visual/animation content | OPEN (D-14 covers the interim) |
| D-16 — PS5 confirmation | Sony application + all PS5 work | OPEN |

## 5. Critical path (accelerated model, 2026-11-20)

```
P-01 ratification + Day-0 orders (reference PC, content team, NVMe)
  → P-08 core contracts (W1 d1–d2)
  → M1 core (W1–W3) ── M1 gate W3 (AC-01…31, 3 cold runs)
  → M2 traversal (W3–W4) ── M2 gate W4 ──► CHECKPOINT A (W4): verified core loop
  → M3 combat (W4–W5) ── M3 gate W5
  → M4 AI + pilot boss (W5–W6) ── M4 gate W6
  → ch.1 content integration (W5–W7, content team; PCG/modular)
  → M5 look-dev + perf baseline (W4–W7; reference PC from W2)
  → M6 systems on live world (W6–W7: UI/audio/save/flow)
  → M8 optimization (W7) → M9 QA (W8) → M10 packaging (W8)
  ──► CHECKPOINT B (W8): ch.1 release candidate (RC) + final readiness report
  → Post-RC waves: ch.2–8, remaining bosses/endings/memories (same gates, same bar)
```

**Day-0 actions (all at P-01 — do not wait):** (1) owner ratification incl. SA scope register (this week); (2) **reference PC order — the single authoritative purchase date is Day 0 (ratification day)**; shipping lead 1–2 weeks → arrives W1, calibrated W2, Windows CI node from W2 (dependency: the accelerated plan needs Windows verification at Checkpoint A (W4) and look-dev/perf sign-off from W3–W5 — every later order date removes one of those; the earlier plan's "M2 exit" / "M5 entry" / "Phase 3 entry" timings are superseded, see TR-15/TR-18); (3) content team mobilization (Q-18/19) — the content clock dominates W5–W8; (4) CD-3 archetype + Q-14 boss mechanics + CD-2 consultant engagement kickoffs (approvals needed by W3, else SA-2/SA-5 deepen); (5) LFS provisioning (one owner action); (6) Sony application only if D-16 = yes — post-RC under the fast-track (SA-7).

## 6. What is NOT on the critical path (safe to defer)

- C-05 telegraph contract work (parked, D-02) — re-enters at M3 combat, not before.
- Motion Matching (TR-03) — corpus-gated, M3+.
- Hosted CI (TR-15) — release-phase option.
- MetaHuman/Fab content — not used (D-25/TR-17).
- PS5-specific engineering — devkit-gated.
- Localisation content (Q-13) — pipeline at M6, content at M9/M10.
