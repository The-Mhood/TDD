# PRODUCTION WORKFLOW — M1 AND SCALE-UP

## Current workspace reality

The sandbox is CPU-only with approximately 4 GB RAM, no Blender executable, and no detected GPU. It cannot justify a hardware purchase or certify render-farm capacity. M1 therefore uses a reproducible, versionable CPU pipeline:

- **Geometry and scene:** Python 3 + NumPy + trimesh.
- **Portable delivery:** glTF 2.0 GLB with named nodes and PBR material intent; OBJ for geometry interchange.
- **Reference colour/management:** exact approved board palette sampled with Pillow; no calibrated texture maps claimed.
- **Render proof:** a deterministic in-repo CPU triangle rasterizer with z-buffer, low-key side/far lighting, atmospheric depth, contact shadows, vignette, bloom, and grain.
- **Review:** PNG hero/three-quarter/side views, turntable GIF, source/reference comparison sheet, and local static preview.

This is a production-quality **stage proof**, not a beginner exercise and not a claim that the sandbox is the final studio.

## M1 execution sequence

1. Preserve exact source ID, hash, approval text, palette, and restrictions.
2. Build stable modules at neutral proxy scale: carved/forked post, lashings, roof bay, earthen bench, wall/opening, stool, exposure cards.
3. Assemble named geometry nodes and export GLB/OBJ plus a production manifest.
4. Render from actual 3D geometry with a low central camera derived from the approved board's one-point composition.
5. Evaluate against the approved board, Art Bible direction, and Phase 1 restrictions.
6. Record exact next milestone in `PHASE_2_PROGRESS.md`.

## Recommended scale-up toolchain

Use the existing H0–H11 gates in `TDD_PHASE2_PRODUCTION_READINESS_AUDIT_v1/H_RECOMMENDED_PRODUCTION_PIPELINE.md`.

- **One version-pinned primary DCC:** Blender is the reasonable consolidated choice unless an existing, staffed Maya pipeline is proven. Re-benchmark before pinning release and plug-ins.
- **Modelling/sculpting:** primary DCC for hard-surface architecture and modular blockout; ZBrush or equivalent only for demonstrated hero sculpt needs.
- **Retopology/UVs:** primary DCC plus a dedicated UV tool when hero texel density or UDIM scale requires it. No universal all-quad or polygon rule.
- **Materials/texturing:** Krita or equivalent for source-preserving paint; Substance 3D Painter/Designer or Mari only when hero texturing/UDIM and artist proficiency justify them.
- **Rigging/animation:** environment M1 needs none. Character work later requires a separate approved Adanna technical interpretation before body/face/groom/cloth rigging.
- **Lighting/rendering:** Cycles or an equivalently benchmarked production renderer; pin colour management, render settings, AOVs, and review transforms before release.
- **Compositing/edit:** Blender compositor or Fusion for a small team; Nuke only when shot/AOV/deep/team scale justifies it. DaVinci Resolve or an equivalent validated NLE/colour/QC path.
- **Interchange/storage:** GLB/USD/Alembic/FBX only for proven handoffs; Git for code/manifests; versioned large-file storage with tested backup/restore for native art, textures, caches, and renders. Keep canonical Google Drive sources immutable.
- **Capacity:** measure representative hero skin/braids/cloth, repeated earthen/thatch sets, dark interiors, volumes, and worst rig/cache case before any hardware/licence purchase.

## Milestone roadmap

- **M1 (this deliverable):** approved-source H2/H3 modular blockout, named GLB/OBJ, material intent, and CPU look-dev renders.
- **M2:** CD-approved shared Chapter 8 spatial/metric/camera interpretation → final H3 modular kit, UVs, and validated handoff.
- **M3:** H4 earth/hardwood/thatch PBR materials and H9 representative moving-camera lighting/render proof.
- **M4:** only after separate authority, character technical interpretation, modelling, hair/clothing, rigging, and facial systems.
- **M5:** scene construction, animation, motion graphics, VFX, and compositing from an approved timed shot package.
- **M6:** measured capacity benchmark, final render/AOV/comp workflow, and production-scale reuse.

No stage silently changes approved design, canon, cultural authority, or source bytes.
