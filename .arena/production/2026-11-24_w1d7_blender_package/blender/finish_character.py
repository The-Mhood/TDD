# finish_character.py — Blender 4.2 LTS (Apple Silicon / macOS) finisher, W1 D7 package.
# Runs HEADLESS inside Blender's own bundled Python. No pip installs, no system
# graphics libraries: Blender.app is self-contained on macOS.
#
# What it does, per character:
#   1. Imports the shipped skinned GLB (source of truth from build_*_v*.py).
#   2. Validates: mesh/armature presence, vertex groups, skin-weight sanity,
#      dimensions (~1.8 m), triangle count.
#   3. Pose-test: bends elbow/shoulder/knee/neck via pose bones, confirms the
#      evaluated (deformed) mesh actually moves, then resets to rest.
#   4. Saves the native editable project: <NAME>.blend
#   5. Exports Unreal-ready FBX (metres->cm via FBX unit scale, leaf bones off).
#   6. Renders 4 Workbench previews (front / three-quarter / side / back).
#   7. Writes <NAME>_BLENDER_QC.json next to the outputs.
#
# Invoked ONLY via run_all.sh (which passes --input/--name/--outdir after "--").
# v1.2 (2026-11-24): height measured as combined world-space bbox over skinned
# parts (was: max single-part object dimension = 0.521 m shin segment -> false
# fail). 1.6-2.0 m requirement unchanged; see ROOT_CAUSE_HEIGHT.md.
# v1.1 (2026-11-24): object classification fix. Blender 4.2's glTF importer
# creates an "Icosphere" bone-shape HELPER mesh (imp/gltf2_blender_node.py
# armature_display(): primitive_ico_sphere_add -> hidden "glTF_not_exported"
# collection, assigned as pose_bone.custom_shape). It is NOT character geometry
# and must never be skin-validated. Meshes are now classified:
#   SKINNED  (has Armature modifier)  -> strict weight validation, unchanged
#   HELPER   (in glTF_not_exported collection, or a bone custom-shape target)
#            -> recorded in QC, excluded from validation/deformation/FBX
#   OTHER    (anything else unskinned) -> hard FAIL (a rigid accessory would
#            need a deliberate bone-parent attachment, never silent weights)
import bpy, json, math, os, sys
from mathutils import Vector

def args():
    a = sys.argv[sys.argv.index("--") + 1:]
    d = {}
    for i in range(0, len(a) - 1, 2):
        d[a[i].lstrip("-")] = a[i + 1]
    return d

A = args()
SRC = os.path.abspath(A["input"]); NAME = A["name"]; OUT = os.path.abspath(A["outdir"])
os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
qc = {"character": NAME, "source_glb": SRC, "blender": bpy.app.version_string, "checks": {}}

def fail(msg):
    qc["verdict"] = "FAIL"; qc["error"] = msg
    json.dump(qc, open(os.path.join(OUT, f"{NAME}_BLENDER_QC.json"), "w"), indent=2)
    raise SystemExit(f"FINISHER FAIL: {msg}")

# --- clean scene + import -------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
arms = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
if not arms:
    fail("import produced no armature")
arm = arms[0]; arm.name = "HUMAN_BASE_PROPOSED"
# --- classification (see header v1.1 note) --------------------------------
shape_targets = {pb.custom_shape.name for pb in arm.pose.bones if pb.custom_shape}
meshes, helpers, other = [], [], []
for o in bpy.context.scene.objects:
    if o.type != "MESH":
        continue
    in_special = any(c.name == "glTF_not_exported" for c in o.users_collection)
    if in_special or o.name in shape_targets:
        helpers.append(o)
    elif any(m.type == "ARMATURE" for m in o.modifiers):
        meshes.append(o)
    else:
        other.append(o)
qc["checks"]["skinned_mesh_objects"] = len(meshes)
qc["checks"]["helper_objects"] = [{"name": o.name,
                                    "reason": "glTF importer bone custom-shape helper (glTF_not_exported)"} for o in helpers]
qc["checks"]["armatures"] = len(arms)
if other:
    fail("unclassified unskinned mesh object(s): " + ", ".join(o.name for o in other) +
         " — rigid accessories require an explicit bone-parent decision; refusing silent handling")
if not meshes:
    fail("import produced no skinned mesh")

# --- geometry / rig validation -------------------------------------------
total_tris = 0; wmin, wmax = 1e9, -1.0; unweighted = 0
for o in meshes:
    o.data.calc_loop_triangles()
    total_tris += len(o.data.loop_triangles)
    groups = {g.index for g in o.vertex_groups}
    if not groups:
        fail(f"{o.name}: no vertex groups")
    for v in o.data.vertices:
        s = sum(ge.weight for ge in v.groups if ge.group in groups)
        if s < 0.001: unweighted += 1
        wmin, wmax = min(wmin, s), max(wmax, s)
# v1.2 measurement fix: character height = COMBINED world-space bbox over all
# skinned part meshes (bound-box corners x matrix_world). v1.0/v1.1 wrongly used
# max(per-object dimensions.z), which measures the tallest single PART (the
# 0.521 m shin segment), not the character. Gate range 1.6-2.0 m is unchanged.
bpy.context.view_layer.update()
def world_bbox(objs):
    pts = []
    for o in objs:
        pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return [min(xs), max(xs)], [min(ys), max(ys)], [min(zs), max(zs)]
bbx, bby, bbz = world_bbox(meshes)
height_m = bbz[1] - bbz[0]
legacy_single_part_max = max(o.dimensions.z for o in meshes)
qc["checks"].update({"triangles": total_tris, "weight_sum_min": round(wmin, 3),
                     "weight_sum_max": round(wmax, 3), "unweighted_verts": unweighted,
                     "bones": len(arm.data.bones),
                     "world_bbox_m": {"x": [round(v, 3) for v in bbx], "y": [round(v, 3) for v in bby], "z": [round(v, 3) for v in bbz]},
                     "height_m_combined_world": round(height_m, 3),
                     "diagnostic_legacy_max_single_part_z_m": round(legacy_single_part_max, 3),
                     "armature_transform": {"location": [round(v, 3) for v in arm.location],
                                            "scale": [round(v, 3) for v in arm.scale]},
                     "scene_units": {"system": bpy.context.scene.unit_settings.system,
                                     "scale_length": bpy.context.scene.unit_settings.scale_length}})
if unweighted: fail(f"{unweighted} unweighted vertices")
if not (1.6 < height_m < 2.0): fail(f"height {height_m:.2f} m outside 1.6-2.0")

# --- pose / deformation smoke test ----------------------------------------
def evaluated_bbox():
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in meshes:
        eo = o.evaluated_get(dg)
        pts += [o.matrix_world @ Vector(c) for c in eo.bound_box]
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

bpy.context.view_layer.objects.active = arm
arm.select_set(True)
# BACKGROUND-MODE FIX (2026-12-08): bpy.ops.object.mode_set(mode="POSE") polls
# fail in `blender -b` ("context is incorrect") because background mode has no
# viewport area to satisfy the operator poll. Pose-bone rotations do NOT
# require POSE mode: pose_bones are data, the evaluated depsgraph applies
# them. We therefore pose via data only and never call mode_set.
rest_bb = evaluated_bbox()
tests = {"forearm.L": ("FORWARD", 1.4), "upperarm.R": ("FORWARD", 1.2),
         "shin.L": ("BACKWARD", 1.2), "head": ("YAW", 0.5)}
moved = {}
for bone_name, (kind, ang) in tests.items():
    pb = arm.pose.bones.get(bone_name)
    if pb is None:
        fail(f"missing bone {bone_name}")
    pb.rotation_mode = "XYZ"
    if kind == "FORWARD": pb.rotation_euler = (ang, 0, 0)
    elif kind == "BACKWARD": pb.rotation_euler = (-ang, 0, 0)
    else: pb.rotation_euler = (0, 0, ang)
    bpy.context.view_layer.update()
    bb = evaluated_bbox()
    delta = max(abs(a - b) for a, b in zip(bb, rest_bb))
    moved[bone_name] = round(delta, 3)
    pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    if delta < 0.005: fail(f"pose test: {bone_name} did not deform mesh (delta {delta})")
qc["checks"]["pose_test_bbox_delta_m"] = moved
# (no mode_set return to OBJECT mode - see background-mode fix above)

# --- save .blend + export FBX ----------------------------------------------
blend_path = os.path.join(OUT, f"{NAME}.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
fbx_path = os.path.join(OUT, f"{NAME}.fbx")
# Selection + export under temp_override so operator polls pass headless.
with bpy.context.temp_override(active_object=arm, selected_objects=[arm]+meshes):
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    for o in meshes:  # skinned meshes only — helpers never enter the FBX
        o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=True, global_scale=1.0,
                             apply_unit_scale=True, add_leaf_bones=False, bake_anim=False,
                             path_mode="COPY", use_mesh_modifiers=True)

# --- previews (Workbench: fast, deterministic, no path tracing) ------------
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.show_cavity = True
# v1.3: shade from the embedded base-colour textures; MATERIAL mode rendered
# textured cloth as flat grey in the qualification previews (inspection D5).
scene.display.shading.color_type = "TEXTURE"
scene.render.resolution_x = 640; scene.render.resolution_y = 800
scene.render.film_transparent = False
cam_data = bpy.data.cameras.new("QC_CAM"); cam = bpy.data.objects.new("QC_CAM", cam_data)
scene.collection.objects.link(cam); scene.camera = cam
sun_data = bpy.data.lights.new("QC_SUN", "SUN"); sun = bpy.data.objects.new("QC_SUN", sun_data)
sun.rotation_euler = (math.radians(50), 0, math.radians(30)); scene.collection.objects.link(sun)
# v1.3: view labels corrected. The characters face +Y in Blender (glTF->Blender
# conversion of the shipped GLBs; proven by the qualification renders, where
# the file named *_back.png shows the chest, baldric and pendant). v1.0-1.2
# filmed the back and labelled it "front". Cameras now match their labels.
VIEWS = {"front": (0, 3.2, 1.0), "three_quarter": (2.0, 2.6, 1.15), "side": (3.2, 0, 1.0), "back": (0, -3.2, 1.0)}
target = Vector((0, 0, 0.92))
for label, loc in VIEWS.items():
    cam.location = loc
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(OUT, "previews", f"{NAME}_{label}.png")
    bpy.ops.render.render(write_still=True)
qc["checks"]["previews"] = sorted(os.listdir(os.path.join(OUT, "previews")))

qc["outputs"] = {"blend": blend_path, "fbx": fbx_path}
qc["verdict"] = "PASS"
json.dump(qc, open(os.path.join(OUT, f"{NAME}_BLENDER_QC.json"), "w"), indent=2)
print(json.dumps(qc, indent=2))
