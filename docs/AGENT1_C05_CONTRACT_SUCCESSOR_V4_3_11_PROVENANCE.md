# Provenance register — `A1-C05-S4.3.11`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document** and as the two instrument files it describes. The mechanism is unchanged from S4.2 through S4.3.10: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. All four files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md` |
| Version | 4.3.11 (`A1-C05-S4.3.11`) |
| **Blob of this document** | **`1929551681d6f6852076606384e22ad1424e266e`** |
| Lines | 2,581 |
| Validator | `docs/validation/dv_c05.py`, blob **`9e88c5a44c09788646198cbd77c4259c82534efe`** |
| Regression suite | `docs/validation/test_dv_c05_regressions.py`, blob **`ca0a4f902de74180fbf165013462a728130ddb07`** |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, the validator, the suite, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.10` at `7662926c4c3b7293daedcc393c0ec4d015cdd883`, blob `857778e18a35b35b1a5420905ec5f1482fddf868`, 2,441 lines — **unmodified**. Its instruments are preserved at that commit: validator `353a2bff220d4daa4c176daafc941256098959ed`, suite `7ab55805c27a271706f16e9295f1f503dc5a6c94` |
| Its accepted verification | `50578ed` — `TDD-A2-FINAL-VERIFY-C05-003` v1.0, `PASS WITH UNRELATED LIMITATIONS`, read-only |
| **The assessment this revision implements** | `f0f80b9810d71a46e125b55644f7bf28d121dcd8` — `TDD-A2-ASSESS-C05-RESIDUAL-001` v1.0, `Docs/AGENT2_ASSESS_C05_RESIDUAL_V1.md`, 424 lines, **read only, not modified** |
| Earlier baselines, **unmodified** | S4.3.9 `83c24f9` / `72d218a8` · S4.3.8 `c4761f5` / `3c6bab6c` · S4.3.7 `f1beb0c` / `0a0c36be` · S4.3.6 `034d091` / `e3a1fa85` · S4.3.5 `baa31db` / `a0b46f46` · S4.3.4 `90971e0` / `41df692d` · S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md
# 1929551681d6f6852076606384e22ad1424e266e   (must equal the field above)
git rev-parse HEAD:docs/validation/dv_c05.py                      # 9e88c5a44c09788646198cbd77c4259c82534efe
git rev-parse HEAD:docs/validation/test_dv_c05_regressions.py     # ca0a4f902de74180fbf165013462a728130ddb07
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_11.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 164/164
```

## What this revision is

**The correction TD authorised after Agent 2's residual-family assessment: `D-a` and `D-b`, in the measured `A+D` form. No contract sentence changes, and every verdict verified at S4.3.10 keeps its expectation.**

| # | Finding | Disposition |
|---|---|---|
| **1** | `D-a` — `DV-22`'s **object-negation** construction read `\bnot` alone, so a **true** denial failed: `Agent 1 owns the camera, never the audio cues.` was rejected although `TN-C-15` gives audio to Agent 2 alone. Agent 2's `R-1`, `R-1b`, `R-1c`; the only **fail-closed** family and the only one reachable in the contract's own voice | **CLOSED** (§2.26.1, `TD-122`…`TD-124`). The construction is now `(?:\bnot|\bnever)\s+(?:the\s+|any\s+)` + modifiers + `audio`. **`never` enters this site only** — not `NEG_AFTER`, not `_FOIL_ANY`, because a general substitution of the pair re-opens the `not only` positive claim |
| **2** | `D-b` — the passive was read only as `is\|are\|was\|were` + participle, so `has been owned by`, `had been owned by` and the **zero-copula** appositive `supplied by Agent 1` were invisible. Agent 2's `R-3b`, `R-5`, `R-5b`, `R-5c`; `R-5b` has no commas, so the missing copula — not punctuation — is the mechanism | **CLOSED** (§2.26.2, `TD-125`…`TD-136`). Three alternatives: simple copula, `has\|have\|had` + `been`, and a **guarded** bare participle; and the quantified denial reads the same chain, so a legitimate denial is still a denial |
| **3** | **A measured departure from the variant as assessed, disclosed rather than absorbed** | Implemented exactly as "the copula made optional", the pattern also reads a **negated** passive as an assignment: **eight** new false alarms on legitimate denials (`are not provided by`, `are not supplied by`, `have never been owned by`, `were not owned by`, `are not selected by`, `No audio cue has been owned by`, `None of the audio cues have been owned by`, `No audio cue had been supplied by`). The zero-copula guard (`not` / `never` / `been` immediately before the participle) and the denial-side widening remove all eight. **Measured after: `12/14` probes, `26/26` controls, `27/27` document, `164/164` suite, 0 wrong on a seventeen-shape edge set** |
| **4** | `D-c` (the foil markers, `R-4`/`R-4b`) | **DEFERRED**, as recommended and as directed — the verdicts are **unchanged** (`PASS`, i.e. still missed) and `TD-137`/`TD-138` pin them so a later cycle must move them deliberately |
| **5** | `D-d` (a participle content taxonomy) | **REFUSED** — not a grammar fix |
| **6** | `F-1b` | **NOT REOPENED.** Its construction, its stated-negation requirement and `TD-104`…`TD-108` are untouched and re-run |

### Counts, derived by running the suite

**164** cases — the 147 carried forward plus 17 added: `TD-122`…`TD-138` in §5k. `--compare` against the S4.3.10 validator (`/tmp/dv_s4310.py`, blob `353a2bff`) shows **exactly eight verdicts move**, all intended: `TD-122`…`TD-124` **FAIL → PASS** (the fail-closed denials, now accepted) and `TD-125`…`TD-129` **PASS → FAIL** (the unattributed passives, now caught). **No carried-forward case moves**, including the two deferred `R-4` pins and every one of the twenty-six required controls.

### Normative clauses: byte-identical

§5.2, §5.4, §8's preamble, `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, the six preserved clauses, the 17 case specifications, all 43 obligation rows and all 18 suites — unchanged by this revision, which edits **no** contract text.

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` is superseded); the eight-row decision table of S4.2; the staleness bound `TN-C-14`; `U-07` open; `F-1b` closed.

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
| `TDD-A1-C05-SUCCESSOR-004.3.7` | `f1beb0c07f643d56c15297529196fb6a4118a97b`, blob `0a0c36bec71f40d709878e67c19e4bca8f0b8b39` | S4.3.7 |
| `TDD-A1-C05-SUCCESSOR-004.3.8` | `c4761f52003958fb95c405db56591063f255f55f`, blob `3c6bab6c63b6ed47e82a490a8858819080695f86` | S4.3.8 |
| `TDD-A1-C05-SUCCESSOR-004.3.9` | `83c24f9ce974c8194d5788d62c28043cc7511974`, blob `72d218a865b6713f78cb22308fa3dea81c74ac39` | S4.3.9 |
| `TDD-A1-C05-SUCCESSOR-004.3.10` | `7662926c4c3b7293daedcc393c0ec4d015cdd883`, blob `857778e18a35b35b1a5420905ec5f1482fddf868` | S4.3.10, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.11` | this document, blob `1929551681d6f6852076606384e22ad1424e266e` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again, to the claim that no Agent 3 review of S4.3.10 exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `6a7da5b` (before this push) · `arena/5dde91a4-tdd` **`f0f80b9`** (Agent 2's residual-family assessment — present and read) · `arena/b2c58152-tdd` `7d22836` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 review of S4.3.10 present on any ref, at any reachable commit | **no** — the tree holds exactly **three** `AGENT3` files, all on `arena/c64fc525-tdd` (S1 integration readiness, the S4.1 independent review, the C-05.3 telegraph-authority recommendation): **none of them S4.3.10**, and none is on this branch at all |
| `git rev-parse 7662926:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md` | `857778e18a35b35b1a5420905ec5f1482fddf868` — the baseline is intact |
| `git diff 7662926 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md` | **empty** — the baseline was not edited |
| S4.3.10's instruments at `7662926` | validator `353a2bff`, suite `7ab55805` — **intact** |
| Predicate diff vs `7662926` | `docs/validation/dv_c05.py`: **+31 / −6** lines, confined to three constructions (the object negator, the passive attribution, the quantified denial), their comments, one shared participle constant and the `REG` constant |
| Suite diff vs `7662926` | `docs/validation/test_dv_c05_regressions.py`: **+48 / −0** lines — 17 new cases and their section header; **no existing case edited, renamed or removed** |
| Predecessor blobs at the tip | S4.3.10 `857778e1`, S4.3.9 `72d218a8`, S4.3.8 `3c6bab6c`, S4.3.7 `0a0c36be`, S4.3.6 `e3a1fa85`, S4.3.5 `a0b46f46`, S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027` — unchanged |
| `python3 docs/validation/dv_c05.py docs/…V4_3_11.md` | **27/27 checks passed** — `DV-22` 0 offenders of 169 mentions, `DV-24` 10 pairs / 0 disagreeing / anchors 3/3, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / 8 owner checks |
| Same checker on earlier blobs | S4.3.10 **26/27** (`DV-27` only — it names its own register), `DV-22` **0 offenders of 165 mentions** on it, so the correction fires on nothing new; S4.3.9 **25/27** (`DV-22` + `DV-27`); S4.3.8 … S4.3.1 and S4.3 **26/27**; S4.2 **24/27**; S4.1 **21/27**; S4.0 **21/27**; S3 **10/27** — **every predecessor tally matches the one S4.3.10 published** |
| `python3 docs/validation/test_dv_c05_regressions.py` | **164/164 cases behaved as required** |
| `--compare /tmp/dv_s4310.py` | **8 verdicts move, all intended**: `TD-122`…`TD-124` **FAIL → PASS**, `TD-125`…`TD-129` **PASS → FAIL**; every carried case and all 17 other new cases stable |
| The fourteen probes | **12/14** correct — `R-1`, `R-1b`, `R-1c`, `R-3b`, `R-5`, `R-5b`, `R-5c` closed; `R-2`, `R-2b`, `R-3`, `R-6`, `R-7` correct and unmoved; **`R-4`, `R-4b` still `PASS` (unchanged, as directed)** |
| The twenty-six controls | **26/26**, unchanged from S4.3.10 |
| The independent edge set (seventeen shapes: ten denials that must pass, seven assignments that must fail) | **17/17** under this revision; the plain, unguarded variant scores **7 wrong** and the naive optional copula **8 wrong** |
| Preservation sweep | `TD-104`…`TD-108` (`F-1b`) unchanged; `TD-81`…`TD-85` (`CONDITION-1`) `PASS`; `TD-86`…`TD-89` (`CONDITION-2`) `FAIL`; `TD-116`…`TD-121` unchanged; `TD-71`…`TD-76`, `TD-90`…`TD-94` (boundaries) unchanged; `TD-40` unchanged |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **164/164**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text and the two instruments are so a reviewer can pin them.
