# W1 D8 Design Work Order — Stage B/C/D Production Assignments

**Issued by:** PM/Implementation (integrated production schedule owner)
**Date:** 2026-11-20 · **Status:** ACTIVE — Stage A passed on the owner Mac at `712ee22`; production is resumed at Stage C.
**Basis:** Visual batch 1 (`1e56daf`) integrated in `9f36558`; `W1D8_VISUAL_BATCH1_INTEGRATION_RECORD.md`; `VISUAL_PRODUCTION_REGISTER.md` (14 deliverables); existing dependency gates.

Design continues its visual-development lane in parallel with implementation. These are **production assignments with dependencies and gates** — not a new roadmap. Dependencies gate delivery; nothing here reorders existing milestones.

## Assignments (in execution order)

### D-1. Guard animation set — pose board → production animation assets
- **Deliverable 1a:** Guard pose board for the confirmed set — **idle, patrol, alert, hit-react, defeat** — on the shared `HUMAN_BASE_PROPOSED` skeleton, following the Adanna six-unarmed-poses reference (`combat_animation/ADANNA_MOVEMENT_COMBAT_POSE_REFERENCE_V1.jpg`) as the pose-language authority.
- **Deliverable 1b:** Production-ready Guard animation assets for the five states, retargeted to the shared skeleton (no bone-name or scale changes — the integration architecture requires skeleton/bone-name/scale compatibility).
- **Depends on:** Stage A (passed). **Gate:** internal Design approval + retarget drop-in test (Stage C implementation owns the shared-skeleton retarget test).
- **Scheduled stage:** B → C/D (supports the M1/M3 anim set; not an M1 blocker).

### D-2. Adanna six unarmed poses → animation implementation support
- **Deliverable:** The six unarmed poses from the approved reference, prepared as animation implementation references (key poses + timing notes) for the Stage C/D anim set.
- **Depends on:** Stage A (passed). **Gate:** internal approval; implementation consumes via the retarget test.

### D-3. CH01 environment kit → implementation-ready modular assets
- **Deliverable:** Advance the approved Environment Kit V1 (`environment_kit/ENV_KIT_V1_CH01_FAMILY_COMPOUND_REFERENCE_V1.jpg` + construction-materials detail) toward **implementation-ready modular greybox-to-hero assets** for the CH01 settlement swap.
- **Constraint:** Follow the **smoother-maintained-clay-plaster correction** (the compound view is the plaster authority). Environment Kit V1 stays **provisional, never canon**; it pairs with the existing W1 D7 KIT modules.
- **Depends on:** none (parallel-safe). **Scheduled stage:** E (CH01 settlement swap, W3–4).

### D-4. Physical VFX references → in-engine implementation preparation
- **Deliverable:** Prepare the physical VFX board (`vfx/VFX_PHYSICAL_EFFECTS_REFERENCE_V1.jpg`: dust, mud-impact, rain, firelight) as implementation-ready reference packages (sprite/material/texture specs) for in-engine implementation.
- **Constraint:** **Physical base only.** No ability/supernatural VFX until gameplay defines abilities (enemy classes and abilities are HELD until story supplies definitions).
- **Depends on:** none (parallel-safe). **Scheduled stage:** D/E + M5.

### D-5. Adanna V5 / Guard V3 qualification package
- **Deliverable:** Produce the Adanna V5 / Guard V3 package through the **required Mac Blender workflow** (the same QC/deform/joint-influence pipeline used for the V3/V2 package at `2a4a88e`), with checksums and QC JSONs.
- **Depends on:** Design's M2 sculpt/character roadmap work (proceeds where dependencies permit). **Gate:** the package must pass the same qualification gate before it replaces the integration baseline.
- **Integration rule:** V3/V2 remain the active integration baseline and **V2/V1 remain rollback fallbacks** until V5/V3 passes its gate. Do not silently replace approved identity or design constraints.

### D-6. Outstanding asset qualification issues
- **Deliverable:** Resolve any outstanding asset qualification issues found in the V3/V2 package review **without** altering approved identity, skeleton, or design constraints. Report each resolution with evidence (QC JSON, checksums).

## Non-assignments (held, per existing gates)

- **Enemy/encounter classes, abilities, supernatural VFX:** BLOCKED until story supplies the class list and gameplay defines abilities. Do not invent classes, encounters, abilities, or VFX before their definitions exist.

## Coordination

- Implementation (this tree, `arena/553fb02d-tdd`) is executing Stage C now: encounter + restart flow (`3fde1f4`), camera pitch clamp (`4712b0a`), greybox map pipeline validated. Design deliverables integrate at their scheduled stages; implementation will not block on Design, and Design must not block on implementation beyond the stated dependencies.
- Completed Design deliverables move into production as they pass their gates; the PM integrates them and records evidence.
