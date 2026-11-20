#!/usr/bin/env python3
"""KIT-HUT modular placeholder/provisional geometry v0.1 (2026-11-22, W1 D6).
Pure-Python OBJ writer (no bpy — sandbox has no Blender). Modules aligned to the
VERIFIED CH01-SUBJ-001 family-house target: laterite mud walls, broad foundation,
high-pitched hipped thatch roof, small doorway, plain timber lintel.
STATUS: PROVISIONAL greybox-replacement geometry. NOT approved cultural canon,
NOT production-ready. CD kit sign-off + TD/PM dimension sign-off required before
any Unreal import. Units: metres, +Z up, origin at ground centre of each module.
Run: python3 build_kit_hut.py  -> writes OBJ/MTL/manifest into ./out/
"""
import json, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

class Mesh:
    def __init__(self, name):
        self.name = name; self.verts = []; self.faces = []  # (indices, material)
    def v(self, x, y, z):
        self.verts.append((x, y, z)); return len(self.verts)
    def quad(self, a, b, c, d, mat):
        self.faces.append(((a, b, c, d), mat))
    def tri(self, a, b, c, mat):
        self.faces.append(((a, b, c), mat))

def box(m, cx, cy, cz, sx, sy, sz, mat):
    x0, x1 = cx-sx/2, cx+sx/2; y0, y1 = cy-sy/2, cy+sy/2; z0, z1 = cz-sz/2, cz+sz/2
    a=m.v(x0,y0,z0); b=m.v(x1,y0,z0); c=m.v(x1,y1,z0); d=m.v(x0,y1,z0)
    e=m.v(x0,y0,z1); f=m.v(x1,y0,z1); g=m.v(x1,y1,z1); h=m.v(x0,y1,z1)
    m.quad(a,b,f,e,mat); m.quad(b,c,g,f,mat); m.quad(c,d,h,g,mat); m.quad(d,a,e,h,mat)
    m.quad(e,f,g,h,mat); m.quad(d,c,b,a,mat)

def wall_straight():
    m = Mesh("KIT_HUT_WALL_3M")
    box(m, 0, 0, 0.25, 3.0, 0.45, 0.5, "foundation_laterite_rubble")   # broad foundation
    box(m, 0, 0, 1.45, 3.0, 0.35, 1.9, "wall_laterite_mud")            # wall to eaves 2.4m
    return m

def wall_door():
    m = Mesh("KIT_HUT_WALL_DOOR_3M")
    box(m, 0, 0, 0.25, 3.0, 0.45, 0.5, "foundation_laterite_rubble")
    # door opening 0.8w x 1.7h centred; two side piers + lintel band
    box(m, -1.1, 0, 1.35, 0.8, 0.35, 1.7, "wall_laterite_mud")
    box(m,  1.1, 0, 1.35, 0.8, 0.35, 1.7, "wall_laterite_mud")
    box(m,  0, 0, 2.05, 1.4, 0.35, 0.7, "wall_laterite_mud")
    box(m,  0, 0, 1.78, 1.0, 0.42, 0.14, "timber_lintel_plain")        # plain timber lintel
    return m

def wall_corner():
    m = Mesh("KIT_HUT_CORNER")
    box(m, -0.9, 0, 0.25, 1.35, 0.45, 0.5, "foundation_laterite_rubble")
    box(m, 0, -0.9, 0.25, 0.45, 1.35, 0.5, "foundation_laterite_rubble")
    box(m, -0.9, 0, 1.45, 1.35, 0.35, 1.9, "wall_laterite_mud")
    box(m, 0, -0.9, 1.45, 0.35, 1.35, 1.9, "wall_laterite_mud")
    box(m, 0, 0, 1.45, 0.35, 0.35, 1.9, "wall_laterite_mud")
    return m

def hipped_roof():
    m = Mesh("KIT_HUT_ROOF_HIP_4x3")
    # footprint 4.4 x 3.4 (overhang), eaves z=2.4, ridge z=4.1, ridge along X length 1.6
    ex, ey, ez, rz, rl = 2.2, 1.7, 2.4, 4.1, 0.8
    a=m.v(-ex,-ey,ez); b=m.v(ex,-ey,ez); c=m.v(ex,ey,ez); d=m.v(-ex,ey,ez)
    r0=m.v(-rl,0,rz); r1=m.v(rl,0,rz)
    m.quad(a,b,r1,r0,"thatch_ata_bundles"); m.quad(c,d,r0,r1,"thatch_ata_bundles")
    m.tri(b,c,r1,"thatch_ata_bundles"); m.tri(d,a,r0,"thatch_ata_bundles")
    # corner stakes at wall tops (triangular stake markers, per R1/R4)
    for sx in (-1,1):
        for sy in (-1,1):
            box(m, sx*1.95, sy*1.45, 2.45, 0.09, 0.09, 0.35, "timber_stake")
    return m

def doorframe():
    m = Mesh("KIT_HUT_DOORFRAME")
    box(m, -0.45, 0, 0.85, 0.1, 0.12, 1.7, "timber_lintel_plain")
    box(m,  0.45, 0, 0.85, 0.1, 0.12, 1.7, "timber_lintel_plain")
    box(m,  0, 0, 1.75, 1.0, 0.12, 0.12, "timber_lintel_plain")
    box(m,  0, 0.03, 0.02, 1.0, 0.18, 0.05, "timber_threshold")
    return m

MTL = """newmtl foundation_laterite_rubble
Kd 0.45 0.26 0.16
newmtl wall_laterite_mud
Kd 0.58 0.33 0.20
newmtl thatch_ata_bundles
Kd 0.62 0.48 0.26
newmtl timber_lintel_plain
Kd 0.30 0.20 0.12
newmtl timber_stake
Kd 0.32 0.22 0.13
newmtl timber_threshold
Kd 0.28 0.19 0.11
"""

def write(m):
    p = os.path.join(OUT, m.name + ".obj")
    tris = sum(len(f[0])-2 for f in m.faces)
    with open(p, "w") as fh:
        fh.write(f"# {m.name} - KIT-HUT provisional module v0.1 2026-11-22 - NOT production-ready, NOT canon\n")
        fh.write("mtllib kit_hut.mtl\n")
        for x,y,z in m.verts: fh.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
        cur = None
        for idx, mat in m.faces:
            if mat != cur: fh.write(f"usemtl {mat}\n"); cur = mat
            fh.write("f " + " ".join(str(i) for i in idx) + "\n")
    return {"file": os.path.basename(p), "verts": len(m.verts), "faces": len(m.faces), "tris_est": tris}

mods = [wall_straight(), wall_door(), wall_corner(), hipped_roof(), doorframe()]
with open(os.path.join(OUT, "kit_hut.mtl"), "w") as fh: fh.write(MTL)
manifest = {"kit": "KIT-HUT", "version": "0.1", "date": "2026-11-22", "status": "PROVISIONAL - not production-ready, not canon",
            "target_sheet": "CH01-SUBJ-001_FAMILY_HOUSE_TARGET_SHEET.jpg (VERIFIED target, CD kit sign-off pending)",
            "modules": [write(m) for m in mods]}
with open(os.path.join(OUT, "KIT_HUT_MANIFEST.json"), "w") as fh: json.dump(manifest, fh, indent=2)
print(json.dumps(manifest, indent=2))
