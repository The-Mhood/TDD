# THE DISOBEDIENT DAUGHTER — AGENT 4 ASSESSMENT
# Unreal Engine 5 on Mac · PlayStation 5 Compatibility · Real-Resource Production Path

**Status:** Independent assessment. Advisory only — no decision is made on the owner's behalf. Production continues independently; nothing here is a prerequisite for other work.
**Date:** 2026-11-18
**Prepared by:** Independent technical assessment agent (Agent 4), reporting directly to the project owner.
**Repository:** `The-Mhood/TDD` @ branch `arena/b2c58152-tdd` (no implementation, migration or new project was created or modified).
**Prior work:** A separate repository-level UE5 assessment exists at `docs/TECHNICAL_ASSESSMENT_UE5_GRAPHICS.md`; this report does not duplicate it and does not depend on it.

---

## 0. THE CENTRAL QUESTION — SHORT ANSWER

**Yes, with hard boundaries:** you can realistically start and carry real production on your Mac — UE 5.8 on macOS is officially supported for development, and Blueprints, gameplay logic, MetaHuman assembly, animation, World Partition editing, GAS, Enhanced Input, Sequencer, UI and save systems are all editor-side tools that do not depend on Windows. **No, with equal clarity:** your Mac cannot be the machine that *validates the final visual quality target* and *cannot produce or test PS5 builds at any stage*. The PS5 is not reachable by any route that avoids (a) Sony's approval process, (b) loaned/authorised Sony hardware, and (c) a Windows (or Linux) build host running Sony's SDK. A retail PS5 cannot run your builds, ever, by legitimate means.

The smart path therefore has three phases:

1. **Phase 0 — Mac-only (now, ~$0):** UE 5.8 + macOS/Xcode per Epic's official matrix; greybox + gameplay foundation + software-lit look-dev; everything renderer-agnostic.
2. **Phase 1 — Minimal reference hardware (when an affordable used Windows/Linux PC ~US$600–1,200, or equivalent, becomes available):** final rendering reference (Nanite/Lumen HWRT as applicable), and the PS5 toolchain host. This is the single most important non-Mac purchase and is *conditionally necessary*, not a convenience — but defer it until Phase 0 proves the vertical slice or funding opens.
3. **Phase 2 — Sony approval (once the slice is playable + GDD exists):** apply at partners.playstation.net; sign GDPA; receive dev kit + test kit; enable the UE5 PS5 platform integration from Epic (only issued to Sony-verified licensees); cook/deploy/profile/certify. PS5 supports Nanite and Lumen natively — it is where final quality must be signed off.

Everything in this plan avoids building something that must be rebuilt later, and spends money only where it is genuinely required.

---

## 1. SECTION 1 — MAC DEVELOPMENT FEASIBILITY

### 1.1 What I could not do: inspect your actual Mac

I have **no access to your Mac** — this assessment was produced in an isolated Linux workspace. I will not invent its specifications. The only data point available is the owner's statement that it was "previously identified as having 16 GB RAM".

**Exactly what is missing:** model identifier, chip (Intel vs M1/M2/M3/M4 …), core counts (CPU/GPU), unified memory, storage size/free space, macOS version, Xcode version, display count/resolution.

**Simplest way to obtain them (takes ~2 minutes):**

```bash
system_profiler SPHardwareDataType SPDisplaysDataType SPMemoryDataType > ~/tdd_mac_specs.txt
sw_vers
sysctl -n hw.memsize hw.model machdep.cpu.brand_string 2>/dev/null   # Intel only for brand_string; harmless if empty
df -h /
```

Or: Apple menu → **About This Mac** → **More Info…**, and paste/screenshot the summary. Once pasted, the gap analysis in §1.4 can be converted to exact numbers.

### 1.2 Official UE5-on-macOS position (Epic documentation, fetched 2026-11-18)

Epic publishes a dedicated **macOS Development Requirements** page ([dev.epicgames.com → macOS Development Requirements](https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?lang=en-US)). For **UE 5.8** specifically:

| Item | Minimum | Recommended |
|---|---|---|
| macOS | **Sonoma 14.5** | Latest macOS 15 Sequoia |
| Processor | **M1 or M2** "depending on rendering features" | **Apple Silicon M3** |
| Memory | **16 GB** | **32 GB or more** |
| GPU | Metal 1.2-compatible | — |
| Xcode | 26.0 (**Xcode 26.4 is incompatible with Unreal Engine**) | **26.1.1** |
| Distribution | Universal binaries (Intel + Apple Silicon) since UE 5.2 via Epic Launcher | — |

The general [Hardware and Software Specifications](https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine) page keeps its recommended baseline at Windows 11, 32 GB RAM, DX12 GPU with ≥8 GB VRAM — i.e. **Epic treats Windows as the reference platform; macOS is a supported development host with a reduced feature set, not a rendering reference.**

### 1.3 Feature-by-feature reality on macOS (Metal RHI)

| System | On Mac (UE 5.8, Metal) | Practical consequence |
|---|---|---|
| Editor, C++/Blueprint compilation | ✅ Supported, universal binaries; Apple Silicon native since 5.2; Clang toolchain (Rider/VS Code/Xcode, not Visual Studio) | Fully viable for gameplay, systems, AI, UI, save logic |
| Blueprints, GAS, Enhanced Input, StateTree, Mass | ✅ Platform-agnostic | Develop freely |
| World Partition (authoring, cells, data layers, OFPA) | ✅ Authoring works | Editing large cells on 16 GB is heavy but greybox-scale is fine |
| MetaHuman (assembly/animation in-editor) | ✅ Works; MetaHuman Creator is cloud-based (browser), so even an 8 GB machine can author; runtime perf limited | Assemble now; heavy crowd scenes are a PS5/PC problem |
| Sequencer + Movie Render Graph (offline export) | ✅ Works | Cinematic **look** tests will differ from DX12/HWRT output — treat Mac MRG as blocking/iteration, not final grade |
| Control Rig / IK Retarget / Motion Warping / Anim | ✅ | Fine |
| PCG (scatter/foliage) | ✅ Authoring works | Tune densities later on reference hardware |
| Niagara | ⚠️ Core GPU emitters work; some simulation modes are slow or limited on Metal; fluids disproportionately expensive | Prototype effects; final FX pass on reference hardware |
| **Nanite / Virtual Shadow Maps** | ❌ **Not an available production path on Metal.** Epic lists Nanite/VSM requirements as DX12 (Shader Model 6.6 atomics) or Vulkan; Metal is not listed. Community reports of partial/experimental Nanite on M2+ exist, but it is unsupported — do not plan around it | **Final Nanite assets must be authored and validated on Windows/DX12 (or PS5).** Author clean, well-UV'd, sensible meshes that would work either way |
| **Lumen — Hardware RT** | ❌ Requires Windows + DX12 + SM6 + RTX 2000/RX 6000/Arc ([Epic rendering-requirements table](https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine)) | No HWRT on Mac |
| **Lumen — Software RT** | ⚠️ Runs on Metal with reduced quality/stability and heavy cost at 1080p on unified memory; historically broken GI corners on some M1/M2 builds; treat as reference-ish, not final | Use for blocking light mood; sign-off elsewhere |
| MegaLights | ❌ Tied to the DX12/SM6 path | PS5/Windows only |
| Virtual Texturing, Substrate materials | ⚠️ Substrate exists but Metal-specific issues/cost apply; virtual texturing works with caveats | Use sparingly on Mac; final pass elsewhere |
| Shader compilation | ⚠️ First launch / first cook / first MRG render compiles everything via Metal toolchain; unified memory + limited threads = long stalls, occasionally 30–60+ min on first full cook for a mid-size project | Use shared DerivedDataCache on a fast external SSD; budget compile time into schedule; never judge perf on first run |
| Packaging/testing | ✅ `Package Project` → macOS works | Useful for iteration and for any future Mac/holiday marketing build; irrelevant to PS5 |

**Bottom line on ambition:** developing *toward* the intended quality on Mac is realistic **only** if (a) you architect content renderer-agnostically (good UVs, real LODs, disciplined materials — good practice anyway), (b) you treat Mac lighting/render output as *approximate*, and (c) all quality sign-offs happen on reference hardware. You do **not** need to water down the final game's visual ambition — but you must not confuse "runs on my Mac" with "meets the art bible".

### 1.4 16 GB reality check (assuming the stated 16 GB is exact)

- Epic's **minimum** is 16 GB — you will run the editor, not run it comfortably. Expect: macOS swap pressure, Jetsam kills of background apps, multi-minute stalls with MetaHuman + dense levels open, and painful `cook`/`shader compile` sessions.
- Apple Silicon RAM is **soldered** — upgrading later means a new machine. If your Mac is an entry Air/Pro with 16 GB, an honest plan is: Mac carries Phase 0 only, and a modest Windows/Linux box carries everything else (§5, §7).
- Mitigations that actually help: close everything else; disable unused plugins; greybox over detailed art; Software Lumen off or Minimal on maps; uncapped editor textures off; external NVMe SSD for project + DDC; 4K displays off or scaled.
- Project sizes: UE5 projects with art typically reach **30–80 GB** (project) plus **30–80 GB** DerivedDataCache/Intermediate; a near-empty project is ~15–20 GB installed. An external 1–2 TB NVMe (~US$80–180) is the cheapest hardware purchase that buys back enormous time — recommended now (§5).

### 1.5 What is genuinely missing from this assessment

Model, chip, exact memory, storage, macOS version and Xcode version (commands in §1.1), plus your tolerance for a second machine and a rough monthly budget. These change the numbers, not the strategy.

---

## 2. SECTION 2 — PLAYSTATION 5 DEVELOPMENT AND TESTING

### 2.1 The hard boundary statements

1. **A retail PS5 cannot run your development builds — full stop.** It executes only Sony-signed packages. There is no legitimate sideload path for a commercial title in development. Jailbreaks/homebrew exist but are (a) illegal for commercial distribution, (b) unsupported, (c) unusable for certification, and (d) irrelevant to shipping — they are not an option for this project.
2. **You need Sony approval before you can even *install* anything on test hardware.** Access flows through **PlayStation Partners** (partners.playstation.net): registration → review → **Global Developer & Publisher Agreement (GDPA)** under NDA → **DevNet** access → PS5 SDK (internal codename **Prospero**, LLVM/Clang toolchain on a FreeBSD-derived OS) → hardware.
3. **Hardware is mandatory for shipping:** a **development kit (DFI-D1000 class)** with expanded memory/debug/profiling, plus a **test kit** mirroring retail. Sony loan terms are confidential and vary by agreement; current public guidance (2026) indicates kits are commonly loaned to approved projects at no purchase cost (returnable), while other public accounts describe material cost, bonding, or leasing arrangements — **terms are Sony's decision, are not public, and are not to be budgeted from internet hearsay.**
4. **UE5 has full PS5 support** — for Sony-verified licensees only. The PS5 platform integration ships through a private distribution gated by Sony's verification (via Epic + Sony). It does not appear by default in the launcher. Epic's own staff state you cannot export PS5 builds without registration + hardware; the console platform code is not distributable otherwise.
5. **UE supports Nanite and Lumen on PS5.** PS5 is a next-gen SM6-class console and is squarely within the DX12-class requirements — final-quality lighting and geometry are first-class on it (unlike Mac). This is why PS5 (or a Windows DX12 box) must be the quality bar.

### 2.2 Access requirements, honestly itemised

| Requirement | Detail |
|---|---|
| Legal entity | Sony requires a registered business (in EU, sole trader acceptable per public reports). Project owner must operate as or via a company/registered entity |
| Application | partners.playstation.net — studio details, company info, **GDD**, intended content (age rating implications, memory/violence content), portfolio |
| Review outcome | Approval is discretionary. Public accounts range from half-hour approvals to outright rejection for portfolio-less first-time applicants. **A playable slice + GDD materially improves odds** — sequencing matters (§7) |
| GDPA + NDA | Signed before SDK/docs/hardware are issued; protects Sony IP; dictates handling of all Prospero materials |
| SDK + toolchain | LLVM/Clang-based; delivered under NDA via DevNet to approved members |
| Hardware | Dev kit + test kit under loan/lease terms set by Sony (see §2.1-3) |
| Epic verification | Console platform modules for UE distributed only after Epic confirms Sony verification |
| Certification (TRC) | Build must pass Sony's Technical Requirements Checklist; cert reports + age ratings (ESRB/PEGI/IARC as applicable); typical iteration of fix → re-cert |
| Commercials | ~30% PlayStation Store revenue share; publishing terms negotiable; physical releases need a publisher |

### 2.3 Can you test on retail PS5 during early development?

**No.** You cannot. Retail = signed code only. Early development testing happens on Mac (iteration/logic) and on a Windows/DX12 PC (rendering reference). PS5-specific behaviour — GPU timings, DualSense, memory pressure, suspend/resume, TRC behaviours — can only be verified on Sony hardware. Do not plan any PS5-specific task until devkit/test kit possession is real.

### 2.4 How Mac connects to PS5 testing

**It doesn't, directly — and pretending otherwise wastes money and schedule:**

```
[Your Mac]  ──git push──►  [Repo]  ──pull──►  [Windows/Linux build host + Sony SDK]
                                                         │ cook (UnrealBuildTool, PS5 target)
                                                         ▼
                                              [PS5 Dev Kit over network]
                                                         │ debug/profile (Razor CPU/GPU, PIX-like Sony tools)
                                                         ▼
                                              [Test Kit → certification]
```

- **The PS5 build host must be Windows or Linux.** Sony's public tooling and all credible practitioner evidence place the Prospero toolchain on Windows/Linux; **macOS is not a supported PS5 packaging host**, and Epic's platform support follows the SDK's host requirements.
- Deployment to the devkit is network-based (deploy & run from the build machine to the kit); debugging/profiling use Sony's tools on the host connected to the kit.
- A practical low-cost option: reuse one machine as both PC-rendering-reference box and PS5 build host — a Windows PC with an RTX-class GPU does both jobs.
- Perforce/Git on the build host; CI can produce nightly dev-kit packages once access exists (Windows runner, self-hosted on the same PC).

### 2.5 Costs, access & restrictions — realistic picture

| Item | Cost position |
|---|---|
| UE5 engine | Free; 5% royalty above US$1M lifetime gross per title (0% on Epic Games Store sales) |
| PlayStation Partner registration / GDPA / SDK | Free to apply; terms confidential post-approval |
| Dev kit + test kit | Commonly loaned free for approved projects (2026 public guidance); some report costs — **unknown until you are inside GDPA; do not budget a number from this document** |
| Windows build/reference PC (used RTX 3060 12 GB–class + 32–64 GB RAM) | ~US$600–1,200 used / US$1,200–1,800 new — Phase 1 purchase, deferred (§5) |
| Certifications/ratings | Ratings fees vary by body (ESRB/PEGI are self-rated under IARC for many stores; console cert itself has no public fee, but failing TRC costs schedule) |
| PlayStation Store | ~30% revenue share; publisher arrangement optional |
| Linux build host alternative | ~US$300–800 used; viable if Windows licensing is an obstacle; adds friction for tools/Visual Studio |

**Restrictions to internalise now:** no retail PS5 testing; no public sharing of SDK materials; no screenshots of kits/SDK; builds signed and sealed-catalogued; TRC compliance mandatory; content ratings required; and PS5 release is only possible as Sony-approved signed master — never from your Mac.

---

## 3. SECTION 3 — UE5 COMPATIBILITY ASSESSMENT (FOR THIS GAME)

### 3.1 Engine version pinning

Pin **UE 5.8.x** (latest patch; as of 2026-11-18 that is the 5.8 line; e.g. 5.8.4). Rationale: it is the latest full release and the last planned UE5 major; UE 5.9 is Preview-only; UE6 Early Access targeted late 2027. Upgrades only at chapter/milestone boundaries. On macOS, follow the 5.8 matrix exactly: **macOS Sonoma 14.5+ (Sequoia 15 recommended), Xcode 26.0–26.1.1 (26.4 incompatible), Apple Silicon, 16 GB minimum / 32 GB recommended.**

### 3.2 System-by-system compatibility matrix for TDD

| System | Mac (dev/iteration) | Windows DX12 (reference) | PS5 (final target) | Verdict |
|---|---|---|---|---|
| Nanite | ❌ Unsupported path | ✅ SM6.6 atomics | ✅ | Author everywhere; validate on DX12/PS5 |
| Lumen HWRT | ❌ | ✅ | ✅ (scalable) | Reference-only path |
| Lumen Software | ⚠️ Heavy/limited | ✅ | ✅ | Mac blocking only |
| Lumen Lite (5.8) | ⚠️ With caveats | ✅ | ✅ (60 fps path) | Preferred console GI path |
| Virtual Shadow Maps | ❌ (requires Nanite path) | ✅ | ✅ | Mac: force traditional shadowing |
| Niagara | ⚠️ Core OK; sims slow/limited | ✅ | ✅ | Prototype on Mac, grade on ref |
| World Partition | ✅ authoring | ✅ | ✅ | Design cells at slice scale on Mac |
| PCG | ✅ | ✅ | ✅ | Author on Mac; tune density on ref |
| MetaHuman | ✅ (cloud creator + in-editor) | ✅ | ✅ | Start now — your flagship asset |
| Control Rig | ✅ | ✅ | ✅ | Mac-fine |
| Sequencer / MRG | ✅ (iterative export) | ✅ (final grades) | ✅ (in-game cinematics) | Pre-render final marketing elsewhere |
| GAS | ✅ | ✅ | ✅ | Core combat framework |
| Enhanced Input | ✅ | ✅ | ✅ | Gamepad-first design |
| StateTree / EQS / Mass | ✅ | ✅ | ✅ | NPC logic + crowds |
| CommonUI | ✅ | ✅ | ✅ | Focus/navigation for pad |
| Substrate / Virtual Texture | ⚠️ caveats | ✅ | ✅ | Hero assets only |
| Single Layer Water | ✅ caveats | ✅ | ✅ | Rivers (Idemili chapter) |
| MetaSounds | ✅ | ✅ | ✅ | Audio direction |

### 3.3 Configurations to adopt from day one (renderer-agnostic hygiene)

Because Mac cannot render the flagship features, **all content you author must work on both Metal and the DX12/PS5 path**:

- Real meshes, real LOD chains for characters/hero props (do not rely on Nanite as a crutch; Nanite lights up on DX12 fine, but *authored* LODs protect min-spec and Mac iteration).
- Sensible UV density, no broken normals, no megasculpt without decimation plan — assets must survive Metal's path today and Lumen/Nanite later.
- Material discipline: keep instruction counts moderate, use Material Attributes, avoid platform-specific hacks; test with Complexity view on Mac.
- All lighting features behind scalability cvars — never hard-bake Lumen-dependent assumptions into level logic.
- World Partition cells sized small enough for 16 GB Mac editing (start with 128–256 m cells, one chapter slice); larger/HLOD layers tuned later.
- Data Layers for realm-state variants (e.g., Sealed Quarter sealed/open) — engine-agnostic logic, identical on both paths.

### 3.4 Recommended baseline graphics configuration

**Mac (development):** Metal RHI (default), Lumen Software OFF or Minimal for iteration (or classic baked/SSR lookmode for mood), **no Nanite/VSM**, shadows: medium, texture pool: limited, screen percentage 70–80%, TSR at Performance, 55–60 fps target in editor at 1080p for greybox; accept 30 fps mediums for fuller scenes. **Quality sign-off builds:** never from Mac.

**Windows reference / PS5:** Nanite on eligible meshes; Lumen (HWRT on Windows; scalable Lumen on PS5, targeting Lumen Lite for 60 fps Performance mode; full Lumen for 30 fps Quality mode); VSM on; MegaLights for firelit interiors (5.8 production-ready); TSR + dynamic resolution; PS5-specific: 60 fps Performance default, 30 fps Quality optional; texture budget per PS5 unified memory (~5–6 GB texture pool discipline within 16 GB shared).

**Neither machine changes the art bible.** The bible defines the *look*; the configuration defines the *cost*; your job is hitting both by iterating on reference hardware later, not by compromising now.

---

## 4. SECTION 4 — CROSS-PLATFORM PRODUCTION STRATEGY

### 4.1 Environment layering (prevent rebuilds later)

1. **Source of truth:** Git repo (`The-Mhood/TDD`) + Git LFS (add `.gitattributes` **before** first binary) — or Perforce later; Drive remains read-only art bible, never production storage.
2. **Two runtime profiles in-project from day one:** `MacDev` (Metal, low/med, no Nanite/Lumen HWRT) and `RefPC` (DX12, Nanite/Lumen/VSM, High/Epic). PS5 profile derived from `RefPC` when SDK access exists. Configs committed, never ad-hoc.
3. **Feature flags via scalability**, not via forks of content: one asset set; platform cvars decide cost.
4. **No platform-specific gameplay logic.** Everything platform-shaped lives in config/Build.cs/Platform profiles. Gameplay identical everywhere → zero porting debt.
5. **CI from day one** (even a local script): clean cook + package for Mac profile; PC/PS5 cook added later on the build host. Catches rot daily.

### 4.2 Iteration loop on Mac

```
Concept (Drive bible) → DCC (Blender/ZBrush/Substance or free equivalents) → UE 5.8 on Mac
   → greybox in World Partition slice → Blueprint/GA gameplay → local test (30–60 fps)
   → git push → (later) build host cooks → PS5 devkit deploy/profile
```

- Author narrative data as **Primary Data Assets** + Gameplay Tags (seven-memory IDs `MEM_01..07`, gating, chapter state) — data-driven = engine-portable = safe on both paths.
- Keep lighting direction/intensity values documented per scene so the Windows/PS5 pass is reproduction, not re-creation.
- Record PS5-monocrome differences as known issues with TSR settings noted.

### 4.3 Technologies that create Mac↔PS5 compatibility problems (avoid or gate)

- **Nanite-dependent content habits** (no LODs, insane tri counts "because Nanite") — gate behind DX12; author LODs anyway.
- **Lumen HWRT-only lighting graphs** — keep a Software/Lite variant per hero scene.
- **Virtual Shadow Map page-pool tuning** — meaningless on Metal; only tune on ref/PS5.
- **MegaLights-only fire scenes** — provide baked/SS fallback notes for Mac mood checks (final is PS5 anyway).
- **Hair grooms everywhere** — keep to 3–4 heroes; PS5/GPU budget; test cost on ref.
- **Movie Render Graph final grades** — always on DX12/PS5-class GPU; Mac exports are for approval of edit/story only.
- **PCG graphs tuned for Nanite foliage** — fine on both, but density must survive PS5 unified memory; tune there later.
- **DirectX-skeuomorphic SDKs/plugins (Win64-only marketplace code)** — ban from `MacDev` profile; vet all Fab plugins for macOS + PS5 slices or replace.
- **Source control mismatch** (Drive-style manual copies) — permanent drift; rejected.

### 4.4 Sequencing to avoid waste

Mac proves **fun, flow and systems** (character controller, combat grammar, memory reveal, save loop) on greybox + software lighting → Windows/PS5 proves **fidelity and budget** → vertical slice gate → chapter production. Character models, homes, rivers get *final* passes only after the loop is proven — this is the anti-waste order of operations.

---

## 5. SECTION 5 — FINANCIAL & RESOURCE ASSESSMENT

### 5.1 What your Mac alone can accomplish (near-zero spend)

- Install UE 5.8 + Xcode 26.1.1 (or CLI tools minimum) + Epic Launcher — free.
- Lyra/Third Person samples, engine learning, Blueprint prototyping — free.
- Foundation vertical slice: controller, GAS melee+dodge, Enhanced Input, one World Partition cell (Home Settlement greybox), one MetaHuman, save/load, one Memory beat — on greybox with Software Lumen/low settings.
- Narrative data architecture (memory system, chapter gates) in Blueprint/C++.
- Pre-production: GDD refinement, cinematic blocking, UI flow, memory-board review exports.
- MetaHuman creation/assembly (cloud, browser-based) — free tier sufficient for a handful of heroes.
- Version control: GitHub + Git LFS (1 GB free; paid tiers ~US$4–5/mo if exceeded) or **Perforce Helix Core free tier (up to 5 users)** — free.
- Blender (models/rigs/UVs), Krita (2D), DaVinci Resolve (free, edit/MRG grades are separate), GNONE — free.

### 5.2 What you can use free (software)

UE5 engine · MetaHuman Creator · Blender · Krita · VS Code · Xcode/CLT · Epic Launcher · Git/LFS · Perforce (≤5 users) · Megascans/Fab free-licensed assets (respect licences; UE-exclusive use for many assets) · IARC rating via store questionnaires (where applicable) · GitHub Issues/Projects for tracking.

### 5.3 What costs money or approval

| Item | Type | Rough cost (2026) |
|---|---|---|
| External NVMe SSD 1–2 TB (project + DDC) | Low, immediate | US$80–180 |
| Perforce/Git LFS paid tier (if >1 GB) | Low, optional | ~US$4–23/mo |
| Rider (if preferred over VS Code) | Optional | ~US$14–15/mo |
| Substance 3D Painter/Designer | Optional (Blender/Substance alternatives + Quixel suffice) | ~US$20–50/mo each |
| Maya | Optional (skip) | ~US$235/mo — **do not buy now** |
| SpeedTree | Optional (skip) | Licence-based — **do not buy now** |
| **Windows DX12 reference + PS5 build PC (used/new)** | **Conditionally necessary (Phase 1)** | used ~US$600–1,200 / new ~US$1,200–1,800 |
| PS5 dev kit / test kit | Sony-controlled, confidential | Possibly US$0 under loan for approved titles (2026 public guidance) or material — **unknown until GDPA** |
| Certifications / ratings / store | Sony/3rd-party | Ratings fees vary; ~30% store revenue share |
| Publisher fee/advance (if any) | Commercial | Variable |
| Photogrammetry/bespoke African-architecture kit | Production | Variable commission — budget later |
| Cultural consultancy (Igbo-language/religious accuracy) | Production | Day-rate consultants — needed before Chapter lock |

### 5.4 What is genuinely necessary now

1. **External NVMe SSD** — cheapest, highest-impact purchase; do it before the project grows.
2. **Git LFS configuration** (zero cost) — protects every asset you will ever commit.
3. **Your time on the foundation slice** — worth more than any hardware right now.
4. **Nothing else.** Do not buy a workstation, do not buy plugins, do not subscribe to asset packs until the slice gate is passed.

### 5.5 What can wait for funding

Phase 1 Windows/Linux box (until slice proved or Sony kit host needed) · PS5 costs (post-approval) · Substance/Maya/SpeedTree (if ever) · large Fab packs · motion capture suits/sessions · VO casting · marketing MRG node rental · trademark/registration beyond basics.

### 5.6 What requires Sony specifically

Development access (GDPA/NDA), all PS5 SDK/toolchain and docs, dev kit + test kit, Epic's PS5 platform modules, certification, PlayStation Store distribution — **none substitutable, none available retail, none purchasable off the shelf.**

---

## 6. SECTION 6 — REALISTIC CAPABILITIES, HONESTLY STATED

| Question | Answer |
|---|---|
| Can I build the complete game on my Mac alone, shipping commercial quality? | **No.** Mac cannot render/validate the Nanite/Lumen target and cannot package PS5 builds. Mac can build the entire *game* (systems, story, gameplay, greybox-to-mid-fidelity content) |
| Can I validate final visual quality without buying anything? | **No.** You need (eventually) a Windows DX12 GPU box and/or the PS5 kit |
| Can a retail PS5 work for development? | **No** — signed builds only; Sony hardware + approval mandatory |
| Will 16 GB RAM cripple the project? | **Not cripple — constrain.** Expect constant memory pressure; greybox-first workflow mandatory; final passes need more (unified 32 GB+ Mac or, realistically, the Windows box) |
| Can the game eventually run at high quality on PS5? | **Yes** — PS5 supports Nanite/Lumen officially; performance via dynamic resolution + Lumen Lite (60 fps) and full Lumen (30 fps), TSR, disciplined budgets — proven by shipping UE5 PS5 titles |
| Risk of building the wrong thing on Mac? | **Low if** you follow §4 layering; **High if** you tune visuals for Metal's limitations and assume they transfer — they don't, and you don't have to find out the hard way |

---

## 7. SECTION 7 — FIRST IMPLEMENTATION MILESTONE (FOR YOUR ACTUAL HARDWARE)

**Milestone 1 — "Foundation Playable" (Mac-first; 6–10 weeks, scope-fixed)**

**Objective:** The starting point you asked for — a playable third-person character inside an actual game world, built so every system expands into the complete commercial game. Not a disposable demo; not a beauty reel.

**In scope (all executable on your Mac today):**
1. **Repo hygiene:** add `.gitattributes` (Git LFS for `*.uasset`, `*.umap`, textures, audio, video) in a dedicated technical-setup task; document Mac build steps in `README.md`. *(Note: repository modification for implementation is outside my remit — this is a recommendation for whoever executes Milestone 1.)*
2. **UE 5.8 project bootstrap** (pin 5.8.x; macOS Sequoia 15; Xcode 26.1.1 — verify compatibility; Metal RHI default; `MacDev` scalability profile committed).
3. **`TDDGame` module + GameFeature skeleton** (`TDD_Combat`, `TDD_MemorySystem`); C++ base classes + Blueprint content.
4. **Third-person character** (start with engine mannequin or free MetaHuman): locomotion (walk/sprint/jump), camera with combat-aware offsets, **GAS attributes + one melee combo + dodge with i-frames**, one enemy placeholder with StateTree idle→chase→attack.
5. **Enhanced Input** mapping contexts (Exploration/Combat/Menu).
6. **One World Partition cell** — Home Settlement greybox at true scale (1 compound + paths + tree line); data-layer plumbing proven with one realm-state variant (sealed/unsealed toggle).
7. **One complete beat:** Memory 6 framing — a 20–40 second sequencer scene triggered in-world (fade, memory UI, return) — narrative system end-to-end.
8. **Save/load:** slot + chapter-checkpoint autosave; reload restores position/memory state.
9. **Perf gate:** stable 30–60 fps (1080p, Low–Medium) **on the Mac** for the slice scene; documented as Mac profile only — explicitly not the quality bar.
10. **Asset pipeline proof:** one hero environment asset (e.g., Nneka's House wall segment) + one weapon from the weapon register, end-to-end DCC→UE→in-slice render.

**Explicitly out of scope:** PS5 anything; Nanite/Lumen final look; all 9 chapters; final audio; certification; Switch 2; 4K/marketing exports; Fab purchases; workstation purchase.

**Exit criteria (all required):** packaged macOS build runs the full loop (spawn → explore → combat → memory beat → save → quit → relaunch → resume) at the Mac perf target; CI/local script produces the build deterministically; short design doc records decisions + known Mac/PS5 deltas; risk register updated; **Phase 1 purchase re-evaluated with evidence** (frame captures, memory logs).

**Why this order:** every system here is load-bearing for the final game (controller, combat grammar, narrative spine, streaming skeleton, save loop, pipeline). Deleting Milestone 1 deletes zero future work; skipping it guarantees expensive relearning after PS5 access arrives.

---

## 8. SECTION 8 — DECISIONS REQUIRING YOUR APPROVAL

| # | Decision | Why it matters / options |
|---|---|---|
| A1 | **Phase acceptance:** adopt Mac-first → Phase 1 used DX12 box → Phase 2 Sony application sequencing (§0/§4) | This is the plan's backbone |
| A2 | **Your Mac's exact specs** — send the §1.1 output; qualify whether 16 GB/entry-Apple-Silicon assumptions hold | Changes Phase 0 limits and timing |
| A3 | **PS5 remains the console target** (vs. Xbox/PC-first) — confirmation | Drives SDK application timing and content ratings review |
| A4 | **Phase 1 hardware approval:** used Windows PC (~US$600–1.2k) vs. waiting for funding to do nothing — and when | The one purchase that unblocks rendering sign-off + PS5 host |
| A5 | **External NVMe SSD (US$80–180)** — approve now? | Cheapest velocity gain; protects DDC/project |
| A6 | **Git LFS vs. Perforce** (Git LFS simplest; Perforce free ≤5 users scales better for binaries) | Irreversible-ish; decide before first binary commit |
| A7 | **UE 5.8 pin + macOS/Xcode environment** (Sequoia 15, Xcode 26.1.1; avoid 26.4) | Compatibility correctness |
| A8 | **Sony application timing** — recommend applying **after** Milestone 1 gate, with GDD + playable slice; alternative: apply now with concept only (lower odds for first-time applicants) | Sequencing is a strategic choice |
| A9 | **Business entity for Sony** (sole trader vs company; VAT/tax position) | Required for GDPA |
| A10 | **PC launch vs. simultaneous PS5 launch** — recommend PC first, PS5 port phase-gated after cert readiness | Commercial risk management |
| A11 | **Localisation & cultural consultancy budget** line items (Igbo terminology, deity content review) before Chapter lock | Already flagged in prior assessment (R8) |
| A12 | **Milestone 1 scope freeze** — approve §7 in-scope list as binding | Prevents demo-creep; preserves the "expandable foundation" mandate |

---

## 9. OPERATING BOUNDARIES & ISOLATION STATEMENT

- I worked independently and report only to you; I contacted, instructed, blocked and waited for no other agent; ongoing production is unaffected and this report is **not** a prerequisite for it.
- No repository implementation was modified; no new Unreal project was created or migrated; no engine/hardware purchases were authorised or made.
- No Mac was inspected — its specs are unknown beyond your "16 GB" statement; §1.1 lists precisely what is missing and the 2-minute command to obtain it. **Nothing in §1 involving exact performance figures should be treated as measured fact about your machine.**
- PS5 facts are limited by Sony's NDA: registration flow, GDPA, SDK (Prospero), dev kit/test kit models and Epic's verified distribution are confirmed via public sources; exact loan terms, fees and eligibility criteria are **confidential and Sony-discretionary** — they are deliberately not invented here.
- This report recommends; you approve. Items in §8 are not decided.

---

## 10. APPENDIX — SOURCES (accessed 2026-11-18)

**Official Epic documentation:**
- macOS Development Requirements (UE 5.8 matrix: Sonoma 14.5+/Sequoia 15, Xcode 26.0–26.1.1, M3 recommended, 16 GB min/32 GB rec) — https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?lang=en-US
- Hardware and Software Specifications (Windows 11 baseline; Lumen = DX12+SM6+GPU list; Nanite = DX12 SM6.6 atomics/Vulkan) — https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine
- Nanite — https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- Lumen — https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- World Partition — https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
- iOS/iPadOS Quick Start (Xcode compatibility enforcement example) — https://dev.epicgames.com/documentation/unreal-engine/ios-ipados-tvos-quick-start-guide-for-unreal-engine

**PlayStation access (public sources):**
- [PlayStation Game Development: Complete PS5 SDK Guide 2026 — generalistprogrammer.com](https://generalistprogrammer.com/tutorials/playstation-game-development-ps5-sdk-guide) (Partners registration, GDPA, DevNet, Prospero SDK, dev kit DFI-D1000 loan, TRC, ~30% cut)
- [Is it possible to make games for PS5 without DevKit? — Epic Developer Community Forums](https://forums.unrealengine.com/t/is-it-possible-to-make-games-for-playstation-5-without-devkit-hardware/2035741) (SDK access requires registered developer; retail units unusable)
- [PS4/PS5 packaging requirements forum — unrealengine.com](https://dev.epicgames.com/community/forums/g/GAME_DEVELOPMENT/) / [Epic forums thread 1261616](https://forums.unrealengine.com/t/package-project-for-ps5/1261616) (retail cannot run dev builds; Epic verifies Sony verification before console modules)
- [How do you dev games for PS4/PS5 with UE5? — r/gamedev](https://www.reddit.com/r/gamedev/comments/wvxorn/how_do_you_dev_games_for_ps4_or_ps5_using_unreal/) (portfolio/registration discretion; approval variability)

**macOS + UE5 practitioner evidence:**
- [Unreal 5+ on Mac? — r/unrealengine](https://www.reddit.com/r/unrealengine/comments/17lvmrd/unreal_5_on_mac/) (Metal: Lumen software-only, Nanite unsupported/partial, Niagara caveats)
- [UE 5.1 on macOS Silicon — r/unrealengine](https://www.reddit.com/r/unrealengine/comments/z0c0j0/ue_51_on_macos_silicon_m1m2/) (Lumen-on-Metal fragility reports)
- [Mac Studio for Game Development — evezone.evetech.co.za](https://evezone.evetech.co.za/daily-drop/mac-studio-for-game-development-unity-and-unreal-engine-on-macos) (Nanite Metal 3 status; Lumen SW OK; HWRT not on macOS; shader compile slower)
- [Apple Silicon Macs natively support UE5 — engadget via HN](https://news.ycombinator.com/item?id=35918061) · [Unreal Engine 5.2 on MacOS — gamefromscratch.com](https://gamefromscratch.com/unreal-engine-5-2-on-macos/) (universal binaries, native Apple Silicon)

**UE pricing:** first US$1M lifetime gross per title royalty-free; 5% above; 0% on Epic Games Store — see prior assessment appendix for citations.

---

*End of report. Direct submission to the project owner. No implementation, purchase, migration or application is authorised by this document.*
