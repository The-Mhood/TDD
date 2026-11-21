#!/usr/bin/env python3
"""Dressing kit SPLIT v1.1 - same approved props as KIT_COURTYARD_DRESSING,
now one OBJ per prop with its own origin at ground centre (TD-ready).
Contents unchanged: no new object types."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","2026-11-23_w1d7_production","pipeline"))
from charbuild import Part, lathe, box, ellipsoid, write_obj
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
MATS={"clay_pot_v1":(0.42,0.25,0.16),"basket_woven_v1":(0.55,0.42,0.25),"wood_palm_v1":(0.35,0.24,0.15),"stone_hearth_v1":(0.32,0.30,0.28)}
def one(name, build):
    p=Part(name,"clay_pot_v1","pelvis"); build(p)
    nv,t=write_obj(os.path.join(OUT,name+".obj"),[p],MATS); return {"asset":name,"verts":nv,"tris":t,"origin":"ground centre of prop"}
res=[]
res.append(one("PROP_POT_LARGE", lambda p:(setattr(p,'mat','clay_pot_v1'), lathe(p,[(0.16,0.16,0.02),(0.23,0.23,0.18),(0.19,0.19,0.38),(0.13,0.13,0.44),(0.15,0.15,0.48)],20,cap_bot=True))))
res.append(one("PROP_POT_SMALL", lambda p:(setattr(p,'mat','clay_pot_v1'), lathe(p,[(0.11,0.11,0.02),(0.16,0.16,0.14),(0.10,0.10,0.28),(0.12,0.12,0.31)],18,cap_bot=True))))
res.append(one("PROP_BASKET_WOVEN", lambda p:(setattr(p,'mat','basket_woven_v1'), lathe(p,[(0.20,0.20,0.02),(0.26,0.26,0.16),(0.30,0.30,0.30)],18,cap_bot=True))))
# firewood: 3-log stack as one prop
def fw(p):
    p.mat='wood_palm_v1'
    for (x,y,z) in ((0,0,0.05),(0.02,0.13,0.05),(-0.01,0.06,0.14)): box(p,x,y,z,0.55,0.09,0.09)
res.append(one("PROP_FIREWOOD_STACK", fw))
def hs(p):
    p.mat='stone_hearth_v1'
    for (x,y) in ((0,0.16),(0.15,-0.06),(-0.15,-0.06)): ellipsoid(p,(x,y,0.06),(0.09,0.08,0.06),10,8)
res.append(one("PROP_HEARTH_STONES", hs))
man={"package":"CH01_DRESSING_SPLIT_V1.1","tier":"production assets - NOT qualified, NOT Unreal-integrated","supersedes_for_import":"KIT_COURTYARD_DRESSING cluster (kept as rollback)","props":res}
json.dump(man,open(os.path.join(OUT,"DRESSING_SPLIT_MANIFEST.json"),"w"),indent=2); print(json.dumps(man,indent=2))
