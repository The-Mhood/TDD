# Release Readiness Plan (Phase 6)

**Document ID:** TDD-PLAN-RRP-001 · **Version:** 1.1 · **Date:** 2026-11-20
**v1.1 (review pass):** G-02 corrected — it referenced "11 M1 ACs"; the accepted M1 specification contains **31** ACs (AC-01…AC-31) and that is the correct traceability target; gates now explicitly evaluated against the owner-approved release scope (SA register, ROADMAP v2.0 §5).
**Mandate (owner, Phase 6):** full validation and QA with a defect register (severity, repro, ownership, resolution evidence); performance with profiling evidence only; commercial preparation (platforms, packaging, crash reporting, licensing, store assets); 11 release gates; a final release-readiness report containing actual evidence.
**Companions:** QUALITY_ENGINEERING_PLAN.md (gate definitions) · MILESTONE_ACCEPTANCE_CRITERIA.md M9/M10 (milestone-level ACs) · RISK_AND_BLOCKER_REGISTER.md.

## 1. Scope of "release-ready"

The Disobedient Daughter, single-player action-adventure:
- **Platforms:** Windows x64 (primary shipping target, D-04); macOS (demo-capable, dev-validated); PlayStation 5 **only if** D-16 is confirmed and Sony onboarding completes (else the PS5 option is formally retired by ADR at M8).
- **Content:** 8 chapters, 7 bosses, 6 endings, all memories, per the accepted design documents.
- **Quality bar:** every gate below passes with committed evidence. A gate that cannot produce evidence is FAILED, not waived.

## 2. Phase 6A — Full validation matrix

Executed at M9 (WBS M9-01). Each row: procedure, environment (reference HW, release build), evidence. 100% of rows executed with evidence linked is the exit condition (MAC M9.1).

| # | Validation area | Procedure | Evidence |
|---|---|---|---|
| V-01 | Movement (all 31 ACs re-run on the full game, not just test map) | 3 cold runs of the full TDD.Movement suite in-chapter | Bundles × 3 |
| V-02 | Traversal E1–E7 in real chapter geometry (not just blockout) | Traversal gauntlet on ch.1 + ch.4 + ch.8 geometry | Gauntlet reports |
| V-03 | Combat vs real enemies (not dummy): taxonomy, parry, block, stagger, death | QG-COMBAT battery + 30-min real combat | CSV + recording |
| V-04 | All 7 bosses: every phase graph path reachable, transitions deterministic | Per-boss gauntlet (all transition paths, seeded) | Gauntlet reports × 7 |
| V-05 | All 6 endings reachable & resolved correctly | Truth-table gauntlet (scripted flag states → ending) | 6 ending captures + state dumps |
| V-06 | All 7 memories discoverable, countable, persisting through death/reload | Memory gauntlet | State dumps + captures |
| V-07 | Save/load: 100 cycles across 10 chapter points (checksum-verified) + 2-version migration live | Soak report | M9-04 |
| V-08 | Cinematics: every shot streaming-ready; skip leaves state consistent | Cinematic gauntlet (all shots) | Gauntlet report |
| V-09 | Population: every chapter reconciled against register (TR-3/4), zero double-counts | Reconciliation reports × 8 | Reports |
| V-10 | Quests: every quest flow from trigger to resolution, flags verified | Quest gauntlet | State dumps |
| V-11 | World streaming: full-game traversal gauntlet start → ending, zero holes, hitch budget | Gauntlet + .utrace | Report |
| V-12 | Checkpoints: every checkpoint restores world state byte-identically | Restore-compare per checkpoint (sample: all ch.1, 3 per other chapter) | State dumps |
| V-13 | Input parity: all actions on all 3 devices, all screens | Parity automation + gamepad session | Report + recording |
| V-14 | Accessibility: all options functional end-to-end | Option tests in-game | Report |
| V-15 | Audio: feedback map 100% in final content; 20-min soak per chapter (sample 3) | Event-fire + soak logs | Logs |
| V-16 | Localisation pipeline: final strings, pseudo-loc sanity, no hard-coded strings | String audit + build | Report |
| V-17 | Fell-out-of-world / flow edge cases: kill plane, load failure, mid-transition crash-recovery | Fault-injection tests | Test reports |
| V-18 | Crash/telemetry per Q-22 decision: opt-in flow works or opt-out documented | Flow test / compliance note | Report |

## 3. Phase 6B — Eight QA disciplines & defect register

### 3.1 Disciplines (M9-02, each with its own scenario set + report)

1. **Gameplay QA** — movement/combat/traversal in real content; feel defects require repro steps (recording + inputs), not opinion.
2. **Camera QA** — all rigs (exploration/combat/lock-on/traversal/cinematic/death) through every transition; penetration/stability/displacement/recovery re-measured in-chapter (QG-SHOT camera positions).
3. **Animation QA** — cancel pops, foot-slide in real geometry, LOD transitions, ragdoll quality on real death cases; production character identity-lock verification (GAP-01 closure).
4. **Combat QA** — QG-COMBAT on real enemies; telegraph readability review (C-05); feedback completeness in final content (QG-FEEDBACK).
5. **AI QA** — QG-AI battery on final archetypes; 10-min free-play soaks per archetype (I-6); population behaviour.
6. **Save/Load QA** — 100-cycle soak; corruption recovery (atomic-write paths); migration; slot management (Auto×2/Checkpoint×1/Manual×3 per ADR-0007).
7. **Visual QA** — QG-SHOT per chapter vs approved boards; pop-in sweep; shader stutter (G-7); Windows sign-off + Mac delta.
8. **Audio QA** — S-1…S-4 on final content; adaptive music transitions; spatial spot checks.

### 3.2 Defect register (single register, ledger-linked)

Every defect from every discipline and every gate run goes in `docs/06_IMPLEMENTATION/DEFECT_REGISTER.md`:

| Field | Required |
|---|---|
| ID (`TDD-DEF-####`, monotonic) | yes |
| Severity (P0–P3, §4) + player impact (H/M/L) | yes |
| System / milestone / gate that found it | yes |
| Reproduction: commit, machine, build, inputs/timeline, expected vs actual | yes (no-repro defects are P3 max until reproducible) |
| Owner (WS + named) | yes |
| Status: OPEN → IN-PROGRESS → FIXED → VERIFIED / DEFERRED (owner-ratified, impact stated) / WONTFIX (owner-ratified, reason) | yes |
| Resolution evidence: fix commit + verification run (bundle) + re-test result | yes for FIXED/VERIFIED |

**Rules:** (a) a P0/P1 blocks M9 exit until FIXED+VERIFIED (Phase 5E: defects are not ignored); (b) DEFERRED is only by owner decision with recorded player impact; (c) re-opened defects increment a counter — 2 re-opens force root-cause review; (d) the register is the single defect source of truth — no side lists.

## 4. Severity definitions

| Sev | Definition | Example | SLA |
|---|---|---|---|
| P0 | Crash, data loss/save corruption, unfinishable game | save corruption on load | Block all merges; fix immediately |
| P1 | Core gameplay broken or major content missing/wrong | boss phase unreachable; a quest dead-ends | Block M9 exit |
| P2 | Noticeable quality defect, workaround exists | animation pop on one cancel; a VFX off-board | Fix or owner-defer with impact |
| P3 | Minor/polish | minor audio timing, cosmetic | Owner's call at M10 |

## 5. Phase 6C — Performance (profiling evidence only)

Owner rule: **no optimization or performance claim without profiling evidence.**

- **Instrumentation:** Insights scopes per MEAD §15.2 buckets on all major systems (M8-02); every .utrace archived (LFS) with the gate it feeds.
- **Baseline:** reference scene + worst chapter on reference HW (identity recorded in ledger) — the "before" for everything (M8-01).
- **Budgets (law, MEAD §15):** 60 fps / 1% low ≥ 50; game ≤ 6.0 ms; GPU ≤ 16.0 ms; ≤ 10 M visible Nanite tris; ≤ 3,000 non-Nanite draws; VRAM ≤ 8 GB; RAM ≤ 10 GB; hitches > 50 ms ≤ 1/10 min; chapter load ≤ 15 s cold / 5 s warm.
- **Per optimization:** commit → before/after .utrace + CSV delta → ledger row. Unmeasured "optimizations" are rejected at merge (M8.2).
- **Sign-off:** full budget table per platform in the final report, with the machine named. Min-spec check: the $600–1,200 DX12 reference (D-12) is the floor; anything below is documented as unsupported, not "maybe".

## 6. Phase 6D — Commercial preparation

| # | Item | Requirement | Evidence | Gate |
|---|---|---|---|---|
| D-1 | Store presence | Steam account + Direct fees (owner); page live or ready; screenshot set, icon, description, trailer cut | Store assets committed / store URL | G-10 |
| D-2 | Crash reporting | Q-22 decision (ADR): opt-in telemetry implemented + consent flow tested, or documented opt-out + store-compliance note | Implementation test / compliance note | G-10 |
| D-3 | Licensing audit | 100% of shipped content conforms to ADR-0104 (provenance recorded); engine/platform licensing (Epic, any third-party) verified; no unlicensed assets | Audit report (per-asset provenance list) | G-10 |
| D-4 | Age rating / store compliance | Self-certification materials prepared (violence, cultural content notes per CD sign-offs) | Rating questionnaire draft | G-10 |
| D-5 | Update/patch path | Versioning scheme + patch build demonstrated (M10-01 pipeline) | Patch build + apply test | G-09 |
| D-6 | Platform matrix final | Windows (primary) ✓; Mac (demo) ✓; PS5: D-16 confirmed + onboarding complete, or retired by ADR | Decision record + platform builds | G-09 |

## 7. The 11 release gates

All must pass with actual committed evidence. Waiver = owner-ratified ADR stating impact (none anticipated).

**Scope rule (accelerated model):** gates are evaluated against the **owner-approved release scope** — under the 4–8-week fast-track that is the ch. 1 release candidate (SA-1; ROADMAP v2.0 §5). Matrix rows, inventories and sign-offs (G-01, G-03, G-07, G-08) therefore cover shipped content only; each SA-approved scope adjustment is restated in the final report's "Known limitations" (§8.9) so the report never implies content that was not shipped. Post-RC chapters re-enter through the same gates per wave.

| Gate | Definition | Required evidence |
|---|---|---|
| **G-01** | **Full validation matrix 100% executed** (V-01…V-18), zero unexecuted rows | Matrix with 18/18 linked evidence paths |
| **G-02** | **All 31 M1 ACs (AC-01…AC-31, spec v1.4) still green** in the final build — full regression of the accepted baseline (spec v1.4 is the contract; traceability: M1 spec §5 ↔ MAC M1.32 row ↔ this gate) | Final-run bundles × 3 cold runs, 31/31 `TDD_RESULT` lines quoted |
| **G-03** | **Defect register closed to policy:** P0 = 0 open, P1 = 0 open, P2 ≤ 5 with owner-ratified deferrals (impact stated) | Register snapshot |
| **G-04** | **Save/load soak:** 100 cycles + migration + corruption recovery, zero corruption | Soak report |
| **G-05** | **Performance sign-off:** all MEAD §15 budgets met on reference HW in reference scene + every chapter reference encounter; 2-h soak clean | Per-chapter .utrace + CSV + soak log, machine named |
| **G-06** | **Stability:** full-game gauntlet start → all 6 endings × 3 unattended runs, zero crashes, zero softlocks | 18 gauntlet reports (6 endings × 3) |
| **G-07** | **Content completeness:** 8 chapters × 7 bosses × 6 endings × 7 memories — inventory 100% reconciled vs design docs; CD sign-off per chapter recorded | 8 chapter gate records + content inventories |
| **G-08** | **Visual sign-off:** QG-SHOT per chapter signed by CD; identity locks verified; no unlabelled interim asset in the shipped build | 8 signed capture sets + asset audit (zero `WIP_` in package) |
| **G-09** | **Platform builds:** all confirmed platforms packaged from a tagged commit; clean-machine install → launch → 30-min play per platform; update path demonstrated | Per-platform install/launch/play logs + patch test |
| **G-10** | **Commercial readiness:** D-1…D-6 complete (store, telemetry, licensing, rating, update path, platform matrix) | Six item evidence sets |
| **G-11** | **Final release-readiness report** (below) delivered and auditable: every claim carries an evidence path; no claim without evidence | The report itself + evidence path audit |

## 8. Final release-readiness report (structure)

`docs/06_IMPLEMENTATION/RELEASE_READINESS_REPORT_<date>.md`:

1. **Verdict** — READY / NOT READY (per gate) + the specific failing gates if any.
2. **Build identity** — commit, version, per-platform build IDs, reference machine identity.
3. **Gate table** — G-01…G-11, each: PASS/FAIL + evidence path(s).
4. **Validation summary** — matrix execution counts; suites × runs × platforms with pass/fail/skip (skips justified).
5. **Defect summary** — total opened/closed by severity; deferred list with owner-ratified impacts; re-open counts.
6. **Performance report** — full budget table per platform with .utrace paths; the single worst location named; memory curves.
7. **Content report** — chapter/boss/ending/memory inventory vs design; CD sign-off list; cultural compliance (consultant sign-offs).
8. **Platform & commercial** — D-1…D-6 status; store readiness; licensing audit result.
9. **Known limitations** — everything not met, honestly, with owner decisions attached. (A report with no limitations is not believed.)
10. **Recommendation** — ship / ship-with-conditions / hold, with the specific conditions.

**Audit rule (G-11):** the TL performs a random sample audit — 20 evidence paths from the report, each opened and verified to exist and match the claim. The audit result is recorded in the report.

## 9. Release decision

The owner makes the release call (it is never the agent's). The TL's obligation ends at G-11: a truthful, auditable report. If any gate fails, the report says so and names the remaining work with effort estimates — the owner then decides (fix, descope by ADR, or hold). No gate is "mostly passed".
