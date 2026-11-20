> Coverage-qualified working audit. Phase2 all-file inspection is incomplete; no approval/execution is issued.

# I. Software and hardware recommendations

## I1. Decision basis and limitations

The actual film cut, workstation/OS/GPU/VRAM/RAM, licences, team capacity, budget and deadline have **not been established from inspected evidence**. Remaining resource documents must be checked before requesting them again. No exact workstation purchase, tool subscription, farm booking, price or current 'latest version' claim is made here.

The quality target is grounded cinematic animation/dark fantasy with potentially demanding skin, braids/cloth, earthen/thatch sets, water/volumes and selected emissive effects—not necessarily every proposed game feature. The owner can act as CD and commission specialists. The recommendation is to minimize **unnecessary pipeline complexity**, not artistic or technical standards.

## I2. Essential versus conditional tools

| Capability | Recommended starting approach | When a specialist/paid alternative earns its cost |
|---|---|---|
| Native modelling, layout, rigging, animation, rendering | **One version-pinned capable DCC.** Blender is a reasonable consolidated option; Maya is reasonable if the actual team/pipeline already depends on it. Validate the chosen release/plug-ins on the benchmark. | A second DCC only for a demonstrated interchange or specialist need. Do not buy both for perceived prestige. |
| Reference, paint and texture preparation | Krita or equivalent layered paint tool; DCC-native painting/procedural materials for appropriate assets. Preserve original references and distinguish colour/data maps. | Substance 3D Painter/Designer or Mari where hero texturing, masks/UDIM scale and assigned artist proficiency measurably improve delivery. No automatic high-end texture suite for all dressing. |
| Sculpting | Existing DCC sculpting may suffice for approved forms and the assigned artist. | ZBrush or equivalent for demonstrably heavy hero sculpt/detail workflows under a specialist. A polished sculpt is still not an animation-ready model. |
| Garment/groom/FX | Start with the chosen DCC's supported tools and controllable animation; test actual braids, fabric and effects. | Marvelous Designer, dedicated grooming or Houdini when approved shot complexity demands pattern/simulation/procedural control and someone qualified owns it. CH07 does not get wind or flame because the tool supports it. |
| Compositing | A reliable scene-linear/layer-aware compositor; Blender compositor or Fusion may be enough for the selected shot package. | Nuke or another specialist pipeline when shot/AOV/roto/deep/large-team demands and available expertise justify it. No complex deep pipeline without an actual need. |
| Edit, review and delivery QC | DaVinci Resolve or another validated NLE/colour/QC workflow appropriate to actual OS/licence/delivery. Agree review transforms, frame rate and audio handoff. | Paid editions/features only when required by delivery/colour/performance/collaboration, not automatically. |
| Tracking, source control and storage | Structured CSV/JSON/issue tracker plus explicit asset/shot manifests; Git for code/config; versioned large-file art/cache storage with tested backup/restore. Keep canonical Drive sources untouched. | A production-tracking suite/NAS/central asset service when real team concurrency, security and data volume exceed a simple controlled workflow. |
| Interchange and distributed rendering | Keep native scenes primary; test the few required exports. Local validated rendering is the initial benchmark, not an assumption about final throughput. | USD/Alembic/FBX services, farm management and remote GPU capacity only when multiple applications/artists, cache scale or measured schedule needs justify them. A farm cannot solve an unresolved design. |

**Unnecessarily complex now, unless evidence proves otherwise:** multiple competing render engines, USD/Katana-style orchestration for a small single-DCC team, full crowd/muscle systems, game UI/engine infrastructure, deep compositing by default, per-object high-resolution UDIMs, every weather state and full procedural destruction. Do not add a real-time engine solely because the source project was a game. Evaluate it only for a specific approved virtual-production/real-time delivery need.

## I3. Provisional capability tiers — not purchase specifications

| Planning tier | Useful capability target | Restriction |
|---|---|---|
| Reference/editorial/light proxy work | Existing reliable machine; responsive SSD workspace, adequate RAM for actual source/cut sizes and a supported display/codec path. | Benchmark first. No need to buy a hero-render workstation merely to catalogue references or edit proxies. |
| Consolidated hero-asset / moderate shot development | **64GB RAM and roughly 12–16GB GPU memory** are reasonable candidates to test for this kind of look; fast local SSD scratch/work storage and a calibrated review path matter. | Not a universal minimum, not proof of sufficiency and not a specific product recommendation. Renderer/OS/tool support and measured scene load decide. |
| Dense groom/cloth/volume/heavy assembly work | Test whether **128GB RAM / 24GB-class VRAM or higher-capacity workers** are needed, or whether proxies, instancing, partitioning and controlled caches solve the load. | Only a measured high-load shot and funded schedule justify the upgrade. More hardware does not replace good assets/lighting or specialist skill. |
| Final throughput / resilient storage | Measured render workers, independent backup with restore test, sufficient cache/output volume, power protection appropriate to the actual site and reliable versioned handoffs. | Do not assume the audit sandbox represents the owner's machine, network or studio infrastructure. No speculative local-price quote. |

A colour-managed display/review path, dependable storage and restore procedure are production requirements at the relevant stage. A powerful GPU without adequate memory, backups, source authority or disciplined versioning is not a production pipeline.

## I4. Capacity and cost worksheet

Use the actual cut and benchmark—not invented duration or a still-image average:

- `frames = sum(ceil(approved_shot_duration_seconds × delivery_fps) + approved_handles)`.
- `render_worker_hours = frames × measured_p95_seconds_per_frame / 3600`.
- `elapsed_render_hours ≈ render_worker_hours / effective_concurrent_workers`, then add measured setup, failed-frame retry, cache/IO, comp and QC allowances. Hardware concurrency is not the same as usable throughput.
- `output_storage = measured_bytes_per_frame_with_required_layers × frames × retained_output_versions`; add native assets, texture/groom/FX caches, editorial media and independent backups separately.
- `cost = actual labour + approved licences + tested local/remote compute + storage/transfer/backup + agreed contingency`. Use real quotes only after scope and capacity are known.

Benchmark the representative **selected** cases: hero skin/eyes/braids/cloth; repeated thatch/foliage/earth; darkest readable interior/void; water/volume/emission where used; worst camera/rig/cache case. Record app/renderer/settings, peak RAM/VRAM, median/p95 frame time, IO, viewport/rig responsiveness, temporal artefacts and restore/reopen result. Agree headroom against the schedule rather than promising a universal safety percentage.

---

