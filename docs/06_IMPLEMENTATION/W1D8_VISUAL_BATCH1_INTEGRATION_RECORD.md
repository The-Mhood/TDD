# W1 D8 — Visual Batch 1 Handoff Integration Record

**Date:** 2026-11-20  **PM branch:** `arena/553fb02d-tdd`  **Design source:** `arena/6e649a9b-tdd` @ `1e56daf`
**Type:** Handoff acknowledgment + integration into the existing production sequence.
Updates the existing controls; **not** a new roadmap and **not** implementation.

## Acknowledgment

Design's roadmap visual batch 1 (`1e56daf`, "W1 D11 roadmap visuals batch 1") is
received and integrated into the existing production sequence
(`W1D8_PRODUCTION_SEQUENCE_AND_HANDOFF.md`). The Design branch and its history are
untouched; the visual batch files were imported file-by-file into the PM branch under
`.arena/production/2026-11-27_w1d11_roadmap_visuals/` (a new directory — no PM file
overwritten). The four reference images are valid JPEGs (verified).

**Immediate engineering priority is unchanged:** the UHT fix (commit `5ea2997`) and the
failed Mac verification. The visual batch is integrated into the sequence but does not
divert the critical path; the build + automation must be rerun on the owner's Mac for
genuine passing evidence before any engine verification is claimed.

## Imported deliverables (Design @ `1e56daf`)

| # | Asset | Path (PM branch) | Status |
|---|---|---|---|
| 1 | Adanna movement/combat pose reference (6 unarmed keys) | `…/combat_animation/ADANNA_MOVEMENT_COMBAT_POSE_REFERENCE_V1.jpg` | APPROVED — ready for PM/anim |
| 2 | Environment Kit V1 — CH01 family compound reference | `…/environment_kit/ENV_KIT_V1_CH01_FAMILY_COMPOUND_REFERENCE_V1.jpg` | APPROVED provisional |
| 3 | Environment Kit V1 — construction/materials detail | `…/environment_kit/ENV_KIT_V1_CONSTRUCTION_MATERIALS_DETAIL_V1.jpg` | APPROVED provisional |
| 4 | VFX physical effects reference | `…/vfx/VFX_PHYSICAL_EFFECTS_REFERENCE_V1.jpg` | APPROVED — physical base only |
| — | PM handoff note + visual register + research/approval record | `…/PM_HANDOFF_ROADMAP_VISUALS.md`, `VISUAL_PRODUCTION_REGISTER.md`, `RESEARCH_AND_APPROVAL_RECORD.md` | Imported |

## Integration into the existing production sequence

Each deliverable is mapped to the existing stages in `W1D8_PRODUCTION_SEQUENCE_AND_HANDOFF.md`.
No stage is reordered or skipped; the visuals slot into stages that already exist.

### 1. Adanna's six unarmed poses → Stage C (W2: M1 candidate + V3 import), then Stage D (W3: M1 gate)

- **Use:** shared-skeleton retarget test + first animation implementation.
- **Owner:** PM coordinates; implementation produces the retarget test and the first anim set.
- **Depends on:** Stage A (first green Mac train — UE compile must succeed before any in-engine anim work).
- **Design deliverable:** the 6 unarmed keys (idle, alert-ready, run stride, dodge lunge, crouch recovery, look-back), skeleton-compatible with `HUMAN_BASE_PROPOSED`, unarmed (CQ-9 deferred).
- **PM coordination:** run the shared-skeleton retarget test (Adanna ↔ Guard) using these poses as the reference; confirm the retarget needs zero bone mapping (verified identical 11-joint skeleton). Animator note carried to TD: skirt is rigid-ish at current tier — dodge/crouch keys flagged for cloth-sim/skirt-bone follow-up, not solved in the reference.
- **Tests / gates:** retarget test green; `TDD.Movement.*` + animation tests discovered and green via Mac train. **Not PASS until implementation + Mac evidence exist.**
- **Enables:** M1 movement anim (Stage C/D) and, later, M3 combat anim.

### 2. Environment Kit V1 → Stage E (W3–4: M2 traversal + Checkpoint A), CH01 settlement swap

- **Use:** CH01 settlement swap using the approved provisional compound reference + the existing W1 D7 KIT modules.
- **Owner:** PM coordinates the settlement swap; Design already delivered the reference.
- **Depends on:** Stage A (engine runtime); pairs with the existing W1 D7 KIT modules already in tree.
- **Design deliverable:** compound reference + construction/materials detail (both APPROVED provisional).
- **PM coordination:** assemble the CH01 settlement from the existing KIT modules, guided by the compound reference. **Follow the smoother plaster correction** — the detail study's mud plaster reads heavily cracked/derelict; production finish should be smoother maintained clay plaster (the compound view is the plaster authority). Status ceiling: CH01 settlement stays **provisional, never canon** (standing rule).
- **Tests / gates:** UMAP built, settlement bounds/route/collision verified in PIE; asset audit labels all provisional. **Not PASS until built + PIE evidence.**
- **Enables:** M2 forest slice / Checkpoint A environment; M5 look-dev.

### 3. Physical VFX board → Stage D/E (combat feel) + M5 look-dev (ambience)

- **Use:** dust, mud-wall impacts, rain, cooking-fire ambience.
- **Owner:** PM coordinates VFX implementation; TD reviews against the physical base language.
- **Depends on:** Stage A (engine runtime); physical effects only.
- **Design deliverable:** four physical studies (earth dust burst, mud-wall impact debris, rain on thatch, cooking-fire light/embers/smoke at dusk). No ability/supernatural VFX.
- **PM coordination:** VFX team develops from this physical base language. **No ability VFX until gameplay defines abilities** — the board is physical base only; palette ties to the environment kit.
- **Tests / gates:** VFX inventory + per-emitter budget measured; no frame-time regression vs M3 baseline (M5.4). **Not PASS until VFX implemented + perf measured.**
- **Enables:** M3 combat feedback (M3.3), M5 look-dev/ambience.

### 4. Guard animation set — CONFIRMED by PM

- **PM decision (confirmed):** the proposed Guard animation set is **idle, patrol, alert, hit-react, defeat** (as proposed W1 D7). This is the confirmed set for Design's Guard pose board.
- **Owner:** PM confirms; Design produces the Guard pose board next (register item #5).
- **Depends on:** none — confirmation is immediate; Design lead time ~1 session.
- **PM coordination:** Design proceeds to produce the Guard pose board against this confirmed set. Guard shares the `HUMAN_BASE_PROPOSED` skeleton — the pose board will be directly retarget-compatible with Adanna's set.
- **Tests / gates:** Guard pose board APPROVED by Design; retarget consistency verified. **Not PASS until the board is delivered + reviewed.**
- **Enables:** Guard animation implementation (Stage C/D), M3 combat.

### 5. Enemy/encounter classes — BLOCKED (standing hold)

- **Hold:** enemy/encounter class visuals (beyond Royal Guard class) are **blocked** until story supplies the class list. Design will **not** invent classes visually ahead of it (register item #11).
- **Owner:** PM/story supplies the class list; Design produces visuals after.
- **Depends on:** story class list.
- **PM coordination:** carry the hold; do not advance enemy visual production. The existing training enemy/boss actors remain the placeholder/mechanical baseline (no production enemy visuals until the class list lands).
- **Tests / gates:** class list supplied → Design visual production → identity/cultural review. **No visual work to PASS until the class list exists.**
- **Enables:** M4 enemy/encounter content (Stage E / W5-8).

## Integration baseline (unchanged)

Per Design's handoff: the Mac run still finishes **ADANNA_AD03_V5 + GUARD_CLASS_V3**; the
**milestone-1 FBX pair (Adanna V3 / Guard V2) remains the PM integration baseline** until
that lands. The visual batch does **not** change the integration target — V3/V2 FBX stay the
qualified builds; V2/V1 remain rollback fallbacks. No swap now.

## Claims discipline

- **Visual integration PASS** requires: implementation produced the asset/test + committed
  evidence. The visual batch is a **reference handoff**, not implementation — nothing here is
  marked visually integrated or engine-verified PASS.
- **Engine verification PASS** requires the Mac build + automation rerun green at `5ea2997+`.
  The UHT fix is in source but **not yet compiled**; the failed train stands until rerun.
- Pure-core success is not engine verification (QUALITY_LEDGER semantics).
