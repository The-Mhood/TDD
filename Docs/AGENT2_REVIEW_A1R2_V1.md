# AGENT 2 — FORMAL REVIEW OF AGENT 1 REVISION `A1-R2` v1.1

**Document ID:** `TDD-A2-REVIEW-A1R2-001`
**Version:** 1.0
**Date:** 2026-11-16 UTC
**Author:** Agent 2 — World Structure and Level Architecture

**Reviewing:** `TDD-A1-CONTRACT-RESPONSE-002` **v1.1 (`A1-R2`)**, exact commit `f578fe612ad173b74f99fcb187f825eb3de6f59a`
**Against:** my `A2-C01…C07-1.0`, exact commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644`
**Governing decisions:** `TDD-TD-INT-001` **v1.2**, commit `e121bbbf09562e3cba0efe81aad971809685db23`
**Reconciliation:** `TDD-INT-RECON-001` v2.0, commit `d32660fee1b0234871b39b9fa56677c7cf62f28f`
**Prior review:** `TDD-A2-REVIEW-A1R1-001` v1.0, commit `93b2f07a71a48046e17bd59c0efde4c993e4bb46` — preserved unchanged

**Status:** `DESIGN_ONLY`. No C++, no Core type, no Unreal project, no merge, no API freeze, no M0 claim.

> Every shape in this document is `PROPOSED — NOT FROZEN`.
> No test named here has run. **Agreed: 0 of 7** — see §1.3 for why that is still the honest
> number and what specifically would change it.

---

## 0. Reading notes and one finding that has to come first

### 0.1 There are three documents called `TDD-MEAD-001` v1.0, and it decides C-05 and C-07

Before reviewing any clause I had to resolve which MEAD `A1-R2` cites, because eight of its
citations are to `MEAD §3.5`, `§4.4`, `§4.5`, `§5.4` and `§5.5`. I initially checked the two MEAD
files I had and found **no §5.4 in either, no `Status.*` tag, no `Damage.*` tag, no
`ITDDDamageable`, no `FTDDDamageRequest`**. On that basis I was about to write that A1's citations
were fabricated.

**That would have been wrong, and it would have been my third wrong-version error in two
reviews.** There are three divergent documents:

| ID | Path | Lines | §5.4? | `Status.*` tags | Where it exists |
|---|---|---|---|---|---|
| **MEAD-A** | `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` | 1,078 | **no** | **none** | my working tree |
| **MEAD-B** | `docs/MASTER_ENGINEERING_ARCHITECTURE.md` | 247 | **no** | **none** | packet `50b1431`, recon commit `d32660f` |
| **MEAD-C** | `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | 1,231 | **yes** | **7 tags** | Agent 1's branch `b9ab305` |

**`A1-R2`'s citations are correct — against MEAD-C.** I verified every one (§7.5, §9.6). MEAD-C
§5.4 is a real "Damage pipeline" section containing exactly the diagram `A1-R1`/`A1-R2` quote, and
MEAD-C §5.1 does list `Status.Staggered` among seven status tags.

**So I withdraw the fabrication hypothesis before stating it.** But the three-way divergence is
itself a finding that blocks C-07 and part of C-05, and it is raised as **TD-12** (§11).

**Method lesson, recorded because I have now made this error twice:** my review of `A1-R1`
corrected me for saying v1.2 "does not exist" when it existed at a commit I had not fetched. The
correct procedure is to **search every reachable commit and branch for a document identity before
asserting absence**, not to search the refs I happen to have. This review does that (§14.4 lists
the search), and that is why the fabrication hypothesis was killed before publication.

### 0.2 What I checked before reviewing

| Check | Result |
|---|---|
| A1-R2 read in full (688 lines) | **done** |
| Three MEADs located, identified and diffed on the cited clauses | **done** — §0.1 |
| Every `A1-R2` MEAD citation traced to MEAD-C | **done** — §7.5, §9.6 |
| Every `A1-R2` attribution of a position to *me* checked against my submission | **done** — two are wrong, §0.3 |
| TD v1.2 re-read against A1-R2's §10 claims | **done** — §10.1 |
| Recon v2.0 re-read against A1-R2's §11 answers | **done** |
| Ran my existing checks and tests | **done** — §13.1 |
| Wrote C++, Core types, project files | **no** |
| Merged, froze, or marked anything agreed | **no** |

### 0.3 Two places where `A1-R2` misattributes a position to me

Both matter because a review cannot accept a resolution of a request I did not make.

**Misattribution 1 — `A1-R2` §9.2 says I proposed `Combat.State.*` and `Combat.Damage.*` as
namespaces that *collide* with MEAD.** My submission's §9.4 table has these two rows:

```
| `Combat.Damage` | `Slash`, `Impact`, `Root`, `Thunder` | C-03 | REQUESTED |
| `Combat.State`  | `Staggered`, `Cinematic`, `Dead`     | C-04 | REQUESTED |
```

I did propose them. **But `A1-R2` treats the collision as one I should map onto MEAD's
`Status.*`/`Damage.*`.** MEAD-C has **no `Status.Dead`** and **no `Status.Died`** — I verified
this (§9.6). So my `Combat.State.Dead` cannot yield to a MEAD tag that does not exist, and the
"yield to MEAD" instruction is unexecutable for exactly one of my three values. §9.4 states the
resolution.

**Misattribution 2 — `A1-R2` §4.5 and §11 item 5 imply I hold `CarryState` as a live `REQUIRED`
field that A1 is declining to provide.** My submission does have `CarryState`/`ETDDCarryState`
marked `REQUIRED` (§4.2). **The request asks me to establish whether a Chapter 1 requirement
actually supports it.** I did that check and the answer is that it does not. **I withdraw it**
(§4.5). A1's refusal was correct and I am not contesting it — I am conceding it.

### 0.4 Corrections to my own prior position in this review

| # | What changes | Driven by | Section |
|---|---|---|---|
| 1 | **My C-05 "undilated window" rule is defective. I withdraw it.** | MEAD-C §5.5's pair-hitstop definition, and A1-R2's arithmetic | §7.3 |
| 2 | `CarryState` withdrawn — no Chapter 1 requirement supports it | the request's explicit test, and my own check | §4.5 |
| 3 | `PostureFraction` was never actually requested by me; I said so correctly, A1-R2 correctly reads it as unrequested | my §4.2 vs A1-R2 §4.4 | §4.4 |
| 4 | My `Interaction.Mode` tag request is withdrawn — `HoldDurationSeconds` suffices | A1-R2 §9.3's argument, which is correct | §9.5 |
| 5 | My `Traversal.State` tag request is withdrawn — duplicates A1's outcome enum and `bOneWay` | A1-R2 §9.2 | §9.5 |

**Five corrections, and #1 is substantive: A1-R2 is right and I was wrong on the single item
flagged as a "major unresolved disagreement".** §7.3 says so plainly.

---

## 1. Agreement matrix

### 1.1 The seven verdicts

| Contract | A1-R2 clauses reviewed | Verdict | What stands in the way |
|---|---|---|---|
| **C-01** | §3.1–§3.5, P1–P5, projection | **AGREE with one recorded condition** | P3 "never reused" is stricter than the evidence supports (§3.6); projection is sound (§3.5) |
| **C-02** | §4.1–§4.7 | **AGREE** | None blocking. `CarryState` withdrawn, health removed, `bInCombat`/`CameraForward` accepted |
| **C-03** | §5.1–§5.5 | **AGREE** | Event scope and single publisher accepted; one payload field clarified (§5.5) |
| **C-04** | §6.1–§6.4 | **AGREE with one condition** | `ETDDStaggerClass` semantics accepted; recovery notification accepted; **`Status.Dead` gap must close** (§6.5) |
| **C-05** | §7.1–§7.4 | **PARTIALLY AGREE** | I withdraw my undilated rule (§7.3); **per-entity clock is incomparable under asymmetric dilation** (§7.4) |
| **C-06** | §8.1–§8.4 | **AGREE** | `bWantsProgress` resolves my position; damage-interrupt correctly escalated (§8.5) |
| **C-07** | §9.1–§9.4 | **CLARIFICATION REQUIRED** | Three-MEAD divergence (§0.1); `Status.Dead` absent (§9.4); no registry owner |

**Agreed: 0 of 7.** Five contracts are at `AGREE`/`AGREE with condition` at the *clause* level,
which is the strongest position these two submissions have reached — but §1.3 explains why that
is not the same as a signature, and §1.4 names exactly what closes each one.

### 1.2 Counts

| | |
|---|---|
| Contracts reviewed | **7 of 7** |
| Marked `AGREED` | **0** |
| `AGREE` (clause level) | **3** — C-02, C-03, C-06 |
| `AGREE with one recorded condition` | **2** — C-01, C-04 |
| `PARTIALLY AGREE` | **1** — C-05 |
| `CLARIFICATION REQUIRED` | **1** — C-07 |
| A1-R2 clause verdicts recorded | **61** |
| Accepted without change | **56** |
| Accepted with a named revision or condition | **5** |
| Rejected | **0** |
| Deferred to the registry owner (in the C-07 collision table, not counted above) | **2 namespaces** |
| My own positions withdrawn this review | **5** (§0.4) |
| A1-R2's 16 dependency answers accepted | **15** |
| A1-R2's 16 dependency answers disputed | **1** (item 12, dilation) |
| New TD items raised | **2** (TD-12, TD-13) |
| Tests executed | **9 checks + 23 + 43 tests** (§13.1) |
| Contract acceptance tests run | **0** |

**A1-R2 rejected zero clauses of mine, and this review rejects zero of A1-R2's.** That is worth
stating: the two submissions have no clause-level conflict remaining except C-05, and the C-05
conflict is now mine to concede (partly) rather than A1's.

### 1.3 Why I still do not write `AGREED`

`AGREED` means I accept the *exact version and clauses* as they stand. Three specific things
prevent that, and none of them is a matter of preference:

1. **C-07 cannot be agreed by either agent.** It requires a registry owner and a save inventory
   that do not exist, and the three-MEAD divergence (§0.1) means "yield to MEAD's namespace" is
   not yet an executable instruction. A1-R2 says the same thing in its own §9.1 — we agree the
   contract is unagreed.
2. **C-05 contains a defect I can now demonstrate** (§7.4) in the model A1-R2 proposes. Signing
   it would be signing something I can show produces a parry window the player cannot see.
3. **TD v1.2 §4.1 requires both agents to sign the same version and TD to review after.** Four
   of A1-R2's own `UNRESOLVED` items (U-01, U-02, U-08, U-10) change clauses inside the contracts
   I would be signing.

**What I will do instead, and it is stronger than a signature on an unstable version:** §1.4
lists, per contract, the exact condition under which I sign the next version. Each is one or two
items and none requires a TD design ruling except C-07.

### 1.4 The signing conditions — what closes each contract

| Contract | I sign the next version when… | Owner |
|---|---|---|
| **C-01** | P3 is restated to match the evidence (`A1-R2` §10.4 already says route key "may be renamed per level edit with no migration" — P3's "permanent, never reused" contradicts it) | **A1-R2 self-consistency** |
| **C-02** | Nothing. **I sign C-02 as written today**, subject to A1 confirming the exact version is final | — |
| **C-03** | Nothing blocking. **I sign C-03 as written today**, subject to TD-03 confirming the blocked/parried event scope | TD-03 |
| **C-04** | `Status.Dead` (or a named equivalent) is added to the inventory, because `Dead > Cinematic > Stagger` needs a tag for `Dead` | A1 + registry |
| **C-05** | The asymmetric-dilation case is handled by one of the two options in §7.6 | TD-06 |
| **C-06** | Nothing blocking. **I sign C-06 as written today**; the damage-interrupt question is correctly outside it | — |
| **C-07** | Three-MEAD divergence resolved and a registry owner named | TD-12 + Agent 3 |

**Three contracts (C-02, C-03, C-06) are signable now.** I am not signing them in this document
because the request asks for a review, not a signature, and because signing three of seven in a
review whose verdict table says `0 agreed` would be a document disagreeing with itself. I say
plainly: **on C-02, C-03 and C-06 I have no remaining technical objection to the A1-R2 text.**

---

## 2. Method

### 2.1 The test applied to every clause

1. **Does it contradict a pinned ownership decision?** → `DISAGREE`, name it.
2. **Does it require me to author, persist or validate data I cannot source?** → `DISAGREE` or
   `CLARIFICATION`, name the missing source.
3. **Would it produce a defect at a boundary I own** — streaming, 57-location parenting, scene
   absence, dilation? → `PARTIALLY AGREE` with a counter-proposal.
4. **Does it resolve a question I raised, even if I disagree with the answer?** → accept and say
   so. This is the rule that produced all five withdrawals in §0.4.
5. Otherwise → accept without hedging.

Rule 4 did the most work this review. The request warns "do not simply repeat your original
preference", and the correct response to that warning is to check whether the preference survives
scrutiny rather than to defend it. It did not survive for C-05.

### 2.2 What I refuse to do

| Refused | Why |
|---|---|
| Treat near-identical proposals as agreement | The request's own instruction; §1.3 shows it would also be inaccurate |
| Defend my C-05 rule because it was mine | It is defective under MEAD-C §5.5; §7.3 |
| Assert "A1 cited a document that does not exist" without searching all refs | I nearly did; §0.1 |
| Claim A1's answers to my 16 items are agreement | They are answers. §11 reviews each |
| Accept `CarryState` because I once marked it `REQUIRED` | It has no source; §4.5 |
| Invent a carry system, interactable id family, or persistence policy | Explicitly prohibited; §4.5, §9.7 |
| Mark a contract agreed while its clauses are still `UNRESOLVED` in A1's own table | §1.3 |

---

## 3. C-01 — Traversal

**Reviewed:** `A1-R2` §3.1–§3.5. **Verdict: AGREE, with one recorded condition on P3.**

### 3.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §3.2 | Route format withdrawn; restated as P1–P5 properties | **ACCEPT** — this is a better answer than my format |
| §3.2 P1 | Opacity: runtime never parses the key | **ACCEPT** |
| §3.2 P2 | Uniqueness: global, duplicate registration refused deterministically | **ACCEPT** |
| §3.2 P3 | Stability: "permanent, never reused" | **ACCEPT with condition** §3.6 |
| §3.2 P4 | Non-derivation: not computed from a transform | **ACCEPT** |
| §3.2 P5 | Key must not encode required capability | **ACCEPT — and it is a good catch** §3.3 |
| §3.2 | Accepts my location-anchored shape as satisfying P1–P4 | **ACCEPT** |
| §3.2 | Accepts Category-not-prefix as a reported source fact, flagged `DEPENDENCY` | **ACCEPT** — correct handling of evidence it did not gather |
| §3.3 | Five capabilities named | **ACCEPT** |
| §3.3 | Requirements are **data**: tag container + AND/OR grouping, no predicates | **ACCEPT** — answers my `A2R-1` in full |
| §3.3 | Independent set membership, no "A then B" sequence | **ACCEPT** |
| §3.3 | Revocable; evaluated per query; no mid-execution abort | **ACCEPT — see §3.4** |
| §3.3 | Water/rope out of scope for the slice | **ACCEPT as scope, note §3.5** |
| §3.4 | Seven outcomes → six world projections, `Cooldown` → `Blocked`+reason | **ACCEPT — see §3.7** |
| §3.4 | Projection is total, lossy only at `Cooldown` | **ACCEPT with verification** §3.7 |
| §3.4 | No prompt for five of seven outcomes; no M1 v1.4 conflict | **ACCEPT** |
| §3.5 | Status table | **ACCEPT** |

### 3.2 P1–P5 — A1's properties are better than my format, and I say so

My `A2-C01…C07-1.0` §3.4 argued for a specific string: `<PARENT_LOCATION_ID>/ROUTE-<LETTER>`.
`A1-R2` §3.2 withdraws its own competing format and restates the requirement as **five
properties any format must satisfy**. That is the correct move and it is better than my answer for
a reason worth naming: **my format was one solution to a problem A1 had stated as one solution,
and A1 has now stated the problem.** Two agents agreeing on a property set is a contract. Two
agents agreeing on a string is a coincidence that breaks the first time someone writes an
importer.

**P1–P4 are satisfied by my shape** and A1 says so. **P5 is new to me and I accept it without
reservation:** the key must not encode the required capability. My proposed key
(`CH01-TRV-002/ROUTE-A`) does not, so nothing changes — but the property is right and I would not
have thought of it. A route whose `Vault` requirement becomes `Mantle` after review must not
become a different route; encoding capability in the key would silently retire it.

### 3.3 The independent/revocable capability model — accepted, including the part that limits me

`A1-R2` §3.3 answers my four open questions:

| My question | A1-R2 answer | My acceptance |
|---|---|---|
| Capability names and shape | `Vault`, `Mantle`, `LedgeShimmy`, `Drop`, `ClimbLadder`; exec enum + one tag each | **Accepted, adopted verbatim** |
| Data or code | **Data** — tag container + AND/OR grouping | **Accepted — this is what makes my offline validator possible** |
| Cumulative vs independent | Independent set membership | **Accepted** |
| Revocable | Yes; per-query; no mid-execution abort | **Accepted** |
| Water/rope context | Out of scope in this slice | **Accepted as scope** |

**The independent model costs me something and I am accepting it anyway.** My §3.3 asked whether
requirements could express "Vault **or** Mantle clears the same obstacle". Under independent set
membership that is now expressible only if A1's AND/OR grouping is real. `A1-R2` §3.3 says
"tag container plus an AND/OR grouping" — so it is. **`A2R-1` is closed.**

**The revocation rule is the one I want to underline, because it settles `A2R-2` differently than
I expected.** A1 says revocation takes effect on the next query and **does not abort a traversal
in flight**, because M1 v1.4 governs the exit and a tag change is not an abort trigger. That is
correct and it is better than my position: I had asked for revocation to be able to stop a
traversal. It cannot, and should not — a capability being removed mid-montage is not a reason to
strand the player mid-air, and the recorded exit anchor is authoritative. **I withdraw the
request for mid-execution revocation.**

### 3.4 Water and rope — accepted as scope, with one consequence A1 should see

`A1-R2` §3.3 puts water/rope out of scope for the slice. I accept the scope. The consequence is
concrete and belongs on the record rather than in a discussion:

**`CH01-TRV-003 The Stream Crossing` and `CH01-TRV-004 The Ravine and Liana Bridge` cannot have
authored routes in this slice.** Not "are deprioritised" — cannot. A1's five capabilities contain
no branch that crosses water or uses a liana bridge, and A1's own §1.2 rule is that a sixth
capability needs an ADR.

**This does not block C-01.** It is a content-scope fact the level design must respect, and I
would rather record it than discover it when someone tries to author a route there. If the slice
later needs them, the sequence is: new capability → ADR → contract revision, exactly as A1 says.

### 3.5 P3 — the one condition I record

`A1-R2` §3.2 P3 says a route key is **"Permanent, never reused after retirement"**, justified as
"Saves, logs and telemetry must resolve the same content forever".

**`A1-R2` §10.4 contradicts this, in the same document:**

> "if none does [reference a route], a route key **may be renamed per level edit with no
> migration**"

Both cannot be true. And §10.4 is the half that matches the evidence I supplied: **no narrative,
checkpoint or save content in Chapter 1 references a route key** (`A2-C01…C07-1.0` §9.3; A1-R2
§10.4 concurs from its side).

**So P3 as written over-constrains the slice.** "Never reused after retirement" is the right
property for an identifier that appears in a save. For a route key that appears only in a
validator, a log and telemetry, it imposes tombstone governance on content that has no
compatibility surface.

**My condition, stated as a proposed P3 revision:**

> **P3 (revised):** A route key is **stable for the lifetime of the content it names**. It is
> never reused for different content while referenced by any save, log or telemetry entry. Whether
> a retired key must be tombstoned depends on whether a save references route keys, which is
> **TD-04's question and not a C-01 property**.

This is not me asking A1 to weaken a guarantee. It is asking that the guarantee be scoped to the
thing it protects. If TD-04 rules that saves will reference routes, **P3 as originally written
becomes correct and I will support it.** A1-R2 §10.4's own answer is that they will not.

### 3.6 The seven-outcome projection — verified, and `Cooldown` is safe

The request asks specifically whether the projection loses information my systems need,
**especially `Cooldown` represented as `Blocked` with a reason code.**

I enumerated all seven of A1's outcomes against the six world values and the reason-code escape:

| A1-R2 outcome | Projects to | Information lost? | Do I need the lost bit? |
|---|---|---|---|
| `CandidateFound` | `Available` | none | — |
| `UnsupportedByPlayer` | `Unsupported` | none | — |
| `None` | `NoCandidate` | none | — |
| `BlockedPath` | `Blocked` | none | — |
| `WorldUnavailable` | `Unloaded` | none | — |
| `InvalidAuthoredData` | `Invalid` | none | — |
| `Cooldown` | `Blocked` **+ reason code** | none **if the reason code is carried** | **yes** |

**Verdict: the projection does not lose information I need, and the one lossy point is exactly
where A1 has put a reason code.**

Why the distinction matters to me concretely: `Blocked` and `Cooldown` drive different authoring
responses. A route returning `Blocked` at authoring time usually means my geometry is wrong — an
exit anchor inside a wall, a chest-high obstacle classified as `Mantle` when it needs `Vault`.
A route returning `Cooldown` at authoring time usually means the same route is being queried for
both directions of a two-way path and the re-entry guard is firing. **If those collapse, my
validator reports a geometry bug for a routing bug**, and the author spends an afternoon moving a
marker that was correct.

**Two conditions I record, neither of which disputes the design:**

1. **The reason code must be present on every `Blocked`, not only on `Cooldown`.** A `Blocked`
   with no reason is indistinguishable from a projection bug. A1-R2 §3.4 says `Cooldown` "keeps
   the reason visible"; I am asking that `Blocked`-from-`BlockedPath` also name itself, so that
   the world value plus reason is a total map back to A1's enum. That makes the projection
   **invertible**, which is a stronger and more testable property than "total with one lossy
   point".
2. **`Invalid` must be unreachable in a cooked build.** A1-R2 §3.4 agrees it is "an authoring
   error, never a player-facing message". I need it to fail my L0 gate so it cannot reach a
   build — that makes it a `Error` at author time and a `check()` at run time, not a silent
   `Invalid`.

**Both are mine to implement** in the validator I own. I am not asking A1 to change the enum.

### 3.7 Tests

`A1-R2` §12.5 proposes `TDD-Contract.Traversal.WorldProjectionTotality` (new, +1 over A1-R1). **Accepted**, and I add the invertibility assertion in my own layer:

| Proposed addition (mine) | Asserts |
|---|---|
| `TDD-Contract.World.RouteProjectionIsInvertible` | For every one of A1's seven outcomes, `project(outcome)` followed by `unproject(worldValue, reason)` returns the original outcome — including `Cooldown` vs `BlockedPath` both mapping to `Blocked` with distinct reasons |

**Plus the two tests from my previous review that remain unbuilt:**

| Test | Asserts |
|---|---|
| `TDD-Contract.World.RouteKeySyntaxAcceptsAllPermittedFamilies` | syntax accepts every permitted registered family; no traversal eligibility inferred from prefix |
| `TDD-Contract.World.RouteParentCategoryIsTraversal` | resolves `ParentLocationId` to the register and requires multi-valued Category ∋ `Traversal Area`; **a prefix-only implementation fails** |

### 3.8 C-01 verdict

**AGREE**, with P3's self-contradiction recorded as the only condition, and the water/rope
content-scope consequence noted. **P1, P2, P4, P5, the five capabilities, the data-driven
requirements, the independent-and-revocable model, and the projection are all accepted as
written.**

---

## 4. C-02 — Player context

**Reviewed:** `A1-R2` §4.1–§4.7. **Verdict: AGREE.**

### 4.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §4.2 R2-1 | `HealthFraction` **and** `PostureFraction` removed | **ACCEPT amended** §4.4 |
| §4.2 | Health threshold becomes `EvaluatePhaseCondition(ConditionTag) -> bool` query | **ACCEPT — this is what I asked for** |
| §4.3 R2-2 | `bInCombat` accepted as a derived field | **ACCEPT — see §4.2** |
| §4.3 R2-2 | `CameraForward` accepted; documented as distinct from `AimDirection` | **ACCEPT — see §4.3** |
| §4.4 R2-3 | Full field classification table | **ACCEPT with two corrections** §4.4 |
| §4.4 | `ControlState`, `bAllowsInput`, `bLocked`, `StateElapsedSeconds` → **Conditional** | **ACCEPT, and I resolve them** §4.6 |
| §4.4 | `ActiveActionId` conditional (diagnostics) | **ACCEPT** |
| §4.4 | `HeightAboveGround`, `GroundSlopeDegrees`, `bOnWalkableFloor` → Conditional | **ACCEPT** |
| §4.5 | `CarryState` **not provided** — no carry system exists | **ACCEPT — and I withdraw the request** §4.5 |
| §4.6 R2-4 | Staleness: A1's one-frame guarantee is stronger than my 2-frame rule | **ACCEPT** |
| §4.6 | Both readings supported: `GetPlayerContext` false **and** last frame carries `bValid=false` + reason | **ACCEPT — resolves my previous `A2R-8`** |

### 4.2 `bInCombat` — accepted, and A1's reasoning is better than mine

I requested `bInCombat` and `A1-R2` §4.3 accepts it as **derived**: `CombatState != None &&
CombatState != Dead`. Its stated reason — *"rather than make A2 infer it from a 12-value enum,
because 'is this a fight' is a real consumer decision and inference across modules is how drift
starts"* — is exactly right and it is a stronger argument than the one I made.

My consumer is Chapter 1's crowd and ambient system: ambient barks and crowd idle must suppress
when combat starts and return when it ends. I could infer that from `ETDDCombatState`, but I would
be encoding A1's enum semantics in my subsystem, and the moment A1 adds a combat substate my
inference is wrong. **A derived boolean published by the authority is the right shape.**

One implementation note, not a condition: `bInCombat` must be derived from the **same** frame's
`CombatState` inside the envelope, not computed separately, or a consumer can see
`bInCombat == true` with `CombatState == None`. A1-R2 §2.4 of A1-R1 already guarantees envelope
consistency; I am noting that the derived field must be inside it.

### 4.3 `CameraForward` versus `AimDirection` — accepted, and I withdraw `CameraForward`

`A1-R2` §4.3 publishes both and documents them as different: camera forward is the **view axis**,
aim is the **input-derived direction**.

**I accept the distinction and I withdraw my request for `CameraForward`.**

Reason: my only stated consumer was AI facing prediction — *"where is the player looking"*. For
that decision, `AimDirection` is the correct signal, because it is what the player's input is
steering and it is what the attack will follow. `CameraForward` describes where the camera points,
which in a third-person game diverges from aim by the framing offset. **I was asking for the
wrong one of the two.** I had previously withdrawn `CameraForward` in my A1-R1 review (§4.5) for
the same reason; `A1-R2` accepting it does not revive my need for it.

**So: `CameraForward` is A1's to publish, it is useful for view-cone scoring, and I am not a
consumer.** I record that plainly so the field is not carried on the strength of a request I no
longer make.

### 4.4 Health and posture — the removal is correct, with one amendment to the credit

`A1-R2` §4.2 removes **both** `HealthFraction` and `PostureFraction`, and attributes the health
half to my withdrawal and the posture half to it being "unrequested".

**Both halves are correct and I want the record exact:**

- **Health:** I withdrew it in `A2-C01…C07-1.0` §4.3, and asked for a phase-condition evaluation
  instead. `A1-R2` §4.2 now offers `EvaluatePhaseCondition(ConditionTag) -> bool`. **Accepted,
  and it is precisely the shape I asked for** — one derived boolean, no continuous value I could
  trend or interpolate, no attribute access from my side.
- **Posture:** I never requested it. A1-R2 §4.4 says "posture unrequested", which is accurate. My
  A1-R1 review had marked `PostureFraction` as **REQUIRED** for `CH01-BOS-001` phase 2 keying on
  posture break — that was my review's position, not my submission's, and it was wrong to
  promote it. **`EvaluatePhaseCondition` covers it.** I withdraw the posture requirement.

**One consequence I accept rather than dispute:** without `PostureFraction` I cannot trend
aggression against posture *continuously*. My enemy AI will see `bIsStaggered` transitions and
phase-condition booleans instead. That is a coarser signal and it is the correct trade — a
continuous posture read is a second authority by the back door, which is exactly what my own §4.3
said about health.

### 4.5 `CarryState` — I withdraw it, and here is the check the request asked for

The request: *"establish whether there is an actual Chapter 1 requirement supported by an existing
design or register entry. If so, identify the source and required semantics. If not, withdraw the
requirement for this slice rather than inventing a carry system."*

**I ran that check. The answer is no, and I withdraw `CarryState`.**

| Where I looked | What is there |
|---|---|
| Location register v2.9, all 57 CH01 entries | **No carry, portage or burden vocabulary.** No `Category`, name, or status mentions carrying |
| Scene register v1.9, all 46 CH01 scenes | **No scene is gated on, or describes, carrying an object** |
| `A2-C01…C07-1.0` §4.2 (my own snapshot) | `ETDDCarryState CarryState` marked `REQUIRED` for "traversal gating" — **my assertion, no source cited** |
| My C-01 route requirements | No route requires a carry state; requirement is capability tags only |
| M1 v1.4 (A1's movement spec) | No carry system |
| Canon rules (21) | No carrying rule |

**My submission cited no source because there was none.** The row said "Q2 in the C-01 request:
some routes close under carry" — and the C-01 request does not say that either. This is the same
class of error as the "62 interactables" and "8 props" I withdrew earlier: **an assertion of need
without a source.**

**Withdrawn.** No `CarryState` field, no `ETDDCarryState`, no carry system invented. If a Chapter
2 design introduces carrying, the sequence is: design decision → carry system owner → enum →
gating rule → snapshot field, exactly as `A1-R2` §4.5 states. **A1's refusal to provide it was
correct and I am not contesting it — I am conceding it.**

### 4.6 Conditional fields — I resolve the ones that are mine

`A1-R2` §4.4 marks `ControlState`, `ControlStateTag`, `StateElapsedSeconds`, `bAllowsInput`,
`bLocked` as **Conditional** because "A2 has not named a decision that fails without them". It
also offers one candidate: *"do not attack a player locked in a traversal or a cinematic"*.

**I now name the decisions, so these resolve:**

| Field | My decision that fails without it | Resolution |
|---|---|---|
| `ControlState` / `ControlStateTag` | Boss must not launch a punish during a `Cinematic` takeover; encounter manager must not count a `Cinematic` player as engaged | **REQUIRED** — C-02 confirmation |
| `bAllowsInput` / `bLocked` | Tutorial beat in `CH01-SUB-001`: AI must not punish an unresponsive player | **REQUIRED** — C-02 confirmation |
| `StateElapsedSeconds` | Boss fairness pacing: no re-attack within 0.5 s of `Stagger` exit | **CONDITIONAL** — becomes required only if that pacing survives design review |
| `HeightAboveGround` / `bOnWalkableFloor` | Ledge-awareness at `CH01-SUB-005 Waterfall Escarpment` | **REQUIRED** for the escarpment; **removable** if the escarpment encounter is cut |
| `GroundSlopeDegrees` | **none** | **UNREQUESTED** — as A1-R2 classifies it |
| `ActiveActionId` | **none** that I own | **UNREQUESTED** by me; A1 may keep it for telemetry |

**A1-R2's `Conditional` classification was correct at the time it wrote it, and my naming of these
decisions is what converts two of them to `REQUIRED`.** That is the process working.

### 4.7 C-02 verdict

**AGREE.** `bInCombat` and `EvaluatePhaseCondition` are accepted; health, posture, `CarryState` and
`CameraForward` are withdrawn or resolved; the field list is settled with the resolutions in §4.6.
**No remaining technical objection to the A1-R2 text.**

---

## 5. C-03 — Damage

**Reviewed:** `A1-R2` §5.1–§5.5. **Verdict: AGREE.**

### 5.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §5.2 R3-1 | `RequestId` (caller-generated) + `HitEventId` (publisher) replaces `HitInstanceId` | **ACCEPT** |
| §5.2 | Dedupe on `(SourceEntityId, RequestId)` | **ACCEPT — simpler than mine** |
| §5.3 R3-2 | Event scope table: applied/blocked/parried yes; immune/miss/rejection **no** | **ACCEPT — see §5.4** |
| §5.3 | `Amount` = clamped health actually removed; `bLethal` carries overkill | **ACCEPT** |
| §5.3 | `PostureDelta` added | **ACCEPT** |
| §5.4 R3-3 | **A1 is sole publisher** for every applied hit, including on MY actors | **ACCEPT — see §5.3** |
| §5.4 | Target unload drops the event (my request) | **ACCEPT** |
| §5.4 | `SourceContentKey` accepted as proposal, empty for player until C-07 | **ACCEPT — correct caution** |
| §5.4 | Per-source `SequenceNumber`; cross-source order unspecified | **ACCEPT** |

### 5.2 Is Agent 1 the exclusive arbitration authority for every hit involving the player?

**Yes. Confirmed without reservation.** This is the central ownership question and both documents
now state it identically:

> `A1-R2` §10.9 role 3: *"Arbitration / resolution — **A1, exclusive**, for every hit involving
> the player. No second arbiter, no A2-side outcome guessing."*

**My side, stated as a commitment rather than a claim:**

| Agent 2 will | Agent 2 will not |
|---|---|
| Emit a damage request carrying authored intent | Detect overlap against the player capsule |
| Consume the applied event | Evaluate the player's defence, block or parry |
| Own and write **its own** actors' health via `ITDDDamageable` | Apply damage to the player outside A1's arbiter |
| React to `Outcome` for combo/poise/phase | Guess an outcome from its own request |

**I accept `A1-R2` role 2 as well**: A1 performs **hit detection** against the player, not me.
That is slightly stronger than my original submission, which assumed I would detect the overlap
and send the result. `A1-R2` §10.9 says detection is authority, and that A2's authored volumes
are data. **That is the correct split** — it removes the frame-ordering question of whether my
trace or A1's arbitration runs first, because only one of us runs a trace at all.

### 5.3 The single publisher for hits on my actors — accepted

`A1-R2` §5.4: **A1 publishes every applied event**, including hits where the target is my actor;
my `ITDDDamageable` implementation performs the attribute write and **returns the applied delta**.

**Accepted, and it is better than my own proposal.** My `A2-C01…C07-1.0` §6 had me publishing
`FTDDDamageAppliedEvent` for hits on my enemies. A1's argument wins: *"One publisher means one
ordering, one dedupe and one place where 'exactly once' can be asserted."*

What I give up is real and worth naming: my enemy reaction code no longer receives the event from
a publisher it controls. It receives it from A1's stream. The consequence is that **my reaction
code must tolerate an event arriving after my actor's own state has moved on** — which is exactly
the contract, and it is more honest than having two publishers disagree about when a hit happened.

**One requirement I add (mine, not a dispute):** the delta I return from `ApplyDamage` must be
what appears in `Amount`. If A1 clamps after my return, `Amount` and my attribute write disagree
and the field stops being a fact. A1-R2 §5.3 says `Amount` is "the health actually removed, after
mitigation and clamping" — so the clamp is inside the application, before the return. **I am
recording the requirement, not disputing the design.**

### 5.4 Event scope — including the blocked/parried question the request highlights

The request asks directly: *"Agent 1 currently proposes an applied event for blocked and parried
outcomes even when no health is applied. State whether this event is semantically suitable for
your consumers, or whether a distinct resolution/outcome event and damage-applied event are
required."*

**My answer: the single event is suitable, and I do not want a second event. Here is the reasoning,
because the naive answer is the opposite.**

| Outcome | A1-R2 publishes | Is that semantically right for me? |
|---|---|---|
| `Applied` / `KillingBlow` / `WeakPoint` | yes, clamped `Amount` | **Yes** — the normal fact |
| `Blocked` | yes, `Amount` 0 (or guard-reduced), `PostureDelta` set | **Yes — and I need it** |
| `Parried` | yes, `Amount` 0 | **Yes — and I need it** |
| `Immune` | **no** | **Yes** — see §5.5 |
| `Miss` | **no** | **Yes** |
| Rejected / duplicate / out-of-window | **no** | **Yes — these are not facts** |

**Why a single event with an `Outcome` discriminator is better than two events, for my consumers
specifically:**

1. **My boss reaction is one decision, not two.** When the boss's heavy attack lands, the boss must
   know *what happened* — did it connect, was it blocked, was it parried — and react once. Two
   events means my code joins them by `RequestId` and needs to prove that exactly one arrived. That
   is a bug surface I do not want, and it is the same class of problem as two arbitration
   authorities.
2. **The parry reaction is timing-critical.** A parried boss must stagger and open a counter
   window. If parries arrive on a different stream from hits, my reaction ordering depends on two
   publishers' relative timing, which A1-R2 §5.4 correctly refuses to guarantee across sources.
3. **`Amount` 0 distinguishes it cleanly.** An event with `Outcome == Blocked && Amount == 0` is
   not a lie — it is a true statement that a hit occurred and no health was removed. The event
   name (`DamageAppliedEvent`) is the only awkward part, and that is a naming question, not a
   semantics one.

**So I require no second event.** My one recorded request, which is a naming matter for whoever
owns the Core type:

> **Proposed:** the event's payload should make `Amount == 0` impossible to read as "no hit
> occurred". `Outcome` already does this. I would support renaming the type to
> `FTDDDamageResolvedEvent` **if and only if** Agent 3 prefers it — and I would not block on the
> name. The semantics in A1-R2 §5.3 are correct as they stand.

### 5.5 `Immune` and `Miss` publishing nothing — the one case I check

`A1-R2` §5.3: `Immune` publishes **no** event, because "publishing an 'applied' fact for a
non-application is a lie in the event log".

**Accepted — with one check, which I ran.** My enemy needs to stop attacking into an invulnerable
player, or it looks broken. Can I observe immunity without an event?

| Immunity source | Observable by me? |
|---|---|
| `Status.Invulnerable` during a dodge | **Yes** — `Status.Invulnerable` is a MEAD-C tag (§5.1), and `ControlState`/`bLocked` are in C-02 |
| Any other immunity source | **Unknown** — none is named in MEAD-C, M1 v1.4, or my documents |

**Conclusion: for every immunity source that exists today, I can observe it, so no event is
required.** If a future design adds an immunity I cannot see, that is the trigger for a C-03
revision — not a reason to publish events for non-applications now. **I accept `Immune` → no
event.**

### 5.6 C-03 verdict

**AGREE.** Six roles separated and accepted, A1 exclusive arbitration confirmed, single publisher
accepted, event scope accepted including blocked/parried, `Immune`/`Miss` accepted as silent.
**No remaining technical objection to the A1-R2 text.**

---

## 6. C-04 — Stagger

**Reviewed:** `A1-R2` §6.1–§6.4. **Verdict: AGREE, with one condition on the tag inventory.**

### 6.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §6.2 R4-1 | `ETDDStaggerClass { Never, Always, OnPostureBreak, OnParryOnly }` preferred | **ACCEPT — see §6.2** |
| §6.2 | Default when absent = `Never` (degrades to non-staggering) | **ACCEPT** |
| §6.2 | Validator warns (not blocks) on `PostureDamage > 0 && Never` | **ACCEPT** |
| §6.2 | Bool is an acceptable fallback; code identical | **ACCEPT** |
| §6.2 | GAS effect excluded — inverts the required order | **ACCEPT, and it is a M1 v1.4 argument not a preference** |
| §6.3 R4-2 | `FTDDRecoveryCompletedEvent` as **notification only** | **ACCEPT — see §6.3** |
| §6.3 | Alternative: derive from `FTDDControlStateChangedEvent` and drop the new event | **ACCEPT — and this is my preference** §6.3 |
| §6.4 | Precedence `Dead > Cinematic > Stagger`, single winner | **ACCEPT — preserved exactly** |
| §6.4 | Health independent of control | **ACCEPT** |

### 6.2 `ETDDStaggerClass` — accepted, and it is what I asked for from the content side

`A1-R2` §6.2 prefers the four-value enum. **I accept it, and my reasoning is the content reason
rather than A1's structural one:**

`OnPostureBreak` is a **real Chapter 1 case**, not a hypothetical. `CH01-BOS-001`'s Great Root
Mother has a slam that should stagger **only if it breaks posture** — otherwise it is a heavy hit
that does not stagger. Under the bool I would have to choose `Always` (over-staggers: the player
is stunlocked by a routine attack) or `Never` (the posture break never pays off: the mechanic has
no consequence). **The enum is the only representation that expresses the design.**

`Default = Never` is correct for the same reason my own parser work has been careful about
defaults: **a missing classification must degrade toward "does nothing", never toward "does
something surprising".**

**I accept the bool as an acceptable fallback** and I will not block on it — but I state for the
record that if TD chooses the bool, `OnPostureBreak` is lost and the boss's slam becomes a design
compromise rather than a design.

### 6.3 Recovery notification — accepted, and I prefer the derivation

The request asks me to *"state whether you agree that recovery notification is informational only
and cannot create or mutate a control-state transition."*

**I agree, without qualification.** `A1-R2` §6.3 is precise: the event "carries no ability to
influence the transition, cannot be raised by a consumer, and is emitted strictly after the state
change is committed." **My consumption is read-only and has no write path.** It cannot become a
state authority because there is no mechanism by which I could make it one.

**Why I need it, restated from my A1-R1 review because it is unchanged and it is the `High` item:**
`CH01-BOS-001` phase 2 commits the boss to a 0.8 s punish then repositions. If stagger ends at
0.6 s, the boss is committed to 0.2 s of punish into a recovered player — an unfair hit the player
did not cause. Polling `bIsStaggered` cannot tell me **when** it became false, only that it is
false now, and my decision has already committed.

**My preference between A1's two options, stated because A1 offered the choice:**

I prefer **deriving from `FTDDControlStateChangedEvent`** with the rule
`OldState == Stagger && NewState ∈ {Locomotion, Idle}`, and **dropping `FTDDRecoveryCompletedEvent`**.

Reasons: it adds no Core surface for a convenience; it cannot ever disagree with the state change
because it *is* the state change; and it fires on every exit path automatically, including the
ones A1-R2 §6.3 lists. A dedicated event that fires only on some paths would be the same bug in
several places.

**This is a preference, not a condition.** If A1 or TD prefers the dedicated event, I will consume
it, provided it fires on **all four** exits from `Stagger` — timeout, lethal, cinematic,
supersession — not only timeout.

### 6.4 Precedence — preserved, and verified rather than trusted

The request requires `Dead > Cinematic > Stagger`. `A1-R2` §6.4 states it is a `CONFIRMED
DECISION` and preserves it with the single-winner rule, supersession logging, and no
downward override.

**I confirm it matches the TD requirement exactly** (100 / 90 / 80 in that order) and that A1-R2
adds no state and removes none. **No Agent 2 mechanism in this contract can violate it** — my only
influence is the `StaggerClass` and posture damage values my attacks carry, and neither can set a
control state.

### 6.5 The `Status.Dead` gap — my one condition

`A1-R2` §9.2's collision table discusses `Status.Staggered` at length. **It does not mention that
MEAD-C has no tag for `Dead`.** I checked:

| Tag | In MEAD-C §5.1 (7 tags) | In A1-R2's inventory | In my inventory |
|---|---|---|---|
| `Status.Staggered` | **yes** | yes | `Combat.State.Staggered` |
| `Status.Cinematic` | **yes** | **no** — dropped | `Combat.State.Cinematic` |
| `Status.Dead` / `Status.Died` | **no — does not exist** | **no** | `Combat.State.Dead` |
| `Status.Attacking`, `Status.Blocking`, `Status.Parrying`, `Status.Invulnerable`, `Status.Grabbed` | **yes** | **none of the five** | — |

**Two findings here, both of which need the registry owner rather than me:**

1. **`Dead` has no tag anywhere.** C-04's precedence is `Dead > Cinematic > Stagger`, and two of
   the three have MEAD-fixed tags while the third does not. That is not a naming preference — a
   precedence rule whose top entry is unrepresentable as a tag is a rule that cannot be written
   against in an AI condition. **I am not inventing `Status.Dead`.** It is raised as a registry
   item (§9.4, TD-08).
2. **`A1-R2`'s own inventory dropped five MEAD-fixed status tags** — `Attacking`, `Blocking`,
   `Parrying`, `Invulnerable`, `Grabbed`, and also `Cinematic`. Its R7-1 "Keep" list names only
   `Status.Interacting`, `Traversing`, `Airborne`, `LockedOn`. **A1-R2 §9.3 says it withdraws
   nothing**, yet six tags present in A1-R1's inventory are absent from A1-R2's. That may be
   deliberate compression to "the tags in dispute" rather than a withdrawal — **but it reads as a
   withdrawal and the reconciliation will record it as one unless A1 says otherwise.** I am
   flagging the ambiguity rather than assuming it.

**My condition on C-04: the tag inventory must be stated completely and consistently before C-04
can be signed as a version**, because `Dead` is part of the precedence and `Cinematic` is part of
both the precedence and my §4.6 decision. This is a registry question, not a C-04 semantics
question — **A1-R2's C-04 semantics are accepted in full.**

### 6.6 Tests

`A1-R2` §12.5 adds a recovery-notification case (+1) and retains the fourteen. **Accepted.** My
addition from the previous review stands and is unchanged:

| Proposed addition (mine) | Asserts |
|---|---|
| `TDD-Contract.World.StaggerRecoveryNotificationFiresOnEveryExit` | recovery fires on all four exits exactly once, each carrying an authoritative gameplay time from A1's clock |

### 6.7 C-04 verdict

**AGREE** on classification, default, fallback, precedence, health independence and recovery
notification. **One condition:** the tag inventory must be completed (`Dead` added by the
registry; the six MEAD-fixed tags' status clarified).

---

## 7. C-05 — Telegraph and gameplay clock

**Reviewed:** `A1-R2` §7.1–§7.4. **Verdict: PARTIALLY AGREE.**

The request calls this "a major unresolved disagreement". **It is no longer a symmetrical
disagreement: I concede the central point.** I then raise a defect in A1's model that is not the
point I originally argued, and it needs a TD ruling.

### 7.1 Why I concede — the arithmetic

My `A2-C01…C07-1.0` §7.3 said: *"`EndGameplayTime` is in **undilated** gameplay time; a dilated
window still ends at the same gameplay time."*

`A1-R2` §7.3 says a 100 ms hitstop would make my window end 100 ms of gameplay time early relative
to the animation. **A1 is right and the error is worse than A1 states.** Concretely:

| | My rule (undilated timestamps) | A1-R2's rule (scaled per-entity clock) |
|---|---|---|
| Attack active window as authored | 0.20 s of montage time | 0.20 s of montage time |
| Pair hitstop at 0.05× for 100 ms wall | montage continues at 0.05× | montage continues at 0.05× |
| When does the window close? | At **0.20 s of undilated time** = 0.20 s wall | After **0.20 s of montage time** = 4.0 s wall |
| How much of the active animation has played when it closes? | **5 %** | **100 %** |
| Player-visible result | Parry window closes almost immediately after the attack becomes active | Parry window spans the whole active animation |

**My rule desynchronises the window from the animation it was authored on.** MEAD-C §5.5 defines
hitstop as a dilation applied to *the pair of actors*, so the montage is dilated and the window
must dilate with it. **I withdraw the undilated rule. `A1-R2` §7.2's scaled accumulation is
correct for the pair case.**

This is correction #1 of five in §0.4, and it is the one I most want on the record, because I
argued the opposite position in my previous review and called it a fairness requirement.

### 7.2 The behaviour under each condition the request lists

| Condition | My old rule | A1-R2's rule | Which is right, and why |
|---|---|---|---|
| **World pause** | freeze | freeze (`DeltaWorld == 0`) | **Both agree.** A1-R2 §7.2's table is right |
| **Global time dilation** (cinematic 0.3×) | window ends at same gameplay time → window shorter in wall time than montage | window scales with montage | **A1-R2.** A cinematic that slows the montage must slow the window or the parry is unreadable |
| **Pair-specific hitstop** | desyncs (see §7.1) | scales for both participants identically | **A1-R2**, decisively |
| **Different attacker/defender dilation histories** | — | **per-entity clocks diverge** | **Neither — this is the defect** §7.4 |
| **Telegraph start** | producer stamps `StartGameplayTime` on its own clock | producer stamps on **its** `T_e` | A1-R2, provided the consumer can interpret it (§7.5) |
| **Telegraph end** | `EndGameplayTime` on undilated clock | on producer's `T_e` | A1-R2 for the same reason |
| **Parry-window evaluation** | overlap computed by subtracting undilated timestamps | **same-frame phase overlap**, never timestamp subtraction | **A1-R2, and this rule is stronger than mine** §7.7 |
| **Late subscription** | every message carries `StartGameplayTime`; consumer computes remaining | must not synthesise; overlap rule; query surface open | **Compatible** — both reject synthesis; A1-R2 adds the rule that prevents a stale pass |
| **Same-frame hit resolution** | — | parry evaluated on the frame the hit resolves | **A1-R2** — this is the only rule that cannot pass a frame late |

**Six of the eight conditions favour A1-R2 and I say so.** The two that do not are the same
defect, stated next.

### 7.3 The defect that remains: per-entity clocks are not comparable

`A1-R2` §7.2 defines:

```
T_e(n) = T_e(n-1) + DeltaWorldSeconds * PrimaryDilation * CustomDilation(e)
```

and §7.2's ownership rule: *"Agent 1 and Agent 2 both **read** `T_e` for their own entity."*

**That is correct for the pair-hitstop case, where both participants are dilated identically. It
breaks whenever attacker and defender dilations differ**, because then `T_attacker` and
`T_defender` measure different amounts of elapsed time, and a timestamp produced on one cannot be
compared with a timestamp read from the other.

A worked case, which is a real Chapter 1 situation rather than a hypothetical:

```
Enemy is staggered mid-windup -> its custom dilation is 0.05 (slow recovery tell).
Player is NOT dilated -> 1.0 (no pair was formed; the hitstop never applied).

wall t = 0.0     T_attacker = 0.00    T_defender = 0.00
wall t = 1.0     T_attacker = 0.05    T_defender = 1.00

Enemy opens a telegraph with StartGameplayTime = T_attacker = 0.05.
Player compares against its own clock T_defender = 1.00.

  elapsed = 1.00 - 0.05 = 0.95 s
  authored window = 0.20 s
  => player concludes the window closed 0.75 s ago
  => PARRY FAILS on an attack that is, in wall time, still in windup.
```

**This is not covered by `A1-R2` §7.2's pause/dilation table**, which assumes the pair is always
dilated together. It is a fairness bug of exactly the kind A1-R2 §7.3 warns about — and it appears
in the model A1 proposes to fix that warning.

**When does it bite?** Whenever enemy and player animation rates diverge without a pair hitstop:
enemy stagger recovery tells, a boss slow-motion telegraph, per-actor slowdown effects, and any
cinematic that dilates only one of the two. **A staggered enemy is the canonical case and Chapter 1
has one.**

### 7.4 Can A1-R2's clock be made compatible with my producer/consumer model?

**Yes — and it should be, because the scaled clock is right. The fix is small and it is inside
A1's own design.**

`A1-R2` §7.2 already separates `PrimaryDilation` (global) from `CustomDilation(e)` (per entity). The
defect is that the **telegraph timestamp is stamped from the producer's composite clock**, so the
consumer has to unwrap a ratio it cannot see. Two ways to fix it, and **I do not choose between
them — TD-06 does**:

**Option A — normalise the timestamp to a shared axis (my recommendation).**
Carry the timestamp in **uns­caled world-accumulated gameplay time** (`T_world`, with
`PrimaryDilation` applied, `CustomDilation` **not** applied), and carry the producer's
`CustomDilation` **as a field on the message**. The consumer converts:

```
remaining_montage_time = (End_axis - T_world_now) / CustomDilation(producer)
```

This keeps every property A1-R2 needs — the window still scales with the montage, because the
division by `CustomDilation` restores montage time — and it makes the timestamp interpretable by
any consumer regardless of its own dilation.

**Option B — publish both axes.** Send `StartScaled` and `StartUnscaled` plus the dilation factor,
so a consumer uses whichever axis its own clock speaks. More fields, same correctness, no division
in the consumer.

**What I will not accept is the current shape**, where `StartGameplayTime` is on the producer's
composite clock and the message carries no factor to convert it. That is the version that
produces the 0.95 s error above.

**And one rule I would keep from A1-R2 regardless:** parry must be evaluated as **same-frame phase
overlap**, never by subtracting timestamps (§7.7). With either option above, timestamps remain
scheduling and diagnostic data, not the parry test.

### 7.5 A1-R2's MEAD-C citations — verified, and they support the scaled clock

Because §0.1 nearly produced a false accusation, I traced every citation rather than assuming:

| `A1-R2` citation | Claim | Verified in MEAD-C? |
|---|---|---|
| §5.1 | 7 `Status.*` tags exist | **yes** — `Blocking, Parrying, Invulnerable, Staggered, Attacking, Grabbed, Cinematic` |
| §5.2 | `Damage.Physical.Slash` is the damage-type vocabulary | **yes** |
| §5.4 | attacker-driven damage pipeline diagram | **yes** — the exact diagram A1-R2 §10.9 discusses |
| §5.5 | hitstop is applied to the **pair**, "not global world time" | **yes** — and it directly supports A1-R2 §7.2's per-entity design |
| §4.5 | interaction verb is a tag | **yes** — MEAD-C §4.5 is "Interaction" |

**MEAD-C §5.5 is the strongest evidence for A1-R2's position and against mine:** *"`UTDDHitStopSubsystem`
applies a scaled time dilation to the **pair** of actors (not global world time)... Global time
dilation is reserved for cinematics and death, so a hitstop can never corrupt a cinematic's
timing."* A per-pair dilation with an undilated window is incoherent. **My rule could not have been
implemented against MEAD-C.**

### 7.6 What I need to sign C-05

| # | Requirement | Owner |
|---|---|---|
| 1 | Option A or B in §7.4, so a timestamp stamped by one entity is interpretable by another with different dilation | **TD-06** |
| 2 | Confirmation that the parry test is same-frame phase overlap and **not** timestamp subtraction | A1 — already stated, wanted in the contract text |
| 3 | Late-subscriber surface: event-only vs event + `GetActiveTelegraphs` | **TD** (A1-R2 U-07) |

**Everything else in C-05 I accept**: the four-message lifecycle, exactly-once close, the
pause/dilation/hitstop table, "telegraph ≠ damage", producer obligations 1–5, and all twelve
`TDD-Contract.Combat.TelegraphWindowConsumerSemantics` cases.

### 7.7 Tests

`A1-R2` §12.5 adds `TDD-Contract.Combat.ClockDilationAlignment` (drift ≤ 1 frame across 3
hitstops; pause freezes; resume preserves remaining duration). **Accepted.** I add one, which is
the case A1-R2's test does not cover:

| Proposed addition (mine) | Asserts |
|---|---|
| `TDD-Contract.Combat.AsymmetricDilationTimestampComparability` | With attacker `CustomDilation` 0.05 and defender 1.0, a telegraph opened by the attacker yields the same *remaining window* whether computed on the producer's clock or the consumer's, within 1 frame. **Fails against the un-normalised per-entity stamp** |

### 7.8 C-05 verdict

**PARTIALLY AGREE.** I withdraw my undilated-window rule entirely (§7.1) — A1-R2 is right and I
was wrong. I accept the scaled clock for pause, global dilation and pair hitstop. **I do not
accept the un-normalised per-entity stamp**, because §7.4's worked case shows it produces a parry
decision 0.75 s out. That needs TD-06, and both options I propose are inside A1-R2's own design.

---

## 8. C-06 — Interaction

**Reviewed:** `A1-R2` §8.1–§8.4. **Verdict: AGREE.**

### 8.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §8.2 R6-1 | `bWantsProgress` (default **false**); `TickInteract` only when true | **ACCEPT — this is my position as the default** |
| §8.2 | Progress stays entirely inside the router; world sees `Begin → (optional Tick) → End` or `Cancel` | **ACCEPT** |
| §8.2 | Router owns hold duration, progress integration, completion instant | **ACCEPT — TD-07 answered as I needed** |
| §8.2 | World owns legality and what completion means locally | **ACCEPT** |
| §8.3 R6-2 | Damage-interrupt **escalated**, not assumed; three implementations listed | **ACCEPT — see §8.4** |
| §8.4 | Completion fact vs progression grant: compatible direction, shape unresolved | **ACCEPT** |

### 8.2 Does `bWantsProgress` satisfy my original requirement?

**Yes, exactly.** My `A2-C01…C07-1.0` §8.4 said:

> *"My answer: begin/end/cancel only. The world object does NOT consume progress... If Agent 1
> requires the world object to observe progress, I will add a read-only
> `OnProgressChanged(float Normalised)` — but I am **not** proposing to become the timing
> authority."*

`A1-R2` §8.2 makes **begin/end/cancel the default** and progress **opt-in via `bWantsProgress`**.
That is my position adopted as the default, and the optional callback I offered is now the opt-in
path. **`TD-07` is answered, `A2R-12` is closed, and my disagreement from the previous review is
resolved — I withdraw it.**

The `bWantsProgress` default matters independently: it means an interactable that never thinks
about progress cannot accidentally become frame-rate dependent. That was my objection in the
A1-R1 review and it is now structurally prevented rather than merely agreed.

### 8.3 The end/cancel lifecycle, and what I must tolerate

`A1-R2` retains the `Begin` / optional `Tick` / `End(result)` **or** `Cancel(reason)` shape with
exactly-once terminal handling. **Accepted.** My obligations, restated because they are mine:

| Obligation | My implementation |
|---|---|
| Tolerate `Cancel` in the same frame as `Begin` | a tap followed by a stagger; my actor must not assume `Begin` owns a frame |
| Tolerate `Cancel` before any `Tick` | `bWantsProgress == false` is the common case |
| Never end the session myself; `End` is A1's call | I report completion of my local action, not session termination |
| Never grant progression on `End` | §8.5 |

### 8.4 Damage interruption — correctly escalated, and I state my position

The request: *"Do not assume damage interruption is already a TD decision."* **I do not, and
`A1-R2` §8.3 does not either — it escalates it.**

My position, stated as a design opinion rather than a decision:

**I support damage interrupting a hold.** A sustained action that survives being hit makes
"hold to read the memory fragment while being attacked" a viable defensive tactic, which is not a
design anyone authored. `A1-R2` §8.3's reasoning is the same and I agree with it.

**But I am not claiming it as a decision, and I am not relying on it in C-06.** My cancellation
handling is trigger-agnostic: whatever reason the router sends, my actor runs the same clean
shutdown. **So the ruling does not block my implementation** — it changes one branch in A1's
router. I state my preference and leave the decision to TD/design as the request and A1-R2 §8.3
require.

**What I will not do:** treat `Cancel(Damaged)` as guaranteed and write code that assumes it. If
the ruling goes the other way, my cancellation path is still correct.

### 8.5 Source destruction, unload, exactly-once completion

| Trigger | A1-R2 / my position |
|---|---|
| **Source destruction / stream-out** | `Cancel(TargetUnloaded)` — accepted; my actor unregisters on stream-out and A1 must not hold a session against an invalid pointer |
| **Forced-state interruption** | `Cancel(Staggered)` / `Cancel(Died)` / `Cancel(Cinematic)` **before** the state is entered — accepted, and the ordering is the contract |
| **Level transition** | `Cancel(LevelTransition)` before teardown, no session survives — accepted |
| **Exactly-once completion** | Router's `Idle → Begun → Terminal` with `ProtocolViolation` on misuse — accepted |
| **Progression grant** | **Neither router nor interactable grants.** The owning subsystem (`UTDDMemoryDirector`, `UTDDCampaignSubsystem`) evaluates the completion fact and grants idempotently, keyed on `InteractionId` |

**The grant rule, stated against the request's instruction** ("Do not allow an interactable to
grant progression merely because it was interacted with"): my interactables **report completion**
and never grant. `CH01-SUB-018 The Wayside Offering Place` and the `CH01-SUB-001` shrine both read
as "interact to receive", and the grant is keyed on `InteractionId` in the owning subsystem so a
second interaction is idempotent. **This is my obligation and I accept it.**

### 8.6 C-06 verdict

**AGREE.** `bWantsProgress` resolves my position and my previous disagreement is withdrawn;
damage-interrupt correctly escalated with my preference stated and not assumed; cancellation
matrix and exactly-once accepted; progression boundary accepted with my obligation named.
**No remaining technical objection to the A1-R2 text.**

---

## 9. C-07 — IDs and tags

**Reviewed:** `A1-R2` §9.1–§9.4. **Verdict: CLARIFICATION REQUIRED.**

### 9.1 Clause-by-clause

| Clause | Subject | Verdict |
|---|---|---|
| §9.1 | Three reasons C-07 cannot be revised by A1 alone | **ACCEPT — same three reasons I have** |
| §9.2 | Eight-row collision table | **ACCEPT with corrections** §9.3 |
| §9.2 | `Traversal.Capability.*` compatible, A2 defers correctly | **ACCEPT** |
| §9.3 R7-1 | Yield to MEAD on `Damage.Physical.*` and `Status.*` | **ACCEPT, with the `Dead` exception** §9.4 |
| §9.3 | Withdraw implied tag for tap/hold distinction | **ACCEPT — and I withdraw `Interaction.Mode` too** §9.5 |
| §9.3 | Keep telegraph reason **enum**, not tags | **ACCEPT** §9.5 |
| §9.3 | Keep `Traversal.Capability.*` five names | **ACCEPT** |
| §9.3 | Keep `Status.Interacting`, `Traversing`, `Airborne`, `LockedOn` | **ACCEPT as registry requests, not grants** |
| §9.4 | Eight required inputs before namespace approval | **ACCEPT — this is the right list** §9.6 |

### 9.2 Which collisions I accept, reject, or defer

The request asks me to identify, per proposed resolution, whether I accept, reject, or require the
registry owner to decide.

| Collision | A1-R2's proposed resolution | My answer |
|---|---|---|
| `Status.Staggered` vs my `Combat.State.Staggered` | **Yield to MEAD `Status.*`** | **ACCEPT — withdraw `Combat.State`** §9.4 |
| `Damage.Physical.*` vs my `Combat.Damage.*` | **Yield to MEAD `Damage.*`** | **ACCEPT — withdraw `Combat.Damage`** §9.4 |
| `Interact.Verb.*` vs my `Interaction.Verb.*`, and differing verb sets | "naming open" | **DEFER — registry owner** §9.5 |
| Telegraph cancel: enum vs `Telegraph.Cancel.*` tags | **A1 keeps the enum** | **ACCEPT A1's enum; withdraw my tags** §9.5 |
| `Traversal.Capability.*` | Compatible; names are A1's | **ACCEPT** |
| My `Traversal.State.Blocked/OneWay` | Would duplicate A1's outcome enum + `bOneWay` | **ACCEPT — withdraw** §9.5 |
| My `Interaction.Mode.Tap/Hold` | Float `HoldDurationSeconds` expresses it | **ACCEPT — withdraw** §9.5 |
| `NPC.Activity.*` (mine, not in A1's table) | Not addressed by A1 | **DEFER — registry owner** §9.5 |

**Net: I withdraw four namespaces and defer two.** That is a large concession and it is correct —
A1-R2 §9.2's analysis is better than my inventory, and four of my requests were either duplicative
or unexecutable against MEAD.

### 9.3 Where A1-R2's collision table needs correction

Three rows, and one of them is a factual error worth stating precisely:

**(a) `Status.Staggered` — A1-R2 is right and my namespace was wrong.** MEAD-C §5.1 fixes
`Status.Staggered`. My `Combat.State.Staggered` would create a second vocabulary for one concept.
**Withdrawn.**

**(b) `Damage.Physical.*` — A1-R2 is right, and my contents were unsourced.** MEAD-C §5.2 fixes
`Damage.Physical.Slash` etc. My `Combat.Damage.Slash/Impact/Root/Thunder` —

| My value | Source? |
|---|---|
| `Slash` | MEAD-C §5.2 has it as `Damage.Physical.Slash` |
| `Impact` | no source (MEAD-C has `Blocked` as an outcome, not a damage class) |
| `Root` | **no source** — I appear to have derived it from `The Root Way`, a *location name*, which is a category error |
| `Thunder` | no source; the canon rule is `CH05 white lightning only` — invoking it as a Chapter 1 damage class would be a canon error |

**`Root` and `Thunder` were invented.** That is the fifth instance in this project of me asserting
content without a source, and it is the same failure mode as `62 interactables`, `8 props`,
`CarryState` and `4 doors`. **Withdrawn in full; `Combat.Damage` is withdrawn, not mapped.**

**(c) `Status.Dead` — A1-R2's table omits that the tag does not exist.** §6.5 covers this. It is
not a collision; it is an absence, and neither agent may fill it.

### 9.4 My two withdrawals and the one gap I cannot close

| Namespace | Action | Reason |
|---|---|---|
| `Combat.State` (`Staggered`, `Cinematic`, `Dead`) | **WITHDRAWN** | `Staggered`/`Cinematic` exist in MEAD-C; `Dead` must be requested from the registry, not created by me |
| `Combat.Damage` (`Slash`, `Impact`, `Root`, `Thunder`) | **WITHDRAWN in full** | MEAD-C fixes `Damage.Physical.*`; two of my four values were invented and one invoked a Chapter 5 canon rule |

**But the `Dead` gap remains and it is not mine to close.** `Dead > Cinematic > Stagger` needs
`Dead` representable. I am requesting it **as a registry item, tagged to the feature that needs
it**, per MEAD-C §6.6's own rule ("new tags are proposed to the tag owner and land in
`DefaultGameplayTags.ini` with a comment naming the requiring feature"):

> **Registry request:** `Status.Dead` (or the registry owner's chosen spelling), required by C-04's
> forced-transition precedence, consumed by Agent 2 boss/AI reaction and Agent 1's state machine.
> Two of the three precedence values already have MEAD-fixed tags; this is the third.

**I am not creating it, not assuming the spelling, and not using it in any data until granted.**

### 9.5 Withdrawals, deferrals and what I keep

| Namespace | Action | Reason |
|---|---|---|
| `Interaction.Verb.*` (`Open`, `Take`, `Inspect`, `Climb`, `Listen`, `Read`) | **DEFER to registry owner** | Two spellings (`Interact.*` vs `Interaction.*`) and two different verb sets. I will not choose; the registry publishes one list and I author against it |
| `Interaction.Mode.Tap/Hold` | **WITHDRAWN** | A1-R2 §9.3 is right: `HoldDurationSeconds` (0 = tap) carries both the mode and the duration, and a tag cannot express 1.35 s |
| `Traversal.Capability.*` | **KEEP** | Names are A1's; five values; accepted |
| `Traversal.State.Blocked/OneWay` | **WITHDRAWN** | Duplicates A1's query-outcome enum and its authored `bOneWay` flag |
| `Telegraph.Cancel.*` tags | **WITHDRAWN** | A1-R2's enum gives compile-time exhaustiveness; my tags gave nothing an enum cannot |
| `NPC.Activity.*` (`Cook`, `Farm`, `Weave`, `Hunt`) | **DEFER to registry owner** | My request; sourced from routine data in `WORLD_ARCHITECTURE` §5.2. A1-R2 does not address it. Not urgent: no code exists |
| `World.Access.*` (`OpenExterior` etc.) | **DEFER to registry owner** | Derived from register access vocabulary, already parsed in `population_policy.json`. A1-R2 §9.4 item 8 correctly says whether it must be a *tag* is a governance choice |

**Four withdrawn, two deferred, one kept, one requested (`Status.Dead`).** My original nine-row
inventory reduces to four live items and none of them is contested between the agents.

### 9.6 The three-MEAD divergence blocks namespace resolution — TD-12

A1-R2 §9.3 says "yield to MEAD" and cites MEAD-C's namespaces. **That instruction is correct and
unexecutable**, because "MEAD" is three documents:

| | MEAD-A (my tree) | MEAD-B (packet) | MEAD-C (A1's branch) |
|---|---|---|---|
| `Status.*` vocabulary | **none** | **none** | **7 tags** |
| `Damage.*` vocabulary | **none** | **none** | `Damage.Physical.Slash` |
| §5.4 damage pipeline | **absent** | **absent** | **present** |
| §5.2 is… | "Project settings" | "Combat and damage" | "Attack data model" |

**A2 and A1 cannot both "yield to MEAD" if we are reading different MEADs** — and today we are.
Every namespace decision in C-07 depends on which one is canonical, and so does `TD-09` (MEAD §5.4
exists only in C).

**Raised as TD-12** (§11). It is a documentation-identity question, not a design question, and it
is the cheapest unblock in this review: **declare one file canonical, archive the other two.**

### 9.7 Interactable identity — still unresolved, still not invented

Unchanged from my previous review, restated because the request requires it:

| Question | Answer |
|---|---|
| How many interactables exist in Chapter 1? | **Not established.** No source enumerates them |
| Do any save references point at an interactable? | **Unknown** — no save schema, no save content |
| Do interactables need identity beyond actor lifetime? | **Unknown**, and it depends on the previous row |
| Does any interactable have persistent state (a shrine that stays lit)? | **Plausibly**, but not in a source I can cite |

**I do not recommend a namespace and I do not create one.** `A1-R2` §9.4 items 3–4 name the same
blockers from its side, and §11's U-11 agrees. **Raised as TD-13.**

### 9.8 C-07 verdict

**CLARIFICATION REQUIRED.** I accept A1-R2's collision analysis and its two central "yield to MEAD"
resolutions, and I withdraw four of my own namespaces and defer two. **C-07 cannot be agreed by
either agent until three things exist: one canonical MEAD (TD-12), a named registry owner with a
published namespace list, and the save inventory (TD-13).**

---

## 10. MEAD §5.4 authority — the six roles

### 10.1 Do I agree with A1's six-role separation?

**Yes, in full.** `A1-R2` §10.9 separates authorship, detection, arbitration, defence, application
and publication, and assigns each an owner. I checked each against my own position:

| Role | A1-R2 owner | My agreement |
|---|---|---|
| **1. Attack authorship** | A2 for enemies, A1 for player | **Agreed** — authorship confers no arbitration |
| **2. Hit detection** | **A1** for every hit involving the player | **Agreed**, and stronger than my original submission (§5.2) |
| **3. Arbitration / resolution** | **A1 exclusive** | **Agreed** — no second arbiter |
| **4. Defence / mitigation** | **A1 exclusive** for the player as victim | **Agreed** — I must not evaluate the player's defence |
| **5. Health / attribute application** | Target's owner: A1 for player, A2 for own actors, **only after (3) authorises** | **Agreed** |
| **6. Applied-event publication** | **A1, single publisher** | **Agreed**, accepting that I lose my own publisher (§5.3) |

### 10.2 Do I confirm Agent 2 does not arbitrate hits involving the player?

**I confirm it.** Explicitly and as a commitment:

> **Agent 2 supplies enemy attack intent and authored data. Agent 2 does not arbitrate, resolve,
> classify, mitigate or apply any hit involving the player. Agent 2 does not detect overlap against
> the player. Agent 2 writes health only for its own actors, only after Agent 1's arbiter
> authorises the application, and it returns the applied delta rather than publishing an event.**

This supersedes my `A2-C01…C07-1.0` §6 in one respect: **my original submission had me running the
overlap trace and sending the result.** `A1-R2` role 2 makes detection A1's. **I accept that and
withdraw my detection role** — it is the correct split and it removes a frame-ordering question.

### 10.3 MEAD §5.4's ambiguity — the exact wording that needs an erratum

The request asks me to identify the precise wording if §5.4 remains ambiguous. **It does, and here
is the exact text from MEAD-C §5.4:**

```
Attacker CombatComponent
  -> FTDDAttackHitOutcome
  -> FTDamageRequest { InstigatorId, TargetId, RawDamage, DamageType, HitLocation,
                       OutcomeType, bCritical, SourceAttackId }
  -> ITDDDamageable::ApplyDamage(FTDDamageRequest)   [Core interface]
     -> victim's UTDDCombatComponent (or boss/AI controller for non-pawn damageables)
        -> if Blocked: reduce by guard, drain posture
        -> if Parried: apply attacker stagger, no health loss
        -> else: GAS GameplayEffect (damage) -> AttributeSet -> OnHealthChanged
        ...
  -> FTDDDamageAppliedEvent published on the bus
```

**Two specific ambiguities in this diagram:**

1. **`OutcomeType` is an input to `ApplyDamage`, and the branch decisions (`Blocked`, `Parried`)
   are made *inside* the victim after that input arrives.** Read literally, the *attacker* supplies
   the outcome and the victim acts on it. That is the opposite of arbitration: it makes the
   attacker's classification authoritative. Under the six-role split, `OutcomeType` cannot be an
   input to defence evaluation — it is the *result* of it. **This is the wording that needs the
   erratum**, more than the arrow direction does.
2. **The pipeline is drawn as one flow with no owner boundary.** It does not say who runs it. For
   the player as attacker, A1 runs all of it, so the diagram is accurate. For the player as victim,
   the diagram implies the enemy's `CombatComponent` initiates and the player's component branches
   — two code paths, which is exactly the two-arbiter problem.

**My proposed erratum, for TD-09 (a) in A1-R2 §10.9:**

> **§5.4 erratum:** This diagram describes **authorship and initiation**, not arbitration
> authority. `OutcomeType` on `FTDDDamageRequest` is **advisory attacker-side input** and is
> **re-derived** by the victim-side arbiter; it is never accepted as the outcome. For any hit in
> which the player is the victim, arbitration, defence evaluation and mitigation are Agent 1's
> alone; the attacker submits intent and authored data only, and receives the applied event.
> The diagram's arrow into `ITDDDamageable::ApplyDamage` denotes an authorised application call,
> not an attacker-controlled entry point.

**This is the single most important documentation change in this review**, because a reader
implementing from MEAD-C §5.4 alone would build the `OutcomeType`-as-input shape and would produce
two arbiters. I agree with A1-R2 §10.9 that the diagram should be **annotated, not deleted** — the
authorship flow it draws is correct and useful.

### 10.4 Do I introduce a second arbitration authority?

**No.** `A2-C01…C07-1.0` §6 never proposed one, this review does not propose one, and §5.2 states
my side as a written commitment. There is **one** arbiter for hits involving the player and it is
Agent 1's.

---

## 11. TD items — A1-R2's nine, plus two new

### 11.1 A1-R2's nine items, reviewed

| A1 item | A1-R2 status | My review |
|---|---|---|
| **TD-01** v1.2 visibility | **CLOSED** | **AGREE with the closure.** v1.2 exists at `e121bbb`; A1's §0.2 error is the same class as mine in the previous submission. Closed as a visibility fact on both sides |
| **TD-02** stagger representation | Preference stated, decision **OPEN** | **AGREE with the preference (enum B)** and with the fallback. My content reason: `OnPostureBreak` is a real CH01 case (§6.2) |
| **TD-03** applied-event scope | Position complete, ruling needed | **AGREE with the position in full** (§5.4). I want no second event. Two items for TD: blocked/parried-as-applied-event, and A1 as sole publisher for my targets — **I support both** |
| **TD-04** RouteId stability/save | **CLARIFIED** | **AGREE with the clarification**, and it exposes P3's self-contradiction (§3.5). No A1 save field references a route; my side agrees |
| **TD-05** stealth/noise | **CONFIRMED excluded** | **AGREE.** No approved design, no consumer. Revisit condition in A1-R2 §10.5 is right |
| **TD-06** gameplay clock | Proposed, **divergence recorded** | **PARTIAL.** I withdraw my undilated rule (§7.1) — the divergence A1-R2 §7.3 records is now one-sided and resolved in A1's favour. **What remains is the asymmetric-dilation defect** (§7.4), which is a new question |
| **TD-07** interaction progress | **CLARIFIED**, friction removed | **AGREE.** `bWantsProgress` resolves `TD-07` and my `A2R-12` |
| **TD-08** tag namespaces/retirement | Eight inputs listed | **AGREE with the list**, and I add that the three-MEAD divergence (TD-12) blocks item 1 |
| **TD-09** MEAD §5.4 | **Resolved by role separation; concern maintained** | **AGREE with the role separation and with maintaining the concern.** §10.3 gives the exact erratum text |

**My verdict on A1-R2's nine: 7 agreed as closed/positioned, 1 partial (TD-06, resolved in A1's
favour on the original question), 1 agreed with an addition (TD-08).**

### 11.2 A1-R2's sixteen answers to my dependency items

| # | My item | A1-R2 answer | Accept? |
|---|---|---|---|
| 1 | Capability enum and names | five names | **Yes** |
| 2 | Requirements data or code | **data** | **Yes** |
| 3 | Cumulative vs independent; revocable | independent; per-query; no mid-execution abort | **Yes** |
| 4 | Water/rope context | out of slice | **Yes**, with the scope consequence (§3.4) |
| 5 | C-02 field list | health/posture removed; `CarryState` not provided | **Yes** — and I concede `CarryState` |
| 6 | Event-vs-query split | both; scoring-vs-commit adopted | **Yes** |
| 7 | Applied event payload | full payload, clamped `Amount` | **Yes** |
| 8 | Resolution not published as fact | confirmed | **Yes** |
| 9 | Target-unload drop | accepted | **Yes** |
| 10 | Outcome event shape / `ResolutionId` | no `ResolutionId`; correlate on `RequestId`/`HitEventId` | **Yes** |
| 11 | Recovery event | yes, notification only | **Yes**, preferring the derivation (§6.3) |
| 12 | Gameplay time and pause | proposed clock; **dilation still diverges** | **PARTIAL** — the divergence is now mine to concede (§7.1), but a new defect emerges (§7.4) |
| 13 | `CancelReason` vocabulary | six close reasons, enum preferred | **Yes**, withdraw my tags |
| 14 | `ITDDInteractable` final shape | extended; progress opt-in | **Yes** |
| 15 | `CanInteract` frequency | once per router tick, focused candidate only | **Yes** |
| 16 | Traversal capability tags | five requested | **Yes** |

**15 accepted, 1 partial.** A1-R2 answered my entire dependency list.

### 11.3 Two new items

| ID | Issue | Why it blocks | Needed from |
|---|---|---|---|
| **TD-12** | **Three divergent documents all identify as `TDD-MEAD-001` v1.0** (§0.1): MEAD-A `Docs/00_…` (1,078 lines, no §5.4), MEAD-B `docs/MASTER_ENGINEERING_ARCHITECTURE.md` (247 lines), MEAD-C `docs/01_ARCHITECTURE/…` (1,231 lines, §5.4 present, 7 `Status.*` tags). §5.4 exists only in C; the tag vocabularies exist only in C | C-07 says "yield to MEAD" — unexecutable when MEAD is three documents. TD-09's §5.4 erratum cannot be applied to a specific file. Every namespace decision depends on which is canonical | **TD**: declare one canonical file, archive the others, and state which commit the canonical version is at |
| **TD-13** | **Interactable identity and persistence** (§9.7): does the vertical slice persist interactable state across level transition and save? | No interactable id policy can be chosen without it, and neither agent may invent one. A1-R2 §11 U-11 agrees | **TD**: state yes/no, or "deferred"; a deferred answer also unblocks |

### 11.4 What I am not asking the TD to decide

- Not the C-05 clock design — I concede the model and propose a fix inside it (§7.4).
- Not the C-03 event scope — I give a position and no contest (§5.4).
- Not the C-06 damage-interrupt rule — escalated by A1-R2, preference stated, not relied on (§8.4).
- Not any tag name — I withdraw four namespaces and defer two rather than choosing (§9.5).
- Not whether `A1-R2` is competent. It is, and this review concedes the two largest technical
  points in it.

---

## 12. Where the two submissions stand

### 12.1 The trajectory, stated honestly

| | A1-R1 review | This review |
|---|---|---|
| Contracts agreed | 0 | **0** |
| Contracts with no remaining technical objection | 0 | **3** (C-02, C-03, C-06) |
| Contracts with one narrow condition | 0 | **2** (C-01, C-04) |
| Contracts with a substantive unresolved issue | 7 | **1** (C-05) |
| Contracts that cannot be agreed by either agent | 1 (C-07) | **1** (C-07) |
| My own positions withdrawn | 5 | **5** |

**This is real convergence and I am not going to pretend otherwise.** Two reviews ago I rejected
A1's route format; A1 withdrew it and stated properties, and I accepted the properties. I rejected
`TickInteract`; A1 made progress opt-in, and that was my position. I disputed the clock; **I was
wrong and I have withdrawn it.**

### 12.2 What is genuinely left

1. **C-05 asymmetric dilation** (§7.4) — a real defect with two fixes, needing TD-06.
2. **C-07's three blockers** (§9) — MEAD canonicality (TD-12), a registry owner, save inventory
   (TD-13).
3. **`Status.Dead`** (§6.5) — a registry request, not a design question.
4. **C-01 P3's self-contradiction** (§3.5) — fixable by A1 without anyone else.

**Four items. Three of them are not design disagreements at all** — they are a documentation
identity question, a missing registry owner, and a missing tag. Only C-05 is a technical dispute,
and it is narrower than the one this review was commissioned to resolve.

### 12.3 What I need from Agent 1 to sign

| # | Need | Contract |
|---|---|---|
| **A2R-17** | Restate P3 so it does not contradict §10.4 | C-01 |
| **A2R-18** | Confirm `StartGameplayTime` will carry a normalisation axis or the producer's dilation factor (§7.4 option A or B) — or state why the asymmetric case cannot occur | C-05 |
| **A2R-19** | Confirm the parry test is same-frame phase overlap, not timestamp subtraction, in the contract text | C-05 |
| **A2R-20** | Clarify whether the six MEAD-fixed `Status.*` tags absent from A1-R2's inventory were withdrawn or merely omitted from the table | C-04, C-07 |
| **A2R-21** | Confirm `ApplyDamage` returns the clamped applied delta so `Amount` is a fact | C-03 |

**Five items, all narrow.** None is a redesign.

---

## 13. Evidence

### 13.1 Executed — my own checks and tests, run in this session

| Command | Result | Exit |
|---|---|---|
| `python3 Tools/world/contract_data_checks.py` | **9/9 passed** | **0** |
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_submission.py"` | **23 OK** | **0** |
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_review.py"` | **43 OK** | **0** |
| `python3 -m unittest discover -s Tools/canon/tests` | **114 OK** | **0** |
| `python3 -m unittest discover -s Tools/world/tests` | **337 OK** | **0** |
| `python3 Tools/ci/l0_checks.py` | **14/14** | **0** |
| `python3 -m unittest discover -s Tools/world/tests -p "test_contract_review_r2.py"` | **38 OK** | **0** |
| `python3 Tools/world/gen_evidence.py` | **13/13** | **0** |

**These test my submission and my prior review. None tests A1-R2 and none is a contract acceptance
test.**

### 13.2 The five evidence categories, kept separate

| Category | Count | Executed? |
|---|---|---|
| **(a)** Independent data checks (`contract_data_checks.py`) | **9** | **Yes**, §13.1 |
| **(b)** Document tests, submission (`test_contract_submission.py`) | **23** | **Yes**, §13.1 |
| **(c)** Document tests, prior review (`test_contract_review.py`) | **43** | **Yes**, §13.1 |
| **(d)** Proposed contract acceptance tests (both agents) | **A1-R2: 7 suites + 4 new cases/cases; mine: 42** | **No — 0 run** |
| **(e)** Repository suite | canon 114, world 337, L0 14/14 | **Yes**, §13.1 |
| **(f)** Analysis queries for *this* review | **11** | **Yes**, but **not tests** — §13.4 |
| **(g)** New review tests locking this document's claims | **38** (`test_contract_review_r2.py`) | **Yes**, §13.1 |

### 13.3 What A1-R2 claims and what it actually ran

`A1-R2` §12.5 states: *"**Executed: none. Zero tests, zero builds, zero runtime checks in this
document and in `A1-R1`.**"*

**That is accurate and I take it as stated.** A1-R2 ran nothing. My §13.1 ran only my own Python.

**I did not rerun any A1 test** — none exists to run, and none of A1's tests is implementable
against anything in this workspace. **Agent 3 did not rerun my tests either** (recon v2.0 §7 says
so explicitly), and this review makes no claim otherwise.

### 13.4 The eleven analysis queries run for this review

None of these is a test. §13.5 states what each would need to become one.

| # | Query | Finding |
|---|---|---|
| 1 | Locate all files identifying as `TDD-MEAD-001` across all reachable refs | **three divergent MEADs** (§0.1) |
| 2 | Test each MEAD for `§5.4`, `Status.*`, `Damage.*`, `ITDDDamageable`, `FTDDDamageRequest` | only MEAD-C has them |
| 3 | Trace each A1-R2 MEAD citation to a section in MEAD-C | all 5 verified (§7.5) |
| 4 | Extract MEAD-C's 7 `Status.*` tags | `Status.Dead` **absent** (§6.5) |
| 5 | Compare A1-R2's inventory against MEAD-C's fixed set | 6 MEAD tags missing from A1-R2 (§6.5) |
| 6 | Check my submission's `CarryState`/`Combat.Damage`/`Root`/`Thunder` sourcing | **no source** (§4.5, §9.3) |
| 7 | Compute the dilation divergence at 0.05× (mine) | window closes at 5 % of animation (§7.1) |
| 8 | Compute the asymmetric-dilation timestamp error | 0.75 s parry error (§7.3) |
| 9 | Confirm the 8 traversal-capable locations and 4 scene-less ones | unchanged from prior review |
| 10 | Enumerate the 42 acceptance test IDs by layer | 42 unique, 10/11/21 |
| 11 | Verify A1-R2's 16 dependency answers are complete | 16 present, 15 accepted |

### 13.5 Findings that are not yet tests

| Finding | Would become a test by | Exists? |
|---|---|---|
| Three divergent MEADs (§0.1) | A repo check asserting exactly one file carries `Document ID: TDD-MEAD-001` | **No** |
| `Status.Dead` absent (§6.5) | A registry-completeness check over the precedence set | **No** |
| Asymmetric-dilation error (§7.3) | A unit test with two clocks at different dilations | **No** — no clock exists |
| `CarryState`/`Root`/`Thunder` unsourced (§4.5, §9.3) | A claim-to-source checker over my tag inventory | **No** |
| 4 scene-less traversal locations (§3.4) | Already tested — `TestSceneGapForTraversalLocations` | **Yes**, 43 tests |

**I am not claiming the first four are tested.** They are analysed.

### 13.6 Preserved, unmodified

| Item | Status |
|---|---|
| 57/57 Chapter 1 location capture, provenance to register v2.9 (Drive `1E-PPUQh-…`, 534,140 bytes) | **preserved**, register **not modified** |
| `A2-C01…C07-1.0`, commit `3ac438b` | **preserved unchanged** |
| `AGENT2_REVIEW_A1R1_V1.md`, commit `93b2f07` | **preserved unchanged** |
| Withdrawn interactable/prop totals | **still withdrawn**; no count stated anywhere in this document |
| `Status.*` / `Damage.*` / `CarryState` / `Interaction.Mode` / `Traversal.State` / `Telegraph.Cancel` tags | **withdrawn this review** (§9.5) — plus `Combat.State` and `Combat.Damage` |

**No interactable or prop count appears in this document.** No canon register was altered. No
namespace was created or assumed granted.

---

## 14. Method, limits, and what this does not establish

### 14.1 What this does not establish

| Not established | Why |
|---|---|
| That any contract is agreed | §1.3 — 0 of 7; A1-R2's own `UNRESOLVED` items sit inside them |
| That A1 accepts anything here | A1 has not seen this document |
| That TD accepts anything here | v1.2 predates it |
| That any contract test passes | 0 run; no implementation exists |
| That the C-05 fix works | It is an arithmetic argument, not a measured result |
| That M0 is complete | no `.uproject`, no `Source/`, no build |
| That the environment is viable | C-10 unchanged; production host unknown |

### 14.2 Limits of the C-05 argument specifically

§7.4's worked case is **arithmetic on A1-R2's stated formula**, not a measurement. It shows the
two clocks differ by the dilation ratio; it does not show what A1's implementation would do,
because no implementation exists. **If A1's real design already normalises — for instance if
`StartGameplayTime` is defined on a shared axis and only *durations* are scaled — then the defect
does not exist and I would withdraw §7.4 on the spot.** `A2R-18` asks precisely that, and it is
phrased so that either answer closes the item.

### 14.3 The correction record

| # | What I got wrong | Who/what found it | Section |
|---|---|---|---|
| 1 | **C-05 "undilated window" is defective** — desynchronises the window from the animated montage | **A1-R2 §7.3's arithmetic**, supported by MEAD-C §5.5's pair-hitstop definition | §7.1 |
| 2 | `CarryState` marked `REQUIRED` with no source | the request's explicit test; my own check found no register/scene/design basis | §4.5 |
| 3 | `Combat.Damage.Root`/`Thunder` invented | checking my own inventory against MEAD-C | §9.3 |
| 4 | `Combat.State.*` and `Interaction.Mode` and `Traversal.State` and `Telegraph.Cancel` duplicative | **A1-R2 §9.2/§9.3's analysis** | §9.5 |
| 5 | `CameraForward` requested for a decision `AimDirection` already serves | reviewing my own consumer list | §4.3 |
| 6 | Nearly asserted A1 fabricated its MEAD citations | **my own all-refs search before publishing** — MEAD-C exists | §0.1 |

**Four found by A1-R2, two by my own checking.** I note which, because a review that presents every
concession as voluntary generosity is not trustworthy.

### 14.4 The procedure I changed after making the same error twice

Previous review: I claimed v1.2 did not exist; it existed at a commit I had not fetched.
This review: I nearly claimed A1's MEAD citations were fabricated; the cited document existed on a
branch I had not fetched.

**The procedure, now applied, and it is what saved this review from a false accusation:**

1. Before asserting any document is absent, **search every reachable ref and commit** for its
   identity string (`Document ID:`), not its path.
2. Fetch the other agents' branch tips explicitly (`git ls-remote`, then fetch refs by name) rather
   than assuming my default refs are complete.
3. When two documents claim the same ID and version, **treat that as a finding**, not as noise.

**I record this as a process correction, because twice is a pattern and the second time I caught it
only by luck of doing step 1 before writing.**

---

## 15. Publication

### 15.1 Provenance

| Field | Value |
|---|---|
| Document | `Docs/AGENT2_REVIEW_A1R2_V1.md` — **new file** |
| Branch | `arena/5dde91a4-tdd` (existing; no new branch, no merge) |
| Reviewed A1 version | `A1-R2` v1.1, commit `f578fe612ad173b74f99fcb187f825eb3de6f59a` |
| My submission | `A2-C01…C07-1.0`, commit `3ac438b32fcd73ceb22dcd81385356f7b8b39644` — **unchanged** |
| Prior review | `TDD-A2-REVIEW-A1R1-001` v1.0, commit `93b2f07` — **unchanged** |
| Governing TD version | v1.2, commit `e121bbbf09562e3cba0efe81aad971809685db23` |
| Reconciliation | v2.0, commit `d32660fee1b0234871b39b9fa56677c7cf62f28f` |
| MEADs located | A `Docs/00_…` 1,078 lines; B `docs/MASTER_…` 247 lines; C `docs/01_ARCHITECTURE/…` 1,231 lines (A1 branch `b9ab305`) |
| Code, Core types, project | **none created** |
| Merge / API freeze / M0 claim | **none** |
| Contracts marked `AGREED` | **0** |

### 15.2 Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Formal review of `A1-R2` v1.1 against `A2-C01…C07-1.0` and TD v1.2. Seven verdicts (3 agree, 2 agree-with-condition, 1 partially, 1 clarification); 61 clause verdicts (56 accepted, 5 accepted with a named condition, 0 rejected), 2 namespaces deferred; **five positions of my own withdrawn**, including the C-05 undilated-window rule; 15 of A1-R2's 16 dependency answers accepted; two new TD items (TD-12 three-MEAD divergence, TD-13 interactable persistence); five new requirements on A1 (A2R-17…21); six corrections recorded with attribution; evidence split into six categories with 9 checks, 23 + 43 tests and 0 contract tests executed. |

**This document is a review, not a contract.** It agrees nothing, freezes nothing, and authorises no
implementation.
