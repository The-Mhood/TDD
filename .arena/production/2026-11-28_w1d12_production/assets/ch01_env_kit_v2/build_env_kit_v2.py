#!/usr/bin/env python3
"""CH01 Environment Kit V2 (2026-11-28) - advances the approved Family
Compound reference (W1 D11) into modular Unreal-ready kit pieces.
Extends W1 D7 modules (same material names/dimensions; wall 2.0 m,
thatch language). All PROVISIONAL - not canon, not production-final.
Modules: corner wall, pitched house roof, veranda, courtyard set
(storage pots, basket, fire pit). Collision = one box proxy per module
(bounds in manifest) for PM/TD to confirm in-engine. Units: metres, Z-up OBJ.
"""
import json, os
class Mesh:
    def __init__(self, name): self.name=name; self.verts=[]; self.faces=[]
    def v(self,x,y,z): self.verts.append((x,y,z)); return len(self.verts)
    def quad(self,a,b,c,d,mat): self.faces.append(((a,b,c,d),mat))
def box(m,cx,cy,cz,sx,sy,sz,mat):
    x0,x1,y0,y1,z0,z1=cx-sx/2,cx+sx/2,cy-sy/2,cy+sy/2,cz-sz/2,cz+sz/2
    a=m.v(x0,y0,z0);b=m.v(x1,y0,z0);c=m.v(x1,y1,z0);d=m.v(x0,y1,z0)
    e=m.v(x0,y0,z1);f=m.v(x1,y0,z1);g=m.v(x1,y1,z1);h=m.v(x0,y1,z1)
    m.quad(a,b,f,e,mat);m.quad(b,c,g,f,mat);m.quad(c,d,h,g,mat);m.quad(d,a,e,h,mat);m.quad(e,f,g,h,mat);m.quad(d,c,b,a,mat)
def gable_roof(m, w, d, eave, ridge, mat, over=0.35):
    a=m.v(-w/2-over,-d/2-over,eave); b=m.v(w/2+over,-d/2-over,eave); c=m.v(w/2+over,d/2+over,eave); dd=m.v(-w/2-over,d/2+over,eave)
    r0=m.v(-w/2-over,0,ridge); r1=m.v(w/2+over,0,ridge)
    m.quad(a,b,r1,r0,mat); m.quad(c,dd,r0,r1,mat); m.faces.append(((b,c,r1),mat)); m.faces.append(((dd,a,r0),mat))
    # ridge cap + eave binding poles
    box(m,0,0,ridge+0.03,w+2*over,0.12,0.07,TIM); box(m,0,-d/2-over,eave-0.03,w+2*over,0.08,0.06,TIM); box(m,0,d/2+over,eave-0.03,w+2*over,0.08,0.06,TIM)

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out"); os.makedirs(OUT,exist_ok=True)
MUD="wall_laterite_mud"; FND="foundation_laterite_rubble"; TH="thatch_ata_bundles"; TIM="timber_lintel_plain"; CLAY="clay_pot_fired"; FIB="woven_fibre_plain"; STONE="courtyard_stone_plain"

def wall_corner():
    m=Mesh("KIT_WALL_CORNER_3M")
    box(m,0.2,0,0.2,3.0,0.5,0.4,FND); box(m,0,0.2,0.2-0.0,0.5,3.0,0.4,FND)
    box(m,0.2,0,1.15,3.0,0.32,1.5,MUD); box(m,0,0.2,1.15,0.32,3.0,1.5,MUD)
    box(m,0.2,0,1.95,3.0,0.4,0.1,TH); box(m,0,0.2,1.95,0.4,3.0,0.1,TH)  # thatch caps as W1 D7 wall
    return m
def roof_house():
    m=Mesh("KIT_ROOF_HOUSE_5X4")  # for 5x4 m house, wall top 2.2 m
    gable_roof(m,5.0,4.0,2.2,3.9,TH); return m
def veranda():
    m=Mesh("KIT_VERANDA_5M")  # front shade along 5 m wall: posts + lean-to thatch
    for x in (-2.4,-1.2,0,1.2,2.4): box(m,x,-1.15,1.05,0.11,0.11,2.1,TIM)
    a=m.v(-2.65,-1.45,1.95); b=m.v(2.65,-1.45,1.95); c=m.v(2.65,0.05,2.5); d=m.v(-2.65,0.05,2.5)
    m.quad(a,b,c,d,TH); box(m,0,-0.7,0.06,5.0,2.3,0.12,FND)  # raised earth platform
    return m
def courtyard():
    m=Mesh("KIT_COURTYARD_SET")
    # storage pots (lathe-ish stacked boxes approximated by tapered boxes)
    for i,(x,y,s) in enumerate(((-0.8,-0.5,1.0),(-0.35,-0.55,0.75),(0.05,-0.5,0.6))):
        box(m,x,y,0.22*s,0.42*s,0.42*s,0.44*s,CLAY); box(m,x,y,0.50*s,0.30*s,0.30*s,0.12*s,CLAY); box(m,x,y,0.58*s,0.34*s,0.34*s,0.05*s,CLAY)
    box(m,0.75,-0.5,0.16,0.5,0.5,0.32,FIB)   # coiled basket
    box(m,1.25,-0.45,0.02,0.6,0.45,0.04,FIB) # woven mat flat
    # fire pit: ring of stones + ash centre (cooking-fire ambience anchor)
    import math
    for k in range(8):
        a=2*math.pi*k/8; box(m,1.0+0.28*math.cos(a),0.55+0.28*math.sin(a),0.07,0.16,0.14,0.14,STONE)
    box(m,1.0,0.55,0.03,0.4,0.4,0.05,STONE)
    return m
MTL="""newmtl foundation_laterite_rubble
Kd 0.45 0.26 0.16
newmtl wall_laterite_mud
Kd 0.58 0.33 0.20
newmtl thatch_ata_bundles
Kd 0.62 0.48 0.26
newmtl timber_lintel_plain
Kd 0.30 0.20 0.12
newmtl clay_pot_fired
Kd 0.42 0.24 0.15
newmtl woven_fibre_plain
Kd 0.55 0.42 0.24
newmtl courtyard_stone_plain
Kd 0.32 0.30 0.28
"""
def write(m):
    p=os.path.join(OUT,m.name+".obj")
    with open(p,"w") as fh:
        fh.write(f"# {m.name} - CH01 Env Kit V2 PROVISIONAL - not canon\nmtllib env_kit_v2.mtl\n")
        for x,y,z in m.verts: fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
        cur=None
        for idx,mat in m.faces:
            if mat!=cur: fh.write(f"usemtl {mat}\n"); cur=mat
            fh.write("f "+" ".join(str(i) for i in idx)+"\n")
    xs=[v[0] for v in m.verts]; ys=[v[1] for v in m.verts]; zs=[v[2] for v in m.verts]
    return {"file":os.path.basename(p),"verts":len(m.verts),"tris_est":sum(len(f[0])-2 for f in m.faces),
            "bounds_m":[round(max(xs)-min(xs),2),round(max(ys)-min(ys),2),round(max(zs)-min(zs),2)],
            "collision_proxy":"single box = bounds (PM/TD confirm in-engine)"}
mods=[wall_corner(), roof_house(), veranda(), courtyard()]
open(os.path.join(OUT,"env_kit_v2.mtl"),"w").write(MTL)
man={"kit":"CH01-ENV-KIT","version":"2.0","date":"2026-11-28","status":"PROVISIONAL production kit - not canon, not final",
     "units":"metres, Z-up OBJ (Unreal import: rotate to Z-up convention as with W1 D7 modules)",
     "materials_shared_with":"W1 D7 settlement.mtl (identical names for wall/thatch/timber/foundation)",
     "modules":[write(m) for m in mods],
     "prior_modules_reused":["KIT_COMPOUND_WALL_3M","KIT_GATE_2M","KIT_STALL_2x2 (W1 D7, unchanged)"],
     "plaster_note":"production finish = smooth maintained clay plaster (compound reference is authority; detail study reads too cracked)"}
json.dump(man, open(os.path.join(OUT,"ENV_KIT_V2_MANIFEST.json"),"w"), indent=2)
print(json.dumps(man,indent=2))
