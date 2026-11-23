#!/usr/bin/env python3
"""Orthographic flat-shaded preview renderer (pure PIL) for sculpt milestones.
Not a Blender render - a geometry sanity view so Design can self-inspect
before the Mac finisher produces official previews.
Usage: render_preview.py file.glb out_prefix  -> {front,back,side,three_quarter}.png
"""
import json, math, struct, sys
sys.path.insert(0, "../2026-11-23_w1d7_production/pipeline")
from test_deformation import load
from PIL import Image, ImageDraw

path, prefix = sys.argv[1], sys.argv[2]
g, acc = load(path)
tris = []  # (verts3, color, depthkey normal)
for mesh in g['meshes']:
    pr = mesh['primitives'][0]
    pos = [tuple(v) for v in acc(pr['attributes']['POSITION'])]
    idx = [t[0] for t in acc(pr['indices'])]
    mat = g['materials'][pr.get('material', 0)]
    col = mat.get('pbrMetallicRoughness', {}).get('baseColorFactor', [0.7, 0.7, 0.7, 1])
    rgb = tuple(int(255*c) for c in col[:3])
    for i in range(0, len(idx), 3):
        a, b, c = pos[idx[i]], pos[idx[i+1]], pos[idx[i+2]]
        tris.append((a, b, c, rgb))

def project(p, view):
    # Returns (u, v, depth) with depth = distance from camera (far drawn first).
    # Character faces -Z in glTF space. Anatomical left = -X (proven in the
    # qualified Blender renders: armlet appears image-right in true front view).
    x, y, z = p
    if view == 'front': return (-x, y, z)          # camera at -Z looking +Z
    if view == 'back': return (x, y, -z)           # camera at +Z looking -Z
    if view == 'side': return (-z, y, -x)          # camera at +X looking -X (character's left side)
    t = math.radians(-35)                          # three_quarter: front-left orbit
    return (-(x*math.cos(t) - z*math.sin(t)), y, x*math.sin(t) + z*math.cos(t))

W, H = 480, 600
for view in ('front', 'back', 'side', 'three_quarter'):
    img = Image.new('RGB', (W, H), (176, 176, 176))
    dr = ImageDraw.Draw(img)
    faces = []
    for a, b, c, rgb in tris:
        pa, pb, pc = project(a, view), project(b, view), project(c, view)
        # face normal (view space) for flat shading + backface-ish light
        ux, uy, uz = pb[0]-pa[0], pb[1]-pa[1], pb[2]-pa[2]
        vx, vy, vz = pc[0]-pa[0], pc[1]-pa[1], pc[2]-pa[2]
        nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        L = math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        shade = 0.55 + 0.45*abs(nz/L)
        col = tuple(max(0, min(255, int(ch*shade))) for ch in rgb)
        depth = (pa[2]+pb[2]+pc[2])/3
        faces.append((depth, pa, pb, pc, col))
    faces.sort(key=lambda f: -f[0])  # painter: farthest first
    for depth, pa, pb, pc, col in faces:
        pts = [(W/2 + p[0]*235, H - 40 - p[1]*300) for p in (pa, pb, pc)]
        dr.polygon(pts, fill=col)
    img.save(f"{prefix}_{view}.png")
    print("wrote", f"{prefix}_{view}.png")
