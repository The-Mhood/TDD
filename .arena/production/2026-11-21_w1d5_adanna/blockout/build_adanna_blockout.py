#!/usr/bin/env python3
"""ADANNA_BLOCKOUT_PROXY v1 (2026-11-21) — PLACEHOLDER for PM import/scale/capsule/silhouette testing ONLY.
NOT the production model, NOT an identity reference, NOT approved art. Neutral grey single material.
Proportions derived from approved master (~1.80 m, ~7.5 heads). Meters, origin at ground centre, +Z up, +Y forward."""
import math, json, os

verts, faces, mtl_groups = [], [], {}

def v(x, y, z):
    verts.append((round(x, 5), round(y, 5), round(z, 5)))
    return len(verts)  # 1-based

def quad(a, b, c, d): faces.append((a, b, c, d))
def tri(a, b, c): faces.append((a, b, c))

def frustum(sects, r_bottom, r_top, y_squash=1.0, n=10):
    """Vertical elliptical frustum; returns (bottom_ring, top_ring) vertex indices."""
    bottom, top = [], []
    for i in range(n):
        a = 2*math.pi*i/n
        ca, sa = math.cos(a), math.sin(a)
        bottom.append(v(r_bottom*ca, r_bottom*sa*y_squash, sects[0]))
        top.append(v(r_top*ca, r_top*sa*y_squash, sects[1]))
    for i in range(n):
        j = (i+1) % n
        quad(bottom[i], bottom[j], top[j], top[i])
    # cap bottom (fan to centroid) and top
    cb = v(0, 0, sects[0]); ct = v(0, 0, sects[1])
    for i in range(n):
        j = (i+1) % n
        tri(cb, bottom[j], bottom[i]); tri(ct, top[i], top[j])
    return bottom, top

def capsule_limb(p0, p1, r0, r1, n=8, rings=2):
    """Tapered limb along arbitrary axis via two rings per segment (linear interp)."""
    import math as m
    x0,y0,z0 = p0; x1,y1,z1 = p1
    dx,dy,dz = x1-x0, y1-y0, z1-z0
    L = m.sqrt(dx*dx+dy*dy+dz*dz)
    ux,uy,uz = dx/L, dy/L, dz/L
    # orthonormal basis
    if abs(uz) < 0.9: ax,ay,az = -uy, ux, 0.0
    else: ax,ay,az = 1.0, 0.0, 0.0
    l = m.sqrt(ax*ax+ay*ay+az*az); ax,ay,az = ax/l, ay/l, az/l
    bx,by,bz = uy*az-uz*ay, uz*ax-ux*az, ux*ay-uy*ax
    rings_idx = []
    for k in range(rings+1):
        t = k/rings
        cx,cy,cz = x0+dx*t, y0+dy*t, z0+dz*t
        r = r0 + (r1-r0)*t
        ring = []
        for i in range(n):
            a = 2*m.pi*i/n
            ca,sa = m.cos(a), m.sin(a)
            px = cx + r*(ca*ax + sa*bx)
            py = cy + r*(ca*ay + sa*by)
            pz = cz + r*(ca*az + sa*bz)
            ring.append(v(px,py,pz))
        rings_idx.append(ring)
    for k in range(rings):
        rA, rB = rings_idx[k], rings_idx[k+1]
        for i in range(n):
            j = (i+1) % n
            quad(rA[i], rA[j], rB[j], rB[i])
    c0 = v(x0,y0,z0)
    for i in range(n):
        j = (i+1) % n
        tri(c0, rings_idx[0][j], rings_idx[0][i])
    c1 = v(x1,y1,z1)
    for i in range(n):
        j = (i+1) % n
        tri(c1, rings_idx[-1][i], rings_idx[-1][j])

def ellipsoid(cx, cy, cz, rx, ry, rz, n_u=10, n_v=6):
    rings = []
    for iv in range(1, n_v):                       # interior latitude rings (skip poles)
        phi = math.pi*iv/n_v
        row = []
        for iu in range(n_u):
            th = 2*math.pi*iu/n_u
            row.append(v(cx + rx*math.sin(phi)*math.cos(th),
                         cy + ry*math.sin(phi)*math.sin(th),
                         cz + rz*math.cos(phi)))
        rings.append(row)
    top = v(cx, cy, cz + rz)                        # single pole vertices
    bot = v(cx, cy, cz - rz)
    r0 = rings[0]
    for i in range(n_u):                            # top fan
        tri(top, r0[i], r0[(i+1) % n_u])
    for iv in range(len(rings)-1):                  # bands
        for iu in range(n_u):
            a = rings[iv][iu]; b = rings[iv][(iu+1) % n_u]
            c = rings[iv+1][(iu+1) % n_u]; d = rings[iv+1][iu]
            quad(a, b, c, d)
    rL = rings[-1]
    for i in range(n_u):                            # bottom fan
        tri(bot, rL[(i+1) % n_u], rL[i])

def box(cx, cy, cz, sx, sy, sz):
    x0,x1 = cx-sx/2, cx+sx/2; y0,y1 = cy-sy/2, cy+sy/2; z0,z1 = cz-sz/2, cz+sz/2
    p = [v(x0,y0,z0), v(x1,y0,z0), v(x1,y1,z0), v(x0,y1,z0),
         v(x0,y0,z1), v(x1,y0,z1), v(x1,y1,z1), v(x0,y1,z1)]
    quad(p[0],p[1],p[2],p[3]); quad(p[4],p[7],p[6],p[5])
    quad(p[0],p[4],p[5],p[1]); quad(p[1],p[5],p[6],p[2])
    quad(p[2],p[6],p[7],p[3]); quad(p[3],p[7],p[4],p[0])

# ---- body masses (1.80 m standing, meters) ----
frustum((0.90, 1.01), 0.205, 0.175, 0.62, n=12)          # pelvis/hip block
frustum((1.01, 1.31), 0.165, 0.150, 0.68, n=12)          # torso lower→bust
frustum((1.31, 1.47), 0.150, 0.185, 0.66, n=12)          # bust→shoulders
frustum((1.47, 1.58), 0.060, 0.048, 0.80, n=8)           # neck
ellipsoid(0, 0, 1.685, 0.088, 0.098, 0.120, n_u=12, n_v=7)   # head
# arms (straight, slight A)
capsule_limb(( 0.205, 0.0, 1.44), ( 0.245, 0.0, 1.13), 0.062, 0.052, n=8, rings=2)
capsule_limb(( 0.245, 0.0, 1.13), ( 0.265, 0.0, 0.87), 0.050, 0.038, n=8, rings=2)
capsule_limb((-0.205, 0.0, 1.44), (-0.245, 0.0, 1.13), 0.062, 0.052, n=8, rings=2)
capsule_limb((-0.245, 0.0, 1.13), (-0.265, 0.0, 0.87), 0.050, 0.038, n=8, rings=2)
ellipsoid( 0.268, 0.01, 0.815, 0.040, 0.028, 0.075, n_u=8, n_v=5)   # hands
ellipsoid(-0.268, 0.01, 0.815, 0.040, 0.028, 0.075, n_u=8, n_v=5)
# legs
capsule_limb(( 0.115, 0.0, 0.90), ( 0.120, 0.0, 0.48), 0.092, 0.066, n=8, rings=2)
capsule_limb(( 0.120, 0.0, 0.48), ( 0.122, 0.0, 0.115), 0.064, 0.043, n=8, rings=2)
capsule_limb((-0.115, 0.0, 0.90), (-0.120, 0.0, 0.48), 0.092, 0.066, n=8, rings=2)
capsule_limb((-0.120, 0.0, 0.48), (-0.122, 0.0, 0.115), 0.064, 0.043, n=8, rings=2)
# feet: wedge boxes, toes +Y
box( 0.124, 0.115, 0.045, 0.095, 0.21, 0.075)
box(-0.124, 0.115, 0.045, 0.095, 0.21, 0.075)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
obj = os.path.join(OUT_DIR, 'ADANNA_BLOCKOUT_PLACEHOLDER_m.obj')
with open(obj, 'w') as f:
    f.write('# ADANNA_BLOCKOUT_PLACEHOLDER_m v1 2026-11-21\n')
    f.write('# PLACEHOLDER ONLY - PM scale/capsule/silhouette testing. NOT production mesh.\n')
    f.write('mtllib adanna_placeholder.mtl\nusemtl M_ADANNA_PLACEHOLDER\n')
    for x,y,z in verts: f.write(f'v {x} {y} {z}\n')
    f.write('g Adanna_blockout\n')
    for face in faces: f.write('f ' + ' '.join(str(i) for i in face) + '\n')
with open(os.path.join(OUT_DIR, 'adanna_placeholder.mtl'), 'w') as f:
    f.write('newmtl M_ADANNA_PLACEHOLDER\nKa 0.5 0.5 0.5\nKd 0.62 0.62 0.62\nKs 0.0 0.0 0.0\n')
with open(os.path.join(OUT_DIR, 'ADANNA_BLOCKOUT_MANIFEST.json'), 'w') as f:
    json.dump({'asset': 'ADANNA_BLOCKOUT_PLACEHOLDER_m.obj', 'status': 'PLACEHOLDER - NOT production', 'units': 'meters', 'origin': 'ground centre', 'up': '+Z', 'forward': '+Y', 'height_m': 1.80, 'faces': len(faces), 'vertices': len(verts), 'material': 'M_ADANNA_PLACEHOLDER (flat grey)', 'ue_import': 'UE 5.8.4 OBJ; scale to cm on import (x100) per FP-07; verify capsule r/h per TD', 'replaced_by': 'ADANNA_base_LOD0 after AD-02 CD selection + AD-03'}, f, indent=2)
print('verts', len(verts), 'faces', len(faces))
