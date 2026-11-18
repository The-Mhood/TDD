# C-05 Tranche 1 — Implementation/Test Mapping and Owner Register

**Date:** 2026-11-18 UTC
**Target contract:** S4.3.11 at `6ddc8ed740b37d271cf2417a483c3408b1a41623`, blob `d9c3016cbd50d119721a1d09941bf69d31bc2527`
**Tranche:** `T-C05-01…10`, `T-C05-21…27` (17 proposed cases)
**State:** mapping and owner assignments prepared; **C-05 code and acceptance execution NOT STARTED** pending contract decisions/freeze and UE toolchain.

## 1. Design-specified interfaces to freeze before code

These are copied from the pinned proposed contract, not newly designed or implemented here. Their names and ownership remain subject to TD-12 and formal freeze.

- `FTDDTelegraphTiming`: `AxisNow`, `RemainingLocalSeconds`, `WindupEndAxis`, `ActiveEndAxis`, `RecoveryEndAxis`, `ProducerRate`, `StateRevision`.
- `ETDDTelegraphPhase`: `Windup`, `Active`, `Recovery`.
- `ETDDTelegraphCloseReason`: `Natural`, `Cancelled`, `Interrupted`, `ProducerInvalidated`, `SourceDied`.
- `FTDDTelegraphSnapshot`: `AttackInstanceId`, `SourceEntityId`, `Phase`, fixed-per-instance `WindowKey`/`AttackTag`, and `Timing`.
- `FTDDTelegraphMessage`: `Opened`, `PhaseChanged`, `Retimed`, `Closed`, complete snapshot, and close reason for `Closed`.
- `ITDDTelegraphSource`: `TryGetOpenTelegraph(FGuid, FTDDTelegraphSnapshot&) const` and `GetOpenTelegraphIds(TArray<FGuid>&) const`.

**Not included in Tranche 1:** a shared clock provider, `RemainingLocalSeconds` aging implementation, parry arbitration, C-05/global event transport, `FTDDTelegraphResynchronisation` implementation, consumer asset resolution, new MEAD/module placement, or any change to acceptance criteria. T-C05-11 is deferred until TD-06 is resolved. No second source-of-truth types are to be introduced in the foundation module.

## 2. Fixture and SUT plan

After the frozen interface and contract-layer owner are recorded, implement these as real Unreal Automation Tests against the approved module, not as text checks or a Python imitation:

- **Deterministic input fixture:** explicit `FGuid` instance/source identities; fixed phase and timing VF; fixed revision sequence; no wall-clock reads. Each test supplies deterministic messages/pulls.
- **Producer fake/test seam:** one producer owned by the selected tranche implementer, returning a value snapshot at call time and publishing complete messages; test hooks only for deliberately controlled duplicate/lower revisions and terminal lifecycle events.
- **Consumer-under-test:** minimal revision holder/baseline/phase-entry consumer; records adopted snapshots, entry count, close state and publication order. It does not implement AI/audio/VFX/montage or hit outcomes.
- **Lifecycle fixture:** explicit close/cancel/producer-invalidation/stream-out/world-teardown paths, with the producer/source invalidated before destruction. It must not use a global registry or aggregate another producer's IDs.
- **Assertions:** exact ordered event kind/revision sequence; query return value; adopted revision; entry count; ID non-reuse; close terminality; source invalidation timing. No “test passed” sentinel or success-only mock.

## 3. Case-by-case mapping

| Case | Contract obligation | Fixture / stimulus | Required assertion | Primary owner after freeze |
|---|---|---|---|---|
| `T-C05-01` | TN-P-12 | Replay identical fixed producer inputs twice | Identical values and message sequence; no frame/random dependence | Producer owner |
| `T-C05-02` | TN-C-01 | Held revision `n`; pull with equal revision | Discard equal revision; held versioned state unchanged | Agent 1/Agent 2 consumer owner |
| `T-C05-03` | TN-C-01 | Held `n`; message/pull with lower revision | Discard; held revision never moves backwards | Consumer owner |
| `T-C05-04` | TN-R-02 | Query a terminally closed instance | `TryGetOpenTelegraph` returns false; no partial/stale output accepted | Agent 1 shared support + producer owner |
| `T-C05-05` | TN-R-02 | Query an ID never opened by this producer | Returns false; no cross-producer/global fallback | Agent 1 shared support + producer owner |
| `T-C05-06` | TN-P-11 | Change producer live state, then query | Query reflects live state at call time and correct current revision | Producer owner |
| `T-C05-07` | TN-P-01 | Open instance, then emit a phase transition | `Opened` is first and precedes every other instance message | Producer owner |
| `T-C05-08` | TN-C-02 | Consumer attaches to active baseline | Establish baseline without fabricating a phase-entry event | Consumer owner |
| `T-C05-09` | TN-C-02 | Establish baseline by pull and by `Opened` | Both paths establish the same baseline; neither creates a false entry | Consumer owner |
| `T-C05-10` | TN-C-03 | Deliver one observed phase transition | Exactly one entry for that phase; no duplicate entry | Consumer owner |
| `T-C05-21` | TN-P-03 | Natural terminal path | Exactly one `Closed`; terminal after close | Producer owner |
| `T-C05-22` | TN-P-04 | Exercise each authorized cancellation path | Every cancellation closes the instance exactly once | Producer owner |
| `T-C05-23` | TN-P-05 | Invalidate producer during teardown | Source invalidation/deregistration precedes producer destruction | Producer owner + Agent 1 shared support |
| `T-C05-24` | TN-P-06 | Stream out one producer's source | Only that producer's instances are invalidated | Producer owner |
| `T-C05-25` | TN-C-06 | Consumer receives/remembers removal | Treat removal as terminal closure, not as an error | Consumer owner |
| `T-C05-26` | TN-P-02 | Close an ID; then open a later instance | No `AttackInstanceId` reuse | Producer owner |
| `T-C05-27` | TN-P-09 | Attempt emission after close and query never-opened ID | No post-close message; no message for never-opened instance | Producer owner |

**Coverage:** 17 rows, 17 unique acceptance IDs. All remain `PROPOSED / NOT RUN`; this mapping does not execute or reclassify them.

## 4. Parallel owner assignment register

Assignments below are the Project Owner's requested coordination routing. They are **not** represented as received acknowledgements or completed decisions; direct agent dispatch is not available in this workspace. Owners should publish version-pinned responses/decisions on the authorized branch or project record. The remaining C-05 status is `DESIGN_ONLY` until those records and formal freeze/kickoff approval exist.

| Item | Assigned owner(s) | Required version-pinned output | Status / execution gate |
|---|---|---|---|
| **TD-06 — clock/shared axis** | TD decision owner; Agent 1 supplies producer/timing requirements; Agent 2 reviews consumer timing; Agent 3 checks traceability | Named clock owner/provider, units, pause/global/local dilation semantics, observation point and exact affected obligations/tests | **PENDING**; blocks `TN-P` timing/aging and T-C05-11, C/D/M/Q timing portions |
| **TD-09 — parry authority/MEAD erratum** | TD decision owner + Agent 1 arbitration owner; Agent 2 review; Agent 3 independent boundary check | Exact canonical file/commit/section, permitted hit-resolution inputs, chosen arbiter owner, and matching T-C05-32…34/T-C05-63 instrumentation | **PENDING**; no arbitration implementation until recorded |
| **TD-12 — canonical MEAD / contract-layer ownership** | TD decision owner; Agent 3 prepares candidate/source comparison; Agents 1/2 review the exact candidate | One canonical MEAD path+commit, one named contract-layer owner, module/API home, and disposition of materially conflicting candidates | **PENDING**; blocks freezing/implementing C-05 value types and read interface |
| **B-11 — C-04-4 / `Status.Dead`** | C-04 contract owner and status/tag registry owner; TD records effect on C-05 | Exact C-04-4 and registry decision, or explicit authorized isolation of TN-C-07/T-C05-35…39 | **PENDING**; affects only the precedence case family |
| **B-9 — Agent 2 review** | Agent 2 | Review exact S4.3.11 document blob `d9c3016cbd50d119721a1d09941bf69d31bc2527`, including recorded `D-1`/`D-3` differences, and state accept/required revision | **PENDING**; milestone and L-2 reports are not same-version design sign-off |
| **B-10/B-15 — Agent 3 review/arbitration boundary** | Agent 3; TD owns final adjudication | Pin an exact-S4.3.11 review; address the `TN-C-11` selection versus hit-outcome boundary and T-C05-63's input/use-path evidence | **PENDING**; existing workspace S2/S3 reviews are untracked and do not approve this exact baseline |
| **B-12 — resynchronization routing** | TD decision; Agent 1/Agent 2 consumer owners implement; Agent 3 verifies | **DECIDED for this S4.3.11 design baseline:** keep `FTDDTelegraphOnResynchronised` consumer-local as specified by C05-2.2/EN-3/TN-C-09. No cross-agent transport, registry or queue is added. Any future request for routing requires a separate versioned TD decision. | **RESOLVED — scope confirmation only**; does not add behavior or waive TD-12 type ownership |
| **B-14 — numeric tolerance** | TD fixture decision; Agent 3 records helper; Agent 2 independently reviews before timing-case execution | **DECIDED for tests only:** for `double` axis values, absolute comparison tolerance `1e-9` axis-seconds; for `float` `RemainingLocalSeconds`, pass when `abs(actual-expected) <= max(1e-4 seconds, 1e-5 * max(abs(actual), abs(expected)))`. This is test-fixture precision only; it does not change contract values or timing semantics. | **RESOLVED — fixture convention; Agent 2 review pending**; not needed for Tranche 1 and required before T-C05-54/55/64 execution |

## 5. First-tranche gate and status

**Ready to begin after gates:** project/module foundation exists; test map and owner routing are prepared. **Not ready for C-05 code/test execution:** the canonical MEAD/type owner, formal design freeze, required clock/arbitration decisions and UE toolchain are not yet in place. The first available verified target should be Mac Development on the owner's authorized Mac; Win64 requires separate verification on an authorized Windows host.

Once TD-12 and the exact C-05 freeze are approved, and the UE 5.8 toolchain is available on the authorized Mac host:

1. Implement one agreed producer/read interface and consumer baseline using only the frozen types.
2. Add deterministic automation fixtures for A/B/E cases above; keep T-C05-11 outside the tranche until TD-06.
3. Build `TheDisobedientDaughterEditor Mac Development` on the authorized Mac host, run the 17 named filters/cases, and preserve complete logs, engine identity, commit, exit status and assertions. Verify Win64 separately on an authorized Windows host before claiming Windows compatibility.
4. Agent 2 independently validates test-to-contract mapping and evidence; Agent 3 checks traceability, dependency compliance and governance; Project Owner approves the next tranche/status change.

No acceptance test, C-05 runtime interface, gameplay behavior, or contract status was changed by this mapping.
