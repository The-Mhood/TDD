# T00 — Takeover Assessment and Execution Strategy

**Project:** THE DISOBEDIENT DAUGHTER (*Nwanyi Na-anụghị Ihe*)
**Document ID:** TDD-TD-T00-001
**Version:** 1.0
**Date:** 2026-11-20 (UTC)
**Author:** Takeover Technical Lead (Arena Agent Mode, session branch `arena/553fb02d-tdd`)
**Status:** SUBMITTED FOR OWNER RATIFICATION (decisions D-01…D-09, §9)
**Method:** every claim below is tied to a commit, file, issue, screenshot or Drive reference verified directly on 2026-11-20. Nothing here is inferred.

---

## 1. Executive summary

1. **The project is real but pre-M1.** Four days of multi-agent work (2026-11-16 → 2026-11-20) produced: one UE 5.8 project that **compiles and passes 2/2 Unreal Automation tests on the owner's Mac** (M0, 2026-11-18), an excellent accepted M1 movement specification with a 31-criterion acceptance gate (v1.4), a two-day-old browser-playable technical prototype of Adanna in the Forbidden Forest, a 1.9 MB production asset handoff (proxy character + forest blockout), and a substantial Art Bible in Google Drive. **No gameplay system beyond the dodge-distance math exists in Unreal. Zero of AC-01…AC-31 is demonstrated.**
2. **The history was fragmented, not lost.** Five parallel branch lines never merged. One line (Agent 1/TD) holds the accepted M1 spec and ADRs; the canonical line (Agent 3, `arena/c64fc525-tdd`) holds the building project; the Agent 2 line holds the world architecture and the independent dodge review; the production line (today) holds the playable prototype and UE tooling; Agent 4 holds platform assessments. **This takeover has consolidated all of it onto `arena/553fb02d-tdd` (this branch) as the single working line. No branch was deleted or altered; originals remain as provenance.**
3. **The dominant risk is process, not technology.** Roughly 60% of agent effort to date went into a C-05 documentation-contract verification loop (40+ commits of fine-grained contract edits; 0/67 acceptance cases executed; the underlying telegraph system is unimplemented). Three separate UE project scaffolds were created in parallel. Two ADR series with colliding IDs exist. Until this is consolidated, every future agent risks re-fragmenting the project. The consolidation is executed (Phase 0); the C-05 line is parked by explicit decision (D-02).
4. **The verification loop is the critical path.** This sandbox is Linux with no Unreal Engine. The only machine that can build, run, cook and package the game is the owner's Mac (Apple M4, 16 GB, macOS 27.2.1, UE 5.8.4, Xcode 27.2). The established pattern — agent writes code + tests + a one-command runbook; owner executes and returns an evidence bundle; agent verifies — is proven (M0) and is the backbone of the plan. Every "verified" claim in this project is or will be an owner-executed, agent-reviewed, checksummed evidence artifact.
5. **The schedule is honest:** on current resources (1 Mac, 1 future reference PC, owner + agents), M1 completion is ~2–4 weeks, the playable vertical slice ~3–4 months, and commercial release of the full 8-chapter game is a **12–24 month program**, gated by Sony approval for PS5 and by creative-content decisions only the owner can make (§9).

---

## 2. Where the project actually stands (evidence)

### 2.1 Repository topology (verified 2026-11-20)

| Branch | Tip (UTC) | Line | Contents (verified by tree inspection) |
|---|---|---|---|
| `main` | 2026-11-16 | — | `README.md` (1 line) only. Commit `5e3d1da`. |
| `arena/c64fc525-tdd` | 2026-11-18 20:43 | **Agent 3 — canonical per Issue #1** | `TheDisobedientDaughter.uproject` (UE 5.8, 1 runtime module, Mac+Windows), 16 small source files, 3 automation tests, `Tools/engine/` build tooling, ~30 governance/contract docs. |
| `arena/3bc206a0-tdd` | 2026-11-18 20:28 | Agent 1 + TD + TDD-build/project | TDD-MEAD-001 master architecture (TDD-MEAD-001), **M1 Movement Specification v1.4 with AC-01…AC-31**, ADR-0001…0013, 9-module `TDD.uproject` scaffold (**never compiled**), M0 verification record, M1 execution scope (S1–S8), 22-item open-questions register, C-05 contract v4.0…v4.3.11 line. |
| `arena/5dde91a4-tdd` | 2026-11-18 17:28 | Agent 2 | World architecture (5-tier NPC model, streaming budgets, memory director, boss phase graphs), ADR-0101…0108 (imported renumbered), **independent M1 §3.5/AC-19 dodge review**, dependency/blocker register (B-01…B-12), evidence JSONs. Docs only; no project. |
| `arena/8efaa23f-tdd` | **2026-11-20 07:32 (today)** | Production/art line (owner commits directly) | Playable browser/Node prototype (verified), Adanna technical proxy GLB (21 joints/5 clips) + Forbidden Forest blockout GLB, `TDD_GAME.uproject` Mac-only scaffold (statically audited 79/79, **not compiled in-repo**), 10-gate owner runbook, toolchain gate for **UE 5.8.4 / Xcode 27.2 / macOS 27.2.1 / M4**, OUR_EYES 193-asset verdict package, Phase 2 production audit. |
| `arena/b2c58152-tdd` | 2026-11-18 09:47 | Agent 4 | Two assessment docs: UE5 graphics/engine production assessment (`48051c6`) and Mac/PS5 development assessment. No implementation. |

No pull requests exist. One open issue: **#1 "Dodge implementation review and UE 5.8 Mac verification handoff"** (2026-11-18) — a cross-agent handoff whose two tasks have since been overtaken (see §2.5). Companion public repo `The-Mhood/chat-gpt` holds the previous PM's artifact index (193-report art assessment) and **today's UE editor screenshots** (see §2.7).

### 2.2 Code state in the canonical project (verified file-by-file at `a7f940a`)

| Item | State | Evidence |
|---|---|---|
| Project descriptor | UE 5.8, one Runtime module, `TargetPlatforms: [Mac, Windows]` | `TheDisobedientDaughter.uproject` |
| Dodge distance math | **Implemented + verified** (18/18 standalone, g++ ASan/UBSan; in-engine test green per owner run) | `TDDDodgeDistanceMath.h`, `TDD.Movement.DodgeDistanceMath` |
| Capsule sweep | Implemented, code-level correct per Agent 2 review; **no world test, never exercised** | `TDDDodgeSweep.{h,cpp}` |
| Player character | Minimal `ATDDAdannaCharacter : ACharacter` — spring arm + follow camera + legacy input bindings + jump. No mesh, no state machine, no Enhanced Input | `TDDAdannaCharacter.*` |
| GameMode / PlayerController | Minimal wiring, automation-covered | `TDDGameMode.*`, `TDDPlayerController.*` |
| State machine, CMC subclass, camera criteria, input buffering, test map, animation | **Do not exist** | absence verified |
| M1 spec deliverables §2.1 (15 files) | 3 of 15 present in any form | spec §2.1 vs tree |

### 2.3 M0 — the one thing that is actually verified

Per `docs/06_IMPLEMENTATION/M0_VERIFICATION_RECORD_V1.md` (imported): on **2026-11-18**, the Project Owner ran `Tools/engine/mac_build.sh` on the owner's Mac at commit `e71401b6`: project generation, `TheDisobedientDaughterEditor` **BUILD PASS**, `TheDisobedientDaughter` **BUILD PASS**, automation **2 discovered / 2 passed / 0 failed**.

Honest limits recorded in that same document:
- Executed by the owner, not by any agent; **raw logs live on the owner's Mac** (`~/tdd-m0/Saved/BuildEvidence/20261118T202235Z`), gitignored, not inspectable by anyone else. The archive procedure (copy `index.json` + SHA256 into the repo) **was never executed**.
- Gate A (editor open with map, twice) and Gate D (packaging) **not evidenced**. Windows never compiled. No CI. No second cold run (AC-31 unproven).

### 2.4 M1 design — accepted and preserved (no changes made)

The M1 gate is **AC-01…AC-31** in `docs/02_PRODUCTION/AGENT1/M1_MOVEMENT_SPECIFICATION.md` v1.4 (TDD-A1-M1-SPEC-001), unchanged through four TD review rounds (v1.0→v1.4; each round's change log records "gate unchanged"). The traversal/combat contracts the owner listed are all in this document and are **intact**:

- **Damage taxonomy** (§3.2.1): `staggering | non-staggering | lethal | cinematic`, carried as data on the damage request; same-frame posture-break **promotion** evaluated before state resolution so a hit is never both "abort" and "stagger".
- **Staggering damage → forced `Stagger`** (priority 80, unrefusable); **non-staggering damage aborts only inside `AbortWindow`** (a *requested* abort → `Locomotion|Land`); health handling independent (health always decreases).
- **E1–E7 exit paths** each with fallback + restoration; **Dead outranks Stagger** when both apply (E5); **cinematic (E6) freezes the capsule — no positional fallback**.
- **Ordering rule** (§3.2.2): `ResolveAbortFallback()` → `RunRestorationChecklist()` → target state entry — restoration runs **exactly once**, fallback before restoration, restoration before entry (no "travelling hit reaction").
- **`ResolveAbortFallback()`** (§3.2.2, v1.3/v1.4): two-phase — bounded relocation loop (candidates 1 complete / 2 reverse / 3 drop-to-floor, `MaxRelocationAttempts` clamped [0,3], default 3) then **unbudgeted terminal hold** (H0 `FellOutOfWorld` → 4a Hold-Grounded snap ≤ 5 cm → 4b Hold-Unsupported zero-write `MOVE_Falling`). Two-phase "validate twice, place once"; single write path; forced transitions arriving mid-resolution are queued, never lost, applied after restoration.
- **Cinematic traversal uses no positional fallback** (E6 freeze mode) — preserved.
- **`bCausesStagger`**: remains a **proposal** pending Core interface review (v1.3/v1.4 notes; Appendix A). **Unresolved** — disposition in §8.3 (D-03).
- **`TraversalAbortPaths`** (M2 test, spec §5): edge cases E3–E7 fully specified including lethal-and-staggering precedence, cinematic no-drop, 4a/4b/4c behaviour, mid-abort placement failure, mid-resolution forced transitions, budget-0 direct-to-4a, kill-plane respawn. **Specified, not implemented** (M2).

**This takeover changed none of the above.** The document was copied verbatim onto the working branch (it was previously absent from the canonical branch — a gap the M1 execution scope document itself flagged: "copy it, do not re-derive it").

### 2.5 Outstanding handoff (Issue #1) — actual status

Issue #1 asked (a) Agent 2 to independently review the dodge implementation and (b) Agent 1/owner to execute the Mac verification and return evidence.

- (a) **Done**: `AGENT2_VERIFY_M1_DODGE_REVIEW_V1.md` (commit `e87c4d8`, now on this branch). Verdict: sweep mechanics PASS at code level; **three open defects**: ① AC-19 100-run determinism test absent; ② test-name/traceability mismatch (`TDD.Movement.DodgeDistanceMath` vs mandated `TDD-Unit.Movement.DodgeSpecMath` + `DodgeDistanceRepeatable`); ③ §3.5 clamped-end **floor validation not implemented**. Expected gaps: start-penetration refusal not wired; sweep not connected to CMC movement.
- (b) **Superseded in flight**: the owner's toolchain is now UE **5.8.4** (the Issue assumed 5.8.0–5.8.3-era Xcode constraints). Epic fixed the Xcode incompatibility (UE-396802) in 5.8.4; today's `verify_toolchain.sh` gate (commit `036d2b7`) encodes this. The owner opened `TDD_GAME.uproject` in the UE 5.8.4 editor **today** (screenshots in `The-Mhood/chat-gpt`: editor with `PLAYABLE_FOREST_M1` level, `C++ Classes`, imported `forbidden_forest_m1` folder, 8 actors). The 10-gate runbook (`README_MACOS_UE58.md`) is in progress on the production scaffold, **not** on the canonical project.

### 2.6 The three-scaffold problem (resolved by decision D-01)

| Scaffold | Location | Built? | Disposition |
|---|---|---|---|
| `TheDisobedientDaughter.uproject` (1 module) | canonical line | **Yes** (owner Mac, M0) | **Canonical project of record** |
| `TDD.uproject` (9 modules) | 3bc206a0 line | No, never compiled | Retired as a project; its **ADRs and specs are the adopted architecture** (TDD-MEAD-001 §3.2 module graph remains the target shape) |
| `TDD_GAME.uproject` (Mac-only, Python plugin) | 8efaa23f line | In progress on owner Mac today | Retired as a project; its **runbook, setup tooling, forest blockout and proxy character are imported** into the canonical project (Phase 0/1) |

### 2.7 Environment facts (verified)

- **Owner Mac (only UE machine):** Apple M4, 16 GB RAM, macOS 27.2.1 (26B131), UE 5.8.4 (CL 58902052), Xcode 27.2 (27B52). Confirmed by commit `036d2b7` message + today's editor screenshots. 16 GB is Epic's *minimum*; expect swap pressure and long shader compiles (Agent 4 §1.4).
- **Agent sandbox (me):** Linux, no UE, no Epic access. Can compile standalone C++/Python, cannot run Unreal.
- **Google Drive (connected):** canonical Art Bible workspace — 21 numbered folders + character/chapter/registry folders; Adanna and Amadioha master references approved (OAD-02); 193-file independent art assessment complete with CD final verdicts; `09_ANIMATION_AND_COMBAT`, `12_CINEMATOGRAPHY`, `13_GAMEPLAY_AND_LEVEL_DESIGN` folders **empty** (per Agent 4, 2026-11-18). Chapter 8 "Hall of Posts" V004 approved as environment design (canon still PENDING APPROVAL).
- **Previous PM conversation:** the ChatGPT share link is **not reachable from this sandbox** (network allowlist). Its substance was recovered from: the repo history, Issue #1, the `The-Mhood/chat-gpt` artifact repo (193-report index, today's UE screenshots), and the Drive workspace. **Gap recorded:** no verbatim transcript of PM decisions is available here; where PM intent matters (e.g., PS5 ambition, budget), §9 asks the owner to confirm.

### 2.8 Game design baseline (what we are building)

- **Genre:** single-player (ADR-0011), narrative third-person action-adventure with action-RPG combat, 8 chapters + Home Settlement (Forbidden Forest → Kingdom Beneath Earth → City of Living Dead → River of Idemili → Mountain of Thunder → Kingdom of Masks → Gates of the Dead → The Last Daughter/Ancestral Realm).
- **Player:** Adanna (25, approved identity locks recorded in the M1 art spec §2; weapon *omitted* from M1 pending its own review).
- **Enemies/bosses:** six PROPOSED archetypes (Rootwarden, Maskbearer, Thrall, Thunder Aspirant, +2) — **not ratified** (CD-3 open); shrine/mask/ritual vocabulary gated by cultural consultant (CD-2 open); seven named bosses, zero mechanics specified (Q-14).
- **Combat kit** (MEAD §4.2): attack/block/parry/stagger/dodge; damage taxonomy above; GAS for attributes (ADR-0004, proposed); declarative boss phase graphs (ADR-0107).
- **Rendering target:** Nanite + Lumen + VSM + World Partition + MegaLights on Windows/PS5 (production-ready in 5.8 per Agent 4 §5); **not available on Metal** — Mac is a development host, quality sign-off happens on a Windows DX12 reference or PS5 devkit.
- **Platforms:** canonical descriptor says Mac + Windows; production line today is Mac-only; PS5 requires Sony GDPA + devkit (Phase 2 gate; Agent 4 §2). **Owner decision D-04.**

---

## 3. What is already established (do not re-litigate)

1. Engine pin **UE 5.8** (Agent 4: last planned UE5 major; 5.9 preview-only; UE6 EA late 2027 — do not wait). Owner machine runs 5.8.4.
2. M1 gate **AC-01…AC-31** and all traversal/damage contracts (§2.4).
3. M0 **passed** (owner Mac, 2026-11-18, commit `e71401b6`) with honestly recorded Gate A/D gaps.
4. Status vocabulary and evidence rules (PASS/FAIL/BLOCKED/NOT RUN/NOT MEASURED; no inferred status; evidence is a log, not a sentence).
5. Canonical project identity: `TheDisobedientDaughter.uproject`, branch of record now `arena/553fb02d-tdd` (continuation of `arena/c64fc525-tdd`).
6. Adanna approved identity references (Drive OAD-02 master + portrait anchor + interim partial costume ref) and the explicit non-approved list (turnarounds, blade geometry, etc.).
7. The owner-executed verification loop (mac_build.sh pattern) and BuildEvidence bundle convention.
8. Art authority: Drive Art Bible + CD verdicts; nothing unapproved may be promoted (Phase 1 restrictions remain in force).
9. L-2 CLOSED (owner approval 2026-11-18); F-1b CLOSED; the C-05 S4.3.11 document set preserved as design record.

## 4. What is missing (gap register)

| ID | Gap | Blocks | Severity |
|---|---|---|---|
| G-01 | 11 of 15 M1 code deliverables (state machine, CMC, Enhanced Input, camera system, metrics harness, tests) | M1 | Critical |
| G-02 | `L_TDD_Test_Movement` test map (11 zones, spec §7) — must be authored in the editor on the Mac | All functional ACs | Critical |
| G-03 | M0 raw evidence not archived in repo; Gate A/D never evidenced; Windows never built; no CI; no second cold run | Trust in "verified" claims; AC-31 | High |
| G-04 | Agent 2's three dodge defects (100-run test, test naming, floor validation) | AC-19/AC-21 | High |
| G-05 | Sweep not wired to CMC; start-penetration refusal not wired | AC-21/AC-26 | High |
| G-06 | No character animation content (ADR-0005 blend-space fallback + mannequin clips are the path); `09_ANIMATION_AND_COMBAT` empty | M1 feel, M3 | High |
| G-07 | No save/persistence, UI, audio, camera shake, performance capture | M2+ | Medium |
| G-08 | Creative content decisions open: Q-01…Q-22 (platforms, hardware, bosses, memories, endings, cultural consultant, content pipeline) | Phase 2+ scope | Medium |
| G-09 | No Windows/PS5 build capability (no DX12 reference machine; no Sony devkit) | Final quality sign-off, PS5 | Structural |
| G-10 | No Git LFS; binaries currently committed raw (2.3 MB now; art imports will scale) | Repo hygiene | Medium |
| G-11 | C-05 telegraph contract unsigned/unfrozen, 0/67 executed; TD-06/TD-09/TD-12, U-07 open; B-11/B-15 open | M3 combat (telegraphs) | Medium |
| G-12 | Enemy archetypes unratified (CD-3); consultant gate open (CD-2); boss mechanics unauthored (Q-14) | M3+ | Medium |
| G-13 | Previous PM transcript unavailable in sandbox | Provenance completeness | Low (recorded) |

## 5. What must be recovered / researched / designed / implemented / tested / integrated / optimized / demonstrated

- **Recovered (this turn, done):** all five branch lines onto one working branch with provenance map (§10.1); M1 spec v1.4 into the canonical tree; M0 verification record; Agent 2 dodge review; ADR series unified (0001–0013 + 0101–0108 with collision map); production tooling/models into the tree.
- **To recover (Phase 0):** M0 raw evidence archive (owner runs one command: copy `index.json` + SHA256SUMS into `docs/06_IMPLEMENTATION/evidence/20261118T202235Z/`); confirm the exact state of the in-flight `TDD_GAME` run today (which of the 10 gates passed) so nothing is re-run twice.
- **To research:** (1) macOS 27.2.1 + UE 5.8.4 + Xcode 27.2 support matrix against Epic's published requirements (the `verify_toolchain.sh` gate encodes the working theory; first green Mac run confirms); (2) 16 GB memory headroom for editor+cook with the forest content (Agent 4 mitigations: DDC on external SSD, plugin pruning); (3) UE 5.8 Python API surface for map authoring (`LevelEditorSubsystem`, `new_level_from_template`) — the Phase 3 line already de-risked this; (4) CI options that work without a permanent Mac runner (GitHub Actions macOS runners for *package* verification only vs owner-Mac "build host" as de-facto CI).
- **To design (owner input, §9):** platform/hardware targets (D-04), module split timing (start single-module; split to TDD-MEAD-001 §3.2 graph on evidence), C-05 fate (D-02), boss pilot (Q-14), memory/ending content (Q-15/16), cultural consultant (Q-17/Q-02-CD-2).
- **To implement (M1, spec-driven):** S1–S8 per `M1_EXECUTION_SCOPE_AND_GATE_V1.md` (world-bound sweep test → floor validation → character+CMC+state machine → collision edge cases → camera five-criteria → Enhanced Input+buffering → test map → first playable Adanna), plus the first-playable gate M1-P1…P5 (packaging included).
- **To test:** every AC has a named automation test in spec §5 (already specified — implement as written); result lines `TDD_RESULT <test> <PASS|FAIL> <metric>=<value>`; manual procedures P1–P6 with CSV.
- **To integrate:** production forest blockout + proxy character into the canonical project (replacing/alongside the mannequin, clearly labelled); Drive Art Bible as content authority; M1 spec as movement authority.
- **To optimize (M2+):** streaming budgets measured on real content (B-12: ≤12 resident locations, ≤20 scenes, ≤14 AI agents, ≤8 s stream-in — currently *unmeasured*); AC-28 frame-cost budgets; reference-hardware perf capture.
- **To demonstrate before release:** §11 gate — 31/31 AC with quoted results; packaged build launch without editor; vertical slice at 60 fps on reference hardware; every `PENDING_CONTENT` label resolved or explicitly waived; PS5 (if in scope) Sony TRC pass; accessibility pass; save/load soak; crash-free 4-hour session; store-package install/launch on clean machines.

---

## 6. Consolidation (Phase 0) — executed and pending

**Executed this turn on `arena/553fb02d-tdd`:**
1. Fast-forward merged `origin/arena/c64fc525-tdd` (canonical project + Agent 3 docs) into this branch — this branch is now the continuation of the canonical line.
2. Imported from `3bc206a0`: TDD-MEAD-001, coding standards, PROJECT_STATE, OPEN_QUESTIONS (Q-01…Q-22), Agent 1 assessment v1.4, **M1 spec v1.4**, ADR-0001…0013 (+archives), M0 verification record, M1 execution scope, foundation docs, C-05 contract set (42 files, design record).
3. Imported from `5dde91a4`: world architecture, dependency/blocker register, enemy archetype review, **Agent 2 dodge review**, canon index, ADRs renumbered **ADR-0101…0108**, evidence JSONs → `docs/02_PRODUCTION/AGENT2/`.
4. Imported from `8efaa23f`: `TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/` (models, `ue_project` tooling + runbook, scripts, manifests, web-prototype source) + production governance docs → `docs/production/`.
5. This assessment, the canonical docs map, the post-consolidation state record, and the new README (§10).

**Pending (owner ratification D-01, then ≤1 day of work):**
- Archive the M0 evidence bundle (one command, §5).
- Migrate the forest blockout + proxy character from `TDD_GAME` content into the canonical project's import pipeline (GLBs are already in-tree; the import step runs on the Mac via the setup helper, adapted to the canonical project).
- Point the owner's next Mac run at the **consolidated** project (one runbook swap).
- Close/update Issue #1 with the consolidated handoff.

## 7. Verification loop (the operating system of this project)

```
Agent (Linux sandbox)                     Owner (M4 Mac, UE 5.8.4)
────────────────────────                  ────────────────────────────
write code + tests + runbook              run ONE command:
commit + push to this branch   ──►        ./Tools/engine/mac_build.sh --test-filter TDD
                                          (build both targets, run automation,
write evidence contract (paths,          collect Saved/BuildEvidence/<UTC>/
  report schema, exit-code semantics)    compact report: index.json + SHA256)
                                          commit the compact report (small,
verify the returned report:               text, committable) to the repo
  - discovered/started/completed counts  ◄── or post it as an issue attachment
  - every AC's named test present
  - TDD_RESULT lines parsed
  - Agent 2 independent diff review
verdict: PASS / FAIL / BLOCKED per AC;
quality ledger updated with commit+hash
```

Rules: no stage is complete on standalone tests alone (M1 execution scope §4); a green editor is not a build pass; screenshots supplement, never replace, logs; every evidence bundle names the exact commit it was run against.

## 8. Technical decisions made by the Takeover Lead (binding unless owner objects within the ratification window)

1. **D-01 — Single canonical project.** `TheDisobedientDaughter.uproject` is the only Unreal project. `TDD.uproject` and `TDD_GAME.uproject` are retired as projects (their useful content is imported; both scaffolds remain on their original branches, untouched). Rationale: one verified build identity, one evidence stream, no split module graphs.
2. **D-02 — C-05 parked, not cancelled.** The telegraph/StateRevision contract (S4.3.11 set) is preserved as design record with its 0/67-executed status. It is **not** to be signed, frozen, or re-revised until the M3 combat framework exists that consumes it; the 67 acceptance cases will then be executed against real code or the contract re-scoped with evidence. TD-06/TD-09/TD-12 remain owner/TD decisions, untouched. No further C-05 document edits are authorized under this takeover.
3. **D-03 — `bCausesStagger` ruling (closes the open review).** APPROVED as specified: a data-driven flag on the damage request (`FTDDDamageRequest::bCausesStagger`), defaults = heavy/unblockable → staggering, chip/environmental → non-staggering, tuning deferred to M3 combat design. Rationale: the M1 spec's entire arbitration (§3.2.1–§3.2.3) is already written against this exact shape; making it data (not a hard-coded rule) satisfies the review's concern; freezing it now prevents the state machine from being built around a different contract. It becomes a frozen Core type when M3 damage implementation lands.
4. **D-04 — Platform posture (default, pending owner D-04 ratification).** Development on Mac (canonical + owner machine). **Windows (x64) is the first shipping target** (matches the canonical descriptor and Epic's reference platform; required for Nanite/Lumen-HWRT quality sign-off). PS5 is a **Phase 3 gated target** (Sony GDPA + devkit; application filed after the vertical slice). Mac packaging is supported for iteration/demos but is not a shipping target. This matches the M0 record, Agent 4's assessment, and the canonical descriptor — it does *not* follow the production line's interim Mac-only setting.
5. **D-05 — Module strategy.** Start and ship M1–M2 in the single existing runtime module (proven by M0; fastest compile on 16 GB). Split toward TDD-MEAD-001 §3.2's graph (`TDDCore` / `TDDGameplay` / `TDDAI` / `TDDWorld` / `TDDNarrative` / `TDDUI` / `TDDTests`) **only when** cross-team ownership or compile-time evidence justifies it; the 9-module scaffold's layering rules (ADR-0003) are adopted as the split's target, not as day-one structure.
6. **D-06 — Test naming.** All project tests use `TDD.<Area>.<Subject>` with `EditorContext | EngineFilter` and `#if WITH_DEV_AUTOMATION_TESTS`; M1's mandated `TDD-Unit.Movement.*` names from spec §5 are the traceability source of truth (fixes Agent 2 defect ②).
7. **D-07 — Evidence in repo, build output out.** Only machine-readable reports + checksums are committed (`docs/06_IMPLEMENTATION/evidence/<UTC>/`); `Saved/`, `DerivedDataCache/`, `Intermediate/` stay gitignored. Git LFS (ADR-0104) activates when binary content imports begin.
8. **D-08 — Governance.** One working branch (this one), one quality ledger, one ADR series (0001–0013 + 0101–0108; new ADRs continue from 0109), one issue for cross-agent handoffs. Specialist agents work on short-lived offshoots merged back within the same day or their branch is closed; **no agent creates a new .uproject, a new ADR series, or a new contract series without TD sign-off recorded in the ledger.**
9. **D-09 — Schedule gate cadence.** Each phase ends in (a) an owner-executed evidence run and (b) a ledger entry. No phase is "done" on code-only claims.

## 9. Decisions required from the owner (with my recommendation + default if unanswered)

| # | Decision | My recommendation | Default if silent |
|---|---|---|---|
| D-10 | Ratify consolidation (§6) and the canonical-project ruling (D-01) | Yes | Proceed (reversible; originals untouched) |
| D-11 | Platform scope: Windows first ship; PS5 Phase 3-gated; Mac dev-only (D-04) | As recommended | As recommended |
| D-12 | Reference/min hardware: accept the proposed **RTX 3060 Ti / 16 GB class, 1440p @ 60 fps** min as the perf budget anchor (Q-03) | Yes; buy/lease a used DX12 PC at Phase 3 entry (Agent 4: the single most important non-Mac purchase, ~$600–1,200) | Budget held at that class |
| D-13 | Ratify D-02 (C-05 parked) and D-03 (bCausesStagger approved) | Yes | As recommended |
| D-14 | Adanna M1 visual: use the labelled engineering proxy (stock mannequin per spec §3.1) until creative approval of a production character lands; the Phase-3 technical proxy GLB is an *interim labelled* asset, not Adanna art | Yes | As recommended |
| D-15 | Authorize M0 evidence archive + one consolidated "M0′" Mac run on this branch (one command) | Yes | Blocked until answered |
| D-16 | Confirm PS5 ambition (it changes the Sony application timing: file after vertical slice, needs a registered entity + GDD) | Keep the option, file at Phase 3 | Kept, not filed |
| D-17 | Cultural consultant engagement (Q-17; CD-2 gate blocks shrine/mask/ritual vocabulary incl. Maskbearer) | Engage before Phase 3 content; blockout-only meanwhile (CD-5 restrictions) | Blockout-only |
| D-18 | External NVMe SSD for project+DDC (Agent 4: cheapest large time-buy on a 16 GB machine) | Yes | Recommended, non-blocking |

## 10. Dependency-aware roadmap

### Phase 0 — Consolidation & governance (this turn → +1 day) ✅/⏳
- ✅ History recovered; five lines consolidated onto `arena/553fb02d-tdd`; provenance map published (`CANONICAL_DOCS_MAP.md`).
- ✅ M1 spec v1.4 + M0 record + Agent 2 review + ADRs in the canonical tree.
- ⏳ Owner: ratify D-10…D-13, D-15; run the M0 evidence archive command.
- ⏳ M0′ — one consolidated Mac build+automation run on this branch's tip (evidence bundle committed).
- ⏳ Issue #1 updated; new handoff issue opened for the M1 execution loop.
- **Exit gate:** one green M0′ run + archived M0 evidence + owner ratification recorded in the ledger.

### Phase 1 — M1 completion (≈ weeks 1–4; agent code + owner runs)
- S1 world-bound sweep tests (`TDD.Movement.DodgeSweepBlocked/Clear`) — kills "unexercised code" (Agent 2 gap 4).
- S2 destination-floor validation + floor-distance correction (defect ③) + 100-run determinism test `TDD-Unit.Movement.DodgeSpecMath`/`DodgeDistanceRepeatable` (defects ①②).
- S3 `ATDDPlayerCharacter` v2: `UTDDCharacterStateMachine` (196-pair rules table, forced transitions, exit checklist, buffer policy, min dwell), `UTDDCharacterMovementComponent`, Enhanced Input (plugin + Build.cs), dodge drives real CMC movement, mode restoration (AC-26/AC-29).
- S4 collision edge cases: clamped distance, start-penetration refusal wired, per-frame no-penetration (AC-21/AC-22/AC-23).
- S5 camera: `TDDPlayerCameraManager` + `UTDDCameraRigComponent`, five stability criteria instrumented (AC-14…AC-18).
- S6 input: mapping contexts, buffering (single consumption, replace-not-queue, expiry), coyote window, device parity (AC-24/AC-25/AC-27).
- S7 `L_TDD_Test_Movement` authored in the editor on the Mac (spec §7 zones; Python-assisted where possible, owner confirms).
- S8 first playable Adanna: launch → control → traverse → obstacle → movement actions → interaction (M1-P1…P5; **packaging = Gate D**).
- **Exit gate:** 31/31 AC PASS with quoted `TDD_RESULT` lines; P1–P6 manual procedures recorded; Agent 2 diff review clean; packaged `.app` launches without editor; AC-31 three cold runs identical.

### Phase 2 — M2 traversal & world; M3 combat framework (≈ weeks 4–10)
- M2: traversal execution + `TraversalExitRevalidation` (E1/E2) + `TraversalAbortPaths` (E3–E7) exactly as spec'd (the preserved edge cases); interaction volumes; forest blockout integrated into a `L_TDD_Forest_Slice`; streaming budgets first measured (B-12).
- World: 5-tier NPC model for Chapter 1 (register data exists; 29 scenes exact head-count); navigation; memory director frame (memory 1 binding verified).
- C-05: implement telegraph against real code; execute the 67 acceptance cases or re-scope with evidence (D-02).
- M3: combat kit (attack/block/parry/stagger), damage pipeline with `bCausesStagger` data (D-03), first placeholder enemy (CD-3 ratification required for real archetypes).
- **Exit gate:** traversal abort paths green; combat loop playable with one enemy type; C-05 disposition evidenced.

### Phase 3 — Vertical slice + reference hardware (≈ months 3–4)
- Home Settlement slice at real scale (World Partition); Nanite-appropriate assets authored for DX12/PS5 (Mac uses Software Lumen for mood only); lighting look-dev vs approved boards; audio (MetaSounds) first pass; UI/UX (pause, map, inventory frame); save/load (ADR-0007: 3 manual + auto + checkpoint); performance capture vs D-12 budget; crash soak.
- Owner purchases DX12 reference PC (D-12) → final-quality sign-off pipeline established.
- Sony partners application filed if D-16 confirms PS5 (entity + GDD + slice).
- **Exit gate:** 20-minute slice, 60 fps on min-spec DX12, no fatal errors, save/load soak pass, marketing screenshots at the approved quality bar.

### Phase 4 — Full production (≈ months 5–12+)
- Chapters 1–8 content pipeline (Drive Art Bible → 3D, per CD verdicts); seven bosses (declarative phase graphs, ADR-0107; pilot first); memories 2–7 + three endings (Q-15/16); full NPC populations (TR-1…TR-5 traceability); localization (Q-13); accessibility (Q-10); difficulty options (Q-11, data-driven hooks ready); PS5 devkit bring-up + TRC certification (if D-16); packaging/install/release engineering; marketing build.
- **Release gate:** §11.

## 11. Commercial release demonstration list (what "done" means)

1. Graphics: final art pass on every shipping scene per approved boards; quality sign-off on reference hardware (not Mac); LODs/UVs/materials clean for Nanite.
2. Character: production Adanna (approved turnaround → sculpt → rig → groom → PBR), no `PENDING_CONTENT` on shipped content.
3. Animation: full locomotion/combat set, blend-space/retarget pipeline per ADR-0005; no mannequin in a shipping build.
4. Physics/collision: zero unexplained penetrations in 4-hour soak; step/slope/corner ACs hold in shipped levels (not just the test map).
5. Movement/traversal: M1 ACs + M2 abort paths green in shipped content.
6. Combat: kit + all shipping enemy archetypes + pilot boss balance pass; damage taxonomy honoured in every hit path.
7. AI: five-tier model within measured streaming budgets; no budget overruns (B-12 measured, not assumed).
8. World: World Partition streaming ≤ 8 s worst case; navigation complete per chapter.
9. Progression: chapter flow, save/load (3 manual + auto + checkpoint), no save corruption across 100 cycles.
10. Audio: MetaSounds mix, VO/adaptive music per `11_AUDIO_AND_MUSIC` (currently empty → to be produced), no pop/click in 20-min soak.
11. UI/UX: pause/map/inventory/credits; all screens reachable by mouse, keyboard and gamepad; rebind works live.
12. Camera: five-criteria suite green on shipped levels; no unflagged acquisition.
13. Performance: 60 fps min-spec DX12 on the slice's heaviest scene; frame-cost budgets (AC-28 class) documented per system.
14. Persistence: cross-session save integrity; delete/save-scum policy per Q-09 decision.
15. Stability: 4-hour unattended session, zero fatal errors; crash telemetry decision per Q-22.
16. Multiplayer: out of scope (ADR-0011) — re-opened only by owner decision.
17. Accessibility/platform: Q-10 baseline; Windows primary; PS5 TRC pass if in scope; Mac demo build.
18. Packaging: clean-machine install → launch → 10-minute session on the target platform(s); store-package metadata; age-rating content review (violence/gore per platform boards).

## 12. Risks (top 8, with owners and mitigations)

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-1 | Owner Mac (16 GB, only UE machine) is a single point of failure and a perf bottleneck | High | High | Evidence loop keeps Mac duty to discrete runs; D-18 SSD; DX12 PC at Phase 3; all authoring renderer-agnostic so nothing is re-authored |
| R-2 | macOS 27.2.1 / Xcode 27.2 / UE 5.8.4 support not officially confirmed by Epic | Medium | High | `verify_toolchain.sh` gate; first green run is the confirmation; fallback pinned Xcode 26.1.1 alongside (runbook documents both) |
| R-3 | Process re-fragmentation by parallel agents | Medium | High | D-08 governance; one branch; ledger-enforced status vocabulary; TD veto on new scaffolds/ADRs/contracts |
| R-4 | Creative content decisions (bosses, memories, consultant) stall Phase 3+ | Medium | High | Frameworks built content-agnostic with labelled placeholders (OPEN_QUESTIONS defaults); decisions surfaced weekly in the ledger |
| R-5 | Scope creep toward "commercial quality" across 8 chapters on solo-owner capacity | High | High | Phase gates with evidence; slice-first; per-phase exit gates (§10); release list (§11) is the contract |
| R-6 | M1 feel fails P1–P6 despite green ACs (tuning loop on one machine) | Medium | Medium | Thresholds are data (spec); tuning iterations batched into single Mac runs; owner plays the build each stage |
| R-7 | Binary asset growth breaks the repo (no LFS yet) | Medium | Medium | D-07; LFS (ADR-0104) at first content import; 128 MB patchset discipline |
| R-8 | PS5 ambition without entity/approval derails schedule | Medium | Medium | Phase 3-gated (D-16); Windows ship path never depends on it |

## 13. What this document deliberately does NOT do

- It does not modify AC-01…AC-31, the traversal/damage contracts, or any approved art verdict.
- It does not authorize gameplay implementation beyond what Phase 0 requires (per the owner's Part 6 instruction).
- It does not claim any build/test result that was not executed by the owner's Mac.
- It does not close Issue #1 (its owner-Mac verification items are superseded but the issue remains the vehicle for the consolidated handoff).
