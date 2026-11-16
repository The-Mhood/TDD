# MILESTONE 1 — IMPLEMENTATION SPECIFICATION
## Responsive, testable third-person character controller

**Project:** THE DISOBEDIENT DAUGHTER
**Agent:** 1 — Gameplay, Character and Combat Engineering
**Document:** TDD-A1-M1-SPEC-001
**Version:** 1.0 — for Technical Director review
**Date:** 2026-11-16
**Status:** `DESIGN_ONLY` — nothing in this document is implemented or verified
**Parent:** `GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` (TDD-A1-ASSESS-001)
**Governing:** TDD-MEAD-001 §4, §8, §13, §14, §15; ADR-0002, ADR-0005, ADR-0012, ADR-0013 (proposed)

---

## 1. Objective

Deliver a third-person character controller that is **responsive by measurement**, **correct under specific physics conditions**, and **testable without a human watching it**, in a controlled test environment, before any combat work begins.

M1 is complete when a build exists in which:

1. Movement responsiveness meets the thresholds in §4, measured by the in-build harness and asserted by automation.
2. The camera cannot penetrate geometry, cannot jitter, and blends within specified durations in five named situations.
3. The player state machine's transition table is exhaustively covered by tests — there are no undeclared transitions and no state that can silently lock input.
4. A dedicated test map reproduces flat ground, slopes at 30/40/50/60°, steps at 15/30/45/50 cm, a 1.2 m corridor, a 2.0 m corridor, and 1/2/4 m drops, each with measurement gates.
5. Every metric is exported as CSV and summarised by a console command that a reviewer can run themselves.

**Not in M1:** combat, damage, enemies, weapon, traversal (M2), interaction (M2), animation content integration beyond a stock mannequin.

---

## 2. Scope and deliverables

### 2.1 Code deliverables (to be written once B-1…B-6 exist)

| File | Purpose |
|---|---|
| `Source/TDDGameplay/Public/Player/TDDPlayerCharacter.h` / `.cpp` | `ATDDPlayerCharacter` — component host, capsule, mesh, input wiring |
| `Source/TDDGameplay/Public/Player/TDDPlayerController.h` / `.cpp` | `ATDDPlayerController` — input routing, camera manager, UI bridge |
| `Source/TDDGameplay/Public/Player/TDDPlayerInputComponent.h` / `.cpp` | Intent production, buffering, mapping-context switching |
| `Source/TDDGameplay/Public/Player/TDDCharacterStateMachine.h` / `.cpp` | State authority, transition table evaluation |
| `Source/TDDGameplay/Public/Movement/TDDLocomotionComponent.h` / `.cpp` | Gait/stance resolution, CMC parameter application, anim provider driving |
| `Source/TDDGameplay/Public/Movement/TDDLocomotionAnimProvider.h` / `.cpp` | Interface + `UTDDBlendSpaceProvider` (M1), MM provider stub declaring `NOT_IMPLEMENTED` |
| `Source/TDDGameplay/Public/Movement/TDDMovementConfig.h` | `UTDDMovementConfig` data asset |
| `Source/TDDGameplay/Public/Movement/TDDStateRules.h` | `FTDDStateRuleRow`, `UTDDStateRulesTable` wrapper |
| `Source/TDDGameplay/Public/Movement/TDDInputBuffer.h` | Pure-logic buffer (unit-testable, no world) |
| `Source/TDDGameplay/Public/Movement/TDDDodgeSpec.h` | `FTDDDodgeSpec` + pure distance/window maths |
| `Source/TDDGameplay/Public/Camera/TDDPlayerCameraManager.h` / `.cpp` | Camera shakes, FOV/post blending |
| `Source/TDDGameplay/Public/Camera/TDDCameraRigComponent.h` / `.cpp` | Rig blending, boom collision, lock-on framing (lock-on stub in M1) |
| `Source/TDDGameplay/Private/Movement/TDDMovementMetricsComponent.h` / `.cpp` | Instrumentation, CSV export, console commands |
| `Source/TDDGameplay/Private/Tests/TDDMovementUnitTests.cpp` | `TDD-Unit.Movement.*` |
| `Source/TDDTests/Private/Movement/TDDMovementFunctionalTests.cpp` | `TDD-Functional.Movement.*` |

Every file carries the owning-agent comment required by CODING_STANDARDS §8.

### 2.2 Content deliverables

| Asset | Purpose |
|---|---|
| `Content/TDD/Test/L_TDD_Test_Movement` | The controlled test environment (§7) |
| `Content/TDD/Data/Movement/DA_MovementConfig` | Tuning data |
| `Content/TDD/Data/Movement/DT_StateRules` | Transition table |
| `Content/TDD/Data/Movement/DA_CameraConfig` | Camera tuning |
| `Content/TDD/Input/DA_InputConfig` + `IMC_Exploration`, `IMC_Menu` | Input (co-owned with Agent 3's B-4) |
| `Content/TDD/Test/WBP_TDDMovementOverlay` | On-screen metrics overlay (dev) |

Test content lives under `Content/TDD/Test/` precisely so it cannot be mistaken for shipping content and so the cook validator can exclude it from Shipping.

### 2.3 Foundation deliverables (Agent 3)

B-1…B-6 from the assessment §3.1, including the `TDDCore` contracts in Appendix A. **M1 cannot start without them.** I will not create a parallel `TDDCore` or a second input setup.

---

## 3. Class specifications

### 3.1 `ATDDPlayerCharacter`

| Aspect | Specification |
|---|---|
| Base | `ACharacter` |
| Capsule | Half-height 88 cm, radius 34 cm (parameterised in `DA_MovementConfig`; **not** derived from the mannequin's visual height, which will change when Adanna's mesh arrives) |
| Movement component | `UTDDCharacterMovementComponent` (thin `UCharacterMovementComponent` subclass, placed in `TDDGameplay/Public/Movement/`, added to this spec as required for step/slope overrides) |
| Components owned | state machine, locomotion, combat (declared, inert in M1), weapon (inert), interaction (inert), traversal (inert), audio hooks, metrics |
| Tick | `PrimaryActorTick` **disabled**; components tick with justification per CODING_STANDARDS §3. Metrics ticks only when enabled |
| Mesh | Stock mannequin (`SKM_Manny`/`SKM_Quinn` from the engine) in M1, explicitly labelled `PLACEHOLDER-A1-01`. No custom skeleton, no retarget, no attempt to represent Adanna |
| Camera | Spring arm + camera on `ATDDPlayerCharacter`, driven by `UTDDCameraRigComponent`; `ATDDPlayerCameraManager` selected by `ATDDPlayerController` |
| Movement modes | Walking by default; `MOVE_None` only during root-motion actions (dodge in M1); explicit restore with test M-13 |

**Explicit non-goal:** no attempt to make the mannequin look like Adanna. Character visual work requires the approved reference turned into an asset, which does not exist. A mannequin labelled as a placeholder is honest; a slapdash stand-in that people start calling "Adanna" is not.

### 3.2 `UTDDCharacterStateMachine`

Public API (published to Agent 2):

```cpp
UENUM(BlueprintType)
enum class ETDDPlayerState : uint8
{
    Idle, Locomotion, Sprint, Airborne, Land, Dodge,
    Attack, Block, Parry, Stagger, Traversal, Interaction, Cinematic, Dead
};

DECLARE_MULTICAST_DELEGATE_TwoParams(FOnTDDPlayerStateChanged, ETDDPlayerState /*Old*/, ETDDPlayerState /*New*/);

class TDDGAMEPLAY_API UTDDCharacterStateMachine : public UPawnComponent
{
public:
    ETDDPlayerState GetState() const;
    bool  IsInState(ETDDPlayerState State) const;
    bool  AllowsInput(ETDDIntent Intent) const;
    bool  RequestState(ETDDPlayerState NewState, ETDDStateChangeReason Reason);  // single entry point
    FOnTDDPlayerStateChanged OnStateChanged;
};
```

Rules:
- **`RequestState` is the only way the state changes.** Components request; the machine decides; the machine broadcasts. No component writes state directly, ever.
- Decision inputs: target state's row in `DT_StateRules` (allowed transitions), current state's `AcceptedInputs`/locks, whether the caller's precondition passes (e.g. dodge requires grounded + stamina in M3+), and forced transitions (death, cinematic, stagger) which are declared `bForced` and cannot be refused.
- Diagnostic: every refused transition logs at `Verbose` with the pair and reason; `TDD.State.History` console command dumps the last 120 transitions with timestamps. Debugging "why did it do that" needs a record, not a guess.
- Cooldown guard: a per-pair minimum dwell time (data) prevents 1-frame state flapping; asserted by unit test.

### 3.3 `UTDDLocomotionComponent`

| Responsibility | Detail |
|---|---|
| Gait resolution | Input magnitude + sprint state + stance (exploration/combat) → target gait `ETDDGait { Idle, Walk, Jog, Sprint }` and `ETDDStance { Exploration, Combat }` |
| CMC application | Sets `MaxWalkSpeed`, `MaxAcceleration`, `BrakingDecelerationWalking`, `GroundFriction`, `RotationRate` from `DA_MovementConfig` by gait — the component is the only writer of these values |
| Animation provider | Computes `FTDDLocomotionParams { Speed, LocalVelocityYaw, Gait, Stance, bGrounded, TurnRate, Acceleration }` and drives the active `ITDDLocomotionAnimProvider` |
| Camera-relative movement | Converts input to a world direction relative to the camera yaw; when locked on, converts to strafe/orbit mode with facing held toward the target |
| Rotation | `bOrientRotationToMovement` in exploration; `bUseControllerRotationYaw` with clamped yaw offset in combat/lock-on; turn rate per gait |
| Airborne | Air control multiplier, no rotation change while airborne unless data allows |

Gait table (M1 defaults, all in `DA_MovementConfig`, all tunable):

| Gait | Max speed (cm/s) | Max accel (cm/s²) | Braking decel | Rotation rate (°/s) | Turn-in-place threshold (°) |
|---|---|---|---|---|---|
| Idle | 0 | 2048 | 2400 | 600 | — |
| Walk | 220 | 1600 | 2000 | 600 | 60 |
| Jog | 480 | 2048 | 2400 | 540 | 45 |
| Sprint | 700 | 2400 | 1600 | 420 | 30 |

Justification for the defaults: Jog 480 cm/s gives a believable adult jog with the 1 m grid blockout scale (a 2.7 m doorway crossed in ~0.6 s); sprint 700 cm/s is a controlled run, not a superhero sprint, because a 25-year-old warrior with a blade on her hip at a God-of-War-like pace should read as athletic rather than arcade. Turn rates are set so that a 180° reversal at jog takes ≈0.33 s of rotation plus acceleration — inside the 0.50 s **[MEAD]** threshold with margin. These numbers are **engineering defaults pending the Creative Director's feel pass**, and they live in data so that pass is a data edit, not a code change.

### 3.4 `UTDDPlayerInputComponent` and `FTDDInputBuffer`

Intent enum (produced, not consumed, by input): `Move2D, Look2D, Sprint, Jump, Dodge, LightAttack, HeavyAttack, Block, Parry, LockOn, Interact, TraversalConfirm, Pause`.

Buffering rules (pure logic in `FTDDInputBuffer`, no world dependency, fully unit-tested):

| Intent | Buffer window | Consumed by | Cleared by |
|---|---|---|---|
| `Dodge` | 0.20 s | State machine on landing / attack cancel / recovery end | Expiry, `Stagger`, `Dead`, `Cinematic` |
| `Jump` | 0.15 s | State machine on grounding | Expiry, `Dead` |
| `LightAttack` | 0.20 s | `UTDDCombatComponent` (M3) | Expiry, `Stagger`, `Dead` |
| `HeavyAttack` | 0.20 s | `UTDDCombatComponent` (M3) | Expiry, `Stagger`, `Dead` |
| `Parry` | 0.15 s (window) | `UTDDCombatComponent` (M3) | Expiry |
| `Block` | held + 0.10 s release grace | State machine | Release beyond grace |
| `Interact` | not buffered | `UTDDInteractionComponent` (M2) | — |
| `LockOn`, `Pause` | immediate | Direct | — |

Coyote time: 0.12 s after leaving ground, `Jump` still accepted. Jump "queue then consume on land" is *not* implemented by default (it fights deliberate landing recovery); it is a data flag for the CD's feel pass.

Rules:
- One buffer entry per intent kind; a newer press replaces an older unexpired one (no queue of five dodges).
- Consumption is explicit (`Consume(Intent)` returns bool and removes the entry) so a buffered dodge cannot fire twice.
- Buffer state is dumped by `TDD.Input.Buffer`.

### 3.5 Dodge (M1 implementation)

`FTDDDodgeSpec` (data): `Distance` (cm), `Duration` (s), `InvulnStart` (s), `InvulnEnd` (s), `Cooldown` (s), `bRootMotion`, `MaxZeroGrounds`.

Defaults: distance 320 cm, duration 0.55 s, invulnerability 0.10–0.45 s, cooldown 0.35 s, root motion on.

Pure maths (unit-tested, no world):

```
ClampDistance(Authored, CapsuleRadius, ForwardSweepClearance) =
    min(Authored, ForwardSweepClearance - CapsuleRadius - SafetyMargin)   // >= 0
InvulnMontageRange(Spec, MontageLength) =
    [ InvulnStart / Duration * MontageLength , InvulnEnd / Duration * MontageLength ]
```

- Invulnerability windows are expressed in **gameplay seconds** and converted to montage positions at play time, so hitstop/slow-motion cannot desynchronise them (MEAD §3.3).
- The dodge direction comes from the movement input (fallback: facing) and is latched at the moment the dodge is accepted — mid-dodge input cannot steer it.
- Collision: forward sweep before the montage plays. If blocked earlier than the authored distance, the root-motion distance is clamped and a shorter clip variant may be selected (data: `FallbackMontage`). A dodge into a wall never clips and never leaves the capsule inside geometry.
- Root motion on: CMC set to `MOVE_None` for the montage duration, restored on `Land`/end with M-13 asserting restoration.
- M1 exposes invulnerability as a status tag only (`Status.Invulnerable`); the damage consequence arrives in M3, the tag boundary is measured in M1 (M-10).

### 3.6 Camera

`UTDDCameraRigComponent` on the character owns rig state; `ATDDPlayerCameraManager` owns shakes/FOV.

| Rig | Arm length | Socket offset | FOV | Blend in |
|---|---|---|---|---|
| `Explore` | 320 cm | (0, 45, 65) | 90° | 0.25 s |
| `CombatSoft` | 380 cm | (0, 55, 60) | 95° | 0.30 s |
| `LockOn` | 400 cm | (0, 60, 55) + target bias | 95° | 0.20 s |
| `Traversal` | 360 cm | (0, 30, 90) | 90° | 0.25 s |
| `Cinematic` | Sequencer | — | per shot | 0.40 s |

Correctness requirements (automated): boom sphere sweep radius 12 cm; camera-to-geometry distance ≥ 10 cm at all times in the corridor tests; no single-frame rotation delta > 720°/s except explicit lock-on acquisition; pitch clamp [-60°, +45°] explore / [-50°, +35°] combat; shoulder swap (left/right) supported by input and reflected in socket offset sign.

M1 lock-on is a **stub**: `UTDDTargetLockComponent` exists with the published API, selects nothing (no targets exist), and `TDD-Functional.Movement.LockOnStubStateIsConsistent` asserts the unlocked path is coherent. Real acquisition lands in M3 when enemies exist.

### 3.7 `UTDDMovementMetricsComponent` (instrumentation — a first-class deliverable)

This is what makes "responsive" a number rather than an argument.

Recording (per frame, ring buffer + optional CSV):

```
Frame, TimeSeconds, DeltaSeconds, FrameRateCap,
State, PrevState, IntentMask,
InputDirection, VelocityX/Y/Z, Speed2D, Acceleration,
Yaw, YawRateDegPerSec, bGrounded, CapsuleZ, FloorSlopeDeg,
Gait, Stance, CameraDistanceToGeometryCm,
[AnimationProviderId, FootSlideCm]   // M2
```

Console commands:

| Command | Behaviour |
|---|---|
| `TDD.Movement.Overlay 0/1` | On-screen readout: state, speed, yaw rate, grounded, gait, active anim provider |
| `TDD.Movement.Record start/stop` | CSV to `Saved/Profiling/Movement_<timestamp>.csv` |
| `TDD.Movement.Report` | Prints M-01…M-04, M-06, M-09, M-10 computed from the last recording, with pass/fail against thresholds |
| `TDD.Movement.Reset` | Returns to spawn, clears buffers and metrics |
| `TDD.Input.Buffer` | Dumps live buffer contents |
| `TDD.State.History` | Dumps last 120 transitions |
| `TDD.Movement.FrameCap <n>` | Sets `t.MaxFPS` for repeatable tests (default 60 in automation) |

The report command exists so a reviewer (or the Technical Director) can reproduce a claim in ten seconds instead of trusting a paragraph.

---

## 4. Acceptance criteria

Each criterion names its metric, threshold, verification method and test. **All must pass for M1 to be reported complete.** Frame-rate-dependent tests run at `t.MaxFPS 60`; latency test additionally at 120 to prove no hidden frame assumptions.

| ID | Criterion | Threshold | Verified by |
|---|---|---|---|
| AC-01 | Input reaches the movement system without added delay | Intent accepted on the same frame the input arrives (exactly 1 frame from device sample to velocity delta) | `TDD-Functional.Movement.InputLatencyOneFrame` (M-01) |
| AC-02 | Acceleration to max jog speed | ≥ 95% of max within **0.35 s** | `TDD-Functional.Movement.AcceleratesToMaxSpeed` (M-02) |
| AC-03 | Stop from max jog | Speed 0 within **0.20 s**, displacement ≤ **50 cm** | `TDD-Functional.Movement.StopsWithinDistance` (M-03) |
| AC-04 | 180° turn at max jog | Completed in ≤ **0.50 s**, no state flap, yaw settles ±2° | `TDD-Functional.Movement.Turn180Degrees` (M-04) |
| AC-05 | Step-up | 45 cm step traversed at walk speed; capsule settles within 0.25 s; no post-settle oscillation | `TDD-Functional.Movement.StepUp45cm` (M-06) |
| AC-06 | Slopes | 40° walkable (≥ 4.5 m progress in 5 m), 50° blocked (≤ 0.5 m progress in 3 s) | `TDD-Functional.Movement.SlopeLimits` (M-07) |
| AC-07 | Camera wall penetration | Zero samples closer than **10 cm** in a 60 s scripted sweep in the 1.2 m corridor | `TDD-Functional.Movement.CameraNoWallPenetration` (M-08) |
| AC-08 | Camera jitter | No frame-to-frame camera angular delta > 720°/s without an explicit acquisition event | Same test, additional assertion |
| AC-09 | Dodge distance repeatability | Mean within **5 cm** of authored, σ ≤ **5 cm** over 100 runs | `TDD-Functional.Movement.DodgeDistanceRepeatable` (M-09) |
| AC-10 | Dodge invulnerability window | `Status.Invulnerable` false at 0.09 s, true 0.11–0.44 s, false at 0.46 s (±1 frame) | `TDD-Functional.Movement.DodgeIFrames` (M-10) |
| AC-11 | Dodge into geometry | No capsule penetration; distance clamped; no movement-mode leak | `TDD-Functional.Movement.DodgeRespectsCollision` |
| AC-12 | State machine completeness | Every state pair is either declared legal or asserted illegal; no illegal transition reproduced | `TDD-Unit.Movement.StateRulesComplete` |
| AC-13 | Input buffering | Buffered intent consumed exactly once; expires correctly; cleared by `Stagger`/`Dead`/`Cinematic` | `TDD-Unit.Movement.InputBuffer` |
| AC-14 | Coyote time | `Jump` accepted up to **0.12 s** after leaving ground, rejected after | `TDD-Unit.Movement.CoyoteWindow` + functional |
| AC-15 | Root-motion hygiene | Prior movement mode restored after every root-motion action, 100% of runs | `TDD-Unit.Movement.RootMotionRestoresMovementMode` (M-13) |
| AC-16 | Device parity | Keyboard/mouse and gamepad produce action timings within 1 frame | `TDD-Functional.Movement.InputDeviceParity` (M-12) |
| AC-17 | Player frame cost | ≤ **0.30 ms** on reference hardware, Development build, in the movement test map | Insights capture, quoted in report (M-11) |
| AC-18 | No input lock | No state reachable from gameplay that permanently ignores input except `Cinematic` and `Dead`, both of which have a tested exit | `TDD-Functional.Movement.NoPermanentInputLock` |
| AC-19 | Metrics harness fidelity | `TDD.Movement.Report` reproduces the automation numbers within 2% on the same run | Manual cross-check recorded in report |
| AC-20 | Reproducibility | Three consecutive cold runs of the functional suite produce identical pass results and metric values within tolerance | CI evidence |

Tolerances are declared up front so a result can be judged rather than negotiated after the fact.

---

## 5. Automated test specifications (assertions in detail)

| Test | Setup | Assertions |
|---|---|---|
| `TDD-Unit.Movement.StateRulesComplete` | Synthetic `DT_StateRules` (test data, not content) | For all 14×14 state pairs: either a row declares it legal, or `RequestState` returns false **and** the state is unchanged; no pair is silently permitted |
| `TDD-Unit.Movement.InputBuffer` | No world | Push/pop per intent; expiry at exact window ±1 ms; single consumption; replace-not-queue; clear-on-lock matrix |
| `TDD-Unit.Movement.DodgeSpecMath` | No world | `ClampDistance` never negative, never exceeds clearance; invuln range monotonic and inside [0, MontageLength] for 1000 random specs; behaviour under time dilation 0.25× and 2× |
| `TDD-Unit.Movement.CoyoteWindow` | No world | Accept at 0.11 s, reject at 0.13 s |
| `TDD-Unit.Movement.RootMotionRestoresMovementMode` | Mock action table | 100 random root-motion actions: mode before == mode after; abort mid-action also restores |
| `TDD-Unit.Movement.TurnRateMonotonic` | No world | Yaw approaches target without overshoot for 1000 random rate/target pairs |
| `TDD-Functional.Movement.AcceleratesToMaxSpeed` | Flat zone, spawn (0,0,0), facing +X, `t.MaxFPS 60` | Inject `Move(1,0)` at frame 0; record speed per frame; assert speed ≥ 0.95·MaxJog at t ≤ 0.35 s; assert no overshoot > 1% of max; export CSV |
| `TDD-Functional.Movement.StopsWithinDistance` | From max jog | Release input; assert speed == 0 within 0.20 s; assert displacement ≤ 50 cm |
| `TDD-Functional.Movement.Turn180Degrees` | From max jog | Inject `Move(-1,0)`; assert |yaw − target| ≤ 2° within 0.50 s; assert state never leaves `Locomotion`; assert speed ≥ 60% max throughout (no full stop) |
| `TDD-Functional.Movement.StepUp45cm` | Step rig, 45 cm | Walk forward at 220 cm/s; assert capsule Z increases by 45 ± 2 cm; assert settles (|ΔZ| < 0.1 cm/frame) within 0.25 s; assert ≤ 1 CMC correction logged |
| `TDD-Functional.Movement.SlopeLimits` | Slope rig 40° and 50° | 40°: displacement along slope ≥ 4.5 m in 5 m of travel; 50°: ≤ 0.5 m progress in 3 s; assert no per-frame Z jitter > 0.5 cm |
| `TDD-Functional.Movement.CameraNoWallPenetration` | 1.2 m corridor, cameras swept | Scripted 60 s sweep of yaw 360°, pitch −20…+30; assert camera-to-wall ≥ 10 cm every sample; assert no angular delta > 720°/s without acquisition flag |
| `TDD-Functional.Movement.DodgeDistanceRepeatable` | Flat zone, 100 dodges | Assert mean within 5 cm of authored distance; σ ≤ 5 cm; assert final `YawRate` ≈ 0 |
| `TDD-Functional.Movement.DodgeIFrames` | Flat zone | Read `Status.Invulnerable` per frame; assert false at 0.09 s, true at 0.11 s and 0.44 s, false at 0.46 s (tolerance ±1 frame) |
| `TDD-Functional.Movement.DodgeRespectsCollision` | 1 m from wall | Dodge toward wall; assert capsule never penetrates (trace check per frame); assert distance ≤ clearance; assert movement mode restored |
| `TDD-Functional.Movement.InputLatencyOneFrame` | Flat zone, 60 and 120 fps runs | Record injection frame; assert first frame with nonzero velocity delta is exactly injection + 1 |
| `TDD-Functional.Movement.InputDeviceParity` | Flat zone | Run AC-02 with synthesised keyboard input and with synthesised gamepad input; assert timing difference ≤ 1 frame |
| `TDD-Functional.Movement.NoPermanentInputLock` | All test zones | For each reachable state, attempt exit via its declared inputs; assert exit within 2 s; `Cinematic`/`Dead` exits forced by test |
| `TDD-Functional.Movement.LockOnStubStateIsConsistent` | Flat zone | Toggle lock-on with no valid targets; assert state remains coherent, no null deref, camera returns to `Explore` rig |

Test harness rules: every functional test spawns into a clean sublevel state, sets `t.MaxFPS`, disables the metrics overlay, and writes a result line `TDD_RESULT <test> <PASS|FAIL> <metric>=<value>`. Results are greppable by CI and quotable in reports without interpretation.

---

## 6. Manual test procedures (reproducible)

Each procedure records: build ID, machine spec, frame rate, input device, and the CSV file name. Numbers first, impressions second.

**P1 — Responsiveness sweep (10 min)**
Setup: `L_TDD_Test_Movement`, flat zone, `TDD.Movement.Overlay 1`, `TDD.Movement.Record start`, `t.MaxFPS 60`.
Steps: (1) Idle → jog for 2 s → stop, ×5. (2) Jog → sprint → release, ×5. (3) Jog → 180° reversal, ×10. (4) Jog → dodge, ×10. (5) Jump, then jump at 0.10 s after leaving a ledge (coyote), ×5.
Expected: motion begins on the frame you press; no perceived dead zone; reversal does not slide; dodge does not clip on flat ground.
Record: `TDD.Movement.Report` output, plus a one-paragraph qualitative note (label it qualitative).

**P2 — Camera in a tight interior (5 min)**
Setup: 1.2 m corridor zone; sweep yaw slowly and quickly; walk into a corner and reverse; back to a wall and drag the mouse upward.
Expected: camera pulls in and never enters geometry; no flicker between in/out states; no snap when exiting the corridor; shoulder swap works and keeps the character off-centre convincingly.
Record: any penetration with timestamp (from CSV) — a single penetration fails the procedure.

**P3 — Steps, slopes, drops (10 min)**
Setup: step rig, slope rig, drop rig.
Steps: walk up/down each step height; walk up 40° and 50°; walk off 1 m, 2 m, 4 m drops; land while holding forward.
Expected: no capsule pop or stuck state; 50° slope clearly refuses; landing recovers and does not eat held input; no fall-through.
Record: any stuck state, with the `TDD.State.History` dump.

**P4 — Device parity (10 min)**
Setup: keyboard/mouse then gamepad.
Steps: repeat P1 steps 1–4 on both devices.
Expected: same timings within one frame; no device-specific dead zone that makes one feel sluggish.
Record: side-by-side report outputs.

**P5 — Long-session stability (20 min)**
Setup: continuous movement, dodges, camera sweeps for 20 minutes.
Expected: no drift in capsule height, no movement-mode leak (verify with `TDD.Movement.Overlay`), memory flat (no per-frame allocation growth), frame time stable.
Record: memory before/after from `memreport -full`, frame time median and 1% low.

---

## 7. The controlled test environment (`L_TDD_Test_Movement`)

| Zone | Content | Gate/measurement |
|---|---|---|
| `Z_Flat` | 100×100 m plane, 1 m floor grid material, 10 m distance markers | Spawn; start/stop markers at 5 m intervals |
| `Z_Slope` | Ramps at 30°, 40°, 50°, 60° | Entry/exit trigger volumes log displacement and time |
| `Z_Steps` | Steps at 15, 30, 45, 50 cm, 3 m wide | Capsule Z sampling on crossing |
| `Z_Corridor1` | 1.2 m wide, 12 m long, 3 m high, closed both ends | Camera sweep rig with scripted yaw/pitch driver |
| `Z_Corridor2` | 2.0 m wide, with a 90° corner and a doorway | Same, corner behaviour |
| `Z_Drop` | Platforms at 1, 2, 4 m with a 12 m landing area | Landing velocity and recovery sampling |
| `Z_Dodge` | Flat 20 m run-up with a wall variant | Distance and i-frame sampling |
| `Z_SpawnPoints` | Named `PlayerStart` actors per zone | Automation entry points |

The map is engine-basic: grey materials, no lighting artistry, no attempt at presentation. It is a measuring instrument. It must not be mistaken for environment work, and it is excluded from Shipping cooks by folder.

---

## 8. Performance observation requirements

For M1 the report must include, from a Development build on reference hardware:

1. Player frame cost breakdown (Insights scopes for input, CMC, locomotion, camera, metrics) against AC-17/M-11.
2. Median and 1% low frame time over a 120 s scripted run in `Z_Flat` and `Z_Corridor1`, with the metrics recorder **on** and **off** (the harness must not distort what it measures by more than 0.05 ms).
3. Memory: `memreport -full` before and after P5, showing no growth attributable to my components.
4. Any observed hitch with cause (streaming, GC, shader) — attributed or explicitly marked unattributed.

"Runs smoothly" is not a performance observation.

---

## 9. Definition of done (M1)

- All 20 acceptance criteria pass, with quoted results.
- All named tests exist and pass in CI; three consecutive cold runs identical (AC-20).
- Manual procedures P1–P5 executed and recorded, including the qualitative notes.
- No `Tick` without justification; no gameplay literal outside data assets; no `UE_LOG` spam in Shipping.
- Metrics harness on by default in Development, off in Shipping, and proven not to distort measurement beyond 0.05 ms.
- Interfaces in §10 published and unchanged since the assessment (or changed via ADR).
- Handoff report per CODING_STANDARDS §9 / assessment §9, listing every file touched and every status honestly.
- Known limitations listed explicitly, with a named placeholder ID for anything stand-in.

**M1 cannot be marked complete on the strength of a human saying it feels responsive.** It is complete when the numbers say so and the reviewer can reproduce them.

---

## 10. Interfaces exposed at M1 (frozen for Agent 2)

Published to Agent 2 so they can build enemy perception, telegraphs and boss fairness rules without waiting for M3:

```cpp
// TDDGameplay/Public/Combat/TDDCombatant.h  (interface; implementation lands in M3)
class TDDGAMEPLAY_API ITDDCombatant
{
public:
    virtual FGuid GetEntityId() const = 0;
    virtual bool  IsAlive() const = 0;
    virtual ETDDCombatState GetCombatState() const = 0;
    virtual bool  IsTelegraphingAttack() const = 0;        // M3
    virtual float GetAttackTelegraphRemaining() const = 0; // M3, gameplay seconds
    virtual void  ApplyStagger(float DurationSeconds, FGameplayTag Source) = 0;
};

// Exposed now (implemented in M1)
UTDDCharacterStateMachine::GetState / IsInState / AllowsInput / OnStateChanged
UTDDTargetLockComponent::GetLockedTarget / IsLockedOn        // stub: always unlocked in M1
FTDDPawnKinematics (value snapshot; no pointers)             // fields: EntityId, Velocity,
                                                             // bGrounded, Speed2D, Stance,
                                                             // HeightAboveGround, CombatState
```

Contract stability: these names and signatures are frozen for M1–M3. Additions are allowed; renames are not. If Agent 2 needs a different shape, that is an ADR before M3, not a quiet change mid-phase.

---

## 11. Known limitations and out-of-scope items at M1

| Item | State | Note |
|---|---|---|
| Animation quality | Placeholder mannequin, no clips | C-1 pending; M2 integrates real clips |
| Motion Matching | Not used; provider interface exists with blendspace implementation | ADR-0005; MM evaluated in M2 |
| Traversal | Not implemented (M2) | Declared state exists, unused |
| Interaction | Not implemented (M2) | Prompt/focus system follows traversal |
| Combat, weapon, damage, enemies | Not implemented (M1–M6) | Contracts published only |
| Lock-on | Stub (no targets exist) | Real in M3 |
| Stamina economy | Not implemented | Q-08 (progression model) open; dodge cooldown only in M1 |
| Difficulty options | Not implemented | Q-11 open |
| Accessibility (remapping, toggle modes) | Input config supports it; UI is Agent 3/M6+ | Q-10 |
| Feel tuning | Engineering defaults only | Requires CD feel pass; all values are data |

---

## 12. Risks specific to M1

| Risk | Mitigation |
|---|---|
| CMC defaults produce mushy, floaty movement that gets "fixed" by adding hacks | Explicit tuning table (§3.3) with rationale, all data-driven, so the feel pass is a data edit; measurement before opinion |
| Step-up and slope edge cases silently regress | Dedicated physics zones + AC-05/AC-06 as permanent tests |
| Camera collision solved per-scene instead of systematically | One rig system, probe-based, tested in two corridor widths |
| Metrics harness distorts measurement | Measured on/off delta as a required observation |
| One-frame animation latency mistaken for a bug and "fixed" by breaking correctness | Documented in assessment §4.5; Option B is a measured experiment, not a default |
| Root-motion movement-mode leaks | AC-15 unit test over 100 random actions |
| Mannequin placeholder mistaken for character progress | Named `PLACEHOLDER-A1-01`, documented in every report, no Adanna-specific tweaks applied to it |

---

## Appendix A — Contract additions requested from Agent 3 (`TDDCore`)

These are **requests**, not unilateral definitions. Agent 3 owns `TDDCore`; I need these shapes to exist before M1 compiles.

```cpp
// TDDCore/Public/Types/TDDCombatTypes.h
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

// TDDCore/Public/Types/TDDPawnTypes.h
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

Requested rationale: `ETDDCombatState` is consumed by Agent 2's AI, Agent 3's UI and my combat component; it must live in the leaf module to avoid an upward dependency (ADR-0003). `FTDDPawnKinematics` is the only sanctioned way for AI/animation to read player state, and it deliberately contains no actor pointers.

**Change request log:** none yet. If Agent 3 accepts a different shape, I will adapt my code, not fork the type.

---

## Appendix B — File/asset naming for this milestone

| Kind | Names |
|---|---|
| Classes | `ATDDPlayerCharacter`, `ATDDPlayerController`, `UTDDCharacterMovementComponent`, `UTDDCharacterStateMachine`, `UTDDLocomotionComponent`, `UTDDBlendSpaceProvider`, `UTDDCameraRigComponent`, `ATDDPlayerCameraManager`, `UTDDMovementMetricsComponent`, `UTDDPlayerInputComponent` |
| Pure logic | `FTDDInputBuffer`, `FTDDDodgeSpec`, `FTDDLocomotionParams`, `FTDDStateRuleRow` |
| Data | `DA_MovementConfig`, `DA_CameraConfig`, `DT_StateRules`, `DA_InputConfig` |
| Maps | `L_TDD_Test_Movement` |
| Console namespace | `TDD.Movement.*`, `TDD.State.*`, `TDD.Input.*` |
| Test prefixes | `TDD-Unit.Movement.*`, `TDD-Functional.Movement.*` |
| Placeholders | `PLACEHOLDER-A1-01` (stock mannequin mesh/anims) |

---

## Appendix C — Review questions for the Technical Director

1. Accept `ETDDCombatState` / `FTDDPawnKinematics` into `TDDCore` as specified (Appendix A)?
2. Approve the M1 tuning defaults in §3.3 as an engineering baseline for the CD's feel pass?
3. Approve thresholds M-01…M-13 where marked **[A1]** (they are my proposals, not from the MEAD)?
4. Confirm test content under `Content/TDD/Test/` is excluded from Shipping cooks (Agent 3).
5. Accept that M1 will use the stock mannequin, with animation quality deferred to M2 and requiring C-1 content?
6. Confirm whether `t.MaxFPS 60`-capped functional tests are acceptable as the canonical number for responsiveness (I recommend yes, with a 120 fps latency cross-check).
