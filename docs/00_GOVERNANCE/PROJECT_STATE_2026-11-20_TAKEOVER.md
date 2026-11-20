# Project State — 2026-11-20 (post-consolidation)

**Branch of record:** `arena/553fb02d-tdd` (continuation of `arena/c64fc525-tdd` @ `a7f940a`).
**Method:** statuses per the controlled vocabulary in `STATUS_AND_CLAIMS.md`; every row is evidence-linked. This record supersedes `PROJECT_STATE_2026-11-16.md` for the items it restates; that file is preserved.

## 1. Verified (evidence exists)

| Item | Status | Evidence |
|---|---|---|
| M0 Gates B+C (build + 2/2 automation) on owner Mac, 2026-11-18, commit `e71401b6` | `IMPLEMENTED_AND_VERIFIED` (Mac only; see limits) | `docs/06_IMPLEMENTATION/M0_VERIFICATION_RECORD_V1.md`; raw bundle owner-local `~/tdd-m0/Saved/BuildEvidence/20261118T202235Z` (archive pending, D-15) |
| Dodge distance pure math (radius-once, clamp, margin) | `IMPLEMENTED_AND_VERIFIED` (standalone 18/18 ASan/UBSan + in-engine `TDD.Movement.DodgeDistanceMath`) | `TDDDodgeDistanceMath.h`, `Tests/Standalone/TDDDodgeDistanceMathTests.cpp`, M0 record |
| Capsule sweep mechanics (code level) | `IMPLEMENTED_UNVERIFIED` (Agent 2 code review PASS; never exercised against a world) | `TDDDodgeSweep.{h,cpp}`; `docs/02_PRODUCTION/AGENT2/AGENT2_VERIFY_M1_DODGE_REVIEW_V1.md` |
| Adanna minimal pawn (spring arm/camera/legacy input/jump) | `COMPILES` (M0 build) — not behaviourally tested | `TDDAdannaCharacter.*`, M0 record |
| Browser/Node playable prototype (Adanna + Forbidden Forest blockout) | `IMPLEMENTED_AND_VERIFIED` (browser + Node 11/11, 120-frame replay) — **not a UE integration** | `origin/arena/8efaa23f-tdd` PLAYABLE_MILESTONE_TRACKER; `TDD_PHASE3_PRODUCTION/…/web_src/` (imported) |
| Adanna technical proxy + forest blockout GLBs | `IMPLEMENTED_UNVERIFIED` (local GLB validation only; not imported into the canonical UE project) | `TDD_PHASE3_PRODUCTION/…/model/` |
| `TDD_GAME.uproject` opened in UE 5.8.4 editor on owner Mac (today) | `COMPILES`-adjacent: editor open + level + C++ Classes + imported forest visible (screenshot evidence); **no compile/PIE/package result recorded yet** | screenshots in `The-Mhood/chat-gpt` (2026-11-20) |
| M1 spec v1.4 + AC-01…AC-31 + traversal/damage contracts | `DESIGN_ONLY` — accepted, unchanged, now in the canonical tree | `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` |

## 2. Not yet done (the honest list)

| Item | Status |
|---|---|
| Any gameplay system beyond dodge math (state machine, CMC, camera system, input buffering, metrics) | `DESIGN_ONLY` |
| L_TDD_Test_Movement map | `DESIGN_ONLY` (must be authored on the Mac) |
| AC-01…AC-31 demonstrations | **0/31** (dodge-math sub-part of AC-19 has code + standalone proof only) |
| M1-P1…P5 first-playable gate | `BLOCKED` on S1–S8 |
| Packaging / Gate D | `NOT RUN` |
| Windows build | `NOT RUN` (target declared, never compiled) |
| CI | does not exist |
| Gate A (editor open with map, twice, on canonical project) | `NOT EVIDENCED` |
| M0 raw-evidence archive in repo | `NOT RUN` (one command, D-15) |
| C-05 telegraph contract | `DESIGN_ONLY`, parked (D-02); 0/67 executed |
| Enemy archetypes / boss mechanics / memories / endings | `DESIGN_ONLY` / owner-decision-gated (Q-14…Q-17, CD-2/CD-3) |
| Production Adanna 3D character | `BLOCKED — CREATIVE APPROVAL` (turnarounds unapproved; interim proxy only, D-14) |
| Windows DX12 reference machine / PS5 devkit | not acquired (Phase 3 / D-12, D-16) |

## 3. Open items carried forward (IDs preserved)

- TD-06, TD-09, TD-12 (C-05 implementation dependencies) — open, owner/TD.
- U-07 — open, unchanged.
- B-11, B-15 — open (C-05 dependency on C-04 decision; Agent 3 S3 review absence).
- B-01 (no UE project) — **resolved in substance** by M0; superseded by "canonical project consolidated onto `arena/553fb02d-tdd`".
- B-02 (CD-3), B-03 (CD-2) — open, creative/consultant gates.
- B-04 (traversal contract) — **resolved by M1 spec v1.4 §3.2.2/§3.7** (the contract the request asked for is the accepted v1.4 rule set).
- B-12 (access budgets unmeasured) — open until Phase 2 measurement.
- Q-01…Q-22 — open, owner (mapped to D-10…D-18 in T00 §9).
- Agent 2 dodge defects ①②③ — open, Phase 1 S1–S2 (owner: Agent 3/me).
- Issue #1 — open; to be updated with the consolidated handoff.
