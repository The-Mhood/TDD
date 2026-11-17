# Agent 1 — Corrections Following Agent 2's Review of `A1-R3`

**Response ID:** `TDD-A1-CONTRACT-RESPONSE-004`
**Version:** 1.3 (`A1-R4`)
**Date:** 2026-11-17 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`

| Reviewed | Exact version | Commit | Blob |
|---|---|---|---|
| Agent 1 submission under review | `A1-R3` v1.2 | `70db9665b67723a526a6d40fa71ec832f1a95498` (verified reachable on this branch) | `109331f36eddce7eee068aa278a474c07c950753` — the blob A2 reviewed |
| Agent 2 formal review | `AGENT2_REVIEW_A1R3_V1` | `4c0998004f8870fff9a6022ada0ceb2b7eb3de8e` | read in full (1,145 lines) |
| Governing addendum | `TDD-TD-INT-001` v1.2 | `e121bbbf09562e3cba0efe81aad971809685db23` | `08c79415…` |

**Status:** `DESIGN_ONLY` — corrections and clarifications only. No C++, no Core types, no Unreal project, no API freeze, no merge, **no MEAD selection**, **no tag registration**, **no erratum issuance**, no M0 claim. **No contract is bilaterally agreed.**

---

## 0. Reading notes

### 0.1 The one defect A2 found is real, and it is arithmetic

`A1-R3` §3.3(a) printed `local_span = axis_span / ProducerRate`. **That is inverted.** Derived from §3.2's own definitions, `d(local)/d(axis) = CustomDilation(e) = ProducerRate`, so the conversion is a **multiplication**. The error is invisible at rate 1.0 and inflates by `1/rate²` where the mechanism exists to help: at rate 0.05 an authored 0.20 s window reports as **80 s**.

I reproduced the numbers before writing anything (all four verified in this session, §2.2). A2's diagnosis, its magnitude, its worked case and its conclusion that §3.3(b) is the correct half are **all correct**. This is a transcription error of mine, not a design difference, and the correction is in §2.

Two things A2 stated that I want on the record because they bound the damage:
- **The parry outcome was never corrupted** by it: §3.4's same-frame phase-overlap test reads neither the axis endpoints nor `RemainingLocalSeconds`. C-05's defect is a **reporting** defect.
- **My own §7.3 and §7.4 contradicted each other on signature status** (§1.3 of their review). §7.3 was right; §7.4 was wrong. Corrected in §10.

### 0.2 What this document is

Nine requested corrections (§1), each traced to A2's finding ID. Where a correction changes contract text, the replacement text is given verbatim and labelled `PROPOSED — NOT FROZEN`. Where a correction is a TD question, it says so and does not answer it.

### 0.3 What is preserved

`A1-R1` (blob `25ab47c2…`), `A1-R2` (blob `5ee2769…` — the reviewed `bdcd0fe…` plus the one provenance line `A1-R3` §0.1 already documented) and `A1-R3` (blob `109331f3…`) are **unmodified by this task**, and their bytes still hash to the blobs recorded when each was published (§14.2). This is a new file. All three MEADs remain **read only** — nothing moved, deleted, renamed, archived, overwritten or edited. No tag was registered, no erratum issued, no namespace chosen.

---

## 1. Correction-to-review traceability

Every finding in A2's review, its disposition, and where the fix lives. **A2's §11 heading says "ten asks" and lists nine identifiers (A2R-22 … A2R-30); I address all nine and assume the count is a slip in their text, not a missing item.**

| A2 finding | A2's ask | My disposition | Fixed in | Contract |
|---|---|---|---|---|
| **A2R-22** | `§3.3(a)`: multiply by `ProducerRate`, not divide; state the derivation | **ACCEPTED — defect confirmed by independent computation** | §2 | C-05 |
| **A2R-23** | `§3.3(a)`: state that `RemainingLocalSeconds` ages by **axis × rate**, not wall time | **ACCEPTED** — the field is authoritative at emission only | §3 | C-05 |
| **A2R-24** | `§3.3(c)4`: record U-07 as blocking the retime mechanism, or define republish-on-request | **ACCEPTED BOTH WAYS** — a mechanism is defined **and** the residual blocker is retained explicitly | §4 | C-05 |
| **A2R-25** | `§5.2`: name the request-struct spelling as a TD decision; do not select by transcription. Three spellings at 15/16/17 characters | **ACCEPTED** — three exact locations listed, no selection made, TD asked | §6 | C-03 |
| **A2R-26** | `§4.3`: extend the MEAD-A column to all seven retained tags plus `Dead`; distinguish rename / semantic / new request | **ACCEPTED** — complete mapping, and A2's own count of four requests is confirmed | §7 | C-04, C-07 |
| **A2R-27** | `§2.2`: state that `Dead` is the only non-tag precedence value if the registry declines | **ACCEPTED** — exact sentence supplied | §8 | C-04 |
| **A2R-28** | `§7.2`: `A1-INTERNAL` fields are **excluded** from the published snapshot, not included-and-marked | **ACCEPTED** — and made testable | §9.1 | C-02 |
| **A2R-29** | `§7.2`: state whether `CombatState` is coarse projection or derived from the tag set | **ANSWERED** — it is authoritative; the tags are derived from it, with the mapping table and an invariant | §9.2 | C-02 |
| **A2R-30** | Amend `AsymmetricDilationTimestampComparability` to compare against the **authored** local window | **ACCEPTED** — amended, plus a negative control that would have caught A2R-22 | §5 | C-05 |
| **C-02-1** | The three narrowed fields must not leak back | **ACCEPTED** — folded into A2R-28's fix | §9.1 | C-02 |
| **C-02-2** | `CombatState` versus the C-04 tag set | **ANSWERED** — A2R-29 | §9.2 | C-02 |
| **C-03-1** | The erratum must name one spelling; `A1-R3` silently chose | **ACCEPTED — the silent selection is acknowledged as mine** | §6 | C-03 |
| **C-04-1** | If the registry declines `Dead`, say it is the only non-tag precedence value | **ACCEPTED** | §8 | C-04 |
| **C-04-2** | Extend `§4.3` to all seven tags plus `Dead` | **ACCEPTED** — same fix as A2R-26 | §7 | C-04 |
| **C-05-1** | Correct `§3.3(a)` with the derivation stated | **ACCEPTED** | §2 | C-05 |
| **C-05-2** | Revision gap is unrecoverable without U-07, or define recovery | **ACCEPTED BOTH WAYS** | §4 | C-05 |
| **C-07-1** | The contingency map is incomplete; complete it before TD-12 is answerable | **ACCEPTED** — same fix as A2R-26, and extended beyond the required scope | §7 | C-07 |
| **C-07-2** | TD-13 deferral accepted; C-07 needs three separate answers | **ACCEPTED, and A2's extension adopted**: no ordering shortcuts the other two | §11.2 | C-07 |
| **A2 §1.3** | `A1-R3` §7.4 overreaches on signature status; §7.3 and §7.4 contradict each other | **ACCEPTED — my error**; §7.3 was right | §10 | all |
| **A2 §1.4** | Their dispositions of my `§0.4`, `§0.5`, `§7.4` claims | **NOTED** — two accepted by them, one rejected by them and **accepted by me as correctly rejected** | §10.2 | — |
| **A2 §4.2** | `Dead` as a state value widens the fallback's limits (two-representation table) | **ACCEPTED** — A2's four-row table is more complete than my one-sentence fallback, and §8 now states the consequence | §8 | C-04 |
| **A2 §4.3** | Under MEAD-A, three tags and `Dead` become **namespace requests against a document that forbids new namespaces** | **ACCEPTED** — the sharpest point in the review; reflected in §7.3 | §7.3 | C-04, C-07 |
| **A2 §7.5** | Pause: the axis is pause-aware but `RemainingLocalSeconds` is not self-sufficient | **ACCEPTED** — folded into §3 | §3 | C-05 |
| **A2 §7.6** | A stale revision closes an open window at axis 2.0 that runs to 16.4 | **ACCEPTED** — this is the case §4's mechanism exists to fix | §4 | C-05 |
| **A2 §7.8 closing note** | The test as written lets producer and consumer agree while both are wrong | **ACCEPTED** — see the negative control in §5 | §5 | C-05 |

**Score, counted from the table below: 23 of 25 review findings accepted (two of them answered questions rather than defects, two accepted in both of the ways A2 offered), 1 noted, 0 rejected, 0 contested.** A2's own numbered asks are nine — `A2R-22` … `A2R-30` — and all nine are accepted. No A2 finding is disputed. Nothing in this table is a bilateral signature.

---

## 2. Item 1 — C-05: the conversion, derived

### 2.1 Derivation from the unchanged definitions

The definitions in `A1-R3` §3.2 stand and are **not** being redefined — which is why the formula must change:

```
Axis  (shared):   d(Axis) / d(wall)  = PrimaryDilation
Local_e:          d(Local_e) / d(wall) = PrimaryDilation × CustomDilation(e)
ProducerRate      := CustomDilation(producer)

Divide the two:
  d(Local)/d(Axis) = CustomDilation(producer) = ProducerRate

Over any interval in which ProducerRate is constant:
  ΔLocal = ΔAxis × ProducerRate            (local  ← axis : MULTIPLY)
  ΔAxis  = ΔLocal / ProducerRate           (axis   ← local : DIVIDE)
```

**`A1-R3` §3.3(a) printed the second relation under the name of the first.** It is wrong by a factor of `1/ProducerRate²`, and it is invisible at `ProducerRate = 1.0`.

### 2.2 Verification — the required example, computed not asserted

Authored parry window **0.20 s of local (montage) time**, producer at `CustomDilation = 0.05`:

| Quantity | Relation | Value | Expected by the request |
|---|---|---|---|
| Authored local window | given | **0.20 s** | 0.20 s |
| Shared-axis span | `0.20 / 0.05` | **4.00 axis-seconds** | **4.00** ✓ |
| Local span recovered | `4.00 × 0.05` | **0.20 s** | **0.20** ✓ |
| `A1-R3` §3.3(a) as printed | `4.00 / 0.05` | **80.00 s** | defect |
| Inflation factor | `80.00 / 0.20` | **400×** | `1/rate²` = 400 ✓ |

A2's retime case also reproduces exactly: `AxisNow = 0.4`, `Rate = 0.2`, `RemainingLocal = 0.800` → new `EndAxis = 0.4 + 0.800/0.2 = **4.40**`, which is §3.3(b)'s behaviour and therefore the correct one (the `§3.3(a)` path gives 20.00).

### 2.3 Replacement text — `§3.3(a)` corrected

> **`A1-R4` §3.3(a) — coordinate, conversion and derivation (replaces the `A1-R3` row).**
>
> | Quantity | Where it lives | Conversion |
> |---|---|---|
> | Telegraph endpoints | shared **axis** (`*EndAxis`) | none needed for scheduling; comparable across every entity |
> | Remaining time in **montage** terms | **`RemainingLocalSeconds`**, computed by the producer at emission | **none** — the consumer reads it |
> | Montage span between endpoints | axis endpoints | **`local_span = (EndAxis − AxisNow) × ProducerRate`** — **multiply**, valid only while `TimingRevision` is unchanged **and** `ProducerRate` has not changed |
> | Axis span from a local duration | local duration | **`axis_span = local_span / ProducerRate`** — **divide** |
>
> **Derivation (normative, so the next reader does not have to re-derive it):** the axis advances by `PrimaryDilation` per wall second; the producer's local clock advances by `PrimaryDilation × CustomDilation(producer)`. Therefore `d(local)/d(axis) = CustomDilation(producer) = ProducerRate`, so a consumer **multiplies** by `ProducerRate` to convert axis to local and **divides** to convert local to axis. Dividing where this says multiply inflates the span by `1/ProducerRate²` (at `ProducerRate = 0.05`, a 0.20 s window reports as 80 s) and is the defect this clause exists to prevent.
>
> **Both directions are stated because they are inverses, and stating only one is how the `A1-R3` error survived review.**

### 2.4 Reconciliation of §3.3(a) and §3.3(b)

| Clause | Direction it implies | After correction |
|---|---|---|
| `§3.3(a)` conversion table | axis → local | **`local = axis × rate`** |
| `§3.3(a)` inverse row (new) | local → axis | **`axis = local / rate`** |
| `§3.3(b)` retime endpoint recomputation | local → axis | **`EndAxis = AxisNow + RemainingLocal / rate`** — agrees with the inverse row |

They are now the same arithmetic applied in the two directions, and the retime rule is unchanged from `A1-R3` §3.3(b), which was already correct.

---

## 3. Item 2 — `RemainingLocalSeconds` semantics, stated in full

A2's finding is that the field was described as authoritative *at emission* and never defined afterwards, so two conforming consumers could disagree — one decrementing by wall time (closing a window early across a pause), one by axis × rate (correct). That is fixed by making the aging rule normative.

> **`A1-R4` §3.3(e) — lifecycle of `RemainingLocalSeconds` (new clause).**
>
> `RemainingLocalSeconds` (`R0`) is the producer-local montage time remaining in the **current phase** at the instant of emission, and is exact at that instant only. It is aged as:
>
> ```
> R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)
> ```
>
> and the phase is complete when `R(t) = 0`, equivalently when `Axis(t) − AxisNow ≥ R0 / ProducerRate`.
> **A consumer must age by axis elapsed multiplied by `ProducerRate`; never by wall-clock elapsed, and never by its own `CustomDilation`.** Aging by wall time shortens the reported window across any pause or dilation change; aging by the consumer's own rate is wrong whenever the rates differ, which is the case this mechanism exists for.

| Condition | Behaviour of `R(t)` | Message from producer | Consequence for the consumer |
|---|---|---|---|
| **Normal gameplay**, rate constant | Linear in axis elapsed, per the formula | none | Correct |
| **World pause** | Axis does not advance, so `R` is **constant**. No aging, no drift | none | Correct if the consumer respects the axis; a wall-clock consumer is wrong by the pause duration |
| **Primary dilation changes** | Axis keeps integrating at the new rate; `R` continues along the formula unchanged | **none required** — the axis definition already absorbs primary dilation, and the montage slows with it, so local and montage stay aligned | Nothing to do; this is why the axis is defined with primary dilation applied |
| **Producer `CustomDilation` changes** | **Formula becomes invalid at once.** Do not extrapolate | **`Retimed` in the same frame**, carrying `TimingRevision + 1`, a new `AxisNow`, recomputed `*EndAxis`, the new `ProducerRate` and a recomputed `R0` | **Replace** the stored block; never integrate across a rate change |
| **`Retimed` received** | Restart from the new `AxisNow` / `R0` | — | Use the highest revision only |
| **Revision gap** (e.g. holds `k−2`, sees `k`) | **Undefined — the consumer must not interpolate and must not extrapolate a stale revision** | producer does not re-send unilaterally | Recover per §4, or treat the phase timing as unknown and flag a diagnostic |
| **Phase change** | New `R0` for the new phase; `TimingRevision` increments | `PhaseChanged` | Re-anchor on the new block |
| **Telegraph closed** | Undefined and meaningless | `Closed` | Discard the block |

Two supporting rules, both testable:

1. **`R` is monotonically non-increasing** between messages with a fixed revision, and never negative (`max(0, …)` above).
2. **`R` is not the parry test.** §3.4 remains the authority for parry, and it reads live phase state, not this field. A wrong `R` produces a wrong *display, schedule or AI reaction*, never a wrong parry — which is exactly what bounds the severity of A2R-23 and A2R-24.

---

## 4. Item 3 — A2R-24: retime recovery, defined and still blocking where it is not

A2's finding: with U-07 open, a stale-revision consumer's only sanctioned response was "treat the phase as unknown" — a gameplay stall. Their model shows a stale consumer closing at axis 2.0 a window that runs to 16.4. I accept the finding and answer it **both ways**, because only one of the two is mine to give.

### 4.1 The mechanism I am proposing (resolves U-07 as a proposal)

> **`A1-R4` §3.3(f) — telegraph state retention and recovery (new clause, `PROPOSED — NOT FROZEN`).**
> `UTDDTelegraphBroker` (Core) is **stateful for open telegraphs**: it retains the current timing block and phase for every open `AttackInstanceId`, and exposes:
>
> ```cpp
> // PROPOSED — NOT FROZEN
> UFUNCTION() bool GetOpenTelegraphs(TArray<FTDDTelegraphState>& Out) const;
> // Synchronously copies the current phase + timing block of every open telegraph.
> // No allocation per frame; intended for subscription-time and gap recovery only.
> ```
>
> **Snapshot on subscribe:** when a consumer registers with the broker, the broker **synchronously delivers the current state of all open telegraphs** before the consumer processes any subsequent message. A subscriber is therefore never blind to an attack already in flight, and a revision gap is recoverable by one call rather than by waiting for the next phase.
>
> Two consequences stated rather than hidden: (a) the broker becomes **authoritative for current telegraph state**, not merely a relay — which is what "stateful" above means; (b) `GetOpenTelegraphs` is a query surface, so U-07 is no longer merely "event vs query" but "does the broker retain state", and I recommend **yes**.

### 4.2 What remains blocking, stated plainly

> **If the broker is not approved to retain state and expose `GetOpenTelegraphs`, then a missed `Retimed` is unrecoverable and C-05 remains blocked on U-07.** No consumer may recover fresh timing data from anywhere else, and this document does not claim otherwise.

The residual risk is bounded but real: in a same-process synchronous event bus a *subscriber* does not drop messages, so the gap case reduces to (i) late subscription — fixed by snapshot-on-subscribe — (ii) a future asynchronous transport, and (iii) any future coalescing or throttling of telegraph messages. Case (ii) and (iii) are why the query is worth having even though nothing in the slice requires them today.

**Corrected wording for `§3.3(c)4`:**

> A consumer that detects a revision gap **must not interpolate and must not extend a stale block**. It calls `GetOpenTelegraphs` once and adopts the returned block, or — if that surface is unavailable — treats the phase as **unknown** and raises a diagnostic. In the second case the gap is **unrecoverable**, the affected scheduling/UI/AI consumers are stale until the next message, and C-05 is blocked on U-07.

---

## 5. Item 4 — A2R-30: the test must compare against the authored window

A2 is right that `AsymmetricDilationTimestampComparability` as I accepted it compares producer-computed against consumer-computed — two implementations of the same formula. **Both wrong is a passing result.** Amended:

> **`TDD-Contract.Combat.AsymmetricDilationTimestampComparability` — amended (`PROPOSED / NOT RUN`).**
>
> **Setup:** authored parry window **0.20 s local**; producer `CustomDilation` 0.05; consumer 1.0; hit resolution frame-stepped deterministically.
>
> | # | Assertion | Would it catch A2R-22? |
> |---|---|---|
> | 1 | Producer-side computed local span == **authored 0.20 s** ± 1 frame | **yes** — 80.00 ≠ 0.20 |
> | 2 | Consumer-side computed local span == **authored 0.20 s** ± 1 frame | **yes** |
> | 3 | Shared-axis span == **4.00 axis-seconds** ± 1 frame tolerance | **yes** |
> | 4 | Producer-computed and consumer-computed spans agree with each other ± 1 frame | no (the original test) — **retained as a necessary but insufficient case** |
> | 5 | **Negative control:** a variant fixture that applies `axis / rate` instead of `axis × rate` **must fail assertions 1–3** | **this is the guard against a shared error** |
> | 6 | With a 10 s world pause mid-window, the reported remaining local time is unchanged across the pause | catches wall-clock aging (A2R-23) |
> | 7 | After a retime from rate 0.5 → 0.2 with 0.800 s local remaining, `EndAxis == AxisNow + 4.00` ± 1 frame | catches the §3.3(a)/(b) disagreement |
>
> Case 5 is the one that matters most: **a test that cannot fail is not evidence.** It is a test of the test, and it is the direct answer to the review instruction that producer/consumer agreement does not establish correctness.

**All proposed tests remain `NOT RUN`.** See §13.

---

## 6. Item 5 — the damage-request spelling: three names, no silent choice

### 6.1 The three spellings, with exact locations and lengths

I verified every row directly against the files rather than against either agent's transcription. Character counts are of the identifier only.

| Spelling | Characters | Where it appears, exactly |
|---|---|---|
| `FTDamageRequest` | **15** | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` (MEAD-C) **line 476** — `-> FTDamageRequest { InstigatorId, TargetId, …` |
| `FTDDamageRequest` | **16** | MEAD-C **line 478** — `-> ITDDDamageable::ApplyDamage(FTDDamageRequest)   [Core interface]` |
| `FTDDDamageRequest` | **17** | `docs/01_ARCHITECTURE/CODING_STANDARDS.md` **line 21** (the naming convention's own example); `A1-R1` §3.2; `A1-R2` §5.2; `A1-R3` §5.2 |

**MEAD-C names the same struct with two different lengths on consecutive lines (476 vs 478).** That is the underlying defect and neither agent may settle it by citation.

### 6.2 What the project's own convention predicts — and why that is not a decision

`CODING_STANDARDS.md` line 21 fixes the pattern **`FTDD<Thing>`** with `FTDDDamageRequest` as its worked example. `F` + `TDD` + `DamageRequest` = `FTDDDamageRequest`, 17 characters. The convention therefore **uniquely predicts** the long form, which is also the form both of my prior documents use consistently.

That is a *convention argument*, not a decision, and I am not treating it as one:
- `CODING_STANDARDS.md` is Agent 1's document and is itself `DESIGN_ONLY`, not TD-approved.
- MEAD-C, whatever its canonicality, contains the counter-evidence on its own line 476.
- `A1-R3` §5.2 **silently selected the 17-character form** by reproducing A2's erratum text without comment. A2 is right that this is the defect, and right that it is more insidious than a stated choice: **an accidental decision is still a decision.**

### 6.3 Request to the Technical Director

> **TD request (C-03).** Designate the authoritative spelling of the damage-request struct before the TD-09 erratum is issued. Three forms exist across 15, 16 and 17 characters; MEAD-C is internally inconsistent on consecutive lines (476 vs 478). Agent 1 has **no authority** to settle it and makes **no selection** here.
> Agent 1's **recommendation**, offered as input: **`FTDDDamageRequest`** (17), because it is the only form the project's own naming convention generates (`FTDD<Thing>`, `CODING_STANDARDS.md` line 21) and the form both prior submissions use. If the TD designates either shorter form, Agent 1 updates three documents and one coding-standard example; the cost is a find-and-replace, which is why it must be decided before any code exists.

**Until designated, `FTDDDamageRequest` is used in my documents provisionally and is not frozen.** Every use is labelled as provisional in §6.4.

### 6.4 Erratum addition — proposed wording, naming the decision rather than making it

> **Erratum addition (3) — type name.** The damage-request struct must be named consistently in the canonical architecture and in every contract document. MEAD-C §5.4 is internally inconsistent: line 476 uses `FTDamageRequest` (15 characters) and line 478 uses `FTDDamageRequest` (16), while `CODING_STANDARDS.md` line 21's `FTDD<Thing>` rule generates `FTDDDamageRequest` (17). **The spelling is a Technical Director decision recorded here explicitly, not a consequence of which diagram a drafter copied.** Agent 1 uses `FTDDDamageRequest` provisionally pending that decision.

---

## 7. Item 6 — complete MEAD-A mapping: seven tags and `Dead`

A2's finding is correct: `A1-R3` §4.3 mapped one of the seven retained tags. The cost they identified is precise — **TD-12 asks the TD to choose a canonical file without showing what the choice costs.** This section shows it.

### 7.1 The complete mapping

Classes: **RENAME** (same semantics, different namespace) · **SEMANTIC** (same concept, different granularity or axis; a design decision, not a rename) · **MISSING** (no equivalent; becomes a registry request) · **CONTRADICTION** (the mapping would change accepted behaviour).

| Tag (`A1-R3` §2.1) | MEAD-C §5.1 | MEAD-A equivalent (line) | Class | Consequence if MEAD-A is canonical |
|---|---|---|---|---|
| `Status.Invulnerable` | present, line 429 | `State.Combat.Invulnerable` (507), plus the scoped `State.Invulnerable.Dodge` (488) | **RENAME** (A offers two granularities) | Rename only; my dodge i-frame tag maps to A's scoped form, which is arguably a better model |
| `Status.Staggered` | present, line 429 | `State.Combat.Staggered` (507) | **RENAME** | Rename only — **this is the one row `A1-R3` §4.3 already had** |
| `Status.Parrying` | present, line 429 | `State.Combat.ParryWindow` (507) | **SEMANTIC** | A names the **window**; I name the **state**, which outlives the window and carries the input lock. Mapping requires either splitting my state into state + window, or redefining the tag as window-only. Not a rename |
| `Status.Cinematic` | present, line 429 | `State.Locomotion.Cinematic` (506) | **CONTRADICTION** | A puts it on the **locomotion axis**; M1 v1.4 treats `Cinematic` as a control state that outranks Stagger in the forced precedence and freezes a movement mode it does not replace. Mapping the precedence member into a locomotion enum would break the accepted precedence table |
| `Status.Attacking` | present, line 429 | **none** — `State.Combat` has no attacking value; `Ability.Attack.*` (509) names abilities, not a state | **MISSING** | Becomes a new-namespace request |
| `Status.Blocking` | present, line 429 | **none** — no block state anywhere in MEAD-A's vocabulary | **MISSING** | New-namespace request |
| `Status.Grabbed` | present, line 429 | **none** — `ledge-grab` (450) is a traversal action, not a victim state | **MISSING** | New-namespace request |
| `Status.Dead` (requested) | **absent** | **none as a tag.** `State.Combat.Downed` (507) exists; `Dead` appears only as an **enemy AI state** (§8.2, line 615) | **MISSING + SEMANTIC trap** | Still a registry request. `Downed` is **not** a substitute: downed implies survivable and revivable; `Dead` is terminal. Mapping dead → downed would be a correctness bug, not a rename |

**Count, matching A2's independently: under MEAD-A, two renames, one semantic change, one contradiction, and four requests — three tags plus `Dead` — against a document whose line 517 reads "Prohibition: no agent introduces a tag namespace."**

### 7.2 One correction to A2's table, and one addition of my own

| Item | A2's row | My verification |
|---|---|---|
| `Status.Dead` | "MEAD-A: enemy AI `Dead` only (line 615)" | **Confirmed** — line 615 is `ATDDEnemyBase`'s StateTree state list (`… Staggered, Dead`), an AI state machine, not a player tag. A2's characterisation is exact |
| `Status.Cinematic` | "a different axis" | **Confirmed and sharpened**: it is a *locomotion* value in A, and under M1 v1.4 `Cinematic` is a forced-precedence control state that can freeze a `MOVE_Falling` capsule. The two are not reconcilable by rename; that is why I classify it **CONTRADICTION** rather than SEMANTIC |

### 7.3 The point A2 makes that I had missed, recorded as theirs

Under MEAD-A, **three of my seven retained tags and `Dead` are four namespace requests against a document that forbids introducing namespaces.** In `A1-R3` I presented "yield to MEAD" as a resolution and the contingency as a convenience. Under one of the three candidates it is a **cost of four requests plus a contradiction in the precedence table** — and the TD was being asked to choose without that number. **A2's framing is better than mine and I adopt it.**

### 7.4 Beyond the required scope: C-01's capability vocabulary under MEAD-A

Discovered while completing the mapping, and it belongs to the same contingency. Not required by the nine items, offered because TD-12 affects C-01 too.

| My capability (C-01) | MEAD-A `ETDDTraversalAction` (line 450) | Class |
|---|---|---|
| `Vault` | `vault` | **RENAME** |
| `Drop` | `drop` | **RENAME** |
| `ClimbLadder` | `climb-lite` | **SEMANTIC** — a ladder and a "climb-lite" mantle-climb are different content |
| `LedgeShimmy` | `ledge-grab` | **SEMANTIC** — grab is entry; shimmy is lateral traversal along the ledge |
| `Mantle` | **none** | **MISSING** — a new capability, with its own montage requirement (already a C-1…C-5 content blocker) |

**Consequence:** under MEAD-A, C-01's five-capability set becomes two renames, two semantic remaps and one new capability — **not** the "compatible" state `A1-R3` §3.3 implied. The five-capability *model* survives; the vocabulary does not.

---

## 8. Item 7 — `Dead` fallback, stated as a consequence not a reassurance

`A1-R3` §2.2 said the fallback works "inside Agent 1". A2 is right that this is true for precedence comparison and false for everything else. Replacement text:

> **`A1-R4` §2.2 fallback (replaces `A1-R3`'s sentence).**
> If the registry declines `Status.Dead`, then **`Dead` is the only value in the `Dead > Cinematic > Stagger` precedence that is expressed as a non-tag control-state value**, and the precedence table is therefore **split across two representation types**: an enum value for `Dead`, tags for `Cinematic` and `Stagger`. Consequences, stated so nobody assumes a uniform table later:
> 1. **Arbitration is unaffected** — it compares priorities, not representations, and remains entirely inside Agent 1.
> 2. **Tag-driven consumers cannot ask "is the player dead" in the same vocabulary as "is the player staggered".** They must use C-02's `bAlive` (already published) or a phase condition. No tag is invented for it.
> 3. **The precedence table is not authorable as one data table.** It becomes one enum comparison plus two tag lookups, which is a **maintenance surface, not a correctness bug.**
> 4. Logs and telemetry name the state as `Dead` (the enum), not as a tag.

A2's word for this is "a maintenance surface, not a correctness bug", and it is the right way to describe it.

---

## 9. Item 8 — C-02 clarifications

### 9.1 A2R-28 / C-02-1 — `A1-INTERNAL` means **absent**, not marked

> **`A1-R4` §2.2 (C-02) — internal fields are not published.**
> `CameraForward`, `GroundSlopeDegrees` and `ActiveActionId` are **not members of the published snapshot struct at all**. They are values owned by internal components and are never copied into `FTDDPlayerContextFrame`. There is no "published but marked internal" tier: a field either exists in the shared struct or does not exist.
> Consequence: a consumer that references them **fails to compile**, which is the only form of this promise that can be tested. Re-exposing one later requires a C-02 revision, not a convenience change.

Three tests pin it: a reflection test asserting the shared struct has no property named `CameraForward`, `GroundSlopeDegrees` or `ActiveActionId`; a compile-fail fixture for each; and a test asserting the struct's property count equals the documented required set.

### 9.2 A2R-29 / C-02-2 — `CombatState` is authoritative; the tags are derived from it

The question was whether `CombatState` is (a) the coarse enum the tags refine, or (b) a projection of the tag set. **The answer is (a), with the derivation direction stated explicitly**, because "two overlapping representations" only stays safe if exactly one of them is authored.

**Authority chain — three links, one writer:**

```
UTDDCharacterStateMachine (control state)   ← the only writer, Agent 1
        │  projects to (lossy, published)
        ▼
ETDDCombatState  (coarse enum, AUTHORITATIVE for consumers)
        │  derived per the table below (one-way, on transition only)
        ▼
Status.* tags    (finer projection, DERIVED — never authored independently)
```

| `ETDDCombatState` | Derived status tags | Note |
|---|---|---|
| `None` | — | |
| `Approaching` | — | `bInCombat` carries engagement, per C-02 |
| `Telegraphing` | — | **Deliberate:** the windup has no status tag; C-05's telegraph stream is authoritative for it, and adding a `Status.Telegraphing` tag would duplicate C-05 |
| `Attacking` | `Status.Attacking` | |
| `Recovering` | `Status.Attacking` | Recovery is part of the attack; input lock still applies |
| `Blocking` | `Status.Blocking` | |
| `Parrying` | `Status.Parrying` | |
| `Dodging` | `Status.Invulnerable` (i-frames only) | No `Status.Dodging` exists in MEAD-C's seven; the dodge is visible as `ControlState == Dodge` |
| `Staggered` | `Status.Staggered` | |
| `Grabbing` | `Status.Grabbed` | |
| `Dead` | `Status.Dead` **if granted**; otherwise none | §8's fallback |

`Status.Cinematic`, `Status.Interacting`, `Status.Traversing`, `Status.Airborne` and `Status.LockedOn` are **not** combat states: they derive from the control state machine directly and never from `ETDDCombatState`.

> **Invariant (testable):** at any instant, the published tag set equals the table row for the published `CombatState` (plus the control-state-derived tags). `CombatState` is never derived from the tags, and no consumer can author either — there is no setter and no Blueprint-callable mutator. A consumer reading both can never observe them disagree.

**Where I decline A2's proposed wording:** their draft said "`CombatState` is the coarse projection of the actor's control state; the `Status.*` tags refine it." That is (a) and I accept its substance. I decline only the word "coarse": `ETDDCombatState` distinguishes `Telegraphing` from `Attacking` from `Recovering`, so it is not coarser than the tag set — it is *the authoritative one*, and the tags are its projection. Accepting "coarse" would imply the tags are the finer truth, which is exactly the second authority this clause prevents.

---

## 10. Item 9 — signature-status correction

### 10.1 The correction

`A1-R3` §7.4 wrote:

> "If A2 reviews it and states AGREE per contract against this blob, then C-01, C-02, C-04, C-05 and C-07 become candidates for `AGREED BY BOTH — PENDING TD`, and **C-03 and C-06 are already there.**"

**That sentence is withdrawn in full.** It contradicted `A1-R3` §7.3, in the same document, which correctly said that C-02, C-03 and C-06 are *not* bilaterally agreed merely because A2 has no technical objection. A2's rejection of it (§1.3 of their review) is correct and I accept it.

**Corrected statement:**

> **No contract in this series is bilaterally agreed, conditionally agreed, or "already there".** A2's "no remaining technical objection" and "would sign" statements are **review verdicts, not signatures**, and nothing in `A1-R1` … `A1-R4` should be read as recording a signature.
>
> Formal bilateral agreement requires, in this order: (1) both agents explicitly sign **the same exact version** — same blob, not "the latest"; (2) the TD reviews; (3) three items remain outside both agents' authority even after two signatures — TD-12 (canonical MEAD), the registry owner's namespace and `Status.Dead` decisions, and the save inventory for TD-13. **No combination of agent signatures can settle those.**

### 10.2 A2's dispositions of my review-of-their-review, recorded

| My claim in `A1-R3` | A2's disposition | Mine, now |
|---|---|---|
| §0.5 — their §6.6 tag rule is MEAD-A's, not MEAD-C's | **Accepted by A2** | No further action; verified by both sides |
| §0.4 — their `CarryState` finding was accurate against their submission and superseded by their withdrawal | **Accepted by A2 as a fair reading** | No further action |
| §7.4 — "C-03 and C-06 are already there" | **Rejected by A2** | **Accepted as correctly rejected** — withdrawn in §10.1 |

### 10.3 My verdicts on `A1-R4` itself

I do not sign my own document, and the following is not a signature:

| Contract | Position after `A1-R4` | What it still needs |
|---|---|---|
| C-01 | Text stable since `A1-R3`; `P3′` unchanged | A2 review of this blob |
| C-02 | Two clarifications added (§9); field set unchanged | A2 review |
| C-03 | Erratum additions (1)–(3); **spelling is a TD decision** (§6) | TD designation + A2 review |
| C-04 | `Dead` fallback stated (§8); mapping complete (§7) | Registry decision + A2 review |
| C-05 | **Formula corrected, aging defined, recovery mechanism proposed** (§2–§4) | TD on U-07 (broker state) + A2 review |
| C-06 | Text stable since `A1-R3` | A2 review |
| C-07 | Mapping complete (§7.1); conditionality unchanged | TD-12, registry, TD-13 |

---

## 11. What remains open

### 11.1 Unresolved items — updated from `A1-R3` §9.1

| ID | Item | Owner | Change since `A1-R3` |
|---|---|---|---|
| U-01 | `ETDDStaggerClass` vs bool vs tag mapping (TD-02) | TD | unchanged; A2 agrees with the preference |
| U-02 | Applied-event shared semantics + A1 sole publisher (TD-03) | TD | unchanged; A2 supports both |
| U-03 | Whether any durable reference points at a route key (TD-04) | TD | unchanged; `P3′` makes either answer implementable |
| U-06 | Clock coordinate and ownership (TD-06) | TD | **narrowed** — the formula is now correct and derived; what TD-06 approves is the axis design, not the arithmetic |
| U-07 | Late-subscriber surface / broker state | TD | **narrowed to one question**: may `UTDDTelegraphBroker` retain state and expose `GetOpenTelegraphs`? §4.1 proposes yes; §4.2 states what stays blocked if it is refused |
| U-08 | Does damage interrupt a hold? | TD/design | unchanged |
| U-09 | Completion-fact event shape | A1/A2 + TD | unchanged |
| U-10 | Canonical tag namespaces | Agent 3 | **narrowed** — the MEAD-A cost is now quantified (§7) |
| U-11 | Save inventory → retirement; interactable persistence | Agent 3 (save) | **narrowed** — and A2's three-answer framing adopted (§11.2) |
| U-12 | MEAD §5.4 erratum | TD | **narrowed** — both agents accept the text; needs the canonical file and the **spelling** (§6) |
| U-13 | Which MEAD is canonical (TD-12) | TD | unchanged; **now shown with its cost for C-01 and C-04** |
| U-14 | Is `Status.Dead` granted? | Agent 3 registry | unchanged; fallback fully specified (§8) |
| **U-15** *(new)* | **Authoritative spelling of the damage-request struct** | TD | **NEW** — three forms at 15/16/17 characters, MEAD-C inconsistent on consecutive lines (§6) |

### 11.2 C-07 needs three answers, and no ordering shortcuts them

A2's extension is adopted: **the save schema (TD-13), the namespace decision (TD-12), and a retirement policy are three separate answers, and any one alone unblocks nothing.** `A1-R3` §6 said the first does not unblock C-07 by itself; that was correct and incomplete.

### 11.3 Dependencies

**On Agent 2:** review of this blob. Nothing else outstanding — every A2 finding is answered here.

**On Agent 3/TD:** TD-12 (with §7's cost now visible), the registry's namespace list and `Status.Dead`, the damage-request spelling (U-15), U-07's broker decision, the save inventory (TD-13), and the TD-02 / TD-03 / TD-06 / TD-09 / U-08 rulings.

**On nobody in this session:** the Unreal toolchain (ADR-0012).

---

## 12. Per-contract verdicts against `A1-R3` v1.2 as reviewed

| Contract | A2's verdict on `A1-R3` | My position after `A1-R4` | Text changed by this document |
|---|---|---|---|
| C-01 | **AGREE** | Unchanged; `P3′` stable; capability contingency added at §7.4 | §7.4 only (contingency note, not the contract) |
| C-02 | AGREE WITH CONDITIONS | Both conditions answered | §9 |
| C-03 | AGREE WITH CONDITIONS | Condition answered as far as Agent 1 can; **spelling left to TD** | §6 |
| C-04 | AGREE WITH CONDITIONS | Both conditions answered | §7, §8 |
| C-05 | **DISAGREE** | **Defect corrected**; aging and recovery defined; test amended | §2, §3, §4, §5 |
| C-06 | AGREE | Unchanged | none |
| C-07 | AGREE WITH CONDITIONS | Condition answered; scope extended beyond requirement | §7 |

**Nothing here is a signature, and no contract's status changes because of a verdict in this table.** C-05's `DISAGREE` is not withdrawn by my correcting the defect — A2 must review the correction and state its own verdict on this blob.

---

## 13. Tests — executed versus proposed

### 13.1 Executed

**Contract acceptance tests executed in this task: 0. Written: 0. Suites run against Agent 1 code: 0 — no Agent 1 code exists.**

The only things executed in preparing this document were **arithmetic verifications** of the conversion, run as plain Python in this workspace and reported in §2.2:

| Verification | Result |
|---|---|
| `axis_span = 0.20 / 0.05` | **4.00** — matches the value the review request requires |
| `local_span = 4.00 × 0.05` | **0.20** — matches the authored window |
| `A1-R3` formula `4.00 / 0.05` | **80.00**, inflation **400×** = `1/0.05²` |
| Retime case: `0.4 + 0.800/0.2` | **4.40** — §3.3(b)'s behaviour, confirming A2's identification of the correct half |

That is arithmetic on constants, **not a test of an implementation**, and it is not evidence that any contract behaves correctly. A2's reported suites (337 world tests, 114 canon tests, 14 L0 checks, 13/13 evidence checks) are **theirs** at **their** commit; I did not rerun them and none tests Agent 1.

### 13.2 Proposed — `PROPOSED / NOT RUN`

| Suite | Contract | Cases | Change in `A1-R4` |
|---|---|---|---|
| `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics` | C-01 | 8 | — |
| `TDD-Contract.Traversal.WorldProjectionTotality` | C-01 | 2 | — |
| `TDD-Functional.Traversal.MarkerStreamingLifetime` | C-01 | 3 | — |
| `TDD-Contract.PlayerContext.ReadOnlyLifetimeAndStateSeparation` | C-02 | 10 | — |
| `TDD-Contract.PlayerContext.ConditionalFieldAbsence` | C-02 | 2 | — |
| **`TDD-Contract.PlayerContext.InternalFieldsAbsent`** | C-02 | **4** | **NEW** — reflection (no such property), three compile-fail fixtures, property-count equals the documented set |
| **`TDD-Contract.PlayerContext.CombatStateTagProjection`** | C-02 | **6** | **NEW** — for each `ETDDCombatState`, the published tag set equals the §9.2 table row; a consumer write attempt changes nothing; the two can never disagree |
| `TDD-Contract.Combat.SingleDamageApplicationAndEvent` | C-03 | 13 | — |
| `TDD-Contract.Combat.EventScopeMatrix` | C-03 | 6 | — |
| **`TDD-Contract.Combat.RequestTypeSpellingIsSingle`** | C-03 | **1** | **NEW** — after the TD designation, exactly one identifier resolves; the other two do not exist |
| `TDD-Contract.Combat.ForcedPrecedenceAndStaggerClassification` | C-04 | 15 | — |
| `TDD-Contract.World.StaggerRecoveryNotificationFiresOnEveryExit` | C-04 | 1 | — |
| **`TDD-Contract.Combat.DeadFallbackTwoRepresentations`** | C-04 | **3** | **NEW** — with `Status.Dead` absent, precedence still resolves; `bAlive` carries the deceased state; no tag is fabricated |
| `TDD-Contract.Combat.TelegraphWindowConsumerSemantics` | C-05 | 12 | — |
| `TDD-Contract.Combat.ClockDilationAlignment` | C-05 | 3 | — |
| `TDD-Contract.Combat.AsymmetricDilationTimestampComparability` | C-05 | **7** | **AMENDED (A2R-30)** — authored-window comparison plus the negative control; was 1 |
| `TDD-Contract.Combat.WindowRetimingOnDilationChange` | C-05 | 3 | — |
| **`TDD-Contract.Combat.RemainingLocalSecondsAging`** | C-05 | **5** | **NEW** — aging by axis×rate; constant across a 10 s pause; invalidated by a rate change; monotone non-increasing; never negative |
| **`TDD-Contract.Combat.TelegraphRevisionGapRecovery`** | C-05 | **4** | **NEW** — snapshot-on-subscribe delivers open telegraphs; gap → single `GetOpenTelegraphs` adoption; absent the query, diagnostic raised and no extrapolation; no interpolation ever |
| `TDD-Contract.Interaction.PlayerRoutingAndCancellation` | C-06 | 15 | — |
| `TDD-Contract.Core.Agent1IdAndTagRegistry` | C-07 | 10 | — |
| `TDD-Contract.Core.StatusDeadRegistryRequest` | C-07 | 2 | — |
| **`TDD-Contract.Core.MeadContingencyMap`** | C-07 | **4** | **NEW** — data-driven: every retained tag has a class (rename / semantic / missing / contradiction) per candidate MEAD; a tag appearing in two classes fails |

**Total: 23 suites, 139 cases, 0 executed.** No test in any prior version of this series has been run either.

---

## 14. Publication

| Field | Value |
|---|---|
| Document | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md` |
| Version | 1.3 (`A1-R4`) |
| Branch | `arena/3bc206a0-tdd` |
| Publishing commit | `PUB_COMMIT` |
| `A1-R4` blob | `PUB_BLOB` at that commit — the two rows naming the commit and the blob are the only later change, exactly as `A1-R2` §10 and `A1-R3` §10 did |
| Predecessor | `70db9665b67723a526a6d40fa71ec832f1a95498` (`A1-R3`), on this same branch |
| `A1-R3` (reviewed) | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md`, blob `109331f36eddce…` at `70db966` and **still `109331f3…` now** — **unmodified by this task** |
| `A1-R2` | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V2.md`, blob `f578fe6`→`bdcd0fed…` (reviewed) then `b9ab305`→`5ee27694…` (provenance line) and **still `5ee2769…` now** — **unmodified by this task** |
| `A1-R1` | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md`, blob `25ab47c263db3a9f…` at `97828db` and **still `25ab47c2…` now** — **unmodified by this task** |
| Agent 2 review | `4c0998004f8870fff9a6022ada0ceb2b7eb3de8e` — present in this clone, read in full |
| MEAD-A / MEAD-B / MEAD-C | **Read only.** No file moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| Tags registered | **None.** `Status.Dead` remains a request (§7.1, `A1-R3` §2.2) |
| Erratum issued | **None.** Additions (1)–(3) are proposed text for the TD (§6.4) |
| Status | `DESIGN_ONLY`; proposals `PROPOSED — NOT FROZEN`; tests `PROPOSED / NOT RUN` |
| C++ / Core types / project / merge / M0 | **None** |

### 14.1 Change log

| Version | Date | Effect |
|---|---|---|
| `A1-R1` v1.0 | 2026-11-16 | Initial submission against v1.1 |
| `A1-R2` v1.1 | 2026-11-16 | Acknowledged TD v1.2; six contracts revised; TD-01…TD-09 answered |
| `A1-R3` v1.2 | 2026-11-17 | `P3′`; complete status inventory and the `Status.Dead` request; Option A+ clock; yield clauses conditional on TD-12; the §5.4 erratum; per-contract verdicts |
| `A1-R4` v1.3 | 2026-11-17 | **C-05 conversion corrected** with the derivation stated, the required example verified (4.00 axis / 0.20 local), and the `§3.3(a)`/`§3.3(b)` halves reconciled; `RemainingLocalSeconds` aging defined for all five conditions; retime recovery defined via broker state **and** the residual blocker retained; `AsymmetricDilationTimestampComparability` amended to compare against the authored window with a negative control; the three request-struct spellings located exactly and left to the TD; the MEAD-A mapping completed for all seven tags plus `Dead` (two renames, one semantic change, one contradiction, four requests) and extended to C-01's capabilities; the `Dead` two-representation fallback stated; `A1-INTERNAL` clarified as absent-not-marked and `CombatState` as authoritative with derived tags; the §7.4 signature overreach withdrawn. 23 of 25 review findings accepted (2 answered questions, 2 accepted in both offered ways), 1 noted, 0 rejected, 0 contested |

### 14.2 Version identity — verified by ancestry and by content, not transcribed

I checked the branch's history before writing the SHA rows above instead of transcribing remembered SHAs, and both checks agree:

| Check | Result |
|---|---|
| `git rev-parse 70db966:docs/…_V3.md` | `109331f3…` — **identical to the file in this workspace**, so the text A2 reviewed at `4c09980` is byte-for-byte the text I corrected, with no drift |
| `git rev-parse f578fe6:docs/…_V2.md` | `bdcd0fe…` — the blob `A1-R3` §0.1 recorded as reviewed; `b9ab305` then added the single provenance line, giving `5ee2769…`, which is what still hashes now |
| `git rev-parse 97828db:docs/…_V1.md` | `25ab47c2…` — unchanged today |
| `git rev-parse be0badf:docs/…_V3.md` | `4175b7f8…` — the pre-provenance blob; `70db966` added `A1-R3`'s own publishing line, which is the version A2 reviewed |
| Working-tree blobs after my edits | `25ab47c2…`, `5ee2769…`, `109331f3…` — **all three unchanged by this task** |

One procedural note, recorded because it is the kind of thing that produces false provenance claims: my workspace's clone was created from `main`, which sits at `5e3d1da` ("Initial commit") and does **not** contain this branch's history. Before pushing I fetched `arena/3bc206a0-tdd` and confirmed every commit above is reachable on it, so the SHAs in this section are verified facts rather than recollections. If a reader cannot reach them, the problem is their clone, not the branch.

`A1-R1`, `A1-R2` and `A1-R3` sit on this branch already and are **not touched by this commit**; the commit that publishes `A1-R4` adds one file and edits two index rows.
