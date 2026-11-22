# ADR-0009 — MetaSounds and Quartz only; no audio middleware

- **Status:** Proposed (reversible)
- **Date:** 2026-11-16
- **Owning agent:** 2 (audio runtime), 3 (build)

## Context
No audio design or audio director exists yet. Wwise/FMOD give strong tooling but cost licence fees, add a plugin dependency, require per-platform integration and are hard to remove once assets are authored inside them.

## Decision
Use engine audio: MetaSounds, Sound Concurrency, submix hierarchy, Quartz for rhythmic events. Wrap playback behind `ITDDAudioService` so a later middleware decision does not reach into gameplay code.

## Consequences
- **Positive:** no licensing, no integration risk now, full control of procedural combat audio.
- **Positive:** interface keeps the door open.
- **Negative:** less mature sound-design tooling than Wwise; if the audio director requires Wwise later, existing MetaSounds must be re-authored (assets, not code).
- **Negative:** complex interactive music needs more hand-authoring.

## Reversal condition
An approved audio direction that requires middleware features unavailable in MetaSounds. Then: ADR + re-author cost estimate before any asset work.
