# AGENT 2 — Independent Implementation Review: M1 §3.5 Dodge Clearance & AC-19

**Deliverable:** `AGENT2_VERIFY_M1_DODGE_REVIEW_V1.md`
**Reviewer role:** Agent 2 — independent implementation review (assess/verify, does not implement).
**Review target:** commit `dab65e57ad03d2b8632c8f6172fb37d958c6b00c`, branch `arena/c64fc525-tdd` (canonical per directive).
**Review bar:** `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` §3.5 (dodge clearance calculation) and AC-19 (dodge distance/clearance determinism), authored on Agent 1's branch `origin/arena/3bc206a0-tdd`.
**Session branch:** `arena/5dde91a4-tdd` (review committed here; no code changes made to the target).
**Verification basis:** source inspection + independent standalone compile/run. **No Unreal toolchain exists in the sandbox** (blocker B-3); the UE `.cpp` was **not compiled or executed in Unreal** — see "Unreal verification: BLOCKED".

---

## 0. Scope and method

This review is **code review only**. I read the published tree at `dab65e5`, extracted it read-only, and reviewed the dodge implementation against M1 §3.5 / AC-19. I independently compiled and ran the **pure-math** standalone test (`Tests/Standalone/TDDDodgeDistanceMathTests.cpp`) — it is host-compiler C++ with no Unreal dependency — which returned **18/18 assertions passed, exit 0** (confirmed by me, not merely reported). I did **not** compile or run any Unreal module; that is impossible here.

The canonical branch now **does** contain a Unreal project and a dodge implementation. Earlier premises in the directive (docs-only branch, no `.uproject`) were **superseded** by commits `4667a8f` (foundation), `9714583` (consolidation), `502a9e4` (dodge math), `66cc31d` (capsule sweep), `dab65e5` (Mac build preflight) — all now present at `dab65e5`.

**Files reviewed (at `dab65e5`):**
- `Source/TheDisobedientDaughter/Public/Movement/TDDDodgeDistanceMath.h` — `ResolveDodgeDistance` pure-math helper.
- `Source/TheDisobedientDaughter/Private/Movement/TDDDodgeSweep.cpp` / `.h` — `ResolveDodgeSweep` capsule sweep.
- `Source/TheDisobedientDaughter/Private/Tests/TDDDodgeDistanceMathTests.cpp` — automation test `TDD.Movement.DodgeDistanceMath`.
- `Tests/Standalone/TDDDodgeDistanceMathTests.cpp` — standalone 18/18.
- `TheDisobedientDaughter.uproject`, `TheDisobedientDaughter.Build.cs`, both `*.Target.cs`, `Config/*.ini` — project foundation.

---

## 1. Requirement-by-requirement verdict

### §3.5 — sweep mechanics (capsule, radius, channel, filtering, planar, prediction)

| # | Requirement (M1 §3.5) | Verdict | Evidence |
|---|---|---|---|
| 1 | Capsule sweep uses exactly the CMC capsule via `MakeCapsule(R, H)` | **PASS** (code) | `TDDDodgeSweep.cpp`: `GetScaledCapsuleRadius()` / `GetScaledCapsuleHalfHeight()` → `FCollisionShape::MakeCapsule(Radius, HalfHeight)`. Exactly the CMC capsule. |
| 2 | Radius counted exactly once (centre at contact, no second radius subtraction; only `DodgeSafetyMargin` subtracted) | **PASS** (code + standalone test) | `TDDDodgeDistanceMath.h` subtracts only `SafetyMarginCm`. Standalone test assertion "capsule contact subtracts only safety margin" (120→118) explicitly proves radius is **not** subtracted twice. |
| 3 | Channel `ECC_Pawn`, query-only | **PASS** (code) | `World->SweepSingleByChannel(..., ECC_Pawn, Shape, QueryParams)`. |
| 4 | `bTraceComplex=false` | **PASS** (code) | `FCollisionQueryParams(SCENE_QUERY_STAT(TDDDodgeSweep), false)` — second argument is `bTraceComplex=false`. |
| 5 | Ignores owner + lock-on target | **PASS** (code) | `AddIgnoredActor(&Character)`; `if (LockedTargetActor != nullptr) AddIgnoredActor(LockedTargetActor)`. |
| 6 | `bStartPenetrating` → **refuse** the dodge (not clamp-to-zero) | **PASS** (signal) / **NOT YET WIRED** (behaviour) | `TDDDodgeSweep.cpp`: `if (bBlocked && Hit.bStartPenetrating) → StartingPenetration` status returned, distance not clamped. The **refusal signal** is correct. The actual refusal behaviour (no montage, no movement, `Dodge.Refused.StartingPenetration` log, no cooldown consumed) belongs to the state-machine/character integration, which is **Agent 3's remaining scope** and is not in this commit. |
| 7 | Planar — Z preserved | **PASS** (code) | `Direction` zeroes Z (`FVector(X, Y, 0)`); start/end share Z; centre distance uses `Size2D()`. |
| 8 | CMC moves the capsule; sweep is a **prediction only** (ADR-0013) | **PASS** (by design) | `FDodgeSweepResult` / `ResolveDodgeSweep` do not move the character; header documents the caller must still validate. Correct. |
| 9 | Clamped-end **floor validation** (≤10 cm diff, max 3 iterations) | **FAIL — NOT IMPLEMENTED** | The sweep and math contain **no floor validation**. The header explicitly defers it: "callers must still perform the M1-specified destination-floor validation before executing the dodge." This §3.5 requirement is **not met** in `dab65e5`. |

### AC-19 — dodge distance / clearance determinism

| # | Requirement (AC-19) | Verdict | Evidence |
|---|---|---|---|
| A | On flat ground / no obstruction, `ResolvedDistance == AuthoredDistance` | **PASS** (math) | `ResolveDodgeDistance(Authored, bBlocked=false, ...) → AuthoredDistance`. Standalone test "unobstructed keeps authored distance" (300→300). |
| B | Unit test proves radius is included once and not double-counted | **PASS** (math + standalone) | Standalone assertion 120→118 ("capsule contact subtracts only safety margin"). |
| C | Mean within 5 cm of resolved distance, σ ≤ 5 cm over **100 runs** | **FAIL — TEST ABSENT** | No 100-run repeatability test exists. `DodgeDistanceRepeatable` (M-09a) required by AC-19 is **not implemented**. Determinism is structurally true (pure function) but **not demonstrated** over 100 runs. |
| D | Required tests named `TDD-Unit.Movement.DodgeSpecMath` + `...DodgeDistanceRepeatable` (M-09a) | **FAIL — NAMING/COVERAGE MISMATCH** | Implemented test is `TDD.Movement.DodgeDistanceMath` (dot, not `TDD-Unit`), and there is **no** `DodgeSpecMath` or `DodgeDistanceRepeatable`. Traceability to AC-19 is **broken**. |

### Unreal verification

| # | Requirement | Verdict | Evidence |
|---|---|---|---|
| E | Functionality verified **in Unreal** (compiled + automation test run) | **BLOCKED** | No UE toolchain/compiler in the sandbox (blocker B-3); Epic hosts unreachable. The `.cpp` files are **structurally valid but `IMPLEMENTED_UNVERIFIED`** — never compiled or run in Unreal. The standalone 18/18 proves the pure-math header only. Per ADR-0005 and the directive, this is **not** Unreal-verified. |

---

## 2. Summary of defects and required changes

**Defects (blocking AC-19 acceptance):**

1. **AC-19 determinism test absent.** No 100-run repeatability test (`DodgeDistanceRepeatable` / M-09a). Required: a test that runs the clearance resolution 100 times and asserts mean within 5 cm and σ ≤ 5 cm. *Owner: Agent 3.*
2. **Test-name / traceability mismatch.** Implemented test `TDD.Movement.DodgeDistanceMath` does not match M1's mandated `TDD-Unit.Movement.DodgeSpecMath`; no `DodgeDistanceRepeatable`. Required: align test names to `TDD-Unit.Movement.*` so AC-19 traceability holds. *Owner: Agent 3.*
3. **§3.5 clamped-end floor validation not implemented.** No floor-distance correction / destination-floor validation (≤10 cm, max 3 iterations). Explicitly deferred to the caller. *Owner: Agent 3 (destination-floor validation + floor-distance correction are in Agent 3's M1 scope).*

**Gaps (expected, outside this commit — integration, Agent 3 scope):**

4. **Start-penetration refusal behaviour not wired.** The sweep correctly **signals** `StartingPenetration`, but the refusal behaviour (no montage, no movement, `Dodge.Refused.StartingPenetration` log, no cooldown consumed) is not implemented — it depends on the character/state-machine integration.
5. **No connection to CMC movement.** The sweep is correctly prediction-only (ADR-0013); the actual capsule displacement by CMC during the dodge is not implemented.

**Not a defect (verified correct in code):** capsule construction, radius-once math, `ECC_Pawn`, `bTraceComplex=false`, ignored actors, planar Z, prediction-only design, `ResolvedDistance == AuthoredDistance` on the unobstructed path.

## 3. Blocker

**B-3 (engine availability) is the sole blocker on Unreal verification.** The sandbox has no UE 5.8 install and cannot reach Epic's hosts, so the `.cpp` dodge implementation cannot be compiled, the automation tests cannot be executed, and AC-19 cannot be **empirically** closed in Unreal. **Required to unblock:** the Project Owner executes the provided `Tools/engine/mac_build.sh` (and automation test run) on the owner's Mac with UE 5.8 installed, and supplies the output. Until then, per ADR-0005, the UE implementation is **IMPLEMENTED_UNVERIFIED — not ESTABLISHED**, and no AC-19 PASS is granted at the engine level.

## 4. Overall outcome

- **§3.5 sweep mechanics (capsule, radius-once, channel, filtering, planar, prediction): PASS at code level — UE verification BLOCKED.**
- **§3.5 clamped-end floor validation: FAIL — not implemented.**
- **AC-19 radius-once + `ResolvedDistance == AuthoredDistance`: PASS at math level (standalone 18/18), UE verification BLOCKED.**
- **AC-19 100-run determinism + required test names: FAIL — tests absent / mismatched.**
- **Unreal verification: BLOCKED (B-3).**

**Verdict:** The dodge clearance **math and sweep** are implemented and structurally correct against M1 §3.5, and the radius-once requirement is demonstrated by a passing standalone test. **AC-19 is NOT fully met**: the 100-run determinism test and the mandated test names are missing, and the clamped-end floor validation is not implemented. **No engine-level PASS is granted** — the Unreal `.cpp` is unverified (B-3). This review does **not** approve functionality that has only passed standalone tests but has not been verified in Unreal.

**Recommended actions:** (1) Agent 3 implements AC-19's 100-run determinism test + floor validation + names tests per M1; (2) Owner runs `mac_build.sh` + automation on the Mac to close B-3; (3) re-review after both land.
