# Provenance register — `A1-C05-S4.3.8`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document** and as the two instrument files it describes. The mechanism is unchanged from S4.3 through S4.3.7: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. All four files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md` |
| Version | 4.3.8 (`A1-C05-S4.3.8`) |
| **Blob of this document** | **`3c6bab6c63b6ed47e82a490a8858819080695f86`** |
| Lines | 2,242 |
| Validator | `docs/validation/dv_c05.py`, blob **`cd1606c208e9db2d51b4267dff5099167ee29921`** |
| Regression suite | `docs/validation/test_dv_c05_regressions.py`, blob **`a99adaf674e8bc86f9f99f50040a5b59374cd608`** |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, the validator, the suite, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.7` at `f1beb0c07f643d56c15297529196fb6a4118a97b`, blob `0a0c36bec71f40d709878e67c19e4bca8f0b8b39`, 2,107 lines — **unmodified**. Its instruments are preserved at that commit: validator `06cfe2f24fb17b2540eab9e6f8fd12efdcc79a93`, suite `2a33543a8b6941262915e9a33b614411910b030b` |
| Earlier baselines, **unmodified** | S4.3.6 `034d091` / `e3a1fa85` (validator `840fed67`, suite `ee69f549`, register `ce1ebc8d`) · S4.3.5 `baa31db` / `a0b46f46` · S4.3.4 `90971e0` / `41df692d` · S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md
# 3c6bab6c63b6ed47e82a490a8858819080695f86   (must equal the field above)
git rev-parse HEAD:docs/validation/dv_c05.py                      # cd1606c208e9db2d51b4267dff5099167ee29921
git rev-parse HEAD:docs/validation/test_dv_c05_regressions.py     # a99adaf674e8bc86f9f99f50040a5b59374cd608
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_8.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 120/120
```

## What this revision is

**A final targeted correction, answering the two conditions and the one discrepancy in Agent 2's review of S4.3.7. No contract sentence changes, and nothing verified at S4.3.7 is weakened.**

| # | Finding | Disposition |
|---|---|---|
| **1** | Agent 2 `CONDITION-1` — `DV-22` read a **determiner-quantified denial** as an assignment (`No audio cue belongs to Agent 1.`) | **CLOSED** (§2.21). Three denial constructions added — the `no` / `none of the` quantifier with `belongs to`, with `is owned by`, and with the possessive — each spanning the mention. **No positive-attribution pattern was touched**: `TD-84` proves a genuine `belongs to` assignment still fails. Two of the three forms (`is owned by`, the possessive) are this revision's own probes, labelled as such |
| **2** | Agent 2 `CONDITION-2` — `DV-24`'s continuation gate rejected **every capitalised two-line wrap**, a missed hazard and a regression against S4.3.6 | **CLOSED** (§2.22). The gate is now a parameter set for **three-line windows only**; the block-boundary guard, the sentence-terminator guard and the single-pair rule are untouched and still carry the false-join defence. The inversion Agent 2 asked for is published: `S4.3.6 FAIL / S4.3.7 PASS / S4.3.8 FAIL` for all three capitalised wraps. Heading, blockquote, table-row, fence and list boundaries all remain closed |
| **3** | Agent 2 `MINOR-1` — the document's `DV-24` pair count was **8**; the runner printed **9** | **CLOSED** (§2.23). The figure is now measured from the finished text and stated once per location; §2.23 records the mechanism (a figure measured mid-draft and never re-measured) as the same class §5.4 warns about |
| — | Agent 2's §3.6 residual families (auxiliary/modal, perfect aspect, appositive `not`/`never` foil) | **NOT ADDRESSED, deliberately.** Non-blocking, outside the two authorised corrections, and adding them would be the general-purpose expansion the directive forbids. Recorded in §0.7.8 |

### Counts, derived by running the suite

**120** cases — the 106 carried forward plus 14 added: `TD-81`…`TD-85` (`DV-22`) and `TD-86`…`TD-94` (`DV-24`). `--compare` against the S4.3.7 validator (`/tmp/dv_s437.py`, blob `06cfe2f2`) shows **seven verdicts move**: four false alarms removed (`TD-81`, `TD-82`, `TD-83`, `TD-85`) and three missed hazards restored (`TD-86`, `TD-87`, `TD-88`). **All 106 carried-forward cases keep their expected verdicts** — including every S4.3.7 control — and the table is §13.3.8.

### Normative clauses: byte-identical

§5.2, §5.4, §8's preamble, `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, the six preserved clauses, the 17 case specifications, all 43 obligation rows and all 18 suites are carried forward without a character of change. `git diff f1beb0c -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md` is **empty**. No normative defect was demonstrated, so none is claimed, and `D-1`…`D-7` are not reopened. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and are untouched.**

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.7 and every earlier artifact and register; the same-commit register mechanism.

## Identity declaration (unchanged, restated so the register is self-contained)

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `arena/3bc206a0-tdd`, `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143` | authoritative S4.2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | `arena/c64fc525-tdd`, `99717e0` / `c800bf0`, blobs `eb774f5d…` / `61ef03b4…` | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | S4.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.1` | `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` | S4.3.1 |
| `TDD-A1-C05-SUCCESSOR-004.3.2` | `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` | S4.3.2 |
| `TDD-A1-C05-SUCCESSOR-004.3.3` | `40d29cca0bd2624fb731f4260145454a53a9860a`, blob `d827e017467b3bc320e2c5040a31f3aae0926d94` | S4.3.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.4` | `90971e052e0eb2cbb843fcc80bdb2d1b5fa8e444`, blob `41df692d3d80aa967c0f80326a47582957fa8eca` | S4.3.4 |
| `TDD-A1-C05-SUCCESSOR-004.3.5` | `baa31db3c631f0fc3e69a82b6d71207ad8061218`, blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` | S4.3.5 |
| `TDD-A1-C05-SUCCESSOR-004.3.6` | `034d091e1abcb507fdba6df4a05318a15aa5d7a1`, blob `e3a1fa85243a4749591363d4196bb5d65dad7c84` | S4.3.6 |
| `TDD-A1-C05-SUCCESSOR-004.3.7` | `f1beb0c07f643d56c15297529196fb6a4118a97b`, blob `0a0c36bec71f40d709878e67c19e4bca8f0b8b39` | S4.3.7, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.8` | this document, blob `3c6bab6c63b6ed47e82a490a8858819080695f86` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again, to the claim that no Agent 3 S4.3.7 review exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `f1beb0c` (before this push) · `arena/5dde91a4-tdd` `17af7be` (Agent 2's S4.3.7 review, read-only) · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.3.7 review present on any ref, at any reachable commit | **no** — three `AGENT3` files exist, all published before S4.3; `git grep` for `AGENT3_A1_C05_S4_3_7` and for `S4_3_7` inside `AGENT3*` over all **79** commits returns nothing |
| `git rev-parse f1beb0c:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md` | `0a0c36bec71f40d709878e67c19e4bca8f0b8b39` — the baseline is intact |
| `git diff f1beb0c -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md` | **empty** — the baseline was not edited |
| S4.3.7's instruments at `f1beb0c` | validator `06cfe2f2`, suite `2a33543a` — **intact** |
| Predicate diff vs `f1beb0c` | `docs/validation/dv_c05.py`: **+30 / −6** lines, confined to three denial constructions, the `require_cont` parameter and the `REG` constant |
| Suite diff vs `f1beb0c` | `docs/validation/test_dv_c05_regressions.py`: **+39 / −1** lines — 14 new cases; the single `−` line is the section anchor the new block is inserted before, **no existing case edited, renamed or removed** |
| Predecessor blobs at the tip | S4.3.7 `0a0c36be`, S4.3.6 `e3a1fa85`, S4.3.5 `a0b46f46`, S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_8.md` | **27/27 checks passed** — `DV-22` 0 offenders of 146 mentions, `DV-24` 10 pairs / 0 disagreeing / anchors 3/3, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / 8 owner checks / 0 failures |
| Same checker on earlier blobs | S4.3.7 **26/27**, S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — **every predecessor tally unchanged**; the single failure on each 26/27 row is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **120/120 cases behaved as required** |
| `--compare /tmp/dv_s437.py` | **7 verdicts move, all intended**: `TD-81`, `TD-82`, `TD-83`, `TD-85` **FAIL → PASS** (false alarms removed); `TD-86`, `TD-87`, `TD-88` **PASS → FAIL** (missed hazards restored); every other case stable (§13.3.8) |
| Preservation sweep | the S4.3.7 DV-22, DV-24 and DV-11 corrections re-checked individually: Agent 2's `MAJOR-1`/`MAJOR-2` texts still fail, the denial and contrast-object controls still pass, the four false-join boundaries still pass, the owner rule still fires on row 5 and still passes on the unmodified table |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **120/120**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text and the two instruments are so a reviewer can pin them. **No acceptance test is executed by anything recorded here, no behavioural claim is made from any of it, and the 120 regression cases are tests of the checker — not acceptance evidence.** **S4.3.8 stops here for independent review.**
