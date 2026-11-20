# Provenance register — `A1-C05-S4.3.7`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document** and as the two instrument files it describes. The mechanism is unchanged from S4.3 through S4.3.6: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. All four files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md` |
| Version | 4.3.7 (`A1-C05-S4.3.7`) |
| **Blob of this document** | **`0a0c36bec71f40d709878e67c19e4bca8f0b8b39`** |
| Lines | 2,107 |
| Validator | `docs/validation/dv_c05.py`, blob **`06cfe2f24fb17b2540eab9e6f8fd12efdcc79a93`** |
| Regression suite | `docs/validation/test_dv_c05_regressions.py`, blob **`2a33543a8b6941262915e9a33b614411910b030b`** |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, the validator, the suite, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.6` at `034d091e1abcb507fdba6df4a05318a15aa5d7a1`, blob `e3a1fa85243a4749591363d4196bb5d65dad7c84`, 1,931 lines — **unmodified**. Its instruments are preserved at that commit: validator `840fed6730a5b2e18a5f717f98c6de273b9c8721`, suite `ee69f549a5c684c211a3dc15878c69c6dc32afe8`, register `ce1ebc8d079f83aa594ef222ff71a108def1e8a6` |
| Earlier baselines, **unmodified** | S4.3.5 `baa31db` / `a0b46f46` · S4.3.4 `90971e0` / `41df692d` · S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md
# 0a0c36bec71f40d709878e67c19e4bca8f0b8b39   (must equal the field above)
git rev-parse HEAD:docs/validation/dv_c05.py                      # 06cfe2f24fb17b2540eab9e6f8fd12efdcc79a93
git rev-parse HEAD:docs/validation/test_dv_c05_regressions.py     # 2a33543a8b6941262915e9a33b614411910b030b
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_7.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 106/106
```

## What this revision is

**A validator revision, answering the two independent reviews of S4.3.6. No contract sentence changes.**

### The three finding areas, resolved one by one

| Area | Reported | Disposition |
|---|---|---|
| **A — `DV-22` attribution** | Agent 2 `MAJOR-1` (possessive synonym), Agent 2 `MAJOR-2` (foil longer than the 32-character window), Agent 3's "positive-ownership escape" | **`MAJOR-1` and `MAJOR-2` reproduced and closed** (`TD-61`, `TD-62`). They are **distinct** defects — one a lexicon never taught, one a distance-bounded rule — and each test fails for exactly one of them. **Agent 3's escape is `OPEN — ARTIFACT ABSENT` and deliberately unpaired**: its review is on no ref and at none of the 78 reachable commits. Instead of guessing it, this revision probed the family and closed **seven further members** (`belongs to`, `selected by`, `ownership is …'s`, `cue's owner is`, `Agent 1 's`, `whose owner is`, dash attribution), labelled `P1`…`P9` as this revision's own probes. Two new false positives the widening created (`do not belong to`, the contrast object) were caught by controls and taken back (`TD-66`, `TD-67`) |
| **B — `DV-24` wrapped contradictions and false joining** | Agent 2 `MINOR-1` (three-line wrap); Agent 3 (three-line wraps; unrelated adjacent facts falsely joined) | **The two three-line reports are the same defect** and are closed by a guarded join of up to three lines (`TD-71`, `TD-72`). **The false-joining report is a distinct defect, and the S4.3.6 validator already committed it**: `- declared 6` followed by `- observed 5` was welded into a `(6, 5)` contradiction and failed the document. `TD-75` records that `FAIL → PASS` flip. Four guards — block boundary, sentence terminator, continuation, one label of each kind per window — with four controls (`TD-73`…`TD-76`) |
| **C — `DV-11` owner column** | Agent 3 reports the owner-column claim unenforced; TD asks whether `TD-60` isolates it | **Confirmed and closed by direct enforcement.** `TD-60` fails under both validators because **row 7 is outside `TN-C`'s `{5, 6}`** — it exercises the *allowed-row* rule, never ownership, and its row has the correct owner. The §5.4 owner clause is now its own rule: the row-owner map is declared and **verified against §5.2's own text at run time**, token agents are read from §5.4's `Agent` column, and each declared row's owner must intersect the token's agent. `TD-77` is the **discriminator** — row 5 is inside the allowed set, so only ownership can reject it, and the document moves `PASS → FAIL` between validators. `TD-78` (correct evidence), `TD-79` (dual-owned row legal) and `TD-80` (allowed-row rule still fires alone) complete the set |

### Counts, derived by running the suite

**106** cases — the 86 carried forward plus 20 added: `TD-61`…`TD-70` (`DV-22`), `TD-71`…`TD-76` (`DV-24`), `TD-77`…`TD-80` (`DV-11`). `--compare` against the S4.3.6 validator (`/tmp/dv_s436.py`, blob `840fed67`) shows **ten verdicts move**: eight `PASS → FAIL` that had to fail (`TD-61`…`TD-65`, `TD-71`, `TD-72`, `TD-77`) and two `FAIL → PASS` that were **false positives** (`TD-67`, `TD-75`). **No pre-existing case regressed**; the table is §13.3.7.

### Normative clauses: byte-identical

§5.2, §5.4, §8's preamble, `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, the six preserved clauses, the 17 case specifications, all 43 obligation rows and all 18 suites are carried forward without a character of change. `git diff 034d091 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md` is **empty**: the baseline was not touched. No normative defect was demonstrated, so none is claimed, and `D-1`…`D-7` are not reopened. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and are untouched.**

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.6 and every earlier artifact and register; the same-commit register mechanism.

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
| `TDD-A1-C05-SUCCESSOR-004.3.6` | `034d091e1abcb507fdba6df4a05318a15aa5d7a1`, blob `e3a1fa85243a4749591363d4196bb5d65dad7c84` | S4.3.6, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.7` | this document, blob `0a0c36bec71f40d709878e67c19e4bca8f0b8b39` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again, to the claim that no Agent 3 S4.3.6 review exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `034d091` (before this push) · `arena/5dde91a4-tdd` `759ef10` (Agent 2's S4.3.6 review, read-only) · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.3.6 review present on any ref, at any reachable commit | **no** — three `AGENT3` files exist, all published before S4.3; `git grep` for `AGENT3_A1_C05_S4_3_6` and for `S4_3_6` inside `AGENT3*` over all **78** commits returns nothing |
| `git rev-parse 034d091:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md` | `e3a1fa85243a4749591363d4196bb5d65dad7c84` — the baseline is intact |
| `git diff 034d091 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md` | **empty** — the baseline was not edited |
| S4.3.6's instruments at `034d091` | validator `840fed67`, suite `ee69f549`, register `ce1ebc8d` — **all intact** |
| Predicate diff vs `034d091` | `docs/validation/dv_c05.py`: **+162 / −17** lines, confined to the agent-name tokens and their derivations, the clause-bounded foil test, the contrast-object test, the `DV-24` guarded join and the `DV-11` owner rule, plus the `REG` constant |
| Suite diff vs `034d091` | `docs/validation/test_dv_c05_regressions.py`: **+67 / −0** lines — 20 new cases; **no existing case edited, renamed or removed** |
| Predecessor blobs at the tip | S4.3.6 `e3a1fa85`, S4.3.5 `a0b46f46`, S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_7.md` | **27/27 checks passed** — `DV-22` 0 offenders of 138 mentions, `DV-24` 8 pairs / 0 disagreeing / anchors 3/3, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / **8 owner checks (map verified)** / 0 failures |
| Same checker on earlier blobs | S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — **every predecessor tally is unchanged from S4.3.6**; the single failure on each 26/27 row is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **106/106 cases behaved as required** |
| `--compare /tmp/dv_s436.py` | **10 verdicts move, all intended**: `TD-61`…`TD-65`, `TD-71`, `TD-72`, `TD-77` **PASS → FAIL**; `TD-67`, `TD-75` **FAIL → PASS** (false positives removed); ten controls stable (§13.3.7) |
| False-positive sweep | **0** on 24 valid-denial and benign-co-occurrence probes; `DV-24`'s four false-join controls pass |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **106/106**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text and the two instruments are so a reviewer can pin them. **No acceptance test is executed by anything recorded here, no behavioural claim is made from any of it, and the 106 regression cases are tests of the checker — not acceptance evidence.** **S4.3.7 stops here for TD reassessment.**
