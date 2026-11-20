# Canonical Documentation Map (post-consolidation, 2026-11-20)

Purpose: one place that says which document is authoritative for what, where every imported document came from, and how the ADR ID collision was resolved.

## 1. Branch disposition

| Branch | Status after consolidation |
|---|---|
| `arena/553fb02d-tdd` | **Working line of record.** Continuation of the canonical Agent 3 line (`arena/c64fc525-tdd` @ `a7f940a`, fast-forward merged) + all imported material below. All future work lands here. |
| `arena/c64fc525-tdd` | Preserved as provenance (canonical project origin). No new work. |
| `arena/3bc206a0-tdd` | Preserved as provenance (Agent 1/TD line: M1 spec v1.4, ADR-0001…0013, TDD-MEAD-001, M0 record). No new work. |
| `arena/5dde91a4-tdd` | Preserved as provenance (Agent 2 line: world architecture, dodge review, ADR-0101…0108 source). No new work. |
| `arena/8efaa23f-tdd` | Preserved as provenance (production line: Phase 3 assets/tooling, OUR_EYES verdicts, web build with vendored libs — not imported wholesale). No new work. |
| `arena/b2c58152-tdd` | Preserved as provenance (Agent 4 assessments). No new work. |
| `main` | Untouched (1-line README). Promotion to `main` happens at a milestone gate with owner sign-off, not continuously. |

## 2. Authority by subject

| Subject | Authoritative document | Location |
|---|---|---|
| Project identity / canonical project | T00 assessment §2, `TheDisobedientDaughter.uproject` | repo root |
| Master engineering architecture (governs M1 spec + ADRs) | **TDD-MEAD-001 v1.0** (imported) | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` |
| Architecture companion (Agent 3's assessment-era MEAD) | preserved, non-governing | `docs/MASTER_ENGINEERING_ARCHITECTURE.md` |
| Architecture companion (Agent 2's MEAD) | preserved, non-governing | `docs/02_PRODUCTION/AGENT2/MASTER_ENGINEERING_ARCHITECTURE_AGENT2_V1.md` |
| M1 movement gate (AC-01…AC-31) + traversal/damage contracts | **M1 spec v1.4** (TDD-A1-M1-SPEC-001) | `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` |
| M1 character assessment | v1.4 (TDD-A1-ASSESS-001) | `docs/02_PRODUCTION/AGENT1/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` |
| M0 evidence standard | M0 checklist + verification record | `docs/M0_UNREAL_FOUNDATION_CHECKLIST.md`, `docs/06_IMPLEMENTATION/M0_VERIFICATION_RECORD_V1.md` |
| M1 execution stages S1–S8 + first-playable gate | M1 execution scope v1 | `docs/06_IMPLEMENTATION/M1_EXECUTION_SCOPE_AND_GATE_V1.md` |
| Status vocabulary + claim ledger rules | STATUS_AND_CLAIMS (canonical branch version, post-L-2-closure) | `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| Open product decisions Q-01…Q-22 | OPEN_QUESTIONS (imported) | `docs/00_GOVERNANCE/OPEN_QUESTIONS.md` |
| Takeover decisions D-01…D-09, owner decisions D-10…D-18 | T00 assessment | `docs/00_GOVERNANCE/T00_TAKEOVER_ASSESSMENT_AND_EXECUTION_STRATEGY.md` |
| World / NPC / streaming / boss architecture | WORLD_ARCHITECTURE + dependency register (imported) | `docs/02_PRODUCTION/AGENT2/` |
| Dodge implementation review (pending-item closure) | Agent 2 review v1 (imported) | `docs/02_PRODUCTION/AGENT2/AGENT2_VERIFY_M1_DODGE_REVIEW_V1.md` |
| C-05 telegraph contract (parked, design record) | S4.3.11 set + responses | `docs/AGENT1_C05_*` |
| Adanna art/animation integration contract | M1 art spec (canonical branch) | `docs/implementation/M1_ADANNA_CHARACTER_ART_ANIMATION_SPEC.md` |
| Mac/PS5 platform feasibility | Agent 4 assessments (provenance) | `origin/arena/b2c58152-tdd:docs/` |
| Production (Phase 2/3) history, runbook, owner request | imported production docs | `docs/production/`, `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/` |
| Art authority (visual) | Google Drive Art Bible + CD verdicts (not in repo) | Drive `THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE` |

## 3. ADR series and the ID collision

Two independent ADR series were created in parallel by the Agent 1/TD line and the Agent 2 line, with colliding IDs. Resolution: the Agent 1/TD series keeps **0001–0013**; the Agent 2 series is renumbered **0101–0108**. New ADRs continue from **0109**.

| New ID | Subject | Original (branch) | Conflict note |
|---|---|---|---|
| ADR-0001 | Engine version (UE 5.8) | 3bc ADR-0001 | vs 5dd ADR-0002 (engine baseline UE 5.8) — same outcome, two records; 0001 is the adopted record |
| ADR-0002 | C++ first | 3bc ADR-0002 | — |
| ADR-0003 | Module layering | 3bc ADR-0003 | target graph for any future module split (D-05) |
| ADR-0004 | GAS adoption | 3bc ADR-0004 | vs 5dd ADR-0003 (GAS scope) — complementary: 0004 = adopt, 0103 = scope; both kept |
| ADR-0005 | Animation provider | 3bc ADR-0005 | — |
| ADR-0006 | AI stack | 3bc ADR-0006 | — |
| ADR-0007 | Persistence | 3bc ADR-0007 | — |
| ADR-0008 | Canon gating | 3bc ADR-0008 | — |
| ADR-0009 | Audio (MetaSounds only) | 3bc ADR-0009 | — |
| ADR-0010 | Experimental features | 3bc ADR-0010 | — |
| ADR-0011 | Single-player | 3bc ADR-0011 | — |
| ADR-0012 | Verification boundary (no engine in agent workspace) | 3bc ADR-0012 | — |
| ADR-0013 | Root-motion policy v1.4 | 3bc ADR-0013 (+v1.0–v1.3 archive) | — |
| ADR-0101 | Automation test harness | 5dd ADR-0001 | vs 3bc ADR-0012 territory; kept as Agent 2's harness detail |
| ADR-0102 | Engine baseline UE 5.8 | 5dd ADR-0002 | see 0001 conflict note |
| ADR-0103 | GAS scope | 5dd ADR-0003 | see 0004 note |
| ADR-0104 | Binary asset storage (LFS) | 5dd ADR-0004 | adopted via D-07 |
| ADR-0105 | Engine verification | 5dd ADR-0005 | — |
| ADR-0106 | Canonical ID scheme | 5dd ADR-0006 | — |
| ADR-0107 | Declarative boss phase graphs | 5dd ADR-0007 | — |
| ADR-0108 | Memory fragment state machines | 5dd ADR-0008 | — |

Files: `docs/03_DECISIONS/ADR-0001…0013*.md`, `docs/03_DECISIONS/ADR-0101…0108*.md`.

## 4. Known duplicate documents (both preserved, canonical one named)

| Document | Canonical copy | Other copy (provenance) |
|---|---|---|
| C-05 successor v4.2 | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` (canonical-branch provenance) | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_FROM_3BC_LINE.md` (3bc variant, blob `7d03e1d…`) |
| MEAD | TDD-MEAD-001 (§2 above) | Agent 3 MEAD, Agent 2 MEAD (companions) |
| M0 checklist | `docs/M0_UNREAL_FOUNDATION_CHECKLIST.md` (canonical) | — |
| Master art/asset verdicts | Drive (not in repo) | `origin/arena/8efaa23f-tdd:OUR_EYES_CD_FINAL_VERDICTS_v1/` (repo mirror) |

## 5. What was NOT imported (and why)

- `TDD.uproject` + 9-module source (3bc): retired scaffold (D-01); its architecture lives in TDD-MEAD-001 §3.2 and ADR-0003.
- `TDD_GAME.uproject` descriptor + Config/Targets (8ef): retired scaffold (D-01); its **tooling, runbook, audit scripts and models** are imported; the setup helper will be adapted to the canonical project in Phase 1.
- `web_build/` vendored libraries + replay captures (8ef): re-fetchable/large; source files (`game.js`, `main.js`, `index.html`, `server.mjs`, `styles.css`) imported to `web_src/`.
- `OUR_EYES_CD_FINAL_VERDICTS_v1/` (8ef): 193-asset verdict mirror; canonical home is Drive + `The-Mhood/chat-gpt`.
- `PHASE_2_SUCCESSOR_HANDOVER_FILES/`, `TDD_PHASE2_PRODUCTION_READINESS_AUDIT_v1/` (8ef): audit history; stays on the provenance branch.
- `Config/DefaultGameplayTags.ini` (5dd): belonged to the Agent 2 scaffold, not the canonical project.
