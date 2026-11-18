# Unreal Project Foundation — V1 (platform consolidation update)

**Repository/branch:** `The-Mhood/TDD` / `arena/c64fc525-tdd`
**Engine association:** Unreal Engine **5.8** (`EngineAssociation: "5.8"`)
**Current state:** One canonical project descriptor and a minimal C++ runtime/editor foundation exist. This Linux sandbox cannot install or run Unreal; project open/build/Automation results are **NOT RUN**.

## 1. Canonical project and platform intent

- **Only authoritative project descriptor:** repository-root `TheDisobedientDaughter.uproject`. Repository/index/history inspection on this branch found no `TDD.uproject`; it was not present to merge or delete. Do not create a second descriptor. If a separate external copy exists on the owner's machine, do not copy it into the repository; use this root descriptor and migrate any unique needed settings explicitly after review.
- **Engine:** UE 5.8, initially selected as an engine association, not a verified installed patch/build and not a choice of canonical MEAD.
- **Platforms:** Mac and Windows are both listed as project target platforms for the current project workflows. Mac is the immediate development host/target; Win64 remains a production candidate. PS5 remains an intended production path, but is intentionally not declared as an enabled target here: access, console SDK/engine integration and platform tooling are gated by Sony/Epic authorization.
- **Module architecture:** one minimal runtime module, `TheDisobedientDaughter`, with no third-party plugin or speculative contract module. Existing `TheDisobedientDaughterTarget` and `TheDisobedientDaughterEditorTarget` rules are platform-generic; UE's installed UBT selects the requested Mac or Win64 platform. The project GameMode is a minimal `AGameModeBase` subclass. No gameplay system or C-05 interface is introduced.

## 2. Consolidation and files

`TheDisobedientDaughter.uproject` is kept at the repository root as the sole descriptor. Its `TargetPlatforms` list is now `Mac`, `Windows` (previously Windows only). There was no second descriptor in the tracked tree, available history, or filesystem under this checkout, so consolidation means retaining the one existing descriptor and extending its platform declaration—not renaming it, copying it, or removing project history.

| Path | Purpose |
|---|---|
| `TheDisobedientDaughter.uproject` | Canonical root descriptor, UE 5.8, one runtime module, Mac and Windows project target platforms. |
| `Source/TheDisobedientDaughter.Target.cs` | Game target; generic UBT target rules. |
| `Source/TheDisobedientDaughterEditor.Target.cs` | Editor target; generic UBT target rules. |
| `Source/TheDisobedientDaughter/TheDisobedientDaughter.Build.cs` | Runtime module with Core/CoreUObject/Engine dependencies. |
| `Source/TheDisobedientDaughter/Private/TheDisobedientDaughter.cpp` | Runtime module registration. |
| `Source/TheDisobedientDaughter/Public/TDDGameMode.h`, `Private/TDDGameMode.cpp` | Minimal project `AGameModeBase`; no gameplay behavior. |
| `Source/TheDisobedientDaughter/Private/Tests/TDDProjectFoundationTests.cpp` | Unreal Automation source test `TDD.Foundation.GameModeClass`; not yet compiled or run. |
| `Config/DefaultEngine.ini`, `Config/DefaultGame.ini` | Engine startup/GameMode and project identity settings. |
| `.gitignore` | Unreal generated outputs and IDE/temp exclusions. |

No fabricated map/assets or placeholder tests are added. Engine `/Engine/Maps/Entry` remains the configured startup map.

## 3. Exact Mac requirements and preparation plan

Epic's versioned [UE macOS Development Requirements](https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?application_version=5.8) lists for UE 5.8: minimum macOS Sonoma 14.5, Xcode 26.0 minimum and Xcode 26.1.1 recommended; it warns Xcode 26.4 is incompatible. The page recommends 32 GB+ memory and lists 16 GB as minimum. This Apple M4 / 16 GB machine meets the listed minimum memory and processor class, but has no headroom over the memory minimum for editor, shader compilation, Xcode, and other tools; expect memory pressure and close other applications. Epic's M2+ rendering feature notes describe hardware ray tracing/MegaLights as experimental and Nanite/Virtual Shadow Maps as beta on Apple Silicon, so validate the chosen feature set and performance on the actual M4.

The same Epic page's broad current headline/recommended OS text is older than the supplied `macOS 27.2.1` and recommends Sequoia 15 for the UE 5.8 row. It does **not** certify macOS 27.2.1. Treat OS 27 compatibility as unverified; an Editor launch/build/Automation smoke run on the actual host is required before claiming support. Epic's UE 5.8 release-note search content has a conflicting older macOS Xcode table (15.2 minimum); use the dedicated versioned macOS Development Requirements page's UE 5.8 row as the install target, and confirm with the exact installed UE 5.8 build/UBT before production. Do not install Xcode 26.4 for this project baseline.

**Prepare on the owner's Mac (not executable from this Linux sandbox):**

1. Install an authorized UE 5.8 Editor distribution from Epic Games Launcher or an authorized Epic source build; include Mac support. Confirm exact engine changelist/patch and Mac SDK/compiler reported by that build.
2. Install **Xcode 26.1.1** (recommended; **26.0 is the stated minimum**) and its command-line tools. Do not use 26.4. Complete first-launch component installation and license acceptance.
3. Select and record the active developer directory and verify toolchain versions:
   ```sh
   xcode-select -p
   xcodebuild -version
   xcrun --sdk macosx --show-sdk-version
   clang++ --version
   ```
4. Open the root `TheDisobedientDaughter.uproject` in UE 5.8. Let the Editor generate project metadata as needed; do not commit generated `Intermediate`, `Binaries`, `Saved`, or user IDE files.
5. Build the Editor target for Mac Development with the `Build.sh` shipped by that exact UE installation (substitute the installed engine root):
   ```sh
   "$UE_ROOT/Engine/Build/BatchFiles/Mac/Build.sh" \
     TheDisobedientDaughterEditor Mac Development \
     -Project="$PWD/TheDisobedientDaughter.uproject" -WaitMutex
   ```
   To build the game target separately, use `TheDisobedientDaughter Mac Development` with the same project argument. After a successful Editor build, run the foundation Automation filter with that installation's commandlet:
   ```sh
   "$UE_ROOT/Engine/Binaries/Mac/UnrealEditor-Cmd" \
     "$PWD/TheDisobedientDaughter.uproject" -unattended -nop4 -NullRHI \
     -ExecCmds="Automation RunTests TDD.Foundation.GameModeClass;Quit" \
     -TestExit="Automation Test Queue Empty" -log
   ```
   Preserve the full commands/output, engine build/changelist, macOS and Xcode versions, log, exit codes, and test result for Agent 2's independent review. These commands are instructions only; none has run here.

**No Mac installation, opening, build, or test has been performed by this agent.** The checkout host is Linux x86_64 and lacks Unreal Editor, UBT, RunUAT, .NET and the Apple/Xcode toolchain; it cannot install onto the owner's Mac. No remote Mac access is available in the session.

## 4. Windows and PS5 path

- **Windows x64:** the generic Game and Editor targets remain; build with the same UE 5.8 project on an authorized Windows x64 host using the UE 5.8-compatible Visual Studio 2022 C++ toolchain and Windows SDK as reported by the exact installed UBT. Windows compilation/cooking/package verification still needs to be run separately.
- **PS5:** preserving future intent is not equivalent to platform enablement. Epic's [PS5 development guidance](https://dev.epicgames.com/documentation/en-us/unreal-engine/development-for-playstation-5-in-unreal-engine) requires PS5 documentation access permissions after NDA requirements, and Sony-approved developer status/access is required. Named blocker owner: Project Owner / organization console administrator to secure Sony partner status, Epic console access, SDK and dev kit; Agent 1 to integrate once authorized; Agent 2 to verify on authorized console tooling. Do not put proprietary SDKs, binaries, secrets, or gated details in this repo without authorization.

## 5. Verification ledger

| Check | Result | Evidence |
|---|---|---|
| Number and location of descriptors in this checkout | **PASS: 1** | `find` and `git ls-files` found only root `TheDisobedientDaughter.uproject`; history contains only its addition. `TDD.uproject` is absent here. |
| Descriptor JSON and platform list | **PASS: static only** | Python JSON parse confirms engine association `5.8`, module `TheDisobedientDaughter`, and platforms `Mac`, `Windows`. Not a UE validation. |
| Project structure and references | **PASS: static only** | Source/target/config files and configured GameMode references are present. |
| Open in UE 5.8 | **BLOCKED / NOT RUN** | No Unreal Editor in this Linux sandbox; no access to owner's Mac. |
| Compile Mac module | **BLOCKED / NOT RUN** | No Mac/Xcode host or UE installation available to this agent. |
| Foundation Automation test | **BLOCKED / NOT RUN** | Test source exists only; no compiled Editor or Automation runner. Agent 2 has not independently verified this consolidation or run. |
| Win64 / PS5 builds | **NOT RUN** | Require the corresponding authorized host and platform toolchains. |

## 6. Governance and C-05 boundary

C-05 remains `DESIGN_ONLY`, unsigned/unfrozen, and 0/67 acceptance cases executed. The proposed first tranche remains unimplemented/unrun; T-C05-11 remains deferred pending TD-06. This foundation change does not resolve C-05 dependencies, establish a formal freeze/kickoff, choose a canonical MEAD, or start gameplay implementation. L-2 remains CLOSED; S4.3.10 and its historical `147/147` evidence are preserved. No project-opening/build/test or Agent 2 verification claim is made.

## References

- Epic, [macOS Development Requirements for UE 5.8](https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?application_version=5.8) — OS, Xcode, memory, rendering feature notes.
- Epic, [Development for PlayStation 5 in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/development-for-playstation-5-in-unreal-engine) — console permissions and access gate.
