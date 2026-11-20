# Unreal project foundation — v1

**Document ID:** `TDD-IMPL-FOUNDATION-001`
**Date:** 2026-11-18 UTC
**Author:** Agent 1 — implementation lead
**Branch:** `arena/3bc206a0-tdd` (session branch of record; the directive named `arena/c64fc525-tdd`, which this session may not switch to — see §7)
**Status:** **`IMPLEMENTED_UNVERIFIED`** — the project skeleton is authored and statically checked; **no Unreal Engine exists in this workspace, so nothing has been compiled, opened, cooked or run.** This document does not claim a build.

---

## 1. What was created

A real Unreal project, in this repository, at the repository root — not a detached sample.

| Item | Path | State |
|---|---|---|
| Project descriptor | `TDD.uproject` | present, `"EngineAssociation": "5.8"`, 9 modules, `EnhancedInput` enabled |
| Game target | `Source/TDD.Target.cs` | present, `TargetType.Game` |
| Editor target | `Source/TDDEditor.Target.cs` | present, `TargetType.Editor`, includes `TDDEditor` + `TDDTests` |
| Primary game module | `Source/TDD/TDD.Build.cs`, `Private/TDDModule.cpp` | present, `IMPLEMENT_PRIMARY_GAME_MODULE` |
| `TDDCore` (leaf) | `Source/TDDCore/…` | present: module, `TDDEnginePin.h`, `TDDLog.h/.cpp`, **first automation test** |
| `TDDWorld`, `TDDGameplay`, `TDDAI`, `TDDNarrative`, `TDDUI` | `Source/<Module>/…` | present: `Build.cs` + module implementation |
| `TDDEditor`, `TDDTests` | `Source/<Module>/…` | present, Editor-type in the descriptor |
| Config | `Config/DefaultEngine.ini`, `DefaultGame.ini`, `DefaultInput.ini` | present (maps, RHI/Lumen, product identity, Enhanced Input default classes) |
| Toolchain preflight | `Tools/engine/preflight.sh` | present and executable |
| Structural verifier | `Tools/engine/verify_project_structure.py` | present and executable |

**Module graph** follows MEAD §3.2 exactly: `TDDCore` is a leaf; `TDDWorld` → `TDDCore`; `TDDGameplay` → `TDDCore`+`TDDWorld`; `TDDAI` may reach `TDDGameplay`, `TDDNarrative`/`TDDUI` only `TDDCore`+`TDDWorld`; `TDDEditor`/`TDDTests` are Editor-only and **nothing depends on them**. The direction is enforced mechanically, not just documented (§4).

**What is deliberately *not* in the skeleton.** No gameplay behaviour. The C-05 obligations that need unresolved decisions — the clock axis (B-1/TD-06), parry authority (B-2/TD-09), the contract-layer owner and value-type freeze (B-4/TD-12), the `C-04-4` carrier coupling (B-11) — are **not guessed at** in code. The modules that will host them exist and are empty on purpose; inventing behaviour there would silently decide a TD question.

## 2. Engine version and target platform

| Decision | Value | Authority |
|---|---|---|
| Engine | **Unreal Engine 5.8** | `docs/03_DECISIONS/ADR-0001` (status: *Proposed — requires TD confirmation*), MEAD §2.3 recommendation |
| Engine association string | `5.8` | MEAD §2.3: *"Exact version recorded in `.uproject` (`\"EngineAssociation\": \"5.8\"`)"* |
| C++ standard | **C++20** | MEAD §2.5 |
| Primary target platform | **Windows x64** (MSVC 14.4x) | MEAD §2.5: *"Compilers: MSVC 14.4x on Windows; Clang for any future Linux/console builds"* |
| Secondary / deferred | Linux and consoles | not configured; no Linux-specific config is committed |
| Build settings | `BuildSettingsVersion.Latest`, `EngineIncludeOrderVersion.Latest` | deliberate: survives the 5.8 patch stream without pinning an enum that may move |

**ADR-0001 is still `Proposed`.** The pin is therefore recorded as *the project's configured pin*, not as a ratified decision; if TD confirms a different 5.8 build or a different version, `TDD.uproject`, `TDDEnginePin.h` and this table change together, under an ADR.

## 3. Verified vs unverified — stated precisely

| Claim | Basis | Verified? |
|---|---|---|
| The descriptor is valid JSON and names 9 modules | `verify_project_structure.py`, run (§4) | **YES** — machine-checked |
| Every module has a `Build.cs`, a `ModuleRules` class and an implementation TU | same run, 58/58 checks | **YES** — machine-checked |
| The dependency graph obeys MEAD §3.2 and nothing depends on Editor-only modules | same run | **YES** — machine-checked |
| Targets, config files and the automation-test foundation exist and the test is guarded and named per MEAD §15 | same run | **YES** — machine-checked |
| The project **compiles** | requires UE 5.8 + MSVC/Clang + build machine | **NO — no engine, no compiler for UE headers** |
| The project **opens** in the editor | requires UE 5.8 | **NO** |
| The automation test **runs and passes** | requires a built editor | **NO** |
| The Unreal API calls and `Build.cs`/`Target.cs` symbols are correct for 5.8 | requires a compile | **NO — unverified API risk** |

**The honest summary:** everything a machine without Unreal can check, has been checked and passes; everything that requires Unreal is unverified. The API risk is real and named: `EAutomationTestFlags::EditorContext`, `IMPLEMENT_PRIMARY_GAME_MODULE`, `BuildSettingsVersion.Latest` and the `EnhancedInput` default classes are written to the 5.x API as documented, but only a first compile confirms them against 5.8.

## 4. Evidence from this workspace (actual output, not summarised)

**Structural verifier** — `python3 Tools/engine/verify_project_structure.py` → **`58/58 structural checks passed`**, covering the descriptor, all 9 module graphs, both targets, all three config files, the test guard, the `TDD-Unit.Canon.EnginePin` naming, and the absence of any dependency on an Editor-only module.

**Toolchain preflight** — `./Tools/engine/preflight.sh` → **`RESULT: NOT READY — 4 blocking gap(s)`**:

```
  TDD.uproject                               present
  EngineAssociation                          5.8 (pin 5.8)
  engine root                                NOT FOUND (set UE_ROOT): checked $UE_ROOT, /opt/UnrealEngine, /opt/UnrealEngine-5.8, ~/UnrealEngine
  clang / clang++ / dotnet / mono / cmake    MISSING
  g++ / make                                 present
  logical CPUs                               2 (UE 5.8 source build: 8+ recommended)
  RAM                                        3 GB (UE 5.8 editor: 32 GB recommended, 16 GB minimum)
  free disk                                  20 GB (UE 5.8 source + DDC: 200 GB+ recommended)
```

## 5. The exact blocker, and what unblocks it

**Blocker (B-3 in the contract's dependency table).** There is no Unreal Engine 5.8 installation in this workspace, and this workspace cannot obtain one:

1. **Distribution.** UE 5.8 is available only through the Epic Games Launcher (Windows/macOS) or the private `EpicGames/UnrealEngine` GitHub repository, which requires an Epic account with the EULA accepted and linked. This workspace's outbound access is restricted and carries no Epic credentials, so **no legal download path exists from here**.
2. **Machine.** 2 vCPU / 3 GB RAM / 20 GB free. A UE 5.8 source build is ~200 GB and compiles for hours on 8+ cores with 32 GB RAM; the editor itself needs 16 GB minimum. Even with a download path, this host cannot build or run the engine.
3. **Toolchain.** No Clang, no .NET, no CMake/Ninja. UE ships its own bundled Clang and .NET for Linux, but only as part of the engine tree that does not exist here.

**What is required, concretely, to turn `IMPLEMENTED_UNVERIFIED` into a build result:**

| Requirement | Minimum | Notes |
|---|---|---|
| Machine | 8+ cores, 32 GB RAM, 250 GB free NVMe | Windows 11 23H2+ or Ubuntu 22.04 LTS |
| Engine | **UE 5.8** (exact build recorded in `docs/02_PRODUCTION/ENGINE_PIN.md` once installed) | Launcher (Windows) or Epic GitHub (Linux) |
| Compiler | MSVC 14.4x + Windows SDK 10.0.22621+ (Windows); bundled Clang (Linux) | C++20 |
| .NET | 8.x SDK | required by UnrealBuildTool |
| Then | `GenerateProjectFiles`, `Build.bat TDDEditor Win64 Development`, open `TDD.uproject`, run `TDD-Unit.Canon.EnginePin` in the Session Frontend | each step recorded here with its output |

**Until then this repository will not pretend.** No build output, no `.sln`, no `Binaries/` and no test result is fabricated, and `Tools/engine/preflight.sh` is committed so any machine can re-measure itself rather than trust this page.

## 6. Automation-test foundation

- Unit tests live inside each module behind `#if WITH_DEV_AUTOMATION_TESTS`; functional/integration tests live in `TDDTests` (Editor-only) — MEAD §3.2.
- Naming follows MEAD §15: `TDD-Unit.<Area>.<Check>`, first test `TDD-Unit.Canon.EnginePin`.
- The first test is a **real assertion** about a fact this repository owns (the engine pin), not a green placeholder: it fails if `TDDEnginePin.h` and `TDD.uproject` drift apart.
- The runner contract (`python3`-free, in-editor) is: `UnrealEditor-Cmd … -ExecCmds="Automation RunTests TDD-Unit"` on a build machine; unavailable here for the same reason as §5.

## 7. Branch and scope notes for the Project Owner

- **Branch.** The directive names `arena/c64fc525-tdd` as active. This session is pinned to `arena/3bc206a0-tdd` and may not switch branches, so all work here is on `arena/3bc206a0-tdd`. `arena/c64fc525-tdd` also holds the **superseded** identity `TDD-A1-C05-SUCCESSOR-004.2-D`, which the repository records as *"not a baseline, not citable, not merged"* — creating the project there would place new engineering work on the branch the governance record disclaims. **Recommendation: ratify `arena/3bc206a0-tdd` as the engineering branch, or direct a different one explicitly.**
- **L-2's recorded status.** The directive asks to preserve `L-2`'s **CLOSED** status. The repository currently records `L-2` as **`OPEN — parked`** against the immutable S4.3.10 text, with the discrepancy fully documented in `docs/AGENT1_C05_L2_COUNT_ADDENDUM_V1.md` and the consistent reading fixed at `129 → 147 (+18)`. **No governance record was changed**; if TD intends `CLOSED`, that is a one-line change to `STATUS_AND_CLAIMS.md` and needs to be directed, not assumed.
- **Preserved untouched:** `A1-C05-S4.3.10` and its 147/147 evidence blob, the 43 obligations, 18 suites, 67 case identities, and every existing evidence document. C-05 remains `DESIGN_ONLY`.

## 8. Next actions, in dependency order

1. **TD:** confirm or amend the engine pin (ADR-0001) and provide a build machine (§5) — nothing below can be *verified* without it.
2. **TD:** answer B-1 (TD-06), B-2 (TD-09), B-4 (TD-12); **C-04 owner:** B-11; these gate tranche behaviour (see the dependency matrix).
3. **Agent 1:** first tranche implementation against the mapping, in `TDDCore` (contract types) then `TDDWorld`/`TDDGameplay`; each file lands `IMPLEMENTED_UNVERIFIED` until a build exists.
4. **Agent 2:** independent verification of the first compile and of `TDD-Unit.*` results; **Agent 3:** design/governance traceability of the module graph against MEAD §3.2.
