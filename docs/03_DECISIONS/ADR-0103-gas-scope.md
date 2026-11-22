# ADR-0003 — GAS for combat abilities only; movement on Character Movement Component

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 1 (Gameplay, Character, Combat)
- **Affects:** Agent 1, Agent 2 (AI reads attributes), Agent 3 (UI reads attributes)

## Context

The Gameplay Ability System (GAS) is the standard Unreal solution for abilities, cooldowns, attribute
modification, gameplay cues and prediction. It is also heavy: it imposes ASC ownership rules, replication
assumptions, effect/policy architecture, and a learning cost.

Some studios run **locomotion through GAS** as abilities. That is attractive for animation-driven combat but
introduces a well-known class of problems: input latency through the ability pipeline, difficulty mixing
root motion with free locomotion, and awkward interaction with `CharacterMovementComponent` (CMC).

Three agents must share this code. Complexity is therefore a direct integration risk.

## Decision

Split the responsibility:

| Concern | Owner system | Rationale |
|---|---|---|
| Walking, jogging, sprinting, strafing, dodging displacement, vaults, slides, air control | **CMC** (`UTDDCharacterMovementComponent`) | CMC is purpose-built, well-understood, tunable, and cheap to iterate |
| Attacks, parries, blocks, special abilities, damage application, status effects, poise, cooldowns, resource costs | **GAS** (`UTDDAbilitySystemComponent`) | Exactly GAS's job; gives us GameplayEffects, cues and clean data-driven tuning |
| Animation selection | Animation Blueprint driven by `FTDDLocomotionState` + montages | Presentation, not authority |

Explicit rules:

1. **Movement is never a Gameplay Ability.** Dodge is a movement-mode change on CMC with an
   invulnerability window exposed as a tag (`State.Combat.Invulnerable`).
2. **`TDDVitals` AttributeSet** holds Health, Stamina, Poise, Resolve. Only the damage pipeline and stamina
   consumers (movement/abilities) write to it, via GameplayEffects.
3. **AI never writes attributes.** AI reads them; damage is applied through `UTDDHitArbiter` → GameplayEffect.
4. **Animation cues are gameplay cues** (`UGameplayCueNotify_*`), so VFX/SFX fire from one authority, not
   from three places.
5. **No replication.** `ASC` is created locally; the project is single-player. `NetExecutionPolicy` is
   `LocalOnly` where it matters. We do not pay prediction costs we do not need.

## Consequences

**Positive**
- Input latency stays low: locomotion never traverses the ability queue.
- Iteration speed on feel (the single most important quality attribute for this genre) is high — tuning CMC
  parameters does not require ability-graph changes.
- GAS is confined to a small, well-bounded surface, which lowers integration risk for three agents.

**Negative / risks**
- Two authorities (CMC + GAS) mean a clear boundary must be enforced in review. Mitigation: the boundary is
  written in the header docs and enforced by a test that fails if an ability modifies `MaxWalkSpeed`
  directly instead of through the movement component's API.
- If we later want GAS-driven animation-driven traversal, this decision must be revisited with an ADR.
- GAS's default replication bookkeeping is unused overhead. Accepted: it is small, and removing it is more
  risk than value.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Full GAS for movement | Latency, root-motion/locomotion conflicts, higher integration risk across three agents |
| No GAS at all (custom ability system) | Re-implements effects, cues, cooldowns and attribute math for no gain; worse data-driven tuning for designers |
| CMC + custom ability layer with no attributes | No clean damage/poise pipeline; would end up rebuilding half of GAS informally |
