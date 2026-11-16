# THE DISOBEDIENT DAUGHTER — MASTER ENGINEERING ARCHITECTURE DOCUMENT

**Working title (Igbo):** *Nwanyi Na-anụghị Ihe*
**Document ID:** TDD-MEAD-001
**Version:** 1.0
**Date:** 2026-11-16
**Status:** PROPOSED — awaiting Technical Director (ChatGPT) review and Creative Director ratification
**Owner:** Engineering (jointly: Agent 1 / Agent 2 / Agent 3, see §12)
**Supersedes:** nothing (first architecture document)

---

## 0. How to read this document

This document is the engineering contract for the project. It states:

1. **What actually exists today** (§2) — verified by inspection, not assumed.
2. **What the architecture must be** (§4–§11) — system boundaries, interfaces, data contracts.
3. **What is already decided by canon** and therefore *not* an engineering choice (§3).
4. **What remains undecided** and who decides it (§16).

Statements carry a status tag. The tag vocabulary is used consistently throughout the project and in every
engineering report:

| Tag | Meaning |
|---|---|
| **ESTABLISHED** | Built, runs, and passed its acceptance tests in the current milestone. Evidence exists and is linked. |
| **PARTIAL** | Some of the system works and is tested; named sub-features do not. The gap is listed. |
| **SPEC** | Specified here and agreed, not yet implemented. |
| **STUB** | Interface exists so integration can proceed; behaviour is a deliberate no-op or debug fallback. Never presented as gameplay. |
| **EXPERIMENTAL** | Implemented behind a flag, unproven, not a dependency of any milestone. |
| **MOCKED** | Stands in for a real subsystem (e.g. a recorded animation cue instead of motion matching). Labelled in-game in debug builds. |
| **BLOCKED** | Cannot proceed without a decision or an external input. The blocker is named. |
| **UNAVAILABLE** | Cannot be executed in the current environment at all. |

Two rules follow from the project directive and are binding on all agents:

- **No tag inflation.** A system may not be reported ESTABLISHED without a linked, reproducible test.
- **No silent substitution.** If a real subsystem is replaced by a mock for integration, the mock is registered in
  the Mock Ledger (§13.4), not described as the feature.

---

## 1. Executive summary

The repository at base commit `5e3d1da` contains **one file** (`README.md`, six bytes of content) and no Unreal
project. There is no code, no content, no configuration, no plugin list, no build script, no test suite. Everything
in the *Master Game Development Directive* is therefore **greenfield work**, with one important qualification:

**The creative canon is not greenfield.** A substantial and internally consistent Art Bible exists in Google Drive:
character identity locks, environment rules per chapter, 59 numbered art decisions (OAD-01 … OAD-59, many
RESOLVED), a seven-memory narrative sequence with scene IDs, and an environment register carrying canonical
location IDs (`CH01-SCN-046`, `CH08-SUB-007`, …). **These IDs are load-bearing.** Levels, quest actors, memory
triggers, save data and telemetry must key off them. This document fixes that contract in §6 before a single
line of gameplay code is written, because retrofitting story IDs into save files after playtesting starts is
expensive and error-prone.

The engineering posture this document takes:

- **Baseline: Unreal Engine 5.8.** Released 2026-06-17, and the **last planned major UE5 release** (Epic has
  reserved the option of a 5.9, and targets UE6 Early Access for late 2027). Starting a multi-year production on
  a terminal minor release is the correct risk position: the engine will not churn under us, and 5.8 has
  production-ready MegaLights, a Lumen Lite path, production PCG + Substrate, and improved PSO precaching —
  all directly useful to a dark, atmosphere-heavy, foliage-dense game. Detail and rationale: §5 and ADR-0002.
- **Vertical slice first, but not a fake one.** The first playable milestone is a *complete loop* through one
  chapter's worth of mechanics — movement, camera, combat, one enemy archetype, one boss phase, one memory
  discovery, save/load — on **shippable-quality architecture**, with primitive art. The art is replaced;
  the architecture is not. This is the only way to satisfy both "playable" and "not a visual prototype" in
  a staged production.
- **One authority per system.** Three agents work in parallel; §12 assigns every subsystem to exactly one
  owning agent, with explicit interfaces for the other two. Competing implementations are a release blocker.
- **Evidence-or-silence.** Every milestone gate requires a named, reproducible evidence artefact under
  `Docs/evidence/`. Reports that assert success without evidence are rejected at review.

Two environment realities constrain *how* work is verified here, and are stated up front rather than
discovered later:

1. **No Unreal Engine in this sandbox.** There is no `UnrealEditor`, no `UBT`/`UAT`, no GPU, and no
   ability to launch PIE. C++ and configuration can be authored here; they **cannot be compiled or run here**.
   Any claim of the form "the character moves correctly" must come from a machine that runs the editor, and be
   filed as evidence with build ID, engine version and test name. See §13 and ADR-0005.
2. **Binary assets do not belong in this Git repository.** The project is on GitHub without LFS provisioned;
   `.umap`, `.uasset`, MetaHuman data, audio and video will destroy it. §10 fixes the asset policy and the
   content-ownership boundary *before* content production begins, so no agent has to make that call under
   pressure later. See ADR-0004.

---

## 2. Current project assessment (verified 2026-11-16)

### 2.1 Repository facts

| Item | Finding | Method |
|---|---|---|
| Branch | `arena/5dde91a4-tdd`, from `main` @ `5e3d1da` | `git log`, `git branch -a` |
| Commits | 1 (`5e3d1da Initial commit`) | `git log --all` |
| Tracked files | 1 — `README.md` (content: `# TDD`) | `git ls-tree -r main` |
| Unreal project (`.uproject`) | **None** | `find` |
| `Source/`, `Config/`, `Content/` | **Absent** (created empty scaffolding by this document's authoring pass) | `find` |
| Build scripts (`Build.sh`, `GenerateProjectFiles`, UAT) | **None** | — |
| Plugins / `.uplugin` | **None** | — |
| Automated tests | **None** | — |
| CI configuration | **None** | — |
| `.gitignore` / `.gitattributes` | **None** | — |
| Git LFS | **Not provisioned** | `git remote -v`, no LFS config |
| Repo size | 116 KB (`.git`) | `du -sh` |
| Engine installation | **Absent**; no editor binary on PATH, no `/opt` engine | `which UnrealEditor`, `ls /opt` |
| GPU / display | **None assumed**; headless sandbox | environment |
| Toolchain available | Python 3.11.2 (no `pytest`), Node 22 / Yarn 1.22, `git`, `gh` | `python3 -V`, `which` |

**World scale, established 2026-11-16 by reading the location and scene registers:** 8 major environments,
142 other locations, 46 interiors, **135 scenes and micro-locations**, 40 environment-state references. Only
4 main story scenes and 9 secondary story scenes exist in the whole game; the rest is ambient life, exploration
and atmosphere. Chapter 1 alone has 46 scenes. This sizes the world systems directly — see
`Docs/WORLD_ASSESSMENT.md`.

**Conclusion:** the engineering baseline is *zero*. There is no existing functionality to preserve, no prior
agent work to integrate, and no technical debt to pay down. That is an advantage — the project gets a clean
architecture — but it also means **nothing can be declared working until a machine with the engine runs it.**

### 2.2 What exists outside the repository (authoritative, and it is not code)

Verified by reading Google Drive on 2026-11-16. This is **creative canon**, and it is the input to §3.

| Drive document | Content relevant to engineering | Status of doc |
|---|---|---|
| `CHARACTER_DESIGN_REGISTER.md` (v. 2026-11-15, 14,538 B in `17_DOCUMENTATION/Character_Registers`) | Identity locks for Adanna, Ezeani, Nneka, Okwu, Amadioha, Idemili, Hollow King; 13 supporting cast; NPC population; per-feature **side rules** for Adanna; timeline facts | Canon reference |
| `ENVIRONMENT_DESIGN_REGISTER.md` (v002, 10,213 B) | Per-chapter visual identity, per-chapter *rules*, recurring production faults, governing landmarks (e.g. the Great Root Mother tree) | Canon reference; location IDs live in sibling registers |
| `OPEN_ART_DECISIONS.md` (21,812 B) | **OAD-01 … OAD-59.** Many RESOLVED. Includes design-approval ≠ canon-approval (OAD-47/48), python rule (OAD-14), Okwu hood (OAD-12), clothing standard (OAD-55/56), endings (OAD-27/31/32) | Decisions register |
| `NNEKA_MEMORIES_AND_TIMELINE.md` (v1.2, 21,024 B) | The seven memories with scene IDs and discovery fragments; concealment mechanics; the 25-year timeline; established facts list | Canon + PROPOSED detail |
| `LOCATION_MASTER_REGISTER.md` (534,140 B), `SCENE_AND_MICROLOCATION_MASTER_REGISTER.md` (278,372 B) | Canonical `CHxx-*` identifiers and status per location/scene | Canon register (large; sampled, not exhaustively read) |
| `13_GAMEPLAY_AND_LEVEL_DESIGN/` | **Empty** — no gameplay or level design documents exist yet | — |

**Critical engineering consequence:** the Art Bible is a *visual and narrative* authority. It contains
**no** combat design, no movement specification, no enemy AI design, no progression numbers, no audio design,
no UI specification, and no technical design of any kind. `13_GAMEPLAY_AND_LEVEL_DESIGN` is empty.
Those must be authored as **engineering specifications** (§6–§9) and, where they express design intent rather
than implementation detail, **ratified by the Creative Director** — they are not canon until he says so.

### 2.3 Gap analysis against the directive

| Directive requirement | Exists today | Engineering action |
|---|---|---|
| Third-person movement & physics | Nothing | Stage 2 — `UTDDCharacterMovementComponent` on `CMC` (§7.2) |
| Camera & controls | Nothing | Stage 2 — custom orbit camera + input abstraction (§7.3) |
| Combat & hit detection | Nothing | Stage 3 — data-driven combat, hit arbitration (§7.4) |
| Weapon handling & animation | Nothing | Stage 4 — GAS-lite ability layer + anim contract (§7.5, §9) |
| Enemy behaviour & AI | Nothing | Stage 5 — StateTree-based enemies (§8.2) |
| Boss architecture | Nothing | Stage 5 — phase-graph bosses (§8.3) |
| Exploration & traversal | Nothing | Stage 6 — traversal component, chapter streaming (§8.5) |
| Environmental interaction | Nothing | Stage 6 — interactable interface (§8.6) |
| NPC behaviour & world simulation | Nothing | Stage 6 — Mass + StateTree civilians (§8.4) |
| Quest/mission/progression | Nothing | Stage 7 — campaign graph + memory ledger (§9) |
| Inventory & equipment | Nothing | Stage 7 — minimal, justified by canon (§9.5) |
| Story delivery / cinematics | Nothing | Stage 7 — sequencer-driven with ID contract (§9.4) |
| Audio & feedback | Nothing | Cross-cutting, §9.7 |
| Save/load & persistence | Nothing | Stage 1 + Stage 7 — versioned save (§9.6) |
| Performance optimisation | Nothing | Continuous; gates at Stage 5/9 (§14) |
| Build & release | Nothing | Stage 9; early smoke build at Stage 1 (§15) |

---

## 3. Canon constraints that bind the architecture

These are **not** engineering choices. They are inputs. An engineer who violates them is producing
non-canon content, and review must reject it regardless of code quality.

### 3.1 Fixed narrative facts (ESTABLISHED)

| Fact | Source |
|---|---|
| Adanna is 25 at game start; a formidable warrior; daughter of Ezeani | Directive; character register |
| Adanna was **six** when Nneka died; nineteen years pass between death and game start | OAD-35; register timeline facts |
| Ezeani killed Nneka | ESTABLISHED canon (memories doc §Status) |
| The boundary demanded Adanna; Nneka offered herself; asked Ezeani to do it; he did; then let Adanna believe he was simply a murderer | OAD-34, APPROVED IN PRINCIPLE |
| Both parents hid memories, for different motives | OAD-34 |
| The Hollow King began erasing the boundary ~1 year before the game opens | OAD-41 |
| Why Nneka's voice reaches Adanna at 25: boundary weakening lets her deliberately call | OAD-39 |
| Eight chapters with named locations and bosses | Directive §2 |
| Seven hidden memories, one in Chapters 1–7; all seven required for Ending 3 | OAD-32 |
| Three endings: kill Ezeani / spare Ezeani / hidden ending | OAD-27; OAD-31 (Ending 1 killing is **literal**) |
| Nneka is dead; any voice or appearance must never imply otherwise | OAD-39 |

### 3.2 Design constraints that produce hard technical requirements

| Canon rule | Source | Technical consequence |
|---|---|---|
| The seven memories are met as **fragments** (place, object, sound, interaction, then memory) and **not** as collectible cutscenes | OAD-32 | Memory delivery is *multi-stage world interaction*, not a pickup + playback. Requires a staged interaction state machine and audio-first delivery (§9.3). |
| Each memory "is found where a place echoes it; it did not necessarily happen there" | Memories doc | Memory scenes are **separate sublevels/sequencer assets** from their discovery location. Trigger and content are decoupled. |
| Environment design approval ≠ canon approval (OAD-47, OAD-48) | OAD-47, OAD-48; LOCATION_MASTER_REGISTER v2.9 | Two **independent** status fields, never collapsed: canon status (`ESTABLISHED` / `PROPOSED` / `PENDING APPROVAL`) and environment design status (`NOT STARTED` … `APPROVED`). See `Docs/CANON_INDEX.md` §2. |
| Chapter 4: pythons are never enemies and never loot | OAD-14 | Fauna spawn tables must be data-driven with per-chapter exclusion lists. Hard-coding "hostile snake" is a canon bug. |
| Chapter 2 has no living flame until the boss; Chapter 4 has no lightning (reserved for Amadioha); Chapter 5 lightning is white only | Environment register | Lighting/VFX capability flags per chapter level, enforced by a validation test (§13.3). |
| The Great Root Mother tree must be visible from every major clearing in Chapter 1 and is the navigation landmark | Environment register, OAD-11 | World composition constraint + a visibility assertion test per Chapter 1 scene. |
| Chapter 7's ramparts must read as earth and burnt timber, never coursed masonry; ember red only deep in cracks, never flame | Environment register | Material/asset validation list; no generic castle kit permitted. |
| Chapter 6: all face coverings are invented, featureless, at most two eye slits | Environment register; needs consultant review | Asset validation flag on mask assets; content review gate. |
| No remains are ever shown in Chapter 3 | Environment register | Prop exclusion list per chapter. |
| Okwu's hood shows darkness only, in every light, always | OAD-12 | Material rule: an unlit/black-hole material that is exempt from Lumen GI bleed; needs a specific rendering solution (§9.8). |
| Okwu must stay clearly distinct from any real masquerade form | OAD-04 | Cultural review gate before any Okwu shippable asset. |
| Adanna's features are never mirrored or moved; right side is plain | OAD-51 | Skeletal mesh and material must not be mirror-instanced; LODs and ports must preserve side. Character validation test. |
| Adanna carries exactly one weapon: short leaf-bladed iron sword (~60 cm), left hip; no spear, no second weapon | Character register, OAD-09, OAD-37 | Inventory system must be *constrained by canon default*, not generic. Second-weapon slots are out of scope unless approved. |
| Amadioha: human form, ~5 m, no armour/crown/weapon, fulgurite staff | OAD-05, OAD-16 APPROVED | Boss rig scale and camera framing requirements. |
| Settlement villager clothing standard: constructed torso-covering garments, varied; not a uniform | OAD-55/56 | NPC variation must come from a **garment-variant data set**, not random material colour. Crowd system requirement (§8.4). |
| Invented mythology must never be presented as authentic Igbo tradition | Directive §1 | In-game codex/credits must carry a **fictionality statement**; cultural review gate on deity depictions. |

### 3.3 Canon identifiers — the contract

The registers use a stable, human-readable ID scheme. **Adopt it verbatim; do not invent a parallel scheme.**

```
CHxx                 chapter, zero-padded: CH01 … CH08
CHxx-ENV-001         major environment (one per chapter)
CHxx-SUB-nnn         sub-location
CHxx-SET-nnn         settlement
CHxx-INT-nnn         interior
CHxx-LMK-nnn         landmark
CHxx-TRV-nnn         traversal area
CHxx-EXP-nnn         exploration area
CHxx-BOS-nnn         boss arena
CHxx-SCN-nnn         scene or micro-location
```

> **Corrected 2026-11-16 (Agent 2, index v2.0.0).** §3.3 originally proposed `CHxx-BOSS-<slug>` for boss
> arenas and recognised only three categories. Reading `LOCATION_MASTER_REGISTER.md` v2.9 showed arenas use
> `BOS` with a numeric suffix and that six further categories exist. See `Docs/CANON_INDEX.md` §7.

Known-good examples verified against the registers:

| ID | Meaning | Source |
|---|---|---|
| `CH01-SCN-046` | Memory 1 discovery scene (register status: PENDING APPROVAL) | Memories doc; scene register |
| `CH01-SUB-018` | The Wayside Offering Place (register status: PROPOSED) | Memories doc; location register |
| `CH01-BOS-001` | Great Root Mother Arena (ESTABLISHED encounter; design IN REVIEW) | Location register |
| `CH02-SUB-003` | The Clear Water | Memories doc |
| `CH03-INT-001` | A House, Meal Uneaten | Memories doc |
| `CH04-SUB-002` | The Shrine Landing | Memories doc |
| `CH05-SUB-002` | The Oath Ground | Memories doc |
| `CH06-INT-003` | A Memory Room | Memories doc |
| `CH07-INT-005` | The Shrine No One Remembers | Memories doc |
| `CH08-SUB-005` | Mothers' Courtyard | OAD-45 |
| `CH08-SUB-006` | Nneka's House, exterior | OAD-45 |
| `CH08-SUB-007` | Sealed Quarter | OAD-45 |
| `CH08-INT-001` | Nneka's House, interior | OAD-45 |
| `CH08-INT-003` | Hall of Posts | OAD-45 |

**Rule:** an ID that is not present in the Drive registers is not canonical. Engineering may *propose* new IDs
(suffix `-P`) but they stay `PROPOSED` until the registers are updated by the authority that owns them.
`Tools/canon/data/canon_index.json` in this repository holds the engineering-side working index and is validated
against a schema in CI (§13.2).

---

## 4. Proposed technical architecture

### 4.1 Architectural principles

1. **Data over code where design will iterate.** Combat, enemy tuning, memory triggers, quest objectives and
   canon rule-sets are Data Assets (`.uasset` → `UDataAsset`), not C++ constants. Designers must be able to
   change a boss phase threshold without an engineer and a recompile.
2. **One owning agent per subsystem.** §12. Cross-agent changes go through an interface file, not an edit to
   another agent's implementation.
3. **Interfaces are narrow and versioned.** Public headers are the contract. A gameplay-facing API that must
   survive refactors is documented at its declaration *and* in §6.
4. **The world is streamed, never one level.** Eight chapters, each a persistent level plus world-partitioned
   cells. No monolithic map. (§8.5)
5. **Engine stock where it is good.** Use `CMC` (Character Movement Component), `GAS` where it earns its cost,
   `StateTree` for behaviour, `Mass` for crowds, `Niagara` for VFX, `MetaSounds` for audio, `Sequencer` for
   cinematics, `CommonUI` for UI. **Do not** build a custom physics, AI or animation framework. Deviations
   require an ADR.
6. **Testability is a design input.** Every system has a deterministic seam: combat resolution, memory gating,
   save serialisation, canon validation are all testable without a renderer.
7. **Performance budgets are per-system and enforced early.** §14. A system that cannot meet its budget is
   reported, not hidden.

### 4.2 Module layout (target)

```
TDD.uproject
├── Config/
│   ├── DefaultEngine.ini          Rendering, streaming, physics, networking
│   ├── DefaultGame.ini            Packaging, project ID
│   ├── DefaultInput.ini           Enhanced Input defaults
│   └── DefaultGameplayTags.ini    Gameplay tag registry (canonical, versioned)
├── Source/
│   ├── TDD.uproject targets: TDD (Game), TDDEditor (Editor), TDDServer (dedicated, later)
│   ├── TDDRuntime/                Primary game module — gameplay, world, progression
│   │   ├── Core/                  GameMode, GameState, PlayerState, GameInstance, subsystem registry
│   │   ├── Character/             Adanna: movement, camera, animation bridge, traversal
│   │   ├── Combat/                Ability layer, hit arbitration, damage resolution, weapons
│   │   ├── AI/                    Enemy pawns, StateTree tasks, perception, boss phase graph
│   │   ├── World/                 Chapter director, streaming, interactables, memory director
│   │   ├── Progression/           Campaign graph, memory ledger, save/load, endings
│   │   ├── Narrative/             Dialogue, cinematics glue, codex
│   │   ├── Audio/                 MetaSound routing, mix states, music director
│   │   ├── UI/                    CommonUI roots, HUD, menus (view-model driven)
│   │   └── Framework/             Shared: interfaces, canon validation, telemetry
│   ├── TDDEditor/                 Editor-only: asset validators, canon linters, bulk tools
│   └── TDDTests/                  Automation tests (UE Automation Spec) + test data
├── Content/                       (see §10 — LFS or external store; placeholder structure committed)
└── Tools/
    ├── canon/                     Canon index + validators (Python, stdlib only)
    └── ci/                        Build/test driver scripts
```

### 4.3 Key architectural decisions (ADR index)

Full records in `Docs/adr/`. Summary:

| ADR | Decision | State | Rationale (short) |
|---|---|---|---|
| 0001 | Use UE **automation framework** (`IMPLEMENT_SIMPLE_AUTOMATION_TEST` / Spec) as the only unit-test harness; no third-party test frameworks in-engine | ACCEPTED | Zero dependency; runs headless via `-ExecCmds="Automation RunTests TDD"`; supports CI |
| 0002 | Baseline engine **UE 5.8** | ACCEPTED (pending TD confirm) | Terminal UE5 release ⇒ stable target; MegaLights/Lumen Lite/PCG production-ready; PSO precaching matters for our stutter-prone content |
| 0003 | **No GAS for movement**; GAS adopted only for combat abilities + attribute sets | ACCEPTED | GAS is excellent for abilities/effects and costly for locomotion; CMC + a thin ability layer is faster to iterate and easier for three agents to share |
| 0004 | **Git holds text only**; binaries in LFS *or* external store | PROPOSED — needs CD decision | Repo is on GitHub without LFS; 8 chapters of content will exceed sane repo size; ownership must be explicit before content production |
| 0005 | **Engine-side verification is required** for any "works" claim; sandbox verification limited to canon/tooling | ACCEPTED | There is no engine in this environment; honesty requirement |
| 0006 | Canonical ID scheme adopted from Drive registers; engineering maintains a validated mirror index | ACCEPTED | Prevents save-data and quest drift |
| 0007 | Bosses use a **declarative phase graph** data asset, not bespoke per-boss C++ | ACCEPTED | Seven+ bosses; bespoke code does not scale across three agents |
| 0008 | Memories delivered as **staged fragment state machines** with audio-first cues; sequencer playback is the *last* stage | ACCEPTED | Required by OAD-32 ("not collectible cutscenes") |

---

## 5. Engine and project configuration

### 5.1 Engine baseline

| Decision | Value | Notes |
|---|---|---|
| Engine | **UE 5.8** | Last planned UE5 major (Epic, State of Unreal 2026). Option to 5.9 reserved by Epic. |
| Project type | C++ project with Blueprint subclasses | Gameplay-critical systems in C++; content and tuning in BP/Data Assets |
| Target platforms | **PC (Win64) primary**, current-gen console later | Directive does not name platforms; PC-first is the only verifiable default |
| Renderer | Deferred, Lumen **High Quality** for PC hero paths; **Lumen Lite** path required for 60 fps tier | 5.8 shipped a lightweight dynamic GI path; use it as the scalable tier |
| Lighting | Fully dynamic, no baked lightmaps for hero content; MegaLights (production-ready in 5.8) for dense local lights | Our art direction is contrast-heavy (ember cracks, mist shafts, lightning) — many small dynamic lights |
| Virtual geometry | Nanite on environment hero meshes; **Nanite Foliage** flagged EXPERIMENTAL (it was experimental in 5.7) and evaluated, not assumed | Dense rainforest in Ch01 is the test case |
| World building | World Partition + OFPA; **PCG** (production-ready in 5.8) for foliage/debris scatter | Scatter must be deterministic + seedable for art review reproducibility |
| Physics | Chaos (engine default) | No custom physics |
| Animation | Animation Blueprint + **Motion Matching** evaluated for locomotion; Control Rig for IK/procedural fixes | Motion Matching cost/benefit vs. our animation volume is an open decision (§16, D-07) |
| Audio | MetaSounds + Quartz; submix hierarchy built at Stage 1 | Memory fragments are audio-first (OAD-32), so audio is not a late-stage bolt-on |
| UI | CommonUI + UMG, view-model pattern | |
| Networking | Single-player. No replication architecture | Directive is a single-player action-adventure. Do **not** pay replication cost. `TDDServer` target deferred indefinitely. |

### 5.2 Project settings that must be fixed at Stage 1 (not defaults-by-accident)

| Setting | Value | Why |
|---|---|---|
| `r.DefaultFeature.AutoExposure` | Manual exposure per chapter, with eye-adaptation only where art approves | Ch07 "images too dark" and Ch03 "ash reads as snow" are both auto-exposure failures in the register |
| `r.DynamicGlobalIlluminationMethod` | Lumen; project-level tier switch | §14 |
| `bUseFixedFrameRate` in automation maps | true (60) | Determinism for tests |
| `MaxChannelsCount` (animation) | Per-character, not global inflation | Crowd NPCs must not cost hero budget (§14) |
| World Partition cell size | Per chapter, specified in a chapter config Data Asset | Forest needs different cells to an interior city |
| `bEnableWorldBoundsChecks` | true | Memory sublevels are small; kill-Z must be authored, not global |
| Gameplay Tags | Registered in `DefaultGameplayTags.ini`, reviewed like code | Tags are the cross-agent vocabulary (§6.6) |

### 5.3 What is deliberately *not* configured yet

- **Nanite skinning for hero characters** — evaluate after Stage 4, not before (skin/rig iteration cost).
- **MetaHuman pipeline** — a decision, not a default. MetaHuman gives quality but imposes a pipeline, licence
  review, and a likeness-review obligation for West African facial features; see D-09. Adanna's identity locks
  are specific (7.5 heads, scar, side-specific ornament) and must survive any pipeline.
- **Console SDKs** — unavailable here; must not appear in any build script until provisioned.

---

## 6. Core gameplay systems and inter-agent contracts

This section is the heart of the document: what each system *is*, what it *owns*, and what it *promises*
to the other two agents.

### 6.1 System map

```
                       ┌───────────────────────────────┐
                       │  TDDRuntime/Core              │
                       │  GameMode · GameState ·       │
                       │  Subsystem registry · Tags    │
                       └───────────┬───────────────────┘
            ┌──────────────────────┼──────────────────────────┐
            │                      │                          │
   ┌────────▼────────┐    ┌────────▼─────────┐      ┌─────────▼────────┐
   │ CHARACTER (A1)  │    │ COMBAT (A1)      │      │ WORLD (A2)       │
   │ movement/camera │    │ abilities/damage │      │ chapters/stream  │
   │ anim bridge     │    │ hit arbitration  │      │ interactables    │
   │ traversal       │    │ weapons          │      │ memory director  │
   └────────┬────────┘    └────────┬─────────┘      └─────────┬────────┘
            │                      │                          │
   ┌────────▼────────┐    ┌────────▼─────────┐      ┌─────────▼────────┐
   │ AI (A2)         │    │ AUDIO (A2)       │      │ PROGRESSION (A3) │
   │ StateTree       │    │ MetaSound/mix    │      │ campaign graph   │
   │ perception      │    │ music director   │      │ memory ledger    │
   │ boss phase graph│    │                  │      │ save/load        │
   └─────────────────┘    └──────────────────┘      └──────────────────┘
                                   ▲
                          ┌────────┴─────────┐
                          │ UI (A3)          │
                          │ CommonUI/VMs     │
                          │ save UI, codex   │
                          └──────────────────┘
```

### 6.2 Identity and ID types (shared value types — owned by Core, frozen early)

All systems speak these. They are `USTRUCT`s and `UENUM`s in `TDDRuntime/Public/Framework/`.

```cpp
// TDDIds.h — SPEC. Frozen at Stage 1. Changes require an ADR + save-version bump.

USTRUCT(BlueprintType)
struct FTDDLocationId
{
    GENERATED_BODY()
    /** Canonical register ID, e.g. "CH04-SUB-002". Never a display name. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName Id;
};

UENUM(BlueprintType)
enum class ETDDApprovalState : uint8
{
    Proposed,          // PROPOSED, not canon
    DesignApproved,    // visual design signed off only (OAD-47)
    CanonApproved,     // established story location/character
    Shippable          // passes all gates incl. cultural review
};

UENUM(BlueprintType)
enum class ETDDChapter : uint8 { Ch01_ForbiddenForest, Ch02_KingdomBeneathEarth,
    Ch03_CityOfLivingDead, Ch04_RiverOfIdemili, Ch05_MountainOfThunder,
    Ch06_KingdomOfMasks, Ch07_GatesOfTheDead, Ch08_LastDaughter, None };

USTRUCT(BlueprintType)
struct FTDDMemoryId
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere, BlueprintReadOnly) int32 Index;        // 1..7, canon order
    UPROPERTY(EditAnywhere, BlueprintReadOnly) ETDDChapter Chapter;
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName SceneId;      // e.g. CH01-SCN-046
    UPROPERTY(EditAnywhere, BlueprintReadOnly) FName LocationId;   // e.g. CH01-SUB-018
};
```

**Why this matters:** the seven memories map to `(Index, Chapter, SceneId, LocationId)`. The save file stores
`Index` plus a *content hash* of the memory's fragment definition, so an edited memory definition invalidates
a stale completion flag rather than silently mis-granting Ending 3.

### 6.3 Character & camera contract (Agent 1 → all)

| Field / method | Contract |
|---|---|
| `ATDDCharacter` | `ACharacter` subclass; camera boom + spring arm; `UTDDCharacterMovementComponent` |
| `FTDDLocomotionState` | `Idle, Walk, Jog, Sprint, Strafe, Land, Slide, Vault, ClimbLite, Ragdoll, Cinematic` — authoritative for audio and animation |
| `OnLocomotionStateChanged` | Multicast delegate; **audio (A2) and UI (A3) subscribe, never poll** |
| `GetMoveIntent()` | `FVector2D` from Enhanced Input, camera-relative; combat locks rotation independently |
| Traversal | `UTDDTraversalComponent` with named `ETDDTraversalAction` (vault / ledge-grab / climb-lite / drop). Chapter gating via `FGameplayTag` requirements |
| Root motion | Authoritative for attacks and cinematics; capsule movement for locomotion. No mixed mode inside one montage |
| Adanna-only constraints | One weapon (`ETDDWeaponSlot::Primary` only, defaults to *short iron sword*); no mirror-scaling; left-side ornaments validated by test |

**Non-goal (explicit):** no climbing system beyond scripted `ClimbLite` and vaults at Stage 2. A full free-climb
system is a separate high-cost feature and is not justified by any canon reference currently available.

### 6.4 Combat contract (Agent 1)

```cpp
// TDDCombatTypes.h — SPEC
UENUM() enum class ETDDHitResult : uint8 { Hit, Blocked, Parried, Dodged, Invulnerable, Miss };
UENUM() enum class ETDDDamageType : uint8 { Iron, Divine_Thunder, Divine_Water, Ancestral, Environmental };

USTRUCT() struct FTDDAttackDefinition
{
    FGameplayTag AttackTag;         // e.g. Ability.Attack.Light.Combo1
    float WindupSec, ActiveSec, RecoverySec;   // data, designer-tunable
    float BaseDamage, PoiseDamage, StaminaCost;
    FName HitWindowSocketRoot;      // bones from which sweeping volumes grow
    TObjectPtr<UAnimMontage> Montage;
};

USTRUCT() struct FTDDHitEvent
{
    FTDDAttackDefinition Attack;
    TWeakObjectPtr<AActor> Instigator, Target;
    ETDDHitResult Result;
    FVector_NetQuantize Location;   // reused for local hit FX placement
    int64 FrameStamp;
};
```

Rules:
- **Hit arbitration is single-owner.** Only `UTDDHitArbiter` (a world subsystem) decides Hit/Blocked/Parried.
  Abilities request a hit; they do not apply damage directly. This prevents the classic three-agent bug where
  two systems both apply the same damage.
- **I-frames are declared, not discovered.** `UTDDInvulnerabilityComponent` with tag-based windows
  (`State.Invulnerable.Dodge`) so AI and UI can query intent.
- **Poise, not health, drives boss feedback.** Bosses read poise breaks; this is what makes heavy hits *feel*
  correct and it is cheap to tune via Data Assets.
- **Canon guard:** `ETDDDamageType::Divine_Water` exists for Idemili's domain; **snakes are excluded as
  damage sources in Ch04** by a data rule, satisfying OAD-14 by construction rather than by art discipline.

### 6.5 Ability layer (GAS, constrained)

`UTDDAbilitySystemComponent` on characters; AttributeSets: `TDDVitals` (Health, Stamina, Poise, Resolve),
`TDDCombatStats`. GameplayEffects for damage and status. **Movement is not an ability.** Enemy AI reads
attributes, never writes them (only the damage pipeline writes).

### 6.6 Gameplay Tag vocabulary (cross-agent contract)

Namespaces are closed and reviewed like code:

```
Chapter.Ch01 … Chapter.Ch08
State.Locomotion.<Idle|Jog|Sprint|Strafe|Vault|Slide|Cinematic>
State.Combat.<InCombat|Staggered|Downed|ParryWindow|Invulnerable>
State.Memory.<Index>.<FragmentStage>     // 1..7, stages: Place|Object|Sound|Interaction|Playback
Ability.Attack.<Light|Heavy|Special>.Combo<N>
Ability.Boss.<Slug>.<Phase<N>>
World.Interactable.<Type>
Canon.Rule.<RuleName>                    // e.g. Canon.Rule.NoSnakeEnemies.Ch04
UI.Screen.<Name>
Audio.Mix.<Combat|Exploration|Memory|Cinematic>
```

**Prohibition:** no agent introduces a tag namespace. New tags are proposed to the tag owner (Core, Agent 3)
and land in `DefaultGameplayTags.ini` with a comment naming the requiring feature.

### 6.7 World & chapter contract (Agent 2)

| Interface | Contract |
|---|---|
| `ATDDChapterDirector` | One per persistent chapter level. Exposes `ChapterId`, `ActivateScene(FName SceneId)`, `DeactivateScene`, `OnChapterStateChanged` |
| `ITDDInteractable` | `bool CanInteract(ATDDCharacter*) const`, `FTDDInteractionPrompt GetPrompt() const`, `void Interact(ATDDCharacter*)`. **No UI code inside interactables** |
| `UTDDMemoryDirector` | Owns the seven-memory state machine (§9.3). **Only** authority allowed to grant memory progress. Listens to fragment events from interactables and audio cue completion |
| `ATDDEncounterVolume` | Spawns/arms encounters; reports begin/end to `UTDDCombatDirector`; bosses use phase graphs (§8.3) |
| Streaming | Chapters expose `FTDDStreamingBudget` (cell size, memory ceiling, expected resident actors). Exceeding it is a test failure, not a warning |

### 6.8 Progression, save, UI contract (Agent 3)

| Interface | Contract |
|---|---|
| `UTDDCampaignSubsystem` | Owns chapter unlock state, ending eligibility, "all seven memories" predicate |
| `UTDDMemoryLedger` | Insert-only record of memory fragment discovery, keyed by `(MemoryIndex, FragmentStage)` with content hash |
| `UTDDSaveGame` | Versioned, explicit fields, no raw UPROPERTY dumps of actor state; see §9.6 |
| `UTDDHudViewModel` | UI never reaches into gameplay objects; gameplay pushes view-models |
| `UTDDTelemetrySubsystem` | Local, privacy-safe event log used for tuning and for *evidence* (§13.5) |

### 6.9 Interface change protocol

1. Propose in a PR touching only `Docs/interfaces/`, with the affected agents named.
2. Two-agent sign-off (the owner + every consumer).
3. Land the interface + a `STUB` implementation before any consumer depends on behaviour.
4. Breaking change ⇒ save-version bump or migration function, listed in `Docs/SAVE_MIGRATIONS.md`.

---

## 7. Character and combat architecture (detail)

### 7.1 Adanna's movement model

| Parameter | Target | Notes |
|---|---|---|
| Capsule | 42 cm radius, 90 cm half-height (≈1.78 m visual) | 7.5 heads visual scale; matched to art |
| Walk / Jog / Sprint | 1.6 / 3.4 / 6.2 m/s | Sprint is traversal, not combat |
| Strafe | 2.6 m/s, rotation locked to camera | Core of the GoW-like feel |
| Acceleration | 1400 (ground), 380 (air) | Tunable Data Asset |
| Turn rate | 540°/s combat, 720°/s exploration | With motion-matched turns evaluated |
| Dodge | 5.5 m, 0.42 s, i-frames 0.06–0.28 s | Directional, stamina-costed |
| Stamina | 100, regen 22/s after 0.8 s delay; attack 18–28 | Prevents infinite aggression without slowing exploration |
| Root motion | Attacks/cinematics; **locomotion never root-motion driven** | Mixed mode caused most of the "sliding feet" bug class in reference projects |

### 7.2 Custom movement component

`UTDDCharacterMovementComponent : UCharacterMovementComponent`. Adds: slide, ledge probe, traversable-surface
tags (laterite/rock/wood/mud change footstep + speed slightly), and a *hard* separation of "camera-relative
strafe" vs. "movement-vector" modes so combat and exploration do not fight.

### 7.3 Camera

Spring-arm orbit with:
- **Combat framing**: over-the-shoulder, target-lock optional, shoulder swap, FOV 78→68 on lock.
- **Exploration framing**: wider, slower recentre, soft auto-follow with deadzone.
- **Collision**: sphere-cast probe with falloff; never snap. Chapter interiors (Ch06 memory rooms) need
  tighter minimum arm length.
- **Boss framing**: per-boss `FTDDCameraProfile` Data Asset (Amadioha at ~5 m requires a different vertical
  offset and pitch limit than the Hollow King at ~2.6 m).

### 7.4 Encounter and boss architecture

See §8.3. Combat's responsibility in a boss fight is the *player half*: lock-on profiles, damage feedback,
poise reads, and the `OnBossPhaseChanged` hook for UI/audio. Boss *logic* is Agent 2's phase graph.

### 7.5 Weapon handling

One weapon at Stage 3 — `TDDWeapon_ShortIronSword` — with a `FTDDWeaponDefinition` Data Asset: mesh, socket
(hand_r), sheathe socket (left hip — canon), damage profile, trail VFX, swing MetaSounds. Multiple weapon slots
are **out of scope** until the Creative Director approves a second weapon in the weapon register (register does
not currently contain one).

---

## 8. World, environment, AI and NPC architecture

### 8.1 Chapter structure

Eight chapters, each:

```
/Game/Chapters/CH04_RiverOfIdemili/
├── L_CH04_Persistent         (World Partition; chapter director; streaming sources)
├── Scenes/                   (per CH04-* scene: sublevel or data layer)
├── Memory/                   (CH04 memory: M04 sublevel + Sequencer asset — separate from discovery site)
├── Boss/                     (the deep pool arena, phase graph asset)
└── Audio/                    (chapter mix + ambience MetaSounds)
```

Canon note (memories doc): a memory "is found where a place echoes it; it did not necessarily happen there."
Therefore **memory playback sublevel ≠ discovery location**, by architecture.

### 8.2 Enemy AI

- `ATDDEnemyBase` + `UStateTreeComponent`. States: `Idle, Patrol, Alert, Chase, Attack, Recover, Flank, Flee,
  Staggered, Dead`.
- Perception: sight + hearing (AIPerception). Sound events come from the audio system via a documented
  `UTDDSoundEventSubsystem` — **AI must not guess from animation length.**
- Archetypes for Stage 5 (proposed, needs CD ratification): `Thrall` (slow, Ch03/Ch07), `Rootwarden`
  (Ch01 bruiser), `AshHound` (fast flanker), `Maskbearer` (Ch06, uses reflections — see canon: nothing monstrous),
  `Ore-Slave` (Ch02, cold kingdom), `Thunder-Champion` (Ch05 elite).
- Canon guardrails as *tests*: no snake-type enemy can exist in Ch04 spawn tables; no enemy in Ch06 may use a
  real masquerade visual (asset validation).

### 8.3 Boss architecture — declarative phase graph

Each boss is a `UTDDBossPhaseGraph` Data Asset: ordered phases, transition conditions (poise break, health %,
time, player distance, memory-discovered flag), arena state changes, camera profile, music state. Code
(`UTDDBossController`) executes the graph; it contains no boss-specific branching.

Established boss list (from directive; **ESTABLISHED** as encounters per OAD-21):

| Ch | Location | Boss |
|---|---|---|
| 1 | Forbidden Forest | Great Root Mother |
| 2 | Kingdom Beneath the Earth | Iron Elephant |
| 3 | City of the Living Dead | King Without a Face |
| 4 | River of Idemili | Daughter of the Deep |
| 5 | Mountain of Thunder | Amadioha's Champion |
| 6 | Kingdom of Masks | Mother of Masks |
| 7 | Gates of the Dead | Hollow King |
| 8 | Last Daughter / Ancestral Realm | Ezeani (three endings) |

**Arena design is PROPOSED until reviewed** (OAD-21). Engineering therefore builds *one* boss (Stage 5) —
the Great Root Mother — on the final architecture, and proves the graph can express a second (Iron Elephant)
as a data-only addition. That data-only proof is the acceptance test for the boss architecture.

### 8.4 NPC behaviour and world simulation

- **Named cast** (12 + supporting) are bespoke actors with dialogue and (where canon) scripted presence.
- **Crowds** use Mass + StateTree for settlement ambience (farms, market, fishing, wells). Crowd NPCs are
  **non-interactive by canon default** unless a specific quest opts in.
- Clothing variety (OAD-55/56) comes from a **garment-variant set** — constructed torso garments in varied cuts,
  not colour-swaps of one mesh. Validation test rejects bare-chested/one-shoulder defaults.
- Children NPCs exist (canon references them) and must be handled with care: no harm states, no combat targeting.

### 8.5 Streaming and traversal

World Partition with per-chapter cell sizing; streaming sources on the player and on "vista" volumes.
Traversal gating uses Gameplay Tags + chapter unlocks. Fast travel is **not** canon-approved; not built.

### 8.6 Environmental interaction

`ITDDInteractable` implementations: offerings, seals, bowls, cloth strips, doorways, levers. Interaction is
*hold-to-commit* for meaningful actions (memory fragments) and *tap* for trivial ones. Prompts are
view-model driven and localised-ready.

### 8.7 Cinematics

Sequencer, with a strict contract: a cinematic asset declares `FTDDCinematicRequest { FName SceneId; FGameplayTag
Mode; bool bSkippable; FName CompletionEvent; }`. Cinematics never own game state; they emit events the
campaign subsystem consumes. Memory scenes are Sequencer sublevels driven by `UTDDMemoryDirector`.

---

## 9. Animation, progression and narrative architecture

### 9.1 Animation architecture

| Layer | Responsibility | Owner |
|---|---|---|
| Locomotion ABP | Strafe/jog/sprint blend, turn-in-place, landing | A1 |
| Combat ABP layer | Upper-body montage slots, weapon layers, hit reactions | A1 |
| IK layer | Foot placement on uneven laterite; hand-on-prop for interactions | A1 (Control Rig) |
| Additive layer | Breathing, fatigue, memory-echo overlay for Ch06 | A1 |
| Facial | Expressions where cinematics demand; MetaHuman or custom — **undecided**, D-09 | A1/A3 |

Target: **motion-matched locomotion if D-07 approves**, else a tuned blend-space with turn-in-place. Either
way the ABP's public surface (`FTDDLocomotionState` + delegates) is identical, so other systems are unaffected
by that decision.

### 9.2 Campaign graph

`UTDDCampaignGraph` Data Asset: nodes = chapter objectives; edges = predicates (boss defeated, memory found,
scene completed). Linear spine with side exploratory objectives. Ending eligibility is a query, not a branch
buried in a level Blueprint.

### 9.3 The seven-memory director (highest canon risk — design carefully)

```
Stage 0  UNDISCOVERED     nothing in world
Stage 1  PLACE            player is inside the discovery location; ambience shifts
Stage 2  OBJECT           the specific object is found/highlighted
Stage 3  SOUND            the recorded cue plays (audio-first, per OAD-32)
Stage 4  INTERACTION      player performs the canon interaction (e.g. "retie the cloth")
Stage 5  PLAYBACK         memory sublevel + Sequencer plays; grants memory index
Stage 6  COMMITTED        ledger written; save flagged; Ending-3 counter incremented
```

Invariants enforced by tests:
- Stages are strictly ordered; no skipping (each stage has an explicit `CanAdvance` predicate).
- A memory cannot be granted twice; re-entering after COMMITTED plays a short "echo" only.
- Missing any memory leaves Ending 3 ineligible *and* the campaign graph must report **which** are missing
  (canon: "missing one closes Ending 3 only").
- The memory's content hash is stored with completion.
- Memory 7's discovery must be reachable only after memories 5 and 6? — **No.** Canon says all seven are needed,
  not that discovery is gated. Do not invent gating. (Flagged to CD as D-04.)

Canon fragment table (from the memories doc) becomes `DT_MemoryFragments` — one row per memory, listing the
four discovery fragments as `FGameplayTag` cues (`Fragment.Place.WaysideOffering` etc.).

### 9.4 Story delivery

Dialogue via DataTable + MetaSound; no dialogue in level Blueprints. Codex entries carry
`bFictionalMythology = true` where applicable, satisfying the directive's cultural-honesty rule at the data layer.

### 9.5 Inventory and equipment — deliberately minimal

Canon gives Adanna **one weapon** and defined costume states (initial, exploration, primary combat armour,
upgraded, battle-worn, MMUO manifestation). Therefore:

- **IN SCOPE:** weapon stats (single blade), armour state swap (cosmetic + stats), consumables if approved.
- **OUT OF SCOPE:** loot systems, rarity tiers, second weapon, crafting. Any of these requires
  Creative Director approval and entry in the Art Bible registers first.

This is a *canon-driven* scoping decision, not a shortcut.

### 9.6 Persistence

`UTDDSaveGame` v1 fields (explicit, versioned):

```
Header: SaveVersion(int32), ContentHash(FString), BuildId(FString), TimestampUtc
Campaign: ChapterUnlocked, ObjectiveStates[], EndingEligibility{1,2,3}, EndingCompleted
Memories: Ledger[]  — records of { MemoryIndex, Stage, ContentHash, UtcTime }
Character: Transform, VitalsSnapshot, ArmourState, WeaponState
World: DiscoveredLocations[], OpenedShortcuts[], BossDefeated[]
Settings: separate UGameUserSettings + a small TDD settings object
```

Rules: no serialising actor pointers; no serialising Blueprint object graph; forward migration function per
version; corrupt-save detection by content hash, and a **safe fallback to chapter start** (never to "new game"
silently — that is data loss).

### 9.7 Audio architecture

Audio is load-bearing for this game: the memories are audio-first, and the score carries the ancestral register.

- Submix hierarchy: `Master → Music / SFX / Ambience / Voice / UI / CinematicDuck`.
- `UTDDMusicDirector` drives states: `Exploration.<Chapter>`, `Combat.Intensity.<0-3>`, `Boss.<Slug>.<Phase>`,
  `Memory.<Index>`, `Ending.<N>`.
- Footstep surfaces from the movement component's surface tags (§7.2) — one source of truth.
- Sound events publish to `UTDDSoundEventSubsystem` for AI hearing (§8.2).

### 9.8 Rendering the canon-specific art problems

These are real technical requirements, not polish:

| Canon requirement | Technical approach | Owner |
|---|---|---|
| Okwu's hood is darkness only, in every light, always (OAD-12) | Unlit custom material with depth-write, GI-independent; excluded from Lumen gather; validated under 3 lighting rigs | A1+A3 |
| Nneka manifests with soft edges, cool moonlit skin, drifting chalk dust; **never glows** | Layered translucent material + Niagara chalk particles; explicit "no emissive" test | A1 |
| Ch07 ember red only deep in cracks, **never flame** | Material-based emissive in crack masks; no fire Niagara assets permitted in the chapter pool | A2+A3 |
| Ch05 lightning is white only | VFX pool restriction + validation | A2 |
| Ch03 ash "must not read as snow" | Material response tuning; snow/ash differentiation test on 3 lighting setups | A2+A3 |
| Ch01 Great Root Mother tree visible from every major clearing | Vista composition + per-scene visibility automation test | A2 |
| Ch06 mirrors are still water / polished metal, no glass | Asset validation list; reflection method choice per scene | A2 |

---

## 10. Content, asset and repository policy

**This must be decided before content production, not during.**

### 10.1 The problem

Git holds text well. `.uasset`, `.umap`, MetaHuman data, WAV/`.bnk`, video, USD and texture sources are binary,
large, and non-mergeable. Eight chapters of production content will be tens to hundreds of gigabytes. This
repository has **no LFS** configured and is hosted where large binaries will make clones unusable and
eventually fail.

### 10.2 Proposed split (needs Creative Director / infra decision — D-01)

| Class | Location | In Git? |
|---|---|---|
| Source code, config, docs, tools, tests, small data (`.json`, `.csv`) | This repo | **Yes** |
| Generated documentation, evidence reports, canon index | This repo | **Yes** |
| `.uproject`, `.Build.cs`, `.Target.cs`, ini | This repo | **Yes** (text) |
| Game logic Data Assets where authored as text (CSV→import) | This repo | Yes, as CSV source of truth |
| Binary `.uasset`/`.umap`, MetaHuman, audio, video, textures, USD | **Git LFS, or Perforce/Drive-sync/Epic DVCS** | **No** — must be decided |
| Engine install, DerivedDataBinaries, Intermediate, Saved | Ignored | No |

### 10.3 Minimum controls landed now

- `.gitignore` for UE (Binaries, Intermediate, Saved, DerivedDataCache, *.sln, .vs).
- `.gitattributes` marking UE binaries as `-merge -diff` **and** `filter=lfs` commented-ready, so enabling LFS
  is a one-line change rather than a history rewrite.
- Hard rule: **no file > 5 MB** in Git without an ADR exception.
- Where content must be referenced before the store exists, commit **CSV/JSON definitions** describing content
  (e.g. `Content/SourceData/Bosses/CH01_GreatRootMother.csv`) so engineering can proceed and designers have a
  reviewable, diffable source.

### 10.4 Content ownership boundary

| Content | Owner | Review gate |
|---|---|---|
| Hero characters (Adanna, Ezeani, Nneka, Okwu, Amadioha, Idemili, Hollow King) | Visual team → integration A1 | Identity-lock validation + art approval + cultural review where flagged |
| Environments per chapter | Visual team → integration A2 | Canon rule validation (§3.2) + legend of approval states |
| Animations | A1 (integration) / animation vendor | Montage naming + root-motion validation |
| Audio | A2 (integration) | MetaSound graph + mix compliance |
| UI | A3 | CommonUI view-model compliance |

---

## 11. Testing strategy

### 11.1 Test layers

| Layer | Tool | Runs where | Gates |
|---|---|---|---|
| **L0 Canon/data** | Python `unittest` in `Tools/canon/tests` | Sandbox + CI | Every push |
| **L1 Unit (C++)** | UE Automation (`IMPLEMENT_SIMPLE_AUTOMATION_TEST`) | Headless nullrhi editor | Every push with editor machine |
| **L2 Integration** | UE Automation `EAutomationTestFlags::ApplicationContextMask` + functional test maps | Editor | Per merge to integration branch |
| **L3 Play-in-editor smoke** | Automation driven map + `GameplayDebugger` assertions | Editor w/ GPU | Daily |
| **L4 Performance** | Unreal Insights + `stat` capture scripts against budgets (§14) | Editor/standalone | Stage gates |
| **L5 Manual/experiential** | Recorded session + design checklist | Human | Milestone gates |

### 11.2 What must be automated (non-negotiable list)

1. Canon ID validity: every `LocationId` in data exists in `canon_index.json`.
2. Canon rule enforcement: per-chapter exclusion lists (pythons, flames, remains, masks) validated against
   chapter asset/spawn manifests.
3. Memory director invariants (§9.3) — order, no double grant, hash stability, ending-3 predicate.
4. Save/load round-trip + migration from v1→v2 fixture + corrupt-save fallback.
5. Combat hit arbitration determinism (fixed frame, seeded).
6. Adanna identity invariants: single weapon slot used, no mirrored mesh, side-specific sockets present.
7. Streaming budget per chapter (resident memory, actor count).
8. Boss phase graph reachability: every phase reachable, no dead-end phase, all transitions terminating.
9. UI view-model: no gameplay object references leaking into widget tree (reflection check).
10. Build smoke: packaged build launches, reaches main menu, enters Ch01 sandbox (Stage 1 onward).

### 11.3 Evidence format

`Docs/evidence/<milestone>/<test-name>.json` + a human summary `.md`:

```json
{ "test": "TDD.Memory.Director.SecondGrantRejected", "engine": "5.8.0", "buildId": "…",
  "dateUtc": "…", "result": "PASS", "durationMs": 42, "logs": "…", "assertions": 7 }
```

Manual evidence: written observation, what was tried, what failed, video link (Drive), and the tester's name/role.

### 11.4 What this sandbox can verify

Only **L0** plus static review of C++/config. Everything else must be verified on an engine machine. Any report
that conflates the two is a process failure.

---

## 12. Agent ownership and interfaces

### 12.1 Ownership matrix

| Domain | Owner | Consumers | Handoff artefact |
|---|---|---|---|
| Core framework, ID types, tags, GameMode/State | **A3** (integration) | all | `Framework/*.h` + tag registry |
| Character movement, camera, input | **A1** | A2 (AI targets), A3 (UI) | `FTDDLocomotionState`, delegates |
| Combat abilities, damage, hit arbitration, weapon | **A1** | A2 (enemies), A3 (HUD) | combat types (§6.4) |
| Animation bridge, IK, montages | **A1** | A2 (AI anim), A3 (UI cues) | montage naming spec |
| Enemy AI, perception, boss phase graphs | **A2** | A1 (damage), A3 (UI/telemetry) | `UTDDBossPhaseGraph` schema |
| Chapters, streaming, interactables, memory director | **A2** | A3 (save), A1 (traversal gating) | `ITDDInteractable`, memory events |
| NPC/crowd simulation | **A2** | A3 (telemetry) | crowd budget profile |
| Audio, music director | **A2** | A1 (footsteps), A3 (mix UI) | sound event registry |
| Progression, campaign graph, memory ledger | **A3** | A2 (scene activation) | campaign graph schema |
| Save/load, settings | **A3** | all | save schema + migration doc |
| UI/HUD/menus/codex | **A3** | — | view-model contracts |
| Telemetry, evidence tooling, CI, build, packaging, perf | **A3** | all | CI config, perf reports |
| Canon validators | **A3** (tooling) with **A2** (content rules input) | all | `Tools/canon/*` |

### 12.2 Prohibitions

- No agent implements a second version of another agent's owned system "temporarily". A stub goes in the
  owner's module with the owner's signature.
- No agent edits another agent's `.cpp`. Cross-cutting needs go through the interface file and a PR note.
- No agent changes an ID type, tag namespace, or save field without §6.9.
- No agent adds a plugin or third-party dependency without an ADR.

### 12.3 Reporting

Each agent reports per task: **what was asked, what was done, what was tested, what was not, tags used (§0),
evidence links, new risks, interface changes**. Reports are reviewed by the Technical Director; unsupported
claims are sent back.

---

## 13. Performance targets and risks

### 13.1 Budgets (PC, current-gen-class, 1440p, "High" preset)

| Metric | Target | Ceiling | Notes |
|---|---|---|---|
| Frame time (GPU) | ≤ 16.6 ms | 20 ms | Lumen HQ; Lite path must hold 60 fps |
| Frame time (game thread) | ≤ 8 ms | 11 ms | Streaming + AI included |
| Draw/submit | ≤ 4,000 | 6,000 | Nanite reduces, MegaLights raises light cost |
| Resident texture | ≤ 5.5 GB | 7 GB | Per-chapter streaming setup required |
| Total process memory | ≤ 9 GB | 12 GB | |
| PSO hitches in first 5 min | 0 stutter > 100 ms | ≤ 2 | 5.8 precaching + our own collection |
| Chapter load (stream-in) | ≤ 8 s | 15 s | |
| Boss arena frame time | ≤ 16.6 ms | 20 ms | Boss + player + VFX heavy |
| Crowd (settlement) NPC count | 40 visible @ 60 fps | 80 | Mass; no hero anim budget |

### 13.2 Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R-01 | **No engine in the current sandbox** ⇒ code cannot be compiled here | Certain | High | Explicit evidence requirement; CI on engine machine at Stage 1; no "works" claims from sandbox | A3 |
| R-02 | Binary content overwhelms Git | High | High | §10 policy + ADR-0004 decision now | A3 |
| R-03 | Three agents duplicate systems | Medium | High | §12 ownership + §6.9 protocol + interface-first PRs | A3 |
| R-04 | Canon IDs drift from Drive registers | Medium | High | `canon_index.json` + L0 validator in CI; register owner notified on mismatch | A3 |
| R-05 | Cultural review gates arrive late (deity depictions, mask concepts, shrine/oath ground boards) | Medium | Very High | Gate every pre-shippable asset on `CanonApproved`; do not build shippable art for unapproved concepts; flag in art register | CD + A2 |
| R-06 | MetaHuman pipeline imposes likeness/quality constraints on West African features and Adanna's specific locks | Medium | Medium | D-09; evaluate on one head before committing; keep custom-rig fallback | A1 |
| R-07 | Lumen/MegaLights cost with dense foliage + rain + many small lights | High | Medium | Lumen Lite tier from day one; Nanite Foliage evaluation; per-chapter budget tests | A3 |
| R-08 | Motion matching cost/quality for strafe combat | Medium | Medium | D-07 decision at Stage 4; locomotion contract insulated | A1 |
| R-09 | Scope: 8 chapters + 7 memories + 3 endings with 3 agents is a multi-year programme | High | High | Stage gates; one chapter vertical slice first; explicit "not in scope" lists; no feature creep without CD approval | TD |
| R-10 | Solo-player save corruption destroys trust | Low | High | Hash + fallback + migration tests; versioned schema | A3 |
| R-11 | Boss arena designs are PROPOSED (OAD-21) — building detailed arenas early wastes work | High | Medium | Build Phase graphs as data; arena layouts stay blockout until reviewed | A2 |
| R-12 | Engine 5.9/UE6 transition mid-production | Medium | Medium | Stay on 5.8; plugin/API hygiene (no deprecated APIs); migrate only with an ADR late in polish | A3 |

### 13.3 Canon validation as automated tests

Implemented in `Tools/canon/` (Python, stdlib only) and mirrored as UE editor automation once an engine exists:

- `test_ids.py` — every referenced ID resolves; no duplicates; chapter prefixes match.
- `test_rules.py` — per-chapter canonical exclusion rules (§3.2).
- `test_register_status.py` — no asset is `Shippable` while its canon status is `Proposed`.
- `test_memory_sequence.py` — 7 memories, one per chapter 1–7, ordered, unique scene/location IDs.

### 13.4 Mock ledger

| Mock | Stands in for | Lives | Exits when |
|---|---|---|---|
| `UTDDMockAudioCueComponent` | Memory sound fragments | Test maps only | Real MetaSounds exist |
| `ATDDMockBoss` | Phase graph execution targets | Test maps | Real bosses at Stage 5 |
| `UTDDTestPawn` | Adanna (for AI tests) | Test maps | Character stabilised |
| `UTDDDummySaveProvider` | Filesystem save | Unit tests | — (permanent, test-only) |

Mocks never ship in `Content/` production folders and are named `*Mock*` or `*Test*` by rule.

---

## 14. Development phases, dependencies and gates

Stage order is mandated by the directive. Each gate requires evidence and TD review.

| Stage | Name | Scope (this document's reading) | Depends on | Gate evidence |
|---|---|---|---|---|
| **0** | Architecture & technical foundation | This document set; repo hygiene; canon index + validators; module skeleton; tag registry; `.gitignore` policy; ADRs | — | Docs ratified; L0 tests green |
| **1** | Project & build foundation | `.uproject`, modules, target files, ini baseline, CI smoke build, save schema v1, evidence harness | 0 | Headless build + empty map boots; L1 test harness runs |
| **2** | Movement & character laboratory | CMC subclass, Enhanced Input, orbit camera, locomotion states, traversal (vault/ledge), test gym map | 1 | Automation: movement specs; manual video; perf of gym |
| **3** | Combat foundation | Hit arbitration, abilities, weapon, dodge/block/parry, one enemy dummy, damage feedback, audio hooks | 2 | Determinism test; combat gym video; tuning sheet |
| **4** | Character behaviour & animation | Locomotion ABP (or motion matching), combat layers, IK, hit reactions, facial/cinematic hooks | 3 | Anim contract tests; foot-slide metric; adanna invariants |
| **5** | Enemy & boss architecture | StateTree enemies (2 archetypes), perception, phase graph + 1 boss (Great Root Mother), second boss by data-only proof | 3, 4 | Phase graph reachability; boss fight video; perf capture |
| **6** | World simulation, exploration & traversal | Chapter 1 (Forbidden Forest) integration: streaming, vistas, interactables, memory fragments 1, NPC/crowd baseline, canon rule tests | 5 | Ch01 playable end-to-end incl. memory 1; streaming budget test |
| **7** | Progression & narrative systems | Campaign graph, memory ledger + all 7 definitions, endings eligibility, save/load, codex, cinematics glue, audio states | 6 | Save round-trip + migration; ending predicate tests; memory invariants |
| **8** | Campaign & chapter production | Chapters 2–8 production, bosses, environment canon compliance, cutscenes, audio | 7 | Per-chapter acceptance matrix |
| **9** | Polish, optimisation, testing, release prep | Performance passes, LOD/streaming tuning, packaging, platform cert readiness, final test sweep | 8 | Perf report vs budget; packaging smoke; regression suite green |

**The vertical slice** = Stages 2–7 restricted to Chapter 1 + memory 1 + Ending-3 eligibility plumbing.
That is the first genuinely playable, canon-correct slice of the game, and it is the project's first
demonstrable milestone. It is deliberately *not* "a boss arena demo".

**Explicit non-goals until after Stage 7:** multiplayer/co-op, free-climb, fast travel, weapon variety,
crafting, seasonal content, console certification, localisation beyond string-table readiness.

---

## 15. Build, packaging and release readiness

| Item | Stage | Notes |
|---|---|---|
| `.uproject` + module targets | 1 | Committed as text |
| Build script (`Tools/ci/build.sh`) wrapping UAT | 1 | Windows-first; must run headless |
| Automation runner script | 1 | `-ExecCmds="Automation RunTests TDD;Quit"` + report parsing |
| Cooked Development build (Win64) | 1 (smoke), 8 (real) | Evidence attached |
| Packaging config + shipping map list | 8 | |
| Crash reporter / logs policy | 7 | Local logs, privacy-safe |
| Credits + fictionality statement (mythology disclaimer) | 7 | Canon-required |
| Console cert | 9 / post-launch | Unavailable here |

---

## 16. Open decisions requiring the Creative Director or Technical Director

Engineering cannot resolve these without inventing canon or infrastructure. Each is tracked with an ID.

| ID | Question | Blocks | Recommendation |
|---|---|---|---|
| **D-01** | Binary asset storage: Git LFS vs Perforce/Drive/Epic DVCS? | All content production from Stage 6 | LFS for small binaries + external store for hero content; decide at Stage 1 |
| **D-02** | Target platforms and min-spec (PC only? console?) | Perf budgets, renderer tiering | PC-first, current-gen console later |
| **D-03** | Chapter scope for first shippable release: 8 chapters, or a shorter canon-complete arc first? | Whole schedule | Vertical slice (Ch01) then chapter-by-chapter; do not commit dates before Stage 5 evidence |
| **D-04** | Are memory discoveries order-gated, or free-order within chapters 1–7? Canon only requires all seven. | Memory director design | Free-order within chapter; ordered by chapter progression. **Needs CD confirmation** |
| **D-05** | Ending 2/3 environmental and cinematic content (OAD-23: still to be defined) | Ch08 production | Provide treatment before Ch08 art lock |
| **D-06** | Chapter 8 Ancestral Realm final design (OAD-30 direction resolved; design NOT approved) | Ch08 environment build | Keep blockout; no hero art |
| **D-07** | Motion Matching vs. tuned blend-space for locomotion | Stage 4 | Evaluate with a 2-week spike on strafe combat |
| **D-08** | Combat archetype list (enemy types) — no canon source exists | Stage 5 | CD review of proposed archetypes (§8.2) before asset work |
| **D-09** | MetaHuman pipeline for hero faces? | Stage 4, casting/likeness | Spike one head; confirm likeness policy |
| **D-10** | Cultural review cadence and named consultant | R-05, any shippable deity/mask/shrine art | Appoint before Stage 6 |
| **D-11** | Save-slot count, autosave cadence, accessibility requirements | Stage 7 | Propose 3 slots + autosave at chapter/scene boundaries; accessibility is not optional (subtitles, remap, colour-blind, motion) |
| **D-12** | Difficulty model (single, or story/action tiers) | Combat tuning | Propose two tiers; no canon conflict |

---

## 17. What already exists / needs modification / must be built / remains undecided

| Category | Items |
|---|---|
| **Already exists** | Creative canon in Drive (characters, environments, 59 OADs, 7 memories, timeline); canonical ID scheme; this architecture document set; repo scaffolding; canon index + validators (L0). |
| **Needs modification** | Nothing in code (there is none). In *process*: the Drive registers need canonical ID coverage for **boss encounters** and **memory scenes** to be engineering-consumable; `13_GAMEPLAY_AND_LEVEL_DESIGN` must be populated with ratified gameplay specs (currently empty). |
| **Must be built** | Engine project + modules; every system in §6–§9; CI + evidence harness; content pipeline per §10; Chapter 1 vertical slice; then Chapters 2–8. |
| **Remains undecided** | D-01 … D-12 (§16), plus all eight ending treatments, Chapter 8 design, and enemy archetype canon. |

---

## 18. Immediate next actions (Stage 0 → Stage 1)

Ordered, with owners and evidence:

1. **A3** — Land repo hygiene: `.gitignore`, `.gitattributes`, `README` rewrite, module skeleton (empty but
   valid), `DefaultGameplayTags.ini` registry. *Evidence:* files + L0 green.
2. **A3** — Canon index (`Tools/canon/data/canon_index.json`) + four validators + CI hook. *Evidence:* L0 test run.
3. **A1/A2/A3** — Ratify interfaces (§6.2, §6.6, §6.7, §6.8) in `Docs/interfaces/`; sign-off.
4. **TD/CD** — Resolve D-01, D-02, D-04, D-10 (highest blocking value).
5. **A3** — Stage 1 build foundation: `.uproject`, `Build.cs`/`Target.cs`, ini baseline, headless build + automation
   runner, first smoke evidence on an engine machine.
6. **A1** — Stage 2 begins only after Stage 1's smoke build evidence exists.

---

## Appendix A — Verification log for this document

| Claim in this document | How verified |
|---|---|
| Repo contains one file | `git ls-tree -r main`, `find` |
| No engine in sandbox | `which UnrealEditor`, `ls /opt` |
| Art Bible contents and OAD numbering | Read Drive `CHARACTER_DESIGN_REGISTER.md`, `OPEN_ART_DECISIONS.md`, `NNEKA_MEMORIES_AND_TIMELINE.md`, `ENVIRONMENT_DESIGN_REGISTER.md` 2026-11-16 |
| `13_GAMEPLAY_AND_LEVEL_DESIGN` is empty | Drive `list_files` on folder ID `1APIsaxdUb9WtXZIXst8bI0E3r_LoNSai` → 0 files |
| Memory scene/location IDs | Read `NNEKA_MEMORIES_AND_TIMELINE.md` table §1 |
| Chapter 8 approved locations | `OPEN_ART_DECISIONS.md` OAD-45 |
| UE 5.8 is the last planned UE5 major | Epic, State of Unreal 2026 release notes (public) |

## Appendix B — Documents in this architecture set

| Doc | Purpose |
|---|---|
| `00_MASTER_ENGINEERING_ARCHITECTURE.md` | This document — binding architecture |
| `adr/ADR-0001…0008_*.md` | Decision records |
| `CANON_INDEX.md` | Engineering mirror of canon IDs + status, and how it is validated |
| `REGISTER_INGESTION.md` | Source versions, parsing assumptions, unsupported table formats, validation failures, regeneration procedure |
| `REGISTER_TRACEABILITY.md` | Register→world mapping; the two status axes; per-row verification results; the six counts discriminated |
| `WORLD_ASSESSMENT.md` | Repo state, register findings, missing systems, staged plan |
| `WORLD_ARCHITECTURE.md` | Runtime world components (all SPEC), streaming, five-tier population, interfaces |
| `POPULATION_SENSITIVITY_REPORT.md` | How the Ch1 population estimate moves when policy assumptions vary; facts vs assumptions; the rounding correction |
| `ENEMY_ARCHETYPE_REVIEW.md` | Six PROPOSED archetypes for CD-3; risk ranked by cultural exposure |
| `DEPENDENCY_AND_BLOCKER_REGISTER.md` | CD-5/CD-3/CD-2 outcomes, 12 blockers, cross-agent needs, honest capability table |
| `AGENT1_TRAVERSAL_CONTRACT_REQUEST.md` | Request only — provisional ids, no frozen enum |
| `interfaces/` | Frozen cross-agent interfaces (tagged by version) |
| `production/STAGE_GATES.md` | Gate checklist and evidence requirements |
| `production/RACI.md` | Who owns/approves what, including review gates |
| `evidence/` | Test outputs and manual verification records |
