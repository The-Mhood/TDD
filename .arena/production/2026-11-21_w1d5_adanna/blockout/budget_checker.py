#!/usr/bin/env python3
"""FP07-adjacent OBJ budget checker v0.1 (2026-11-21) — parse + report + fail conditions.
Usage: python3 budget_checker.py file.obj [--max-tris N] [--height-min M --height-max M]
Checks: vertex count, triangle estimate (ngon fan), bounds (X/Y/Z), NaN/inf, duplicate vertices, degenerate faces.
Exit 0 = pass, 2 = fail. Prints JSON report."""
import sys, json, math, argparse
from collections import Counter

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('obj')
    ap.add_argument('--max-tris', type=int, default=None)
    ap.add_argument('--height-min', type=float, default=None)
    ap.add_argument('--height-max', type=float, default=None)
    a = ap.parse_args()
    verts, faces = [], []
    for raw in open(a.obj, 'r', errors='replace'):
        s = raw.strip()
        if s.startswith('v '):
            p = s.split()
            try: verts.append((float(p[1]), float(p[2]), float(p[3])))
            except ValueError: verts.append((float('nan'),)*3)
        elif s.startswith('f '):
            idx = []
            for tok in s.split()[1:]:
                i = tok.split('/')[0]
                idx.append(int(i))
            faces.append(tuple(idx))
    tris = sum(max(0, len(f)-2) for f in faces)
    nan = sum(1 for v in verts if any(math.isnan(c) or math.isinf(c) for c in v))
    xs = [v[0] for v in verts]; ys = [v[1] for v in verts]; zs = [v[2] for v in verts]
    bounds = {'x': [min(xs), max(xs)], 'y': [min(ys), max(ys)], 'z': [min(zs), max(zs)]}
    dup = len(verts) - len(set(v for v in verts))
    degen = 0
    for f in faces:
        pts = [verts[i-1] for i in f if 1 <= i <= len(verts)]
        if len(pts) < 3: degen += 1; continue
        area2 = 0.0
        for i in range(1, len(pts)-1):
            a1, b1, c1 = pts[0], pts[i], pts[i+1]
            ux,uy,uz = b1[0]-a1[0], b1[1]-a1[1], b1[2]-a1[2]
            vx,vy,vz = c1[0]-a1[0], c1[1]-a1[1], c1[2]-a1[2]
            degen += 0
            area2 += math.sqrt((uy*vz-uz*vy)**2 + (uz*vx-ux*vz)**2 + (ux*vy-uy*vx)**2)
        if area2 < 1e-12: degen += 1
    problems = []
    if nan: problems.append(f'NaN/Inf vertices: {nan}')
    if degen: problems.append(f'Degenerate faces: {degen}')
    if a.max_tris is not None and tris > a.max_tris: problems.append(f'Tris {tris} > cap {a.max_tris}')
    h = bounds['z'][1] - bounds['z'][0]
    if a.height_min is not None and h < a.height_min: problems.append(f'Height {h:.3f} < min {a.height_min}')
    if a.height_max is not None and h > a.height_max: problems.append(f'Height {h:.3f} > max {a.height_max}')
    report = {'file': a.obj, 'vertices': len(verts), 'faces': len(faces), 'tris_est': tris,
              'bounds_m': {k: [round(v,4) for v in b] for k,b in bounds.items()},
              'height_m': round(h, 4), 'duplicate_vertices': dup, 'nan_vertices': nan,
              'degenerate_faces': degen, 'verdict': 'PASS' if not problems else 'FAIL', 'problems': problems}
    print(json.dumps(report, indent=2))
    sys.exit(0 if not problems else 2)

if __name__ == '__main__':
    main()
