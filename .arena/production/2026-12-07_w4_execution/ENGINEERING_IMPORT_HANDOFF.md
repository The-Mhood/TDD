# ENGINEERING HANDOFF - import settings (Design -> Engineering/TA, 2026-12-07)
Asset IDs covered: ADANNA_AD03_V5, GUARD_CLASS_V3, NPC_CIVILIAN_* (x6), CH01 Env Kit V2 modules, CH01_COMPOUND_ASSEMBLED_V2, CH01_POPULATED_{LOW_4,MEDIUM_6,HIGH_8}, PROP_* dressing split v1.1.
- Source files: exact paths in each package manifest (inventory: 2026-12-06_w3_execution/DESIGN_PRODUCTION_INVENTORY.json).
- Units/axes: metres, Z-up in OBJ/GLB as authored; Engineering to confirm Unreal import rotation/scale on first import and report back - Design has NOT verified in-engine.
- Skeleton: HUMAN_BASE_PROPOSED, 11 joints, names/order contractual (CHARACTER_ASSET_SPEC_V1.json). NPC youth = actor scale 0.85.
- Materials: shared names (env_kit_v2.mtl family; cloth_*/skin_*/leather_plain_v1). No PBR values beyond kit colours/texture set - TA to author.
- Acceptance status: production tier (source-validated) for all above; qualified tier = M1 FBX pair only; integrated = none claimed.
- Known limitations: populated assemblies are static bind-pose (use GLBs+clips for animated), dressing split v1.1 supersedes cluster for import (cluster kept as rollback), facial likeness is stylised tier pending owner decision.
- Receiving dept: Engineering (import) + TA (materials/rig). Required next action: confirm import transform + first-import report; pick populated density (PM).
