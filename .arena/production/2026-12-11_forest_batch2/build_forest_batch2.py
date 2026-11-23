#!/usr/bin/env python3
"""FORBIDDEN FOREST BATCH 2 - environment + world-object modules from
established CH01 forest boards (THRESHOLD_PATH, ROOT_WAY, STREAM_CROSSING,
ROOT_MOTHER_ARENA - REVIEW REQUIRED boards, kit PROVISIONAL not canon).
Gameplay-aware specs in manifest (traversal widths, collision)."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","2026-11-23_w1d7_production","pipeline"))
from charbuild import Part, lathe, ellipsoid, box, limb, write_obj
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
MATS={"bark_v1":(0.30,0.22,0.16),"rock_dark_v1":(0.23,0.23,0.22),"canopy_v1":(0.16,0.30,0.14),"undergrowth_v1":(0.20,0.34,0.16),
      "wood_palm_v1":(0.35,0.24,0.15),"ground_forest_v1":(0.32,0.24,0.16),"path_earth_v1":(0.42,0.32,0.20),"water_dark_v1":(0.10,0.16,0.18)}
def P(n,m): return Part(n,m,"pelvis")
res=[]
def save(name,parts,spec):
    nv,t=write_obj(os.path.join(OUT,name+".obj"),parts,MATS); res.append({"asset":name,"verts":nv,"tris":t,"spec":spec})
# boundary posts (threshold): pair of tall posts flanking 2.2m path gap
ps=[]
for x in (-1.3,1.3):
    p=P("post","wood_palm_v1"); box(p,x,0,1.1,0.16,0.16,2.2); ps.append(p)
save("FOREST_BOUNDARY_POSTS",ps,"path gap 2.2 m between posts; collision cylinders r0.1; marks forest threshold (board: posts on ridge)")
# stepping stones across 3.4m stream bed + dark water plane
parts=[P("water","water_dark_v1")]; box(parts[0],0,0,-0.06,4.6,3.0,0.08)
for i,(x,y) in enumerate(((-1.5,-0.5),(-0.75,0.25),(0.0,-0.3),(0.75,0.3),(1.5,-0.2))):
    s=P(f"stone_{i}","rock_dark_v1"); ellipsoid(s,(x,y,0.05),(0.34,0.28,0.12),10,8); parts.append(s)
save("FOREST_STREAM_CROSSING",parts,"stones top z~0.15, spacing 0.75 m (steppable); water plane visual only, no collision")
# log bridge: horizontal trunk over 4m gap
lg=P("log","bark_v1"); limb(lg,(-2.2,0,0.9),(2.2,0,0.9),0.22,0.22,12)
r1=P("root_l","bark_v1"); limb(r1,(-2.2,0,0.0),(-2.2,0,0.9),0.16,0.18,8)
r2=P("root_r","bark_v1"); limb(r2,(2.2,0,0.0),(2.2,0,0.9),0.16,0.18,8)
save("FOREST_LOG_BRIDGE",[lg,r1,r2],"walk surface z0.9 width ~0.44; collision capsule along log; gap span 4.4 m")
# liana set: 3 hanging segmented vines
parts=[]
for k,(x,z0) in enumerate(((-0.8,3.2),(0.1,2.6),(0.9,3.5))):
    v=P(f"liana_{k}","canopy_v1"); limb(v,(x,0,z0),(x+0.15,0.05,0.6),0.035,0.025,8); parts.append(v)
save("FOREST_LIANA_SET",parts,"visual dressing, no collision; hang from canopy anchor z2.6-3.5")
# undergrowth set: low leafy masses
parts=[]
for i,(x,y,s) in enumerate(((-1.2,0.6,1.0),(0.2,-0.8,1.3),(1.3,0.5,0.8),(-0.4,1.2,0.7))):
    u=P(f"under_{i}","undergrowth_v1"); ellipsoid(u,(x,y,0.35*s),(0.6*s,0.5*s,0.35*s),10,8); parts.append(u)
save("FOREST_UNDERGROWTH_SET",parts,"foliage dressing, no collision; keep 1.6 m path corridor clear on placement")
# arena root wall segment: curved row of root pillars (Great Root Mother arena boundary)
parts=[]
for i in range(5):
    a=math.radians(-40+i*20); x=math.sin(a)*4.2; y=-math.cos(a)*4.2+4.2
    rp=P(f"root_pillar_{i}","bark_v1"); limb(rp,(x,y,0.0),(x*0.92,y+0.35,3.0),0.34,0.26,10); parts.append(rp)
save("ROOTMOTHER_ROOT_WALL_SEG",parts,"arena boundary segment r~4.2 m arc; collision cylinders r0.34 per pillar; tile segments to enclose arena")
man={"package":"FORBIDDEN_FOREST_BATCH2_ENV_WORLDOBJECTS","status":"PROVISIONAL production (source boards REVIEW REQUIRED)","modules":res,
 "chapter":"CH01 Forbidden Forest","naming":"FOREST_<MODULE> / ROOTMOTHER_<MODULE>, metres Z-up, ground-centre pivots",
 "performance":"all modules <1k tris; foliage/rocks share 3 materials for batching"}
json.dump(man,open(os.path.join(OUT,"FOREST_BATCH2_MANIFEST.json"),"w"),indent=2); print(json.dumps(man,indent=2))
