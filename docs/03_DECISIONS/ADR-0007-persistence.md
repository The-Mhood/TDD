# ADR-0007 — Custom versioned save subsystem with module providers

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 3

## Context
Save data must survive years of schema change across eight chapters, memory discoveries, world state, endings and settings. `USaveGame` alone is a serialisation format, not a persistence architecture: no versioning discipline, no atomicity, no migration, no corruption handling. Third-party plugins add dependency risk and opaque formats.

## Decision
Build `UTDDPersistenceSubsystem` on `USaveGame` with: explicit `FTDDSaveHeader` (schema version, build, timestamp, checksum), per-module sections contributed through `ITDDSaveProvider`, a migration chain, atomic write (tmp → verify → rotate to `.sav`, keep `.bak`), checksum validation, and captured-blob migration tests. Slots: Auto (2-deep), Checkpoint (1), Manual (3). Memory discovery writes immediately as a documented exception.

## Consequences
- **Positive:** versioned, testable, debuggable saves; corrupt saves cannot silently destroy progress.
- **Positive:** modules own their own data without a central god-struct.
- **Negative:** every new persisted field needs a migration decision — deliberate friction.
- **Negative:** more code than `SaveGameToSlot`.

## Verification
`TDD-Unit.Persistence.RoundTrip`, `.Migration`, `.AtomicWriteInterrupt` with real captured blobs; a deliberate corruption test that must fail gracefully.
