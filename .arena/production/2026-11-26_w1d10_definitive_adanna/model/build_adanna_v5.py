#!/usr/bin/env python3
"""AD-03 V5 — DEFINITIVE ADANNA (2026-11-26, W1 D10). Built from the internally approved definitive concept (2026-11-26_w1d10_definitive_adanna/concept/), NOT a continuation of V4 appearance: cropped bandeau wrap top with bare midriff, folded skirt waistband, pendant on chest above wrap, leather sandals.
Procedural sculpt refinement of ADANNA_AD03_V2 (Blender unavailable in sandbox;
geometry authored in source, .blend regenerated via the Mac finisher package).
Changes vs V2:
 - Face: nose, brow band, lips, ears, dark eye insets (base facial modelling).
 - Hands: palm + 4 fingers + thumb per hand. Feet: toe caps.
 - Joints: shoulder/elbow/knee joint SPHERES removed (caused scalloped ridges);
   limbs now 6-ring tapered profiles for continuous transitions.
 - Garments: intersecting ellipsoid shells REPLACED by lathe construction —
   wrap top and flared skirt with cloth folds, hem rings, torso-following radii;
   baldric kept as strap with edge thickness; pendant = 2-ring spiral stack.
 - Identity locks unchanged (scar L marker, 3 plain coils L, pendant FICTIONAL,
   3B+2C beads L, baldric L->R, knot + braids, plain indigo). No blade/scabbard.
Same skeleton, bone names, scale (~1.80 m) and material slots as V2.
"""
import io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "2026-11-23_w1d7_production", "pipeline"))
from charbuild import Part, ellipsoid, limb, torus, strap, box, lathe, hand, toes, write_obj, write_glb, JOINTS
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "2026-11-20_w1d4_research", "textures"))
OUT = os.path.join(HERE, "..", "out"); os.makedirs(OUT, exist_ok=True)

def blend(zlo, zhi, low, high):
    return lambda x, y, zz: {low: 1-max(0.0, min(1.0, (zz-zlo)/(zhi-zlo))), high: max(0.0, min(1.0, (zz-zlo)/(zhi-zlo)))}
def prox_blend(z_joint, prox, main, amt=0.45, span=0.14):
    """Descending-limb weights: `main` bone owns the segment; `prox` (the joint
    above) fades in only within `span` below the joint, up to `amt`.
    REGRESSION GUARD (2026-11-25): V3's first build reused blend() here, which
    inverted influence (forearm owned 16 verts / 0.054 m leverage -> Blender
    pose test delta 0.0). Never use blend() on limb segments."""
    def fn(x, y, zz):
        t = max(0.0, min(1.0, (zz-(z_joint-span))/span)) * amt if zz < z_joint else amt
        return {prox: t, main: 1-t}
    return fn
def tex(name):
    im = Image.open(os.path.join(ROOT, name)).convert("RGB").resize((512, 512))
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

parts = []
def P(name, mat, w): p = Part(name, mat, w); parts.append(p); return p
skin = "skin_base_v1"

_head = P("head", skin, blend(1.50, 1.58, "spine", "head"))
ellipsoid(_head, (0, 0, 1.655), (0.088, 0.100, 0.112), 28, 20)
ellipsoid(_head, (0, -0.014, 1.590), (0.056, 0.064, 0.046), 20, 12)          # jaw/chin (M2 softened)
limb(_head, (0, 0, 1.40), (0, 0, 1.60), 0.048, 0.042, 16)                    # neck
ellipsoid(P("nose", skin, "head"), (0, 0.096, 1.638), (0.015, 0.020, 0.024), 12, 8)
ellipsoid(P("brow", skin, "head"), (0, 0.078, 1.690), (0.052, 0.013, 0.009), 14, 8)  # M2 softened brow
ellipsoid(P("lips", "lips_v1", "head"), (0, 0.088, 1.600), (0.020, 0.010, 0.008), 12, 8)
for sx in (-1, 1):
    ellipsoid(P(f"eye_{'L' if sx<0 else 'R'}", "eye_dark_v1", "head"), (sx*0.033, 0.089, 1.662), (0.011, 0.006, 0.007), 10, 6)
    ellipsoid(P(f"ear_{'L' if sx<0 else 'R'}", skin, "head"), (sx*0.089, -0.002, 1.655), (0.010, 0.016, 0.022), 10, 8)

ellipsoid(P("neck_torso_upper", skin, blend(1.22, 1.40, "pelvis", "spine")), (0, 0, 1.37), (0.155, 0.112, 0.165), 28, 16)
ellipsoid(P("pelvis_lower", skin, blend(1.02, 1.20, "pelvis", "spine")), (0, 0, 1.07), (0.160, 0.118, 0.155), 28, 16)
for side, sx in (("L", -1), ("R", 1)):
    ua = P(f"upperarm.{side}", skin, prox_blend(1.45, "spine", f"upperarm.{side}", amt=0.30, span=0.12))
    limb(ua, (sx*0.205, 0, 1.45), (sx*0.295, 0, 1.185), 0.050, 0.043, 20, rings_n=6)
    ellipsoid(ua, (sx*0.205, 0, 1.45), (0.056, 0.056, 0.056), 16, 12)
    fa = P(f"forearm_hand.{side}", skin, prox_blend(1.185, f"upperarm.{side}", f"forearm.{side}", amt=0.45, span=0.14))
    limb(fa, (sx*0.295, 0, 1.185), (sx*0.335, 0, 0.945), 0.040, 0.030, 20, rings_n=6)
    hand(fa, (sx*0.337, 0, 0.945), sx)
    th = P(f"thigh.{side}", skin, prox_blend(0.95, "pelvis", f"thigh.{side}", amt=0.40, span=0.16))
    limb(th, (sx*0.098, 0, 0.95), (sx*0.108, 0, 0.525), 0.072, 0.052, 20, rings_n=6)
    sh = P(f"shin_foot.{side}", skin, prox_blend(0.525, f"thigh.{side}", f"shin.{side}", amt=0.45, span=0.14))
    limb(sh, (sx*0.108, 0, 0.525), (sx*0.108, 0, 0.07), 0.050, 0.034, 20, rings_n=6)
    ellipsoid(sh, (sx*0.108, 0.048, 0.032), (0.042, 0.105, 0.028), 14, 10)
    toes(sh, (sx*0.108, 0.048, 0.030))
    _sd = P(f"sandal.{side}", "leather_baldric_v1", f"shin.{side}")
    box(_sd, sx*0.108, 0.052, 0.006, 0.088, 0.225, 0.010)          # sole
    box(_sd, sx*0.108, 0.075, 0.038, 0.080, 0.030, 0.008)          # forefoot strap

# --- garments: lathe construction with folds + hems (no ellipsoid shells) ---
wrap = P("wrap_top_indigo", "cloth_indigo_plain_v1", blend(1.24, 1.40, "pelvis", "spine"))  # V5: cropped bandeau per definitive concept; bare midriff 1.13-1.24
# M2: elliptical plan (torso aspect), hem lips top/bottom, bottom overlaps skirt top (no waist gap)
lathe(wrap, [(0.158, 0.119, 1.275), (0.154, 0.116, 1.292), (0.168, 0.128, 1.335), (0.172, 0.131, 1.385), (0.164, 0.124, 1.408), (0.148, 0.110, 1.420), (0.152, 0.113, 1.430)], 28, fold_amp=0.022, fold_n=7, cap_top=False, cap_bot=False)
skirt = P("skirt_wrap_indigo", "cloth_indigo_plain_v1", "pelvis")
# M2: elliptical plan, folded hem lip at bottom, top tucks under wrap (overlap zone 1.13-1.20)
lathe(skirt, [(0.216, 0.163, 0.652), (0.212, 0.160, 0.668), (0.204, 0.154, 0.80), (0.192, 0.145, 0.95), (0.184, 0.139, 1.04), (0.191, 0.145, 1.095), (0.195, 0.148, 1.128), (0.189, 0.143, 1.152), (0.185, 0.140, 1.168)], 28, fold_amp=0.030, fold_n=9, cap_top=False, cap_bot=False)
# Baldric follows the garment surface (sculpt-gate fix: flat strap at fixed y
# was buried inside the circular wrap lathe; pendant likewise). Surface =
# wrap/skirt lathe radius profile; +6 mm stand-off.
import math as _m
_prof = [(1.128, 0.195, 0.148), (1.292, 0.154, 0.116), (1.335, 0.168, 0.128), (1.385, 0.172, 0.131), (1.43, 0.148, 0.110)]
def _surf_y(x, z):
    pr = _prof
    if z <= pr[0][0]: rx, ry = pr[0][1], pr[0][2]
    elif z >= pr[-1][0]: rx, ry = pr[-1][1], pr[-1][2]
    else:
        for (z0, ax, ay), (z1, bx, by) in zip(pr, pr[1:]):
            if z0 <= z <= z1:
                t = (z-z0)/(z1-z0); rx, ry = ax+(bx-ax)*t, ay+(by-ay)*t; break
    return ry*_m.sqrt(max(1-(x/rx)**2, 0.02)) + 0.006
_bal = P("baldric_L_to_R", "leather_baldric_v1", "spine")
_pts = []
for _i in range(9):
    _t = _i/8; _x = -0.118 + 0.256*_t; _z = 1.418 - 0.282*_t
    _pts.append((_x, _surf_y(_x, _z), _z))
for _a, _b in zip(_pts, _pts[1:]):
    strap(_bal, _a, _b, 0.036, 0.010)
# V5: baldric continues across the back (definitive concept back view)
_bpts = [(x, -y, z) for (x, y, z) in reversed(_pts)]
for _a, _b in zip(_bpts, _bpts[1:]):
    strap(_bal, _a, _b, 0.036, 0.010)
for i, z in enumerate((1.40, 1.362, 1.324)):
    torus(P(f"armlet_coil{i+1}_L_plain", "bronze_armlet_plain_v1", "upperarm.L"), (-0.238, 0, z), 0.056, 0.0105, 20, 10)
pend = P("pendant_spiral_FICTIONAL", "pendant_spiral_FICTIONAL_v1", "spine")
torus(pend, (0, 0.107, 1.448), 0.028, 0.0075, 20, 10, axis='y')
torus(pend, (0, 0.109, 1.446), 0.017, 0.006, 16, 8, axis='y')   # inner spiral turn
_cord = P("pendant_cord_master", "leather_baldric_v1", "spine")
limb(_cord, (-0.050, 0.040, 1.532), (0, 0.105, 1.472), 0.0055, 0.0055, 8)
limb(_cord, (0.050, 0.040, 1.532), (0, 0.105, 1.472), 0.0055, 0.0055, 8)
ellipsoid(P("hair_knot", "hair_v1", "head"), (0, -0.028, 1.795), (0.052, 0.052, 0.048), 16, 12)
for i, (x, z) in enumerate(((-0.048, 1.615), (-0.062, 1.575), (0.048, 1.615))):
    limb(P(f"braid{i+1}", "hair_v1", "head"), (x, -0.062, 1.715), (x*1.15, -0.082, z), 0.010, 0.0075, 10)
for i in range(5):
    mat = "bronze_armlet_plain_v1" if i < 3 else "coral_bead_v1"
    ellipsoid(P(f"temple_bead_{i+1}_{'bronze' if i<3 else 'coral'}_L", mat, "head"), (-0.086, -0.042+i*0.0115, 1.698-i*0.0035), (0.0085,)*3, 8, 6)
ellipsoid(P("LOCK_scar_L_marker", "scar_marker_v1", "head"), (-0.060, 0.082, 1.660), (0.011, 0.005, 0.017), 10, 8)

MATS = {"skin_base_v1": (0.42, 0.27, 0.18), "cloth_indigo_plain_v1": (0.10, 0.12, 0.32),
        "leather_baldric_v1": (0.30, 0.19, 0.11), "bronze_armlet_plain_v1": (0.55, 0.36, 0.15),
        "pendant_spiral_FICTIONAL_v1": (0.55, 0.36, 0.15), "coral_bead_v1": (0.75, 0.30, 0.22),
        "hair_v1": (0.05, 0.04, 0.035), "scar_marker_v1": (0.30, 0.16, 0.12),
        "lips_v1": (0.36, 0.16, 0.13), "eye_dark_v1": (0.03, 0.02, 0.02)}
TEXTURES = {"cloth_indigo_plain_v1": tex("T_ADANNA_IndigoCloth_BC_2048.png"),
            "leather_baldric_v1": tex("T_ADANNA_VegetLeather_BC_2048.png"),
            "bronze_armlet_plain_v1": tex("T_ADANNA_Bronze_BC_2048.png"),
            "pendant_spiral_FICTIONAL_v1": tex("T_ADANNA_Bronze_BC_2048.png")}
nv, tris = write_obj(os.path.join(OUT, "ADANNA_AD03_V5.obj"), parts, MATS)
write_glb(os.path.join(OUT, "ADANNA_AD03_V5.glb"), parts, MATS, TEXTURES, meta="AD-03 V5 definitive Adanna (concept-approved 2026-11-26)")
qc = {"asset": "ADANNA_AD03_V5", "milestone": "DEFINITIVE Adanna from internally approved concept 2026-11-26 (cropped wrap/bare midriff/waistband/pendant-on-chest/sandals)",
      "supersedes": "ADANNA_AD03_V4 (sculpt milestone 2, recoverable); V3 remains milestone-1 qualified fallback",
      "tier": "sculpt-refined production-intent - NOT final character",
      "parts": len(parts), "verts": nv, "tris": tris, "skeleton": "HUMAN_BASE_PROPOSED unchanged (11 joints, same names)",
      "changes": ["face: nose/brow/lips/ears/eyes/jaw", "hands: palm+fingers+thumb", "feet: toes",
                  "joints: spheres removed, 6-ring limb profiles", "garments: folded lathe wrap+skirt with hems (no ellipsoid shells)",
                  "pendant: 2-ring spiral"], "blade_scabbard": "NONE (CQ-9)"}
json.dump(qc, open(os.path.join(OUT, "AD03_V5_QC.json"), "w"), indent=2)
print(json.dumps(qc, indent=2))
