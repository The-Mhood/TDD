#!/usr/bin/env python3
"""ROYAL GUARD (unnamed guard-class) V1 model (2026-11-23, W1 D7).
Built on the shared charbuild pipeline + HUMAN_BASE skeleton (same joint names
as Adanna -> shared animation set). From RG_V003_GUARD_CLASS_TARGET.jpg
(owner-selected, verified). Generic adult man, broader proportions (~1.15x
Adanna shoulder width in geometry), one-shoulder indigo wrap, plain waist sash,
plain bronze armband (RIGHT arm, no motifs/insignia claim), sandals.
NO weapons, NO shield, NO disc/coral mark, NO text, no invented identities.
Tier: production-intent base model - NOT final; same Blender finish path as AD-03.
"""
import io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
from charbuild import Part, ellipsoid, limb, torus, strap, write_obj, write_glb, JOINTS
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "2026-11-20_w1d4_research", "textures"))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

def blend(zlo, zhi, low, high):
    return lambda x, y, zz: {low: 1-max(0.0, min(1.0, (zz-zlo)/(zhi-zlo))), high: max(0.0, min(1.0, (zz-zlo)/(zhi-zlo)))}
def tex(name):
    im = Image.open(os.path.join(ROOT, name)).convert("RGB").resize((512, 512))
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()

parts = []
def P(name, mat, w): p = Part(name, mat, w); parts.append(p); return p
skin = "skin_guard_v1"; S = 1.14  # shoulder breadth factor vs Adanna profile
_ghead = P("head_generic", skin, blend(1.50, 1.58, "spine", "head"))
ellipsoid(_ghead, (0, 0, 1.66), (0.092, 0.103, 0.115), 24, 18)
limb(_ghead, (0, 0, 1.42), (0, 0, 1.62), 0.050, 0.044, 14)  # neck (visual fix: head floated)
ellipsoid(P("torso_upper", skin, blend(1.22, 1.40, "pelvis", "spine")), (0, 0, 1.37), (0.175*S, 0.12, 0.165), 24, 14)
ellipsoid(P("pelvis_lower", skin, blend(1.02, 1.20, "pelvis", "spine")), (0, 0, 1.07), (0.175*S, 0.125, 0.155), 24, 14)
for side, sx in (("L", -1), ("R", 1)):
    _ua = P(f"upperarm.{side}", skin, f"upperarm.{side}")
    limb(_ua, (sx*0.235*S, 0, 1.45), (sx*0.325*S, 0, 1.185), 0.058, 0.049, 18)
    ellipsoid(_ua, (sx*0.235*S, 0, 1.45), (0.068, 0.068, 0.068), 14, 10)  # shoulder volume (visual fix: arms detached)
    limb(P(f"forearm_hand.{side}", skin, f"forearm.{side}"), (sx*0.325*S, 0, 1.185), (sx*0.365*S, 0, 0.945), 0.046, 0.034, 18)
    limb(P(f"thigh.{side}", skin, f"thigh.{side}"), (sx*0.108, 0, 0.95), (sx*0.118, 0, 0.525), 0.080, 0.058, 18)
    limb(P(f"shin_sandal.{side}", skin, f"shin.{side}"), (sx*0.118, 0, 0.525), (sx*0.118, 0, 0.07), 0.056, 0.038, 18)
    ellipsoid(parts[-1], (sx*0.118, 0.048, 0.030), (0.046, 0.108, 0.026), 12, 8)
# costume: one-shoulder wrap (covers anatomical LEFT shoulder/torso), skirt, sash, armband R
ellipsoid(P("wrap_oneshoulder_indigo", "cloth_indigo_plain_v1", blend(1.24, 1.40, "pelvis", "spine")), (-0.03, 0, 1.35), (0.185*S, 0.135, 0.155), 24, 12)
ellipsoid(P("skirt_wrap_indigo", "cloth_indigo_plain_v1", "pelvis"), (0, 0, 0.90), (0.195*S, 0.15, 0.25), 24, 12)
# W1D7 re-inspection fix: a circular torus sash protruded as a disc (skirt
# cross-section at sash height is elliptical ~0.171 x 0.115 m). Flattened
# ellipsoid band hugs the skirt (protrudes ~0.02 m uniformly = wrapped cloth).
ellipsoid(P("waist_sash_plain", "cloth_sash_undyed_v1", "pelvis"), (0, 0, 1.06), (0.188, 0.138, 0.038), 24, 10)
# visual fix: ring around the vertical arm (default Z axis), not axis='x' strip
torus(P("armband_plain_bronze_R", "bronze_plain_v1", "upperarm.R"), (0.275*S, 0, 1.36), 0.062, 0.012, 20, 10)
for side, sx in (("L", -1), ("R", 1)):  # sandal soles
    ellipsoid(P(f"sandal_sole.{side}", "leather_baldric_v1", f"shin.{side}"), (sx*0.118, 0.048, 0.012), (0.048, 0.112, 0.010), 12, 6)

MATS = {"skin_guard_v1": (0.36, 0.22, 0.14), "cloth_indigo_plain_v1": (0.10, 0.12, 0.32),
        "cloth_sash_undyed_v1": (0.62, 0.55, 0.42), "bronze_plain_v1": (0.55, 0.36, 0.15),
        "leather_baldric_v1": (0.30, 0.19, 0.11)}
TEXTURES = {"cloth_indigo_plain_v1": tex("T_ADANNA_IndigoCloth_BC_2048.png"),
            "bronze_plain_v1": tex("T_ADANNA_Bronze_BC_2048.png"),
            "leather_baldric_v1": tex("T_ADANNA_VegetLeather_BC_2048.png")}
nv, tris = write_obj(os.path.join(OUT, "GUARD_CLASS_V1.obj"), parts, MATS)
write_glb(os.path.join(OUT, "GUARD_CLASS_V1.glb"), parts, MATS, TEXTURES, meta="GUARD V1")
qc = {"asset": "GUARD_CLASS_V1", "source_visual": "RG_V003_GUARD_CLASS_TARGET.jpg (verified 2026-11-22)",
      "tier": "production-intent base model - NOT final", "parts": len(parts), "verts": nv, "tris": tris,
      "skeleton": "HUMAN_BASE_PROPOSED (shared with AD-03)", "weapons_emblems_markings": "NONE",
      "proportions": "shoulder breadth x1.14 vs Adanna V2 profile (class readability)"}
json.dump(qc, open(os.path.join(OUT, "GUARD_V1_QC.json"), "w"), indent=2)
print(json.dumps(qc, indent=2))
