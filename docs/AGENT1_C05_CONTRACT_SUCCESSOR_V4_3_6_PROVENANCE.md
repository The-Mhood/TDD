# Provenance register — `A1-C05-S4.3.6`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document** and as the two instrument files it describes. The mechanism is unchanged from S4.3 through S4.3.5: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. All four files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md` |
| Version | 4.3.6 (`A1-C05-S4.3.6`) |
| **Blob of this document** | **`e3a1fa85243a4749591363d4196bb5d65dad7c84`** |
| Lines | 1,931 |
| Validator | `docs/validation/dv_c05.py`, blob **`840fed6730a5b2e18a5f717f98c6de273b9c8721`** |
| Regression suite | `docs/validation/test_dv_c05_regressions.py`, blob **`ee69f549a5c684c211a3dc15878c69c6dc32afe8`** |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, the validator, the suite, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.5` at `baa31db3c631f0fc3e69a82b6d71207ad8061218`, blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb`, 1,779 lines — **unmodified**. Its instrument blobs are preserved at that commit: validator `6927644fb2a684024b3acc722ede0f0b610fc7d9`, suite `954588d324fa9ff64d5801fd0f2ddbe45624b408` |
| Earlier baselines, **unmodified** | S4.3.4 `90971e0` / `41df692d` · S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md
# e3a1fa85243a4749591363d4196bb5d65dad7c84   (must equal the field above)
git rev-parse HEAD:docs/validation/dv_c05.py                      # 840fed67…
git rev-parse HEAD:docs/validation/test_dv_c05_regressions.py     # ee69f549…
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 86/86
```

## What this revision is

**A validator revision, answering TD's directive on two independent reviews of S4.3.5. No contract sentence changes.**

**The three finding areas, and what is actually closed.**

| Finding | Source | Disposition |
|---|---|---|
| `DV-22` attribution admitted two ownership sentences | **Agent 2's `MAJOR-1`**, reproduced on the published blob | **CLOSED** — §2.15. The synonym is read through a named group and contrastive foils are skipped; the foil that named the wrong agent was also a false **positive** (`TD-47`), and it is fixed too. One measured departure from Agent 2's recipe is documented: `whereas` is **not** a foil, because dropping it loses a true positive |
| `DV-24` false negatives | **Agent 3's review — NOT IN THIS REPOSITORY** (§0.9: absent from every ref and all 76 reachable commits) | **`OPEN — ARTIFACT ABSENT`.** Three *different* `DV-24` false negatives were found by this revision's own probing and **are** closed (`A1-P1`…`A1-P3`, §2.16, `TD-52`…`TD-54`) — additional, **not** a substitute, and not described as Agent 3's |
| `DV-11` enforcement gap | Agent 2 reports an independent reimplementation with 0 failures; Agent 3 reports a narrower gap — **also absent** | **Reconciled and closed on this revision's own reproduction** (§2.17, `A1-P4`…`A1-P6`, `TD-56`…`TD-60`): the declaration parser read only the first number, the allowed-row test was an intersection instead of a **subset**, and §5.4's hand cell counts were never compared. Agent 2's 0-failure result is consistent — a correct document cannot distinguish a subset rule from an intersection rule. **Agent 3's narrower claim stays `OPEN — ARTIFACT ABSENT`** |

**No invented examples.** Every counterexample this revision closes is either Agent 2's, verbatim (§2.15), or was **reproduced by this revision before it was fixed** and is published as a mutation with its before/after verdict (§2.16, §2.17, §13.3.6). Nothing is attributed to Agent 3.

**The count, derived by running the suite, not assumed.** **86** cases — the 67 carried forward plus 19 added: `TD-42`…`TD-51` (`DV-22`), `TD-52`…`TD-55` (`DV-24`), `TD-56`…`TD-60` (`DV-11`). Before/after against the `baa31db` validator (`/tmp/dv_s435.py`, blob `6927644f`) shows **12 verdicts move** — eleven `PASS → FAIL` on cases that had to fail and one `FAIL → PASS` (`TD-47`, a false positive) — and **no pre-existing case regressed**. The whole table is §13.3.6.

**Normative clauses: byte-identical.** §5.2, §8's preamble, `TN-C-11`, `TN-C-14`, `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, all 43 obligation rows and all 18 suites are carried forward without a character of change. `git diff baa31db -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md` is **empty**: the baseline was not touched. No normative defect was demonstrated, so none is claimed, and `D-1`…`D-7` are not reopened.

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.5 and every earlier artifact and register; the same-commit register mechanism. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and are not touched here.**

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
| `TDD-A1-C05-SUCCESSOR-004.3.5` | `baa31db3c631f0fc3e69a82b6d71207ad8061218`, blob `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` | S4.3.5, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.6` | this document, blob `e3a1fa85243a4749591363d4196bb5d65dad7c84` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again, this time to **two** claims: that no Agent 3 S4.2 report exists, and that the Agent 3 S4.3.5 QA review named in the directive does not exist either.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `baa31db` (before this push) · `arena/5dde91a4-tdd` `659944b` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.3.5 QA review present on any ref, at any reachable commit | **no** — `git grep -l` for `S4_3_5_INDEPENDENT_INTEGRATION_QA` and `INTEGRATION_QA_REVIEW` over all **76** commits of `git rev-list --all` returns nothing; only three Agent 3 files exist, all published before S4.3, and none mentions `DV-24` |
| Agent 3 S4.2 review present | **no** — unchanged from S4.3.5 |
| `git rev-parse baa31db:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md` | `a0b46f46c81e85cea5d04b940aaf9aee46c19deb` — the baseline is intact |
| `git diff baa31db -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md` | **empty** — the baseline was not edited |
| Predicate diff vs `baa31db` | `docs/validation/dv_c05.py`: **+80 / −13** lines, confined to `DV-22`'s reference pattern and attribution, `DV-24`'s pair patterns and cross-line scan, `DV-11`'s declaration parser, subset rule and cell-count comparison, and the `REG` constant |
| Suite diff vs `baa31db`'s blob | `docs/validation/test_dv_c05_regressions.py`: **+64 / −0** lines — 19 new cases and one helper; **no existing case edited, renamed or removed** |
| Predecessor blobs at the tip | S4.3.5 `a0b46f46`, S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_6.md` | **27/27 checks passed** — `DV-22` 0 offenders of 137 mentions, `DV-24` 24 pairs / 0 disagreeing / anchors 3/3, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / 0 failures |
| Same checker on earlier blobs | S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — **every predecessor tally is unchanged from S4.3.5**; the single failure on each of them is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **86/86 cases behaved as required** |
| `--compare /tmp/dv_s435.py` | **12 verdicts move, all intended**: `TD-42`…`TD-46`, `TD-52`…`TD-54`, `TD-56`…`TD-58` **PASS → FAIL**; `TD-47` **FAIL → PASS**; `TD-48`…`TD-51`, `TD-55`, `TD-59`, `TD-60` stable (§13.3.6) |
| The two escapes on a copy of the live document | `DV-22` **fails** on both of Agent 2's counterexamples; `DV-24` **fails** on all three of this revision's; `DV-11` **fails** on all three of this revision's (§2.15–§2.17) |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **86/86**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text and the two instruments are so a reviewer can pin them. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it. S4.3.6 stops here for TD reassessment.**
