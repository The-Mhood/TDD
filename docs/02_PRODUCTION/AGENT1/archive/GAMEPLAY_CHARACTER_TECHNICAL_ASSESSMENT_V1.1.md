# GAMEPLAY AND CHARACTER TECHNICAL ASSESSMENT

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Agent:** 1 — Gameplay, Character and Combat Engineering
**Document:** TDD-A1-ASSESS-001
**Version:** 1.1 — revised after Technical Director review (2026-11-16)
**Date:** 2026-11-16
**Supersedes:** v1.0 (`archive/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT_V1.0.md`, preserved unchanged)
**Change log:** §11 of this document records every correction made in v1.1
**Governing architecture:** `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` (TDD-MEAD-001)
**Next document:** `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md`

---

## 0. Control and verification statement

### 0.1 What this document is

An inspection-grounded assessment of the gameplay/character domain, the gap between that domain and what exists, the prerequisites that must land before I can write buildable code, the architecture I intend to implement inside my ownership boundary, the interfaces I will expose to Agent 2 and Agent 3, and a staged plan whose first milestone is a responsive, testable third-person character controller.

### 0.2 What I could and could not verify

| Activity | Possible | Result |
|---|---|---|
| Read repository contents and history | Yes | No Unreal project present; documentation only |
| Read the authoritative Art Bible / decision registers | Yes (Drive connector) | 176 indexed files, 7 approved concept designs, no 3D/animation/audio assets, animation+combat design folder empty |
| Compile any C++ | **No** — no UE 5.8, no UBT, no MSVC/Clang, no .NET | Zero build evidence possible here |
| Run PIE, automation tests, or measure frame times | **No** — no GPU, no engine | Zero runtime evidence possible here |
| Author source and specification | Yes | This assessment and the M1 specification |

Per ADR-0012, everything I write is `DESIGN_ONLY` until the Technical Director builds it on the UE 5.8 production workstation. **I am not reporting any implemented feature. Nothing in my domain exists yet.**

### 0.3 Scope of my ownership (restated so boundaries are unambiguous)

I own: player character, movement, physics, camera, combat foundations, weapon handling, animation integration for the player, player-facing feedback, and the combat-facing contracts that enemies use.

I do not own: world/chapter architecture, streaming, encounters, boss AI internals, quests/progression, UI framework, persistence, build/release, and all final creative, narrative and visual decisions.

---

## 1. Inspection findings

### 1.1 Repository

```
5e3d1da Initial commit            README.md only (6 bytes)
169a8d8 TDD-arch: add master engineering architecture and governance docs
```

Contents today: `README.md`, `.gitignore`, `.gitattributes`, and 20 documents under `docs/`. No `.uproject`, no `Source/`, no `Config/`, no `Content/`, no assets, no tests, no CI. `Source/`, `Content/`, `Config/` exist as empty directories only.

**Conclusion:** there is no Unreal project to inspect. There is no existing gameplay code, no character class, no input configuration, no animation setup, and no prior agent work in my domain to preserve, extend or avoid overwriting. The instruction "use the project's existing architecture where appropriate" resolves to: **use TDD-MEAD-001 and the ADRs, because they are the only architecture that exists.**

### 1.2 Workspace capability (blocking constraint)

No Unreal Engine, no UnrealBuildTool, no .NET SDK, no MSVC/Clang, no GPU, 2 vCPU, 3 GB RAM. I cannot compile, launch PIE, run an automation test, capture a frame time, or open a level. This is not a temporary glitch; it is the environment. ADR-0012 defines the consequence: every claim carries a status, and `IMPLEMENTED_AND_VERIFIED` requires evidence produced elsewhere.

### 1.3 Architecture I inherit and must comply with

| Source | Constraint on my work |
|---|---|
| MEAD §3.2 | `TDDGameplay` may not include `TDDAI`, `TDDNarrative` or `TDDUI` headers. All upward communication via `TDDCore` events/interfaces |
| ADR-0002 | Gameplay rules in C++; Blueprints only for content wiring and data |
| ADR-0003 | Strict module layering; `TDDCore` is a leaf owned by Agent 3 |
| ADR-0004 | GAS for attributes/effects only; attack *flow* stays custom in `UTDDCombatComponent` |
| ADR-0005 | Locomotion behind `ITDDLocomotionAnimProvider` with Motion Matching and BlendSpace implementations |
| ADR-0011 | Single-player; no replication code |
| ADR-0012 | Status vocabulary; no verification claims without external evidence |
| MEAD §4.2 | Player kit contract (light chain, heavy, block, parry, dodge, lock-on, sprint, interact) with default timings |
| MEAD §8.3 | Animation may only talk to gameplay through the declared notify set |
| MEAD §13.2 | `ITDDCombatant` and the `UTDDCombatComponent` public API shape I must publish |
| CODING_STANDARDS | IWYU, export macros, naming, tick justification, tests in the same commit |

I am not free to redesign these. If a constraint proves wrong once code exists, it goes through the ADR process in MEAD §13.3.

### 1.4 Art, design and content authority relevant to my domain

| Item | Status | Direct consequence for gameplay/character engineering |
|---|---|---|
| `CHAR_ADANNA_MASTER_REFERENCE_V001` | **APPROVED** (OAD-02) | Identity anchor for any character work; proportions, hair, costume, mmuo markings are not mine to change |
| Left shoulder guard (OAD-01), single larger left guard when upgraded (OAD-10) | APPROVED | Armour mesh asymmetry; sockets and IK must survive an armour swap without re-rigging |
| Blade worn on left hip (OAD-09); approved blade only, no alternates (OAD-37) | APPROVED | Weapon socket scheme must be `holster_l` + hand grip; exactly one weapon data asset in M4 |
| `WEAPON_ADANNA_PRIMARY_BLADE_V001.jpg` | Exists in Drive (`06_WEAPONS_AND_ARMOUR`, plus a duplicate). **Not among the 7 approved designs** | Grip type, blade length, guard geometry and two-handed feasibility are **unconfirmed**. My socket layout must not assume a blade length |
| `09_ANIMATION_AND_COMBAT` folder | **Empty** | There is no combat design document, no animation direction, no move list and no timing design beyond MEAD §4.2 defaults. M3+ is blocked on this |
| Rigged Adanna mesh, skeleton, locomotion clips, attack clips | **None exist** | M1 must run on a stock mannequin; M2 measurement of foot slide needs real clips; M3+ needs an attack set |
| Cultural items OAD-03 (Ezeani regalia), OAD-04 (Okwu/raffia), OAD-06 (uli motifs), OAD-07 (bronze level) | OPEN, consultant pending | Not blocking M1–M3, blocking final character materials |
| Boss movesets for the seven named bosses | **Not specified anywhere** | I own enemy *combat interaction contracts* (telegraphs, timing, state communication), not the movesets. Agent 2 owns boss behaviour; I must give them a contract they can build against before they need it |

**Finding that matters most:** the project has approved *visual* references for the protagonist but **no combat design, no animation design and no assets**. The gameplay domain therefore cannot be built "from the art down". It has to be built as a measured, data-driven system that accepts content later without rework. That is the organising principle of everything below.

---

## 2. Gap analysis against my five responsibilities

| # | Responsibility | Current state | What is actually required | Blocker |
|---|---|---|---|---|
| 1 | Character controller | Nothing | CMC configuration, state machine, input pipeline, camera, dodge, traversal, measurement harness | Phase 0 skeleton (Agent 3), mannequin clips for locomotion |
| 2 | Combat architecture | Nothing (design only, MEAD §4.2/§5) | Combat component, attack data assets, damage pipeline through GAS, block/parry/dodge, posture/stagger, hitstop, reactions | M1–M2 complete; dummy target; placeholder attack clips |
| 3 | Animation | Nothing; no rig, no clips, no anim BP, empty design folder | Locomotion provider, montage integration, notify contract implementation, hit reactions, weapon anim, interaction anim, interruption rules | Animation content + animation direction (external). I can build the integration layer and the notify implementations; I cannot produce clips |
| 4 | Player feedback | Nothing | Hitstop subsystem, camera feedback assets, VFX/audio hooks, HUD state publishing | M3 combat events; audio/VFX content |
| 5 | Gameplay-facing enemy behaviour | Nothing | `ITDDCombatant`, telegraph/timing contract, combat-state events, token participation API | Contract must be published *early* so Agent 2 is not blocked |
| — | Interfaces to Agent 2 | Not yet published | `ITDDCombatant`, `UTDDCombatComponent` API, state events, lock-on query, stagger command | Me (this document + M1 spec), then Agent 3 sign-off for `TDDCore` additions |

---

## 3. Critical path: what I can start, and what is blocked

### 3.1 Prerequisites from Agent 3 (Phase 0) — hard blockers B-1…B-6

I cannot compile a single line of my domain until these exist. They are Agent 3's ownership per MEAD §13.1; I am requesting them, not building them.

| ID | Prerequisite | Why it blocks me |
|---|---|---|
| **B-1** | `TDD.uproject` pinned to UE 5.8, with modules `TDDCore`, `TDDGameplay`, `TDDAI`, `TDDWorld`, `TDDNarrative`, `TDDUI`, `TDDEditor`, `TDDTests` and correct `Build.cs`/`Target.cs` files | No module, no compilation unit |
| **B-2** | `TDDGameplay.Build.cs` public dependencies: `Core`, `CoreUObject`, `Engine`, `InputCore`, `EnhancedInput`, `GameplayTags`, `GameplayTasks`, `MotionWarping`, `AnimGraphRuntime`, `PoseSearch`, `Niagara`, `UMG`, `Slate`, `SlateCore`, plus private `TDDCore` | Missing deps = unresolved includes, and I must not add them unilaterally (shared build file) |
| **B-3** | `TDDCore` baseline contracts: `ETDDCombatState`, `FTDDPawnKinematics`, `ITDDDamageable`, `FTDDDamageRequest`, `ITDDInteractable`, `UTDDEventBus` + the event structs in MEAD §3.5 | My components publish and consume these; defining them myself would create the competing-Core failure MEAD §13.5 forbids |
| **B-4** | Enhanced Input configuration: `DefaultInput.ini`, an input config data asset (`DA_InputConfig`) and mapping contexts registered, with a player-input subsystem or equivalent | I cannot bind actions that do not exist; input asset naming must be agreed once, not per agent |
| **B-5** | Log categories: `LogTDDGameplay` (or per-area categories) declared in `TDDGameplay` | Logging is mandatory in my components; declaring categories in two places collides |
| **B-6** | A build + test workflow on the UE 5.8 workstation, and a first green CI run | Without it I cannot move anything from `IMPLEMENTED_UNVERIFIED` to `VERIFIED`, and the milestone gates are meaningless |

**B-1…B-5 are small.** They are a few files of scaffolding. **B-6 is the project's real bottleneck** and is Agent 3's problem to prove, not mine to assume.

### 3.2 Content prerequisites (external; I do not create these)

| ID | Content | Needed by | Where it comes from |
|---|---|---|---|
| C-1 | Locomotion clip set (idle, walk, jog, sprint, strafe set, starts, stops, turns) — even a 20-clip placeholder set | M2 (measurement), M1 can limp on the stock mannequin | Animation team; direction not yet written |
| C-2 | Combat design: Adanna's move list, weapon handling intent (one- vs two-handed, grip), parry/block visual language | M3 | `09_ANIMATION_AND_COMBAT` is empty; needs Creative Director direction |
| C-3 | Attack/reaction/hit-reaction clip set | M3–M5 | Animation team |
| C-4 | Approved weapon reference confirmation (grip, length, guard) | M4 | Art Bible; weapon asset exists but is not in the approved designs list |
| C-5 | Enemy telegraph visual/audio language | M6 | Creative Director + Agent 2 |

### 3.3 What I can produce *now*, with no engine

1. This assessment.
2. The M1 implementation specification with measurable acceptance criteria.
3. The exact interface headers I will publish, written as contract proposals for Agent 3 to accept into `TDDCore` and Agent 2 to code against (M1 spec appendix).
4. Test designs (assertions, thresholds, procedures) that will become code the moment B-1…B-6 land.
5. Data-asset schemas and default tuning values, so tuning is authorable on day one rather than hard-coded and retrofitted.

Anything past item 5 would be unverifiable source that another agent has to debug blind. I will not do that.

---

## 4. Proposed player architecture (my domain)

### 4.1 Class map

```
ATDDPlayerCharacter : ACharacter
├── UTDDAttributeSet / UTDDBasicAttributeComponent  (GAS adapter, ADR-0004)
├── UTDDCharacterStateMachine    ← single authority on player state
├── UTDDLocomotionComponent      ← gait/stance intent → CMC + anim provider
├── UTDDLocomotionAnimProvider   (interface; MM and BlendSpace impls, ADR-0005)
├── UTDDCombatComponent          ← attack flow, windows, cancels, hit resolution
├── UTDDWeaponComponent          ← weapon mesh, sockets, holster/draw, trails
├── UTDDInteractionComponent     ← focus, prompts, hold-to-perform
├── UTDDTraversalComponent       ← ledge/vault detection + execution
├── UTDDCharacterAudioComponent  ← footsteps, cloth, exertion hooks
├── UTDDMovementMetricsComponent ← measurement/instrumentation (dev builds)
└── UTDDPlayerInputComponent : UEnhancedInputComponent
        (buffering, mapping-context switching, hold/toggle semantics)

ATDDPlayerController : APlayerController
├── ATDDPlayerCameraManager : APlayerCameraManager
└── UTDDCameraRigComponent   ← rig blending, lock-on framing, shake

Components that live in TDDCore (Agent 3) or other modules and are only *queried*:
    UTDDEventBus, UTDDPersistenceSubsystem, UTDDPawnRegistry (Agent 2/3)
```

Design rules for this map:

- **One authority on state.** `UTDDCharacterStateMachine` decides what is allowed. No component self-authorises an action by checking another component's flags; that produces the classic "two systems both think they own dodge" bug.
- **No component reaches into another's internals.** They talk through the state machine, through the combat component's public API, or through events.
- **Instrumentation is a component, not scattered `UE_LOG`s**, so measurement can be enabled, disabled and exported by console command and is identical in every run.

### 4.2 Player state machine

States (M1 implements the bold ones; the rest are declared now so transition rules do not need rewriting):

| State | Entered by | Exit to | Notes |
|---|---|---|---|
| **`Idle`** | no movement input, grounded | `Locomotion`, `Airborne`, `Dodge`, `Attack`, `Interaction`, `Cinematic` | |
| **`Locomotion`** | movement input, grounded | `Idle`, `Sprint`, `Airborne`, `Dodge`, `Attack`, `Interaction`, `Traversal`, `Cinematic` | Gait resolved by `UTDDLocomotionComponent` |
| **`Sprint`** | sprint held/released policy, grounded, not in combat lock | `Locomotion`, `Airborne`, `Dodge` | No attacks from sprint except approved dash attack (future) |
| **`Airborne`** | became ungrounded (jump, fall, knockback) | `Land`, `Dodge` (air-dodge, if approved later) | Air control limited by data |
| **`Land`** | grounding while `Airborne` | `Idle`, `Locomotion` | Landing recovery window data-driven; cancelled by dodge input above a fall-speed threshold only if data allows |
| **`Dodge`** | dodge intent accepted | `Locomotion`, `Idle`, `Attack` (dodge-cancel rules), `Airborne` | i-frames expressed in gameplay seconds, not frames |
| `Attack` | attack intent accepted | `Locomotion`, `Idle`, `Dodge` (per cancel rules), `Stagger` | M3+ |
| `Block` / `Parry` | block intent | `Locomotion`, `Stagger` | M3+ |
| `Stagger` | `ApplyStagger` from damage or parry | `Locomotion`, `Idle`, `Dead` | M3+ |
| `Traversal` | traversal candidate confirmed | `Locomotion`, `Idle` | M2+ |
| `Interaction` | interactable accepted | `Idle`, `Locomotion` | M2+ |
| `Cinematic` | cinematic subsystem takes control | previous state | Owned by narrative/cinematic system; I only obey and restore |
| `Dead` | lethal damage | `Idle` on respawn | Post-M3; respawn driven by flow system |

Transition authority: a single `FTDDStateRules` data table row per state declares `AllowedTransitions`, `AcceptedInputs`, `bLocksMovement`, `bLocksRotation`, `bLocksCameraRig`, and `bInvulnerable`. Code reads the table; designers can re-tune without a programmer, and a unit test enumerates every state pair to assert there are no undeclared transitions.

**Revised in v1.1 (C-06): an allowed-transition matrix is necessary but not sufficient.** A matrix says *whether* a transition is permitted; it does not say *when* it must be refused, what may interrupt it, what must happen on exit, or how it ends. The authoritative transition semantics are therefore specified in **M1 spec §3.2** and cover, per state: entry preconditions; forced-entry sources; forced-exit sources; interruption windows and who may interrupt; exit actions (montage stop, tag clearing, mode restoration, lock release, event publication); recovery conditions; minimum dwell; locks; and the buffer policy for requests received while locked. Priority ordering for forced transitions is defined there (Dead > Cinematic > Stagger > Attack/Block > Dodge > Traversal > Land > Locomotion) so two systems can never both believe they control the character.

### 4.3 Input mapping (full, to be realised in B-4)

**Ownership (corrected in v1.1 — see C-03):** in Unreal the gameplay input component belongs to the **pawn**, not the controller. `APawn::PawnClientRestart()` calls `SetupPlayerInputComponent()` with the component produced by `APawn::CreatePlayerInputComponent()`; the class is controlled by `APawn::InputComponentClass` (or by overriding `CreatePlayerInputComponent()`). `UTDDPlayerInputComponent` is therefore created and owned by `ATDDPlayerCharacter`, exists only while the pawn is possessed by a player controller, and is destroyed/recreated on re-possession. `ATDDPlayerController` keeps only a separate, minimal input component for pause/menu actions that must work while the pawn is dead, unpossessed or in a cinematic. The controller routes device input and owns the camera manager; it does **not** own gameplay action bindings. v1.0 was ambiguous about this and is corrected here.

Mapping contexts: `IMC_Exploration`, `IMC_Combat`, `IMC_LockOn`, `IMC_Cinematic`, `IMC_Menu`, `IMC_Traversal`. Only one gameplay context + `IMC_Menu` overlap is legal; the state machine requests context switches via the subsystem, and contexts are pushed against the pawn's input component (not recreated per switch).

| Action | Keyboard/Mouse | Gamepad | Type | Buffering policy |
|---|---|---|---|---|
| `Move` | WASD | Left stick | Axis2D | Device-aware deadzone (0.15 stick / 0 mouse) |
| `Look` | Mouse | Right stick | Axis2D | Sensitivity + invert per user settings |
| `Sprint` | Left Shift | L3 (press) | Button (hold or toggle per settings) | Held state |
| `Jump` | Space | A / Cross | Button | Buffer 0.15 s, coyote time 0.12 s |
| `Dodge` | Ctrl (left) or Alt | B / Circle | Button | Buffer 0.20 s |
| `LightAttack` | Left Mouse | X / Square | Button | Buffer 0.20 s; chain window from attack data |
| `HeavyAttack` | Right Mouse | Y / Triangle | Button | Buffer 0.20 s |
| `Block` | Right Mouse (hold) or Q | LB / L1 | Button (hold or toggle) | Held; parry window on press inside guard |
| `Parry` | Q (tap) | LB (tap) | Button | 0.15 s window from press (MEAD §4.2) |
| `LockOn` | Middle Mouse | R3 (press) | Button (toggle + hold modes) | Immediate |
| `Interact` | E | RB / R1 | Button (hold variants) | Immediate |
| `TraversalConfirm` | Space / context | A | Button | Immediate |
| `Pause` | Esc | Start | Button | Immediate, always allowed |
| `DebugOverlay` | F1 (dev only) | — | Button | Dev builds only |
| `CycleTargetLeft/Right` | Mouse wheel / Q-E (lock-on) | D-pad left/right | Button | Immediate |

Mouse and keyboard are first-class (a GoW-class PC action game must not feel like a pad port). Settings support per-action rebinding, hold/toggle inversion for sprint/block/interact, stick/mouse deadzones, sensitivity curves, and an accessibility option to remove repeated taps (no QTE-style mashing is designed, and if one appears it will get a hold alternative — G-ACCESS-1, open).

### 4.4 Data assets for gameplay tuning

| Asset | Holds | Owner |
|---|---|---|
| `DA_MovementConfig` | CMC values, gait speeds, accel/decel, air control, dodge spec, step/slope limits | 1 |
| `DA_CameraConfig` | rig offsets, FOV, lags, pitch clamp, lock-on scoring weights | 1 |
| `DA_TraversalConfig` | detect ranges, heights, montage-per-type, warp targets | 1 |
| `DA_InputConfig` | mapping contexts, action refs | 1 (with 3 for registration) |
| `DT_StateRules` | transition table above | 1 |
| `DA_Attack_*`, `DA_EnemyArchetype_*` | combat and AI content | 1 (attacks), 2 (archetypes) |

All values above are authorable; no tuning literal lives in C++ beyond sentinel defaults. That is a hard rule because tuning is the single largest iteration cost in action-game combat.

### 4.5 Tick ordering, latency definitions and the responsiveness budget

**Corrected in v1.1 (C-02).** v1.0 asserted that animation evaluates after movement and therefore the visible pose lags input by one frame. That was an assumption about engine tick groups presented as a fact, and it contradicted v1.0's own same-frame latency criterion (AC-01 in the M1 spec). It is withdrawn. What replaces it is an explicit three-stage latency model, each stage separately measured, with the engine's actual behaviour recorded as a measurement result rather than a claim.

Observed tick ordering within one engine frame (to be **confirmed by instrumented measurement** in M0, not assumed):

```
Frame F:
  TG_PrePhysics    : PlayerController input processing (Enhanced Input)
                     → intent produced → buffered → state machine decision
  TG_PrePhysics    : CharacterMovementComponent tick (accel applied, capsule moved)
  TG_PostPhysics   : SkeletalMesh pose evaluation; camera update
  (render)         : frame presented
```

Three latency stages, defined so tests cannot conflate them:

| ID | Stage | Definition | Frame-index reference points |
|---|---|---|---|
| **L1** | Sample → intent | From the frame on which the input event is *delivered to the engine* to the frame on which the intent is recorded (buffered or accepted) | `FrameInjected` → `FrameIntentRecorded` |
| **L2** | Intent → first velocity change | From `FrameIntentRecorded` to the first frame in which `CMC->Velocity` differs from the pre-intent baseline by more than ε (1 cm/s) | `FrameIntentRecorded` → `FrameVelocityChanged` |
| **L3** | Intent → pose reflects it | From `FrameIntentRecorded` to the first frame in which the animation parameter set (speed/gait) reflects the new velocity | `FrameIntentRecorded` → `FramePoseUpdated` |

Expected values and the reasoning behind them:

- **L2 = 0 frames** is the design requirement: input processing, state decision and CMC movement occur in the same `TG_PrePhysics` pass, so velocity must change in the frame the intent is recorded. Any L2 > 0 is a **tick-order defect**, not a tuning issue, and fails AC-02.
- **L1 ≤ 1 frame.** It is 0 when the input event is delivered before that frame's input processing (which is how the automation harness injects, making tests deterministic) and 1 when delivered after it. The 1-frame case is the real-world worst case for a device polled mid-frame.
- **L3 ≤ 1 frame**, and its *actual* value is reported, not predicted. If the engine evaluates the pose in `TG_PostPhysics` after movement, L3 is 0; if the pose for frame F is built before movement, L3 is 1. v1.0 claimed 1 without evidence; v1.1 requires the number to be measured at 60 and 120 FPS and recorded in the phase report.
- **Device-to-photon latency is out of scope for automation** (OS polling, display scanout, vsync). It is measured manually with a high-speed camera or a latency tester if the Creative Director requires it, and is reported separately so it is never confused with L1–L3.

Measurement rules (both frame rates):

1. Tests run with `t.MaxFPS` fixed at 60, then repeated at 120; vsync disabled; physics substepping disabled unless explicitly under test (recorded either way).
2. Results are reported in **frames and milliseconds** (at 60 FPS one frame = 16.667 ms; at 120 FPS, 8.333 ms) so a frame-rate-dependent threshold cannot hide.
3. The harness logs frame counters from a single monotonic source (the metrics component), never from wall-clock deltas, so a hitch cannot masquerade as latency.
4. If L3 measures 1 and the Creative Director judges it perceptible, the *only* sanctioned remedy is the measured `TG_PrePhysics` mesh-tick experiment below; it is adopted only if it reduces perceived latency and the M2 foot-slide budget still holds.

Budget table for the player, measured not assumed:

| Stage | Budget (ms) | Measurement |
|---|---|---|
| Input sampling + intent + state decision | ≤ 0.10 | Insights scope |
| CMC update | ≤ 0.15 | Insights |
| Locomotion component + anim provider parameter update | ≤ 0.10 | Insights |
| Combat component (idle/no attack) | ≤ 0.02 | Insights |
| Camera rig + spring arm | ≤ 0.10 | Insights |
| **Total player frame cost** | **≤ 0.30** (MEAD §17 budget) | `stat game` scope |

### 4.6 Root motion policy (ADR-0013, proposed by me)

Root motion is the single most common source of "the character controller feels wrong" in third-person action games. Policy:

| Motion | Root motion? | Reason |
|---|---|---|
| Ground locomotion | **No** | Capsule driven by CMC; animation follows velocity. Root motion locomotion fights collision, breaks acceleration curves, and makes input latency visible |
| Dodge | **Yes**, authored distance, pre-validated by a capsule sweep, clamped with a fallback clip if blocked | Precise, repeatable distances. Collision authority stays with CMC; the sweep only chooses distance and clip (v1.1, C-05/C-07) |
| Attacks with a lunge | **Yes**, with Motion Warping to the target | Alignment quality; root motion supplies travel, warping supplies aim. The 300 cm / 60° values are **provisional and configurable** (per-attack override), not constants (v1.1, C-05) |
| Stationary attacks | **No** (in-place clip) | Avoids drift; damage comes from windows, not translation |
| Traversal (vault/mantle) | **Yes** + Motion Warping entry/exit alignment | Quality of alignment; capsule is locked to CMC during the clip and snapped to the validated end transform |
| Cinematics | **Yes**, with the capsule frozen and restored on exit | Standard cinematic practice |
| Hit reactions | **No** for small reactions; **Yes** for knockdowns | Predictability; knockdowns need authored displacement |

**Engine configuration (corrected in v1.1, C-05).** `AnimInstance->SetRootMotionMode(ERootMotionMode::RootMotionFromMontagesOnly)`; `bAllowPhysicsRotationDuringAnimRootMotion=false`.

v1.0 proposed setting the CMC to `MOVE_None` during root-motion montages. That is **withdrawn as an assumption**: CMC processes animation root motion inside its movement update, so a mode in which that update does not run risks the capsule never receiving the authored translation, and the failure would appear as "the attack has no lunge" rather than as an error. The revised policy is specified in ADR-0013 v1.1: root-motion actions keep a CMC mode in which the movement update *does* run, with input influence suppressed and rotation mode controlled per action, so that CMC performs the translation **and** its own collision sweeps. This is to be **verified on the first build** by an instrumented test (`TDD-Unit.Movement.RootMotionAppliesToCapsule`) that asserts capsule displacement actually occurred, at which point the mechanism is either confirmed or replaced — it is not treated as true because it was written down.

Traversal exit transforms are revalidated against collision at the exit notify before the capsule is snapped (v1.1, C-05); see M1 spec §3.9 and ADR-0013 §5.

### 4.7 Camera architecture

`ATDDPlayerCameraManager` + `UTDDCameraRigComponent` with named rigs:

| Rig | Offset / arm | FOV | Use |
|---|---|---|---|
| `Explore` | shoulder (0, 45, 65), arm 320 cm | 90° | Default |
| `CombatSoft` | (0, 55, 60), arm 380 cm | 95° | Enemies within 12 m, no lock |
| `LockOn` | framing both actors, screen-space bias 0.35 | 95° | Hard lock |
| `Traversal` | pulled back/down, wider | 90° | Mantle/vault |
| `Cinematic` | Sequencer owns it | per shot | Blended in/out over 0.4 s |

**Ownership (corrected in v1.1, C-04).** UE requires camera *modifiers* (shakes, post-process blends) to be applied through the player camera manager, which the player controller owns and creates. Rig *state* (desired arm length, offsets, FOV per gameplay state) belongs with the pawn's gameplay state. Therefore:

| Element | Owner | Responsibility |
|---|---|---|
| `ATDDPlayerCameraManager` | created by `ATDDPlayerController` | Camera shakes, post-process blending, FOV blending; the only place `UCameraModifier`/`CameraShake` are applied |
| `UTDDCameraRigComponent` | on `ATDDPlayerCharacter` | Computes the desired rig (arm length, socket offset, FOV, lock-on framing) and writes it to the pawn's spring arm; never applies shakes itself |
| `USpringArmComponent` + `UCameraComponent` | on `ATDDPlayerCharacter` | Physical rig; reads desired values from the rig component |
| Sequencer / `CineCameraActor` | cinematic subsystem (Agent 2) | Takes the view target; the rig component detects the takeover and suspends its writes, then restores over 0.4 s on exit |

v1.0 described `ATDDPlayerCameraManager + UTDDCameraRigComponent` as if they were one unit on the pawn; v1.1 separates them because they have different lifetimes and different engine-mandated homes.

**Stability criteria (corrected in v1.1, C-04).** v1.0 used "no camera snap faster than 720°/s except lock-on" as a universal jitter rule. That number is an acquisition bound, not a jitter threshold, and it conflated five distinct failure modes. They are now separate criteria with separate thresholds (all **[A1]** proposals, full set in M1 spec §3.6):

| Failure mode | v1.1 criterion |
|---|---|
| Penetration | Camera never within 10 cm of blocking geometry, sampled every frame over a scripted sweep in 1.2 m and 2.0 m corridors |
| Angular jitter | Per-frame angular delta ≤ 6°/frame and jerk ≤ 3°/frame² during steady following; no more than 3 sign changes of the delta in any 10-frame window |
| Sudden displacement | ≤ 10 cm/frame in normal follow; ≤ 25 cm/frame while an obstruction is actively forcing the boom in; never > 15 cm/frame without an obstruction event flag |
| Obstruction recovery | Re-extension ≤ 150 cm/s, monotonic (no overshoot), complete within 0.6 s for obstructions under 90 cm |
| Intentional acquisition (lock-on) | Whitelisted event: 0.20 s blend, total slew ≤ 120°, peak ≤ 600°/s, completion within 0.35 s; excluded from jitter metrics via an event flag |

Camera *feel* remains a manual (T5) gate; camera *correctness* (the five rows above) is automated.

### 4.8 Traversal architecture (M2)

Trace-based candidate detection (forward + down from a height band), `FTDDTraversalCandidate { Type, EntryTransform, ExitTransform, Height, Depth, bValid }`, validated against capsule clearance and slope; montage selection per type from `DA_TraversalConfig`; Motion Warping aligns entry/exit; capsule is snapped to the validated exit only after the clip's exit notify. **No prompt is shown for an invalid candidate** — refusing to show a broken prompt is better than fixing it later.

### 4.9 Combat architecture (summary; detailed in M3/M4 specs)

Per MEAD §5, unchanged: custom attack flow, animation-notify hit windows, one damage pipeline via `FTDDDamageRequest` → GAS effects, posture/stagger, per-actor hitstop, reaction tables, `FTDDDamageAppliedEvent` on the bus. What I add here is the *boundary*: enemies issue `RequestAttack()` intents and receive damage through `ITDDDamageable`; they never play my montages, and I never read their AI state. Enemy attack *timing* is expressed in the same units as mine (gameplay seconds, telegraph duration, active window, recovery) so Agent 2 can build fairness rules without knowing my internals.

---

## 5. Interfaces

### 5.1 What I expose (published from `TDDGameplay/Public`)

```cpp
// Combat-facing contract consumed by Agent 2's AI (shape fixed in MEAD §13.2)
class ITDDCombatant
{
    virtual FGuid GetEntityId() const = 0;
    virtual bool  IsAlive() const = 0;
    virtual ETDDCombatState GetCombatState() const = 0;
    virtual bool  IsTelegraphingAttack() const = 0;      // added: fairness input for AI
    virtual float GetAttackTelegraphRemaining() const = 0;
    virtual void  ApplyStagger(float DurationSeconds, FGameplayTag Source) = 0;
};

class UTDDCombatComponent : public UPawnComponent
{
    bool  RequestAttack(FName AttackId, AActor* Target);
    bool  CancelAttack(ETDDCancelReason Reason);
    bool  IsAttacking() const;
    float GetAttackRecoveryRemaining() const;
    bool  CanBeInterrupted() const;
};

class UTDDCharacterStateMachine : public UPawnComponent
{
    ETDDPlayerState GetState() const;
    bool  IsInState(ETDDPlayerState State) const;
    bool  AllowsInput(ETDDIntent Intent) const;
    FOnTDDPlayerStateChanged OnStateChanged;   // delegate, no raw actor retention
};

class UTDDTargetLockComponent : public UPawnComponent
{
    AActor* GetLockedTarget() const;           // weak-checked; null when unlocked
    bool    RequestLockOn(AActor* Candidate);
    void    ReleaseLockOn();
    bool    IsLockedOn() const;
};

// Value snapshot for AI/animation consumers — no pointers, no dependencies
struct FTDDPawnKinematics
{
    FVector  Velocity;  bool bGrounded;  float Speed2D;
    ETDDStance Stance;  float HeightAboveGround;
    FGuid    EntityId;  ETDDCombatState CombatState;
};
```

### 5.2 What I need from others

| Need | From | Already specified? |
|---|---|---|
| Module + build scaffolding, `TDDCore` contracts, input config, log categories, CI | Agent 3 (B-1…B-6) | Yes, §3.1 |
| `FTDDDamageRequest` / `ITDDDamageable` shape accepted into `TDDCore` | Agent 3 (owner of Core) | Proposed in MEAD §13.2, appendix of M1 spec |
| Lock-on / target acquisition events | Agent 2 (encounters may want to force/deny lock) | Not yet — I will publish the component and Agent 2 can request additions |
| Cinematic takeover/restore protocol | Agent 2 | MEAD §9.6, needs concrete delegate shape |
| Enemy telegraph timing standard (so fairness rules are shared) | Agent 2 + me | This document §4.9 begins it; M6 completes it |

---

## 6. Measurement and verification plan

### 6.1 Metrics, thresholds, methods

Revised in v1.1 (C-02, C-07, C-08): latency split into three stages, camera split into five criteria, step coverage extended, dodge clearance restated. Metric IDs are stable across documents; the **authoritative acceptance criteria live in M1 spec §4**, and this table is the assessment-level summary that maps to them.

| ID | Metric | Threshold | Method |
|---|---|---|---|
| M-01a | L1 sample→intent | ≤ 1 frame (0 in deterministic harness) at 60 and 120 FPS | `TDD-Functional.Movement.LatencyL1` |
| M-01b | L2 intent→first velocity change | **0 frames** (same `TG_PrePhysics` pass) at 60 and 120 FPS | `TDD-Functional.Movement.LatencyL2` |
| M-01c | L3 intent→pose reflection | ≤ 1 frame; **actual value reported** | `TDD-Functional.Movement.LatencyL3` |
| M-02 | Acceleration to 95% max jog | ≤ 0.35 s **[MEAD]** | `TDD-Functional.Movement.AcceleratesToMaxSpeed` |
| M-03 | Stop from max jog | ≤ 0.20 s, ≤ 50 cm **[A1]** | `TDD-Functional.Movement.StopsWithinDistance` |
| M-04 | 180° turn at max jog | ≤ 0.50 s **[MEAD]**, yaw settles ±2° **[A1]** | `TDD-Functional.Movement.Turn180Degrees` |
| M-05 | Foot slide per metre | ≤ 5 cm at 60 FPS **[MEAD]** — M2 only (needs clips) | M2 harness |
| M-06a | Step-up 15/30/45 cm | Climbs, settles ≤ 0.25 s, ≤ 1 CMC correction **[A1]** | `TDD-Functional.Movement.StepUpSupported` |
| M-06b | Step-up 50 cm | **Blocked**: net Z gain ≤ 1 cm over 5 attempts, speed ≤ 5 cm/s after contact, no Airborne, no penetration **[A1]** | `TDD-Functional.Movement.StepUpOverMaxBlocked` |
| M-06c | Step-down 15/30/45/50 cm | ≤ 45 cm: no Airborne, smooth descent, settle ≤ 0.25 s. 50 cm: Airborne permitted, lands and recovers ≤ 0.25 s **[A1]** | `TDD-Functional.Movement.StepDownBehaviour` |
| M-06d | Angled / sprint / corner approaches | Angled 30/45/60° climbs 45 cm; sprint retains ≥ 60% speed; corner: no stick, ≤ 2 yaw sign flips per 10 frames **[A1]** | `TDD-Functional.Movement.StepAngledApproach`, `.SprintOverStep`, `.CornerStability` |
| M-07 | Walkable slope | 40° traversable, 50° blocked, no jitter **[A1]** | `TDD-Functional.Movement.SlopeLimits` |
| M-08a | Camera penetration | Zero samples < 10 cm from blocking geometry, 60 s sweep, two corridor widths **[A1]** | `TDD-Functional.Movement.CameraPenetration` |
| M-08b | Camera angular jitter | Δ ≤ 6°/frame, jerk ≤ 3°/frame², ≤ 3 sign changes / 10 frames **[A1]** | `TDD-Functional.Movement.CameraAngularStability` |
| M-08c | Camera displacement pop | ≤ 10 cm/frame normal, ≤ 25 cm/frame under active obstruction, never > 15 cm/frame unflagged **[A1]** | `TDD-Functional.Movement.CameraDisplacement` |
| M-08d | Obstruction recovery | ≤ 150 cm/s re-extension, monotonic, complete ≤ 0.6 s **[A1]** | `TDD-Functional.Movement.CameraRecovery` |
| M-08e | Lock-on acquisition | Whitelisted: 0.20 s, ≤ 120° total, ≤ 600°/s peak, ≤ 0.35 s **[A1]** | `TDD-Functional.Movement.CameraAcquisitionSlew` |
| M-09a | Dodge distance & clearance | Mean within 5 cm of resolved distance, σ ≤ 5 cm over 100 runs; capsule sweep includes radius; no penetration **[A1]** | `TDD-Functional.Movement.DodgeDistanceRepeatable` |
| M-09b | Dodge i-frame window | Boundaries at 0.10 s / 0.45 s ± 1 frame **[A1]** | `TDD-Functional.Movement.DodgeIFrames` |
| M-10 | (retired) | Merged into M-09b; ID kept reserved to avoid renumbering | — |
| M-11 | Player frame cost | ≤ 0.30 ms **[MEAD]** | Insights capture |
| M-12 | Device parity | ≤ 1 frame difference keyboard vs gamepad **[A1]** | `TDD-Functional.Movement.InputDeviceParity` |
| M-13 | Root-motion restoration | 100% restore after natural end, interruption, death and cinematic takeover **[A1]** | `TDD-Unit.Movement.RootMotionRestoresMovementMode`, `.RootMotionAppliesToCapsule` |
| M-14 | Traversal exit revalidation | 100% of exits validated against collision before snap; blocked exit → documented fallback, never teleport into geometry **[A1]** — M2 | `TDD-Functional.Movement.TraversalExitRevalidation` |

### 6.2 Automated tests (M1)

Aligned in v1.1 (C-09) with the authoritative specifications in M1 spec §5.

```
TDD-Unit.Movement.StateRulesComplete
TDD-Unit.Movement.StateSemantics            preconditions, forced transitions, exit actions, recovery
TDD-Unit.Movement.InputBuffer
TDD-Unit.Movement.CoyoteWindow
TDD-Unit.Movement.DodgeSpecMath
TDD-Unit.Movement.TurnRateMonotonic
TDD-Unit.Movement.RootMotionRestoresMovementMode
TDD-Unit.Movement.RootMotionAppliesToCapsule
TDD-Functional.Movement.LatencyL1
TDD-Functional.Movement.LatencyL2
TDD-Functional.Movement.LatencyL3
TDD-Functional.Movement.AcceleratesToMaxSpeed
TDD-Functional.Movement.StopsWithinDistance
TDD-Functional.Movement.Turn180Degrees
TDD-Functional.Movement.StepUpSupported
TDD-Functional.Movement.StepUpOverMaxBlocked
TDD-Functional.Movement.StepDownBehaviour
TDD-Functional.Movement.StepAngledApproach
TDD-Functional.Movement.SprintOverStep
TDD-Functional.Movement.CornerStability
TDD-Functional.Movement.SlopeLimits
TDD-Functional.Movement.CameraPenetration
TDD-Functional.Movement.CameraAngularStability
TDD-Functional.Movement.CameraDisplacement
TDD-Functional.Movement.CameraRecovery
TDD-Functional.Movement.CameraAcquisitionSlew
TDD-Functional.Movement.DodgeDistanceRepeatable
TDD-Functional.Movement.DodgeIFrames
TDD-Functional.Movement.DodgeRespectsCollision
TDD-Functional.Movement.InputDeviceParity
TDD-Functional.Movement.NoPermanentInputLock
TDD-Functional.Movement.LockOnStubStateIsConsistent
```

### 6.3 Reproducible manual procedures (physics/animation)

Documented as numbered procedures in the M1 spec, each with: purpose, setup (map, spawn, debug flags), exact input sequence, expected observations with tolerance, repetition count, and what to record. Hardware, build config, frame rate and input device must be recorded for every run, otherwise the run is invalid. "Feels good" is recorded as a qualitative note *alongside* the numbers, never instead of them.

---

## 7. Risks in my domain

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| G-1 | No engine in workspace → my code lands unverified, and debugging happens on someone else's machine | Critical | Small batches (one subsystem per handoff); pure-logic cores unit-tested first; M1 spec written so a build failure is cheap to locate |
| G-2 | No animation content; locomotion quality is the player's first impression | Critical | Mannequin-first M1; provider interface (ADR-0005) so clip sets can be swapped; measurement harness ready before clips arrive |
| G-3 | Empty animation/combat design folder → no move list, no weapon handling intent | High | MEAD §4.2 kit used as the *technical* contract only; M3 proceeds on placeholder clips clearly labelled; C-2 escalated as blocking |
| G-4 | Weapon grip/length unapproved → sockets and IK built on a guess | Medium | Length-agnostic socket scheme (`weapon_root`/`blade_base`/`blade_tip`) scaled from the mesh bounds at runtime; no hard-coded trace length |
| G-5 | Root motion vs CMC conflicts produce subtle bugs (movement mode leaks, capsule drift) | Medium | ADR-0013 policy + M-13 unit test + explicit restore in every root-motion path |
| G-6 | Motion Matching corpus may never arrive | High | BlendSpace provider shipped and playable in M1/M2; MM behind a setting (ADR-0005) |
| G-7 | Responsiveness claims drift into opinion | Medium | M-01a…M-14 thresholds; reports quote numbers or state "not measured" |
| G-8 | Scope creep into enemies/world (my boundary) | Medium | Interfaces published early so Agent 2 builds their own side; I never read AI state |
| G-9 | Character scale/proportions assumed wrong (height, capsule) | Low | Capsule dimensions and scale live in `DA_MovementConfig`, derived from the approved reference once a mesh exists |
| G-10 | Latency measured in frames is misread when frame rate changes | Medium | L1–L3 reported in frames **and** milliseconds at 60 and 120 FPS (v1.1, C-02); gameplay windows expressed in seconds, never frames |
| G-11 | Camera stability is judged by eye and regresses silently | Medium | Five separate automated criteria (penetration, angular jitter, displacement, recovery, acquisition) with per-mode thresholds instead of one blanket number (v1.1, C-04) |
| G-12 | Root-motion behaviour is assumed rather than verified (v1.0 made exactly this error with `MOVE_None`) | High | ADR-0013 v1.1 requires `RootMotionAppliesToCapsule` to prove capsule displacement on the first build; the mechanism is provisional until that test passes |
| G-13 | Step/edge geometry produces states the matrix does not describe | Medium | 50 cm blocked case, descent behaviour, angled/sprint/corner approaches added as first-class tests (v1.1, C-06) |

---

## 8. Staged implementation plan

Milestones map to the seven areas I was assigned. M0 is the prerequisite gate; M1 is the first practical milestone required by the assignment.

| # | Milestone | Scope | Depends on | Exit criteria (evidence) |
|---|---|---|---|---|
| **M0** | **Prerequisite gate** | Consume B-1…B-6; verify build, test run, CI; create my empty test map and metrics component skeleton | Agent 3 Phase 0 | Build + automation report exists; `L_TDD_Test_Movement` loads |
| **M1** | **Character controller, camera and movement** | CMC tuning, state machine and transition semantics, input pipeline and buffering, camera rigs and the five stability criteria, dodge, metrics harness | M0, stock mannequin | **Single gate, defined once in M1 spec §4: all AC-01…AC-31 pass** with quoted results (covering M-01a–c, M-02–M-04, M-06a–d, M-07, M-08a–e, M-09a/b, M-11–M-13); manual procedures **P1–P6** executed and recorded; reproducibility AC met over three cold runs (v1.1, C-01) |
| **M2** | **Movement and animation laboratory** | Animation provider integration (BlendSpace first), traversal (vault/mantle/ledge), foot-slide measurement (M-05), locomotion tuning against real/placeholder clips, turn-in-place, land/fall polish | M1 + C-1 clips | M-05 within threshold; traversal candidates validated and rejecting invalid ones; lab map with measurement overlays; MM provider evaluated and switched only if it meets thresholds |
| **M3** | **Combat foundation** | Combat component, attack data assets, state machine combat states, GAS attributes, damage pipeline to a dummy target, block/parry/dodge-cancel rules, posture/stagger, hitstop subsystem | M2 + placeholder attack clips + C-2 direction | Full player-vs-dummy loop (4-hit chain, heavy, block, parry, dodge, stagger, death); one damage path; `TDD-Unit.Combat.*` passes |
| **M4** | **Weapon and hit detection** | Weapon component, socket scheme, draw/holster, swept-capsule hit windows with substepping, dedup, classification (Hit/Blocked/Parried/Immune), warping targets | M3 + C-4 weapon confirmation | No double hits in any test; hit classification correct at window boundaries; M-10-style boundary accuracy for active windows |
| **M5** | **Combat feedback** | Hitstop feel pass, camera shakes, VFX/audio hook integration, haptics, state communication to UI | M4 | `TDD-Functional.Combat.FeedbackComplete`: every hit produces VFX + audio + camera cue within one frame; manual feel gate with CD |
| **M6** | **Enemy combat interaction** | `ITDDCombatant` finalisation, telegraph/timing contract, token participation, enemy attack fairness rules with Agent 2, stagger/damage exchange in both directions | M5 + Agent 2's AI stack | Player can be hit, staggered and killed by an enemy; enemy can be parried/staggered by player; shared timing contract documented and tested |
| **M7** | **Integration and gate** | Chapter 1 blockout integration, performance validation on reference hardware, full regression | M6 + Agent 2 world | All my metrics within threshold in a real chapter scene; no boundary violations; phase report complete |

Effort is not estimated in days here: without a build loop, calendar estimates would be fiction. Relative sizing only — M1 and M3 are the two largest engineering efforts; M4–M6 are moderate; M0 is small but externally gated.

### 8.1 Why M1 is defined the way it is

The assignment requires "a responsive, testable third-person character controller in a controlled test environment". That means M1 is not "the character moves". It is:

1. Movement that meets **measured** responsiveness thresholds, not vibes.
2. A camera that provably cannot clip through geometry in a corridor and cannot jitter.
3. A state machine whose transition table is exhaustively tested.
4. A test environment that reproduces specific physics conditions (flat, slope, steps, corridor, drop) and a harness that prints numbers.
5. Instrumentation that stays in the build and gates every later milestone.

If M1 is done properly, M3 (combat) is mostly new components plugged into an already-measured foundation. If M1 is skipped, every later combat feature inherits an unmeasurable control feel and the project debates it forever.

---

## 9. Reporting protocol

Every milestone report from me contains, in this order: files created/modified; systems implemented with a status from `STATUS_AND_CLAIMS.md`; interfaces exposed and consumed; dependencies and blockers; **tests executed with actual results quoted** (not summarised); known limitations; performance observations with capture reference; evidence bundle pointers; next proposed milestone.

Rules I hold myself to:
- A test that could not run is reported as "not run (reason)", not omitted.
- A threshold that was missed is reported as a miss with the measured value. A near-miss is a miss.
- Any placeholder is named (`PLACEHOLDER-A1-<n>`) and listed in the report.
- No feature is "complete" until its acceptance criteria are met and evidence exists.

---

## 10. Status claim table (honest state at this timestamp)

| Item | Status | Evidence |
|---|---|---|
| Gameplay and Character Technical Assessment | `DESIGN_ONLY` — **v1.1 revised per TD review; awaiting re-review** | This file (v1.0 archived) |
| M1 implementation specification | `DESIGN_ONLY` — v1.1 revised; awaiting re-review | `M1_MOVEMENT_SPECIFICATION.md` (v1.0 archived) |
| Root motion policy | `DESIGN_ONLY` — ADR-0013 **v1.1**, mechanism provisional pending `RootMotionAppliesToCapsule` | `docs/03_DECISIONS/ADR-0013-root-motion-policy.md` |
| `ETDDCombatState`, `FTDDPawnKinematics` | **Proposed contracts only** — pending Agent 3 Core review; **not created by Agent 1** (v1.1, C-12) | M1 spec Appendix A |
| Player character, controller, camera, combat, weapon, traversal code | **Does not exist** — no implementation begun, per TD instruction | — |
| Any gameplay test | **Cannot run** | No engine in workspace (ADR-0012) |
| Any measurement (M-01a…M-14) | **Not measured** | Requires UE 5.8 reference hardware |
| Prerequisites B-1…B-6 | `BLOCKED` on Agent 3 | §3.1 |
| Content prerequisites C-1…C-5 | `BLOCKED` externally | §3.2 |

**Statement to the Technical Director:** I have delivered the assessment and the M1 specification, and I have published the interfaces Agent 2 needs before they build enemy behaviour. I have not written unverifiable C++ into an empty repository; doing so would create debugging debt with no way to discharge it. The moment B-1…B-6 exist on a UE 5.8 machine, M1 implementation begins with the pure-logic cores (state rules, input buffer, dodge maths) which are the parts most likely to be silently wrong and least likely to be caught by eye.

---

## 11. Change log — v1.0 → v1.1 (response to Technical Director review, 2026-11-16)

The TD review accepted the architecture and milestone approach in principle and required the following corrections before implementation. Each correction is listed with what was wrong, what changed and where. v1.0 is preserved at `archive/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT_V1.0.md`.

| ID | Review item | What was wrong in v1.0 | Correction in v1.1 | Where |
|---|---|---|---|---|
| **C-01** | 1 — Reconcile M1 exit criteria | §8's M1 row listed a *subset* of metrics (M-01…M-04, M-08…M-13) and P1–P3, while the spec defined 20 ACs and P1–P5. Two different gates for one milestone | Removed the partial list. There is now **one gate**: "all AC-01…AC-31 in M1 spec §4 pass", with the metric table explicitly labelled as a summary that maps to the ACs. Manual procedures corrected to P1–P6 in both documents | §6.1, §8 |
| **C-02** | 2 — Separate latency stages; resolve same-frame/next-frame | v1.0 asserted "animation evaluates after movement, so the pose lags one frame" as engine fact, while its own AC required a same-frame velocity delta. Two contradictory claims | Claim withdrawn. Latency split into **L1 sample→intent, L2 intent→first velocity change, L3 intent→pose**, each with a frame-index definition, expected value (**L2 = 0**, L1 ≤ 1, L3 ≤ 1 measured not predicted) and a measurement rule at **60 and 120 FPS** reported in frames *and* ms | §4.5 |
| **C-03** | 7 — Input-component ownership | v1.0 implied the controller owned input routing while the input component subclass was on the pawn, without explaining the lifecycle | Documented the Unreal lifecycle: `PawnClientRestart → SetupPlayerInputComponent` with the component from `CreatePlayerInputComponent`, class controlled by `InputComponentClass`; pawn owns gameplay bindings, controller owns only pause/menu bindings | §4.3 |
| **C-04** | 4 — Camera stability; 7 — camera ownership | One blanket rule ("no snap faster than 720°/s") conflated penetration, jitter, pop, recovery and intentional acquisition; camera manager and rig were described as one unit | Five separate criteria with per-mode thresholds (10 cm penetration; 6°/frame + 3°/frame² jerk; 10/25/15 cm-frame displacement; 150 cm/s recovery; whitelisted 0.20 s acquisition ≤ 600°/s). Ownership split documented: manager on PC, rig component on pawn, Sequencer takeover handled explicitly | §4.7, §6.1 |
| **C-05** | 8 — Root motion, collision, interruption, restoration | v1.0 proposed `MOVE_None` for root-motion montages *assuming* CMC would still apply anim root motion, and snapped traversal to the exit transform without revalidation; 300 cm/60° presented as fixed | `MOVE_None` withdrawn as an assumption; ADR-0013 v1.1 specifies the execution model, requires `RootMotionAppliesToCapsule` to prove displacement, adds interruption/restoration checklist, traversal exit revalidation, and makes warp limits configurable per attack | §4.6, §4.8, ADR-0013 v1.1 |
| **C-06** | 5 — State transition semantics | v1.0 specified a 14×14 "allowed" matrix plus column notes; v1.1 needs preconditions, forced transitions, interruption, exit actions and recovery as first-class rules | Spec §3.2 expanded (priority order, forced vs requested, interruption windows, exit checklist, recovery conditions, min dwell). Assessment §`4.2` refers to it as authoritative and adds the missing 50 cm/descent/angled/sprint/corner cases to the test plan | §4.2, §6.2, spec §3.2 |
| **C-07** | 3 — Dodge clearance | Formula subtracted `CapsuleRadius` from a "clearance" whose shape was undefined, double-counting the radius and leaving units ambiguous | Restated precisely: **capsule-shaped sweep using the CMC capsule dimensions**, so the radius is already included and is *not* subtracted; margin only; explicit channel, ignored actors, `bStartPenetrating` refusal, planar Z handling, and CMC as final collision authority | spec §3.5, §4 (AC-19/21) |
| **C-08** | 4/6 — Metric coverage | Metric IDs were too coarse (one camera metric, one step metric, one latency metric) | Split to M-01a/b/c, M-06a–d, M-08a–e, M-09a/b, added M-13 (restoration incl. interruption) and M-14 (traversal exit revalidation); M-10 retired with a note so IDs do not shift | §6.1 |
| **C-09** | 1/6 — Test list consistency | Test names in the assessment did not match the spec, and the edge-case tests did not exist | Test list regenerated from the spec (33 tests), including the new step-descent, 50 cm-blocked, angled, sprint, corner, camera-recovery and latency-stage tests | §6.2 |
| **C-10** | 6 — Step 50 cm expectation | The spec listed a 50 cm step in the test map with no expected outcome | Expected outcome now defined as **blocked and stable** (net Z gain ≤ 1 cm over 5 attempts, speed ≤ 5 cm/s after contact, no Airborne, no penetration), with descent and approach-angle behaviour specified | §6.1, spec §4/§5 |
| **C-11** | 9 — Core types | Appendix A could read as an instruction to create `TDDCore` types | Restated as **proposals pending Agent 3's Core review**; Agent 1 will not create competing Core types, and will adapt rather than fork if the shape changes | spec Appendix A |
| **C-12** | Review header | No version history; originals not preserved | Versioned to v1.1, v1.0 archived unchanged, this change log added to both revised documents and to ADR-0013 | Header, this section |

### Unchanged by this revision

Inspection findings (§1), gap analysis (§2), prerequisites B-1…B-6 and content prerequisites C-1…C-5 (§3), the class map (§4.1), input mappings (§4.3 table), data assets (§4.4), traversal architecture (§4.8), combat summary (§4.9), interfaces (§5), risks G-1…G-9, milestones M0 and M2–M7, and the reporting protocol (§9) stand as reviewed and accepted in principle.

### Status after revision

Still **no implementation, no compilation, no test execution, and no measurement**. This revision changes specification only. `DESIGN_ONLY` remains the correct status for every item in §10.
