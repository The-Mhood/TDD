# Technical Director Addendum — Cross-Agent Integration Decisions

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Document ID:** `TDD-TD-INT-001`
**Version:** 1.1
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Decision authority:** Technical Director
**Status:** v1.1 clarifications accepted for documentation by the TD instruction. v1.0 is preserved unchanged. Agent 1/2 contract proposals and agreement are **not yet received**; packets are prepared in the accompanying documents. This addendum does not invent their agreement or freeze specific API signatures.

## 1. Purpose and history

This v1.1 addendum records the TD review clarifications to `TDD-TD-INT-001 v1.0`, makes the accepted forced-transition precedence explicit, records the exact local repository baseline, refines environment feasibility claims, reconciles C-08 against the W-M2.3 source evidence, and begins the C-01…C-07 proposal process using two separate submission packets.

**v1.0 remains unchanged** at [`TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1.md`](TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1.md). Preserve it and all Agent 1/2 specifications and archive/version histories. v1.1 supplements v1.0; it does not rewrite their historical wording.

TDD remains canonical. The four initial modules remain `TDDCore`, `TDDRuntime`, `TDDEditor`, and `TDDTests`; `TDDCore` must not depend on gameplay/world modules. Agent 2's skeleton remains separate and is not copied or adopted. No project creation, gameplay implementation, competing Core type, Unreal build or runtime claim is authorized here.

## 2. Forced-transition precedence and preserved M1 behavior

### 2.1 Complete forced-transition precedence

The accepted priority ordering is:

> **Dead (100) > Cinematic (90) > Stagger (80).**

For multiple forced targets pending during one traversal resolution, keep only the highest-priority target. Exactly one state change occurs; lower-priority forced requests are superseded/logged. The currently resolving fallback/restoration is not interleaved or abandoned; the pending forced target is applied after restoration, except for the distinct cinematic takeover path below.

### 2.2 Traversal event resolution remains Agent 1 M1 v1.4

This clarification documents, and does **not redesign**, Agent 1's accepted traversal behavior:

1. Apply health/posture through the damage pipeline independently of state/control. State resolution must not suppress otherwise-applicable health damage.
2. Classify the interrupt and apply the following established order:
   - **Lethal:** resolve fallback → run restoration → enter `Dead`. Death outranks cinematic and stagger if multiple forced targets compete.
   - **Cinematic takeover:** perform **no positional fallback**; freeze the capsule at its current pose/position, run restoration with the cinematic freeze-mode exception, then enter `Cinematic`. This outranks stagger but not `Dead`.
   - **Staggering:** resolve fallback → run restoration → enter `Stagger`. Stagger classification includes the M1 semantics (stagger-classified damage, posture break or successful parry against the victim); storage of that classification is still not prescribed as a permanent `bCausesStagger` field.
   - **Non-staggering damage:** it is an abort **request**, not a forced transition. Abort only when traversal is within its authored `AbortWindow`; otherwise traversal continues while health application remains independent.
3. For fallback-required paths, fallback finishes before restoration, and restoration finishes before a grounded/locomotion/stagger/death target is entered. The single validated transform-write path remains the only abort repositioning route.
4. Preserve M1 v1.4's two phases without alteration: the ordered relocation attempts (complete, reverse, drop-to-floor) are bounded by total per-call `MaxRelocationAttempts` clamped `[0,3]` (default 3); the terminal hold phase is unbudgeted and always runs (out-of-world first, then grounded hold, otherwise unsupported hold). Unsupported hold performs no transform write and uses `MOVE_Falling`; out-of-world is a flow-system handoff, not a placement.
5. Preserve M1 v1.4's revalidation, no-teleport/no-stale-transform-write rule, terminal resolution, movement-mode restoration, and forced-target processing. Do not alter these semantics while drafting Core/shared contracts.

**Source basis:** Agent 1 M1 Movement Specification v1.4, §3.2.1–§3.2.3, especially §3.2.2 and §3.2.2d, source commit `bb2685c605efd4958b1c67944721c77e1b393931`. These remain design rules; no implementation or runtime verification is claimed.

## 3. Verified P0 canonical repository baseline

| Field | Verified result |
|---|---|
| Canonical repository | `The-Mhood/TDD` working checkout at `/home/user/TDD`; TDD is canonical per TD decision. |
| Current session branch | `arena/c64fc525-tdd` (active; no branch switch performed). |
| Local HEAD | `1354e3d891e4964ab5ba6b8d96c29f5143520667` — `docs: record TD cross-agent integration decisions`. |
| `origin/main` | `5e3d1da4eee42ad8255760530291ff91cdfb39b2`. |
| Published canonical branch at inspection | `origin` `arena/c64fc525-tdd` = `ba5b23cb69b88da286c76ece9b06934a922c285f`; local HEAD is newer and has not been shown to be published by the remote-ref check. No push was performed. |
| Local worktree | **Not clean.** `README.md` is modified. Untracked: `docs/M0_UNREAL_FOUNDATION_CHECKLIST.md`, `docs/MASTER_ENGINEERING_ARCHITECTURE.md`, `docs/PROJECT_BOOTSTRAP_DECISION.md`, `docs/TECHNICAL_QUALITY_AND_INTEGRATION_ASSESSMENT.md`, and `docs/quality/QUALITY_LEDGER.md` (reported by directory as `docs/quality/`). `docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1.md` is tracked in local HEAD. Preserve all existing work; no reset/clean/overwrite. |
| Canonical Unreal project | **No `.uproject` found** in the canonical worktree at inspection. The tracked/untracked local content is documentation/planning, not an Unreal project. |
| M0 status | **Not passed.** No canonical Unreal project/editor/build/test evidence exists in this checkout. This baseline does not assert a project exists or that M0 has passed. |
| Agent 1 published source | `arena/3bc206a0-tdd` = `bb2685c605efd4958b1c67944721c77e1b393931` (remote ref verified). |
| Agent 2 published source | `arena/5dde91a4-tdd` = `ed36ad6d9cab946ede859e0dd1000a480b114f91` (remote ref verified). |
| Agent-branch separation | Both agent commit IDs are separate from/not ancestors of canonical local HEAD; no agent branch was checked out, merged or copied. Their files remain source material for review only. |

The baseline describes the actual **local** branch/worktree state, including dirty documentation. It is not a clean-release baseline. Keep the existing unrelated work and historical documents intact.

## 4. Environment feasibility assessment

The separate [`Environment Feasibility Assessment v1`](ENVIRONMENT_FEASIBILITY_ASSESSMENT_V1.md) records all required dimensions: intended editor host; host OS/hardware; candidate target; engine distribution/version; compiler/SDK; plugin compatibility; and actual availability/access.

The limited Linux check found only agent-workspace facts: host `Linux x86_64`, kernel `6.1.158+`, 2 visible CPUs, about 3.85 GiB available memory, `g++ 12.2.0` and Python 3.11.2; `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh`, `dotnet`, `clang++` and `clang` were not found on `PATH` or in the specified common roots to depth 4. This establishes only that the **inspected agent workspace** could not run UE checks. It does **not** establish UE availability or absence on any production workstation.

**Recommendation:** do not select UE 5.8 or any other version without compatibility evidence. The intended editor host, target platform, version/distribution, compiler/SDK and plugin set are unknown. Select and pin an exact UE release only after checking it on the named production host against the target platform and plugin requirements, then opening/building/running the project-owned M0 test. Exact engine/toolchain choices remain open TD decisions.

## 5. Agent 1 and Agent 2 contract submission process

### 5.1 Prepared packets and current status

- [Agent 1 Contract Submission Packet](AGENT1_CONTRACT_SUBMISSION_PACKET_V1.md) — asks Agent 1 for executable/player-side requirements across C-01…C-07.
- [Agent 2 Contract Submission Packet](AGENT2_CONTRACT_SUBMISSION_PACKET_V1.md) — asks Agent 2 for actual world-side requirements across the same contracts.

These are **prepared request packets**, not evidence that a message was sent to an external agent or that a response was received. No agent-control/submission channel is available in this repository session. Current response status for C-01…C-07 is `AWAITING AGENT SUBMISSION`; do not record agreement for either agent until the agent provides its proposal and the counterpart signs it.

### 5.2 Submission and consolidation gates

For every C-01…C-07 proposal, the submitting owner must supply all of:

1. Publisher.
2. Implementation owner.
3. Named consumers.
4. Lifetime and validity rules (including world/streaming/actor destruction, time/clock and stale data as applicable).
5. Mutation authority and explicitly read-only surfaces.
6. Proposal status and version; unresolved alternatives and compatibility impact.
7. Named acceptance tests with measurable assertions and test-layer designation; proposed names are not evidence tests already exist or passed.

Agent 1 must specify its executable/player-side requirements. Agent 2 must specify the actual world-side requirements and payloads it will author/consume. The producer and at least one named consumer (all affected consumers for a breaking/shared contract) must independently acknowledge the same proposal. Agent 3 consolidates only after both sides' positions and any disagreement are recorded; the consolidated contract then goes to the Technical Director for explicit acceptance. No contract is frozen by these packets or by default.

## 6. Updated C-01–C-10 agreement and blocker register

| ID | Contract / decision | Required submissions or evidence | Current agreement/status | Unresolved conflict / blocker | Closure condition |
|---|---|---|---|---|---|
| **C-01** | Traversal vocabulary, route IDs, markers, query and failure semantics | A1: executable action set, required candidate fields, query parameters/results, player-side failure/abort semantics. A2: actual route IDs, marker representation, authored requirements, streaming/content validity and reachability use. | **AWAITING A1 + A2 proposals.** Ownership split is accepted; concrete API is not. | Capability names; stable route ID; tag/data/code requirements; marker lifetime; query ordering; no-candidate/invalid/unsupported/blocked/unloaded result meanings. | Both sides complete packet fields, producer/consumer agreement, named tests; TD signs consolidated version. Preserve M1 v1.4 semantics. |
| **C-02** | Read-only player context and locomotion/action/combat snapshots | A1: field-by-field player provider/snapshot, units/coordinate frame, cadence, validity, transition/event semantics. A2: each world-side field actually consumed and why, required freshness/null behavior. | **AWAITING A1 + A2 proposals.** Separate state concepts and A1 mutation authority accepted. | Snapshot type/fields; actor handle policy; event vs query; target/stealth/noise inclusion; update/lifetime semantics. | Producer and consumer agree on minimal read-only surface and tests for immutability, freshness and invalid lifetime; TD acceptance. |
| **C-03** | Damage request, hit-resolution result, damage application and applied event | A1: single resolution/application flow, request/result semantics, dedupe/transaction rules and event timing. A2: actual world enemy/boss response facts required from the result/event; no duplicate damage path. | **AWAITING A1 + A2 proposals.** A1 arbitration/application ownership; Core event publication accepted. | Local transient actor refs vs durable stable IDs; distinguish hit-resolution from applied damage; payload/identity and duplicate policy. | Both sides trace one hit from intent through exactly-once application/event; named tests; TD accepts Core contract. |
| **C-04** | Stagger classification and precedence | A1: semantic classification inputs and exact state/fallback outcomes, storage alternatives (no assumed permanent `bCausesStagger`). A2: world consumer response to resulting state/event, not an independent classifier. | **AWAITING A1 + A2 proposals.** Precedence accepted: Dead > Cinematic > Stagger. M1 v1.4 damage/AbortWindow behavior retained. | Classification representation; event timing; posture/parry promotion mapping; integration with simultaneous pending forced targets. | Producer/consumer agree on decision table and acceptance tests including simultaneous targets, health independence, non-stagger damage inside/outside AbortWindow; TD acceptance. |
| **C-05** | Telegraph timing, identity, cancellation and clock semantics | A1: parry/block consumer expectations, gameplay-time/window boundaries, pause/time-dilation behavior, missed/late event handling. A2: actual enemy producer lifecycle/IDs/update/cancel and scheduling needs. | **AWAITING A1 + A2 proposals.** Shared stream required; neither stream nor clock is frozen. | Event IDs, producer authority, gameplay clock, pause, updates, cancel, target/area, ordering, world unload and late subscribers. | Shared event timeline/lifecycle plus named deterministic tests and two-party agreement; TD acceptance. |
| **C-06** | One interaction lifecycle | A1: player-side focus/input/tap/hold/progress/cancel/verb-to-animation requirements. A2: world actor prompt/eligibility/requirements/location/action/completion behavior. | **AWAITING A1 + A2 proposals.** Core owns lifecycle; A1 router and A2 implementations accepted. | Method/event shapes; hold progress authority; location/requirements ownership; cancellation and completion exactly-once semantics; progress grant boundary. | Both sides sign sequence and lifecycle cases; named tests for tap/hold/cancel/unload/duplicate; TD accepts one Core contract. |
| **C-07** | Shared IDs and Gameplay Tag ownership | A1: player/combat/traversal IDs and tags needed. A2: route/location/scene/interactable/world data identifiers and tags needed. | **AWAITING A1 + A2 inventories.** Agent 3/TD registry/governance ownership accepted. | Stable entity vs content IDs; typed wrappers vs registry; route namespace; tag lifecycle; save compatibility/retirement policy. | Consolidated registry policy plus cross-agent requested vocabulary and duplicate/unknown/retired reference tests; TD acceptance. |
| **C-08** | W-M2.3 bounded-class/count reconciliation | Independently compare W-M2.3 commit's exact verbatim fixture rows with sensitivity and budget evidence. | **RECONCILED / CLOSED FOR THE STATED COUNT.** Exact rows below show 29 exact, 5 bounded, 1 unbounded, 11 uncaptured = 46. The TD's earlier “6 bounded” figure differs by one; source evidence supports 5. | Does not close C-09's unbounded source content, nor turn projections into measurements. | Reconciliation recorded in §7; no change to Agent 2 historical documents required. If the authoritative Drive register changes, rerun against its new version. |
| **C-09** | `CH01-SCN-014` unbounded population prose | Creative Director reviews source wording and chooses whether to amend the authoritative register, accept the open upper bound, or direct an approved capture/ruling. | **OPEN — CREATIVE DIRECTOR DECISION.** | Register says collective “A line of women and girls…” with no numeral/bound. Do not infer or invent a count. | CD records decision and, only if needed, updates authoritative source/version. Until then band remains open and upper endpoint is a floor. |
| **C-10** | Environment/toolchain feasibility and M0 entry | Identify intended Editor host, OS/hardware, candidate target, engine distribution/version, compiler/SDK, plugin set and actual access; obtain TD project-creation authorization separately. | **ASSESSMENT DOCUMENTED FOR AGENT WORKSPACE ONLY; PRODUCTION HOST UNKNOWN.** M0 not passed; project creation not authorized. | Exact UE release and target/toolchain are unselected; no evidence of production workstation availability. | Named host inventory and compatibility spike; exact version pin and M0 entry authorization, then real project/open/build/automation evidence. |

### 6.1 C-08 exact W-M2.3 source-row reconciliation

**Reviewed source identity:** Agent 2 `arena/5dde91a4-tdd` HEAD `ed36ad6d9cab946ede859e0dd1000a480b114f91`; W-M2.3 document `Docs/W2M3_CORRECTION.md`; verbatim scene source fixture `Tools/canon/tests/fixtures/scene_register_ch01_v19_verbatim.md`; generated source evidence `Docs/evidence/agent2/CH01_population_sensitivity.json` and `Docs/evidence/agent2/CH01_population_budget.json`.

Direct row comparison yields:

| Class | Exact rows / basis | Count |
|---|---|---:|
| Exact register head-count | W-M2.3 sensitivity evidence: `scenes_with_register_npc_data = 29`; the corrected `CH01-SCN-018` wording is “A dozen people.” = exactly 12. | 29 |
| Bounded, not exact | `CH01-SCN-005` “Sometimes one cook.” `[0,1]`; `CH01-SCN-017` “Six to ten adults; Unoka (storyteller) some days.” `[6,10]`; `CH01-SCN-020` “Four or five men.” `[4,5]`; `CH01-SCN-021` “Occasional passer-by.” `[0,1]`; `CH01-SCN-034` “Sometimes a traveller.” `[0,1]`. | 5 |
| Unbounded | `CH01-SCN-014` “A line of women and girls filling pots and lifting them onto head-pads, talking.” No numeral or bound. | 1 |
| Uncaptured | `scenes_without_any_capture = 11`; absence of detail is not a zero count. | 11 |
| **Total** | `29 + 5 + 1 + 11` | **46** |

The six `unresolved_detail` rows are five bounded plus `CH01-SCN-014` open; the budget evidence separately reports `scenes_with_stated_bounds = 5` and the open row list containing only `CH01-SCN-014`. Thus W-M2.3's actual class is **5 bounded**, not 6; the supplied classification totals 46. **Verification result:** the exact 5-row classification reconciles with the verbatim fixture and the two generated JSON artifacts. This is source-data reconciliation, not an engine test or measurement. Cost/performance figures remain projections.

## 7. M0 preparation remains in force

Continue documentation and feasibility work without creating a project. The existing [M0 evidence checklist](M0_UNREAL_FOUNDATION_CHECKLIST.md) remains the detailed standard. Next preparation order:

1. Preserve and report the P0 repository baseline in §3; keep agent refs separate.
2. Have TD/project owner identify intended Editor host, target platform, toolchain/access and plugin requirements; complete the environment inventory.
3. Receive A1/A2 C-01…C-07 submissions and consumer signatures; consolidate and obtain explicit TD approval before anyone implements those shared interfaces.
4. Keep C-09 open for CD and track C-08 as source-reconciled; keep all population/performance figures explicitly projected until engine captures exist.
5. Obtain separate explicit M0 project-creation authorization and canonical path. Only then may the authorized owner prepare the four-module Unreal foundation; do not copy Agent 2's skeleton.
6. Pass M0 only with real Editor open/reopen, successful clean build, meaningful project-owned Unreal Automation Test and captured evidence tied to a single project commit/toolchain.

## 8. Changes in v1.1

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Original accepted architecture addendum; preserved unchanged. |
| 1.1 | 2026-11-16 | Clarified Dead > Cinematic > Stagger and retained all M1 v1.4 semantics; qualified toolchain findings to inspected sandbox; recorded verified P0 branch/HEAD/dirty state and agent separation; prepared A1/A2 C-01…C-07 packets; reconciled C-08 to exact W-M2.3 rows; kept C-09 open; expanded C-10 environment/M0 status. |

**No gameplay implementation, project creation, skeleton copying, Core type creation, Unreal build or runtime claim is included in v1.1.**
