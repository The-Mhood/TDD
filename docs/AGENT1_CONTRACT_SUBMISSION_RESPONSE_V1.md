# Agent 1 Response — Player/Executable Side of the Shared Contracts C-01 … C-07

**Response ID:** `TDD-A1-CONTRACT-RESPONSE-001`
**Version:** 1.0 (`A1-R1`)
**Date:** 2026-11-16 UTC (submitted ahead of the requested deadline, 18 November 2026 17:00 UTC)
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Responds to:** [`TDD-A1-CONTRACT-PACKET-001` v1.0](AGENT1_CONTRACT_SUBMISSION_PACKET_V1.md), packet source commit `50b14318c8089dedcc688fb2c78ad3cb361c15f5`
**Governing addendum read:** `TDD-TD-INT-001` **v1.1** (`TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_1.md`) — see §0.2 for the v1.2 discrepancy
**Source basis:** Agent 1 M1 Movement Specification **v1.4** (`docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md`, commit `bb2685c605efd4958b1c67944721c77e1b393931`) and Technical Assessment v1.4; MEAD `TDD-MEAD-001` §3.5, §4.4, §4.5, §5.2–§5.5, §13.2
**Status:** `DESIGN_ONLY` — contract proposals only. **No Core type created, no code written, no test executed, no project created, no branch merged.**

> **Every interface or data shape in this document is `PROPOSED — NOT FROZEN`.**
> Every test name is `PROPOSED / NOT RUN`. Nothing here is evidence that a contract is agreed or a behaviour observed. Agent 3/TD publishes the Core surfaces; Agent 1 states requirements and offers shapes for review.

---

## 0. Reading notes, conventions and scope

### 0.1 What this document is, and what it is not

It is Agent 1's **producer-side and player-side requirement submission** for all seven shared contracts: what Agent 1 will execute, what it will publish, what it needs from Agent 2, and where it must not be touched. It is a negotiation input.

It is **not**: an agreed contract; an API freeze; an implementation plan authorised to start; a claim that any test exists or ran; a Core type definition (Agent 3 owns `TDDCore`); a merge or a project creation.

| Constraint from the request | Compliance |
|---|---|
| Do not implement the shared Core APIs | No code, no headers, no `.uproject`. Every shape is labelled `PROPOSED — NOT FROZEN` |
| Do not merge branches or create an Unreal project | Nothing merged; no project; `Source/` remains empty |
| Do not begin gameplay implementation | None begun |
| Preserve M1 v1.4 damage, AbortWindow, fallback, restoration, terminal-hold semantics | Preserved verbatim; C-01 §1.6 restates them as non-negotiable and does not redesign them |
| Keep locomotion / action-control / combat status separate | C-02 publishes three distinct snapshots, never a merged "player state" |
| Keep Dead (100) > Cinematic (90) > Stagger (80) | C-04 §4.4 preserves the exact ordering and single-winner rule |
| Health application independent of control resolution | C-03 §3.4 and C-04 §4.5 assert it as a testable invariant |
| Do not assume `bCausesStagger` is approved | C-04 §4.2 offers four storage alternatives; `bCausesStagger` is one candidate, explicitly provisional |
| TDD canonical; Agent 2 skeleton not adopted | Assumed throughout; nothing copied from `arena/5dde91a4-tdd` |
| Do not contradict TD decisions without naming the conflict | §8.1 names the one real tension found (MEAD §5.4 attacker-applies vs A1 damage authority) |

### 0.2 Version discrepancy that must be resolved before consolidation

The request names **`TDD-TD-INT-001` v1.2** as the governing integration document. **v1.2 is not present in the repository.**

| Check performed | Result |
|---|---|
| Packet commit `50b1431` tree | Contains `TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1.md` and `..._V1_1.md`. **No `V1_2` file** |
| `origin/main` (`5e3d1da`) | No integration addendum v1.2 |
| All remote branches visible from this session | No branch carries an integration addendum v1.2 (Agent 2 `ed36ad6`, Agent 3 `e121bbb`, Agent 1 `bb2685c`) |
| Packet header itself | Names **v1.1** as the related governing addendum |

**Therefore** this response is authored against **v1.1** plus the seven standing directives stated in the request text (ownership split, state separation, forced precedence, M1 v1.4 preservation, health independence, `bCausesStagger` provisional, TDD canonical). Those directives are consistent with v1.1 §2.2 and §5–§6 as read here, so no interpretation was invented. **If v1.2 differs materially in any of the seven contract scopes, this response must be re-based and the affected rows re-submitted.** This is raised as issue **TD-01** in §8.2.

### 0.3 Reference conventions

| Convention | Meaning in this document |
|---|---|
| `PROPOSED — NOT FROZEN` | A shape offered for review; Agent 1 will adapt to whatever Core shape Agent 3 publishes |
| `SUBMITTED` | Agent 1's position is stated here and is stable unless the TD or Agent 2 raises a conflict |
| `NOT RECEIVED` | Agent 2 has not reviewed this exact version |
| `PENDING` | Reserved for Agent 3/TD; Agent 1 does not fill these cells |
| Units | Unreal conventions: **centimetres**, **cm/s**, **degrees**, world space, left-handed, Z-up. Time in **seconds** unless marked `ms` |
| Client-side scope | Player-side surfaces are single-player, single local player. No replication requirement in the vertical slice (stated explicitly in C-07) |

### 0.4 Ownership summary assumed by every contract

| Domain | Owner | What the other side may do |
|---|---|---|
| Player state mutation (control state, movement mode, input, capsule, camera, combat status) | **Agent 1** | Read through C-02 snapshots only; never write |
| Traversal execution and fallback/hold resolution | **Agent 1** | Agent 2 authors markers/routes and consumes query results for authoring/debug |
| Hit arbitration and damage application | **Agent 1** | Agent 2 submits damage **requests** and consumes applied events; never writes health |
| Player-side interaction routing (focus, input, hold progress, cancel) | **Agent 1** | Agent 2 implements interactable behaviour; never starts or completes on its own |
| Telegraph production | **Agent 2** | Agent 1 consumes; Agent 1 also produces player attack telegraphs for Agent 2 AI |
| World marker/route authoring, encounter state, chapter flow, memory persistence | **Agent 2** | Agent 1 consumes completion signals; never grants progress |
| `TDDCore` publication: event structs, `UTDDEventBus`, `ITDDDamageable`, `ITDDInteractable`, registry/governance | **Agent 3/TD** | Agent 1 requests; never creates a competing type or registry |

### 0.5 Five cross-contract principles Agent 1 asks to be honoured

1. **Identity is separable three ways** — runtime `FGuid EntityId`, authored `FName` content id, and `FGameplayTag` classification. A contract that conflates them cannot survive actor destruction, saves, or content renaming. Detail in C-07.
2. **Cross-module payloads never carry actor pointers.** Events carry `FGuid` + values (MEAD §3.5). Local synchronous APIs may take `TWeakObjectPtr` with an explicit validity rule.
3. **Exactly-once is a contract property, not a hope.** Damage application, interaction completion, telegraph closure and forced-state change each have one authoritative commit point with a dedupe/terminal rule (§C-03.4, §C-06.5, §C-05.4, §C-04.4).
4. **No consumer may be able to write player state.** Every read surface is a value snapshot; no setters, no Blueprint-callable mutators, no friend access.
5. **A contract that can silently do nothing is a defect.** Every rejection path returns a distinguishable outcome and logs once — no silent no-ops (C-01 §1.6 table, C-03 §3.6, C-06 §6.6).

### 0.6 Submission summary

| Contract | Scope | A1 proposal version | Proposal status | A2 sign-off | Blocking issues |
|---|---|---|---|---|---|
| **C-01** | Traversal vocabulary, route IDs, markers, query, failure semantics | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-04 (route-id stability/format), A2 marker schema |
| **C-02** | Read-only player context and state snapshots | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-05 (stealth/noise exclusion) |
| **C-03** | Damage request, resolution, application, applied event | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-03 (non-health event semantics), §8.1 (MEAD §5.4 tension) |
| **C-04** | Stagger classification and forced-state outcome | `A1-R1` | `REQUEST_TD_DECISION` | `NOT RECEIVED` | TD-02 (classification storage) |
| **C-05** | Telegraph timing and lifecycle | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-06 (canonical gameplay clock) |
| **C-06** | Interaction lifecycle (player side) | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-07 (hold-progress authority) |
| **C-07** | Shared IDs and Gameplay Tags | `A1-R1` | `UNDER_REVIEW` | `NOT RECEIVED` | TD-08 (tag approval + registry policy) |

Nine items require Technical Director resolution or Agent 3 arbitration: **TD-01 … TD-09**, §8.2.

---

## 1. C-01 — Traversal vocabulary, route IDs, markers, query and failure semantics

**Contract ID / proposal version:** `C-01` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 1.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-01` / `A1-R1` (v1.0). Supersedes no prior contract; M1 v1.4 §3.2.2–§3.2.3 and §3.7 supply the executable semantics |
| **Publisher (Core contract authority)** | `Agent 3/TD` for any Core-owned type. Agent 1 requests **no exception**: the traversal query result and marker spec may live in `TDDGameplay` if Core prefers, because only Agent 1 and Agent 2 authoring touch them — see §1.9 item 1 |
| **Implementation owner(s)** | `UTDDTraversalComponent` (A1, execution + query), `UTDDTraversalRegistry` (A1, world-subsystem registration of markers), marker/interactable authoring (A2) |
| **Producers** | (A1) `UTDDTraversalComponent::QueryCandidates` produces `FTDDTraversalQueryResult`; `ResolveAbortFallback` produces `ETDDFallbackResult` outcomes. (A2) authored marker actors/data register `FTDDTraversalMarkerSpec` with the registry |
| **Consumers (named)** | A1 consumes A2's marker specs. A2 consumers: the **authoring validator** (editor-time: reachability, missing exit, duplicate `RouteId`), **streaming/level systems** (marker register/unregister), and **narrative gating** where a route is conditionally enabled. Agent 1 produces for Agent 2's debug visualisation only — no A2 runtime decision may depend on A1 query results |
| **Executable/player-side requirements** | Detect candidates from capsule + movement mode + capabilities; select deterministically; validate entry and exit against current collision; execute the montage with motion warping; on interruption run the M1 v1.4 two-phase fallback and restoration. Consumers must not mutate the capsule, the montage, the state machine or the route registry |
| **Lifetime and validity** | Registry entries live for the streamed-in lifetime of the marker actor; entry validity = `TWeakObjectPtr` resolves **and** not pending kill **and** same world. Route *identity* (`RouteId`) outlives the actor (it is authored content). Query results are valid for the frame they are produced in and are **revalidated at execution**. A route whose marker streamed out mid-execution does **not** abort the traversal: the exit transform already recorded is authoritative and is revalidated by physics (M1 §3.2.2a) |
| **Mutation authority** | Agent 1 alone writes: capsule transform during traversal (single write path `ApplyCandidateNow()`), control state, movement mode, montage playback. Agent 2 alone writes: marker/route authored data. Agent 1 reads marker data; it never writes it. Agent 2 never writes player state |
| **Proposal status** | `UNDER_REVIEW`. Unresolved alternatives: (a) whether marker data is an actor, a data asset or a data-table row — Agent 2's call; (b) whether the query result type is Core or `TDDGameplay`; (c) `RouteId` format and stability guarantees (TD-04) |
| **Acceptance tests** | `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics` (unit) and `TDD-Functional.Traversal.MarkerStreamingLifetime` (functional). Assertions in §1.7. All `PROPOSED / NOT RUN`. M1 v1.4 `TraversalAbortPaths` and `TraversalExitRevalidation` are **retained unchanged and not replaced** |
| **Agent 2 consumer agreement** | `NOT RECEIVED` — Agent 2 must review this exact version (`A1-R1`) |
| **Agent 3/TD decision** | `PENDING` |

### 1.2 Capability vocabulary and behaviour definitions

Grounded traversal only, matching MEAD §4.4's vertical-slice list. Each capability is a stable `FName`/tag pair; the tag is the authored requirement, the enum is the executable branch. **No capability is added without an ADR**, because each implies animation content (C-1…C-5 blockers).

| Capability | Tag (requested) | Behaviour definition | Entry condition | Exit requirement |
|---|---|---|---|---|
| `Vault` | `Traversal.Capability.Vault` | Cross an obstacle of height **≤ 100 cm** with clear landing space beyond; ends standing | Obstacle top within capsule-forward trace, exit floor within ±25 cm of entry floor height | Walkable floor beyond, clearance ≥ capsule |
| `Mantle` | `Traversal.Capability.Mantle` | Climb onto a ledge of height **100–200 cm**; ends standing on top | Ledge top trace hit, headroom ≥ capsule height above it | Walkable top surface, clearance ≥ capsule |
| `LedgeShimmy` | `Traversal.Capability.LedgeShimmy` | Lateral displacement while hanging from a ledge edge | Hang state active, lateral clearance along the ledge | Ledge continuity for the full lateral distance, or a valid detach point |
| `Drop` | `Traversal.Capability.Drop` | Controlled descent from an edge to a floor **≤ 300 cm** below, with authored landing | Edge detected, floor below within the drop limit | Walkable floor below; otherwise ordinary fall (`Airborne`), not a traversal |
| `ClimbLadder` | `Traversal.Capability.ClimbLadder` | Vertical ladder transition between bottom and top anchors | Ladder volume overlap and facing tolerance | Top/bottom exit anchor validated |

**Not in scope for the slice** (declared, so nobody assumes them): wall-run, slide, swing, zip-line, ledge-to-ledge leap, combat-on-ledge. Each would need its own capability tag, montage set and exit-validation rule.

### 1.3 Query inputs, selection policy and outputs

Player-side query is **Agent 1's** (`UTDDTraversalComponent`), not Agent 2's:

```cpp
// PROPOSED — NOT FROZEN. Agent 3 decides TDDCore vs TDDGameplay placement.
struct FTDDTraversalQueryRequest
{
    FGuid      EntityId;                 // requester (player); invalid guid is rejected
    FVector    FeetLocation;             // world, capsule base
    FVector    ForwardVector;            // world, normalised
    float      Speed2D;                  // cm/s
    ETDDMovementMode MovementMode;       // proposed Core enum, or CMC EMovementMode
    FGameplayTagContainer CapabilityTags;// player's granted capabilities
    ETDDStance Stance;                   // Exploration only in the slice
    FGameplayTagContainer BlockingTags;  // Status.Cinematic, Status.Staggered, Status.Dead suppress query
    double     QueryGameplayTime;        // combat gameplay clock (see C-05 §5.3)
};

struct FTDDTraversalQueryResult
{
    ETDDTraversalQueryOutcome Outcome;   // table below
    FName        RouteId;                // empty unless CandidateFound
    FGameplayTag CapabilityTag;          // which branch the candidate took
    FTransform   EntryTransform;         // world, validated at query time
    FTransform   ExitTransform;          // world, validated at query time — revalidated at execution
    float        Score;                  // selection score, for debug only
    int32        CandidateCount;         // how many passed validation, for debug
};
```

**Deterministic selection policy (ordered, total, no randomness, no frame dependence):**

1. Filter: candidate must be inside the detection volume, `CanInteract`-equivalent eligibility true, capability granted, not blocked by a tag, `RouteId` non-empty.
2. Score = authored `Priority` (**int32**, higher wins) → then `dot(ForwardVector, RouteForward)` (higher wins) → then distance to entry anchor (lower wins) → then `RouteId` **lexicographic ascending** as the final deterministic tiebreak.
3. Validation before returning: capsule sweep at entry and exit, walkable-slope check at exit, clearance check at exit, same-traversal-chain check.
4. Exactly one `CandidateFound` is returned; the runner-up list is *not* part of the contract (an executor that re-selects mid-execution is a defect — see §1.6).

**Validity and expiry:** a query result is valid only for the tick that produced it. At execution start Agent 1 re-queries; if the same `RouteId` no longer wins, execution does not begin (log `Traversal.QueryExpired`). Once the montage begins, the recorded entry/exit transforms are authoritative for fallback (M1 v1.4 §3.2.2), and physics revalidates at the instant of every write.

### 1.4 Distinct outcomes — and which ones show a prompt

| `ETDDTraversalQueryOutcome` | Meaning | Prompt? | Diagnostic | Log category | Player-facing result |
|---|---|---|---|---|---|
| `None` | Nothing in range | **No** | No | `LogTDDTraversal` Verbose | Nothing |
| `CandidateFound` | Validated candidate | Yes (if prompts enabled in the slice — currently a debug widget only) | No | Verbose | Executable |
| `UnsupportedByPlayer` | Route requires a capability the player lacks | **No** | Editor-time warning only; runtime Verbose | Warning (editor validator), Verbose (runtime) | Nothing — deliberately no "locked" affordance |
| `InvalidAuthoredData` | Missing exit anchor, zero-length route, duplicate `RouteId`, entry inside geometry | **No** | **Yes** — error with `RouteId`, reason, actor path | Error | Nothing; route is skipped, never executed |
| `BlockedPath` | Exit or entry occupied at query time, or path obstructed | **No** | Verbose | Verbose | Nothing (retry next frame) |
| `WorldUnavailable` | Marker streamed out / level transition pending / registry not ready | **No** | Verbose | Verbose | Nothing; explicitly retryable, no state change |
| `Cooldown` | Same route re-query inside its re-entry guard | **No** | Verbose | Verbose | Nothing |

**Execution failure is a different axis** and is not a query outcome: once the montage runs, failure is handled by the M1 v1.4 fallback (`ETDDFallbackResult`), never by returning to the query layer. This separation is deliberate: a query outcome can suppress a prompt silently, but once the capsule is moving, silence is forbidden.

### 1.5 Route identity and requested marker fields

**Identity requirement:** routes need a stable authored id that survives re-cooking, level edits, streaming and saves, and that is **not** derived from a transform. Proposed format, `PROPOSED — NOT FROZEN`:

```
TRV.<ChapterId>.<SceneId>.<NNN>      e.g.  TRV.CH01.SCN-014.001
```

- `RouteId` is `FName`, **opaque to code**: Agent 1 must never parse it. A validator enforces the format; runtime treats it as an identity token.
- Distinguishable from `EntityId` (`FGuid`, runtime instance) and from `SceneId` (canon register, Agent 2/3 owned). A route is *content*, not an entity.
- Stable across saves only if narrative or memory content references it — flagged for TD-04, since that determines how strict retirement policy must be.

**Marker fields Agent 1 requests** (representation is **Agent 2's choice** — actor, data asset or data-table row — Agent 1 asks only for the fields):

| Field | Type | Required | Why Agent 1 needs it |
|---|---|---|---|
| `RouteId` | `FName` | Yes | Stable identity, dedupe, log correlation |
| `CapabilityTag` | `FGameplayTag` | Yes | Which executable branch; eligibility filter |
| `EntryAnchor` | `FTransform` or child component | Yes | Montage start alignment and reverse-to-entry fallback |
| `ExitAnchor` | `FTransform` or child component | Yes | Completion target and revalidation reference |
| `RequiredCapabilityTags` | `FGameplayTagContainer` | No (default: `CapabilityTag`) | Support gated routes |
| `Priority` | `int32` | Yes | First selection key; deterministic ordering |
| `bOneWay` | `bool` | No (default false) | Suppresses reverse traversal from the far side |
| `EnabledCondition` | project condition type (Agent 3 owned) | No | Narrative-gated routes must be evaluable without A1 knowing narrative rules |
| `ChapterId` / `SceneId` | `FName` | No | Diagnostics, authoring validation, canon traceability |
| `EntryToleranceCm` / `ExitToleranceCm` | `float` | No (defaults 15 / 25) | Authored alignment slack; does **not** relax physics validation |

**What Agent 1 explicitly does not want:** authored `bCanExecute`, authored result enum, authored fallback choice, or any marker field that would let content bypass exit revalidation. Physics remains the authority; the marker is a hint. This is the C-01 restatement of "no teleport, no stale transform".

### 1.6 Interruption, abort, failure — and the M1 v1.4 boundary

**Non-negotiable preservation (not redesigned by C-01):**

| M1 v1.4 element | Preserved statement |
|---|---|
| Bounded relocation loop | Candidates 1 complete, 2 reverse, 3 drop-to-floor; `MaxRelocationAttempts` total per call, clamp `[0,3]`, default 3 |
| Always-run terminal hold | `ResolveHold()`: H0 out-of-world → H1 Hold-Grounded (5 cm) → H2 Hold-Unsupported; never budgeted |
| Validation at write | `ApplyCandidateNow()` is the only transform writer; a stale transform is never applied; failure falls through to the next candidate |
| Restoration ordering | fallback → restoration checklist → target-state entry, exactly once |
| Out-of-world handoff | `FellOutOfWorld` is a flow-system outcome, not a placement |

C-01 adds no new placement behaviour. It defines only **what triggers** an abort and **what the player sees** when the query, rather than the execution, fails.

| Event during traversal | Class | Executable response |
|---|---|---|
| Lethal damage | Forced | M1 v1.4 E5: fallback → restoration → `Dead`. Outranks everything |
| Cinematic takeover | Forced, no fallback | M1 v1.4 E6: capsule frozen, freeze-mode restoration, `Cinematic` |
| Staggering damage / posture break / successful parry | Forced | M1 v1.4 E4: fallback → restoration → `Stagger` |
| Non-staggering damage inside `AbortWindow` | **Request** | E3: fallback → restoration → `Locomotion`/`Land`; refused if `HoldUnsupported` |
| Non-staggering damage outside `AbortWindow` | Request, denied | Traversal continues; health already applied |
| Route streamed out mid-execution | Not an abort | Contract continues (recorded exit is authoritative, revalidated at write) |
| Self-cancel / input | Never | There is no self-cancel path; the seven exit paths are exhaustive |
| EndPlay / unpossess | Forced | E7: full checklist, default mode |

**Ordering guarantee Agent 2 may rely on:** the traversal component never yields between the abort decision, fallback resolution and restoration. There is no frame in which the capsule is between two placements.

### 1.7 Acceptance tests — `PROPOSED / NOT RUN`

#### `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics` — unit layer, no world (mock traces)

| # | Setup | Assertion |
|---|---|---|
| 1 | Three markers in range, equal priority/facing, distances differing | Selected `RouteId` is the nearest; **1000 repeated queries return the identical `RouteId`** |
| 2 | Two markers with identical priority, facing and distance | Tiebreak resolves to the lexicographically lower `RouteId`, every call |
| 3 | Marker requires a capability the player lacks | `Outcome == UnsupportedByPlayer`; **prompt count 0**; player state unchanged (state id, mode, transform byte-equal) |
| 4 | Marker with null exit anchor | `Outcome == InvalidAuthoredData`; one `Error` log naming `RouteId`; no montage, no transform write; engine does not assert |
| 5 | Exit volume blocked by a dynamic actor introduced after query | `BlockedPath` at query; if introduced **after selection**, placement validation fails and M1 fallback runs (asserted via the retained v1.4 test, not replaced) |
| 6 | Registry empty / marker unregistered mid-frame | `WorldUnavailable`; explicitly retryable; subsequent frame with the marker restored returns `CandidateFound` |
| 7 | Registered marker actor destroyed without unregistering | Registry purges the entry within **1 frame**; query never dereferences a stale pointer (`WorldUnavailable`) |
| 8 | `RouteId` collides between two actors | Second registration refused with `Error`; first remains authoritative; query returns the first |

#### `TDD-Functional.Traversal.MarkerStreamingLifetime` — functional layer, `L_TDD_Test_Movement`

| # | Assertion |
|---|---|
| 1 | Streaming the marker in enables the route within 1 frame; streaming out disables it with no state change and no crash |
| 2 | Streaming out **during** the montage does not abort: the traversal completes and ends grounded on a validated surface |
| 3 | Level transition during execution runs E7 restoration exactly once (no double-restore log) |

**Retained, not replaced:** `TDD-Functional.Movement.TraversalAbortPaths` and `TDD-Functional.Movement.TraversalExitRevalidation` (M1 v1.4). The packet requires that a generic contract test must not stand in for them; agreed.

### 1.8 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Marker representation decision (actor / data asset / data-table row) and registration timing | `NOT RECEIVED` |
| 2 | Confirmation of the authored field set in §1.5, or a reduced set with justification | `NOT RECEIVED` |
| 3 | `RouteId` format agreement, and whether narrative/save content will reference `RouteId` (drives retirement policy) | `NOT RECEIVED` |
| 4 | Whether any route is one-way, gated, or requires capabilities beyond the player's default set | `NOT RECEIVED` |
| 5 | Authoring validator behaviour for invalid markers (block save? warn only?) — an Agent 2/Agent 3 decision | `NOT RECEIVED` |

### 1.9 Unresolved alternatives (C-01)

1. **Placement of `FTDDTraversalQueryRequest`/`Result`.** Either Core (Agent 3 publishes) or `TDDGameplay` (Agent 1 owns, Agent 2's editor validator includes the header). Agent 1 has a mild preference for `TDDGameplay`: only these two modules need it, and it keeps `TDDCore` smaller. **Not a decision Agent 1 may take** — Agent 3 chooses.
2. **Marker as actor vs pure data.** An actor is authorable in-level and streams naturally; a data-table row is easier to validate in bulk but needs a transform source. Agent 2's call; Agent 1 is indifferent provided identity and anchors exist.
3. **Prompt visibility in the slice.** Currently a debug widget only (no approved UI). If the slice needs a real prompt, that is a UI/A2 deliverable and a new contract row, not an A1 change.
4. **Reverse traversal from the far side.** `bOneWay` covers the authored case; whether the executor should *discover* a reverse route from the exit anchor is left out of `A1-R1` (it would double the query surface for no slice benefit).

---

## 2. C-02 — Read-only player context and state snapshots

**Contract ID / proposal version:** `C-02` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 2.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-02` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` for the event structs if they are published on `UTDDEventBus`. The **snapshot structs themselves** are Agent 1's (`TDDGameplay/Public/Player/TDDPlayerContext.h`) because only Agent 1 writes them; requested as a documented exception to "Core publishes everything", justified in §2.9 item 1 |
| **Implementation owner(s)** | Agent 1: `UTDDPlayerContextComponent` (assembler + publisher), `UTDDCharacterStateMachine` (control state), `UTDDLocomotionComponent` (locomotion), `UTDDCombatComponent` (combat status) |
| **Producers** | `UTDDPlayerContextComponent::PublishFrame` once per tick after movement; `OnControlStateChanged` / `OnCombatStatusChanged` / `OnLocomotionModeChanged` delegates |
| **Consumers (named)** | Agent 2: enemy AI perception and engagement decisions, boss phase logic, encounter manager (player-in-encounter checks), narrative trigger volumes needing player position, scripted-camera/cinematic director needing facing and state. Agent 1 internal: camera, input routing, UI debug |
| **Executable/player-side requirements** | Publish three **separate** value snapshots plus a frame envelope; never expose a merged state; support one query call per consumer per frame at no allocation; publish discrete-change events on the bus |
| **Lifetime and validity** | A snapshot is valid until the next published frame. `GetPlayerContext` returns `false` when there is no possessed player, when the pawn is being destroyed, or during a level transition. A2-held copies become stale: the contract requires A2 to re-query rather than cache beyond one frame |
| **Mutation authority** | Agent 1 only. No setter, no Blueprint-callable mutator, no public non-const member. `const` accessors return by value |
| **Proposal status** | `UNDER_REVIEW`. Unresolved: (a) whether stealth/noise is included at all (TD-05); (b) whether A2 prefers polling only, events only, or both (A1 supplies both); (c) whether the frame envelope is Core or gameplay-owned |
| **Acceptance tests** | `TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation` (unit + functional). Assertions §2.7. All `PROPOSED / NOT RUN` |
| **Agent 2 consumer agreement** | `NOT RECEIVED` |
| **Agent 3/TD decision** | `PENDING` |

### 2.2 Three snapshots, not one

The packet requires locomotion, action/control and combat status to stay distinct, and the v1.4 control-state vs movement-mode matrix already depends on that separation. One merged "player state" struct would recreate the class of bug v1.3 fixed.

```cpp
// PROPOSED — NOT FROZEN
struct FTDDLocomotionSnapshot        // authoritative source: UTDDLocomotionComponent + CMC
{
    FVector Velocity;                // cm/s, world space
    float   Speed2D;                 // cm/s, horizontal magnitude
    bool    bGrounded;
    float   HeightAboveGround;       // cm, capsule base to floor; 0 when grounded
    EMovementMode MovementMode;      // CMC mode: Walking / Falling / Flying / None
    float   GroundSlopeDegrees;      // 0 when airborne
    bool    bOnWalkableFloor;
};

struct FTDDActionControlSnapshot     // authoritative source: UTDDCharacterStateMachine
{
    ETDDControlState ControlState;   // Idle, Locomotion, Sprint, Airborne, Land, Dodge,
                                     // Attack, Block, Parry, Stagger, Traversal,
                                     // Interaction, Cinematic, Dead
    FGameplayTag     ControlStateTag;// Status.* mirror, for tag-driven consumers
    float            StateElapsedSeconds;
    bool             bAllowsInput;
    bool             bLocked;        // action lock (montage owns the character)
    FName            ActiveActionId; // authored id of the active montage action, empty if none
};

struct FTDDCombatStatusSnapshot      // authoritative source: UTDDCombatComponent
{
    ETDDCombatState CombatState;     // MEAD §5.1 / M1 Appendix A enum
    bool            bAlive;
    float           HealthFraction;  // 0..1, read-only projection of the attribute set
    float           PostureFraction; // 0..1, read-only projection
    bool            bIsStaggered;
    float           StaggerRemainingSeconds;
    bool            bIsTelegraphing; // player's own attack telegraph, consumed by A2 AI
    float           TelegraphRemainingSeconds;
};

struct FTDDPlayerContextFrame        // envelope: one consistent frame, one tick
{
    FGuid                       EntityId;          // stable runtime identity (C-07)
    uint64                      FrameCounter;      // monotonic, +1 per published frame
    double                      WorldTimeSeconds;  // capture time
    double                      GameplayTimeSeconds;
    FVector                     ActorLocation;     // cm, world, capsule centre
    FRotator                    ActorRotation;     // degrees, world (yaw/pitch/roll)
    FVector                     AimDirection;      // normalised, camera-relative input aim
    TWeakObjectPtr<AActor>      CurrentTarget;     // transient; validity rule below
    FGuid                       CurrentTargetEntityId;

    FTDDLocomotionSnapshot      Locomotion;
    FTDDActionControlSnapshot   Action;
    FTDDCombatStatusSnapshot    Combat;
};
```

### 2.3 Field-by-field justification (the packet requires that no field be speculative)

| Field group | Named Agent 2 consumer | Decision it enables | Verdict |
|---|---|---|---|
| `ActorLocation`, `ActorRotation` | Enemy AI perception, encounter volumes, narrative triggers | Can I see/reach the player; is the player in my volume | **Required** |
| `Velocity`, `Speed2D` | Enemy AI pursuit/interception, boss chase phases | Intercept point, "is the player fleeing" | **Required** |
| `bGrounded`, `HeightAboveGround` | Enemy AI ledge awareness; boss "player is airborne" branch | Whether to commit to a ground attack | **Required** |
| `MovementMode` | AI reaction to air-dodge/fall | Whether the player can be hit by a ground-only sweep | **Required** |
| `ControlState`, `ControlStateTag` | Boss phase logic ("player is staggering — punish window"), scripted camera | React to readable player commitment | **Required** |
| `bAllowsInput`, `bLocked` | AI difficulty pacing (avoid attacking a locked player), tutorial triggers | Do not punish an unresponsive player | **Required** |
| `ActiveActionId` | Boss fairness tuning, telemetry attribution | Which player action is locked in | **Required (diagnostics)** |
| `CombatState`, `bAlive` | Boss victory/death flow, encounter manager | Did the player die; is combat live | **Required** |
| `HealthFraction` | Boss phase thresholds ONLY (if A2 phases need HP bands) | Phase transitions without reading the ASC | **Conditional** — if A2 confirms it does not need HP bands, this field is **removed** (A2 must not read the attribute set directly; that would bypass C-03) |
| `PostureFraction` | Enemy AI aggression (press the advantage when posture is low) | Aggression tuning | **Conditional**, same rule |
| `bIsStaggered`, `StaggerRemainingSeconds` | Enemy AI punish timing | Timing the punish window | **Required** |
| `bIsTelegraphing`, `TelegraphRemainingSeconds` | Enemy AI defensive response to a player attack | Block/dodge decision | **Required** (mirrors `ITDDCombatant`, C-05) |
| `CurrentTarget`, `CurrentTargetEntityId` | Encounter aggro, threat logic | Which enemy the player is engaged with | **Required** (entity id durable, weak ptr transient) |
| `AimDirection` | AI facing prediction | Where the player is looking | **Required** |
| **Stealth / noise radius** | — | — | **NOT PROVIDED.** No approved stealth design exists in the canon set, and no A2 consumer has named a decision it enables. Adding it now would be speculation. Raised as TD-05 |

### 2.4 Cadence, consistency and ordering

| Property | Rule |
|---|---|
| Frame assembly point | End of the player character's tick, **after** CMC movement and state-machine evaluation, so a frame never mixes pre-move position with post-move state |
| Cadence | Exactly one published frame per player tick — asserted, not assumed |
| Consistency | All three snapshots in one envelope share `FrameCounter` and capture times. A consumer that needs coherent data must read one envelope, not three accessors |
| Event ordering within a frame | snapshot published → `FTDDControlStateChangedEvent` (if changed) → `FTDDCombatStatusChangedEvent` → `FTDDLocomotionModeChangedEvent`. A listener may therefore always re-query and see the state the event describes |
| No-change policy | Discrete events fire **only** on change. Continuous values (velocity, height) produce no events. A consumer polling every tick sees values; a consumer listening sees transitions. Neither is flooded |
| Pause | A paused world does not publish frames (no tick). `GetPlayerContext` returns the last frame with its original timestamps — consumers must compare timestamps rather than assume freshness |
| Level transition | `FTDDPlayerContextInvalidatedEvent { EntityId, Reason }` with `Reason ∈ {Unpossessed, Despawned, LevelTransition, Paused}`; `GetPlayerContext` returns false from the moment the pawn begins tearing down |
| Respawn | Same `EntityId` (identity is the player, not the pawn instance). `FrameCounter` continues monotonically; a fresh `FTDDPlayerContextInvalidatedEvent` is **not** emitted for death→respawn, only `bAlive` false→true and a state change |

### 2.5 Read-only enforcement mechanism

Three layers, because a comment is not an enforcement:

1. **Type-level:** snapshots are plain `USTRUCT`s of values with no setters; accessors are `const` and return by value.
2. **API-level:** `UTDDPlayerContextComponent` exposes only `bool GetPlayerContext(FTDDPlayerContextFrame& Out) const` and the event delegates. No `Set*`, no `BlueprintCallable` mutator, no protected friend.
3. **Test-level:** a unit test mutates the returned copy and asserts the component's stored frame is unchanged; a second test asserts no `UFunction` on the component has a non-const `Out`/`In` parameter that writes player state (introspection over the generated class).

Consumers may hold `CurrentTarget` only as `TWeakObjectPtr` and must call `IsValid()`; the durable reference is `CurrentTargetEntityId`.

### 2.6 Failure and invalidation behaviour

| Situation | Behaviour |
|---|---|
| No possessed player (menu, cinematic with detached view) | `GetPlayerContext` → `false`; no events |
| Pawn destroyed while A2 holds a copy | Copy's `TWeakObjectPtr` invalidates; `EntityId` remains usable for log correlation; A2 must not act on a stale frame older than one tick |
| Player unpossessed/repossessed | `InvalidatedEvent` then a fresh frame with the same `EntityId`, `FrameCounter` +1 |
| Multiple local players | Not supported in the vertical slice; the component is a player-character component, so a second player produces a second context and the contract makes no cross-player guarantee |
| Consumer reads mid-tick | It reads the previous complete frame — by design. There is no partially assembled frame exposed |

### 2.7 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation`**

| # | Layer | Setup | Assertion |
|---|---|---|---|
| 1 | Unit | Move player at a fixed 600 cm/s for 10 frames | `Speed2D` == 600 ± 1 cm/s; `Velocity.Size2D()` matches; units are cm/s, not m/s |
| 2 | Unit | 60 ticks | Exactly 60 published frames; `FrameCounter` strictly increasing by 1 |
| 3 | Unit | Mutate every field of a returned frame copy | Re-queried frame is unchanged (byte-compare of the value fields; weak ptr compared separately) |
| 4 | Unit | Enter `Stagger` via forced path | `Action.ControlState` changes; `Locomotion` snapshot is unchanged except `MovementMode` where v1.4 requires `MOVE_Falling`; `Combat.bIsStaggered` true. **Assert the three are changed independently** |
| 5 | Unit | Take non-staggering damage | `Combat.HealthFraction` decreases; `Action.ControlState` unchanged if outside `AbortWindow` (health/state independence) |
| 6 | Unit | No state change for 30 frames | Zero discrete events emitted |
| 7 | Unit | Change state, then re-query in the same frame's event | Re-queried `ControlState` equals the state named in the event (ordering rule) |
| 8 | Functional | Destroy the pawn while a listener holds a frame | Listener receives `InvalidatedEvent` within 1 frame; `GetPlayerContext` false; no crash; `TWeakObjectPtr` invalid |
| 9 | Functional | Pause during combat | No new frames; stored timestamps unchanged; on resume, `FrameCounter` continues from where it stopped (no gap) |
| 10 | Unit (introspection) | Enumerate the component's `UFunction`s | No public function writes player state; only the const query and event registration exist |

### 2.8 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Confirmation of which fields are actually consumed, with the decision each enables — and explicit removal of the rest | `NOT RECEIVED` |
| 2 | Whether HP/posture fractions are needed (phase bands) or must be removed | `NOT RECEIVED` |
| 3 | Preferred freshness: polling every tick, events only, or both | `NOT RECEIVED` |
| 4 | Whether any A2 system needs player context during a cinematic or a paused state | `NOT RECEIVED` |
| 5 | Stealth/noise: does any approved design need it? (TD-05) | `NOT RECEIVED` |

### 2.9 Unresolved alternatives (C-02)

1. **Where the snapshot structs live.** Agent 1 requests they stay in `TDDGameplay` (only Agent 1 writes them; A2 includes the header read-only). If Agent 3/TD requires Core ownership for the event structs, that is fine — the snapshots themselves can remain gameplay-owned and be referenced by the events. Splitting the envelope from the events is also acceptable.
2. **Health/posture exposure.** Excluded by default in `A1-R1` unless A2 names a phase-band decision; the alternative (A2 reads the ASC) is explicitly rejected in this proposal because it bypasses C-03's authority.
3. **Event granularity.** Per-transition events (proposed) vs a per-frame "context updated" event. Per-frame events are rejected as needless traffic; polling covers continuous data.
4. **`ActiveActionId` type.** `FName` (authored id) vs `FGameplayTag`. Agent 1 proposes `FName` to match `UTDDAttackDefinition::AttackId`; if C-07 settles on tags for action identity, this field follows C-07.

---

## 3. C-03 — Damage request, local resolution, application and applied event

**Contract ID / proposal version:** `C-03` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 3.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-03` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` for `FTDDDamageRequest`, `FTDDDamageAppliedEvent`, `ITDDDamageable` (all already exist as Core contracts in MEAD §5.4 / §3.5). Agent 1 requests **one field addition and one event-field addition**, both labelled proposals |
| **Implementation owner(s)** | Agent 1: `UTDDCombatComponent` (attacker side, hit windows, arbitration), `UTDDPlayerDamageAuthority` (victim-side validation and application for the player), `UTDDHitStopSubsystem` interaction. Agent 2: `ITDDDamageable` implementation on enemy actors (its own health), and request emission from its attack windows |
| **Producers** | (A1) `FTDDDamageRequest` from player attack hit windows; resolution results; `FTDDDamageAppliedEvent` for every applied hit; `FTDDPostureBrokenEvent`. (A2) `FTDDDamageRequest` from enemy attack windows — **requests only** |
| **Consumers (named)** | Agent 2: enemy combo/poise/aggro logic, boss phase transitions, encounter manager (enemy defeat), audio/VFX hooks driven by A2. Agent 1: its own AI-agnostic reaction, camera shake, hitstop, narrative kill counters via A2/A3 subscriptions to `FTDDEntityKilledEvent` |
| **Executable/player-side requirements** | One resolution path; one application per hit; exactly one applied event per applied hit; dedupe per hit instance; no consumer may write health or posture; request validation rejects out-of-window, duplicate, stale-target and invalid-source requests with distinguishable outcomes |
| **Lifetime and validity** | Requests are synchronous and value-only: `FGuid` ids, no actor pointers. Actor resolution happens at application time. An applied event remains meaningful after the actor is destroyed (ids only). A request whose window has closed is rejected, not queued |
| **Mutation authority** | Agent 1 alone commits health/posture **for the player** and arbitrates all hits against the player. Agent 2 owns and writes its own actors' health through its `ITDDDamageable` implementation, but only **after** an A1-authorised resolution — it may not self-resolve enemy-vs-player hits. No system other than the resolving authority calls `ApplyDamage` for a player-vs-enemy hit |
| **Proposal status** | `UNDER_REVIEW`. Unresolved: (a) `HitInstanceId` field on `FTDDDamageRequest` (TD-03); (b) whether blocked/immune/posture-only hits publish an applied event and with what payload (TD-03); (c) the §8.1 MEAD §5.4 tension |
| **Acceptance tests** | `TDD-Contract.Combat.SingleDamageApplicationAndEvent` (§3.7). All `PROPOSED / NOT RUN`. Retains `TDD-Unit.Combat.HitDedup` from MEAD §5.3 |
| **Agent 2 consumer agreement** | `NOT RECEIVED` |
| **Agent 3/TD decision** | `PENDING` |

### 3.2 The four stages, explicitly separated

The packet asks for request, local resolution, application and applied event to be distinguished. They are four different things with four different owners and timings:

| Stage | What it is | Who | Output | Failure modes |
|---|---|---|---|---|
| **1. Request** | An intent to affect a target: "this attack instance overlapped this victim in its active window" | Attacker side (A1 for player attacks, A2 for enemy attacks) | `FTDDDamageRequest` | Malformed ids, empty damage type, negative values → rejected before resolution |
| **2. Local hit resolution** | A1's arbitration: dedupe, window check, immunity, block/parry, damage math, outcome classification | **Agent 1 (exclusive)** | `FTDDHitResolution` (local transient) | Out-of-window, duplicate, target absent, source absent → rejected with reason |
| **3. Application** | The single commit of health and posture through GAS `UGameplayEffect` | Target's owner (A1 for the player, A2 for its own actors) — invoked only by the authorised resolver | Attribute change | Clamped at 0 health / 0 posture; no negative attributes |
| **4. Applied event** | Confirmation that stage 3 happened, published for observers | **Agent 1** for player-authored hits; the target's owner for hits on its own actors — see TD-03 for the unified rule | `FTDDDamageAppliedEvent` | Exactly once; never on a rejected request |

```cpp
// PROPOSED — NOT FROZEN. Field requests on existing Core types are marked (req).
struct FTDDDamageRequest                     // Core (Agent 3) — exists in MEAD §5.4
{
    FGuid            InstigatorId;           // source entity (attacker)
    FGuid            TargetId;               // victim entity
    FName            SourceAttackId;         // authored id, e.g. ATK.Ada.Heavy.01
    FGameplayTag     DamageType;             // Damage.Physical.Slash etc.
    float            RawDamage;
    float            PostureDamage;
    FVector          HitLocation;            // world cm
    FVector          HitDirection;           // normalised
    ETDDHitOutcome   PreResolvedOutcome;     // Miss/Hit/Blocked/Parried/... as sent by the attacker
    FGuid            HitInstanceId;          // (req) unique per swing-victim pair; dedupe key
    ETDDStaggerClass StaggerClass;           // (req) see C-04 §4.2 — provisional pending TD-02
};

struct FTDDHitResolution                     // Agent 1 local, not a Core contract
{
    ETDDHitResolutionOutcome Outcome;        // Applied, Blocked, Parried, Immune, Duplicate,
                                             // OutOfWindow, InvalidTarget, InvalidSource, Rejected
    float FinalDamage;
    float PostureDelta;
    bool  bLethal;
    FGuid HitInstanceId;
    FGameplayTag RejectionReason;            // set only when not Applied
};

struct FTDDDamageAppliedEvent                // Core (Agent 3) — exists in MEAD §3.5
{
    FGuid        InstigatorId;
    FGuid        TargetId;
    FGuid        HitInstanceId;              // (req) correlation with the request and the resolution
    float        Amount;                     // health delta actually applied (may be 0)
    float        PostureDelta;               // (req) needed for poise/aggression response
    FGameplayTag DamageType;
    ETDDHitOutcome Outcome;                  // Applied / Blocked / KillingBlow
    FVector      HitLocation;
    bool         bLethal;
    double       AppliedWorldTimeSeconds;
};
```

### 3.3 Authority: who may apply, and the exact sequence

```
A2 enemy attack window opens
  -> A2 builds FTDDDamageRequest(HitInstanceId = new guid per swing+victim)
  -> A1 UTDDPlayerDamageAuthority::SubmitRequest(Request)
        1. validate ids, window open, source alive, target alive
        2. dedupe on (InstigatorId, SourceAttackId, HitInstanceId) within the window + 0.5 s
        3. evaluate defence: Status.Invulnerable -> Immune; Block -> posture only;
           Parry active overlapping the attack's Active phase -> Parried (attacker staggers)
        4. compute damage with attribute multipliers, clamp
        5. verify final values are finite and >= 0
  -> A1 applies: GAS GameplayEffect -> AttributeSet (health, posture)   [stage 3, player only]
  -> A1 publishes FTDDDamageAppliedEvent                                [stage 4, exactly once]
  -> A1 resolves control state (dead / stagger / abort request)         [C-04]
```

**The player's own attacks** follow the mirror sequence: A1 resolves, then calls the target's `ITDDDamageable::ApplyDamage(Resolution)`; the target applies to its own attributes and reports back; A1 publishes the applied event (or the target does — TD-03 settles this).

**Agent 2 must not:** read the player's attribute set, write the player's health/posture, apply damage to the player outside `SubmitRequest`, or re-implement block/parry evaluation. If an enemy needs to know "my attack was blocked", it reads `Outcome` in the applied event.

### 3.4 Health applies irrespective of control resolution

This is the invariant the TD set and the one a naive implementation breaks first. In code terms: stage 3 (attribute commit) is **not** conditional on stage 5 (control state). It executes before classification, on every path — including the path where the abort request will be refused because the traversal is outside `AbortWindow`, and including the forced paths where fallback resolution later fails to find a placement.

Testable statement: *for any request that resolves to `Applied`, the attribute delta is committed exactly once, whether or not any state change follows.*

### 3.5 Duplicate, replay and stale-lifetime rules

| Case | Rule | Outcome |
|---|---|---|
| Same `HitInstanceId` submitted twice | Second rejected; nothing applied; no event | `Duplicate` |
| Same ids but new `HitInstanceId` inside one swing (multi-hit weapon) | Allowed **only** if the attack definition declares multi-hit; otherwise the window's dedupe set rejects it | `Duplicate` / `Applied` for declared multi-hit |
| Retry after a rejected request | Rejected requests are terminal; a retry is a new request | — |
| Request arrives after its window closed (late frame, hitch) | Rejected; never queued, never applied retrospectively | `OutOfWindow` |
| Source despawned before application | Rejected; ids remain valid for logging | `InvalidSource` |
| Target despawned before application | Rejected; no crash, no event | `InvalidTarget` |
| Event consumed after both actors destroyed | Payload carries ids and values only; a listener must not attempt actor resolution | Contract property |

### 3.6 Non-health outcomes (needs TD-03)

| Outcome | Health | Posture | Applied event? | Rationale |
|---|---|---|---|---|
| `Applied` | Yes | Yes if authored | **Yes** | The normal case |
| `Blocked` | No (or reduced by guard) | Yes | **Proposed: yes**, `Amount` 0, `Outcome = Blocked` | Agent 2's aggression logic needs to know a block happened; suppressing the event forces A2 to infer it |
| `Parried` | No | No | **Proposed: yes**, `Outcome = Parried` | The attacker's stagger depends on it (see §8.1 for who applies that) |
| `Immune` | No | No | **Proposed: no** (A2 may still react via its own tags) | Immune hits are not applied; publishing would imply application |
| `WeakPoint` / `KillingBlow` | Yes (multiplied) | Per data | **Yes**, with `Outcome` set | Observers need the distinction for feedback |
| `Miss` | No | No | No | Nothing happened |

This table is the interface between C-03 and C-04 and needs Agent 3/TD's ruling, because it changes what every subscriber must handle.

### 3.7 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.Combat.SingleDamageApplicationAndEvent`** (unit, stub world + stub attribute set)

| # | Setup | Assertion |
|---|---|---|
| 1 | One valid hit | `ApplyDamage` invoked **exactly once**, health delta equals `FinalDamage` ±0.01, exactly **one** applied event, one health-change callback |
| 2 | Same request submitted twice | Second returns `Duplicate`; cumulative **application count stays 1**; event count 1 |
| 3 | Target despawned before submission | `InvalidTarget`; 0 applications; 0 events; exactly one Warning log |
| 4 | Source despawned before submission | `InvalidSource`; 0 applications; 0 events |
| 5 | Request after window close | `OutOfWindow`; 0 applications; 0 events |
| 6 | Damage exactly equal to remaining health | Health reaches exactly 0 (not −ε), `bLethal` true, death transition exactly once, killed event once |
| 7 | Damage exceeding remaining health by 1000 | Health clamped to 0; applied `Amount` reports the **clamped** value or the raw value per TD-03 — the test asserts one documented choice, not both |
| 8 | `Status.Invulnerable` active | `Immune`; 0 health delta; 0 applied events; no state change |
| 9 | Block active, guard absorbs all | Health unchanged, posture reduced by authored value, one `Blocked` event (per §3.6 decision) |
| 10 | Successful parry overlapping the active window | Victim takes 0 damage; attacker receives a stagger request (asserted via C-04, not by direct state inspection) |
| 11 | Non-staggering damage outside traversal `AbortWindow` | Health delta applied; traversal continues; control state unchanged (health/state independence) |
| 12 | Event observed after both actors destroyed | Listener receives the event with ids and no valid actor; no crash; `bLethal` and `Amount` still correct |
| 13 | Negative or NaN damage in the request | Rejected with `Rejected`; no attribute write |

### 3.8 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Confirmation that A2 will submit **requests only** and never apply damage to the player | `NOT RECEIVED` |
| 2 | `ITDDDamageable` implementation behaviour on A2 enemy actors: does it apply and return, or apply and publish? (TD-03 decides the split) | `NOT RECEIVED` |
| 3 | Which fields its poise/boss logic actually consumes (`Amount`, `PostureDelta`, `Outcome`, `bLethal`) | `NOT RECEIVED` |
| 4 | Enemy attack-window → request timing, and whether multi-hit attacks exist in the slice (drives dedupe design) | `NOT RECEIVED` |
| 5 | Whether A2 needs `FTDDEntityKilledEvent` from A1 or produces it itself | `NOT RECEIVED` |

### 3.9 Unresolved alternatives (C-03)

1. **Who publishes the applied event for hits on A2-owned actors.** Option (a) the resolving authority (A1) publishes for all hits — one publisher, simplest ordering guarantee; option (b) the target's owner publishes — cleanest ownership, but ordering between "applied" and "reaction" differs per target type. Agent 1 prefers **(a)** for a single ordered stream. TD-03.
2. **Clamped vs raw `Amount` in the event.** Clamped is honest ("this much was actually removed"); raw is informative for overkill feedback. Agent 1 prefers **clamped**, with `bLethal` carrying the overkill information. TD-03.
3. **`HitInstanceId` ownership.** A1-proposed on the request (dedupe needs a stable key before application). Alternative: dedupe on `(InstigatorId, SourceAttackId, HitCount)` maintained by the resolver. The guid is simpler and survives reordering; recommended.
4. **`ITDDDamageable` vs a pure event contract.** MEAD §5.4 defines the interface; the integration decision requires A1 authority for player-directed hits. §8.1 records the tension; Agent 1 recommends keeping the interface and constraining **who may call it**.

---

## 4. C-04 — Stagger classification, precedence and control outcome

**Contract ID / proposal version:** `C-04` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 4.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-04` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` for whichever representation is chosen (enum, tag or flag). Agent 1 executes the classification and states the alternatives |
| **Implementation owner(s)** | Agent 1: `UTDDCharacterStateMachine` (forced transition, priority queue), `UTDDPlayerDamageAuthority` (classification input), `UTDDCombatComponent` (posture break, parry outcome). Agent 2 sets **data** (attack's stagger class) on its attacks; it does not classify hits |
| **Producers** | A1 produces `FTDDCombatStateChangedEvent`, `FTDDPostureBrokenEvent`, `FTDDControlStateChangedEvent`. A2 produces attack data carrying the stagger class and telegraph phase (C-05) |
| **Consumers (named)** | Agent 2: boss/AI reaction to player stagger and death, encounter victory, audio/VFX. Agent 1: camera, input gating, animation selection. Agent 3/UI: state display |
| **Executable/player-side requirements** | Deterministic classification; single-winner forced application; exact ordering; promotion rules; health independence; queued forced targets applied after restoration |
| **Lifetime and validity** | Forced targets are frame-scoped requests; they are applied or superseded within the resolution, never persisted across frames except through the queue (§4.6) which drains in the same frame |
| **Mutation authority** | Agent 1 only. Agent 2 may not set the player's state, may not call `ApplyStagger` on the player, and may not force `Stagger`/`Dead`/`Cinematic` — it supplies attack data and requests; A1 decides |
| **Proposal status** | **`REQUEST_TD_DECISION`** — the representation (TD-02). Behaviour and precedence are `UNDER_REVIEW` but not in question |
| **Acceptance tests** | `TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification` (§4.8). All `PROPOSED / NOT RUN` |
| **Agent 2 consumer agreement** | `NOT RECEIVED` |
| **Agent 3/TD decision** | `PENDING` — TD-02 required before this contract can be marked agreed |

### 4.2 Classification storage — four alternatives, with consequences

`bCausesStagger` is **not** assumed permanent. Agent 1's state machine does not care where the classification lives; it reads one resolved value per hit. The choice is Agent 3/TD's.

| # | Representation | Where it lives | Advantages | Costs / risks | A1 impact |
|---|---|---|---|---|---|
| **A** | `bool bCausesStagger` on `FTDDDamageRequest` (the v1.2 request) | Core struct field | Smallest possible change; explicit per hit; trivially testable | Boolean cannot express "staggers only on posture break" or "staggers only when target is already winded"; duplicates knowledge already implied by damage type; easy to set wrongly and hard to audit at scale | None — read as `Always`/`Never` |
| **B** | `ETDDStaggerClass` enum on the request: `Never`, `Always`, `OnPostureBreak`, `OnParryOnly` | Core struct field | Expresses the real production cases; authorable per attack; one enum to test exhaustively | One more Core enum; needs an authoring rule so designers do not default to `Always` | None — natural fit |
| **C** | Damage-type tag hierarchy, e.g. `Damage.Physical.Heavy` + a data-table row mapping type → class | `TDDCore` tag registry + `DA_DamageClasses` | No new field; data-driven tuning without code; tag container already exists on the request | The classification becomes implicit in a tag taxonomy; renaming a tag silently changes gameplay; tag mistakes are harder to unit-test than an enum | Small — A1 queries the mapping table by tag |
| **D** | Gameplay Effect / status tag applied to the victim (`Status.Staggering.Hit`) | GAS effect on the target | Reuses GAS; visible to other GAS consumers | Classification happens **after** application, which inverts the required order (classify → fallback → restore → enter); makes the unit test depend on GAS activation; slowest path | Significant — A1 would have to classify after applying, contradicting M1 §3.2.2 ordering |

**Agent 1's recommendation:** **B** (`ETDDStaggerClass`), with **A** as the acceptable minimal fallback if the TD wants the smallest possible Core delta, and with **D excluded** because it inverts the ordering the TD already accepted. **C** is viable but moves a gameplay rule into a naming convention, which is where such rules rot.

Whichever is chosen, Agent 1 reads **one resolved value** and defaults to `Never` when the field/tag is absent — so a missing classification degrades to "does not stagger", never to "staggers by accident".

### 4.3 Classification inputs, evaluated in this order

| Order | Input | Effect on classification | Source |
|---|---|---|---|
| 1 | Health reaches 0 | **Lethal** — forces `Dead`, supersedes all | C-03 stage 3 |
| 2 | Successful parry against the victim's attack | **Staggering** (the *attacker* staggers; the parrying victim does not) | A1 parry resolution |
| 3 | Posture break this hit | **Staggering**, promoted in the same frame | A1 posture check |
| 4 | Request's stagger class / damage-class mapping | `Always` → staggering; `OnPostureBreak` → non-staggering unless (3); `Never` → non-staggering | TD-02 representation |
| 5 | Absent classification | Treated as `Never` (non-staggering), logged once at Warning in development | Defensive default |

**Posture-break promotion rule:** posture is evaluated **after** the posture delta is applied and **before** classification is committed, so the same hit that breaks posture is classified staggering without a second frame. A test asserts this specifically (§4.8 case 4).

### 4.4 Forced-transition precedence — preserved exactly

```
Dead (100)  >  Cinematic (90)  >  Stagger (80)  >  Attack/Block/Parry (60)
            >  Dodge (50)  >  Traversal (40)  >  Land (30)  >  Locomotion/Idle (10)
```

| Rule | Statement |
|---|---|
| Single winner | When several forced targets are pending in one resolution, **only the highest-priority one is applied**; each superseded request is logged once (`Combat.ForcedSuperseded`) with both priorities |
| Exactly one state change | The resolution produces exactly one `FTDDCombatStateChangedEvent` / control-state change |
| Never queued downwards | A lower-priority target never overrides an in-progress higher-priority transition |
| Preservation | This ordering, and the seven exit paths E1–E7, are the accepted M1 v1.4 semantics. C-04 adds no new state and removes none |

**Per-path behaviour (unchanged, restated for the consumer):** lethal → fallback → restoration → `Dead`; cinematic → **no fallback**, capsule frozen, freeze-mode restoration → `Cinematic`; staggering → fallback → restoration → `Stagger`; non-staggering → abort **request** honoured only inside `AbortWindow`, otherwise traversal continues; `Dead` outranks a simultaneous stagger (one state change, `Dead`).

### 4.5 Health independence (testable invariant)

*For every hit whose resolution outcome is `Applied`, the attribute delta commits exactly once, and control-state resolution can neither add, suppress nor repeat it.* A refused abort, a failed fallback, a superseded forced target — none of them change the health delta. Asserted in §4.8 case 7 and mirrored in C-03 §3.7 case 11.

### 4.6 Queued forced targets and event ordering

| Moment | Action |
|---|---|
| Forced target arrives while a traversal fallback/restoration is resolving | Queued (highest priority only); the resolution is never interleaved or abandoned (M1 v1.4 §3.2.2d) |
| Resolution completes | Restoration runs → highest-priority pending target is applied → queue cleared |
| Forced target arrives outside any resolution | Applied immediately in the same frame |
| Forced target arrives during restoration | Queued; applied after the checklist's final step, before the next frame's input |

**Publication order, per frame (one documented sequence for all consumers):**

1. Attribute commit (stage 3, silent to observers until step 2).
2. `FTDDDamageAppliedEvent`.
3. `FTDDPostureBrokenEvent` (if posture crossed its break threshold).
4. Forced transition applied (fallback → restoration → target state).
5. `FTDDCombatStateChangedEvent`.
6. `FTDDControlStateChangedEvent`.
7. Movement-mode change notification, if the mode changed (e.g. `MOVE_Falling` under terminal hold).

A consumer needing "damage happened but the player is not yet staggered" subscribes to step 2; a consumer needing the outcome subscribes to step 5. No consumer should infer state from step 2.

### 4.7 Failure, interruption and cancellation

| Situation | Behaviour |
|---|---|
| Classification missing or malformed | Treated non-staggering; one Warning in development; never a crash |
| Posture break and lethal in the same frame | `Dead` (priority) — posture break does not resurrect the queue |
| Parry succeeded but the attacker is already dead | Parry outcome recorded; no stagger applied to a dead actor |
| Forced target arrives during cinematic | Highest priority wins: `Cinematic` (90) beats `Stagger` (80), loses to `Dead` (100) |
| Two staggers in one frame | One applied; the second is superseded and logged — not refreshed silently (a duration-refresh rule would be a documented exception requiring TD approval) |
| Stagger while terminal hold is active | M1 v1.4 §3.2.2b: staggered while falling, `bPendingGroundingRecovery`, landing recovery on grounding |

### 4.8 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification`** (unit, stub world; deterministic frame stepping)

| # | Setup | Assertion |
|---|---|---|
| 1 | All three pairs (Dead+Stagger, Dead+Cinematic, Cinematic+Stagger) | Exactly one state change each; winner is the higher priority; one superseded log per loser |
| 2 | All three simultaneously | Single state change to `Dead`; two superseded logs |
| 3 | Staggering damage on a grounded player | `Stagger` entered after fallback and restoration (assert order via instrumentation timestamps, not just final state) |
| 4 | Hit that breaks posture, classified non-staggering | `Stagger` in the **same frame**; no second frame required |
| 5 | Successful parry | Victim: no stagger, no health loss. Attacker: `Stagger` forced |
| 6 | Non-staggering damage, inside `AbortWindow` | Abort request honoured: fallback → restoration → `Locomotion`; health delta present |
| 7 | Non-staggering damage, outside `AbortWindow` | Traversal continues; control state unchanged; **health delta still present** (independence) |
| 8 | Lethal + staggering in one hit | `Dead` only; no `StaggerEvent` emitted; health 0 |
| 9 | Cinematic takeover with a stagger pending | `Cinematic`; capsule transform **byte-equal** before and after (no fallback movement); freeze-mode restoration ran |
| 10 | Cinematic takeover with lethal | `Dead`; cinematic does not supersede death |
| 11 | Forced target arriving mid-fallback | Resolution completes, restoration runs, then the target applies — assert the target applies **after** restoration and that no capsule write happened after the apply |
| 12 | Classification representation swapped (A ↔ B ↔ C via test fixture) | **Identical outcome matrix** in all three representations — proves A1's logic is representation-independent |
| 13 | Classification field absent | Non-staggering; exactly one Warning; no state change |
| 14 | Two staggers in one frame | One application; second logged superseded; no duration refresh |

**Retained:** M1 v1.4 `TDD-Unit.Movement.FallbackResolution` and `TDD-Functional.Movement.TraversalAbortPaths` remain the authority for the fallback/hold behaviour these tests call into. Contract tests assert the **contract**; they do not replace those.

### 4.9 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Which stagger classes its attacks need (`Never` / `Always` / `OnPostureBreak` / `OnParryOnly`) | `NOT RECEIVED` |
| 2 | Confirmation that A2 will not call `ApplyStagger` on the player or force states | `NOT RECEIVED` |
| 3 | Which events its boss logic subscribes to (state changed vs posture broken vs damage applied) | `NOT RECEIVED` |
| 4 | Whether any enemy needs "I was parried" as a distinct signal (affects C-03 §3.6) | `NOT RECEIVED` |

### 4.10 Unresolved alternatives (C-04)

1. **Representation** — A/B/C/D in §4.2; Agent 1 recommends B. **TD-02.**
2. **Stagger duration refresh on re-hit.** Proposed: no refresh (supersede and log). If production wants refresh, it needs an explicit rule and a test.
3. **Posture regeneration timing** relative to stagger entry — A1 has it in M1 v1.4 as data; no change requested.
4. **Whether `ApplyStagger` survives on `ITDDCombatant`.** Under A1 damage authority, only A1 calls it on the player; A2 enemies are staggered by A1's resolution through `ITDDDamageable`. Whether the method stays on the interface at all is Agent 3's call.

---

## 5. C-05 — Telegraph timing and lifecycle

**Contract ID / proposal version:** `C-05` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 5.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-05` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` for the event structs and any broker/subsystem. Agent 1 requests no exception; the broker must not be owned by Agent 1, or Agent 1 would be publishing Agent 2's attack lifecycle |
| **Implementation owner(s)** | Agent 2: enemy telegraph production from attack montages/windows. Agent 1: player telegraph production and the parry/block consumer. Broker (proposed): `UTDDTelegraphBroker` world subsystem, Agent 3 |
| **Producers** | A2: enemy attack telegraphs (open / phase change / close). A1: the player's own attack telegraph, exposed both as an event and via `ITDDCombatant::IsTelegraphingAttack` / `GetAttackTelegraphRemaining` (existing M1 interface) |
| **Consumers (named)** | A1: parry/block evaluation, dodge i-frame timing, camera/audio cues. A2: its AI reading the **player's** telegraph for defensive decisions (block/dodge) but not for hit resolution |
| **Executable/player-side requirements** | Receive a complete, ordered lifecycle with a monotonic instance id; compare windows on a shared gameplay clock; never apply damage from a telegraph; tolerate cancellation and unload without a stuck defence state |
| **Lifetime and validity** | An `AttackInstanceId` is valid from `Opened` to `Closed` and never reused. After `Closed`, any late message about that id is rejected. Open telegraphs must be force-closed on world unload, source death or source despawn |
| **Mutation authority** | A2 owns its telegraphs and is the only writer of its own timeline; A1 owns only its consumption. Neither may rewrite the other's timestamps. A1 never publishes a telegraph for an enemy and vice versa |
| **Proposal status** | `UNDER_REVIEW`. Unresolved: (a) canonical gameplay clock ownership (TD-06); (b) event-only vs event + registry query for late subscribers; (c) whether phase changes are events or polled |
| **Acceptance tests** | `TDD-Contract.Combat.TelegraphWindowConsumerSemantics` (§5.8) with a deterministic clock fixture. All `PROPOSED / NOT RUN` |
| **Agent 2 consumer agreement** | `NOT RECEIVED` — required as the **producer** in this contract, not just a consumer |
| **Agent 3/TD decision** | `PENDING` |

### 5.2 Lifecycle: four messages, exactly once each

```cpp
// PROPOSED — NOT FROZEN
struct FTDDTelegraphOpenedEvent
{
    FGuid                AttackInstanceId;    // unique per swing, never reused
    FGuid                SourceEntityId;      // attacker
    FGuid                TargetEntityId;      // intended victim; may be invalid for area attacks
    FName                AttackId;            // authored content id
    FGameplayTag         AttackTag;           // e.g. Combat.Attack.Heavy
    double               StartGameplayTime;   // combat gameplay clock (see 5.3)
    double               WindupEndGameplayTime;
    double               ActiveEndGameplayTime;
    double               RecoveryEndGameplayTime;
    float                AreaRadiusCm;        // 0 for single-target
    bool                 bUnblockable;        // informational; block evaluation still uses tags
};

struct FTDDTelegraphPhaseChangedEvent
{
    FGuid              AttackInstanceId;
    ETDDTelegraphPhase Phase;                 // Windup, Active, Recovery
    double             PhaseStartGameplayTime;
};

struct FTDDTelegraphClosedEvent
{
    FGuid               AttackInstanceId;
    ETDDTelegraphEndReason Reason;            // Completed, Cancelled, Interrupted,
                                              // SourceDied, SourceUnloaded, Superseded
    double              ClosedGameplayTime;
};

// Optional, for late subscribers only (TD decision): query current state
struct FTDDTelegraphState { FGuid AttackInstanceId; FGuid SourceEntityId; ETDDTelegraphPhase Phase; double PhaseEndGameplayTime; };
```

| Message | Exactly-once guarantee |
|---|---|
| `Opened` | Once per `AttackInstanceId`. A duplicate id is **rejected** and logged (`Combat.TelegraphDuplicate`) |
| `PhaseChanged` | At most once per phase transition, in order Windup → Active → Recovery. Skipping a phase is allowed (a cancelled attack goes Windup → Closed) |
| `Closed` | Exactly once, and always follows `Opened`. A close without an open is rejected and logged |
| No message after `Closed` | Any later message for that id is rejected; the id is retired |

### 5.3 Clock and units — the part that must be exact

| Requirement | Agent 1's stated need |
|---|---|
| Unit | All telegraph timestamps in **gameplay seconds**, `double` precision, millisecond resolution sufficient |
| Clock definition | Accumulated world delta **scaled by the actor's custom time dilation**, so hitstop and slow-motion stretch windows exactly as the animation stretches. A global world pause must **stop** the clock; a pair hitstop must **slow** it for both participants identically |
| Ownership | **TD-06.** Either `TDDCore` provides `UTDDGameplayTimeSubsystem` (agent-3 owned, queryable, monotonic) or Agent 1 maintains a local accumulator per combat pair — the latter risks two divergent clocks across modules, so Agent 1 recommends the Core subsystem |
| Precision needs of the consumer | Parry evaluation resolves on the **same frame** as the hit: Agent 1 needs to know whether the defender's parry window and the attacker's `Active` phase overlapped **this frame**. That is a sub-17 ms requirement at 60 FPS, which timestamps alone cannot guarantee — hence the rule below |
| Boundary convention | Windows are **half-open**: `Active` = `[WindupEnd, ActiveEnd)`. A hit at exactly `WindupEnd` is active; at exactly `ActiveEnd` it is not. Both are asserted at the boundary |
| Ordering | Messages for one attack are ordered; messages across attacks are ordered by `StartGameplayTime`, tie-broken by `AttackInstanceId` (guid ascending) so a replay of the same frame is deterministic |

**Do not evaluate parry by timestamp subtraction.** The consumer rule Agent 1 requires is *phase overlap at hit resolution*: the attack's current phase is queried/known from the last `PhaseChanged` **plus** the clock; the defender's parry tag is read; both must be live in the same frame. Timestamps are for scheduling and diagnostics, not for a tolerance check that could pass a frame late.

### 5.4 Telegraph ≠ damage

A telegraph is a **timing and identity announcement**. It carries no authority:

- The telegraph never applies damage; only C-03's resolution path does.
- The telegraph does not arbitrate a hit: the hit window overlap (montage notify / A2 window) does.
- A telegraph may be a lie to the player on purpose (feint) — that is an authoring choice within A2, and A1 must not treat a telegraph as a guaranteed hit.
- Conversely a hit **must not** resolve without a preceding `Opened` for its instance; if it does, Agent 1 treats it as `InvalidSource` and logs (`Combat.HitWithoutTelegraph` in development only, not in shipping).

### 5.5 Pause, dilation, unload, late subscription, missed windows

| Situation | Required behaviour |
|---|---|
| World paused | Clock stops; no messages; windows retain their remaining duration; on resume the montage and the telegraph resume together |
| Pair hitstop / slow-motion | Both timestamps and montage advance on the scaled clock, so window boundaries stay aligned with the animation. A1 asserts no drift > 1 frame over a 2 s attack with 3 hitstops |
| World unload / level transition | A2 force-closes every open telegraph with `SourceUnloaded` **before** teardown; A1 must end up with no live defence state. If a telegraph is never closed, A1's defence must still time out via its own montage and must not latch |
| Late subscriber (A1 joins after `Opened`) | Receives no history. If the query surface exists (TD decision), it queries `GetActiveTelegraphs` once and continues from there. Without a query surface, a late subscriber must treat unknown instances as "no telegraph" and must not block parry |
| Missed window (message arrives after `Closed`) | Rejected by the broker; A1 logs `Combat.TelegraphMissed` once at Verbose and proceeds with current state |
| Cancellation before `Active` (source staggered/died) | `Closed(Cancelled/Interrupted/SourceDied)`; a **buffered** block/parry intent is **not** consumed — it remains buffered for its 0.20 s window. This prevents punishing the player for an attack that never happened |
| Cancellation during `Active` | Hit resolution for that instance is void; no damage; the player's defence is evaluated normally on the next hit |
| Duplicate `AttackInstanceId` (reused guid) | Rejected; the first open remains authoritative; one Error log |
| Telegraph arriving from a despawned source | Rejected at `Opened` if the source cannot be resolved; one Warning |

### 5.6 What Agent 1 needs from the producer, concretely

1. Open the telegraph **before** the windup montage section begins, at or before the first frame a player could read it (target ≤ 1 frame of lead; more is acceptable, less is not).
2. Send `PhaseChanged` on the frame the phase changes, not on a timer.
3. Close exactly once on completion, interruption, death or unload.
4. Never send a telegraph for an attack that cannot execute (e.g. cancelled before the windup starts).
5. Do not encode damage numbers in the telegraph. Agent 1 ignores them by contract, and their presence would tempt consumers to bypass C-03.

### 5.7 Interruption and cancellation of a defence

| Player situation | Behaviour |
|---|---|
| Parry input during the attacker's windup | Buffered (0.20 s); consumed on the first overlapping `Active` frame |
| Parry input after `Active` began | Evaluated on the frame; a late parry is a block at best, per authored rules |
| Block held across a cancelled attack | Remains held; no posture cost, since nothing resolved |
| Player staggered while parrying | Parry cancelled; `Stagger` entered; defence tags cleared before state entry |
| Player dies while parrying | `Dead`; defence cleared; no events on the cleared tags |

### 5.8 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.Combat.TelegraphWindowConsumerSemantics`** (unit, deterministic clock fixture, no world)

| # | Setup | Assertion |
|---|---|---|
| 1 | Open with windup 0.40 s, active 0.20 s, recovery 0.30 s | Phase transitions occur at exactly those gameplay times ±1 ms; `Active` includes `WindupEnd` and excludes `ActiveEnd` (boundary asserted at both ends) |
| 2 | Parry input 1 frame before `Active` | Buffered, then succeeds on the first active frame |
| 3 | Parry input 1 frame after `ActiveEnd` | Fails; no stagger on the attacker; no damage taken by the defender for that instance |
| 4 | Pause for 5 s during windup | No phase change during pause; after resume the windup completes with its remaining duration ±1 frame |
| 5 | Hitstop applied to the pair for 100 ms | Window boundaries shift with the scaled clock; no drift > 1 frame relative to the montage |
| 6 | Cancel before `Active` | `Closed(Cancelled)`; buffered defence **retained**; buffer expires naturally |
| 7 | Duplicate `AttackInstanceId` | Second `Opened` rejected; one Error; no state change |
| 8 | `Closed` without `Opened` | Rejected; one Warning |
| 9 | Message after `Closed` | Rejected; `Combat.TelegraphMissed` logged once |
| 10 | Unload with 3 open telegraphs | 3 `Closed(SourceUnloaded)`; defence state cleared; zero live instances |
| 11 | Late subscriber with a query surface | Sees exactly the open instances, no history |
| 12 | Telegraph carries a damage field | It is ignored: damage equals C-03's resolution, never the telegraph's number (assert both differ) |

### 5.9 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Agreement to produce the four-message lifecycle, or a documented counter-proposal | `NOT RECEIVED` |
| 2 | Clock choice: is A2 able to publish gameplay-scaled timestamps, or must Core own the clock? (TD-06) | `NOT RECEIVED` |
| 3 | Whether attack montages can guarantee one phase change per phase (notify-based) | `NOT RECEIVED` |
| 4 | Whether A2's AI needs the **player's** telegraph as an event, a poll of `ITDDCombatant`, or both | `NOT RECEIVED` |
| 5 | Enemy attack set in the slice: single-target vs area, feints, multi-hit | `NOT RECEIVED` |

### 5.10 Unresolved alternatives (C-05)

1. **Clock ownership** — Core gameplay-time subsystem (recommended) vs per-pair accumulators. **TD-06.**
2. **Late-subscription support** — event-only (simplest, no stale-data risk) vs event + `GetActiveTelegraphs` query (needed if A1 can be spawned into a live fight). A1 needs the query only in the second case; it is cheap either way.
3. **Phase messages vs polling.** Events (proposed) keep traffic at 3 messages per attack; polling would move cost to every consumer every frame.
4. **Where the broker lives** — Core (proposed) vs `TDDGameplay`. If `TDDGameplay`, Agent 1 would be hosting A2's lifecycle, which contradicts the ownership split; Core is preferred.

---

## 6. C-06 — Player-side interaction routing and lifecycle

**Contract ID / proposal version:** `C-06` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 6.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-06` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` — the lifecycle (interface + events) is Core-owned per the accepted decision. Agent 1 implements the **router**, not the contract |
| **Implementation owner(s)** | Agent 1: `UTDDInteractionRouterComponent` (focus, input, progress, terminal calls, cancellation). Agent 2: `ITDDInteractable` implementations on world actors |
| **Producers** | A1 produces `FTDDInteractionFocusedEvent`, `FTDDInteractionProgressEvent` (throttled), `FTDDInteractionEndedEvent`. A2 produces prompt/eligibility data via the interface and completion results |
| **Consumers (named)** | A2 interactables (consume begin/tick/end/cancel); UI (prompt display, progress); audio (loop start/stop); narrative (completion routed separately, never through the router) |
| **Executable/player-side requirements** | Deterministic focus selection; exactly one begin; progress integration while held; exactly one terminal call; cancellation ordered before any forced state entry; never grants progress itself |
| **Lifetime and validity** | Focus target is a `TWeakObjectPtr` + stable `FGuid InstanceId`; eligibility is re-evaluated every frame; the focus drops immediately on invalid/out-of-range/unloaded. An interaction session lives from `Begin` to exactly one terminal call, never spanning a level transition |
| **Mutation authority** | Agent 1: player state, input, hold progress, session state. Agent 2: the interactable's own state, its prompt data, its completion result. **Neither may complete the other's half**: A2 cannot end the session; A1 cannot grant a memory/quest |
| **Proposal status** | `UNDER_REVIEW`. Unresolved: (a) hold-progress authority (TD-07); (b) prompt data shape and localisation; (c) whether tap/hold is authored per interactable or per verb |
| **Acceptance tests** | `TDD-Contract.Interaction.PlayerRoutingAndCancellation` (§6.7). All `PROPOSED / NOT RUN` |
| **Agent 2 consumer agreement** | `NOT RECEIVED` |
| **Agent 3/TD decision** | `PENDING` |

### 6.2 The lifecycle: five calls, one session

MEAD §4.5 already names the interface (`GetInteractionPrompt`, `CanInteract`, `BeginInteract`, `TickInteract`, `EndInteract`, `CancelInteract`). Agent 1 asks for the addition of an explicit **result** and **cancel reason** so the terminal call is unambiguous:

```cpp
// PROPOSED — NOT FROZEN (Core, Agent 3 owns). Extends MEAD §4.5 rather than replacing it.
UENUM() enum class ETDDInteractionEndResult : uint8 { Completed, Failed, Refused };
UENUM() enum class ETDDInteractionCancelReason : uint8
{
    Released, OutOfRange, FocusLost, Damaged, Staggered, Died, Cinematic,
    TargetUnloaded, Superseded, LevelTransition, Restarted
};

struct FTDDInteractionPrompt
{
    FText        Label;              // from a String Table; A1 never composes prose
    FGameplayTag VerbTag;            // Interact.Verb.* — drives icon and animation choice
    float        HoldDurationSeconds;// 0 == instant/tap
    bool         bEnabled;           // false => no prompt at all (see 6.3)
    FGameplayTag BlockedReasonTag;   // diagnostic only; never displayed as a lock
};

class ITDDInteractable
{
    virtual FGuid  GetInstanceId() const = 0;                 // stable runtime identity
    virtual FName  GetInteractionId() const = 0;              // authored content id
    virtual bool   CanInteract(const FTDDInteractionContext&) const = 0;
    virtual FTDDInteractionPrompt GetPrompt(const FTDDInteractionContext&) const = 0;
    virtual void   BeginInteract(const FTDDInteractionContext&) = 0;
    virtual void   TickInteract(const FTDDInteractionContext&, float Progress01) = 0;
    virtual void   EndInteract(const FTDDInteractionContext&, ETDDInteractionEndResult) = 0;
    virtual void   CancelInteract(const FTDDInteractionContext&, ETDDInteractionCancelReason) = 0;
};
```

### 6.3 Focus selection and prompt rules

| Rule | Statement |
|---|---|
| Candidate volume | Forward cone from the camera-relative aim, half-angle 60°, max range authored per interactable, line-of-sight trace ignoring the player |
| Score | authored `Priority` (int32, higher wins) → facing alignment → distance (lower wins) → `InteractionId` lexicographic (deterministic tiebreak) |
| Eligibility | `CanInteract` **and** requirement tags satisfied **and** not blocked by player state (e.g. `Cinematic`, `Dead`) |
| Ineligible candidates | **No prompt.** No locked/greyed prompt, no "you need X" text — the slice has no such UI and inventing one would be a design decision, not a contract one |
| Prompt change | Only when the focused `InteractionId` changes or its prompt data changes; otherwise no per-frame prompt event |
| Focus hysteresis | Switching requires the new candidate to score strictly higher by > 10 % to avoid flicker between near-equal candidates |

### 6.4 Tap vs hold — and who owns progress (needs TD-07)

**Proposed: the router owns hold duration and progress.** Reasons: it must be frame-accurate, it must be cancellable by player state, and a per-interactable implementation would produce N different damping curves and N different cancel bugs. The interactable receives `Progress01` and decides only what to do with it (open a door gradually, play a reading animation).

| Input | Behaviour |
|---|---|
| `HoldDurationSeconds == 0` | Completes on press; `Begin` and `End(Completed)` may occur in the same frame, but not the same call stack without a `Tick(1.0)` — ordering asserted |
| `HoldDurationSeconds > 0` | `Begin` on press; `Tick(progress)` each frame while input held, focus valid, no blocking state; `End(Completed)` at `progress >= 1.0` (±1 frame) |
| Release before completion | `Cancel(Released)`; **no completion, no grant** |
| Input held but focus lost | `Cancel(FocusLost)` at the frame focus changes |
| Player moves beyond range mid-hold | `Cancel(OutOfRange)` before the movement is committed to the state machine |

### 6.5 Cancellation ordering — one table, because ordering is the whole risk

| Trigger | Cancel reason | Order relative to the cause |
|---|---|---|
| Damage received, non-staggering | `Damaged` | After the attribute commit (C-03 stage 3), **before** any abort/state resolution |
| Staggering damage / posture break | `Staggered` | Before `Stagger` is entered; the interactable must not still be ticking when the state changes |
| Death | `Died` | Before `Dead` is entered; exactly once |
| Cinematic takeover | `Cinematic` | Before the camera takes over and before the capsule freezes |
| Target destroyed / streamed out | `TargetUnloaded` | On the frame the weak ptr invalidates or unregistration arrives |
| Another interactable becomes the focus | `Superseded` | Before the new focus's prompt is published |
| Level transition / EndPlay | `LevelTransition` | Before teardown; exactly once; no dangling session |
| Player releases input | `Released` | Immediate |

**Exactly-once guarantee:** the router asserts a session state machine (`Idle → Begun → Terminal`) and refuses `End`/`Cancel` from `Idle` or after `Terminal`, logging `Interaction.ProtocolViolation`. Agent 2 implementations must tolerate a `Cancel` arriving in the same frame as a `Begin` (player taps, then is staggered).

### 6.6 What the router will **not** do

- It does not grant memory fragments, quest steps, items or checkpoints. Completion is reported; the interactable or its owning subsystem performs the grant (A2/A3).
- It does not decide eligibility requirements beyond tag checks; authored conditions are evaluated by the interactable.
- It does not compose prompt text; text comes from a String Table keyed by the interactable's data (MEAD §4.5).
- It does not persist anything across a level transition. A session never survives teardown.

### 6.7 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.Interaction.PlayerRoutingAndCancellation`** (unit for routing, functional for the world cases)

| # | Setup | Assertion |
|---|---|---|
| 1 | Three eligible interactables, varying priority/distance | Deterministic focus; 1000 repeated evaluations pick the same instance |
| 2 | Two candidates within 10 % score | Hysteresis prevents switching until the margin is exceeded |
| 3 | Ineligible candidate (requirement unsatisfied) | **No prompt**, no begin, no log spam (one Verbose at most) |
| 4 | Tap interaction (hold 0) | Exactly one `Begin`, exactly one `Tick(1.0)` or none, exactly one `End(Completed)`; grant count 1 |
| 5 | Hold 1.5 s interaction | Progress monotonic 0→1; completion at 1.5 s ±1 frame; `Tick` called once per frame while held |
| 6 | Release at 0.75 progress | Exactly one `Cancel(Released)`; **zero** `End`; grant count 0 |
| 7 | Non-staggering damage mid-hold | `Cancel(Damaged)` occurs **before** state resolution; health delta still applied; session terminal |
| 8 | Stagger mid-hold | `Cancel(Staggered)` before `Stagger` entry; exactly one terminal call |
| 9 | Cinematic takeover mid-hold | `Cancel(Cinematic)` before freeze |
| 10 | Interactable streamed out mid-hold | `Cancel(TargetUnloaded)` within 1 frame; no dangling session; no crash |
| 11 | Duplicate `Begin` from the router (simulated re-entry) | Second refused; one `ProtocolViolation` log |
| 12 | Second `End` after terminal | Refused; exactly one grant in total |
| 13 | Unregistered verb tag in prompt data | Begin refused with `End(Refused)`; one Error naming the tag; no animation played |
| 14 | Level transition mid-hold | `Cancel(LevelTransition)`; no session persists; on reload a fresh session is required |

### 6.8 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Agreement on the extended interface (result + cancel reason) or a counter-proposal | `NOT RECEIVED` |
| 2 | The actual interactable set in the slice, with `InstanceId`/`InteractionId` schemes and hold durations | `NOT RECEIVED` |
| 3 | Whether any interactable needs to *refuse* completion at the last moment (e.g. requirement invalidated mid-hold) — affects `End(Refused)` semantics | `NOT RECEIVED` |
| 4 | Whether prompts are needed at all in the slice (currently debug-only), and who authors the String Table keys | `NOT RECEIVED` |
| 5 | Confirmation that grants go through A2/A3 subsystems, never the router | `NOT RECEIVED` |

### 6.9 Unresolved alternatives (C-06)

1. **Hold-progress authority** — router (proposed) vs interactable. **TD-07.**
2. **Interface extension** — result/reason parameters (proposed) vs a single `EndInteract(bool)` with a separate reason event. The proposed form keeps exactly-once explicit.
3. **Focus source** — camera-relative aim (proposed) vs actor forward. The camera bias is MEAD §4.5; the contract only needs it stated once.
4. **Prompt visibility** — debug widget only until UI exists. Not a contract change; a content/UI deliverable.

---

## 7. C-07 — Shared IDs and Gameplay Tags needed by Agent 1

**Contract ID / proposal version:** `C-07` · `A1-R1` · `PROPOSED — NOT FROZEN`

### 7.1 The record, as the packet requires

| Required field | Agent 1 response |
|---|---|
| **Contract ID and proposal version** | `C-07` / `A1-R1` (v1.0) |
| **Publisher (Core contract authority)** | `Agent 3/TD` — registry, tag governance and any typed id wrappers. Agent 1 submits an **inventory of needs**, not a registry |
| **Implementation owner(s)** | Agent 3: registry/governance, `UTDDEventBus`, id types. Agent 1: player-side producers of `EntityId`; consumers of the requested tags |
| **Producers** | A1 assigns `EntityId` for the player pawn (and for any A1-spawned entity); A1 authors no shared ids. A2 assigns `EntityId` for world characters. Authored ids (`RouteId`, `InteractionId`, `AttackId`) are content/A2 authored; the tag registry is Agent 3's |
| **Consumers (named)** | A1: tags for state/defence/traversal eligibility/interaction verbs. A2: `EntityId` for damage routing and perception, tags for attack classification and encounter logic. A3/UI: state tags for display |
| **Executable/player-side requirements** | Stable identity for the player across death/respawn; tag-based gating without hard-coded names; deterministic validation of unknown/retired ids; no parsing of authored id strings at runtime |
| **Lifetime and validity** | `EntityId`: valid while the entity exists in the world; **not** persisted; re-issued on a new session. Authored ids: valid across sessions and saves; retirement is a governance action, not a rename. Tags: valid for the life of the registry version; unknown tags are non-fatal but diagnostic |
| **Mutation authority** | Agent 3 alone registers tags and defines id types. Agent 1 may assign its own entities' `EntityId`; no agent may register a tag or mint an id class unilaterally |
| **Proposal status** | `UNDER_REVIEW` — the inventory is submitted; tag naming and the retirement policy need Agent 3/TD approval (TD-08) |
| **Acceptance tests** | `TDD-Contract.Core.Agent1IdAndTagRegistry` (§7.7). All `PROPOSED / NOT RUN` |
| **Agent 2 consumer agreement** | `NOT RECEIVED` |
| **Agent 3/TD decision** | `PENDING` |

### 7.2 Three identity classes, kept apart

| Class | Type | Example | Stable across | Who assigns | May code parse it? |
|---|---|---|---|---|---|
| **Runtime entity identity** | `FGuid` | `{7f3a…}` for an enemy instance | The entity's lifetime only. **Not** saves, not sessions | Whoever spawns the entity (A1 player, A2 world) | No — opaque |
| **Authored content identity** | `FName` | `TRV.CH01.SCN-014.001`, `ATK.Ada.Heavy.01`, `INT.Shrine.CH01.01` | Saves, sessions, level edits (by policy) | Content authors / A2 data | No at runtime; validators may |
| **Canon place identity** | `FName` | `CH01`, `SCN-014` | Everything; owned by the canon register (A2/A3) | Canon register | Only by the canon/validator layer |

The rule Agent 1 depends on: **an `EntityId` identifies an instance; an authored id identifies content; a canon id identifies a place.** Any contract that asks one to do another's job will break at the first respawn, save or rename.

Additional identity notes:

- The **player keeps one `EntityId`** across death and respawn within a session; the pawn instance may change, identity does not. This is what C-02's invalidation rules assume.
- `FGuid` of all-zeros is **invalid by definition** and must never be treated as a real entity.
- `MemoryId` is an `int32` 1–7 in the canon model (MEAD §13.2, `UTDDMemorySubsystem`); Agent 1 does not propose changing it to a guid — it is content, and its range is canonically fixed.

### 7.3 Tag inventory — required by Agent 1

All namespaces below are **requests to the registry**, except the `Status.*` and `Damage.*` entries already present in MEAD §5.1/§5.2. "Existing" means the name appears in an approved document, not that it is registered in code (no code exists).

| Tag | Namespace | Status | Feature that needs it | Producer | Consumer (A1 side) | Justification |
|---|---|---|---|---|---|---|
| `Status.Attacking` | `Status` | **Existing** (MEAD §5.1) | Attack state mirror | A1 | A1, A2 (AI reads it) | Already the agreed vocabulary |
| `Status.Blocking` | `Status` | **Existing** | Block | A1 | A1, A2 | Defence evaluation |
| `Status.Parrying` | `Status` | **Existing** | Parry window | A1 | A1 | C-05 parry overlap |
| `Status.Invulnerable` | `Status` | **Existing** | Dodge i-frames | A1 | A1 | C-03 immunity outcome |
| `Status.Staggered` | `Status` | **Existing** | Stagger | A1 | A1, A2 | C-04 |
| `Status.Grabbed` | `Status` | **Existing** | Grab (M3) | A1/A2 | A1 | Declared for M3, unused in M1 |
| `Status.Cinematic` | `Status` | **Existing** | Cinematic lock | A1 | A1, A2 | C-04 precedence |
| `Status.Interacting` | `Status` | **Requested** | Interaction session | A1 | A1, A2 (AI must not interrupt?) | C-06 needs a tag other systems can read without an interface call |
| `Status.Traversing` | `Status` | **Requested** | Traversal active | A1 | A1, debug/telemetry | Same reason; also lets A2 gate AI attacks during traversal |
| `Status.Airborne` | `Status` | **Requested** | Airborne/falling | A1 | A1, A2 | AI ground-attack gating (C-02 alternative to reading mode) |
| `Status.LockedOn` | `Status` | **Requested** | Target lock | A1 | A1, A2 | Encounter threat logic |
| `Damage.Physical.Slash` | `Damage` | **Existing** | Attack type | Content (A2 data) | A1 | Damage type vocabulary |
| `Damage.Physical.Blunt` | `Damage` | **Requested** | Second damage class | Content | A1 | Needed if the slice has more than one weapon class |
| `Damage.Physical.Pierce` | `Damage` | **Requested** | Third class | Content | A1 | Same; can be deferred if the slice is one-weapon |
| `Damage.Class.Staggering` / `.NonStaggering` | `Damage` | **Requested, conditional** | Only if TD-02 chooses representation **C** (tag-based classification) | Content | A1 | Not needed under A or B |
| `Traversal.Capability.Vault` | `Traversal.Capability` | **Requested** | C-01 capability gating | A2 authored marker, A1 granted set | A1 (eligibility) | Routes must declare requirements as tags, not enums, so content can gate without code |
| `Traversal.Capability.Mantle` | `Traversal.Capability` | **Requested** | Same | A2 | A1 | Same |
| `Traversal.Capability.LedgeShimmy` | `Traversal.Capability` | **Requested** | Same | A2 | A1 | Same |
| `Traversal.Capability.Drop` | `Traversal.Capability` | **Requested** | Same | A2 | A1 | Same |
| `Traversal.Capability.ClimbLadder` | `Traversal.Capability` | **Requested** | Same | A2 | A1 | Same |
| `Interact.Verb.Open` / `.Read` / `.Take` / `.Talk` / `.Climb` / `.Rest` / `.Examine` | `Interact.Verb` | **Requested** | Prompt verb → animation/icon mapping (C-06) | A2 prompt data | A1 router, UI | The verb must be data, not a hard-coded enum, per MEAD §4.5 |
| `Combat.Telegraph.Phase.*` | `Combat.Telegraph` | **Requested, conditional** | Only if tags are preferred to `ETDDTelegraphPhase` | A2 | A1 | Enum preferred; tags acceptable |
| `Input.Intent.*` | — | **Not requested** | — | — | — | Input intents are A1-internal; publishing them would invite consumers to simulate input |

**Deliberately not requested:** `State.*` (would duplicate `Status.*` and create two vocabularies for one concept), `TDD.*` root brand tags, per-attack tags (authored ids already cover that), and any tag that names an implementation class.

### 7.4 Persistence, lifetime and network

| Requirement | Agent 1 position |
|---|---|
| `EntityId` persistence | **No.** Ids are session-runtime. A save stores authored ids and entity *types*, never runtime guids |
| Authored id persistence | **Yes, if referenced** — memory fragments, interaction completions and checkpoint state reference authored ids (`InteractionId`, `MemoryId`), so those ids must be retirement-governed (TD-08) |
| Route id persistence | Depends on TD-04: if narrative or checkpoints reference routes, they must be retirement-governed; if not, they may be freely renamed per level |
| Network replication | **Not required in the vertical slice** (single-player). If multiplayer arrives, `FGuid`/`FName` remain replicable; no pointer-based identity is used anywhere in this contract |
| Save compatibility | A save referencing a retired id must fail **loudly** with a named error, never silently rebind to a similarly-named id. This is the single most important policy in C-07 and it is Agent 3's to define |
| Streaming | `EntityId` of a streamed-out entity becomes stale; consumers must handle `InvalidTarget` (C-03) rather than assume liveness |

### 7.5 Invalid, unknown and retired ids

| Case | Required behaviour | Consumer impact |
|---|---|---|
| Empty/zero `FGuid` | Invalid; request rejected with `InvalidTarget`/`InvalidSource`; one Warning | No crash, no event |
| Unknown tag (not registered) | Non-fatal; the operation requiring the tag does not match; one Warning in development, silent in shipping | Must not throw, must not assert |
| Malformed authored id (format violation) | Editor validator **Error**; runtime treats as opaque and attempts normal resolution | Authoring-time failure, not a runtime crash |
| Retired authored id at runtime | Explicit `Retired` resolution status; the referencing feature is disabled with a diagnostic, **never** rebound | Prevents silently activating a different route/interaction |
| Duplicate authored id | Second registration refused at load with an Error; first wins deterministically | Authoring bug surfaced, not a coin flip |

### 7.6 Acceptance tests — `PROPOSED / NOT RUN`

**`TDD-Contract.Core.Agent1IdAndTagRegistry`** (unit + data-validation layer)

| # | Setup | Assertion |
|---|---|---|
| 1 | Data-driven completeness over §7.3 | Every tag Agent 1 lists as required is registered and resolvable; unregistered required tags fail the test with the tag name |
| 2 | Register the same tag twice | Second registration rejected with a diagnostic; registry state unchanged |
| 3 | Resolve an unknown tag | Returns invalid handle; one Warning; no crash; dependent feature simply does not match |
| 4 | Resolve a retired authored id | Returns `Retired`, not a substitute id; the referencing feature is disabled; one Error |
| 5 | Two markers claim one `RouteId` | Second refused; first authoritative; query result stable across 1000 calls |
| 6 | Event delivered after both actors destroyed | Payload ids still readable; no actor resolution attempted; no crash |
| 7 | Empty `FGuid` in a damage request | Rejected `InvalidTarget`; 0 applications; 0 events |
| 8 | Player death → respawn | `EntityId` identical before and after; C-02 `FrameCounter` monotonic; no duplicate identity in the registry |
| 9 | Authored id format violation | Editor validator emits an Error naming the asset and the id; runtime resolution of the same id does not crash |

### 7.7 Dependencies on Agent 2 (this contract)

| # | Need | Status |
|---|---|---|
| 1 | Its own id/tag inventory, so the registry is consolidated once rather than twice | `NOT RECEIVED` |
| 2 | Agreement on `RouteId` / `InteractionId` formats and who validates them | `NOT RECEIVED` |
| 3 | Whether A2 needs `EntityId` assignment for player characters (it does not assign the player's, but it must read it) | `NOT RECEIVED` |
| 4 | Which of the requested tags collide with A2's own naming plans | `NOT RECEIVED` |

### 7.8 Unresolved alternatives (C-07)

1. **Typed id wrappers** (`FTDDEntityId`, `FTDDRouteId` strong types) vs raw `FGuid`/`FName`. Strong types prevent accidental mixing — the exact bug class §7.2 describes — at the cost of boilerplate. Agent 1 leans toward strong types for entity ids and raw `FName` for authored ids. Agent 3's call.
2. **Tag naming for capabilities** — `Traversal.Capability.*` (proposed) vs folding them into `Ability.*`. Naming is Agent 3's; Agent 1 needs only that they exist and are stable.
3. **Retirement policy** — tombstones with explicit `Retired` status (proposed) vs hard deletion (rejected: breaks saves silently).
4. **Whether `Status.Traversing`/`Status.Interacting` are needed at all**, given Agent 2 could read C-02's `ControlState`. Tags are cheaper for AI conditions and survive without an interface dependency; if A2 confirms it only reads C-02, these two can be dropped.

---

## 8. Cross-contract position, conflicts and issues for Technical Director resolution

### 8.1 One conflict identified in an existing document (not a disagreement with a TD decision)

**Where:** MEAD `TDD-MEAD-001` §5.4 draws the damage pipeline as *attacker-driven*: `Attacker CombatComponent → FTDDDamageRequest → ITDDDamageable::ApplyDamage → victim's UTDDCombatComponent → …`. The TD integration decision states that **Agent 1 owns hit arbitration and damage application**.

**Why it is a tension:** for player-as-attacker both readings agree — A1 *is* the attacker's combat component, so A1 resolves and applies. For **enemy-as-attacker**, MEAD as written has the enemy's combat component run the pipeline and call into the victim's component, while the integration decision requires A1 to arbitrate hits against the player. If both are implemented literally, there are two arbitration code paths and the "one hit → one application → one event" guarantee becomes a coordination problem instead of a structural one.

**Agent 1's reading (proposed, not asserted):** A2's enemy emits a **request**; A1's `UTDDPlayerDamageAuthority` performs validation and arbitration; the player's attributes are written by A1 only; A2 never evaluates block/parry against the player. In both readings the *player's health* is written by A1 — the unresolved question is **who runs the arbitration branch for incoming hits**, and it changes where block/parry logic lives.

**Options:**

| Option | Description | Consequence |
|---|---|---|
| **1 (A1-preferred)** | A1 arbitrates all hits involving the player; A2 submits requests | One authority, one event stream, one place for defence logic. Requires A2 to accept a submit-and-wait result |
| **2 (MEAD-literal)** | Attacker arbitrates; A1 provides the player's defence evaluation as a callable service | Keeps MEAD §5.4 unchanged but splits arbitration across modules |
| **3** | Symmetric: each side arbitrates hits against its own actors | Cleanest ownership, but the player's defence rules then live in A2's calling code |

**This needs a TD ruling (TD-09).** Agent 1 has not quietly implemented either reading — no code exists.

### 8.2 Issues requiring Technical Director resolution

| ID | Issue | Why it blocks agreement | Agent 1's recommendation |
|---|---|---|---|
| **TD-01** | **Which integration addendum governs?** The request names `TDD-TD-INT-001` **v1.2**; only **v1.1** exists at the packet commit and on `main` (§0.2) | If v1.2 changes scope, this submission is based on the wrong document | Confirm v1.1 is current, or publish v1.2 and name the delta |
| **TD-02** | **C-04 classification representation** — `bCausesStagger` vs `ETDDStaggerClass` vs damage-tag mapping vs GAS effect (§4.2) | A1 needs one resolved value; the storage choice is Core's | **B** (`ETDDStaggerClass`); **A** acceptable; **D** rejected (inverts the accepted ordering) |
| **TD-03** | **C-03 applied-event scope** — do blocked/parried/posture-only hits publish `FTDDDamageAppliedEvent`? Is `Amount` clamped or raw? Who publishes for A2-owned targets? (§3.6, §3.9) | Every subscriber must handle the same cases; ambiguity here produces inconsistent AI reactions | Publish for Blocked/Parried with `Amount` 0; clamped `Amount`; **one** publisher (A1) for all hits |
| **TD-04** | **C-01 `RouteId` format and stability** — and whether narrative/saves may reference routes | Determines retirement policy and how much validation is required | Format `TRV.<CH>.<SCN>.<NNN>`, opaque to code, no save references in the slice |
| **TD-05** | **C-02 stealth/noise exclusion** — no approved stealth design exists | Adding the field would be speculative; omitting it may block an A2 need | **Omit** until a named A2 consumer exists; revisit as a C-02 revision |
| **TD-06** | **C-05 canonical gameplay clock** — Core subsystem vs per-module accumulators | Two clocks across modules = windows that disagree by frames; hitstop makes it worse | **Core** `UTDDGameplayTimeSubsystem`, Agent 3 owned |
| **TD-07** | **C-06 hold-progress authority** — router (proposed) vs interactable | Determines where the hold-duration bug class lives | **Router** owns progress; the interactable consumes `Progress01` |
| **TD-08** | **C-07 tag approval and retirement policy** — the requested namespaces, and whether strong id types are used | Tag names are permanent compatibility surface once content exists | Approve `Traversal.Capability.*`, `Interact.Verb.*`, the four `Status.*` additions; tombstone retirement |
| **TD-09** | **§8.1 conflict** — who arbitrates hits where the player is the victim | Two authorities would break exactly-once | **Option 1**: A1 arbitrates all hits involving the player |

**No issue above has been resolved by assumption.** Where Agent 1 had to state a position to make the submission concrete, it is marked "proposed" and listed here.

### 8.3 What Agent 1 is explicitly *not* asking for

- No new Core type authored by Agent 1, no registry, no event bus, no alternative to `ITDDDamageable`/`ITDDInteractable`.
- No change to M1 v1.4 semantics, to AC-01…AC-31, or to any accepted threshold.
- No expansion of scope beyond the vertical slice's traversal set, one player, single-player networking model.
- No permission to implement: this is a design submission and the gate for code remains B-1…B-6 plus TD authorisation.

---

## 9. Producer/consumer sign-off (as required by packet §5)

| Contract | Agent 1 sign-off (producer/executable owner) | Required Agent 2 counterpart | Agent 2 sign-off on **this exact version** | TD decision |
|---|---|---|---|---|
| C-01 | `SUBMITTED — A1-R1` | World marker/route authoring | `NOT RECEIVED` | `PENDING` |
| C-02 | `SUBMITTED — A1-R1` | Read-only snapshot consumer | `NOT RECEIVED` | `PENDING` |
| C-03 | `SUBMITTED — A1-R1` | Damage/poise event consumer | `NOT RECEIVED` | `PENDING` |
| C-04 | `SUBMITTED — A1-R1` (representation `REQUEST_TD_DECISION`) | Combat-state consumer | `NOT RECEIVED` | `PENDING` |
| C-05 | `SUBMITTED — A1-R1` | **Telegraph producer** | `NOT RECEIVED` | `PENDING` |
| C-06 | `SUBMITTED — A1-R1` | Interactable implementation | `NOT RECEIVED` | `PENDING` |
| C-07 | `SUBMITTED — A1-R1` | World ID/tag consumer and requester | `NOT RECEIVED` | `PENDING` |

**Nothing in this table is agreed.** No row may be marked agreed until Agent 2 reviews `A1-R1` and both sides state agreement on the same version; where they differ, the disagreement is retained here rather than smoothed over.

## 10. Submission metadata and provenance

| Field | Value |
|---|---|
| Branch | `arena/3bc206a0-tdd` (Agent 1's existing branch; no new branch, no merge) |
| Source basis commits | `bb2685c605efd4958b1c67944721c77e1b393931` — M1 spec v1.4, assessment v1.4, ADR-0013 v1.4. This document's own publishing commit: `09769de05975882df8ec1581317bc3fd54ddcae7` on `origin/arena/3bc206a0-tdd` |
| Packet source commit | `50b14318c8089dedcc688fb2c78ad3cb361c15f5` |
| Governing addendum read | `TDD-TD-INT-001` **v1.1** (v1.2 absent — TD-01) |
| Document status | `DESIGN_ONLY`; contract proposals `PROPOSED — NOT FROZEN`; tests `PROPOSED / NOT RUN` |
| Prior Agent 1 versions preserved | M1 spec v1.0–v1.3 and assessment v1.0–v1.3 in `docs/02_PRODUCTION/AGENT1/archive/`; ADR-0013 v1.0–v1.3 in `docs/03_DECISIONS/archive/`. This document adds no new version of those; it is a new contract-response document |
| Code, Core types, project, build, tests | **None created, none run.** `Source/` remains empty; no `.uproject` exists |
| Merge | None performed; no branch other than Agent 1's was touched |

### 10.1 Change log

| Version | Date | Change |
|---|---|---|
| 1.0 (`A1-R1`) | 2026-11-16 | Initial Agent 1 response to `TDD-A1-CONTRACT-PACKET-001` for C-01…C-07: per-contract 12-field record, proposed shapes (labelled), ownership and mutation authority, lifetime and failure semantics, named acceptance tests (`PROPOSED / NOT RUN`), Agent 2 dependencies, nine issues for TD resolution, and the §8.1 conflict against MEAD §5.4 |
