# Project Bootstrap Decision — Unreal Project and Agent Integration

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Prepared by:** Agent 3 — Integration, QA, Build and Performance
**Date:** 2026-11-16 UTC
**Repository / branch:** `The-Mhood/TDD` / `arena/c64fc525-tdd` (active)
**Decision status:** **HOLD — do not create a `.uproject` or gameplay modules yet.** This is a proposed bootstrap plan for Technical Director / Creative Director review, not an implementation contract.

## 1. Decision and evidence

The inspected repository currently contains documentation only; no `.uproject`, `.uplugin`, `Source/`, `Config/`, `Content/`, targets, maps, tests, or build/package scripts were found. The current HEAD is `7f24859f716bdc36d15f5ef8b54370e4b6be80da` on `arena/c64fc525-tdd`. The repository history before the documentation baseline is the original `5e3d1da4eee42ad8255760530291ff91cdfb39b2` commit. The accepted architecture/QA documents have been committed on this branch; this bootstrap decision is the follow-up report.

Host/tool inspection on Linux `6.1.158+ x86_64` found no `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh`, `dotnet`, or `clang++` on `PATH`, and no Unreal Editor/UBT/RunUAT executable under the inspected common roots `/opt`, `/usr/local`, and `/home/user`. `g++` and `python3` are present, but they are not substitutes for Unreal's toolchain. This is not a machine-wide search for every possible installation path; it is sufficient to establish that the current workspace cannot execute an Unreal toolchain through the checked paths.

### Current Unreal capability assessment

| Capability | Status | Evidence / reason |
|---|---|---|
| Prepare project/bootstrap documentation | **PASS** | Markdown and Git are available; this document is the planning deliverable. |
| Create a genuine supported Unreal project | **BLOCKED** | No UE editor/project generator is available, and project creation is expressly on hold. A hand-written `.uproject` descriptor would not prove a valid project. |
| Open the project in Unreal Editor | **BLOCKED** | No `.uproject` exists in checkout and no `UnrealEditor` executable is available in inspected paths. |
| Generate project files / compile | **BLOCKED** | No UBT, UE source/build, Unreal target, or compiler toolchain for a verified UE installation. `g++` alone cannot compile a UE target. |
| Run Unreal automation/gameplay tests | **BLOCKED** | No engine, game module, test fixtures, or test runner. |
| Cook/package a build | **BLOCKED** | No RunUAT, `.uproject`, target platform/SDK, or package config. |
| Measure gameplay performance | **BLOCKED / NOT MEASURED** | No executable, representative map, or approved hardware/quality target. |
| Validate repository Markdown and links | **PASS** | Local Python/Markdown checks are available; these are documentation checks only, not CI or game tests. |

No CI workflow is configured or reported operational. No Unreal operation has been attempted in this environment.

### README change assessment

The README change included in documentation commit `7f24859f716bdc36d15f5ef8b54370e4b6be80da` replaces the placeholder `# TDD` with the game title and Igbo subtitle, states plainly that the checkout is a planning repository with no UE project or implemented gameplay, links to the Master Engineering Architecture, and points to the Drive Art Bible as visual authority. The changed lines do not add implementation claims, alter source code, or replace unrelated files. The local architecture-document link resolves. Assessment: **accurate and appropriately scoped**; the README should be revised when a real project is bootstrapped, not claim one already exists.

## 2. Proposed project shape (for approval before creation)

Keep the first project deliberately small and source-controlled. Use one runtime game module initially; split modules only after real ownership/dependency evidence supports the split. Do not scaffold these files until the Creative Director/Technical Director identifies the canonical project location and approves engine/platform choices.

```text
<ProjectRoot>/
├── <ProjectName>.uproject
├── Config/
│   ├── DefaultEngine.ini
│   ├── DefaultGame.ini
│   ├── DefaultInput.ini
│   └── DefaultEditor.ini              # only settings actually needed
├── Source/
│   ├── <ProjectModule>.Target.cs
│   ├── <ProjectModule>Editor.Target.cs
│   └── <ProjectModule>/
│       ├── <ProjectModule>.Build.cs
│       ├── Public/                    # reviewed public API only
│       └── Private/                   # implementations
├── Content/
│   ├── Maps/                          # test map before campaign maps
│   └── ...                            # authored content, gated by approval
├── Plugins/                           # empty unless individually approved
├── Tests/                             # only if a real non-UHT test runner is selected
├── Scripts/                           # pinned, documented build/test wrappers
└── docs/
```

The exact project/module name, directory layout, game/editor targets, input map setup, startup map, collision profiles, rendering/scalability settings, source asset organization, and test-map contents remain undecided until project creation is authorized. `Server.Target.cs` and replication scaffolding are **not** proposed unless multiplayer/dedicated-server scope is confirmed. Avoid adding a separate Editor module until editor tooling is actually required.

### Module boundary recommendation (provisional)

- Start with one `<ProjectModule>` runtime module and explicit folders/contracts; avoid premature UBT module boundaries.
- Keep player movement/combat implementation, world simulation, and integration bootstrap as identifiable feature areas with a single owner and narrow public APIs.
- If Agent 1 and Agent 2 need independently compiled feature modules, first establish a small, stable `GameplayContracts` module with only shared value types/interfaces/events and no dependency on either feature module. Candidate graph: `PlayerGameplay → GameplayContracts`; `WorldGameplay → GameplayContracts`; `<ProjectModule> → PlayerGameplay + WorldGameplay`. This is a review option, not a final architecture decision; the actual existing project may imply a different graph.
- No contract module may include concrete classes from both sides. Cross-feature implementations are bound by the game/integration layer, not by reciprocal feature-module dependencies.

### Files/config and code policy

- `.uproject` pins/records the engine association and explicit plugin descriptors; exact format generated/validated by the approved UE editor/tooling.
- `*.Target.cs` and `*.Build.cs` are the declared target/module dependency surfaces. Keep dependencies minimal and explicit; no circular module dependencies.
- Put project defaults in versioned `Config/` only after inspecting engine defaults and platform needs. Avoid copying unexplained generated settings.
- Keep game logic in C++ where reusable/critical; expose approved tuning/content hooks to Blueprint. The appropriate implementation division remains subject to Agent 1/2 review.
- No engine fork, custom binary, marketplace package, or plugin without a documented need, version/compatibility review, license/access check, owner, and removal/upgrade plan.

## 3. Engine, platform, plugins, and large assets

### Engine and toolchain

**Requirement:** Unreal Engine 5, exact minor version **not selected**. Before project creation, choose one available/approved UE5 version and pin it for all agents and build runners. Record editor/build version, host OS, compiler/toolchain, target SDK, enabled plugin versions, and any engine-source change. The engine and the project's build tool must generate/open/build the project; do not fabricate an engine version or rely on a different agent's local default.

The existing sandbox is Linux x86_64 and has no Unreal toolchain. Select a host and licensed UE installation that can support the approved target platform; its capabilities cannot be inferred from the C++ compiler in this workspace.

### Target-platform assumptions

- **Project constraint:** the creative brief specifies UE5 but does not specify shipping platform, hardware minimum, resolution, frame-rate goal, or distribution channel.
- **Planning assumption only:** a local, single-player desktop Development build is the lowest-cost first integration target. A Win64 first build is a reasonable candidate if the project owner has the required licensed UE installation and Windows toolchain, but **is not approved** and is not a shipping commitment.
- **Must decide:** initial development platform, final supported platforms, reference/minimum hardware, graphics quality and resolution targets, controller/keyboard support, online/multiplayer requirement, and release/distribution expectations. Do not create platform-specific files or assert compliance before these are decided.

### Plugin policy

Begin with core UE modules only and the smallest plugin list needed by inspected code. For every plugin, record name, exact version/source, purpose, enabled target platforms, dependencies, license, owner, test evidence, and upgrade/removal risk. Require TD review before enabling non-core, third-party, marketplace, online, telemetry, or platform plugins. Do not enable GAS, World Partition, an AI framework, or a vendor plugin solely because it appears in a recommendation; verify engine version, project needs, and owner agreement first.

### Source control and binary assets

- Git is the record for source code, project configuration, build/test scripts, and technical documentation.
- Decide binary strategy before bringing `.uasset`/`.umap` production data into Git. **Recommendation for review:** use Git LFS for versioned Unreal binary assets if quota, lock semantics, and contributor access are confirmed; keep source docs/config in ordinary Git. Do not mix an unannounced LFS transition with the bootstrap commit.
- Add only tested ignore rules for generated `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, IDE files, and local-only outputs. Never ignore source/config, maps, test assets, or approved content accidentally.
- The Google Drive Production Art Bible remains authoritative for visual status and source references; do not treat Drive as a runtime asset loader or copy exploratory/rejected assets into production Content. Define approved asset import, stable ID, provenance/checksum, license, review-status, and sync ownership before import.
- Avoid committing cooked builds, caches, or opaque generated content. Store CI packages in an approved artifact location with retention, access control, and checksum policy.

## 4. Repository-level build and validation proposal

This repository has no workflow today. The following are **proposed**, not active CI. Use the status vocabulary exactly: **PASS** (executed and satisfied criteria), **FAIL** (executed and did not satisfy), **BLOCKED** (could not execute due to a stated prerequisite), **NOT RUN** (available but not executed), **NOT MEASURED** (no valid metric/capture).

### Phase A — documentation-only validation (can run now)

- Check Markdown whitespace and repository-local link targets using a pinned, documented script or simple Python tooling.
- Check that `README.md` and docs distinguish proposed from accepted, include source references for claimed status, and do not claim engine or gameplay evidence.
- Run `git diff --check` for staged/tracked changes and separately validate newly added/untracked Markdown files (Git's default diff check does not include untracked files).
- Status today: prior document/link/whitespace checks **PASS** as manual repository QA. There is no workflow and this is not CI.

### Phase B — project foundation (requires real UE project/toolchain)

1. Clean checkout, assert pinned engine/toolchain/plugin versions.
2. Run a project and asset/config validation command; fail on missing required project or unresolved approved asset references.
3. Compile the editor/development target with a preserved log and explicit exit status.
4. Run fast Unreal Automation Tests and map/content validation; report separate pass/fail/blocked/skipped totals.
5. Package a Development build for the agreed platform, then launch a minimal test map on an available test runner/device.
6. Archive exact commit, environment, commands, logs, test results, package checksum and artifact location.

### Phase C — feature/integration milestones

- Require contract review, owner approval, clean compilation, targeted automated tests, and a smoke test for each integrated feature slice.
- Run broader automation and packaged-map tests on scheduled builds and milestone candidates; run packaged Shipping build checks on release candidates.
- Add performance captures only after reference hardware, fixed map/route/settings, and an approved performance budget are defined. Compare identical conditions and retain raw captures.
- CI is operational only after the real workflow is committed, a runner has executed it successfully against the real pinned UE project, and logs/artifacts prove its behavior. Until then all relevant build/test gates remain **BLOCKED** or **NOT RUN**, not PASS.

No exact command, job matrix, test filter, or provider workflow is set here: target project, engine version, build host, platform SDK, and artifact service are undecided.

## 5. Agent 1 / Agent 2 interface review: evidence limits and dependency matrix

### What was available to review

No Agent 1 or Agent 2 system-specific interface proposal, source header, data schema, or implementation requirement document was present in the repository. The visible user material assigns role boundaries and general responsibilities, and the Master Engineering Architecture contains a **proposed** system-contract outline. A targeted Drive filename search for Agent 1/Agent 2 proposals found no dedicated files. The Drive search also surfaced broad Art Bible/location-register matches, which are not technical interfaces. Therefore, the detailed proposals requested for review are **not supplied/available in this checkout**. The matrix below is an integration-review agenda, not a finding that agents have approved these contracts and not authority to freeze them.

**Recommendation to Technical Director:** request Agent 1's current movement/combat proposal and Agent 2's world-system requirements (interfaces, types, ownership, lifecycle, failure modes, test seams, dependencies) before approving implementation. Review them together with the actual project source. The candidate owner labels below reflect the stated agent roles only; shared ownership and exact types must be agreed by those agents.

| Seam / shared concept | Candidate authoritative owner (for review only) | Dependency direction to review | Circular-dependency risk | Minimum test seam for first integrated slice |
|---|---|---|---|---|
| Player command/input and locomotion state | Agent 1 is the candidate owner of player movement; input/action routing ownership requires Agent 1's proposal | Controller/command producer → player movement implementation; Agent 2 consumes capability/state through a narrow contract and must not own locomotion internals | World actors directly calling player movement implementation or movement including world-specific actors | Deterministic command/state test; in-map move/look/jump or approved initial movement set; collision and camera-obstruction smoke test. Exact moves await Agent 1. |
| Combat action, health/damage result, targetability | Agent 1 candidate for combat/damage rules; Agent 2 candidate for enemy/world actor implementation. Shared types and ownership need explicit agreement. | Combat action applies a typed result through a small target/damage contract; world enemy implements it; encounter orchestration consumes outcome | Agent 1 combat including concrete Agent 2 enemy class while enemy AI includes concrete player combat class; two damage/health authorities | Once Stage 3 is approved: combat rules tested without map; one test target receives one deduplicated hit; world encounter verifies defeat/result transition. Not part of current implementation. |
| Interactable/world target query | Agent 2 candidate for world/interactable contract; Agent 1 candidate for player-side interaction command/query integration | Player asks through a narrow interface; world object validates/responds; no player code depends on concrete world implementations | Interface located in Agent 1 module while Agent 2 must depend on Agent 1 implementation, or reciprocal direct includes | Test candidate selection/range/visibility and response with a test interactable; verify unavailable/error response does not claim success. Exact semantics await proposals. |
| Traversal affordance/transition | Agent 2 candidate for authored world affordance; Agent 1 candidate for player movement execution/state. Exact control owner is unresolved. | World advertises permitted affordance; player system executes validated transition; state change/event is explicit | World directly teleports or mutates private movement state, or movement hard-codes chapter-specific actor types | Test start/cancel/completion and invalid/unavailable transition on a representative test actor. Traversal types are not selected here. |
| Enemy AI and encounter lifecycle | Agent 2 candidate, consuming Agent 1 combat/damage contracts | Encounter/AI → shared target/damage/action capability; not to player implementation internals | Enemy behavior owns a second health/damage/action system or has compile-time references to player feature module | State/phase test without map; encounter start/complete/fail idempotence; later packaged test encounter. |
| Progression, objective, memory and save state | Agent 2 is role-adjacent for world progression, but authoritative save owner and cross-chapter campaign-state owner are not specified by the supplied proposals. Agent 3 can validate, not own gameplay semantics. | Gameplay/world emits stable-ID event → campaign state owner persists/validates it; save service depends on neutral DTOs, never live actors | Save service imports both feature modules; chapter actor directly owns global progression; mutual dependencies between world and campaign services | Pure prerequisite/memory-gate test and save/load round trip once owner/schema approved. No save format implementation until decided. |
| Shared IDs, tags, event payloads, common enums | Joint decision with named maintainer; possible contract module only if proven necessary | Stable, low-level contract surface → both feature implementations; avoid feature-to-feature dependency | “Shared” module grows gameplay behavior or imports both sides; different agents invent duplicate ID/type vocabularies | Compile-time contract test, duplicate/missing-ID validator, producer-consumer test fixture. Naming/version policy unresolved. |
| Camera and world/cinematic control handoff | Agent 1 candidate for player camera/input handoff; Agent 2 supplies world/cinematic triggers; presentation owner needs confirmation | World sends request/state change through controller/camera interface; no world actor takes camera ownership silently | Level BP changes camera state independently of player controller or sequence code strands input | Test request/release/interrupt/restore of camera and input. Cinematic policy must be authored/approved. |

### Candidate contract/module rule (not a frozen API)

Keep shared interfaces limited to values and operations actually used by both owners. Prefer stable IDs, small event payloads, documented ownership/lifetime, and explicit result/error states. A contract boundary must not own player movement, combat tuning, AI decisions, quest semantics, or narrative facts. Agent 3 recommends detecting include/build cycles and running consumer contract tests; Agent 3 does not decide the gameplay meaning of those APIs.

## 6. Proposed first integration milestone (subject to Agent/TD review)

**Milestone M0 — Project foundation / clean toolchain proof.** This is the first integration gate, not a playable feature and not implemented now.

- **Entry conditions:** canonical project location and rights confirmed; UE5 minor version/host/build platform selected; platform assumptions and network scope recorded; Agent 1/2 submit their current contracts; Tech Director approves module/project plan; available engine host and source/binary policy identified.
- **Scope:** create/open the real project with approved UE tooling; record initial clean baseline; agree one game runtime module and the initial owner/API map; establish a test map/automation entry point/build wrapper. No character, combat, enemy, campaign, art import, or story implementation is authorized by this milestone.
- **Owners:** project/toolchain and verification — Agent 3; player/gameplay module contract — Agent 1; world/content/test-map requirements — Agent 2; cross-system/module review — Technical Director. These proposed assignments do not change creative authority.
- **Exit criteria:** project opens in pinned UE; clean Development/editor target builds on selected runner; documented test command executes at least one real Unreal automation smoke test; a package or explicitly deferred package gate for unsupported SDK has a recorded result; build/test logs tied to commit; no undocumented plugin/module dependency; Agent 1/2 contracts reviewed and dependency graph has no cycle.
- **Status now:** **BLOCKED** by absent project, unavailable UE toolchain, undecided platform/engine version, and missing Agent 1/2 proposals. No work on M0 has started.

**First feature integration after M0 — Movement/world-interaction lab (candidate):** a clearly labelled non-campaign test map, with Agent 1's approved minimal controllable-character movement/camera contract and one Agent 2-owned test interactable (and only a test target/encounter if their reviewed contracts require it). Test input-to-movement and player-query-to-world-response independently; avoid imported concept art and unapproved visual canon. This is a validation fixture, not a Chapter 1 production level or a claim of complete gameplay. Agent 1/2 and TD must agree the exact scope before implementation. Combat integration follows the project's required stage ordering and approved weapon/animation dependencies.

## 7. Decisions required before project bootstrap

### Creative Director / product owner

1. Is there an existing canonical UE project outside this repository? If so, provide its location/branch and authorize inspection/integration. If not, explicitly authorize creation after this plan is approved.
2. What is the first development target platform/OS? Is Win64 desktop acceptable as a temporary Development target, or should the first target differ?
3. Is the game single-player only for the initial project, or must multiplayer/network replication be supported? What are the intended eventual release platforms and distribution constraints?
4. What minimum/recommended reference hardware, resolution, and frame-rate/quality targets should Stage 1 use? These are needed for build/performance gates, not to assert a current target.
5. Confirm the intended source/binary asset strategy (including Git LFS suitability, team access/quota, and approved Drive-to-Content import ownership).

### Technical Director / system owners

6. Select/pin the UE5 minor version and supported host/toolchain once the canonical project and platform access are known.
7. Agent 1: submit current movement/camera and combat/health/targetability API proposal, movement-state ownership, dependencies, cancellation/failure behavior, and test requirements.
8. Agent 2: submit current interactable/traversal, AI/encounter, progression/save, and world-state requirements, including data/event ownership and test map expectations.
9. Jointly agree first-slice contract IDs/types, public API location, module dependency direction, and one named owner per system. Agent 3 reviews cycle and test risks; TD approves architecture changes.
10. Approve plugin allowlist and CI/build runner/artifact environment. Until a real UE workflow executes, status stays not operational.

## 8. Recommendation to the Technical Director

**Approve the hold and the M0/M1 sequencing as a proposed review plan; do not authorize gameplay implementation or a new `.uproject` in the current sandbox.** The next engineering action should be to identify the canonical Unreal project or explicitly authorize a new project, select a real UE/toolchain/platform, and obtain Agent 1/2 interface proposals. Agent 3 can then compare those proposals against the existing project, refine the dependency matrix with named owners, define test fixtures, and report a real baseline build before accepting integration work.

Until those decisions are complete:

- project bootstrap/build/test/package/performance: **BLOCKED** or **NOT RUN** as defined above;
- CI: **NOT OPERATIONAL**;
- game implementation/first playable milestone: **NOT STARTED**;
- performance targets: **NOT MEASURED**;
- architecture and interface matrix: **PROPOSED, pending owner review**.
