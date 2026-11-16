# ADR-0002 — C++-first gameplay, Blueprints for content wiring only

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 1 (primary), all agents affected

## Context
Blueprints are fast for prototyping and slow for large-team iteration: merge conflicts are unresolvable binary conflicts, logic is hard to review, unit testing is limited, and performance hotspots are invisible. Three agents write into one codebase with no shared editor session.

## Decision
- Gameplay rules, state machines, damage, AI decisions, persistence and validation: **C++**.
- Blueprints: content wiring (asset defaults, event hookups to VFX/audio, level-specific setup), UI widget layout, and designer-facing data authoring.
- Every Blueprint that alters gameplay must be a thin subclass of a C++ class with no logic beyond property values.

## Consequences
- **Positive:** reviewable, diffable, testable, no binary merge conflicts in logic.
- **Positive:** automation tests can exercise systems without loading a Blueprint graph.
- **Negative:** slower iteration for pure-tuning changes than BP-only workflows — mitigated by data assets and console variables.
- **Negative:** requires C++ competence on all three agents; a designer cannot implement a mechanic alone.

## Verification
Phase 0 skeleton contains zero gameplay Blueprints. Code review rejects gameplay logic found in BP events.
