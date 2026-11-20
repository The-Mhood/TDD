# THE DISOBEDIENT DAUGHTER

*Nwanyi Na-anụghị Ihe* — a single-player, narrative third-person action-adventure built in **Unreal Engine 5.8** (canonical target platforms: Mac + Windows; PS5 is a later, approval-gated target).

## What this repository is (2026-11-20)

This is the **canonical project of record** and the single working branch of the project (`arena/553fb02d-tdd`, continuing `arena/c64fc525-tdd`). On 2026-11-20 the previously parallel agent lines (TD/Agent 1, Agent 2, Agent 3/canonical, Agent 4, production) were consolidated here. See [docs/00_GOVERNANCE/CANONICAL_DOCS_MAP.md](docs/00_GOVERNANCE/CANONICAL_DOCS_MAP.md) for what is authoritative and where every imported document came from.

## Verified state (no claim in this repo exceeds its evidence)

- **M0 passed 2026-11-18 on the project owner's Mac** (UE 5.8, commit `e71401b6`): both targets built; Unreal Automation **2/2 passed** (`TDD.Foundation.GameModeClass`, `TDD.Movement.DodgeDistanceMath`). Raw evidence is on the owner's machine; the compact report archive is pending. Gate A (editor-with-map) and Gate D (packaging) are **not** evidenced. See [M0 verification record](docs/06_IMPLEMENTATION/M0_VERIFICATION_RECORD_V1.md).
- **Dodge distance math** is implemented and verified (18/18 standalone under ASan/UBSan + in-engine automation). The capsule sweep is code-reviewed correct but **not yet exercised against a world**.
- **0 of 31** M1 acceptance criteria (AC-01…AC-31) are demonstrated. There is no state machine, camera system, Enhanced Input, test map, or playable session in Unreal yet. A browser-based technical prototype (playable Adanna in a Forbidden Forest blockout) exists as a design/feel reference only — it is not the game.

## The accepted gate

**M1** is complete only when AC-01…AC-31 pass with quoted results — [M1 Movement Specification v1.4](docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md) (TDD-A1-M1-SPEC-001) is the single authoritative movement contract, including the traversal/damage taxonomy, the E1–E7 exit paths, and the fallback→restoration→entry ordering. That document was changed by this consolidation **in no way** — it was copied verbatim from the line that owns it.

## Read first

| Document | Why |
|---|---|
| [T00 — Takeover Assessment & Execution Strategy](docs/00_GOVERNANCE/T00_TAKEOVER_ASSESSMENT_AND_EXECUTION_STRATEGY.md) | Current state, decisions, owner decision list, roadmap to commercial release |
| [Project State 2026-11-20](docs/00_GOVERNANCE/PROJECT_STATE_2026-11-20_TAKEOVER.md) | Verified / not-done / open-items ledger |
| [Canonical Docs Map](docs/00_GOVERNANCE/CANONICAL_DOCS_MAP.md) | Authority map, ADR collision resolution, branch disposition |
| [Status & Claims](docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md) | Status vocabulary and evidence rules (the project's anti-spin law) |
| [Open Questions Q-01…Q-22](docs/00_GOVERNANCE/OPEN_QUESTIONS.md) | Product decisions needed from the Creative Director/owner |
| [Master Engineering Architecture (TDD-MEAD-001)](docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md) | Governing architecture |
| [Quality & Integration Ledger](docs/quality/QUALITY_LEDGER.md) | The running integration/build/evidence log |

## Engineering layout

```
TheDisobedientDaughter.uproject      UE 5.8, one Runtime module, Mac + Windows
Source/TheDisobedientDaughter/       runtime module (movement, player, game mode, tests)
Tests/Standalone/                    host-compiler C++ tests (no UE dependency)
Tools/engine/                        Mac build/test runner, readiness checks, report parser
Config/                              DefaultEngine/Game/Input
docs/                                all project documentation (map above)
TDD_PHASE3_PRODUCTION/               imported production assets/tooling (proxy character, forest blockout, Mac runbook)
```

## Visual authority

The **Google Drive Production Art Bible** is the sole visual authority. Per-asset approval status, CD verdicts, and cultural gates live there (and in the `The-Mhood/chat-gpt` artifact index). Nothing in this repository grants visual, narrative, or cultural approval, and no unapproved artwork is imported or promoted.

## Build & verify (owner's Mac only)

There is no Unreal Engine in the agent sandbox; the only build/verify machine is the project owner's Mac (Apple M4, macOS 27.2.1, UE 5.8.4, Xcode 27.2). The verification loop is: agent commits code + tests + runbook → owner runs `Tools/engine/mac_build.sh --test-filter TDD` → the compact `Saved/BuildEvidence/<UTC>/` report (index + SHA256) is committed or posted → the agent verifies and updates the ledger. No stage is complete on standalone tests alone.
