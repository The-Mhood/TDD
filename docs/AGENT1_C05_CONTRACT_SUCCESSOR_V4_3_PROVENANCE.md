# Provenance register — `A1-C05-S4.3`

**Purpose.** This register names the exact blob of the document it accompanies, and it is **committed in the same commit as that document**. That is a change of mechanism, not a change of wording, and it answers two defects at once.

- **The placeholder defect (Agent 3 finding 7, TD item 6).** A document cannot contain its own blob hash without a post-publication edit; S4.1 tried and left literal placeholder fields in the blob both reviewers pinned.
- **The stale-register defect (Agent 2's check 3b, TD item 4).** S4.2 wrote its register *in the following commit*, and at its own publishing commit `a788f953256d208f3eb1310f3897924d007179b1` the register (blob `eda9bd2671650b0c41a8aa1cff97da0dd0fad593`) still pinned the **first** S4.2 draft `86f56af0b4e88441eb897fb9e369f56be6cf4563`, while the document in that same commit was already `7d03e1df837493305831962f43882a1cd3496143`. A register one commit behind the text it describes is a smaller instance of the same failure.

**With S4.3 the document and this register are written into one commit.** There is no earlier commit of this document for the register to be stale about, and the register names the document's blob exactly. The commit itself is identified by the paths it introduced, because no file can contain the hash of the commit that contains it:

```bash
git log --format=%H -1 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md
```

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md` |
| Version | 4.3 (`A1-C05-S4.3`) |
| **Blob of this document** | **`7454602783575eaf4deba6a3d3f7043cff174f96`** |
| Lines | 1,432 |
| Branch | `arena/3bc206a0-tdd` |
| Published in the same commit as | this register, `docs/validation/dv_c05.py`, `docs/validation/test_dv_c05_regressions.py`, `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` |
| **Reviewed artifact revised** | `A1-C05-S4.2` at `a788f953256d208f3eb1310f3897924d007179b1`, blob `7d03e1df837493305831962f43882a1cd3496143`, 1,265 lines — **unmodified** |
| Predecessor (pinned by both S4.1 reviews) | `A1-C05-S4.1` at `95918268ed5b20b878fef3ee0a7855ad18e6eeb6`, blob `d54e194affeaee98b1030e2b83b4c34e234fa382` — **unmodified** |
| **Identity decision** | `docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md` — restated in the document's §2.9 |

The full hash is spelled out rather than abbreviated: an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse HEAD:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md
# 7454602783575eaf4deba6a3d3f7043cff174f96   (must equal the field above)
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md    # 27/27
python3 docs/validation/test_dv_c05_regressions.py                             # 18/18
```

## The identity declaration (`N-2`)

Two files declared `TDD-A1-C05-SUCCESSOR-004.2`. This register is the place Agent 2 named for the declaration, so the declaration is here, in the same words as the document and the decision record:

| Identifier | Denotes | Status |
|---|---|---|
| `TDD-A1-C05-SUCCESSOR-004.2` | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` on `arena/3bc206a0-tdd`, commit `a788f953256d208f3eb1310f3897924d007179b1`, blob **`7d03e1df837493305831962f43882a1cd3496143`**, 1,265 lines | **authoritative S4.2**; reviewed in full by Agent 2 |
| `TDD-A1-C05-SUCCESSOR-004.2-D` | the same path on `arena/c64fc525-tdd`, commits `99717e0` (text) and `c800bf0` (pin), blobs `eb774f5d6b281fd632333c39af95d7d66d047ed3` / `61ef03b4`, 1,237 lines | **superseded** — not a baseline, not citable, **not merged** |
| `TDD-A1-C05-SUCCESSOR-004.3` | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md`, blob `7454602783575eaf4deba6a3d3f7043cff174f96` | this revision |

**The `TN-C-14` measure is one frame on the shared axis.** The `1/60` second monotonic-elapsed measure in `…-004.2-D` is recorded as a rejected alternative, with the reasons in §2.9 and in the decision record. It is not a variant, an option, or a second reading.

**Residual, stated rather than hidden:** line 3 of the file on `arena/c64fc525-tdd` still reads `…-004.2`. Removing it requires a commit on a branch this revision may read and may not write; if TD wants that, TD must direct it.

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied to every claim of that kind in this revision, including the claim that no Agent 3 S4.2 report exists (§0.8).

| Check | Result (run immediately before the publishing commit) |
|---|---|
| `git ls-remote --heads origin` | `arena/3bc206a0-tdd` `d1d9ac9861a73cfe0e9190713801d19307d5bac1` (before this push) · `arena/5dde91a4-tdd` `c8e9f2a` · `arena/c64fc525-tdd` `c800bf0` · `main` `5e3d1da` |
| Agent 3 S4.2 review present on any branch | **no** — commands and results in §0.8 of the document |
| `git rev-parse a788f95:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | `7d03e1df837493305831962f43882a1cd3496143` — the reviewed artifact is intact |
| `git show a788f95:docs/…V4_2_PROVENANCE.md \| git hash-object --stdin` | `eda9bd2671650b0c41a8aa1cff97da0dd0fad593`, naming `86f56af…`, not `7d03e1df…` — the stale-register defect, reproduced |
| Predecessor blobs at the tip | S4.1 `cc056a48…`, S4 `d72831e7…`, S3 `80060de…`, S2 `30a98b88…`, S1 `dcec9e1a…` — **all unmodified** |
| `python3 docs/validation/dv_c05.py docs/…V4_3.md` | **27/27 checks passed** |
| Same checker on earlier blobs | S4.2 **25/27**, S4.1 **21/27**, S4.0 **21/27**, S3 **10/27** |
| `python3 docs/validation/test_dv_c05_regressions.py` | **18/18 cases behaved as required** |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is, so that a reviewer can pin it; the review is Agent 2's and Agent 3's to give. **No acceptance test is executed by anything recorded here, and no behavioural claim is made from any of it.**
