# Documentation index — THE DISOBEDIENT DAUGHTER

Start here. The primary deliverable is the Master Engineering Architecture Document.

| # | Document | Purpose | Status |
|---|---|---|---|
| 1 | `01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | Full technical architecture, systems, interfaces, testing, performance, phasing, risks | `DESIGN_ONLY` — awaiting Technical Director review |
| 2 | `00_GOVERNANCE/PROJECT_STATE_2026-11-16.md` | Evidence-based audit: repo, workspace capability, Art Bible state | `IMPLEMENTED_AND_VERIFIED` (within workspace limits) |
| 3 | `00_GOVERNANCE/STATUS_AND_CLAIMS.md` | Status vocabulary + current claim ledger | Active |
| 4 | `00_GOVERNANCE/OPEN_QUESTIONS.md` | 22 decisions needed, their blockers, and default assumptions | Active |
| 5 | `01_ARCHITECTURE/CODING_STANDARDS.md` | Mandatory engineering rules for all agents | Active |
| 6 | `03_DECISIONS/ADR-0001…0013` | Architecture decision records (ADR-0013 at v1.4; v1.3/v1.2/v1.1/v1.0 in `03_DECISIONS/archive/`) | Proposed (0001–0011, 0013), Accepted (0012) |
| 7 | `02_PRODUCTION/AGENT1/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` | Agent 1: gameplay/character assessment, interfaces, staged plan M0–M7, thresholds — **v1.4** (v1.3/v1.2/v1.1/v1.0 in `AGENT1/archive/`) | `DESIGN_ONLY` — awaiting re-review |
| 8 | `02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` | Agent 1: Milestone 1 specification — **v1.4**, accepted single gate of 31 acceptance criteria, 36 test specs, 6 manual procedures, L1–L3 latency model, five camera criteria, traversal damage taxonomy E1–E7, two-phase placement validation, hold semantics and a two-phase (relocation / terminal hold) fallback budget | `DESIGN_ONLY` — blocked on Phase 0 prerequisites |
| 9 | `AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md` | Agent 1: response to the Agent 1 contract packet (C-01…C-07) — proposed shapes, ownership/mutation authority, failure semantics, named tests, Agent 2 dependencies, nine TD issues — **v1.0 (`A1-R1`)** | `DESIGN_ONLY` — `PROPOSED — NOT FROZEN`; awaiting Agent 2 and TD review |
| 10 | `AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md` | Agent 1: TD v1.2 acknowledgment and contract revision — per-contract `UNCHANGED`/`REVISED`/`CLARIFICATION REQUIRED` status, TD-01…TD-09 answers, 15 of Agent 2's 16 dependency items answered — **v1.1 (`A1-R2`)** | `DESIGN_ONLY` — `PROPOSED — NOT FROZEN`; `A1-R1` preserved unchanged |

## Reading order for a new agent

1. `CODING_STANDARDS.md` — how to write code here.
2. `STATUS_AND_CLAIMS.md` — how to report honestly.
3. MEAD §1 (current state) and §13 (interfaces + ownership), then the section for your area.
4. `OPEN_QUESTIONS.md` — what you must not assume.

## Reading order for the Creative Director

1. MEAD §1 (what exists), §16 (phases) and §17 (risks).
2. `OPEN_QUESTIONS.md` — the decisions only you can make, starting with platforms, progression model and content availability.
3. `STATUS_AND_CLAIMS.md` §"Current claim ledger" — what is actually true today.

## Non-negotiables

- Story, characters, art and cultural representation are **not** engineering's to invent. The Drive Production Art Bible and the Creative Director are authoritative.
- Design approval ≠ canon approval (OAD-48).
- Invented mythology is never presented as authentic Igbo tradition; the cultural sign-off gate is mechanical (ADR-0008).
- No functionality is claimed without evidence from a machine that can build and run Unreal Engine.
