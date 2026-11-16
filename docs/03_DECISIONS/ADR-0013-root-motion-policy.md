# ADR-0013 — Root motion: execution, collision, interruption and restoration

- **Status:** Proposed — **v1.4** (v1.1 accepted provisionally; v1.2 aligned the damage taxonomy; v1.3 added placement validation and hold-while-forced; v1.4 separates the bounded relocation budget from the unbudgeted terminal hold resolution)
- **Date:** 2026-11-16
- **Deciders:** Technical Director; Agent 1 (owner); Agent 2 (consumes enemy attack timing and traversal transitions)
- **Owning agent:** 1
- **Supersedes:** v1.3 (`archive/ADR-0013-root-motion-policy_V1.3.md`), v1.2, v1.1, v1.0 — all preserved unchanged
- **Companion rules:** M1 spec v1.4 §3.2.2a (two-phase validation), §3.2.2a.1 (attempt-budget scope), §3.2.2b (hold under forced transition), §3.2.2c (control state vs movement mode), §3.2.2d (forced transitions during resolution)
- **Related:** ADR-0005 (animation provider), ADR-0012 (verification boundary), M1 spec v1.1 §3.5/§3.7/AC-26

## 1. Context

Mixing engine-driven capsule movement with animation root motion is the most common source of control-feel defects in third-person action games: characters that slide, that lunge through walls, that get stuck because a movement mode was never restored, or that can be steered mid-dodge in ways the animation cannot express.

v1.0 of this ADR made a specific technical assumption that the review correctly identified as unverified: it proposed putting the Character Movement Component into `MOVE_None` during root-motion montages, on the assumption that CMC would still apply animation root motion. That assumption is unsafe. CMC processes animation root motion as part of its movement update; if a movement mode causes that update to be skipped, the capsule may receive no translation at all and the authored lunge silently disappears. The failure would look like a content problem ("the attack has no travel") rather than an engine misuse, which is the worst kind of bug.

Because this workspace cannot build or run Unreal Engine (ADR-0012), the mechanism **cannot be verified here**. This ADR therefore specifies the intended mechanism, the verification that must confirm it, and the fallbacks if it fails — instead of asserting a behaviour it cannot check.

## 2. Decision — execution model

| Motion | Root motion | CMC mode during action | Mechanism and notes |
|---|---|---|---|
| Ground locomotion | **No** | `MOVE_Walking` | Capsule driven by CMC from input; animation follows measured velocity. Root motion for continuous locomotion is rejected: it fights acceleration curves and makes input latency visible |
| Dodge | **Yes** | `MOVE_Walking` | Authored distance; input influence suppressed; distance pre-validated by a capsule sweep (M1 spec §3.5) to choose clip/distance. **CMC performs the translation and its own sweeps** |
| Attacks with travel | **Yes** | `MOVE_Walking` | Root motion supplies travel; `UMotionWarpingComponent` supplies aim within per-attack limits |
| Stationary attacks | **No** | `MOVE_Walking` | In-place clip; damage from hit windows, not translation |
| Traversal (vault/mantle/climb) | **Yes** | `MOVE_Flying` (vertical/ledge paths) or `MOVE_Walking` (walkable paths) | `MOVE_Flying` avoids floor-snapping fighting a mantle arc; both are modes in which CMC's movement update **runs**, so root motion is consumed and collision is swept |
| Authored non-animation travel (kinematic snaps, scripted shifts) | n/a | `MOVE_Walking`/`MOVE_Flying` | `FRootMotionSource_MoveToForce` / `MoveToDynamicForce` applied via CMC, not `SetActorLocation` |
| Hit reactions (small) | **No** | `MOVE_Walking` | Predictability |
| Hit reactions (knockdown) | **Yes** | `MOVE_Walking` | Authored displacement |
| Cinematics | **Yes** | Capsule frozen; mode recorded | Root motion on the mesh; capsule has no input; mode restored on exit |

Engine configuration required:

- `AnimInstance->SetRootMotionMode(ERootMotionMode::RootMotionFromMontagesOnly)`
- `bAllowPhysicsRotationDuringAnimRootMotion = false`
- `bEnableScopedMovementUpdates = true` for root-motion actions (avoids per-update hitches on large translations)
- Movement mode changes are **only** to modes in which CMC's movement update runs. `MOVE_None` is **prohibited** for any action that depends on root motion.

## 3. Decision — verification before trust (provisional mechanism)

The mechanism above is **provisional**. On the first build that supports it, `TDD-Unit.Movement.RootMotionAppliesToCapsule` must:

1. Play a montage with a known authored root-motion displacement.
2. Assert the capsule's world position changed by that displacement within **5%**, in the expected direction, with collision disabled and enabled (two variants).
3. Assert the movement mode was restored.

If the test fails, the mechanism is wrong and is replaced by one of the following, chosen by measurement, in this order of preference:

| Option | Description | Cost |
|---|---|---|
| A | Drive displacement with `FRootMotionSource_MoveToForce` matched to the montage length, instead of consuming animation root motion | Extra authoring: distance must be data, not baked in the clip |
| B | `UTDDCharacterMovementComponent` custom movement mode that explicitly consumes the anim root motion delta | Most control, most code, most risk |
| C | In-place clip plus explicit capsule interpolation with per-substep CMC sweeps | Loses animator-authored arcs; perceived quality drop |

No option is adopted until the test says which is needed. Writing the fallbacks down now is what stops the failure being discovered as a "missing lunge" three months later.

## 4. Decision — collision handling

1. **CMC is the collision authority for all root-motion movement.** Root-motion translation is swept by CMC with its normal per-substep collision; the capsule cannot pass through blocking geometry because an animation says so.
2. **Pre-sweeps are predictions, not authority.** The dodge pre-sweep (M1 spec §3.5) selects distance and fallback clip; it never replaces CMC's sweeps and never writes the capsule transform.
3. **No direct capsule writes.** `SetActorLocation` on the capsule is prohibited during root-motion actions. The only sanctioned non-CMC positional change is the validated traversal exit snap (§5).
4. **Blocked travel degrades by data**, not by clipping: the action's `FallbackMontage`/distance applies; if none applies, the action completes in place and the collision is logged for tuning.
5. **Tunnelling**: CMC substepping is enabled for root-motion actions whose speed exceeds the sweep threshold per frame (data), verified by a fast-lunge collision test in M4.

## 5. Decision — interruption and restoration

| Event | Behaviour |
|---|---|
| Natural end | Montage ends → restoration checklist |
| Declared cancel window | Allowed cancel (e.g. dodge from attack recovery) → restoration checklist, then the new action |
| **Staggering damage** (`bCausesStagger`, posture break, or parry) | Forced `Stagger`, never refusable → if the action had displaced the capsule, resolve a legal resting position first → root motion stops → restoration checklist → hit reaction starts **after** restoration |
| **Non-staggering damage** | Not a state transition. It is an abort request (a) honoured only by states that declare it, inside their declared window, or (b) ignored. If honoured: resolve resting position → restoration checklist → return to that state. Health is affected either way; only control changes |
| Death (lethal damage) | Forced `Dead`, outranks stagger → resolve resting position (a corpse must not be left mid-clip or mid-air) → root motion stops → restoration checklist → death presentation |
| Cinematic takeover | Forced `Cinematic` → action aborted **without** any positional fallback (the cinematic owns placement) → restoration checklist except mode restore → mode frozen and recorded |
| Unpossess / EndPlay / level transition | Restoration checklist must not leave the CMC in a non-default mode; EndPlay asserts restoration in Development |
| Self-cancel | Prohibited inside the state's min dwell (no dodge-cancelling a dodge) |

**Restoration checklist** (every exit path, including aborts; executed as one function so no path can skip a step):

1. Stop the owned montage (and any linked montages).
2. Clear root-motion sources added by the action.
3. Restore the movement mode recorded at action start — **with one documented exception**: if fallback resolution returned `HoldUnsupported` (no validated support for the capsule), the mode is set to `MOVE_Falling` instead, and `Restoration.ModeOverrideFalling` is logged. Restoring a walking mode for an unsupported capsule would produce the prohibited "unsupported grounded state" (M1 spec §3.2.2b/§3.2.2c).
4. Restore CMC tuning values from `UTDDLocomotionComponent` (speed, accel, braking, friction, rotation rate).
5. Restore rotation flags (`bOrientRotationToMovement` / `bUseControllerRotationYaw`).
6. Clear motion-warping targets.
7. Clear the action's status tags (`Status.Invulnerable`, attack tags).
8. Release the input lock and re-evaluate the buffered intent.
9. Publish the state/exhaustion event.

A test asserts all nine steps ran on natural exit **and** on each forced path; a double-restore (step already in the restored state) logs a warning, because it indicates two systems believe they own the action.

**Ordering rule (v1.2):** *positional fallback → restoration → target state entry.* Applying the target state first would start a hit-reaction montage while root motion was still driving the capsule, producing a stagger that travels — the specific failure this ADR exists to prevent. The consequence for staggering damage is deliberate: the character resolves where it legally stands **before** it is staggered, so a stagger on a ledge grip does not end mid-air.

## 6. Decision — traversal exit revalidation

At the exit notify, before any snap:

1. Re-sweep the exit capsule (location **and** rotation) against current collision, including dynamic actors that moved since detection.
2. Verify a walkable floor exists at the exit (downward trace; slope within limits).
3. **Valid** → snap to the exit transform, hand control back to CMC in the restored mode, run the restoration checklist.
4. **Invalid** → take the documented fallback, log `Traversal.ExitInvalid`, publish a diagnostic event, and remain playable. **Never** teleport into geometry.
5. The fallback is not a single option but the ordered resolution defined in M1 spec §3.2.2 (`ResolveAbortFallback`): complete the traversal if past the commit fraction and the exit is *currently* valid; otherwise reverse to the entry side if valid; otherwise drop to a walkable floor beneath and enter `Airborne`/`Land`. If all three fail **or the relocation budget is exhausted**, the terminal hold phase runs: out-of-world first (flow-system handoff), then a validated downward snap onto nearby support, else hold position, mark unsupported (`MOVE_Falling`, no transform write), and log `Traversal.FallbackFailed`.
6. **Every** exit path of a root-motion action — natural completion, invalid exit, non-staggering damage abort, staggering damage, death, cinematic capture, EndPlay — runs fallback resolution (except cinematic capture, which must not move the capsule) followed by the restoration checklist, in that order. The authoritative enumeration is M1 spec §3.2.3 (E1–E7).
7. A cinematic takeover must **not** trigger a positional fallback; the cinematic system owns placement, and a silent drop mid-shot would read as a teleport.
8. **The attempt budget bounds relocation only.** `MaxRelocationAttempts` (total per call, clamped [0, 3], default 3) limits how many of the *relocating* candidates — complete, reverse, drop-to-floor — may be attempted. It never bounds whether the capsule is placed safely: the hold phase is entered on budget exhaustion, on all-candidates-failed and on a budget of 0, and always produces exactly one outcome. A configuration value must never be able to skip the support check (M1 spec §3.2.2a.1).
9. **Placement validation is mandatory and is repeated at the instant of application.** A transform validated at candidate selection may be stale by the time it is applied (a door closed, a pawn stepped in, a platform moved). The write function performs the validation itself and is the only code permitted to write the capsule transform; on failure the stored transform is discarded, the next candidate is attempted from the capsule's current position, and only when no candidate succeeds does the hold path apply. A stale transform is never applied.
10. **Hold never refuses or delays a forced transition.** If no valid placement exists, the capsule keeps its position, the CMC enters `MOVE_Falling`, and the forced `Stagger`/`Dead` proceeds immediately — with the hit reaction playing while falling, ragdoll death simulating immediately, and montage deaths deferred to first grounding per data. Only when the capsule falls out of the world does the flow system take over: this is reported as the distinct result `FellOutOfWorld`, evaluated before the grounded-hold check, and is never reported as a placement (checkpoint respawn, logged as `Traversal.FellOutOfWorld`).

## 7. Decision — warping limits are configurable, not fixed

The attack warp limits of 300 cm and 60° are **provisional defaults**, not rules:

- Stored in `DA_MovementConfig` with a per-attack override on `UTDDAttackDefinition`.
- Never hard-coded in C++.
- To be tuned in M4 against measured lunge distances and the visual result of warping from extreme angles.
- Out-of-range requests are refused (attack plays without warp) and logged, rather than silently clamped into an unnatural pose.

## 8. Consequences

**Positive**
- Collision correctness is delegated to the engine's movement component, which is the only subsystem that already does this well.
- Locomotion responsiveness is governed by CMC tuning alone and stays measurable (M1 AC-04…AC-06).
- Interruption and restoration are enumerated, so "the character got stuck in a dodge" has one place to look.
- Unverified assumptions are converted into a test that must pass before the mechanism is trusted.

**Negative**
- Root-motion actions need authored fallbacks and per-action data.
- Dodge distance against geometry is deliberately *shorter* than authored; this must be communicated in feel testing or it reads as a bug.
- Traversal requires revalidation logic and a fallback path, which is extra work in M2.
- The mechanism may be replaced after first build (options A–C), costing rework — accepted, because the alternative is shipping on an assumption.

## 9. Alternatives considered

- **`MOVE_None` during root-motion montages** (v1.0 proposal): rejected — movement update may not run, so root motion may not be applied; also disables CMC collision during the action. Not adopted without proof; and if proof existed, it would still be inferior to a mode with collision.
- **Root motion for ground locomotion**: rejected — fights acceleration, exposes latency, breaks collision responsiveness.
- **No root motion anywhere (fully capsule-driven)**: rejected — sliding lunges, weak impact.
- **Warp-everything (no root motion, all warping)**: rejected as a blanket rule; warping complements root motion rather than replacing it.
- **Direct `SetActorLocation` for action travel**: rejected — bypasses collision, causes clipping and stuck states.

## 10. Verification

| Test | Asserts |
|---|---|
| `TDD-Unit.Movement.RootMotionAppliesToCapsule` | Capsule displacement matches authored root motion within 5%, with and without collision |
| `TDD-Unit.Movement.RootMotionRestoresMovementMode` | All nine restoration steps run on natural and forced exits; 100 random actions |
| `TDD-Functional.Movement.DodgeRespectsCollision` | No per-frame penetration; clamping; refusal when starting inside geometry |
| `TDD-Functional.Movement.TraversalExitRevalidation` (M2) | Invalid exit → fallback, no teleport, checklist ran |
| M4 (planned) | Fast lunge does not tunnel; warp limits respected or refused and logged |

## 11. Reversal conditions

- If `RootMotionAppliesToCapsule` fails, the execution mechanism is replaced per §3; the collision, interruption and restoration decisions stand unchanged.
- If animation testing shows locomotion quality is unacceptable without root-motion starts/stops, a **scoped exception** may be granted for start/stop anticipation only — never for continuous locomotion — and only if M1 thresholds still pass.

## 12. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-16 | Initial policy: per-motion table, `MOVE_None` proposal, fixed 300 cm/60° limits |
| **1.1** | **2026-11-16** | Per TD review item 8: `MOVE_None` withdrawn as an unverified assumption and prohibited for root-motion actions; execution model restated with modes in which CMC's movement update runs; verification-before-trust requirement added with three documented fallbacks; collision authority explicitly assigned to CMC with pre-sweeps demoted to predictions; interruption and a nine-step restoration checklist specified; traversal exit transforms revalidated with a defined fallback; warp limits made configurable with provisional defaults; alternatives and reversal conditions expanded |
| **1.2** | **2026-11-16** | Review round 2 alignment: interruption table now separates staggering damage, non-staggering damage (abort request, not a transition), lethal damage and cinematic capture; the ordering rule *fallback → restoration → target entry* is stated and justified; traversal §6 references the ordered `ResolveAbortFallback` resolution and enumerates all exit paths (E1–E7) instead of a single "damage/death" clause; prohibition on positional fallback during cinematic capture added. No collision, execution-model, or restoration-step changes. |
| **1.3** | **2026-11-16** | Final v1.2 clarifications: restoration step 3 gains its single documented exception (`MOVE_Falling` when placement is unsupported, logged); §6 gains the mandatory double validation at the instant of application with the next-candidate-then-hold rule and the explicit prohibition on applying a stale transform; hold semantics restated so a forced transition is never refused or delayed and a montage death does not play in mid-air. No changes to the execution model, collision authority, checklist steps 1–2 and 4–9, or warp limits. |
| **1.4** | **2026-11-16** | Final v1.3 correction: the fallback attempt budget is separated from terminal hold resolution. `MaxRelocationAttempts` (renamed from `MaxFallbackAttempts`; total per call, clamp [0, 3], default 3) bounds only the relocating candidates, so hold-grounded is always evaluated after relocation fails or is exhausted; hold-unsupported remains the guaranteed zero-write fallback and out-of-world is a distinct flow-system result. No change to the execution model, collision authority, restoration steps, or warp limits. |