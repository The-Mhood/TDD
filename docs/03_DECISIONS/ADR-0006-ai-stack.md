# ADR-0006 — AI on StateTree + AIPerception + combat director tokens

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 2

## Context
Enemies and bosses need readable, fair, maintainable behaviour. Options: Blueprint behaviour trees (old), C++ behaviour trees, StateTree, or bespoke state machines. Separately, third-person action games fail if enemies attack simultaneously; coordination must be a first-class system, not a per-enemy hack.

## Decision
- Behaviour selection: **StateTree**, one tree per archetype, authored so a designer can add a behaviour without C++.
- Perception: `UAIPerceptionComponent` (sight, hearing, damage).
- Combat decision: `UTDDCombatBrainComponent` selecting from the archetype's attack set, constrained by the **combat director** token system.
- Coordination: `UTDDCombatDirectorSubsystem` with a pure-function token policy (`FTDDAttackTokenPolicy`), unit-tested.
- Bosses: `UTDDBossComponent` + data-driven phases with a pure-function phase selector.

## Consequences
- **Positive:** fair fights by construction; testable coordination and boss selection without playing the game.
- **Positive:** designers extend enemies via data, not code.
- **Negative:** StateTree learning curve; schema/version churn across engine upgrades is a real (small) risk.
- **Negative:** the token system needs tuning per encounter type; a single global setting will feel wrong everywhere.

## Verification
`TDD-Unit.AI.TokenPolicy` and `TDD-Unit.AI.PhaseSelectorWeights`; `TDD-Functional.AI.TokenLimitsSimultaneousAttackers` with 6 enemies and a measurement of concurrent attackers over 60 s.
