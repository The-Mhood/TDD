# Cross-Agent Contract Reconciliation — C-01 through C-07

**Document:** `TDD-INT-RECON-001` · **Version:** 1.0
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Governing record:** [`TDD-TD-INT-001 v1.2`](TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md)
**Status:** `AWAITING SUBMISSIONS — NO CONTRACT IS AGREED OR FROZEN`.

## 1. Source identity and evidence boundary

The C-01…C-07 submission packets are the exact files at published commit `50b14318c8089dedcc688fb2c78ad3cb361c15f5`:

- Agent 1 packet: `docs/AGENT1_CONTRACT_SUBMISSION_PACKET_V1.md`.
- Agent 2 packet: `docs/AGENT2_CONTRACT_SUBMISSION_PACKET_V1.md`.

The pinned published agent sources reviewed for prior interface shapes are Agent 1 branch `arena/3bc206a0-tdd`, commit `bb2685c605efd4958b1c67944721c77e1b393931`; and Agent 2 branch `arena/5dde91a4-tdd`, commit `ed36ad6d9cab946ede859e0dd1000a480b114f91`. Those historical documents are **context only**, not responses to the packets. Current remote refs should be rechecked when submissions arrive.

**Dispatch:** no direct agent-message/assignment channel was exposed in this session. Copy-ready, separately addressed requests and proposed deadline `2026-11-18 17:00 UTC` are recorded in [`Agent 1 response ledger`](AGENT1_CONTRACT_RESPONSES_V1.md) and [`Agent 2 response ledger`](AGENT2_CONTRACT_RESPONSES_V1.md). Neither has been sent through an agent channel; receipt is not claimed. No proposals or acknowledgements have been received.

## 2. Reconciliation rules

- `AWAITING SUBMISSION` means the agent has not supplied a versioned response to the current packet; old source material is not silently reclassified as a response.
- `NOT ASSESSABLE` means producer/consumer agreement cannot be checked because at least one side's packet response is absent.
- “Known source-shape conflict” below records observable differences in the pinned historical documents only. It does not claim either agent endorses that old wording now.
- Technical recommendations are limited to process and preservation of accepted boundaries until both submissions arrive. No API, field, enum, tag or signature is selected here.
- Candidate test IDs in the submission packets are proposals only; none is claimed implemented or passed.

## 3. Contract-by-contract comparison

| ID | Agent 1 proposal | Agent 2 proposal | Producer/consumer agreement | Known historical source-shape conflicts (not current submissions) | Recommended resolution / technical rationale | TD decision required now? |
|---|---|---|---|---|---|---|
| **C-01 Traversal** | **AWAITING SUBMISSION.** Required: executable action vocabulary, player query and result/failure semantics, required candidate inputs and interruption behavior. Existing M1 v1.4 supplies fallback/hold behavior, not a frozen cross-agent route API. | **AWAITING SUBMISSION.** Required: authored route IDs, markers, world requirements, streaming validity and reachability use. Existing request asks for action/data/code/failure definitions but is not a finalized proposal. | **NOT ASSESSABLE.** No same-version producer/consumer review. | Agent 2's request explicitly leaves action enum, data-vs-code requirements and failure semantics open. Agent 1's M1 contract does not settle markers/route IDs/query API. | Collect both sides' concrete fields and examples first. Keep Agent 1 execution/fallback authority and Agent 2 authored-data authority; preserve M1 v1.4 unchanged. Compare route lifetimes and unsupported/invalid/unloaded outcomes without choosing for either side. | No detailed TD API decision until both submissions; current authority split is already accepted. |
| **C-02 Player context and states** | **AWAITING SUBMISSION.** Required: authoritative Agent 1 provider, field list, state snapshots, time/units/lifetime, validity and read-only boundary. | **AWAITING SUBMISSION.** Required: actual world fields consumed, named consumers, cadence/freshness and invalid-context handling. | **NOT ASSESSABLE.** No field-level consumer sign-off. | Agent 1 MEAD's proposed character/action state machine and proposed `FTDDPawnKinematics` differ in scope from Agent 2's `FTDDLocomotionState` list and requested `UTDDPlayerContext`. They combine locomotion/action/combat differently and are not source-compatible as written. | Require minimal field-by-field use cases. Keep locomotion, action/control and combat status separate per TD. Agent 1 alone mutates; Agent 2's interface must be read-only. Do not make a mega-enum or include fields without consumers. | Only if proposals leave source/authority/lifetime ambiguous. |
| **C-03 Damage** | **AWAITING SUBMISSION.** Required: Agent 1 single hit arbitration/application, request/result lifecycle, dedupe, timing and Core event payload needs. | **AWAITING SUBMISSION.** Required: enemy/boss reactions and exact damage/poise data needed; no separate application path. | **NOT ASSESSABLE.** No producer/consumer trace or agreement. | Agent 1 MEAD proposes actor-free `FTDDDamageAppliedEvent` with stable entity IDs. Agent 2 proposes `FTDDHitEvent` with weak actor pointers, result and frame stamp. These may represent distinct transient-vs-applied concepts but the split is not approved. | Ask Agent 1 to distinguish local resolution from applied damage; ask Agent 2 which facts each world consumer needs and lifetime. Then Core can publish one consistent event/value contract without duplicative damage or stale durable actor references. | No payload decision until both submissions. A1 sole authority/Core event ownership are accepted. |
| **C-04 Stagger / forced result** | **AWAITING SUBMISSION.** Required: semantic classification alternatives and executable precedence/outcome behavior, not presuming `bCausesStagger`. | **AWAITING SUBMISSION.** Required: world response to authoritative result/state, without independent player classification. | **NOT ASSESSABLE.** No same-version acknowledgment. | M1 v1.4 references `bCausesStagger` but explicitly leaves it a Core proposal. It defines lethal/cinematic/stagger behavior. Agent 2 needs damage/poise notification but has no agreed outcome contract. | Preserve **Dead > Cinematic > Stagger**, independent health application, non-stagger `AbortWindow`, and fallback/restoration semantics. Agent 1 proposes storage alternatives; Agent 2 specifies only required reactions. TD chooses representation only if owner proposals do not converge. | No storage/signature decision until proposals; accepted priority and M1 behavior remain governing. |
| **C-05 Telegraph** | **AWAITING SUBMISSION.** Required: parry/block consumer lifecycle, temporal precision, clock/pause, ordering and cancel behavior. | **AWAITING SUBMISSION.** Required: actual enemy producer, attack/window identity, timing source, updates and cancellation. | **NOT ASSESSABLE.** No shared event timeline or signed semantics. | Agent 2 requests a telegraph stream; prior text mentions activation/window timing. No shared clock, IDs, pause/time dilation, cancellation, late consumer or ordering contract is established. | Each side supplies a sequence/timeline and invalidation cases. Keep telegraph separate from hit arbitration/application. Agree time source and window ID before matching parry logic to producer windows. | No detailed event decision until timeline proposals. |
| **C-06 Interaction** | **AWAITING SUBMISSION.** Required: player focus/input, tap/hold, progress timing, animation verb, cancellation and completion needs. | **AWAITING SUBMISSION.** Required: world prompts, eligibility, requirements, location association, action and completion behavior. | **NOT ASSESSABLE.** No lifecycle sequence reviewed by both. | Prior Agent 1 MEAD proposes Begin/Tick/End/Cancel; Agent 2 has both a short CanInteract/GetPrompt/Interact shape and a longer `UTDDPlayerContext`/verb/mode/completion proposal. They differ in signature, ownership and lifecycle. | Ask each side for a concrete sequence and cancellation matrix. Preserve one Core-owned lifecycle; A1 routes player input, A2 implements world content; progression authority remains separate. No choice of signatures before mutual review. | No API decision until proposals; accepted ownership split remains. |
| **C-07 IDs / Tags** | **AWAITING SUBMISSION.** Required: player/combat/traversal identity and tag inventory, persistence/lifetime needs. | **AWAITING SUBMISSION.** Required: exact world/content IDs/tags, source versions, reference validation and persistence needs. | **NOT ASSESSABLE.** No merged inventory or registry agreement. | Agent 1 event proposal uses `FGuid` identity; Agent 2 branch defines typed `FTDDLocationId`/`FTDDMemoryId`; world docs also use `FName`. Gameplay Tags are Core-governed but no shared initial vocabulary is accepted. | Collect use cases and distinguish runtime entity identity from authored content IDs and tags. Agent 3/TD owns one registry/contract; do not invent conversions or duplicate registries. Review save compatibility and retired-ID rules. | TD decides shared ID representation/tag policy only after both inventories; governance ownership already accepted. |

## 4. Dependencies and compatibility concerns pending confirmation

The following are dependency candidates inferred from existing architecture and require confirmation in the agents' submissions; they are **not new requirements**:

| Contract | Likely dependency to validate | Compatibility question |
|---|---|---|
| C-01 | C-02 read-only context and C-07 route/tag identity; M1 traversal/fallback design. | Can world-authored data request capability without depending on Agent 1 private classes? How do streaming and candidate expiry work? |
| C-02 | C-07 typed IDs/tags where used. | Are snapshots value-only or do they contain handles? Which state dimensions and update order are actually consumed? |
| C-03 | C-07 stable source/target identity; C-04 classification result. | Which result is transient and which event is durable/applied? How is exactly-once damage enforced? |
| C-04 | C-03 damage result; parry outcome from C-05. | Does posture/parry classification happen in one authority and how does it participate in priority arbitration? |
| C-05 | C-07 attack/window identity and C-03 hit-result separation. | What clock/window lifecycle connects telegraph to hit attempt without making telegraph apply damage? |
| C-06 | C-02 player context and C-07 interaction/verb/location IDs. | Who owns progress timing, target validity, and exactly-once completion across streaming/cancellation? |
| C-07 | Shared Core governance / registry owned by Agent 3/TD. | Can authored IDs remain stable across save, scene streaming and version changes? |

For every dependency, Agent 1 and Agent 2 must confirm or correct it. Any mismatch belongs in the next reconciliation version with both positions quoted and source/version cited.

## 5. Agreement and decision ledger

| Status | Meaning | Current C-01…C-07 count |
|---|---|---:|
| `AWAITING SUBMISSION` | Agent response not received. | 14 agent-side response slots (7 per agent) |
| `AWAITING COUNTERPART REVIEW` | A response exists but counterpart has not reviewed the same version. | 0 (no responses) |
| `DISAGREEMENT RECORDED` | Both positions exist and differ; record exact versions/quotes. | 0 submitted disagreements; this does not mean the historic documents had no conflicts |
| `AGREED — PENDING TD` | Both producer and consumer signed the exact same version. | 0 |
| `ACCEPTED / FROZEN` | TD explicitly accepts the consolidated version. | 0 |

**Required next event:** Agent 1 and Agent 2 provide versioned responses. Agent 3 records each arrival independently, then requests counterpart review on the exact revision. Do not draft a consolidated API from incomplete rows. If either response is late, keep that contract `AWAITING SUBMISSION` and leave downstream dependencies blocked.
