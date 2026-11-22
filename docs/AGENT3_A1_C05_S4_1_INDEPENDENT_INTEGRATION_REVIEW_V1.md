# Agent 3 — A1-C05-S4.1 independent integration review

**Review outcome:** targeted integration review of the exact published text; not a signature, freeze, implementation authorization, merge, MEAD selection, or M0 claim.

## Target verification and method

Reviewed only `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md` at publishing commit `95918268ed5b20b878fef3ee0a7855ad18e6eeb6`. `git rev-parse 95918268ed5b20b878fef3ee0a7855ad18e6eeb6:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md` returns `d54e194affeaee98b1030e2b83b4c34e234fa382`, the requested blob. S4.0 was used only as the predecessor for a byte-diff check, not as a substitute review target. The earlier S3 assessment in this worktree was untracked and unpublished; I do not cite or rely on it. Findings below come from direct S4.1 clauses and independently specified checks.

## Findings

### 1. `TN-C-11` / arbitration boundary — **AGREE WITH CONDITIONS**

**Clauses:** §4.8 `C05-2.8`; §4.10 `C05-6.1`/`C05-6.4`; §5.2 `C05-7.2` rows 5 and 8; §6.1; §8 `TN-C-11`; §9.2 and §9.3 `TN-A-01`–`TN-A-03`.

**Assessment and integration consequence:** the new three-domain rule is sound in isolation. `AttackTag` is authored by the producer, may guide consumer selection, and cannot participate in the hit outcome; `TN-A-02` and `TN-A-03` explicitly forbid using even a cached snapshot/tag on the hit-resolution path. However, §5.2 row 5 still describes Agent 1's integration as “parry/block/dodge evaluation from the pull.” Read literally, that permits the pull to enter the very parry/block evaluation whose outcome §4.8 and §9.2 reserve from all C-05 inputs. A consumer could use pulled `AttackTag` or phase to decide whether a hit was parried, contrary to `TN-A-01`–`TN-A-03`.

- **Expected:** C-05 fields may guide a response attempt/selection only; hit outcome uses the live hit-resolution inputs specified in `TN-A-01`/`TN-A-03` and never the pull or `AttackTag`.
- **Actual text:** the boundary clauses say that, but the ownership row's unqualified “evaluation from the pull” leaves a conflicting implementation reading.
- **Blocks contract closure?** Yes, until the consumer-vs-outcome wording is consistent across the ownership and arbitration clauses.
- **Smallest correction:** in §5.2 row 5, scope pull use to response selection/telegraph consumption and explicitly exclude hit outcome; point actual parry/block arbitration to row 8 and `C05-6.1`/`TN-A-01`–`TN-A-03`.
- **Reproducible check:** trace the two legal paths in `C05-6.4` and search all ownership descriptions for “parry/block/dodge evaluation from the pull.” The S4.1 text contains that row-5 phrase while row 8 says C-05 supplies no arbitration input.

### 2. `AttackTag` lifetime, creation/selection/outcome, and downstream boundary — **AGREE**

**Clauses:** §3.8; §4.2 `C05-2.2`; §4.6 `TN-P-19`; §4.8; §4.10 `C05-6.4`; §6.1; §8 `TN-C-11`/`TN-C-15`; §9.2 `TN-A-03`; §14.2 B-13.

**Assessment and integration consequence:** the three domains are consistently expressed: the producer creates/authors the tag at `Opened`; identity and tag are fixed for the instance; consumers use the landed snapshot for response/cue/montage selection; the hit outcome is not decided by C-05. `TN-P-19` specifies the identity-change path (close old instance, open a new ID at revision 1), avoiding an in-place identity mutation. Audio and AI selection are compatible with consumer-local state and do not imply event history.

- **Expected vs actual:** a mid-instance tag change is rejected and represented by close/reopen; selection can use the snapshot, but arbitration cannot. The normative text says exactly that.
- **Blocks contract closure?** No, for C-05's own boundary. B-13 tag registration/ownership and the C-03/C-04/TD-09 outcome rules remain external dependencies for end-to-end gameplay validation; S4.1 does not define or resolve them.
- **Correction:** none to C-05's creation/selection/outcome rule. Keep B-13 and the named outcome dependencies visible; do not treat a C-05 tag as the authoritative unblockable result.
- **Reproducible test:** T-C05-62/T-C05-66 cover fixed identity and close/reopen; T-C05-57/58/67 cover selection use. T-C05-63 should be strengthened as described in finding 6. These cases are proposed, not run.

### 3. `TN-P-18`, PO-5, and per-message `ProducerRate` — **AGREE**

**Clauses:** §4.2 `ProducerRate` field comment; §4.9 `PO-3`/`PO-5`; §7 `TN-P-08`, `TN-P-11`, `TN-P-15`, `TN-P-17`, `TN-P-18`; §10.5 EX-5; §10.11 EX-11; T-C05-51/T-C05-65.

**Assessment and integration consequence:** PO-3 supplies phase-before-retime order, while PO-5/TN-P-18 require application and publication to interleave, so each complete message's `VF` (including its `ProducerRate`) describes only the changes applied through that revision. For a phase transition followed by a dilation change, the phase message is `n+1` at the prior rate; the `Retimed` message is `n+2` at the new rate. A mid-sequence pull is explicitly constrained to the earlier revision's `VF`.

- **Expected vs actual:** the normative clauses and examples agree; no `n+1` message can carry the later rate, nor can a pull observe an unpublished rate revision under the specified sequencing.
- **Blocks contract closure?** No text defect found. It remains unvalidated behaviorally.
- **Correction:** none identified.
- **Reproducible test:** T-C05-51 asserts each message's rate in a phase-plus-two-retime sequence; T-C05-65 specifies pulls after each application and a batching negative control. Both are `PROPOSED / NOT RUN`.

### 4. PO-5 and the one-pull-per-frame residual-staleness bound — **DISAGREE**

**Clauses:** §4.9 PO-5; §8 `TN-C-10`/`TN-C-14`; §10.5 EX-5(d); T-C05-64.

**Concrete failure scenario:** a timing-dependent consumer performs its required pull early in frame *k*. The `Retimed` is lost immediately after that pull. It performs no other pull in frame *k*, then performs its one required pull near the end of frame *k+1*. This satisfies “at least once per frame,” yet its rate estimate remains stale for almost two frame durations. If it acts on that value before the next pull, it can also make a timing-dependent choice from stale rate during that interval.

- **Expected:** TN-C-14 and T-C05-64 claim staleness is bounded by one frame.
- **Actual:** “at least once per frame” does not constrain the maximum elapsed interval between pulls or their position within successive frames, so the claimed one-frame bound does not follow from the requirement as written. The accepted message-only residual is explicit; the timing-dependent bound is not yet guaranteed.
- **Blocks contract closure?** Yes, for D-1's claimed bound and the corresponding T-C05-64 assertion.
- **Smallest correction:** specify a maximum interval between successful refreshes (and define its measure), or prescribe a polling point/order that proves that maximum; if the consumer can act after a newer retime may have occurred, require a fresh pull before that timing-dependent action. Keep message-only residual staleness explicitly accepted if that remains the chosen policy.
- **Reproducible test:** extend T-C05-64 with the just-after-poll lost-retime schedule above and a poll at the latest allowed time. Assert the stated maximum age in the chosen frame/axis measure. Current T-C05-64 does not specify this worst-case poll placement; it is unrun.

### 5. Audio ownership — **DISAGREE**

**Clauses:** §5.2 `C05-7.2` rows 5–6; §5.4 `C05-7.4`; §6.1; §8 introduction; §8 `TN-C-15`; §13.1 DV-22; T-C05-67.

**Concrete failure scenario:** a team follows the §8 introduction and assigns audio work to both Agent 1 (“audio”) and Agent 2 (“audio cue”), while §5.2 says Agent 1 owns no C-05 audio and Agent 2 alone owns cue selection. Work can be duplicated or split inconsistently despite the row table's intended assignment.

- **Expected:** Agent 2 alone owns C-05 audio cue selection; Agent 1 has no C-05 audio responsibility.
- **Actual text:** §5.2 row 5 and row 6 plus TN-C-15 give the single-owner rule, but the §8 introduction still lists “Agent 1 for defence, dodge, camera and audio” and separately “Agent 2 for AI reaction, audio cue…”.
- **Blocks contract closure?** Yes, for the ownership split and D-4's claim that audio has one owner throughout the contract.
- **Smallest correction:** remove “and audio” from Agent 1's §8 introduction, and state Agent 2's audio cue responsibility there consistently with row 6/TN-C-15.
- **Reproducible check:** scan all ownership prose, not just the C05-7.2 table. DV-22 currently checks row 5, row 6, and TN-C-15, so it misses the contradictory §8 introduction. Add that introduction to DV-22's inspected locations; T-C05-67 should retain its single-owner assertion.

### 6. D-1…D-7, T-C05-63/DV-20, and validation coverage — **AGREE WITH CONDITIONS**

**Clauses/instruments:** §2 D-1…D-7; §5.4 DV-11 mapping; §8 TN-C-11/14/15; §9.2 TN-A-02/03; §10.5; §12 T-C05-51/T-C05-63–67; §13 DV-11, DV-17, DV-20, DV-21, DV-22, DV-23.

**D-1…D-7 integration disposition:**

| Defect | Independent result | Integration consequence / closure |
|---|---|---|
| **D-1** lost retime | **AGREE WITH CONDITIONS** | The message-only residual is stated honestly. The claimed one-frame timing-dependent bound still needs the correction in finding 4. |
| **D-2** publication content | **AGREE** | PO-5/TN-P-18 and T-C05-51/65 coherently require per-revision state and per-message rate; no correction beyond the polling issue. |
| **D-3** identity change | **AGREE** | Fixed identity plus close/reopen is explicit and testable; no mid-instance tag revision. |
| **D-4** audio owner | **DISAGREE** | The §8 introduction contradicts the intended sole Agent 2 assignment; see finding 5. |
| **D-5** role token rows | **AGREE** | The new Agent 2 C-05-consumer token distinguishes row 6 from outside-C-05 row 7. |
| **D-6** DV-11 row mapping | **AGREE** | Independent text parsing found 43 obligation cells, five observed tokens, and no token/prefix/allowed-row mismatch. DV-11's documented row-level check addresses the S3 row-6/row-7 failure mode. |
| **D-7** INV-2 condition | **AGREE** | §4.6 states the one-revision precondition in INV-2 itself and TN-C-10 repeats the stale-held-revision limit. |

**T-C05-63 / DV-20 coverage condition:** the normative exclusion in TN-A-02/03 is clear, but DV-20 is a text-presence check, not evidence of the hit-resolution data path. T-C05-63 includes a held-snapshot variant and a corrupted-tag variant, but does not explicitly combine them. A spy on the telegraph surface can miss a cached `AttackTag` read: the hit-resolution code can consume a snapshot already held for selection without making a new surface call. In that scenario, “zero reads on the hit-resolution path” at the surface does not establish zero C-05-value use.

- **Expected:** the hit result is invariant to a held/corrupted tag, and no C-05-derived value reaches the outcome decision.
- **Actual:** the test specification separately names held-snapshot and corrupted-tag variants, and the stated spy watches the surface; it does not explicitly observe cached-value dataflow in the combined case.
- **Blocks contract closure?** It blocks claiming the arbitration boundary has been adequately falsified by the proposed acceptance test; the normative boundary itself is clear.
- **Smallest correction:** extend T-C05-63 to combine “selection snapshot already held” with an adversarial change to that held `AttackTag`, assert unchanged hit outcome, and instrument the hit-resolution input/use path (tainted-value or equivalent call-site/dataflow spy), not only new reads from the source surface. Retain an independent assertion that the selection call site can still use the tag.
- **Reproducible test:** compare a hit with a held selection snapshot whose tag is `blockable` against the same hit with only the held tag changed to `unblockable`; assert identical hit result and no tag-derived value observed by the hit resolver. T-C05-63 is proposed and unrun.

### 7. S4.1-only delta and provenance text — **AGREE WITH CONDITIONS**

**Clauses:** §0.5; §1 row 6; §17; §18.1.

**Normative delta check:** compared S4.1 with the exact S4.0 blob `424d2c69df62ebc1930eacd0ba67077c854ab31e` at `4692e973d04a94d7781677c704e7a0198abd2d70`. The body from §2 through §16 is byte-identical. S4.1 adds provenance/scope material, updates title/version/handoff metadata, and corrects the §1 DV-11 summary from “6 observed” to “5 observed,” matching §13.1. I found no unrelated normative change in S4.1 itself.

There is a remaining documentary handoff defect: §17 and §18.1 contain literal `S41_COMMIT` and `S41_BLOB` placeholders. The review target is still independently pinned here by the user-supplied commit and the verified path-to-blob result above, so this does not compromise this review's identity.

- **Expected:** the publication record and handoff point to the exact published S4.1 artifact.
- **Actual:** their commit/blob fields are placeholders.
- **Blocks contract closure?** No normative contract block; it does block a reader using the document alone from following its “review this exact blob” handoff reproducibly.
- **Smallest correction:** replace the placeholders with commit `95918268ed5b20b878fef3ee0a7855ad18e6eeb6` and blob `d54e194affeaee98b1030e2b83b4c34e234fa382` in §17 and §18.1.
- **Reproducible evidence:** inspect those exact fields in the reviewed blob; the path-to-blob verification command is recorded above.

## Executed checks and limits

- Exact commit/path resolution and blob verification succeeded.
- Compared S4.1 against its pinned S4.0 baseline; a read-only Python check confirmed §2–§16 are byte-identical.
- Independently parsed S4.1's four obligation tables: 43 implementer cells; five distinct tokens used; no prefix/allowed-row mismatch. A separate targeted text scan found the §8 audio contradiction, confirmed that TN-C-14 lacks a maximum elapsed poll interval, and confirmed that T-C05-63 does not explicitly combine the held-snapshot and corrupted-tag cases.
- Agent 1 reports 23 document checks passing. I did not run `/home/user/dv4.py`; DV outputs are not behavioral tests. No T-C05 acceptance case, build, engine, or runtime test was executed here; all 67 cases remain `PROPOSED / NOT RUN` in the reviewed document.
- The C-03/C-04/TD-09 decisions and AttackTag registration remain external dependencies for end-to-end outcome validation. They do not erase the direct text conflicts and test-spec gaps above.

**Overall outcome: TARGETED REVISION**