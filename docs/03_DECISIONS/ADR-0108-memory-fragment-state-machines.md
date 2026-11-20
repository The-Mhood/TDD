# ADR-0008 — Memories as staged fragment state machines, audio-first

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 2 (World, Systems) / Agent 3 (Progression, persistence)
- **Affects:** Agent 1 (interaction animation), Agent 2 (audio), Agent 3 (save, UI)

## Context

The seven hidden memories are the spine of the game's ending structure and its most canonically constrained
mechanic. `OPEN_ART_DECISIONS` OAD-32 is explicit and APPROVED IN PRINCIPLE:

- one hidden memory in each of Chapters 1–7;
- each reveals something different;
- **found only by exploration**;
- a distinct visual identity each;
- a coherent sequence;
- **missing one closes Ending 3 only**;
- the last changes the meaning of the confrontation;
- **"met as fragments (place, object, sound, interaction, memory), not as collectible cutscenes."**

The memories document adds: a memory is found where a place echoes it, and **did not necessarily happen
there**.

The cheap implementation — a glowing collectible that plays a cutscene — is explicitly **forbidden by canon**.
So is treating the memory as an item in an inventory.

## Decision

Implement memories as an explicit, per-memory **six-stage state machine** owned by a single director.

```
Stage 0 UNDISCOVERED   no world presence
Stage 1 PLACE          player inside the discovery location; ambience shifts (subtle, non-UI)
Stage 2 OBJECT         the canon object is findable and readable (no quest marker by default)
Stage 3 SOUND          the canon sound cue plays (audio-first, spatially placed)
Stage 4 INTERACTION    the canon verb is performed (retie / drink / set bowl / work free / touch / replace / unfold)
Stage 5 PLAYBACK       Sequencer scene in a separate memory sublevel; memory granted on completion
Stage 6 COMMITTED      ledger written with content hash; Ending-3 eligibility recomputed
```

Rules, each backed by an automated test:

| # | Rule | Why |
|---|---|---|
| M1 | Stages advance strictly in order; no skipping | Canon: it is a sequence of fragments, not a trigger volume |
| M2 | Each stage has an explicit `CanAdvance` predicate | Prevent accidental auto-advance on spawn overlap |
| M3 | A memory cannot be granted twice | Save integrity; re-entry yields a short "echo" only |
| M4 | Playback sublevel is distinct from the discovery location | Canon: the memory did not necessarily happen there |
| M5 | Grant records `(Index, Chapter, SceneId, LocationId, ContentHash)` | A changed memory definition invalidates stale completion instead of silently granting Ending 3 |
| M6 | Ending 3 eligibility = all seven COMMITTED **and** content hashes current | OAD-32: missing one closes Ending 3 only |
| M7 | Campaign reports *which* memories are missing | Canon-consistent UX; never a generic "you missed something" |
| M8 | Memory 6 camera is locked to child eye height; no violence depicted | Canon: memories doc visual identity |
| M9 | Memory grant writes audio state before UI state | The experience is audio-led; UI must never lead the moment |
| M10 | No memory may be gated behind another memory's discovery | Canon requires all seven, not an order. Order-gating would be an invented rule (pending CD decision D-04) |

Data shape — the seven memories are one `DT_MemoryFragments` DataTable generated from
`Tools/canon/data/canon_index.json`, so the published table and the game cannot diverge.

## Consequences

**Positive**
- Canon compliance is structural, not a matter of art discipline.
- Fully testable headless: the state machine, ordering, hash invalidation and ending predicate are pure logic.
- Discovery is genuinely exploratory: no map marker, no inventory row, no "collect 3/7" HUD by default.
- The audio-first rule (M9) makes the memories land as experiences rather than menu events.

**Negative / risks**
- Players may not realise exploration is rewarded. Mitigation: environmental legibility, an optional
  "echo sense" accessibility aid to be designed and approved (does not reveal location outright).
- Six-stage state machines are more authoring work per memory than a pickup. That is the canon cost, accepted.
- Content-hash invalidation means editing a memory invalidates existing test saves. Correct, but QA must know.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Collectible item + cutscene | Explicitly forbidden by OAD-32 |
| Trigger volume plays sequencer scene | Skips the fragment sequence; makes discovery accidental rather than exploratory |
| Inventory/codex-based memory collection | Turns narrative inheritance into a checklist; conflicts with the game's thematic core |
| All memories at chapter end, in order | Removes exploration; contradicts "found only by exploration" |
