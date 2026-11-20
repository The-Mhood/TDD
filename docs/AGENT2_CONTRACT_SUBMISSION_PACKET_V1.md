# Agent 2 Submission Packet — World/Authored Side of Shared Contracts

**Packet ID:** `TDD-A2-CONTRACT-PACKET-001` · **Version:** 1.0
**Date:** 2026-11-16 UTC
**Recipient:** Agent 2 — World, Systems and Gameplay Simulation
**Prepared by:** Agent 3 — Integration / Technical Quality
**Related governing addendum:** [`TDD-TD-INT-001 v1.1`](TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_1.md)
**Status:** `PREPARED — AWAITING AGENT 2 SUBMISSION`; this file is a request/template, not an Agent 2 response or an accepted interface.

## 1. Purpose and boundary

Submit Agent 2's **actual world-side requirements** for C-01 through C-07: what Agent 2 will author, produce, query or consume in world data/systems, with the smallest useful cross-agent surface. Use exact register IDs and source versions where the requirement concerns authored material. Preserve all previous Agent 2 documents and versions.

Agent 2 owns authored traversal opportunities/world requirements and world interactable implementations. Agent 1 owns player state mutation, traversal execution, hit arbitration/damage application and player-side interaction routing. Agent 3/TD owns shared Core publication/governance. Agent 2 must not create competing Core IDs/events/interfaces, write player state through a façade, apply damage independently, or claim runtime behavior from register/Python checks.

These packets are prepared for submission; they do not establish that an agent was contacted or agreed. A consolidated contract is sent to the TD only after Agent 1 and Agent 2 have reviewed and agreed to the same version. Record every disagreement rather than smoothing it over.

## 2. Required response format — every C-01…C-07

Complete every row for **each** contract. For fields outside Agent 2 authority, state the requested boundary and leave the decision to its owner instead of inventing it.

| Required field | Agent 2 response |
|---|---|
| Contract ID and proposal version | `TO BE COMPLETED BY AGENT 2` |
| Publisher (Core contract authority) | `Agent 3/TD` unless requesting a documented exception; explain any exception |
| Implementation owner(s) | Name world producer/consumer implementation owner(s) |
| Producers | Name actual world actors/data/directors that publish or produce this contract/event |
| Consumers (named) | Name player-side and other consuming systems explicitly |
| Actual world-side requirements | Required authored data, queries, output events, failure response and validation behavior; justify each field/use |
| Lifetime and validity | Chapter/scene/streaming scope; unload/destruction, stale IDs, data version and temporal rules as applicable |
| Mutation authority | Which Agent 2 world data/state can be changed by which subsystem; explicitly state what Agent 2 must not mutate (player state, damage authority, persistent progress) |
| Proposal status | `DRAFT` / `UNDER_REVIEW` / `AGREED_WITH_CONSUMERS` / `REQUEST_TD_DECISION`; list unresolved alternatives |
| Acceptance tests | Stable named candidate test IDs, test layer, setup, measurable assertions; distinguish proposed tests from tests that exist or ran |
| Agent 1 producer/consumer agreement | `NOT RECEIVED` until Agent 1 reviews the exact same version; quote their response or record disagreement |
| Agent 3/TD decision | Leave blank until recorded by Agent 3/TD |

## 3. Per-contract requests to Agent 2

### C-01 — World-authored traversal opportunities and requirements

Specify the actual world-side schema and behavior needed by authored traversal content:

- Stable route/opportunity ID requirements and exact ID source/version; distinguish route IDs from location, scene, actor and entity IDs.
- Marker representation (actor, data asset, or authored data record), required transforms/anchors, entry/exit metadata, capabilities/tags, chapter/scene association and streaming lifetime.
- World requirement representation: tags/data/registry references/code query or alternatives; explain authoring and validation consequences.
- How world data expresses gated/unavailable route, one-way traversal, destination/reachability hints or invalid content, if those are actual needs.
- Exact query fields Agent 2 requires from Agent 1; do not request write access to player state or dictate Agent 1's execution internals.
- Desired behavior when marker/route is missing, unsupported by the player, blocked, invalid or streamed out; distinguish authoring validator output from runtime query output.
- Acceptance tests for route-ID resolution, marker load/unload, requirement matching, invalid references, offline reachability and runtime-unavailable data.

Do not settle the action enum on Agent 1's behalf. M1 v1.4 fallback/hold behavior is preserved and is not an Agent 2-controlled world placement behavior.

### C-02 — Actual read-only player information needed by world systems

Specify the minimal fields Agent 2 genuinely consumes:

- For each field (position, facing, locomotion, action/control, combat status, target, stealth/noise or other), name the world consumer and decision it enables. Remove fields with no concrete use case.
- Required units, coordinate frame, update rate/freshness, event-vs-query preference and tolerance for missing/stale player context.
- Distinguish AI/perception use from traversal/interaction gating; avoid asking one snapshot to combine independent state taxonomies.
- Confirm the Agent 2 side only reads this data and how world behavior reacts to invalid/despawned/unpossessed player context.
- Acceptance tests for actual consumer decisions, missing/stale context, no writes and event/snapshot consistency.

### C-03 — Damage/hit/applied-event consumers and world outputs

Specify what world enemies/bosses need to know from Agent 1's single authority pipeline:

- What actual reactions require hit outcome, damage amount/type, posture break, lethal, source/target identity or hit location; justify each independently.
- Whether world systems need a local ephemeral event or a durable actor-free Core event; state how the world consumer behaves if source actor unloads/dies.
- If Agent 2 creates enemy attack intent, state how it submits intent to Agent 1's hit/damage path without applying health damage or duplicating hit arbitration.
- Event ordering, deduplication and lifetime requirements; do not read/write health directly outside the accepted authority.
- Acceptance tests for exactly-once enemy reaction, stable IDs, actor/world unload and no duplicate damage application.

### C-04 — Stagger and forced-state outcome consumer

Specify what the world must observe, not an independent way to classify the player's stagger:

- Which resulting state/event or status Agent 2 needs for enemy AI, encounter response, attack scheduling, ambient reactions or interaction eligibility. Cite actual consumers.
- What happens on Dead, Cinematic or Stagger in world systems; distinguish display/AI behavior from player transition authority.
- Confirm world systems do not override Agent 1's classification or precedence. Required forced precedence is **Dead (100) > Cinematic (90) > Stagger (80)**.
- Acceptance tests for world reaction to each published outcome and simultaneous/superseded events; no second state authority.

### C-05 — Enemy telegraph producer and timing lifecycle

Specify the actual world/enemy producer side:

- Which world systems produce an attack telegraph and which source is authoritative for its start, update, close and cancellation.
- Stable attack/window/source identity, target or area representation, time units, sequence/order, gameplay pause/time dilation, level streaming and actor cancellation semantics.
- How the telegraph relates to enemy AI intent, active damage window and later hit result. It must not itself apply damage.
- What data Agent 1's parry/block consumer must observe and what is optional vs required.
- Acceptance tests for exact start/end, cancellation on interrupted attack/death/unload, pause behavior, reused IDs, late consumers and producer/consumer clock consistency.

### C-06 — World-side `ITDDInteractable` implementation

Specify the world actor/content side of one Core-owned lifecycle:

- Actual world interactable categories and the minimum methods/data needed for prompt, eligibility, verb, requirements, location association, action response and completion.
- Tap vs hold needs per category; clarify whether the world object consumes progress updates or only receives begin/end/cancel. Do not assign player input/progress timing authority without Agent 1 agreement.
- Cancellation and validity when actor/world streams out, requirements change or the player loses focus.
- Completion fact/event needed by audio/telemetry/memory/quest consumers; distinguish the interaction fact from a persistent progression grant. World interactables do not directly grant persistent memory/quest state unless the accepted architecture explicitly assigns that authority.
- Acceptance tests for eligibility, prompt/verb, tap/hold, cancel/unload, exactly-once completion and no direct progress grant.

### C-07 — World IDs and Gameplay Tags needed by Agent 2

Provide exact authored-world data requirements:

- ID inventory for locations, scenes, route opportunities, interactables, memories, chapters, actors/entities and persistence links; name source register/document/version for each.
- Identify which IDs are stable content keys, runtime entity identities, transient actor names or display labels; never conflate them.
- Tag inventory with feature, authoring use, consumer and whether it already exists vs requested. Agent 3/TD owns registry publication and tag namespace governance.
- Retired/missing ID behavior, version migration and validation needed for authored data.
- Acceptance tests for source traceability, duplicate/unknown/retired ID detection, tag registry completeness and world streaming reference validity.

## 4. Proposed test naming (candidate identifiers only)

These names are prompts for Agent 2 to confirm, replace or extend; they do **not** assert the tests exist or passed:

- `TDD-Contract.World.TraversalRouteIdsAndMarkerValidation`
- `TDD-Contract.World.PlayerContextConsumersAreReadOnly`
- `TDD-Contract.World.DamageEventReactionAndIdentity`
- `TDD-Contract.World.ForcedStateEventConsumption`
- `TDD-Contract.World.TelegraphProducerLifecycle`
- `TDD-Contract.World.InteractableLifecycleAndProgressBoundary`
- `TDD-Contract.World.IdAndTagRegistryValidation`

For each accepted test, name the layer (pure/unit, Unreal automation, functional/map, or data validation), fixture/data version, measurable assertions and evidence type. Python/register tests remain data/document validation, not UE runtime evidence.

## 5. Producer/consumer sign-off

| Contract | Agent 2 sign-off (world producer/implementation owner) | Required Agent 1 executable/player-side counterpart | Agent 1 sign-off on same version | TD decision |
|---|---|---|---|---|
| C-01 | `PENDING` | Agent 1 traversal query/execution | `NOT RECEIVED` | `PENDING` |
| C-02 | `PENDING` | Agent 1 player-context/state provider | `NOT RECEIVED` | `PENDING` |
| C-03 | `PENDING` | Agent 1 hit arbitration/damage application | `NOT RECEIVED` | `PENDING` |
| C-04 | `PENDING` | Agent 1 stagger/state authority | `NOT RECEIVED` | `PENDING` |
| C-05 | `PENDING` | Agent 1 parry/block consumer | `NOT RECEIVED` | `PENDING` |
| C-06 | `PENDING` | Agent 1 player interaction router | `NOT RECEIVED` | `PENDING` |
| C-07 | `PENDING` | Agent 1 tag/ID consumer/requester | `NOT RECEIVED` | `PENDING` |

**Do not mark a row agreed** until both sides explicitly sign the same proposal version. Record each disagreement and affected downstream blocker in the C-01…C-10 register; submit a consolidated contract to the TD only after producer and consumer agreement.
