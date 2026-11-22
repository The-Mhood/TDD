# Provenance register — `A1-C05-S4.3.10`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document** and as the two instrument files it describes. The mechanism is unchanged from S4.3 through S4.3.9: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. All four files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md` |
| Version | 4.3.10 (`A1-C05-S4.3.10`) |
| **Blob of this document** | **`857778e18a35b35b1a5420905ec5f1482fddf868`** |
| Lines | 2,441 |
| Validator | `docs/validation/dv_c05.py`, blob **`353a2bff220d4daa4c176daafc941256098959ed`** |
| Regression suite | `docs/validation/test_dv_c05_regressions.py`, blob **`7ab55805c27a271706f16e9295f1f503dc5a6c94`** |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, the validator, the suite, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.9` at `83c24f9ce974c8194d5788d62c28043cc7511974`, blob `72d218a865b6713f78cb22308fa3dea81c74ac39`, 2,349 lines — **unmodified**. Its instruments are preserved at that commit: validator `50635db370793a02969d42cadaa0d352b1d7bbf2`, suite `c140a82f9ab32cb11cdb8494fbe9c928f4f48b6e` |
| Earlier baselines, **unmodified** | S4.3.8 `c4761f5` / `3c6bab6c` (validator `cd1606c2`, suite `a99adaf6`) · S4.3.7 `f1beb0c` / `0a0c36be` (validator `06cfe2f2`, suite `2a33543a`) · S4.3.6 `034d091` / `e3a1fa85` (validator `840fed67`, suite `ee69f549`, register `ce1ebc8d`) · S4.3.5 `baa31db` / `a0b46f46` · S4.3.4 `90971e0` / `41df692d` · S4.3.3 `40d29cc` / `d827e017` · S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md
# 857778e18a35b35b1a5420905ec5f1482fddf868   (must equal the field above)
git rev-parse HEAD:docs/validation/dv_c05.py                      # 353a2bff220d4daa4c176daafc941256098959ed
git rev-parse HEAD:docs/validation/test_dv_c05_regressions.py     # 7ab55805c27a271706f16e9295f1f503dc5a6c94
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 147/147
```

## What this revision is

**A targeted closure of `F-1b`, reported at S4.3.9 and authorised by TD as a separate, narrowly scoped cycle. No contract sentence changes, and nothing verified at S4.3.9 is weakened.**

| # | Finding | Disposition |
|---|---|---|
| **1** | `F-1b` — `No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.` passed `DV-22`. The S4.3.6 **object-negation** construction read `(?:\bnot\|,)` followed by `the` / `any` + the audio noun, so its **bare comma alternative** matched `, the audio` with no negator anywhere near it, and — because a denial excuses a mention only when its match spans it — negated the object of a clause that *asserts* ownership | **CLOSED** (§2.25, `TD-104`…`TD-121`). The construction is now `\bnot\s+(?:the\s+\|any\s+)` + modifiers + `audio`. **One alternation removed, nothing added**: the `the` / `any` requirement, the modifier class, the noun, the case-insensitivity and the positional rule are untouched |
| **2** | TD's instruction: *do not assume that every comma followed by an ownership-related phrase is contradictory* | **HONOURED BY CONSTRUCTION, NOT BY EXCEPTION.** The comma was never the trigger for a legitimate form: `, not the audio` and `,not the audio` are both matched by `not`, with or without a space after the comma, so the comma alternative covered **no intended form at all**. Five preserved legitimate forms are cases (`TD-109`…`TD-113`), not claims |
| **3** | The smallest correct change, and the alternatives rejected | `never` was **not** added to the negators (a widening, and Agent 2's §3.6 appositive family); a structure-sensitive "negated object must follow a verb" rule was **not** written (a redesign); a comma-plus-negator branch was **not** kept (unreachable, hence dead code). All four candidates and their effects are tabulated in §2.25 |

### Counts, derived by running the suite

**147** cases — the 129 carried forward plus 18 added: `TD-104`…`TD-121` in §5j. `--compare` against the S4.3.9 validator (`/tmp/dv_s439.py`, blob `50635db3`) shows **five verdicts move**, all in the closed direction: `TD-104`, `TD-105`, `TD-106`, `TD-107`, `TD-108` **PASS → FAIL**. **All 129 carried-forward cases keep their expected verdicts**, including every `F-1` case, every `CONDITION-1` and `CONDITION-2` case, the seven `_joinable` boundaries and the false-join and continuation controls; the table is §13.3.10.

### Normative clauses: byte-identical

§5.2, §5.4, §8's preamble, `TN-C-11`, `TN-C-14` (one frame on the shared axis), `TN-C-15`, `TN-A-01`…`TN-A-03`, `T-C05-63`, `T-C05-64`, the six preserved clauses, the 17 case specifications, all 43 obligation rows and all 18 suites are carried forward without a character of change. `git diff 83c24f9 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md` is **empty**. No normative defect was demonstrated, so none is claimed, and `D-1`…`D-7` are not reopened. **`TN-C-11` / `TN-A-01` / `TN-A-02` remain unresolved and are untouched.**

**Preserved, exactly:** 43 obligations (19 P / 15 C / 6 R / 3 A), 18 suites, 67 proposed acceptance cases `PROPOSED / NOT RUN`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.9 and every earlier artifact and register; the same-commit register mechanism.

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
| `TDD-A1-C05-SUCCESSOR-004.3.9` | `83c24f9ce974c8194d5788d62c28043cc7511974`, blob `72d218a865b6713f78cb22308fa3dea81c74ac39` | S4.3.9, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.10` | this document, blob `857778e18a35b35b1a5420905ec5f1482fddf868` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again, to the claim that no Agent 3 review of S4.3.9 exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `83c24f9` (before this push) · `arena/5dde91a4-tdd` **`0769248`** (Agent 2's final verification of S4.3.8 — present and read) · `arena/b2c58152-tdd` `7d22836` (Agent 4 UE5 material, unrelated) · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.3.9 review present on any ref, at any reachable commit | **no** — three `AGENT3` files exist, all published before S4.3; a grep for `AGENT3` and `S4_3_9` across every reachable commit returns no fourth Agent 3 artifact |
| `git rev-parse 83c24f9:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md` | `72d218a865b6713f78cb22308fa3dea81c74ac39` — the baseline is intact |
| `git diff 83c24f9 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md` | **empty** — the baseline was not edited |
| S4.3.9's instruments at `83c24f9` | validator `50635db3`, suite `c140a82f` — **intact** |
| Predicate diff vs `83c24f9` | `docs/validation/dv_c05.py`: **+11 / −3** lines, confined to one construction (one alternation removed), its comment and the `REG` constant |
| Suite diff vs `83c24f9` | `docs/validation/test_dv_c05_regressions.py`: **+50 / −0** lines — 18 new cases and their section header; **no existing case edited, renamed or removed** |
| Predecessor blobs at the tip | S4.3.9 `72d218a8`, S4.3.8 `3c6bab6c`, S4.3.7 `0a0c36be`, S4.3.6 `e3a1fa85`, S4.3.5 `a0b46f46`, S4.3.4 `41df692d`, S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_10.md` | **27/27 checks passed** — `DV-22` 0 offenders of 165 mentions, `DV-24` 10 pairs / 0 disagreeing / anchors 3/3, `DV-11` 7 declared / 5 observed / 43 cells / 7 cell-count claims / 8 owner checks / 0 failures |
| Same checker on earlier blobs | S4.3.9 **25/27** (`DV-27`, plus `DV-22` on **one** offender — its own §2.24 prose reproduction of `F-1b`, which S4.3.10 moves into a `[QUOTED]` table: the validator is not silenced, the quotation is labelled), S4.3.8 **26/27**, S4.3.7 **26/27**, S4.3.6 **26/27**, S4.3.5 **26/27**, S4.3.4 **26/27**, S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — **every predecessor tally unchanged from S4.3.9**; the single failure on each 26/27 row is `DV-27`, the register that pins *this* document |
| Per-document offender counts, before vs after the fix | identical on **every** document except one: S4.3.10 **0**, S4.3.8 … S4.3 **0**, S4.2/S4.1/S4.0 **2** each, S3 **1**. The single change is S4.3.9, **0 → 1**, and that offender is its own prose reproduction of the `F-1b` sentence — correct behaviour, fixed in this text by quoting it inside a `[QUOTED]` table |
| `python3 docs/validation/test_dv_c05_regressions.py` | **147/147 cases behaved as required** |
| `--compare /tmp/dv_s439.py` | **5 verdicts move, all intended**: `TD-104`…`TD-108` **PASS → FAIL** (the fail-open, now caught); every carried case stable, and the 13 other new cases stable (§13.3.10) |
| The reproduced case, checked for the right reason | `TD-104` fails with **one offender** (the second mention) and the first mention stays excused by the quantified denial about Agent 2 — the assertion is no longer covered, and the true denial still is |
| Preservation sweep | `TD-81`…`TD-85` (`CONDITION-1`) still `PASS`; `TD-86`…`TD-88` (`CONDITION-2`) still `FAIL`; `TD-89`…`TD-94` unchanged; `TD-95`…`TD-103` (`F-1`, S4.3.9) unchanged; `TD-71`…`TD-76` and `TD-90`…`TD-93` (the seven boundaries and false-join controls) closed; `TD-50` (the original object negation) still `PASS` |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **147/147**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text and the two instruments are so a reviewer can pin them. **No acceptance test is executed by anything recorded here, no behavioural claim is made from any of it, and the 147 regression cases are tests of the checker — not acceptance evidence.** **S4.3.10 stops here for independent review.**
