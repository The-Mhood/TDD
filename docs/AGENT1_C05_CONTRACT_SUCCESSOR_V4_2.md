# Agent 1 — C-05 Successor `A1-C05-S4.2`

**Response ID:** `TDD-A1-C05-SUCCESSOR-004.2`
**Version:** 4.2 — **targeted revision** answering both independent reviews of S4.1 (`TDD-A2-REVIEW-A1C05-S4-1-001` and Agent 3's independent integration review) and the TD's six consolidated corrections. Current C-05 position.
**Date:** 2026-11-16 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Scope:** **Agent 2's seven defects `D-1`…`D-7` and their conditions (`C4a-1`, `C4a-2`, `C4c-1`, `C4c-2`, `C6-1`, `C6-2`, `C9`), plus Agent 3's `TN-C-11` / `TN-A-01`-`TN-A-02` conflict** — no other change. No new architecture layer, no history, no event bus, no scheduler, no implementation. **S4.2 changes no obligation's count and adds no obligation: it corrects one normative clause's measurement rule (`TN-C-14`), one rationale bullet (§3.6(b)), one ownership row (§5.2 row 5), one ownership preamble (§8), two proposed test specifications (`T-C05-63`, `T-C05-64`), three validation instruments (DV-20, DV-22, plus new DV-24) and the publication metadata. Every change and its reviewer source is in §2.5–§2.7.**
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no C++, no Unreal project, no API or contract freeze, **no MEAD selection**, no signature, no merge, no M0 claim. **C-05 remains proposed, unsigned and unfrozen; U-07 remains open.**

---

## 0. Provenance and scope lock

### 0.1 What this revision answers

| Field | Value |
|---|---|
| **Baseline under revision** | `A1-C05-S3` v3.0 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md`, blob **`077232368c42b2cd910be2c9642ba05cd7faa382`** at `a6b4e22999c7f8622c7c67e9cdc39e2f57565c20`; **preserved unmodified** |
| **Immediate predecessor (both reviews pinned its blob)** | `A1-C05-S4.1` v4.1 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md`, blob **`d54e194affeaee98b1030e2b83b4c34e234fa382`** at **`95918268ed5b20b878fef3ee0a7855ad18e6eeb6`**; **preserved unmodified**. Both reviews verified this exact blob: Agent 2 `TDD-A2-REVIEW-A1C05-S4-1-001` (commit `eee9401`) and Agent 3 (commit `34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a`) |
| Predecessor (older) | `A1-C05-S4` v4.0 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md`, blob `424d2c69df62ebc1930eacd0ba67077c854ab31e` at `4692e973d04a94d7781677c704e7a0198abd2d70` — **preserved unmodified** |
| **Agent 2's targeted review of S3** | `TDD-A2-REVIEW-A1C05-S3-001` v1.0 — `Docs/AGENT2_REVIEW_A1C05_S3_V1.md`, **813 lines, read in full**; commit `47dbdffb8a52aa0c20adc2105a28b4b5466685ac`; outcome **`TARGETED REVISION`**, 7 defects `D-1`…`D-7`, conditions `C4a-1/2`, `C4c-1/2`, `C6-1/2`, `C9` not resolved |
| Agent 2's prior review (S2) | `ac498ce` — `Docs/AGENT2_REVIEW_A1C05_S2_V1.md`, 686 lines; its conditions C1–C9 are the subject of S3 and are re-adjudicated in A2's S3 review |
| **Agent 3's targeted review of S3** | **NOT PRESENT IN THE REPOSITORY** — see §0.2. Its `TN-C-11` / `TN-A-01`-`02` conflict is addressed in §9.2 from the conflict's own terms, **not from their wording**, which I do not have |
| My predecessors | `A1-C05-S2` v2.0 at `e5ddad6`, blob `bf6c8fb3…`; `A1-C05-S1` v1.0 at `2bb729f`, blob `dcec9e1a…` — **both preserved unmodified** |
| Agent 2's submission | `A2-C05-1.0` at `3ac438b32fcd73ceb22dcd81385356f7b8b39644` — §7.1, §7.3, §7.6 |
| Aging-formula source | `A1-R4` §3.3(e) — `docs/AGENT1_CONTRACT_SUBMISSION_RESPONSE_V4.md`, blob `2cc548faf86cb9b30cd2e26386fc672edbdd9f75`, lines 143–167 |
| MEAD-A — `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **not selected**; at `586152b` (`arena/5dde91a4-tdd`), blob `bd0f3afdf24736349f2045bf0ee423ee0b4e1a78`, read only |
| MEAD-B — `docs/MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **not selected**; at `1eb613f` (`arena/c64fc525-tdd`), blob `1e8d1bd1b223c364c02464f6036e3f9ee9a9b0a7`, read only |
| MEAD-C — `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | candidate, **none selected**; this branch, blob `f49354631c86601e9311865901bf1fcd44846d89`, read only |

### 0.2 Agent 3's S3 review is not in the repository — and that constrains this revision

The disposition refers to Agent 3's `TN-C-11` versus `TN-A-01`/`TN-A-02` conflict and to *"Agent 3's proposed wording"*. **I could not read that review, and I will not invent its text.** Checked at the time of writing, four ways:

```
$ git ls-remote --heads origin
ec3c2af…  refs/heads/arena/3bc206a0-tdd
47dbdff…  refs/heads/arena/5dde91a4-tdd
1eb613f…  refs/heads/arena/c64fc525-tdd      <- Agent 3, unchanged since the S1 assessment
5e3d1da…  refs/heads/main
$ git log --oneline -4 origin/arena/c64fc525-tdd
1eb613f Assess A1-C05-S1 integration readiness      <- the S1 document, not an S3 review
58ec7fd Add C-05-3 telegraph authority recommendation
98399af Add v3 contract reconciliation and response ledgers
d32660f docs: reconcile cross-agent contracts v2
$ gh api repos/The-Mhood/TDD/contents/docs?ref=arena/c64fc525-tdd --jq '.[].name' | grep -i agent3
AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md
AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md
$ gh pr list --state all
(no pull requests)
```

**What I did instead, and what it means for the record:**

1. I **derived the conflict from the S3 text itself**, where it is real and visible without any review: `TN-C-11` required every consumer to take "blockability" from the snapshot's `AttackTag`, while `TN-A-02` forbade any arbitration decision depending on a C-05 value. Both cannot be true unless "blockability used to choose a response" is separated from "blockability used to decide a hit's outcome".
2. I **resolved it** with a three-domain separation and a new normative clause `C05-6.4`, and I **independently verified** that the resolution preserves both boundaries (§9.2, DV-20, T-C05-63).
3. **I did not put words in Agent 3's mouth.** No sentence in this document is attributed to Agent 3's S3 review, and §18.2 asks them to confirm this resolution or substitute their own wording. **If their text differs materially, this is the one section that will need re-cutting**, and I say so rather than letting a later reader assume agreement.

This is recorded as dependency **B-15** in §14.2.

### 0.3 What Agent 2 found in S3, and what I am doing about it

Agent 2 returned **`TARGETED REVISION`**: 7 AGREE (C1, C2, C3, C4b, C5, C7, C8), 3 AGREE WITH CONDITIONS (C4a, C4c, C6), 1 DISAGREE (C9), and **seven defects `D-1`…`D-7`**, all closable without reopening a settled requirement. They explicitly did **not** sign v3.0 and stated that agreement is not inferred from direction of travel.

Every one of the seven is closed here. Three of them changed what an implementer would do, and each required a decision rather than a rewording:

| Defect | The decision S4 makes |
|---|---|
| **D-1** (lost retime → silent stale rate) | Accept the residual and **bound it**: new `TN-C-14` requires a timing-dependent consumer to re-pull at least once per frame, capping staleness at one frame; plus an explicit statement that message-only consumers accept stale-rate risk. Case **(d)** added to `EX-5`. |
| **D-2** (`PO-3` fixes order, not content) | New **`PO-5`**: publication is **interleaved with application**, so a message at `n+1` carries exactly the changes applied up to `n+1`, and live state may never contain an unpublished `VF` change. Reading B becomes the only legal reading, and reading A becomes a violation. |
| **D-3** (identity "constant" vs `TN-P-07`'s identity clause) | **Constancy chosen**, with the change path named: a change of attack identity is a **close-and-reopen** (`TN-P-04`), never a mid-instance revision. `TN-P-07`'s identity clause is removed; `T-C05-62`'s identity rows are replaced by a testable close-and-reopen case. Agent 2 recommended mutability; the reason for differing is in §2. |
| **D-4** (audio owned twice) | Row 5 loses audio; row 6 keeps it; and the missing obligation is added as **`TN-C-15`** (cue selection from identity, never on a retime). |
| **D-5** (`TN-C-12`/`TN-C-13` mapped to the outside-C-05 row) | New token **`Agent 2, C-05 consumer`** → row 6; both re-mapped. `Agent 2, in its own systems` keeps row 7 and now maps only the outside-C-05 half. |
| **D-6** (`DV-11` agent-level, cannot fail on rows 6 vs 7) | `DV-11` is **row-level**: it checks each obligation's prefix against an allowed row set and the token's mapped row against it, so a `TN-C` obligation carrying the outside-C-05 token **fails**. It also reports declared and observed token counts separately (7 declared, 5 observed, 2 declared-but-unused by design). |
| **D-7** (`INV-2` states its equivalence unconditionally) | The one-revision precondition goes **into `INV-2` itself**, and `TN-C-10` echoes it. |

**Plus the advisory `C4a-2`:** `DV-12` now compares the versioned-field set across all three homes (`INV-1`, §3.2, the §4.2 struct) and fails on drift.

**What I am not doing:** re-arguing verdicts, treating the review as a rejection of S3's substance (Agent 2 calls the `INV-2` correction *"better than what I asked for"*), converting any finding into a TD decision, or claiming that Agent 2 or Agent 3 agrees with S4.

### 0.4 Scope lock — what is preserved verbatim

| Preserved | Where |
|---|---|
| Per-instance, no-history pull recovery | `C05-2.4`, `RS-1`/`RS-2`/`RS-3`, §4.4, §4.6 |
| `StateRevision` and complete-snapshot messages | `C05-2.2`, `C05-2.3`, `TN-P-07`, `TN-P-13`, `TN-P-14` |
| `VF`/`OF` split, `INV-1` over the versioned class | §3.2, §3.3, §4.6 |
| `TM-1`, `EN-1`/`EN-2`/`EN-3`, `AD-1`/`AD-2`, lifecycle semantics | §4.6, §4.7 |
| MEAD neutrality — no module, no class, no candidate selected | `C05-2.2`, §5.1, DV-9 |
| Arbitration separated from telegraph production | `C05-6.1`, `TN-A-01`, `TN-A-02`, **new `C05-6.4`**, §9.2 |
| Conditional X-1 | `TN-R-03`, §14.1 B-5 |
| Directory scope, not-a-scheduler, deregistration triggers | `DN-1`, `DN-1a`, `TN-R-01`, `TN-R-06` |
| The ownership split, except the row-5 audio correction and the token re-mapping | §5.2, §5.4 |
| Every earlier document, byte for byte | §17 |

### 0.5 S4.1 — the single correction, stated exactly

**Preserved as S4.1's own record, with one note:** the checker path it names (`/home/user/dv4.py`) no longer exists and was outside the repository, so no reviewer could reach it. S4.2 publishes the checker at `docs/validation/dv_c05.py` (§13, §17) and its 27 checks supersede that file's 23; **the figures in this subsection are S4.1's and are correct for S4.1.**

TD review of S4 found **one** documentation inconsistency. It is corrected here and nothing else is touched.

| | |
|---|---|
| **Where** | §1, the ten-corrections table, row **6** (`DV-11`) |
| **S4 said** | "declared vs observed tokens separately (**7 declared, 6 observed**)" |
| **Correct value** | "declared vs observed tokens separately (**7 declared, 5 observed**)" |
| **Source of truth** | §13.1's DV-11 row — the actual output of `python3 /home/user/dv4.py` on this document: *"7 declared / 5 observed tokens, 43 cells"*; §5.4's token table; §2's `D-6` row; §18.1's C9 question. The checker counts **distinct tokens appearing in implementer cells**: five do, and the two that do not — `Agent 2, in its own systems` (row 7) and `contract layer, owner pending TD-12` (row 3) — carry no obligation row by design |
| **How S4 came to be wrong** | §1's cell was written from a draft estimate made before the checker was first run. When the run produced 5, §0.3, §2, §5.4, §13 and §18 were brought into line and **this one cell was missed** — a summary line disagreeing with the instrument, not a failed check and not a revised result |
| **What changed in S4.1** | that single parenthetical: `6 observed` → `5 observed`. **One cell.** |
| **What did not change** | every normative clause; `TN-C-11`, `TN-A-02`, `TN-A-03`, `TN-P-18`, `T-C05-63`; the `D-1`…`D-7` resolutions and all seven conditions; the `C-04` dependency and the status of **B-11** and **B-15**; every count (43 obligations, 18 suites, 67 cases, 23 document checks); every validation result, including DV-11's PASS on this file and its recorded FAIL on the S3 blob; the scope lock of §0.4; and every earlier document |
| **Instrument added** | **none.** A permanent check that every declared/observed sentence equals the checker's output would be a new validation instrument (DV-24) and would change §13's count of 23 — outside a targeted documentation correction. It is **recommended** in §18.3 and not performed |
| **Verification** | `DV-11` re-run on this file: *7 declared / 5 observed*, PASS. The scan claim is stated so that it cannot itself drift: **every statement of DV-11's output for S4/S4.1 in this document reports 5 observed**, and the only lines still showing the old figure are the two rows of this table that quote and explain it; §13.2's S3 transcript reads *6 declared / 5 observed*, where the 6 is S3's true **declared** count. `grep` reproduces both facts |

---

## 1. The ten corrections at a glance

Every row is expanded, with its closure evidence, in §2.

| # | Correction | Closes | Section |
|---|---|---|---|
| **1** | **`PO-5`** — publication is interleaved with application; each message carries the changes at or before its own revision and live state may never hold an unpublished `VF` change | **D-2**, C4c-2 | §3.6, §4.9, `TN-P-18` |
| **2** | **`EX-5` case (d)** — only `n+1` received: adopt, entry once, no gap; **`TN-C-14`** bounds rate staleness to one frame for timing-dependent consumers, and the residual for message-only consumers is stated rather than hidden | **D-1**, C4c-1 | §3.6, §10.5, `TN-C-14` |
| **3** | **Identity is fixed for the instance's lifetime**; a change of attack identity is a close-and-reopen (`TN-P-04`), never a mid-instance revision. `TN-P-07`'s identity clause removed; `T-C05-62`'s identity rows replaced by a close-and-reopen case | **D-3**, C6-1 | §3.8, §6.1, `TN-P-19`, T-C05-66 |
| **4** | **Audio has one owner.** Row 5 loses "audio cues"; row 6 keeps cue selection; **`TN-C-15`** is added to cover cue selection, which no obligation covered | **D-4**, C6-2 | §5.2, `TN-C-15`, T-C05-67 |
| **5** | **New token `Agent 2, C-05 consumer`** → row 6; `TN-C-12` and `TN-C-13` re-mapped to it, so the inside/outside-C-05 distinction is carried by the token rather than by prose | **D-5** | §5.4, §7–§8 |
| **6** | **`DV-11` is row-level**, with an allowed-row set per obligation prefix, and reports declared vs observed tokens separately (7 declared, 5 observed) `[CORRECTED at S4.1: the summary cell said 6; the instrument says 5 — §0.5]` | **D-6**, C9 | §5.4, §13 |
| **7** | **`INV-2` carries its one-revision precondition in the clause**, and `TN-C-10` echoes it | **D-7**, C4a-1 | §3.4, §4.6, `TN-C-10` |
| **8** | **`DV-12` compares the `VF` set across all three homes** and fails on drift | C4a-2 | §13 |
| **9** | **New `C05-6.4` — `AttackTag` is descriptive, not decisive**, with a three-domain separation (creation, selection, outcome); `TN-C-11` rewritten to selection, `TN-A-02` extended to name `AttackTag`, new `TN-A-03` | **the `TN-C-11` / `TN-A-01`-`02` conflict** | §9.2, T-C05-63, DV-20 |
| **10** | **Every instrument re-derived**: totals (43 obligations, 18 suites, 67 cases, 23 checks), the `VF` list in one normative home with two pointers, and the three counts that changed refreshed everywhere | housekeeping D-5/D-6 depend on | §11–§13 |

---

### 0.6 S4.2 in one paragraph, and where every change is recorded

Two independent reviews were run against the **same** pinned blob (`d54e194a…`): Agent 2's reassessment `TDD-A2-REVIEW-A1C05-S4-1-001` (594 lines) and Agent 3's independent integration review (115 lines). Both returned **`TARGETED REVISION`**; neither found a defect in a normative clause. **S4.2 answers all fourteen findings and both reviews' conditions** — the mapping is §2.5 (Agent 2), §2.6 (Agent 3) and §2.7 (the TD's consolidated six corrections), each naming the exact section that resolves it and, where I did not adopt a reviewer's suggested mechanism, the technical reason. **No obligation is added or removed: 43 remains 43.** Six instruments are new or widened — four new (**DV-24**…**DV-27**) and two widened in place (**DV-20**, **DV-22**) — and **every one of them is shown failing on a blob that contains the defect it was built for** (§13.3) — S4.1 for five of them, S4.0 for DV-24, S3 for DV-11 — before being shown passing here: a check that has never failed proves nothing.

---

## 2. Finding-by-finding closure matrix

**Column 3 is the precise S4 location that resolves the finding.** Where S4 chose differently from Agent 2's recommendation, the row says so and gives the reason; that is the "remaining disagreement" column the disposition asks for.


### 2.1 Agent 2's seven defects

| # | Finding (abridged from `TDD-A2-REVIEW-A1C05-S3-001` §10) | S4 resolution — precise location | Status | Remaining disagreement |
|---|---|---|---|---|
| **D-1** | `EX-5` (c) omits only-`n+1`; §3.6 rationale (c) "asserts a resync nothing obliges"; the consumer ages at a stale rate with no diagnostic | **§3.6** rationale (c) rewritten to state the real outcome; **§10.5** gains case **(d)**; **`TN-C-14`** (§8) bounds staleness to one frame for timing-dependent consumers; **§4.6 `TN-C-10`** acknowledges the residual; **T-C05-64** | **CLOSED** | Agent 2 offered (i)/(ii)/(iii) and called (iii) cheapest. **S4 takes (i) + (iii):** the bound *and* the explicit acceptance. Reason: (iii) alone leaves a known defect unmitigated, and (i) costs one pull per frame for the consumers that need accuracy. (ii) is rejected because it would forbid the canonical same-frame pair `PO-3` requires |
| **D-2** | `PO-3` fixes order, not content; readings A and B both permitted; B violates `INV-1` through `TN-P-11`; `T-C05-51` cannot discriminate | **§4.9 `PO-5`** (new); **§3.6** interleaving paragraph; **`TN-P-18`** (§7); **T-C05-51** extended to assert `ProducerRate` per message; **T-C05-65** asserts the mid-frame pull | **CLOSED** | none — S4 adopts the closure condition as written |
| **D-3** | "Constant for the lifetime" contradicts `TN-P-07`'s identity clause and `T-C05-62`'s identity rows | **§3.8** and **§6.1 alternative 3** reworded to "fixed for the instance's lifetime"; **`TN-P-19`** (§7) makes the change path explicit; **`TN-P-07`** loses the identity clause; **`TN-P-04`** extended to name identity change as a cancellation; **§10.12 EX-12**; **T-C05-62** identity rows replaced; **T-C05-66** | **CLOSED** | **Agent 2 recommended (ii) mutability; S4 takes (i) constancy *with a named change path*.** Reason: (ii)'s "a change closes the instance and opens a new one" *is* constancy for the instance's life, so the two readings converge once the change path is stated — and (i) plus a close/reopen obligation is testable in a way "mutable, new revision carries it" is not, because the latter re-opens the question `INV-1` was fixed to answer. `T-C05-62` is not left vacuous: its identity rows become a close-and-reopen assertion |
| **D-4** | Audio owned by Agent 1 (row 5) and Agent 2 (row 6, §6.1); no obligation covers cue selection | **§5.2 row 5** loses "and audio cues"; **row 6** keeps cue selection; **`TN-C-15`** (§8) added; **§6.1** audio row names the owner and the obligation; **T-C05-67** | **CLOSED** | none. Agent 1's camera-relative audio occlusion, which Agent 2 floated as a possible distinct Agent 1 responsibility, is **not claimed here** — no source assigns it to Agent 1, and inventing it would be the scope expansion this disposition forbids |
| **D-5** | `TN-C-12`/`TN-C-13` carry the row-7 (outside C-05) token while being row-6 consumer obligations | **§5.4** new token `Agent 2, C-05 consumer` → row 6; **`TN-C-12`**, **`TN-C-13`** implementer cells re-mapped; **§5.4** allowed-row rule | **CLOSED** | none — S4 adopts the closure condition |
| **D-6** | `DV-11` is agent-level, so it cannot fail on rows 6 vs 7; it reports 6 tokens where 5 are used | **§13 DV-11** rewritten row-level with an allowed-row set per obligation prefix, and reports **7 declared / 5 observed**; **§5.4** states which token is declared-but-unused and why | **CLOSED** | none |
| **D-7** | `INV-2` states its equivalence unconditionally; the one-revision precondition is only in rationale prose | **§4.6 `INV-2`** now carries the precondition in the clause; **`TN-C-10`** echoes it; **§3.4** keeps the proof as rationale | **CLOSED** | none |

### 2.2 Agent 2's conditions on C4a, C4c and C6

| Condition | Resolution — precise location | Status |
|---|---|---|
| **C4a-1** — `INV-2` precondition unstated | §4.6 `INV-2`, sentence 3; `TN-C-10` failure column; §3.4 | **CLOSED** |
| **C4a-2** — the `VF` list has three homes | §3.2 becomes the normative list; `INV-1` and the §4.2 struct comment now *reference* it and restate the same seven names; **DV-12** extracts all three and compares sets | **CLOSED** (advisory, and closed rather than deferred) |
| **C4c-1** — `EX-5` case (d) missing | §10.5 case (d); `TN-C-14`; §3.6 rationale (c) | **CLOSED** |
| **C4c-2** — `PO-3` fixes order not content | §4.9 `PO-5`; `TN-P-18`; T-C05-51 extended; T-C05-65 | **CLOSED** |
| **C6-1** — constancy contradiction | §3.8, §6.1, `TN-P-07`, `TN-P-19`, `TN-P-04`, T-C05-62, T-C05-66 | **CLOSED** (constancy + named change path; see D-3 disagreement) |
| **C6-2** — audio owned twice | §5.2 rows 5/6, `TN-C-15`, §6.1, T-C05-67 | **CLOSED** |
| **C9 / §3.11.1** — 6 tokens declared, 5 used | §5.4 declares **7** and states that two of them (`contract layer, owner pending TD-12`, `Agent 2, in its own systems`) carry no obligation row by design; DV-11 reports 7 declared / 5 observed separately | **CLOSED** |
| **C9 / §3.11.2** — agent-level check cannot fail on D-5 | §13 DV-11 row-level; §5.4 allowed-row rule | **CLOSED** |

### 2.3 Agent 3's conflict

| Finding | Resolution — precise location | Status |
|---|---|---|
| **`TN-C-11` vs `TN-A-01`/`TN-A-02`** — a consumer must take blockability from `AttackTag`, while no arbitration decision may depend on a C-05 value | **§9.2 `C05-6.4`** separates three domains — **creation** (the producer authors the tag), **selection** (a consumer may use it to choose a response), **outcome** (no C-05 value may decide a hit) — and states which clause governs each; **`TN-C-11`** rewritten to selection only; **`TN-A-02`** extended to name `AttackTag`; **`TN-A-03`** added; **T-C05-63** asserts a corrupted `AttackTag` cannot change a parry; **DV-20** checks the boundary in the text | **CLOSED as S4's own resolution** — see the caveat below |

**The caveat, stated where it cannot be missed.** I resolved this conflict from its own terms because Agent 3's review is not in the repository (§0.2). **Their proposed wording has not been used and no sentence here is attributed to them.** If their wording differs materially, §9.2 and `TN-C-11` are the sections that will need re-cutting. This is dependency **B-15**, and §18.2 asks them to confirm or replace.

### 2.4 What S3 resolved and S4 leaves alone

C1, C2, C3, C4b, C5, C7, C8 — **AGREE in Agent 2's S3 review, and unchanged here** except where D-2 and D-5 touch their wording (`PO-3`'s content rule and two implementer cells). Nothing in S4 reopens a settled requirement, and no S3 decision outside the ten corrections in §1 is altered.

---

### 2.5 Agent 2's S4.1 reassessment (`TDD-A2-REVIEW-A1C05-S4-1-001`, commit `eee9401`) — every finding

Agent 2's tally against S4.1 was **10 AGREE, 3 AGREE WITH CONDITIONS, 1 DISAGREE** across seven defects and seven conditions, plus two carried conditions, one cosmetic and one confirmed explanatory defect. **Every row below is answered; none is dismissed.**

| A2 finding | What Agent 2 found | S4.2 resolution — precise location | Status |
|---|---|---|---|
| **D-6a** — `DV-11` count (`§3`) | **RESOLVED in S4.1**, verified twice independently, and **withdrawn** by Agent 2. "The obsolete S4.0 finding is withdrawn." | Nothing to fix. **7 declared / 5 observed is retained** (§1 row 6, §5.4, §13.1) and the obsolete 6-observed figure is not reintroduced. The only surviving occurrences of it are §0.5's two rows that quote the defect being corrected | **CLOSED — agreed, no action** |
| **D-6a-i** — condition (`§3.5`) | "when S4.1's next substantive successor opens §13 for any other reason, add `DV-24` — every declared/observed sentence equals `DV-11`'s computed output" | **`DV-24` added** (§13.1, §13.3). S4.2 opens §13 (it widens DV-20 and DV-22), so the condition is activated rather than deferred, and DV-24 is **shown failing on the S4.0 blob** `424d2c69…`, where §1 said 6 and the instrument computed 5 | **CLOSED — condition adopted** |
| **D-4 / C6-2** — audio (`§4`) | §8's preamble, line 566, still assigns audio to Agent 1: *"Agent 1 for defence, dodge, camera **and audio**"*, 107 lines above `TN-C-15`'s "Agent 2 alone" | **§8 preamble, two words deleted** and the single owner named positively: *"— Agent 1 for defence, dodge and camera; Agent 2 for AI reaction, **audio cue (the only C-05 audio responsibility)**, montage trigger and VFX timing."* `TN-C-15` unchanged; row 5 unchanged; the allocation is untouched. **`DV-22` widened** to scan the preamble and the whole document (§13.1), and **it is shown failing on the reviewed blob** (§13.3) | **CLOSED — both halves, as Agent 2 required** |
| **D-22-scope** — instrument (`§4.4`) | "`DV-22` checks three objects … §8's preamble is none of the three. So `DV-22` reports PASS on a document that still contains the defect it exists to prevent." | `DV-22`'s method now inspects **row 5, row 6, `TN-C-15`, the §8 preamble, and a whole-document scan** for any line pairing audio with an agent other than Agent 2 outside a marked historical/quotation context | **CLOSED** |
| **C4c-N1** — `PO-3` rationale (`§6.2`) | §3.6(b)'s premise *"the producer's internal application order is **not observable** at frame granularity"* is **falsified by `PO-5`**, which makes a mid-frame pull return the earlier revision exactly. `PO-3` remains necessary and must not be discarded | **§3.6(b) rewritten to Agent 2's suggested text**: the order **is observable** through a mid-frame pull once `PO-5` is in force, so leaving it to the producer would expose different revision sequences; `PO-5` therefore requires the application order to follow `PO-3`'s publication order. **`PO-3`, `PO-5`, `TN-P-15`, `TN-P-18`, `T-C05-51` and `T-C05-65` are byte-identical** — nothing discarded, nothing weakened | **CLOSED** |
| **D-1a** — upper-bound wording (`§6.1`) | *"Staleness is then bounded by one frame, by construction"* reads as a same-frame guarantee; the bound is from the missed revision's publication to the next successful observation | **Adopted, and made stronger by being derived rather than asserted:** `TN-C-14` now proves the bound from its own rules and states it as *"at most one frame, measured on the shared axis from the publication of the missed revision to the timing-dependent use (and to the next successful refresh), not a same-frame guarantee that the pull lands after the producer's publication"* (§8 `TN-C-14`; §13 DV-25) | **CLOSED** |
| **D-1b** — undefined classification (`§6.1`) | "nothing defines which consumer is which. Make it a property of the **call site**" | **Adopted exactly:** `TN-C-14`(i) attaches to the call site — *every call site that reads `RemainingLocalSeconds`* — and removes the per-agent taxonomy | **CLOSED** |
| **D-6b** — §5.4 tallies (`§6.3`) | "`producer owner` … 19" vs **23** cells (19 `TN-P` + 4 `TN-R`); "`each consumer` … 11" vs **12** cells | **§5.4's "Used by" column replaced with exact cell counts** for all seven tokens (23 / 12 / 3 / 2 / 3 / 0 / 0 = 43), labelled as counted by `DV-11` from the tables rather than by hand. The TD routed D-6b to Agent 2's addendum; it is fixed here anyway because §5.4 is the table `DV-11` reads, and leaving a hand-copied count beside the instrument would be the third instance of the class `DV-24` now closes | **CLOSED** |
| **Carried verdicts** D-1, D-2, D-3, D-5, D-6, D-7, C4a-1, C4a-2, C4c-1, C4c-2, C6-1, C9 | AGREE / AGREE WITH CONDITIONS — S4.1 changed no normative clause, and Agent 2 re-verified that rather than assuming it | Nothing reopened. `D-1`'s *condition* is §2.5's D-1a/D-1b rows (both closed); the others are unchanged and untouched | **CARRIED — no action** |
| **A2's own provenance withdrawal** (`§1`) | Agent 2 withdrew its "no V4_1 exists" claim and adopted the rule *re-verify any negative existence claim immediately before publication* | **Not mine to close and not treated as a finding.** Recorded here so the record shows the withdrawal and the new rule; **S4.2 follows that rule itself** (§17: the existence and blob check was re-run as the last action before this file was published) | **NOTED** |

### 2.6 Agent 3's S4.1 review (commit `34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a`) — every finding

Agent 3's outcome was **`TARGETED REVISION`** with two DISAGREE (findings 4 and 5), four AGREE and one AGREE WITH CONDITIONS. Every finding is answered below.

| A3 finding | What Agent 3 found | S4.2 resolution — precise location | Status |
|---|---|---|---|
| **1** — `TN-C-11` / arbitration boundary (**AGREE WITH CONDITIONS**) | §5.2 row 5's *"parry/block/dodge evaluation from the pull"* permits the pull to enter the parry/block **outcome**, which §4.8 and §9.2 reserve from all C-05 inputs | **§5.2 row 5 rescoped**: Agent 1's integration is *response selection and telegraph consumption* — using the adopted snapshot **including `AttackTag`** to choose and initiate a defence — and **explicitly not the hit outcome**, which is decided on the hit-resolution path by **row 8** with `C05-6.1` and `TN-A-01`–`TN-A-03`. The pull and any cached `AttackTag` are excluded from it by name (§5.2). The three-domain model of §9.2 is unchanged and is cited, not restated | **CLOSED** |
| **2** — tag lifetime, three domains, downstream boundary (**AGREE**) | no C-05 defect; B-13 and the C-03/C-04/TD-09 outcome rules remain external | **No change.** B-13 and the outcome dependencies stay visible (§14.2), and no C-05 tag is presented as an authoritative unblockable result | **CLOSED — no action** |
| **3** — `TN-P-18`, `PO-5`, per-message `ProducerRate` (**AGREE**) | "no text defect found; it remains unvalidated behaviorally" | **No change** to `PO-3`, `PO-5`, `TN-P-15`, `TN-P-18`, `T-C05-51`, `T-C05-65` — byte-identical | **CLOSED — no action** |
| **4** — the one-frame staleness bound (**DISAGREE**) | concrete counterexample: pull early in frame *k*, `Retimed` lost immediately after, one pull late in frame *k+1* → almost two frame durations of staleness while satisfying "at least once per frame". Also: no maximum interval, no measure, no required fresh pull before a timing-dependent action | **`TN-C-14` rewritten as a five-rule obligation** (§8): (i) call-site scope; (ii) **refresh in the frame, before first use** — the observation's `AxisNow` may not precede the current frame's start, so a value carried across a frame boundary may not be used; (iii) **maximum one frame between successful refreshes, measured on the shared axis**; (iv) **fresh pull before the action when the guarantee cannot be established**, else suppress the action; (v) the message-only residual, still explicitly accepted. The bound is **derived** from (ii)+(iv), not asserted. **`T-C05-64` extended** with Agent 3's exact counterexample schedule, the worst-case permitted poll placement, the requirement to assert the age in the stated measure, and both negative controls (§12.2) | **CLOSED — the bound is now proven, not claimed** |
| **5** — audio ownership (**DISAGREE**) | §8's introduction contradicts sole Agent 2 ownership; `DV-22` misses it | Same resolution as A2's D-4/D-22-scope rows above — one defect, two reviewers, one fix | **CLOSED** |
| **6** — D-1…D-7 disposition and T-C05-63/DV-20 (**AGREE WITH CONDITIONS**) | the normative exclusion is clear, but **`DV-20` is a text-presence check, not evidence of the data path**, and `T-C05-63` does not *combine* the held-snapshot and corrupted-tag cases — a spy on the surface cannot see a cached tag already held for selection | **`T-C05-63` rewritten to combine all three** — a snapshot already held for selection, an adversarial alteration of its `AttackTag`, and a hit-resolution attempt — with **the hit-resolver's input/use path instrumented (tainted-value dataflow), not merely the source surface**, and a **separate** assertion that the selection call site still uses the tag. **`DV-20` extended** to require row 5's outcome exclusion and T-C05-63's three-part structure. **And DV-20's own status is stated honestly**: it remains a text check; the dataflow claim belongs to T-C05-63, which is `PROPOSED / NOT RUN` | **CLOSED, with the limit Agent 3 named** |
| **7** — S4.1 delta and provenance text (**AGREE WITH CONDITIONS**) | §17 and §18.1 carry literal commit/blob placeholder fields (`S41_*`) in the reviewed blob; the handoff is not reproducible from the document alone | **Placeholders eliminated and the pattern removed, not just filled.** §17 records S4.1's exact commit and blob; **this file carries no placeholder at all** — its own provenance is written to `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md` in the commit immediately after the text, so the blob a reviewer pins never contains an unfilled field (§17) | **CLOSED — root cause, not instance** |

### 2.7 The TD's six consolidated corrections → where each is resolved

| TD item | Requirement | Resolved at | Verified by |
|---|---|---|---|
| **1** | D-4 audio: remove "and audio"; make Agent 2's exclusive responsibility explicit; widen DV-22 to all ownership prose including §8's introduction; preserve `TN-C-15` and the allocation | **§8 preamble**, **§5.2 row 5**, **§13.1 DV-22** (`TN-C-15` unchanged) | DV-22 PASS here, **FAIL on `d54e194a…`** |
| **2** | D-1: prove the bound — max interval or polling point/order, the measure, a fresh pull before a timing-dependent action when the guarantee is insufficient, keep the message-only residual, extend `T-C05-64` with A3's just-after-poll schedule and the worst-case placement | **§8 `TN-C-14`**(i)–(v), **§12.2 `T-C05-64`**, §10.5 case (d) | DV-25 PASS here, **FAIL on `d54e194a…`** |
| **3** | C4c-N1: correct §3.6(b); `PO-5` makes intermediate revisions observable; preserve `PO-3` | **§3.6(b)** | DV-26 PASS here, **FAIL on `d54e194a…`** |
| **4** | Row 5: distinguish selection/initiation from hit outcome; exclude the pull from hit-outcome arbitration; point to the right row and `TN-A-01`–`TN-A-03`; preserve the three domains | **§5.2 row 5**, §9.2 cited | DV-20 PASS here |
| **5** | T-C05-63/DV-20: held snapshot + adversarial tag + hit attempt; identical outcome; no tag-derived value reaches the resolver; instrument the input/use path; retain the selection assertion | **§12.2 `T-C05-63`**, **§13.1 DV-20** | DV-20 PASS here |
| **6** | S4.1 metadata: replace the `S41_*` placeholder fields with `95918268…` / `d54e194a…` | **§17**, **§18.1**, **§18.2** | DV-27 PASS (no placeholder anywhere; S4.1 values exact) |

**Counting rule recorded once:** §2.5 and §2.6 answer **14 reviewer findings** (9 Agent 2 rows carrying findings or conditions, 7 Agent 3 findings, with D-4/C6-2 and A3's 5 being the same defect counted once in the fix and twice in the matrix because two reviewers raised it). §2.7 answers the **6** TD items. **No finding in either review is left without a row.**

---

## 3. The corrected revision model

### 3.1 The defect Agent 2 found, restated exactly

S2's `INV-1` said two observations at the same `StateRevision` are *"identical in every pull-visible field — phase, all timing endpoints, `ProducerRate`, `RemainingLocalSeconds`"*. But `RemainingLocalSeconds` is not a stored field; it is a **function of the observation instant**, defined by the aging rule at `A1-R4` §3.3(e). Agent 2's arithmetic:

| Frame | `Axis(t) − AxisNow` | `RemainingLocalSeconds` | `StateRevision` |
|---|---|---|---|
| 0 | 0.0 | 0.2000 | 1 |
| 1 | 0.2 | 0.1900 | 1 |
| 2 | 0.4 | 0.1800 | 1 |

Two pulls at revision 1 return `0.2000` and `0.1800`. **The producer is conforming; the invariant was wrong.** The same error propagated to `TN-R-05` and `T-C05-46`, and it collided with `TN-P-11` ("pull answers from live state at call time"), which no correct implementation can reconcile with a frozen `RemainingLocalSeconds`.

### 3.2 Two field classes, named so the invariant can be stated over one of them

> **VF — versioned fields (this is the normative list; `INV-1` and the §4.2 struct comment quote it and neither extends nor narrows it).** The fields a `StateRevision` versions, and the only fields `INV-1` constrains: **`Phase`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`, `ProducerRate`, `WindowKey`, `AttackTag`.** The three endpoints and `ProducerRate` live inside `Timing`; `Phase`, `WindowKey` and `AttackTag` sit directly on the snapshot. Instance identity (`AttackInstanceId`, `SourceEntityId`) is fixed for the instance's lifetime and cannot vary at all. **DV-12** extracts this list, `INV-1`'s and the struct's, and fails on any difference.

> **OF — observation-instant fields.** The fields that describe **when** the snapshot was taken, not **what** the state is: **`AxisNow`, `RemainingLocalSeconds`.** They are determined by the observation instant and the versioned fields, by `INV-2`, and by nothing else.

**The split is not a convenience, it is the contract's own semantics.** A versioned field is authored or applied by the producer under `RM-1`'s lifecycle; an observation-instant field is computed from the axis at the moment of the pull or the emission. Grouping them was the S2 defect. The division is exhaustive: every field of `FTDDTelegraphTiming` and `FTDDTelegraphSnapshot` is in exactly one class, and `StateRevision` itself is in neither — it is the counter that indexes `VF`.

### 3.3 `INV-1`, corrected

> **C05-2.6 INV-1 (corrected).** For a given `AttackInstanceId`, two observations carrying the same `StateRevision` are **identical in every versioned field** (`VF`: phase — `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis` — `ProducerRate`, `WindowKey`, `AttackTag`). They are **not** required to be identical in the observation-instant fields (`OF`): `AxisNow` and `RemainingLocalSeconds` describe the instant of observation and are governed by `INV-2`. A producer that publishes or answers at a revision with different `VF` content is in violation (`TN-P-07`).

**What is preserved:** `Phase` is a versioned field, so Agent 3's original defect stays closed — a phase change at an unchanged revision is still unrepresentable, and equal-revision discard still cannot lose a phase change.
**What is fixed:** a producer that ages its own remaining time correctly is no longer diagnosed as a violator on every frame.

### 3.4 `INV-2` — the aging law, stated in the contract

> **C05-2.6 INV-2 (new).** Within one snapshot, the observation-instant fields are consistent with the versioned fields at that snapshot's own `AxisNow`:
>
> ```
> RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)
> ```
>
> where `PhaseEndAxis` is the endpoint of the current phase (`WindupEndAxis` in `Windup`, `ActiveEndAxis` in `Active`, `RecoveryEndAxis` in `Recovery`). A consumer holding a snapshot ages it by the same law in the form established at `A1-R4` §3.3(e):
>
> ```
> R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)
> ```
>
> with `R0` the snapshot's `RemainingLocalSeconds` and `AxisNow` its `AxisNow` stamp. **Never by wall-clock elapsed, never by the consumer's own `CustomDilation`.**

**The equivalence holds within one revision, and the clause now says so.** Agent 2's `C4a-1`/`D-7` is accepted in full: `INV-2` is a closed system only while `ProducerRate` and `PhaseEndAxis` are fixed, which `INV-1` guarantees inside a revision and nothing guarantees across one. The precondition is stated in the clause itself (§4.6), not only here, and `TN-C-10` echoes it.

**These two forms are the same function, and that is the consistency proof the instruction asks for.** Substituting the snapshot's own value, `R0 = (PhaseEndAxis − AxisNow) × Rate`, into the consumer form gives `(PhaseEndAxis − AxisNow) × Rate − (Axis(t) − AxisNow) × Rate = (PhaseEndAxis − Axis(t)) × Rate` — algebraically identical to producer form. So the producer's obligation (`TN-P-17`) and the consumer's obligation (`TN-C-10`) are two views of one equation, not two independent rules that could drift. The identity holds exactly while `ProducerRate` and `PhaseEndAxis` are fixed, which is precisely what one revision guarantees; a rate change is a `Retimed` (`TN-P-08`) and a phase change is a `PhaseChanged` (`TN-P-13`), and each re-anchors both forms at a new revision.

### 3.5 Why equal-revision discard still loses nothing

This is the property S2's `INV-1` existed to justify, and it must survive the correction. It does, and the argument is now explicit rather than assumed:

1. A discarded equal-revision observation can differ from what the consumer holds **only** in `OF` — `AxisNow` and `RemainingLocalSeconds` (by `INV-1`).
2. `OF` carries no state: it is a deterministic function of `VF` and the observation instant (`INV-2`).
3. A consumer holding revision `n` can compute the `OF` values for any instant from its own snapshot by `R(t)`, using the shared axis it is already granted (`A1-R4` §3.3(a)).
4. Therefore discarding the later observation and aging the earlier one yields the **same** numbers, and the only thing discarded is a redundant recomputation.

**Contrapositive, which is the operative rule:** if the observation differs in any `VF` field — phase, an endpoint, `ProducerRate`, `WindowKey`, `AttackTag` — then the revision differs (`TN-P-07`), so the discard rule never applies to it. **A genuine state change cannot arrive at an unchanged revision.** `T-C05-62` enumerates the complete change table and asserts the correspondence; `T-C05-56` asserts the discard-then-age path is observationally equivalent, with a wall-clock-aging negative control that must diverge.

### 3.6 Simultaneous phase and retime: one canonical order

> **C05-2.9 `PO-1`.** A frame containing **only** phase transitions publishes one `PhaseChanged` per transition, in authored order, revisions `n+1`, `n+2`, … (§3.7).
> **`PO-2`.** A frame containing **only** dilation changes publishes one `Retimed` per change, in the order applied, revisions `n+1`, `n+2`, … No coalescing (`TN-P-08`).
> **`PO-3`.** A frame containing **both** publishes **all phase transitions first, in authored order, then all dilation changes, in the order applied.** One phase change plus one retime is therefore `PhaseChanged` at `n+1` followed by `Retimed` at `n+2` — never one message, never the reverse order, never a shared revision.

**Why this order, and not the other one:** (a) the phase transition is a **lifecycle fact** — the state the retime adjusts is the state the phase names; a retime published first would describe the timing of a phase the consumer has not been told about. (b) Within one frame the internal application order **is observable through a mid-frame pull once `PO-5` is in force**, so leaving the order to the producer would let two conforming producers expose different revision sequences for identical gameplay — the exact non-determinism a contract exists to remove. `PO-5` therefore requires the application order to follow the publication order `PO-3` fixes, not merely to interleave publication with application. **S4.1 and earlier said the opposite here** — that the order was *not* observable at frame granularity — and that premise was falsified by `PO-5` itself (Agent 2's `C4c-N1`, Agent 3 finding 3). The correction is stated rather than quietly applied, because an implementer who read the old premise could have concluded that the application order was unconstrained. (c) It is the safer order under loss, but **only for phase, and S3 overstated what that buys**. A consumer that loses the second message is phase-correct and rate-stale, and **nothing obliged a resynchronisation** — S3's claim that it "merely needs a resync" was wrong, because `AD-2` triggers on `incoming > held + 1` and no further revision arrives to trigger it. The residual is real, is bounded by `TN-C-14`, and is stated rather than implied; the reverse order would be worse, because it would leave the consumer timing-correct and phase-wrong with no bound at all.

**Consequence for consumers, spelled out because it decides entry:** a consumer holding `n` that receives both messages sees a contiguous run (`n+1`, `n+2`), adopts both, fires entry once for the new phase and none for the retime. A consumer holding `n` that receives only `n+2` — the retime — sees `n+2 > n+1`, records a gap, fires no entry and raises exactly one `FTDDTelegraphResynchronisation` (`AD-2`, `EN-3`, `TN-C-09`). A consumer that receives only `n+1` — the phase — adopts it, fires entry once and records **no gap**; it is phase-correct and rate-stale until a newer revision arrives (`EX-5` case (d), `T-C05-64`).

> **C05-2.9 `PO-5` (new).** Publication is **interleaved with application**, not batched at the end of a frame. The producer applies a change, publishes the message carrying exactly the state at that revision, applies the next change, and publishes again. **A message at revision `r` therefore carries the changes applied at or before `r` and none after it, and the producer's live state may never contain a `VF` change that no published revision covers** (`TN-P-11`, `INV-1`). A pull taken between two publications of the same frame returns the earlier revision's `VF` exactly.

**Why `PO-5` is a separate rule and not a footnote to `PO-3`:** `PO-3` fixed the *sequence* and left the *content* open, and Agent 2's `D-2` shows both readings are permitted as S3 stood. Reading B — `n+1` carries the pre-retime rate, `n+2` the post-retime rate — is the natural one and, without `PO-5`, is unsatisfiable together with `TN-P-11` whenever the producer applies the dilation before publishing the phase. `PO-5` makes reading B the only legal reading and makes it satisfiable, by requiring the producer to publish between applications rather than after them.

### 3.7 Two phase transitions inside one frame

> **C05-2.9 `PO-4`.** Two phase transitions occurring within one frame are **two transitions**: two increments of `StateRevision`, two `PhaseChanged` messages, published in authored order and never collapsed into one revision or one message. A producer whose authoring model can produce two transitions in one frame — montage section boundaries landing in the same tick — **must publish both**. It may not drop the intermediate phase, merge the pair, or publish only the resulting phase.

Two consequences worth stating because they are what an implementer will hit:

- **A phase can begin and end inside one frame.** Such a phase is published twice and may never be observable through a pull at all: a pull taken after the frame returns the later phase. Consumers must not infer "this phase never happened" from a pull — a pull is current state, not history (`RS-1`, `TN-C-08`).
- **The consumer rules do not need a special case.** Receiving both messages from `n` is a contiguous run: both phases are adopted and each fires entry at most once (`EN-2`). Receiving only the second is a gap: no entry, one resync. This is `PO-3`'s arithmetic with a different number of increments, which is exactly why the ordering rule is stated as a sequence of revisions rather than as a special case per frame.

### 3.8 The identity fields: fixed for the instance's lifetime `[CORRECTED: D-3]`

`WindowKey` and `AttackTag` are **versioned fields, authored at `Opened` and fixed for that instance's lifetime**. They do not age, so they cannot repeat S2's mistake, and they cannot change under one instance, so they cannot become a second staleness surface — which is what makes carrying identity in the snapshot safe rather than a second lookup problem (§6.1).

**What happens when the attack identity changes.** It cannot change *within* an instance. A change of attack identity — a re-authored definition, a phase-graph swap that substitutes a different attack, a requirement change — **closes the instance** through `TN-P-04`'s cancellation path and opens a **new** one with a new `AttackInstanceId` at revision 1. That is `TN-P-19`. It is also why `TN-P-07` no longer carries S3's clause about "every change to `WindowKey` or `AttackTag`": under constancy that clause could never fire, and a dead norm is worse than no norm.

**This differs from Agent 2's recommendation, deliberately** (`C6-1`). Their option (ii) was *"fixed while the instance is open under one attack definition; a change of attack identity closes the instance and opens a new one"* — which **is** constancy for the instance's life. The two readings converge once the change path is named, and S4 states it as an obligation with a test (`T-C05-66`) rather than leaving it in prose. **`T-C05-62` does not become vacuous:** its two identity rows are replaced by the close-and-reopen assertion, which is representable and falsifiable.

### 3.9 What this section did not change

`AD-1` (strict-greater adoption), `AD-2` (gap flag), `EN-1` (baseline), `EN-2` (at most once per phase), `TM-1` (terminal close outside the freshness rule), `RS-1`/`RS-2`/`RS-3` (current-state recovery, no revision log, one snapshot per instance), `RM-1`/`RM-2` (removal semantics), the pull surface, the directory's content, and the producer/consumer boundary. **The correction is confined to how the invariant is stated over two field classes, and to the publication order of a frame that contains more than one change.**

---

## 4. The complete revised contract

Readable without either predecessor. `[UNCHANGED]` means the S2 text stands; `[CORRECTED]` and `[NEW]` mark this revision's edits. Every clause is `PROPOSED — NOT FROZEN`.

### 4.1 C05-2.1 — What the contract is about `[UNCHANGED]`

Telegraph timing is published by the **producer** — Agent 2 for enemy attacks, Agent 1 for the player's own attack — as an ordered message stream plus a per-instance pull, and consumed by defence and feedback consumers on both sides. The producer is the sole authority for the values it publishes. **No component in this contract retains a copy of another producer's timing block.** Producer and consumer responsibilities are allocated by activity in `C05-7.2` / `C05-7.3`, and the vocabulary of that allocation is fixed in `C05-7.4`.

### 4.2 C05-2.2 — Value types (contract-layer types; owner pending TD-12) `[CORRECTED]`

```cpp
// PROPOSED — NOT FROZEN. Owner: the cross-agent contract layer of the canonical
// architecture (TDDCore under MEAD-C; no TDDCore module under MEAD-A or MEAD-B,
// whose nearest home is a framework area with no assigned owner). See §5.
// Engine types only: FGuid, FName, FGameplayTag. No candidate-specific module.

struct FTDDTelegraphTiming
{
    // ---- OF: observation-instant fields (INV-2; differ between observations at one revision)
    double  AxisNow;                 // shared axis at this observation (emission, or the pull's call time)
    float   RemainingLocalSeconds;   // = max(0, (PhaseEndAxis - AxisNow) * ProducerRate)   [INV-2]

    // ---- VF: versioned fields (INV-1; identical for one revision).
    //      Normative list and source of truth: §3.2. The VF fields are exactly
    //      {Phase, WindupEndAxis, ActiveEndAxis, RecoveryEndAxis, ProducerRate,
    //       WindowKey, AttackTag}; this comment quotes that list and DV-12 compares them.
    double  WindupEndAxis;
    double  ActiveEndAxis;
    double  RecoveryEndAxis;
    float   ProducerRate;            // ProducerRate == CustomDilation(producer) at this revision
    uint32  StateRevision;           // the counter that indexes VF. 1 on Opened; +1 on every
                                     // phase transition and every retime (PO-1..PO-4).
                                     // Renamed from TimingRevision at S2; supersedes A1-R3 §3.2
                                     // on this field only.
};

enum class ETDDTelegraphPhase : uint8 { Windup, Active, Recovery };   // closed is terminal

enum class ETDDTelegraphCloseReason : uint8
{
    Natural, Cancelled, Interrupted, ProducerInvalidated, SourceDied
};

struct FTDDTelegraphSnapshot      // what a pull returns and what EVERY message carries
{
    // identity: fixed for the instance's lifetime
    FGuid               AttackInstanceId;
    FGuid               SourceEntityId;

    // VF: versioned fields (INV-1)
    ETDDTelegraphPhase  Phase;
    FName               WindowKey;    // stable per attack definition; authored at Opened and
                                      // FIXED for this instance's lifetime (TN-P-19: an identity
                                      // change closes and reopens, it is never a new revision)
    FGameplayTag        AttackTag;    // block / dodge / unblockable, for SELECTION only (C05-6.4):
                                      // never an input to a hit-resolution decision; a transported
                                      // value, never defined or registered by this contract
    FTDDTelegraphTiming Timing;       // carries StateRevision and the OF pair

    // -- equality classes used by INV-1: {identity, Phase, WindowKey, AttackTag, Timing.VF}
    // -- observation-instant: {Timing.AxisNow, Timing.RemainingLocalSeconds}
};

struct FTDDTelegraphMessage       // one struct, complete state, plus the event kind
{
    enum class EKind : uint8 { Opened, PhaseChanged, Retimed, Closed };
    EKind                  Kind;
    FTDDTelegraphSnapshot  Snapshot;      // the complete pull-visible state at emission
    ETDDTelegraphCloseReason CloseReason; // meaningful only when Kind == Closed
};

struct FTDDTelegraphResynchronisation   // NEW: declared, because TN-C-09 is normative
{
    FTDDTelegraphSnapshot LandedState;    // the state adopted across the gap; no history (RS-1/RS-2)
};

DECLARE_DELEGATE_OneParam(FTDDTelegraphOnResynchronised, const FTDDTelegraphResynchronisation&);
```

**`Resynchronised`'s status, stated once and unambiguously:** it is a **contract-layer type with normative semantics and consumer-local delivery**. C-05 fixes what it carries, when it fires and how often; C-05 defines **no transport, no subscription registry, no queue and no cross-agent delivery** — each consumer raises it in its own code, on its own delegate, for its own gap. It is therefore checkable (a delegate's invocation count is observable inside the consumer) without becoming the event bus this contract has repeatedly refused to be. Cross-agent routing, if anyone ever wants it, is a TD decision and is not proposed here (§14.2, B-12).

### 4.3 C05-2.3 — The message stream `[UNCHANGED, plus PO-3/PO-4 ordering]`

Four kinds — `Opened`, `PhaseChanged`, `Retimed`, `Closed` — each carrying the **complete snapshot** (`C05-2.3a`). `Closed` additionally carries an `ETDDTelegraphCloseReason` and is **terminal** (`TM-1`). `Opened` establishes revision 1. Ordering within a frame is fixed by `C05-2.9`.

> **C05-2.3a.** No message carries a partial aspect of the state. A consumer that receives any message holds the whole state at that revision and therefore never needs a follow-up pull to complete it — including the identity fields a per-attack consumer needs to act (`WindowKey`, `AttackTag`).

### 4.4 C05-2.4 — The pull surface `[UNCHANGED]`

```cpp
class ITDDTelegraphSource
{
public:
    // Live read of one instance the caller can name. False if not open, never opened
    // by this producer, or this producer is shutting down. Answers from live state at
    // call time (TN-P-11): AxisNow is the call's axis instant and RemainingLocalSeconds
    // satisfies INV-2 at that instant, while VF fields match the instance's current
    // revision exactly (INV-1).
    virtual bool TryGetOpenTelegraph(FGuid AttackInstanceId, FTDDTelegraphSnapshot& Out) const = 0;

    // Instances this producer currently holds open. Per-producer, bounded by that
    // producer's own concurrency. NOT global enumeration and must not be aggregated.
    // A timing-dependent consumer re-pulls at least once per frame (TN-C-14); the pull
    // surface therefore has no "subscribe once" mode to offer.
    virtual void GetOpenTelegraphIds(TArray<FGuid>& Out) const = 0;
};
```

There is no third method, no descriptor query and no identity lookup: `WindowKey` and `AttackTag` travel **inside** the snapshot (§6.1 explains why a second call was rejected).

### 4.5 C05-2.5 — Resolution through the directory `[CORRECTED: C1, C2]`

> **DN-1.** The contract layer exposes a resolution function mapping `AttackInstanceId` to the producer that opened it. The directory stores per instance only: the id, `SourceEntityId`, and one **weak liveness handle**. Producers **register on `Opened`** and **deregister on `Closed` or on any invalidation of that producer's instances — whichever occurs first** (`RM-1`: `Closed`, producer invalidation, unload or stream-out, death-cancel, world teardown). An entry whose handle has expired answers `false`; world teardown drops every entry. The "no actor pointers" rule applies to published value structs, not to this private liveness record. **Implementation: Agent 1, as shared support; see `C05-7.2` and `C05-7.3`.**
>
> **DN-1a — why this is not a second scheduler.** The directory holds **no timing, no phase, no revision, no window and no queue**; it **schedules nothing**, orders nothing, emits nothing and wakes nothing; it is consulted **only** to map an `AttackInstanceId` to the producer that opened it and to answer whether that producer is still alive. A component that could schedule work would need a clock and an order; this one has neither, and `TN-R-06` forbids it acquiring either. It is therefore not the central director that `A2-C05` §7.1 rejected, and Agent 2's own words are the test: their objection was to a director that *competes*, and a liveness map does not compete.

### 4.6 C05-2.6 — Adoption, entry, invariants and terminal rules `[CORRECTED at S3: C4a, C4b, C5; at S4: D-7]`

> **INV-1 (corrected).** Two observations of one instance carrying the same `StateRevision` are **identical in every versioned field** — the seven of §3.2: `Phase`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`, `ProducerRate`, `WindowKey`, `AttackTag` — and in instance identity. They are **not** required to be identical in the observation-instant fields `AxisNow` and `RemainingLocalSeconds`, which `INV-2` governs.

> **INV-2 (corrected: precondition stated).** Within one revision, a snapshot satisfies `RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)`, and a consumer ages the snapshot it holds as `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)`, using the shared axis and that snapshot's `ProducerRate` — never wall-clock elapsed and never the consumer's own `CustomDilation`. **`INV-2` holds only while `ProducerRate` and `PhaseEndAxis` are fixed, i.e. within a single revision.** When either changes the revision advances (`TN-P-07`) and both forms re-anchor at a new `R0`; **a consumer aging a snapshot across a revision change it has not yet adopted is aging with stale `VF`, and its obligation is limited to the revision it holds** (`TN-C-10`).

> **AD-1.** A consumer adopts a snapshot only if its `StateRevision` is **strictly greater** than the revision it holds. Equal or lower is discarded silently. This applies identically to messages and pulls. **Discarding an equal-revision observation loses no state change:** by `INV-1` it can differ only in `OF`, and `OF` is recomputable by `INV-2` (§3.5).

> **AD-2.** If an incoming revision is **greater than held + 1**, the consumer records a revision gap, sets `bStateGapObserved` for that instance and keeps it set until the instance closes. The flag means: *at least one observable state change — phase, retime, or both — was missed.*

> **EN-1.** The **first** observation of an instance by a consumer establishes the baseline: the current phase is recorded as already held and **no entry hook fires** for it. An `Opened` and a pull-derived first observation are the same case.

> **EN-2.** After the baseline, a phase transition is observable **at most once** per consumer per `(AttackInstanceId, phase)`. A `Retimed` never re-fires entry — it changes timing, not phase identity. A duplicate `PhaseChanged` fires nothing.

> **EN-3 (corrected).** A snapshot adopted **across a revision gap** fires **no** phase entry for any phase not observed. The consumer raises exactly one **`FTDDTelegraphResynchronisation`** for that gap, carrying the landed snapshot (`LandedState`) and no transition history, on its own `FTDDTelegraphOnResynchronised` delegate; it must not synthesise entries for phases it did not see. The type is declared at `C05-2.2`; delivery is consumer-local, with no transport (§4.2).

> **TM-1.** `Closed` is **terminal** and is **not** subject to `AD-1`. A `Closed` whose revision equals or precedes the held revision still closes the instance. A producer does not advance `StateRevision` to announce a close.

> **RS-1.** A pull recovers the **current** snapshot of a known instance. It never reconstructs an intermediate revision.
> **RS-2.** No component retains more than one snapshot per instance. The revision counter is not a log.
> **RS-3.** A phase that opens and closes within a single frame is published as two transitions (`PO-4`) and may be unobservable through a pull. Absence from a pull is not evidence that a phase did not occur.

### 4.7 C05-2.7 — Removal `[UNCHANGED]`

> **RM-1.** An instance ceases to exist on `Closed`, on producer invalidation, on producer unload or stream-out, on producer death-cancel and on world teardown. Invalidation and teardown are not messages: they are observed as a pull returning `false` and a directory entry that no longer resolves. **Removal emits no synthesised message.**
> **RM-2.** A consumer holding state for an instance that returns `false` or no longer resolves **must** treat it as closed, release its block, fire no further entry, and raise no error.

### 4.8 C05-2.8 — What this contract explicitly does not do `[CORRECTED: C7, C8]`

No retained copy of another producer's state; no global enumeration (X-1 only); no arbitration, parry/block decision or damage application; no clock ownership (TD-06) or contract-layer home (TD-12); no MEAD selection, tag definition or registration, erratum or freeze; **no phase history, revision log or replay**; **no C-05 value — `AttackTag` included — as an input to any hit-resolution or arbitration decision (`C05-6.4`, `TN-A-02`, `TN-A-03`)**; **no transform, position, attach point or socket** (world placement is resolved from `SourceEntityId` outside the contract, `TN-C-12`); **no animation asset, montage or cue reference** (asset selection is resolved from attack data keyed by `WindowKey`, outside the contract, `TN-C-13`); no second query surface for attack identity (§6.1).

### 4.9 C05-2.9 — Publication order within a frame `[NEW at S3: C3, C4c; PO-5 added at S4: D-2]`

> **PO-1.** A frame containing **only** phase transitions publishes one `PhaseChanged` per transition, in authored (montage) order, at consecutive revisions `n+1`, `n+2`, ….
>
> **PO-2.** A frame containing **only** dilation changes publishes one `Retimed` per change, in the order applied, at consecutive revisions `n+1`, `n+2`, …. Never batched, coalesced, throttled or deferred (`TN-P-08`).
>
> **PO-3.** A frame containing **both** publishes **all phase transitions first, in authored order, then all dilation changes, in the order applied.** One phase change plus one retime is `PhaseChanged` at `n+1` followed by `Retimed` at `n+2`: two revisions, two messages, this order, never a shared revision and never the reverse.
>
> **PO-4.** Two phase transitions within one frame are **two transitions**: two revisions, two `PhaseChanged` messages, in authored order. A producer may not collapse them, drop the intermediate phase, merge the pair, or publish only the resulting phase. Where an authoring model can produce two section boundaries in one tick, both are published.
>
> **PO-5 (new).** Publication is **interleaved with application**. Each message carries exactly the state at its own revision — the changes applied at or before it and none after — and the producer's live state may never hold a `VF` change that no published revision covers. A pull taken between two publications of the same frame returns the earlier revision's `VF` exactly.

### 4.10 Referenced and boundary clauses `[C05-6.1, C05-6.3, C05-7.1 UNCHANGED; C05-6.4 NEW]`

Referenced by §9.2 and §10; listed so every clause reference resolves inside this document. `C05-6.4` is new in S4 and is set out in full in §9.2, because it is a boundary clause about arbitration and belongs next to the obligations that enforce it.

| Id | Statement, carried forward | Full text | Status |
|---|---|---|---|
| `C05-6.1` | Parry succeeds only when, in the frame the hit is resolved, the defender's parry window is active **and** the attacker's phase for that instance is `Active`: a same-frame phase-overlap test against live state, never timestamp subtraction, cross-entity clock comparison or tolerance for a late check. First stated at `A1-R3` §3.4. | S1 §6.1 | `PROPOSED — NOT FROZEN` |
| `C05-6.3` | `Dead > Cinematic > Staggered` over three carriers, priority order, first match wins, carriers never compared. Touches C-04 through the proposed amendment `C-04-4`; the carriers are stated in full only in S1 §6.3 (see §14.2 B-11). | S1 §6.3 | `PROPOSED — NOT FROZEN`, coupled to `C-04-4` |
| `C05-7.1` | The contract names no module and no class; its types are contract-layer types of the canonical architecture, owned by whoever TD-12 designates, implementable in a single-module layout. **Its second sentence remains withdrawn** and replaced by `C05-7.2`. | S1 §7.1, §5.1 here | `PROPOSED — NOT FROZEN` |
| `C05-6.4` | **New.** `AttackTag` is **descriptive, not decisive**: three domains — creation (producer), selection (consumer, `TN-C-11`), outcome (the attack/defence contracts, `TN-A-01`/`TN-A-02`/`TN-A-03`). No C-05 value, `AttackTag` included, is an input to a hit-resolution decision. | **§9.2** (full text) | `PROPOSED — NOT FROZEN` |

---

## 5. Ownership `[CORRECTED: C7, C8, C9]`

### 5.1 C05-7.1 — the neutrality rule `[UNCHANGED]`

The contract names **no module** and **no class**. Its value types, message structs, resynchronisation type and read interface are contract-layer types of the canonical architecture; their owner is whoever the TD designates when TD-12 settles which candidate is canonical. The interface must be implementable in a single-module layout, which holds under all three candidates. **No MEAD is selected by this document.**

### 5.2 C05-7.2 — the split, by activity `[CORRECTED at S3: rows 5–7; row 5 again at S4: D-4]`

> | Activity | Owner | Basis |
> |---|---|---|
> | **Gameplay production** — the authored attack, its montage windows, when a telegraph opens, changes phase and closes, and every cancellation decision | **Agent 2** for enemy attacks; **Agent 1** for the player's own attack | TD v1.2 C-05; `A2-C05` §8; `A1-R1` §5.1 |
> | **Producer-side implementation of `TN-P-01` … `TN-P-19`** — the pull answer, the per-producer id list, revision advancement, publication and ordering | **the owner of that producer**: Agent 2 on its enemy producers, Agent 1 on the player producer | follows from production ownership: an obligation about a producer's own state can only be implemented by the code that owns that state |
> | **Shared contract artefacts** — the value types, the message struct, `FTDDTelegraphResynchronisation`, the delegate signature and `ITDDTelegraphSource` | the **contract layer** of the canonical architecture; owner designated by TD-12 (Agent 3 under MEAD-C; unassigned under MEAD-A; absent under MEAD-B). **The contract layer carries no obligation row by design** — it owns types, not behaviour | TD v1.2 C-05 "publisher: Agent 3/TD (event type)"; MEAD-C line 228 |
> | **Shared read-surface support** — the directory of `C05-2.5` and the resolution helper | **Agent 1**, as shared support that stores only association and liveness; Agent 1 does not implement any part of an Agent 2-owned producer, and Agent 2 does not implement the directory | one world-scoped home; holds nothing a producer owns |
> | **Consumer integration (Agent 1)** — **response selection and telegraph consumption**: using the adopted snapshot, **including `AttackTag`**, to choose and initiate parry, block or dodge, and to drive camera response and framing. **This row does not own the hit outcome:** whether a hit is parried or blocked is decided on the hit-resolution path, which is **row 8** with `C05-6.1` and `TN-A-01`–`TN-A-03`; the pull, any cached snapshot and any `AttackTag` are **excluded from that path by name** (`C05-6.4`, §9.2). **Agent 1 owns no audio responsibility in C-05.** | **Agent 1**, in its own code | TD v1.2 C-05; `A2-C05` §8 consumer list; **corrected at S4 for audio** (S3's row 5 also claimed "audio cues", which row 6 assigns to Agent 2 — `D-4`); **rescoped at S4.2 for arbitration** (Agent 3 finding 1: the unqualified phrase "evaluation from the pull" permitted the pull to enter the outcome) |
> | **Consumer integration (Agent 2)** — **AI reaction** (`TN-C-11`); **audio cue selection** (`TN-C-15`); **montage switch trigger** (`TN-C-13`); **VFX marker timing and phase** (`TN-C-12`) | **Agent 2**, in its own code, from the snapshot and the messages. **This is the only C-05 row that owns audio** | `A2-C05` §8; `C05-7.4`; `D-4` |
> | **Resolved outside C-05 (Agent 2, in its own systems)** — **VFX world placement and attachment**, **montage and cue asset selection**, **per-attack response tuning data** | **Agent 2**, from `SourceEntityId` and from attack data keyed by `WindowKey`. **C-05 supplies neither placement nor assets and promises neither.** **No obligation row is assigned to this row** (`D-5`): `TN-C-12` and `TN-C-13` are C-05 consumer obligations and belong to row 6 | `C05-2.8`; Agent 2's review C7 and C8; §5.4 |
> | **Arbitration** — the parry/block decision for hits involving the player | **Agent 1**, subject to the TD-09 erratum and unchanged by this document. **C-05 supplies no input to it** (`C05-6.4`) | TD integration decision; `A1-R3` §3.4; `C05-6.1`; **§9.2** |

**What rows 5–7 fix, and what S4 had to fix again.** S2 named "AI reaction to the player's telegraph, audio cue, VFX marker, montage selection" as one row of C-05 consumers, which implied C-05 supplies what all four need. It does not: the VFX marker needs a world position the contract deliberately excludes, and montage selection needs an asset reference it also excludes. S3 split the row three ways — C-05 consumer, outside-C-05 resolution, trigger versus asset — but **left "and audio cues" in row 5**, so agent 1 and agent 2 both owned audio (Agent 2's `D-4`). **S4 removes it** and adds the obligation that was missing (`TN-C-15`), so each of the four consumers now has exactly one owner, one obligation and one test. Agent 2's own submission carries the same overstatement ("animation montage selection" among C-05 consumers); this document corrects **both**, and §15.3 records theirs as withdrawn-by-agreement rather than as a defect of theirs alone.

### 5.3 C05-7.3 — what "Agent 1 implements" means `[UNCHANGED]`

Agent 1 implements: (a) every `TN-P` obligation **on the player's own producer**; (b) the shared read-surface support — directory and resolution — for all producers; (c) every `TN-C` obligation in Agent 1's own consumers; (d) every `TN-A` obligation in the arbitration path, subject to TD-09. **Agent 1 does not implement the `TN-P` obligations on Agent 2's enemy producers**; those are Agent 2's, on Agent 2's code, against the shared interface.

### 5.4 C05-7.4 — role vocabulary, and the row-level mapping check `[CORRECTED: D-5, D-6, C9]`

The obligation tables name **roles**; `C05-7.2` names **agents and rows**. Both are deliberate — role vocabulary survives a change of producer ownership, agent vocabulary answers "who does it" — but the two must be mechanically comparable. This table is the bridge: **seven tokens, each mapped to exactly one `C05-7.2` row**, and **DV-11** checks every implementer cell against that mapping *and* against an allowed-row set determined by the obligation's prefix.

| Role token used in §7–§9 | Agent | `C05-7.2` row | Used by |
|---|---|---|---|
| `producer owner` | Agent 2 on enemy producers; Agent 1 on the player producer | **row 2** (inside C-05: producer implementation) | **23 cells** (19 `TN-P`, 4 `TN-R`) |
| `each consumer` | Agent 1 in Agent 1's consumers; Agent 2 in Agent 2's consumers | **rows 5–6** | **12 cells** (12 `TN-C`) |
| `Agent 2, C-05 consumer` | Agent 2 | **row 6** (inside C-05: consumer integration) | **3 cells** (`TN-C-12`, `TN-C-13`, `TN-C-15`) |
| `Agent 1, shared support` | Agent 1 | **row 4** | **2 cells** (`TN-R-01`, `TN-R-06`) |
| `Agent 1, subject to TD-09` | Agent 1 | **row 8** | **3 cells** (`TN-A-01`, `TN-A-02`, `TN-A-03`) |
| `Agent 2, in its own systems` | Agent 2 | **row 7** (outside C-05: placement, assets, tuning) | **0 cells — by design** |
| `contract layer, owner pending TD-12` | designated by TD-12 | **row 3** (types only) | **0 cells — by design** |

**Why a separate token for `Agent 2, C-05 consumer` (Agent 2's `D-5`).** S3 gave `TN-C-12` and `TN-C-13` the token `Agent 2, in its own systems`, which maps to **row 7 — outside C-05** — while both are C-05 **consumer obligations** belonging to **row 6**. Because rows 6 and 7 share the same owner, an agent-level check passed them (Agent 2's `D-6`). The tokens are now row-specific: an inside-C-05 consumer obligation carries `Agent 2, C-05 consumer`; the outside-C-05 half of the same responsibility is prose in §6.2 and never an implementer cell.

**The counts in the last column are the cells `DV-11` actually finds, not hand tallies** (Agent 2's `D-6b`: S4.1 said "19 `TN-P` rows" and "11 `TN-C` rows" where the instrument finds 23 and 12 — a third hand-copied count diverging from the instrument beside it, now closed by stating the machine-counted figures). 23 + 12 + 3 + 2 + 3 + 0 + 0 = **43**, the obligation count of `DV-1`.

**The row-level rule DV-11 enforces (Agent 2's `D-6`).** For each obligation row: the token must be declared above; the token's row must be in the **allowed-row set for that obligation's prefix** — `TN-P` → {2}; `TN-C` → {5, 6}; `TN-R` → {2, 4}; `TN-A` → {8}; and the row's owner must match the token's agent. A `TN-C` obligation carrying the row-7 token **fails**, which is the behaviour C9 asked for and which S3's agent-level check could not produce.

**Declared versus observed (Agent 2's `C9/§3.11.1`).** S3 declared six tokens and reported "6 role tokens" while only five appeared in cells. The table above declares **seven**; **five appear in obligation cells** — `producer owner`, `each consumer`, `Agent 2, C-05 consumer`, `Agent 1, shared support`, `Agent 1, subject to TD-09`. The other two — `Agent 2, in its own systems` (row 7) and `contract layer, owner pending TD-12` (row 3) — carry **no obligation row by design**: row 7 is outside C-05, and row 3 owns types rather than behaviour. They are declared so the mapping is complete if an obligation ever needs them. **DV-11 reports declared (7) and observed (5) counts separately**, so a declared-but-unused token can never again be reported as used.

---

## 6. Consumer information paths `[NEW at S3: C6, C7, C8; re-scoped at S4 by D-4 and the §9.2 conflict]`

### 6.1 `WindowKey` and `AttackTag` — who needs them, and why they are carried

The instruction is explicit that the snapshot must not grow automatically. So the case is made consumer by consumer, against the requirements Agent 2 actually submitted (`A2-C05` §7.6 marks both **Required**), and then against the alternatives.

| Consumer | Needs | Without the field | Verdict |
|---|---|---|---|
| **AI reaction** (Agent 2) | which attack, and which defence to **select**, **after a gap** | A resync into `Active` says an attack is active but not whether a block is even worth attempting — the one selection the resync exists to enable. Agent 2's words: *"a resync that says Active without saying unblockable is a resync my AI cannot act on"* | **needs both — for selection only** (`C05-6.4`) |
| **Audio cue** (**Agent 2** — the only owner, `C05-7.2` row 6; `TN-C-15`) | which attack, at the moment of the phase transition, to select the cue | The transition is observable but anonymous: every attack's windup sounds the same, or the consumer invents its own identity path | **needs `WindowKey`** |
| **Montage switch trigger** (Agent 2) | *when* to switch (from C-05) and *which* asset (from attack data) | The trigger works; the asset lookup has no key, so the montage system must re-derive identity through a path C-05 does not define | **needs `WindowKey`** |
| **Per-attack tuning** (Agent 1 and Agent 2) | stable key for authored response data | Tuning cannot be persisted per attack | **needs `WindowKey`** |
| **VFX marker** (Agent 2) | phase and timing (C-05); world placement (not C-05) | — | **needs neither**: placement resolves from `SourceEntityId` through the owning actor. `TN-C-12` |
| **Parry/block outcome** (Agent 1) | phase, from live producer state **off** the arbitration path | — | **needs neither**, and may use neither: no C-05 value decides a hit (`C05-6.4`, `TN-A-01`, `TN-A-02`, `TN-A-03`) |

**Three of four named consumers need identity; none of them can supply it from C-05's existing fields.** `AttackInstanceId` is unique per firing, so it cannot key authored data (the same attack fired twice has two ids); `SourceEntityId` names the entity, not the attack (an enemy has several attacks). Neither substitutes.

**Alternatives, considered and rejected:**

1. **State that C-05 does not carry identity and let consumers resolve it.** Rejected: the only holder of "which attack is this instance" is the producer, so every consumer would need its own path back to it. Three bespoke paths is three chances to diverge, and the divergence would be invisible — one consumer treats an attack as blockable while another dodges. It also cannot work after a gap for the same reason the pull was needed in the first place.
2. **Add a descriptor query to `ITDDTelegraphSource`** (`TryGetTelegraphDescriptor(Id, Out)`). Rejected: it is a **second read surface over the same instance**, with its own availability, liveness and staleness questions — the class of problem `DN-1`'s expired handle exists to solve. It also breaks `C05-2.3a`: a message would no longer carry the whole state, reintroducing a follow-up call on the message path, which is the defect S2 closed.
3. **Carry them in the snapshot.** **Chosen.** Both are authored at `Opened` and **fixed for that instance's lifetime** (`TN-P-19`; an identity change closes and reopens), and are therefore **versioned fields** that cannot age and cannot repeat the `INV-1` error. `FName` (8 bytes) and `FGameplayTag` (8 bytes) per snapshot; no serialisation, no allocation, no new dependency beyond the engine's own GameplayTags module, which every candidate has.

**Selection is not outcome — the one distinction this table must not blur.** `AttackTag` answers *"which response should I attempt?"* for a consumer, and that is all it answers. It never answers *"did this hit land, and was it parried?"* — that is `C05-6.1`'s same-frame phase overlap plus the defender's state, on the hit-resolution path, with no C-05 value in it (`TN-A-01`, `TN-A-02`, `TN-A-03`). §9.2 sets the three domains out and `TN-C-11` is written against the selection domain only.

**Boundary, stated so it cannot erode:** C-05 **transports** `AttackTag`; it does not define the tag, register it, or require a registry to exist. If no tag is authored, the field is empty and consumers behave as they would have without it. Tag **ownership and registration** stay where they are (registry/TD, U-14 adjacent) and are listed as a visible, non-blocking dependency at §14.2 B-13.

### 6.2 What stays outside C-05, and the path that resolves it

| Concern | Owner | Resolution path | Why not C-05 |
|---|---|---|---|
| **VFX world placement and attachment** | Agent 2, in its own systems | the owning actor, via `SourceEntityId`, and the attack's own attach data | C-05 carries values only; a transform is not timing, and `C05-2.8` excludes it |
| **Montage and cue asset selection** | Agent 2, in its own systems | attack data keyed by `WindowKey` | an asset reference is not timing; C-05 supplies the **trigger** and the **key** |
| **Per-attack response tuning** | the consuming agent | authored data keyed by `WindowKey` | data, not contract |
| **Damage and hit resolution** | C-03 (and C-04 for defence state), subject to TD-09 | — | `A2-C05` §7.5; unchanged; **no C-05 input** (`C05-6.4`, `TN-A-03`) |

### 6.3 `Resynchronised` — status

Declared as `FTDDTelegraphResynchronisation` at `C05-2.2`, normative in `EN-3` and `TN-C-09`, delivered consumer-locally on `FTDDTelegraphOnResynchronised` with no transport, no registry and no queue (§4.2). It is **not** demoted to a self-check: the type is contract-layer, the firing rule is a contract obligation, and `T-C05-45`, `T-C05-50` and `T-C05-57` assert on the declared artefact.

---

## 7. Producer obligations

Nineteen. `TN-P-01` … `TN-P-14` are S2's (with `TN-P-07` corrected twice: at S3 for the versioned class, at S4 to drop its identity clause); `TN-P-15` … `TN-P-17` are S3's; `TN-P-18` and `TN-P-19` are new in S4. **Every row is implemented by the owner of that producer** — Agent 2 on its enemy producers, Agent 1 on the player producer (`C05-7.2` row 2). All tests are `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-P-01** | Publish `Opened` before the first frame the wind-up is observable to a stream consumer, with revision 1 and the complete snapshot. | authored window → `Opened` | A pull consumer that missed `Opened` is not in error; its first pull is a baseline (EN-1). For a stream consumer a missed open is a producer violation. | `Opened` precedes every other message for the instance | T-C05-07 | producer owner |
| **TN-P-02** | `AttackInstanceId` is unique per open instance and never reused. | allocation → `FGuid` | A reused id is a producer violation; consumers and the directory treat it as a new instance and diagnose in Test/Development. | n/a | T-C05-26 | producer owner |
| **TN-P-03** | Exactly one `Closed` per instance, carrying a close reason; no message at all for that instance afterwards. | close event → `Closed` | A second close is a duplicate (rejected); a post-close message is rejected and diagnosed. | after every other message for the instance | T-C05-21 | producer owner |
| **TN-P-04** | Every cancellation path closes: ability cancel, montage abort, interruption, forced transition, requirement change, **a change of attack identity (`TN-P-19`)**, the producer's own death. | cancel source → `Closed` with the matching reason | An unclosed cancelled instance remains pullable — a producer violation the consumer cannot detect, which is why it is normative. | same frame as the cancel | T-C05-22 | producer owner |
| **TN-P-05** | Invalidate open instances in the teardown path, before the producer stops being valid. | `EndPlay` → deregistration and `Closed(ProducerInvalidated)` | Best effort; the pull's `false` and directory liveness are the fail-safe (`TN-R-02`), not a substitute. | before removal from the world | T-C05-23 | producer owner |
| **TN-P-06** | Stream-out invalidates only that producer's instances; it neither requires nor implies world teardown, and it deregisters them from the directory even when no `Closed` can be emitted. | unload → deregistration of its own ids | Other producers are untouched; world teardown removes everything because the world-scoped owner is destroyed. | n/a | T-C05-24 | producer owner |
| **TN-P-07** | **Corrected at S4.** `StateRevision` strictly increases on **every change to a versioned field that can change mid-instance** — every phase transition and every retime — and two observations at the same revision never differ in any `VF` field (`INV-1`). Changes to `OF` fields do not advance it. **Identity fields cannot change mid-instance at all (`TN-P-19`), so no revision ever carries an identity change.** | state change → revision + 1 | An observation at an equal revision with different `VF` content is a producer violation and is never applied; an equal revision with different `OF` content is normal aging, not a violation. A revision whose `WindowKey` or `AttackTag` differs from the previous revision's is a violation: it is the `TN-P-19` case, not a state change. | monotone per instance | T-C05-16, T-C05-62, T-C05-66 | producer owner |
| **TN-P-08** | One `Retimed` per `CustomDilation` change, published in the frame of the change, reflected in live state no later than that frame; ordered after any phase transition in the same frame (`PO-3`). **Never batch, coalesce, throttle or defer.** | dilation change → `Retimed` + live-state update | A batched retime is a violation; `UTDDHitStopSubsystem` boundaries are explicitly not exempt. | publish and live-state update in the same frame | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | producer owner |
| **TN-P-09** | Publish no message for an instance that is closed or was never opened. | stray publish → rejected | Rejected with a diagnostic; no directory entry is created and no held state changes. | n/a | T-C05-27 | producer owner |
| **TN-P-10** | All axis values come from the shared axis of `A1-R3` §3.3(a); never wall-clock, frame count or another entity's local time. | engine time → axis value | Any other domain is a violation, detected by a wall-clock fixture. | n/a | T-C05-15 | producer owner |
| **TN-P-11** | `TryGetOpenTelegraph` answers from live state at call time: `AxisNow` is the call's axis instant, `RemainingLocalSeconds` satisfies `INV-2` at that instant, and every `VF` field equals the instance's current revision exactly. Never a cached copy older than the last completed update. | id → snapshot or `false` | A stale `VF` copy is a violation; a caught-up `OF` pair is not. `false` for an open instance is a violation except during teardown (`TN-P-05`). | as of the last completed update before the call | T-C05-06, T-C05-40, T-C05-42 | producer owner |
| **TN-P-12** | No frame deltas, random seeds or tick-order dependence in any published or pulled value. | deterministic inputs → identical outputs | Non-determinism makes every suite flaky; treated as a producer defect. | n/a | T-C05-01 | producer owner |
| **TN-P-13** | Every phase transition advances `StateRevision` by exactly one, even when the timing block and every other value are unchanged, and publishes one `PhaseChanged` carrying the new snapshot. A phase change may not be published at the revision the consumer already holds. | phase transition → revision + 1 and `PhaseChanged` with the new snapshot | A phase change at an unchanged revision is the defect this obligation forbids; diagnosed in Test/Development. | one revision per transition | T-C05-43, T-C05-44, T-C05-45, T-C05-62 | producer owner |
| **TN-P-14** | Every message carries the complete snapshot at emission (`C05-2.3a`), identity fields included; no message carries a partial aspect. | state → `FTDDTelegraphMessage` with full snapshot | A partial message is a violation: it can advance the revision while leaving another aspect stale. | n/a | T-C05-49 | producer owner |
| **TN-P-15** | **New at S3, extended at S4.** Within one frame, publish in the canonical order of `C05-2.9`: all phase transitions in authored order, then all dilation changes in the order applied. One phase change plus one retime is `PhaseChanged` at `n+1` then `Retimed` at `n+2` — never one message, never the reverse order, never a shared revision. Each of those messages carries the content rule of `PO-5` (`TN-P-18`). | frame contents → ordered message sequence | Any other order or any merged revision is a violation, and it is detectable because the resulting message sequence differs from the canonical one. | canonical, total, per frame | T-C05-51 | producer owner |
| **TN-P-16** | **New.** Two phase transitions within one frame are two transitions: two revisions, two `PhaseChanged`, authored order, never collapsed or merged; a section-boundary pair is published in full (`PO-4`). | collapsed boundary → two messages | Collapsing, dropping the intermediate phase, or publishing one message for two transitions is a violation. | authored order within the frame | T-C05-52, T-C05-53 | producer owner |
| **TN-P-17** | **New.** Every published snapshot satisfies `INV-2` at its own `AxisNow`: `RemainingLocalSeconds = max(0, (PhaseEndAxis − AxisNow) × ProducerRate)`, so that a consumer's aging rule reproduces the producer's own value exactly. | snapshot → internally consistent `OF` pair | An inconsistent snapshot makes the consumer's aging diverge from the producer's; diagnosed at emission in Test/Development. | evaluated at the snapshot's own `AxisNow` | T-C05-54 | producer owner |
| **TN-P-18** | **New (D-2).** Publish **between** applications, not after them (`PO-5`): apply a change, publish at its revision, apply the next change, publish again. The producer's live state may never hold a `VF` change that no published revision covers, so a pull taken between two same-frame publications returns the earlier revision's `VF` exactly. | frame's change list → message sequence interleaved with application | Publishing a batch at end of frame, or applying all changes before publishing the first message, is a violation: it makes a mid-frame pull return `VF` the published revision does not cover (`INV-1` through `TN-P-11`). | canonical, total, per frame; interleaved with application | T-C05-65 | producer owner |
| **TN-P-19** | **New (D-3).** `WindowKey` and `AttackTag` are **fixed for the instance's lifetime**. A change of attack identity — re-authored definition, substituted attack, requirement change — **closes the instance** (`TN-P-04`) and opens a new one with a new `AttackInstanceId` at revision 1. It is never carried as a mid-instance revision. | identity change → `Closed` + new `Opened` | A revision whose identity differs from the previous revision's is a violation, and consumers must treat the instance as ended rather than adopt it (`T-C05-66`). | close precedes the new `Opened`; no overlap of ids | T-C05-66 | producer owner |

`TN-P-07` and `TN-P-13` overlap by design: one states monotonicity for all versioned changes, the other that phase changes are among them. The duplication is deliberate — the missing case is the one that produced Agent 3's finding.

---

## 8. Consumer obligations

Fifteen. `TN-C-01` … `TN-C-09` are S2's, corrected where Agent 2's findings require; `TN-C-10` … `TN-C-13` are S3's; `TN-C-14` and `TN-C-15` are new in S4 (`D-1`, `D-4`). **Each obligation is implemented by each consuming agent in its own code** — Agent 1 for defence **selection**, dodge, camera response and framing; Agent 2 for AI reaction, **audio cue selection (the only C-05 audio responsibility)**, montage trigger and VFX timing. **Agent 1 has no C-05 audio responsibility** (`C05-7.2` row 5; `TN-C-15`; `DV-22`). Tests `PROPOSED / NOT RUN`.

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-C-01** | Adopt only on strictly greater `StateRevision`; discard equal or lower silently, for messages and pulls alike. | snapshot, held revision → adopt or discard | **Corrected justification:** an equal-revision observation can differ only in `OF`, which the consumer re-derives by `INV-2`, so discarding loses no state change (§3.5). A `VF` difference always arrives with a revision bump. | commutative — outcome independent of arrival order | T-C05-02, T-C05-03, T-C05-46, T-C05-56, T-C05-62 | each consumer |
| **TN-C-02** | First observation of an instance establishes the baseline; record the phase as held and fire no entry for it. | first observation → baseline | Firing entry on a baseline double-fires on every subscribe. | baseline before any entry evaluation | T-C05-08, T-C05-09, T-C05-47 | each consumer |
| **TN-C-03** | After the baseline, entry at most once per `(AttackInstanceId, phase)`; a retime never re-fires; a duplicate `PhaseChanged` fires nothing. | phase transition → at most one entry | A second entry for the same phase is detectable by counting. | per consumer, per phase | T-C05-10, T-C05-11 | each consumer |
| **TN-C-04** | On `incoming > held + 1`, record a gap and set `bStateGapObserved` until the instance closes. Never interpolate or extrapolate. | gap → flag | Clearing the flag before close is a violation. | on adoption of the post-gap snapshot | T-C05-12, T-C05-13 | each consumer |
| **TN-C-05** | After a gap, recover with **one** pull; if it is unavailable or not newer, report timing as unknown and diagnose rather than guess. | id → current snapshot or unknown | "Unknown" is a legitimate terminal state for that instance. | once per gap | T-C05-14, T-C05-19, T-C05-44 | each consumer |
| **TN-C-06** | Removal is closure: a pull returning `false`, an unresolvable id, or a `Closed` message means closed — release the block, fire no further entry, raise no error. **A `Closed` closes regardless of its revision (`TM-1`).** | false, unresolvable id, or `Closed` → closure | Treating "not found" as an error is a defect; so is discarding a `Closed` because its revision is not newer. | immediate on observation | T-C05-25, T-C05-48 | each consumer |
| **TN-C-07** | Evaluate `Dead > Cinematic > Staggered` in priority order over the three carriers of `C05-6.3`; never compare carriers. | published state → one effective value | Comparing an enum to a tag is a violation. **Inherits `C05-6.3`'s `PROPOSED — NOT FROZEN` status and its `C-04-4` coupling (§14.2 B-11).** | priority order, first match wins | T-C05-35, T-C05-36, T-C05-37, T-C05-38, T-C05-39 | each consumer |
| **TN-C-08** | Never treat a pull as revision history; a post-gap block is current state, not a substitute for what was missed, and a phase absent from a pull is not a phase that did not occur (`RS-3`). | pull result → current value | A consumer that assumes full recovery makes telemetry and AI timings silently wrong. | n/a | T-C05-20, T-C05-50, T-C05-53 | each consumer |
| **TN-C-09** | A snapshot adopted across a gap fires no phase entry; the consumer raises exactly **one** `FTDDTelegraphResynchronisation` per gap, on its own delegate, carrying the landed snapshot and no history, and synthesises no entries for phases it did not observe. | gap adoption → zero entries, one resynchronisation | A fabricated entry is a violation; more than one resynchronisation per gap is a violation; a resynchronisation after a contiguous adoption is a violation. | immediately on gap adoption, before any further entry evaluation | T-C05-45, T-C05-50, T-C05-53, T-C05-57 | each consumer |
| **TN-C-10** | **Corrected at S4.** Age a held snapshot by `INV-2` — `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` — and never treat a difference confined to `OF` as a state change, a gap, or a diagnostic. Never age by wall-clock elapsed or by the consumer's own dilation. **The obligation is limited to the revision the consumer holds:** once a newer revision exists — including a `Retimed` it has not yet adopted — the aged value is stale by construction (`INV-2` precondition) and the consumer's remedy is to adopt, or to re-pull (`TN-C-14`), never to keep aging and call it correct. | held snapshot, axis now → remaining local seconds | Wall-clock aging is wrong across any pause or dilation change; treating `OF` drift as a change produces a false gap on every frame; aging past an unadopted retime is stale by `INV-2` and must not be reported as the current remaining time. | continuously, per consumer, within the held revision | T-C05-54, T-C05-55, T-C05-56, T-C05-64 | each consumer |
| **TN-C-11** | **Corrected at S4 — selection only.** Take attack identity and the response the attack invites (`WindowKey`, `AttackTag`) from the adopted snapshot — including after a resynchronisation — and from no other source, **for selection**: which defence to attempt, which cue to pick, which montage family, which tuning row. **`TN-C-11` grants no authority over a hit's outcome:** no C-05 value, `AttackTag` included, may be read on the hit-resolution path, and whether an attack is actually blockable is decided there by the attack/defence contracts (`C05-6.4`, `TN-A-01`, `TN-A-02`, `TN-A-03`). No consumer may add a second lookup surface for identity. | snapshot → attack identity, response selection | A consumer that re-derives identity through its own path will disagree with another consumer's; that divergence is the failure this obligation forbids. A consumer that lets `AttackTag` decide a hit's outcome commits the `TN-A-02` violation this clause exists to fence off. | on adoption, before any selection decision; never on the hit-resolution path | T-C05-57, T-C05-58, T-C05-63 | each consumer |
| **TN-C-12** | **New at S3; implementer re-mapped at S4.** For VFX, consume **timing and phase only**; resolve world placement and attachment from `SourceEntityId` through the owning actor, outside this contract. No contract type carries a transform, and none may be added. | snapshot + `SourceEntityId` → marker start/stop and placement | A marker placed from anything in C-05 is a violation of `C05-2.8`; the contract supplies no position and must not be asked to. | on the phase transition that starts or stops the marker | T-C05-59 | Agent 2, C-05 consumer |
| **TN-C-13** | **New at S3; implementer re-mapped at S4.** Montage selection is a **trigger-and-key** relationship: C-05 supplies **when** to switch (the phase transition and its phase) and **which attack** (`WindowKey`); the montage asset is selected from attack data keyed by `WindowKey`, outside this contract. C-05 carries no animation asset reference. | phase transition + `WindowKey` → montage switch request | Selecting an asset from anything in C-05 is a violation; so is switching on a retime (a retime is not a switch trigger). | on the phase transition, in the same frame | T-C05-60 | Agent 2, C-05 consumer |
| **TN-C-14** | **New at S4, rewritten at S4.2 (`D-1`; Agent 3 finding 4; `D-1a`; `D-1b`).** Five rules, from which the staleness bound is **derived** rather than asserted. **(i) Call-site scope.** The obligation attaches to the **call site**, not to an agent: every call site that reads `RemainingLocalSeconds`, or derives a remaining time from it, is timing-dependent and must satisfy (ii)–(iv). A consumer with no such call site is governed only by (v). **(ii) Refresh in the frame, before first use.** Before its first timing-dependent use in each frame, the consumer takes a **successful observation** of the instance — a pull, or an adopted message — and uses that observation's `VF` for the rest of the frame. The observation's `AxisNow` must not precede the start of the frame in which it is used: **a value carried across a frame boundary is not used.** **(iii) Maximum interval between successful refreshes.** While any timing-dependent call site is active, successive successful refreshes of one instance are at most **one frame apart**, measured **on the shared axis** — from the earlier observation's `AxisNow` to the later one's. Wall-clock time, frame counters and the consumer's own dilation are not the measure. **(iv) Fresh pull before the action when the guarantee cannot be established.** If the consumer cannot show (ii) — the pull failed, the newest successful observation's `AxisNow` precedes the current frame's start, or the snapshot was adopted before the instance's current revision existed — it **must not perform the timing-dependent action on the aged value**: it re-pulls until a pull succeeds, or suppresses the action for that frame. **(v) Message-only residual, still accepted.** A consumer with no timing-dependent call site may rely on messages alone; if it loses a `Retimed` it remains rate-stale until the next revision, and that residual is **accepted and stated**, not hidden (`EX-5` case (d); §3.6 rationale (c)). **The bound (closing `D-1a`), stated exactly:** under (ii) and (iv), **at most one frame** separates the publication of a missed revision from the timing-dependent use that follows it, and at most one frame separates it from the next successful refresh — measured on the shared axis from that publication to the use. This is **not** a same-frame guarantee that a pull lands after the producer's publication inside the frame; it is an upper bound of one frame, and the worst case approaches but never reaches one frame (a revision published immediately after the frame's observation, used at the frame's last instant). The residual in (v) is unbounded in the same sense and is accepted **for message-only consumers only**. | held instance, frame boundaries, axis → observation used this frame, and its age | Losing a `Retimed` is the case this closes: a message-only consumer is rate-stale by the retime ratio (accepted, (v)); a consumer with a timing-dependent call site that skips (ii) is rate-stale **across frames and without bound** — Agent 3's counterexample, which satisfies "at least once per frame" but reaches nearly two frames; a consumer that fails (iv) acts on aged data rather than re-pulling or suppressing. | at most one frame between successful refreshes; observation in the frame of use; re-pull or suppress when (ii) cannot be shown | T-C05-64 | each consumer |
| **TN-C-15** | **New (D-4).** Audio cue selection is a C-05 consumer responsibility of **Agent 2 alone**: the cue is selected on the **phase transition**, using the adopted snapshot's `Phase`, `WindowKey` and `AttackTag` (`TN-C-11`). A `Retimed` raises no cue change, and the cue **asset** is resolved from audio data keyed by those identity fields, outside this contract. | phase transition + identity → cue selection request | Raising a cue on a retime is a violation; selecting a cue from an asset reference carried by C-05 is impossible by `C05-2.8` and must not be attempted. | on the phase transition, in the same frame | T-C05-67 | Agent 2, C-05 consumer |

---

## 9. Shared read-surface and arbitration obligations

Six read-surface obligations (`TN-R-01` … `TN-R-06`) and **three** arbitration obligations (`TN-A-01` … `TN-A-03`, the third new in S4). Tests `PROPOSED / NOT RUN`.

### 9.1 The read surface

The six `TN-R` obligations below are unchanged from S3 except `TN-R-01`'s cross-reference.

### 9.2 `C05-6.4` — `AttackTag` is descriptive, not decisive `[NEW: resolves the TN-C-11 / TN-A-01-02 conflict]`

> **C05-6.4.** Three domains, and the `AttackTag` has a different standing in each:
>
> | Domain | Question | Who decides | May a C-05 value be used? |
> |---|---|---|---|
> | **Creation** | *What is this attack, and what response does it invite?* | the **producer** authors `WindowKey` and `AttackTag` at `Opened` and publishes them in the snapshot (`TN-P-19`, `TN-P-14`) | it **is** the C-05 value — this is where it comes from |
> | **Selection** | *Which defence, cue, montage family or tuning row should this consumer choose?* | **the consumer**, in its own code, from the adopted snapshot (`TN-C-11`, `TN-C-15`) | **yes** — this is the whole purpose of carrying the tag |
> | **Outcome** | *Did this hit land, and was it parried or blocked?* | `C05-6.1`'s same-frame phase overlap plus the defender's live state, on the hit-resolution path — **never** a C-05 value, `AttackTag` included | **no** — `TN-A-01`, `TN-A-02`, `TN-A-03` |
>
> **The line, in one sentence:** a consumer may use `AttackTag` to decide what to *attempt*; nothing may use it — or any other C-05 value — to decide what *happened*. Whether an attack is genuinely unblockable is enforced where the hit is resolved, by the attack and defence contracts (C-03, C-04, subject to TD-09), not by C-05's copy of the tag.

**Why this is a clause and not a comment.** S3's `TN-C-11` required every consumer to take "blockability" from `AttackTag`, which — read literally — puts a C-05 value inside the decision `TN-A-02` forbids it from touching. That is a real contradiction in S3's text, visible without any review, and it is resolved here rather than by softening either clause.

**What each clause now says, and what was deliberately left alone:**

- `TN-C-11` — **rewritten**: identity and the invited response come from the snapshot **for selection**; it explicitly grants no authority over a hit's outcome.
- `TN-A-02` — **extended, not weakened**: it now names `AttackTag` so that "no arbitration decision depends on any value produced by C-05" cannot be read as excluding the tag.
- `TN-A-03` — **new**: the positive form of the same rule, so a producer-, consumer- or arbiter-side implementation has an obligation it can fail.
- `C05-6.1`, `TN-A-01`, `TN-A-02`'s core, the directory's content and the arbitration row of `C05-7.2` — **unchanged**. The arbitration boundary is not widened, not narrowed and not re-negotiated.

**Independently verified, not assumed** (the disposition asks for exactly this):

| Question | Answer | Evidence |
|---|---|---|
| Does the resolution let a C-05 value decide a hit? | **No.** The outcome domain names `C05-6.1` and the defender's state; the tag appears in neither. | `TN-A-02`, `TN-A-03`; §13 DV-20; T-C05-63 |
| Can a consumer still act after a resync? | **Yes.** `TN-C-11`'s selection domain keeps `AttackTag` available exactly where S3 wanted it. | `EX-7`, T-C05-57 |
| Is there any new read of the telegraph on the arbitration path? | **No.** No clause adds one, and `C05-2.8` now excludes arbitration inputs by name. | §4.8, DV-20 |
| Does it move the arbitration boundary in either direction? | **No.** `C05-6.1`/`TN-A-01` are byte-identical to S1 and S3; only the *descriptive* clause gained a sentence and an obligation. | §16 diff table |
| Does it re-open TD-09? | **No.** Who *owns* the unblockable determination is still TD-09's, untouched. C-05 only says it is not C-05's. | §14.1 B-2 |

**Provenance caveat, repeated because it matters:** Agent 3's review is not in this repository (§0.2), so **this is S4's own resolution and not their proposed wording**. §18.2 asks them to confirm it or substitute theirs.

### 9.3 The obligations

| ID | Normative requirement | Inputs → outputs | Failure and invalidation | Ordering | Test | Implemented by |
|---|---|---|---|---|---|---|
| **TN-R-01** | The directory stores per instance only the id, `SourceEntityId` and one weak liveness handle — no timing, no phase, no revision — and never serves timing through the handle. **Register on `Opened`; deregister on `Closed` or producer invalidation, whichever first.** | registration → association record | A record carrying timing is a violation detectable by structure. An expired handle resolves `false`; teardown drops all. | registration completes before a pull by id can succeed | T-C05-28, T-C05-29, T-C05-61 | Agent 1, shared support |
| **TN-R-02** | `TryGetOpenTelegraph` returns `false` for closed instances, instances the producer never opened, and instances during teardown; never a partial or stale-filled record. | id → snapshot or `false` | `false` is never an error (`RM-2`); `true` for a closed instance is a violation. | n/a | T-C05-04, T-C05-05 | producer owner |
| **TN-R-03** | `GetOpenTelegraphIds` reports only the calling producer's own instances; not a world query, not aggregated in this version, not X-1. | producer → its ids | Answering with other producers' ids would silently re-create custody. | n/a | T-C05-30 | producer owner |
| **TN-R-04** | A pull returns a value copy, is callable from any consumer phase without re-entrancy, reflects the producer's last completed update, and mutates nothing the caller can see. | call → copy | A returned reference into producer storage or a re-entrant marshal is a violation. | as of the last completed update | T-C05-31 | producer owner |
| **TN-R-05** | **Corrected.** A pull at revision `R` returns **`VF` content identical to every other observation at `R`** (`INV-1`) and an `OF` pair consistent with `INV-2` at its own call instant. It may never manufacture a `VF` state the revision does not cover, and it is never required to reproduce an earlier observation's `OF` values. | id, held revision → snapshot | A `VF` difference at equal revision is a violation; an `OF` difference is expected aging and is not a diagnosable event. | n/a | T-C05-46, T-C05-49 | producer owner |
| **TN-R-06** | **New.** The directory performs no scheduling: it holds no clock, no queue, no ordering, no phase, no revision and no window; it emits nothing and wakes nothing; it answers id→producer and liveness only. | query → producer handle or `false` | Any added timing field, any ordering or deferral behaviour, or any emission from the directory is a violation — it would make the directory the director `A2-C05` §7.1 rejected. | n/a | T-C05-61 | Agent 1, shared support |
| **TN-A-01** | Parry is `C05-6.1`: same-frame phase overlap. The attacker's phase is read on the hit-resolution path from the component that owns the attack instance — never from the pull, the directory or a published block; no timestamp subtraction, no late tolerance. | hit data, defence state, attacker live phase → parry outcome | Any C-05 value influencing the outcome is a violation; a wrong timing block must not change the result. | in the frame the hit is resolved | T-C05-32, T-C05-33 | Agent 1, subject to TD-09 |
| **TN-A-02** | No arbitration decision depends on any value produced by the C-05 contract — **`AttackTag` included**. The tag is descriptive for selection (`TN-C-11`); it is never an input to a hit-resolution decision. | as above → outcome plus diagnostic | An observed read of the telegraph surface, **or of `AttackTag` from it**, on the arbitration path is a violation, detectable with a spy. | n/a | T-C05-34, T-C05-63 | Agent 1, subject to TD-09 |
| **TN-A-03** | **New (conflict resolution).** The hit-resolution path uses exactly three inputs — the incoming hit data, the defender's live defence state, and the attacker's live phase from the component that owns the instance (`TN-A-01`). **A C-05 snapshot, message, directory record or `AttackTag` value may not appear among them**, and the unblockable determination is the attack/defence contracts' (C-03, C-04, subject to TD-09). | hit data, defence state, attacker live phase → outcome, and a diagnostic if a C-05 read is attempted | Reading any C-05 artefact — including `AttackTag` from a snapshot held for selection — on the hit-resolution path is a violation, detectable with a spy and with a corrupted-tag fixture. | in the frame the hit is resolved | T-C05-63 | Agent 1, subject to TD-09 |

---

## 10. Worked transitions

Ten examples. `rev` is `StateRevision`; "held" is what a given consumer holds; each scenario is a candidate acceptance case (§12).

### 10.1 EX-1 — a phase-only transition, observed in order

| t | Producer event | Message | Snapshot |
|---|---|---|---|
| 1 | wind-up begins, `ProducerRate` 0.05 | `Opened` | Windup, rev **1** |
| 2 | wind-up ends; **no dilation change, endpoints unchanged** | `PhaseChanged` | Active, rev **2** |

Consumer holds rev 1, receives rev 2: `2 == 1 + 1` → contiguous, adopt, phase differs → **entry fires once**.

### 10.2 EX-2 — the transition is missed, and a pull recovers it

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | **message lost** |
| 3 | nothing changes | pulls: Active, rev **2**; `2 > 1` → adopt; `2 == 1+1` → **not** a gap → entry fires once |

The pull's `OF` pair is later than it would have been at t=2; that difference is aging (`INV-2`), not a state change, and it is not diagnosed (`TN-C-10`).

### 10.3 EX-3 — several transitions missed (gap)

| t | Producer | Consumer |
|---|---|---|
| 2 | `PhaseChanged` Active, rev 2 | lost |
| 3 | `PhaseChanged` Recovery, rev 3 | lost |
| 4 | nothing changes | pulls: Recovery, rev **3**; `3 > 1+1` → **gap** |

Adopt Recovery; **no entry** for Active or Recovery; exactly one `FTDDTelegraphResynchronisation` carrying the landed Recovery snapshot; `bStateGapObserved` set until close.

### 10.4 EX-4 — a retime only

`Retimed`, rev 3, `ProducerRate` 0.2, endpoints recomputed, `OF` re-anchored at the new `AxisNow`. Contiguous → adopt, no entry, no resynchronisation. `TN-P-08` still forbids batching: two boundaries in one frame are revisions 3 and 4 (`PO-2`).

### 10.5 EX-5 — the same-frame cases, enumerated `[REWRITTEN at S3: C4c; case (d) added at S4: D-1]`

S2's version of this example described one phase change and one retime in a frame and then assigned revisions to a *different* scenario. It is replaced, and the ordering it now states is normative (`C05-2.9`).

| Case | What the frame contains | Message sequence | Revisions | Consumer holding `n` |
|---|---|---|---|---|
| **(a)** phase only | Windup→Active, dilation unchanged | one `PhaseChanged` | `n+1` | adopt, entry once, no gap |
| **(b)** retime only | one `CustomDilation` change, phase unchanged | one `Retimed` | `n+1` | adopt, no entry, no gap |
| **(c)** one of each, both received | Windup→Active **and** a dilation change | `PhaseChanged` then `Retimed` | `n+1` then `n+2` | adopt both, entry once, no gap |
| **(cʹ)** one of each, only the retime received | as (c), `PhaseChanged` lost | `Retimed` only | `n+2` arrives, `n+1` held | `n+2 > n+1` → **gap**, no entry, one resynchronisation landing in Active (`EN-3`) |
| **(d)** one of each, only the phase received | as (c), `Retimed` lost | `PhaseChanged` only | `n+1` arrives, `n` held | adopt: entry once, **no gap** (contiguous). The consumer is **phase-correct and rate-stale** — it holds the pre-retime `ProducerRate`. Its obligations are `TN-C-10` (age against the revision it holds, not against a rate it does not have) and `TN-C-14` (a timing-dependent call site must hold an observation taken **in the frame of use** and re-pull before acting when it cannot show one — measured on the shared axis, with the bound derived in `TN-C-14`); a message-only consumer stays rate-stale and that residual is **accepted and stated**, not hidden |
| **(e)** one of each, received out of order | the two messages arrive `Retimed` first | consume in revision order: `n+2` alone → gap and resync; `n+1` later → stale (`n+1 < n+2`) → discarded | see left | phase and timing are never wrong, but the entry is not fired — the consumer resyncs instead |

**The order is normative, not advisory** (`PO-3`, `TN-P-15`): two conforming producers may not publish (c) in different orders, because which message lands at `n+1` decides whether entry fires or a resync is raised.

**What case (d) adds, and why S3 was wrong to omit it.** Cases (c) and (cʹ) cover loss of the *first* message. Loss of the *second* is the cheaper failure — the consumer has the phase — and S3 treated it as "merely needs a resync", which no clause obliged and which `AD-2` never triggers, because no later revision arrives. **S4 states three things instead of one assumption:** the consumer is rate-stale by exactly one revision; `TN-C-14` bounds how long a timing-dependent consumer may remain so (one frame, by re-pull); and a message-only consumer's staleness is **accepted, with its consequence named** — its remaining-time estimate can be wrong by the whole ratio of the retime until the next phase transition. Agent 2 offered this as option (iii); S4 takes (iii) **and** (i), because (iii) alone documents the defect without bounding it, and (i) costs one pull per frame.

**Why (ii) — forbidding the same-frame pair — was not taken.** Agent 2's option (ii) would require the producer not to publish a same-frame `Retimed` unless delivery of both messages in order is guaranteed. C-05 deliberately specifies no transport (`C05-2.3a`, §4.2), so the producer **cannot** guarantee ordered delivery of a pair, and (ii) would therefore forbid every same-frame phase+retime — contradicting `PO-3`/`TN-P-15`, which require exactly that pair. Rejecting (ii) is a consequence of a decision S3 preserved, not a new one.

### 10.6 EX-6 — repeated pulls and duplicate messages (with aging)

Consumer at rev 3 pulls twice with no producer change, one frame apart. Both returns carry **identical `VF`**: same phase, same endpoints, same `ProducerRate`, same `WindowKey`, same `AttackTag`. Their `OF` pairs differ: `AxisNow` is one frame later and `RemainingLocalSeconds` is lower by exactly one frame × `ProducerRate` (`INV-2`). The second pull is **discarded** (`AD-1`) — and nothing is lost, because the consumer's own aging of its held snapshot yields the same remaining time (§3.5). No entry, no resynchronisation, no diagnostic. **A change of phase at an unchanged revision remains unrepresentable.**

### 10.7 EX-7 — late subscriber, then a real transition

A consumer subscribes mid-Active and pulls Active at rev 5: baseline (`EN-1`), **no entry**, and it now holds `WindowKey` and `AttackTag` for that attack — so its first defensive decision is already informed. The producer then enters Recovery at rev 6: contiguous, phase differs → **exactly one entry**. Miss rev 6 and pull rev 7 Recovery later → gap: no entry, one resynchronisation, and the landed snapshot still carries identity, so the resync is actionable (`TN-C-11`).

### 10.8 EX-8 — terminal close at an unchanged revision

Consumer holds rev 3. The producer publishes `Closed(Natural)` carrying rev 3, because a close does not advance the state revision. `TM-1` applies: the instance closes, the consumer releases state, fires nothing further, raises no error. Without `TM-1`, `AD-1` would have discarded the close as an equal revision.

### 10.9 EX-9 — aging and the clamp `[NEW at S3: C4a]`

Producer opens Windup with `PhaseEndAxis = 4.0`, `AxisNow = 0.0`, `ProducerRate = 0.05`, so `R0 = (4.0 − 0.0) × 0.05 = 0.20` local s.

| Axis now | `RemainingLocalSeconds` by `INV-2` | Consumer aging from the t=0 snapshot | Agree? |
|---|---|---|---|
| 0.0 | 0.2000 | `0.20 − (0 − 0) × 0.05 = 0.2000` | yes |
| 0.2 | 0.1900 | `0.20 − 0.2 × 0.05 = 0.1900` | yes |
| 2.0 | 0.1000 | `0.20 − 2.0 × 0.05 = 0.1000` | yes |
| 4.0 | **0.0000** | `0.20 − 4.0 × 0.05 = 0.0000` | yes |
| 8.0 | **0.0000** (clamped) | `max(0, 0.20 − 8.0 × 0.05) = 0.0000` | never negative |

The phase is complete when `Axis(t) − AxisNow ≥ R0 / ProducerRate` (here `0.20 / 0.05 = 4.0` axis s), which is `A1-R4` §3.3(e)'s equivalent condition and the same equation as `INV-2`. **A wall-clock consumer diverges at the first pause** — the negative control in `T-C05-55`.

### 10.10 EX-10 — two transitions in one frame, and what a consumer can still see `[NEW at S3: C3]`

A montage section boundary pair lands in one tick: Windup ends and Active begins, then Active ends and Recovery begins, both before the frame ends. `PO-4` requires **two** messages: `PhaseChanged(Active)` at `n+1`, `PhaseChanged(Recovery)` at `n+2`.

| Consumer | What it receives | Result |
|---|---|---|
| Attentive | both | contiguous; entry once for Active, once for Recovery (`EN-2`), no gap |
| Late by one | only `n+2` | `n+2 > n+1` → gap; no entry; one resynchronisation landing in Recovery |
| Pull-based only | a pull after the frame | returns **Recovery at `n+2`**; Active is not observable at all — a legitimate outcome (`RS-3`), not a missing state |

The producer may not collapse the pair into one revision "because the frame only shows Recovery". A phase that a consumer never observes is not a phase that never happened, and the AI's audit trail must be able to tell those apart.

### 10.11 EX-11 — the mid-frame pull sees the published revision's `VF` `[NEW: D-2]`

A frame where the producer transitions Windup→Active at axis 40 and then dilates `ProducerRate` 1.0 → 1.5 at axis 41. Under `PO-5`/`TN-P-18` the producer interleaves:

| Producer step | Published at | `Phase` | `ProducerRate` | A pull taken now returns |
|---|---|---|---|---|
| applies the transition | `n+1` (`PhaseChanged`) | `Active` | **1.0** | Active, rate **1.0** — the `n+1` `VF` exactly (`TN-R-05`) |
| applies the dilation | `n+2` (`Retimed`) | `Active` | **1.5** | Active, rate **1.5** |

**What S3 permitted and S4 forbids:** a producer that applied both changes before publishing either would have a pull between the two messages return rate 1.5 under revision `n+1` — `VF` the published revision does not cover, which `INV-1` forbids and which no test could see. **`T-C05-51` is extended** to assert `ProducerRate` in each of the three observations (the `n+1` message, the mid-frame pull, the `n+2` message) rather than only their order, and **`T-C05-65`** asserts the mid-frame pull directly.

**The reading that `PO-5` selects, stated once:** `n+1` carries the state *as of* `n+1` (pre-retime rate); `n+2` carries the state *as of* `n+2` (post-retime rate). The alternative — retro-fitting the new rate into `n+1` — is not merely discouraged, it is a `TN-P-18` violation.

### 10.12 EX-12 — an attack identity change closes and reopens `[NEW: D-3]`

An enemy's attack definition is re-authored mid-fight so the instance would need a different `WindowKey`. Under `TN-P-19` the producer **does not** publish a revision carrying the new key:

| Step | Published | Held by the consumer |
|---|---|---|
| identity change decided | `Closed` (`Cancelled`) for instance `A`, no revision advance (`TM-1`) | `A` closes, terminal |
| new attack opens | `Opened` for instance `B`, revision **1**, new `AttackInstanceId` | `B` baseline; `EN-1` suppresses an entry for B's opening phase |

**Consumers are not asked to reconcile identity inside an instance**, and no consumer may treat a differing `WindowKey` at a higher revision as a legitimate update — `TN-P-07`'s failure column makes that a violation and `T-C05-66` asserts it. This is the change path that S3's "constant for the lifetime" sentence lacked, and it is why S4 keeps constancy instead of Agent 2's suggested mutability: the mutability option needs a revision to carry the new identity, which is exactly what `INV-1` and `TN-P-07` were fixed to prevent.

---

## 11. Traceability

### 11.1 The instruction's validation requirements → clause → check → test

| # | Validation requirement (instruction §4) | Clause | Document check | Test |
|---|---|---|---|---|
| 1 | Equal-revision identity excludes legitimate aging without weakening phase, endpoint or rate consistency | `INV-1`, §3.2, §3.3 | DV-12 | T-C05-46, T-C05-54 |
| 2 | Aging formula consistent across producer and consumer obligations | `INV-2`, `TN-P-17`, `TN-C-10`, §3.4 | DV-13 | T-C05-54, T-C05-55 |
| 3 | Equal-revision discard cannot lose a genuine state change | `AD-1`, `TN-P-07`, `TN-C-01`, §3.5 | DV-12 | T-C05-56, T-C05-62 |
| 4 | Simultaneous phase/retime publication is deterministic **and each message's content is fixed** | `C05-2.9` `PO-3`, **`PO-5`**, `TN-P-15`, **`TN-P-18`** | DV-14, **DV-21** | T-C05-51, **T-C05-65** |
| 5 | Multiple phase transitions within one frame are unambiguous | `C05-2.9` `PO-4`, `TN-P-16`, `RS-3` | DV-14 | T-C05-52, T-C05-53 |
| 6 | Directory registration, deregistration, invalidation and liveness compose | `DN-1`, `TN-R-01`, `TN-R-06`, `RM-1`, `TN-P-05`, `TN-P-06` | DV-16 | T-C05-61 |
| 7 | AI, audio, VFX and montage responsibilities have **one owner each** and implementable information paths | §6.1, §6.2, `TN-C-11`, `TN-C-12`, `TN-C-13`, **`TN-C-15`**, §5.2 | DV-17, **DV-22** | T-C05-57 … T-C05-60, **T-C05-67** |
| 8 | `Resynchronised` has an unambiguous normative status | `C05-2.2`, `EN-3`, `TN-C-09`, §6.3 | DV-18 | T-C05-45, T-C05-50, T-C05-57 |
| 9 | All implementer assignments agree with the ownership table **at row granularity** | `C05-7.4`, §7–§9 | **DV-11 (row-level)** | all 43 rows |
| 10 | Every test maps to an obligation and every obligation to one or more tests | §11.2, §12.1 | DV-15 | all 67 cases |
| 11 | Every Agent 2 finding (`D-1`…`D-7`, `C4a`, `C4c`, `C6`, `C9`) is individually traceable to a section | §2 | DV-19 | — |
| 12 | **No C-05 value enters a hit-resolution decision, and `AttackTag` still serves selection** | **`C05-6.4`**, `TN-C-11`, `TN-A-02`, `TN-A-03`, §9.2 | **DV-20** | **T-C05-63** |
| 13 | **A lost retime leaves rate staleness bounded, or explicitly accepted** | `TN-C-14`, `TN-C-10`, `EX-5`(d), §3.6(c) | DV-17 | T-C05-64 |

### 11.2 Obligation → test coverage

| Obligation | Cases | Obligation | Cases |
|---|---|---|---|
| TN-P-01 | T-C05-07 | TN-C-01 | T-C05-02, T-C05-03, T-C05-46, T-C05-56, T-C05-62 |
| TN-P-02 | T-C05-26 | TN-C-02 | T-C05-08, T-C05-09, T-C05-47 |
| TN-P-03 | T-C05-21 | TN-C-03 | T-C05-10, T-C05-11 |
| TN-P-04 | T-C05-22, T-C05-66 | TN-C-04 | T-C05-12, T-C05-13 |
| TN-P-05 | T-C05-23 | TN-C-05 | T-C05-14, T-C05-19, T-C05-44 |
| TN-P-06 | T-C05-24 | TN-C-06 | T-C05-25, T-C05-48 |
| TN-P-07 | T-C05-16, T-C05-62, T-C05-66 | TN-C-07 | T-C05-35 … T-C05-39 |
| TN-P-08 | T-C05-17, T-C05-18, T-C05-19, T-C05-41 | TN-C-08 | T-C05-20, T-C05-50, T-C05-53 |
| TN-P-09 | T-C05-27 | TN-C-09 | T-C05-45, T-C05-50, T-C05-53, T-C05-57 |
| TN-P-10 | T-C05-15 | TN-C-10 | T-C05-54, T-C05-55, T-C05-56, T-C05-64 |
| TN-P-11 | T-C05-06, T-C05-40, T-C05-42, T-C05-65 | TN-C-11 | T-C05-57, T-C05-58, T-C05-63 |
| TN-P-12 | T-C05-01 | TN-C-12 | T-C05-59 |
| TN-P-13 | T-C05-43, T-C05-44, T-C05-45, T-C05-62 | TN-C-13 | T-C05-60 |
| TN-P-18 | T-C05-65 | TN-C-14 | T-C05-64 |
| TN-P-19 | T-C05-66 | TN-C-15 | T-C05-67 |
| TN-P-14 | T-C05-49 | TN-R-01 | T-C05-28, T-C05-29, T-C05-61 |
| TN-P-15 | T-C05-51, T-C05-65 | TN-R-02 | T-C05-04, T-C05-05 |
| TN-P-16 | T-C05-52, T-C05-53 | TN-R-03 | T-C05-30 |
| TN-P-17 | T-C05-54 | TN-R-04 | T-C05-31 |
| TN-R-05 | T-C05-46, T-C05-49 | TN-R-06 | T-C05-61 |
| TN-A-01 | T-C05-32, T-C05-33 | TN-A-02 | T-C05-34, T-C05-63 |
| TN-A-03 | T-C05-63 | — | — |

**43 obligations (19 `TN-P`, 15 `TN-C`, 6 `TN-R`, 3 `TN-A`), every one covered; 67 cases, every one assigned** (verified by DV-15 in both directions).

---

## 12. Acceptance-test catalogue

**67 cases, 18 suites, every case `PROPOSED / NOT RUN`, 0 executed.** No code exists to run them against and no Unreal project exists in this workspace (ADR-0012).

### 12.1 The suites

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
| J | `TDD-Contract.Combat.TelegraphPhaseRevisionAdvancement` | TN-P-13, TN-C-05, TN-C-09, TN-R-05 | 4 | T-C05-43 … 46 |
| K | `TDD-Contract.Combat.TelegraphResyncTerminalAndLateSubscriber` | TN-C-02, TN-C-06, TN-P-14, TN-C-09 | 4 | T-C05-47 … 50 |
| **L** | **`TDD-Contract.Combat.TelegraphSameFramePublicationOrder`** | **TN-P-15, TN-P-16, TN-C-08** | **3** | **T-C05-51 … 53** |
| **M** | **`TDD-Contract.Combat.TelegraphAgingAndObservationInstant`** | **TN-P-17, TN-C-10, TN-C-01** | **3** | **T-C05-54 … 56** |
| **N** | **`TDD-Contract.Combat.TelegraphAttackIdentityResolution`** | **TN-C-09, TN-C-11, TN-C-12, TN-C-13** | **4** | **T-C05-57 … 60** |
| **O** | **`TDD-Contract.Combat.TelegraphDirectoryComposition`** | **TN-R-01, TN-R-06** | **2** | **T-C05-61 … 62** |
| **P** | **`TDD-Contract.Combat.TelegraphHitResolutionBoundary`** | **TN-A-02, TN-A-03, TN-C-11** | **1** | **T-C05-63** |
| **Q** | **`TDD-Contract.Combat.TelegraphLostRetimeStaleness`** | **TN-C-10, TN-C-14, TN-P-15** | **2** | **T-C05-64 … 65** |
| **R** | **`TDD-Contract.Combat.TelegraphIdentityAndCueOwnership`** | **TN-P-19, TN-P-07, TN-P-04, TN-C-15** | **2** | **T-C05-66 … 67** |

### 12.2 The cases added or rewritten by this revision, specified

S3 added or rewrote twelve (`T-C05-51` … `T-C05-62`). **S4 adds five (`T-C05-63` … `T-C05-67`) and rewrites `T-C05-51` and `T-C05-62`.** All seventeen are specified here, because a reader of S4 should not have to open S3 to know what a case asserts. All are `PROPOSED / NOT RUN`.

| Case | Setup | Assertion |
|---|---|---|
| **T-C05-51** `[REWRITTEN: D-2]` | A frame contains one phase transition (Windup→Active) and two dilation changes; a pull is taken **between** the first and second publications; consumer holds `n` | the message sequence is exactly `PhaseChanged`@`n+1`, `Retimed`@`n+2`, `Retimed`@`n+3` — phase first, retimes in applied order, no coalescing, no shared revision; **the `ProducerRate` carried by each of the three messages is asserted individually**, not just their order; the mid-frame pull returns the `n+1` `VF` exactly (`PO-5`, `TN-P-18`); the consumer adopts all three contiguously, fires entry once, records no gap |
| **T-C05-52** `[NEW: C3]` | Two phase transitions in one frame (montage section boundary pair); consumer holds `n` | two `PhaseChanged` messages at `n+1` (Active) and `n+2` (Recovery), authored order, neither collapsed; the consumer fires entry once for Active and once for Recovery and records no gap |
| **T-C05-53** `[NEW: C3]` | Same producer, consumer receives only the second message (`n+2`) | `n+2 > n+1` → gap; no entry for the unobserved Active; exactly one `FTDDTelegraphResynchronisation` landing in Recovery; a subsequent pull returns Recovery at `n+2` and never the intermediate phase (`RS-3`, `TN-C-08`) |
| **T-C05-54** `[NEW: C4a]` | Two pulls at the same revision, Δ axis apart, no producer change | identical `VF` on both (phase, three endpoints, `ProducerRate`, `WindowKey`, `AttackTag`); `AxisNow` differs by Δ; `RemainingLocalSeconds` differs by exactly Δ × `ProducerRate`; both satisfy `INV-2`, and the second equals `R(t) = max(0, R0 − (Axis(t) − AxisNow) × ProducerRate)` evaluated from the first (`TN-P-17`, `TN-C-10`) |
| **T-C05-55** `[NEW: C4a]` | Aging past the end of the phase, and across a pause | `RemainingLocalSeconds` reaches 0 at `Axis(t) − AxisNow = R0 / ProducerRate`, is clamped at 0 and never negative; across a pause the axis does not advance and neither does `R`; a wall-clock-aging consumer diverges and is the negative control |
| **T-C05-56** `[NEW: C4a]` | Consumer at `n` discards an equal-revision pull, then receives `n+1` with a changed endpoint | the discarding consumer's `VF` state after adopting `n+1` equals that of a consumer that never discarded; the discarded observation's only difference was `OF`; a fixture in which the equal-revision pull carries a `VF` change is rejected as a producer violation, not silently adopted |
| **T-C05-57** `[NEW: C6, C5]` | Consumer resyncs into Active across a gap, `AttackTag` = unblockable | exactly one `FTDDTelegraphResynchronisation` carrying the landed snapshot; the consumer reads `WindowKey` and `AttackTag` from that snapshot and selects dodge rather than block with no second lookup; the delegate fires once and is not re-raised for the same gap |
| **T-C05-58** `[NEW: C6]` | Two attacks with different `WindowKey` and different `AttackTag` reach the audio consumer | the phase transition alone (snapshot identity included) selects two different cue ids; no additional query is issued; a consumer that instead derives identity from `SourceEntityId` fails the assertion |
| **T-C05-59** `[NEW: C7]` | A VFX marker consumes the telegraph for one attack | the marker starts and stops on phase transitions from C-05 timing only; its world placement is resolved from `SourceEntityId` through the owning actor; no contract type carries a transform, position, socket or attach point (compile-time and structural assertion) |
| **T-C05-60** `[NEW: C8]` | A montage consumer observes a phase transition, then a retime | the phase transition raises exactly one montage switch request carrying `WindowKey`; the asset is resolved from attack data keyed by `WindowKey`, outside C-05; the retime raises **no** switch request; no asset reference appears in any contract type |
| **T-C05-61** `[NEW: C1, C2]` | Five producer fates: natural close, cancellation, stream-out with no graceful close, producer death, world teardown | each deregisters the association; `TryGetOpenTelegraph` and the resolution helper answer `false` in every case; no entry survives teardown; the directory emits nothing, orders nothing and defers nothing throughout (`TN-R-01`, `TN-R-06`) |
| **T-C05-62** `[REWRITTEN: D-3]` | The complete change table — open, phase transition, retime, close, plus pure `OF` drift — **and, as the negative control, a producer that attempts a mid-instance `WindowKey` change** | every legal `VF` change arrives with a revision bump (`TN-P-07`, `TN-P-13`); pure `OF` drift arrives with no bump and triggers no diagnosis; **the attempted identity change is rejected as a producer violation** and the consumer treats the instance as ended rather than adopting the new key (`TN-P-19`, T-C05-66) |
| **T-C05-63** `[NEW: conflict; rewritten at S4.2: Agent 3 finding 6, TD item 5]` | **Three conditions combined in one scenario**, not three separate variants: (1) the consumer **already holds** a snapshot of the instance that it took for **selection** (it has read `AttackTag` from it, as `TN-C-11` allows); (2) that held snapshot's `AttackTag` is **adversarially altered** in place — `blockable` → `unblockable`, and the reverse in the paired run — with no new source call, so no surface spy can see the change; (3) a **hit-resolution attempt** is then made against the same incoming hit. | **The hit outcome is byte-identical across the pair** — decided by `C05-6.1`'s same-frame phase overlap and the defender's live state, never by the held tag — and **no tag-derived value reaches the hit resolver**: the assertion is made on the resolver's **input/use path** with a tainted-value (dataflow) instrument that marks the tag at the selection call site and fails if any tainted value is observed by the resolver, so a cached read cannot hide behind the absence of a surface call. **Separately asserted, as required:** the selection call site **does** consume the tag — the AI selects dodge on `unblockable` and block on `blockable` — and the two call sites are shown to be distinct code paths (`C05-6.4`; `TN-A-02`, `TN-A-03`). |
| **T-C05-64** `[NEW at S4; extended at S4.2: Agent 3 finding 4, `D-1a`, `D-1b`, TD item 2]` | A frame with one phase transition and one dilation change; the `Retimed` at `n+2` is **dropped**. **Three schedules and two negative controls:** **(s1) nominal** — the consumer's frame-start pull succeeds, then it uses the value later in the frame. **(s2) Agent 3's counterexample, stated exactly** — the pull happens at the **first instant of frame *k***, the `Retimed` is published **immediately after that pull**, the consumer takes **no further pull in frame *k***, its next pull lands at the **last instant of frame *k+1***, and it performs a timing-dependent **use late in frame *k+1* before that pull**. **(s3) the worst-case permitted placement** — the pull lands at the **first instant of a frame**, the `Retimed` is published **one tick later in that same frame**, and the use happens at the **last instant of that frame** (the latest placement `TN-C-14` permits). **Negative controls:** (n1) a consumer that carries a frame-*k* value into frame *k+1*; (n2) a consumer whose pull fails and which acts anyway instead of re-pulling or suppressing. | **(s1)** staleness ≤ one frame; the next successful refresh adopts `n+2`; the aged remaining time matches a consumer that received both messages. **(s2) the conforming schedule fails the obligation as S4.1 stated it and passes as S4.2 states it:** the frame-*k+1* use has no observation whose `AxisNow` lies in frame *k+1*, so `TN-C-14`(ii) and (iv) require a **re-pull before that use**; with the re-pull the aged value equals (s1), and the total staleness never reaches the "almost two frames" the old rule permitted. **(s3)** the age is asserted in the **stated measure** — axis units from the missed revision's publication to the use — and must be **strictly less than one frame**, which is the bound's supremum. **(n1)** must be reported as a violation, not a slow refresh. **(n2)** must be reported as a violation; a consumer that suppresses the action instead **passes**. **Message-only consumer, unchanged:** stale by exactly the retime ratio, with **no gap, no resync and no diagnostic** — the accepted residual (`EX-5` case (d), `TN-C-14`(v)). |
| **T-C05-65** `[NEW: D-2]` | A frame where the producer transitions Windup→Active and then dilates, with a pull taken after each application | the pull after the transition returns Active at the **old** `ProducerRate` under `n+1`; the pull after the dilation returns Active at the **new** rate under `n+2`; **at no instant does a pull return `VF` content the current revision does not cover** (`INV-1`, `TN-P-11`, `TN-P-18`); a negative-control producer that batches both changes before publishing fails on the first pull |
| **T-C05-66** `[NEW: D-3]` | An attack identity change mid-fight: the producer is asked to substitute a different `WindowKey` for an open instance | the producer publishes `Closed` (`Cancelled`) for the old instance with no revision advance, then `Opened` for a new instance with a new `AttackInstanceId` at revision 1; the consumer's baseline for the new instance suppresses an entry for its opening phase (`EN-1`); the identity value never changes inside an instance (`TN-P-19`); a producer that emits a higher revision carrying the new key is a **failure**, not a variance (`TN-P-07`) |
| **T-C05-67** `[NEW: D-4]` | An audio consumer observes a phase transition, then a retime, on the same instance | the phase transition raises **exactly one** cue-selection request carrying `Phase`, `WindowKey` and `AttackTag` from the adopted snapshot; the retime raises **none** (`TN-C-15`); the cue asset is resolved from audio data keyed by those fields, outside C-05; the *only* implementer of this obligation in the ownership table is Agent 2, row 6 (`C05-7.2`, DV-11) |

**T-C05-46 is rewritten** (Agent 2's C4b): it asserts **versioned-field** identity across two pulls and one duplicated message at rev 3, plus `INV-2` consistency of each `OF` pair — it no longer demands byte-identical `RemainingLocalSeconds`, which no conforming producer could deliver.

### 12.3 Complete case catalogue

`Status` is `PROPOSED / NOT RUN` for every row without exception; the column is repeated rather than stated once because this catalogue is the artefact Agent 2 asked to be complete.

| Case | Suite | Obligation(s) | Intent | Status |
|---|---|---|---|---|
| T-C05-01 | A | TN-P-12 | deterministic fixture: identical inputs, identical sequence | `PROPOSED / NOT RUN` |
| T-C05-02 | A | TN-C-01 | equal revision discarded | `PROPOSED / NOT RUN` |
| T-C05-03 | A | TN-C-01 | lower revision discarded, consumer never moves backwards | `PROPOSED / NOT RUN` |
| T-C05-04 | A | TN-R-02 | `false` for a closed instance | `PROPOSED / NOT RUN` |
| T-C05-05 | A | TN-R-02 | `false` for an instance never opened | `PROPOSED / NOT RUN` |
| T-C05-06 | A | TN-P-11 | pull answers from live state at call time | `PROPOSED / NOT RUN` |
| T-C05-07 | B | TN-P-01 | `Opened` precedes every other message | `PROPOSED / NOT RUN` |
| T-C05-08 | B | TN-C-02 | baseline fires no entry | `PROPOSED / NOT RUN` |
| T-C05-09 | B | TN-C-02 | pull-derived baseline and `Opened` baseline are the same case | `PROPOSED / NOT RUN` |
| T-C05-10 | B | TN-C-03 | entry at most once per phase | `PROPOSED / NOT RUN` |
| T-C05-11 | B | TN-C-03 | duplicate `PhaseChanged` fires nothing; retime re-fires nothing | `PROPOSED / NOT RUN` |
| T-C05-12 | C | TN-C-04 | gap flagged on `incoming > held + 1` | `PROPOSED / NOT RUN` |
| T-C05-13 | C | TN-C-04 | gap flag persists until close | `PROPOSED / NOT RUN` |
| T-C05-14 | C | TN-C-05 | a single pull recovers, never an iteration | `PROPOSED / NOT RUN` |
| T-C05-15 | C | TN-P-10 | axis domain, not wall clock or frame count | `PROPOSED / NOT RUN` |
| T-C05-16 | C | TN-P-07 | revision monotone on every versioned change | `PROPOSED / NOT RUN` |
| T-C05-17 | D | TN-P-08 | one `Retimed` per dilation boundary, no batching | `PROPOSED / NOT RUN` |
| T-C05-18 | D | TN-P-08 | hitstop boundaries are not exempt | `PROPOSED / NOT RUN` |
| T-C05-19 | D | TN-P-08, TN-C-05 | burst then recovery, no coalescing | `PROPOSED / NOT RUN` |
| T-C05-20 | D | TN-C-08 | a pull is not history | `PROPOSED / NOT RUN` |
| T-C05-21 | E | TN-P-03 | exactly one `Closed`, terminal | `PROPOSED / NOT RUN` |
| T-C05-22 | E | TN-P-04 | every cancellation path closes | `PROPOSED / NOT RUN` |
| T-C05-23 | E | TN-P-05 | teardown invalidates before the producer dies | `PROPOSED / NOT RUN` |
| T-C05-24 | E | TN-P-06 | stream-out scoped to its own instances | `PROPOSED / NOT RUN` |
| T-C05-25 | E | TN-C-06 | removal is closure, not an error | `PROPOSED / NOT RUN` |
| T-C05-26 | E | TN-P-02 | ids never reused | `PROPOSED / NOT RUN` |
| T-C05-27 | E | TN-P-09 | no message for a closed or never-opened instance | `PROPOSED / NOT RUN` |
| T-C05-28 | F | TN-R-01 | registration precedes resolution | `PROPOSED / NOT RUN` |
| T-C05-29 | F | TN-R-01 | expired handle answers `false` | `PROPOSED / NOT RUN` |
| T-C05-30 | F | TN-R-03 | per-producer ids only, never aggregated | `PROPOSED / NOT RUN` |
| T-C05-31 | F | TN-R-04 | value copy, no re-entrancy, no visible mutation | `PROPOSED / NOT RUN` |
| T-C05-32 | G | TN-A-01 | parry from live phase, not from C-05 | `PROPOSED / NOT RUN` |
| T-C05-33 | G | TN-A-01 | corrupted timing block does not change the parry result | `PROPOSED / NOT RUN` |
| T-C05-34 | G | TN-A-02 | spy shows no telegraph read on the arbitration path | `PROPOSED / NOT RUN` |
| T-C05-35 … 39 | H | TN-C-07 | `Dead > Cinematic > Staggered`, priority order, carriers never compared | `PROPOSED / NOT RUN` |
| T-C05-40 | I | TN-P-11, TN-P-08 | message and pull agree within one frame | `PROPOSED / NOT RUN` |
| T-C05-41 | I | TN-P-08 | two boundaries in one frame are two revisions | `PROPOSED / NOT RUN` |
| T-C05-42 | I | TN-P-11 | pull never returns an older revision than the last message | `PROPOSED / NOT RUN` |
| T-C05-43 | J | TN-P-13 | phase-only transition advances the revision by one | `PROPOSED / NOT RUN` |
| T-C05-44 | J | TN-P-13, TN-C-05 | dropped `PhaseChanged` recovered by one pull, contiguous, entry fires | `PROPOSED / NOT RUN` |
| T-C05-45 | J | TN-P-13, TN-C-09 | two transitions missed: gap, no entry, one resynchronisation | `PROPOSED / NOT RUN` |
| T-C05-46 | J | TN-C-01, TN-R-05 | **rewritten:** versioned-field identity at one revision, `INV-2` consistency of the `OF` pairs | `PROPOSED / NOT RUN` |
| T-C05-47 | K | TN-C-02 | late subscriber baseline mid-phase, no entry | `PROPOSED / NOT RUN` |
| T-C05-48 | K | TN-C-06 | `Closed` at an equal revision still closes (`TM-1`) | `PROPOSED / NOT RUN` |
| T-C05-49 | K | TN-P-14, TN-R-05 | complete payload on all four message kinds | `PROPOSED / NOT RUN` |
| T-C05-50 | K | TN-C-09, TN-C-08 | one resynchronisation per gap, none afterwards | `PROPOSED / NOT RUN` |
| T-C05-51 | L | TN-P-15 | same-frame phase + retimes: canonical order, no shared revision | `PROPOSED / NOT RUN` |
| T-C05-52 | L | TN-P-16 | two transitions in one frame: two messages, two revisions | `PROPOSED / NOT RUN` |
| T-C05-53 | L | TN-P-16, TN-C-09, TN-C-08 | receiving only the second transition: gap, resync, no fabricated entry | `PROPOSED / NOT RUN` |
| T-C05-54 | M | TN-P-17, TN-C-10 | `VF` identical, `OF` ages by exactly Δ × rate, `INV-2` holds | `PROPOSED / NOT RUN` |
| T-C05-55 | M | TN-C-10 | clamp at zero, pause freezes, wall-clock negative control | `PROPOSED / NOT RUN` |
| T-C05-56 | M | TN-C-01, TN-C-10 | discard-then-age is observationally equivalent | `PROPOSED / NOT RUN` |
| T-C05-57 | N | TN-C-09, TN-C-11 | resync into Active is actionable: blockability from `AttackTag` | `PROPOSED / NOT RUN` |
| T-C05-58 | N | TN-C-11 | audio cue selected from identity carried in the snapshot | `PROPOSED / NOT RUN` |
| T-C05-59 | N | TN-C-12 | VFX timing from C-05, placement from `SourceEntityId`, no transform in any type | `PROPOSED / NOT RUN` |
| T-C05-60 | N | TN-C-13 | montage trigger + key from C-05, asset from attack data, retime is not a trigger | `PROPOSED / NOT RUN` |
| T-C05-61 | O | TN-R-01, TN-R-06 | five producer fates compose; directory schedules and emits nothing | `PROPOSED / NOT RUN` |
| T-C05-62 | O | TN-P-07, TN-P-13, TN-C-01 | complete change table: every `VF` change bumps, `OF` drift never does; a mid-instance identity change is rejected (`TN-P-19`) | `PROPOSED / NOT RUN` |
| T-C05-63 | P | TN-A-02, TN-A-03, TN-C-11 | held selection snapshot + adversarially altered `AttackTag` + hit-resolution attempt: outcome identical, no tag-derived value observed by the resolver (dataflow instrument), selection still uses the tag | `PROPOSED / NOT RUN` |
| T-C05-64 | Q | TN-C-10, TN-C-14 | lost `Retimed`: nominal, A3's just-after-poll counterexample, worst-case permitted placement; bound measured in axis units and strictly below one frame; carry-over and act-on-failure controls fail; message-only residual accepted | `PROPOSED / NOT RUN` |
| T-C05-65 | Q | TN-P-18, TN-P-11 | mid-frame pulls return the current revision's `VF` exactly; a batching producer fails | `PROPOSED / NOT RUN` |
| T-C05-66 | R | TN-P-19, TN-P-07, TN-P-04 | identity change closes and reopens with a new id at revision 1; never a mid-instance revision | `PROPOSED / NOT RUN` |
| T-C05-67 | R | TN-C-15 | audio cue on the phase transition only, identity-keyed, never on a retime; single owner | `PROPOSED / NOT RUN` |

**67 cases, 0 executed.** Case rows `T-C05-35 … 39` are grouped because the suite distinguishes them by carrier and priority order, not by obligation; DV-2 range-expands them so the count is 67, not 63.

### 12.4 What this catalogue is not

It is not evidence that any obligation holds, that any suite compiles, or that the contract behaves as written. **Acceptance tests executed: 0 — not by me, not by Agent 2, not by Agent 3, in this workspace or any other I can see.** Written against Agent 1 code: 0. Engine available: none (ADR-0012). The document checks in §13 are the only executed evidence in this document, and they are statements about text.

---

## 13. Document validation — executed

Twenty-seven checks on **this document's text**, run with `python3` over the file. They are not tests of contract behaviour, and passing them says nothing about whether any obligation holds. Every result below is the actual output of the check listed. **The checker is now in the repository** — `docs/validation/dv_c05.py` — so a reviewer can re-run it instead of trusting this table, which is itself a correction: S4.1 recorded the checker at `/home/user/dv4.py`, outside the repository, where no reviewer could reach it.

Command for all checks:

```
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md
```

### 13.1 The twenty-seven checks and their actual output

| Check | Method | Result |
|---|---|---|
| **DV-1** | extract every obligation id from §§7–9, dedupe, compare with the declared sets (19 P, 15 C, 6 R, 3 A) | **PASS** — 43 obligation rows; P19 C15 R6 A3 |
| **DV-2** | extract `T-C05-nn`, range-expand `T-C05-35 … 39`, compare with `01…67` | **PASS** — 67 distinct case ids; missing []; extra [] |
| **DV-3** | every obligation row has exactly 7 cells with non-empty requirement and implementer cells | **PASS** — 43 rows, 7 cells each, implementer non-empty; bad [] |
| **DV-4** | count occurrences of the withdrawn ownership claim; must be 0 | **PASS** — 0 occurrences of the withdrawn ownership claim |
| **DV-5** | every `C05-x.y` reference resolves to a §4 heading or a §4.10 row | **PASS** — 15 referenced, 15 defined, unresolved [] |
| **DV-6** | count suite rows, sum the `Cases` column, compare with the stated totals | **PASS** — 18 suites, case sum 67 |
| **DV-7** | `TD-06`, `TD-09`, `TD-12` appear in §14 with status `OPEN` | **PASS** — TD-06, TD-09, TD-12 present in §14, each still OPEN |
| **DV-8** | enumerate every line containing `execut`; each must concern a document check or be negated; `0 executed` present | **PASS** — 9 lines contain 'execut'; every one concerns a document check or is negated; '0 executed' present |
| **DV-9** | every line containing `TDDCore` also names a MEAD | **PASS** — 2 lines mention TDDCore, all MEAD-qualified |
| **DV-10** | every table block has a constant cell count per row | **PASS** — 39 tables, 0 malformed rows |
| **DV-11** | parse §5.4's token table **with its row mapping**; for each obligation, test the token's row against the prefix's allowed-row set (`TN-P`→{2}, `TN-C`→{5,6}, `TN-R`→{2,4}, `TN-A`→{8}); report declared and observed separately | **PASS** — 7 declared / 5 observed tokens, 43 cells; declared-unused ['Agent 2, in its own systems', 'contract layer, owner pending TD-12']; failures [] |
| **DV-12** | extract the `VF` set from `INV-1`, §3.2 and the §4.2 struct; require set equality; the old equality phrase must not survive | **PASS** — VF homes equal: §3.2=7 INV-1=7 struct=7; sets equal True; old equality phrase occurrences 0 |
| **DV-13** | the `R(t)` form in `INV-2`/`TN-C-10`/`T-C05-54`; the endpoint form in `INV-2`; the one-revision precondition stated in the clause | **PASS** — R(t) form in INV-2/TN-C-10/T-C05-54: [True, True, True]; endpoint form in INV-2 True; one-revision precondition stated True |
| **DV-14** | `PO-3` names the phase→retime order at `n+1`/`n+2`; `PO-5` present; `EX-5` carries (a)(b)(c)(d) and (cʹ)(e); `TN-P-15` names the canonical order | **PASS** — PO-3 order phase→retime n+1→n+2 True; PO-5 present True; EX-5 cases (a)(b)(c)(d) True, (cʹ)(e) True; TN-P-15 canonical True |
| **DV-15** | every obligation appears in §11.2 with ≥1 case; inverting §11.2 covers every case id `01…67` | **PASS** — 43 obligations mapped; cases covered 67; missing obligations []; missing cases [] |
| **DV-16** | `DN-1` carries `whichever occurs first`, `Closed`, `invalidation`; `TN-R-06` forbids timing, scheduling and emission | **PASS** — DN-1 carries all three trigger strings; TN-R-06 forbids timing, scheduling and emission |
| **DV-17** | §6.1 names AI, audio, montage and VFX with a verdict each; §6.2 has the VFX-placement and montage-asset rows; audio names one owner | **PASS** — 4 consumer rows with verdicts; §6.2 VFX+montage rows True; audio single owner stated True |
| **DV-18** | `FTDDTelegraphResynchronisation` declared in §4.2 and referenced by `EN-3`, `TN-C-09`, §6.3 | **PASS** — struct in §4.2; referenced by EN-3, TN-C-09 and §6.3 |
| **DV-19** | §2 carries rows for `D-1`…`D-7` and for `C4a-1`, `C4a-2`, `C4c-1`, `C4c-2`, `C6-1`, `C6-2`, `C9` | **PASS** — 7 defect rows + 7 condition rows in §2; all present True |
| **DV-20** | three domains in §9.2; `TN-C-11` selection-only; `TN-A-02` names `AttackTag`; `TN-A-03` exists; **§5.2 row 5 excludes the hit outcome and names row 8 / `TN-A-01`**; **`T-C05-63` combines held snapshot + altered tag + input/use instrumentation + a separate selection assertion** | **PASS** — three domains in §9.2 True; TN-C-11 selection-only True; TN-A-02 names AttackTag True; TN-A-03 present True; row 5 excludes the outcome True; T-C05-63 combines held snapshot + altered tag + dataflow instrumentation True; separate selection assertion True |
| **DV-21** | the `PO-5` content rule appears in §3.6, §4.9, `TN-P-18` and `EX-11` | **PASS** — content rule present in 4/4 places {'§3.6': True, '§4.9': True, 'TN-P-18': True, 'EX-11': True}; interleaving stated |
| **DV-22** | row 5 clean of audio; row 6 owns cue selection; `TN-C-15` implementer; **§8 preamble clean**; **whole-document scan: no line pairs audio with Agent 1 outside a marked correction or quotation** | **PASS** — row 5 audio removed True; row 6 owns audio True; TN-C-15 present True, implementer Agent 2, C-05 consumer; §8 preamble clean True; whole-document scan offenders 0 [] |
| **DV-23** | normative sections use "fixed for the instance's lifetime"; the rejected phrase appears only inside quotation marks; `TN-P-19`, `TN-P-04`, T-C05-66 present | **PASS** — identity 'fixed for the instance's lifetime' in normative sections 7; unquoted rejected phrase 0; TN-P-19 present; TN-P-04 names identity change; T-C05-66 present |
| **DV-24** | extract the declared/observed pair stated in §1 row 6, §5.4, §13.1's DV-11 row and §18.1, and require every site to equal `DV-11`'s computed pair | **PASS** — computed 7 declared / 5 observed; stated at 3 sites {'§1 row 6': (7, 5), '§5.4': (7, 5), '§13.1 DV-11': (7, 5)}; consistent True |
| **DV-25** | `TN-C-14` carries call-site scope, the one-frame maximum interval, the shared-axis measure, the frame-of-use refresh, re-pull-or-suppress, the derived bound and the message-only residual; `T-C05-64` carries A3's schedule, the worst-case placement, the measure assertion and the negative controls | **PASS** — TN-C-14 rules 7/7, missing []; T-C05-64 extensions 4/4, missing [] |
| **DV-26** | §3.6 does not assert the falsified premise; it states that the order **is** observable through a mid-frame pull; `PO-3` and `PO-5` both retained | **PASS** — falsified premise absent True; 'observable through a mid-frame pull' present True; PO-3 and PO-5 both retained True |
| **DV-27** | no placeholder token anywhere in the file; §17 records S4.1's exact commit and blob; the provenance register is referenced in §17 and §18 | **PASS** — placeholders found []; S4.1 commit+blob recorded in §17 True; provenance register referenced in §17 and §18 True |

**27/27 PASS.**

### 13.2 DV-11 is still shown failing, on the blob it was built for

The S3 demonstration stands, unchanged: `DV-11` must fail on the S3 blob or it proves nothing.

```
$ git show a6b4e22:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md > /tmp/s3.md
$ python3 docs/validation/dv_c05.py /tmp/s3.md
DV-11 FAIL — 6 declared / 5 observed tokens, 38 cells; declared-unused
  ['contract layer, owner pending TD-12']; failures
  ["TN-C-12: token 'Agent 2, in its own systems' maps to rows [7], allowed for TN-C are [5, 6]",
   "TN-C-13: token 'Agent 2, in its own systems' maps to rows [7], allowed for TN-C are [5, 6]"]
...
10/27 checks passed
```

### 13.3 Every instrument S4.2 adds or widens is shown failing on the blob the reviews pinned

This is the reconciliation the TD asked for, and it is the only form of it that means anything: **each check must fail on the text that contains the defect, and pass on the text that removes it.** The reviewed blob is `d54e194affeaee98b1030e2b83b4c34e234fa382` (commit `9591826`); S4.0's is `424d2c69…` (commit `4692e97`).

| Instrument | Built for | On the blob where the defect exists | On this file |
|---|---|---|---|
| **DV-11** | row-level token→row mapping | **FAIL on S3** `a6b4e22` — names `TN-C-12` and `TN-C-13` mapped to row 7 against allowed {5, 6} | PASS |
| **DV-20** (widened) | row 5 must exclude the hit outcome; T-C05-63 must combine held snapshot, altered tag and input/use instrumentation | **FAIL on S4.1** — `row 5 excludes the outcome False; T-C05-63 … False; separate selection assertion False` | PASS |
| **DV-22** (widened) | audio has exactly one owner **in all ownership prose**, §8's preamble included | **FAIL on S4.1** — `§8 preamble clean False`; **FAIL on S3** with two offenders, including row 5's old "camera and audio cues" | PASS |
| **DV-24** (new) | every hand-restated declared/observed count equals `DV-11`'s computed pair | **FAIL on S4.0** — `stated at 4 sites {'§1 row 6': (7, 6), '§5.4': (7, 5), '§13.1 DV-11': (7, 5), '§18.1 C9': (7, 5)}; consistent False` | PASS |
| **DV-25** (new) | the staleness bound is defined, measurable and derived | **FAIL on S4.1** — `TN-C-14 rules 0/7; T-C05-64 extensions 0/4` | PASS |
| **DV-26** (new) | `PO-3`'s rationale must not assert a premise `PO-5` falsifies | **FAIL on S4.1** — `falsified premise absent False; 'observable through a mid-frame pull' present False` | PASS |
| **DV-27** (new) | no unfilled commit/blob placeholder; S4.1's exact values recorded; register referenced | **FAIL on both** — the checker reports placeholder fields present in each reviewed blob (verbatim output below the table) | PASS |

**The DV-27 failures, verbatim** — quoted in a fenced block, which `DV-27` strips before scanning, so an instrument's own output can neither satisfy nor trip its check:

```
$ python3 docs/validation/dv_c05.py /tmp/s41.md
DV-27 FAIL — placeholders found ['S41_COMMIT', 'S41_BLOB']; S4.1 commit+blob recorded in §17 False;
             provenance register referenced in §17 and §18 False

$ python3 docs/validation/dv_c05.py /tmp/s40.md
DV-27 FAIL — placeholders found ['PUB_COMMIT_PLACEHOLDER', 'PUB_BLOB_PLACEHOLDER', '_PLACEHOLDER']; ...
```

**Full tallies of the same checker on the four blobs:** S4.2 **27/27**, S4.1 **22/27**, S4.0 **21/27**, S3 **10/27**. The S4.1 and S4.0 tallies are lower precisely because those documents lack the five corrections made here — not because the checker was tuned to this file: **the failing checks are the ones the two reviews named, in the order they named them.**

### 13.4 What this section proves, and what it does not

**It proves that the text is internally consistent, and that the seven instruments reach the defects they were built for.** It does not prove the contract is correct, implementable or agreed, and **no acceptance test has been run**: 67 cases are `PROPOSED / NOT RUN`, **0 executed** — not by me, not by Agent 2, not by Agent 3, in this work or in any predecessor. The one thing `DV-25` cannot do is prove that a consumer honours `TN-C-14`; that is `T-C05-64`'s job, and it has not run.

---

## 14. Dependencies and blockers

### 14.1 External blockers — unchanged, and not resolved by this revision

| ID | Dependency | Blocks | Status |
|---|---|---|---|
| **B-1** | **TD-06** — clock ownership and the shared axis | any code that stamps or ages timing | **OPEN** — TD |
| **B-2** | **TD-09** — parry-authority location and the MEAD-C/MEAD-A erratum | implementing the arbitration path | **OPEN** — TD |
| **B-3** | No engine, compiler or project in this workspace (ADR-0012) | executing any of the 67 cases | **OPEN** — Phase 0 |
| **B-4** | **TD-12** — canonical MEAD and the contract-layer owner | freezing the value types, the resynchronisation type and the read interface | **OPEN** — TD |
| **B-5** | U-07 / global enumeration (X-1 only) | nothing in C-05 | **OPEN**, conditional |
| **B-6** | U-15 damage-request spelling | C-03 only | **OPEN** — TD |
| **B-7** | U-14 `Status.Dead` grant | C-04 only | **OPEN** — registry |
| **B-8** | TD-13 save inventory | C-07 only | **OPEN** — Agent 3 |

### 14.2 Dependencies this revision makes visible

| ID | Dependency | Why it is visible now | Status |
|---|---|---|---|
| **B-9** | Agent 2's re-review of **this exact blob** | their seven defects and seven conditions are addressed one by one in §2; consistency is not agreement, and two resolutions differ from their recommendation (`D-1`, `D-3`) and must be adjudicated | **OPEN** — requested in §18.1 |
| **B-10** | Agent 3's reassessment of S2 **and** S3 | neither document exists at `arena/c64fc525-tdd` (§0.2), so no A3 finding against S2 or S3 is known to be closed | **OPEN** — requested in §18.2 |
| **B-11** | `C05-6.3`'s three carriers are stated in full only in `A1-C05-S1` §6.3, and the clause is proposed rather than frozen and coupled to `C-04-4` | Agent 2's §5.4; it makes `TN-C-07` inherit both statuses | **`BLOCKED BY DEPENDENCY`** — the decision required is C-04's (`C-04-4` plus the registry's `Status.Dead` grant, B-7). `TN-C-07` remains implementable only once that decision exists; nothing else in C-05 depends on it |
| **B-12** | Cross-agent routing of the resynchronisation signal | the type is declared and normative, but delivery is consumer-local; routing it would need the contract layer's owner (TD-12) and a transport C-05 refuses | **OPEN, not proposed** |
| **B-13** | Ownership and registration of the `AttackTag` values | C-05 transports a tag value and defines/registers nothing; with no tag authored the field is empty and behaviour is unchanged | **OPEN** — registry/TD, non-blocking |
| **B-14** | Float comparison tolerance for `INV-2` assertions | `T-C05-54`/`T-C05-55` compare derived values; the tolerance is a test-fixture decision, not a contract one | **OPEN** — implementation-time, non-blocking |
| **B-15** | **Agent 3's S3 review is not in the repository**, so the `TN-C-11` / `TN-A-01`-`02` conflict was resolved from its own terms rather than from their proposed wording | §0.2 and §9.2: **no sentence of S4 is attributed to Agent 3.** If their wording differs materially, §9.2, `TN-C-11`, `TN-A-03` and T-C05-63 are the sections that need re-cutting; nothing else depends on the resolution | **OPEN** — this is the one closure in S4 that is S4's own, not a reviewer's |

**No status in §14.1 has changed since S1.** This revision claims no closure of TD-06, TD-09, TD-12, U-07, C-05 or any registry item. One dependency (B-11) is marked **`BLOCKED BY DEPENDENCY`** rather than resolved, per the instruction's stop condition: the correction it touches cannot be completed without a C-04 decision that is not mine to make, and every other correction proceeded independently of it.

---

## 15. What changed, defect by defect, and what each reviewer should now test

S3's §15 tried to predict how Agent 2's verdicts should move. **That framing is dropped**, because Agent 2 has now reviewed S3 and returned verdicts of their own: predicting them again would be arguing with a review I have already read. This section states, per finding, what changed and **what a reviewer could falsify** — and it names the two places where S4 knowingly departs from Agent 2's recommendation rather than pretending the departure is agreement.

| Finding | What S4 changed | What a reviewer should test | If the test fails |
|---|---|---|---|
| **D-1** | `EX-5` case (d); `TN-C-14` (one pull per frame for timing-dependent consumers); §3.6 rationale (c) corrected; `TN-C-10` limited to the held revision | that one frame is a defensible bound for a consumer that acts on remaining time, **and** that stating the message-only residual is acceptable in place of eliminating it | if one frame is too coarse, `TN-C-14`'s period is the number to change and nothing else moves |
| **D-2** | `PO-5` in §3.6 and §4.9; `TN-P-18`; T-C05-51 extended; `EX-11`; T-C05-65 | that "publish between applications" is implementable on Agent 2's producers without an extra allocation or a second update pass | if it is not, the alternative is Agent 2's reading A plus a weakened `TN-P-11`, which reopens `INV-1` — that is why the obligation is on publication, not on storage |
| **D-3** | constancy kept, change path named (`TN-P-19`, `TN-P-04`, `EX-12`, T-C05-66); `TN-P-07`'s identity clause removed; `T-C05-62` identity rows replaced | whether close-and-reopen is *actually* how an identity change would be expressed in Agents 1/2's montage-driven attacks, or whether some real case needs identity to vary inside one instance | if a real case exists, the instance boundary is in the wrong place and `TN-P-19` is wrong — not just the wording |
| **D-4** | row 5 loses audio; row 6 keeps it; `TN-C-15` added; T-C05-67 | that no other row or clause still implies Agent 1 owns a cue | if another assignment survives, `DV-22` was scoped too narrowly **This risk materialised:** Agent 2 (`§4.4`) and Agent 3 (finding 5) both found §8's preamble still assigned audio to Agent 1 while `DV-22` passed it — exactly the "scoped too narrowly" case this column predicted. Closed at S4.2 in §8 and in DV-22 (§13.1), with DV-22 now shown failing on the reviewed blob (§13.3). |
| **D-5** | token `Agent 2, C-05 consumer` → row 6; `TN-C-12`/`TN-C-13` re-mapped | that the token split matches how Agent 2's code is actually organised | if row 6 and row 7 are the same code in practice, the split is cosmetic and the *ownership* claim, not the token, is what needs the TD's eye |
| **D-6** | row-level `DV-11` with per-prefix allowed sets; declared/observed reported separately; **the failure on S3's blob is shown in §13.2** | that the allowed-row sets are right — read §5.4's table, not the checker | if an obligation legitimately belongs to a row outside its prefix's set, the set is wrong and will fail a correct document |
| **D-7** | `INV-2` carries its precondition; `TN-C-10` echoes it | that the precondition does not weaken `INV-2` into a tautology | if it does, the clause needs the re-anchor statement moved into it (it is in the following sentence) |
| **C4a-1** | as D-7 | — | — |
| **C4a-2** | `DV-12` extracts all three homes and compares sets | that §3.2 is acceptable as the single normative list | if not, pick another home; the instrument follows whichever is named |
| **C4c-1, C4c-2** | as D-1, D-2 | — | — |
| **C6-1, C6-2** | as D-3, D-4 | — | — |
| **C9** | §5.4 declares 7 and reports 5 observed; §13's DV-11 output is the actual run | that a declared-but-unused token is acceptable when its row owns no obligation | if not, delete the two unused tokens — but then the mapping table stops covering rows 3 and 7 |
| **the `TN-C-11` / `TN-A-01`-`02` conflict** | §9.2 `C05-6.4`; `TN-C-11` rewritten to selection; `TN-A-02` extended; `TN-A-03` added; T-C05-63; DV-20 | **whether the three-domain separation preserves BOTH boundaries** — that a consumer can still act on the tag, and that no C-05 value can decide a hit. §9.2's verification table is the claim; T-C05-63 is the test that would falsify it | if selection and outcome cannot be separated in practice, the conflict is real and belongs to the TD — **not** to a further C-05 revision |

### 15.1 Where S4 disagrees with Agent 2, stated plainly

Two findings, both about **how** to close rather than **whether**:

1. **D-1** — Agent 2 offered three closures and said (iii) was cheapest. S4 takes **(i) + (iii)**: a bounded obligation *and* an explicit acceptance. The reason is that (iii) alone leaves a defect documented but unmitigated, and (i) is one pull per frame for the consumers that need accuracy. **Option (ii) is rejected on a structural ground**: C-05 specifies no transport, so a producer cannot guarantee ordered delivery of a same-frame pair, and (ii) would forbid the very pair `PO-3` requires.
2. **D-3** — Agent 2 recommended mutability (their option (ii)). S4 takes constancy **with a named change path**, because their option (ii) explicitly says a change *closes the instance and opens a new one*, which is constancy for the instance's life; the only thing S3 lacked was the obligation, not the choice. Choosing mutability instead would require a revision to carry a new identity, which is the reading `INV-1`/`TN-P-07` were corrected to exclude.

**Neither disagreement is a claim that Agent 2 is wrong about the defect** — both defects were real in S3, and both are closed here. They are disagreements about the mechanism, and they are Agent 2's to adjudicate.

### 15.2 What I am correcting in my own earlier text

- **S3, still mine to own:** the identical `INV-2` clause with its precondition only in prose (`D-7`); the identity clause in `TN-P-07` that constancy made unreachable (`D-3`); the "audio cues" in row 5 (`D-4`); the two implementer cells carrying a row-7 token (`D-5`); the `DV-11` that compared agents (`D-6`); the "merely needs a resync" sentence in §3.6 rationale (c), which asserted an obligation nothing imposed (`D-1`); and the `PO-3` that fixed order without fixing content (`D-2`).
- **S3, withdrawn rather than corrected:** the sentence in §3.6 rationale (c) claiming a lost retime *"merely needs a resync"*. It is quoted in §3.6 so a reader of S4 can see what changed, and it is no longer normative.
- **Mine, carried forward from S2 and still owned:** the `INV-1` aging-field error, `TN-R-05`/`T-C05-46`, `EX-5`, the row-5 split, the undeclared `Resynchronised`, and the missing `C05-6.3` carrier dependency — all corrected in S3 and unchanged here.
- **Agent 2's own corrections, recorded not argued:** `A2-C05` §7.3's dilation sentence, withdrawn by them in their §2.5; and `A2-C05` §8's listing of "animation montage selection" among C-05 consumer capabilities, overstated in the same way their C8 finding said mine was.

---

## 16. Change log and supersession

### 16.1 Exactly what changed from `A1-C05-S3`

| Artefact | Change |
|---|---|
| §0 | rewritten: provenance, the missing A3 review stated with the commands that establish it, the seven defects and the decisions taken, the scope lock |
| §1, §2 | **new**: ten corrections at a glance and the finding-by-finding closure matrix naming the precise resolving section |
| §3.2 | the `VF` list becomes the **single normative home**; `INV-1` and the §4.2 struct quote it |
| §3.4 | one-revision precondition paragraph added ahead of the consistency proof |
| §3.6 | rationale (c) corrected (S3's resync claim withdrawn); `EX-5` case (d) described; **`PO-5` added** |
| §3.8 | retitled and rewritten: identity **fixed for the instance's lifetime**, with the close-and-reopen change path |
| §4.2 | struct comments point at §3.2 for the `VF` set; `WindowKey`/`AttackTag` comments state constancy and the selection-only boundary |
| §4.4 | the pull comment says a timing-dependent consumer re-pulls once per frame, so there is no "subscribe once" mode |
| §4.6 | **`INV-2` carries its precondition**; `INV-1` cites the seven fields of §3.2 |
| §4.8 | non-goals now exclude a C-05 value — `AttackTag` included — from any hit-resolution decision |
| §4.9 | **`PO-5`** added to the `C05-2.9` block |
| §4.10 | `C05-6.4` added to the carried-forward/boundary table, with its full text in §9.2 |
| §5.2 | row 5 loses audio and states Agent 1 owns none; row 6 owns audio and names its obligations; row 7 states it carries no obligation row; row 8 points at `C05-6.4`; row 3 states it owns types, not behaviour; row 2's range now `TN-P-01`…`TN-P-19` |
| §5.4 | rewritten: **seven tokens, each mapped to one row**, with the allowed-row rule DV-11 enforces and the declared/observed distinction |
| §6.1 | audio named as Agent 2's alone; AI row stated as *selection*; parry row stated as *outcome*; new paragraph separating selection from outcome; alternative 3 restated as constancy |
| §6.2 | damage/hit resolution row points at `C05-6.4` |
| §7 | `TN-P-07` identity clause removed; **`TN-P-18`** and **`TN-P-19`** added; `TN-P-15` cites `PO-5`; `TN-P-04` names the identity-change cancellation |
| §8 | `TN-C-10` limited to the held revision; **`TN-C-11` rewritten to selection**; `TN-C-12`/`TN-C-13` re-mapped; **`TN-C-14`** and **`TN-C-15`** added |
| §9 | **new §9.2 with `C05-6.4`** and its independent verification; `TN-A-02` extended to name `AttackTag`; **`TN-A-03`** added |
| §10 | `EX-5` cases (c), (cʹ), (d), (e); **`EX-11`** (mid-frame pull) and **`EX-12`** (identity close/reopen) added |
| §11 | requirements 12 and 13 added; coverage rows for the five new obligations; totals 43 / 67 |
| §12 | suites P, Q, R; cases **T-C05-63**…**T-C05-67**; `T-C05-51` and `T-C05-62` rewritten; catalogue extended to 67 |
| §13 | rewritten: **23 checks**, DV-11 row-level, DV-12 three-home, DV-19…DV-23 new, and the S3 failure demonstration |
| §14 | B-9/B-10 restated; **B-15** added |
| §15, §16, §17, §18 | rewritten for S4 |

### 16.2 What did not change

The per-instance no-history pull recovery; `TM-1`; `EN-1`/`EN-2`/`EN-3`; `AD-1`/`AD-2`; `RS-1`/`RS-2`/`RS-3`; `RM-1`/`RM-2`; the directory's content and its "schedules nothing" rule (`TN-R-06`); `C05-2.1`, `C05-2.3`, `C05-2.3a`, `C05-2.4`, `C05-2.5`, `C05-2.7`, `C05-2.8`; **`C05-6.1` and `TN-A-01` byte for byte**; X-1's conditional status; `C05-7.1`'s withdrawal of its own second sentence; `C05-6.3` and its `BLOCKED BY DEPENDENCY` status (B-11); every external blocker's status; every earlier document.

### 16.3 Supersession

`A1-C05-S4` supersedes `A1-C05-S3` **by statement, not by edit**. S3 remains at `a6b4e22` (provenance commit `ec3c2af`), blob `077232368c42b2cd910be2c9642ba05cd7faa382`, **unmodified**, as the record of what Agent 2 reviewed; S2 remains at `e5ddad6`, blob `bf6c8fb3…`; S1 at `2bb729f`, blob `dcec9e1a…`. Where S4 and S3 differ, S4 is the current C-05 text; where S4 is silent, S3 stands.

**Field-level supersessions worth naming, cumulative:** `A1-R3` §3.2's `TimingRevision` (renamed at S2, meaning restated at S3); `A1-R4` §3.3(e) (embedded as `INV-2`, same equation, same prohibition on wall-clock aging); `A2-C05` §7.3's dilation sentence (withdrawn by Agent 2); S3's `TN-P-07` identity clause and its §3.6 rationale sentence (withdrawn here, quoted so the change is visible).

---

## 17. Publication and provenance record

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` — **new file** |
| Version | 4.2 (`A1-C05-S4.2`) — targeted revision answering Agent 2's S4.1 reassessment and Agent 3's S4.1 review |
| Branch | `arena/3bc206a0-tdd` |
| **This document's own publishing commit and blob** | **written to `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md`** in the commit immediately after this text — see the note below |
| **Reviewed predecessor (pinned by both reviews)** | `A1-C05-S4.1` v4.1 at **`95918268ed5b20b878fef3ee0a7855ad18e6eeb6`**, blob **`d54e194affeaee98b1030e2b83b4c34e234fa382`** — **unmodified** |
| Reviews answered | Agent 2 `TDD-A2-REVIEW-A1C05-S4-1-001` v1.0 (commit `eee9401`, 594 lines, read in full); Agent 3 independent integration review v1 (commit `34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a`, 115 lines, read in full) — **read only, not modified** |
| Earlier reviews answered | Agent 2's S3 review `47dbdffb…` (`Docs/AGENT2_REVIEW_A1C05_S3_V1.md`); Agent 2's S2 review `ac498ce` — read only, not modified |
| Baselines preserved unmodified | `A1-C05-S4` v4.0 at `4692e973d04a94d7781677c704e7a0198abd2d70`, blob `424d2c69df62ebc1930eacd0ba67077c854ab31e`; `A1-C05-S3` v3.0 at `a6b4e22999c7f8622c7c67e9cdc39e2f57565c20`, blob `077232368c42b2cd910be2c9642ba05cd7faa382`; `A1-C05-S2` v2.0 at `e5ddad6`, blob `bf6c8fb3ddf3152d1627d3b6471278f57fc82541`; `A1-C05-S1` v1.0 at `2bb729f`, blob `dcec9e1ae3efd4651c290636e8a4d6623603dc83` |
| `A1-R1` / `A1-R2` / `A1-R3` / `A1-R4` / C-05-3 response | `25ab47c2…` / `5ee2769…` / `109331f3…` / `2cc548fa…` / `a94b49ef…` — **unmodified** |
| MEAD-A / MEAD-B / MEAD-C | read only; none moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| **Validation instrument** | **`docs/validation/dv_c05.py` — in this repository, 27 checks, runnable by any reviewer**: `python3 docs/validation/dv_c05.py <document>`. It is a **document-text** checker, not a test suite, and no test-suite claim is made from it |
| Contracts signed / frozen | **None** — C-05 remains proposed and unsigned |
| Code, Core types, project, merge, M0 | **None** |
| Acceptance tests | 67 cases `PROPOSED / NOT RUN`, **0 executed**; 27 document checks executed (§13) |

**Why this file carries no placeholder, and why that is the point.** S4.1's reviewed blob contained literal commit/blob placeholder fields (`S41_*`), which a later commit then filled — so the blob both reviewers pinned was one where a reader could not follow the document's own "review this exact blob" instruction (Agent 3 finding 7). **S4.2 removes the pattern rather than repeating it:** a document cannot contain its own blob hash without a post-publication edit, so the hash is written to **`docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md`** in the next commit, and both §18.1 and §18.2 point there. `DV-27` fails if any placeholder token appears in this file and fails if the register is not referenced — so the defect cannot return silently.

**This table's S4.1 values are exact, not abbreviated:** commit `95918268ed5b20b878fef3ee0a7855ad18e6eeb6` and blob `d54e194affeaee98b1030e2b83b4c34e234fa382`, the values TD item 6 requires and Agent 3's finding 7 names.

---

## 18. Handoff

### 18.1 To Agent 2 — re-review of your S4.1 reassessment

Review **the blob named in `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md`**, path `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` — not a branch tip, not a diff, not the S4.1 blob. **Your S4.1 findings and their dispositions are in §2.5**, one row each, and the TD's six consolidated items are in §2.7.

1. **D-4 / C6-2 the two-word deletion** — §8's preamble now reads *"Agent 1 for defence selection, dodge, camera response and framing; Agent 2 for AI reaction, audio cue selection (the only C-05 audio responsibility), montage trigger and VFX timing"*. `TN-C-15` unchanged.
2. **D-22-scope** — `DV-22` now inspects row 5, row 6, `TN-C-15`, **the §8 preamble** and **the whole document**, and it is **shown failing on the blob you reviewed** (§13.3). Is that the scope you asked for?
3. **C4c-N1** — §3.6(b) now states that the order **is** observable through a mid-frame pull under `PO-5`, with your conclusion kept and `PO-3` retained. `PO-3`, `PO-5`, `TN-P-15`, `TN-P-18`, `T-C05-51` and `T-C05-65` are byte-identical.
4. **D-1a / D-1b** — `TN-C-14` now attaches to the **call site**, requires an observation taken **in the frame of use**, states a **maximum interval of one frame measured on the shared axis**, requires **re-pull or suppression** when the guarantee cannot be shown, and **derives** the bound instead of asserting it. Is "at most one frame, measured from the missed revision's publication to the use" the wording you wanted?
5. **D-6b** — §5.4's tallies are now machine counts (23 / 12 / 3 / 2 / 3 / 0 / 0 = 43). The TD routed this to your addendum; it is fixed here because §5.4 is the table `DV-11` reads.
6. **D-6a-i condition** — `DV-24` is added and **fails on the S4.0 blob**, where your finding originated (§13.3). The class is closed, not just the instance.
7. **Carried verdicts** — D-1, D-2, D-3, D-5, D-6, D-7, C4a-1/2, C4c-1/2, C6-1, C9 are untouched; nothing is reopened.
8. **Agent 3's finding 6** on T-C05-63 — the combined held-snapshot + altered-tag + dataflow-instrumented scenario was raised by Agent 3, not by you. **It is in §12.2**; if you consider it insufficient, say so, and say which dataflow instrument you would accept.

**No signature, freeze or acceptance is requested, and none is implied by a verdict.**

### 18.2 To Agent 3 — re-review of your seven findings

Review **the blob named in `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md`**. Your findings and their dispositions are **§2.6**, one row each.

1. **Finding 1 (row 5)** — §5.2 row 5 is now *response selection and telegraph consumption*, explicitly **not** the hit outcome, and it points to **row 8** with `C05-6.1` / `TN-A-01`–`TN-A-03`. Is the exclusion stated where an implementer would look?
2. **Finding 4 (the bound)** — your counterexample is now a **named schedule** in `T-C05-64` (**s2**), the obligation is five rules in `TN-C-14` with the measure and the maximum interval stated, and the bound is derived. **Please try to break it again:** the interesting case is a consumer with no frame of its own (§`TN-C-14`(iii) requires it to use the shortest interval at which it acts).
3. **Finding 5 (audio)** — §8's preamble is corrected and `DV-22` widened; **DV-22 is shown failing on the blob you reviewed** (§13.3).
4. **Finding 6 (T-C05-63 / DV-20)** — the three conditions are combined, the assertion is on the **hit-resolver's input/use path** with a tainted-value instrument, and a **separate** selection-path assertion is retained. **`DV-20`'s limit is unchanged and admitted:** it is a text check; the dataflow claim is T-C05-63's, which is `PROPOSED / NOT RUN`.
5. **Finding 7 (provenance)** — no placeholder token exists anywhere in this file; the register carries the hash. **A negative existence claim is re-checked immediately before publication**, per Agent 2's §1.3 rule, and the result is recorded in the register.
6. **Your S3 review** — still not in the repository as of this revision (§0.2). If it exists elsewhere, say where; if not, the `TN-C-11`/`TN-A-01`–`02` resolution remains **S4's own** and B-15 stays `OPEN`.
7. **B-13 / TD-09** — unchanged and still external. `C05-6.4` still decides nothing about registration or unblockable authority.

### 18.3 Status

`DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD is selected. No C++ was written, no runtime validation was performed, and none is claimed.** TD-06, TD-09 and TD-12 are untouched and remain external blockers (B-1, B-2, B-4). **B-11 is `BLOCKED BY DEPENDENCY` on a C-04 decision**; B-12, B-13, B-14 unchanged; **B-15 stays `OPEN`** because Agent 3's S3 review is still absent, so the tag/arbitration resolution remains S4's own rather than a reviewer's. 67 acceptance cases are proposed and unexecuted — **no behaviour is validated by anything in this document**; 27 document checks pass and prove only that the text is internally consistent, and six of them are shown failing on earlier blobs in §13.3. **S4.2 stops here for TD reassessment.**
