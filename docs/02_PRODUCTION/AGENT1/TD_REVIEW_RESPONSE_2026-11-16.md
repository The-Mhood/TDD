# Response to Technical Director review — 2026-11-16

**From:** Agent 1 (Gameplay, Character and Combat Engineering)
**To:** Technical Director
**Subject:** Revision of the Gameplay/Character Assessment, M1 Specification and ADR-0013 following review
**Status:** `DESIGN_ONLY`. No implementation begun. Nothing compiled, executed or measured.

---

## 1. What was done

All nine review items are addressed. Originals preserved; revised documents versioned; each carries its own change log.

| Document | Path | Version | Original preserved at |
|---|---|---|---|
| Gameplay and Character Technical Assessment | `docs/02_PRODUCTION/AGENT1/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT.md` | **v1.1** (log §11) | `docs/02_PRODUCTION/AGENT1/archive/GAMEPLAY_CHARACTER_TECHNICAL_ASSESSMENT_V1.0.md` |
| M1 Movement Specification | `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` | **v1.1** (log §13) | `docs/02_PRODUCTION/AGENT1/archive/M1_MOVEMENT_SPECIFICATION_V1.0.md` |
| ADR-0013 Root motion | `docs/03_DECISIONS/ADR-0013-root-motion-policy.md` | **v1.1** (revision history §12) | `docs/03_DECISIONS/archive/ADR-0013-root-motion-policy_V1.0.md` |

## 2. Item-by-item resolution

| # | Review requirement | Resolution | Where |
|---|---|---|---|
| 1 | Reconcile M1 exit criteria into one gate | Single authoritative gate: **AC-01…AC-31**. Assessment §8 now *references* it instead of listing a partial metric subset; P1–P3/P1–P5 mismatch fixed to **P1–P6** in both documents. AC renumbering map included for traceability | spec §4, §9, §13; assessment §8, §11 |
| 2 | Separate input-sampling from intent-to-velocity latency; resolve same/next-frame; measure at 60 and 120 FPS | Three stages: **L1** sample→intent (≤ 1 frame; 0 in harness), **L2** intent→first velocity change (**0 frames, hard requirement**), **L3** intent→pose (≤ 1 frame, **measured not predicted**). v1.0's contradictory "one-frame animation floor" claim is withdrawn explicitly. Measurement protocol includes mid-frame worst case, frame counters, vsync state, substepping state, results in frames *and* ms, and device-to-photon declared out of engine scope | spec §3.4, AC-01…03; assessment §4.5 |
| 3 | Correct dodge collision clearance; state geometry and radius handling | Capsule sweep using the **CMC's exact capsule** (`MakeCapsule(R,H)`); radius is inside the shape so it is **counted once and not subtracted**; only a 2 cm margin deducted. Channel `ECC_Pawn`, owner/lock-target ignored, planar Z, floor check with ≤ 3 iterations, `bStartPenetrating` → **refuse the dodge**, CMC remains collision authority. A unit test asserts the radius is not double-counted, including the rejected ray variant | spec §3.5, AC-19/21 |
| 4 | Separate the camera failure modes; replace the 720°/s rule | Five criteria with distinct thresholds and event flags: **penetration** 10 cm; **angular jitter** 6°/frame + 3°/frame² + ≤ 3 sign flips per 10 frames; **displacement** 10 / 25 / 15 cm per frame (normal / obstructed / unflagged); **recovery** 150 cm/s monotonic, ≤ 0.6 s; **acquisition** whitelisted 0.20 s, ≤ 120°, ≤ 600°/s. 720°/s retained only as the acquisition ceiling. Rationale and tuning status stated | spec §3.6, AC-14…18; assessment §4.7 |
| 5 | Preconditions, interruption, forced transitions, exit behaviour, recovery | Two per-state tables (entry/exit/recovery/dwell; forced/interruption/buffer policy) plus global rules: priority order, forced-vs-requested, exit checklist executed on **every** exit including aborts, buffer policy, min dwell, no-permanent-lock rule. Two unit tests cover pair completeness **and** semantics | spec §3.2, AC-22/23 |
| 6 | 50 cm step outcome; add descent, angled, sprint, corner cases | 50 cm defined as **blocked and stable** (net Z ≤ 1 cm over 5 attempts, speed ≤ 5 cm/s after contact, no Airborne, no penetration, no oscillation). Added: descent 15/30/45 (no Airborne) vs 50 (Airborne + recovery), angled 30/45/60°, sprint-over-45 cm with speed retention, inside/outside corners, dodge-into-step | spec §4, §5, §7; AC-07…12 |
| 7 | Resolve input and camera ownership; explain the Enhanced Input lifecycle | Input: documented `Possess → PawnClientRestart → CreatePlayerInputComponent → SetupPlayerInputComponent`, `InputComponentClass`, pawn-owned gameplay bindings, controller-owned pause/menu component, contexts pushed/popped on possess/unpossess, component absent before possession. Camera: manager (PC-owned, shakes/modifiers) vs rig component (pawn-owned, desired rig only) vs spring arm (pawn) vs Sequencer takeover | spec §3.1, §3.6; assessment §4.3, §4.7 |
| 8 | ADR-0013: execution, collision, interruption, restoration; verify `MOVE_None`; revalidate traversal exit; keep warp limits provisional | `MOVE_None` **withdrawn and prohibited** for root-motion actions because CMC may not process root motion in a mode where its movement update does not run. Execution table now names modes in which the update runs (`MOVE_Walking`, `MOVE_Flying` for vertical traversal). Mechanism is **provisional** until `RootMotionAppliesToCapsule` proves displacement within 5%, with three documented fallbacks (A/B/C) chosen by measurement. Collision authority assigned to CMC; pre-sweeps demoted to predictions; no direct capsule writes. Nine-step restoration checklist on every path incl. interruption/death/cinematic/EndPlay. Traversal exit revalidated against current collision incl. dynamic actors, with defined fallback. Warp limits configurable per attack, defaults provisional | ADR-0013 v1.1 §2–§7; spec §3.5, §3.7, AC-26 |
| 9 | Keep `ETDDCombatState` / `FTDDPawnKinematics` as proposals; create no competing Core types | Appendix restated as **PROPOSED — pending Agent 3 Core review**, with an explicit statement that Agent 1 creates no Core types and will adapt rather than fork; change-request log field added | spec Appendix A; assessment §5.2 |

## 3. Things I chose not to do, and why

- **No implementation code.** Per instruction, and per ADR-0012: unverifiable code in an empty repo creates debt with no way to discharge it.
- **No claim that root motion now works.** The revision makes the mechanism *testable*, not proven. Until `RootMotionAppliesToCapsule` runs, the mechanism is a hypothesis with a fallback plan.
- **No invented animation or combat content.** The `09_ANIMATION_AND_COMBAT` folder is still empty; M2+ remains blocked on C-1/C-2.
- **No silent rewrites.** v1.0 files are preserved byte-identical in `archive/` so the review trail is auditable.

## 4. Decisions I need from you (blocking or shaping)

1. Accept the single gate AC-01…AC-31 as the definition of M1 completion.
2. Is a measured **L3 = 1 frame** acceptable if the M2 foot-slide budget still holds, or is a mesh tick-group change mandatory?
3. Approve the camera first-pass thresholds (they are proposals; I expect tuning against real captures).
4. Confirm a **50 cm step is intended to be impassable** at `MaxStepHeight = 45 cm`.
5. Confirm dodge refusal when starting inside geometry (no cooldown consumed).
6. Confirm the ADR-0013 v1.1 execution model and its provisional status.
7. Confirm attack warp limits stay configurable with provisional defaults.
8. Approve or replace the proposed `TDDCore` types — Agent 2 is waiting on these to start enemy work.

## 5. Unchanged blockers

B-1…B-6 (Agent 3 scaffolding, build and CI) and C-1…C-5 (animation/combat content and weapon confirmation) remain open. M1 implementation cannot start until B-1…B-6 exist on a UE 5.8 workstation.
