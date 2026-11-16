# WORLD AND GAMEPLAY SYSTEMS TECHNICAL ASSESSMENT

**Document:** TDD-WGTA-001 · **Version:** 1.0 · **Date:** 2026-11-16
**Author:** Agent 2 — World, Systems and Gameplay Simulation
**Status:** `PARTIAL` — the assessment is complete and evidence-backed; every runtime system it proposes is `SPEC`
**Reviewed by:** pending Technical Director review

---

## 0. Summary for the Technical Director

The repository contains **no world code, no AI code, no quest code and no content**. The world domain is
100% greenfield. That is the easy part of this report.

The important finding is elsewhere: **the Art Bible already defines the game's world structure in machine-readable
detail, at a scale that dwarfs what the engineering architecture assumed — and the canon model I inherited in
Stage 0 was wrong in two material ways.** §2 documents both, with the correction already landed and tested.

Headline numbers from the Drive registers (`LOCATION_MASTER_REGISTER` v2.9 and
`SCENE_AND_MICROLOCATION_MASTER_REGISTER` v1.9):

| Quantity | Count |
|---|---|
| Major environments | 8 (one per chapter) |
| Other locations | 142 |
| Interiors (location entries) | 46 |
| **Scenes and micro-locations** | **135** |
| Environment-state references (night/rain/supernatural) | 40 |

For scale: **Chapter 1 alone contains 46 scenes and 68 location entries**, of which 45 scenes are *not* story
scenes. Most are ambient life — cooking, sweeping, wells, goats at dusk. That is not incidental detail dumped
into the register; it is a design statement about what this game is. The world is a **living place the player
walks through**, and the registers specify its life in detail.

That has a direct engineering consequence, and it is the single most important architectural decision in this
document:

> **The settlement cannot be 68 hand-placed actors running full AI. It must be a population simulation with a
> small number of high-fidelity "named" actors, a crowd tier, and a background tier that needs no AI at all.**

This is why my world architecture (§5) is built around **three NPC fidelity tiers with an explicit budget**,
and why the scene register's `Scene Category` column — AMBIENT NPC SCENE, WORLD ACTIVITY SCENE, ATMOSPHERIC
SCENE, BACKGROUND ENVIRONMENT — is not documentation. **It is the population budget, authored by the design
team.** Engineering consumes it directly.

Second most important finding: **most of the world is not canon and not visually approved.** Of Chapter 1's 68
entries, 19 are ESTABLISHED, 43 are PROPOSED and 6 are PENDING APPROVAL. Environment design status is `IN
REVIEW`, `NOT STARTED` or `REQUIRES REVISION` for nearly everything. Engineering must therefore build against
**blockout geometry and a status-driven content pipeline**, not against final art, for a long time yet.

---

## 1. Existing world and gameplay systems

### 1.1 Inspected state of the repository (verified 2026-11-16)

| Area | Files | State |
|---|---|---|
| World / level architecture | none | **Absent** |
| Streaming / partition | none | **Absent** |
| Interaction framework | none | **Absent** |
| Traversal | none | **Absent** |
| NPC / crowd | none | **Absent** |
| Enemy AI / boss | none | **Absent** |
| Quest / progression | none | **Absent** |
| Memory director | none | **Absent** |
| Canon tooling | `Tools/canon/*` | **ESTABLISHED** — 101 tests passing |
| ID value types | `Source/TDDRuntime/Public/Framework/TDDIds.h` | **SPEC** — authored, uncompiled |
| Gameplay tag registry | `Config/DefaultGameplayTags.ini` | **SPEC** — authored, unparsed |
| Architecture / ADRs | `Docs/*` | **ESTABLISHED** |

There is **nothing to preserve and nothing to conflict with** in the world domain. There is also **no engine in
this environment**, so every system below will be authored here and must be compiled and executed on an
engine-equipped machine before it can be called working (ADR-0005).

### 1.2 What the Art Bible supplies that engineering did not expect

| Register content | Why it matters to engineering | Status |
|---|---|---|
| Per-chapter location tables with ID, name, category, canon status, design status, `Added in` | A complete, authoritative world inventory with a stable identity scheme | Real; parseable; **parser landed** |
| Five location categories beyond `SUB`/`INT` — `ENV`, `SET`, `LMK`, `TRV`, `EXP`, `BOS` | World structure is already classified by *function* (landmark, traversal, exploration, boss arena) | Real |
| **Access levels** — FULLY / PARTIALLY ENTERABLE, VISUALLY ACCESSIBLE, BACKGROUND ENVIRONMENT, OPEN EXTERIOR | This is a **streaming and collision budget** in disguise | Real |
| Scene categories (AMBIENT NPC, WORLD ACTIVITY, ATMOSPHERIC, EXPLORATION, ENVIRONMENTAL STORYTELLING, …) | Population and performance budget, authored by design | Real |
| Per-scene NPC counts, routines, time-of-day and weather variants | NPC routine requirements, written per scene | Real |
| 40 environment-state references | Time/weather/pressure state requirements | Real |
| Per-scene "Required assets" and "Soundscape" lines | Asset and audio requirements per scene | Real |
| Board status per scene (`NOT STARTED` overwhelmingly) | Nothing is art-approved; build to blockout | Real |

### 1.3 A worked example of register-to-engine fidelity

`CH01-SCN-001 Woman Cooking Outside Her Door` (read verbatim from the scene register):

| Register field | Engineering use |
|---|---|
| Category: AMBIENT NPC SCENE | Tier 2 crowd actor, not a named actor |
| Access: OPEN EXTERIOR | Streaming cell resident; no door transition |
| Canon: PROPOSED | Cannot ship; blockout only |
| NPCs: one woman, one child | Two crowd slots; child flagged non-combat |
| Routines: cooks at dawn and dusk; at the farm between | Two routine states + one off-scene absence state |
| Time of day: day and night required | Scene must support both environment states |
| Weather: dry and rain | Two weather states |
| Interaction: greet her; she answers without stopping | Bark interaction, no dialogue tree, no quest |
| Gameplay relevance: **None required** | Explicitly no reward, no quest — engineering must not add one |

That last row matters. The register repeatedly states "no quest, no reward". **Adding a collectible or a quest
marker here would be inventing content**, which my remit forbids.

---

## 2. Corrections to the inherited canon model (already landed)

My Stage 0 work (Agent 3) modelled canon approval as an invented triplet:

```
approval: { design: bool, canon: bool, shippable: bool }
```

and ID'd boss arenas as `CHxx-BOSS-<Name>`.

Reading the registers in full shows **both were wrong**:

| Stage 0 (v1.0.0) | Registers (v2.9) | Consequence of the error |
|---|---|---|
| `approval.design / .canon / .shippable` booleans | Three-value `Canon Status`: `ESTABLISHED`, `PROPOSED`, `PENDING APPROVAL` | The triplet conflated two independent axes into one object and invented a "shippable" axis the registers do not have. It would have forced engineering to invent canon statuses for locations. |
| Separate `Environment Design Status` with 7 values: `NOT STARTED, EXPLORATORY, IN REVIEW, REQUIRES REVISION, CONDITIONAL, APPROVED, REJECTED` | Same, and it is **explicitly separate** from canon status (OAD-48) | Stage 0 flattened them. A `CONDITIONAL` design would have been recorded as a canon fact. |
| `CH01-BOSS-GreatRootMother` | `CH01-BOS-001 Great Root Mother Arena` | A wrong ID scheme would have propagated into level names, save data and evidence filenames. Costly to reverse later. |

**Correction landed and tested** (`Tools/canon/data/canon_index.json` v2.0.0, `canon_index.py`,
`test_canon.py`): the index now carries `canon_status` and `env_design_status` as separate fields with the
register vocabularies enforced as closed enums, plus a new `verified_against_register` flag so engineering
cannot assert a status it has not actually read. Nineteen new assertions pin the corrected model; the suite is
at **101 tests, all passing**.

I record this prominently because it is the exact failure mode the directive warns about: a plausible-looking
engineering abstraction quietly diverging from canon. It was caught by reading the authoritative document
rather than trusting the mirror.

**A second, still-open integrity issue:** locations referenced only by the memories document (e.g.
`CH04-SUB-002 The Shrine Landing`) have **not** been read from the Chapter 4 register section. They are now
marked `UNVERIFIED`, and the validator forbids presenting them as canonical. Six of the seven memory discovery
locations are in this state.

---

## 3. Missing systems

Ordered by dependency. "Blocks" names what cannot proceed without it.

| # | System | Why it is needed | Blocks | Complexity |
|---|---|---|---|---|
| W-01 | Chapter/world partition scheme + streaming budget model | 135 scenes, 191 location entries; no single level can hold a chapter | everything | High |
| W-02 | Location registry (runtime) + canon metadata access | Every system needs `CHxx-…` identity and status | interaction, quests, save | Low |
| W-03 | Environment state system (time, weather, supernatural) | 40 state references; scenes require day/night/rain | NPC routines, art, audio | High |
| W-04 | Interaction framework (`ITDDInteractable` + prompt plumbing) | Every exploration and memory beat is an interaction | memory director, quests, NPC dialogue | Medium |
| W-05 | Traversal handshake with Agent 1 | `TRV` and `EXP` locations exist to be traversed | exploration content | Medium |
| W-06 | NPC tier system (named / crowd / background) | 68 Chapter 1 locations with NPC life; 20 ambient scenes | all settlement content | High |
| W-07 | NPC routine + activity simulation | Registers specify per-scene routines and time variants | world believability | High |
| W-08 | Enemy AI core (perception, StateTree, perception of sound) | Chapters 1,2,3,5,7 need combat populations | bosses, chapter combat | High |
| W-09 | Boss phase graph executor | 8 bosses (ADR-0007) | chapter climaxes | Medium |
| W-10 | Memory director (7 × six-stage FSM) | ADR-0008; Ending 3 gate | endings, progression | Medium |
| W-11 | Quest/scene state tracking | 9 story scenes + 4 main story scenes (Ch08) | campaign flow | Medium |
| W-12 | Ending eligibility + campaign graph | 3 endings, hidden ending requires all 7 memories | shipping | Low |
| W-13 | World-state persistence (what changed) | Save/load of scenes, doors, bosses, memories | save system | Medium |
| W-14 | Ambient audio/visual scene drivers | 22 atmospheric scenes have no gameplay purpose | atmosphere | Medium |

---

## 4. Dependencies

### 4.1 On Agent 1 (Gameplay, Character, Combat)

I do not own the player controller, movement or combat. I need the following **contracts**, not implementations.

| ID | Need | Purpose | Proposed contract |
|---|---|---|---|
| A1-1 | `FTDDLocomotionState` + change delegate | NPC/ambient audio and AI reaction to player stance; traversal gating | Already specified in architecture §6.3 |
| A1-2 | `UTDDTraversalComponent` action list + query API | Traversal locations (`TRV`), ledges, liana bridges | `ETDDTraversalAction`, `bool CanPerform(action, context)` |
| A1-3 | Interaction verb handshake | Agent 1 owns animation; I own the interactable | `ITDDInteractable::GetInteractionVerb()` returning a tag Agent 1 maps to a montage |
| A1-4 | Damage/poise notification stream | Enemy and boss must react to hits without reading health directly | `OnDamageApplied(FTDDHitEvent)` |
| A1-5 | Attack telegraph registration | AI must know an attack is incoming for block/parry timing | `FTDDAttackWindowTelegraph` from ability activation |
| A1-6 | Player presence/stealth state | Enemy perception gating, NPC reactions | `UTDDPlayerContext` with `bIsStealthed`, `NoiseLevel` |

**Blocking risk:** A1-2 and A1-3 are needed before traversal and interaction can be completed. If Agent 1
changes the traversal action set after I build gating, my `TRV` scene data becomes invalid. **Therefore the
traversal action enum must be frozen before Stage 6.**

### 4.2 On Agent 3 (Integration, Technical Quality, Build)

| ID | Need | Purpose | Blocking? |
|---|---|---|---|
| A3-1 | Engine build + first boot (Stage 1) | Nothing I write can be compiled here | **Yes — hard block on all runtime work** |
| A3-2 | Gameplay tag registry parsed and validated | My systems are tag-driven | Yes, for integration |
| A3-3 | Save schema v1 with world-state section | Scene/quest/boss state must persist | No, but Stage 7 |
| A3-4 | Canon validator CI hook | My data must fail the build if non-canon | No, but strongly wanted |
| A3-5 | Evidence harness | My milestone reports need machine-readable evidence | No |
| A3-6 | Streaming/perf capture tooling | Budgets are meaningless unmeasured | Yes for Stage 6 gate |

### 4.3 On the Creative Director

| ID | Decision | Blocks |
|---|---|---|
| CD-1 | **D-01 binary content storage** | All environment content from Stage 6 |
| CD-2 | **D-10 cultural consultant** | Any shippable depiction of shrines, masks, deities, ritual spaces |
| CD-3 | Enemy archetype list (no canon source exists — I must propose one) | Stage 5 |
| CD-4 | Chapter 1 is the vertical slice — confirm its scene scope | Stage 6 |
| CD-5 | Whether `PENDING APPROVAL` locations (e.g. `CH01-SUB-001 The Abandoned Shrine`) may be built as blockout | Stage 6 |

---

## 5. Proposed world architecture

### 5.1 The two-axis truth model

Every location carries **two independent statuses** and engineering behaviour is derived from them:

| Canon status | Design status | Engineering may |
|---|---|---|
| ESTABLISHED | IN REVIEW | Build final-geometry blockout; author gameplay; ship-ready plumbing |
| PROPOSED | NOT STARTED | Build greybox only; no gameplay authoring beyond validation stubs |
| PENDING APPROVAL | any | Greybox **may be blocked by CD** (CD-5); no narrative content |
| any | APPROVED | Promote to art-ready; final assets permitted |
| any | REQUIRES REVISION | Nothing; the asset is being reworked |

This is enforced by a **content validation gate**, not by discipline: a scene manifest declaring a gameplay
element on a `PROPOSED` location fails the build (L0) unless the element is tagged `BlockoutContent`.

### 5.2 Chapter organisation and streaming

```
/Game/Chapters/CH01_ForbiddenForest/
├── L_CH01_Persistent            persistent level, World Partition, chapter director
├── Cells/                       auto-generated WP cells (cell size per chapter config)
├── Locations/                   one data layer per location id group
│   ├── DL_CH01-SET-001_HomeSettlement
│   ├── DL_CH01-SUB-018_WaysideOfferingPlace
│   └── ...
├── States/                      environment state variants (day/night/rain/supernatural)
│   ├── ES_CH01_Night
│   └── ES_CH01_Rain
├── Memory/                      CH01 memory playback sublevel (separate, canon rule)
└── Audio/                       chapter ambient + mix states
```

**Access level drives streaming policy** — this is the key economy, because it is authored data:

| Access level | Streaming | Collision | Tick | Budget share |
|---|---|---|---|---|
| FULLY ENTERABLE | Always resident when player in region | Full | Enabled | 1.0 |
| PARTIALLY ENTERABLE | Resident; distant parts culled | Simplified | Enabled | 0.6 |
| VISUALLY ACCESSIBLE | Resident when in sightline | None | Disabled | 0.2 (render only) |
| BACKGROUND ENVIRONMENT | Never streamed as geometry; impostor / skybox layer | None | None | 0.05 |
| OPEN EXTERIOR | Part of the region cell | Full | Enabled | 1.0 |

Proposed Chapter 1 budget (to be validated in Stage 6 — these are targets, not measurements):

| Metric | Target |
|---|---|
| Resident location entries at any moment | ≤ 12 |
| Resident scenes (Tier-2/Tier-3 actors included) | ≤ 20 |
| Active AI agents (enemies + named NPCs) | ≤ 14 |
| Crowd agents (Tier 2, Mass) | ≤ 60 visible |
| Background agents (Tier 3) | ≤ 120, no tick |
| Chapter stream-in to playable | ≤ 8 s |

### 5.3 NPC three-tier model (the core population decision)

| Tier | Who | Implementation | Tick | Count target | Interaction |
|---|---|---|---|---|---|
| **1 — Named** | The 13 supporting cast (Mgbafo, Obika, Ojiugo, Akuebue, Omenka, Ogbuagu, Okorie, Mgborie, Uchendu, Mgbokwo, Nwanyibuife, Onwuka, Unoka) | `ATDDNamedNPC` + StateTree + dialogue | Full | ≤ 4 nearby | Dialogue, quests |
| **2 — Crowd** | AMBIENT NPC SCENE and WORLD ACTIVITY SCENE populations | Mass entity + StateTree processor | LOD-ticked | ≤ 60 | Bark only |
| **3 — Background** | ATMOSPHERIC SCENE and BACKGROUND ENVIRONMENT figures | Instanced, animation via vertex/ISK on Mass; no individual logic | None | ≤ 120 | None |

Why this and not "all Mass": named NPCs need dialogue, quest hooks and precise animation; Mass is the wrong
tool for four characters with authored performances. Why not "all actors": 68 location entries in Chapter 1
alone cannot each carry an AIController.

**Routine model** (from the register's "routines" lines): each Tier-1/2 NPC has a `FTDDDailyRoutine` — an
ordered set of `(time window, location id, activity tag)` entries. The register authoring for SCN-001 gives:
cooks at dawn and dusk at `CH01-INT-007`, at the farm (`CH01-SUB-012`) between. That is directly encodable.
Routines are **data**, and a routine referencing an unregistered location fails validation.

**Canon guard:** the register's production note "Children appear only in the home settlement and are never
combat targets" is now a canon rule in the index (`RULE-NPC-CHILDREN-NO-COMBAT`) and will be a validation
failure if a child actor is ever added to a targeting profile.

### 5.4 Interaction framework

```cpp
// STATUS: SPEC
UINTERFACE(MinimalAPI, BlueprintType)
class UTDDInteractable : public UInterface { GENERATED_BODY() };

class ITDDInteractable
{
    GENERATED_BODY()
public:
    /** Canon location this interactable belongs to. */
    virtual FTDDLocationId GetLocationId() const = 0;

    /** What the player is about to do, as a tag Agent 1 maps to an animation. */
    virtual FGameplayTag GetInteractionVerb() const = 0;

    /** Tap or hold. Memory fragments require hold-to-commit (ADR-0008). */
    virtual ETDDInteractionMode GetInteractionMode() const = 0;

    /** Localisable, context-aware prompt. No UI code lives here. */
    virtual FText GetInteractionPrompt(const UTDDPlayerContext& Player) const = 0;

    virtual bool CanInteract(const UTDDPlayerContext& Player) const = 0;
    virtual void Interact(UTDDPlayerContext& Player) = 0;

    /** Fired for audio, telemetry and the memory director. */
    virtual FOnTDDInteractionCompleted& OnCompleted() = 0;
};
```

Three deliberate constraints:

1. **No UI inside interactables.** Prompts are view-models; Agent 3 owns presentation.
2. **The verb is a tag, not an enum I own**, so Agent 1 can add an animation without a code change in my module.
3. **Interactables never grant progress directly.** They emit events; `UTDDMemoryDirector` is the only authority
   that may advance a memory (ADR-0008).

### 5.5 Environment states

40 state references across the registers. Model: a state is a **data layer + parameter set**, never a separate
location (explicit register rule: "environment states are not locations").

```cpp
USTRUCT() struct FTDDEnvironmentState
{
    FName StateId;                 // e.g. ES_CH01_Night
    FTDDLocationId ParentLocation;
    FGameplayTag TimeOfDay;        // Dawn/Day/Dusk/Night
    FGameplayTag Weather;          // Dry/Rain/Mist/Storm
    FGameplayTag Supernatural;     // None/Thinning/Ancestral
    TArray<FName> DataLayers;
    FName LightingProfile;
    FName AudioMixProfile;
};
```

Scenes that declare time or weather variants (per the register) **must** have matching states, and a validator
reports any scene requiring a state that does not exist. That is how "Time-of-day variations. Day and night
states required" becomes a build error instead of a missed detail.

### 5.6 Enemy AI and boss architecture

Enemy AI is **StateTree**, per architecture §8.2, with perception fed by the audio system's sound events (my
domain) rather than by animation length guessing. Enemy archetypes **do not exist in canon**; I propose an
initial set for CD ratification (CD-3) rather than inventing them silently:

| Proposed archetype | Chapter fit | Role | Canon safety |
|---|---|---|---|
| Rootwarden | 1 | Slow heavy bruiser | Forest is ESTABLISHED; creature is invented, needs CD sign-off |
| Thrall | 3, 7 | Weak swarm, ash-dulled | Ch03/Ch07 are dead lands; no remains may be shown |
| Ash Hound | 3 | Fast flanker | Invented; must not imply a real animal rite |
| Ore Thrall | 2 | Slow, cold kingdom | No flame anywhere in Ch02 |
| Thunder Aspirant | 5 | Elite, storm-touched | Lightning white only |
| Maskbearer | 6 | Ch06 only; featureless invented face covering | Cultural review required |

**Explicitly excluded by canon and now by rule:** any python/snake enemy in Chapter 4
(`RULE-CH04-PYTHONS`), any child combat target (`RULE-NPC-CHILDREN-NO-COMBAT`), any remains in Chapter 3.

Boss execution is the declarative phase graph from ADR-0007. I am **not** building a boss in this pass; the
directive is explicit that bosses come after combat and enemy interfaces exist. What I will land first is the
graph *schema and validator*, so boss data can be authored and checked before any boss exists.

### 5.7 Quest, progression and the seven memories

- **Memory director:** seven independent six-stage machines (ADR-0008). Only seven exist; each is tracked
  separately; Ending 3 requires all seven committed with current content hashes.
- **Scene state:** each of the 135 scenes gets a `FTDDSceneState { Discovered, Completed, Variant }`. Most will
  never be queried — that is fine; it is a small dictionary and it makes "world remembers" possible without a
  bespoke flag per scene.
- **Quest structure:** the registers give 4 MAIN STORY SCENES and 9 SECONDARY STORY SCENES in total. That is a
  **very small** authored quest spine — the overwhelming majority of the world is atmosphere and exploration.
  Engineering must not build a large quest graph the content does not need. Concretely: a single linear campaign
  graph per chapter with optional side objectives, not a branching quest network.
- **No fast travel, no collectibles beyond the seven memories** — neither is canon-approved.

---

## 6. Risks

| ID | Risk | L | I | Mitigation |
|---|---|---|---|---|
| W-R1 | **Scope:** 135 scenes / 191 locations is far larger than a three-agent team can author | High | High | Vertical slice = Chapter 1's *story* spine + a representative subset of ambient scenes; ambient scenes are data-driven kits, not bespoke work |
| W-R2 | **No engine here:** none of this compiles or runs in my environment | Certain | High | Author schemas + validators (runnable), keep runtime C++ to frozen interfaces until Stage 1 evidence exists |
| W-R3 | **Canon drift:** my Stage 0 model was already wrong in two ways | Medium | High | Register parser + `verified_against_register` flag + closed vocabularies; §2 documents the correction |
| W-R4 | **6 of 7 memory locations unverified** against their chapter registers | High | High | Marked `UNVERIFIED`; cannot be presented as canon; must be read before Stage 7 memory work |
| W-R5 | **Population cost:** 20 ambient scenes in Ch01 with per-scene NPC counts and routines | High | Medium | Three-tier model with hard budgets; routine data validated; Mass for tiers 2–3 |
| W-R6 | **Streaming seam failures** across 46 scenes in one chapter | High | Medium | Access-level-driven policy; per-cell budgets; automated seam test in Stage 6 |
| W-R7 | **Environment states multiply content** (40 references) | Medium | Medium | States are layers + parameter sets, not duplicated geometry; validated against scene requirements |
| W-R8 | **CD-5 unresolved:** may `PENDING APPROVAL` locations be greyboxed? | Medium | Medium | Default to no; ask; greybox only ESTABLISHED + PROPOSED |
| W-R9 | **Agent 1 traversal enum freeze** | Medium | Medium | Freeze before Stage 6; my scene data depends on it |
| W-R10 | Boss arenas are `IN REVIEW`/unverified — building arena logic early wastes work | High | Medium | Phase graph schema only; no arena logic until Stage 5 |
| W-R11 | Culture-gated content (shrines, masks, oath ground) blocks shippable work | Medium | Very high | CD-2; nothing cultural progresses past greybox until consultant review |

---

## 7. Staged implementation plan

Dependency order per the directive. Each stage names what is **verifiable here** and what is **not**.

| Stage | Scope (my domain) | Verifiable in sandbox | Needs engine | Depends on |
|---|---|---|---|---|
| **W0** | Register parser, canon model correction, world manifest schema, scene/state validators | **Yes — done, 101 tests** | no | — |
| **W1** | Runtime location registry (`UTDDLocationRegistry`), chapter manifest data assets, content validation gate | schema + data yes; code no | yes (build) | A3-1 |
| **W2** | Interaction framework interfaces + prompt view-model contract | interfaces reviewed | yes | A1-3 |
| **W3** | Environment state system + scene state tracking | data model yes | yes | W1 |
| **W4** | Traversal gating integration with Agent 1 | no | yes | A1-2 frozen |
| **W5** | NPC tier system: named NPC actor, routine data, Mass crowd processor | routine data + validation yes | yes | W1, W3 |
| **W6** | Enemy AI: perception, StateTree base, 2 archetypes | no | yes | A1-4/5, CD-3 |
| **W7** | Boss phase graph schema + validator + executor; **no boss content** | schema/validator yes | yes | W6 |
| **W8** | Memory director (7 FSM) + ledger integration | **yes** — pure logic, headless-testable | yes (compile) | W2, A3-3 |
| **W9** | Quest/campaign graph + ending eligibility | **yes** — pure logic | yes | W8 |
| **W10** | Chapter 1 integration (vertical slice world) | no | yes | all above |
| **W11** | World simulation polish, ambient scene drivers, perf | no | yes | W10 |

**The two stages I can genuinely finish and prove without an engine are W0 and the logic half of W8/W9.**
That is deliberate: they are also the stages where a mistake is most expensive (canon identity and the ending
gate). I would rather land those with 100% test coverage now than leave them until an engine machine is
available.

---

## 8. Immediate next actions

1. **This document** — delivered.
2. **Land the register parser + corrected canon model** — in progress this pass, with tests.
3. **World manifest schema** — a validated, generated world inventory (`Tools/world/`) so chapter content can be
   checked against canon before it is built.
4. **Raise to Technical Director:** the canon-model correction (§2), the memory-location verification gap
   (W-R4), and CD-3/CD-5.
5. **Do not start runtime world code** until Stage 1 build evidence exists (ADR-0005). I will keep to interfaces
   and schemas until then.
