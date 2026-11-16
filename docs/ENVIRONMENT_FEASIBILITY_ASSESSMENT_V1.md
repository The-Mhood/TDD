# Unreal Environment and Toolchain Feasibility Assessment

**Document:** `TDD-M0-ENV-001` · **Version:** 1.0
**Date:** 2026-11-16 UTC
**Prepared by:** Agent 3 — Integration / Technical Quality
**Status:** Agent-workspace inspection complete; production environment unknown. No UE version selected.

## 1. Scope and conclusion

This is an assessment of the inspected **agent workspace only**. It establishes limitations of this Linux sandbox; it does **not** establish whether Unreal Engine is available, installed, licensed, accessible or usable on the intended production workstation. No Unreal project was opened, created or built. No runtime or Unreal Automation Test was run.

**Workspace feasibility:** BLOCKED for Unreal project generation/open/build/automation based on the inspected environment.
**Production-workstation feasibility:** NOT ASSESSED — the intended editor host and its owner have not been identified or inspected.
**Version recommendation:** defer exact version selection. Do not choose UE 5.8 or another release without compatibility evidence from the intended host/target combination.

## 2. Assessment dimensions

| Dimension | Current finding | Evidence / limitation | Required follow-up |
|---|---|---|---|
| Intended Unreal Editor host | Unknown | No production workstation, operator or remote build host was named in the decision request. The agent sandbox is not presumed to be the editor host. | TD/project owner identifies the editor host and who can run the M0 checks. |
| Host OS and hardware | Agent workspace only: Linux `x86_64`, kernel `6.1.158+`; 2 visible CPUs; about 3.85 GiB total RAM and about 3.60 GiB available RAM at inspection. | `uname -a`, `/proc/meminfo`, `nproc`; sandbox resource view only. No production GPU, disk, driver or workstation inventory supplied. | Record production host OS/build, CPU, RAM, GPU/driver, disk capacity and available workspace. |
| Candidate target platform | Unknown / unselected | No target OS, device family, SDK or distribution chosen. Agent host OS does not determine game target. | TD selects initial target platform(s), development configuration and required SDKs. |
| Engine distribution and version | Unknown / unselected | No Unreal installation found in inspected workspace paths. A `.uproject` on Agent 2's separate branch is not installation/version compatibility evidence. | Inventory available launcher/source distributions on intended host; record exact UE major/minor/patch/build and distribution after a compatibility spike. |
| Compiler and SDK requirements | Agent workspace has `/usr/bin/g++` Debian 12.2.0 and Python 3.11.2. `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh`, `dotnet`, `clang++` and `clang` were not found on `PATH`. | Inspected common roots `/opt`, `/usr/local`, `/home/user/UnrealEngine`, `/home/user/UE` and `/mnt` to depth 4; no `UnrealEditor`, `UnrealBuildTool`, `RunUAT.sh` or `UE_5.*` found. This bounded search cannot prove machine-wide absence. `g++` is not a substitute for a matching Unreal toolchain. | On intended host, verify UE-required compiler, IDE/toolchain, SDK, build tools and target-specific prerequisites against the chosen release. Capture actual versions and access. |
| Plugin compatibility | Unknown | No final plugin allowlist, target engine version or production plugin inventory has been approved. Agent 2 branch plugin declarations are not an approved canonical list and were not tested. | Identify required plugins, source/binary distribution and support for exact engine version, host and target. Test load/build on actual project. |
| Actual engine availability and access | Agent sandbox: no UE editor/build tools found in the inspected locations/PATH. Production workstation: unknown, not checked. | No credential/license/access check, installer inventory, editor launch or project generation was attempted. | Named operator confirms launcher/source availability, account/license/access, install path, disk space and ability to run Editor/UBT/Automation. Do not request credentials in repository/chat. |

## 3. Version recommendation and selection gate

**Recommendation: defer pinning an exact version.** The choice must be driven by the intended editor host, candidate target platform, matching compiler/SDK, plugin availability and production access. No evidence here distinguishes UE 5.8 from another minor release as compatible or supportable for TDD.

After the host and target are named, the TD should select from versions actually available on that host, favoring the newest production-suitable UE5 release that passes all of the following on that exact host/target/plugin set:

1. Project opens in the selected Editor and can be closed/reopened from a clean checkout.
2. Official build tooling compiles the project for the approved editor/development target using the matching compiler and SDK.
3. The approved plugin allowlist loads and builds without missing modules or unsupported target dependencies.
4. A project-owned Unreal Automation Test is discovered, executed and produces a report tied to the same project commit and engine build.
5. Version, distribution, toolchain, target and plugin identity can be recorded reproducibly in the M0 manifest.

Only after this evidence should the exact engine version/build be recorded as selected. This recommendation does not assert which version is latest, installed, supported or compatible; those facts must be checked on the chosen host.

## 4. M0 readiness snapshot

| M0 prerequisite | Status |
|---|---|
| Canonical TDD repository and local branch identity recorded | PASS — see §5 of `TD_CROSS_AGENT_INTEGRATION_DECISIONS_V1_1.md` |
| Canonical `.uproject` exists | NO — none found in the canonical working tree at assessment time |
| Intended Editor host identified | BLOCKED / NOT PROVIDED |
| Exact engine version/distribution pinned | BLOCKED / NOT SELECTED |
| Compiler/SDK and target platform verified | BLOCKED / NOT SELECTED |
| Plugin compatibility verified | NOT RUN / plugin allowlist not selected |
| Editor open/reopen | NOT RUN |
| Clean Unreal build | NOT RUN |
| Project-owned Unreal Automation Test | NOT RUN; no canonical project/test module exists |
| Captured Unreal evidence bundle | NOT RUN |
| M0 pass | **NOT PASSED** — M0 evidence gate is not met |

A dirty documentation worktree is not an Unreal project and is not a clean-build baseline. The local branch has uncommitted/untracked documentation work; see the exact P0 record in the v1.1 addendum. No project creation or runtime implementation is authorized by this assessment.
