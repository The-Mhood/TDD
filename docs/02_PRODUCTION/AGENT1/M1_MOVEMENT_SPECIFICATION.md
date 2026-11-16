# MILESTONE 1 — IMPLEMENTATION SPECIFICATION
## Responsive, testable third-person character controller

**Project:** THE DISOBEDIENT DAUGHTER
**Agent:** 1 — Gameplay, Character and Combat Engineering
**Document:** TDD-A1-M1-SPEC-001
**Version:** 1.1 — revised after Technical Director review (2026-11-16)
**Date:** 2026-11-16
**Supersedes:** v1.0 (`archive/M1_MOVEMENT_SPECIFICATION_V1.0.md`, preserved unchanged)
**Status:** `DESIGN_ONLY` — nothing in this document is implemented or verified
**Parent:** `GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` v1.1 (TDD-A1-ASSESS-001)
**Governing:** TDD-MEAD-001 §4, §8, §13, §14, §15; ADR-0002, ADR-0005, ADR-0012, ADR-0013 v1.1
**Change log:** §13 of this document explains every correction from v1.0

---

## 0. Revision note (v1.1)

The Technical Director accepted the architecture and milestone approach in principle and required nine corrections before implementation. This revision makes them, and **changes no implementation intent**: M1 is still a responsive, measured, testable controller. What changed is precision.

| Review item | Effect on this document |
|---|---|
| 1 Reconciliation | M1 now has **one gate**: AC-01…AC-31 in §4, referenced identically by the assessment (§8) and by this spec (§9) |
| 2 Latency | §3.4 defines three stages (L1/L2/L3) with frame-index definitions and 60/120 FPS measurement; the v1.0 same-frame/next-frame contradiction is resolved and the false "one-frame animation floor" claim is withdrawn |
| 3 Dodge clearance | §3.5 restates the sweep as a **capsule sweep that already includes the radius**; the v1.0 formula double-counted it |
| 4 Camera | §3.6 replaces one blanket rule with **five separate criteria** and per-mode thresholds |
| 5 State transitions | §3.2 adds preconditions, forced transitions, interruption windows, exit actions, recovery conditions, dwell and buffer policy |
| 6 Steps | §4/§5 define the **50 cm step outcome as blocked**, and add descent, angled approach, sprint and corner cases |
| 7 Ownership | §3.1 and §3.6 resolve input-component and camera-rig ownership using Unreal's lifecycle, not convention |
| 8 Root motion | ADR-0013 v1.1, §3.5/§3.7 here: no `MOVE_None` assumption, exit-transform revalidation, warp limits configurable |
| 9 Core types | Appendix A restated as **proposals pending Agent 3 review**; Agent 1 creates no Core types |

**No implementation has begun.** No code, no compilation, no tests, no measurements. All statuses remain `DESIGN_ONLY` or `BLOCKED`.

---

## 1. Objective

Deliver a third-person character controller that is responsive **by measurement**, correct under enumerated physics conditions, and testable without a human watching, in a controlled test environment, before any combat work begins.

M1 is complete when a build demonstrates **AC-01…AC-31** (§4) with quoted results — not before, and not on the strength of an opinion that it feels good.

**Not in M1:** combat, damage, enemies, weapon, traversal execution (M2), interaction (M2), animation content beyond a stock mannequin.

---

## 2. Scope and deliverables

### 2.1 Code deliverables (to be written only after B-1…B-6 exist)

| File | Purpose |
|---|---|
| `Public/Player/TDDPlayerCharacter.h/.cpp` | `ATDDPlayerCharacter` — capsule, mesh, component host, input component creation |
| `Public/Player/TDDPlayerController.h/.cpp` | `ATDDPlayerController` — device routing, camera manager creation, pause/menu input component |
| `Public/Player/TDDPlayerInputComponent.h/.cpp` | `UTDDPlayerInputComponent : UEnhancedInputComponent` — intent production, mapping-context push/pop |
| `Public/Player/TDDCharacterStateMachine.h/.cpp` | `UTDDCharacterStateMachine` — the only state authority (§3.2) |
| `Public/Movement/TDDCharacterMovementComponent.h/.cpp` | `UTDDCharacterMovementComponent` — step-down smoothing, slope overrides, root-motion hooks (§3.2/§3.7) |
| `Public/Movement/TDDLocomotionComponent.h/.cpp` | Gait/stance resolution, CMC parameter application, provider driving |
| `Public/Movement/TDDLocomotionAnimProvider.h/.cpp` | Interface + `UTDDBlendSpaceProvider`; MM provider declared and returning `NotImplemented` |
| `Public/Movement/TDDMovementConfig.h` | `UTDDMovementConfig` data asset |
| `Public/Movement/TDDStateRules.h` | `FTDDStateRuleRow`, rules table wrapper |
| `Public/Movement/TDDInputBuffer.h` | Pure-logic buffer (no world dependency) |
| `Public/Movement/TDDDodgeSpec.h` | `FTDDDodgeSpec` + pure clearance/window math (§3.5) |
| `Public/Camera/TDDPlayerCameraManager.h/.cpp` | Shakes, post-process/FOV blending (PC-owned) |
| `Public/Camera/TDDCameraRigComponent.h/.cpp` | Desired rig computation, boom collision policy, acquisition events (pawn-owned) |
| `Private/Movement/TDDMovementMetricsComponent.h/.cpp` | Instrumentation, CSV, console commands, latency frame stamps (§3.8) |
| `Private/Tests/TDDMovementUnitTests.cpp` | `TDD-Unit.Movement.*` |
| `Source/TDDTests/Private/Movement/TDDMovementFunctionalTests.cpp` | `TDD-Functional.Movement.*` |

### 2.2 Content deliverables

| Asset | Purpose |
|---|---|
| `Content/TDD/Test/L_TDD_Test_Movement` | Controlled environment (§7) |
| `Content/TDD/Data/Movement/DA_MovementConfig` | Tuning + dodge/warp/camera params |
| `Content/TDD/Data/Movement/DT_StateRules` | State semantics data (§3.2) |
| `Content/TDD/Data/Movement/DA_CameraConfig` | Five camera criteria parameters (§3.6) |
| `Content/TDD/Input/DA_InputConfig`, `IMC_Exploration`, `IMC_Menu` | Input (co-owned with Agent 3's B-4) |
| `Content/TDD/Test/WBP_TDDMovementOverlay` | Metrics overlay (dev) |

### 2.3 Foundation deliverables (Agent 3, unchanged from v1.0)

B-1…B-6 (assessment §3.1) including the **proposed** Core contracts in Appendix A. M1 cannot start without them. I will not create a parallel Core or a second input setup.

### 2.4 Verification deliverables (new emphasis in v1.1)

For every AC: the test name, the raw result line, and the capture/CSV reference. The gate is auditable: a reviewer can rerun `TDD.Movement.Report` and compare.

---

## 3. Class specifications

### 3.1 `ATDDPlayerCharacter` and input-component ownership (corrected, review item 7)

| Aspect | Specification |
|---|---|
| Base | `ACharacter` |
| Capsule | Half-height 88 cm, radius 34 cm, parameterised in `DA_MovementConfig`. **Not** derived from the mannequin's visual height |
| Movement component | `UTDDCharacterMovementComponent` (§2.1), set via `ACharacter`'s movement component class |
| Input component class | `InputComponentClass = UTDDPlayerInputComponent::StaticClass()` (or an override of `CreatePlayerInputComponent()`), so the pawn receives an Enhanced Input component of my subclass |
| Tick | `PrimaryActorTick` disabled; components tick with written justification |
| Mesh | Stock mannequin, labelled `PLACEHOLDER-A1-01`. No Adanna-specific tuning applied to it |

**Unreal lifecycle, stated explicitly because v1.0 was ambiguous:**

```
APlayerController::Possess(pawn)
  → APawn::PawnClientRestart()
      → APawn::CreatePlayerInputComponent()      // returns InputComponentClass instance
      → Pawn->SetupPlayerInputComponent(InputComponent)
      → my bindings registered against that component
  → Pawn's InputComponent is pushed onto the PlayerController's input stack
On unpossess/destroy: the pawn's input component goes with the pawn.
```

Consequences that drive the design:

1. **Gameplay bindings live on the pawn**, because the component is created by the pawn during possession. Binding gameplay actions on the controller would work only for the currently possessed pawn and would leave me handling possession changes manually.
2. **The pawn's input component does not exist before possession.** Any code that assumes it exists at `BeginPlay` is wrong; mapping contexts are pushed on possession and popped on unpossession.
3. **The controller keeps a second, tiny input component** for actions that must survive pawn death or cinematic control (pause, skip-cinematic, UI confirm). Two components, two clearly different jobs — not one component with conditional bindings, which is how "pause stops working when the player dies" bugs happen.
4. Mapping contexts are added on possess and removed on unpossess; the state machine *requests* context switches through the input component, it does not create contexts.

### 3.2 State machine and transition semantics (expanded, review item 5)

`UTDDCharacterStateMachine` is the only writer of player state. Components call `RequestState()`; forced transitions use `ForceState()`. Both funnel through one decision function:

```
RequestState(Target, Reason):
  1. if bTransitionInProgressAndTargetIsForcedIn -> queue after current forced exit (never interleave)
  2. if Target.priority < Current.priority && !Forced(Reason) -> refuse, log Verbose (pair + reason)
  3. if !EntryPreconditions(Target).IsSatisfied() -> refuse, apply buffer policy (see below)
  4. if Current.minDwell not elapsed && !Forced(Reason) -> refuse (anti-flap)
  5. run Current.ExitActions
  6. set state, run Target.EntryActions
  7. broadcast OnStateChanged(old, new, reason)
```

**Priority (higher wins, forced only):** `Dead` 100 → `Cinematic` 90 → `Stagger` 80 → `Attack`/`Block`/`Parry` 60 → `Dodge` 50 → `Traversal` 40 → `Land` 30 → `Locomotion`/`Sprint`/`Idle` 10.

**Rules that the matrix alone could not express:**

| Rule | Statement |
|---|---|
| Forced transitions | `Dead`, `Cinematic`, `Stagger` can be forced by their owners at any time and cannot be refused. They preempt regardless of priority or dwell. The previous state is recorded for restoration where applicable (`Cinematic`), never for `Dead` |
| Requested transitions | All other transitions are requests and may be refused with a logged reason. A refusal is not silent |
| Interruption | A state may only be interrupted inside its declared windows and only by callers it lists. Damage/stagger/death/cinematic are always allowed (they are forced). Root-motion actions (dodge, traversal, attacks) are **not** self-cancellable during their min dwell |
| Exit actions | Every exit runs the same checklist, always, including on forced exits and aborts: stop the owned montage; clear owned status tags; restore movement mode/flags; restore rotation mode; release the input lock; clear motion-warp targets; publish the state-changed event |
| Recovery | A state ends when its recovery condition is met: montage end, or a declared cancel window satisfied by a buffered intent, or an explicit timer. Recovery is data, not code paths scattered per state |
| Buffer policy | Requests received while refused are buffered **only** if the current state declares `bBufferRequests`; otherwise dropped with a Verbose log. Buffered requests expire on their buffer window (§3.4) and are consumed exactly once |
| No permanent lock | No state may end with input permanently ignored unless it is `Cinematic` or `Dead`, and both have tested exits (AC-29) |

**Per-state table A — entry, exit, recovery, dwell**

| State | Entry preconditions | Exit actions | Recovery / end condition | Min dwell |
|---|---|---|---|---|
| `Idle` | grounded; speed < 5 cm/s; no action state active | publish event | any movement/action intent accepted | 0.05 s |
| `Locomotion` | grounded; input above deadzone; state allows movement | restore gait params | input below deadzone (→ `Idle`) or action accepted | 0.05 s |
| `Sprint` | grounded; sprint held or toggled on; input magnitude ≥ 0.7; (M3+: stamina > 0) | restore non-sprint gait/accel | sprint released or input dropped (→ `Locomotion`) | 0.10 s |
| `Airborne` | became ungrounded (jump, fall, knockback) | clear airborne tag | grounding (→ `Land`) | 0 |
| `Land` | grounding while `Airborne` | clear landing tag; restore gait | landing timer elapsed (scaled by fall speed) **or** dodge cancel if fall speed < threshold (data) | landing timer |
| `Dodge` | grounded (or air-dodge enabled); cooldown expired; direction resolvable; clearance > 0; (M3+: stamina) | restore movement mode; clear `Status.Invulnerable`; stop montage | montage end or clamped-distance end | 0.15 s |
| `Attack` (M3) | grounded or air-attack allowed; stamina; weapon ready | stop montage; end hit windows; restore rotation mode; clear attack tags | montage end **or** cancel window satisfied by buffered intent | per attack data |
| `Block` (M3) | grounded; guard allowed | clear blocking tag; restore speed | guard released beyond grace (0.08 s) | 0.08 s |
| `Parry` (M3) | inside parry window from block input | clear parry tag | window expiry or success resolution | window |
| `Stagger` | forced by damage, posture break or parry | clear stagger tag; restore movement/rotation | stagger duration **and** hit-reaction montage end (whichever is later) | stagger duration |
| `Traversal` (M2) | valid candidate; grounded; capsule clear | revalidate exit transform; snap; restore; stop montage | exit notify reached **and** exit transform valid | montage |
| `Interaction` (M2) | interactable in range and allowed | cancel interaction; restore | hold complete, or cancel-on-move (data) | 0 |
| `Cinematic` | forced by cinematic subsystem | restore prior state; restore input/mapping context | subsystem reports end or skip | per sequence |
| `Dead` | forced by lethal damage | disable input; start death presentation | respawn forced by flow system | n/a |

**Per-state table B — forced in/out, interruption, buffer policy**

| State | Forced in (priority) | Forced out | Interruptible by (window) | While locked |
|---|---|---|---|---|
| `Idle` | Cinematic, Dead, Stagger | — | any request | buffer `Dodge`/`Attack` only |
| `Locomotion` | Cinematic, Dead, Stagger | — | any request | buffer `Dodge`, `Jump`, `Attack` |
| `Sprint` | Cinematic, Dead, Stagger | — | any request | buffer `Dodge`; drop `Attack` (unless dash attack approved) |
| `Airborne` | Cinematic, Dead, Stagger | `Land` on grounding | `Dodge` only if air-dodge enabled | drop `Attack` |
| `Land` | Dead, Stagger | — | `Dodge` after landing frame if fall speed < threshold | buffer `Dodge` |
| `Dodge` | Dead, Stagger, Cinematic | — | damage/parry/stagger/death only; no self-cancel in 0–0.15 s | buffer `Attack` after 0.15 s; drop `Dodge` (cooldown) |
| `Attack` | Dead, Stagger, Cinematic | — | `Dodge` from cancel window; damage if attack declares interruptible; parry | buffer `Attack` (chain), `Dodge`; drop `Jump` |
| `Block` | Dead, Stagger, Cinematic | guard break → `Stagger` | parry success; guard break | drop `Dodge` while guard-raising (0.08 s) |
| `Parry` | Dead, Stagger, Cinematic | success → attacker stagger, self returns to `Block` | damage | drop all except forced |
| `Stagger` | (is forced) | — | `Dead` only | drop all |
| `Traversal` | Dead, Cinematic | damage abort → safe fallback then `Locomotion` | damage, death, cinematic | drop all except forced |
| `Interaction` | Dead, Cinematic, Stagger | movement input if cancel-on-move | damage | drop all |
| `Cinematic` | (is forced) | subsystem end/skip | nothing | drop all; pause/skip handled by PC input component |
| `Dead` | (is forced) | respawn | nothing | drop all |

Data model: one `FTDDStateRuleRow` per state containing the preconditions (as declarative flags + a small enum of checks, not script), exit-action flags, recovery condition type and values, min dwell, locks, interruption mask and buffer policy. The row is authored in `DT_StateRules`; the state machine interprets it. Tests enumerate all 14×14 pairs and assert that unlisted pairs are refused **and** that listed pairs satisfy their preconditions (AC-22, AC-23).

### 3.3 `UTDDLocomotionComponent` (unchanged from v1.0)

Gait resolution, CMC parameter application (sole writer of `MaxWalkSpeed`, `MaxAcceleration`, `BrakingDecelerationWalking`, `GroundFriction`, `RotationRate`), provider driving, camera-relative movement, combat strafe mode, air control.

| Gait | Max speed (cm/s) | Max accel (cm/s²) | Braking decel | Rotation rate (°/s) |
|---|---|---|---|---|
| Idle | 0 | 2048 | 2400 | 600 |
| Walk | 220 | 1600 | 2000 | 600 |
| Jog | 480 | 2048 | 2400 | 540 |
| Sprint | 700 | 2400 | 1600 | 420 |

These remain engineering defaults pending the Creative Director's feel pass; all values are data.

### 3.4 Input, buffering and the latency model (rewritten, review item 2)

**Ownership** per §3.1. **Intent** enum: `Move2D, Look2D, Sprint, Jump, Dodge, LightAttack, HeavyAttack, Block, Parry, LockOn, Interact, TraversalConfirm, Pause`.

Buffer policy (pure logic, `FTDDInputBuffer`, no world dependency):

| Intent | Window | Consumed by | Cleared by |
|---|---|---|---|
| `Dodge` | 0.20 s | state machine on recovery end / landing | expiry, `Stagger`, `Dead`, `Cinematic` |
| `Jump` | 0.15 s | state machine on grounding (plus 0.12 s coyote) | expiry, `Dead` |
| `LightAttack` / `HeavyAttack` | 0.20 s | combat component (M3) | expiry, `Stagger`, `Dead` |
| `Parry` | 0.15 s window | combat component (M3) | expiry |
| `Block` | held + 0.10 s release grace | state machine | release beyond grace |
| `Interact` | not buffered | interaction component (M2) | — |
| `LockOn`, `Pause` | immediate | direct | — |

**The latency model (this replaces v1.0 §4.5 of the assessment and resolves its contradiction).**

v1.0 contained two incompatible statements: that intent is accepted and velocity changes on the same frame, and that the pose lags by one frame because "animation evaluates after movement". The second was an assumption about tick groups presented as fact, and it is withdrawn. v1.1 defines three stages, each with its own reference points:

| Stage | Definition | Reference points | Requirement |
|---|---|---|---|
| **L1** sample → intent | Input event delivered to the engine → intent recorded by the input component | `FrameInjected` → `FrameIntentRecorded` | ≤ **1** frame. **0** in the deterministic harness, where injection is stamped at the frame boundary before input processing |
| **L2** intent → first velocity change | `FrameIntentRecorded` → first frame where `CMC->Velocity` differs from the pre-intent baseline by > **1 cm/s** | `FrameIntentRecorded` → `FrameVelocityChanged` | **0** frames — same `TG_PrePhysics` pass. Any other result is a tick-order defect, not a tuning issue |
| **L3** intent → pose reflects it | `FrameIntentRecorded` → first frame where the animation parameters (speed/gait) reflect the new velocity | `FrameIntentRecorded` → `FramePoseUpdated` | ≤ **1** frame; the **measured** value is reported (0 or 1), never predicted |

Why this is the correct decomposition:

- L2 is the one that must be zero, because input processing, intent creation, state decision and CMC movement all happen in the same `TG_PrePhysics` pass. If L2 is 1, two things are in the wrong tick group and no amount of tuning fixes it.
- L1 cannot be zero in the real world for a device polled mid-frame; it is bounded at one frame, and the automation harness deliberately injects at the frame boundary so the tests isolate engine behaviour from OS sampling (otherwise test noise would be mistaken for design).
- L3 is the only stage where the engine's tick groups could add a frame. It is measured, not asserted, and if it is 1 the only sanctioned remedy is the measured mesh-tick-group experiment (with the M2 foot-slide budget as the constraint). This is honest: v1.0 claimed a number I could not verify.

**Measurement procedure (both frame rates):**

1. `t.MaxFPS 60`, vsync off; run. Repeat with `t.MaxFPS 120`. Physics substepping off for latency tests, recorded when changed.
2. The metrics component stamps `FrameInjected` (from the test injector, at `TG_PrePhysics` with priority before the player controller), `FrameIntentRecorded`, `FrameVelocityChanged`, `FramePoseUpdated` — all from one monotonic frame counter.
3. Assertions are made on **frame indices**, then reported in **frames and milliseconds** (16.667 ms at 60 FPS; 8.333 ms at 120 FPS).
4. The harness also runs the *worst case*: injection stamped mid-frame (after input processing), which must yield L1 = 1 and L2 = 0, proving the bound rather than only the best case.
5. Device-to-photon latency (OS polling, scanout, display) is **explicitly out of engine scope**; if the Creative Director requires it, it is measured externally with a latency tester and reported separately so it can never be confused with L1–L3.

### 3.5 Dodge, and the corrected collision-clearance calculation (review item 3)

`FTDDDodgeSpec` (data): `Distance` (cm, authored), `Duration` (s), `InvulnStart`/`InvulnEnd` (s of gameplay time), `Cooldown` (s), `FallbackMontage`, `bRootMotion`.

**What v1.0 got wrong:** the formula `min(Authored, ForwardSweepClearance - CapsuleRadius - SafetyMargin)` subtracted the capsule radius from a quantity whose shape was never defined. If the sweep is capsule-shaped, the radius is already inside the shape and subtracting it again shortens the dodge by 34 cm for no reason; if a ray was intended, the radius must be subtracted. Undefined units plus double-counted geometry.

**v1.1 definition — capsule sweep, radius included:**

```cpp
// Shape: exactly the CMC capsule. The radius is part of the swept shape,
// so it must NOT be subtracted again from the hit distance.
const float  R = CMC->GetScaledCapsuleRadius();
const float  H = CMC->GetScaledCapsuleHalfHeight();
const FCollisionShape Shape = FCollisionShape::MakeCapsule(R, H);

const FVector Start = CMC->GetActorLocation();          // capsule centre == actor origin
const FVector End   = Start + Dir2D * Spec.Distance;    // planar: Z preserved

FCollisionQueryParams P(SCENE_QUERY_STAT(TDDDodgeSweep), /*bTraceComplex*/ false, GetOwner());
P.AddIgnoredActor(GetOwner());
P.AddIgnoredActor(LockedTargetActor);                   // if any

FHitResult Hit;
const bool bBlocked = GetWorld()->SweepSingleByChannel(
    Hit, Start, End, FQuat::Identity, ECC_Pawn, Shape, P);

float ResolvedDistance = Spec.Distance;
if (bBlocked)
{
    // Hit.Location is the swept capsule's CENTRE at contact: radius accounted for.
    const float Available = (Hit.Location - Start).Size2D();
    ResolvedDistance = FMath::Max(0.f, Available - Config.DodgeSafetyMargin);   // margin only
}
ResolvedDistance = FMath::Min(ResolvedDistance, Spec.Distance);
```

Stated precisely, because precision is the point:

| Question | Answer |
|---|---|
| What geometry does the sweep use? | A capsule identical to the CMC capsule (`MakeCapsule(R, H)`), swept from the current capsule centre along the dodge direction in the horizontal plane, ending at the capsule centre for the authored distance |
| Is the capsule radius already accounted for? | **Yes.** It is inside the swept shape, so `Hit.Location` is the *centre* at contact. The radius is **not** subtracted again. Only `DodgeSafetyMargin` (default **2 cm**) is subtracted |
| If a ray were used instead | Then and only then would the formula be `HitDistance - R - Margin`. A ray is rejected because it permits corner clipping |
| Channel and filters | `ECC_Pawn` (matches CMC blocking semantics), query-only, ignores the owner, ignores the current lock-on target if it would block, `bTraceComplex = false` |
| Start overlapping geometry | `Hit.bStartPenetrating` → **refuse the dodge**: no montage, no movement, log `Dodge.Refused.StartingPenetration`, remain in the current state. Clamping to zero would look like a button that does nothing while consuming cooldown |
| Vertical / slopes | Dodge is planar (Z preserved). After clamping, a downward trace at the clamped end position checks floor difference; if the floor under the end is > 10 cm different, distance is reduced iteratively (max 3 iterations) until the end is on walkable floor |
| Who actually moves the capsule? | **CMC**, not this sweep (ADR-0013). The sweep is a *prediction* used to pick distance and fallback clip; CMC's own sweeps remain authoritative for collision. Tests assert no penetration per frame, which is the property that matters |
| Repeatability | On flat ground with no obstruction, `ResolvedDistance == AuthoredDistance`, so distance is deterministic (AC-19) |

Invulnerability window conversion (unchanged intent, restated): `InvulnMontageRange = [InvulnStart/Duration, InvulnEnd/Duration] × MontageLength`, evaluated in gameplay seconds so hitstop and slow motion cannot desynchronise the window.

### 3.6 Camera: ownership and five stability criteria (rewritten, review items 4 and 7)

**Ownership:**

| Element | Owner | Responsibility |
|---|---|---|
| `ATDDPlayerCameraManager` | created by `ATDDPlayerController` | The only place `UCameraModifier`, camera shakes, FOV and post-process blends are applied. UE mandates that shakes go through the camera manager |
| `UTDDCameraRigComponent` | on `ATDDPlayerCharacter` | Computes *desired* rig parameters (arm length, socket offset, FOV, lock-on framing) from gameplay state; writes them to the spring arm. Never applies shakes |
| `USpringArmComponent` + `UCameraComponent` | on `ATDDPlayerCharacter` | Physical rig |
| `CineCameraActor` / Sequencer | cinematic subsystem (Agent 2) | Takes the view target; rig component detects takeover, suspends writes, restores over 0.4 s |

Rigs are unchanged from v1.0 (`Explore` 90°/320 cm, `CombatSoft` 95°/380 cm, `LockOn` 95°/400 cm, `Traversal` 90°/360 cm, `Cinematic`). Boom probe: sphere sweep, radius 12 cm, minimum resolved boom 35 cm (below that, a close-up mode engages rather than the camera entering the character).

**The five criteria (v1.0 replaced):** v1.0's "no camera snap faster than 720°/s except lock-on" used an acquisition bound as a universal jitter threshold and therefore could not distinguish a bad obstruction recovery from an intentional snap. Each failure mode now has its own metric, threshold (all **[A1]** proposals for TD approval) and event flag.

| # | Failure mode | Threshold | How measured | Exemptions |
|---|---|---|---|---|
| 1 | **Penetration** | Camera never closer than **10 cm** to blocking geometry (sphere sweep, radius 12 cm, from pivot to camera) | Every frame over a scripted 60 s sweep in 1.2 m and 2.0 m corridors; also sampled at 5° yaw steps | None. A single violation fails |
| 2 | **Angular jitter** | Steady following: per-frame angular delta ≤ **6°/frame**; jerk (second difference) ≤ **3°/frame²**; ≤ **3 sign changes** of the delta in any 10-frame window | Derived from recorded camera yaw/pitch per frame | Frames flagged `AcquisitionActive` |
| 3 | **Sudden displacement** | Normal follow ≤ **10 cm/frame**; during an *active obstruction* ≤ **25 cm/frame**; never > **15 cm/frame** without the obstruction flag | Camera position delta per frame + boom length delta | Obstruction-forced frames (flagged), which are still bounded at 25 cm |
| 4 | **Obstruction recovery** | Re-extension ≤ **150 cm/s** (configurable 80–200), **monotonic** (no overshoot), complete within **0.6 s** for obstructions under 90 cm | Boom length time series after the obstruction clears | Never snaps; a snap fails |
| 5 | **Intentional acquisition (lock-on)** | Whitelisted and bounded: blend **0.20 s**, total slew ≤ **120°**, peak ≤ **600°/s**, completes ≤ **0.35 s** | Same recorder, with the acquisition event flag set | This is the *only* sanctioned fast rotation, and only with the flag |

Rationale for the numbers: 6°/frame at 60 FPS equals 360°/s sustained, which is comfortably above normal follow speed for a 540°/s character rotation and therefore only trips on genuine instability; 3°/frame² distinguishes a smooth zoom from a fight between spring-arm smoothing and collision resolution; 10 cm/frame bounds translation so a pull-in reads as a move rather than a teleport. **720°/s is retained only as the acquisition absolute ceiling in criterion 5, not as a jitter rule.** All thresholds are data, and are expected to be tuned once real captures exist.

Camera *feel* remains a T5 manual gate; the five criteria above are automated.

### 3.7 Traversal: exit-transform revalidation (review item 8)

Traversal executes in M2, but the rule is fixed now because it affects the movement component interface:

1. Candidate detected and validated (capsule clearance at entry and exit, walkable slope at exit).
2. Montage plays with root motion and warping to the entry target.
3. **At the exit notify, the exit transform is revalidated against the *current* collision state** — capsule sweep/penetration test at the exit location and rotation, including dynamic actors that may have moved since detection.
4. If valid → snap and hand control back to CMC in the restored mode. If invalid → take the fallback path (drop to ground beneath, or reverse to the entry side), log `Traversal.ExitInvalid`, publish a diagnostic event, and never teleport into geometry.
5. All exits run the state-machine exit checklist (§3.2), and the traversal montage is stoppable on damage/death.

Test: `TDD-Functional.Movement.TraversalExitRevalidation` (M2) uses a blocker inserted between detection and exit and asserts the fallback path, plus a second variant that removes the floor to assert no floating.

### 3.8 Metrics harness (extended for latency stages and camera criteria)

Per-frame record (ring buffer + optional CSV):

```
Frame, TimeSeconds, DeltaSeconds, MaxFPSCap, VSyncState, PhysicsSubstepping,
State, PrevState, StateChangeReason, IntentMask,
FrameInjected, FrameIntentRecorded, FrameVelocityChanged, FramePoseUpdated,
InputDirection, VelocityX/Y/Z, Speed2D, Acceleration,
Yaw, YawRateDegPerSec, bGrounded, CapsuleZ, FloorSlopeDeg, Gait, Stance,
CamPosX/Y/Z, CamYaw, CamPitch, BoomLengthCm, CamObstructed, CamAcquisitionActive,
CamMinGeomDistanceCm, ActiveAnimProviderId,
[FootSlideCm]   // M2
```

Console commands:

| Command | Behaviour |
|---|---|
| `TDD.Movement.Overlay 0/1` | State, speed, yaw rate, grounded, gait, anim provider, boom length, obstruction flag |
| `TDD.Movement.Record start/stop` | CSV to `Saved/Profiling/Movement_<timestamp>.csv` |
| `TDD.Movement.Report` | Computes L1/L2/L3, M-02…M-04, step results, camera criteria 1–5, dodge distance, from the last recording, with pass/fail |
| `TDD.Camera.Report` | Camera-only summary (criteria 1–5) with the offending frame index for any violation |
| `TDD.Movement.Reset` | Return to spawn; clear buffers, measurements, event flags |
| `TDD.Input.Buffer` | Dump live buffer contents |
| `TDD.State.History` | Dump last 120 transitions with reason |
| `TDD.Movement.FrameCap <n>` | Sets `t.MaxFPS` for repeatable tests (60 default, 120 for latency cross-check) |

Instrumentation requirements: the harness must not itself change what it measures (AC-30 checks the on/off delta ≤ 0.05 ms); it must be a no-op in Shipping; and it must record the frame-rate cap and vsync state in the CSV header so a capture can never be quoted out of context.

---

## 4. Acceptance criteria — the single M1 gate (review item 1)

**This table is the authoritative M1 gate.** The assessment (§8) refers here; §9 of this document restates it as the definition of done. Nothing else defines "M1 complete".

Thirty-one criteria. Each names its metric, threshold, test and, where relevant, the manual procedure. Frame-rate-dependent tests run at `t.MaxFPS 60` and are cross-checked at 120.

| ID | Criterion | Threshold | Verified by |
|---|---|---|---|
| AC-01 | L1 sample→intent | ≤ 1 frame worst case; 0 in harness, at 60 and 120 FPS | `TDD-Functional.Movement.LatencyL1` (M-01a) |
| AC-02 | L2 intent→first velocity change | **0 frames** at 60 and 120 FPS | `TDD-Functional.Movement.LatencyL2` (M-01b) |
| AC-03 | L3 intent→pose reflection | ≤ 1 frame, measured value reported | `TDD-Functional.Movement.LatencyL3` (M-01c) |
| AC-04 | Acceleration to 95% max jog | ≤ 0.35 s, no overshoot > 1% | `...AcceleratesToMaxSpeed` (M-02) |
| AC-05 | Stop from max jog | ≤ 0.20 s and ≤ 50 cm | `...StopsWithinDistance` (M-03) |
| AC-06 | 180° turn at max jog | ≤ 0.50 s, yaw settles ±2°, no state flap | `...Turn180Degrees` (M-04) |
| AC-07 | Step-up 15/30/45 cm | Climbs; settle ≤ 0.25 s; ≤ 1 CMC correction; no Airborne | `...StepUpSupported` (M-06a) |
| AC-08 | Step-up 50 cm | **Blocked and stable**: net Z gain ≤ 1 cm over 5 attempts; speed ≤ 5 cm/s after contact within 0.2 s; no Airborne; no penetration; no oscillation > 1 cm | `...StepUpOverMaxBlocked` (M-06b) |
| AC-09 | Step-down 15/30/45/50 cm | ≤ 45 cm: no Airborne, smooth, settle ≤ 0.25 s. 50 cm: Airborne allowed, landing recovery ≤ 0.25 s, no fall-through | `...StepDownBehaviour` (M-06c) |
| AC-10 | Angled approach 30/45/60° | 45 cm step climbed at every angle; lateral deflection ≤ 10 cm; no jitter | `...StepAngledApproach` (M-06d) |
| AC-11 | Sprint over 45 cm step | Climbs; speed never < 60% max; no Airborne > 0.10 s | `...SprintOverStep` (M-06d) |
| AC-12 | Corner stability | Inside/outside corners at walk and sprint: no stick (≥ 90% target speed within 0.3 s of clearing), ≤ 2 yaw sign flips per 10 frames, no penetration | `...CornerStability` (M-06d) |
| AC-13 | Slopes | 40° traversable (≥ 4.5 m per 5 m), 50° blocked (≤ 0.5 m in 3 s), no Z jitter > 0.5 cm/frame | `...SlopeLimits` (M-07) |
| AC-14 | Camera penetration | Zero samples < 10 cm from blocking geometry, 60 s sweep, both corridors | `...CameraPenetration` (M-08a) |
| AC-15 | Camera angular jitter | Δ ≤ 6°/frame; jerk ≤ 3°/frame²; ≤ 3 sign changes per 10 frames | `...CameraAngularStability` (M-08b) |
| AC-16 | Camera displacement | ≤ 10 cm/frame normal; ≤ 25 cm/frame obstructed; never > 15 cm/frame unflagged | `...CameraDisplacement` (M-08c) |
| AC-17 | Camera obstruction recovery | ≤ 150 cm/s; monotonic; ≤ 0.6 s for obstructions < 90 cm | `...CameraRecovery` (M-08d) |
| AC-18 | Lock-on acquisition | Flagged event only: 0.20 s, ≤ 120° total, ≤ 600°/s peak, ≤ 0.35 s; excluded from jitter | `...CameraAcquisitionSlew` (M-08e) |
| AC-19 | Dodge distance and clearance | Mean within 5 cm of resolved distance, σ ≤ 5 cm over 100 runs; unit test proves radius is included once and not double-counted; margin only | `...DodgeDistanceRepeatable` (M-09a) + `TDD-Unit.Movement.DodgeSpecMath` |
| AC-20 | Dodge invulnerability | False at 0.09 s, true 0.11–0.44 s, false at 0.46 s (±1 frame) | `...DodgeIFrames` (M-09b) |
| AC-21 | Dodge into geometry | Start-penetrating → dodge refused (no montage, no cooldown consumed); blocked en route → clamped distance; capsule never penetrates per frame; movement mode restored | `...DodgeRespectsCollision` (M-09a) |
| AC-22 | State pair completeness | All 196 pairs: declared legal or refused with the state unchanged | `TDD-Unit.Movement.StateRulesComplete` |
| AC-23 | State semantics | Every state's preconditions, forced-in/out, interruption mask, exit checklist (on natural *and* forced exit), recovery condition and min dwell behave as specified | `TDD-Unit.Movement.StateSemantics` |
| AC-24 | Input buffering | Single consumption; exact expiry; replace-not-queue; clear-on-lock matrix | `TDD-Unit.Movement.InputBuffer` |
| AC-25 | Coyote time | Accepted at 0.11 s, rejected at 0.13 s after leaving ground | `TDD-Unit.Movement.CoyoteWindow` |
| AC-26 | Root-motion execution and restoration | Capsule actually displaced by root-motion action (verified, not assumed); prior mode restored after natural end, interruption, death and cinematic takeover | `TDD-Unit.Movement.RootMotionAppliesToCapsule`, `.RootMotionRestoresMovementMode` (M-13) |
| AC-27 | Device parity | Keyboard/mouse vs gamepad ≤ 1 frame difference | `...InputDeviceParity` (M-12) |
| AC-28 | Player frame cost | ≤ 0.30 ms on reference hardware (Development) | Insights capture (M-11) |
| AC-29 | No permanent input lock | Every reachable state exits within 2 s via its declared inputs; `Cinematic`/`Dead` exits tested as forced | `...NoPermanentInputLock` |
| AC-30 | Harness fidelity | Report reproduces automation numbers within 2%; instrumentation overhead ≤ 0.05 ms | Manual cross-check + capture (M-11) |
| AC-31 | Reproducibility | Three consecutive cold runs: identical pass results, metric values within tolerance | CI evidence |

Tolerances are declared in advance so results are judged, not negotiated.

---

## 5. Automated test specifications

| Test | Setup | Assertions |
|---|---|---|
| `TDD-Unit.Movement.StateRulesComplete` | Synthetic rules table | All 196 pairs: legal → transition occurs; illegal → refused **and** state unchanged; no pair silently permitted |
| `TDD-Unit.Movement.StateSemantics` | Synthetic rules table | Per state: preconditions reject when unsatisfied; forced transitions preempt regardless of dwell/priority; exit checklist items all executed (verified via recording stubs) on natural **and** forced exit; recovery condition ends the state at the declared time; min dwell blocks flap re-entry |
| `TDD-Unit.Movement.InputBuffer` | No world | Push/pop per intent; expiry at window ±1 ms; single consumption; replace-not-queue; clear-on-lock matrix |
| `TDD-Unit.Movement.CoyoteWindow` | No world | Accept 0.11 s, reject 0.13 s |
| `TDD-Unit.Movement.DodgeSpecMath` | No world | `ResolvedDistance` for 1000 random specs: never negative, never exceeds authored, never exceeds sweep availability; **asserts radius is counted exactly once** (a ray-based variant would subtract it, capsule-based must not); invulnerability range monotonic and inside the montage; behaviour at 0.25× and 2× time dilation |
| `TDD-Unit.Movement.TurnRateMonotonic` | No world | Yaw approaches target without overshoot, 1000 random pairs |
| `TDD-Unit.Movement.RootMotionRestoresMovementMode` | Mock action table | 100 random root-motion actions: mode before == mode after, including abort, death and cinematic-interrupt paths |
| `TDD-Unit.Movement.RootMotionAppliesToCapsule` | Minimal world, one montage with authored root motion | On the first build: capsule displacement > 0 and matches the authored root-motion distance within 5%. **This test exists because v1.0 assumed the mechanism worked** |
| `TDD-Functional.Movement.LatencyL1` | Flat zone, injector at frame boundary, 60 and 120 FPS | Assert `FrameIntentRecorded - FrameInjected == 0`; repeat with mid-frame injection and assert `== 1` |
| `TDD-Functional.Movement.LatencyL2` | Same | Assert `FrameVelocityChanged - FrameIntentRecorded == 0` at both frame rates; `Velocity` delta > 1 cm/s |
| `TDD-Functional.Movement.LatencyL3` | Same | Assert `FramePoseUpdated - FrameIntentRecorded <= 1`; **record the actual value** in the result line |
| `TDD-Functional.Movement.AcceleratesToMaxSpeed` | Flat zone, facing +X, 60 FPS | Speed ≥ 0.95·MaxJog within 0.35 s; overshoot ≤ 1%; CSV exported |
| `TDD-Functional.Movement.StopsWithinDistance` | From max jog | Speed 0 within 0.20 s; displacement ≤ 50 cm |
| `TDD-Functional.Movement.Turn180Degrees` | From max jog | abs(yaw − target) ≤ 2° within 0.50 s; state stays `Locomotion`; speed ≥ 60% max |
| `TDD-Functional.Movement.StepUpSupported` | 15, 30, 45 cm steps | Each climbs; settle ≤ 0.25 s; ≤ 1 correction; never enters `Airborne` |
| `TDD-Functional.Movement.StepUpOverMaxBlocked` | 50 cm step | Five 3 s approaches: net capsule Z gain ≤ 1 cm total; speed ≤ 5 cm/s after contact within 0.2 s; no `Airborne`; per-frame capsule penetration count == 0; Z oscillation ≤ 1 cm |
| `TDD-Functional.Movement.StepDownBehaviour` | 15/30/45/50 cm descents | ≤ 45 cm: never `Airborne`, Z monotonic decreasing, settles ≤ 0.25 s, final Z within 2 cm. 50 cm: `Airborne` entered, `Land` recovery ≤ 0.25 s, no fall-through, final Z within 2 cm |
| `TDD-Functional.Movement.StepAngledApproach` | 45 cm step approached at 30/45/60° | Climbs at each angle; lateral deflection from the intended heading ≤ 10 cm; no per-frame Z jitter > 0.5 cm |
| `TDD-Functional.Movement.SprintOverStep` | 15 m run-up at sprint into 45 cm | Climbs; speed never < 60% max through the step; `Airborne` duration ≤ 0.10 s; no penetration |
| `TDD-Functional.Movement.CornerStability` | Inside and outside 90° corners, walk and sprint | No stick: ≥ 90% of target speed within 0.3 s of clearing; yaw-rate sign flips ≤ 2 per 10 frames; zero penetration frames |
| `TDD-Functional.Movement.SlopeLimits` | 40° and 50° ramps | 40°: ≥ 4.5 m progress per 5 m travelled; 50°: ≤ 0.5 m in 3 s; Z jitter ≤ 0.5 cm/frame |
| `TDD-Functional.Movement.CameraPenetration` | Two corridors, scripted 60 s sweep | `CamMinGeomDistanceCm ≥ 10` every sample; boom ≥ 35 cm or close-up mode flag set |
| `TDD-Functional.Movement.CameraAngularStability` | Same capture, quiet-follow segment | Per-frame angular delta ≤ 6°; jerk ≤ 3°/frame²; ≤ 3 sign changes per 10-frame window; acquisitions excluded by flag |
| `TDD-Functional.Movement.CameraDisplacement` | Obstruction sequence: walk into a corner, back out | Normal segments ≤ 10 cm/frame; obstructed segments ≤ 25 cm/frame; no unflagged frame > 15 cm |
| `TDD-Functional.Movement.CameraRecovery` | Clear the obstruction | Re-extension rate ≤ 150 cm/s; boom length monotonic; completion ≤ 0.6 s for a 90 cm obstruction; zero overshoot frames |
| `TDD-Functional.Movement.CameraAcquisitionSlew` | Lock-on stub with a synthetic target | Acquisition flagged; blend 0.20 s ±1 frame; total slew ≤ 120°; peak ≤ 600°/s; completion ≤ 0.35 s; jitter metrics ignore flagged frames |
| `TDD-Functional.Movement.DodgeDistanceRepeatable` | Flat, 100 dodges | Mean within 5 cm of authored; σ ≤ 5 cm; final yaw rate ≈ 0 |
| `TDD-Functional.Movement.DodgeIFrames` | Flat | Tag false at 0.09 s, true at 0.11 s and 0.44 s, false at 0.46 s (±1 frame) |
| `TDD-Functional.Movement.DodgeRespectsCollision` | (a) 1 m from wall; (b) spawned overlapping geometry | (a) distance clamped to sweep result − 2 cm margin; zero penetration frames; mode restored. (b) dodge refused: state unchanged, no montage, cooldown not consumed, one logged refusal |
| `TDD-Functional.Movement.InputDeviceParity` | Flat, synthesised keyboard then gamepad | AC-04 timings differ ≤ 1 frame; no device-specific dead zone divergence |
| `TDD-Functional.Movement.NoPermanentInputLock` | All zones | Each state exits within 2 s via declared inputs; `Dead` and `Cinematic` exits forced by test and verified |
| `TDD-Functional.Movement.LockOnStubStateIsConsistent` | Flat, no targets | No crash, coherent state, camera returns to `Explore`, no acquisition events fired |
| `TDD-Functional.Movement.TraversalExitRevalidation` | M2 | Blocker inserted after detection → fallback path taken, no teleport into geometry, exit checklist ran, `Traversal.ExitInvalid` logged |

Result line format (unchanged): `TDD_RESULT <test> <PASS|FAIL> <metric>=<value> ...`, greppable and quotable without interpretation.

---

## 6. Manual procedures (P1–P6)

Every procedure records build ID, machine spec, frame rate, vsync state, input device and CSV reference. Numbers first, impressions second (impressions labelled as such).

**P1 — Responsiveness sweep (10 min).** Flat zone, overlay on, recording on, `t.MaxFPS 60`. Idle→jog→stop ×5; jog→sprint→release ×5; 180° reversal ×10; dodge ×10; ledge walk-off with a jump at 0.10 s (coyote) ×5. Expected: motion begins on the pressed frame; no dead zone; reversal does not slide; dodge does not clip. Record `TDD.Movement.Report`.

**P2 — Camera behaviour in tight interiors (10 min).** 1.2 m and 2.0 m corridors; slow and fast yaw sweeps; corner reverse; back to wall and pitch up; obstruction then clearing. Expected: no penetration; pull-in reads as a move (criterion 3), not a teleport; recovery is smooth and monotonic; acquisition (if a stub target is present) is flagged and bounded. Record `TDD.Camera.Report`; any single penetration fails the procedure.

**P3 — Steps, slopes, drops, edges (15 min).** Step rig at 15/30/45/50 cm; approach each at 0°, 30°, 45°, 60°; sprint into 45 cm; descend 15/30/45/50; 40° and 50° slopes; inside/outside corners; drops of 1/2/4 m; dodge into a step and into a wall. Expected: **45 cm climbs, 50 cm refuses cleanly** (no creep, no pop, no Airborne); descents ≤ 45 cm do not enter falling; corners do not stick; dodge clamps and never clips. Record any stuck state with `TDD.State.History`.

**P4 — Device parity and rebinding (10 min).** Repeat P1 steps 1–4 on keyboard/mouse and gamepad; rebind every action once and repeat. Expected: parity within a frame; rebinding takes effect without restarting; no action becomes unreachable.

**P5 — Long-session stability (20 min).** Twenty minutes of continuous movement, dodges, camera sweeps. Expected: no capsule-height drift, no movement-mode leak (overlay), flat memory, stable frame time.

**P6 — Latency and pose observation (10 min, new in v1.1).** Run the latency tests, then observe manually: is the *pose* update visibly behind the *motion*? Compare at 60 and 120 FPS. Expected: L3 numeric value matches what is seen (if L3 measures 0 and it looks late, the measurement is wrong and must be fixed before any tuning). Optionally, if the Creative Director wants device-to-photon figures, measure externally with a high-speed camera and report separately from L1–L3.

---

## 7. The controlled test environment (`L_TDD_Test_Movement`)

| Zone | Content | Measurement |
|---|---|---|
| `Z_Flat` | 100×100 m plane, 1 m grid, 5/10 m markers | Spawn, L1–L3, accel/stop/turn |
| `Z_Slope` | 30/40/50/60° ramps | Entry/exit volumes log displacement and time |
| `Z_Steps` | 15/30/45/50 cm steps, 3 m wide, **with approach wedges at 30/45/60°** | Capsule Z sampling per frame |
| `Z_StepDown` | Mirrored descent set at 15/30/45/50 cm | Z monotonicity, Airborne detection |
| `Z_SprintRun` | 15 m run-up to a 45 cm step and to a corner | Speed retention, Airborne duration |
| `Z_Corner` | Inside and outside 90° corners, 1.2 m and 2.0 m widths | Stick detection, yaw sign flips, penetration |
| `Z_Corridor1` | 1.2 m wide, 12 m long, 3 m high, closed | Camera sweep driver |
| `Z_Corridor2` | 2.0 m wide, 90° corner, doorway | Camera sweep + obstruction sequence |
| `Z_Drop` | 1/2/4 m platforms with 12 m landing | Landing speed, recovery |
| `Z_Dodge` | Flat 20 m run-up, plus a wall variant and an overlap variant | Distance, i-frames, clamp, refusal |
| `Z_SpawnPoints` | Named `PlayerStart` per zone | Automation entry points |

Grey materials, no art pass, excluded from Shipping cooks. It is a measuring instrument, not environment work, and it will not be presented as progress on the game's visuals.

---

## 8. Performance observation requirements

1. Player frame cost breakdown (Insights scopes: input, CMC, locomotion, camera, metrics) against AC-28.
2. Median and 1% low frame time over 120 s in `Z_Flat` and `Z_Corridor1`, with the recorder **on and off** — the delta must be ≤ 0.05 ms (AC-30).
3. Camera criteria overhead included in the above (the recorder samples per frame; it must not be the reason a threshold passes or fails).
4. Memory: `memreport -full` before/after P5, no growth attributable to my components.
5. CSV sizes recorded (a 20-minute capture must be practical to store and share).
6. Any hitch with its cause, or explicitly marked unattributed.

---

## 9. Definition of done (single gate)

- **All 31 acceptance criteria (§4) pass**, with quoted results, test names and capture references.
- Manual procedures **P1–P6** executed and recorded, including qualitative notes clearly labelled.
- Three consecutive cold runs identical (AC-31).
- No `Tick` without written justification; no gameplay literal outside data assets; no log spam in Shipping.
- Harness on in Development, absent in Shipping, and proven not to distort measurement beyond 0.05 ms.
- Interfaces (§10) published and unchanged since v1.1, or changed by ADR.
- Handoff report per the reporting protocol (assessment §9).
- Known limitations listed with named placeholder IDs.

**M1 is not complete because a human says it feels responsive.** It is complete when AC-01…AC-31 pass and the reviewer can rerun the numbers.

---

## 10. Interfaces exposed at M1 (frozen for Agent 2)

Unchanged in shape from v1.0; **the Core types they reference are proposals, not created code** (§Appendix A, review item 9).

```cpp
// TDDGameplay/Public/Combat/TDDCombatant.h — interface; implementation lands in M3
class TDDGAMEPLAY_API ITDDCombatant
{
public:
    virtual FGuid GetEntityId() const = 0;
    virtual bool  IsAlive() const = 0;
    virtual ETDDCombatState GetCombatState() const = 0;
    virtual bool  IsTelegraphingAttack() const = 0;         // M3
    virtual float GetAttackTelegraphRemaining() const = 0;  // M3, gameplay seconds
    virtual void  ApplyStagger(float DurationSeconds, FGameplayTag Source) = 0;
};

// Implemented in M1
UTDDCharacterStateMachine::GetState / IsInState / AllowsInput / RequestState / OnStateChanged
UTDDTargetLockComponent::GetLockedTarget / IsLockedOn     // stub in M1: always unlocked
FTDDPawnKinematics (value snapshot, no pointers)           // proposed Core struct
```

Contract stability: names and signatures frozen for M1–M3. Additions allowed; renames require an ADR before M3.

---

## 11. Known limitations and out-of-scope items at M1

| Item | State | Note |
|---|---|---|
| Animation quality | Placeholder mannequin, no clips | C-1 pending; M2 integrates real clips |
| Motion Matching | Not enabled; provider interface + blendspace implementation | ADR-0005; MM evaluated in M2 |
| Traversal execution | Not implemented (M2); only the exit-revalidation rule is fixed (§3.7) | AC for it lands in M2 |
| Interaction | Not implemented (M2) | — |
| Combat/weapon/enemies | Not implemented (M1–M6) | Contracts published only |
| Lock-on | Stub | Real acquisition in M3; camera acquisition criterion tested against a synthetic target |
| Stamina economy | Not implemented | Q-08 open; dodge cooldown only in M1 |
| Difficulty / accessibility UI | Not implemented | Q-10, Q-11 |
| Device-to-photon latency | Not measured | Out of engine scope; external method if required |
| Feel tuning | Engineering defaults | Requires CD feel pass; all values data |

---

## 12. Risks specific to M1 (updated)

| Risk | Mitigation |
|---|---|
| CMC defaults feel mushy and get "fixed" with hacks | Tuning table with rationale, all data-driven; measurement before opinion |
| Step/edge geometry produces undeclared states | 50 cm blocked, descent, angled, sprint and corner cases are first-class ACs (AC-08…AC-12) |
| Camera stabilised per-scene instead of systematically | Five criteria, two corridor widths, obstruction sequence, acquisition flag |
| Latency claims drift across frame rates | L1–L3 measured at 60 and 120 FPS, reported in frames and ms |
| Root motion assumed to work (the v1.0 error) | `RootMotionAppliesToCapsule` proves displacement on the first build; restoration tested through interruption/death/cinematic |
| Dodge clearance re-introduces radius double-counting | `DodgeSpecMath` asserts the radius is counted exactly once, for both capsule and hypothetical ray paths |
| Metrics harness distorts what it measures | On/off delta ≤ 0.05 ms (AC-30) |
| Mannequin mistaken for character progress | `PLACEHOLDER-A1-01`, stated in every report; no Adanna-specific tuning |
| Thresholds are wrong for this game | All **[A1]** thresholds are data and explicitly provisional pending first captures |

---

## Appendix A — Contract proposals for `TDDCore` (review item 9)

**Status: PROPOSED — pending Agent 3's Core review. Not created by Agent 1.**

These shapes are requested, not authored. `TDDCore` is Agent 3's module (MEAD §13.1); creating competing types there would violate MEAD §13.5 and split identity for `ETDDCombatState`, which is consumed by AI, UI and combat alike. If Agent 3 accepts a different shape, I adapt my code — I do not fork the type.

```cpp
// PROPOSAL — TDDCore/Public/Types/TDDCombatTypes.h
UENUM(BlueprintType)
enum class ETDDCombatState : uint8
{
    None, Approaching, Telegraphing, Attacking, Recovering, Blocking, Parrying,
    Dodging, Staggered, Grabbing, Dead
};

UENUM(BlueprintType)
enum class ETDDStance : uint8 { Exploration, Combat };

UENUM(BlueprintType)
enum class ETDDCancelReason : uint8
{
    Input, Damaged, Parried, Staggered, Cinematic, Death, Forced
};

// PROPOSAL — TDDCore/Public/Types/TDDPawnTypes.h
USTRUCT(BlueprintType)
struct FTDDPawnKinematics
{
    GENERATED_BODY()
    UPROPERTY() FGuid EntityId;
    UPROPERTY() FVector Velocity = FVector::ZeroVector;
    UPROPERTY() bool bGrounded = false;
    UPROPERTY() float Speed2D = 0.0f;
    UPROPERTY() ETDDStance Stance = ETDDStance::Exploration;
    UPROPERTY() float HeightAboveGround = 0.0f;
    UPROPERTY() ETDDCombatState CombatState = ETDDCombatState::None;
};
```

Rationale: both are consumed across module boundaries, so they belong in the leaf module to preserve ADR-0003's dependency direction. `FTDDPawnKinematics` intentionally contains no actor pointers, so a consumer cannot hold stale state.

**Change request log:** none yet. If Agent 3 requests changes, they will be recorded here with the date and the adapting commit.

---

## Appendix B — Naming for this milestone

| Kind | Names |
|---|---|
| Classes | `ATDDPlayerCharacter`, `ATDDPlayerController`, `UTDDCharacterMovementComponent`, `UTDDCharacterStateMachine`, `UTDDLocomotionComponent`, `UTDDBlendSpaceProvider`, `UTDDCameraRigComponent`, `ATDDPlayerCameraManager`, `UTDDMovementMetricsComponent`, `UTDDPlayerInputComponent` |
| Pure logic | `FTDDInputBuffer`, `FTDDDodgeSpec`, `FTDDLocomotionParams`, `FTDDStateRuleRow` |
| Data | `DA_MovementConfig`, `DA_CameraConfig`, `DT_StateRules`, `DA_InputConfig` |
| Maps | `L_TDD_Test_Movement` |
| Console | `TDD.Movement.*`, `TDD.Camera.*`, `TDD.State.*`, `TDD.Input.*` |
| Tests | `TDD-Unit.Movement.*`, `TDD-Functional.Movement.*` |
| Placeholders | `PLACEHOLDER-A1-01` (stock mannequin) |

---

## Appendix C — Questions for the Technical Director (v1.1)

1. Accept the **single gate** (AC-01…AC-31) as the M1 definition of done, replacing the earlier partial metric list?
2. Accept the latency decomposition with **L2 = 0 frames as a hard requirement** and L3 measured-but-unpredicted? Is a measured L3 of 1 frame acceptable if the foot-slide budget still holds, or is a mesh-tick change mandatory?
3. Confirm the camera thresholds (10 cm / 6° per frame / 3°/frame² / 10–25–15 cm per frame / 150 cm/s / 0.20 s acquisition) are suitable as first-pass values to be tuned against real captures.
4. Confirm the **50 cm step is intended to be impassable** at `MaxStepHeight = 45 cm`, and that entering `Airborne` on a 50 cm *descent* is acceptable.
5. Confirm the dodge `SafetyMargin` of 2 cm and the refusal behaviour when starting inside geometry.
6. Confirm the root-motion execution model in ADR-0013 v1.1 (CMC keeps a mode in which its movement update runs) and that the mechanism is provisional until `RootMotionAppliesToCapsule` passes.
7. Confirm attack warp limits remain **configurable** (300 cm / 60° defaults) with a per-attack override.
8. Confirm `t.MaxFPS`-capped functional tests (60, cross-checked at 120) as the canonical responsiveness numbers.
9. Confirm test content under `Content/TDD/Test/` is excluded from Shipping cooks.
10. Approve the proposed `TDDCore` types in Appendix A, or specify replacements (Agent 1 will not create them).

---

## 13. Change log — v1.0 → v1.1 (response to Technical Director review, 2026-11-16)

v1.0 is preserved unchanged at `archive/M1_MOVEMENT_SPECIFICATION_V1.0.md`. Acceptance criteria were renumbered as part of this revision; the mapping is given below so an earlier review comment can still be traced.

| ID | Review item | What was wrong in v1.0 | Correction in v1.1 | Section |
|---|---|---|---|---|
| **C-01** | 1 — Reconcile exit criteria | Assessment §8 and spec §4/§9 described slightly different gates (partial metric list, P1–P3 vs P1–P5) | One gate: **AC-01…AC-31**, declared authoritative here, referenced by the assessment, restated in §9; manual procedures P1–P6 in both documents | §4, §9 |
| **C-02** | 2 — Latency stages | One "input latency" metric conflating sampling, acceptance and pose update; v1.0 asserted a one-frame animation lag as fact while requiring a same-frame velocity delta | Three stages with frame-index definitions: **L1 ≤ 1** (0 in harness), **L2 = 0** (hard requirement), **L3 ≤ 1 and measured, not predicted**; measured at 60 and 120 FPS; reported in frames and ms; device-to-photon explicitly out of scope | §3.4, AC-01…03 |
| **C-03** | 3 — Dodge clearance | `Clearance − CapsuleRadius − Margin` deducted the radius from a shape that already contained it, with undefined units | Capsule sweep with the CMC's exact dimensions; **radius counted once** (inside the shape), margin 2 cm only; explicit channel, ignored actors, planar Z handling, start-penetration refusal, CMC as final collision authority; unit test asserts the radius is not double-counted | §3.5, AC-19/21 |
| **C-04** | 4 — Camera criteria | Single 720°/s rule used as a jitter threshold; penetration/jitter/pop/recovery/acquisition conflated | Five criteria with separate thresholds and event exemptions: penetration 10 cm; angular 6°/frame + 3°/frame² + sign-flip limit; displacement 10/25/15 cm per frame; recovery 150 cm/s monotonic ≤ 0.6 s; acquisition whitelisted (0.20 s, ≤ 120°, ≤ 600°/s) | §3.6, AC-14…18 |
| **C-05** | 7 — Camera ownership | Camera manager and rig described as one unit on the pawn | Camera manager is PC-owned (shakes/modifiers must go through it); rig component is pawn-owned and computes desired rig only; spring arm on pawn; Sequencer takeover suspends rig writes | §3.6 |
| **C-06** | 7 — Input ownership | Ambiguous: controller "routes input" while the Enhanced Input subclass sat on the pawn, with no lifecycle explanation | Documented possession flow (`PawnClientRestart → SetupPlayerInputComponent`), `InputComponentClass` usage, pawn-owned gameplay bindings, controller-owned pause/menu component, contexts pushed/popped on possess/unpossess | §3.1 |
| **C-07** | 5 — State transitions | A 14×14 allowed matrix plus column notes; no preconditions, forced transitions, interruption windows, exit actions or recovery conditions | Two per-state tables (entry/exit/recovery/dwell; forced/interruption/buffer) plus global rules: priority order, forced vs requested, exit checklist on every exit including aborts, buffer policy, min dwell; two unit tests | §3.2, AC-22/23 |
| **C-08** | 6 — Step 50 cm and edge cases | 50 cm step listed with no expected outcome; no descent, angled, sprint or corner coverage | 50 cm defined as **blocked and stable** (net Z ≤ 1 cm over 5 attempts, no Airborne, no penetration); added descent (45 vs 50), angled 30/45/60°, sprint-over-step, corner stability, and dodge-into-step tests | §4, §5 |
| **C-09** | 8 — Root motion | `MOVE_None` assumed to preserve CMC root-motion processing; exit transform snapped without revalidation; warp limits fixed | v1.1: no `MOVE_None` assumption; CMC keeps a mode in which its movement update runs and performs collision; `RootMotionAppliesToCapsule` proves displacement on first build; exit transform revalidated at the exit notify with a defined fallback; warp limits configurable per attack | §3.5, §3.7, ADR-0013 v1.1, AC-26 |
| **C-10** | 9 — Core types | Appendix A read as an instruction to create `TDDCore` types | Restated as **PROPOSED, pending Agent 3 review**, with an explicit statement that Agent 1 creates no Core types and adapts rather than forks | Appendix A |
| **C-11** | 6 — Metric/test consistency | Test names and metric IDs diverged from the assessment | Test suite expanded to 34 named tests (§5); metric IDs made suffixes of the same families (M-01a–c, M-06a–d, M-08a–e, M-09a/b) and mirrored in the assessment | §5, §8 |
| **C-12** | Review header | No versioning, no preserved original | Versioned to v1.1; v1.0 archived unchanged; change log in this section, in the assessment (§11) and in ADR-0013 | this section |

### AC renumbering map (v1.0 → v1.1)

| v1.0 | v1.1 |
|---|---|
| AC-01 input latency | AC-01 (L1), AC-02 (L2), AC-03 (L3) |
| AC-02 acceleration | AC-04 |
| AC-03 stop | AC-05 |
| AC-04 turn | AC-06 |
| AC-05 step-up 45 | AC-07 |
| — | AC-08 step 50 blocked, AC-09 descent, AC-10 angled, AC-11 sprint, AC-12 corner |
| AC-06 slopes | AC-13 |
| AC-07 camera penetration | AC-14 |
| AC-08 camera jitter | AC-15, AC-16, AC-17, AC-18 |
| AC-09 dodge distance | AC-19 |
| AC-10 dodge i-frames | AC-20 |
| AC-11 dodge collision | AC-21 |
| AC-12 state matrix | AC-22 |
| — | AC-23 state semantics |
| AC-13 buffering | AC-24 |
| AC-14 coyote | AC-25 |
| AC-15 root motion | AC-26 |
| AC-16 device parity | AC-27 |
| AC-17 frame cost | AC-28 |
| AC-18 no input lock | AC-29 |
| AC-19 harness fidelity | AC-30 |
| AC-20 reproducibility | AC-31 |

### Status after revision

**No implementation has begun; nothing is compiled, executed or measured.** This document remains `DESIGN_ONLY`, and M1 implementation remains `BLOCKED` on Agent 3 prerequisites B-1…B-6. The revision is specification work only.
