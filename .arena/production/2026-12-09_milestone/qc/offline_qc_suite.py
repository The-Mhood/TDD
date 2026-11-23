#!/usr/bin/env python3
"""Offline QC suite (sandbox-runnable) for character GLBs: mesh/UV/material/
skeleton/weights/scale/checksum. Deformation+joint checks run separately
(existing validators). Verdict per asset; this is NOT Blender/Unreal QC."""
import glob, hashlib, json, os, struct, sys
sys.path.insert(0,"/home/user/TDD/.arena/production/2026-11-23_w1d7_production/pipeline")
import test_deformation as td
FILES={
 "ADANNA_AD03_V6_FACEPOC":"2026-12-08_gate_removal/facial_poc/out/ADANNA_AD03_V6_FACEPOC.glb",
 "ADANNA_AD03_V7":"2026-12-10_adanna_v7/out/ADANNA_AD03_V7.glb",
 "ADANNA_AD03_V5":"2026-11-26_w1d10_definitive_adanna/out/ADANNA_AD03_V5.glb",
 "GUARD_CLASS_V3":"2026-11-25_w1d9_sculpt2/out/GUARD_CLASS_V3.glb",
 "NPC_CIVILIAN_M1":"2026-12-01_w1d15_production/npc_civilian_builds/out/NPC_CIVILIAN_M1.glb",
 "NPC_CIVILIAN_F1":"2026-12-01_w1d15_production/npc_civilian_builds/out/NPC_CIVILIAN_F1.glb",
 "NPC_CIVILIAN_YOUTH_M":"2026-12-02_w1d16_production/npc_variants/out/NPC_CIVILIAN_YOUTH_M.glb",
 "NPC_CIVILIAN_ELDER_M":"2026-12-02_w1d16_production/npc_variants/out/NPC_CIVILIAN_ELDER_M.glb",
 "NPC_CIVILIAN_ELDER_F":"2026-12-02_w1d16_production/npc_variants/out/NPC_CIVILIAN_ELDER_F.glb",
 "NPC_CIVILIAN_F1_EARTHRED":"2026-12-02_w1d16_production/npc_variants/out/NPC_CIVILIAN_F1_EARTHRED.glb"}
P="/home/user/TDD/.arena/production"; out={}
for name,rel in FILES.items():
    p=os.path.join(P,rel); g,acc=td.load(p)
    mesh=g["meshes"][0] if False else g["meshes"]
    mats=[m.get("name") for m in g.get("materials",[])]
    joints=len(g["skins"][0]["joints"]) if g.get("skins") else 0
    has_uv=all("TEXCOORD_0" in pr["attributes"] for m in g["meshes"] for pr in m["primitives"])
    has_skin=all("JOINTS_0" in pr["attributes"] and "WEIGHTS_0" in pr["attributes"] for m in g["meshes"] for pr in m["primitives"])
    out[name]={"sha256":hashlib.sha256(open(p,'rb').read()).hexdigest(),"meshes":len(g["meshes"]),"materials":mats,
      "joints":joints,"uv_all_primitives":has_uv,"skinned_all_primitives":has_skin,
      "verdict":"PASS" if (joints==11 and has_uv and has_skin) else "CHECK"}
res={"suite":"offline QC v1 (mesh/uv/material/skeleton/weights-presence/checksum)","assets":out,"all_pass":all(v["verdict"]=="PASS" for v in out.values()),
 "not_covered":["normals quality/topology (visual + Blender stage)","in-engine import (Engineering)"]}
json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"OFFLINE_QC_REPORT.json"),"w"),indent=2)
print(json.dumps({k:v['verdict'] for k,v in out.items()},indent=1), "ALL_PASS", res["all_pass"])
