# M1 — Execution Scope, Stage Gate and Verification Process v1

**Purpose:** turn M1 from "a maths helper" into a playable Adanna, in ordered stages that each end in a build and a test result. Written by Agent 1 for Agent 3 (implementation) and Agent 2 (review) to agree or amend.
**Basis:** `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` **v1.4** (TDD-A1-M1-SPEC-001) — AC-01…AC-31, tests M-01…M-13, manual procedures P1–P6, test map §7. **This document adds no new movement rules**; where the spec already decides something it is cited, not restated.
**Canonical tree:** `arena/c64fc525-tdd` @ `e71401b6`. M0 passed (see `M0_VERIFICATION_RECORD_V1.md`).
**Status:** proposal, pending Agent 3 agreement and Agent 2 review.

## 1. What exists in the canonical tree today

| Item | State |
|---|---|
| `TheDisobedientDaughter.uproject` + one runtime module | present, builds on Mac |
| `TDDGameMode` (`Config/DefaultEngine.ini` → `GlobalDefaultGameMode`) | present, automation-covered |
| `Movement/TDDDodgeDistanceMath.h` + `ResolveDodgeDistance` | present, 18/18 standalone assertions, **`TDD.Movement.DodgeDistanceMath` green in-engine** |
| `Movement/TDDDodgeSweep.{h,cpp}` | present; **no automation test, no world, never exercised** |
| Player character, camera, input, test map, animation | **absent** |

The honest position: one pure function is verified. No mechanic exists yet.

## 2. Stages — each one ends in a build plus a result

Each stage is independent enough to land as its own commit on `arena/c64fc525-tdd`, and is not "done" until Agent 1 has a green Mac run and Agent 2 has reviewed the diff.

| # | Deliverable | Spec | Closes |
|---|---|---|---|
| S1 | `TDDDodgeSweep` against a real world: capsule sweep using the **CMC's own capsule**, `ECC_Pawn`, owner ignored, planar Z, `bStartPenetrating` → refuse | §3.5 | AC-19 (radius counted once), AC-21 (refusal) |
| S2 | Destination-floor validation + the specified floor-distance correction (≤ 3 iterations, planar) | §3.5, §3.7 | AC-21 |
| S3 | `ATDDPlayerCharacter` + CMC wiring; dodge drives real movement, montage/root motion, prior mode restored on natural end, abort, death, cinematic | §3.1, §3.2 | AC-26, AC-29 |
| S4 | Interruption and collision edge cases: blocked en route → clamped distance; no per-frame penetration; movement mode restored | §3.5, §3.2 | AC-21, AC-22, AC-23 |
| S5 | Third-person camera with the five stability criteria | §3.6 | AC-14…AC-18 |
| S6 | Input: Enhanced Input actions/contexts, buffering, coyote window, device parity | §3.4 | AC-24, AC-25, AC-27 |
| S7 | `L_TDD_Test_Movement` zones `Z_Flat`, `Z_Dodge`, `Z_Steps`, `Z_Corridor1/2` (`PlayerStart` per zone) | §7 | enables the functional ACs |
| S8 | First playable Adanna: launch → control → traverse → obstacle → movement actions → interact | §9 + §4 of the director's M1 brief | proposed gate below |

**Do not reorder S1–S2 behind S5–S7.** Clearance and floor validation are what make the movement trustworthy; camera and input feel are worthless on a controller whose dodge clips walls.

## 3. Acceptance criteria

**Existing, unchanged — do not renumber:** AC-19…AC-31 as specified in v1.4 §4. Each has a named automation test in §5 and, where it is a feel criterion, a manual procedure in §6.

**First-playable gate — proposed, needs Technical Director sign-off** (the spec's §9 definition of done is stricter than "playable", so this is an explicit intermediate gate, not a replacement):

| ID | Criterion (the director's own wording, made checkable) | Verified by |
|---|---|---|
| `M1-P1` | A player can launch the game: `TheDisobedientDaughter` **packaged Development** build starts to the test map without a fatal error | package + launch log (Gate D, currently `NOT RUN`) |
| `M1-P2` | A player can control Adanna: walk/jog/sprint move the capsule on the pressed frame | P1 procedure + `TDD-Functional.Movement.LatencyL1` |
| `M1-P3` | A real 3D environment: the test map loads with floor, walls and the zones of §7 | automation map-load assertion + P1 |
| `M1-P4` | Navigate obstacles and perform implemented movement actions: 45 cm step climbs, 50 cm refuses, dodge respects geometry | AC-07/AC-08/AC-21 + P3 |
| `M1-P5` | Interact with the world: one interaction volume in the map responds to an input and reports it in the log | new automation test `TDD.Movement.InteractSmoke` (name to be agreed) |

`M1-P1` is deliberately included because "launch the game" cannot be satisfied by an editor session; it stays `BLOCKED` until packaging is in scope.

## 4. Verification process (the part that has been missing)

1. **Test naming** — `TDD.<Area>.<Subject>`, flags `EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter`, `#if WITH_DEV_AUTOMATION_TESTS` around the unit. The canonical runner discovers by prefix, so a mis-flaggued test silently does not run; Agent 1 checks discovery counts on every run.
2. **Per-commit, on the Mac:**
   ```bash
   Tools/engine/mac_build.sh --engine "/Users/Shared/Epic Games/UE_5.8" --test-filter TDD
   ```
   `0` exit = both targets built and the queue ran. Any other exit is a failure to report as such.
3. **Evidence** — `Saved/BuildEvidence/<UTC>/` plus `automation-report/index.json`; the machine-readable report is what Agent 2 reviews, so archive it per `M0_VERIFICATION_RECORD_V1.md` §5.
4. **Feel criteria** — manual P1/P3 with the overlay and CSV; impressions labelled as impressions.
5. **Sign-off per stage** — Agent 3 implements and self-tests; Agent 1 produces build + automation evidence; Agent 2 reviews the diff and the report; the owner runs the Mac command. No stage is "complete" on standalone tests alone.

## 5. Dependencies and blockers

| Dependency | Owner | Status |
|---|---|---|
| **This spec is not in the canonical branch.** `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` lives on `arena/3bc206a0-tdd` | Agent 3 or owner | **blocking Agent 3's ability to cite §3.5/AC-19 in-tree**; copy it, do not re-derive it |
| `EnhancedInput` module (S6) | Agent 3 | must be added to `TheDisobedientDaughter.Build.cs` **and** the plugin enabled before input code compiles |
| Character mesh/skeleton, dodge montage (S3) | art pipeline | absent; root-motion tests need one authored montage first |
| `L_TDD_Test_Movement` (S7) | Agent 3 | must be authored **in the editor on the Mac**; it cannot be produced headlessly here |
| Packaging for `M1-P1` | owner + Agent 1 | `NOT RUN`; needs a packaging decision and the same Mac |
| TD decisions: TD-06, TD-09, TD-12 | Technical Director | unresolved and **not to be resolved by this work**; L-2 remains CLOSED |

## 6. Immediate next actions

1. **Agent 3** — land S1 as a commit that adds a world-bound sweep test (a minimal `UWorld`, a wall actor, one blocked and one clear case) so `TDDDodgeSweep` stops being unverified code. Name it `TDD.Movement.DodgeSweepBlocked` / `…DodgeSweepClear`.
2. **Agent 3** — copy the v1.4 spec into the canonical tree (`docs/02_PRODUCTION/AGENT1/`), committing it unchanged, so reviews cite a path that exists.
3. **Agent 1** — on the next canonical commit, run the readiness check and the Mac command as soon as the owner reports a new SHA.
4. **Agent 2** — review with the gate table in §3 as the checklist, and treat `TDD.Foundation.GameModeClass` + `TDD.Movement.DodgeDistanceMath` as the only verified behaviour so far.
