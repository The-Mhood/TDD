# Provenance register — `A1-C05-S4.3.3`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document**. The mechanism is unchanged from S4.3, S4.3.1 and S4.3.2: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. Both files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_3.md` |
| Version | 4.3.3 (`A1-C05-S4.3.3`) |
| **Blob of this document** | **`d827e017467b3bc320e2c5040a31f3aae0926d94`** |
| Lines | 1,657 |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, `docs/validation/dv_c05.py`, `docs/validation/test_dv_c05_regressions.py`, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.2` at `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b`, 1,584 lines — **unmodified**, including the under-reported `DV-22` result cell described below |
| Earlier baselines, **unmodified** | S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_3.md
# d827e017467b3bc320e2c5040a31f3aae0926d94   (must equal the field above)
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_3.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 56/56
```

## What this revision is

**A targeted revision of S4.3.2, found by doing what TD asked for.** TD's verdict on S4.3.2 was `PASS WITH CONDITIONS` with two conditions outstanding:

1. **Independently reproduce the published verification against the exact commit.** Done, and it reproduced exactly: `git archive b754deb3 | tar -x -C /tmp/verify_s432` gave a clean 58-file tree with no working-tree state, in which the validator reported **27/27** and the regression suite **44/44**. The three relevant blobs at `HEAD:` and in the working tree are identical, and there is one worktree, so the numbers are that commit's numbers.
2. **Adversarially test `NEG_AFTER`.** Done, and it found a third class of false negative. A denial placed *after* an audio mention exempted that mention even when the sentence had just asserted that the first agent owns it:

```
Agent 1 owns audio cues, but those cues are not assigned to Agent 1.    -> accepted  (required FAIL)
Agent 1 owns audio, which is not a responsibility assigned to Agent 2.  -> accepted  (required FAIL)
Agent 1 owns audio cues and those cues are not owned by Agent 2.        -> accepted  (required FAIL)
Agent 1 owns audio cues which are not owned by anyone.                  -> accepted  (required FAIL)
```

The three further probes (a denial in a following sentence, a denial *before* a positive assertion, and a semicolon-joined denial naming Agent 2) were caught, and the four required-pass denials passed. **The defect is specifically the reversed order across a clause boundary, not a general failure of denial recognition.**

`DV-22` now requires a denial that follows a mention to sit in the mention's **own clause and phrase** — no comma, semicolon, sentence end, em or en dash, or conjunction or relative pronoun between them — and to name the **first** agent or nobody, with the agent read through the rest of the clause. `NEG_BEFORE` is untouched.

**Measured before it was written.** On the S4.3.2 text, **0 of the 110 audio mentions were accepted only by `NEG_AFTER`**, so no verdict on the document itself could change. That is the evidence that this is a narrow scoping fix rather than a blunter check.

**Four changes, no others:** the `NEG_AFTER` scope rules; the regression suite (44 → **56** cases: nine lines that must fail, three genuine denials that must keep passing); one stale result cell recorded rather than quietly restated; and §18.3's revision stamp, which names the current revision by design.

**A provenance defect found and recorded, not papered over.** §13.1's `DV-22` row on the published S4.3.2 blob states *exempt lines 229 (fenced 157) … audio mentions evaluated 93*. The checker's actual output for that blob is **exempt lines 234 (fenced 162) … mentions 110**. The figures predate the evidence blocks §0.7.2 and §2.11 added, and no check compares a result cell to the computed value. S4.3.2's text is preserved byte-identical; the discrepancy is recorded in §0.7.3 row 3 and §2.12, and this revision states the computed figures for its own text.

**Preserved, exactly:** every normative clause of S4.2 and its 43 obligations / 18 suites / 67 proposed cases; `DV-24`; `NEG_BEFORE`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.2 and every earlier artifact and register; the same-commit register mechanism.

## Identity declaration (unchanged, restated so the register is self-contained)

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `arena/3bc206a0-tdd`, `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143` | authoritative S4.2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | `arena/c64fc525-tdd`, `99717e0` / `c800bf0`, blobs `eb774f5d…` / `61ef03b4…` | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | S4.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.1` | `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` | S4.3.1 |
| `TDD-A1-C05-SUCCESSOR-004.3.2` | `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` | S4.3.2, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.3` | this document, blob `d827e017467b3bc320e2c5040a31f3aae0926d94` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again to the claim that no Agent 3 S4.2 report exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `b754deb317284df967eaaf84f08e72ecdd2a3ad3` (before this push) · `arena/5dde91a4-tdd` `c8e9f2a` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.2 review present on any branch | **no** — three Agent 3 files exist, none an S4.2 review, none mentioning `DV-24` or `7d03e1df` |
| `git rev-parse b754deb3:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_2.md` | `74840d70a1620caaa3fe1138ab68eccd71c0665b` — the baseline is intact |
| Predecessor blobs at the tip | S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df`, S4 `424d2c69`, S3 `07723236` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_3.md` | **27/27 checks passed** |
| Same checker on earlier blobs | S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — the single failure on S4.3.2, S4.3.1 and S4.3 is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **56/56 cases behaved as required** |
| Before/after on TD's third class | S4.3.2 predicate **accepted six** of the new forms (`TD-19`, `TD-20`, `TD-21`, `TD-22`, `TD-26`, `TD-27`); S4.3.3 catches all six; three further forms (`TD-23`, `TD-24`, `TD-25`) were already caught in both columns and are reported as guard cases, not evidence (§13.3.4) |
| Required-pass set re-tested | `TD-3`, `TD-3b`, `TD-12`…`TD-18`, `TD-28`, `TD-29`, `TD-30` — **all still PASS** |
| Condition 1 reproduction | `git archive b754deb3` → validator **27/27**, suite **44/44**, all 44 case names captured |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is so a reviewer can pin it. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it. S4.3.3 stops here for TD reassessment.**
