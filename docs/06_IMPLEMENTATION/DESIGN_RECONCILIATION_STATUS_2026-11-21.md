# Design Reconciliation & Integration Status — 2026-11-21 (post-`cf14d7e`)

**Document ID:** TDD-IMPL-RECONSTATUS-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM. **Purpose:** Reconciliation and game-wide integration report. Distinguishes **completed & evidenced**, **started but not completed**, **awaiting technical verification**, **awaiting Story input**, **awaiting Research**, **awaiting owner/CD decision**. No syntax check is reported as a functional test; no document as a completed asset; no proposal as an approved decision.
**Objective:** bring *The Disobedient Daughter* together as one coherent game — one storyline, one consistent cast, one visual world, one integrated pipeline.

---

## A. Completed & evidenced

| Item | Owner | Evidence |
|---|---|---|
| **DP-01 Zero-budget facial-likeness strategy — OWNER APPROVED** | PM + Design | Strategy doc (`53d76de`); owner approval in this directive (2026-11-21). Quality target not lowered. |
| **Facial PoC pipeline REPAIRED (v2)** — all five owner-flagged defects fixed | Character Art / Tech Art | `build_adanna_facial_poc.py` + `verify_facial_poc.py` v2 committed; portrait-guided base, portrait loaded, full 11-joint skeleton, consistent binding, QC API corrected. Syntax-verified in-sandbox. |
| **ST05–ST07 APPROVED** with owner-supplied definitions | Owner / PM | `ST05_ST07_APPROVAL_RECORD.md` v2: ST05 Rain, ST06 Market day, ST07 Gathering. Ordinary scenes; production proceeds. |
| **Enemy taxonomy RECONCILED** with Story dispositions | PM/Story | `ENEMY_DECISION_PACKAGE.md` v2: Rootwarden RETAIN, Thrall→non-humanoid swarm, Ash Hound RETAIN, Ore Sentinel, White-Arc Duelist, Maskbearer→ordinary enemy. Decision points identified for owner. |
| **Character naming audit + allocation** | PM + Research | `CHARACTER_NAMING_PLAN.md` (8 deliverables), `IGBO_NAME_CATALOGUE.md` (Research draft), `CHARACTER_IDENTITY_RECORDS.md` (20 named characters). Drive audited via connector. |
| **Registers updated** | PM | `PM_DEPENDENCY_REGISTER.md` (DP-01 approved, DP-02 v2, DP-12 approved, DP-13/14 added); `VISUAL_PRODUCTION_REGISTER.md` (ST05–07 approved, enemies reconciled, naming added). |

## B. Started but not completed

| Item | Owner | What remains |
|---|---|---|
| **Facial PoC v2 — owner-Mac execution** | Owner (sole Blender/UE authority) | Run `run_facial_poc.sh` on the Mac with `PORTRAIT_PATH` set; capture evidence bundle. **Not technically approved until run.** |
| **Character identity records — supporting cast refinement** | PM + Character Art | Main cast (7) established; supporting cast (13) in compact form, refined as their assets are produced. |
| **Scene production for ST05–ST07** | Design | Briefs ready; visual production of the three approved ordinary states proceeds. |

## C. Awaiting technical verification

| Item | Owner | Verification required |
|---|---|---|
| **Facial PoC v2 functional validation** | Owner Mac | Build + QC (QC_RESULT.json QUALIFIED) + owner visual review vs portrait + UE import. **Syntax check ≠ functional test** — v2 is syntax-verified only; functional validation is the owner-Mac step. |
| **Adanna AD-03 V3 / facial FBX in UE** | Engineering + owner | Import + acceptance tests per INTSPEC. |

## D. Awaiting Story input

| Item | Owner | What's needed |
|---|---|---|
| **Character naming allocation — narrative fit** | Story | Review the 20 retain decisions for narrative consistency; confirm the Nneka–Ezeani–Adanna relationship is unchanged. |
| **Maskbearer replacement enemy name** | Story/PM → owner | Propose a name for the ordinary physical enemy replacing the rejected mask identity. |
| **Enemy taxonomy — narrative confirmation** | Story → owner | Confirm the reconciled dispositions (esp. Thrall non-humanoid swarm, White-Arc Duelist in Ch.5) before owner ratification. |

## E. Awaiting Research

| Item | Owner | What's needed |
|---|---|---|
| **Name-catalogue specialist verification** | Research | Verify LOW/MEDIUM-confidence meanings: Adanna, Ezeani, and the 9 unverified supporting names (OAD-15); finalise the catalogue with traceable sources. Distinguish traditional vs modern/Christian reinterpretations. |
| **Candidate names for future gaps** | Research | Verify §5 candidate meanings (only used if a genuine gap emerges — no cast inflation). |

## F. Awaiting owner/CD decision

| Item | Owner | What's needed |
|---|---|---|
| **DP-03 Enemy taxonomy ratification (CD-3)** | Owner/CD | Ratify the reconciled six (per-archetype KEEP/REVISE/REJECT/APPROVE); confirm cultural points; approve the Maskbearer-replacement name. |
| **DP-04 Cultural review (CD-2)** | Owner/CD | Engage/confirm consultant for sensitive items: Amadioha & Idemili (deities), Okwu (masquerade-adjacent), Ezeani regalia (OAD-03), Hollow King funerary framing. |
| **DP-13 Character naming allocation approval** | Owner/CD | Approve the 20-character retain allocation (after Story review). **No Drive asset modified until approved.** |

## G. Connected deliverables (departments tied together)

The integration relationships PM coordinates are now operational:
- **Story ↔ naming:** every proposed name checked against identity, relationships, chapters, narrative purpose (Nneka–Ezeani–Adanna unchanged).
- **Research ↔ naming:** catalogue supplies names + evidence; does **not** assign to characters.
- **Design ↔ environments:** ST05–ST07 approved; scene production proceeds.
- **Character Art ↔ facial likeness:** v2 pipeline repaired; owner-Mac execution is the next step.
- **Technical Art ↔ pipeline/qualification:** skeleton, binding, QC all corrected in v2.
- **Engineering ↔ UE integration:** INTSPEC delivered; import/acceptance pending the PoC FBX.
- **PM ↔ registers/decisions:** DP-01 approved, DP-12 approved, DP-02/03/04/13/14 tracked with owners, deliverables, blockers, dates, criteria, evidence.

## H. What is NOT claimed (honesty)
- The facial PoC is **not built, not qualified, not reviewed, not accepted** — v2 is a repaired, syntax-verified pipeline; functional validation and the visual likeness verdict are the owner-Mac step.
- The enemy roster is **not approved** — Story dispositions are reconciled recommendations; CD-3 ratification is still required.
- Character names are **not reassigned** — the allocation retains all 20; Drive assets are untouched until Story + owner approve.
- ST05–ST07 are **approved** — this is the one item moved to completed this cycle.
- The Igbo name catalogue is a **Research draft** — meanings marked LOW/MEDIUM require specialist verification before being treated as established.

## Next PM cycle (priorities)
1. Owner runs the facial PoC v2 on the Mac → evidence → likeness verdict (DP-02).
2. Story reviews the naming allocation → owner approves (DP-13).
3. Research verifies flagged name meanings (DP-13/E).
4. Owner/CD ratifies the enemy roster + Maskbearer-replacement name (DP-03).
5. Continue ST05–ST07 scene production and connect character/environment/asset registers into one integrated record.
