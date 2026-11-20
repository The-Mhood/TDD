# TDD M1 — Character FBX Import Guide (UE 5.8.4)

## Assets Ready for Import

Both character FBX files are validated and ready for UE 5.8.4 import:

| Character | FBX Path | Height | Skeleton |
|---|---|---|---|
| Adanna AD-03 V2 | `.arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` | 1.837 m | HUMAN_BASE_PROPOSED (11 joints) |
| Guard Class V1 | `.arena/production/2026-11-24_w1d7_blender_package/output/GUARD_CLASS_V1/GUARD_CLASS_V1.fbx` | 1.771 m | HUMAN_BASE_PROPOSED (11 joints) |

## Import Procedure

### 1. Create Skeleton Asset (once)
Import **either** FBX first. In the UE Content Browser:
- Right-click the imported Skeletal Mesh → **Create Skeleton** → name it `HUMAN_BASE_PROPOSED`
- This Skeleton will be shared by both characters.

### 2. Import Adanna AD-03 V2
- Content Browser → **Import** → select `ADANNA_AD03_V2.fbx`
- **Import Options:**
  - Scale: 1.0 (FBX already exported with metres→cm conversion)
  - Import Animations: No (no animations in this package)
  - Import Materials: Yes
  - Import Textures: Yes
  - Skeletal Mesh: Yes (assign `HUMAN_BASE_PROPOSED` skeleton)
  - Normals: Calculate
  - Tangents: Calculate
- Place at: `Content/Characters/ADANNA_AD03_V2/`

### 3. Import Guard Class V1
- Content Browser → **Import** → select `GUARD_CLASS_V1.fbx`
- **Import Options:** same as above, assign the same `HUMAN_BASE_PROPOSED` skeleton
- Place at: `Content/Characters/GUARD_CLASS_V1/`

### 4. Verify Skeleton Compatibility
- Open both Skeletal Meshes in the Skeletal Mesh Editor
- Verify bone names match: `pelvis`, `spine`, `head`, `upperarm.L`, `forearm.L`, `upperarm.R`, `forearm.R`, `thigh.L`, `shin.L`, `thigh.R`, `shin.R`
- Both should reference the same `HUMAN_BASE_PROPOSED` Skeleton asset

### 5. Animation Retargeting Test
- Import a test animation clip (or create a simple idle pose)
- Use UE's **Retarget Manager** to retarget from Adanna to Guard
- No bone mapping should be needed — identical skeleton

### 6. Capsule Collision
- Adanna: Capsule r=0.32 m, h=1.80 m (pending TD ruling)
- Guard: Capsule r=0.30 m, h=1.77 m (pending TD ruling)

## Integration Architecture Notes

- The `HUMAN_BASE_PROPOSED` skeleton and 11 joint names are **frozen** as the shared standard.
- Future mesh upgrades (Adanna V3, Guard V2) will replace mesh data only — no skeleton, bone-name, or scale changes required.
- All assets are in metres, METRIC, scale 1.0.
