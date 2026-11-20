# AGENT 2 — INDEPENDENT REVIEW OF `A1-C05-S4` v4.0

**Review ID:** `TDD-A2-REVIEW-A1C05-S4-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — no signature, no freeze, no merge, no implementation, no MEAD
selection, no TD decision. **C-05 and U-07 remain open and I do not claim otherwise.**
**Outcome:** **`TARGETED REVISION`** (§10).

---

## 0. Provenance, and one correction to the object I was asked to review

### 0.1 The requested path does not exist; what I reviewed instead

The instruction names `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md` and calls the document "C-05 S4.1".
**No file by that name exists on any remote branch**, and no commit message mentions a 4.1:

```
$ git ls-remote origin
5e3d1da4…  refs/heads/main
a3453548…  refs/heads/arena/3bc206a0-tdd   <- Agent 1
47dbdffb…  refs/heads/arena/5dde91a4-tdd   <- Agent 2 (mine)
1eb613f3…  refs/heads/arena/c64fc525-tdd

$ for b in <every remote head>; do git ls-tree -r --name-only origin/$b | grep -i "V4_1"; done
(no output)
$ git log --all --oneline --grep="4\.1"
13a2f43 A1 C-05-3: respond to Agent 3's telegraph authority recommendation   (unrelated, S1-era)
```

What exists is **`docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md`**, internally versioned **`A1-C05-S4` v4.0**,
and its own §1/§2 are scoped to exactly the seven defects and four conditions this instruction lists.
I reviewed that document rather than stopping, because it is unambiguously the intended object —
but **I did not silently substitute a path**, and if Agent 1 later publishes a genuine v4.1, this
review does **not** cover it.

### 0.2 The exact blob reviewed

| Field | Value |
|---|---|
| **Blob reviewed** | **`424d2c69df62ebc1930eacd0ba67077c854ab31e`** |
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md` |
| **Content commit** | **`4692e973d04a94d7781677c704e7a0198abd2d70`** |
| Version | `A1-C05-S4` v4.0 |
| Lines | 1,165 |
| Branch | `arena/3bc206a0-tdd` (`origin/a1branch`) |
| Baseline | `A1-C05-S3` v3.0, blob `07723236…` at `a6b4e229` — **unmodified, verified** |

**Which blob is the object, and why the choice is not arbitrary.** The branch tip is `a3453548`,
whose file is blob `d72831e7…`. I diffed the two blobs:

```
$ git diff 424d2c69 d72831e7
12 changed lines: 6 insertions, 6 deletions
  PUB_COMMIT_PLACEHOLDER -> 4692e973…
  PUB_BLOB_PLACEHOLDER   -> 424d2c69…
  + one paragraph explaining that the placeholder fill touches nothing else
  §18.1 and §18.2 handoff sentences: placeholders -> filled values
```

**Every one of the 12 lines is a placeholder fill or the paragraph describing that fill.** No
normative clause differs. S4 states its own review target at §17 — *"review the blob named above,
`424d2c69…` at `4692e973…`"* — and the tip's own paragraph says the same. **I reviewed `424d2c69`
as instructed by the document and confirmed by diff that the finding set is identical at the tip.**
Unlike S3, where I had to reconcile a placeholder gap myself, S4 names its target explicitly and
the branch history confirms it. That is correct practice and I record it as such.

### 0.3 What else I read

| Document | Commit / blob | Why |
|---|---|---|
| **My own S3 review** | `47dbdff`, 813 lines | the D-1…D-7 and C4a/C4c/C6/C9 findings this review adjudicates |
| `A1-C05-S3` | `a6b4e229`, blob `07723236…` | the baseline; verified unmodified |
| My `A2-C05` submission | `3ac438b`, §7.6, §8 | `WindowKey`/`AttackTag` **Required**; ownership list |
| `A1-C05-S2`, `A1-C05-S1` | `e5ddad69` / `2bb729f` | supersession chain |
| MEAD-A (mine) / MEAD-B / MEAD-C | `Docs/00_MASTER…`, 247 lines, `f4935463…` | neutrality, TD-12 status |

I read all 1,165 lines of S4.

---

## 1. Verdict summary

| # | Finding | Verdict | Defect genuinely resolved? |
|---|---|---|---|
| **D-1** | Lost retime → silent stale rate | **AGREE WITH CONDITIONS** | **Yes** — bound added, residual stated |
| **D-2** | Ordering without per-message content | **AGREE** | **Yes** — `PO-5` is real |
| **D-3** | Identity constancy contradiction | **AGREE** | **Yes** — consistent everywhere |
| **D-4** | Audio owned twice | **DISAGREE** | **No** — one stale clause survives |
| **D-5** | Implementer-token mapping | **AGREE** | **Yes** — new token, re-mapped |
| **D-6** | `DV-11` not row-level | **AGREE WITH CONDITIONS** | **Yes** — but a count is still wrong |
| **D-7** | `INV-2` precondition | **AGREE** | **Yes** |

| Condition | Verdict | Resolved? |
|---|---|---|
| **C4a-1** (`INV-2` precondition) | **AGREE** | Yes — in the clause |
| **C4a-2** (`VF` three homes) | **AGREE** | Yes — `DV-12` set equality |
| **C4c-1** (`EX-5` case (d)) | **AGREE WITH CONDITIONS** | Yes, with the D-1 condition |
| **C4c-2** (`PO-3` content) | **AGREE** | Yes — `PO-5` |
| **C6-1** (constancy) | **AGREE** | Yes — see D-3 |
| **C6-2** (audio) | **DISAGREE** | No — see D-4 |
| **C9** (token counts / row-level) | **AGREE WITH CONDITIONS** | Partly — see D-6 |

**Tally over seven defects and seven conditions: 8 AGREE, 4 AGREE WITH CONDITIONS, 2 DISAGREE.**
Five of seven defects are fully closed, one is closed with conditions, and **D-4 is not closed**.
S4 is a substantial and largely successful revision; the remaining problems are three clusters,
all narrow.

**I am not signing v4.0.**

---

## 2. D-1 — lost retime and stale-rate handling · **AGREE WITH CONDITIONS**

**Clauses:** §3.6 rationale (c); §10.5 case (d); `TN-C-14` (§8); `TN-C-10` (§4.6); `EX-5` (d); `T-C05-64`.

### 2.1 What was wrong and what changed

My defect was that `EX-5` (c) enumerated only *both received* and *only `n+2` received*, omitting
**only `n+1` received** — the case where the consumer is phase-correct, records no gap, raises no
resync, and ages at the pre-retime rate with no detection. §3.6's rationale then asserted the
consumer "merely needs a resync", which nothing obliged.

S4 does four things, and I checked each:

1. **§3.6 (c) is honestly retracted.** It now reads: *"S3's claim that it 'merely needs a resync'
   was wrong, because `AD-2` triggers on `incoming > held + 1` and no further revision arrives to
   trigger it."* That is an accurate statement of my finding in Agent 1's own voice.
2. **`EX-5` case (d)** is added and specifies the consumer as *"phase-correct and rate-stale"*,
   naming `TN-C-10` and `TN-C-14` as its obligations.
3. **`TN-C-14`** imposes a re-pull at least once per frame on any consumer *"whose behaviour depends
   on remaining time"*, with a carve-out for message-only consumers.
4. **The message-only residual is stated, not hidden**, both in `EX-5` (d) (*"its remaining-time
   estimate can be wrong by the whole ratio of the retime until the next phase transition"*) and in
   `T-C05-64` (*"asserted to be wrong by exactly the retime ratio"*).

### 2.2 Does the bound actually hold? I tested it rather than accepting it

The bound depends on the pull recovering the withheld revision. Tracing it:

| Step | Clause | Result |
|---|---|---|
| Consumer adopts `n+1`, loses `Retimed`@`n+2` | `AD-1`, `EX-5` (d) | phase-correct, `Rate` = pre-retime |
| Producer applies dilation | `PO-5` / `TN-P-18` | live state may **not** hold an unpublished `VF` change |
| Consumer pulls within frame F | `TN-P-11` + `PO-5` | returns `n+1`'s `VF` — stale rate, correctly |
| Consumer pulls in frame F+1 | `TN-C-14` + `AD-1` | returns `n+2`, adopts it |
| Worst-case staleness | — | **≤ one frame** |

**The bound is sound, and it is sound *because* `PO-5` exists** — without `PO-5`, a producer could
apply the dilation and leave the retime unpublished indefinitely, and the re-pull would return a
`VF` the revision does not cover. `PO-5` closes that. This is a genuinely well-constructed fix:
`TN-C-14` is only meaningful in the presence of `PO-5`, and S4 added both.

### 2.3 Condition D-1a — the bound is an upper bound, and `TN-C-14`'s wording blurs that

`TN-C-14`'s failure column says *"Staleness is then bounded by one frame, **by construction**."*
That is true as an **upper** bound. It is **not** true as a same-frame guarantee, and the
difference matters to an implementer sizing a defensive window.

Frame-internal ordering is unspecified. Within frame F, a consumer that pulls **before** the
producer publishes `n+2` gets `n+1`; one that pulls **after** gets `n+2`. Both satisfy *"at least
once per frame"*. So the staleness a consumer can observe is *"up to one frame"*, and whether it is
zero or one frame depends on **where in the frame the pull lands relative to the producer's
publication point** — which no clause fixes.

**Why this is a condition and not a defect.** `TN-C-14` says "bounded by one frame", which is
literally correct. It does not say "within the same frame" and I am not accusing it of that. The
condition is that the *implementer-facing* text should not be readable as the stronger claim.

**Closure condition (D-1a).** Add to `TN-C-14`: *"The bound is 'at most one frame', measured from
the publication of the missed revision to the next successful pull. `TN-C-14` does not require the
pull to land after the producer's publication within the same frame, and the period is a per-frame
minimum, not a per-frame guarantee of recovery."* One sentence. If Agent 1 prefers, state in
`T-C05-64` that the fixture must exercise **both** pull positions (before and after the producer's
publication in F) so the two-frame worst case is pinned by test rather than by prose.

### 2.4 Condition D-1b — the carve-out's boundary is undefined

`TN-C-14` splits consumers into *"a consumer whose behaviour depends on remaining time — it acts on
`TN-C-10`'s output"* and *"a consumer that only reacts to phase transitions"*. Nothing in the
contract defines **which** consumers fall where. §6.1 lists AI, audio, montage, VFX; a reader can
argue that an AI that begins a dodge *n* frames before a phase ends is timing-dependent, while one
that reacts only on `PhaseChanged` is not — and the same consumer may be both at different times.

**Closure condition (D-1b).** Either (i) assign each of §6.1's four consumers to one side of the
split, in `TN-C-14` or a table beside it, so the classification is checkable; or (ii) state that the
classification is per-call-site and the consumer must satisfy `TN-C-14` in any call site that reads
`RemainingLocalSeconds`, which makes it a property of the code path rather than of the agent.
**Option (ii) is cleaner and I recommend it** — it removes the need for a taxonomy.

---

## 3. D-2 — publication ordering and per-message content · **AGREE**

**Clauses:** §4.9 `PO-5`; §3.6 interleaving paragraph; `TN-P-18`; §10.11 `EX-11`; `T-C05-51`
(extended); `T-C05-65`.

**This is the best fix in the document.** My defect was that `PO-3` fixed *sequence* but left
*content* open, so reading B — `n+1` carries the pre-retime rate — was unsatisfiable with `TN-P-11`
whenever the producer applied the dilation before publishing the phase.

`PO-5` resolves it by changing the *publication discipline* rather than the message format:

> *"Publication is **interleaved with application**, not batched at the end of a frame. The producer
> applies a change, publishes the message carrying exactly the state at that revision, applies the
> next change, and publishes again… A pull taken between two publications of the same frame returns
> the earlier revision's `VF` exactly."*

I verified the three-way consistency this depends on:

| Clause | Constraint | Consistent? |
|---|---|---|
| `PO-5` | publish between applications; live state never ahead of publication | — |
| `TN-P-11` | pull answers from live state, `VF` == current revision | **yes**, only if `PO-5` holds |
| `INV-1` | same revision ⇒ identical `VF` | **yes**, now that live state cannot lead the revision |

Reading B becomes the only legal reading *and* becomes satisfiable. `T-C05-51` now asserts
`ProducerRate` per message and `T-C05-65` asserts the mid-frame pull, including a negative control
(*"a batching producer fails on the first pull"*). **The discriminating power I asked for is present.**

**No remaining defect in `PO-5` itself.** One consequence elsewhere is a new finding — see §7.1.

---

## 4. D-3 — attack identity and close-and-reopen · **AGREE**

**Clauses:** §3.8; §6.1 alternative 3; `TN-P-19`; `TN-P-07` (identity clause removed);
`TN-P-04` (extended); §10.12 `EX-12`; `T-C05-66`; `T-C05-62` (rewritten).

S4 takes **constancy plus a named change path**, which is my option (ii) expressed as (i). The two
readings do converge once the change path is an obligation: *"fixed while the instance is open under
one attack definition; a change closes the instance and opens a new one"* is exactly what `TN-P-19`
now says. I recommended mutability because I did not see that the change path could be made
normative rather than prose; S4 made it normative, which is the stronger form. **I accept the
choice and withdraw the preference for my wording.**

I checked all four places for full consistency:

| Location | Now says | Consistent |
|---|---|---|
| §3.8 | "fixed for that instance's lifetime" | ✔ |
| §6.1 alternative 3 | "fixed for the instance's lifetime" | ✔ |
| `TN-P-07` | "every change to a versioned field **that can change mid-instance**"; "Identity fields cannot change mid-instance at all" | ✔ |
| `T-C05-62` | identity rows **replaced** by a close-and-reopen assertion; attempted mid-instance change is a **producer violation** | ✔ |

The dead norm is gone and the untestable rows are gone. `DV-23` checks that the rejected phrase
"constant for the lifetime" appears only inside quotation marks — I verified that independently:
**0 unquoted occurrences.** `T-C05-66` is falsifiable in both directions (a producer that emits a
higher revision carrying the new key is a failure, not a variance). **Genuinely resolved.**

---

## 5. D-4 — audio ownership · **DISAGREE**

**Clauses:** §5.2 row 5 (corrected); §5.2 row 6; `TN-C-15`; §6.1 audio row; `DV-22`.

### 5.1 What was fixed, and it is most of it

Three of my four sub-findings are closed, and closed well:

- **Row 5 loses audio** and now states positively *"**Agent 1 owns no audio responsibility in
  C-05**"*, with the correction recorded inline rather than silently.
- **Row 6** becomes the only row owning audio and names its obligations by ID.
- **`TN-C-15`** is added — the obligation whose absence I flagged. It correctly scopes cue selection
  to the phase transition, keys the asset lookup to identity fields outside C-05, and forbids a cue
  on a retime. `T-C05-67` asserts single ownership.
- **S4 explicitly declines** to invent a camera-relative audio responsibility for Agent 1, on the
  ground that *"no source assigns it to Agent 1, and inventing it would be the scope expansion this
  disposition forbids."* **That is the right call** and I want it on the record: I floated that
  possibility as an option and S4 correctly refused it rather than manufacturing a responsibility.

### 5.2 The defect that survives

**`§8`'s preamble still assigns audio to Agent 1.** Line 549, unmodified:

> *"**Each obligation is implemented by each consuming agent in its own code** — Agent 1 for
> defence, dodge, camera **and audio**; Agent 2 for AI reaction, audio cue, montage trigger and VFX
> timing."*

This is the **third** location where audio was assigned to Agent 1, and it is the only one S4 did
not edit. §5.2 row 5 now says Agent 1 owns no audio; §8's preamble — the head of the section that
*contains* `TN-C-15` — says Agent 1 implements audio. The two sentences are 40 lines apart in the
same document.

**Why `DV-22` did not catch it.** `DV-22` checks *"row 5 contains no audio claim", "row 6 owns
audio", "`TN-C-15` exists and its implementer is `Agent 2, C-05 consumer`"*. All three are true.
`DV-22` is scoped to the **ownership table and the obligation row**, and §8's preamble is neither.
So the instrument reports `PASS` on a document that still contains the defect it was written for —
**the same failure mode as S3's `DV-11`**, which is precisely the pattern S4 was asked to break.

This is not a cosmetic inconsistency. §8's preamble is the first thing a reader of the consumer
obligations sees, and it tells them Agent 1 implements audio. An implementer following §8 rather
than §5.2 would build an Agent 1 cue path — the exact duplicate ownership `TN-C-15`'s *"Agent 2
alone"* forbids.

### 5.3 Closure condition (D-4)

**Required:** delete *"and audio"* from §8's preamble, so it reads *"Agent 1 for defence, dodge and
camera; Agent 2 for AI reaction, audio cue, montage trigger and VFX timing."* One phrase.

**Required, so this cannot recur a fourth time:** extend `DV-22` to grep the **whole document** for
any clause associating Agent 1 with audio outside a quoted correction, and fail on a hit. The
present check is scoped to two structures; the defect lives in a third. Without the widened check,
DV-22 will keep passing on a document that keeps saying it.

**Not required, and I am not asking for it:** any change to §5.2 or `TN-C-15`. Those are correct.

---

## 6. D-5, D-6 and C9 — token mapping and `DV-11` · **AGREE / AGREE WITH CONDITIONS**

### 6.1 D-5 — implementer-token mapping · **AGREE**

**Clauses:** §5.4 (new token `Agent 2, C-05 consumer` → row 6); `TN-C-12`, `TN-C-13`, `TN-C-15`
cells re-mapped.

The new token is exactly what I asked for, and S4 took the option that makes the distinction
*encoded* rather than *prose*:

| Token | Row | Scope |
|---|---|---|
| `Agent 2, C-05 consumer` | **row 6** | inside C-05: consumer integration |
| `Agent 2, in its own systems` | **row 7** | outside C-05: placement, assets, tuning |

`TN-C-12`, `TN-C-13` and `TN-C-15` now carry the row-6 token. I verified all 43 implementer cells
parse against the §5.4 table: **0 undeclared tokens, 0 row violations.** **Genuinely resolved.**

### 6.2 D-6 — is `DV-11` now row-level? · **Yes, verified by simulation**

I did not take §13's `PASS` on trust. I extracted the §5.4 token→row mapping from the document and
re-implemented `DV-11`'s stated rule — token declared; token's row ∩ allowed-row set for the
obligation's prefix; row owner matches — then ran it over all 43 cells:

```
declared tokens : 7
observed tokens : 5
failures        : 0
declared-unused : ['Agent 2, in its own systems', 'contract layer, owner pending TD-12']
```

**It is genuinely row-level and it genuinely passes.** I also confirmed the discriminating power
that S3's check lacked: `TN-C` allows rows {5, 6}; a `TN-C` obligation carrying the row-7 token
would fail. Rows 6 and 7 share the owner, so an agent-level check could never catch that — a
row-level check does. **The specific mechanism I asked for is present.**

**The §13.2 tamper proof is real and is the strongest thing in this document.** S4 ran the new
checker against **S3**, the blob it must reject, before running it against itself:

```
DV-11 FAIL — 6 declared / 5 observed tokens, 38 cells; failures
  ["TN-C-12: token 'Agent 2, in its own systems' maps to rows [7], allowed for TN-C are [5, 6]",
   "TN-C-13: token 'Agent 2, in its own systems' maps to rows [7], allowed for TN-C are [5, 6]"]
10/23 checks passed
```

The instrument **names both mis-mapped obligations** and **reproduces the S3 miscount** (6 declared
vs 5 observed). This is a check with a demonstration that it can fail, which is what I said S3
lacked. It also states, rather than hides, that `DV-12` passes on S3 too.

### 6.3 Condition D-6a — `§1` row 6 reports the wrong observed count

Two of S4's own summaries disagree, and one is arithmetically wrong:

| Location | Says | Correct? |
|---|---|---|
| **§1 row 6** | *"7 declared, **6 observed**"* | **No** — 5 tokens appear in cells |
| §2.1 D-6 | "7 declared / 5 observed" | ✔ |
| §2.2 C9 | "7 declared / 5 observed" | ✔ |
| §5.4 prose | "declares **seven**; **five appear**" | ✔ |
| §13 `DV-11` | "7 declared / 5 observed tokens" | ✔ |
| §18.1 Q9 | "7 declared / 5 observed" | ✔ |

I counted the 7th cell of all 43 obligation rows: **`producer owner` 23, `each consumer` 12,
`Agent 2, C-05 consumer` 3, `Agent 1, subject to TD-09` 3, `Agent 1, shared support` 2 = 5 distinct.**
§1 row 6 is the sole outlier, and it is wrong in the direction that flatters the instrument — it
reports one more token as used than are used.

**This is the third consecutive revision in which the `DV-11`/token-count narrative has contained an
arithmetic error** (S2's DV-8: 10 vs 16; S3's DV-11: 6 vs 5; S4's §1: 6 vs 5). The instrument is now
correct; the *prose summarising* it is not. That pattern is itself the finding.

**Closure condition (D-6a).** Correct §1 row 6 to *"7 declared, 5 observed"*. Then generate the
count in the summary tables **from the same extraction `DV-11` uses**, rather than restating it by
hand — otherwise a fifth recurrence is likely.

### 6.4 Condition D-6b — `§5.4`'s "Used by" column has two imprecise tallies

Not load-bearing, but they are counts in a table whose purpose is to be checkable:

| Token | §5.4 "Used by" | Actual cells |
|---|---|---|
| `producer owner` | "19 `TN-P` rows" | **23** cells — 19 `TN-P` **+ 4 `TN-R`** |
| `each consumer` | "11 `TN-C` rows" | **12** `TN-C` cells |

Both under-report. Neither is a false mapping — the mapping is right; the tally omits rows. The
`producer owner` omission is the more misleading of the two, because `TN-R-02`/`-03`/`-04`/`-05`
are genuine read-surface obligations implemented by the producer owner.

**Closure condition (D-6b).** State the totals as *"23 cells (19 `TN-P`, 4 `TN-R`)"* and *"12
cells"*, or drop the column and let `DV-11` print the counts.

### 6.5 C9 — overall · **AGREE WITH CONDITIONS**

My C9 had two halves. **Both mechanisms are now correctly built**: the row-level check exists and
passes, and the declared-vs-observed separation exists and is reported. What remains is that the
counts *surrounding* the instrument are wrong in three places (§1, §5.4 × 2) while the instrument
itself is right. **The check is fixed; the reporting is not yet trustworthy.** Conditions D-6a,
D-6b.

---

## 7. C4a, C4c and C6 reassessed

### 7.1 C4a — `INV-1` / `INV-2` · **AGREE**

**C4a-1 (precondition in the clause) — resolved.** `INV-2` (§4.6) now carries it in the operative
sentence: *"**`INV-2` holds only while `ProducerRate` and `PhaseEndAxis` are fixed, i.e. within a
single revision**… a consumer aging a snapshot across a revision change it has not yet adopted is
aging with stale `VF`, and its obligation is limited to the revision it holds."* `TN-C-10` echoes
it in its requirement and failure columns. The precondition I asked to be moved from rationale into
the clause has been moved. **Genuinely closed.**

I re-verified the algebra again at four axes; the two forms remain identical and all clamps hold.

**C4a-2 (`VF` list in three homes) — resolved.** §3.2 is now the normative list; the `Timing` struct
comment and `INV-1` both quote all seven names explicitly and point at §3.2; `DV-12` extracts all
three and requires **set equality** (reported "§3.2=7 INV-1=7 struct=7; sets equal True"). I
re-derived the three sets independently and they are equal. **Closed.**

**New finding (advisory, not a defect):** `DV-12` passing on S3 as well is stated honestly by S4 —
the `VF` set was already consistent. So `DV-12` is a **drift guard**, not a defect detector, and
its `PASS` should not be read as evidence that the S3 problem was real. S4 says this. Good.

### 7.2 C4c — same-frame ordering · **AGREE WITH CONDITIONS**

**C4c-2 (`PO-3` content) — resolved** by `PO-5`; see §3 above. **Closed.**

**C4c-1 (`EX-5` case (d)) — resolved**, with conditions D-1a/D-1b above.

#### New finding C4c-N1 — `PO-5` falsifies the stated reason for `PO-3`, which is unchanged

This is a **new** inconsistency created by S4's own fix, and it is not in the closure matrix.

§3.6 gives three reasons for the canonical order. Reason **(b)** is:

> *"(b) Within one frame the producer's internal application order is **not observable** at frame
> granularity, so leaving it to the producer would let two conforming producers emit different
> sequences for identical gameplay…"*

`PO-5` **makes the internal application order observable.** It requires the producer to publish
*between* applications, and obliges *"a pull taken between two publications of the same frame
[to] return the earlier revision's `VF` exactly"*. `T-C05-65` then **observes** it explicitly: pull
after the transition sees the old rate under `n+1`; pull after the dilation sees the new rate under
`n+2`. That is the internal application order, made visible by the contract's own new test.

So reason (b) now asserts something that the same section's new rule contradicts.

**Severity: low-to-medium, and I want to be precise about why.** The *rule* `PO-3` is not wrong and
is not weakened — reasons (a) and (c) survive, and sequence determinism for stream consumers is
still the operative justification (which message lands at `n+1` decides whether entry fires). What
is wrong is a **stated premise**, and it points the wrong way: an implementer reading (b) could
conclude the application order is unconstrained and internally reorder freely, which `PO-5` now
forbids. A false justification attached to a correct rule is a real hazard, not pedantry.

**Closure condition (C4c-N1).** Rewrite §3.6 (b) to the reason that is still true: *"the internal
application order **is** observable through a mid-frame pull once `PO-5` is in force, so leaving the
publication order to the producer would let two producers that applied the same two changes in
different orders expose different revision sequences for identical gameplay."* Optionally note that
`PO-5` requires the application order to *follow* the publication order, which is a stronger
constraint than `PO-3` alone states. Two sentences in one bullet.

### 7.3 C6 — identity and audio · **AGREE WITH CONDITIONS**

- **C6-1 (constancy) — resolved.** See §4. `TN-P-19` names the change path; `TN-P-07` drops the dead
  clause; `T-C05-62`'s rows become a falsifiable close-and-reopen assertion. S4 recorded the
  disagreement with my recommended wording and gave a reason — that its form is testable where mine
  is not — and **the reason is correct.** Closed.
- **C6-2 (audio) — not resolved.** See §5. `DISAGREE`.

---

## 8. The `TN-C-11` / `TN-A-01`/`TN-A-02` conflict and `C05-6.4` — outside my seven, assessed because it is new

S4 adds `C05-6.4`, rewrites `TN-C-11`, extends `TN-A-02` and adds `TN-A-03`. This was not one of my
findings, but it changes text I reviewed in S3, so I checked it.

**The conflict was real and S4's resolution is sound.** S3's `TN-C-11` said a consumer must take
"blockability" from `AttackTag`, while `TN-A-02` allows no arbitration decision to depend on a C-05
value. Read literally those collide. The three-domain separation — **creation** (producer authors
the tag) / **selection** (consumer may use it to choose what to *attempt*) / **outcome** (nothing
from C-05 may decide what *happened*) — draws the line where it belongs, and the one-sentence form
is the clearest statement in the document:

> *"a consumer may use `AttackTag` to decide what to attempt; nothing may use it — or any other C-05
> value — to decide what happened."*

I verified the four things that could have gone wrong:

| Check | Result |
|---|---|
| Does any clause let a C-05 value decide a hit? | **No** — `TN-A-02`, `TN-A-03` name `AttackTag` explicitly as forbidden |
| Is selection still usable after a resync? | **Yes** — `TN-C-11` keeps it, `EX-7` and `T-C05-57` exercise it |
| Did the arbitration boundary move? | **No** — `C05-6.1`/`TN-A-01` unchanged; only descriptive clauses gained text |
| Is TD-09 reopened? | **No** — §14.1 B-2 still `OPEN`; C-05 says only that the decision is not C-05's |
| Does `TN-A-03` presuppose an architecture or module? | **No** — it names inputs, not components; MEAD-neutral |

`T-C05-63` is the right falsifier: same outcome under an honest tag, a corrupted tag, and a held
snapshot, with a spy showing **zero** C-05 reads on the hit-resolution path.

**The provenance handling deserves credit.** §9.2 states plainly that Agent 3's review is not in the
repository, that this is **S4's own resolution and not Agent 3's wording**, and that B-15 asks Agent
3 to confirm or replace it. That is exactly the right way to resolve a conflict whose other party's
text is unavailable: resolve it, disclose the authorship, and leave the door open. **I have no
objection to `C05-6.4`.** Whether it satisfies Agent 3 is theirs to say and I do not speak for them.

---

## 9. Independent verification of S4's counts

Every figure below I re-derived from the text. **Where a document check and my result differ, it is
reported here and nowhere else.**

| Claim | My method | Result |
|---|---|---|
| **43 obligations**, 19 P / 15 C / 6 R / 3 A | parse `| **TN-x-nn` rows from §§7–9 | **43**, exact split ✔ |
| **67 cases**, 18 suites, case sum 67 | parse suite table, sum `Cases` | **18 / 67** ✔ |
| Case ids 01–67 complete | regex all `T-C05-nn` | 67 distinct, no gaps, none extra ✔ |
| **§11.2 bidirectional** | invert both directions incl. prefixed ranges | 43 obligations covered, 67 cases covered, 0 orphans ✔ |
| No case in two suites | case→suite map | none ✔ |
| **23 document checks**, `DV-1`…`DV-23` | count `| **DV-nn**` rows in §13.1 | **23** ✔ |
| **`DV-11` row-level, 7 declared / 5 observed, 0 failures** | re-implement the stated rule over 43 cells | **matches** ✔ |
| `DV-12` three-home `VF` set equality | extract §3.2, `INV-1`, struct comment | **all 7, sets equal** ✔ |
| `DV-23` unquoted rejected phrase = 0 | search "constant for the lifetime" outside quotes | **0** ✔ |
| `INV-2` algebra at 4 axes | recompute both forms | identical, clamps hold ✔ |
| **`§1` row 6: "6 observed"** | count distinct 7th-cell tokens | **5 — does NOT match** ✗ (D-6a) |
| **`§5.4`: "19 TN-P rows" / "11 TN-C rows"** | per-token breakdown | **23 / 12 — does NOT match** ✗ (D-6b) |
| `DV-22` audio single owner | full-document search | **fails: §8 preamble** ✗ (D-4) |

**These are document-text and arithmetic checks, not acceptance tests.** No contract behaviour is
exercised. **All 67 cases are `PROPOSED / NOT RUN`; 0 executed, by Agent 1, by me, or by anyone.**
**I do not claim any case passed.** The three `✗` rows are the findings in §5 and §6.

---

## 10. Remaining defects and closure conditions

| # | Defect | Clause | Closure condition | Severity |
|---|---|---|---|---|
| **D-4** | §8 preamble still assigns audio to Agent 1; `DV-22` cannot see it | §8 preamble; `DV-22` | Delete "and audio"; widen `DV-22` to whole-document search | **Blocking** — duplicate ownership of a contract responsibility |
| **D-6a** | §1 row 6 reports "6 observed" where 5 tokens are used | §1 row 6 | Correct to 5; generate summary counts from `DV-11`'s extraction | **Blocking** — false figure about an instrument |
| **C4c-N1** | `PO-5` makes application order observable, falsifying §3.6 (b)'s stated premise | §3.6 (b) | Rewrite (b) to the still-true reason | **Material** — false justification for a correct rule |
| **D-1a** | "bounded by one frame, by construction" reads as a same-frame guarantee | `TN-C-14` | State it is an upper bound; or pin both pull positions in `T-C05-64` | Minor |
| **D-1b** | timing-dependent vs message-only classification is undefined | `TN-C-14` | Make it a property of the call site, not of the agent | Minor |
| **D-6b** | §5.4 "Used by" tallies omit rows (19 vs 23; 11 vs 12) | §5.4 | State full cell counts or drop the column | Cosmetic |

**Nothing here reopens a settled requirement.** D-4 is a one-phrase deletion plus a check widening;
D-6a is one number; C4c-N1 is one bullet. D-1a/D-1b/D-6b are wording. **All six are closable inside
existing clauses.**

**Outcome: `TARGETED REVISION`.** Why not `PASS`: D-4 is a live duplicate-ownership defect in the
contract text and a validation instrument reports `PASS` on it — the exact failure class S4 was
asked to eliminate. Why not `BLOCKED BY DEPENDENCY`: none of the six needs a TD decision. B-11
(C-04), B-12 (resync routing), B-13 (tag registry) and B-15 (Agent 3's wording) are correctly
recorded and none gates these six.

---

## 11. Answers to the specified verification points

| Verification point | Result |
|---|---|
| **One-pull-per-frame bound and residual staleness under D-1** | **Bound holds** as an upper bound, and holds *because* `PO-5` exists. Residual is stated, quantified by the retime ratio, and accepted. Conditions D-1a (upper-bound wording), D-1b (classification). |
| **`PO-5` and per-message `ProducerRate` under D-2** | **Both present and correct.** `PO-5` is normative in §4.9 and §3.6 and operationalised by `TN-P-18`; `T-C05-51` asserts `ProducerRate` per message; `T-C05-65` adds the mid-frame pull and a batching negative control. Reading A/B collision resolved. One consequence: C4c-N1. |
| **Fixed identity and close-and-reopen under D-3** | **Fully consistent** across §3.8, §6.1, `TN-P-07`, `TN-P-19`, `TN-P-04`, `EX-12`, `T-C05-66`, `T-C05-62`. Dead norm removed; previously untestable rows replaced by a falsifiable assertion. |
| **Audio ownership** | **Not resolved.** §5.2, §6.1 and `TN-C-15` are correct; **§8's preamble is not**, and `DV-22` is scoped too narrowly to catch it. **D-4, blocking.** |
| **Token mapping** | **Resolved.** 7 declared, 5 observed, 43 cells, 0 undeclared, 0 row violations — verified by independent re-implementation, not by reading `DV-11`'s `PASS`. |
| **`DV-11`'s actual row-level validation** | **Genuinely row-level**, with a real tamper proof against S3 that names both mis-mapped rows and reproduces the S3 miscount. The mechanism I asked for exists. |
| **Consistency of all validation counts, including 7 declared / 5 observed** | **The instrument is right; three surrounding tallies are wrong** — §1 row 6 (6 vs 5, D-6a), §5.4 (19 vs 23 and 11 vs 12, D-6b). All other figures — 43 / 67 / 18 / 23 / 43-cells / three-home `VF` — **reconcile exactly**. |
| **Document checks vs behavioural acceptance tests** | Kept separate throughout, as §13.3 itself insists. **23 document checks are text/arithmetic checks. 67 acceptance cases are `PROPOSED / NOT RUN`, 0 executed.** No behavioural claim is made in this review and none is inherited. |
| **Pinned to the exact blob** | `424d2c69df62ebc1930eacd0ba67077c854ab31e` at `4692e973`. Tip `d72831e7` differs only by 6/6 placeholder-fill lines, verified by diff. |

---

## 12. What I did and did not do

**Did:** reviewed blob `424d2c69…`, verified by `git rev-parse` and diffed to the tip; read all 1,165
lines; re-derived `INV-2`; re-implemented `DV-11`'s row-level rule over all 43 cells rather than
accepting its `PASS`; recounted every total; traced the `TN-C-14` bound through `PO-5`/`TN-P-11`/`AD-1`;
checked D-3 across all four locations; searched the whole document for surviving audio assignments.

**Did not:** edit any Agent 1 document (all verified byte-identical); sign, freeze, merge or
implement C-05 — **I am not signing v4.0**; select a MEAD or make a TD decision; close U-07; run or
claim any of the 67 acceptance cases; overwrite `Docs/AGENT2_REVIEW_A1C05_S3_V1.md`; reopen any
settled requirement; accept `C05-6.4` on Agent 3's behalf; or confirm Agent 1's closure matrix
without independent verification.

**One process note I am putting on the record.** For the third revision running, a count attached to
the `DV-11` narrative has been wrong while the mechanism was right. S4 fixed the mechanism and
demonstrated it failing on S3 — genuinely good practice — and then mis-summarised it in §1. The
lesson is not that the instrument is unreliable; it is that **hand-restated counts drift away from
the instrument that computes them.** Generating those figures from the extraction would close the
class, not just the instance.

### 12.1 A correction I am making to my own published S3 review

While confirming that S3's baseline was unmodified, I found that **`Docs/AGENT2_REVIEW_A1C05_S3_V1.md`
and `Tools/world/tests/test_review_a1c05_s3.py` carried a mis-transcribed blob hash.** Both gave the
S3 branch-tip blob as `80060de6…`. The actual value is:

```
$ git rev-parse ec3c2af7455db614f7c9090fbe3c7033cd2fcaf8:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md
80060dea6685f2f17cae1128ef1a4532eed4e316
```

**`80060de6…` does not exist as an object in this repository**; `80060dea…` does. The substantive
finding was unaffected — the diff of `07723236` against `80060dea` is still **3 insertions, 3
deletions**, all `PUB_COMMIT`/`PUB_BLOB` placeholder fill, which is what I claimed — but the
identifier was wrong, and an identifier that does not resolve is a citation defect regardless of
whether the conclusion survives it.

I have corrected the hash in both files and added a regression test to each review's suite asserting
that the recorded tip hash **resolves via `git rev-parse` to the recorded value**, so a transcription
error of this class fails a test rather than sitting in a published review.

**This is the second time in this engagement that a short-hash or transcription error has produced a
false or unsupported citation from me** (the first being the `d32660f` retraction in W-M2.10). The
pattern is specifically hashes copied by hand rather than derived from `git rev-parse` at write time.
The regression tests now derive them.

**Status:** `DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD
is selected.** TD-06, TD-09 and TD-12 remain external blockers, untouched by this review.

---

*End of review. `TDD-A2-REVIEW-A1C05-S4-001` v1.0.*
