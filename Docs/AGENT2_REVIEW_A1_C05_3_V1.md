# AGENT 2 — INDEPENDENT REVIEW OF AGENT 1'S TELEGRAPH AUTHORITY RESPONSE

**Review ID:** `TDD-A2-REVIEW-A1C05-3-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — no C++, no contract freeze, no signature, no signature change,
no canonical MEAD selection, no TD decision taken. **U-07 and C-05 are not closed by this review
and I do not claim they are.**

---

## 0. Provenance and what was actually read

Every reference below resolved from a command, not from a summary. The commands are in §0.4
because my own §11.4 countermeasure from the `A1-R4` review is exactly what failed here (§0.3).

### 0.1 The exact objects under review

| Role | Document | Commit | Blob | Lines |
|---|---|---|---|---|
| **Reviewed — Agent 1's response** | `docs/AGENT1_C05_3_TELEGRAPH_AUTHORITY_RESPONSE_V1.md` | **`22c29daddc3b7a9285ceb4709113d9657ddbe0bd`** | **`a94b49efb65c671c6c9fc8bb56436778aeb7030b`** | 584 |
| **Reviewed — Agent 3's recommendation** | `docs/AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md` | **`58ec7fd4bacbaaddf55f64e3e784de5c3fc8b0e6`** | **`79b79e30263b905262672993f4e3e8943df5d921`** | 56 |
| **Referenced — the exact `A1-R4` blob named in the task** | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md` | `142cabdd62bbe23e8a2d64f2ec0586d8b69ba6c6` | **`2cc548faf86cb9b30cd2e26386fc672edbdd9f75`** | 557 |
| My prior review (A2R-31…A2R-35) | `Docs/AGENT2_REVIEW_A1R4_V1.md` | `7ea0a85cc5e1d9bfe6aff4fc861f041f01c30cc1` | — | 1,002 |
| `A1-R3` (source of the normative parry text) | `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md` | `70db9665b67723a526a6d40fa71ec832f1a95498` | `109331f36eddce7eee068aa278a474c07c950753` | — |
| M1 v1.4 | `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` | `22c29dad…` | — | 1,042 |
| MEAD-C (candidate) | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | `169a8d8f4f95dca526239dfbf744e97590504a70` | **`f49354631c86601e9311865901bf1fcd44846d89`** | 1,231 |
| MEAD-A (candidate — **mine**) | `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` | `912fac9f76a1011f8c823b368a92a0edf059a283` | — | 1,078 |
| MEAD-B (candidate) | `docs/MASTER_ENGINEERING_ARCHITECTURE.md` | `58ec7fd…` (Agent 3 branch) | — | 247 |

**Branch note.** Agent 1's branch moved twice during this review: `142cabd` → `13a2f43` (document
created) → `22c29da` (commit and blob recorded in §11). The document blob changed from
`de01831ef392bbcd4c3217d59f4ce9eda9bcdafe` to `a94b49efb65c671c6c9fc8bb56436778aeb7030b`. **I review
`a94b49ef…` at `22c29dad…`**, the current head, and I state which one I signed nothing against.

### 0.2 The four supplied inputs, and where each one actually lands

| Input the task names | Status in the reviewed response | My note |
|---|---|---|
| Agent 3's C-05-3 recommendation, `58ec7fd` | Traced item by item in A1 §12.1, all 19 rows. **I verified the seven MEAD-C citations independently** (§2.2) | Accurate |
| A1-R4 blob `2cc548fa…` | Treated as the baseline; §4.1's broker quoted and then relocated | Accurate, and the blob is unchanged on the branch |
| My A2R-32…A2R-35 | All five answered with clause text in A1 §8 | Four accepted as written; A2R-35 accepted with a dependency I flag in §7.4 |
| M1 v1.4 `IsTelegraphingAttack` / `C-02 bIsTelegraphing` | Used as the precedent for the smaller alternative (§2.4, §10.1) | **Verified exact at M1 lines 796–797** |

### 0.3 I was wrong, and Agent 1 caught it correctly

This belongs at the top, not in an appendix.

`A2R-31`'s review states in three places (`AGENT2_REVIEW_A1R4_V1.md` lines 78, 566, 801, 850, 905)
that `A1-R4` §7.1 miscites MEAD-A line 505 for `State.Locomotion.Cinematic`. **It does not.**

```
$ git rev-parse origin/a1branch:docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md
2cc548faf86cb9b30cd2e26386fc672edbdd9f75          # the exact blob the task names
$ git show 2cc548fa… | grep -c "505"
0
$ git show 2cc548fa… | grep -n "Locomotion.Cinematic"
277:| `Status.Cinematic` | present, line 429 | `State.Locomotion.Cinematic` (506) | **CONTRADICTION** | …
```

A1-R4 §7.1 writes **(506)**. It contains no occurrence of "505" at all. My review attributed to
Agent 1 a citation error Agent 1 did not make.

**Root cause, stated because the countermeasure should have prevented it.** MEAD-A line 505 *is*
`Chapter.Ch01 … Chapter.Ch08` and 506 *is* the locomotion line — my substantive fact was right. What
I did was verify the MEAD-A line numbers by reading MEAD-A, and then **assert what A1-R4 said**
without grepping A1-R4 for the string I was quoting. That is the same failure class as my published
"three MEADs claim `TDD-MEAD-001`" error and my "ten asks" slip: **a true fact about a source,
mistaken for a fact about a document that cites the source.** My §11.4 countermeasure said "emit
section references from the command that located the text"; it did not say "and quote the citing
document from a command too." It now does, in §0.4.

**This is a defect in my review, not in A1-R4, and it is not a defect in Agent 1's response
either — Agent 1's response correctly declined to treat it as one.** I am recording it as an erratum
to `TDD-A2-REVIEW-A1R4-001`, per the "corrections are new versioned artifacts" rule. I do **not**
rewrite the prior review; the erratum stands beside it.

**One qualification, in Agent 1's favour and against a point of its own rhetoric.** A1 §0.4 says a
citation error "attributed to the wrong document is worse than no citation at all." Agreed — and a
missing citation is still worse than a correct one, so I am not withdrawing the general instruction
to cite exact lines. I am withdrawing only the charge.

### 0.4 The countermeasure, extended

For any claim of the form "*document D says X at line N*", the check is two commands, not one:

```
# 1. establish the fact in the source
$ sed -n "${N}p" <source>                  # must contain X
# 2. establish that D says X at N — quote D from D
$ git show <D-blob> | grep -n "<the quoted literal>"
```

Step 2 is the one I skipped. Every citation in §2 of this review was produced that way, and §2.6
lists the two places where step 2 *did* fail for Agent 1's response.

---

## 1. Verdicts

The task asks for three separate verdicts. They are separate because they answer different
questions and one of them is negative.

### 1.1 Is central custody necessary?

> ## NOT ESTABLISHED

**Per-instance recovery is adequate and needs no custodian. Enumeration has no demonstrated
requirement.** I reach this independently of Agent 1's §2.4 argument, and I reach it by a slightly
different route, which strengthens rather than merely repeats it (§3).

This is *not* a rejection of custody as a design. It is a finding that the requirement document does
not currently contain the requirement, and that the contract should not acquire a stateful authority
on the strength of a convenience.

### 1.2 Is the proposed ownership boundary appropriate if custody is adopted?

> ## AGREE WITH CONDITIONS

If custody exists, the Agent 1-owned world-scoped boundary is the right home and beats Core and
`UTDDEventBus` decisively on lifetime. **But the boundary as drafted is not implementable under two
of the three candidate MEADs** (§2), and the two-representation problem it creates for the recovery
path (§4) is unresolved. Seven conditions, C2R-1…C2R-7.

**Agent 3's placement reasoning is sound and I accept it. Agent 1's twelve conditions are a real
improvement over `A1-R4` §4.1 and I accept ten of them unmodified.** What I do not accept is that
the resulting clause is complete, and the incompleteness is concentrated in the parts that would be
hard to change after a freeze.

### 1.3 Is the revised contract model sufficient for a successor submission?

> ## NOT SUFFICIENT

Six blocking defects, three of them contradictions with Agent 1's own text, and two of them
introduced by this response rather than inherited from `A1-R4`. Details in §8. The successor
submission can fix all six without new authority from anyone, which is why this is "not sufficient"
and not "reject".

### 1.4 Signature status

| Contract | Status after this review |
|---|---|
| **C-05** | **NOT SIGNED. Unchanged from my `A1-R4` review — still not signed.** Nothing in this response is a contract version; a review of a response cannot sign a contract (§10.3). |
| **C-01, C-02, C-06** | **Still signed on `2cc548fa…` only** — see §10.3 for why this response does not extend or revoke that. |
| **C-03, C-04, C-07** | **Not signed.** Unchanged. |
| Bilateral agreement | **None claimed.** Agent 1's response is not a signature; Agent 3's is not a signature. No two agents have signed one blob. |

**I add no signature and remove none.** A review of a design response is not a contract version, and
C-05's blocker has moved rather than closed — so signing would be worse than not signing.

---

## 2. How far the ownership boundary actually travels

This is the section Agent 1 did not write, and it is the reason §1.2 carries conditions.

### 2.1 C2's "Core-owned surface" exists in exactly one of the three candidate MEADs

A1 §1.1 **C2** requires: "*The shared surface is Core-owned: the `FTDDTelegraphState` value struct and
a read interface are Agent 3's types*". A1 §5.5 repeats it as a table row: `FTDDTelegraphState` →
**Agent 3 (Core value type)**.

I checked whether "Core" is a module in each candidate:

| Candidate | Has a `TDDCore` module? | Evidence |
|---|---|---|
| **MEAD-C** | **Yes** | line 227 "`TDDCore` is a leaf. No module may depend on a module above it"; line 228 "Cross-agent contracts live in `TDDCore` as interfaces/structs"; line 267 module diagram |
| **MEAD-A** | **No** | §4.2 module layout lists `TDDRuntime/{Core, Character, Combat, AI, World, Progression, Narrative, Audio, UI, Framework}`, `TDDEditor`, `TDDTests` — **no `TDDCore` module anywhere in the tree.** `grep -c TDDCore` over MEAD-A = **0** |
| **MEAD-B** | **No** | 247 lines; `grep` for `TDDCore` = **0**, for `Telegraph` = 0 occurrences of the class name |

**Consequence.** Under MEAD-A, "Core-owned (Agent 3)" names a folder (`TDDRuntime/Core/`) inside the
*shared* game module whose stated contents are "GameMode, GameState, PlayerState, GameInstance,
subsystem registry" — not a cross-agent contract layer. The nearest contract home under MEAD-A is
`TDDRuntime/Framework/` ("Shared: interfaces, canon validation, telemetry"), which is **not** what C2
says, and MEAD-A does not assign it to Agent 3.

**So A1's clause is MEAD-neutral in its class name and MEAD-specific in its ownership.** §5.1 says the
clause "stays MEAD-neutral" and names a concrete class only under MEAD-C. That is true of the
**state** placement. It is not true of the **surface** placement, which C2 makes a condition. This is
the same error A1 correctly diagnosed in `A1-R4` §5.1 and then reproduced one layer down.

**This is not a reason to prefer MEAD-C.** I authored MEAD-A and I am not going to argue that a
clause is inferior because it fits a document I wrote. The finding is that **C2 is not
MEAD-neutral**, and a condition that only holds under one candidate cannot be a precondition for a
contract that is supposed to survive all three.

### 2.2 Agent 1's MEAD-C citations — all seven verified exact

Because A1 built a large part of its argument on seven MEAD-C lines, I re-read each one against the
blob Agent 1 names, not against Agent 1's transcription.

| Line | Content as quoted by A1 | Verdict |
|---|---|---|
| 303 | `UTDDEventBus \| UGameInstanceSubsystem \| Process \| Typed events between modules \| 3` | **exact** |
| 310 | `UTDDCombatDirectorSubsystem \| UWorldSubsystem \| World \| Attack tokens, simultaneous-attacker budget \| 1` | **exact** |
| 315 | `UTDDPerformanceBudgetSubsystem \| UWorldSubsystem (dev) \| World \| Runtime budget assertions in Test/Development \| 3` | **exact** |
| 317 | "State that dies with the world goes in a `WorldSubsystem`" | **exact** |
| 321 | events carry `FGuid` entity IDs, "so a listener cannot accidentally hold a stale actor" | **exact** |
| 599 | telegraph fairness — wind-up below a threshold requires the player to be free or it is deferred | **exact** |
| 600 | `FTDDAttackTokenPolicy` is "a pure function of (candidates, current tokens, time) and is unit-tested" | **exact** |

**And the blob identity claim checks out:** `169a8d8f…:docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md`
= `f49354631c86601e9311865901bf1fcd44846d89` = the blob on Agent 1's branch. Same document, as claimed.

**Seven for seven. Agent 1's citation discipline in this response is better than mine was in the
review it is answering.** I say so because my §0.3 error would otherwise let a reader infer the
reverse.

### 2.3 A1 §5.1's MEAD-A column is also accurate

| A1's claim | Verified |
|---|---|
| MEAD-A combat director is `UTDDCombatDirector` at line 527, referenced by `ATDDEncounterVolume`, no subsystem table | **exact** — line 527 reads `ATDDEncounterVolume \| Spawns/arms encounters; reports begin/end to UTDDCombatDirector; bosses use phase graphs` |
| MEAD-A arbiter is `UTDDHitArbiter`, world subsystem, "single-owner" | **exact** — line 484: "Hit arbitration is single-owner. Only `UTDDHitArbiter` (a world subsystem) decides Hit/Blocked/Parried" |
| MEAD-A module shape is one `TDDRuntime` module with folder areas | **exact** — §4.2 |

### 2.4 The MEAD-A verdict has a consequence Agent 1 states and does not follow through

A1 §5.2: "*If MEAD-A is canonical, a contract clause naming 'the Agent 1-owned world-scoped combat
boundary' resolves to `UTDDHitArbiter`. I would accept custody there if the TD required it, and I
would argue against it.*"

That is honest, and it is also **a condition C9 violation by construction**. C9 requires that "*parry
and block evaluation must never read the custody store*". Under MEAD-A:

- `UTDDHitArbiter` **is** the parry/block decision path (line 484: only it decides `Hit/Blocked/Parried`);
- the same class would hold the custody store (§5.2);
- therefore the class that decides parry holds the store it must not read.

A rule of the form "this class must not read its own member" is not a contract, it is a code-review
convention. **C9 is enforceable only under MEAD-C**, where the arbiter role and the Director role are
different classes. So both C2 *and* C9 are MEAD-C-only — the two conditions A1 presents as protecting
C-05's severity bound.

**This does not choose a MEAD and I do not choose one.** It states that the clause cannot be frozen
until TD-12 is settled, which is a stronger form of A1's own §5.1 conclusion.

### 2.5 The recommended alternative has a consumer-side gap A1 does not mention

A1's §2.4 per-instance query is proposed as the smaller surface and is the option A1 recommends
first. Its signature:

```cpp
// PROPOSED — NOT FROZEN. Core-owned interface (Agent 3's type), implemented by each producer.
UFUNCTION() bool TryGetOpenTelegraph(FGuid AttackInstanceId, FTDDTelegraphState& Out) const;
```

**"Implemented by each producer" means the caller must already hold a reference to the specific
producer.** A consumer that detects it holds revision `k−2` for instance `X` knows `X`, and §2.4 says
that is all it needs. It is not all it needs: it must resolve `X` → **the producing object** before
it can call a method on that object. Nothing in §2.4 defines that resolution, and §3.1 explicitly
says the registry is keyed by `AttackInstanceId` *not* by actor precisely because "one actor may hold
several open instances" — so even `SourceEntityId` → actor is not stated to be a live actor lookup
under the value-only rule of §7.2.

This is the exact problem a custodian exists to remove, and it is why the smaller surface is smaller
in **state** but not obviously smaller in **consumer obligations**. A1 §2.4's comparison table lists
"Cross-agent write coupling: none" for the producer query and does not list "producer resolution"
as a cost on either side.

**Fix is one sentence** (C2R-3, §9.2), not a redesign. But as written, §2.4 trades a stateful
custodian for an unresolved indirection, and the trade is understated.

### 2.6 Two claims in A1's response that do not survive the check

Both are minor and both are the same kind of slip I made in §0.3, which is why I check them
symmetrically.

| A1 claim | Location | Verified |
|---|---|---|
| A1-R4 §4.1 "called the broker 'authoritative for current telegraph state'" and that word is withdrawn | §0.3, §7.1 change 3 | **exact** — A1-R4 §4.1(a): "the broker becomes **authoritative for current telegraph state**, not merely a relay" |
| A1-R1 §5.1 said "the broker must not be owned by Agent 1, or Agent 1 would be publishing Agent 2's attack lifecycle" | §0.3, §4.4 | **exact** — A1-R1 line 772 |
| M1 v1.4 lines 796–797 are `IsTelegraphingAttack()` / `GetAttackTelegraphRemaining()` | §2.4, §10.1 | **exact** — M1 lines 796, 797 |
| **"`A1-R4` §4.1's word 'authoritative' is withdrawn"** — but §7.2's replacement clause calls the custodian "the only place the producer's current state can be **found**" | §7.1 change 3 vs §7.2 | **contradiction — see §8.2** |
| **C9 says parry "must never read the custody store"; §7.2 also says the store is the only place the state can be found** | C9 vs §7.2 / §7.3 change 3 | **contradiction — see §8.2** |

The last two are the substantive ones and they share one root cause, discussed in §8.2.

---

## 3. Primary question — is a central state custodian actually necessary?

I was asked not to assume enumeration is required because it is useful. I applied the same test to
A1's *necessity* claim and to A1's *sufficiency* claim, because a review that only tests one side is
not independent.

### 3.1 The two requirements, kept separate

| # | Requirement | Who has it | What it needs | Does it need a custodian? |
|---|---|---|---|---|
| **R1** | Recover the current block+phase for **one known** `AttackInstanceId` after a revision gap or a late subscribe | Any consumer that already received `Opened` | one answer, for one instance, on demand | **No** — a per-instance read suffices |
| **R2** | Enumerate **all currently open** telegraphs, including instances the caller never heard of | Only a consumer that is newly created, or that must reconcile without knowing what it missed | an aggregate answer | **Yes** — nothing else can supply it |

### 3.2 R1 is adequately satisfied by per-instance capability — subject to §2.5

Three independent supports, and I weight them differently than A1 does.

1. **The mechanical argument.** R1's consumer holds `AttackInstanceId` already — it received `Opened`
   and then missed `Retimed`. It is asking about a thing it can name. A name-addressed read answers a
   name-addressed question. Custody is a name-addressed read **plus** storage, eviction, ordering,
   and a cross-agent write path, none of which R1 requires.

2. **The precedent argument.** This is the strongest and A1 understates it. The capability already
   exists in a shipped-spec interface, **not** as a proposal:
   ```
   M1 v1.4, lines 796–797:
     virtual bool  IsTelegraphingAttack() const = 0;         // M3
     virtual float GetAttackTelegraphRemaining() const = 0;  // M3, gameplay seconds
   ```
   `ITDDCombatant` already answers "is this actor telegraphing, and how long is left" **per actor, per
   instance, without any registry.** C-02 already publishes `bIsTelegraphing` /
   `TelegraphRemainingSeconds` as **Required** for Agent 2. So R1's data is already on the consumer's
   side of the fence, and the only thing `A1-R4`'s broker adds for R1 is a second copy.

   I want to be careful here, because the precedent is not a complete answer: `ITDDCombatant` is
   **actor-scoped**, and A1 §3.1 correctly notes a boss may hold two open instances, which an
   actor-scoped query cannot disambiguate. So the precedent establishes that per-instance recovery
   needs no registry — it does not establish that the existing signature is sufficient as-is. That
   is C2R-4.

3. **The absence-of-evidence argument for R2.** See §3.3.

### 3.3 Enumeration has no demonstrated requirement

A1 names the enumeration consumers as "A1's camera/audio cues and UI" (§2.4). I traced that list to
its source, because a consumer list is only as strong as its provenance:

```
A1-R1, docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V1.md, line 775:
  | **Consumers (named)** | A1: parry/block evaluation, dodge i-frame timing,
    camera/audio cues. A2: its AI reading the player's telegraph for defensive
    decisions (block/dodge) but not for hit resolution |
```

**The enumeration consumers are named in `A1-R1` §5.1 — Agent 1's own proposal — and nowhere else.**
Specifically:

- **No camera, audio or UI document in any of the three candidate MEADs** specifies a telegraph
  enumeration query. `grep` over MEAD-A, MEAD-B and MEAD-C for camera/audio/UI co-occurring with
  telegraph enumeration returns nothing. MEAD-C line 312 and 496 cover hitstop; nothing covers a
  telegraph read surface.
- **No acceptance test anywhere in the series** exercises enumeration. `A1-R4` §10 proposes
  `TelegraphRevisionGapRecovery` (**4 cases**, marked NEW), whose four cases are all name-addressed:
  snapshot-on-subscribe; gap → *single* `GetOpenTelegraphs` adoption; absent the query → diagnostic;
  no interpolation. **None of the four requires enumeration** — each could be satisfied by a
  name-addressed read if the consumer knows the name.
- **A1's own new suite set does not test enumeration either.** Of the eight suites in §10.2, **zero**
  exercise enumeration (§3.4).

So the position is: **R2's consumers exist only as a list in the document that proposes R2, and R2
has no acceptance test in any version.** That is the definition of an unestablished requirement.

**I am not saying camera/audio/UI will never need it.** A camera director that wants "the most
imminent telegraph in frame" needs a set, not a name — and that is a plausible future requirement.
The finding is that it is not a *stated* requirement today, and a stateful authority should not be
added on a plausible future. If the TD wants R2, it should appear as a requirement with a test, which
is exactly A1's own condition C1. **C1 is correct and I endorse it.**

### 3.4 Where I disagree with A1's framing of its own argument

A1 §1 presents NOT ESTABLISHED as a *sufficiency* verdict and AGREE WITH CONDITIONS as a *placement*
verdict, then says (correctly) that this is not a contradiction. I agree it is not. But A1 §2.4's
summary — "*The only thing custody buys is enumeration*" — is **too strong in one direction and too
weak in another**:

- **Too strong:** custody also buys eviction visibility. A1 itself says this in §6.2 — "*because
  eviction does not emit a message, the aggregate query is the only way a consumer can learn that an
  entry vanished*." If eviction is silent, then **R1 also needs enumeration** for a consumer that
  knows its instance vanished but not whether it was replaced. A1 records the point and does not let
  it change the C1 conclusion; I think it should, and §8.3 explains why it is a defect rather than a
  footnote.
- **Too weak:** custody buys a *third* thing A1 never lists — **cross-producer consistency at a
  single instant**. Two per-instance queries are two reads at two instants; one aggregate query is
  one read at one instant. For R1 that difference is irrelevant. For any consumer that must compare
  two open telegraphs (the "most imminent" camera case) it is decisive, and it is an argument *for*
  custody that belongs in the ledger. I add it because a review that only subtracts from the
  proposal is not testing the proposal.

**Net: my NOT ESTABLISHED verdict survives the addition, because the comparison case is also unstated
and untested.** But the ledger in §2.4 should have three rows, not one.

### 3.5 Verdict on the primary question

**NOT ESTABLISHED**, for these reasons in order of strength:

1. R1 is satisfied by a per-instance read, and the capability **already exists** in M1 v1.4 and C-02
   — subject to C2R-4 (actor-scoping) and C2R-3 (producer resolution).
2. R2's only named consumers trace to the document proposing R2, with no test anywhere.
3. The one argument *for* custody that A1 does not make (§3.4, single-instant cross-producer
   consistency) is also unstated and untested — so it does not rescue R2.

**This is a finding about the requirement set, not about Agent 3's recommendation and not about
Agent 1's competence.** The recommendation answers "whose should it be?" correctly. Nobody in this
exchange has yet answered "should it exist?" with evidence, and A1 is the first to say so.

---

## 4. The proposed conditional custody model and its twelve conditions

### 4.1 All twelve present, ten accepted as drafted

C1…C12 verified present and distinct in A1 §1.1. My disposition:

| # | Condition | My disposition | Note |
|---|---|---|---|
| **C1** | Custody only if cross-producer enumeration is established | **ACCEPT — endorse strongly** | This is the correct gate and it is the right shape: a requirement, not a preference (§3.3) |
| **C2** | Shared surface Core-owned; implementation Agent 1's | **ACCEPT WITH CONDITION** | **C2R-1**: C2 is MEAD-C-only (§2.1). Needs a MEAD-neutral fallback |
| **C3** | Custodian stores verbatim, never authors | **ACCEPT** | The mutation-test framing (§4.3) is genuinely good and I adopt it into my acceptance tests (§9.4) |
| **C4** | Strict-greater `TimingRevision` adoption, messages and snapshots identical | **ACCEPT** | Answers A2R-32 fully. The commutativity argument (§8.1) is correct and better than my three options |
| **C5** | At-most-once entry per `(AttackInstanceId, phase)` | **ACCEPT WITH CONDITION** | **C2R-5**: correct rule, but it collides with snapshot recovery for a *late* subscriber (§8.1). Agent 1's own P11 is the collision |
| **C6** | Eviction on close/invalidity/unload/death/teardown; query never returns invalid | **ACCEPT WITH CONDITION** | **C2R-6**: depends on a "producer handle" the same clause forbids storing (§8.4) |
| **C7** | Non-reentrancy: copies, queued delivery, no mutation during iteration | **ACCEPT** | FIFO-drain and "current state, not queue-time state" (§8.4) are both correct additions |
| **C8** | Named write-ordering point within a frame | **ACCEPT WITH CONDITION** | **C2R-7**: the condition requires a *named* point and the clause supplies **no name** (§8.5) |
| **C9** | Parry/block never read the custody store | **ACCEPT WITH CONDITION** | **C2R-2**: unenforceable under MEAD-A (§2.4); also contradicted by §7.2's "only place it can be found" (§8.2) |
| **C10** | No second per-instance registry; token policy stays pure | **ACCEPT** | Correct and well-argued — MEAD-C line 600 makes purity a testing guarantee |
| **C11** | Producer obligations normative and enumerated | **ACCEPT WITH CONDITION** | Obligations P1–P12 are good; **eight of twelve have no test** (§4.4) |
| **C12** | Not a freeze, not a closure; U-07 stays open | **ACCEPT** | And I confirm it: neither this review nor A1's response closes U-07 or C-05 |

**Ten accepted, six with a condition attached — of which C2, C6, C8 and C9 are blocking.**

### 4.2 What the twelve conditions get right that `A1-R4` got wrong

Worth recording, because a review that lists only defects misrepresents the delta.

- **The asymmetry argument (§6 preamble) is correct and non-obvious.** "*The custodian cannot verify
  any of [P1–P12] — it can only observe their absence. That asymmetry is why they belong in the
  producer's contract clause rather than in the registry's implementation notes.*" That is the right
  place to put an obligation that cannot be enforced from the receiving side, and it is the kind of
  reasoning `A1-R4` §4.1 lacked entirely.
- **C3's testability test is genuinely strong.** "Perturb a stored field and the returned value must
  change by exactly that perturbation, with no arithmetic in between" turns a vague "don't
  recompute" into a property a test can fail. I have adopted it (§9.4).
- **C10 is a real catch.** The token policy's purity (MEAD-C 600) would be quietly destroyed by
  putting mutable per-frame state in the same class, and no one had noticed.

### 4.3 A structural problem with the condition set

Twelve conditions, twelve producer obligations (P1–P12), two new Core artefacts, one read interface,
one relocated owner. **That is a larger specification surface than the recovery problem it solves.**

For R1 alone (name-addressed recovery), the alternative in §2.4 needs: one method, one struct, one
resolution rule (§2.5). **One condition, not twelve.**

A1's C1 says custody is adopted only if R2 is established. I would put the arithmetic more sharply,
because it is the decision the TD is actually being asked to make:

> If R2 is not established, the TD is being asked to accept **twelve conditions, twelve producer
> obligations, a new stateful owner and a cross-agent write path** to deliver a requirement that **one
> method** delivers.

A1 does not state the comparison in those terms, and it is the single most useful number in this
response. It supports A1's own recommendation, so I am not scoring a point — I am sharpening the case
A1 already makes.

### 4.4 Test coverage of the twelve conditions — six uncovered

A1 proposes eight suites / 30 cases (§10.2). I mapped each condition to a suite:

| Condition | Named in a proposed suite? |
|---|---|
| C3, C4, C5, C6, C7, C9 | **yes** |
| **C1, C2, C8, C10, C11, C12** | **no suite row names them** |

Of these, **C8 is blocking and untested**: the ordering point is the condition whose absence makes a
same-frame query "legitimately return the previous frame's block and nobody can call it a bug"
(A1's own justification for C8). A condition that exists to make a bug detectable, with no test that
detects it, is the exact failure mode C8 was written to prevent.

C1/C2/C12 are process conditions and need no runtime test — fine. **C8, C10 and C11 do.** C10 in
particular ("no token decision may depend on a custody read") is mechanically testable and is not
tested.

**Producer obligations: four of twelve tested.** Named in suite rows: **P4, P5, P6, P8.** Not named
anywhere: **P1, P2, P3, P7, P9, P10, P11, P12.** Of these:

- **P7 (revision monotonicity)** is the producer half of C4 — C4 is unenforceable if P7 is violated,
  and P7 has no test. C4 is the rule that makes snapshot/message races converge; it is tested; its
  producer precondition is not.
- **P1 (exactly one `Closed`)** and **P9 (no retime after close)** are the two obligations whose
  violation corrupts consumer state permanently, and neither has a test.
- **P11** is the one whose absence breaks C5 (§8.1).

**This is not a demand for eight more suites.** It is a demand that the two conditions A1 itself calls
load-bearing (C4 via P7, C5 via P11) have their producer precondition tested, or be acknowledged as
conventions rather than contract terms.

---

## 5. Strict-greater adoption and at-most-once entry (A2R-32, A2R-33)

### 5.1 A2R-32 — ACCEPTED, and A1's reasoning is better than mine

A1 §8.1 supplies the rule and justifies it on **commutativity**: strict-greater is the only one of my
three candidate rules whose outcome does not depend on arrival order, so a snapshot/message race has
one correct answer for every conforming consumer.

That is a better argument than the one I made when raising the finding, where I offered the three
options without ranking them. **Commutativity is the correct criterion** and it generalises: any
future adoption rule (a revision *range*, a per-phase revision) should be tested against the same
question. I adopt it.

One refinement A1 states and I want to make explicit, because it is a precondition rather than a
consequence: **C4 is sound only if P7 holds.** If two messages carry the same `TimingRevision` with
different content, "discard the equal revision" discards a real change. A1 says this (P7, §8.1). It
is not tested (§4.4). **Not a defect in the rule; a gap in the evidence for it.**

### 5.2 A2R-33 — ACCEPTED with a condition, and the condition is A1's own

A1 §8.2:

> A phase transition is observable **at most once** per consumer per `(AttackInstanceId, phase)`. A
> snapshot establishes the consumer's current phase **without** re-firing entry for a phase already
> held…

A1 is right that the identity must be `(AttackInstanceId, phase)` and not `TimingRevision`, and the
reason given is correct: keying on revision would make every hitstop boundary (§5.7) re-fire every
on-entry hook, i.e. the bug the rule prevents would fire *more* often. **My original finding left that
implicit and A1 fixed it. Accept.**

**But see §8.1** — the rule as written is correct for a *continuing* consumer and wrong for a *new*
one, and P11 is where the collision appears.

---

## 6. Producer invalidation, destruction, cancellation, unload and query-time fail-safe

### 6.1 Three lifetimes distinguished correctly

A1 §3.4 separates producer-destroyed (world alive), producer-dies (its own death cancels its attack),
and victim-dies (no registry effect). **This is correct and it is the sharpest piece of analysis in
the response**, because `A1-R4` had conflated all three into "death" and therefore had no path at
all.

### 6.2 The fail-safe mechanism is right and it is stated three different times, differently

The rule is: *(i)* producer invalidates in `EndPlay` (P4); *(ii)* **independently**, the custodian
checks producer validity when building a query result and omits invalid records (P5); *(iii)* a sweep
at a defined frame point drops invalid records from storage.

The three-way structure is right — and A1's own note on why (ii) cannot depend on (iii) is exactly
correct: "*the query cannot depend on the sweep having run, because a query can arrive in the same
frame a producer died, which is exactly the frame a recovering consumer is most likely to be asking.*"

**Then §7.2's single clause compresses all three into one sentence and loses (ii)'s
independence** — "A query never returns a record whose producing entity is invalid" states the
*outcome* but not that the check is inline rather than sweep-dependent. Under §7.2 alone, an
implementation that sets a "dirty" flag and returns invalid records until the next sweep satisfies
the sentence. **This is C2R-6's first half.** The fix is to carry (ii)'s independence into the clause,
not just into the commentary.

### 6.3 Eviction is silent — accepted, and it has a consequence A1 records but does not price

A1 §8.3: eviction emits no message. The reasoning is sound: synthesising `Closed` on eviction makes
the custodian a publisher of the producer's lifecycle, which §4.4 withdraws, and would make a real
close indistinguishable from a registry decision. **Accept.**

A1 then says (§6.2) that "*the aggregate query is the only way a consumer can learn that an entry
vanished*". I verified the per-instance alternative returns `false` for closed/unknown/gone (§2.4), so
for a **known** instance, `TryGetOpenTelegraph` returning `false` *is* the removal signal. A1's
sentence is therefore **too strong** — but only because it compares against the custodian's own read
surface, not against the alternative. Within the custody design, if the only query is the aggregate
one, the sentence holds.

Either way the point stands and is not priced: **silent eviction makes removal a query-only fact, and
A1 uses that to argue for enumeration (§6.2, §8.3) while condition C1 says enumeration is
unestablished.** That circularity is §8.3.

---

## 7. Requirement 5 — every hitstop boundary emits `Retimed`; does the model preserve every revision without coalescing?

This was the specific question I was asked to settle, and the answer is **partly, and the model's own
guarantee is weaker than the text claims.**

### 7.1 The mechanism A1 identifies is real

A1 §5.7: `UTDDHitStopSubsystem` applies a scaled dilation to the **pair** of actors (MEAD-C line 496),
so every hitstop start *and* end changes `CustomDilation` on up to two actors, including producers
with open telegraphs. Therefore every hitstop boundary emits `Retimed` for every open telegraph on
that actor, in the same frame. **Verified:** MEAD-C line 312 (`UTDDHitStopSubsystem`, `UWorldSubsystem`,
owner 1) and line 496 ("applies a scaled time dilation to the *pair* of actors"). A1's reading is exact,
and the interaction between two Agent 1-owned world subsystems is a genuine new conflict.

### 7.2 Coalescing is named as forbidden in the commentary and never forbidden in a clause

`grep` for coalescing/throttling/batching across A1's response returns **three hits, all in
non-normative places**:

| Location | Kind | Text |
|---|---|---|
| §5.7 bullet | **commentary** | "a custodian that throttles or coalesces 'too many retimes in one frame' **creates** the revision gap it exists to fix" |
| §10.2 test description | **test description** | "no coalescing; no gap observed by a consumer" |
| — | — | *(no third instance in any condition, obligation or clause)* |

**The twelve conditions do not prohibit coalescing. P1–P12 do not prohibit coalescing. §7.2's
replacement clause does not prohibit coalescing.** The prohibition exists only as an argument in
§5.7 and an assertion in a test that is not run.

**This matters more than it looks, because the model structurally invites coalescing.** §7.2's State
clause: "*One record per open `AttackInstanceId`*" — one record, holding the current block. There is
**no revision log, no queue, no history**. So when two hitstop boundaries land in one frame and a
consumer misses the first `Retimed`, the custodian holds only the second block, and the consumer
recovers the *latest* block having never seen the intermediate one. That is indistinguishable, from
the consumer's side, from coalescing. A1 says coalescing "creates the revision gap it exists to
fix" — and the current-state-only record does exactly that, by design, in the same way.

**So the honest answer to requirement 5:**
- **Every `Retimed` is emitted** — nothing in the proposal drops a message, and P8 requires
  same-frame publication of a `CustomDilation` change. ✅
- **Every revision is *preserved in storage*** — **no.** The store keeps the current block only. A
  missed intermediate `Retimed` is unrecoverable through custody, exactly as it is without custody.
- **Without coalescing** — **not guaranteed by any clause.** Commentary only. ❌

**A1's §5.7 conclusion is therefore right about the *danger* and does not deliver the *guarantee*.**
The fix is either (a) a clause forbidding coalescing and requiring one record per (instance,
revision) for the frame, or (b) an explicit statement that custody provides *current-state* recovery
and never *revision-history* recovery, so no consumer may assume it recovers a missed intermediate.
I propose (b) plus the coalescing prohibition, in §9.3, because (a) alone still leaves a consumer
unable to tell a coalesced gap from a real one.

### 7.3 The ordering half of §5.7 is correct and C8 does not deliver it

A1 §5.7: "*the same-frame ordering between hitstop application and retime publication must be
defined (C8), or a consumer can read a block whose `ProducerRate` was already replaced.*"

C8 requires "a named update point". **No name appears anywhere** — `grep` for `TickGroup`,
`pre-physics`, `post-physics`, `named frame point` returns only the requirement that one be named
(§8.5). So the exact failure §5.7 warns about is unaddressed by the clause written to address it.

---

## 8. Blocking defects, contradictions, missing obligations and untestable requirements

Six blocking. Each has a location, a technical reason, and proposed replacement wording.

### 8.1 BLOCKING — C5 and P11 collide: a late subscriber can never observe the phase it joined in

**Location.** A1 §8.2 (entry rule), §7.2 Entry clause, §6.1 **P11**, §3.2 ("a late subscriber's first
observation is indistinguishable from a continuous subscriber's").

**The texts.**

> **P11.** Open before the first frame the wind-up is observable. `Opened` precedes any frame in which
> the wind-up is live, **so a snapshot never reports a phase that was never announced.**

> **Entry.** A phase transition is observable **at most once** per consumer per `(AttackInstanceId,
> phase)`. **A snapshot establishes the current phase without re-firing entry** for a phase already
> held.

**The reason this fails.** Take a consumer that subscribes mid-`Active`, having never received
`Opened` or `PhaseChanged(Windup)` or `PhaseChanged(Active)`:

1. P11 says this can happen: the snapshot reports a phase (`Active`) that **this consumer was never
   told about**. P11's own failure-mode column says so — "*Late subscribers see a phase with no entry
   history*". P11's requirement is that the *producer* announced `Opened` before the phase went live,
   which is a statement about the message stream, **not** about what this consumer received.
2. C5 says the snapshot "establishes the current phase **without** re-firing entry for a phase already
   held". But this consumer holds **no** phase. The phase is therefore **not** "already held", so C5
   does not tell the implementation whether to fire entry or not.
3. Two conforming implementations now diverge. One reads "at most once per `(instance, phase)`" as
   "suppress entry, because the *system* already entered that phase" → the subscriber never gets the
   on-entry hook for the phase it is in, and a boss reaction timer or parry prompt tied to that entry
   never starts. The other reads it as "the consumer has not seen it, so fire it" → the exact
   double-fire C5 exists to prevent is now reachable for late subscribers on every subscribe.

**A1 asserts the property that the text does not deliver.** §3.2: "*With those, a late subscriber's
first observation is indistinguishable from a continuous subscriber's — which is the property that
makes snapshots safe rather than merely convenient.*" That is the correct property to want. **It
requires a rule C5 does not contain: that a snapshot establishes entry-baseline state for a new
consumer.** As drafted, C5 plus P11 produce either silence or duplication, and the choice is left to
implementation taste.

**Why this is blocking rather than a wording nit.** It is the interaction between the two clauses A1
presents as the answer to my two findings (A2R-32/33), and it fails precisely on the case that
motivated custody in the first place — the late subscriber of `A1-R4` §4.1. A contract that is
ambiguous on its own motivating case cannot be frozen.

### 8.2 BLOCKING — "the only place it can be found" contradicts C9 and cannot be tested

**Locations.** §7.1 change 3; §7.2 Explicit non-authorities; C9.

> **Change 3.** Withdraw "authoritative" → "*the only place the producer's current state can be
> **found**; the producer remains its author*"

> **C9.** Parry and block evaluation must **never** read the custody store. §3.4's same-frame
> phase-overlap test remains the only parry authority.

> **§7.2 non-authorities.** "*Parry and block evaluation must not read this store; §3.4's same-frame
> phase-overlap test **over live phase state** remains their only authority.*"

**Two problems, the second worse than the first.**

**(a) The contradiction.** If custody is "the only place the producer's current state can be found",
then "live phase state" is in the custody store, and C9 forbids the parry path from reading the only
place the state exists. A1 must mean "live phase state owned by the producer, read through the
producer's own interface" — which is what §2.4's alternative does and what the custody clause never
says. **The two sentences cannot both be true as written.**

**(b) The unresolvable reference.** C9, §7.2 and §4.2 all cite "**§3.4**" as the parry authority.
**`A1-R4` has no §3.4** — its section 3 contains only §3.3 (headings verified: `grep "^#\+ "` on
`2cc548fa…` gives `## 3. Item 2`, no `### 3.4`). The normative parry text lives at **`A1-R3` §3.4**
("Parry is same-frame phase overlap — normative contract text (A2R-19)", verified at
`70db9665…:docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V3.md` line 234).

**Eight bare `§3.4` references in a 584-line document, none of which says which document's §3.4,
and the document they most naturally point at does not contain that section.** A contract clause
whose central safety property references a section that does not exist in the document it is
revising is not citable, and C9 is C-05's severity bound.

**Why blocking.** C9 is the clause that lets everyone say "a wrong timing block can never produce a
wrong parry". It is the reason this whole area is bounded. It currently points at nothing and
contradicts its own model.

### 8.3 BLOCKING — the eviction-requires-enumeration argument is circular, and it strengthens C1 against A1's own recommendation

**Locations.** §6.2 ("one consequence worth stating plainly"), §8.3, C1, §2.4.

A1's chain:

1. Eviction is silent (§8.3, accepted — §6.3 above).
2. Therefore "the aggregate query is the only way a consumer can learn that an entry vanished" (§6.2).
3. Therefore "that is an argument for enumeration (the very requirement C1 says is unestablished)".
4. And C1 says custody is adopted only if enumeration is established.

**The circle.** Enumeration is needed **because** the custodian was built to hold silent-evicting
state; and the custodian is justified **because** enumeration is needed. Remove the custodian and the
silent eviction disappears: with a per-instance producer query, "the producer is gone" is answered by
`false`, exactly as §2.4 says. **Silent eviction is a cost of custody, not a requirement that
justifies custody.**

A1 records the argument as "the strongest point in favour of Agent 3's recommendation" and treats it
as honest self-criticism. It is honest, and it is also **the strongest point against the model A1
recommends**, because it shows the model generates a requirement for the very surface whose necessity
is in doubt.

**I am not using this to argue for Core custody or against the Director.** I am recording that the
argument cannot appear in a successor contract in its current form, because a TD reading it would
reasonably conclude enumeration is required, when the requirement was created by the design.

**Correct use of the same fact** (proposed in §9.3): state that eviction is silent, that a consumer
learns of removal only by asking about an instance it already knows (§2.4 semantics), and that
enumeration is therefore **not** required for removal detection — closing the circle in the direction
that does not manufacture a requirement.

### 8.4 BLOCKING — C6's validity check requires a "producer handle" that the same clause forbids

**Locations.** §6.2 table ("Never return an entry whose **producer handle** is invalid"), §7.2 State
("Records hold values and entity IDs only — **no actor pointers**"), C6.

**The problem.** Query-time validity is the fail-safe A1 calls non-optional (§3.4, §6.2) and it is the
only mechanism covering the case A1 says is expected rather than excused (P5, "ungraceful loss is
expected"). To check "is the producer valid" the custodian must be able to ask *about the producer*.
§7.2 forbids storing an actor pointer, and A1 supplies no alternative — `grep` for
`weak|TWeakObjectPtr|handle|IsValid` across the response returns only C7 (unrelated) and the two
contradictory lines themselves.

MEAD-C line 321 gives the pattern for *events* ("carry `FGuid` entity IDs … Subscribers are
weak-lifetime-checked") — but that is event delivery, not custody, and it does not say how a
`FGuid` resolves to a validity answer.

**Two coherent resolutions, neither chosen by A1:**

- **(i)** store a `TWeakObjectPtr<UObject>` to the producer *alongside* the value record, accepting
  that "no actor pointers" means "no actor pointers **in the published value struct**", not "none in
  the custodian's private record"; or
- **(ii)** require a producer-liveness registry (a set of live `SourceEntityId`s) maintained by
  registration/invalidation, so validity is a set membership test on data.

Both are implementable and both are contracts. A1's text admits neither and forbids one of them.

**Why blocking.** It is the fail-safe for the failure A1 says is expected. A clause that requires a
capability and forbids the means to it is not implementable, and the test A1 proposes
(`TelegraphProducerLossInvalidation`, 5 cases) cannot be written against it.

### 8.5 BLOCKING — C8 and §7.2 require a *named* ordering point and never name one

**Locations.** C8 ("A named update point is required"), §7.1 change 8 ("a named frame point"), §7.2
Ordering ("The named point is required so that a same-frame read is defined rather than incidental").

**The problem.** `grep -i` for `TickGroup|TickGroup|pre-physics|post-physics|named update point|
named frame point` returns **only the three statements that one is required**. No name is supplied: not
a tick group, not a phase, not an ordinal, not "after `UTDDHitStopSubsystem` ticks and before any
consumer's `Tick`".

**Consequence, in A1's own words.** The condition's stated purpose is that otherwise "*a same-frame
query legitimately returns the previous frame's block and nobody can call it a bug*". With the
requirement stated and the name absent, a same-frame query **still** legitimately returns the previous
frame's block, and the condition has changed nothing. It is a requirement to make a decision that the
document does not make.

**And it is untested** (§4.4) — no suite row names C8 — so nothing detects the gap.

### 8.6 BLOCKING — A2R-35's evaluation rule depends on `CombatState == Dead`, which the same document routes elsewhere

**Locations.** §8.5 step 1; `A1-R4` §9.2 table; `A1-R4` §9.2 closing paragraph.

> **A1 §8.5 step 1.** `bAlive == false` (or `CombatState == Dead`) → the effective state is `Dead`; stop.

> **`A1-R4` §9.2 (the 11-row table).** `Dead` → `Status.Dead` **if granted**; otherwise none.
> "`Status.Cinematic`, `Status.Interacting`, `Status.Traversing`, `Status.Airborne` and `Status.LockedOn`
> are **not** combat states: they derive from the **control state machine** directly and never from
> `ETDDCombatState`."

**The problem.** C-02's `ETDDCombatState` enumerates `Dead` (the table's 11th row), so
`CombatState == Dead` **is** reachable and A1's step 1 is sound on that path. But A1-R4 §9.2 also
places `Cinematic` on the control state machine and *not* on `ETDDCombatState`, while A1 §8.5's
**step 2** tests `Status.Cinematic` as a tag and its preamble says the other two precedence members
are "tags".

So the rule tests three different carriers — `bAlive`/`CombatState` (enum), `Status.Cinematic` (tag),
`Status.Staggered` (tag) — while asserting "*Because the order is total, no consumer ever compares an
enum to a tag*". **It does not compare an enum to a tag; it tests them in sequence, which is fine —
but the clause's own justification is that no comparison is needed, when the reason no comparison is
needed is that the carriers are different, i.e. precisely the thing the sentence denies.**

**Second, and the blocking part:** step 2 reads `Status.Cinematic`, and A1-R4 §9.2 says `Cinematic`
"derive[s] from the control state machine directly and never from `ETDDCombatState`". So the
`Status.Cinematic` tag A1's rule reads is **not** the tag C-02 derives — it is a tag with a different
provenance, published outside the C-02 authority chain. A1 §8.5's rule therefore depends on a
`Status.Cinematic` whose authority A1-R4 §9.2 explicitly does not grant.

**This is a real contradiction between two accepted clauses, not a wording problem**, and it sits
inside the answer to my own A2R-35.

### 8.7 Non-blocking defects and missing obligations

| # | Defect | Location | Severity |
|---|---|---|---|
| N1 | §2.4's per-instance query has no producer-resolution rule (§2.5) | §2.4 | **high** — makes the recommended alternative incomplete |
| N2 | §3.4's 3-case table does not include the *victim-died-while-producer-alive* case that C-04 introduces | §3.4 | medium |
| N3 | P3 requires `Closed` "with a reason value"; no reason enumeration is given, and none is proposed for test | §6.1 | medium — untestable as written |
| N4 | §1.1 C1 says "the Combat Director keeps its current responsibilities unchanged" if R2 fails — but C1's own gate then cannot be evaluated, because nothing defines who establishes R2 or against what evidence | C1 | medium |
| N5 | §10.2 claims "8 suites, 30 cases"; the eight rows sum to **30** ✅ (verified) but the §10.1 executed count (six file checks) is presented beside them in a way that could be read as coverage | §10.1–10.2 | low — I verified it is honestly labelled "0 executed" |
| N6 | §5.7's hitstop interaction is attributed as "a new conflict, not one Agent 3 or A2 raised" — correct, and it is the best catch in the document | §5.7 | **not a defect — recorded as a strength** |

### 8.8 Missing obligations

| # | Missing | Why it matters |
|---|---|---|
| M1 | **No obligation on the custodian to reject a `Retimed` for an instance it does not hold** | P9 binds the producer. Nothing binds the custodian when P9 is violated — §6.2's Rejection row covers non-monotonic revisions, not unknown instances. A custodian that silently creates the entry resurrects a closed attack |
| M2 | **No obligation covering producer ID reuse across worlds** | P2 says "never reused, in this world or any other" — but the custodian is world-scoped (C6), so it cannot detect cross-world reuse, and no world-transition check exists. Harmless today; a latent trap if persistence is ever added (§5.8 of A1's own response warns about exactly this) |
| M3 | **No rule for a producer that publishes a block whose `SourceEntityId` is valid but whose attack was cancelled without `Closed`** | This is P3's violation, and the custodian's only signal is that the producer is alive — so the entry survives. P3 has no test (§4.4) |
| M4 | **No consumer-side obligation for the case where a query returns nothing for an instance the consumer holds** | §8.3 says "treats 'not found' as closed". That is a consumer rule stated in commentary, not a clause, and it is not in §7.2 |

### 8.9 Untestable requirements

| Requirement | Why untestable as written |
|---|---|
| **C8** (named ordering point) | No name supplied; cannot be asserted (§8.5) |
| **C2** (Core-owned surface) | No `TDDCore` exists under MEAD-A/MEAD-B; the requirement has no referent (§2.1) |
| **P3** (`Closed` "with a reason value") | No reason enumeration (§8.7 N3) |
| **C6's validity check** | Requires a handle the clause forbids (§8.4) |
| **§8.5 step 2** (`Status.Cinematic` tag) | Authority not granted by §9.2 (§8.6) |
| **C10** ("no token decision may depend on a custody read") | Mechanically testable, **not tested** (§4.4) |
| **P7** (revision monotonicity) | Testable, and it is C4's precondition, **not tested** (§4.4) |

---

## 9. Exact replacement wording

Every clause below is `PROPOSED — NOT FROZEN` and is offered as text for a successor version, not as
an edit to Agent 1's document (which I have not touched).

### 9.1 C2 — make the surface MEAD-neutral (replaces A1 §1.1 C2)

> **C2 (revised).** The shared surface — the `FTDDTelegraphState` value type and the read interface —
> is owned by the **cross-agent contract layer of the canonical architecture**, and its owner is
> whatever Agent 3 and the TD designate once TD-12 settles which candidate is canonical. Under
> MEAD-C that layer is `TDDCore` and the owner is Agent 3. **Under MEAD-A there is no `TDDCore`
> module; the nearest contract home is `TDDRuntime/Framework/`, and no owner is assigned there by
> that document.** The stateful implementation is Agent 1's in every candidate. **Consumers depend on
> the contract-layer type, never on an Agent 1 class, and never on a type whose owner is undecided.**
> This condition is satisfied only when TD-12 designates an owner; until then the interface may not be
> frozen.

### 9.2 New condition C13 — producer resolution for the per-instance surface (fixes §2.5 / N1)

> **C13 (new).** If custody is **not** adopted and recovery is served by a per-instance query, the
> contract must state **how a consumer holding only an `AttackInstanceId` reaches the object that owns
> it**. At least one of: (a) the contract-layer defines a resolution service keyed by
> `AttackInstanceId` that returns a read-only handle; (b) producers register with a resolution table
> on `Opened` and deregister on `Closed`; (c) the query is offered as a free function on the
> contract layer that performs the resolution internally. **A per-instance query that requires the
> caller to already hold the producer is not a recovery mechanism — the caller reaching the producer
> is the problem the query is supposed to solve.**

### 9.3 §7.2 Entry / State / Removal — fix §8.1 and §8.3

> **State.** One record per open `AttackInstanceId`. A record holds the producer-authored timing
> block, the current phase, the `TimingRevision` of the block it holds, and `SourceEntityId`.
> **The record holds the latest block only; custody never retains a revision history.** A consumer
> may therefore recover the *current* state of a known instance and may never recover an intermediate
> revision it missed. This is a stated limit of the mechanism, not a gap in it.

> **Entry — new consumer.** When a consumer subscribes, the snapshot **establishes the entry
> baseline**: for every instance in the snapshot, the consumer records the current phase as
> *already held*, and **fires no entry hook for it**. Entry fires only for phase transitions
> observed after the baseline. A consumer that has never observed a phase therefore never fires
> entry for it, and a consumer resuming after a gap re-baselines from the snapshot rather than
> replaying entries.

> **Entry — continuing consumer.** A phase transition after the baseline is observable **at most
> once** per consumer per `(AttackInstanceId, phase)`. A `Retimed` message **never** re-fires entry —
> it changes timing, not phase identity.

> **No coalescing (new, normative).** The custodian **must not** throttle, batch, coalesce or defer
> `Retimed` publication, and must not merge two retimes for one instance within a frame. Every
> producer-issued revision is stored as it arrives, overwriting the previous block. **If a consumer
> misses an intermediate revision, it recovers the latest block and must treat the missed revision as
> unrecovered (§3.3(c)4), not as evidence that no retime occurred.**

> **Removal.** A record leaves custody on `Closed`, on producer invalidity, on producer unload or
> stream-out, on producer death-cancel and on world teardown. Removal emits no message. A consumer
> learns of removal **by querying for an instance it already knows**; a `false` result, or an absence
> from the snapshot, means closed. **Enumeration is not required for removal detection**, because
> removal is only ever relevant for an instance the consumer holds. No age or staleness bound is the
> sole removal mechanism; no bound is selected here.

### 9.4 C6 — the validity mechanism (replaces the "producer handle" phrasing)

> **C6 (revised).** A query **never** returns a record whose producer is invalid, and **this check is
> performed inline when the query result is built** — it does not depend on a sweep having run. The
> custodian maintains producer liveness by **(i)** a private `TWeakObjectPtr` to the producer recorded
> at registration, **or (ii)** a set of live `SourceEntityId`s maintained by registration and
> invalidation. **The "no actor pointers" rule of the State clause applies to the published value
> struct, not to the custodian's private liveness record.** A sweep at a defined frame point drops
> invalid records from storage, and the query result is correct with or without it.

### 9.5 C8 — name the ordering point (replaces A1 §1.1 C8)

> **C8 (revised).** Within a frame the order is: producer publishes → custodian stores → consumers may
> query, and this ordering is realised at a **named** point: *after every producer's tick and
> `UTDDHitStopSubsystem`'s tick have completed for the frame, and before any consumer's tick that may
> query*. The update point is named so that a same-frame read has one defined answer. **The concrete
> tick group is fixed when TD-12 selects a canonical architecture, because tick-group names are
> engine-version and module-layout dependent**; until then the clause names the *relative* order and
> the test asserts it, not the engine enum.

### 9.6 C9 — resolve the parry ambiguity and the dangling reference

> **C9 (revised).** Parry and block evaluation **must never read the custody store**. Their sole
> authority is the normative parry rule at **`A1-R3` §3.4** (repeated for convenience: same-frame
> phase overlap between the defender's parry window and the attacker's **live** phase state for that
> `AttackInstanceId`, evaluated against live state and never by subtracting timestamps). **"Live phase
> state" means state read from the producing object, not from the custodian.** Custody is a recovery
> and reporting surface; it is not on the arbitration path, and the phrase "the only place the state
> can be found" in the custody clause refers to **recovery**, not to arbitration.

### 9.7 A2R-35 / §8.5 — fix the carrier and the `Cinematic` provenance

> **Evaluation rule (revised).** The precedence order is `Dead > Cinematic > Stagger`. The three
> members are read from **two carriers**, and the rule tests them in priority order rather than
> comparing them:
>
> 1. `bAlive == false` **or** `CombatState == ETDDCombatState::Dead` → `Dead`; stop.
> 2. `ControlState == Cinematic` **or** `Status.Cinematic` **when that tag is derived from the control
>    state machine** → `Cinematic`; stop.
> 3. `Status.Staggered` **or** `CombatState == ETDDCombatState::Staggered` → `Staggered`; stop.
> 4. otherwise → none of the three.
>
> **The carriers are stated explicitly because they differ, and a consumer must know which it is
> reading.** Step 2's `Status.Cinematic` is **not** derived from `ETDDCombatState` (`A1-R4` §9.2 places
> `Cinematic` on the control state machine); it is therefore a control-state projection and must be
> published as such, with the same authority chain as `ControlState`. **If `ControlState` is granted
> on the published player context, steps 2 and 3 read `ControlState` directly and the tag path is
> unnecessary.** The clause does not claim that no comparison is necessary; it claims that a *total
> order* makes comparison unnecessary, which is the property that holds.

### 9.8 New consumer obligation C14

> **C14 (new).** A consumer that has held an `AttackInstanceId` and receives a query result without
> that id **must** treat the instance as closed, release its block, and fire no further entry hook for
> it. This is a consumer-side obligation because the custodian emits no removal message (§8.3), and it
> must be in the contract rather than in commentary, or every consumer implements "not found" as an
> error.

---

## 10. Reassessment of A2R-32 … A2R-35

| Finding | Agent 1's response | My reassessment |
|---|---|---|
| **A2R-32** strict-greater adoption | **ACCEPTED**, text supplied, commutative justification (§8.1) | **RESOLVED.** The rule is correct, better justified than when I raised it, and applies identically to messages and snapshots. **Precondition P7 is untested** (§4.4) — a gap in evidence, not in the rule. |
| **A2R-33** at-most-once `(instance, phase)` entry | **ACCEPTED**, identity made explicit; retime does not re-fire (§8.2) | **PARTLY RESOLVED.** Correct for a continuing consumer. **Collides with snapshot recovery for a new consumer (§8.1, blocking).** Needs §9.3's two-part split. |
| **A2R-34a** eviction on producer invalidation | **ACCEPTED**, three-part mechanism named; silent eviction (§8.3) | **PARTLY RESOLVED.** Mechanism is right; **the clause requires a handle it forbids (§8.4, blocking)** and the clause compresses away the inline check's independence (§6.2). Silent eviction accepted, with §8.3's circularity corrected by §9.3. |
| **A2R-34b** non-reentrancy | **ACCEPTED**, FIFO drain and current-state-from-callback (§8.4) | **RESOLVED.** Both additions correct. No further finding. |
| **A2R-35** `Cinematic > Stagger` evaluation with non-tag `Dead` | **ACCEPTED**, priority-order rule (§8.5) | **NOT RESOLVED.** Depends on a `Status.Cinematic` whose provenance `A1-R4` §9.2 denies, and the "no consumer compares an enum to a tag" justification mis-states its own mechanism (§8.6, blocking). Replacement in §9.7. |
| A2 note — completion predicate as inequality | **ACCEPTED**; `Axis(t) − AxisNow ≥ R0 / ProducerRate` | **RESOLVED.** Correct. |
| A2 note — §5 case 5 both wrong operator and wrong rate | **ACCEPTED**; second fixture using consumer `CustomDilation` | **RESOLVED.** Correct — and it is the right fixture, because the rate error is the one a shared formula would hide. |
| A2 condition C-05-5 — same-frame retime | **ACCEPTED** as P8 | **RESOLVED** as an obligation; **untested** (§4.4). |
| A2 §7.2 claimed citation error | **Does not reproduce** | **I WAS WRONG.** Withdrawn with root cause in §0.3. |

**Summary: 5 resolved, 3 partly resolved, 1 not resolved.** Nothing is DISAGREE — C-05's blocker is
ownership and the concurrency rules, and those have moved substantially toward a resolution.

---

## 11. Acceptance tests — proposed, **NOT RUN**

I ran **zero** tests of any contract behaviour. Everything below is written text. What I *did* run was
document and arithmetic checks on the reviewed documents, listed in §11.4 because the distinction has
mattered in this series.

### 11.1 The eight suites Agent 1 proposes — my assessment

| Suite | Cases | Verdict |
|---|---|---|
| `TelegraphCustodyStoresVerbatim` | 4 | **accept** — the mutation-test framing is the right test for C3 |
| `TelegraphRevisionAdoptionOrdering` | 5 | **accept**, add case 6 (§11.2 T1) |
| `TelegraphPhaseEntryAtMostOnce` | 4 | **amend** — must split continuing vs new consumer, else it tests the ambiguity of §8.1 rather than resolving it |
| `TelegraphProducerLossInvalidation` | 5 | **amend** — add a case where the producer is destroyed without `EndPlay` (the P5 fail-safe path), since the current 5 test the graceful path |
| `TelegraphQueryReentrancy` | 3 | **accept** |
| `TelegraphArbiterIndependence` | 2 | **amend** — 2 cases cannot distinguish "did not read the store" from "read the store and got a correct answer"; needs a spy on the store |
| `TelegraphHitstopRetimeBurst` | 3 | **amend** — add the coalescing case (§11.2 T3); as written "no coalescing" is asserted, not tested against an implementation that coalesces |
| `TelegraphDeadPrecedenceEvaluation` | 4 | **amend** — add the `Status.Cinematic`-provenance case (§9.7) |

**Verified: 8 suites, case counts 4+5+4+5+3+2+3+4 = 30, matching A1's stated total.** ✅

### 11.2 Six tests I propose that Agent 1's set does not contain

| # | Test | Requirement | Why it is missing today |
|---|---|---|---|
| **T1** | **Late-subscriber entry baseline.** Consumer subscribes mid-`Active` having received nothing. Assert: no entry hook fires for `Active`; a subsequent `PhaseChanged(Recovery)` fires exactly one entry. | C5 revised (§9.3) | The existing 4-case suite tests a continuing consumer only; the case that matters is the one that motivated custody |
| **T2** | **Silent eviction is removal, not error.** Consumer holds `X`; producer destroyed; query returns nothing for `X`; assert the consumer releases `X` and fires no entry. Assert **no** `Closed` message was synthesised. | C6, C14, §8.3 | Not in any suite; C14 does not exist yet |
| **T3** | **Coalescing impossibility.** Two hitstop boundaries on one producer in one frame with two open instances. Assert exactly **two** `Retimed` per instance across the frame (four total), revisions strictly increasing, and a consumer that missed the first recovers the **second** block and reports the first as unrecovered (§9.3). | §7.2 No-coalescing, P8 | The current suite asserts "no coalescing" in its *description*; nothing tests a coalescing implementation |
| **T4** | **Validity check is inline, not sweep-dependent.** Producer destroyed mid-frame; query in the **same** frame before any sweep. Assert the record is not returned. | C6 revised, P5 | This is A1's own stated reason the check cannot depend on the sweep, and no case tests it |
| **T5** | **Revision monotonicity as C4's precondition.** Producer emits revision 7, then revision 7 with different content. Assert the custodian rejects with a diagnostic and does not overwrite. | P7, §6.2 Rejection | P7 has no test; C4's correctness depends on it |
| **T6** | **Ordering point is observable.** Query in the frame's query phase sees the block published in the same frame's producer phase; query before it does not. | C8 revised | C8 is the condition with no test, and its own purpose is detection |

### 11.3 Test-evidence split, stated precisely

| Category | Count |
|---|---|
| Contract acceptance tests **executed** by me | **0** |
| Contract tests **written against Agent 1 code** | **0** — no telegraph, clock, arbiter, custodian or registry exists |
| Tests **proposed** in this review (T1–T6) | **6** |
| Tests **assessed** from Agent 1's 8 suites / 30 cases | **30**, of which 2 accepted as-is, 5 need amendment, 1 (C3 mutation) accepted with the framing |
| Document and arithmetic checks **executed** | **see §11.4** |

**None of this is evidence that any contract behaves correctly.** No C++ exists, no Unreal project
exists, and no engine is present in this workspace.

### 11.4 Document checks I actually ran (the only executed evidence)

| Check | Method | Result |
|---|---|---|
| Agent 1's response is the blob I name | `git rev-parse origin/a1branch:<path>` | `a94b49ef…` at `22c29dad…` ✅ |
| Agent 3's recommendation is the blob I name | `git rev-parse origin/a3branch:<path>` | `79b79e30…` at `58ec7fd4…` ✅ |
| **My own §0.3 error: does A1-R4 contain "505"?** | `git show 2cc548fa… \| grep -c 505` | **0 — A1-R4 says 506; I was wrong** ❌ (mine) |
| A1-R4 has no §3.4 | `grep "^#\+ "` on the blob | **confirmed — section 3 has only §3.3** |
| `A1-R3` §3.4 is the normative parry text | `sed -n` on `70db9665…` | **line 234, confirmed** |
| MEAD-C lines 303/310/315/317/321/599/600 | line-by-line read | **7/7 exact** |
| MEAD-C blob identity across A3 and A1 branches | `git rev-parse` both | **identical** `f4935463…` ✅ |
| MEAD-A has no `TDDCore` module | `grep -c TDDCore` + §4.2 read | **0 — confirmed absent** |
| MEAD-A L484 / L527 | line read | **exact** |
| M1 v1.4 lines 796–797 | line read | **exact** (`IsTelegraphingAttack`, `GetAttackTelegraphRemaining`) |
| Twelve conditions C1–C12 present | `grep -oE "\*\*C[0-9]+\*\*" \| sort -u` | **12 distinct** ✅ |
| A1's 30-case total | sum of per-suite counts | **30 ✅** |
| Conditions with no suite row | regex per condition over §10.2 rows | **C1, C2, C8, C10, C11, C12** |
| P obligations with no suite row | same | **P1, P2, P3, P7, P9, P10, P11, P12** |
| No coalescing prohibition in any normative clause | `grep -i` coalesc/throttl/batch | **3 hits, all commentary/test-description** |
| C8's named point never named | `grep -i` tickgroup/pre-physics/named point | **only the requirement, no name** |
| Producer-resolution rule absent | `grep -i` resolve/locate | **absent** |
| Eviction-learns-by-aggregate claim vs per-instance `false` | compare §6.2 with §2.4 comment | **§6.2 too strong within design, correct across designs** |

---

## 12. What this review does not do, and what remains open

| Not done | Why |
|---|---|
| **Not closing U-07 or C-05** | I do not claim either is closed. C-05 remains unsigned by both agents; U-07 remains a TD decision (§1.4) |
| **Not signing anything** | A review of a design response is not a contract version (§10.3) |
| **Not choosing a MEAD** | §2.1 and §2.4 establish that C2 and C9 hold only under MEAD-C. **I authored MEAD-A and will not recommend it here.** TD-12 must settle it; that is the point of §2.1 |
| **Not resolving TD-12, TD-13, U-14, U-15** | All outside both agents' authority |
| **Not editing Agent 1's documents** | `AGENT1_C05_3_TELEGRAPH_AUTHORITY_RESPONSE_V1.md` and all its predecessors are untouched; blobs verified unchanged in §11.4 |
| **Not editing my prior reviews** | `AGENT2_REVIEW_A1R4_V1.md` at `7ea0a85` is unmodified. **Its §7.2 error is corrected in §0.3 of this document, not by rewriting it** |
| **Not free-ing or promoting any contract** | No contract version, no signature, no freeze |
| **Not approving the broker** | The broker is withdrawn by Agent 1 and replaced by a custody model I find **not sufficient** (§1.3) but repairable |
| **Not claiming tests passed** | 0 executed (§11.3) |

### 12.1 The decision I would put to the TD, stated as one question

Because the response contains two live options and the TD should not have to read 584 lines to find
the choice:

> **Does the product require "give me every open telegraph at one instant", or only "tell me about the
> telegraph whose id I already hold"?**
>
> - **Only the second** → adopt the per-instance surface, add C13's resolution rule, add nothing
>   stateful, and C-05's recovery requirement is met. **Twelve conditions become one.**
> - **The first** → adopt custody at the Agent 1-owned world-scoped boundary, fix the six blocking
>   defects in §8, and accept that the boundary is implementable only under whichever MEAD TD-12
>   selects.

**Today no document establishes the first**, including the one that recommends custody. That is why
my necessity verdict is NOT ESTABLISHED rather than AGREE.

### 12.2 What I would need to see to change the necessity verdict

Not a re-argument — a requirement. Specifically one of:

1. A camera/audio/UI document that states the enumeration requirement with a failure mode, in the
   same form C-02's `ControlState` request took; or
2. An acceptance test that cannot be written without enumeration — i.e. one where a name-addressed
   read is insufficient; or
3. A TD ruling that R2 is in scope for this slice.

Any of the three would move NOT ESTABLISHED to ESTABLISHED and I would then review the twelve
conditions as a **forward** proposal rather than a conditional one.

---

## 13. Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Independent review of `TDD-A1-C05-3-RESPONSE-001` v1.0 (blob `a94b49ef…` at `22c29dad…`) against `TDD-A3-ARCH-RECOMMENDATION-C05-3` v1.0 (`58ec7fd4…`) and `A1-R4` v1.3 (`2cc548fa…`). Three verdicts: central custody **NOT ESTABLISHED**; ownership boundary **AGREE WITH CONDITIONS** (seven conditions, six of which attach to A1's C2/C6/C8/C9/C5/C11); revised model **NOT SUFFICIENT** (six blocking defects, three of them contradictions with A1's own text). Six new acceptance tests proposed (T1–T6), none executed. **Withdraws my own `A1-R4` §7.2 citation finding** — A1-R4 says 506 and contains no "505"; the error is mine, with root cause recorded. **No signature given or withdrawn on any contract.** U-07 and C-05 confirmed open. |
