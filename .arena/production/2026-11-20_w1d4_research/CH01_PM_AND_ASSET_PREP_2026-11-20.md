# CH01 — PM COORDINATION + PRODUCTION ASSET PREP (2026-11-20, W1 D4)
**Basis:** provisional greybox authorised (C-01, owner 2026-11-20) · `CH01_GREYBOX_PLAN.png` verified · builder v0.1 env-blocked · greybox stays an *engineering* artefact — never canon, never art. **Status discipline: engineering assumptions are listed in §B and are NOT approved cultural canon.** No architecture/prop/material is final through this document.

## A. BUILDER OUTPUT REQUIREMENTS (for PM/TD to verify on the first successful run)
1. **Determinism & manifest:** builder must write `CH01_GREYBOX_MANIFEST.json` listing every object, its token, transform, collision class, and anchor list; re-run must be idempotent (same inputs → same names/counts).
2. **Scale:** 1 Blender unit = 1 m in source; FBX export cm-consistent with FP-07; no per-asset scale fudging. Gate gap, wall height (1.5–2.5 m), hut eaves, stall heights all tagged in the manifest as ASSUMPTION (not canon).
3. **Collision:** box primitives for huts/stalls/wall ring; capsule exclusion for posted NPCs; anchors as empties with stable names (`ANC_*`); no concave collision on walls.
4. **Lights/probes:** none baked; engine-side only.
5. **File set:** `CH01_GREYBOX_vX.blend` + `CH01_GREYBOX_vX.fbx` + `CH01_GREYBOX_MANIFEST.json`; version bump on every re-run; old versions kept.
6. **FBX axis/scale check on first Unreal import** (rotate -90° or axis rule per TD-SPEC-001 Addendum A) — PM confirms no unit drift before any walkthrough.
7. **Walkthrough script for PM (10 checks):** gate→square walk · palace axis line-of-sight · spawn anchor trigger zones · patrol route anchors A–D passable · stream wading entries reachable · farm fork decision legible · compound wall ring closed · hut interiors entered (no stuck spots) · market stall rows navigateable · backroom door anchors aligned to wall openings.
8. **Failure logging:** any deviation logged in the manifest AND reported to TD; greybox fixes never edit the FBX by hand in Unreal.

## B. ENGINEERING ASSUMPTIONS (adjustable by PM/TD; NOT canon)
Wall height 1.5–2.5 m · gate width ≈2.2 m · hut eaves 2.2–3.0 m · stall footprint 2×3 m · mbara ezi (courtyard) ≈ 18×14 m · stream width ≈4 m · palace portal block height ≈6.5 m · verandah post spacing 3.0 m · all wall/roof/bamboo geometry = placeholder massing · all timber = generic brown box material · all thatch = placeholder plane/loft · "palace" composition = axis + portal + verandah rhythm only (no palace grammar approved).

## C. WHAT REMAINS DESIGN- (NOT ENGINEERING-) OWNED
Gate joinery · wall cap profile · thatch lap · uli/motif policy (expected: NONE per OAD-06 generic lines; Research must confirm) · substrate tint/mortar · vegetation palette · CH01 biome ruling · palace designation vs fiction · SUB-017/EXP-003/004 art targets · SCN-012-class Sahelian-leak prevention (see FP-10 report) · M̀barị̀/shrine forms excluded entirely. **None of these may be locked by greybox or by this document.**

## D. PRODUCTION-READY TARGET ASSET LIST (gated; prepare briefs only — NO generation)
| Asset | Type | Gate to start | Source plate (FP-10 verdict) |
|---|---|---|---|
| Mud-laterite wall kit (wall/corner/gate-pier) | modular mesh | CD art-target approval + grammar ruling | ENV-CH01-SUB-017 (ref) |
| Thatched hipped roof kit (2 pitches) | modular mesh | same | SCN-006/007 (refs) |
| Compound gate frame + posts | hero prop | same | SCN-019 (PASS ref) |
| Market stall kit + goods dressed | modular + dressing | same + dressing density ruling | SCN-011/012 (SCN-012 needs REVISE) |
| Water-point basin + pots | prop cluster | same | SCN-014 (ref) |
| Forest path / clearing / pool biome set | environment kit | biome ruling | EXP-003 (ref), EXP-004 (flag: verify biome), EXP-005 (REVISE) |
| Stream + wading entries | environment kit | PM walkthrough pass | greybox only |
| Palace portal block | hero architecture | palace grammar research + CD ruling | SCN-030 (REVISE — do not build from it) |
| Guard shelter (gate) | prop | subject ruling (PROPOSED) + FP-10 | SCN-019 |
| Palm-wine shelter | prop | subject ruling (PROPOSED) + FP-10 | SCN-020 |
| Street/lane set | environment kit | CD art-target approval | SCN-021/022 (refs) |
**EXP-005 (THE_STILL_POOL)** failed biome review — flora reads non-W-African; do not use as CH01 target without correction. **SCN-030** rejected as a palace target (no grammar). **SCN-012** requires Sahelian-grammar rebuild before any market-stall final.

## E. PM DEPENDENCY PRECISION (no workstream-wide holds)
- **PM → TD/Builder:** run greybox (§A) — blocked only on a capable machine/docker runner; not on any art review.
- **PM → Design (us):** SCN-017/SCN-024 dispositions (REJECT-lineage) — affects only those two boards, not the whole CH01 set.
- **PM → CD/Research:** art-target approvals (D above) — independent of greybox run.
- **PM → Research (CH03):** ENV-CH03 DEFER pair — CH03-only items; no CH01 dependency.
- **Greybox does NOT block** design-board reviews, texture work, Adanna build, or RG prep. Design boards do NOT block the greybox.

## F. UNREAL INTEGRATION NOTES
Import FBX → `SM_CH01_*` naming · cm scale · `_GRY` suffix for greybox versions · separate folder `Content/CH01/GRYBOX/` · no collision from UCX until PM verifies §A-7 walkthrough · LOD0 only · single grey material + anchor debug materials · lighting = default preview, no baked GI · screenshot the §A-7 walkthrough for the W1 D5 report.
