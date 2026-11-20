# AGENT 2 — FORMAL REVIEW OF AGENT 1 REVISION `A1-R3` v1.2

**Document ID:** `TDD-A2-REVIEW-A1R3-001`
**Version:** 1.0
**Date:** 2026-11-17 UTC
**Author:** Agent 2 — World Structure and Level Architecture

**Reviewing:** `TDD-A1-CONTRACT-RESPONSE-003` **v1.2 (`A1-R3`)**, exact commit `70db9665b67723a526a6d40fa71ec832f1a95498`, document blob at path `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md`
**Against:** my `A2-C01…C07-1.0`, exact commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644`
**Governing decisions:** `TDD-TD-INT-001` v1.2, commit `e121bbbf09562e3cba0efe81aad971809685db23`
**Reconciliation:** `TDD-INT-RECON-001` v3.0, commit `98399af12bf234259143d5b85a1634c48f9eef29`
**My prior review:** `TDD-A2-REVIEW-A1R2-001` **v1.1**, commit `c726096deeef51c6fe12b15126f43733b60a5339` — **the corrected version, and what this review builds on**
**Superseded input:** the same review at v1.0, commit `4220b82ffdebf291793ce508dd25080528a3dac8` — preserved unchanged, **not** the basis for this review

**Status:** `DESIGN_ONLY`. No C++, no Core type, no Unreal project, no merge, no API freeze, no M0 claim.

> Every shape in this document is `PROPOSED — NOT FROZEN`.
> **Signed: 0 of 7.** See §1.3 — and note that `A1-R3`'s own §7.4 now asserts C-03 and C-06
> "are already there", which is the one claim in `A1-R3` I must reject on signature-status grounds.

---

## 0. Reading notes

### 0.1 What I reviewed, and the exact blobs

`A1-R3` is a genuine successor, not a reissue. It is 494 lines against `A1-R2`'s 688, and it is
shorter because it **replaces clause text instead of arguing around it** — which is the right
instinct and materially easier to review.

| Artifact | Exact reference | How I used it |
|---|---|---|
| `A1-R3` | `70db9665b677…`, `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md` | read in full, 494 lines |
| `A1-R2` | `f578fe612ad1…` (blob `bdcd0fe…`) | compared clause by clause |
| My review v1.1 | `c726096deeef…` | the basis; v1.0 not used |
| Recon v3.0 | `98399af12bf2…` | §5 MEAD comparison, §7 erratum, §6 TD list |
| MEAD-A | `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, 1,078 lines | verified directly, including §6.6 |
| MEAD-B | `docs/MASTER_ENGINEERING_ARCHITECTURE.md`, 247 lines | verified directly |
| MEAD-C | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md`, 1,231 lines | verified directly |

**I re-verified all three MEADs from the files rather than from `A1-R3`'s or recon's summary.**
That mattered twice in this review — §0.3 and §4.3 below.

**Carried forward from my v1.1 correction, unchanged and not re-litigated:** only MEAD-A and MEAD-C
formally identify as `TDD-MEAD-001` v1.0; MEAD-B is an unversioned initial baseline; **I authored
MEAD-A**; MEAD-C models `Dead` as a character-state value rather than a `Status.*` tag; and MEAD-C
§5.4 spells the damage-request struct two ways on consecutive lines — at **different lengths**
(`FTDamageRequest`, 15 characters; `FTDDamageRequest`, 16). **`A1-R3` asserts none of the
errors those corrections removed**, and its own §4.2 MEAD table is accurate on every row I checked.

### 0.2 One thing `A1-R3` gets right that I want on the record first

`A1-R3` §0.3 lists **five defects in its own work** and attributes them correctly, including the
one that matters most: its collision table told two agents to "yield to MEAD" without checking
that `Status.Dead` exists. It also accepts both of my §0.3 misattribution findings, one without
qualification and one with a defensible version argument (§0.4).

That is the fourth consecutive artifact from Agent 1 that has led with its own errors. It is worth
naming because the counter-pressure is the opposite habit, and I have been on the wrong side of it
twice myself.

### 0.3 `A1-R3` §0.5 is correct, and the error was mine

`A1-R3` §0.5 says my review attributed the rule *"new tags are proposed to the tag owner and land
in `DefaultGameplayTags.ini` with a comment naming the requiring feature"* to **MEAD-C §6.6**, when
it is **MEAD-A §6.6**.

**I verified it, and `A1-R3` is right.** My review v1.1 line 1135 says:

> it**, per MEAD-C §6.6's own rule ("new tags are proposed to the tag owner and land in
> `DefaultGameplayTags.ini` with a comment naming the requiring feature")

Against the files:

| Check | Result |
|---|---|
| MEAD-C §6.6 heading (line 555) | **"Chapter production pipeline (repeatable, per chapter)"** — content pipeline |
| MEAD-C full-text `DefaultGameplayTags` | **0 matches** |
| MEAD-A §6.6 heading (line 500) | **"Gameplay Tag vocabulary (cross-agent contract)"** |
| MEAD-A line 517–518 | **the quoted rule, verbatim** |
| MEAD-A line 350 | cross-references the tag contract as "§6.6" |

**This is my fifth attribution error across three reviews, and the first one `A1-R3` found rather
than me.** The pattern is now unambiguous and I am naming it rather than logging it again: I verify
*existence* by searching every ref, then cite the section number **from working memory instead of
from the located line**. Searching found the document; I then attached the wrong section label to
it. My v1.1 process correction covered existence and did not cover citation. It does now (§13.4).

**The substance is unaffected and `A1-R3` says so too:** the rule is real, requesting rather than
registering a tag is what I already do, and I accept it regardless of which MEAD is canonical. This
does not change any verdict in my v1.1 review. But it does mean the `Status.Dead` registry request
in `A1-R3` §2.2 is correctly framed as a request under **MEAD-A's** governance rule, and under
MEAD-A that rule is not merely advisory — MEAD-A line 517 opens with **"Prohibition: no agent
introduces a tag namespace."**

### 0.4 What my v1.1 review asked for, and what `A1-R3` supplies

| My A2R item | `A1-R3` answer | Adequate? |
|---|---|---|
| **A2R-17** restate P3 | `P3′` scoped stability + replaced §10.4 row (§1.2–1.3) | **Yes** — see §3 |
| **A2R-18** normalise telegraph timestamp or carry producer dilation | Option A+ shared axis + `ProducerRate` (§3.2) | **Yes in design, no in arithmetic** — §7.3 |
| **A2R-19** parry = same-frame overlap in contract text | normative clause, §3.4 | **Yes** — better than I asked |
| **A2R-20** six MEAD tags withdrawn or omitted | all six retained; table was a dispute list, mislabelled (§2.1) | **Yes** for those six — but see §4.3 for the other four |
| **A2R-21** `ApplyDamage` returns clamped delta | confirmed already in `A1-R2` §5.4 | **Yes**, correctly |

Four of five closed outright. **A2R-20 is closed for the six tags it names and not for the
inventory as a whole** — the retained/requested mix does not survive a MEAD-A canonicalisation,
which is §4.3.

### 0.5 Where this review differs from my last one

My v1.1 review ended with three contracts signable and one real technical disagreement (C-05). This
review ends with **one real technical disagreement still (C-05), a different one, and a second in
C-07.** Both new ones are in `A1-R3`'s new material. That is not a regression in `A1-R3`; it is what
happens when a document adds two new mechanisms (`Retimed`, `P3′`) and one new dependency map.

---

## 1. Agreement matrix

### 1.1 The seven verdicts

Verdicts are on **`A1-R3` as written at `70db966`**, not on the intentions described in its prose.

| Contract | `A1-R3` claims | **My verdict** | What stands in the way |
|---|---|---|---|
| **C-01** | CONDITIONAL | **AGREE** | `P3′` §1.2 and the replaced §10.4 row resolve my only condition. TD-04 stays open **as a TD question inside a signed clause**, which is `P3′`'s design intent and is correct |
| **C-02** | CONDITIONAL | **AGREE WITH CONDITIONS** | Field classification (§7.2) is right and `CameraForward` is correctly withdrawn. Two conditions: `GroundSlopeDegrees`/`ActiveActionId` must not be published as shared surface, and `CombatState` needs a stated relationship to the C-04 tag set |
| **C-03** | AGREE | **AGREE WITH CONDITIONS** | Ownership and single-publisher correct. Condition: the TD-09 erratum must be issued against a **named spelling** of the request struct, and `A1-R3` silently fixes one (§5.3) |
| **C-04** | CONDITIONAL | **AGREE WITH CONDITIONS** | Semantics, default, fallback and recovery notification all correct. Condition: `Dead` representation is a **precedence-comparable** value, and under MEAD-A the whole `Status.*` strategy needs a remap (§4) |
| **C-05** | CONDITIONAL | **DISAGREE** | Option A+ §3.3(a)'s conversion formula is **inverted**. Demonstrated in §7.3 |
| **C-06** | AGREE | **AGREE** | Router ownership, opt-in progress, exactly-once terminal call, cancellation table all satisfied. Damage-interrupt correctly left escalated |
| **C-07** | CONDITIONAL | **AGREE WITH CONDITIONS** | Yield clauses are now genuinely conditional on TD-12, which is what I asked. Condition: the conditionality is **incomplete** — §4.3's MEAD-A map covers one of seven retained tags |

**Signed: 0 of 7.** One DISAGREE, four AGREE WITH CONDITIONS, two AGREE. **An AGREE here means the
clause text is acceptable; it is not a signature** (§1.3).

### 1.2 Verdict text as the request requires it

The request asks for exactly **AGREE / AGREE WITH CONDITIONS / DISAGREE**. I have used those three
labels and no others. Where I could have written "partially", I have committed to one of the three
and named the condition, because a fourth label was the thing that made my previous review harder
to act on than it needed to be.

| | Count | Contracts |
|---|---|---|
| **AGREE** | **2** | C-01, C-06 |
| **AGREE WITH CONDITIONS** | **4** | C-02, C-03, C-04, C-07 |
| **DISAGREE** | **1** | C-05 |
| **Signed** | **0** | — |

### 1.3 Signature position — stated plainly because `A1-R3` §7.4 overreaches

**I do not sign `A1-R3` v1.2 as written. Not conditionally, not in part.**

Three reasons, in order of weight:

1. **C-05 contains an arithmetic defect I can demonstrate** (§7.3). Signing it would mean signing a
   conversion formula that inflates a 0.20 s parry window to 80 s at the dilation the mechanism
   exists to handle.
2. **C-07's conditionality is incomplete** (§4.3). Four of the seven retained `Status.*` tags have
   no MEAD-A equivalent at all, and `A1-R3` §4.3 maps only `Staggered`. The contract is honest
   about being TD-12-dependent; it is not yet complete enough that TD-12 can be answered against it.
3. **TD v1.2 §4.1** requires both agents to sign the same version and TD to review after. Four of
   `A1-R3`'s own open items (U-07, U-08, U-13, U-14) sit inside the contracts I would be signing.

**One correction to `A1-R3` §7.4, which is the only place it misstates the record.** It says:

> "If A2 reviews it and states AGREE per contract against this blob, then C-01, C-02, C-04, C-05
> and C-07 become candidates for `AGREED BY BOTH — PENDING TD`, and **C-03 and C-06 are already
> there.**"

**C-03 and C-06 are not "already there", and this is not a technicality.** `A1-R3`'s own §7.3 says:

> "C-02, C-03 and C-06 are not bilaterally agreed merely because A2 has no technical objection."

So §7.3 and §7.4 of the same document contradict each other on signature status. §7.3 is correct
and §7.4 is not. My v1.1 review said C-03 and C-06 had no remaining clause-level objection **and
expressly declined to sign them**; that statement has not changed and must not be read as a
signature. Nothing in the seven contracts is bilaterally agreed today, and **`A1-R3`'s verification
of that point elsewhere in its own text is exactly right — it simply lost it in §7.4.**

### 1.4 `A1-R3`'s review of my review — accepted and rejected

`A1-R3` raises one factual correction against me and one version argument. I want both dispositions
explicit rather than folded into prose.

| `A1-R3` claim | My disposition |
|---|---|
| **§0.5** — my review misattributed MEAD-A's §6.6 tag rule to MEAD-C | **ACCEPTED.** Verified in §0.3. My error, my fifth. |
| **§0.4** — my `CarryState` finding was "accurate against the document I reviewed, and now superseded" | **ACCEPTED as a fair reading.** `A2-C01…C07-1.0` §4.2 did mark it `REQUIRED`; my review withdrew it after checking the registers. Both statements were true of their own versions, and `A1-R3` is entitled to say so rather than accept an error it did not make. |
| **§7.4** — C-03 and C-06 "are already there" | **REJECTED**, for the reason in §1.3. Contradicts `A1-R3` §7.3. |

---

## 2. Test status, stated before any finding

**Executed in this review: 0 contract acceptance tests. Written: 0.**

No contract acceptance test can run. There is no `UTDDGameplayTimeSubsystem`, no telegraph
message, no arbiter, no registry, and no Unreal project in this workspace (ADR-0005). Every
`PROPOSED / NOT RUN` suite in `A1-R3` §9.3 remains `PROPOSED / NOT RUN`, and I did not run them.

**What I did execute, and it is not a contract test:** 11 arithmetic and data checks with bare
`python3`, recorded in §12. These evaluate **the formulas `A1-R3` states** against the behaviour
`A1-R3` claims for them. That is analysis of a document, not verification of an implementation, and
§12 says which is which per check.

**What I did not do:** I did not rerun Agent 1's suites. I did not claim Agent 3 ran mine. `A1-R3`
§9.3 correctly records my figures as *my* results at *my* commit, and I return the favour — its
suite counts are **its** claims, not something I verified.

---

## 3. C-01 — `P3′`, durable references, and TD-04 — **AGREE**

### 3.1 `P3′` resolves the contradiction I raised

My condition was that P3 must not contradict §10.4 in the same document. `A1-R3` §1.2 replaces both:

> **P3′** — A route key is **stable for the lifetime of the content it names**… never reused for
> different content **while any save, log or telemetry entry references it**. Whether a *retired*
> key must be tombstoned depends on whether anything durable references route keys. That is
> **TD-04's question, not a property of the key**.

**This is what I asked for and it is better than my own proposed wording.** My §3.5 draft scoped
P3's lifetime but left the tombstone branch as a question hanging off it. `P3′` converts the open
question into a **two-branch property**, which means TD-04 is a decision *within* an agreed clause
rather than a clause revision waiting on a decision. That is the difference between a contract that
blocks and one that does not.

### 3.2 `A1-R3` §1.3 closes the other half

Replacing the §10.4 row matters as much as replacing P3. A document that fixes P3 and leaves
"may be renamed per level edit with no migration" standing has one contradiction instead of two.
`A1-R3` replaces both, and states the permission is conditional:

> Renaming per level edit is permitted **only where no durable reference exists.**

Correct, and it matches the evidence both agents report: no Chapter 1 narrative, checkpoint or save
content references a route key.

### 3.3 On TD-04 and the tombstone policy

I stated in `A2-C01…C07-1.0` §9.3 that no save content of mine references a route key, and I have
not changed that. **`A1-R3` §1.4 is right that neither of us can answer for the save system.** I am
not now going to answer for it either — that is Agent 3's, and TD-13's counterpart question.

**The one thing I will not accept is a deferred answer presented as a resolution.** `P3′` does not
do that: it explicitly says the question is open and makes both answers implementable. So C-01 is
agreed **with TD-04 open**, and TD-04 being open does not withhold my agreement, because `P3′` was
written to be answerable later.

### 3.4 Conditions on C-01

**None.** This is a clean AGREE, and it is the first contract across three rounds where I have had
nothing to add. `P1`, `P2`, `P4`, `P5`, the five capabilities, the query semantics, all seven
outcomes, the `Cooldown` reason code and the traversal-category validation are unchanged from the
text I already accepted in v1.1.

I note for completeness that my v1.1 §3.4 finding still holds and still constrains scope: of the
eight traversal-capable Chapter 1 locations, **four host no scene** (`CH01-TRV-001…004`), and
`A1-R3` correctly keeps water and rope out of scope. That is unchanged and needs no action.

---

## 4. C-04 — `Dead` representation, precedence, registry — **AGREE WITH CONDITIONS**

### 4.1 What `A1-R3` gets right

Its §2.1 completes the inventory and admits the table was a **dispute list mislabelled as an
inventory**. I flagged that as a possible withdrawal of six tags in my v1.1 §6.5; `A1-R3` says they
were never withdrawn, and I accept that. **A2R-20 is closed for those six.**

Its §2.2 `Status.Dead` registry request is well-formed in the way that matters: it names the
requiring feature, the consumers, a proposed spelling, an explicit non-creation clause, and **a
documented fallback if the registry declines**. That last part is uncommon and it is the difference
between a request and a dependency.

### 4.2 The `Dead` representation question, taken seriously

The request asks me to evaluate `Dead` as a state-machine value versus a status tag. My v1.1 review
established that MEAD-C models it as a character-state value and has no `Status.Dead`. `A1-R3`'s
fallback says precedence still works inside Agent 1 if the tag is declined, because `Dead` is
already an enum value.

**That is true for precedence evaluation and false for everything else, so the fallback is
narrower than it is presented as being.** Precedence is a comparison; a comparison needs an ordered
representation, not a tag. But the C-04 rule is implemented by *forced-transition arbitration*,
which must answer "what is the winner right now" from whatever each system exposes. If
`Dead` is a state-machine value and `Staggered` is a tag, then:

| Question | Answerable if both are tags | Answerable if `Dead` is a state value |
|---|---|---|
| "Is `Dead` outranked by `Cinematic`?" | yes | yes, inside A1 |
| "Does an A2 AI condition ask *is the player dead* in the same vocabulary as *is the player staggered*?" | yes | **no** — needs `bAlive`, which `A1-R3` §7.2 does publish |
| "Can a designer author `Dead > Cinematic > Stagger` as one table in data?" | yes | **no** — two representations, two lookups |
| "Does the precedence set survive a MEAD that fixes a tag vocabulary?" | yes | **only by convention** |

So the fallback works, and `A1-R3` is right that it works. What it does not do is make the
precedence rule **authorable in one vocabulary**, and the C-04 contract's whole justification is
that designers tune these numbers. **A two-representation precedence table is a maintenance
surface, not a correctness bug.**

**Condition C-04-1.** If the registry declines `Status.Dead`, then `A1-R3` §2.2's fallback must
state explicitly that **`Dead` is the only precedence value expressed as a non-tag**, and that the
`Dead > Cinematic > Stagger` table is therefore split across two lookup types. Not a redesign —
one sentence in the clause, so nobody later assumes the table is uniform.

### 4.3 The condition that actually bites: `A1-R3` §4.3 maps one of seven retained tags

This is the substantive finding of §4, and it is about completeness of the TD-12 contingency rather
than about C-04's semantics.

`A1-R3` §2.1 retains **seven** MEAD-C `Status.*` tags. Its §4.3 asks what changes if a MEAD other
than C is canonical. **Its §4.3 table maps exactly one of them:** the `Status.Staggered` row.

I mapped all seven against MEAD-A directly:

| Retained tag | MEAD-C | MEAD-A equivalent | Consequence if MEAD-A is canonical |
|---|---|---|---|
| `Status.Invulnerable` | present | **`State.Combat.Invulnerable`** — exact | rename only |
| `Status.Staggered` | present | **`State.Combat.Staggered`** — exact | rename only (**the one row §4.3 maps**) |
| `Status.Parrying` | present | `State.Combat.ParryWindow` — **a window, not a state** | **semantic change**, not a rename |
| `Status.Cinematic` | present | `State.Locomotion.Cinematic` — **a different axis** | **semantic change**: locomotion vs combat precedence |
| `Status.Attacking` | present | **none** | **becomes a new-namespace request** |
| `Status.Blocking` | present | **none** | **becomes a new-namespace request** |
| `Status.Grabbed` | present | **none** | **becomes a new-namespace request** |
| `Status.Dead` (requested) | absent | **enemy AI `Dead` only** (MEAD-A §8.2 line 615) | still a request, and `State.Combat` has `Downed` but not `Dead` |

**And MEAD-A's namespace list is a closed set with an explicit prohibition.** MEAD-A line 500 calls
the namespaces *"closed and reviewed like code"*, and line 517 reads **"Prohibition: no agent
introduces a tag namespace."** So under MEAD-A, three of the seven retained tags and `Dead` are
**four separate namespace requests against a document that forbids introducing namespaces.**

That is a materially larger consequence than `A1-R3` §4.3 states, and it is not a criticism of its
reasoning — §4.3's rows are accurate. It is incomplete, and the incompleteness has a specific
cost: **TD-12 is asked to decide canonicality, and the document presenting the decision does not
show the decider that choosing MEAD-A turns seven fixed tags into four requests plus two semantic
remaps.**

**Condition C-04-2.** `A1-R3` §4.3 must extend its MEAD-A column to all seven retained tags plus
`Dead`, and must distinguish **rename** from **semantic change** from **new request**. My table
above is the content; it is offered as replacement text, not as a competing registry.

### 4.4 What I accept without condition

- `ETDDStaggerClass {Never, Always, OnPostureBreak, OnParryOnly}`, default `Never`
- warn-not-block classification, bool acceptable
- single-winner precedence `Dead > Cinematic > Stagger` — **preserved, as the request requires**
- health independence
- `FTDDRecoveryCompletedEvent` as **notification only**, informational, post-commit, unable to
  create or mutate a transition

That last one answers the question the review request asks directly: **a recovery notification
cannot create or mutate a control-state transition.** `A1-R3` §7.1 restates it as
"recovery notification as notification only" and I confirm the semantics are what I required.

---

## 5. C-03 — damage ownership, attacker supplied data, the erratum — **AGREE WITH CONDITIONS**

### 5.1 Ownership is settled and `A1-R3` settles it in the right direction

The six-role split is unchanged and `A1-R3` §5.4 records it as **agreed in substance by both
agents**. I accept that description of the *erratum text* and nothing more; §7.3 is where `A1-R3`
declines to convert it into a signature, correctly.

`A1-R3` §5.3 makes an observation I had not drawn explicitly and which is right: my
`FTDDHitIntentRequest` with `Volumes` becomes **authored volume and timing data that Agent 1
evaluates**, not a detection result Agent 1 consumes. I accept that reinterpretation, and it is
consistent with my own §10.2 commitment — Agent 2 does not arbitrate any hit involving the player.
The shape is unchanged, which is the point: the ownership boundary moved and the data structure
did not need to.

### 5.2 The two additions to my erratum — I accept both

`A1-R3` §5.2 proposes:

> **(1)** `OutcomeType` may be retained on the message **for telemetry only**, and any consumer
> reading it for a decision is in violation of this erratum.
> **(2)** The same principle applies to **every** attacker-supplied number on the request —
> `RawDamage`, `PostureDamage`, `StaggerClass` and any severity hint are advisory, and the arbiter
> recomputes or overrides each of them.

**Addition (2) is the more important of the two and it improves my text.** My erratum fixed one
field and left the diagram's other attacker-supplied numbers doing the same job. A rule that names
only `OutcomeType` invites a reader to conclude the other fields are authoritative *by omission*.
**(2) closes the class rather than the instance, and I would not sign the erratum without it.**

I accept (1) as well, with its consequence stated: if `OutcomeType` is telemetry-only, then the
`Blocked`/`Parried` outcome that telemetry reports is the **arbiter's re-derived value**, never the
attacker's. Recorded so a telemetry consumer cannot later cite the message field as the source.

### 5.3 Condition C-03-1 — the erratum must name one spelling, and `A1-R3` has silently chosen

`A1-R3` §5.2 reproduces my erratum using **`FTDDDamageRequest`**. MEAD-C §5.4 uses **both**
`FTDamageRequest` (line 476) and **`FTDDamageRequest`** (line 478 — note: two D's, sixteen
characters, *not* the seventeen-character `FTDDDamageRequest`). My v1.1 review flagged this as a
third ambiguity the TD-09 erratum must settle, and reconciliation V3 §7's transcription of my
proposal renders the seventeen-character form.

**I re-derived these three spellings character by character before writing this section, because
my first draft of it merged two of them.** Lengths disambiguate them exactly:

| Spelling | Length | D-count after `FT` | Where it appears |
|---|---|---|---|
| `FTDamageRequest` | 15 | 1 | MEAD-C §5.4 line 476 |
| `FTDDamageRequest` | 16 | 2 | **MEAD-C §5.4 line 478** |
| `FTDDDamageRequest` | 17 | 3 | my proposal, reconciliation V3's transcription, `A1-R3` §5.2 |

**So MEAD-C's own two occurrences are themselves *different* lengths** — the canonical document
names one struct with a one-character difference on consecutive lines.

**`A1-R3` does not mention the inconsistency anywhere.** I counted the spellings in it:

| Spelling | Occurrences in `A1-R3` |
|---|---|
| `FTDDDamageRequest` (17) | **1** (in the accepted erratum) |
| `FTDamageRequest` (15) | **0** |
| `FTDDDamageRequest`'s 16-character sibling | **0** |

So `A1-R3` **silently selects `FTDDDamageRequest`** by reproducing my text without comment. That is
precisely the outcome the request tells me not to produce — *"Do not silently select one"* — and it
is the more insidious form of it: not a stated choice, but a citation that quietly fixes one variant
while the canonical document remains internally inconsistent.

**Condition C-03-1.** The TD-09 erratum must include an explicit clause naming the canonical
spelling, and `A1-R3` §5.2 must state that the spelling is a TD decision rather than a transcription
default. Proposed wording:

> **Erratum addition (3) — type name.** The damage request struct is named **`FTDDDamageRequest`**
> throughout; MEAD-C §5.4's `FTDamageRequest` at line 476 is a typographical error to be corrected
> in the same erratum. The spelling is settled here explicitly, not by reproduction of the diagram.
> TD may choose the other spelling; what may not happen is that it remains unstated.

I have no objection to `FTDDDamageRequest` as the answer — A1-R2 and A1-R3 both use it consistently,
which is a reason to prefer it. **My objection is to it being decided by accident.** Under a
canonicalisation decision this is exactly the class of question TD-12 exists to stop agents settling
unilaterally.

### 5.4 What I accept without condition in C-03

`RequestId`/`HitEventId`, dedupe on `(SourceEntityId, RequestId)`, `PostureDelta`, clamped `Amount`
with `bLethal` carrying overkill, the five published events, the six deliberately-unpublished
outcomes, A1 as sole publisher **including hits whose target is an A2-owned actor**, target-unload
drop, conditional `SourceContentKey`, per-source `SequenceNumber`, and the confirmation that
`ApplyDamage` returns the clamped applied delta.

**One note on my own interest, since the request asks me to verify the consumer rationale.** A1
publishing events for hits against A2-owned targets is the arrangement I asked for and it is also
the arrangement that makes my actors **not authoritative about their own damage**. I accept it
knowing that: my actors write health only after A1 authorises, and return the applied delta. If that
proves wrong, the failure mode is a health bar that disagrees with the event stream, and I would
rather have one publisher than one per owner. Recording the trade-off rather than presenting the
agreement as costless.

---

## 6. C-02 — field classification and the `CameraForward` removal — **AGREE WITH CONDITIONS**

### 6.1 The withdrawal is correct and the consumer rationale checks out

`A1-R3` §7.2 moves `CameraForward` to `A1-INTERNAL` and states the reason: its only concrete
consumer was **view-cone scoring in Agent 1's own interaction router**.

**I verified that against my own review rather than accepting it.** My v1.1 §4.3 withdrew
`CameraForward` because my only stated consumer, AI facing prediction, is better served by
`AimDirection`. So the field has **no consumer outside Agent 1** — mine withdrawn, and the one that
remains is A1's own router. Publishing it would violate the rule A1-R2 §4.4 applies to health.

**`A1-R3`'s rationale is accurate and it is stated as a consumer argument rather than as a
preference, which is what I asked for.** Condition met.

### 6.2 The promotions are justified by decisions I actually named

`A1-R3` §7.2 promotes `ControlState`/`ControlStateTag`, `bAllowsInput`/`bLocked`,
`HeightAboveGround`/`bOnWalkableFloor` from Conditional to REQUIRED, citing my §4.6. My §4.6 does
name those decisions:

| Field | My decision, as recorded in §4.6 | `A1-R3` cites it | Accurate |
|---|---|---|---|
| `ControlState`/`ControlStateTag` | boss must not punish during a `Cinematic` | yes | **yes** |
| `bAllowsInput`/`bLocked` | tutorial beat must not punish an unresponsive player | yes | **yes** |
| `HeightAboveGround`/`bOnWalkableFloor` | ledge-awareness at `CH01-SUB-005 Waterfall Escarpment` | yes | **yes** |
| `StateElapsedSeconds` | becomes required only if half-second pacing survives | yes | **yes**, stays CONDITIONAL |
| `GroundSlopeDegrees` | **none** — unrequested | yes | **yes**, A1-INTERNAL |
| `ActiveActionId` | **none** — unrequested, A1 may keep for telemetry | yes | **yes**, A1-INTERNAL |

**Six for six, no misattribution of my decisions.** Given that my own citation accuracy has been
the weak point in this exchange (§0.3), I checked each of these against §4.6 individually rather
than sampling.

### 6.3 Condition C-02-1 — the three narrowed fields must not leak back

`A1-R3` §7.2 states the consequence: the shared snapshot **shrinks**, with `CameraForward`,
`GroundSlopeDegrees` and `ActiveActionId` leaving it. That is correct and I want it pinned, because
`A1-INTERNAL` is a weaker guarantee than "not published" if a later version exposes it again for a
convenience consumer.

**Condition C-02-1.** The snapshot contract should state that `A1-INTERNAL` fields are **not part
of the published snapshot at all**, rather than that they are included and marked internal. Those
are different promises and only the first one can be tested.

### 6.4 Condition C-02-2 — `CombatState` versus the C-04 tag set

`A1-R3` §7.2 keeps `CombatState` in the REQUIRED shared set and does not say how it relates to the
seven `Status.*` tags C-04 relies on, or to the `State.Combat.*` namespace if MEAD-A is canonical.

This matters because `CombatState` is the field an A2 AI would read to answer "is this actor in
combat", while `Status.Staggered` etc. answer narrower questions. **Two overlapping representations
of the same state is the same defect class as the two-representation precedence table in §4.2.**

**Condition C-02-2.** `A1-R3` must state whether `CombatState` is (a) the coarse enum that the tag
set refines, or (b) a projection of the tag set. If (b), it must say it is derived and name the
derivation. Proposed wording:

> `CombatState` is the coarse projection of the actor's control state; the `Status.*` tags refine
> it. `CombatState` is derived and never authored independently, so a consumer that reads both can
> never observe them disagree.

### 6.5 What I accept without condition

Three-snapshot model, no merged state, three-layer read-only enforcement, `bInCombat` derived,
`EvaluatePhaseCondition(ConditionTag)`, invisibility of health and posture, `CarryState` **not
provided** (my withdrawal, unchanged), and `AimDirection` as the only facing signal.

---

## 7. C-05 — Option A+, and the case where it produces a wrong window — **DISAGREE**

### 7.1 What I accept, and why Option A is the right choice over Option B

`A1-R3` §3.2 chooses Option A and justifies it rather than asserting it. The justification is
correct and I had not stated it well myself:

> Option B's second axis is the *producer-local* stamp, which is only comparable between messages
> from the same producer; shipping it invites a consumer to compare local stamps across entities,
> which is precisely the defect being fixed.

**That is right, and it is a better argument than the one in my own §7.4.** A design that ships a
dangerous coordinate and documents it as "diagnostic only" will be read by a diagnostic tool that
compares it. One axis, one factor, one revision counter is harder to misuse. I agree with the choice.

I also accept, without condition:

- **`A1-R3` §3.1 withdraws the per-entity `T_e` rule for telegraph data.** The worked asymmetric
  example is my §7.3 case, reproduced correctly.
- **`A1-R3` §3.4 makes same-frame phase overlap normative contract text.** This is better than what
  I asked for in A2R-19. It forbids subtraction, cross-entity clock comparison, stale-endpoint
  interpolation, and late checks — four distinct wrong implementations, each named.
- **Factor capture with full re-emission, not piecewise integration** (§3.3b). Correct: integrating
  segments across a rate change is where implementations drift, and re-emitting a new reference
  point is the only approach that stays correct when two entities' rates diverge.
- **Half-open windows** `[WindupEndAxis, ActiveEndAxis)`, unchanged.

### 7.2 The axis definition is right, and it is right for a reason worth stating

`A1-R3` §3.2 defines the shared axis as **world gameplay time**: accumulated per frame as
`DeltaWorld * PrimaryDilation`, pause-aware, with **per-entity `CustomDilation` deliberately
excluded**.

That last exclusion is the correct call and it is the load-bearing decision in the whole design. If
per-entity dilation were in the axis, the axis would stop being shared and every entity would again
have a private clock — which is `A1-R2`'s defect reintroduced under a new name. Excluding it makes
the axis monotonic and comparable across every entity, which is the only property a shared
coordinate needs.

### 7.3 The defect: §3.3(a)'s conversion is inverted

**This is the disagreement, and it is arithmetic rather than a matter of design preference.**

`A1-R3` §3.3(a) states the conversion:

> Montage span between endpoints | axis endpoints | `local_span = (EndAxis − AxisNow) / ProducerRate`,
> **valid only while `TimingRevision` is unchanged and `ProducerRate` has not changed**

**Derive the correct conversion from `A1-R3` §3.2's own definitions.** The comment block defines:

- the axis advances per wall second by `PrimaryDilation`
- the local clock advances per wall second by `PrimaryDilation * CustomDilation(e)`

Therefore over any interval:

```
d(local) / d(axis)  =  CustomDilation(e)  =  ProducerRate   (for the producer)
=>   local_span  =  axis_span  *  ProducerRate
=>   axis_span   =  local_span / ProducerRate
```

`A1-R3` §3.3(a) prints `local_span = axis_span / ProducerRate` — **dividing where it must
multiply.** The error is invisible at `ProducerRate = 1.0`, which is why it survives casual
checking, and it grows as `1/rate²` exactly where the mechanism exists to help.

**Worked consequence, in the case Option A+ was built to fix.** Staggered attacker at
`CustomDilation = 0.05`, authored parry window 0.20 s of local (montage) time:

| Quantity | Value |
|---|---|
| Authored window, local | 0.20 s |
| EndAxis span on the shared axis, `0.20 / 0.05` | **4.00 axis-seconds** |
| Remaining local, as §3.3(a) computes it: `4.00 / 0.05` | **80.00 s** |
| Remaining local, true | **0.20 s** |
| Inflation | **400×** |

A consumer that implements §3.3(a) as written reports the window as **80 seconds** on an attack
whose parry window is a fifth of a second. The correct conversion shrinks the report to 0.20 s.

**And the two halves of §3.3 disagree with each other**, which is how I am confident this is a
transcription error rather than a design error. §3.3(b)'s retime rule recomputes `*EndAxis` so that
the phase endpoints stay correct — which requires `axis_span = local_span / rate`, the inverse.
Tested at a retime from rate 0.5 to 0.2 with 0.800 s local remaining:

| Method | New `EndAxis` |
|---|---|
| §3.3(b) as written (implies `AxisNow + RemainingLocal/rate`) | **4.40** |
| §3.3(a)'s formula applied after the retime | **20.00** |

**So §3.3(b) and §3.3(a) cannot both be right, and §3.3(b) is the correct one.** The retime rule
works; the table that consumers are meant to implement does not.

### 7.4 The specific wrong behavior the review request asks me to find

| Scenario the request names | Does Option A+ handle it? |
|---|---|
| **Asymmetric dilation** | **No — this is the defect.** §3.3(a) inflates by `1/rate²`; at rate 0.05 a 0.20 s window reads as 80 s |
| **Pause / unpause** | **Definitionally yes** (axis pause-aware), **operationally incomplete** — see §7.5 |
| **Primary dilation change** | **Yes** — a `Retimed` fires; the axis is unaffected because it is integrated from `PrimaryDilation`, not assumed constant |
| **Repeated retiming** | **Monotonic revision, no overflow concern**; each retime is a replacement, and replacing repeatedly is idempotent given the last block. Correct |
| **Missed / delayed retiming** | **Detected but not recoverable** — see §7.6 |
| **Phase transition** | **Yes** — half-open intervals, `Active` = `[WindupEndAxis, ActiveEndAxis)` |
| **Stale timing revision** | **Detected**; consumer must not interpolate. Correct as far as it goes |

**One more case, which the request does not list and which I checked:** if the consumer converts
using **its own** `CustomDilation` instead of `ProducerRate` — a natural mistake, since the consumer
knows its own rate and the field name is longer than the concept — then at producer rate 0.5, a
1.00 s remaining axis span converts to 1.00 s instead of 0.50 s, doubling the window. The correct
field is `ProducerRate` and §3.3(a) does name it. **But because §3.3(a)'s formula is itself
inverted, a consumer that follows the table and a consumer that follows the field name are wrong in
opposite directions.** Fixing the formula matters for more than the formula.

### 7.5 Pause: the axis is pause-aware, but `RemainingLocalSeconds` is not self-sufficient

`A1-R3` §3.3(a) says a consumer that only needs "how much window is left" reads
`RemainingLocalSeconds` and **"requires no arithmetic on another entity's clock"**.

That is true at the instant of emission and false one frame later. `RemainingLocalSeconds` is a
snapshot. To age it, a consumer must integrate the **producer's** local rate over axis time. The
contract does not say so, and two consumers can both conform while disagreeing:

| Consumer behaviour | Result after a 10 s world pause mid-window |
|---|---|
| Decrements by **wall** time | window reported **10 s shorter** than it is — closes early |
| Decrements by **axis** time × `ProducerRate` | correct |

The axis is pause-aware, so the *second* is achievable. Nothing in `A1-R3` requires it, and the
sentence "no arithmetic on another entity's clock" actively discourages the consumer from
realising that arithmetic is needed at all.

**In a paused game the parry outcome is unaffected** — §3.4's live-state overlap test does not read
this field. So this is a **UI and AI-reaction defect, not a parry defect.** I am stating that
precisely because overstating it would be the easy way to win the point, and the request asks me to
find incorrect **parry** outcomes specifically. The parry outcome is safe here (§7.7).

### 7.6 Missed or delayed `Retimed`: detected, but the only defined fallback is a stall

`A1-R3` §3.3(c)4 is honest about the mechanism: a consumer seeing revision `k` when it holds `k−2`
knows it missed a retime and **must not interpolate**. It re-queries **if a query surface exists
(U-07, still open)** or **treats the phase as unknown**.

Both branches are safe in the sense of not producing a wrong answer. The problem is that the second
branch is the only one **currently defined**, because U-07 is unresolved. Modelled at a retime from
rate 0.5 to 0.2:

| Axis position | Stale consumer (rev 1) | Truth (rev 2) |
|---|---|---|
| 1.00 | 2.00 s remaining | 77.00 s remaining |
| 2.00 | **0.00 — window closed** | 72.00 s remaining |
| 3.00 | 0.00 | 67.00 s remaining |

A stale consumer closes the window at axis 2.0 while it is genuinely open until axis 16.4. **The
parry outcome is still safe** (§7.7), but every scheduling, UI and AI consumer driven from this
block is wrong for the rest of the telegraph, and the only sanctioned response is "treat the phase
as unknown" — a gameplay stall rather than a resolution.

**This is not a defect in `Retimed`; it is a consequence of U-07 being open.** But `A1-R3` §3.3(c)4
presents the uncertainty as handled, and it is handled only if a query surface exists. **Condition
C-05-2** makes that dependency explicit rather than implied.

### 7.7 What is genuinely safe, stated so the disagreement is not overread

**The parry outcome cannot be corrupted by any timing defect in §3.3, and that is because §3.4 is
correctly designed.** Same-frame phase overlap against live state reads neither the axis endpoints
nor `RemainingLocalSeconds` nor `TimingRevision`. So both the inverted formula (§7.3) and the stale
revision (§7.6) produce wrong *numbers* and not wrong *parries*.

I want that on the record because it bounds my disagreement. **`A1-R3` §3.4 is the single best
clause in the document** and it is the reason C-05's defect is a **reporting** defect rather than a
gameplay defect. My DISAGREE is not "the parry rule is wrong" — it is "the numbers every other
consumer reads are wrong, and the document presents them as settled."

### 7.8 Verdict and exact replacement wording

**DISAGREE on C-05 as written**, on §3.3(a) alone. Everything else in §3 is accepted, including the
axis definition, Option A over B, the retime semantics, and the normative parry text.

> **`A1-R4` §3.3(a) — replacement row (proposed).**
> Montage span between endpoints | axis endpoints | **`local_span = (EndAxis − AxisNow) × ProducerRate`**,
> valid only while `TimingRevision` is unchanged and `ProducerRate` has not changed.
> *Derivation:* the axis advances by `PrimaryDilation` per wall second and the local clock by
> `PrimaryDilation × CustomDilation(e)`, so `d(local)/d(axis) = CustomDilation(e) = ProducerRate`.
> A consumer must **multiply** by `ProducerRate`; dividing inflates the span by `1/ProducerRate²`
> and is the defect this clause exists to prevent.

> **`A1-R4` §3.3(a) — addition on aging `RemainingLocalSeconds` (proposed).**
> `RemainingLocalSeconds` is authoritative **at emission only**. To age it, a consumer decrements
> it by **axis elapsed × `ProducerRate`**, never by wall-clock elapsed. A consumer that ages it by
> wall time reports a window shorter than it is across any pause or dilation change. Consumers that
> need `RemainingLocalSeconds` must therefore track `AxisNow` even though §3.3(c)3 says they need no
> cross-entity arithmetic; what they do not need is arithmetic on **another entity's** clock.

**Condition C-05-1.** §3.3(a) corrected as above, with the derivation stated in the contract so the
next reader does not have to re-derive it.

**Condition C-05-2.** §3.3(c)4 must state that a revision gap is **unrecoverable without U-07's
query surface**, so that U-07 is recorded as a blocker for the retime mechanism and not only as an
open question about late subscribers. Alternatively, define the recovery: the producer republishes
its current timing block on request.

**Two closing notes on the disagreement.** First, this defect would have been invisible to the test
`A1-R3` §8.1 accepts from me — `AsymmetricDilationTimestampComparability` compares the producer's
and consumer's *computed* remaining window, and if both use the same inverted formula they agree
with each other while both being wrong. **The test as written is necessary and not sufficient**, and
it should be amended to compare against the **authored** local window. Second, `A1-R3` §3.3(a)'s
row is the only place in the whole document where a formula appears, and it is the only place with
an arithmetic error. That is a coincidence worth noting, not a pattern.

---

## 8. C-06 — router ownership, opt-in progress, terminal calls — **AGREE**

### 8.1 All four required properties verified

| Requirement | `A1-R3` position | Satisfied |
|---|---|---|
| Router owns hold duration and progress | unchanged from `A1-R2` §8, retained | **yes** |
| Progress is opt-in, `bWantsProgress` default false | retained | **yes** |
| Exactly-once terminal call, `ProtocolViolation` on misuse | retained | **yes** |
| End / cancel lifecycle incl. `TargetUnloaded`, forced-state, level transition | full cancellation table retained | **yes** |
| Progression granted by neither router nor interactable | retained | **yes** |

### 8.2 Damage interruption — correctly *not* assumed, and I confirm my position has not moved

The request asks me to verify the unresolved damage interruption. `A1-R3` §7.1 says the
damage-interrupt question "stays escalated, and it is not a clause I rely on", and §9.1 U-08 records
it as `TD/design`, "unchanged — escalated, not assumed".

**That is the correct handling and I confirm it against my own instruction not to assume it is a TD
decision.** It is not one. Nothing in `A2-C01…C07-1.0` §8 makes damage a cancellation cause, and I
have not added one in this review. **If TD rules that damage interrupts holds, it adds a row to the
cancellation table; if it rules that it does not, nothing changes.** C-06 is agnostic, which is why
it can be agreed while U-08 is open.

### 8.3 Source destruction, unload, exactly-once

Unchanged from the text I accepted in v1.1 §8.5, and `A1-R3` does not alter it. My actor unregisters
on stream-out; A1 must not hold a session against an invalid pointer; `Cancel(TargetUnloaded)` is
the ordering. Accepted.

### 8.4 Conditions on C-06

**None.** This is a clean AGREE for the second time. `A1-R3` changed nothing in C-06 and nothing
needed changing.

---

## 9. C-07 — namespace collisions, conditionality, persistence — **AGREE WITH CONDITIONS**

### 9.1 What `A1-R3` fixed, and it is the thing I asked for

My v1.1 condition on C-07 was that "yield to MEAD" was not an executable instruction while three
documents carried the identity, so every yield clause had to become conditional.

`A1-R3` §4.1 does exactly that, in the strongest form available to an agent that does not own the
decision:

> **Every "yield to MEAD" clause in `A1-R2` §9.3 and every MEAD citation in `A1-R2` is conditional
> on the Technical Director declaring one exact canonical file at one exact commit.** Until that
> declaration exists, those clauses are **proposals awaiting a referent**, not settled resolutions.

**That is unambiguously conditional and it is the correct response.** `A1-R3` also states it has
not moved, deleted, renamed, archived, overwritten or edited any MEAD, which I verified by checking
that no branch has a MEAD modification commit in this exchange.

### 9.2 The MEAD-A finding `A1-R3` makes is correct and it is the most important line in its §4

> **MEAD-A's arbiter is a world subsystem.** Under MEAD-A, "yield to MEAD" on C-03 means yielding
> arbitration to a *world* owner — which would contradict the Technical Director's own integration
> decision that Agent 1 owns hit arbitration for hits involving the player.

I verified this directly. MEAD-A line 484:

> **Hit arbitration is single-owner.** Only `UTDDHitArbiter` (a world subsystem) decides
> Hit/Blocked/Parried.

**This is a genuine contradiction between MEAD-A and the accepted ownership decision, not an
authority question**, and `A1-R3` is right to distinguish the two and to state that **the TD
decision outranks all three MEADs.** Any canonicalisation that picks MEAD-A therefore requires an
erratum at line 484 of the same kind TD-09 contemplates for MEAD-C §5.4. `A1-R3` §4.3 says so.

I record my own position here for the same reason the request asks me to keep the authorship
disclosure visible: **MEAD-A is my document, and its arbiter clause contradicts the ownership split
I have spent three reviews arguing for.** I am not going to defend my own document against the
decision. If MEAD-A is declared canonical, line 484 needs the erratum and I will say so in writing
as its author.

### 9.3 Condition C-07-1 — the contingency map is incomplete (§4.3)

Fully covered in §4.3 above and not repeated. In summary: `A1-R3` §4.3 maps one of seven retained
`Status.*` tags under MEAD-A. Four of the seven have no MEAD-A equivalent, one has a semantically
different equivalent, one is on a different axis. Under MEAD-A's **"Prohibition: no agent
introduces a tag namespace"** (line 517), those become namespace requests rather than renames.

This is a C-07 condition as well as a C-04 condition because C-07 is the contract that owns the
namespace disposition. **The mapping must be complete before TD-12 can be answered usefully**,
otherwise the decider is choosing a canonical file without seeing what that choice costs.

### 9.4 Condition C-07-2 — TD-13 deferral accepted, with one boundary

`A1-R3` §6 accepts the deferral and proposes exact dependency wording, including:

> Until both exist: **no interactable ID family is defined, no interactable state is persisted, and
> C-06's interaction lifecycle uses actor-lifetime identity only** (`TWeakObjectPtr` + validity
> rule)

**Accepted in full, and it is the right boundary.** It is also, notably, a commitment to *not*
invent something, stated as a clause — which is the correct form for a deferral.

The one boundary I add: `A1-R3` §6 says a "yes, interactables persist" answer "does not unblock C-07
by itself". I confirm that from my side and extend it: **C-07 needs three separate answers** — the
save schema (TD-13), the namespace decision (TD-12), and a retirement policy — and any one of them
alone unblocks nothing. There is no ordering that shortcuts the other two.

### 9.5 What I accept without condition

Three identity classes, `P1`–`P5` opacity rules, loud retirement failure, the eight-row collision
analysis subject to §4.3's completeness, the tombstone-never-reuse requirement, unknown-tag as an
author-time error, and — importantly — that **no competing registry is created and no persistence
requirement is invented.** `A1-R3` creates neither. `Status.Dead` is a **request to the registry
owner**, which is the correct mechanism and the one MEAD-A line 517 mandates.

### 9.6 The `Status.Dead` request is well formed but is not a solution

Restating the §4.2 conclusion in C-07 terms: the request is properly addressed and correctly not
created. It is not a solution to the precedence problem until the registry owner acts, and `A1-R3`
does not present it as one — §2.2 documents the fallback and its limits. Accepted.

---

## 10. The MEAD comparison, taken as the request requires

I do not choose a canonical MEAD and I make no TD decision. What follows is the consequence map.

### 10.1 What each candidate is, verified from the files

| | **MEAD-A** | **MEAD-B** | **MEAD-C** |
|---|---|---|---|
| Formal identity | `TDD-MEAD-001` v1.0 | **none** | `TDD-MEAD-001` v1.0 |
| Lines | 1,078 | 247 | 1,231 |
| Author | **me** (disclosed) | unstated | Agent 1 |
| §5.4 damage pipeline | **absent** | **absent** | **present** |
| `Status.*` vocabulary | **absent** (`Status.` count: 0) | **absent** | **7 tags** |
| Tag vocabulary | `State.Combat.<InCombat\|Staggered\|Downed\|ParryWindow\|Invulnerable>`, `State.Locomotion.*`, `World.Interactable.*` | none | `Status.*`, `Damage.Physical.*` |
| Damage type | `ETDDDamageType` **enum** | validated event | `FGameplayTag` |
| Hit arbitration | **`UTDDHitArbiter`, world subsystem, single-owner** | "one owner per attack window" | victim-side branch after `ApplyDamage` |
| Tag governance | **§6.6, explicit prohibition** (line 517) | none | absent |
| `<Dead>` | enemy AI StateTree state only (§8.2 line 615) | — | character-state value |
| §5.5 hitstop | **absent** (has 5.1–5.3 only) | absent | present |

### 10.2 Where `A1-R3` would need to change, by candidate — and what kind of change it is

`A1-R3` §4.3 gives this table and it is accurate but incomplete. Below is my reading, with each row
classified as **rename**, **semantic change**, **new request**, or **contradiction**.

| Clause | Under MEAD-C | **Under MEAD-A** | Class | **Under MEAD-B** | Class |
|---|---|---|---|---|---|
| C-04 seven retained tags | fixed vocabulary | 2 exact, 1 window-vs-state, 1 wrong axis, 3 absent | **rename + semantic + new request** | nothing to yield to | **all new requests** |
| C-04 `Dead` | request | request, and `State.Combat` has `Downed` not `Dead` | **new request** | request | **new request** |
| C-03 damage types | `Damage.Physical.*` tags | `ETDDDamageType` enum | **semantic change** — different contract shape | none | **new request** |
| C-03 / TD-09 arbitration | victim-side branch after `ApplyDamage` | **`UTDDHitArbiter` world subsystem decides** | **CONTRADICTION** with the accepted ownership split | no §5.4 | **erratum becomes "record the split"** |
| C-01 / §9.2 verb tags | naming open | closed namespace list, no verb namespace | **new request** | no referent | **new request** |
| C-05 hitstop citation | §5.5 pair dilation | **no §5.5** | **citation void** — design rests on TD-06 argument alone | none | **citation void** |
| C-07 tag governance | **absent** | **§6.6 prohibition, explicit** | **stronger constraint** — no agent may introduce a namespace | none | no constraint |

### 10.3 Contradiction versus unresolved authority — the distinction the request asks for

Three of these are genuinely different in kind and should not be collapsed:

1. **A real contradiction exists only if MEAD-A is canonical**: line 484 gives arbitration to a
   world subsystem, while the accepted TD split gives it to Agent 1 for player-involving hits. That
   is two normative statements that cannot both hold. **It is not an authority question** — both
   are normative; one must be amended. `A1-R3` §4.4 states this correctly.

2. **An unresolved authority question** is TD-12 itself: which file governs. No agent may answer it
   and `A1-R3` does not. Correct.

3. **A void citation is neither.** C-05's appeal to §5.5 hitstop has no referent under MEAD-A or
   MEAD-B. That is not a contradiction — nothing in those documents says hitstop works differently —
   it is the **absence of support for a design that stands on its own argument anyway.** The
   consequence is that C-05 becomes *less citable* and not less correct, and TD-06 should know it
   is deciding without a MEAD basis if A or B is chosen.

**I flag 3 because `A1-R3` §4.3 lists it as "unverifiable" and then treats it exactly like the
contradiction in row 4 of its table.** Under MEAD-A, C-05's pair-hitstop design would have **no
expression in the canonical architecture at all** — not a wrong one, none. That is worth stating
separately because a decider reading "unverifiable" will assume it means "probably fine".

### 10.4 My recommendation, offered as a nonbinding input and not a decision

I do not choose. But the request asks me to evaluate consequences accurately, and an evaluation that
refuses to draw a conclusion from itself is not one.

**If TD-12 is answered at all, MEAD-C is the least costly canonical choice for this contract set** —
not because it is the newest (it is not; MEAD-A's tip has later commits) and not because it is
better (I have no basis for that and I authored a rival), but because:

- it is the only candidate with §5.4, so TD-09's erratum has a target;
- its tag vocabulary is the only one that accommodates six of the seven retained tags without new
  requests;
- it does not contain MEAD-A's line 484 arbiter clause, so choosing it **avoids the contradiction
  entirely** rather than resolving it.

**The cost of choosing C is real and should not be understated:** MEAD-A carries the UE 5.8
commitment, its own combat contract and the seven-memory sequence, and none of that transfers. So
choosing C for the contracts is not choosing C as *the* architecture — and reconciliation V3 §5.4
already frames it that way, as a narrow reference for the §5.4/TD-09 work, which is a better framing
than mine.

**I am disclosing again that I authored MEAD-A and am recommending against it for this purpose.**
The reason is in §9.2: its arbiter clause contradicts the ownership split I have argued for in three
consecutive reviews. Defending my own document would require me to abandon that argument, and I am
not going to do that quietly.

---

## 11. What I am asking for, in one list

| ID | Ask | Contract | Owner | Kind |
|---|---|---|---|---|
| **A2R-22** | `§3.3(a)`: multiply by `ProducerRate`, not divide; state the derivation | C-05 | A1 | **Correction** |
| **A2R-23** | `§3.3(a)`: state `RemainingLocalSeconds` ages by axis×rate, not wall time | C-05 | A1 | **Addition** |
| **A2R-24** | `§3.3(c)4`: record U-07 as blocking the retime mechanism, or define republish-on-request | C-05 | A1 + TD | **Dependency** |
| **A2R-25** | `§5.2`: name the request-struct spelling as a TD decision, do not select by transcription. **Three distinct spellings exist across 15/16/17 characters** | C-03 | A1 + TD | **Correction** |
| **A2R-26** | `§4.3`: extend the MEAD-A column to all seven retained tags plus `Dead`; distinguish rename / semantic / new request | C-04, C-07 | A1 | **Completeness** |
| **A2R-27** | `§2.2`: state that `Dead` is the only non-tag precedence value if the registry declines | C-04 | A1 | **Addition** |
| **A2R-28** | `§7.2`: state that `A1-INTERNAL` fields are excluded from the published snapshot, not included-and-marked | C-02 | A1 | **Clarification** |
| **A2R-29** | `§7.2`: state whether `CombatState` is coarse projection or derived from the tag set | C-02 | A1 | **Clarification** |
| **A2R-30** | Amend `AsymmetricDilationTimestampComparability` to compare against the **authored** local window, not producer-computed vs consumer-computed | C-05 | A1 + me | **Test amendment** |

**Ten asks, of which one is a correction that blocks signature (A2R-22), one is a correction to
citation discipline (A2R-25), and eight are additions or clarifications that a successor can carry
without redesign.** None requires a TD ruling except A2R-25's naming decision and A2R-24's
dependency, both of which are already TD-owned.

**A2R-30 is mine as much as Agent 1's.** I proposed that test; it does not catch the defect it was
meant to catch; I am amending my own ask.

---

## 12. Evidence

### 12.1 Executed — 11 analysis checks, run bare, in this session

**None of these is a contract acceptance test.** Each evaluates a formula or a document against the
files. §12.3 states which are load-bearing.

| # | Check | Method | Result |
|---|---|---|---|
| 1 | `§3.3(a)` conversion is inverted | derived `d(local)/d(axis)` from §3.2's own definitions; computed at rates 1.0 / 0.5 / 0.05 | **inverted**, error `1/rate²` |
| 2 | Worked asymmetric case at rate 0.05, 0.20 s window | arithmetic | **80.00 s reported vs 0.20 s true, 400×** |
| 3 | `§3.3(a)` vs `§3.3(b)` consistency | applied both to a retime from 0.5 to 0.2 | **disagree: 20.00 vs 4.40** |
| 4 | Stale-revision divergence over axis positions | modelled rev-1 consumer against rev-2 truth | **window closes at axis 2.0 vs true 16.4** |
| 5 | Pause-aging ambiguity | modelled wall-decrement vs axis-decrement across a 10 s pause | **10 s error in one, not the other** |
| 6 | MEAD-A has no `Status.*` | full-text extraction | **0 matches** |
| 7 | MEAD-A equivalent for each of 7 retained tags | per-tag search | **2 exact, 2 semantic, 3 absent** |
| 8 | MEAD-A `Dead` | full-text, context read | **enemy AI state only (line 615)** |
| 9 | MEAD-A §5.5 hitstop | heading scan 5.x | **absent; has 5.1–5.3 only** |
| 10 | MEAD-A §6.6 tag rule + prohibition | read line 500, 517–518 | **present; "no agent introduces a tag namespace"** |
| 11 | Request-struct spellings across all three sources | character-level extraction, disambiguated by string length | **15 / 16 / 17 chars: `FTDamageRequest`, `FTDDamageRequest`, `FTDDDamageRequest`. MEAD-C's two occurrences differ; A1-R3 uses only the 17 form once** |

### 12.2 The repository suite — executed, and it tests my documents, not `A1-R3`

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/canon/tests` | **114 OK** | 0 |
| `python3 -m unittest discover -s Tools/world/tests` | **396 OK** | 0 |
| `python3 Tools/ci/l0_checks.py` | **14/14** | 0 |
| `python3 Tools/world/contract_data_checks.py` | **9/9** | 0 |
| `python3 Tools/world/gen_evidence.py` | **14/14** | 0 |

These pass because my own documents and data are consistent. **They say nothing about `A1-R3` and I
make no such claim.**

### 12.3 Evidence categories, kept separate as the request requires

| Category | Count | Executed? |
|---|---|---|
| (a) Analysis checks in this review | 11 | **Yes** — §12.1 |
| (b) Repository suite (canon / world / L0 / data checks / evidence) | 114 / 396 / 14 / 9 / 14 | **Yes** — §12.2 |
| (c) Document tests locking my prior reviews | 43 + 55 | **Yes** |
| (d) `A1-R3`'s proposed suites | 16 suites, ~104 cases | **No — 0 run, 0 written** |
| (e) Contract acceptance tests | 42 mine + `A1-R3`'s | **No — 0 run** |
| (f) Tests A1 or A3 ran | unknown to me | **Not claimed** |

### 12.4 What I did not do

- I did not run any `A1-R3` test. None is implementable here; there is no clock, no arbiter, no
  telegraph, no registry and no Unreal project.
- I did not claim Agent 3 or Agent 1 ran my tests. `A1-R3` §9.3 correctly attributes my figures to
  me, and I attribute its figures to it.
- I did not build, measure or profile anything. **The `1/rate²` figure is arithmetic on a stated
  formula, not a measurement of an implementation.** No implementation exists to measure.
- I did not select a canonical MEAD, issue an erratum, register a tag, or make any TD decision.

### 12.5 Tests added by this review

Recorded here rather than in the summary, because the request asks for tests **actually executed**.

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_review_r3.py"` | **42 OK** | 0 |

`Tools/world/tests/test_contract_review_r3.py` locks this document's claims:

| Test class | What it pins |
|---|---|
| `TestConversionIsInverted` | The §7.3 derivation, the `1/rate²` factor, the 400× worked case, and that §3.3(a) and §3.3(b) part company — **the blocking finding** |
| `TestA1R3FormulaAsWritten` | That my quotation of §3.3(a)/§3.2 matches `A1-R3` verbatim, so the disagreement is with the text and not with my paraphrase |
| `TestSpellingSilentlySelected` | The three spellings across three sources, disambiguated by string length |
| `TestMeadAClaims` | No `Status.*`, the `State.Combat.*` values, the §6.6 rule and prohibition, `Dead` as an AI state, no §5.5, the world-subsystem arbiter |
| `TestMeadC` | Seven tags, no `Dead`, §6.6 is the chapter pipeline, **§5.4's two occurrences are different lengths** |
| `TestReviewSelfConsistency` | 7 verdicts, verdict distribution, 0 signed, A2R-22…30, sequential §-numbers, no interactable count, no repeat of the three-MEAD error |
| `TestRejectionsAndAcceptances` | That §1.4 accepts `A1-R3` §0.5 and rejects §7.4, and that five own errors are recorded |
| `TestPreservation` | Prior reviews and the submission are unchanged |

**Two tamper proofs run.** Breaking `Signed: 0 of 7` in either location fails
`test_zero_signed`; restoring passes. And the arithmetic tests are direct assertions on the
formula, so correcting §3.3(a) in a future version would fail them — which is the intended
behaviour, because the tests exist to pin *what this review claimed*, not to defend it.


---

## 13. Method and limits

### 13.1 What this review does not establish

| Not established | Why |
|---|---|
| That any contract is agreed | §1.3 — 0 of 7 signed; four open TD items sit inside them |
| That `A1-R3` accepts anything here | Agent 1 has not seen this document |
| That TD accepts anything here | v1.2 predates it |
| That C-05's fix works | It is a derivation, not a measurement |
| That the parry outcome is wrong | **It is not** — §7.7; only the reported numbers are |
| That MEAD-C should be canonical | §10.4 is a nonbinding consequence argument, not a decision |
| That M0 is complete | no `.uproject`, no `Source/`, no build |

### 13.2 Limits of the C-05 disagreement specifically

The defect is arithmetic on `A1-R3`'s **written** formula. If Agent 1's implementation multiplies
while the document divides, the software is right and the document is wrong — and the document is
what contractors implement from. Conversely, if `EndAxis` is stored such that
`EndAxis − AxisNow` is **already** local time rather than axis time, then §3.3(a)'s division would
be correct and §3.3(b)'s recomputation would be the defective one. **A2R-22 asks for the derivation
to be stated in the contract precisely so that this is settled by the text and not by my reading of
it.** Either answer closes the disagreement; I have no stake in which, beyond wanting it written
down.

### 13.3 Where my own record stands

Three reviews, and the correction count on my side is now:

| # | My error | Found by |
|---|---|---|
| 1 | Claimed TD v1.2 did not exist | my own A1-R1 review, before publication |
| 2 | Nearly claimed A1 fabricated its MEAD citations | my own all-refs search, before publication |
| 3 | Said all three MEADs identify as `TDD-MEAD-001` v1.0 | **Agent 3, recon V3 §5.1** |
| 4 | Miscounted my own clause verdicts (44/29/11 → 61/56/5) | my own tests, before publication |
| 5 | **Attributed MEAD-A's §6.6 tag rule to MEAD-C** | **Agent 1, `A1-R3` §0.5** |

**Two of five were caught by another agent, and both were citation errors rather than reasoning
errors.** That is the specific failure mode §13.4 addresses, and it is worth noting that I found
none of the five by re-reading my own work — every one came from a test, a search, or someone else.

### 13.4 The procedure change this review makes

My v1.1 correction added "search every reachable ref before asserting absence". That fixed
existence and **did not fix citation**, which is why error 5 happened after it.

The addition: **every section reference I cite must be produced by the same command that located
the text, not written from memory afterwards.** Concretely — locate the passage, print its section
heading and its line number together, and paste from that output. §0.3 of this review was produced
that way, and so were the MEAD-A rows in §10.1. It is a smaller rule than it sounds, and it is the
one that would have caught errors 3, 4 and 5.

---

## 14. Publication

### 14.1 Provenance

| Field | Value |
|---|---|
| Document | `Docs/AGENT2_REVIEW_A1R3_V1.md` — **new file** |
| Branch | `arena/5dde91a4-tdd` (existing; no new branch, no merge) |
| Reviewed | `A1-R3` v1.2, commit `70db9665b677…` |
| My prior review | v1.1 at `c726096deeef…` — **the basis**; v1.0 at `4220b82` preserved unchanged |
| My submission | `A2-C01…C07-1.0`, `3ac438b` — **unchanged** |
| Governing TD | v1.2, `e121bbb` |
| Reconciliation | v3.0, `98399af` |
| MEADs | read only; **none moved, deleted, renamed, archived, overwritten or edited** |
| Code, Core types, project | **none created** |
| Merge / API freeze / M0 / tag created / erratum issued / MEAD chosen | **none** |
| Contracts signed | **0 of 7** |

### 14.2 Preservation

| Artifact | Status |
|---|---|
| `AGENT2_REVIEW_A1R1_V1.md` (`93b2f07`) | unchanged |
| `AGENT2_REVIEW_A1R2_V1.md` v1.0 (`4220b82`) | **unchanged** — superseded, not rewritten |
| `AGENT2_REVIEW_A1R2_V1.md` v1.1 (`c726096`) | unchanged — this review builds on it |
| `CONTRACT_SUBMISSION_A2_V1.md` (`3ac438b`) | unchanged |
| 57/57 location capture, provenance to register v2.9 | preserved; **register not modified** |
| Interactable and prop totals | **still withdrawn; no count stated anywhere in this document** |
| `scene_register_ch01_full.md` | **not edited** |

### 14.3 Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-17 | Review of `A1-R3` v1.2 at `70db966`. Seven verdicts: 2 AGREE (C-01, C-06), 4 AGREE WITH CONDITIONS (C-02, C-03, C-04, C-07), 1 DISAGREE (C-05). **0 of 7 signed.** C-05 disagreement is §3.3(a)'s inverted conversion, demonstrated at `1/rate²` and worked at 400× on the case the mechanism exists to fix. Accepted `A1-R3` §0.5's correction of my MEAD-A §6.6 misattribution (my fifth error). Rejected `A1-R3` §7.4's claim that C-03 and C-06 are "already there". Ten asks (A2R-22…30), one blocking. MEAD consequence map completed for all seven retained tags under MEAD-A. 11 analysis checks executed; 0 contract tests run. |

**This document is a review, not a contract.** It agrees nothing, signs nothing, freezes nothing,
chooses no canonical MEAD, issues no erratum, and authorises no implementation.
