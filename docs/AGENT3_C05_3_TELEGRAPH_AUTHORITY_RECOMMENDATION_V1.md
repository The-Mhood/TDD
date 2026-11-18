# Agent 3 Architectural Recommendation — A2R-31 / C-05-3 Telegraph Authority

**Document:** `TDD-A3-ARCH-RECOMMENDATION-C05-3` · **Version:** 1.0
**Scope:** Focused architectural recommendation on the proposed stateful telegraph broker and ownership boundary.
**Status:** Recommendation only; not a TD ruling, contract signature, implementation authorization, or API freeze.

## Recommendation

**Do not place authoritative open-telegraph state in generic `TDDCore` or its process-lifetime event bus.** A stateful recovery/query surface is architecturally useful for late subscribers and revision-gap recovery, but the retained state belongs in the **Agent 1-owned, world-scoped combat ownership boundary**—the existing `UTDDCombatDirectorSubsystem` boundary identified in MEAD-C—subject to TD/Agent 1 approval of that responsibility. Keep TDDCore responsible for shared value contracts and message transport, not custody of live combat timing state.

This recommendation does **not** decide A2R-31/U-07 for the TD, close C-05, or approve A1-R4's proposed broker. If the TD elects to put the authority in Core anyway, it should explicitly require a world-lifetime boundary. The inspected MEAD-C architecture lists no existing TDDCore `UWorldSubsystem` suitable for that role; its `UTDDEventBus` is a `UGameInstanceSubsystem` with process lifetime, which is too broad for state belonging to one streamed combat world. Creating/assigning such a Core authority would therefore be a separate ownership decision, not merely adding a query method.

## Basis in the exact records

1. **A1-R4 proposes an actual authority transfer.** In `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md`, A1-R4 v1.3, exact blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75` at branch head `142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6`, §4.1 proposes a Core `UTDDTelegraphBroker` that retains the current timing block and phase per open `AttackInstanceId`, supplies `GetOpenTelegraphs`, and snapshots active state on subscription. The clause expressly says the broker becomes “authoritative for current telegraph state,” not merely a relay.
2. **A2 identifies the ownership change as A2R-31 / C-05-3.** The formal review `Docs/AGENT2_REVIEW_A1R4_V1.md`, commit `7ea0a85cc5e1d9bfe6aff4fc861f041f01c30cc1`, §§5.3–5.5 says this changes custody from the producing ability system to Core. A2 recommends the recovery mechanism, but withholds its C-05 signature until Agent 3/TD decide whether Core may own that state. A2R-31 expressly asks that this be treated as a Core-ownership request, separate from the event-versus-query question.
3. **TD v1.2 leaves C-05 ownership/lifecycle open.** `docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md`, exact commit `e121bbbf09562e3cba0efe81aad971809685db23`, C-05 requires a common event timeline, pause/time-dilation behavior, open/close/cancel and world-unload rules; it does not grant the broker authority.
4. **The candidate architecture's lifetime and ownership table favors a world combat boundary.** MEAD-C, `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md`, commit `169a8d8f4f95dca526239dfbf744e97590504a70`, §3.4 assigns `UTDDEventBus` to Agent 3 as a process-lifetime `UGameInstanceSubsystem`, but assigns `UTDDCombatDirectorSubsystem` and `UTDDHitStopSubsystem` to Agent 1 as `UWorldSubsystem`s. The same section says world-scoped state belongs in a `UWorldSubsystem`; §7.1/§7.3 describes the combat director's combat-coordination role. §3.5 keeps Core events as value data with IDs rather than actor pointers.
5. **A distinct candidate document separates Core contracts from gameplay combat.** MEAD-A, `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, inspected tip `912fac9f76a1011f8c823b368a92a0edf059a283`, §4.2 places combat ability/hit arbitration/damage resolution under the runtime Combat area, while shared interfaces/framework are separate. This is corroborating architecture evidence only. These MEAD documents diverge; citing either does not select a canonical MEAD. Reconciliation V3 §5 records the divergence and TD's pending authority.

## Ownership split recommended for TD consideration

### Producing ability system / actor (Agent 1 domain)

- Own attack-instance creation and the authored phase/window definition.
- Compute and publish the timing block using the approved clock conversion; issue monotonically increasing revisions for that `AttackInstanceId`.
- Publish phase changes, retimes, normal close, and explicit cancellation/invalidation. It remains the authority for the timing facts it produces; the broker must not invent a new end time or run a competing timer.
- Invalidate its open entries before, or as part of, actor/component teardown, death cancellation, and stream-out.

### World-scoped combat authority (recommended existing boundary: `UTDDCombatDirectorSubsystem`)

- Retain the latest producer-authored timing block and phase for each currently registered attack instance so late subscribers and recovering consumers can obtain one consistent snapshot across all active producers.
- Enforce revision adoption (A2R-32), at-most-once phase-entry observation (A2R-33), and invalidation/eviction plus non-reentrant snapshot/query behavior (A2R-34) if those clauses are accepted in a later exact contract version. This recommendation does not itself close those findings.
- Scope entries to the owning world; provide a current-state snapshot/query as well as event notifications. Keep records value-based (IDs, revisions and timing data), not owning actor pointers.
- Do not own authored attack timing, calculate local-time conversion, decide parry success, perform hit arbitration, or apply damage. Those remain producer/gameplay decisions under their respective contracts.

### TDDCore

- Own only the approved shared message/value contract and generic event transport required by the architecture.
- Do not retain a process-global collection of open attack timing blocks in `UTDDEventBus` or other `UGameInstanceSubsystem` merely to provide recovery. If TD explicitly chooses Core custody, require an explicitly approved world-lifetime boundary and named owner; do not let the existence of a struct, event bus, or query imply that decision.

## Lifecycle and dependency consequences

- **Actor destruction / death:** a producer can disappear without sending normal `Closed`. The world combat authority needs an explicit invalidation path tied to producer teardown, with a fail-safe for unexpected invalidation; otherwise stale entries can be returned by a recovery query. A `Closed` event alone is not sufficient.
- **Streaming unload:** unloading one producer must invalidate only its attack instances while the world authority remains alive. World teardown must clear all entries. A process-lifetime registry risks carrying a stale telegraph across map/world transitions; a weak actor reference alone is not a lifecycle policy.
- **Producer invalidation:** consumers must treat invalidated entries as closed and never recover a block whose producer is gone. Any age/staleness fallback must use the agreed gameplay-time semantics (including pause/dilation) and must not be the sole cleanup mechanism; no staleness bound is selected here.
- **Ordering and re-entrancy:** snapshots and messages need a shared revision rule, and query delivery must not mutate a registry while a subscriber is iterating it. A consumer resuming after a gap must be able to reconcile to one current snapshot without duplicate phase-entry effects. These are A2's C-05-4a–d findings, not implementation work authorized by this recommendation.
- **Ownership dependency:** moving storage into Core makes Agent 3 responsible for world teardown, actor invalidation, ordering, and the query contract, not merely the generic event bus. Keeping it inside the Agent 1-owned combat boundary preserves one feature owner while still allowing a shared Core-facing read/message contract. TD must decide whether to accept this responsibility boundary.

## Alternative if the world combat boundary is not approved

Keep each producer as the authority for its own open timing block and recovery snapshot. Consumers recover from the relevant producer authority (or a producer-owned world registry), while Core remains a stateless event/value transport. If there is no approved aggregation/query authority, retain the A1-R4 fallback: a revision gap is unknown/unrecoverable and C-05 remains blocked on U-07. Do **not** silently promote the Core event bus into a state owner to make the gap appear resolved.

## Explicit non-decisions

This document does not implement or create/modify C++ types; does not freeze C-05 or another contract; does not claim Agent 1/Agent 2 agreement; does not select a canonical MEAD; and does not decide U-15, U-14, TD-12, or TD-13. It makes no M0 claim. A2's reported arithmetic/document checks are source-reported evidence; they do not establish broker runtime behavior, and the review reports zero contract acceptance tests run.
