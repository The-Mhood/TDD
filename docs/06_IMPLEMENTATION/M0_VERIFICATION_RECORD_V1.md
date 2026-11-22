# M0 — Unreal Foundation Verification Record v1

**Status: `PASSED`** — Gates B and C, from a real Mac run.
**Executed by:** the Project Owner, on macOS (Apple Silicon), 2026-11-18.
**Recorded by:** Agent 1, from the owner's supplied results. **Agent 1 did not execute this run** — there is no Unreal Engine in Agent 1's workspace — and has not inspected the raw logs (see §5).

This record closes M0 as a blocker for M1. It does not close Gate A or Gate D, which are recorded honestly below rather than silently marked pass.

## 1. Identity of the verified tree

| Field | Value |
|---|---|
| Canonical branch | `arena/c64fc525-tdd` |
| Commit | `e71401b674ac5987b4eed6f46330b8b22c09e9b2` — "Count automation start events across UE log formats" |
| Descriptor | `TheDisobedientDaughter.uproject` (`EngineAssociation` 5.8, one `Runtime` module, `TargetPlatforms` Mac + Windows) |
| Module | `TheDisobedientDaughter` (single runtime module; `IMPLEMENT_PRIMARY_GAME_MODULE` present) |
| Engine | Unreal Engine 5.8 |
| Host | macOS, Apple Silicon; Xcode 26.x (`Tools/engine/mac_build.sh` on this commit refuses below 26.0 and refuses 26.4) |
| Evidence | `Saved/BuildEvidence/20261118T202235Z` (owner's Mac, `~/tdd-m0`) |

## 2. Results as supplied by the owner

| Step | Result |
|---|---|
| Project readiness | **PASS** |
| Project file generation | **PASS** |
| `TheDisobedientDaughterEditor` | **BUILD PASS** |
| `TheDisobedientDaughter` | **BUILD PASS** |
| Automation tests discovered | 2 |
| Started | 2 |
| Completed | 2 |
| Passed | 2 |
| Failed | 0 |

The two discovered tests are verifiable in the tree at this commit:
`TDD.Foundation.GameModeClass` and `TDD.Movement.DodgeDistanceMath` (both `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, `EditorContext | EngineFilter`). Their presence and names were checked by Agent 1 in the source; their **execution** is the owner's report, not Agent 1's observation.

## 3. Mapping against `docs/M0_UNREAL_FOUNDATION_CHECKLIST.md`

| Gate | What the checklist requires | What this run supplies | Recorded as |
|---|---|---|---|
| **A** — project opens in the pinned editor, twice, with the test map loaded | Editor log showing project + engine version, module load, map opened, no fatal error; second open from the same commit | Not in the supplied summary. The headless automation run does load the project and modules, but no map-load evidence and no second-open evidence was supplied | **`NOT EVIDENCED`** (not `FAIL`; not attempted as specified) |
| **B** — clean build succeeds | Full command, toolchain versions, raw log, exit `0`, artifact path/checksum, second clean run | Both targets built on the Mac from a fresh clone of the exact commit; command/exit codes/checksums not supplied | **`PASS` on owner attestation**; artifact checksums and the second clean run **`NOT EVIDENCED`** |
| **C** — a real Unreal Automation test executes and passes | Named project test discovered, started, completed, assertions, zero failures, exit `0` | 2 discovered / 2 started / 2 completed / 2 passed / 0 failed | **`PASS`** |
| **D** — optional packaged launch | Cook/package/launch, or explicit out-of-scope | Not attempted | **`NOT RUN`** (outside M0 scope) |

## 4. What M0 passing does not establish

- Windows x64 has not been built. `TargetPlatforms` lists it; nothing has compiled for it.
- Packaging/cooking has never run (Gate D), so "it builds" is not "it ships".
- No CI exists; the run was local. Reproducibility (a second cold run, AC-31) is unproven.
- No performance measurement (AC-28) has been taken.
- `TDD.Movement.DodgeDistanceMath` passing proves the **clearance maths** is correct in the engine's process. It does not prove a dodge works in a world: no sweep against geometry, no character movement, no montage, no floor validation. That is M1 work (spec §3.5, AC-19/AC-21).
- Nothing in M1 is playable. There is no character, camera, input mapping or test map in the tree yet.

## 5. Evidence location and its limits

Evidence is on the owner's Mac at `~/tdd-m0/Saved/BuildEvidence/20261118T202235Z`. `Saved/` is in `.gitignore`, so **these logs are not in the repository** and no other agent can inspect them. That is acceptable for a local run, but it means the record rests on the owner's attestation.

To make the evidence inspectable without committing build output, commit only the machine-readable report plus a short manifest:

```bash
cd ~/tdd-m0 && mkdir -p docs/06_IMPLEMENTATION/evidence/20261118T202235Z \
  && cp Saved/BuildEvidence/20261118T202235Z/automation-report/index.json docs/06_IMPLEMENTATION/evidence/20261118T202235Z/ \
  && (cd docs/06_IMPLEMENTATION/evidence/20261118T202235Z && shasum -a 256 index.json > SHA256SUMS) \
  && git add -f docs/06_IMPLEMENTATION/evidence/20261118T202235Z \
  && git commit -m "TDD-build: archive the M0 automation report and its checksum"
```

## 6. Reproduce

```bash
cd ~/tdd-m0 && git fetch origin && git checkout e71401b674ac5987b4eed6f46330b8b22c09e9b2 \
  && Tools/engine/mac_build.sh --engine "/Users/Shared/Epic Games/UE_5.8" --test-filter TDD
```

Writes a new `Saved/BuildEvidence/<UTC>/` and exits `0` only if both targets build and the queue runs.

## 7. Sign-off

| Role | Name | Status |
|---|---|---|
| Executed the build and test run | Project Owner (Mac) | **PASS**, 2026-11-18 |
| Recorded the result | Agent 1 | this document |
| Independent review of the evidence | Agent 2 | **pending** |
