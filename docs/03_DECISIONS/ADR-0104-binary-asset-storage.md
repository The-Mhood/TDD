# ADR-0004 — Binary asset storage: Git holds text only

- **Status:** **PROPOSED — BLOCKED** on Creative Director / infrastructure decision (architecture doc D-01)
- **Date:** 2026-11-16
- **Owner:** Agent 3 (Integration / Technical Quality)
- **Affects:** all agents; blocks all content production from Stage 6

## Context

The repository `The-Mhood/TDD` is a GitHub repository with **no Git LFS configured** and currently 116 KB of
history. The game will require:

| Asset class | Realistic volume | Mergeable? |
|---|---|---|
| `.uasset` / `.umap` (Blueprints, levels, data assets) | tens of thousands of files, GBs | No |
| MetaHuman / skeletal meshes / textures | GBs | No |
| Audio (WAV sources, MetaSounds are assets) | GBs | No |
| Video (cinematics, references) | GBs | No |
| USD / DCC sources | GBs | No |

Git stores binary blobs whole on every revision. An eight-chapter game in plain Git becomes unclonable,
and GitHub will reject or throttle very large pushes. The failure is not theoretical; it is the standard
outcome for game projects that start in Git without a plan and notice too late.

At the same time, the directorate's workflow uses Google Drive for the Art Bible, and agents consume that
image reference from Drive rather than from the repo.

## Decision (proposed)

1. **Git holds text only:** source code, config (`.ini`), `.uproject`, `.Build.cs`/`.Target.cs`, docs, tools,
   tests, and small data (`.json`, `.csv`, `.md`).
2. **Binary game content does not enter this repository's Git history.** It lives in exactly one of:
   - **Git LFS** for small/medium binaries (UI icons, small data assets) **if** LFS is provisioned on the
     remote, or
   - an **external content store** (Perforce, Epic DVCS, or a signed-off Drive/Dropbox mirror) for hero content.
3. **Definitions, not binaries, while the store is undecided.** Engineering authors content *definitions* as
   CSV/JSON under `Content/SourceData/` (e.g. boss phase graphs, combat tuning, memory fragment tables).
   These are diffable, reviewable, and import into Unreal assets. This lets Stage 1–5 proceed with zero
   binaries and gives the project a real source of truth for tuning data.
4. **Hard size rule:** no file over **5 MB** is committed to plain Git. Exceptions require an ADR.
5. `.gitattributes` marks UE binary extensions `-merge -diff` and carries the commented LFS filter lines, so
   enabling LFS is a one-commit change with no history rewrite.

## Consequences

**Positive**
- The repository stays clonable and reviewable by every agent, indefinitely.
- Tuning data becomes code-reviewable and diffable — a genuine production advantage over binary assets.
- Clear ownership: nobody accidentally commits a 4 GB `.umap` at midnight.

**Negative / risks**
- Two-step workflow: a data asset change requires editing CSV → reimport. Slightly slower than in-editor edit.
  Mitigation: an editor utility to export Data Assets back to CSV (Stage 7 tooling task).
- Some Unreal-native features (curve assets, Niagara systems) are binary and cannot be CSV-authored.
  Mitigation: those live in the external store and are referenced by ID from versioned manifests.
- **Until the store is chosen**, heroes, environments and audio cannot be integrated. This is a hard blocker
  and is the single most important decision outstanding.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Commit everything to Git | Repository becomes unusable; violates the directive's production-quality requirement |
| Enable LFS unilaterally | Quota/cost and remote policy are a Creative Director / infra decision, not an engineering one |
| Keep all content in Drive only | No revision integrity for assets, no reproducible builds |
| Wait and decide later | By Stage 6 the damage is done; this must be settled now |
