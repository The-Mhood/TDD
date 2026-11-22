# ADR-0004 — Adopt GAS for attributes/effects; keep attack flow custom

- **Status:** Proposed (requires TD confirmation before Phase 2)
- **Date:** 2026-11-16
- **Owning agent:** 1

## Context
The game needs health, stamina, posture, damage modifiers, buffs/debuffs, cooldowns and progression-driven stat growth. UE offers the Gameplay Ability System (GAS) or hand-rolled components. GAS brings attribute maths, modifier stacking, duration effects and tag-based immunity that are easy to get subtly wrong by hand — but its ability/task model is awkward for frame-precise melee combat that must expose cancel windows and explicit hit windows to animation.

## Decision
Use GAS for the **attribute and effect layer** (`UTDDAttributeSet`, `UGameplayEffect`, status tags, immunity/blocking, cooldown primitives). Do **not** implement attack flow as GAS abilities: attacks are driven by `UTDDCombatComponent` + animation notifies, producing `FTDDDamageRequest` objects that are applied through GAS effects. GAS is wrapped behind a small adapter so that only a few files know GAS types.

## Consequences
- **Positive:** correct, tested attribute maths; clean progression modifiers; status tags integrate with animation and AI naturally.
- **Positive:** combat timing stays explicit, greppable and unit-testable without the ability system.
- **Negative:** two systems to understand; risk of someone "helpfully" moving combat into abilities — hence this ADR.
- **Negative:** GAS adds initialisation complexity (`InitAbilityActorInfo`, `AbilitySystemGlobals`).

## Alternatives considered
- **All-GAS** — poor fit for melee cancel windows; harder to unit test.
- **No GAS** — reimplementing modifiers/effects, a known source of balance bugs.

## Verification
Phase 2: `TDD-Unit.Combat.*` must run with no world and no ability system initialisation for pure maths; attributes must only change through effects (review rule).
