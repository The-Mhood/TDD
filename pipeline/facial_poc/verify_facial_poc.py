#!/usr/bin/env python3
"""
verify_facial_poc.py — Qualification verification for the Adanna facial-likeness PoC  [REPAIRED v2.2]
The Disobedient Daughter · Zero-budget facial likeness strategy (TDD-IMPL-FACIAL-001)

Run HEADLESS after build_adanna_facial_poc.py:
  blender -b -P verify_facial_poc.py

v2.2 — BACKGROUND-SAFE + BMesh topology:
  - Topology (triangle count, degenerate polygons, non-manifold edges) now computed with
    BMesh (bmesh.new() + bm.from_mesh), a valid background-safe method. No edit-mode context needed.
  - UV check verifies the active UV layer actually has loop data.
  - Skin-weight check verifies the armature modifier AND vertex groups named after bones.
  - Portrait-loaded, full-skeleton-joint-presence, and binding-consistency checks retained.
  - EXITS NON-ZERO when the verdict is FAILED, so run_facial_poc.sh cannot report a
    failed QC as a successful run.

Checks (the qualification package, TDD-IMPL-QUALPKG-001):
  - file_integrity, scale_orientation, geometry, topology, uv, material_slots,
    skin_weights, skeleton, portrait_loaded, binding_consistency

Writes QUALIFIED / FAILED + per-check detail to evidence/QC_RESULT.json.
Record actual failures — do not suppress.
"""

import bpy
import bmesh
import json
import os
import sys
import hashlib

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "output")
EVIDENCE_DIR = os.path.join(OUT_DIR, "evidence")
FBX_NAME = "ADANNA_FACIAL_POC_V2.fbx"

REQUIRED_SLOTS = [
    "skin_base_v1", "lips_v1", "eye_dark_v1", "scar_marker_v1",
    "hair_dark_v1", "metal_aged_v1", "cloth_indigo_v1",
]
SKELETON_JOINTS = [
    "pelvis", "spine", "head",
    "upperarm.L", "upperarm.R", "forearm.L", "forearm.R",
    "thigh.L", "thigh.R", "shin.L", "shin.R",
]
TRI_BUDGET = 20000  # PoC head + identity features budget (Adanna V3 full body = 13,680)


def sha256(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_character_mesh(obj):
    return obj.type == "MESH" and not obj.name.startswith("PORTRAIT_REFERENCE")


def main():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    # The verifier runs as a SEPARATE `blender -b` invocation from the build, so it must
    # open the saved .blend first. Without this, bpy.data.objects is empty and every
    # geometry/skeleton/binding check fails.
    blend_path = os.path.join(OUT_DIR, "ADANNA_FACIAL_POC_V2.blend")
    if os.path.exists(blend_path):
        bpy.ops.wm.open_mainfile(filepath=blend_path)
        print("[verify] opened %s" % blend_path)
    else:
        print("[verify] ERROR: blend not found at %s — run the build first" % blend_path)

    checks = []

    def check(name, passed, detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    # 1. File integrity
    fbx_path = os.path.join(OUT_DIR, FBX_NAME)
    digest = sha256(fbx_path)
    check("file_integrity", digest is not None,
          "FBX sha256=%s" % (digest[:16] + "..." if digest else "MISSING"))

    # 2. Scale / orientation
    scene = bpy.context.scene
    unit = scene.unit_settings.system
    check("scale_orientation", unit == "METRIC",
          "unit_system=%s (expect METRIC); global_scale=1.0" % unit)

    # 3 & 4. Geometry + topology — computed with BMesh (background-safe).
    total_tris = 0
    total_verts = 0
    degenerate = 0
    non_manifold = 0
    mesh_objects = []
    for obj in bpy.data.objects:
        if is_character_mesh(obj):
            mesh_objects.append(obj.name)
            me = obj.data
            total_verts += len(me.vertices)
            bm = bmesh.new()
            bm.from_mesh(me)
            bm.faces.ensure_lookup_table()
            for f in bm.faces:
                n = len(f.verts)
                total_tris += n - 2          # n-gon -> n-2 triangles
                if n < 3:
                    degenerate += 1
            for e in bm.edges:
                if len(e.link_faces) != 2:
                    non_manifold += 1
            bm.free()
    check("geometry", total_tris <= TRI_BUDGET,
          "tris=%d (budget %d), verts=%d, meshes=%d" % (total_tris, TRI_BUDGET, total_verts, len(mesh_objects)))
    check("topology", degenerate == 0 and non_manifold == 0,
          "degenerate=%d, non_manifold_edges=%d" % (degenerate, non_manifold))

    # 5. UV — active layer exists AND has loop data.
    uv_ok = 0
    uv_missing = []
    for obj in bpy.data.objects:
        if is_character_mesh(obj):
            me = obj.data
            if me.uv_layers:
                uvl = me.uv_layers.active if me.uv_layers.active else me.uv_layers[0]
                if uvl is not None and len(uvl.data) > 0:
                    uv_ok += 1
                else:
                    uv_missing.append(obj.name)
            else:
                uv_missing.append(obj.name)
    check("uv", uv_ok > 0 and len(uv_missing) == 0,
          "objects_with_uv_data=%d, missing=%s" % (uv_ok, uv_missing))

    # 6. Material slots
    used_slots = sorted({m.name for m in bpy.data.materials if m.users > 0})
    missing_slots = [s for s in REQUIRED_SLOTS if s not in used_slots]
    check("material_slots", len(missing_slots) == 0,
          "used=%s; missing=%s" % (used_slots, missing_slots))

    # 7. Skin weights — head mesh bound to armature with deform weights.
    head = bpy.data.objects.get("ADANNA_HEAD")
    arm = bpy.data.objects.get("HUMAN_BASE_PROPOSED")
    weight_ok = False
    weight_detail = "head not found or not bound"
    if head and arm and head.parent == arm:
        me = head.data
        has_arm_mod = any(mod.type == "ARMATURE" for mod in me.modifiers)
        bone_names = [b.name for b in arm.data.bones]
        vgroup_names = [g.name for g in me.groups]
        has_vgroups = len(vgroup_names) > 0
        bone_groups_match = any(bn in vgroup_names for bn in bone_names)
        weight_ok = has_arm_mod and has_vgroups and bone_groups_match
        weight_detail = "armature_modifier=%s, vertex_groups=%d, bone_groups_match=%s" % (
            has_arm_mod, len(vgroup_names), bone_groups_match)
    check("skin_weights", weight_ok, weight_detail)

    # 8. Skeleton — full HUMAN_BASE_PROPOSED joint set present.
    skeleton_ok = False
    skeleton_detail = "HUMAN_BASE_PROPOSED not found"
    if arm:
        bone_names = [b.name for b in arm.data.bones]
        missing_joints = [j for j in SKELETON_JOINTS if j not in bone_names]
        skeleton_ok = len(missing_joints) == 0
        skeleton_detail = "bones=%s; missing_joints=%s" % (bone_names, missing_joints)
    check("skeleton", skeleton_ok, skeleton_detail)

    # 9. Portrait loaded as modelling reference.
    portrait_ok = False
    portrait_detail = "no portrait reference image found"
    for img in bpy.data.images:
        if "ADANNA_MASTER_PORTRAIT" in img.name or "REF_ADANNA" in img.name:
            portrait_ok = True
            portrait_detail = "portrait image loaded: %s" % img.name
            break
    check("portrait_loaded", portrait_ok, portrait_detail)

    # 10. Binding consistency — every non-reference mesh is parented to the armature.
    unbound = []
    if arm:
        for obj in bpy.data.objects:
            if is_character_mesh(obj):
                if obj.parent != arm:
                    unbound.append(obj.name)
    check("binding_consistency", len(unbound) == 0,
          "meshes_not_bound_to_armature=%s" % unbound)

    # Verdict
    passed = all(c["passed"] for c in checks)
    verdict = "QUALIFIED" if passed else "FAILED"
    result = {
        "asset": "ADANNA_FACIAL_POC_V2",
        "pipeline_version": "v2.4 (background-safe, subdivide_edges + to_mesh)",
        "verdict": verdict,
        "checks": checks,
        "summary": {
            "tris_total": total_tris, "verts_total": total_verts,
            "mesh_objects": mesh_objects, "materials_used": used_slots,
            "fbx_sha256": digest,
        },
    }
    with open(os.path.join(EVIDENCE_DIR, "QC_RESULT.json"), "w") as f:
        json.dump(result, f, indent=2)

    for c in checks:
        print("[verify] %-22s %-6s %s" % (c["check"], "PASS" if c["passed"] else "FAIL", c["detail"]))
    print("[verify] VERDICT: %s" % verdict)
    # Non-zero exit on FAILED so the shell cannot report a failed QC as success.
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
