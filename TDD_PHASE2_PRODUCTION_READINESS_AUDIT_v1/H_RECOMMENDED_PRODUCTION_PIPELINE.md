> Coverage-qualified working audit. Phase2 all-file inspection is incomplete; no approval/execution is issued.

# H. Recommended production pipeline

**Proposed project policy, not a statement that these stages have already been executed.** Existing approved designs/identities remain fixed unless the CD explicitly authorizes change. Technical release is separate from visual/cultural/canon authority.

## H1. Gates and concrete delivery

| Gate / stage | Required input and deliverable | Objective release test / responsible sign-off |
|---|---|---|
| **H0 — Scope and authority** | Selected shot rows; logical asset IDs and exact source versions/hashes; approval/use and Research dependencies. | No unselected game scope or orphan authority. CD/producer approves use; coordinator validates joins. G00 remains a separate audit-completeness requirement. |
| **H1 — Reference preparation** | Source-preserving copies/crops clearly labelled; measured panel/detail limits; anatomical-side key; necessary missing-surface decisions only. | Exact source hashes retained; no new view/detail inferred from crop/upscale; sufficient information for the selected camera/action. CD/department lead approves interpretation, not altered originals. |
| **H2 — Proxy geometry and layout** | Approved units/datums, actor/prop contact envelope, basic set plan/elevations/joins and selected cameras. | Interior/exterior and reverse cuts fit one plan; door, actor and camera paths have no impossible clearance. CD/layout accepts. Proposed metrics are not represented as prior canon. |
| **H3 — Modelling and UVs** | Versioned native mesh; separated body/clothes/rigid props/groom; approved topology/detail and UV/pivot/naming conventions. | No accidental non-manifold/normal/transform errors; required silhouette/deformation surfaces work; UV seams/stretch/texel detail pass actual framing. Modelling/rigging leads sign specialist evidence. No universal polygon count/all-quad rule. |
| **H4 — Materials and texture/look development** | Approved material intent, colour/data spaces, maps and dry/wet/ash masks only as selected; neutral and chapter light tests. | No baked lighting treated as albedo; correct roughness/scale/weathering and identity; no seams/tiling/flicker or unapproved cultural/material claim. CD/look-development signs. |
| **H5 — Rigging, facial and attachments** | Native body/hand/eye/facial controls needed by the cut; prop/groom/cloth interfaces; required expression/action tests. | Required poses/contacts and actual dialogue range without collapse, sliding or intersections; stable anatomical identifiers. No prohibited Okwu face or inferred cavity. Rig/animation leads sign; CD approves acting-read targets. |
| **H6 — Scene assembly and camera/layout** | Published asset versions linked into shot-native scenes; camera sensor/lens/focus/transform, time state and scale record. | No missing dependencies; correct asset/variant and shared spatial continuity; actual shot framing/actor contact works. Layout/continuity/CD accepts. Camera changes are allowed when authorized—no universal pixel lock. |
| **H7 — Blocking → animation** | Timed editorial shot, body/face/eye/prop blocking before polish; required motion only. | CD approves readable performance and staging; animation lead approves contacts/arcs/weight/continuity. Recut or layout changes are resolved before costly final motion and caches. |
| **H8 — Secondary motion / FX** | Stable animation inputs; only required cloth/groom/net/water/ash/lightning/fracture/graphics effects; versioned caches and handles. | Deterministic replay, no penetration or temporal jumps; chapter no-flame/no-wind/WHITE-lightning/cold-rack rules maintained. FX/animation lead signs; CD approves look/timing. |
| **H9 — Lighting and render proof** | Pinned native engine/app/settings, project colour path, approved shot state and representative moving proof; measured memory/time. | Correct skin/black-level/material/lens and chapter continuity; no prohibited reveal; noise, sampling and denoising stable in motion. Lighting/render lead signs technical proof; CD signs look. |
| **H10 — Rendering and compositing** | Versioned image sequences with required beauty/AOVs/IDs/holdouts/volumes, colour metadata, tested alpha/depth/vector conventions and comp scene. | Independent reopen/re-render/recomp; no missing files, bad edges, colour shifts or flicker; required corrections are controllable without repainting the whole shot. Render/comp/QC signs. |
| **H11 — Edit, graphics and final QC** | Approved cut, audio/graphics copy/credits, delivery fps/aspect/colour/container and rights/source manifest. | Frame/handle continuity, title/diacritic legibility, audio sync, exposure/colour consistency, technical conformance and final narrative/CD acceptance; release only exact versions that passed. |

No unseen native asset is certified by these gates. Check any existing package first; do not order a redundant rebuild because this partial audit has not reached it.

## H2. Safe parallel work and change control

**Parallel after H0:** authority/reference indexing; editorial timing; resource/restore tests; approved material test surfaces; model/rig feasibility on controlled provisional interfaces. **Parallel after H2/H3:** texture work on stable UVs, rigging on approved topology, environment dressing on approved layout, lighting look tests on versioned assets. **After blocking:** final animation, then expensive collision-dependent caches; render and comp proof may run early, final frames use signed inputs.

Changes affecting silhouette, proportions, topology, UVs, contact dimensions, skeleton, camera/layout or wardrobe can invalidate downstream work. Raise a specific change record: exact asset/version, why, affected shots/stages, authority, migration/retest cost and approval. Never overwrite approved originals or silently update every linked scene to a new design.

## H3. Proposed native package conventions

These apply to **future working/published production deliveries**, not renaming the existing Drive corpus:

- Stable logical IDs plus variant/state and version; source filenames/IDs remain immutable provenance. Anatomical `L/R` is explicit; viewer-side labels are separate.
- Explicit scene units, axis/up/forward, transforms, pivots and export scale; verify a neutral scale test through actual DCC handoff rather than adopting unapproved story dimensions.
- Separate geometry, materials, textures, rig, groom, caches, cameras/lights and shot assembly; role/layer/collection names are consistent. Shared assets are referenced/version-pinned, not uncontrolled scene copies.
- Model authority, material authority, rig version and permitted use are recorded independently. UV/UDIM, normals, displacement and colour conventions are documented only as needed by chosen tools.
- Each publish carries application/plug-in versions, dependency manifest, source references/hashes, units, tests, restrictions and responsible sign-offs. Reopen on another working machine before handoff is called complete.
- Keep source control for code/config/manifests; use appropriate large-file/versioned storage for native art and caches. Do not put large datasets/renders in ordinary Git or execute historical sync scripts to reorganize canonical Drive.

---

