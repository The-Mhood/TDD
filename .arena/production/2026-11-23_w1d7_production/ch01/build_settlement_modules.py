#!/usr/bin/env python3
"""CH01 settlement modules W1 D7 (2026-11-23): compound wall, gate, market stall.
Continues KIT-HUT (same materials/dimensions language). Pure-Python OBJ.
Research basis: compound walls of mud/clay enclosing family compounds, small
gated entrance (W1 D5 sources R3/R4; CH01 research notes W1 D3: compound wall
'ngwulu' class; obi faces gate). Stall = generic market shelter: 4 timber
posts + pitched thatch shade roof + counter — construction-generic, NO claimed
ritual/cultural specificity. All PROVISIONAL, not canon, not production-ready.
Collision: simple box proxies listed in manifest (PM/TD to confirm in-engine).
"""
import json, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "2026-11-22_w1d6_production", "kit_hut")))
# reuse Mesh/box from kit builder without running it: inline minimal copy
class Mesh:
    def __init__(self, name): self.name=name; self.verts=[]; self.faces=[]
    def v(self,x,y,z): self.verts.append((x,y,z)); return len(self.verts)
    def quad(self,a,b,c,d,mat): self.faces.append(((a,b,c,d),mat))
def box(m,cx,cy,cz,sx,sy,sz,mat):
    x0,x1,y0,y1,z0,z1=cx-sx/2,cx+sx/2,cy-sy/2,cy+sy/2,cz-sz/2,cz+sz/2
    a=m.v(x0,y0,z0);b=m.v(x1,y0,z0);c=m.v(x1,y1,z0);d=m.v(x0,y1,z0)
    e=m.v(x0,y0,z1);f=m.v(x1,y0,z1);g=m.v(x1,y1,z1);h=m.v(x0,y1,z1)
    m.quad(a,b,f,e,mat);m.quad(b,c,g,f,mat);m.quad(c,d,h,g,mat);m.quad(d,a,e,h,mat);m.quad(e,f,g,h,mat);m.quad(d,c,b,a,mat)

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
MUD="wall_laterite_mud"; FND="foundation_laterite_rubble"; TH="thatch_ata_bundles"; TIM="timber_lintel_plain"

def compound_wall():
    m=Mesh("KIT_COMPOUND_WALL_3M"); box(m,0,0,0.2,3.0,0.5,0.4,FND); box(m,0,0,1.15,3.0,0.32,1.5,MUD)
    box(m,0,0,1.95,3.0,0.4,0.1,TH)  # protective thatch cap (wall-top aju cover, cf. uli-archive R7 note)
    return m
def gate():
    m=Mesh("KIT_GATE_2M")
    box(m,-0.95,0,0.25,0.4,0.5,0.5,FND); box(m,0.95,0,0.25,0.4,0.5,0.5,FND)
    box(m,-0.95,0,1.2,0.3,0.34,1.9,MUD); box(m,0.95,0,1.2,0.3,0.34,1.9,MUD)
    box(m,0,0,2.22,2.3,0.4,0.16,TIM); box(m,0,0,1.05,1.45,0.06,2.0,TIM)  # lintel + plain timber leaf
    return m
def stall():
    m=Mesh("KIT_STALL_2x2")
    for sx in (-0.95,0.95):
        for sy in (-0.75,0.75): box(m,sx,sy,1.05,0.12,0.12,2.1,TIM)
    # pitched thatch shade roof 2.6x2.2, ridge along X at z=2.45, eaves z=2.1
    a=m.v(-1.3,-1.1,2.1); b=m.v(1.3,-1.1,2.1); c=m.v(1.3,1.1,2.1); d=m.v(-1.3,1.1,2.1)
    r0=m.v(-1.3,0,2.45); r1=m.v(1.3,0,2.45)
    m.quad(a,b,r1,r0,TH); m.quad(c,d,r0,r1,TH)
    m.faces.append(((b,c,r1),TH)); m.faces.append(((d,a,r0),TH))
    box(m,0,-0.85,0.55,2.0,0.35,0.08,TIM); box(m,0,-0.85,0.28,2.0,0.08,0.5,TIM)  # counter + legs panel
    return m

MTL="""newmtl foundation_laterite_rubble
Kd 0.45 0.26 0.16
newmtl wall_laterite_mud
Kd 0.58 0.33 0.20
newmtl thatch_ata_bundles
Kd 0.62 0.48 0.26
newmtl timber_lintel_plain
Kd 0.30 0.20 0.12
"""
def write(m):
    p=os.path.join(OUT,m.name+".obj")
    with open(p,"w") as fh:
        fh.write(f"# {m.name} - CH01 provisional module W1 D7 - not canon\nmtllib settlement.mtl\n")
        for x,y,z in m.verts: fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
        cur=None
        for idx,mat in m.faces:
            if mat!=cur: fh.write(f"usemtl {mat}\n"); cur=mat
            fh.write("f "+" ".join(str(i) for i in idx)+"\n")
    return {"file":os.path.basename(p),"verts":len(m.verts),"faces":len(m.faces),
            "tris_est":sum(len(f[0])-2 for f in m.faces),
            "collision_proxy":"single box = module bounds (PM/TD confirm)"}
mods=[compound_wall(), gate(), stall()]
open(os.path.join(OUT,"settlement.mtl"),"w").write(MTL)
man={"kit":"CH01-SETTLEMENT","version":"0.1","date":"2026-11-23","status":"PROVISIONAL - not production-ready, not canon",
     "modules":[write(m) for m in mods],
     "assembly":"CH01_COMPOUND_ASSEMBLED_V1.obj = KIT-HUT house + 6 wall segments + gate (see assemble_compound.py)"}
json.dump(man, open(os.path.join(OUT,"SETTLEMENT_MANIFEST.json"),"w"), indent=2)
print(json.dumps(man,indent=2))
