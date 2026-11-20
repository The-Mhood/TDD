#!/usr/bin/env python3
"""AD-03 V2 refinement (2026-11-23, W1 D7). Continues ADANNA_AD03_V1.
Improvements over V1: denser smooth-shaded topology (computed normals), refined
proportions (head/neck/waist/shoulder balance vs SELECT-A composite), joint
spheres at elbows/knees/shoulders/hips, blended (non-rigid) skin weights across
neck/shoulder/elbow/hip/knee/waist, embedded 512px base-colour textures from the
v1 texture set (indigo/leather/bronze), UVs on every part.
Identity locks preserved as separate parts; NO blade/scabbard (CQ-9).
Tier: refined production-intent model. NOT final: Blender sculpt/retopo +
weight paint + TD texture ratification still required (see W1D7 report).
"""
import io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from charbuild import Part, ellipsoid, limb, torus, strap, compute_normals, write_obj, write_glb, JOINTS
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "2026-11-20_w1d4_research", "textures"))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

def blend(z, zlo, zhi, low, high):
    def fn(x, y, zz):
        t = max(0.0, min(1.0, (zz-zlo)/(zhi-zlo))) if isinstance(zz, (int, float)) else 0.0
        return {low: 1-t, high: t}
    return fn

def tex(name):
    im = Image.open(os.path.join(ROOT, name)).convert("RGB").resize((512, 512))
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

parts = []
def P(name, mat, w): p = Part(name, mat, w); parts.append(p); return p

skin = "skin_base_v1"
# head + neck volume (W1D7 visual fix: head floated on torso with no neck)
_head = P("head", skin, blend(None, 1.50, 1.58, "spine", "head"))
ellipsoid(_head, (0, 0, 1.655), (0.088, 0.10, 0.112), 24, 18)
limb(_head, (0, 0, 1.40), (0, 0, 1.60), 0.048, 0.042, 14)
ellipsoid(P("neck_torso_upper", skin, blend(None, 1.22, 1.40, "pelvis", "spine")), (0, 0, 1.37), (0.155, 0.112, 0.165), 24, 14)
ellipsoid(P("pelvis_lower", skin, blend(None, 1.02, 1.20, "pelvis", "spine")), (0, 0, 1.07), (0.16, 0.118, 0.155), 24, 14)
for side, sx in (("L", -1), ("R", 1)):
    ua, fa, th, sh = f"upperarm.{side}", f"forearm.{side}", f"thigh.{side}", f"shin.{side}"
    limb(P(f"upperarm.{side}", skin, lambda x, y, z, s=side: {"spine": max(0, (z-1.38)/0.14)*0.3 if z > 1.38 else 0, f"upperarm.{s}": 1-max(0, (z-1.38)/0.14)*0.3}), (sx*0.205, 0, 1.45), (sx*0.295, 0, 1.185), 0.050, 0.043, 18)
    ellipsoid(parts[-1], (sx*0.205, 0, 1.45), (0.058, 0.058, 0.058), 14, 10)   # shoulder joint volume
    limb(P(f"forearm_hand.{side}", skin, lambda x, y, z, s=side: {f"upperarm.{s}": max(0, (z-1.10)/0.16)*0.45 if z > 1.10 else 0, f"forearm.{s}": 1-(max(0, (z-1.10)/0.16)*0.45 if z > 1.10 else 0)}), (sx*0.295, 0, 1.185), (sx*0.335, 0, 0.945), 0.040, 0.030, 18)
    ellipsoid(parts[-2] if False else parts[-1], (sx*0.295, 0, 1.185), (0.046, 0.046, 0.046), 12, 8)  # elbow
    limb(P(f"thigh.{side}", skin, lambda x, y, z, s=side: {"pelvis": max(0, (z-0.82)/0.18)*0.4 if z > 0.82 else 0, f"thigh.{s}": 1-(max(0, (z-0.82)/0.18)*0.4 if z > 0.82 else 0)}), (sx*0.098, 0, 0.95), (sx*0.108, 0, 0.525), 0.072, 0.052, 18)
    limb(P(f"shin_foot.{side}", skin, lambda x, y, z, s=side: {f"thigh.{s}": max(0, (z-0.44)/0.16)*0.45 if z > 0.44 else 0, f"shin.{s}": 1-(max(0, (z-0.44)/0.16)*0.45 if z > 0.44 else 0)}), (sx*0.108, 0, 0.525), (sx*0.108, 0, 0.07), 0.050, 0.034, 18)
    ellipsoid(parts[-1], (sx*0.108, 0.048, 0.032), (0.042, 0.105, 0.028), 12, 8)  # foot
    ellipsoid(parts[-2], (sx*0.108, 0, 0.525), (0.056, 0.056, 0.056), 12, 8)      # knee (on shin part list order: knee added to thigh part below)

# costume + identity locks (unchanged placement from V1, verified vs composite)
ellipsoid(P("wrap_top_indigo", "cloth_indigo_plain_v1", blend(None, 1.24, 1.40, "pelvis", "spine")), (0, 0, 1.355), (0.172, 0.128, 0.148), 24, 12)
ellipsoid(P("skirt_wrap_indigo", "cloth_indigo_plain_v1", "pelvis"), (0, 0, 0.92), (0.182, 0.142, 0.235), 24, 12)
strap(P("baldric_L_to_R", "leather_baldric_v1", "spine"), (-0.128, 0.122, 1.465), (0.148, 0.112, 1.125), 0.034, 0.012)
for i, z in enumerate((1.40, 1.362, 1.324)):
    # W1D7 visual fix: coils ring AROUND the (vertical) upper arm -> default
    # Z-axis torus. axis='x' rendered them as vertical strips (see inspection).
    torus(P(f"armlet_coil{i+1}_L_plain", "bronze_armlet_plain_v1", "upperarm.L"), (-0.238, 0, z), 0.056, 0.0105, 20, 10)
# W1D7 visual fix: pendant faces forward (+Y) -> ring in XZ plane (axis='y');
# axis='x' showed the ring edge-on from the front / full circle from the side.
torus(P("pendant_spiral_FICTIONAL", "pendant_spiral_FICTIONAL_v1", "spine"), (0, 0.142, 1.30), 0.027, 0.0075, 20, 10, axis='y')
_cord = P("pendant_cord_master", "leather_baldric_v1", "spine")
limb(_cord, (-0.068, 0.10, 1.465), (0, 0.142, 1.328), 0.0055, 0.0055, 8)
limb(_cord, (0.068, 0.10, 1.465), (0, 0.142, 1.328), 0.0055, 0.0055, 8)
ellipsoid(P("hair_knot", "hair_v1", "head"), (0, -0.028, 1.795), (0.052, 0.052, 0.048), 14, 10)
for i, (x, z) in enumerate(((-0.048, 1.615), (-0.062, 1.575), (0.048, 1.615))):
    # W1D7 visual fix: braids read as rigid bars; thinner, seated on the head.
    limb(P(f"braid{i+1}", "hair_v1", "head"), (x, -0.062, 1.715), (x*1.15, -0.082, z), 0.010, 0.0075, 10)
for i in range(5):
    mat = "bronze_armlet_plain_v1" if i < 3 else "coral_bead_v1"
    ellipsoid(P(f"temple_bead_{i+1}_{'bronze' if i<3 else 'coral'}_L", mat, "head"), (-0.086, -0.042+i*0.0115, 1.698-i*0.0035), (0.0085,)*3, 8, 6)
ellipsoid(P("LOCK_scar_L_marker", "scar_marker_v1", "head"), (-0.060, 0.080, 1.660), (0.011, 0.005, 0.017), 10, 8)

MATS = {"skin_base_v1": (0.42, 0.27, 0.18), "cloth_indigo_plain_v1": (0.10, 0.12, 0.32),
        "leather_baldric_v1": (0.30, 0.19, 0.11), "bronze_armlet_plain_v1": (0.55, 0.36, 0.15),
        "pendant_spiral_FICTIONAL_v1": (0.55, 0.36, 0.15), "coral_bead_v1": (0.75, 0.30, 0.22),
        "hair_v1": (0.05, 0.04, 0.035), "scar_marker_v1": (0.30, 0.16, 0.12)}
TEXTURES = {"cloth_indigo_plain_v1": tex("T_ADANNA_IndigoCloth_BC_2048.png"),
            "leather_baldric_v1": tex("T_ADANNA_VegetLeather_BC_2048.png"),
            "bronze_armlet_plain_v1": tex("T_ADANNA_Bronze_BC_2048.png"),
            "pendant_spiral_FICTIONAL_v1": tex("T_ADANNA_Bronze_BC_2048.png")}

nv, tris = write_obj(os.path.join(OUT, "ADANNA_AD03_V2.obj"), parts, MATS)
write_glb(os.path.join(OUT, "ADANNA_AD03_V2.glb"), parts, MATS, TEXTURES, meta="AD-03 V2")
qc = {"asset": "ADANNA_AD03_V2", "supersedes": "ADANNA_AD03_V1 (history retained)",
      "tier": "refined production-intent model - NOT final character",
      "reference": "AD-02 SELECT A composite (frozen 2026-11-22); master = identity authority",
      "parts": len(parts), "verts": nv, "tris": tris, "joints": [n for n, _, _ in JOINTS],
      "weights": "blended LBS (<=4 influences) at neck/shoulder/elbow/waist/hip/knee",
      "textures_embedded_512": sorted(TEXTURES), "blade_scabbard": "NONE (CQ-9)",
      "identity_locks": ["scar_L marker", "armlet 3 plain coils L", "pendant FICTIONAL + master cord",
                          "3B+2C temple beads L", "baldric L->R", "high knot + 3 braids", "plain indigo"]}
json.dump(qc, open(os.path.join(OUT, "AD03_V2_QC.json"), "w"), indent=2)
print(json.dumps(qc, indent=2))
