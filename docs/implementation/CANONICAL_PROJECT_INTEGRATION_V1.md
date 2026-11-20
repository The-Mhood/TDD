# Canonical Unreal Project Integration — V1

**Branch:** `arena/c64fc525-tdd`
**Project owner environment supplied:** Apple M4, 16 GB unified memory, macOS 27.2.1
**Current project state:** consolidated in repository; editor/build/test validation remains blocked on the actual Mac host.

## Decision and consolidation

- **Canonical branch:** `arena/c64fc525-tdd`; no branch switch or new branch.
- **Canonical descriptor:** `TheDisobedientDaughter.uproject` at repository root. This checkout's filesystem, Git index, and available history contain exactly one descriptor, `TheDisobedientDaughter.uproject`; no `TDD.uproject` exists here. Thus there was no second in-repository descriptor to merge or remove. If the owner has a separate local `TDD.uproject`, treat this canonical root descriptor as authoritative and do not copy the other descriptor into the repository.
- **Engine:** UE 5.8 association. Exact installed patch/changelist is not yet known.
- **Project platforms:** `Mac` and `Windows` enabled in the descriptor. Mac is the immediate development workflow; Windows x64 is retained as the production target path. PS5 is future intent only and remains gated by platform access/SDK/toolchain.
- **Module architecture:** one minimal runtime module, `TheDisobedientDaughter`; generic Game and Editor targets; minimal `ATDDGameMode`; Engine/Core/CoreUObject dependencies; one source-only UE Automation smoke test. No gameplay/C-05 modules or contract APIs were added.

## UE 5.8 Mac install requirements

Epic's UE 5.8 [macOS Development Requirements](https://dev.epicgames.com/documentation/unreal-engine/macos-development-requirements-for-unreal-engine?application_version=5.8) specifies minimum macOS Sonoma 14.5, minimum Xcode 26.0, recommended Xcode 26.1.1, and explicitly says Xcode 26.4 is incompatible. It lists 16 GB as minimum memory and 32 GB+ recommended. The M4 exceeds the documented Apple Silicon processor floor; this host sits exactly at the documented RAM minimum, so shader compilation/editor use may be memory constrained.

Epic's published UE 5.8 OS recommendation is macOS Sequoia 15, and the requirements page does not establish compatibility with the supplied macOS 27.2.1. Because 27.2.1 is newer than the documented row, its support is **unconfirmed**, not assumed. Use Xcode 26.1.1 if obtainable; if not, 26.0 is the stated floor, and check exact UBT compatibility on the installed UE patch. Avoid 26.4. Complete Xcode first-launch setup and select the active developer directory. Host-side verification commands are in `UNREAL_PROJECT_FOUNDATION_V1.md`.

## Verification and independent review

| Requirement | Result |
|---|---|
| Exactly one authoritative descriptor | **PASS in this checkout**: only root `TheDisobedientDaughter.uproject` found; `TDD.uproject` absent from worktree, index and available history. |
| Descriptor/platform structure | **PASS static checks only**: JSON parses; UE association is `5.8`; module is `TheDisobedientDaughter`; targets are Mac and Windows. |
| Open project in UE 5.8 on M4/macOS 27.2.1 | **NOT RUN / BLOCKED**: no access to the owner's Mac or an Unreal installation in this Linux sandbox. |
| Compile initial Mac game module | **NOT RUN / BLOCKED**: no Mac, Xcode, Unreal Editor or UBT in this environment. |
| Foundation Automation test | **NOT RUN / BLOCKED**: the test is source-only; test discovery and execution require a compiled Editor. |
| Agent 2 independent verification | **NOT RECEIVED**: no Agent 2 dispatch/acknowledgement or independent report for this consolidation/build was available. Static checks here are not a substitute. Agent 2 remains the named independent reviewer after host evidence is produced. |
| Agent 3 integration review | This report and the static descriptor/structure checks are the integration work performed in this session; not an independent review. |

No claim of successful Editor launch, compilation, Automation execution, or Agent 2 verification is made.

## Remaining blockers and named owners

1. **Mac engine/toolchain installation and real verification:** Project Owner/authorized Mac operator to install UE 5.8 and Xcode 26.1.1 (26.0 minimum), run the Editor open/build/foundation test, and preserve full logs/version/exit codes. Agent 1 coordinates installation/build procedure. Agent 3 records the manifest and traceability. Agent 2 independently reviews the evidence.
2. **macOS 27.2.1 support:** Agent 1/owner must validate launch, build, shader compilation and Automation on this exact OS; only passing evidence can confirm it. If unsupported, select a documented OS or resolve with Epic before committing to the host baseline.
3. **Windows x64 production path:** Agent 1 to coordinate a licensed UE 5.8-compatible Windows host, Visual Studio 2022 C++ toolchain and UBT-selected Windows SDK; Agent 2 to independently check Win64 build/cook evidence. No Windows build has run.
4. **PS5:** Project Owner/organization console admin to obtain Sony-approved developer access, Epic PS5 console documentation permission, SDK and dev kit; Agent 1 can integrate after authorization; Agent 2 verifies on authorized tooling. Epic's [PS5 development access page](https://dev.epicgames.com/documentation/en-us/unreal-engine/development-for-playstation-5-in-unreal-engine) describes access/NDA requirements.
5. **C-05 dependencies:** As listed in `C05_TRANCHE1_IMPLEMENTATION_MAP_V1.md`, TD decision owners still need version-pinned dispositions for TD-06, TD-09, TD-12 and B-11; Agent 2 needs to complete B-9 and B-14 independent review; Agent 3/TD need the exact S4.3.11/B-10/B-15 boundary disposition. B-12 scope confirmation and B-14 test tolerance convention were recorded, but Agent 2 review of B-14 remains outstanding. Do not freeze or implement acceptance behavior until required design decisions and formal kickoff are recorded.

## Production commencement gate

The canonical project structure and Mac target declaration are now prepared. **Production gameplay implementation has not begun**: the requested order requires opening, compiling, and running the foundation Automation test first, and these actions need the owner's actual Mac host. C-05 also remains `DESIGN_ONLY`, unsigned/unfrozen, `0/67` executed. First-tranche tests remain proposed/unrun, with T-C05-11 deferred pending TD-06. L-2 remains CLOSED, and S4.3.10 plus its historical `147/147` evidence remain unchanged.
