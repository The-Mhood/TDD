#!/usr/bin/env python3
"""GUARD CLASS V3 — SCULPT MILESTONE 2 (2026-11-25, W1 D9). Same treatment as
Adanna V3: face volumes, hands/fingers, toes, joint spheres removed (6-ring
limbs), garments as folded lathes (one-shoulder wrap approximated by offset
lathe + shoulder drape strap, flared skirt), sash as close ellipsoid band
(retained from gate fix), sandals with sole + toe strap. Generic unnamed
guard-class, unarmed, no emblems/markings. Same skeleton/scale as V1.
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
def tex(name):
    im = Image.open(os.path.join(ROOT, name)).convert("RGB").resize((512, 512))
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

parts = []
def P(name, mat, w): p = Part(name, mat, w); parts.append(p); return p
skin = "skin_guard_v1"; S = 1.14
_gh = P("head_generic", skin, blend(1.50, 1.58, "spine", "head"))
ellipsoid(_gh, (0, 0, 1.66), (0.092, 0.103, 0.115), 28, 20)
ellipsoid(_gh, (0, -0.013, 1.596), (0.058, 0.066, 0.047), 20, 12)  # M2 softened jaw
limb(_gh, (0, 0, 1.42), (0, 0, 1.62), 0.050, 0.044, 16)
ellipsoid(P("nose_g", skin, "head"), (0, 0.099, 1.645), (0.016, 0.021, 0.025), 12, 8)
ellipsoid(P("brow_g", skin, "head"), (0, 0.081, 1.697), (0.054, 0.014, 0.010), 14, 8)  # M2 softened brow
for sx in (-1, 1):
    ellipsoid(P(f"eye_g_{'L' if sx<0 else 'R'}", "eye_dark_v1", "head"), (sx*0.034, 0.092, 1.668), (0.011, 0.006, 0.007), 10, 6)
    ellipsoid(P(f"ear_g_{'L' if sx<0 else 'R'}", skin, "head"), (sx*0.093, -0.002, 1.662), (0.010, 0.016, 0.022), 10, 8)
ellipsoid(P("torso_upper", skin, blend(1.22, 1.40, "pelvis", "spine")), (0, 0, 1.37), (0.175*S, 0.120, 0.165), 28, 16)
ellipsoid(P("pelvis_lower", skin, blend(1.02, 1.20, "pelvis", "spine")), (0, 0, 1.07), (0.175*S, 0.125, 0.155), 28, 16)
for side, sx in (("L", -1), ("R", 1)):
    ua = P(f"upperarm.{side}", skin, f"upperarm.{side}")
    limb(ua, (sx*0.235*S, 0, 1.45), (sx*0.325*S, 0, 1.185), 0.058, 0.049, 20, rings_n=6)
    ellipsoid(ua, (sx*0.235*S, 0, 1.45), (0.068, 0.068, 0.068), 16, 12)
    fa = P(f"forearm_hand.{side}", skin, f"forearm.{side}")
    limb(fa, (sx*0.325*S, 0, 1.185), (sx*0.365*S, 0, 0.945), 0.046, 0.034, 20, rings_n=6)
    hand(fa, (sx*0.367*S, 0, 0.945), sx)
    th = P(f"thigh.{side}", skin, f"thigh.{side}")
    limb(th, (sx*0.108, 0, 0.95), (sx*0.118, 0, 0.525), 0.080, 0.058, 20, rings_n=6)
    sh = P(f"shin_sandal.{side}", skin, f"shin.{side}")
    limb(sh, (sx*0.118, 0, 0.525), (sx*0.118, 0, 0.07), 0.056, 0.038, 20, rings_n=6)
    ellipsoid(sh, (sx*0.118, 0.048, 0.030), (0.046, 0.108, 0.026), 14, 10)
    toes(sh, (sx*0.118, 0.048, 0.028))
    sd = P(f"sandal.{side}", "leather_baldric_v1", f"shin.{side}")
    ellipsoid(sd, (sx*0.118, 0.048, 0.012), (0.048, 0.112, 0.010), 14, 8)
    box(sd, sx*0.118, 0.075, 0.030, 0.055, 0.016, 0.012)  # toe strap
wrap = P("wrap_oneshoulder_indigo", "cloth_indigo_plain_v1", blend(1.24, 1.40, "pelvis", "spine"))
# M2: genuine one-shoulder construction - elliptical lathe with slanted top edge
# (rises 0.10 m over the anatomical LEFT shoulder, -X), hem lip at bottom.
lathe(wrap, [(0.220, 0.148, 1.188), (0.216, 0.145, 1.205), (0.218, 0.146, 1.32), (0.210, 0.141, 1.42), (0.196, 0.130, 1.485)], 28, fold_amp=0.020, fold_n=7, cap_top=False, cap_bot=False, slant=-0.075)
skirt = P("skirt_wrap_indigo", "cloth_indigo_plain_v1", "pelvis")
# M2: elliptical plan, hem lip, top overlaps wrap bottom (no waist gap)
lathe(skirt, [(0.254, 0.193, 0.652), (0.250, 0.190, 0.668), (0.238, 0.180, 0.82), (0.224, 0.168, 0.98), (0.220, 0.165, 1.12), (0.222, 0.166, 1.20)], 28, fold_amp=0.028, fold_n=9, cap_top=False, cap_bot=False)
_sash = P("waist_sash_plain", "cloth_sash_undyed_v1", "pelvis")
lathe(_sash, [(0.230, 0.174, 1.022), (0.233, 0.176, 1.058), (0.230, 0.174, 1.094)], 28, fold_amp=0.0, cap_top=False, cap_bot=False)  # M2: narrower (72mm) elliptical band, proud of skirt
torus(P("armband_plain_bronze_R", "bronze_plain_v1", "upperarm.R"), (0.275*S, 0, 1.36), 0.062, 0.012, 20, 10)

MATS = {"skin_guard_v1": (0.36, 0.22, 0.14), "cloth_indigo_plain_v1": (0.10, 0.12, 0.32),
        "cloth_sash_undyed_v1": (0.62, 0.55, 0.42), "bronze_plain_v1": (0.55, 0.36, 0.15),
        "leather_baldric_v1": (0.30, 0.19, 0.11), "eye_dark_v1": (0.03, 0.02, 0.02)}
TEXTURES = {"cloth_indigo_plain_v1": tex("T_ADANNA_IndigoCloth_BC_2048.png"),
            "bronze_plain_v1": tex("T_ADANNA_Bronze_BC_2048.png"),
            "leather_baldric_v1": tex("T_ADANNA_VegetLeather_BC_2048.png")}
nv, tris = write_obj(os.path.join(OUT, "GUARD_CLASS_V3.obj"), parts, MATS)
write_glb(os.path.join(OUT, "GUARD_CLASS_V3.glb"), parts, MATS, TEXTURES, meta="GUARD V3 sculpt milestone 2")
qc = {"asset": "GUARD_CLASS_V3", "milestone": "sculpt 2 (one-shoulder wrap/elliptical/sash/face soften)", "supersedes": "GUARD_CLASS_V2 (milestone-1 qualified, recoverable)",
      "tier": "sculpt-refined production-intent - NOT final", "parts": len(parts), "verts": nv, "tris": tris,
      "skeleton": "HUMAN_BASE_PROPOSED unchanged", "weapons_emblems_markings": "NONE"}
json.dump(qc, open(os.path.join(OUT, "GUARD_V3_QC.json"), "w"), indent=2)
print(json.dumps(qc, indent=2))
