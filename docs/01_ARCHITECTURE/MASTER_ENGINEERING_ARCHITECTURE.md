# THE DISOBEDIENT DAUGHTER — MASTER ENGINEERING ARCHITECTURE DOCUMENT

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Document ID:** TDD-MEAD-001
**Version:** 1.0 — DRAFT FOR TECHNICAL DIRECTOR REVIEW
**Date:** 2026-11-16
**Author:** Arena Agent Mode (engineering agent), acting under the Technical Director
**Authority chain:** Creative Director (final, creative) → Technical Director (technical) → engineering agents
**Companion documents:** `docs/00_GOVERNANCE/PROJECT_STATE_2026-11-16.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md`, `docs/00_GOVERNANCE/OPEN_QUESTIONS.md`, `docs/01_ARCHITECTURE/CODING_STANDARDS.md`, `docs/03_DECISIONS/ADR-*.md`

---

## 0. Document control

### 0.1 What this document is

This is the Stage 1 deliverable required before substantial implementation: a complete technical architecture, the current-state assessment that justifies it, the interfaces between the three development agents, the testing strategy, performance targets, and a phased plan with dependencies and exit criteria.

It is **a plan**, not evidence of working software. Nothing described here is implemented except where Section 1 says so.

### 0.2 Verification statement (read before trusting anything here)

The agent workspace used to author this document has **no Unreal Engine, no UnrealBuildTool, no .NET SDK, no C++ toolchain for MSVC/Clang**, 2 vCPU and 3 GB RAM. Inspected state:

| Capability | Present in agent workspace | Consequence |
|---|---|---|
| Unreal Engine 5.8 editor | No | Cannot open, compile, cook or run any UE project |
| UnrealBuildTool / AutomationTool | No | Cannot compile C++ or run automation tests |
| .NET SDK | No | Cannot build UBT |
| MSVC / Clang | No (only system `g++`) | Cannot compile MSVC-target C++ |
| GPU | No | Cannot render, profile or capture frames |
| Google Drive (Art Bible) | Yes (connected) | Can read authoritative art/narrative decisions |
| Git/GitHub | Yes | Can version, commit, push, open PRs |

**Therefore:** all code authored by this agent is `IMPLEMENTED_UNVERIFIED` at best and `DESIGN_ONLY` until the Technical Director builds and tests it on a UE 5.8 machine. Status vocabulary is defined in `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` and must be used in every agent report. No agent may mark a system `IMPLEMENTED_AND_VERIFIED` without attached build log, automation test output, and (where relevant) frame-time capture.

This constraint is recorded as **ADR-0012** and is the single biggest process risk in the project; Section 17 addresses mitigation.

### 0.3 Scope boundaries

- **In scope:** runtime architecture, build configuration, systems design, interfaces, data/persistence, testing, performance, phasing.
- **Out of scope (other authority):** story content, chapter events, dialogue, visual design, asset approval. Those come from the Creative Director and the Google Drive Production Art Bible. Engineering may not invent them. Where engineering needs content it does not yet have, it must use a **named, visibly-labelled placeholder** and log a blocking question — never an invented fact dressed as canon.

---

## 1. Current project assessment

### 1.1 Repository state (inspected 2026-11-16)

The directive says "do not assume the project is empty". It was inspected, and it is empty of game content:

```
$ git log --oneline
5e3d1da Initial commit
$ git show --stat HEAD
 README.md | 1 +
$ find . -path ./.git -prune -o -type f -print
./README.md          # 6 bytes: "# TDD"
```

| Item | State |
|---|---|
| Unreal project file (`.uproject`) | **Absent** |
| `Source/`, `Config/`, `Content/` | **Absent** (directories created empty by this document's author) |
| C++ modules, target files, Build.cs | **Absent** |
| Any `.uasset` / `.umap` | **Absent** |
| Engine version pin | **Undecided** (recommended: 5.8, see ADR-0001) |
| CI, build scripts, test harness | **Absent** |
| Git LFS | **Not installed in this workspace**; must be configured on the production workstation before the first binary asset is committed |
| Branch | `arena/3bc206a0-tdd`, branched from `main` @ `5e3d1da` |

There is no prior agent work in this repository to preserve, integrate with, or avoid overwriting. This is the cleanest possible starting condition and also the most dangerous one: **there is no established code convention to inherit**, so this document defines them.

### 1.2 Production Art Bible state (Google Drive, read 2026-11-16)

The authoritative visual source is the Drive folder `THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE` (`1lzJBgHHSO2OJMB0LFmwQoU6R7Kv2iGlZ`), indexed by `ART_BIBLE_MASTER_INDEX_POST_SYNC_2026-11-16.md` (`1r5TKhV74Q3hATrSwwm9r-zP4HxRIwF4f`).

| Measure | Value |
|---|---|
| Indexed files | 176 |
| **Approved designs (section 0 of index)** | **7** |
| Files still `REVIEW REQUIRED` | The large majority of the 176 |
| Exploratory (explicitly not canon) | Chapter 8 combined direction, Okwu hood exploration, others |
| Rejected designs | Kept separately in `16_REJECTED_DESIGNS` |

The seven approved designs:

| Asset | Decision | Nature |
|---|---|---|
| `CHAR_ADANNA_MASTER_REFERENCE_V001` | OAD-02 | Concept reference sheet (not a 3D asset) |
| `CHAR_AMADIOHA_MASTER_REFERENCE_V001` | OAD-16 | Concept reference sheet |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_SEALED_QUARTER_V003` | OAD-45 | Environment concept board |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_NNEKAS_HOUSE_V004` | OAD-45 | Environment concept board |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_NNEKAS_HOUSE_INTERIOR_V003` | OAD-45 | Environment concept board |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_HALL_OF_POSTS_V004` | OAD-45 | Environment concept board |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_MOTHERS_COURTYARD_SAME_COURTYARD_V007` | OAD-53 | Environment concept board |

**Critical engineering consequence.** The project has **zero production-ready 3D assets**: no meshes, rigs, textures, animation, audio or cinematic content in any approved form. Boards are 1376×768 renders upscaled into 2560×1440 boards (OAD-08). Every approved design also notes that design approval is not narrative-canon approval (OAD-48): all five Chapter 8 environments carry canon status `PENDING APPROVAL`.

This drives three architectural mandates:
1. Stage 1–5 must be playable with **engine-basic placeholder geometry and labelled stand-in animation**, never presented as art progress.
2. All character/environment content must be reachable through **data assets carrying canon status + Art Bible IDs**, so that content can be swapped without touching code (ADR-0008).
3. No agent may generate "final-looking" art assets for gameplay. Environment and character design authority sits with the Creative Director and the visual production team.

### 1.3 Open art and canon decisions that constrain engineering

Read from `OPEN_ART_DECISIONS.md` (`1HkaV90iCq3Kmn3M8rgyNPiJ61m7UISPN`) and `DECISIONS.md` root file (`1kMDn5oXmy6DhBJsROJ6EIn_ZXUPbLENx`). The register is authoritative; this is a filtered view of items with engineering impact.

**Resolved and binding on implementation**

| ID | Decision | Engineering effect |
|---|---|---|
| OAD-01 | Adanna's single shoulder guard is on her **left** shoulder | Skeleton/socket layout, armour mesh attach point, asymmetry must survive retargeting |
| OAD-02 | Adanna master portrait is the identity anchor | Character data asset references this ID; no proportions invented |
| OAD-09 | Blade worn on her **left** hip | Weapon socket `weapon_holster_l`, sheath attach |
| OAD-10 | Upgraded armour = single larger left guard | Progression system must support alternate armour mesh, not recolor |
| OAD-12 | Okwu's hood hides **darkness only**, in every light | No face geometry; shader/lighting must not reveal; render a black-body material, tested in Lumen-lit and shadowed cases |
| OAD-14 | Pythons are never enemies or loot (Ch. 4) | AI spawn tables for Ch. 4 exclude python archetypes; validator check |
| OAD-19 | White rams are ordinary livestock, no gameplay rule | Animal archetype = ambient NPC, no loot table entry |
| OAD-31 | Ending 1's killing of Ezeani is **literal** | Ending presentation is not symbolic; cinematic must show it directly |
| OAD-32 | Seven Nneka memories, Ch. 1–7, exploration-earned, met as *fragments of place/object/sound/interaction* — not collectible cutscenes | Memory system must trigger from world interaction, not from a pickup-and-play-cutscene flow. This is an architectural constraint, not a content preference |
| OAD-34 | Memory 7 truth: Nneka offered herself, asked Ezeani to do it, he killed her, he concealed it; canon unchanged; Ezeani stays morally complicated | Ending resolver must not treat "truth known" as absolution; no morality score may flip the outcome |
| OAD-35 | Adanna was **six** when Nneka died | Memory 4/6 child-POV presentation (reduced locomotion set, camera scale, no adult animations) |
| OAD-37 | Adanna on environment boards: small, approved blade only | No alternate weapons without weapon-register approval (also OAD-09) |
| OAD-39 | Nneka's voice is deliberate, she is dead, never implied alive; no new supernatural mechanism | Voice playback system must not imply presence; a code rule bans "echo" wording in UI copy keys |
| OAD-41 | Hollow King began ~1 year before game opens | Timeline constant in narrative data; no pregame memory content |
| OAD-44 | Courtyard tree ages *older and larger* going back; four generations | Level variants are data-layer states of one location, not separate levels |
| OAD-48 / OAD-53 | Environment design approval ≠ canon approval | Canon status is a separate field from design status |

**Open — engineering must not assume**

| ID | Open question | Blocking for |
|---|---|---|
| OAD-03 | Ezeani's regalia (consultant review) | Ezeani character asset only; not blocking gameplay |
| OAD-04 | Okwu and raffia/masquerade imagery | Okwu asset; culturally sensitive — requires consultant |
| OAD-06 | Uli-style linework on Adanna's *mmuo* markings | Material/texture work only; **never invent named uli motifs** |
| OAD-07 | Gold level (aged bronze standard) | Material language; blocking for final art pass |
| OAD-13 | Nneka's hair (braided crest vs threaded) | Nneka asset |
| OAD-23 | Content of the three ending sequences | Ending cinematic content; **not** the resolver contract |
| OAD-32 (content half) | Exact content/implementation of each of the seven memories | Memory content data; framework is not blocked |
| OAD-34 (detail half) | Detailed memory sequence, events, dialogue | Memory content data |
| OAD-55 | Villager clothing standard (proposed) | NPC crowd content, not NPC framework |

### 1.4 What exists / needs modification / must be built / remains undecided

| Classification | Items |
|---|---|
| **Exists** | Git repository; branch; Art Bible (Drive); decision registers (Drive); this document set |
| **Needs modification** | `README.md` (replaced with real project onboarding); nothing else — no code exists to modify |
| **Must be built** | Everything: project skeleton, 9 modules, all gameplay systems in Sections 4–12, test harness, CI, packaging pipeline, 8 chapters of content (content is owned by production, not engineering) |
| **Undecided** | Engine pin (recommend 5.8); target platforms; audio middleware (recommend none); GAS adoption (recommend yes); reference hardware; whether console port is in scope; save-scumming policy; localisation languages; accessibility baseline; whether combat uses a stamina economy or posture-only |

---

## 2. Engine and project configuration

### 2.1 Engine version

**Recommendation: Unreal Engine 5.8** (released June 2026; the final planned major UE5 release, now receiving bug-fix support only). Rationale in ADR-0001: it is the last UE5 branch, so it is the terminal target for plugin compatibility and the longest-lived stable branch for a multi-year project; UE6 early access is expected ~2027 and adopting an unproven next-gen engine mid-production is a schedule risk, not a quality gain.

**Pin requirements (non-negotiable once fixed):**
- Exact version recorded in `.uproject` (`"EngineAssociation": "5.8"`) and in `Config/DefaultEngine.ini` project version fields.
- Source builds pinned by git tag/commit in `docs/02_PRODUCTION/ENGINE_PIN.md` (to be created on first build).
- Engine upgrades are ADR-gated and require a full regression run (Section 14) — never a casual upgrade.

**Experimental-feature policy (ADR-0010):** production paths may use only features marked Production-Ready in 5.8. Explicitly **excluded** from shipping paths: Mesh Terrain (Experimental), MetaHuman Crowd (Experimental), MCP editor plugin (Experimental), Substrate (only if the material team adopts it deliberately — currently excluded to avoid locking asset reauthoring), Lumen Lite (Beta; evaluated for min-spec only, behind a scalability switch).

Production-ready features adopted: Nanite, Lumen (High for PC), Virtual Shadow Maps, TSR, World Partition, World Partition HLOD, StateTree, Motion Matching/Pose Search (see 8.2 for the maturity caveat), Enhanced Input, MetaSounds, Sequencer, Control Rig, Chaos Cloth/Physics, MetaHuman (character pipeline only, subject to art direction), MegaLights (evaluated, not baseline).

### 2.2 Build targets and configurations

| Target | Type | Purpose |
|---|---|---|
| `TDDEditor` | Editor | Development, content authoring, automation tests, data validation |
| `TDD` | Game | Packaged client (Development / Test / Shipping configs) |
| `TDDServer` | Server | **Not required** (single-player). Created only if a networked mode is later approved |

- C++ standard: C++20 (UE 5.8 default). Compilers: MSVC 14.4x on Windows; Clang for any future Linux/console builds.
- `bUseUnityBuild = false` for `TDDCore` and `TDDGameplay` (faster incremental iteration, catches missing includes); unity builds enabled elsewhere.
- `bUseAdaptiveUnityBuild` on for the editor.
- Warnings-as-errors enabled in Development; `bWarningsAsErrors = true` for our modules only (engine third-party warnings not escalated).
- RTTI off, exceptions off (engine defaults), IWYU enforced (`IWYUSupport = IWYUSupport.Full`).

### 2.3 Required plugins (each justified; nothing speculative)

| Plugin | Justification | Shipping risk |
|---|---|---|
| Enhanced Input | Required for modern input, rebinding, mapping contexts | Engine default, safe |
| Gameplay Abilities (GAS) | Attributes, effects, cooldowns for combat/progression (ADR-0004) | Shipped in many AAA titles; safe |
| StateTree | Enemy/boss/NPC behaviour (ADR-0006) | Production-ready; safe |
| Pose Search (+ Motion Matching) | Locomotion quality target (ADR-0005) | **Verify 5.8 maturity**; documented fallback |
| Chooser | Context selection for animation/behaviour | Stable |
| Motion Warping | Attack and traversal alignment | Stable |
| Control Rig | Foot IK, weapon grip, facial | Stable |
| Niagara | VFX | Stable |
| MetaSound | Audio design without middleware (ADR-0009) | Stable |
| Sequencer / Level Sequence Editor | Cinematics | Stable |
| World Partition | Chapter streaming | Stable |
| Level Sequence Editor, Data Validation | Authoring + canon gating (ADR-0008) | Stable |
| Common UI | Menu/HUD framework, gamepad focus, accessibility | Stable |
| Automation Driver + Functional Testing (dev only) | Automated input-driven tests | Dev-only, not cooked |
| Unreal Insights / Trace (dev only) | Profiling | Dev-only |

**Not adopted (deliberately):** Wwise/FMOD (middleware cost and integration risk before audio design exists), any third-party save plugin, any marketplace combat framework, any networked framework, Mesh Terrain, MetaHuman Crowd, MCP editor plugin.

### 2.4 Source control and asset policy

- Git with **Git LFS mandatory** for `Content/**/*.{uasset,umap,ubulk,uexp}`, `.fbx`, `.wav`, `.mp4`, `.exr`, `.tga`, `.png`, `.jpg` over 100 KB. `.gitattributes` is committed and authoritative.
- 100 MB hard per-file limit on the agent snapshot path: **large binaries (cinematic renders, source art PSDs, audio stems) live in Drive/Perforce, not in this repo.** The repo holds engine-ready assets only.
- `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, `.vs/`, `*.sln` are ignored.
- Commit message convention: `TDD-<area>: <imperative summary>` with body stating status claim and test evidence, e.g. `TDD-combat: add posture break window (IMPLEMENTED_UNVERIFIED, no build available)`.

### 2.5 Project identity and naming

- Unreal project name: `TDD` (short, stable, matches module prefix). Product name: `The Disobedient Daughter`.
- Module prefix `TDD`; class prefixes `ATDD*`, `UTDD*`, `FTDD*`, `ETDD*`, `ITDD*`.
- Asset prefixes: `BP_`, `M_`, `MI_`, `SK_`, `SM_`, `T_`, `AN_`, `AM_` (anim montage `AM_`), `ABP_`, `L_`, `DA_`, `PDA_` (primary data asset), `LS_` (level sequence), `NS_` (Niagara), `MS_` (MetaSound), `W_` (widget), `DT_`, `EQS_`, `ST_` (StateTree).
- Content root layout mirrors the Art Bible register so asset↔canon lookup is mechanical: `Content/TDD/Characters/<Character>/`, `Content/TDD/Environments/CH01_ForbiddenForest/…`, `Content/TDD/Core/`, `Content/TDD/Audio/`, `Content/TDD/Cinematics/`, `Content/TDD/UI/`, `Content/TDD/Data/`.
- Every asset carries `AssetName + _V###` version suffix only where the Art Bible does; otherwise we do not version assets in filenames (git does that).

---

## 3. Proposed technical architecture

### 3.1 Architectural principles

1. **Downward-only dependencies.** `TDDCore` is a leaf. No module may depend on a module above it. Cycles are a build failure, not a style preference.
2. **Contracts before implementations.** Cross-agent contracts live in `TDDCore` as interfaces/structs and change only under ADR review (Section 13).
3. **Data over code for content.** Attacks, enemies, bosses, quests, memories, chapters, locations are data assets; code supplies the evaluators. Content authors must not need a programmer to add an enemy variant or a memory.
4. **One implementation per system.** No parallel combat systems, no second save system, no shadow AI stack. Extending a system is preferred over forking it.
5. **Everything testable off the render thread.** Damage math, posture, phase selection, quest conditions, ending resolution, save serialisation must be testable with no viewport.
6. **Explicit failure.** Missing animation database, missing data asset, unresolvable condition → loud, logged, non-silent degradation with a name attached.
7. **Single-player by design.** No replication cost, no client prediction complexity. Gameplay code must not be written in a way that makes a later co-op impossible, but we do not pay for it now.

### 3.2 Module map

```
                      +-------------------+
                      |      TDDUI        |  HUD, menus, prompts, journal, settings
                      +---------+---------+
                                |
          +---------------------+---------------------+
          |                     |                     |
 +--------+--------+   +--------+--------+   +--------+---------+
 |  TDDNarrative   |   |     TDDAI       |   |    TDDEditor     |  (Editor-only)
 | quests/memories |   | enemies, bosses |   | validators, cmdlets,
 | endings, cinemas|   | encounters, NPC |   | data audits, cook gates
 +--------+--------+   +--------+--------+   +--------+---------+
          |                     |                     |
          |                     v                     |
          |            +--------+--------+            |
          |            |   TDDGameplay   |<-----------+
          |            | pawns, camera,  |
          |            | combat, input,  |
          |            | interaction     |
          |            +--------+--------+
          |                     |
          +----------+----------+
                     v
            +--------+--------+
            |     TDDWorld    |  chapters, streaming, world state,
            |                 |  time/weather data layers, checkpoints
            +--------+--------+
                     |
                     v
            +--------+--------+
            |     TDDCore     |  types, interfaces, events, save contracts,
            |                 |  persistence, canon refs, logging, RNG, math
            +-----------------+
```

Rules:
- `TDDGameplay` **must not** include `TDDAI`, `TDDNarrative` or `TDDUI` headers. AI/narrative/UI observe gameplay through `TDDCore` events and interfaces.
- `TDDAI` may depend on `TDDGameplay` (it needs to perceive pawns and issue combat intents) but must not reach into gameplay private internals — only the public components/interfaces listed in Section 13.
- `TDDNarrative` depends on `TDDCore` + `TDDWorld` only.
- `TDDEditor` may depend on everything; nothing may depend on `TDDEditor`.
- Test code lives inside each module behind `WITH_DEV_AUTOMATION_TESTS`, plus `TDDTests` (Editor-only functional/integration tests).

### 3.3 Frame data flow

```
Device input
  -> Enhanced Input (mapping context by player state)
  -> UTDDPlayerInputComponent  (buffering, hold/toggle, deadzone/sensitivity)
  -> intent  (FTDDIntent: Move, Look, LightAttack, HeavyAttack, Dodge, Block, Parry,
              LockOn, Interact, Traversal, Sprint, Menu)
  -> UTDDCharacterStateMachine (Exploration | Combat | Traversal | Cinematic | Dead | Menu)
  -> system resolves:  locomotion (CMC + motion matching)
                       combat (attack data -> hit windows -> damage request)
                       interaction / traversal (traces -> prompt -> montage)
  -> TDDCore event bus (DamageApplied, EnemyKilled, MemoryDiscovered, ChapterCompleted …)
  -> consumers: AI (aggro), narrative (quests/memories), UI, audio, VFX, persistence
  -> feedback: hitstop, camera shake, haptics, audio, VFX, damage response
```

Determinism note: gameplay resolution runs on the game thread at a fixed step; any timed gameplay window (parry, i-frame, hitstop) is expressed in **seconds of gameplay time** and converted with the current time dilation, never in raw frames, so slow-motion and hitstop cannot silently change combat tuning.

### 3.4 Runtime ownership: subsystems and lifetime

| Class | Base | Lifetime | Responsibility | Owner agent |
|---|---|---|---|---|
| `UTDDGameInstance` | `UGameInstance` | Process | Boot, session, save slot selection, chapter hand-off | 3 |
| `UTDDEventBus` | `UGameInstanceSubsystem` | Process | Typed events between modules (Section 3.5) | 3 |
| `UTDDPersistenceSubsystem` | `UGameInstanceSubsystem` | Process | Save/load, versioning, migration, integrity | 3 |
| `UTDDCanonRegistry` | `UGameInstanceSubsystem` | Process | Canon-status lookups, Art Bible ID resolution, ship-time validation hook | 3 |
| `UTDDNarrativeSubsystem` | `UGameInstanceSubsystem` | Process | Quest/flag store, chapter state | 2 |
| `UTDDMemorySubsystem` | `UGameInstanceSubsystem` | Process | Seven memories: discovery, count, Ending-3 gate | 2 |
| `UTDDChapterFlowSubsystem` | `UWorldSubsystem` | World | Chapter load/unload, checkpoints, transitions | 2 |
| `UTDDWorldStateSubsystem` | `UWorldSubsystem` | World | Time of day, weather, data-layer states (OAD-24) | 2 |
| `UTDDCombatDirectorSubsystem` | `UWorldSubsystem` | World | Attack tokens, simultaneous-attacker budget | 1 |
| `UTDDEncounterManager` | `UWorldSubsystem` | World | Encounter activation, waves, leash, completion | 2 |
| `UTDDHitStopSubsystem` | `UWorldSubsystem` | World | Time dilation stacks, deterministic expiry | 1 |
| `UTDDCinematicSubsystem` | `ULocalPlayerSubsystem` | Player | Sequencer play/skip, input suppression, letterbox, subtitles | 2 |
| `UTDDInteractFocusSubsystem` | `ULocalPlayerSubsystem` | Player | Interaction focus/proximity resolution | 1 |
| `UTDDPerformanceBudgetSubsystem` | `UWorldSubsystem` (dev) | World | Runtime budget assertions in Test/Development | 3 |

Naming/lifetime discipline: state that must survive a level transition goes in a `GameInstanceSubsystem` and is **serialisable** (Section 10). State that dies with the world goes in a `WorldSubsystem`. Static utility with no state is a `UBlueprintFunctionLibrary` or plain namespace function.

### 3.5 Cross-module event contract

Events are `USTRUCT`s in `TDDCore` (`Events/TDDEvents.h`), published on `UTDDEventBus`, and carry **no pointers to actors** — they carry `FGuid` entity IDs and value data, so a listener cannot accidentally hold a stale actor. Subscribers are weak-lifetime-checked.

| Event | Payload | Typical subscribers |
|---|---|---|
| `FTDDDamageAppliedEvent` | InstigatorId, TargetId, Amount, DamageType tag, HitResult summary, bLethal | AI, UI, audio, narrative (kill counters) |
| `FTDDEntityKilledEvent` | EntityId, ArchetypeId, ChapterId, Method tag | Encounters, narrative, progression |
| `FTDDCombatStateChangedEvent` | PawnId, OldState, NewState | UI, audio, camera |
| `FTDDPostureBrokenEvent` | TargetId, SourceId | AI, VFX, audio |
| `FTDDMemoryDiscoveredEvent` | MemoryId (1–7), ChapterId, FragmentKind | Memory subsystem, UI, audio, ending gate |
| `FTDDQuestStepCompletedEvent` | QuestId, StepId | Narrative, UI, persistence |
| `FTDDChapterStateChangedEvent` | ChapterId, OldState, NewState | Chapter flow, persistence, UI |
| `FTDDLocationEnteredEvent` | LocationId (`CH08-INT-001`), bIsScene | World state, audio, codex |
| `FTDDInteractionPerformedEvent` | InteractableId, Verb tag | Narrative, audio, persistence |
| `FTDDCheckpointReachedEvent` | CheckpointId, ChapterId | Persistence |
| `FTDDPlayerDiedEvent` | Cause tag, LocationId | Flow, UI, persistence |
| `FTDDEndingReachedEvent` | EndingId | Narrative, UI, credits |
| `FTDDCinematicStateChangedEvent` | SequenceName, bPlaying, bSkippable | UI, input, audio |

Adding a new event type is a `TDDCore` contract change (Section 13) — not a free action.

---

## 4. Core gameplay systems

### 4.1 Player representation

| Class | Base | Notes |
|---|---|---|
| `ATDDPlayerCharacter` | `ACharacter` | Adanna in playable chapters. Owns the components below. |
| `ATDDPlayerController` | `APlayerController` | Input routing, camera manager selection, UI ownership |
| `ATDDPlayerCameraManager` | `APlayerCameraManager` | Camera shakes, FOV, post-process blending |
| `UTDDCharacterStateMachine` | `UPawnComponent` | Single authority on "what is allowed right now" |
| `UTDDLocomotionComponent` | `UPawnComponent` | Gait/stance intent → anim + movement params |
| `UTDDCombatComponent` | `UPawnComponent` | Attack graph, windows, cancels, hit resolution |
| `UTDDWeaponComponent` | `USceneComponent` | Weapon mesh, sockets, holster/draw, trail hooks |
| `UTDDInteractionComponent` | `UPawnComponent` | Focus, prompts, hold-to-perform |
| `UTDDTraversalComponent` | `UPawnComponent` | Ledge/vault/climb detection and execution |
| `UTDDCharacterAudioComponent` | `UActorComponent` | Footsteps, cloth, exertion, voice hooks |
| `UTDDPlayerInputComponent` | `UEnhancedInputComponent` | Binding, buffering, remapping |

`UTDDCharacterStateMachine` exists because "can I dodge during a heavy attack recovery, while falling, with an enemy grabbing me" must have exactly one answer in exactly one file. All systems query it; only it decides.

States: `Idle`, `Locomotion`, `Sprint`, `Airborne`, `Attack`, `Block`, `Parry`, `Dodge`, `Stagger`, `Traversal`, `Interaction`, `Cinematic`, `Death`. Each state declares allowed transitions, input acceptance mask, and movement mode overrides in a data table (`DT_StateRules`) so tuning is authorable and testable.

### 4.2 Player kit (combat contract, before any animation exists)

The player kit is fixed here so AI, animation and UI can be built against it. It is a *technical* specification of inputs and outcomes; it does not invent new visual moves.

| Input | Behaviour | Timing contract (tunable defaults) |
|---|---|---|
| Light attack | 4-hit chain, root-motion driven | Cancel to dodge from frame after active; chain window 0.15–0.45 s after active start |
| Heavy attack | Slower, posture-breaking, committed | No dodge cancel after commit point unless hit-confirm |
| Block | Raises guard, reduces damage, costs posture | Guard-ready in 0.08 s; guard break at posture 0 |
| Parry | Tight window inside block input | Window 0.15 s from press; success = attacker stagger, no damage |
| Dodge | Directional step/roll, i-frames | i-frames 0.10–0.45 s of clip; stamina cost |
| Lock-on | Soft/hard target lock, camera framing | Toggle and hold modes both supported |
| Sprint | Boost locomotion, no combat | Cancel into attack (dash attack) or slide |
| Interact | Contextual action | Hold variants for heavy objects |
| Aim/thrown weapon | **Not in baseline.** Only if a weapon-register decision adds it | — |

Every value above is a default to be tuned with the Creative Director; all live in data, not code.

### 4.3 Camera

- Third-person spring-arm rig; shoulder offset per stance; collision-aware boom (probe size tuned for tight interiors in Nneka's house).
- `UTDDCameraRigComponent` blends between rigs by state: exploration, combat (wider, further, target-biased), lock-on (framing both player and target with screen-space bias), traversal, cinematic (Sequencer takeover), death.
- Lock-on: target selection scoring = screen-centre angle + distance + visibility + threat; hysteresis to prevent target flicker; break on line-of-sight loss with a grace period.
- Shake: camera modifiers driven by data assets (`DA_CameraShake_*`), never hard-coded curves in code.
- FOV: base 90° horizontal; combat 95°; no ADS. Overridable per-rig.
- Cinematics own the camera absolutely; gameplay rigs restore with a 0.4 s blend.
- Accessibility: camera shake scale, motion blur toggle, FOV slider, camera-assist strength (all in Section 12).

### 4.4 Traversal and exploration

Grounded traversal only in the vertical slice: vault, mantle, ledge shimmy, drop, climb-ladder. Built as: forward/down trace detects candidate → `FTDDTraversalCandidate` (type, heights, entry/exit transforms) → validated against capsule clearance and slope → montage with `UMotionWarpingComponent` aligning start/end → state machine locks input → exit.

Rules: no traversal without a validated exit; failed validation returns "no prompt" rather than a broken animation; all traversal montages authorable per-type so an animator can add without code.

### 4.5 Interaction

`ITDDInteractable` (Core) exposes: `GetInteractionPrompt`, `CanInteract`, `BeginInteract`, `TickInteract` (hold progress), `EndInteract`, `CancelInteract`, plus an optional `FTDDInteractionRequirements` (flags/tags the player must have). Implementations: memory fragment anchor, door, lever, dialogue partner, pickup, checkpoint shrine, lore object.

Focus resolution: nearest valid interactable within a forward cone, scored by distance + facing + priority, with camera-facing bias. Prompt text comes from a String Table; the verb comes from a `FGameplayTag` so localisation and iconography are data.

### 4.6 Game flow and states

```
Boot -> MainMenu -> (Continue | NewGame) -> ChapterLoad -> Gameplay
Gameplay <-> Pause
Gameplay -> Cinematic -> Gameplay
Gameplay -> PlayerDied -> CheckpointRespawn -> Gameplay
Gameplay -> EndingSequence -> Credits -> MainMenu
```

`UTDDGameFlowSubsystem` (GameInstance) is the only writer of flow state. Input suppression, UI stack, save points and cinematic blending all key off it. Death → checkpoint respawn restores world state from the last checkpoint, **not** from the last save file, and must not lose discovered memories (memories persist on discovery — they are knowledge, not items).

---

## 5. Character and combat architecture

### 5.1 Attributes and the ability backend (ADR-0004)

GAS is used for **attributes, modifiers, cooldowns and status effects** only. Reasons: it gives us replication-free, well-tested attribute maths, modifier stacking, duration effects, immunity/blocking tags, and a standard way to express buffs/debuffs that progression will need. Attack *flow* is **not** implemented as GAS abilities: melee timing, cancel windows and hit resolution need frame-precise, simply-debuggable control and are better served by our own state machine. This split is deliberate and documented so no agent re-litigates it mid-production.

| Component | Detail |
|---|---|
| `UTDDAttributeSet` | Health, MaxHealth, Posture, MaxPosture, PostureRegen, Stamina, MaxStamina, StaminaRegen, DamageMultiplier, DefenseMultiplier, MoveSpeedScale |
| Attributes changed via | `UGameplayEffect` only. Direct float writes are a code-review rejection. |
| Status tags | `Status.Blocking`, `Status.Parrying`, `Status.Invulnerable`, `Status.Staggered`, `Status.Attacking`, `Status.Grabbed`, `Status.Cinematic` |
| Immunity/blocking | `FGameplayTagContainer` on ASC; e.g. a dodge grants `Status.Invulnerable` for its i-frame window |

### 5.2 Attack data model

`UTDDAttackDefinition` (`UPrimaryDataAsset`):

| Field | Type | Purpose |
|---|---|---|
| `AttackId` | `FName` | Stable identifier used by AI and animation |
| `Montage` | `TSoftObjectPtr<UAnimMontage>` | Root-motion attack clip |
| `DamageType` | `FGameplayTag` | `Damage.Physical.Slash` etc. |
| `BaseDamage`, `PostureDamage` | `float` | Scaled by attributes |
| `StaminaCost` | `float` | Denied if insufficient |
| `HitWindowNotifies` | Implied by montage notifies | `ANS_TDDHitWindow` authoring, not a float here |
| `CancelRules` | `FTDDCancelRules` | What cancels what, at which phase |
| `HitStop` | `FTDDHitStopSpec` | Attacker/victim ms, scaled by hit type |
| `HitReactionTable` | `TSoftObjectPtr<UDataTable>` | Directional reaction selection |
| `CameraShake` | `TSoftObjectPtr<UCameraShakeBase>` | Feedback |
| `TargetingWarp` | `FTDDWarpSpec` | Max warp distance/angle, motion-warp target |
| `AudioSet` | `FTDDAttackAudioSet` | Swing/impact/whiff MetaSounds |
| `UnlockCondition` | `FTDDCondition` | Progression gating (combination unlocks) |

Hit windows are **animation notifies** (`UAnimNotifyState_TDDHitWindow`), not data floats: the attack's active frames belong to the clip that shows them. This prevents the classic desync where data says "hits at 0.3s" and the animation hits at 0.45s.

### 5.3 Hit detection

```
ANS_TDDHitWindow::NotifyBegin -> CombatComponent opens window with trace spec
each tick during window:
  sweep from weapon socket (previous frame position) -> current
  capsule sweep radius from attack spec, substepped if linear speed > threshold
  collect overlaps, filter: owner, friendlies (tag), already-hit this attack instance,
                            targets behind a blocking wall, invulnerable targets
  classify each hit -> FTDDAttackHitOutcome
ANS_TDDHitWindow::NotifyEnd -> close window, clear dedup set
```

Classification outcomes: `Miss`, `Hit`, `Blocked`, `Parried`, `WeakPoint`, `KillingBlow`, `Immune`, `OutOfRange`.

Determinism requirement: hit resolution is `O(hits × substeps)` with a hard cap per window; the dedup set is per attack *instance*, cleared on window close, so one swing cannot double-hit one enemy. These rules are unit-testable with a stub world (Section 14, `TDD-Unit.Combat.HitDedup`).

### 5.4 Damage pipeline

```
Attacker CombatComponent
  -> FTDDAttackHitOutcome
  -> FTDamageRequest { InstigatorId, TargetId, RawDamage, DamageType, HitLocation,
                       OutcomeType, bCritical, SourceAttackId }
  -> ITDDDamageable::ApplyDamage(FTDDamageRequest)   [Core interface]
     -> victim's UTDDCombatComponent (or boss/AI controller for non-pawn damageables)
        -> if Blocked: reduce by guard, drain posture
        -> if Parried: apply attacker stagger, no health loss
        -> else: GAS GameplayEffect (damage) -> AttributeSet -> OnHealthChanged
        -> posture damage -> posture break check -> Staggered state
        -> hit reaction montage selection (direction = hit vector vs facing)
        -> hitstop request, VFX, audio, camera shake, haptics
        -> if health <= 0: death flow (ragdoll optional, AI notify, loot, events)
  -> FTDDDamageAppliedEvent published on the bus
```

All numbers are scaled by attribute multipliers so difficulty/progression adjusts in one place. Damage numbers are never presented in the UI (visual language decision; not a mechanic).

### 5.5 Reaction, stagger and hitstop

- **Hit reactions:** `FTDDHitReactionEntry` rows keyed by (direction, severity, stance). Missing row → fallback to a default flinch and a logged warning; never silence.
- **Stagger:** posture break opens a stagger window; during it, all incoming damage is multiplied and a riposte/execution prompt may appear (if the target is eligible). Stagger is cancellable by the boss framework only via defined transitions.
- **Hitstop:** `UTDDHitStopSubsystem` applies a scaled time dilation to the *pair* of actors (not global world time) for a spec'd duration, stacking with diminishing returns, and always expiring deterministically. Global time dilation is reserved for cinematics and death, so a hitstop can never corrupt a cinematic's timing.
- **Death:** two legitimate presentations (ragdoll via Chaos, or authored death montage). Choice is per-archetype data. Player death always uses an authored sequence, not ragdoll (camera control and readability).

### 5.6 Enemy contact and player defence

- Enemy attacks use the same attack pipeline as the player — one damage path, no "enemy special case".
- Blocking: guard state reduces damage by a data-defined fraction and applies posture damage; guard break staggers.
- Parry: a successful parry against an attacker with `Attack.Parryable` tag causes attacker stagger and opens a counter window. Non-parryable attacks (unblockable, telegraphed with a distinct visual/audio cue) must be consistently identified by a tag so UI/audio can warn the player without bespoke code per attack.

### 5.7 Progression hooks (engineering only)

The combat layer exposes: unlocked attack definitions, attribute growth curve application, armour/weapon stat modifiers, and combination unlocks. **No progression content is invented here.** Which upgrades exist, their names and costs, and whether an upgrade economy exists at all are Creative Director decisions still open (Section 17). The subsystem is built so that "no progression beyond chapter rewards" is also a valid configuration.

---

## 6. World and environment architecture

### 6.1 Chapter and level topology

One persistent level per chapter, World Partition enabled, plus dedicated sublevels for boss arenas and cinematics:

```
Content/TDD/Environments/CH01_ForbiddenForest/
  L_CH01_ForbiddenForest_P           (persistent, World Partition, cells 256m)
  L_CH01_Boss_GreatRootMother        (streamed sublevel, arena)
  L_CH01_Cin_Intro                   (streamed, Level Sequence host)
  DA_CH01_ChapterDefinition
```

Rules:
- Persistent levels hold no gameplay logic beyond the chapter definition reference; logic lives in systems.
- Boss arenas are separate sublevels so they can be loaded/unloaded independently and iterated without touching exploration cells.
- Cinematic sublevels are never cooked into shipping builds with debugging geometry.
- Level name ↔ location register ID mapping is stored in `DA_CH01_ChapterDefinition` using the Art Bible's identifiers (`CH01-ENV-001`, `CH01-BOS-001`, …). Engineering does not invent location IDs; unmapped scenes are logged as `PENDING_REGISTER` and are not allowed to ship.

### 6.2 World state, time and weather (OAD-24 compliant)

Time-of-day and weather are **environment states of a parent location**, not locations. Implementation: `UTDDWorldStateSubsystem` holds a state set (`Time.Dawn`, `Time.Day`, `Time.Dusk`, `Time.Night`, `Weather.Clear`, `Weather.Rain`, `Supernatural.BoundaryThin`), each mapped to a Data Layer + lighting/audio/VFX parameter set. States are saved per-location in the save file. Supernatural variants are gated by narrative flags (e.g. `Supernatural.BoundaryThin` only after the Hollow King's interference is established).

This design is the direct engineering expression of OAD-24 and prevents the common failure of duplicating levels per lighting mood.

### 6.3 Streaming, loading and checkpoints

- World Partition with HLOD layers (2 levels: distant terrain/settlement silhouette, mid-detail architecture) generated per chapter.
- Chapter transition: async load of the next persistent level with a loading screen (data-driven art + tips from a String Table), minimum display time 1.5 s to avoid flicker, hard timeout 30 s with a logged, surfaced error rather than an infinite black screen.
- Checkpoints: `ATDDCheckpointVolume` (or narrative-driven checkpoint event) serialises `FTDDWorldSnapshot` (location, transform, world-state set, encounter completion flags, defeated-entity IDs) plus the GameInstance narrative store.
- Streaming source management: player is a World Partition streaming source; cinematics add a temporary source so a camera move never outruns streaming (a classic cinematic pop). This is validated by an automated check that every Level Sequence camera key has its region loaded (Section 14).

### 6.4 Navigation and gameplay volumes

- `ANavigationData` via `RecastNavMesh` with dynamic generation limited to encounter footprints (never whole-chapter dynamic nav — a performance trap).
- Named nav query areas for: `NavArea.Combat`, `NavArea.Stealth`(if stealth exists — currently not specified), `NavArea.NoSpawn`.
- Gameplay volumes are explicit actors with editor visualisers: `ATDDEncounterVolume`, `ATDDCheckpointVolume`, `ATDDArenaBounds`, `ATDDMemoryAnchorVolume`, `ATDDCombatRestrictionVolume` (e.g. no combat in Nneka's house), `ATDDTraversalVolume`.
- Every volume has `bEnabledInBuild` and a debug colour; a cook validator fails the build if a volume has zero references and no debug purpose.

### 6.5 Environment interaction

Interactive props implement `ITDDInteractable` and are *authored as data-linked actors*, not hard-coded level Blueprints, so the same door/lever/keeper can be reused across chapters with different flags. Destructibles use Chaos destruction only where the Creative Director's design calls for it (none approved yet) — architecture supports it via a `ITDDDestructible` extension point but no system is built speculatively.

### 6.6 Chapter production pipeline (repeatable, per chapter)

1. Chapter definition data asset created from the Art Bible register (locations, scenes, boss, memories).
2. Blockout at true scale in the persistent level + sublevels, using `SM_Blockout_*` primitives (1 m grid, 2.7 m door, 0.45 m step — fixed module constants shared with animation).
3. Encounter and checkpoint placement; navmesh; streaming sources; time/weather states.
4. Boss arena integration against `TDDBossDefinition`.
5. Memory anchor placement (one per chapter, Chapters 1–7 only).
6. Cinematics and dialogue hooks.
7. Optimisation pass (Nanite/HLOD/VSM budgets), then perf gate.
8. Chapter acceptance test (Section 14, Tier 3).

This pipeline is the "chapter factory". Chapter 1 is the pilot; no other chapter starts until Chapter 1 passes its gate.

---

## 7. AI and NPC architecture

### 7.1 Layers

| Layer | Component | Purpose |
|---|---|---|
| Perception | `UAIPerceptionComponent` + sight/hearing/damage configs | Sensing player and world events |
| Decision | `UStateTreeAIComponent` with per-archetype StateTree | Behaviour selection |
| Combat decision | `UTDDCombatBrainComponent` | Choose attack from archetype's attack set |
| Execution | GAS-free action driver + animation montages | Play chosen action |
| Coordination | `UTDDCombatDirectorSubsystem` | Attack tokens, spacing, simultaneous attackers |
| Encounter | `UTDDEncounterManager` | Spawn waves, leash, completion, rewards |
| Boss | `UTDDBossComponent` + `UTDDBossDefinition` | Phases, sequences, arena constraints |

### 7.2 Enemy archetypes

`UTDDEnemyArchetype` (`UPrimaryDataAsset`): display ref (Art Bible character ID or `PENDING_REGISTER`), attributes, attack set, movement profile (speed, turn rate, preferred range, strafe bias), reaction table, death behaviour, loot table (may be empty), spawn cost, tags (`Enemy.Type.Brute`), and `bIsBoss`.

Archetype variants are data. A new enemy = new data asset + animation set; no code. This is a hard architectural requirement so that later chapters do not require engineering to add factions.

AI archetypes named in the directive (Great Root Mother, Iron Elephant, King Without a Face, Daughter of the Deep, Amadioha's Champion, Mother of Masks, Hollow King) are **bosses, not archetypes invented here**. Their mechanics are not yet specified by the Creative Director and must not be invented. The framework supports them; the content is gated on design.

### 7.3 Combat director (why it exists)

Left alone, UE AI produces the "everyone attacks at once" failure that makes third-person action games feel unfair. `UTDDCombatDirectorSubsystem`:

- Grants a limited number of **attack tokens** (default 1 attacker + 1 "approach" slot + 1 ranged slot for a normal group).
- Enforces **spacing**: non-token holders circle at a preferred radius, with a minimum angular separation.
- Enforces **aggression cooling**: after a token holder's attack resolves, it cannot re-take a token for `X` seconds unless it is the only enemy left.
- Honours **telegraph fairness**: an attack whose wind-up is below a threshold requires the player to be free (not staggered, not in a committed recovery) or it is deferred.
- Is deterministic under test: `FTDDAttackTokenPolicy` is a pure function of (candidates, current tokens, time) and is unit-tested.

### 7.4 Boss architecture

`UTDDBossDefinition`: ordered `FTDDBossPhase` array. Each phase has:
- entry condition (health fraction, or narrative flag),
- allowed attack set with weights, cooldowns, per-phase combo rules,
- arena constraint set (bounds, hazards, phase-transition animation),
- cinematic hooks (intro, phase transition, death),
- `bInvulnerableWindows` (e.g. transition), explicitly data-authored.

Runtime: `UTDDBossComponent` owns phase state, health threshold transitions (debounced so 2 hits cannot double-trigger), attack selection, and a `FTDDBossEventLog` for debugging and test assertions. Phase transitions are atomic: no attack can be triggered during a transition; the state machine refuses and logs.

**Testability contract:** `FTDDBossPhaseSelector::Select(Definition, PhaseIndex, Context)` is a pure function returning an attack ID, tested with a seeded RNG over 10,000 draws to assert weights, cooldown exclusion, and "never select an attack outside the phase". This is how we get boss reliability without playing the game a thousand times.

### 7.5 NPC and world simulation

- Villagers/ambient NPCs: lightweight `ATDDNPCCharacter` with a StateTree for routine behaviour (wander, work, react), no combat brain, no GAS attributes beyond a stub. Budget: ≤ 40 active NPCs per scene, ≤ 2 ms game-thread total (measured, not assumed).
- Daily routine: tick-rate-limited, schedule from a `UDataTable` per settlement; schedule only advances while the player is in the settlement.
- Reaction to player: distance-based acknowledgement, never pathfinding to the player across the world.
- Combat restriction volumes prevent NPCs entering arenas.
- OAD-55 (villager clothing standard) is a *content* constraint: NPC archetypes reference approved dress data; engineering enforces "no bare-chest default" only as a data-validation warning, because it is a visual standard owned by art.

### 7.6 Navigation and performance guards

- Max active pawns with navmesh pathfinding per encounter: 12 (configurable). Beyond that, spawn logic defers.
- AI tick budget: perception updates staggered across frames (round-robin, 5-frame cadence); StateTree tick rate set per archetype (default 0.1 s idle / 0.0 s in combat).
- No `Tick` on AI actors that can be event-driven; every `Tick` requires a comment justifying it (code review rule).

---

## 8. Animation architecture

### 8.1 Layers

| Layer | Technology | Owns |
|---|---|---|
| Locomotion | Motion Matching (Pose Search) + Chooser | Idle/walk/jog/sprint/strafe, turn-in-place, stops, starts |
| Combat | Anim montages driven by `UTDDCombatComponent` | Attacks, hit reactions, dodges, blocks, parries |
| Traversal | Montages + Motion Warping | Vault, mantle, shimmy, ladder |
| Facial / dialogue | Control Rig + MetaHuman rigs (when characters exist) | Memory scenes, dialogue |
| Procedural | Control Rig foot IK, look-at, weapon grip | Ground adaptation, aiming head/torso, hand placement |
| Cinematics | Sequencer + (optionally) Take Recorder | Chapter cutscenes |

### 8.2 Motion Matching maturity caveat (honest risk)

Motion Matching through Pose Search is the right technology for the God-of-War-class locomotion the brief asks for, but it requires a **large, well-tagged animation corpus** that does not exist yet, and its 5.8 status must be confirmed on the production workstation. ADR-0005 therefore specifies:

- Build the locomotion component against an `ITDDLocomotionAnimProvider` interface with two implementations: `UTDDMotionMatchingProvider` and `UTDDBlendSpaceProvider` (state machine + blendspaces).
- Ship-path selection is a project setting. If the corpus is not ready by the end of Stage 3, the blend-space provider keeps the game playable and the switch is one config value — no system rewrite.
- Whichever provider is active is printed in the debug HUD and asserted by an automation test, so no one can claim motion matching is in place while a blendspace is playing.

### 8.3 Animation notify contract (the code↔animation interface)

Animators may only communicate with gameplay through these notifies; ad-hoc notifies calling gameplay code are rejected in review.

| Notify | Type | Meaning |
|---|---|---|
| `ANS_TDDHitWindow` | NotifyState | Attack active window; carries `FName HitSpecId` |
| `ANS_TDDIFrameWindow` | NotifyState | Invulnerability window |
| `ANS_TDDParryWindow` | NotifyState | Parry acceptance window |
| `AN_TDDAttackCommit` | Notify | Point after which the attack cannot be cancelled |
| `AN_TDDComboWindowOpen/Close` | Notify | Chain input acceptance |
| `AN_TDDMotionWarpTarget` | Notify | Warp target evaluation point |
| `AN_TDDFootstep` | Notify | Footstep audio/surface event |
| `AN_TDDWeaponTrace` | Notify | Weapon trail VFX on/off |
| `AN_TDDEffectCue` | Notify | Generic Niagara/MetaSound cue by tag |
| `AN_TDDCameraShake` | Notify | Named shake asset |
| `AN_TDDSpawnProjectile` | Notify | Ranged attacks (if approved) |

Naming and payloads live in `docs/01_ARCHITECTURE/CODING_STANDARDS.md` §Animation.

### 8.4 Retargeting and budgets

- Skeleton: one shared humanoid skeleton for Adanna, Ezeani, Nneka, humans NPCs (IK Rig + retargeter chains), with a separate boss skeleton for non-humanoid bosses. Shared skeleton means one animation set can serve all humans; unique characters get additive/pose overrides, not duplicated sets.
- Bone budget: ≤ 180 bones for gameplay characters (facial via separate LOD/curve), ≤ 300 for bosses.
- LODs: 4 for named characters (LOD0 60k tris → LOD3 8k, bones reduced at LOD2+), 3 for NPC crowds.
- Anim update: `URO` (Update Rate Optimisation) enabled for NPCs and distant enemies; never for the player or the currently-attacking enemy.
- Animation memory budget per encounter: ≤ 120 MB.

### 8.5 Cinematic animation

Sequencer-driven, with gameplay disabled but visible (player input suppressed, not teleported into a dummy). The cinematic subsystem cross-fades from gameplay camera to cine camera over 0.4 s; the camera is never cut hard on entry unless the sequence's first shot is authored as a cut. Skippable sequences must leave world state consistent — the skip handler runs the same "post-cinematic state application" code path as normal completion (this is tested).

---

## 9. Progression and narrative architecture

### 9.1 Design rule

Narrative systems are **mechanisms**, not content. Engineering builds the ability to express quests, memories, flags, conditions and endings; the Creative Director and Technical Director supply what they contain. Anything not supplied is a named placeholder (`PENDING_CONTENT_<domain>_<n>`), visible in the debug overlay and in the content audit report.

### 9.2 Flags, counters and conditions

- `FGameplayTag` flag store (`UTDDNarrativeSubsystem`): boolean flags (`Narrative.Memory.03.Found`, `Narrative.Chapter.04.Completed`, `Narrative.Nneka.TruthKnown`), and integer counters (`Counter.EnemiesKilled.*`, `Counter.MemoriesFound`).
- `FTDDCondition`: a small, serialisable, *composable* condition tree — `HasFlag`, `NotFlag`, `HasCounterAtLeast`, `ChapterCompleted`, `MemoryFound`, `AllOf`, `AnyOf`, `NoneOf`. Evaluated by a pure function, fully unit-tested. This is intentionally not a scripting language: no agent or designer should be able to write unbounded logic into content.
- Persisted in the save file with stable tags (tags are content-stable identifiers; renaming a tag is a save-migration event).

### 9.3 Quest system

`UTDDQuestDefinition` (`UPrimaryDataAsset`): id, title/description string-table keys, ordered `FTDDQuestStep[]` (each with condition, optional world marker, completion event, next step), states `Inactive → Active → StepComplete → Completed / Failed`. No branching dialogue graph in v1 — dialogue is sequence + choice presentation, not a node editor (that would be premature abstraction for a game whose dialogue system is not yet specified).

`UTDDQuestSubsystem` evaluates steps on relevant events (not on tick), and is a pure state machine over conditions. Tested with scenario tables (`TDD-Unit.Narrative.QuestFlow`).

### 9.4 The seven memories (OAD-32 compliant)

Architectural contract:

| Requirement (from OAD-32) | Implementation |
|---|---|
| One hidden memory in each of Chapters 1–7 | `UTDDMemoryFragment` records with `ChapterId` 1–7; validation fails if a chapter has 0 or >1 |
| Found only by exploration | Anchors are `ITDDInteractable` world objects placed off the critical path; there is no quest marker, no map icon, no prompt until the player is within focus range |
| Met as fragments (place, object, sound, interaction), **not** collectible cutscenes | Fragment presentation types enum: `Place`, `Object`, `Sound`, `Interaction`. Presentation is a short authored moment in-world (camera restraint, audio cue, brief overlay), **not** a full cinematic. The enum drives the presentation component used |
| Each reveals something different, distinct visual identity | Per-memory data asset holds its own VFX/audio/lighting set reference |
| A coherent sequence; missing one closes Ending 3 only | Memories are independent for discovery, ordered for *understanding*; the journal shows recovered fragments in order 1–7 with gaps visible |
| Last memory changes the meaning of the confrontation | Flag `Narrative.Memory.07.Found` is read by the ending resolver and by Ezeani-confrontation dialogue conditions |

`UTDDMemorySubsystem` exposes `FoundCount()`, `IsFound(MemoryId)`, `AllFound()`, and publishes `FTDDMemoryDiscoveredEvent`. Discovery is idempotent; a duplicate discovery logs and does nothing. It is persisted immediately on discovery (so a crash after discovery does not erase it) — an explicit, tested exception to checkpoint-only saving.

**Content status:** the specific content of all seven memories is `PENDING APPROVAL` per OAD-32/OAD-34. Memory 7's *truth* is approved in principle (OAD-34), but the sequence, events and dialogue are not. The system above ships with placeholder presentation assets and a content audit listing all seven as `PENDING_CONTENT`.

### 9.5 Endings

```
ETDDEnding { Kill, Spare, Hidden }
Inputs: bConfrontationResolved, bChoseKill, bAllSevenMemories
Resolver: pure static function, single source of truth
```

Rules encoded in the resolver:
- `Kill` and `Spare` are always available at the confrontation (no morality gating) — the decision is the player's, not a score's.
- `Hidden` requires all seven memories (OAD-32) **and** the confrontation resolution path that leads to it; the resolver refuses `Hidden` otherwise and logs why.
- The resolver returns an ending ID only. It does not decide consequences, epilogue content or environment treatment (OAD-23 content is open). `FTDDEndingReachedEvent` triggers a content asset lookup by ID.
- OAD-34 constraint enforced by *absence of mechanism*: there is no "absolution" flag, no morality meter, no outcome inversion based on truth knowledge. A unit test asserts the resolver ignores `bTruthKnown`.

### 9.6 Cinematics, dialogue, localisation

- Cinematics: `LS_<Chapter>_<Beat>` Level Sequences, played by `UTDDCinematicSubsystem`; skippable flag per sequence; skip path applies the same completion handler as natural end.
- Dialogue: voice playback via MetaSound/`UAudioComponent` with subtitle events; all lines from String Tables keyed `TDD.<Chapter>.<Scene>.<LineId>`. Text is never hard-coded in C++ or Blueprints.
- Localisation: UE localisation pipeline, `LOCTEXT`/String Tables, target languages **undecided** (open question), but no string may ship unlocalisable. Pseudo-localisation test in CI.
- Voice direction and Nneka-voice representation (OAD-39) are content decisions; the audio system adds no "ghostly echo" processing by default because that would imply presence.

### 9.7 Codex / journal

`UTDDJournalSubsystem` aggregates: recovered memories (with gaps), quest state, discovered locations, bestiary entries (unlocked on kill), and codex lore. Each entry carries its canon reference (Art Bible asset ID or narrative decision ID) and a **cultural status tag** — see Section 9.8. Entries are data assets; no code change to add lore.

### 9.8 Cultural integrity mechanism (engineering support for a creative constraint)

The directive states invented mythology must never be presented as authentic Igbo tradition. Engineering cannot police that editorially, but it can make the distinction structural:

`ETDDCulturalStatus` on every lore/codex/visual data asset:
- `Fictional_Original` — invented for the game (default for the Hollow King, the boundary work).
- `Inspired_RequiresConsultant` — draws on real practice/belief; cannot pass the shipping content audit without a consultant sign-off record ID.
- `Documented_Real_RequiresSignoff` — depicts a real, documented practice; requires consultant sign-off record ID and a codex attribution line.

The editor validator fails Shipping cook if any `Inspired_*` or `Documented_*` asset lacks a valid sign-off record. The Art Bible's `CULTURAL_REFERENCE_GUIDE.md` currently reads "Needs consultant review", and OAD-03/04/06/07 are open — so this gate is not hypothetical, it is already blocking final content. Engineering implements the gate; the Creative Director decides the content.

---

## 10. Data structures and persistence

### 10.1 Data asset catalogue

| Asset type | Base | Count driver |
|---|---|---|
| `UTDDChapterDefinition` | PrimaryDataAsset | 8 |
| `UTDDLocationRecord` | PrimaryDataAsset | per location register entry |
| `UTDDMemoryFragment` | PrimaryDataAsset | 7 |
| `UTDDQuestDefinition` | PrimaryDataAsset | content-driven |
| `UTDDAttackDefinition` | PrimaryDataAsset | per attack |
| `UTDDEnemyArchetype` | PrimaryDataAsset | per enemy |
| `UTDDBossDefinition` | PrimaryDataAsset | per boss (7 named + Hollow King encounter = 8) |
| `UTDDWeaponDefinition` | PrimaryDataAsset | **exactly 1** (Adanna's approved blade) until a weapon register approval adds more |
| `UTDDArmourDefinition` | PrimaryDataAsset | base + upgraded set (OAD-10) |
| `UTDDDialogueSet` | PrimaryDataAsset | per scene |
| `UTDDCodexEntry` | PrimaryDataAsset | per entry |
| `UTDDAudioCueMap` | PrimaryDataAsset | per chapter |
| Data tables | `UDataTable` | state rules, hit reactions, schedules, loot |

All primary assets are registered with `UAssetManager` under primary asset types (`Chapter`, `Memory`, `Enemy`, `Boss`, `Attack`, …) so they can be asynchronously loaded and cooked selectively, and so the editor validator can enumerate them exhaustively.

Every content asset embeds:

```cpp
UPROPERTY(EditDefaultsOnly, Category="Canon")
FTDDCanonReference CanonRef;   // ArtBibleAssetId, DecisionId, ETDDCanonStatus, ETDDCulturalStatus
```

`ETDDCanonStatus { Approved, PendingApproval, Proposed, Exploratory, Rejected }`. Shipping validators (ADR-0008) fail the cook if a narrative-critical asset (chapter, memory, boss, character, weapon) is not `Approved`, or if a `Rejected`/`Exploratory` asset is referenced by anything in a shipping map.

### 10.2 Save data schema

```
USaveGame (USaveGame subclass: UTDDSaveGame)
└── FTDDSaveHeader
      SchemaVersion (int32), BuildVersion (FString), Timestamp (FDateTime),
      ChapterId (FName), PlaytimeSeconds (double), SlotKind (enum), Checksum (uint32)
└── Sections (registered by modules through ITDDSaveProvider)
      NarrativeSection  (flags, counters, quest states, memories, ending choices)
      PlayerSection     (transform, health/stamina state, unlocked attacks, equipment)
      WorldSection      (per-location world-state sets, defeated entity IDs,
                         encounter completion, checkpoint id, opened interactables)
      SettingsSection   (gameplay/accessibility settings — local, not slot data)
```

Rules:
- **Versioned, additive-only** changes within a schema version; any structural change increments `SchemaVersion` and adds a migration function. Migration chain is explicit (`Migrate_1_2`, `Migrate_2_3`, …) and unit-tested with real captured save blobs.
- **Atomic writes**: serialise to memory → write `.tmp` → verify read-back → rename over `.sav`, keeping one `.bak`. A crash mid-save must never destroy the previous save. Test: simulate interruption, assert previous save loads.
- **Corruption handling**: checksum mismatch or schema newer than build → load fails gracefully with a user-facing message and preserves the file; never silent reset.
- **Slots**: `Auto` (rotating, 2 deep), `Checkpoint` (single), `Manual` (3). Save-scumming policy is an open design question; the architecture supports either.
- Discovery of a memory writes immediately (Section 9.4) as an explicit, documented exception.

### 10.3 Runtime state vs saved state (explicit boundary)

| State | Lives in | Saved | Notes |
|---|---|---|---|
| Narrative flags/counters | `UTDDNarrativeSubsystem` | Yes | Stable tags |
| Memory discoveries | `UTDDMemorySubsystem` | Yes, immediately | Cannot be lost on death |
| Encounter completion | `UTDDEncounterManager` | Yes (world snapshot) | Restored on checkpoint |
| Defeated bosses | `UTDDWorldStateSubsystem` | Yes | Never respawn unless design says otherwise |
| Time/weather per location | `UTDDWorldStateSubsystem` | Yes | OAD-24 |
| Player transform | Checkpoint snapshot | Yes | Respawn position |
| Camera, VFX, transient AI state | Runtime only | No | Reconstructed |
| Combat combo counters | Runtime only | No | Reset on load |

### 10.4 UUIDs and entity identity

Stable identity for world actors comes from **level-placed GUIDs** (`ActorGuid` from World Partition), not from array indices or names. Save records reference `FGuid`; a renamed actor keeps its GUID, so renaming a door cannot corrupt a save. Runtime-spawned entities (AI waves, projectiles) are *not* saved individually — their spawner and wave index is, and they are reconstructed on load.

---

## 11. Audio and feedback architecture

### 11.1 Approach

MetaSounds + Sound Concurrency + Submixes, no middleware (ADR-0009). Justification: no audio design exists yet to justify middleware integration cost; MetaSounds covers the design needs of a single-player action game (procedural layers, parameter-driven combat impacts, Quartz-synced rhythmic cues for Chapter 7's drums); the decision is reversible behind an `ITDDAudioService` interface if the audio director later requires Wwise.

### 11.2 Structure

| Layer | Detail |
|---|---|
| Mix | Master → Music / SFX / Dialogue / Ambience / UI submixes; sidechain duck on dialogue; loudness target per platform (documented at mix stage) |
| Combat | Attack swings layered by speed, impacts by surface + material + severity, weapon body resonance; hitstop duck |
| Ambience | Per-location ambience beds driven by `FTDDLocationEnteredEvent` and world-state sets (rain, night) |
| Music | Chapter themes + boss state-driven layers; transitions on boss phase (data, not hard-cut) |
| VO | Dialogue from String-Table-keyed lines, subtitle events, no positional reverb tail that implies presence for Nneka (OAD-39) |
| Spatial | Attenuation per asset class; occlusion on for combat-critical audio only (perf) |
| Rhythm | Quartz clock for Chapter 7's Gathering Ground drums (OAD-44-adjacent content) so player actions can land on the beat |

### 11.3 Feedback budget

Every damage event must produce, within one frame: impact VFX, impact audio, camera response, haptic (if controller). Losing any one of these is a bug, not a polish item — a `TDD-Functional.Combat.FeedbackComplete` test asserts the VFX/audio components received a cue for a scripted hit.

---

## 12. UI, UX, localisation and accessibility

- **Framework:** Common UI with a single root layout; UI never queries gameplay internals — it reads `TDDCore` events and view models.
- **HUD:** health, posture/stamina, active memory count (as recovered fragments, not "3/7 collectible" icons — content decision honoured), enemy indicators for off-screen threats (limited), interaction prompt, lock-on reticle. Minimal by design.
- **Menus:** pause, settings (graphics, audio, controls incl. full rebinding), accessibility, journal/codex, chapter select (if approved), credits.
- **Accessibility baseline (engineering proposal, needs CD approval):** remappable controls; hold↔toggle for block/interact; camera shake scale 0–100%; FOV slider; motion blur off; subtitle size/background/speaker labels; colourblind-safe UI palette (Lumen-lit scenes are not colourblind-adjustable, so gameplay-critical cues must not rely on colour alone — a validation rule on marking up cues); difficulty options are a design question (not built, not assumed); no quick-time events required to progress (if the design calls for them, they get an alternate input option).
- **Performance:** UI budget ≤ 1.0 ms CPU and ≤ 40 draw calls; no per-frame widget tree rebuilds; view-model updates event-driven.
- **Localisation:** all strings from String Tables; no concatenation; pseudo-loc CI test; fonts must ship with the needed glyph coverage (Igbo diacritics: ị, ọ, ụ, ṅ — a font-coverage test is required before shipping any Igbo text).

---

## 13. Inter-agent interfaces

### 13.1 Ownership matrix

| Area | Owns | May read but not modify |
|---|---|---|
| **AGENT 1 — Gameplay, Character & Combat** | `TDDGameplay` (player character, camera, input, combat, weapon, interaction, traversal, state machine), player-facing combat UI, combat animation notify implementation | `TDDAI` internals, `TDDWorld`, `TDDNarrative` |
| **AGENT 2 — World, Systems, Environment & Simulation** | `TDDWorld`, `TDDAI`, `TDDNarrative` (quests, memories, endings, cinematics), encounter/arena framework, NPC simulation, environment gameplay volumes | `TDDGameplay` internals (uses public components only) |
| **AGENT 3 — Integration, Technical Quality, Build & Performance** | `TDDCore` (shared contracts, events, persistence, canon registry), `TDDUI` framework, `TDDEditor` validators, CI, packaging, profiling gates, `TDDTests` | All runtime modules' internals — integration fixes must be negotiated, not silently applied |

`TDDCore` is owned by Agent 3 because it is the shared contract surface; **any change to a `TDDCore` interface, event or save struct requires a change request** (Section 13.3) regardless of which agent proposed it.

### 13.2 Frozen public surfaces (the actual contracts)

Agent 1 publishes to the others (all in `TDDGameplay/Public`):

```cpp
// Victim-side extension of the Core damage interface
class ITDDCombatant
{
    virtual FGuid GetEntityId() const = 0;
    virtual bool IsAlive() const = 0;
    virtual ETDDCombatState GetCombatState() const = 0;
    virtual void ApplyStagger(float DurationSeconds, FGameplayTag Source) = 0;
};

class UTDDCombatComponent : public UPawnComponent
{
    // AI issues intents; it never plays montages itself
    bool RequestAttack(FName AttackId, AActor* Target);
    bool CancelAttack(ETDDCancelReason Reason);
    bool IsAttacking() const;
    float GetAttackRecoveryRemaining() const;
    bool CanBeInterrupted() const;
};
```

Agent 2 publishes to the others (all in `TDDAI/Public`, `TDDWorld/Public`, `TDDNarrative/Public`):

```cpp
class UTDDEncounterManager : public UWorldSubsystem
{
    bool ActivateEncounter(FName EncounterId);
    bool IsEncounterComplete(FName EncounterId) const;
    int32 GetActiveEnemyCount(FName EncounterId) const;
};

class UTDDChapterFlowSubsystem : public UWorldSubsystem
{
    bool RequestChapterTransition(ETDDChapterId Chapter, FName EntryPointId);
    bool IsTransitionInProgress() const;
    FName GetCurrentChapterId() const;
};

class UTDDMemorySubsystem : public UGameInstanceSubsystem
{
    int32 GetFoundCount() const;                 // 0..7
    bool IsMemoryFound(int32 MemoryIndex) const; // 1..7
    bool AreAllMemoriesFound() const;
};

UTDDEndingResolver::Resolve(const FTDDEndingInputs&) -> ETDDEnding   // pure, static
```

Agent 3 publishes to everyone: `UTDDEventBus`, `UTDDPersistenceSubsystem`, `UTDDCanonRegistry`, all `FTDD*Event` structs, `ITDDDamageable`, `ITDDInteractable`, `FTDDCondition`, `FTDDSaveGame` sections.

### 13.3 Contract change process

1. Author writes `docs/03_DECISIONS/ADR-XXXX-<slug>.md` with: what changes, why, affected agents, migration/compat impact, test impact.
2. Technical Director approves or rejects; approval is recorded in the ADR's Status field.
3. The owning agent implements the change **plus** an updated contract test, in **one** commit.
4. Consumers are updated by their own agents in the same phase; a broken consumer blocks the phase gate, not the release of the contract.

**Freeze windows:** during a phase gate week, `TDDCore` is frozen except for defect fixes approved by Agent 3 and the Technical Director.

### 13.4 Handoff artefacts (required at every phase boundary)

Each agent must deliver, in `docs/02_PRODUCTION/PHASE_<n>/`:
- `REPORT_AGENT_<n>.md`: what was built, status per item using the claim vocabulary, tests run with output, known defects, blocked items, dependencies on other agents.
- Evidence bundle: build log path/timestamp, automation test report (pass/fail counts + names), profiling capture for performance work, screenshots/video for anything visual.
- A `CONTRACT_DELTA.md` if any public surface changed.

No report may state a system works without evidence; a report with missing evidence is treated as `PARTIAL`.

### 13.5 Conflict avoidance rules

- No agent creates an alternative implementation of a system owned by another agent. Need a variation? Request an extension point (this document already defines the main ones: `ITDDLocomotionAnimProvider`, `ITDDAudioService`, `ITDDDamageable`, `ITDDInteractable`, data-driven archetypes/phases).
- No agent rewrites another agent's file without an ADR-level justification and the owner's acknowledgement in the handoff.
- Shared files (`TDDCore` headers, `.uproject`, `Config/*.ini`, `.uplugin`-level settings) are Agent 3 territory; changing them is a request, not an edit.

---

## 14. Testing strategy

### 14.1 Tiers

| Tier | Scope | Technology | Runs | Blocks |
|---|---|---|---|---|
| **T1 Unit** | Pure logic: damage math, posture, hit dedup, phase selection, quest conditions, ending resolver, save serialisation, token policy, condition compose | `IMPLEMENT_SIMPLE_AUTOMATION_TEST` / `BEGIN_DEFINE_SPEC` (`TDD-Unit.*`) | Every commit (build agent) | Merge |
| **T2 Functional** | Actor-level behaviour in a test map: attack connects, dodge i-frames, parry staggers, enemy aggro, encounter completes, memory discovered, interaction prompts, checkpoint restore | Functional Testing plugin + `TDD-Functional.*` automation | Every merge to main; nightly full run | Phase gate |
| **T3 Integration / smoke** | Scripted-input chapter run (Automation Driver): start chapter → reach first encounter → complete memory → checkpoint → transition; assert no errors in log | Automation Driver + Gauntlet | Nightly | Phase gate |
| **T4 Performance** | Frame timing, memory, streaming hitches in packaged builds | Insights traces, gauntlet perf run, CSV frame capture | Nightly + per phase gate | Phase gate |
| **T5 Manual** | Feel, readability, fairness, accessibility, cultural review, art direction | Human test scripts + sign-off forms | Per phase | Phase gate |

### 14.2 Named test suites (created as systems land)

```
TDD-Unit.Combat.DamageMath
TDD-Unit.Combat.PostureAndStagger
TDD-Unit.Combat.HitDedup
TDD-Unit.Combat.CancelRules
TDD-Unit.Combat.HitStopExpiry
TDD-Unit.AI.TokenPolicy
TDD-Unit.AI.PhaseSelectorWeights
TDD-Unit.Narrative.ConditionEval
TDD-Unit.Narrative.QuestFlow
TDD-Unit.Narrative.EndingResolver        // truth table incl. "truth known does not absolve"
TDD-Unit.Narrative.MemoryCounting
TDD-Unit.Persistence.RoundTrip
TDD-Unit.Persistence.Migration
TDD-Unit.Persistence.AtomicWriteInterrupt
TDD-Unit.World.WorldStateSerialisation
TDD-Unit.Canon.ValidatorRules
TDD-Functional.Combat.LightChainConnects
TDD-Functional.Combat.DodgeIFrames
TDD-Functional.Combat.ParryStaggers
TDD-Functional.Combat.FeedbackComplete
TDD-Functional.AI.AggroOnSight
TDD-Functional.AI.TokenLimitsSimultaneousAttackers
TDD-Functional.World.EncounterCompletes
TDD-Functional.World.CheckpointRestoresEncounterState
TDD-Functional.Narrative.MemoryFragmentDiscovered
TDD-Functional.Narrative.InteractionPromptAppears
TDD-Functional.Cinematic.SkipLeavesStateConsistent
TDD-Functional.Cinematic.StreamingReadyForEveryShot
TDD-Gauntlet.ChapterSmoke.CH01
TDD-Perf.ReferenceScene.CH01_Encounter
```

### 14.3 Acceptance criteria format (mandatory)

Every task in every phase must state acceptance criteria as **measurable assertions**, e.g.:

- "Light attack chain: pressing attack within the chain window while `Attack` state active plays hits 2, 3, 4 in order with no state reset. Asserted by `TDD-Functional.Combat.LightChainConnects`."
- "Dodge grants invulnerability between 0.10 s and 0.45 s of the clip; damage received in that window is `Immune`, outside it is `Hit`. Asserted by `TDD-Functional.Combat.DodgeIFrames`."
- "Save round-trip preserves 7 memory flags, 12 counters and 3 world-state sets byte-identically after deserialisation. Asserted by `TDD-Unit.Persistence.RoundTrip`."

"We will play it and see" is not acceptance criteria. Manual feel testing (T5) exists *in addition*, not instead.

### 14.4 Evidence requirements

| Claim | Minimum evidence |
|---|---|
| Code compiles | Build log with timestamp, platform, config |
| Unit test passes | Automation report excerpt with test name and PASS |
| Functional test passes | Automation report + log with no `Error:` lines |
| Performance target met | Insights/CSV capture with median and 1%-low figures over ≥ 120 s |
| Visual feature exists | Screenshot/video + scene + build identifier |
| Bug fixed | Reproducing steps now failing to reproduce + test added that would have caught it |

### 14.5 CI pipeline (to be hosted on the production workstation/build agent — not possible in this workspace)

```
on push:
  1. UBT compile TDDEditor (Win64 Development)        ~8 min cached
  2. Data validation (editor commandlet)              must pass
  3. Automation: TDD-Unit.*                           must pass
  4. Cook smoke (single chapter, Development)         must complete
on merge to main:
  5. Automation: TDD-Functional.*  + TDD-Gauntlet.ChapterSmoke.CH01
  6. Package Development build
  7. TDD-Perf.ReferenceScene.CH01_Encounter with thresholds
nightly:
  8. Full automation sweep + Insights capture archive + content audit report
```

Content audit report (generated, committed as artifact): every data asset with canon status, cultural status, placeholder markers, missing references, unmapped locations, memory count per chapter, boss definitions missing phases, and weapons beyond the one approved.

---

## 15. Performance targets and budgets

### 15.1 Reference hardware (proposed — needs CD/TD approval)

| Tier | Spec | Target |
|---|---|---|
| **Reference** | 8-core CPU (Ryzen 5 5600X / i5-12400 class), RTX 3060 Ti / RX 6700 XT, 16 GB RAM, NVMe | **60 fps @ 1440p internal, TSR → 4K output; 1% low ≥ 50 fps** |
| **Min** | 6-core, RTX 2060 / RX 5600 XT, 16 GB RAM | 60 fps @ 1080p internal with TSR Performance; 1% low ≥ 45 fps |
| **High** | RTX 4070+ | 60 fps @ 1440p native, TSR Quality; headroom for 120 fps if approved |

Consoles: **out of scope until the Creative Director states otherwise.** No console-specific work, certification requirements or controller-specific features beyond standard gamepad support.

### 15.2 Frame budget at 60 fps (16.67 ms)

| Bucket | Budget (ms) | Notes |
|---|---|---|
| Game thread | ≤ 6.0 | Player + combat 1.5, AI ≤ 2.0, animation ≤ 1.5, world/narrative ≤ 1.0 |
| Render thread | ≤ 7.5 | Includes Nanite, culling, VSM setup |
| RHI thread | ≤ 2.0 | |
| GPU total | ≤ 16.0 | Base pass 4.0, Lumen GI+reflections 6.0, shadows/VSM 2.0, translucency/VFX 1.5, post+TSR 1.5, UI 0.3, headroom 0.7 |
| Slack | ≥ 0.6 | Never spend the whole budget; frame-to-frame variance must fit |

### 15.3 Scene and memory budgets

| Metric | Target |
|---|---|
| Visible Nanite triangles | ≤ 10 M/frame in combat arenas |
| Non-Nanite draw calls | ≤ 3,000 |
| Instanced foliage instances | ≤ 60,000 visible, HISM only |
| Dynamic lights in combat arena | ≤ 8 shadow-casting + MegaLights evaluated for non-shadow |
| VRAM (1440p) | ≤ 8 GB, texture pool streaming ≤ 4.5 GB |
| System RAM | ≤ 10 GB |
| Boss arena with 8 enemies + 4 VFX layers | 60 fps on reference hardware |
| Chapter load | ≤ 15 s cold, ≤ 5 s with warm shader cache |
| Sublevel / cinematic stream | ≤ 2 s, never visible as a pop during a shot |
| Hitches > 50 ms | ≤ 1 per 10 minutes of gameplay |
| Shader compilation stutter | zero in packaged build (precompile + PSO cache shipped) |

### 15.4 Profiling workflow

- Every phase gate runs `TDD-Perf.ReferenceScene.CH01_Encounter` (fixed camera path, fixed spawns, fixed VFX) on the reference machine and archives `.utrace` + CSV.
- Regression rule: > 5 % regression in frame time or > 100 MB VRAM growth blocks the gate until explained or fixed.
- `stat unit`, `stat GPU`, `stat game`, `stat streaming`, `memreport -full`, Insights counters are the standard toolset. Numbers are recorded in the phase report, never asserted from memory.

---

## 16. Development phases and dependencies

Durations are indicative engineering effort for one agent working continuously; they are planning aids, not commitments, and they exclude content production (art, animation, audio, cinematics), which is the dominant cost of this project and is not yet staffed.

### Phase 0 — Architecture and technical foundation
**Scope:** this document set; `.uproject`; 9 modules with correct dependencies; target/build files; `Config/*.ini` baseline; Enhanced Input setup; `TDDCore` types/interfaces/events/save skeleton; canon registry + Asset Manager types; editor validators (naming, canon status, missing references); test harness; CI scripts; engine pin record; coding standards.
**Dependencies:** engine installed on production workstation; LFS configured; TD approves ADR-0001/0003/0004.
**Exit criteria:** project opens and compiles on UE 5.8 (Editor + Game Development); empty test map runs at target frame rate; `TDD-Unit.Canon.ValidatorRules` passes; validator catches a deliberately bad asset; CI green on first push; zero warnings in our modules.
**Deliverable evidence:** build log, automation report, CI run link.

### Phase 1 — Movement and character laboratory
**Scope:** `ATDDPlayerCharacter`, CMC tuning, state machine, input buffering, camera rig + lock-on, locomotion provider interface with blend-space implementation (motion matching follows when clips exist), traversal (vault/mantle/ledge), debug lab level with measurement tools (speed, turn, latency, foot-slide overlay).
**Dependencies:** P0. Animation clips (even placeholder mannequin) for locomotion.
**Exit criteria:** measurable locomotion targets met and recorded; no foot sliding > 5 cm at 60 fps in the lab; camera collision verified in a tight interior; `TDD-Functional.Movement.*` suite passes; input latency ≤ 1 frame measured.
**Gate note:** the "does it feel right" pass is a T5 manual gate with the Creative Director; engineering cannot self-certify feel.

### Phase 2 — Combat foundation
**Scope:** attributes/GAS wiring, attack data assets, hit windows, hit resolution, damage pipeline, block/parry/dodge, posture/stagger, hitstop, reactions, hit feedback bundle, combat dummy + training room, `TDD-Unit.Combat.*` and `TDD-Functional.Combat.*`.
**Dependencies:** P1 (state machine, camera, locomotion), placeholder attack animations.
**Exit criteria:** full player-vs-dummy loop functional: 4-hit chain, heavy, block, parry, dodge, stagger, death; all damage flows through one pipeline; every hit produces complete feedback; all listed tests pass; no attack can double-hit.

### Phase 3 — Character behaviour and animation
**Scope:** motion matching corpus integration (or blend-space hardening), hit-reaction tables, foot IK, turn-in-place, weapon grip, animation LODs/URO, attack cancel polish, hitstop feel pass, camera behaviour in combat.
**Dependencies:** P2. **Animation content from the animation team** — this is the first phase genuinely blocked on content production.
**Exit criteria:** 12+ distinct attack/reaction clips wired; no animation-pop during chain cancels; animation memory within budget; manual feel gate passed.

### Phase 4 — Enemy and boss architecture
**Scope:** `TDDAI` module (perception, StateTree archetypes, combat brain, token director), encounter manager, boss framework, arena bounds, one complete boss encounter (Chapter 1's Great Root Mother — framework demonstration, mechanics **subject to CD design approval**), `TDD-Unit.AI.*`, `TDD-Functional.AI.*`.
**Dependencies:** P2 (damage pipeline), P3 (enemy animation set).
**Exit criteria:** 3 enemy archetypes behave distinctly; token system caps simultaneous attackers; the pilot boss completes three phases, transitions deterministically, and its selector passes seeded weight tests; 8-enemy encounter holds 60 fps on reference hardware.

### Phase 5 — World simulation, exploration and traversal
**Scope:** `TDDWorld` (chapter flow, world state, time/weather data layers, checkpoints, streaming), interaction framework, chapter 1 blockout at true scale, memory anchor volumes, encounter/checkpoint placement, loading/transition flow, `TDD-Functional.World.*`.
**Dependencies:** P1 (traversal), P4 (encounters), environment blockout from world team.
**Exit criteria:** Chapter 1 blockout traversable end-to-end; streaming never exposes a hole; checkpoint restore is exact; time/weather state persists across save/load; chapter transition works with loading screen and failure path.

### Phase 6 — Progression and narrative systems
**Scope:** `TDDNarrative` (flags, conditions, quests, seven-memory framework, ending resolver, cinematics subsystem, journal/codex hooks), persistence hardening (migration, atomic write, corruption), UI framework + HUD + menus + settings/rebinding, localisation pipeline + pseudo-loc test.
**Dependencies:** P0 (save contracts), P2 (combat events), P5 (world events).
**Exit criteria:** all six ending cases resolve correctly (truth table); memories discovered through world interaction persist through death and reload; save migration tested across two schema versions; a full menu/settings/rebinding loop works with gamepad; pseudo-loc build runs.

### Phase 7 — Campaign and chapter production (waves)
**Scope:** Chapters 1–8 built through the Chapter pipeline (6.6), boss by boss, memory by memory, cinematic by cinematic.
**Dependencies:** P0–P6 complete and gated; **content production capacity** (art, animation, audio, cinematics, writing) — this phase is primarily content, not engineering.
**Execution:** Chapter 1 fully finished and gated first (vertical slice), then Chapters 2–7 in production waves, Chapter 8 last (it depends on all memory content and the approved Chapter 8 environments, which are still `PENDING APPROVAL` canon).
**Exit criteria per chapter:** chapter acceptance test passes; perf gate passes; content audit clean (no placeholders, canon statuses approved, cultural sign-offs present); T5 manual review signed off by Creative Director.

### Phase 8 — Polish, optimisation, testing and release preparation
**Scope:** full-game playthrough passes, difficulty/balance pass, accessibility audit, localisation, platform packaging, crash/telemetry (if approved), certification readiness (only if console approved), bug triage to zero-blocker, final perf validation, build reproducibility.
**Exit criteria:** full campaign completable with all three endings reachable in a packaged Shipping build; zero blockers; all performance targets met; all content audits clean; release candidate build archived and reproducible from a tagged commit.

### Dependency chain (summary)

```
P0 -> P1 -> P2 -> P3 -\
                \-> P4 -> P5 -> P6 -> P7 -> P8
                          P1 -----^
P0 (save contracts) ----> P6
Content production (art/animation/audio) gates P3, P4, P5, P7
CD/TD decisions gate: OAD-03/04/06/07/13 (art), OAD-23 (ending content),
OAD-32/34 (memory content), boss mechanics, progression economy
```

---

## 17. Risks and mitigations

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | **No engine in the agent workspace.** Agents cannot compile, run or test. Unverified code accumulates. | Critical | ADR-0012: every claim carries `UNVERIFIED`; TD builds on the production workstation each phase; keep change batches small enough to review; never merge unbuilt code into a phase gate |
| R2 | **Zero production assets.** Only 7 approved concept designs; no meshes, rigs, animation, audio, VO or cinematics. | Critical | Placeholder-first policy with explicit labelling; content pipeline (6.6) proven on blockout; asset delivery tracked as a separate content schedule; no "art progress" claims from engineering |
| R3 | **Scope.** 8 chapters × boss + combat + narrative + endings is a multi-year AAA-scale effort. | Critical | Vertical slice (Chapter 1) before any other chapter; phase gates are hard; framework-first so content scales without new code; explicit statement that Phase 7 dominates total cost |
| R4 | Motion Matching corpus not ready | High | Provider interface with blend-space fallback (ADR-0005); config switch; asserted in tests |
| R5 | Canon/art decisions still open (OAD-03/04/06/07/13/23/32/34/55) | High | Canon status field on every asset; cook-time gate; engineering never fills gaps; placeholders named and audited |
| R6 | Cultural representation risk (invented mythology read as authentic Igbo tradition; uli motifs; masquerade imagery) | High | `ETDDCulturalStatus` gate with consultant sign-off; no reproduction of named uli motifs (OAD-06); Okwu kept distinct from real masquerade (OAD-04); codex attribution field; the Art Bible's cultural guide still needs consultant review |
| R7 | Chapter 8 canon status `PENDING APPROVAL` while 5 of 7 approved designs are Chapter 8 environments | Medium | Environment design used for blockout scale only; no Chapter 8 narrative content built before canon approval |
| R8 | Performance regressions from Lumen + VSM + Nanite in dense forest (Chapter 1) | Medium | Budgets in Section 15; reference scene benchmark every phase; HLOD; foliage limits; MegaLights/Lumen Lite evaluated for min-spec |
| R9 | Agent collision on shared systems (`TDDCore`) | Medium | Ownership matrix + contract change process + freeze windows (Section 13) |
| R10 | Git LFS not configured; binary assets could be committed as raw blobs | Medium | `.gitattributes` committed now; LFS required on workstation before first asset; 100 MB snapshot cap documented |
| R11 | Save-data corruption across versions during long production | Medium | Versioned schema + migrations + atomic write + checksum + captured-blob tests |
| R12 | Narrative systems over-engineered (dialogue graph, scripting VM) for content that does not exist | Low | Conditions are a closed, small composable set; no scripting language; extend only with an ADR |

---

## 18. Appendices

### A. Canon-to-data mapping (engineering-relevant facts, sourced — not invented)

| Fact | Source | Where it lives in code |
|---|---|---|
| Adanna, 25, warrior; six when Nneka died | Directive; OAD-35 | `UDA_Character_Adanna`, narrative timeline constant |
| Left shoulder guard; blade on left hip | OAD-01, OAD-09, OAD-10 | Skeleton sockets, armour data asset |
| Okwu's hood = darkness only | OAD-12 | Okwu character asset (no face geometry), material rule |
| Seven memories, Ch. 1–7, exploration-earned, fragment presentation | OAD-32 | `UTDDMemorySubsystem`, `UTDDMemoryFragment` × 7 |
| Memory 7 truth; canon unchanged; no absolution | OAD-34 | Ending resolver ignores truth flags; dialogue conditions |
| Three endings; kill is literal; hidden = all seven memories | Directive; OAD-27, OAD-31, OAD-32 | `UTDDEndingResolver` |
| Hollow King began ~1 year before game opens | OAD-41 | Narrative timeline constant |
| Environment design approval ≠ canon approval | OAD-48, OAD-53 | `ETDDCanonStatus` on location records |
| Time/weather are states, not locations | OAD-24 | `UTDDWorldStateSubsystem`, data layers |
| Pythons are never enemies or loot (Ch. 4) | OAD-14 | AI spawn validation for Chapter 4 |
| White rams are ordinary livestock | OAD-19 | Ambient NPC archetype, empty loot table |
| Single approved weapon | OAD-09, OAD-37 | `UTDDWeaponDefinition` count = 1, validator |
| Courtyard: four generations, tree ages older/larger going back | OAD-42, OAD-44 | Chapter 8 data-layer variants |
| Nneka's voice is deliberate; she is dead | OAD-39 | Audio/subtitle rule keys (`NoEchoProcessing`, `NoInPresence`) |

Anything not in this table is **undecided** and must not be implemented as if it were canon.

### B. Glossary

- **ADR** — Architecture Decision Record (`docs/03_DECISIONS/`).
- **OAD** — Open Art Decision, in the Art Bible's `OPEN_ART_DECISIONS.md`.
- **ASC** — Ability System Component (GAS).
- **CMC** — Character Movement Component.
- **ANS / AN** — AnimNotifyState / AnimNotify.
- **World Partition** — UE5 level streaming by spatial cells.
- **Data Layer** — a runtime-togglable grouping of World Partition content (used here for time/weather states).
- **TSR** — Temporal Super Resolution.
- **VSM** — Virtual Shadow Maps.
- **Claim status** — see `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md`.

### C. Decisions required from the Technical Director / Creative Director before Phase 0 closes

1. Confirm engine pin **UE 5.8** (ADR-0001) or specify another version.
2. Confirm target platform: **PC (Windows) only**, consoles out of scope (Section 15.1).
3. Confirm reference and minimum hardware (Section 15.1) so performance gates are meaningful.
4. Confirm **GAS adoption** (ADR-0004) — it is expensive to reverse after Phase 2.
5. Confirm **audio approach**: MetaSounds only, no Wwise/FMOD (ADR-0009).
6. Confirm **single-player only** (no co-op/networking), so no replication work is scheduled.
7. Confirm the **player combat kit** defaults in Section 4.2 as a tuning baseline.
8. Confirm **progression model**: RPG progression is in the directive, but no economy, upgrade tiers, currency or skill tree is defined. Options: chapter-gated unlocks only / equipment tiers / skill tree. Phase 6 scope depends on this.
9. Confirm **save-scumming and manual-save policy** (affects persistence design and difficulty framing).
10. Confirm **accessibility baseline** in Section 12 as a requirement, not an option.
11. Provide or schedule **content**: placeholder-beating animation, boss mechanics for the seven named bosses, memory content (OAD-32/34), ending sequences (OAD-23), and cultural consultant review of the Art Bible's cultural guide.
12. Confirm whether **QTEs or scripted instants** are permitted in cinematics, and whether an accessibility bypass is required.

### D. Document change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Initial architecture; companion ADRs 0001–0012; project state audit; claims ledger; open questions |
