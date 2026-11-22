# Agent 1 — TD v1.2 Acknowledgment and Contract Revision

**Response ID:** `TDD-A1-CONTRACT-RESPONSE-002`
**Version:** 1.1 (`A1-R2`)
**Date:** 2026-11-16 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`

| Reviewed document | Exact version | Commit | Blob |
|---|---|---|---|
| **Governing addendum** | `TDD-TD-INT-001` **v1.2** | `e121bbbf09562e3cba0efe81aad971809685db23` | `08c79415…` |
| Agent 3 reconciliation | `TDD-INT-RECON-001` **v2.0** | `d32660fee1b0234871b39b9fa56677c7cf62f28f` | `9d0f383b…` |
| Agent 2 submission (reviewed, **not** agreed with) | `A2-C01…C07-1.0` | `3ac438b32fcd73ceb22dcd81385356f7b8b39644` | `b8417288…` |
| Agent 1 prior submission (**preserved unchanged**) | `A1-R1` **v1.0** | `97828db7d9786c0fa5415578e796a822aab497a8` | `25ab47c2…` |

**Status:** `DESIGN_ONLY` — acknowledgment and proposal revision only. No Core type, no C++ or gameplay, no project, no merge, no API frozen, no M0 claim, **no Agent 2 agreement inferred**.

---

## 0. How to read this document

### 0.1 Status legend — used exactly as written

| Label | Meaning in this document |
|---|---|
| **CONFIRMED DECISION** | A Technical Director decision I have read and am implementing my design against. Not mine to change |
| **MY PROPOSAL** | Agent 1's design position, `PROPOSED — NOT FROZEN`, subject to Agent 2 review and TD acceptance |
| **UNRESOLVED** | I cannot settle this; it needs a TD ruling, an Agent 3 registry decision, or Agent 2's explicit position |
| **DEPENDENCY** | Something I need from Agent 2 or Agent 3 before the proposal can be finalised |
| **TEST PROPOSED** | A named test with measurable assertions that **has not been written and has not run** |
| **TEST EXECUTED** | A test that actually ran, with output. **There are none in this document** |

### 0.2 What changed, and why — stated precisely because the distinction matters

**Against TD v1.2 alone, all seven contracts are UNCHANGED.** v1.2 is a coordination and status document: it records awaiting-submission states, per-contract dependency notes, delivery limitations, the C-08/C-09/C-10 positions, and explicitly says it "does not resolve these implementation/design choices" and that "No row below declares a new TD decision" (§4 of the reconciliation says the same). Its own §1 says the governing baseline is v1.1 at commit `50b1431`. Nothing in v1.2 contradicts, narrows or expands a clause of `A1-R1`.

**The six revisions in this document are driven by three things, none of which is a change of TD decision:**

1. **The Technical Director's own numbered requests** TD-02 … TD-09, which ask me to resolve or refine positions I had left open.
2. **Agent 2's submission (`A2-C01…C07-1.0`)**, which became visible to me through the reconciliation and which I had not read when writing `A1-R1`. Several of my clauses were written without knowing what the consumer wanted; two of them (C-01 identity format, C-06 progress delivery) are genuinely improved by that knowledge.
3. **The reconciliation's correction of one factual claim of mine** (TD-01 visibility), which I accept and close.

Where a revision would be read as accepting Agent 2's position, it is labelled as my proposal that happens to agree — **never** as bilateral agreement.

### 0.3 Preservation

`A1-R1` v1.0 (`docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md`, blob `25ab47c2…`) is **not modified, not overwritten and not amended** by this document. It remains the historical record of what Agent 1 proposed before seeing TD v1.2, the reconciliation or Agent 2's submission. Where this document revises a clause, it names the clause number in `A1-R1` so the two can be read side by side.

---

## 1. Acknowledgment of TD v1.2

### 1.1 The exact document I reviewed

I read `docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md` at commit `e121bbbf09562e3cba0efe81aad971809685db23` (blob `08c7941587a6cedcfca3def4997577a35d3382e1`), fetched directly by commit SHA rather than by branch name. I also read Agent 3's `CROSS_AGENT_CONTRACT_RECONCILIATION_V2.md` at `d32660fee1b0234871b39b9fa56677c7cf62f28f`, and Agent 2's `Docs/CONTRACT_SUBMISSION_A2_V1.md` at `3ac438b32fcd73ceb22dcd81385356f7b8b39644` as counterpart material — reading is not agreeing.

### 1.2 What I understand v1.2 to be — **CONFIRMED DECISION**

| Point | My understanding |
|---|---|
| Status | `TDD-TD-INT-001` **v1.2** is the **current governing cross-agent integration addendum**. v1.0 and v1.1 remain unchanged; v1.2 supplements them |
| Character | A **coordination and status** package: response tracking, delivery limitations, per-contract status/dependencies, C-08/C-09/C-10 positions, and the next TD decisions. It is **not** an implementation-ready or frozen API |
| Governing baseline | v1.1 at published commit `50b14318c8089dedcc688fb2c78ad3cb361c15f5` |
| Technical effect | **None on my proposals.** It freezes no enum, struct, delegate, tag or Core API and resolves none of TD-01…TD-09 |
| Binding content I must respect | (a) Agent 1 keeps ownership of player state mutation, traversal execution, hit arbitration/damage application and player interaction routing; (b) locomotion, action/control and combat status stay separate; (c) **Dead (100) > Cinematic (90) > Stagger (80)**; (d) M1 v1.4 damage/`AbortWindow`/fallback/restoration/terminal-hold semantics preserved without reinterpretation; (e) health application independent of control-state resolution; (f) `bCausesStagger` not an approved permanent field; (g) TDD canonical, Agent 2's skeleton not adopted |
| What it does **not** grant | No tag namespace, no ID family, no persistence policy, no clock ownership, no progress authority, no arbitration amendment. Those remain open (`TD-02`…`TD-09`) |

### 1.3 Visibility context and the TD-01 correction

`A1-R1` §0.2 stated that v1.2 was absent from the repository. That statement was true **of what I could see**: the packet commit `50b1431` contains only v1.0 and v1.1, and `origin/main` is `5e3d1da`, which does not contain v1.2 either. v1.2 was published on Agent 3's branch and is visible by commit SHA.

**I accept the reconciliation's correction and close my original TD-01 as a visibility fact, not a defect in anyone's delivery.** Nothing in `A1-R1` is invalidated by it, because v1.2 adds no technical ruling that my v1.1-based reading would have missed — verified clause by clause against `A1-R1` §1–§7 in §2 below.

### 1.4 Acknowledgment statement

> **I have read `TDD-TD-INT-001` v1.2 at commit `e121bbb…`, I understand it as the current governing cross-agent integration addendum, and I accept it as the baseline for this revision.** I do not treat it as approving any of my proposals, and I do not treat my reading of Agent 2's submission as Agent 2's approval of mine.

---

## 2. Per-contract review — the one-word answer first

| Contract | Effect of v1.2 | Label for `A1-R2` | Cause of the label | Clauses revised |
|---|---|---|---|---|
| **C-01** Traversal | None | **REVISED** | A2's route-key submission + TD-04 request | `A1-R1` §1.5 (identity example), new §1.5a (world-facing projection), §1.3a (capability semantics) |
| **C-02** Player context | None | **REVISED** | TD-05 request + A2's field list (health withdrawn by A2, `bInCombat`/`CameraForward` added) | `A1-R1` §2.2/§2.3 (health & posture removed), §2.5a (staleness), new §2.3a (carry not provided) |
| **C-03** Damage | None | **REVISED** | TD-03 request + A2's `RequestId`/`HitEventId`/unload policy | `A1-R1` §3.2 (identity), §3.6 (event scope table finalised), §3.9 (publisher) |
| **C-04** Stagger | None (register notes it as `TD REVIEW REQUIRED`) | **REVISED** | TD-02 request + A2's recovery-event need (`A2-R1` §11 item 11) | `A1-R1` §4.2 (recommendation restated with implications), new §4.6a (recovery notification) |
| **C-05** Telegraph | None | **REVISED** | TD-06 request + divergence with A2's undilated-window proposal | `A1-R1` §5.3 (concrete clock definition), §5.5 (pause/dilation table) |
| **C-06** Interaction | None (register escalates damage-interrupts-hold) | **REVISED** | TD-07 request + A2's "no progress" position | `A1-R1` §6.2/§6.4 (progress becomes opt-in), §6.5 (damage rule flagged as design escalation) |
| **C-07** IDs and tags | None | **CLARIFICATION REQUIRED** | Namespace collisions with A2 + no registry owner decision | `A1-R1` §7.3 inventory retained; §7.9 states exactly what is needed |

**Summary:** 6 REVISED, 1 CLARIFICATION REQUIRED, 0 UNCHANGED — and **0 changes caused by v1.2 itself**. If the TD wants the narrower reading ("did v1.2 change anything?"), the answer is: **nothing, in all seven.**

---

## 3. C-01 — Traversal: **REVISED**

### 3.1 What v1.2 says about C-01 — **CONFIRMED DECISION**

v1.2's C-01 row records: "AWAITING SUBMISSION from both… Depends on C-02 context and C-07 route/tag identity; **M1 v1.4 behavior stays unchanged**… compare no-candidate/invalid/unsupported/blocked/unloaded semantics." No clause of mine is altered; the instruction to compare outcome semantics is exactly what §3.4 below does.

### 3.2 Revision R1-1 — route identity becomes format-agnostic (`A1-R1` §1.5)

`A1-R1` proposed the example format `TRV.<ChapterId>.<SceneId>.<NNN>` and said explicitly it was a suggestion and that the authoring side owns the representation. Agent 2 proposes `<LOCATION_ID>/ROUTE-<LETTER>`, anchored on a location register entry whose multi-valued `Category` includes `Traversal Area`, and reports that a prefix-only rule (`TRV-`) would exclude three legitimately traversal-capable Chapter 1 locations (`SUB-009`, `SUB-020`, `EXP-003`).

**I withdraw my example format and restate the requirement as four properties, which any format must satisfy:**

| Property | Requirement | Why Agent 1 needs it |
|---|---|---|
| **P1 Opacity** | Runtime code never parses the key. Only a validator may | Renaming or re-prefixing must never change behaviour |
| **P2 Uniqueness** | Globally unique across all chapters; duplicate registration refused deterministically | Selection must be a total order (R1-3) |
| **P3 Stability** | Permanent, never reused after retirement | Saves, logs and telemetry must resolve the same content forever |
| **P4 Non-derivation** | Not computed from a transform at runtime | A moved marker must not silently become a different route |

**I accept A2's location-anchored shape as satisfying P1–P4**, and I add one requirement from my side (**P5**): the key must not encode the *capability* the route requires. Capability lives in the requirement data, not the key, because a route may legitimately change capability after authoring review without becoming a different route.

**I accept, as a reported source fact, A2's correction that the parent must be validated by register `Category`, not by ID prefix.** I have not read the location register myself; I am accepting their captured evidence as stated, flagged as `DEPENDENCY` for the moment a route validator is written.

### 3.3 Revision R1-2 — capability semantics answered (A2's §11 items 1–4)

Agent 2's four `High`/`Medium` questions about capability requirements had no answer in `A1-R1`. They now do:

| A2 question | My answer |
|---|---|
| Capability names and shape (item 1) | `Vault`, `Mantle`, `LedgeShimmy`, `Drop`, `ClimbLadder`. Two surfaces: an exec branch enum for A1's own dispatch, and one `Traversal.Capability.*` tag per capability for authored requirements. **Both are mine to name because the execution branch is mine**; the tag names are requested from the registry (C-07) |
| Data or code (item 2) | **Data.** Requirements are a tag container plus an AND/OR grouping; no `TFunction` predicates. This is what makes A2's offline validation possible and I want that |
| Cumulative vs independent (item 3) | **Independent set membership.** The player holds a set of granted capabilities; a route requires set membership. There is no "A then B" sequence — a sequence would be a scripted gate, not traversal capability, and scripted gates belong to narrative conditions, not C-01 |
| Revocable (item 3) | **Yes.** Grants can be removed (a plot-granted capability revoked, a carry blocking a vault). Evaluation happens **per query**, so revocation takes effect on the next query, never mid-execution. Mid-execution revocation does not abort a traversal: M1 v1.4 governs exit, and aborting on a tag change would be a new abort trigger I am not adding |
| Water / rope context (item 4) | **Out of scope in this slice.** M1 v1.4's executable set is grounded traversal; water and rope contexts would require capabilities I have not designed and content nobody has approved. I am not adding a context dimension to the contract to cover them. If the slice later includes `CH01-TRV-003`/`TRV-004` traversal, that is a new capability plus a contract revision, not a parameter I can guess |

### 3.4 Revision R1-3 — the world-facing result is a **projection**, not a second enum

Agent 2 proposes the runtime values `Available`, `Unsupported`, `Blocked`, `Unloaded`, `Invalid`, `NoCandidate`. My query returns `None`, `CandidateFound`, `UnsupportedByPlayer`, `InvalidAuthoredData`, `BlockedPath`, `WorldUnavailable`, `Cooldown`. The reconciliation correctly refuses to collapse them silently.

**My proposal:** keep both, and define the mapping explicitly as a projection emitted *for the world*, distinct from the player query outcome:

| My outcome | World-facing projection | Note |
|---|---|---|
| `CandidateFound` | `Available` | |
| `UnsupportedByPlayer` | `Unsupported` | |
| `None` | `NoCandidate` | |
| `BlockedPath` | `Blocked` | |
| `WorldUnavailable` | `Unloaded` | Explicitly "not resident", not "unavailable" |
| `InvalidAuthoredData` | `Invalid` | Authoring error, never a player-facing message |
| `Cooldown` | `Blocked` **with a distinct reason code** | Folding it silently into `Blocked` would hide a re-entry guard behind a world-state word; `A1-R2` keeps the reason visible |

**Two claims this makes, both testable:** the projection is total (every one of my outcomes maps) and lossy in exactly one place (`Cooldown`), which is why the reason code exists. I am **not** merging the enums; I am defining one direction of translation, owned by me, reviewable by A2.

On A2's **silent feedback** request (their §3.5.1): my `A1-R1` §1.4 already produces **no prompt** for `UnsupportedByPlayer`, `BlockedPath`, `WorldUnavailable`, `Cooldown` and `InvalidAuthoredData`. There is **no conflict with M1 v1.4** — v1.4's animation response belongs to *execution* (E1–E7), not to query outcomes. I record that explicitly because A2 flagged it as a possible conflict.

### 3.5 Where C-01 stands

| Item | Status |
|---|---|
| Five capabilities and their behaviour definitions | **MY PROPOSAL**, unchanged from `A1-R1` §1.2, now with names offered to A2 |
| Route key format | **MY PROPOSAL**, revised: format-agnostic P1–P5; A2's shape accepted as conforming |
| Marker representation | **DEPENDENCY** on A2; unchanged |
| Query semantics and seven outcomes | **MY PROPOSAL** |
| World-facing projection | **MY PROPOSAL**, new in `A1-R2` |
| Route persistence/save references | **UNRESOLVED** — TD-04, §10.4 |
| Tests | `TEST PROPOSED` only; see §12.6 |

---

## 4. C-02 — Player context: **REVISED**

### 4.1 What v1.2 says — **CONFIRMED DECISION**

v1.2's C-02 row: obtain minimal field lists, preserve Agent 1 mutation authority, "May use C-07 IDs/tags", no field-level consumer review yet. Nothing narrows my proposal; the reconciliation requires a required/conditional/unrequested classification, which §4.4 supplies.

### 4.2 Revision R2-1 — health and posture **removed** (`A1-R1` §2.2, §2.3, §2.9)

`A1-R1` marked `HealthFraction` and `PostureFraction` **conditional on a named A2 consumer**. Agent 2's submission withdraws health explicitly and states that if a boss ever needs a health threshold it will ask for a **phase-condition evaluation** rather than a polled field, because polling health would be "a second authority by the back door".

That is the correct instinct and it matches my own authority model. **I remove both fields from the proposal.** A boss phase condition becomes a query I evaluate (`EvaluatePhaseCondition(ConditionTag) -> bool`), which keeps the attribute in the owner's hands and gives A2 exactly one derived boolean instead of a continuous value it might trend-log or interpolate.

### 4.3 Revision R2-2 — `bInCombat` and `CameraForward` accepted

| A2 request | My response |
|---|---|
| `bInCombat` (`REQUIRED` for them) | **Accepted as a derived field**: `bInCombat = (CombatState != None && CombatState != Dead)` per `ETDDCombatState`. I publish it rather than make A2 infer it from a 12-value enum, because "is this a fight" is a real consumer decision and inference across modules is how drift starts |
| `CameraForward` (`REQUESTED`) | **Accepted.** The camera is Agent 1's; A1 already computes an aim basis. Note it is **not** `AimDirection`: camera forward is the view axis, aim is the input-derived direction. Both are published and they are documented as different |
| `Velocity` (`REQUESTED`) | Already published in `FTDDLocomotionSnapshot`; no change. Their fallback (position deltas) degrades by one frame — my field removes that reason to approximate |

### 4.4 Revision R2-3 — field classification, as the reconciliation requires

| A1 field | Classification for `A1-R2` | Basis |
|---|---|---|
| `ActorLocation`, `ActorRotation`, `Velocity`, `Speed2D`, `bGrounded`, `MovementMode` | **Required** | Named by A2 (crowd LOD, crowd reaction radius, traversal gating, telegraph targeting) |
| `AimDirection`, `CameraForward` | **Required** | Aim: AI facing prediction. Camera: view-cone scoring |
| `bInCombat` | **Required** (new) | A2 combat start/stop |
| `CurrentTargetEntityId` (+ weak ptr) | **Required** | Interaction target / threat |
| `FrameCounter`, capture timestamps | **Required** | Freshness and event/query consistency |
| `ControlState`, `ControlStateTag`, `StateElapsedSeconds`, `bAllowsInput`, `bLocked` | **Conditional** | A2 has not named a decision that fails without them. They stay published locally; whether they enter the *shared* surface is A2's call. I note one concrete candidate use A2 should consider: "do not attack a player locked in a traversal or a cinematic" is a fairness decision that currently has no named consumer |
| `ActiveActionId` | **Conditional (diagnostics)** | Telemetry attribution |
| `CombatState`, `bAlive`, `bIsStaggered`, `StaggerRemainingSeconds` | **Required** | A2 boss/AI reaction, punish windows |
| `bIsTelegraphing`, `TelegraphRemainingSeconds` | **Required** | A2 defensive response to player attacks |
| `HeightAboveGround`, `GroundSlopeDegrees`, `bOnWalkableFloor` | **Conditional** | Ground-only attacks and ledge awareness; A2 asked for locomotion "at an abstract level" only |
| `HealthFraction`, `PostureFraction` | **Removed** (R2-1) | A2 withdrew health; posture unrequested |
| `CarryState` | **Not provided** — see 4.5 | No carry system exists |
| Stealth / noise radius | **Not provided** — TD-05, §10.5 | No approved design, no consumer |

### 4.5 `CarryState` — not provided, and why I will not invent it

Agent 2 marks `CarryState` `REQUIRED` for route gating, and the reconciliation records it as "required by A2, unrequested in A1's current field list".

There is **no carry system in M1 v1.4**, no approved design for carrying objects, and no content decision that says Chapter 1 gating depends on it. A field called `CarryState` with invented enum values would be a fabricated system in a data shape, which is exactly what this project's rules forbid.

**My position:** `CarryState` is not in the C-02 surface for this slice. If route gating on carried objects is a real Chapter 1 need, it is a **new design decision** that produces (a) a carry system owner, (b) an enum, (c) a gating rule, and only then (d) a snapshot field. I will add it the day (a)–(c) exist, and not before. This is `UNRESOLVED` with A2/design, listed in §10.5's neighbour table and in §12.3.

### 4.6 Revision R2-4 — staleness and invalidity reconciled (`A1-R1` §2.4)

A2 proposes: stale if `FrameStamp` older than **2 frames**; may score with stale, must not commit. My guarantee is one frame per tick, so their rule is *weaker* than what I provide and causes no conflict at the producer boundary. I adopt their **scoring vs commit** distinction as the documented consumer rule, and keep my stronger guarantee: **a frame is published exactly once per player tick, and a consumer committing on a frame older than the current tick is out of contract.**

One difference remains, and it is deliberate: A2 proposes `bValid=false` on the snapshot; I propose `GetPlayerContext()` returning `false` plus an invalidation event. Both express "no usable context"; mine also gives a **reason** (unpossessed, despawned, level transition, paused) and a **moment** (an event), which a frame-stamp-only flag cannot. I propose that the shared surface supports both readings: query returns false **and** the last frame carries `bValid=false` with a reason. No consumer has to change its pattern.

### 4.7 Where C-02 stands

| Item | Status |
|---|---|
| Three separate snapshots + envelope (no merged mega-state) | **MY PROPOSAL**, unchanged and explicitly required by v1.2's state-separation rule |
| Health/posture removal | **MY PROPOSAL**, revised (R2-1) |
| `bInCombat`, `CameraForward` additions | **MY PROPOSAL**, revised (R2-2) |
| `CarryState` | **UNRESOLVED** — needs a design decision first (§4.5) |
| Stealth/noise exclusion | **CONFIRMED** as excluded for now — TD-05, §10.5 |
| Read-only enforcement (three layers) | **MY PROPOSAL**, unchanged |
| Tests | `TEST PROPOSED` only |

---

## 5. C-03 — Damage: **REVISED**

### 5.1 What v1.2 says — **CONFIRMED DECISION**

v1.2's C-03 row accepts Agent 1 arbitration/application ownership and Core event publication, requires separating transient result from applied fact "only if both proposals support it", and leaves payload/publisher to the TD. Agent 2's submission supports the separation explicitly. **Both proposals therefore support it, which is the condition v1.2 set** — that is a fact about the two documents, not an agreement between their authors.

### 5.2 Revision R3-1 — identity aligned with A2's request key (`A1-R1` §3.2)

| `A1-R1` | `A1-R2` |
|---|---|
| `HitInstanceId` minted by the resolver | **`RequestId`** (uint64, caller-generated, unique per attack intent) on the request, **plus** `HitEventId` (unique, minted by the publisher) on the applied event |
| Dedupe key `(InstigatorId, SourceAttackId, HitInstanceId)` | Dedupe key `(SourceEntityId, RequestId)`, retained for the window + 0.5 s |

A2 generates the request and needs its own correlation handle; forcing them to consume an id I mint before they see it would create an ordering requirement with no benefit. Both ids appear in the applied event, so a consumer can correlate intent → resolution → application without guessing.

### 5.3 Revision R3-2 — the applied-event scope, settled as a proposal (TD-03)

| Outcome | Health applied | Posture applied | Applied event | `Amount` | Rationale |
|---|---|---|---|---|---|
| `Applied` / `KillingBlow` / `WeakPoint` | Yes | Per data | **Yes** | **Clamped delta** (actual health removed) | The normal case; clamped is honest and `bLethal` carries overkill |
| `Blocked` | No (or guard-reduced) | Yes | **Yes** | Clamped delta (often 0) | A2's aggression needs to know a block happened; inferring it forces a second signal |
| `Parried` | No | No | **Yes** | `0` | Requires the attacker-side stagger the player caused (see §10.9 on who applies it) |
| `Immune` | No | No | **No** | — | Publishing an "applied" fact for a non-application is a lie in the event log |
| `Miss` | No | No | **No** | — | Nothing happened |
| `Duplicate` / `OutOfWindow` / `InvalidTarget` / `InvalidSource` | No | No | **No** | — | Rejections are not facts about the world |

`PostureDelta` is added to the event (A2 needs it for poise response; the reconciliation lists it as open). **`Amount` means the health actually removed, after mitigation and clamping — never the requested damage, never the post-mitigation-but-pre-clamp number.** Overkill information is carried by `bLethal`, not by inflating `Amount`.

### 5.4 Revision R3-3 — the single publisher, and A2's unload request

**Publisher:** **Agent 1 publishes every applied event**, including hits whose target is an A2-owned actor. The target's `ITDDDamageable` implementation performs the attribute write and **returns the applied delta**; it does not publish. One publisher means one ordering, one dedupe and one place where "exactly once" can be asserted.

This is compatible with A2's proposal (they consume the applied fact) and does not require them to change; it does require them to **return** the delta rather than publish.

**Target unload:** A2 explicitly requests that a hit whose target unloads before application is **dropped, not delivered with a dead handle**. **Accepted.** It matches my `InvalidTarget` path: no application, no event, one diagnostic log. A2's ring-buffer idempotence then never sees an event for a target that does not exist.

**Source unload:** A2 asks for a stable `SourceContentKey` alongside the possibly-stale `SourceEntity`. **Accepted as a proposal**, with a caveat: the content key is authored identity (C-07), and I will not invent one for the player until C-07 settles whether the player has an authored content key at all. Until then the event carries `SourceEntityId` and the player's key is empty.

**Ordering:** per-source monotonic `SequenceNumber` added (A2 asked; it costs one integer and removes an ordering assumption). Cross-source ordering remains **unspecified** — I will not promise a global order I cannot produce.

### 5.5 Where C-03 stands

| Item | Status |
|---|---|
| Six stages (authorship, detection, arbitration, defence, application, publication) | **MY PROPOSAL**, unchanged in structure, refined in §10.9 |
| Single arbiter for player-involving hits | **MY PROPOSAL** — see §10.9 for the maintained MEAD §5.4 concern |
| Event scope / `Amount` / publisher / unload policy | **MY PROPOSAL**, new and complete as a position (TD-03 asks for exactly this) |
| `RequestId` + `HitEventId` + `SequenceNumber` + optional `SourceContentKey` | **MY PROPOSAL**, revised (R3-1, R3-3) |
| Core struct ownership | **DEPENDENCY** on Agent 3; I request fields, I do not author the struct |
| Tests | `TEST PROPOSED` only |

---

## 6. C-04 — Stagger classification: **REVISED**

### 6.1 What v1.2 says — **CONFIRMED DECISION**

The reconciliation marks C-04 `TD REVIEW REQUIRED` and v1.2 registers TD-02 as **OPEN**: "Do not permanently choose `bCausesStagger` or any representation… TD decides after A1 and A2 explicitly review the same proposal; preserve M1 ordering." The precedence Dead > Cinematic > Stagger and health independence are decisions I implement, not propose.

### 6.2 Revision R4-1 — preferred representation, with its implications (TD-02)

**My preference: an enum on the request, `ETDDStaggerClass { Never, Always, OnPostureBreak, OnParryOnly }`** (`A1-R1` §4.2 option **B**).

| Implication | Detail |
|---|---|
| Core delta | One `UENUM` (four values) and one field on `FTDDDamageRequest`. No struct redesign |
| Authoring rule needed | An attack with `PostureDamage > 0` classified `Never` is almost certainly a mistake; the validator should warn, not block, because "chip posture without staggering" is a legitimate design |
| Default when absent | `Never`. A missing classification degrades to **non-staggering** — never to accidental staggering |
| Why not the bool | `bCausesStagger` cannot express "staggers only when posture breaks", which is the common case for light attacks; forcing designers to choose always-vs-never produces either over-staggering or unreachable posture breaks |
| Why not the tag mapping alone | It makes a gameplay rule live in a naming convention; a tag rename silently changes combat feel and no unit test catches it |
| Why not the GAS effect | It classifies **after** application, inverting the accepted order (classify → fallback → restoration → enter). This is a M1 v1.4 violation, not a preference |
| If the TD chooses the bool | My code is **identical**: one resolved value, defaulted. The loss is expressiveness, not structure — which is why I accept it as a fallback and do not block on it |
| When I need it | Before M3 combat implementation. Not before then, and **not frozen now** |

### 6.3 Revision R4-2 — recovery notification accepted (A2's `High` item 11)

A2 asks whether a recovery-from-stagger event exists, and marks it **High** because the alternative is every consumer polling. `A1-R1` left it unsettled.

**My position:** yes, publish a **notification**, from Agent 1's authority, as part of C-04:

| Event | Payload | Authority |
|---|---|---|
| `FTDDControlStateChangedEvent` (existing proposal) | `EntityId`, `OldState`, `NewState`, sequence, gameplay time | A1 — the state change itself |
| `FTDDRecoveryCompletedEvent` (new proposal) | `EntityId`, `PreviousState` (Stagger/Dead/Cinematic), `FrameStamp` | A1 — **notification only** |

The second event is a **convenience for consumers who need the end of a state, not a second authority**: it carries no ability to influence the transition, cannot be raised by a consumer, and is emitted strictly after the state change is committed. If the TD prefers consumers to derive recovery from `FTDDControlStateChangedEvent`, the derived rule is "`OldState == Stagger && NewState == Locomotion|Idle`" — I will document that instead and drop the extra event. Either way, **no parallel state authority is created**, which is the constraint the reconciliation set.

### 6.4 Where C-04 stands

| Item | Status |
|---|---|
| Precedence Dead > Cinematic > Stagger, single winner | **CONFIRMED DECISION** |
| Health independent of control | **CONFIRMED DECISION**, asserted in tests |
| Classification storage | **UNRESOLVED** — TD-02; my preference stated with implications |
| Recovery notification | **MY PROPOSAL**, new (R4-2) |
| Classification evaluation order (lethal → parry → posture → class → default) | **MY PROPOSAL**, unchanged |
| Tests | `TEST PROPOSED` only |

---

## 7. C-05 — Telegraph: **REVISED**

### 7.1 What v1.2 says — **CONFIRMED DECISION**

v1.2 keeps a shared telegraph stream required and the clock unfrozen; TD-06 is **OPEN** and asks me to name the proposed clock and its pause/dilation/hitstop behaviour. A2 states it "cannot freeze the clock" and proposes rules.

### 7.2 Revision R5-1 — one clock, defined concretely (TD-06)

**Proposed:** a Core-owned `UTDDGameplayTimeSubsystem` (Agent 3), exposing a **scaled accumulation per entity**:

```
T_e(n) = T_e(n-1) + DeltaWorldSeconds * PrimaryDilation * CustomDilation(e)
```

| Condition | `PrimaryDilation` | `CustomDilation(e)` | Result for a combat window |
|---|---|---|---|
| Normal play | 1.0 | 1.0 | Real time |
| **World pause** | 0.0 (DeltaWorld is zero while paused in UE) | 1.0 | Clock **freezes**; windows retain remaining duration |
| Global slow-motion (cinematic) | 0.3 (example) | 1.0 | Windows scale with the montage — a 0.20 s active window occupies 0.20 s of *gameplay* time, i.e. longer in wall time |
| **Hitstop on a pair** | 1.0 | attacker/defender dilated to ~0.05 for the stop duration | Both clocks slow **identically**, so the window stays aligned with both montages |
| Global pause + hitstop | 0.0 | any | Frozen; the hitstop resumes with the world |

**Why per-entity and not one world clock:** hitstop is applied per pair (MEAD §5.5 — never global). A single world clock would either freeze unrelated actors or fail to slow the pair, and in both cases the telegraph window and the attack montage would drift apart — the drift is exactly what makes a parry feel unfair.

**Who owns which clock:** Agent 3 owns the subsystem; Agent 1 and Agent 2 both *read* `T_e` for their own entity. Neither writes the other's time. This is what lets A2 keep producing timestamps without owning a clock, which is what they asked for.

### 7.3 Revision R5-2 — the divergence with A2, named precisely

| Question | `A1-R2` (me) | `A2-C05-1.0` | Consequence if we do not settle it |
|---|---|---|---|
| Does dilation scale window **timestamps**? | **Yes** — windows are measured in the scaled per-entity clock, so a dilated window aligns with the montage | **No** — "`EndGameplayTime` is in **undilated** gameplay time; a dilated window still ends at the same gameplay time" | With a 100 ms hitstop, A2's window would end 100 ms of *gameplay* time earlier relative to its own animation. The parry window the player sees would be shorter than the window I evaluate, or vice versa. This is a **1-frame-level fairness bug**, not a bookkeeping difference |
| Pause | Freeze, no drift | Freeze, no drift | **Agreed in substance** (two documents, not a signature) |
| Late subscription | Must not synthesise a start; parry is evaluated as **same-frame phase overlap**, never by timestamp subtraction | Must not synthesise a start; every message carries `StartGameplayTime` so a late consumer can compute remaining window | **Compatible in substance** — both reject synthesis. Mine adds the overlap rule so a late consumer cannot pass a stale check |

**My proposal to close it without a TD ruling is impossible** — the two readings produce different player-visible timing, so this is a genuine `UNRESOLVED` item for TD-06. I state my reading and why; I do not adopt A2's.

**What I will not do:** evaluate parry by subtracting timestamps. Even with a perfect clock, timestamp subtraction lets a check pass one frame late; the rule that matters is *phase overlap on the frame the hit resolves*, with the phase derived from `T_attacker` and the defender's live parry tag. Timestamps are for scheduling and diagnostics.

### 7.4 Where C-05 stands

| Item | Status |
|---|---|
| Four-message lifecycle, exactly-once close | **MY PROPOSAL**, unchanged |
| Telegraph never applies damage | **MY PROPOSAL**, unchanged; A2 states the same boundary independently |
| Clock | **UNRESOLVED** — TD-06; my concrete definition in R5-1 |
| Dilation semantics | **UNRESOLVED** — direct divergence with A2 (§7.3) |
| Late-subscriber query surface | **UNRESOLVED** — event-only vs event + query |
| Tests | `TEST PROPOSED` only |

---

## 8. C-06 — Interaction: **REVISED**

### 8.1 What v1.2 says — **CONFIRMED DECISION**

v1.2's register: interaction lifecycle Core-owned; escalate **whether damage interrupts a hold** to TD/design if the agents do not agree; "do not adopt A2's suggested default or A1's proposed behavior as a decision". TD-07 asks me to clarify hold-progress ownership.

### 8.2 Revision R6-1 — progress becomes **opt-in** for the interactable (`A1-R1` §6.2, §6.4)

`A1-R1` had the router calling `TickInteract(Progress01)` every frame on every interactable. A2 states plainly that the world object does **not** consume progress, does not own the timer, and would only accept an optional read-only callback.

**My revision, and it is a real simplification:**

| Before (`A1-R1`) | After (`A1-R2`) |
|---|---|
| `TickInteract(ctx, Progress01)` called every frame on every interactable | Prompt data carries `bWantsProgress` (default **false**). `TickInteract` is called **only** when true |
| Progress delivery part of the lifecycle | Progress remains **entirely inside the router**; the world sees `Begin → (optional Tick) → End(Completed / Failed / Refused)` **or** `Cancel(reason)` |
| A2's "begin/end/cancel only" read as a divergence | It is now the **default behaviour**; the difference closes with no loss to me |

**Ownership answer (TD-07):** the **router** owns hold duration, progress integration and the completion instant, because it must be frame-accurate, cancellable by player state, and identical across every interactable type. The world object owns whether the action is legal and what completion means for its own local state. **A2's position and mine are now compatible**: they never time anything, and they never need progress unless they ask for it.

### 8.3 Revision R6-2 — the damage-interrupt question, escalated rather than assumed

`A1-R1` §6.5 asserted damage cancels a hold. A2 says that is a design decision with combat-feel consequences and explicitly declines to assume it. The reconciliation instructs that neither default be adopted.

**My position, stated as a proposal and not as a ruling:** sustained actions should break on damage — otherwise "hold to read the memory fragment while being hit" is a viable tactic and the interaction system becomes a defensive option nobody designed. **But I do not own this decision**, and the implementation cost either way is one boolean.

| Ruling | Implementation |
|---|---|
| Damage interrupts (my proposal) | `Cancel(Damaged)` fires after the attribute commit, before control-state resolution — as `A1-R1` §6.5 already specified |
| Damage does not interrupt | Router ignores damage, continues while `ControlState` permits; only stagger/death/cinematic cancel |
| Configurable | Per-interaction `bDamageInterruptsHold`, default decided by the ruling, not by me |

**Escalated as a design decision.** Until ruled, my code would ship the interrupt behaviour and it would be labelled as a default, not a settled rule.

### 8.4 Where C-06 stands

| Item | Status |
|---|---|
| Router owns focus/input/hold/terminal call; never grants progression | **MY PROPOSAL**, unchanged |
| Hold progress delivery | **MY PROPOSAL**, revised: opt-in (R6-1); ownership answer given |
| Damage-interrupts-hold | **UNRESOLVED** — design escalation (§8.3) |
| Interface extension (`EndResult`, `CancelReason`) | **MY PROPOSAL**; A2's own interface shape is close but not identical — see §11 |
| Completion fact vs progression grant | Compatible direction; exact event shape **UNRESOLVED** with A2 |
| Tests | `TEST PROPOSED` only |

---

## 9. C-07 — IDs and tags: **CLARIFICATION REQUIRED**

### 9.1 Why this one cannot be "REVISED" by me

Three reasons, none of them a disagreement with v1.2:

1. **v1.2 grants no namespace and no policy** — "No namespace or save policy is granted here" (reconciliation §3 C-07). I cannot revise toward a decision that does not exist.
2. **A2's inventory and mine use incompatible spellings for the same concepts** (§9.2). Choosing between them is registry governance, which is Agent 3/TD's, and either choice changes permanent compatibility surface.
3. **Retirement policy depends on save references I do not own** — the save system is Agent 3's, and whether an interactable or route identifier appears in a save is not knowable from my documents.

### 9.2 The concrete collisions, so they are not discovered later

| Concept | `A1-R1` (me) | `A2-C07-1.0` | MEAD (accepted architecture) | Conflict |
|---|---|---|---|---|
| Staggered status | `Status.Staggered` | `Combat.State.Staggered` | `Status.Staggered` (MEAD §5.1) | **Same concept, two namespaces.** MEAD already fixes `Status.*`; A2's namespace would create a second vocabulary |
| Interaction verbs | `Interact.Verb.Open/Read/Take/Talk/Climb/Rest/Examine` | `Interaction.Verb.Open/Take/Inspect/Climb/Listen/Read` | Verb is "a `FGameplayTag`" with no namespace fixed (MEAD §4.5) | **Three-way mismatch**: `Interact.Verb` vs `Interaction.Verb`, plus different verb sets (`Read`/`Talk`/`Rest`/`Examine` vs `Listen`/`Inspect`) |
| Damage type | `Damage.Physical.Slash/Blunt/Pierce` | `Combat.Damage.Slash/Impact/Root/Thunder` | `Damage.Physical.Slash` (MEAD §5.2) | **MEAD already fixes `Damage.*`.** A2's `Combat.Damage.*` would duplicate it; `Root`/`Thunder` are new damage classes I have no reaction data for |
| Telegraph cancellation | close-reason **enum** (`ETDDTelegraphEndReason`) | `Telegraph.Cancel.SourceDied/SourceUnloaded/AttackInterrupted` | — | Enum vs tags for the same four values. One of them is redundant; I prefer the enum (compile-time exhaustiveness) |
| Traversal capability | `Traversal.Capability.*` (names mine) | `Traversal.Capability.*` (names deferred to me) | — | **Compatible**; A2 defers correctly |
| Traversal state | — (my outcomes are enums) | `Traversal.State.Blocked/OneWay` | — | Would duplicate my `BlockedPath` outcome and my `bOneWay` authored flag |
| Interaction mode | `HoldDurationSeconds` (float; 0 = tap) | `Interaction.Mode.Tap/Hold` | — | Float vs tag. A float expresses "1.35 s"; a tag cannot, and a per-verb hold duration is a real design need |

### 9.3 Revision R7-1 — my own requests narrowed, and two yielded

I am **not** asking the registry to carry both spellings. Concretely:

- **Yield to MEAD:** `Damage.Physical.*` and `Status.*` are already fixed by the accepted architecture. I withdraw nothing, but I note that A2's `Combat.Damage.*` and `Combat.State.*` should map onto them, not beside them.
- **Yield on mode:** I withdraw any implied tag for the tap/hold distinction. `HoldDurationSeconds` (0 = tap) is sufficient and carries the duration; a mode tag adds nothing.
- **Hold on telegraph reasons:** I keep the enum and request A2 confirm they need tags for anything the enum cannot carry.
- **Keep:** `Traversal.Capability.*` (five names), `Interact.Verb.*` (naming open), `Status.Interacting`, `Status.Traversing`, `Status.Airborne`, `Status.LockedOn` (all requested from the registry, none granted).

### 9.4 What is required before namespaces and retirement policy can be approved (TD-08)

| # | Required input | Owner | Why it blocks |
|---|---|---|---|
| 1 | One canonical namespace list, published by the registry | Agent 3 | Until `Status.*`/`Combat.State.*` and `Damage.*`/`Combat.Damage.*` are resolved, every authored attack and every AI condition is written against a guess |
| 2 | A named consumer and a decision for **every** requested tag | A1 + A2 | A tag with no consumer is permanent surface with no purpose. This is the same rule `A1-R1` §2.3 applied to fields |
| 3 | The **save schema inventory**: which authored ids appear in saves | Agent 3 (save owner) | Retirement policy cannot be stricter than the save data; if no save references a route, routes need no tombstone |
| 4 | Whether interactables persist anything (A2's `C07-Q3`) | Agent 3/TD | Determines whether an interactable id family exists at all — A2 explicitly refuses to invent one, correctly |
| 5 | Register provenance/version for canon ids | A2 (has it) | Ids derived from a register must name the version they came from |
| 6 | Validator rule: unknown tag is an **author-time error**, runtime is log-and-ignore | Agent 3 | Otherwise the same typo is sometimes fatal and sometimes silent |
| 7 | Retirement = tombstone, **never reuse** | Agent 3/TD | Non-reuse is the only property that makes a save reference permanently meaningful |
| 8 | Decision on which vocabularies are **tags** and which are **enums** | TD/Agent 3 | `World.Access` is register vocabulary; whether it must be a tag is a governance choice, not a data fact |

**Evidence I can supply from my side, now:** the complete list of tags and ids Agent 1 produces or consumes (`A1-R1` §7.3, revised in R7-1), all of them `REQUESTED` and none assumed granted. **Evidence I cannot supply:** save schema, register versions, registry host.

---

## 10. The nine TD items

### 10.1 TD-01 — governing document version and visibility — **CLOSED**

| Question | Answer |
|---|---|
| Which version governs? | **`TDD-TD-INT-001` v1.2**, commit `e121bbb…`, acknowledging v1.1 as its governing baseline |
| What was the visibility problem? | v1.2 was absent from the packet baseline `50b1431` and from `main` `5e3d1da`; it exists on Agent 3's branch and is reachable by SHA |
| Did it change my proposals? | **No**, verified contract by contract in §2 |
| Is my earlier statement retracted? | The *factual* claim ("not present in the repository") is **corrected** — it was not present in the sources I could see; it exists. The *consequence* claim ("must be re-based if v1.2 differs materially") is **resolved**: it does not differ materially |
| Status | **CLOSED.** No further action from me |

### 10.2 TD-02 — stagger classification — **PREFERENCE STATED, DECISION OPEN**

Preference: `ETDDStaggerClass { Never, Always, OnPostureBreak, OnParryOnly }` (option B). Implications, fallbacks and the reason the GAS option is excluded are in §6.2. **I am not treating my preference as a decision**, and I will implement the bool without complaint if that is chosen. Needed before M3, not now.

### 10.3 TD-03 — applied-event scope — **POSITION COMPLETE, RULING NEEDED**

Fully specified in §5.3–§5.4: blocked yes / parried yes / immune no / miss no / rejection no; `Amount` = clamped health delta; `PostureDelta` added; **A1 is the single publisher**; target unload drops the event (accepted from A2); `RequestId` + `HitEventId` + `SequenceNumber`; per-source ordering only. Two items remain for the TD: whether "blocked publishes an event" is acceptable as shared semantics, and whether A1 as sole publisher for A2-owned targets is confirmed.

### 10.4 TD-04 — RouteId stability, persistence, save references — **CLARIFIED**

| Question | Answer |
|---|---|
| Stability | **Permanent; never reused.** A retired route stays retired |
| Persistence | Depends on whether anything saves a route reference. **From Agent 1's side, nothing does**: M1 v1.4 persists no traversal state, and my telemetry is not a save |
| Save references | If narrative, checkpoints or memory gating reference a route, that reference must be tombstone-governed; if none does, a route key may be renamed per level edit with no migration |
| Format dependence | My requirements are P1–P5 (§3.2), satisfied by A2's location-anchored key. **I do not require a specific syntax** |
| Namespace | `ROUTE-` belongs to A2's authored keys; I request no namespace of my own in that space |
| What I need from the TD | Confirmation that **no Agent 1 save field will reference a route key in the vertical slice** — which is my current design intent, and which keeps route retirement out of the save-compatibility path |

### 10.5 TD-05 — stealth/noise exclusion — **CONFIRMED, with a stated revisit condition**

| Item | Position |
|---|---|
| Stealth / noise fields | **Excluded.** No approved stealth design, no named consumer, no decision that fails without them |
| Health / posture | **Excluded** as well (§4.2) — A2 withdrew health; posture was never requested |
| Revisit condition | All three must exist: (1) an approved design, (2) a named consumer with a decision it cannot make otherwise, (3) an explicit statement of the units and the freshness needed. Then it is a C-02 revision, not a silent field addition |
| Risk I am accepting | If stealth is designed in Chapter 2, the player context grows a field late. That is cheaper than carrying a fabricated field for months |

### 10.6 TD-06 — canonical gameplay clock — **PROPOSED, DIVERGENCE RECORDED**

Proposed clock, formula and per-entity rationale: §7.2. Pause freezes; global dilation and pair-hitstop both scale; both participants read their own `T_e`. **The divergence with A2's undilated-window reading is recorded in §7.3 with its player-visible consequence** (a 100 ms hitstop would misalign the window by 100 ms of gameplay time). I cannot settle it from my side and I do not adopt theirs.

### 10.7 TD-07 — interaction hold progress — **CLARIFIED, AND THE FRICTION REMOVED**

Router owns hold duration, progress and the completion instant (§8.2). The interactable receives progress **only if it opts in** via `bWantsProgress`. A2's "begin/end/cancel only" is therefore the default and no longer a divergence. The remaining decision — **does damage interrupt a hold** — is escalated as design, not technical (§8.3).

### 10.8 TD-08 — tag namespaces and retirement — **WHAT IS NEEDED, LISTED**

Eight inputs in §9.4, with owners. The blocking ones are the canonical namespace list (Agent 3) and the save inventory (Agent 3). Until then I hold my inventory as **requested**, register nothing, and do not publish a competing registry.

### 10.9 TD-09 — MEAD §5.4 and attacker-driven hit handling — **RESOLVED BY ROLE SEPARATION; CONCERN MAINTAINED ON THE DOCUMENT**

**The six roles, separated explicitly. This is the substance of my answer:**

| Role | Owner | What it means | What it must never imply |
|---|---|---|---|
| **1. Attack authorship** | A2 for enemies, A1 for the player | Who authored the attack: montage, timing, damage intent, hit volumes, telegraph | Authorship does not confer arbitration. Writing "this attack has a 20 cm blade" is not deciding whether it connected |
| **2. Hit detection** | **A1** for every hit involving the player | Volume/overlap evaluation against the player capsule, within the authored window | A2 proposing volumes is data; computing the overlap is authority |
| **3. Arbitration / resolution** | **A1, exclusive**, for every hit involving the player | Dedupe, window validity, ordering, outcome classification (`Applied`/`Blocked`/`Parried`/`Immune`/…) | No second arbiter, no A2-side outcome guessing |
| **4. Defence / mitigation evaluation** | **A1, exclusive**, for the player as victim | Immunity tags, block guard, parry window overlap, posture arithmetic | A2 must not evaluate the player's defence; it supplies intent only |
| **5. Health / attribute application** | The **target's owner**: A1 for the player, A2 for its own actors | The single GAS attribute write, clamped, exactly once | Applied only after (3) authorised it, returning the applied delta |
| **6. Applied-event publication** | **A1, single publisher** (§5.4) | One event per applied hit, after (5) returns | A resolution is not a fact; only an application is |

**Where MEAD §5.4 stands.** The diagram reads `Attacker CombatComponent → FTDDDamageRequest → ITDDDamageable::ApplyDamage → victim's UTDDCombatComponent`. Read as a **flow of authorship and initiation**, it is correct and I have no objection. Read as a statement of **arbitration authority**, it conflicts with the TD integration decision for hits where the player is the victim, because it would let the attacker's code run defence and outcome logic against the player.

**My position:** the diagram is an authorship/initiation diagram and should be **annotated as such**, not deleted. Concretely, I request one of:
- (a) an erratum note on MEAD §5.4 saying arbitration and defence for hits involving the player are Agent 1's alone; or
- (b) an ADR recording the authority split; or
- (c) an explicit TD statement that option 1 (`A1-R1` §8.1) is the ruling, which Agent 3 then reflects in the next reconciliation.

**I maintain the concern until one of those exists**, because a reader of MEAD alone would implement two arbiters, and §5.4 is a normative architecture section. This is not a disagreement with any decision — it is a request that a decision be recorded where the code will be written against it.

**One consequence worth stating:** under this split, A2's proposed `FTDDHitIntentRequest` is *authorship data* (role 1) that A1 consumes as a request (role 2/3). That is a clean fit. Their statement that they "do not compute whether the volume overlaps the player" is exactly right under this split, and it is the strongest evidence in their submission that they intend the same boundary.

---

## 11. Agent 2's sixteen dependencies — answered where I can

A2 lists 16 items, seven `High`. Answering them is the fastest route to bilateral review; **answering is not agreeing**, and A2 must still review this exact version.

| # | A2 item | Severity | My answer in `A1-R2` | Status |
|---|---|---|---|---|
| 1 | Capability enum and names | High | Five names given: `Vault`, `Mantle`, `LedgeShimmy`, `Drop`, `ClimbLadder` (§3.3) | **ANSWERED** |
| 2 | Requirements: data or code | High | **Data** — tag container + AND/OR grouping, no code predicates (§3.3) | **ANSWERED** |
| 3 | Cumulative vs independent; revocable | Medium | Independent set membership; revocable; per-query evaluation; no mid-execution abort (§3.3) | **ANSWERED** |
| 4 | Traversal context (water/rope) | Medium | Out of scope in this slice; would be a new capability + contract revision (§3.3) | **ANSWERED** |
| 5 | C-02 field list; `Velocity`, `CameraForward` | Medium | `Velocity` already published; `CameraForward` **accepted**; `AimDirection` is separate; health/posture **removed**; `CarryState` **not provided** (§4) | **ANSWERED** |
| 6 | Event-vs-query split | Low | Both provided: query per frame + discrete-change events; your scoring-vs-commit rule adopted (§4.6) | **ANSWERED** |
| 7 | Applied event payload | High | Full payload in §5.3: `Amount` clamped, `PostureDelta`, `Outcome`, `bLethal`, ids, sequence, time | **ANSWERED** |
| 8 | Confirm resolution not published as fact | Medium | Confirmed. Only applied events and state events are published; resolutions are local (§5.3) | **ANSWERED** |
| 9 | Target-unload drop policy | Low | **Accepted** — drop, no event, one diagnostic (§5.4) | **ANSWERED** |
| 10 | Outcome event shape; `ResolutionId` scope | High | **No `ResolutionId` is published.** Correlate on `RequestId`/`HitEventId`; outcome events are the applied event plus `FTDDControlStateChangedEvent` (§5.2, §6.3) | **ANSWERED** |
| 11 | Is there a recovery event? | High | **Yes, as a notification only** — `FTDDRecoveryCompletedEvent` (§6.3) | **ANSWERED** |
| 12 | Gameplay-time and pause confirmation | High | Proposed clock with formulas (§7.2); **dilation semantics still diverge** (§7.3) | **PARTIAL — divergence** |
| 13 | `CancelReason` vocabulary | Medium | Five close reasons (`Completed`, `Cancelled`, `Interrupted`, `SourceDied`, `SourceUnloaded`, `Superseded`); prefer enum to `Telegraph.Cancel.*` tags (§9.2) | **ANSWERED (proposal)** |
| 14 | `ITDDInteractable` final shape | High | Extended with `EndResult` + `CancelReason`; progress now **opt-in** (§8.2) | **ANSWERED (proposal)** |
| 15 | `CanInteract` call frequency | Medium | Called **once per router tick for the focused candidate only**, not for all candidates — no per-candidate allocation (§8.2) | **ANSWERED** |
| 16 | Traversal capability tags | — | Blocked on #1, now answered: five `Traversal.Capability.*` tags requested (§3.3, §9.3) | **ANSWERED** |

**Fifteen of sixteen answered, one partial** (dilation semantics). None of these answers constitutes agreement between the agents: A2 must review `A1-R2` and state `AGREE`/`DISAGREE`/counterproposal per contract.

---

## 12. What is confirmed, proposed, unresolved — and what was actually run

### 12.1 CONFIRMED DECISIONS (not mine to change)

1. `TDD-TD-INT-001` v1.2 is the governing addendum (§1.2).
2. Agent 1 owns player state mutation, traversal execution, player-involving hit arbitration, damage application authority and player-side interaction routing.
3. Locomotion, action/control and combat status remain separate taxonomies.
4. **Dead (100) > Cinematic (90) > Stagger (80)**, single winner, no interleaving of a resolving fallback.
5. M1 v1.4 damage taxonomy, `AbortWindow`, two-phase placement validation, bounded relocation + always-run terminal hold, restoration ordering, out-of-world handoff — preserved without reinterpretation.
6. Health application independent of control-state resolution.
7. `bCausesStagger` is **not** an approved permanent field.
8. TDD is canonical; Agent 2's skeleton is not adopted.
9. No contract of mine is agreed by Agent 2, and none is frozen.

### 12.2 MY PROPOSALS (new or revised in `A1-R2`)

| ID | Proposal | Contract |
|---|---|---|
| P-01 | Route identity required as properties P1–P5, format-agnostic | C-01 |
| P-02 | Capability set semantics: independent, revocable, per-query, no mid-execution abort | C-01 |
| P-03 | World-facing projection of the seven query outcomes (total, one lossy point) | C-01 |
| P-04 | Health/posture removed from the context surface; phase-condition query instead | C-02 |
| P-05 | `bInCombat`, `CameraForward` added; `AimDirection` documented as distinct | C-02 |
| P-06 | `RequestId` + `HitEventId` + `SequenceNumber`; dedupe on `(SourceEntityId, RequestId)` | C-03 |
| P-07 | Applied-event scope table, clamped `Amount`, `PostureDelta`, A1 single publisher | C-03 |
| P-08 | Target-unload drops the event (accepted from A2) | C-03 |
| P-09 | `ETDDStaggerClass` preferred; bool acceptable; GAS effect excluded on ordering grounds | C-04 |
| P-10 | `FTDDRecoveryCompletedEvent` as notification only | C-04 |
| P-11 | `UTDDGameplayTimeSubsystem` with per-entity scaled clocks; formula in §7.2 | C-05 |
| P-12 | Progress opt-in (`bWantsProgress`); router owns progress | C-06 |
| P-13 | Damage-interrupts-hold as design proposal, with the configurable escape hatch | C-06 |
| P-14 | Tag-collision resolution: yield to MEAD `Status.*`/`Damage.*`, drop mode tags, keep telegraph enum | C-07 |

### 12.3 UNRESOLVED (needs a decision that is not mine)

| ID | Item | Owner | What it blocks |
|---|---|---|---|
| U-01 | `ETDDStaggerClass` vs bool vs tag mapping (TD-02) | TD | M3 combat authoring |
| U-02 | Applied-event shared semantics + A1-as-sole-publisher confirmation (TD-03) | TD | A2 reaction code |
| U-03 | Whether any Agent 1 save field references a route key (TD-04) | TD | Route retirement policy |
| U-04 | `CarryState` — does a carry system exist, and does Chapter 1 gate on it? | TD/design | C-02 completeness; route gating |
| U-05 | Does dilation scale window timestamps? (mine yes, A2's no) | TD (TD-06) | Parry fairness; one implementation or the other is wrong |
| U-06 | Clock ownership: Core subsystem vs per-module | TD (TD-06) | Both producers' timestamps |
| U-07 | Late-subscriber query surface: event-only vs event + snapshot | TD | C-05 lifecycle completeness |
| U-08 | **Does damage interrupt a hold?** | TD/design | C-06 cancellation matrix |
| U-09 | Completion fact event shape (A2 emits `FTDDInteractionCompleted`, I emit an end result) | A1/A2 + TD | Interaction completion contract |
| U-10 | Canonical tag namespaces (four concrete collisions, §9.2) | Agent 3 | Every authored attack, every AI condition, every interactable prompt |
| U-11 | Save schema inventory → retirement policy; interactable persistence | Agent 3 (save) | C-07 identity families |
| U-12 | MEAD §5.4 annotation/erratum (TD-09) | TD | A reader implementing from MEAD alone would build two arbiters |

### 12.4 DEPENDENCIES

**On Agent 2:** marker representation and registration; field-by-field confirmation of the C-02 matrix; explicit confirmation of exclusive A1 arbitration for player-victim hits; telegraph producer agreement on my four-message lifecycle; completion-fact shape; its own tag inventory after collisions are resolved; and an explicit `AGREE`/`DISAGREE` review of `A1-R2`.

**On Agent 3/TD:** registry and namespace decision; save inventory; Core placement of every struct I request (I request fields, I do not author types); clock ownership; and the TD-02/TD-03/TD-09 rulings above.

**On nobody in this session:** the Unreal toolchain. Nothing here can be built, run or measured in this workspace (ADR-0012).

### 12.5 Test status — proposed versus executed

**Executed: none. Zero tests, zero builds, zero runtime checks in this document and in `A1-R1`. No Unreal Engine, compiler, editor or automation harness exists in this workspace (ADR-0012).**

| Contract | Proposed tests (`TEST PROPOSED`, none written) | Change from `A1-R1` |
|---|---|---|
| C-01 | `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics`; `TDD-Functional.Traversal.MarkerStreamingLifetime`; **new** `TDD-Contract.Traversal.WorldProjectionTotality` (every outcome projects; `Cooldown` retains its reason) | +1 |
| C-02 | `TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation` (10 cases); **new** `TDD-Contract.PlayerContext.ConditionalFieldAbsence` (health/posture absent; a consumer referencing them fails to compile) | +1 |
| C-03 | `TDD-Contract.Combat.SingleDamageApplicationAndEvent` (13 cases); **new** `TDD-Contract.Combat.EventScopeMatrix` (blocked/parried/immune/miss/rejection × event emitted or not; `Amount` clamped; single publisher) | +1 |
| C-04 | `TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification` (14 cases); **new** recovery-notification case (notification strictly after commit; cannot be raised by a consumer) | +1 case |
| C-05 | `TDD-Contract.Combat.TelegraphWindowConsumerSemantics` (12 cases); **new** `TDD-Contract.Combat.ClockDilationAlignment` (montage vs window drift ≤ 1 frame across 3 hitstops; pause freezes; resume preserves remaining duration) | +1 |
| C-06 | `TDD-Contract.Interaction.PlayerRoutingAndCancellation` (14 cases); **new** progress opt-in case (`bWantsProgress=false` → zero `TickInteract` calls) | +1 case |
| C-07 | `TDD-Contract.Core.Agent1IdAndTagRegistry` (9 cases); **new** collision-resolution case (no concept registered under two namespaces) | +1 case |

The M1 v1.4 suite (`TDD-Unit.Movement.FallbackResolution`, `TDD-Functional.Movement.TraversalAbortPaths`, `TDD-Functional.Movement.TraversalExitRevalidation`) remains the authority for fallback/hold behaviour and is **not replaced** by any contract test.

### 12.6 Scope compliance

| Restriction | Compliance |
|---|---|
| No shared Core types created | None. I request fields and name them `PROPOSED` |
| No C++ / gameplay implementation | None |
| No Unreal project | None; `Source/`, `Config/`, `Content/` remain empty |
| No branch merge | None; only `arena/3bc206a0-tdd` touched |
| No API freeze | None; every shape `PROPOSED — NOT FROZEN` |
| No M0 claim | None; M0 remains not passed |
| No inferred Agent 2 agreement | None. A2's submission is cited as counterpart material only |
| `A1-R1` preserved | Unmodified at blob `25ab47c2…` |

---

## 13. Publication

| Field | Value |
|---|---|
| Document | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md` |
| Version | 1.1 (`A1-R2`) — supersedes `A1-R1` **for review purposes only**, not as evidence and not as a replacement of the historical record |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `f578fe612ad173b74f99fcb187f825eb3de6f59a` (this document); previous commit `97828db…` carries `A1-R1` |
| Prior document | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md`, `A1-R1` v1.0, commit `97828db7d9786c0fa5415578e796a822aab497a8`, blob `25ab47c2…` — **preserved unchanged** |
| Governing addendum | `TDD-TD-INT-001` v1.2, commit `e121bbbf09562e3cba0efe81aad971809685db23` |
| Status | `DESIGN_ONLY`; proposals `PROPOSED — NOT FROZEN`; tests `PROPOSED / NOT RUN` |
| Core types / code / project / merge / M0 | **None** |

### 13.1 Change log

| Version | Date | Effect |
|---|---|---|
| `A1-R1` v1.0 | 2026-11-16 | Initial submission against v1.1 (v1.2 not visible): seven contracts, twelve fields each, nine TD issues |
| `A1-R2` v1.1 | 2026-11-16 | Acknowledged TD v1.2 as governing; confirmed it changes **no** proposal; six contracts revised (C-01, C-02, C-03, C-04, C-05, C-06) and one marked `CLARIFICATION REQUIRED` (C-07); resolved TD-01 and answered TD-02…TD-09; answered 15 of Agent 2's 16 dependency items; separated confirmed decisions, proposals, unresolved items, dependencies and test status |
