# Adanna Facial-Likeness PoC — Owner-Mac Runbook

**The Disobedient Daughter · Zero-budget facial likeness (TDD-IMPL-FACIAL-001)**
**Status:** EXECUTION READY — **v2.2 BACKGROUND-SAFE** (all context-dependent Blender operators removed; BMesh for mesh editing; portable shell error handling). **Logic-tested in-sandbox** (stub-bpy end-to-end run: build produces all outputs, verifier returns QUALIFIED, non-zero exit on FAILED) **+ syntax-verified**. **Functional validation = the owner-Mac Blender run** (the one genuine environment-specific step). Strategy (DP-01) is OWNER APPROVED; this PoC is **not** technically approved until the owner runs it and returns the evidence. **PM owns driving this to a finished face.**
**Verification authority:** the owner Mac (Blender 4.2.23 LTS + UE 5.8.4) is the only machine that can build/import/verify. The agent completed everything possible in-sandbox (pipeline authored, reviewed, syntax-verified, runbook staged); the owner executes the single required Mac step and returns the evidence. This is not a convenience handoff — Blender cannot run in the agent environment.

## What this PoC is
The proof-of-concept from the zero-budget strategy: build **one** Adanna facial likeness (sculpt → retopo → PBR texture → facial rig → expression turntable → UE import) from the approved master portrait, to demonstrate the **actual achievable quality** before full production commits. **The deliverable is the actual built face with renders + QC + evidence — not the pipeline itself.**

**Approved reference anchor:** `REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg` (Google Drive ID `1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF`, 380 KB, confirmed accessible). **v2 loads this portrait as a modelling reference** — see Step 1.

## v2.1 repair (addresses the owner's five defect findings + two functional bugs)
1. **Portrait-guided facial base block** — the head is now a face-appropriate mesh (cranium + jaw/mandible + facial landmark regions) shaped to portrait proportions, not a naked scaled sphere.
2. **Portrait loaded** — the approved portrait is loaded as a modelling reference (image + backdrop), and its aspect drives head proportions.
3. **Full shared skeleton** — the armature now builds the complete `HUMAN_BASE_PROPOSED` (11 joints), not just head + facial controls.
4. **Consistent binding** — every mesh (head + all accessories) is bound to the armature: head with automatic weights; head-level accessories to the `head` bone; body-level accessories to `pelvis`.
5. **QC verifier corrected** — n-gon triangle count, robust UV/weight/portrait/binding checks.
6. **[v2.1] Verifier opens the saved .blend** — the verifier runs as a separate `blender -b` invocation; it now opens `ADANNA_FACIAL_POC_V2.blend` first (without this it checked an empty scene and would always FAIL).
7. **[v2.1] Backdrop excluded from FBX** — the portrait reference backdrop is removed before FBX export so the FBX contains only the character meshes + armature.

## Files (this directory)
- `build_adanna_facial_poc.py` — Blender headless build v2.1 (portrait-guided facial base + identity features + PBR slots + full skeleton + facial rig + turntable + FBX 7.400 + manifest).
- `verify_facial_poc.py` — Blender headless QC v2.1 (opens the .blend; checks integrity, scale, geometry, topology, UV, material slots, skin weights, skeleton, portrait, binding) → `QC_RESULT.json`.
- `run_facial_poc.sh` — orchestrator (build → verify → evidence bundle).
- `FACIAL_POC_QUALIFICATION_CHECKLIST.md` — the owner-review checklist.

## Step 1 — Preconditions (owner Mac)
- Blender **4.2.23 LTS** installed (free/open-source — the only tool).
- **Place the approved master portrait** at `pipeline/facial_poc/reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg` (or set `PORTRAIT_PATH` to its location). v2 loads it as the modelling reference; without it the pipeline warns and uses proportion defaults (the portrait is required for the likeness verdict).
- No paid tools, no cloud. Everything runs locally.

## Step 2 — Run the Blender pipeline
```bash
cd pipeline/facial_poc
chmod +x run_facial_poc.sh
# Optionally: export PORTRAIT_PATH="/path/to/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg"
./run_facial_poc.sh
```
This writes `output/` with: `ADANNA_FACIAL_POC_V2.fbx`, `.blend`, `previews/*.png`, `turntable/frame_*.png`, `evidence/BUILD_MANIFEST.json`, `evidence/QC_RESULT.json`, `evidence/EVIDENCE_BUNDLE_<ts>.txt`.

**If the build fails:** capture `output/evidence/RUN_<ts>.log`, record the failure in the register, and do **not** proceed. Do not claim progress.

## Step 3 — Owner visual review (the likeness test)
Open `output/previews/ADANNA_FACIAL_POC_front.png` (and side / three_quarter / back) **side-by-side with the approved master portrait**. Review against the identity locks:
- Deep brown skin; thin braids, top half in high knot ✓
- **Left** temple: 3 bronze cuffs + 2 coral beads ✓
- **Left** cheekbone: diagonal scar ✓
- Coiled bronze armlet on **left** upper arm ✓
- Spiral bronze pendant (fictional) ✓
- Indigo hand-woven wrap ✓
- Guarded/defiant default expression ✓
- **No gold; never mirrored; identifying features not moved/duplicated** ✓

Watch the `turntable/frame_*.png` sequence for the expression turntable (neutral → guarded → blink → jaw).

**Verdict:** does the face read as the approved identity at gameplay camera distance, or is it generic/artificial/inconsistent? Record PASS/FAIL with the evidence.

## Step 4 — UE import + integration acceptance
Hand `ADANNA_FACIAL_POC_V1.fbx` to Engineering per `M1_ASSET_INTEGRATION_SPECIFICATION.md`:
1. Import to `/Game/TDD/Characters/Adanna/` as Skeletal Mesh against `Skeleton_HUMAN_BASE_PROPOSED`.
2. Bind skeleton; verify bone names match (pelvis/spine/head/…).
3. Check collision (capsule) + LOD.
4. Resolve materials/textures (no missing textures; PBR slots populated).
5. Spawn in the M1 greybox map; render; run the integration acceptance tests (spec §6).
6. Capture the owner-Mac UE verification bundle (checksums, import exit, spawn render).

## Evidence required to close the PoC
- `output/evidence/EVIDENCE_BUNDLE_<ts>.txt` (build + QC)
- Owner visual-review verdict (PASS/FAIL) with the preview comparison
- UE import + acceptance bundle (owner Mac)

**Do not mark the PoC QUALIFIED / production-approved until all three exist and pass.** No AAA claim without this evidence.

## v2.2 background-safe rewrite (owner-Mac run `2693a3f` failure)
The v2.1 run failed at `bpy.ops.object.select_all(action="DESELECT")` — a context-dependent operator that requires a valid UI context and fails in Blender background mode. v2.2 eliminates **every** context-dependent operator:

| Removed operator | Background-safe replacement |
|---|---|
| `bpy.ops.object.select_all` | data API: `for o in bpy.data.objects: o.select_set(False)` |
| `bpy.ops.object.transform_apply` | `apply_scale_data()` (transform verts by scale, reset scale) |
| `bpy.ops.object.mode_set` (mesh edit) | BMesh for all mesh editing (no edit-mode context) |
| `bpy.ops.mesh.select_all / subdivide / remove_doubles` | `bmesh.ops.subdivide` / BMesh collection ops |
| `bpy.ops.object.join` | head/jaw kept as separate bound meshes (no merge) |

Kept (background-safe with data-API selection): mesh primitives, `armature_add`, `parent_set`, `render`, `export_scene.fbx`, `wm.save_as_mainfile`.

**Additional bugs fixed in the v2.2 audit** (caught by the in-sandbox logic test, invisible to syntax checks):
- `primitive()` helper double-appended `_add` -> `primitive_plane_add_add` (AttributeError on first primitive).
- `bmesh.update_mesh(mesh, ...)` was missing the required `bm` argument (TypeError).
- Tri-budget overrun: `torus_add` defaults (128x32 segments) + `subdivide(2)` on a 64x48 sphere would exceed the 20k-tri QC budget. Segment counts now explicit/modest; head/jaw subdivide reduced to 1 cut (estimated ~11k tris, under budget).
- `verify_facial_poc.py` used `bm.from_mesh(me)` (not a BMesh method) -> corrected to the module function `bmesh.from_mesh(me)`.
- `run_facial_poc.sh` used non-portable `sha256` (exit 127 on systems with only `sha256sum`/`shasum`) -> portable `hash_file()` helper.

## Sandbox logic test (regression)
`test_facial_poc_stub.py` runs the **real** `build.main()` + `verify.main()` against a faithful fake `bpy`/`bmesh`/`mathutils`, exercising control flow, BMesh calls, file outputs, QC verdict logic and exit codes. **This is NOT Blender execution** (Blender cannot run in-sandbox) — it is a logic-level regression test. Run: `python3 test_facial_poc_stub.py`. It confirms: build produces `.blend`/FBX/manifest/renders; verifier returns QUALIFIED with all 10 checks PASS; verifier exits non-zero on a FAILED check; the shell orchestrator exits non-zero on build failure, QC failure, and missing artifacts.

## v2.3 colour-socket fix (owner-Mac Blender 4.2.23 run failure)
The v2.2 pipeline failed in real Blender 4.2.23 at `build_adanna_facial_poc.py:133`:
`bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)`. The function
**always appended alpha 1.0**, but every call site supplies **RGBA (4 components)**,
so the assignment produced a **5-component** value. Blender colour sockets require
**exactly 4 components**, so the call raised.

**Fix — `normalize_color(base_color)`:**
- Accepts **RGB (3)**: appends alpha `1.0`.
- Accepts **RGBA (4)**: used unchanged.
- Rejects any other length with a clear `ValueError`.
- `make_pbr_material` now calls `normalize_color(base_color)` instead of `(*base_color, 1.0)`.

**Call-site audit (all material call sites):**
- `make_materials()` — 8 materials (`skin_base_v1` … `cloth_indigo_v1`), all RGBA.
- line ~357 — `coral_bead_v1`, RGBA.
- Emission Color (line ~238) uses an explicit 4-tuple `(1.0,1.0,1.0,1.0)` — unaffected.
- No other `default_value` colour-append defect exists. **All call sites are now safe
  under the fixed function** (RGBA passes through; RGB would also work).

**Stub-test hardening:** `test_facial_poc_stub.py` now enforces 4-component RGBA on
colour sockets (`Base Color`, `Emission Color`), so this defect class is caught by
the logic test (the broken code raises; the fixed code passes). Explicit
`normalize_color` unit tests cover RGB→RGBA, RGBA-unchanged, and invalid-length rejection,
plus a regression test for the exact failing caller form.

**Verification status — HONEST:**
- ✅ Code fix complete; all call sites audited; logic test (`test_facial_poc_stub.py`)
  passes and now catches the defect class. **This is mocked-bpy logic verification, NOT
  Blender execution.**
- ❌ **Real Blender 4.2.23 execution was NOT performed.** This agent environment has
  **no Blender installation and cannot fetch one** (outbound access is restricted to
  GitHub/npm/PyPI — no Blender mirror). Background-mode Blender runs are owner-Mac-only.
- Therefore the pipeline is **NOT represented as QUALIFIED or Blender-verified**. The
  QUALIFIED target requires real Blender 4.2.23 execution (build exit 0, valid
  `.blend`+FBX, 4 previews + turntable renders, 10/10 QC checks, complete manifest +
  evidence bundle, visual inspection), which only a Blender-capable environment can
  provide. No mock test is presented as proof of Blender completion.
