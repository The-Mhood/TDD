# Provenance register — `A1-C05-S4.3.2`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document**. The mechanism is unchanged from S4.3: a document cannot contain its own blob hash without a post-publication edit, and a register written in a *later* commit can pin a superseded draft of the text it describes. Both files are published together, so neither can happen here.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_2.md` |
| Version | 4.3.2 (`A1-C05-S4.3.2`) |
| **Blob of this document** | **`74840d70a1620caaa3fe1138ab68eccd71c0665b`** |
| Lines | 1,584 |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, `docs/validation/dv_c05.py`, `docs/validation/test_dv_c05_regressions.py`, `docs/README.md`, `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` |
| **Baseline corrected** | `A1-C05-S4.3.1` at `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90`, 1,506 lines — **unmodified** |
| Earlier baselines, **unmodified** | S4.3 `2acfc2e` / `74546027` · S4.2 `a788f95` / `7d03e1df` · S4.1 `95918268` / `d54e194a` |
| Identity decision (unchanged) | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_2.md
# 74840d70a1620caaa3fe1138ab68eccd71c0665b   (must equal the field above)
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_2.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                               # 44/44
```

## What this revision is

**A targeted revision of S4.3.1, found by source inspection rather than by testing.** TD read `NEG_BEFORE` and saw that it accepted any `no … audio` within 28 characters, so *"has no problem owning audio cues"*, *"has no objection to owning audio cues"* and *"has no restriction on owning audio cues"* were read as **denials of ownership** when they assert it.

`DV-22` now recognises a **bounded set of grammatical denials** — denial verb + `no` + audio object; `no <audio> <denial noun>`; `no <denial noun> for/over/of <audio>`; `is not responsible/owner for/of <audio>`; `does not own <audio>`; `owns none of the audio`; plus two reversed forms. Anything outside that set is a positive statement, and a positive statement governed by the first agent is an offender. **This is a whitelist of denials, not an exemption list**: failing to match it does not exempt a line, it condemns one.

**Three changes, no others:** the `DV-22` predicate; the regression suite (30 → **44** cases, including TD's five forms, the three required-pass denials, four further genuine denials, and the historical control); and §18.3's revision stamp, which names the current revision by design.

**Two genuine denials that S4.3.1 wrongly rejected now pass** — `does not own any audio cues` and `is not responsible for audio cue selection` — which is why §13.3.3 reports movement in both directions rather than only the four rows that changed from accepted to caught.

**Preserved, exactly:** every normative clause of S4.2 and its 43 obligations / 18 suites / 67 proposed cases; `DV-24`; the `N-2` identity declaration (`…-004.2` denotes `7d03e1df…`; `…-004.2-D` superseded, not merged); `TN-C-14` at one frame on the shared axis; `D-4`, `D-1a`, `D-1b`, `C4c-N1`; the same-commit register mechanism.

## Identity declaration (unchanged, restated so the register is self-contained)

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `arena/3bc206a0-tdd`, `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143` | authoritative S4.2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | `arena/c64fc525-tdd`, `99717e0` / `c800bf0`, blobs `eb774f5d…` / `61ef03b4…` | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `2acfc2ec91c38fea8b1e556988df652b49dff5bc`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | S4.3 |
| `TDD-A1-C05-SUCCESSOR-004.3.1` | `db95404c6d6dfac3f49b34059cb96ba85ffe282c`, blob `c8708ef0e990117bbc6ff3815faecb857301db90` | S4.3.1, the baseline this revision corrects |
| `TDD-A1-C05-SUCCESSOR-004.3.2` | this document, blob `74840d70a1620caaa3fe1138ab68eccd71c0665b` | **this revision** |

**Residual, unchanged:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; that remains TD's to direct.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied again to the claim that no Agent 3 S4.2 report exists.

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `db95404c6d6dfac3f49b34059cb96ba85ffe282c` (before this push) · `arena/5dde91a4-tdd` `c8e9f2a` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.2 review present on any branch | **no** — three Agent 3 files exist, none an S4.2 review, none mentioning `DV-24` or `7d03e1df` |
| `git rev-parse db95404:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_1.md` | `c8708ef0e990117bbc6ff3815faecb857301db90` — the baseline is intact |
| Predecessor blobs at the tip | S4.3.1 `c8708ef0`, S4.3 `74546027`, S4.2 `7d03e1df`, S4.1 `cc056a48`, S4 `d72831e7`, S3 `80060de`, S2 `30a98b88`, S1 `dcec9e1a` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3_2.md` | **27/27 checks passed** |
| Same checker on earlier blobs | S4.3.1 **26/27**, S4.3 **26/27**, S4.2 **24/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** — the one failure on S4.3.1 and S4.3 is `DV-27`, the register that pins *this* document |
| `python3 docs/validation/test_dv_c05_regressions.py` | **44/44 cases behaved as required** |
| Before/after on TD's second class | S4.3.1 predicate **accepted four** of the new forms (`TD-6`, `TD-7`, `TD-8`, `TD-10`); S4.3.2 catches all four; two of TD's five were already caught in both columns and are reported as guard cases, not evidence (§13.3.3) |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is so a reviewer can pin it. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it.**
