# ADR-0005 — Locomotion behind a provider interface (Motion Matching now, BlendSpace fallback)

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 1 (with animation team)

## Context
The brief calls for cinematic-quality character animation. Motion Matching (Pose Search) is the strongest UE5 technique for that, but it requires a large, well-tagged animation corpus that does not exist, and its 5.8 maturity for our use must be confirmed on the production machine. Committing the locomotion architecture to Motion Matching alone risks a stalled Phase 1 if clips are late.

## Decision
Define `ITDDLocomotionAnimProvider` with two implementations: `UTDDMotionMatchingProvider` (Pose Search) and `UTDDBlendSpaceProvider` (state machine + blendspaces). A project setting selects the active provider. The selected provider is shown in the debug HUD and asserted by an automation test.

## Consequences
- **Positive:** Phase 1 can complete and be measured with blendspaces; Motion Matching is adopted when the corpus supports it, without a rewrite.
- **Positive:** prevents the false claim "motion matching is in" while a blendspace plays.
- **Negative:** one interface and two implementations to maintain; the interface must not leak provider-specific assumptions (it exposes locomotion parameters, not animation internals).

## Verification
Phase 1 exit: locomotion targets met under **both** providers on available clips; debug HUD reports the active provider correctly.
