# Technical Director Addendum — Cross-Agent Integration Decisions

**Document ID:** `TDD-TD-INT-001` · **Version:** 1.2
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Branch:** `arena/c64fc525-tdd`
**Governing baseline:** v1.1 at published commit `50b14318c8089dedcc688fb2c78ad3cb361c15f5`
**Status:** Documentation/coordination only. Agent 1/2 response records explicitly remain `AWAITING SUBMISSION`; no contract agreement or frozen API is claimed. v1.0 and v1.1 remain unchanged.

## 1. Change from v1.1

This v1.2 integration addendum records the start of the response-tracking phase, separate copy-ready Agent 1 and Agent 2 request messages, current delivery/response limitations, per-contract status/dependencies, and the next Technical Director decisions. It does not reclassify historical source documents as current packet responses.

- [Agent 1 Contract Responses v1](AGENT1_CONTRACT_RESPONSES_V1.md) — awaiting submission; contains prepared message, not sent.
- [Agent 2 Contract Responses v1](AGENT2_CONTRACT_RESPONSES_V1.md) — awaiting submission; contains prepared message, not sent.
- [Cross-Agent Contract Reconciliation v1](CROSS_AGENT_CONTRACT_RECONCILIATION_V1.md) — comparison and prior source-shape differences; no agreement claimed.
- [Environment Feasibility Assessment v1](ENVIRONMENT_FEASIBILITY_ASSESSMENT_V1.md) — unchanged; no new production-host/toolchain evidence was obtained in this assignment.

## 2. Baseline and existing work

- Canonical repository: `The-Mhood/TDD`; current branch is `arena/c64fc525-tdd`.
- Assignment starting HEAD: `50b14318c8089dedcc688fb2c78ad3cb361c15f5`; starting worktree was clean.
- Exact Agent 1 packet: [at baseline commit](https://github.com/The-Mhood/TDD/blob/50b14318c8089dedcc688fb2c78ad3cb361c15f5/docs/AGENT1_CONTRACT_SUBMISSION_PACKET_V1.md).
- Exact Agent 2 packet: [at baseline commit](https://github.com/The-Mhood/TDD/blob/50b14318c8089dedcc688fb2c78ad3cb361c15f5/docs/AGENT2_CONTRACT_SUBMISSION_PACKET_V1.md).
- Agent 1 source branch/ref checked: `arena/3bc206a0-tdd`, `bb2685c605efd4958b1c67944721c77e1b393931`.
- Agent 2 source branch/ref checked: `arena/5dde91a4-tdd`, `ed36ad6d9cab946ede859e0dd1000a480b114f91`.
- Agent branches remain separate; no branch was checked out, merged or copied. No `.uproject`, Source, Config or Content foundation was created. No gameplay/Core implementation was made.

## 3. Agent contact and response status

### Agent 1

- Packet: published at the exact URL above.
- Direct agent dispatch: **not available in the tools exposed in this session**.
- Delivery: **NOT DELIVERED** through a direct channel; canonical publication is not proof of receipt.
- Prepared request: copy-ready message is in `AGENT1_CONTRACT_RESPONSES_V1.md`.
- Requested response deadline: **2026-11-18 17:00 UTC**; ask Agent 1 for a revised ETA if unavailable. This is a requested deadline, not an agent commitment.
- Response: **AWAITING SUBMISSION** for C-01…C-07.

### Agent 2

- Packet: published at the exact URL above.
- Direct agent dispatch: **not available in the tools exposed in this session**.
- Delivery: **NOT DELIVERED** through a direct channel; canonical publication is not proof of receipt.
- Prepared request: copy-ready message is in `AGENT2_CONTRACT_RESPONSES_V1.md`.
- Requested response deadline: **2026-11-18 17:00 UTC**; ask Agent 2 for a revised ETA if unavailable. This is a requested deadline, not an agent commitment.
- Response: **AWAITING SUBMISSION** for C-01…C-07.

No response, receipt, producer/consumer sign-off, disagreement outcome or agreement is invented. Historical branch documents are traceable input only; not packet responses.

## 4. Updated C-01–C-10 response, agreement and blocker register

| ID | Status | Agent 1 response / role | Agent 2 response / role | Producer-consumer agreement | Dependencies / blockers / next action |
|---|---|---|---|---|---|
| **C-01 Traversal** | **AWAITING SUBMISSION** from both. | Propose executable action vocabulary, player query inputs/results, failures/interruption and required candidate fields. | Propose authored route IDs, markers, world requirements, streaming validity and reachability needs. | None; same-version review not received. Prior source docs show open enum/data/failure questions only. | Depends on C-02 context and C-07 route/tag identity (confirm with agents); M1 v1.4 behavior stays unchanged. Obtain both proposals, then compare no-candidate/invalid/unsupported/blocked/unloaded semantics. |
| **C-02 Player context/states** | **AWAITING SUBMISSION** from both. | Propose authoritative Agent 1 read-only provider; separate locomotion/action-control/combat snapshots, lifetimes and validity. | Name actual world fields consumed and each consumer/use case, freshness and missing-player behavior. | None; no field-level consumer review. | May use C-07 IDs/tags. Obtain minimal field lists; preserve Agent 1 mutation authority and read-only Agent 2 boundary. |
| **C-03 Damage** | **AWAITING SUBMISSION** from both. | Propose single hit/damage authority, request/result/application/event lifecycle, identity and dedupe semantics. | Specify enemy/boss facts required and reactions; no independent damage application. | None; prior source shapes differ (`FTDDDamageAppliedEvent` value IDs vs `FTDDHitEvent` weak actors). | C-07 stable identity and C-04 classification may interact. Separate transient result vs applied event only if both proposals support it; TD decides unresolved payload. |
| **C-04 Stagger** | **AWAITING SUBMISSION** from both. | Propose classification alternatives and player transition semantics; no permanent `bCausesStagger` assumption. | Specify world reaction to resulting state/event only. | None; high-level authority/precedence already accepted, API not. | Depends on C-03 result and parry outcome from C-05. Preserve **Dead > Cinematic > Stagger**, health independence, M1 damage/AbortWindow/fallback/restoration. |
| **C-05 Telegraph** | **AWAITING SUBMISSION** from both. | Propose parry/block consumer timing and invalidation expectations. | Propose actual enemy telegraph producer lifecycle, IDs, clock and cancellation. | None; no shared timeline/clock. | Depends on C-07 IDs and separation from C-03 hit resolution. Require a common event timeline, pause/time dilation, open/close/cancel and world-unload rules. |
| **C-06 Interaction** | **AWAITING SUBMISSION** from both. | Propose player focus/input/routing/tap-hold/progress/cancel/completion. | Propose actual world interactable prompt/eligibility/verb/requirements/location/action/completion. | None; prior source signatures/lifecycles conflict. | Depends on C-02 player context and C-07 IDs/tags. Require a shared sequence, cancellation matrix and progress-grant boundary before TD review. |
| **C-07 IDs/Tags** | **AWAITING SUBMISSION** from both. | Inventory player/combat/traversal identity and tags plus stability/persistence needs. | Inventory authored world/content IDs/tags and source versions/validation. | None; prior materials use distinct `FGuid`, typed ID and `FName` shapes. | Foundational input to C-01/02/03/05/06. Agent 3/TD owns one Core registry/policy; compare before selecting representation. |
| **C-08 Population classification** | **RECONCILED / CLOSED for reported classification.** | — | W-M2.3 source evidence retained. | 29 exact / 5 bounded / 1 unbounded / 11 uncaptured = 46. | Exact fixture and evidence paths are in §6; all counts remain register-derived, not measured. |
| **C-09 `CH01-SCN-014`** | **OPEN — Creative Director.** | — | Existing source says an unnumbered collective. | No numerical bound. | CD to decide whether to amend authoritative register or accept the open term. No number may be inferred or invented. |
| **C-10 Environment/M0** | **PREPARATION ONLY; production host unknown.** | — | — | No environment/toolchain selection or M0 pass. | Need intended Editor host, OS/hardware, target, exact UE distribution/version, compiler/SDK, plugin compatibility and actual access. Keep version unselected until compatible evidence exists. No project creation authorized. |

### 4.1 Required response metadata

Each Agent 1 and Agent 2 submission must identify for every C-01…C-07: (1) contract ID/version, (2) publisher, (3) implementation owner, (4) named producers/consumers, (5) lifetime/validity, (6) mutation authority/read-only surfaces, (7) proposal status/unresolved alternatives, (8) named acceptance tests with measurable assertions, and (9) dependencies/compatibility concerns.

Producer and consumer agreement is tracked independently. Both must review and explicitly sign the **same proposal version**. Only then may Agent 3 prepare a consolidated, non-frozen proposal for explicit TD review. Any difference remains visible in the reconciliation register.

## 5. C-08 source/evidence references retained

The reconciled classification remains **29 exact / 5 bounded / 1 unbounded / 11 uncaptured / 46 total**. The previous W-M2.3 source-row verification is retained against Agent 2 commit `ed36ad6d9cab946ede859e0dd1000a480b114f91`:

- Verbatim source fixture: `Tools/canon/tests/fixtures/scene_register_ch01_v19_verbatim.md` (scene register v1.9).
- Generated sensitivity evidence: `Docs/evidence/agent2/CH01_population_sensitivity.json`.
- Generated population-budget evidence: `Docs/evidence/agent2/CH01_population_budget.json`.
- Correction/report: `Docs/W2M3_CORRECTION.md` and `Docs/POPULATION_SENSITIVITY_REPORT.md`.
- W-M2.3 evidence run: `Docs/evidence/agent2/W-M2.3_evidence.json`.
- Bounded rows: SCN-005 `[0,1]`; SCN-017 `[6,10]`; SCN-020 `[4,5]`; SCN-021 `[0,1]`; SCN-034 `[0,1]`.
- Unbounded row: SCN-014, no numeral or bound. `CH01-SCN-018` “A dozen people” is exact 12, not bounded.

No register or evidence artifact was modified. These are data reconciliation and Python evidence only, not runtime/performance measurements.

## 6. C-10 environment and M0 dependencies

The environment assessment is unchanged because no new production-host information was obtained. The Linux inventory remains limited to the inspected agent workspace; it says nothing about production workstation availability. Keep the exact UE version/distribution unselected until the intended host, target, compiler/SDK and plugin compatibility can be checked.

M0 remains preparation-only. No project creation/copy, `.uproject`, Source, Config, Content, Core implementation, gameplay implementation, Unreal build/runtime test or M0 pass is authorized or claimed. The four-module topology and existing M0 evidence criteria remain governing.

## 7. Technical Director decisions / coordination needed

1. **Dispatch path:** if direct agent assignment is expected, identify/provide the supported dispatch channel or ask the agents to monitor the published canonical packet URLs. Until then, the copy-ready requests in the response records remain unsent.
2. **Response deadline:** confirm or adjust the requested `2026-11-18 17:00 UTC` deadline, or request each agent's ETA. No agent has accepted it yet.
3. **After submission:** review only the contracts with both sides' exact-version responses; decide unresolved compatibility choices in C-01…C-07 after their producer/consumer positions are recorded. No signature, enum, struct, delegate, tag or Core API is frozen now.
4. **C-09:** Creative Director decision remains required for `CH01-SCN-014`.
5. **C-10:** production host/target/toolchain/access inventory and exact-version compatibility evidence are required before M0 can begin. Project creation requires its separate explicit authorization.

## 8. Change history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Original accepted integration architecture; unchanged. |
| 1.1 | 2026-11-16 | Precedence, P0 baseline, environment scope, packets and W-M2.3 row reconciliation; unchanged. |
| 1.2 | 2026-11-16 | Added per-agent awaiting-submission records, copy-ready unsent requests/deadlines, C-01…C-07 comparison and independent agreement statuses, C-01…C-10 blocker register and current M0/dispatch dependencies. |

**This document is a coordination/status package, not an implementation-ready or frozen API.**
