# AGENT 2 — FORMAL REVIEW OF AGENT 1 REVISION `A1-R4` v1.3

**Document ID:** `TDD-A2-REVIEW-A1R4-001`
**Version:** 1.0
**Date:** 2026-11-17 UTC
**Author:** Agent 2 — World Structure and Level Architecture

**Reviewing:** `TDD-A1-CONTRACT-RESPONSE-004` **v1.3 (`A1-R4`)**
**Final branch head:** `142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6`
**Exact reviewed blob:** `2cc548faf86cb9b30cd2e26386fc672edbdd9f75` — `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md`
**Blob verified before reading:** `git rev-parse origin/a1branch:docs/…V4.md` → `2cc548f…` ✅
**Against:** my `A2-C01…C07-1.0`, commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644`
**Governing decisions:** `TDD-TD-INT-001` v1.2, commit `e121bbbf09562e3cba0efe81aad971809685db23`
**Reconciliation:** `TDD-INT-RECON-001` v3.0, commit `98399af12bf234259143d5b85a1634c48f9eef29`
**My prior review:** `TDD-A2-REVIEW-A1R3-001` v1.0, commit `4c0998004f8870fff9a6022ada0ceb2b7eb3de8e`

**Status:** `DESIGN_ONLY` — **PENDING TD DECISION**. No C++, no Core type, no Unreal project, no API
freeze, no contract promotion, no merge, no canonical MEAD selected, no tag registered, no erratum
issued, no change to `DECISIONS.md`, no M0 claim.

> Every shape referenced here is `PROPOSED — NOT FROZEN`.
> **Signed this review: 3 of 7.** See §1.3 — this is the first review in the series where I sign
> anything, and §1.3 states exactly which blobs and why.

---

## 0. Reading notes

### 0.1 The document under review, and one correction to my own prior review

`A1-R4` is 557 lines and corrects **all nine** of my numbered asks. It does so by replacing clause
text with derived arithmetic rather than by asserting agreement, which is the right response to a
review that found an arithmetic defect.

**`A1-R4` §1 makes one correction to me and it is correct:** my `A1-R3` review §11 was headed
**"Ten asks"** and listed **nine** identifiers, `A2R-22` … `A2R-30`. I verified this against my own
document — the heading says ten, the table has nine. `A1-R4` says it "assume[s] the count is a slip
in their text, not a missing item." **The count is a slip and there is no missing item.**
`A1-R4` guessed correctly, but it should not have had to guess: a numbering error in a review is
exactly the kind of thing a recipient must be able to resolve by counting, and mine did not count.
That is my sixth error in this series and the second found by Agent 1 (§11.3).

### 0.2 What `A1-R4` changed, by my finding IDs

| My ask | `A1-R4` disposition | Adequate? |
|---|---|---|
| **A2R-22** multiply not divide, with derivation | §2.1 derives from unchanged definitions; §2.3 gives both directions as normative text | **Yes — fully resolved** (§3) |
| **A2R-23** aging rule for `RemainingLocalSeconds` | §3 new clause `§3.3(e)` with a formula and an eight-row condition table | **Yes** (§4) |
| **A2R-24** U-07 blocking or define recovery | §4 defines the broker **and** retains the residual blocker | **Partly** — see §5.4 |
| **A2R-25** name the spelling as a TD decision | §6 locates all three, selects none, asks TD, adds U-15 | **Yes** (§6) |
| **A2R-26** complete MEAD-A mapping | §7 all seven tags + `Dead`, four classes, plus C-01 capabilities | **Yes, and beyond scope** (§7) |
| **A2R-27** `Dead` is the only non-tag precedence value | §8 four numbered consequences | **Yes** (§7.4) |
| **A2R-28** `A1-INTERNAL` = absent, not marked | §9.1 makes it a compile-fail promise | **Yes** (§8) |
| **A2R-29** `CombatState` authority direction | §9.2 answers (a) with an invariant, declines the word "coarse" | **Yes** (§8) |
| **A2R-30** amend the asymmetric test | §5 seven assertions plus a negative control | **Yes, and better than I asked** (§3.4) |

**Nine of nine addressed.** Five of the six conditions I recorded in my `A1-R3` review are closed
outright; C-05's is closed on the arithmetic and replaced by a different, smaller condition.

### 0.3 What I verified independently, and the two claims that did not survive

The instruction is not to accept conclusions because they accept my findings. I re-derived every
technical claim in `A1-R4` from the source files rather than from its prose. Twenty-five checks,
§12.1. **Twenty-four passed and one failed on a line-number citation.** Three things are worth
separating at the top:

1. **`A1-R4`'s arithmetic is correct, and I checked it against my own derivation rather than its
   result.** §3.1 shows the derivation, §12.1 checks it, and I confirm the 4.00 axis-seconds /
   0.20 local / 400× figures independently.

2. **A precision concern I raised against it did not hold up, and I am discarding it rather than
   reporting it.** I suspected `float RemainingLocalSeconds` would lose resolution against a
   double-valued axis at low dilation. Computed properly, the float32 ULP for a 0.20 s window is
   `1.5e-8 s` — about `9e-5` of a 60 fps frame. **It is not a defect and I am not raising it**
   (§3.5). Recording the discards is as important as recording the findings; a review that reports
   only its hits is not reproducible.

3. **One line-number citation is off by one:** `A1-R4` §7.1 cites MEAD-A **505** for
   `State.Locomotion.Cinematic`; it is **506**. Harmless, corrected in §7.2, and notable only
   because it is the same class of error as mine in v1.1 (`A1-R3` §0.5) — citation drift, not
   reasoning error.

### 0.4 Where this review lands

My `A1-R3` review ended in **DISAGREE on C-05** with a blocking arithmetic defect. **That defect is
fixed and C-05 is now signable**, on the arithmetic. What remains is a smaller and differently
shaped condition: the broker mechanism (§5) introduces a **Core-owned stateful authority** that is
not Agent 1's to take unilaterally, and it has four unresolved concurrency gaps.

So this review signs **three contracts** — C-01, C-02, C-06 — and withholds signature on four for
reasons that are now mostly **not** technical defects in Agent 1's work.

---

## 1. Verdicts and signature status

### 1.1 The seven verdicts

| Contract | My `A1-R3` verdict | **Verdict on `A1-R4`** | Change |
|---|---|---|---|
| **C-01** | AGREE | **AGREE** | unchanged — `P3′` stable, no new conflict (§9) |
| **C-02** | AGREE WITH CONDITIONS | **AGREE** | **condition resolved** (§8) |
| **C-03** | AGREE WITH CONDITIONS | **AGREE WITH CONDITIONS** | spelling correctly deferred to TD (§6) |
| **C-04** | AGREE WITH CONDITIONS | **AGREE WITH CONDITIONS** | mapping complete; registry still open (§7) |
| **C-05** | **DISAGREE** | **AGREE WITH CONDITIONS** | **defect fixed**; broker adds a condition (§3–§5) |
| **C-06** | AGREE | **AGREE** | unchanged — no new conflict (§9) |
| **C-07** | AGREE WITH CONDITIONS | **AGREE WITH CONDITIONS** | cost now quantified; TD-12 still open (§7) |

| | Count | Contracts |
|---|---|---|
| **AGREE** | **3** | C-01, C-02, C-06 |
| **AGREE WITH CONDITIONS** | **4** | C-03, C-04, C-05, C-07 |
| **DISAGREE** | **0** | — |

**Nothing is DISAGREE.** The one DISAGREE in the series is resolved on the clause text, and I say
so plainly rather than letting it stand for the sake of a consistent shape.

### 1.2 Resolved findings — the full list

| Finding | Where it was raised | Resolution in `A1-R4` | Verified |
|---|---|---|---|
| C-05 §3.3(a) inverted conversion | my `A1-R3` §7.3 | §2.1–2.4, both directions stated, derivation normative | ✅ §3 |
| `§3.3(a)`/`§3.3(b)` mutual inconsistency | my `A1-R3` §7.3 | §2.4 reconciles them as one arithmetic in two directions | ✅ §3.3 |
| `RemainingLocalSeconds` aging undefined | my `A1-R3` §7.5 | §3 `§3.3(e)` formula + eight conditions | ✅ §4 |
| U-07 left blocking with no mechanism | my `A1-R3` §7.6, A2R-24 | §4.1 broker + §4.2 retained residual blocker | ✅ §5 (with new gaps) |
| Test compares two implementations, not truth | my `A1-R3` §7.8 | §5 assertions 1–3 against the authored window | ✅ §3.4 |
| No guard against a shared error | my `A1-R3` §7.8 | §5 assertion 5, the negative control | ✅ §3.4 |
| Silent selection of a type spelling | my `A1-R3` §5.3, C-03-1 | §6 all three located, none selected, U-15 raised | ✅ §6 |
| MEAD-A map covered 1 of 7 tags | my `A1-R3` §4.3, C-04-2 | §7.1 all seven + `Dead`, four classes | ✅ §7 |
| `Dead` fallback presented as reassurance | my `A1-R3` §4.2, C-04-1 | §8 four explicit consequences | ✅ §7.4 |
| `A1-INTERNAL` ambiguous | my `A1-R3` §6.3, C-02-1 | §9.1 absent-not-marked, compile-fail | ✅ §8 |
| `CombatState` vs tag authority | my `A1-R3` §6.4, C-02-2 | §9.2 authority chain + invariant | ✅ §8 |
| `A1-R3` §7.4 signature overreach | my `A1-R3` §1.3 | §10.1 withdrawn in full | ✅ §10.2 |
| My "ten asks" count error | — (found by A1) | note in `A1-R4` §1 | ✅ §0.1 |

### 1.3 Signature status — explicit, per contract

The instruction is explicit that a verdict is not a signature, and `A1-R4` §10.1 correctly states
that no contract in this series is bilaterally agreed. **I am signing three contracts now, and this
is the first signature I have given in the series.**

> **Signature declaration — Agent 2 — re `TDD-A1-CONTRACT-RESPONSE-004` v1.3, blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75`, branch head `142cabd`**

| Contract | Signature | Conditions attached |
|---|---|---|
| **C-01** | **SIGNED — `AGREE`, no conditions** | none |
| **C-02** | **SIGNED — `AGREE`, no conditions** | none |
| **C-03** | **NOT signed** | C-03-1: the struct spelling is a TD decision (U-15) and must be designated before the TD-09 erratum is issued |
| **C-04** | **NOT signed** | C-04-1: `Status.Dead` grant is a registry decision; C-04-2: §7.1's classification must be carried into the registry request |
| **C-05** | **NOT signed** | C-05-3: the broker raises a Core-ownership question that is not Agent 1's to settle (§5.3); C-05-4: four concurrency gaps (§5.4) |
| **C-06** | **SIGNED — `AGREE`, no conditions** | none |
| **C-07** | **NOT signed** | C-07-1: TD-12 canonical file; C-07-2: TD-13 save inventory; the namespace owner's decisions — all three outside both agents' authority |

**Why I sign C-01, C-02 and C-06 and not the other four, stated precisely:**

- **C-01, C-02, C-06 have no open condition that either agent can settle and none that a TD ruling
  would rewrite.** C-01's `P3′` was written so TD-04 is a decision *inside* an agreed clause —
  that was its design intent and it worked. C-02's two clarifications are answered. C-06 was
  untouched and had no condition.
- **C-03, C-04, C-07 are blocked on decisions outside Agent 1's and my authority.** A signature from
  me would not unblock them and would misrepresent my position as "the text is final" when the text
  contains a placeholder for a TD decision.
- **C-05 is not signed for a different reason, and it is not the arithmetic.** The arithmetic is
  correct. The broker proposal in §4.1 asserts **stateful authority inside Core** (§5.3), which is
  Agent 3's and the TD's to grant, and it leaves four concurrency gaps open (§5.4). Signing C-05
  would sign a mechanism whose owner has not agreed to own it.

**No bilateral agreement is claimed anywhere in this document.** Three signatures from one agent on
one blob is not agreement. Under the sequence `A1-R4` §10.1 correctly states — both agents sign the
same exact blob, then TD review — the position today is:

| Contract | Agent 2 | Agent 1 | TD | Status |
|---|---|---|---|---|
| C-01 | **SIGNED** | not signed by A1 (A1 does not sign its own document) | not reviewed | **1 of 3** |
| C-02 | **SIGNED** | " | " | **1 of 3** |
| C-06 | **SIGNED** | " | " | **1 of 3** |
| C-03, C-04, C-05, C-07 | not signed | " | " | **0 of 3** |

**Not one contract reaches two signatures, and I am not going to describe three of seven as
progress toward agreement.** It is progress toward a signature, which is a different and smaller
thing.

---

## 2. Test status, stated before any finding

**Executed contract acceptance tests: 0. Written against Agent 1 code: 0.** No clock, arbiter,
telegraph, broker or registry exists in this workspace, and no Unreal project exists (ADR-0005).

**What I executed:** 25 document and arithmetic checks (§12.1) plus the repository suite (§12.2).
These evaluate **formulas and file contents**, not behaviour. Where a check produced a negative
result I discarded it rather than reporting it as a finding (§3.5).

**What I did not do:** I did not rerun any `A1-R4` suite — none exists to run. I did not claim
Agent 1 or Agent 3 ran mine. `A1-R4` §13.1 accurately attributes my figures to me at my commit and
I return the same.

---

## 3. A — C-05 clock conversion and arithmetic

### 3.1 The derivative relationship, derived independently

I re-derived from the definitions rather than reading `A1-R4` §2.1's result:

```
Axis  (shared):   d(Axis)/d(wall)  = PrimaryDilation (P)
Local_e:          d(Local_e)/d(wall) = P × CustomDilation(e) (C)

⇒ d(Local)/d(Axis) = (P·C) / P = C = ProducerRate

⇒ ΔLocal = ΔAxis × ProducerRate        (axis → local: MULTIPLY)
⇒ ΔAxis  = ΔLocal / ProducerRate       (local → axis: DIVIDE)
```

**`A1-R4` §2.1 states exactly this and `P` cancels.** The cancellation is the whole argument:
because primary dilation appears in *both* numerators it drops out of the derivative, which is why
the axis is comparable across entities while the conversion between the two depends only on the
producer's own `CustomDilation`. **`A1-R4`'s derivation is correct and I confirm it independently.**

**One thing `A1-R4` does not say that I want on the record**, because it is the property that makes
the axis safe: `P` cancels **only because it is applied to both clocks**. If a future revision moved
primary dilation out of the local clock — a plausible "the montage should not slow under global
slow-mo" change — the derivative becomes `d(Local)/d(Axis) = C` still, but `d(Local)/d(wall)` would
change and every `RemainingLocalSeconds` would be wrong by `P`. **The cancellation is a
consequence of the definition, not an independent invariant.**

### 3.2 The required example, recomputed

| Quantity | Relation | Value | `A1-R4` claims | Agreement |
|---|---|---|---|---|
| Authored local window | given | 0.20 s | 0.20 s | ✅ |
| Shared-axis span | `0.20 / 0.05` | **4.0000** | 4.00 | ✅ |
| Local recovered | `4.00 × 0.05` | **0.2000** | 0.20 | ✅ |
| `A1-R3` divide form | `4.00 / 0.05` | **80.0000** | 80.00 | ✅ |
| Inflation | `80.00 / 0.20` | **400** | 400 = `1/rate²` | ✅ |

All five reproduce. **I also ran the mutual-inverse check across four rates** (`1.0, 0.5, 0.2, 0.05`)
— `local → axis → local` returns `1.000000` at every rate to 1e-12. **The two conversions `A1-R4`
now states are genuine inverses**, which is the property `A1-R3` lacked.

### 3.3 §3.3(a) and §3.3(b) reconciled — confirmed

`A1-R4` §2.4 claims the retime rule and the corrected conversion are "the same arithmetic applied in
the two directions." Verified:

| Path | Arithmetic | Result |
|---|---|---|
| §3.3(b) retime, `EndAxis = AxisNow + RemainingLocal / rate` | divide | `0.4 + 0.800/0.2` = **4.4000** |
| §2.3 inverse row, `axis_span = local_span / ProducerRate` | divide | identical form |

**They agree, and `§3.3(b)` was always the correct half** — which is what my `A1-R3` §7.3 claimed and
`A1-R4` §2.2 now confirms from its own side.

### 3.4 The amended test — does it catch the original defect?

`A1-R4` §5 asserts seven things. I checked each against the specific error it is supposed to catch:

| # | Assertion | Catches `A1-R3`'s divide form? | Catches wall-clock aging? | Catches §3.3(a)/(b) split? |
|---|---|---|---|---|
| 1 | Producer local span == **authored** 0.20 s | **yes** — 80.00 ≠ 0.20 | no | no |
| 2 | Consumer local span == **authored** 0.20 s | **yes** | no | no |
| 3 | Axis span == 4.00 | **yes** | no | no |
| 4 | Producer and consumer agree with each other | **no** — both wrong passes | no | no |
| 5 | **Negative control**: `axis / rate` fixture must fail 1–3 | **yes, and this is the guard** | no | no |
| 6 | 10 s pause leaves remaining unchanged | no | **yes** | no |
| 7 | Retime 0.5→0.2 gives `EndAxis == AxisNow + 4.00` | no | no | **yes** |

**Assertion 5 is the correct answer to the point I made and it is better than what I proposed.** My
A2R-30 asked only that assertions compare against the authored window. `A1-R4` additionally adds a
fixture that *must fail* — a test of the test. **A test suite that cannot fail its own deliberately
broken fixture is not evidence, and `A1-R4` states that principle explicitly.**

**One gap in the suite that I record rather than demand:** assertion 5 uses `axis / rate` as its only
broken fixture. The original defect also had a second form — **using the consumer's own
`CustomDilation` instead of `ProducerRate`** — which at producer 0.5 / consumer 1.0 doubles the
window. Assertions 1–3 would catch it, but assertion 5's negative control would not, because that
fixture is correct arithmetic with the wrong rate. **Suggest §5 case 5 becomes two fixtures: wrong
operator, and wrong rate.** Not a condition; the existing assertions already cover the outcome.

### 3.5 Checked and discarded — the precision concern does not hold

I suspected `float RemainingLocalSeconds` (from `A1-R3` §3.2, unchanged by `A1-R4`) would lose
resolution as `R(t)` counts down against a double axis. **Computed properly, it does not:**

| `R0` | float32 ULP | as % of a 60 fps frame | as % of a 240 fps frame |
|---|---|---|---|
| 1.00 s | 1.19e-07 s | 7.2e-04 % | 2.9e-03 % |
| 0.20 s | 1.49e-08 s | 8.9e-05 % | 3.6e-04 % |
| 0.05 s | 3.73e-09 s | 2.2e-05 % | 8.9e-05 % |

I also checked the double axis's own accumulation over a long session — after 8 hours at 240 fps the
ULP is `3.6e-12 s`, six orders of magnitude below one frame increment. **Neither is a defect.**

**My first pass at this computation used double-precision ULP and produced a badly wrong
conclusion.** I caught it before writing it up. Recording the discard because a review that lists
only the concerns that survived implies it had none that did not.

**Remaining dimensional/sign/boundary audit: no errors found.** Units are consistent
(axis-seconds vs local seconds, both `s`); every conversion is positive (rates are in `(0,1]` so no
sign flip); the half-open interval `[WindupEndAxis, ActiveEndAxis)` is unchanged and correct.

**One boundary note, not an error:** §3 says the phase is complete "when `R(t) = 0`, equivalently
when `Axis(t) − AxisNow ≥ R0 / ProducerRate`." Both predicates are equivalent, but `R(t) = 0` holds
over the **entire** interval `[threshold, ∞)`, not just at the crossing. A test asserting "the frame
at which `R` first equals zero" will match many frames unless it uses a tolerance or tests the
inequality. Worth one sentence in the clause so the test is written against the inequality.

### 3.6 C-05 arithmetic verdict

**Resolved.** The blocking defect is corrected, the derivation is now part of the contract, the two
halves agree, and the amended test would have caught the original error. **My `A1-R3` DISAGREE on
§3.3(a) is withdrawn in full** — not because `A1-R4` accepted it, but because I re-derived the
correction and it is right.

---

## 4. B — `RemainingLocalSeconds` lifecycle

### 4.1 The rule as stated, and the eight conditions

`A1-R4` §3 defines `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` and tabulates eight
conditions. I checked each against the formula rather than against the prose:

| Condition | `A1-R4` claim | My check | Verdict |
|---|---|---|---|
| **Normal gameplay**, rate constant | linear in axis elapsed | ✅ `R` is affine in axis with slope `−rate` | **correct** |
| **World pause** | axis does not advance → `R` constant | ✅ verified: after a 10 s pause `R` is unchanged at `0.500` | **correct** |
| **Primary dilation changes** | no message required; formula unaffected | ✅ — see §4.2 | **correct, with a caveat** |
| **Producer `CustomDilation` changes** | formula invalid at once; `Retimed` same frame | ✅ — formula's `rate` term is stale otherwise | **correct** |
| **`Retimed` received** | restart from new `AxisNow`/`R0` | ✅ — replacement, not accumulation | **correct** |
| **Revision gap** | undefined; must not interpolate or extrapolate | ✅ conservative | **correct** |
| **Phase change** | new `R0`, revision increments | ✅ | **correct** |
| **Telegraph closed** | undefined and meaningless; discard | ✅ | **correct** |

**Two supporting rules also verify:** monotone non-increasing over 20 steps (checked numerically) and
never negative (guaranteed by `max(0, …)`).

### 4.2 The pause and primary-dilation claims are correct, and the reason is worth stating

The formula depends on exactly three quantities: `R0`, `Axis(t)`, and `ProducerRate`. **A primary
dilation change alters `d(Axis)/d(wall)` and leaves `d(Local)/d(Axis)` untouched**, so no field in
`R(t)` needs updating and no message is required. **That is correct and it is not obvious** — the
natural mistake would be to emit a `Retimed` on a global slow-mo, which would be noise.

Similarly a pause stops `d(Axis)`, so `R` is constant. **Both are consequences of putting primary
dilation inside the axis and per-entity dilation outside it**, which is the decision I endorsed in my
`A1-R3` §7.2 and which now pays off twice.

### 4.3 The hard case the instruction asks about: `CustomDilation` changes mid-telegraph

**This is the condition that could break coherence, and it does not — but only because `A1-R4`
requires same-frame re-emission, which is a stronger guarantee than it looks.**

| Step | State |
|---|---|
| `t0` | `Opened`, `rate = 0.5`, `R0 = 1.0`, `AxisNow = 0`, reverse `10.0` |
| `t1` (axis 2.0) | Producer's dilation retargets to `0.2` |
| **same frame** | `Retimed`, `rev 2`, `AxisNow = 2.0`, recomputed `R0`, `rate = 0.2` |
| consumer adopts | correct from `t1` forward |

**The coherence argument:** between `t0` and `t1` the formula is valid with `rate = 0.5`. From `t1`
forward it is valid with `rate = 0.2`. **There is no interval over which both are true and no
interval covered by neither**, *provided* the `Retimed` is emitted in the same frame as the change.
`A1-R4` states "in the same frame" and labels the old formula "invalid at once."

**The failure mode if that promise is broken** is worth documenting because `A1-R4` does not:
a consumer that does not see `Retimed` keeps aging at `rate = 0.5` while the truth is `0.2`, so it
reports the window **closing 2.5× too early** — and it will be *silently* consistent with itself
until the next message. That is §5's revision-gap case, and it is why the gap rule matters.

### 4.4 What I would add

**Condition C-05-5 (minor, wording).** `§3.3(e)` should state that the same-frame guarantee is a
**producer obligation**, not a consumer assumption — i.e. "a consumer must not observe a frame in
which `Axis(t) > AxisNow` under an old `ProducerRate` that the producer has already changed." As
written, the consumer has no way to detect a violation, so the obligation is unenforceable except by
the producer's own conformance test.

---

## 5. C — the broker and recovery mechanism

### 5.1 What is proposed

`A1-R4` §4.1 proposes `UTDDTelegraphBroker` (Core) as **stateful for open telegraphs**, retaining
the current timing block and phase per open `AttackInstanceId`, exposing
`GetOpenTelegraphs`, and delivering a **snapshot on subscribe** before any subsequent message.

**The mechanism does resolve the problem I raised.** My `A1-R3` §7.6 modelled a stale consumer
closing at axis 2.0 a window running to 16.4, with "treat the phase as unknown" as the only
sanctioned response. A query surface fixes that: one call returns the live block and the consumer
adopts it. **U-07 is genuinely narrowed from an open design question to a single yes/no.**

### 5.2 The mechanism is sound in the single-threaded case, and I recommend it — with four conditions

**I recommend accepting the broker proposal.** But I am not signing it, because as specified it has
four gaps that would each produce a shipped bug:

### 5.3 Gap 1 — the broker takes **Core** authority that is not Agent 1's to grant

`A1-R4` §4.1 puts `UTDDTelegraphBroker` in **Core** and states the consequence explicitly: it
"becomes **authoritative for current telegraph state**, not merely a relay."

**A relay is a message-pipeline component. An authoritative state holder in Core is a different
thing**, and the difference matters because it decides who owns telegraph truth:

- Today, per `A1-R3` §3.2, the **producer** owns the timing block and publishes it. Consumers cache.
- Under §4.1, the **Core broker** owns the current block and consumers query it.

**That is a change of owner, not an addition of a query.** And Agent 1 has already conceded, in
`A1-R2` §11, exactly this class of point about Core:

> "Core placement of every struct I request (**I request fields, I do not author types**)"

and of the clock itself:

> "a Core-owned `UTDDGameplayTimeSubsystem` (**Agent 3**)"

**So `A1-R4` §4.1 proposes an architectural authority inside Core while `A1-R2` §11 correctly says
Agent 1 does not author Core types.** That is not a contradiction Agent 1 made carelessly — §4.1
does flag that the broker "becomes authoritative" — but it is an **authority transfer stated inside a
C-05 proposal** rather than escalated as its own decision.

**Condition C-05-3.** The broker's statefulness must be raised as a **Core-ownership request to
Agent 3 and the TD**, separate from U-07's "event vs query" question. Proposed wording:

> **Core ownership request (Agent 3 / TD).** `UTDDTelegraphBroker` is proposed as a **stateful
> authority for open telegraph timing** in `TDDCore`. This is not a query surface added to a relay:
> it moves custody of the current timing block from the producing ability system to Core. Agent 1
> requests the placement and does not create the type. If the request is declined, C-05 reverts to
> the §4.2 residual state and remains blocked on U-07, exactly as if it had never been answered.

**This is the reason C-05 is not signed**, and it is the cleanest framing of it: *the arithmetic is
mine to agree with and I have; the Core authority is not Agent 1's to give and not mine to grant.*

### 5.4 Gaps 2–4 — concurrency and lifecycle, each a shipped bug

**(a) No adoption-ordering rule between snapshot and message.** §4.1 requires the snapshot to be
delivered "before the consumer processes any subsequent message" — that is an ordering of *delivery*.
It does not state an ordering of *adoption*. If a `Retimed` (rev 3) is dispatched in the same frame
before the snapshot is written, and the snapshot then carries rev 4, a consumer that adopts whatever
it received last is correct; one that adopts the snapshot unconditionally over a newer message is
wrong; and one that ignores snapshots with `revision ≤ current` is correct. **The contract does not
say which, and two conforming consumers differ.**

**Condition C-05-4a.** "A consumer adopts a timing block only if its `TimingRevision` is **strictly
greater** than the currently held revision. A snapshot whose revision is ≤ the held revision is
discarded. This applies to messages and snapshots identically, so the two cannot conflict."

**(b) No at-most-once phase-entry semantics.** The snapshot delivers "current phase = `Active`". An
`Opened`/`PhaseChanged` for that same phase may also be delivered to the same consumer. **A consumer
with an on-phase-enter hook — a boss starting an attack-reaction timer, a UI presenting a parry
prompt — will fire it twice.** `A1-R4` §3's table says a phase change increments the revision and
re-anchors; it does not say a phase is entered once.

**Condition C-05-4b.** "A phase transition is observable **at most once** per consumer. A snapshot
establishes the consumer's current phase without re-firing entry for a phase it already observes.
Consumers must treat phase entry as idempotent, and the broker must not deliver an entry for a phase
the snapshot has already reported."

**(c) No eviction rule when a producer dies without `Closed`.** I searched `A1-R4` for
producer-destruction, purge, evict or abandoned-telegraph handling: **no match.** §3's table says
`Closed` → "discard the block", which covers the clean path. It does not cover the attacker being
destroyed, unloaded or killed mid-windup — the ordinary case in a level with streaming.

A stateful broker that only removes entries on `Closed` **leaks an entry for every telegraph whose
producer dies**, and `GetOpenTelegraphs` then returns a telegraph that no longer exists. A consumer
recovering from a revision gap would adopt a block for a dead attack.

**Condition C-05-4c.** "The broker removes an `AttackInstanceId`'s entry on `Closed`, **or** when the
producing actor becomes invalid or is unloaded, **or** when the entry's `AxisNow` exceeds a
staleness bound. A consumer must treat an entry whose producing actor is invalid as `Closed`."

**Condition C-05-4d.** "Snapshot delivery and `GetOpenTelegraphs` must be callable **without
re-entrancy** into the broker: a consumer that calls it from within a message handler must not
cause the broker to mutate the collection it is iterating. Specify copy-then-apply or a documented
invalidation."

### 5.5 Does this resolve U-07 or move it?

**Neither, precisely.** It **narrows** U-07 from "is there a query surface?" to "may Core hold this
state?" — and that second question is a *different question with a different owner*, not the same
question deferred.

**I recommend accepting the broker**, conditional on C-05-3 (Core ownership, for Agent 3/TD) and
C-05-4a–d (four concurrency rules, for Agent 1). The mechanism is the right shape; it is specified
one level short of being implementable.

---

## 6. E — C-03 damage request and ownership

### 6.1 The three spellings, independently verified

`A1-R4` §6.1 lists them with locations. **Every row verifies, and I checked at character level rather
than by eye:**

| Spelling | Length | Location | Verified |
|---|---|---|---|
| `FTDamageRequest` | **15** | MEAD-C line 476 | ✅ `-> FTDamageRequest { InstigatorId, …` |
| `FTDDamageRequest` | **16** | MEAD-C line 478 | ✅ `-> ITDDDamageable::ApplyDamage(FTDDamageRequest)` |
| `FTDDDamageRequest` | **17** | `CODING_STANDARDS.md` line 21; `A1-R1` §3.2; `A1-R2` §5.2; `A1-R3` §5.2 | ✅ `| Struct | FTDD<Thing> | FTDDDamageRequest |` |

**`A1-R4` does not silently select one, and this is a real change from `A1-R3`.** It locates all
three, states that MEAD-C "names the same struct with two different lengths on consecutive lines",
declines to decide, raises **U-15**, and asks the TD. **My C-03-1 condition is satisfied on
process.** It remains unsatisfied on outcome, which is why C-03 is still not signed — the condition
was that a decision be *named*, and it now is, but the decision itself is outstanding.

### 6.2 The convention argument is sound and correctly labelled as not-a-decision

`A1-R4` §6.2 argues that `FTDD<Thing>` uniquely generates the 17-character form and explicitly
refuses to treat that as authoritative because `CODING_STANDARDS.md` is Agent 1's own `DESIGN_ONLY`
document. **I verified the standard says exactly that** (line 21, table row `Struct | FTDD<Thing> |
FTDDDamageRequest`).

**That self-limitation is the correct instinct and I want it noted**, because it is the opposite of
the failure mode my `A1-R3` §5.3 found. A convention is evidence about intent; it is not a decision
procedure when the decision belongs to someone else. `A1-R4` says so itself.

### 6.3 Ownership semantics — the erratum is sound, and I evaluated it without choosing a name

`A1-R4` §5.2's additions (1) and (2) are unchanged from `A1-R3` and I accepted them there. Addition
(3) now names the decision instead of making it:

> "The spelling is a Technical Director decision recorded here explicitly, **not a consequence of
> which diagram a drafter copied**."

**Evaluated on ownership semantics, not on the name:** the erratum correctly leaves arbitration with
Agent 1 for player-involving hits, marks every attacker-supplied number advisory, and now separates
the naming question from the authority question. **I do not choose the final name and neither
should this review.** If the TD designates either shorter form, my own documents need no change —
I reference the struct only in review prose, never in a contract clause of mine.

### 6.4 C-03 verdict

**AGREE WITH CONDITIONS.** One condition: C-03-1, the spelling designation (U-15). Everything else
in C-03 is unchanged and was accepted in my `A1-R3` review §5.4.

---

## 7. F — C-04 and C-07, MEAD and status representation

### 7.1 The contingency map, verified against the file

`A1-R4` §7.1 maps all seven retained tags plus `Dead` across four classes. **I verified each MEAD-A
citation directly** (§12.1) and the classifications hold:

| Tag | MEAD-A | Line | Class claimed | My verification |
|---|---|---|---|---|
| `Status.Invulnerable` | `State.Combat.Invulnerable` + `State.Invulnerable.Dodge` | 507, 488 | RENAME | ✅ both exist; two granularities, as stated |
| `Status.Staggered` | `State.Combat.Staggered` | 507 | RENAME | ✅ |
| `Status.Parrying` | `State.Combat.ParryWindow` | 507 | **SEMANTIC** | ✅ window vs state — correct, not a rename |
| `Status.Cinematic` | `State.Locomotion.Cinematic` | **506** | **CONTRADICTION** | ✅ see §7.2 |
| `Status.Attacking` | none | — | MISSING | ✅ `State.Combat` has no attacking value |
| `Status.Blocking` | none | — | MISSING | ✅ |
| `Status.Grabbed` | none | — | MISSING | ✅ `ledge-grab` (450) is traversal, not victim state |
| `Status.Dead` | none as a tag; `State.Combat.Downed` exists | 507, 615 | MISSING + semantic trap | ✅ §7.3 |

**Tally: two renames, one semantic change, one contradiction, three missing tags plus `Dead` = four
requests.** Matches my own independent count in `A1-R3` §4.3 exactly.

### 7.2 One citation error, and the `Cinematic` classification is right for a better reason

**`A1-R4` cites MEAD-A line 505 for `State.Locomotion.Cinematic`. It is line 506.** Line 505 is
`Chapter.Ch01 … Chapter.Ch08`. Corrected. This is the same class of error as my own in `A1-R3`
§0.5 — a citation drawn from a heading I located rather than from the line itself.

**The `CONTRADICTION` classification is correct and `A1-R4`'s justification is stronger than its own
table shows.** It says A puts `Cinematic` on the locomotion axis while M1 v1.4 treats it as a control
state that outranks Stagger. **I confirm from the file that `State.Locomotion.<…|Cinematic>` is a
*collision with a legitimate locomotion value*, not a misnamed equivalent** — under MEAD-A a
cinematic takeover and a slide are the same kind of thing, which is exactly why mapping the
precedence member into it would break the accepted table.

### 7.3 `Dead`: a player status tag is not an enemy AI state, and the distinction holds

**Independently verified.** MEAD-A line 615 is `ATDDEnemyBase`'s StateTree list ending
`Staggered, Dead` — an **AI state machine for enemies**, not a player-facing tag. MEAD-C models
`Dead` as a value of `UTDDCharacterStateMachine`. **Neither provides a `Status.Dead` tag, and
`State.Combat.Downed` is not a substitute.** `A1-R4` §7.1's framing is correct: downed implies
survivable and revivable; dead is terminal. Mapping one to the other would be a correctness bug.

### 7.4 The two-representation fallback — coherent, and the consequences are adequate

`A1-R4` §8's four numbered consequences are a direct answer to my C-04-1:

1. arbitration unaffected (compares priorities, not representations) — **correct**;
2. tag-driven consumers must use `bAlive` or a phase condition — **correct**, and `bAlive` is
   already published per C-02;
3. the table is not authorable as one data table — **correct**, and it is the cost I identified;
4. logs and telemetry name the enum — **correct**.

**This is coherent and the consumer consequences are adequately stated.** My C-04-1 is satisfied.

**One thing it does not say that a consumer needs**, which I raise as an addition rather than a
condition: if `Status.Dead` is declined, then **the precedence evaluation path differs by value** —
an enum comparison for `Dead`, tag lookups for the other two. A consumer implementing
`Dead > Cinematic > Stagger` from outside Agent 1 (an A2 boss deciding whether to stop attacking)
has no single call that answers it. **`A1-R4` says tag-driven consumers must use `bAlive`; it does
not say what a consumer uses to ask "is `Cinematic` currently outranking `Stagger`."** That is
answerable inside Agent 1 and not outside it, and should be stated.

### 7.5 The C-01 capability map in §7.4 is beyond scope, correct, and consequential

`A1-R4` §7.4 maps my five C-01 capabilities onto MEAD-A's `ETDDTraversalAction`. **I verified line
450:** `ETDDTraversalAction (vault / ledge-grab / climb-lite / drop)`. **Four values against my
five capabilities.** The mapping is correct and its conclusion is right: two renames (`Vault`,
`Drop`), two semantic (`ClimbLadder`→`climb-lite`, `LedgeShimmy`→`ledge-grab`), one missing
(`Mantle` — I confirmed `mantle` appears **zero** times in MEAD-A).

**This matters more than §7.4 gives it credit for, and it is the finding I most want TD-12's decider
to see.** `A1-R4` says "the five-capability model survives; the vocabulary does not." Correct — but
**`Mantle` is not a naming difference, it is a capability with its own montage requirement**, and I
have already recorded it as a content blocker. Under MEAD-A, C-01 would need a new capability *and*
its animation content, not a rename. **That is a production cost, not a schema cost**, and it belongs
in the TD-12 decision alongside the four namespace requests.

### 7.6 C-04 and C-07 verdicts

**Both AGREE WITH CONDITIONS.**

| Condition | Contract | Owner | Closed by |
|---|---|---|---|
| C-04-1: `Dead` is the only non-tag precedence value | C-04 | A1 | **satisfied** (§7.4) |
| C-04-2: full contingency map | C-04, C-07 | A1 | **satisfied** (§7.1) |
| **C-04-3** (new): state what an external consumer uses to evaluate `Cinematic > Stagger` when `Dead` is non-tag | C-04 | A1 | one sentence |
| **C-07-1**: TD-12 must name one canonical file **and commit** | C-07 | TD | open |
| **C-07-2**: TD-13 save inventory | C-07 | Agent 3 | open |
| **C-07-3**: registry owner's namespace list + `Status.Dead` | C-07 | Agent 3 | open |

C-07 is not signed because **all three of its conditions belong to other people.** `A1-R4` §11.2
adopts my "no ordering shortcuts the other two" framing, which is correct and which I confirm.

---

## 8. D — C-02 published player context

### 8.1 `A1-INTERNAL` is now genuinely absent — my C-02-1 is satisfied

`A1-R4` §9.1 states `CameraForward`, `GroundSlopeDegrees` and `ActiveActionId` are "**not members of
the published snapshot struct at all**", with "no 'published but marked internal' tier", and the
consequence that a consumer referencing them **fails to compile**.

**That is exactly the promise I asked for** and better phrased than my own: a compile failure is the
only form of "not published" that can be tested. Three tests proposed against it. ✅

**One refinement, offered not demanded.** "Fails to compile" is true for C++ consumers. A
`BlueprintReadWrite` struct field or a reflection-driven consumer would not fail to compile — it
would simply not find the property at runtime. **The reflection test in `A1-R4` §9.1's own list
covers this**, so the claim is right and the mechanism is covered; I note it only so the clause's
"fails to compile" sentence is not read as covering Blueprint.

### 8.2 `CombatState` authority — answered correctly, and the objection to "coarse" is right

`A1-R4` §9.2 answers (a): `CombatState` is **authoritative**, tags are **derived**, with a
three-link chain and a testable invariant.

**The invariant is the load-bearing part:** "at any instant, the published tag set equals the table
row for the published `CombatState` (plus the control-state-derived tags). `CombatState` is never
derived from the tags, and no consumer can author either." **That is a single-authority guarantee and
it is exactly what prevents "two overlapping representations" from becoming two truths.**

**`A1-R4` declines my word "coarse" and its reasoning is correct.** `ETDDCombatState` distinguishes
`Telegraphing` / `Attacking` / `Recovering`, so it is not coarser than the tag set — accepting
"coarse" would imply the tags are the finer truth, which reintroduces the second authority. **I
withdraw the word and accept the substance.**

### 8.3 Mapping completeness — verified, with two observations

I enumerated all eleven `ETDDCombatState` rows and cross-checked every tag in the series:

| Check | Result |
|---|---|
| All 7 retained tags covered or explicitly excluded | ✅ 6 from combat rows, `Status.Cinematic` explicitly excluded as control-state-derived |
| All 4 requested tags covered | ✅ `Interacting`, `Traversing`, `Airborne`, `LockedOn` all explicitly excluded as non-combat |
| Every state has a row | ✅ 11 of 11 |
| Any state with no tag and no explanation | ✅ `Telegraphing` — **explained**: the windup has no tag, C-05's stream is authoritative, adding one would duplicate C-05 |

**Observation 1 — the exclusion is stated but the derivation is not.** §9.2 says the excluded tags
"derive from the control state machine directly". It does not say **which control state yields
`Status.Airborne`**, and `Airborne` is in C-02's published field set. A consumer holding both
`ControlState` and the tag set cannot verify the invariant for the four excluded tags without a
mapping. **The invariant is therefore testable for the seven combat-derived tags and asserted-only
for the four control-derived ones.** One table column would close it.

**Observation 2 — `Recovering` and `Attacking` both emit `Status.Attacking`.** That is deliberate
and correct (recovery is part of the attack; input lock applies), and it means the tag is **lossy**:
a consumer cannot distinguish recovery from attacking by tag. **That is fine as long as nothing
needs to**, and C-05's telegraph stream supplies the distinction. Worth one sentence so the loss is
documented rather than discovered.

### 8.4 C-02 verdict — **AGREE, signed, no conditions**

Both conditions from my `A1-R3` review are answered. The two observations in §8.3 are refinements
that do not change the contract, and I am **not** attaching them as conditions — attaching a
condition to something I am signing would make the signature meaningless.

---

## 9. G — C-01 and C-06, and whether the corrections introduce conflicts

### 9.1 C-01

**Unchanged since `A1-R3`, which I already agreed.** `P3′` is stable, the §10.4 row replacement
stands, and TD-04 remains a decision *inside* an agreed clause — which was the point of `P3′` and
which still works.

**Does any correction elsewhere conflict with C-01?** Checked three:

| Potential conflict | Result |
|---|---|
| §7.4's capability remap (MEAD-A contingency) | **No conflict** — it is a TD-12 contingency note, not contract text. It does not change the five capabilities. |
| C-05's broker touching traversal timing | **No conflict** — traversal has no telegraph stream; C-01's route query is synchronous, not timed |
| C-02's field removals vs C-01's `HeightAboveGround` | **No conflict** — `HeightAboveGround`/`bOnWalkableFloor` stay REQUIRED (my §4.6 decision at `CH01-SUB-005`), and §9.1 removes only `CameraForward`, `GroundSlopeDegrees`, `ActiveActionId` |

**No new conflict. C-01 signed.**

### 9.2 C-06

**Unchanged and untouched.** `A1-R4` §12 confirms "Text stable since `A1-R3`" and "none" changed.

**Does any correction elsewhere conflict with C-06?** Checked two:

| Potential conflict | Result |
|---|---|
| C-05's `Retimed` message on the shared bus | **No conflict** — interaction holds are not timed by the telegraph axis; C-06's hold duration is router-owned, not axis-derived |
| §8's `Dead` fallback vs C-06's `Cancel(Died)` | **No conflict** — the cancel reason is a cancellation cause, not a precedence value |

**U-08 (damage interrupts a hold) remains escalated and unassumed**, which I verified: `A1-R4` §11.1
lists it "unchanged" and §12 says C-06 needs nothing. **My instruction not to treat it as decided is
honoured on both sides.** **C-06 signed.**

---

## 10. H — signatures, and one thing `A1-R4` gets right about them

### 10.1 The overreach is withdrawn correctly

`A1-R3` §7.4's claim that C-03 and C-06 were "already there" is **withdrawn in full** in `A1-R4`
§10.1, with the correct replacement: "No contract in this series is bilaterally agreed, conditionally
agreed, or 'already there'." **My `A1-R3` §1.3 rejection is accepted and I confirm the correction.**

### 10.2 The signature sequence `A1-R4` states is correct and I adopt it

`A1-R4` §10.1 lists three items that "remain outside both agents' authority even after two
signatures": TD-12, the registry's namespace and `Status.Dead`, and the save inventory for TD-13.

**That is a correct statement of the boundary and it is the same three items I identified.** I adopt
the ordering: two signatures on one exact blob, then TD review, with those three decisions outside
the sequence entirely.

### 10.3 What I signed, restated so it cannot be misread

**Three contracts: C-01, C-02, C-06. On blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75` only.**

If a successor version changes those three contracts, **the signatures do not carry forward** — a
signature names a blob, not a contract name. If the TD issues the C-05 or C-03 decisions and Agent 1
publishes a successor, I review it and sign again or not, from scratch.

**And a signature from me is one of three.** It is not agreement, and the table in §1.3 is the
accurate record: no contract has two signatures and none has TD review.

---

## 11. Findings, corrections and what I am asking for

### 11.1 Resolved — nothing further needed

`A2R-22`, `A2R-23`, `A2R-25`, `A2R-26`, `A2R-27`, `A2R-28`, `A2R-29`, `A2R-30`, `C-02-1`, `C-02-2`,
`C-03-1` (process), `C-04-1`, `C-04-2`, the `A1-R3` §7.4 overreach. **Fourteen findings closed.**

### 11.2 Still open — none of them a technical defect in Agent 1's clause text

| ID | Item | Owner | Blocks signature of |
|---|---|---|---|
| **U-07 / C-05-3** | May Core hold stateful telegraph authority? | Agent 3 + TD | C-05 |
| **U-15 / C-03-1** | Authoritative struct spelling | TD | C-03 |
| **U-12** | MEAD §5.4 erratum (needs canonical file + spelling) | TD | C-03, C-07 |
| **U-13 / TD-12** | Canonical MEAD file and commit | TD | C-07 |
| **U-11 / TD-13** | Save inventory | Agent 3 | C-07 |
| **U-14** | `Status.Dead` grant | Registry owner | C-04 |
| **U-08** | Damage interrupts a hold | TD / design | nothing — C-06 is agnostic |
| TD-02, TD-03 | Stagger-class representation; applied-event semantics | TD | nothing — both contracts signed |

### 11.3 New asks — five, all additions or precision, none a redesign

| ID | Ask | Contract | Owner |
|---|---|---|---|
| **A2R-31** | C-05-3: raise broker statefulness as a **Core-ownership request** to Agent 3/TD, separate from U-07 | C-05 | A1 → A3/TD |
| **A2R-32** | C-05-4a: strict-greater revision adoption for both messages and snapshots | C-05 | A1 |
| **A2R-33** | C-05-4b: at-most-once phase entry per consumer | C-05 | A1 |
| **A2R-34** | C-05-4c/d: broker eviction on producer invalidation; non-re-entrant query | C-05 | A1 |
| **A2R-35** | C-04-3: state what an external consumer uses to evaluate `Cinematic > Stagger` when `Dead` is non-tag | C-04 | A1 |

**Plus three minor wording notes, not asks:** C-05-5 (same-frame `Retimed` is a producer obligation),
§3's completion predicate should be the inequality not `R = 0` alone, and §5 case 5 should test both
a wrong operator and a wrong rate.

**`A1-R4` also owes me one correction, and I am recording it:** §7.1 cites MEAD-A line **505** for
`State.Locomotion.Cinematic`; it is **506**.

### 11.4 My own errors in this series, updated

| # | Error | Found by |
|---|---|---|
| 1 | Claimed TD v1.2 did not exist | my own search, pre-publication |
| 2 | Nearly claimed A1 fabricated MEAD citations | my own all-refs search, pre-publication |
| 3 | Said all three MEADs identify as `TDD-MEAD-001` v1.0 | **Agent 3, recon V3 §5.1** |
| 4 | Miscounted my clause verdicts (44/29/11 → 61/56/5) | my own tests, pre-publication |
| 5 | Attributed MEAD-A §6.6's tag rule to MEAD-C | **Agent 1, `A1-R3` §0.5** |
| 6 | **Headed a table "Ten asks" and listed nine** | **Agent 1, `A1-R4` §1** |
| 7 | **Drafted a float32 precision finding that was arithmetically wrong** | **my own check, pre-publication (§3.5)** |

**Seven errors, four caught by my own tests or searches before publication, three by other agents.**
Errors 3, 5 and 6 are all citation-or-counting failures rather than reasoning failures, which is a
consistent signature and now the dominant one. The countermeasure I adopted in my `A1-R3` §13.4 —
emit section references from the command that located the text — is the right one for 3. It does not
catch 6, which is arithmetic on my own table. **The addition: enumerate a list and count it in the
same command that writes its heading.**

---

## 12. Evidence

### 12.1 Executed — 25 document and arithmetic checks

Each evaluates a formula or a file, **not** behaviour. 24 passed; 1 failed on a line citation (§7.2).

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Derivative `d(local)/d(axis) = ProducerRate`, `P` cancels | re-derived from `A1-R4` §2.1 definitions | ✅ matches |
| 2 | `local = axis × rate` and `axis = local / rate` are inverses | round-trip at rates 1.0/0.5/0.2/0.05 | ✅ 1.000000 to 1e-12 |
| 3 | 0.20 s local at 0.05 → 4.00 axis | arithmetic | ✅ 4.0000 |
| 4 | …and back to 0.20 | arithmetic | ✅ 0.2000 |
| 5 | `A1-R3` divide form → 80.00 | arithmetic | ✅ 80.0000 |
| 6 | Inflation = `1/rate²` = 400 | arithmetic | ✅ 400 |
| 7 | Retime `0.4 + 0.800/0.2` = 4.40 | arithmetic | ✅ 4.4000 |
| 8 | §3.3(a) inverse row == §3.3(b) | form comparison | ✅ same direction |
| 9 | `R(t)` constant across a 10 s pause | model: axis frozen | ✅ 0.500 unchanged |
| 10 | Wall-clock aging would close early | counter-model | ✅ → 0.0 |
| 11 | `R = 0` ⟺ `elapsed ≥ R0/rate` | predicate check | ✅ equivalent (R=0 over the whole tail) |
| 12 | `R` monotone non-increasing, never negative | 20-step numeric | ✅ |
| 13 | Primary-dilation change needs no message | inspected `R`'s dependencies | ✅ only `R0`, axis, rate |
| 14 | float32 ULP for 0.20 s is negligible | `struct`-based float32 | ✅ 1.49e-08 s — **discarded as a finding** |
| 15 | double axis ULP after 8 h at 240 fps | mantissa computation | ✅ 3.6e-12 s — **discarded** |
| 16 | MEAD-A 450 = `ETDDTraversalAction` 4 values | line read | ✅ |
| 17 | MEAD-A 488 = `State.Invulnerable.Dodge` | line read | ✅ |
| 18 | MEAD-A 506 = `State.Locomotion` incl. `Cinematic` | line read | ✅ **`A1-R4` cites 505 — off by one** |
| 19 | MEAD-A 507 = `State.Combat` 5 values | line read | ✅ |
| 20 | MEAD-A 517 = "no agent introduces a tag namespace" | line read | ✅ |
| 21 | MEAD-A 615 = enemy AI `Staggered, Dead` | line read | ✅ AI state, not player tag |
| 22 | MEAD-A has zero `mantle`, `shimmy`, `ladder` | full-text count | ✅ 0 / 0 / 0 — `Mantle` genuinely missing |
| 23 | MEAD-C 476/478 = 15-char and 16-char forms | character extraction | ✅ distinct lengths |
| 24 | `CODING_STANDARDS` 21 = `FTDD<Thing>` → 17-char form | line read | ✅ |
| 25 | `A1-R4` states what it claims to (9 markers) | string presence | ✅ all 9 |

### 12.2 Repository suite — executed, tests my documents not `A1-R4`

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/canon/tests` | see §12.5 | see §12.5 |
| `python3 -m unittest discover -s Tools/world/tests` | see §12.5 | see §12.5 |
| `python3 Tools/ci/l0_checks.py` | see §12.5 | see §12.5 |
| `python3 Tools/world/contract_data_checks.py` | see §12.5 | see §12.5 |
| `python3 Tools/world/gen_evidence.py` | see §12.5 | see §12.5 |

**These pass because my own documents and data are consistent. They say nothing about `A1-R4`.**

### 12.3 Categories kept separate

| Category | Count | Executed? |
|---|---|---|
| (a) Analysis checks in this review | 25 | **Yes** — §12.1 |
| (b) Repository suite | see §12.5 | **Yes** |
| (c) Document tests locking my prior reviews | 43 + 55 + 42 | **Yes** |
| (d) `A1-R4`'s proposed suites | 23 suites, 139 cases | **No — 0 run** |
| (e) Contract acceptance tests | 42 mine + `A1-R4`'s 139 | **No — 0 run** |
| (f) Tests A1 or A3 ran | unknown to me | **Not claimed** |

### 12.4 What I did not do

- No `A1-R4` test was run; none is implementable here.
- I did not claim Agent 1 or Agent 3 ran my tests; `A1-R4` §13.1 attributes mine correctly.
- **I did not measure anything.** The `1/rate²` and 400× figures are arithmetic on a stated formula.
- I did not select a canonical MEAD, issue an erratum, register a tag, or make any TD decision.

### 12.5 Tests added by this review

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_review_r4.py"` | **64 OK** | 0 |

`Tools/world/tests/test_contract_review_r4.py` locks this document's claims:

| Test class | What it pins |
|---|---|
| `TestConversionCorrected` | The re-derivation, mutual inverses at four rates, the 4.00/0.20/80.00/400× figures, and that both forms coincide at rate 1.0 — **the correction this review certifies** |
| `TestRetimeAgreement` | That §2.4's inverse row and §3.3(b) are the same arithmetic, and that the old form inflates an axis offset |
| `TestAgingRule` | §3.3(e): linearity, constancy across a pause, why wall-clock aging closes early, the completion predicate, monotonicity, and that a primary-dilation change needs no message |
| `TestPrecisionConcernDiscarded` | **The concern I raised and discarded (§3.5)** — float32 and long-session double ULPs both negligible |
| `TestA1R4DocumentClaims` | That the reviewed blob is `2cc548f`, and that every formula the review quotes exists verbatim in `A1-R4` |
| `TestBrokerGaps` | **The four broker gaps** — each absent phrase is asserted absent, so if `A1-R5` closes one these tests fail and this review must be updated |
| `TestMeadCitations` | MEAD-A 450/488/506/507/517/615, `Mantle` absent, no `Status.*`, and **that the locomotion axis is 506 not 505** |
| `TestCodingStandard` | `FTDD<Thing>` on line 21 generates the 17-character form |
| `TestReviewSelfConsistency` | 7 verdicts, the distribution, 3 signed / 4 not, the blob named, no bilateral claim, A2R-31…35, 7 recorded errors |
| `TestPreservation` | The `A1-R3` review still exists, still says 0 of 7, and was not retro-edited |

**Three tamper proofs run.**
1. Replacing the `×` in `A1-R4`'s conversion with a division removes the literal
   `test_states_multiply_form` asserts on — verified: substitution applied, key absent, test would fail.
2. Adding "strictly greater", "at most once" or "evict" to a simulated successor trips the
   `TestBrokerGaps` assertions — verified against a synthetic document.
3. Changing "Signed: 3 of 7" to "5 of 7" fails `test_three_signed_and_named`; restoring passes.

**Class 2 is deliberately fragile in one direction.** Those tests assert a phrase is *absent*, so a
future `A1-R5` that fixes a gap breaks them — which is correct, because the review's claim is
about *this blob*. A passing suite against a later document would hide the closure.


---

## 13. Method and limits

### 13.1 What this review does not establish

| Not established | Why |
|---|---|
| That any contract is bilaterally agreed | §1.3 — three signatures from one agent; no contract has two |
| That TD accepts anything | v1.2 predates this document |
| That the broker works | It is a proposal; no implementation exists; four gaps open (§5.4) |
| That the Core placement will be granted | Agent 3/TD own it (§5.3) |
| That C-05's arithmetic is implemented correctly | It is correct **on paper**; the defect was a transcription error, which is exactly the class that survives a correct derivation |
| That M0 is complete | no `.uproject`, no `Source/`, no build |

### 13.2 The limit specific to this review

**The C-05 defect I found was a transcription error, not a conceptual one.** `A1-R3`'s derivation and
its formula disagreed, and I found it by deriving independently. **`A1-R4` fixes the formula and now
puts the derivation in the contract** — which is the right fix, because it makes the same class of
error visible to the next reader.

**But a correct derivation in a document does not prove a correct implementation.** The risk that
remains is that the eventual C++ follows `A1-R3`'s habit rather than `A1-R4`'s text. That is what
`A1-R4` §5's negative control exists to catch, and it is why I asked for a second broken fixture.

### 13.3 My recommendation to the TD, offered as input only

I do not make TD decisions. Three items where my reading may be useful:

1. **U-07 / C-05-3 is an ownership decision, not a design one.** The broker is the right mechanism;
   the question is whether Core may hold telegraph state. Deciding it unblocks C-05. See §5.5.
2. **U-15 (spelling) is cheap now and expensive later.** `A1-R4` §6.3 is right that the cost today
   is a find-and-replace across three documents and one coding-standard example.
3. **TD-12's MEAD-A option costs more than `A1-R3` showed and `A1-R4` §7 now quantifies:** four
   namespace requests against a document that forbids them, one precedence contradiction, and **one
   missing capability with its own animation content** (§7.5). That last item is production cost,
   not schema cost, and it is the one most likely to be missed.

---

## 14. Publication

### 14.1 Provenance

| Field | Value |
|---|---|
| Document | `Docs/AGENT2_REVIEW_A1R4_V1.md` — **new file** |
| Branch | `arena/5dde91a4-tdd` (existing; no new branch, no merge) |
| Reviewed | `A1-R4` v1.3, branch head `142cabd`, **blob `2cc548f` (verified before reading)** |
| My prior review | `TDD-A2-REVIEW-A1R3-001` v1.0 at `4c09980` — **basis** |
| My submission | `A2-C01…C07-1.0` at `3ac438b` — **unchanged** |
| Governing TD | v1.2 at `e121bbb` |
| Reconciliation | v3.0 at `98399af` |
| MEAD-A / B / C | read only; **none moved, deleted, renamed, archived, overwritten or edited** |
| `DECISIONS.md` | **not modified** |
| `A1-R4` document | **not modified** |
| Code, Core types, project, merge, API freeze, tag, erratum, canonical MEAD | **none** |
| Contracts signed | **3 of 7** (C-01, C-02, C-06) |

### 14.2 Preservation

| Artifact | Status |
|---|---|
| `AGENT2_REVIEW_A1R1_V1.md` (`93b2f07`) | unchanged |
| `AGENT2_REVIEW_A1R2_V1.md` v1.0 (`4220b82`) and v1.1 (`c726096`) | unchanged |
| `AGENT2_REVIEW_A1R3_V1.md` (`4c09980`) | unchanged |
| `CONTRACT_SUBMISSION_A2_V1.md` (`3ac438b`) | unchanged |
| 57/57 location capture, register v2.9 provenance | preserved; **register not modified** |
| Interactable and prop totals | **still withdrawn; no count stated in this document** |
| `scene_register_ch01_full.md` | **not edited** |

### 14.3 Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-17 | Review of `A1-R4` v1.3 at `142cabd`, blob `2cc548f`. Seven verdicts: **3 AGREE (C-01, C-02, C-06), 4 AGREE WITH CONDITIONS (C-03, C-04, C-05, C-07), 0 DISAGREE**. **Three contracts signed on this exact blob** — the first signatures given in the series. The C-05 arithmetic defect is verified fixed by independent re-derivation, and my `A1-R3` DISAGREE is withdrawn. Fourteen prior findings closed. Five new asks (A2R-31…35) plus three wording notes, none a redesign. Four concurrency and ownership gaps found in the broker (§5.3–5.4). One citation error in `A1-R4` (§7.2). One precision concern raised and **discarded as arithmetically wrong** (§3.5). 25 analysis checks executed, 24 passing; 0 contract acceptance tests run. |

**This document is a review, not a contract.** It signs three contracts on one exact blob and
agrees nothing bilaterally. It freezes nothing, chooses no canonical MEAD, issues no erratum,
registers no tag, and authorises no implementation.
