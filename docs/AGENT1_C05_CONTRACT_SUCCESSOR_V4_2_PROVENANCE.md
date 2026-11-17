# Provenance register — `A1-C05-S4.2`

**Purpose.** A document cannot contain its own blob hash without a post-publication edit, and S4.1's attempt to do so left literal placeholder fields in the blob both reviewers pinned (Agent 3 finding 7; TD item 6). **This register carries the hash instead**, in the commit immediately after the text, so the reviewed blob is never a document with an unfilled field.

## The artifact to review

| Field | Value |
|---|---|
| Document | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` |
| Version | 4.2 (`A1-C05-S4.2`) |
| **Publishing commit** | **`16479425bf98e8b4bdb6e6cd335f80a043e462cd`** |
| **Blob at that commit** | **`86f56af0b4e88441eb897fb9e369f56be6cf4563`** |
| Branch | `arena/3bc206a0-tdd` |
| Predecessor (pinned by both reviews) | `A1-C05-S4.1` at `95918268ed5b20b878fef3ee0a7855ad18e6eeb6`, blob `d54e194affeaee98b1030e2b83b4c34e234fa382` — **unmodified** |
| Validation instrument | `docs/validation/dv_c05.py` (in the same commit) |

The full SHA above is spelled out rather than abbreviated, because an abbreviated hash in a provenance record is one more thing a reader has to resolve before trusting it.

```bash
git rev-parse 16479425bf98e8b4bdb6e6cd335f80a043e462cd:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md
# 86f56af0b4e88441eb897fb9e369f56be6cf4563
git diff --stat 3784949 1647942          # the S4.2 change set
python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md   # 27/27
```

## Verification performed immediately before publication

Agent 2's §1.3 rule — *re-verify any negative existence claim as the last action before publication* — was applied to every claim of this kind in S4.2, including its own provenance claims.

| Check | Result (run at `2026-11-17T18:36:37Z`) |
|---|---|
| `git ls-remote origin refs/heads/arena/3bc206a0-tdd` | `3784949595d2d62944f712e7345be69118aa14d9` — the S4.1 tip, before this push |
| `git rev-parse 16479425bf98e8b4bdb6e6cd335f80a043e462cd:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | `86f56af0b4e88441eb897fb9e369f56be6cf4563` |
| `python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | **27/27 checks passed** |
| Same checker on the reviewed blobs | S4.1 `22/27`, S4.0 `21/27`, S3 `10/27` — the failures are the reviewed findings (§13.3) |
| Acceptance tests executed | **0** — 67 cases `PROPOSED / NOT RUN` |

## What this register is not

It is not a signature, a freeze, an implementation authorisation, a merge, a MEAD selection or an M0 claim. **C-05 and U-07 remain open.** It records where the text is, so that a reviewer can pin it; the review itself is Agent 2's and Agent 3's to give.
