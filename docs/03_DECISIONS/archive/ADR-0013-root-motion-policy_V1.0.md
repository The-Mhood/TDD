# ADR-0013 — Root motion policy

- **Status:** Proposed (authored by Agent 1; requires Technical Director approval)
- **Date:** 2026-11-16
- **Deciders:** Technical Director; Agent 1 (owner); Agent 2 (consumes enemy attack timing)
- **Owning agent:** 1

## Context
In a third-person action game, mixing engine-driven capsule movement with animation root motion is the most common source of control-feel bugs: characters that slide, that feel laggy because root motion is fighting acceleration curves, that clip through geometry when a lunge is authored too long, that get stuck because a movement mode was never restored, or that can be steered mid-dodge in ways the animation cannot express. UE offers root motion per montage, `ERootMotionMode`, and Motion Warping, but no policy — the policy is ours to choose and must be chosen once.

## Decision
| Motion | Root motion | Mechanism |
|---|---|---|
| Ground locomotion | **No** | Capsule driven by CMC; animation follows measured velocity (motion matching or blendspace) |
| Dodge | **Yes** | Authored distance, pre-validated by forward sweep, clamped by clearance |
| Attacks with travel | **Yes** | Root motion supplies travel; `UMotionWarpingComponent` supplies aim (≤ 300 cm, ≤ 60°) |
| Stationary attacks | **No** | In-place clips |
| Traversal | **Yes** | Entry/exit validated, Motion Warping for alignment, capsule snapped only at the exit notify |
| Hit reactions | **No** (small) / **Yes** (knockdown) | Displacement only where the design needs authored travel |
| Cinematics | **Yes** | Capsule frozen, restored on exit |

Engine rules: `ERootMotionMode::RootMotionFromMontagesOnly`; `bAllowPhysicsRotationDuringAnimRootMotion = false`; movement mode explicitly set before and restored after every root-motion action, including abort paths; every action has a `FallbackMontage` for blocked travel.

## Consequences
- **Positive:** locomotion responsiveness is governed by CMC tuning alone (measurable per M1 AC-02/AC-03), not by whatever clip is playing.
- **Positive:** authored attack/dodge/traversal distances stay under designer control while collision safety remains guaranteed by a pre-sweep.
- **Positive:** one place to look when "the character got stuck" — the movement-mode restore path, covered by a unit test.
- **Negative:** attacks cannot inherit travel from an animator's in-place tweak without a data change.
- **Negative:** root-motion actions need explicit collision fallbacks, which is extra authoring per attack.
- **Negative:** dodge distance repeatability depends on the sweep result, so a dodge against geometry is *shorter* by design — this must be communicated in feel testing or it reads as a bug.

## Alternatives considered
- **Root motion for locomotion** — better-looking starts/stops in isolation, but fights acceleration, exposes input latency, and breaks collision responsiveness. Rejected.
- **No root motion anywhere (fully capsule-driven attacks)** — predictable but produces sliding lunges and weak impact. Rejected.
- **Warp-everything (no root motion, all warping)** — tunable but every attack becomes a warp tuning problem and gaps open at extreme ranges. Rejected as a blanket rule; warping is used *with* root motion, not instead of it.

## Verification
- `TDD-Unit.Movement.RootMotionRestoresMovementMode` (100 randomised actions, including aborts).
- `TDD-Functional.Movement.DodgeRespectsCollision` and `TDD-Functional.Movement.DodgeDistanceRepeatable`.
- M4: attack lunge never clips geometry; warp range clamp verified per attack definition.

## Reversal condition
If animation testing shows locomotion quality is unacceptable without root-motion starts/stops, revisit **only** for start/stop anticipation windows (a scoped exception), not for continuous locomotion. Any exception must be measured against M1 thresholds before adoption.
