# ADR-0006 — Canonical ID scheme adopted from the Drive registers

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 3 (Integration / Technical Quality)
- **Affects:** all agents

## Context

The Drive registers already use stable identifiers:

```
CHxx-SCN-yyy    scene
CHxx-SUB-yyy    sublocation / microlocation
CHxx-INT-yyy    interior
```

Real examples in use today: `CH01-SCN-046`, `CH01-SUB-018`, `CH03-INT-001`, `CH08-SUB-007`, `CH08-INT-003`.

These IDs are referenced by the seven-memory table, by approval decisions (OAD-45, OAD-36), and by the
location and scene master registers (534 KB and 278 KB documents respectively).

If engineering invents its own scheme — names like `L_ForbiddenForest_Start`, `Q_Memory1`, GUIDs — then:

- the save file cannot be reconciled with the art registers,
- a location rename in the Art Bible silently breaks quests,
- evidence and reports cannot be cross-referenced with design documents,
- memory verification against the published table becomes manual and unreliable.

## Decision

1. **Adopt the register scheme verbatim.** It is the primary key of the content pipeline.
2. **Extend it minimally** where the registers have no scheme, using a suffix convention that cannot collide:
   - `CHxx-BOSS-<PascalCaseName>` — boss encounters (e.g. `CH01-BOSS-GreatRootMother`).
   - `-P` suffix — engineering-proposed, not yet in a register (e.g. `CH03-SUB-021-P`).
3. **Maintain a mirror index** at `Tools/canon/data/canon_index.json`, validated by
   `Tools/canon/tests/test_canon.py`. The mirror is *derived*; the registers are authority.
4. **Drift is a build failure, not a warning.** If the mirror disagrees with the registers, the L0 gate fails
   and the mismatch is raised to the register owner. Engineering never silently "corrects" canon.
5. **Everything keys on IDs:** levels, data assets, save records, telemetry events, evidence filenames,
   sequencer assets, audio metasounds, and bug reports.
6. **Never key on display names.** Display names are localised and change. `"The Clear Water"` is a label;
   `CH02-SUB-003` is identity.

## Consequences

**Positive**
- Save data, quests, art review and telemetry share one vocabulary.
- The published seven-memory table is machine-verifiable (see `test_memory_scene_and_location_ids_match_published_table`).
- Register drift is caught in seconds, by CI, instead of at chapter integration.

**Negative / risks**
- The mirror duplicates data. Mitigation: it is small, schema-validated, and contains only what engineering
  needs (ids, status, memory fragments, chapter rules) — not the full registers.
- Register updates require a mirror update in the same change window. Mitigation: the gate tells you exactly
  what to add; this takes minutes.
- Registers use identifiers that engineering cannot mint. If the Drive registers stall, content can be
  *blocked*. Mitigation: `-P` suffix for engineering proposals lets work proceed on non-canon plumbing without
  pretending it is canon.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Engineering-native naming (GUIDs / level names) | Cannot be reconciled with the Art Bible; breaks evidence and save integrity |
| Parse the Drive markdown at build time | Registers are large, evolving prose documents; parsing is brittle. Mirror + validation is sturdier |
| Wait for a formal CMS | Content production cannot wait; the mirror is small and the schema is enforceable today |
