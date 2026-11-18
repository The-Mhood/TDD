# THE DISOBEDIENT DAUGHTER — *Nwanyi Na-anụghị Ihe*

Third-person action-adventure, dark African mythological fantasy, Unreal Engine 5.
Original Igbo-inspired folklore retold as original dark fantasy — **not** a depiction of authentic Igbo tradition.

- **Protagonist:** Adanna, 25, warrior, daughter of former warrior-king Ezeani
- **Chapters:** 8, from the Forbidden Forest to the Ancestral Realm
- **Endings:** kill Ezeani, spare Ezeani, and a hidden ending earned through seven concealed memories of Nneka

---

## Current state of this repository (2026-11-18)

**The Unreal project now exists in this repository, and it has never been compiled.** As of `TDD-IMPL-FOUNDATION-001`, the repository contains a real UE 5.8 project at the root — `TDD.uproject`, nine C++ modules (`TDD`, `TDDCore`, `TDDWorld`, `TDDGameplay`, `TDDAI`, `TDDNarrative`, `TDDUI`, `TDDEditor`, `TDDTests`), both target files, `Config/`, an automation-test foundation and two toolchain verifiers — plus the architecture and governance documents.

**Status: `IMPLEMENTED_UNVERIFIED`.** The skeleton is statically checked (`58/58` structural checks) and **no Unreal Engine exists in the workspace**, so the project has not been built, opened, cooked or run, and no acceptance case has been executed. `Tools/engine/preflight.sh` re-measures any machine and currently reports `NOT READY — 4 blocking gap(s)`; the exact engine/machine requirement is in `docs/06_IMPLEMENTATION/UNREAL_PROJECT_FOUNDATION_V1.md` §5. There is still **no game content**. See `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md`.

Verified by inspection: the repository was an empty initialised repo (one 6-byte README, one commit) before this documentation set was added. The production Art Bible lives in Google Drive; it currently holds 176 indexed files, of which **7 are approved designs** and none is a production-ready 3D asset.

The first required deliverable — the Master Engineering Architecture Document — is complete. Implementation starts at Phase 0, which cannot be built in the agent workspace (no Unreal Engine, no compiler, no GPU).

Read `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` before believing any status claim in this project, including your own.

---

## Documents

| Path | What it is |
|---|---|
| `docs/01_ARCHITECTURE/MASTER_ENGINEERING_ARCHITECTURE.md` | **Primary deliverable.** Full architecture: project assessment, module design, all gameplay systems, AI, animation, narrative, persistence, interfaces, testing, performance, phasing, risks |
| `docs/00_GOVERNANCE/PROJECT_STATE_2026-11-16.md` | Evidence-based audit of the repository, the workspace and the Art Bible |
| `docs/00_GOVERNANCE/STATUS_AND_CLAIMS.md` | Status vocabulary + current claim ledger |
| `TDD.uproject`, `Source/`, `Config/`, `Tools/engine/` | **The Unreal project** — UE 5.8 pin, nine modules on the MEAD §3.2 graph, targets, config, automation-test foundation, `preflight.sh` and `verify_project_structure.py` (`IMPLEMENTED_UNVERIFIED`: never compiled) |
| `docs/06_IMPLEMENTATION/UNREAL_PROJECT_FOUNDATION_V1.md` | What was created, what is verified vs unverified, the exact engine/machine blocker and the installation requirement |
| `docs/06_IMPLEMENTATION/C05_DEPENDENCY_OWNERSHIP_MATRIX_V1.md` | Every outstanding C-05 dependency (B-1…B-15) with owner, recorded status, the exact decision required and what it blocks — **no decision invented** |
| `docs/06_IMPLEMENTATION/C05_TRANCHE_1_MAPPING_V1.md` | The 17 first-tranche cases mapped to modules, test kinds, automation names and fixtures; `T-C05-11` deferred pending TD-06; **0 implemented, 0 executed** |
| `docs/00_GOVERNANCE/OPEN_QUESTIONS.md` | 22 decisions needed, what each blocks, and the default assumption while open |
| `docs/01_ARCHITECTURE/CODING_STANDARDS.md` | Mandatory coding, naming, tick, logging, test and commit rules |
| `docs/03_DECISIONS/ADR-0001…0012` | Architecture decision records (engine pin, modules, GAS, animation provider, AI stack, persistence, canon gating, audio, experimental features, single-player, verification boundary) |

## Working rules (short form)

1. **Inspect before replacing.** No agent overwrites another's work; ownership is in MEAD §13.
2. **No claim without evidence.** `IMPLEMENTED_AND_VERIFIED` requires a build log and test output from a machine with Unreal Engine.
3. **Canon is not engineering's to invent.** Story, characters, art and culture come from the Creative Director and the Drive Art Bible. Missing content gets a named placeholder, never an invented fact.
4. **Framework before content.** Mechanisms are content-agnostic; chapters are built through one repeatable pipeline, proven on Chapter 1.
5. **One implementation per system.** Extend, do not fork.

## Environment requirements (for the machine that actually builds this)

- Unreal Engine **5.8** (see ADR-0001), Visual Studio 2022 with C++ game development workload
- Git LFS installed and initialised before the first binary asset is committed
- GPU and 32 GB RAM recommended for editor and cook work

## Source control

- `.gitattributes` enforces Git LFS for binary content. **LFS is not installed in the agent workspace**, so no binaries may be committed from there.
- Engine-ready assets only in this repo; source art, large renders and audio stems stay in Drive/Perforce.

## Branch

Active development branch for this session: `arena/3bc206a0-tdd`.
