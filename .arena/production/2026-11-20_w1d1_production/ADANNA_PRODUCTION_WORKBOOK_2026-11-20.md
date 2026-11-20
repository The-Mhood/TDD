# ADANNA — PRODUCTION WORKBOOK (W1 D1)
**Prepared 2026-11-20 · Original VA · status: PRE-PRODUCTION EVIDENCE & SPEC DRAFT — nothing here is modelled, promoted, or approved**
Sources: approved `CHAR_ADANNA_MASTER_REFERENCE_V001` (md5 901a5009…, Drive `1k08XH8VjNJAnSoMNU4YvBPtBEUdYD20y` / approved copy `1FY3hw3602iB-1405RgUIO3ih2USmck_Y`) · `REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001` (`1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF`) · turnaround **V004/V003 candidates** (workspace `google_drive/`, uploaded 2026-11-18, md5s per 2026-11-18 sync log; REVIEW REQUIRED) · V001/V002 turnaround plates formally REJECTED 2026-11-17 (8 reports, `1x5T4V3R-…`).
**Standing:** blade/scabbard (CQ-9) OPEN · armlet U-14/U-18 consultant gate OPEN · pendant FICTIONAL · design-approved ≠ canon anywhere in this file.

---

## 1. EXACT TECHNICAL SPECIFICATIONS — CURRENT STATE vs MISSING (the FP-07 target list)

Legend: ✅ locked in an approved source · 🟡 exists only as board text/raster (not a spec) · ❌ missing entirely — must be created/ratified before or during production.

| Element | Value today | Class | Needed for |
|---|---|---|---|
| Identity: face, scar (LEFT cheekbone), hair knot, beads (3 bronze + 2 coral LEFT temple), cuff count | Master ref + portrait locks | ✅ | Model/face likeness, textures |
| Proportion lock: "about 7.5 heads tall" | Board text | 🟡 | Basemesh proportions |
| Absolute height | none | ❌ | Camera, collision, rig scale — **ratify in TD-SPEC-001 (proposal: 1.80 m; head unit 24 cm — NOT decided)** |
| Eye height / camera calibration | none | ❌ | Greybox camera, anim |
| Hand length (weapon scale) | none | ❌ | Blade/scabbard build (CQ-9) |
| Head-to-floor in raster candidates | ≈1,095–1,125 px (see §2) — **CONSISTENT with board note "1099–1103 px"** (raster scans 2026-11-20: crown band ≈185 abs vs header-offset-adjusted board 57; height ≈1,100) | 🟡 raster read, ±10 px | Alignment sheet for the accepted set (AD-02); not a build number |
| Shoulder span | ≈1.32–1.38 heads raster (≈205–215 px on 2560-px plate) | 🟡 | Basemesh shoulders |
| 7.5-head ratios table (vertex–chin–clavicle–nipple–waist–hip–knee–ankle–floor) | ❌ | ❌ | Basemesh; to be extracted in modelling SOP from accepted plates |
| Blade/scabbard length, carry height, cross-draw clearance | ~60 cm "plain leather scabbard, ~60 cm" exists as board text only (V002/V004 lineage notes; no TD ratification) | 🟡 | CQ-9 closure; collision/socket; draw anim |
| LOD bands, tri budgets, texel density, texture sizes | proposals only (this doc §6–§7) | ❌ ratified numbers | Model + budget pass |
| Skeleton/joint set, skin weights/Influences | proposals (this doc §5) | ❌ ratified | Rig |
| Face shape set (FACS subset) | proposal ≥18 shapes (§5) | ❌ ratified | Rig/anim |
| Animation list + counts, foot-lock tolerances, root-motion policy | proposal (§8) | ❌ ratified; needs AD-04 input | Anim |
| Collision capsule + hit boxes + damage scalars | proposal (§9) | ❌ ratified | Gameplay integration |
| Engine, platform, budget class, tools | **UNSPECIFIED anywhere** | ❌ | Everything; **owner decision required** |
| File formats & naming, package manifest, LFS/repo path | conventions exist for images; not for engine assets | ❌ | Integration |

## 2. MEASURED FROM THE ACCEPTED-CANDIDATE RASTER (FRONT V004, 2560×1440) — ADVISORY ONLY
Method: PIL grid overlay (`measurements/front_v004_grid.png`) + pixel-count scans; figure limited to panel x∈[80,1130]; all values **±4–10 px**, painterly source, no sub-pixel truth. Not a build spec; TD ratifies nothing from this section without the AD-02 ruling and the alignment sheet.

| Landmark (absolute px, board top y=0) | Value |
|---|---|
| Top of high knot (crown) | ≈ 165–190 (first dark raster row ≈ 185–190; grid eyeball 168) |
| Vertex (skull top, hair excluded) | ≈ 215–235 |
| Chin | ≈ 375–385 |
| Head unit (vertex→chin) | ≈ 140–160 px |
| Clavicle / acromio line (shoulder y) | ≈ 395–425 |
| Shoulder span (deltoid edge → edge) | ≈ 945→1155 px (grid; right edge clipped by x limit in scan) ≈ 205–210 px |
| Nipple/bust line | ≈ 460–470 |
| Bandeau lower edge / upper rib | ≈ 545–555 |
| Natural waist | ≈ 575–605 |
| Hip bone / wrap top | ≈ 600–630 |
| Skirt hem | ≈ 1155–1200 |
| Ankle | ≈ 1240–1255 |
| Floor (sole) | ≈ 1280–1290 |
| Total figure height — raster (knot-top→floor) | ≈ 1,095–1,125 px (≈ 1,100 nominal) |
| Board's own recorded geometry (V003/V004 notes) | "crown row 57 · floor 1155–1159 · height 1099–1103 px" |
| Consistency check (2026-11-20 pass 3, crop x∈[80,1110]) | **CONSISTENT** — crown abs band ≈185–235 vs board's 57 explained by the board's own header offset (≈+125); floor ≈1280–1290 vs note's 1155–1159 sits ≈+125 lower for the same reason; standalone height ≈1,100 px matches note 1099–1103. The earlier "conflict >100 px" wording was an artefact of comparing absolute rows across two origin canvases — retired. TD still fixes the canonical canvas & panel offset in TD-SPEC-001 (panel provenance, not a geometry dispute). |

**Ratios (knot-to-floor H≈1,100 px, head≈150 px):** ≈ 7.3 heads raster — nominally consistent with the "about 7.5 heads" lock (build text is the lock; raster is a check, not the law). Shoulder-to-head ≈ 1.36. Waist ≈ 0.62 H. Hem below knee ≈ 1170 px (≈ 0.87 H).

**Identity-lock compliance (FRONT V004 plate, 1:1 view):** scar on LEFT cheekbone ✓ present (viewer-right) · coiled bronze armlet LEFT upper arm, plain concentric coils, no fused medallion ✓ · spiral pendant on braided cord ✓ present · LEFT temple cuffs/beads ✓ (3 bronze + 2 coral) · baldric anatomical LEFT shoulder → RIGHT hip ✓ · right-hand cross-draw scabbard — **absent by design (CQ-9 open)** ✓ · 0 human figures, unapproved chrome intact ✓. V002-class defects (medallion fusion, scar flip, sidebar inversion, plate-number repeat, false view-note) = **absent** in this plate per its own correction ledger; independent Our Eyes re-check is the required gate (AD-02), not my assertion.

## 3. MODEL / TOPOLOGY REQUIREMENTS (for AD-03 sign-off; bands are proposals)
- **Tri budget bands (proposal, TD ratifies):** LOD0 ≤ 35k · LOD1 ≤ 18k · LOD2 ≤ 8k · LOD3 ≤ 3.5k.
- **Topology:** quads-dominant; ≥3 eye loops; nose/mouth/jaw loops; shoulder/elbow/wrist/hip/knee/ankle loops; clean baldric→skirt junction loop; hands 2-segment fingers with sword-grip loops; poles away from deform zones; mirror L/R until intentional asymmetry (scar side, armlet, pendant, scabbard); watertight pre-UV; no n-gons >4 in deforming regions.
- **UVs:** single UV0 (UDIM optional); consistent texel density (target set in FP-07); seams hidden; scabbard/baldric/pendant as **sockets/submeshes**; no mirrored-island overlap outside undergarment/hair (flagged).
- **Detail fidelity vs approved sources only:** scar geometry must land on the anatomical LEFT cheekbone plate-matched; armlet coil count/pitch matched to master ref panel (measure in modelling SOP; master ref panel is native-res crops); pendant spiral = ref-matched; 3 bronze cuffs + 2 coral beads at LEFT temple.

## 4. MATERIALS & TEXTURES (proposals; FP-02/FP-01 sign-off assumed)
- Skin SSS/pre-integrated; bronze (armlet/pendant/cuffs) = aged cast bronze, single shared material, polished vs worn mask zones; indigo cotton = woven, macro variation; leather = vegetable-tanned, worn strap variant with contact darkening (ref: LEATHER STRAP panel); hair = deep brown, matte, 3 braid groups + loose ends; scabbard (when CQ-9 closes) = plain leather + indigo cord wrap.
- Maps: BaseColor/Normal/Roughness (+Metallic bronze; +AO where authored; Height LOD0 only if used). 4K face/body base, 2K costume/prop. No flat albedos; no baked directional light.
- Palette conformance vs FP-01 swatches (#06080D/#121215/#241916/#2B3338/#403D3E/#44525C/#677A85) with deviations logged; indigo may run brighter per ref; coral constant.
- Pendant + ornament IDs carry FICTIONAL-provenance tags in the material manifest; no Igbo-emblem claims — culture note stays on every deliverable.

## 5. RIG
- Humanoid: spine 3, neck+head(+jaw), clavicles, 2-seg arms, hands full fingers, 2-seg legs, feet+toes; ≤4 influences/vertex (engine-dependent); zero unbound verts at hand-off.
- Face: FACS-subset ≥18 shapes (brow in/out up/down ×4, eye squint/wide ×2, cheek raise, nose sneer, lip stretch/press/smile/frown/open) or equivalent delta coverage; lip-sync out of slice scope unless AD-04 says otherwise.
- Cloth: sash/wrap = 4–6 bones + hip collision sphere; LOD0 optional 1-bone flutter; no cloth solver dependency in slice.
- Sockets: `Socket_Scabbard` (left hip, AD-01-ratified vector), `Socket_Baldric` (left shoulder→right hip), `Socket_Pendant` (sternum), weapon grip socket per AD-01.
- QC: bind pose = approved neutral (match portrait camera family); A-pose vs T-pose per FP-07 #7; no foot-slide >5 mm at 30 fps in locomotion loop test.

## 6. ANIMATION (set sized by AD-04; proposal if waiver limits scope)
- Non-combat (14): idle ×2 · walk ×2 · run · sprint · start/stop · crouch/sneak · sit · crouch_to_stand · interact_reach · talk_gesture ×3 · sheath_unsheathe · carry_pose.
- Combat (adds 14–18): draw, light ×3, heavy ×2, block, dodge ×4, pain ×2, death ×2, hit_react combo.
- Naming `ADANNA_<state>_<variant>`; clip length ≤150 fr; in-place (no root motion) unless engine ruling; montage video required for sign-off; thumbnails in review pack.
- Counts/tolerances ratified in TD-SPEC-001; **combat set is blocked on AD-04**; without it the package ships non-combat + `ADANNA_POSE_READY` placeholder only, clearly labelled PROVISIONAL.

## 7. LODs & COLLISION
- LOD0–LOD3 per §3; transition screen-height thresholds TD-set; LOD3 keeps scabbard/baldric silhouette read.
- Controller capsule: radius/height TD-ratified (proposal: r 0.34 m, h 1.72 m on 1.80 m figure).
- Hit boxes: head/torso/pelvis/upper-lower arm/hand/thigh/shin/foot; per-box scalars TD-ratified; no per-poly; LOD-independent; debug capture mandatory in evidence pack.
- Scabbard/baldric: no damage, no blocking collision in slice.

## 8. WORK THAT CAN BEGIN TODAY vs GATED (the split you asked for)
**Begin now (no approvals required; non-destructive, evidence-producing):**
- This workbook; TD-SPEC-001 §measurements (done — §2) as the substrate for ratification.
- Re-measure accepted plates once AD-02 rules; produce alignment sheet (Assistant VA, after AD-02).
- UV/topology SOP draft from §3 (template reused for enemy); material ID map from §4 (no textures baked yet — texture *authoring* is gated by AD-03).
- Evidence-pack scaffolding (report MD/CSVs) from §9 of the plan; budget-checker script (tri/texel checks) — automatable, quality-safe.
- Toolchain discovery (engine present? viewer? DCC?) — owner answers FP-07 #7.

**Gated — do NOT start:**
- Mesh/basemesh generation (needs AD-02 candidate ruling + FP-07) · texture authoring (AD-03) · rig (AD-03) · anims (AD-04) · CQ-9-dependent geometry (sword/scabbard final forms) · any promotion/move of plates · any image regeneration (paused).

**Blocked on owner (nothing in this package outruns these):** AD-01 CQ-9 · AD-02 AD-03 AD-04 · FP-07 #7 engine/tools · FP-06 consultant (pendant stays FICTIONAL regardless).

## 9. EVIDENCE SO FAR (traceability)
- FRONT V004 pixel scan outputs (raw values in §2; grid overlay at `measurements/front_v004_grid.png`, md5 to be captured at pack time).
- Board-recorded geometry quoted verbatim from V003/V004 plates ("crown row 57 … 1099–1103 px"); 2026-11-20 pass-3 scan found it **consistent** with the raster (height ≈1,100 px; board crown 57 + header offset ≈ +125 = abs ≈185). Residual action = TD canonical canvas ruling, not a data dispute.
- Rejection evidence preserved: 8 turnaround plates REJECTED 2026-11-17; V004/V003 remain PENDING, unapproved.

## 10. MODELLING → ENGINE PIPELINE REQUIREMENTS & DELIVERABLE MANIFEST (Blender→Unreal, DRAFT — 2026-11-20 W1 D2)
Prepared so production can start the day AD-02/AD-03/FP-07 #7 land. Nothing below promotes or approves anything; all values tagged DRAFT are proposals for TD ratification.

### 10.1 DCC → engine chain (assumption flagged: FP-07 #7 UNSPECIFIED — chain below is the working default until owner rules otherwise)
1. **Blender (source of truth)** — modelling, UV, sculpt→retopo flow, material ID pass, vertex colour for masking where useful.
2. **Export** — FBX 2020 binary, units metric (1 BU = 1 cm workflow in Blender or 1 BU = 1 m with Unreal scale 100 — **pick once in TD-SPEC-001 and never mix**); transforms applied (loc/rot/scale), +Z up → FBX exporter handles Unreal axis; smoothing = face/edge split normals only after custom split normals are intentional; no ngons in deforming regions at export.
3. **Textures** — Substance/equivalent authoring → 4K face/body, 2K costume/props; BaseColor, Normal (OpenGL→DirectX flip at import decision TD-set), Roughness, Metallic (bronze only), optional AO pack; sRGB/linear discipline: BaseColor sRGB, data maps linear; no baked lighting.
4. **Unreal** — import as skeletal mesh; physics asset = ragdoll-lite (capsule per limb, not final combat capsule — gameplay capsule is separate, §7); materials = master material instances (SSS skin, aged bronze, woven indigo, tanned leather); LODs via Unreal auto-LOD + manual override for face loops; socket list per §5; scabbard/baldric as socket-attached static submeshes.
5. **Animation** — mocap-or-keyframe hybrid; retarget against UE skeleton only if project skeleton == UE Manny-family (owner ruling pending — else custom skeleton, retarget out); montage sign-off requires viewport capture in evidence pack.

### 10.2 Identity-lock pre-flight (run on every export before any review)
- scar LEFT cheekbone (viewer-right in front ortho) — never mirrored/flipped in any mirror operation; mirror must be "mirror object data only pre-asymmetry" step, then apply asymmetry passes AFTER base mirror.
- bronze coiled armlet LEFT upper arm — coil count/pitch per master ref panel (to be measured in modelling SOP); no fused medallion (V002-class defect — auto-reject in QC).
- spiral pendant on braided cord, sternum socket — FICTIONAL provenance tag stays in manifest.
- LEFT temple: 3 bronze cuffs + 2 coral beads — right temple stays clean.
- baldric: anatomical LEFT shoulder → RIGHT hip — verify in engine viewport, not just DCC.
- scabbard: absent until CQ-9 closes (socket may exist, mesh does not).
- no idemili / mask / plain-textile-only violations; no Igbo-emblem claims anywhere in tags/notes.

### 10.3 Deliverable manifest (DRAFT — file list production must produce)
| # | Deliverable | Format | Gate |
|---|---|---|---|
| D01 | `ADANNA_base_LOD0..3.fbx` | FBX | AD-02 + FP-07 |
| D02 | `ADANNA_SK_*` Unreal skeleton+asset | uasset | FP-07 #7 + AD-03 |
| D03 | `T_ADANNA_Body_BC/N/R_4K`, `T_ADANNA_Costume_2K`, `T_ADANNA_Bronze_*` | PNG/TGA/EXR | AD-03 |
| D04 | `ADANNA_physics.uasset` (ragdoll-lite) | uasset | AD-03 |
| D05 | `ADANNA_anim_*` non-combat set (14) | uasset | AD-04 (non-combat may proceed under waiver; label PROVISIONAL) |
| D06 | `ADANNA_anim_combat_*` (14–18) | uasset | AD-04 hard gate |
| D07 | `ADANNA_review_pack_v001` (renders + engine captures + QC checklist) | folder | internal review, then owner |
| D08 | `ADANNA_evidence.md` (this workbook + FP-07 + TD-SPEC-001 + QC logs) | md | every milestone |
| D09 | `budget_report.csv` (tri/texel/LOD per export) | csv | every D01/D03 export |

### 10.4 QC gates between stages (hard stops)
Modelling → QC-1 (topology checklist §3) → UV → QC-2 (texel density, seam map) → Texture → QC-3 (no flat albedos, palette conformance vs FP-01 swatches) → Rig → QC-4 (bind pose vs portrait, ≥18 FACS, ≤4 influences) → Anim → QC-5 (foot-slide ≤5 mm, montage captured) → Evidence pack → owner review → (promotion is owner-only, always).

### 10.5 What is deliberately NOT in this manifest
No canon claims, no promotion steps, no image regeneration, no weapon final forms (CQ-9), no idemili/mask/textile-restricted items. The package ends at owner review; shipping/release is not this workbook's call.

## 11. OWNER DECISIONS APPLIED — 2026-11-20 W1 D3 (supersedes conflicting lines above where noted)
- **AD-01 applied:** final blade/scabbard geometry DEFERRED. `Socket_Scabbard`, `Socket_Baldric`, `Socket_Weapon_R`-equivalents remain **socket placeholders only**; no scabbard/blade mesh, no CQ-9 geometry work. CQ-9 stays open and is explicitly **non-blocking** for all unrelated character production.
- **AD-02 in flight:** V003 vs V004 selection is **Our Eyes + Research exact-version assessment → CD delegated selection/correction**. This workbook's V004-measurements-consistent finding is evidence for that review, NOT an approval. No plate may enter model build before CD records the candidate selection.
- **AD-03 pipeline authority:** TD/CD may approve Blender→Unreal modelling/topology/texture/rig against the approved master ref + TD-SPEC-001 Addendum A baseline. No invented cultural details — full stop.
- **AD-04 animation scope:** PM defines the MINIMUM set from actual gameplay. Non-combat authoring may proceed as PROVISIONAL (labelled); combat set = PM-minimum only; no cinematic/facial expansion without explicit ruling.
- **Identity locks:** unchanged and binding (scar LEFT cheekbone; coiled armlet LEFT upper arm; spiral pendant FICTIONAL on braided cord; 3 bronze + 2 coral LEFT-temple; baldric anatomical LEFT→RIGHT). Armlet consultant restriction in force. Pendant stays FICTIONAL in manifest and materials.
- **Start-now list (per owner):** everything independent of AD-02/CQ-9 — §10 manifest (D01–D09), QC tooling, evidence pack, non-combat PROVISIONAL anims, greybox/engine integration hooks, LOD budget test scenes.
