# ADR-0012 — Verification boundary for agent-authored work

- **Status:** Accepted (environmental fact, not a preference)
- **Date:** 2026-11-16
- **Owning agent:** 3 (enforces)

## Context
The agent workspace has no Unreal Engine, no .NET SDK, no MSVC/Clang, no GPU, 2 vCPU and 3 GB RAM. Agents can write source and documentation but cannot compile, run, cook, render or profile. Simultaneously, the project's rules forbid claiming functionality without testing. These two facts must be reconciled explicitly, or the project will accumulate confidently-described software that has never executed.

## Decision
1. Every agent-authored item carries a status from `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md`; default is `IMPLEMENTED_UNVERIFIED` or `DESIGN_ONLY`.
2. `IMPLEMENTED_AND_VERIFIED` requires external evidence (build log, automation report, perf capture) produced on the production workstation.
3. Phase gates cannot pass on unverified code; verification is the Technical Director's step.
4. Change batches stay small (one system per handoff) so verification is tractable.
5. Documentation is exempt from needing a build, but must not describe unimplemented behaviour as present.

## Consequences
- **Positive:** honest reporting; no virtual progress; the Creative Director always knows what actually runs.
- **Negative:** progress is gated by an external machine; throughput depends on the verification loop.
- **Negative:** agents will sometimes deliver unbuildable code; hence small batches and strict IWYU/export-macro standards.
