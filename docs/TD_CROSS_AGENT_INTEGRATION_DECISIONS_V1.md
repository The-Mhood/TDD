# Technical Director Addendum — Cross-Agent Integration Decisions and Core Contract Plan

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Document:** `TDD-TD-INT-001`
**Version:** 1.0
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Decision authority:** Technical Director
**Branch:** `arena/c64fc525-tdd`
**Status:** TD decisions A1–A8 and module topology in §2 are **ACCEPTED / GOVERNING** as supplied in the 2026-11-16 TD instruction. Contract semantics below are the consolidated **proposal for compatible Agent 1 / Agent 2 submissions**, not a frozen C++ API. Environment/version recommendation and outstanding decisions are in §4 and §8.
**History:** New versioned addendum. It supplements, and does not rewrite, the original Agent 1/Agent 2 documents or `docs/AGENT1_AGENT2_INTERFACE_REVIEW.md`.

## 1. Purpose, authority and guardrails

This addendum records the TD's accepted boundaries, specifies the minimum information required for the shared Core contract package, establishes the four-module dependency direction, and gives a dependency-ordered M0 preparation path. It does not import, copy, modify or accept Agent 2's project skeleton. It does not create an Unreal project, implement gameplay, freeze a specific C++ signature, or claim engine/runtime verification.

This is the current governing integration record. The earlier [Agent 1 / Agent 2 interface review](AGENT1_AGENT2_INTERFACE_REVIEW.md) remains unchanged as historical analysis; this addendum supersedes its list of requested TD decisions where §2 records an accepted outcome. The existing [M0 evidence checklist](M0_UNREAL_FOUNDATION_CHECKLIST.md) remains the detailed evidence standard; this addendum does not authorize its execution.

The canonical repository remains TDD. Agent 3/TD publishes and governs shared Core contracts. Agent 1 owns player state mutation, traversal execution, hit arbitration and damage application, plus player-side interaction routing. Agent 2 owns authored traversal opportunities/world requirements and world interactable implementations. Consumers receive read-only player information. Preserve Agent 1 M1 v1.4's accepted fallback/hold behavior as specified; any change must be explicit and versioned.

**Project creation and Unreal work remain unauthorized by this documentation task.** M0 is a preparation target; actual project bootstrap requires the separately recorded M0 entry authorization and access to the selected toolchain.

## 2. Accepted TD decisions

| Decision | Governing direction | Consequence |
|---|---|---|
| Canonical project | TDD remains canonical; Agent 2's project skeleton is not adopted. | No copying or merging the Agent 2 branch's `.uproject`, source, config, targets or modules. |
| Shared contracts | Agent 3/TD owns Core contract publication and governance. | No agent independently defines competing shared IDs, tags, event structs or interfaces. Contract changes require review and recorded acceptance. |
| Player state | Locomotion, action/control and combat status are separate concepts. Agent 1 owns player state mutation; Agent 2 receives read-only state. | No one mega-enum or competing state authority. Snapshot fields and lifetimes remain to be proposed. |
| Traversal | Agent 1 owns traversal execution; Agent 2 owns authored traversal opportunities and world requirements. | Marker/schema/query handshake must be jointly proposed; Agent 2 does not execute player traversal. |
| Damage | Agent 1 owns hit arbitration and damage application; shared events belong to Core. | One damage-application path; Agent 2 consumes results/events and does not duplicate damage. |
| Interaction | One Core-owned lifecycle. Agent 1 owns player-side routing; Agent 2 owns world interactables. | One cross-agent signature/lifecycle after proposal review; no competing `ITDDInteractable` variants. |
| Movement interruptions | Preserve Agent 1 M1 v1.4 fallback/hold design. | The bounded relocation budget plus terminal hold resolution and precedence/restoration semantics remain the design baseline. This is not evidence of implementation or runtime validation. |
| M0 gate | Real Unreal project, successful build, meaningful project-owned Unreal Automation Test and captured evidence. | Documentation/Python checks cannot pass M0; no runtime claim without the evidence bundle. |
| Initial modules | `TDDCore`, `TDDRuntime`, `TDDEditor`, `TDDTests`. | Core remains independent of gameplay/world. Add downstream modules only when actual dependency boundaries justify them. |

## 3. Consolidated Core contract specification — proposal for owner submissions

### 3.1 Contract status and required fields

The rows below define the **contract requirements and proposal ownership** to align Agent 1 and Agent 2. They are not source declarations and do not choose a permanent field layout where the agents must still supply options. For each submitted contract, Agent 1/2 must state: **publisher; implementation owner; consumers; lifetime; mutation authority; status; acceptance tests**. Agent 3/TD reviews the delta and records accepted version/status before consumers implement against it.

“Core-owned” means the stable public contract/event/value schema is published and versioned from `TDDCore`; it does not automatically mean all runtime behavior or producer logic belongs in Core.

### 3.2 Shared ID and Gameplay Tag policy

| Item | Proposed rule | Publisher / implementation | Consumers / lifetime / authority | Status and acceptance evidence |
|---|---|---|---|---|
| Stable entity identity | Core publishes one entity identity contract for cross-module/event references. Choose whether identity is a GUID, registered typed ID, or another stable value; define creation, persistence, invalid/default values, actor association, and reuse semantics. Do not substitute raw actor pointers for cross-module durable identity. | Publisher: Agent 3/TD. Runtime allocation/association owner: to be nominated per entity domain. | Agent 1 and Agent 2 producers/consumers; event lifetime may outlast an actor/world. Only designated identity authority creates/changes identity. | Proposed; exact representation open. Tests: uniqueness within declared scope; serialization/round-trip if persistent; stale actor destruction does not invalidate value event; invalid IDs rejected. |
| Domain IDs (location, memory, route, interactable, chapter/scene) | Define typed wrappers or a documented registered-ID vocabulary per domain; no inconsistent implicit conversion between FName, FGuid and tag. Route IDs are needed for authored traversal reachability. | Core publishes shared ID rules; domain owner (Agent 2 for authored world IDs) proposes registry/schema. | World data and validation; memory/progression; traversal consumer. Data IDs persist as long as authored/save references require. World authoring mutates content IDs only through registered-data review. | Proposed; route ID and canonical entity policy pending. Tests: duplicate/unknown/retired ID validation; stable references across parse/load. |
| Gameplay Tags | One Core-owned registry/configuration and namespace/change review. Feature agents request tags with a consumer/purpose; no private duplicate tag hierarchy. | Publisher: Agent 3/TD; feature owners request and consume. | Agents 1/2 and systems using tags. Registry lifetime is project-wide; only approved tag change process mutates it. | Accepted ownership; exact initial vocabulary pending agent proposals. Tests: all used tags registered; no accidental namespace/typo; requested ownership/purpose traceable. |

### 3.3 Player context and state snapshots

| Contract | Publisher / implementation owner | Consumers | Lifetime and mutation authority | Proposal status | Acceptance tests to include |
|---|---|---|---|---|---|
| Read-only player context | Agent 1 proposes fields/API; Agent 3/TD publishes stable cross-module contract. Agent 1 implements provider. | Agent 2 world, encounter/perception and interactables; other approved consumers. | Snapshot/view valid for documented player/world lifetime; any weak actor handles must have null/lifetime rules. Agent 1 alone mutates authoritative player state; consumers cannot write through the façade. | Required; compatible proposal not yet received. | Consumer cannot mutate; invalid player/world lifetime handled safely; each published field has units/coordinate frame/update cadence; snapshot consistency and null-player tests. |
| Locomotion snapshot/event | Agent 1 proposes and implements; Core event/schema published by Agent 3/TD. | Agent 2 NPC/audio/AI reaction; UI or other approved consumers. | Value snapshot/event; authoritative state changes only in Agent 1. Define dispatch order and whether event is synchronous/asynchronous. | Required; unresolved names/fields/delegate shape. | State change publishes once, old/new are consistent, no polling required, no stale actor pointer, no event for unchanged value unless explicitly specified. |
| Action/control snapshot | Agent 1 proposes and implements; Core type published by Agent 3/TD. | Agent 2 eligibility/traversal/interaction gating; other consumers by approval. | Distinct from locomotion and combat status; player mutation only by Agent 1. Define transition reason and invalid/unknown state behavior. | Required; action vocabulary/transition schema open. | Valid transitions; prohibited transitions rejected; consumer sees consistent snapshot; interruption/terminal state cases covered. |
| Combat-status snapshot | Agent 1 proposes and implements; Core type/event published by Agent 3/TD. | Agent 2 enemy/encounter response; other consumers. | Separate from action/control and locomotion; Agent 1 is player authority. | Required; do not reuse the old single state enum by assumption. | Combat state transition notification, separation from locomotion, no duplicate authority, combat exit/death cases. |

Agent 1 and Agent 2 must reconcile position, facing, locomotion/action/combat state, target/interaction target, and any stealth/noise values. Each field needs a consumer and authority rationale; do not add fields solely because a prior proposal mentioned them.

### 3.4 Traversal opportunity, query and result

| Contract element | Required proposal content | Publisher / implementation owner | Consumers / lifetime / mutation | Status / acceptance tests |
|---|---|---|---|---|
| Action vocabulary | Stable capability/action names and meanings; map authored route needs to executable actions; mark deprecated/unsupported actions and compatibility policy. | Agent 1 proposes execution vocabulary; Agent 2 confirms authoring needs; Agent 3 publishes shared contract. Agent 1 implements execution. | Agent 2 authors requirements; Agent 1 reads and executes. Vocabulary versioned; only Agent 1/TD-approved contract changes. | Not agreed. Test each action's supported/unsupported classification and unknown-action failure. |
| Route IDs and route requirements | Stable route/opportunity identifier form; whether requirements are tags, IDs, data records, code query or a constrained combination; chapter/scene association and validation behavior. | Agent 2 proposes authored data/schema; Agent 1 validates executable capability; Agent 3 owns shared ID contract. | Authored content survives load/validation; Agent 2 changes world data, not player state. | Not agreed; route IDs remain provisional. Tests: registered IDs, missing refs, capability mismatch, offline reachability reports exact route. |
| Marker representation | Marker actor/data representation, required transforms/anchors, optional exit/entry metadata, authored tags, lifetime under streaming and association to route ID. | Agent 2 owns authored opportunity/marker; Agent 1 specifies execution-required fields; Agent 3 approves cross-module shape. | Agent 1 performs read-only discovery/query, then owns traversal execution. Marker lifetime follows loaded world/streaming cell. | Not agreed. Tests: marker load/unload, missing/invalid fields, deterministic candidate discovery. |
| Query parameters | Query origin/forward, player snapshot reference, capability/context, interaction/route filters, collision/clearance requirements, deterministic ordering, and whether query is pure/read-only. | Agent 1 publishes query contract; Agent 2 provides authored metadata. | Query reads world/player; only Agent 1 execution mutates player/capsule. | Not agreed. Tests: boundary/invalid context, deterministic choice, unavailable route, no mutation during query. |
| Query result and failure semantics | Typed success/no-candidate/blocked/unsupported/invalid-data/streaming-unavailable outcomes; result candidate identity and expiry/revalidation rules; define prompt vs silent failure and diagnostic path. | Agent 1 owns result/behavior; Core owns shared result values if consumed by Agent 2. | Agent 2 may consume result for gating/authoring validation, never perform player fallback itself. | Not agreed. Tests cover each terminal result and ensure no false success/unsafe transform. |
| Interruption/fallback | Preserve M1 v1.4 priority, bounded relocation candidate attempts, terminal hold phase, revalidation at only permitted transform-write path, restoration and forced transition semantics. | Agent 1 owns implementation; Core publishes only needed result/events. | Agent 1 owns player/capsule writes. Agent 2 receives events/results only. | Design accepted, not implemented/verified. Contract tests must include lethal + stagger, cinematic takeover, blocker inserted after detection, unsupported hold with falling mode, and terminal out-of-world routing. |

### 3.5 Damage, hit resolution, stagger and applied event

| Contract | Publisher / implementation owner | Consumers / lifetime / mutation authority | Required semantics | Status and acceptance tests |
|---|---|---|---|---|
| Damage request | Agent 1 proposes combat fields; Agent 3 publishes Core request. Agent 1 owns producer/application pipeline. | Agent 1 combat/receiver; Agent 2 may originate approved enemy attack intent but must use the single pipeline. Request lifetime is one resolution/application transaction unless explicitly persisted. Only Agent 1 hit/damage authority applies player/enemy damage under TD decision. | Attacker/target identity; base amount/type; source/attack identity; relevant hit summary; requested effect; validation and duplicate handling. Separate intent from applied result. | Required proposal pending. Tests: invalid target/request, one application per accepted hit, deterministic duplicate rejection/idempotence policy. |
| Hit-resolution result | Core publishes shared value/result; Agent 1 owns arbitration implementation. | Agent 1 reactions; Agent 2 enemy response. Local transient references may be weak and short-lived; durable consumers use stable IDs. | Enumerate outcomes (e.g. hit/block/parry/dodge/invulnerable/miss as candidates); state whether result implies damage applied; include ordering/transaction ID. | Required proposal pending. Tests: mutually exclusive resolution; ordering; result does not accidentally double-apply damage. |
| Damage application | Agent 1 is sole owner per TD decision. | Applies to authoritative damage attributes/effects; emits Core event only after actual result. | Define exactly when health/posture changes, how lethal outcome is determined, and failure/rollback behavior. GAS or another approved system remains an implementation choice subject to architecture. | Ownership accepted; concrete API pending. Tests: one application, lethal boundary, invalid/immunity paths, no event claiming unapplied damage. |
| Applied-damage event | Agent 3 publishes Core value event; Agent 1 emits; Agent 2 consumes. | Cross-module event lifetime must survive source actor destruction; no owning actor pointers in durable event. Stable identity and value payload. | Distinguish requested damage, resolved hit and applied damage. Define amount, damage type/tag, result, target/source IDs, lethal/posture information, optional location summary and transaction identity. | Required proposal pending. Tests: identity valid, actor destruction safe, emitted only once after application, payload agrees with resulting state. |
| Stagger classification/precedence | Agent 1 proposes semantic contract; Agent 3 publishes shared classification; Agent 1 implements precedence. | Agent 2 reads resulting combat/action event, does not independently decide whether player stagger occurs. | Preserve M1 v1.4: lethal damage takes precedence (priority 100); cinematic takeover bypasses positional fallback; stagger-causing damage, posture break or successful parry forces Stagger (priority 80); non-staggering damage aborts only within `AbortWindow`, else traversal continues; health application is independent of control/state. Do not assume permanent `bCausesStagger` field. | Behavior accepted; storage unresolved. Tests exhaust precedence pairs, posture/parry cases, damage outside abort window, health/state independence. |

### 3.6 Telegraph timing and identity

| Contract | Publisher / implementation owner | Consumers / lifetime / mutation | Status / acceptance tests |
|---|---|---|---|
| Telegraph/window message | Agent 1 proposes shared attack-window schema; Agent 3 publishes; Agent 2 produces enemy/encounter timing through approved producer API; Agent 1 consumes for parry/block. Any player attack window uses same semantics. | Consumers include combat and AI. Message lifetime covers declared attack window and its cancellation; only source/attack authority creates or cancels its window, with Agent 1 hit arbitration remaining sole hit/damage authority. | Not agreed. Specify stable window/attack and source IDs, target/area, gameplay-time units, open/update/close/cancel events, sequence/order, pause/time dilation/world unload, late subscriber snapshot semantics and duplicate prevention. Tests: deterministic timing, pause/resume, cancel/interrupt, repeated IDs, stale/cross-world message rejection and exact open/close boundary. |

### 3.7 Core interaction lifecycle

| Lifecycle surface | Contract requirement | Publisher / implementation owner | Consumers / lifetime / mutation | Status / acceptance tests |
|---|---|---|---|---|
| Prompt and verb | Contextual localized prompt data and a stable verb/tag, without UI implementation inside the world actor. | Agent 3 publishes Core interface; Agent 2 supplies world content; Agent 1 routes to presentation/animation. | Prompt data lives with content; verb is registry-backed; only authorized content/tag changes. | Not agreed. Tests: missing prompt, unregistered verb, context variation, localization-safe result. |
| Eligibility and requirements | Query eligibility with read-only player context; model requirements (state/tags/items/flags/range) without interactable mutating player state. | Agent 2 proposes world requirements; Agent 1 supplies player snapshot; Agent 3 publishes shape. | Query is read-only; authoritative progression/requirements are evaluated by owner. | Not agreed. Tests: eligible/ineligible transitions and no state mutation during query. |
| Location association | Define whether location ID is required, optional or supplied by actor/data registry; use canonical typed ID. | Agent 2 authors association; Agent 3 governs ID type. | World/content lifetime; data owner changes association through reviewed data. | Not agreed. Tests: valid/missing/retired location reference. |
| Begin/tap/hold/progress | One caller-owned lifecycle supports tap and hold; progress source, units, completion threshold and repeated tick behavior are explicit. | Agent 1 player interaction router calls; Agent 2 implementation responds; Agent 3 publishes API. | Player router owns input/progress timing; interactable owns action behavior but cannot mutate player state directly. | Not agreed. Tests: tap, hold start/progress/complete, cancellation before completion, duplicate begin suppression. |
| Cancel/end/completion | Explicit cancel reasons and terminal outcome; completion emitted once as Core event/value; distinguish cancellation from successful action. | Agent 2 produces outcome; Agent 3 publishes event; Agent 1 routes call. | Completion event survives actor lifetime as needed; no raw pointer required for durable consumers. | Not agreed. Tests: cancel/interrupt/unload, exactly-once completion, no completion on cancel/failure. |
| Progress grant | Interactable reports an interaction fact; it does not directly grant persistent memory/quest progression. | Agent 3/TD owns persistence/progression event authority; Agent 2 world object supplies fact. | Progress subsystem is sole grant authority. | Existing authority preserved. Tests: event can be consumed once, duplicate/replay policy, invalid context cannot grant. |

### 3.8 Contract lifecycle/status protocol

For every contract version, Agent 3 maintains: stable ID/version; owner/publisher; implementation owner; named consumers; lifetime/thread/world scope; mutation authority; status (`DRAFT`, `UNDER_REVIEW`, `ACCEPTED`, `DEPRECATED`); compatibility/migration note; and executable acceptance test names. A proposal is not `ACCEPTED` until the producer and all named consumers agree and TD records acceptance. No field is frozen merely by inclusion in this planning document.

## 4. Environment/toolchain feasibility and version recommendation

### 4.1 Inspection performed

Inspection in this workspace found:

- Host: Linux `x86_64`, kernel `6.1.158+`.
- Available: `/usr/bin/g++` (Debian 12.2.0), Python 3.11.2 and Git.
- Not found on `PATH`: `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh`, `dotnet`, `clang++` or `clang`.
- No `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh` or `UE_5.*` installation found in inspected common roots `/opt`, `/usr/local`, `/home/user/UnrealEngine`, `/home/user/UE`, `/mnt` (search limited to depth 4).
- The canonical checkout has no `.uproject`, targets, modules or runtime code. No actual editor/build/test attempt was made.

This establishes that **this workspace cannot presently prove UE project creation/open/build/automation feasibility**. It does not prove that the production workstation lacks Unreal or that no installation exists outside inspected paths.

### 4.2 Recommendation

**Recommendation: do not pin an exact Unreal minor/patch/build from this workspace.** The host, compiler/distribution, target platform, SDK, required plugin compatibility and intended production workstation are unknown, and this environment has no Unreal toolchain. Selecting UE 5.8 (or any other specific minor) from the Agent 2 branch descriptor would repeat the unverified assumption the TD explicitly rejected.

Recommended selection procedure: nominate the intended production host and target platform first; inventory officially available UE5 distributions on that host; compare supported compiler/SDK and required plugin availability; then choose the newest production-suitable UE5 release that passes a clean project-open/build/Automation-Test compatibility spike on the actual target host. Pin the exact major/minor/patch/build and distribution in the M0 manifest only after that evidence. This is a recommendation to defer the exact version, not a claim that any particular release has been tested or is currently available.

**Feasibility status:** BLOCKED in this workspace; production-host feasibility NOT ASSESSED.
**Exact version/build/distribution:** OPEN TD DECISION.
**Target platform/toolchain:** OPEN TD DECISION.
**No Unreal build or runtime test was run.**

## 5. Revised interface ownership register

| Contract/domain | Publisher / contract authority | Implementation owner | Consumers | Lifetime / mutation authority | Status |
|---|---|---|---|---|---|
| Core IDs, tags, events, shared interfaces/value types | Agent 3/TD in `TDDCore` | Domain owner for each producer/consumer; Agent 3 maintains Core definitions | Agents 1/2, approved UI/persistence | Stable value/event lifetime as specified; only contract owner/TD-approved changes | Accepted ownership; details proposed, not frozen |
| Player controller/input/state/locomotion/traversal execution/combat/damage | Agent 1 for system surface; Core publisher for shared types | Agent 1 | Agent 2 via read-only snapshots/events; Agent 3 integration | Agent 1 alone mutates player state/capsule and resolves hit/damage | Accepted |
| Traversal opportunities/markers/route requirements/world association | Agent 2 authors schema proposal; Agent 3 publishes shared ID/contract; Agent 1 specifies executable requirements | Agent 2 for authored world data/markers; Agent 1 for execution | Agent 1 query/execution; Agent 3 validators | World data lifetime follows authored content/streaming; Agent 2 mutates content, not player state | Ownership accepted; interface unresolved |
| Player context and state snapshots | Agent 1 proposes fields; Agent 3 publishes shared Core contract | Agent 1 provider | Agent 2 and approved consumers | Read-only value/view, safe lifetime; Agent 1 authority | Requested, not agreed |
| Hit arbitration and damage application | Agent 1 behavior owner; Agent 3 publishes shared Core request/result/events | Agent 1 | Agent 2 enemy/boss response; other approved event consumers | Transaction-local result; actor-free durable applied event; Agent 1 sole resolver/applier | Ownership accepted; payload unresolved |
| Stagger semantics | Agent 1 proposes behavior; Agent 3 publishes any shared classification | Agent 1 | Agent 2 consumes result/state events | State mutation only by Agent 1; preserve M1 precedence | Behavior accepted, storage pending |
| Telegraph timing | Agent 1 proposes schema/consumer semantics; Agent 2 proposes enemy producer needs; Agent 3 publishes shared contract | Agent 2 enemy timing producer; Agent 1 player combat consumer/arbiter | Both agents | Gameplay-time stream with declared IDs, cancellation and pause semantics | Requested, unresolved |
| Interaction lifecycle | Agent 3/TD Core publisher | Agent 1 player router; Agent 2 world interactable implementation | Both agents; narrative/progression receives event | Explicit tap/hold/cancel/completion; progress grant owned by progression authority | Ownership accepted; API unresolved |
| Scene/chapter/streaming/population/world simulation | Agent 2 domain authority | Agent 2 | Agent 1 traversal/encounter integration; Agent 3 validation/persistence | Authored data vs runtime-measured results explicitly distinguished | Domain ownership accepted; measurements pending |
| Module/build foundation | Agent 3/TD | Agent 3 for foundation; domain owners for their modules | All agents | Build/module graph controlled by TD; change recorded | Four initial modules accepted; project/toolchain unavailable |

## 6. Agent 1 / Agent 2 agreement and unresolved-conflict register

The TD has accepted responsibility boundaries, but concrete compatible Agent 1/2 proposals have **not yet been received or reconciled** in this addendum. The following are submission requests, not claims that either agent has been contacted through a separate agent-control channel.

| ID | Required compatible submissions | Current agreement | Unresolved conflict / decision needed | Blocks / closure evidence |
|---|---|---|---|---|
| C-01 | A1 proposes traversal executable vocabulary/query/results; A2 proposes route IDs, marker/schema and world requirements. | Authority split accepted. | Enum/action names; route-ID type; data-vs-code requirements; entry/exit data; query parameters/order; unsupported/blocked/invalid/unloaded semantics; revalidation/lifetime. | Route gating and reachability. Close with jointly referenced proposal, consumer sign-off, TD acceptance and test list. |
| C-02 | A1 proposes player-context/state snapshot; A2 lists minimal actual reads. | Read-only consumer boundary accepted; state concepts separate. | Snapshot shape, location/clock/update semantics, optional stealth/noise/target fields, event/delegate shape and lifetime. | World gating/perception. Close with field-level consumer justification and immutability/lifetime tests. |
| C-03 | A1 proposes damage request, local hit result and application outputs; A2 states enemy/boss reaction needs. | A1 owns arbitration/application; shared events Core-owned. | Actor pointers vs stable IDs, hit vs applied event distinction, event payload, duplicate handling, transaction identity. | Enemy reaction and damage integration. Close with one pipeline diagram and exact result/event acceptance tests. |
| C-04 | A1 proposes stagger classification storage alternatives and precedence mapping; A2 confirms required response events. | Preserve M1 v1.4 semantics; `bCausesStagger` not presumed permanent. | Classification source (request field, tag, damage data/effect or combination), posture/parry classification, event timing. | Traversal interruption/combat response. Close with semantic matrix and precedence tests; TD accepts storage choice. |
| C-05 | A1 proposes parry/block window consumption semantics; A2 proposes enemy telegraph production fields/time. | Shared timing boundary required. | Clock and pause/time-dilation, IDs, start/update/end/cancel, target/area, late join, ordering, world unload, intent vs active window. | Enemy fairness/parry. Close with event timeline, lifecycle/state diagram and deterministic timing tests. |
| C-06 | A1 proposes player-side begin/tap/hold/cancel routing and verb mapping; A2 proposes world actor eligibility/content/completion. | One Core-owned lifecycle; A1 router, A2 implementations. | Method/event signatures, who tracks hold progress, requirements/location placement, context constness, completion exactly-once and error/cancel semantics. | All world interaction. Close with sequence diagram and tap/hold/interrupt/duplicate tests. |
| C-07 | A1 lists tags/IDs needed for gameplay; A2 supplies world/location/memory/route identity use cases. | Shared registries and IDs governed by Agent 3/TD. | Canonical stable ID representation, route ID namespace, actor-vs-content IDs, tag naming/change policy and save migration. | All cross-module data and persistence. Close with registry contract and duplicate/unknown/retired ID validation. |
| C-08 | Agent 2 provides W-M2.3 bounded class arithmetic against source rows and exact register version; Agent 3 independently checks reconciliation. | Counts must be register-derived and endpoint-aware; values remain projections. | Discrepancy in count of bounded classes (W-M2.3 correction text shows five bounded rows, while the TD notes a bounded-class count mismatch requiring reconciliation). | Capacity model confidence only; no runtime gate can rely on it yet. Close with source-row reconciliation and reproducible evidence artifact. |
| C-09 | Creative Director reviews `CH01-SCN-014` source prose/count and decides amendment or acceptance of an unbounded term. | No number may be invented. | Whether source register changes, accepts open upper bound, or directs another authoritative capture. | Ch1 capacity band remains open; only CD can decide source/content. |
| C-10 | Agent 3 prepares M0 manifest after toolchain feasibility check; TD chooses exact engine/platform. | M0 evidence requirements accepted. | UE exact version/distribution/build, intended host/compiler/SDK, target platform, plugin allowlist, runner access. | Actual project/build/test blocked. Close with pinned environment and captured M0 gates. |

### Agent submission packet

Each Agent 1/Agent 2 submission should be a versioned proposal/addendum to its own source material (preserving prior versions), cross-reference the corresponding IDs C-01 through C-07, state all seven required contract metadata fields, list concrete alternatives where unresolved, and include acceptance-test names/assertions. Mark it `PROPOSAL — NOT FROZEN` until the other named consumer signs and TD accepts it. Agent 3 will consolidate only after both sides submit; this document does not silently resolve remaining signature/design choices.

## 7. Initial module dependency diagram

Initial topology accepted by TD; diagram expresses permitted dependency direction, not a claim that files/modules exist:

```text
                     ┌──────────────────────────┐
                     │       TDDCore             │
                     │ IDs, tags, events,        │
                     │ shared contracts/value   │
                     └────────────┬─────────────┘
                                  ▲
                                  │ depends on Core only
                     ┌────────────┴─────────────┐
                     │       TDDRuntime          │
                     │ gameplay + world runtime  │
                     │ (Agent 1 / Agent 2 areas) │
                     └──────────┬───────┬───────┘
                                ▲       ▲
                 depends on     │       │     depends on
                 Runtime/Core   │       │     Runtime/Core
                   ┌────────────┘       └────────────┐
          ┌────────┴────────┐                 ┌──────┴─────────┐
          │   TDDEditor      │                 │   TDDTests     │
          │ editor-only tools│                 │ automation/tests│
          └─────────────────┘                 └────────────────┘
```

Constraints:

- `TDDCore` must not depend on `TDDRuntime`, Agent 1/2 implementation code, world modules, editor modules or test modules.
- `TDDRuntime` may depend on `TDDCore`; `TDDCore` cannot call upward into it. Keep editor-only dependencies out of runtime.
- `TDDEditor` and `TDDTests` may depend on the modules they test/extend as required by actual Unreal rules; neither becomes a backdoor shared gameplay API.
- Avoid circular dependencies. Cross-domain calls/events go through Core contracts or deliberately narrow public APIs.
- Additional `TDDAI`, `TDDWorld`, `TDDNarrative` or other modules require a documented concrete dependency boundary, ownership, dependency graph, build/test evidence and TD approval. The MEAD's earlier multi-module proposal is historical input, not the current initial topology.
- Module names and dependency policies are accepted; no build files or project descriptors are authorized/created here.

## 8. Dependency-ordered M0 preparation plan

This plan prepares a future authorized M0; it does **not** authorize project creation or any gameplay code.

| Step | Preparation action | Owner(s) | Exit/acceptance evidence | Gate / blocker |
|---|---|---|---|---|
| P0 | Preserve canonical TDD checkout and record exact branch, commit, status. Keep Agent 2 skeleton read-only and separate. | Agent 3 | Manifest references TDD; no imported skeleton files; worktree unrelated work preserved. | Satisfied as repository direction; project still absent. |
| P1 | Identify intended development/production host, OS, compiler, target platform/SDK, distribution/licensing/access, plugins and asset/source-control policy. | TD + project/toolchain owner | Written environment inventory with exact versions, availability and responsible operator. | OPEN; current sandbox is not a UE workstation. |
| P2 | Evaluate production-host UE candidates against platform/toolchain/plugin needs; select exact release only after a real compatibility spike. | Agent 3 recommends; TD decides | Candidate matrix and recommendation; exact major/minor/patch/build/distribution; target SDK compatibility evidence. | OPEN; no version can be verified from current workspace. |
| P3 | Receive compatible A1/A2 proposals C-01…C-07; Core review for IDs/tags/events/interactions and contract tests. | Agent 1 + Agent 2; Agent 3/TD | Each proposed contract contains publisher, implementation owner, consumers, lifetime, mutation authority, status and acceptance tests; producer/consumer sign-off and TD acceptance recorded. | OPEN; no implementation against unresolved contracts. |
| P4 | Confirm M0 entry authorization, project/module location, plugin allowlist, binary/source policy and initial module graph. | TD | Explicit authorization record, canonical path and pinned environment; four modules (Core, Runtime, Editor, Tests) with reviewed downward dependencies. | BLOCKED until TD authorization/toolchain. |
| P5 | Only after P4, establish the genuine Unreal project and minimal four-module foundation in canonical TDD. Do not copy Agent 2 skeleton. | Authorized project owner / Agent 3 | Created by supported Unreal workflow on pinned engine; project identity and initial clean status captured. | NOT AUTHORIZED by this instruction. |
| P6 | Add a meaningful project-owned Unreal Automation Test and designated foundation test content/config as minimally required. | Agent 3, review by TD | Test has concrete fail conditions; compiles into approved target; not an echo/Python surrogate. | Depends on P5 and actual engine/test environment. |
| P7 | Execute M0 gates: editor open/reopen, clean build, Automation Test; capture manifest, raw logs, reports and artifact identity. | Agent 3 / operator | Exact M0 checklist evidence on same commit/toolchain; each result PASS/FAIL/BLOCKED/NOT RUN/NOT MEASURED. | Depends on P6 and working runner/SDK. |
| P8 | Report M0 and update quality ledger; preserve defects/open decisions; do not overstate CI/package/performance. | Agent 3; TD accepts gate | Evidence-linked report and explicit outstanding items; no CI/package claim without execution. | Only after P7. |

## 9. Updated decision and blocker register

### 9.1 Accepted decisions (closed for this phase)

| ID | Decision | Status / binding effect |
|---|---|---|
| D-01 | TDD is canonical; Agent 2 skeleton not adopted. | **ACCEPTED / GOVERNING.** No copy/merge. |
| D-02 | Agent 3/TD owns Core publication/governance. | **ACCEPTED / GOVERNING.** Shared type/event/interface changes require review. |
| D-03 | Separate locomotion, action/control and combat status; Agent 1 mutates, Agent 2 reads. | **ACCEPTED / GOVERNING.** Concrete snapshots pending proposals. |
| D-04 | Agent 1 executes traversal; Agent 2 authors opportunities and world requirements. | **ACCEPTED / GOVERNING.** Handshake pending proposals. |
| D-05 | Agent 1 owns hit arbitration/damage application; shared events Core-owned. | **ACCEPTED / GOVERNING.** Request/result/event shapes pending. |
| D-06 | Single Core interaction lifecycle; Agent 1 player routing, Agent 2 interactables. | **ACCEPTED / GOVERNING.** Signature/sequence pending proposals. |
| D-07 | Agent 1 M1 v1.4 fallback/hold design preserved. | **ACCEPTED / DESIGN ONLY.** No runtime claim; no permanent `bCausesStagger` storage decision. |
| D-08 | M0 requires genuine project, build, project-owned Unreal automation and captured evidence. | **ACCEPTED / GATE.** Documentation/Python tests do not substitute. |
| D-09 | Initial module topology `TDDCore`, `TDDRuntime`, `TDDEditor`, `TDDTests`; Core independent; later modules need evidence. | **ACCEPTED / GOVERNING.** No module files created. |

### 9.2 Open decisions and blockers

| ID | Outstanding item | Owner / decider | Effect / next required action |
|---|---|---|---|
| B-01 | Exact Unreal version/build/distribution; host/compiler/SDK; first target platform. | TD, advised by Agent 3 after host inventory. | M0 environment and foundation blocked. Current sandbox lacks UE editor/UBT/RunUAT/dotnet/clang++; exact release recommendation deferred pending intended host/platform. |
| B-02 | Agent 1/Agent 2 compatible proposals C-01…C-07. | Agent 1 and Agent 2 submit; Agent 3 reviews; TD accepts. | Contract-dependent implementation remains blocked; proposals must preserve source/version history. |
| B-03 | `CH01-SCN-014` unbounded source term. | Creative Director. | Keep capacity upper band open; amend authoritative register or explicitly accept open bound; do not invent a number. |
| B-04 | W-M2.3 bounded-class count discrepancy. | Agent 2 reconciles against authoritative register; TD reviews. | Correct the row/class count with exact register/version and reproducible evidence; retain all projections as projections. |
| B-05 | Population/performance capacity figures are not engine measurements. | Agent 2 + Agent 3 measurement owner; TD accepts criteria. | No measured/performance claim until actual representative UE build/map/capture on approved hardware. |
| B-06 | Explicit project creation/M0 entry authorization and canonical project path. | TD. | This instruction accepts topology and evidence gate but does not authorize project creation; P5 cannot begin until separately authorized. |
| B-07 | M0 operator access to compatible engine, target SDK and runner. | Project/toolchain owner. | Build and automation remain BLOCKED until toolchain is actually available. |
| B-08 | Tag/typed ID schema and exact initial registry. | Agent 3/TD with Agent 1/2 submissions. | Prevent inconsistent IDs/tags, route data errors and save migration hazards. |
| B-09 | Exact module dependency edges and any later module split. | Agent 3/TD; domain owners provide concrete graph. | Keep initial four-module boundary; additions require demonstrated dependency reason and approval. |

**No other creative, narrative, cultural or visual content decision is made here.** The `CH01-SCN-014` ruling belongs to the Creative Director; population and performance data cannot authorize story/content changes.

## 10. Change history and acceptance

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Recorded TD-accepted integration boundaries and four-module topology; specified Core contract submission requirements; documented local toolchain feasibility and version recommendation; added A1/A2 agreement register, M0 preparation plan, and updated decision/blocker register. |

This addendum preserves prior agent sources and historical review documents unchanged. A future update must increment the version and append a change entry; do not overwrite archived Agent 1/2 material.
