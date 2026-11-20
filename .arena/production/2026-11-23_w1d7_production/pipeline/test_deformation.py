#!/usr/bin/env python3
"""Deformation + GLB integrity test (W1 D7). Parses a skinned GLB built by
charbuild.py, applies joint rotations (shoulder raise, elbow bend, wrist via
forearm twist, hip/knee bend, neck turn, torso twist), linear-blend-skins all
vertices in pure Python, and asserts: finite output, max displacement sane,
height stays plausible, blended joints show no rigid-fold spike (max per-vertex
displacement < 1.1 m limb-length bound). Usage: test_deformation.py file.glb -> JSON, exit 0 pass.
This is a smoke test, NOT a substitute for Blender deformation review.
"""
import json, math, struct, sys

def mat_mul(A, B):
    # column-major storage (glTF): element (r,c) at index c*4+r
    return [sum(A[k*4+r]*B[c*4+k] for k in range(4)) for c in range(4) for r in range(4)]
def mat_point(M, p):
    x, y, z = p
    return (M[0]*x+M[4]*y+M[8]*z+M[12], M[1]*x+M[5]*y+M[9]*z+M[13], M[2]*x+M[6]*y+M[10]*z+M[14])
def rot(axis, ang):
    c, s = math.cos(ang), math.sin(ang)
    if axis == 'x': return [1,0,0,0, 0,c,s,0, 0,-s,c,0, 0,0,0,1]
    if axis == 'y': return [c,0,-s,0, 0,1,0,0, s,0,c,0, 0,0,0,1]
    return [c,s,0,0, -s,c,0,0, 0,0,1,0, 0,0,0,1]
def trans(t): return [1,0,0,0, 0,1,0,0, 0,0,1,0, t[0],t[1],t[2],1]

def load(path):
    d = open(path, 'rb').read()
    assert struct.unpack('<I', d[:4])[0] == 0x46546C67, "not GLB"
    jl = struct.unpack('<I', d[12:16])[0]
    g = json.loads(d[20:20+jl])
    boff = 20+jl+8
    binchunk = d[boff:]
    def acc_data(ai):
        a = g['accessors'][ai]; bv = g['bufferViews'][a['bufferView']]
        o = bv.get('byteOffset', 0); n = a['count']
        fmt = {5126: ('f', 4), 5123: ('H', 2), 5125: ('I', 4)}[a['componentType']]
        comp = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[a['type']]
        vals = struct.unpack_from(f"<{n*comp}{fmt[0]}", binchunk, o)
        return [vals[i*comp:(i+1)*comp] for i in range(n)]
    return g, acc_data

POSES = {"rest": {}, "shoulder_raise_L": {"upperarm.L": ('z', -1.9)}, "elbow_bend_L": {"forearm.L": ('z', -1.6)},
         "forearm_twist_R": {"forearm.R": ('y', 1.2)}, "hip_knee_bend_R": {"thigh.R": ('x', -1.1), "shin.R": ('x', 1.5)},
         "neck_turn": {"head": ('y', 0.7)}, "torso_twist": {"spine": ('y', 0.55)}, "combined": {"spine": ('y', 0.4), "upperarm.R": ('z', 1.7), "forearm.R": ('z', 1.4), "thigh.L": ('x', -0.9), "shin.L": ('x', 1.3), "head": ('y', -0.5)}}

def run(path):
    g, acc_data = load(path)
    joints = g['skins'][0]['joints']
    ibm = [list(m) for m in acc_data(g['skins'][0]['inverseBindMatrices'])]
    name2joint = {g['nodes'][j]['name']: k for k, j in enumerate(joints)}
    verts, jnts, wgts = [], [], []
    for mesh in g['meshes']:
        pr = mesh['primitives'][0]
        verts += [tuple(v) for v in acc_data(pr['attributes']['POSITION'])]
        jnts += [tuple(int(x) for x in j) for j in acc_data(pr['attributes']['JOINTS_0'])]
        wgts += [tuple(w) for w in acc_data(pr['attributes']['WEIGHTS_0'])]
    parents, locals_ = {}, {}
    for j in joints:
        nd = g['nodes'][j]; locals_[j] = trans(nd.get('translation', [0, 0, 0]))
    for ni, nd in enumerate(g['nodes']):
        for c in nd.get('children', []): parents[c] = ni
    def skin(pose):
        world = {}
        def compute(j):
            if j in world: return world[j]
            p = parents.get(j)
            base = mat_mul(compute(p), locals_[j]) if p in [x for x in joints] or p in world or (p is not None and p in locals_) else locals_[j]
            if p is not None and p in joints: base = mat_mul(world[p], locals_[j])
            nm = g['nodes'][j]['name']
            if nm in pose: base = mat_mul(base, rot(*pose[nm]))
            world[j] = base; return base
        for j in joints: compute(j)
        skinm = [mat_mul(world[joints[k]], ibm[k]) for k in range(len(joints))]
        out = []; maxd = 0.0
        for v, jj, ww in zip(verts, jnts, wgts):
            p = [0.0, 0.0, 0.0]
            for k in range(4):
                if ww[k] <= 0: continue
                q = mat_point(skinm[jj[k]], v)
                for a in range(3): p[a] += ww[k]*q[a]
            out.append(p)
            maxd = max(maxd, math.dist(v, p))
        return out, maxd
    results = {}
    ok = True
    for pname, pose in POSES.items():
        mapped = {name2joint and k: v for k, v in pose.items() if k in name2joint}
        out, maxd = skin(pose)
        finite = all(all(math.isfinite(c) for c in p) for p in out)
        ys = [p[1] for p in out]
        passed = finite and maxd < 1.1 and (max(ys)-min(ys)) > 1.2
        ok = ok and passed
        results[pname] = {"finite": finite, "max_vertex_disp_m": round(maxd, 3), "height_m": round(max(ys)-min(ys), 3), "pass": passed}
    print(json.dumps({"file": path, "verts_skinned": len(verts), "joints": len(joints), "poses": results, "verdict": "PASS" if ok else "FAIL"}, indent=2))
    return 0 if ok else 2

if __name__ == '__main__':
    sys.exit(run(sys.argv[1]))
