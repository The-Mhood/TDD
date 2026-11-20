# Quality Engineering Plan

**Document ID:** TDD-PLAN-QUAL-001 · **Version:** 1.1 · **Date:** 2026-11-20
**v1.1 (review pass):** added claim-classification policy (item 6) per the owner's technical-claims audit; C-1 and §4 phrasing clarified — reproducibility is a *verified design property*, not an engine guarantee (TR-19 T2); all requirement rows already carry a measurement method (verified in the audit — TR-19).
**Mandate (owner, Phase 4):** measurable quality requirements per system with an explicit evaluation method; dedicated quality gates (screenshots, transition inspection, repro scenarios, deterministic combat cases, multi-scenario AI); no placeholder asset may claim production readiness; quality gaps tracked by player impact and technical risk.
**Companions:** MILESTONE_ACCEPTANCE_CRITERIA.md (per-milestone ACs) · RELEASE_READINESS_PLAN.md (Phase 6 execution) · TR-19 (claims audit + conventions).

## 1. Quality policy (binding)

1. **Measured, not claimed.** Every quality statement in any report must cite: the measurement method, the run (evidence path), and the reference (budget/AC). "Looks good" is a claim and is not recorded as a result.
2. **Gates are pass/fail with evidence.** A quality gate is a named procedure with inputs, a pass criterion, and an archived output. Gates block milestones (MAC) and merges (Roadmap §6) as specified.
3. **Placeholder discipline.** Interim assets (mannequin, labelled proxies, placeholder VFX/audio) are allowed *in development* but are (a) labelled in-tree (filename prefix `WIP_` / ledger tag `interim`), (b) never cited as evidence for a production-readiness claim, and (c) tracked in the quality gap register (§8) with a named replacement task. A milestone that exits on interim assets states so explicitly in the progress report.
4. **Reference hardware discipline.** Visual and performance sign-off requires the reference PC (D-12). Mac (Metal) captures are labelled `DEV-HW` and are look-development evidence only (D-19).
5. **No silent regression.** Any gate that previously passed and now fails is a P1 defect until triaged (not a "re-baseline").
6. **Claim classification (TR-19, binding).** Statements about engine behaviour are classed [DS-G] design guarantee (enforced in code + tested) / [BUD] budget (target until measured) / [EN-V] engine behaviour (verify by named test before citing as fact) / [ST] status claim (dated citation) / [UNV] unverified (no claim permitted). An [UNV] item may never appear in a report as fact; it appears as "to be verified by \<test\>". The audit of the existing planning set is TR-19; the conventions apply to all future documents and reports.

## 2. Domain quality requirements & evaluation methods

### 2.1 Graphics (rendering, Lumen, Nanite, VFX)

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| G-1 | 60 fps sustained (1% low ≥ 50) in the reference scene and each chapter reference encounter | `TDD-Perf.ReferenceScene` .utrace + CSV on reference HW; frame histogram | M5, every chapter gate, M8 |
| G-2 | Frame budget split holds: game thread ≤ 6.0 ms, GPU ≤ 16.0 ms (MEAD §15.2) | Insights CPU/GPU comparison scopes | Same as G-1 |
| G-3 | ≤ 10 M visible Nanite triangles in combat scenes; ≤ 3,000 non-Nanite draw calls; ≤ 60k HISM foliage | Draw call / triangle counters from the reference scene (Stat + .utrace) | M5 + chapter gates |
| G-4 | VRAM ≤ 8 GB, RAM ≤ 10 GB, no growth > 100 MB over 30 min | Memory reports (platform-specific) at scene start and +30 min | M5, M8 soak |
| G-5 | Lighting fidelity vs approved boards: 10 fixed capture positions per location, colour/exposure within tolerance of the approved board (CD-judged, A/B side-by-side) | Controlled screenshot set: fixed camera transforms, same exposure settings, both platforms captured; CD signs each set | M5 slice + each chapter gate |
| G-6 | No visible lighting pop / material pop / shadow pop on streaming or state change | 20-min scripted traversal with camera recording; pop-in counter + manual review | M5, M8 |
| G-7 | Zero packaged shader compile stutter in the release build (all shaders pre-compiled at packaging) | Clean-machine install → full 30-min play → zero shader compile events in log | M8, M10 |
| G-8 | VFX: every gameplay event has its effect (feedback map 100%); per-emitter particle count within budget; no > 1 ms emitter cost | VFX inventory vs event list; Niagara stats + frame compare with effect off | M3 (combat set), M5 (full set) |
| G-9 | Visual parity Windows vs Mac documented (Metal = dev level, D-19): identical capture set on both, delta notes | Dual capture sets + delta table in ledger | M5, chapter gates (Windows is sign-off) |
| G-10 | Hitches: > 50 ms frames ≤ 1 per 10 min in gameplay | Hitch counter in .utrace over 10-min windows | M8 soak + chapter gates |

### 2.2 Animation (locomotion, combat, traversal)

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| A-1 | Foot-slide ≤ 5 cm on the lab set (walk/run/jump/sprint/dodge) | Foot-locator delta vs ground over 30 s lab run, CSV | M1 (mannequin), M3 (combat set), M5 (production) |
| A-2 | No animation pop on state cancel (light chain cancels, dodge-cancel, parry-cancel): position delta on cancel ≤ 10 cm, rotation ≤ 15° | Cancel-case battery: scripted cancels, joint-position delta measured pre/post | M3 |
| A-3 | All 196 state transitions produce a valid animation (no T-pose / no default-pose flash) | State-transition sweep: enter each transition, capture 5 frames post-transition, skeleton pose check | M1 (loco), M3 (combat) |
| A-4 | Traversal motion warping: endpoint pose matches exit transform (position ≤ 5 cm, orientation ≤ 5°) at completion | Warp-convergence test per traversal type (E1–E7) | M2 |
| A-5 | Animation frame cost ≤ 1.5 ms (MEAD §15.2) | Insights scope | M3, M8 |
| A-6 | Animation memory: clip + pose-budget tracked; no growth across a chapter | Memory report | M7 waves, M8 |
| A-7 | Production character: identity locks verified (25, LEFT-temple cuffs/coral beads, LEFT-cheek scar, no gold/mirroring); LOD1/LOD2/URP pop ≤ 5° silhouette diff | Turnaround capture + joint-lock validator + LOD compare | M5 (technical validation, MEAD §8.5) |

### 2.3 Physics & collision (traversal, environment)

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| P-1 | No floating capsule in any state (movement, traversal, combat, death): floor-trace ≤ 2 cm or intentional airborne state | Floor-trace assertion in every state exit (M1-S2 guard) + 100-run sweep | M1 → all gates (continuous) |
| P-2 | No teleport-into-geometry: post-resolution position never inside solid (trace check) | Same assertion suite + random-placement fuzz (1000 placements) | M1, M2, M8 |
| P-3 | Slope behaviour per spec: 15/30/45° climbs ok, 50° blocked; 40° slope ok, 50° blocked — measured angles, not assumed | Slope-fixture gauntlet (each angle × both directions) | M1 (AC-05…09) |
| P-4 | Step-up / ledge / gap edge cases: exact spec §3.3 values, no oscillation (bounce ≤ 1 frame) | Edge-case suite | M1 |
| P-5 | Traversal E1–E7: restoration exactly once; hold ≤ 5 cm; resolution ≤ 1 frame; lethal+staggering → Dead (Dead > Stagger); cinematic → no positional fallback | TraversalAbortPaths + TraversalExitRevalidation suites (named in spec §5) | M2 (MAC M2.1–M2.5) |
| P-6 | Environment physics bounded: breakables/fallables within per-scene physics budget; no runaway velocity (cap enforcement tested) | Physics scenario battery (below, §6) | M5, chapter gates |
| P-7 | Checkpoint restore: world object states (doors, levers, destroyed objects) byte-identical after restore | Restore-compare test (state dump pre-death vs post-respawn) | M6, chapter gates |

### 2.4 Combat

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| C-1 | Deterministic combat cases: 10-case seeded battery (exact input timestamps → exact outcome log: hits landed, damage values, posture, staggers, deaths); outcome logs identical across 3 runs *within the same platform/build/test conditions* — a verified design property (no-async gameplay paths, seeded RNG, fixed test frame clock), **not** an engine guarantee; cross-platform determinism is not claimed (TR-19 T2); any mismatch = P1 root-cause, never re-baseline | Battery CSV + 3-run diff (see §4 for the 10 cases) | M3 (MAC M3.5), M8 |
| C-2 | No double-hits: every attack lands each hit exactly once (10-hit-per-attack gauntlet vs dummy) | Hit-registration log vs expected | M3 (MAC M3.2) |
| C-3 | Timing windows exact to spec: light chain cancel from frame after active, chain window 0.15–0.45 s; guard-ready 0.08 s; parry window 0.15 s; i-frames 0.10–0.45 s (AC verified 0.11–0.44) | Frame-timestamped input sequences, outcome asserted | M3 (AC-verified values) |
| C-4 | Damage taxonomy 100%: 5 categories × 8 defender states (idle/run/dodge-active/dodge-iframe/block/parry/stagger/dead) all resolve per M1 spec §3.2.1 | Taxonomy matrix automation (all 40 cells) | M3 (MAC M3.4) |
| C-5 | Parry → attacker stagger; block → posture damage (not health); posture break → Stagger state (same-frame promotion verified) | Scripted parry/block cases with frame-precise outcome assertions | M3 |
| C-6 | Feedback completeness: 100% of hit events → VFX + audio + camera + hitstop (map audit, zero gaps) | Event-fire automation + audit table | M3 (MAC M3.3) |
| C-7 | Readability: every attack has a telegraph visible ≥ the C-05 contract duration before the active window (re-enters at M3, D-02) | Telegraph timing assertion per attack | M3, M4 (enemies) |
| C-8 | Combat feel review (human): owner plays the training room; feel issues logged as defects with reproduction steps (not opinions without repro) | Session with recording + defect entries | M3 exit, M8 |

### 2.5 AI & world

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| I-1 | Concurrent-attacker caps: 6 enemies / 60 s → concurrent attacks ≤ 1 (measured) | TokenLimitsSimultaneousAttackers suite × 3 runs | M4 (MAC M4.2) |
| I-2 | Multi-scenario AI battery: 8 scenarios (ambush, flanking, player death mid-aggro, boss arena entry, checkpoint respawn during aggro, 8-enemy room, cinematic during aggro, save during aggro) — each with an expected end state, asserted | Scenario CSV + end-state assertions (see §5) | M4 (MAC M4.6), M8 |
| I-3 | Determinism: seeded AI behaviour reproducible (same seed + inputs → same decisions log) | Seeded 1000-iteration decision-log compare | M4 |
| I-4 | Archetype distinction: per archetype, attack-style/spacing/reaction metrics within design envelope (measured from encounter logs) | Encounter log analysis per archetype | M4 (CD review) |
| I-5 | AI perf ≤ 2.0 ms (8 enemies); ≤ 14 active AI agents (B-12) | Insights scope + agent counter | M4, chapter gates |
| I-6 | No AI stuck states: 10-min free-play per archetype, zero stuck > 5 s (state-graph monitor) | Free-play soak with state monitor | M4, M8 |
| I-7 | Population exact against register (TR-3/4); zero double-counts (TR-2) | Count reconciliation report per chapter | M4 (model), chapter gates |
| I-8 | World streaming: no visible holes in a full traversal gauntlet; stream-in ≤ 8 s; hitches ≤ 1/10 min (B-12) | Gauntlet + streaming log | M2 (data), M5, chapter gates |
| I-9 | Navigation integrity: AI-reachable volume covers 100% of designated play areas; no unreachable-quest-object flags | Bake coverage test + designer walk-through | M2, chapter gates |

### 2.6 Audio

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| S-1 | Feedback map 100%: every mapped event fires its cue (automation asserts event fire, not hearing) | Event-fire report vs map | M6 (MAC M6.5) |
| S-2 | No pop/click in a 20-min soak (loop + stingers + adaptive transitions) | 20-min soak log (listener notes + waveform check of flagged moments) | M6, M9 |
| S-3 | Concurrency: no > N simultaneous cues (per MEAD §11.3 caps); ducking works (combat music under dialogue) | Concurrency counter in soak | M6 |
| S-4 | Spatial correctness: directional cues for 4 cardinal + 2 diagonal sources (spot check) | Manual spot check with recording | M9 |

### 2.7 UI / UX / accessibility

| # | Measurable requirement | Evaluation method | Gate / when |
|---|---|---|---|
| U-1 | All screens reachable on mouse + keyboard + gamepad (parity matrix 100%) | Parity automation (every action bound on every device) | M6 (MAC M6.8) |
| U-2 | Rebinding round-trip: rebind → save → load → works | Automation | M6 |
| U-3 | Accessibility options effective (shake scale, motion blur off, FOV range, camera assist) and persisted | Option tests + save check | M6 |
| U-4 | Localisation-safe: pseudo-loc build runs; no hard-coded strings in UI (String Table audit 100%) | Pseudo-loc build + string audit | M6 (MAC M6.6) |
| U-5 | UI GPU ≤ 0.3 ms (MEAD §15.2) | Insights scope | M8 |

## 3. Quality gate catalogue (dedicated gates, Phase 4)

| Gate | Type | Inputs | Pass criterion | Frequency |
|---|---|---|---|---|
| **QG-SHOT** | Controlled screenshot set | Fixed camera transforms + exposure settings per location (10 positions); reference HW | CD signs A/B vs approved boards (G-5) | M5 slice, each chapter gate, M8 |
| **QG-TRANS** | Transition inspection | Chapter/memory/cinematic transitions + save/load points | Zero pop, zero state corruption, ≤ 2 s stream, skip/restore consistent (G-6, M6.4, M7.c.5) | M5, M6, chapter gates, M8 |
| **QG-REPRO** | Repro scenario battery | Named scenarios with inputs + expected end state (combat, traversal, AI, save, physics — §4–§6) | 100% pass, 3-run determinism | M3, M4, every milestone gate, M8 |
| **QG-COMBAT** | Deterministic combat cases | 10-case seeded battery (C-1) | Byte-identical outcomes × 3 runs; taxonomy 100% (C-4) | M3, M8 |
| **QG-AI** | Multi-scenario AI | 8-scenario battery (I-2) | All end states match; caps hold (I-1); determinism (I-3) | M4, M8 |
| **QG-PHYS** | Physics scenario battery | §6 scenarios | No floating capsule, no runaway, bounded (P-1, P-2, P-6) | M2, M5, M8 |
| **QG-SOAK** | Stability soak | 2-h full-game play (scripted + free) on reference HW | Zero crashes, memory growth ≤ 100 MB, hitch budget (G-10, M8.3) | M8, M9 |
| **QG-PERF** | Performance budget gate | Reference scene + worst chapter | All MEAD §15 budgets met; regression rule (G-1…G-4) | Every milestone from M5, M8 final |
| **QG-FEEDBACK** | Feedback completeness | Event → cue map (combat/world/UI) | 100% mapped events fire (C-6, S-1, U audit) | M3, M6, chapter gates |
| **QG-CULTURAL** | Cultural/canon compliance | Consultant sign-offs, canon status validator | 100% sacred vocabulary signed; validator clean (M7.c.7) | Chapter gates (chapters with sacred content) |

## 4. Deterministic combat case battery (QG-COMBAT, 10 cases)

Seeded; exact input timestamps; outcome log = (event, frame, subject, value) tuples; 3-run identity within the same platform/build/test conditions required (reproducibility per C-1/TR-19 T2 — the battery *is* the verification; a failing run is a P1 defect, not a design change).

1. **L1-chain-full** — 4 light attacks from rest: chain window respected, cancel points exact.
2. **L1-cancel-heavy** — light-2 → heavy cancel: commit point respected, no cancel after commit.
3. **Parry-stagger** — attack telegraph → parry at window midpoint → attacker staggers (timing 0.15 s window verified at edge ±1 frame).
4. **Block-posture** — N blocked hits → posture damage accumulates → posture break → Stagger (same-frame promotion).
5. **Dodge-iframe** — attack active window vs dodge i-frames (0.11–0.44 s): no damage inside window, damage at window edges.
6. **Lethal-staggering** — lethal+staggering hit: Dead > Stagger (death wins, no stagger after death).
7. **Posture-promotion** — two non-staggering hits same frame, second breaks posture: exactly one Stagger entry (no double).
8. **Restoration-once** — traversal abort → damage during resolution: fallback → restoration → entry exactly once (spec §3.2.3).
9. **Cinematic-freeze** — damage during cinematic: capsule frozen, no positional fallback, state restored on exit.
10. **Hitstop-expiry** — hitstop bounded by data; expiry resumes simulation (no frame skip, no double-hit after expiry).

## 5. AI scenario battery (QG-AI, 8 scenarios)

Each: seeded start state + scripted player actions + expected end state (asserted, not observed).

1. **Ambush** — player enters 3-enemy room mid-combat: all 3 aggro, concurrent attacks ≤ 1.
2. **Flanking** — 4 enemies, 30 s: flanking positions form within design envelope; no overlap > 1 s.
3. **Player-death-mid-aggro** — player dies at 40 s: aggro resets per checkpoint policy on respawn; no enemies stuck in attack recovery.
4. **Boss-arena-entry** — Great Root Mother (pilot): entry telegraph → phase 1; arena bounds respected (no pathing outside).
5. **Checkpoint-respawn-during-aggro** — respawn 20 m from aggro group: enemies de-aggro / re-aggro per policy, no memory of pre-respawn positions.
6. **8-enemy-room** — 8 enemies 60 s: token caps hold, AI ≤ 2.0 ms, 60 fps (reference HW).
7. **Cinematic-during-aggro** — cinematic triggers mid-aggro: AI frozen correctly, resumes on exit, no desync.
8. **Save-during-aggro** — save at 30 s aggro, load: aggro state restored per policy, world state byte-identical.

## 6. Physics scenario battery (QG-PHYS, 8 scenarios)

1. **Fuzz-placement** — 1000 random placements: zero inside-solid post-resolution, zero floating.
2. **Slope-full** — every spec angle (15/30/45/50 climb, 40/50 slope) both directions: pass/block per spec, no oscillation.
3. **Ledge-marathon** — 50 consecutive ledge holds: hold stability ≤ 5 cm, no slip accumulation.
4. **Fall-chain** — 10 falls from increasing heights: landing recovery per spec; fall damage thresholds (if data says) exact.
5. **Breakable-cascade** — 20 breakables in cascade: no runaway velocity, physics budget held, no penetration of floor.
6. **Falling-object-on-player** — object strikes player mid-dodge: i-frames respected; mid-idle: damage exact.
7. **Checkpoint-restore** — destroy 5 objects → die → respawn: states identical (P-7).
8. **Traversal-kill-plane** — E-path with fall past kill plane: `FellOutOfWorld` flow, clean respawn, no crash.

## 7. Production-readiness definition (placeholder prohibition, Phase 4)

A system/location/character is **production-ready** only when:
1. All its interim assets are replaced (or a specific interim is owner-ratified as shippable with an ADR — none are proposed today).
2. Its domain quality rows (§2) have passed at the current milestone with reference-HW evidence where required.
3. The quality gap register (§8) has no open row with player-impact ≥ High for that scope.
4. CD sign-off is recorded (visual/animation/audio/narrative as applicable).

Any milestone progress report must state, per workstream: `production-ready` / `dev-quality (interim: <list>)` — never an unqualified "done" when interim assets remain.

## 8. Quality gap register (player impact × technical risk)

Maintained in the ledger (`QUALITY_LEDGER.md` → gaps section). Columns:

| Gap ID | System/location | Gap description | Player impact (H/M/L) | Technical risk (H/M/L) | Replacement task (WBS ID) | Owner | Status |
|---|---|---|---|---|---|---|---|

Scoring: **Player impact** = how a player experiences the gap (H = breaks the fantasy/gameplay, M = noticeable, L = invisible to casuals). **Technical risk** = probability/impact that the gap becomes a late-stage blocker (H = rework likely, M = contained, L = trivial swap).

**Seeding rows (2026-11-20):**
- GAP-01: Adanna character = mannequin/proxy — impact H, risk M — replacement M5-06 (CT) — OW/CD.
- GAP-02: All VFX/audio interim placeholders — impact M, risk L — M5-04, M6-03 — AG.
- GAP-03: Enemy archetypes = placeholders pending CD-3 — impact H, risk H (rework if ratification is late) — M4-09 — CD.
- GAP-04: Boss mechanics placeholder (Q-14) — impact H, risk M — M4-06 pilot → M7 — CD.
- GAP-05: No Windows hardware (dev-only Mac captures) — impact L (now), risk H (M5+) — M5-01 — OW.
- GAP-06: Cultural content pending consultant (CD-2) — impact H (if content built early), risk H — M7 waves — CD.
- GAP-07: Chapter environments blockout-only — impact H, risk M — M7 waves — CT.

## 9. Tools & capture discipline

- **Captures:** fixed camera transforms stored as data assets (reproducible); every capture set names: commit, machine (reference HW identity), platform, RHI, settings profile.
- **Trace:** `.utrace` archived per gate run (LFS); CSV summaries committed as text.
- **Videos:** only where a judgment is subjective (feel, pop-in) — archived with the gate record, with timestamps noted in the ledger.
- **Determinism:** all batteries seed explicitly; seeds recorded in the output CSV.
- **Ledger:** one row per gate run: gate ID, date, commit, machine, result, evidence paths, deltas vs previous run.
