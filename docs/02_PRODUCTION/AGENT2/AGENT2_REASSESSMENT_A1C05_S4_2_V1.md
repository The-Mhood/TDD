# AGENT 2 — INDEPENDENT REASSESSMENT OF `A1-C05-S4.2` v4.2

**Review ID:** `TDD-A2-REASSESS-A1C05-S4-2-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — nothing is signed, frozen or merged; no implementation is
authorised; **no MEAD has been selected**; no M0 claim is made. **C-05 and U-07 remain open.**
**Outcome:** **`PASS WITH CONDITIONS`** (§11).

Two conditions block a clean `PASS`. Neither is a defect in how the contract assigns work; both are
instrument and provenance defects, and both are narrow. **Every one of my previous findings is
closed on the text.**

---

## 0. Verdict summary

| | Count |
|---|---|
| Previous findings and conditions reassessed | **17** |
| Closed, verified against the text | **15** |
| Closed with a recorded caveat | **2** |
| Still open | **0** |
| **Newly introduced defects** | **2** — both instruments, neither normative |
| Overall | **`PASS WITH CONDITIONS`** |

**The two blocking conditions:**

| # | Defect | Class | Why it blocks |
|---|---|---|---|
| **N-1** | `DV-22`'s whole-document scan is a keyword whitelist with a **false-negative escape hatch** | `PASS-BLOCKING` | The instrument added to close D-22-scope does not detect the class it was built for. I demonstrate a live false negative in §7.1 |
| **N-2** | **Two incompatible documents** carry the identifier `TDD-A1-C05-SUCCESSOR-004.2` on two branches, differing in what `TN-C-14` measures | `PASS-BLOCKING` | Provenance. A reader citing "S4.2" does not know which contract they are citing (§8) |

**Everything else is closed, including all of D-4, D-1a, D-1b, C4c-N1, D-6a, D-6a-i, D-6b.**

---

## 1. Exact target verification

Verified **before** reading the document, and re-verified after writing this review.

```
$ git rev-parse a788f953256d208f3eb1310f3897924d007179b1:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md
7d03e1df837493305831962f43882a1cd3496143          <- matches the instruction exactly
```

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` |
| **Reviewed blob** | **`7d03e1df837493305831962f43882a1cd3496143`** |
| **Publishing commit** | **`a788f953256d208f3eb1310f3897924d007179b1`** |
| Lines | 1,265 · 184,226 bytes |
| Branch containing it | `origin/arena/3bc206a0-tdd` |
| Provenance register (at tip `d1d9ac9`) | blob `68c1cd713228e901a2c45fc7840957a0e1930386` — the **repointed** register; the register blob *at* `a788f95` was `eda9bd26…` and still pinned the first draft |
| Predecessor | S4.1 `d54e194a…` at `95918268…` — **verified unmodified** |

**I reviewed the blob, not the branch tip.** The tip is `d1d9ac9` and its `V4_2.md` blob is the same
`7d03e1df`, so the distinction is immaterial *for this document* — but I did not assume that (§1.1).

### 1.1 Publication chain — read from commit metadata, not assumed

| Commit | Time (UTC) | Event |
|---|---|---|
| `1647942` | 18:36:32 | S4.2 text published — blob `86f56af` |
| `7248cf2` | 18:36:42 | provenance register published, still naming `86f56af` |
| **`a788f95`** | **18:36:59** | **three sentences corrected → blob `7d03e1df`; register repointed** |
| `d1d9ac9` | 18:37:11 | register **repointed** to `7d03e1df` (the register blob committed at `a788f95` still named `86f56af`) |

**`a788f95` is not the first S4.2 commit; it is a follow-up correction.** I verified what it changed
rather than assuming it was cosmetic:

```
$ git diff 86f56af 7d03e1df  ->  3 insertions, 3 deletions
  -Agent 2's reassessment ... (595 lines)  +  (594 lines)   x2
  -The S3 refusal standed, unchanged        +  The S3 demonstration stands, unchanged
```

Three sentences: one typo, and a **line-count correction about my own review** (594, not 595 — my
review is 594 lines, which the register got right where the first draft did not). No clause, count,
test or validation result changed. **The correction is real and correct.**

### 1.2 The instruction says "Do not review ... an earlier S4.2 publication"

I therefore confirm explicitly: **`86f56af` (at `1647942`) is not the reviewed object**, and no
finding in this review is derived from it. I read it only to establish §1.1's chain.

---

## 2. Method, and what these checks are

I read all 1,265 lines. Beyond reading, I ran five kinds of check:

| Kind | What it establishes |
|---|---|
| **Text re-derivation** | Every count, tally and table re-parsed from the reviewed blob rather than read off Agent 1's summary |
| **Independent re-implementation** | `DV-11`'s rule and the `TN-C-14` bound re-implemented from their stated definitions |
| **Bound analysis** | 400,000-case brute-force search over legal pull schedules for the staleness bound |
| **Executed validator** | Agent 1 now ships `docs/validation/dv_c05.py`; I ran it on **this blob and on S3/S4.0/S4.1** |
| **Falsification injection** | Mutated documents to test whether the new instruments actually fire |

**What none of this establishes.** No contract behaviour is exercised. **0 of 67 acceptance cases
have been executed** — not by Agent 1, not by Agent 3, not by me. All 67 remain `PROPOSED / NOT RUN`.
Every "PASS" in this document is a statement about **text**, never about a telegraph, a producer, a
consumer, a directory or an engine. There is no C++, no Unreal project, no GPU and no runtime.

This distinction is load-bearing and S4.2 makes it itself (§13.4: *"It does not prove the contract is
correct, implementable or agreed, and no acceptance test has been run"*). I record that the
disclosure is honest and correctly scoped.

---

## 3. Finding-by-finding disposition

Vocabulary: **AGREE** · **AGREE WITH CONDITIONS** · **DISAGREE** · **NOT VERIFIED**.
"Closed" means the defect no longer exists in the reviewed blob, verified against the text.

### 3.1 D-4 / C6-2 — audio ownership · **AGREE — CLOSED**

**§8 preamble (line 624); §5.2 row 5; §6.1; `TN-C-15`; `DV-22`.**

S4.1's defect was §8's preamble assigning audio to Agent 1. It now reads:

> *"— Agent 1 for defence **selection**, dodge, camera response and framing; Agent 2 for AI reaction,
> **audio cue selection (the only C-05 audio responsibility)**, montage trigger and VFX timing.
> **Agent 1 has no C-05 audio responsibility** (`C05-7.2` row 5; `TN-C-15`; `DV-22`)."*

**I did not accept this on sight — I swept the whole document.** Every `Agent 1` + `audio`
co-occurrence (15 windows) was classified. **Zero are unmarked positive assignments.** All 15 are one
of: the corrected preamble, §5.2 row 5's *"Agent 1 owns no audio responsibility in C-05"*, the
disposition table in §2.5 quoting the old text to mark it as corrected, or §14.2 recording that the
old risk *"materialised"*. The one window my scan flagged as unmarked was a **quotation of the
corrected preamble** inside the §2.5 disposition — not an assignment.

**Beyond a deletion.** S4.1's fix would have been two words removed. S4.2 removed the words **and**
named the owner positively, three times, in three registers. That is a better correction than the one
I asked for, and I say so.

**Disposition: `AGREE`. D-4 is closed.**

### 3.2 D-22-scope — is `DV-22` now able to see the defect? · **AGREE WITH CONDITIONS — PARTIALLY CLOSED**

`DV-22` states, and the shipped validator enforces:

> *"row 5 clean of audio; row 6 owns cue selection; `TN-C-15` implementer; **§8 preamble clean**;
> **whole-document scan: no line pairs audio with Agent 1 outside a marked correction or
> quotation**"*

**It fires correctly on the blobs where the defect existed.** Executed by me, not taken on trust:

| Blob | `DV-22` result |
|---|---|
| S4.2 `7d03e1df` | **PASS** — preamble clean, 0 offenders |
| S4.1 `d54e194a` | **FAIL** — `§8 preamble clean False` |
| S3 `07723236` | **FAIL** — `§8 preamble clean False`; **2 offenders** incl. row 5's old *"camera and audio cues"* |

**That is exactly the discrimination `DV-22` could not produce at S4.1, and it is real.**

**But the whole-document scan is not sound, and this is condition N-1** (§7.1). It is a keyword
allowlist over lines, and a defect-bearing line can evade it. I have a live demonstration: the S4.1
preamble — which *does* assign audio to Agent 1 — is **exempted from the scan** because the line
happens to contain the string `D-4`. On that blob the scan reports **0 offenders** while the defect
is present, and only the separate `§8 preamble clean` check catches it.

**Disposition: `AGREE WITH CONDITIONS`.** The instrument now reaches the known defect; it does not
yet reliably reach the unknown one it exists to catch. Condition N-1.

### 3.3 D-1a — the staleness bound · **AGREE — CLOSED**

**`TN-C-14` (rewritten, line 641).**

My W-M2.13 finding was that *"at least once per frame"* constrains a **count**, not an **interval**,
and permits a 1.98-frame gap — so *"bounded by one frame, by construction"* did not follow. My own
addendum then upgraded this from minor to `PASS-CONDITION`.

S4.2 replaces the assertion with **five rules from which the bound is derived**. The two that do the
work:

> **(ii) Refresh in the frame, before first use.** Before its first timing-dependent use in each
> frame, the consumer takes a **successful observation** … The observation's `AxisNow` must not
> precede the start of the frame in which it is used: **a value carried across a frame boundary is
> not used.**
>
> **(iii) Maximum interval between successful refreshes.** … successive successful refreshes of one
> instance are at most **one frame apart**, measured **on the shared axis** — from the earlier
> observation's `AxisNow` to the later one's. Wall-clock time, frame counters and the consumer's own
> dilation are not the measure.

**I tested the derivation rather than reading it.** 400,000 randomly generated legal schedules, over
which I maximised the interval from a missed revision's publication to the next successful refresh
consistent with (ii) and (iii):

```
max staleness found : 0.999772 frames
<= 1 frame?         : True
approaches 1?       : True
```

and the analytic worst case (observe at frame start, revision published one tick later, next refresh
at the frame boundary) is **`1 − ε`**. The text states exactly this: *"the worst case approaches but
never reaches one frame (a revision published immediately after the frame's observation, used at the
frame's last instant)"*. **The arithmetic and the prose agree, and the conclusion is now derived
instead of asserted.**

**S4.1's 1.98-frame schedule is genuinely eliminated by (iii).** I checked that the schedule
`0.99 → 1.99` is now illegal and confirmed why: at `t_o = 0.99` the permitted next refresh is
`≤ 1.99`, but the missed revision must be published *after* the observation, inside frame 0, so the
worst achievable gap is `1.99 − 0.99⁺ < 1`. **Rule (iii) closes the exact hole.**

**Is the fix proportionate, or over-built?** Fair question, since (ii) and (iv) go further than my
finding strictly required. My finding was that the *stated reason* was false. S4.2 could have
weakened the claim to 1.98 frames and been done. It instead made the bound true, which is the
stronger choice and the one my addendum listed first among three options (§2.2(i)). **Not
over-built — it is the option I ranked as preferred.**

**One residual I record and do not press.** Rule (iii)'s measure is the **shared axis**, from the
earlier observation's `AxisNow` to the later one's. `AxisNow` is the producer's scope-position, and
`TN-P-11` lets a consumer carry `AxisNow` across revisions. So the bound is measured against a
quantity the consumer re-derives, not against a producer clock. This is deliberate and *correct* —
wall-clock and the consumer's own dilation are explicitly excluded, which is what makes the bound
meaningful across pauses and dilations — but it means the guarantee is *"at most one frame of
scope-position age"*, not *"at most one frame of real time"*. At `ProducerRate 0.05` a frame is 20
seconds of real time. **That is the right semantics for a timing contract**; I note it only so an
implementer does not read (iii) as a real-time bound.

**Disposition: `AGREE`. D-1a is closed.**

### 3.4 D-1b — the consumer classification · **AGREE — CLOSED**

S4.1's clause said *"a consumer whose behaviour depends on remaining time — it acts on `TN-C-10`'s
output"*, and I originally called that undefined. My addendum then **downgraded D-1b to `ADVISORY`**,
having found the em-dash parenthetical is itself a definition with identical compliance sets, and
**withdrew** my call-site recommendation.

S4.2 nonetheless adopted the call-site version in full:

> **(i) Call-site scope.** The obligation attaches to the **call site**, not to an agent: every call
> site that reads `RemainingLocalSeconds`, or derives a remaining time from it, is timing-dependent
> and must satisfy (ii)–(iv). A consumer with no such call site is governed only by (v).

**This is better than what I asked for, and it does not contradict my withdrawal.** My addendum's
point was that the requirement was already *satisfiable* without the change — `ADVISORY` means "not
required", not "forbidden". What (i) adds is a **positive, testable scope**: it names the concrete
read (`RemainingLocalSeconds`) and the derivation, rather than relying on a reader parsing a
parenthetical. That is a real improvement in testability, at no cost in meaning.

**I record one honesty point:** S4.2 §2.5 marks D-1b *"Adopted exactly"* against W-M2.13 (`eee9401`),
which is accurate — that is the review it answered. **It did not answer my addendum `e434dbe`,
which post-dates its drafting** (addendum 18:33; S4.2 text 18:36). So it adopted an ask I had
withdrawn four minutes earlier, in ignorance of the withdrawal. **That is not a defect in S4.2.**
The result is a better clause; I simply record that the lineage differs from what a reader might
assume. Condition N-3 (§9) is advisory only.

**Disposition: `AGREE`. D-1b is closed.**

### 3.5 C4c-N1 — `PO-3`'s rationale · **AGREE — CLOSED**

S4.1's §3.6 (b) asserted the internal application order *"is **not observable** at frame
granularity"* — a premise `PO-5` falsifies. S4.2 now reads:

> **(b)** Within one frame the internal application order **is observable through a mid-frame pull
> once `PO-5` is in force**, so leaving the order to the producer would let two conforming producers
> expose different revision sequences for identical gameplay — the exact non-determinism a contract
> exists to remove. `PO-5` therefore requires the application order to follow the publication order
> `PO-3` fixes, not merely to interleave publication with application. **S4.1 and earlier said the
> opposite here** — that the order was *not* observable at frame granularity — and that premise was
> falsified by `PO-5` itself (Agent 2's `C4c-N1`, Agent 3 finding 3).

**This is the correction I specified, near-verbatim**, and it does the two things my §6.2 required:
it **keeps `PO-3`** (which remains necessary — a producer could satisfy `PO-5` fully and still apply
the dilation first) and it **keeps the conclusion** while replacing only the false premise.

**It also credits the finding to me and to Agent 3, and states the correction explicitly** rather
than quietly applying it — *"because an implementer who read the old premise could have concluded
that the application order was unconstrained."* That is the right instinct.

**Verified independently, not from the prose:** `DV-26` fails on S4.1 and passes here, and I
confirmed both by direct text search on each blob.

**Disposition: `AGREE`. C4c-N1 is closed.**

### 3.6 D-6a — the `DV-11` count · **AGREE — REMAINS CLOSED**

Re-derived from the reviewed blob: **7 declared, 5 observed, 43 cells, 0 failures**, by parsing the
7th cell of all 43 obligation rows and re-implementing `DV-11`'s allowed-row rule
(`TN-P`→{2}, `TN-C`→{5,6}, `TN-R`→{2,4}, `TN-A`→{8}). Matches the document. Unchanged from S4.1 and
still correct.

### 3.7 D-6a-i — the `DV-24` condition · **AGREE — CLOSED**

My condition was: *"when S4.1's next substantive successor opens §13 for any other reason, add
`DV-24` — every declared/observed sentence equals `DV-11`'s computed output."*

**`DV-24` exists and is the instrument I specified.**

> **`DV-24` (new)** | every hand-restated declared/observed count equals `DV-11`'s computed pair |
> **FAIL on S4.0** — `stated at 4 sites {'§1 row 6': (7, 6), '§5.4': (7, 5), '§13.1 DV-11': (7, 5),
> '§18.1 C9': (7, 5)}; consistent False`

**I verified the failure claim rather than trusting it.** S4.0 §1 row 6 genuinely says *"7 declared,
6 observed"* while §5.4 and §13.1 say 5 — one inconsistent site among four, exactly as `DV-24`
reports. And S4.1, which fixed that cell, would pass — confirmed.

**S4.2 did better than my condition asked.** I said the instrument would close *"the class, not just
the instance"*. S4.2 adds `DV-24` **and shows it failing on the blob where the defect originated**,
which is the discipline my own S3 and S4 reviews established and which S4.1 had declined. The
decline at S4.1 was respectable (it would have changed §13's count from 23 in a targeted
correction); taking it now, at a revision that legitimately reopens §13, is the *right time*.

**Disposition: `AGREE`. D-6a-i is closed.**

### 3.8 D-6b — the §5.4 tallies · **AGREE — CLOSED**

S4.1's §5.4 said *"19 `TN-P` rows"* where the token occupies 23 cells, and *"11 `TN-C` rows"* where
it occupies 12. S4.2 now states full cell counts:

| Token | S4.2 declares | I re-derived |
|---|---|---|
| `producer owner` | **23 cells** (19 `TN-P`, 4 `TN-R`) | **23** (19 + 4) ✔ |
| `each consumer` | **12 cells** (12 `TN-C`) | **12** ✔ |
| `Agent 2, C-05 consumer` | 3 cells | **3** ✔ |
| `Agent 1, shared support` | 2 cells | **2** ✔ |
| `Agent 1, subject to TD-09` | 3 cells | **3** ✔ |
| `Agent 2, in its own systems` | **0 cells — by design** | **0** ✔ |
| `contract layer, owner pending TD-12` | **0 cells — by design** | **0** ✔ |

**Every figure matches my independent parse.** Note this is the third hand-restated count in this
document family — after S2's DV-8 and S3/S4's DV-11 — and it is the first one corrected by
**machine-deriving** rather than re-typing. The tallies are now consistent with `DV-11`'s own output.

**Disposition: `AGREE`. D-6b is closed.**

### 3.9 D-1, D-2, D-3, D-5, D-6, D-7, C4a-1, C4a-2, C4c-1, C4c-2, C6-1, C9 — **AGREE — PRESERVED**

S4.2 claims to preserve these. **I verified preservation rather than accepting it**, by byte-comparing
the clauses against S4.1:

| Clause | Identical to S4.1 |
|---|---|
| `TN-P-18`, `TN-P-19` (D-2, D-3) | **yes** |
| `TN-C-10` (D-7 echo) | **yes** |
| `TN-C-11`, `TN-C-15` (arbitration, audio) | **yes** |
| `TN-A-02`, `TN-A-03` (arbitration boundary) | **yes** |
| `PO-5` and its "pull between two publications" consequence (D-2) | **present, unchanged** |

And re-derived structurally: **43 obligations (19 P / 15 C / 6 R / 3 A)**, **67 cases over 18
suites**, **ids 1…67 complete**, **5 observed tokens over 43 cells, 0 failures**. All match S4.1.

**D-3's identity constancy** remains coherent: `"fixed for the instance's lifetime"` appears 9 times,
`TN-P-04` names the close-and-reopen path, `T-C05-66` is present.

**Disposition: `AGREE` across all twelve. None reopened.**

---

## 4. Summary disposition table

| Finding | §3 | Disposition | Closed? |
|---|---|---|---|
| **D-4 / C6-2** audio ownership | 3.1 | **AGREE** | **Yes** |
| **D-22-scope** instrument reach | 3.2 | **AGREE WITH CONDITIONS** | **Partially** — N-1 |
| **D-1a** staleness bound | 3.3 | **AGREE** | **Yes** |
| **D-1b** consumer classification | 3.4 | **AGREE** | **Yes** |
| **C4c-N1** `PO-3` rationale | 3.5 | **AGREE** | **Yes** |
| **D-6a** `DV-11` count | 3.6 | **AGREE** | **Yes** (remains closed) |
| **D-6a-i** `DV-24` | 3.7 | **AGREE** | **Yes** |
| **D-6b** §5.4 tallies | 3.8 | **AGREE** | **Yes** |
| **D-1, D-2, D-3, D-5, D-6, D-7** | 3.9 | **AGREE** | **Yes** (preserved) |
| **C4a-1, C4a-2, C4c-1, C4c-2, C6-1** | 3.9 | **AGREE** | **Yes** (preserved) |
| **C9** | 3.6 | **AGREE** | **Yes** (remains closed) |
| **N-1** `DV-22` scan false negative | 7.1 | **DISAGREE** | **No** — new |
| **N-2** duplicate S4.2 identity | 8 | **DISAGREE** | **No** — new |
| **N-3** addendum not answered | 9 | advisory | n/a |

**15 closed · 2 closed with caveat · 2 new defects · 0 previous findings still open.**

---

## 5. Normative correctness vs documentation vs instrument correctness

The instruction requires this separation, and it matters because the two new defects fall in
different columns from the closed ones.

| Layer | State |
|---|---|
| **Normative correctness** — who must do what | **Sound.** All 43 obligations, `PO-3`/`PO-5`, `TN-C-14`'s five rules, the `TN-A` arbitration boundary and `TN-C-15`'s single ownership are internally consistent and satisfiable. **No normative defect found.** |
| **Derived-guarantee correctness** — does the claimed bound follow? | **Sound, and now genuinely derived.** Verified by 400,000-case search. This is the layer my D-1a was about, and it is fixed |
| **Documentation correctness** — do the prose, tables and tallies agree with the clauses? | **Sound.** Every count I re-derived matches. The §2 disposition tables match §7–§9 |
| **Validation-instrument correctness** — do the checks reach the defects? | **Two defects.** `DV-22`'s scan has a false-negative escape hatch (N-1). The other 26 checks behave correctly on all four blobs I tested |
| **Provenance correctness** — can a reader pin exactly what they cite? | **One defect.** Two documents share `TDD-A1-C05-SUCCESSOR-004.2` (N-2). The *reviewed* artifact's own chain is exemplary |

**The headline: the contract text is in the best state it has been in. The two failures are in the
machinery around it.**

---

## 6. Proposed test specifications vs executed tests

**Nothing in this document field has ever been executed against a running system.** I want that
stated without hedging, because S4.2 now contains more testable-looking material than any
predecessor.

| Category | Count | Status |
|---|---|---|
| Acceptance cases `T-C05-01` … `T-C05-67` | **67** | **`PROPOSED / NOT RUN` · 0 executed** |
| Document checks `DV-1` … `DV-27` | **27** | **executed** — text checks only |
| Of which added or widened at S4.2 | 7 (`DV-20` widened, `DV-22` widened, `DV-24`–`DV-27` new) | executed, and shown failing on the pre-fix blobs |
| Lines of executable validation shipped | `docs/validation/dv_c05.py`, 383 lines | **I ran it: 27/27 on the reviewed blob** |

**`T-C05-64` deserves specific mention**, because it is the case that would falsify the new
`TN-C-14`, and S4.2 extends it substantially: three schedules — (s1) nominal, **(s2) Agent 3's
counterexample stated exactly**, (s3) the worst-case permitted placement — plus two negative
controls (n1) carrying a value across a frame boundary, (n2) acting after a failed pull.

**This is a *specification*, not a result.** (s2) in particular now asserts what *should* happen on
a schedule that would break S4.1's rule; whether a conforming consumer behaves that way is
**unverified**, because no consumer exists. I record that S4.2 marks it `PROPOSED / NOT RUN` and that
`DV-25` — which checks that the four extension elements are *present in the text* — is not a
substitute for running the case. S4.2 says this itself (§13.4: *"The one thing `DV-25` cannot do is
prove that a consumer honours `TN-C-14`; that is `T-C05-64`'s job, and it has not run."*).

**I confirm that statement is accurate and I endorse it.**

---

## 7. Newly introduced defects

### 7.1 N-1 — `DV-22`'s whole-document scan has a false-negative escape hatch

**`§13.1` `DV-22`; `docs/validation/dv_c05.py` lines 287–301.**

This is the instrument added to answer my D-22-scope finding, so it is exactly the place to look for
a new flaw. **It is a keyword allowlist.** The implementation exempts any line containing one of
fifteen substrings — `'D-4'`, `'preamble'`, `'C6-2'`, `'also claimed'`, `'finding 1'`, and others —
before deciding whether the line assigns audio to Agent 1.

**Live consequence on the reviewed blob's own predecessor:** the S4.1 §8 preamble
(`"Agent 1 for defence, dodge, camera and audio"`) assigns audio to Agent 1. The scan exempts it,
because the line also contains `D-4`:

```
S4.1 preamble line matches whitelist keyword: ['D-4']
DV-22 whole-document scan offenders on S4.1: 0        <- defect present, scan reports clean
```

`DV-22` still **fails** S4.1, because the separate `§8 preamble clean` check requires the positive
phrase *"no C-05 audio responsibility"*. So no wrong verdict is produced today. **The scan component,
however, does not do the job it claims**, and its claim is the one that closes D-22-scope.

**Demonstrated false negative.** I injected a genuine violation — a new obligation row reading
`"Agent 1 owns the camera and audio cues for the player"`:

| Injected line | Offenders detected | Correct? |
|---|---|---|
| `Agent 1 owns the camera and audio cues…` | **1** | ✔ caught |
| `D-4 note: Agent 1 owns the camera and audio cues…` | **0** | **✘ missed** |

A one-word prefix defeats the check. Any author who mentions a finding number on the same line —
which this document does constantly — silently disables the scan for that line.

**Why this is `PASS-BLOCKING` and not cosmetic.** The instrument's stated purpose is *"audio has
exactly one owner **in all ownership prose**"*. An allowlist that exempts lines *for containing
subject matter the document routinely contains* cannot substantiate "all". It is the same class of
failure as S3's `DV-11` and S4.1's `DV-22`: **a check scoped to the cases its author had in mind.**
It would pass a future regression introduced next to a `D-4` reference.

**Exact closure condition.** Detect assignment by **structure, not by keyword presence**. Two workable
forms, either sufficient:

1. **Negative-form requirement:** in any line pairing `Agent 1` with `audio`, require one of a small
   set of *negations* (`owns no audio`, `has no C-05 audio responsibility`, `not claimed`) **and fail
   closed otherwise** — i.e. invert the default from allow-by-default to deny-by-default; or
2. **Explicit marked-region list:** replace substring matching with an explicit line-number or
   block-ID allowlist of *review-disposition regions* (§2.5, §13.3, §14.2), so exemption is a
   property of **where the text is**, not of what words it happens to contain.

**Deny-by-default is the point.** As written the scan is allow-by-default with keyword escapes; the
fix is to make it fail unless the line is affirmatively recognised as a non-assignment.

**Also required: add the counterexample to §13.3.** `DV-22`'s failure demonstration should include
the keyword-prefixed injection above, so the escape hatch is shown closed. Right now §13.3 shows
`DV-22` failing on S4.1 and S3 — **both of which it catches via the `preamble` check, not via the
scan**. The scan has never been shown to catch anything.

### 7.2 N-2 — two incompatible documents carry the identifier `TDD-A1-C05-SUCCESSOR-004.2`

**Provenance. Not a defect in the reviewed document's own text.**

| | Reviewed here | Also published as "S4.2" |
|---|---|---|
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | **same path, different branch** |
| Branch | `arena/3bc206a0-tdd` | `arena/c64fc525-tdd` |
| Commit / blob | `a788f95` / **`7d03e1df`** | `c800bf0` / **`61ef03b4`** |
| Lines | 1,265 | 1,237 |
| **`Response ID`** | **`TDD-A1-C05-SUCCESSOR-004.2`** | **`TDD-A1-C05-SUCCESSOR-004.2`** |
| §8 preamble | audio removed ✔ | audio removed ✔ |
| **`TN-C-14` measure** | **one frame on the shared axis** | **1/60 s monotonic elapsed time** |
| Diff between them | **360 changed lines** | |

**The two are not duplicates and not alternatives of equal standing — they encode different
contracts.** The staleness guarantee is the clearest case: one bounds *scope-position age on the
shared axis*, the other bounds *1/60 second of monotonic elapsed time*. Both cannot be the contract.
They are also not reconcilable by merge — 360 lines differ.

**Why it blocks.** The instruction to me says *"Do not review … an unpinned branch-tip substitute"*,
which is the right discipline and which I followed. But it presumes pinning resolves ambiguity. It
resolves which *bytes* I read; it does not resolve which *contract* "S4.2" names. A TD consolidating
reviews must be able to write "S4.2 §8" and mean one sentence. **Today that is not possible**, and
the collision is inside the document itself: both files declare `Response ID:
TDD-A1-C05-SUCCESSOR-004.2` on line 3.

**I am not asserting which is authoritative.** The reviewed blob is the one my instruction pins, and
it is the one whose provenance register is complete and verifiable. I have not reviewed the other, do
not assess its quality, and make no claim about which Agent 1 intends to publish.

### 7.2.1 Exact closure condition

One of:
1. **Withdraw** the unreviewed copy from `arena/c64fc525-tdd`; or
2. **Re-identify** it (`…-004.2-draft`, or a distinct version) so the response ID is unique; or
3. **Declare** in the provenance register which blob `TDD-A1-C05-SUCCESSOR-004.2` denotes and that
   the other is superseded, with a commit message that says so.

**Any of the three closes it.** What must not persist is two files claiming one identity.

### 7.3 No other new defect found

I swept the remaining surface for regressions:

| Area | Check | Result |
|---|---|---|
| Structural totals | 43 / 67 / 18 / 27 | **reconcile** ✔ |
| `DV-1`…`DV-27` | contiguous, none dropped from the previous 23 | **contiguous 1..27**, 24–27 new ✔ |
| Preservation | `TN-P-18/19`, `TN-C-10/11/15`, `TN-A-02/03`, `PO-5` vs S4.1 | **byte-identical** ✔ |
| Tokens | 43 cells, 7 declared, 5 observed | **0 failures** ✔ |
| Test specs | 67 cases, ids 1…67 | **complete, none removed** ✔ |
| Placeholders | `S41_*`, `PUB_*`, `TBD` in the reviewed blob | **none live** — the only occurrences are `DV-27`'s quoted output ✔ |

---

## 8. `DV-27` and the placeholder problem — the best fix in this revision

S4.1's reviewed blob carried literal `S41_COMMIT`/`S41_BLOB` fields, filled by a later commit. That
is a genuine trap: **the blob reviewers pin is not the blob the author intended to publish.**

S4.2 solves it properly — **by refusing to put its own hash in itself:**

> *"A document cannot contain its own blob hash without a post-publication edit … **This register
> carries the hash instead**, in the commit immediately after the text, so the reviewed blob is never
> a document with an unfilled field."*

`DV-27` enforces it: *"no placeholder token anywhere in the file; §17 records S4.1's exact commit and
blob; the provenance register is referenced in §17 and §18."*

**Verified:** the reviewed blob contains no live placeholder. `S41_COMMIT`/`S41_BLOB` appear **only**
inside `DV-27`'s own quoted failure output at lines 1081 and 1085 — i.e. as evidence, not as fields.
`§17` records S4.1's exact values (`95918268…` / `d54e194a…`, spelled out in full) and points at the
register for its own.

**And the register is real, correct, and pins the blob I reviewed:**
`git rev-parse a788f953256d208f3eb1310f3897924d007179b1:docs/…V4_2.md` → `7d03e1df…`, matching both
the instruction and the register's own table, three occurrences of the full hash.

**This is the correct architectural answer to the S4.1 trap and I record it as such.** It also
adopts my own §1.3 provenance rule, and states that it applied it to its own claims — a discipline I
did not expect to see reflected back, and which I note with approval.

---

## 9. N-3 (advisory) — S4.2 did not answer my addendum

Not a defect in S4.2. Recorded so the consolidation has the fact.

My addendum `Addendum A1` (`e434dbe`, committed **18:33:02Z**) downgraded D-1b to `ADVISORY` and
upgraded D-1a to `PASS-CONDITION` with the count-versus-interval arithmetic. S4.2's text was written
at **18:36:32Z**, three and a half minutes later, and its §17 names only
`TDD-A2-REVIEW-A1C05-S4-1-001` (commit `eee9401`) as the Agent 2 review answered. The strings
`e434dbe`, `ADDENDUM`, `PASS-CONDITION`, `PASS-BLOCKING` and `ADVISORY` appear **zero** times.

**Consequence, in both directions:**

- **S4.2 reached the D-1a conclusion independently** — its `TN-C-14` derivation matches the
  arithmetic in my addendum §2.2, and it credits `D-1a` to my W-M2.13 review, which is the review
  that raised the bound at all. Nothing is misattributed.
- **S4.2 adopted my *withdrawn* D-1b ask**, marking it *"Adopted exactly"*. Since the clause it
  produced is a genuine improvement (§3.4), no harm resulted. But a reader comparing my addendum
  ("not required") with S4.2 ("adopted exactly") would see a contradiction that is purely a timing
  artifact.

**Advisory closure:** in the next revision, cite the addendum in §17 and state that D-1b was adopted
as an improvement while remaining `ADVISORY` under the taxonomy. **Not blocking.**

---

## 10. Executed checks — reproducibility

All run against the reviewed blob `7d03e1df`. None is an acceptance test.

| # | Check | Method | Result |
|---|---|---|---|
| 1 | Reviewed blob is the named one | `git rev-parse a788f95:docs/…V4_2.md` | `7d03e1df…` ✔ |
| 2 | Blob ≠ first S4.2 draft | `git diff 86f56af 7d03e1df` | 3 ins / 3 del, three sentences ✔ |
| 3 | Provenance register at the tip pins the reviewed blob | `git show d1d9ac9:docs/…PROVENANCE.md` → blob `68c1cd71` | full hash ×3 ✔ |
| 3b | Register *at* `a788f95` still pinned the first draft | `git show eda9bd26…` | `86f56af` — corrected by `d1d9ac9` ✔ |
| 4 | S4.2's validator runs | `python3 docs/validation/dv_c05.py` on the blob | **27/27 passed** ✔ |
| 5 | Validator discriminates | same file on S4.1 / S4.0 / S3 | **22/27 · 21/27 · 10/27** ✔ |
| 6 | `DV-22` reaches the D-4 defect | run on S4.1, S3 | **FAIL on both** ✔ |
| 7 | `DV-24` reaches the count defect | run on S4.0 | **FAIL**, one site (`§1 row 6` (7,6)) ✔ |
| 8 | `DV-22` scan false negative | S4.1 preamble keyword match; injected line | **`['D-4']` → 0 offenders** ✘ |
| 9 | Audio ownership, whole document | 15 `Agent 1`+`audio` windows classified | **0 unmarked assignments** ✔ |
| 10 | `TN-C-14` bound holds | 400,000 legal schedules, maximised gap | **0.999772 < 1** ✔ |
| 11 | Rule (iii) eliminates S4.1's schedule | analytic, `0.99 → 1.99` | **now illegal** ✔ |
| 12 | §5.4 tallies | re-parse 43 cells | **23 / 12 / 3 / 2 / 3 / 0 / 0** ✔ |
| 13 | `DV-11` row-level rule | independent re-implementation | **0 failures** ✔ |
| 14 | Structural totals | parse §7–§9, §12.1, §13.1 | **43 / 67 / 18 / 27** ✔ |
| 15 | Preservation vs S4.1 | byte-compare 7 clauses + `PO-5` | **all identical** ✔ |
| 16 | Placeholders live in reviewed blob | search, excluding quoted output | **none** ✔ |
| 17 | Two S4.2 identities | compare `Response ID` on both branches | **collision confirmed** ✘ |

---

## 11. Overall verdict

# `PASS WITH CONDITIONS`

**On the contract text: `PASS`.** Every one of my seventeen reassessed findings and conditions is
closed, and closed *properly* — by corrected substance, not by assertorial rewording:

- **D-4** — the audio contradiction is gone from the whole document, not just from the sentence I
  named, and the owner is now stated positively in three registers.
- **D-1a** — the bound is **derived**, and I could not break it in 400,000 schedules.
- **C4c-N1** — corrected exactly as specified, with `PO-3` retained and the correction disclosed.
- **D-6a-i** — `DV-24` added, and shown **failing on the blob where the defect originated**.
- **D-6b** — tallies now machine-derived and matching my independent parse.
- **D-1b** — improved beyond what was required.

**Why not an unconditional `PASS`.** Two defects, both in the machinery rather than the contract:

1. **N-1 — `DV-22`'s scan can be defeated by a single word on the line.** The instrument that closes
   my D-22-scope finding has a demonstrated false negative. An instrument that certifies a property
   it cannot test is not a closed condition.
2. **N-2 — two incompatible documents answer to `TDD-A1-C05-SUCCESSOR-004.2`.** Both are on remote
   branches; they differ on what `TN-C-14` measures; 360 lines separate them. That is a provenance
   defect a TD cannot consolidate past.

**Why not `TARGETED REVISION`.** Neither condition requires a normative change, a reopened
requirement, or a re-review of the contract text. N-1 is a rewrite of one checker's predicate; N-2 is
a withdrawal, a rename, or a declaration. **Both are closable without touching a single obligation,
and I would then move to `PASS` without re-reviewing the text.** That is the distinction between
`PASS WITH CONDITIONS` and `TARGETED REVISION`, and it is doing real work here.

**What would still not be true after both are closed.** C-05 would still be unsigned, U-07 open,
**no MEAD would have been selected**, 0 of 67 acceptance cases executed, and no consumer would have honoured `TN-C-14`
because no consumer exists. **This review is evidence about a document. It is not evidence about a
game.**

---

## 12. What I did and did not do

**Did.** Verified the exact blob by hash before reading, and confirmed it is not the first S4.2
draft; read all 1,265 lines; re-derived every count and tally from the text; re-implemented `DV-11`'s
rule; ran Agent 1's shipped validator on four blobs and confirmed it discriminates; brute-forced the
`TN-C-14` bound over 400,000 schedules; swept the whole document for audio-assignment prose;
byte-compared seven clauses and `PO-5` against S4.1 to confirm preservation; injected a mutation to
test whether `DV-22` catches it, and found the escape hatch; verified the two-document identity
collision; separated normative, documentation, instrument and provenance correctness; separated
proposed test specifications from executed tests.

**Did not.** Modify Agent 1's S4.2 document or any predecessor; review the unreviewed S4.2 copy on
`arena/c64fc525-tdd` or assess its quality; assert which of the two S4.2 documents is authoritative;
reopen S4.1 or use it as a substitute target; claim any acceptance case executed; treat `DV-25`'s
presence checks as evidence a consumer honours `TN-C-14`; sign, freeze, merge, select a MEAD,
authorise implementation, or claim M0 completion.

**C-05 and U-07 remain open. Nothing is signed. 0 of 67 acceptance cases executed.**

---

## 13. Provenance of this review

| Field | Value |
|---|---|
| Review ID | `TDD-A2-REASSESS-A1C05-S4-2-001` v1.0 |
| Author | Agent 2 — World Structure and Level Architecture |
| Branch | `arena/5dde91a4-tdd` |
| Reviewed artifact | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md`, blob **`7d03e1df837493305831962f43882a1cd3496143`**, at commit **`a788f953256d208f3eb1310f3897924d007179b1`** |
| Predecessor reviewed earlier | S4.1 blob `d54e194a…` at `95918268…`; S4.0 blob `424d2c69…`; S3 blob `07723236…` |
| Prior Agent 2 artifacts | `TDD-A2-REVIEW-A1C05-S4-1-001` (`eee9401`) · `ADDENDUM-A1` (`e434dbe`) — **both preserved unmodified** |
| Test module | `Tools/world/tests/test_review_a1c05_s4_2.py` |
| Test-basis blobs (pinned) | S4.2 `7d03e1df` · S4.1 `d54e194a` · S4.0 `424d2c69` · S3 `07723236` |
| Engine | **NONE** — no Unreal, no GPU, no compiled code |
| Acceptance tests executed | **0 of 67** |

**Provenance rule applied and stated.** My W-M2.13 §1.3 rule — *re-verify any negative existence
claim as the last action before publication* — was applied to `N-2`, the one repository-wide claim in
this review. `git ls-remote` was re-run immediately before this document was committed, and the
result recorded in the commit message. Both S4.2 blobs were confirmed present on their branches at
that moment.

**Independent of Agent 3.** This review was written without reading Agent 3's S4.2 reassessment, if
one exists at the time of writing. Where S4.2 itself credits Agent 3 (findings 3, 4, 5, 7) I record
the credit as S4.2 states it; I make no independent claim about Agent 3's conclusions, and nothing
here characterises or anticipates its verdict. Agent 3's review of S4.2 is its own, and a TD
consolidating the two should treat them as separate evidence.

---

*End of reassessment. `TDD-A2-REASSESS-A1C05-S4-2-001` v1.0. `PASS WITH CONDITIONS` — two conditions,
neither normative.*
