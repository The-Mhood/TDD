#!/usr/bin/env python3
"""Shared character production toolkit v0.2 (W1 D7, 2026-11-23).
Pure-Python (sandbox has no bpy). Builds skinned characters -> OBJ (Z-up, with
normals/UVs) + GLB (glTF 2.0, Y-up, smooth normals, up to 4-joint LBS weights,
optional embedded PNG base-colour textures). Source of truth = the builder
scripts that call this; Blender 4.2+ remains the sculpt/retopo finisher.
Skeleton: HUMAN_BASE proposal (11 joints) shared by Adanna + guard class.
"""
import json, math, os, struct

JOINTS = [("pelvis",-1,(0,0,0.98)), ("spine",0,(0,0,1.28)), ("head",1,(0,0,1.52)),
          ("upperarm.L",1,(-0.21,0,1.45)), ("forearm.L",3,(-0.30,0,1.18)),
          ("upperarm.R",1,(0.21,0,1.45)), ("forearm.R",5,(0.30,0,1.18)),
          ("thigh.L",0,(-0.10,0,0.95)), ("shin.L",7,(-0.11,0,0.52)),
          ("thigh.R",0,(0.10,0,0.95)), ("shin.R",9,(0.11,0,0.52))]
BONE = {n:i for i,(n,_,_) in enumerate(JOINTS)}

class Part:
    def __init__(self, name, mat, weights):
        """weights: bone-name str, or fn(x,y,z)->{bone: w}"""
        self.name, self.mat, self.wspec = name, mat, weights
        self.v, self.uv, self.f, self.w = [], [], [], []
    def add(self, p, uv):
        self.v.append(p); self.uv.append(uv)
        w = {self.wspec:1.0} if isinstance(self.wspec,str) else self.wspec(*p)
        s = sum(w.values()) or 1.0
        self.w.append({BONE[k]:v/s for k,v in w.items()})
        return len(self.v)-1
    def quad(self,a,b,c,d): self.f.append((a,b,c,d))
    def tri(self,a,b,c): self.f.append((a,b,c))

def ellipsoid(p, c, r, nu=20, nv=14):
    cx,cy,cz = c; rings=[]
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

def limb(p, a, b, r0, r1, nu=16, rings_n=3):
    ax,ay,az=a; bx,by,bz=b
    dx,dy,dz=bx-ax,by-ay,bz-az; L=math.sqrt(dx*dx+dy*dy+dz*dz); dx,dy,dz=dx/L,dy/L,dz/L
    tx,ty,tz=(0,0,1) if abs(dz)<0.9 else (1,0,0)
    ux,uy,uz=(dy*tz-dz*ty, dz*tx-dx*tz, dx*ty-dy*tx); n=math.sqrt(ux*ux+uy*uy+uz*uz); ux,uy,uz=ux/n,uy/n,uz/n
    wx,wy,wz=(dy*uz-dz*uy, dz*ux-dx*uz, dx*uy-dy*ux)
    rows=[]
    for ri in range(rings_n+1):
        t=ri/rings_n; px,py,pz=ax+dx*L*t, ay+dy*L*t, az+dz*L*t; r=r0+(r1-r0)*t
        row=[]
        for i in range(nu):
            th=2*math.pi*i/nu; co,si=math.cos(th),math.sin(th)
            row.append(p.add((px+r*(co*ux+si*wx), py+r*(co*uy+si*wy), pz+r*(co*uz+si*wz)), (i/nu, t)))
        rows.append(row)
    for ra,rb in zip(rows, rows[1:]):
        for i in range(nu): p.quad(ra[i], ra[(i+1)%nu], rb[(i+1)%nu], rb[i])
    ea=p.add(a,(0.5,0)); eb=p.add(b,(0.5,1))
    for i in range(nu): p.tri(ea, rows[0][(i+1)%nu], rows[0][i]); p.tri(eb, rows[-1][i], rows[-1][(i+1)%nu])

def torus(p, c, R, r, nu=20, nv=10, axis='z', squash_z=1.0):
    cx,cy,cz=c; grid=[]
    for i in range(nu):
        t=2*math.pi*i/nu; row=[]
        for j in range(nv):
            s=2*math.pi*j/nv
            x=cx+(R+r*math.cos(s))*math.cos(t); y=cy+(R+r*math.cos(s))*math.sin(t); z=cz+r*math.sin(s)*squash_z
            if axis=='x': x,y,z = cx+r*math.sin(s), cy+(R+r*math.cos(s))*math.cos(t), cz+(R+r*math.cos(s))*math.sin(t)
            if axis=='y': x,y,z = cx+(R+r*math.cos(s))*math.cos(t), cy+r*math.sin(s), cz+(R+r*math.cos(s))*math.sin(t)
            row.append(p.add((x,y,z),(i/nu,j/nv)))
        grid.append(row)
    for i in range(nu):
        for j in range(nv):
            p.quad(grid[i][j], grid[(i+1)%nu][j], grid[(i+1)%nu][(j+1)%nv], grid[i][(j+1)%nv])

def strap(p, a, b, w, thick):
    ax,ay,az=a; bx,by,bz=b
    front=[p.add((x,y,z),(0,0)) for (x,y,z) in [(ax-w,ay,az),(ax+w,ay,az),(bx+w,by,bz),(bx-w,by,bz)]]
    p.quad(*front)
    back=[p.add((x,y-thick,z),(0,0)) for (x,y,z) in [(ax-w,ay,az),(ax+w,ay,az),(bx+w,by,bz),(bx-w,by,bz)]]
    p.quad(back[3],back[2],back[1],back[0])

def box(p, cx,cy,cz, sx,sy,sz):
    x0,x1,y0,y1,z0,z1 = cx-sx/2,cx+sx/2,cy-sy/2,cy+sy/2,cz-sz/2,cz+sz/2
    a=p.add((x0,y0,z0),(0,0)); b=p.add((x1,y0,z0),(1,0)); c=p.add((x1,y1,z0),(1,1)); d=p.add((x0,y1,z0),(0,1))
    e=p.add((x0,y0,z1),(0,0)); f=p.add((x1,y0,z1),(1,0)); g=p.add((x1,y1,z1),(1,1)); h=p.add((x0,y1,z1),(0,1))
    p.quad(a,b,f,e); p.quad(b,c,g,f); p.quad(c,d,h,g); p.quad(d,a,e,h); p.quad(e,f,g,h); p.quad(d,c,b,a)

def lathe(p, profile, nu=24, fold_amp=0.0, fold_n=7, cap_top=True, cap_bot=True, slant=0.0):
    """Garment/body lathe around Z axis. profile items: (radius, z) or
    (rx, ry, z) for elliptical plans (milestone 2). slant: top edge rises by
    slant*cos(theta) (one-shoulder construction)."""
    rows = []
    for item in profile:
        if len(item) == 2: rx = ry = item[0]; z = item[1]
        else: rx, ry, z = item
        row = []
        for i in range(nu):
            t = 2*math.pi*i/nu
            f = 1 + fold_amp*math.sin(fold_n*t + z*3.0)
            row.append(p.add((rx*f*math.cos(t), ry*f*math.sin(t), z + slant*math.cos(t)), (i/nu, z)))
        rows.append(row)
    for ra, rb in zip(rows, rows[1:]):
        for i in range(nu): p.quad(ra[i], ra[(i+1) % nu], rb[(i+1) % nu], rb[i])
    if cap_bot:
        c = p.add((0, 0, profile[0][-1]), (0.5, 0))
        for i in range(nu): p.tri(c, rows[0][(i+1) % nu], rows[0][i])
    if cap_top:
        c = p.add((0, 0, profile[-1][-1]), (0.5, 1))
        for i in range(nu): p.tri(c, rows[-1][i], rows[-1][(i+1) % nu])

def hand(p, cx, side):
    """Palm + 4 fingers + thumb at wrist point cx (hanging hand, sculpt milestone)."""
    box(p, cx[0], cx[1], cx[2]-0.045, 0.055, 0.022, 0.085)
    for i in range(4):
        fx = cx[0] + side*(i-1.5)*0.013
        limb(p, (fx, cx[1], cx[2]-0.085), (fx, cx[1]+0.002, cx[2]-0.145), 0.0058, 0.0045, 8, rings_n=2)
    limb(p, (cx[0]+side*0.030, cx[1]+0.008, cx[2]-0.055), (cx[0]+side*0.048, cx[1]+0.014, cx[2]-0.105), 0.006, 0.0045, 8, rings_n=2)

def toes(p, cx):
    for i in range(3):
        ellipsoid(p, (cx[0]+(i-1)*0.020, cx[1]+0.105, cx[2]), (0.0095, 0.014, 0.008), 8, 6)

def compute_normals(part):
    n=[[0.0,0.0,0.0] for _ in part.v]
    for f in part.f:
        idx=list(f)
        tris=[idx] if len(idx)==3 else [idx[:3],[idx[0],idx[2],idx[3]]]
        for t in tris:
            a,b,c=[part.v[i] for i in t]
            ux,uy,uz=b[0]-a[0],b[1]-a[1],b[2]-a[2]; vx,vy,vz=c[0]-a[0],c[1]-a[1],c[2]-a[2]
            cx,cy,cz=uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
            for i in t: n[i][0]+=cx; n[i][1]+=cy; n[i][2]+=cz
    out=[]
    for x,y,z in n:
        l=math.sqrt(x*x+y*y+z*z) or 1.0; out.append((x/l,y/l,z/l))
    return out

def conv(x,y,z): return (x, z, -y)   # Z-up -> glTF Y-up

def write_obj(path, parts, mats):
    off=1; tris=0; nv=0
    with open(path,"w") as fh:
        fh.write("# skinned character source export (Z-up, metres) - see QC json for tier\nmtllib "+os.path.basename(path).replace(".obj",".mtl")+"\n")
        for p in parts:
            normals=compute_normals(p)
            fh.write(f"o {p.name}\nusemtl {p.mat}\n")
            for (x,y,z),(u,v),nn in zip(p.v,p.uv,normals):
                fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\nvt {u:.3f} {v:.3f}\nvn {nn[0]:.3f} {nn[1]:.3f} {nn[2]:.3f}\n")
            for f in p.f:
                tris += len(f)-2
                fh.write("f "+" ".join(f"{off+i}/{off+i}/{off+i}" for i in f)+"\n")
            off+=len(p.v); nv+=len(p.v)
    with open(path.replace(".obj",".mtl"),"w") as fh:
        for m,(r,g,b) in mats.items(): fh.write(f"newmtl {m}\nKd {r} {g} {b}\n")
    return nv, tris

def write_glb(path, parts, mats, textures=None, meta=""):
    textures = textures or {}
    blob=bytearray(); accessors=[]; views=[]; images=[]; gltf_mats=[]; meshes=[]; nodes=[]
    def pad4():
        while len(blob)%4: blob.append(0)
    def acc(data, ctype, atype, count, mn=None, mx=None):
        pad4(); o=len(blob); blob.extend(data)
        views.append({"buffer":0,"byteOffset":o,"byteLength":len(data)})
        a={"bufferView":len(views)-1,"componentType":ctype,"count":count,"type":atype}
        if mn is not None: a["min"]=mn; a["max"]=mx
        accessors.append(a); return len(accessors)-1
    tex_index={}
    for mname, png in textures.items():
        pad4(); o=len(blob); blob.extend(png)
        views.append({"buffer":0,"byteOffset":o,"byteLength":len(png)})
        images.append({"bufferView":len(views)-1,"mimeType":"image/png","name":mname})
        tex_index[mname]=len(images)-1
    for m,(r,g,b) in mats.items():
        mat={"name":m,"pbrMetallicRoughness":{"baseColorFactor":[r,g,b,1.0],
             "metallicFactor":0.65 if ("bronze" in m or "pendant" in m) else 0.0,"roughnessFactor":0.62}}
        if m in tex_index: mat["pbrMetallicRoughness"]["baseColorTexture"]={"index":tex_index[m]}
        gltf_mats.append(mat)
    for name,parent,pos in JOINTS:
        pp = JOINTS[parent][2] if parent>=0 else (0,0,0)
        nodes.append({"name":name,"translation":list(conv(pos[0]-pp[0],pos[1]-pp[1],pos[2]-pp[2]))})
    mesh_nodes=[]
    for p in parts:
        normals=compute_normals(p)
        pos=[]; uv=[]; nor=[]; idx=[]; jnt=[]; wgt=[]
        for (x,y,z),(u,v),nn,w in zip(p.v,p.uv,normals,p.w):
            pos.extend(conv(x,y,z)); uv.extend([u,1-v]); nor.extend(conv(*nn))
            top=sorted(w.items(), key=lambda kv:-kv[1])[:4]
            jj=[k for k,_ in top]+[0]*(4-len(top)); ww=[v for _,v in top]+[0.0]*(4-len(top))
            s=sum(ww) or 1.0; jnt.extend(jj); wgt.extend([x2/s for x2 in ww])
        for f in p.f:
            if len(f)==3: idx.extend(f)
            elif len(f)==4: idx.extend([f[0],f[1],f[2], f[0],f[2],f[3]])
            else:
                for i in range(1,len(f)-1): idx.extend([f[0],f[i],f[i+1]])
        xs,ys,zs=pos[0::3],pos[1::3],pos[2::3]
        pa=acc(struct.pack(f"<{len(pos)}f",*pos),5126,"VEC3",len(p.v),[min(xs),min(ys),min(zs)],[max(xs),max(ys),max(zs)])
        na=acc(struct.pack(f"<{len(nor)}f",*nor),5126,"VEC3",len(p.v))
        ta=acc(struct.pack(f"<{len(uv)}f",*uv),5126,"VEC2",len(p.v))
        ja=acc(struct.pack(f"<{len(jnt)}H",*jnt),5123,"VEC4",len(p.v))
        wa=acc(struct.pack(f"<{len(wgt)}f",*wgt),5126,"VEC4",len(p.v))
        ia=acc(struct.pack(f"<{len(idx)}I",*idx),5125,"SCALAR",len(idx))
        meshes.append({"name":p.name,"primitives":[{"attributes":{"POSITION":pa,"NORMAL":na,"TEXCOORD_0":ta,"JOINTS_0":ja,"WEIGHTS_0":wa},"indices":ia,"material":list(mats).index(p.mat)}]})
        mesh_nodes.append(len(nodes)); nodes.append({"name":p.name,"mesh":len(meshes)-1,"skin":0})
    ibm=[]
    for name,parent,pos in JOINTS:
        x,y,z=conv(*pos); ibm.extend([1,0,0,0, 0,1,0,0, 0,0,1,0, -x,-y,-z,1])
    ibma=acc(struct.pack(f"<{len(ibm)}f",*ibm),5126,"MAT4",len(JOINTS))
    root=len(nodes); nodes.append({"name":"HUMAN_BASE_PROPOSED","children":[0]+mesh_nodes})
    for i,(name,parent,pos) in enumerate(JOINTS):
        ch=[j for j,(n2,p2,_) in enumerate(JOINTS) if p2==i]
        if ch: nodes[i]["children"]=ch
    gltf={"asset":{"version":"2.0","generator":"charbuild.py v0.2 2026-11-23 "+meta},
          "scene":0,"scenes":[{"nodes":[root]}],"nodes":nodes,"meshes":meshes,"materials":gltf_mats,
          "accessors":accessors,"bufferViews":views,
          "skins":[{"name":"HUMAN_BASE_PROPOSED","joints":list(range(len(JOINTS))),"skeleton":0,"inverseBindMatrices":ibma}],
          "buffers":[{"byteLength":len(blob)}]}
    if images: gltf["images"]=images; gltf["samplers"]=[{"magFilter":9729,"minFilter":9987}]; gltf["textures"]=[{"sampler":0,"source":i} for i in range(len(images))]
    js=json.dumps(gltf).encode()
    while len(js)%4: js+=b" "
    with open(path,"wb") as fh:
        fh.write(struct.pack("<III",0x46546C67,2,12+8+len(js)+8+len(blob)))
        fh.write(struct.pack("<II",len(js),0x4E4F534A)); fh.write(js)
        fh.write(struct.pack("<II",len(blob),0x004E4942)); fh.write(bytes(blob))
