# Cross-Agent Contract Reconciliation — C-01 through C-07

**Document:** `TDD-INT-RECON-001` · **Version:** 3.0
**Date:** 2026-11-17 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Governing decisions:** `TDD-TD-INT-001 v1.2`, commit [`e121bbbf09562e3cba0efe81aad971809685db23`](https://github.com/The-Mhood/TDD/blob/e121bbbf09562e3cba0efe81aad971809685db23/docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md)
**Status:** Documentation/reconciliation only. All seven contracts remain **DESIGN_ONLY / PROPOSED — NOT FROZEN**. No contract is bilaterally agreed. No API, Core/C++ implementation, `.uproject`, merge, or M0 claim is authorized here.

## 1. Purpose, pinned sources, and rules of interpretation

This version reconciles A1-R2 against A2's formal review of that exact response, carries forward TD v1.2 and reconciliation v2 without overwriting either, and records the independent read-only comparison of the three MEAD documents.

| Record | Exact source | Identity / role |
|---|---|---|
| Agent 1 submission | [`f578fe612ad173b74f99fcb187f825eb3de6f59a`](https://github.com/The-Mhood/TDD/blob/f578fe612ad173b74f99fcb187f825eb3de6f59a/docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md) | `A1-R2` v1.1; exact proposal being reviewed |
| Agent 2 formal review | [`4220b82ffdebf291793ce508dd25080528a3dac8`](https://github.com/The-Mhood/TDD/blob/4220b82ffdebf291793ce508dd25080528a3dac8/Docs/AGENT2_REVIEW_A1R2_V1.md) | `TDD-A2-REVIEW-A1R2-001` v1.0; review of the A1 source above |
| TD decisions | [`e121bbbf09562e3cba0efe81aad971809685db23`](https://github.com/The-Mhood/TDD/blob/e121bbbf09562e3cba0efe81aad971809685db23/docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md) | `TDD-TD-INT-001` v1.2 |
| Previous reconciliation | [`d32660fee1b0234871b39b9fa56677c7cf62f28f`](https://github.com/The-Mhood/TDD/blob/d32660fee1b0234871b39b9fa56677c7cf62f28f/docs/CROSS_AGENT_CONTRACT_RECONCILIATION_V2.md) | `TDD-INT-RECON-001` v2.0; preserved historical record |

**No inferred agreement.** A2's clause-level acceptance, “no remaining technical objection,” willingness to sign, or compatibility with A1 is not an executed same-version signature. In particular C-02, C-03, and C-06 are **not agreed**: A2 explicitly says it did not sign them in the review, and no explicit A1 counter-signature to this A2 review exists. Any agreement must identify the same exact version and clauses for both agents. Silence, related earlier documents, parallel wording, or this reconciliation do not substitute for signatures.

The following distinctions are maintained throughout:

- A **review verdict** reports A2's assessment of A1-R2; it is not a bilateral status or TD ruling.
- An **agent proposal** remains proposed until the other agent explicitly approves the same version and any required TD/design/registry decision is made.
- A **TD question** stays open unless TD issues a decision. Recommendation is not adoption.
- Historical documents and all MEAD files remain unmodified. This version adds no contract semantics by implication.

## 2. Executive status

A2 reports 61 clause verdicts: **56 accepted, 5 accepted with condition, 0 rejected**. At the contract level, A2 records C-01 agree with a condition; C-02 agree in substance; C-03 agree in substance; C-04 agree with a condition; C-05 partial agreement; C-06 agree in substance; C-07 clarification required. A2's own headline correctly reports **0/7 contracts agreed/signed**. This reconciliation retains that 0/7 position.

| Contract | A2 review of A1-R2 (review verdict only) | Remaining substance / dependency | Bilateral status here |
|---|---|---|---|
| C-01 Traversal and route identity | Agree with condition | A1 P3 “permanent, never reused after retirement” conflicts with §10.4 rename-without-migration; A1 must give exact replacement or explain TD-04-dependent save policy. | `RECONCILIATION IN PROGRESS` |
| C-02 Player context | Agree in substance; no technical objection | A2 says it would sign but did not sign; both agents must explicitly confirm this exact A1-R2 version. | `RECONCILIATION IN PROGRESS` |
| C-03 Hit/damage | Agree in substance; no technical objection | A2 says it would sign but did not sign; TD-03 and explicit same-version signatures remain. TD-09 document erratum also remains. | `RECONCILIATION IN PROGRESS` |
| C-04 Stagger / forced-state classification | Agree with condition | Missing `Status.Dead`/equivalent; six MEAD-C status tags absent from A1-R2's inventory need explicit retain/omit/withdraw disposition and registry owner. | `TD REVIEW REQUIRED` |
| C-05 Telegraph / gameplay clock | Partial agreement | A2 withdraws its undilated-window rule; the per-entity clock still fails under asymmetric dilation. Need an axis/conversion decision and behavior when dilation changes mid-window. | `TD REVIEW REQUIRED` |
| C-06 Interaction | Agree in substance; no technical objection | A2 says it would sign but did not sign; exact version signatures still absent. Damage interrupt remains design-escalated, not decided. | `RECONCILIATION IN PROGRESS` |
| C-07 IDs, tags, registry and persistence | Clarification required | Three distinct MEAD documents, no canonical declaration; no registry owner; TD-13 save/consumer inventory and interactable persistence unresolved. | `TD REVIEW REQUIRED` |

These status labels are process state, not approval. None is `AGREED BY BOTH — PENDING TD` or `FROZEN`.

A2's five withdrawals are preserved as A2-attributed review positions, not independently validated policy: (1) undilated parry-window rule; (2) `CarryState`; (3) invented `Combat.Damage.Root` / `.Thunder`; (4) duplicative `Combat.State` / `Interaction.Mode` / `Traversal.State` / `Telegraph.Cancel`; and (5) `CameraForward`. They do not create tags, namespaces, or implementation requirements here.

## 3. C-01…C-07 clause-level reconciliation

### C-01 — Traversal vocabulary, route query, and route identity

**A1-R2 proposal:** A1 revises the example route-key format to format-agnostic properties P1–P5, accepts A2's location-anchored key form as conforming, requires parent validation by the register's multi-valued `Category` containing `Traversal Area`, and defines five grounded capabilities, data-driven AND/OR requirements, independent set membership, per-query revocation, and a total world-facing projection of its seven query outcomes. A1 P3 currently says a key is permanent and never reused after retirement. A1 §10.4 also says a route key may be renamed per level edit without migration when no save references a route key.

**A2 review verdict:** Agree with condition. A2 identifies the P3/§10.4 internal contradiction and proposes: “A route key is stable for the lifetime of the content it names. It is never reused for different content while referenced by any save, log or telemetry entry. Whether a retired key must be tombstoned depends on whether a save references route keys, which is TD-04's question and not a C-01 property.” A2 says original P3 would be appropriate if TD-04 establishes that saves reference route keys. This is A2's proposed replacement, not adopted text.

**Reconciliation:** P1/P2/P4/P5, the location-anchored shape, category-based semantic validation, capability model, and projection are accepted by A2 at clause level according to its review. P3 is not reconciled. A1 must either accept/counter the exact proposed revision and amend A1-R2 in a new version, or explain how both existing sentences can coexist. TD-04 must settle whether route keys are persisted before a retirement/tombstone guarantee is selected. Preserve the distinction between a syntactic key check and semantic parent lookup; no prefix-only rule and no invented ID family.

**Review verdict:** `AGREE WITH CONDITION` (A2). **Joint status:** `RECONCILIATION IN PROGRESS`.

### C-02 — Read-only player context and snapshots

**A1-R2 proposal:** Retains A1-authored, read-only player context, revises field choices in response to earlier input, removes health/posture, accepts `bInCombat` and `CameraForward`, distinguishes `AimDirection`, and declines to invent `CarryState` without an approved carry system/use case. Freshness and invalidity rules remain proposals.

**A2 review verdict:** “Agree” in substance, no blocking condition. A2 withdraws `CarryState`, accepts the health removal and the `bInCombat`/`CameraForward` changes, and states it has no remaining technical objection. A2 explicitly does **not** sign C-02 in the review, which says a review is not the requested signature.

**Reconciliation:** No substantive disagreement is identified by A2, but there is no same-version bilateral confirmation. Preserve A1 as sole player-state mutator. Do not call C-02 agreed until both agents explicitly confirm A1-R2 v1.1 (or a named successor) and its field/freshness clauses. No C++ shape or API is frozen.

**Review verdict:** `AGREE IN SUBSTANCE` (A2; not signed). **Joint status:** `RECONCILIATION IN PROGRESS`.

### C-03 — Hit arbitration, damage application, and applied event

**A1-R2 proposal:** Separates transient hit handling from the applied-damage fact, proposes request/event identities and dedupe, assigns A1 as sole publisher of the applied-event stream, and defines event inclusion/exclusion cases and target-unload handling. A1 states A1 exclusively owns hit detection/arbitration/defence evaluation for hits involving the player; target owners apply health/attributes, and Agent 2 supplies enemy intent and consumes outcomes. A1's player-victim ownership claim does not authorize an enemy-side second arbiter.

**A2 review verdict:** “Agree” in substance. A2 confirms exclusive A1 arbitration, defence evaluation and mitigation for player-victim hits; accepts one applied-event stream for applied, blocked and parried hits; and accepts no event for miss, immune, rejected, duplicate or out-of-window requests. A2 raises an exact ambiguity in MEAD-C §5.4: `OutcomeType` appears as `FTDDDamageRequest` input and the diagram does not mark the arbitration boundary. It accepts A1's six-role separation but requests a TD-09 erratum (see §6). A2 says it would sign C-03 but did not sign; TD-03 still needs its designated ruling on blocked/parried event scope.

**Reconciliation:** The role boundary is directionally clear in A1-R2 and explicitly accepted as a review position by A2, but C-03 is not bilaterally agreed. Retain A1 sole publisher, single applied-event stream, and the source-reported event matrix as proposals pending exact signatures and TD-03. No MEAD amendment is effected by this ledger; the TD-09 request is set out separately.

**Review verdict:** `AGREE IN SUBSTANCE` (A2; not signed). **Joint status:** `RECONCILIATION IN PROGRESS`.

### C-04 — Stagger classification, forced-state precedence, recovery notice

**A1-R2 proposal:** Preserves `Dead > Cinematic > Stagger`, keeps health/application separate from control-state resolution, states a preferred `ETDDStaggerClass` representation with fallback alternatives, and proposes `FTDDRecoveryCompletedEvent` as a notification only. A1-R2 does not include `Status.Dead`/`Status.Died` in the MEAD-linked tag inventory.

**A2 review verdict:** Agree with condition. A2 accepts the C-04 semantics and recovery notification at clause level but identifies that MEAD-C's seven fixed status tags include `Status.Cinematic` and `Status.Staggered`, not `Status.Dead`. A2 also lists six omitted MEAD-C tags from A1-R2's inventory: `Status.Cinematic`, `Status.Attacking`, `Status.Blocking`, `Status.Parrying`, `Status.Invulnerable`, and `Status.Grabbed`. Together with `Status.Staggered` these are MEAD-C's seven; the six-item list is the set A2 says is missing from A1-R2's inventory. A2 requests registry clarification and does not invent a tag.

**Reconciliation:** Before C-04 can advance, A1 must state whether each of the six omitted tags is retained by the MEAD candidate, merely omitted from a dispute-focused table, or withdrawn; TD/registry owner must identify `Status.Dead` or a named equivalent if the precedence rule is to be represented in tags. Do not add/register a tag here. Preserve precedence and notification-only semantics; no independent state authority is created. C-07 / TD-08 governs vocabulary/registry resolution.

**Review verdict:** `AGREE WITH CONDITION` (A2). **Joint status:** `TD REVIEW REQUIRED`.

### C-05 — Telegraph lifecycle and cross-entity time

**A1-R2 proposal:** Defines a proposed Core-owned gameplay-time subsystem and a per-entity scaled accumulation `T_e(n) = T_e(n-1) + DeltaWorldSeconds * PrimaryDilation * CustomDilation(e)`. It states pair-hitstop dilates both participants identically and parry is evaluated by same-frame phase overlap rather than timestamp subtraction. A2's earlier undilated-window rule is expressly withdrawn in A2's review.

**A2 review verdict:** Partial agreement. A2 accepts the scaled-window direction and withdraws its earlier undilated-window rule because it conflicts with the pair-hitstop/montage timing described in MEAD-C §5.5. A2 demonstrates that `T_attacker` and `T_defender` cease to be comparable when custom dilation differs (e.g. staggered enemy at 0.05, player at 1.0), and proposes two fixes without selecting one: (A) timestamp on a shared world-accumulated axis with `PrimaryDilation` applied but producer `CustomDilation` excluded, plus producer factor on message; consumer converts remaining montage time using that factor; or (B) publish both scaled/unscaled axes and factor. A2 also requires parry phase overlap, not timestamp subtraction, in contract wording.

**Unresolved mid-window case:** Neither A1-R2's formula nor A2's two options, as stated, defines how an already-open telegraph behaves when `CustomDilation(producer)` changes after start (or when the relevant primary factor changes). An instantaneous producer factor cannot by itself reconstruct elapsed scaled time across prior factor values. Before signature, define whether the contract uses (i) a piecewise-integrated clock/history and segment boundary updates, (ii) a fixed factor captured at telegraph start with changes deferred until close, or another explicit method. Define endpoints/remaining time and consumer behavior at each dilation-change boundary. This reconciliation does not choose a timing model or claim the proposed arithmetic has been tested.

**Reconciliation:** Keep the four-message lifecycle, exactly-once close, pause/dilation/hitstop intent, and phase-overlap rule as proposals. TD-06 must select/approve a cross-entity comparable time coordinate and specify mid-window dilation changes; A1 must amend its proposal and A2 must explicitly approve the resulting exact text. Late-subscriber event/query surface also remains a TD question in A1-R2/A2 review.

**Review verdict:** `PARTIALLY AGREE` (A2). **Joint status:** `TD REVIEW REQUIRED`.

### C-06 — Interaction lifecycle and progress

**A1-R2 proposal:** Router owns hold duration, progress integration and completion instant; progress callbacks are opt-in via `bWantsProgress`; world interactables report completion but do not grant progression. A1 proposes damage interruption as a design position while explicitly escalating the choice rather than treating it as a ruling.

**A2 review verdict:** “Agree” in substance. A2 accepts `bWantsProgress`, exactly-once lifecycle expectations, target stream-out/destruction cancellation, level-transition cleanup, and progression grant ownership by the relevant subsystem, while stating damage interruption is a preference/design question and not relied on by its contract. A2 explicitly says it would sign but does **not** sign C-06 in the review.

**Reconciliation:** No technical objection remains in A2's review, but no bilateral same-version signature exists. Do not infer agreement. Preserve damage-interrupts-hold as unresolved TD/design decision; do not assume `Cancel(Damaged)` is guaranteed. Preserve report-vs-grant separation and do not make either router or interactable the progression grant authority.

**Review verdict:** `AGREE IN SUBSTANCE` (A2; not signed). **Joint status:** `RECONCILIATION IN PROGRESS`.

### C-07 — IDs, tags, registry, persistence, MEAD dependency

**A1-R2 proposal:** Lists identity/tag concepts and collision dispositions, yields some vocabulary to MEAD `Status.*` / `Damage.*`, removes proposed overlapping mode namespaces, and keeps other items proposed. It says final namespace, registry owner, and save policy depend on TD/Agent 3; its “yield to MEAD” approach presupposes a uniquely identified canonical MEAD that has not been selected.

**A2 review verdict:** Clarification required. A2 identifies the divergence among MEAD-A/B/C, missing `Status.Dead`, and absence of a registry owner. A2 raises TD-12 for document identity/canonicalization and TD-13 for interactable identity/persistence; it asks that interactable policy be deferred until the save owner provides schema and consumer inventory. It does not choose an ID family or persistence policy.

**Reconciliation:** C-07 is blocked on TD's exact-file/commit canonicalization declaration, a named registry owner and published vocabulary inventory, plus TD-13/save-owner evidence (schema and consumer inventory). “Yield to MEAD” means only “defer pending TD declaration”; it is not A1's adoption of any MEAD. No ID/tag namespace, retirement policy, or interactable persistence behavior is selected here.

**Review verdict:** `CLARIFICATION REQUIRED` (A2). **Joint status:** `TD REVIEW REQUIRED`.

## 4. Required unsent Agent 1 questions

### Delivery status

Direct agent messaging is unavailable in this session. The following request is **prepared, not sent**. It is reproduced in the Agent 1 ledger for standalone delivery. This status means no request was delivered through a direct agent channel. No response is implied.

### Copy-ready request

> **To Agent 1 — please respond against your exact A1-R2 v1.1 at commit `f578fe612ad173b74f99fcb187f825eb3de6f59a` and A2's formal review at commit `4220b82ffdebf291793ce508dd25080528a3dac8`. Give exact replacement text/new version where requested; do not infer counterpart agreement.**
>
> 1. **C-01 / P3:** Resolve the contradiction between §3.2 “Permanent, never reused after retirement” and §10.4 rename per level edit without migration when no save references routes. Accept/counter A2's exact scoped-stability wording (stable for named content; no reuse while save/log/telemetry references exist; tombstone requirement dependent on TD-04 save references), or provide exact replacement clauses. State whether route keys are saved; leave that policy to TD-04 if unresolved.
> 2. **C-04 / C-07 status inventory:** State whether each omitted MEAD-C tag—`Status.Cinematic`, `Status.Attacking`, `Status.Blocking`, `Status.Parrying`, `Status.Invulnerable`, `Status.Grabbed`—is retained, intentionally omitted from the dispute-only inventory, or withdrawn. Address the missing `Status.Dead`/`Status.Died` explicitly, including exact proposed registry request or named equivalent, without unilaterally registering it. Preserve `Dead > Cinematic > Stagger`.
> 3. **C-05 / TD-06:** Address A2's asymmetric-dilation finding. Choose/counter Option A (shared time axis plus producer factor) or Option B (both axes plus factor), and specify the exact message coordinate/conversion. Also define what happens when dilation changes during an active telegraph: endpoints and remaining duration, factor capture vs piecewise-integrated history, and how consumer data remains comparable. Confirm explicitly that parry is same-frame phase overlap, not timestamp subtraction. Supply exact contract text; do not report proposed tests as run.
> 4. **C-07 / TD-12:** State that every “yield to MEAD” clause is conditional on TD declaring a specific canonical file and commit. Identify A1-R2 clauses/citations that must be revised if the canonical source differs from MEAD-C. Do not declare a canonical document or move/delete/rename/archive/overwrite any MEAD.
> 5. **TD-09 / MEAD-C §5.4:** Accept or counter A2's proposed erratum in A2 review §10.3. Resolve whether `OutcomeType` on `FTDDDamageRequest` is advisory attacker-side input that the victim-side arbiter re-derives, never an authoritative outcome; annotate that for any player-victim hit A1 alone owns detection, arbitration, defence evaluation and mitigation, and that the `ApplyDamage` arrow denotes an authorised application call. Provide exact replacement/annotation wording or an alternative.
> 6. **C-07 / TD-13:** Explicitly accept or counter deferring interactable identity/persistence until the Agent 3/save owner supplies a save-schema and consumer inventory. State exact dependency wording; do not choose an interactable ID family or persistence policy now.
> 7. For **each C-01…C-07**, state `AGREE` / `DISAGREE` / `CONDITIONAL` against the exact same-version A1-R2 v1.1 text as reviewed by A2; distinguish proposed revisions from current text. In particular, do not call C-02, C-03 or C-06 bilaterally agreed merely because A2 has no technical objection. No API freeze, implementation, or M0 declaration is requested or authorized.

## 5. Three-MEAD read-only comparison and TD recommendation

### 5.1 Exact inspected identities and chronology

These are the branch-tip versions inspected for this comparison. Creation order is based on the creation commit metadata; authorship strings and branch context are stated literally, not used to infer canonical authority.

| Candidate | Inspected branch tip / path / blob | Formal identity in document | Creation and later history |
|---|---|---|---|
| **MEAD-A** | `origin/arena/5dde91a4-tdd`, tip `912fac9f76a1011f8c823b368a92a0edf059a283`, `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, blob `bd0f3afdf24736349f2045bf0ee423ee0b4e1a78` | Explicitly `TDD-MEAD-001`, v1.0 | Created `e95c2389e49532f4f1c1cacb4d095378f66ca43d` by “Arena Agent” at 2026-11-16 18:44:06 UTC. Later Agent 2-authored changes are present by tip `912fac9` (tip time 20:26:17 UTC). At source creation it was 1,054 lines; inspected tip 1,078 lines. |
| **MEAD-C** | `origin/arena/3bc206a0-tdd`, tip/creation `169a8d8f4f95dca526239dfbf744e97590504a70`, `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md`, blob `f49354631c86601e9311865901bf1fcd44846d89` | Explicitly `TDD-MEAD-001`, v1.0 | Created by “Arena Agent” at 2026-11-16 18:39:41 UTC; 1,231 lines. |
| **MEAD-B** | `origin/arena/c64fc525-tdd`, tip `d32660fee1b0234871b39b9fa56677c7cf62f28f`, `docs/MASTER_ENGINEERING_ARCHITECTURE.md`, blob `1e8d1bd1b223c364c02464f6036e3f9ee9a9b0a7` | Header identifies “Master Engineering Architecture (initial baseline)”; no formal document ID/version found in the header or full-text identity search | Created `7f24859f716bdc36d15f5ef8b54370e4b6be80da` by “The-Mhood” at 2026-11-16 19:35:21 UTC; 247 lines. |

Thus, it is inaccurate to say all three formally identify as `TDD-MEAD-001 v1.0`: **A and C do; B does not**. B is nevertheless a third, materially different architecture document. The order is C, A, B; A was subsequently edited by Agent 2. Chronology alone establishes neither supersession nor intended canonical status.

### 5.2 Substantive comparison and distinct contributions

| Topic | MEAD-A | MEAD-B | MEAD-C |
|---|---|---|---|
| Scope / structure | Long, production-oriented architecture, 1,078 lines at inspected tip; engine/project setup, gameplay and world systems, contracts, content and production plans. | Short initial baseline, 247 lines; architecture boundaries, provisional systems, content/campaign outline, risk and production gates. | Long, detailed architecture, 1,231 lines; character/combat, damage pipeline, world, persistence, status tags, decisions/governance. |
| Engine / project | Explicit UE 5.8 baseline; C++ project with Blueprint subclasses; single-player/PC-first and extensive engine, rendering and project configuration. | Explicitly leaves UE minor version, platform, hardware, renderer, online scope, source-control asset strategy and other project decisions unselected. | Detailed Unreal module/subsystem architecture and GAS scope; distinct assumptions and component names. It is not the source of A's UE 5.8 decision. |
| Combat ownership/material | Its own combat architecture: `UTDDHitArbiter` is sole hit arbitration owner; its own tag vocabulary includes `State.Combat.*`, not MEAD-C's seven `Status.*` set. | Provisional combat/damage receiver contract and ownership boundaries, without MEAD-C's detailed §5.4 pipeline. | Section 5 is character/combat architecture; detailed hit detection and §5.4 damage pipeline; seven fixed status tags and `Damage.Physical.Slash`. |
| Narrative/content | Seven-memory mapping and a specific seven-memory narrative sequence; memory fragment, canonical location ID and save/content-hash treatment. | Chapter and memory/endings scope with explicit caveats that detailed narrative/canon is not final; save concepts remain proposed. | Broad chapter/world and memory systems, with distinct save schema and world-state architecture. |
| Identity | Canonical location and memory IDs, stable actor GUIDs, content/save references; distinct identity and persistence decisions. | Stable namespaced IDs are proposed but final schema/policies remain open. | Multiple event/entity/content IDs and a distinct persistence schema; not identical to A or B. |
| Damage-pipeline citation | No §5.4 damage-pipeline section; its Section 5 concerns engine/project configuration. | No §5.4 damage-pipeline section; its Section 5 concerns core gameplay systems. | Contains the exact §5.4 pipeline cited by A1-R2/A2, including `OutcomeType` in the request and victim-side branching. |

**Relationship finding:** A and C share broad architecture concerns and common project context, but differ in section structure, ownership vocabulary, tag systems, engine/project commitments, combat structures, and content/persistence details. Neither is a mere path copy or demonstrably superseded duplicate of the other. A contains later Agent 2-authored updates and substantive material not captured by C, including UE 5.8 and its seven-memory sequence. B is a shorter, separately authored initial baseline and not a truncated version formally labeled v1.0. No inspected document itself supplies a clear supersession statement resolving all three as a single authoritative record.

### 5.3 Latest intended architecture and omissions

There is **no evidenced single “latest intended architecture”** among the three candidates. If “latest” means latest edit by commit chronology, MEAD-A's inspected tip includes later Agent 2-authored changes; if it means latest separately added document, MEAD-B is newer but self-identifies only as an initial baseline; MEAD-C is the earliest and is the sole source for the exact §5.4 and status vocabulary currently cited. These different senses must not be collapsed into a canonicality claim.

A canonical text based only on MEAD-C would omit or fail to carry across, without explicit reconciliation, MEAD-A's UE 5.8/project configuration decisions, extensive engine/rendering details, distinct combat-arbitration design, seven-memory sequence and its persistence/content-hash choices. A canonical text based only on MEAD-A would omit MEAD-C's exact §5.4/§5.5 pipeline and hitstop specification, its seven `Status.*` tags, and other distinct component/persistence details. MEAD-B omits substantial specifics present in both longer documents, while its deliberate “unselected” scope is itself meaningful and should not be overwritten by accidental merge. These are examples of material differences, not a claim that one document is complete or correct.

### 5.4 Recommendation to TD — candidate only, not a decision

**Recommendation:** Consider **MEAD-C at exact commit `169a8d8f4f95dca526239dfbf744e97590504a70`** as the *canonicalization candidate/reference for the current A1-R2 citation and TD-09 erratum work*, because it is the only candidate containing the specific §5.4 damage pipeline and seven-tag vocabulary that A1-R2/A2 review cite, and its clauses are the subject of TD-09. This narrow suitability does **not** mean C is the latest architecture, the most complete overall, already canonical, or that A and B are superseded.

TD retains final authority. Before declaring canonicality, TD should decide whether to: (a) designate C as a narrow reference while separately reconciling A's later content and B's baseline, (b) designate a different exact file/commit and specify the required migration of citations, or (c) request a new, versioned synthesis with a clause-level source/decision map. No option is adopted here. Preserve all three files and histories; do not move, delete, rename, archive, overwrite or edit any MEAD.

## 6. TD rulings and owner inputs still required

1. **TD-02 / C-04:** Resolve classification representation only after Agent 1/2 confirm same-version semantics; preserve `Dead > Cinematic > Stagger`. Name the registry owner and resolve the unrepresented `Dead` status/equivalent without an agent inventing a tag.
2. **TD-03 / C-03:** Rule on applied-event scope for blocked/parried outcomes and confirm the designated publisher/meaning against the exact proposal; keep miss/immune/rejected/duplicate/out-of-window exclusions as the reviewed proposal pending ruling.
3. **TD-04 / C-01, C-07:** Determine whether route keys appear in saves. Only then settle retirement/tombstone requirements and reconcile P3 with §10.4.
4. **TD-06 / C-05:** Choose/approve a shared cross-entity clock coordinate and conversion, including how changes in dilation during an active telegraph are represented and integrated. Confirm same-frame phase overlap rather than timestamp subtraction and determine late-subscriber query/event surface.
5. **TD-07 / C-06:** Existing proposal makes progress opt-in and router-owned; retain damage-interrupts-hold as an open design ruling. Do not infer a cancellation reason is guaranteed.
6. **TD-08 / C-04, C-07:** Publish registry ownership and status/tag namespace disposition, including the six omitted MEAD-C tags and missing `Dead` representation.
7. **TD-09 / C-03, C-07:** Decide and issue an erratum/annotation for the exact canonical MEAD clause after identifying file and commit. A2's requested text is prepared but not adopted (see §7).
8. **TD-12 / C-07:** Declare canonicalization status against exact file path and commit, or explicitly defer and commission a versioned synthesis. TD retains final authority; recommendation §5.4 is nonbinding.
9. **TD-13 / C-07:** Defer interactable persistence/ID policy until Agent 3/save owner supplies the save-schema and consumer inventory, or issue a specific decision after that evidence. No policy or namespace is selected here.
10. **Registry/save owner:** Provide the inventory required by TD-08/TD-13. No agent-level source authorizes guessing it.

## 7. Prepared TD-09 wording — not adopted

A2's review §10.3 proposes an annotation/erratum to MEAD-C §5.4. For TD's consideration only:

> **Proposed §5.4 erratum:** This diagram describes authorship and initiation, not arbitration authority. `OutcomeType` on `FTDDamageRequest` is advisory attacker-side input and is re-derived by the victim-side arbiter; it is never accepted as the outcome. For any hit in which the player is the victim, arbitration, defence evaluation and mitigation are Agent 1's alone; the attacker submits intent and authored data only, and receives the applied event. The diagram's arrow into `ITDDDamageable::ApplyDamage` denotes an authorised application call, not an attacker-controlled entry point.

This is a prepared candidate quotation from A2, not an adopted amendment. Agent 1 must accept/counter exact wording, and TD must identify the canonical file/commit and authorize the erratum. No MEAD has been altered.

## 8. Evidence and test-status separation

This task performed source inspection/comparison and document preparation only. **No tests, builds, Unreal/editor checks, route parser, or runtime checks were run for this reconciliation.** A2's review reports the following source claims at its pinned source; they are not independently rerun or certified here:

| Evidence category | Reported source evidence | What it does not establish |
|---|---|---|
| Data checks | 9 `contract_data_checks.py` checks, reported 9/9. | Not cross-agent contract acceptance, API correctness, or runtime behavior. |
| Document tests | A2 reports 23 document tests and other source-reported suites/checks (including 43 plus 38 additional/review checks as itemized in its source). | Not acceptance of A1-R2 by both agents; not Unreal runtime validation. |
| Other project/source checks | A2 reports canon 114, world 337, L0 14/14, contract checks 9/9, evidence 13/13, and 43 + 38 additional/review tests or checks as itemized in its source. | These remain attributed reports and are not task-run evidence; counts are not combined into a new pass claim. |
| Contract acceptance | **42 proposed contract acceptance tests remain unexecuted.** A2's review explicitly reports zero contract acceptance tests run. | No contract acceptance, implementation, or behavior proof. |
| Engine/runtime | No Unreal implementation/runtime test exists in this task evidence. | No functioning game, build, runtime, or packaged behavior claim. |
| M0 | No M0 claim authorized. | No M0 pass/declaration. |

## 9. Files, publication boundary, and history

New versioned documents are:

- `docs/CROSS_AGENT_CONTRACT_RECONCILIATION_V3.md` — this reconciliation and MEAD comparison.
- `docs/AGENT1_CONTRACT_RESPONSES_V3.md` — Agent 1 response/status ledger and prepared unsent questions.
- `docs/AGENT2_CONTRACT_RESPONSES_V3.md` — Agent 2 response/status ledger and same-version signature record.

Prior V1/V2 reconciliation and response ledgers remain unchanged. The previous reconciliation's C-08 population caveat (29 exact / 5 bounded / 1 unbounded / 11 uncaptured) and C-09 `CH01-SCN-014` no-invented-bound constraint remain historical constraints; A2's withdrawn unsupported prop/interactable totals and reported 57/57 Chapter 1 location capture/provenance are not altered or independently revalidated here. MEAD-A/B/C and authoritative registers remain unchanged. Unrelated `README.md` and pre-existing files are not part of this document change. The only requested publication scope is these three new ledgers.

| Version | Change |
|---|---|
| 1.0 | Earlier awaiting-submission reconciliation; preserved. |
| 2.0 | Reconciled A1-R1/A2 initial submissions against TD v1.2; preserved. |
| 3.0 | Pinned A1-R2 and A2 review exact commits; reconciled C-01…C-07 separately; recorded no signatures for C-02/C-03/C-06; added unsent Agent 1 questions, three-MEAD read-only comparison and nonbinding TD recommendation, TD-09 proposed erratum, TD-12/13, and explicit evidence boundaries. No MEAD or contract changed/frozen. |
