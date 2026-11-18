# Unreal Project Foundation — V1

**Date:** 2026-11-18 UTC
**Repository/branch:** `The-Mhood/TDD` / `arena/c64fc525-tdd`
**Authority:** Project Owner directive “CREATE THE UNREAL PROJECT AND COMMENCE C-05 IMPLEMENTATION.”
**Status:** Project files created; Editor open/build/Automation execution **BLOCKED / NOT RUN** because the Unreal toolchain is unavailable in this workspace.

## 1. Project decisions

- **Engine baseline selected:** Unreal Engine **5.8** (`EngineAssociation: "5.8"`). This follows MEAD-A's UE 5.8 proposal at `912fac9f76a1011f8c823b368a92a0edf059a283` (`Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md`, blob `bd0f3afdf24736349f2045bf0ee423ee0b4e1a78`) and the Project Owner's instruction to select an engine baseline. This selects only an initial project engine association; it does not select MEAD-A as the canonical architecture. It is not a claim that UE 5.8 is installed or that the exact patch/build has been verified.
- **Initial target:** **Windows x64 (Win64), Development**; an Editor target is also defined. This follows MEAD-A's PC-first proposal, but is only the first development target, not a shipping-platform or minimum-hardware commitment.
- **Project name/location:** `TheDisobedientDaughter.uproject` at the repository root; module `TheDisobedientDaughter`.
- **Initial module architecture:** one minimal runtime game module, with no third-party plugins. This creates a project shell without selecting among the materially different MEAD candidates, adding speculative module boundaries, or assigning the C-05 contract layer. C-05 interfaces remain gated by TD-12 and formal contract freeze.

The engine/target choice is versioned here because the owner explicitly directed project creation. It does **not** resolve TD-12, choose a canonical MEAD, change C-05 semantics, or change any acceptance-case identity.

## 2. Files established

| Path | Purpose |
|---|---|
| `TheDisobedientDaughter.uproject` | UE project descriptor, engine association 5.8, one runtime module, Windows target platform. |
| `Source/TheDisobedientDaughter.Target.cs` | Game target. |
| `Source/TheDisobedientDaughterEditor.Target.cs` | Editor target. |
| `Source/TheDisobedientDaughter/TheDisobedientDaughter.Build.cs` | Minimal Core/CoreUObject/Engine module dependencies. |
| `Source/TheDisobedientDaughter/Private/TheDisobedientDaughter.cpp` | Primary runtime module registration. |
| `Source/TheDisobedientDaughter/Public/TDDGameMode.h` and `Private/TDDGameMode.cpp` | Project-owned minimal `AGameModeBase` subclass; no gameplay rules added. |
| `Source/TheDisobedientDaughter/Private/Tests/TDDProjectFoundationTests.cpp` | Real Unreal Automation Framework smoke test asserting the project GameMode class is registered and derives from `AGameModeBase`. |
| `Config/DefaultEngine.ini` | Engine entry map and project GameMode defaults. |
| `Config/DefaultGame.ini` | Project identity/version settings. |
| `.gitignore` | Unreal-generated binaries, intermediate/cache/saved output and common IDE artifacts. |

The project uses the engine's `/Engine/Maps/Entry` map; no fabricated `.umap`, `.uasset`, C-05 stub, or placeholder test was added. The smoke test is foundation-only, not a C-05 acceptance test.

## 3. Verification state and exact toolchain blocker

| Gate | Result | Evidence / next action |
|---|---|---|
| Project descriptor syntax | **PASS — static JSON parse only** | Descriptor parses as JSON and names the module/target. This does not prove Unreal accepts it. |
| Project opens in Unreal Editor | **BLOCKED / NOT RUN** | No `UnrealEditor` binary is available in the current Linux workspace. No editor launch is claimed. |
| Project generation/compile | **BLOCKED / NOT RUN** | No `UnrealBuildTool`, `RunUAT`, .NET SDK/runtime or UE installation is available. `g++` alone is not an Unreal toolchain. |
| Automation test discovery/execution | **BLOCKED / NOT RUN** | Test source exists, but no Editor build or Unreal Automation runner is available. No C-05 case has been executed. |
| Package/cook | **BLOCKED / NOT RUN** | No UE AutomationTool, Windows SDK or authorized Windows runner is available. |

### Installation/toolchain process assigned

- **Required host:** an authorized Windows 10/11 x64 development machine or runner with supported disk/GPU capacity and project access. The Linux agent sandbox is not the editor host.
- **Engine:** install an available, licensed **Unreal Engine 5.8** distribution (Epic Games Launcher binary installation or an authorized Epic-source build); include Editor, Win64 target support and UnrealBuildTool/AutomationTool. Do not download engine binaries or source from unofficial mirrors.
- **Compiler/SDK:** install Visual Studio 2022 with the C++ game-development/Desktop C++ components and the Windows SDK supported by that UE 5.8 build. Confirm exact versions with the installed UBT/engine requirements and record them; do not infer an SDK version here.
- **Access:** an authorized operator must have the required Epic account/license and permitted engine/source access. Credentials must not be placed in chat or the repository.
- **Owner/sequence:** Agent 1 coordinates installation or identifies the already-installed authorized host; Agent 3 records the environment manifest; Agent 2 independently checks the project-open/build/test evidence. No host/operator confirmation has been received in this environment, and I cannot perform the installation from this sandbox: the engine is absent and outbound access is limited to GitHub/API, npm and PyPI rather than Epic's distribution services.
- **First verification commands:** on the authorized host, use the installed UE 5.8 editor to open and close/reopen the root `.uproject`; build `TheDisobedientDaughterEditor Win64 Development`; run Unreal Automation filter `TDD.Foundation.GameModeClass`; preserve exact command, engine/build version, runner, logs and exit status. These commands are a procedure only; none has run here.

## 4. C-05 implementation boundary

This foundation does not contain C-05 runtime types or behavior. The user authorized creating the project now, but the C-05 direction itself requires the relevant contract decisions and formal kickoff authorization before acceptance execution. In particular, TD-12 still controls the canonical MEAD and contract-layer owner; TD-06 controls shared-axis timing; TD-09 controls arbitration. The 17-case mapping and owner/task register are in `docs/implementation/C05_TRANCHE1_IMPLEMENTATION_MAP_V1.md`.

- C-05 contract remains `DESIGN_ONLY`, unsigned and unfrozen.
- T-C05-01…10 and T-C05-21…27 remain **PROPOSED / NOT RUN**; T-C05-11 remains deferred until TD-06 is resolved.
- L-2 remains **CLOSED**; S4.3.10 and both L-2 evidence commits remain untouched.
- No C-05 implementation, C-05 API, project status promotion, or gameplay behavior claim is made by this project foundation.

## 5. Scope and follow-up

This is a genuine source/config project foundation committed inside the existing repository, not a disconnected sample. Its loading and build compatibility remain unverified until the authorized UE 5.8 toolchain is available. The prior bootstrap HOLD is superseded only to the extent of this Project Owner's explicit project-foundation direction; it is not blanket authorization to choose a canonical MEAD or freeze C-05.
