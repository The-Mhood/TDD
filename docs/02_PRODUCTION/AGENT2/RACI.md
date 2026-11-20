# RACI — responsibilities, approvals and review gates

**Document:** TDD-PROD-003 · Version 1.0 · 2026-11-16

R = Responsible (does the work) · A = Accountable (owns the outcome, one only) · C = Consulted ·
I = Informed. **Noah**

## Roles

| Code | Role |
|---|---|
| **CD** | Creative Director / user — final authority on creative direction, story, visual identity, priorities |
| **TD** | Technical Director (ChatGPT) — architecture, specs, sequencing, review of reports, integration risk |
| **A1** | Agent 1 — Gameplay, Character and Combat Engineering |
| **A2** | Agent 2 — World, Systems, Environment and Gameplay Simulation |
| **A3** | Agent 3 — Integration, Technical Quality, Build and Performance |
| **VIS** | Visual production team (Art Bible authors) |
| **CUL** | Igbo cultural consultant (**not yet appointed — blocks several gates**) |

## Decisions

| Decision type | R | A | C | I |
|---|---|---|---|---|
| Story canon, narrative facts, character identity | CD | **CD** | CUL, VIS, TD | all |
| Visual design approval | VIS | **CD** | CUL | A1, A2 |
| **Canon approval of a location/character** (distinct from design) | CD | **CD** | CUL, VIS | all |
| Cultural review | CUL | **CD** | — | all |
| Technical architecture, ADRs | TD, A3 | **TD** | A1, A2 | CD |
| Engine version changes | A3 | **TD** | A1, A2 | CD |
| Interface changes | owner agent | **TD** | all consumers | all |
| New plugins/dependencies | requesting agent | **TD** | A3 | CD |
| Milestone acceptance / stage gate | A3 | **TD** | A1, A2 | CD |
| Schedule and scope | CD, TD | **CD** | A1, A2, A3 | — |
| Build and packaging | A3 | **A3** | TD | all |
| Performance acceptance | A3 | **TD** | A1, A2 | CD |
| Bug triage severity | A3 | **TD** | A1, A2 | CD |
| Asset storage policy (D-01) | A3 proposes | **CD** | TD | all |

## Systems

| System | R | A | C |
|---|---|---|---|
| Core framework, ID types, gameplay tags | A3 | **A3** | A1, A2 |
| Movement, camera, input | A1 | **A1** | A2, TD |
| Combat abilities, damage, hit arbitration | A1 | **A1** | A2, A3, TD |
| Animation bridge, IK | A1 | **A1** | VIS |
| Weapon definition + handling | A1 | **A1** | VIS (identity locks) |
| Enemy AI, perception | A2 | **A2** | A1, TD |
| Boss phase graphs | A2 | **A2** | A1, A3, CD (phase lists) |
| Chapters, streaming, world composition | A2 | **A2** | A3, TD |
| Interactables, memory director | A2 | **A2** | A3, TD, CD (fragments) |
| NPC/crowd simulation | A2 | **A2** | VIS, A3 |
| Audio, music director | A2 | **A2** | A1, A3 |
| Progression, campaign graph | A3 | **A3** | TD, CD |
| Save/load, settings | A3 | **A3** | A1, A2, TD |
| UI/HUD/menus/codex | A3 | **A3** | CD, A1 |
| Telemetry, CI, build, perf | A3 | **A3** | TD |
| Canon validators | A3 | **A3** | A2 (rules input), CD (canon) |

## Escalation

1. **Technical dispute** between agents → TD decides, ADR recorded.
2. **Creative dispute** → CD decides.
3. **Canon vs. engineering conflict** → CD decides; engineering records the decision in the mirror.
4. **Schedule vs. quality conflict** → TD recommends, CD decides; any accepted quality risk is recorded as a
   waiver with an expiry condition.
5. **Cultural sensitivity question** → CUL review; if no consultant is appointed, the asset **cannot** be
   marked Shippable. This is a hard stop, not a preference.

## Reporting contract

Every agent report contains, per item:

```
Item:            <name>
Status:          ESTABLISHED | PARTIAL | SPEC | STUB | EXPERIMENTAL | MOCKED | BLOCKED | UNAVAILABLE
Authored:        yes/no
Compiled:        yes/no/untested
Executed:        yes/no
Verified:        yes/no — evidence path
Known gaps:      <explicit>
Interface impact: <none | changed: list>
```

A report without an evidence path for an ESTABLISHED claim is rejected.
