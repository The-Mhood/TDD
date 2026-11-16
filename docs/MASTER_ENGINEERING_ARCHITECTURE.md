# THE DISOBEDIENT DAUGHTER — Master Engineering Architecture

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Document:** Master Engineering Architecture (initial baseline)
**Status:** Proposed technical baseline; not an implementation report
**Prepared:** 2026-11-16
**Repository baseline:** `arena/c64fc525-tdd`, based on `5e3d1da4eee42ad8255760530291ff91cdfb39b2`

> This document is the first required engineering deliverable. It records what was actually inspected, proposes a deliberately conservative UE5 architecture, and marks decisions that still require confirmation. It does not claim a playable game, a configured Unreal project, or tested engine functionality exists.

## 1. Current project assessment and executive summary

### Verified repository state

At the inspected baseline, the repository contains only a six-byte `README.md` (`# TDD`). The tracked tree contains no `.uproject`, `Config/`, C++ source, `Source/`, `Content/`, maps, plugins, automated tests, assets, build scripts, or dependency declarations. Git history contains only the initial commit. No Unreal Editor or UnrealBuildTool executable is available in this workspace. Consequently, the engine version, target platforms, rendering configuration, plugin set, asset inventory, current game functionality, build health, and performance baseline **cannot be verified here**.

**Current status:** architecture/planning only. There is no engine project in this checkout to build, launch, or test. This assessment describes this repository and workspace, not any separate project that may exist elsewhere.

### Verified creative and production constraints

The user-provided directive is the source for the campaign facts in this document: Adanna is 25; the eight chapter identities, seven hidden memories, and three endings must be preserved. No story events, dialogue, weapon identity, visual design, or folklore claims are invented here.

The Google Drive production art bible is accessible and remains the visual authority. The versioned `ART_BIBLE_MASTER_INDEX_BATCH4W_2026-11-16.md` (updated 2026-11-16) says the original sync-13 index is preserved; it distinguishes approved designs from exploratory work and states that environment-design approval is not narrative-canon approval. Its listed approved designs include the Adanna and Amadioha references and specific Chapter 8 environment boards; each asset's current status must be checked in the index rather than inferred from a thumbnail or an older board. A Chapter 8 character composition listed as exploratory is explicitly not a character-design approval. The accompanying `DECISIONS.md` establishes the Memory 7 direction and Adanna's age when Nneka died as six, and requires detailed memory sequence/dialogue/events to be reviewed before they are locked. These sources were consulted read-only:

- [Production Art Bible archive](https://drive.google.com/drive/folders/1lzJBgHHSO2OJMB0LFmwQoU6R7Kv2iGlZ)
- [Versioned Master Art Bible Index (2026-11-16)](https://drive.google.com/file/d/1ntf2gnwyZf-t0J2zreugsg4E58vWVMdJ/view)
- [Creative decisions: Memory 7, age, Chapter 8 boards](https://drive.google.com/file/d/1kMDn5oXmy6DhBJsROJ6EIn_ZXUPbLENx/view)

The index—not this engineering document—governs per-asset visual status. The Creative Director and visual production team retain approval authority. Cultural references require careful research and consultant review; invented mythology must not be represented as authentic Igbo tradition.

## 2. Status vocabulary and decision discipline

- **Observed** — verified directly in the checked-out repository or cited production source.
- **Proposed** — recommended technical direction, subject to validation once the real UE project and target hardware are available.
- **Open** — must be decided or verified before the dependent production gate.
- **Creative lock** — user-provided canon or a Creative Director decision; engineering must preserve it.

No proposed technical choice below promotes a visual asset, changes canon, or authorizes story/character redesign. If an existing Unreal project is supplied later, inventory and compatibility review precede adopting or replacing any of these proposals.

## 3. Configuration and technical foundation

### 3.1 Proposed UE project shape

- Build a **source-controlled Unreal Engine 5 C++ project**, using the team's installed, licensed UE5 minor version once confirmed. Pin that exact version in the project/readme and CI/build instructions; do not guess a minor version now.
- Keep gameplay rules, state transitions, save compatibility, and reusable system contracts in C++. Use Blueprint for level assembly, authored tuning, Animation Blueprints, UI/layout, and bounded content-specific orchestration. Avoid putting core rules solely in level Blueprints.
- Start with engine-provided systems and a small number of explicit project modules. Do not add plugins, marketplace dependencies, a custom engine fork, or a framework until the inventory and a documented need justify them.
- Keep authored content data separate from runtime behavior. Use `UPrimaryDataAsset`/Data Tables only where they solve an actual authoring or lookup need; version stable IDs and validate references in editor/automation checks.
- Use Git for source/config/docs. Decide binary asset storage (Git LFS or approved external asset pipeline), access control, and generated-file ignore rules before real `.uasset`/`.umap` content is committed. Do not put derived build/cache output in source control.
- Establish editor, development, test, and shipping build configurations; a reproducible clean checkout build; map naming/ownership; and a project coding/asset naming standard in Stage 1.

### 3.2 Initial configuration inventory (not present yet)

When the actual project arrives, record and review: `.uproject` engine association; modules and targets; `Config/Default*.ini`; input mapping; default game/editor maps; collision channels and profiles; world/streaming settings; rendering scalability and RHI; platform SDKs; plugins and versions; source-control/large-file rules; asset references; packaging settings; and any existing CI/build scripts. Preserve existing behavior until the owner and impact of each item are understood.

**Unselected:** UE5 minor version, Windows/console/other platform scope, minimum hardware, online/multiplayer support, renderer and scalability baseline, source-control asset strategy, plugin list, localization requirements, and distribution/store requirements.

## 4. Proposed runtime architecture

### 4.1 Boundaries and dependency direction

Organize around a thin project runtime module and clear ownership boundaries, not a bespoke engine inside the game:

1. **Engine/framework layer** — Unreal lifecycle, input, physics, animation, navigation, audio, rendering, streaming, UI, and save APIs.
2. **Reusable gameplay layer** — player movement, combat, damage/health, interaction, enemy behavior, boss encounters, traversal, and progression components/services.
3. **Campaign/content layer** — chapter maps, encounters, quests/objectives, narrative assets, authored enemy/encounter definitions, and art-approved content.
4. **Presentation layer** — animation graphs, camera presentation, UI, cinematics, sound, VFX, and feedback, driven by gameplay state rather than owning it.
5. **Persistence layer** — versioned save DTOs and safe serialization/migration, separate from live actor pointers and presentation state.

Dependencies flow inward toward stable contracts: presentation consumes gameplay state; authored content configures systems; gameplay does not depend on a particular chapter map, cinematic shot, or visual asset. Use interfaces/events for cross-system communication where ownership differs. Avoid global mutable state and direct hard references from long-lived systems to streamed actors.

### 4.2 Unreal ownership proposal

- `GameInstance` / `UGameInstanceSubsystem`: application-lifetime services such as save-slot coordination and campaign/session flow across map changes. Subsystems do not become unbounded containers for unrelated gameplay state.
- `GameMode`: rules for the currently loaded single-player map/encounter; create the configured player pawn/controller and apply map-level rules.
- `PlayerController`: input contexts, player-facing command routing, pause/UI entry points, and camera mode requests. It sends intent; it does not implement weapon hit logic.
- `Character` plus focused components: movement/collision, combat capability, health/damage reception, interaction, and progression-facing state. Components should have one clear owner and test seam.
- `GameState` only for genuinely shared map state; `PlayerState` only if player identity/state needs that engine abstraction. Do not add multiplayer replication contracts until network scope is decided.
- Level actors/data assets: authored encounter and world setup. Streamed actors register and unregister through scoped interfaces/events; no stale actor references in saved data.

### 4.3 System interface contracts

Stable IDs are strings or project-defined namespaced identifiers, not actor pointers or mutable display labels. Public contracts below are conceptual names; final UCLASS/UINTERFACE names follow the inspected codebase.

| Contract | Owner / input | Output and rules |
|---|---|---|
| Player command | Controller → pawn/components | Move/look/jump/evade/attack/guard/lock-on/interact intent; input mapping independent of device; disabled/blocked actions report a reason or state. |
| Movement state | Character movement | Authoritative locomotion and movement mode (grounded, airborne, climbing/traversal if enabled); animation reads state, it does not secretly teleport the pawn. |
| Combat action | Combat component → targetable actors | Start/commit/recover/cancel action lifecycle; authored action data defines timing/windows/cost; hit detection has one owner per attack window and filters owner/team/valid targets. |
| Damage | Damage receiver | Validated damage event with source, amount/type, hit context, and result; health changes once; death/stagger/poise are explicit outcomes. |
| Interaction | Player query → interactable interface | A single selected candidate with stable interactable ID, range/visibility/priority checks, and explicit success/failure result. |
| Encounter | Encounter director → spawn/AI/objective actors | Enter/complete/fail and phase transitions; idempotent completion; encounter-scoped cleanup. Boss behavior remains a specialization of the same lifecycle. |
| Progression | Progression service | Unlock/collect/quest/ending state keyed by stable IDs; validates prerequisites and emits one event for each actual state change. |
| Narrative event | Content trigger → narrative director | Stable event ID and authored payload; conditions are evaluated from game state; playback can be interrupted/resumed according to authored policy. |
| Save snapshot | Persistence service ↔ save DTO | Schema version, slot metadata, chapter/checkpoint, progression/collectibles/settings; no raw UObject pointers or transient combat/AI/animation state. |

## 5. Core gameplay systems

### 5.1 Character movement and camera

Use `ACharacter`/`CharacterMovementComponent` as the initial physics/movement baseline unless project inspection exposes a concrete requirement they cannot meet. Build an input-to-movement contract and expose tunable movement values. Camera behavior belongs to a camera/controller boundary (e.g. spring arm/camera rig), with explicit transitions for exploration, combat focus, aim/lock-on if approved, and cinematics. Prioritize collision-safe camera behavior and player readability; camera never becomes the source of authoritative movement or combat state.

Initial movement lab scope should test acceleration/deceleration, turn response, grounded/air transitions, slopes/steps, jump/fall/landing, movement cancellation, camera obstruction, controller remapping, and gamepad/keyboard parity. Traversal moves (climb, squeeze, vault, ledge, swimming, etc.) remain unconfirmed until world/level needs are approved; do not silently add them.

### 5.2 Combat and damage

Separate **input intent**, **action selection**, **animation timing**, **hit detection**, **damage resolution**, and **feedback**. Attack definitions are authored data (stable ID, legal states, timings, costs, hit shape/trace policy, cancel windows, target rules, and feedback tags). Animation notifies may mark authored commit windows but must not be the sole safety mechanism: the combat component validates state and opens/closes hit windows; hit results are deduplicated per target per window. Prefer swept traces or validated collision queries over per-frame arbitrary damage overlap. Use explicit collision channels/profiles, friendly-fire/team filtering, and deterministic test seams.

Health, stagger/poise, death, invulnerability, and damage reception are distinct state/results. A weapon visual/mesh is not itself proof of a functional weapon. The approved weapon identity/design is unresolved in this repository; retrieve the current weapon register and Creative Director approval before implementation or new weapon art. Combat tuning should be data-driven without allowing content data to bypass validation.

### 5.3 Interaction, exploration, and feedback

A shared interaction interface supports pickups, memory discoveries, gates, NPC conversations, and authored world objects without coupling the player to each concrete actor. Interaction selection validates distance, line-of-sight/occlusion as appropriate, priority, availability, and current player state. Traversal or puzzle objects expose their own explicit begin/complete/fail contract. Audio, animation, camera, UI, and VFX subscribe to confirmed gameplay events; feedback cannot falsely indicate a failed action succeeded.

## 6. AI and NPC architecture

Use UE navigation/perception and a single selected decision framework after confirming engine version and team familiarity. Behavior Trees/EQS or StateTree are candidates, not a decision in this baseline. Keep behavior logic out of character animation graphs. Split each actor into:

- **Character/pawn**: movement, collision, health, combat and interaction capabilities.
- **AIController/decision asset**: sensing, target selection, tactical intent, and state transitions.
- **Enemy definition**: authored stats, capabilities, reactions, and allowed behavior set.
- **Encounter director**: group pacing, spawn/phase conditions, and completion, not individual locomotion.

Every AI state must have valid entry/exit conditions, timeout or failure handling, and a recovery path. NPCs that are not combatants use a separate interaction/ambient behavior path; do not imply full world simulation where only scripted behavior exists. Bosses own a phase machine and telegraphed attack patterns, but use shared damage, action, encounter, and persistence contracts. Boss phase transitions must be testable without cinematics or animation assets.

## 7. Animation architecture

Use the approved character reference and eventual production skeletal/rig assets as constraints; do not design a competing character. Animation Blueprints consume stable movement/combat state from the pawn/components. Root motion, in-place motion, motion matching, IK, retargeting, control rigs, and animation layering are implementation choices to validate against actual rigs, locomotion requirements, engine version, and performance; none is asserted as present.

Contract: gameplay owns action legality and damage timing; animation owns pose/presentation and reports authored markers through validated events. A missing montage or notify must fail safely (no permanent combat lock, phantom damage, or stuck traversal). Cinematics must have explicit handoff/restore of input, camera, character control, and gameplay state. Validate transitions, interruption, blend behavior, foot/ground contact, hit reaction, death, and cinematic return in a dedicated character lab before campaign-wide use.

## 8. World and environment architecture

Treat maps as authored spaces assembled from reusable systems, not as owners of campaign truth. Use level streaming/World Partition only after representative Chapter 1/large-area requirements and the selected UE version are known. One gameplay test map and one representative content slice should precede campaign-scale content. Define reusable world actor contracts for interaction, traversal, encounter boundaries, checkpoints, collectible/memory discovery, audio zones, and cinematic triggers.

World art is integrated only against the current Art Bible asset index and per-asset approval state. Keep `APPROVED`, `REVIEW REQUIRED`, `EXPLORATORY`, `REJECTED`, and superseded versions distinct in asset metadata/review records. An approved environment design authorizes neither story events nor unapproved character/weapon designs. Engineering can validate scale, collision, navigation, streaming, lighting cost, and gameplay readability; visual and narrative sign-off remains with their owners.

## 9. Progression, quest, and narrative architecture

Represent objectives, quests, memories, chapter gates, and ending eligibility with stable IDs and explicit prerequisite/state transitions. Keep authored narrative content separate from the runtime evaluator. A memory discovery is a durable progression event with a chapter/ID and first-discovery semantics; the seven Chapter 1–7 memories must be independently testable, persist through save/load, and collectively gate the hidden ending only when all seven are recorded. The hidden ending gate must not be bypassable through UI state or a chapter-local counter.

Creative canon to preserve in content and tests:

- Principal characters: Adanna, Nneka, Ezeani, Okwu, Amadioha, Idemili, and the Hollow King. Adanna is 25 in the main story.
- The eight user-specified chapter identities and bosses are fixed for implementation planning; this table is a faithful index, not additional lore:

  | Chapter | Identity / boss |
  |---|---|
  | 1 | Forbidden Forest — Great Root Mother |
  | 2 | Kingdom Beneath the Earth — Iron Elephant |
  | 3 | City of the Living Dead — King Without a Face |
  | 4 | River of Idemili — Daughter of the Deep |
  | 5 | Mountain of Thunder — Amadioha's Champion |
  | 6 | Kingdom of Masks — Mother of Masks |
  | 7 | Gates of the Dead — Hollow King |
  | 8 | The Last Daughter / Ancestral Realm — Ezeani |

- Seven Nneka memories, one hidden in each of Chapters 1–7; all seven are required for the hidden ending.
- The three endings are kill Ezeani, spare Ezeani, and the hidden ending (earned by finding all seven memories). The technical ending gate must not alter or add a branch.
- The current approved-in-principle Memory 7 direction: the boundary demanded Adanna; Nneka offered herself; Ezeani killed her and then concealed the circumstances; the revelation complicates but does not absolve him. Adanna was six when Nneka died and recalls the event through an incomplete child's perspective. Exact sequence, dialogue, and details still require Creative Director review per `DECISIONS.md`.

The narrative system must not claim an unreviewed detailed memory sequence as final canon. Cinematic and dialogue playback report completion/interruption; game-state changes are explicit authored events, not inferred from a sequence ending. The quest system owns objective state, not dialogue text or cinematic camera control.

## 10. Data and persistence

### Static authored data (proposed)

Use stable-ID data definitions for attack actions, enemies, encounters, interactables, objectives, memories, chapters, and tuning. Validate duplicate/missing IDs, dangling references, invalid prerequisites, and asset approval metadata in editor/automation checks. Do not make a general-purpose schema before the first content vertical slice proves its need.

### Runtime/save data (proposed)

Use a versioned `USaveGame`-derived container or equivalent engine-supported save service. Store a schema version, slot/profile metadata, chapter/checkpoint identifiers, durable quest and collectible/memory states, ending decisions/eligibility, player progression/equipment only where approved, and user settings. Save stable identifiers and values; never serialize live actors, pointers, transient AI/encounter internals, or assume actor load order. Add migration functions and preserve a backup/previous slot when upgrading data. Save writes should be atomic/validated as far as platform APIs permit, with explicit failure reporting and a recoverable checkpoint policy.

Test new game, save, reload, map transition, checkpoint recovery, corrupt/older schema handling, duplicate discovery, all-seven-memory gate, each ending route, and interrupted save/load. Save format changes require compatibility tests and release notes.

## 11. Inter-agent interfaces and ownership

| Agent | Primary ownership | Required integration contract |
|---|---|---|
| **1 — Gameplay, Character & Combat Engineering** | Player pawn/input-facing gameplay, movement, camera control contract, combat/damage, character action state, combat test fixtures. | Publishes player-command, movement-state, combat-action, damage, and interaction contracts. Does not create a second progression/encounter/save implementation or approve art/canon. |
| **2 — World, Systems, Environment & Gameplay Simulation** | World interaction/traversal, encounters and AI/NPC behavior, progression/quest/memory runtime, chapter/world integration. | Consumes Agent 1 contracts; publishes interactable, encounter, progression/narrative-event, and checkpoint interfaces. Does not implement competing player movement/combat or silently change story/art. |
| **3 — Integration, Technical Quality, Build & Performance** | Project configuration/build pipeline, integration gates, automated test harness, profiling, packaging readiness, dependency and risk tracking. | Owns reproducible build/test evidence and integration review; cannot silently change gameplay contracts or creative decisions. Reports regressions and proposes options before modifying shared system boundaries. |

All agents work on the current repository branch/authorized workflow and preserve existing work. Before parallel implementation: agree on UE version, module layout, public headers/interfaces, ownership and test fixture; document interface changes and dependents; one owner integrates a shared system. Integration tests are run after each cross-agent change. Creative questions (canon, visual approval, folklore/cultural claims) go to the Creative Director, not resolved by engineering consensus.

## 12. Testing and evidence strategy

No Unreal automation was possible in the inspected checkout: there is no `.uproject`, engine binary, or implementation to test. Once available, create a clean-checkout editor/command-line build and automated test path before gameplay features.

- **Static/editor validation:** project opens; assets compile; stable IDs/references validate; no errors or new unexplained warnings; maps and data pass validators.
- **Unit/component tests:** movement state transitions; combat legality, hit-window deduplication, damage filtering; interaction candidate selection; memory/progression prerequisites; save migrations and ending eligibility.
- **Unreal Automation Tests:** deterministic tests of gameplay components/services and content validation. Keep pure state rules testable without loading full cinematic maps.
- **Functional/map tests:** launch representative map; possess Adanna; traverse the approved test route; execute attacks and receive damage; complete an encounter; interact with a memory; transition/checkpoint; save/reload. Run on a packaged Development build as well as Editor where feasible.
- **End-to-end campaign tests:** each chapter gate, memory persistence across travel, all seven-memory hidden gate, kill/spare Ezeani branches, hidden ending unlock, repeated/interrupted sequence safety, checkpoint and failure recovery.
- **Manual playtests:** input feel/readability, camera comfort, accessibility, visual and audio feedback, traversal clarity, cultural and narrative review. Record build, map, steps, expected/actual result, evidence, severity, and owner for every issue.
- **Release/quality:** clean package on every supported platform, fresh install and upgrade save checks, crash/error review, performance captures, known-issues list, and explicit sign-off. Tests never substitute for Creative Director/visual/cultural approval.

A test is only reported as passing with the engine/project/build identifier, command or reproducible steps, result, and captured log/evidence. Mocked, partially implemented, experimental, and unavailable behavior is labeled honestly.

## 13. Performance targets, profiling and risks

**Provisional target only:** aim for stable 60 FPS on a yet-to-be-selected reference PC at a yet-to-be-selected 1080p quality preset (16.67 ms frame budget). This is a planning placeholder, not an accepted platform commitment or measured result. Establish CPU/GPU/memory budgets on named reference hardware before production content scales; set minimum spec, resolution, quality tiers, and platform-specific target with the Creative Director/producer.

Use Unreal Insights and engine stat/profiling tools on representative gameplay captures. Track game thread, render thread, GPU, memory, streaming hitches, shader compilation, actor/tick counts, animation, AI, VFX, audio voices, and load/save latency. Profile packaged builds, not only editor. Use scalable quality settings and validate lighting/material/geometry choices with actual art rather than prematurely imposing asset budgets.

Key risks/open gates:

1. **No actual project or engine version:** major compatibility and implementation assumptions remain unverified; block feature implementation until the real project baseline is provided or explicitly authorized as a new project.
2. **Platform and quality target unspecified:** performance targets and packaging cannot be finalized or evidenced.
3. **Weapon/character asset approval:** never select or fabricate a weapon/character design from engineering convenience; verify the current approved asset/register.
4. **Art-bible revision churn:** integrate versioned assets by ID and approval state; preserve superseded versions and source links, never overwrite approved work.
5. **Memory/canon detail:** Memory 7 direction is approved in principle; exact content and sequence need review. Maintain separation between technical flag logic and narrative text.
6. **Save compatibility:** early schema mistakes can corrupt campaign state; version from the first persistent field and test migration.
7. **Combat animation coupling:** missing or late animation can break action timing; combat state validates notify events and fails safe.
8. **Scope/performance:** eight chapters and a cinematic visual bar can exceed content and hardware budgets; prove a representative vertical slice and profile early.
9. **Cultural representation:** avoid unsupported claims about Igbo tradition; flag invented lore clearly and require research/consultation review.
10. **Integration ownership:** overlapping agent work risks competing systems; contracts, system owner, and integration gates are mandatory.

## 14. Production phases, dependencies and exit gates

The sequence below follows the required production order. Later phases do not begin substantial implementation before prior gate evidence exists.

| Stage | Scope and dependencies | Exit/acceptance evidence |
|---|---|---|
| **1. Architecture & technical foundation** | This document; obtain the real UE project or explicit new-project authorization; confirm engine/platform/network scope; inventory project, plugins, assets, art bible references; set modules/source-control/build/test baseline and interface ownership. | Clean checkout opens/builds in the pinned UE version; asset/config inventory and decisions log exist; a minimal test map and automated test command run; all proposed contracts reviewed; no unowned plugin/dependency. **Current: document delivered; technical foundation not executed.** |
| **2. Movement & character laboratory** | Stage 1 project baseline; approved Adanna reference and rig availability; input/device decision. | Reproducible movement/camera test map; acceptance tests for locomotion, collision, camera obstruction, controls and state transitions; manual feel review on target input devices; no placeholder represented as a finished system. |
| **3. Combat foundation** | Stage 2 movement/action ownership; approved weapon identity/asset and animation availability; damage contract. | Testable attack/defense/evade/action lifecycle, validated hit windows and damage, target filtering, reactions/death, tuning data validation; repeatable combat test map and packaged functional evidence. |
| **4. Character behavior & animation** | Movement/combat state contracts; production rig/animation source and approval. | Robust locomotion/action/hit/death/cinematic transitions, interruption/fallback tests, animation/gameplay timing review and representative performance evidence. |
| **5. Enemy & boss architecture** | Combat/damage/animation contracts; selected AI framework; authored approved enemy/boss references. | Reusable enemy and boss phase architecture; deterministic state/phase tests; telegraph/readability and recovery tests; encounter lifecycle and packaged encounter evidence. |
| **6. World simulation, exploration & traversal** | Stable player/interaction/encounter contracts; representative map scale and streaming decision. | Interaction/traversal contracts, NPC/world behavior, navigation/streaming/collision checks, route and encounter tests, performance capture on a representative space. |
| **7. Progression & narrative systems** | Stable gameplay/world contracts; reviewed quest/memory/ending content and stable IDs. | Persistence-backed objectives, seven-memory tracking, ending eligibility, sequence interruption/return, save migration and campaign-state tests. No unreviewed canon. |
| **8. Campaign & chapter production** | All foundation gates; approved asset pipeline, chapter content/register, staffing and platform budget. | Each of eight chapters integrated to the accepted vertical-slice standard; chapter entrance/exit, boss/quest/memory requirements validated; full branch and hidden-ending coverage; level content reviewed by creative/art owners. |
| **9. Polish, optimization, test & release** | Complete campaign candidate and target platform/hardware. | Content-complete packaged builds, performance/memory/frame pacing within approved targets, save upgrade/compatibility, accessibility/audio/localization decisions, crash/known-issue review, QA evidence, and explicit release sign-off. |

Every stage also maintains a scope, owner, dependencies, interfaces, measurable acceptance criteria, automated/manual tests, evidence links, risks, and unresolved issues. A failed gate is reported and addressed; it is not relabeled as complete.

## 15. Immediate next decisions and actions

1. Provide the location/branch of the actual Unreal project, or explicitly authorize creation of a new UE5 project in this repository. Do not overwrite or scaffold over an existing project before it is inspected.
2. Confirm UE5 minor version and supported platform(s), reference hardware, frame-rate/resolution target, single-player vs network scope, and intended release/distribution.
3. Confirm source control and binary asset strategy, and identify the current asset/weapon/character registers and approved playable production references.
4. With Agent 3, inventory the real project and produce a build/config/plugin/asset report; verify the engine can open and build it before coding systems.
5. Review this architecture with Agents 1–3; accept or amend contracts before beginning Stage 2. Technical proposals remain proposals until validated against the project.

### Completion state of this deliverable

**Delivered:** initial Master Engineering Architecture Document and honest repository/project-state assessment.
**Not delivered or tested:** Unreal project/configuration, code, playable mechanics, build, automated engine tests, performance captures, production art integration, or stage-1 exit evidence.
