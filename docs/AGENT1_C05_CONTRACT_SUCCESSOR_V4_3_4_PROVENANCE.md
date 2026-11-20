# Provenance register — `A1-C05-S4.3.4`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document**. The mechanism is unchanged from S4.3 through S4.3.3: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. Both files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_4.md` |
| Version | 4.3.4 (`A1-C05-S4.3.4`) |
| **Blob of this document** | **`41df692d3d80aa967c0f80326a47582957fa8eca`** |
| Lines | 1,730 |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, `docs/validation/dv_c05.py`, `docs/validation/test_dv_c05_regressions.py`, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.3` at `40d29cca0bd2624fb731f4260145454a53a9860a`, blob `d827e017467b3bc320e2c5040a31f3aae0926d94`, 1,657 lines — **unmodified** |
| Earlier baselines, **unmodified** | S4.3.2 `b754deb` / `74840d70` · S4.3.1 `db95404` / `c8708ef0` · S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_4.md
# 41df692d3d80aa967c0f80326a47582957fa8eca   (must equal the field above)
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_4.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 67/67
```

## What this revision is

**A targeted revision of S4.3.3, answering the two residual `DV-22` conditions in TD's S4.3.3 review.** Both reproduce on the published blob, and both come from the same place: the trailing-denial rule treated *"no agent is named"* as evidence that the first agent is excluded.

**Condition A — an unnamed denial must not excuse a positive Agent 1 ownership assertion.** `negated_mention()` ended with `if not named or named[0] == '1': return True`. The first disjunct accepted any post-mention denial that named nobody, so a line asserting that the first agent owns cue selection, followed by an unnamed `is not owned`, was called a denial. An unnamed denial is now accepted only when it carries an explicit **universal** term (`nobody`, `no one`, `anyone`) **and** the same clause does not also assert that the first agent owns the cues.

**Condition B — the missing relative-clause boundary.** `_NOT_CROSS` stopped a denial from crossing a comma, semicolon, sentence end, dash, conjunction or relative pronoun, but not `that`. So *"owns … cues that are not owned by anyone"* was accepted while the `which` form was rejected: the boundary, not the grammar, was deciding the verdict. `that` is now a phrase boundary.

**One judgement recorded rather than hidden:** the possessive universal form (the first agent's name in the possessive, then a universal denial of ownership of the same cues) is now an offender, pinned as `TD-41`, because the wording does not genuinely exclude the first agent.

**Five new false negatives reproduced and closed; eleven permanent cases added.**

| Case | Requirement | S4.3.3 predicate | S4.3.4 predicate |
|---|---|---|---|
| `TD-31` unnamed denial, `that` relative clause | FAIL | PASS — missed | FAIL |
| `TD-32` unnamed denial with a stated object | FAIL | PASS — missed | FAIL |
| `TD-33` universal denial inside a `that` relative clause | FAIL | PASS — missed | FAIL |
| `TD-40` universal denial, then a first-agent ownership phrase | FAIL | PASS — missed | FAIL |
| `TD-41` universal denial beside a possessive assertion | FAIL | PASS — missed | FAIL |
| `TD-34` explicit denial naming the first agent | PASS | PASS | PASS |
| `TD-35` genuine universal exclusion | PASS | PASS | PASS |
| `TD-37` `NEG_BEFORE` denial (`has no authority over …`) | PASS | PASS | PASS |
| `TD-36` `that`-relative denial naming another agent | FAIL | FAIL | FAIL |
| `TD-38` plain positive ownership | FAIL | FAIL | FAIL |
| `TD-39` `TD-31`'s line inside an authorised historical block | PASS | PASS | PASS |

**Changes, exhaustively:** the trailing-denial branch of `DV-22` (unnamed case removed, universal case gated, `that` added to the boundary); the regression suite (56 → **67** cases); and §18.3's revision stamp, which names the current revision by design.

**Measured before it was written:** on the S4.3.3 text, **0 of the 123 audio mentions depend on a trailing denial at all**, and the full 56-case S4.3.3 suite passes unchanged under the new predicate. No verdict on the document or on any earlier case moved.

**Preserved, exactly:** every normative clause of S4.2 and its 43 obligations (19 P / 15 C / 6 R / 3 A) / 18 suites / 67 proposed cases; `DV-24`; `NEG_BEFORE` in full, so every denial stated before the mention behaves as before; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; S4.3.3 and every earlier artifact and register; the same-commit register mechanism.

## Identity declaration (unchanged, restated so the register is self-contained)

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `arena/3bc206a0-tdd`, `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143` | authoritative S4.2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | `arena/c64fc525-tdd`, `99717e0` / `c800bf0`, blobs `eb774f5d…` / `61ef03b4…` | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | S4.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.1` | `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` | S4.3.1 |
| `TDD-A1-C05-SUCCESSOR-004.3.2` | `b754deb317284df967eaaf84f08e72ecdd2a3ad3`, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` | S4.3.2 |
| `TDD-A1-C05-SUCCESSOR-004.3.3` | `40d29cca0bd2624fb731f4260145454a53a9860a`, blob `d827e017467b3bc320e2c5040a31f3aae0926d94` | S4.3.3, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.4` | this document, blob `41df692d3d80aa967c0f80326a47582957fa8eca` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again to the claim that no Agent 3 S4.2 report exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `40d29cca0bd2624fb731f4260145454a53a9860a` (before this push) · `arena/5dde91a4-tdd` `c8e9f2a` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.2 review present on any branch | **no** — three Agent 3 files exist (`AGENT3_A1_C05_S1_INTEGRATION_READINESS_V1.md`, `AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md`, `AGENT3_C05_3_TELEGRAPH_AUTHORITY_RECOMMENDATION_V1.md`, all on `arena/c64fc525-tdd`), none an S4.2 review, none mentioning `DV-24` or `7d03e1df` |
| `git rev-parse 40d29cc:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_3.md` | `d827e017467b3bc320e2c5040a31f3aae0926d94` — the baseline is intact |
| Predecessor blobs at the tip | S4.3.3 `d827e017`, S4.3.2 `74840d70`, S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df`, S4 `424d2c69`, S3 `07723236` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_4.md` | **27/27 checks passed** |
| Same checker on earlier blobs | S4.3.3 **26/27**, S4.3.2 **26/27**, S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — the single failure on S4.3.3/S4.3.2/S4.3.1/S4.3 is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **67/67 cases behaved as required** |
| Before/after on TD's fourth class | S4.3.3 predicate **accepted five** of the new forms (`TD-31`, `TD-32`, `TD-33`, `TD-40`, `TD-41`); S4.3.4 catches all five; `TD-36`, `TD-38` were already caught in both columns and are reported as guard cases, not evidence (§13.3.5) |
| Required-pass set re-tested | `TD-3`, `TD-3b`, `TD-12`…`TD-18`, `TD-28`…`TD-30`, `TD-34`, `TD-35`, `TD-37`, `TD-39` — **all still PASS**; all 56 S4.3.3 cases unchanged |
| Clean-archive reproduction | `git archive <published commit>` extracted to a fresh directory: validator **27/27**, suite **67/67**, document blob equal to the field above |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is so a reviewer can pin it. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it. S4.3.4 stops here for TD reassessment.**
