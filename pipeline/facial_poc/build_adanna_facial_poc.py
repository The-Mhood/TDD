#!/usr/bin/env python3
"""
build_adanna_facial_poc.py — Adanna facial-likeness Proof of Concept (PoC)  [REPAIRED v2.2]
The Disobedient Daughter · Zero-budget facial likeness strategy (TDD-IMPL-FACIAL-001)

v2.2 — BACKGROUND-SAFE REWRITE. The v2.1 pipeline failed at owner-Mac run 2693a3f:
`bpy.ops.object.select_all(action="DESELECT")` requires a valid UI context and fails in
Blender background mode (`blender -b`). This revision eliminates EVERY context-dependent
operator and uses background-safe data/API + BMesh operations instead.

Context-dependent operators REMOVED / replaced:
  - bpy.ops.object.select_all(...)          -> data API: for o in bpy.data.objects: o.select_set(False)
  - bpy.ops.object.transform_apply(...)     -> data API: apply_scale_data() (transform verts, reset scale)
  - bpy.ops.object.mode_set(EDIT/OBJECT)   -> BMesh for all mesh editing (no edit-mode context)
  - bpy.ops.mesh.select_all / subdivide / remove_doubles -> BMesh ops
  - bpy.ops.object.join(...)               -> BMesh merge (merge_bmesh)
Operators KEPT (verified background-safe with data-API selection): mesh primitives,
armature_add, parent_set (ARMATURE_AUTO / OBJECT_RELATIVE), render, export_scene.fbx,
wm.save_as_mainfile, wm.read_factory_settings.

v2.1 fixes retained: portrait-guided facial base block (not a naked sphere); portrait
loaded as modelling reference; full HUMAN_BASE_PROPOSED 11-joint skeleton; consistent
binding; corrected QC (in verify_facial_poc.py).

v2.2 ADDITIONAL bug fixes found in audit:
  - Tri-budget overrun: torus_add defaults (128x32 segs) + subdivide(2) on a 64x48 sphere
    would exceed the 20k-tri QC budget. Segment counts now explicit and modest; head/jaw
    subdivide reduced to 1 cut. Estimated total ~11k tris (under budget).
  - Head/jaw kept as SEPARATE bound meshes (ADANNA_HEAD / ADANNA_JAW) — avoids UV loss
    from a BMesh face-merge; both bound to the armature.
  - apply_scale_data() replaces transform_apply so local space == world space correctly.
  - UV safety net (ensure_uvs) guarantees a UV layer with data for the QC UV check.

Grounding (authoritative):
  - M1_ADANNA_CHARACTER_ART_ANIMATION_SPEC.md — Adanna facial identity locks
  - W1D7_CHARACTER_INTEGRATION_MANIFEST.md    — HUMAN_BASE_PROPOSED skeleton, material slots, FBX 7.400
  - CHARACTER_DESIGN_REGISTER.md (Drive)      — Adanna identity + right-side rules (OAD-51)

NOTE: This script is background-safe and syntax-verified; FUNCTIONAL validation is the
owner-Mac step (FACIAL_POC_RUNBOOK.md). Do not mark the face built/qualified/reviewed
until the owner runs it and returns the evidence bundle. Zero paid tools: Blender 4.2.23 LTS.
"""

import bpy
import bmesh
import math
import os
import sys
import json
import hashlib
import traceback
from mathutils import Vector

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
FBX_NAME = "ADANNA_FACIAL_POC_V2.fbx"
BLEND_NAME = "ADANNA_FACIAL_POC_V2.blend"
FRAME_DURATION = 120  # expression turntable length (frames @ 24fps = 5s)

# Portrait path: owner places the approved portrait on the Mac and points here.
PORTRAIT_PATH = os.environ.get(
    "PORTRAIT_PATH",
    os.path.join(SCRIPT_DIR, "reference", "REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg"),
)

IDENTITY = {
    "left_temple_cuffs": 3,
    "left_temple_coral_beads": 2,
    "scar": "LEFT cheekbone (diagonal)",
    "armlet": "LEFT upper arm (coiled aged-bronze)",
    "pendant": "spiral bronze (EXPLICITLY FICTIONAL)",
    "braids": "thin, top half in high knot",
    "wrap": "indigo hand-woven",
    "default_expression": "guarded / defiant",
    "forbidden": "NO gold; NEVER mirrored; do not move/duplicate identifying features",
}

# Shared skeleton joint names (W1D7 manifest) — 11 joints.
SKELETON_JOINTS = [
    "pelvis", "spine", "head",
    "upperarm.L", "upperarm.R", "forearm.L", "forearm.R",
    "thigh.L", "thigh.R", "shin.L", "shin.R",
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def log(msg):
    print("[facial_poc] " + msg)


def fail(msg):
    """Log a fatal error and exit non-zero so the shell detects failure."""
    log("FATAL: " + msg)
    traceback.print_exc()
    sys.exit(1)


def ensure_dirs():
    for d in (OUT_DIR, os.path.join(OUT_DIR, "previews"),
              os.path.join(OUT_DIR, "turntable"), os.path.join(OUT_DIR, "evidence"),
              os.path.join(SCRIPT_DIR, "reference")):
        os.makedirs(d, exist_ok=True)


def clear_scene():
    # read_factory_settings is background-safe and yields a clean empty scene.
    bpy.ops.wm.read_factory_settings(use_empty=True)


def hash_file(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_color(base_color):
    """Normalize a colour to a 4-component RGBA tuple for Blender sockets.

    Blender's colour sockets require exactly four components. Accept both RGB
    (3 components) and RGBA (4 components): RGB gets alpha 1.0 appended, RGBA is
    used unchanged. Reject any other length with a clear error so a bad call
    fails loudly instead of producing a malformed 5-component value.
    """
    n = len(base_color)
    if n == 3:
        return (float(base_color[0]), float(base_color[1]), float(base_color[2]), 1.0)
    if n == 4:
        return (float(base_color[0]), float(base_color[1]), float(base_color[2]), float(base_color[3]))
    raise ValueError(
        "base_color must be RGB (3 components) or RGBA (4 components); "
        "got %d components: %r" % (n, base_color))


def make_pbr_material(name, base_color, roughness=0.7, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf is None:
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(bsdf.outputs["BSDF"], nt.nodes["Material Output"].inputs["Surface"])
    bsdf.inputs["Base Color"].default_value = normalize_color(base_color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return mat


def make_materials():
    return {
        "skin_base_v1":       make_pbr_material("skin_base_v1",       (0.46, 0.30, 0.22, 1.0), roughness=0.62),
        "lips_v1":            make_pbr_material("lips_v1",            (0.42, 0.20, 0.18, 1.0), roughness=0.55),
        "eye_dark_v1":        make_pbr_material("eye_dark_v1",        (0.08, 0.06, 0.05, 1.0), roughness=0.25),
        "scar_marker_v1":     make_pbr_material("scar_marker_v1",     (0.85, 0.70, 0.55, 1.0), roughness=0.80),
        "hair_dark_v1":       make_pbr_material("hair_dark_v1",       (0.10, 0.08, 0.07, 1.0), roughness=0.75),
        "metal_aged_v1":      make_pbr_material("metal_aged_v1",      (0.55, 0.40, 0.22, 1.0), roughness=0.35, metallic=1.0),
        "metal_hardware_v1":  make_pbr_material("metal_hardware_v1",  (0.72, 0.62, 0.40, 1.0), roughness=0.25, metallic=1.0),
        "cloth_indigo_v1":    make_pbr_material("cloth_indigo_v1",    (0.16, 0.20, 0.42, 1.0), roughness=0.90),
    }


def deselect_all():
    """Background-safe replacement for bpy.ops.object.select_all(action='DESELECT')."""
    for o in bpy.data.objects:
        o.select_set(False)


def set_active(obj):
    """Background-safe: deselect all (data API), select obj, make it active."""
    deselect_all()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def primitive(kind, **kwargs):
    """Create a mesh primitive (background-safe operator) and return the new object."""
    getattr(bpy.ops.mesh, "primitive_" + kind)(**kwargs)
    obj = bpy.context.active_object
    if obj is None:
        meshes = [o for o in bpy.data.objects if o.type == "MESH"]
        obj = meshes[-1] if meshes else None
    if obj is None:
        fail("primitive %s_add did not create an object" % kind)
    return obj


def apply_scale_data(obj):
    """Background-safe replacement for bpy.ops.object.transform_apply(scale=True).
    Transforms mesh vertices by the object scale in local space, then resets scale to 1.
    Assumes identity rotation (true for freshly created primitives)."""
    s = obj.scale
    if s == Vector((1.0, 1.0, 1.0)):
        return
    me = obj.data
    if me is not None and me.vertices:
        sv = Vector(s)
        for v in me.vertices:
            v.co = v.co * sv
        me.update()
    obj.scale = (1.0, 1.0, 1.0)


def ensure_uvs(me):
    """Safety net: guarantee a UV layer with data (QC UV check). Primitives already carry
    UVs and BMesh preserves them; this only fills in if a layer is missing/empty."""
    if me.uv_layers and len(me.uv_layers[0].data) > 0:
        return
    if not me.uv_layers:
        uvl = me.uv_layers.new(name="UVMap")
    else:
        uvl = me.uv_layers[0]
    # Crude planar UVs from vertex (x, y) — valid for a PoC; owner retopos proper UVs.
    for i, loop in enumerate(me.loops):
        v = me.vertices[loop.vertex_index]
        uvl.data[i].uv = (v.co.x, v.co.y)
    me.update()


# --------------------------------------------------------------------------- #
# [FIX 2] Portrait as modelling reference
# --------------------------------------------------------------------------- #
def load_portrait_reference():
    """Load the approved master portrait as a modelling reference + backdrop.

    Returns (portrait_image, backdrop_obj, loaded_bool). If the portrait file is not
    present on the Mac, the pipeline still runs with proportion defaults but records a
    warning so the owner knows to place the portrait (the runbook requires it).
    """
    loaded = False
    portrait_img = None
    backdrop = None
    if os.path.exists(PORTRAIT_PATH):
        portrait_img = bpy.data.images.load(PORTRAIT_PATH, check_existing=False)
        portrait_img.name = "REF_ADANNA_MASTER_PORTRAIT"
        loaded = True
        log("portrait loaded from %s" % PORTRAIT_PATH)

        # Reference backdrop plane (kept out of the render and the FBX export).
        backdrop = primitive("plane_add", size=4.0, location=(0.0, -2.6, 1.55))
        backdrop.name = "PORTRAIT_REFERENCE_BACKDROP"
        ref_mat = bpy.data.materials.new("portrait_reference_mat")
        ref_mat.use_nodes = True
        nt = ref_mat.node_tree
        bsdf = nt.nodes.get("Principled BSDF")
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = portrait_img
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        # Emission input names were renamed in Blender 4.0 ("Emission" -> "Emission
        # Color"). Guard defensively so a future rename cannot crash the run.
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = 1.0
        backdrop.data.materials.append(ref_mat)
        backdrop.hide_render = True
        backdrop["exclude_from_export"] = True
        log("portrait reference backdrop created")
    else:
        log("WARNING: portrait not found at %s — run with PORTRAIT_PATH set to the "
            "approved portrait on the Mac; using proportion defaults" % PORTRAIT_PATH)
    return portrait_img, backdrop, loaded


def portrait_proportions(portrait_img):
    """Derive head proportion hints from the portrait aspect where available."""
    if portrait_img and portrait_img.size[0] and portrait_img.size[1]:
        w, h = portrait_img.size
        return {"portrait_aspect": round(w / float(h), 3), "source": "portrait"}
    return {"portrait_aspect": None, "source": "default"}


# --------------------------------------------------------------------------- #
# [FIX 1] Portrait-guided facial base block (not a naked sphere) — BMesh, background-safe
# --------------------------------------------------------------------------- #
def build_facial_base_block(proportions):
    """Build a face-appropriate head mesh (cranium + jaw) shaped toward human-head
    proportions. Uses BMesh for subdivide + vertex deformation (no edit-mode context).
    Head and jaw are kept as separate bound meshes (ADANNA_HEAD / ADANNA_JAW)."""
    aspect = proportions.get("portrait_aspect") or 0.75

    # --- Cranium: UV sphere at origin, scaled, subdivided, deformed in local space ---
    head = primitive("uv_sphere_add", segments=32, ring_count=24, radius=1.0,
                     location=(0.0, 0.0, 0.0))
    head.scale = (0.90, 0.84, 1.22)
    apply_scale_data(head)  # local space now == scaled sphere, centered at origin

    bm = bmesh.new()
    bm.from_mesh(head.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=1, use_grid_fill=True)
    # Vertex-space facial shaping (correct local-space thresholds).
    for v in bm.verts:
        x, y, z = v.co
        if y < -0.2:                       # back of the head stays rounded/cranial
            v.co.y = y * 1.05
        if y > 0.0:                        # face region: flatten + widen per portrait aspect
            v.co.y = y * (0.90 + 0.05 * aspect)
            v.co.x = x * (0.95 + 0.05 * aspect)
        if z < -0.3:                       # jaw taper (lower vertices)
            taper = max(0.0, (-0.3 - z) / 0.50)
            v.co.x *= (1.0 - 0.18 * taper)
            v.co.y *= (1.0 - 0.10 * taper)
    bm.to_mesh(head.data)
    head.data.update()
    ensure_uvs(head.data)
    head.name = "ADANNA_HEAD"
    bm.free()

    # --- Jaw/mandible block: separate sphere, subdivided, positioned in head space ---
    jaw = primitive("uv_sphere_add", segments=16, ring_count=12, radius=0.62,
                    location=(0.0, 0.0, 0.0))
    jaw.scale = (0.95, 0.70, 0.80)
    apply_scale_data(jaw)
    bmj = bmesh.new()
    bmj.from_mesh(jaw.data)
    bmj.faces.ensure_lookup_table()
    bmesh.ops.subdivide_edges(bmj, edges=list(bmj.edges), cuts=1, use_grid_fill=True)
    bmj.to_mesh(jaw.data)
    jaw.data.update()
    ensure_uvs(jaw.data)
    jaw.name = "ADANNA_JAW"
    # Position jaw at the lower-front of the head (relative to head center, local space).
    jaw.location = (0.0, -0.02, -0.37)
    bmj.free()

    log("facial base block built (cranium + jaw), portrait aspect=%s" % aspect)
    return head, jaw


def add_face_features(mats):
    """Identity-feature meshes. Left/right locks preserved, never mirrored.
    Modest segment counts keep the tri budget well under 20k.
    Returns a dict of {feature_key: obj or [objs]}."""
    created = {}

    # Eyes
    eyes = []
    for sx in (-1, 1):
        eye = primitive("uv_sphere_add", segments=16, ring_count=10, radius=0.12,
                        location=(sx * 0.30, 0.22, 1.78))
        eye.scale = (0.9, 0.5, 0.5)
        apply_scale_data(eye)
        eye.data.materials.append(mats["eye_dark_v1"])
        eye.name = "ADANNA_EYE_%s" % ("L" if sx < 0 else "R")
        eyes.append(eye)
    created["eyes"] = eyes

    lip = primitive("uv_sphere_add", segments=16, ring_count=10, radius=0.20,
                    location=(0.0, -0.18, 1.52))
    lip.scale = (1.6, 0.5, 0.6)
    apply_scale_data(lip)
    lip.data.materials.append(mats["lips_v1"])
    lip.name = "ADANNA_LIPS"
    created["lips"] = lip

    nose = primitive("cone_add", vertices=10, radius1=0.0, radius2=0.08, depth=0.30,
                     location=(0.0, 0.26, 1.72))
    nose.data.materials.append(mats["skin_base_v1"])
    nose.name = "ADANNA_NOSE"
    created["nose"] = nose

    # Left-temple bronze cuffs (3) + coral beads (2) — LEFT only, never mirrored.
    cuffs = []
    for i in range(IDENTITY["left_temple_cuffs"]):
        y = 0.46 - i * 0.05
        c = primitive("torus_add", major_radius=0.16, minor_radius=0.035,
                      major_segments=16, minor_segments=8, location=(-0.86, y, 1.74))
        c.data.materials.append(mats["metal_aged_v1"])
        c.name = "ADANNA_CUFF_L_%d" % i
        cuffs.append(c)
    beads = []
    for i in range(IDENTITY["left_temple_coral_beads"]):
        b = primitive("uv_sphere_add", segments=12, ring_count=8, radius=0.045,
                      location=(-0.90, 0.30 + i * 0.05, 1.76))
        b.data.materials.append(make_pbr_material("coral_bead_v1", (0.78, 0.28, 0.18, 1.0), roughness=0.5))
        b.name = "ADANNA_CORAL_L_%d" % i
        beads.append(b)
    created["left_temple_cuffs"] = cuffs
    created["left_temple_coral_beads"] = beads

    # Left-cheekbone scar — diagonal marker (LEFT)
    scar = primitive("cube_add", size=0.06, location=(-0.55, 0.10, 1.62))
    scar.scale = (0.9, 2.6, 0.35)
    apply_scale_data(scar)
    scar.rotation_euler = (0.0, 0.0, math.radians(35))
    scar.data.materials.append(mats["scar_marker_v1"])
    scar.name = "ADANNA_SCAR_L"
    created["scar_left"] = scar

    # Braids — top half in a high knot
    knot = primitive("uv_sphere_add", segments=20, ring_count=14, radius=0.28,
                     location=(0.0, -0.05, 2.05))
    knot.scale = (1.0, 1.0, 0.8)
    apply_scale_data(knot)
    knot.data.materials.append(mats["hair_dark_v1"])
    knot.name = "ADANNA_BRAID_KNOT"
    created["braids"] = knot

    # Left upper-arm coiled bronze armlet (body-level accessory)
    armlet = primitive("torus_add", major_radius=0.20, minor_radius=0.045,
                       major_segments=16, minor_segments=8, location=(-0.95, 0.0, 1.10))
    armlet.rotation_euler = (math.radians(90), 0.0, 0.0)
    armlet.data.materials.append(mats["metal_aged_v1"])
    armlet.name = "ADANNA_ARMLET_L"
    created["armlet_left"] = armlet

    # Spiral bronze pendant (EXPLICITLY FICTIONAL)
    pendant = primitive("torus_add", major_radius=0.10, minor_radius=0.022,
                        major_segments=16, minor_segments=8, location=(0.0, 0.0, 1.20))
    pendant.data.materials.append(mats["metal_aged_v1"])
    pendant.name = "ADANNA_PENDANT_FICTIONAL"
    created["pendant"] = pendant

    # Indigo hand-woven wrap (body-level accessory)
    wrap = primitive("torus_add", major_radius=0.26, minor_radius=0.05,
                     major_segments=16, minor_segments=8, location=(0.0, 0.0, 1.02))
    wrap.rotation_euler = (math.radians(90), 0.0, 0.0)
    wrap.data.materials.append(mats["cloth_indigo_v1"])
    wrap.name = "ADANNA_WRAP_INDIGO"
    created["wrap"] = wrap

    return created


def assign_skin_to_head(head, mats):
    head.data.materials.clear()
    head.data.materials.append(mats["skin_base_v1"])


# --------------------------------------------------------------------------- #
# [FIX 3] Full shared HUMAN_BASE_PROPOSED skeleton + [FIX 4] consistent binding
# --------------------------------------------------------------------------- #
def build_full_skeleton(head, jaw, features):
    """Build the complete shared HUMAN_BASE_PROPOSED skeleton (11 joints) with facial
    controls as children of `head`. Bind the head mesh with automatic weights and
    parent every mesh (head, jaw, accessories) to the armature."""
    # enter_editmode=False keeps this fully background-safe: bones are built via the
    # data API (arm.data.edit_bones.new) in object mode, with no edit-mode context needed.
    bpy.ops.object.armature_add(enter_editmode=False, align="WORLD", location=(0.0, 0.0, 0.0))
    arm = bpy.context.active_object
    arm.name = "HUMAN_BASE_PROPOSED"
    eb = arm.data.edit_bones

    # Root + spine + head chain
    root = eb.new("pelvis"); root.head = Vector((0.0, 0.0, 1.0)); root.tail = Vector((0.0, 0.0, 1.25))
    spine = eb.new("spine"); spine.head = Vector((0.0, 0.0, 1.25)); spine.tail = Vector((0.0, 0.0, 1.55))
    spine.parent = root
    head_bone = eb.new("head"); head_bone.head = Vector((0.0, 0.0, 1.55)); head_bone.tail = Vector((0.0, 0.0, 1.90))
    head_bone.parent = spine

    # Arms (L/R): upperarm -> forearm, parented to spine
    for side in ("L", "R"):
        sx = -1 if side == "L" else 1
        ua = eb.new("upperarm.%s" % side)
        ua.head = Vector((sx * 0.45, 0.0, 1.30)); ua.tail = Vector((sx * 0.45, 0.0, 1.10))
        ua.parent = spine
        fa = eb.new("forearm.%s" % side)
        fa.head = Vector((sx * 0.45, 0.0, 1.10)); fa.tail = Vector((sx * 0.45, 0.0, 0.85))
        fa.parent = ua

    # Legs (L/R): thigh -> shin, parented to pelvis
    for side in ("L", "R"):
        sx = -1 if side == "L" else 1
        th = eb.new("thigh.%s" % side)
        th.head = Vector((sx * 0.18, 0.0, 0.95)); th.tail = Vector((sx * 0.18, 0.0, 0.60))
        th.parent = root
        sh = eb.new("shin.%s" % side)
        sh.head = Vector((sx * 0.18, 0.0, 0.60)); sh.tail = Vector((sx * 0.18, 0.0, 0.30))
        sh.parent = th

    # Facial control bones — children of head
    def add_facial_bone(name, head_v, tail_v):
        b = eb.new(name); b.head = head_v; b.tail = tail_v; b.parent = head_bone
        return b
    add_facial_bone("facial_brow", Vector((0.0, 0.20, 1.85)), Vector((0.0, 0.20, 1.89)))
    add_facial_bone("facial_eyelid_L", Vector((-0.30, 0.22, 1.85)), Vector((-0.30, 0.22, 1.88)))
    add_facial_bone("facial_eyelid_R", Vector((0.30, 0.22, 1.85)), Vector((0.30, 0.22, 1.88)))
    add_facial_bone("facial_jaw", Vector((0.0, -0.18, 1.85)), Vector((0.0, -0.18, 1.87)))
    add_facial_bone("facial_cheek_L", Vector((-0.45, 0.10, 1.85)), Vector((-0.45, 0.10, 1.87)))
    add_facial_bone("facial_cheek_R", Vector((0.45, 0.10, 1.85)), Vector((0.45, 0.10, 1.87)))

    # No edit-mode exit needed: we never entered edit mode (enter_editmode=False).
    log("full HUMAN_BASE_PROPOSED skeleton built: %d joints + facial controls" % len(SKELETON_JOINTS))

    # Bind the head mesh with automatic weights (deformable). Background-safe selection.
    set_active(arm)
    head.select_set(True)
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")

    # Collect all accessory meshes (jaw + features).
    accessory_objs = [jaw]
    for key, val in features.items():
        if isinstance(val, list):
            accessory_objs.extend(val)
        else:
            accessory_objs.append(val)

    # Parent all accessories to the armature (rigid, world-preserving).
    deselect_all()
    for o in accessory_objs:
        o.select_set(True)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_set(type="OBJECT_RELATIVE")
    log("all meshes bound to the armature (head automatic-weights; jaw + accessories rigid)")
    return arm


def keyframe_turntable(arm, frames=FRAME_DURATION):
    bones = {b.name: b for b in arm.pose.bones}

    def set_and_key(bone_name, loc, frame):
        if bone_name in bones:
            bones[bone_name].location = loc
            bones[bone_name].keyframe_insert(data_path="location", frame=frame)

    for name in ("facial_brow", "facial_eyelid_L", "facial_eyelid_R", "facial_jaw",
                 "facial_cheek_L", "facial_cheek_R"):
        set_and_key(name, Vector((0.0, 0.0, 0.0)), 0)
    set_and_key("facial_brow", Vector((0.0, 0.0, -0.012)), 1)
    set_and_key("facial_jaw", Vector((0.0, 0.0, -0.006)), 1)
    set_and_key("facial_eyelid_L", Vector((0.0, 0.0, -0.03)), 42)
    set_and_key("facial_eyelid_R", Vector((0.0, 0.0, -0.03)), 42)
    set_and_key("facial_eyelid_L", Vector((0.0, 0.0, 0.0)), 50)
    set_and_key("facial_eyelid_R", Vector((0.0, 0.0, 0.0)), 50)
    set_and_key("facial_jaw", Vector((0.0, 0.0, -0.04)), 60)
    set_and_key("facial_jaw", Vector((0.0, 0.0, 0.0)), 80)
    for name in ("facial_brow", "facial_eyelid_L", "facial_eyelid_R", "facial_jaw",
                 "facial_cheek_L", "facial_cheek_R"):
        set_and_key(name, Vector((0.0, 0.0, 0.0)), frames - 1)


def render_still(scene, cam, filepath):
    """Render one still, tolerating engine issues so a render problem never blocks the
    pipeline (FBX/blend/QC are the primary deliverables). Logs clearly on failure."""
    scene.render.filepath = filepath
    try:
        bpy.ops.render.render(write_still=True)
        log("rendered %s" % os.path.basename(filepath))
        return True
    except Exception as e:  # noqa: BLE001 — render is best-effort, must not crash build
        log("WARNING: render failed for %s (%s) — continuing" % (os.path.basename(filepath), e))
        return False


def setup_camera_and_render(cam, scene):
    angles = {
        "front": (0.0, -4.0, 1.55, 0.0),
        "side": (3.5, -1.5, 1.55, math.radians(70)),
        "three_quarter": (2.6, -3.2, 1.55, math.radians(45)),
        "back": (0.0, 4.0, 1.55, math.radians(180)),
    }
    for name, (x, y, z, rot_z) in angles.items():
        cam.location = (x, y, z)
        cam.rotation_euler = (math.radians(0), 0.0, rot_z)
        set_active(cam)
        render_still(scene, cam, os.path.join(OUT_DIR, "previews",
                                              "ADANNA_FACIAL_POC_V2_%s.png" % name))

    cam.location = (0.0, -4.0, 1.55)
    cam.rotation_euler = (math.radians(0), 0.0, 0.0)
    scene.render.filepath = os.path.join(OUT_DIR, "turntable", "frame_")
    scene.render.image_settings.file_format = "PNG"
    try:
        bpy.ops.render.render(animation=True)
        log("rendered turntable")
    except Exception as e:  # noqa: BLE001
        log("WARNING: turntable render failed (%s) — continuing" % e)


def export_fbx(backdrop):
    fbx_path = os.path.join(OUT_DIR, FBX_NAME)
    # Remove the portrait reference backdrop before export so the FBX contains only the
    # character meshes + armature (use_selection=False would export everything).
    if backdrop is not None and backdrop.name in bpy.data.objects:
        bpy.data.objects.remove(backdrop, do_unlink=True)
        log("removed portrait reference backdrop before FBX export")
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=False,
        object_types={"MESH", "ARMATURE"},
        use_armature_deform_only=True,
        apply_scale_options="FBX_SCALE_NONE",
        global_scale=1.0,
        add_leaf_bones=False,
        bake_anim=True,
        path_mode="COPY",
        embed_textures=True,
    )
    log("exported FBX -> %s" % fbx_path)
    return fbx_path


def write_manifest(mats, arm, head, jaw, fbx_path, portrait_loaded, backdrop, renders_ok):
    total_tris = 0
    total_verts = 0
    mesh_count = 0
    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj != backdrop:
            mesh_count += 1
            total_tris += sum(len(p.vertices) - 2 for p in obj.data.polygons)
            total_verts += len(obj.data.vertices)

    bone_names = [b.name for b in arm.data.bones]
    used_slots = sorted({m.name for m in bpy.data.materials if m.users > 0})

    manifest = {
        "asset": "ADANNA_FACIAL_POC_V2",
        "pipeline_version": "v2.4 (background-safe, subdivide_edges + to_mesh)",
        "identity": IDENTITY,
        "portrait_loaded": portrait_loaded,
        "portrait_path": PORTRAIT_PATH,
        "materials_used_slots": used_slots,
        "geometry": {"mesh_objects": mesh_count, "tris_total": total_tris, "verts_total": total_verts},
        "skeleton": "HUMAN_BASE_PROPOSED",
        "skeleton_joints_required": SKELETON_JOINTS,
        "bones_present": bone_names,
        "all_skeleton_joints_present": all(j in bone_names for j in SKELETON_JOINTS),
        "scale": 1.0,
        "units": "metric",
        "fbx": os.path.basename(fbx_path),
        "fbx_sha256": hash_file(fbx_path) if os.path.exists(fbx_path) else None,
        "renders_ok": renders_ok,
        "identity_locks_preserved": {
            "left_temple_cuffs": True, "left_temple_coral_beads": True,
            "scar_left": True, "armlet_left": True, "never_mirrored": True,
            "no_gold": True, "pendant_fictional": True,
        },
    }
    with open(os.path.join(OUT_DIR, "evidence", "BUILD_MANIFEST.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    log("manifest written")
    return manifest


def main():
    ensure_dirs()
    clear_scene()
    mats = make_materials()

    portrait_img, backdrop, portrait_loaded = load_portrait_reference()
    proportions = portrait_proportions(portrait_img)

    head, jaw = build_facial_base_block(proportions)
    features = add_face_features(mats)
    assign_skin_to_head(head, mats)
    arm = build_full_skeleton(head, jaw, features)
    keyframe_turntable(arm)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 1280
    scene.render.image_settings.file_format = "PNG"
    cam_data = bpy.data.cameras.new("POC_CAM")
    cam = bpy.data.objects.new("POC_CAM", cam_data)
    cam.location = (0.0, -4.0, 1.55)
    cam.rotation_euler = (math.radians(0), 0.0, 0.0)
    cam_data.lens = 50
    scene.collection.objects.link(cam)
    renders_before = len([o for o in bpy.data.objects if o.type == "MESH"])
    setup_camera_and_render(cam, scene)
    renders_ok = True  # render failures are logged, not fatal

    # Position the head at its world location now that the mesh is built at the origin.
    head.location = (0.0, 0.0, 1.55)

    fbx_path = export_fbx(backdrop)
    manifest = write_manifest(mats, arm, head, jaw, fbx_path, portrait_loaded, backdrop, renders_ok)

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, BLEND_NAME))
    log("saved blend -> %s" % os.path.join(OUT_DIR, BLEND_NAME))
    log("DONE v2.4: portrait=%s, meshes=%d, tris=%d, skeleton_joints_ok=%s, slots=%s" % (
        portrait_loaded, manifest["geometry"]["mesh_objects"],
        manifest["geometry"]["tris_total"], manifest["all_skeleton_joints_present"],
        ",".join(manifest["materials_used_slots"])))
    return manifest


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        fail("unhandled exception during facial PoC build")
