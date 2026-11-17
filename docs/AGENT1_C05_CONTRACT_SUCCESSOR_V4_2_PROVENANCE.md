# Provenance register — `A1-C05-S4.2`

**Purpose.** A document cannot contain its own blob hash without a post-publication edit, and S4.1's attempt to do so left literal placeholder fields in the blob both reviewers pinned (Agent 3 finding 7; TD item 6). **This register carries the hash instead**, in the commit immediately after the text, so the reviewed blob is never a document with an unfilled field.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` |
| Version | 4.2 (`A1-C05-S4.2`) |
| **Publishing commit** | **`a788f953256d208f3eb1310f3897924d007179b1`** |
| **Blob at that commit** | **`7d03e1df837493305831962f43882a1cd3496143`** |
| Branch | `arena/3bc206a0-tdd` |
| Predecessor (pinned by both reviews) | `A1-C05-S4.1` at `95918268ed5b20b878fef3ee0a7855ad18e6eeb6`, blob `d54e194affeaee98b1030e2b83b4c34e234fa382` — **unmodified** |
| Validation instrument | `docs/validation/dv_c05.py` (in the same commit) |

The full SHA above is spelled out rather than abbreviated, because an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse a788f953256d208f3eb1310f3897924d007179b1:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md
# 7d03e1df837493305831962f43882a1cd3496143
git diff --stat 3784949 a788f953           # the S4.2 change set
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md   # 27/27
```

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied to every claim of this kind in S4.2, including its own provenance claims.

| Check | Result (run at `2026-11-17T18:36:37Z`) |
|---|---|
| `git ls-remote origin refs/heads/arena/3bc206a0-tdd` | `3784949595d2d62944f712e7345be69118aa14d9` — the S4.1 tip, before this push |
| `git rev-parse a788f953256d208f3eb1310f3897924d007179b1:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | `7d03e1df837493305831962f43882a1cd3496143` |
| `python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | **27/27 checks passed** |
| Same checker on the reviewed blobs | S4.1 `22/27`, S4.0 `21/27`, S3 `10/27` — the failures are the reviewed findings (§13.3) |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## Two disclosed post-publication corrections, and why they are disclosed

S4.2 was first published at `16479425bf98e8b4bdb6e6cd335f80a043e462cd` (blob `86f56af0b4e88441eb897fb9e369f56be6cf4563`). A read-back before handoff found **three sentences** to correct: a typo (`standed` → `stands`), Agent 2's review length (595 → **594** lines, the count `wc -l` gives), and §0.6's claim that every new instrument is shown failing "on the reviewed blob" — false for DV-24, which fails on S4.0. **The corrected text above is the artifact to review**; the first commit is left in history rather than rewritten, and no clause, count, test specification or validation result changed between them.

This is the S4.1 placeholder pattern's honest cousin: **an edit after publication, disclosed here with both hashes**, rather than an unfilled field in the blob a reviewer pins. The difference that matters is that this register names the blob to review and the commit that produced it, and `git log --follow` shows the whole path.

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is, so that a reviewer can pin it; the review itself is Agent 2's and Agent 3's to give.
