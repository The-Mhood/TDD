# TDD — Production Campaign Reconciliation (A–E ↔ W1–W4)

**Document ID:** TDD-IMPL-CAMPAIGN-001 · **Version:** 1.0 · **Date:** 2026-11-22
**Author:** PM. **Branch:** `arena/553fb02d-tdd`.
**Purpose:** reconcile the owner's **campaign A–E** production framing to the four
**W1–W4 workstreams**, with **explicit dependencies, owners and acceptance gates** for
each. **GitHub (`arena/553fb02d-tdd`) remains the single source of truth**; no status is
upgraded without actual evidence.

**Status vocabulary:** `PREPARED` (authored, not yet run) · `IN PROGRESS` ·
`BLOCKED` (waiting on a named dependency) · `QUALIFICATION PENDING` (artifact produced,
gate not yet passed) · `VERIFIED` (evidence on the owner platform) · `CLEARED` (acceptance
gate passed with evidence).

---

## 1. Campaign ↔ Workstream map

| Campaign | Workstream | Title | Current status (2026-11-22) |
|---|---|---|---|
| **A** | **W1** | UE 5.8 Phase-1 Ọmà-valley core build + runtime | **BUILD CLEARED (B1)**; runtime/PIE open (B2/B3) |
| **B** | **W2** | **Adanna V5 / Guard V3** character production package | **PREPARED / QUALIFICATION PENDING** — BMesh v2.4 fixes on source of truth; real Blender run + likeness review pending; **blocked on real portrait** |
| **C** | **W2 → W3** | **Unreal integration** (Adanna/Guard import, BP wiring, skeleton/bone mapping, animation integration) | **PREPARED** — import scripts hash-verified; Mac import/wiring steps pending; depends on **Campaign B** qualification + V3 baseline |
| **D** | **W3 → W4** | World/content: CH01 greybox map, environment kit, physical VFX | **PREPARED** — greybox builder validated agent-side; Mac map authoring pending |
| **E** | **W3 / W4** | Story / Research / Cultural Review reconciliation (Explorer's Report) | **RECONCILED, PENDING HUMAN APPROVAL** — Research/Story/Cultural Review sign-off outstanding |

> **Campaign A is the only one with an engine-verified gate so far (B1).** Campaigns B–E
> remain at the prepared/qualification-pending/approval-pending tiers; none is upgraded
> without owner-platform or human evidence.

---

## 2. Campaign A — W1 UE Phase-1 Ọmà-valley core

- **Status:** **BUILD CLEARED (B1).** Owner-Mac UE 5.8 Mac ARM64 Development build of
  commit `995caf9` exited 0 (2026-11-22); executable `Binaries/Mac/TDD_GAME` produced.
- **Dependencies:** none outstanding for the build gate (all C++/UHT defects resolved).
- **Owner:** Engineering (agent, C++ fixes — done); Owner (Mac, build — done; PIE — next).
- **Acceptance gates:**
  - **B1 — Owner-machine UE 5.8 compilation: CLEARED** ✅ (`995caf9`, exit 0).
  - **B2 — Runtime/PIE verification: OPEN** — pending the PIE session per
    `PHASE1_PIE_ACCEPTANCE_CHECKLIST.md` (§4e Output Log checks + recording).
  - **B3 — Launch-map setup: OPEN** — pending `OMEGA_VALLEY_PHASE1.umap` + game mode +
    Player Start + PIE.
- **Next owner action:** the four documented editor actions (create map, assign
  `TDDOmegaValleyGameMode`, place Player Start, PIE) + capture the §4e logs/recording.

## 3. Campaign B — Adanna V5 / Guard V3 (W2) — **explicit dependencies / owners / gates**

- **Status:** **PREPARED / QUALIFICATION PENDING.** The BMesh/API **v2.4 fixes are on the
  GitHub source of truth** (`pipeline/facial_poc/`, committed on `arena/553fb02d-tdd`;
  `build_adanna_facial_poc.py` uses `bmesh.ops.subdivide_edges` + `bm.to_mesh(...)`,
  `pipeline_version` `v2.4`). The pipeline is agent-side-tested (stub suite ALL PASS); a
  **real Blender 4.2.23 run has not executed**.
- **Dependencies:**
  1. **Real approved Adanna portrait** — the committed reference
     `pipeline/facial_poc/reference/REF_ADANNA_MASTER_PORTRAIT_APPROVED_V001.jpg` is a
     **19-byte stub (`fakejpg`)**, **NOT** the approved portrait. **BLOCKER for the
     likeness review** — owner must supply the real portrait before any likeness verdict.
  2. **Blender 4.2.23 on the Mac** (absent in the agent sandbox; owner-only).
  3. **Design's M2 sculpt/character roadmap work** (proceeds where dependencies permit).
- **Owner:** Character Art + Technical Art (agent — pipeline); Owner (Mac — Blender run +
  visual likeness review).
- **Acceptance gates:**
  - `run_facial_poc.sh` **exit 0** on the Mac (Blender 4.2.23).
  - Valid **`ADANNA_FACIAL_POC_V2.blend` + `.fbx`** produced.
  - **Four previews + a turntable** rendered.
  - **`QC_RESULT.json` QUALIFIED (10/10).**
  - **Separate visual likeness review** vs the **real** approved portrait (not the stub).
  - Checksums + `EVIDENCE_BUNDLE_*.txt` recorded.
- **Integration rule (binding):** V3/V2 remain the active integration baseline and V2/V1
  remain rollback fallbacks **until V5/V3 passes its qualification gate**. Do not silently
  replace approved identity or design constraints.
- **Exact owner-side Blender execution command:**
  ```bash
  cd ~/TDD/pipeline/facial_poc && bash run_facial_poc.sh
  ```
  (set `PORTRAIT_PATH` to the real approved portrait; `BLENDER_BIN` defaults to `blender`).
  **Do not run Blender against an outdated pipeline — confirm the v2.4 sources are
  checked out first** (they are, on `arena/553fb02d-tdd`).

## 4. Campaign C — Unreal integration (W2 → W3) — **explicit dependencies / owners / gates**

- **Status:** **PREPARED.** The V3 import script is hash-verified
  (`import_adanna_production_v3.py`, Adanna V3 FBX `40f1c83d…`); V2/V1 rollback intact.
  Mac-side import/wiring steps are prepared but **not executed**.
- **Dependencies:**
  1. **Campaign B qualification** — the Adanna V5 / Guard V3 package must pass its gate
     before it replaces the integration baseline (V3/V2 remain baseline meanwhile).
  2. **Campaign A build environment** — the UE 5.8 project builds (B1 CLEARED at `995caf9`),
     so integration can be compiled/verified on the Mac.
  3. **Mac-side import + wiring** — run the import script, wire `BP_Adanna_ProductionV3`,
     verify skeleton/bone mapping against the movement clips (V1, 46/46 source PASS).
  4. **Guard V3 / Guard animation integration** (5 states, 36/36 source PASS) — pending.
- **Owner:** Technical Art / Integration (agent — scripts, wiring); Owner (Mac — import
  run, in-engine verification).
- **Acceptance gates:**
  - Import script runs on the Mac; `BP_Adanna_ProductionV3` wired; skeleton/bone mapping
    verified against movement clips.
  - Movement clips V1 (6 clips) integrated; Guard clips (5 states) integrated.
  - In-engine animation integration verified (owner-Mac, with evidence).
  - V5/V3 integration only after Campaign B qualification passes.
- **Next owner action:** after Campaign B is qualified (or on the V3 baseline), run the
  import script on the Mac and complete the `BP_Adanna_ProductionV3` wiring + bone-mapping
  verification.

## 5. Campaign D — World / content (W3 → W4)

- **Status:** **PREPARED.** `build_chapter1_greybox.py` + `world.json` validated agent-side
  (7 waypoints, 46 obstacles, spawn in bounds); `import_ch01_compound_v2.py` prepared.
  Environment Kit V2 modular OBJs and physical VFX sprites imported/qualified agent-side.
- **Dependencies:** Campaign A build environment; Mac-side map authoring.
- **Owner:** World/Environment (agent — pipeline); Owner (Mac — map build).
- **Acceptance gates:** greybox map built at `/Game/Maps/Ch01_Greybox`; functional
  movement automation (`TDD-Functional.Movement.*`, AC-04…AC-13) requires the Mac-authored
  test map zones (`L_TDD_Test_Movement`: Z_Flat, Z_Dodge, Z_Steps, Z_Corridor1/2).
- **Next owner action:** run the greybox builder on the Mac → `/Game/Maps/Ch01_Greybox`.

## 6. Campaign E — Story / Research / Cultural Review (W3 / W4)

- **Status:** **RECONCILED, PENDING HUMAN APPROVAL.** The Explorer's Report is reconciled
  against the authoritative regional atlas; §16 distance corrected. Approval of the `[A]`
  market-day assignments and §15 (shrine-groves) is outstanding.
- **Dependencies:** human Research (market-day evidence), Story (narrative fit), Cultural
  Review (sacred-places restraint), Owner/CD (approval).
- **Owner:** PM (reconciliation); Research / Story / Cultural Review (human sign-off).
- **Acceptance gates:** recorded Research/Story/Cultural Review sign-off;
  `WORLD_SOURCE_AND_EVIDENCE_REGISTER.md` updated (`[A]`→approved); report version bumped.
- **Next action:** route to Research → Story → Cultural Review per the review doc §6.

---

## 7. Critical-path / dependency summary

- **Campaign A (build) is CLEARED** — it unblocks Campaign C's in-engine verification.
- **Campaign B is the near-term critical path** for character identity: it is **blocked
  on the real portrait**, then requires the Blender run + QC 10/10 + likeness review.
- **Campaign C depends on B** (V5/V3 qualification) and on A (build); it cannot integrate
  V5/V3 before B passes, and must hold the V3/V2 baseline meanwhile.
- **Campaign D** can proceed on the Mac greybox build in parallel with B/C.
- **Campaign E** is human-gated and runs in parallel; it does not block B/C/D engineering
  but gates canon claims.

**Rule:** no campaign is marked VERIFIED/CLEARED without owner-platform or recorded
human evidence. GitHub is the single source of truth.
