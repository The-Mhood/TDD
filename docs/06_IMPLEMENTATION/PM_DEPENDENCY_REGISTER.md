# PM Dependency Register

**Document ID:** TDD-IMPL-DEP-001 · **Version:** 1.0 · **Date:** 2026-11-21
**Author:** PM. **Purpose:** Every dependency has an accountable owner, required deliverable, current status, blocking dependency, target completion date, acceptance criteria, and evidence of completion. **Objective: move Design from dependency reporting into controlled production — every blocker assigned, measurable, actively progressing.**

**Field schema (all 7 required per dependency):**
1. Accountable owner · 2. Required deliverable · 3. Current status · 4. Blocking dependency · 5. Target completion date · 6. Acceptance criteria · 7. Evidence of completion

**Status legend:** BLOCKED · IN PROGRESS · READY · AWAITING APPROVAL · DONE · NOT STARTED
**Status tiers (separate these — do not conflate):** *documentation complete* (artifact authored) · *production started* (executable code/pipeline authored) · *technically verified* (run + evidence recorded) · *owner-approved* (owner sign-off recorded). An item is only *owner-approved* when the owner signs off with evidence.

---

## Register

### DP-01 — Zero-budget facial-likeness strategy
1. **Owner:** PM + Design Lead
2. **Deliverable:** `FACIAL_LIKENESS_ZERO_BUDGET_STRATEGY.md` (TDD-IMPL-FACIAL-001)
3. **Status:** **OWNER APPROVED** — *documentation complete; production started (PoC pipeline repaired, see DP-02)*. Approved direction: best practical character quality using free tools, existing hardware, AI assistance and own production effort; zero budget is **not** permission to lower the quality target. **Strategy approval does NOT technically approve the facial PoC implementation** (that is DP-02).
4. **Blocking dependency:** None (approved). DP-02 technical repair was the prerequisite for owner execution.
5. **Target date:** Complete (approved 2026-11-21)
6. **Acceptance criteria:** Owner approved the strategy; quality tier, production approach, tools (free vs paid), hardware limits, and PoC-before-full-production all accepted
7. **Evidence:** Strategy document committed (`53d76de`); owner approval recorded in this directive (2026-11-21)

### DP-02 — Proof of concept: Adanna facial likeness (P0 gate)
1. **Owner:** Character Art + Technical Art (agent); owner reviews/executes on Mac
2. **Deliverable:** Adanna facial sculpt → retopo → PBR texture → facial rig → expression turntable → UE import, from the approved master portrait
3. **Status:** IN PROGRESS — *pipeline REPAIRED (v2.2, BACKGROUND-SAFE) + logic-tested; awaiting owner-Mac execution to produce the actual face*. v2.2 removes every context-dependent Blender operator (the v2.1 `select_all` background-mode failure at `2693a3f`) via data API + BMesh, fixes five owner-flagged defects + two functional bugs + four logic bugs (caught by in-sandbox stub test: primitive `_add` double-append, `update_mesh` missing `bm`, tri-budget overrun from torus defaults, `bm.from_mesh` misuse, non-portable `sha256`). **Logic-tested (stub-bpy end-to-end: build produces all outputs, verifier QUALIFIED, non-zero exit on FAILED) + syntax-verified**; **the actual Blender face has NOT been built** (Blender cannot run in-agent — this is the single genuine owner-Mac step, a clean run not a debugging cycle). **THIS TURN (v2.4, commit `8937332`):** a comprehensive Blender 4.2.23 BMesh/API audit was performed (NOT an isolated traceback fix — see `pipeline/facial_poc/BMESH_API_AUDIT_BLENDER_4_2_23.md`); it corrected the owner-reported `bmesh.ops.subdivide`→`subdivide_edges` defect, **and** a second cascading defect (`bmesh.update_mesh`→`bm.to_mesh`+`me.update()`); the stub was rewritten to mirror the REAL API (invalid calls raise AttributeError). Stub regression tests ALL PASS. **PM owns driving this to a finished, reviewed, qualified face — not closed at pipeline completion.**
4. **Blocking dependency:** owner-Mac execution (the sole Blender/UE authority); DP-01 approval (now satisfied)
5. **Target date:** Owner runs `run_facial_poc.sh` on the Mac (with `PORTRAIT_PATH` set to the approved portrait)
6. **Acceptance criteria:** Owner-Mac build + QC pass (QC_RESULT.json QUALIFIED); owner visual review vs approved portrait PASS; UE import + acceptance tests pass; evidence bundle recorded
7. **Evidence:** `pipeline/facial_poc/output/evidence/` (BUILD_MANIFEST.json, QC_RESULT.json, EVIDENCE_BUNDLE_<ts>.txt) + owner visual-review verdict + UE acceptance bundle; v2 repair committed

### DP-12 — ST05–ST07 environment-state approval
1. **Owner:** Owner / CD
2. **Deliverable:** Definitions + authoritative approval of environment states ST05, ST06, ST07
3. **Status:** **OWNER APPROVED** — *definitions supplied and approved 2026-11-21*. ST05 = Rain (Home Settlement, rainy); ST06 = Market day (crowded village square, ordinary trading/goods); ST07 = Gathering (village square prepared for a community assembly). Ordinary environmental/community scenes; no ritual/shrine/masquerade without an established story requirement + cultural verification.
4. **Blocking dependency:** None (approved). CD-2 remains active for any content that later introduces ritual/shrine/masquerade imagery.
5. **Target date:** Complete (approved 2026-11-21); scene production proceeds
6. **Acceptance criteria:** Owner-supplied definitions + APPROVE recorded; cultural review where required
7. **Evidence:** `ST05_ST07_APPROVAL_RECORD.md` v2 (APPROVED); record committed

### DP-13 — Character naming (Research catalogue + PM allocation)
1. **Owner:** PM (allocation); Research (catalogue); Story (narrative fit); owner/CD (approval)
2. **Deliverable:** `IGBO_NAME_CATALOGUE.md` (Research), `CHARACTER_NAMING_PLAN.md` (PM), `CHARACTER_IDENTITY_RECORDS.md` (integration)
3. **Status:** IN PROGRESS — *catalogue drafted (Research DRAFT, needs specialist verification); PM allocation + identity records drafted; awaiting Story reconciliation + owner approval*. Audit of Drive character folders done (20 named characters: 7 main + 13 supporting, all names retained; NPC population unnamed).
4. **Blocking dependency:** Story narrative-fit review of the 20 retain decisions; Research verification of flagged meanings (Adanna, Ezeani, 9 supporting names); owner/CD approval of the allocation. No Drive asset modified until approved.
5. **Target date:** Story review + owner approval this cycle
6. **Acceptance criteria:** 8 required naming deliverables complete; allocation reconciled with the Nneka–Ezeani–Adanna relationship (unchanged); no cast inflation; Drive assets untouched until approved
7. **Evidence:** Three documents committed; Drive audit evidence (CHARACTER_DESIGN_REGISTER.md + OPEN_ART_DECISIONS.md read via connector)

### DP-14 — Character identity records (integration foundation)
1. **Owner:** PM (with Story, Design, Character Art)
2. **Deliverable:** `CHARACTER_IDENTITY_RECORDS.md` — one consistent record per character (name/aliases, role, relationships, chapters, visual refs, model/animation status, gameplay, dialogue/story dependencies)
3. **Status:** IN PROGRESS — *main cast (7) established; supporting cast (13) in compact form*. Serves as the single consistency anchor tying name, story, visual, model and gameplay together.
4. **Blocking dependency:** None for the records themselves; model/animation status updates as Character Art/Engineering progress each character
5. **Target date:** Main cast complete this cycle; supporting cast refined as their assets are produced
6. **Acceptance criteria:** Every named character has one record; records cross-reference the naming plan, design register and asset status
7. **Evidence:** `CHARACTER_IDENTITY_RECORDS.md` committed

### DP-15 — Research catalogue merge (commit `41252e5`) — **CLOSED**
1. **Owner:** PM (merge); Research (supply)
2. **Deliverable:** Research's Igbo name catalogue incorporated into `arena/553fb02d-tdd` (no-overwrite, preserve PM work)
3. **Status:** **CLOSED (RESOLVED).** Commit `41252e5aada69d390b6342943d0f769a27c624a5` (branch `arena/b2c58152-tdd`, research-agent, 2026-11-21) **verified to exist** (owner-confirmed + PM fetched the branch). **Cherry-picked the single commit** onto canonical `arena/553fb02d-tdd` at `0b30cdf` (the whole Research branch was not merged — branches diverged). `docs/IGBO_NAME_CATALOGUE.md` (341 lines) is now present in the canonical production branch, verified byte-identical to the Research content. PM-authored `docs/06_IMPLEMENTATION/IGBO_NAME_CATALOGUE.md` (`1de0111`) **preserved** — distinct path, distinct purpose.
4. **Blocking dependency:** None — resolved.
5. **Target date:** 2026-11-21 (completed).
6. **Acceptance criteria:** `docs/IGBO_NAME_CATALOGUE.md` present in canonical branch; contents verified; PM catalogue preserved. All met.
7. **Evidence:** commit `0b30cdf` (cherry-pick); `diff` confirming file identical to `41252e5` content; both catalogues present with distinct purposes. **CORRECTION:** the earlier "commit does not exist" finding was incorrect and is withdrawn.

### DP-03 — Enemy taxonomy ratification (CD-3)
1. **Owner:** Owner / Creative Director
2. **Deliverable:** Ratified (or rejected/amended) subset of the 6 proposed enemy archetypes
3. **Status:** BLOCKED (on CD-3 ratification)
4. **Blocking dependency:** **CD-3 ratification** by owner/CD (not ratified as of 2026-11-21); cultural exposure for Thrall/Thunder Aspirant/Maskbearer
5. **Target date:** CD decision (no firm date — CD owns)
6. **Acceptance criteria:** Explicit CD-3 decision on each archetype; surviving archetypes carry a named canon source; none built before the combat+enemy interface exists
7. **Evidence:** CD-3 ratification record (PR/commit note or decision doc)

### DP-04 — Cultural consultant engagement (CD-2)
1. **Owner:** Owner / CD (Q-17 owner)
2. **Deliverable:** Cultural consultant engagement decision + clearance path for shrine/mask/ritual content
3. **Status:** BLOCKED (consultant NOT engaged)
4. **Blocking dependency:** **CD-2 gate** — consultant (Q-17) not engaged; nothing relying on real Igbo practice ships without sign-off
5. **Target date:** CD decision (no firm date)
6. **Acceptance criteria:** Consultant engaged or a documented decision to proceed without; any mask/shrine/ritual content formally cleared
7. **Evidence:** CD-2 clearance record

### DP-05 — Scene briefs (PM/Story)
1. **Owner:** PM + Story
2. **Deliverable:** `ENEMY_TAXONOMY_AND_SCENE_BRIEFS.md` (TDD-IMPL-ENEMYSCENE-001)
3. **Status:** DONE (deliverable written; population reconciliation against the 29-scene register to follow)
4. **Blocking dependency:** None for authoring; enemy-involving scenes remain conditional on DP-03/DP-04
5. **Target date:** Complete this cycle
6. **Acceptance criteria:** Briefs cover narrative + gameplay + location + arch/props/population + cultural refs & restrictions; scene IDs reconciled (no double-counts)
7. **Evidence:** Document committed

### DP-06 — Design qualification package (visual review/acceptance)
1. **Owner:** Design Lead
2. **Deliverable:** `M1_ASSET_QUALIFICATION_PACKAGE.md` (TDD-IMPL-QUALPKG-001)
3. **Status:** DONE (package authored); qualification evidence pending
4. **Blocking dependency:** Qualification evidence requires assets + owner-Mac execution (DP-07)
5. **Target date:** Evidence collected after assets are produced and imported
6. **Acceptance criteria:** Owner-Mac verifies file integrity, scale/orientation, geometry, materials/textures, export compatibility, UE import readiness; qualification status recorded (QUALIFIED/FAILED/NOT QUALIFIED)
7. **Evidence:** Qualification ledger entry with evidence bundle path + owner signature

### DP-07 — Owner-Mac asset verification (integration)
1. **Owner:** Engineering (executes with owner on Mac)
2. **Deliverable:** Import + verification bundle for each qualified asset (file integrity, scale/orientation, geometry, materials, export compat, UE import readiness)
3. **Status:** IN PROGRESS (spec-dependent)
4. **Blocking dependency:** Assets produced + integration spec (DP-08); owner-Mac is the sole UE verification authority
5. **Target date:** After each asset is produced and the spec is in force
6. **Acceptance criteria:** All 6 verification checks pass; import errors = 0; evidence recorded
7. **Evidence:** Owner-Mac verification bundle (checksums, JSON, exit codes, date)

### DP-08 — Integration specification (PM/Technical Direction)
1. **Owner:** PM + Technical Direction
2. **Deliverable:** `M1_ASSET_INTEGRATION_SPECIFICATION.md` (TDD-IMPL-INTSPEC-001)
3. **Status:** DONE
4. **Blocking dependency:** None
5. **Target date:** Complete this cycle
6. **Acceptance criteria:** Spec covers destination folders, asset types, naming, import settings, material requirements, collision/LOD, integration validation + acceptance tests; both technical (Engineering) and visual (Design) acceptance defined
7. **Evidence:** Document committed

### DP-09 — Skeleton / animation retarget (shared pipeline)
1. **Owner:** Technical Art + Engineering
2. **Deliverable:** Shared `HUMAN_BASE_PROPOSED` skeleton + retargeted animation set working for all characters
3. **Status:** IN PROGRESS (Adanna V3 + Guard V2 already share the skeleton; retarget pipeline reused)
4. **Blocking dependency:** None (the pipeline is already proven); per-character animation requires the character asset
5. **Target date:** With each character's import
6. **Acceptance criteria:** Retarget works for all characters on the shared skeleton; no per-character skeleton duplication
7. **Evidence:** Import verification + retarget test result (DP-07 bundle)

### DP-10 — Environment content pipeline (built-content path)
1. **Owner:** Design + Engineering
2. **Deliverable:** Built-content path: Prop Package + Mushroom Cloud, LOD/HLOD, texture-memory discipline
3. **Status:** READY (spec in force)
4. **Blocking dependency:** None for the pipeline definition; environment assets produced per scene briefs
5. **Target date:** With environment production
6. **Acceptance criteria:** Built content imports with LODs; no tri-count/texture-memory blow-up
7. **Evidence:** Environment import verification (DP-07 bundle)

### DP-11 — Reference hardware acquisition (D-12)
1. **Owner:** Owner
2. **Deliverable:** RTX 3060 Ti / 16 GB reference PC (future paid purchase, ~$600–1,200)
3. **Status:** NOT STARTED / FUTURE (not acquired; **zero budget constraint**)
4. **Blocking dependency:** Paid hardware — explicitly NOT assumed in this strategy; facial production does not depend on it
5. **Target date:** TBD by owner; not a gate for facial likeness
6. **Acceptance criteria:** Perf/visual sign-off target available when acquired
7. **Evidence:** Acquisition decision/record when applicable

---

### DP-16 — Phase-1 UE build (Ọmà-valley core) — Mac compile/PIE

1. **Depiction:** Produce a Mac-built, PIE-run Phase-1 build of the `TDD_GAME` Ọmà-valley core (population simulation, market, calendar, weather, NPCs) and verify its acceptance behaviour in-engine.
2. **Status:** IN PROGRESS — *engine layer authored + statically checked clean (0 blockers); build FAILURE diagnosed and source-FIXED (commit `a4cec47`); awaiting owner-Mac re-run*. The owner's first Mac build (commit `3b8463e` procedure) exited 1. Engineering traced the root cause to **22 real compile/UHT errors** in the Phase-1 UE C++ (authored but never compiled in-sandbox before), all now fixed: removed invalid `PrimaryComponentTick` usage in all 5 `UWorldSubsystem` ctors; added `UENUM()` + global-scope enums; added 8 missing includes; `AllowPrivateAccess` on private Blueprint property; `EActorIteratorFlags::AllActors`; Unity-build symbol rename. Added `build_phase1_diagnostic.sh` (persistent log + exact failing command) and a `PrimaryComponentTick`-in-`UWorldSubsystem` regression guard. `build_readiness.py` 0 blockers/0 warnings; pure logic core 947/947. **NOT engine-compiled** — UE absent from sandbox; owner-Mac build + PIE is the sole authority.
3. **Owner action (next):** `cd TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1 && bash build_phase1_diagnostic.sh`. On success: create `OMEGA_VALLEY_PHASE1.umap`, set Game Mode = `TDDOmegaValleyGameMode`, PIE. On failure: send the `BUILD_DIAGNOSTIC_<ts>.log` back to Engineering (do not fix C++ yourself).
4. **Blocking dependency:** owner-Mac execution (sole UE authority). Phase 1 is NOT complete until build + PIE + acceptance logs are reviewed.

## Blocked-work rules
- **Design continues all work not depending on outstanding approvals** (CD-3, CD-2, owner approval of strategy).
- **No exploratory asset is promoted to approved production status without required sign-offs** (QUALITY §7): each asset needs the automated QC (agent) + owner visual review + (for enemies) CD-3 ratification + CD-2 cultural clearance where applicable.
- **Enemies/bosses are not built before the combat foundation + enemy interface exists** (`WORLD_ARCHITECTURE.md`).
- Every blocker above is **assigned, measurable, and actively progressing** (or explicitly awaiting a named owner's decision, never silently unowned).
