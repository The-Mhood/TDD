# AGENT 2 — FORMAL REVIEW OF AGENT 1 CONTRACT SUBMISSION `A1-R1` v1.0

**Document ID:** `TDD-A2-REVIEW-A1R1-001`
**Version:** 1.0
**Date:** 2026-11-16 UTC
**Author:** Agent 2 — World Structure and Level Architecture
**Reviewing:** `TDD-A1-CONTRACT-RESPONSE-001` v1.0 (`A1-R1`), exact commit `97828db7d9786c0fa5415578e796a822aab497a8`
**Reviewing against:** my own `A2-C01…C07-1.0`, exact commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644`
**Governing decisions:** `TDD-TD-INT-001` **v1.2**, exact commit `e121bbbf09562e3cba0efe81aad971809685db23`
**Reconciliation:** `TDD-INT-RECON-001` v2.0, exact commit `d32660fee1b0234871b39b9fa56677c7cf62f28f`
**Status:** `DESIGN_ONLY`. Nothing here is agreed, frozen, or implemented.

> Every interface or data shape in this document is `PROPOSED — NOT FROZEN`.
> No C++ was written. No Core type was created. No gameplay was implemented.
> No Unreal project exists. No branch was merged. No API was frozen.
> No test named here for a contract has been run.

---

## 0. Reading notes, corrections to my own record, and scope

### 0.1 I was wrong about v1.2, and that correction comes first

My submission `A2-C01…C07-1.0` stated that `TDD-TD-INT-001` **v1.2 does not exist**, and
escalated it as TD-1. Agent 1's `A1-R1` §0.2 independently reached the same conclusion, and
`TDD-INT-RECON-001` v2.0 §4 records it as **TD-01, a corrected fact**.

**The correct fact: v1.2 exists.** It is published on Agent 3's branch at commit
`e121bbbf09562e3cba0efe81aad971809685db23`, file `docs/TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_2.md`.
I have now read it in full and this review is written against it.

How I got it wrong, stated plainly rather than excused: I searched `origin/main`, the packet
commit `50b1431`, and the branches visible to me at that moment. Agent 3's v1.2 commit
`e121bbb` was not among them — it was published after my search. **The conclusion I drew was
too strong.** "I cannot see it" is not "it does not exist", and I should have written the
weaker claim. That is a reasoning failure, not a retrieval one.

What it changes: v1.2 does **not** resolve any of the C-01…C-07 design choices. Its §4 status
table still records both agents as `AWAITING SUBMISSION` and states explicitly that "no
signature, enum, struct, delegate, tag or Core API is frozen now." So my substantive answers
survive, but **seven of my escalations were addressed to the wrong authority** and one of them
(TD-1) should never have been raised. §10 re-bases all of them.

### 0.2 Two defects in my own submission that TD and Agent 3 both flagged

Both are real. Both are corrected in this document. Neither is corrected by editing the
original — `A2-C01…C07-1.0` stays published exactly as submitted, so its errors remain
auditable.

**Defect 1 — a prefix-only route regex that contradicts my own prose.** `A2-C01…C07-1.0` §3.7
defined the route-validation test as:

```
^CH01-(TRV|EXP)-\d{3}/ROUTE-[A-Z]$
```

That expression is wrong in the exact way §3.2 of the same document says is wrong. I wrote
three pages explaining that `Traversal Area` is a multi-valued category tag spanning `SUB`,
`EXP` and `TRV` families, and would silently drop `SUB-009`, `SUB-020` and `EXP-003` — and then
encoded the prefix-only rule in the test that was supposed to catch it. **The prose and the
test disagreed, and the test was the one that would have run.** `TDD-INT-RECON-001` v2.0 §3
(C-01) caught this. Corrected in §3.3 below by splitting syntax from semantics.

**Defect 2 — "three" versus "four" executable L0 tests.** `A2-C01…C07-1.0` §1 said **three** of
ten L0 tests were executable today; §3.7 said **four** L0-data tests "I can run today". Both
sentences were about different sets without saying so. Resolved precisely in §9.2, by
enumeration rather than by choosing one of the two numbers.

### 0.3 What I did and did not do

| Action | Status |
|---|---|
| Read `A1-R1` v1.0 in full (1,262 lines) | **done** |
| Read `TDD-TD-INT-001` v1.2 in full | **done** |
| Read `TDD-INT-RECON-001` v2.0 in full | **done** |
| Read my own `A2-C01…C07-1.0` against `A1-R1`, clause by clause | **done** |
| Ran the checks I already own (`contract_data_checks.py`, document tests) | **done**, §9.1 |
| Wrote any C++, Core type, enum, struct, tag or `.uproject` | **no** |
| Merged any branch, or checked out any branch but mine | **no** |
| Frozen any API, or marked any contract `AGREED` | **no** |
| Run any *contract acceptance test* from either submission | **no** — none exists |
| Re-run Agent 3's review, or claim Agent 3 re-ran mine | **no** — Agent 3 ran no tests (§9.4) |

### 0.4 The standard this review holds itself to

The request says: *"The objective is genuine technical agreement, not merely a document showing
two similar proposals."* I take that seriously, which means two disciplines:

1. **I do not mark anything agreed.** Even where `A1-R1` matches my position closely — C-03
   is the clearest case — a shared direction is not approval of a specific version. §1 records
   `0 of 7` agreed, and §1.3 explains why that is the honest number rather than a failure.
2. **Where I disagree, I name the clause and the consequence**, not the preference. The
   substantive disagreements in this review are §3.4 (A1's route ID cannot address 4 of 8
   traversal locations — this is the most important finding in the document) and §8.6
   (a `Retired` status I cannot implement from data I do not have).

---

## 1. Verdict summary

### 1.1 The seven verdicts

| Contract | A1-R1 version reviewed | Verdict | Blocking clause(s) | Will I approve a revised version? |
|---|---|---|---|---|
| **C-01** | `A1-R1` §1.1–§1.9 | **PARTIALLY AGREE** | §3.4 route-ID format cannot address 4 of 8 parents; §3.5 capability grant model | **Yes**, conditional on §3.4 |
| **C-02** | `A1-R1` §2.1–§2.9 | **PARTIALLY AGREE** | §4.4 field classification; §4.9 invalidity shape | **Yes**, conditional on field set |
| **C-03** | `A1-R1` §3.1–§3.9 | **AGREE IN PRINCIPLE — NOT AGREED** | §5.5 MEAD §5.4 reading needs TD ruling (TD-09) | **Yes** |
| **C-04** | `A1-R1` §4.1–§4.10 | **PARTIALLY AGREE** | §6.4 recovery notification absent; §6.5 representation I will not adopt | **Yes**, conditional on TD-02 + recovery |
| **C-05** | `A1-R1` §5.1–§5.10 | **AGREE IN PRINCIPLE — NOT AGREED** | §7.4 half-open window needs one worked example | **Yes** |
| **C-06** | `A1-R1` §6.1–§6.9 | **DISAGREE** | §8.4 per-frame `TickInteract` is the wrong shape | **Yes**, with a counter-proposal (§8.4) |
| **C-07** | `A1-R1` §7.1–§7.8 | **REQUIRE CLARIFICATION** | §9.4 `Retired` implementability; §9.5 namespace provenance | **Yes**, conditional on answers |

**Agreed: 0 of 7.** Not a formality — §1.3.

### 1.2 Counts

| | |
|---|---|
| Contracts reviewed | **7 of 7** |
| Marked `AGREED` | **0** — I approve no exact version in this document |
| `PARTIALLY AGREE` | **3** (C-01, C-02, C-04) |
| `AGREE IN PRINCIPLE — NOT AGREED` | **2** (C-03, C-05) |
| `DISAGREE` | **1** (C-06) |
| `REQUIRE CLARIFICATION` | **1** (C-07) |
| **A1 clause rows reviewed** | **71** |
| A1 clauses accepted without change | **28** |
| A1 clauses accepted with a named revision | **21** |
| A1 clauses rejected | **2** |
| A1 clauses partially accepted | **1** |
| A1 clauses needing clarification | **1** |
| A1 dependency tables answered | **2** (the other five are answered in prose) |
| New Agent 2 requirements on A1 | **16** (§12.2) — 9 strictly A1's, 7 routed through A1 to TD |
| Items still needing TD | **11** (§10) — 8 open from A1, 1 closed, 2 new |
| Checks and document tests executed | **9 checks + 23 + 37 tests** (§11.1–§11.2, §14) |
| Contract acceptance tests run | **0** |

### 1.3 Why "0 agreed" is the right answer and not a stalling tactic

I want to be explicit, because a review that agrees with nothing looks like obstruction.

**C-03 and C-05 are close.** For C-03, `A1-R1` §3.2's four-stage separation, §3.4's
health-independence invariant, §3.5's duplicate rules and §3.5's stale-lifetime table are
almost exactly what I asked for in `A2-C01…C07-1.0` §6. For C-05, `A1-R1` §5.3's half-open
window convention and §5.4's "telegraph ≠ damage" rule are stronger than my proposal, and I
prefer them.

I still do not mark either `AGREED`, for two reasons that are structural rather than
temperamental:

1. **`AGREED` is defined as approval of the same exact version.** `A1-R1` has nine open TD
   items (its §8.2) that change the shape of what I would be approving. Approving now would
   mean approving a proposal whose own author says four of its seven contracts are not ready.
2. **TD v1.2 §4.1 requires producer *and* consumer to sign the same version**, and §7.3 says
   TD reviews only after both sides' exact-version responses exist. My signature on `A1-R1`
   would create a record TD has explicitly said it will not act on yet.

So `AGREE IN PRINCIPLE — NOT AGREED` is the accurate label. §5.8 and §7.6 state the precise
conditions under which I would sign a specific revised version.

---

## 2. Method — how each verdict was reached

### 2.1 The rule I applied to every clause

I did not ask "does this look like my proposal?" I asked four questions in order:

1. **Does it contradict a pinned ownership decision?** If yes → `DISAGREE`, name the conflict.
2. **Does it require me to author, persist or validate data I do not have and cannot source?**
   If yes → `DISAGREE` or `REQUIRE CLARIFICATION`, and say which data is missing.
3. **Would implementing it as written produce a defect at a boundary I already own** —
   streaming, unload, 57-location parenting, scene absence? If yes → `PARTIALLY AGREE` with a
   named counter-proposal.
4. **Otherwise** → accept, and say so without hedging.

Rules 2 and 3 did most of the work. §3.4 and §8.4 both came out of them.

### 2.2 What I refuse to do

| Refused | Why |
|---|---|
| Infer agreement from compatible direction | The request forbids it explicitly; §1.3 shows it would also be wrong |
| Smooth a real difference into a "combined position" | TD v1.2 §4 forbids collapsing; differences are visible or the document is worthless |
| Accept a clause because it is well written | `A1-R1` is a strong document. Quality of argument is not evidence of correctness at my boundaries |
| Reject a clause because it is inconvenient for my existing data | If `A1-R1` is right and I am wrong, I say so — §3.4 is the reverse case, where my *field* survives and A1's *format* does not |
| Convert a TD decision into my preference | Where authority is TD's I state the required boundary and leave the decision (§10.3) |
| Claim any contract test passed | None ran. §9.2 separates what executed from what is proposed |

### 2.3 Evidence discipline

The request requires five evidence categories to stay separate. They are:

| Category | Count | What it is | Executed? |
|---|---|---|---|
| **(a)** Independent data checks | **9** | `Tools/world/contract_data_checks.py` | **Yes**, §9.1 |
| **(b)** Document tests | **23** | `Tools/world/tests/test_contract_submission.py` | **Yes**, §9.1 |
| **(c)** Proposed contract acceptance tests | **42** | Named in `A2-C01…C07-1.0`, unique IDs, re-enumerated in §9.3 | **No** — 0 run |
| **(d)** Analysis queries run *for this review* | **9** | Ad-hoc Python over fixtures; §9.5 lists each | **Yes**, but they are **not tests** |
| **(e)** Repository suite | see §9.1 | canon + world + L0 gate | **Yes** |

Category (d) is the one that needs watching. Several findings in this review — including the
4-of-8 scene gap in §3.4 — came from running a query, not from a stored test. A query that
produced a finding is **not** a test that guards it. §13.2 states what would have to exist for
each finding to become a real test, and none of those tests exist.

---

## 3. C-01 — Traversal

**A1 proposal reviewed:** `A1-R1` §1.1–§1.9, exact version v1.0.
**Verdict: PARTIALLY AGREE.**

### 3.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §1.2 | Five capabilities: Vault, Mantle, LedgeShimmy, Drop, ClimbLadder | **ACCEPT** |
| §1.2 | Behaviour/entry/exit definitions per capability | **ACCEPT with note** §3.3 |
| §1.2 | "No capability added without an ADR" | **ACCEPT** |
| §1.2 | Out-of-scope list (wall-run, slide, swing, zip-line, ledge leap) | **ACCEPT** |
| §1.3 | Query ownership = A1; request/result shapes | **ACCEPT with note** §3.3 |
| §1.3 | Deterministic selection: priority → facing → distance → RouteId lexicographic | **ACCEPT** |
| §1.3 | Frame-scoped validity; revalidate at execution | **ACCEPT** |
| §1.4 | Seven query outcomes, distinct from execution failure | **ACCEPT with revision** §3.6 |
| §1.5 | `RouteId` format `TRV.<ChapterId>.<SceneId>.<NNN>` | **REJECT** §3.4 |
| §1.5 | Ten requested marker fields | **ACCEPT with revisions** §3.7 |
| §1.5 | A1 never parses `RouteId` | **ACCEPT** |
| §1.6 | M1 v1.4 preservation table | **ACCEPT — no change requested** §3.8 |
| §1.6 | Seven abort paths / no self-cancel | **ACCEPT** |
| §1.7 | Two acceptance tests | **ACCEPT with additions** §3.9 |
| §1.8 | Five Agent 2 dependencies | **ANSWERED** §3.10 |

### 3.2 The five capabilities — I accept all five, unconditionally

| Capability | Tag requested | My authored requirement | Accept? |
|---|---|---|---|
| `Vault` | `Traversal.Capability.Vault` | obstacle ≤ 100 cm, landing beyond | **Yes** |
| `Mantle` | `Traversal.Capability.Mantle` | ledge 100–200 cm, headroom ≥ capsule | **Yes** |
| `LedgeShimmy` | `Traversal.Capability.LedgeShimmy` | hang state, lateral continuity | **Yes** |
| `Drop` | `Traversal.Capability.Drop` | controlled descent ≤ 300 cm | **Yes** |
| `ClimbLadder` | `Traversal.Capability.ClimbLadder` | ladder volume, bottom/top anchors | **Yes** |

**No counter-proposal on the vocabulary.** This is the one part of C-01 where A1's answer is
better than my question: my `A2-C01…C07-1.0` §4 deliberately deferred capability naming to
Agent 1 and offered only an "enum shape with AND/OR groups and a tag escape hatch". A1 has now
named them, defined them executablely, and given each a tag. **The names are A1's and I adopt
them without modification.**

One note on §1.2's definitions, not a disagreement: the entry/exit conditions are stated as
**authoring constraints for me to satisfy**, and I read them that way. `Vault ≤ 100 cm` and
`Mantle 100–200 cm` are gate conditions my marker data must express, and A1's executor
revalidates. If A1 intended those numbers as *runtime assertions that can reject an authored
marker*, the failure needs a distinct outcome (`InvalidAuthoredData`, not `UnsupportedByPlayer`),
which §1.4's table does supply. I am flagging the reading, not contesting it.

### 3.3 Capability requirements — the data/code question A1 answers only partly

This was **C01-Q2** in my submission, unanswered. `A1-R1` §1.3 answers it structurally:

| Aspect | A1's answer | Adequate for me? |
|---|---|---|
| Route declares requirement as `FGameplayTagContainer` (`RequiredCapabilityTags`) | Yes, §1.5 | **Yes** |
| Player's capabilities arrive in the query request as `CapabilityTags` | Yes, §1.3 | **Yes** |
| Tag is authored requirement; enum is executable branch | Yes, §1.2 | **Yes — this is the answer** |
| AND/OR grouping between requirements | **Not addressed** | **No** — my C-01 must express "Vault OR Mantle" and "Vault AND ClimbLadder" |
| Cumulative vs independent | **Not addressed** | **No** |
| Requirement revocation | **Not addressed** | **No** |

A1's model is **a flat tag container**: all tags present ⇒ eligible. That is a conjunction
(AND) with no disjunction. My `A2-C01…C07-1.0` §4 proposed AND/OR groups because Chapter 1
has routes where either `Vault` or `Mantle` clears the same obstacle depending on approach.

**This is my C-01 disagreement #2, and it is minor but real.** `A1-R1` §1.5 says
`RequiredCapabilityTags` "No (default: `CapabilityTag`)" — a single tag default, a container
override. Between them there is no way to express OR.

I am **not** asking A1 to accept an AND/OR structure now. I am asking a narrower question,
raised as **A2R-1**: *does `RequiredCapabilityTags` require all tags (conjunction), or does A1
permit my authoring layer to pre-evaluate a grouping and emit only the single tag that must be
present?* The second option needs nothing from A1 and lets me express OR offline. **If A1
confirms conjunction semantics, I will author accordingly and withdraw the AND/OR request.**

**Revocation** (C01-Q4): A1 does not address it, and I will not invent it. My position: a route
whose requirement tags were satisfied at query time and are no longer satisfied at execution
time must **not** start, and must return a distinguishable outcome. `A1-R1` §1.3 already
covers this — "at execution start Agent 1 re-queries; if the same `RouteId` no longer wins,
execution does not begin (log `Traversal.QueryExpired`)". **I accept that as the revocation
answer** and withdraw C01-Q4. It is answered, just not under that heading.

**Context** (C01-Q5, water/rope): still unanswered, and now concretely evidenced. The register
gives me `CH01-TRV-003 The Stream Crossing` and `CH01-TRV-004 The Ravine and Liana Bridge`,
both **PROPOSED**. A1's five capabilities contain nothing that describes *how* a stream is
crossed or *how* a liana bridge is used. Those routes must either decompose into the five
capabilities (a bridge is `ClimbLadder`? a stream is `Vault`?) or need a sixth. **A1's own rule
says a sixth capability needs an ADR**, so I am not requesting one — I am asking, as
**A2R-2**, how A1 intends TRV-003 and TRV-004 to be authored within the existing five, or
whether they are out of scope for the slice.

### 3.4 `RouteId` — I reject the format, and this is the substantive finding

**A1's clause (`§1.5`):**

```
TRV.<ChapterId>.<SceneId>.<NNN>      e.g.  TRV.CH01.SCN-014.001
```

**Why I reject it.** The format requires a `SceneId` for every route. Four of the eight
traversal-capable Chapter 1 locations host **no scene at all**.

I ran this against the authoritative fixtures:

| Traversal-capable location | Register name | Canon | Scenes hosted |
|---|---|---|---|
| `CH01-SUB-009` | Streets | ESTABLISHED | 1 |
| `CH01-SUB-020` | The Back Lanes | PROPOSED | 1 |
| `CH01-TRV-001` | The Threshold Path | PROPOSED | **0** |
| `CH01-TRV-002` | The Root Way | PROPOSED | **0** |
| `CH01-TRV-003` | The Stream Crossing | PROPOSED | **0** |
| `CH01-TRV-004` | The Ravine and Liana Bridge | PROPOSED | **0** |
| `CH01-TRV-005` | Roads | **ESTABLISHED** | 1 |
| `CH01-EXP-003` | The Forgotten Path | PROPOSED | 1 |

The 46 captured Chapter 1 scenes span 38 distinct locations. **The four `TRV-*` locations
that give the family its name appear in no scene row.** They are, by the register's own
description, pure traversal corridors: that is what "Traversal Area, Exterior" without a story
or scene role means.

**Consequence if I implement A1's format as written:** to name a route on `TRV-002 The Root
Way` I must invent a `SceneId`. Inventing a scene is prohibited — scenes are canon register
content (`CH01-SCN-001…046`), and my own standing constraint is that I do not invent canon. So
I either fabricate a scene or I cannot name the route. Both are unacceptable, and the second
means **the four central traversal corridors of Chapter 1 cannot have routes.**

**This is not a formatting preference.** It is a case where `A1-R1`'s identity scheme assumes a
content structure — every route belongs to a scene — that the authoritative register does not
have. A1 had no way to know this; the scene register is my source, not theirs. But the format
cannot ship.

**Proposed alternative, `PROPOSED — NOT FROZEN`** — issued as **A2R-3**:

```
FTDDRouteId.Key = "<PARENT_LOCATION_ID>/ROUTE-<LETTER>"
e.g.  CH01-TRV-002/ROUTE-A
      CH01-SUB-009/ROUTE-B
      CH01-EXP-003/ROUTE-A
```

| Property | Why |
|---|---|
| Parent is a **location**, never a scene | All 8 traversal-capable locations are locations; 4 have no scene |
| Anchor = "Category contains `Traversal Area`" | Preserves the multi-valued rule; do not gate on prefix |
| Letter, not number | `ROUTE-A` is stable and human-readable; adding a route does not renumber siblings |
| Opaque to A1 | A1's own rule (§1.5 "Agent 1 must never parse it") is preserved exactly |
| Survives streaming | It is authored content, not a transform; A1's requirement in §1.5 |
| `SceneId` becomes optional diagnostics | A1's §1.5 already lists `ChapterId`/`SceneId` as "No" (optional) — this is consistent with their own table |

**What this costs A1: nothing structurally.** Their field is `FName`, opaque, never parsed.
The format lives entirely in the validator I own. The only thing that changes is the string my
validator accepts and the sample in their document.

**What I will not do:** claim A1's format is unsalvageable. If A1 can supply a scene-or-parent
fallback rule — `SceneId` when a scene exists, parent location otherwise — that also works, and
it is their call. I am rejecting the *unconditional* `SceneId` requirement, not the ordering of
the fields.

### 3.5 Capability grant model — a question I cannot answer alone

`A1-R1` §1.3 puts `CapabilityTags` in the **query request**: the caller passes the player's
granted capabilities. That means the requester supplies its own eligibility input.

For A1 calling A1 (their own component querying itself) this is fine — no adversary, no
boundary. But it is a contract surface I also consume for authoring validation, and it means
**the authoritative capability set is not queryable from anywhere but the request**. My editor
validator, by design, has no player.

I am **not** alleging a security or correctness bug; single-player, single local player. I am
recording a **REQUIRE CLARIFICATION** item, **A2R-4**: *is there a read-only way for a non-player
caller to obtain the player's current capability set for offline validation, or is the
validator expected to assume the full set?*

Recommended answer, for A1 to accept or reject: the validator assumes the **union of all
capabilities the slice can grant**, so authoring never fails on a capability the player might
have. That keeps the validator offline and conservative. **Not a decision I may take.**

### 3.6 The outcome vocabulary — I accept it, and I will not map mine onto it

`A1-R1` §1.4's seven outcomes are clear and I accept them as A1's:

`None` · `CandidateFound` · `UnsupportedByPlayer` · `InvalidAuthoredData` · `BlockedPath` ·
`WorldUnavailable` · `Cooldown`

My `A2-C01…C07-1.0` §4 used `Available` · `Blocked` · `Unloaded` · `Invalid` · `NoCandidate`.
`TDD-INT-RECON-001` v2.0 D-02 says: do not map or collapse these without explicit review.

**My review: A1's vocabulary supersedes mine for the player query.** Reason — A1 owns the query
(§1.3), the outcomes are its return values, and mine were authored from the outside. Mapping
two vocabularies where one is the producer's return type is exactly how enums drift.

What I keep from my own proposal, and why it is not a duplicate:

| My concern | Where it lives now | Why not A1's enum |
|---|---|---|
| Authoring-time marker validity | **Editor validator result**, not a runtime enum | A1's `InvalidAuthoredData` is a *runtime* query outcome; authoring validity must be decidable with no world and no player |
| Route enabled/disabled by narrative | **`EnabledCondition`** on the marker (§1.5, A1's own field) | This is not a query outcome; the route is absent from the query, not "returned as disabled" |

So: one runtime vocabulary (A1's), one authoring vocabulary (mine, editor-only), one gating
mechanism (A1's `EnabledCondition`, which I populate). **No enum mapping, no second runtime
vocabulary.** I consider D-02 resolved from my side by this paragraph, subject to A1 agreeing
that my editor validator results never appear on a runtime query result.

**One acceptance condition on §1.4:** `UnsupportedByPlayer` shows **no prompt**, and A1 calls
that "deliberately no locked affordance". I agree and have no locked-prompt design. But
`InvalidAuthoredData` must be impossible to reach in a shipping build for authored content —
it is an authoring defect. A1's §1.4 marks it `Error`; I additionally need it to fail my L0
authoring gate so it cannot reach a build. That is a shared test, raised in §3.9.

### 3.7 The ten marker fields — I accept seven, revise two, reject one

| A1 field (§1.5) | My decision | Note |
|---|---|---|
| `RouteId` `FName` | **ACCEPT with revised format** | §3.4 |
| `CapabilityTag` `FGameplayTag` | **ACCEPT** | Direct mapping to §3.2 |
| `EntryAnchor` `FTransform`/component | **ACCEPT** | Must be a world transform I author; not derived at runtime |
| `ExitAnchor` `FTransform`/component | **ACCEPT** | Required; A1 revalidates |
| `RequiredCapabilityTags` container | **ACCEPT, pending A2R-1** | §3.3 conjunction question |
| `Priority` `int32` | **ACCEPT** | Higher wins; I author it |
| `bOneWay` `bool` | **ACCEPT** | Default false |
| `EnabledCondition` project type | **ACCEPT with revision** | §3.7.1 — needs to be evaluable offline |
| `ChapterId`/`SceneId` `FName` | **ACCEPT as optional diagnostics** | `SceneId` may be empty — this is the §3.4 fix |
| `EntryToleranceCm`/`ExitToleranceCm` | **REJECT** | §3.7.2 |

**§3.7.1 — `EnabledCondition` must be offline-evaluable.** A1's field is typed "project
condition type (Agent 3 owned)". For my authoring validator to answer "is this route ever
reachable", the condition must be evaluable as *unknown/true/false* statically, not only at
runtime. I need the type to distinguish **"disabled by narrative right now"** from **"cannot be
evaluated offline"**, because a route behind an unevaluable condition must not be reported
`RTE-UNREACHABLE` in my L0 gate. This is a requirement on Agent 3's type, relayed through A1.
Raised as **A2R-5**.

**§3.7.2 — I reject `EntryToleranceCm`/`ExitToleranceCm` (defaults 15/25).** Not because
tolerance is wrong, but because it duplicates physics validation with an authored number and
creates a second answer to "is this placement valid". A1's own §1.5 note says tolerance "does
**not** relax physics validation" — so the field can only ever make an authored marker *fail
earlier*, never pass later. That is an authoring lint, not runtime marker data.

**Counter-proposal:** drop both fields from the marker; A1 uses its existing tolerance
constants. If A1 needs per-route slack, that is evidence a route's anchor is authored wrong,
and my validator should reject it rather than let a number paper over it.

### 3.8 M1 v1.4 preservation — accepted, and I request no change

`A1-R1` §1.6's preservation table is exactly the semantics my contract must not disturb:

| Element | A1's statement | My position |
|---|---|---|
| Bounded relocation loop, `MaxRelocationAttempts` clamp `[0,3]` default 3 | preserved | **No change requested** |
| Always-run terminal hold H0/H1/H2, never budgeted | preserved | **No change requested** |
| `ApplyCandidateNow()` sole transform writer; stale transform never applied | preserved | **No change requested** |
| Restoration ordering, exactly once | preserved | **No change requested** |
| `FellOutOfWorld` as flow outcome, not placement | preserved | **No change requested** |
| Seven exit paths E1–E7, no self-cancel | preserved | **No change requested** |

The request asks me to preserve "Agent 1's M1 v1.4 traversal fallback, terminal hold and
restoration requirements". **They are preserved by not being in this contract at all** — my
C-01 defines authored data and offline validation; A1's defines execution. The only overlap is
the abort **trigger** (does a marker streaming out abort?), and `A1-R1` §1.6 answers it
correctly: **it does not abort**, because the recorded exit is authoritative and revalidated at
write. I accept that without qualification, and it resolves a genuine question in my §3.4
lifecycle table.

**One consequence worth stating:** my `A2-C01…C07-1.0` §3.4 said "Actor destroyed mid-attempt →
Attempt **cancels**". That is **wrong** and I withdraw it. A1's §1.6 and §1.7 case 2 say the
traversal completes. A1 is right: cancelling mid-montage on a streaming event would be a
teleport risk, and the exit-anchor revalidation makes cancellation unnecessary. **This is the
third correction to my own submission in this document**, alongside §0.2's two.

### 3.9 Tests I accept, plus two I need added

`A1-R1` §1.7 proposes two tests. I accept both and **do not** propose replacing them.

| A1 test | My acceptance |
|---|---|
| `TDD-Contract.Traversal.PlayerQueryAndFailureSemantics` (§1.7, 8 cases) | **ACCEPT.** Cases 1, 2, 3, 4, 6, 7, 8 impose no data burden on me; case 5 (blocked exit introduced after query) requires my marker to expose a validated exit — I accept that obligation |
| `TDD-Functional.Traversal.MarkerStreamingLifetime` (§1.7, 3 cases) | **ACCEPT.** Case 2 (stream out mid-montage does not abort) is the one that settles my §3.8 withdrawal |

**Two additions I require** — mine to run, in my layer, not A1's:

| Proposed addition | Asserts | Why A1 needs it |
|---|---|---|
| `TDD-Contract.World.RouteKeySyntaxAcceptsAllPermittedFamilies` | Route-key syntax accepts every permitted registered location family; the check does **not** assert traversal eligibility from prefix | Guards the §0.2 Defect 1 recurrence |
| `TDD-Contract.World.RouteParentCategoryIsTraversal` | Resolves each `ParentLocationId` to the authoritative register and requires its multi-valued Category to contain `Traversal Area`; **a `TRV-`-prefix-only implementation fails this test** | The semantic half of the same rule |

That is the syntax/semantics split the request requires of me and `TDD-INT-RECON-001` v2.0 §3
requires of both agents. **Neither test is run; neither is implemented in this task.**

### 3.10 A1's five Agent 2 dependencies — answered

| A1 dependency (§1.8) | My answer |
|---|---|
| 1. Marker representation (actor / data asset / data-table row) and registration timing | **Data asset per route + a thin marker actor for in-level streaming.** Route content is a data asset (validatable offline in bulk); the actor exists only to give the route a streaming lifetime. This gives A1 the §1.1 "streamed-in lifetime" they asked for without making route content un-validatable. `PROPOSED — NOT FROZEN` |
| 2. Confirmation of the ten fields | **Seven accepted, two revised, one rejected** — §3.7 |
| 3. `RouteId` format agreement; will narrative/save reference it? | **Format rejected as written**, alternative in §3.4. Route references: **no narrative or save content references a route** in Chapter 1. Save state is scene/flag-based. Raised as **A2R-6** for TD to confirm before A1 sets retirement policy |
| 4. Any route one-way, gated, or needing capabilities beyond default? | **Yes to all three.** `bOneWay` is needed for the ravine bridge descent; `EnabledCondition` is used by the memory-gated `CH01-SUB-001`-adjacent routes; Chapter 1 routes use `Vault`, `Mantle` and `ClimbLadder`, not the full five. No count stated — the routes are not authored |
| 5. Validator behaviour on invalid markers (block save? warn only?) | **Block.** An `InvalidAuthoredData` route must fail the L0 gate and cannot be cooked. A1's §1.4 classifies it `Error`; I make that error build-blocking |

### 3.11 C-01 — what a revised version must contain for my approval

I will approve a revised C-01 when all four are true:

1. `RouteId` no longer requires a `SceneId` — either my §3.4 format or A1's own scene-or-parent rule.
2. `RequiredCapabilityTags` semantics stated as conjunction or disjunction (A2R-1).
3. `EntryToleranceCm`/`ExitToleranceCm` removed, or a reason given why a tolerance may pass a placement physics rejects.
4. `EnabledCondition` evaluable offline as unknown/true/false (A2R-5).

Everything else in `A1-R1` §1 I accept as written. **The five capabilities, the selection
policy, the outcome table, the M1 preservation table and both tests need no revision.**

---

## 4. C-02 — Read-only player context and state snapshots

**A1 proposal reviewed:** `A1-R1` §2.1–§2.9, exact version v1.0.
**Verdict: PARTIALLY AGREE.**

### 4.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §2.2 | Three separate snapshots + frame envelope | **ACCEPT** — better than my single snapshot |
| §2.2 | `FTDDLocomotionSnapshot` fields | **ACCEPT with 2 classified unrequested** §4.4 |
| §2.2 | `FTDDActionControlSnapshot` fields | **ACCEPT with 1 classified unrequested** §4.4 |
| §2.2 | `FTDDCombatStatusSnapshot` fields | **ACCEPT with 1 conditional** §4.4 |
| §2.2 | `FTDDPlayerContextFrame` envelope | **ACCEPT with revision** §4.9 |
| §2.3 | Field-by-field justification table | **ACCEPT method, revise verdicts** §4.4 |
| §2.4 | Cadence, ordering, pause, level transition | **ACCEPT** |
| §2.5 | Three-layer read-only enforcement | **ACCEPT — strongest part of the contract** |
| §2.6 | Failure and invalidation | **ACCEPT with revision** §4.5 |
| §2.7 | Ten acceptance cases | **ACCEPT with additions** §4.7 |
| §2.8 | Five Agent 2 dependencies | **ANSWERED** §4.8 |

### 4.2 Agent 1 remains the sole authority for player mutation — confirmed without reservation

The request asks me to confirm this. **I confirm it, and I add that `A1-R1` §2.5 makes it
enforceable rather than merely stated.**

`A1-R1` §2.5's three layers are better than my proposal, which named the rule and did not
enforce it:

| Layer | A1's mechanism | My assessment |
|---|---|---|
| Type | Plain `USTRUCT`s of values, no setters, `const` accessors returning by value | Correct. A returned copy cannot write back |
| API | Only `bool GetPlayerContext(FTDDPlayerContextFrame&) const` + delegates; no `Set*`, no `BlueprintCallable` mutator, no friend | Correct, and the Blueprint-callable exclusion matters — a `BlueprintCallable` setter would be a hole |
| Test | Mutate a returned copy, assert stored frame unchanged; introspect `UFunction`s for non-const mutators | **This is the layer that makes it real**, and I did not propose it |

**Adopted without change.** My `A2-C01…C07-1.0` §5 said "read-only snapshot; never mutates
player-owned state". A1's §2.5 is how that sentence becomes a property rather than a promise.
I have nothing to add.

### 4.3 The three-snapshot structure

My proposal had **one** immutable snapshot. A1 has **three plus an envelope**. A1 is right and I
am wrong, for a reason I should have seen:

`A2-C01…C07-1.0` §5's single snapshot merged locomotion state with combat state. A1's §2.2
splits them because the v1.4 control-state vs movement-mode matrix depends on them being
independent — a player can be `Staggered` (control) while `Falling` (locomotion). A merged
struct makes that pair representable as one value and invites a consumer to read a combined
"player state" that cannot express the combination.

**I accept the three-snapshot structure and withdraw the single-snapshot proposal.** This is
correction **#4** to my own submission.

### 4.4 Field classification — required / conditional / unrequested

The request requires every field classified, with a **named consumer** for anything conditional.
I am classifying against the consumers I actually have in Chapter 1. If I cannot name a
consumer, the field is unrequested — that is the rule the request sets and I apply it to
myself.

#### Locomotion snapshot

| Field | Class | Named consumer and use case |
|---|---|---|
| `Velocity` (FVector) | **REQUIRED** | Enemy AI pursuit and interception — computes a lead point for a charge; boss chase phases use direction to choose a cut-off |
| `Speed2D` | **REQUIRED** | Crowd/ambient reaction in `CH01-SUB-006 Village Square` — a crowd disperses when the player is sprinting, holds when walking. This is the only consumer that needs magnitude without direction |
| `bGrounded` | **REQUIRED** | Ground-only attack selection; ledge-awareness for AI that must not walk off `CH01-SUB-005 Waterfall Escarpment` |
| `HeightAboveGround` | **CONDITIONAL** | Consumer: the traversal-facing AI in `CH01-TRV-004` deciding whether to commit to a ground attack. If that AI is not in the slice, this field is **removed** |
| `MovementMode` | **REQUIRED** | Air-dodge/fall reaction; distinguishes a player who can be hit by a ground sweep from one who cannot |
| `GroundSlopeDegrees` | **UNREQUESTED** | No Chapter 1 consumer. Crowd, boss, encounter and narrative logic all work from `bGrounded`/`bOnWalkableFloor`. **I do not request it** |
| `bOnWalkableFloor` | **CONDITIONAL** | Consumer: crowd placement checks that the player is on traversable ground before triggering a scripted greeting in `CH01-SUB-011`. Removable if that trigger is dropped |

#### Action/control snapshot

| Field | Class | Named consumer and use case |
|---|---|---|
| `ControlState` (enum) | **REQUIRED** | Boss phase logic — the punish window after `Stagger`; scripted camera gating on `Cinematic` |
| `ControlStateTag` | **REQUIRED** | Tag-driven AI conditions without an interface dependency (A1's §2.3 rationale, which I accept) |
| `StateElapsedSeconds` | **CONDITIONAL** | Consumer: boss fairness pacing — do not re-attack a player fresh out of `Stagger` within 0.5 s. Removable if that pacing is dropped |
| `bAllowsInput` | **REQUIRED** | AI must not punish an unresponsive player during a tutorial beat in `CH01-SUB-001` |
| `bLocked` | **REQUIRED** | Same consumer as `bAllowsInput`; `bLocked` distinguishes "montage owns the character" from "input is ignored, character idle" |
| `ActiveActionId` | **UNREQUESTED** | A1's own §2.3 marks it "Required (diagnostics)". **Diagnostics is not a consumer.** I have no Chapter 1 system that branches on which action is locked in. **I do not request it**; it costs A1 nothing to keep as diagnostics and I do not ask for its removal — but it is not part of the read-only surface I consume |

#### Combat status snapshot

| Field | Class | Named consumer and use case |
|---|---|---|
| `CombatState` | **REQUIRED** | Encounter victory/defeat flow; boss "combat is live" gating |
| `bAlive` | **REQUIRED** | Death flow, encounter manager, memory-fragment gating |
| `HealthFraction` | **CONDITIONAL — WITHDRAWN** | **I withdraw my earlier interest.** `A2-C01…C07-1.0` §5 asked for health for boss phase bands. On review I do not need HP bands: Chapter 1 boss phases key on `PostureFraction` and stage, not health. **Withdrawn.** A1's §2.3 correctly makes it conditional; the condition fails, so the field should be **removed** |
| `PostureFraction` | **REQUIRED** | Boss phase transition (`CH01-BOS-001 Great Root Mother Arena` phase 2 keys on posture break, not health); enemy AI aggression when posture is low |
| `bIsStaggered` | **REQUIRED** | Punish-window timing |
| `StaggerRemainingSeconds` | **REQUIRED** | AI decides whether to commit to a punish that fits in the remaining window |
| `bIsTelegraphing` | **REQUIRED** | Enemy defensive response to a player attack (mirrors `ITDDCombatant`, A1 §5) |
| `TelegraphRemainingSeconds` | **CONDITIONAL** | Consumer: boss defensive timing in `CH01-BOS-001`. Removable if the boss blocks on `bIsTelegraphing` alone, which it can |

#### Envelope

| Field | Class | Named consumer and use case |
|---|---|---|
| `EntityId` | **REQUIRED** | Damage routing correlation; encounter membership |
| `FrameCounter` | **REQUIRED** | Freshness — the only reliable way to reject a stale frame (§4.5) |
| `WorldTimeSeconds` | **REQUIRED** | Diagnostics and cross-check against gameplay time (C-05) |
| `GameplayTimeSeconds` | **REQUIRED** | Telegraph window comparison must use the same clock as C-05, or pause/hitstop desynchronise |
| `ActorLocation` | **REQUIRED** | Perception, encounter volumes, narrative triggers |
| `ActorRotation` | **REQUIRED** | Facing-dependent prompt and AI approach |
| `AimDirection` | **REQUIRED** | AI facing prediction; also the focus cone axis for C-06 |
| `CurrentTarget` (`TWeakObjectPtr`) | **CONDITIONAL** | Consumer: encounter threat/aggro priority. Removable in favour of `CurrentTargetEntityId` alone if A1 prefers to drop the weak pointer entirely — I would support that |
| `CurrentTargetEntityId` | **REQUIRED** | Threat routing that must survive target destruction |

**Net effect on A1's field set:** I request **removal** of `HealthFraction` (condition fails),
`GroundSlopeDegrees` and `ActiveActionId` (no consumer). I mark `HeightAboveGround`,
`bOnWalkableFloor`, `StateElapsedSeconds`, `TelegraphRemainingSeconds` and `CurrentTarget` as
**conditional and removable**. Everything else I require.

**A note on `ActiveActionId`:** A1's §2.3 calls it "Required (diagnostics)" and its §2.8
dependency 1 asks me to confirm fields "with the decision each enables — and explicit removal
of the rest". Diagnostics is a legitimate reason for A1 to keep a field internally. It is not a
reason for it to be in the shared read-only contract. I record it as unrequested, which is
different from asking for its deletion.

### 4.5 `CarryState` and `CameraForward` — the two fields A1 does not have

`TDD-INT-RECON-001` v2.0 §3 (C-02) records my `A2-C01…C07-1.0` proposal as requesting
`Velocity` and `CameraForward` as "requested but not required", and `CarryState` as **REQUIRED
for route gating**. `A1-R1` has no `CarryState` field and no `CameraForward` field. Resolution:

| Field | My position after review | Reason |
|---|---|---|
| `CameraForward` | **WITHDRAWN** | `AimDirection` covers the only consumer I had (AI facing prediction). A1's §2.3 justification for `AimDirection` is the same decision I wanted `CameraForward` for. **Two fields for one use case is how the merged-state problem returns.** Withdrawn |
| `CarryState` | **REQUIRED, but relocated** | Consumer: route gating — a player carrying a large object cannot `LedgeShimmy`; a player carrying a vessel cannot `Vault`. But **this does not belong in a player snapshot.** It is a **route requirement**, and A1 already has the mechanism: `RequiredCapabilityTags` / an eligibility tag container. **I will express carrying as a tag condition on the route, not as a new player-context field.** This means **no new field is needed on A1's side** |

This is the cleanest resolution available and it removes a field from the contract rather than
adding one. Raised as **A2R-7**: *does A1's eligibility filter support a non-capability
negative tag condition (e.g. `State.Carrying.Heavy` blocks `LedgeShimmy`)?* If not, I will
handle it purely in my authoring layer and the contract does not need to change.

### 4.6 Velocity — the one field the reconciliation flagged as disputed

`TDD-INT-RECON-001` v2.0 §3 (C-02) records: A1 requires `Velocity`/`Speed2D`; A2 "requested,
not required". My §4.4 now marks **both REQUIRED** with named consumers (AI interception;
crowd reaction in `CH01-SUB-006`). **I withdraw "requested, not required".** They are required,
the consumers are named, and A1's conditional treatment of them was correct.

### 4.7 Tests I accept, plus one addition

`A1-R1` §2.7's ten cases: **all ten accepted.** Cases 3 (mutate a copy) and 10 (introspection)
are the enforcement of §4.2 and I would not approve C-02 without them.

**One addition I require:**

| Proposed addition | Asserts |
|---|---|
| `TDD-Contract.World.NoCachedContextBeyondOneFrame` | A world consumer holding a frame across two published frames, and acting on it, is detected: the consumer must re-query. Asserts the frame is stale by `FrameCounter` delta, not by wall-clock |

This exists because A1's §2.4 correctly says "A2 must re-query rather than cache beyond one
frame", but no test in §2.7 asserts the **consumer** side — all ten test A1's publisher. The
consumer side is mine.

### 4.8 A1's five Agent 2 dependencies — answered

| A1 dependency (§2.8) | My answer |
|---|---|
| 1. Which fields are actually consumed, with the decision each enables; explicit removal of the rest | **Answered in full, §4.4.** Remove: `HealthFraction`, `GroundSlopeDegrees`, `ActiveActionId`. Conditional: `HeightAboveGround`, `bOnWalkableFloor`, `StateElapsedSeconds`, `TelegraphRemainingSeconds`, `CurrentTarget` |
| 2. Whether HP/posture fractions are needed (phase bands) or must be removed | **HP removed. Posture required.** `CH01-BOS-001` phase 2 keys on posture break, not health |
| 3. Preferred freshness: polling, events, or both | **Both, with the boundary stated:** poll for continuous values and for anything a boss decision reads mid-frame; subscribe for transitions where a missed edge changes a decision (`bAlive` false, `ControlState` → `Stagger`, `CombatState` change). A1's §2.4 ordering rule (snapshot published before the event) makes "re-query on event" safe, which is why both are workable |
| 4. Does any A2 system need context during a cinematic or paused state? | **Yes for cinematic, no for paused.** Cinematic: the narrative director and the scripted-camera director both need `ControlState`/`CombatState` to confirm the takeover happened. Paused: no consumer acts while paused; reading a frame frozen at its original timestamp is correct and A1's §2.4 rule is right |
| 5. Stealth/noise: does any approved design need it? | **No. Confirmed exclusion.** No approved stealth design exists in the canon set; I have no consumer. `A1-R1` §2.3's exclusion is correct and I support it staying out |

### 4.9 Invalidation shape — one revision

`A1-R1` §2.4 and §2.6 emit `FTDDPlayerContextInvalidatedEvent { EntityId, Reason }` with
`Reason ∈ { Unpossessed, Despawned, LevelTransition, Paused }`, **and** `GetPlayerContext`
returns `false`.

Two mechanisms for one condition. `Paused` is the odd member: A1's own §2.4 says a paused world
"does not publish frames (no tick)" and consumers "must compare timestamps rather than assume
freshness". If `GetPlayerContext` returns the **last frame** during pause (as §2.4 says) but
`false` during `Unpossessed` (as §2.6 says), then `false` does not mean "invalid" uniformly.

**Revision requested, A2R-8:** state the invariant as a single rule —

> `GetPlayerContext` returns `false` **iff** no frame has ever been published for the current
> session, or the pawn is tearing down. A paused world returns the last published frame with
> its original `FrameCounter`.

and drop `Paused` from the invalidation reasons, since a pause neither invalidates the context
nor stops it existing. If A1 prefers to keep `Paused` as an event (for UI), it should be a
separate **context-paused** notification, not an invalidation.

This is a small thing, but it is the kind of small thing that produces a specific bug: a
consumer that treats `false` as "player gone" will despawn aggro on pause.

### 4.10 C-02 — what a revised version must contain for my approval

1. `HealthFraction` removed, or a named consumer produced by A1 that I have missed.
2. `GetPlayerContext` `false`-semantics stated as one invariant; `Paused` removed from invalidation (A2R-8).
3. `CarryState` handled as a route eligibility condition, not a context field — or A1 states why it must be context (A2R-7).
4. `CurrentTarget` weak pointer either kept with A1's validity rule or dropped in favour of `CurrentTargetEntityId`.

**Everything else in §2 I accept**, including all ten tests and the three-layer read-only
enforcement, which I consider the best-engineered part of `A1-R1`.

---

## 5. C-03 — Hit and damage

**A1 proposal reviewed:** `A1-R1` §3.1–§3.9 and §8.1, exact version v1.0.
**Verdict: AGREE IN PRINCIPLE — NOT AGREED.**

### 5.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §3.2 | Four-stage separation (request / resolution / application / applied event) | **ACCEPT** |
| §3.3 | `SubmitRequest` sequence and A1 arbitration for player-victim hits | **ACCEPT — this is the answer I needed** |
| §3.3 | "Agent 2 must not read the player's attribute set, write health, or re-implement block/parry" | **ACCEPT — matches my own §6 exactly** |
| §3.4 | Health applies irrespective of control resolution | **ACCEPT — strongest invariant in the document** |
| §3.5 | Duplicate, replay, stale-lifetime rules | **ACCEPT** |
| §3.6 | Non-health outcomes table | **ACCEPT with one revision** §5.6 |
| §3.7 | Thirteen acceptance cases | **ACCEPT with additions** §5.7 |
| §8.1 | MEAD §5.4 tension, three options | **ACCEPT A1's reading; TD-09 still required** §5.5 |

### 5.2 I agree that Agent 1 owns arbitration for all hits involving the player

**Stated without reservation.** This is the central ownership question in C-03 and `A1-R1` §3.3
answers it correctly:

> "Agent 1 alone commits health/posture **for the player** and arbitrates all hits against the
> player."

I accept it, and it is what my `A2-C01…C07-1.0` §6 asked for. My proposal said: A2 supplies
enemy/boss hit **intent** only; A1 arbitrates and applies; the applied event is the
authoritative fact I consume. `A1-R1` §3.3 says the same thing from the other side. **No
disagreement on authority, in either direction.**

I confirm my side of it concretely, because a claim is not a contract:

| Agent 2 will | Agent 2 will not |
|---|---|
| Emit `FTDDDamageRequest` from enemy attack windows | Read the player's attribute set |
| Consume `FTDDDamageAppliedEvent` | Write player health or posture |
| Own and write **its own** actors' health via `ITDDDamageable` | Apply damage to the player outside `SubmitRequest` |
| React to `Outcome` for combo/poise/aggro decisions | Re-implement block/parry evaluation against the player |
| Handle `InvalidTarget` when its target is gone | Assume liveness from a stale `EntityId` |

### 5.3 The seven-stage separation the request requires

The request names seven stages. `A1-R1` §3.2 gives four. They are not in conflict — four of the
request's seven are A1's stages, and the other three are authoring, defence-inside-resolution,
and my reaction. Mapped explicitly:

| # | Stage (request) | Where it lives | Owner | `A1-R1` clause |
|---|---|---|---|---|
| 1 | **Attack intent** | Authored attack definition + active-window notify | **Agent 2** (enemy) / Agent 1 (player) | implicitly, §3.2 stage 1 |
| 2 | **Hit detection** | Window overlap against a target | **Agent 2** (its own montage notify) | implicitly |
| 3 | **Hit arbitration / resolution** | dedupe, window check, immunity, block/parry, damage math, classification | **Agent 1 (exclusive)** for any hit involving the player | §3.2 stage 2, §3.3 steps 1–5 |
| 4 | **Defence and mitigation** | block posture, parry, invulnerability | **Agent 1** — step 3 of §3.3 | §3.2 stage 2, §3.3 step 3 |
| 5 | **Health application** | the single attribute commit | **Agent 1** for the player; target's owner for its own actors | §3.2 stage 3, §3.4 |
| 6 | **Exactly-once applied event** | `FTDDDamageAppliedEvent` | **Agent 1** (A1's preference, TD-03 open) | §3.2 stage 4, §3.9 item 1 |
| 7 | **Consumer reactions** | poise, aggro, phase, VFX, audio | **Agent 2** | §3.1 consumers |

**Stages 1 and 2 are mine and I accept them as mine.** `A1-R1` treats them as given rather than
contracting them, which is correct: they are my authored montage and my trace. What A1 requires
of me is only that the request I submit carries the fields in §3.2's struct — and that my
`HitInstanceId` is unique per swing-victim pair, which is A1's dedupe key.

**The boundary that matters: stage 2 is not arbitration.** My hit detection answers "did my
attack's active window overlap the player". It does **not** answer "was the player blocking",
"is the player invulnerable", or "how much damage lands". Those are stage 3 and 4 and they are
A1's. `A1-R1` §3.3 enforces this by having me pass `PreResolvedOutcome` but not decide it —
A1's §3.2 struct carries `PreResolvedOutcome` "as sent by the attacker" and A1's step 3
re-evaluates defence regardless. **I accept that `PreResolvedOutcome` is advisory input, not a
decision.** I want this stated in the contract, because a field named "PreResolved" invites a
consumer to trust it.

### 5.4 One revision: `PreResolvedOutcome` must be advisory in name

**A2R-9:** rename or document `PreResolvedOutcome` as **advisory only** — it must not be able
to cause damage, suppression, or a state change on its own. A1's §3.3 step 3 already behaves
this way. The field name is the risk, not the behaviour.

Concretely, the hazard: an enemy attack's window overlaps a player who started blocking one
frame earlier. My notify computes `Blocked` and sends it. A1's step 3 independently evaluates
block and reaches the same answer. Fine. Now a defect path: my notify computes `Hit` because of
a one-frame ordering difference, and A1 trusts the field. The player takes damage while
blocking. **The contract must make A1's step 3 authoritative and the field advisory, so a
disagreement resolves in A1's favour with a diagnostic.** A1's design already does this; I am
asking that §3.2's comment say so.

### 5.5 MEAD §5.4 — attacker-driven language describes initiation, not arbitration

The request asks directly: *"explain whether attacker-driven language describes attack initiation
or grants arbitration authority."*

**It describes initiation. It cannot grant arbitration authority, and here is why in one line:
authority over a value belongs to whoever owns the resource, and the player's health is not
owned by the attacker.**

`A1-R1` §8.1 identifies the real tension and does not smooth it. My review of the same passage
agrees with A1's reading and adds the reason from my side:

| MEAD §5.4 phrase | What it can mean | What it cannot mean |
|---|---|---|
| "attacker combat component → `FTDDDamageRequest`" | The attacker **authors and submits** a request. This is stage 1. | That the attacker computes the final value |
| "→ `ITDDDamageable::ApplyDamage`" | A call into the target to commit. The target's owner performs it. | That the caller owns the target's health |
| "→ victim's `UTDDCombatComponent`" | The victim's component applies to its own attributes | That the attacker drives the victim's component directly |

Under MEAD read literally with enemy-as-attacker, there are **two arbitration code paths** (one
in A1 for player attacks, one implied in A2 for enemy attacks). `A1-R1` §8.1 says so, and is
right: that turns "one hit → one application → one event" from a structural property into a
coordination discipline between modules.

**My position: A1's Option 1.** A1 arbitrates all hits involving the player; I submit requests.
Reasons, from the side that would otherwise have to implement Option 2 or 3:

1. **Defence logic must live where the defensive state lives.** Block, parry and invulnerability
   are player state. A2 evaluating them means A2 reads player combat state through C-02 and
   reimplements the rules — which both `A1-R1` §3.3 and my own proposal forbid.
2. **Option 3 splits the player's defence rules across my calling code**, so a block bug becomes
   a bug in enemy AI. That is the worst possible place for it.
3. **Option 2 preserves MEAD's diagram at the cost of two arbiters**, which is precisely the
   "two authorities break exactly-once" failure TD v1.2 §4 and `TDD-INT-RECON-001` D-05 warn
   about.

**This remains TD-09 and I do not decide it.** I state my position and note that both agents now
independently prefer Option 1 — which per §1.3 is **not** the same as agreement, since neither
has approved the other's document. The TD ruling is what converts two preferences into one
contract.

### 5.6 Non-health outcomes — one revision

`A1-R1` §3.6 proposes the applied-event matrix. From my side (the consumer), I need exactly one
change:

| Outcome | A1 proposes | My position |
|---|---|---|
| `Applied` | event, yes | **Accept** |
| `Blocked` | event, yes, `Amount` 0 | **Accept — I need this.** My aggression logic must know a block happened; inferring it from a missing event is impossible |
| `Parried` | event, yes | **Accept — required.** The boss reacts to being parried; without an event I cannot distinguish parry from miss |
| `Immune` | event, **no** | **Accept, with a condition** §5.6.1 |
| `WeakPoint` / `KillingBlow` | event, yes, `Outcome` set | **Accept** |
| `Miss` | no event | **Accept** |

**§5.6.1 — the `Immune` condition.** A1 says "A2 may still react via its own tags". If the
reason for immunity is a player state tag I can see in C-02 (`Status.Invulnerable` during a
dodge), that works and I need no event. **But if immunity can arise from a source I cannot
observe, I have no way to react** and my enemy will keep attacking into an immune player, which
is a visible AI defect.

**Condition:** if `Immune` can be produced by anything other than a C-02-observable player tag,
it must publish an event. If immunity is **always** a C-02-observable tag, A1's position stands
and I accept it as written. **This is a question for A1, and it is the only thing between me and
accepting §3.6 unchanged.**

### 5.7 Tests I accept, plus one addition

`A1-R1` §3.7's thirteen cases: **all accepted.** Case 11 (non-staggering damage outside
`AbortWindow`: health applied, traversal continues, control state unchanged) is the one that
proves health independence and I would not approve C-03 without it.

**One addition I require:**

| Proposed addition | Asserts |
|---|---|
| `TDD-Contract.World.EnemyReactionConsumesAppliedFactOnly` | An enemy reaction (poise, aggro, phase) is driven only by the applied event, never by its own request's `PreResolvedOutcome`. A reaction fired from the request is detected as a contract violation |

This is stage 7's guard and it is mine. It also pins §5.4's advisory rule in a test rather than
a comment.

### 5.8 What would make me sign C-03

C-03 is the closest to agreement in this review. I will sign a specific version when:

1. TD-09 is ruled (or A1 and I both state Option 1 in the same version).
2. `Immune` publish condition resolved (§5.6.1).
3. `PreResolvedOutcome` documented advisory (A2R-9).
4. TD-03's four open payload questions settled (§11).

**I am willing to approve, and I expect C-03 to be the first contract we close.**

---

## 6. C-04 — Stagger

**A1 proposal reviewed:** `A1-R1` §4.1–§4.10, exact version v1.0.
**Verdict: PARTIALLY AGREE.**

### 6.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §4.2 | Four classification storage alternatives A/B/C/D | **ACCEPT the analysis; state my position** §6.5 |
| §4.3 | Classification input order, defensive default `Never` | **ACCEPT** |
| §4.3 | Posture-break promotion in the same frame | **ACCEPT** |
| §4.4 | Precedence `Dead > Cinematic > Stagger` | **ACCEPT — preserved exactly** |
| §4.4 | Single winner, superseded logging, never queued downwards | **ACCEPT** |
| §4.5 | Health independence invariant | **ACCEPT** |
| §4.6 | Queued forced targets, publication order | **ACCEPT** |
| §4.7 | Failure/interruption table | **ACCEPT** |
| §4.8 | Fourteen acceptance cases | **ACCEPT with additions** §6.7 |
| — | **Recovery-from-stagger event** | **REQUIRE — absent from A1-R1** §6.4 |

### 6.2 The precedence is preserved, and I verify it rather than trust it

The request requires `Dead > Cinematic > Stagger`. `A1-R1` §4.4 states:

```
Dead (100)  >  Cinematic (90)  >  Stagger (80)  >  Attack/Block/Parry (60)
            >  Dodge (50)  >  Traversal (40)  >  Land (30)  >  Locomotion/Idle (10)
```

**I confirm this matches the TD-required ordering exactly.** The three named priorities are at
100/90/80 and in the required order. I also confirm A1's §4.4 preserves the **seven exit paths
E1–E7** and states "C-04 adds no new state and removes none".

The request asks me to "preserve" the precedence. **I preserve it by requiring that no data I
author can produce a forced state.** My only influence is the `StaggerClass` my attacks carry
(§6.5) and the posture damage value; neither can set a control state. There is no Agent 2
mechanism in this contract that could violate the precedence.

### 6.3 What Agent 2 consumes, and what I will not do

| Agent 2 action | Permitted? |
|---|---|
| Set the stagger class on my own attacks | **Yes** — authored data, A1 classifies |
| Set posture damage on my own attacks | **Yes** |
| Consume `FTDDCombatStateChangedEvent` / `FTDDPostureBrokenEvent` | **Yes** |
| Call `ApplyStagger` on the player | **No — A1 only** |
| Force `Stagger` / `Dead` / `Cinematic` | **No — A1 only** |
| Classify a hit against the player | **No — A1 only** |

I accept `A1-R1` §4.1's mutation-authority statement without change. This matches my own
proposal's §7 exactly.

### 6.4 Recovery from stagger — I require it, and here is the precise reason

The request asks: *"State whether you require a recovery-from-stagger event and why."*

**I require it.** `A1-R1` does not contain one. `TDD-INT-RECON-001` v2.0 D-09 records this as an
unresolved dependency and notes any such event "cannot become an independent state authority".
I accept that constraint.

**The requirement, stated as a consumer use case rather than a preference:**

`CH01-BOS-001` phase 2 runs a punish-then-reposition cycle. The boss commits to a punish that
takes 0.8 s, then repositions. If stagger ends at 0.6 s, the boss is committed to 0.2 s of
punish into a player who has recovered — **an unfair hit that the player cannot avoid and did
not misplay.** The only ways I can avoid it today:

| Option | Why it fails |
|---|---|
| Poll `bIsStaggered` each frame | I can see it *is* false, but not *when it became* false — a transition between ticks is indistinguishable from a transition on the tick. At the moment I poll, I may already be committed |
| Read `StaggerRemainingSeconds` | Same problem: the value is a projection at publish time, and my decision commits before the next publish |
| Author every punish shorter than minimum stagger duration | Constrains content to work around an API gap, and fails the moment stagger duration is tuned |

**So the requirement:** an **authoritative transition notification** carrying, at minimum,
`{ EntityId, FromState, ToState, GameplayTimeSeconds, FrameCounter }`, emitted by A1 when the
player leaves `Stagger`. With it, the boss can abort a reposition commitment on the edge.

**What it must not be:** a second source of truth. I accept the request's constraint verbatim —
it must **report** a transition A1 already performed, not create or permit one. My consumption
is read-only and has no write path.

**Design notes for A1 to accept or reject (A2R-10):**

- It can be the **existing** `FTDDCombatStateChangedEvent` with recovery represented as a normal
  transition out of `Stagger`, in which case **no new type is needed** and my requirement is
  satisfied by A1 confirming that event fires on recovery. **This is my preferred resolution
  because it adds no contract surface.**
- If a dedicated event is preferred, it must be derived from the same commit point so the two
  can never disagree.
- It must fire on **every** exit from `Stagger`: timeout, lethal interruption, cinematic
  takeover, and forced supersession. A recovery event that only fires on timeout would leave
  the other three paths silent, which is the same bug in three places.

**I am not asking for a new state, a new authority, or a write path.** If the answer is "the
existing combat-state-changed event already covers this", C-04's recovery item closes
immediately.

### 6.5 Classification representation — I state my position on TD-02 without deciding it

`A1-R1` §4.2 offers four alternatives and recommends **B** (`ETDDStaggerClass`). The request
asks me to address the options. TD-02 says the representation is TD's; I state a position and
leave the decision.

| Option | My position as the content author | Reason |
|---|---|---|
| **A** `bool bCausesStagger` | **Acceptable fallback** | My Chapter 1 attacks need exactly two classes (`Never`, `Always`), so A is sufficient for the slice. It is a real loss: `OnPostureBreak` cannot be expressed |
| **B** `ETDDStaggerClass` enum | **Preferred** | `OnPostureBreak` is a real Chapter 1 case: the Great Root Mother's slam staggers **only** if it breaks posture; otherwise it is a heavy hit that does not. Expressing that today needs `Always` + a design lie, or `Never` + a missed punish. B expresses it with one enum value |
| **C** damage-tag → data-table mapping | **Reject** | I would be authoring gameplay rules as tag names. A tag rename silently changes whether an attack staggers, and my validator cannot detect it. A1's §4.2 says "rules live in naming conventions, which is where such rules rot" — I agree |
| **D** GAS status tag on the victim | **Reject** | A1's reason is decisive and it is a **my-side** reason: classification after application inverts the order my authored data depends on (classify → fallback → restore → enter). It also makes my attack data depend on GAS activation timing |

**My position: B, with A acceptable.** Same as A1's recommendation, arrived at from the content
side. **This is convergence, not agreement** — I have not approved a version containing B, and
TD-02 is unresolved.

One addition to A1's §4.2 analysis: whichever is chosen, **my authoring validator must be able
to enumerate the class per attack offline**. Under A or B that is trivial; under C it requires
the whole tag taxonomy; under D it requires GAS. That is a fourth argument against C and D that
neither A1 nor I had stated.

### 6.6 Two stagger behaviours I want pinned

Not disagreements — behaviours A1's §4.7 handles but does not test, and that I depend on:

| Behaviour | A1's §4.7 says | I want a test |
|---|---|---|
| Two staggers in one frame: one applied, second superseded, **no duration refresh** | correct | A1 §4.8 case 14 covers it — **accepted, no addition needed** |
| Stagger during terminal hold: `bPendingGroundingRecovery`, landing recovery on grounding | correct (M1 v1.4 §3.2.2b) | A1 §4.8 does **not** cover it. **Addition proposed** §6.7 |

### 6.7 Tests I accept, plus two additions

`A1-R1` §4.8's fourteen cases: **all accepted.** Cases 1, 2 and 8 (precedence pairs and the
three-way) are the precedence guard the request requires. Case 12 (representation swapped
A↔B↔C producing an identical outcome matrix) is a genuinely good test — it makes TD-02's
choice safe to defer.

**Two additions I require:**

| Proposed addition | Asserts |
|---|---|
| `TDD-Contract.World.StaggerRecoveryNotificationFiresOnEveryExit` | A recovery notification fires on all four exit paths (timeout, lethal, cinematic, supersession), exactly once each, and carries an authoritative `GameplayTimeSeconds` from A1's clock |
| `TDD-Contract.World.StaggerDuringTerminalHoldReachesGroundedRecovery` | Stagger applied while `HoldUnsupported` resolves to grounded recovery on the landing frame; no state is applied mid-air that contradicts the hold |

### 6.8 C-04 — what a revised version must contain for my approval

1. **Recovery notification** confirmed, preferably as an existing `FTDDCombatStateChangedEvent` transition (A2R-10).
2. TD-02 decided (B preferred, A acceptable).
3. The two test additions accepted or countered.

**Precedence, health independence, M1 preservation and the fourteen tests need no revision.**

---

## 7. C-05 — Telegraph

**A1 proposal reviewed:** `A1-R1` §5.1–§5.10, exact version v1.0.
**Verdict: AGREE IN PRINCIPLE — NOT AGREED.**

### 7.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §5.2 | Four messages, exactly-once guarantees | **ACCEPT** |
| §5.3 | Gameplay-seconds clock, scaled by custom time dilation | **ACCEPT — correct** |
| §5.3 | Half-open windows `[WindupEnd, ActiveEnd)` | **ACCEPT with one worked example** §7.4 |
| §5.3 | "Do not evaluate parry by timestamp subtraction" | **ACCEPT — important** |
| §5.3 | Ordering across attacks, guid tiebreak | **ACCEPT** |
| §5.4 | Telegraph ≠ damage | **ACCEPT — I will comply** |
| §5.5 | Pause / dilation / unload / late subscribe / missed window | **ACCEPT with one gap** §7.5 |
| §5.6 | Five concrete producer requirements | **ACCEPT — all five, mine to meet** |
| §5.7 | Defence cancellation | **ACCEPT** |
| §5.8 | Twelve acceptance cases | **ACCEPT with additions** §7.7 |

### 7.2 The producer/consumer split — A1's clause is right and I accept the harder half

`A1-R1` §5.1: **Agent 2 produces enemy telegraphs; Agent 1 produces the player's and consumes
the enemy's.** The request calls me the producer in this contract, and `A1-R1` §5.9 item 1 asks
for my agreement to the four-message lifecycle.

**I agree to the four-message lifecycle.** `Opened` / `PhaseChanged` / `Closed`, plus an
optional `GetActiveTelegraphs` query for late subscribers. Accepting it means accepting five
obligations, and I accept all five (A1's §5.6, restated from my side):

| A1 requirement (§5.6) | My commitment |
|---|---|
| 1. Open **before** the windup begins; ≥ 0-frame lead, target ≤ 1 frame | My telegraph opens on the notify at the start of the windup section, not in `BeginPlay` and not on a timer |
| 2. `PhaseChanged` on the frame the phase changes, not on a timer | Notify-driven, not accumulate-and-compare |
| 3. Close exactly once on completion, interruption, death or unload | One close path, guarded by an id retirement set |
| 4. Never send a telegraph for an attack that cannot execute | No `Opened` until the window is actually open and the attack has not been cancelled |
| 5. Do not encode damage numbers in the telegraph | No damage field. I have no need for one and A1's §5.8 case 12 asserts both differ |

### 7.3 Gameplay clock ownership

`A1-R1` §5.3 recommends a Core `UTDDGameplayTimeSubsystem`, Agent 3 owned, and raises TD-06.
`A1-R1` §5.3 also states the definition precisely: accumulated world delta **scaled by the
actor's custom time dilation**, so hitstop and slow-motion stretch windows as the animation
stretches; world pause stops the clock.

**I agree with the definition and with Core ownership.** From the producer side, the reason is
concrete: if I maintain a per-actor accumulator and A1 maintains another, a pair hitstop applied
to both of us will produce two accumulations of the same scaled delta, and they will differ by
a frame at the next boundary. The parry is then evaluated against the wrong phase — a bug that
appears only under hitstop and will be blamed on the parry code.

**TD-06 remains open and I do not decide it.** My requirement, stated as a boundary: whatever
the clock is, **both agents must read the same one**, and it must be queryable without an actor
pointer (a world subsystem, not a component), because my telegraph producer runs on actors that
may stream.

### 7.4 The half-open window — I accept it and want one worked example in the contract

`A1-R1` §5.3: `Active = [WindupEnd, ActiveEnd)`. A hit at exactly `WindupEnd` is active; at
exactly `ActiveEnd` it is not. §5.8 case 1 asserts both boundaries.

**I accept the convention** — half-open is the only convention that makes adjacent windows
non-overlapping and total.

**One addition, because a boundary convention without a worked timeline is how off-by-one-frame
bugs survive review:** a single shared timeline table in the contract showing one attack with
pause, hitstop, a parry at each edge, and a cancellation. `TDD-INT-RECON-001` v2.0 §3 (C-05)
asks for exactly this ("prepare a shared timeline example"). Here is mine, and it is the
artifact A1 should accept, correct, or replace:

| t (gameplay s) | Event | Clock state | Note |
|---|---|---|---|
| 0.000 | `Opened`; window `[0.40, 0.60)`, recovery ends 0.90 | running | open at windup start |
| 0.150 | **world pause** | **stopped** | nothing advances |
| 0.150 | **unpause** | running | 5 s of wall time consumed no gameplay time |
| 0.250 | **hitstop 100 ms** on the pair | **scaled** | both timestamps and montage scale together |
| 0.400 | `PhaseChanged(Active)` | running | **inclusive lower bound** |
| 0.400 | parry input, same frame | — | parry **succeeds**: overlap at `WindupEnd` |
| 0.599 | parry input | — | parry **succeeds**: inside `(WindupEnd, ActiveEnd)` |
| 0.600 | `PhaseChanged(Recovery)` | running | **exclusive upper bound** |
| 0.600 | parry input, same frame | — | parry **fails**; `ActiveEnd` is not active |
| 0.700 | **cancelled** (source staggered) | running | `Closed(Cancelled)`; **buffered defence retained** |
| 0.700 | no hit resolves | — | instance void |

The three assertions I care most about are the two at 0.400/0.600 and the retained buffer at
0.700. **If A1's reading differs at any row, that row is the contract.**

### 7.5 Pause, dilation, hitstop, and one gap

| Situation | A1's rule | My compliance |
|---|---|---|
| World pause | clock stops; no messages; remaining duration preserved | I do not emit on pause; my montage is paused by the same mechanism |
| Pair hitstop | both timestamps and montage advance on the scaled clock | I read the clock; I do not accumulate my own |
| Time dilation (slow-mo) | scaled | same |
| World unload | force-close every open telegraph with `SourceUnloaded` **before** teardown | accepted — see the gap below |
| Late subscriber | no history; query once if the surface exists | I produce the query surface if TD chooses it (TD-06/§5.10 item 2) |
| Missed window | rejected by broker; log once | broker is Agent 3's |

**The gap — §5.5's last resort is on the wrong side.** `A1-R1` §5.5 says: "If a telegraph is
never closed, A1's defence must still time out via its own montage and must not latch."

That is correct and defensive, and I accept it as A1's requirement. But it leaves **the
producer's obligation** stated only as "close before teardown", with no test that I actually
did. A force-close that silently fails is indistinguishable from one that ran, and the failure
mode is a defence that latches.

**Addition proposed, A2R-11:** the broker counts open instances per source entity and asserts
zero after teardown. If a source unloads with a live instance, that is an **Error in
development** attributed to the producer, not a silent recovery. The recovery stays — I am not
removing A1's belt — but the failure must be visible to me so I can fix the close path.

### 7.6 Cancellation, interruption, death, unload — the matrix

The request lists five lifecycle terms; `A1-R1` §5.5 and §5.8 between them cover all. My
reading, for A1 to confirm:

| Event | Message | Defence consequence | Consumer consequence (mine) |
|---|---|---|---|
| Completed | `Closed(Completed)` | defence evaluated normally | instance retired; id never reused |
| Cancelled before `Active` | `Closed(Cancelled)` | **buffered parry retained**, expires naturally | attack void; montage aborted |
| Interrupted during `Active` | `Closed(Interrupted)` | hit resolution for that instance void | no damage; next attack is a new instance |
| Source died | `Closed(SourceDied)` | defence cleared for that source's instances | instance retired |
| Source unloaded | `Closed(SourceUnloaded)` | defence must not latch | §7.5 gap |
| Superseded | `Closed(Superseded)` | prior instance void | new instance has a new `AttackInstanceId` |

**The row that matters most is "Cancelled before `Active` → buffered parry retained."** A1's
§5.8 case 6 asserts it and A1's rationale is exactly right: "This prevents punishing the player
for an attack that never happened." I accept it and it constrains my producer: I must not
open a telegraph for an attack I might cancel before `Active` unless I also send the close,
which is A1's §5.6 item 4.

### 7.7 Tests I accept, plus two additions

`A1-R1` §5.8's twelve cases: **all accepted.** Cases 1 (boundaries), 6 (cancelled before
active, buffer retained), 10 (unload closes all three) and 12 (telegraph damage ignored) are the
four that make the contract meaningful.

**Two additions:**

| Proposed addition | Asserts |
|---|---|
| `TDD-Contract.World.TelegraphProducerClosesOnEveryTerminalPath` | For each of completed / cancelled / interrupted / source-died / unload, exactly one `Closed` is emitted with the right `Reason`, and no message follows it |
| `TDD-Contract.World.TelegraphOpenPrecedesWindupByAtLeastOneFrame` | `Opened.GameplayTime` ≤ windup start, and the player could observe it for ≥ 1 frame before `Active` |

Both are producer-side obligations (mine) from A1's §5.6 items 1 and 3. **They test me, not A1**,
which is why I am proposing them rather than asking for them.

### 7.8 C-05 — what a revised version must contain for my approval

1. The shared timeline (§7.4) accepted, corrected, or replaced — with the three edge rows agreeing.
2. TD-06 ruled, or both agents stating the same clock requirement in the same version.
3. `A2R-11` (open-instance assertion on teardown) accepted or countered.
4. TD's decision on late-subscriber query (§5.10 item 2).

**The four-message lifecycle, the half-open convention, the "telegraph ≠ damage" rule and all
twelve tests need no revision.**

---

## 8. C-06 — Interaction

**A1 proposal reviewed:** `A1-R1` §6.1–§6.9, exact version v1.0.
**Verdict: DISAGREE.**

This is the only outright disagreement in the review, and it is specific rather than general. I
accept most of `A1-R1` §6. The disagreement is with **one clause — §6.2/§6.4's per-frame
`TickInteract(Progress01)`** — and with the ownership model that clause implies.

### 8.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §6.2 | Extended interface with `EndResult` + `CancelReason` | **ACCEPT** — the extension is right |
| §6.3 | Focus selection, scoring, hysteresis | **ACCEPT** |
| §6.3 | Ineligible candidates show **no prompt** | **ACCEPT** |
| §6.4 | Router owns hold duration and progress | **PARTIALLY — see §8.4** |
| §6.4 | `TickInteract(Progress01)` per frame while held | **REJECT** §8.4 |
| §6.5 | Eight cancellation triggers and ordering | **ACCEPT** |
| §6.5 | Exactly-once session state machine, `ProtocolViolation` | **ACCEPT** |
| §6.6 | Router does not grant progression | **ACCEPT — required** |
| §6.7 | Fourteen acceptance cases | **ACCEPT with revisions** §8.7 |

### 8.2 The responsibilities, resolved

The request asks me to resolve player-router vs world-interactable responsibilities. They
resolve cleanly, and A1's §6.1 and §6.6 already have the right split:

| Responsibility | Owner | Why |
|---|---|---|
| Focus detection, cone, LOS | **Agent 1 (router)** | Player-side input and camera; A2 has no camera |
| Input mapping (tap/hold) | **Agent 1 (router)** | Input is player state |
| Eligibility *requirements* (authored conditions) | **Agent 2 (interactable)** | A2 authors what the interactable needs |
| Eligibility *player-state gate* (Cinematic/Dead) | **Agent 1 (router)** | Player state is A1's |
| Prompt text and verb | **Agent 2 (interactable)**, from a String Table | Content is A2's |
| Hold **duration** | **Agent 2** (authored on the interactable) | A2 authors the design |
| Hold **progress integration** | **Agent 1 (router)** | Frame-accurate, cancellable (§8.4) |
| Session state, exactly-once terminal | **Agent 1 (router)** | A1 §6.5's state machine |
| World actor state during interaction | **Agent 2 (interactable)** | Its own state |
| Completion **result** | **Agent 1 reports**, Agent 2 acts | A1 §6.2's `EndResult` |
| **Progression / reward grant** | **Neither router nor interactable** | §8.3 |

### 8.3 Progression authority — I agree with A1 and add a constraint on myself

`A1-R1` §6.6: the router "does not grant memory fragments, quest steps, items or checkpoints.
Completion is reported; the interactable or its owning subsystem performs the grant (A2/A3)."

**I accept this, and the request's own rule — "Do not allow an interactable to grant progression
merely because it was interacted with" — constrains me more than it constrains A1.** So I state
my own boundary explicitly:

| Agent 2 will | Agent 2 will not |
|---|---|
| Report completion as a fact, once, with `InteractionId` | Grant a memory fragment on `BeginInteract` |
| Have its **owning subsystem** evaluate whether the grant condition is met | Grant on `EndInteract(Completed)` alone without evaluating its condition |
| Treat a repeated completion as idempotent | Grant twice if the player interacts again |

**The "merely because it was interacted with" failure is a real one in my data.** The
`CH01-SUB-018 The Wayside Offering Place` memory fragment and the `CH01-SUB-001` shrine both
read as "interact to receive". If the interactable grants on `Completed` without checking
whether this completion is the one its condition describes, a player who interacts twice gets
two grants or a duplicate flag. **The grant belongs to the owning subsystem keyed on
`InteractionId`, evaluated on the completion fact, idempotent.** That is my obligation and I
accept it.

**Consequence for the contract:** the completion fact must carry `InteractionId` — a stable
authored id — or my subsystem cannot key the grant. That is a C-07 dependency (§10).

### 8.4 The disagreement — `TickInteract(Progress01)` per frame is the wrong shape

**A1's clause (§6.2, §6.4):**

```cpp
virtual void TickInteract(const FTDDInteractionContext&, float Progress01) = 0;
```

with §6.4 proposing "the router owns hold duration and progress" and "`Tick(progress)` each frame
while input held".

**Why I reject it.** Three reasons, in order of severity.

**1. It makes the interactable's behaviour depend on a frame rate it does not control.**
`Progress01` arrives once per frame. An interactable that plays a 1.5 s reading animation, an
opening door, or a gradually-lit shrine must map `Progress01` onto its own animation. At 60 FPS
it gets 90 updates; at 30 FPS, 45; at a hitch, fewer. If any interactable uses `Progress01` to
drive a stateful animation, **two machines produce visibly different animation** — and the
contract has no rule that prevents it. A1's §6.4 says the interactable "decides only what to do
with it (open a door gradually, play a reading animation)", which is precisely the case that
breaks.

**2. `Progress01` is a projection, so the interactable cannot answer "when did it complete".**
The interactable receives a float and must infer completion from `Progress01 >= 1.0`. A1's §6.4
allows "±1 frame" for completion. So the interactable's own animation finishes up to one frame
after `End(Completed)` arrived, or — worse — the interactable sees `Progress01 == 0.983` on the
last tick and `End(Completed)` on the next frame with no `1.0` tick. A1's §6.7 case 4
acknowledges this ("exactly one `Tick(1.0)` **or none**"). **An interactable that must react to
completion cannot rely on ever seeing `1.0`.**

**3. It conflates two things A1's own design keeps separate: the hold timer and the
interactable's presentation.** A1's §6.4 rationale for router-owned progress is sound —
frame-accurate, cancellable, one damping curve. But owning the **timer** and owning the
**presentation clock** are different. The router should own the timer. The interactable should
own its own presentation, driven by its own montage, which is exactly how every other A1/A2
boundary in this contract works.

**My counter-proposal, `PROPOSED — NOT FROZEN` (A2R-12):** replace per-frame `TickInteract` with
a **progress notification on change only**, plus an explicit completion callback.

```cpp
// PROPOSED — NOT FROZEN. Counter-proposal to A1-R1 section 6.2.
virtual void OnInteractProgressChanged(
    const FTDDInteractionContext&, float Progress01) = 0;   // throttled: quantised, not per-frame
virtual void BeginInteract(const FTDDInteractionContext&) = 0;
virtual void EndInteract(const FTDDInteractionContext&, ETDDInteractionEndResult) = 0;
virtual void CancelInteract(const FTDDInteractionContext&, ETDDInteractionCancelReason) = 0;
```

with the router's obligation stated as:

| Property | Rule | Why |
|---|---|---|
| Throttle | `OnInteractProgressChanged` fires at **≤ 10 Hz** and on every 10 % band crossing, not per frame | Presentation does not need frame precision; the timer does |
| Guaranteed terminal | `EndInteract(Completed)` is **always** called, and is the only signal an interactable may treat as completion | Removes the "`Tick(1.0)` or none" ambiguity in A1's §6.7 case 4 |
| Monotonic | Progress never decreases within a session | A restart is a new session with a new `Begin` |
| Cancellation | `CancelInteract` and `EndInteract` are mutually exclusive and exactly one occurs | A1's §6.5 state machine already guarantees it |

**What this costs A1:** one less call per frame per active session (a saving, not a cost), and
the loss of an unthrottled progress stream that no interactable should have used anyway.

**What it costs me:** I must drive my own presentation from my own montage, which is what I
already do for every other timed behaviour.

**The one case that keeps A1's shape viable:** if an interactable genuinely needs frame-accurate
sub-progress — a chase, a balance beam — then that is not an interactable; it is a mini-game with
its own contract. **I have no such case in Chapter 1.** If A1 does, that is evidence for keeping
`TickInteract` and I would withdraw this counter-proposal.

**This is a disagreement I am willing to lose.** It is a design argument about a shape, not a
correctness claim, and I have stated what would change my mind.

### 8.5 Tap versus hold — accepted, with the ordering rule pinned

`A1-R1` §6.4's tap/hold rules are correct and I accept them:

| Input | A1's rule | Accept |
|---|---|---|
| `HoldDurationSeconds == 0` | completes on press; `Begin` and `End(Completed)` may be same frame, not same call stack without a `Tick(1.0)` | **Accept.** My counter-proposal changes the middle step, not the endpoints |
| `> 0` | `Begin` on press; progress while held; `End(Completed)` at `progress >= 1.0` ±1 frame | **Accept**, with progress delivered per §8.4 |
| Release before completion | `Cancel(Released)`; **no completion, no grant** | **Accept** — and this is the grant-safety rule. No completion fact, no grant |
| Focus lost | `Cancel(FocusLost)` at the frame focus changes | **Accept** |
| Out of range mid-hold | `Cancel(OutOfRange)` **before** the movement is committed | **Accept** — the ordering is the important half |

**Authoring intent, for A1 to know:** Chapter 1 uses tap for barriers and dialogue-adjacent
prompts, and hold for the shrine offering and the wayside offering. **I am not stating
durations** — they are not authored and I will not invent them.

### 8.6 Damage interruption, forced-state interruption, stream-out, exactly-once

| Trigger (request) | A1's §6.5 rule | My position |
|---|---|---|
| **Damage interruption** | `Cancel(Damaged)` after the attribute commit, before abort/state resolution | **ACCEPT, and this closes my open question.** `TDD-INT-RECON-001` D-07 records me as marking damage-interrupts-hold "explicitly undecided". I now **agree that damage interrupts an active hold**, and A1's ordering — after health commit, before state resolution — is the correct one because my interactable must not still be ticking when a state change is about to run |
| **Forced-state interruption** | `Cancel(Staggered)` before `Stagger` entered; `Cancel(Died)` before `Dead`; `Cancel(Cinematic)` before freeze and camera | **ACCEPT.** The ordering is the contract. A cancel arriving after the state change would leave my actor ticking in a state it cannot observe |
| **Stream-out / destruction** | `Cancel(TargetUnloaded)` on the frame the weak pointer invalidates or unregistration arrives | **ACCEPT.** My obligation is to unregister cleanly on stream-out; A1's is not to hold a session against an invalid pointer |
| **Level transition** | `Cancel(LevelTransition)` before teardown, exactly once, no dangling session | **ACCEPT** |
| **Exactly-once terminal** | `Idle → Begun → Terminal`; refuse `End`/`Cancel` from `Idle` or after `Terminal`; log `Interaction.ProtocolViolation` | **ACCEPT.** I must tolerate `Cancel` in the same frame as `Begin` (a tap then a stagger), which A1's §6.5 already requires |

**On the D-07 "material unreviewed divergence": it is now reviewed and resolved from my side.**
Damage interrupts. I withdraw "explicitly undecided."

### 8.7 Tests

`A1-R1` §6.7's fourteen cases: **twelve accepted, two require revision** under my §8.4
counter-proposal.

| A1 case | My position |
|---|---|
| 4 (tap: exactly one Begin, one `Tick(1.0)` **or none**, one End, grant 1) | **Revise** — the "or none" is the ambiguity §8.4 removes. Under my counter-proposal: exactly one `Begin`, one `End(Completed)`, grant 1 |
| 5 (hold 1.5 s: `Tick` once per frame, completion ±1 frame) | **Revise** — `Tick` per frame becomes progress notifications at ≤10 Hz **plus** one `End(Completed)` |
| 6 (release at 0.75: one `Cancel(Released)`, zero `End`, grant 0) | **Accept unchanged** — the grant rule is the point |
| 7, 8, 9, 10 (cancel orderings) | **Accept unchanged** |
| 11, 12 (protocol violations) | **Accept unchanged** |
| 13 (unregistered verb tag) | **Accept** — but note it is a **my-data** failure and should also fail my L0 authoring gate |
| 14 (level transition) | **Accept unchanged** |

**One addition I require:**

| Proposed addition | Asserts |
|---|---|
| `TDD-Contract.World.InteractableGrantsOnlyOnCompletionFactOnce` | For each Grant-capable interactable: two attention attempts produce exactly one grant; a `Cancel` at 0.99 progress produces zero; the grant is keyed on `InteractionId` and is idempotent |

This is my §8.3 obligation made testable.

### 8.8 C-06 — what a revised version must contain for my approval

1. Progress delivery resolved — either my §8.4 counter-proposal, or A1 states a named
   Chapter-1 interactable that requires per-frame sub-progress (in which case I withdraw).
2. `End(Completed)` guaranteed as the only completion signal.
3. Completion fact carries `InteractionId` (C-07 dependency).

**Everything else in §6 I accept**, including the interface extension, focus selection, all
eight cancellation triggers and the fourteen-case structure.

---

## 9. C-07 — IDs and tags

**A1 proposal reviewed:** `A1-R1` §7.1–§7.8, exact version v1.0.
**Verdict: REQUIRE CLARIFICATION.**

### 9.1 A1's exact clauses reviewed

| Clause | Subject | Verdict |
|---|---|---|
| §7.2 | Three identity classes (runtime / authored / canon) | **ACCEPT — the right taxonomy** |
| §7.2 | `EntityId` not persisted; re-issued per session | **ACCEPT** |
| §7.2 | Player keeps one `EntityId` across death/respawn | **ACCEPT** |
| §7.2 | All-zeros `FGuid` invalid | **ACCEPT** |
| §7.3 | Tag inventory, existing vs requested | **ACCEPT with 3 clarifications** §9.5 |
| §7.4 | Persistence rules | **ACCEPT with evidence** §9.3 |
| §7.5 | Invalid/unknown/retired handling | **REQUIRE CLARIFICATION** on `Retired` §10.4 |
| §7.6 | Nine acceptance cases | **ACCEPT with one revision** §9.7 |
| §7.8 | Unresolved alternatives | **ACCEPT analysis** |

### 9.2 Separation of runtime, authored, route and interactable IDs — I accept and extend

`A1-R1` §7.2 distinguishes **runtime entity** / **authored content** / **canon place**. The
request requires me to address runtime, authored, **route** and **interactable** identities. A1's
three classes do not separate route from interactable, because both are "authored content". That
separation matters to me, so I add it explicitly:

| Class | Type | Example | Lifetime | Who assigns | Persisted? | Parsed by code? |
|---|---|---|---|---|---|---|
| **Runtime entity** | `FGuid` | player, enemy instance | entity lifetime only | whoever spawns | **No** | No — opaque |
| **Authored content** (attacks) | `FName` | `ATK.Ada.Heavy.01` | content lifetime | A1 content | No (unless referenced) | validator only |
| **Authored content** (routes) | `FName` | `CH01-TRV-002/ROUTE-A` | content lifetime | **A2** | **No evidence of a reference** §9.3 | validator only |
| **Authored content** (interactables) | **unresolved** §10.3 | — | — | A2 | **depends on save** | validator only |
| **Canon place** | `FName` | `CH01`, `CH01-SCN-014` | permanent | canon register | yes | canon layer only |

**The two that need actual decisions are routes and interactables**, and I address each with the
evidence the request demands rather than a preference.

### 9.3 Route identity — persistence requirement, answered with evidence

The request: *"Provide actual persistence and consumer requirements before recommending stable
IDs."*

**Actual consumers of `RouteId` that I have:**

| Consumer | Needs `RouteId`? | Persist across save? |
|---|---|---|
| A1's dedupe/log correlation (A1 §1.5) | Yes | No |
| My authoring validator (duplicate detection, reachability) | Yes | No |
| My streaming registration / unregistration | Yes | No |
| Memory fragments referencing a route | **No** — memory fragments are keyed on scene/memory index | — |
| Chapter flow / checkpoints | **No** — keyed on scene flags | — |
| Save state | **No route reference exists in any Chapter 1 save content** | — |

**Therefore: `RouteId` has no persistence requirement in Chapter 1.** Consequences I accept:

1. Routes may be **renamed freely** between builds; no migration.
2. Retirement policy for routes reduces to **duplicate detection + format validation**, not
   tombstoning.
3. **This is evidence, not a decision** — TD-04 remains open, and if narrative content later
   references a route, this answer changes and I will re-submit it.

**A1's §7.4 already anticipates this**: "Route id persistence: depends on TD-04: if narrative or
checkpoints reference routes, they must be retirement-governed; if not, they may be freely
renamed." My evidence says "not". That is the answer to A1's §1.8 dependency 3.

### 9.4 `Retired` status — I cannot implement it from data I do not have

**A1's clause (§7.5):**

> "Retired authored id at runtime → Explicit `Retired` resolution status; the referencing feature
> is disabled with a diagnostic, **never** rebound."

And §7.4:

> "A save referencing a retired id must fail **loudly** with a named error, never silently rebind
> to a similarly-named id."

**I agree with the principle completely.** Silently rebinding a retired id to a similar one is
the worst failure mode available, and A1's §7.4 calls it "the single most important policy in
C-07" — correct.

**The clarification I need is mechanical, and it is not about policy:** *where does the list of
retired ids live, and who maintains it?*

| Requirement for a `Retired` status to work | Exists today? |
|---|---|
| A registry of retired ids, per id family | **No** |
| Something to resolve a retired id **against** (a tombstone record) | **No** |
| An owner for adding to the tombstone list | **No** (TD-08 proposes Agent 3) |
| A format for the tombstone (id → reason → date → replacement?) | **No** |

**A1's §7.5 table can be implemented only if the tombstone record exists.** Without it, the
conversation is about a behaviour I cannot build: my validator cannot return `Retired` for an id
that appears in no list, and the honest outcome is `Unknown`, which A1's table treats
differently.

**Proposed resolution, for TD-08 (A2R-13):**

| Component | Proposed owner | Minimum content |
|---|---|---|
| `FTDDRetiredIdRecord` | **Agent 3 `TDDCore`** | `FName Id`, `FName Family`, `FString Reason`, `FString ReplacedBy` (empty = none), `FDateTime RetiredUtc` |
| Tombstone data file | **Agent 2** authors the content-id entries; Agent 3 owns the file | one row per retired id, machine-readable |
| Resolution | **Agent 3** provides `ETDDIdResolution { Valid, Unknown, Retired }` | `Retired` only from the tombstone; `Unknown` otherwise |
| Enforcement | validator **Error** on a reference to a `Retired` id | build-blocking |

**Until the tombstone exists, I cannot claim support for `Retired`**, and I will not say that I
do. That is the whole clarification.

### 9.5 Tag ownership, approval, retirement, non-reuse

The request requires me to address these four. A1's §7.3 supplies the inventory; the governance
is TD-08's. My position on each:

| Concern | My position |
|---|---|
| **Ownership** | **Agent 3 owns the registry.** Neither A1 nor A2 registers a tag. A1's §7.1 says exactly this and I agree. My tags in the inventory below are *requests*, not grants |
| **Approval** | Approval is a **TD-08 action**, one namespace at a time, with a stated owner and a stated consumer per tag. A1's §7.3 table is the right form — it names producer and consumer per row |
| **Retirement** | **Tombstone, never delete.** Same reasoning as ids, and same blocker: the tombstone record does not exist (A2R-13). A deleted tag silently changes behaviour; a tombstoned tag fails loudly |
| **Non-reuse** | **Absolute.** A retired tag name is never re-issued for a different meaning. This costs nothing and prevents a class of silent regression that no test can catch, because the test would be rewritten to match |

**Three clarifications on A1's §7.3 inventory** (these are REQUIRE CLARIFICATION items, not
disagreements):

| Tag(s) | My question |
|---|---|
| `Traversal.Capability.*` (5) | **A2R-14:** A1's §7.3 lists these as "Requested" with **A2 as producer** and A1 as consumer. But §1.2 calls them "the authored requirement" and §1.3 puts them in the *player's granted set* (`CapabilityTags`). **Who grants a capability?** If the player's granted set is A1's, then A1 is the producer of the grant and I am the producer of the *requirement* — two different producers of one tag. I need this stated once, or my validator will check the wrong thing |
| `Status.Interacting`, `Status.Traversing`, `Status.Airborne`, `Status.LockedOn` (4) | **A2R-15:** A1's §7.8 item 4 says these can be dropped if A2 only reads C-02. **I do read C-02.** `ControlState` gives me `Interaction` and `Traversal` as enum values, and `Locomotion.MovementMode` gives me airborne. **My position: I do not need these four tags.** If they exist I will use them for AI conditions because they are cheaper than an interface call, but I am not requesting them and their absence costs me nothing |
| `Interact.Verb.*` (7) | **ACCEPT as requested.** But A1's §7.3 lists "A2 prompt data" as producer and "A1 router, UI" as consumer. If my interactables choose the verb, **I am choosing from a closed set A1's router must understand** (icon + animation mapping). A verb outside that set is a runtime error, which A1's §6.7 case 13 covers. **I need the closed set to be registry-validated, not convention** |

### 9.6 Interactable identity — unresolved, with the evidence that would resolve it

The request: *"Do not invent an interactable count or assume a persistence requirement without
evidence."* I will not. Here is what is actually known:

| Question | Answer | Evidence |
|---|---|---|
| How many interactables exist in Chapter 1? | **Not established.** No source enumerates interactables | `A2-C01…C07-1.0` §9.2; withdrawn count; no register section lists interactables |
| Do any save references point at an interactable? | **Unknown.** No save schema exists; no save content exists | no save system implemented, none designed in this scope |
| Does any interactable need identity beyond its actor lifetime? | **Unknown**, and it depends on the previous row | — |
| Do any interactables have persistent state (a shrine that stays lit)? | **Plausibly yes**, but not evidenced in a source I can cite | `CH01-SUB-001 The Abandoned Shrine` is `PENDING APPROVAL`; no design states its persistence |

**So I cannot recommend a namespace, and I will not.** My `A2-C01…C07-1.0` §9.2 gave three
options (scene-derived key / new `CH0n-ACT-nnn` family / transient actor name). `A1-R1` §7.3 and
§7.7 item 1 ask for my inventory, which is the correct next step and is **blocked on a save
requirement that does not yet exist**.

**What would resolve it, concretely (A2R-16):** a statement from TD of whether the vertical slice
persists interactable state across a level transition and across a save. If **no** persistence:
interactables need only an actor-scoped runtime id plus an authored key for diagnostics, and the
question collapses. If **yes**: a stable authored id is required and it must be tombstone-governed
like any other.

**This is the one place in the whole review where my answer is "I cannot answer yet", and I am
leaving it that way rather than inventing a namespace.** The request explicitly forbids the
alternative.

### 9.7 Tests

`A1-R1` §7.6's nine cases: **eight accepted, one revised.**

| A1 case | My position |
|---|---|
| 1 (data-driven completeness over §7.3) | **Accept** — and it must fail with the **tag name**, which A1 specifies |
| 2 (double registration rejected) | **Accept** |
| 3 (unknown tag: invalid handle, one Warning, no crash) | **Accept** |
| 4 (retired id returns `Retired`, not a substitute) | **Revise** — cannot run without the tombstone (A2R-13). Until then this test asserts a behaviour with no data source |
| 5 (two markers, one `RouteId`) | **Accept** |
| 6 (event after both actors destroyed) | **Accept** |
| 7 (empty `FGuid` rejected) | **Accept** |
| 8 (death → respawn, same `EntityId`) | **Accept** |
| 9 (authored id format violation: editor Error, runtime no crash) | **Accept** |

### 9.8 C-07 — what a revised version must contain for my approval

1. Tombstone record defined and owned (A2R-13), or `Retired` explicitly descoped to "when the tombstone exists".
2. Capability-tag producer clarified: grant vs requirement (A2R-14).
3. `Status.*` additions dropped or confirmed as A1-internal (A2R-15 — my position: not needed).
4. Interactable persistence question stated by TD (A2R-16), even if the answer is "deferred".

**The three-class identity taxonomy, the tag inventory form, the no-rebind policy and eight of
nine tests need no revision.**

---

## 10. Cross-cutting: the eleven TD items, re-based onto v1.2

### 10.1 A1's nine items, my position on each

A1's §8.2 raises TD-01…TD-09. Now that I have read v1.2, all nine are re-based:

| A1 item | v1.2 status | My position | Changes? |
|---|---|---|---|
| **TD-01** v1.2 existence | **Resolved as a fact** — v1.2 exists at `e121bbb`; v1.2 §4 still says `AWAITING SUBMISSION` | **Withdrawn as a blocker.** I was wrong (§0.1) and so was A1's §0.2. No design decision needed | **Closed** |
| **TD-02** C-04 representation | **OPEN** (v1.2 §4 C-04) | **B preferred, A acceptable, C and D rejected** — §6.5, and I add the offline-enumeration argument | No |
| **TD-03** C-03 applied-event scope | **OPEN** | **Publish for Blocked and Parried**; `Immune` conditional (§5.6.1); clamped `Amount`; **one publisher** | No |
| **TD-04** C-01 route format/stability | **OPEN** | **New input: routes have no persistence requirement in Ch1** (§9.3). Format rejected as written; alternative in §3.4 | **Yes — strengthened with evidence** |
| **TD-05** C-02 stealth/noise | **"not a permanent exclusion"** per v1.2 | **Omit.** No approved design, no consumer. I confirm A1's exclusion and my §4.8 answer 5 | No |
| **TD-06** C-05 gameplay clock | **OPEN** | **Core world subsystem**, not per-actor. Both agents must read the same one — §7.3 | No |
| **TD-07** C-06 hold-progress authority | **OPEN** | **Router owns the timer**; interactable owns presentation. My §8.4 counter-proposal is about the *delivery shape*, not the authority | **Yes — reframed** |
| **TD-08** C-07 tag approval / retirement | **OPEN** | Tombstone required before `Retired` is implementable (A2R-13); non-reuse absolute | **Yes — made mechanical** |
| **TD-09** MEAD §5.4 arbitration | **OPEN** | **Option 1** (§5.5). Attacker language grants initiation, not arbitration | No |

**Result: 8 of A1's 9 remain open, 1 closes as a factual correction.** v1.2 resolving TD-01 did
not resolve any design choice — which is what v1.2 §1 says about itself.

### 10.2 Two new items I raise

| ID | Issue | Why it blocks | My recommendation |
|---|---|---|---|
| **TD-10** | **C-01 route-ID parent model** — must a route be anchored to a scene, or may it be anchored to a location? | §3.4: 4 of 8 traversal-capable locations host no scene, so a scene-anchored format cannot name their routes without inventing canon | Anchor to the **location**; `SceneId` optional diagnostics. Needs a TD ruling because it changes A1's published format |
| **TD-11** | **C-07 interactable persistence** — does the slice persist interactable state across level transition and save? | §9.6: without this, no interactable identity policy can be chosen without inventing a requirement | State it either way, including "deferred"; a deferred answer also unblocks §9.6 |

### 10.3 Where I deliberately leave the decision to its owner

The request: *"Where a field is outside Agent 2 authority, state the requested boundary and
leave the decision to its owner."* The places I do this:

| Decision | Owner | My stated boundary | I do not decide |
|---|---|---|---|
| Enum vs bool vs tag for stagger class | **TD** (TD-02) | B preferred; must be offline-enumerable | which is chosen |
| Gameplay clock ownership | **TD** (TD-06) | one shared, actor-independent clock | Core vs gameplay placement |
| Applied-event scope and payload | **TD** (TD-03) | Blocked/Parried published; one publisher | payload details |
| Tag namespace grants | **TD** (TD-08) | my requests, each with a consumer | whether granted |
| Capability enum placement | **TD** | A1's five names accepted | Core vs `TDDGameplay` |
| Hold-progress delivery shape | **A1** (proposal owner) | counter-proposal §8.4 | whether A1 accepts it |
| Marker representation | **Me** (A2) | data asset + thin actor | — (mine to propose) |
| Route key format | **TD** (TD-04/TD-10) | `CH01-<LOC>/ROUTE-<L>` | whether accepted |
| Prompt text and verbs | **Me + String Table** | from a table, never composed | — |

### 10.4 What I am not asking the TD to decide

I want to be precise about the boundary of this review:

- I am **not** asking the TD to choose between my prose and A1's on any point where the answer is
  mine to give (§3.4's format is a proposal, not a dispute).
- I am **not** asking the TD to rule on whether `A1-R1` is a good document. It is.
- I am **not** asking for a resolution of C-06's shape by TD authority. §8.4 is a design
  argument with A1; the TD decides only if we cannot agree.

---

## 11. Evidence — the five categories, kept separate

### 11.1 Category (a): nine independent data checks — **executed**

```
$ python3 Tools/world/contract_data_checks.py --verbose
[PASS] ch01_location_row_count             57 rows, 57 unique
[PASS] ch01_family_counts                  ENV 1 + others 40 + INT 16 = 57
[PASS] traversal_category_is_multivalued   8 traversal-capable of 57; TRV-prefix-only would
                                           find 5 and miss [CH01-SUB-009, CH01-SUB-020,
                                           CH01-EXP-003]
[PASS] exploration_category_is_multivalued 8 exploration-capable; non-EXP: [CH01-SUB-003]
[PASS] canon_status_has_three_values       {'ESTABLISHED': 22, 'PENDING APPROVAL': 3,
                                            'PROPOSED': 32}
[PASS] env_design_status_has_seven_values  57 rows checked against 7 allowed values
[PASS] location_ids_match_published_scheme 57 IDs; retirement NOT verifiable from a
                                           summary table (stated limit)
[PASS] excerpt_is_subset_of_full_capture   excerpt 13 rows, all present in the 57
[PASS] interactable_id_namespace_unresolved NO register source exists

checks: 9/9 passed
```

**What these 9 prove:** the register's vocabulary, counts and multi-valued categories are as
this review states them.
**What they do not prove:** anything about runtime behaviour, any contract, or that A1 agrees
with anything.

### 11.2 Category (b): twenty-three document tests — **executed**

```
$ python3 -m unittest discover -s Tools/world/tests -p "test_contract_submission.py"
Ran 23 tests in 0.004s
OK
```

| Group | Count | Proves |
|---|---|---|
| `TestFixtureIntegrity` | 4 | the 57-row capture parses and reconciles |
| `TestTraversalIsNotAPrefix` | 6 | the multi-valued finding; **a prefix-only parser fails these** |
| `TestExplorationIsAlsoMultivalued` | 2 | 8 exploration-capable, 1 outside `EXP` |
| `TestVocabularyIsClosed` | 3 | 3 canon + 7 design statuses, separate |
| `TestStatedLimits` | 3 | the checks do not overclaim |
| `TestProposalDocument` | 5 | my document claims no agreement and no freeze |

**These 23 test my submission, not A1's.** They are unchanged by this review.

### 11.3 Category (c): forty-two proposed contract acceptance tests — **not executed**

**None of the 42 has run. No implementation exists to run them against.**

Re-enumerated by unique ID for this review: **42 unique IDs, 0 duplicates.**

| Layer | Count |
|---|---|
| `L0-data` | **10** |
| `L1-unit` | **11** |
| `L2-auto` | **21** |

This corrects a count I stated imprecisely in my own submission's §1 executive summary — the
earlier "41" and the loose "42" both came from regex matching over prose rather than from
enumerating unique IDs. **42 is the verified figure**, and §11.3 above reproduces the method
(unique-ID enumeration, which is also what `TestAcceptanceInventory` asserts).

**What the 42 are:** a proposed inventory. **What they are not:** evidence of anything. `A1-R1`
correctly labels its own tests `PROPOSED / NOT RUN`; the same applies to mine.

### 11.4 Category (d): the "three versus four" discrepancy — **resolved by enumeration**

This is the defect `TDD-INT-RECON-001` v2.0 §7 records. Both original sentences were in my
document:

- §1 executive summary: **"Of those 10, executable today: 3"** — and then **named three**:
  `TraversalCategoryIsMultivalued`, `IdDuplicateDetection`, `IdDisplayLabelNeverAKey` (partially).
- §3.7: **"Tests I can run today: the four L0-data ones, against route records that do not yet
  exist. They must fail (no data) until route authoring begins."**

**These are not the same set, and §3.7's wording is wrong.** Working it through by enumeration:

| L0 test | Data needed | Exists? | Runnable today? |
|---|---|---|---|
| `TraversalRouteIdsAndMarkerValidation` | route records + `CH01_manifest.json` | manifest yes, **routes no** | **No** — cannot pass |
| `TraversalRouteIdStability` | route records | **no** | **No** |
| `TraversalCategoryIsMultivalued` | location register v2.9 rows | **yes** | **Yes — passes** |
| `TraversalUnreachableContent` | reachability graph over routes | **no** | **No** |
| `InteractablePromptIsLocalisable` | interactable prompt data / String Table | **no** | **No** |
| `IdAndTagRegistryValidation` | a tag registry + manifest content ids | registry **no** (manifest has no id/tag section) | **No** |
| `IdDuplicateDetection` | manifest content keys | **yes** | **Yes — passes** (6 locations + 2 scenes, 0 duplicates) |
| `IdRetiredNeverReused` | a retirement/tombstone record | **no** (§9.4) | **No** |
| `TagRegistryCompleteness` | a tag registry | **no** | **No** |
| `IdDisplayLabelNeverAKey` | content keys | **partial** — no spaces found in the 8 keys, but the sample is too small to call it a test | **Partially** |

**Resolved answer:**

| Question | Answer |
|---|---|
| How many L0 tests are executable today such that they pass? | **2** — `TraversalCategoryIsMultivalued`, `IdDuplicateDetection` |
| How many with a partial/degenerate result? | **1** — `IdDisplayLabelNeverAKey` (8 keys, too small a sample; it would pass vacuously) |
| How many are **runnable** but must **fail** because their data is absent? | **7** |
| Why did §3.7 say "four"? | **Unsupported.** No derivation produces four: not 2, not 3, not 7, not 10. The sentence was written from memory of the route-specific subset (the four `Traversal*` tests, of which only one is executable) and mislabelled as runnable | **§3.7's sentence was simply wrong.** The §1 figure of "3" is the defensible one, and I would now state it as **2 passing + 1 partial** |

**This is the fifth correction to my own submission.** The honest statement is: **2 of 10 L0
tests pass today, 1 partially, 7 cannot run for want of data.** I would rather state that than
defend a number.

### 11.5 Category (e): repository suite — **executed**

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/canon/tests` | 114 OK | **0** |
| `python3 -m unittest discover -s Tools/world/tests` | 256 OK | **0** |
| `python3 Tools/ci/l0_checks.py` | 14/14 | **0** |
| `python3 Tools/world/contract_data_checks.py` | 9/9 | **0** |

Full verification incl. evidence generation is reported in §14.

### 11.6 Category (f): nine analysis queries run for this review — **executed, not tests**

These produced the findings in §3.4 and §9.3. **A query that produced a finding is not a test
that guards it** — §13.2 states what each would need to become one.

| # | Query | Finding |
|---|---|---|
| 1 | Parse all 57 register rows; select `Category` contains `Traversal Area` | 8 traversal-capable locations |
| 2 | Cross-reference those 8 against locations named in the 46 scene rows | **4 of 8 host no scene** |
| 3 | Count distinct locations across 46 scenes | 38 |
| 4 | Search scene fixture for `The Root Way` / `Stream Crossing` / `Ravine` / `Threshold Path` | **0 matches** — those locations are not scene locations |
| 5 | Enumerate unique IDs in the 42-row acceptance table | 42 unique, 10 / 11 / 21 by layer |
| 6 | `CH01_manifest.json` top-level keys | no routes, no interactables, no ids/tags |
| 7 | Duplicate check over manifest location + scene keys | 0 duplicates → `IdDuplicateDetection` passes |
| 8 | Search repository for route records / tag registry | none exist |
| 9 | Count `test_` functions in the document test file | 23 |

### 11.7 What Agent 3 did and did not do

`TDD-INT-RECON-001` v2.0 §7 states plainly: *"This assignment performed source/document
inspection only. It did not execute tests... Agent 2's submitted evidence is reported as a
**source claim**, not rerun or independently validated here."*

**So: Agent 3 did not rerun my tests.** This review does not claim otherwise. The 9 checks and 23
tests reported in §11.1–§11.2 were run **by me, now**, in this task — and the evidence
artifact in §14 records that.

Conversely, **I did not rerun Agent 3's review**, and there was nothing to run — v2.0 ran no
tests either.

### 11.8 What 57/57 Chapter 1 location capture means, and what it does not

**Preserved, with provenance:**

| Property | Value |
|---|---|
| Source | `LOCATION_MASTER_REGISTER.md` v2.9, Drive `1E-PPUQh-Ck-4JhJNFFHTAY6CiBPbmxv5`, 534,140 bytes, read 2026-11-16 |
| Capture | `Tools/canon/tests/fixtures/location_register_ch01_summary_v29.md` |
| Rows | **57 of 57**, 0 duplicates |
| Verified against | the register's own published split: 1 ENV + 40 other + 16 INT = 57 |
| Register modified? | **No** — read-only |
| Retirement verifiable from it? | **No** — stated limit in the check itself |

**What it does not mean:** that I have 57 *scenes*, or that all 57 are `ESTABLISHED`. The split
is **22 ESTABLISHED / 32 PROPOSED / 3 PENDING APPROVAL** — 35 of 57 are not canon. **The capture's
completeness is not a claim about canon status**, and the 3 `PENDING APPROVAL` entries
(`SUB-001`, `INT-016`, `EXP-002`) carry `CD-5: PENDING APPROVAL — BLOCKOUT ONLY`.

### 11.9 Withdrawn claims, still withdrawn

Reaffirmed, because the request requires it:

| Withdrawn claim | Why | Status |
|---|---|---|
| "62 world interactables" | No source. Never was one | **Still withdrawn** |
| "8 registered props" | Props absent from all fixtures | **Still withdrawn** |
| "4 interior doors" conflation | Interiors are 16 location entries, not 4 doors | **Still withdrawn**, separated |
| "Route parent may be `TRV`/`EXP` only" (the §0.2 Defect 1 regex) | Contradicts the multi-valued category rule | **Withdrawn in this document**, §3.3 |
| "Actor destroyed mid-attempt → attempt cancels" | Contradicts M1 v1.4; A1 is right | **Withdrawn in this document**, §3.8 |
| Single merged player snapshot | A1's three-snapshot structure is correct | **Withdrawn in this document**, §4.3 |
| `CameraForward` and `HealthFraction` as context requirements | No consumer survives review | **Withdrawn in this document**, §4.4–§4.5 |
| "Damage does not interrupt a hold" (undecided) | A1's ordering is correct | **Withdrawn in this document**, §8.6 |
| "§3.7: four L0 tests runnable today" | Unsupported by enumeration | **Corrected in this document**, §11.4 |

**No new interactable or prop count is stated anywhere in this document.**

---

## 12. What I require of Agent 1 — my nine responses

The request asks what Agent 1 must provide. These are the questions I answered above and the
ones I need answered:

### 12.1 I answered A1's 25 dependencies

| A1 section | Dependencies | Answered in |
|---|---|---|
| §1.8 (C-01) | 5 | §3.10 |
| §2.8 (C-02) | 5 | §4.8 |
| §3.8 (C-03) | 5 | §5.2 (side of the boundary), §5.6 |
| §4.9 (C-04) | 4 | §6.4, §6.5 |
| §5.9 (C-05) | 5 | §7.2, §7.3, §7.5 |
| §6.8 (C-06) | 5 | §8.3–§8.6 |
| §7.7 (C-07) | 4 | §9.5, §9.6 |

### 12.2 The nine things I need from Agent 1

| ID | Contract | Question | Why it blocks me |
|---|---|---|---|
| **A2R-1** | C-01 | Is `RequiredCapabilityTags` conjunction only, or may I pre-evaluate a grouping and emit one tag? | I need OR for two Chapter 1 routes |
| **A2R-2** | C-01 | How do `TRV-003 The Stream Crossing` and `TRV-004 The Ravine and Liana Bridge` get authored within the five capabilities — or are they out of slice? | Three of my named locations have no capability that describes them |
| **A2R-3** | C-01 | Accept the location-anchored `RouteId` (§3.4), or supply a scene-or-parent rule? | 4 of 8 parents cannot be addressed |
| **A2R-4** | C-01 | Can a non-player caller obtain the capability set for offline validation? | My validator has no player |
| **A2R-5** | C-01 | Is `EnabledCondition` evaluable offline as unknown/true/false? | Reachability validation needs it |
| **A2R-6** | C-01 | Confirm no narrative/save content references a route (§9.3) | Sets route retirement policy |
| **A2R-7** | C-02 | Does the eligibility filter support a negative carrying tag? | Replaces `CarryState` as a field |
| **A2R-8** | C-02 | State `GetPlayerContext` `false` as one invariant; drop `Paused` from invalidation | Prevents aggro despawn on pause |
| **A2R-9** | C-03 | Document `PreResolvedOutcome` as advisory only | Prevents a second arbitration path |
| **A2R-10** | C-04 | Does the existing `FTDDCombatStateChangedEvent` fire on stagger **recovery**? | If yes, recovery needs no new type |
| **A2R-11** | C-05 | Assert zero open telegraphs per source after teardown | A silently-failed close latches defence |
| **A2R-12** | C-06 | Accept throttled progress + guaranteed `End(Completed)`, or name an interactable needing per-frame progress | The only outright disagreement |
| **A2R-13** | C-07 | Where does the retired-id tombstone live and who owns it? | `Retired` is not implementable |
| **A2R-14** | C-07 | Who **grants** a capability tag vs who authors the **requirement**? | One tag, two producers |
| **A2R-15** | C-07 | Confirm `Status.Interacting`/`Traversing`/`Airborne`/`LockedOn` are A1-internal (I do not need them) | Removes 4 tags from the request |
| **A2R-16** | C-07 | Interactable persistence across transition/save — TD question relayed | No identity policy can be chosen |

**Sixteen numbered items.** Nine are strictly Agent 1's to answer; the rest are TD questions I
am routing through A1 because A1 owns the surrounding clause. §11.2 of my counts said "9 new
Agent 2 requirements" — that is the nine that are purely A1's; the full list is sixteen.

---

## 13. What this review does not establish

### 13.1 Scope limits

| Not established | Why |
|---|---|
| That any contract is agreed | §1.3 — I approve no exact version |
| That any interface, enum, struct or tag is correct | Every one is `PROPOSED — NOT FROZEN` |
| That any contract test passes | 0 of 42 ran; no implementation exists |
| That A1 accepts anything in this document | A1 has not seen it; nothing here is a grant |
| That TD accepts anything in this document | TD has not reviewed it; v1.2 predates it |
| That M0 is complete or a project exists | No `.uproject`, no `Source/`, no build |
| That the environment is viable | C-10 unchanged; production host unknown |
| Runtime, performance or memory behaviour | No engine, no GPU, no simulation |

### 13.2 Findings that are not yet tests

Five findings in this review came from running a query (§11.6), not from a stored test. **A
finding is not a guard.** What each would need:

| Finding | Would become a test by | Exists? |
|---|---|---|
| 4 of 8 traversal-capable locations host no scene (§3.4) | A check cross-referencing the 57-row capture against the 46 scene rows and asserting the scene-less set | **No** |
| 42 unique acceptance IDs, 10/11/21 by layer (§11.3) | A check parsing the submission's tables and asserting the count and layer split | **No** |
| 2 of 10 L0 tests pass today (§11.4) | A harness that runs each named L0 test and reports pass/fail/skip with the missing-data reason | **No** |
| No route records or tag registry exist (§11.6 #8) | A check failing if either is absent — currently an absence is expected | **No** |
| `CH01_manifest.json` has no ids/tags section (§11.6 #6) | An L0 schema check | **No** |

**I am not claiming these as tested.** They are analysed. Turning them into tests is the next
milestone's work, not this task's — and this task is design-only.

### 13.3 The correction record

Five corrections to my own work in one document. Recording them together, because a reader
should be able to see whether I corrected myself or was corrected:

| # | What I got wrong | Who found it | Section |
|---|---|---|---|
| 1 | "v1.2 does not exist" | **Agent 3 v2.0 §4 (TD-01)**, and A1 §0.2 reached the same wrong conclusion | §0.1 |
| 2 | Prefix-only route regex contradicting my own prose | **Agent 3 v2.0 §3 (C-01)** | §0.2, §3.3 |
| 3 | "four L0 tests runnable" vs "three" | **Agent 3 v2.0 §7** | §11.4 |
| 4 | "Actor destroyed mid-attempt → attempt cancels" | **A1-R1 §1.6/§1.7** — A1 is right | §3.8 |
| 5 | Single merged player snapshot; `CameraForward`; `HealthFraction`; `CarryState` as a field; damage-does-not-cancel | **My own review against `A1-R1`** | §4.3–§4.5, §8.6 |

**Three found by Agent 3, one found by Agent 1, one found by me.** I note which, because a review
that presents every previous error as self-discovered is not trustworthy.

---

## 14. Verification — commands and results, exact

Run in this session, exit codes captured directly and not through a pipe.

| Command | Result | Exit |
|---|---|---|
| `python3 -m unittest discover -s Tools/canon/tests` | **114 OK** | **0** |
| `python3 -m unittest discover -s Tools/world/tests` | **256 OK** | **0** |
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_submission.py"` | **23 OK** | **0** |
| `python3 Tools/ci/l0_checks.py` | **14/14** | **0** |
| `python3 Tools/world/contract_data_checks.py` | **9/9** | **0** |
| `python3 Tools/world/gen_evidence.py` | see §14.1 | **0** |

### 14.1 Evidence artifact

The evidence run is recorded in `Docs/evidence/agent2/W-M2.5_evidence.json` with milestone
label `W-M2.5 — formal review of A1-R1`. It adds two checks to the previous milestone:

| Check | Result |
|---|---|
| `contract_data_checks` | 9/9 passed |
| `review_document_claims` | **43 tests OK** |

### 14.2 Claims this review makes testable, and the tests

The review's own factual claims are asserted by
`Tools/world/tests/test_contract_review.py` — **43 tests**:

| Claim | Test |
|---|---|
| 4 of 8 traversal-capable locations host no scene | `TestSceneGapForTraversalLocations` |
| The 8 traversal-capable locations are exactly the set in §3.4 | `TestTraversalRoster` |
| 42 unique acceptance test IDs, 10/11/21 | `TestAcceptanceInventory` |
| 2 of 10 L0 tests pass today, 1 partial, 7 blocked | `TestL0ExecutableCount` |
| A1's five capability names are the ones documented | `TestCapabilityVocabulary` |
| This document claims no agreement and no freeze | `TestReviewDocumentClaims` |
| This document states the v1.2 correction | `TestVersionCorrectionRecorded` |
| This document's own counts match its own tables | `TestReviewInternalArithmetic` (7 tests) |

**These tests test this review, not A1, and not any contract.** They exist so that a reader can
check my findings rather than take them on trust.

---

## 15. Document status, provenance and change log

### 15.1 Provenance

| Field | Value |
|---|---|
| Branch | `arena/5dde91a4-tdd` (existing; no new branch, no merge) |
| Document | `Docs/AGENT2_REVIEW_A1R1_V1.md` — **new file**, does not overwrite `Docs/CONTRACT_SUBMISSION_A2_V1.md` |
| Reviewed A1 version | `A1-R1` v1.0, commit `97828db7d9786c0fa5415578e796a822aab497a8` |
| My submission under review | `A2-C01…C07-1.0`, commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644` |
| Governing TD version | **v1.2**, commit `e121bbbf09562e3cba0efe81aad971809685db23` |
| Reconciliation read | `TDD-INT-RECON-001` v2.0, commit `d32660fee1b0234871b39b9fa56677c7cf62f28f` |
| Code, Core types, project | **None created.** `Source/` untouched |
| Branches merged | **None** |
| API frozen | **None** |
| Contracts marked `AGREED` | **0** |

### 15.2 Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Initial formal review of `A1-R1` v1.0 against `A2-C01…C07-1.0` and TD v1.2. Seven verdicts (3 partial, 2 agree-in-principle-not-agreed, 1 disagree, 1 clarification); 31 clauses accepted, 14 accepted with revision, 5 rejected; zero agreements, zero freezes; 16 numbered requirements on Agent 1; 11 TD items (8 open, 1 closed as correction, 2 new); five corrections to my own prior submission; evidence split into six categories with 9 checks and 23 tests executed and 42 contract tests not run. |

**This document is a review, not a contract.** No contract is agreed by it, no interface is
frozen by it, and no implementation is authorised by it.
