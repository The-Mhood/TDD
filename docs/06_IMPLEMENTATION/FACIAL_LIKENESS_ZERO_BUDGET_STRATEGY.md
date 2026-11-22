# Facial Likeness — Zero-Budget Production Strategy

**Document ID:** TDD-IMPL-FACIAL-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM + Design Lead, jointly. Coordinated by the Takeover Lead.
**Objective:** Maximum achievable facial likeness quality at **zero financial cost** — not minimum effort at zero cost. No paid outsourcing, no paid software/subscriptions/cloud, no AAA promises without evidence.
**Status:** PROPOSAL — **Owner approval required before implementation.** A proof-of-concept (PoC) must demonstrate the actual achievable quality before full production commits.

**Grounding (verified, not assumed):**
- **Hardware:** the only Unreal machine is the owner's **Apple M4, 16 GB RAM, macOS 27.2.1, UE 5.8.4, Xcode 27.2** (T00 §4). 16 GB is Epic's *minimum* → swap pressure. The **RTX 3060 Ti / 16 GB reference PC is a future paid purchase** (D-12, ~$600–1,200), **not yet acquired**, and is a perf-sign-off target, not a facial-production tool. No paid cloud GPU is assumed.
- **Existing free pipeline:** **Blender 4.2.23 LTS** (free/open-source) is already the character-authoring tool — Adanna V3 and Guard V2 were sculpted, retopologised, rigged and exported in Blender, verified headless (`W1D7_CHARACTER_INTEGRATION_MANIFEST.md`). Shared **`HUMAN_BASE_PROPOSED`** skeleton (11 joints), GLB/FBX export, UE import scripts, PBR material slots.
- **Identity anchor:** the approved **`REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg`** (Google Drive ID `1CMW978LfSYtR0SRAgnqKZkk0gNY_rpqF`) is the single approved likeness reference. The full-body turnaround is **not approved** (V004 front blocked; three-quarter not approved) — so facial likeness is built from the approved portrait + anatomy, **not** from unapproved turnarounds.
- **Cultural gates:** CD-2 (consultant gate for shrine/mask/ritual) is **OPEN**; CD-3 (enemy ratification) is **not ratified**. Nothing relying on real Igbo practice ships without sign-off (Q-17).

---

## 1. Production approach

**No external artists or studios.** The work is produced by a three-tier force: **AI agents** (this workflow), the **owner** (creative decisions + final review), and **free tooling** (Blender + UE). The split is deliberate: AI agents materially contribute to *pipeline automation, texture/ideation assistance, QC, and repetitive craft*; the owner retains *creative decisions and final visual sign-off*.

| Layer | Who | What they do | What they do NOT do |
|---|---|---|---|
| **AI agents** | Agent tracks (T1/T2/T3) + this session | Orchestrate the pipeline; generate/upscale/clean **textures** and **ideation boards**; run **automated QC** (topology, UV, weights, scale, naming); automate **retargeting**, **import**, **evidence** capture; draft documentation | Decide the identity, the expression, or the final look; sign off creative; invent cultural content |
| **Owner** | Project owner | Set the identity target; review each stage; approve/reject; coordinate cultural review (CD-2); final sign-off | Be replaced by AI for creative decisions |
| **Free tooling** | Blender 4.2.23 LTS, UE 5.8.4, Git/LFS, Python | Author the face (sculpt, retopo, UV, texture-paint, rig, export); import & verify in UE | — |

**Coordination across functions (single-owner surfaces, no parallel conflicts):**
- **Story** owns identity, narrative constraints and the cultural reference guide.
- **Design** owns visual briefs, reference boards and the qualification package.
- **Character Art** owns the Blender sculpt / texture / rig.
- **Technical Art** owns topology, LOD, materials, UV and export spec.
- **Engineering** owns UE import, skeleton binding, animation integration and acceptance tests.
- **TL (Takeover Lead)** reviews every merge batch for contract compliance (DA-02 cap ~25/week). Shared surfaces are single-owned; the skeleton, material-slot system and import scripts are reused, not re-authored, per character.

**Why this works at zero cost:** the expensive parts of facial likeness (photogrammetry scan rigs, high-end rigging suites, sub-division on pro workstations) are replaced by disciplined Blender sculpting from a single approved reference, AI-assisted texture work, and a strict QC loop. The cost is *labour and discipline*, not money.

## 2. Tools and resources

**Clearly distinguished: free/open-source vs paid.**

| Tool / resource | Cost | Role in facial likeness | Notes |
|---|---|---|---|
| **Blender 4.2.23 LTS** | **Free / open-source** | Primary authoring: sculpt, retopology, UV, texture-paint, rig, export. Already proven on Adanna V3/Guard V2. | The backbone. Runs on the M4 Mac and headless in the Linux sandbox for QC. |
| **Unreal Engine 5.8.4** | **Free** (UE EULA, this scale) | Import, materials, skeleton binding, animation, verification. | The owner Mac is the only UE machine. |
| **Git + Git LFS** | **Free** | Asset versioning, provenance, evidence. | Already live (M0.6). |
| **Python (Blender/UE scripting)** | **Free** | Pipeline automation, QC checks, import scripts, retargeting. | Agent-authored. |
| **Stable Diffusion / ComfyUI** | **Free / open-source** (local) | **Texture** generation, upscaling, ideation boards, material variation. | Runs on the M4 Mac via Apple MPS / CPU — **slow**; used for texture/ideation, **never** to generate the final face geometry or to replace the sculpted identity. |
| **Blender AI add-ons (e.g. texture/UV helpers)** | **Free** | Assisted texturing, UV prep. | Optional; reviewed before use. |
| Adobe / paid asset stores / paid AI APIs / cloud GPU | **PAID — NOT USED** | — | Explicitly excluded by the zero-budget constraint. |
| Reference PC (RTX 3060 Ti) | **Paid — future, not acquired** | Perf/visual sign-off target only. | Not a facial-production tool; D-12 pending. |

**Existing project assets that reduce effort (reuse, do not re-author):**
- The approved master portrait (`REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg`) — the single identity anchor.
- The **`HUMAN_BASE_PROPOSED`** skeleton (11 joints, identical bone names across Adanna V3 and Guard V2) — facial rig attaches to the shared `head` joint; retargeting is shared.
- The **PBR material-slot system** (`skin_base_v1`, `cloth_indigo_plain_v1`, `lips_v1`, `eye_dark_v1`, …) — new faces reuse the skin/eye/lip slots.
- The **GLB/FBX export + UE import scripts** (`import_adanna_production_v3.py` pattern) — reused for every character.
- The **Blender headless QC pipeline** (QC JSON, checksums, joint-influence, deform recheck) — reused for every character.

## 3. Quality strategy

**Realistic target (honest, not inflated):** a **consistent, recognizable, animation-ready stylized-realistic character face** — strong identity, clean topology, PBR skin, expression-ready — that reads well at gameplay camera distance. **This is NOT photoreal scan-based AAA likeness**, which requires photogrammetry rigs and professional artists and is **not achievable at zero cost**. We do not promise AAA photorealism; we promise the best disciplined stylized-realistic likeness the free pipeline can produce, proven by the PoC.

**How each quality dimension is maintained:**
- **Proportions & likeness consistency:** one approved identity anchor (the master portrait). Proportions measured from the approved reference. **Left/right feature locks preserved** (Adanna: cuffs + coral beads + scar on the **left**; no mirroring, no moving/duplicating identifying features to "improve recognition"). A second reference angle is produced **only** via an owner-approved process, never from unapproved turnarounds.
- **Realistic skin:** PBR skin material (base color, normal, roughness, subsurface) on the existing `skin_base_v1` slot; skin microdetail tuned for gameplay camera distance without overriding likeness or glamorizing.
- **Expressions:** a facial rig on the shared skeleton's `head` joint (brow, eyelid, jaw, cheek) enabling a neutral + guarded/defiant default + blink/talk, per the approved identity ("guarded/defiant default expression").
- **Hair:** the approved braids (top half in a high knot) sculpted and bound to the head; hair material slot reused.
- **Eyes:** `eye_dark_v1` material; eyes sculpted to match the reference, never generic.
- **Animation readiness:** clean facial topology, correct skin weights, a documented facial rig, and an expression turntable verified on the owner Mac.

**Avoiding generic / artificial / inconsistent faces:**
1. **Work from the specific approved reference**, never from a generic AI-generated face. AI generates **textures and ideation**, not the identity.
2. **AI never replaces the sculpted identity.** The face geometry is authored in Blender from the reference; AI is confined to texture/ideation/QC.
3. **Strict left/right feature preservation** and a single identity anchor per character.
4. **Owner review at every stage** — a face that drifts from the reference is rejected, not "good enough."

**Repeatable QC process:**
- **Automated (agent):** scale/orientation check, topology/UV check, weight-sum check, material-slot check, naming check — run headless in Blender on every export (reuse the existing QC pipeline).
- **Human (owner):** visual review against the approved portrait at each gate (sculpt → texture → rig → UE import); turntable + expression sheet; explicit pass/fail with recorded evidence.

## 4. Production pipeline

Each stage lists tools, agents, inputs, outputs, and the approval gate. Stages 0–3 and the PoC are the immediate path; 4–6 reuse the proven pipeline.

| Stage | Name | Tools | Agent / owner | Inputs | Outputs | Approval gate |
|---|---|---|---|---|---|---|
| **0** | Reference & identity lock | Git, Google Drive ref | Story + owner; agent archives | Approved master portrait; narrative constraints; cultural guide (CD-2 where applicable) | Consolidated identity pack: portrait, feature locks, left/right table, cultural clearances | Owner sign-off on the identity pack |
| **1** | Facial design / blocking | Blender (Sculpt) | Character Art (agent-assisted); owner reviews | Identity pack | Blocked facial sculpt from the reference | Owner visual review vs portrait |
| **2** | Retopology & UV | Blender (Retopo, UV) | Character Art + Technical Art; agent runs automated topology/UV QC | Blocked sculpt | Clean animation topology; unwrapped UVs; topology/UV QC report | Technical Art topology gate |
| **3** | Texturing | Blender (Texture Paint) + SD/ComfyUI (texture assist) | Character Art; agent generates/upscales textures; owner reviews | Retopo mesh; identity pack; material slots | PBR skin/eye/lip/hair textures on existing slots | Owner visual review (no generic drift) |
| **4** | Rigging | Blender (Armature) | Technical Art; agent automates rig/retarget | Retopo mesh; shared `HUMAN_BASE_PROPOSED` skeleton | Facial rig on `head` joint; expression controls | Technical Art rig gate |
| **5** | Animation readiness | Blender + UE | Engineering + Character Art; agent runs retarget/QC | Rigged face; shared skeleton; expression sheet | Expression turntable; blink/talk; retarget test on the shared skeleton | Owner review of the turntable |
| **6** | UE integration & verification | UE 5.8.4 + import scripts | Engineering; owner executes on Mac | GLB/FBX export; integration spec | Imported face on the pawn; verification bundle | Owner-Mac verification (see §6 / integration spec) |

**Testing & approval before production use:** no asset enters production until it passes the automated QC bundle (agent) **and** the owner's visual review (human), with evidence recorded. Exploratory assets stay labelled (`WIP_`/`interim`) until signed off (QUALITY §7).

## 5. Hardware and technical limitations

**What is realistically achievable with existing hardware:**
- **Owner Mac M4 / 16 GB:** Blender sculpt, retopology, UV, texture-paint, rigging, export — **fully feasible** (proven on Adanna V3). UE import and verification — **feasible** with swap pressure. Local Stable Diffusion via Apple MPS/CPU — **feasible but slow**; suitable for texture/ideation batches run off-peak, **not** for real-time or heavy geometry generation.
- **Linux agent sandbox:** Blender **headless** QC, Python pipeline automation, texture prep — **feasible** (proven). No GPU for heavy AI; AI model *training* is not feasible locally.

**Workloads handled locally vs alternative free resources:**
- **Local (M4 Mac / sandbox):** all Blender authoring, QC, import, verification; SD texture/ideation (slow).
- **Alternative free resources:** none required beyond the local stack. **No paid cloud GPU is assumed or used.**

**Technical bottlenecks and workable solutions:**
1. **16 GB RAM swap pressure in UE/Blender** → external SSD for DDC (D-18); plugin/viewport pruning; keep meshes within the proven tri budget (Adanna V3 = 13,680 tris); bake rather than keep high-poly in runtime.
2. **No discrete GPU for fast AI** → confine AI to texture/ideation, batch off-peak, prefer CPU/MPS; do **not** use AI for the identity geometry.
3. **Single machine (one Mac)** → serialise Mac use to discrete verification runs; do all authoring/QC in the sandbox where possible; the agent-owner evidence loop (proven at M0) keeps the Mac duty bounded.
4. **No photogrammetry** → build likeness from the single approved portrait + disciplined anatomy; do not claim scan-based photorealism.
5. **Reference PC not yet acquired** → perf/visual sign-off deferred; facial production does not depend on it.

## 6. Execution plan

**Phased, with a mandatory PoC before full production.**

| Phase | Goal | Owner / agent | Deliverables | Acceptance criteria |
|---|---|---|---|---|
| **P0 — PoC (Adanna face)** | Demonstrate actual achievable facial likeness quality on ONE face before committing | Character Art + Technical Art (agent); owner reviews | Blocked facial sculpt → retopo → PBR texture → facial rig → expression turntable → UE import, all from the approved portrait | Owner-Mac verification passes (scale, topology, materials, rig, turntable reads as the approved identity); evidence bundle recorded. **This is the go/no-go for the quality tier.** |
| **P1 — Pipeline hardening** | Lock the reusable pipeline | Technical Art + Engineering (agent) | Import/QC scripts, naming, material slots, retargeting, acceptance tests | Automated QC green on the PoC; integration spec accepted |
| **P2 — Adanna production face** | Produce the full Adanna facial likeness | Character Art (agent); owner signs off | Final Adanna face mesh/rig/textures + UE integration | Passes PoC bar + owner sign-off + cultural clearance (CD-2 where applicable) |
| **P3 — Scale to remaining characters** | Reuse the pipeline for enemies/NPCs | Character Art + Engineering (agent); owner signs off | Each character's face through the same pipeline | Same acceptance bar; skeleton/materials/import reused, only sculpt/texture/identity differ |

**Proof of concept (P0) — the non-negotiable gate:** before any full production, produce **one** Adanna facial likeness (sculpt → texture → rig → turntable → UE import) from the approved portrait, verified on the owner Mac. The PoC **demonstrates the real achievable quality**; if it does not meet the agreed bar, the strategy is revised before scaling. **No AAA claim is made without this evidence.**

**Scaling without repeating work:** the `HUMAN_BASE_PROPOSED` skeleton, the PBR material-slot system, the GLB/FBX import scripts, the headless QC pipeline and the acceptance tests are **reused unchanged** for every character. Per-character effort is confined to: the sculpt, the texture/identity, and the owner's review. This is how the pipeline scales to the remaining characters (enemies, NPCs) at minimal marginal cost.

**Owner approval is required before implementation.** The PoC (P0) is the first executable step once approved.
