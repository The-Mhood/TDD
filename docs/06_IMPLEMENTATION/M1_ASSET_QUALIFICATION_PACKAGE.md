# M1 Asset Qualification Package — Design Deliverable

**Document ID:** TDD-IMPL-QUALPKG-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** Design Lead. **Status:** PROPOSED — qualification evidence to be recorded by the owner.
**Purpose:** Define the representative M1 assets, technical specs, expected results, and export requirements so Design can **qualify** an asset (examine it under representative conditions and record evidence) — a **different process from build acceptance** (which is the Takeover Lead's batch gate). Qualification is Design's visual review/acceptance of the asset's readiness for production.
**Rule:** No exploratory asset is promoted to approved production status without required sign-offs (QUALITY §7).

---

## 1. Representative assets

The qualification package targets the **representative production targets** identified by the PM:

| Asset | Role | Representative because |
|---|---|---|
| **Adanna character (full body + face)** | Hero protagonist | The primary production asset; the facial-likeness benchmark |
| **Guard NPC** | Secondary character | Secondary skeleton-reuse test; confirms the shared `HUMAN_BASE_PROPOSED` pipeline scales |
| **One environment zone greybox** | Location | Confirms the built-content path (Prop Package / Mushroom Cloud / LOD / nav-gen) |
| **One interaction volume + marker** | Interaction | Confirms the interaction-volume path |
| **Facial rig + expression turntable (Adanna)** | Facial likeness | The PoC face — the zero-budget facial likeness benchmark |

> Enemy assets are **not** qualified here: no enemy is ratified (CD-3 not ratified) and CD-2 cultural holds are open. Qualification of an enemy asset requires its CD-3 ratification + CD-2 clearance first.

## 2. Technical specifications

### Character technical spec (from `M1_ADANNA_CHARACTER_ART_ANIMATION_SPEC.md` + `W1D7_CHARACTER_INTEGRATION_MANIFEST.md`)
- **Geometry:** Adanna V3 = 13,680 tris / 7,028 verts; Guard V2 = 10,752 tris / 5,556 verts.
- **Skeleton:** `HUMAN_BASE_PROPOSED` 11-joint skeleton (pelvis→spine→head; upperarm/forearm.L/R; thigh/shin.L/R). Identical bone names across Adanna V3 and Guard V2 → shared retarget animation set.
- **Material slots (Adanna V3):** `skin_base_v1`, `skin_base_rough_v1`, `skin_repaired_v1`, `cloth_indigo_plain_v1`, `cloth_indigo_print_v1`, `leather_strap_deep_v1`, `leather_strap_print_v1`, `metal_hardware_v1`, `metal_aged_v1`, `hair_dark_v1` (10 slots). Guard V2 = 6 slots.
- **Face:** identity locks per the Adanna spec — deep brown skin; thin braids with top half in high knot; **three bronze cuffs + two coral beads at the LEFT temple**; **diagonal scar on the LEFT cheekbone**; coiled aged-bronze armlet on the LEFT upper arm; spiral bronze pendant (FICTIONAL); guarded/defiant default; **no gold; never mirrored.** Material slots include `lips_v1`, `eye_dark_v1`, `scar_marker_v1`.

### Environment technical spec
- **Scale:** 300-unit tile; greybox 900×900 m; bounded on all sides; **no open world**.
- **Built-content path:** Prop Package + Mushroom Cloud; LOD and HLOD; **do not flatten tri-count into texture memory.**
- **Coordinate axes:** Z-up semantics for Blender/UE; world origin co-located with the map grid origin (`Axis & Scale` evidence).
- **Collision:** capsule-based; poly/volume collision for blocking; no baked mesh physics.
- **Nav mesh:** generated in-engine (M1 spec §7).

## 3. Expected results (acceptance intent)

| Check | Expected result |
|---|---|
| **Scale/orientation** | Asset imports at scale 1.0, correct axes; metres = centimetres; origin co-located with map grid |
| **Topology/weights** | Animation topology; skin-weight sums per joint = 1.0 ±1%; no degenerate vertices |
| **UV/materials** | Clean UVs; correct PBR textures on the right material slots; no missing textures |
| **Material/texture fidelity** | Skin/eye/hair/scar read as the approved identity at gameplay camera distance |
| **Export compatibility** | Binary FBX 7.400 (characters); collada/GLB (content); metric units; parses cleanly |
| **UE import readiness** | Loads in UE 5.8.4 (owner Mac) with no errors; skeleton binds to the correct class |
| **Collision/LOD** | Character capsule collision present; mesh LODs set; nav-gen passes |
| **Animation** | Retarget to shared skeleton works; expression turntable/idle plays |
| **Facial identity** | Facial features match the approved master portrait; left-side locks preserved; no mirroring |

## 4. Export requirements

- **Characters:** Binary **FBX 7.400**, metric units, **scale 1.0**; embedded skeleton `HUMAN_BASE_PROPOSED`; reference the integration spec for naming.
- **Content:** Collada/GLB with textures alongside (W1D7 verification path).
- **Facial rig:** Blender FBX with the facial rig; expression controls documented; exported alongside the character.
- **Evidence bundle per asset:** geometry/tri/material-slot/joint-influence/deform-recheck JSON + **text hashes** + exported FBX + export script + exit code — archived per character (E-5 archive convention).

## 5. Owner verification requirements

**Owner-Mac execution must verify, and record evidence for:**
1. **File integrity** — checksums match; archive complete.
2. **Scale & orientation** — metres; correct axes; origin placement.
3. **Geometry** — tris/verts within budget; topology valid; no degenerate geometry.
4. **Materials & textures** — correct slots, no missing textures, PBR resolved.
5. **Export compatibility** — FBX parses; UE import succeeds with no errors.
6. **UE import readiness** — asset loads; skeleton binds; collision/LOD present.

**Qualification evidence** is recorded in the qualification ledger (asset name, checks passed, date, owner, evidence bundle path, **qualification status** = QUALIFIED / FAILED / NOT QUALIFIED). **Owner signature** confirms visual review/acceptance (Design owns visual acceptance; Engineering owns technical integration).

## 6. Sign-off

- **Technical Art:** topology, UV, material, export spec.
- **Character Art:** sculpt, texture, rig visual fidelity.
- **Design Lead:** visual review/acceptance (owner-side).
- **Engineering:** UE import/integration technical acceptance.

**No asset is QUALIFIED and promoted to approved production without these sign-offs.**
