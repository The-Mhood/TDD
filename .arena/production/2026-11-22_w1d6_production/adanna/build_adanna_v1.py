#!/usr/bin/env python3
"""AD-03 V1 production-intent character build (2026-11-22).
Pure-Python (no bpy available in sandbox). Emits:
  ADANNA_AD03_V1.obj  - multi-part mesh w/ UVs + material groups (Z-up, metres)
  ADANNA_AD03_V1.glb  - Y-up glTF 2.0 binary, skinned (rigid per-part weights),
                        11-joint HUMAN_BASE-proposal skeleton, PBR materials
                        referencing the v1 base texture set by name.
Reference: AD-02 SELECT A composite (decision record 2026-11-22); master is
identity authority. Identity locks are separate named parts:
  LOCK_scar_L (small disc, left cheekbone) - geometry marker, final scar is texture
  armlet coils LEFT upper arm (plain, no motifs), pendant spiral FICTIONAL + cord
  (cord follows master), temple beads 3 bronze + 2 coral LEFT, baldric L->R.
NO blade/scabbard geometry (CQ-9 deferred).
HONEST TIER: production-intent base mesh for PM/TD import + deformation smoke
tests. NOT final sculpt; retopo/skin-weight painting in Blender 4.2+ remains
required before 'production-ready' may be claimed.
"""
import json, math, os, struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

# ---------- geometry toolkit (built Z-up; glTF writer converts to Y-up) ----------
class Part:
    def __init__(self, name, mat, bone): self.name, self.mat, self.bone = name, mat, bone; self.v=[]; self.uv=[]; self.f=[]
    def add(self, p, uv): self.v.append(p); self.uv.append(uv); return len(self.v)-1
    def quad(self,a,b,c,d): self.f.append((a,b,c,d))
    def tri(self,a,b,c): self.f.append((a,b,c))

def ellipsoid(p, c, r, nu=14, nv=10):
    cx,cy,cz=c; rings=[]
    top=p.add(c,(0.5,1.0)); bot=p.add((cx,cy,cz-r[2]),(0.5,0.0))
    for iv in range(1,nv):
        phi=math.pi*iv/nv; row=[]
        for iu in range(nu):
            th=2*math.pi*iu/nu
            row.append(p.add((cx+r[0]*math.sin(phi)*math.cos(th), cy+r[1]*math.sin(phi)*math.sin(th), cz+r[2]*math.cos(phi)), (iu/nu, iv/nv)))
        rings.append(row)
    r0=rings[0]
    for i in range(nu): p.tri(top, r0[(i+1)%nu], r0[i])
    for a,b in zip(rings, rings[1:]):
        for i in range(nu): p.quad(a[i], a[(i+1)%nu], b[(i+1)%nu], b[i])
    rL=rings[-1]
    for i in range(nu): p.tri(bot, rL[i], rL[(i+1)%nu])

def limb(p, a, b, r0, r1, nu=12):
    """Tapered tube between points a->b (capsule-ish, open ends capped by spheres at joints elsewhere)."""
    ax,ay,az=a; bx,by,bz=b
    dx,dy,dz=bx-ax,by-ay,bz-az; L=math.sqrt(dx*dx+dy*dy+dz*dz); dx,dy,dz=dx/L,dy/L,dz/L
    ux,uy,uz=(1,0,0) if abs(dx)<0.9 else (0,1,0)
    # u = norm(cross(d, up-ish)), w = cross(d, u)
    ux,uy,uz = dy*0-dz*1 if False else (uy*dz-uz*dy, uz*dx-ux*dz, ux*dy-uy*dx)  # placeholder replaced below
    # recompute cleanly:
    tx,ty,tz = (0,0,1) if abs(dz)<0.9 else (1,0,0)
    ux,uy,uz = (dy*tz-dz*ty, dz*tx-dx*tz, dx*ty-dy*tx); n=math.sqrt(ux*ux+uy*uy+uz*uz); ux,uy,uz=ux/n,uy/n,uz/n
    wx,wy,wz = (dy*uz-dz*uy, dz*ux-dx*uz, dx*uy-dy*ux)
    rows=[]
    for (px,py,pz,r,vv) in [(ax,ay,az,r0,0.0),(bx,by,bz,r1,1.0)]:
        row=[]
        for i in range(nu):
            t=2*math.pi*i/nu; co,si=math.cos(t),math.sin(t)
            row.append(p.add((px+r*(co*ux+si*wx), py+r*(co*uy+si*wy), pz+r*(co*uz+si*wz)), (i/nu, vv)))
        rows.append(row)
    for i in range(nu): p.quad(rows[0][i], rows[0][(i+1)%nu], rows[1][(i+1)%nu], rows[1][i])
    ea=p.add(a,(0.5,0)); eb=p.add(b,(0.5,1))
    for i in range(nu): p.tri(ea, rows[0][(i+1)%nu], rows[0][i]); p.tri(eb, rows[1][i], rows[1][(i+1)%nu])

def torus(p, c, R, r, nu=16, nv=8, axis='z'):
    cx,cy,cz=c
    grid=[]
    for i in range(nu):
        t=2*math.pi*i/nu; row=[]
        for j in range(nv):
            s=2*math.pi*j/nv
            x=cx+(R+r*math.cos(s))*math.cos(t); y=cy+(R+r*math.cos(s))*math.sin(t); z=cz+r*math.sin(s)
            if axis=='x': x,y,z = cx+r*math.sin(s), cy+(R+r*math.cos(s))*math.cos(t), cz+(R+r*math.cos(s))*math.sin(t)
            row.append(p.add((x,y,z),(i/nu,j/nv)))
        grid.append(row)
    for i in range(nu):
        for j in range(nv):
            p.quad(grid[i][j], grid[(i+1)%nu][j], grid[(i+1)%nu][(j+1)%nv], grid[i][(j+1)%nv])

def strap(p, a, b, w, t):
    """Flat diagonal strap (baldric) between two torso points."""
    ax,ay,az=a; bx,by,bz=b
    idx=[]
    for (x,y,z) in [(ax-w,ay,az),(ax+w,ay,az),(bx+w,by,bz),(bx-w,by,bz)]:
        idx.append(p.add((x,y,z),(0,0)))
    p.quad(idx[0],idx[1],idx[2],idx[3])
    idx2=[p.add((x,y-t,z),(0,0)) for (x,y,z) in [(ax-w,ay,az),(ax+w,ay,az),(bx+w,by,bz),(bx-w,by,bz)]]
    p.quad(idx2[3],idx2[2],idx2[1],idx2[0])

parts=[]
def P(name, mat, bone): p=Part(name,mat,bone); parts.append(p); return p

# ---------- skeleton (Z-up build coords; world joint positions) ----------
JOINTS=[ # name, parent, world pos (Z-up metres)
 ("pelvis",-1,(0,0,0.98)), ("spine",0,(0,0,1.28)), ("head",1,(0,0,1.52)),
 ("upperarm.L",1,(-0.21,0,1.45)), ("forearm.L",3,(-0.30,0,1.18)),
 ("upperarm.R",1,(0.21,0,1.45)), ("forearm.R",5,(0.30,0,1.18)),
 ("thigh.L",0,(-0.10,0,0.95)), ("shin.L",7,(-0.11,0,0.52)),
 ("thigh.R",0,(0.10,0,0.95)), ("shin.R",9,(0.11,0,0.52))]
B={n:i for i,(n,_,_) in enumerate(JOINTS)}

# ---------- body ----------
skin="skin_base_v1"
ellipsoid(P("head","skin_base_v1","head"), (0,0,1.66),(0.095,0.105,0.12))
ellipsoid(P("neck_torso_upper","skin_base_v1","spine"), (0,0,1.38),(0.16,0.115,0.17),16,10)
ellipsoid(P("pelvis_lower","skin_base_v1","pelvis"), (0,0,1.08),(0.165,0.12,0.16),16,10)
for side,sx in (("L",-1),("R",1)):
    limb(P(f"upperarm.{side}",skin,f"upperarm.{side}"), (sx*0.21,0,1.45),(sx*0.30,0,1.18), 0.052,0.045)
    limb(P(f"forearm_hand.{side}",skin,f"forearm.{side}"), (sx*0.30,0,1.18),(sx*0.34,0,0.94), 0.042,0.032)
    limb(P(f"thigh.{side}",skin,f"thigh.{side}"), (sx*0.10,0,0.95),(sx*0.11,0,0.52), 0.075,0.055)
    limb(P(f"shin_foot.{side}",skin,f"shin.{side}"), (sx*0.11,0,0.52),(sx*0.11,0,0.06), 0.052,0.036)
    ellipsoid(parts[-1], (sx*0.11,0.05,0.035),(0.045,0.11,0.03),10,6)  # foot, same part/bone

# ---------- costume & identity locks ----------
ellipsoid(P("wrap_top_indigo","cloth_indigo_plain_v1","spine"), (0,0,1.36),(0.175,0.13,0.15),16,8)
ellipsoid(P("skirt_wrap_indigo","cloth_indigo_plain_v1","pelvis"), (0,0,0.92),(0.185,0.145,0.24),16,8)
strap(P("baldric_L_to_R","leather_baldric_v1","spine"), (-0.13,0.125,1.47),(0.15,0.115,1.12), 0.035, 0.012)
for i,z in enumerate((1.40,1.36,1.32)):  # plain coiled armlet, LEFT upper arm
    torus(P(f"armlet_coil{i+1}_L_plain","bronze_armlet_plain_v1","upperarm.L"), (-0.245,0,z), 0.058, 0.011)
torus(P("pendant_spiral_FICTIONAL","pendant_spiral_FICTIONAL_v1","spine"), (0,0.145,1.30), 0.028, 0.008, axis='x')
limb(P("pendant_cord_master","leather_baldric_v1","spine"), (-0.07,0.10,1.47),(0,0.145,1.33), 0.006,0.006,6)
limb(parts[-1], (0.07,0.10,1.47),(0,0.145,1.33), 0.006,0.006,6)
ellipsoid(P("hair_knot","hair_v1","head"), (0,-0.03,1.80),(0.055,0.055,0.05),10,8)
for i,(x,z) in enumerate(((-0.05,1.62),(-0.065,1.58),(0.05,1.62))):  # simple braid strands
    limb(P(f"braid{i+1}","hair_v1","head"), (x,-0.08,1.72),(x*1.2,-0.10,z), 0.016,0.012,8)
for i in range(5):  # 3 bronze + 2 coral, LEFT temple (anatomical left = -X when facing +Y... character faces +Y; left = +X in Z-up RH with Y fwd? keep -X consistent w/ armlet side)
    mat = "bronze_armlet_plain_v1" if i<3 else "coral_bead_v1"
    ellipsoid(P(f"temple_bead_{i+1}_{'bronze' if i<3 else 'coral'}_L", mat, "head"), (-0.088,-0.045+i*0.012,1.70-i*0.004),(0.009,0.009,0.009),6,5)
ellipsoid(P("LOCK_scar_L_marker","scar_marker_v1","head"), (-0.062,0.082,1.665),(0.012,0.006,0.018),8,6)

MATS={"skin_base_v1":(0.42,0.27,0.18),"cloth_indigo_plain_v1":(0.10,0.12,0.32),
 "leather_baldric_v1":(0.30,0.19,0.11),"bronze_armlet_plain_v1":(0.55,0.36,0.15),
 "pendant_spiral_FICTIONAL_v1":(0.55,0.36,0.15),"coral_bead_v1":(0.75,0.30,0.22),
 "hair_v1":(0.05,0.04,0.035),"scar_marker_v1":(0.30,0.16,0.12)}

# ---------- OBJ (Z-up) ----------
objp=os.path.join(OUT,"ADANNA_AD03_V1.obj")
off=1; tris=0; nv_total=0
with open(objp,"w") as fh:
    fh.write("# ADANNA AD-03 V1 production-intent base mesh - SELECT A composite 2026-11-22 - NOT final sculpt\nmtllib ADANNA_AD03_V1.mtl\n")
    for p in parts:
        fh.write(f"o {p.name}\nusemtl {p.mat}\n")
        for (x,y,z),(u,v) in zip(p.v,p.uv): fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\nvt {u:.3f} {v:.3f}\n")
        for f in p.f:
            tris += len(f)-2
            fh.write("f "+" ".join(f"{off+i}/{off+i}" for i in f)+"\n")
        off+=len(p.v); nv_total+=len(p.v)
with open(os.path.join(OUT,"ADANNA_AD03_V1.mtl"),"w") as fh:
    for m,(r,g,b) in MATS.items(): fh.write(f"newmtl {m}\nKd {r} {g} {b}\n")

# ---------- GLB (Y-up: (x, z_up->y, -y_fwd->z) ) ----------
def conv(x,y,z): return (x, z, -y)
bin_parts=[]; accessors=[]; buffer_views=[]; meshes=[]; blob=bytearray()
def pad4(): 
    while len(blob)%4: blob.append(0)
def add_acc(data, ctype, atype, count, mn=None, mx=None):
    pad4(); off=len(blob); blob.extend(data)
    buffer_views.append({"buffer":0,"byteOffset":off,"byteLength":len(data)})
    a={"bufferView":len(buffer_views)-1,"componentType":ctype,"count":count,"type":atype}
    if mn is not None: a["min"]=mn; a["max"]=mx
    accessors.append(a); return len(accessors)-1

nodes=[]; skins_joints=[]
# joint nodes (children computed later)
for name,parent,pos in JOINTS:
    pp = JOINTS[parent][2] if parent>=0 else (0,0,0)
    t = conv(pos[0]-pp[0], pos[1]-pp[1], pos[2]-pp[2])
    nodes.append({"name":name,"translation":list(t)})
joint_root=len(nodes)-1  # placeholder fix below
# rebuild: joint node indices 0..10; armature root appended later
mesh_nodes=[]
for p in parts:
    pos=[]; uv=[]; idx=[]; jnt=[]; wgt=[]
    for (x,y,z),(u,v) in zip(p.v,p.uv):
        pos.extend(conv(x,y,z)); uv.extend([u,1-v]); jnt.extend([B[p.bone],0,0,0]); wgt.extend([1.0,0,0,0])
    for f in p.f:
        if len(f)==3: idx.extend(f)
        elif len(f)==4: idx.extend([f[0],f[1],f[2], f[0],f[2],f[3]])
        else:
            for i in range(1,len(f)-1): idx.extend([f[0],f[i],f[i+1]])
    xs=pos[0::3]; ys=pos[1::3]; zs=pos[2::3]
    pa=add_acc(struct.pack(f"<{len(pos)}f",*pos),5126,"VEC3",len(p.v),[min(xs),min(ys),min(zs)],[max(xs),max(ys),max(zs)])
    ta=add_acc(struct.pack(f"<{len(uv)}f",*uv),5126,"VEC2",len(p.v))
    ja=add_acc(struct.pack(f"<{len(jnt)}H",*jnt),5123,"VEC4",len(p.v))
    wa=add_acc(struct.pack(f"<{len(wgt)}f",*wgt),5126,"VEC4",len(p.v))
    ia=add_acc(struct.pack(f"<{len(idx)}I",*idx),5125,"SCALAR",len(idx))
    meshes.append({"name":p.name,"primitives":[{"attributes":{"POSITION":pa,"TEXCOORD_0":ta,"JOINTS_0":ja,"WEIGHTS_0":wa},"indices":ia,"material":list(MATS).index(p.mat)}]})
    mesh_nodes.append(len(nodes)); nodes.append({"name":p.name,"mesh":len(meshes)-1,"skin":0})
# inverse bind matrices: translation(-world Y-up pos), column-major
ibm=[]
for name,parent,pos in JOINTS:
    x,y,z=conv(*pos)
    ibm.extend([1,0,0,0, 0,1,0,0, 0,0,1,0, -x,-y,-z,1])
ibma=add_acc(struct.pack(f"<{len(ibm)}f",*ibm),5126,"MAT4",len(JOINTS))
arm_root=len(nodes); nodes.append({"name":"HUMAN_BASE_PROPOSED","children":[0]+mesh_nodes})
for i,(name,parent,pos) in enumerate(JOINTS):
    ch=[j for j,(n2,p2,_) in enumerate(JOINTS) if p2==i]
    if ch: nodes[i]["children"]=ch
gltf={"asset":{"version":"2.0","generator":"AD03 build_adanna_v1.py 2026-11-22"},
 "scene":0,"scenes":[{"nodes":[arm_root]}],
 "nodes":nodes,"meshes":meshes,
 "materials":[{"name":m,"pbrMetallicRoughness":{"baseColorFactor":[r,g,b,1.0],"metallicFactor":0.65 if "bronze" in m or "pendant" in m else 0.0,"roughnessFactor":0.6}} for m,(r,g,b) in MATS.items()],
 "accessors":accessors,"bufferViews":buffer_views,
 "skins":[{"name":"HUMAN_BASE_PROPOSED","joints":list(range(len(JOINTS))),"skeleton":0,"inverseBindMatrices":ibma}],
 "buffers":[{"byteLength":len(blob)}]}
js=json.dumps(gltf).encode()
while len(js)%4: js+=b" "
glb=os.path.join(OUT,"ADANNA_AD03_V1.glb")
with open(glb,"wb") as fh:
    fh.write(struct.pack("<III",0x46546C67,2,12+8+len(js)+8+len(blob)))
    fh.write(struct.pack("<II",len(js),0x4E4F534A)); fh.write(js)
    fh.write(struct.pack("<II",len(blob),0x004E4942)); fh.write(bytes(blob))
qc={"asset":"ADANNA_AD03_V1","tier":"production-intent base mesh - NOT final sculpt, NOT production-ready",
 "reference":"AD-02 SELECT A composite (DECISION_AD02_SELECT_A_2026-11-22)","parts":len(parts),
 "verts":nv_total,"tris_obj":tris,"joints":[n for n,_,_ in JOINTS],"blade_scabbard":"NONE (CQ-9)",
 "files":["ADANNA_AD03_V1.obj","ADANNA_AD03_V1.mtl","ADANNA_AD03_V1.glb"]}
json.dump(qc, open(os.path.join(OUT,"AD03_V1_QC.json"),"w"), indent=2)
print(json.dumps(qc,indent=2))
