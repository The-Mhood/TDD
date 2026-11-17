# STATUS AND CLAIMS — vocabulary and rules

Every agent report, commit message and document must classify each item with exactly one of these statuses. The vocabulary exists to prevent the most common failure in this project: a system being described as working because it was described.

| Status | Meaning | Evidence required |
|---|---|---|
| `DESIGN_ONLY` | Specified in a document; no code or asset exists | Document reference |
| `IMPLEMENTED_UNVERIFIED` | Code/assets written; **not** compiled, run or tested (typical in the agent workspace) | File paths |
| `COMPILES` | Code builds; not behaviourally tested | Build log (timestamp, target, config) |
| `PARTIAL` | Some acceptance criteria met, others not; list which | Test output for the parts that pass |
| `IMPLEMENTED_AND_VERIFIED` | All acceptance criteria met, tests pass, integrated | Build log + automation output + integration note |
| `MOCKED` | Present only to unblock something else; **not** a real implementation; must be visibly labelled in-game/debug | Stub location + list of what it replaces |
| `BLOCKED` | Cannot proceed; dependency named | Blocker ID + owner |
| `OUT_OF_SCOPE` | Explicitly excluded by Technical/Creative Director | Decision reference |
| `PENDING_CONTENT` | Framework ready, content owned by Creative Director not supplied | Content request ID |

## Rules

1. **No status may be inferred.** If a test cannot run, the item is `IMPLEMENTED_UNVERIFIED` (or `DESIGN_ONLY`), never `IMPLEMENTED_AND_VERIFIED`.
2. **`MOCKED` must be visible.** A mock that looks finished is a defect. Mocked placeholders must appear in the debug overlay and in the generated content audit report.
3. **`PENDING_CONTENT` must name the request.** "We need memory content" is not a request; `CONTENT-REQ-007 Memory 3 (Chapter 3) fragment presentation` is.
4. **No silent degradation.** Missing data, missing animation, missing audio must log a named warning and surface in the audit; the failure must not be swallowed by a `nullptr` check.
5. **Evidence is a link or a log, not a sentence.** "Tested locally, works" is not evidence.
6. **A regression is a status change,** even to `IMPLEMENTED_AND_VERIFIED`: if a later change breaks it, the status must be stepped down in the next report. Statuses are not permanent achievements.

## Current claim ledger (2026-11-16)

| Item | Status | Evidence |
|---|---|---|
| Master Engineering Architecture Document | `DESIGN_ONLY` (documentation complete, unapproved) | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` v1.0 |
| Project inspection / current-state audit | `IMPLEMENTED_AND_VERIFIED` (within workspace limits) | `docs/00_GOVERNANCE/PROJECT_STATE_2026-11-16.md` §1–3 |
| Architectural decisions ADR-0001…0012 | `DESIGN_ONLY` (proposed, awaiting TD) | `docs/03_DECISIONS/` |
| Coding standards | `DESIGN_ONLY` | `docs/01_ARCHITECTURE/CODING_STANDARDS.md` |
| Engine/project skeleton | `DESIGN_ONLY` (nothing created) | — |
| Any gameplay system (movement, combat, AI, world, narrative, save, UI) | `DESIGN_ONLY` | Sections 4–12 of TDD-MEAD-001 |
| Agent 1 gameplay/character assessment | `DESIGN_ONLY` — **v1.4**, final clarifications and budget correction applied; v1.3/v1.2/v1.1/v1.0 archived | `docs/02_PRODUCTION/AGENT1/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` |
| Agent 1 Milestone 1 specification | `DESIGN_ONLY` — **v1.4**, gate AC-01…AC-31 accepted and unchanged; implementation `BLOCKED` on Agent 3 prerequisites B-1…B-6 | `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` §2.3, §4 |
| Agent 1 root-motion policy | `DESIGN_ONLY` — ADR-0013 **v1.4**; execution mechanism provisional pending `RootMotionAppliesToCapsule` | `docs/03_DECISIONS/ADR-0013-root-motion-policy.md` |
| Agent 1 shared-contract response C-01…C-07 | `DESIGN_ONLY` — **v1.0 (`A1-R1`)**, proposals labelled `PROPOSED — NOT FROZEN`; every test `PROPOSED / NOT RUN`; 0 contracts agreed, 0 consumers signed | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md` |
| Agent 1 TD v1.2 acknowledgment and contract revision | `DESIGN_ONLY` — **v1.1 (`A1-R2`)**; 6 contracts `REVISED`, 1 `CLARIFICATION REQUIRED`, **0 changes caused by v1.2 itself**; 12 items `UNRESOLVED`; 0 contracts agreed; tests `PROPOSED / NOT RUN` | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md` |
| Agent 1 response to A2's formal review | `DESIGN_ONLY` — **v1.2 (`A1-R3`)**; 2 contracts `AGREE` and 5 `CONDITIONAL` against `A1-R2` v1.1; 0 contracts bilaterally agreed; 14 unresolved items; tests `PROPOSED / NOT RUN`, 0 executed | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md` |
| Player controller / camera / combat / weapon code | **Does not exist** | — |
| Any gameplay measurement (M-01a…M-14) | **Not measured** | No engine in agent workspace (ADR-0012) |
| Any art, animation, audio, cinematic asset | **Does not exist** | Drive Art Bible: 7 approved concept boards, no production assets; `09_ANIMATION_AND_COMBAT` folder is empty |

**Statement to the Creative Director:** at this timestamp the project has an architecture and an honest audit. It does not yet have a game. The next deliverable that changes that is Phase 0 (project skeleton), which requires an Unreal Engine 5.8 machine to build.
