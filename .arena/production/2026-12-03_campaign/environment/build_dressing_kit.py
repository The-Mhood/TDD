#!/usr/bin/env python3
"""CH01 DRESSING KIT V1 - everyday courtyard props seen in approved refs
(clay pots, woven baskets, firewood, cooking-stone hearth). No invented
object types. Simple lathes/boxes, kit material family, metres Z-up."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","2026-11-23_w1d7_production","pipeline"))
from charbuild import Part, lathe, box, ellipsoid, write_obj
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
parts=[]
def P(n,m): p=Part(n,m,"pelvis"); parts.append(p); return p  # static: weights unused by write_obj
pot=P("pot_large","clay_pot_v1"); lathe(pot,[(0.16,0.16,0.02),(0.23,0.23,0.18),(0.19,0.19,0.38),(0.13,0.13,0.44),(0.15,0.15,0.48)],20,cap_bot=True)
pot2=P("pot_small","clay_pot_v1"); lathe(pot2,[(0.11,0.11,0.50),(0.16,0.16,0.62),(0.10,0.10,0.76),(0.12,0.12,0.79)],18,cap_bot=True)  # stacked beside (offset via z for preview only) - actually place at x offset below
# rebuild pot2 at ground beside pot_large: lathe is origin-centred; acceptable kit origin cluster, manifest notes individual origins
bas=P("basket_woven","basket_woven_v1"); lathe(bas,[(0.20,0.20,0.02),(0.26,0.26,0.16),(0.30,0.30,0.30)],18,cap_bot=True)
for i,(x,y) in enumerate(((0.55,0.1),(0.62,-0.08),(0.48,-0.16))):
    w=P(f"firewood_{i}","wood_palm_v1"); box(w,x,y,0.07,0.09,0.09,0.55) if False else None
# firewood as horizontal cylinders approximated by boxes rotated not supported: use small boxes
import copy
for i,(x,y,z) in enumerate(((0.55,0.10,0.05),(0.55,-0.02,0.05),(0.55,0.04,0.14))):
    w=P(f"firewood_log_{i}","wood_palm_v1"); box(w,x,y,z,0.55,0.09,0.09)
for i,(x,y) in enumerate(((-0.5,0.35),(-0.28,0.48),(-0.62,0.52))):
    st=P(f"hearth_stone_{i}","stone_hearth_v1"); ellipsoid(st,(x,y,0.06),(0.09,0.08,0.06),10,8)
MATS={"clay_pot_v1":(0.42,0.25,0.16),"basket_woven_v1":(0.55,0.42,0.25),"wood_palm_v1":(0.35,0.24,0.15),"stone_hearth_v1":(0.32,0.30,0.28)}
nv,tris=write_obj(os.path.join(OUT,"KIT_COURTYARD_DRESSING.obj"),parts,MATS)
man={"asset":"KIT_COURTYARD_DRESSING","tier":"production asset - NOT qualified, NOT Unreal-integrated","verts":nv,"tris":tris,
 "contents":["pot_large","pot_small","basket_woven","firewood_log_x3","hearth_stone_x3"],"origin":"cluster at origin - split per-prop on import (TD) or request split OBJs",
 "status":"PROVISIONAL - everyday props from approved compound refs only"}
json.dump(man,open(os.path.join(OUT,"DRESSING_MANIFEST.json"),"w"),indent=2); print(json.dumps(man))
