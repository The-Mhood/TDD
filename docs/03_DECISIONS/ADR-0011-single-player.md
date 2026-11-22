# ADR-0011 — Single-player only; no replication work

- **Status:** Proposed (requires CD confirmation)
- **Date:** 2026-11-16
- **Owning agent:** 3

## Context
The game as specified is a narrative single-player action-adventure. Networking is a large hidden cost: authority, prediction, replication, anti-cheat implications and save/session ownership.

## Decision
No networking. No `Replicated` properties, no `Server`/`Client` RPCs, no `TDDServer` target unless co-op is approved. Gameplay code avoids patterns that make future co-op impossible (e.g. no global mutable singletons for per-player state), but pays no replication cost now.

## Consequences
- **Positive:** roughly no networking schedule; simpler debugging; save format unaffected.
- **Negative:** adding co-op later would be a major architectural change, not a switch.

## Reversal condition
Creative Director approves a multiplayer mode; then this ADR is superseded and a networking architecture ADR is written before any implementation.
