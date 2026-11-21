# RECONCILIATION of reported achievements vs files (2026-12-06)
| Claim | File evidence | True classification |
|---|---|---|
| Batches A/B 6/6 boards accepted | ST02_DAY, CIVILIAN_ANIMATION_REFERENCE_V1, POPULATED_COMPOUND_COMPOSITION_REFERENCE_V1, UI_MENU_LAYOUT_REFERENCE_V1 + campaign boards | **Concept/reference images** - approved design references; NOT environments, NOT animations, NOT integrated |
| 3 rejected attempts retained | `_rejected/` attempt1-3 with reasons in BATCH_A_LOG | Rejected candidates, correctly excluded from accepted counts |
| CH01 dawn/dusk/night keys | ST01_DAWN/ST03_DUSK/ST04_NIGHT.jpg | **Lighting reference images** (provisional); the environment itself is the OBJ assembly below |
| CH01 V2 compound 1,058 tris | CH01_COMPOUND_ASSEMBLED_V2.obj + manifest | **Produced 3D asset (OBJ)** - production tier; NOT Blender-qualified as an assembly, NOT Unreal-integrated; not canon |
| Six Adanna movement clips | ADANNA_MOVEMENT_CLIPS_V1.json (idle/walk/run/dodge/crouch/look-back) | **Animation data (JSON keyframes)** - source-validated; NOT Blender/Unreal animation assets until retarget/integration |
| Deformation 46/46 PASS | ADANNA_MOVEMENT_CLIPS_V1_VALIDATION.json via test_deformation.py | **Source-level skinning validation** on 2 GLBs; NOT engine verification |
| (Also) Guard clips 36/36, civilian 48/48 | respective VALIDATION.json | Same source-level tier |
| Qualified assets | blender package output/ (M1 Adanna V3 + Guard V2 FBX) | **Technically qualified** - the only qualified tier; NOT confirmed Unreal-integrated by Design |
| Integrated Unreal assets | none verifiable from Design repo | **0 claimed** - integration status belongs to PM/Engineering |
