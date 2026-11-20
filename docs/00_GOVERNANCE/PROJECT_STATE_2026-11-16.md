# PROJECT STATE — 2026-11-16

**Audit type:** direct inspection of the repository plus read-only inspection of the authoritative Google Drive Art Bible.
**Auditor:** Arena engineering agent.
**Purpose:** establish the real starting condition before any implementation. This document records evidence, not intentions.

---

## 1. Repository inspection (evidence)

```
$ git log --oneline
5e3d1da Initial commit
$ git show --stat HEAD
 README.md | 1 +
 1 file changed, 1 insertion(+)
$ find . -path ./.git -prune -o -type f -print | wc -l
1
$ cat README.md
# TDD
```

**Finding:** the repository contains no game project. No `.uproject`, no `Source/`, no `Config/`, no `Content/`, no assets, no tests, no CI, no engine pin. The only commit is an initialised README.

**Branch:** `arena/3bc206a0-tdd`, based on `main` at `5e3d1da4eee42ad8255760530291ff91cdfb39b2`.

**Implication:** there is no prior engineering work to integrate with or avoid overwriting. There is also no inherited convention, which is why `docs/01_ARCHITECTURE/CODING_STANDARDS.md` exists.

---

## 2. Agent workspace capability inspection

| Check | Command | Result |
|---|---|---|
| Unreal Engine | `which UnrealEditor` | Not present |
| UnrealBuildTool | `which UnrealBuildTool` | Not present |
| .NET SDK | `which dotnet` | Not present |
| MSVC / Clang | `which clang++` | Not present |
| System compiler | `which g++` | `/usr/bin/g++` (cannot build UE targets) |
| Python | `which python3` | Present (tooling only) |
| Git LFS | `git lfs version` | Not installed |
| CPU / RAM / disk | `nproc`, `free -g`, `df -h` | 2 vCPU / 3 GB RAM / 20 GB free |
| GPU | — | None |
| Google Drive connector | `list_connector_tools` | Enabled and readable |
| GitHub / Git | — | Configured |

**Finding:** this workspace **cannot build, cook, run, render or profile an Unreal Engine project.**

**Consequence (ADR-0012):** all agent-authored code is `IMPLEMENTED_UNVERIFIED` until built on the production workstation. No agent may claim `IMPLEMENTED_AND_VERIFIED` without attaching a build log, automation report and — for performance claims — a frame-time capture produced outside this workspace.

---

## 3. Authoritative content inspection (Google Drive)

Source of truth: `THE DISOBEDIENT DAUGHTER — PRODUCTION ART BIBLE` folder `1lzJBgHHSO2OJMB0LFmwQoU6R7Kv2iGlZ`, indexed by `ART_BIBLE_MASTER_INDEX_POST_SYNC_2026-11-16.md` (`1r5TKhV74Q3hATrSwwm9r-zP4HxRIwF4f`).

| Measure | Value | Note |
|---|---|---|
| Indexed files | 176 | concept boards, registers, documentation, reference archives |
| **Approved designs** | **7** | 2 character references + 5 Chapter 8 environment boards |
| Approved 3D/production assets | **0** | all approved items are concept boards/renders |
| Rejected designs | Kept in `16_REJECTED_DESIGNS` | preserved, not deleted |
| Exploratory designs | Kept in `15_EXPLORATORY_DESIGNS` | explicitly not canon |
| Decision register | `DECISIONS.md`, `OPEN_ART_DECISIONS.md` | OAD-01 … OAD-55 |
| Cultural guide | `CULTURAL_REFERENCE_GUIDE.md` | status: **needs consultant review** |

### 3.1 Approved designs (complete list)

| Asset | Decision |
|---|---|
| `CHAR_ADANNA_MASTER_REFERENCE_V001` | OAD-02 |
| `CHAR_AMADIOHA_MASTER_REFERENCE_V001` | OAD-16 |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_SEALED_QUARTER_V003` | OAD-45 |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_NNEKAS_HOUSE_V004` | OAD-45 |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_NNEKAS_HOUSE_INTERIOR_V003` | OAD-45 |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_HALL_OF_POSTS_V004` | OAD-45 |
| `ENV_LAST_DAUGHTER_ANCESTRAL_REALM_MOTHERS_COURTYARD_SAME_COURTYARD_V007` | OAD-53 |

All seven are **visual development references**, at 1376×768 source resolution (OAD-08). None is a production-ready asset: no mesh, rig, texture set, animation or shader exists for any of them.

Each approved design also has a duplicate copy filed in `14_APPROVED_DESIGNS` (the index lists both the location-folder issue and its approved-designs copy). Do not double-count those copies as additional approvals.

### 3.2 Canon status caveat

Per OAD-48/OAD-53, environment **design** approval is not narrative-**canon** approval: all five approved Chapter 8 environments still carry canon status `PENDING APPROVAL`. Engineering may use them for blockout scale and mood only.

### 3.3 Open items with engineering impact

| ID | Item | Blocks |
|---|---|---|
| OAD-03 | Ezeani's regalia (consultant) | Ezeani content |
| OAD-04 | Okwu and raffia/masquerade imagery (consultant) | Okwu content |
| OAD-06 | Uli-style linework — do not reproduce named uli motifs | Adanna material work |
| OAD-07 | Gold level; aged bronze standard | Final material pass |
| OAD-13 | Nneka's hair | Nneka content |
| OAD-23 | Content of the three ending sequences | Ending cinematics (not the resolver) |
| OAD-32 (content) | Content/implementation of the seven memories | Memory content (not the framework) |
| OAD-34 (detail) | Detailed memory sequence, events, dialogue | Memory content |
| OAD-55 | Villager clothing standard (proposed) | NPC crowd content |

---

## 4. What exists / needs modification / must be built / undecided

| Class | Items |
|---|---|
| **Exists** | Git repo + branch; Art Bible and decision registers in Drive; this document set |
| **Needs modification** | `README.md` (replaced); no code exists to modify or preserve |
| **Must be built** | Project skeleton, 9 modules, all systems in Sections 4–12 of TDD-MEAD-001, tests, CI, packaging; all game content (content is production-owned, not engineering-owned) |
| **Undecided** | Engine pin (recommend 5.8); platforms (recommend PC only); reference hardware; GAS (recommend adopt); audio middleware (recommend none); progression model; save policy; accessibility baseline as requirement; localisation languages; QTE policy |

Full decision list: `docs/00_GOVERNANCE/OPEN_QUESTIONS.md`.

---

## 5. Honest status of this audit

- **Verified:** repository contents, commit history, workspace tooling, Drive Art Bible index and decision registers, UE 5.8 release status (public sources).
- **Not verified:** anything about how the game will perform, because no project exists. All performance figures in TDD-MEAD-001 are **targets**, not measurements.
- **Not attempted:** generating any art asset, mesh, animation or audio. That is outside engineering authority and would be false progress.
