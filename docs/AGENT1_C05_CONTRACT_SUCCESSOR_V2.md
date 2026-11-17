# Agent 1 — C-05 Successor `A1-C05-S2`

**Response ID:** `TDD-A1-C05-SUCCESSOR-002`
**Version:** 2.0 — successor to `A1-C05-S1` v1.0; current C-05 position
**Date:** 2026-11-17 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Scope:** **two corrections only** — (1) phase changes must advance the snapshot revision; (2) Agent 1 / Agent 2 ownership wording. Nothing else is reopened.
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no C++, no Unreal project, no API or contract freeze, **no MEAD selection**, no signature, no merge, no M0 claim. **C-05 remains proposed, unsigned and unfrozen.**

| Basis | Exact version | Commit | Blob / note |
|---|---|---|---|
| Agent 3's bounded integration-readiness assessment (the review answered here) | `AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1` v1.0 | `1eb613f` | `docs/AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md`, 74 lines, read in full |
| My predecessor under review | `A1-C05-S1` v1.0 | `2bb729f2cbd525e3cd7f5f5d46b3b9cc72c803d0` | `dcec9e1ae3efd4651c290636e8a4d6623603dc83` — **preserved, unmodified** |
| Agent 2's C-05 submission (the ownership assignment I must reconcile with) | `A2-C05-1.0` (in `A2-C01…C07-1.0`) | `3ac438b32fcd73ceb22dcd81385356f7b8b39644` | §8, "Implementation owner" row |
| TD integration decisions | v1.2 | `e121bbbf09562e3cba0efe81aad971809685db23` | C-05 row |
| Agent 2's reviews (prior) | `7ea0a85`, `586152b` | as cited | read only; **no review of the S1 blob exists yet** |
| MEAD-A / MEAD-B / MEAD-C | candidates | `912fac9` / `d32660f` / `169a8d8` | read only; **none selected** |

---

## 0. Provenance and scope lock

### 0.1 What Agent 3 found, in their words

Two blocking items and nothing else: **"Revision must version the complete recoverable state, not only rate retimes"**, and **"Blocking integration ownership clarification"** — `C05-2.1` assigning enemy production to Agent 2 against `C05-7.1` assigning producer-side implementation to Agent 1. Everything else in their assessment is either positive (MEAD neutrality, arbitration separation, lifecycle model, no-history recovery) or an external dependency they explicitly keep outside C-05 text.

### 0.2 What this document does

It makes exactly those two corrections, restates the complete contract so that the successor can be read without the predecessor, and adds the examples and test cases Agent 3 asked for. **It does not redesign the recovery model, does not add history, does not add an event bus, does not re-open any resolved finding, and does not touch X-1, the MEAD position, the arbitration boundary or the blocker list's statuses.**

### 0.3 The one place I extend Agent 3's request rather than merely executing it

Agent 3's recommended fix for finding 1 was: *"the monotonic snapshot revision advances on every change to the pull-visible phase/timing block (including every phase transition and every retime); explicitly scope the freshness filter so terminal `Closed` is handled even when the timing revision is unchanged."* I implement that, and I add one thing their wording does not require but their failure mode does: **every message must carry the complete snapshot.** Without it, a partial message can advance the revision while leaving another aspect stale — the same defect the correction exists to remove, reproduced on the message path. Reasoning in §2.4; it is one payload rule, not a redesign.

---

## 1. The two corrections

| # | Correction | Effect on the contract |
|---|---|---|
| **1** | **The revision versions the whole pull-visible state, and it is renamed to say so.** `StateRevision` advances by exactly one on **every** observable change — every phase transition and every retime — and every message carries the complete snapshot at that revision. Terminal `Closed` is handled outside the freshness rule. New invariant: **equal revision ⇒ identical pull-visible state.** | `C05-2.2` (field rename and meaning), `C05-2.3` (complete-snapshot payload), `C05-2.6` (AD-1/AD-2 restated, EN-3 resync and TM-1 terminal close added, INV-1 added), `TN-P-07`, **`TN-P-13`**, **`TN-P-14`**, `TN-C-01`, `TN-C-06`, **`TN-C-09`**, **`TN-R-05`** |
| **2** | **Ownership is split by activity, not by clause.** Enemy telegraph *production* and the *producer-side implementation* on enemy producers are Agent 2's; the player producer's are Agent 1's; shared contract artefacts belong to the contract layer pending TD-12; the shared read-surface support (directory and resolution helper) is Agent 1's and holds no producer data beyond association and liveness; consumer integration belongs to each consuming agent. | `C05-2.1` (unchanged, now consistent), **`C05-7.2`** (new split), **`C05-7.3`** (what "Agent 1 implements" means), `C05-7.1` (offending sentence removed), implementer column added to every obligation table |

---

## 2. Finding 1 — phase-only changes must advance the revision

### 2.1 Agent 3's problem, restated exactly

`StateRevision` (then `TimingRevision`) started at 1 on `Opened` and incremented **only** on `CustomDilation` changes (`C05-2.2`, `TN-P-07`, §5.1 of S1). A `PhaseChanged` carried a revision but did not advance it. So a consumer holding Windup at revision `k`, which misses a `PhaseChanged` to Active with no dilation change, pulls and receives **Active at revision `k`**. `TN-C-01` says equal revisions are discarded. The consumer therefore keeps a stale phase, and `TN-C-05` — the recovery clause — cannot recover it, because the recovery path is gated by the same rule that rejects the answer. **The pull-visible state had two components and only one of them was versioned.**

### 2.2 Resolution: one revision over the whole pull-visible state

> **C05-2.6 INV-1 (new invariant).** For a given `AttackInstanceId`, two observations carrying the same `StateRevision` are **identical in every pull-visible field** — phase, all timing endpoints, `ProducerRate`, `RemainingLocalSeconds`. This is an invariant, not a recommendation: a producer that publishes or answers at a revision with different content is in violation (`TN-P-07`).

Four consequences follow, and together they close the hole rather than patching the one path Agent 3 identified:

1. **Phase transitions advance the revision** (`TN-P-13`). Windup→Active is a state change whether or not the dilation changed.
2. **Equal-revision discard is now always safe.** Before, "same revision" meant "maybe the phase moved"; under INV-1 it means "nothing changed". `TN-C-01` keeps its rule and loses its hazard.
3. **A pull can no longer return a newer phase at the held revision.** If the phase moved, the revision moved with it. Agent 3's exact scenario becomes unrepresentable, which is stronger than recovering from it.
4. **The gap now means something stronger and still honest.** A revision jump means at least one observable state change was missed — phase, retime, or both — and the consumer is told so by arithmetic alone.

### 2.3 The field is renamed, because the old name was the defect

`TimingRevision` → **`StateRevision`**, same width, same position. **Why rename rather than redefine in place:** a field called `TimingRevision` whose normative meaning is "the whole state, including phase" is the same ambiguity in a smaller place, and every future reader would have to be told to ignore the name. Nothing is frozen or implemented, so the rename costs one edit in one struct that I own as a proposal; keeping the name would cost a permanent correction in every clause that cites it. The rename is recorded in the change log (§15) and supersedes `A1-R3` §3.2 on this field only.

### 2.4 Every message carries the complete snapshot — and why that is part of the same fix

Agent 3's wording did not require this; it is required by the same failure mode on the message path. Consider a `Retimed` that advances the revision but carries only timing: a consumer that missed the preceding `PhaseChanged` would adopt the higher revision, keep the stale phase, and be **unable to pull its way out** — because the pull would now return exactly the revision it holds, and `TN-C-01` would discard it. That is Agent 3's defect reproduced one path over.

> **C05-2.3 (revised).** Every message in this contract — `Opened`, `PhaseChanged`, `Retimed`, `Closed` — carries the **complete pull-visible snapshot** at emission: the instance and source ids, the phase, the full timing block and `StateRevision`. No message carries a partial aspect of the state.

Costs and non-costs, stated rather than assumed: the payload grows to the size of the snapshot struct (a handful of doubles, floats and ids — tens of bytes), which for in-process delivery is a copy, not a serialisation. **I have not measured this and am not claiming a performance result**; if a future budget makes the payload material, the correct change is a discussed revision, not a silent partial message that re-creates this finding.

### 2.5 How a consumer tells a genuinely new state from a repeated observation

Three distinguishable cases, and no heuristics:

| Comparison | Meaning | Required action |
|---|---|---|
| same revision, identical content | **repeat** — a duplicated message, or a pull of what is held | discard; no entry, no resync, no diagnostic (`TN-C-01`, INV-1) |
| `incoming == held + 1` | **contiguous successor** — one observable change | adopt; fire entry if the phase differs and the baseline rule allows (`EN-1`/`EN-2`); no gap flag |
| `incoming > held + 1` | **gap** — one or more observable changes missed | adopt; **fire no entry**; raise exactly one `Resynchronised`; set `bStateGapObserved` until close (`AD-2`, `EN-3`) |
| `incoming < held` | **stale** — an older message, or a pull taken before a newer message | discard; a pull never moves a consumer backwards (`TN-C-01`) |

### 2.6 What happens when a consumer misses one or more phase transitions

> **C05-2.6 EN-3 (new).** When a consumer adopts a snapshot across a revision gap, it **must not fabricate phase entry** for any phase it did not observe. It raises exactly one **`Resynchronised(AttackInstanceId, Phase)`** signal for that gap, which carries the phase it has landed in and no transition history, and it must not fire `PhaseEntered` for that phase at resynchronisation time. Subsequent transitions observed contiguously fire entry normally.

**Why resync rather than "fire entry late":** firing `PhaseEntered(Active)` for a phase that was entered and possibly already left is a lie about the past, and it makes the difference between "started now" and "started while you were blind" unobservable — which is exactly the information a boss reaction timer or a parry prompt needs. A separate signal keeps `PhaseEntered` honest and gives reacting consumers an explicit, testable re-arm path. **No history is retained:** the resync signal carries the current phase only, and a consumer that needs to know what it missed cannot learn it — that limit is `RS-1`/`RS-2`, unchanged.

### 2.7 Terminal `Closed` is outside the freshness rule

> **C05-2.6 TM-1 (new).** `Closed` is terminal. It is **not** subject to `AD-1`: a `Closed` carrying a revision equal to or lower than the consumer's held revision still closes the instance. Termination is a lifecycle fact, not a state update, and gating it on the revision is how a consumer keeps defending against an attack that ended.

**Consistency with the rest:** a producer must not advance `StateRevision` to announce a close (that would be a change to a state that no longer exists), so `Closed` normally carries the last state revision. `TM-1` is what makes that safe, and it is Agent 3's requested scope for the freshness filter, implemented as a message-type rule rather than a revision trick.

### 2.8 Do the existing stale and gap rules remain consistent? Yes, with two clarifications and no weakenings

| Existing rule | After this revision |
|---|---|
| `AD-1` strict-greater adoption | **Unchanged**, and now stronger in meaning: a strictly greater revision means strictly different content (INV-1) |
| `AD-2` gap flag | **Unchanged in mechanism.** Its meaning widens from "a retime was missed" to "at least one observable state change was missed", which is what the flag was always for |
| `TN-C-05` single-pull recovery | **Unchanged.** It now works for phase-only changes, which it previously did not |
| `RS-1` current-state-only recovery | **Unchanged.** Resync reports the phase it landed in; it never replays the phases it did not see |
| `RS-2` no revision history | **Unchanged.** One state per instance; the revision counter is not a log |
| `TN-P-08` no coalescing of retimes | **Unchanged.** Two dilation changes in one frame still produce two revisions and two messages — which is why the revision advances per *change*, not per frame |

### 2.9 What this does not do

- **No retained history.** One snapshot per instance; the resync signal carries no transitions.
- **No generic event bus.** `Resynchronised` is a consumer-side notification raised from information the consumer already holds; it needs no new transport, no subscription registry and no retained queue.
- **No separate counter.** Agent 3 offered "separate state and event sequence counters" as an alternative; I did not take it, because one revision over the whole state is simpler and because two counters would let the two disagree — which is the class of bug this whole finding is an instance of.
- **No change to the recovery model, the pull, or the producer/consumer split.**

---

## 3. Finding 2 — the ownership wording

### 3.1 Agent 3's problem, restated

`C05-2.1` says telegraphs are produced by Agent 2 for enemies and Agent 1 for the player. `C05-7.1` then said the contract's *implementation* — "the producer-side pull, the per-producer id list and the directory" — "is Agent 1's in every candidate". Read literally, Agent 1 would implement the producer side of **Agent 2's** enemy telegraphs, which contradicts `C05-2.1`, TD v1.2's C-05 row and Agent 2's own submission.

### 3.2 What the existing sources actually assign

| Source | Assignment |
|---|---|
| TD v1.2, C-05 row (`e121bbb`) | Agent 1: "Propose parry/block **consumer** timing and invalidation expectations." Agent 2: "Propose actual **enemy telegraph producer** lifecycle, IDs, clock and cancellation." |
| Agent 2's submission `A2-C05-1.0` §8 (`3ac438b`) | "**Implementation owner:** Agent 2 for the producer (enemy AI owns its own attack telegraph); Agent 1 for consumption (parry/block)." Producers: `ATDDEnemyBase` StateTree tasks, `UTDDBossPhaseGraph` phase actions. "**Mutation authority:** I own the producer." |
| My `A1-R1` §5.1 | Agent 2: enemy telegraph production. Agent 1: player telegraph production and the parry/block consumer. |
| MEAD-C §3.4 / §7.1 | Combat director and hitstop are Agent 1's world subsystems; enemy behaviour and attack execution are the AI area — i.e. the producing side is not Agent 1's subsystem |

**Three of the four sources agree, and S1's sentence contradicted all three.** There is no new ownership arrangement in this document; there is a correction of one sentence that overstated Agent 1's remit.

### 3.3 The split, by activity

> **C05-7.2 (new; replaces the second sentence of `C05-7.1`).**
>
> | Activity | Owner | Basis |
> |---|---|---|
> | **Gameplay production** — the authored attack, its montage windows, when a telegraph opens, changes phase and closes, and every cancellation decision | **Agent 2** for enemy attacks; **Agent 1** for the player's own attack | TD v1.2 C-05; `A2-C05` §8; `A1-R1` §5.1 |
> | **Producer-side implementation of `TN-P-01` … `TN-P-14`** — the pull answer, the per-producer id list, revision advancement and publication, registration and deregistration | **the owner of that producer**: Agent 2 on its enemy producers, Agent 1 on the player producer | follows from production ownership: an obligation about a producer's own state can only be implemented by the code that owns that state |
> | **Shared contract artefacts** — `FTDDTelegraphTiming`, `ETDDTelegraphPhase`, `ETDDTelegraphCloseReason`, `FTDDTelegraphSnapshot`, the message structs and `ITDDTelegraphSource` | the **contract layer** of the canonical architecture; owner designated by TD-12 (Agent 3 under MEAD-C; unassigned under MEAD-A; absent under MEAD-B) | TD v1.2 C-05 "publisher: Agent 3/TD (event type)"; MEAD-C line 228 |
> | **Shared read-surface support** — the directory of `C05-2.5` and the resolution helper | **Agent 1**, as shared support that stores only association and liveness. **Agent 1 does not implement any part of an Agent 2-owned producer, and Agent 2 does not implement the directory** | it needs one world-scoped home and it holds nothing a producer owns; both sides reach it only through the shared interface |
> | **Consumer integration** — parry/block/dodge evaluation, camera and audio cues (Agent 1); AI reaction to the player's telegraph, audio cue, VFX marker, montage selection (Agent 2) | **each consuming agent, in its own code** | TD v1.2 C-05; `A2-C05` §8 consumer list; `A1-R1` §5.1 |
> | **Arbitration** — the parry/block decision for hits involving the player | **Agent 1**, subject to the TD-09 erratum and unchanged by this document | TD integration decision; `A1-R3` §3.4; `C05-6.1` |

### 3.4 What "Agent 1 implements" therefore means

> **C05-7.3 (new).** Agent 1 implements: (a) every `TN-P` obligation **on the player's own producer**; (b) the shared read-surface support — directory and resolution — for all producers; (c) every `TN-C` obligation in Agent 1's own consumers; (d) every `TN-A` obligation in the arbitration path, subject to TD-09. **Agent 1 does not implement the `TN-P` obligations on Agent 2's enemy producers.** Those are Agent 2's, on Agent 2's code, against the shared interface; Agent 1's responsibility for them is limited to the interface being implementable and to reviewing the contract text.

### 3.5 Why this follows from the existing architecture rather than inventing one

1. **Mutation authority and implementation authority belong together.** Agent 2's submission states "I own the producer". An obligation to advance a revision on a phase change is an obligation *about a producer's own state*; assigning its implementation to another agent would create the second writer that every contract in this series has been built to avoid.
2. **The shared interface is what lets the two owners meet without either owning the other's code.** Both producers implement `ITDDTelegraphSource`; the directory holds only association and liveness; no agent reads another's state except through the interface. This is the same shape as the existing `ITDDCombatant` precedent (M1 v1.4 lines 796–797).
3. **The directory is support, not production.** It has one implementation because a second one would be two authorities about liveness. Agent 1 hosts it because it needs one world-scoped home, Agent 1's consumers are its heaviest users, and it holds nothing a producer authored.
4. **Nothing in the split requires a MEAD.** The four activities and their owners are the same under all three candidates; only the contract layer's home moves, and TD-12 owns that (§11).

### 3.6 Consequence: this revision needs Agent 2's review of this exact version

`C05-7.2` gives Agent 2 obligations it did not sign up for in the exact wording used here — revision advancement on phase transitions, complete-snapshot messages, registration and deregistration, and the no-coalescing rule. **Those obligations are consistent with their own submission's stance, but "consistent with their stance" is not their agreement.** Agent 2's review of this exact blob is a prerequisite for anything downstream, and it is requested in §17.

---

## 4. The complete revised contract

Readable without the predecessor. `[UNCHANGED]` means the S1 text stands verbatim; `[CHANGED]` and `[NEW]` mark this revision's edits. Every clause is `PROPOSED — NOT FROZEN`.

### 4.1 C05-2.1 — What the contract is about `[UNCHANGED]`

Telegraph timing is published by the **producer** — Agent 2 for enemy attacks, Agent 1 for the player's own attack — as an ordered message stream plus a per-instance pull, and consumed by defence and feedback consumers on both sides. The producer is the sole authority for the values it publishes. **No component in this contract retains a copy of another producer's timing block.** Producer and consumer responsibilities are allocated by activity in `C05-7.2` / `C05-7.3`.

### 4.2 C05-2.2 — Value types (contract-layer types; owner pending TD-12) `[CHANGED]`

```cpp
// PROPOSED — NOT FROZEN. Owner: the cross-agent contract layer of the canonical
// architecture (TDDCore under MEAD-C; no TDDCore module under MEAD-A or MEAD-B,
// whose nearest home is a framework area with no assigned owner). See §11.

struct FTDDTelegraphTiming
{
    double  AxisNow;                 // shared axis = world gameplay time, pause-aware
    double  ActiveEndAxis;
    double  WindupEndAxis;
    double  RecoveryEndAxis;
    float   ProducerRate;            // CustomDilation(producer) at emission
    float   RemainingLocalSeconds;   // producer-local remaining time of the CURRENT phase
    uint32  StateRevision;           // CHANGED: revision of the COMPLETE pull-visible
                                     // state. 1 on Opened; +1 on every phase transition
                                     // and every retime. Renamed from TimingRevision;
                                     // same width and position. Supersedes A1-R3 §3.2
                                     // on this field only.
};

enum class ETDDTelegraphPhase : uint8 { Windup, Active, Recovery };   // closed is terminal

enum class ETDDTelegraphCloseReason : uint8
{
    Natural, Cancelled, Interrupted, ProducerInvalidated, SourceDied
};

struct FTDDTelegraphSnapshot      // what a pull returns and what EVERY message carries
{
    FGuid               AttackInstanceId;
    FGuid               SourceEntityId;
    ETDDTelegraphPhase  Phase;
    FTDDTelegraphTiming Timing;
};

struct FTDDTelegraphMessage       // CHANGED: one struct, complete state, plus the event kind
{
    enum class EKind : uint8 { Opened, PhaseChanged, Retimed, Closed };
    EKind                  Kind;
    FTDDTelegraphSnapshot  Snapshot;      // the complete pull-visible state at emission
    ETDDTelegraphCloseReason CloseReason; // meaningful only when Kind == Closed
};
```

### 4.3 C05-2.3 — The message stream `[CHANGED]`

Four kinds — `Opened`, `PhaseChanged`, `Retimed`, `Closed` — each carrying the **complete snapshot** (`C05-2.3a`). `Closed` additionally carries an `ETDDTelegraphCloseReason` and is **terminal** (`TM-1`). `Opened` establishes revision 1.

> **C05-2.3a.** No message carries a partial aspect of the state. A consumer that receives any message holds the whole state at that revision and therefore never needs a follow-up pull to complete it.

### 4.4 C05-2.4 — The pull surface `[UNCHANGED]`

```cpp
class ITDDTelegraphSource
{
public:
    // Live read of one instance the caller can name. False if not open, never opened
    // by this producer, or this producer is shutting down.
    virtual bool TryGetOpenTelegraph(FGuid AttackInstanceId, FTDDTelegraphSnapshot& Out) const = 0;

    // Instances this producer currently holds open. Per-producer, bounded by that
    // producer's own concurrency. NOT global enumeration and must not be aggregated.
    virtual void GetOpenTelegraphIds(TArray<FGuid>& Out) const = 0;
};
```

### 4.5 C05-2.5 — Resolution through the directory `[UNCHANGED, owner clarified]`

> **DN-1.** The contract layer exposes a resolution function mapping `AttackInstanceId` to the producer that opened it. The directory stores per instance only: the id, `SourceEntityId`, and one **weak liveness handle**. **It stores no timing block, no phase and no revision**, and never serves timing through the handle. Producers register on `Opened` and deregister on `Closed`; the directory drops entries at world teardown and answers `false` for an expired handle. The "no actor pointers" rule applies to published value structs, not to this private liveness record. **Implementation: Agent 1, as shared support; see `C05-7.2` and `C05-7.3`.**

### 4.6 C05-2.6 — Adoption, entry, revision and terminal rules `[CHANGED]`

> **INV-1 (new).** Two observations of one instance carrying the same `StateRevision` are identical in every pull-visible field: phase, all endpoints, `ProducerRate`, `RemainingLocalSeconds`.

> **AD-1.** A consumer adopts a snapshot only if its `StateRevision` is **strictly greater** than the revision it holds. Equal or lower is discarded silently. This applies identically to messages and pulls.

> **AD-2.** If an incoming revision is **greater than held + 1**, the consumer records a revision gap, sets `bStateGapObserved` for that instance and keeps it set until the instance closes. The flag means: *at least one observable state change — phase, retime, or both — was missed.*

> **EN-1.** The **first** observation of an instance by a consumer establishes the baseline: the current phase is recorded as already held and **no entry hook fires** for it. An `Opened` and a pull-derived first observation are the same case.

> **EN-2.** After the baseline, a phase transition is observable **at most once** per consumer per `(AttackInstanceId, phase)`. A `Retimed` never re-fires entry — it changes timing, not phase identity. A duplicate `PhaseChanged` fires nothing.

> **EN-3 (new).** A snapshot adopted **across a revision gap** fires **no** `PhaseEntered` for any phase not observed. The consumer raises exactly one **`Resynchronised(AttackInstanceId, Phase)`** for that gap, carrying the phase it landed in and no transition history, and must not synthesise entries for phases it did not see.

> **TM-1 (new).** `Closed` is **terminal** and is **not** subject to `AD-1`. A `Closed` whose revision equals or precedes the held revision still closes the instance. A producer does not advance `StateRevision` to announce a close.

> **RS-1.** A pull recovers the **current** snapshot of a known instance. It never reconstructs an intermediate revision.
> **RS-2.** No component retains more than one snapshot per instance. The revision counter is not a log.

### 4.7 C05-2.7 — Removal `[UNCHANGED, cross-referenced to TM-1]`

> **RM-1.** An instance ceases to exist on `Closed`, on producer invalidation, on producer unload or stream-out, on producer death-cancel and on world teardown. Invalidation and teardown are not messages: they are observed as a pull returning `false` and a directory entry that no longer resolves. **Removal emits no synthesised message.**
> **RM-2.** A consumer holding state for an instance that returns `false` or no longer resolves **must** treat it as closed, release its block, fire no further entry, and raise no error.

### 4.8 C05-2.8 — What this contract explicitly does not do `[UNCHANGED]`

No retained copy of another producer's state; no global enumeration (X-1 only); no arbitration, parry/block decision or damage application; no clock ownership (TD-06) or contract-layer home (TD-12); no MEAD selection, tag registration, erratum or freeze; **no phase history, revision log or replay.**

### 4.9 Referenced clauses carried forward unchanged `[UNCHANGED]`

Three clause ids are referenced in §8 and §10 but are not restated in full above. Their normative text is unchanged S1 text; they are listed here so that **every clause reference in this document resolves inside this document**.

| Id | Statement, carried forward verbatim in meaning | Full text |
|---|---|---|
| `C05-6.1` | Parry succeeds only when, in the frame in which the hit is resolved, the defender's parry window is active **and** the attacker's phase for that instance is `Active`: a same-frame phase-overlap test against live state, never timestamp subtraction, cross-entity clock comparison or tolerance for a late check. First stated at `A1-R3` §3.4. | S1 §6.1 |
| `C05-6.3` | `Dead > Cinematic > Staggered` over the three carriers of S1 §6.3, evaluated in priority order, first match wins, carriers never compared. `PROPOSED — NOT FROZEN`; it touches C-04 through the proposed amendment `C-04-4`. | S1 §6.3 |
| `C05-7.1` | The contract names no module and no class; its value types, message structs and read interface are contract-layer types of the canonical architecture, owned by whoever TD-12 designates, and the interface must be implementable in a single-module layout. **Its second sentence is withdrawn** and replaced by `C05-7.2` (§3.2). | S1 §7.1, and §3.2 here |

---

## 5. Phase-only revisions — concrete state transitions

Eight worked examples. `rev` is `StateRevision`; "held" is what a given consumer holds; every scenario is a candidate acceptance case (§13).

### 5.1 EX-1 — a phase-only transition, observed in order

| t | Producer event | Message | Snapshot |
|---|---|---|---|
| 1 | wind-up begins, `ProducerRate` 0.05 | `Opened` | Windup, rev **1** |
| 2 | wind-up ends; **no dilation change, endpoints unchanged** | `PhaseChanged` | Active, rev **2** |

Consumer holds rev 1 and receives rev 2: `2 == 1 + 1` → contiguous, adopt, phase differs → **entry fires once**. *This is the case that previously produced rev 1 with a new phase.*

### 5.2 EX-2 — the transition is missed, and a pull recovers it (Agent 3's case (a))

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | **message lost** |
| 3 | nothing changes | pulls: Active, rev **2**; `2 > 1` → adopt; `2 == 1+1` → **not** a gap → entry fires once |

**Recovery now works**, and it works without a gap flag because nothing was actually missed beyond the one message that the pull replaced. Before the correction the pull returned Active at rev 1 and was discarded.

### 5.3 EX-3 — several transitions missed (gap)

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | lost |
| 3 | `PhaseChanged` Recovery, rev 3 | lost |
| 4 | nothing changes | pulls: Recovery, rev **3**; `3 > 1+1` → **gap** |

Adopt Recovery; **no entry** for Active or Recovery; one `Resynchronised(Recovery)`; `bStateGapObserved` set until close. The consumer's phase is now correct and its ignorance is recorded — it is never left on Windup.

### 5.4 EX-4 — a retime only, unchanged behaviour

`Retimed`, rev 3, `ProducerRate` 0.2, endpoints recomputed. Contiguous → adopt, no entry, no resync. (`TN-P-08` still forbids batching; two boundaries in one frame are revs 3 and 4.)

### 5.5 EX-5 — phase change and retime in the same frame

Two observable changes → two revisions, **2** (Active, new rate) then **3** (a second retime if the dilation changes again). A consumer receiving both: entry once at rev 2, adoption at rev 3, no gap. A consumer receiving only rev 3 from a held 1: `3 > 2` → gap → no entry, one resync, phase correct.

### 5.6 EX-6 — repeated pulls and duplicate messages

Consumer at rev 3 pulls twice with no producer change: both return rev 3 with identical content (INV-1), both discarded, no entry, no resync, no diagnostic. A duplicated `PhaseChanged` at rev 3 is likewise a repeat. **A change of phase at an unchanged revision is now unrepresentable**, which is the whole point of `C05-2.6`.

### 5.7 EX-7 — late subscriber, then a real transition

A consumer subscribes mid-Active and pulls Active at rev 5: baseline (`EN-1`), **no entry**. The producer then enters Recovery at rev 6: contiguous, phase differs → **exactly one entry**. A consumer that subscribes and then misses rev 6, pulling rev 7 Recovery later, gets a gap: no entry, one resync.

### 5.8 EX-8 — terminal close at an unchanged revision (Agent 3's case (b))

Consumer holds rev 3. The producer publishes `Closed(Natural)` carrying rev 3, because a close does not advance the state revision. `TM-1` applies: the instance closes, the consumer releases its state, fires no further entry, raises no error. Without `TM-1`, `AD-1` would have discarded the close as an equal revision and left the consumer defending against an attack that ended.

---

## 6. Producer obligations

Fourteen. `TN-P-01` … `TN-P-12` are S1's, with `TN-P-07` amended and the implementer named; `TN-P-13` and `TN-P-14` are new. **Every row is implemented by the owner of that producer** — Agent 2 on its enemy producers, Agent 1 on the player producer (`C05-7.2`) — and no row is implemented by Agent 1 on an Agent 2-owned producer. All tests are `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-P-01** | Publish `Opened` before the first frame the wind-up is observable to a stream consumer. | authored window → `Opened` | A pull consumer that missed `Opened` is not in error; its first pull is a baseline (EN-1). For a stream consumer a missed open is a producer violation. | `Opened` precedes every other message for the instance | T-C05-07 | producer owner |
| **TN-P-02** | `AttackInstanceId` is unique per open instance and never reused. | allocation → `FGuid` | A reused id is a producer violation; consumers and the directory treat it as a new instance and diagnose in Test/Development. | n/a | T-C05-26 | producer owner |
| **TN-P-03** | Exactly one `Closed` per instance, carrying a close reason; no message at all for that instance afterwards. | close event → `Closed` | A second close is a duplicate (rejected); a post-close message is rejected and diagnosed. | after every other message for the instance | T-C05-21 | producer owner |
| **TN-P-04** | Every cancellation path closes: ability cancel, montage abort, interruption, forced transition, requirement change, the producer's own death. | cancel source → `Closed` with the matching reason | An unclosed cancelled instance remains pullable — a producer violation the consumer cannot detect, which is why it is normative. | same frame as the cancel | T-C05-22 | producer owner |
| **TN-P-05** | Invalidate open instances in the teardown path, before the producer stops being valid. | `EndPlay` → deregistration and `Closed(ProducerInvalidated)` | Best effort; the pull's `false` and directory liveness are the fail-safe (TN-R-02), not a substitute. | before removal from the world | T-C05-23 | producer owner |
| **TN-P-06** | Stream-out invalidates only that producer's instances; it neither requires nor implies world teardown. | unload → deregistration of its own ids | Other producers are untouched; world teardown removes everything because the world-scoped owner is destroyed. | n/a | T-C05-24 | producer owner |
| **TN-P-07** | **Amended.** `StateRevision` strictly increases per instance on **every observable state change** — every phase transition and every retime — and two observations at the same revision never differ in any pull-visible field (INV-1). | state change → revision + 1 | An observation at an equal revision with different content is a producer violation and is never applied. | monotone per instance | T-C05-16 | producer owner |
| **TN-P-08** | One `Retimed` per `CustomDilation` change, published in the frame of the change and reflected in live state no later than that frame. **Never batch, coalesce, throttle or defer.** | dilation change → `Retimed` + live-state update | A batched retime is a violation; `UTDDHitStopSubsystem` boundaries are explicitly not exempt. | publish and live-state update in the same frame | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | producer owner |
| **TN-P-09** | Publish no message for an instance that is closed or was never opened. | stray publish → rejected | Rejected with a diagnostic; no directory entry is created and no held state changes. | n/a | T-C05-27 | producer owner |
| **TN-P-10** | All axis values come from the shared axis of `A1-R3` §3.3(a); never wall-clock, frame count or another entity's local time. | engine time → axis value | Any other domain is a violation, detected by a wall-clock fixture. | n/a | T-C05-15 | producer owner |
| **TN-P-11** | `TryGetOpenTelegraph` answers from live state at call time — never a cached copy, never older than the producer's last completed update. | id → snapshot or `false` | A stale copy is a violation; `false` for an open instance is a violation except during teardown (TN-P-05). | as of the last completed update before the call | T-C05-06, T-C05-40 | producer owner |
| **TN-P-12** | No frame deltas, random seeds or tick-order dependence in any published or pulled value. | deterministic inputs → identical outputs | Non-determinism makes every suite flaky; treated as a producer defect. | n/a | T-C05-01 | producer owner |
| **TN-P-13** | **New.** Every phase transition advances `StateRevision` by **exactly one**, even when the timing block and every other value are unchanged. A phase change may not be published at the revision the consumer already holds.* | phase transition → revision + 1 and a `PhaseChanged` carrying the new snapshot | A phase change at an unchanged revision is the defect this obligation exists to forbid; the producer must diagnose it in Test/Development. | one revision per transition; a transition and a retime in the same frame are two revisions | T-C05-43, T-C05-44, T-C05-45 | producer owner |
| **TN-P-14** | **New.** Every message carries the complete snapshot at emission (`C05-2.3a`); no message carries a partial aspect. | state → `FTDDTelegraphMessage` with full snapshot | A partial message is a violation: it can advance the revision while leaving another aspect stale, which is the failure `TN-P-13` closes on the pull path. | n/a | T-C05-49 | producer owner |

\* `TN-P-13` and `TN-P-07` overlap by design: `TN-P-07` states monotonicity for all changes, `TN-P-13` states that phase changes are among them. The duplication is deliberate — the missing case is the one that caused this revision.

---

## 7. Consumer obligations

Nine. `TN-C-01` … `TN-C-08` are S1's, with `TN-C-06` extended for `TM-1`; `TN-C-09` is new. **Each obligation is implemented by each consuming agent in its own code** — Agent 1 for defence, dodge, camera and audio; Agent 2 for AI reaction to the player's telegraph, its audio cue, VFX marker and montage selection (`A2-C05` §8). Tests `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-C-01** | Adopt only on strictly greater `StateRevision`; discard equal or lower silently, for messages and pulls alike. | snapshot, held revision → adopt or discard | Because of INV-1 an equal revision carries identical content, so discarding never loses a change. | commutative — outcome independent of arrival order | T-C05-02, T-C05-03, T-C05-46 | each consumer |
| **TN-C-02** | First observation of an instance establishes the baseline; record the phase as held and fire no entry for it. | first observation → baseline | Firing entry on a baseline double-fires on every subscribe. | baseline before any entry evaluation | T-C05-08, T-C05-09, T-C05-47 | each consumer |
| **TN-C-03** | After the baseline, entry at most once per `(AttackInstanceId, phase)`; a retime never re-fires; a duplicate `PhaseChanged` fires nothing. | phase transition → at most one entry | A second entry for the same phase is detectable by counting. | per consumer, per phase | T-C05-10, T-C05-11 | each consumer |
| **TN-C-04** | On `incoming > held + 1`, record a gap and set `bStateGapObserved` until the instance closes. Never interpolate or extrapolate. | gap → flag | Clearing the flag before close is a violation. | on adoption of the post-gap snapshot | T-C05-12, T-C05-13 | each consumer |
| **TN-C-05** | After a gap, recover with **one** pull; if it is unavailable or not newer, report timing as unknown and diagnose rather than guess. | id → current snapshot or unknown | "Unknown" is a legitimate terminal state for that instance. | once per gap | T-C05-14, T-C05-19, T-C05-44 | each consumer |
| **TN-C-06** | **Extended.** Removal is closure: a pull returning `false`, an unresolvable id, or a `Closed` message means closed — release the block, fire no further entry, raise no error. **A `Closed` closes regardless of its revision (TM-1).** | false, unresolvable id, or `Closed` → closure | Treating "not found" as an error is a defect; so is discarding a `Closed` because its revision is not newer. | immediate on observation | T-C05-25, T-C05-48 | each consumer |
| **TN-C-07** | Evaluate `Dead > Cinematic > Staggered` in priority order over the three carriers of `C05-6.3`; never compare carriers. | published state → one effective value | Comparing an enum to a tag is a violation. | priority order, first match wins | T-C05-35, T-C05-36, T-C05-37, T-C05-38, T-C05-39 | each consumer |
| **TN-C-08** | Never treat a pull as revision history; a post-gap block is current state, not a substitute for what was missed. | pull result → current value | A consumer that assumes full recovery makes telemetry and AI timings silently wrong. | n/a | T-C05-20, T-C05-50 | each consumer |
| **TN-C-09** | **New.** A snapshot adopted across a gap fires no `PhaseEntered`; the consumer raises exactly **one** `Resynchronised(instance, phase)` per gap, carrying the phase it landed in and no history, and synthesises no entries for phases it did not observe. | gap adoption → zero entries, one resync | A fabricated `PhaseEntered` is a violation; more than one `Resynchronised` per gap is a violation; a resync after a contiguous adoption is a violation. | immediately on gap adoption, before any further entry evaluation | T-C05-45, T-C05-50 | each consumer |

---

## 8. Shared read-surface and arbitration obligations

`TN-R-01` … `TN-R-04` are S1's; `TN-R-05` is new. `TN-A-01` / `TN-A-02` are unchanged. Tests `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-R-01** | The directory stores per instance only the id, `SourceEntityId` and one weak liveness handle — no timing, no phase, no revision — and never serves timing through the handle. | registration → association record | A record carrying timing is a violation detectable by structure. An expired handle resolves `false`; teardown drops all. | registration completes before a pull by id can succeed | T-C05-28, T-C05-29 | Agent 1, shared support |
| **TN-R-02** | `TryGetOpenTelegraph` returns `false` for closed instances, instances the producer never opened, and instances during teardown; never a partial or stale-filled record. | id → snapshot or `false` | `false` is never an error (RM-2); `true` for a closed instance is a violation. | n/a | T-C05-04, T-C05-05 | producer owner |
| **TN-R-03** | `GetOpenTelegraphIds` reports only the calling producer's own instances; not a world query, not aggregated in this version, not X-1. | producer → its ids | Answering with other producers' ids would silently re-create custody. | n/a | T-C05-30 | producer owner |
| **TN-R-04** | A pull returns a value copy, is callable from any consumer phase without re-entrancy, reflects the producer's last completed update, and mutates nothing the caller can see. | call → copy | A returned reference into producer storage or a re-entrant marshal is a violation. | as of the last completed update | T-C05-31 | producer owner |
| **TN-R-05** | **New.** A pull at revision `R` returns content identical to every other observation of that instance at `R` — the read surface may not manufacture a state the revision does not cover. | id, held revision → snapshot | If it can, INV-1 is false and equal-revision discard becomes unsafe again; the producer must diagnose. | n/a | T-C05-46, T-C05-49 | producer owner |
| **TN-A-01** | Parry is `C05-6.1`: same-frame phase overlap. The attacker's phase is read on the hit-resolution path from the component that owns the attack instance — never from the pull, the directory or a published block; no timestamp subtraction, no late tolerance. | hit data, defence state, attacker live phase → parry outcome | Any C-05 value influencing the outcome is a violation; a wrong timing block must not change the result. | in the frame the hit is resolved | T-C05-32, T-C05-33 | Agent 1, subject to TD-09 |
| **TN-A-02** | No arbitration decision depends on any value produced by the C-05 contract. | as above → outcome plus diagnostic | An observed read of the telegraph surface on the arbitration path is a violation, detectable with a spy. | n/a | T-C05-34 | Agent 1, subject to TD-09 |

---

## 9. Lifecycle, invalidation, revision and hitstop semantics

Everything in S1 §5 stands. Four sentences change, and they are the ones this revision is about:

1. **§5.1 (revision representation).** One revision per instance covering the whole pull-visible state; it advances on every phase transition and every retime; every message carries the complete snapshot. Still no history: one snapshot per instance.
2. **§5.2 (detection).** The four arithmetic cases of §2.5 above replace S1's five-row table; the only substantive change is that `equal revision` now guarantees identical content, and that a terminal `Closed` bypasses the comparison entirely.
3. **§5.3 (recovery).** A single pull recovers the current snapshot. **If the gap is one revision, the transition is contiguous and entry fires; if it is larger, no entry fires and exactly one resync is raised.** S1 had no rule for either case because a phase change at an equal revision was impossible to express; it is now impossible to express *and* recoverable.
4. **§5.5 (hitstop).** Unchanged: each boundary is one revision, never batched. One clarification: because a hitstop boundary changes only dilation, its revisions are retimes, not phase changes — a burst of boundaries produces a burst of `Retimed` at consecutive revisions, and a consumer that receives them all sees no gap.

S1 §5.4 (messages versus pull), §5.6 (why a missed revision cannot be mistaken for continuity) and §6 (arbitration independence) are unchanged. §5.6's three mechanisms still hold, and the first of them is now stronger: the revision arithmetic covers phase, so "no observable change" and "no revision change" are the same statement in both directions.

---

## 10. Combat-arbitration independence `[UNCHANGED]`

`C05-6.1` (parry rule, restated in S1 §6.1), `TN-A-01` and `TN-A-02` stand as written. The directory still holds nothing the arbitration path could use; the parry phase source is still defined by role, so the separation holds under all three candidates. **The parry authority itself remains externally unsettled by TD-09 and is not resolved here.** The only change in this section is the implementer column: arbitration is Agent 1's, subject to that erratum.

---

## 11. MEAD-neutral ownership boundary `[UNCHANGED, clarified by C05-7.2]`

`C05-7.1` stands minus its second sentence, which `C05-7.2` replaces (§3.3). The contract still names no module and no class: value types, message structs and the read interface are contract-layer artefacts whose owner TD-12 designates; the producer-side implementation is the producer owner's; the shared support is Agent 1's; consumer integration is each consumer's. **This remains consistent under MEAD-A (no `TDDCore`; framework area, unassigned), MEAD-B (no `TDDCore`) and MEAD-C (`TDDCore`, Agent 3).** No MEAD is selected by this document.

The one thing that could now break neutrality is an ownership clause that presumes a module — and `C05-7.2` avoids that by naming **activities and agents**, never classes or modules, except where it says the contract layer's owner is TD-12's to name.

---

## 12. Traceability — requirement → clause → test

### 12.1 Finding 1's six questions

| Requirement (Agent 3 / task) | Clause | Test |
|---|---|---|
| Does every observable phase change advance the producer revision? | `INV-1`, `TN-P-07`, `TN-P-13` | T-C05-43, T-C05-45, T-C05-46 |
| Does a phase-**only** change produce a new revision even when timing is unchanged? | `TN-P-13`, `C05-2.2` (StateRevision) | T-C05-43 |
| How does a consumer distinguish a genuinely new phase state from a repeated observation? | §2.5 comparison table, `AD-1`, `INV-1`, `TN-C-01`, `TN-R-05` | T-C05-46, T-C05-49 |
| What happens when a consumer misses one or more phase transitions? | `AD-2`, `EN-3`, `TN-C-04`, `TN-C-09`, `RS-1` | T-C05-44, T-C05-45, T-C05-50 |
| Do the stale and gap rules remain consistent? | §2.8 consistency table; `AD-1`/`AD-2` unchanged; `TM-1` scopes terminal close | T-C05-48 |
| Required behaviour for initial observation, late subscription and subsequent pulls | `EN-1`, `EN-2`, `EN-3`, `C05-2.6`; examples EX-1, EX-2, EX-6, EX-7 | T-C05-08, T-C05-09, T-C05-44, T-C05-47 |

### 12.2 Finding 2's four distinctions

| Distinction | Where stated | Consistency check |
|---|---|---|
| Ownership of enemy telegraph / gameplay production | `C05-2.1`, `C05-7.2` row 1 | unchanged from S1; matches TD v1.2 C-05 and `A2-C05` §8 |
| Ownership of the producer-side implementation | `C05-7.2` row 2, `C05-7.3`, implementer column in §6 | **the sentence it replaces is gone** (`C05-7.1`) |
| Ownership of shared interfaces and contracts | `C05-7.2` row 3, `C05-2.2`, `C05-2.4` | owner left to TD-12; no module named |
| Ownership of consumer integration | `C05-7.2` row 5, implementer column in §7 | matches TD v1.2 C-05 and `A2-C05` §8's consumer list |

### 12.3 Obligation → test coverage

| Obligation | Cases | Obligation | Cases |
|---|---|---|---|
| TN-P-01 | T-C05-07 | TN-C-02 | T-C05-08, T-C05-09, T-C05-47 |
| TN-P-02 | T-C05-26 | TN-C-03 | T-C05-10, T-C05-11 |
| TN-P-03 | T-C05-21 | TN-C-04 | T-C05-12, T-C05-13 |
| TN-P-04 | T-C05-22 | TN-C-05 | T-C05-14, T-C05-19, T-C05-44 |
| TN-P-05 | T-C05-23 | TN-C-06 | T-C05-25, T-C05-48 |
| TN-P-06 | T-C05-24 | TN-C-07 | T-C05-35 … T-C05-39 |
| TN-P-07 | T-C05-16 | TN-C-08 | T-C05-20, T-C05-50 |
| TN-P-08 | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | TN-C-09 | T-C05-45, T-C05-50 |
| TN-P-09 | T-C05-27 | TN-R-01 | T-C05-28, T-C05-29 |
| TN-P-10 | T-C05-15 | TN-R-02 | T-C05-04, T-C05-05 |
| TN-P-11 | T-C05-06, T-C05-40, T-C05-42 | TN-R-03 | T-C05-30 |
| TN-P-12 | T-C05-01 | TN-R-04 | T-C05-31 |
| TN-P-13 | T-C05-43, T-C05-44, T-C05-45 | TN-R-05 | T-C05-46, T-C05-49 |
| TN-P-14 | T-C05-49 | TN-A-01 | T-C05-32, T-C05-33 |
| TN-C-01 | T-C05-02, T-C05-03, T-C05-46 | TN-A-02 | T-C05-34 |

**30 obligations, every one covered.** `TN-C-01`'s third case (`T-C05-46`) is the INV-1 check that makes equal-revision discard safe.

---

## 13. Acceptance tests and executed checks

### 13.1 The suites

**50 cases, 11 suites, `PROPOSED / NOT RUN`, zero executed.** Suites A–I are S1's, unchanged except for the case they now cover where noted; J and K are new.

| # | Suite | Covers | Cases | Case ids |
|---|---|---|---|---|
| A | `TDD-Contract.Combat.TelegraphPullRecovery` | TN-P-12, TN-C-01, TN-R-02, TN-P-11 | 6 | T-C05-01 … 06 |
| B | `TDD-Contract.Combat.TelegraphEntryBaseline` | TN-P-01, TN-C-02, TN-C-03 | 5 | T-C05-07 … 11 |
| C | `TDD-Contract.Combat.TelegraphRevisionGapDetection` | TN-C-04, TN-C-05, TN-P-10, TN-P-07 | 5 | T-C05-12 … 16 |
| D | `TDD-Contract.Combat.TelegraphHitstopRevisionBurst` | TN-P-08, TN-C-05, TN-C-08 | 4 | T-C05-17 … 20 |
| E | `TDD-Contract.Combat.TelegraphProducerLossPull` | TN-P-03, TN-P-04, TN-P-05, TN-P-06, TN-C-06, TN-P-02, TN-P-09 | 7 | T-C05-21 … 27 |
| F | `TDD-Contract.Combat.TelegraphResolutionAndDirectory` | TN-R-01, TN-R-03, TN-R-04 | 4 | T-C05-28 … 31 |
| G | `TDD-Contract.Combat.TelegraphArbitrationIndependence` | TN-A-01, TN-A-02 | 3 | T-C05-32 … 34 |
| H | `TDD-Contract.Combat.TelegraphDeadPrecedenceEvaluation` | TN-C-07 | 5 | T-C05-35 … 39 |
| I | `TDD-Contract.Combat.TelegraphSameFrameCoherence` | TN-P-08, TN-P-11, TN-C-01 | 3 | T-C05-40 … 42 |
| **J** | **`TDD-Contract.Combat.TelegraphPhaseRevisionAdvancement`** | **TN-P-13, TN-C-05, TN-C-09, TN-R-05** | **4** | **T-C05-43 … 46** |
| **K** | **`TDD-Contract.Combat.TelegraphResyncTerminalAndLateSubscriber`** | **TN-C-02, TN-C-06, TN-P-14, TN-C-09** | **4** | **T-C05-47 … 50** |

### 13.2 The eight new cases, specified

| Case | Setup | Assertion |
|---|---|---|
| **T-C05-43** | Phase-only transition: consumer holds Windup rev 1; producer enters Active with `ProducerRate` and every endpoint unchanged | the `PhaseChanged` carries rev **2**; the pull after it returns rev 2; exactly one entry fires |
| **T-C05-44** | Agent 3's case (a): the rev-2 `PhaseChanged` is dropped; the consumer then pulls | pull returns **Active at rev 2**; `2 == 1+1` so no gap flag; the phase is corrected; exactly one entry fires |
| **T-C05-45** | Two transitions missed: held rev 1, pull returns Recovery at rev 3 | gap flagged; phase corrected to Recovery; **no** entry for Active or Recovery; exactly **one** `Resynchronised(Recovery)`; flag persists until close |
| **T-C05-46** | Same revision observed three ways: two pulls and one duplicated message at rev 3 | all three are **byte-identical** in every pull-visible field (INV-1); the duplicates are discarded; no entry, no resync, no diagnostic |
| **T-C05-47** | Late subscriber: first observation mid-Active at rev 5, then a contiguous transition to Recovery at rev 6 | no entry at the baseline; exactly one entry at rev 6; no resync |
| **T-C05-48** | Agent 3's case (b): consumer holds rev 3; `Closed(Natural)` also carries rev 3 | the instance **closes**; block released; no further entry; no error; `TryGetOpenTelegraph` returns `false` |
| **T-C05-49** | Full-snapshot payload: for each of the four message kinds, compare the message's snapshot with a pull at the same revision | identical in phase, all endpoints, `ProducerRate`, `RemainingLocalSeconds` and revision; no message carries a partial aspect |
| **T-C05-50** | Resync discipline: a gap adoption followed by two contiguous transitions | exactly one `Resynchronised` for the gap and none afterwards; entries fire only for the contiguous transitions; no fabricated entry for the unobserved phase |

### 13.3 Document-validation checks — executed

Static checks on **this document**, not tests of contract behaviour. Run with a read-only Python pass over the published file.

| Check | Rule | Result |
|---|---|---|
| DV-1 every obligation declared once and covered | 30 declared, no duplicates, all present in §12.3 | **PASS** — 30 obligations, 0 duplicates, all covered in §12.3 |
| DV-2 case ids complete | `T-C05-01` … `T-C05-50`, ranges expanded, none missing or extra | **PASS** — 01…50 present, none missing or extra |
| DV-3 every obligation row names an implementer | the implementer column is filled on all 30 rows | **PASS** — implementer column filled on all 30 rows |
| DV-4 the superseded ownership sentence is gone | the withdrawn claim appears only inside the correction ledger, never in a normative clause | **PASS** — 1 occurrence, inside the §3.2 correction ledger |
| DV-5 clause ids defined once, none dangling | every `C05-*` reference resolves to a definition or a carried-forward statement inside this document | **PASS** — 14 referenced, 0 unresolved |
| DV-6 suite and case arithmetic | 11 suite rows; case column sums to the stated 50 | **PASS** — 11 suite rows, case column sums to 50 |
| DV-7 the three external blockers remain listed and open | TD-06, TD-09, TD-12 each present in §14 with status unchanged | **PASS** — TD-06, TD-09, TD-12 present and still `OPEN` |
| DV-8 no acceptance test reported as executed | every occurrence of "executed" refers to document checks, and "0 executed" appears for acceptance tests | **PASS** — 10 occurrences of "execut", all about document checks or negated; "0 executed" present |
| DV-9 no unqualified `TDDCore` assertion | every `TDDCore` mention names a MEAD | **PASS** |
| DV-10 every table is well formed | each table block has the same cell count on every row | **PASS** — 0 malformed tables, 22 tables |

### 13.4 What is not claimed

**Acceptance tests executed: 0. Written against Agent 1 code: 0. Unreal tests run: 0. No engine, no compiler and no project exist in this workspace (ADR-0012).** The ten document checks are the only executed evidence in this document, and a passing document check is a statement about text, never about behaviour.

---

## 14. Unresolved dependencies and external blockers

**Unchanged by this revision, and explicitly not resolved by it.**

| ID | Dependency | Blocks | Status |
|---|---|---|---|
| **B-1** | **TD-06** — clock ownership and the shared axis | any code that stamps or ages timing | **OPEN** — TD |
| **B-2** | **TD-09** — parry-authority location and the MEAD-C/MEAD-A erratum | implementing the arbitration path | **OPEN** — TD |
| **B-3** | No engine, compiler or project in this workspace (ADR-0012) | executing any of the 50 cases | **OPEN** — Phase 0 |
| **B-4** | **TD-12** — canonical MEAD and the contract-layer owner | freezing the value types and read interface | **OPEN** — TD |
| **B-5** | U-07 / global enumeration (X-1 only) | nothing in C-05 | **OPEN**, conditional |
| **B-6** | U-15 damage-request spelling | C-03 only | **OPEN** — TD |
| **B-7** | U-14 `Status.Dead` grant | C-04 only | **OPEN** — registry |
| **B-8** | TD-13 save inventory | C-07 only | **OPEN** — Agent 3 |

**Two additions this revision makes to the dependency list, both process rather than technical:**

| ID | Dependency | Why |
|---|---|---|
| **B-9** | **Agent 2's review of this exact blob** | `C05-7.2` gives Agent 2 producer obligations in new wording (revision advancement, complete-snapshot messages, registration). Consistency with their stance is not their agreement |
| **B-10** | **TD ruling on `Resynchronised`** if any consumer wants it routed beyond the local process | the signal is consumer-side today; making it a cross-agent event would need the contract layer's owner (TD-12) and is **not proposed here** |

**No status in this table has changed since S1.** This revision does not claim to have resolved TD-06, TD-09 or TD-12, and does not imply that a TD decision is no longer needed.

---

## 15. Change log and supersession

### 15.1 Exactly what changed from `A1-C05-S1`

| Artefact | Change |
|---|---|
| `C05-2.2` | `TimingRevision` → **`StateRevision`**; normative meaning widened to the complete pull-visible state; comment states phase transitions and retimes both advance it. `FTDDTelegraphMessage` added as the single message struct carrying the complete snapshot |
| `C05-2.3` | New `C05-2.3a`: every message carries the complete snapshot; no partial aspects |
| `C05-2.6` | `INV-1` added; `AD-1`/`AD-2` restated (mechanism unchanged, meaning widened); `EN-1`/`EN-2` unchanged; **`EN-3`** and **`TM-1`** added; `RS-1`/`RS-2` unchanged |
| `C05-2.7` | `RM-1`/`RM-2` unchanged, cross-referenced to `TM-1` |
| `C05-2.8` | Adds "no phase history, revision log or replay" to the non-goals |
| **`C05-7.2`** | **New** — ownership by activity, replacing the second sentence of `C05-7.1` |
| **`C05-7.3`** | **New** — what "Agent 1 implements" means |
| `C05-7.1` | Offending sentence removed; neutrality claim otherwise unchanged |
| `TN-P-07` | Amended: monotonicity over **all** observable state changes, plus INV-1 |
| **`TN-P-13`**, **`TN-P-14`** | **New** — phase transitions advance the revision; complete-snapshot messages |
| `TN-C-01` | Cross-references INV-1 as the reason equal-revision discard is safe |
| `TN-C-06` | Extended with `TM-1`: `Closed` closes regardless of revision |
| **`TN-C-09`** | **New** — resync discipline for gap adoption |
| **`TN-R-05`** | **New** — a pull at revision `R` returns the state `R` versions |
| §5 (semantics) | Four sentences updated; the rest of S1 §5 stands |
| §13 | **8 new cases** (`T-C05-43` … `50`) in two new suites (J, K); total now 50 |
| Every obligation table | Implementer column added; totals now 30 obligations (14 P, 9 C, 5 R, 2 A) |
| §12 | New traceability tables for both findings |
| **§4.9** | **New** — the three clause ids referenced by §8 and §10 (`C05-6.1`, `C05-6.3`, `C05-7.1`) carried forward with one-line statements, so every reference resolves inside this document |

### 15.2 What did **not** change

The per-instance, no-history recovery model; the pull-based approach; the producer-state versus consumer-observation distinction; the directory's liveness-only content; the MEAD-neutral position; `C05-2.1`, `C05-2.4`, `C05-2.5`; `TN-P-01` … `TN-P-12` except `TN-P-07`; `TN-C-02` … `TN-C-05`, `TN-C-07`, `TN-C-08`; `TN-R-01` … `TN-R-04`; `TN-A-01`/`TN-A-02`; the arbitration boundary; X-1 and its evidence bar; every blocker's status; every earlier document.

### 15.3 Supersession

`A1-C05-S2` supersedes `A1-C05-S1` **by statement, not by edit**. S1 remains on the branch at `2bb729f` with blob `dcec9e1a…`, unmodified, as the record of what Agent 3 assessed. Where S1 and S2 differ, S2 is the current C-05 text; where S2 is silent, S1 stands except for the clauses enumerated in §15.1.

**The one field-level supersession worth naming:** `A1-R3` §3.2 defined `TimingRevision`; `A1-C05-S2` renames it `StateRevision` with widened meaning. `A1-R3` is unmodified; the successor supersedes that field.

---

## 16. Publication

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V2.md` — **new file** |
| Version | 2.0 (`A1-C05-S2`) |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `e5ddad6965e06b179061d8cebb6ffecf59829224` |
| Blob at that commit | `bf6c8fb3ddf3152d1627d3b6471278f57fc82541` |
| Superseded | `A1-C05-S1` v1.0 at `2bb729f`, blob `dcec9e1a…` — **unmodified** |
| `A1-R1` / `A1-R2` / `A1-R3` / `A1-R4` / C-05-3 response | `25ab47c2…` / `5ee2769…` / `109331f3…` / `2cc548fa…` / `a94b49ef…` — **unmodified** |
| Agent 3's assessment (`1eb613f`) and recommendation (`58ec7fd`) | read only, **not modified** |
| Agent 2's reviews (`4c09980`, `7ea0a85`, `586152b`) and submission (`3ac438b`) | read only, **not modified** |
| MEAD-A / MEAD-B / MEAD-C | read only; none moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| Contracts signed / frozen | **None** — C-05 remains proposed and unsigned |
| Code, Core types, project, merge, M0 | **None** |
| Acceptance tests | 50 cases `PROPOSED / NOT RUN`, **0 executed**; 10 document checks executed (§13.3) |

---

## 17. Handoff

### 17.1 Summary of the two corrections

1. **Phase changes now version the state.** `StateRevision` covers the complete pull-visible state and advances on every phase transition as well as every retime; every message carries the complete snapshot; `INV-1` makes "equal revision" mean "identical state", which is what makes equal-revision discard safe; a terminal `Closed` bypasses the freshness rule; a gap adoption fires no fabricated entry and raises exactly one `Resynchronised`. **No history, no bus, no second counter.**
2. **Ownership is now split by activity.** Enemy production *and* the producer-side implementation on enemy producers are Agent 2's; the player producer's are Agent 1's; shared artefacts belong to the contract layer pending TD-12; Agent 1 implements the shared directory and resolution support and **no part of an Agent 2-owned producer**; consumer integration belongs to each consuming agent.

### 17.2 Request to Agent 2 — one review of this exact blob

Five questions, and nothing broader:

1. Does `C05-7.2` state your producer obligations accurately — revision advancement on phase transitions (`TN-P-13`), complete-snapshot messages (`TN-P-14`), registration and deregistration, one `Retimed` per dilation change with no coalescing?
2. Is `Inv-1` implementable on your producers, given that your attacks change phase without changing dilation — and is there any case in your attack set where a phase change and a timing change are genuinely simultaneous and you cannot order them?
3. Does `Resynchronised` (`EN-3`, `TN-C-09`) give your AI what it needs when it has been blind across a gap, or does your defensive logic need something the signal does not carry?
4. Do the consumer obligations in §7 match what your AI, audio cue, VFX marker and montage selection actually require from a pull?
5. Is there any conflict between the implementer column in §6–§8 and your submission's own assignment in `A2-C05` §8?

**No signature is requested and none is implied**; a review verdict is not a contract version.

### 17.3 Request to Agent 3 — one bounded reassessment

Scope: whether the two corrections close the two blocking findings, and whether anything in the correction broke a property their assessment found sound.

1. Does `StateRevision` over the complete state close the phase-only defect, including the message-path variant in §2.4 that their wording did not name?
2. Do `INV-1`, `TM-1` and `EN-3` remain consistent with the no-history recovery model, or do they imply retained history they did not intend?
3. Does `C05-7.2` resolve the ownership mismatch without contradicting TD v1.2's C-05 row or `A2-C05` §8?
4. Does anything in this revision disturb MEAD neutrality, arbitration separation, the lifecycle model or X-1's conditional status?

### 17.4 Status

`DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD is selected. TD-06, TD-09 and TD-12 are untouched and remain external blockers (B-1, B-2, B-4).** 50 acceptance cases are proposed and unexecuted; ten document checks pass and prove nothing about behaviour.
