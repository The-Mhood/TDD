# Adanna Facial PoC — Blender 4.2.23 BMesh / API Comprehensive Audit

**Document ID:** TDD-IMPL-FACIAL-AUDIT-002 · **Date:** 2026-11-22
**Trigger:** Owner-reported failure at `build_adanna_facial_poc.py:298` —
`AttributeError: BMeshOpsModule: operator "subdivide" doesn't exist`.
**Scope:** Comprehensive audit of the ENTIRE facial PoC pipeline against the real
Blender 4.2.23 Python API (not an isolated traceback fix).
**Commit:** `8937332` (v2.4). **Status:** corrected in-sandbox; **NOT Blender-verified**
(Blender 4.2.23 is not installed in this sandbox and cannot be fetched).

## 1. APIs audited (complete inventory)

Every Blender API surface used by `build_adanna_facial_poc.py`,
`verify_facial_poc.py`, and `run_facial_poc.sh` was checked against the Blender
Python API reference and, for the bmesh operators, the Blender C source
(`source/blender/bmesh/operators/bmo_subdivide.c`).

### BMesh module
| API | Where | Verdict |
|---|---|---|
| `bmesh.new()` | build 295, 321; verify 105 | ✅ correct module function |
| `bm.from_mesh(me)` | build 296, 322; verify 106 | ✅ correct instance method |
| `bm.to_mesh(me)` | build 311, 325 (after fix) | ✅ correct instance method |
| `me.update()` | build 312, 326 (after fix) | ✅ correct Mesh method |
| `bm.free()` | build 314, 328; verify 117 | ✅ correct instance method |
| `bm.faces.ensure_lookup_table()` | build 297, 323; verify 107 | ✅ correct |
| `bmesh.ops.subdivide_edges(bm, edges, cuts, use_grid_fill)` | build 298, 324 (after fix) | ✅ correct operator name + params |
| `bmesh.ops.subdivide(...)` | build 298, 324 (BEFORE fix) | ❌ **INVALID** — operator is `subdivide_edges` |
| `bmesh.update_mesh(...)` | build 311, 325 (BEFORE fix) | ❌ **INVALID** — not a module function; use `bm.to_mesh` + `me.update()` |
| `bmesh.from_mesh(...)` | (removed in v2.3) | ❌ invalid — instance method only |

### bpy.ops (background-mode safety)
| API | Verdict |
|---|---|
| `bpy.ops.wm.read_factory_settings(use_empty=True)` | ✅ background-safe |
| `bpy.ops.mesh.primitive_*_add(**kw)` | ✅ background-safe |
| `bpy.ops.object.armature_add(enter_editmode=False, ...)` | ✅ background-safe (v2.3 fix) |
| `bpy.ops.object.parent_set(type=ARMATURE_AUTO / OBJECT_RELATIVE)` | ✅ background-safe (object-mode, data-API selection) |
| `bpy.ops.render.render(write_still=True / animation=True)` | ✅ background-safe |
| `bpy.ops.export_scene.fbx(...)` | ✅ background-safe; all params valid in 4.x |
| `bpy.ops.wm.save_as_mainfile(filepath=...)` | ✅ background-safe |
| `bpy.ops.wm.open_mainfile(filepath=...)` | ✅ background-safe |
| `bpy.ops.object.mode_set / select_all / transform_apply / mesh.select_all / mesh.subdivide / mesh.remove_doubles / object.join` | ✅ **removed** (v2.3) — context-sensitive, fail in background mode |

### Data API (background-safe replacements)
| API | Verdict |
|---|---|
| `o.select_set()`, `bpy.context.view_layer.objects.active` | ✅ correct |
| `apply_scale_data()` (custom): `me.vertices`, `v.co`, `me.update()`, `obj.scale` | ✅ correct |
| `ensure_uvs()` (custom): `me.uv_layers.new()`, `me.uv_layers[0]` | ✅ correct |
| `arm.data.edit_bones.new()`, bone `.head/.tail/.parent` | ✅ correct (object-mode bone creation) |
| `arm.pose.bones`, `bone.location`, `bone.keyframe_insert()` | ✅ correct |
| `bpy.data.objects.remove(obj, do_unlink=True)` | ✅ correct |
| `bpy.data.cameras.new()`, `bpy.data.objects.new()`, `scene.collection.objects.link()` | ✅ correct |
| `scene.render.engine/resolution/image_settings`, `cam_data.lens` | ✅ correct |

### Materials
| API | Verdict |
|---|---|
| `Principled BSDF` `Base Color` | ✅ correct |
| `Principled BSDF` `Emission Color` / `Emission Strength` | ✅ correct names (4.x rename); now **guarded** (v2.3) |
| `normalize_color()` (custom) | ✅ 4-component RGBA enforcement |

## 2. Lines changed (v2.4, commit `8937332`)

**`pipeline/facial_poc/build_adanna_facial_poc.py`:**
- **Line 298:** `bmesh.ops.subdivide(bm, edges=list(bm.edges), number_cuts=1)`
  → `bmesh.ops.subdivide_edges(bm, edges=list(bm.edges), cuts=1, use_grid_fill=True)`
- **Line 324:** same correction for the jaw bmesh (`bmj`).
- **Line 311:** `bmesh.update_mesh(head.data, bm, selected_only=False)`
  → `bm.to_mesh(head.data)` + `head.data.update()`
- **Line 325:** same correction for the jaw (`bmj.to_mesh(jaw.data)` + `jaw.data.update()`).
- Version strings bumped to v2.4.

**`pipeline/facial_poc/verify_facial_poc.py`:** version string bumped to v2.4
(BMesh usage already correct: `bmesh.new()` + `bm.from_mesh()` + `bm.free()`).

**`pipeline/facial_poc/test_facial_poc_stub.py`:** bmesh fake rewritten to mirror the
REAL API (`subdivide_edges` present; `subdivide` and `update_mesh` ABSENT so invalid
calls raise `AttributeError`). Regression tests added for every invalid/correct pattern.

## 3. Why the v2.3 stub did not catch this

The v2.3 stub modeled the **invalid** API — it defined `bmesh.ops.subdivide` and
`bmesh.update_mesh` as working functions. A stub that mocks an invalid implementation
cannot catch the defect; it passed while real Blender failed. **The stub must mirror
the real API.** This is the same lesson as the v2.3 `bmesh.from_mesh` bug.

## 4. What was NOT changed (confirmed correct)

- BMesh lifecycle (`new` → `from_mesh` → ops → `to_mesh` → `free`).
- All `bpy.ops` calls (background-safe).
- All data-API helpers.
- Armature construction, parenting, modifier setup.
- Rendering and FBX export parameters.
- Verifier logic (10 checks).

## 5. Honest verification limit

Blender 4.2.23 is **not installed in this sandbox and cannot be fetched**. The fixes
are verified against the Blender API reference, the Blender C source, and an
in-sandbox stub that now mirrors the real API (all checks PASS, exit 0). **This is
NOT a real Blender run.** Acceptance still requires, on the owner Mac:
- `run_facial_poc.sh` exits 0,
- valid `ADANNA_FACIAL_POC_V2.blend` + `.fbx`,
- 4 previews + turntable rendered,
- `QC_RESULT.json` QUALIFIED (10/10 checks),
- complete evidence bundle,
- visual likeness review against the approved portrait.

Until that run succeeds, the PoC is **NOT qualified**.
