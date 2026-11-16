# M0 — Unreal Foundation Evidence Checklist

**Purpose:** define exactly what evidence is required before reporting that the authorized Unreal project opens, builds, and runs a real automation test.
**Status:** preparation only. No project creation or gameplay implementation is authorized by this checklist.
**Current state:** **BLOCKED** — canonical project and UE toolchain are not available in this workspace.
**Owner:** Agent 3 for evidence collection and quality gate; project and system ownership remain with the Technical Director and assigned agents.

## 1. M0 entry authorization

Do not start project bootstrap until the Technical Director records all of the following:

- Canonical source repository and branch/path, and whether it already contains an Unreal project.
- Explicit authorization to create a new project **only if** no canonical project exists. Record the authorizing decision/date; do not infer authorization from this checklist.
- Approved project/module name and location. Do not move, replace, or overwrite existing source or project files.
- Exact UE5 version (major, minor, patch/build) and source/launcher distribution; selected host OS, compiler/toolchain, build configuration, platform SDK/version where applicable.
- Initial development platform and network scope; distinguish a temporary Development target from shipping-platform approval.
- Plugin allowlist and binary-asset/source-control policy, including whether Git LFS is approved and how art-bible source assets are imported.
- Agent 1/2 system interface proposals and a named reviewer/owner for each contract. M0 does not approve player movement, combat, world, narrative, or visual design.

**Entry-gate status:** `BLOCKED` until all required choices above are recorded and the owner can access the authorized engine/toolchain.

## 2. Evidence bundle and identity

For every M0 attempt, create an immutable evidence bundle associated with the exact Git commit and environment, outside Git-generated directories or in the team's approved artifact store. Do not commit DerivedDataCache, Intermediate, or temporary build output merely to preserve evidence.

Required identity manifest (`M0-manifest.md` or machine-readable equivalent):

- Project repository URL, branch, full commit SHA, and clean/dirty status (`git status --short --branch`).
- Project file path/name and checksum; exact project/module/target names.
- UE version/build identifier, editor executable/source, host OS, compiler, SDK and build tool versions.
- Enabled plugins with versions; selected target platform, configuration, map, command, environment variables that affect the run (excluding secrets).
- Date/time, operator, runner/device identifier, and artifact links/checksums.
- Explicit results for each gate using only: **PASS**, **FAIL**, **BLOCKED**, **NOT RUN**, **NOT MEASURED**. Explain every non-PASS; never collapse a missing prerequisite into PASS.

Preserve raw editor, build, and automation logs, test report output, and relevant editor/compiler diagnostics. Screenshots/video may supplement evidence but do not replace logs, test assertions, command/exit status, or commit identity.

## 3. Required gates and exact pass evidence

### Gate A — Authorized project opens in the pinned Unreal Editor

**Procedure**

1. Start from the canonical project checkout at the manifest's commit; verify no unrecorded source/config changes.
2. Open the recorded `.uproject` with the exact UE version in the manifest using the supported editor workflow for that host.
3. Wait for project/module load and initial shader/asset processing to finish; open the designated M0 test map. Do not count an OS file association, text editor, generated project file, or fabricated descriptor as opening in Unreal.
4. Close and reopen once from the same clean checkout to check the result is reproducible. If the editor prompts to rebuild/recompile, record the exact prompt and outcome; unexplained project conversion or plugin prompts are not silently accepted.

**Required evidence for PASS**

- Editor log from the exact run showing project path and engine version, module/plugin load completed, map opened, and no fatal error, missing module, unresolved required plugin, or failed project conversion.
- A saved copy of the raw editor log and any generated diagnostics; record process exit status on normal close.
- Screenshot of the editor with project/map identity visible as corroboration only.
- Successful second open from the same clean commit (log or recorded repeat result).

`FAIL` means the authorized, available editor attempted to open the supplied project and an acceptance condition failed. `BLOCKED` means the project, version, license/access, or editor environment was unavailable. If not attempted despite availability, report `NOT RUN`.

### Gate B — Clean project build succeeds

**Procedure**

1. Use a clean checkout/workspace at the recorded commit. Do not rely on untracked local files or stale binaries to make the build pass. Record whether the build is cold/clean and any cache policy.
2. Invoke the official Unreal Build Tool/installed build entry point for the authorized editor or Development target, using the exact host/toolchain/configuration recorded in the manifest. The exact command line depends on the approved UE version and host; record the command actually executed—do not copy an untested placeholder command into the evidence.
3. Capture complete standard output/error and tool log, final process exit code, target/configuration, elapsed time, compiler warnings/errors, and produced executable/target artifact path and checksum where applicable.
4. Run the same documented command once again from a clean/reset build state or a second clean workspace to demonstrate reproducibility. Document caches intentionally shared.

**Required evidence for PASS**

- Full build command and invocation context, exact toolchain versions, full raw log, and exit code `0`.
- Build log reports the expected project/target and completes without compiler/linker errors; all warnings are listed/classified, with no unexplained new warning hidden.
- Identifiable output artifact and checksum; second clean run succeeds under the documented clean-workspace/cache policy.
- Commit and worktree status match the identity manifest.

A successful editor launch without a build log is not a build PASS. A pre-existing executable is not proof that this commit builds. If no matching toolchain/SDK is available, status is `BLOCKED`, not `FAIL` or `PASS`.

### Gate C — A real Unreal Automation Test executes and passes

**Minimum M0 test requirement**

Implement at least one project-owned test in Unreal's actual Automation Test Framework (not a shell script that echoes success, a Python-only check, a manually clicked test map, or a test that unconditionally returns true). Name it in a stable project namespace, for example `TDD.Foundation.ProjectSmoke` (final name is project-owner-approved).

The test must make meaningful assertions against the real project and content. A suitable M0 foundation test can verify that the project runtime module/class is available and that the designated M0 test map can be loaded and has its expected world/game-mode configuration. It should fail if the map/package/class is missing or cannot load. It need not implement gameplay systems, and it must not claim movement/combat/world gameplay works. If this specific test shape is incompatible with the selected UE version, agree an equivalent assertion with Agent 3 and the Technical Director before using it.

**Procedure**

1. Compile the test into the approved editor/development target as part of Gate B.
2. Run it using the selected UE version's real Automation Framework runner (for example, the editor's automation command/runner; exact invocation and flags must be verified for the pinned version). Record the full command, target/device, test filter, process exit code, and complete raw test log/report.
3. Verify the log/report names the exact project test, shows it started and completed, lists its assertions/result, and records zero failed, aborted, or unexecuted required tests. Confirm the report belongs to the manifest's commit and test binary.
4. Repeat once from the documented clean state or CI runner after the workflow exists. Until there is an actual workflow run, mark it as a local automation run—not CI.

**Required evidence for PASS**

- Test source path and review showing concrete assertions; compiled target/build identity.
- Actual Unreal Automation Framework result/log and report for the named test, including assertion output and a final pass summary.
- Runner invocation, environment/UE versions, process exit status `0`, and no automation errors/crash/timeout.
- Reproducible repeat from a clean state or a second approved runner; if this cannot yet be done, report the first run separately and keep reproducibility `NOT RUN`.

A process exit code alone is insufficient if the test was not discovered/executed. A green UI without the test name/assertion report is insufficient. Do not mark a test PASS because the editor itself opened.

### Gate D — Optional M0 packaged launch

If the platform SDK and runner are available and the Technical Director includes packaging in M0, record the exact cook/package command, platform/configuration, package checksum, install/launch device, logs, map startup, clean exit, and any save-directory result. Otherwise report packaging as `BLOCKED` or `NOT RUN` with the reason; do not imply Gate A–C prove a package works.

## 4. Repository-level validation and truthful status

Before each M0 commit, Agent 3 records the diff and runs local whitespace/link/document checks, stages only intended files, checks the staged diff, and verifies the branch/commit. This validates the repository change only; it does not validate the Unreal project.

After a real project exists, proposed CI should separately run: pinned-toolchain assertion, clean project compilation, asset/config validation, selected fast Unreal Automation Tests, and packaged Development smoke checks on an approved runner. The workflow is **not operational** until the committed workflow has executed successfully against the real authorized project and its logs/artifacts are available. Record CI state as `NOT RUN` before its first execution, then `PASS` or `FAIL` based on the actual run; missing runner/license/SDK is `BLOCKED`.

## 5. M0 exit checklist

M0 may be reported **PASS** only when all mandatory conditions below are evidenced against the same authorized project and compatible commit/toolchain:

- [ ] Authorization and canonical project identity recorded; project is not a competing/unapproved scaffold.
- [ ] UE version, host/toolchain, target and plugin list pinned and recorded.
- [ ] Clean checkout opens twice in the pinned Unreal Editor; Gate A evidence archived.
- [ ] Clean build succeeds reproducibly; Gate B logs, exit code, target and artifact recorded.
- [ ] At least one meaningful project-owned Unreal Automation Test is discovered, executed and passes; Gate C logs/report, assertions and exit code recorded.
- [ ] README/docs accurately distinguish planning, implementation, local validation and CI state.
- [ ] Any package requirement is either passed with evidence or explicitly outside M0 scope; no false package claim.
- [ ] Agent 1/2 contracts and module/dependency ownership are reviewed, with open questions logged; no contract is silently frozen by Agent 3.
- [ ] Quality ledger updated with commit, exact files, results, evidence locations, defects/risks, and release-readiness status.

**Current result:** M0 is **BLOCKED**. This checklist defines future evidence; it records no engine/project operation and authorizes no gameplay implementation.
