# STAGE 0 EVIDENCE REPORT

**Date:** 2026-11-16
**Engine:** none available in this environment (`UNAVAILABLE` — see ADR-0005)
**Status tag for the whole stage:** **PARTIAL** — all host-verifiable work is ESTABLISHED; all runtime work is SPEC.

---

## 1. What was actually executed

| # | Command | Result | Evidence file |
|---|---|---|---|
| 1 | `python3 -m unittest discover -s Tools/canon/tests -v` | **PASS — 58 tests** | `Docs/evidence/stage0/L0_canon_index_validation.json` |
| 2 | `python3 Tools/ci/l0_checks.py --evidence …` | **PASS — 8/8 checks** | `Docs/evidence/stage0/L0_repository_checks.json` |

Both commands are reproducible from a clean clone with Python 3.9+ and no third-party packages.

## 2. Test coverage — what the 58 canon tests prove

The suite is not a smoke test. Most cases **mutate the index into a known-invalid state and assert the
specific rejection**, which is the only way to show a validator would actually stop bad data.

| Area | Tests | Proves |
|---|---|---|
| Structure & schema | 6 | Index shape is correct; the hand-rolled schema validator supports every keyword the schema uses (so no constraint is silently skipped); booleans are not accepted as integers |
| Chapters | 5 | Exactly 8 chapters, ordered 1–8, names and bosses match the directive; removing a chapter fails |
| Approvals (OAD-47/48) | 4 | Design approval cannot masquerade as canon approval; nothing can be `Shippable` before `CanonApproved`; Chapter 8 is correctly design-approved-but-not-canon |
| Memories (OAD-32) | 10 | Exactly 7; one per chapter 1–7; scene/location IDs match the published table; discovery locations must be registered (or the memory can never be found); all four fragments non-empty; no memory may live in Ch08 |
| Bosses (OAD-21) | 5 | All 8 present and matching the chapter table; every arena design is `Proposed`, never canon-approved |
| Chapter rules | 9 | Python rule excludes both enemy and loot (OAD-14); Ch02 no-flame; Ch07 ember-not-stone; every rule must name its enforcement; cultural-fictionality rule exists |
| IDs | 4 | Unpadded, lowercase, wrong-length and unknown-type ids all rejected |
| Source documents | 3 | Four authority registers recorded with Drive IDs and declared authority |
| Schema behaviour | 7 | Type/enum/required/additionalProperties violations caught |
| Query helpers | 5 | Lookups used by the engine mirror behave correctly |
| Evidence | 1 | The run itself emits a machine-readable artifact |

## 3. What the 8 repository checks prove

`no_forbidden_binaries` · `required_docs` · `doc_links` · `json_parses` · `uproject` · `stage_gates` ·
`status_vocabulary` · `evidence_claims`

Two of these found real defects during authoring, which is the point:

1. **`json_parses` / canon schema:** the first canon test run failed with
   `$: unexpected property '$schema'` — the index declared `$schema` but the schema forbade additional
   properties. The schema was wrong, not the data. Fixed.
2. **`doc_links`:** the architecture document contained the save-schema snippet
   `Ledger[]` followed immediately by a parenthesised field list, which Markdown reads as a link to a
   non-existent file. The document was corrected to unambiguous notation.

Neither defect would have been visible in a prose review. Both were caught in under two seconds by a gate.

## 4. What was NOT verified (explicit)

| Item | Why | Tag |
|---|---|---|
| Any C++ compiles | No engine in this environment | `SPEC` |
| `TDD.uproject` loads | No engine | `SPEC` |
| Module build order and dependencies are correct | No engine; the `Build.cs` dependency lists are plausible but unproven (`MetasoundEngine`, `GameplayStateTreeModule`, `ModelViewViewModel` module names are **not** confirmed against 5.8) | `SPEC` — **first thing Stage 1 must confirm** |
| `Source/TDD.Target.cs` `EngineIncludeOrderVersion` value is valid for 5.8 | No engine; `Unreal5_6` is used as the most recent value known at authoring time | `SPEC` — verify on first build |
| Gameplay Tags registry parses | No engine | `SPEC` |
| Any gameplay behaves | Not implemented | `SPEC` |
| Visual canon compliance of any asset | No assets exist | `N/A` |

**Known risk carried into Stage 1:** the `Build.cs` files were written without an engine to validate module
names. Two entries are genuinely uncertain (`MetasoundEngine`, `GameplayStateTreeModule`) and one enum value
(`EngineIncludeOrderVersion`) may not exist in 5.8. Resolving these is the first task of the first build, and
they are recorded here rather than discovered silently later.

## 5. Stage 0 exit criteria

| Criterion | State |
|---|---|
| Master Engineering Architecture Document produced | **DONE** |
| Canon index + validators, green | **DONE** — 58 tests |
| Repo hygiene (`.gitignore`, `.gitattributes`, text-only policy) | **DONE** |
| ADRs 0001–0008 recorded | **DONE** |
| Stage gates and RACI documented | **DONE** |
| Interfaces (§6.2 ID types, §6.6 tags) authored | **DONE** — as `SPEC`, pending compilation |
| Interfaces signed off by all three agents | **PENDING** — requires agent onboarding |
| Architecture ratified by Technical Director | **PENDING** |
| Blocking decisions raised to Creative Director (D-01, D-02, D-04, D-10) | **RAISED** — see architecture doc §16 |

**Recommendation to the Technical Director:** accept Stage 0 on the host-verifiable evidence above, note the
three unverified build-configuration assumptions, and gate Stage 1 behind an engine-equipped run. The
highest-value Creative Director decisions are **D-01** (binary storage — blocks all content) and **D-10**
(cultural consultant — blocks every shippable depiction of a deity, mask or shrine).

---

## 6. Post-hoc correction (recorded 2026-11-16, Agent 2)

Read in full on 2026-11-16, `LOCATION_MASTER_REGISTER.md` v2.9 showed that this stage's canon model was **wrong
in two material ways**: it used an invented `{design, canon, shippable}` approval triplet, and it used
`CHxx-BOSS-<Name>` for boss arenas. The registers use three canon statuses plus a separate seven-value design
status, and `CHxx-BOS-nnn` for arenas.

The correction is landed and tested (`canon_index.json` v2.0.0, 101 canon tests). Full account:
`Docs/CANON_INDEX.md` §7 and `Docs/WORLD_ASSESSMENT.md` §2.

The three unverified build-configuration risks listed in §4 above remain **open** — the correction concerned
canon data, not engine code, and no engine has been available.
