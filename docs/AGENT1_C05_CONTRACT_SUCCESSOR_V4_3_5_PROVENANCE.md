# Provenance register — `A1-C05-S4.3.5`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document**. The mechanism is unchanged from S4.3 through S4.3.4: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. Both files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md` |
| Version | 4.3.5 (`A1-C05-S4.3.5`) |
| **Blob of this document** | **`a0b46f46c81e85cea5d04b940aaf9aee46c19deb`** |
| Lines | 1,779 |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, `docs/validation/dv_c05.py`, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.4` at `90971e052e0eb2cbb843fcc80bdb2d1b5fa8e444`, blob `41df692d3d80aa967c0f80326a47582957fa8eca`, 1,730 lines — **unmodified**, including the `74` figure recorded in §0.7.5 row 1 and §2.14 |
| Earlier baselines, **unmodified** | S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md
# a0b46f46c81e85cea5d04b940aaf9aee46c19deb   (must equal the field above)
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 67/67
```

## What this revision is

**A metadata correction, answering the single publication inconsistency in TD's S4.3.4 reassessment** (`PASS WITH CONDITIONS`: both `DV-22` defects accepted as corrected; one figure to fix).

**The defect.** The Scope line of S4.3.4 stated that the regression suite grew *from 56 to **74** cases*. The suite grew from 56 to **67** — 56 cases carried from S4.3.3 plus the eleven added at S4.3.4 (`TD-31`…`TD-41`). Four independent measurements agree, and all four are recorded in §2.14:

| Measurement | Value |
|---|---|
| `python3 docs/validation/test_dv_c05_regressions.py` | **67 PASS lines**, `67/67 regression cases behaved as required` |
| `git diff 40d29cc 90971e0 -- docs/validation/test_dv_c05_regressions.py` | **+11** `case(` lines, **0** removed |
| `DV-2` on the document | **67 distinct case ids**, none missing, none extra |
| The S4.3.4 register | **67/67** |

**The correction, and the audit TD asked for.** The Scope line now reads *56 to **67*** and states the composition, so the number is checkable without opening the test file. §2.14 lists **every** suite-count claim in the document — eleven of them, historical growth steps included — with the value each one should have and its verdict: **one was wrong, ten are correct.** It also states the coincidence that invited the error: **67** is also the number of proposed *acceptance* cases (`T-C05-01`…`T-C05-67`), none of which is executed, while the 67 *instrument regression* cases are the checker's own tests and the only 67 in this document that ran.

**Changes, exhaustively:** the Scope line's figure and composition; the §2.14 audit; §18.3's revision stamp. **Nothing else.** The `DV-22` predicate is byte-identical to S4.3.4, the regression suite is byte-identical (no case added, removed, renamed or re-ordered), and every normative clause, obligation, count, suite and proposed case is carried forward unchanged.

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; `DV-24`; `NEG_BEFORE`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.4 and every earlier artifact and register; the same-commit register mechanism.

## Identity declaration (unchanged, restated so the register is self-contained)

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `arena/3bc206a0-tdd`, `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143` | authoritative S4.2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | `arena/c64fc525-tdd`, `99717e0` / `c800bf0`, blobs `eb774f5d…` / `61ef03b4…` | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | S4.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.1` | `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` | S4.3.1 |
| `TDD-A1-C05-SUCCESSOR-004.3.2` | `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` | S4.3.2 |
| `TDD-A1-C05-SUCCESSOR-004.3.3` | `40d29cca0bd2624fb731f4260145454a53a9860a`, blob `d827e017467b3bc320e2c5040a31f3aae0926d94` | S4.3.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.4` | `90971e052e0eb2cbb843fcc80bdb2d1b5fa8e444`, blob `41df692d3d80aa967c0f80326a47582957fa8eca` | S4.3.4, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.5` | this document, blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again to the claim that no Agent 3 S4.2 report exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `90971e052e0eb2cbb843fcc80bdb2d1b5fa8e444` (before this push) · `arena/5dde91a4-tdd` `c8e9f2a` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.2 review present on any branch | **no** — three Agent 3 files exist (`AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md`, `AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md`, `AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md`, all on `arena/c64fc525-tdd`), none an S4.2 review, none mentioning `DV-24` or `7d03e1df` |
| `git rev-parse 90971e0:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_4.md` | `41df692d3d80aa967c0f80326a47582957fa8eca` — the baseline is intact |
| Predicate unchanged | `git diff 90971e0 -- docs/validation/dv_c05.py` touches **only** the `REG` path constant — no pattern, no branch, no threshold |
| Regression suite unchanged | `git diff 90971e0 -- docs/validation/test_dv_c05_regressions.py` — **empty** |
| Predecessor blobs at the tip | S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_5.md` | **27/27 checks passed** |
| Same checker on earlier blobs | S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — the single failure on S4.3.4/S4.3.3/S4.3.2/S4.3.1/S4.3 is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **67/67 cases behaved as required**, 67 PASS lines |
| §2.14 audit re-derived | 11 suite-count claims listed; **1 wrong** (the `74`), **10 correct**; the eleven S4.3.4 cases are present and no earlier case was removed |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **67/67**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is so a reviewer can pin it. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it. S4.3.5 stops here for TD reassessment.**
