#!/usr/bin/env python3
"""FORBIDDEN FOREST KIT V1 - production modules from established CH01 forest
boards (ESTABLISHING/ROOT_WAY/NIGHT_PATH/ROOT_MOTHER_ARENA, REVIEW REQUIRED
boards - kit is PROVISIONAL, not canon). Modules: buttress tree, root arch,
rock set, ground path tile, white-cloth route marker. Metres Z-up, origin at
ground centre, collision = trunk/rock bounds (manifest)."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","2026-11-23_w1d7_production","pipeline"))
from charbuild import Part, lathe, ellipsoid, box, limb, write_obj
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
MATS={"bark_v1":(0.30,0.22,0.16),"canopy_v1":(0.16,0.30,0.14),"rock_dark_v1":(0.23,0.23,0.22),"ground_forest_v1":(0.32,0.24,0.16),"path_earth_v1":(0.42,0.32,0.20),"cloth_white_v1":(0.88,0.86,0.80),"wood_palm_v1":(0.35,0.24,0.15)}
def P(n,m): return Part(n,m,"pelvis")
res=[]
def save(name,parts):
    nv,t=write_obj(os.path.join(OUT,name+".obj"),parts,MATS); res.append({"asset":name,"verts":nv,"tris":t}); return name
# buttress tree: trunk lathe + 5 buttress fins (tapered boxes rotated) + canopy blobs
tr=P("tree","bark_v1"); lathe(tr,[(0.85,0.85,0.0),(0.78,0.78,1.2),(0.62,0.62,3.0),(0.55,0.55,5.0),(0.58,0.58,7.0)],14,cap_bot=True)
parts=[tr]
for i in range(5):
    a=i/5*math.pi*2; f=P(f"buttress_{i}","bark_v1")
    box(f, math.cos(a)*0.95, math.sin(a)*0.95, 1.0, 0.18, 1.6, 2.0)  # axis-aligned fin approximation; rotated placement noted for TA
    parts.append(f)
for (x,y,z,r) in ((0,0,8.2,2.6),(1.4,0.6,7.4,1.9),(-1.3,-0.5,7.6,1.8),(0.4,-1.2,7.8,1.6)):
    c=P("canopy","canopy_v1"); ellipsoid(c,(x,y,z),(r,r*0.95,r*0.55),12,9); parts.append(c)
save("FOREST_TREE_BUTTRESS_L",parts)
# root arch: two slanted trunks + cross root limb
a1=P("arch_l","bark_v1"); limb(a1,(-1.6,0,0.0),(-0.25,0,2.1),0.20,0.15,10)
a2=P("arch_r","bark_v1"); limb(a2,(1.6,0,0.0),(0.25,0,2.1),0.20,0.15,10)
a3=P("arch_top","bark_v1"); limb(a3,(-0.3,0,2.05),(0.35,0,2.2),0.14,0.13,10)
save("FOREST_ROOT_ARCH",[a1,a2,a3])
rocks=[]
for i,(x,y,s) in enumerate(((0,0,1.0),(0.9,0.3,0.6),(-0.7,0.5,0.45))):
    r=P(f"rock_{i}","rock_dark_v1"); ellipsoid(r,(x,y,0.22*s),(0.55*s,0.42*s,0.30*s),10,8); rocks.append(r)
save("FOREST_ROCK_SET",rocks)
g=P("ground","ground_forest_v1"); box(g,0,0,-0.05,10,10,0.1)
pth=P("path","path_earth_v1"); box(pth,0,0,0.01,1.6,10,0.03)
save("FOREST_GROUND_PATH_10M",[g,pth])
post=P("marker_post","wood_palm_v1"); box(post,0,0,0.7,0.09,0.09,1.4)
cloth=P("marker_cloth","cloth_white_v1"); box(cloth,0.16,0,1.12,0.34,0.03,0.42)
save("ROUTE_MARKER_WHITECLOTH",[post,cloth])
man={"package":"FORBIDDEN_FOREST_KIT_V1","status":"PROVISIONAL production kit (source boards REVIEW REQUIRED - not canon)","modules":res,
 "pivot":"ground centre each module","collision":"tree: cylinder r0.9 h7; arch: two posts r0.2; rocks: bounds spheres; ground: none (landscape); marker: none (visual route cue)",
 "botany":"West African rainforest read (buttress roots, lianas as TA dressing); no temperate/tree-fern forms per board defect notes",
 "white_cloth_note":"route marker per NIGHT_PATH board cloth marker; NOT a ritual/sacred claim - ordinary route presentation, PM/Story confirm gameplay meaning"}
json.dump(man,open(os.path.join(OUT,"FOREST_KIT_MANIFEST.json"),"w"),indent=2); print(json.dumps(man,indent=2))
