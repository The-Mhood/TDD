# Agent 1 — C-05 Successor `A1-C05-S4.3.8`

**Response ID:** `TDD-A1-C05-SUCCESSOR-004.3.8`
**Version:** 4.3.8 — **final targeted validator correction of S4.3.7** (blob `0a0c36bec71f40d709878e67c19e4bca8f0b8b39`), closing the two conditions in Agent 2's review of S4.3.7 and the one non-blocking discrepancy it found. `DV-22` no longer reads a **determiner-quantified denial** (`No audio cue belongs to Agent 1.`) as an assignment; `DV-24` no longer gates **two-line** windows on a lowercase continuation, which had lost every capitalised wrap, and the document's `DV-24` pair count is corrected to the runner's value. **Seven verdicts move and nothing else does.** **No normative clause changes**, and no instrument behaviour verified at S4.3.7 is weakened — §0.7.8 is the exhaustive change list, §2.21 and §2.22 the two conditions, §2.23 the count discrepancy.

**Version of the baseline (history):** 4.3.7 — **targeted validator revision of S4.3.6** (blob `e3a1fa85243a4749591363d4196bb5d65dad7c84`), answering the two independent reviews of S4.3.6: Agent 2's `PASS WITH CONDITIONS` — one condition, three escapes (`MAJOR-1` possessive synonym, `MAJOR-2` foil window, `MINOR-1` three-line wrap) plus a weak `TD-60` — and Agent 3's separately reported `DV-22`/`DV-24`/`DV-11` findings, **whose review is again not in this repository** (§0.9). **No normative clause changes.** Seven instrument corrections, twenty new cases, every count re-derived. §0.7.7 is the exhaustive change list; §2.18, §2.19 and §2.20 are the three finding areas, each stating which reported defects are the same defect and which are distinct.

**Supersedes:** `A1-C05-S4.3.6`. **Superseded:** nothing yet.

**Version:** 4.3.6 — **targeted validator revision of S4.3.5** (blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb`), answering TD's directive on the two independent reviews: Agent 2's `MAJOR-1` (two ownership sentences its predicate accepted: one with a contrastive `unlike` clause, one using the document's synonym `the first agent`), Agent 3's `DV-24` and `DV-11` reports, and TD's instruction to reconcile the `DV-11` enforcement gap. **No normative clause changes** — Agent 2 gives the contract an independent PASS and reports no architectural blocker, so §5.2, §8, `TN-C-11`, `TN-C-15` and all 43 obligation rows are carried forward byte-identical. §0.7.6 is the exhaustive change list; §2.15, §2.16 and §2.17 are the three finding areas; **Agent 3's S4.3.5 QA review is not in this repository** — verified, stated and not worked around (§2.16).
**Date:** 2026-11-16 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch:** `arena/3bc206a0-tdd`
**Scope:** **S4.3.8 closes exactly two conditions and one arithmetic discrepancy. It is a correction cycle, not an expansion.** `DV-22`'s denial set gains the **quantified-subject** construction the `belongs to` widening made necessary — `no … audio … belongs to`, `none of the … audio … belong to`, and the same quantifier with the other possession predicates. `DV-24`'s `_joinable` gate is applied to **three-line windows only**, because a two-line window is already protected by the block guard, the sentence guard and the one-label-each rule; that restores detection of every capitalised wrap without weakening a single false-join control. The `DV-24` pair count is corrected from the hand-written `8` to the runner's `9`. The suite grows from **106 to 120** cases. **No new ownership pattern, no new validator feature and no contract change** — §0.7.8 is the exhaustive change list.

**Scope of S4.3.7 (history):** **S4.3.7 closes the three escapes Agent 2 reproduced and finishes three predicates; it changes nothing normative.** `DV-22`'s possessor is now derived from the agent-name token rather than re-spelled (so the synonym works as possessor), the foil test is bound to the clause the reference sits in rather than to a 32-character window, and the remaining positive-ownership forms the probe matrix found (`belongs to`, `owner is`, dash attribution) are recognised — with their denials and their contrast-object case kept passing. `DV-24` joins runs of up to three consecutive lines under guards that stop unrelated adjacent facts being welded into a contradiction. `DV-11` enforces the §5.4 owner clause as its **own** rule, verified against §5.2's row owners, instead of relying on the allowed-row test to catch it by accident. The suite grows from **86 to 106** cases. **No contract text changes at all** — §0.7.7 is the exhaustive change list.

**Scope of S4.3.6 (history):** **S4.3.6 corrects three instruments and nothing normative.** `DV-22`'s attribution now reads the document's own synonym (`the first agent`, via a named capture group) and skips a contrastive foil (`unlike`, `as opposed to`, `rather than`, `but not`) instead of taking the nearest reference blindly — closing Agent 2's two counterexamples. `DV-24` now reads label-first pairs, sentence-split pairs and pairs wrapped across a line break. `DV-11` now parses every row a token declares, applies the allowed-row rule as a **subset** test rather than an intersection, and compares §5.4's hand cell counts with the instrument. The regression suite grows from **67 to 85** cases. **No normative clause, obligation, count, identity decision, measure or publication mechanism is touched, and no contract text changes at all** — §0.7.6 is the exhaustive change list.
**Scope carried forward from S4.2, and unchanged:** **Agent 2's seven defects `D-1`…`D-7` and their conditions (`C4a-1`, `C4a-2`, `C4c-1`, `C4c-2`, `C6-1`, `C6-2`, `C9`), plus Agent 3's `TN-C-11` / `TN-A-01`-`TN-A-02` conflict** — no other change. No new architecture layer, no history, no event bus, no scheduler, no implementation. **S4.2 changes no obligation's count and adds no obligation: it corrects one normative clause's measurement rule (`TN-C-14`), one rationale bullet (§3.6(b)), one ownership row (§5.2 row 5), one ownership preamble (§8), two proposed test specifications (`T-C05-63`, `T-C05-64`), three validation instruments (DV-20, DV-22, plus new DV-24) and the publication metadata. Every change and its reviewer source is in §2.5–§2.7.**
**Status:** `DESIGN_ONLY` — contract text `PROPOSED — NOT FROZEN`; every acceptance test `PROPOSED / NOT RUN`; no C++, no Unreal project, no API or contract freeze, **no MEAD selection**, no signature, no merge, no M0 claim. **C-05 remains proposed, unsigned and unfrozen; U-07 remains open.**

---

## 0. Provenance and scope lock

### 0.1 What this revision answers

| Field | Value |
|---|---|
| **Baseline under revision** | `A1-C05-S4.3.7` v4.3.7 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md`, blob **`0a0c36bec71f40d709878e67c19e4bca8f0b8b39`** at `f1beb0c07f643d56c15297529196fb6a4118a97b`, 2,107 lines; **preserved unmodified**, with its instruments (validator `06cfe2f2…`, suite `2a33543a…`) |
| **TD's S4.3.8 directive** | the two independently identified material corrections only — `DV-22`'s quantified denial and `DV-24`'s capitalised continuation — while preserving every verified S4.3.7 improvement; answered in §2.21, §2.22 and §2.23 |
| **Independent review 1 (of S4.3.7)** | Agent 2, `TDD-A2-REVIEW-A1C05-S4-3-7-001` v1.0, commit **`17af7be859d517e273f3f7d3af055a768daa8abe`**, `Docs/AGENT2_REVIEW_A1C05_S4_3_7_V1.md`, 589 lines — **read only, not modified.** Verdict **`PASS WITH CONDITIONS`**: `CONDITION-1` (quantified denial), `CONDITION-2` (two-line continuation) and `MINOR-1` (the pair count) |
| **Independent review 2 (of S4.3.7)** | Agent 3 — **NOT IN THIS REPOSITORY**, verified across every ref and all 79 reachable commits immediately before publication (§0.9.2). Nothing here quotes or reconstructs it |
| **Baseline under revision (history)** | `A1-C05-S4.3.6` v4.3.6 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md`, blob **`e3a1fa85243a4749591363d4196bb5d65dad7c84`** at `034d091e1abcb507fdba6df4a05318a15aa5d7a1`, 1,931 lines; **preserved unmodified**, together with its instruments (validator `840fed67…`, suite `ee69f549…`) |
| **TD's S4.3.7 directive** | resolve the S4.3.6 review findings — `DV-22` (Agent 2 `MAJOR-1`/`MAJOR-2`, and Agent 3's separately reported positive-ownership escape), `DV-24` (three-line wraps and false joining), `DV-11` (the owner column, and `TD-60` reviewed) — while preserving the contract byte-for-byte; answered in §2.18, §2.19 and §2.20 |
| **Independent review 1 (of S4.3.6)** | Agent 2, `TDD-A2-REVIEW-A1C05-S4-3-6-001` v1.0, commit **`759ef103d1f8c9b2bdc64d0f41d1497f6c842313`**, `Docs/AGENT2_REVIEW_A1C05_S4_3_6_V1.md`, 560 lines — **read only, not modified.** Verdict **`PASS WITH CONDITIONS`**: one condition (`C-1`), three escapes, and `MINOR-2` on `TD-60` |
| **Independent review 2 (of S4.3.6)** | Agent 3 — **NOT IN THIS REPOSITORY**, verified across every ref and all 78 reachable commits immediately before publication (§0.9). Nothing here quotes, paraphrases or reconstructs it |
| **Baseline under revision (S4.3.6)** | `A1-C05-S4.3.5` v4.3.5 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md`, blob **`a0b46f46c81e85cea5d04b940aaf9aee46c19deb`** at `baa31db3c631f0fc3e69a82b6d71207ad8061218`, 1,779 lines; **preserved unmodified** |
| **TD's S4.3.6 directive** | resolve the independently reproduced validator/enforcement findings while preserving the contract: `DV-22` (Agent 2's `MAJOR-1`), `DV-24` (Agent 3) and `DV-11` (Agent 2 and Agent 3) — answered in §2.15, §2.16 and §2.17 |
| **Independent review 1** | Agent 2, `TDD-A2-ARCH-REVIEW-A1C05-S4-3-5`, commit **`659944b043b649601a555177fd0648018b1475e4`**, `Docs/AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md`, 541 lines — read only, not modified. Verdict: **PASS on the contract**, one `MAJOR-1` against the instrument and two minor consequences |
| **Independent review 2** | Agent 3, `AGENT3_A1_C05_S4_3_5_INDEPENDENT_INTEGRATION_QA_REVIEW_V1.md`, branch `arena/c64fc525-tdd` — **NOT IN THIS REPOSITORY.** Verified across every ref and all 76 reachable commits immediately before publication (§0.8, §2.16). Nothing here quotes, paraphrases or reconstructs it |
| **TD's S4.3.5 directive** | TD's S4.3.4 reassessment is **`PASS WITH CONDITIONS`**: both `DV-22` defects are accepted as corrected, and one publication inconsistency must be fixed — the *74* figure. Corrected here; §2.14 audits the rest |
| **TD's S4.3.4 directive** | TD's S4.3.3 review named two residual false negatives in `DV-22`: an **unnamed** denial excusing a positive ownership assertion, and a missing **relative-clause (`that`) boundary**. Both are reproduced on the published blob and closed in §2.13 and §13.3.5 |
| **TD's S4.3.3 directive** | TD's S4.3.2 verdict was `PASS WITH CONDITIONS` and named two outstanding conditions: reproduce the published verification against the exact commit, and adversarially test `NEG_AFTER`. Condition 1 reproduced exactly (§2.12). Condition 2 found a third false-negative class, answered in §2.12 and §13.3.4 |
| **TD's S4.3.2 directive** | a second `DV-22` false-negative class — `no problem owning audio cues` and relatives read as denials; answered in §2.11 and §13.3.3 — **closed at S4.3.2, unchanged here** |
| **Earlier baseline** | `A1-C05-S4.3` v4.3 — blob `7454602783575eaf4deba6a3d3f7043cff174f96` at `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, 1,432 lines; **preserved unmodified** |
| Reviewed artifact revised at S4.3 (still the object Agent 2 reviewed) | `A1-C05-S4.2` v4.2 — blob **`7d03e1df837493305831962f43882a1cd3496143`** at `a788f953256d208f3eb1310f3897924d007179b1`; **preserved unmodified** |
| **Immediate predecessor of the revised baseline (both S4.1 reviews pinned its blob)** | `A1-C05-S4.1` v4.1 — blob **`d54e194affeaee98b1030e2b83b4c34e234fa382`** at **`95918268ed5b20b878fef3ee0a7855ad18e6eeb6`**; **preserved unmodified**. Agent 2 `TDD-A2-REVIEW-A1C05-S4-1-001` (commit `eee9401`) and Agent 3 (commit `34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a`) both verified this exact blob |
| Predecessor (older) | `A1-C05-S4` v4.0 — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md`, blob `424d2c69df62ebc1930eacd0ba67077c854ab31e` at `4692e973d04a94d7781677c704e7a0198abd2d70` — **preserved unmodified** |
| **Agent 2's reassessment of S4.2 (the review this revision answers)** | `TDD-A2-REASSESS-A1C05-S4-2-001` v1.0 — `Docs/AGENT2_REASSESSMENT_A1C05_S4_2_V1.md`, **708 lines, read in full**; commit `c8e9f2a`; outcome **`PASS WITH CONDITIONS`** — contract text **passes**, two `PASS-BLOCKING` conditions (`N-1` `DV-22`, `N-2` duplicate identity) and one advisory (`N-3` unaddressed addendum) |
| **Agent 2's addendum to its S4.1 review** | `ADDENDUM-A1` at `e434dbe` — downgraded `D-1b` to `ADVISORY` and upgraded `D-1a`; S4.2 answered neither by name, which is `N-3`. **Cited in §17 as S4.3 requires** |
| **Agent 3's S4.2 report** | **NOT PRESENT IN THE REPOSITORY** — verified four ways immediately before publication; see §0.8. Its two attributed findings were reproduced from the reviewed blob instead, and are answered as defect *classes* |
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

| **Item** [QUOTED] | **Value** |
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

**Agent 2's S4.2 review corrected the attribution in that sentence, and S4.3 records the correction rather than restating the claim.** The per-blob attribution above is about whether an *instrument* fails on the blob containing the defect; it says nothing about which *component* inside the instrument did the failing. For `DV-22` both earlier failures came from the `§8 preamble clean` component — the whole-document scan component had never been shown to catch anything, and Agent 2 defeated it with a one-word prefix (§13.3). That is finding `N-1`, and it is closed by rewriting the predicate (§13.1), not by widening the claim.

---

### 0.7 What S4.3 and S4.3.1 changed — both lists, carried forward unchanged

**S4.3 was a targeted revision of the S4.2 blob, not a new revision of the contract.** The reviewed artifact is commit `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143`, 1,265 lines. Agent 2's verdict on it is **`PASS WITH CONDITIONS`**: the contract text **passes** and every one of its seventeen reassessed findings is closed; two conditions remain, both in the machinery rather than the contract, plus one advisory. **No normative clause is reopened, and no obligation is added, removed or renumbered: 43 remains 43, 18 suites remain 18, 67 proposed cases remain 67, 27 document checks remain 27.**

Every change S4.3 made, with no row omitted — **all eight are preserved unchanged in S4.3.1**:

| # | Change | Answers | Where |
|---|---|---|---|
| **1** | **`DV-22` rewritten, deny-by-default.** The fifteen-substring allowlist is deleted. Exemption is now a property of **location** — a fenced block, a table whose header carries `[QUOTED]`, or a `<!-- QUOTED-HISTORY-START -->` block — never of the words a line happens to contain. Outside those regions, a line containing the audio token and the first agent's name must negate the assignment **in the same clause**, or it is an offender. The live ownership sections may not be exempted at all, and the check asserts that. | `N-1` | §13.1, `docs/validation/dv_c05.py` |
| **2** | **`DV-24` rewritten, deny-by-default over the whole document.** Every declared/observed pair — digits or number words, either statement order, every match on a line, not the first — must equal the pair the instrument computes; all four anchor sites must still exist; a second contradictory pair on an anchor line fails. Previously only four hard-coded sites were read. | the reproduced `DV-24` false negative (§13.3) | §13.1, `docs/validation/dv_c05.py` |
| **3** | **The counterexamples are published.** Agent 2's keyword-prefixed injection and three `DV-24` probes are added to §13.3 with the exempt-region control, so each rewrite is shown catching the defect it exists for and shown *not* exempting legitimate history. | `N-1`, directive item 3 | §13.3 |
| **4** | **The duplicate `…-004.2` identity is resolved and recorded**: `7d03e1df…` is what `TDD-A1-C05-SUCCESSOR-004.2` denotes; the `arena/c64fc525-tdd` copy is **declared superseded and re-identified** as `TDD-A1-C05-SUCCESSOR-004.2-D`, and is **not merged**. Exact branches, commits and blobs in §2.9, in the decision record `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md`, and in the register. | `N-2` | §2.9, register |
| **5** | **The `TN-C-14` measure conflict is resolved on the record**: one frame on the **shared axis** is authoritative; the `1/60` second monotonic-elapsed measure is recorded as **rejected**, with the reasons. No merge, no averaging. | `N-2` | §2.9 |
| **6** | **Publication mechanism changed so a register cannot pin a superseded draft.** The document and the register naming its blob are published **in one commit**; the blob in the register is therefore the blob a reader of that commit holds, and the commit is identified by the paths it introduced rather than by a self-referential hash. | directive item 4 | §17, register |
| **7** | **Agent 2's addendum is answered**: `ADDENDUM-A1` (`e434dbe`) is cited in §17, and `D-1b` is recorded as adopted-as-an-improvement while remaining `ADVISORY` under Agent 2's own taxonomy. | `N-3` (advisory) | §17, §18.1 |
| **8** | **A runnable regression suite** accompanies the validator: `docs/validation/test_dv_c05_regressions.py` runs the injections above against mutated copies and asserts the verdict of each, so the two rewrites are testable by a reviewer in one command. | directive items 1 and 3 | `docs/validation/` |

**What S4.3 preserved, and how a reviewer can check it in one minute.** The seven clauses Agent 2 byte-compared (`TN-P-18`, `TN-P-19`, `TN-C-10`, `TN-C-11`, `TN-C-15`, `TN-A-02`, `TN-A-03`, and `PO-5`) are not touched by S4.3 — every change in the table above is either validator code, metadata, or text in §0, §2, §13, §17 or §18. `DV-1`…`DV-27` remain contiguous, none added, none dropped. D-4 audio ownership, D-1a, D-1b, C4c-N1, `PO-3`/`PO-5`, D-6a (*withdrawn*: 7 declared / 5 observed, never 6 observed), D-6a-i, D-6b, the `TN-C-11` arbitration boundary and `T-C05-63` are **carried forward exactly**.

**What S4.3 is not.** It is not a signature, a freeze, a merge, a MEAD selection, a C++ change, an M0 authorisation, or a claim that C-05 or U-07 is closed. **Acceptance tests remain unrun: 0 of 67.** Every check in §13 is a check on document text.

### 0.7.1 What S4.3.1 changed — the exhaustive list, and it had three rows

**S4.3.1 was a narrow correction, not a new revision.** TD accepted S4.3 as the baseline and found one further reproducible false negative in `DV-22`. That defect, its tests and one stale cross-reference were the whole of it, and **all three are preserved unchanged here**.

| # [QUOTED] | Change | Why | Where |
|---|---|---|---|
| **1** | **`DV-22` now evaluates every audio mention separately.** A negation must cover *the mention being judged*; it may not be inherited from another clause, another sentence, or another object. Word order is read both ways (before the mention and, for explicit ownership constructions, after it). The keyword allowlist is still absent, and the live ownership sections still may not be exempted. | TD's *"owns no audio, but owns audio cues"* form passed S4.3's predicate (verbatim in §2.10 and §13.3.2), because S4.3 took one negation per clause and a comma does not end a clause | §13.1, §13.3.2, `docs/validation/dv_c05.py` |
| **2** | **The adversarial cases become regression tests.** The suite grows from 18 to **30** cases, including all six TD cases and four word-order variants, with a `--compare` mode that runs the same cases against a named older validator so the before/after is reproducible by a reviewer. | TD item 2: the failure must be shown, not asserted | `docs/validation/test_dv_c05_regressions.py` |
| **3** | **§18.3's final sentence corrected** from *"S4.2 stops here"* to *"S4.3.1 stops here"*. | TD item 3: it was stale by one revision | §18.3 |

**What is explicitly not changed.** The contract text of S4.2 — every clause, obligation, count, suite and proposed case — is carried forward byte-identical; `DV-24`'s deny-by-default rewrite is untouched; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded) stands; `TN-C-14` remains one frame on the shared axis; `D-4`, `D-1a`, `D-1b` and `C4c-N1` stand as closed; the provenance mechanism (register published in the same commit as the document) stands. **43 obligations, 18 suites, 67 proposed cases, 0 executed.**

---

### 0.7.2 What S4.3.2 changed — the exhaustive list, and it had three rows

**S4.3.2 was a targeted revision, not a new contract.** TD accepted S4.3.1's fix and then identified a second class of false negative by reading the predicate: `NEG_BEFORE` accepted any `no … audio` within 28 characters, so *"has no problem owning audio cues"* and *"has no objection to owning audio cues"* — which assert ownership — counted as denials of it. That class, its tests, and the revision stamp in §18.3 are the whole of this revision.

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **`DV-22` accepts a bounded set of grammatical denials instead of `no … audio`.** A negation must *deny ownership or responsibility*: a denial verb with `no` and the audio object (`owns no audio cue`), `no <audio> <denial noun>` (`no C-05 audio responsibility`), `no <denial noun> for/over/of <audio>` (`no responsibility for audio cue selection`), `is not responsible/owner for/of <audio>`, `does not own <audio>`, `owns none of the audio`, and the two reversed forms. Anything else — `no problem owning`, `no objection to owning`, `no restriction on owning`, `no difficulty taking responsibility for`, `no issue with owning` — is a **positive** statement about ownership. | TD's source inspection: the previous pattern read a *denial of difficulty* as a *denial of ownership* | §13.1, §13.3.3, `docs/validation/dv_c05.py` |
| **2** | **The class becomes regression tests.** The suite grows from 30 to **44** cases: the five TD forms, one further noun in the same class, a positive assertion following one of them, the three required-pass denials, four further genuine denials (including two that S4.3.1 wrongly rejected), and the historical-exemption control for this class. | TD item 2: the failure must be demonstrated, not asserted | `docs/validation/test_dv_c05_regressions.py` |
| **3** | **§18.3's closing sentence re-stamped** to *"S4.3.2 stops here for TD reassessment."* | the sentence names the current revision by design; S4.3.1 carried the S4.2→S4.3.1 correction, and the same rule applies to this revision's own stamp | §18.3 |

**What is explicitly not changed by S4.3.2.** Every clause, obligation, count, suite and proposed case is byte-identical to S4.3.1; `DV-24` is untouched; the `N-2` identity declaration stands (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded); `TN-C-14` remains one frame on the shared axis; `D-4`, `D-1a`, `D-1b` and `C4c-N1` stand; the register is published in the same commit as the document it pins. **The check was not made stricter by flagging every audio mention** — a denial still passes, and the two classes of denial S4.3.1 rejected are now accepted (§13.3.3). **43 obligations, 18 suites, 67 proposed cases, 0 executed.**

### 0.7.3 What S4.3.3 changed — the exhaustive list, and it had four rows

**S4.3.3 was a targeted revision, not a new contract.** TD's S4.3.2 verdict was `PASS WITH CONDITIONS`. Condition 1 — independently reproduce the published verification against the exact commit — reproduced exactly: an archive of `b754deb3` gave **27/27** document checks and **44/44** regression cases (§2.12). Condition 2 — adversarially test `NEG_AFTER` — found a third class of false negative: a denial *after* an audio mention exempted that mention even when the first agent's ownership was asserted in the same sentence, before the denial. That class, its tests, one stale result cell, and the revision stamp in §18.3 are the whole of this revision.

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **`NEG_AFTER` is scoped to its own clause and its own agent.** A denial that follows a mention now exempts it only if the denial is in the *same clause and same phrase* — the gap may not cross a comma, a semicolon, a sentence end, an em or en dash, or a conjunction or relative pronoun (`and`, `but`, `yet`, `while`, `although`, `whereas`, `which`, `who`, `whose`) — and only if the denial names the **first** agent or names nobody. The agent is read through the rest of the clause, so *"not owned by Agent 2"* is Agent 2's denial and does not excuse the mention. Denials stated *before* the mention (`NEG_BEFORE`) are unchanged. | TD's adversarial test — an ownership assertion in the first clause and a denial in the second, joined by a comma and `but` — was accepted although the sentence asserts the ownership | TD's S4.3.3 condition; §13.1, §13.3.4, §2.12, `docs/validation/dv_c05.py` |
| **2** | **The class becomes regression tests.** The suite grows from **44** to **56** cases: nine lines that must fail (comma + `but`, `which` naming Agent 2, `and` naming Agent 2, a denial naming nobody, a second sentence, denial-then-assertion, semicolon-joined, em-dash apposition naming Agent 1, a parenthesised denial naming Agent 2) and three genuine denials that must keep passing, including the reversed order and a denial in a later clause about a different object. | the correction is only as good as the cases that pin it, and TD required the must-PASS set to be re-tested | §13.3.4, `docs/validation/test_dv_c05_regressions.py` |
| **3** | **One result cell corrected, not rewritten.** §13.1's `DV-22` row on the published S4.3.2 blob stated *exempt lines 229 (fenced 157) … audio mentions evaluated 93*; the checker's actual output for that blob is **exempt lines 234 (fenced 162) … mentions 110**. The figures were left over from a draft of S4.3.2 taken before §0.7.2 and §2.11 added their evidence blocks, and no check compares a result cell to the computed value, so nothing caught it. This revision reports the computed figures for its own text and records the discrepancy rather than quietly restating it. | an inaccurate result cell is a provenance defect, and TD asked for honesty over tidiness | §13.1, §2.12 |
| **4** | **§18.3's closing sentence re-stamped** to *"S4.3.3 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** Every clause, obligation, count, suite and proposed case is byte-identical to S4.3.2; `DV-24` is untouched; `NEG_BEFORE` is untouched, so every denial that S4.3.2 accepted before the mention is still accepted; the `N-2` identity declaration stands; `TN-C-14` remains one frame on the shared axis; `D-4`, `D-1a`, `D-1b` and `C4c-N1` stand; S4.3.2 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **The tightening was measured before it was made**: on the S4.3.2 text, **0 of the 110 audio mentions were accepted only by `NEG_AFTER`**, so no verdict on the document itself could change. **43 obligations, 18 suites, 67 proposed cases, 0 executed.**

### 0.7.4 What S4.3.4 changed — the exhaustive list, and it had four rows

**S4.3.4 was a targeted revision, not a new contract.** TD reviewed S4.3.3 and named two residual false negatives in the same predicate, both of which reproduce on the published blob. They share one root: the trailing-denial rule decided *what counts as a denial* by looking for an agent name, and treated the absence of one as evidence of denial rather than as an absence of evidence.

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **An unnamed trailing denial no longer counts.** `negated_mention()` used to accept a post-mention denial when it named no agent at all (`if not named or named[0] == '1'`). It now accepts three cases only: the denial **names the first agent**; or it names **nobody** and is an explicit **universal** exclusion (`nobody`, `no one`, `anyone`); or it is a denial stated **before** the mention, which is `NEG_BEFORE` and untouched. An unnamed `is not owned` is no longer evidence that the first agent does not own the cues. | TD's condition A: a line that asserts the first agent owns cue selection, followed by an unnamed `is not owned`, was accepted although it asserts the ownership; an unnamed denial must not excuse that | TD's S4.3.4 directive; §13.1, §13.3.5, §2.13 |
| **2** | **The universal exclusion must genuinely exclude the first agent.** The universal branch is refused when the same clause also carries an explicit first-agent ownership construction (`owned/claimed/carried/held/supplied/provided/selected by Agent 1`, a possessive `Agent 1's … cues`, or a colon form `… : Agent 1`). | a universal denial followed in the same clause by an explicit first-agent ownership phrase is not a denial of his ownership, and the wording test TD asked for is *"where the wording genuinely excludes Agent 1"* | §13.1, §13.3.5, §2.13 |
| **3** | **`that` joins the phrase boundary.** `_NOT_CROSS` already stopped a denial from crossing a comma, a semicolon, a sentence end, a dash, a conjunction or a relative pronoun; it omitted `that`, so *"owns audio cues that are not owned by anyone"* could be read as a denial spanning the relative clause. | TD's condition B: a denial may not cross a relative clause and excuse an earlier assertion | §13.1, §13.3.5 |
| **4** | **§18.3's closing sentence re-stamped** to *"S4.3.4 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** Every clause, obligation, count, suite and proposed case is byte-identical to S4.3.3; `DV-24` is untouched; `NEG_BEFORE` is untouched, so every denial stated before the mention — `owns no audio cue`, `no C-05 audio responsibility`, `does not own …`, `owns none of the audio` — behaves exactly as it did; the `N-2` identity declaration stands; `TN-C-14` remains one frame on the shared axis; `D-4`, `D-1a`, `D-1b` and `C4c-N1` stand; S4.3.3 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **The tightening was measured before it was written**: on the S4.3.3 text, **0 of the 123 audio mentions depend on a trailing denial at all**, and the full 56-case suite passes unchanged under the new predicate, so no verdict on the document or on the previous cases moved. **43 obligations, 18 suites, 67 proposed cases, 0 executed.**


---

### 0.7.5 What S4.3.5 changed — the exhaustive list, and it had three rows

**S4.3.5 was a metadata correction, not a revision of the contract or of the check.** TD accepted S4.3.4's two `DV-22` corrections and found one inconsistency in the document's own front matter: the Scope line said the regression suite grew from 56 to **74** cases. It grew from 56 to **67**. Nothing else in the file was wrong, and nothing else in the file changes.

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **The Scope line's suite figure is corrected** from *"grows from **56** to **74** cases"* to *"grows from **56** to **67** cases"*. The sentence also now states the composition — 56 predecessor cases plus `TD-31`…`TD-41` — so the number can be checked against §17 and the runner without opening the test file. | the suite has 67 cases; `DV-2` counts 67 case ids, the runner prints `67/67`, and the register records 67 | §8 scope line, §2.14 |
| **2** | **Every other suite-count claim in the document is audited and listed**, with the value the runner actually prints, so that the same class of drafting error is visible rather than merely corrected once. | TD's instruction: *"Check the complete document for any other inconsistent suite-count claims"* | §2.14 |
| **3** | **§18.3's closing sentence re-stamped** to *"S4.3.5 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** The `DV-22` predicate is **byte-identical** to S4.3.4 — S4.3.5 contains no predicate change at all, and the validator is carried forward with only its register path repointed at this revision. The regression suite is unchanged: **67 cases**, no case added, removed, renamed or re-ordered. Every clause, obligation, count, suite and proposed case is byte-identical to S4.3.4; `DV-24` and `NEG_BEFORE` are untouched; the `N-2` identity declaration stands; `TN-C-14` remains one frame on the shared axis; `D-4`, `D-1a`, `D-1b` and `C4c-N1` stand; S4.3.4 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **43 obligations, 18 suites, 67 proposed cases, 0 executed.**


### 0.7.6 What S4.3.6 changed — the exhaustive list, and it had five rows

**S4.3.6 was a validator revision, not a contract revision.** Agent 2's independent review passes the contract and finds no architectural blocker: one counterexample pair in `DV-22`'s attribution, two minor consequences and one acknowledged limitation. Agent 3's review is not in the repository, so its `DV-24` and `DV-11` claims cannot be reproduced here (§2.16). Everything this revision changes is inside `docs/validation/dv_c05.py` and its suite; **no contract sentence moves.**

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **`DV-22` reads the document's own synonym and skips contrastive foils.** `AGENT_REF` gains `the first agent`, read from a **named group** (a bare alternative leaves `group(1)` as `None`, and the escape survives — Agent 2 measured that trap and so did this revision); a reference introduced by `unlike`, `as opposed to`, `rather than` or `but not` is dropped before the governing subject is chosen. | Agent 2's `MAJOR-1`: two ownership sentences — one with a contrastive `unlike` clause, one using the synonym — both scored `PASS` | §2.15, §13.3.6, `TD-42`…`TD-51` |
| **2** | **`whereas` is deliberately *not* a foil, and an object negation is recognised.** Dropping a reference introduced by `whereas` loses a true positive (a `whereas` clause whose subject is the first agent — probe `C7`); and once `the first agent` becomes attributable, `The first agent owns the camera, not the audio cues` must still pass, so `, not the audio` joins the bounded denial set. | measured deviation from Agent 2's recipe, and a false positive the synonym change would otherwise create | §2.15, `TD-50`, `TD-51` |
| **3** | **`DV-24` reads three more restatement forms**: a label followed by punctuation, a pair split by a sentence break, and a pair wrapped across a line break. | three false negatives found by this revision's own probing (§2.16); the check's own comment already claimed "every pair" | §2.16, §13.3.6, `TD-52`…`TD-55` |
| **4** | **`DV-11` is reconciled with its normative sentence**: every row a token declares is parsed (`rows 2 and 5` used to read as `{2}`), the allowed-row rule is a **subset** test (`decl[tok] <= allowed[prefix]`) instead of an intersection that passed on one legal row, and §5.4's hand cell counts are compared with the instrument. | TD's `DV-11` item; the three gaps are reproduced in §2.17 | §2.17, §13.3.6, `TD-56`…`TD-59` |
| **5** | **§18.3's closing sentence re-stamped** to *"S4.3.6 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** Every normative clause, obligation, count, suite and proposed case is byte-identical to S4.3.5 — §5.2, §8's preamble, `TN-C-11`, `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64` and all 43 obligation rows are carried forward without a character of change, because Agent 2's review gives the contract an independent PASS and no reviewer demonstrated a normative defect. `D-1`…`D-7` and the seven conditions are not reopened. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain explicitly unresolved and are not touched** — the arbitration boundary is TD's to settle, and this revision does not settle it. The `N-2` identity declaration stands; `TN-C-14` remains one frame on the shared axis; S4.3.5 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **43 obligations, 18 suites, 67 proposed cases, 0 executed; the instrument suite is 85 cases (67 + 18 new).**

### 0.7.7 What S4.3.7 changed — the exhaustive list, and it had seven rows

**S4.3.7 was a validator revision, not a contract revision.** Agent 2's `PASS WITH CONDITIONS` passes the contract and confines its single condition to three escapes in two predicates and one join; no reviewer demonstrated a normative defect. Everything this revision changes is inside `docs/validation/dv_c05.py` and its suite. **No contract sentence moves** — not one character of §5.2, §5.4, §8's preamble, `TN-C-11`, `TN-C-14`, `TN-C-15`, the `TN-A` boundary, the 43 obligation rows, the 18 suites, the six preserved clauses or the 17 case specifications.

| # | Change | Why | Where |
|---|---|---|---|
| **1** | **The agent-1 name is written once and every attachment path is derived from it.** `AGENT1`/`AGENT1_POSS` replace the literal `agent[-\s]?1` in `FORWARD_OWNER` and in the denial helper, so the synonym works as a **possessor** and not only as a subject | Agent 2's `MAJOR-1`: the possessive synonym is accepted | §2.18 A, `TD-61` |
| **2** | **The foil test is bound to the clause the reference sits in**, not to a fixed 32-character window: scan back to the nearest clause boundary (comma, semicolon, parenthesis, em dash) and ask whether *that* clause opens with a contrastive marker | Agent 2's `MAJOR-2`: a foil carrying a subordinate clause re-inverted attribution | §2.18 B, `TD-62` |
| **3** | **The remaining positive-ownership forms are recognised** — `belongs to`, `owner is`, and dash attribution — each derived from the same two tokens, with their denials taught in the same change (`does not belong to`) and the contrast-object case excluded | the class `MAJOR-1` belongs to, found by this revision's own probe matrix (§2.18 C); Agent 3's separately reported escape is **not obtainable** and is not claimed to be one of these | §2.18 C, `TD-63`…`TD-67` |
| **4** | **`DV-24` joins runs of up to three consecutive non-exempt lines**, under four guards: never across a block boundary (table row, heading, blockquote, list item, fence, blank), never across a sentence terminator, the next line must continue the sentence, and a window may carry at most one `declared` and one `observed` label | Agent 2's `MINOR-1`, and the three-line class reported separately: joining adjacent pairs only left a three-line wrap unassembled — and the old join **did** weld list items into a contradiction (`TD-75`) | §2.19, `TD-71`…`TD-76` |
| **5** | **`DV-11` enforces the §5.4 owner clause as its own rule**: the row-owner map is declared and **verified against §5.2's own text**, each token's agent is read from §5.4's `Agent` column, and every declared row's owner must intersect the token's agent | the third clause of the normative sentence had no instrument; `TD-60` failed only because row 7 is outside `TN-C`'s `{5, 6}` | §2.20, `TD-77`…`TD-80` |
| **6** | **`TD-60` kept and re-cast, not deleted**: it is recorded as the case that isolates the *allowed-row* rule, and `TD-77` is added as the case that isolates the *owner* rule (`row 5` is inside `TN-C`'s allowed set, so only ownership can reject it) | Agent 2's `MINOR-2` and TD's instruction to strengthen or replace `TD-60` | §2.20, §13.3.7 |
| **7** | **§18.3's closing sentence re-stamped** to *"S4.3.7 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** Every normative clause, obligation, count, suite and proposed case is byte-identical to S4.3.6 — including `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64` and all 43 obligation rows — because no reviewer demonstrated a normative defect and this revision found none. `D-1`…`D-7` and the seven conditions are not reopened. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain explicitly unresolved** and are not touched; the arbitration boundary is TD's to settle. The `N-2` identity declaration stands. S4.3.6 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **43 obligations, 18 suites, 67 proposed cases, 0 executed; the instrument suite is 106 cases (86 + 20 new).**

### 0.7.8 What S4.3.8 changes — the exhaustive list, and it has four rows

**S4.3.8 is a correction cycle, not an expansion.** Agent 2's review of S4.3.7 passes the contract and files two conditions and one discrepancy, all mechanical. **No contract sentence moves**, and no behaviour verified at S4.3.7 is weakened: every S4.3.7 case keeps its expected verdict, and the two changes are made inside denial coverage and one join gate.

| # [QUOTED] | Change | Why | Where |
|---|---|---|---|
| **1** | **`DV-22`'s denial set gains the determiner-quantified subject** — `no … audio … belongs to <Agent 1>`, `none of the … audio … belong to <Agent 1>`, and the same quantifier with `is owned by` / `is <Agent 1>'s`. Each construction spans the mention, so it denies *that* mention and no other | Agent 2's `CONDITION-1`: `No audio cue belongs to Agent 1.` was read as an **assignment** — a fail-closed false alarm created by the S4.3.7 `belongs to` widening | §2.21, `TD-81`…`TD-85` |
| **2** | **`_joinable`'s continuation gate applies to three-line windows only.** The block-boundary guard, the sentence-terminator guard and the one-label-each rule are untouched and still protect two-line windows | Agent 2's `CONDITION-2`: S4.3.7 gated two-line windows on a lowercase continuation, so **every capitalised wrap** was accepted — a missed hazard, and a regression against S4.3.6 | §2.22, `TD-86`…`TD-94` |
| **3** | **The document's `DV-24` pair count is corrected to the runner's value (9, not 8)** in §13.1 and in the register | Agent 2's `MINOR-1`: a hand-restated tally drifted from its computed value — the exact class §5.4 warns about | §2.23, §13.1 |
| **4** | **§18.3's closing sentence re-stamped** to *"S4.3.8 stops here for TD reassessment."* | the sentence names the current revision by design | §18.3 |

**What is explicitly not changed.** Every normative clause, obligation, count, suite and proposed case is byte-identical to S4.3.7 — `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, the six preserved clauses, the 17 case specifications, all 43 obligation rows and all 18 suites. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain explicitly unresolved and are not touched.** `D-1`…`D-7` are not reopened. **No new ownership pattern is taught and no new validator feature is added**: the only ownership change is a *denial* the widening required, and the only join change is **removing** a gate from the shorter window, not adding one. Agent 2's §3.6 residual families (auxiliary/modal, perfect aspect, the appositive `not`/`never` foil) are **not** addressed here — they are non-blocking, they are not among the two authorised corrections, and adding them would be the general-purpose expansion the directive forbids. S4.3.7 and every earlier artifact and register are preserved byte-identical, and this revision's register is published in the same commit as this document. **43 obligations, 18 suites, 67 proposed cases, 0 executed; the instrument suite is 120 cases (106 + 14 new).**

### 0.8 Agent 3's reports are not in the repository — stated, not worked around

The S4.3 directive asked for a response to Agent 3's latest S4.2 report, and named two findings from it: a demonstrated `DV-24` false negative and a reported commit/blob mismatch. **As of this publication there is no Agent 3 S4.2 review in this repository.** That is a negative existence claim, so it is verified the way Agent 2's §1.3 rule requires — immediately before publication, and four ways:

| # | Check | Result |
|---|---|---|
| 1 | `git ls-remote --heads origin` | three branches: `arena/3bc206a0-tdd`, `arena/5dde91a4-tdd` (`c8e9f2a`), `arena/c64fc525-tdd` (`c800bf0`) |
| 2 | commits on `arena/c64fc525-tdd` after Agent 3's S4.1 review (`34b035b`) | `99717e0` and `c800bf0` only — both touch `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md`, neither is a review |
| 3 | Agent 3 files on any branch | three, all on `arena/c64fc525-tdd`: `AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md`, `AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md` (114 lines — the S4.1 review) and `AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md`. **None is an S4.2 review**, and none mentions `DV-24`, `7d03e1df` or `eb774f5d` |
| 4 | repository-wide grep for `DV-24`, `7d03e1df`, `eb774f5d` in Agent 3 files | no match outside the file in row 3; no other Agent 3 file exists |

**Consequences, stated so the record cannot be read as more than it is.**

1. **I do not quote, paraphrase, characterise or anticipate Agent 3's S4.2 findings**, and I make no claim about its verdict. Nothing here should be read as an answer to a text I have not read.
2. **The two defect classes the directive names were nevertheless reproduced from the reviewed blob itself, and both are real.** The `DV-24` false negatives are demonstrated in §13.3 with three probes on the S4.2 text; the commit/blob mismatch class is demonstrated by `git show eda9bd2671650b0c41a8aa1cff97da0dd0fad593:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md` naming `86f56af0b4e88441eb897fb9e369f56be6cf4563` while that same commit (`a788f953256d208f3eb1310f3897924d007179b1`) held `7d03e1df837493305831962f43882a1cd3496143` — Agent 2's check 3b, and a defect S4.3 fixes structurally rather than by editing the value.
3. **If Agent 3's report exists outside this repository, TD should treat its exact probe as unread by me.** The closures offered here are closures of the *classes*, demonstrated by reproducible probes; if Agent 3's probe differs from mine, the corrected `DV-24` should be tested against it before the condition is called closed.
4. **Agent 3's S4.1 review remains the only Agent 3 artifact I have read**, and nothing in it is extended, restated or re-attributed here.

### 0.9 The Agent 3 S4.3.5 QA review named in the directive is also absent — verified, not assumed

TD's S4.3.6 directive names Agent 3's `AGENT3_A1_C05_S4_3_5_INDEPENDENT_INTEGRATION_QA_REVIEW_V1.md` on branch `arena/c64fc525-tdd` and instructs me to obtain its exact `DV-24` counterexamples. **That file is not in this repository.** The claim is negative, so it is verified the way the rule requires — immediately before publication, and five ways:

| # | Check | Result (run immediately before the publishing commit) |
|---|---|---|
| 1 | `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `baa31db` · `arena/5dde91a4-tdd` `659944b` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| 2 | every file on `arena/c64fc525-tdd` (`c800bf0`) | three Agent 3 files, all published before S4.3: `AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md`, `AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md`, `AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md` |
| 3 | filename search across **all 76 commits reachable from every ref** | `git grep -l "S4_3_5_INDEPENDENT_INTEGRATION_QA"` and `git grep -l "INTEGRATION_QA_REVIEW"` over `$(git rev-list --all)` — **no match** |
| 4 | `DV-24` mentions inside the three Agent 3 files | **0, 0, 0** — none of them discusses the instrument at all |
| 5 | `git log --all --name-only` filtered for `AGENT3` | the same three paths; no fourth Agent 3 artifact exists at any commit |

**What that means for this revision, stated so the record cannot be read as more than it is.**

1. **Agent 3's two `DV-24` counterexamples and its narrower `DV-11` gap are NOT reproduced, NOT quoted, and NOT closed here.** I cannot test a probe I have not seen, and I will not substitute my own probes for the reviewer's and call the finding closed. **Both Agent 3 findings remain `OPEN — ARTIFACT ABSENT`** (§2.16, §2.17).
2. **What this revision does close is three `DV-24` and three `DV-11` defects that I found by probing the instruments myself**, with the probes and the mutations published in §2.16 and §2.17 so they can be re-run. Those are labelled `A1-P1`…`A1-P6` and are **additional**, not substitutes.
3. **If Agent 3's review exists outside this repository, its probes should be run against the corrected validator before either finding is called closed** — and if they fail, the instrument is still defective, whatever this revision's own probes show.
4. **No statement in this document characterises Agent 3's verdict, its severity assignments or its claims.** The directive's description of its findings is the only information about it that I have, and it is reported as the directive's description, not as the review.

### 0.9.1 The same check, one revision later: Agent 3's S4.3.6 review is absent too

TD's S4.3.7 directive relays three Agent 3 findings — a `DV-22` positive-ownership escape, `DV-24` three-line wraps and false joining, and the `DV-11` owner column. **No Agent 3 review of S4.3.6 exists in this repository**, so those findings arrive as the directive's description and nothing more. Verified immediately before publication, five ways:

| # | Check | Result |
|---|---|---|
| 1 | `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `034d091` · `arena/5dde91a4-tdd` **`759ef10`** (Agent 2's S4.3.6 review — **present**) · `arena/c64fc525-tdd` `c800bf0` (unchanged) · `main` `5e3d1da` |
| 2 | every `AGENT3` path on every ref | **three**, all published before S4.3: the S1 readiness note, the S4.1 review and the telegraph-authority recommendation |
| 3 | filename search across **all 78 commits** reachable from every ref | `git grep -l` for `AGENT3_A1_C05_S4_3_6` and for `S4_3_6` inside `AGENT3*` — **no match** |
| 4 | `DV-24` mentions in the three Agent 3 files | **0, 0, 0** |
| 5 | `git log --all --name-only` for `AGENT3` | the same three paths; no fourth artifact at any commit |

### 0.9.2 One revision further: Agent 3's S4.3.7 review is absent as well

Verified immediately before publication, the same five ways, on the tree this document ships with: `git ls-remote --heads origin` (`arena/3bc206a0-tdd` `f1beb0c` · `arena/5dde91a4-tdd` **`17af7be`** — Agent 2's S4.3.7 review, present and read · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da`); every `AGENT3` path on every ref — **three**, all published before S4.3; a filename and content grep for `AGENT3_A1_C05_S4_3_7` and `S4_3_7` inside `AGENT3*` across **all 79 reachable commits** — **no match**; `DV-24` absent from all three Agent 3 files; and `git log --all --name-only` filtered for `AGENT3` — the same three paths.

**What this costs, stated plainly.** Agent 3's `DV-22` escape **cannot be matched** against Agent 2's `MAJOR-1`/`MAJOR-2`, because I have not seen it; §2.18 says that explicitly rather than inventing a correspondence. Its `DV-24` three-line finding **does** correspond to a defect Agent 2 reproduced independently, so that one can be discussed on the merits (§2.19). Its `DV-11` owner-column finding **does** correspond to a defect this revision confirmed by construction — the third clause of the normative sentence had no instrument, and the directive's own `TD-60` observation is the proof (§2.20). **None of the three is closed by asserting Agent 3 said so**; each is closed, or not, on reproduced evidence, and the two that could not be reproduced from the artifact are labelled.


---

## 2. Finding-by-finding closure matrix

**Column 3 is the precise S4 location that resolves the finding.** Where S4 chose differently from Agent 2's recommendation, the row says so and gives the reason; that is the "remaining disagreement" column the disposition asks for.


### 2.1 Agent 2's seven defects

| # | Finding (abridged from `TDD-A2-REVIEW-A1C05-S3-001` §10) | S4 resolution — precise location | Status | Remaining disagreement  [QUOTED] |
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

| A2 finding | What Agent 2 found | S4.2 resolution — precise location | Status  [QUOTED] |
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

### 2.8 Agent 2's S4.2 conditions (`TDD-A2-REASSESS-A1C05-S4-2-001`, commit `c8e9f2a`) — every condition

Agent 2's reassessment is 708 lines, read in full, and it reviewed blob `7d03e1df…` rather than a branch tip. Its verdict is `PASS WITH CONDITIONS`; the contract text **passes**, seventeen findings are closed, and two conditions plus one advisory remain.

| # | Condition | What Agent 2 demonstrated | Where S4.3 resolves it  [QUOTED] |
|---|---|---|---|
| **`N-1`** | `PASS-BLOCKING` — `DV-22`'s whole-document scan is a keyword allowlist and can be defeated by a word on the line | The S4.1 preamble is exempted for containing `D-4` while assigning audio; the injection `D-4 note: Agent 1 owns the camera and audio cues…` yields **0 offenders** | **§13.1 `DV-22`** rewritten deny-by-default; §13.3 rows `N-1` and `N-1b` show the prefixed injection caught and a legitimate quotation still exempt; the regression suite asserts both |
| **`N-2`** | `PASS-BLOCKING` — two incompatible documents carry `TDD-A1-C05-SUCCESSOR-004.2` | Same path, two branches, `7d03e1df` (1,265 lines) vs `61ef03b4` (1,237 lines), 360 lines apart, and they disagree on what `TN-C-14` measures | **§2.9** — authority declared for `7d03e1df…`, the other **re-identified** `…-004.2-D` and declared superseded, the measure conflict resolved; recorded in the register and in `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |
| **`N-3`** | `ADVISORY` — S4.2 did not cite Agent 2's addendum, and recorded `D-1b` as *"adopted exactly"* though the addendum withdrew that ask | `e434dbe`, `ADDENDUM`, `PASS-CONDITION`, `PASS-BLOCKING`, `ADVISORY` all appear zero times in S4.2; D-1b was adopted although downgraded to `ADVISORY` | **§17** cites `ADDENDUM-A1` (`e434dbe`) and states the classification explicitly; §18.1 answers it |

**Nothing else was raised.** Agent 2's §7.3 sweep re-derived the totals (43 / 67 / 18 / 27), confirmed `DV-1`…`DV-27` contiguous, byte-compared the preserved clauses, re-parsed the §5.4 tallies and found no live placeholder. **S4.3 does not reopen any closed finding to answer these three.**

### 2.9 The duplicate `…-004.2` identity — decision, record, and the `TN-C-14` measure

Two files, same path, same declared response ID, different contracts. This section is the whole record: what the two artifacts are, which one the identity denotes, what happens to the other, and which measure of `TN-C-14` survives.

| | **Denoted by `TDD-A1-C05-SUCCESSOR-004.2`** | Re-identified: **`TDD-A1-C05-SUCCESSOR-004.2-D`** |
|---|---|---|
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | same path |
| Branch | `arena/3bc206a0-tdd` | `arena/c64fc525-tdd` |
| Commit (text / pinned) | **`a788f953256d208f3eb1310f3897924d007179b1`** | `99717e0` / `c800bf0` |
| Blob (text / pinned) | **`7d03e1df837493305831962f43882a1cd3496143`** | `eb774f5d6b281fd632333c39af95d7d66d047ed3` / `61ef03b4` |
| Lines | **1,265** | 1,237 |
| Provenance register | yes — `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md` | none; its §18.1 states the body would be recorded after commit |
| Independently reviewed | **yes — Agent 2, whole file** | no |
| `TN-C-14` measure | **one frame, shared axis** | `1/60` second, monotonic elapsed time |
| Status after S4.3 | **authoritative S4.2; baseline of S4.3** | **superseded, withdrawn as a C-05 baseline, not citable** |

**Why `7d03e1df…` is the artifact the identity denotes.** Not by seniority of drafting and not by assertion — by five recorded grounds:

1. **It is the artifact the TD's directive names as the reviewed object** (commit `a788f953…`, blob `7d03e1df837493305831962f43882a1cd3496143`), so the consolidation record already treats it as S4.2.
2. **It is the only S4.2 text that has been independently reviewed**, end to end, by Agent 2 at blob level. The other is unreviewed by anyone.
3. **It descends from the published S1→S4.1 series on this branch**, which is the branch of record for Agent 1's C-05 work; the other copy cites pre-publication hashes from that same series (`4692e97` for S4, `a6b4e22` for S3) and was produced in another agent's worktree.
4. **It carries a complete, verifiable provenance register**; the other has none, and its own §18.1 says the values "will be recorded after commit".
5. **Its `TN-C-14` measure is the one Agent 2 verified** — 400,000 legal schedules, maximised ratio 0.999772 < 1 — and the one D-1a was closed against.

**What is not claimed.** I do not assess the other copy's quality, do not treat it as a draft of this one, and **do not merge it**: 360 lines differ and a merge would produce a third artifact with no reviewer. I did not modify it, and I do not report its author's intent.

**Why re-identification rather than physical withdrawal.** Agent 2's closure condition allows any one of three: withdraw, re-identify, or declare. The file lives on `arena/c64fc525-tdd`, which this revision may read and may not write — no commit I can make on my own branch can delete bytes from another. So the closure taken here is **declaration plus re-identification**, recorded in three places with matching content: this section, the provenance register, and `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md`. **Residual, stated plainly:** line 3 of that file still reads `TDD-A1-C05-SUCCESSOR-004.2`. Closing that literally requires a commit on `arena/c64fc525-tdd`; if TD wants it, TD must direct it, because I will not write to a branch I do not own.

**The `TN-C-14` measure: one frame on the shared axis, and why the alternative is rejected.** The two copies disagree on what the staleness bound measures. The shared-axis measure is authoritative — the one published in §4.4's clause, in `T-C05-64` and in the register — for four reasons, in order of weight:

1. **C-05 has exactly one time base.** `TN-C-10` and `INV-2` age revisions on the shared axis, and `C05-6.1` forbids reconciling quantities across clocks. A staleness bound in monotonic elapsed time would put a second time base inside the clause that uses the first, and the two are not comparable.
2. **A fixed real-time constant cannot entail the axis bound.** Nothing in C-05 fixes the ratio between monotonic time and axis advance. When the axis advances faster than real time — a long frame, a catch-up step, dilation above one — a consumer can satisfy a `1/60` second real-time cap while the rated value ages **more than one frame on the axis**, which is the quantity the requirement is about. The real-time cap is therefore neither necessary nor sufficient; the axis bound is both.
3. **No frame rate is normative anywhere in C-05**, and `1/60` second silently makes one normative — including in `T-C05-64`, where the assertion would become unmeasurable whenever the axis is paused.
4. **The axis measure is the one already closed.** Agent 2 brute-forced it over 400,000 schedules and closed D-1a against it. Adopting the other measure would reopen a closed finding without a defect to justify it.

**No reconciliation is attempted.** The two measures are not averaged, not made "configurable", and not both stated. One is the contract; the other is recorded as a rejected alternative in the provenance history, where a future reader can see it was considered.

---

### 2.10 TD's S4.3.1 finding — one reproducible `DV-22` false negative, reproduced and closed

TD accepted S4.3 as the baseline and demonstrated one further false negative in the check that S4.3 had already rewritten once. It is a defect in the checker's *logic*, not in the contract, and it is recorded here the way the earlier findings were: reproduced first, then closed, then tested.

| # | What TD demonstrated | Why S4.3's predicate accepted it | Where S4.3.1 resolves it |
|---|---|---|---|
| **`TD-1`** | the *"owns no audio, but owns audio cues"* form passed `DV-22` with **0 offenders** (verbatim in the block below) | `negated_in_clause()` took the **first** audio mention, split the line only on the statement separators (full stop, semicolon and the table cell boundary), found `owns no audio` in that clause, and stopped. The comma does not end a clause and the second assignment was never examined. | **§13.1 `DV-22`**, rewritten to evaluate **every mention**; demonstrated in §13.3.2 rows `TD-1`, `TD-2`, `TD-5`…`TD-5c`, and shipped as regression cases |

**Reproduced before it was fixed, on the published blob.** Run on `74546027…`, the four contradictory forms below all returned `scan offenders 0` — the exact failure TD reported, not a paraphrase of it:

```
Agent 1 owns no audio, but Agent 1 owns audio cues for the player.   -> 0 offenders  (missed)
Agent 1 owns no audio. Agent 1 owns audio cues.                      -> 0 offenders  (missed)
Agent 1 owns no audio; Agent 1 owns audio cues; Agent 1 owns audio banks.  -> 0 offenders  (missed)
Agent 1 has no C-05 audio responsibility and owns audio cues.        -> 0 offenders  (missed)
```

**What the correction does, and what it deliberately does not do.** It does not add a list of forbidden words or a list of permitted ones. For each audio mention in a non-exempt line it asks a structural question: *does a negative construction cover this mention, and if not, which agent governs it?* A negation covers only the mention inside it — `no C-05 audio` covers the audio token it contains and nothing else, so a later `owns audio cues` is judged on its own. Attribution is read from the nearest agent reference before the mention in the same segment, or — for the reversed word orders — from an explicit ownership construction after it: a passive *"are owned by"* naming the first agent, a possessive *"are the first agent's"*, or a colon followed by that agent's name. The three patterns are checked, but they are patterns of grammar, not a list of permitted sentences. Consequently a negation of a **different object** cannot cover audio either: *"owns no camera, but owns audio cues"* is an offender, and so is *"has no C-05 audio responsibility and owns audio cues"* — both are regression cases `TD-5b` and `TD-5c`.

**Nothing else in this revision moves.** `DV-24`'s truth-table is unchanged; the `N-2` identity declaration and the `TN-C-14` measure are unchanged; every closure from S4.2's six corrections stands. The one non-validator change is §18.3's stale final sentence (TD item 3).

---

### 2.11 TD's S4.3.2 finding — a second false-negative class, reproduced and closed

TD accepted S4.3.1's fix and then read the predicate rather than testing it, which is where this class came from: `NEG_BEFORE` treated *any* `no` within 28 characters of `audio` as a denial of ownership. A denial of *difficulty*, *objection* or *restriction* is the opposite: it presupposes that the agent does own the thing and denies only that it is a burden.

**Reproduced before it was fixed, on the published S4.3.1 blob.** These lines were injected into the live ownership area and accepted:

```
Agent 1 has no problem owning audio cues.                                -> 0 offenders  (accepted)
Agent 1 has no objection to owning audio cues.                           -> 0 offenders  (accepted)
Agent 1 has no restriction on owning audio cues.                         -> 0 offenders  (accepted)
```

**Two of TD's five cases were already caught, and this is recorded rather than claimed as a fix.** *"no difficulty taking responsibility for audio cues"* and the composite form (*"no objection to owning"* followed by a second, plainly positive assignment) both failed `DV-22` on S4.3.1 — the first because the phrase exceeded the 28-character window before `audio`, the second because the *second* mention was positive. They are kept as regression cases (`TD-9`, `TD-11`) but they are not evidence for this correction, and §13.3.3 marks them as such.

| # | What TD demonstrated | Why S4.3.1 accepted it | Where S4.3.2 resolves it |
|---|---|---|---|
| **`TD-6`** | `no problem owning audio cues` accepted as a denial | `NEG_BEFORE` matched `no … audio` with nothing but a 28-character window between them | **§13.1 `DV-22`** — bounded denial constructions; §13.3.3 rows `TD-6`…`TD-11`; regression cases |

**What the correction does.** It replaces the broad window with an explicit, semantically bounded set of denials. The set is a *whitelist of denials*, which is the opposite of a keyword exemption: a line that matches none of them is not exempt, it is a positive statement, and if an agent reference governs the mention it is an offender. The deny-by-default default is untouched; only the recognition of "this is a denial" is now grammatical and bounded.

**What it also repaired.** Two genuine denials were being *rejected* by S4.3.1 — `Agent 1 does not own any audio cues.` and `Agent 1 is not responsible for audio cue selection.` — because neither contains `no`. Both now pass, as `TD-15` and `TD-16`. A check that rejects correct denials pushes authors toward the very wordings that caused the first defect, so this is part of the same correction rather than a separate change.

**Nothing else in that revision moved.** `DV-24`, the `N-2` identity declaration, the `TN-C-14` measure and every closure from S4.2 and S4.3 stand.

### 2.12 TD's S4.3.3 finding — a later denial does not answer an earlier assertion

**Condition 1 reproduced, before anything was changed.** The published verification ran against the exact commit, not a branch tip and not a stale copy: `git archive b754deb3 | tar -x -C /tmp/verify_s432` produced a 58-file tree, and in it `python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_2.md` reported **27/27 checks passed** with `DV-22` at **110 mentions** and **0 offenders**, and `python3 docs/validation/test_dv_c05_regressions.py` reported **44/44 regression cases behaved as required**. Working-tree and `HEAD:` blobs match for all three files, and there is one worktree. Nothing in this revision rests on a figure that was not reproduced.

**Condition 2 found a class the reproduction could not.** `NEG_AFTER` matched a denial *after* a mention and exempted that mention, whoever the sentence said owned the cues and whichever agent the denial named. Ten probes were injected into the live ownership area of the published blob; four were accepted that must fail:

```
Agent 1 owns audio cues, but those cues are not assigned to Agent 1.    -> 0 offenders  (accepted — required FAIL)
Agent 1 owns audio, which is not a responsibility assigned to Agent 2.  -> 0 offenders  (accepted — required FAIL)
Agent 1 owns audio cues and those cues are not owned by Agent 2.        -> 0 offenders  (accepted — required FAIL)
Agent 1 owns audio cues which are not owned by anyone.                  -> 0 offenders  (accepted — required FAIL)
```

Three further probes — a denial in a following sentence, a denial *before* a positive assertion, and a semicolon-joined denial naming Agent 2 — were already caught, and the four must-pass denials (`has no C-05 audio responsibility`, `does not own audio`, `Audio is not owned by Agent 1`, `Audio is not a responsibility of Agent 1`) passed. **So the defect is exactly the reversed order across a clause boundary, and it is not a general failure of denial recognition** — which is the distinction TD required this revision to preserve.

**Why it happened.** `negated_mention()` returned `True` if any `NEG_AFTER` pattern's span covered the mention's position. The pattern began at `audio` and allowed up to 40 characters before `is not owned` — commas, conjunctions and relative pronouns included. A sentence that asserted ownership in its first clause and denied something else in its second was therefore read as a denial of the first clause.

**What the correction does, in two rules.** A trailing denial now counts only when (i) it sits in the mention's own clause and phrase — the gap may not cross a comma, semicolon, sentence end, em or en dash, or a conjunction or relative pronoun — and (ii) it names the first agent or names nobody, with the agent read through the rest of the clause so that *"not owned by Agent 2"* is Agent 2's denial. **Both rules narrow the denial, not the mention**: `NEG_BEFORE` is untouched, no keyword was added to a flag list, and the check still accepts a line that genuinely denies that ownership.

**Measured before it was written, not after.** Instrumenting the validator over the S4.3.2 text showed that **0 of the 110 audio mentions were accepted only by `NEG_AFTER`** — every mention that passed had a `NEG_BEFORE` denial, a non-first agent, or an exempt location. The tightening could therefore be made without changing a single verdict on the document, which is the evidence that it is narrow rather than a blunt restatement of the check.

**A provenance defect found while doing this, and recorded rather than papered over.** §13.1's `DV-22` result cell on the published blob states *exempt lines 229 (fenced 157) … audio mentions evaluated 93*. That blob's actual output is *exempt lines 234 (fenced 162) … audio mentions evaluated 110*. The S4.3.2 text is preserved byte-identical and its cell is not edited; §0.7.3 row 3 records the discrepancy, and this revision reports the computed figures for its own text.

**Nothing else in that revision moved.** `DV-24`, `NEG_BEFORE`, the `N-2` identity declaration, the `TN-C-14` measure and every closure from S4.2, S4.3 and S4.3.2 stand.

### 2.13 TD's S4.3.4 finding — an unnamed denial is not evidence of non-ownership

**Both conditions reproduced on the published S4.3.3 blob before anything was changed**, by loading that commit's validator and asking it about one line at a time:

```
Agent 1 owns audio cues that are not owned.                          -> 0 offenders  (accepted — required FAIL)
Agent 1 owns audio cues that are not claimed by the team.            -> 0 offenders  (accepted — required FAIL)
Agent 1 owns audio cues that are not owned by anyone.                -> 0 offenders  (accepted — required FAIL)
Audio cues are not owned by anyone and are owned by Agent 1.         -> 0 offenders  (accepted — required FAIL)
Agent 1's audio cues are not owned by anyone.                        -> 0 offenders  (accepted — required FAIL)
```

The first is TD's condition A verbatim. The second is the same defect with the denial's object spelled out. The third is the interaction TD's condition B names: the same sentence, but with the relative clause opened by `that` instead of `which` — S4.3.3 rejected the `which` form and accepted the `that` form, so the boundary, not the grammar, was deciding the verdict. The last two are the same hole seen from the universal side.

**Why it happened, exactly.** `negated_mention()` ended with `if not named or named[0] == '1': return True`. The first disjunct meant *"no agent is named, so treat the denial as covering Agent 1"*. That is an absence-of-evidence test: a denial that names nobody does not establish that the first agent is excluded, it merely fails to name him. And `_NOT_CROSS` listed `which`, `who` and `whose` as phrase boundaries but not `that`, so a denial inside a defining relative clause could still be read as spanning the assertion the clause modifies.

**What the correction does.** Three changes, all inside the trailing-denial branch:
1. **the unnamed case is gone.** A trailing denial counts only if it names the first agent, or if it names nobody **and** carries an explicit universal term (`nobody`, `no one`, `anyone`);
2. **the universal term must genuinely exclude the first agent** — if the same clause also asserts that he owns the cues (an ownership phrase naming him, a possessive form, or a colon form), the universal denial is refused, because the sentence contradicts it;
3. **`that` is a phrase boundary**, so a denial cannot reach back across a relative clause.

**What did not change, and was checked rather than assumed.** `NEG_BEFORE` is untouched: *owns no cue*, *has no C-05 audio responsibility*, *does not own*, *has no responsibility for cue selection*, *has no authority over cue selection* and *owns none of the* — each with the first agent as subject — all still pass. The named reversed form still passes (`Audio cues are not owned by Agent 1`), and a genuine universal exclusion that does exclude the first agent still passes (`Agent 1 reported that audio cues are not owned by anyone`, where the assertion names no owner). **The full 56-case suite from S4.3.3 passes unchanged under the new predicate** — no earlier case moved — and the document's own 123 audio mentions are unaffected, because none of them depends on a trailing denial (§0.7.4).

**One judgement recorded rather than hidden.** The *possessive* form of the universal case — the first agent's name in the possessive, followed by a universal denial of ownership of the same cues — is now an **offender** (`TD-41`). The possessive asserts that the cues are his at the same time as the sentence denies that anyone owns them; under TD's own test — *"where the wording genuinely excludes Agent 1"* — it does not, and deny-by-default applies.

### 2.14 TD's S4.3.5 finding — one miscounted suite figure, and the audit that closes the class

**TD's finding is exact and it is a drafting error, not a predicate error.** The Scope line of S4.3.4 read *"The regression suite grows from **56** to **74** cases"*. The suite has **67**: 56 cases from S4.3.3 plus the eleven added at S4.3.4 (`TD-31`…`TD-41`). Four independent measurements agree, and all four were re-run for this revision:

| Measurement | Command | Value |
|---|---|---|
| Cases the runner runs | `python3 docs/validation/test_dv_c05_regressions.py` | **120 PASS lines**, `67/67 regression cases behaved as required` |
| Cases the commit added | `git diff 40d29cc 90971e0 -- docs/validation/test_dv_c05_regressions.py` | **+11** `case(` lines, **0** removed — 56 + 11 = 67 |
| Case ids the validator counts | `DV-2` on this document | **67 distinct case ids**, none missing, none extra |
| Cases the register records | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_4_PROVENANCE.md` | **67/67** |

**How the figure got in.** S4.3.4's §0.7.4 was drafted with a row that described the suite growth as part of the change list; that row was rewritten during the build, and the number it left behind in the front matter was never reconciled with the runner's output. No check compares a **front-matter** figure with an executed test count: `DV-2` counts case ids in §11/§12, `DV-6` checks the 18 suites, and neither reads the Scope line. That is the same class of defect as the under-reported `DV-22` cell recorded at S4.3.3 (§0.7.3 row 3) — a stated number drifting from a computed one — and it is recorded here in the same way rather than quietly overwritten.

**Every suite-count claim in the document, audited.** TD asked for the complete document, not just the corrected line. This is the whole set:

| # | Where | Claim | Verified value | Verdict |
|---|---|---|---|---|
| 1 | Front matter — Scope, as published in S4.3.4 | *"grows from 56 to 74 cases"* | **67** | **wrong — corrected in this revision's Scope line** |
| 2 | §0.7.1 row 2 | suite grew 18 → **30** at S4.3.1 | S4.3.1 register records **30/30** | correct |
| 3 | §0.7.2 row 2 | suite grew 30 → **44** at S4.3.2 | S4.3.2 register records **44/44** | correct |
| 4 | §0.7.3 row 2 | suite grew 44 → **56** at S4.3.3 | S4.3.3 register records **56/56** | correct |
| 5 | §0.7.3 row 2 | twelve cases added at S4.3.3 (nine must-fail, three must-pass) | `TD-19`…`TD-30` — twelve | correct |
| 6 | §0.7.4 and §13.3.5 | eleven cases added at S4.3.4 (`TD-31`…`TD-41`) | `git diff` — eleven, none removed | correct |
| 7 | §2.13 and §13.3.5 | *"the full 56-case suite from S4.3.3 passes unchanged"* | 56 at `40d29cc` | correct |
| 8 | §13 introduction | *"plus **one hundred and twenty** regression cases on the checker itself"* | 120 | correct |
| 9 | §13 command block | `# 120/120` | 120 PASS lines | correct |
| 10 | §17, instrument regression suite row | **120 cases**, **120/120 behaving as required** | 120 | correct |
| 11 | §17, acceptance-test row | 27 document checks and **120** instrument regression cases run | 27 and 120 | correct |
| 12 | §0.7.8, closing sentence | *"the instrument suite is **120** cases (106 + 14 new)"* | 120 | correct — 106 carried forward plus `TD-81`…`TD-94` |
| 13 | §13.1, the three widened rows | `146` mentions, **`10`** pairs, `7` cell-count claims, `8` owner checks | printed by the run | correct — **re-measured from the finished text**, and this is the row S4.3.7 got wrong: for *its* text it stated `8` where the runner printed `9` (Agent 2's `MINOR-1`, §2.23). This document's own text prints `10` |
| 14 | §13.3.8, the tallies paragraph | S4.3.7 **26/27**, S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27** | same | correct — each predecessor blob was re-run through the S4.3.8 checker and its tally is **unchanged**, the one failure being `DV-27` (S4.2 also fails `DV-22`/`DV-24`) |

**The coincidence that produced S4.3.5 is gone, and the audit keeps it gone.** At S4.3.5 the instrument suite had **67** cases and the proposed acceptance catalogue had **67** cases (`T-C05-01`…`T-C05-67`) — two different populations with the same figure, which is how a stale count can survive a review. At S4.3.6 the suite is **86** and the catalogue is still **67**, every one of which is `PROPOSED / NOT RUN`. The audit rows above are re-derived, never patched: rows 8, 9, 10, 11 and 12 all now read 86, and the two figures can no longer be confused. The 67 instrument regression cases are a different set: they test the checker, not the contract, and they are the only 67 in this document that actually ran. Row 11 above states both on purpose, because the coincidence is exactly the kind of thing a reviewer should not have to guess at.

**What S4.3.5 did not do, carried forward as history.** It did not change the predicate, the contract, the suite or the register mechanism, and it did not add a check. A check that compared front-matter figures with test counts would be a new instrument, and TD's directive for this revision is a narrowing: fix the number, audit the class, and change nothing else. The audit is therefore a **recorded table**, reviewed by eye, not a guarantee enforced by code — and that limitation is stated rather than implied.

### 2.15 TD's S4.3.6 item 1 — `DV-22`'s attribution (Agent 2's `MAJOR-1`), reproduced and closed

**Agent 2's two counterexamples reproduce on the published blob, exactly as reported.** Run on `baa31db`'s validator, with the line injected into the live ownership area immediately before §9, both scored `0 offenders`:

```
Agent 1, unlike Agent 2, owns the audio cues.    -> 0 offenders  (accepted — required FAIL)
The first agent owns the audio cues.             -> 0 offenders  (accepted — required FAIL)
```

**Root cause, in one sentence each.** `AGENT_REF` recognised only the literal `Agent <digit>` forms, so the document's own synonym — used seventeen times in this file, including to state the `DV-22` rule itself — matched nothing and no attribution was made; and the attribution rule took *the nearest reference before the mention* unconditionally, so in a contrastive `unlike` sentence it took the foil inside the contrastive clause and read the sentence backwards.

**The correction, and where it deliberately departs from the recipe.** Two parts as Agent 2 specified — the synonym read from a **named group**, and contrastive foils dropped before the subject is chosen — plus two adjustments this revision measured and made:

| Part | Implementation | Why |
|---|---|---|
| synonym | `AGENT_REF` gains an alternation for `the first agent`, read through `agent_of()`: the two alternatives are structurally different, so the agent is taken from a **named group** and never from a positional one | a bare alternative leaves `group(1)` as `None`, so `group(1) == '1'` never fires and the escape survives — Agent 2 measured that trap, and so did this revision before choosing the named group |
| foil | a reference whose immediately preceding text ends with `unlike`, `as opposed to`, `rather than` or `but not` is not the subject | `unlike Agent 2` names the party the subject is *contrasted with* |
| **`whereas` (departure)** | **not treated as a foil** | it introduces a clause whose subject is the reference that follows it. Probe `C7` — a `whereas` clause whose subject is the first agent — must **fail**, and dropping that reference makes it pass. Measured, not assumed |
| **object negation (addition)** | `, not the audio` joins the bounded denial set | once `the first agent` is attributable, *"The first agent owns the camera, not the audio cues"* would have become a **new false positive**. It is a genuine denial and must pass (probe `C11`) |

**Three-population evidence, which is the standard Agent 2 set and the one this revision holds itself to:**

| Population | Result |
|---|---|
| the clean S4.3.5 document | **27/27**, `DV-22` **0 offenders**, **132** mentions — unchanged from S4.3.5 |
| the two escapes | `TD-42` **FAIL**, `TD-43` **FAIL** (both were `PASS` under the S4.3.5 predicate — §13.3.6) |
| the 67 pre-existing regression cases | **67/67**, zero expectation mismatches — no collateral damage |

**A false positive the correction also fixes, recorded because it is evidence the rule was wrong in both directions.** `TD-47` — *"Agent 2, unlike Agent 1, owns the audio cues"* — is **Agent 2's** assignment and must pass. Under the S4.3.5 predicate it **failed**, because the nearest reference was the foil `Agent 1`. The corrected predicate passes it. `TD-48`…`TD-50` keep every genuine denial passing, and `TD-51` pins the `whereas` decision.

**What is not claimed.** `DV-22` remains a **predicate over wording**, not a parser: it recognises the phrasings and agents this document uses and the dialects its reviewers published. §13.3.6's table is the whole of the evidence, and the standing limitation is unchanged — a dialect nobody has written yet may still escape, which is why every round is closed by a **published probe** and a permanent case.

### 2.16 TD's S4.3.6 item 2 — `DV-24`: three false negatives found and closed, and Agent 3's two left open

**Agent 3's exact counterexamples could not be obtained** — the named review is absent from every ref and all 76 commits (§0.9), and I will not invent replacements for it. **Its finding therefore stays `OPEN — ARTIFACT ABSENT`.** What follows is this revision's own probing of the same instrument, and it found three genuine false negatives on the published blob.

**The three, reproduced on `baa31db`'s validator** (injected into live prose, each document scoring a clean `27/27`):

```
Counts: declared: 6, observed: 5.        -> DV-24 PASS  (accepted — required FAIL)
Counts: 6 declared / and 5 observed.     -> DV-24 PASS  (accepted — required FAIL)   [pair wrapped across a line break]
It said 6 declared. Then 5 observed.     -> DV-24 PASS  (accepted — required FAIL)
```

**Why each escaped, precisely.** The check read the pair only when the **number came first** (`6 declared`), so a label followed by punctuation (`declared: 6`) was invisible; its separator class excluded `.`, so a pair split by a sentence break never joined; and it scanned **one line at a time**, so a restatement wrapped across a line break was never seen at all. The check's own comment claimed *"every pair … on every non-exempt line"*, and the first two forms were not on that list at all.

**The correction.** `DECL_PAREN` now accepts `[\s:(]{0,4}` after the label, so `declared: 6` and `declared 6` both read; the separator class in `DECL_OBS` admits `.`, so a sentence break no longer hides a pair; and the scan runs **per line and over each adjacent pair of non-exempt lines**, so a wrapped restatement is caught. The pair is still read as `(declared, observed)` and compared with the computed `(7, 5)`; the digit-exclusion guard that stops a second pair hiding behind a first is unchanged.

**Effect on the clean document:** `DV-24` now reads **18** pairs instead of 6 — the twelve additional reads are adjacent-line windows on lines that carry no pair, and **0 disagree** with the computed pair. The three new cases are `TD-52`…`TD-54`; the control `TD-55` puts the **correct** pair in all three new forms and must pass.

**What is not claimed.** This closes three forms, on my authority and my probes. **It does not close Agent 3's finding**, whose probes I have not seen; when the artifact appears, its two reproductions must be run against this validator and added as cases before the finding is called closed.

### 2.17 TD's S4.3.6 item 3 — the `DV-11` enforcement gap, reconciled against three sources

TD asked for a determination: **genuine validator defect, difference of interpretation, or already-covered condition.** The three sources disagree, so each is stated separately.

| Source | What it says | What this revision found |
|---|---|---|
| **the normative requirement**, §5.4 | *"For each obligation row: the token must be declared above; the token's row must be in the **allowed-row set** for that obligation's prefix — `TN-P` → {2}; `TN-C` → {5, 6}; `TN-R` → {2, 4}; `TN-A` → {8}; and the row's owner must match the token's agent."* Also: *"The counts in the last column are the cells `DV-11` actually finds, not hand tallies."* | the sentence is **precise and correct**; the instrument below it was weaker than the sentence |
| **the current predicate** at `baa31db` | declared-row parse reads **only the first number or range** in the cell; the mapping test is an **intersection** (`decl[tok] & allowed[pref]`); the §5.4 cell counts are **never read** | **three genuine gaps**, all reproduced below |
| **Agent 2's independent reimplementation** | *"Re-implemented the allowed-row rule independently: **0 failures**"* | **consistent with this finding, not contradictory.** Agent 2 reimplemented the rule as it is *stated* (subset over the declared rows) and got 0 failures on a **correct document** — which is exactly what a correct document should give. A correct document cannot distinguish a subset rule from an intersection rule; only a *wrong* document can, and Agent 2 did not mutate this table |

**The three gaps, each reproduced on the published blob** (mutations of §5.4; the document otherwise scores `27/27`):

| Probe | Mutation | `DV-11` at `baa31db` | Required |
|---|---|---|---|
| `A1-P4` | `producer owner` declared as **rows 2 and 5** | **PASS** — the declaration was parsed as `{2}`, and row 5 was never seen | FAIL |
| `A1-P5` | `producer owner` declared as **rows 2–5** | **PASS** — `{2,…,5} ∩ {2} ≠ ∅` was enough | FAIL |
| `A1-P6` | the §5.4 cell count changed from **23** to **22** (`TN-R` 4 → 3) | **PASS** — the hand-restated count was never compared | FAIL |

**The correction, mapped one-to-one to the normative sentence.** Every number and range in the declaration cell is parsed and unioned (`rows 2 and 5` → `{2, 5}`); the mapping test becomes a **subset** test (`decl[tok] <= allowed[prefix]`), which is what *"the token's row must be in the allowed-row set"* means; and the §5.4 `Used by` column — the total and every per-prefix breakdown — is compared with the instrument's own counts. On the clean document the check now reports **7 declared / 5 observed tokens, 43 cells, 7 cell-count claims checked, 0 failures**.

**On the third clause — "the row's owner must match the token's agent" — the determination is *already covered*, and this is the one place the three sources genuinely differ in interpretation.** The allowed-row sets are **row-specific per prefix**, so a token whose declared row belongs to the wrong agent cannot survive the subset test: row 3 (types), row 7 (Agent 2, outside C-05) and row 8 (arbitration) are each outside some prefix's allowed set, and the only token that spans two rows is `each consumer` (rows 5–6), whose agent is *per side by definition* and therefore cannot be checked against a single owner. `TD-60` makes this concrete: declaring the C-05-consumer token as **row 7** — Agent 2's *own* agent, wrong *row* — now fails on the three `TN-C` cells that use it. **The owner clause is therefore enforced through the row, not through a separate owner map**, and no normative weakening is involved.

**What remains open.** **Agent 3's "narrower `DV-11` enforcement gap" is `OPEN — ARTIFACT ABSENT`.** I have not seen it and cannot say whether it is one of the three above, a fourth gap, or an interpretation difference. If it is a fourth gap, this validator does not close it, and the finding should stay open until it is reproduced against the corrected instrument.

### 2.18 TD's S4.3.7 item A — `DV-22`: three reports, two defects I could reproduce, and one I could not

**The three reports, kept apart.** TD's directive lists Agent 2's `MAJOR-1` (possessive synonym), Agent 2's `MAJOR-2` (foil window) and "Agent 3's independently reported positive-ownership escape", and instructs me to establish whether the third is the same defect as the others **rather than merging distinct defects because they share a subject**.

| Report [QUOTED] | Artifact | Reproduced on `034d091`? | Assessment |
|---|---|---|---|
| Agent 2 `MAJOR-1` — `The audio cues are the first agent's.` | read, §3.6 of the review | **yes**, `DV-22 PASS`, 0 offenders | **DISTINCT** — a *lexicon* defect: `AGENT_REF` learned the synonym, `FORWARD_OWNER` still spelled `agent 1` literally, so the synonym worked as a subject and not as a possessor |
| Agent 2 `MAJOR-2` — a foil longer than the window | read, §3.6 | **yes**, `DV-22 PASS`, 0 offenders | **DISTINCT** — a *distance* defect: the foil test sliced a fixed 32 characters before the reference, so a subordinate clause pushed the marker out of the window and the foil became the subject |
| Agent 3 — "positive-ownership escape" | **not in this repository** (§0.9.1) | **cannot be attempted** | **UNPAIRABLE.** I will not assert it is `MAJOR-1`, `MAJOR-2`, one of the forms below, or anything else. It stays `OPEN — ARTIFACT ABSENT` |

**Why `MAJOR-1` and `MAJOR-2` are distinct despite touching the same predicate.** They fail for opposite reasons: `MAJOR-1` is a form the predicate never *recognised*, `MAJOR-2` is a form it recognised and then *mis-assigned*. Their fixes are independent — I applied them separately and each test fails for exactly one of them (`TD-61` fails on the possessor alone; `TD-62` has a literal `Agent 1` subject and fails on the foil alone).

**What I did about the unpaired report: I probed the class rather than guessing the example.** Agent 2's `MAJOR-1` is one member of a family — positive-ownership constructions in which the first agent is named as the owner. A matrix of fifteen such forms, each injected into live prose, produced **seven further escapes** at `034d091`, all with a clean `27/27`:

| Probe [QUOTED] | Form | `034d091` | Now |
|---|---|---|---|
| `P1` | `The audio cues belong to the first agent.` | PASS | **FAIL** (`TD-63`) |
| `P2` | `The audio cues are selected by the first agent.` | PASS | **FAIL** |
| `P3` | `Audio cue selection ownership is the first agent's.` | PASS | **FAIL** |
| `P5` | `The audio cue's owner is the first agent.` | PASS | **FAIL** (`TD-64`) |
| `P6` | `The audio cues are Agent 1 's.` | PASS | **FAIL** |
| `P8` | `The audio cues, whose owner is the first agent, are selected per frame.` | PASS | **FAIL** |
| `P9` | `The audio cues -- the first agent.` | PASS | **FAIL** (`TD-65`) |

**These are this revision's probes, not Agent 3's example**, and are labelled `P1`…`P9` to keep that distinction visible. Whether Agent 3's escape is among them is **unknown and not claimed**.

**Two forms remain out of scope, recorded rather than hidden.** `P10` — *"Consider the audio cues. The first agent."* — is not an ownership construction: the second sentence has no predicate. Teaching the checker to attribute across a sentence break would re-open the reverse defect `TD-47` settles, so it is deliberately not caught. A fragment joined by an em dash is caught (`TD-65`); a fragment across a full stop is not.

**The fix, and the two false positives it created and I had to take back.** The agent-1 name is now written once (`AGENT1`, `AGENT1_POSS`) and every attribution and denial path derives from it — the structural repair Agent 2 recommended in place of widening one lexicon. The foil is bound to the clause containing the reference. Widening the possessor immediately produced two **new** false positives, both caught by the control sweep before any test was written:

| Control [QUOTED] | Why it fired | Fix |
|---|---|---|
| `The audio cues do not belong to the first agent.` | the new `belongs to` form had no denial | a bounded denial construction for `does/do not belong to` (`TD-66`) |
| `The camera, rather than the audio cues, is owned by Agent 1.` | the mention is the **contrasted object**, and forward attribution still fired | `_mention_is_contrast`: a marker governs the mention only when it stands **directly before** it (`TD-67`) |

**Three-population evidence:**

| Population | Result |
|---|---|
| the clean S4.3.6 document | **27/27**, `DV-22` **0 offenders** (`TD-69`, `TD-78` controls) |
| 24 valid-denial and benign-co-occurrence controls | **0 false positives** — including `TD-70` (possessive denial), `TD-66` (`do not belong to`), `TD-67` (contrast object), `TD-68` (marker in the previous clause) |
| the seven escapes and both Agent 2 cases | **FAIL**, `TD-61`…`TD-65` and the §13.3.7 table |

### 2.19 TD's S4.3.7 item B — `DV-24`: the three-line wrap and the false join are two findings, one of which the old validator caused

**The reports overlap in one place and not the other.**

| Report [QUOTED] | Same defect? | Evidence |
|---|---|---|
| Agent 2 `MINOR-1` — "a three-line-wrapped pair escapes" | **the same defect**, reported twice | reproduced exactly: `6 declared` / `and then` / `5 observed` scored `DV-24 PASS` at `034d091`; the S4.3.6 scan joined **adjacent** pairs only |
| Agent 3 — "three-line-wrapped contradictions are missed" | **the same defect** as above | — |
| Agent 3 — "unrelated adjacent facts can be falsely joined" | **a distinct defect**, and the stronger of the two | **the S4.3.6 join already did it**: `- declared 6` followed by `- observed 5` was welded into a `(6, 5)` contradiction and the document **failed** for a pair no line stated. `TD-75` records it: `FAIL` under the S4.3.6 validator, `PASS` under this one |

**So the finding is not merely a risk created by widening the join — the existing join was already wrong at block boundaries.** That is why the fix is a guarded join rather than a wider one.

**The four guards**, each written because a control demanded it:

| Guard | Control it protects [QUOTED] |
|---|---|
| never across a block boundary — table row, heading, blockquote, list item, fence, blank | `TD-75` (list items) — the false join that already existed |
| never across a sentence terminator (`.` `!` `?` at the end of a line) | `TD-74` (two unrelated complete sentences), `TD-76` (two single-sided facts) |
| the next line must continue the sentence — lowercase, a digit, or a connective (`and`, `or`, `then`, `with`, `versus`, `of`, `in`, `for`, `per`, `the`, `each`) | `TD-74`; a new fact normally starts with a capital |
| the window may carry at most **one** `declared` and **one** `observed` label | two separate claims cannot be cross-paired into a contradiction that neither states |

**Coverage, one line to three:**

| Case | Lines | Verdict |
|---|---|---|
| `TD-52` (S4.3.6) | 1 | **FAIL** |
| `TD-53` (S4.3.6) | 2 | **FAIL** |
| `TD-71` | 3 | **FAIL** — was `PASS` |
| `TD-72` | 3, with an intervening continuation | **FAIL** — was `PASS` |
| `TD-73` | 3, correct pair | **PASS** (control) |
| `TD-74`–`TD-76` | adjacent but unrelated | **PASS** (controls) |

**One number falls and that is expected.** The document's assembled-window count drops from **24** to **8**: the guards reject windows that end a sentence, begin a block or carry a second pair, and those windows were never contradictions — the anchors still read **3/3** and no detection was lost, because every target form is proven by a case rather than by a window count. **A window count is a coverage indicator, not a score**, and this revision prefers a smaller honest number to a larger one that reports failures for text no line claims.

### 2.20 TD's S4.3.7 item C — `DV-11`: the owner column, and why `TD-60` could not test it

**The normative sentence has three clauses**, and S4.3.6 instrumented two:

> *"For each obligation row: the token must be declared above; the token's row must be in the allowed-row set for that obligation's prefix …; **and the row's owner must match the token's agent**."*

**`TD-60` cannot reach the third clause, and the reason is structural, not a bug in the test.** It declares `Agent 2, C-05 consumer` at **row 7**. Row 7 is *outside* `TN-C`'s allowed set `{5, 6}`, so the **allowed-row** test rejects it — under the S4.3.6 subset rule *and* under the older intersection rule, which is exactly why Agent 2 measured `FAIL` on both validators and TD reported it. The row-7 mutation also happens to have the correct owner (Agent 2), so nothing about ownership is being exercised. **`TD-60` is a valid assertion of the allowed-row rule and a weak discriminator for the owner rule** — Agent 2's `MINOR-2` and TD's observation are the same finding, and both are correct.

**The fix enforces the clause directly.** The eight row owners are declared and then **verified against §5.2's own words** at run time — if that table changes, `DV-11` fails rather than silently re-defining ownership. Each token's agent comes from §5.4's `Agent` column. For every declared row the check requires `owner(row) ∩ agent(token) ≠ ∅`, which handles the two dual-owned cases honestly: row 1 and row 2 are owned by both agents, and `each consumer` declares rows 5 and 6 with both agents.

**The three cases TD asked for, and nothing weaker:**

| Case [QUOTED] | What it establishes | S4.3.6 | S4.3.7 |
|---|---|---|---|
| `TD-78` — the unmodified §5.4 table | **correct owner-column evidence** passes: eight owner checks, zero failures | PASS | **PASS** |
| `TD-77` — `Agent 2, C-05 consumer` declared at **row 5** | **incorrect owner-column evidence** is caught — and it is caught **only** by the owner rule: row 5 ∈ `{5, 6}`, so the subset test passes | **PASS** | **FAIL** |
| `TD-80` — the same token at **row 7** | the **allowed-row** rule still fires on its own, so the two rules are separately exercised rather than one standing in for the other | FAIL | **FAIL** |
| `TD-79` — `Agent 1, shared support` at row 2 | the owner rule is not over-strict: a dual-owned row inside `TN-R`'s `{2, 4}` stays legal | PASS | **PASS** |

**`TD-77` is the discriminator**: under the S4.3.6 validator the document passes, and under this one it fails with `'Agent 2, C-05 consumer' declares row 5, whose owner is 1, but the token's agent is 2`. A case that moves between validators for the stated reason is the only evidence that the new rule is doing the work — `TD-60` never moved.

**No normative weakening.** The rule is the sentence §5.4 already states; this revision supplies the instrument the sentence implied. **The contract text is unchanged**, and if TD considers the owner clause to mean something narrower than "the row's owner must match the token's agent", the sentence is the place to say so — not the validator.

### 2.21 TD's correction 1 — `DV-22` read a quantified denial as an assignment

**Agent 2's `CONDITION-1` reproduces exactly, and it is a defect S4.3.7 created.** All four forms below scored `DV-22 PASS` at S4.3.6 and `DV-22 FAIL` at S4.3.7 — that is, the `belongs to` widening turned valid denials into false alarms:

| Probe [QUOTED] | Form | S4.3.6 | S4.3.7 | S4.3.8 |
|---|---|---|---|---|
| `C1` | a `no`-quantified subject with `belongs to` (Agent 2's verbatim example) | PASS | **FAIL** | **PASS** (`TD-81`) |
| `C1b` | the same with an existential frame and the synonym | PASS | **FAIL** | **PASS** (`TD-82`) |
| `C1c` | `none of the` + plural `belong to` + synonym | PASS | **FAIL** | **PASS** (`TD-83`) |
| `C1d` | a `no`-quantified subject with `is owned by` | PASS | **FAIL** | **PASS** (`TD-85`) |

**Root cause, precisely.** Every denial construction in the set negates a **verb** (`does not belong to`, `does not own`) or quantifies a **possessed object** (`no ownership of audio`). A **determiner-quantified subject** — *no audio cue*, *none of the audio cues* — denies possession without negating anything: the negative word sits on the subject, three to five words before the verb. The `belongs to` and `owner is` widenings added those verbs as *positive* attributors and taught only the verb-negated denial, so the quantified subject fell through to the positive path and the mention was attributed.

**The fix is a denial, not a new ownership pattern** — which is the distinction TD's boundary turns on. Three constructions are added, each spanning the mention so it denies *that* mention and no other:

| Construction | Covers |
|---|---|
| `no` / `none of the` … `audio` … `belongs to` <Agent 1> | `C1`, `C1b`, `C1c` |
| `no … audio … is/are owned by <Agent 1>` | `C1d` |
| `no … audio … is/are <Agent 1>'s` | the same quantifier with the possessive |

**`C1d` and the possessive are this revision's own probes, labelled as such.** Agent 2 named three forms (all the `belong` verb); I checked whether the same quantifier also defeated the two other possession predicates the widening taught, and it did. They are the **same one-line rule** — a quantifier governing the mention — so they are fixed in the same change rather than left as a known gap, and each has its own case. **No positive-attribution pattern was touched**: the genuine forms still fail, which is the control that matters.

**Evidence that the repair did not buy precision with recall:**

| Control | Verdict |
|---|---|
| `TD-84` — a genuine `belongs to` assignment | **FAIL** (unchanged — the positive form is not weakened) |
| `TD-63`, `TD-64`, `TD-65` — the S4.3.7 ownership class | **FAIL** (unchanged) |
| `TD-61`, `TD-62` — Agent 2's `MAJOR-1` and `MAJOR-2` | **FAIL** (unchanged) |
| `TD-66`, `TD-67`, `TD-70` — the S4.3.7 denial and contrast controls | **PASS** (unchanged) |
| the clean document | **0 offenders** — the new denials never fire on prose that assigns ownership |

### 2.22 TD's correction 2 — the continuation gate cost every capitalised wrap

**Agent 2's `CONDITION-2` reproduces exactly, and the diagnosis of *why* it is redundant is correct.** S4.3.6 joined every adjacent pair unconditionally; S4.3.7 put both the two-line and the three-line window behind `_joinable`, whose `_CONT_START` requires the continuation to begin with a lowercase letter, a digit, or one of a fixed set of connectives. **A capitalised continuation therefore failed the gate**, and the table inverts exactly as Agent 2 predicted:

| Probe [QUOTED] | Wrap | S4.3.6 | S4.3.7 | S4.3.8 |
|---|---|---|---|---|
| `J1` | `6 declared` / `The audit shows 5 observed.` (the confirmed Counts example) | **FAIL** | PASS | **FAIL** (`TD-86`) |
| `J2` | `6 declared` / `Then 5 observed.` | **FAIL** | PASS | **FAIL** (`TD-87`) |
| `J3` | `6 declared` / `And 5 observed.` | **FAIL** | PASS | **FAIL** (`TD-88`) |
| `J4` | `6 declared` / `and 5 observed.` | FAIL | FAIL | **FAIL** (control, `TD-89`) |

**Why the gate is redundant for two lines, stated as the argument rather than as an assertion.** Three guards protect a join, and only the third is at issue:

1. **Block boundary** — a table row, heading, blockquote, list item, fence or blank line is never joined. This is what stops the false joins `TD-75` and its siblings record, and it is untouched.
2. **Sentence terminator** — a line ending in `.`, `!` or `?` ends its claim, so the next line is a new claim. This is what stops `TD-74`, `TD-76` and the two-sentence controls, and it is untouched.
3. **A single `declared` and a single `observed` label per window** — two separate claims cannot be cross-paired into a contradiction that neither states. **This is the guard Agent 2 called sufficient**, and for a two-line window it is: the window has exactly one clause to assemble, so the only way to produce a pair is to read the two labels that are actually there.

The continuation gate added a fourth, *lexical* condition — and that condition is the only one that can reject a genuine wrap, because a wrap may legitimately begin with a capital (`The tally reads …`, `Then …`, `And …`). It buys nothing on two lines and costs every capitalised continuation.

**The change is a removal, not an addition:** `_joinable(a, b, require_cont)` takes the gate as a parameter, `require_cont = (k == 2)` — set for the internal boundaries of a **three**-line window only. Nothing else in the join changed.

**False-join protections, re-verified case by case** (each one passes, and each is now a permanent case):

| Boundary | Case | Verdict |
|---|---|---|
| sentence terminator | `TD-74`, `TD-76` | **PASS** |
| list item | `TD-75` | **PASS** |
| heading | `TD-90` | **PASS** |
| blockquote | `TD-91` | **PASS** |
| table row | `TD-92` | **PASS** |
| fence | `TD-93` | **PASS** |
| correct pair across a capitalised wrap | `TD-94` | **PASS** |
| three-line wraps (S4.3.7's closures) | `TD-71`, `TD-72`, `TD-73` | **FAIL / FAIL / PASS** (unchanged) |

**One residual is recorded rather than hidden.** A **three**-line window still requires a continuation on each internal boundary, so a three-line wrap whose second line begins with a capital remains unread. That is deliberate: with two internal boundaries the false-join risk is materially higher, the case was not reported, and widening it would be the general-purpose expansion the directive forbids. It is a known, stated limit, not a claim of completeness.

### 2.23 TD's correction 3 (non-blocking) — the pair count was hand-written and drifted

**Agent 2's `MINOR-1` is correct and the number is theirs, not mine to argue with.** At `f1beb0c` the runner prints `pairs read 9`; S4.3.7's §13.1 and register both said **8** — and this document, once its own text was complete, prints **10**, because the prose written here adds a joinable window. Both figures are stated so the drift is visible rather than papered over.

**Why it happened, stated because the mechanism is the defect.** The count was measured while the document was still being written, and later text added a joinable window; the figure was never re-measured after that. That is precisely the failure §5.4 warns about — a hand-restated tally drifting from the value computed beside it — and it is the same class the S4.3.6 revision closed for the *cell counts* and that `DV-24` exists to police for the *declared/observed pair*. The instrument was right; the prose about the instrument was stale.

**The correction:** every occurrence of the pair count in this document and in the register now carries the value the runner prints, and §13.3.8 records the measurement rather than restating a remembered one. **The value this revision publishes is set by measurement, not by this paragraph** — §13.1 and §13.3.8 are re-measured from the finished text, and that is the reason the figure is quoted in both places rather than remembered in one.

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

Fifteen. `TN-C-01` … `TN-C-09` are S2's, corrected where Agent 2's findings require; `TN-C-10` … `TN-C-13` are S3's; `TN-C-14` and `TN-C-15` are new in S4 (`D-1`, `D-4`). **Each obligation is implemented by each consuming agent in its own code** — Agent 1 for defence **selection**, dodge, camera response and framing; Agent 2 for AI reaction, **audio cue selection (the only C-05 audio responsibility — Agent 1 has no C-05 audio responsibility)**, montage trigger and VFX timing. **Agent 1 has no C-05 audio responsibility** (`C05-7.2` row 5; `TN-C-15`; `DV-22`). Tests `PROPOSED / NOT RUN`.

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

Twenty-seven checks on **this document's text**, plus **one hundred and twenty** regression cases on the checker itself, run with `python3`. **`DV-22` and `DV-24` were rewritten at S4.3 from allow-by-default to deny-by-default, `DV-22` was rewritten again at S4.3.1 to judge each audio mention separately, and again at S4.3.2 to accept only bounded denials, and again at S4.3.3 to scope a trailing denial to its own clause and agent, and again at S4.3.4 to require a trailing denial to name the first agent or a genuine universal exclusion**; their rows are tagged, and §13.3.1–§13.3.5 show what each previous predicate missed. They are not tests of contract behaviour, and passing them says nothing about whether any obligation holds. Every result below is the actual output of the check listed. **The checker is now in the repository** — `docs/validation/dv_c05.py` — so a reviewer can re-run it instead of trusting this table, which is itself a correction: S4.1 recorded the checker at `/home/user/dv4.py`, outside the repository, where no reviewer could reach it.

Commands for all checks — the document checks and the instrument's own regression cases:

```
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md     # 27/27
python3 docs/validation/test_dv_c05_regressions.py                              # 120/120
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
| **DV-11** | `[CORRECTED at S4.3.8 — TD-81]` `[EXTENDED at S4.3.7 — TD-77]` `[WIDENED at S4.3.6 — TD-56]` parse §5.4's token table **with its row mapping** — **every** number and range a declaration names, not the first — and for each obligation test the token's declared row set against the prefix's allowed-row set (`TN-P`→{2}, `TN-C`→{5,6}, `TN-R`→{2,4}, `TN-A`→{8}) as a **subset**, not an intersection; compare §5.4's hand-stated cell counts, total and per prefix, with the instrument's own; and require **every declared row's owner, read from §5.2 and verified against it at run time, to be the agent §5.4 names for that token**; report declared and observed separately | **PASS** — 7 declared / 5 observed tokens, 43 cells; declared-unused ['Agent 2, in its own systems', 'contract layer, owner pending TD-12']; failures []; cell-count claims 7 checked, failures []; owner checks 8 (map verified True), failures [] |
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
| **DV-22** `[REWRITTEN at S4.3 — N-1; at S4.3.1 — TD-1; at S4.3.2 — TD-6; at S4.3.3 — TD-19; at S4.3.4 — TD-31; at S4.3.6 — TD-42; at S4.3.7 — TD-61]` | row 5 clean of the audio token; row 6 owns cue selection; `TN-C-15` implementer; **§8 preamble clean**; **whole-document scan, deny-by-default, per mention**: outside exempt regions, **every** audio mention is judged on its own — it is accepted only if a **bounded denial construction** covers *that* mention — a negated verb, a negated object, a **determiner-quantified subject** (`no … audio … belongs to`), or a universal exclusion — a denial of ownership or responsibility, not merely `no` before `audio`; the six templates are listed in §0.7.2 row 1 and in the validator's `NEG_BEFORE`, and a denial that **follows** the mention counts only when it sits in the mention's own clause and phrase (no comma, semicolon, sentence end, dash, conjunction or relative pronoun between them) and names the first agent, or names nobody *only* as an explicit universal exclusion that genuinely excludes him (§13.3.4, §13.3.5) — or if the agent governing it is not the first agent (nearest reference before it in the segment — **skipping a contrastive foil** introduced by `unlike`, `as opposed to`, `rather than` or `but not` — the marker being read **in the clause the reference sits in**, not within a fixed character window — and reading `the first agent` as the first agent through a named group — or an explicit ownership construction after it: `are owned by`, `are …'s`, `: Agent 1`, `belongs to`, `owner is`, dash-attributed — every one of them deriving the agent-1 name from a single token so the synonym works in each). No keyword allowlist exists, and the live ownership sections may not be exempted at all | **PASS** — row 5 audio removed True; row 6 owns audio True; TN-C-15 present True, implementer Agent 2, C-05 consumer; §8 preamble clean True; exempt lines 343 (fenced 201, quoted table 139, marked block 3); live sections unexempted True; audio mentions evaluated 146; scan offenders 0 |
| **DV-23** | normative sections use "fixed for the instance's lifetime"; the rejected phrase appears only inside quotation marks; `TN-P-19`, `TN-P-04`, T-C05-66 present | **PASS** — identity 'fixed for the instance's lifetime' in normative sections 7; unquoted rejected phrase 0; TN-P-19 present; TN-P-04 names identity change; T-C05-66 present |
| **DV-24** `[CORRECTED at S4.3.8 — TD-86]` `[REWRITTEN at S4.3; extended at S4.3.6 — TD-52; guarded join at S4.3.7 — TD-71]` | deny-by-default over the **whole document**: every declared/observed pair — digits or number words, either statement order, **every** match on a line rather than the first, and **across runs of up to three non-exempt lines** so a wrapped restatement cannot hide, joined only where the run continues a sentence — **the continuation test applying to three-line windows only, because a two-line window is already protected by the block, sentence and single-pair guards** — and never across a block boundary, a sentence terminator or a second pair — must equal `DV-11`'s computed pair unless it sits in an exempt region (fenced block, `[QUOTED]` table, marked history block); the three anchor sites must still exist, so a site cannot be dropped to make the check pass (S4.2 also named a fourth, §18.1's `C9` line, which never resolved in any revision — a dead anchor that read three sites and reported nothing missing; it is dropped here rather than silently skipped) | **PASS** — computed 7 declared / 5 observed; anchor sites 3/3; pairs read 10, all equal; no pair outside an exempt region disagrees |
| **DV-25** | `TN-C-14` carries call-site scope, the one-frame maximum interval, the shared-axis measure, the frame-of-use refresh, re-pull-or-suppress, the derived bound and the message-only residual; `T-C05-64` carries A3's schedule, the worst-case placement, the measure assertion and the negative controls | **PASS** — TN-C-14 rules 7/7, missing []; T-C05-64 extensions 4/4, missing [] |
| **DV-26** | §3.6 does not assert the falsified premise; it states that the order **is** observable through a mid-frame pull; `PO-3` and `PO-5` both retained | **PASS** — falsified premise absent True; 'observable through a mid-frame pull' present True; PO-3 and PO-5 both retained True |
| **DV-27** `[WIDENED at S4.3]` | no placeholder token anywhere in the file; §17 records **both** pinned artifacts (S4.1 and S4.2) by exact commit and blob; the v4.3 provenance register is referenced in §17 and §18; the identity decision is recorded with the withdrawn identity `…-004.2-D`; Agent 2's addendum `e434dbe` is cited | **PASS** — placeholders found []; S4.1 and S4.2 commit+blob recorded in §17 True; provenance register referenced in §17 and §18 True; identity decision recorded with the withdrawn identity in §17 True; Agent 2's addendum cited in §17 True |

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
| **DV-22** (rewritten) | audio has exactly one owner **in all ownership prose**, §8's preamble included, with no keyword escape | **FAIL on S4.1** — `§8 preamble clean False` **and 5 scan offenders, one of them line 566, the preamble itself**; **FAIL on S3** with `row 5 audio removed False` | PASS |
| **DV-24** (rewritten) | every hand-restated declared/observed count in the whole document equals `DV-11`'s computed pair | **FAIL on S4.0** — 2 disagreeing pairs, `[(108, (7, 6)), (984, (6, 5))]`; **FAIL on S4.2** — 2 disagreeing historical pairs, `[(106, (7, 6)), (113, (6, 5))]`, because S4.2 states its correction record without marking it | PASS |
| **DV-25** (new) | the staleness bound is defined, measurable and derived | **FAIL on S4.1** — `TN-C-14 rules 0/7; T-C05-64 extensions 0/4` | PASS |
| **DV-26** (new) | `PO-3`'s rationale must not assert a premise `PO-5` falsifies | **FAIL on S4.1** — `falsified premise absent False; 'observable through a mid-frame pull' present False` | PASS |
| **DV-27** (widened) | no unfilled commit/blob placeholder; the pinned artifacts recorded; register and identity decision referenced | **FAIL on both S4.1 and S4.0**, on the provenance fields (v4.3 output below), and **FAIL on the S4.1 *reviewed blob*** on the placeholder tokens themselves (S4.2's output, retained below) | PASS |

**The DV-27 failures, verbatim.** The first block is **S4.2's recorded output** on the two reviewed blobs, kept here as history: the repository copies of S4.1 and S4.0 were later filled, so re-running on the tip copies no longer shows the placeholder tokens — that component is unchanged and its demonstration is S4.2's, not mine. The second block is the **v4.3 output on the tip files**, which fails them for the provenance fields instead. Both are quoted in fenced blocks, which `DV-27` strips before scanning, so an instrument's own output can neither satisfy nor trip its check:

```
$ python3 docs/validation/dv_c05.py /tmp/s41.md
DV-27 FAIL — placeholders found ['S41_COMMIT', 'S41_BLOB']; S4.1 commit+blob recorded in §17 False;
             provenance register referenced in §17 and §18 False

$ python3 docs/validation/dv_c05.py /tmp/s40.md
DV-27 FAIL — placeholders found ['PUB_COMMIT_PLACEHOLDER', 'PUB_BLOB_PLACEHOLDER', '_PLACEHOLDER']; ...
```
```
$ python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md
DV-27 FAIL — placeholders found []; S4.1 and S4.2 commit+blob recorded in §17 False; provenance register
             referenced in §17 and §18 False; identity decision recorded with the withdrawn identity in §17 False;
             Agent 2's addendum cited in §17 False

$ python3 docs/validation/test_dv_c05_regressions.py
PASS  keyword-prefixed injection is caught (this is the defect N-1 named)
      DV-22 expected FAIL, got FAIL  — S4.2 reported 0 offenders for exactly this line
PASS  injection inside a marked history block is exempt (narrow exemption still works)
      DV-22 expected PASS, got PASS
PASS  P4 second contradictory pair on the anchor line is caught
      DV-24 expected FAIL, got FAIL
...
120/120 regression cases behaved as required
```

### 13.3.1 The two instruments Agent 2 defeated, and the demonstrations that close them

An instrument is only closed when the *defect that defeated it* is shown failing it. For `DV-22` that required more than running it on S4.1: Agent 2 showed that the scan component had never caught anything, and produced a one-word bypass. The table below is that bypass and its closure; every row is a case in `docs/validation/test_dv_c05_regressions.py`, which any reviewer can run with `python3 docs/validation/test_dv_c05_regressions.py`.

| # [QUOTED] | Injected or probed text | `DV-22`/`DV-24` under S4.2's predicate | Under the S4.3 predicate |
|---|---|---|---|
| **A2-1** | `Agent 1 owns the camera and audio cues for the player.` | 1 offender — **caught** | caught |
| **A2-2** | `D-4 note: Agent 1 owns the camera and audio cues for the player.` | **0 offenders — missed** (the line contained `D-4`) | **caught** |
| **A2-3** | `§8 preamble, finding 1, row 5 also claimed: Agent 1 owns the camera and audio cues…` | **0 — missed** (three allowlist keywords on the line) | **caught** |
| **A2-4** | the same assignment inside a marked history block | exempt, but via keywords | **exempt, via location** — the block, not the words |
| **A2-5** | the same assignment inside a `[QUOTED]` review-disposition table | exempt, but via keywords | **exempt, via location** |
| **A2-6** | a `[QUOTED]` marker pasted into live §8 text with an assignment beside it | n/a — no location rule existed | **caught** — live sections may not be exempted, and the check asserts it |
| **P1** | `The instrument reports 6 observed tokens against 7 declared.` outside the anchors | **PASS — missed** (four hard-coded sites only) | **caught** |
| **P2** | `Seven declared, six observed.` (number words) | **PASS — missed** | **caught** |
| **P4** | a *second*, contradictory pair appended to the §1 row-6 line, which already stated the correct pair | **PASS — missed** (first match per site won) | **caught** |
| **P5** | the anchor pair itself made wrong | FAIL — caught | FAIL — caught (control: the old predicate did work here) |
| **P6** | the anchor row's pair deleted entirely | **PASS — missed** (`len(found) >= 3` tolerated a dropped site) | **caught** — a missing anchor is a failure |
| **P7** | a wrong historical count inside a marked block | n/a | **exempt** — history survives, by location |

**Why `DV-22` now fails on S4.2 itself, and why that is the correct behaviour.** The rewritten scan reads S4.2's text and reports **7 offenders** — all of them historical disposition rows in §2.1, §2.5, §2.6, §2.7 and §16 that say, truthfully, that a previous revision assigned audio to the wrong agent. They are legitimate history; under S4.2's predicate they were exempt *for the words they contained*, which is exactly the escape Agent 2 broke. **S4.3 does not widen the predicate to accommodate them and does not weaken it to pass itself: it marks the regions** (§13.1 documents the three exempt forms), so the exemption is visible in the text a reviewer reads. A checker that the current document can pass by re-wording the document is not a checker.

**Why `DV-24` now fails on S4.2 as well.** S4.2 restates its own correction record — *"the summary cell said 6"* and *"`6 observed` → `5 observed`"* — in §0.5. Those are correct history and wrong arithmetic, and the old check never read them because it read four sites. They are marked in S4.3 and the check passes here. **Two failures on the reviewed blob, both from the fix, both resolved by marking rather than by exemption language.**

### 13.3.2 TD's `DV-22` finding — the adversarial cases, before and after

The comparison below isolates the predicate: **both columns are the same validator code except `DV-22`, run over the same mutated text, built from the reviewed S4.3 blob** (`74546027…`) so that the document is not a second variable. It is reproducible in one command, against the S4.3 validator taken from commit `2acfc2e`:

```
$ git show 2acfc2e:docs/validation/dv_c05.py > /tmp/dv_s43.py
$ python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s43.py \
      --compare-base docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md
```

| # | Injected assignment | S4.3 predicate | S4.3.1 predicate | Required |
|---|---|---|---|---|
| **TD-1** | negation, then a positive assignment, comma + `but` | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-2** | negation, full stop, positive assignment | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-5** | three positive assignments separated by semicolons | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-5c** | negated responsibility, `and`, positive assignment | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-4a** | the contradictory text unquoted, in live text | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-3** | a pure negation, alone | PASS | PASS | PASS |
| **TD-3b** | a pure negation, worded differently | PASS | PASS | PASS |
| **TD-4b** | the contradictory text inside an authorised marked history block | PASS | PASS | PASS |
| **TD-4c** | the same inside a `[QUOTED]` review-disposition table | PASS | PASS | PASS |
| **TD-4d** | a `[QUOTED]` marker pasted into live text beside an assignment | FAIL | FAIL | FAIL |
| **TD-5b** | negation of a *different* object, then audio | FAIL | FAIL | FAIL |
| — | passive order (`… are owned by`) | FAIL | FAIL | FAIL |
| — | possessive order (`… are X's`) | FAIL | FAIL | FAIL |
| — | colon order (`audio cue selection: <agent>`) | FAIL | FAIL | FAIL |

**Three observations, in the order they matter for TD's reassessment.**

1. **The five `PASS — missed` cells are the defect TD found**, reproduced on the published blob and on the record. They are not a hypothesis about the old predicate: they are its actual verdicts.
2. **The negation cases and the exemption cases pass in both columns.** That is the check that the correction did not simply make the predicate stricter: `TD-3`, `TD-3b`, `TD-4b` and `TD-4c` are unchanged between the two validators, so genuine negations and genuine history still pass. A fix that caught the defect by failing everything would show `PASS → FAIL` in those rows too.
3. **`TD-4d` and `TD-5b` already failed under S4.3** and still fail — they are not evidence for the correction, and they are kept because they guard the surrounding properties (live text cannot be exempted; a negation of another object never launders an audio mention).

**The current-document rows are excluded from this table on purpose.** The S4.3 predicate also reports offenders on the *S4.3.1* text, because that text now contains TD's examples in prose. That comparison would mix two changes; the table above changes one thing at a time.

### 13.3.3 TD's second class — `no … audio` is not a denial of ownership

Same isolation method as §13.3.2: one variable, the predicate. Both columns run over mutated text built from the published S4.3.1 blob, so the document is not a second variable. Reproduce with:

```
$ git show db95404:docs/validation/dv_c05.py > /tmp/dv_s431.py
$ python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s431.py \
      --compare-base docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_1.md
```

| # | Injected line | S4.3.1 predicate | S4.3.2 predicate | Required |
|---|---|---|---|---|
| **TD-6** | *"has no problem owning audio cues"* | **PASS — accepted as a denial** | **FAIL — caught** | FAIL |
| **TD-7** | *"has no objection to owning audio cues"* | **PASS — accepted** | **FAIL — caught** | FAIL |
| **TD-8** | *"has no restriction on owning audio cues"* | **PASS — accepted** | **FAIL — caught** | FAIL |
| **TD-10** | *"has no issue with owning audio cues"* | **PASS — accepted** | **FAIL — caught** | FAIL |
| **TD-9** | *"has no difficulty taking responsibility for audio cues"* | FAIL (incidentally — the phrase exceeded the 28-character window) | **FAIL** | FAIL |
| **TD-11** | *"no objection to owning"* followed by a positive assignment | FAIL (incidentally — the second mention was positive) | **FAIL** | FAIL |
| **TD-12** | *"has no C-05 audio responsibility"* | PASS | **PASS** | PASS |
| **TD-13** | *"owns no audio cues"* | PASS | **PASS** | PASS |
| **TD-14** | *"has no responsibility for audio cue selection"* | PASS | **PASS** | PASS |
| **TD-17** | *"has no ownership of audio cue selection"* | PASS | **PASS** | PASS |
| **TD-15** | *"does not own any audio cues"* | **FAIL — a genuine denial, wrongly rejected** | **PASS** | PASS |
| **TD-16** | *"is not responsible for audio cue selection"* | **FAIL — a genuine denial, wrongly rejected** | **PASS** | PASS |
| **TD-18** | *"no objection to owning"* inside an authorised historical block | PASS | **PASS** | PASS |

**Read the columns in this order.**

1. **Four rows move from `PASS` to `FAIL`** — `TD-6`, `TD-7`, `TD-8`, `TD-10`. That is TD's class, and those are the only rows that move in the direction this revision is for.
2. **`TD-9` and `TD-11` fail in both columns.** They are TD's cases 4 and 5 and they are kept, but S4.3.1 already rejected them — by accident of character distance and by catching the second mention — so they are **guard cases, not evidence**. A report that presented them as proof of the fix would be overstating what changed.
3. **Two rows move from `FAIL` to `PASS`** — `TD-15` and `TD-16`. Those are genuine denials that S4.3.1 rejected because they contain no `no`. The bounded set recognises them. This makes the check **less** prone to flagging correct text while it becomes **more** able to catch incorrect text: the two directions are independent, and both are reported.
4. **The denial and exemption controls do not move.** `TD-12`, `TD-13`, `TD-14`, `TD-17` and `TD-18` pass in both columns. If the correction had been implemented by flagging every audio mention, those five would read `PASS → FAIL`.

**Why TD's caution — *"do not fix these cases by broadly flagging every mention of audio"* — was the right one.** A predicate that flags everything catches TD-6 through TD-11 and also catches `Agent 1 has no C-05 audio responsibility`, which is the S4.2 correction's own wording. It would have passed the new tests by breaking the old ones.

**Full tallies of the same checker, under the S4.3.2 predicate:** S4.3.2 **27/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27**.

### 13.3.4 TD's third class — a trailing denial, scoped to its own clause

Same isolation method again: **one variable, the predicate.** Both columns run over mutated text built from the published S4.3.2 blob, so the document is not a second variable.

```
$ git show b754deb3:docs/validation/dv_c05.py > /tmp/dv_s432.py
$ python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s432.py
```

| # | Injected line (described) | S4.3.2 predicate | S4.3.3 predicate | Required |
|---|---|---|---|---|
| **TD-19** | ownership, comma + `but`, denial naming Agent 1 | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-20** | ownership, comma + `which`, denial naming Agent 2 | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-21** | ownership, `and`, denial naming Agent 2 | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-22** | ownership + `which`, denial naming nobody | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-26** | ownership, em dash, appositive role denial naming Agent 1 | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-27** | ownership, parenthesised denial naming Agent 2 | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-23** | ownership, full stop, denial in the next sentence | FAIL (incidentally — the denial was outside every window) | **FAIL** | FAIL |
| **TD-24** | denial first, positive assertion second | FAIL (incidentally — the assertion was itself a mention) | **FAIL** | FAIL |
| **TD-25** | ownership, semicolon, denial naming Agent 2 | FAIL (incidentally — the semicolon ended the window) | **FAIL** | FAIL |
| **TD-28** | `Audio is not owned by Agent 1` — reversed order, genuine denial | PASS | **PASS** | PASS |
| **TD-29** | `Audio is not a responsibility of Agent 1` | PASS | **PASS** | PASS |
| **TD-30** | a genuine audio denial in a later clause about the same object | PASS | **PASS** | PASS |

**Read the columns in this order.**

1. **Six rows move from `PASS` to `FAIL`** — `TD-19`, `TD-20`, `TD-21`, `TD-22`, `TD-26`, `TD-27`. Those are TD's class: a trailing denial that answers a different clause, a different object or a different agent.
2. **`TD-23`, `TD-24` and `TD-25` fail in both columns.** They are kept as regression cases, but S4.3.2 already rejected them — by the sentence break, by catching the second clause's own mention, and by the semicolon ending the character window. They are not evidence for this correction and are marked as such here, exactly as §13.3.3 marks `TD-9` and `TD-11`.
3. **The denial controls do not move.** `TD-28`, `TD-29` and `TD-30` are genuine denials in reversed order and in later clauses, and they pass in both columns — as do every denial case from §13.3.2 and §13.3.3 (`TD-3`, `TD-3b`, `TD-12`…`TD-18`). If the correction had been implemented by flagging mentions that sit near any denial, those rows would have moved; they did not.

**Tallies of the same checker after the correction:** S4.3.3 **27/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27**. The predecessor figures are unchanged from S4.3.2's own table, which is a second measurement that the tightening did not leak into text it was not aimed at; S4.3.2 now fails only `DV-27`, as S4.3.1 and S4.3 already did, because `DV-27` requires the register that pins *this* revision and the register has moved on. That is the intended behaviour of the check, not a regression. **S4.3.1 and S4.3 fail only `DV-27`** — every content check passes under the corrected predicate, and the single failure is the provenance check that requires the register pinning *this* document. S4.2's tally is lower because the rewritten predicates are strictly stronger and S4.2 carries no exemption markers, so its own history reads as offenders. S4.1 and S4.0 are lower because they lack the corrections — not because the checker was tuned to a target: **the failing checks are the ones the reviewers named, in the order they named them.**

### 13.3.5 TD's fourth class — an unnamed denial, and the `that` boundary

Same isolation method again: **one variable, the predicate.** Both columns run over mutated text built from the published S4.3.3 blob.

```
$ git show 40d29cc:docs/validation/dv_c05.py > /tmp/dv_s433.py
$ python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s433.py
```

| # | Injected line (described) | S4.3.3 predicate | S4.3.4 predicate | Required |
|---|---|---|---|---|
| **TD-31** | ownership, `that`, unnamed denial (`is not owned`) | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-32** | ownership, `that`, unnamed denial with a stated object | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-33** | ownership, `that`, universal denial naming nobody | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-40** | universal denial, then a first-agent ownership phrase in the same clause | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-41** | universal denial beside a possessive first-agent assertion | **PASS — missed** | **FAIL — caught** | FAIL |
| **TD-34** | explicit denial naming the first agent, reversed order | PASS | **PASS** | PASS |
| **TD-35** | genuine universal exclusion (nobody owns them; no assertion of ownership) | PASS | **PASS** | PASS |
| **TD-37** | `has no authority over audio cue selection` — a `NEG_BEFORE` denial | PASS | **PASS** | PASS |
| **TD-36** | `that`-relative denial naming Agent 2 | FAIL | **FAIL** | FAIL |
| **TD-38** | plain positive ownership of cue selection | FAIL | **FAIL** | FAIL |
| **TD-39** | TD-31's line inside an authorised historical block | PASS | **PASS** | PASS |

**Read the columns in this order.**

1. **Five rows move from `PASS` to `FAIL`** — `TD-31`, `TD-32`, `TD-33`, `TD-40`, `TD-41`. `TD-31` is TD's condition A verbatim; `TD-33` is its interaction with condition B; `TD-40` and `TD-41` are the universal branch failing the *"genuinely excludes"* test.
2. **`TD-36`, `TD-38` and `TD-39` do not move.** `TD-36` and `TD-38` were already offenders; `TD-39` shows the historical exemption is still decided by location, not by wording — the very line that now fails in live text still passes inside a marked block.
3. **Every denial that was accepted before is still accepted.** `TD-34`, `TD-35`, `TD-37` do not move, and the whole S4.3.3 suite — `TD-3`, `TD-3b`, `TD-12`…`TD-18`, `TD-28`…`TD-30`, the `N-1` injections, the `DV-24` probes and the predecessor probes — passes unchanged. A correction that had been implemented by flagging mentions near any denial would have moved those rows; it did not.

**Tallies of the same checker after the S4.3.4 correction:** S4.3.4 **27/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — identical to the S4.3.3 table for every predecessor. S4.3.3, S4.3.2, S4.3.1 and S4.3 now fail only `DV-27`, the check that requires the register pinning *this* revision.

### 13.3.6 TD's S4.3.6 findings — every corrected instrument, before and after, on the same cases

**What was run.** The S4.3.6 suite (`86` cases) twice, once against the **published** validator (`/tmp/dv_s435.py`, the `baa31db` blob `6927644f`) and once against the corrected one, with `--compare` printing both verdicts per case:

```
python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s435.py
```

**The twelve cases whose verdict moves, and nothing else moves.** Every row is a case added at S4.3.6 except `TD-47`, which is pre-existing and was **wrongly failing**:

| Case | Wording (condensed) | S4.3.5 predicate | S4.3.6 predicate | Required |
|---|---|---|---|---|
| `TD-42` | first agent, contrastive `unlike` clause naming the second | **PASS** | **FAIL** | FAIL — Agent 2's counterexample |
| `TD-43` | the synonym `the first agent` as the sole subject | **PASS** | **FAIL** | FAIL — Agent 2's counterexample |
| `TD-44` | `as opposed to` | PASS | FAIL | FAIL |
| `TD-45` | `rather than` | PASS | FAIL | FAIL |
| `TD-46` | `but not` | PASS | FAIL | FAIL |
| `TD-47` | a foil naming the **first** agent leaves the second the subject | **FAIL** | **PASS** | PASS — a false positive the correction removes |
| `TD-52` | label, punctuation, wrong number | PASS | FAIL | FAIL |
| `TD-53` | the pair wrapped across a line break | PASS | FAIL | FAIL |
| `TD-54` | the pair split by a sentence break | PASS | FAIL | FAIL |
| `TD-56` | a token declaring an extra disallowed row | PASS | FAIL | FAIL |
| `TD-57` | a token declaring a disallowed range | PASS | FAIL | FAIL |
| `TD-58` | §5.4's hand cell count falsified | PASS | FAIL | FAIL |

**The nine cases that must *not* move, and do not**: `TD-48` (denial with a foil), `TD-49` (denial through the synonym), `TD-50` (object negation after the synonym), `TD-51` (`whereas` is a clause, not a foil — fails under **both**, by design), `TD-55` (the correct pair in the three new forms), `TD-59` (the unmodified §5.4 table), `TD-60` (a row whose owner is the wrong agent — fails under both, because an intersection with an empty set also fails; the subset rule keeps it failing for the right reason), and the two baseline checks (the live document passes `DV-22` and `DV-24` under both).

**The 67 pre-existing cases do not move at all** except `TD-47`, which is the false positive named above. That is the whole of the collateral: **one intended correction and no regressions.**

**And the clean document, three ways.** The S4.3.5 text under the S4.3.5 validator: **27/27**. The S4.3.5 text under the S4.3.6 validator: **27/27** — `DV-22` **0 offenders of 137 mentions**, `DV-24` **24 pairs, 0 disagreeing**, `DV-11` **7 declared / 5 observed, 43 cells, 7 cell-count claims, 0 failures**. This document under the S4.3.6 validator: **27/27**, with the same three instrument lines.

**Tallies of the same checker after the S4.3.6 correction:** S4.3.5 **27/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27** — every predecessor's tally is **unchanged**. (After the register is repointed, S4.3.5 reads 26/27: the one failure is `DV-27`, which requires the live register's path to appear in the document it ships with.)

### 13.3.7 TD's S4.3.7 findings — every corrected instrument, before and after, on the same cases

**What was run.** The S4.3.7 suite (106 cases) twice, once against the **published S4.3.6 validator** (`/tmp/dv_s436.py`, blob `840fed67`) and once against the corrected one, with `--compare` printing both verdicts per case:

```
python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s436.py
```

**Ten cases move, and every one of them for a stated reason.** Eight were accepted contradictions and must now fail; two were **false positives** the S4.3.6 validator produced and this revision removes.

| Case [QUOTED] | Wording (condensed) | S4.3.6 | S4.3.7 | Required |
|---|---|---|---|---|
| `TD-61` | the synonym as possessor — Agent 2's `MAJOR-1` | **PASS** | **FAIL** | FAIL |
| `TD-62` | foil carrying a subordinate clause — Agent 2's `MAJOR-2` | **PASS** | **FAIL** | FAIL |
| `TD-63` | `belongs to` + synonym | PASS | FAIL | FAIL |
| `TD-64` | `the cue's owner is` + synonym | PASS | FAIL | FAIL |
| `TD-65` | dash attribution + synonym | PASS | FAIL | FAIL |
| `TD-71` | the pair wrapped across **three** lines | PASS | FAIL | FAIL |
| `TD-72` | three lines with an intervening continuation | PASS | FAIL | FAIL |
| `TD-77` | owner clause violated while the allowed-row rule holds | **PASS** | **FAIL** | FAIL — the discriminator |
| `TD-67` | the mention is the **contrasted object** | **FAIL** | **PASS** | PASS — false positive removed |
| `TD-75` | `- declared 6` / `- observed 5` — **list items welded** | **FAIL** | **PASS** | PASS — false positive removed |

**The ten cases that must not move, and do not:** `TD-66` (`do not belong to` is a denial), `TD-68` (a marker in the previous clause does not drop the subject), `TD-69` (a short foil still fails), `TD-70` (the possessive denial), `TD-73` (the correct pair across three lines), `TD-74` and `TD-76` (adjacent but unrelated facts), `TD-78` (the unmodified table), `TD-79` (a dual-owned row stays legal) and `TD-80` (the allowed-row rule still fires on its own).

**The 86 pre-existing cases do not move at all** — including `TD-42`…`TD-60`, whose expectations this revision preserves exactly. **Zero regressions.**

**And the clean document, three ways.** The S4.3.6 text under the S4.3.6 validator: **27/27**. The S4.3.6 text under the S4.3.7 validator: **27/27** — `DV-22` 0 offenders, `DV-24` 8 pairs / 0 disagreeing, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / **8 owner checks** / 0 failures. This document under the S4.3.7 validator: **27/27**, same three instrument lines.

**Tallies of the same checker after the S4.3.7 correction:** S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — every predecessor's tally is **unchanged from S4.3.6**, and the single failure on each of the 26/27 rows is `DV-27`, the register that pins this document.

### 13.3.8 TD's S4.3.8 corrections — before and after, on the same cases

**What was run.** The S4.3.8 suite (120 cases) twice, once against the **published S4.3.7 validator** (`/tmp/dv_s437.py`, blob `06cfe2f2`) and once against the corrected one:

```
python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s437.py
```

**Seven cases move — four false alarms removed, three missed hazards restored — and nothing else moves.**

| Case | What it asserts | S4.3.7 | S4.3.8 | Why |
|---|---|---|---|---|
| `TD-81` | a `no`-quantified subject with `belongs to` is not an assignment | **FAIL** | **PASS** | `CONDITION-1`: a valid denial was rejected |
| `TD-82` | the existential frame with the synonym | **FAIL** | **PASS** | same |
| `TD-83` | `none of the` + plural `belong to` | **FAIL** | **PASS** | same |
| `TD-85` | the same quantifier with `is owned by` | **FAIL** | **PASS** | same family, this revision's probe |
| `TD-86` | the confirmed capitalised two-line wrap | **PASS** | **FAIL** | `CONDITION-2`: the hazard was missed |
| `TD-87` | continuation by `Then` | **PASS** | **FAIL** | same |
| `TD-88` | continuation by `And` | **PASS** | **FAIL** | same |

**The seven controls that must not move, and do not:** `TD-84` (a genuine `belongs to` assignment still fails), `TD-89` (a lowercase two-line wrap still fails), `TD-90`…`TD-93` (heading, blockquote, table-row and fence boundaries still do not join) and `TD-94` (a **correct** pair across a capitalised wrap still passes — the gate removal does not over-trigger).

**And all 106 carried-forward cases keep their expected verdicts**, including every S4.3.7 closure: `TD-61`, `TD-62` (Agent 2's `MAJOR-1`/`MAJOR-2`), `TD-63`…`TD-65` (the ownership class), `TD-66`, `TD-67` (denial and contrast-object controls), `TD-71`…`TD-76` (three-line wraps and the four false-join controls) and `TD-77`…`TD-80` (the owner clause and its controls). **Zero regressions**, which is the property TD's preservation requirement is about.

**The clean document, three ways.** The S4.3.7 text under the S4.3.7 validator: **27/27**. The S4.3.7 text under the S4.3.8 validator: **27/27** — `DV-22` **0 offenders**, `DV-24` **9 pairs / 0 disagreeing** (the S4.3.7 text's own count, measured), `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / 8 owner checks. This document under the S4.3.8 validator: **27/27**, same three instrument lines. **The new denial constructions never fire on prose that assigns ownership**, which is the precision half of the evidence.

**Tallies of the same checker after the S4.3.8 correction:** S4.3.7 **26/27**, S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — **every predecessor tally is unchanged**, and the single failure on each 26/27 row is `DV-27`, the register that pins this document.

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
| **D-4** | row 5 loses audio; row 6 keeps it; `TN-C-15` added; T-C05-67 | that no other row or clause still implies the first agent owns a cue | if another assignment survives, `DV-22` was scoped too narrowly **This risk materialised:** Agent 2 (`§4.4`) and Agent 3 (finding 5) both found §8's preamble still assigned the cue to the wrong agent while `DV-22` passed it — exactly the "scoped too narrowly" case this column predicted. Closed at S4.2 in §8 and in DV-22 (§13.1), with DV-22 now shown failing on the reviewed blob (§13.3). |
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
| §5.2 | row 5 loses audio and states Agent 1 owns no audio cue; row 6 owns audio and names its obligations; row 7 states it carries no obligation row; row 8 points at `C05-6.4`; row 3 states it owns types, not behaviour; row 2's range now `TN-P-01`…`TN-P-19` |
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

### 16.4 Supersession by S4.3, S4.3.1, S4.3.2, S4.3.3, S4.3.4, S4.3.5, S4.3.6, S4.3.7 and S4.3.8

**`A1-C05-S4.3` superseded `A1-C05-S4.2` by statement, not by edit; `A1-C05-S4.3.1` superseded `S4.3` the same way; `A1-C05-S4.3.2` superseded `S4.3.1` the same way; `A1-C05-S4.3.3` superseded `S4.3.2` the same way; `A1-C05-S4.3.4` superseded `S4.3.3` the same way; `A1-C05-S4.3.5` superseded `S4.3.4` the same way; `A1-C05-S4.3.6` superseded `S4.3.5` the same way; `A1-C05-S4.3.7` superseded `S4.3.6` the same way; and `A1-C05-S4.3.8` supersedes `S4.3.7` the same way.** S4.2 remains at `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143`, **unmodified**, as the record of what Agent 2 reviewed and passed on the contract text.

| Superseded | By | Nature of the change |
|---|---|---|
| `A1-C05-S4.3.1` v4.3.1 (`db95404` / `c8708ef0`) | `A1-C05-S4.3.2` v4.3.2 | **No normative clause.** `DV-22` accepts only bounded denials of ownership or responsibility instead of any `no … audio`; the class joins the regression suite; §18.3's stamp moves to that revision |
| `A1-C05-S4.3.2` v4.3.2 (`b754deb` / `74840d70`) | `A1-C05-S4.3.3` v4.3.3 | **No normative clause.** A denial stated *after* a mention counts only in the mention's own clause; the class joins the regression suite; one stale result cell is recorded rather than restated; §18.3's stamp moves to that revision |
| `A1-C05-S4.3.3` v4.3.3 (`40d29cc` / `d827e017`) | `A1-C05-S4.3.4` v4.3.4 | **No normative clause.** An unnamed trailing denial no longer counts — it must name the first agent, or be a universal exclusion that genuinely excludes him; `that` joins the phrase boundary; the class joins the regression suite; §18.3's stamp moves to that revision |
| `A1-C05-S4.3.4` v4.3.4 (`90971e0` / `41df692d`) | `A1-C05-S4.3.5` v4.3.5 | **No normative clause and no predicate change.** One front-matter suite figure corrected (56 → 74 restated as 56 → 67) and every other suite-count claim audited; the DOCUMENT content, the suite and the register mechanism are otherwise byte-identical; §18.3's stamp moves to this revision |
| `A1-C05-S4.3.7` v4.3.7 (`f1beb0c` / `0a0c36be`) | `A1-C05-S4.3.8` v4.3.8 | **No normative clause.** Two instrument corrections and one count correction (`DV-22` quantified denial, `DV-24` two-line continuation gate, the `DV-24` pair count), fourteen cases added; the contract text is **byte-identical**; §18.3's stamp moves to this revision |
| `A1-C05-S4.3.6` v4.3.6 (`034d091` / `e3a1fa85`) | `A1-C05-S4.3.7` v4.3.7 | **No normative clause.** Seven instrument corrections (`DV-22` possessor, foil clause, ownership class; `DV-24` guarded three-line join; `DV-11` owner clause), twenty cases added, every count re-derived; the contract text is **byte-identical**; §18.3's stamp moves to this revision |
| `A1-C05-S4.3.5` v4.3.5 (`baa31db` / `a0b46f46`) | `A1-C05-S4.3.6` v4.3.6 | **No normative clause.** Three instruments corrected (`DV-22` attribution, `DV-24` pair forms, `DV-11` subset rule and cell counts), nineteen cases added, every count re-derived; the contract text is **byte-identical**; §18.3's stamp moves to this revision |
| `A1-C05-S4.3` v4.3 (`2acfc2e` / `74546027`) | `A1-C05-S4.3.1` v4.3.1 | **No normative clause.** `DV-22` evaluates every audio mention separately instead of one negation per clause; the adversarial cases join the regression suite; §18.3's stale cross-reference corrected |
| `A1-C05-S4.2` v4.2 (`a788f95` / `7d03e1df`) | `A1-C05-S4.3` v4.3 | **No normative clause.** Two validator predicates rewritten deny-by-default (`DV-22`, `DV-24`), their counterexamples published (§13.3.1), `DV-27` widened to the provenance record, and the identity/measure decision recorded (§2.9, register, decision record) |
| `TDD-A1-C05-SUCCESSOR-004.2-D` (the copy on `arena/c64fc525-tdd`, `c800bf0` / `61ef03b4`) | **declared superseded** | Re-identified so that `…-004.2` names one artifact. **Not merged**: 360 lines differ and it states a different `TN-C-14` measure, which §2.9 rejects on the record |

**Cumulative chain, exact:** `A1-C05-S1` `2bb729f`/`dcec9e1a` → `A1-C05-S2` `e5ddad6`/`bf6c8fb3` → `A1-C05-S3` `a6b4e22`/`07723236` → `A1-C05-S4` `4692e97`/`424d2c69` → `A1-C05-S4.1` `95918268`/`d54e194a` → `A1-C05-S4.2` `a788f95`/`7d03e1df` → `A1-C05-S4.3` `2acfc2e`/`74546027` → `A1-C05-S4.3.1` `db95404`/`c8708ef0` → `A1-C05-S4.3.2` `b754deb`/`74840d70` → `A1-C05-S4.3.3` `40d29cc`/`d827e017` → `A1-C05-S4.3.4` `90971e0`/`41df692d` → `A1-C05-S4.3.5` `baa31db`/`a0b46f46` → `A1-C05-S4.3.6` `034d091`/`e3a1fa85` → `A1-C05-S4.3.7` `f1beb0c`/`0a0c36be` → `A1-C05-S4.3.8` (blob in the register).

---

## 17. Publication and provenance record

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md` — **new file** |
| Version | 4.3.8 (`A1-C05-S4.3.8`) — **final targeted validator correction** of S4.3.7: the denial set gains the **determiner-quantified subject** (`no … audio … belongs to`, `none of the … belong to`, and the same quantifier with `is owned by` / the possessive) so a valid denial is no longer read as an assignment (Agent 2 `CONDITION-1`); the `DV-24` continuation gate applies to **three-line windows only**, restoring every capitalised two-line wrap (`CONDITION-2`); and the document's `DV-24` pair count is corrected to the runner's **9** (`MINOR-1`). The suite grows 106 → **120**, and **no normative clause, obligation, count, identity decision, measure or publication mechanism changes** |
| Version of the baseline (history) | 4.3.7 (`A1-C05-S4.3.7`) — targeted **validator revision** of S4.3.6: the agent-1 name derived once so the synonym works as possessor (Agent 2 `MAJOR-1`), the foil bound to its clause instead of a 32-character window (`MAJOR-2`), the positive-ownership class widened with its denials and its contrast-object case (`MAJOR-1`'s family), a **guarded three-line join** in `DV-24` that closes wrapped contradictions and stops welding unrelated adjacent facts, and the §5.4 **owner clause** enforced as its own rule with §5.2 verified at run time. The suite grows 86 → **106**, and **no normative clause, obligation, count, identity decision, measure or publication mechanism changes** |
| Version of the baseline (history) | 4.3.6 (`A1-C05-S4.3.6`) — targeted **validator revision** of S4.3.5: `DV-22`'s attribution reads the document's synonym and skips contrastive foils (Agent 2 `MAJOR-1`), `DV-24` reads label-first, sentence-split and line-wrapped pairs, `DV-11` parses every declared row, applies the allowed-row rule as a subset and compares §5.4's hand cell counts. The suite grows 67 → **86**, and **no normative clause, obligation, count, identity decision, measure or publication mechanism changes** |
| Branch | `arena/3bc206a0-tdd` — the branch of record for Agent 1's C-05 series (S1 → S4.3.8) |
| **This document's own blob** | **named in `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8_PROVENANCE.md`, committed in the same commit as this file.** The register cannot pin a superseded draft of this document, because there is no earlier commit of this document for it to pin — mechanism and reason below the table |
| **Baseline this revision corrects** | `A1-C05-S4.3.7` v4.3.7 at **`f1beb0c07f643d56c15297529196fb6a4118a97b`**, blob **`0a0c36bec71f40d709878e67c19e4bca8f0b8b39`**, 2,107 lines — **preserved unmodified**. Its validator blob was `06cfe2f24fb17b2540eab9e6f8fd12efdcc79a93` and its suite blob `2a33543a8b6941262915e9a33b614411910b030b`, both preserved at that commit |
| **Earlier corrected baseline** | `A1-C05-S4.3.6` v4.3.6 at `034d091e1abcb507fdba6df4a05318a15aa5d7a1`, blob `e3a1fa85243a4749591363d4196bb5d65dad7c84` — **preserved unmodified**, with its validator `840fed67…`, suite `ee69f549…` and register `ce1ebc8d…` |
| **Earlier corrected baseline** | `A1-C05-S4.3.5` v4.3.5 at `baa31db3c631f0fc3e69a82b6d71207ad8061218`, blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` — **preserved unmodified**, with its validator `6927644f…` and suite `954588d3…` |
| **Earlier corrected baseline** | `A1-C05-S4.3.4` v4.3.4 at `90971e052e0eb2cbb843fcc80bdb2d1b5fa8e444`, blob `41df692d3d80aa967c0f80326a47582957fa8eca` — **preserved unmodified**, including the *74* figure recorded in §0.7.5 row 1 and §2.14 |
| **Earlier corrected baseline** | `A1-C05-S4.3.3` v4.3.3 at `40d29cca0bd2624fb731f4260145454a53a9860a`, blob `d827e017467b3bc320e2c5040a31f3aae0926d94` — **preserved unmodified** |
| **Earlier corrected baseline** | `A1-C05-S4.3.2` v4.3.2 at `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` — **preserved unmodified**, including the under-reported `DV-22` cell recorded in §0.7.3 row 3 |
| **Earlier corrected baseline** | `A1-C05-S4.3.1` v4.3.1 at `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` — **preserved unmodified** |
| **Earlier baseline** | `A1-C05-S4.3` v4.3 at `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` — **preserved unmodified** |
| **Reviewed artifact revised at S4.3 (still the object Agent 2 reviewed)** | `A1-C05-S4.2` v4.2 at **`a788f953256d208f3eb1310f3897924d007179b1`**, blob **`7d03e1df837493305831962f43882a1cd3496143`**, 1,265 lines — **the exact object the TD directive pinned** — **preserved unmodified** |
| **Reviewed predecessor (pinned by both S4.1 reviews)** | `A1-C05-S4.1` v4.1 at **`95918268ed5b20b878fef3ee0a7855ad18e6eeb6`**, blob **`d54e194affeaee98b1030e2b83b4c34e234fa382`** — **unmodified** |
| **The review this revision answers** | **Agent 2's independent review of S4.3.7** — `TDD-A2-REVIEW-A1C05-S4-3-7-001` v1.0, commit **`17af7be859d517e273f3f7d3af055a768daa8abe`** (`Docs/AGENT2_REVIEW_A1C05_S4_3_7_V1.md`, 589 lines) — **read only, not modified.** `PASS WITH CONDITIONS`: `CONDITION-1` (§2.21, `TD-81`…`TD-85`), `CONDITION-2` (§2.22, `TD-86`…`TD-94`) and `MINOR-1` (§2.23). Its `VERIFIED` findings — the structural `MAJOR-1`/`MAJOR-2` closures, the quantified-foil controls and the `DV-11` owner discriminator — are **preserved unchanged**, and its §3.6 residual families are **not** addressed here, as the directive requires |
| **Agent 3's S4.3.7 review** | **NOT PRESENT IN THIS REPOSITORY** — no `AGENT3` artifact of any kind exists after S4.1: verified five ways across all 79 reachable commits immediately before publication (§0.9.2). Nothing here quotes or reconstructs it |
| **The review the previous revision answered** | **Agent 2's independent review of S4.3.6** — `TDD-A2-REVIEW-A1C05-S4-3-6-001` v1.0, commit **`759ef103d1f8c9b2bdc64d0f41d1497f6c842313`** (`Docs/AGENT2_REVIEW_A1C05_S4_3_6_V1.md`, 560 lines) — **read only, not modified.** `PASS WITH CONDITIONS`, one condition `C-1`: `MAJOR-1` (possessive synonym), `MAJOR-2` (foil window) and `MINOR-1` (three-line wrap) — all three answered in §2.18/§2.19 and `TD-61`, `TD-62`, `TD-71`; `MINOR-2` (`TD-60` under-discriminates) answered in §2.20 and `TD-77`; `OBS-2` (the S4.2 clarification) recorded in §13.3.7 |
| **Agent 3's S4.3.6 review** | **NOT PRESENT IN THIS REPOSITORY** — no `AGENT3` artifact of any kind exists after S4.1: verified five ways across all 78 reachable commits immediately before publication (§0.9.1). **Its `DV-22` escape is `OPEN — ARTIFACT ABSENT` and unpaired**; its `DV-24` and `DV-11` findings are discussed on reproduced evidence only (§2.19, §2.20) |
| **The review the previous revision answered** | **Agent 2's independent review of S4.3.5** — `TDD-A2-ARCH-REVIEW-A1C05-S4-3-5`, commit **`659944b043b649601a555177fd0648018b1475e4`** (`Docs/AGENT2_ARCH_REVIEW_A1C05_S4_3_5_V1.md`, 541 lines) — **read only, not modified.** One `MAJOR-1` against `DV-22` (answered in §2.15, reproduced and closed), `MINOR-1`…`MINOR-4` (the audit's enforcement, the count's consequences, the branch-tip pinning — all carried into this revision's counts and register), and the acknowledged limitation that `DV-22` is a predicate over wording |
| **Agent 3's S4.3.5 QA review** | **NOT PRESENT IN THIS REPOSITORY** — `AGENT3_A1_C05_S4_3_5_INDEPENDENT_INTEGRATION_QA_REVIEW_V1.md` does not exist on any ref or at any of the 76 reachable commits; verified five ways immediately before publication (§0.9). **Its `DV-24` and `DV-11` findings are therefore `OPEN — ARTIFACT ABSENT`, and nothing here quotes, paraphrases or reconstructs them.** What §2.16 and §2.17 close are this revision's own reproduced defects, labelled `A1-P1`…`A1-P6` |
| Reviews answered | **TD's S4.3.6 directive** (resolve the independently reproduced validator findings while preserving the contract) — answered in §0.7.6, §2.15, §2.16 and §2.17; **TD's S4.3.5 directive** (`PASS WITH CONDITIONS` on S4.3.4: both `DV-22` corrections accepted, one publication inconsistency — the *74* figure — to fix) — answered in §2.14 and §0.7.5; **TD's S4.3.4 directive** (two residual `DV-22` false negatives on S4.3.3: an unnamed denial, and the missing relative-clause boundary) — answered in §2.13 and §13.3.5; **TD's S4.3.3 directive** (`PASS WITH CONDITIONS` on S4.3.2: reproduce the verification against the exact commit, then adversarially test `NEG_AFTER`) — answered in §2.12 and §13.3.4; **TD's S4.3.2 directive** (a second `DV-22` false-negative class, its tests, the §18.3 stamp) — answered in §2.11 and §13.3.3; **TD's S4.3.1 directive** and Agent 2 `TDD-A2-REASSESS-A1C05-S4-2-001` v1.0 (commit `c8e9f2a`, 708 lines, `PASS WITH CONDITIONS` — `N-1`, `N-2`, `N-3` closed at S4.3, **unchanged here**) with Agent 2 `ADDENDUM-A1` (commit `e434dbe`); Agent 2 `TDD-A2-REVIEW-A1C05-S4-1-001` v1.0 (commit `eee9401`, 594 lines); Agent 3 independent integration review v1 (commit `34b035b3eb135bbb4e8dfd47bbd54d3a46b8062a`, 114 lines) — **read only, not modified** |
| **Agent 3's S4.2 report** | **NOT PRESENT IN THIS REPOSITORY** — verified four ways immediately before publication, §0.8. Nothing in this file quotes, paraphrases or characterises it |
| Earlier reviews answered | Agent 2's S3 review `47dbdffb…` (`Docs/AGENT2_REVIEW_A1C05_S3_V1.md`); Agent 2's S2 review `ac498ce` — read only, not modified |
| Baselines preserved unmodified | `A1-C05-S4` v4.0 at `4692e973d04a94d7781677c704e7a0198abd2d70`, blob `424d2c69df62ebc1930eacd0ba67077c854ab31e`; `A1-C05-S3` v3.0 at `a6b4e22999c7f8622c7c67e9cdc39e2f57565c20`, blob `077232368c42b2cd910be2c9642ba05cd7faa382`; `A1-C05-S2` v2.0 at `e5ddad6`, blob `bf6c8fb3ddf3152d1627d3b6471278f57fc82541`; `A1-C05-S1` v1.0 at `2bb729f`, blob `dcec9e1ae3efd4651c290636e8a4d6623603dc83` |
| `A1-R1` / `A1-R2` / `A1-R3` / `A1-R4` / C-05-3 response | `25ab47c2…` / `5ee2769…` / `109331f3…` / `2cc548fa…` / `a94b49ef…` — **unmodified** |
| MEAD-A / MEAD-B / MEAD-C | read only; none moved, deleted, renamed, archived, overwritten or edited; **no canonical document selected** |
| **Validation instrument** | **`docs/validation/dv_c05.py` — in this repository, 27 checks, runnable by any reviewer**: `python3 docs/validation/dv_c05.py <document>`. It is a **document-text** checker, not a test suite, and no test-suite claim is made from it. `DV-22` is deny-by-default, evaluated **per mention**, and accepts only **bounded denials**; `DV-24` is deny-by-default over the whole document |
| **Instrument regression suite** | **`docs/validation/test_dv_c05_regressions.py`** — **120 cases**, `python3 docs/validation/test_dv_c05_regressions.py`, **120/120 behaving as required**. S4.3.8 adds `TD-81`…`TD-85` (the quantified-denial family and its positive control) and `TD-86`…`TD-94` (the capitalised two-line wraps, the lowercase control, the correct-pair control and the heading, blockquote, table-row and fence boundaries); the before/after table is §13.3.8. S4.3.7 adds `TD-61`…`TD-70` (`DV-22`: the possessive synonym, the long foil, the widened ownership class, and five controls), `TD-71`…`TD-76` (`DV-24`: three-line wraps and four false-join controls) and `TD-77`…`TD-80` (`DV-11`: the owner-rule discriminator, the correct-evidence control, the dual-owned control and the allowed-row control); the before/after table is §13.3.7. S4.3.6 adds `TD-42`…`TD-51` (the `DV-22` attribution cases, including the foil that named the wrong agent and the `whereas` decision), `TD-52`…`TD-55` (the three `DV-24` pair forms and their control) and `TD-56`…`TD-60` (the `DV-11` declaration, range, cell-count and row-owner cases); the before/after table is §13.3.6. It contains Agent 2's injection verbatim, TD's `D-4`-prefixed form, the four S4.3.1 contradictory forms, TD's five `no … audio` forms, the three required-pass denials, four further genuine denials, the word-order variants, TD's twelve `NEG_AFTER` scoping cases, TD's eleven unnamed/relative-clause cases, the six `DV-24` probes and the exempt-region controls; `--compare <older validator> [--compare-base <blob>]` reproduces the before/after tables in §13.3.2, §13.3.3, §13.3.4 and §13.3.5 |
| **Identity decision record** | **`docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md`** — declares `7d03e1df…` the artifact `TDD-A1-C05-SUCCESSOR-004.2` denotes, re-identifies the `arena/c64fc525-tdd` copy as `…-004.2-D` and supersedes it, and resolves the `TN-C-14` measure. Restated in §2.9 |
| **Duplicate identity** | `TDD-A1-C05-SUCCESSOR-004.2` denotes **one** blob: `7d03e1df837493305831962f43882a1cd3496143`. `TDD-A1-C05-SUCCESSOR-004.2-D` denotes the superseded copy on `arena/c64fc525-tdd` (`c800bf0`, blob `61ef03b4…`) — **not merged, not adopted, not citable** |
| Contracts signed / frozen | **None** — C-05 remains proposed and unsigned |
| Code, Core types, project, merge, M0 | **None** |
| Acceptance tests | 67 cases `PROPOSED / NOT RUN`, **0 executed**; 27 document checks and 120 instrument regression cases run (§13) |

**Why this file carries no placeholder — and the one thing S4.2 got wrong about the mechanism.** S4.1's reviewed blob contained literal commit/blob placeholder fields (`S41_*`), which a later commit then filled, so the blob both reviewers pinned was one where a reader could not follow the document's own "review this exact blob" instruction (Agent 3 finding 7). S4.2 answered it by putting the hash in a register written *in the next commit* — and that created a smaller version of the same defect: at the publishing commit `a788f95`, the register still pinned the first S4.2 draft, blob `86f56af…` (register blob `eda9bd2671650b0c41a8aa1cff97da0dd0fad593`), while the document in that same commit was already `7d03e1df…`. Agent 2 caught it in its check 3b; `d1d9ac9` corrected the value but not the mechanism. **S4.3 changes the mechanism: this document and the register that names its blob are written into one commit.** A document still cannot contain its own blob hash without an edit, but it no longer needs to: the register names this document's blob, and both files appear together, so there is no earlier commit of this document for a register to be stale about. The commit itself is identified by the paths it introduced — `git log --format=%H -1 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md` — rather than by a hash no file can hold. `DV-27` fails if any placeholder token appears in this file, and fails if the register is not referenced in §17 and §18, so the defect cannot return silently.

**A negative existence claim is re-verified immediately before publication** (Agent 2's §1.3 rule): `git ls-remote --heads origin` was run as the last action before this document was committed, and the result is recorded in the register together with the blobs present at that moment. **Claim: there is no Agent 3 S4.2 review in this repository** — §0.8 states the four checks and their results.
**This table's S4.1 values are exact, not abbreviated:** commit `95918268ed5b20b878fef3ee0a7855ad18e6eeb6` and blob `d54e194affeaee98b1030e2b83b4c34e234fa382`, the values TD item 6 requires and Agent 3's finding 7 names.

---

## 18. Handoff

### 18.1 To Agent 2 — your S4.3.7 review, and what S4.3.8 does with its two conditions

Review **the blob named in `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8_PROVENANCE.md`**, path `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md` — not a branch tip, not a diff, not the S4.3.6 blob and not the S4.2 blob. **Your two conditions are closed on the evidence you asked for, including the specific inversion you said you would look for**: the table in §2.22 now reads `S4.3.6 FAIL / S4.3.7 PASS / S4.3.8 FAIL` for all three capitalised wraps, and `TD-86`…`TD-88` are permanent cases. `CONDITION-1` is closed without touching a single positive-attribution pattern — `TD-84` proves the genuine form still fails. `MINOR-1` is corrected to **9** and §2.23 states why the figure drifted. **Your §3.6 residual families are not addressed**: they are non-blocking, they are not among the two authorised corrections, and this cycle is explicitly not a general-purpose expansion. **The S4.3.6 condition `C-1` was closed on the evidence you asked for and in the form you asked for**: `MAJOR-1` (`TD-61`), `MAJOR-2` (`TD-62`) and `MINOR-1` (`TD-71`) each produce `DV-22`/`DV-24` `FAIL`, the three-population evidence is §2.18 and §13.3.7, the clean document is 27/27 with 0 offenders, and all 86 carried-forward cases behave as required. **One deliberate departure from your recipe is recorded**: the foil is bound to the *clause*, not to a fixed distance, and the mention inside a contrastive clause is excluded — without that, widening the possessor produced the false positive `TD-67`. **Your `MAJOR-1` is closed as you stated it**, with one measured departure from your recipe that you should check: `whereas` is *not* in the foil set (§2.15), because dropping it loses a true positive. Your `MINOR-1` (an unenforced audit) is answered by §2.14 rows 12–14, `MINOR-2` (the count's consequences) by re-deriving every figure for 86 rather than patching 67, and `MINOR-4` (branch-tip pinning) by the register naming this document's blob in the same commit. **No normative clause changed at S4.3 or at S4.3.1**, so this is a re-review of two predicates, one identity record and one publication mechanism, not of the contract; your §11 says that is all that stands between `PASS WITH CONDITIONS` and `PASS`. **The only thing S4.3.1 through S4.3.4 change is `DV-22`'s predicate** (§13.1, §13.3.2, §13.3.3, §13.3.4, §13.3.5) — TD found four residual false-negative classes in the check you made S4.2-blocking, and all four are closed without touching the contract: a negation may not launder a later assignment, a denial of *difficulty* is not a denial of *ownership*, a denial after a mention answers only its own clause, and a denial that names nobody is not evidence that the first agent is excluded. **S4.3.5 changes no predicate and no test** — it corrects one front-matter figure and audits the rest (§2.14). **Your S4.1 findings and their dispositions are in §2.5**, one row each, and the TD's six consolidated items are in §2.7.

<!-- QUOTED-HISTORY-START -->
1. **D-4 / C6-2 the two-word deletion** — §8's preamble now reads *"Agent 1 for defence selection, dodge, camera response and framing; Agent 2 for AI reaction, audio cue selection (the only C-05 audio responsibility), montage trigger and VFX timing"*. `TN-C-15` unchanged.
<!-- QUOTED-HISTORY-END -->
2. **D-22-scope / your `N-1`** — the allowlist is gone. `DV-22` now exempts **regions** only (fenced block, `[QUOTED]` table, marked history block), requires a negation in the **same clause** as the audio mention, and refuses to let §5.2, §6.1, §8 or §12.2 be exempted at all — it asserts that. Your injection is in §13.3.1 rows `A2-2` and `A2-3`, verbatim, and it is a case in `docs/validation/test_dv_c05_regressions.py`. **On your reviewed blob the rewritten scan now reports the defect itself**: 5 offenders on S4.1 including line 566's preamble, where S4.2's scan reported 0 for that line.
3. **C4c-N1** — §3.6(b) now states that the order **is** observable through a mid-frame pull under `PO-5`, with your conclusion kept and `PO-3` retained. `PO-3`, `PO-5`, `TN-P-15`, `TN-P-18`, `T-C05-51` and `T-C05-65` are byte-identical.
4. **D-1a / D-1b** — `TN-C-14` now attaches to the **call site**, requires an observation taken **in the frame of use**, states a **maximum interval of one frame measured on the shared axis**, requires **re-pull or suppression** when the guarantee cannot be shown, and **derives** the bound instead of asserting it. Is "at most one frame, measured from the missed revision's publication to the use" the wording you wanted?
5. **D-6b** — §5.4's tallies are now machine counts (23 / 12 / 3 / 2 / 3 / 0 / 0 = 43). The TD routed this to your addendum; it is fixed here because §5.4 is the table `DV-11` reads.
6. **D-6a-i condition / the `DV-24` false negative** — `DV-24` still fails on S4.0 (`2 disagreeing pairs`), and it now reads the **whole document** instead of three sites: all pairs, digits or number words, either order, every match on a line; the three anchors must exist. Three probes that S4.2's version passed with a wrong count in the text are §13.3.1 rows `P1`, `P2`, `P4`; `P5` is the control that both versions catch. **It now fails on S4.2 too**, because S4.2 states its own correction record unmarked; S4.3 marks it and passes.
7. **Carried verdicts** — D-1, D-2, D-3, D-5, D-6, D-7, C4a-1/2, C4c-1/2, C6-1, C9 are untouched; nothing is reopened.
8. **Agent 3's finding 6** on T-C05-63 — the combined held-snapshot + altered-tag + dataflow-instrumented scenario was raised by Agent 3, not by you. **It is in §12.2**; if you consider it insufficient, say so, and say which dataflow instrument you would accept.

9. **`N-2` — the duplicate identity** — §2.9 and `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` do the one thing you left open and refused to assume: they **declare** which blob `TDD-A1-C05-SUCCESSOR-004.2` denotes (`7d03e1df…`), **re-identify** the copy on `arena/c64fc525-tdd` as `…-004.2-D`, **supersede** it, and resolve the `TN-C-14` measure in favour of the shared axis with four stated reasons. No merge, no averaging. **The residual is stated rather than hidden:** line 3 of that file still reads `…-004.2`, and physically withdrawing it needs a commit on a branch I may read and may not write.
10. **`N-3` — your addendum** — §17 now cites `ADDENDUM-A1` (`e434dbe`), and the classification is stated: `D-1b` was **adopted as a genuine improvement** and remains **`ADVISORY`** under your taxonomy. The S4.2 text saying *"adopted exactly"* is not repeated here.
11. **The commit/blob mismatch your check 3b found** — the mechanism changed, not just the value (§17): this document and the register naming its blob are written in **one commit**, so a register cannot pin a superseded draft of the document it describes.

**Is `PASS` now available?** That is the verdict requested, and it is requested on your terms rather than mine: §11 says two conditions closed without touching an obligation would move you to `PASS` without re-reviewing the contract text, and S4.3 touches no obligation. **If either condition is not closed as you stated it, name the line and it will be corrected in place.**

**No signature, freeze or acceptance is requested, and none is implied by a verdict.**

### 18.2 To Agent 3 — your S4.1 findings, and the four reports that are not here

Review **the blob named in `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8_PROVENANCE.md`**. **Your S4.3.5, S4.3.6 and S4.3.7 reviews are not in this repository** (§0.9, §0.9.1, §0.9.2). Nothing in this revision is attributed to you; the quantified-denial family closed in §2.21 is Agent 2's condition plus this revision's own probes, labelled as such. **Your S4.3.5 and S4.3.6 reviews are not in this repository** (§0.9, §0.9.1). Your `DV-22` positive-ownership escape is therefore **`OPEN — ARTIFACT ABSENT` and deliberately unpaired**: §2.18 reproduces seven further members of that family and labels them as this revision's probes, not as yours. Your `DV-24` three-line finding corresponds to a defect Agent 2 reproduced independently and is closed; your false-joining finding is closed on evidence that the S4.3.6 join **already** welded list items (`TD-75`). Your `DV-11` owner-column finding is closed by direct enforcement, with the `TD-60` analysis in §2.20. **Your S4.3.5 QA review is not in this repository** (§0.9, five checks) — so your `DV-24` counterexamples and your narrower `DV-11` gap are **`OPEN — ARTIFACT ABSENT`**, not answered. If you can publish them, they will be run against this validator as written; §2.16 and §2.17 record what *was* closed and label it as this revision's own probes, not as yours. Your S4.1 findings and their dispositions are **§2.6**, one row each. **Your S4.2 report is not in this repository** — §0.8 states the four checks and their results, and nothing here quotes, paraphrases or anticipates it. Two defect classes the S4.3 directive attributes to it were reproduced from the reviewed blob instead (§13.3.1), and both were real. **If your report exists elsewhere, please say where, or paste the probe**: the rewritten `DV-24` should be tested against *your* probe before the condition is called closed, not only against mine.

1. **Finding 1 (row 5)** — §5.2 row 5 is now *response selection and telegraph consumption*, explicitly **not** the hit outcome, and it points to **row 8** with `C05-6.1` / `TN-A-01`–`TN-A-03`. Is the exclusion stated where an implementer would look?
2. **Finding 4 (the bound)** — your counterexample is now a **named schedule** in `T-C05-64` (**s2**), the obligation is five rules in `TN-C-14` with the measure and the maximum interval stated, and the bound is derived. **Please try to break it again:** the interesting case is a consumer with no frame of its own (§`TN-C-14`(iii) requires it to use the shortest interval at which it acts).
3. **Finding 5 (audio)** — §8's preamble is corrected and `DV-22` widened; **DV-22 is shown failing on the blob you reviewed** (§13.3).
4. **Finding 6 (T-C05-63 / DV-20)** — the three conditions are combined, the assertion is on the **hit-resolver's input/use path** with a tainted-value instrument, and a **separate** selection-path assertion is retained. **`DV-20`'s limit is unchanged and admitted:** it is a text check; the dataflow claim is T-C05-63's, which is `PROPOSED / NOT RUN`.
5. **Finding 7 (provenance)** — no placeholder token exists anywhere in this file; the register carries the hash. **A negative existence claim is re-checked immediately before publication**, per Agent 2's §1.3 rule, and the result is recorded in the register.
6. **Your S3 review** — still not in the repository as of this revision (§0.2). If it exists elsewhere, say where; if not, the `TN-C-11`/`TN-A-01`–`02` resolution remains **S4's own** and B-15 stays `OPEN`.
7. **B-13 / TD-09** — unchanged and still external. `C05-6.4` still decides nothing about registration or unblockable authority.
8. **A note on the duplicate** — the copy of S4.2 on `arena/c64fc525-tdd` was produced in that worktree. It is **not** merged, not adopted, and not citable; §2.9 records why `7d03e1df…` is the artifact the identity denotes. If the drafting effort behind it should be preserved under its own identity, `…-004.2-D` is that identity and the register records its exact commits and blobs.

### 18.3 Status

`DESIGN_ONLY`. **C-05 and U-07 remain open. Nothing is signed, frozen or merged. No MEAD is selected. No C++ was written, no runtime validation was performed, and none is claimed.** TD-06, TD-09 and TD-12 are untouched and remain external blockers (B-1, B-2, B-4). **B-11 is `BLOCKED BY DEPENDENCY` on a C-04 decision**; B-12, B-13, B-14 unchanged; **B-15 stays `OPEN`** because Agent 3's S3 review is still absent, so the tag/arbitration resolution remains S4's own rather than a reviewer's. 67 acceptance cases are proposed and unexecuted — **no behaviour is validated by anything in this document**; 27 document checks pass and prove only that the text is internally consistent, and six of them are shown failing on earlier blobs in §13.3. **S4.3.8 stops here for TD reassessment.**
