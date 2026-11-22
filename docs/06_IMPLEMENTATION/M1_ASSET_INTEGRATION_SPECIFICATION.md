# M1 Asset Integration Specification — PM / Technical Direction

**Document ID:** TDD-IMPL-INTSPEC-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM + Technical Direction, jointly.
**Purpose:** The binding integration specification for importing M1 assets into Unreal Engine 5.8.4. **Engineering owns technical integration; Design owns visual review/acceptance.** This spec is what the owner-Mac verification loop checks against.

---

## 1. Destination folders & asset types

| Asset | Destination path | Type |
|---|---|---|
| Adanna production character | `/Game/TDD/Characters/Adanna/` | Skeletal Mesh + Anim Blueprint + Material + Textures |
| Guard NPC character | `/Game/TDD/Characters/NPCs/Guard/` | Skeletal Mesh + Anim Blueprint + Material + Textures |
| Character skeleton | `/Game/TDD/Characters/Common/Skeleton_HUMAN_BASE_PROPOSED` | Skeleton (shared) |
| Character animations | `/Game/TDD/Animations/` | Animation + Anim Sequences |
| Environment kit | `/Game/TDD/Environment/M1_Environment_Kit_V1/` | Static Mesh + Materials + Textures |
| Props (unique) | `/Game/TDD/Props/` | Static Mesh + Materials |
| Interaction volumes | `/Game/TDD/Interaction/` | Actor + Blueprint |
| Markers / anchors | `/Game/TDD/Markers/` | Actor |

## 2. Naming conventions

- **Consistent with the existing project:** `BP_Adanna_*`, `BP_Guard_*`, `M1_Environment_Kit_V1_*`, `SkeletalMesh`/`Skeleton` prefixed, `AnimBP` suffix for animation blueprints.
- **Textures:** `TDD_<Asset>_<Slot>_` prefix, matching the material-slot names in the asset spec (`skin_base_v1`, `eye_dark_v1`, `lips_v1`, …).
- **Materials:** `M_<Asset>_<Slot>` to mirror the slot system.
- **No** collision-language placeholders, no per-asset ad-hoc names. **Purpose:** predictable import + script-verification.

## 3. Import settings

### Characters (FBX → Skeletal Mesh)
- **FBX import:** source FBX 7.400, binary, metric, **scale 1.0**.
- **Skeleton:** imported against the shared `Skeleton_HUMAN_BASE_PROPOSED`; bone names must match exactly (`pelvis`, `spine`, `head`, `upperarm.L/R`, `forearm.L/R`, `thigh.L/R`, `shin.L/R`).
- **Animation:** retarget to the shared skeleton; animation retargeting set reused.
- **Collision:** capsule-based collision profile; blocking poly/volume as specified.
- **Textures:** exported alongside; import into the matching material slots.
- **Texture compression:** default (BCn); no obvious-quality degradation (PBR-equivalent).

### Content (environment / props)
- **Source:** Collada/GLB.
- **Textures:** alongside; import with the standard texture pipeline.
- **Collision:** generated/declared as specified; no baked mesh physics.
- **LOD:** set per the environment tech spec (do not flatten tri-count into texture memory).

### Interaction volumes / markers
- Actor Blueprints; collision/volume set per the M1 interaction design; nav-generated.

## 4. Material requirements

- **PBR materials** on the existing material-slot system — **do not invent a parallel material system.** Reuse `skin_base_v1` etc.
- **Skin:** base color, normal, roughness, subsurface (per the identity spec).
- **Materials must resolve on import** (no missing textures). The owner-Mac verification checks for missing-texture errors.
- **Facial material slots** (`lips_v1`, `eye_dark_v1`, `scar_marker_v1`) must be present and populated.

## 5. Collision & LOD (where applicable)

| Asset | Collision | LOD |
|---|---|---|
| Characters | Capsule collision profile | Mesh LODs set (tri budget per spec) |
| Environment kit | Poly/volume blocking | HLOD + mesh LODs |
| Props | Blocking (as specified) | LODs as needed |
| Interaction volumes | Volume collision | n/a |

## 6. Integration validation & acceptance tests

**Engineering owns technical integration; Design owns visual review/acceptance.** Validation is a two-sided process:

**Technical (Engineering — run on owner Mac):**
- Import succeeds with no errors; skeleton binds to the correct class.
- Scale/orientation correct (metres, Z-up, origin co-located).
- Collision present; LODs present; nav-gen passes.
- Texture/material resolution: no missing textures.

**Visual (Design — owner signs off):**
- Character reads as the approved identity (facial locks, materials) at gameplay camera distance.
- Environment/props read as intended; interaction marker visible.

**Acceptance tests (must pass before the asset is production-approved):**
1. Import test — clean load, correct binding.
2. Scale/orientation test — metres + axes + origin.
3. Geometry test — tris within budget; topology valid.
4. Material/texture test — all slots resolved, PBR correct.
5. Collision/LOD test — collision + LOD present.
6. Animation/facial test — retarget + expression turntable plays.
7. Integration smoke — asset spawns in the M1 greybox map and renders.

**Evidence:** the owner-Mac verification bundle (with the checks above recorded) is the integration-acceptance evidence. **No asset is production-approved without the technical acceptance (Engineering) and the visual acceptance (Design/owner) both passing.**
