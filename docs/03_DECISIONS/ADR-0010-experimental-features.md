# ADR-0010 — No experimental engine features in shipping paths

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 3

## Context
UE 5.8 ships several attractive features that are not production-ready. Shipping a multi-year project on experimental tech risks API churn, missing platform support and silent quality problems.

## Decision
Shipping paths use only Production-Ready features. Excluded: Mesh Terrain (Experimental), MetaHuman Crowd (Experimental), MCP editor plugin (Experimental), Substrate (deferred), Lumen Lite (Beta; min-spec evaluation only, behind a switch). Adopted production-ready: Nanite, Lumen, VSM, TSR, World Partition, HLOD, StateTree, MetaSounds, Sequencer, Control Rig, Chaos Cloth. Pose Search/Motion Matching is conditional on ADR-0005's verification step.

## Consequences
- **Positive:** predictable support and upgrade paths.
- **Negative:** no Mesh Terrain overhangs/cliffs in Chapter 2's underground kingdom — must be authored with Nanite meshes instead (a real art-pipeline cost, accepted).
- **Negative:** periodic re-evaluation effort as features reach production-ready.

## Verification
Phase 0 `.uproject`/plugin list contains no excluded plugin. Reviewed at every engine pin.
