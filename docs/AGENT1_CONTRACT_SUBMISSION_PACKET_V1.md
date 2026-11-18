# Agent 1 Submission Packet — Player/Executable Side of Shared Contracts

**Packet ID:** `TDD-A1-CONTRACT-PACKET-001` · **Version:** 1.0
**Date:** 2026-11-16 UTC
**Recipient:** Agent 1 — Gameplay, Character and Combat Engineering
**Prepared by:** Agent 3 — Integration / Technical Quality
**Related governing addendum:** [`TDD-TD-INT-001 v1.1`](TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_1.md)
**Status:** `PREPARED — AWAITING AGENT 1 SUBMISSION`; this file is a request/template, not an Agent 1 response or an accepted interface.

## 1. Purpose and boundary

Submit Agent 1's **actual executable/player-side requirements** for C-01 through C-07. Work from Agent 1 M1 Movement Specification v1.4 and the TD decisions; preserve prior specification versions. Do not create Core types, implementation code or competing APIs in response to this packet.

Agent 1 remains owner of player state mutation, traversal execution, hit arbitration/damage application and player-side interaction routing. Agent 3/TD publishes shared Core contracts. Agent 2 must separately state its actual world-side requirements. A consolidated contract is not sent for TD acceptance until both producer and consumer positions are recorded and agree on the same version. Record any disagreement explicitly; do not silently choose Agent 1's proposal as cross-agent agreement.

## 2. Required response format — every C-01…C-07

Complete this record for **each** contract. Do not leave implied ownership or lifetime unstated.

| Required field | Agent 1 response |
|---|---|
| Contract ID and proposal version | `TO BE COMPLETED BY AGENT 1` |
| Publisher (Core contract authority) | `Agent 3/TD` unless requesting a documented exception; explain any exception |
| Implementation owner(s) | Name the runtime owner(s), not only the contract publisher |
| Producers | List concrete Agent 1 components/systems that publish or produce this contract/event |
| Consumers (named) | List concrete consumers and whether Agent 1 produces, consumes or both |
| Executable/player-side requirements | Required operations, inputs/outputs, authoritative state, and what must not be mutated by consumers |
| Lifetime and validity | Player/world/streaming scope; stale/invalid handles; timing, ordering and cancellation as applicable |
| Mutation authority | Exact owner for player/capsule/combat/interaction state writes; identify read-only surfaces |
| Proposal status | `DRAFT` / `UNDER_REVIEW` / `AGREED_WITH_CONSUMERS` / `REQUEST_TD_DECISION`; list unresolved alternatives |
| Acceptance tests | Stable named candidate test IDs, test layer, setup, measurable pass/fail assertions; distinguish proposed tests from tests that exist or ran |
| Agent 2 consumer agreement | `NOT RECEIVED` until Agent 2's named owner reviews the exact same version; quote their response or record disagreement |
| Agent 3/TD decision | Leave blank until recorded by Agent 3/TD |

## 3. Per-contract requests to Agent 1

### C-01 — Traversal vocabulary, query and result

Specify the executable/player-side traversal surface:

- Candidate action/capability vocabulary and clear behavior definition for each action.
- Data needed to decide whether an action is executable (player state, movement mode, geometry/clearance, tags, route requirements).
- Query inputs, deterministic selection policy, query outputs and candidate validity/expiry/revalidation rules.
- Distinct outcomes for no candidate, unsupported action, invalid authored data, blocked route, streaming/unavailable world, and execution failure; define which outcomes produce no prompt vs diagnostic.
- Player-side interruption, abort and failure behavior, including when a result is a request versus a forced transition.
- Expected world-authored marker fields; do not prescribe Agent 2 marker choices without agreement.
- Stable route identity needs and whether the player component consumes ID/tag/data/code requirements.
- Acceptance tests for query determinism, invalid route data, revalidation, unsupported result and interruption paths.

**Non-negotiable design preservation:** M1 v1.4's fallback/hold behavior is not being redesigned by C-01. Keep its bounded relocation loop, always-run terminal hold, validation-at-write, restoration ordering and out-of-world flow handoff intact.

### C-02 — Read-only player context and state snapshots

Specify what Agent 2 actually needs to read and how Agent 1 can publish it safely:

- Minimal fields for position, facing, locomotion, action/control, combat status, target/interaction target, and any proposed stealth/noise data. Justify every field by a concrete Agent 2 consumer.
- Keep locomotion, action/control and combat status distinct; name each snapshot and authoritative source.
- Units, coordinate frame, update cadence, consistency point, event/delegate versus snapshot query, and null/invalid player/world behavior.
- Any actor references must be weak/short-lived with explicit validity rules; prefer stable values for cross-module events.
- Confirm consumers cannot mutate through the context. Identify how Agent 1 controls all player-state mutation.
- Acceptance tests for read-only behavior, lifecycle invalidation, field units, event order and unchanged-state notification policy.

### C-03 — Damage request, local resolution, application and applied event

Specify Agent 1's single hit/damage path, without choosing Core publication details on behalf of Agent 3:

- Request inputs, attacker/target identity needs, attack/source identity, damage type/amount and validation.
- Separation between request, local hit-resolution result and confirmed applied-damage event; list result semantics and exactly when health/posture changes.
- One hit arbitration/application authority and duplicate/replay behavior; ensure enemy intent cannot bypass Agent 1's damage authority.
- Local transient actor reference needs versus stable identity/value needs for Core events consumed after actor destruction/world transitions.
- When and how Agent 2 enemy/boss systems should react to damage/poise without reading or writing health directly.
- Acceptance tests for one hit → one application → one applied event, invalid targets, lethal boundary, immunity/block paths, duplicate prevention and stale actor lifetime.

### C-04 — Stagger classification, precedence and control outcome

Specify player-side classification semantics and the executable response. Do not require `FTDDDamageRequest::bCausesStagger` as a permanent Core field.

- State how stagger classification may be represented (field/tag/damage-data/effect/other) and offer alternatives with consequences; Agent 3/TD chooses the Core representation.
- Preserve exact forced-target precedence: **Dead (100) > Cinematic (90) > Stagger (80)**.
- Preserve M1 behavior: lethal damage forces Dead; cinematic takeover skips positional fallback and freezes; staggering damage/posture break/successful parry forces Stagger after fallback/restoration; health application is independent of control.
- Non-staggering damage is an abort request only inside `AbortWindow`; outside it traversal continues and health damage still applies.
- Define promotion when posture breaks in the same frame, pending forced-event queuing, and event/result publication order.
- Acceptance tests for pairwise and simultaneous precedence, posture/parry promotion, damage inside/outside the window, cinematic-vs-stagger, lethal-and-stagger, and health/state independence.

### C-05 — Telegraph timing and parry/block consumption

Specify the player combat consumer contract and producer needs Agent 2 must meet:

- Required start/update/close/cancel messages and attack/window identity, source identity, target/area representation and ordering.
- Clock/unit for windup, active and recovery; pause, time dilation, world pause/unload, late subscription and missed-window behavior.
- How a parry/block consumer uses the stream, how much timing precision it needs, and how telegraph cancellation affects a buffered/active defense.
- Clarify telegraph/intent versus actual hit resolution; telegraphs never apply damage or arbitrate a hit.
- Acceptance tests with deterministic clock, open/close boundary, pause/resume, cancellation, duplicate/stale identity and parry timing.

### C-06 — Player-side interaction routing/lifecycle

Specify the player router's needs for one Core-owned lifecycle:

- Focus selection and eligibility query, prompt display inputs, verb-to-animation/action mapping, tap vs hold initiation.
- Whether player input/router owns hold duration/progress and exactly when it calls progress/end/cancel.
- Cancellation reasons and ordering for movement, damage, stagger, death, cinematic, target loss and streaming unload.
- How the router receives exactly-once completion/failure and how interaction stays separate from persistent memory/quest grants.
- Context/target lifetime and behavior if the world interactable disappears mid-action.
- Acceptance tests for focus/eligibility, tap, hold progress, early cancel, forced transition, unload, duplicate begin/completion and verb registration.

### C-07 — IDs and Gameplay Tags needed by Agent 1

Provide a concrete inventory, not a new independent registry:

- Player/combat/traversal identity needs, distinguishing entity identity from authored route/content IDs.
- Tag namespaces/individual tags required by an identified feature, producer and consumer; mark existing vs requested.
- Any persistence/network/world-lifetime requirements, invalid/default policy and compatibility concern.
- Which IDs are only local transient data and which must remain stable across actors, levels, saves or events.
- Acceptance tests for registered tags, duplicate/unknown/retired ID rejection and value event behavior after actor destruction.

## 4. Proposed test naming (candidate identifiers only)

These names are prompts for Agent 1 to confirm, replace or extend; they do **not** assert that tests have been written or executed:

- `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics`
- `TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation`
- `TDD-Contract.Combat.SingleDamageApplicationAndEvent`
- `TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification`
- `TDD-Contract.Combat.TelegraphWindowConsumerSemantics`
- `TDD-Contract.Interaction.PlayerRoutingAndCancellation`
- `TDD-Contract.Core.Agent1IdAndTagRegistry`
- Retain M1 v1.4 named fallback/abort test plans; do not weaken or replace them with a generic contract test.

For each accepted candidate, name automation layer and give assertions. All are `PROPOSED / NOT RUN` until implemented in the authorized Unreal project and backed by actual reports.

## 5. Producer/consumer sign-off

| Contract | Agent 1 sign-off (producer/executable owner) | Required Agent 2 consumer/producer counterpart | Agent 2 sign-off on same version | TD decision |
|---|---|---|---|---|
| C-01 | `PENDING` | Agent 2 world marker/route authoring | `NOT RECEIVED` | `PENDING` |
| C-02 | `PENDING` | Agent 2 read-only snapshot consumer | `NOT RECEIVED` | `PENDING` |
| C-03 | `PENDING` | Agent 2 damage/poise event consumer | `NOT RECEIVED` | `PENDING` |
| C-04 | `PENDING` | Agent 2 combat-state consumer | `NOT RECEIVED` | `PENDING` |
| C-05 | `PENDING` | Agent 2 telegraph producer | `NOT RECEIVED` | `PENDING` |
| C-06 | `PENDING` | Agent 2 interactable implementation | `NOT RECEIVED` | `PENDING` |
| C-07 | `PENDING` | Agent 2 world ID/tag consumer/requester | `NOT RECEIVED` | `PENDING` |

**Do not mark a row agreed** until both sides explicitly sign the same proposal version. Any mismatch must be retained as an explicit unresolved entry in the v1.1 C-register before TD review.
