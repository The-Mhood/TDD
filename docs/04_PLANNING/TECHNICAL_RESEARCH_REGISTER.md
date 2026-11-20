# Technical Research Register

**Document ID:** TDD-PLAN-TRR-001 · **Version:** 1.1 · **Date:** 2026-11-20
**Owner:** Takeover Technical Lead · **Status:** Research complete for M1–M4 scope; items marked OPEN re-verify on the first reference-hardware run.
**v1.1 (review pass):** reference-PC timing reconciled to one authoritative date — **order at P-01 (Day 0)**, arrives W1, calibrated W2, Windows CI node from W2 (TR-13/TR-15 corrected; TR-18 added with full specification/cost/validation); TR-19 adds the technical-claims audit (engine-behaviour statements that were phrased as guarantees are reclassified with measurable ACs and named verification methods); RG-05 retimed.

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

**Decision:** budgets are law from the first slice; the reference machine (D-12 — **ordered at P-01/Day-0 under the accelerated plan**; specification and validation procedure in TR-18) is the only authority for GPU numbers. The RTX 3060 Ti / 1440p@60 anchor is a *budget target, not a proven fact*: it becomes "established" only when TR-18's benchmark procedure has been executed on the reference scene.

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
| Windows build host (future reference PC doubles as it) | Agent 4: the single most important non-Mac purchase [A] | **Adopted — order at Day 0 (P-01); Windows CI node operational from W2** (D-12, timing clarified 2026-11-20; see TR-18) |

**Decision:** build = one command on the owner Mac (daily test train, ROADMAP v2.0 §4.3); packaging = RunUAT same host; LFS on; the reference PC serves as the self-hosted Windows CI node from W2 (supersedes the old "hosted CI deferred to M10" timing for the fast-track — hosted runners remain a release-phase option only).

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

## TR-18 Reference hardware — specification, cost, purchase timing, validation (v1.1)

**Requirement:** a DX12 reference machine that (a) is the sole authority for visual/perf sign-off (D-19), (b) defines the min-spec the game must hit (MEAD §15.1 anchor: 8-core + RTX 3060 Ti + 16 GB, 1440p@60, 1% low ≥ 50), (c) under the accelerated plan doubles as the **Windows build/CI node from W2** — so it must be present in W1.

**Purchase timing — single authoritative date (reconciles T00 D-12, TR-13, TR-15, ROADMAP, dep-map):** **order at P-01, i.e. ratification day (Day 0)**. The earlier texts carried three different timings — T00: "Phase 3 entry"; TR-15: "M6 entry"; ROADMAP/dep-map v1.0: "M2 exit" / "M5 entry (week 6–8)". Those were all correct *for the 13–14-month plan*, whose first sign-off need was ~W16. The accelerated plan (owner instruction, 4–8 weeks) needs Windows verification at **Checkpoint A (W4)** and look-dev/perf sign-off from **W3–W5**; with 1–2 weeks of used-market shipping lead, any order date later than Day 0 removes one of those. **All prior timings are superseded by Day-0.**

**Recommended specification (DX12, Windows 11 Pro):**

| Tier | CPU | GPU | RAM | Storage | OS | Est. cost (Nov 2026, used/new) |
|---|---|---|---|---|---|---|
| **Minimum (sign-off floor = min-spec anchor)** | Ryzen 5 5600 / i5-12400 (6c/12t) | RTX 3060 **12 GB** (closest current card to the 3060 Ti anchor; used 3060 Ti also acceptable if found ≤ 3060-12GB price) | **32 GB** DDR4-3200 | 1 TB NVMe Gen4 | Win 11 Pro | **$750–950** |
| **Recommended (dev + CI + headroom)** | Ryzen 7 5700X / i5-13600K (8c/16t+) | RTX 4070 / 4070 SUPER (or used RTX 3080 12 GB) | **32 GB** (64 if ≤ +$100) | 2 TB NVMe Gen4 | Win 11 Pro | **$1,300–1,700** (new) / $1,000–1,300 (used GPU) |

- **Why 32 GB even though the min-spec anchor is 16 GB:** Epic recommends 32 GB [E: Epic macOS page equivalent guidance for PC: 32 GB recommended]; World Partition headroom (RG-04); and the machine runs build + editor + test train concurrently as a CI node. The *shipped min-spec claim* stays 16 GB: the RAM budget (≤ 10 GB, MEAD §15.2) is measured on the reference machine and, by construction, leaves a 16 GB machine inside budget.
- **Alternatives considered:** (a) used RTX 3090 24 GB build (~$1,200) — maximum GPU headroom, +250 W PSU; acceptable if within the recommended-tier budget, not required. (b) Cloud GPU (e.g. g4dn-class) for CI overflow only — **not acceptable as the sign-off reference**: sign-off requires a stable, named physical machine identity (TR-13). (c) Mac Studio M3 Ultra as a *second* Metal dev host — optional, does not substitute for any DX12 requirement.
- **What can be tested on the current Mac (M4, 16 GB) immediately (W0–W2):** all in-workspace pure-core C++ suites (g++ 12.2 verified 2026-11-20); all UE logic + world functional tests and gauntlets on Metal at **dev level** (D-19: look-dev/approximate, not sign-off); movement/traversal/combat verification (AC-01…31); save/load, UI, audio event verification; performance *development* captures (labelled `DEV-HW`). **What requires the Windows reference machine:** final visual sign-off (Lumen HWRT / DX12; Metal is beta/experimental per [E]), all performance sign-off + the min-spec 1440p@60 claim, packaged primary-platform builds, PSO precompilation / zero shader-stutter check (RRP G-07), RHI-specific behaviour (R-21), and — from W2 — CI runs that de-risk the single-Mac bottleneck.

**1440p/60 validation procedure (the RTX 3060 Ti class is "established" only after this is executed — per owner instruction):**
1. Build `TDD-Perf.ReferenceScene.CH01_Encounter` (fixed 8-enemy spawns + 4 VFX layers + scripted combat path — MEAD §15.3) in a Development + Shipping pair.
2. 3 × 10-minute runs: cold start, warm, steady-state (post 5-min burn-in). Capture `.utrace` + frame histogram + `memreport -full`.
3. **Pass criteria (all, on the minimum-tier card at 1440p internal):** mean ≥ 59.5 fps; 1% low ≥ 50 fps; hitches > 50 ms ≤ 1 per 10 min; VRAM ≤ 8 GB; RAM ≤ 10 GB.
4. Record machine identity (OS build, GPU + driver version, CPU, RAM, UE 5.8.4 CL, RHI) in the ledger; archive traces (LFS) + CSV summary (text).
5. Re-run at every chapter gate and at final sign-off; the regression rule (MEAD §15.4: > 5 % frame-time or > 100 MB VRAM blocks) applies from the first capture.
6. If the minimum tier fails any criterion: the *budget* or the *min-spec* changes — via documented review + ADR, never by silent acceptance (Roadmap Rule 2/6).

**Owner actions:** ratify tier (minimum vs recommended) in the P-01 batch; order Day 0; ship to the build location; one-time Windows setup (UE 5.8.4 install, ~1 h, runbook provided at P-04).

## TR-19 Technical claims audit (v1.1)

**Mandate (owner, review pass):** statements describing engine behaviour as *guaranteed* when it still requires testing must be reclassified; every requirement needs a measurable AC + named verification method. This section is the audit of the planning set (and the accepted specs it inherits); the same conventions now apply to all future documents.

**Claim classes (binding convention):**
- **[DS-G] Design guarantee** — a property we *enforce in code* (assertion/arbitration/data); holds only while the enforcing code and its tests hold. Never "the engine guarantees this."
- **[BUD] Budget** — a numeric target; unproven until measured on the named hardware.
- **[EN-V] Engine behaviour** — plausible UE behaviour we rely on; must be verified by a named test before any claim cites it as fact.
- **[ST] Status claim** — a statement about the engine/platform's current state; requires a dated citation.
- **[UNV] Unverified** — no claim permitted; the document must say "to be verified by \<test\>".

| # | Claim as previously phrased | Where | Reclassified | Why | Measurable AC + named verification method |
|---|---|---|---|---|---|
| T1 | "No floating capsule / no teleport-into-geometry" | QUALITY P-1/P-2, MAC M2.5 | **[DS-G]** enforced by floor-trace + trace assertions in every state exit — not an engine property (UE capsule resolution is approximate; tunneling at high velocity is possible) | Engine does not guarantee non-penetration | AC: zero assertion failures; verification: 100-run movement sweep (M1-S1), 1000-placement fuzz (QG-PHYS #1), E1–E7 suites (M2.1–2.3) |
| T2 | "Deterministic combat outcomes (byte-identical × 3 runs)" | QUALITY C-1, MAC M3.5 | **[DS-G]** design target — same platform/build/seed → reproducible outcome log, *enforced* by: no async in gameplay paths, seeded RNG, fixed frame clock in tests. **Cross-platform determinism is NOT claimed** (RHI/FPU/task ordering may differ) | Reproducibility is a property of our constraints + test conditions, not a UE guarantee | AC: 10-case battery × 3 runs, outcome logs identical; verification: QG-COMBAT battery (QUALITY §4); any mismatch = P1 defect, root-caused — never re-baselined |
| T3 | "No animation pop on cancels (≤ 10 cm / ≤ 15°)" | QUALITY A-2 | **[DS-G]** design target via pose-matching/blend setup, **measured** per case — engine does not guarantee continuity | Anim blending can pop if mis-set | AC: per-cancel joint delta bounds; verification: cancel-case battery (QUALITY §4 cases 1–3) with 5-frame post-cancel capture |
| T4 | "Foot-slide ≤ 5 cm" | QUALITY A-1, MAC M3.7 | **[BUD]** measured lab metric, not a guarantee | IK/retarget quality varies per clip | AC: ≤ 5 cm over 30 s lab run per clip family; verification: foot-locator CSV (lab gauntlet); per-clip inventory gate at each animation milestone |
| T5 | "AI ≤ 2.0 ms" | QUALITY I-5, MEAD §15.2 | **[BUD]** budget — no measurement exists yet | Never measured on this codebase | AC: scope-measured ≤ 2.0 ms at 8 agents; verification: Insights scope report (M4-10, then every chapter gate); regression rule from first capture |
| T6 | "Visual parity Windows vs Mac" | MAC M5.7, QUALITY G-9 | **[EN-V]** — parity is **not expected and not claimed**; Metal Lumen/Nanite are beta/experimental [ST: Epic macOS page, fetched 2026-11-20] | Cross-RHI parity is untested and engine-marked experimental | AC: parity *documented* — identical capture set on both platforms, per-frame deltas recorded, Windows is the reference; verification: dual QG-SHOT sets + delta table (M5.7); any Metal-only crash = P1 |
| T7 | "World Partition streams with no visible holes" | MAC M2.6 | **[EN-V]** engine capability + our setup; never measured in this project | WP correctness depends on data/levels-of-detail config | AC: full traversal gauntlet completes with zero hole-exposure; verification: streaming gauntlet + streaming log (M2.6, then per chapter); pop-in counter in soak |
| T8 | "Nanite/VSM usable on M4 (beta); Lumen HWRT on Metal (experimental)" | TR-01, D-19 | **[ST]** status claim, cited [E: Epic macOS requirements page, fetched 2026-11-20] — plus our own stability evidence | Vendor status can change per release | AC: 4-h Metal stability soak clean (RG-01) before any Metal look-dev sign-off relies on it; re-verify at each UE patch |
| T9 | "Motion Matching is production-ready in UE 5.7 (Fortnite)" | TR-03, D-21 | **[ST]** cited [strayspark 2026-06-11 / 2026-08-17; GASP sample] — **not** evidence for *our* corpus | Production-ready for their corpus ≠ ours | AC: M3-10 spike passes (foot-slide ≤ 5 cm, blend edges clean on our clips) before MM adoption; revert path = provider interface (ADR-0005) |
| T10 | "Save round-trip byte-identical; no corruption" | MAC M6.2 | **[DS-G]** `USaveGame` serialization of a fixed payload is deterministic *by design* + atomic write (tmp→verify→rotate) enforced; **corruption resistance is a design guarantee enforced by the atomic-write protocol**, verified not assumed | FS-level behaviour (power loss) is not engine-guaranteed | AC: round-trip byte-identical; interrupt test → valid save or valid `.bak`, never torn file; verification: `TDD-Unit.Persistence.*` (named in MEAD §14.2) + M9-04 100-cycle soak |
| T11 | "No double-hits; taxonomy 100%; same-frame posture promotion; Dead > Stagger" | QUALITY C-2/C-4/C-5, MAC M3 | **[DS-G]** enforced by the single arbitration pipeline (M1 spec §3.2.1 ordering) | These are *our* rules, implemented and tested — not engine properties | AC: 40-cell taxonomy matrix; 10-hit-per-attack gauntlet; verification: QG-COMBAT + taxonomy suite (named in spec §5) |
| T12 | "60 fps @ 1440p on RTX 3060 Ti class" | MEAD §15.1, D-12, RRP §5 | **[BUD] [UNV until TR-18 executed]** — the anchor is a *target*, not a proven fact | Never benchmarked in this project (owner instruction: "do not treat as proven") | AC: TR-18 procedure pass (mean ≥ 59.5, 1% low ≥ 50, VRAM ≤ 8 GB, RAM ≤ 10 GB) on the reference scene; verification: 3 × 10-min runs, archived |
| T13 | "In-workspace (agent-side) testing of pure logic" | ROADMAP v1.0 §6, TR-14 | **[ST] verified with a scope limit:** the agent workspace has **no Unreal Engine** (ADR-0012, environmental fact) — agents cannot compile/run *UE-dependent* code. What is verified: the sandbox has **g++ 12.2 (checked 2026-11-20)** and a **proven precedent** (dodge math 18/18 host-compiled in-sandbox, TR-14). Therefore: UE-**independent pure cores** (new constraint, ADR-0109) are testable agent-side on every commit; **all UE-dependent code remains agent-unverifiable** and is verified exclusively on the daily Mac test train + Windows CI | v1.0 text over-claimed "in-sandbox suites for every commit" for all logic | AC: pure-core suites (state-transition table, damage arbitration, token policy, phase selector, narrative conditions, save schema) compile + pass under g++ in the agent workspace, evidence committed; verification: first pure-core suite at P-08 (W1 d1–d2), then per commit. Any UE header in a "pure" file = contract violation at merge review |
| T14 | "Chapter load ≤ 15 s cold / 5 s warm; hitches ≤ 1/10 min" | MEAD §15.3, MAC M7.c.1 | **[BUD]** targets, unmeasured | No streaming data exists yet | AC: measured per chapter on reference HW; verification: streaming reports (M2.7 first data point) + gauntlet |
| T15 | "PSO precompilation → zero packaged shader stutter" | TR-13, RRP G-07 | **[EN-V]** UE PSO precompile is effective for the common case but per-machine/per-driver; "zero" is verified, not assumed | Driver/OS variation | AC: 30-min clean-machine play, zero shader-compile events in log; verification: G-07 procedure per platform |

**Corrections applied in this review pass:** ROADMAP v2.0 (verification model per T13), QUALITY_ENGINEERING_PLAN v1.1 (T2/T3 phrasing + conventions), MAC v1.1 (M3.5 reproducible-not-guaranteed phrasing), dep-map v1.1 (S21/T6 notes), WBS v2.0 (verification assignments). **No accepted spec was changed**; where an accepted spec makes the same over-claim (e.g. M1 spec determinism ACs), it stands as-is — those are *requirements* (which are exactly the verification target), not claims of fact.

---

## Research gaps to close (named, owned, dated)

| ID | Gap | How closed | Due |
|---|---|---|---|
| RG-01 | Nanite/Lumen-HWRT stability on M4 + macOS 27.2.1 (beta/experimental per [E]) | First reference-scene capture on the owner Mac logged in the toolchain gate; decision: keep/ fall back to SWRT | M1 exit run |
| RG-02 | CMC root-motion consumption in `MOVE_Flying`/`MOVE_Walking` as ADR-0013 specifies | `TDD-Unit.Movement.RootMotionAppliesToCapsule` on first Mac run (ADR-0013 §3 provisional rule) | M1 S3 |
| RG-03 | Motion Matching corpus requirements (clip count, tagging) for the M3+ upgrade | GASP sample study + 1-week spike on the M4 when the animation corpus exists | M3 entry |
| RG-04 | 16 GB editor+cook headroom with World Partition content | Measured during first WP slice; trigger D-18 + plugin pruning; 32 GB upgrade option if blocked | M5 |
| RG-05 | Windows DX12 reference-hardware bring-up (install, driver, budget baseline) | One-time bring-up run on the purchased machine (arrives W1); baseline capture archived; Windows CI live from W2 | W2 (was: M6 entry — retimed for the accelerated plan) |
