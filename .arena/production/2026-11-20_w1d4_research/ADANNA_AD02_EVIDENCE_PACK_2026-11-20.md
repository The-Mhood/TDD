# ADANNA — AD-02 EVIDENCE PACK FOR CD CANDIDATE SELECTION (2026-11-20, native-res verification applied)
Purpose: everything CD needs to select V003 vs V004 vs require correction. **CD selects; this review does not.** Sources: approved master (`CHAR_ADANNA_MASTER_REFERENCE_V001`, status APPROVED 2026-11-15) · approved portrait (`REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001`) · plates V004 FRONT/THREE_QUARTER + V003 BACK/LEFT_SIDE (sha256-stamped in `FP10_FRESH_PASS_MANIFEST.csv` and Drive metadata; plate chrome intact).
**Verification method:** display-scale pass (all four plates) + native-resolution crops (FRONT V004 head/waist, THREE_QUARTER arms, BACK V003 baldric, LEFT_SIDE face/arms), crops staged under this folder (`fr_head.png`, `fr_waist.png`, `tq_arms.png`, `ls_face.png`, `ls_arms.png`, `bk_baldric.png`).

## Lock-by-lock verification (native-res where resolvable)
| Lock | FRONT V004 | THREE_QUARTER V004 | BACK V003 | LEFT_SIDE V003 | Master (reference) |
|---|---|---|---|---|---|
| Scar LEFT cheekbone | ✓ viewer-right cheekbone, small diagonal — present at native crop | far-side (her LEFT) per view note — foreshortened, not resolvable, not a defect | n/a (back) | near-side profile; face small at crop size — not resolvable; not a defect | present ✓ |
| Coiled armlet LEFT upper arm | ✓ viewer-right upper arm (her LEFT), plain concentric coils | ✓ viewer-right frame arm = her LEFT per view-note geometry — verified at native crop; plain concentric coils | ✓ viewer-left arm (her LEFT; back view is non-mirrored) at native crop | ✓ near arm = her LEFT (faces camera) — plain coils | LEFT ✓ |
| Temple beads 3B+2C LEFT | ✓ viewer-right temple — bronze cuffs + coral beads visible at native crop | far temple, foreshortened — unverifiable at crop; consistent with note | n/a | ✓ near temple — 3 bronze + coral cluster at native crop | LEFT ✓ |
| Spiral pendant (FICTIONAL) | ✓ sternum, spiral visible at native crop | ✓ sternum (small, native crop) | n/a (back) | ✓ at chest edge | spiral ✓ |
| Baldric L shoulder → R hip | ✓ enters over viewer-right shoulder (her LEFT) at native head crop; exits viewer-left waist (her RIGHT hip) at native waist crop | ✓ viewer-right shoulder (her LEFT) → viewer-left hip (her RIGHT) at native arms crop — CORRECT | ✓ viewer-left shoulder (her LEFT) → viewer-right hip (her RIGHT) at native crop | ✓ over near (her LEFT) shoulder crossing front | L→R ✓ |
| Knot/braids | high knot, fall to blades ✓ | high knot ✓ | full fall to blades ✓ (seen at native back crop) | knot + fall ✓ | same ✓ |
| No blade/scabbard (CQ-9) | absent ✓ | absent ✓ | absent ✓ | absent ✓ | n/a (CQ-9 open) |

## DEFECTS / FLAGS (verified)
- **D1 (RESOLVED — not a defect):** display-scale read suggested a baldric-shoulder ambiguity in THREE_QUARTER V004; native-res crop shows the route correctly enters her LEFT (viewer-right) shoulder and exits her RIGHT hip. No plate swap.
- **D2 (RESOLVED — not a defect):** armlet visible on the TQ frame-right arm = her LEFT per the plate's own view note (near side = her RIGHT) — correct side. The armlet is NOT swapped.
- **D3 (minor, all plates):** pendant cord curvature and drape vary panel-to-panel within painterly tolerance; the model must follow the master ref, not any single plate's cord. No re-render required.
- **D4 (OPEN — composite set):** the four-plate set is a composite of two versions — FRONT/THREE_QUARTER **V004** superseding FRONT/THREE_QUARTER **V003**, plus BACK/LEFT_SIDE **V003**. V004's correction ledger claims only "pendant cord and three-quarter arm" changed, but no mass/consistency measurement across the mixed set has been run. **CD must explicitly accept a mixed-version set (or order a single-version rebuild of BACK/LEFT_SIDE to V004) before AD-03 build.**
- **D5 (expected):** every plate carries status chrome ("REVIEW REQUIRED" / "UNAPPROVED"); nothing may be stripped by review. Plates remain unapproved until CD records selection and registers move.
- **D6 (unverifiable, recorded):** scar detail in LEFT_SIDE (face too small at native crop); pendant cord curvature in BACK (hidden); bead count per temple in THREE_QUARTER (foreshortened). None blocks selection; all are model-phase checks (workbook §10.2 pre-flight).

## RECOMMENDATION TO CD
1. **FRONT V004, THREE_QUARTER V004, BACK V003, LEFT_SIDE V003 are lock-consistent at native resolution.** Eligible for selection as the direction for AD-03, PROVIDED CD explicitly accepts the mixed-version composite (D4) or orders a version-alignment plate first.
2. If CD rejects the composite: order V004 BACK and V004 LEFT_SIDE re-renders (two plates), not a full regen.
3. After selection: AD-03 pipeline build (TD-SPEC-001 Addendum A; identity-lock pre-flight = workbook §10.2; armlet consultant gate OPEN — plain coil profile only, no medallion, no new motifs).
4. Downstream blocked-on-CD: LOD0 build start; AD-04 PM minimum-animation definition; final texture set approval (a procedural v1 BASE set now exists — `../textures/` — TD ratifies on import; it is not a substitute for painted final art).
5. Do NOT promote/move plates; approval lives in the register; review pack stays read-only.
