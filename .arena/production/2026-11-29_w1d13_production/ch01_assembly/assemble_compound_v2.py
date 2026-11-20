#!/usr/bin/env python3
"""CH01 Compound Assembled V2 (2026-11-29) - one importable OBJ assembling
Env Kit V2 + W1 D7 modules into the approved compound layout (Kit V1 ref).
PROVISIONAL - not canon. Metres, Z-up. House walls are a simple mud shell
(module KIT-HUT lineage dims: 5x4 m, walls 2.2 m) under KIT_ROOF_HOUSE_5X4.
"""
import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,"..",".."))
KIT2=os.path.join(ROOT,"2026-11-28_w1d12_production","assets","ch01_env_kit_v2","out")
KIT1=os.path.join(ROOT,"2026-11-23_w1d7_production","ch01","out")
OUT=os.path.join(HERE,"out"); os.makedirs(OUT,exist_ok=True)
verts=[]; faces=[]  # (idx tuple, mat)
def load(path, dx=0, dy=0, rot=0):
    lv=[]; lf=[]; cur="wall_laterite_mud"
    for line in open(path):
        p=line.split()
        if not p: continue
        if p[0]=='v':
            x,y,z=map(float,p[1:4]); c,s=math.cos(rot),math.sin(rot)
            lv.append((x*c-y*s+dx, x*s+y*c+dy, z))
        elif p[0]=='usemtl': cur=p[1]
        elif p[0]=='f': lf.append(([int(t.split('/')[0])-1 for t in p[1:]], cur))
    base=len(verts); verts.extend(lv)
    for idx,mat in lf: faces.append((tuple(i+base for i in idx), mat))
def box(cx,cy,cz,sx,sy,sz,mat):
    # reuse kit writer style via temp verts
    x0,x1,y0,y1,z0,z1=cx-sx/2,cx+sx/2,cy-sy/2,cy+sy/2,cz-sz/2,cz+sz/2
    cs=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    base=len(verts); verts.extend(cs)
    for a,b,c,d in ((0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7),(3,2,1,0)):
        faces.append(((base+a,base+b,base+c,base+d),mat))
MUD="wall_laterite_mud"; TH="thatch_ata_bundles"
# house shell 5x4 at (-2.2, 1.8), roof + veranda on its south face
box(-2.2,1.8,1.1,5.0,4.0,2.2,MUD)
load(os.path.join(KIT2,"KIT_ROOF_HOUSE_5X4.obj"),-2.2,1.8)
load(os.path.join(KIT2,"KIT_VERANDA_5M.obj"),-2.2,-0.6)
# compound wall ring ~13x11 m with south gate gap
for x in (-4.5,-1.5,3.0,5.2): load(os.path.join(KIT1,"KIT_COMPOUND_WALL_3M.obj"),x,-4.6)
for x in (-4.5,-1.5,1.5,4.5): load(os.path.join(KIT1,"KIT_COMPOUND_WALL_3M.obj"),x,5.4)
for y in (-1.6,1.4,4.2): load(os.path.join(KIT1,"KIT_COMPOUND_WALL_3M.obj"),-6.2,y,rot=math.pi/2)
for y in (-1.6,1.4): load(os.path.join(KIT1,"KIT_COMPOUND_WALL_3M.obj"),6.4,y,rot=math.pi/2)
load(os.path.join(KIT2,"KIT_WALL_CORNER_3M.obj"),-6.2,5.4)
load(os.path.join(KIT1,"KIT_GATE_2M.obj"),0.4,-4.6)
load(os.path.join(KIT2,"KIT_COURTYARD_SET.obj"),2.6,1.2)
load(os.path.join(KIT1,"KIT_STALL_2x2.obj"),4.3,-2.4)
with open(os.path.join(OUT,"CH01_COMPOUND_ASSEMBLED_V2.obj"),"w") as fh:
    fh.write("# CH01_COMPOUND_ASSEMBLED_V2 - PROVISIONAL not canon\nmtllib env_kit_v2.mtl\n")
    for x,y,z in verts: fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
    cur=None
    for idx,mat in faces:
        if mat!=cur: fh.write(f"usemtl {mat}\n"); cur=mat
        fh.write("f "+" ".join(str(i+1) for i in idx)+"\n")
import shutil; shutil.copy(os.path.join(KIT2,"env_kit_v2.mtl"), os.path.join(OUT,"env_kit_v2.mtl"))
man={"asset":"CH01_COMPOUND_ASSEMBLED_V2","status":"PROVISIONAL production assembly - not canon","verts":len(verts),
     "tris_est":sum(len(f[0])-2 for f in faces),"footprint_m":"13.4 x 10.6 compound; house 5x4, ridge 3.9",
     "modules":"Env Kit V2 (roof/veranda/corner/courtyard) + W1 D7 (wall/gate/stall), unchanged module files",
     "collision":"use module bounds proxies from kit manifests (PM/TD confirm)"}
json.dump(man, open(os.path.join(OUT,"ASSEMBLY_V2_MANIFEST.json"),"w"), indent=2); print(json.dumps(man,indent=2))
