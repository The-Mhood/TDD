#!/usr/bin/env python3
"""CH01 PROVISIONAL PLAYABLE GREYBOX — builder (W1 D3, 2026-11-20)
Authority: owner directive 2026-11-20 — "I authorize provisional Chapter 1 greybox
construction immediately… dimensions remain engineering assumptions, not canon."
Source of layout: CH01_ENVIRONMENT_PRODUCTION_BREAKDOWN_2026-11-20.md §9 (modules,
traversal drivers, build order). No art, no materials, no approvals claimed.
Run headless: /tmp/bpyenv/bin/python build_ch01_greybox.py
Outputs next to this file: CH01_GREYBOX.blend, CH01_GREYBOX.fbx, CH01_GREYBOX_PLAN.png, CH01_GREYBOX_MANIFEST.json, CH01_GREYBOX_REPORT.md
Units: metres. X=east, Y=north, Z=up. Origin = village-square centre.
"""
import bpy, json, math, os, sys
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- clean scene ----------
bpy.ops.wm.read_factory_settings(use_empty=True)

def mat(name, rgb):
    m = bpy.data.materials.new(name); m.diffuse_color = (*rgb, 1.0); m.use_nodes = False
    return m

M = {
    "GROUND":  mat("GRY_GROUND",  (0.62,0.60,0.55)),
    "ROAD":    mat("GRY_ROAD",    (0.42,0.38,0.33)),
    "WALL":    mat("GRY_WALL",    (0.55,0.52,0.48)),
    "HUT":     mat("GRY_HUT",     (0.78,0.70,0.55)),
    "ROOF":    mat("GRY_ROOF",    (0.40,0.33,0.25)),
    "PALACE":  mat("GRY_PALACE",  (0.66,0.62,0.58)),
    "STALL":   mat("GRY_STALL",   (0.70,0.63,0.45)),
    "TREE":    mat("GRY_TREE",    (0.32,0.45,0.28)),
    "WATER":   mat("GRY_WATER",   (0.35,0.45,0.55)),
    "PROP":    mat("GRY_PROP",    (0.50,0.45,0.40)),
    "FLAG":    mat("GRY_FLAG_PROPOSED", (0.72,0.35,0.30)),  # provisional/proposed subject
}

objects = []
def box(name, loc, size, key="HUT", rot_z=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(loc[0], loc[1], size[2]/2 + (loc[2] if len(loc)>2 else 0)))
    o = bpy.context.active_object; o.name = name
    o.scale = (size[0], size[1], size[2]); o.rotation_euler = (0,0,math.radians(rot_z))
    o.data.materials.append(M[key]); objects.append(o); return o

def cyl(name, loc, radius, height, key="PROP", verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=height,
        location=(loc[0], loc[1], height/2 + (loc[2] if len(loc)>2 else 0)))
    o = bpy.context.active_object; o.name = name
    o.data.materials.append(M[key]); objects.append(o); return o

def cone(name, loc, r1, r2, height, key="ROOF", verts=4):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=height,
        location=(loc[0], loc[1], height/2 + (loc[2] if len(loc)>2 else 0)))
    o = bpy.context.active_object; o.name = name
    o.data.materials.append(M[key]); objects.append(o); return o

def plane(name, loc, size, key="ROAD", rot_z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(loc[0], loc[1], loc[2] if len(loc)>2 else 0.02))
    o = bpy.context.active_object; o.name = name
    o.scale = (size[0], size[1], 1.0); o.rotation_euler = (0,0,math.radians(rot_z))
    o.data.materials.append(M[key]); objects.append(o); return o

def anchor(name, loc):
    e = bpy.data.objects.new(name, None); e.location = loc
    bpy.context.scene.collection.objects.link(e); objects.append(e); return e

def wall_run(name, x0,y0,x1,y1,h=2.6,t=0.35):
    dx, dy = x1-x0, y1-y0; length = math.hypot(dx,dy); ang = math.degrees(math.atan2(dy,dx))
    return box(name, ((x0+x1)/2, (y0+y1)/2, 0), (length, t, h), "WALL", ang)

# ---------- 1. terrain, stream, roads ----------
box("TERRAIN_BLOCK", (0, -2, -0.51), (150, 150, 0.5), "GROUND")
plane("STREAM_WADING_STRIP", (18, -33, 0.03), (70, 4.5), "WATER")
plane("ROAD_FORK_FARM", (52, 2, 0.04), (22, 3.2), "ROAD", 0)
plane("ROAD_GATE_TO_SQUARE", (23, 1.4, 0.04), (46, 3.2), "ROAD", -2)
plane("ROAD_SQUARE_TO_STREAM", (9.5, -16, 0.04), (3.0, 30), "ROAD", 14)
plane("ROAD_PALACE_AXIS", (-10.5, 0, 0.045), (21, 2.6), "ROAD", 0)
plane("ROAD_FARM_RING_N", (39, 9, 0.04), (16, 2.2), "ROAD", 35)

# ---------- 2. perimeter wall + gate ----------
# rect ring x in [-46, 46], y in [-30, 28]; gate gap at east (x=46, y in [1.0, 3.4])
for i,(x0,y0,x1,y1) in enumerate([(-46,-30, 46,-30),(-46,28, 46,28),(-46,-30,-46,28),
                                  (46,-30, 46, 1.0),(46, 3.4, 46, 28)]):
    wall_run(f"WALL_3M_{i+1:02d}", x0,y0,x1,y1)
# gate module at east opening
box("GATE_POST_A", (46, 1.0, 0), (0.45,0.45,2.9), "WALL")
box("GATE_POST_B", (46, 3.4, 0), (0.45,0.45,2.9), "WALL")
box("GATE_LEAF_A", (46, 1.7, 0), (0.12,1.4,2.2), "WALL")
box("GATE_LEAF_B", (46, 2.7, 0), (0.12,1.4,2.2), "WALL")

# ---------- 3. structures ----------
def hut(name, x, y, w=4.0, d=3.0, wall_h=2.2, rot=0, key="HUT", roof="R_HIP"):
    box(name, (x,y,0), (w, d, wall_h), key, rot)
    if roof == "R_PIR":
        cone(name+"_ROOF_PYR", (x,y,wall_h), max(w,d)*0.78, 0.01, 1.3, "ROOF", 4)
    else:
        r = box(name+"_ROOF_HIP", (x,y,wall_h), (w+0.7, d+0.7, 0.9), "ROOF", rot)
        r.rotation_euler = (0,0,math.radians(rot+45))
    return

# residential huts (L1 establishing map approximation — greybox massing only)
hut("HUT_A_01", -12, 14, 4.2, 3.1, 2.2)
hut("HUT_A_02", -22, 12, 4.0, 3.0, 2.2)
hut("HUT_A_03",  16, -24, 4.6, 3.4, 2.3)   # family compound SE
hut("HUT_B_01",  28, -20, 5.0, 3.6, 2.3)   # family compound SE (HUT_B scale)
hut("HUT_A_04",  30,   6, 4.4, 3.2, 2.2)   # empty house FLAGGED proposed
hut("HUT_A_05",  36,  -7, 4.0, 3.0, 2.2)   # small family house FLAGGED proposed
hut("HUT_C_01", -14, -14, 2.4, 2.0, 1.9, roof="R_PIR")  # stores-ish (not granary)
hut("HUT_C_02",  26,  -9, 2.4, 2.0, 1.9, roof="R_PIR")  # compound store

# interiors as blockout boxes (enterable register)
box("INT_SMITHY_BLOCK",   (20, -8, 0),  (4.5,3.4,2.3), "HUT")
box("INT_HEALER_BLOCK",   (-14, 22, 0), (4.0,3.0,2.2), "HUT")
box("INT_WEAVER_BLOCK",   (-20, -6, 0), (4.0,3.0,2.2), "HUT")
box("INT_POTTER_YARD",    (-28,  2, 0), (5.0,4.0,2.0), "FLAG")   # PROPOSED subject
box("INT_KITCHEN_BLOCK",  (-8, -18, 0), (4.2,3.2,2.2), "HUT")
box("INT_BACKROOMS",      (14,  21, 0), (6.0,4.5,2.6), "HUT")
box("INT_BEDROOM_PALACE", (-30, 12, 0), (4.0,3.0,2.2), "PALACE")

# palace complex — axis from square WEST to palace portal
box("PALACE_COURTYARD_FLOOR", (-30, 0, 0), (16, 14, 0.25), "PALACE")
box("PALACE_PORTAL_BLOCK",    (-39, 0, 0), (3.0, 6.5, 4.6), "PALACE")
box("PALACE_HALL_BLOCK",      (-43.5, 0, 0), (8.0, 10.0, 5.2), "PALACE")
for i in range(4):  # verandah bays, 3.0 m rhythm, north & south edges of courtyard
    box(f"VER_BAY_N_{i+1}", (-24.5 - i*3.0,  7.6, 0), (0.35,0.35,2.6), "PALACE")
    box(f"VER_BAY_S_{i+1}", (-24.5 - i*3.0, -7.6, 0), (0.35,0.35,2.6), "PALACE")
box("THRONE_BLOCK_MASSING", (-42, 0, 0.25), (1.2, 1.0, 0.7), "PROP")  # NOT OAD-03 regalia

# market — stall grid, hipped only (SUB-008 family), backrooms behind
for r, y in enumerate([8.5, 12.5]):
    for c, x in enumerate([14, 17.5, 21]):
        box(f"STALL_A_{r+1}{c+1}", (x, y, 0), (2.0, 1.5, 2.3), "STALL")
box("MARKET_STALL_ROOFTEST", (17.5, 10.5, 2.3), (8.6, 5.4, 0.25), "ROOF")

# village square + tree + well + ekwe marker + throne approach
cyl("TREE_SHD_BLOCKER", (0, 0, 0), 0.8, 3.5, "TREE", 12)          # F3-gated species
cyl("TREE_SHD_CANOPY",  (0, 0, 3.4), 3.6, 1.6, "TREE", 12)
cyl("WELL_KERB",       (-8, 4, 0), 0.55, 1.0, "PROP", 16)
cyl("EKWE_DRUM_MASSING", (6.5, -3.5, 0), 0.18, 1.0, "PROP", 10)      # F1/F2 gated form
plane("NAVTEST_SQUARE_DISK_GUIDE", (0, 0, 0.05), (12, 12), "GROUND") # Ø12 walk test Ø (guide plane)

# farm ring outside west wall + stream docks
plane("FARM_TILE_01", (-60, 12, 0.03), (7, 6), "PROP")
plane("FARM_TILE_02", (-62, -4, 0.03), (7, 6), "PROP")
plane("FARM_TILE_03", (-58,-19, 0.03), (7, 6), "PROP")
box("STREAM_DOCK_N", (12, -30.5, 0), (2.0, 2.2, 0.5), "PROP")
box("STREAM_DOCK_S", (26, -35.5, 0), (2.0, 2.2, 0.5), "PROP")

# animal pen + compound walls SE
for i,(x0,y0,x1,y1) in enumerate([(8,-13, 16,-13),(16,-13, 16,-21),(8,-21, 16,-21),(8,-13, 8,-21)]):
    wall_run(f"PEN_WALL_{i+1}", x0,y0,x1,y1, h=1.6, t=0.3)
for i,(x0,y0,x1,y1) in enumerate([(13,-23, 44,-23)]):
    wall_run(f"COMPOUND_WALL_E_{i+1}", x0,y0,x1,y1, h=2.4, t=0.32)

# gate guard shelter (PROPOSED subject — F4 shields excluded)
box("GATE_GUARD_SHELTER", (43, 6, 0), (2.2, 1.8, 2.2), "FLAG")

# ---------- 4. gameplay anchors (empties) ----------
anchor("SPAWN_PLAYER", (54, 2, 0))
anchor("TRIGGER_GATE_ENTRY", (46, 2.2, 0))
anchor("RG_PATROL_A", (42, 2.2, 0))     # outside gate
anchor("RG_PATROL_B", (18, 2.0, 0))     # mid road
anchor("RG_PATROL_C", (2.5, -1.0, 0))   # square edge
anchor("RG_PATROL_D", (8, 2.0, 0))      # road east of square
anchor("MARKET_BACKROOM_DOOR_1", (15, 18.8, 0))
anchor("MARKET_BACKROOM_DOOR_2", (20, 18.8, 0))
anchor("PALACE_APPROACH_START", (-16, 0, 0))
anchor("THRONE_APPROACH", (-37, 0, 0))
anchor("EKWE_ZONE", (6.5, -3.5, 0))
anchor("STREAM_WADING_N", (12, -31, 0))
anchor("STREAM_WADING_S", (26, -33, 0))
anchor("FARM_FORK_L23", (56, 2, 0))

# ---------- 5. save, export FBX, write manifest ----------
blend_path = os.path.join(HERE, "CH01_GREYBOX.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

fbx_path = os.path.join(HERE, "CH01_GREYBOX.fbx")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=fbx_path, use_selection=False,
    apply_unit_scale=True, use_mesh_modifiers=True,
    object_types={'MESH','EMPTY'}, axis_forward='-Y', axis_up='Z')

manifest = {"name":"CH01_GREYBOX","date":"2026-11-20","status":"PROVISIONAL PLAYABLE GREYBOX — engineering assumptions; NOT canon; NOT final art",
    "units":"metres","axes":{"X":"east","Y":"north","Z":"up"},"origin":"village-square centre",
    "module_tokens_used":["TERRAIN_BLOCK","ROAD_*","STREAM_WADING_STRIP","WALL_3M_*","GATE_MOD(posts+leaves)","HUT_A/B/C","ROOF hip/pyram(flag)","VER_BAY_N/S x4","PALACE_*","STALL_A_*","TREE_SHD_*","WELL_KERB","EKWE_DRUM_MASSING","FARM_TILE_*","STREAM_DOCK_*","PEN_WALL_*","GATE_GUARD_SHELTER(flag)","INT_* blockouts"],
    "proposed_subjects_flagged":["INT_POTTER_YARD","GATE_GUARD_SHELTER","HUT_A_04 empty house","HUT_A_05 small family house"],
    "anchors":["SPAWN_PLAYER","TRIGGER_GATE_ENTRY","RG_PATROL_A..D","MARKET_BACKROOM_DOOR_1/2","PALACE_APPROACH_START","THRONE_APPROACH","EKWE_ZONE","STREAM_WADING_N/S","FARM_FORK_L23"],
    "excluded":["bunting (rejected motif)","carved friezes (OAD-06)","regalia (OAD-03)","F1/F2 ekwe final form","F3 tree species","FINAL architecture/materials","CH04 river grammar","Fishing Shelter (owner track)"],
    "objects":[o.name for o in objects]}
with open(os.path.join(HERE,"CH01_GREYBOX_MANIFEST.json"),"w") as f:
    json.dump(manifest, f, indent=2)
print("OBJECT COUNT:", len(objects))
print("SAVED:", blend_path)
print("SAVED:", fbx_path)
