# WORLD AND GAMEPLAY SYSTEMS — ARCHITECTURE SPECIFICATION

**Document:** TDD-WARCH-001 · **Version:** 1.0 · **Date:** 2026-11-16
**Author:** Agent 2 — World, Systems and Gameplay Simulation
**Status:** `SPEC` — every runtime component below is specified and unbuilt. Schemas and validators referenced
here **do** exist and pass tests.
**Companion:** `Docs/WORLD_ASSESSMENT.md` (why), this document (what/how)

This document is the contract between Agent 2 and the rest of the project. If a consumer needs something not
in §7, it must be requested through the interface-change protocol (architecture §6.9) rather than reached into.

---

## 1. Scope

### 1.1 I own

| Domain | Components |
|---|---|
| World structure | Chapter director, location registry, streaming policy, environment states |
| Interaction | `ITDDInteractable`, interaction routing, prompt data, discovery |
| Traversal (data/gating) | Traversal action requirements, `TRV` location gating — **coordination only**, Agent 1 owns the movement |
| NPCs | Five-tier population, routines, activities, bark interaction, dialogue integration points |
| Enemies | AI base, perception, StateTree behaviours, archetype data |
| Bosses | Phase-graph schema, validator, executor — **data, not bespoke code** |
| Progression | Scene state, quest graph, memory director, ending eligibility |
| World simulation | Ambient drivers, environment state transitions, world reaction to player state |

### 1.2 I do not own

| Not mine | Owner | Boundary |
|---|---|---|
| Player controller, camera, input | Agent 1 | I consume a `UTDDPlayerContext` façade only |
| Core combat, damage, hit arbitration, abilities | Agent 1 | I subscribe to damage events; I never apply damage |
| Weapon handling | Agent 1 | — |
| Integration, build, packaging, perf tooling, UI, save | Agent 3 | I provide data; Agent 3 serialises and presents |
| Story, canon, visual approval | Creative Director | I never invent narrative content |

### 1.3 Hard prohibitions I accept

- I will not create a second player controller.
- I will not create a competing combat or damage path.
- I will not add a quest, reward or collectible to a scene the register marks "None required".
- I will not present a `PROPOSED` or `PENDING APPROVAL` location as canon.
- I will not implement a boss before Agent 1's combat and enemy interfaces exist.

---

## 2. World hierarchy

```
World
└── Chapter                    ETDDChapter, 1..8, ESTABLISHED
    └── Major Environment      CHxx-ENV-001 (one per chapter)
        ├── Locations          CHxx-{SUB,SET,INT,LMK,TRV,EXP,BOS}-nnn
        │   └── Scenes         CHxx-SCN-nnn   (135 total)
        └── Environment States ES_<Chapter>_<Time|Weather|Supernatural>
```

Rules encoded from the registers:

- A **scene is not a location** and is counted separately (register rule).
- A scene belongs to exactly one parent location.
- An **environment state is not a location** and must never appear in the location registry.
- **IDs are permanent.** Retired IDs are never reused; a retired location gets `Retired` state, not deletion.

---

## 3. Runtime components

| Component | Type | Responsibility | Status |
|---|---|---|---|
| `UTDDLocationRegistry` | `UWorldSubsystem` | Loads chapter manifest, resolves `FTDDLocationId` → record, exposes canon/design status, validates at start | SPEC |
| `ATDDChapterDirector` | `AActor`, one per chapter level | Chapter lifecycle, scene activation, state transitions | SPEC |
| `UTDDEnvironmentStateSubsystem` | `UWorldSubsystem` | Current time/weather/supernatural state; applies data layers + lighting + mix | SPEC |
| `UTDDInteractionRouter` | `UWorldSubsystem` | Finds best interactable in view/range, produces prompt view-model, routes input | SPEC |
| `UTDDSceneStateSubsystem` | `UGameInstanceSubsystem` | `FTDDSceneState` per scene; persistence handoff to Agent 3 | SPEC |
| `UTDDMemoryDirector` | `UGameInstanceSubsystem` | Seven six-stage machines; the **only** authority that grants memory progress | SPEC |
| `UTDDCampaignSubsystem` | `UGameInstanceSubsystem` | Chapter unlock, quest graph position, ending eligibility | SPEC |
| `ATDDNamedNPC` | `ACharacter` | Tier 1 actors: routine, dialogue hook, quest hook | SPEC |
| `UTDDCrowdSubsystem` | `UWorldSubsystem` | Tier 2/3 populations via Mass, budget enforcement | SPEC |
| `ATDDEnemyBase` | `ACharacter` | Enemy base with StateTree, perception, damage reaction | SPEC |
| `UTDDBossPhaseGraph` | `UPrimaryDataAsset` | Boss phase data (ADR-0007) | SPEC |
| `UTDDBossController` | `AActorComponent` | Executes a phase graph generically | SPEC |
| `ATDDEncounterVolume` | `AVolume` | Arms/disarms encounters; reports to directors | SPEC |

**None of these are implemented.** They are named so that interface discussion is concrete and so ownership is
unambiguous before implementation.

---

## 4. Streaming and budget policy

Budget inputs come from the register's **access level** column. The policy is data, not hard-coded per level.

```cpp
// TDD/World/TDDStreamingTypes.h — SPEC
UENUM(BlueprintType)
enum class ETDDAccessLevel : uint8
{
    OpenExterior,           // part of the region cell
    FullyEnterable,
    PartiallyEnterable,
    VisuallyAccessible,
    BackgroundEnvironment,
    VisuallyInaccessible    // decided but not visible from any reachable point
};

USTRUCT(BlueprintType)
struct FTDDStreamingBudget
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere) int32 MaxResidentLocations = 12;
    UPROPERTY(EditAnywhere) int32 MaxResidentScenes = 20;
    UPROPERTY(EditAnywhere) int32 MaxActiveAIAgents = 14;
    UPROPERTY(EditAnywhere) int32 MaxCrowdAgents = 60;
    UPROPERTY(EditAnywhere) int32 MaxBackgroundAgents = 120;
    UPROPERTY(EditAnywhere) float StreamInSecondsTarget = 8.0f;
};
```

| Access level | Resident | Collision | Tick | Cost units |
|---|---|---|---|---|
| OpenExterior | with region | full | yes | 1.0 |
| FullyEnterable | yes | full | yes | 1.0 |
| PartiallyEnterable | yes | simplified | yes | 0.6 |
| VisuallyAccessible | in sightline | none | no | 0.2 |
| BackgroundEnvironment | never as geometry | none | no | 0.05 |
| VisuallyInaccessible | on demand | none | no | 0.05 |

**Enforcement:** `UTDDLocationRegistry` computes resident cost each tick and logs a violation through
`LogTDDWorld` when a budget is exceeded. In test maps, exceeding a budget is an automation failure.

---

## 5. The five-tier NPC model

### 5.1 Tiers

This was described as three tiers. TR-1 forced it to five, because the register
distinguishes kinds of population that a three-tier model collapses and thereby
over-bills. A scene with a single scripted blacksmith does not need an AI agent,
and the register has more of those than it has crowds.

The authoritative mapping is data, not prose: `Tools/world/data/population_policy.json`,
validated by `Tools/world/population_budget.py`.

| Tier | Actor | Simulation | Interaction | Cost unit | Chapter 1 scenes |
|---|---|---|---|---|---|
| `NAMED` | `ATDDNamedNPC` (ACharacter + StateTree) | full tick, full anim, perception | dialogue, quests, memory | 4.0 | 1 |
| `CROWD` | Mass entity + `UTDDCrowdStateProcessor` | LOD tick 0.5–4 Hz by distance | bark only | 1.0 per actor | 14 |
| `SCRIPTED` | one `ATDDPerformer` | fixed animation loop, **no AI, no perception, no nav** | none | 0.3 per scene | 19 |
| `BACKGROUND` | Mass, instanced, no tick | vertex animation only | none | 0.05 | 0 |
| `NONE` | nothing | nothing | none | 0 | 12 |

Per-scene cost is multiplied by an access multiplier (`OPEN EXTERIOR` 1.0,
`FULLY ENTERABLE` 1.0, `PARTIALLY ENTERABLE` 0.6, `VISUALLY ACCESSIBLE` 0.2,
`BACKGROUND ENVIRONMENT` 0.05), because a scene the player can only see is far
cheaper than one they can walk into. Chapter ceilings: 16 crowd scenes, 60 total
cost units, 4 named nearby.

Values above are read from `population_policy.json`; an earlier revision of this
table stated 0.8 / 0.5 / 0.25, which contradicted the data. A test now compares
this document against the policy file.

Cost units are **relative budget arithmetic, not milliseconds** — a distinction
the policy file states explicitly and a test enforces.

### 5.1.1 Why `SCRIPTED` had to exist

Collapsing `SCRIPTED` into `CROWD` or `NAMED` mis-bills the majority of the
chapter. Chapter 1 has 19 scripted scenes and 14 crowd scenes; treating every
world-activity scene as a simulated NPC would have inflated the chapter by
roughly a third for no behavioural gain.

Why `BACKGROUND` exists separately: an instanced actor with no tick is not a
simulated agent. Counting it as one overstates cost by more than 3x.

### 5.1.2 Derived budget, Chapter 1

Measured, not estimated — `Docs/evidence/agent2/CH01_population_budget.json`:

| Metric | Value |
|---|---|
| scenes | 46 |
| requiring no simulation at all (NONE + SCRIPTED) | 31 of 46 |
| CROWD scenes | 14 |
| NAMED scenes | 1 |
| simulated NPCs, lower/upper bound | 30 / 49 |
| crowd peak estimate | 29 |
| total cost units | 36.58 |
| validation | PASS |

**31 of 46 scenes need no simulated agent.** That is the TD's point answered with
numbers rather than assurance: the majority of ambient activity is a performer on
a loop, not an agent.

### 5.1.4 How much of this is fact

Only **5 of 46 scenes (11%)** have register NPC data. The remaining **41 scenes
(75% of the cost)** rest on policy defaults. Two parameters — the ambient
`expected_npcs` and the `crowd_concurrency_ratio` — control almost the entire
estimate, because only CROWD scenes are priced per NPC.

The estimate ranges from **23.38 to 58.97 cost units** across plausible policy
assumptions, a 2.5x spread. Worst case leaves 1.03 units below the chapter
ceiling. Full analysis: `Docs/POPULATION_SENSITIVITY_REPORT.md`.

Rounding is **upward** (`math.ceil`) by design: overestimating a budget costs
margin, underestimating costs the project. Every scene row carries
`npcs_provenance` (`REGISTER_DATA` / `POLICY_DEFAULT` / `UNPARSED` / `NO_NPCS`)
so a reader never has to infer whether a number is data or assumption.

Every scene records where its tier came from (`tier_source`) and where its NPC
count came from (`npcs_source`: `register` or `policy_default`). 41 of 46 scenes
have no captured detail block, so their counts are policy defaults and are
labelled as such per-scene rather than presented as register data.

### 5.1.3 Safety properties the budget enforces

- An unrecognised scene category does not default to zero. It falls back to
  `SCRIPTED` and **fails validation**.
- An unparseable NPC description does not become zero. It is reported and
  **fails validation**, because zero understates cost.
- A scene whose register prose names a child carries
  `RULE-NPC-CHILDREN-NO-COMBAT` automatically.
- Animal presence is excluded from performer counts but retained as ambience.

### 5.2 Routine data (from the register's per-scene routine lines)

```cpp
// SPEC
USTRUCT(BlueprintType)
struct FTDDRoutineStep
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere) float StartHour;       // 0..24
    UPROPERTY(EditAnywhere) float EndHour;
    UPROPERTY(EditAnywhere) FTDDLocationId Location;
    UPROPERTY(EditAnywhere) FGameplayTag Activity; // Activity.Cook, Activity.Farm, ...
    UPROPERTY(EditAnywhere) bool bMayBeAbsent;     // off-scene, despawn
};

USTRUCT(BlueprintType)
struct FTDDDailyRoutine
{
    GENERATED_BODY()
    UPROPERTY(EditAnywhere) TArray<FTDDRoutineStep> Steps;
};
```

Validation rules (build-time):
- Every `Location` must exist in the registry. A routine pointing at an unregistered location is a data error.
- Steps must be non-overlapping and cover 0–24 h or declare absence explicitly.
- An activity tag must be registered.

The register's `CH01-SCN-001` entry becomes exactly two or three steps. This is the intended authoring cost:
small, legible, reviewable.

### 5.3 Canon guards

- `RULE-NPC-CHILDREN-NO-COMBAT`: a child actor added to any targeting profile fails validation.
- Named cast names are approved (OAD-15) but are not runtime keys; IDs and tags are.

---

## 6. Interaction framework

Full interface in the assessment §5.4. Additional constraints established here:

1. **Hold-to-commit vs tap.** `ETDDInteractionMode { Tap, Hold }`. Memory fragments are `Hold` (ADR-0008 M1
   ordering depends on deliberate commitment, not accidental brush-past).
2. **One interactable at a time.** The router picks by score = `f(angle to view, distance, priority tag)`; ties
   resolve by priority, then by stable ID, so behaviour is deterministic and testable.
3. **No interaction during cinematic or memory playback.** Router checks a world-level `State.Cinematic` tag.
4. **Prompt text is never composed in C++ string concatenation** — it is a localisable `FText` view-model with
   named arguments.
5. **Discovery is silent.** Finding a memory fragment does not pop a HUD element. It changes ambience and audio
   (canon: "found only by exploration", "met as fragments, not collectibles").

---

## 7. Interfaces exposed to other agents

### 7.1 To Agent 1 (consumes from me)

| Interface | Purpose | Notes |
|---|---|---|
| `UTDDPlayerContext` | Read-only player state façade: position, facing, locomotion state, in-combat flag, interaction target | Agent 1 publishes; I read. I never write it. |
| `ITDDInteractable::GetInteractionVerb()` | Tag → Agent 1 picks montage | Decouples animation from world content |
| `ATDDTraversalMarker` | Placement actor declaring a traversal opportunity (vault point, ledge, liana) | Agent 1's traversal component queries these |
| `UTDDEncounterVolume` | Tells Agent 1 when combat is expected (music, stamina rules) | |
| `OnEnemyDamageWindowChanged` | I broadcast telegraph windows for enemy attacks; Agent 1's parry logic consumes | Prevents AI and combat disagreeing about timing |

### 7.2 To Agent 3 (consumes from me)

| Interface | Purpose |
|---|---|
| `UTDDSceneStateSubsystem::ExportState/ImportState` | Save/load of world progress; explicit structs, no actor pointers |
| `UTDDMemoryDirector::GetLedger()` | Memory records for save + Ending 3 predicate |
| `UTDDCampaignSubsystem::GetEndingEligibility()` | Ending 1/2/3 eligibility with *which* memories are missing |
| `UTDDBossPhaseGraph` schema | UI needs phase state for health bars; audio needs music state |
| Location/scene records | Codex, map-less discovery log, telemetry |

### 7.3 From Agent 1 (I need)

`FTDDLocomotionState` + delegate · traversal action enum (**must freeze before Stage 6**) ·
`OnDamageApplied(FTDDHitEvent)` · attack telegraph stream · player presence/stealth state.

### 7.4 From Agent 3 (I need)

Engine build (Stage 1) · parsed tag registry · save schema with a world-state section · canon CI hook ·
evidence harness · perf capture tooling.

---

## 8. Memory director (canon-critical)

Seven independent six-stage machines (ADR-0008). Implementation notes specific to this module:

```cpp
// SPEC
UENUM(BlueprintType)
enum class ETDDMemoryStage : uint8
{
    Undiscovered, Place, Object, Sound, Interaction, Playback, Committed
};

USTRUCT()
struct FTDDMemoryProgress
{
    GENERATED_BODY()
    UPROPERTY() FTDDMemoryId Memory;
    UPROPERTY() ETDDMemoryStage Stage = ETDDMemoryStage::Undiscovered;
    UPROPERTY() FString ContentHash;      // invalidates stale completions
    UPROPERTY() FDateTime CommittedUtc;
};

USTRUCT()
struct FTDDMemoryLedger
{
    GENERATED_BODY()
    UPROPERTY() TArray<FTDDMemoryProgress> Entries;   // at most 7
};
```

**Invariants (each one an automation test):**

| # | Invariant | Failure mode prevented |
|---|---|---|
| M1 | Stage advances only via its own `CanAdvance` predicate | Accidental trigger-volume completion |
| M2 | No stage may be skipped | Fragment sequence becoming a shortcut |
| M3 | A committed memory cannot re-commit | Double-granted ending eligibility |
| M4 | Playback uses a sublevel distinct from the discovery location | Canon violation ("did not necessarily happen there") |
| M5 | Commit writes a content hash of the memory definition | Silent mis-grant after content edit |
| M6 | Ending 3 = all seven committed **and** hashes current | Locking the hidden ending correctly |
| M7 | Absence is reported per memory | Player-facing clarity that respects canon wording |
| M8 | No memory gates another memory's *discovery* | Inventing an order the canon does not state (D-04) |

**State source of truth:** `Tools/canon/data/canon_index.json` → generated `DT_MemoryFragments`. The game does
not hard-code memory titles, locations or fragments anywhere.

---

## 9. Enemy and boss architecture

### 9.1 Enemy base

```
ATDDEnemyBase (ACharacter)
├── UStateTreeComponent          behaviour
├── UAIPerceptionComponent       sight + hearing
├── UTDDDamageReactionComponent  reacts to Agent 1's damage events (no health ownership)
├── UTDDPatrolComponent          optional route
└── UTDDThreatComponent          target selection, coordination token
```

**Coordination rule:** only N enemies may attack simultaneously (default 2, per archetype). A token pool
prevents the classic crowd-surround. This is a *game feel* requirement, not an AI flourish.

**Perception inputs:** sight (cone + occlusion) and **hearing from the audio subsystem's sound events**, not
from guessed animation lengths. This is why audio is my domain.

### 9.2 Boss phase graph

Schema and validator as ADR-0007. Additions from the world side:

- Each phase may reference **arena states** by name; the arena state must exist in the chapter's environment
  state set, or validation fails.
- Each phase may reference a **camera profile** (Agent 1 owns the camera; I own the profile data).
- Each phase may reference a **music state tag** (audio).
- `MemoryFound` transition kind exists so a chapter can react to memory discovery without bespoke code.

**Deliberately not built yet:** any actual boss. Stage 5 at the earliest, after combat interfaces exist.

---

## 10. Quest, scene state and campaign

Given the registers contain only **4 main story scenes and 9 secondary story scenes** across the whole game,
the quest layer is intentionally small:

```
Chapter objective (1 per chapter, linear)
├── Story scene(s)            from the register
├── Boss encounter            complete chapter
└── Optional: 1 memory discovery, 1 exploration area
```

No branching quest network. No fetch quests. No collectibles. This is a canon-driven scoping decision.

`FTDDSceneState { Discovered, Completed, Variant }` exists for all 135 scenes so the world can react
(e.g. "The House No One Lives In" being entered) without per-scene engineering.

---

## 11. Testing strategy (my domain)

| Layer | Test | Runs without engine? |
|---|---|---|
| L0 | Register parsing, canon vocabularies, ID scheme | **Yes — implemented** |
| L0 | World manifest validation against canon (locations registered, parents exist, statuses respected) | Yes — to be built |
| L1 | Memory director invariants M1–M8 | Logic yes; needs compile |
| L1 | Ending eligibility predicate | Logic yes; needs compile |
| L1 | Routine data validation (non-overlapping, locations exist, activities registered) | Yes — to be built |
| L1 | Phase graph reachability / no dead ends | Yes — to be built |
| L2 | Streaming budget not exceeded in a chapter test map | No |
| L2 | Interaction router determinism (angle/distance/priority/tie-break) | No |
| L2 | NPC tier promotion/demotion at budget boundaries | No |
| L2 | Children never enter a targeting profile (canon rule) | No |
| L2 | No snake enemy can spawn in Chapter 4 (canon rule) | No |
| L3 | Chapter 1 playthrough incl. Memory 1 | No |

---

## 12. Milestones

| Milestone | Deliverable | Evidence |
|---|---|---|
| **W-M0** | Register parser + corrected canon model | 101 L0 tests, `Docs/evidence/agent2/W-M0_*.json` |
| **W-M1** | World manifest schema + generator + validators | L0 test run |
| **W-M2** | Interfaces frozen (`ITDDInteractable`, streaming types, memory types) + TD sign-off | review record |
| **W-M3** | Runtime location registry + chapter director (needs engine) | L1 tests |
| **W-M4** | Interaction router + environment states (needs engine) | L1/L2 |
| **W-M5** | NPC tiers + routines (needs engine) | L2 + perf |
| **W-M6** | Enemy AI + 2 archetypes (needs engine) | L2 + video |
| **W-M7** | Phase graph validator + executor, no boss | L1 |
| **W-M8** | Memory director, all 7 (needs engine) | L1 invariants |
| **W-M9** | Campaign + endings | L1 |
| **W-M10** | Chapter 1 world integration | L3 playthrough |
