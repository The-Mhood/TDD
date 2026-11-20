# System Requirements — Master Feature Inventory

**Document ID:** TDD-PLAN-SYSREQ-001 · **Version:** 1.1 · **Date:** 2026-11-20
**v1.1 (review pass):** S02 adds the UE-independent pure-core constraint (TR-19 T13, ADR-0109 — the verification model behind the accelerated plan); S15/S23 reference-PC timing corrected to the authoritative Day-0 order (TR-18); milestone references aligned to the fast-track weeks where they named the old schedule.
**Conventions:** `[ACCEPTED]` = requirement from an accepted in-repo specification (M1 spec v1.4, ADRs, MEAD TDD-MEAD-001, Agent 2 world docs, C-05 design record) — changes require the documented review process. `[NEW]` = Takeover Lead recommendation, ratifiable via ADR. Each system: 11 fields per the plan. "AC" = acceptance criteria location. Effort is agent-weeks (aw) unless stated; owner-Mac runs are part of each verification, not extra.

---

## S01 Project foundation & build system (M0)

| Field | Content |
|---|---|
| Current state | **Verified.** UE 5.8.4 project, 1 runtime module, Mac+Windows targets; M0 passed 2026-11-18 (2/2 automation); `mac_build.sh` + `verify_toolchain.sh` + `build_readiness.py` + report parser in-tree. |
| Intended behaviour | One command builds both targets, runs all automation, emits a committable evidence bundle; toolchain gate fails closed on unsupported environments. |
| Required functionality | Build/automation evidence bundle (index.json + SHA256, committable); packaging via RunUAT (Cook+Package); LFS on (ADR-0104); engine pin record (5.8.4 CL 58902052). |
| Dependencies | Owner Mac (only build host). |
| Architecture | Existing `Tools/engine/` extended: `mac_build.sh` (build+test), `pack_mac.sh` (new: packaging), `verify_toolchain.sh` (gate), `parse_automation_report.py`. |
| Implementation tasks | T01 packaging script + runbook; T02 LFS `.gitattributes` + provisioning; T03 M0 evidence archive (owner, 1 command); T04 M0′ consolidated run. |
| TDD requirements | `TDD.Foundation.*` (existing 2 tests) keep passing; packaging smoke = launch log + clean exit (Gate D format). |
| Integration | All later systems build through this; evidence bundles are the integration currency. |
| Performance | n/a (build times recorded, not budgeted). |
| Acceptance criteria | M0 record §3 gates B+C ✓ (re-run as M0′); Gate D first pass = packaged app launches to title/test map without fatal. |
| Completion evidence | Archived M0 bundle + M0′ report + first package log, all commit-linked in the quality ledger. |

## S02 Core architecture (module, types, tags, config, logging)

| Field | Content |
|---|---|
| Current state | Single module `TheDisobedientDaughter`; no core types yet. `[ACCEPTED]` target graph = ADR-0003 (9 modules) + MEAD §3.2; D-05 defers the split. |
| Intended behaviour | All shared types/interfaces/events live in one place; no cross-system header coupling; everything data-driven where the specs say so. |
| Required functionality | GameplayTags vocabulary (states, status, interact verbs, canon status); `FTDDDamageRequest`; state table schema; `ITDDInteractable`, `ITDDAudioService`, `ITDDSaveProvider`, `ITDDLocomotionAnimProvider` declarations; config data assets; named log categories. **Pure-core constraint (TR-19 T13, ADR-0109):** all arbitration/policy/transition/condition/serialization logic is implemented as UE-independent C++ with a thin UE wrapper — so the logic layer is testable agent-side (g++, no Mac queue) while all UE-dependent behaviour is verified on the daily train + Windows CI. A UE header inside a pure file is a merge-blocking contract violation. |
| Dependencies | M0. |
| Architecture | Single module now (D-05); files under `Source/TheDisobedientDaughter/Public/Core/` structured so the ADR-0003 split is a move, not a rewrite. |
| Implementation tasks | T05 tags + damage request struct (pure, testable); T06 provider interface declarations (empty implementations where content is absent); T07 log categories + error/warning discipline (no silent degradation — STATUS_AND_CLAIMS rule 4). |
| TDD requirements | `TDD-Unit.Canon.ValidatorRules` (MEAD §14.2); struct round-trip unit tests. |
| Integration | Contract list in SYSTEM_DEPENDENCY_MAP §3 — these are the parallel-work enablers. |
| Performance | Zero runtime cost target for tag lookups (precomputed). |
| Acceptance criteria | All MEAD §13.2 frozen surfaces exist as compilable types; unit tests green. |
| Completion evidence | Compilation + `TDD-Unit.*` report on a Mac run; contract table checked off in the ledger. |

## S03 Player movement & character controller (M1)

| Field | Content |
|---|---|
| Current state | Minimal pawn (spring arm/camera/legacy input/jump). 0/31 AC. |
| Intended behaviour | `[ACCEPTED]` M1 spec v1.4 in full: state machine (only writer), CMC subclass, Enhanced Input, buffering, coyote, AC-01…AC-31. |
| Required functionality | `UTDDCharacterStateMachine` (196 pairs), `UTDDCharacterMovementComponent` (step smoothing, slope overrides), `UTDDPlayerInputComponent` (Enhanced), input buffer, metrics harness (`TDD.Movement.Report`, CSV, frame stamps). |
| Dependencies | S02; test map S7. |
| Architecture | M1 spec §2.1 file list (authoritative) + §3 class specs. |
| Implementation tasks | = M1 execution scope S1–S6 (S1 world sweep tests, S2 floor validation, S3 character+CMC+state machine, S4 collision edges, S5 camera, S6 input). |
| TDD requirements | All `TDD-Unit.Movement.*` + `TDD-Functional.Movement.*` named in spec §5; Agent 2 defects ①②③ closed in S1–S2. |
| Integration | State machine API is the contract for combat/AI/cinematics/UI (dep map §3). |
| Performance | AC-28: player frame cost ≤ 0.30 ms (Development); L1/L2/L3 latency per spec. |
| Acceptance criteria | **AC-01…AC-31** (the single M1 gate) + M1-P1…P5 first-playable gate. |
| Completion evidence | 31/31 quoted `TDD_RESULT` lines; P1–P6 manual records; Agent 2 diff review; packaged launch (Gate D). |

## S04 Traversal (M2)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` contract only: M1 spec §3.7 + §3.2.2 (E1–E7, two-phase validation, hold phases, `FellOutOfWorld`). Not implemented. |
| Intended behaviour | Vault/mantle/ledge/drop/climb-ladder (MEAD §4.4) executing the accepted abort/restoration rules exactly. |
| Required functionality | `FTDDTraversalCandidate` (forward/down trace detection), per-type data-able montages with Motion Warping, exit-transform revalidation, `ResolveAbortFallback()` implementation, `TraversalExitRevalidation` + `TraversalAbortPaths` test suites. |
| Dependencies | M1 exit (state machine, CMC); placeholder traversal clips. |
| Architecture | M1 spec §3.7 + §3.2.2–3.2.3 (no new design allowed — the contract is the design). |
| Implementation tasks | T08 candidate detection + data asset; T09 `ResolveAbortFallback()`/`ResolveHold()` (pure-logic first, `TDD-Unit.Movement.FallbackResolution` — spec already enumerates the 5+ budget assertions); T10 montage warp integration; T11 E1–E7 functional tests. |
| TDD requirements | `TDD-Functional.Movement.TraversalExitRevalidation` (E1/E2), `...TraversalAbortPaths` (E3–E7 incl. lethal+staggering precedence, cinematic no-drop, 4a/4b/4c, mid-abort placement failure, mid-resolution forced transitions, budget-0, kill-plane) — all enumerated in spec §5, v1.3/v1.4 additions included. |
| Integration | Consumes state machine; exposes traversal events to AI/narrative (checkpoint on fell-out-of-world). |
| Performance | Resolution ≤ 1 frame (spec rule); no async in resolution. |
| Acceptance criteria | All E-paths green with restoration checklist exactly once each; no floating capsule; no teleport into geometry. |
| Completion evidence | Named suite results in a Mac run + ledger entry. |

## S05 Camera system (M1)

| Field | Content |
|---|---|
| Current state | Fixed spring arm + follow camera. |
| Intended behaviour | `[ACCEPTED]` M1 spec §3.6: five stability criteria with per-mode thresholds; rig table (MEAD §4.3: exploration/combat/lock-on/traversal/cinematic/death); shake via data assets; FOV per rig; accessibility sliders. |
| Required functionality | `UTDDPlayerCameraManager` (shakes/FOV/PP), `UTDDCameraRigComponent` (desired params, takeover detection, 0.4 s restore), boom probe (12 cm sphere, 35 cm min, close-up mode), lock-on scoring + hysteresis (MEAD §4.3), five-criteria recorder + `TDD.Camera.Report`. |
| Dependencies | S03 (state machine events, pose). |
| Architecture | M1 spec §3.6 (authoritative). |
| Implementation tasks | = M1 S5; rig table data at M3 (combat rig), cinematics at M7. |
| TDD requirements | `TDD-Functional.Movement.CameraPenetration/AngularStability/Displacement/Recovery/AcquisitionSlew` (AC-14…AC-18). |
| Integration | Cinematic subsystem takes the view target (contract); UI reads camera state for prompts. |
| Performance | Camera cost inside AC-28; 5°/60 s scripted sweep as the standard capture. |
| Acceptance criteria | AC-14…AC-18. |
| Completion evidence | Named suite results + P2 manual procedure record. |

## S06 Combat kit — player (M3)

| Field | Content |
|---|---|
| Current state | Dodge exists (math+sweep). No attack/block/parry. `[ACCEPTED]` kit = MEAD §4.2 (light 4-chain, heavy posture-break, block 0.08 s guard-ready, parry 0.15 s window, lock-on, sprint-cancel). |
| Intended behaviour | Frame-precise melee with explicit cancel windows; all values data; outcomes rule-computed. |
| Required functionality | `UTDDCombatComponent` (attack data assets, hit windows, notify sampling), attack state rows in the state machine, lock-on (soft/hard), hit-stop (data-bounded). |
| Dependencies | M1 state machine; placeholder attack clips (mannequin); S02 damage contract. |
| Architecture | MEAD §5.2–5.3 + ADR-0004 (GAS for attributes, NOT for attack flow) + TR-06. |
| Implementation tasks | T12 attack data model (pure C++, `TDD-Unit.Combat.CancelRules`); T13 hit detection (custom channels, dedup, `TDD-Unit.Combat.HitDedup`); T14 block/parry (posture interaction); T15 lock-on; T16 combat training room + dummy. |
| TDD requirements | `TDD-Unit.Combat.*` (no world) + `TDD-Functional.Combat.LightChainConnects/DodgeIFrames/ParryStaggers/FeedbackComplete` (MEAD §14.2) + deterministic case battery (QUALITY_PLAN §4). |
| Integration | Damage pipeline S07; AI reads attack states for parry/block reactions; VFX/audio via feedback hooks. |
| Performance | Combat inside 1.5 ms game-thread budget (MEAD §15.2). |
| Acceptance criteria | MEAD P2 exit: full player-vs-dummy loop (chain, heavy, block, parry, dodge, stagger, death); no double-hit; every hit complete feedback. |
| Completion evidence | Named suites + training-room capture + ledger. |

## S07 Damage, posture, stagger, death (M3)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` contract (M1 spec §3.2.1–3.2.3; `bCausesStagger` approved D-03). Not implemented. |
| Intended behaviour | One pipeline for all damage: classify → promote (same-frame posture break) → arbitration → E-path or state transition → restore → entry; health independent; Dead > Stagger; cinematic freeze. |
| Required functionality | `UTDDAttributeSet` (GAS: health, stamina, posture), `UGameplayEffect` damage application, status tags, immunity/dodge i-frame integration, ragdoll-vs-montage death presentation, flow-system handoff (checkpoint respawn). |
| Dependencies | S02 (damage contract), S06 (hit sources), GAS module. |
| Architecture | ADR-0004 + M1 spec §3.2 (authoritative) + MEAD §5.4–5.6. |
| Implementation tasks | T17 attribute set + damage effects (pure math first); T18 pipeline arbitration (the spec's exact ordering as code); T19 reaction/stagger/hitstop data; T20 death + flow handoff. |
| TDD requirements | Taxonomy matrix already in `TDD-Unit.Movement.StateSemantics` (v1.2 additions) + `TDD-Unit.Combat.DamageMath/PostureAndStagger/HitStopExpiry` (MEAD §14.2). |
| Integration | Every enemy attack, player defence, boss phase emits into this pipeline — no side doors. |
| Performance | Damage resolution ≤ 0.2 ms worst case (budget note for profiling). |
| Acceptance criteria | MEAD P2 exit + taxonomy matrix 100% (staggering/non-staggering/lethal/lethal+staggering/posture promotion). |
| Completion evidence | Pure-math suite (in-sandbox) + world suite (Mac run). |

## S08 Enemy AI (M4)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` architecture (ADR-0006: StateTree + AIPerception + combat brain + token director; ADR-0107 bosses). Archetypes PROPOSED, not ratified (CD-3). No code. |
| Intended behaviour | Readable, fair, testable behaviour; concurrent-attacker caps by construction; designers extend via data. |
| Required functionality | `UTDDCombatDirectorSubsystem` (pure token policy), `UTDDCombatBrainComponent`, StateTree per archetype, perception (sight/hearing/damage), `UTDBossComponent` + declarative phase graphs, encounter manager. |
| Dependencies | S07 (damage pipeline); test encounter; CD-3 for real archetypes (placeholders until then). |
| Architecture | ADR-0006 + ADR-0107 (authoritative) + MEAD §7. |
| Implementation tasks | T21 token policy (pure, in-sandbox unit-testable now); T22 phase selector (pure, seeded tests); T23 perception + StateTree scaffolding; T24 pilot encounter (placeholder archetype, 6-enemy token test); T25 pilot boss (Great Root Mother framework — mechanics placeholder, MEAD P4). |
| TDD requirements | `TDD-Unit.AI.TokenPolicy/PhaseSelectorWeights`, `TDD-Functional.AI.AggroOnSight/TokenLimitsSimultaneousAttackers` (6 enemies, 60 s concurrent measurement) + scenario battery (QUALITY_PLAN §5). |
| Integration | Attacks emit via S07; telegraphs consume C-05 contract (re-enters here, D-02); narrative reads aggro state for quest flags. |
| Performance | AI ≤ 2.0 ms game thread (MEAD §15.2); ≤ 14 AI agents (B-12); Mass only for tiers 4–5. |
| Acceptance criteria | MEAD P4 exit: 3 archetypes distinct; token caps hold; pilot boss 3 phases, deterministic transitions, seeded selector tests pass; 8-enemy encounter 60 fps (on reference HW when available, else Mac with note). |
| Completion evidence | Named suites + encounter capture + ledger. |

## S09 Boss system (M4–M7)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` declarative phase graph schema (ADR-0107). Q-14 open (mechanics). Pilot = Great Root Mother (placeholder mechanics). |
| Intended behaviour | Seven named bosses as data (phase graphs, transitions: PoiseBreak/HealthPct/ElapsedSec/Distance/PlayerAbility/MemoryFound/Event), one controller. |
| Required functionality | Phase graph CSV/JSON → data asset importer; arena bounds; phase presentation (telegraphs via C-05 when active). |
| Dependencies | S08; CD ratification of per-boss mechanics (Q-14) for final content. |
| Architecture | ADR-0107 (authoritative). |
| Implementation tasks | T26 graph importer + validator; T27 pilot boss full loop; T28 per-chapter boss content (M7, content-gated). |
| TDD requirements | Seeded phase-selector tests; pilot boss gauntlet (`TDD-Gauntlet.*` at M8). |
| Integration | Narrative (MemoryFound transitions), checkpoints (boss arenas), audio/VFX per phase. |
| Performance | Boss arena = the reference scene (MEAD §15.3: 8 enemies + 4 VFX layers @ 60 fps). |
| Acceptance criteria | Per-boss: all phases reachable in all orders the graph allows; transitions deterministic; arena perf gate. |
| Completion evidence | Seeded tests + gauntlet + CD design sign-off on final mechanics. |

## S10 World streaming & environment physics (M2/M5)

| Field | Content |
|---|---|
| Current state | None in the canonical project. `[ACCEPTED]` budgets: B-12 (≤ 12 resident locations, ≤ 20 scenes, ≤ 14 AI, ≤ 8 s stream-in — unmeasured). |
| Intended behaviour | Real-scale chapters stream without holes; environment physics stable and bounded. |
| Required functionality | World Partition + data layers (time/weather per MEAD §6.2); PCG-seeded scatter (TR-02); Chaos breakables/fallables with per-scene physics budgets; navigation volumes (MEAD §6.4). |
| Dependencies | M2 forest slice as the first WP map; reference PC for final streaming sign-off. |
| Architecture | MEAD §6 (authoritative) + TR-09. |
| Implementation tasks | T29 WP setup on the forest slice; T30 data-layer time/weather; T31 physics budgets + scenario tests (QUALITY_PLAN §3); T32 navigation bake pipeline. |
| TDD requirements | `TDD-Functional.World.*` (encounter completes, checkpoint restores) + streaming budget measurements (closes B-12) + hitch counter (≤ 1 × > 50 ms per 10 min, MEAD §15.3). |
| Integration | Checkpoints ↔ persistence S21; encounters ↔ S08; cinematics ↔ streaming-ready tests (MEAD §14.2). |
| Performance | MEAD §15.3 scene budgets (10 M visible Nanite tris in combat, 3,000 non-Nanite draws, 60k HISM foliage, 8 GB VRAM, 10 GB RAM). |
| Acceptance criteria | Chapter 1 blockout traversable end-to-end, streaming never exposes a hole (MEAD P5 exit). |
| Completion evidence | Measured streaming report + traversal gauntlet + ledger. |

## S11 NPC population (M4/M7)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` five-tier model (WORLD_ARCHITECTURE §5): TIER 1 scripted-interactive … TIER 5 background-only; TR-1…TR-5 traceability rules; Ch. 1 data: 29 scenes exact head-count (B-06 residual = provenance only). |
| Intended behaviour | Ambient populations that are traceable to the register, budget-capped, and never double-counted. |
| Required functionality | Tier data model (register → tier → named actor / Mass / scripted / background-only), Mass setup for tiers 4–5, routine data (per-scene routine lines), canon guards. |
| Dependencies | S10 (streaming), register data (in-repo evidence JSONs). |
| Architecture | WORLD_ARCHITECTURE §5 + §11 testing strategy (authoritative). |
| Implementation tasks | T33 tier data model + register parser tests (mirror the Agent 2 fixtures); T34 Mass crowd setup (budget); T35 per-chapter population (M7, data-driven from register). |
| TDD requirements | Population counts assert against register (reproducible mirror, TR-3); anti-double-count check (TR-2). |
| Integration | Narrative reads NPC state for quest triggers; AI budget shares the 14-agent cap. |
| Performance | Crowd within AI budget; Mass ticks outside the 1.5 ms player+combat line. |
| Acceptance criteria | Ch. 1 population exactly matches register (verified_against_register per TR-4); zero double-counts. |
| Completion evidence | Count reconciliation report (Agent 2 format) + ledger. |

## S12 Interaction & world objects (M2/M5)

| Field | Content |
|---|---|
| Current state | M1 first-playable gate includes one interaction volume (M1-P5). `[ACCEPTED]` framework = MEAD §4.5 `ITDDInteractable`. |
| Intended behaviour | Contextual, localisable interactions: memory anchor, door, lever, dialogue partner, pickup, checkpoint shrine, lore object; hold variants; requirements via tags. |
| Required functionality | Core interface + focus resolution (nearest valid in forward cone, scored) + prompt UI hook + `FTDDInteractionRequirements`. |
| Dependencies | S02 (contract), S17 (prompt UI at M7; log-only before). |
| Architecture | MEAD §4.5 (authoritative). |
| Implementation tasks | T36 core interface + smoke interactable (M1-P5); T37 focus resolution; T38 full object set (M5/M7 per content). |
| TDD requirements | `TDD-Functional.Narrative.InteractionPromptAppears` (MEAD §14.2); M1 `TDD.Movement.InteractSmoke`. |
| Integration | Quests (S13), save (S21), audio (S16). |
| Performance | Focus resolution ≤ 0.1 ms/frame. |
| Acceptance criteria | M1-P5 at M1; full object set at M5 (each with prompt + hold + cancel tested). |
| Completion evidence | Named tests + object inventory table in the ledger. |

## S13 Narrative, quests, memories, endings (M6/M7)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` framework: MEAD §9 (flags/counters/conditions, quest system, seven memories OAD-32, endings resolver, codex, cultural integrity mechanism §9.8). ADR-0108 memory fragment state machines. Content open (Q-15/16). |
| Intended behaviour | Deterministic narrative state; six ending cases by truth table; memories persist through death/reload; cultural sign-off hooks enforced. |
| Required functionality | `UTDDNarrativeSubsystem` (flags/counters/conditions), quest data (CSV/JSON → assets), memory fragment FSMs (ADR-0108), ending resolver, journal/codex hooks, cultural status validator (D-25/TR-17). |
| Dependencies | S12 (anchors), S21 (save), CD content decisions. |
| Architecture | MEAD §9 + ADR-0108 (authoritative). |
| Implementation tasks | T39 flags/conditions pure core (`TDD-Unit.Narrative.ConditionEval`); T40 ending resolver (truth table incl. "truth known does not absolve" — MEAD §14.2); T41 memory FSM + counting (`TDD-Unit.Narrative.MemoryCounting`); T42 quest flow (`TDD-Unit.Narrative.QuestFlow`); T43 content (M7, CD-gated). |
| TDD requirements | All `TDD-Unit.Narrative.*` + `TDD-Functional.Narrative.MemoryFragmentDiscovered` (MEAD §14.2). |
| Integration | World events (S10), combat events (S06/07), UI (S17). |
| Performance | Narrative tick ≤ 0.5 ms (inside world/narrative 1.0 ms line). |
| Acceptance criteria | MEAD P6 exit: six endings resolve correctly; memories persist through death+reload; two-version save migration. |
| Completion evidence | Truth-table suite + soak test + ledger. |

## S14 Cinematics (M6/M7)

| Field | Content |
|---|---|
| Current state | None. `[ACCEPTED]` rules: M1 spec (cinematic = forced state, capsule frozen, no positional fallback, 0.4 s restore) + MEAD §14.2 tests. |
| Intended behaviour | Sequencer-driven cinematics that never corrupt gameplay state; skippable; streaming-ready. |
| Required functionality | Cinematic subsystem (take view target, suspend rig, restore), skip handling, QTE prohibition (Q-12 default: none), streaming preloads. |
| Dependencies | S05 camera contract, S10 streaming, S13 (ending sequences at content time). |
| Architecture | M1 spec §3.2 (Cinematic row) + MEAD (authoritative). |
| Implementation tasks | T44 subsystem + skip test; T45 streaming-ready test; T46 content (M7, CD-gated). |
| TDD requirements | `TDD-Functional.Cinematic.SkipLeavesStateConsistent/StreamingReadyForEveryShot` (MEAD §14.2). |
| Integration | Camera, save (mid-cinematic save policy), audio. |
| Performance | Zero visible pop in shots (MEAD §15.3: sublevel/cinematic stream ≤ 2 s). |
| Acceptance criteria | Both named tests + E6 cinematic-abort case green (no capsule drop). |
| Completion evidence | Named tests + recorded skip scenario + ledger. |

## S15 Build, packaging, release engineering (M0→M10)

| Field | Content |
|---|---|
| Current state | M0 build loop verified; packaging NOT RUN; no CI; no LFS. |
| Intended behaviour | Reproducible builds from tagged commits; one-command Mac build+test+package; versioned installers; update strategy. |
| Required functionality | Packaging scripts (Mac now; Windows CI on the reference PC from W2 — Day-0 order, TR-18); versioning scheme; build metadata in binary; crash/telemetry decision (Q-22); platform store requirements (Phase 6). |
| Dependencies | Reference PC (Windows packaging); store accounts (M10). |
| Architecture | TR-15 decisions. |
| Implementation tasks | T01/T02 (above) + T47 versioning + T48 Windows build bring-up (M6) + T49 release packaging pipeline (M10). |
| TDD requirements | Package smoke gauntlet per platform; build-reproducibility check (two clean builds, same commit → same binary hash or explained delta). |
| Integration | Every milestone's Gate D evidence. |
| Performance | Package size/time tracked per release (MEAD-style recording). |
| Acceptance criteria | RELEASE_READINESS_PLAN §5 gates 1, 8, 9. |
| Completion evidence | Archived package logs + clean-machine install test. |

## S16 Audio (M6/M7)

| Field | Content |
|---|---|
| Current state | None. `[ACCEPTED]` ADR-0009 (MetaSounds-only, `ITDDAudioService`), MEAD §11 structure + feedback budget §11.3. Drive `11_AUDIO_AND_MUSIC` folder empty (content open). |
| Intended behaviour | Adaptive environmental + combat audio; every gameplay feedback complete (sound is part of the feedback bundle, not an afterthought). |
| Required functionality | Submix hierarchy, Sound Concurrency, Quartz rhythmic events, feedback audio mapped 1:1 to combat/world/UI events, placeholder audio labelled until content. |
| Dependencies | S06/S07/S12 event hooks (exist by M4); content (M7+). |
| Architecture | ADR-0009 + MEAD §11 (authoritative). |
| Implementation tasks | T47a service + submixes; T48a combat feedback set (vs training room); T49a environmental beds (vs forest slice); T50a content (CD-gated). |
| TDD requirements | Feedback-completeness audit: every hit/dodge/stagger/death/interaction emits its mapped cue (automation: assert audio events fired, not heard); no pop/click in 20-min soak (Phase 6). |
| Integration | Event-driven only; no audio-owned gameplay state. |
| Performance | Audio inside the frame budget; concurrency caps per MEAD §11.3. |
| Acceptance criteria | MEAD P6 exit (menu loop with audio) + Phase 6A full validation row (audio). |
| Completion evidence | Event-mapping table + soak log + CD audio sign-off. |

## S17 UI/UX (M6)

| Field | Content |
|---|---|
| Current state | None. `[ACCEPTED]` MEAD §12 (localisation, accessibility baseline) + M1 overlay precedent. |
| Intended behaviour | Gamepad+mouse+keyboard parity, live rebinding, accessible, localisable. |
| Required functionality | UMG framework (HUD, pause, map, settings/rebinding, codex, checkpoint screen), String Tables, accessibility options (shake scale, motion blur, FOV slider, camera-assist — MEAD §4.3/§12), metrics/debug overlay (dev). |
| Dependencies | S03 events, S13 (codex), S05 (camera options). |
| Architecture | MEAD §12 (authoritative). |
| Implementation tasks | T51 framework + HUD; T52 settings/rebinding loop (gamepad-verified); T53 codex/journal UI; T54 pseudo-loc build test. |
| TDD requirements | Rebind round-trip automation; pseudo-loc build runs; all screens reachable by all three input devices (MEAD P6 exit). |
| Integration | Every system's debug/feedback surfaces route through the overlay. |
| Performance | UI ≤ 0.3 ms GPU (MEAD §15.2). |
| Acceptance criteria | MEAD P6 exit: full menu/settings/rebinding loop with gamepad; pseudo-loc passes. |
| Completion evidence | Named tests + screen inventory + accessibility check (Q-10). |

## S18 Progression & chapter flow (M6/M7)

| Field | Content |
|---|---|
| Current state | None. `[ACCEPTED]` MEAD §4.6 (game flow/states), §9.1 design rule (content-agnostic framework), Q-08 default (hooks, no economy/tree), Q-21 (chapter select/NG+ supported not exposed). |
| Intended behaviour | Chapter-gated progression with valid config to ship with none; flow system owns respawn (fell-out-of-world, death), transitions, loading. |
| Required functionality | Flow subsystem (chapter transitions, loading screen + failure path), progression hooks (data), checkpoint system integration. |
| Dependencies | S10 (streaming), S21 (save), S13 (gating conditions). |
| Architecture | MEAD §4.6/§9 (authoritative). |
| Implementation tasks | T55 flow subsystem + chapter transition test; T56 progression data model; T57 per-chapter wiring (M7). |
| TDD requirements | Transition gauntlet (start chapter → encounter → memory → checkpoint → transition, MEAD T3 tier); respawn tests (fell-out-of-world path from S04). |
| Integration | The seam between world content and player session. |
| Performance | Chapter load ≤ 15 s cold / ≤ 5 s warm (MEAD §15.3). |
| Acceptance criteria | MEAD P5/P6 exits (transition works with loading + failure path). |
| Completion evidence | Gauntlet + load-time measurements + ledger. |

## S19 Rendering, VFX & environment visual quality (M5→M8)

| Field | Content |
|---|---|
| Current state | None. Stack decided (TR-01/02: Lumen HWRT + Nanite + VSM + WP on DX12/PS5; Mac at beta level for look-dev). Budgets = MEAD §15.2/15.3. |
| Intended behaviour | Approved-board-faithful visuals at 60 fps on min-spec; final sign-off on reference HW. |
| Required functionality | Lighting look-dev per chapter (vs approved boards), material library (classic PBR, TR-02), PCG scatter (seeded), Niagara VFX set with per-emitter budgets, post-process chain (data), atmosphere (fog/exposure per board), character rendering (groom/costume at content time). |
| Dependencies | Reference PC (sign-off); approved art content; M5 slice as the proving ground. |
| Architecture | TR-01/TR-02 decisions + MEAD §15 budgets. |
| Implementation tasks | T58 lighting pipeline + first look-dev (forest slice); T59 material library + PBR standards; T60 VFX set (combat + environment); T61 per-chapter lighting (M7 waves). |
| TDD requirements | Controlled screenshot A/B vs approved boards (QUALITY_PLAN §1); `TDD-Perf.ReferenceScene.CH01_Encounter` budget gate; hitch/pop-in counters. |
| Integration | Everything visual; budgets law from M5. |
| Performance | Full MEAD §15.2/15.3 table (16.67 ms frame; 10 M Nanite tris; 8 GB VRAM; 0 packaged shader stutter). |
| Acceptance criteria | QUALITY_PLAN §1 gates + MEAD P7 per-chapter perf gate. |
| Completion evidence | Archived captures (reference HW) + budget reports + CD visual sign-off per chapter. |

## S20 Character art & animation pipeline (parallel from M2)

| Field | Content |
|---|---|
| Current state | Adanna technical proxy GLB (labelled interim, D-14); mannequin path accepted for M1; identity locks in M1 art spec; ADR-0005 provider interface. |
| Intended behaviour | Approved identity → production character → animation corpus (locomotion, combat, reactions, traversal) → optional MM upgrade (TR-03). |
| Required functionality | GLB exchange standard (TR-17), Control Rig retarget, foot IK, URO/animation LODs (MEAD §8.4), content pipeline staffing (Q-18 — OWNER DECISION), canon/cultural compliance. |
| Dependencies | **Content production capacity (the dominant project cost)**; Adanna creative approval (turnarounds unapproved today). |
| Architecture | ADR-0005 + MEAD §8 + M1 art spec (authoritative). |
| Implementation tasks | T61a import pipeline (proxy → mannequin → production, same code path); T62a animation content (per milestone: M1 mannequin clips → M3 combat set → M7 full); T63a MM spike (M3 entry, RG-03). |
| TDD requirements | Provider switch test (ADR-0005: HUD reports active provider); foot-slide ≤ 5 cm lab gate (MEAD P1 exit); clip inventory vs corpus plan. |
| Integration | Character code is content-agnostic by contract — swaps never touch gameplay code. |
| Performance | Animation ≤ 1.5 ms (MEAD §15.2); animation memory budget tracked. |
| Acceptance criteria | MEAD P3 exit (12+ attack/reaction clips, no animation-pop on cancels) + QUALITY_PLAN §2 gates. |
| Completion evidence | Clip inventory + lab metrics + CD sign-off per set. |

## S21 Save & persistence (contracts M0; hardening M6; soak M9)

| Field | Content |
|---|---|
| Current state | `[ACCEPTED]` ADR-0007 (USaveGame, `FTDDSaveHeader`, `ITDDSaveProvider`, migration chain, atomic write tmp→verify→rotate, slots: Auto×2/Checkpoint×1/Manual×3; memory discovery writes immediately). No code. |
| Intended behaviour | Corruption-safe, migration-safe, cross-session-identical persistence. |
| Required functionality | `UTDDPersistenceSubsystem`, per-system save providers (quest/world/memory/camera), checksum validation, `.bak` rotation, migration tests. |
| Dependencies | S02 (contract) — everything else parallel. |
| Architecture | ADR-0007 (authoritative). |
| Implementation tasks | T64 subsystem + round-trip (`TDD-Unit.Persistence.RoundTrip` — byte-identical assert); T65 atomic-write-interrupt test; T66 migration across 2 schema versions; T67 per-system providers (M6/M7); T68 soak (M9: 100 save/load cycles). |
| TDD requirements | All `TDD-Unit.Persistence.*` (MEAD §14.2) + 100-cycle soak with checksum comparison. |
| Integration | Every persisting system implements `ITDDSaveProvider` — no direct file IO elsewhere. |
| Performance | Save ≤ 2 s; load ≤ 3 s (proposed budget — record in ledger at implementation). |
| Acceptance criteria | MEAD P6 exit (migration across two versions) + Phase 6A row (save/load verified). |
| Completion evidence | Named suites + soak report. |

## S22 Accessibility & platform compatibility (M6/M9)

| Field | Content |
|---|---|
| Current state | Q-10 default = built as requirement; MEAD §12 baseline; AC-27 device parity in M1. |
| Intended behaviour | All systems usable by mouse, keyboard and gamepad; accessibility options effective; platform-specific requirements met (Windows primary; PS5 if D-16; Mac demo). |
| Required functionality | Accessibility options set (camera shake scale, motion blur, FOV, colourblind-friendly UI option), input parity matrix, platform compliance checklists. |
| Dependencies | S17; store requirements at M10. |
| Architecture | MEAD §12 (authoritative) + Phase 6 checklists. |
| Implementation tasks | T69 options implementation; T70 parity matrix automation (every action bound on all devices); T71 platform compliance (M10). |
| TDD requirements | Parity automation (AC-27 extended); options persistence through save. |
| Integration | Cross-cutting; audited at every phase gate from M6. |
| Performance | Options must not breach frame budget (measured). |
| Acceptance criteria | Phase 6A row (accessibility/platform) + Q-10 sign-off. |
| Completion evidence | Parity report + audit form. |

## S23 Performance & optimization (continuous from M1; formal M8)

| Field | Content |
|---|---|
| Current state | Budgets accepted (MEAD §15). AC-28 in M1. No captures yet. |
| Intended behaviour | Every phase gate runs the reference scene; regressions block gates; zero optimization claim without profiling evidence. |
| Required functionality | `TDD-Perf.ReferenceScene.CH01_Encounter` (fixed path/spawns/VFX), Insights workflow, budget dashboards per system, hitch/pop-in/shader-stutter counters, memory reports. |
| Dependencies | Reference PC (ordered Day 0; calibrated W2; sign-off authority from W5 look-dev / W7 baseline — TR-18); Mac captures for dev-loop regressions (labelled `DEV-HW`). |
| Architecture | TR-13 + MEAD §15 (authoritative). |
| Implementation tasks | T72 reference scene + capture automation; T73 per-system scope instrumentation (Insights scopes per MEAD §15.2 buckets); T74 regression rules in the gate process; T75 optimization passes (M8, evidence-per-fix). |
| TDD requirements | `TDD-Perf.*` gauntlet at every gate; regression rule: > 5 % frame-time or > 100 MB VRAM blocks the gate (MEAD §15.4). |
| Integration | All systems carry their budget line from design time. |
| Performance | The whole MEAD §15.2/15.3 table. |
| Acceptance criteria | Phase 6C: frame targets, budgets, memory, loading, streaming, shader behaviour, sustained stability — all measured on target hardware. |
| Completion evidence | Archived `.utrace` + CSV per gate; final perf report with the reference machine named. |

## S24 Quality & release readiness (Phase 6)

See RELEASE_READINESS_PLAN.md in full. Summary: full-game validation matrix; eight QA disciplines; defect register (severity/steps/owner/resolution evidence); 11 release gates; final release-readiness report with actual evidence.

---

## Inventory cross-check (accepted vs new)

- **Accepted specifications carried verbatim:** M1 spec v1.4 (S03/S04/S05 + ACs), ADR-0003/0004/0005/0006/0007/0009/0013 (S02/S06/S07/S08/S20/S16/S15), ADR-0101/0104/0107/0108 (S01/S15/S08/S13), MEAD §4–§15 (S05–S23), WORLD_ARCHITECTURE (S11/S10), C-05 design record (S08 telegraphs, parked).
- **New recommendations (ratified by D-19…D-25 in TRR or via ADR at implementation):** rendering stack usage on Metal (TR-01), PCG scatter (TR-02), Mover rejection (TR-03), in-game menus (TR-12), reference-scene regression rule operationalization (TR-13), canonical status validators (TR-17), GLB exchange standard (TR-17), build entry points (TR-15), content-agnostic pipeline (TR-17).
- **Deliberately NOT in scope:** multiplayer (ADR-0011), QTEs (Q-12 default), aim/thrown weapons (MEAD §4.2 "not in baseline"), economy/currency/skill tree (Q-08 default).
