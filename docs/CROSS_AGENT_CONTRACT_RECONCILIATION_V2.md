# Cross-Agent Contract Reconciliation — C-01 through C-07

**Document:** `TDD-INT-RECON-001` · **Version:** 2.0
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Governing record:** [`TDD-TD-INT-001 v1.2`](TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md), exact commit `e121bbbf09562e3cba0efe81aad971809685db23`
**Status:** Documentation and coordination only. Every contract below remains **DESIGN_ONLY / PROPOSED — NOT FROZEN**. No same-version Agent 1/Agent 2 approval is recorded.

## 1. Scope, source identity, and method

This revision reconciles the exact versioned submissions, not the old packets or historical design documents:

| Source | Exact version and commit | Document |
|---|---|---|
| Agent 1 | `A1-R1`, commit [`97828db7d9786c0fa5415578e796a822aab497a8`](https://github.com/The-Mhood/TDD/blob/97828db7d9786c0fa5415578e796a822aab497a8/docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md) | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md` |
| Agent 2 | `A2-C01…C07-1.0`, commit [`3ac438b32fcd73ceb22dcd81385356f7b8b39644`](https://github.com/The-Mhood/TDD/blob/3ac438b32fcd73ceb22dcd81385356f7b8b39644/Docs/CONTRACT_SUBMISSION_A2_V1.md) | `Docs/CONTRACT_SUBMISSION_A2_V1.md` |
| Technical Director | `TDD-TD-INT-001 v1.2`, commit [`e121bbbf09562e3cba0efe81aad971809685db23`](https://github.com/The-Mhood/TDD/blob/e121bbbf09562e3cba0efe81aad971809685db23/docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md) | `docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md` |

Agent 1 and Agent 2 each explicitly report zero agreements and zero frozen contracts in their exact submissions. Each response says counterpart agreement was not received. Compatibility, parallel suggestions, and silence are not approval. This report distinguishes: (a) verified source facts, (b) each agent's proposal, (c) actual textual differences, (d) questions needing agent/TD/design/save authority, and (e) tests/evidence claimed by the source. No source proposal is promoted into a decision here.

The prior [`Cross-Agent Contract Reconciliation v1`](CROSS_AGENT_CONTRACT_RECONCILIATION_V1.md) and v1.0 response ledgers are retained as historical records; their awaiting-submission state was accurate when written and is superseded only as a record of the present response state by the V2 reconciliation and V2 ledgers linked below.

### Status vocabulary

Each C-01…C-07 row uses exactly one status from the required set: `PROPOSED`, `RECONCILIATION IN PROGRESS`, `AGREED BY BOTH — PENDING TD`, `TD REVIEW REQUIRED`, `FROZEN`. Here every contract is design-only/proposed and none is agreed or frozen. `TD REVIEW REQUIRED` marks an identified decision boundary, not a decision already made.

## 2. Authority boundaries retained

- **Agent 1** owns player mutation, traversal execution, player-hit arbitration (including hits where the player is victim), and player interaction routing. Agent 1 alone mutates player state.
- **Agent 2** owns world-authored route/interactable requirements and data; supplies enemy hit intent; consumes authoritative outcomes; does not mutate player state or apply damage to the player.
- **Agent 3 / TD** governs shared Core publication/integration, registry policy and cross-agent decisions.
- Health/attribute application remains independent of control-state resolution. Preserve **Dead > Cinematic > Stagger**, and retain M1 v1.4 traversal abort-window, fallback and restoration semantics without reinterpreting them.
- No API, Core type, enum, tag namespace or behavior is frozen by this reconciliation.

## 3. Contract-by-contract reconciliation

### C-01 — Traversal vocabulary, route identity, requirements and query

**Status: `RECONCILIATION IN PROGRESS`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §1):** Five grounded capabilities: `Vault`, `Mantle`, `LedgeShimmy`, `Drop`, `ClimbLadder`, with requested `Traversal.Capability.*` tags and executable behavior/entry/exit definitions. Agent 1 proposes the player-side query and deterministic selection, entry/exit collision validation, frame-scoped query results with execution-time revalidation, distinct outcomes, and sole ownership of player traversal execution and mutation. Requested marker data includes route identity, capability/requirements, anchors, priority, direction/gating and diagnostic location/scene fields. Marker representation is left to Agent 2. Agent 1 explicitly retains M1 v1.4: bounded fallback attempts, always-run terminal hold, validation at each write, restoration ordering, and out-of-world handoff. No silent modification of fallback/hold/restoration is proposed.

**Agent 2 proposal (`A2-C01-1.0` §4):** Authored route record plus runtime marker actor, a parent location ID, entry/exit anchors, route direction, failure mode, requirement grouping and evidence source. Agent 2 prefers data-driven requirements (enum shape with AND/OR groups and tag escape hatch) to enable offline validation, but leaves capability names to Agent 1. Agent 2 proposes route availability/blocked/unloaded/invalid semantics and separate authoring-validator results. Agent 2 expressly assigns route data to itself and execution/capability resolution to Agent 1.

**Verified location-register fact:** `LOCATION_MASTER_REGISTER` v2.9 has a multi-valued `Category`; `Traversal Area` is one category value, not an ID family. The Agent 2 capture reports eight CH01 locations carrying that category, including `CH01-SUB-009`, `CH01-SUB-020`, and `CH01-EXP-003` (as well as five `CH01-TRV-*` locations). The two established entries are `CH01-SUB-009` and `CH01-TRV-005`. Preserve this as a source-data fact, not a new canon decision; do not modify the register.

**Correctable inconsistency in A2 proposal:** A2's prose correctly anchors route parents to any location whose multi-valued Category includes `Traversal Area`, but its named L0 test uses `^CH01-(TRV\\|EXP)-\\d{3}/ROUTE-[A-Z]$`. That expression both tests the wrong identity rule and excludes permitted `SUB` parents, including `SUB-009` and `SUB-020`; it also excludes `EXP-003` under its current family group. Replace the recommendation with two distinct checks: (1) a format/syntax check that validates the route suffix and accepts every permitted registered location-ID family without asserting traversal eligibility from prefix; (2) a semantic check resolving `ParentLocationId` to the authoritative register and requiring that the parent's multi-valued Category contains `Traversal Area`. The specific regex implementation and category normalization remain to be agreed; do not freeze the pattern here.

**Unresolved between proposals:** data-vs-code requirement representation and offline reachability; capability set AND/OR/cumulative behavior, revocation, water/rope context; route key format and `ROUTE-` namespace reservation; route identity stability/persistence; actor/data representation and registration; marker/query lifetime differences; execution-time invalidation. A1's query reports `UnsupportedByPlayer`, `InvalidAuthoredData`, `BlockedPath`, `WorldUnavailable`, `Cooldown`; A2 uses `Unsupported`, `Blocked`, `Unloaded`, `Invalid`, `NoCandidate`. Do not map or collapse these outcome vocabularies without explicit review. A2's silent blocked/unsupported presentation preference cannot override M1 v1.4.

**Reconciliation direction (not a decision):** preserve A1 execution and M1 v1.4 behavior; preserve A2 authored-data authority. Validate route syntax independently from the parent-location/category semantic check. Require A2 to respond to A1-R1's five capability definitions and exact query/failure semantics; require A1 to respond to the proposed data/validation needs, category-based route anchoring, and route lifecycle. Keep a location register's category, not a prefix, as the semantic source for traversal-capable parents.

### C-02 — Read-only player context and state snapshots

**Status: `RECONCILIATION IN PROGRESS`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §2):** Three separate snapshots (locomotion, action/control, combat) in one consistent frame envelope, published after movement; read-only by-value access, Agent 1 sole mutation authority, one-frame freshness and invalidation during unpossessed/despawn/transition conditions. Proposed fields include position/rotation/aim, velocity/speed/grounding/movement mode, distinct control and combat state, alive/health/posture projections, stagger/telegraph values, target identity, and frame/time metadata. Health and posture are explicitly conditional on real Agent 2 consumer need; stealth/noise is not provided absent approved design/use case. Polling continuous values plus discrete transition events is proposed.

**Agent 2 proposal (`A2-C02-1.0` §5):** A single immutable snapshot with `Location`, `Facing`, locomotion state, `bInCombat`, interaction target, carry state, and frame stamp. `Velocity` and `CameraForward` are requested but not required; health, stealth, surface type and stamina are withdrawn. Named consumers include the interaction router, crowd subsystem, chapter/memory directors, traversal gating and telegraph targeting. Agent 2 proposes query for continuous levels and events for transitions, ≤2-frame freshness for commit, invalid rather than invented zero-vector context, and read-only use.

**Comparison:** shared direction is a read-only A1-authored source with named world consumers and freshness/validity handling. The concrete taxonomies differ: A1 separates locomotion/action/control/combat; A2's single snapshot adds `bInCombat` and `CarryState` and does not name all A1 fields. A1 has fields A2 withdraws (notably health) and A2 asks for camera-forward/velocity conditionally; A1 has aim direction and a target/identity pair. Their invalidity semantics also differ (`Get...` false/invalidation events versus `bValid=false`). These are proposal differences, not a bilateral disagreement because A2 has not reviewed A1-R1.

**Field reconciliation matrix — proposed labels only, pending agreement:**

| Field/group | A1-R1 proposal | A2-1.0 position | Reconciliation label (not an accepted contract field) |
|---|---|---|---|
| Location / position | `ActorLocation` required; capsule/world-space frame data | `Location` **REQUIRED** for crowd/router | **Required by both proposals**; exact frame/source to align |
| Facing / aim | `ActorRotation`, `AimDirection` required | `Facing` **REQUIRED**; `CameraForward` **REQUESTED, not required** | **Required:** actor facing; **conditional/requested:** camera-forward; aim-direction mapping unresolved |
| Velocity / speed | `Velocity`, `Speed2D` required in locomotion snapshot | `Velocity` **REQUESTED, not required** | **Required in A1 proposal; conditional/requested in A2 proposal** pending named decision/consumer confirmation |
| Grounding / height / movement mode / slope | Grounded, height, `MovementMode`, slope, walkable-floor fields proposed required | `LocomotionState` **REQUIRED** for traversal/router; specific scalar details not requested | **Required at A2's abstract locomotion level; unrequested at A2 for individual slope/height fields** pending whether a named consumer needs them |
| Control/action state and input lock | `ControlState`, tag, elapsed time, `bAllowsInput`, `bLocked`, `ActiveActionId` proposed required | No direct corresponding fields named | **Unrequested by A2 so far**; A1 proposal remains, require a named A2 use before shared inclusion |
| Combat/alive state | CombatState, alive, stagger state/timer, telegraph state/timer proposed required | `bInCombat` **REQUIRED**; no explicit health or combat substate fields | **Required by A2:** `bInCombat`; **unrequested by A2:** remaining A1 combat fields pending consumer mapping |
| Health / posture fractions | A1 **CONDITIONAL** on actual Agent 2 phase/aggression use | A2 health **WITHDRAWN**; no posture request | **Conditional in A1 / unrequested by A2**; exclude absent explicit consumer; no direct A2 attribute-set reads |
| Carry state | No matching field explicitly enumerated in A1 snapshot; traversal request tags/context may need resolution | `CarryState` **REQUIRED** for route gating | **Required by A2, unrequested in A1's current field list**; A1 to state whether carried context belongs in query/snapshot |
| Interaction target / IDs | Weak `CurrentTarget` and stable target `EntityId` proposed required | `InteractionTarget` **REQUIRED** | **Required by both proposals** in concept; identity/lifetime representation unresolved |
| Frame/time/freshness and invalidity | Frame counter, world/gameplay timestamps, false query + invalidation event; one-frame validity | Frame stamp; stale >2 frames blocks commit; invalid snapshot rather than zero vector | **Required by both proposals** in concept; exact stale threshold, invalidity and event semantics remain open |
| Stealth/noise, surface type, stamina | A1 stealth/noise **not provided** absent approved use | A2 **WITHDRAWS** stealth, surface type and stamina | **Unrequested by both** for this proposal set; no inclusion without new approved design/consumer |

**Reconciliation direction (not a decision):** retain A1-exclusive mutation. Ask A2 to affirm or correct the matrix field-by-field against named consumers and decisions, particularly `Velocity`, `CameraForward`, `CarryState`, A1 control/combat fields and field-level locomotion detail. Ask A1 to respond to A2's `bInCombat`, carry and interaction use cases plus proposed invalid/staleness behavior. Keep three state taxonomies separate; no merged mega-state. Remove any field lacking an agreed consumer. Health and posture remain conditional, with no direct A2 attribute-set access.

### C-03 — Hit intent, arbitration, application and applied fact

**Status: `RECONCILIATION IN PROGRESS`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §3 and §8.1):** Resolve hit intent through one authoritative player-side arbiter for hits involving the player, apply health independently of control-state resolution, define duplicate/stale/invalid request handling, and publish proposed applied outcomes. Agent 1 lists unresolved event scope for blocked/parried/posture-only outcomes, payload amount and publisher for hits on A2-owned actors. Agent 1 raises a real tension: MEAD §5.4's attacker-driven flow may be read as allowing A2 to resolve hits, while A1 requires exclusive arbitration when the player is victim. Agent 1 gives alternatives, prefers A1 arbitration for all hits involving the player, and does not silently reinterpret the text.

**Agent 2 proposal (`A2-C03-1.0` §6):** A2 supplies enemy/boss hit **intent** only; Agent 1 arbitrates and applies; shared applied event is the authoritative fact consumed by A2. A2 rejects direct health writes, hit computation, mitigation, and resolution-based enemy reactions. It proposes a request/event shape, unique event ID and deduplication, and says target-unload is dropped (A1 must review). Agent 2's flow is directionally consistent with A1's preferred authority but is not explicit approval of A1-R1 and does not settle exact request, payload or target-unload semantics.

**Required event stages:** keep separate (1) authored attack intent, (2) hit detection and arbitration/resolution, (3) defence/mitigation decision, (4) health/attribute application, (5) exactly-once authoritative applied event, and (6) consumer reaction. A resolution candidate is not an applied fact. For each successfully applied hit there must be one authoritative application and one corresponding applied event; rejected/no-hit intent must not be represented as applied. Health application remains independent of Stagger/Dead/Cinematic arbitration. A2 reactions consume the applied fact, not a provisional resolution. Exact inclusion of blocked, parried, immune, posture-only, clamped/raw amount, publisher for A2-owned targets, and unload behavior remain unresolved.

**Reconciliation direction (not a decision):** clarify MEAD §5.4's attacker-driven diagram: it may express who authors/initiates the attack but cannot confer hit arbitration authority for a hit involving the player. Request an explicit Agent 1 acknowledgement or revision. Ask A2 to explicitly confirm A1-R1's exclusive player-victim hit arbitration and distinguish intent payload, resolution result, application and event consumers. Preserve A2's enemy intent and outcome-consumption responsibilities. Retain one event authority and exactly-once semantics as a design requirement for TD review; do not choose the open payload cases here.

### C-04 — Stagger classification and forced-state outcome

**Status: `TD REVIEW REQUIRED`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §4):** Keep `bCausesStagger` provisional. It compares bool, enum, tag/data mapping and Gameplay Effect alternatives; recommends an enum, accepts a bool as a smaller fallback, and rejects the Gameplay Effect option because classification after application would invert M1 ordering. Agent 1 owns player classification/state transition. It preserves **Dead > Cinematic > Stagger**, exactly one winning forced transition, health independence, fallback/restoration order and M1 v1.4 exit behavior.

**Agent 2 proposal (`A2-C04-1.0` §7):** Treats forced outcome as an authoritative event/state consumed by world AI; no independent player-state authority. Agent 2 requests an applied event shape and asks whether a recovery-from-stagger event exists. It states A1/TD precedence and describes its consumer behavior, but provides no agreement to A1's classification representation.

**Unresolved:** TD-02 representation; event/outcome payload; whether a recovery event belongs in shared scope. Recovery remains an open question unless A1 and TD answer; do not add it as independent state authority and do not assume polling versus event. Agent 2's request for notification is a consumer requirement to evaluate, not authorization to publish another state authority.

**Reconciliation direction:** preserve precedence and M1 behavior; route representation and recovery boundary to explicit A1/TD review. Health application cannot be conditioned on classification or transition success. Any recovery event, if later approved, reports a transition from A1 authority; it cannot write a parallel state.

### C-05 — Telegraph lifecycle, gameplay time and parry timing

**Status: `RECONCILIATION IN PROGRESS`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §5):** Agent 2 authors enemy telegraphs and lifecycle; Agent 1 authors player telegraphs and consumes enemy timing. Proposes unique non-reused attack-instance identity, Opened/PhaseChanged/Closed lifecycle, one shared gameplay-time definition, phase overlap on the same frame for parry, half-open active windows, event ordering, and close/invalidation on completion, interruption, death, unload and supersession. World pause stops time; time dilation/hitstop scales with the animation. Clock owner, late-subscriber query and exact event surface remain open.

**Agent 2 proposal (`A2-C05-1.0` §8):** Proposed event-driven enemy-telegraph producer with `AttackInstanceId`/attack identity, timings/windows, phase/cancel reasons and target/world lifetime. It names pause/time dilation and source lifecycle concerns; its proposed timestamp/phase/consumer path and cancellation detail differ in specifics from A1. A2 does not explicitly approve A1-R1's same-frame overlap/boundary and time source.

**Reconciliation direction (not a decision):** prepare a shared timeline example for open → phases → close/cancel, covering pause, dilation/hitstop, parry at exact window boundaries, attack interruption, source death/unload and late subscription. Ensure telegraph intent never applies damage and C-03 alone arbitrates hits. Resolve one gameplay clock and ID lifetime before matching producer to parry consumer; neither agent rewrites the other's timestamps. Event-only versus query snapshot remains open.

### C-06 — Interaction routing, world lifecycle and cancellation

**Status: `TD REVIEW REQUIRED`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §6):** Agent 1 owns player focus/input/router, hold timing/progress, session state and cancellation; Agent 2 owns world actor state, prompt data and completion result. Proposes Begin/Tick/End/Cancel lifecycle, tap and hold, focus/eligibility/range checks, exactly-once terminal call, and cancellation before forced-state entry. It says router does not grant memory/quest/item/checkpoint progression. Stream-out/destruction, damage, stagger, death, cinematic, level transition and focus changes are cancellation triggers. A1 proposes router-owned progress and enumerates `Damaged` cancellation after health commit but before control-state resolution.

**Agent 2 proposal (`A2-C06-1.0` §9):** Agent 2 implements world interactables with eligibility, localized prompt, mode, requirement, location/scene identity and begin/end/cancel. Agent 2 explicitly does not consume progress (unless a read-only optional progress callback is agreed), does not own the timer, and does not grant persistent progression; completion is an event/fact consumed by the appropriate progression subsystem. Tap/hold examples vary by authored category. Stream-out and requirement invalidation cancel. Agent 2 proposes damage interruption but explicitly says it is a design decision, not decided.

**Unresolved difference and required TD/design escalation:** Agent 1's proposed interface sends progress each frame; A2 says begin/end/cancel only (optional read-only progress callback). A1's default says damage interrupts a hold; A2 marks damage interruption as a decision required. Agent 2 proposes an interaction-completed fact and separate world completion semantics; A1's API has End result but no identical shared event shape. Router/world ownership, focus, eligibility, tap/hold, progress, exactly-once terminal behavior, completion authority, progression boundary, stream-out/destruction and level-transition cancellation must be aligned. Escalate **whether damage interrupts an active hold** to TD/design if the agents do not explicitly agree; do not adopt A2's suggested default or A1's proposed behavior as a decision.

**Reconciliation direction:** preserve A1 router and player mutation ownership, A2 actor-local state, and no direct progression grant from router or interactable. Agree completion fact versus grant separately. Provide a single sequence table for Begin, progress, completion, cancellation and forced-state ordering. Hold-progress consumer semantics are still open.

### C-07 — Runtime, authored, route and interactable identities; tags

**Status: `TD REVIEW REQUIRED`** · **DESIGN_ONLY / PROPOSED — NOT FROZEN**

**Agent 1 proposal (`A1-R1` §7):** Distinguishes runtime entity identity (session lifetime), authored content identity (potential save lifetime), and canon place identity. Requests tags across existing/requested namespaces; proposes runtime entity IDs non-persistent, authored IDs retirement-governed if referenced, unknown/retired handling, and TD-owned registry/type publication. Route ID persistence depends on whether narrative/checkpoint content references routes.

**Agent 2 proposal (`A2-C07-1.0` §10):** Requests TD-owned tag namespace and registry, distinguishes content keys/route keys from runtime handles and display labels, and notes no authoritative interactable ID source exists. Agent 2 gives options (scene-derived key, new family, or transient actor) conditioned on save persistence; it prefers no persistent ID for transient state and seeks a TD/save decision before selecting. Agent 2 retains register provenance/version and retirement/non-reuse concerns.

**Unresolved:** runtime ID's exact Core form/lifetime; authored/route/interactable persistence and save consumers; namespace grants; tag inventories/naming; unknown/retired resolution; retirement and non-reuse policy. No namespace or save policy is granted here. Do not commit to an interactable ID family before Agent 3/save requirements and consumer references are known. Distinguish runtime/authored/route/interactable/canon-location IDs and tags; display labels are not keys.

**Reconciliation direction:** collect concrete consumer/save references per ID family, including route and interaction completion references; then TD/Agent 3 decides registry and persistence policy. Keep IDs opaque to runtime code unless a validator needs syntax. Preserve the no-reuse principle as a proposed safety requirement, pending governance approval and source-register policy.

## 4. TD decision register — A1 TD-01…TD-09, reviewed against v1.2

No row below declares a new TD decision. v1.2 itself establishes coordination/authority boundaries and says contracts remain awaiting; it does not resolve these implementation/design choices. TD-01 is a factual correction; acknowledgment remains requested, not presumed.

| Item | Exact issue / reconciliation | Current disposition | Needed owner/action |
|---|---|---|---|
| **TD-01** | A1 §0.2 and A2 §0.1 say v1.2 was absent, based on their packet baseline/main visibility. Verified fact: v1.2 exists on Agent 3's published branch at `e121bbbf09562e3cba0efe81aad971809685db23`; it was absent from the then-used packet baseline and `main`. This difference in visibility is not evidence either agent had received it. | **Corrected fact; no design decision.** | Request A1 acknowledge/rebase affected interpretation if needed; ask A2 likewise to acknowledge v1.2. Neither request has been sent. Review both responses against v1.2 before sign-off. |
| **TD-02** | C-04 stagger representation: bool, enum, tag/data mapping, or Gameplay Effect; consequences described in A1-R1 §4.2. | **OPEN.** Do not permanently choose `bCausesStagger` or any representation. | TD decides after A1 and A2 explicitly review the same proposal; preserve M1 ordering. |
| **TD-03** | C-03 applied-event scope, blocked/parried/posture-only cases, amount semantics, and publisher for A2-owned targets. | **OPEN.** A2 supplies intent/consumes outcome; A1 proposal has alternatives. | A1/A2 enumerate event semantics and exactly-once authority; TD decides shared payload/publisher questions. |
| **TD-04** | C-01 route ID format/stability, route persistence references and `ROUTE-` namespace. A2's category-based parent rule and regex defect are recorded in C-01. | **OPEN.** No namespace or persistence policy granted. | A1/A2 identify consumers and exact route references; TD reviews identity/namespace. Correct regex/category validation before any test claim. |
| **TD-05** | C-02 stealth/noise inclusion. A1 excludes without approved use; A2 withdraws stealth and health, while its other consumer fields need exact review. | **No stealth/noise field proposed for inclusion now; not a permanent exclusion decision.** | Revisit only with approved design and named consumer. A2 explicitly classify A1 fields as required/conditional/unrequested. |
| **TD-06** | C-05 canonical gameplay clock ownership and time semantics. | **OPEN.** A1 recommends a Core gameplay-time subsystem; no approval. | Align one timeline, pause/dilation/hitstop, frame-boundary and late-subscriber requirements, then TD chooses ownership. |
| **TD-07** | C-06 hold-progress authority, with related A2/A1 mismatch on progress delivery. | **OPEN.** A1 proposes router-owned progress; A2 requires begin/end/cancel only unless optional callback. | A1/A2 agree what world objects observe; TD decides only remaining shared contract boundary. |
| **TD-08** | C-07 tag approval and ID retirement/persistence registry policy. | **OPEN.** No tags, namespace or save policy approved by this report. | Agent 3/save owner supplies consumers and persistence requirements; TD governs registry and retirement. |
| **TD-09** | MEAD §5.4 attacker-driven hit flow versus exclusive A1 arbitration for hits involving player. | **OPEN.** A1's option 1 is recommended by A1; A2's flow is directionally aligned but is not explicit same-version approval. | TD clarifies MEAD intent after A1 acknowledgment and A2 explicit confirmation/counterproposal; preserve one authoritative hit arbiter for player-victim cases. |

### Other A2 escalation items (kept separate from A1 TD-01…09 numbering)

A2 also raises: **damage interrupts hold** (C-06/design), **interactable persistence/ID** (C-07/save), **route namespace**, **category vs prefix** (corrected as above), **blocked traversal feedback** (must not override M1 v1.4), and **C-04 recovery event** (unresolved; if any, it cannot become an independent state authority). A2's TD numbering is not the A1 TD numbering; this report cross-references by topic and does not renumber or treat A2's defaults as rulings.

## 5. Unresolved divergence and disagreement register

**No cross-agent disagreement has been recorded as a mutually reviewed dispute:** neither agent has explicitly reviewed/approved the other's exact proposal version. The following are proposal-level differences or missing decisions, not assertions that either agent has accepted or rejected the other's position.

| ID | Topic | A1 exact position | A2 exact position | Classification / next step |
|---|---|---|---|---|
| D-01 | C-01 requirement representation | Five executable capability definitions; marker requirements and query boundary proposed; data-vs-code still open. | Prefers data-defined enum requirement with AND/OR groups plus tag escape hatch; capability names deferred to A1. | **Unreviewed proposal difference.** A1 answer data/offline validation and cumulative/revocable/context requirements; A2 answer A1 vocabulary and query semantics. |
| D-02 | C-01 outcomes/validation | Distinct player query outcomes and M1 execution fallback. | Distinct world availability outcomes and L0 authoring diagnostics. | **Not yet mapped.** Compare semantics case-by-case; no silent enum mapping. Correct prefix regex and category semantic check. |
| D-03 | C-02 snapshot structure | Three separate locomotion/action-control/combat snapshots; some conditional fields. | One immutable snapshot with narrower fields plus `bInCombat`, `CarryState`; velocity/camera-forward requested; health/stealth withdrawn. | **Unreviewed field-level divergence.** Apply required/conditional/unrequested matrix; preserve A1-only mutation. |
| D-04 | C-03 target unload/payload | Alternatives remain open for event cases/publisher/payload. | Proposes dropping target-unload event; asks A1 for applied event contract. | **Unreviewed policy question.** Decide only after A1 reviews exact case and all consumers. |
| D-05 | C-03 arbitration | A1 must arbitrate hits involving player; MEAD §5.4 tension called out. | A2 flow: A2 intent → A1 arbitration/application → applied event → A2 reaction. | **Directionally aligned, no same-version approval.** Clarify diagram intent and obtain explicit A1/A2 confirmation. |
| D-06 | C-05 time, IDs and timeline | Gameplay-time, same-frame phase overlap and lifecycle rules proposed; clock owner open. | Enemy producer stream and lifecycle proposed; not explicit review of A1's boundary rules. | **Not reconciled.** Agree timeline fixture and clock owner before API review. |
| D-07 | C-06 progress semantics | Router owns time/progress and proposed per-frame Tick; damage cancels in A1 proposal. | World sees Begin/End/Cancel, no progress by default; damage interruption is explicitly undecided. | **Material unreviewed divergence + design escalation.** Request explicit choice; escalate damage-interrupts-hold if no agreement. |
| D-08 | C-06 completion and progression | Router reports end result, does not grant progression. | World emits completion fact; progression subsystem grants. | **Potentially compatible, shape unresolved.** Agree exactly-once event/result and ownership without granting progression to either actor/router. |
| D-09 | C-04 recovery event | A1 response does not settle a shared recovery event. | A2 requests recovery-from-stagger event; TD review sought. | **Unresolved dependency.** A1/TD must state whether in scope; if approved it is notification only, not state authority. |
| D-10 | C-07 identity/persistence/tags | Runtime/authored/canon identities and proposed lifetime rules; tag inventory. | Content/route keys and runtime handles; interactable identity unresolved pending save authority; separate tag inventory. | **Governance question.** Require save/consumer inventory before namespace or persistence selection. |

## 6. Copy-ready Agent 2 request (prepared, not sent)

No direct agent messaging/assignment workflow is available in this session. This exact message is ready for the user to deliver; it has **not** been sent.

> **To Agent 2 — please review Agent 1's exact response `A1-R1` v1.0** at https://github.com/The-Mhood/TDD/blob/97828db7d9786c0fa5415578e796a822aab497a8/docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md against your exact proposal `A2-C01…C07-1.0` at https://github.com/The-Mhood/TDD/blob/3ac438b32fcd73ceb22dcd81385356f7b8b39644/Docs/CONTRACT_SUBMISSION_A2_V1.md and governing `TDD-TD-INT-001 v1.2` at https://github.com/The-Mhood/TDD/blob/e121bbbf09562e3cba0efe81aad971809685db23/docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md. For **each C-01 through C-07**, state explicitly `AGREE` or `DISAGREE` with A1-R1's specific proposal/version, or provide a numbered counterproposal and the exact affected clauses. Do not infer agreement from compatible direction or silence; identify any agreement as approval of the same exact version, or issue a revised version for both agents to review. In C-01 address the five A1 capabilities, data/code requirements, AND/OR/cumulative and revocation/context behavior, route identity, marker lifetime, outcomes, and category-based parent validation. Confirm a syntactic route-key check must accept the permitted `SUB`/`EXP` families and a separate semantic check must resolve parent IDs and require multi-valued Category membership `Traversal Area`; correct the regex in A2 §3.7. In C-02 classify every A1 field as required, conditional, or unrequested and justify each with consumer/use; expressly resolve `Velocity`, `CameraForward`, `CarryState`, health/posture and event/query cadence. In C-03 explicitly approve or counterpropose exclusive A1 arbitration for every hit involving the player, resolve the MEAD §5.4 diagram interpretation, and distinguish intent, detection/arbitration, defence, application, exactly-once applied event and reaction; list event cases/payload/unload needs. In C-04 address the preserved precedence and whether recovery notification is needed without creating another state authority. In C-05 provide one timeline for gameplay clock, pause/dilation/hitstop, phase overlap/parry boundary, IDs and invalidation. In C-06 answer whether the world consumes hold progress, define begin/complete/cancel and streaming/destruction/level-transition behavior, and state whether damage interrupts a hold; if this remains unresolved it will be escalated to TD/design. In C-07 enumerate runtime/authored/route/interactable IDs, tag namespaces, actual save/consumer references, retirement and non-reuse needs; do not assume a namespace or interactable persistence policy. Correct A2's inconsistent count of executable L0 tests versus four route-data tests; separately label the 9 independent `contract_data_checks.py` checks, 23 document tests and 42 proposed acceptance tests. Confirm 57/57 CH01 location capture/provenance and preserve withdrawal of unsupported prop/interactable counts. All test/build/runtime status must be reported exactly as evidenced; this reconciliation ran no tests. Keep all items `PROPOSED`/not frozen unless the exact same version is explicitly approved by both agents. Do not implement or freeze APIs.

## 7. Test and evidence matrix

This assignment performed source/document inspection only. It did not execute tests, builds, runtime checks, route parsing, or new evidence-generation commands. Agent 2's submitted evidence is reported as a **source claim**, not rerun or independently validated here.

| Evidence item | A2 submission claim / source detail | What it supports | What it does not support / V2 session result |
|---|---|---|---|
| `contract_data_checks.py` | **9 independent checks**, 9/9 passed in A2's attached W-M2.4 evidence; includes category multi-value, 57 rows and ID-scheme checks. | Register-derived L0 data claims at the source version. | Does not validate runtime, an agreed route schema, or new reconciliation. Not rerun here. |
| `Tools/world/tests/test_contract_submission.py` | A2 narrative reports **23 document tests** passing; tamper statement says 4 tests fail after removing `Traversal Area` from `SUB-009`, then 23/23 restored. | Assertions over proposal/captured data at A2's source commit. | Does not prove runtime or counterpart agreement. Not rerun here. |
| A2 §3.7 proposed route tests | A2 says **3 L0 tests executable today**, then says **four L0-data tests** can be run against route records that do not exist and must fail until authored. | Evidence of an internal claim inconsistency only. | No interpretation is selected: clarify exact executable test count and distinguish current data checks from not-yet-possible route-record tests. No route records created/tested here. |
| Proposed contract acceptance suite | **42 acceptance tests proposed** across contracts per A2 text. | Proposed future test inventory only. | Not equivalent to 9 data checks or 23 document tests; not run, not implemented, no runtime evidence. |
| Chapter 1 location capture | **57/57**, 0 duplicates; derived from `LOCATION_MASTER_REGISTER` v2.9, reported capture `Tools/canon/tests/fixtures/location_register_ch01_summary_v29.md`; source Drive document/version and capture provenance recorded in A2 response and W-M2.4 evidence. | Reported completeness/provenance of a register-derived Chapter 1 location capture, including eight traversal-category entries. | This reconciliation did not re-run or edit authoritative registers. It does not authorize new locations or ID families. |
| Withdrawn quantity claims | A2 withdraws unsupported interactable/prop totals, including prior unsupported 62 total and 8-prop claim; 13 is only a candidate-scene upper bound, not interactable count. | Preserves corrections and uncertainty from A2 submission. | No interactable/prop totals are inferred here. |
| Population caveat retained | A2 evidence identifies **29 exact / 5 bounded / 1 unbounded / 11 uncaptured** CH01 population classifications; `CH01-SCN-014` has no invented numeric bound. | Preserves prior C-08 reconciliation/provenance constraints. | No register modification or inferred bound. |
| This V2 report | Markdown content review, source comparison, link/reference and status consistency checks only. | Traceability and coordination. | No tests/build/runtime executed, no APIs implemented/frozen, no M0 claim. |

The attached Agent 2 W-M2.4 evidence additionally says it ran other Python/canon/world/L0 checks in that assignment. Those remain A2-reported results at its pinned source commit; they are not evidence that this V2 report or any cross-agent contract passed tests.

## 8. Per-agent response and agreement ledgers

Updated V2 ledgers record the exact source submission, counterpart review state, the one required status per contract, and copy-ready follow-up where appropriate:

- [`Agent 1 Contract Responses v2`](AGENT1_CONTRACT_RESPONSES_V2.md)
- [`Agent 2 Contract Responses v2`](AGENT2_CONTRACT_RESPONSES_V2.md)

No direct agent communication is available. The A1 v1.2 acknowledgment/rebase request and A2 exact A1-R1 review request are prepared, not sent.

## 9. Preserved scope and previous reconciliation constraints

- Preserve prior C-08 **29 exact / 5 bounded / 1 unbounded / 11 uncaptured** and C-09 `CH01-SCN-014` with no invented bound.
- Preserve A2's withdrawn unsupported interactable/prop totals and the reported 57/57 Chapter 1 location capture with provenance; do not alter authoritative registers or invent IDs/data.
- No code, Core types, API freeze, Unreal project, implementation, tests/build/runtime claims, branch merge, Agent 2 skeleton adoption, or M0 pass claim. No canon or creative decision changed.
- v1.0/v1.1 history and the earlier V1 report remain intact.

## 10. Change history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Prior awaiting-submission comparison; retained unchanged in its file. |
| 2.0 | 2026-11-16 | Reconciled exact A1-R1 and A2 submissions against published TD v1.2; corrected TD-01 visibility fact; recorded C-01…C-07, TD-01…TD-09, proposal-level divergences, evidence distinctions, and unsent copy-ready Agent 2 request. No contract agreement or freeze. |
