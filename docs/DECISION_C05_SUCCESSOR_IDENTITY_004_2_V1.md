# Decision record — which artifact `TDD-A1-C05-SUCCESSOR-004.2` denotes

**Decision ID:** `TDD-A1-C05-DECISION-004-2-IDENTITY-001` v1.0
**Date:** 2026-11-16 UTC
**Author:** Agent 1 — Gameplay, Character and Combat Engineering
**Branch of record:** `arena/3bc206a0-tdd`
**Answers:** Agent 2's condition `N-2` in `TDD-A2-REASSESS-A1C05-S4-2-001` (commit `c8e9f2a`), and TD directive items 2 and 4 for S4.3.
**Status:** decision recorded; **nothing signed, frozen, merged or accepted**; C-05 and U-07 remain open.

---

## 1. The problem, stated exactly

Two files at the same path declare the same response identifier on line 3. Agent 2 found the collision, verified it by comparing `Response ID` across branches, and explicitly refused to say which one is authoritative:

| | Artifact A | Artifact B |
|---|---|---|
| Path | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` |
| Branch | `arena/3bc206a0-tdd` | `arena/c64fc525-tdd` |
| Text commit | `a788f953256d208f3eb1310f3897924d007179b1` | `99717e0` |
| Pinned commit / blob | `a788f95` / **`7d03e1df837493305831962f43882a1cd3496143`** | `c800bf0` / **`61ef03b4`** (text blob `eb774f5d6b281fd632333c39af95d7d66d047ed3`) |
| Lines | 1,265 | 1,237 |
| Declared `Response ID` | `TDD-A1-C05-SUCCESSOR-004.2` | `TDD-A1-C05-SUCCESSOR-004.2` |
| Provenance register | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2_PROVENANCE.md` | none — its §18.1 states the body would be recorded after commit |
| Independently reviewed | **yes**, by Agent 2, whole file, blob-pinned | no |
| `TN-C-14` measure | **one frame on the shared axis** | `1/60` second of monotonic elapsed time |
| Diff between them | **360 changed lines** | |

---

## 2. Decision

1. **`TDD-A1-C05-SUCCESSOR-004.2` denotes Artifact A only** — blob `7d03e1df837493305831962f43882a1cd3496143` at commit `a788f953256d208f3eb1310f3897924d007179b1`.
2. **Artifact B is re-identified as `TDD-A1-C05-SUCCESSOR-004.2-D`** (`-D` for *detached*) and is **superseded**: not a C-05 baseline, not citable as S4.2, not merged, not adopted in whole or in part.
3. **`TN-C-14` is measured in one frame on the shared axis.** The monotonic-elapsed measure is recorded as a **rejected alternative**, not as a variant, a configuration option or a second reading.
4. **This record closes `N-2` by Agent 2's option 3** (*declare in the provenance register which blob the ID denotes and that the other is superseded*), combined with a re-identification label under option 2. Option 1 (physical withdrawal) is **not available to this branch** — see §5.

---

## 3. Grounds for the decision, in order of weight

1. **The TD's own directive pins Artifact A** as the reviewed S4.2 object (`a788f953…` / `7d03e1df…`). The consolidation record already treats it as the thing S4.2 names.
2. **Artifact A is the only S4.2 text that has been independently reviewed.** Agent 2 read all 1,265 lines of the pinned blob and separated contract, documentation, instrument and provenance correctness. Artifact B has been reviewed by nobody.
3. **Artifact A is in the published series.** S1 → S2 → S3 → S4 → S4.1 → S4.2 all live on `arena/3bc206a0-tdd` and each one supersedes the last by statement. Artifact B cites pre-publication hashes from that same series (`4692e97` for S4, `a6b4e22` for S3) and was produced in another agent's worktree; it is a derivative of the series, not the series' next member.
4. **Artifact A carries a complete provenance register** naming its own blob, with the verification commands and their output. Artifact B has none, and states in its own text that the record would follow the commit — the S4.1 placeholder pattern in a different position.
5. **Artifact A's `TN-C-14` measure is the one a reviewer already tried to break** — 400,000 legal schedules, maximised ratio 0.999772 < 1 — and the one `D-1a` was closed against. Adopting the other measure would reopen a closed finding with no defect to justify it.

**What these grounds are not.** They are not a judgement of Artifact B's drafting quality. I do not assess its quality, do not treat it as a draft of Artifact A, and make no claim about its author's intent. The drafting effort is preserved in history under its own identity, which is the point of `…-004.2-D`.

---

## 4. Why the `TN-C-14` measure cannot be reconciled, and which one survives

The two artifacts do not differ in wording; they differ in what the staleness requirement *measures*, and a contract has one such measure. One frame on the shared axis survives, for four reasons:

1. **C-05 has exactly one time base.** `TN-C-10` and `INV-2` age revisions on the shared axis, and `C05-6.1` forbids reconciling quantities across clocks. A bound in monotonic elapsed time puts a second time base inside the clause that uses the first.
2. **A fixed real-time constant cannot entail the axis bound.** Nothing in C-05 fixes the ratio between monotonic time and axis advance. When the axis advances faster than real time — a long frame, a catch-up step, dilation above one — a consumer can satisfy a `1/60` second real-time cap while the rated value ages **more than one frame on the axis**, which is the quantity the requirement is about. The real-time cap is therefore neither necessary nor sufficient.
3. **No frame rate is normative anywhere in C-05**, and `1/60` second silently makes one normative — including in `T-C05-64`, whose assertion would become unmeasurable whenever the axis is paused.
4. **The axis measure is the one already closed.** Agent 2 brute-forced it and closed `D-1a` against it.

**No reconciliation is attempted.** The measures are not averaged, not made configurable, and not both stated as valid. `TN-C-14` in `A1-C05-S4.3` is unchanged from `A1-C05-S4.2` (blob `7d03e1df…`).

---

## 5. What this record does not do, and the residual it leaves open

1. **It does not delete Artifact B.** Line 3 of `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md` on `arena/c64fc525-tdd` still reads `TDD-A1-C05-SUCCESSOR-004.2`. That file is on a branch this revision may read and may not write. **Closing that literally requires a commit on `arena/c64fc525-tdd`; if TD wants it, TD must direct it**, and this record should be updated to cite that commit.
2. **It does not merge the two documents.** 360 lines differ; a merge would produce a third artifact with no reviewer and no pinned blob.
3. **It does not review Artifact B**, and nothing in this record should be read as a finding about it.
4. **It is not a signature, freeze, merge, MEAD selection, implementation authorisation or M0 claim.** No acceptance test is executed by anything recorded here: **0 of 67**.

---

## 6. Where this decision is recorded

| Location | What it says |
|---|---|
| This file | the decision, its grounds, the measure resolution and the residual |
| `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md` §2.9 | the same decision in the contract's own record, with the exact table of branch/commit/blob |
| `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_PROVENANCE.md` | the identity declaration, so the register that pins the artifact also pins what the identifier means |
| `A1-C05-S4.3` commit message | states that the duplicate identity is declared and re-identified, and names both branches |
| `DV-27` in `docs/validation/dv_c05.py` | fails the document if the decision record or the withdrawn identity `…-004.2-D` is missing from §17 |

**The rule this record is trying to establish:** an identifier in this series names exactly one blob, and if two blobs ever claim one, the resolution is written down with both branches, both commits and both blobs — never resolved by assumption, and never by merging.
