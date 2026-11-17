# Agent 1 — C-05 Successor Contract (`A1-C05-S1`)

**Response ID:** `TDD-A1-C05-SUCCESSOR-001`
**Version:** 1.0 — successor to the C-05 telegraph proposal, superseding `A1-R4` §4.1 and `TDD-A1-C05-3-RESPONSE-001` v1.0 as the current C-05 position
**Date:** 2026-11-17 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no C++, no Unreal project, no API or contract freeze, **no MEAD selection**, no tag registration, no erratum, no merge, no M0 or implementation-readiness claim. **No contract is bilaterally agreed and nothing here is a signature.**

| Basis | Exact version | Commit | Blob / note |
|---|---|---|---|
| Agent 2's review of the C-05-3 response (the review this document answers) | `AGENT2_REVIEW_A1_C05_3_V1` v1.0 | `586152b0f3992b188fb3861a970c32c62478666b` | `Docs/AGENT2_REVIEW_A1_C05_3_V1.md`, 1,117 lines, read in full |
| My response under review | `TDD-A1-C05-3-RESPONSE-001` v1.0 | `22c29daddc3b7a9285ceb4709113d9657ddbe0bd` | `a94b49efb65c671c6c9fc8bb56436778aeb7030b` |
| `A1-R4` (baseline named in the task) | v1.3 | `142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6` | `2cc548faf86cb9b30cd2e26386fc672edbdd9f75` |
| `A1-R3` — source of the normative parry rule | v1.2 | `70db9665b67723a526a6d40fa71ec832f1a95498` | `109331f36eddce7eee068aa278a474c07c950753`, §3.4 |
| Agent 3's recommendation (related, not adopted as mandatory) | `TDD-A3-ARCH-RECOMMENDATION-C05-3` v1.0 | `58ec7fd4bacbaaddf55f64e3e784de5c3fc8b0e6` | `79b79e30263b905262672993f4e3e8943df5d921` |
| M1 v1.4 — `ITDDCombatant` precedent | 1.4 | `22c29dad…` | lines 796–797 |
| MEAD-A / MEAD-B / MEAD-C | candidates | `912fac9` / `58ec7fd` / `169a8d8` | read only; **none selected** |

---

## 0. Reading notes

### 0.1 What changed in my position, in one paragraph

`A1-R4` §4.1 proposed a **stateful Core broker**. My C-05-3 response **relocated** it to an Agent 1 world-scoped custodian and added twelve conditions. Agent 2's review found that the relocation was sound but the resulting model was **not implementable** — six blocking defects, two of which contradict my own text — and that **no document establishes the requirement** the custodian exists to serve. This document accepts all of that and takes the smaller route the review's own §12.1 offers: **per-instance recovery from the producer, with a directory that stores associations and liveness only and never stores timing.** There is no custodian, no stored timing block, no eviction policy, no stored-copy ordering problem and no cross-agent write path for timing.

### 0.2 The review's own correction, acknowledged

Agent 2's §0.3 withdraws its `A1-R4` §7.2 citation finding: `A1-R4` says `(506)` and contains no "505". I recorded that in my previous response and did not ask for a correction; A2 has made one anyway, with a root cause and an extended countermeasure. **Acknowledged, and I adopt the two-command check from their §0.4 for every citation in this document.**

### 0.3 What this document is and is not

It **is** the revised C-05 contract text, the producer and consumer obligations that make it testable, the hitstop and revision semantics the task asks for, the six findings answered clause by clause, and the acceptance-test matrix.

It is **not** an exploratory paper, a signature, a freeze, a MEAD selection, or a request for another review. It hands to Agent 3 for one bounded integration-readiness assessment (§13), and it does not reopen anything the review did not raise.

### 0.4 The one place I disagree with the review's framing

A2 §4.3 says the twelve-condition custody model is "a larger specification surface than the recovery problem it solves" and that the per-instance alternative needs "one condition, not twelve". **The arithmetic is right and the conclusion is right; the "one condition" is one too few.** Per-instance recovery needs **three** things: the query, the resolution rule their C13 names, and a liveness rule for when the producer is gone (§2.6). That is still a factor of four smaller than the custody model, which is the point — but I do not want the successor's own size understated in the document that has to carry it.

---

## 1. Executive decision and architectural rationale

### 1.1 The decision

> **C-05's recovery requirement is met by a per-instance pull from the producing object, reached through a directory that holds associations and liveness only. No component retains telegraph timing state. Global enumeration is not adopted; it is retained as a conditional future extension with a stated evidence bar (§1.4).**

### 1.2 Why this is the right model, in the order the reasons actually bind

1. **The data already lives where the requirement is.** A consumer that missed a revision holds an `AttackInstanceId` and asks about that id. The producer owns the block, the phase and the revision; a pull reads them where they are. `A1-R3` §3.3(c)4 said a stale consumer "re-queries if a query surface exists" — this is that surface, addressed to the object that already knows the answer.
2. **Precedent rather than novelty.** `ITDDCombatant::IsTelegraphingAttack()` and `GetAttackTelegraphRemaining()` exist at M1 v1.4 lines 796–797, and C-02 already publishes `bIsTelegraphing` / `TelegraphRemainingSeconds` as **Required** for Agent 2. The successor generalises an existing per-actor read into a per-instance read; it does not introduce a new kind of surface.
3. **The producer's lifetime is the state's lifetime.** There is nothing to evict, because there is no second copy. Producer destroyed, unloaded or dead ⇒ the pull returns `false`. The invalidation problem that consumed a third of the twelve conditions **does not exist** in this model.
4. **No stored copy, no ordering problem.** A stored block can be stale relative to a message; a live read cannot be, because it is taken at call time. The ordering condition (my C8) was written to make a *stale copy* detectable, and with no copy there is nothing to detect. What remains is a coherence obligation on the producer, not an ordering point across objects (§5.4).
5. **The arbitration path stays untouched.** The parry rule reads live phase state on the hit path. Under this model "live phase state" is the producer's own state read on the hit path — the same state the pull exposes but read on a different path — so the severity bound holds by construction and not by a clause forbidding a read (§6).

### 1.3 What the model costs, stated rather than implied

A2 §3.4 was right that my previous ledger had one row where it needed three. The honest accounting:

| What a central custodian would buy | Is it bought by the pull model? |
|---|---|
| **Cross-producer enumeration** (every open telegraph at one instant) | **No.** Without it a consumer can see only instances it has observed or can enumerate per producer. |
| **Removal visibility for a consumer that has forgotten an id** | **No** — but a consumer cannot forget an id it is holding state against, so this case does not arise for a conforming consumer (§4.3). |
| **Single-instant consistency across two producers** (needed by "the most imminent telegraph" camera case) | **No.** Two pulls are two instants. This is the strongest argument for custody and it belongs in the ledger, not in a footnote. |
| A second copy of the timing block | **Not bought, and not wanted** (§1.2 reasons 3–4). |

**Therefore:** if a consumer exists that must compare two open telegraphs at one instant, the pull model does not serve it and the conditional extension (§1.4) must be re-opened. Today no such consumer has a stated requirement, a failure mode or a test.

### 1.4 The conditional future extension, with its evidence bar

If the TD decides enumeration is in scope, the extension is one added read surface over the same records — **not** a re-run of the custody debate:

> **X-1 (conditional, not adopted).** A contract-layer read returns one snapshot, at one instant, of every open telegraph. It is adopted only when a named consumer's stated decision fails without it, and the failure is demonstrable in a test that a per-instance pull cannot satisfy. If adopted, A2's §9.3–§9.5 conditions (revision-history limit, entry baseline, inline validity, named coherence point) attach to it unchanged, and my C1 gate applies.

**Evidence required before X-1 can be discussed again:** (a) a camera/audio/UI document stating the decision and its failure mode, in the shape C-02's `ControlState` request took; or (b) an acceptance test that a name-addressed pull cannot satisfy; or (c) a TD ruling that enumeration is in scope for this slice. **A2 §12.2 lists the same three; I adopt them as the bar.** Until one exists, this document does not depend on enumeration and does not build it.

---

## 2. Revised C-05 contract

Every clause below is `PROPOSED — NOT FROZEN`. Clause identifiers (`C05-2.x`) are for citation and for the test matrix in §9.

### 2.1 C05-2.1 — What the contract is about

Telegraph timing is published by the **producer** — Agent 2 for enemy attacks, Agent 1 for the player's own attack (`A1-R1` §5.1) — as an ordered message stream plus a per-instance pull, and consumed by defence/feedback consumers on both sides. The producer is the sole authority for the values it publishes. **No component in this contract retains a copy of another producer's timing block.**

### 2.2 C05-2.2 — Value types (contract-layer types; owner pending TD-12)

```cpp
// PROPOSED — NOT FROZEN. Owner: the cross-agent contract layer of the canonical
// architecture. Under MEAD-C that layer is TDDCore (Agent 3).
// Under MEAD-A there is no TDDCore module at all; the nearest home there is
// TDDRuntime/Framework, with no owner assigned by that document.
// See §7. The owner is NOT settled by this document.

struct FTDDTelegraphTiming        // unchanged from A1-R3 §3.2 — restated, not redefined
{
    double  AxisNow;                 // shared axis = world gameplay time, pause-aware
    double  WindupEndAxis;
    double  ActiveEndAxis;
    double  RecoveryEndAxis;
    float   ProducerRate;            // CustomDilation(producer) at emission
    float   RemainingLocalSeconds;   // producer-local remaining time of the CURRENT phase
    uint32  TimingRevision;          // +1 on every retime; 1 on Opened
};

enum class ETDDTelegraphPhase : uint8 { Windup, Active, Recovery };   // closed is terminal, not a phase

enum class ETDDTelegraphCloseReason : uint8
{
    Natural,            // phase set completed
    Cancelled,          // ability/montage/input cancel
    Interrupted,        // hit, stagger or forced transition
    ProducerInvalidated,// teardown, unload, stream-out
    SourceDied          // the producing actor died, cancelling its own attack
};

struct FTDDTelegraphSnapshot      // what a pull returns; value-only, no pointers
{
    FGuid               AttackInstanceId;
    FGuid               SourceEntityId;
    ETDDTelegraphPhase  Phase;
    FTDDTelegraphTiming Timing;
};
```

**`ETDDTelegraphPhase` and `ETDDTelegraphCloseReason` are formalisations, not new design.** The three phases are the three endpoint groups already in `A1-R3` §3.2; the close reasons name the five cancellation sources this series has already enumerated (P3, §3 of this document, and A2's N3).

### 2.3 C05-2.3 — The message stream (unchanged contract, one addition)

`Opened`, `PhaseChanged`, `Retimed`, `Closed` — as in `A1-R1` §5.2 and `A1-R3` §3.2/§3.3, with two changes:

1. **`Closed` carries an `ETDDTelegraphCloseReason`** (fixes A2's N3: the previous text required "a reason value" and defined none).
2. **Each message carries `SourceEntityId` and `TimingRevision`** — already true in practice; now normative, because the pull's adoption rule (§2.6) compares revisions.

### 2.4 C05-2.4 — The pull surface

```cpp
// PROPOSED — NOT FROZEN. Implemented by each producer (its combat/telegraph component).
class ITDDTelegraphSource
{
public:
    // Live read of one instance the caller can name. Returns false if the instance is
    // not open, was never opened by this producer, or this producer is shutting down.
    virtual bool TryGetOpenTelegraph(FGuid AttackInstanceId, FTDDTelegraphSnapshot& Out) const = 0;

    // Instances this producer currently holds open. Per-producer, bounded by that
    // producer's own concurrency (a boss with two attacks returns two ids).
    // This is NOT global enumeration and must not be aggregated into one.
    virtual void GetOpenTelegraphIds(TArray<FGuid>& Out) const = 0;
};
```

**`GetOpenTelegraphIds` exists for the multi-instance producer, not for enumeration.** `A1-R4` §7.2's "one actor may hold several open instances" is the case it serves: a consumer that knows the actor and must ask about all of that actor's open attacks. It is per producer, it is small, and it is not a world query.

### 2.5 C05-2.5 — Resolution: how a consumer holding only an id reaches the producer

> **DN-1 (the directory).** The contract layer exposes a resolution function that maps an `AttackInstanceId` to the producer that opened it. The directory stores, per instance: the id, `SourceEntityId`, and a **weak liveness handle** to the producer. **It stores no timing block, no phase and no revision.** Producers register on `Opened` and deregister on `Closed`; the directory also drops entries at world teardown and answers `false` for a producer whose liveness handle has expired. Its private weak handles are never dereferenced to obtain timing — they are used only to answer "is this producer still alive". The "no actor pointers" rule applies to the published value structs, not to this private liveness record.

**This is the answer to A2's C13, and it is deliberately not a custodian.** A directory that stores an association is not a store that holds state: a pull *through* it reads the producer, never a copy. The distinction is testable (§9, TN-R-01) and it is the reason C1's gate does not apply: nothing authoritative is retained.

**If a consumer already holds a producer reference** — the player's pawn, an actor it is iterating, its own AI's target — it calls `ITDDTelegraphSource` directly and the directory is not involved. The directory exists only for consumers that hold ids without objects.

**The directory is a contract-layer obligation, and it may be satisfied by any implementation**, including a small one inside the Agent 1 world-scoped boundary. It requires no new class, no new subsystem, and no capability that a world-scoped object does not already have.

### 2.6 C05-2.6 — Adoption, entry and revision rules (messages and pulls alike)

> **AD-1 (adoption).** A consumer adopts a snapshot only if its `TimingRevision` is **strictly greater** than the revision it holds for that instance. An equal or lower revision is discarded without state change. The rule is identical for messages and pulls, which is what makes a message/pull race have one correct answer regardless of arrival order.

> **AD-2 (gap detection).** If an incoming revision is **greater than held + 1**, the consumer records a **revision gap** for that instance and keeps a `bRevisionGapObserved` flag set until the instance closes. A gap is never interpolated, never extrapolation-filled, and never treated as a continuous interval.

> **EN-1 (entry baseline).** The first observation of an instance by a consumer — whether an `Opened` message or a pull — **establishes the baseline**: the consumer records the current phase as already held and **fires no entry hook** for it. Entry fires only for phase transitions observed **after** the baseline.

> **EN-2 (at most once).** After the baseline, a phase transition is observable **at most once** per consumer per `(AttackInstanceId, phase)`. A `Retimed` never re-fires entry: it changes timing, not phase identity. A duplicate `PhaseChanged` for the phase already held fires nothing.

> **RS-1 (recovery is current-state only).** A pull recovers the **current** block and phase of a known instance. It never reconstructs an intermediate revision, and no consumer may treat a post-gap block as evidence that no retime occurred. The `bRevisionGapObserved` flag is the record that one did.

> **RS-2 (no revision history).** No component retains more than one block per instance. Every revision is **emitted** by the producer and **none is retained** after the next arrives. This is a stated limit of the mechanism, not a gap in it.

### 2.7 C05-2.7 — Removal

> **RM-1.** An instance ceases to exist on `Closed`, on producer invalidation, on producer unload or stream-out, on producer death-cancel, and on world teardown. Producer invalidation and world teardown are **not** events: they are the disappearance of the producer, and they are observed as a pull returning `false` and a directory entry that no longer resolves. **Removal emits no synthesised message**; the message stream belongs to the producer.

> **RM-2 (consumer duty).** A consumer that holds state for an instance and receives `false` from a pull, or fails to resolve its id, **must** treat the instance as closed, release its block, fire no further entry hook for it, and raise **no** error. "Not found" is closure, not failure (fixes A2's M4 and adopts their C14).

### 2.8 C05-2.8 — What this contract explicitly does not do

- It does not retain another producer's timing state (no custodian, no store, no snapshot cache).
- It does not provide global enumeration (X-1, §1.4).
- It does not arbitrate, decide parry or block, or apply damage (§6).
- It does not define the clock's ownership (TD-06) or the contract layer's home (TD-12).
- It does not select a MEAD, freeze a name, register a tag or issue an erratum.

---

## 3. Revised producer obligations

Every obligation has an identifier, a normative requirement, its inputs and outputs, its failure and invalidation behaviour, its ordering requirement where one applies, and at least one acceptance test. **All tests are `PROPOSED / NOT RUN`.** The test identifiers refer to §9.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test |
|---|---|---|---|---|---|
| **TN-P-01** | Publish `Opened` before the first frame in which the wind-up phase is observable to a stream consumer. | authored window → `Opened` | A missed `Opened` for a pull consumer is not an error; the pull establishes the baseline (EN-1). For a stream consumer it is a contract violation. | `Opened` precedes every other message for that instance | T-C05-07 |
| **TN-P-02** | `AttackInstanceId` is unique per open instance and never reused, in this world or any other. | allocation → `FGuid` | A directory or consumer that sees a reused id must treat it as a new instance; the producer is in violation and raises a diagnostic in Test/Development builds. | n/a | T-C05-26 |
| **TN-P-03** | Emit **exactly one** `Closed` per instance, carrying an `ETDDTelegraphCloseReason`; emit no message of any kind for that instance afterwards. | close event → `Closed` | A second close is rejected by consumers as a duplicate and raises a producer diagnostic; a post-close retime is rejected and diagnosed. | `Closed` after any other message for that instance | T-C05-21 |
| **TN-P-04** | Every cancellation path closes: ability cancel, montage abort, interruption, forced transition, requirement change, the producer's own death. | cancel source → `Closed(Cancelled/Interrupted/SourceDied)` | An unclosed cancelled instance remains pullable and is a contract violation; the consumer cannot detect it, which is why this obligation is normative rather than advisory. | same frame as the cancel | T-C05-22 |
| **TN-P-05** | Invalidate open instances in the teardown path, before the producer stops being valid. | `EndPlay` → deregistration and `Closed(ProducerInvalidated)` | Best effort by construction; the pull's `false` and the directory's liveness answer are the fail-safe (TN-R-02), not a substitute. | before the actor's removal from the world | T-C05-23 |
| **TN-P-06** | Stream-out invalidates only that producer's instances; it never requires or implies world teardown. | unload → deregistration of that producer's ids only | Other producers' instances are untouched; world teardown removes everything because the world-scoped owner is destroyed. | n/a | T-C05-24 |
| **TN-P-07** | `TimingRevision` strictly increases per instance; two messages never carry the same revision with different content. | retime → `TimingRevision + 1` | An equal-revision-different-content message is rejected with a diagnostic and never overwrites a held block. | monotone per instance | T-C05-16 |
| **TN-P-08** | One `Retimed` per `CustomDilation` change, published in the frame the change is made, and reflected in the producer's own live state **no later than** that same frame. **Never batch, coalesce, throttle or defer.** | dilation change → `Retimed` + live-state update | A batched retime is a contract violation. `UTDDHitStopSubsystem` boundaries are the dominant source and are explicitly not exempt. | publish and live-state update in the same frame | T-C05-17, T-C05-18, T-C05-19, T-C05-41 |
| **TN-P-09** | Publish no message for an instance that is closed or was never opened. | stray publish → rejected | Consumers reject it with a diagnostic; the directory is not consulted and no entry is created. | n/a | T-C05-27 |
| **TN-P-10** | All axis values come from the shared axis defined in `A1-R3` §3.3(a); never a wall-clock, frame count or another entity's local time. | engine time → axis value | Any other domain is a contract violation and is detected by a fixture that supplies a wall-clock stamp. | n/a | T-C05-15 |
| **TN-P-11** | `TryGetOpenTelegraph` answers from the producer's live state at call time — never from a cached copy, and never from a value older than the producer's last completed update. | instance id → snapshot or `false` | Returning a stale copy is a contract violation; returning `false` for an open instance is a contract violation except during teardown (TN-P-05). | as of the producer's last completed update before the call | T-C05-06, T-C05-40 |
| **TN-P-12** | No frame deltas, random seeds or tick-order dependence in any published or pulled value; identical inputs produce identical sequences in a deterministic fixture. | deterministic inputs → identical outputs | Non-determinism makes every suite in §9 flaky and is treated as a producer defect. | n/a | T-C05-01 |

**Two producer-side notes.**

1. **P3's reason enumeration now exists** (`ETDDTelegraphCloseReason`, §2.2), which is A2's N3. `Natural` is the only reason a consumer may treat as "the attack finished"; every other reason means the window ended early.
2. **`TN-P-08` is the clause A2 §7.2 found missing everywhere** — "coalescing is named as forbidden in the commentary and never forbidden in a clause". It is now an obligation with four tests, including one that fails an implementation that coalesces.

---

## 4. Revised consumer and interface obligations

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test |
|---|---|---|---|---|---|
| **TN-C-01** | Adopt a snapshot only if its `TimingRevision` is strictly greater than the held revision; discard equal or lower, silently, for both messages and pulls. | snapshot, held revision → adopt or discard | A pull older than the held block is discarded, so a pull can never move a consumer backwards. | commutative — outcome independent of arrival order | T-C05-02, T-C05-03 |
| **TN-C-02** | The first observation of an instance establishes the baseline: record the phase as already held and fire **no** entry hook for it. | first observation → baseline record | A consumer that fires entry on its baseline double-fires for every subscribe; the test in T-C05-08 fails it. | baseline before any entry evaluation | T-C05-08, T-C05-09 |
| **TN-C-03** | After the baseline, fire entry at most once per `(AttackInstanceId, phase)`; a `Retimed` never re-fires entry; a duplicate `PhaseChanged` fires nothing. | phase transition → at most one entry | A second entry for the same phase is a consumer defect and is detectable by counting. | per consumer, per phase | T-C05-10, T-C05-11 |
| **TN-C-04** | On `incoming revision > held + 1`, record a revision gap and set `bRevisionGapObserved` until the instance closes. Never interpolate, never extrapolate, never assume the interval was continuous. | gap → flag | Clearing the flag before the instance closes is a contract violation; the flag is the record that the timeline is not continuous. | on adoption of the post-gap block | T-C05-12, T-C05-13 |
| **TN-C-05** | After a gap, recover with **one** pull of the current block for the known instance; if the pull is unavailable or not newer, report the timing as unknown and raise a diagnostic rather than guessing. | instance id → current block or unknown | "Unknown" is a legitimate terminal state for that instance until it closes; guessing is not. | once per gap, not once per frame | T-C05-14, T-C05-19 |
| **TN-C-06** | A pull returning `false`, or an id that no longer resolves, means **closed**: release the block, fire no further entry, raise no error. | false or unresolvable → closure | Treating "not found" as an error is a consumer defect; a consumer that keeps defensive state up after closure is a gameplay bug. | immediate on observation | T-C05-25 |
| **TN-C-07** | Evaluate the `Dead > Cinematic > Staggered` precedence in priority order over the carriers defined in §6.3, never by comparing carriers against each other. | published state → one effective value | Comparing an enum to a tag is a contract violation; so is reading `Status.Cinematic` when it is not a control-state projection (§6.4). | priority order, first match wins | T-C05-35 … T-C05-39 |
| **TN-C-08** | Never treat a pull as revision history. A post-gap block is the **current** state, not a replacement for the revisions that were missed. | pull result → current value only | A consumer that assumes it recovered every revision makes its telemetry and its AI timings silently wrong; the gap flag is what prevents it. | n/a | T-C05-20, T-C05-19 |

### 4.1 Read-surface obligations (the pull, the per-producer id list and the directory)

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test |
|---|---|---|---|---|---|
| **TN-R-01** | The directory of `C05-2.5` stores, per instance, exactly: `AttackInstanceId`, `SourceEntityId` and one weak liveness handle. **It stores no timing block, no phase and no revision**, and never serves timing through the handle. | `Opened`/`Closed` → association record | A record carrying timing is a contract violation detectable by structure (T-C05-28). An expired handle resolves `false` and the record is dropped; world teardown drops everything. | registration completes before any pull by id can succeed for that instance | T-C05-28, T-C05-29 |
| **TN-R-02** | `TryGetOpenTelegraph` returns `false` for a closed instance, an instance this producer never opened, and an instance whose producer is tearing down. It never returns a partial or stale-filled record. | id → snapshot or `false` | `false` is never an error (RM-2). A `true` for a closed instance is a contract violation. | n/a | T-C05-04, T-C05-05 |
| **TN-R-03** | `GetOpenTelegraphIds` reports only the calling producer's own open instances. **It is not a world query, may not be aggregated into one in this version, and is not the X-1 extension.** | producer → its ids | An implementation that answers with other producers' ids is a contract violation and would silently re-create custody. | n/a | T-C05-30 |
| **TN-R-04** | A pull returns a value copy, is callable from any consumer phase without re-entrancy, reflects the producer's last completed update, and never mutates a collection the caller can see. | call → copy | Re-entrancy or a returned reference into producer storage is a contract violation. | reflects the producer's last completed update at call time | T-C05-31 |

### 4.2 Arbitration obligations

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test |
|---|---|---|---|---|---|
| **TN-A-01** | Parry is `C05-6.1`: a same-frame phase-overlap test. The attacker's phase is read **on the hit-resolution path from the component that owns the attack instance**, and never from `ITDDTelegraphSource`, the directory, or a published timing block. No timestamp subtraction, no cross-entity clock comparison, no tolerance for a check that passes one frame late. | hit data, defender defence state, attacker live phase → parry outcome | Evaluating parry from any C-05 value is a contract violation. A wrong timing block must not be able to change the outcome. | evaluated in the frame the hit is resolved | T-C05-32, T-C05-33 |
| **TN-A-02** | No arbitration decision may depend on any value produced by the C-05 contract. The arbiter's inputs are the hit data, the defender's defence state and the attacker's live phase — none obtained through the pull surface, the directory or a published block. | as above → outcome plus diagnostic | Any observed read of the telegraph surface on the arbitration path is a contract violation, detectable with a spy. | n/a | T-C05-34 |

**The point of TN-C-02 and TN-C-03 together** is that they close A2's §8.1: a consumer that has never observed a phase never fires entry for it (baseline), and a consumer that has observed it fires exactly once. Neither rule needs to know whether the *system* entered the phase — which was the ambiguity that made the previous C5/P11 pair non-implementable.

---

## 5. Lifecycle, invalidation and hitstop semantics

### 5.1 How every retime revision is represented

**One revision number per instance, one message per change, no history.** `TimingRevision` starts at 1 on `Opened`, increments by exactly one per `CustomDilation` change (`TN-P-07`), and every increment is published as a `Retimed` in the frame of the change (`TN-P-08`). The producer's live state carries the same revision the message carries, so a pull and a message can be compared by arithmetic alone.

**What this does not claim:** that every revision is *preserved*. It is not (§2.6 RS-2). Every revision is **emitted**; only the latest is **retained**, and retaining one block per instance is a deliberate limit of the model, not an omission.

### 5.2 How a consumer detects a stale or a missing revision

Two arithmetic tests, no clocks and no heuristics:

| Condition | Meaning | Required response |
|---|---|---|
| `incoming == held` | duplicate (a message repeated, or a pull of what is already held) | discard silently (`TN-C-01`) |
| `incoming < held` | stale, typically a pull taken before a later message | discard silently (`TN-C-01`) |
| `incoming == held + 1` | continuous | adopt, no gap |
| `incoming > held + 1` | **a revision was missed** | adopt the block **and** set `bRevisionGapObserved` (`TN-C-04`) |
| pull returns `false` | closed, or producer gone | treat as closure (`TN-C-06`) |

### 5.3 How a consumer recovers after missing an intermediate revision

One pull, then an explicit statement of ignorance:

1. Ask the producer for the current block (`TN-C-05`). The answer is the **current** state, which may be two or more revisions ahead of what was held.
2. Adopt it under `TN-C-01`, and set `bRevisionGapObserved` under `TN-C-04`.
3. Treat the interval between the last continuously held revision and the recovered one as **not recovered**: no interpolation of phase boundaries, no assumption that the missed interval had constant dilation, no synthesised entry for any phase that began and ended inside it.
4. Keep the flag until the instance closes, so every downstream use of that instance's timing knows the estimate is discontinuous.

**Measured against the original defect:** the `A1-R3` §7.6 case — a consumer closing at axis 2.0 a window that runs to 16.4 — is now recoverable in one call. What is *not* recoverable is the intermediate revision itself, and the contract says so instead of implying otherwise.

### 5.4 Individual delivery versus an authoritative current-state query

**Both are required, and neither substitutes for the other.**

| Channel | Purpose | Why the other cannot replace it |
|---|---|---|
| Message stream (`Opened`, `PhaseChanged`, `Retimed`, `Closed`) | **transitions** — the events a consumer reacts to, in order, exactly once | A pull cannot tell a consumer *when* a phase began, only what the phase is now; reaction logic keyed on transitions would fire late or never |
| Pull (`TryGetOpenTelegraph`) | **current values after loss** — gap recovery, resubscribe, and any consumer that started late | A message stream has no memory; a consumer that missed a message cannot ask the stream for it |

**The ordering requirement between them is not a frame point, and that is the substantive change from `A1-R4`/my previous response.** With no stored copy, there is no cross-object ordering to define: the answer to a pull *is* the producer's state at call time. What remains is a **producer-side coherence obligation** (`TN-P-08`): the live state must reflect a rate change no later than the frame in which the `Retimed` is published, so that a pull in that frame cannot return a pre-change block while the message says post-change. Combined with `TN-C-01`, a consumer cannot mix the two channels incoherently: whichever it holds, only a strictly greater revision replaces it.

**This is the resolution of A2's §8.5, and I state its shape plainly:** their finding was that I required a named ordering point and never named one. The successor does not name one, because the model has no stored copy for the point to order. The two obligations that replace it are testable without any engine tick-group name: `TN-P-08` (same-frame coherence) and `TN-C-01` (symmetric adoption). **If the conditional custody extension (X-1) is ever adopted, A2's §9.5 named-point wording attaches to it unchanged**, and I accept it there.

### 5.5 Correctness across multiple hitstop boundaries

`UTDDHitStopSubsystem` (MEAD-C line 312, Agent 1) applies a scaled dilation to the pair of actors (line 496). Each boundary changes `CustomDilation` on up to two actors, so a single exchange can produce a burst:

| Situation | Required behaviour |
|---|---|
| One hitstop boundary with one open telegraph | exactly one `Retimed`, revision +1, live state updated in the same frame |
| Two boundaries in one frame on one producer with two open instances | **four** `Retimed` messages — two per instance — each revision monotone, none batched (`T-C05-17`, `T-C05-18`) |
| A consumer that misses the first of the two | adopts the second block, sets the gap flag, and **reports the first as unrecovered** rather than as a continuous interval (`T-C05-19`) |
| A consumer that pulls instead of receiving either | receives the current block with the latest revision; if it held a revision two or more behind, the gap flag is set by `TN-C-04` |
| Victim dies while the producer is alive | the instance is **unaffected** — the producer closes it normally or cancels it under `TN-P-04`; no telegraph state changes because a victim died (`T-C05-22`) |

The burst case is why `TN-P-08` forbids coalescing **as a clause** and not as a comment: a design that batches retimes per frame is indistinguishable, from the consumer's side, from a producer that lost one.

### 5.6 Why no consumer can silently mistake a missed revision for a valid continuous timeline

Three mechanisms, each of which is independently sufficient to prevent silence and which together prevent it even for a careless consumer:

1. **The revision arithmetic is unambiguous.** Revisions are strictly monotone per instance, so `incoming > held + 1` is a fact the consumer can compute from values it already holds — no clock, no timestamp comparison, no cross-entity reading.
2. **The gap flag is a contract obligation, not a courtesy.** `TN-C-04` requires the record and forbids clearing it before closure, so a consumer that resolves a gap and then proceeds as if nothing happened is in violation of an obligation with a test (`T-C05-12`, `T-C05-13`).
3. **The pull participates in the same adoption rule.** A post-gap block cannot masquerade as continuity because `TN-C-01` makes adoption a revision comparison, and `TN-C-08` forbids treating the recovered block as a substitute for the revisions that were missed.

**And the limit is stated where it belongs:** the model does **not** preserve every revision, does **not** reconstruct missed intervals, and does **not** offer a revision log. A consumer that needs to know *what happened* during a gap cannot learn it from this contract; a consumer that needs to know *what is true now* can.

---

## 6. Combat-arbitration independence

### 6.1 The parry rule, restated inside this contract

> **C05-6.1 — parry rule (normative; first stated at `A1-R3` §3.4, repeated here so that this contract does not depend on another document's section numbering).**
> A parry succeeds **only when, in the frame in which the hit is resolved**, both hold: (a) the defender's parry window is active, and (b) the attacker's telegraph phase state for that `AttackInstanceId` is `Active`.
> It is a **same-frame phase-overlap test against live state**. No implementation may evaluate parry by subtracting timestamps, by comparing clock readings from two entities, by interpolating from a stale endpoint, or by tolerating a check that passes one frame late.
> Timestamps and axis endpoints exist for **scheduling, diagnostics and display only**. They are not the parry test.

**Where the arbiter gets the attacker's phase:** from the attacker's own combat state on the hit-resolution path — the component that owns the attack instance and resolves the hit — and **never** from the pull surface, the directory, or any snapshot. That is `TN-A-01`.

**This is the structural repair of A2's §2.4**, which showed my previous C9 was enforceable only under MEAD-C: if MEAD-A is canonical, `UTDDHitArbiter` is both the parry decision path and (under my previous text) the custody home, so "this class must not read its own member" was a code-review convention rather than a contract. Under the successor:

- the parry path's phase source is **defined by role, not by class** — "the component that owns the attack instance, on the hit-resolution path";
- the directory holds **no timing, no phase and no revision** (`TN-R-01`), so there is nothing in it that the parry path could usefully read;
- therefore even if one class implements both the arbiter role and the directory, **the parry rule is not violated**, because the data it is forbidden to use does not exist in the directory.

`C9` therefore survives under **all three** candidate MEADs, which the previous formulation did not.

### 6.2 The severity bound, stated as a property rather than a hope

> **TN-A-02.** No arbitration decision may depend on any value produced by the telegraph contract. The arbiter's inputs are the hit data, the defender's defence state and the attacker's live phase; none of them is obtained through `ITDDTelegraphSource`, the directory, or a published timing block.

**Consequence, which is what the whole bound is for:** a wrong timing block produces a wrong display, a wrong schedule or a wrong AI reaction — never a wrong parry. Test `T-C05-32` asserts it with a spy on the telegraph surface and a deliberately corrupted fixture.

### 6.3 The precedence evaluation rule (A2R-35, repaired)

> **C05-6.3 — `Dead > Cinematic > Staggered`, three carriers, priority order (`PROPOSED — NOT FROZEN`).**
>
> | Priority | Member | Carrier | Provenance |
> |---|---|---|---|
> | 1 | `Dead` | `bAlive == false` **or** `CombatState == ETDDCombatState::Dead` | combat state enum, published by C-02 |
> | 2 | `Cinematic` | `ControlState == Cinematic` if `ControlState` is granted; otherwise `Status.Cinematic` | **control-state projection** — explicitly **not** derived from `ETDDCombatState` |
> | 3 | `Staggered` | `Status.Staggered` **or** `CombatState == ETDDCombatState::Staggered` | combat-state projection |
>
> Evaluate in priority order, first match wins; stop at the first match. **Never compare two carriers against each other.**
>
> **Why the order makes comparison unnecessary:** the ordering is total, so a consumer needs one predicate per rank and never a comparison across representations. `A1-R4` §9.2 is correct that `Cinematic` lives on the control state machine and not in `ETDDCombatState`; **that is exactly why the rule tests carriers in sequence rather than pretending they share a domain.**

**Provenance correction, and the C-04 consequence.** `A1-R4` §9.2 assigns `Status.Cinematic` to the control state machine and says it "derive[s] from the control state machine directly and never from `ETDDCombatState`". The previous response's rule read `Status.Cinematic` without saying so, which is A2's §8.6 and is correct. `C05-6.3` states the provenance. **Because this touches C-04, it is proposed as a C-04 amendment (`C-04-4`) for the next C-04 version and is not frozen, not signed, and not part of this document's review request.** C-04's own conditions (the registry's `Status.Dead` decision) are unaffected.

---

## 7. The MEAD-neutral ownership boundary

### 7.1 The rule

> **C05-7.1.** This contract names **no module** and **no class**. Its value types, its message structs and its read interface are **contract-layer types of the canonical architecture**; its owner is whoever the TD designates when TD-12 settles which candidate is canonical. Its **implementation** — the producer-side pull, the per-producer id list and the directory — is Agent 1's in every candidate, because it lives with the producers and requires no capability beyond a world-scoped object.

### 7.2 Why the previous version failed this test, and how this one passes it

A2 §2.1 showed that my previous condition C2 — "the shared surface is Core-owned, Agent 3's types" — existed in exactly one of three candidates. Their finding is exact:

| Candidate | Contract-layer home | Consequence for the previous C2 |
|---|---|---|
| **MEAD-C** | `TDDCore` — line 227 "`TDDCore` is a leaf"; line 228 "Cross-agent contracts live in `TDDCore` as interfaces/structs" | C2 held |
| **MEAD-A** | **No `TDDCore` module** (`grep -c TDDCore` = 0). Nearest: `TDDRuntime/Framework/` — "Shared: interfaces, canon validation, telemetry" — with **no owner assigned** | C2 had no referent |
| **MEAD-B** | **No `TDDCore` module** (`grep` = 0) | C2 had no referent |

**How C05-7.1 passes it:** it does not say where the types live, it says the types belong to the contract layer **of whichever document is canonical** and that the owner is **designated**, not assumed. It also imposes the one constraint that is true in all three: the interface must be implementable in a **single-module layout** (MEAD-A has one `TDDRuntime` module with folder areas), so no clause may require a separate module, a particular dependency direction, or a class that only one candidate names.

**And it passes the state-placement test for the same reason.** The previous version was MEAD-neutral about the *state* and MEAD-specific about the *surface*; A2 called that out. Under the successor there is no state to place — the producer holds it — so both halves are neutral.

### 7.3 What is deferred to TD-12, and what is not

| Deferred to TD-12 | Not deferred |
|---|---|
| The contract layer's name and owner (C05-7.1) | The producer's ownership of its own timing (true in every candidate) |
| Whether the canonical document names a class for the directory | That the directory stores no timing (`TN-R-01`) |
| The concrete class for the parry path's live-phase read | That the parry path reads live phase by role and never through the telegraph surface (`TN-A-01`) |

**Nothing in this contract becomes unimplementable if TD-12 chooses MEAD-A or MEAD-B.** Under MEAD-A the types land wherever that document's framework area is and someone must be assigned; that is a TD action, not a contract change. **This is the property the previous version lacked and the one I would ask Agent 3 to check first in their assessment (§13).**

---

## 8. Clause-by-clause response to Agent 2's six blocking findings

Each finding: the original problem in A2's terms, what the successor does, which clauses carry the fix, which test discharges it, and the status.

### 8.1 F1 — C5 and P11 collide: a late subscriber can never observe the phase it joined in

| | |
|---|---|
| **A2's problem** | P11 said a snapshot "never reports a phase that was never announced"; C5 suppressed entry for a phase "already held" — but a late subscriber holds no phase, so the text left two conforming behaviours (silence or double-fire) on the case that motivated custody in the first place |
| **Root cause** | "Previously held" was defined relative to the *system*, not to the *consumer*; and the model had a snapshot that carried a phase with no history |
| **Resolution** | The ambiguity is removed rather than decided: **the first observation establishes the baseline and fires no entry** (`EN-1`), and **entry is at most once per `(instance, phase)` after the baseline** (`EN-2`). A pull-derived first observation and an `Opened`-derived first observation are the same case. P11's claim that a snapshot never reports an unannounced phase is **withdrawn as unsatisfiable** and replaced by `TN-P-01`, which is a statement about the producer's stream only |
| **Affected clauses** | `C05-2.6` (EN-1, EN-2), `TN-P-01`, `TN-C-02`, `TN-C-03` |
| **Test obligation** | `T-C05-08` (late pull baseline fires no entry), `T-C05-09` (Opened baseline fires no entry for its own phase), `T-C05-10` (one entry per transition), `T-C05-11` (retime re-fires nothing) |
| **Status** | **RESOLVED** |

### 8.2 F2 — "the only place state can be found" contradicts C9 and cannot be tested

| | |
|---|---|
| **A2's problem** | (a) If the custody store is the only place current state can be found, C9's parry path is forbidden to read the only place it exists; (b) C9 and seven other references cited "§3.4", and **`A1-R4` has no §3.4** — the normative parry text is at `A1-R3` §3.4 |
| **Resolution** | (a) The phrase is **withdrawn**. There is exactly one live source — the producing object — and one reporting path to it. The parry path reads live phase **on the hit-resolution path from the attacker's combat state**, by role, and never through `ITDDTelegraphSource`, the directory or a published block (`TN-A-01`, `TN-A-02`). With no second copy anywhere, "the only place it can be found" no longer describes anything; and because the directory holds no timing (`TN-R-01`), a class that implements both roles in one candidate cannot violate the rule by construction |
| | (b) The **normative parry rule is restated inside this contract** as `C05-6.1`, attributed to `A1-R3` §3.4 and self-contained. Every reference in this document resolves inside this document. The successor does not depend on another document's section numbering, and the dangling reference cannot recur |
| **Affected clauses** | `C05-6.1`, `C05-2.5` (DN-1), `TN-A-01`, `TN-A-02`, `TN-R-01`, `TN-C-07` |
| **Test obligation** | `T-C05-32` (parry outcome unchanged with a corrupted pull fixture and a spy showing zero surface reads), `T-C05-33` (parry is same-frame overlap, not timestamp subtraction), `T-C05-34` (arbiter inputs contain no telegraph-surface value) |
| **Status** | **RESOLVED** |

### 8.3 F3 — silent eviction and the circular argument for central enumeration

| | |
|---|---|
| **A2's problem** | I argued that because eviction is silent, the aggregate query is the only way to learn that an entry vanished — and then used that to argue for enumeration, whose necessity was exactly what was in doubt. Silence was a cost of custody being presented as a requirement for custody |
| **Resolution** | The circle is cut by removing the mechanism that created it. **There is no retained entry to evict**: instance state dies with its producer, a pull returns `false`, and a directory entry stops resolving (`RM-1`). Removal detection is therefore a **per-instance** fact, requires no aggregate, and `C14`/`TN-C-06` makes the consumer's response normative. The sentence "the aggregate query is the only way a consumer can learn that an entry vanished" is **withdrawn**, and A2's correction — that per-instance `false` is the removal signal — is adopted. Enumeration is retained only as X-1 with the evidence bar in §1.4 |
| **Affected clauses** | `C05-2.7` (RM-1, RM-2), `TN-C-06`, `TN-R-02`, §1.4 |
| **Test obligation** | `T-C05-25` (removal is closure: released, no entry, no error, no synthesised message), `T-C05-04`/`T-C05-05` (pull `false` for closed and for unknown instances) |
| **Status** | **RESOLVED** |

### 8.4 F4 — C6's validity check needs a "producer handle" the same clause forbids

| | |
|---|---|
| **A2's problem** | Query-time validity was the non-optional fail-safe, but the clause forbade storing an actor pointer and supplied no alternative, so the fail-safe had no means |
| **Resolution** | Two changes. First, **the scope of the prohibition is stated**: the "no actor pointers" rule applies to **published value structs**, not to a private liveness record. Second, **the only place a liveness answer is needed now is the directory**, which stores a weak handle per `AttackInstanceId` **for liveness only**, and never dereferences it to obtain timing (`DN-1`, `TN-R-01`). In the pull path the question does not arise: a dead producer cannot answer a call, and the caller's own `false` is the answer (`TN-R-02`) |
| **Affected clauses** | `C05-2.5` (DN-1), `TN-R-01`, `TN-R-02`, `TN-P-05` |
| **Test obligation** | `T-C05-28` (a directory record contains no timing, phase or revision field — asserted by structure), `T-C05-29` (expired liveness resolves `false`, and no timing is served through the handle), `T-C05-23` (destroyed producer: pull `false` in the same frame, before any sweep) |
| **Status** | **RESOLVED** |

### 8.5 F5 — C8 and §7.2 require a *named* ordering point and never name one

| | |
|---|---|
| **A2's problem** | I required a named in-frame ordering point so that "a same-frame query legitimately returns the previous frame's block" would become a defect; I then named no tick group, phase or ordinal, so a same-frame query still legitimately returned the previous block and the condition changed nothing. It was also the one blocking condition with no test |
| **Resolution** | **Resolved by removing the object of the requirement, and stating that plainly.** With no stored copy there is no "previous frame's block" to return: a pull is evaluated against the producer's state at call time. Two testable obligations replace the condition — `TN-P-08` (the producer's live state reflects a rate change **no later than** the frame in which the corresponding `Retimed` is published) and `TN-C-01` (a pull participates in strict-greater adoption, so a consumer holding a newer block discards the older pull). **No engine tick-group name is invented**, and none is needed; had I named one it would have been engine-version and module-layout dependent, which is the one thing this document cannot fix |
| **Affected clauses** | `TN-P-08`, `TN-C-01`, §5.4 |
| **Test obligation** | `T-C05-40` (pull in the consumer phase returns the block matching the producer's same-frame message), `T-C05-41` (pull older than the held revision is discarded), `T-C05-17`/`T-C05-18` (no batching across hitstop boundaries) |
| **Status** | **RESOLVED** — by model change. Under the conditional X-1 custody extension the requirement returns, and **A2 §9.5's wording attaches to it unchanged**; I accept it there |

### 8.6 F6 — A2R-35's rule depends on `Status.Cinematic`, whose provenance the same series denies

| | |
|---|---|
| **A2's problem** | The precedence rule read `Status.Cinematic` while `A1-R4` §9.2 says `Cinematic` derives from the control state machine and never from `ETDDCombatState` — so the rule consumed a tag whose authority chain excluded it. And the "no comparison is needed" justification mis-stated its own mechanism: it is the *difference* of carriers, not their sameness, that makes comparison unnecessary |
| **Resolution** | `C05-6.3` states all three carriers explicitly with their provenance, tests them in priority order, and states the real justification — the order is total, so no comparison across representations is required. `Status.Cinematic` is defined as a **control-state projection** published with the same authority chain as `ControlState`, and `ControlState` is used directly where it is granted. The rule is therefore self-consistent whether or not `ControlState` is granted, and whether or not `Status.Dead` is |
| **Affected clauses** | `C05-6.3`, `TN-C-07`; proposed C-04 amendment `C-04-4` |
| **Test obligation** | `T-C05-35` … `T-C05-39`, including one case that fails a consumer reading `Status.Cinematic` as if it were a combat-state derivative |
| **Status** | **RESOLVED within C-05.** The parallel C-04 amendment is **proposed, not agreed**, and C-04 remains unsigned on its own outstanding conditions |

### 8.7 A2's non-blocking findings, conditions and missing obligations

| A2 item | Disposition in this successor |
|---|---|
| **C2R-1** C2 is MEAD-C-only | **FIXED** — §7, `C05-7.1` |
| **C2R-2** C9 unenforceable under MEAD-A | **FIXED** — §6.1: role-defined phase source plus a directory that holds nothing worth reading |
| **C2R-3** producer resolution for a per-instance surface (their C13) | **FIXED** — `DN-1` (`C05-2.5`), with liveness-only storage and no timing |
| **C2R-4** `ITDDCombatant` is actor-scoped, so it cannot disambiguate two instances | **FIXED** — the pull is keyed by `AttackInstanceId`; `GetOpenTelegraphIds` covers the multi-instance producer |
| **C2R-5** C5 collides with P11 | **FIXED** — §8.1 (EN-1/EN-2) |
| **C2R-6** validity needs a handle the clause forbids | **FIXED** — §8.4 |
| **C2R-7** C8 names no ordering point | **FIXED by removal** — §8.5; retained for X-1 |
| **N1** no producer-resolution rule | **FIXED** — `DN-1` |
| **N2** victim-died-while-producer-alive missing from the lifetime table | **FIXED** — stated as its own row in §5.5: the instance is unaffected; the producer closes it normally or cancels it under `TN-P-04` |
| **N3** `Closed` requires "a reason value"; no enumeration | **FIXED** — `ETDDTelegraphCloseReason` (§2.2) |
| **N4** the C1 gate cannot be evaluated (who establishes R2, against what evidence) | **FIXED** — §1.4 names the decider (TD) and the three admissible evidence forms, adopted from A2 §12.2 |
| **N5** executed-check count presented near coverage claims | **ADDRESSED** — §9.3 separates document-validation checks from Unreal acceptance tests in two labelled tables |
| **N6** the hitstop-burst conflict is a strength, not a defect | **RECORDED** — §5.5, and it is now a clause (`TN-P-08`) rather than an observation |
| **M1** no custodian obligation for a `Retimed` on an unknown instance | **ADDRESSED** — no custodian exists; `TN-P-09` binds the producer and the directory creates nothing for an unknown id |
| **M2** producer id reuse across worlds is undetectable | **STATED AS A LIMIT** — ids are unique per instance; the directory is world-scoped and dies with the world; cross-world reuse is undetectable and harmless while nothing persists across worlds. If persistence is ever added this reopens (and `A1-R4` §5.8 already warns against it) |
| **M3** a producer whose attack was cancelled without `Closed` survives its own liveness check | **STATED AS A PRODUCER-CONFORMANCE RISK** — the model cannot detect it, because the producer is alive and the instance is real to it; `TN-P-04` is the obligation and `T-C05-22` is the test. It is a conformance failure, not a contract gap, and I would rather say so than invent a heartbeat |
| **M4** no consumer-side rule for a query returning nothing for a held instance | **FIXED** — `RM-2` / `TN-C-06` |
| **T1–T6** six tests A2 proposed | **ALL ADOPTED** — T1→`T-C05-08`, T2→`T-C05-25`, T3→`T-C05-19`, T4→`T-C05-23`, T5→`T-C05-16`, T6→`T-C05-40` |
| A2 §0.3 withdrawal of its own citation finding | **ACKNOWLEDGED**, §0.2 |
| A2 §4.3 "twelve conditions versus one" | **ACCEPTED with one correction** — per-instance recovery needs the query, the resolution rule and a liveness rule: **three** obligations, not one (§0.4) |

---

## 9. Acceptance-test matrix

### 9.1 The suites

**All 42 cases are `PROPOSED / NOT RUN`. None has been executed, no code exists to execute them against, and no Unreal project exists in this workspace.**

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

**9 suites, 42 cases, 0 executed.**

### 9.2 Obligation to test coverage — every obligation, no orphans

| Obligation | Cases | Obligation | Cases |
|---|---|---|---|
| TN-P-01 | T-C05-07 | TN-C-04 | T-C05-12, T-C05-13 |
| TN-P-02 | T-C05-26 | TN-C-05 | T-C05-14, T-C05-19 |
| TN-P-03 | T-C05-21 | TN-C-06 | T-C05-25 |
| TN-P-04 | T-C05-22 | TN-C-07 | T-C05-35 … 39 |
| TN-P-05 | T-C05-23 | TN-C-08 | T-C05-19, T-C05-20 |
| TN-P-06 | T-C05-24 | TN-R-01 | T-C05-28, T-C05-29 |
| TN-P-07 | T-C05-16 | TN-R-02 | T-C05-04, T-C05-05 |
| TN-P-08 | T-C05-17, T-C05-18, T-C05-19, T-C05-40 | TN-R-03 | T-C05-30 |
| TN-P-09 | T-C05-27 | TN-R-04 | T-C05-31 |
| TN-P-10 | T-C05-15 | TN-A-01 | T-C05-32, T-C05-33 |
| TN-P-11 | T-C05-06, T-C05-40, T-C05-42 | TN-A-02 | T-C05-34 |
| TN-P-12 | T-C05-01 | TN-C-01 | T-C05-02, T-C05-03, T-C05-41 |
| — | — | TN-C-02 | T-C05-08, T-C05-09 |
| — | — | TN-C-03 | T-C05-10, T-C05-11 |

**26 obligations, 42 cases, every obligation covered, every case mapped.** A2's six proposed tests are all present: T1 → `T-C05-08`, T2 → `T-C05-25`, T3 → `T-C05-19`, T4 → `T-C05-23`, T5 → `T-C05-16`, T6 → `T-C05-40`.

### 9.3 Document-validation checks — executed, and separate from acceptance tests

These are checks **I ran on this document**, not tests of any contract behaviour. They are listed separately because conflating the two is the failure this series keeps having to correct.

| Check | Method | Result |
|---|---|---|
| DV-1 obligation ids unique, and all 26 appear in the coverage table | extract ids, dedupe, compare sets | **PASS** — 26 declared, 26 unique, 0 duplicate declarations, 0 obligations absent from the coverage table |
| DV-2 every case id used, count equals the stated total | regex over the matrix, arithmetic | **PASS** — 42 distinct cases (range-expanded), expected 42, missing [] |
| DV-3 no bare `§3.4` reference without a document qualifier | line-level rule: every line containing `§3.4` must name a document or be a statement about the defect | **PASS** — 16 occurrences of §3.4 across 10 lines; 0 lines carry neither a document qualifier nor a meta-statement context [] |
| DV-4 no unqualified assertion that a `TDDCore` module exists | every `TDDCore` occurrence inspected in context | **PASS** — 7 lines mention `TDDCore`; 0 assert it without a MEAD qualifier [] |
| DV-5 clause ids unique across `C05-2.x`, `C05-6.x`, `C05-7.x` | extract and dedupe | **PASS** — 11 clause ids defined, 0 defined twice, 0 referenced but undefined [] |
| DV-6 suite count and case sum match the stated totals | count rows, sum the Cases column | **PASS** — 9 suite rows, case sum 42, stated totals 9 and 42 |

### 9.4 What the matrix is not

It is not evidence that any obligation holds, that any suite compiles, or that the contract behaves as written. **Executed contract acceptance tests: 0. Written against Agent 1 code: 0. Engine available: no (ADR-0012).** The six document checks in §9.3 are the only executed evidence in this document.

---

## 10. Remaining blockers and explicit implementation prerequisites

### 10.1 What genuinely prevents implementation

| # | Blocker | Prevents | Owner |
|---|---|---|---|
| **B-1** | **TD-06 — clock ownership and the gameplay axis** | any code that stamps `AxisNow` or computes a span. The arithmetic is settled (`A1-R3` §3.3(a)/(b), corrected in `A1-R4` §2); the **owner and definition of the axis are not** | TD |
| **B-2** | **Parry-authority location** — `A1-R3` §3.4 states the rule, but MEAD-A line 484 assigns Hit/Blocked/Parried to `UTDDHitArbiter` and the TD-09 erratum is not issued | implementing the arbitration path at all, in any candidate | TD (TD-09 erratum) |
| **B-3** | **No engine, compiler, Unreal project or GPU in this workspace** (ADR-0012) | executing any of the 42 cases. Writing them is possible; running them is not | Phase 0 / TD |

### 10.2 What prevents freezing but not designing

| # | Item | Consequence if unresolved |
|---|---|---|
| **B-4** | **TD-12 — canonical MEAD and the contract layer's owner** | the value types and read interface have no designated home and cannot be frozen; **they remain implementable under all three candidates** (§7) |
| **B-5** | **U-07 / enumeration** | nothing in C-05 depends on it; only the conditional extension X-1 does (§1.4) |
| **B-6** | **U-15** damage-request spelling | C-03 only; C-05 names no damage type |
| **B-7** | **U-14** `Status.Dead` grant | C-04 only; `C05-6.3` holds whether or not the tag is granted |
| **B-8** | **TD-13** save inventory | C-07 only |

### 10.3 What is not a blocker, stated to prevent it being cited as one

- **The absence of a custodian.** Per-instance recovery is the working model and it is complete without one (§2.5–§2.7).
- **The absence of a named tick group.** There is no stored copy to order; the two replacement obligations are `TN-P-08` and `TN-C-01` (§5.4).
- **The absence of global enumeration.** No requirement, consumer, failure mode or test establishes it (§1.4, A2 §3.3).
- **The absence of a `TDDCore` module** under MEAD-A or MEAD-B. The contract names no module (§7).

---

## 11. Migration note — what this supersedes

### 11.1 Documents and clauses superseded

| Superseded artefact | Where it was | Status in this successor |
|---|---|---|
| The `UTDDTelegraphBroker` in Core | `A1-R4` §4.1 | **Withdrawn** (withdrawn in the C-05-3 response, now replaced rather than relocated) |
| The relocated world-scoped **custodian** and its twelve conditions C1–C12 | `TDD-A1-C05-3-RESPONSE-001` §1.1, §7.2 | **Replaced.** C1's gate survives as §1.4; C4→`AD-1`; C5→`EN-1`/`EN-2`; C6→`RM-1`/`RM-2` + `TN-R-02`; C9→`C05-6.1`/`TN-A-01`; C11→§3; C12 retained. **C3, C7, C8 and C10 are void** — there is no store to be verbatim about, no snapshot delivery to be non-re-entrant about, no stored copy to order, and no registry to keep separate from the token policy |
| The per-instance query sketch and its comparison table | same document §2.4 | **Promoted** to `C05-2.4`, `C05-2.5`, and completed with the resolution rule it lacked (`DN-1`) |
| The ten required changes to the broker | same document §7.1 | **Superseded by §2.** Items 1–6 and 9–10 survive in altered form as clauses; items 7–8 (non-reentrancy, named ordering point) are void because their objects are gone |
| The five A2 finding responses | same document §8.1–§8.5 | **Superseded by §4 and §6.3** |
| Producer obligations P1–P12 | same document §6.1 | **Renumbered and extended** as `TN-P-01` … `TN-P-12`, each now with inputs, outputs, failure behaviour and a test |
| `A1-R4` §5's amended test suite set | `A1-R4` §13.2 | **Superseded by §9.** One suite is dropped (custody-specific), the rest are retained or renamed |

### 11.2 Statements that must not be cited again

1. "The broker becomes **authoritative for current telegraph state**" (`A1-R4` §4.1). Withdrawn.
2. "The only place the producer's current state can be **found**" (C-05-3 response §7.2). Withdrawn; there is one live source and one reporting path to it.
3. "The aggregate query is the only way a consumer can learn that an entry vanished" (same §6.2). **Withdrawn** — per-instance `false` is the removal signal (A2 §6.3 is right).
4. The twelve-condition custody model as a current statement of C-05. Superseded.
5. Any unqualified reference to `§3.4`. The parry rule is `C05-6.1` here; its origin is **`A1-R3` §3.4**.
6. "Every revision is preserved." It is not, and the contract now says so (`RS-2`).

### 11.3 What is preserved unchanged

- The timing struct and the conversion arithmetic: `A1-R3` §3.2, §3.3(a)/(b), and `A1-R4` §2's derivation (local = axis × rate; axis = local / rate).
- The `RemainingLocalSeconds` lifecycle: `A1-R4` §3 (`R(t) = max(0, R0 − Δaxis × ProducerRate)`).
- The parry rule as text: `A1-R3` §3.4, now embedded as `C05-6.1`.
- The message names and the four-message lifecycle: `A1-R1` §5.2, `A1-R3` §3.2.
- Every prior document in this series, byte-for-byte. **Nothing is rewritten; this successor supersedes by statement, not by edit.**

---

## 12. Publication

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V1.md` — **new file** |
| Version | 1.0 (`A1-C05-S1`) |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `6af9d807f0a43e9155d6b3cafcedf90223d4db24` |
| Blob at that commit | `ac65aaa15322542c4ffd7f07bb5796b153dc1b03` |
| Superseded position | `TDD-A1-C05-3-RESPONSE-001` v1.0 at `22c29da`, blob `a94b49ef…` — **unmodified** |
| Baseline | `A1-R4` v1.3 at `142cabd`, blob `2cc548fa…` — **unmodified** |
| `A1-R1` / `A1-R2` / `A1-R3` | blobs `25ab47c2…` / `5ee2769…` / `109331f3…` — **unmodified** |
| Agent 2's reviews (`4c09980`, `7ea0a85`, `586152b`) | read only, **not modified, not rewritten** |
| Agent 3's recommendation (`58ec7fd`) | read only, **not modified** |
| MEAD-A / MEAD-B / MEAD-C | read only; none moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| Contracts signed | **None.** C-05 remains unsigned by both agents |
| Tags / erratum / freeze / merge / M0 | **None** |
| Code, Core types, project | **None** |
| Tests | 42 cases `PROPOSED / NOT RUN`, 0 executed; 6 document checks executed (§9.3) |

### 12.1 Document history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-17 | Successor to C-05. Custody not adopted; per-instance pull with a liveness-only directory adopted; all six of Agent 2's blocking findings resolved (five by model change, one with a proposed C-04 amendment); 26 obligations with identifiers, I/O, failure behaviour and tests; 9 suites / 42 cases proposed, none run; six document checks executed; MEAD-neutral ownership boundary that holds under all three candidates; hitstop and revision semantics stated including the explicit non-claim that revisions are preserved. |

---

## 13. Handoff

### 13.1 Status of the six blocking findings

| # | Finding | Status |
|---|---|---|
| F1 | C5/P11 collision on late subscribers | **RESOLVED** — EN-1/EN-2 replace both clauses; P11's unannounced-phase claim withdrawn |
| F2 | "Only place it can be found" versus C9, and the dangling `§3.4` | **RESOLVED** — phrase withdrawn; parry rule embedded as `C05-6.1` and cited to `A1-R3` §3.4 |
| F3 | Silent eviction and the circular enumeration argument | **RESOLVED** — no retained entry to evict; removed-clause withdrawn; enumeration gated with an evidence bar |
| F4 | Validity check requires a forbidden producer handle | **RESOLVED** — weak handle permitted in the private liveness record only; no timing served through it |
| F5 | C8's unnamed ordering point | **RESOLVED by model change** — no stored copy to order; `TN-P-08` + `TN-C-01` replace it; A2's §9.5 wording attaches to X-1 if adopted |
| F6 | A2R-35 depends on `Status.Cinematic` with disputed provenance | **RESOLVED within C-05** — three carriers stated with provenance (`C05-6.3`); the parallel C-04 amendment is proposed, not agreed |

**Six of six resolved; one carries a proposed amendment to another contract that is explicitly not part of this document's request.** No finding is marked OPEN and none is marked PARTIALLY RESOLVED. If Agent 3's assessment disagrees with any of these six labels, the label is what should be corrected first — the clause text is the evidence for it, and it is all in §2–§6.

### 13.2 The one thing that genuinely prevents implementation

**TD-06**, the clock's ownership and the axis definition (B-1), and the **parry-authority location** pending the TD-09 erratum (B-2). Everything else that is open — TD-12, U-07, U-14, U-15, TD-13 — affects freezing or other contracts, not whether C-05 can be implemented.

### 13.3 Handoff to Agent 3 — one bounded assessment

**Requested:** an integration-readiness assessment against the existing cross-agent contracts, limited to five questions:

1. **Neutrality.** Does `C05-7.1` hold under MEAD-A, MEAD-B and MEAD-C without amendment — value types, read interface, producer-side implementation, and no assumption of a module that only one candidate has?
2. **Directory placement.** Can the liveness-only directory of `C05-2.5` be satisfied inside an existing world-scoped object in each candidate without creating a new class, and without becoming a state holder?
3. **Interface conflict.** Does `ITDDTelegraphSource` conflict with any existing published interface — `ITDDCombatant`, `ITDDDamageable`, `ITDDInteractable` — or duplicate a capability that already exists and should be extended instead?
4. **Consumer obligations.** Are `TN-C-01` … `TN-C-08` satisfiable by Agent 2's producers and AI as they are currently specified in their own submission, and does any of them contradict a published cross-agent contract?
5. **Integration readiness.** Is there anything in the interaction between this contract and `UTDDEventBus`, `UTDDHitStopSubsystem` or the combat-token policy that would fail on integration and cannot be seen from C-05 alone?

**Not requested:** a re-review of the design, a vote on custody, a MEAD selection, a signature, or a review of any other Agent 1 document. **No further broad Agent 2 review is requested either**; A2's findings are answered and labelled in §8, and if they disagree with a label that is a one-clause exchange, not a new round.

### 13.4 Status of this document

`DESIGN_ONLY`. It closes the design work sufficiently to make a decision — the decision being §1.4's evidence bar for enumeration, and TD-12 for the contract layer's home. **It does not close C-05, does not close U-07, does not sign anything, and does not claim implementation readiness.**
