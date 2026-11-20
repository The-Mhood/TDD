#!/usr/bin/env python3
"""Regression test: per-joint skinning influence (added 2026-11-25).
Catches the Adanna V3 failure class where a limb bone owned almost no
vertices (forearm.L: 16 verts >0.5 weight, 0.054 m max leverage -> Blender
pose-test bbox delta 0.0, FINISHER FAIL). The deformation suite alone cannot
catch this (it only bounds maximum displacement).
For every joint asserts:
  - at least MIN_STRONG vertices weighted > 0.5 to it, and
  - max leverage (distance from joint origin among verts weighted > 0.25)
    >= MIN_LEVERAGE for limb joints (they must be able to move geometry).
Usage: test_joint_influence.py file.glb -> JSON; exit 0 pass / 2 fail.
"""
import json, math, sys
sys.path.insert(0, ".")
from test_deformation import load

MIN_STRONG = 25
MIN_LEVERAGE = 0.15
LIMB = ("upperarm", "forearm", "thigh", "shin")

def run(path):
    g, acc = load(path)
    joints = g['skins'][0]['joints']
    names = [g['nodes'][j]['name'] for j in joints]
    ibm = [list(m) for m in acc(g['skins'][0]['inverseBindMatrices'])]
    origins = {names[i]: (-ibm[i][12], -ibm[i][13], -ibm[i][14]) for i in range(len(names))}
    strong = {n: 0 for n in names}; lev = {n: 0.0 for n in names}
    for mesh in g['meshes']:
        pr = mesh['primitives'][0]
        pos = [tuple(v) for v in acc(pr['attributes']['POSITION'])]
        jn = [tuple(int(x) for x in j) for j in acc(pr['attributes']['JOINTS_0'])]
        w = [tuple(x) for x in acc(pr['attributes']['WEIGHTS_0'])]
        for v, jj, ww in zip(pos, jn, w):
            for k in range(4):
                n = names[jj[k]]
                if ww[k] > 0.5: strong[n] += 1
                if ww[k] > 0.25: lev[n] = max(lev[n], math.dist(v, origins[n]))
    fails = []
    detail = {}
    for n in names:
        d = {"verts_gt_0.5": strong[n], "max_leverage_m": round(lev[n], 3)}
        detail[n] = d
        if strong[n] < MIN_STRONG: fails.append(f"{n}: only {strong[n]} verts >0.5 (min {MIN_STRONG})")
        if n.startswith(LIMB) and lev[n] < MIN_LEVERAGE:
            fails.append(f"{n}: leverage {lev[n]:.3f} m < {MIN_LEVERAGE} m (bone cannot move geometry)")
    print(json.dumps({"file": path, "joints": detail, "verdict": "PASS" if not fails else "FAIL", "failures": fails}, indent=2))
    return 0 if not fails else 2

if __name__ == '__main__':
    sys.exit(run(sys.argv[1]))
