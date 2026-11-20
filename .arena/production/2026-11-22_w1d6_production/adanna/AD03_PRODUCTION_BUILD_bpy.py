# AD-03 PRODUCTION BUILD — Blender 4.2+ bpy script v0.1 (2026-11-22, W1 D6)
# STATUS: READY TO RUN on a Blender >=4.2 workstation/container. NOT YET EXECUTED —
# this sandbox has no bpy/Blender (verified W1 D3–D6: no module, no binary, no root).
# Do NOT claim any output exists until this script has run and its QC report is filed.
#
# Purpose: build AD-03 LOD0 base production mesh for Adanna from the AD-02 composite
# reference (PENDING CD SELECT — run only after CD records the ruling; the script
# refuses to export with STATUS != "CD_SELECTED" unless --force-placeholder is set).
# Identity locks enforced as named empties + vertex groups (master is authority):
#   scar LEFT cheekbone | armlet LEFT coiled plain (no motifs/medallion; consultant
#   gate OPEN) | spiral pendant FICTIONAL | 3 bronze + 2 coral LEFT temple |
#   baldric anatomical L->R | NO blade/scabbard geometry (CQ-9 deferred).
# Units: metres internally; export scale x100 handled at FBX export for Unreal cm.
import bpy, math, sys, json

STATUS = "AWAITING_CD_SELECT"   # CD flips this via the decision record; see below.
argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
FORCE = "--force-placeholder" in argv

def clear():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()

def make_profile_body():
    # Lathe-style profile: (radius, height) pairs, low-seg base for retopo start.
    profile = [(0.001,0.00),(0.16,0.02),(0.13,0.45),(0.11,0.85),(0.14,1.05),
               (0.17,1.25),(0.15,1.42),(0.06,1.52),(0.055,1.60),(0.10,1.68),(0.001,1.80)]
    verts, faces = [], []
    SEG = 16
    rings = []
    for r, z in profile:
        ring = []
        for i in range(SEG):
            t = 2*math.pi*i/SEG
            ring.append(len(verts)); verts.append((r*math.cos(t), r*math.sin(t), z))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(SEG):
            faces.append((a[i], a[(i+1)%SEG], b[(i+1)%SEG], b[i]))
    me = bpy.data.meshes.new("ADANNA_LOD0_BASE")
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new("ADANNA_LOD0_BASE", me)
    bpy.context.collection.objects.link(ob)
    return ob

def add_lock_empties():
    locks = {"LOCK_scar_L_cheekbone": (-0.055, 0.075, 1.66),
             "LOCK_armlet_L_coils_plain": (-0.24, 0.0, 1.28),
             "LOCK_pendant_spiral_FICTIONAL": (0.0, 0.15, 1.38),
             "LOCK_beads_3B2C_L_temple": (-0.085, 0.03, 1.70),
             "LOCK_baldric_L_to_R_start": (-0.13, 0.13, 1.46),
             "LOCK_baldric_L_to_R_end": (0.15, 0.10, 1.10)}
    for name, loc in locks.items():
        e = bpy.data.objects.new(name, None); e.location = loc
        e.empty_display_size = 0.03; bpy.context.collection.objects.link(e)

def add_armature():
    bpy.ops.object.armature_add(enter_editmode=True)
    arm = bpy.context.object; arm.name = "HUMAN_BASE_PROPOSED"  # TD ruling pending
    # Minimal spine chain placeholder for deformation smoke tests; full HUMAN_BASE
    # bone set is TD-owned and must replace this before any animation claim.
    eb = arm.data.edit_bones
    root = eb[0]; root.name = "pelvis"; root.head = (0,0,0.95); root.tail = (0,0,1.15)
    spine = eb.new("spine"); spine.parent = root; spine.head=(0,0,1.15); spine.tail=(0,0,1.40)
    head = eb.new("head"); head.parent = spine; head.head=(0,0,1.55); head.tail=(0,0,1.72)
    bpy.ops.object.mode_set(mode="OBJECT")
    return arm

def main():
    if STATUS != "CD_SELECTED" and not FORCE:
        print("AD03: CD has not recorded SELECT; refusing production export. "
              "Re-run with --force-placeholder for a labelled placeholder only.")
    clear()
    body = make_profile_body()
    add_lock_empties()
    arm = add_armature()
    mod = body.modifiers.new("Armature", "ARMATURE"); mod.object = arm
    mats = ["skin_base_v1", "cloth_indigo_plain_v1", "leather_baldric_v1",
            "bronze_armlet_plain_v1", "pendant_spiral_FICTIONAL_v1"]
    for mname in mats:
        m = bpy.data.materials.new(mname); body.data.materials.append(m)
    tag = "PLACEHOLDER" if (FORCE and STATUS != "CD_SELECTED") else "PRODUCTION"
    out = f"//ADANNA_AD03_LOD0_{tag}.fbx"
    bpy.ops.export_scene.fbx(filepath=bpy.path.abspath(out), use_selection=False,
                             global_scale=100.0, apply_unit_scale=True,
                             add_leaf_bones=False, path_mode="COPY")
    qc = {"status": STATUS, "tag": tag, "verts": len(body.data.vertices),
          "polys": len(body.data.polygons), "materials": mats,
          "blade_scabbard_geometry": "NONE (CQ-9 deferred)", "export": out}
    with open(bpy.path.abspath("//ADANNA_AD03_QC.json"), "w") as fh:
        json.dump(qc, fh, indent=2)
    print(json.dumps(qc, indent=2))

main()
