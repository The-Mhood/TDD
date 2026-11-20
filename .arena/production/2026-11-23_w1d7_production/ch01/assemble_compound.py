#!/usr/bin/env python3
"""Assemble CH01 compound V1: assembled hut + wall ring + gate. Provisional."""
import math, os
BASE = os.path.dirname(os.path.abspath(__file__))
HUT = os.path.abspath(os.path.join(BASE, "..", "..", "2026-11-22_w1d6_production", "kit_hut", "out"))
SET = os.path.join(BASE, "out")
def load(path):
    vs, fs, cur = [], [], "wall_laterite_mud"
    for line in open(path):
        s = line.split()
        if not s: continue
        if s[0] == "v": vs.append(tuple(map(float, s[1:4])))
        elif s[0] == "usemtl": cur = s[1]
        elif s[0] == "f": fs.append(([int(t.split("/")[0])-1 for t in s[1:]], cur))
    return vs, fs
def xf(p, tx, ty, rot):
    x, y, z = p; c, s = math.cos(rot), math.sin(rot)
    return (x*c-y*s+tx, x*s+y*c+ty, z)
verts, faces = [], []
def place(path, tx, ty, rot):
    vs, fs = load(path); b = len(verts)
    verts.extend(xf(p, tx, ty, rot) for p in vs)
    faces.extend(([i+b for i in idx], m) for idx, m in fs)
place(os.path.join(HUT, "CH01_HUT_ASSEMBLED_V1.obj"), 0, 0.6, 0)
W = os.path.join(SET, "KIT_COMPOUND_WALL_3M.obj"); G = os.path.join(SET, "KIT_GATE_2M.obj")
place(W, -1.5, -3.2, 0); place(G, 1.05, -3.2, 0)          # front wall + gate (gap at right)
place(W, -1.5, 3.6, 0); place(W, 1.5, 3.6, 0)            # back
place(W, -3.4, -1.4, math.pi/2); place(W, -3.4, 1.6, math.pi/2)   # left
place(W, 3.4, -1.4, math.pi/2); place(W, 3.4, 1.6, math.pi/2)     # right
out = os.path.join(SET, "CH01_COMPOUND_ASSEMBLED_V1.obj")
with open(out, "w") as fh:
    fh.write("# CH01 compound assembled V1 - provisional, not canon, not production-ready\nmtllib settlement.mtl\n")
    for v in verts: fh.write("v %.4f %.4f %.4f\n" % v)
    cur = None
    for idx, m in faces:
        if m != cur: fh.write(f"usemtl {m}\n"); cur = m
        fh.write("f " + " ".join(str(i+1) for i in idx) + "\n")
print("verts", len(verts), "faces", len(faces), "->", out)
