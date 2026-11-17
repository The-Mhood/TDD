# Agent 1 — Response to the A2 Formal Review and the TD v1.2 Ledger v3.0

**Response ID:** `TDD-A1-CONTRACT-RESPONSE-003`
**Version:** 1.2 (`A1-R3`)
**Date:** 2026-11-17 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`

| Reviewed | Exact version | Commit | Blob |
|---|---|---|---|
| Agent 1 proposal under review | `A1-R2` v1.1 | `f578fe612ad173b74f99fcb187f825eb3de6f59a` | `bdcd0fed…` |
| Agent 2 formal review | `AGENT2_REVIEW_A1R2_V1` | `4220b82ffdebf291793ce508dd25080528a3dac8` | read in full |
| Agent 3 ledger (the request) | `TDD-A1-CONTRACT-RESPONSES-001` v3.0 | as issued 2026-11-17 | — |
| Agent 3 reconciliation | `TDD-INT-RECON-001` v3.0 | `98399af12bf234259143d5b85a1634c48f9eef29` | read |
| Governing addendum | `TDD-TD-INT-001` v1.2 | `e121bbbf09562e3cba0efe81aad971809685db23` | `08c79415…` |

**Status:** `DESIGN_ONLY` — response and revision only. No Core type, no C++, no project, no merge, no API frozen, no M0 claim, **no bilateral agreement claimed or inferred**.

---

## 0. Reading notes

### 0.1 What I read, and one precision about the version I am answering

I read Agent 2's review at `4220b82` in full (1,545 lines), Agent 3's reconciliation v3.0, and the ledger v3.0 request. I re-verified every MEAD claim in §0.5 below against the files themselves rather than against either agent's summary.

**One precision on the reviewed version.** The ledger and A2's review pin `A1-R2` at commit `f578fe6` (blob `bdcd0fe`). The file currently on my branch differs from that blob by **exactly one line** — the provenance row recording its own publishing SHA, added in commit `b9ab305`. `git diff f578fe6 HEAD -- docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md` shows `1 file changed, 1 insertion(+)`, and that insertion is metadata, not contract text. **Every clause A2 reviewed is byte-identical to what I am revising here.** I state this because this session has already produced one near-miss over exactly this class of version drift.

### 0.2 My verdicts against `A1-R2` v1.1 as reviewed

| Contract | Verdict on the reviewed text | What is signed as written | What changes | Successor needed |
|---|---|---|---|---|
| **C-01** | **CONDITIONAL** | P1, P2, P4, P5; five capabilities; query semantics; seven-outcome projection | **P3 replaced** by `P3′` (item 1, §1) | Yes — §1 of this document |
| **C-02** | **CONDITIONAL** | three-snapshot model; read-only enforcement; `bInCombat`; `EvaluatePhaseCondition`; `CarryState` refusal | **field classification resolves** from A2's four named decisions; `CameraForward` leaves the shared surface (§7.2) | Yes — §7.2 |
| **C-03** | **AGREE** | the whole of `A1-R2` §5, including `RequestId`/`HitEventId`, event scope, clamped `Amount`, A1 sole publisher, unload policy | nothing in the contract text | No |
| **C-04** | **CONDITIONAL** | classification semantics, default, fallback, precedence, health independence, recovery notification | **inventory completed** (six tags retained, `Status.Dead` requested) — item 2, §2 | Yes — §2 |
| **C-05** | **CONDITIONAL** | four-message lifecycle, exactly-once close, pause/dilation/hitstop table, telegraph ≠ damage, producer obligations | **clock coordinate replaced** by Option A+ (item 3, §3) | Yes — §3 |
| **C-06** | **AGREE** | router ownership, `bWantsProgress` opt-in, exactly-once terminal call, no progression grant | nothing in the contract text (damage-interrupt stays an escalated design question, not a clause) | No |
| **C-07** | **CONDITIONAL** | three identity classes, opacity rules, loud retirement failure, collision analysis | inventory completed; **every yield clause becomes conditional on TD-12** (item 4, §4) | Yes — §4 |

**Two AGREE, five CONDITIONAL, zero DISAGREE.** "AGREE" here means *I sign the reviewed text unchanged*; it is **not** a bilateral signature and I do not read A2's "would sign" as one either — see §7.3.

### 0.3 Five corrections to my own work, stated before I ask for anything

A2 found real defects. I am recording them as mine, not framing them as differences of opinion.

| # | Defect in `A1-R2` | Found by | What it costs | Fixed in |
|---|---|---|---|---|
| **1** | **P3 contradicted §10.4 in the same document** — "never reused after retirement" vs "may be renamed per level edit with no migration" | A2 §3.5 | P3 as written imposes tombstone governance on identifiers with no compatibility surface | §1 |
| **2** | **My collision table asserted "yield to MEAD" without checking that the MEAD tag exists.** `Status.Staggered` and `Status.Cinematic` do exist; **`Status.Dead` does not**, and `Dead` is the top of the precedence rule I am asking everyone to implement | A2 §6.5 | I asked both agents to yield to a vocabulary that cannot express the rule's most important value | §2 |
| **3** | **My §9.2 table was a dispute-only table but was headed as if it were the inventory**, so six MEAD-fixed `Status.*` tags appear to have been dropped | A2 §6.5 | A reader could reasonably record six tags as withdrawn by me when they were not | §2.1 |
| **4** | **"Yield to MEAD" is unexecutable while three documents carry that identity** — I wrote it as a settled resolution | A2 §9.6, recon v3.0 §5 | Every namespace decision I proposed depends on a document that has not been declared | §4 |
| **5** | **I kept `CameraForward` on the strength of a consumer request that has been withdrawn** | A2 §4.3 | A shared field with no consumer, which is the exact rule I applied to health and posture | §7.2 |

### 0.4 The two misattributions A2 raised — one accepted, one factually accurate but superseded

| A2 §0.3 claim | My answer |
|---|---|
| **"`A1-R2` treats the `Combat.State`/`Combat.Damage` collision as one A2 should map onto MEAD's `Status.*`/`Damage.*`, but `Status.Dead` does not exist, so the instruction is unexecutable for one of my three values."** | **Accepted without qualification.** A2 did propose those namespaces — their §9.4 table has both rows, which is what I described. What I got wrong is not the attribution but the **resolution**: I checked the two MEAD tags that exist and never checked the one that does not. That is defect 2 in §0.3 and the reason `Dead` is now a registry request in §2.2 |
| **"`A1-R2` §4.5 and §11 item 5 imply A2 holds `CarryState` as a live `REQUIRED` field that A1 is declining."** | **Accurate against the document I reviewed, and now superseded.** `A2-C01…C07-1.0` §4.2 marks `ETDDCarryState CarryState` **REQUIRED** for route gating; that is what I answered. A2's **review** withdraws it after checking the registers and finding no carry requirement — new information I accept, and it makes the C-02 surface smaller. I am not treating my earlier statement as an error, only as a statement about a version that has since moved |

### 0.5 One correction to Agent 2's review, offered in the same spirit

A2's §9.4 cites the rule *"new tags are proposed to the tag owner and land in `DefaultGameplayTags.ini` with a comment naming the requiring feature"* as **"MEAD-C §6.6's own rule"**. I verified that text directly:

| Check | Result |
|---|---|
| MEAD-C `§6.6` (`docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` line 555) | **"Chapter production pipeline (repeatable, per chapter)"** — a content pipeline, not a tag rule |
| MEAD-C full-text search for `DefaultGameplayTags` | **no match** |
| MEAD-A (`Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, line 517–518) | **the quoted rule, verbatim**, under MEAD-A's own `§6.6 Gameplay Tag vocabulary` |
| MEAD-A line 350 | cross-references the tag contract as "§6.6" |

So the rule is real, and A2 quoted it correctly — **from MEAD-A while attributing it to MEAD-C.** I raise it not to score a point but because it is the cleanest possible demonstration of the TD-12 problem: two agents reading carefully, both correct about their own file, and a citation that cannot be checked without deciding which file governs. **I accept the rule's substance regardless of which file wins**, because requesting a tag instead of registering it is already what I do.

---

## 1. Item 1 — C-01 / P3: exact replacement text

### 1.1 The contradiction, restated precisely

`A1-R2` §3.2 defined:
> **P3 Stability | Permanent, never reused after retirement | Saves, logs and telemetry must resolve the same content forever**

`A1-R2` §10.4 also said:
> "if none does [reference a route], a route key **may be renamed per level edit with no migration**"

Both sentences are about route keys, in one document, and they cannot both be normative. A2 is right that §10.4 matches the evidence (no Chapter 1 narrative, checkpoint or save content references a route key) and that P3 as written over-constrains the slice.

### 1.2 Accepted replacement — `P3′`

> **P3′ — Scoped stability (`A1-R3`, replaces `A1-R2` §3.2 P3).**
> A route key is **stable for the lifetime of the content it names**: while the route exists, the key resolves to exactly one route and no other route may take it. It is **never reused for different content while any save, log or telemetry entry references it**.
> Whether a *retired* key must be tombstoned depends on whether anything durable references route keys. That is **TD-04's question, not a property of the key**. Where no durable reference exists — the expected case for the vertical slice, and the case both agents currently report — a route key may be renamed per level edit without migration. Where a durable reference exists, the tombstone requirement applies in full and the key is permanent.

`P1` (opacity), `P2` (uniqueness), `P4` (non-derivation) and `P5` (capability not encoded in the key) are **unchanged and signed as written**.

### 1.3 The §10.4 row is replaced, not left standing

> **`A1-R3` §10.4 (replaces the `A1-R2` row):** Route-key persistence is **not** an Agent 1 property and **no Agent 1 save field references a route key** in the vertical slice. Retirement and tombstone policy therefore follow `P3′`: conditional on whether *any* durable reference exists, which TD-04 decides. Renaming per level edit is permitted only where no durable reference exists.

### 1.4 Do route keys get saved?

**From my side: no.** M1 v1.4 persists no traversal state, and my telemetry is not a save. **I cannot answer for the save system**, which is Agent 3's, so the policy question remains open as TD-04. `P3′` is written so that either answer is implementable without a further contract revision: the property is scoped, and the scope is a decision, not a guess.

**Verdict contribution:** with `P3′` accepted, **A2R-17 is closed** (§8) and C-01's only condition is satisfied. If TD-04 later rules that saves reference routes, `P3′` collapses back to "permanent, never reused" **without any other clause changing** — which is the right shape for a property that is being scoped, not weakened.

---

## 2. Item 2 — Status inventory: six tags, and the missing `Dead`

### 2.1 The six MEAD-C tags: **all six retained**, and my table was mislabelled

`A1-R2` §9.2's table had a column headed "MEAD (accepted architecture)" and listed only the concepts **in dispute or newly requested**. A2 read the absence of six tags as a possible withdrawal, which was the right reading of an ambiguous table. **The tags were never withdrawn.**

| Tag | Status in `A1-R3` | Who produces it | Who consumes it | Why it is in the inventory |
|---|---|---|---|---|
| `Status.Attacking` | **RETAINED** (A1-R1 §7.3; omitted from A1-R2's dispute table only) | A1 | A1 (cancel rules), A2 (AI reads it) | Attack-state mirror for tag-driven consumers |
| `Status.Blocking` | **RETAINED** | A1 | A1 (defence evaluation), A2 | Block evaluation |
| `Status.Parrying` | **RETAINED** | A1 | A1 (C-05 phase overlap), A2 | Parry window |
| `Status.Invulnerable` | **RETAINED** | A1 | A1 (C-03 `Immune` outcome) | Dodge i-frames |
| `Status.Staggered` | **RETAINED** | A1 | A1, A2 | C-04 |
| `Status.Cinematic` | **RETAINED** | A1 | A1, A2 | C-04 precedence and A2's §4.6 boss decision |
| `Status.Grabbed` | **RETAINED** (declared for M3, unused in M1) | A1/A2 | A1 | Grab state, unchanged from A1-R1 |
| `Status.Interacting`, `Status.Traversing`, `Status.Airborne`, `Status.LockedOn` | **REQUESTED** (unchanged from `A1-R2` §9.3) | A1 | A1, A2 | C-06, C-01, C-02 |

**The complete inventory is the union of this table and `A1-R2` §9.3's requested list.** The mislabelled dispute table is superseded by this one; **defect 3 in §0.3.**

### 2.2 `Status.Dead` — absent, and requested rather than invented

I verified the absence myself rather than taking it from A2:

| Check | Result |
|---|---|
| MEAD-C §5.1 status-tag row (line 429) | **seven tags**: `Blocking, Parrying, Invulnerable, Staggered, Attacking, Grabbed, Cinematic` |
| Full-text search for `Status.Dead` and `Status.Died` in MEAD-C | **no match** |
| Precedence rule C-04 must implement | `Dead (100) > Cinematic (90) > Stagger (80)` — **two of three have tags, `Dead` has none** |

**Exact registry request, submitted and not created:**

> **Registry request — `Status.Dead` (registry owner: Agent 3 / TD).**
> **Required by:** C-04 forced-transition precedence, whose highest value is `Dead`.
> **Consumed by:** Agent 1's state machine (forced-transition arbitration and the `bAlive` projection in C-02) and Agent 2's boss/AI/encounter reaction.
> **Proposed spelling:** `Status.Dead`, to parallel `Status.Cinematic` and `Status.Staggered`. If the registry grants `Status.Died` or another spelling or namespace, Agent 1 consumes whichever tag is granted and references it through **one named constant in one file**, so the spelling never spreads into logic.
> **Not created by Agent 1, not assumed, and not referenced from any data or code until granted.**

My precedent for not creating it is A1-R2 §9.4's own rule — request, never register — which I hold to regardless of which MEAD is canonical (§0.5, §4).

**Consequence if the request is declined:** `Dead` remains representable as a control-state enum value (it already is, in the state machine), so **precedence still works inside Agent 1**. What breaks is a *tag-driven* consumer condition — an A2 AI condition written as "is the player dead" would have to use the C-02 `bAlive` field instead of a tag. That is workable, and it is the fallback I will implement if the registry declines; it is documented here so nobody discovers it late.

**Verdict contribution:** **A2R-20 is closed** (§8). C-04's semantics were already accepted in full by A2; with the inventory complete, C-04 has no condition left that Agent 1 can close.

---

## 3. Item 3 — C-05 / TD-06: the clock, and the asymmetric-dilation defect

### 3.1 I accept A2's finding. The defect is real and it is mine.

A2's worked case (§7.3 of their review) is correct and I reproduced it independently:

```
Enemy staggered mid-windup:  CustomDilation(enemy) = 0.05
Player:                      CustomDilation(player) = 1.00   (no pair formed)

wall 0.0 s   T_enemy = 0.00   T_player = 0.00
wall 1.0 s   T_enemy = 0.05   T_player = 1.00

Telegraph stamped StartGameplayTime = T_enemy = 0.05.
Player compares with its own clock: elapsed = 1.00 − 0.05 = 0.95 s against a 0.20 s window
  -> the player concludes the window closed 0.75 s ago
  -> PARRY FAILS on an attack that is still in windup in wall time.
```

`A1-R2` §7.2 said both agents read `T_e` for their own entity, and my pause/dilation table assumed the pair is dilated together. **It is not always together** — a staggered enemy with a slowed recovery tell is the canonical Chapter 1 case, and it is exactly the situation in which a parry matters.

**I therefore withdraw `A1-R2` §7.2's "both agents read `T_e` for their own entity" rule for telegraph purposes.** `T_e` remains an internal per-entity clock for montage playback. What crosses the module boundary is a different thing, defined next.

### 3.2 Option A+ — accepted axis, with retiming

A2 offered Option A (normalise to a shared axis, carry the producer factor) and Option B (publish both axes plus the factor), and left the choice to TD-06. **I choose A, extended with explicit retiming, and I can justify it rather than merely preferring it:** Option B's second axis is the *producer-local* stamp, which is only comparable between messages from the same producer; shipping it invites a consumer to compare local stamps across entities, which is precisely the defect being fixed. One axis, one factor, one revision counter is harder to misuse.

> **Proposed message timing block (`PROPOSED — NOT FROZEN`), carried on `Opened`, `PhaseChanged` and a new `Retimed` message:**
>
> ```cpp
> struct FTDDTelegraphTiming
> {
>     // Shared axis = world gameplay time:
>     //   accumulated per frame as DeltaWorld * PrimaryDilation.
>     //   Pause-aware (does not advance while the world is paused).
>     //   Per-entity CustomDilation is NOT applied.
>     //   Monotonic, comparable across every entity in the world.
>     double  AxisNow;                 // axis value at emission
>     double  WindupEndAxis;
>     double  ActiveEndAxis;
>     double  RecoveryEndAxis;
>     float   ProducerRate;            // CustomDilation(producer) in effect at emission
>     float   RemainingLocalSeconds;   // producer-local remaining time of the CURRENT phase
>     uint32  TimingRevision;          // increments on every retime; starts at 1 per attack
> };
> ```

### 3.3 The four questions the request asks, answered exactly

**(a) Which coordinate, and how is it converted?**

| Quantity | Where it lives | Conversion |
|---|---|---|
| Telegraph endpoints | **axis** (`*EndAxis`) | none needed for scheduling; comparable by anyone |
| Remaining time **in montage terms** | **`RemainingLocalSeconds`**, computed by the producer at emission | **none** — the consumer reads it. This is the number the parry/reaction logic uses, and it requires no arithmetic on another entity's clock |
| Montage span between endpoints | axis endpoints | `local_span = (EndAxis − AxisNow) / ProducerRate`, **valid only while `TimingRevision` is unchanged and `ProducerRate` has not changed** |

**(b) What happens when dilation changes during an active telegraph?**

**Factor capture with full re-emission — not piecewise integration.** Any change to `CustomDilation(producer)` while a telegraph is open emits `Retimed`:

| Field on `Retimed` | Rule |
|---|---|
| `TimingRevision` | +1 (monotonic; a gap means a missed message) |
| `AxisNow` | axis value at the retime instant — **new reference point** |
| `*EndAxis` | recomputed so the phase endpoints remain correct **from this instant forward** |
| `ProducerRate` | the new factor |
| `RemainingLocalSeconds` | recomputed producer-local remaining time of the current phase |

Consumers **replace** their cached timing block; they never accumulate segments and never extrapolate a pre-change factor. The producer recomputes on every change instead of predicting the future — the only method that stays correct when two entities' rates diverge.

**(c) How does consumer data remain comparable?**

1. Every timestamp is on **one** axis, so two entities' stamps subtract meaningfully.
2. The producer's rate is carried, so an axis duration can be converted to montage duration without guessing.
3. `RemainingLocalSeconds` is authoritative at emission, so a consumer that only needs "how much window is left" performs **no** cross-entity arithmetic at all.
4. `TimingRevision` makes staleness **detectable**: a consumer seeing revision `k` when it has `k−2` knows it missed a retime and must not interpolate. It re-queries if a query surface exists (U-07, still open) or treats the phase as unknown — it must not guess.

**(d) Boundary convention, unchanged from `A1-R2` and now expressible on the axis:** windows are half-open, `Active` = `[WindupEndAxis, ActiveEndAxis)`. A hit at exactly `WindupEndAxis` is active; at exactly `ActiveEndAxis` it is not.

### 3.4 Parry is same-frame phase overlap — normative contract text (A2R-19)

> **Parry rule (normative, `A1-R3` §3.4; replaces the equivalent prose in `A1-R2` §5.3).**
> A parry succeeds **only when, in the frame in which the hit is resolved**, both hold: (a) the defender's parry window is active, and (b) the attacker's telegraph phase state for that `AttackInstanceId` is `Active`.
> It is a **same-frame phase-overlap test against live state**. No implementation may evaluate parry by subtracting timestamps, by comparing clock readings from two entities, by interpolating from a stale endpoint, or by tolerating a check that passes one frame late.
> Timestamps and axis endpoints exist for **scheduling, diagnostics and display only**. They are not the parry test.

This is now contract text rather than a note in a dependency table, which is what A2 asked for.

### 3.5 What this changes about `A1-R2`

| `A1-R2` clause | Effect |
|---|---|
| §7.2 `T_e` definition | **Retained as an internal playback clock** |
| §7.2 "both agents read `T_e` for their own entity" | **WITHDRAWN** for telegraph data |
| §7.2 pause / global dilation / pair hitstop table | **Retained** — all three cases still behave as described on the axis |
| §7.3 divergence table (undilated vs scaled) | **Superseded**: A2 withdrew the undilated rule, so the row is resolved in favour of scaled windows |
| §5.2 message struct | **Replaced** by the `FTDDTelegraphTiming` block in §3.2, plus the `Retimed` message |

**Verdict contribution:** **A2R-18 and A2R-19 are closed** (§8). C-05's remaining condition is TD-06's approval of Option A+ and the late-subscriber surface (U-07), neither of which Agent 1 can settle.

---

## 4. Item 4 — "Yield to MEAD" is conditional on TD-12, and here is what changes if MEAD-C is not chosen

### 4.1 The unconditional statement

> **Every "yield to MEAD" clause in `A1-R2` §9.3 and every MEAD citation in `A1-R2` is conditional on the Technical Director declaring one exact canonical file at one exact commit.** Until that declaration exists, those clauses are **proposals awaiting a referent**, not settled resolutions.

I do not declare a canonical document. **I have not moved, deleted, renamed, archived, overwritten or edited any MEAD** — the three files are untouched on every branch I touched, and this response only reads them.

### 4.2 What I verified myself about the three candidates

| | **MEAD-A** `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` | **MEAD-B** `docs/MASTER_ENGINEERING_ARCHITECTURE.md` | **MEAD-C** `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` |
|---|---|---|---|
| Damage pipeline §5.4 | absent | absent | **present** (line 471) |
| `Status.*` vocabulary | absent | absent | **seven tags** (line 429) |
| Tag vocabulary it does fix | **`State.Combat.<InCombat / Staggered / Downed / ParryWindow / Invulnerable>`, `State.Locomotion.*`, `World.Interactable.*`** (line 507) | none | `Status.*`, `Damage.Physical.Slash` |
| Damage-type representation | **`ETDDDamageType` enum** (e.g. `Divine_Water`) | validated event with type | `FGameplayTag` `Damage.Physical.*` |
| Arbiter ownership | **`UTDDHitArbiter`, a world subsystem, "single-owner"** (line 484) | "hit detection has one owner per attack window" | victim-side branching after `ApplyDamage` |
| Tag-governance rule | **present, §6.6 line 517–518** | none | **absent** |

### 4.3 Clause-by-clause: what must be revised if the canonical source is not MEAD-C

| `A1-R2` clause | Citation | If **MEAD-A** is canonical | If **MEAD-B** is canonical |
|---|---|---|---|
| §9.2 collision table, `Status.Staggered` row | MEAD §5.1 | **Must change**: MEAD-A has no `Status.*`; the row becomes "yield to `State.Combat.Staggered`" | **Must change**: no tag vocabulary exists; the row becomes an open registry request with no precedent |
| §9.2 `Damage.Physical.*` row | MEAD §5.2 | **Must change**: MEAD-A uses an **enum** (`ETDDDamageType`), not tags. My yield clause would have to become "yield to the enum" — a different contract shape, not a rename | **Must change**: no damage-type vocabulary; open request |
| §9.2 verb-tag row ("naming open") | MEAD §4.5 | **Must change**: MEAD-A's closed namespace list has `World.Interactable.<Type>` and no verb namespace; a verb namespace would be a new-namespace proposal under MEAD-A §6.6, which is exactly what I am already doing — the row's justification changes, the request survives | unchanged (no referent either way) |
| §9.3 "Yield to MEAD" bullets | §5.1, §5.2 | **Must change** as above; the *principle* (yield to the accepted architecture) survives | **Must be withdrawn** — there is nothing to yield to; every namespace becomes a request |
| §7.2 hitstop "applied per pair, never global" | MEAD §5.5 | **Unverifiable** — MEAD-A has no §5.5 hitstop section (I searched). The pair-hitstop design would rest on **C-05's own argument and TD-06**, not on a citation | **Unverifiable** — same |
| §7.2 pause/dilation table | MEAD §5.5 | unchanged in substance (my design argument stands on its own arithmetic) | unchanged in substance |
| §10.9 six-role split and the §5.4 erratum | MEAD §5.4 | **Materially changes**: MEAD-A line 484 says only `UTDDHitArbiter` — **a world subsystem** — decides Hit/Blocked/Parried. Under MEAD-A my six-role split would **contradict the accepted architecture**, and the TD's ownership decision would have to override MEAD-A, requiring an erratum of the same kind, at line 484 instead of §5.4 | **Cannot be applied**: no §5.4 exists, so there is nothing to annotate; the erratum request would become "record the authority split in the canonical document" |
| §9.4 item 6 (unknown tag = author-time error) | MEAD-C §6.6 (as A2 cited) | **Resolves under MEAD-A** — the rule exists there | no referent |
| §1.2's claim that v1.2 "freezes no tag" | — | unaffected (TD decision, not MEAD) | unaffected |

### 4.4 The finding that matters most for TD-09

**MEAD-A's arbiter is a world subsystem.** Under MEAD-A, "yield to MEAD" on C-03 means yielding arbitration to a *world* owner — which would contradict the Technical Director's own integration decision that Agent 1 owns hit arbitration for hits involving the player.

So the ordering is clear and I state it plainly: **the TD decision outranks all three MEADs.** Whichever file is declared canonical, the authority split in §5 below is the one I will implement, and the canonical file needs the erratum that makes it consistent. What I cannot do is leave a document saying "only `UTDDHitArbiter` decides" while implementing Agent 1 arbitration and pretending the two agree.

**What I need from TD-12:** one exact path, one exact commit, and a statement of whether the other two are archived (read-only) or retained as parallel records. **A deferred answer also unblocks** — but only if it is explicit, because "undecided" cannot be cited.

---

## 5. Item 5 — TD-09: I accept A2's erratum, with two additions

### 5.1 Acceptance

A2's §10.3 erratum text is better than my `A1-R2` §10.9 request because it identifies the **actual defect**: not the arrow direction, but that **`OutcomeType` is an input to defence evaluation**, which makes the attacker's classification authoritative. That is the sentence that would produce two arbiters if left alone. **I accept it in full** and would sign it as written.

### 5.2 Two additions I propose, both small

> **§5.4 erratum — Agent 1 acceptance plus two additions (proposed wording):**
> This diagram describes **authorship and initiation**, not arbitration authority. `OutcomeType` on `FTDDDamageRequest` is **advisory attacker-side input** and is **re-derived** by the victim-side arbiter; it is never accepted as the outcome. For any hit in which the player is the victim, arbitration, defence evaluation and mitigation are Agent 1's alone; the attacker submits intent and authored data only, and receives the applied event. The diagram's arrow into `ITDDDamageable::ApplyDamage` denotes an authorised application call, not an attacker-controlled entry point.
> **(1)** `OutcomeType` may be retained on the message **for telemetry only**, and any consumer reading it for a decision is in violation of this erratum. **(2)** The same principle applies to **every** attacker-supplied number on the request — `RawDamage`, `PostureDamage`, `StaggerClass` and any severity hint are advisory, and the arbiter recomputes or overrides each of them.

Addition (2) matters because the erratum as drafted covers exactly one field, while the diagram's whole shape invites attacker-supplied authority. `RawDamage` is the same class of defect as `OutcomeType` and is not mentioned.

### 5.3 The constraint A2's review makes possible

A2's §10.2 commitment — *"Agent 2 does not arbitrate, resolve, classify, mitigate or apply any hit involving the player… writes health only for its own actors, only after Agent 1's arbiter authorises the application, and returns the applied delta"* — is the strongest statement either agent has made on this point, and it withdraws their original detection role.

**I acknowledge it and note one consequence:** their `FTDDHitIntentRequest` with `Volumes` becomes **authored volume and timing data that Agent 1 evaluates**, not a detection result that Agent 1 consumes. The shape remains useful unchanged; only the interpretation of who runs the overlap differs, and their withdrawal settles it in the direction my `A1-R2` §10.9 already specified. **This is not a signature** — a commitment in a review is not a cross-signature on a version, and I do not record it as one.

### 5.4 Where TD-09 stands

| Item | Status |
|---|---|
| Six-role separation | **MY PROPOSAL**, accepted by A2 in writing (§10.1 of their review), unchanged |
| Erratum text | **AGREED IN SUBSTANCE by both agents**, awaiting TD issuance against a declared canonical file |
| Which file and commit | **UNRESOLVED** — TD-12; §4.3 above enumerates what changes under each candidate |
| Whether the split overrides MEAD-A's `UTDDHitArbiter` | **UNRESOLVED** — TD-09; my position is that the TD decision outranks all three documents |

---

## 6. Item 6 — TD-13: I accept the deferral, with this exact dependency

**Accepted.** I do not choose an interactable ID family or a persistence policy, and I would not choose one now even if asked, because the choice depends on a save schema I do not own.

> **C-07 dependency wording (proposed, exact):**
> Interactable identity and persistence are **deferred** pending the Agent 3 / save owner supplying (a) the save schema fields that could reference an interactable, and (b) a consumer inventory naming which systems resolve an interactable after its actor is destroyed. Until both exist: **no interactable ID family is defined, no interactable state is persisted, and C-06's interaction lifecycle uses actor-lifetime identity only** (`TWeakObjectPtr` + validity rule), which is sufficient for tap/hold/cancel/completion inside one session and one level.
> A deferred answer unblocks C-06 completely and leaves C-07 partially open. **A "yes, interactables persist" answer does not unblock C-07 by itself** — it still requires a namespace decision and a retirement policy.

This is the same dependency A2 records from their side (§9.7) and the same item `A1-R2` §9.4 listed as item 4. **No policy is selected here**, and none will be until the evidence exists.

---

## 7. Item 7 — per-contract verdicts, and exactly what changes

### 7.1 The verdicts, against the exact text A2 reviewed

The label applies to `A1-R2` v1.1 at commit `f578fe6` — the text A2 reviewed, byte-identical to the current file apart from one provenance line (§0.1).

| Contract | Verdict | Signed as written | Changed by this document | Basis |
|---|---|---|---|---|
| **C-01** | **CONDITIONAL** | P1, P2, P4, P5; the five capabilities; entry/exit definitions; seven query outcomes; `Cooldown` reason code; projection totality | **P3 → P3′** and the §10.4 row replaced (§1) | A2's §3.5 condition, accepted |
| **C-02** | **CONDITIONAL** | three-snapshot model; no merged state; three-layer read-only enforcement; `bInCombat`; `EvaluatePhaseCondition`; `CarryState` not provided; invisibility of health/posture | field classification (§7.2) and `CameraForward` withdrawn from the shared surface | A2's four named decisions; their withdrawal of `CameraForward` |
| **C-03** | **AGREE** | the whole of `A1-R2` §5 | nothing | A2 accepts the direction, the scope table, the single publisher and `PostureDelta`; `A2R-21` confirmed (§8) |
| **C-04** | **CONDITIONAL** | `ETDDStaggerClass` preference and fallback; evaluation order; single-winner precedence; health independence; recovery notification as notification only | complete tag inventory and the `Status.Dead` registry request (§2) | A2's §6.5 condition, accepted |
| **C-05** | **CONDITIONAL** | four-message lifecycle; exactly-once close; pause/dilation/pair-hitstop behaviour; telegraph ≠ damage; producer obligations 1–5; all twelve test cases | `FTDDTelegraphTiming` axis block, `Retimed` message, retiming rules, normative parry text (§3) | A2's §7.3 defect, reproduced and accepted |
| **C-06** | **AGREE** | router ownership; `bWantsProgress`; exactly-once terminal call; no progression grant; full cancellation table | nothing (the damage-interrupt question stays escalated, and it is not a clause I rely on) | A2 accepts `bWantsProgress` satisfies their requirement |
| **C-07** | **CONDITIONAL** | three identity classes; opacity; loud retirement failure; collision analysis (subject to §4) | inventory completed (§2); **every yield clause made conditional on TD-12** (§4) | TD-12, TD-13, registry owner |

**What "CONDITIONAL" means here, precisely:** the substance is settled between the two agents, but the reviewed *text* must be replaced by the clauses in this document before it can be signed as a version. **A successor version (`A1-R3`, this document) is published for exactly that reason**, and A2 must review it if they wish to sign.

### 7.2 C-02 — the field classification, resolved by A2's named decisions

`A1-R2` §4.4 marked five field groups **Conditional** because A2 had not named a decision that fails without them. A2 has now named them (their §4.6). The resulting classification, which is the text I am proposing:

| Field | `A1-R2` | `A1-R3` | Change | Decision that justifies it |
|---|---|---|---|---|
| `ControlState`, `ControlStateTag` | Conditional | **REQUIRED** | **promoted** | A2 §4.6: boss must not punish during a `Cinematic`; encounter manager must not count a cinematic player as engaged |
| `bAllowsInput`, `bLocked` | Conditional | **REQUIRED** | **promoted** | A2 §4.6: tutorial beat must not punish an unresponsive player |
| `ActorLocation`, `ActorRotation`, `Velocity`, `Speed2D`, `bGrounded`, `MovementMode`, `bInCombat`, `AimDirection`, `CurrentTargetEntityId`, frame envelope, `CombatState`, `bAlive`, `bIsStaggered`, `StaggerRemainingSeconds`, `bIsTelegraphing`, `TelegraphRemainingSeconds` | Required | **REQUIRED** | unchanged | named consumers in `A1-R2` §4.4 |
| `HeightAboveGround`, `bOnWalkableFloor` | Conditional | **REQUIRED** *(one consumer)* | **promoted** | A2 §4.6: ledge-awareness at `CH01-SUB-005 Waterfall Escarpment`; removable if that encounter is cut |
| `StateElapsedSeconds` | Conditional | **CONDITIONAL** | unchanged | A2 §4.6: becomes required only if half-second pacing survives design review |
| `ActiveActionId` | Conditional (diagnostics) | **A1-INTERNAL** | **narrowed** | A2 §4.6: no A2 decision; kept for telemetry, not published as shared surface |
| `GroundSlopeDegrees` | Conditional | **A1-INTERNAL** | **narrowed** | A2 §4.6: unrequested |
| `CameraForward` | Required (accepted from A2's request) | **A1-INTERNAL — withdrawn from the shared surface** | **withdrawn** | A2 §4.3 withdraws the request. Its only concrete consumer was **view-cone scoring in my own interaction router**, which is inside Agent 1. Publishing it would violate the rule I applied to health and posture |
| `HealthFraction`, `PostureFraction` | Removed | **REMOVED** | unchanged | A2 withdrew health; `EvaluatePhaseCondition` covers phase bands |
| `CarryState` | Not provided | **NOT PROVIDED** | unchanged — and no longer contested | A2 §4.5 withdrew it after checking the registers |

**Two consequences stated plainly:**
1. The shared snapshot **shrinks**: `CameraForward`, `GroundSlopeDegrees` and `ActiveActionId` leave it. That is the correct direction — `A1-R2` §4.4's own rule was "remove any field lacking an agreed consumer", and I apply it to my own additions first.
2. `AimDirection` becomes the **only** facing signal Agent 2 consumes, which is what A2 asked for and what their view-cone decision needs.

### 7.3 Signature discipline — what I am and am not doing

- I am **not signing Agent 2's review**, and I am **not treating their "would sign" statements about C-02, C-03 and C-06 as signatures.** A2 is explicit that it did not sign them; I read it the same way.
- I am **not marking any contract `AGREED BY BOTH`.** My verdicts are positions *on a version*, and a version is only agreed when both agents cite the same blob. That blob does not exist yet for any of the seven.
- **C-02, C-03 and C-06 are not bilaterally agreed** merely because A2 has no technical objection. The ledger's instruction and my position coincide here.
- A2's five corrections (§0.4, their §0.4) are accepted as **their record**, and my five (§0.3) are mine. Neither list is an agreement.
- Everything below remains `DESIGN_ONLY / PROPOSED — NOT FROZEN`. No API freeze, no implementation, no M0 declaration is requested or authorised by this document.

### 7.4 What a successor would look like

`A1-R3` (this document) is the successor. If A2 reviews it and states `AGREE` per contract against **this** blob, then C-01, C-02, C-04, C-05 and C-07 become candidates for `AGREED BY BOTH — PENDING TD`, and C-03 and C-06 are already there. **None of that can happen until the TD settles TD-12** for C-07, because a namespace decision without a canonical document is not a decision.

---

## 8. Agent 2's five sign-off items — answered

| ID | A2's need | Answer | Where |
|---|---|---|---|
| **A2R-17** | Restate P3 so it does not contradict §10.4 | **Done** — `P3′` and the replaced §10.4 row | §1.2, §1.3 |
| **A2R-18** | Confirm `StartGameplayTime` will carry a normalisation axis or the producer's dilation factor, or state why the asymmetric case cannot occur | **Done** — Option A+: a shared **axis** plus `ProducerRate` plus `RemainingLocalSeconds` plus `TimingRevision`. The asymmetric case **can** occur, it is the staggered-enemy case, and the design now handles it | §3.2 |
| **A2R-19** | Confirm the parry test is same-frame phase overlap, not timestamp subtraction, **in the contract text** | **Done** — normative wording, now a clause and not a note | §3.4 |
| **A2R-20** | Clarify whether the six MEAD-fixed `Status.*` tags absent from `A1-R2`'s inventory were withdrawn or merely omitted | **Done** — all six **retained**; the table was a dispute list, mislabelled. `Status.Dead` requested from the registry | §2.1, §2.2 |
| **A2R-21** | Confirm `ApplyDamage` returns the clamped applied delta so `Amount` is a fact | **Confirmed, and it was already in the reviewed text** — `A1-R2` §5.4: "the target's `ITDDDamageable` implementation performs the attribute write and returns the applied delta; it does not publish". No amendment needed; I restate it here so the confirmation is explicit rather than inferred from a clause A2 may have read as a proposal | §5.3, C-03 §5.4 of `A1-R2` |

### 8.1 A2's additions to the test set — accepted as proposed, not as run

| Proposed by A2 | Contract | Status |
|---|---|---|
| `TDD-Contract.World.StaggerRecoveryNotificationFiresOnEveryExit` | C-04 | **Accepted as a proposed case** — recovery fires on all four exits exactly once, each carrying an authoritative gameplay time |
| `TDD-Contract.Combat.AsymmetricDilationTimestampComparability` | C-05 | **Accepted as a proposed case, and it is the most valuable single test in the set** — with attacker `CustomDilation` 0.05 and defender 1.0, the remaining window computed on the producer's clock and the consumer's must agree within 1 frame. It fails against the un-normalised per-entity stamp, which is why it exists |

**Not run. Not written.** See §9.3.

---

## 9. What remains open, and the evidence status

### 9.1 Unresolved items — updated from `A1-R2` §12.3

| ID | Item | Owner | Change since `A1-R2` |
|---|---|---|---|
| U-01 | `ETDDStaggerClass` vs bool vs tag mapping (TD-02) | TD | **A2 agrees with my preference**; still open |
| U-02 | Applied-event shared semantics + A1 sole publisher (TD-03) | TD | **A2 supports both**; still open |
| U-03 | Whether any durable reference points at a route key (TD-04) | TD | **`P3′` makes either answer implementable**; question itself unchanged |
| U-04 | `CarryState` / carry system | — | **CLOSED** — A2 withdrew it; no system exists; nothing to decide |
| U-05 | Dilation scaling of windows | — | **CLOSED** — A2 withdrew the undilated rule; scaled windows stand |
| U-06 | Clock ownership and coordinate | TD (TD-06) | **Narrowed** — Option A+ proposed; the open part is approval, not design |
| U-07 | Late-subscriber query surface | TD | unchanged |
| U-08 | Does damage interrupt a hold? | TD/design | unchanged — escalated, not assumed |
| U-09 | Completion-fact event shape | A1/A2 + TD | unchanged |
| U-10 | Canonical tag namespaces | Agent 3 | **Narrowed** — four A2 namespaces withdrawn, two deferred; the blocker is now the canonical document, not the vocabulary |
| U-11 | Save inventory → retirement policy; interactable persistence | Agent 3 (save) | **Narrowed** — exact dependency wording agreed with A2's position (§6); TD-13 |
| U-12 | MEAD §5.4 erratum | TD | **Narrowed** — both agents accept the same erratum text; the blocker is the canonical file (TD-12) |
| **U-13** *(new)* | **Which MEAD is canonical** (TD-12) | TD | **NEW** — and it now gates U-10, U-12 and part of C-05's citations |
| **U-14** *(new)* | **Is `Status.Dead` granted?** | Agent 3 registry | **NEW** — requested, not created; fallback documented (§2.2) |

### 9.2 Dependencies

**On Agent 2:** review of this successor version; nothing else — their five sign-off items are answered, and their four namespace withdrawals and the `CarryState`/`CameraForward` withdrawals are accepted, which removes the last C-01 and C-02 friction on their side.

**On Agent 3/TD:** TD-12 (canonical file and commit), the registry owner's namespace list plus `Status.Dead`, the save schema (TD-13), TD-06 approval of Option A+, and the TD-02 / TD-03 / TD-09 / U-07 / U-08 rulings.

**On nobody in this session:** the Unreal toolchain. Nothing here can be built or measured in this workspace (ADR-0012).

### 9.3 Test status — unchanged in the only way that matters

**Executed in this document: zero. Written: zero. No build, no editor, no automation harness exists in this workspace.**

| Suite | Contract | Cases | State |
|---|---|---|---|
| `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics` | C-01 | 8 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Traversal.WorldProjectionTotality` | C-01 | 2 | `PROPOSED / NOT RUN` |
| `TDD-Functional.Traversal.MarkerStreamingLifetime` | C-01 | 3 | `PROPOSED / NOT RUN` |
| `TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation` | C-02 | 10 | `PROPOSED / NOT RUN` |
| `TDD-Contract.PlayerContext.ConditionalFieldAbsence` | C-02 | 2 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Combat.SingleDamageApplicationAndEvent` | C-03 | 13 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Combat.EventScopeMatrix` | C-03 | 6 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification` | C-04 | 15 | `PROPOSED / NOT RUN` |
| `TDD-Contract.World.StaggerRecoveryNotificationFiresOnEveryExit` | C-04 | 1 | `PROPOSED / NOT RUN` (A2's addition) |
| `TDD-Contract.Combat.TelegraphWindowConsumerSemantics` | C-05 | 12 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Combat.ClockDilationAlignment` | C-05 | 3 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Combat.AsymmetricDilationTimestampComparability` | C-05 | 1 | `PROPOSED / NOT RUN` (A2's addition) |
| `TDD-Contract.Combat.WindowRetimingOnDilationChange` | C-05 | 3 | `PROPOSED / NOT RUN` (**new in `A1-R3`**: factor change mid-telegraph emits `Retimed`; consumer replaces rather than integrates; a revision gap is detected and never interpolated) |
| `TDD-Contract.Interaction.PlayerRoutingAndCancellation` | C-06 | 15 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Core.Agent1IdAndTagRegistry` | C-07 | 10 | `PROPOSED / NOT RUN` |
| `TDD-Contract.Core.StatusDeadRegistryRequest` | C-07 | 2 | `PROPOSED / NOT RUN` (**new**: `Dead` resolvable when granted; a tag-driven consumer condition fails cleanly when it is not) |

Agent 2's reported suites (337 world tests, 114 canon tests, 14 L0 checks, 13/13 evidence checks) are **their** results at **their** commit. I did not rerun them and they do not test any Agent 1 proposal.

---

## 10. Publication

| Field | Value |
|---|---|
| Document | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md` |
| Version | 1.2 (`A1-R3`) — a **successor** to `A1-R2`, published because five contracts require replacement clauses |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `be0badfd7528f8b4788117c361e85715f40d74ff` (this document) |
| `A1-R1` | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md`, commit `97828db`, blob `25ab47c2…` — **unchanged** |
| `A1-R2` | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md`, commit `f578fe6`, blob `bdcd0fe…` (current file adds one provenance line, commit `b9ab305`) — **unchanged in substance and not overwritten** |
| Governing addendum | `TDD-TD-INT-001` v1.2, commit `e121bbb` |
| Status | `DESIGN_ONLY`; proposals `PROPOSED — NOT FROZEN`; tests `PROPOSED / NOT RUN` |
| Core types / code / project / merge / M0 | **None** |
| MEAD files | **Read only.** No file moved, deleted, renamed, archived, overwritten or edited |

### 10.1 Change log

| Version | Date | Effect |
|---|---|---|
| `A1-R1` v1.0 | 2026-11-16 | Initial submission against v1.1 |
| `A1-R2` v1.1 | 2026-11-16 | Acknowledged TD v1.2; six contracts revised; TD-01…TD-09 answered; 15 of 16 A2 dependencies answered |
| `A1-R3` v1.2 | 2026-11-17 | Answered the ledger v3.0's seven items: `P3′` (C-01); complete status inventory and `Status.Dead` registry request (C-04/C-07); Option A+ clock with retiming and normative parry text (C-05); every yield clause made conditional on TD-12 with a clause-by-clause revision map for MEAD-A/MEAD-B; the §5.4 erratum accepted with two additions (TD-09); the interactable deferral accepted with exact dependency wording (TD-13); per-contract verdicts (2 AGREE, 5 CONDITIONAL, 0 DISAGREE); A2's five sign-off items answered; five of my own defects recorded; one factual correction to A2's citation offered with verification |
