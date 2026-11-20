# ADR-0005 — Engine-side verification requirement

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 3 (Integration / Technical Quality)
- **Affects:** all agents, and every report submitted to the Technical Director

## Context

The current development environment has **no Unreal Engine**, **no GPU** and **no ability to launch a
`-nullrhi` editor**. Verified 2026-11-16: no `UnrealEditor` binary, no engine in `/opt`, no project files.

C++ can be authored here. Config can be authored here. Canon data and tooling can be **executed** here
(Python stdlib). Gameplay cannot be **executed** here.

There is an obvious failure mode for an AI-assisted production: an agent writes plausible C++, writes a
confident report saying "movement and camera are implemented and working", and the next agent builds on
untested code. Three rounds later the project has a beautiful architecture that has never compiled.

The directive explicitly forbids this: *"Never claim a system works without testing it"* and *"Do not
simulate functionality with visual placeholders and claim it is implemented."*

## Decision

1. **A claim of "working" requires engine-side evidence.** The minimum acceptable evidence for any runtime
   system is:
   - engine version + build ID,
   - the automation test name(s) and a PASS report file in `Docs/evidence/`,
   - for feel/presentation, a recorded session (link) and a written observation.
2. **In this environment, authored-but-unrun code is tagged SPEC or STUB — never ESTABLISHED.**
   Every report states, per item: `authored`, `compiled`, `executed`, `verified`. These are four different
   things and are never collapsed into "done".
3. **Stage 1 must produce the first engine-side evidence** (a headless build + one passing automation test)
   before any Stage 2 gameplay work is claimed complete. This is the project's first real gate.
4. **Static review is a valid but limited activity.** It catches design and interface errors; it does not
   catch compile errors, missing `#include`, GC problems, ticking bugs or perf. It is reported as review,
   not as verification.
5. **Waivers are explicit.** If the Creative Director accepts unverified work to unblock something (e.g.
   schedule pressure), it is recorded as a waiver in `Docs/evidence/waivers/` with the risk accepted and an
   expiry condition. Silent acceptance is a process violation.

## Consequences

**Positive**
- The project's reported state matches reality; downstream agents do not build on sandbags.
- The Technical Director can review real evidence instead of narrative.
- Front-loads the inevitable "it doesn't compile" cycle into Stage 1 rather than Stage 6.

**Negative / risks**
- Slower apparent progress: this agent will produce code that it cannot claim works. That is correct but
  may read as under-delivery. Mitigation: precise status reporting, and maximum value extracted from what
  *can* be verified here (canon gates, interfaces, data schemas, save format, tooling).
- Requires an engine-equipped machine (or CI runner) earlier than a "just write code" approach would.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Write C++ and report it as implemented | Explicitly forbidden by the directive; guarantees integration failure |
| Don't write C++ until an engine is available | Wastes the highest-leverage window: interfaces, schemas and data contracts are engine-independent |
| Mock the engine to "run" code | Produces false confidence; a mock engine tests the mock |
