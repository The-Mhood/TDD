#!/usr/bin/env python3
"""Civilian NPC animation V1: derive civilian idle/walk from the VALIDATED
Adanna movement clips (same skeleton/convention) at reduced amplitude
(0.65x walk, idle unchanged, no arm raise) - no new motion invented.
Validate idle keyframes + all civilian keys across all SIX NPC assets."""
import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__)); PROD=os.path.abspath(os.path.join(HERE,"..",".."))
sys.path.insert(0, os.path.join(PROD,"2026-11-23_w1d7_production","pipeline"))
import test_deformation as td
src=json.load(open(os.path.join(PROD,"2026-11-29_w1d13_production","adanna_animation","ADANNA_MOVEMENT_CLIPS_V1.json")))["clips"]
def scaled(clip,f):
    return {"loop":True,"fps":30,"keys":[{"t":k["t"],"pose":{j:[v[0],round(v[1]*f,4)] for j,v in k["pose"].items()}} for k in clip["keys"]]}
out={"skeleton":"HUMAN_BASE_PROPOSED (11 joints)","convention":"joint->[axis, angle_rad], as pipeline/test_deformation.py",
 "derivation":"idle = validated Adanna idle unchanged; walk = validated walk at 0.65 amplitude (civilian amble); no new poses invented",
 "clips":{"civilian_idle":scaled(src["idle"],1.0),"civilian_walk":scaled(src["walk"],0.65)}}
json.dump(out,open(os.path.join(HERE,"CIVILIAN_CLIPS_V1.json"),"w"),indent=2)
NPCS=[os.path.join(PROD,"2026-12-01_w1d15_production","npc_civilian_builds","out",n+".glb") for n in ("NPC_CIVILIAN_M1","NPC_CIVILIAN_F1")]
NPCS+=[os.path.join(PROD,"2026-12-02_w1d16_production","npc_variants","out",n+".glb") for n in ("NPC_CIVILIAN_YOUTH_M","NPC_CIVILIAN_ELDER_M","NPC_CIVILIAN_ELDER_F","NPC_CIVILIAN_F1_EARTHRED")]
poses={}
for cn,clip in out["clips"].items():
    for i,k in enumerate(clip["keys"]): poses[f"{cn}_{i}"]={j:(v[0],v[1]) for j,v in k["pose"].items()}
td.POSES=poses; results={}; ok=True
for g in NPCS:
    rc=td.run(os.path.abspath(g)); results[os.path.basename(g)]="PASS" if rc==0 else "FAIL"; ok&=rc==0
res={"assets":results,"keyframe_poses_tested_per_asset":len(poses),"clips":list(out["clips"]),"verdict":"PASS" if ok else "FAIL",
     "tier":"source-level validation only - NOT Blender qualification, NOT Unreal animation integration"}
json.dump(res,open(os.path.join(HERE,"CIVILIAN_CLIPS_V1_VALIDATION.json"),"w"),indent=2); print(json.dumps(res,indent=2))
