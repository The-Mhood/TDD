# AGENT 2 — CONTRACT SUBMISSION, C-01 TO C-07

**Document:** `TDD-A2-CONTRACT-SUB-001` · **Version:** 1.0
**Date:** 2026-11-16 UTC
**Submitting:** Agent 2 — World, Systems and Gameplay Simulation
**To:** Agent 3 / Technical Director (consolidation), Agent 1 (counterpart signature)
**Responds to:** `TDD-A2-CONTRACT-PACKET-001` v1.0 (`docs/AGENT2_CONTRACT_SUBMISSION_PACKET_V1.md`, commit `50b14318c8089dedcc688fb2c78ad3cb361c15f5`)
**Governing document as received:** `TDD-TD-INT-001` **v1.1**

**Status:** `PROPOSAL — NOT FROZEN — AWAITING AGENT 1 AND TD`
Nothing in this document is an accepted interface. No Core API exists, no Unreal project exists, and no runtime behaviour is claimed. Every type name, field name and signature below is **PROPOSED — NOT FROZEN**.

---

## 0. Reading notes — three things to settle before §1

### 0.1 The request cites a governing document that does not exist

The submission request names **`TDD-TD-INT-001` v1.2**. No v1.2 exists in this repository.

| Checked | Result |
|---|---|
| `origin/main` | `5e3d1da` — no `docs/` tree |
| Commit `50b1431` (the packet's own commit) | contains v1.0 and **v1.1**; no v1.2 |
| `Docs/` on this branch | no `TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md` |
| `git log --all` | no commit introducing v1.2 |

I have therefore answered against **v1.1**, the highest version that exists, and against the packet itself. If v1.2 exists outside this repository, three of its decisions could change my answers and I would need to revise:

1. any change to **Dead (100) > Cinematic (90) > Stagger (80)** — C-04 is built on exactly this ordering;
2. any change to the **C-08 reconciliation** — §0.2 below depends on it;
3. any change to the ownership split in §1 of the packet — every contract here is written against that split.

**Requested of Agent 3/TD:** confirm v1.1 is intended, or supply v1.2. I have not invented its contents.

### 0.2 C-08 is reconciled in my favour, and I am accepting that result

The W-M2.3 submission reported 29 exact / **5** bounded / 1 unbounded / 11 uncaptured = 46 and flagged that the TD's stated 6 bounded summed to 47. v1.1 §6.1 independently reconciles to **5 bounded** against the verbatim fixture and both generated JSON artifacts, and closes C-08 for the stated count.

**I accept that reconciliation and record no dispute.** C-08 does not close C-09 (`CH01-SCN-014` remains unbounded, awaiting a Creative Director decision).

### 0.3 What I am and am not submitting

| I am submitting | I am not submitting |
|---|---|
| World-side requirements and proposed data shapes | Core API implementation |
| Named consumers with a concrete decision each | Any claim that Agent 1 has agreed |
| Failure/cancellation/invalidation semantics | Frozen identifiers |
| Named acceptance tests with measurable assertions | Evidence that those tests exist or passed |
| Exact register IDs and source versions | Chapter 2–8 data (not ingested) |

**No implementation is included, no branch is merged, no Unreal project is created, and no gameplay code is written** — as the request requires.

### 0.4 Standing constraints I have honoured

- **Pending-approval content.** `CH01-SUB-001` (PENDING APPROVAL) and `CH01-SUB-018` (PROPOSED) appear in this document only as *identifiers in reference data*. No final art, cultural property, shrine, mask, ritual or narrative decoration is introduced. Where a contract touches them, it is labelled `PENDING APPROVAL — BLOCKOUT ONLY` per CD-5.
- **Enemy archetypes remain PROPOSED.** C-03 and C-05 cite archetype names only as *data rows that do not yet exist*; none is promoted by this document.
- **Cultural consultant gate open.** `RULE-CULTURAL-FICTIONALITY` and `RULE-CH06-MASK-INVENTED` are carried as data validation rules, not resolved.
- **No competing Core types.** Every type below that lives in `TDDCore` is *requested from* Agent 3/TD, not authored by me.

---

## 1. Executive summary

| | |
|---|---|
| **Contracts proposed** | 7 of 7 |
| **Contracts agreed** | **0 of 7** — Agent 1 has not responded |
| **Contracts frozen** | **0** — nothing here is frozen |
| **TD decisions requested** | **7** (§11) |
| **High-severity dependencies on Agent 1** | **7 of 16** (§10) |
| **Acceptance tests named** | **42**, of which **10 are L0-data** |
| **Of those 10, executable today** | **3** — `TraversalCategoryIsMultivalued`, `IdDuplicateDetection`, `IdDisplayLabelNeverAKey` (partially). The other 7 need route records, interactables or a tag registry that do not exist |
| **Independent checks in `contract_data_checks.py`** | **9**, all passing — these validate the *data claims in this document*, not the 42 contract tests |
| **Tests actually run for these contracts** | **0** — no route records or interactables exist |

### 1.1 The one substantive discovery in this submission

Reading `LOCATION_MASTER_REGISTER.md` v2.9 in full — rather than the 13-row excerpt I had
been working from — showed that the register's **`Category` field is multi-valued**. In
particular:

> "Traversal Area" is a **tag**, not an ID prefix. It appears on **8** Chapter 1 entries
> across four ID families, including `CH01-SUB-009 Streets` (**ESTABLISHED**),
> `CH01-SUB-020 The Back Lanes` and `CH01-EXP-003 The Forgotten Path`.

My own C-01 proposal had anchored routes on `CH0n-TRV-nnn`. **That was wrong**, and the
correction is in §3.2. A prefix-only selector would have silently excluded three
legitimate register locations — one of which is ESTABLISHED, so it cannot be withdrawn by
a canon review. This is now a named test that fails against a prefix-only parser.

The same read also corrected a second error of mine: `DOCS/AGENT1_TRAVERSAL_CONTRACT_REQUEST.md`
v0.1.0 labelled `TRV-002..005` as "PROVISIONAL". **They are register values.** That
document is corrected to v0.2.0.

### 1.2 What I am asking for, ranked

If only three things are resolved, these three decide the most:

1. **C-01 — is the capability enum data or code?** If code, offline reachability validation
   does not exist and every exploration-reward check becomes a playtest question.
2. **C-04 — is there a recovery-from-stagger event?** Without it, every world consumer must
   poll to learn a stagger ended.
3. **C-07 — does any interactable state persist?** This decides whether interactables need
   stable IDs at all, or whether they can be transient.

---

## 2. Summary table

| ID | Contract | My status | Agent 1 status | TD decision | Blocks |
|---|---|---|---|---|---|
| C-01 | Traversal vocabulary / route IDs / markers | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Exploration reachability; TRV-002..005 data |
| C-02 | Read-only player context | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Interaction gating; crowd density; telegraph targeting |
| C-03 | Damage / hit / applied event | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Enemy reaction; boss phase transitions |
| C-04 | Stagger / forced-state outcome | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Enemy AI response; encounter arming |
| C-05 | Telegraph timing / lifecycle | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Parry windows; boss telegraphs |
| C-06 | Interaction lifecycle | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | 13 candidate scenes; interactable count **not established** (§8.2) |
| C-07 | Shared IDs / Gameplay Tags | `PROPOSAL — NOT FROZEN` | `NOT RECEIVED` | `PENDING` | Everything above; save compatibility |

Seven proposals, zero agreements. No row may be marked agreed until Agent 1 signs the same version.

---

## 3. Cross-cutting positions

These apply to all seven and are stated once rather than repeated.

### 2.1 The read/request boundary

| Mode | I use it for | I never do |
|---|---|---|
| **Read-only snapshot** | Player position, locomotion, combat status | Write player state, mutate the snapshot |
| **Request** | "attempt this route", "this act landed", "interact completed" | Assume the request succeeded |
| **Broadcast** | Telegraph windows, damage-window intent | Apply damage myself |

Every proposed interface below is one of these three. There is no fourth.

### 2.2 Identity is typed, not stringly, and not a pointer

A recurring failure mode in this project's history was conflating stable content keys with runtime identities. Position taken:

| Kind | Example | Stable across save/load? | Valid across streaming? |
|---|---|---|---|
| Content key | `CH01-SCN-014` | **Yes** | **Yes** |
| Route key | `CH01-TRV-001/ROUTE-A` (proposed) | **Yes** | **Yes** |
| Runtime entity | `FTDDEntityHandle` (requested, C-07) | No | **No** |
| Transient actor | `AActor*` | No | **No** |

**Rule I propose:** every durable event carries a content key; every ephemeral event may carry a handle. A consumer that only needs to react "now" reads the handle. A consumer that must act after a reload reads the key. Mixing them is how a boss phase transition fires twice after a level stream.

### 2.3 Time

All timing in C-05 is in **gameplay time**, not wall-clock and not frame count. This is a request to Agent 1 to confirm, not an assertion: I cannot freeze a clock Agent 1 owns.

### 2.4 Data-versus-runtime separation, and what my evidence can support

My evidence in this repository is **Python data validation over register-derived fixtures**. It establishes that data is consistent and traceable. It establishes **nothing** about runtime behaviour. Every acceptance test below is labelled with its layer:

| Layer | Meaning | Can I produce it today? |
|---|---|---|
| **L0-data** | Python validation over authored data | **Yes** — this is what my existing suite does |
| **L1-unit** | Pure/unit test, no engine | Partly — logic yes, Unreal types no |
| **L2-auto** | Unreal automation | **No** — no engine, no project |
| **L3-map** | Functional/map test | **No** |

I am not claiming any L2/L3 test exists.

---

## 4. C-01 — Traversal vocabulary, route IDs, markers, queries, failure semantics

**Proposal version:** `A2-C01-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD (Core contract authority). I request publication; I do not publish. |
| **Implementation owner** | **Split.** Agent 1: traversal execution, capability resolution, abort semantics. Agent 2: route data, marker actors, authored requirements, world-side candidate supply. |
| **Producers (world side)** | `ATDDTraversalMarker` (proposed actor), `UTDDLocationRegistry` (SPEC), chapter manifest data (`Tools/world/data/CH01_manifest.json`) |
| **Consumers (named)** | Agent 1 traversal component; Agent 2 offline reachability validator; Agent 2 exploration gating |
| **Mutation authority** | I author and own route *data*. I must **not** mutate player locomotion, capsule state, or traversal execution state. Agent 1 must not author route requirement data. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank — for Agent 3/TD)* |

### 3.1 What I actually need, and why

The existing request document `Docs/AGENT1_TRAVERSAL_CONTRACT_REQUEST.md` v0.1.0 asked five questions and remains unanswered. This submission replaces "please tell me" with "here is a concrete proposal to react to", because a shape is easier to reject than a blank page.

The single most consequential question remains **§2.2 of that document**: are route requirements **data** or **code**?

- If **data**, I validate reachability offline and report unreachable exploration content as a build failure.
- If **code**, I need a query interface and reachability becomes a playtest question.

My proposal assumes **data**, with a code query as the resolution mechanism. If Agent 1 requires code authority, the `FTDDRouteRequirement` struct below collapses into an opaque `FGameplayTagContainer` and I lose offline validation — a real cost I am asking Agent 1 to weigh.

### 3.2 Route identity — proposed

```
PROPOSED — NOT FROZEN

FTDDRouteId
    FName Key;        // "CH01-TRV-001/ROUTE-A"
```

**Format:** `<LOCATION_ID>/ROUTE-<LETTER>`

| Property | Rule |
|---|---|
| Uniqueness | Per `LOCATION_ID`; the pair is globally unique |
| Source | `LOCATION_ID` is the register's (`LOCATION_MASTER_REGISTER` v2.9); `ROUTE-<LETTER>` is **mine**, not the register's |
| Stability | Permanent. A retired route is retired, never reused |
| Namespace collision | I request the `ROUTE-` segment be reserved to avoid colliding with Agent 1's own traversal identifiers |

**Why location-anchored rather than a flat counter:** a flat `TRV-0001` numbering would need a central allocator, and two agents authoring in parallel would collide. Anchoring to a register ID I already own removes that coordination cost entirely.

**Register basis (Chapter 1).** Read directly from `LOCATION_MASTER_REGISTER.md` v2.9
(Drive `1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5`, 534,140 bytes, read 2026-11-16).

**The register's `Category` field is multi-valued, and that breaks my own earlier
proposal.** "Traversal Area" is a *tag inside the category column*, not an ID prefix. It
appears on **8** Chapter 1 entries across **four different ID families**:

| Register ID | Name | Category tags | Canon |
|---|---|---|---|
| `CH01-SUB-009` | Streets | Sub-location, Exterior, **Traversal Area** | ESTABLISHED |
| `CH01-SUB-020` | The Back Lanes | Sub-location, Exterior, **Traversal Area** | PROPOSED |
| `CH01-TRV-001` | The Threshold Path | **Traversal Area**, Exterior, Story Location | PROPOSED |
| `CH01-TRV-002` | The Root Way | **Traversal Area**, Exterior | PROPOSED |
| `CH01-TRV-003` | The Stream Crossing | **Traversal Area**, Exterior | PROPOSED |
| `CH01-TRV-004` | The Ravine and Liana Bridge | **Traversal Area**, Exterior | PROPOSED |
| `CH01-TRV-005` | Roads | **Traversal Area**, Exterior | **ESTABLISHED** |
| `CH01-EXP-003` | The Forgotten Path | Exploration Area, Exterior, **Traversal Area** | PROPOSED |

Exploration Area is likewise multi-valued — **8** entries, `EXP-001..007` plus
`SUB-003 The Raffia Swamp`.

**Consequences I am accepting:**

1. **A route namespace of `CH0n-TRV-nnn/ROUTE-X` is wrong.** It would silently exclude
   `SUB-009`, `SUB-020` and `EXP-003`, all of which the register marks as traversal. The
   correct anchor is **any location whose category includes `Traversal Area`** — the ID
   prefix is not the discriminator.
2. `TRV-002..005` **are** authoritative register names (`The Root Way`, `The Stream
   Crossing`, `The Ravine and Liana Bridge`, `Roads`). My earlier request document
   `AGENT1_TRAVERSAL_CONTRACT_REQUEST.md` v0.1.0 listed the first three as
   "PROVISIONAL" — **they were not provisional; they are register values I had not then
   read.** That document's §3 identifier block understates its own authority and should be
   corrected. `TRV-005` (`Roads`) appears in neither document and is **ESTABLISHED**.
3. `SUB-009 Streets` and `TRV-005 Roads` are the two **ESTABLISHED** traversal-capable
   locations in Chapter 1. Any traversal contract should be exercised against those first,
   because they cannot be withdrawn by a canon review.

Revised route key proposal:

```
FTDDRouteId.Key = "<LOCATION_ID>/ROUTE-<LETTER>"
where LOCATION_ID ∈ { any CH01-* entry whose register Category includes "Traversal Area" }
```

The **anchor is the location, not the prefix**. A validator that only accepts `TRV-` would
reject three legitimate register entries — I have added a named test for exactly that.

### 3.3 Marker representation — proposed

I propose an **actor** (`ATDDTraversalMarker`) as the runtime representation and a **data record** as the authored one, because they have different lifetimes:

```
PROPOSED — NOT FROZEN

FTDDRouteRecord                       // authored, lives in DataTable, stable
    FName                    RouteKey;          // FTDDRouteId
    FName                    FromAnchorId;
    FName                    ToAnchorId;
    FTDDRouteRequirement     Requirement;       // §3.4
    ETDDRouteDirection       Direction;         // Bidirectional | OneWay
    FName                    ParentLocationId;  // register LOCATION_ID
    FName                    SceneId;           // CH01-SCN-nnn, may be None
    ETDDFailureMode          FailureMode;       // §3.5
    bool                     bCarryCompatible;
    FName                    EvidenceSource;    // register id + version

ATDDTraversalMarker                   // runtime, one per placed route
    FTDDRouteId              RouteKey;
    FTransform               EntryAnchor;
    FTransform               ExitAnchor;
    ETDDMarkerState          State;             // §3.6
```

**Why both:** the data record survives streaming and can be validated offline with no engine. The marker carries world transforms, which cannot be validated without geometry. Collapsing them would mean either losing offline validation or baking transforms into a DataTable that then drifts from the level.

### 3.4 Requirement representation — the debated part

```
PROPOSED — NOT FROZEN
```

Three alternatives, with my position:

| Alt | Shape | Offline validation | Agent 1 burden | My preference |
|---|---|---|---|---|
| **A** | `FGameplayTagContainer RequiredTags` | Yes, if tag registry is complete | Must implement tag→capability mapping | Acceptable fallback |
| **B** | Explicit `ETDDTraversalCapability` enum | **Yes, fully** | Must adopt my enum | **Preferred** |
| **C** | Opaque code predicate (`TFunction`) | **No** | Full authority | **Rejected** — loses all offline validation |

**I propose B with an A-compatible escape hatch:**

```
FTDDRouteRequirement
    TArray<ETDDTraversalCapability>  RequiredCapabilities;   // AND semantics
    TArray<ETDDTraversalCapability>  AnyOfCapabilities;      // OR semantics
    FGameplayTagContainer            AdditionalTags;         // Alt A escape hatch
    ETDDRequirementCombination       Combination;            // All | Any
```

**I am not settling the capability names.** That is Agent 1's decision and the TD prohibited me from freezing the enum. The names are placeholders; only the **shape** (an ordered set with AND/OR grouping and revocability) is my proposal.

**Open questions for Agent 1** (from the earlier request, still unanswered):
- Are requirements **cumulative** (A then B) or **independent** (A or B)?
- Can a requirement be **revoked** mid-chapter (e.g. a route closes once a carry is active)?
- Is there a **traversal context** (in-water, on-rope) that changes the available set? Chapter 1 contains water and ravine content (`CH01-TRV-003`, `CH01-TRV-004`), so this is not hypothetical.

### 3.5 Failure semantics — two different outputs

The packet asks me to distinguish **authoring validator** output from **runtime query** output. I propose these are different enums, because conflating them is how "invalid content" gets shown to a player as a flavour message.

**Runtime query result** — what Agent 1 tells the world:

| Value | Meaning | World behaviour |
|---|---|---|
| `Available` | Capability satisfied, route valid | Marker may present an affordance |
| `Unsupported` | Player lacks the capability | Silent. **No hint.** See §3.5.1 |
| `Blocked` | Temporarily blocked by world state (carry, one-way, gate) | Silent |
| `Unloaded` | Route not resident | Treated as absent, not as unavailable |
| `Invalid` | Marker/route data inconsistent | Logged; **marker hides** |
| `NoCandidate` | Nothing found | Normal, not an error |

**Authoring validator result** — what my offline check produces:

| Code | Severity | Meaning |
|---|---|---|
| `RTE-OK` | — | Resolvable |
| `RTE-MISSING-ANCHOR` | **Error** | `From`/`To` anchor does not exist |
| `RTE-ORPHAN-LOCATION` | **Error** | `ParentLocationId` not in registry |
| `RTE-DUP-KEY` | **Error** | Two records share a `RouteKey` |
| `RTE-UNKNOWN-CAP` | **Error** | Capability not in the accepted enum |
| `RTE-NO-EXIT` | **Error** | Bidirectional route with no `ToAnchor` |
| `RTE-UNREACHABLE` | **Warning** | Route exists but no path from chapter entry |
| `RTE-PENDING-BLOCKOUT` | **Info** | Route on PENDING APPROVAL content; blockout only |

#### 3.5.1 A blocked route should be silent, and this is a design position

If `Unsupported` produces an animation refusal or a UI prompt, then a blocked route cannot be used as a **legitimate signpost** — and Chapter 1's exploration design depends on the player reading terrain as negotiable or not. I request that `Unsupported` and `Blocked` be **silent** by default, with any refusal presentation being a per-route authored opt-in.

This is a request about *presentation*, not about Agent 1's execution. If Agent 1's M1 v1.4 behaviour already mandates an animation response, that is a **conflict to record**, not something I can override — M1 v1.4 is preserved by TD decision and I am not asking to change it.

### 3.6 Marker lifetime and invalidation

| Event | Required behaviour |
|---|---|
| Marker streams out | `State = Unloaded`; queries return `Unloaded`, **not** `Invalid` |
| Marker streams in | Re-register under the same `RouteKey`; no duplicate |
| Actor destroyed mid-attempt | Attempt **cancels**; no teleport, no stale transform write (M1 v1.4 rule) |
| Data version mismatch | Marker refuses to register; logs `RTE-UNKNOWN-CAP` |
| Two markers, same `RouteKey` | First registers; second logs `RTE-DUP-KEY` and disables |

### 3.7 Acceptance tests — proposed, none run

| Test ID | Layer | Setup | Measurable assertion |
|---|---|---|---|
| `TDD-Contract.World.TraversalRouteIdsAndMarkerValidation` | **L0-data** | Parse `CH01_manifest.json` + route records | Every `RouteKey` matches `^CH01-(TRV\|EXP)-\d{3}/ROUTE-[A-Z]$`; zero duplicates; zero orphan `ParentLocationId` |
| `TDD-Contract.World.TraversalRouteIdStability` | **L0-data** | Load fixture, mutate one route's letter | Validator emits exactly one `RTE-OK` change and no silent renumbering |
| `…TraversalCategoryIsMultivalued` | **L0-data** | Parse all CH01 location rows | Traversal-capable set == 8 entries incl. `SUB-009`, `SUB-020`, `EXP-003`; **a `TRV-`-prefix-only parser fails this test** |
| `…TraversalMarkerLoadUnload` | **L2-auto** | Spawn marker, stream out region, stream back in | `Unloaded` while out; re-registers with **identical** `RouteKey`; registration count == 1 |
| `…TraversalRequirementMatching` | **L1-unit** | Table of requirement × capability-set | `Available` iff requirement satisfied; AND/OR groups behave per `Combination` |
| `…TraversalUnreachableContent` | **L0-data** | Reachability graph from `CH01-ENV-001` | Every `CH01-EXP-*` reachable; else `RTE-UNREACHABLE` with the blocking route named |
| `…TraversalRuntimeUnavailable` | **L2-auto** | Query with marker absent | Returns `Unloaded`, never `Invalid`, never a crash |

**Tests I can run today:** the four L0-data ones, against route records that **do not yet exist**. They must fail (no data) until route authoring begins — that is the correct state.

### 3.8 Dependencies and unresolved questions

| # | Item | Owner | Status |
|---|---|---|---|
| C01-Q1 | Capability enum + names | Agent 1 | **unanswered** (since v0.1.0 request) |
| C01-Q2 | Requirements: data or code | Agent 1 | **unanswered** — decides offline validation |
| C01-Q3 | Cumulative vs independent requirements | Agent 1 | **unanswered** |
| C01-Q4 | Requirement revocation | Agent 1 | **unanswered** |
| C01-Q5 | Traversal context (water/rope) | Agent 1 | **unanswered** — and now evidenced: `TRV-003 The Stream Crossing` and `TRV-004 The Ravine and Liana Bridge` are both **PROPOSED** register entries, so this is not hypothetical |
| C01-Q6 | `ROUTE-` namespace reservation | Agent 3/TD | requested |
| C01-Q7 | `TRV-002..005` register rows | Agent 2 | **RESOLVED this submission** — read from register v2.9; my earlier "provisional" labelling was wrong, see §3.2 |

---

## 5. C-02 — Read-only player context and state snapshots

**Proposal version:** `A2-C02-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD publishes the Core type; **Agent 1 populates it** |
| **Implementation owner** | Agent 1 (provider). Agent 2 (consumer, read-only) |
| **Producers** | Agent 1 player controller / movement component |
| **Consumers (named)** | `UTDDInteractionRouter`, `UTDDCrowdSubsystem`, `ATDDChapterDirector`, `UTDDMemoryDirector` (eligibility), telegraph target selection (C-05) |
| **Mutation authority** | **Agent 1 exclusively.** I read. No setter exists on my side. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 4.1 The discipline the packet asks for: every field needs a consumer

The packet says *"Remove fields with no concrete use case."* I have applied that literally. My earlier `WORLD_ARCHITECTURE.md` §7.1 listed "position, facing, locomotion state, in-combat flag, interaction target" without justifying each. Below each field is justified by a named consumer and a decision it enables — or it is **withdrawn**.

| Field | Consumer | Decision it enables | Verdict |
|---|---|---|---|
| `Location` (FVector) | Crowd subsystem; interaction router | Proximity/LOD tier for Mass agents; candidate search radius | **REQUIRED** |
| `Facing` (FRotator) | Interaction router | Best-in-view scoring for interactable selection | **REQUIRED** |
| `LocomotionState` | Traversal gating; interaction router | Whether an interaction is legal mid-air; movement mode for route attempts | **REQUIRED** |
| `bInCombat` | Chapter director; crowd subsystem | Suppress ambient barks/crowd idle during combat; arm encounters | **REQUIRED** |
| `InteractionTarget` | Interaction router | Focus target identity; avoids re-querying the world every frame | **REQUIRED** |
| `Velocity` | Crowd subsystem | Noise proxy for ambient reaction radius | **REQUESTED — see 4.2** |
| `CarryState` | Traversal gating | Q2 in the C-01 request: some routes close under carry | **REQUIRED** |
| `CameraForward` | Interaction router | View-cone scoring independent of body facing | **REQUESTED — see 4.2** |
| `StealthState` | — | — | **WITHDRAWN** |
| `SurfaceType` | — | — | **WITHDRAWN** |
| `Stamina` | — | — | **WITHDRAWN** |
| `Health` | — | — | **WITHDRAWN — see 4.3** |

I withdraw four fields I previously implied I wanted. None had a consumer I could name, and asking for them would have expanded the shared surface for no decision.

### 4.2 The two requested fields, and my honest confidence

`Velocity` and `CameraForward` are marked **REQUESTED**, not REQUIRED, because I can name the consumer but not yet a decision that fails without them.

- **`Velocity`** — crowd reaction radius. I could approximate from position deltas, badly, at the cost of a frame of lag. If Agent 1 says no, I drop it.
- **`CameraForward`** — view-cone scoring. Without it the router uses body `Facing`, which is wrong when the player strafes. Acceptable degradation; not free.

### 4.3 Health is withdrawn deliberately

I do **not** request player health. Boss phase transitions may need "player is below X health" as an authored phase condition — but that is a **rule evaluated by Agent 1's authority**, not a snapshot field I poll. Polling health would create a second authority by the back door, and C-03/C-04 already give me applied-damage and forced-state events. If a boss genuinely needs health, I will request a **phase-condition evaluation query**, not a raw field.

### 4.4 Snapshot shape — proposed

```
PROPOSED — NOT FROZEN

FTDDPlayerContextSnapshot          // immutable once produced
    uint64              FrameStamp        // monotonic; detects staleness
    FVector             Location          // world space, cm
    FRotator            Facing
    FVector             Velocity          // REQUESTED
    FRotator            CameraForward     // REQUESTED
    ETDDLocomotionState LocomotionState
    bool                bInCombat
    FTDDEntityHandle    InteractionTarget // invalid handle when none
    ETDDCarryState      CarryState
    bool                bValid            // false when unpossessed/dead/despawned
```

**Units:** centimetres, world space, same frame as `ATDDTraversalMarker::EntryAnchor`. Unreal's native units — I am not introducing a second frame.

### 4.5 Freshness, query vs event — separate state taxonomies

The packet warns against asking one snapshot to combine independent taxonomies. I agree, and split by **rate** rather than by convenience:

| Consumer need | Mechanism | Freshness | Why |
|---|---|---|---|
| Interaction router | **Query** per router tick | Same frame | Scoring is continuous |
| Crowd LOD tier | **Query** at 4 Hz | ≤250 ms | Mass LOD is coarse |
| Combat start/stop | **Event** | Immediate | A one-shot transition; polling misses it |
| Locomotion change | **Event** | Immediate | Traversal legality is a transition |

**Rule:** anything that is a *transition* is an event, because polling a transition either misses it or double-fires. Anything that is a *level* is a query.

**Staleness:** a snapshot with `FrameStamp` older than 2 frames is treated as stale. The router may use a stale snapshot for scoring but must not use it to **commit** an interaction.

### 4.6 Behaviour when context is invalid

| Condition | `bValid` | World behaviour |
|---|---|---|
| Player unpossessed | false | Router clears focus; crowd reverts to baseline density |
| Player dead | false | Combat events ignored; ambient resumes per §C-04 |
| Player streamed out | false | No queries issued; no error |
| Snapshot never produced | n/a | Consumers treat as invalid; **no default vector invented** |

The last row matters: a zero-vector default is indistinguishable from the world origin, which is a real place. I will not default to it.

### 4.7 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.PlayerContextConsumersAreReadOnly` | **L1-unit** | Snapshot type exposes no non-const setter; a consumer attempting mutation fails to compile |
| `…PlayerContextMissingIsInvalidNotZero` | **L1-unit** | Absent snapshot → `bValid=false`; router issues no interaction commits |
| `…PlayerContextStaleSnapshotRejected` | **L1-unit** | `FrameStamp` age > 2 frames blocks commit but permits scoring |
| `…PlayerContextEventQueryConsistency` | **L2-auto** | Combat start event fires exactly once per transition; polling agrees next frame |
| `…PlayerContextDespawnedPlayer` | **L2-auto** | Player destroyed → all consumers observe `bValid=false`; zero crashes |

### 4.8 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C02-Q1 | Confirm units = cm, world space | Agent 1 | proposed |
| C02-Q2 | `Velocity` — in or out | Agent 1 | requested |
| C02-Q3 | `CameraForward` — in or out | Agent 1 | requested |
| C02-Q4 | Event vs query split per §4.5 | Agent 1 | proposed |
| C02-Q5 | `FTDDEntityHandle` definition | Agent 3/TD (C-07) | requested |

---

## 6. C-03 — Damage request, resolution, application, applied event

**Proposal version:** `A2-C03-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD (`TDDCore` applied event); Agent 1 (resolution flow) |
| **Implementation owner** | **Agent 1** — hit arbitration and damage application. Agent 2 supplies intent and consumes results. |
| **Producers (world)** | `ATDDEnemyBase` (SPEC), `UTDDBossPhaseGraph` (SPEC) — attack **intent** only |
| **Consumers (named)** | `ATDDEnemyBase` reactions, `UTDDBossPhaseGraph` transitions, `ATDDEncounterVolume`, audio/telemetry |
| **Mutation authority** | **Agent 1 only** applies damage. **I never write health**, never compute a hit, never resolve penetration or mitigation. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 5.1 What an enemy actually needs to react, justified field by field

| Fact | Needed by | Justification — remove it and this breaks |
|---|---|---|
| `DamageAmount` | Enemy AI | Selection of flinch vs stagger vs unphased response |
| `DamageType` (tag) | Enemy AI | Different reaction per canonical damage kind |
| `bLethal` | Enemy AI; boss phase graph | Death transition; a phase may be gated on a kill |
| `SourceEntity` (handle) | Enemy AI | Retarget / aggro transfer |
| `TargetEntity` (handle) | Enemy AI | Disambiguate when one attack hits several |
| `HitLocation` (FVector) | VFX/socket placement | Wound attachment point; **not** used for damage math |
| `bPostureBroken` | Enemy AI | Distinct response from a plain hit |
| `HitEventId` | **Dedupe** | Exactly-once reaction — see §5.4 |

**Withdrawn:** `DamageMultiplier`, `ResistanceProfile`, `ArmorValue`. All are resolution internals. If I read them I could second-guess the outcome, which is how a second damage authority begins.

### 5.2 The distinction the packet asks me to preserve

> *"distinguish hit-resolution from applied damage"*

They answer different questions and I propose **two different events**:

| | Resolution | Applied |
|---|---|---|
| Question | "would this hit?" | "this hit was applied" |
| Timing | Before application | After application |
| Authority | Agent 1 arbiter | Agent 1 pipeline |
| Consumer | Agent 1 (mostly internal) | **Agent 2 enemies/bosses** |
| Can be corrected after the fact | Yes (rejected) | **No — this is the fact** |

**My consumers subscribe to APPLIED only.** Reacting to a resolution that is later discarded would make an enemy flinch at an attack that never landed. I request that resolution events **not** be published on the shared stream at all, or be clearly marked as non-authoritative.

### 5.3 Enemy attack intent — the submission path

I create enemy attack intent. The packet asks how I submit it without applying damage or duplicating arbitration. Proposed:

```
PROPOSED — NOT FROZEN

FTDDHitIntentRequest
    uint64           RequestId;        // caller-generated, unique per attack
    FTDDEntityHandle SourceEntity;     // the enemy
    FGameplayTag     AttackTag;
    TArray<FTDDHitVolume> Volumes;     // capsules/boxes, world space
    float            NominalDamage;
    FGameplayTag     DamageType;
    FName            TelegraphWindowId; // ties to C-05
```

**Flow:** I submit → Agent 1 arbitrates → Agent 1 applies → Agent 1 publishes applied event → I react.

**I explicitly do not:** compute whether the volume overlaps the player, decide invulnerability, apply mitigation, or write health. If Agent 1's pipeline rejects the intent, I receive a rejection and must not synthesise a hit.

### 5.4 Ordering, deduplication, and the actor-unload problem

| Requirement | Proposal |
|---|---|
| Exactly-once reaction | Every applied event carries a unique `HitEventId`; consumers keep a small ring buffer of seen IDs |
| Ordering | Events for one `SourceEntity` are ordered by sequence number; cross-source ordering is **not** guaranteed and I will not assume it |
| Duplicate delivery | Must be idempotent — a consumer reacting twice to one ID is a defect |
| **Source unloads before consumer reads** | Event carries `SourceContentKey` (stable) **and** `SourceEntity` (handle, may be stale). Consumer that must act post-unload reads the key |
| Source dies mid-flight | Applied event still delivers; `bSourceAlive=false` |
| Target unloads | Event is **dropped** by Agent 1, not delivered with a dead handle — I request this explicitly |

**Why a ring buffer rather than a durable ledger:** applied events are high-frequency and ephemeral. A durable ledger would be a persistence concern I do not own. 256 entries is my proposal; Agent 1 may specify otherwise.

### 5.5 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.DamageEventReactionAndIdentity` | **L2-auto** | One intent → exactly one applied event → enemy reacts **once** |
| `…DamageNoDuplicateApplication` | **L2-auto** | Two intents with same `RequestId` → one application; second rejected |
| `…DamageStableIdentityAcrossUnload` | **L2-auto** | Source streamed out mid-flight; event still resolves `SourceContentKey` |
| `…DamageTargetUnloadDropsEvent` | **L2-auto** | Target destroyed before application → **no** event delivered |
| `…DamageWorldNeverWritesHealth` | **L1-unit** | No Agent 2 symbol writes a health field; enforced by a symbol scan |
| `…DamageResolutionNotPublishedAsFact` | **L1-unit** | Shared stream carries applied events only |

### 5.6 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C03-Q1 | Applied event payload + `HitEventId` | Agent 1 | proposed |
| C03-Q2 | Intent submission shape | Agent 1 | proposed |
| C03-Q3 | Confirm resolution is **not** published | Agent 1 | requested |
| C03-Q4 | Target-unload drop policy | Agent 1 | requested |
| C03-Q5 | Enemy archetypes | **CD (CD-3)** | **PROPOSED — not ratified**; this contract does not depend on any specific archetype existing |

---

## 7. C-04 — Stagger classification and forced-state outcome

**Proposal version:** `A2-C04-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD (event type); Agent 1 (state authority) |
| **Implementation owner** | **Agent 1 exclusively** — classification, precedence, state transition, fallback/restoration |
| **Producers** | Agent 1 state machine |
| **Consumers (named)** | `ATDDEnemyBase` AI, `ATDDEncounterVolume`, `UTDDCrowdSubsystem`, `UTDDInteractionRouter` (eligibility) |
| **Mutation authority** | I **never** classify stagger and **never** transition player state. I observe the published outcome. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 6.1 The precedence I am building against — accepted, not proposed by me

**Dead (100) > Cinematic (90) > Stagger (80)** is a TD decision in v1.1 §2.1. I am not proposing it; I am stating that my consumers are built on it and would break if it changed.

Simultaneous pending forced targets: **exactly one** state change occurs; lower-priority requests are superseded and logged. My consumers must never see two transitions for one resolution.

### 6.2 What each world consumer does, per outcome

| Outcome | Enemy AI | Encounter volume | Crowd | Interaction router |
|---|---|---|---|---|
| **Dead** | Disengage; return to post | Disarm; stop spawning | Resume ambient after delay | Clear focus; no prompts |
| **Cinematic** | Freeze; no attacks | Disarm hard; no re-arm until exit | Suspend ambient | Suspend prompts |
| **Stagger** | **Exploit window** — this is the whole point | Remain armed | Suppress barks | Suspend prompts |
| **Recovered** (no forced state) | Continue attack schedule | Remain armed | Normal | Restore prompts |

**Stagger is the one that matters.** An enemy that does not react to a staggered player is a missed combat beat; this is the strongest world-side reason to need C-04 at all.

### 6.3 Display/AI behaviour versus transition authority — kept apart

I am drawing this line explicitly because the packet asks for it:

| I control | Agent 1 controls |
|---|---|
| Whether an enemy *chooses* to attack a staggered player | Whether the player *is* staggered |
| Ambient crowd suppression | Duration of the stagger |
| Encounter arming state | Fallback/restoration sequencing |
| Prompt visibility | Movement mode restoration |

No world system may extend, shorten, or override a stagger. If a boss wants a longer stagger it must request it as an **authored attack property evaluated by Agent 1**, not by mutating state.

### 6.4 Event shape — proposed

```
PROPOSED — NOT FROZEN

FTDDForcedStateOutcome
    uint64           ResolutionId;     // one per traversal resolution
    ETDDForcedState  AppliedState;     // Dead | Cinematic | Stagger | None
    int32            Priority;         // 100 | 90 | 80 | 0
    TArray<ETDDForcedState> Superseded;// logged, not applied
    bool             bHealthAppliedIndependently;
    FTDDEntityHandle SubjectEntity;
```

`Superseded` is included deliberately: a consumer that wants to log "a cinematic was suppressed by a death" can, without inferring it from ordering.

`bHealthAppliedIndependently` reflects v1.1 §2.2(1): health damage applies independently of state resolution. An enemy needs to know that a lethal hit happened **even when** the state resolved to Cinematic.

### 6.5 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.ForcedStateEventConsumption` | **L2-auto** | Each of Dead/Cinematic/Stagger produces exactly the §6.2 row in each named consumer |
| `…ForcedStatePrecedenceDeadWins` | **L2-auto** | Dead + Cinematic + Stagger pending → one transition, `Priority=100`, other two in `Superseded` |
| `…ForcedStateNoSecondAuthority` | **L1-unit** | Symbol scan: no Agent 2 code writes a player state enum |
| `…ForcedStateHealthIndependent` | **L2-auto** | Lethal damage resolving to Cinematic still applies health; `bHealthAppliedIndependently=true` |
| `…ForcedStateAbortWindowRespected` | **L2-auto** | Non-stagger damage inside `AbortWindow` aborts; outside, traversal continues and health still applies |

The last test is a direct check of preserved M1 v1.4 behaviour — I am asking Agent 1 to confirm my consumer's expectations match it, **not** proposing to change it.

### 6.6 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C04-Q1 | Outcome event shape | Agent 1 | proposed |
| C04-Q2 | `ResolutionId` scope (per resolution, per actor?) | Agent 1 | **unresolved** |
| C04-Q3 | Recovery event — is there one? | Agent 1 | **unresolved**; my consumers currently assume they must poll to leave a suppressed state |
| C04-Q4 | Cinematic takeover outranks Stagger — confirmed | TD v1.1 §2.2 | **accepted** |

**C04-Q3 is a genuine gap.** If there is no recovery event, every consumer must poll to know when a stagger ended, which reintroduces the polling a transition deserves to avoid. I flag it rather than invent one.

---

## 8. C-05 — Telegraph timing and lifecycle

**Proposal version:** `A2-C05-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD (event type) |
| **Implementation owner** | **Agent 2 for the producer** (enemy AI owns its own attack telegraph); **Agent 1 for consumption** (parry/block) |
| **Producers** | `ATDDEnemyBase` StateTree tasks; `UTDDBossPhaseGraph` phase actions |
| **Consumers (named)** | Agent 1 parry/block logic; Agent 2 audio cue; Agent 2 VFX marker; animation montage selection |
| **Mutation authority** | **I own the producer.** I must not apply damage through a telegraph — the telegraph is a **notification**, damage comes only via C-03. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 7.1 Producer authority and lifecycle

I propose that the **enemy that owns the attack** is authoritative for its telegraph. No central telegraph director — it would become a second scheduler competing with StateTree.

```
PROPOSED — NOT FROZEN

FTDDTelegraphWindow
    FName            WindowKey;        // stable, per attack definition
    uint64           InstanceId;       // unique per firing
    FTDDEntityHandle SourceEntity;
    ETDDTelegraphPhase Phase;          // Begin | Update | End | Cancelled
    float            StartGameplayTime;
    float            EndGameplayTime;  // expected
    float            CurrentGameplayTime; // on Update
    FGameplayTag     AttackTag;
    FGameplayTag     TargetAreaTag;    // area attacks; optional
    ETDDTelegraphCancelReason CancelReason; // on Cancelled
```

### 7.2 Identity, and why there are two identifiers

| ID | Scope | Why |
|---|---|---|
| `WindowKey` | **Stable**, per attack definition | Lets Agent 1 tune a parry response per attack type, persisted in data |
| `InstanceId` | **Unique per firing** | Disambiguates two simultaneous enemies using the same attack |

A late subscriber can match `WindowKey` for tuning but **must** use `InstanceId` to avoid treating the second enemy's window as a re-broadcast of the first. This is the "reused IDs" case the packet asks about.

### 7.3 Timing rules I propose

| Rule | Proposal |
|---|---|
| Time source | **Gameplay time**, not wall clock, not frame index |
| Pause | Windows **freeze** while the game is paused; `CurrentGameplayTime` does not advance |
| Time dilation | `EndGameplayTime` is in **undilated** gameplay time; a dilated window still ends at the same gameplay time |
| Level streaming | Source streams out → **`Cancelled`** with `SourceUnloaded` |
| Actor death mid-telegraph | **`Cancelled`** with `SourceDied` |
| Attack interrupted | **`Cancelled`** with `AttackInterrupted` |
| Missed `Begin` | Late subscriber must **not** synthesise a start — see §7.4 |

**I cannot freeze the clock.** The gameplay clock is Agent 1's or the engine's. I am proposing rules and requesting confirmation.

### 7.4 Late consumers, and the honesty rule

If Agent 1's parry logic subscribes after a `Begin` was broadcast:

- **It must not** treat the first `Update` as a start.
- **It must not** assume the window began at subscription time.
- `StartGameplayTime` is carried on every message precisely so a late consumer can compute how much window remains.

A parry window that appears longer than authored because of a late subscription is a **combat bug the player will feel**, so I would rather carry one extra float on every message.

### 7.5 The telegraph is not damage

Explicit, because this is the boundary most likely to erode:

| Telegraph does | Telegraph does **not** |
|---|---|
| Announce an impending attack | Deal damage |
| Carry expected timing | Determine whether the attack lands |
| Cancel on interruption | Resolve a hit |

Damage flows **only** through C-03. An enemy whose telegraph fires but whose C-03 intent is rejected has **not** attacked. I will not add a fallback that damages on telegraph completion.

### 7.6 Required vs optional for Agent 1's consumer

| Field | Required for parry/block | Notes |
|---|---|---|
| `WindowKey` | **Required** | Per-attack tuning |
| `InstanceId` | **Required** | Dedupe |
| `Begin` / `End` | **Required** | The window itself |
| `StartGameplayTime` | **Required** | Late-subscriber correctness |
| `AttackTag` | **Required** | Block vs dodge vs unblockable |
| `Update` | **Optional** | Interpolation only; correctness must not depend on it |
| `TargetAreaTag` | **Optional** | Area attacks |
| `CancelReason` | **Required** | A parry that succeeds against a cancelled window is wrong |

### 7.7 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.TelegraphProducerLifecycle` | **L2-auto** | One attack → `Begin`, ≥0 `Update`, one `End`; **no** `End` without `Begin` |
| `…TelegraphCancelledOnDeath` | **L2-auto** | Enemy killed mid-window → exactly one `Cancelled(SourceDied)`; no `End` follows |
| `…TelegraphCancelledOnUnload` | **L2-auto** | Source streamed out → `Cancelled(SourceUnloaded)`; no dangling reference |
| `…TelegraphPauseFreezesWindow` | **L2-auto** | Pause for N gameplay-seconds → remaining window unchanged |
| `…TelegraphLateSubscriberNoSyntheticStart` | **L1-unit** | Subscribing after `Begin` yields remaining-window = `End - Start - elapsed`, never full duration |
| `…TelegraphReusedWindowKeyDistinctInstances` | **L1-unit** | Two enemies, same `WindowKey` → two distinct `InstanceId`s; both windows tracked |
| `…TelegraphClockConsistency` | **L2-auto** | Producer and consumer compute identical remaining time from the same message |

### 7.8 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C05-Q1 | Confirm gameplay-time semantics | Agent 1 | proposed |
| C05-Q2 | Pause behaviour | Agent 1 | proposed |
| C05-Q3 | `CancelReason` vocabulary | Agent 1 + TD | proposed |
| C05-Q4 | Is `Update` needed at all, or are Begin/End sufficient? | Agent 1 | **open question** — I propose carrying it, Agent 1 may not want the traffic |

---

## 9. C-06 — World-side `ITDDInteractable` implementation

**Proposal version:** `A2-C06-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | Agent 3/TD — the lifecycle interface is **Core-owned**; I implement it, I do not define it |
| **Implementation owner** | **Agent 2** — world actors implement the interface. **Agent 1** — player-side routing, input, focus. |
| **Producers** | World interactable actors (see §8.2) |
| **Consumers (named)** | Agent 1 interaction router; Agent 2 memory director (as a *request*); audio; telemetry; quest graph |
| **Mutation authority** | I own actor-local state (is this lever pulled?). I **must not** grant persistent memory/quest progress — see §8.5. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 8.1 Prompt data, not prompt strings

Position from `WORLD_ARCHITECTURE.md` §6, restated as a contract requirement: prompt text is **never** composed by C++ string concatenation, because it must be localisable.

```
PROPOSED — NOT FROZEN

FTDDInteractionPromptView
    FText        VerbText;        // localisable, e.g. "Open"
    FText        SubjectText;     // localisable, e.g. "the store door"
    FGameplayTag VerbTag;         // drives Agent 1's montage selection
    FGameplayTag PromptStyle;     // whisper / normal / emphatic
```

Agent 1 renders it. I supply the data. Neither of us hardcodes a sentence.

### 8.2 World interactable categories, and their real counts

Counts are from the CH01 scene register v1.9 capture (46 scenes, all categories present)
and the location excerpt (13 of 57 entries). Where a count is not established, the cell
says so rather than carrying an estimate.

| Category | CH01 count | Interactable? | Mode | Basis |
|---|---|---|---|---|
| Memory fragment | **1 verified** (`CH01-SCN-046` @ `CH01-SUB-018`) | **Yes** | **Hold** | `canon_index.json` `memories` |
| Enterable interior (scene) | **4** | **Yes** | Tap | Scene category `ENTERABLE INTERIOR` |
| Exterior micro-location (scene) | **6** | **Yes** | Tap | Scene category `EXTERIOR MICRO-LOCATION` |
| Exploration scene | **2** | **Yes** | Tap | Scene category `EXPLORATION SCENE` |
| Traversal affordance | **1 captured of 5** areas | **Yes** | Tap | `CH01-TRV-001` only; `TRV-002..005` not captured |
| Container / store | **not enumerated** | Yes | Tap | `CH01-SCN-006` "The Compound Store" is one instance |
| Ambient NPC scene | **14** | **No** | — | Barks and crowd only; no interaction |
| Prop | **not in my fixtures** | Unknown | — | The register's prop count is **not captured**; I will not state one |

**Two corrections to my own earlier numbers.** I previously wrote "4 enterable interior
doors" and "8 registered props". The first conflated the 4 `ENTERABLE INTERIOR` *scenes*
with the 16 published *interior location entries* — they are different objects. The second
was **invented**: the register's prop count appears nowhere in my fixtures, and I had no
source for "8". Both are withdrawn.

**Only 1 memory fragment is verified across all eight chapters.** The remaining six have
scene and location bindings recorded in `canon_index.json` but
`verified_against_register: false`. I will not claim their interactables exist, and no
Chapter 2–7 content is in scope here.

**Total interactable count is therefore not established.** An earlier draft of the summary
table said "62 world interactables"; that figure had no source and is withdrawn.

What I can say precisely is weaker than an interactable count: **13 scene-category
instances could plausibly carry an interactable** (1 verified memory + 4 `ENTERABLE
INTERIOR` + 6 `EXTERIOR MICRO-LOCATION` + 2 `EXPLORATION SCENE`). That is an upper bound on
*candidate scenes*, not a count of interactables — a scene may hold zero, one, or several.
`CH01-SCN-006` "The Compound Store" is my one concrete container example and it is not
established by category at all. **I have no source for the number of interactables and will
not state one.**


### 8.3 Minimum interface — proposed shape, Core-owned

```
PROPOSED — NOT FROZEN  (published by Agent 3/TD, implemented by Agent 2)

ITDDInteractable
    // Eligibility — cheap, called per candidate, must not allocate
    bool              CanInteract(const FTDDPlayerContextSnapshot&) const;
    ETDDInteractionAvailability GetAvailability() const;

    // Presentation
    FTDDInteractionPromptView GetPromptView() const;
    ETDDInteractionMode       GetMode() const;   // Tap | Hold

    // Requirements — data, evaluable offline
    FTDDRouteRequirement      GetRequirements() const;

    // Identity and association
    FName                     GetLocationId() const;
    FName                     GetSceneId() const;

    // Lifecycle — called by the router, not by me
    void OnBeginFocus();
    void OnEndFocus(ETDDInteractionCancelReason);
    void OnActivate(ETDDInteractionMode);
    void OnCancel(ETDDInteractionCancelReason);
```

**`CanInteract` must not allocate** — it is called per candidate per tick. I state this as a requirement on my own implementations, and request Agent 1 confirm the call frequency so I can hold that promise.

### 8.4 Tap vs hold, and the progress question the packet flags

The packet asks: *"clarify whether the world object consumes progress updates or only receives begin/end/cancel."*

**My answer: begin/end/cancel only. The world object does NOT consume progress.**

| Reason | Consequence |
|---|---|
| Progress is a **player input** concern, which Agent 1 owns | I never tick a hold timer |
| A hold that streams the actor out mid-progress must cancel cleanly | `OnCancel(StreamedOut)` is sufficient; no progress needed |
| Audio may want a rising pitch keyed to progress | That is an **audio** consumer, not the world actor — it can subscribe to the router's own progress if Agent 1 publishes it |

**By category:**

| Category | Mode | Why |
|---|---|---|
| Memory fragment | **Hold** | ADR-0008 M1: discovery requires deliberate commitment, not an accidental brush-past |
| Door / container | **Tap** | No commitment semantics |
| Traversal affordance | **Tap** | The commitment is the traversal, not the prompt |

If Agent 1 requires the world object to observe progress, I will add a read-only `OnProgressChanged(float Normalised)` — but I am **not** proposing to become the timing authority.

### 8.5 Completion fact versus progress grant — the boundary

This is the most important paragraph in C-06.

| I emit | I never do |
|---|---|
| `FTDDInteractionCompleted { InteractionId, LocationId, SceneId, Mode, FrameStamp }` | Grant a memory stage |
| Completion telemetry | Grant a quest objective |
| Local actor state ("door now open") | Write save data |

**Who grants persistent progress:** `UTDDMemoryDirector` and `UTDDCampaignSubsystem` per `WORLD_ARCHITECTURE.md` §8 and §10. They grant; the interactable only **reports**. A world actor that directly advanced a memory stage would be a second authority on the single most canon-sensitive system in the project (ADR-0008), and `RULE-CULTURAL-FICTIONALITY` makes that worse rather than better.

The memory director may **consume** `FTDDInteractionCompleted` as one of its six stage predicates. Consuming is not granting.

### 8.6 Cancellation and validity

| Condition | Required behaviour |
|---|---|
| Actor streams out mid-hold | `OnCancel(StreamedOut)`; **no** completion event |
| Requirements become unmet mid-hold | `OnCancel(RequirementChanged)` |
| Player loses focus | `OnCancel(FocusLost)` |
| Player takes damage mid-hold | `OnCancel(Interrupted)` — see note |
| Player dies mid-hold | `OnCancel(Interrupted)`; no completion |
| Actor destroyed mid-hold | `OnCancel(ActorDestroyed)` |

**Note on damage-mid-hold:** I am *not* deciding that damage interrupts a hold. I am proposing it and flagging that it is a **design** decision with combat-feel consequences, not a technical one. It needs a ruling, not my preference.

### 8.7 Complete-once semantics

`FTDDInteractionCompleted` fires **exactly once** per activation. Guards:

- Idempotent activation: a second `OnActivate` while active is ignored, not queued.
- After `OnCancel`, the next activation is a **new** attempt.
- A streamed-out-and-back actor does not replay a completion.

### 8.8 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.InteractableLifecycleAndProgressBoundary` | **L1-unit** | No `ITDDInteractable` implementation grants a memory stage; symbol scan |
| `…InteractableEligibility` | **L1-unit** | `CanInteract` returns false when requirement unmet; no allocation during the call |
| `…InteractableTapVsHold` | **L2-auto** | Tap completes on press; Hold completes only after full duration; early release cancels |
| `…InteractableCancelOnUnload` | **L2-auto** | Stream out mid-hold → `Cancelled`, **zero** completion events |
| `…InteractableExactlyOnceCompletion` | **L2-auto** | Two activations → exactly two completions; one activation → exactly one |
| `…InteractablePromptIsLocalisable` | **L0-data** | Every prompt view resolves to an `FText` key; no raw string concatenation in source |

### 8.9 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C06-Q1 | Final `ITDDInteractable` shape | Agent 3/TD | proposed |
| C06-Q2 | `CanInteract` call frequency | Agent 1 | requested |
| C06-Q3 | Does the router publish hold progress? | Agent 1 | requested (audio only) |
| C06-Q4 | **Does damage interrupt a hold?** | **TD / design** | **REQUEST TD DECISION** |
| C06-Q5 | `ETDDInteractionCancelReason` vocabulary | Agent 1 + TD | proposed |

---

## 10. C-07 — Shared IDs and Gameplay Tags

**Proposal version:** `A2-C07-1.0` · **Status:** `PROPOSAL — NOT FROZEN`

| Packet field | Response |
|---|---|
| **Publisher** | **Agent 3/TD exclusively** — registry publication and tag namespace governance |
| **Implementation owner** | Agent 2 authors **content** IDs; Agent 3/TD owns the registry |
| **Producers** | `Tools/canon/data/canon_index.json` (mirror), `Tools/world/data/CH01_manifest.json` |
| **Consumers (named)** | Every contract above; save system; L0 gate |
| **Mutation authority** | I may **not** mint a Core tag or register an ID unilaterally. I submit requests. |
| **Agent 1 agreement** | `NOT RECEIVED` |
| **TD decision** | *(blank)* |

### 9.1 ID inventory — source and version per family

Counts below are **Chapter 1 only** unless stated. Mixing a CH01 excerpt count with a
whole-game published total would misstate both, so the two are separated deliberately.

| Family | Format | Source | Version | CH01 rows | CH01 published | Whole game |
|---|---|---|---|---|---|---|
| Chapter | `^CH0[1-8]$` | `canon_index.json` | 2.0.0 | **8 of 8** | — | 8 |
| Major environment | `CH0n-ENV-001` | `LOCATION_MASTER_REGISTER` | **v2.9** | **1** | 1 | 8 |
| Sub-location | `CH0n-SUB-nnn` | same | v2.9 | **23** | 40 (joint) | 142 (joint) |
| Settlement | `CH0n-SET-nnn` | same | v2.9 | **1** | 40 (joint) | 142 (joint) |
| Interior | `CH0n-INT-nnn` | same | v2.9 | **16** | 16 | **46** |
| Landmark | `CH0n-LMK-nnn` | same | v2.9 | **3** | 40 (joint) | 142 (joint) |
| Traversal area | `CH0n-TRV-nnn` | same | v2.9 | **5** | 40 (joint) | 142 (joint) |
| Exploration area | `CH0n-EXP-nnn` | same | v2.9 | **7** | 40 (joint) | 142 (joint) |
| Boss arena | `CH0n-BOS-nnn` | same | v2.9 | **1** | 40 (joint) | 142 (joint) |
| **Location entries (total)** | — | same | v2.9 | **57 of 57** | 57 | **196** |
| Scene | `CH0n-SCN-nnn` | `SCENE_AND_MICROLOCATION` | **v1.9** | **46 of 46** | 46 | **135** |
| Memory | index 1–7 | `NNEKA_MEMORIES` | — | 1 of 7 verified | 7 | 7 |
| Rule | `^RULE-[A-Z0-9-]+$` | `canon_index.json` | 2.0.0 | 19 | — | 19 |
| **Route** | `<location>/ROUTE-X` | **none — proposed by me** | — | **0 — does not exist** | — | — |
| **Interactable** | *(unresolved)* | — | — | **see §9.2** | — | — |

**Location capture is now complete for Chapter 1, and this submission is what completed
it.** Earlier in this document I was working from a 13-row excerpt and correctly said so.
Reading `LOCATION_MASTER_REGISTER.md` v2.9 in full (534,140 bytes) produced the missing
rows, now captured as `Tools/canon/tests/fixtures/location_register_ch01_summary_v29.md`.

Verification, runnable:

```
python3 Tools/world/contract_data_checks.py --verbose
```

```
[PASS] ch01_location_row_count            57 rows, 57 unique
[PASS] ch01_family_counts                 ENV 1 + others 40 + INT 16 = 57
[PASS] traversal_category_is_multivalued  8 traversal-capable of 57
[PASS] exploration_category_is_multivalued 8 exploration-capable; non-EXP: SUB-003
[PASS] canon_status_has_three_values      ESTABLISHED 22, PENDING APPROVAL 3, PROPOSED 32
[PASS] env_design_status_has_seven_values 57 rows checked against 7 allowed values
[PASS] location_ids_match_published_scheme 57 IDs; retirement NOT verifiable
[PASS] excerpt_is_subset_of_full_capture   excerpt 13 rows, all present in the 57
[PASS] interactable_id_namespace_unresolved NO register source exists
```

Read the bounds on that carefully:

- **The 13-row excerpt remains a strict subset** of the new capture, so the earlier
  fixture was not wrong — only incomplete.
- **Retirement is still not verifiable** from a summary table. The register says retired
  IDs stay and are never reused, but a summary table only lists live rows. That check
  states its own limit rather than implying coverage it does not have.
- `canon_index.json` carries 15 CH01 location rows, not 57. It is a **curated subset**
  used for drift detection, not a full mirror. I have not altered it and do not claim it
  is complete.
- This is **L0-data validation**. It says nothing about runtime behaviour.

Consequence for C-01 and C-06: I can now enumerate Chapter 1's real traversal-capable
locations (§3.2) and its interiors. I still **cannot** enumerate interactables, because
the register does not list them (§9.2).


**Source documents and their Drive IDs** (from `canon_index.json` `source_documents`): `LOCATION_MASTER_REGISTER` `1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5` v2.9; `SCENE_AND_MICROLOCATION_MASTER_REGISTER` `1EYQl5eMZx8PGElDSPHojKcEVWGvU2-UW` v1.9.

### 9.2 The interactable ID problem — unresolved, and I am not inventing one

Every other family has a register source. **Interactables have none.** They are a world-side concept that the registers do not enumerate.

| Option | Shape | Cost |
|---|---|---|
| **A** | Derive from owning scene: `CH01-SCN-006/INT-01` | No new register; but not human-nameable and collides if two agent teams author independently |
| **B** | New family `CH0n-ACT-nnn` | Needs TD namespace grant; a second ID space to maintain |
| **C** | Actor name only, no stable ID | Cheapest; **breaks save compatibility** if an interactable's state must persist |

**My position: option A** for interactables whose state is **not** persisted (doors, containers, levers), and **no stable ID at all** — they are transient. For any interactable whose state **must** persist, option B with a TD-granted namespace.

I do not know yet whether any interactable state must persist. **That is a save-system question owned by Agent 3**, and I am flagging it rather than guessing.

### 9.3 Stable key vs runtime identity vs label — the distinction the packet demands

| Kind | Example | Persist? | Stream-safe? | Human-readable? |
|---|---|---|---|---|
| **Content key** | `CH01-INT-008` | **yes** | **yes** | no |
| **Route key** | `CH01-TRV-001/ROUTE-A` | **yes** | **yes** | partly |
| **Runtime identity** | `FTDDEntityHandle{Guid, Gen}` | no | **no** | no |
| **Transient actor** | `AActor*` | no | no | no |
| **Display label** | "The Healer's House" | — | — | **yes — never a key** |

**Rule:** a display label is **never** used as a lookup key. `CH01-INT-008` has a name, and the register already warns its current art requires revision (patient in modern clothing) — meaning the label may change while the ID must not.

### 9.4 Tag inventory

**Status of every tag I need: none exist yet.** The tag registry is a Core artefact that does not exist. All rows below are **REQUESTED**.

| Namespace | Tag (proposed) | Consumer | Exists? |
|---|---|---|---|
| `Interaction.Verb` | `Open`, `Take`, `Inspect`, `Climb`, `Listen`, `Read` | Agent 1 montage selection | **REQUESTED** |
| `Interaction.Mode` | `Tap`, `Hold` | Router | **REQUESTED** |
| `Traversal.Capability` | *(names = Agent 1's decision)* | C-01 | **REQUESTED — blocked on Agent 1** |
| `Traversal.State` | `Blocked`, `OneWay` | C-01 | **REQUESTED** |
| `Combat.Damage` | `Slash`, `Impact`, `Root`, `Thunder` | C-03 | **REQUESTED** |
| `Combat.State` | `Staggered`, `Cinematic`, `Dead` | C-04 | **REQUESTED** |
| `Telegraph.Cancel` | `SourceDied`, `SourceUnloaded`, `AttackInterrupted` | C-05 | **REQUESTED** |
| `NPC.Activity` | `Cook`, `Farm`, `Weave`, `Hunt` | Routine data (`WORLD_ARCHITECTURE` §5.2) | **REQUESTED** |
| `World.Access` | `OpenExterior`, `FullyEnterable`, `PartiallyEnterable`, `VisuallyAccessible`, `BackgroundEnvironment` | Streaming policy | **REQUESTED — derived from register vocabulary** |

The `World.Access` values are **not invented**: they are the register's own access-level vocabulary, already parsed and validated in `population_policy.json`. I am requesting they be published as tags so code and data share one spelling.

### 9.5 Retired and missing ID behaviour

| Situation | Proposed behaviour |
|---|---|
| ID referenced but absent from registry | **L0 validation failure**, not a runtime warning |
| ID present but retired | Explicit `Retired` state; lookup returns retired, not null |
| Raw ID reused after retirement | **Forbidden**; validator must reject |
| Tag requested but unregistered | **Validation error at author time** — an unregistered tag is a typo, not a runtime fallback |
| Unknown tag at runtime | Log and ignore the **tag**, never crash, never guess a default |

### 9.6 Acceptance tests — proposed

| Test ID | Layer | Assertion |
|---|---|---|
| `TDD-Contract.World.IdAndTagRegistryValidation` | **L0-data** | Every ID in `CH01_manifest.json` resolves to a register source + version |
| `…IdDuplicateDetection` | **L0-data** | Zero duplicate content keys; a synthetic duplicate fails |
| `…IdRetiredNeverReused` | **L0-data** | Retired ID appearing as active fails validation |
| `…TagRegistryCompleteness` | **L0-data** | Every tag referenced by authored data is registered; zero unknown |
| `…IdDisplayLabelNeverAKey` | **L0-data** | No display label appears in a key position |
| `…IdStreamingReferenceValidity` | **L2-auto** | After stream/unstream cycle, all references resolve to the same content keys |

### 9.7 Dependencies

| # | Item | Owner | Status |
|---|---|---|---|
| C07-Q1 | Tag namespace grant | Agent 3/TD | requested |
| C07-Q2 | `FTDDEntityHandle` definition | Agent 3/TD | requested |
| C07-Q3 | **Interactable ID: does any state persist?** | **Agent 3 (save)** | **REQUEST TD DECISION** |
| C07-Q4 | Traversal capability tag names | Agent 1 | blocked on C-01 |
| C07-Q5 | Retirement policy | Agent 3/TD | requested |

---

## 11. Dependencies on Agent 1, consolidated

| # | Contract | What I need from Agent 1 | Blocking severity |
|---|---|---|---|
| 1 | C-01 | Capability enum and names | **High** — blocks all route data |
| 2 | C-01 | Requirements: data or code | **High** — decides whether offline validation exists at all |
| 3 | C-01 | Cumulative vs independent; revocability | Medium |
| 4 | C-01 | Traversal context (water/rope) | Medium — Ch1 has both |
| 5 | C-02 | Confirm field list; `Velocity`, `CameraForward` in/out | Medium |
| 6 | C-02 | Event-vs-query split | Low |
| 7 | C-03 | Applied event payload | **High** — blocks enemy reaction |
| 8 | C-03 | Confirm resolution not published as fact | Medium |
| 9 | C-03 | Target-unload drop policy | Low |
| 10 | C-04 | Outcome event shape; `ResolutionId` scope | **High** |
| 11 | C-04 | **Is there a recovery event?** | **High** — otherwise every consumer polls |
| 12 | C-05 | Gameplay-time and pause confirmation | **High** — timing correctness |
| 13 | C-05 | `CancelReason` vocabulary | Medium |
| 14 | C-06 | `ITDDInteractable` final shape | **High** |
| 15 | C-06 | `CanInteract` call frequency | Medium — allocation promise |
| 16 | C-07 | Traversal capability tags | blocked on #1 |

**Seven of sixteen are High.** No contract in this submission can be agreed until at least the High items are answered.

---

## 12. Items requiring Technical Director resolution

| # | Item | Why I cannot resolve it | Proposed default if TD declines to rule |
|---|---|---|---|
| **TD-1** | Does a **v1.2** of `TDD-TD-INT-001` exist? | I answered against v1.1; the request cites v1.2 | Proceed on v1.1 per §0.1 |
| **TD-2** | **Does damage interrupt a hold interaction?** (C06-Q4) | Combat-feel design, not a technical constraint | Interrupt — safer for combat clarity |
| **TD-3** | **Interactable ID: does any state persist?** (C07-Q3) | Save-system scope is Agent 3's | No persistent interactable state in Ch1 |
| **TD-4** | `ROUTE-` namespace reservation (C01-Q6) | Namespace governance is TD's | I keep `ROUTE-` and will rename if rejected |
| **TD-7** | **Does the route anchor follow the ID prefix or the register's Category tag?** | §3.2 shows `TRV-` alone misses 3 of 8 traversal-capable locations. Choosing the prefix means silently dropping legitimately-marked content | Anchor on Category tag (recommended) |
| **TD-5** | Silent vs refused feedback on blocked traversal (§3.5.1) | Interacts with preserved M1 v1.4 animation behaviour | Silent, per-route opt-in refusal |
| **TD-6** | Is C-04's recovery-from-stagger event in scope, or Agent 1's discretion? | Crosses a contract boundary | Require it — polling is worse |

None of these blocks *drafting*. All six block *agreement*.

---

## 13. Verification performed

Everything below was run in this session. Exit codes captured directly, not through a pipe.

| Command | Result | Exit |
|---|---|---|
| `python3 Tools/world/contract_data_checks.py` | **9/9 checks passed** | **0** |
| `python3 -m unittest discover -s Tools/world/tests` | **256 tests OK** | **0** |
| `python3 -m unittest discover -s Tools/canon/tests` | **114 tests OK** | **0** |
| `python3 Tools/ci/l0_checks.py` | **14/14 passed** | **0** |
| `python3 Tools/world/gen_evidence.py` | **11/11 checks, all passed** | **0** |

### 12.1 What these tests actually prove

| Test group | Proves | Does **not** prove |
|---|---|---|
| `contract_data_checks` (9) | The register's vocabulary, counts and multi-valued categories are as this document states | Anything about runtime |
| `test_contract_submission.TestTraversalIsNotAPrefix` (6) | A `TRV-`-prefix selector loses three legitimate locations | That Agent 1's capability enum matches |
| `test_contract_submission.TestVocabularyIsClosed` (3) | Canon and design statuses are separate and closed sets | That any tag is registered |
| `test_contract_submission.TestProposalDocument` (6) | This document claims no agreement and no frozen state | That the proposals are correct |

### 12.2 Tamper proof

The multi-valued finding is load-bearing, so it was proved to fail:

| Injected fault | Result |
|---|---|
| Remove `Traversal Area` from `CH01-SUB-009` in the capture | **4 tests fail** — the finding is genuinely read from data, not hardcoded |
| Restore | **23/23 pass** |

Had those tests passed with the tag removed, they would have been asserting a constant.

### 12.3 The test is not self-fulfilling

`test_a_prefix_only_parser_would_lose_three_locations` asserts that the loss set is
non-empty *and* names its members. If the register ever tags a `TRV-` entry differently
and the finding goes stale, that test fails rather than silently passing on an empty set.

---

## 14. What is not in this submission

Stated plainly, per the request's prohibitions:

- **No Core API implementation.** No `TDDCore` file was created or modified.
- **No Unreal project.** No `.uproject`, no module, no build.
- **No gameplay implementation.** No enemy, boss, interactable or traversal code.
- **No branch merge.** This is a document on my existing branch.
- **No archetype promotion.** All six remain `PROPOSED — not ratified`.
- **No cultural content introduced.** CD-2 gate untouched; CD-5 blockout rules honoured.
- **No runtime performance claim.** Nothing here has been executed.
- **No Chapter 2–8 data.** Not ingested; not extrapolated.
- **No agreement invented.** Every Agent 1 row above reads `NOT RECEIVED`.

---

## 15. Document status and change log

| Field | Value |
|---|---|
| Proposal versions | `A2-C01-1.0` … `A2-C07-1.0` |
| Overall status | `PROPOSAL — NOT FROZEN — AWAITING AGENT 1 AND TD` |
| Agreed contracts | **0 of 7** |
| Tests run for these contracts | **0** (no route records, no interactables, no engine exist) |
| Supersedes | nothing |
| Preserves | all prior Agent 2 documents, including `AGENT1_TRAVERSAL_CONTRACT_REQUEST.md` v0.1.0 |

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | First submission. All seven contracts proposed; zero agreed; six TD escalations raised. |
