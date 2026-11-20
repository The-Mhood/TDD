#!/usr/bin/env python3
"""Populated CH01 Compound V2 - LOW/MEDIUM/HIGH static scale-check assemblies.
Merges compound V2 OBJ + NPC bind-pose OBJs at PM-proposal slots. STATIC
bind-pose population for scale/composition/clearance checks - animated
population in Unreal uses the skinned GLBs + CIVILIAN_CLIPS_V1.
Slots/facings from POPULATED_COMPOUND_PROPOSAL (W1 D16). Youth at 0.85 scale."""
import json, math, os
HERE=os.path.dirname(os.path.abspath(__file__)); PROD=os.path.abspath(os.path.join(HERE,"..",".."))
COMP=os.path.join(PROD,"2026-11-29_w1d13_production","ch01_assembly","out","CH01_COMPOUND_ASSEMBLED_V2.obj")
NPCDIR=[os.path.join(PROD,"2026-12-01_w1d15_production","npc_civilian_builds","out"),os.path.join(PROD,"2026-12-02_w1d16_production","npc_variants","out")]
def npc(name):
    for d in NPCDIR:
        p=os.path.join(d,name+".obj")
        if os.path.exists(p): return p
    raise FileNotFoundError(name)
# slot: (xy, facing_deg_from_+Y, asset, scale)
SLOTS={
 "A_veranda_edge":((-1.2,-1.3),180,"NPC_CIVILIAN_F1",1.0),
 "B_courtyard_west":((1.6,0.6),90,"NPC_CIVILIAN_M1",1.0),
 "C_courtyard_east":((3.6,1.8),270,"NPC_CIVILIAN_F1_EARTHRED",1.0),
 "D_gate_inside":((1.4,-3.4),180,"NPC_CIVILIAN_ELDER_M",1.0),
 "E_stall_front":((3.6,-3.2),90,"NPC_CIVILIAN_ELDER_F",1.0),
 "F_wall_shade_north":((-4.6,4.4),90,"NPC_CIVILIAN_YOUTH_M",0.85)}
DENS={"LOW_4":["A_veranda_edge","B_courtyard_west","D_gate_inside","F_wall_shade_north"],
      "MEDIUM_6":list(SLOTS),
      "HIGH_8":list(SLOTS)}
def load(path,dx=0,dy=0,rot=0,scale=1.0):
    lv=[];lf=[];cur="default"
    for line in open(path):
        p=line.split()
        if not p: continue
        if p[0]=='v':
            x,y,z=[float(v)*scale for v in p[1:4]]; c,s=math.cos(rot),math.sin(rot)
            lv.append((x*c-y*s+dx,x*s+y*c+dy,z))
        elif p[0]=='usemtl': cur=p[1]
        elif p[0]=='f': lf.append(([int(t.split('/')[0])-1 for t in p[1:]],cur))
    return lv,lf
def build(name,slots,extra_note=""):
    verts=[];faces=[]
    for src in [load(COMP)]+[load(npc(SLOTS[s][2]),SLOTS[s][0][0],SLOTS[s][0][1],math.radians(SLOTS[s][1]),SLOTS[s][3]) for s in slots]:
        lv,lf=src; base=len(verts); verts.extend(lv)
        for idx,m in lf: faces.append((tuple(i+base for i in idx),m))
    with open(os.path.join(HERE,name+".obj"),"w") as fh:
        fh.write(f"# {name} STATIC scale-check - PROVISIONAL\n")
        for x,y,z in verts: fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
        cur=None
        for idx,m in faces:
            if m!=cur: fh.write(f"usemtl {m}\n"); cur=m
            fh.write("f "+" ".join(str(i+1) for i in idx)+"\n")
    # clearance validation: pairwise slot distance, bounds inside wall ring, gate path strip x[0.0,0.8] y[-4.6,-2.6] must hold max 1 NPC at its edge
    pts=[SLOTS[s][0] for s in slots]
    mind=min(math.hypot(a[0]-b[0],a[1]-b[1]) for i,a in enumerate(pts) for b in pts[i+1:])
    inside=all(-6.0<=x<=6.2 and -4.4<=y<=5.2 for x,y in pts)
    gate_clear=all(not(0.0<=x<=0.8 and -4.6<=y<=-2.8) for x,y in pts)
    return {"assembly":name,"npcs":len(slots),"slots":slots,"verts":len(verts),"tris_est":sum(len(f[0])-2 for f in faces),
            "min_pairwise_clearance_m":round(mind,2),"all_inside_wall_ring":inside,"gate_path_strip_clear":gate_clear,
            "validation":"PASS" if (mind>=1.4 and inside and gate_clear) else "CHECK","note":extra_note}
man={"base":"CH01_COMPOUND_ASSEMBLED_V2 (provisional)","type":"STATIC bind-pose scale/composition check - NOT animated population, NOT canon",
     "densities":{k:build("CH01_POPULATED_"+k,v) for k,v in DENS.items() if k!="HIGH_8"}}
# HIGH_8: MEDIUM_6 + two extra Design slots inside verified-clear space (veranda west end + courtyard south), flagged PM-confirm
SLOTS["G_veranda_west"]=((-3.6,-1.3),180,"NPC_CIVILIAN_ELDER_F",1.0); SLOTS["H_courtyard_south"]=((2.6,-1.2),0,"NPC_CIVILIAN_YOUTH_M",0.85)
man["densities"]["HIGH_8"]=build("CH01_POPULATED_HIGH_8",DENS["HIGH_8"]+["G_veranda_west","H_courtyard_south"],"extra slots G/H are Design-proposed, PM-confirm")
man["pm_coordination"]="Density choice + slot/facing approval remains PM's; all three alternatives delivered per owner directive W1 campaign so PM picks without a Design round-trip. Animated population = skinned GLBs + CIVILIAN_CLIPS_V1 in Unreal (TD step)."
json.dump(man,open(os.path.join(HERE,"POPULATED_MANIFEST.json"),"w"),indent=2); print(json.dumps(man,indent=2))
