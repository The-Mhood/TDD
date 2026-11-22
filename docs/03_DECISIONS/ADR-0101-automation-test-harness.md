# ADR-0001 — Unreal Automation framework as the only in-engine test harness

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 3 (Integration / Technical Quality)
- **Affects:** all agents

## Context

The project needs automated tests that run without a human in the editor, can be executed from CI on a
build machine, and do not add third-party dependencies. Three candidate approaches exist: Unreal's built-in
Automation framework, a third-party C++ test framework (Catch2/GoogleTest) integrated into a UE module, or
scripted in-editor tests.

Third-party frameworks require build-system surgery, do not understand UObjects/GC/world contexts, and
create an unbounded maintenance surface across three agents. Scripted tests cannot assert on C++ internals.

## Decision

Use the **Unreal Automation framework exclusively**:

- `IMPLEMENT_SIMPLE_AUTOMATION_TEST` for small behavioural assertions.
- `IMPLEMENT_COMPLEX_AUTOMATION_TEST` / `DEFINE_SPEC` (Automation Spec) for parameterised and BDD-style suites.
- Test sources live in `Source/TDDTests/`.
- Naming: `TDD.<Area>.<Behaviour>` — e.g. `TDD.Memory.Director.SecondGrantRejected`.
- All gameplay-facing tests are tagged so CI can run subsets:
  `EAutomationTestFlags::EditorContext | EngineFilter | ProductFilter`.
- Execution from CLI:
  `UnrealEditor-Cmd.exe <project>.uproject -ExecCmds="Automation RunTests TDD;Quit" -unattended -nullrhi -nopause -testexit="Automation Test Queue Empty" -ReportExportPath=...`

**No hidden third-party test dependency.** Host-side tooling (canon validation, save-format checks) uses
Python's stdlib `unittest` only.

## Consequences

**Positive**
- Zero additional dependencies; nothing to license or update.
- Runs headless with `-nullrhi`, so cheap CI.
- Tests understand the engine: worlds, ticking, GC, data assets.
- Report output is machine-parseable (`-ReportExportPath`), which is what our evidence format needs.

**Negative / risks**
- Automation Spec syntax is less familiar than gtest/Catch2; new engineers need a short ramp.
- `-nullrhi` means no rendering coverage. Rendering/canon-visual checks need functional tests with a GPU
  machine or manual evidence — recorded in `Docs/production/STAGE_GATES.md`.
- Test discovery is implicit (reflection), so a typo'd flag silently omits a test from a run. Mitigation:
  CI asserts an **expected test count** per run; a drop in count fails the build.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| GoogleTest/Catch2 in-module | Build-system complexity, no UObject awareness, duplicate runner infrastructure for three agents |
| Blueprint-only testing | Cannot assert on C++ invariants or determinism; slow; review-hostile |
| Manual QA only | Fails the directive's "testable" and "evidence" requirements outright |
