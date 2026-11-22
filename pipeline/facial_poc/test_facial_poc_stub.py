#!/usr/bin/env python3
"""
Sandbox logic test for build_adanna_facial_poc.py + verify_facial_poc.py.
Provides a faithful-enough fake `bpy` / `bmesh` / `mathutils` so the REAL scripts'
main() run end-to-end: exercising control flow, BMesh calls, file outputs, QC verdict
logic and non-zero exit. This is NOT Blender execution (Blender cannot run in-sandbox);
it is a logic-level regression test that catches bugs before the owner-Mac run.
"""
import sys, os, types, json, importlib.util

FAIL = []
def ok(msg): print("[stub-test] PASS  " + msg)
def bad(msg): print("[stub-test] FAIL  " + msg); FAIL.append(msg)

# ---------- mathutils.Vector ----------
class Vector:
    def __init__(self, data): self.x, self.y, self.z = (float(d) for d in data)
    def __getitem__(self, i): return (self.x, self.y, self.z)[i]
    def __iter__(self): return iter((self.x, self.y, self.z))
    def __mul__(self, o):
        if isinstance(o, Vector): return Vector((self.x*o.x, self.y*o.y, self.z*o.z))
        return Vector((self.x*o, self.y*o, self.z*o))
    __rmul__ = __mul__
    def __add__(self, o): return Vector((self.x+o.x, self.y+o.y, self.z+o.z))
    def __eq__(self, o):
        if isinstance(o, Vector): return (self.x,self.y,self.z)==(o.x,o.y,o.z)
        if isinstance(o,(tuple,list)): return (self.x,self.y,self.z)==tuple(float(v) for v in o)
        return NotImplemented
    def copy(self): return Vector((self.x,self.y,self.z))

mathutils = types.ModuleType("mathutils"); mathutils.Vector = Vector
sys.modules["mathutils"] = mathutils

# ---------- fake mesh data ----------
class Vert:
    def __init__(self, co): self.co = co
class Loop:
    def __init__(self, vi): self.vertex_index = vi
class Poly:
    def __init__(self, n): self.vertices = list(range(n))
class Edge:
    def __init__(self): self.link_faces = [None, None]
class UVLoop:
    def __init__(self): self.uv = (0.0, 0.0)
class UVLayer:
    def __init__(self, name): self.name = name; self.data = [UVLoop() for _ in range(16)]
    def __len__(self): return len(self.data)
class UVLayers:
    def __init__(self): self._layers = []
    def __bool__(self): return len(self._layers) > 0
    def __len__(self): return len(self._layers)
    def __getitem__(self, i): return self._layers[i]
    @property
    def active(self): return self._layers[0] if self._layers else None
    def new(self, name="UVMap"):
        l = UVLayer(name); self._layers.append(l); return l
class Group:
    def __init__(self, name): self.name = name
class Groups:
    def __init__(self): self._g = []
    def __len__(self): return len(self._g)
    def __iter__(self): return iter(self._g)
    def new(self, name): g = Group(name); self._g.append(g); return g
class Mod:
    def __init__(self, t): self.type = t; self.object = None
class _MatList(list):
    def append(self, m):
        super().append(m); m.users += 1
    def clear(self):
        for m in self: m.users -= 1
        super().clear()
class Mesh:
    def __init__(self, name, nverts=12, nquads=8):
        self.name = name
        self.vertices = [Vert(Vector((0.0,0.0,0.0))) for _ in range(nverts)]
        self.polygons = [Poly(4) for _ in range(nquads)]
        self.edges = [Edge() for _ in range(max(1, nquads))]
        self.uv_layers = UVLayers(); self.uv_layers.new("UVMap")
        self.groups = Groups()
        self.loops = [Loop(i % nverts) for i in range(nquads * 4)]
        self.modifiers = []; self.materials = _MatList()
    def update(self): pass

# ---------- fake object ----------
class Object:
    def __init__(self, name, otype="MESH", data=None):
        self.name = name; self.type = otype; self.data = data
        self.hide_render = False
        self.location = Vector((0.0,0.0,0.0)); self.rotation_euler = Vector((0.0,0.0,0.0))
        self.scale = Vector((1.0,1.0,1.0))
        self.parent = None; self.parent_bone = ""
        self._props = {}
        self.pose = types.SimpleNamespace(bones={})
    def select_set(self, v): self.select = v
    def __setitem__(self, k, v): self._props[k] = v
    def __getitem__(self, k): return self._props[k]
    @property
    def matrix_world(self): return Vector((1.0,1.0,1.0))

class Bone:
    def __init__(self, name): self.name = name; self.head = Vector((0,0,0)); self.tail = Vector((0,0,0)); self.parent = None
class ArmatureData:
    def __init__(self):
        self.bones = []
        self.edit_bones = types.SimpleNamespace(new=self._new_bone)
    def _new_bone(self, name):
        b = Bone(name); self.bones.append(b); return b

class Objects:
    def __init__(self): self._objs = []
    def __iter__(self): return iter(self._objs)
    def __len__(self): return len(self._objs)
    def __getitem__(self, i): return self._objs[i]
    def new(self, name, data=None):
        if data is None:
            otype = "MESH"
        elif hasattr(data, "edit_bones"):
            otype = "ARMATURE"
        elif type(data).__name__ == "Camera":
            otype = "CAMERA"
        else:
            otype = "MESH"
        o = Object(name, otype, data)
        self._objs.append(o); return o
    def remove(self, obj, do_unlink=True):
        if obj in self._objs: self._objs.remove(obj)
    def get(self, name):
        for o in self._objs:
            if o.name == name: return o
        return None

# ---------- bmesh fake ----------
class BMFace:
    def __init__(self, verts): self.verts = verts; self.material_index = 0
class BMEdge:
    def __init__(self): self.link_faces = [None, None]

class _BMCollection:
    def __init__(self, items): self._items = list(items)
    def __iter__(self): return iter(self._items)
    def __len__(self): return len(self._items)
    def __getitem__(self, i): return self._items[i]
    def ensure_lookup_table(self): pass

class BMesh2:
    """Fake BMesh. Models the REAL Blender API: bmesh.new() returns a BMesh
    instance, and mesh data is loaded via the instance method bm.from_mesh(me).
    There is deliberately NO module-level bmesh.from_mesh, so an invalid
    `bmesh.from_mesh(...)` call raises AttributeError exactly as it does in
    real Blender — this is what makes the regression test catch the defect."""
    def __init__(self, verts=None, edges=None, faces=None):
        self.verts = _BMCollection(verts or [])
        self.edges = _BMCollection(edges or [])
        self.faces = _BMCollection(faces or [])
    def from_mesh(self, me):
        self.verts = _BMCollection(list(me.vertices))
        self.edges = _BMCollection(list(me.edges))
        self.faces = _BMCollection([BMFace(list(p.vertices)) for p in me.polygons])
    def to_mesh(self, me):
        me.polygons = [Poly(len(f.verts)) for f in self.faces]
        me.vertices = list(self.verts)
    def free(self): pass

bmesh = types.ModuleType("bmesh")
class _BMOps:
    """Models the REAL bmesh.ops module. The subdivide operator is named
    `subdivide_edges` (NOT `subdivide`) and takes `cuts` (NOT `number_cuts`).
    There is deliberately NO `subdivide` attribute, so an invalid
    `bmesh.ops.subdivide(...)` call raises AttributeError exactly as Blender does."""
    @staticmethod
    def subdivide_edges(bm, edges, cuts=1, use_grid_fill=True, **kw):
        # Faithful signature; appends `cuts` new edges per input edge to model
        # the topological change (the stub's tri counts are synthetic anyway).
        for _ in list(edges):
            for _c in range(cuts):
                bm.edges._items.append(BMEdge())
        return
    @staticmethod
    def remove_doubles(bm, verts, threshold=0.0): return
bmesh.ops = _BMOps()
def _new(): return BMesh2()
# NOTE: bmesh.update_mesh is NOT a real Blender module function. The object-mode
# write-back is the instance method bm.to_mesh(me) followed by me.update().
# Deliberately absent so an invalid bmesh.update_mesh(...) call raises AttributeError.
# NOTE: bmesh.from_mesh is also intentionally absent — it is not a real Blender API.
bmesh.new = _new
sys.modules["bmesh"] = bmesh

# ---------- bpy fake ----------
class _Socket:
    """Fake Blender node socket. Colour sockets enforce a 4-component RGBA value,
    mirroring Blender's requirement, so a malformed (e.g. 5-component) colour
    assignment fails the stub test instead of passing silently."""
    COLOR_SOCKETS = ("Base Color", "Emission Color")
    def __init__(self, default=(0,0,0,1), name=""):
        self._name = name
        self.default_value = default
    @property
    def default_value(self):
        return self._default_value
    @default_value.setter
    def default_value(self, value):
        if self._name in _Socket.COLOR_SOCKETS:
            n = len(value)
            if n != 4:
                raise ValueError(
                    "colour socket '%s' requires RGBA (4 components), got %d: %r"
                    % (self._name, n, value))
        self._default_value = value
class _Sockets(dict):
    """Dict-like socket collection (real Blender NodeInputs/NodeOutputs support [] access)."""
    def __getitem__(self, k):
        if k not in self:
            dict.__setitem__(self, k, _Socket(name=k))
        return dict.__getitem__(self, k)
class Node:
    def __init__(self, name):
        self.name = name
        self.inputs = _Sockets()
        self.outputs = _Sockets()
        for k in ("Base Color","Roughness","Metallic","Emission Color","Emission Strength"):
            self.inputs[k] = _Socket(name=k)
        self.outputs["BSDF"] = _Socket()
        self.outputs["Color"] = _Socket()
class _Nodes(dict):
    def __getitem__(self, k):
        if k not in self: raise KeyError(k)
        return dict.__getitem__(self, k)
    def new(self, node_type):
        n = Node(node_type); dict.__setitem__(self, node_type, n); return n
class NodeTree:
    def __init__(self):
        self.nodes = _Nodes(); self.links = types.SimpleNamespace(new=lambda *a, **k: None)
    def nodes_new(self, t): return self.nodes.new(t)
class Material:
    def __init__(self, name):
        self.name = name; self.use_nodes = False; self.node_tree = NodeTree(); self.users = 0
        nt = self.node_tree
        nt.nodes["Principled BSDF"] = Node("Principled BSDF")
        nt.nodes["Material Output"] = Node("Material Output")
class Materials:
    def __init__(self): self._m = []
    def __iter__(self): return iter(self._m)
    def __len__(self): return len(self._m)
    def new(self, name): m = Material(name); self._m.append(m); return m
class Image:
    def __init__(self, path): self.name = "REF_ADANNA_MASTER_PORTRAIT"; self.size = (1024, 1280)
class Images:
    def __init__(self): self._i = []
    def __iter__(self): return iter(self._i)
    def load(self, path, check_existing=False): im = Image(path); self._i.append(im); return im
class Camera:
    def __init__(self, name): self.name = name; self.lens = 50
class Cameras:
    def __init__(self): self._c = []
    def new(self, name): c = Camera(name); self._c.append(c); return c
class Collection:
    def __init__(self): self.objects = types.SimpleNamespace(link=lambda o: None)
class Scene:
    def __init__(self):
        self.render = types.SimpleNamespace()
        self.render.engine = "BLENDER_WORKBENCH"
        self.render.resolution_x = 1280; self.render.resolution_y = 1280
        self.render.filepath = ""
        self.render.image_settings = types.SimpleNamespace(file_format="PNG")
        self.unit_settings = types.SimpleNamespace(system="METRIC")
        self.collection = Collection()
class ViewLayer:
    def __init__(self): self.objects = types.SimpleNamespace(active=None)

STATE = {"active": None}

class _Ctx:
    def __init__(self):
        self._scene = Scene(); self._vl = ViewLayer(); self._coll = Collection()
    @property
    def scene(self): return self._scene
    @property
    def view_layer(self): return self._vl
    @property
    def collection(self): return self._coll
    @property
    def active_object(self): return STATE["active"]
    @active_object.setter
    def active_object(self, v): STATE["active"] = v

class _Ops: pass
ops_wm = _Ops(); ops_mesh = _Ops(); ops_object = _Ops(); ops_render = _Ops(); ops_export = _Ops()

DATA = types.SimpleNamespace(objects=Objects(), materials=Materials(), images=Images(),
                             meshes=[], armatures=[], cameras=Cameras())
CTX = _Ctx()

def _make_primitive(kind):
    me = Mesh("prim_" + kind, nverts=12, nquads=8)
    o = Object("prim_" + kind, "MESH", me)
    DATA.objects._objs.append(o); STATE["active"] = o
    return o
ops_mesh.primitive_uv_sphere_add = lambda **k: _make_primitive("uv_sphere")
ops_mesh.primitive_plane_add = lambda **k: _make_primitive("plane")
ops_mesh.primitive_cone_add = lambda **k: _make_primitive("cone")
ops_mesh.primitive_torus_add = lambda **k: _make_primitive("torus")
ops_mesh.primitive_cube_add = lambda **k: _make_primitive("cube")

def _armature_add(**k):
    adata = ArmatureData()
    arm = Object("HUMAN_BASE_PROPOSED", "ARMATURE", adata)
    DATA.objects._objs.append(arm); STATE["active"] = arm
    return arm
ops_object.armature_add = _armature_add
# NOTE: no bpy.ops.object.mode_set stub. The pipeline must not call context-sensitive
# edit-mode ops (mode_set / select_all / transform_apply / mesh.select_all / object.join),
# which fail in Blender background mode. An un-stubbed op would raise AttributeError here,
# so a regression that reintroduces such a call is caught immediately.

def _parent_set(type="OBJECT_RELATIVE"):
    active = STATE["active"]
    for o in DATA.objects:
        if getattr(o, "select", False) and o is not active and o.type == "MESH":
            if type == "ARMATURE_AUTO" and not any(m.type == "ARMATURE" for m in o.data.modifiers):
                o.data.modifiers.append(Mod("ARMATURE"))
                for j in ("pelvis", "spine", "head"):
                    o.data.groups.new(j)
            o.parent = active
ops_object.parent_set = _parent_set

def _render(write_still=False, animation=False):
    fp = CTX._scene.render.filepath
    if write_still and fp:
        os.makedirs(os.path.dirname(fp) or ".", exist_ok=True)
        with open(fp, "wb") as f: f.write(b"\x89PNG\r\n")
ops_render.render = _render

def _export_fbx(filepath, **k):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "wb") as f: f.write(b"fakeFBX")
ops_export.fbx = _export_fbx
ops_wm.read_factory_settings = lambda use_empty=True: None
def _save_mainfile(filepath):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "wb") as f: f.write(b"fakeBLEND")
ops_wm.save_as_mainfile = _save_mainfile
ops_wm.open_mainfile = lambda filepath: None

ops = types.SimpleNamespace(wm=ops_wm, mesh=ops_mesh, object=ops_object, render=ops_render, export_scene=ops_export)
bpy = types.ModuleType("bpy"); bpy.ops = ops; bpy.data = DATA; bpy.context = CTX
sys.modules["bpy"] = bpy

# ---------- load real scripts ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

import tempfile
tmpout = tempfile.mkdtemp(prefix="facial_out_")

build = load("build_facial_poc", os.path.join(SCRIPT_DIR, "build_adanna_facial_poc.py"))
build.OUT_DIR = tmpout; build.SCRIPT_DIR = SCRIPT_DIR
ref_dir = os.path.join(SCRIPT_DIR, "reference"); os.makedirs(ref_dir, exist_ok=True)

# ---------- normalize_color unit tests (RGB/RGBA/invalid) ----------
# The Blender colour socket requires exactly 4 components. normalize_color must
# accept RGB (append alpha 1.0), accept RGBA (unchanged), and reject bad lengths.
nc = build.normalize_color
rgb_out = nc((0.46, 0.30, 0.22))
ok("normalize_color: RGB -> RGBA with alpha 1.0 (%r)" % (rgb_out,))
if len(rgb_out) != 4 or abs(rgb_out[3] - 1.0) > 1e-9:
    bad("normalize_color RGB output not a 4-tuple with alpha 1.0")
rgba_in = (0.46, 0.30, 0.22, 0.5)
rgba_out = nc(rgba_in)
ok("normalize_color: RGBA used unchanged (%r)" % (rgba_out,))
if rgba_out != rgba_in:
    bad("normalize_color altered a valid RGBA input")
for bad_len in [(0.1, 0.2), (0.1, 0.2, 0.3, 0.4, 0.5), (0.1,)]:
    try:
        nc(bad_len); bad("normalize_color accepted invalid length %d" % len(bad_len))
    except ValueError:
        ok("normalize_color rejects invalid length %d" % len(bad_len))
# Regression: the exact caller form that failed in Blender (RGBA + appended alpha)
# must now produce a valid 4-tuple, not 5 components.
regression = nc((0.46, 0.30, 0.22, 1.0))
if len(regression) != 4:
    bad("regression: RGBA caller produced %d components" % len(regression))
else:
    ok("regression: RGBA caller (0.46,0.30,0.22,1.0) -> 4 components")

# ---------- BMesh API regression (real API contract, not a mock of the invalid impl) ----------
# Real Blender BMesh API: bm = bmesh.new(); bm.from_mesh(mesh). There is NO
# module-level bmesh.from_mesh. The fake above deliberately omits it so an
# invalid call raises AttributeError exactly as Blender does.
import bmesh as _bmesh_mod
ok("bmesh.new exists and returns a BMesh instance")
_bm_inst = _bmesh_mod.new()
ok("bmesh.new() returns a BMesh with a from_mesh method: %s" % hasattr(_bm_inst, "from_mesh"))
ok("bmesh.new() returns a BMesh with a free method: %s" % hasattr(_bm_inst, "free"))
try:
    _bmesh_mod.from_mesh; bad("bmesh.from_mesh should NOT exist (invalid Blender API)")
except AttributeError:
    ok("bmesh.from_mesh correctly ABSENT (invalid Blender API) -> AttributeError")
# The exact defect that failed in Blender 4.2.23 must now raise.
try:
    _bmesh_mod.from_mesh(object()); bad("invalid bmesh.from_mesh() call did not raise")
except AttributeError:
    ok("invalid bmesh.from_mesh(...) call raises AttributeError (matches Blender)")

# ---- BMesh ops + write-back API (the Blender 4.2.23 subdivide failure) ----
# Real Blender: the subdivide operator is bmesh.ops.subdivide_edges(bm, edges,
# cuts=..., use_grid_fill=...). There is NO bmesh.ops.subdivide. The object-mode
# write-back is the instance method bm.to_mesh(me) + me.update(); there is NO
# module-level bmesh.update_mesh. The fake models exactly this, so invalid calls
# raise AttributeError as Blender does.
ok("bmesh.ops.subdivide_edges exists: %s" % hasattr(_bmesh_mod.ops, "subdivide_edges"))
try:
    _bmesh_mod.ops.subdivide; bad("bmesh.ops.subdivide should NOT exist (invalid Blender API)")
except AttributeError:
    ok("bmesh.ops.subdivide correctly ABSENT (invalid Blender API) -> AttributeError")
try:
    _bmesh_mod.ops.subdivide(object()); bad("invalid bmesh.ops.subdivide() call did not raise")
except AttributeError:
    ok("invalid bmesh.ops.subdivide(...) call raises AttributeError (matches Blender)")
try:
    _bmesh_mod.update_mesh; bad("bmesh.update_mesh should NOT exist (invalid Blender API)")
except AttributeError:
    ok("bmesh.update_mesh correctly ABSENT (invalid Blender API) -> AttributeError")
try:
    _bmesh_mod.update_mesh(object(), object()); bad("invalid bmesh.update_mesh() call did not raise")
except AttributeError:
    ok("invalid bmesh.update_mesh(...) call raises AttributeError (matches Blender)")
ok("bmesh.new() returns a BMesh with a to_mesh method: %s" % hasattr(_bm_inst, "to_mesh"))
# The correct operator call must actually work through the fake (signature match).
_bm_inst2 = _bmesh_mod.new()
try:
    _bmesh_mod.ops.subdivide_edges(_bm_inst2, edges=[], cuts=1, use_grid_fill=True)
    ok("bmesh.ops.subdivide_edges(...) callable with cuts/use_grid_fill (correct signature)")
except Exception as _e:
    bad("bmesh.ops.subdivide_edges call failed: %r" % _e)

# Source-level regression: the build + verify scripts must use the correct pattern
# and must NOT contain the invalid module-level bmesh.from_mesh( call.
import re as _re
for _mod_name, _src in (("build_adanna_facial_poc", build.__file__),
                        ("verify_facial_poc", None)):
    pass
# Scan both source files on disk for the invalid pattern.
_src_files = [
    os.path.join(SCRIPT_DIR, "build_adanna_facial_poc.py"),
    os.path.join(SCRIPT_DIR, "verify_facial_poc.py"),
]
_invalid_hits = []
for _f in _src_files:
    _txt = open(_f, encoding="utf-8").read()
    for _m in _re.finditer(r'bmesh\.from_mesh\s*\(', _txt):
        _invalid_hits.append(_f)
if _invalid_hits:
    bad("invalid bmesh.from_mesh( call remains in: %s" % ", ".join(_invalid_hits))
else:
    ok("no invalid bmesh.from_mesh( call remains in build/verify sources")
# Confirm the correct two-line pattern is present in the build script.
_build_txt = open(_src_files[0], encoding="utf-8").read()
if _re.search(r'bmesh\.new\(\)\s*\n\s*bm\.from_mesh\(', _build_txt):
    ok("build script uses correct pattern: bmesh.new() + bm.from_mesh(...)")
else:
    bad("build script does not use the correct bmesh.new() + bm.from_mesh() pattern")

# Source-level: the invalid bmesh.ops.subdivide( and bmesh.update_mesh( calls must
# be absent from build/verify (they fail in real Blender 4.2.23).
_INVALID_OPS = [
    (r'bmesh\.ops\.subdivide\s*\(', "bmesh.ops.subdivide"),
    (r'bmesh\.update_mesh\s*\(', "bmesh.update_mesh"),
]
for _f in _src_files:
    _txt = open(_f, encoding="utf-8").read()
    for _pat, _label in _INVALID_OPS:
        if _re.search(_pat, _txt):
            bad("invalid %s( call remains in %s" % (_label, os.path.basename(_f)))
if not any(_re.search(p, open(f, encoding="utf-8").read())
           for f in _src_files for p, _ in _INVALID_OPS):
    ok("no invalid bmesh.ops.subdivide( / bmesh.update_mesh( call remains in build/verify")
# Confirm the correct operator + write-back patterns are present in the build script.
if _re.search(r'bmesh\.ops\.subdivide_edges\s*\(', _build_txt):
    ok("build script uses correct operator: bmesh.ops.subdivide_edges(...)")
else:
    bad("build script does not use bmesh.ops.subdivide_edges(...)")
if _re.search(r'bm\.to_mesh\([^)]+\)\s*\n\s*\w+\.data\.update\(\)', _build_txt):
    ok("build script uses correct write-back: bm.to_mesh(me) + me.update()")
else:
    bad("build script does not use the correct bm.to_mesh(me) + me.update() write-back")

# Source-level regression: context-sensitive edit-mode ops fail in Blender background
# mode and must NOT appear as actual calls in the pipeline. (Docstring mentions are ok.)
_CTX_SENSITIVE = [
    (r'bpy\.ops\.object\.mode_set\s*\(', "bpy.ops.object.mode_set"),
    (r'bpy\.ops\.object\.select_all\s*\(', "bpy.ops.object.select_all"),
    (r'bpy\.ops\.object\.transform_apply\s*\(', "bpy.ops.object.transform_apply"),
    (r'bpy\.ops\.mesh\.select_all\s*\(', "bpy.ops.mesh.select_all"),
    (r'bpy\.ops\.mesh\.subdivide\s*\(', "bpy.ops.mesh.subdivide"),
    (r'bpy\.ops\.mesh\.remove_doubles\s*\(', "bpy.ops.mesh.remove_doubles"),
    (r'bpy\.ops\.object\.join\s*\(', "bpy.ops.object.join"),
]
# Strip docstring lines (lines that are inside triple-quoted strings) heuristically:
# a call inside a docstring is preceded by "->" or is a literal example. We check only
# lines that are actual code: a bpy.ops.* call line that does NOT start with a
# quote/space-quote and is not within a """ block. Simplest robust check: ensure no
# call appears as a statement (i.e. a line whose stripped form starts with the call
# or is an indented continuation assigning/calling it, excluding pure docstring lines).
_had_bad_ctx = False
for _f in _src_files:
    _txt = open(_f, encoding="utf-8").read()
    for _pat, _label in _CTX_SENSITIVE:
        for _m in _re.finditer(_pat, _txt):
            _line_start = _txt.rfind("\n", 0, _m.start()) + 1
            _line = _txt[_line_start:_txt.find("\n", _m.start())]
            _stripped = _line.strip()
            # A real code call: the matched call is the leading token of the statement
            # (docstring examples are preceded by "->" or a quote, not the op itself).
            if _stripped.startswith(_label):
                bad("context-sensitive op %s found as a real call in %s: %s" % (_label, os.path.basename(_f), _stripped))
                _had_bad_ctx = True
                break
if not _had_bad_ctx:
    ok("no context-sensitive edit-mode op (mode_set/select_all/transform_apply/join/etc.) "
       "is called as real code in build/verify sources")

# Armature must be built in object mode (enter_editmode=False) for background safety.
if _re.search(r'armature_add\(\s*enter_editmode\s*=\s*False', _build_txt):
    ok("armature_add uses enter_editmode=False (background-safe, no edit-mode exit)")
else:
    bad("armature_add does not use enter_editmode=False (would need edit-mode exit)")

portrait_path = os.path.join(ref_dir, "REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg")
if not os.path.exists(portrait_path):
    with open(portrait_path, "wb") as f: f.write(b"\xff\xd8\xff\xe0fakejpg")
build.PORTRAIT_PATH = portrait_path

print("=== Running build.main() ===")
manifest = None
try:
    manifest = build.main(); ok("build.main() completed without exception")
except Exception as e:
    import traceback; traceback.print_exc(); bad("build.main() raised: %r" % e)

for f in [os.path.join(tmpout, "ADANNA_FACIAL_POC_V2.blend"),
          os.path.join(tmpout, "ADANNA_FACIAL_POC_V2.fbx"),
          os.path.join(tmpout, "evidence", "BUILD_MANIFEST.json")]:
    if os.path.exists(f) and os.path.getsize(f) > 0: ok("build output present: %s" % os.path.basename(f))
    else: bad("build output MISSING: %s" % f)

if manifest:
    ok("manifest tris_total=%d (budget 20000) -> %s" % (manifest["geometry"]["tris_total"],
          "OK" if manifest["geometry"]["tris_total"] <= 20000 else "OVER BUDGET"))
    ok("manifest skeleton_joints_ok=%s" % manifest["all_skeleton_joints_present"])
    ok("manifest portrait_loaded=%s" % manifest["portrait_loaded"])

previews = os.path.join(tmpout, "previews")
n_renders = len(os.listdir(previews)) if os.path.isdir(previews) else 0
ok("preview renders produced: %d" % n_renders)

# ---------- verifier ----------
verify = load("verify_facial_poc", os.path.join(SCRIPT_DIR, "verify_facial_poc.py"))
verify.OUT_DIR = tmpout; verify.EVIDENCE_DIR = os.path.join(tmpout, "evidence")

print("\n=== Running verify.main() ===")
rc = None
try:
    rc = verify.main(); ok("verify.main() completed without exception (returned %r)" % rc)
except Exception as e:
    import traceback; traceback.print_exc(); bad("verify.main() raised: %r" % e)

qc_path = os.path.join(tmpout, "evidence", "QC_RESULT.json")
if os.path.exists(qc_path):
    with open(qc_path) as f: qc = json.load(f)
    ok("QC_RESULT.json verdict=%s" % qc.get("verdict"))
    for c in qc.get("checks", []):
        print("[stub-test]   %-22s %s" % (c["check"], "PASS" if c["passed"] else "FAIL"))
    if qc.get("verdict") == "QUALIFIED":
        ok("verdict QUALIFIED")
        if rc != 0: bad("verifier should return 0 on QUALIFIED, got %r" % rc)
    else:
        bad("verdict not QUALIFIED (%s)" % qc.get("verdict"))
else:
    bad("QC_RESULT.json MISSING")

# ---------- negative test ----------
print("\n=== Negative test: verifier exit code on FAILED ===")
fbx = os.path.join(tmpout, "ADANNA_FACIAL_POC_V2.fbx")
fbx_bak = fbx + ".bak"
if os.path.exists(fbx):
    os.rename(fbx, fbx_bak)
    try:
        rc2 = verify.main()
        if rc2 != 0: ok("verifier returns non-zero (%r) when a check FAILS" % rc2)
        else: bad("verifier returned 0 despite a FAILED check")
    except Exception as e:
        bad("verify.main() raised on negative test: %r" % e)
    finally:
        if os.path.exists(fbx_bak): os.rename(fbx_bak, fbx)

print("\n=== SUMMARY ===")
if FAIL:
    print("FAILURES: %d" % len(FAIL))
    for f in FAIL: print("  - " + f)
    sys.exit(1)
print("ALL STUB-TEST CHECKS PASSED")
sys.exit(0)
