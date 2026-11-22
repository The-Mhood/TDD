# Agent 1 / Agent 2 Interface and Integration Review

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Prepared by:** Agent 3 — Integration / Technical Quality
**Review date:** 2026-11-16 UTC
**Review branch:** `arena/c64fc525-tdd`
**Local review base:** `5e3d1da4eee42ad8255760530291ff91cdfb39b2`
**Agent 1 source:** `arena/3bc206a0-tdd`, HEAD `bb2685c605efd4958b1c67944721c77e1b393931`
**Agent 2 source:** `arena/5dde91a4-tdd`, HEAD `ed36ad6d9cab946ede859e0dd1000a480b114f91`
**Status:** Review recommendations only. This document does not freeze interfaces, accept Agent 2's project skeleton, amend the canonical architecture, or authorize implementation.

## 1. Executive summary

The two agents have complementary scopes: Agent 1 owns player/controller, locomotion, traversal execution and combat mechanics; Agent 2 owns world structure, interactable content, scene/population/world simulation. Agent 3/Technical Director owns cross-agent Core contracts, shared build foundation, integration and evidence. The broad division is compatible, but the proposals are not yet one implementable API.

The highest-priority integration issue is **contract divergence**: the current architecture material uses more than one shape for interaction, locomotion/combat state, damage events, event lifetime/entity identity, and traversal. Agent 2's interface requests are consumers' needs, not a settled API; Agent 1's accepted M1 traversal/fallback rules are a design specification, not C++ or a frozen cross-agent type. Keep the specific M1 two-phase fallback/hold behavior as the reviewed movement design, while resolving the shared data and authority boundaries before implementation.

The published Agent 2 branch also contains an implementation-shaped Unreal project skeleton. It is not the canonical project: the local canonical checkout remains documentation/planning only, and the branch skeleton has not been opened or compiled with Unreal. Do not copy or merge it as the foundation by implication. Project bootstrap remains separately gated by the existing M0 checklist and TD decisions.

**No gameplay implementation, project creation, Unreal build, or gameplay test was performed for this review.**

## 2. Sources inspected

### Agent 1 (`bb2685c605efd4958b1c67944721c77e1b393931`)

- `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` — cross-module events, system ownership, Core ownership and change protocol.
- `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` v1.4 — accepted M1 design rules and proposed traversal/damage boundaries; `DESIGN_ONLY`.
- `docs/02_PRODUCTION/AGENT1/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` — ownership, Core blockers, Agent 2 handoffs and status claims.
- `docs/03_DECISIONS/ADR-0013-root-motion-policy.md` — v1.4, still marked proposed/provisional.

### Agent 2 (`ed36ad6d9cab946ede859e0dd1000a480b114f91`)

- `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` — locomotion, combat, interaction, world, tags, change process.
- `Docs/WORLD_ARCHITECTURE.md` and `Docs/WORLD_ASSESSMENT.md` — Agent 2 scope and requested Agent 1 interfaces.
- `Docs/DEPENDENCY_AND_BLOCKER_REGISTER.md` — current blocker/dependency inventory.
- `Docs/AGENT1_TRAVERSAL_CONTRACT_REQUEST.md` — unresolved traversal capability/data/failure questions.
- `Docs/W2M3_CORRECTION.md` and `Docs/evidence/agent2/W-M2.3_evidence.json` — W-M2.3 correction and evidence limits.
- `TDD.uproject`, `Source/TDDRuntime/TDDRuntime.Build.cs`, `Source/TDDRuntime/Public/Framework/TDDIds.h`, `Source/TDD.Target.cs`, `Source/TDDEditor.Target.cs`, `Source/TDDEditor/TDDEditor.Build.cs`, `Source/TDDTests/TDDTests.Build.cs`, and `Config/DefaultGameplayTags.ini` — reviewed as branch-specific project/build artifacts only.

### Canonical review workspace

- Local branch `arena/c64fc525-tdd`, HEAD `5e3d1da4eee42ad8255760530291ff91cdfb39b2` at review start.
- Existing modified `README.md` and untracked `docs/` were preserved. The local architecture, bootstrap decision and M0 checklist state that no canonical `.uproject` or runtime source is present and project creation is on hold pending authorization/decisions.

## 3. Proposed interface and ownership register

The table is a **review recommendation**, not an approved contract. “Publisher” means authority for the public contract and its change; implementation remains with the system owner. Agent 3/TD approval is required for shared Core/build changes.

| Surface | Proposed authority / publisher | Consumers | Review boundary / status |
|---|---|---|---|
| Core IDs, tags, value types, event bus and cross-system event structs | Agent 3 / TD | Agents 1 and 2; UI/persistence | One canonical Core definition. Use registered IDs/Gameplay Tags as appropriate; do not duplicate types in gameplay/world modules. TD acceptance required. |
| Player character/controller, input, locomotion, character state, camera, combat and traversal execution | Agent 1 | Agent 2 queries; Agent 3 integrates | Agent 1 owns mutation and execution. Consumers receive documented read-only snapshots/events or explicit commands, not direct writes into player internals. |
| `UTDDPlayerContext` (read-only player/world-facing façade) | Agent 1 publishes; Agent 3 reviews Core boundary | Agent 2 world/AI/interactables | Agent 2's requested position/facing/state/combat/target and stealth/noise fields need an agreed minimal version, lifetime, update semantics and authority. No Agent 2 writes through this façade. |
| Locomotion snapshot + change notification | Agent 1 | Agent 2 AI/audio/world response; Agent 3/UI | Keep locomotion distinct from combat/control state. Field taxonomy and event payload are unresolved; no polling contract until confirmed. |
| Traversal action/candidate/query and marker handshake | Agent 1 publishes; Agent 2 authors world markers/data; Agent 3/TD accepts shared contract | Agent 2 route gating, reachability, hint/scene data | Agent 1 owns execution and failure/abort behavior; Agent 2 owns authored opportunities/requirements. Enum, query context, route IDs, data-vs-code requirements and failure result remain open. |
| M1 abort arbitration, fallback, hold and restoration behavior | Agent 1 | Agent 2 only consumes stable results/events; Agent 3 integrates | M1 v1.4's accepted design: damage/forced-transition priority and the bounded relocation plus terminal hold phases. This does not itself freeze an enum/header or verify engine behavior. |
| Damage request/application authority and damageable receiver contract | Agent 3 / TD owns Core contract; Agent 1 owns combat/damage pipeline implementation | Agent 2 enemy/boss response | One application pipeline and one arbitration authority. Resolve `FTDDDamageRequest`, `ITDDDamageable`, stagger classification, and applied-event payload before consumers implement. |
| Attack telegraph / damage-window stream | Agent 1 owns combat timing payload and producer; Agent 2 owns AI/encounter scheduling and publishes intents through agreed API; Agent 3 arbitrates shared type | Parry/block and enemy fairness on both sides | Shared time units, clock/pause semantics, start/end/cancel, target/attack identity, and ordering must be explicit. No separate incompatible streams. |
| Interaction interface and focus/animation handoff | Agent 3/TD owns shared contract; Agent 2 implements world interactables; Agent 1 owns player focus/input/animation | Agent 1, Agent 2, narrative/progression | One contract must support prompt, eligibility, tap/hold/cancel lifecycle, verb tag and completion event without granting narrative/memory progress directly. Agent 2's location ID is useful if the canonical location ID is resolved. |
| Chapter/scene, streaming, population, routines and world simulation | Agent 2 | Agent 1 traversal/encounter integration; Agent 3 persistence/validation | Agent 2 owns world authoring and simulation boundaries. Authored counts/projections must remain distinct from measured runtime capacity. Runtime implementations are not evidenced by the reviewed documents. |
| Memory/quest/progression grant authority and persistence schema | Agent 3 / TD owns shared persistence and event contract; Agent 2 owns world triggers/director requirements | Agent 1 interaction/combat events | Interactables emit facts/events; they must not independently grant persistent progress. Preserve existing authority and save-versioning rules. |
| Unreal project, modules, targets, plugins, shared build and automation | Agent 3 / TD | All agents | Canonical project/version/platform/module topology must be decided and verified before implementation. Agent 2's skeleton is not accepted by this review. |

## 4. Shared contracts and conflicts to resolve

### 4.1 State taxonomies are currently conflated

- Agent 1's architecture defines a character state machine (`Idle`, `Locomotion`, `Attack`, `Block`, `Parry`, `Dodge`, `Stagger`, `Traversal`, `Interaction`, `Cinematic`, `Death`) and separately discusses locomotion and combat state.
- Agent 2's `FTDDLocomotionState` list includes `Idle`, `Walk`, `Jog`, `Sprint`, `Strafe`, `Land`, `Slide`, `Vault`, `ClimbLite`, `Ragdoll`, `Cinematic`; Agent 2 also proposes combat states/tags such as `State.Combat.Staggered`.
- Agent 1's proposed `ETDDCombatState` and `FTDDPawnKinematics` are identified as Core proposals, not Agent 1-owned frozen types.

**Recommendation:** publish distinct concepts for locomotion/stance, authoritative character action/control state, and combat status. Define transitions/authority and which snapshot is exposed to Agent 2. Do not force these lists into one enum or allow two state machines to answer the same “can act?” question.

### 4.2 Damage contract, event shape and identity conflict

- Agent 1's Core event proposal uses actor-free value events with `FGuid` entity IDs (`FTDDDamageAppliedEvent`, including amount/type/hit summary/lethal), and its proposal includes `ITDDDamageable`/`FTDDDamageRequest`.
- Agent 2 proposes `FTDDHitEvent` containing an attack definition, weak actor pointers, result enum, hit location and frame stamp, and requests `OnDamageApplied(FTDDHitEvent)` for enemy/boss reactions.
- Agent 2's `TDDIds.h` introduces `FTDDLocationId` and `FTDDMemoryId`, while world interfaces also use `FName` IDs. The reviewed source excerpt provides no shared traversal route-ID contract.
- Agent 1 M1 v1.4 reads a `bCausesStagger` classification on the request but explicitly leaves its storage as a proposal for Core review. Posture break and parry may also force stagger independently.

**Recommendation:** separate a transient local hit-resolution result (which may carry weak references for immediate presentation) from a durable/cross-module applied-damage event (stable entity IDs and value-only data). Decide one authority for hit arbitration/application and one stable identity policy. Resolve stagger cause as a semantic classification (field, tag, or damage-type rule) with a single source of truth; preserve M1 behavior without mandating the proposed storage field.

### 4.3 `ITDDInteractable` has incompatible lifecycles and signatures

- Agent 1 MEAD proposes prompt, `CanInteract`, `BeginInteract`, hold-progress `TickInteract`, `EndInteract`, `CancelInteract`, and optional requirements; it treats this as a Core contract owned by Agent 3.
- Agent 2's master architecture shortens this to `CanInteract(ATDDCharacter*)`, `GetPrompt()`, `Interact(ATDDCharacter*)`.
- Agent 2's world-assessment proposal adds `GetLocationId`, `GetInteractionVerb`, interaction mode, context-dependent localized prompt, `CanInteract(const UTDDPlayerContext&)`, mutable-context `Interact`, and `OnCompleted`.

These shapes are not source-compatible and differ on who owns focus/context, tap/hold/cancel, actor-vs-façade parameters, completion event delivery and ID type. **Do not implement against a guessed subset.** Recommend a Core-owned lifecycle contract with the player interaction component as caller, the interactable as eligibility/content provider and action receiver, the verb as a tag, and completion as a value event. Confirm whether requirements and location association belong in the interface or component/data.

### 4.4 Traversal is the critical unresolved handshake

Agent 2's blocker register calls traversal undefined and blocks route requirements, climbing and reachability; the contract request asks Agent 1 to decide:

1. The capability/action enum and stable vocabulary.
2. Whether authored route requirements are data (tags/IDs) or code-level queries, or a combination.
3. Failure semantics for unavailable/invalid actions and the response of the traversal system.
4. Status/acceptance of provisional fields and identifiers.

Agent 1 M1 v1.4 is specific about interruption, exit validation and fallback/hold but does **not** yet settle the full cross-agent traversal action/candidate/marker interface. Agent 2's route identifiers remain provisional. This is a hard blocker for route gating and offline reachability validation; do not freeze Agent 2's requested enum by assumption.

### 4.5 Event lifetime and temporal semantics are incomplete

Agent 1's event-bus design requires actor-free value events with stable entity IDs and weak-lifetime-checked subscriptions. Agent 2's hit event includes weak pointers; its interaction completion is a returned delegate reference. Telegraph windows are described as a stream without agreed clock, pause behavior, cancellation, identity or ordering. These may serve different local purposes, but their boundaries and ownership need documentation to prevent stale references, missed cancels or duplicate damage.

### 4.6 Duplicate system/build foundations

The Agent 2 branch skeleton has a monolithic `TDDRuntime` module with broad public dependencies; Agent 1's architecture proposes downward-layered modules including `TDDCore`, `TDDGameplay`, `TDDAI`, `TDDWorld`, `TDDNarrative`, `TDDUI`, `TDDEditor`, and `TDDTests`. The project descriptor names `TDDRuntime`, `TDDEditor`, `TDDTests`, and associates the project with UE `5.8`, while both target files set `IncludeOrderVersion.Unreal5_6`. This is a configuration discrepancy to resolve, **not proof the descriptor is invalid**; it was not evaluated by UBT/Unreal.

The branch has no `TDDCore` module in its module list, no gameplay implementation modules, and no `IMPLEMENT_*_AUTOMATION_TEST`/`BEGIN_DEFINE_SPEC` declarations in the inspected `Source/`. Its presence therefore does not satisfy Agent 1's Core/build/test blockers and is not evidence of a runnable project. Plugin/dependency allowlist and the choice of one initial module versus layered modules need one explicit TD foundation decision.

## 5. Dependencies and integration order

| Order | Contract/deliverable | Depends on | Blocks / acceptance evidence |
|---|---|---|---|
| 0 | TD foundation decision: canonical repo/project location, exact UE version/distribution, platform/toolchain, project/module strategy, plugin and source-control policy | Canonical TDD confirmation; no project file imported from Agent 2 by default | M0 checklist decisions recorded; no assumption based on `.uproject` association alone. |
| 1 | Core contract inventory and glossary: IDs, tag ownership, value/entity identity, events, time semantics, public API change/sign-off process | Order 0 architecture boundary; Agent 1/2 review | Every shared concept has one owner, one producer, explicit consumers, lifetime and status; duplicates/legacy alternatives marked superseded only by explicit TD decision. |
| 2 | Agent 1 ↔ Agent 2 traversal contract | Agent 1 M1 v1.4 design rules; Agent 2's contract request; Core/tag/ID decisions | Action vocabulary, route requirement representation, query parameters/results, marker/data responsibility, failure meaning, stable IDs and test plan signed off. This unblocks route gating/reachability, not unrestricted climbing content approval. |
| 3 | Player read-only context, locomotion/state snapshot and interaction handshake | Orders 1–2; Agent 1 player ownership; Agent 2 world use cases | One no-write façade; separate state dimensions; prompt/focus/verb/tap-hold-cancel/completion semantics; test matrix for valid/invalid/interrupt paths. |
| 4 | Damage, stagger, hit result and telegraph contracts | Order 1; Agent 1's damage pipeline; Agent 2 enemy/encounter response requirements | Single hit/damage authority; no duplicate application; stable event identity; lethal/stagger/parry precedence and telegraph start/update/cancel timing specified. M1's `DESIGN_ONLY` fallback/hold rules remain the behavior to implement and test, not a runtime claim. |
| 5 | Canonical Unreal M0 foundation and first project-owned automation test | Order 0; approved contract/module boundary; available authorized engine/toolchain | Actual project open and clean build plus a meaningful automation test with captured logs. Python/register/docs checks do not pass this gate. |
| 6 | World interfaces and data validation | Orders 2–5; Agent 2-owned world schemas; accepted save/event hooks | Route references resolve; interaction content uses the accepted contract; population projections retain provenance; no runtime capacity claims without captures. |
| 7 | End-to-end integration | All prior contracts and owners' implementations | Build and relevant Unreal automation pass; interaction/traversal/combat interrupts cross boundaries; scene/population behavior checked in representative map; report exact evidence and remaining blockers. |

Agent 2's dependency register correctly identifies no canonical project as the dominant runtime blocker, traversal as a hard contract blocker, and unratified content/data limitations separately. Interface design can proceed without ratifying enemy archetypes or consultant-gated visual/story content; implementation of those content-dependent systems cannot infer those approvals.

## 6. Agent 2 W-M2.3 data/evidence review

W-M2.3 corrects W-M2.2's exact “a dozen” interpretation to 12, marks all `npcs_is_measured` values false because the inputs are register-derived rather than runtime measurements, preserves range endpoints and their source wording for capacity planning, and reports 11.63 headroom as a **floor**, not a guarantee, because `CH01-SCN-014` is unbounded. The evidence metadata explicitly states there was no Unreal engine/GPU/compiled code and that runtime streaming, Mass Entity, AI, navigation and boss behavior are unimplemented/untested. Its Python checks support register-derived arithmetic/provenance validation only.

W-M2.3 open items remain: `CH01-SCN-014` needs a Creative Director ruling; the bounded-class count discrepancy needs TD confirmation; performance cost multipliers need measurement; and the 11 uncaptured scenes/13 of 57 locations remain data-capture limitations. These do not change the Agent 1/2 interface ownership recommendations above.

## 7. Exact Technical Director decisions requested

Record an explicit outcome (accept/reject/defer, with rationale and owner) for each before the dependent implementation begins:

1. **Canonical foundation:** confirm that the canonical TDD project remains the current repository and that Agent 2's branch skeleton is not adopted by default; specify project location if this changes. No copying/merging is implied here.
2. **Engine and toolchain:** select exact UE major/minor/patch/build and distribution, host/compiler/toolchain, first target platform, and permitted plugins. Resolve the Agent 2 descriptor/target include-order mismatch only after verifying against that actual engine.
3. **Module topology:** choose whether the first authorized foundation is one runtime module followed by evidence-based splits, or the MEAD layered modules; name module/Core ownership and permitted dependency direction. Reject broad public dependencies without feature justification.
4. **Core governance:** confirm Agent 3/TD as publisher of shared IDs, tag registry, Core events/interfaces and persistence types, with owner + consumers + TD sign-off/change record required for changes.
5. **State model:** specify separate locomotion, action/control and combat-status concepts; nominate Agent 1 as authority for player state mutation and the precise read-only state contract Agent 2 may consume.
6. **Traversal:** direct Agent 1 and Agent 2 to close the four questions in §4.4, approve the action/query/route requirement/marker/failure boundary, and identify stable route-ID policy. Preserve the accepted M1 v1.4 fallback/hold behavior unless changed through an explicit reviewed decision; clarify that this is design acceptance, not implementation verification.
7. **Damage/stagger/events:** choose the single hit arbitration/application authority; approve the split between local hit-resolution data and actor-free Core applied-damage events; resolve the semantic stagger classification and precedence, without presuming `bCausesStagger` storage. Set telegraph timing, identity, cancellation and clock semantics with both gameplay and world owners.
8. **Interaction:** choose one canonical `ITDDInteractable` lifecycle/signature covering player context, prompt/verb, requirements/location, tap/hold/progress/cancel, completion and progress-grant authority. Assign Agent 2 implementation, Agent 1 player-side routing/animation and Agent 3 Core publication, subject to the chosen module boundaries.
9. **W-M2.3 outstanding decisions:** rule on the open scene `CH01-SCN-014` content/count, resolve the bounded-class count discrepancy, and keep all remaining capacity figures explicitly projected/unmeasured pending engine captures. These are separate from contract acceptance.
10. **Implementation entry gate:** confirm the M0 entry checklist and evidence requirements (engine-open/build, project-owned automation, logs) before marking any runtime system implemented or verified. No docs/Python validation substitutes for Unreal evidence.

## 8. Acceptance criteria for this review artifact

- Both published branch heads and all reviewed documents are identified above.
- Proposed publisher/consumer boundaries, overlapping definitions, conflicts, unresolved inputs, and dependencies are explicit.
- Agent 1 M1 fallback/hold rules are retained as a reviewed design boundary without elevating proposals to frozen types.
- Agent 2's project skeleton and W-M2.3 evidence are correctly limited in authority/claims.
- The review does not implement gameplay, create a project, ratify content, or claim Unreal verification.
- All local relative Markdown links resolve; repository whitespace/diff checks pass.

## 9. Review outcome and outstanding status

**Outcome:** recommendations prepared for TD decision; no cross-agent API is frozen by this document.
**Implementation status:** none authorized or performed by this review.
**Unreal build/automation/gameplay status:** not run in this review; Agent 2's cited W-M2.3 evidence independently states engine/runtime work was not available or performed.
**Next step:** TD answers §7; Agent 1/2 revise their consumer/producer proposals against the accepted Core boundary; Agent 3 records the decision and prepares the authorized M0 foundation only when the checklist entry conditions are satisfied.
