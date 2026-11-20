# Technical Research Register

**Document ID:** TDD-PLAN-TRR-001 · **Version:** 1.0 · **Date:** 2026-11-20
**Owner:** Takeover Technical Lead · **Status:** Research complete for M1–M4 scope; items marked OPEN re-verify on the first reference-hardware run.

**Evidence key:** `[E]` = Epic official documentation fetched 2026-11-20 (URLs inline) · `[A]` = Agent 4 assessment (2026-11-18, fetched Epic docs, in-repo at `origin/arena/b2c58152-tdd:docs/`) · `[R]` = accepted in-repo document (ADR / M1 spec / MEAD / Agent 2 world docs) · `[T]` = technical judgement of the Takeover Lead, to be confirmed by a named verification run.

**Method note:** each significant choice below is compared against the game's actual requirements (single-player third-person narrative action, 8 chapters, cinematic ambition, one M4 dev Mac + one future DX12 reference machine + optional PS5), not against popularity. Decisions already made by accepted ADRs are **ratified, not re-decided**; where new research changes an assumption, the register says so explicitly (TR-01, TR-04).

---

## TR-01 Rendering and lighting architecture

**Requirement:** cinematic-quality third-person action; final quality sign-off target = Windows DX12 (and PS5 later); dev host = Mac Metal (M4); min-spec RTX 3060 Ti @ 1440p 60 fps [R: MEAD §15.1, D-12].

| Option | Assessment | Verdict |
|---|---|---|
| Lumen HWRT (DX12) + Nanite + VSM | Epic's current macOS requirements page: Nanite/VSM = **Apple Silicon M2+ (beta)**; Lumen HWRT + MegaLights = **M2+ (experimental)** — i.e. the owner's M4 *can* run both at beta/experimental level [E: dev.epicgames.com "MacOS Development Requirements", fetched 2026-11-20]. **This updates Agent 4's 2026-11-18 reading** (which recorded Nanite as "not a production path on Metal") [A] | **Primary stack** for Windows/PS5 sign-off; **usable on the Mac at beta level for look-dev** |
| Lumen SWRT on Mac | Supported M1+ [E same page] | Mac fallback when HWRT-on-Metal is unstable |
| Legacy SSR/deferred lighting | Cheaper, lower quality | Rejected: the approved boards' quality bar (volumetric canopy light, wet surfaces) needs GI; min-spec 3060 Ti still runs Lumen per Epic scalability docs [A] |
| Nanite for all geometry | [E: Nanite docs] | **Yes**, with authoring rules: clean UVs, sensible tri counts, no reliance on sub-pixel detail; Mac beta status means Windows is the gate (no re-authoring risk if assets are Nanite-clean) |

**Decision (D-19, new):** Lumen HWRT + Nanite + VSM + World Partition is the rendering stack. Mac development uses Lumen (HWRT-on-Metal when stable, SWRT otherwise) purely as an *approximate* look-dev surface — **final lighting sign-off happens only on the DX12 reference machine** (and PS5 devkit when available). MegaLights only after the 8-light cap is proven insufficient in combat arenas [R: MEAD §15.3].
**Why:** quality target met on the reference platforms without a pipeline that must be rebuilt; the M4's beta Nanite support converts the dev Mac from "logic-only" to "look-dev-capable", de-risking lighting iteration without moving the sign-off platform.
**Verification:** first reference-hardware capture `TDD-Perf.ReferenceScene.CH01_Encounter` [R: MEAD §15.4]; Mac-side Nanite stability check logged in the toolchain gate.

## TR-02 Materials, shaders, visual effects

**Requirement:** consistent PBR world from approved boards (earthen, hardwood, textile, bronze — see Art Bible material language); VFX readable at 1440p on min-spec; Metal dev constraints.

| Option | Assessment | Verdict |
|---|---|---|
| Classic material system (PBR) | Battle-tested on all platforms incl. Metal; all approved-surface types are standard PBR | **Default for 100% of shipped materials** |
| Substrate | Newer layered material model; Agent 4 recorded "Metal-specific issues/cost" [A]; no approved-surface requirement needs it yet | **Deferred** — revisit only with a named requirement (e.g. layered paint/wax on a hero prop) and a Metal/Windows parity test |
| World Manifest / PCG for environment dressing | PCG authoring works on Mac [A] | **Adopt PCG** for repeatable environment scatter (foliage density, rubble) with seeded, reproducible placements — also gives deterministic scene state for tests |
| Niagara (particles) | Core GPU emitters on Metal work, some sim modes limited/slow [A] | **Niagara only**; author FX for DX12/PS5, iterate on Mac; per-VFX budget from MEAD §15.2 (translucency/VFX 1.5 ms GPU) |
| Custom shaders | Every custom shader doubles shader-compile/stutter risk and cross-platform cost | **Prohibited without ADR**; use engine material functions first |

**Decision (D-20):** classic PBR materials; PCG for environment dressing (seeded); Niagara with per-emitter frame budgets; no custom shaders without ADR + Mac/Windows parity evidence.
**Verification:** material consistency vs approved boards via controlled screenshot A/B (QUALITY_ENGINEERING_PLAN §1); VFX budget via `stat GPU` capture.

## TR-03 Character animation and blending

**Requirement:** cinematic-quality, responsive locomotion and combat; no visible snapping/pop; root-motion synchronisation exact (AC-26); content pipeline not yet staffed (Q-18 open).

| Option | Assessment | Verdict |
|---|---|---|
| AnimBP state machine + blend spaces | Deterministic, fully testable, works with placeholder mannequin clips, no corpus requirement | **M1–M3 default** [R: ADR-0005] |
| Motion Matching (Pose Search) | **Production-ready** (shipped in UE 5.7, used in Fortnite); requires a large tagged corpus that does not exist [E/T: strayspark 2026-06-11 & 2026-08-17 surveys, fetched 2026-11-20; Epic Pose Search plugin docs] | **Upgrade path** behind `ITDDLocomotionAnimProvider` [R: ADR-0005]; activation requires the M3 animation corpus (Phase 3+), with a measured A/B vs blend spaces |
| Mover (new CMC successor) | Still **Experimental** in 5.7, APIs subject to change [T: same surveys] | **Rejected for this production cycle** — ADR-0013's contract is built on CMC; re-evaluate at a milestone boundary only with an ADR |
| Control Rig / IK Retarget | Standard; Mac-supported [A] | **Adopt** for retargeting approved/placeholder clips to the Adanna skeleton; foot IK for ground interaction (MEAD §8.4) |
| Motion Warping | Engine-native, Mac-supported [A] | **Adopt** for traversal/attack aim [R: ADR-0013, M1 spec §3.7] |

**Decision (D-21):** ADR-0005 ratified exactly as written (provider interface; blend spaces now, MM when the corpus exists). Foot-slide ≤ 5 cm in lab at 60 fps [R: MEAD P1 exit].
**Verification:** `TDD-Functional.Movement.*` (M1 spec §5); animation quality gates in QUALITY_ENGINEERING_PLAN §2.

## TR-04 Root motion and traversal

**Requirement:** the accepted contracts (ADR-0013 v1.4 + M1 spec §3.2.2/§3.5/§3.7) are the law: CMC performs translation; no `MOVE_None` under root motion; two-phase validation; bounded relocation + unbudgeted hold; E1–E7.

| Option | Assessment | Verdict |
|---|---|---|
| CMC + `RootMotionFromMontagesOnly` + scoped movement updates | The only model that satisfies ADR-0013 on a stable, non-experimental component | **Adopted** [R: ADR-0013] |
| `FRootMotionSource_MoveTo*` for authored non-animation travel | Keeps every capsule move inside CMC's swept-update path (no `SetActorLocation` teleports) | **Adopted** [R: ADR-0013] |
| Custom kinematic traversal (no CMC) | Bypasses collision semantics; violates "no teleport into geometry" | **Rejected** |
| Mover-based traversal | Experimental (TR-03) | **Rejected this cycle** |

**Decision:** no new decision — ADR-0013 v1.4 ratified in full (it *is* the research answer). The one open mechanism question (does CMC consume root motion in `MOVE_Flying`/`MOVE_Walking` as specified) is closed by the named test `TDD-Unit.Movement.RootMotionAppliesToCapsule` on the first Mac run — provisional-mechanism rule §3 of the ADR applies.
**Verification:** AC-26 + M2 `TraversalExitRevalidation` / `TraversalAbortPaths` [R: M1 spec §5].

## TR-05 Character physics and collision

**Requirement:** zero unexplained penetration (per-frame asserted in M1 tests); stable step/slope/corner behaviour (AC-07…AC-13); capsule is the single player collider.

| Option | Assessment | Verdict |
|---|---|---|
| CMC built-in (sweep-based, no per-frame penetration by construction) | Proven; all M1 ACs are written against it | **Player capsule: CMC only** |
| Custom character physics (Chaos-driven) | No requirement; adds instability | **Rejected** |
| World collision: static meshes + simple collision for blockout, convex/complex for hero props | Standard | **Adopt**; interactables via overlap, not physics push |
| Ragdoll for death (Chaos) | M1 spec v1.3 explicitly distinguishes ragdoll death from montage death (presentation timing) [R] | **Adopt** for death presentation, data-selected per enemy/character |

**Decision (D-22):** CMC is the only player-capsule authority; world uses engine static/convex collision; ragdolls for death presentation only; tunneling guarded by CMC sweep + high-speed test scenario (QUALITY_ENGINEERING_PLAN §3).
**Verification:** per-frame penetration counters in every `TDD-Functional.Movement.*` test; drop-tower scenario.

## TR-06 Combat state machines and hit detection

**Requirement:** frame-precise melee (M1 state machine exists by M1 exit; combat kit per MEAD §4.2; C-05 telegraph contract parked as design [D-02]); deterministic outcomes from explicit rules.

| Option | Assessment | Verdict |
|---|---|---|
| `UTDDCharacterStateMachine` (M1 spec §3.2) extended with combat states (Attack/Block/Parry already tabled) | Single state authority; 196-pair exhaustiveness already spec'd (AC-22/AC-23) | **Adopt** — combat states are rows in the same table, not a second machine |
| GAS abilities for attack flow | ADR-0004 explicitly rejects this (cancel windows, unit-testability) | **Rejected** [R] |
| Hit detection: physics overlap on custom channels (`ECC_Damage`), hit windows = data on attack assets, sampled at notify frames | Deterministic, testable without animation (pure-math suites possible: `TDD-Unit.Combat.*` [R: MEAD §14.2]); avoids "animation happened, so it hit" | **Adopt** [R: MEAD §5.3] |
| Overlap-all-frames dedup | Prevents double-hit on multi-frame overlap [R: MEAD `TDD-Unit.Combat.HitDedup`] | **Adopt** |

**Decision (D-23):** one state machine for all player states; hit windows are data + notifies; damage enters through one pipeline (`FTDDDamageRequest` → GAS effects per ADR-0004); outcomes are rule-computed, never animation-computed.
**Verification:** `TDD-Unit.Combat.*` (no world) + `TDD-Functional.Combat.*` (world) [R: MEAD §14.2]; deterministic combat case battery (QUALITY_ENGINEERING_PLAN §4).

## TR-07 Damage, stagger, posture, death

**Requirement:** the accepted taxonomy is frozen: staggering vs non-staggering (data: `bCausesStagger`, approved by D-03), same-frame posture-break promotion, Dead > Stagger, cinematic freeze, E1–E7, single restoration [R: M1 spec §3.2.1–3.2.3].

| Option | Assessment | Verdict |
|---|---|---|
| Posture as GAS attribute with blocking modifiers | ADR-0004: GAS for the attribute/effect layer | **Adopt** [R] |
| Stagger = forced state transition (priority 80) with hit-reaction montage | Already accepted; montage-end OR duration = recovery | **Adopted** |
| Death flow: `Dead` state (priority 100) → flow system (checkpoint respawn) | M1 spec tables it; persistence per ADR-0007 (memory discovery writes immediately) | **Adopted** |
| Hitstop | MEAD `TDD-Unit.Combat.HitStopExpiry`; gameplay-time window for i-frames (M1 §3.5) so hitstop cannot desync | **Adopt** (data-bounded, expiry-tested) |

**Decision:** no new architecture — implementation contract only; the open design surface (enemy posture values, parry reward tuning, Q-07 kit values) is data pending CD tuning.
**Verification:** full taxonomy matrix already spec'd in `TDD-Unit.Movement.StateSemantics` (v1.2 additions) + M3 combat suites.

## TR-08 Enemy AI and decision-making

**Requirement:** readable, fair, testable behaviour; no simultaneous-attacker pileups; designer-extensible without C++; budgets (≤ 14 AI agents [R: B-12]).

| Option | Assessment | Verdict |
|---|---|---|
| StateTree (behaviour selection) + AIPerception (sight/hearing/damage) + `UTDDCombatBrainComponent` + **combat director token system** (`UTDDCombatDirectorSubsystem`, pure-function token policy) | ADR-0006 decision; pure functions = unit-testable without a world (`TDD-Unit.AI.TokenPolicy`); fairness by construction | **Adopt** [R: ADR-0006] |
| Behaviour Trees | Older; weaker for data-driven per-archetype behaviour | Superseded by StateTree choice [R] |
| Mass AI for crowds/background NPCs | Five-tier NPC model: tiers 4–5 (background/scripted) use Mass or cheap tickers; tiers 1–3 (interactive enemies) use full AI [R: WORLD_ARCHITECTURE §5, ADR-0006] | **Adopt tiered** — Mass only for non-interactive population |
| Bosses: declarative phase graphs (data) executed by one controller | ADR-0107; pure-function phase selector (seeded tests) | **Adopt** [R] |

**Decision:** ADR-0006 + ADR-0107 ratified. Enemy archetypes remain PROPOSED until CD-3 ratification (content gate, not architecture gate) [R: B-02].
**Verification:** token/phase unit tests + 6-enemy concurrent-attacker measurement [R: ADR-0006] + AI scenario battery (QUALITY_ENGINEERING_PLAN §5).

## TR-09 World simulation and interaction

**Requirement:** 8 chapters at real scale on streaming; deterministic world state (canon guards, OAD-24); interactions with prompts; checkpoints.

| Option | Assessment | Verdict |
|---|---|---|
| World Partition + data layers | Authoring works on Mac [A]; the standard for real-scale open chapters; streaming budgets already set (≤ 12 resident locations, ≤ 20 scenes, ≤ 8 s stream-in [R: B-12]) | **Adopt** |
| Interaction framework `ITDDInteractable` (Core contract) | MEAD §4.5 (prompts, hold variants, requirements via tags) | **Adopt** [R] |
| World state: time/weather as data layers, per MEAD §6.2 (OAD-24 compliant) | Deterministic + saveable | **Adopt** [R] |
| Environment physics: Chaos for breakables/fallables/interactable physics | Engine-native; tested per-scenario (QUALITY_ENGINEERING_PLAN §3) | **Adopt, bounded** (physics object count budget per scene in MEAD §15.3 style) |

**Decision (D-24):** World Partition from the first real slice (not a "later" migration); interaction via the Core contract; environment physics bounded and scenario-tested.
**Verification:** `TDD-Functional.World.*` [R: MEAD §14.2] + streaming budget measurement (closes B-12).

## TR-10 Camera and cinematics

**Requirement:** accepted five-criteria camera system (M1 spec §3.6) + rig table (MEAD §4.3) + cinematics that never corrupt gameplay state.

| Option | Assessment | Verdict |
|---|---|---|
| Camera manager (shakes/FOV/PP, PC-owned) + rig component (desired params, pawn-owned) + spring arm | Lifecycle-correct split already accepted; shake via data assets, never code curves [R: M1 §3.6, MEAD §4.3] | **Adopted** |
| Sequencer/CineCameraActor for cinematics with 0.4 s restore + rig takeover detection | Accepted; skip-leaves-state-consistent test exists [R: MEAD §14.2 `TDD-Functional.Cinematic.SkipLeavesStateConsistent`] | **Adopted** |
| Movie Render Queue / Movie Render Graph for marketing shots | Works on Mac for blocking/iteration, not final grade [A] | **Adopt for iteration**; final marketing renders on reference hardware |
| Camera-assist + accessibility sliders (shake scale, motion blur, FOV) | MEAD §12 accessibility baseline | **Adopted** |

**Decision:** no new architecture; M1 S5 implements the five criteria exactly; cinematics get their own test suite at M7.

## TR-11 Audio

**Requirement:** adaptive environmental + combat audio; MetaSounds-only decision stands (ADR-0009, Q-05 default).

| Option | Assessment | Verdict |
|---|---|---|
| MetaSounds + Sound Concurrency + submixes + Quartz | ADR-0009; wrapped behind `ITDDAudioService` so a later middleware decision cannot leak into gameplay [R] | **Adopted** |
| Middleware (Wwise/FMOD) | Cost + pipeline weight; no requirement forcing it | **Rejected now** (revisit only with a named mixing requirement) |

**Decision:** ADR-0009 ratified; audio implementation at M7 with the feedback budget from MEAD §11.3; VO/music content per `11_AUDIO_AND_MUSIC` (Drive folder currently empty — content decision Q-18-adjacent).

## TR-12 UI and interaction systems

**Requirement:** gamepad+mouse+keyboard parity (AC-27); live rebinding; accessibility (Q-10); localisation-ready (Q-13).

| Option | Assessment | Verdict |
|---|---|---|
| UMG + Slate; Enhanced Input actions/contexts with mapping-context push/pop on state changes | M1 spec §3.1/§3.4 lifecycle rules | **Adopted** |
| String Tables for all copy; verbs as GameplayTags | MEAD §4.5/§12 | **Adopted** |
| Fullscreen vs in-game menus | In-game (chapter-structured game; saves are checkpoint+manual) | **Adopt in-game** |

**Decision:** no new research needed; UI framework lands at M7 (MEAD P6) with pseudo-loc build test [R: MEAD P6 exit].

## TR-13 Performance profiling and optimization

**Requirement:** 60 fps min-spec with explicit frame budgets [R: MEAD §15.2–15.3]; no optimization claim without profiling evidence (ADR-0012 + user Phase 6C rule).

| Option | Assessment | Verdict |
|---|---|---|
| Insights (unrealInsights) traces + `stat unit/GPU/game/streaming` + `memreport -full` | Standard toolset already mandated [R: MEAD §15.4] | **Adopted** |
| Fixed reference scene `TDD-Perf.ReferenceScene.CH01_Encounter` (fixed camera path/spawns/VFX) | Deterministic perf regression detection; regression rule: > 5 % frame-time or > 100 MB VRAM blocks the gate [R: MEAD §15.4] | **Adopted** |
| Gauntlet (packaged-build soak + perf) | MEAD T3/T4 tiers | **Adopted** |
| PSO precompilation + shader compile cache shipped | Zero packaged-build shader stutter (MEAD §15.3) | **Adopted** |
| Metal profiling on Mac | Useful for dev-loop regressions, **not** for budget sign-off | **Dev only** |

**Decision:** budgets are law from the first slice; the reference machine (D-12 purchase at M6 entry) is the only authority for GPU numbers.

## TR-14 Automated testing

**Requirement:** every claim verifiable without a human; evidence in-repo (ADR-0012, ADR-0101, D-07).

| Option | Assessment | Verdict |
|---|---|---|
| Unreal Automation framework exclusively (`TDD.<Area>.<Behaviour>`, flags `EditorContext \| EngineFilter \| ProductFilter`) | ADR-0101 ratified; CLI run with `-ReportExportPath`; named suites already enumerated [R: MEAD §14.2] | **Adopted** |
| Standalone host-compiler C++ for pure math (existing pattern: dodge math 18/18) | Runs in this sandbox; catches math regressions without the Mac | **Adopted** (keep, extend to combat math, save serialisation) |
| Functional Testing plugin (actor-level, test map) | MEAD T2 tier | **Adopted** |
| Automation Driver + Gauntlet (scripted-input chapter runs) | MEAD T3 tier | **Adopted at M8** |
| TDD_RESULT line format (`TDD_RESULT <test> <PASS|FAIL> <metric>=<value>`) | Greppable, quotable [R: M1 spec §5] | **Adopted as the standard result format for all suites** |

**Decision:** tiering per MEAD §14.1 (T1 every commit in-sandbox where pure; T2 every Mac run; T3 nightly from M8; T4 every gate; T5 manual per phase).

## TR-15 Build pipelines

**Requirement:** reproducible builds from a tagged commit; one-command owner-Mac verification; packaging without editor; future CI.

| Option | Assessment | Verdict |
|---|---|---|
| `Tools/engine/mac_build.sh` (proven at M0) + `verify_toolchain.sh` gate (today's 036d2b7) | Proven pattern: env → generate → build both targets → headless automation → evidence bundle | **Adopted as the canonical build entry point** (extended, not replaced) |
| RunUAT packaging (Cook/Package) on the Mac | Works [A: Agent 4 §1.3] | **Adopted** (Gate D from M1 exit) |
| Git LFS for binaries (ADR-0104: text-only git, ≤ 5 MB rule, content definitions as CSV/JSON) | ADR-0104 ratified | **Adopted**; LFS provisioning = owner action (D-19-adjacent, see ROADMAP M2) |
| GitHub Actions macOS runners for package verification | Limited UE licensing/quota practicalities; optional | **Deferred** — owner Mac is the build host; a hosted smoke runner is a release-phase option, not a blocker |
| Windows build host (future reference PC doubles as it) | Agent 4: the single most important non-Mac purchase [A] | **Adopted at M6 entry** (D-12) |

**Decision:** build = one command on the owner Mac; packaging = RunUAT same host; LFS on; hosted CI deferred with a named decision point at M10.

## TR-16 Engine/platform facts (verified 2026-11-20)

| Fact | Source | Consequence |
|---|---|---|
| UE 5.8 is the last planned UE5 major; 5.9 preview-only; UE6 EA late 2027 | [A: Agent 4, Epic release coverage 2026-11-18] | Pin 5.8.x; no wait (ADR-0001 ratified) |
| Owner toolchain: UE 5.8.4 (CL 58902052), Xcode 27.2, macOS 27.2.1, M4 16 GB | [R: commit `036d2b7`, today's editor screenshots] | Toolchain gate is authoritative; Epic's Xcode 26.4 incompatibility was closed in 5.8.4 (UE-396802) [R: commit message] |
| Mac: min 16 GB (Epic), recommended 32 GB; M1/M2 min, M3 recommended; Metal 1.2 GPU | [E: Epic macOS requirements, fetched 2026-11-20] | 16 GB is *minimum* — D-18 (NVMe) + plugin pruning mandatory; a 32 GB machine upgrade is a Phase-3 option, not a blocker |
| Nanite/VSM M2+ beta; Lumen HWRT/MegaLights M2+ experimental (on Metal) | [E: same Epic page] | TR-01 decision (Mac look-dev at beta level) |
| PS5 requires Sony GDPA + devkit + Epic-verified platform integration; retail PS5 never runs dev builds | [A: Agent 4 §2] | PS5 = gated target (D-04/D-16); no PS5-specific code before devkit |

## TR-17 Content production technologies (asset pipeline)

**Requirement:** 8 chapters of approved-board-faithful content; art authority on Drive with CD verdicts; no unapproved promotion.

| Option | Assessment | Verdict |
|---|---|---|
| Drive Art Bible → 3D via labelled blockout → approved-final, per CD verdicts; ADR-0008 canon gating in-repo validators | The existing pipeline is sound; MEAD §9.8 adds engineering support (canon status fields, validator, cultural sign-off hooks) | **Adopted** — engineering adds `FTDDCanonStatus` + editor validators; content stays on the Creative Director's authority |
| Adanna: mannequin proxy (M1–M2) → technical proxy GLB (labelled interim) → production character at creative approval | T00 D-14; the M1 art spec's identity locks are the contract | **Adopted** |
| MetaHuman | Available; but the approved Adanna identity is *not* a MetaHuman-style look and the art spec forbids inventing features | **Rejected** — identity conflict; use Control Rig retargeting instead |
| GLB/OBJ as the exchange format (Phase 3 practice: GLB + OBJ + rig JSON + import manifest with hashes) | Proven today (Phase 3 handoff) | **Adopted as the art↔engine exchange standard** (ADR-0104 binary rules apply to what enters git) |

**Decision (D-25):** canon-status fields + validators in the engine (MEAD §9.8); GLB exchange standard; no MetaHuman.

---

## Research gaps to close (named, owned, dated)

| ID | Gap | How closed | Due |
|---|---|---|---|
| RG-01 | Nanite/Lumen-HWRT stability on M4 + macOS 27.2.1 (beta/experimental per [E]) | First reference-scene capture on the owner Mac logged in the toolchain gate; decision: keep/ fall back to SWRT | M1 exit run |
| RG-02 | CMC root-motion consumption in `MOVE_Flying`/`MOVE_Walking` as ADR-0013 specifies | `TDD-Unit.Movement.RootMotionAppliesToCapsule` on first Mac run (ADR-0013 §3 provisional rule) | M1 S3 |
| RG-03 | Motion Matching corpus requirements (clip count, tagging) for the M3+ upgrade | GASP sample study + 1-week spike on the M4 when the animation corpus exists | M3 entry |
| RG-04 | 16 GB editor+cook headroom with World Partition content | Measured during first WP slice; trigger D-18 + plugin pruning; 32 GB upgrade option if blocked | M5 |
| RG-05 | Windows DX12 reference-hardware bring-up (install, driver, budget baseline) | One-time bring-up run on the purchased machine; baseline capture archived | M6 entry |
