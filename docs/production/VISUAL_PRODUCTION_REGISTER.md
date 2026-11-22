# Visual Production Register — Controlled Production Status

**Document ID:** TDD-REG-VISUAL-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** Design Lead. **Purpose:** Track every visual asset through controlled production status. **No exploratory asset is promoted to APPROVED PRODUCTION without required sign-offs** (QUALITY §7).
**Rule:** This register is the single controlled-production source for visual assets. An asset here is *not* production-approved until its status is `APPROVED PRODUCTION` with the sign-off evidence recorded.

## Status model

| Status | Meaning | Promotion requirement |
|---|---|---|
| `ID_RESERVED` | Asset identified in a brief/spec; not started | — |
| `WIP` | Work in progress (exploratory) | — |
| `QUALIFYING` | Being qualified (Design visual review) | Automated QC pass + owner visual review |
| `QUALIFIED` | Passed qualification (visual + technical) | Owner-Mac verification + qualification evidence |
| `APPROVED PRODUCTION` | Production-approved and cleared for use | All sign-offs + any cultural (CD-2) / enemy (CD-3) gates cleared |
| `HELD` | Blocked (cultural/approval) | Gate cleared before promotion |
| `REJECTED` | Rejected with rationale | — |

## Register

| Asset | Type | Owner | Status | Blocking gate | Last update | Sign-off evidence |
|---|---|---|---|---|---|---|
| Adanna character (full body) | Character | Character Art | QUALIFYING | None (identity approved) | 2026-11-21 | M1 spec + qualification package |
| Adanna facial likeness (PoC) | Facial rig | Character Art / Tech Art | **WIP (pipeline v2.1 ready; face NOT built)** | owner-Mac execution (sole Blender authority) | 2026-11-21 | Pipeline v2.1 repaired + syntax-verified (verifier opens .blend, backdrop excluded); actual Blender face NOT yet produced |
| Guard NPC | Character | Character Art | QUALIFYING | None | 2026-11-21 | Shares `HUMAN_BASE_PROPOSED` skeleton |
| Shared skeleton (`HUMAN_BASE_PROPOSED`) | Skeleton | Technical Art | QUALIFIED | None | 2026-11-21 | W1D7 manifest verified (11 joints) |
| M1 Environment Kit V1 | Environment | Design / Eng | QUALIFYING | None | 2026-11-21 | Provisional, never canon |
| Interaction volumes + markers | Prop/Actor | Design / Eng | ID_RESERVED | None | 2026-11-21 | Spec defined |
| CH01 environment states ST05–ST07 | Environment state | Design / owner | **APPROVED PRODUCTION** | None (owner-approved 2026-11-21) | 2026-11-21 | `ST05_ST07_APPROVAL_RECORD.md` v2 APPROVED; ordinary scenes, no ritual/shrine |
| Rootwarden enemy | Enemy | Agent 2 | `HELD` | CD-3 ratification (Story: RETAIN) | 2026-11-21 | PROPOSED; fictional slow bruiser |
| Thrall enemy | Enemy | Agent 2 | `HELD` | CD-3 + CD-2 (Story: REVISE → non-humanoid swarm) | 2026-11-21 | PROPOSED; swarm, not the dead |
| Ash Hound enemy | Enemy | Agent 2 | `HELD` | CD-3 ratification (Story: RETAIN) | 2026-11-21 | PROPOSED; ash flanker, no remains |
| Ore Sentinel enemy | Enemy | Agent 2 | `HELD` | CD-3 ratification (Story: REVISE → Ore Sentinel) | 2026-11-21 | PROPOSED; renamed from Ore Thrall; no flame |
| White-Arc Duelist enemy | Enemy | Agent 2 | `HELD` | CD-3 + CD (Story: REVISE → White-Arc Duelist) | 2026-11-21 | PROPOSED; renamed from Thunder Aspirant; white lightning |
| [Maskbearer replacement] enemy | Enemy | Agent 2 | `HELD` | CD-3 ratification (Story: REJECT mask identity → ordinary enemy) | 2026-11-21 | PROPOSED; mask identity rejected; name TBD |
| Character naming (20 named) | Naming / identity | PM + Research + Story | **QUALIFYING** (records authored) | Story narrative-fit + owner approval (DP-13) | 2026-11-21 | `CHARACTER_NAMING_PLAN.md`, `CHARACTER_IDENTITY_RECORDS.md`, `docs/06_IMPLEMENTATION/IGBO_NAME_CATALOGUE.md` |
| Research name catalogue (DP-15) | Naming / identity | Research (PM merged) | **DELIVERED** (reconciled) | Specialist verification of flagged meanings | 2026-11-21 | `docs/IGBO_NAME_CATALOGUE.md` (commit `41252e5`, cherry-picked `0b30cdf`); DP-15 CLOSED |

## Notes
- **Enemies:** all six are `PROPOSED` (CD-3 not ratified). Story dispositions reconciled in `ENEMY_DECISION_PACKAGE.md` v2 (Rootwarden RETAIN, Thrall→non-humanoid swarm, Ash Hound RETAIN, Ore Sentinel, White-Arc Duelist, Maskbearer→ordinary enemy). None is canon, none is built. CD-3 ratification still required.
- **ST05–ST07:** OWNER APPROVED (2026-11-21) — ordinary environmental/community scenes; production proceeds. No ritual/shrine/masquerade without a story requirement + cultural verification.
- **Facial likeness:** PoC pipeline **repaired (v2.1)** — portrait-guided base, full skeleton, consistent binding, QC corrected (verifier opens .blend; backdrop excluded from FBX). Syntax-verified; **actual face NOT yet built**. Owner-Mac procedure issued (`pipeline/facial_poc/FACIAL_POC_OWNER_EXECUTION_PROCEDURE.md`); **not** technically approved until the owner runs it (DP-02).
- **Character naming:** 20 named characters audited from Drive; all names retained (no inflation). Research catalogue (`docs/IGBO_NAME_CATALOGUE.md`, `41252e5`) reconciled (DP-15 CLOSED). Drive assets **not modified** until the allocation is reconciled and approved (DP-13).
- **Promotion rule:** `WIP → QUALIFYING → QUALIFIED → APPROVED PRODUCTION` requires automated QC pass + owner visual review + owner-Mac verification; enemies additionally require CD-3 ratification + CD-2 clearance where applicable; naming requires Story + owner approval before any Drive asset is touched.
