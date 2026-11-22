# ADR-0003 — Layered modules with downward-only dependencies

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 3 (owns module boundaries)

## Context
Three agents working in parallel in one game module will collide constantly: every system wants to include every other system's headers, and the build breaks become the merge tool.

## Decision
Nine modules: `TDDCore` (leaf), `TDDWorld`, `TDDGameplay`, `TDDAI`, `TDDNarrative`, `TDDUI`, `TDDEditor`, `TDDTests`, plus the primary game/editor targets. Dependency direction is strictly downward: Core ← World ← Gameplay ← AI; Narrative depends on Core + World; UI on Gameplay + Narrative; Editor on all. `TDDGameplay` may not include AI/narrative/UI headers; communication is via `TDDCore` events and interfaces.

## Consequences
- **Positive:** compile-time enforcement of the ownership matrix; parallel work without header collisions; faster incremental builds.
- **Positive:** a cycle is caught by the build, not by a heated conversation.
- **Negative:** more boilerplate (events instead of direct calls); some indirection for things that "would be simpler" as direct calls.
- **Negative:** more modules to configure.

## Alternatives considered
- Single game module (fast start, guaranteed collisions).
- One module per agent (too coarse: narrative and UI are different lifetimes).
- Plugin-per-system (overkill before systems exist).

## Verification
Phase 0: build with an intentional forbidden include must fail; record that failure as evidence the boundary is real.
