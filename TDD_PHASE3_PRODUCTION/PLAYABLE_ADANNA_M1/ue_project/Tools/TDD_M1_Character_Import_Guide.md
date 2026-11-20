# TDD M1 — Character FBX Import Guide (UE 5.8.4)

## Assets Ready for Import

Design closed the sculpt milestone-1 visual gate at commit `2a4a88e`. The approved **V3/V2**
character FBX files are validated and ready for UE 5.8.4 import. V2/V1 qualified builds remain as
rollback fallbacks.

| Character | FBX Path | Height | Tris | Skeleton |
|---|---|---|---|---|
| **Adanna AD-03 V3** (primary) | `.arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V3/ADANNA_AD03_V3.fbx` | 1.837 m | 13,680 | HUMAN_BASE_PROPOSED (11 joints) |
| **Guard Class V2** (primary) | `.arena/production/2026-11-24_w1d7_blender_package/output/GUARD_CLASS_V2/GUARD_CLASS_V2.fbx` | 1.772 m | 10,752 | HUMAN_BASE_PROPOSED (11 joints) |
| Adanna AD-03 V2 (fallback) | `.arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V2/ADANNA_AD03_V2.fbx` | 1.837 m | 8,660 | HUMAN_BASE_PROPOSED (11 joints) |
| Guard Class V1 (fallback) | `.arena/production/2026-11-24_w1d7_blender_package/output/GUARD_CLASS_V1/GUARD_CLASS_V1.fbx` | 1.771 m | 6,296 | HUMAN_BASE_PROPOSED (11 joints) |

## Import Procedure

### 1. Create Skeleton Asset (once)
Import **either** FBX first. In the UE Content Browser:
- Right-click the imported Skeletal Mesh → **Create Skeleton** → name it `HUMAN_BASE_PROPOSED`
- This Skeleton will be shared by both characters.

### 2. Import Adanna AD-03 V3
- Content Browser → **Import** → select `ADANNA_AD03_V3.fbx`
- **Import Options:**
  - Scale: 1.0 (FBX already exported with metres→cm conversion)
  - Import Animations: No (no animations in this package)
  - Import Materials: Yes
  - Import Textures: Yes (see texture note below)
  - Skeletal Mesh: Yes (assign `HUMAN_BASE_PROPOSED` skeleton)
  - Normals: Calculate
  - Tangents: Calculate
- Place at: `Content/Characters/ADANNA_AD03_V3/`

### 3. Import Guard Class V2
- Content Browser → **Import** → select `GUARD_CLASS_V2.fbx`
- **Import Options:** same as above, assign the same `HUMAN_BASE_PROPOSED` skeleton
- Place at: `Content/Characters/GUARD_CLASS_V2/`

### 4. Verify Skeleton Compatibility
- Open both Skeletal Meshes in the Skeletal Mesh Editor
- Verify bone names match: `pelvis`, `spine`, `head`, `upperarm.L`, `forearm.L`, `upperarm.R`, `forearm.R`, `thigh.L`, `shin.L`, `thigh.R`, `shin.R`
- Both should reference the same `HUMAN_BASE_PROPOSED` Skeleton asset
- (Verified identical via independent Blender FBX import in the sandbox.)

### 5. Animation Retargeting Test
- Import a test animation clip (or create a simple idle pose)
- Use UE's **Retarget Manager** to retarget from Adanna to Guard
- No bone mapping should be needed — identical skeleton

### 6. Capsule Collision
- Adanna: Capsule r=0.32 m, h=1.80 m (pending TD ruling)
- Guard: Capsule r=0.30 m, h=1.77 m (pending TD ruling)

## Texture Note

The FBX files carry material definitions and material-slot assignments but **do not embed the
image textures** (verified). Textures are packed inside the source `.blend` (Adanna V3: 4 PNGs,
Guard V2: 3 PNGs). To supply textures in UE:
- Extract from the `.blend` (Blender: File → External Data → Unpack), or
- Re-import from the GLB (UE5 supports glTF/GLB) to carry textures, or
- Point the UE material texture parameters at the extracted/source images.
This is identical to the qualified V2/V1 builds — not a regression.

## Rollback

If V3/V2 integration hits a UE blocker, swap to the V2/V1 FBX files. Same skeleton, bone names,
scale, and import configuration — drop-in replacement, no import-setting changes.

## Integration Architecture Notes

- The `HUMAN_BASE_PROPOSED` skeleton and 11 joint names are **frozen** as the shared standard
  (confirmed identical across V1/V2/V3 and V1/V2 character generations).
- Future mesh upgrades (e.g. sculpt milestone 2) will replace mesh data only — no skeleton,
  bone-name, or scale changes required.
- All assets are in metres, METRIC, scale 1.0.
