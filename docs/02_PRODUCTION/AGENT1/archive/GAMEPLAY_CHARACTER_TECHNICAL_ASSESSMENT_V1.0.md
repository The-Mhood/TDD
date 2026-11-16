# GAMEPLAY AND CHARACTER TECHNICAL ASSESSMENT

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Agent:** 1 — Gameplay, Character and Combat Engineering
**Document:** TDD-A1-ASSESS-001
**Version:** 1.0
**Date:** 2026-11-16
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

### 4.3 Input mapping (full, to be realised in B-4)

Mapping contexts: `IMC_Exploration`, `IMC_Combat`, `IMC_LockOn`, `IMC_Cinematic`, `IMC_Menu`, `IMC_Traversal`. Only one gameplay context + `IMC_Menu` overlap is legal; the state machine requests context switches.

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

### 4.5 Tick ordering and the responsiveness budget

This is where responsiveness is won or lost, so it is specified rather than discovered:

```
Frame N:
  TG_PrePhysics    : PlayerController input sampling (Enhanced Input)
                     → intent produced → state machine decision
  TG_PrePhysics    : CharacterMovementComponent tick (applies accel, moves capsule)
  TG_PostPhysics   : SkeletalMesh animation update (pose for the moved capsule)
  TG_PostPhysics   : camera update (follows the moved capsule)
```

Consequence: the pose the player sees at frame N reflects movement computed at frame N — good — but the *animation* responding to a new intent appears at N+1 because animation evaluates after movement. Floor latency: **one frame** (16.7 ms at 60 fps).

Two measured options, decided by data, not opinion:
- **Default:** mesh ticked in `TG_PostPhysics` (UE default). Correctness first: no foot slide introduced by ordering.
- **Option B (tunable):** `SkeletalMeshComponent` tick group set to `TG_PrePhysics` so the pose uses the *previous* frame's velocity, reducing perceived input latency at the cost of slightly increased foot slide. Only adopted if measurement shows a real perceptual gain and the slide budget (M2) still holds.

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
| Dodge | **Yes**, authored distance, capped by trajectory sweep | Precise, repeatable distances; validated against collision before playing, with fallback distance if blocked |
| Attacks with a lunge | **Yes**, with Motion Warping to the target (≤ 300 cm, ≤ 60°) | Alignment quality; root motion supplies the travel, warping supplies the aim |
| Stationary attacks | **No** (in-place clip) | Avoids drift; damage comes from windows, not translation |
| Traversal (vault/mantle) | **Yes** + Motion Warping entry/exit alignment | Quality of alignment; capsule is locked to CMC during the clip and snapped to the validated end transform |
| Cinematics | **Yes**, with the capsule frozen and restored on exit | Standard cinematic practice |
| Hit reactions | **No** for small reactions; **Yes** for knockdowns | Predictability; knockdowns need authored displacement |

Engine configuration implied: `AnimInstance->SetRootMotionMode(ERootMotionMode::RootMotionFromMontagesOnly)`; `bAllowPhysicsRotationDuringAnimRootMotion=false`; movement mode set per action (CMC `MOVE_None` or custom during root-motion montages) with explicit restoration; every root-motion action validated by `TDD-Unit.Movement.RootMotionRestoresMovementMode`.

### 4.7 Camera architecture

`ATDDPlayerCameraManager` + `UTDDCameraRigComponent` with named rigs:

| Rig | Offset / arm | FOV | Use |
|---|---|---|---|
| `Explore` | shoulder (0, 45, 65), arm 320 cm | 90° | Default |
| `CombatSoft` | (0, 55, 60), arm 380 cm | 95° | Enemies within 12 m, no lock |
| `LockOn` | framing both actors, screen-space bias 0.35 | 95° | Hard lock |
| `Traversal` | pulled back/down, wider | 90° | Mantle/vault |
| `Cinematic` | Sequencer owns it | per shot | Blended in/out over 0.4 s |

Rules: collision probe with a sphere sweep (radius 12 cm) on the boom; no camera snap faster than 720°/s except on explicit lock-on acquisition (which is a deliberate, authored snap with a short blend); pitch clamped [-60°, +45°] in exploration and [-50°, +35°] in combat; camera shake from data assets only. Lock-on scoring and hysteresis per MEAD §4.3.

Camera feel is a manual (T5) gate; camera *correctness* (no wall penetration, no jitter, blend durations, FOV limits) is automated.

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

Everything subjective in this domain becomes a number here. Thresholds marked **[MEAD]** come from the governing document; **[A1]** are my proposals and need Technical Director sign-off.

| ID | Metric | Threshold | Method |
|---|---|---|---|
| M-01 | Time from input to movement intent accepted | 1 frame | Automation: press move, assert velocity delta on the same frame's CMC tick |
| M-02 | Time to reach 95% max jog speed from idle | ≤ 0.35 s **[MEAD]** | Automation samples speed per frame; CSV curve exported |
| M-03 | Time to stop from max jog | ≤ 0.20 s and ≤ 50 cm **[A1]** | Automation |
| M-04 | 180° turn at max jog speed | ≤ 0.50 s, foot slide ≤ 5 cm **[MEAD]** | Automation (capsule) + M2 animation sockets (slide) |
| M-05 | Foot slide per metre travelled | ≤ 5 cm at 60 fps **[MEAD]** | M2 only: foot socket vs capsule delta, per-frame log |
| M-06 | Step-up height | 45 cm at walk speed, no capsule pop > 2 cm/frame **[A1]** | Automation on a step test map |
| M-07 | Walkable slope | 40° traversable, 50° blocked, no jitter **[A1]** | Automation + manual sweep |
| M-08 | Camera wall penetration | Zero penetrations within 30 cm of geometry over a 60 s scripted sweep **[A1]** | Automation (sweep trace) in a corridor test map |
| M-09 | Dodge distance repeatability | Authored distance ± 5 cm over 100 runs on flat ground **[A1]** | Automation loop |
| M-10 | i-frame window accuracy | Boundary at 0.10 s / 0.45 s ± 1 frame **[A1]** | Automation reads invulnerability tag per frame |
| M-11 | Player frame cost | ≤ 0.30 ms **[MEAD]** | Insights capture, Development build, reference hardware |
| M-12 | Input device parity | Same action timings within 1 frame on keyboard vs gamepad **[A1]** | Automation with synthesised device input |
| M-13 | Root-motion movement-mode restoration | 100% of root-motion actions restore the prior movement mode **[A1]** | `TDD-Unit.Movement.RootMotionRestoresMovementMode` |

### 6.2 Automated tests (M1)

```
TDD-Unit.Movement.StateRulesComplete          every state pair either declared or asserted illegal
TDD-Unit.Movement.InputBuffer                 buffer/coyote windows, expiry, consumption
TDD-Unit.Movement.DodgeSpecMath               distance/duration/i-frame conversion per time dilation
TDD-Unit.Movement.TurnRateMonotonic           turn never overshoots target yaw
TDD-Functional.Movement.AcceleratesToMaxSpeed M-02
TDD-Functional.Movement.StopsWithinDistance   M-03
TDD-Functional.Movement.Turn180Degrees        M-04
TDD-Functional.Movement.StepUp45cm            M-06
TDD-Functional.Movement.SlopeLimits           M-07
TDD-Functional.Movement.CameraNoWallPenetration M-08
TDD-Functional.Movement.DodgeDistanceRepeatable M-09
TDD-Functional.Movement.DodgeIFrames          M-10
TDD-Functional.Movement.InputLatencyOneFrame  M-01
```

Functional tests live in `L_TDD_Test_Movement` (owned by me), use `FAutomationSpec`/Functional Testing, and must pass with the platform-independent metric harness. Every test writes a machine-readable result line so the phase report can quote it.

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
| G-7 | Responsiveness claims drift into opinion | Medium | M-01…M-13 thresholds; reports quote numbers or state "not measured" |
| G-8 | Scope creep into enemies/world (my boundary) | Medium | Interfaces published early so Agent 2 builds their own side; I never read AI state |
| G-9 | Character scale/proportions assumed wrong (height, capsule) | Low | Capsule dimensions and scale live in `DA_MovementConfig`, derived from the approved reference once a mesh exists |
| G-10 | Single-frame latency floor disappoints on a 30 fps machine | Low | Documented explicitly; frame-rate-dependent tuning avoided by using seconds, not frames, for gameplay windows |

---

## 8. Staged implementation plan

Milestones map to the seven areas I was assigned. M0 is the prerequisite gate; M1 is the first practical milestone required by the assignment.

| # | Milestone | Scope | Depends on | Exit criteria (evidence) |
|---|---|---|---|---|
| **M0** | **Prerequisite gate** | Consume B-1…B-6; verify build, test run, CI; create my empty test map and metrics component skeleton | Agent 3 Phase 0 | Build + automation report exists; `L_TDD_Test_Movement` loads |
| **M1** | **Character controller, camera and movement** | CMC tuning, state machine, input pipeline and buffering, camera rigs, dodge, metrics harness, `TDD-Unit.Movement.*` + core `TDD-Functional.Movement.*` | M0, stock mannequin | M-01…M-04, M-08…M-13 measured and within threshold; manual procedure P1–P3 signed off; **responsive testable controller in a controlled environment** |
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
| Gameplay and Character Technical Assessment | `DESIGN_ONLY` (complete as a document; unapproved) | This file |
| M1 implementation specification | `DESIGN_ONLY` | `M1_MOVEMENT_SPECIFICATION.md` |
| Root motion policy | `DESIGN_ONLY` (proposed ADR-0013) | `docs/03_DECISIONS/ADR-0013-root-motion-policy.md` |
| Player character, controller, camera, combat, weapon, traversal code | **Does not exist** | — |
| Any gameplay test | **Cannot run** | No engine in workspace (ADR-0012) |
| Any measurement (M-01…M-13) | **Not measured** | Requires UE 5.8 reference hardware |
| Prerequisites B-1…B-6 | `BLOCKED` on Agent 3 | §3.1 |
| Content prerequisites C-1…C-5 | `BLOCKED` externally | §3.2 |

**Statement to the Technical Director:** I have delivered the assessment and the M1 specification, and I have published the interfaces Agent 2 needs before they build enemy behaviour. I have not written unverifiable C++ into an empty repository; doing so would create debugging debt with no way to discharge it. The moment B-1…B-6 exist on a UE 5.8 machine, M1 implementation begins with the pure-logic cores (state rules, input buffer, dodge maths) which are the parts most likely to be silently wrong and least likely to be caught by eye.
