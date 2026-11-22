# ADR-0001 — Pin Unreal Engine 5.8

- **Status:** Proposed (requires Technical Director confirmation)
- **Date:** 2026-11-16
- **Deciders:** Technical Director, Creative Director (cost/schedule context)
- **Owning agent:** 3 (Integration)

## Context
The project must choose one engine version at the very start. UE 5.8 shipped in June 2026 and is publicly described by Epic as the last planned major UE5 release, with UE5 entering bug-fix support and UE6 early access expected in 2027. A multi-year production cannot casually change engine branch mid-project: assets, plugins and shaders churn, and every upgrade costs a full regression cycle.

## Decision
Pin **Unreal Engine 5.8** (exact build recorded in `docs/02_PRODUCTION/ENGINE_PIN.md` once installed). Do not adopt UE6 during this production. Engine upgrades require an ADR and a full regression run.

## Consequences
- **Positive:** longest-lived, best-supported UE5 branch; plugin ecosystem has caught up; known-good feature set (Nanite, Lumen, VSM, TSR, World Partition, StateTree, Pose Search, MetaSounds, Sequencer, Control Rig).
- **Positive:** no migration risk to an unproven engine generation during production.
- **Negative:** no new UE6 features; eventual technical debt if a sequel uses UE6.
- **Negative:** 5.8 is not receiving new features, only fixes.

## Alternatives considered
- **UE 5.7** — older, narrower fix support, no benefit.
- **UE 5.6** — more battle-tested but similarly exposed; no reason to go further back for a new project.
- **UE6 early access (2027)** — unacceptable schedule and stability risk for a production already in flight.

## Verification / reversal conditions
Build a clean project on 5.8 on the production workstation; confirm every required plugin from MEAD §2.3 loads and that Pose Search / Motion Matching status is as assumed (see ADR-0005). If a required plugin is broken on 5.8, revisit before Phase 1.
