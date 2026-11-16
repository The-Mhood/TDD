# THE DISOBEDIENT DAUGHTER
### *Nwanyi Na-anụghị Ihe*

A third-person action-adventure game of dark African mythological fantasy, built in Unreal Engine 5.

---

## Repository status

This repository is the **engineering** home of the project. It currently contains the technical foundation
and the architecture, not a playable build. Read `Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md` before
touching anything: it states what exists, what does not, and why.

**Honest current state (2026-11-16):**

| Area | State |
|---|---|
| Canon index + validators (L0) | **ESTABLISHED** — 58 automated tests passing |
| Architecture, ADRs, stage gates, RACI | **ESTABLISHED** — documents ratified pending Technical Director review |
| Unreal project (`.uproject`, modules, build) | **SPEC** — no engine available in the current environment |
| All gameplay systems | **SPEC** — designed, not implemented |
| Creative canon (characters, environments, story, memories) | **ESTABLISHED externally** in the Google Drive Production Art Bible |

There is **no playable build**. Any claim otherwise would be false.

## The creative canon lives in Google Drive, not here

The Production Art Bible is the authority for characters, environments, story and visual decisions.
This repository mirrors only what engineering needs to enforce canon in code:
`Tools/canon/data/canon_index.json`, documented in `Docs/CANON_INDEX.md`.

The Drive registers are authoritative. If this repository disagrees with them, **this repository is wrong.**

## Quick start (tooling, no engine required)

```bash
# Validate canon data — the only gate that runs in this environment
python3 -m unittest discover -s Tools/canon/tests -v
```

Expected: `OK`, 58 tests. This writes `Docs/evidence/stage0/L0_canon_index_validation.json`.

## Repository map

```
Docs/
  00_MASTER_ENGINEERING_ARCHITECTURE.md   the binding architecture document
  CANON_INDEX.md                          how canon is mirrored and validated
  adr/                                    architecture decision records
  production/STAGE_GATES.md               what "done" means at each stage
  production/RACI.md                      who owns and who approves what
  evidence/                               test output and verification records
Source/
  TDDRuntime/                             game module (character, combat, world, progression)
  TDDEditor/                              editor-only validators and tools
  TDDTests/                               automation tests
Tools/
  canon/                                  canon index, schema, validators, tests
Content/                                  content root (see ADR-0004 before adding anything)
```

## Non-negotiable rules for everyone working here

1. **No canon invention.** Story facts, character identity and visual decisions belong to the Creative
   Director. Engineering implements; it does not decide.
2. **Design approval is not canon approval.** Three separate axes: design, canon, shippable
   (`Docs/CANON_INDEX.md`).
3. **Evidence or silence.** A system is not "working" until a named test passes on an engine machine and the
   result is filed in `Docs/evidence/`.
4. **Text only in Git.** No `.uasset`, `.umap`, audio or video in this repository (ADR-0004).
5. **One owner per system.** See `Docs/production/RACI.md`. Do not build a second version of someone
   else's system.
6. **Invented mythology is labelled as fiction.** Never present the game's invented beliefs as authentic
   Igbo tradition.

## Engine

Unreal Engine **5.8** — the last planned UE5 major release. See `Docs/adr/ADR-0002-engine-baseline-ue58.md`.
