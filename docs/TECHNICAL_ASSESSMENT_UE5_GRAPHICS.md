# THE DISOBEDIENT DAUGHTER — GAME ENGINE AND GRAPHICS PRODUCTION ASSESSMENT

**Status:** Technical assessment only. Not an implementation authorisation. No decisions herein are approved project decisions.
**Prepared for:** Project owner (direct reporting)
**Prepared by:** Independent technical assessment agent
**Date:** 2026-11-18
**Branch:** `arena/b2c58152-tdd` (assessed against `main` @ `5e3d1da`)
**Repository:** `The-Mhood/TDD`
**Workflow isolation:** No agents, branches, tasks or production schedules were contacted, modified or deprioritised. No dependency is assumed between this assessment and ongoing production. Production work continues uninterrupted regardless of these findings.

---

## 0. EXECUTIVE SUMMARY

1. **No Unreal (or any) game-engine project exists in the TDD repository.** The repository is a single initial commit containing only a one-line `README.md`. There is no `.uproject`, no C++/Blueprint source, no content, no build system, no CI and no Git LFS configuration.
2. **All existing TDD work is design-time 2D material** (concept boards, art direction, world/narrative bibles, decision logs, master character references) held primarily in Google Drive, plus the empty GitHub repository. **Zero game-ready 3D assets, code or audio exist.** Nothing of value would be lost by adopting Unreal Engine 5 now — but everything of value must still be built from scratch.
3. **Recommendation: Unreal Engine 5.8** (released 2026-06-17, the latest full release and the last planned UE5 major) as the pinned engine baseline. UE 5.9 is Preview-only (2026-11-09) and UE6 Early Access is targeted for late 2027 — do not wait for it. Pin to 5.8.x patches; reassess only at milestone boundaries.
4. **The machine used for this assessment cannot develop or validate UE5** (2 vCPU, 3.8 GB RAM, no GPU, ~20 GB disk). It is an agent sandbox, not a development workstation. No local graphics validation has been or can be performed here. The actual development workstation(s) are **not documented anywhere in the repository or Drive** — this is a critical unknown that must be resolved before Milestone 1.
5. **The visual ambition is achievable on UE5.8** with Nanite + Lumen (+ Lumen Lite) + Virtual Shadow Maps + World Partition + MegaLights (production-ready in 5.8) + MetaHuman + Sequencer, provided (a) target platforms are fixed early, (b) min-spec and scalability budgets are enforced from day one, and (c) scope is disciplined. Feasibility is not the risk; **uncontrolled scope and unvalidated hardware are**.
6. **Recommended first milestone:** a *Production Foundation Vertical Slice* — one greyboxed third-person gameplay loop (move/attack/dodge/save) inside a real-scale slice of Home Settlement, built on World Partition + GAS + Enhanced Input, running at 60 fps on the agreed minimum PC spec and one console-class profile, with CI and packaging. **Not a graphics demo** — it is the cheapest possible proof that the complete game is buildable at the intended quality bar.
7. This is an assessment, not an approval. The decisions in §13 require the owner's sign-off.

---

## 1. METHOD AND EVIDENCE GATHERING

**Repository inspection (local, read-only):** `git ls-tree`, `git log`, filesystem listing, `.gitattributes` check, hardware probes (`lscpu`, `free -h`, `df -h`, `nvidia-smi`, `/dev/dri`).
**Google Drive inspection (read-only, connected app `google_drive`):** folder trees of the `THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE` structure (art bible index, character registers, location registers, production reports, approved designs, DECISIONS.md).
**Current official documentation & release data (web, 2026-11-18):** Epic Nanite, Lumen and World Partition documentation (fetched from dev.epicgames.com), UE 5.8 release coverage, UE 5.9 preview coverage, Unity 2026 render-pipeline strategy coverage, and UE licensing/royalty summaries. URLs are cited inline.

Nothing was modified, created, moved, renamed, deleted or committed in Drive. The only file written by this assessment is this document, on branch `arena/b2c58152-tdd`.

---

## 2. CURRENT PROJECT AND ENGINE STATUS (EVIDENCE)

### 2.1 Repository evidence

| Check | Result |
|---|---|
| HEAD commit | `5e3d1da4eee42ad8255760530291ff91cdfb39b2` — "Initial commit" (2026-11-16, `arena-ai-coding-agent[bot]`) |
| Branches | `main` (origin) and `arena/b2c58152-tdd` (current) only |
| Files at HEAD | `README.md` only (6 bytes, content `# TDD`) |
| `.uproject` / `.uplugin` | **None** |
| Source (`.cpp`/`.h`/`.cs`) | **None** |
| Content (`.uasset`/`.umap`) | **None** |
| `.gitattributes` / Git LFS | **Absent** — binary assets would be committed raw if work began today |
| Build system / CI / hooks | **None** |
| Repo size | ~6 bytes of content (shallow clone, `.git/shallow` present) |

**Conclusion: there is no Unreal project, no engine dependency declaration, no art pipeline in-repo, and no implementation of any kind. The repository is an empty placeholder.**

### 2.2 Production status evidence (Google Drive — "THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE", modified Nov 2026)

Recorded structure (top level): `00_MASTER_ART_DIRECTION` … `20_PREVIOUS_VISUAL_AGENT_WORKSPACE_HANDOVER`, plus `DECISIONS.md`, `PENDING`, `CD_REVIEW_2026-11-16`, `17_DOCUMENTATION` (Art_Bible_Index, Location/Character/Asset_Registers, Changelogs, Production_Reports).

- **Characters (9 groups):** Adanna, Ezeani, Nneka, Okwu, Amadioha, Idemili, Hollow King, Supporting_Characters, NPC_Population. Approved: `CHAR_ADANNA_MASTER_REFERENCE_V001`, `CHAR_AMADIOHA_MASTER_REFERENCE_V001`.
- **Locations (9 chapter folders):** Chapter_01_Forbidden_Forest, Chapter_02_Kingdom_Beneath_Earth, Chapter_03_City_of_Living_Dead, Chapter_04_River_of_Idemili, Chapter_05_Mountain_of_Thunder, Chapter_06_Kingdom_of_Masks, Chapter_07_Gates_of_the_Dead, Chapter_08_The_Last_Daughter (Ancestral Realm — KEEP/REVISE/REDO directions), Home_Settlement.
- **Design categories present:** Architecture, Creatures/Enemies, Bosses, Weapons/Armour, Props, Lighting/Atmosphere, Cinematography.
- **Design categories EMPTY at time of inspection:** `09_ANIMATION_AND_COMBAT`, `12_CINEMATOGRAPHY`, `13_GAMEPLAY_AND_LEVEL_DESIGN` (no files) — i.e. **combat and cinematic design has not been produced yet**, only art-direction boards and narrative direction.
- `DECISIONS.md` establishes locked narrative direction (Memory 7 truth; Adanna six years old at Nneka's death; Chapter 8 board KEEP/REVISE/REDO: Sealed Quarter / Nneka's House / Hall of Posts kept; Establishing View / Road of Generations / Wall of Houses / Gathering Ground revised; Folded Stair & Mothers' Courtyard redo).
- `ENVIRONMENTAL_DENSITY_ASSESSMENT.md` (~4.3 KB, 2026-11-15) indicates density is being quantified for environment boards — evidence this is an art-direction workflow, not an engine workflow.
- `14_APPROVED_DESIGNS` (latest batch, 8 items): environment boards for the Ancestral Realm (Sealed Quarter, Nneka's House interior/exterior, Hall of Posts) + Amadioha and Adanna master references + one Wash­ing-Place board.

**Conclusion: the project is a pre-production world, character and art-direction bible with a locked narrative spine — nothing more. No game-ready content, no engine work, no engineering track has visibly started.**

### 2.3 What would be lost or require migration?

| Asset class | In repo today | Action on UE5 adoption |
|---|---|---|
| Code / C++ / Blueprints | None | None to migrate |
| Engine project files | None | None to migrate |
| 3D models / rigs / animations | None | Build from scratch (or commission) |
| 2D boards / concept art (Drive) | Extensive | **Retain as reference only**; re-author as game-ready source in DCC tools (Blender/Maya/3ds Max/ZBrush/SpeedTree/Substance). Boards are not, and are not intended to be, FBX-ready |
| World/narrative bibles (Drive) | DECISIONS.md etc. | Port wholesale into a version-controlled design doc; these become the narrative/quest/memory data source |
| Naming/register conventions in Drive | Character/Location/Asset registers | Reuse as canonical ID schema for the UE content browser (e.g. `CHR_ADANNA`, `LOC_UKWUNNA_…`, `MEM_…`) to prevent a registration reset |
| Git history | One commit | Keep; add `.gitattributes` with LFS for binaries **before** binary work starts, or move to Perforce (§12.6) |

**No existing engineering work would be lost. The migration cost is effectively zero for code and assets; the real cost is pipeline construction (Drive artefacts → DCC → UE) and discipline (LFS/Perforce, registers, naming).**

### 2.4 Game shape implied by existing material

A third-person action-adventure RPG with: open interconnected environments across at least 9 authored chapters + a home hub; high-fidelity characters with facial detail (master references, MetaHuman-class intent); combat (weapon-register implied; combat/animation design not yet done); boss encounters (Hollow King, Idemili, Amadioha figures); exploration + memory/quest narrative system; cinematics (chapter structure, memory framing); African (Igbo-coded) architecture and supernatural realms. This scope class sits squarely in "AA+ / premium AA" territory and is beyond a typical small-indie UE5 project without disciplined scope control.

---

## 3. DEVELOPMENT MACHINE ASSESSMENT (THIS WORKSPACE)

Probed on 2026-11-18 (`lscpu`, `free`, `df`, `nvidia-smi`, `/dev/dri`):

| Component | This machine (agent sandbox) |
|---|---|
| CPU | Intel Xeon @ 2.60 GHz, **2 vCPU** (1 core / 2 threads, KVM virtualised), AVX-512, no IBT/AMX relevance |
| RAM | **3.8 GB** total, 0 swap |
| GPU | **None** (`nvidia-smi` absent; no `/dev/dri`; no `lspci` GPU line) |
| Disk | **21 GB** volume, **~20 GB free** (overlay) |
| OS/runtime | Linux (x86_64), KVM guest |

**Implication:** This environment cannot install, launch, compile, cook, profile or even meaningfully open UE5 (UE requires a DirectX 12 / Vulkan GPU with ≥8 GB VRAM — 12–16 GB+ realistically — 32–64 GB RAM and an NVMe SSD; shader compilation alone would thrash 3.8 GB). **All hardware statements about "actual development machine capability" beyond this sandbox are UNKNOWN from repository evidence and must be supplied by the owner.** Do not schedule graphics work until the real dev hardware is inventoried and benchmarked (§6, §13).

### 3.1 Practical UE5 development requirements (2026 reality)

| Role | CPU | GPU | RAM | Storage | Notes |
|---|---|---|---|---|---|
| Min viable dev station | 8-core (Ryzen 7 7800X3D / i7-14700 class) | RTX 4070-class, 12 GB | 32 GB | 1–2 TB NVMe Gen4 | Can build/greybox; painful for Lumen HWRT |
| **Recommended dev station** | 16-core high-clock (Ryzen 9 7950X / i9-14900K class) | **RTX 4080/4090 or RTX 5080/5090-class, 16–24 GB VRAM** | **64 GB** | **2 TB+ NVMe Gen4/5 (project) + separate drive for DerivedDataCache/builds** | Nanite/Lumen/large worlds; shader compiles |
| Cinematics / Movie Render Graph node | High-core-count (Threadripper/7950X+) | RTX 4090-class, 24 GB | 64–128 GB | 4 TB NVMe | Offline render + path tracing |
| CI / build agents | 16-core | Any DX12 (cook only) or headless with prebuilt DDC | 64 GB | 2 TB NVMe | Automated package + smoke tests |
| Source control server | Perforce (Helix Core) or Git+LFS | — | 32 GB | Large NVMe, off-site backup | Binary art assets demand this |

**Target-player hardware is a different question from development hardware** (§7). Players do not need 64 GB or a 4090; the game must be *authored and validated on* high-end hardware but *budgeted for* a defined min-spec.

### 3.2 Recommended player-facing hardware tiers (to be approved)

- **Minimum (PC):** RTX 3060 / RX 6700 XT (12 GB VRAM), 16 GB RAM, NVMe/SSD, DX12, TSR upscaling, 1080p/30–60 — Lumen off or Lumen Software/Lumen Lite, Nanite on, Low–Medium scalability.
- **Recommended (PC):** RTX 4070 / RX 7800 XT (16 GB), 32 GB RAM, 1440p/60 — Lumen HWRT High, Nanite full, VSM, High scalability.
- **Epic/Cinematic (PC):** RTX 4080+/24 GB — 4K/60 or higher, all features + MegaLights, 5.8 Cinematic scalability.
- **Consoles:** PS5 / Xbox Series X — target **60 fps Performance mode** (Lumen Lite / scalable GI) + **30 fps Quality mode**; Series S likely needs aggressive tuning or is out; **Switch 2** only with Lumen Lite + heavy cutbacks or deferred post-launch (decision required).
- **Dev ≠ player:** every dev station above Recommended tier; **every** performance decision gated on the Minimum tier + one console profile, not on the dev box.

---

## 4. ENGINE RECOMMENDATION: UNREAL ENGINE 5.8

### 4.1 Version position (as of 2026-11-18)

- **UE 5.8** — released 2026-06-17; the latest full release and the last planned UE5 major; headline: production-ready **MegaLights** (60 fps targets on current-gen consoles), **Lumen Lite** (lightweight dynamic GI toward 60 fps on Switch 2 / PC), mesh-based terrain system, improved PSO precaching, updated character/animation tools, updated MetaHuman devkit (Python/Blueprint batch automation, conform in varied poses) and markerless mocap plugin ([UE 5.8 release notes](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274), [coverage](https://cgchannel.com/2026/06/see-5-key-features-for-cg-artists-in-unreal-engine-5-8/), [coverage](https://overclock3d.net/news/software/unreal-engine-5-8-delivers-megalights-and-lumen-lite-with-60-fps-performance-targets/)).
- **UE 5.9** — Preview 1 only (2026-11-09): Lumen World Cache (HWRT path-traced cache), Nanite culling improvements, experimental web builds, AI tooling; full release planned for 2027, no date ([5.9 preview analysis](https://maverickframe.com/blog/unreal-engine-latest-version/)).
- **UE 6** — Early Access targeted late 2027. Not a production basis now.

**Pin the project to UE 5.8.x (latest 5.8 patch, e.g. 5.8.4) and treat engine upgrades as milestone-boundary decisions only.** Do not start on 5.9 Preview; do not wait for UE6.

### 4.2 Why UE5 fits this game specifically

| TDD requirement | UE5.8 capability | Fit |
|---|---|---|
| High-fidelity characters & facial detail | **MetaHuman** (in-engine, batch-scriptable in 5.7/5.8) + Live Link/mocap + Take Recorder | Best-in-class, no competing native equivalent |
| Cinematic combat & animation | Control Rig (in-engine anim), IK Retargeter, Motion Warping, linked Anim Layers, Anim Dynamics, Pose Search (Motion Matching), Sequencer + Movie Render Graph | Complete internal stack; no middleware required |
| Detailed environments / huge counts of assets | **Nanite** virtualized geometry — "multiple orders of magnitude" more geometry, automatic LOD, no manual LOD authoring ([Nanite docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine)) | Core to impossible earthen architecture + dense markets/forests |
| Realistic African environments, supernatural realms | **Lumen** dynamic GI/reflections, infinite bounces, mm→km scale; **MegaLights** (many shadow-casting lights, e.g. compound interiors, firelight) production-ready in 5.8 ([Lumen docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine)) | Designed for exactly this dynamic-lighting ambition |
| Large interconnected environments | **World Partition** (distance streaming, single persistent level, One File Per Actor, Data Layers, HLOD) — replaces manual sublevel streaming and fixes multi-editor conflicts ([World Partition docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine)) | Chapter-based world = grid cells + data layers (day/spirit-state variants) |
| Cinematics & storytelling | **Sequencer** + Movie Render Graph + Take Recorder + Camera Cut tracks + in-game cinematics | Purpose-built; matches Memory-chapter structure |
| VFX / supernatural effects | **Niagara** (GPU sim, scalable, sequencer-integrated) | Idemili waters, Mask-kingdom fires, memory transitions |
| Gameplay framework & code | C++ core + Blueprint exposure; Gameplay Ability System, Gameplay Tags, Enhanced Input, StateTree, Mass (crowds), PCG (foliage/scatter, production-ready in 5.7) | Strong AA-grade action-combat foundation; Lyra sample as reference architecture |
| Foliage / forests | Nanite foliage (experimental since 5.7) + PCG | Forests/riverbanks at scale with care |
| Water (River of Idemili) | Single Layer Water + Water plugin + Niagara | Native |
| Commercial console viability | First-party PS5/Xbox Series pipelines; certification know-how in market | Required for premium release |

### 4.3 Unity — only the material reasons to consider it, and why they don't apply

This is not a generic engine comparison. Unity is materially relevant only on these axes:

1. **High-fidelity rendering trajectory (decisive).** In February 2026 Unity confirmed **HDRP is in maintenance mode** — no new features; effort limited to Switch 2 support and stability; **Built-in RP deprecated in 6.5** (supported to ≥ end-2028); URP is the strategic focus but is not a Nanite/Lumen-class equivalent. For a 36-month high-fidelity production, choosing Unity now means committing to a **frozen high-end feature set** precisely where TDD needs headroom ([render-pipeline strategy coverage](https://gamefromscratch.com/the-unity-hdrp-is-dead/), [technical analysis](https://nastyrodent.com/unity-hdrp-vs-unreal-engine-5/)).
2. **Character-fidelity tooling (decisive).** MetaHuman, in-engine rigging, IK retargeting and markerless mocap have no Unity-native parity; assembling equivalents adds middleware cost and risk.
3. **Licensing.** Both are commercially workable: UE — **5% royalty on lifetime gross above US$1M per title** (first $1M royalty-free; 0% on EGS sales); Unity 6 — seat subscriptions (~US$2,310/yr Pro) plus post-2023 policy turbulence. For a game, UE's royalty is aligned and predictable; it is a real cost to model at scale, not a blocker ([royalty terms summary](https://300mind.studio/blog/unreal-engine-licensing-royalties/), [2026 licensing analysis](https://www.itechguides.com/what-happens-if-a-game-engine-changes-its-pricing-or-terms-developer-faq/)).
4. **Where Unity would genuinely win:** mobile reach, 2D, very rapid iteration, larger hiring pool at junior level, live-service ops. **None of these is material to a premium third-person action-adventure RPG with cinematic ambitions.**

**Verdict: UE5.8 is the recommendation on the merits, not on habit.**

### 4.4 Hard UE5 caveats (owned honestly)

- **Hardware hunger:** Lumen/HWRT and Nanite punish weak GPUs; scalability must be designed, not bolted on.
- **Shader compilation stutter:** mitigate with PSO precaching (improved in 5.8) + cooked builds tested from day one.
- **Nanite limits:** not for translucent/masked-foliage everywhere, deforming/skinned meshes are largely outside Nanite (verify skeletal-Nanite status on the pinned 5.8 build before relying on it), and VSM+Lumen add GPU load; VFX (Niagara) and hair use separate paths. Budget per-object, don't assume "everything Nanite = free".
- **Build times/iteration:** full C++ builds are slow; use Live Coding, explicit module design, cook-on-the-fly for iteration, DDC on shared storage.
- **C++ competence required** for anything beyond Blueprint prototyping; Blueprint-only shipping of an AA action RPG is not advisable.
- **Console devkits and first-party approval** are prerequisites for the console target, not options (§13).

---

## 5. RECOMMENDED GRAPHICS TECHNOLOGY STACK (UE 5.8)

| Layer | Recommendation | Notes / limits |
|---|---|---|
| Engine | **UE 5.8.x pinned** (latest patch) | Upgrade only at milestone boundaries |
| Geometry | **Nanite** for all static architecture/props/scan-quality assets; enable on import + batch enable; **not** for sky spheres, translucency, dynamic/deforming meshes | Measure instance counts & triangle totals per scene ([Nanite docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine)) |
| Skeletal/characters | Conventional skeletal meshes + authored LODs (high→low), ~50k–200k tris hero budget; **MetaHuman** for Adanna/Ezeani/Nneka (+ 5.8 devkit Python batch conform) | Cinematic close-ups may use MetaHuman close-up LOD tier |
| GI / reflections | **Lumen** (HWRT where available; Software fallback) on PC/High; **Lumen Lite** for consoles / Switch 2-class targets / 60 fps mode; static lighting only for pre-baked background fill if ever needed | Never mix baked + Lumen per level without a decision; Lumen replaces lightmaps |
| Lights at scale | **MegaLights** (production-ready 5.8) for many-shadow-casting-light scenes (firelit interiors, festivals) | Profile; budget light counts; 5.8 targets ~60 fps current-gen |
| Shadows | **Virtual Shadow Maps** (default) | Requires Nanite/current-gen; tune page pool on min-spec |
| World streaming | **World Partition** + **One File Per Actor** + **HLOD** + **Data Layers** (chapter/realm state variants: e.g. Sealed Quarter open/closed, day/spirit overlays) + Level Instancing for repeated domestic structures | Convert Commandlet available if legacy levels ever appear |
| Foliage & terrain | Landscape + **PCG** (production-ready 5.7) scatter for forests/rivers; **Nanite foliage** only after measuring on min-spec (experimental); SpeedTree or bespoke plant kits | Density budgets per biome; HLOD far-LODS |
| Materials | **Substrate** for hero cloth/skin/metal/wood; **Virtual Texturing**; Single Layer Water (rivers); Hair (Groom) only for hero close-ups with cost cap | Keep material instruction counts disciplined |
| Sky/water/atmosphere | Sky Atmosphere + Volumetric Clouds + Exponential Height Fog + Sky Light (Lumen final gather) + Water plugin | Atmospheric ash/harmattan/dusk palettes per art bible |
| VFX | **Niagara** GPU sims for supernatural FX; calligraphic memory-transition effects; cap GPU sim cost; LOD/cull FX | Hero moments only at Epic quality |
| Animation | Control Rig (procedural + keyframe cleanup), IK Retargeter (mocap→MetaHuman), **Motion Warping** (combat root-motion targeting), Anim Layers per weapon set, Anim Dynamics, optional Pose Search; Motion Matching only with mocap library budget | Author LODs + physics assets per character |
| Cinematics | **Sequencer** + **Movie Render Graph** for marketing/pre-render; in-game Sequencer for memory chapters; Take Recorder for mocap/VO capture | Memory 4–7 sequences are the riskiest scenes; prototype early |
| UI | UMG + **CommonUI** (console focus semantics) | Gamepad-first navigation |
| Audio | **MetaSounds** + Wwise/Resonance optional | Ancestral audio motif library needed |
| Lighting bakery | **None** — go fully dynamic (Lumen) | Simplifies iteration; test on min-spec early |
| Scalability | Explicit `Low/Medium/High/Epic/Cinematic` per platform + **TSR** + dynamic resolution; per-category toggles (GI, reflections, shadows, foliage, view distance, textures, post) | Ship tested profiles per platform, not one PC build |
| Source control | **Perforce (recommended)** or Git + Git LFS with `.gitattributes` **before first binary commit** | Current repo has no LFS — see §12.6 |
| Build/CI | UnrealBuildTool + BuildGraph; nightly packaged builds + smoke tests; PSO caching | Shader-stutter regression gate |

**The single most important discipline rule:** every feature above is enabled "because the art bible demands it", and every feature must pass the min-spec gate in §3.2 and §13. Quality is fixed by the bible; performance is defended by budgets.

---

## 6. RENDERING & SCALABILITY STRATEGY — HIGH QUALITY THAT STAYS OPTIMISABLE

1. **Author at Epic, ship at scalable.** Build content to Epic-quality targets; define Low/Medium/High/Epic deltas per system (Lumen HWRT→Lumen SW→Lumen Lite→off + SSGI-ish fallbacks; VSM on/off; Nanite always on where supported, conservative VSM pages on min-spec; texture pool 2K/4K; foliage density; view distance; post-process).
2. **Fixed frame budgets.** 60 fps Performance mode (console + min-spec PC, 16.6 ms) / 30 fps Quality mode. Allocate: GPU 12–14 ms, CPU 12–14 ms at 60 fps. Track with `stat unit`, Unreal Insights, and GPU Visualizer from week 1 of Milestone 1.
3. **TSR temporal upscaling + dynamic resolution** as the default; DLSS/FSR where integrations allow; never ship native 4K without upscaling.
4. **Streaming discipline.** World Partition cells sized to the chapter topology; HLOD for far-field; explicit streaming sources; budget IO on HDD-less assumption (NVMe required); measure cell traversal hitches; async load everything narrative (memories, dialogue) — never on the critical frame.
5. **Material & instance budgets.** Per-instance material complexity caps; HISM/ISM for settlement repetition; Substrate only where it pays (hero assets); virtual textures to keep feedback cheap.
6. **VFX governance.** Niagara effect budget per scene; distance culling + scalability replacements; supernatural set-pieces are the graphics "boss fights" — profile them like combat encounters.
7. **Lighting governance.** Lumen + MegaLights for hero areas; strict light-count budgets elsewhere; no real-time GI on background fill if it doesn't read; cooked-build validation, not editor-only.
8. **Measure, don't assume.** Every week of Milestone 1 exports a hardware-class performance report (min-spec PC + one console-class GPU). Regressions block merges, not morale.
9. **PSO precaching + cooked DDC + packaged smoke tests in CI** to eliminate first-play shader stutter.
10. **Cinematic vs runtime parity.** Movie Render Graph output ≠ gameplay GI/perf; gate pre-renders separately; never use cinematic settings as evidence the game runs.

---

## 7. TECHNICAL ARCHITECTURE — THIRD-PERSON ACTION-ADVENTURE RPG

**Modules / plugins (proposed, subject to approval — not to be committed now):**

- **`TDDGame`** (runtime C++ core): game mode, player controller, `TDDCharacter` base, camera system (spring arm + combat offsets), save/load subsystem, settings, accessibility.
- **Gameplay Ability System** for combat: attributes (Health/Stamina/Chi-analogue), effects, costs, cooldowns, tags (`Ability.Combat.Melee.Light` …), ability sets per weapon, dodge/parry/counter as abilities, boss ability sets. Blueprint-authored abilities over C++ base classes; C++ for systems, Blueprint for content.
- **Enhanced Input** (input mapping contexts: exploration/combat/cinematic/menu).
- **Enhanced AI:** StateTree (behaviour) + EQS (targeting/cover/spacing) + Env Query for bosses; MassEntity only for village/market crowds if needed (otherwise HISM + simple anim BP).
- **Modular GameFeature plugins:** `TDD_Combat`, `TDD_Quests`, `TDD_MemorySystem` (the seven-memory spine; data-driven: memory IDs `MEM_01…07`, reveal state, chapter gating), `TDD_Dialogue`, `TDD_SaveGame`, `TDD_AncestralRealm` (data-layer state variants), `TDD_Cinematics`. Keeps systems isolated, testable, and prevents a monolithic game module.
- **Data-driven content:** Primary Data Assets + Gameplay Tags + (optionally) GAS-integrated dialogue tables; all narrative text localisation-ready from day one (English + Igbo-flavoured terms require a glossary — **decision required**).
- **Animation architecture:** one `ABP_TDDCharacter` + linked Anim Layers per weapon family; Motion Warping for root-motion abilities; IK Retargeter from mocap sources; Control Rig for procedural feet/hands.
- **World structure:** one World Partition persistent level (or 2–3: Home Settlement / Chapter realms folded in), HLOD layers per biome, Data Layers for realm-state.
- **Save system:** versioned serialization (slots + metadata), checkpoint + chapter-boundary autosaves, no reliance on GameInstance-only state.
- **Cinematics:** Sequencer + Movie Render Graph pre-renders for trailers; in-game Sequencer for memory scenes; camera work per art-bible cinematography folder (empty — to be designed).
- **Testing & CI:** Unreal Automation tests for systems (save/load, memory-gating, combat attributes), BuildGraph nightly cook + package + smoke test, crash reporting.
- **Repo hygiene:** adopt Perforce or Git LFS; keep Drive as art-direction bible (read-only reference), not as source control.

**Why not a single monolithic game module:** an 8-chapter narrative RPG with memory-gating logic collapses under tight coupling; GameFeatures + GAS + data assets are the cheapest insurance against the inevitable re-scope of Chapters 4–8.

---

## 8. MAJOR PRODUCTION RISKS AND PRACTICAL MITIGATIONS

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | **Scope exceeds team capacity** (open world + 8 chapters + RPG systems + cinematics) | Critical | Lock Chapter 1–2 as shippable slice first; vertical-slice gate before chapter expansion; strict content budgets per chapter; cut content, never quality |
| R2 | **No performance validation possible here**; hardware unknown | Critical | Owner must inventory/benchmark dev machines (§3.1) and approve min-spec (§3.2) **before** Milestone 1 sign-off |
| R3 | **UE5 learning curve / C++ scarcity** on the team | High | Lyra sample study; hire/contract one UE gameplay engineer; Blueprint-heavy content pipeline over C++ systems |
| R4 | **Shader-compile & traversal hitching on first play** | High | PSO precaching (5.8 improved), cooked builds in CI, async streaming tests on min-spec SSD-vs-HDD |
| R5 | **VRAM/memory blowouts** (4K textures, high tri counts) | High | Virtual Texturing, 2K default + 4K hero only, texture streaming pools, per-scene memory reports, 16 GB min-spec hard gate |
| R6 | **Nanite/Lumen misapplied** (translucency, foliage, skinned meshes, light count) | Medium | Enforce §5 stack table; profile per scene; Lumen Lite path ready for consoles/Switch 2 |
| R7 | **African-architecture asset scarcity** (Fab/Megascans bias toward Western/EU/US kits) | High | Budget for bespoke kit (compounds, shrines, Igbo-inspired architecture); photogrammetry trips or commission; do not accept generic "tribal" marketplace kits — authenticity + art-bible violation |
| R8 | **Cultural sensitivity / IP** (Igbo-inflected religious material, Amadioha/Idemili names) | High | Cultural consultants (Enugu/Anambra-based) in review loop; legal review for deity usage vs. fictionalisation; DECISIONS.md already shows this bar — extend it |
| R9 | **Drive→engine workflow drift** (Drive not versioned for production) | Medium | Perforce/Git LFS canonical store; Drive stays bible/reference; one-way export with naming registers |
| R10 | **Art boards ≠ game-ready** (scale, textel density, LOD, collisions) | Medium | Asset Production Guidelines doc before first asset; DDC + review gates; Adanna master reference as the fidelity contract |
| R11 | **Git without LFS** (repo today) | Medium | Adopt LFS/Perforce immediately when binary work starts; never commit raw `.uasset`/source art to Git |
| R12 | **5% royalty above $1M** (EGS exempt) | Low–Medium | Model in financials; EGS strategy optional; unaffected below $1M |
| R13 | **Console certification** (PS5/Xbox X|S) | High | Devkit procurement + first-party registration early; concept-approval for memory/violence content; TRC checklists in CI checklist |
| R14 | **Single-machine/bus-factor for builds** (this sandbox, Drive, one repo) | Medium | CI + artifact retention; DDC on shared storage; off-site Drive backup of bible |
| R15 | **Switch 2 temptation** | Medium | Defer or cut explicitly; it is a different optimisation universe; do not let it creep into PC/PS5 budgets |
| R16 | **Nanite-for-everything illusions / "free quality"** | Medium | Performance budget gate at every milestone; min-spec blue-badge builds required to pass CI |
| R17 | **Cinematic ambition vs gameplay budget** (Memory scenes) | Medium | Prototype Memory 6 (childhood death) as the first cinematic spike in Milestone 2; cap Movie Render Graph use to marketing/pre-render |
| R18 | **Engine obsolescence anxiety** (5.9 preview, UE6 late 2027) | Low | Pin 5.8.x; evaluate upgrades only at chapter boundaries; content on 5.8 remains valid |

---

## 9. MIGRATION RISKS (IF APPLICABLE)

There is **no code, no engine project and no 3D asset migration** — the lowest possible migration risk profile. The residual risks:

1. **Process migration, not asset migration:** Drive-based collaboration → VCS + DCC + engine. Expect 2–4 weeks of pipeline friction; mitigate with registers (already in Drive) ported into repo as YAML/CSV manifests.
2. **Interpretation drift:** art boards (e.g. Chapter 8 KEEP/REVISE/REDO list, Adanna's weapon identity, six-year-old framing) must be enforced in-engine by reference sheets pinned in the project (ContentExamples-style map). Assign this to the art lead at project bootstrap.
3. **Naming/ID continuity:** reuse Drive register IDs in Unreal asset names to preserve traceability (`CHR_ADANNA_*`, `LOC_CH01_*` …).
4. **Git LFS retrofit risk:** if binary art lands in Git before LFS, repo bloat is unrecoverable without history surgery — install LFS hooks first.
5. **No backup/migration of "lost" work possible — because there is none — but do not let "start fresh" become "re-litigate everything": DECISIONS.md is approved direction; do not reopen locked narrative decisions in engineering reviews.
6. **Version pinning:** assets authored on 5.8 must not be casually re-saved on 5.9/6.x without migration review (asset version upgrade irreversibility).

---

## 10. RECOMMENDED GRAPHICS & PRODUCTION STACK — SUMMARY CARD

> UE 5.8.x · Windows dev (Linux source builds optional) · **Nanite + Lumen(HWRT)+Lumen Lite + VSM + MegaLights + World Partition/HLOD/Data Layers + PCG + MetaHuman + Sequencer/Movie Render Graph + GAS + Enhanced Input + StateTree + CommonUI + MetaSounds · TSR + dynamic resolution · 60 fps Performance / 30 fps Quality · Perforce or Git-LFS · CI with cooked smoke tests**

---

## 11. RECOMMENDED FIRST PRODUCTION IMPLEMENTATION MILESTONE

**Milestone 1 — "Foundation Vertical Slice" (recommend 6–10 weeks, team-dependent; scope-fixed, not date-fixed)**

**Goal:** prove the *complete game* is buildable on UE 5.8 at the art-bible quality bar — the cheapest honest proof, not a demo.

**In scope**
1. Project bootstrap (separate from any engine work on other agents' branches; pinned 5.8.x; `.gitattributes`+LFS or Perforce; naming registers from Drive ported).
2. `TDDGame` module + GameFeature skeleton (`TDD_Combat`, `TDD_MemorySystem` stubs), GAS attributes + one melee ability + dodge, Enhanced Input.
3. One **real-scale greybox of Home Settlement** (one compound + environment kit candidates) in a World Partition cell; Nanite/Lumen/VSM on; HLOD off for slice but streaming path proven (cell loaded async).
4. MetaHuman of **Adanna** locomotion + idle; one NPC (market trader) with EQS/StateTree idle-wander.
5. Basic save/load (slot, chapter checkpoint); one **complete memory beat** (Memory 6 framing) as a sequencer scene at 70% fidelity.
6. **Performance gate:** 60 fps @1080p High on the agreed min-spec PC + one console-class profile; packaged Development build passes smoke test in CI; shader precache verified.
7. Asset pipeline validated end-to-end for **one hero environment asset** (e.g. Nneka's House wall segment) and **one weapon** from the weapon register.

**Out of scope (explicitly):** full combat depth, all 9 chapters, multiplayer of any kind, console certification submission, Switch 2, photogrammetry scanning trips, final audio.

**Exit criteria:** packaged build + 5-minute playthrough + perf report + asset pipeline doc + risk register updated. **Only then** does full Chapter 1 production begin.

**Not a graphics demo:** the slice must contain gameplay, a save loop and a narrative beat; beauty-shot-only validation is rejected by definition.

---

## 12. DECISIONS THAT GENUINELY REQUIRE APPROVAL

| # | Decision | Needed by | Owner input required |
|---|---|---|---|
| D1 | **Pin engine to UE 5.8.x** (vs. waiting for 5.9/UE6) | Milestone 1 start | Approve / reject |
| D2 | **Target platforms:** PC-only at launch vs. +PS5/Series X vs. +Switch 2 | Immediately (drives budgets) | Platform list + cert budget |
| D3 | **Minimum PC spec** (§3.2) — this defines every scalability budget | Milestone 1 start | Approve tier |
| D4 | **Performance mode:** 60 fps Performance default on consoles/min-spec? | Milestone 1 | Approve |
| D5 | **Dev hardware acquisition/benchmark** — actual dev workstations undocumented; this sandbox is unusable for UE5 | Before Milestone 1 | Current specs + upgrade plan |
| D6 | **Source control: Perforce vs. Git+LFS** (repo is Git, no LFS today) | Before any binary commit | Choose + license |
| D7 | **Team/hiring:** who implements Milestone 1 (in-house, contractor, co-dev?); UE C++ competence | Milestone 1 | Staffing plan |
| D8 | **Budget for bespoke African-architecture kit + cultural consultancy** (R7/R8) | Milestone 1–2 | Approve line items |
| D9 | **Chapter 1–2 first** (vs. Chapter 8 Ancestral Realm showcase) — recommendation: Chapters 1–2 | Milestone 1 planning | Approve |
| D10 | **Localisation scope** (Igbo terms glossary; languages at launch) | Pre-production | Approve |
| D11 | **MetaHuman usage + likeness/IP review** (character design → MetaHuman conform) | Milestone 1 | Approve |
| D12 | **Royalty/financial model acknowledgement** (5% above $1M; EGS choice) | Commercial planning | Acknowledge |
| D13 | **Drive→VCS migration authority** (who may move/archive Drive production folders — NOT this agent) | Pipeline setup | Assign authority |
| D14 | **Milestone 1 scope freeze** (§11) | Milestone 1 | Approve exit criteria |

---

## 13. WHAT THIS ASSESSMENT DOES NOT AUTHORISE / ISOLATION STATEMENT

- No project was created, no engine was installed or run, no migration was performed, no systems were replaced, no production branch was touched, no agent was contacted, instructed or scheduled. **Existing production continues uninterrupted; this report creates no dependency for it.**
- All findings are advisory to the project owner and their principal assistant. Until the owner approves items in §12, none of them is a project decision.
- No performance claim herein has been measured on real TDD hardware; §3 documents that such measurement is currently impossible and mandatory before Milestone 1 sign-off.

---

## 14. APPENDIX — SOURCE EVIDENCE

**Repository:** `git ls-tree -r HEAD` → `README.md` (6 B); `git log` → 1 commit `5e3d1da`; no `.gitattributes`; `lscpu`/`free`/`df`/`nvidia-smi` outputs as tabulated in §3.

**Drive (read-only):** `THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE` (parent `1lzJBgHHSO2OJMB0LFmwQoU6R7Kv2iGlZ`): 24 top-level items; `01_CHARACTERS` = 9 groups; `02_LOCATIONS` = 9 chapter folders + Home Settlement; `14_APPROVED_DESIGNS` = 8 files (2026-11-16); `DECISIONS.md` (10,451 B, 2026-11-15); `ENVIRONMENTAL_DENSITY_ASSESSMENT.md`; `09_ANIMATION_AND_COMBAT`, `12_CINEMATOGRAPHY`, `13_GAMEPLAY_AND_LEVEL_DESIGN` = **0 files**; `17_DOCUMENTATION` = indices/registers/reports only; `PENDING` and `CD_REVIEW_2026-11-16` present (not inspected — outside assessment scope and owned by other workflows).

**Official documentation (fetched 2026-11-18):**
- Nanite — https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- Lumen — https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- World Partition — https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine

**Release & market evidence (web, 2026-11-18):**
- [UE 5.8 release notes — forums.unrealengine.com](https://forums.unrealengine.com/t/unreal-engine-5-8-released/2729274) · [UE 5.8 analysis — cgchannel.com](https://cgchannel.com/2026/06/see-5-key-features-for-cg-artists-in-unreal-engine-5-8/) · [MegaLights/Lumen Lite 60 fps — overclock3d.net](https://overclock3d.net/news/software/unreal-engine-5-8-delivers-megalights-and-lumen-lite-with-60-fps-performance-targets/)
- [UE 5.7 release — unrealengine.com](https://www.unrealengine.com/news/unreal-engine-5-7-is-now-available) · [UE 5.9 preview — maverickframe.com](https://maverickframe.com/blog/unreal-engine-latest-version/) · [UE5 feature overview — en.wikipedia.org](https://en.wikipedia.org/wiki/Unreal_Engine_5)
- [Unity render-pipeline strategy 2026 — gamefromscratch.com](https://gamefromscratch.com/the-unity-hdrp-is-dead/) · [Unity HDRP vs UE5 2026 — nastyrodent.com](https://nastyrodent.com/unity-hdrp-vs-unreal-engine-5/) · [Unity BiRP deprecation — aplusgamesstudio.com](https://aplusgamesstudio.com/blog/unity-6-upgrade-guide-built-in-render-pipeline)
- [UE licensing & royalties 2026 — 300mind.studio](https://300mind.studio/blog/unreal-engine-licensing-royalties/) · [UE royalty FAQ 2026 — practicetestgeeks.com](https://practicetestgeeks.com/unreal/is-unreal-engine-free) · [Pricing/EULA analysis — itechguides.com](https://www.itechguides.com/what-happens-if-a-game-engine-changes-its-pricing-or-terms-developer-faq/)
- [UE5 recommended hardware 2026 — greypc.net](https://greypc.net/best-pc-build-for-unreal-engine-5-2026-the-definitive-hardware-guide/) · [Nanite workstation guidance — medium.com](https://medium.com/@mumbamweni3/building-a-pc-for-unreal-engine-5-nanite-the-smoothest-dev-workstation-setup-e0f992858d71)

---

*End of assessment. Submission to the project owner; no action beyond this document is authorised by this assessment.*
