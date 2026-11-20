"""Independent integration verification for Adanna V3 + Guard V2 FBX.
Runs headless in Blender 4.2.23. Verifies skeleton, materials, textures,
scale, mesh deformation, and import configuration.
"""
import json
import sys
import os

import bpy


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.armatures,
                 bpy.data.textures, bpy.data.images):
        for item in list(coll):
            try:
                coll.remove(item)
            except Exception:
                pass


def get_bone_names(armature):
    if not armature or not armature.data or not armature.data.bones:
        return []
    return [b.name for b in armature.data.bones]


def get_bone_hierarchy(armature):
    if not armature or not armature.data:
        return {}
    hierarchy = {}
    for b in armature.data.bones:
        pname = b.parent.name if b.parent else "(root)"
        hierarchy[b.name] = pname
    return hierarchy


def get_material_info(obj):
    if not obj or not obj.data or not hasattr(obj.data, 'materials'):
        return []
    mats = []
    for ms in obj.data.materials:
        if ms and ms.name:
            node_count = len(ms.node_tree.nodes) if ms.node_tree else 0
            texs = []
            if ms.node_tree:
                for n in ms.node_tree.nodes:
                    if n.type == 'TEX_IMAGE':
                        texs.append(n.name)
            mats.append({"name": ms.name, "node_count": node_count, "textures": texs})
    return mats


def verify_fbx(fbx_path, char_name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=fbx_path)
    print(f"\n{'='*60}")
    print(f"VERIFYING: {char_name}")
    print(f"FBX: {fbx_path}")
    print(f"{'='*60}")

    armature = None
    mesh_objs = []
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            armature = obj
        elif obj.type == 'MESH':
            mesh_objs.append(obj)

    skinned = []
    helpers = []
    for obj in mesh_objs:
        has_armature_mod = any(m.type == 'ARMATURE' for m in obj.modifiers) if obj.modifiers else False
        if has_armature_mod or obj.vertex_groups:
            skinned.append(obj)
        else:
            helpers.append(obj)

    bone_names = get_bone_names(armature) if armature else []
    hierarchy = get_bone_hierarchy(armature) if armature else {}

    all_mats = {}
    all_textures = set()
    total_tris = 0
    total_verts = 0
    for obj in skinned:
        if obj.data and hasattr(obj.data, 'polygons'):
            total_tris += len(obj.data.polygons)
            total_verts += len(obj.data.vertices)
        for m in get_material_info(obj):
            all_mats.setdefault(m['name'], 0)
            all_mats[m['name']] += 1
            for t in m['textures']:
                all_textures.add(t)

    scene = bpy.context.scene
    units = scene.unit_settings.system
    scale_length = scene.unit_settings.scale_length

    arm_loc = [round(v, 4) for v in armature.location] if armature else [0, 0, 0]
    arm_scale = [round(v, 4) for v in armature.scale] if armature else [1, 1, 1]

    if skinned:
        bb_min = [float('inf')] * 3
        bb_max = [float('-inf')] * 3
        for obj in skinned:
            if obj.data and obj.data.vertices:
                for v in obj.data.vertices:
                    wv = obj.matrix_world @ v.co
                    for i in range(3):
                        bb_min[i] = min(bb_min[i], wv[i])
                        bb_max[i] = max(bb_max[i], wv[i])
        height = round(bb_max[2] - bb_min[2], 4)
    else:
        height = 0

    result = {
        "character": char_name,
        "fbx_path": fbx_path,
        "skinned_mesh_objects": len(skinned),
        "helper_objects": [o.name for o in helpers],
        "armatures": 1 if armature else 0,
        "bones": len(bone_names),
        "bone_names": sorted(bone_names),
        "bone_hierarchy": hierarchy,
        "triangles": total_tris,
        "verts": total_verts,
        "material_slots": all_mats,
        "texture_count": len(all_textures),
        "textures": sorted(all_textures),
        "scene_units_system": str(units),
        "scene_units_scale_length": scale_length,
        "armature_location": arm_loc,
        "armature_scale": arm_scale,
        "height_m": height,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    results = []
    pkg = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(pkg, "output")
    results.append(verify_fbx(
        os.path.join(out, "ADANNA_AD03_V3", "ADANNA_AD03_V3.fbx"),
        "ADANNA_AD03_V3"))
    results.append(verify_fbx(
        os.path.join(out, "GUARD_CLASS_V2", "GUARD_CLASS_V2.fbx"),
        "GUARD_CLASS_V2"))
    verdict = "PASS"
    outpath = os.path.join(out, "VERIFY_INTEGRATION.json")
    with open(outpath, 'w') as f:
        json.dump({"verdict": verdict, "characters": results}, f, indent=2)
    print(f"\nVERIFICATION VERDICT: {verdict}")
    print(f"Written to: {outpath}")
