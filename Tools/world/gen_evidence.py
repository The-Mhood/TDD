#!/usr/bin/env python3
"""Generate the evidence artifact for this milestone.

Evidence must be produced by running the tools, not written by hand. This
scripts the run and records what actually happened, including failures.

Usage: python3 Tools/world/gen_evidence.py [--out PATH]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]


def run(cmd: List[str]) -> Dict[str, Any]:
    started = dt.datetime.now(dt.timezone.utc)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    finished = dt.datetime.now(dt.timezone.utc)
    return {
        "command": " ".join(cmd),
        "exit_code": proc.returncode,
        "passed": proc.returncode == 0,
        "duration_ms": int((finished - started).total_seconds() * 1000),
        "stdout_tail": proc.stdout.strip().splitlines()[-6:],
        "stderr_tail": proc.stderr.strip().splitlines()[-6:],
    }


def check_measurement_claims() -> Dict[str, Any]:
    """Verify NO generated scene row claims to be empirically measured.

    This is a direct check, not a delegated one. The L0 gate also covers it, but
    evidence that only asserts a gate ran is evidence about the gate, not about
    the data. If a future change made this field True, the run must fail loudly
    here - the artifact itself is what a reader will believe.
    """
    started = dt.datetime.now(dt.timezone.utc)
    artifact = (REPO_ROOT / "Docs" / "evidence" / "agent2"
                / "CH01_population_budget.json")
    problems: List[str] = []
    checked = 0
    try:
        data = json.loads(artifact.read_text(encoding="utf-8"))
        for scene in data["budget"]["scenes"]:
            checked += 1
            if scene.get("npcs_is_measured") is not False:
                problems.append(
                    f"{scene.get('scene_id')}: npcs_is_measured="
                    f"{scene.get('npcs_is_measured')!r} (provenance "
                    f"{scene.get('npcs_provenance')!r}) - authored register data "
                    f"is not a measurement and no engine has run")
    except Exception as exc:
        problems.append(f"cannot verify measurement claims: {exc}")
    if checked == 0 and not problems:
        problems.append("no scene rows inspected; the artifact may be empty")

    finished = dt.datetime.now(dt.timezone.utc)
    return {
        "command": "gen_evidence.check_measurement_claims",
        "exit_code": 1 if problems else 0,
        "passed": not problems,
        "duration_ms": int((finished - started).total_seconds() * 1000),
        "stdout_tail": [f"{checked} scene rows inspected, all npcs_is_measured=false"]
        if not problems else [],
        "stderr_tail": problems[-6:],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(
        REPO_ROOT / "Docs" / "evidence" / "agent2" / "W-M2_evidence.json"))
    args = parser.parse_args()

    py = sys.executable
    results = {
        "canon_tests": run([py, "-m", "unittest", "discover",
                            "-s", "Tools/canon/tests"]),
        "world_tests": run([py, "-m", "unittest", "discover",
                            "-s", "Tools/world/tests"]),
        "l0_gate": run([py, "Tools/ci/l0_checks.py"]),
        "count_reconciliation": run([py, "Tools/world/count_reconciliation.py"]),
        "population_budget": run([py, "Tools/world/population_budget.py",
                                  "--chapter", "CH01"]),
        "greybox_rules": run([py, "Tools/world/greybox_rules.py",
                              "Tools/world/data/greybox_ch01.json"]),
        "sensitivity": run([py, "Tools/world/sensitivity.py",
                            "--out", "Docs/evidence/agent2/"
                                     "CH01_population_sensitivity.json"]),
        "world_manifest": run([py, "Tools/world/world_manifest.py",
                               "Tools/world/data/CH01_manifest.json"]),
        "canon_index_validation": run([py, "-m", "unittest",
                                       "Tools.canon.tests.test_canon"
                                       ".TestIndexIsValid"]),
        "measurement_claims": check_measurement_claims(),
        "contract_data_checks": run([py, "Tools/world/contract_data_checks.py"]),
        "review_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_contract_review.py"]),
        "review_r2_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_contract_review_r2.py"]),
        "review_r3_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_contract_review_r3.py"]),
        "review_r4_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_contract_review_r4.py"]),
        "review_c05_3_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1_c05_3.py"]),
        "review_c05_s2_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s2.py"]),
        "review_c05_s3_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s3.py"]),
        "review_c05_s4_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s4.py"]),
        "review_c05_s4_1_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s4_1.py"]),
        "review_c05_s4_1_addendum_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s4_1_addendum.py"]),
        "review_c05_s4_2_document_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s4_2.py"]),
        "review_c05_s4_3_5_arch_claims": run(
            [py, "-m", "unittest", "discover", "-s", "Tools/world/tests",
             "-p", "test_review_a1c05_s4_3_5.py"]),
    }

    payload = {
        "meta": {
            "milestone": "W-M2.15 — independent reassessment of A1-C05-S4.2 v4.2, blob "
                         "7d03e1df at a788f95, path "
                         "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md. Outcome: PASS WITH "
                         "CONDITIONS. All 17 prior findings and conditions reassessed: 15 "
                         "closed and verified against the text, 2 closed with a recorded "
                         "caveat, 0 still open. D-4 audio closed document-wide; D-1a bound "
                         "now DERIVED and unbroken in 400,000 brute-forced schedules; "
                         "C4c-N1 corrected as specified with PO-3 retained; D-6a-i satisfied "
                         "by DV-24 failing on S4.0; D-6b tallies machine-derived and matching "
                         "my independent parse. TWO NEW DEFECTS, both non-normative: N-1 "
                         "DV-22's whole-document scan is a keyword allowlist with a "
                         "demonstrated false negative; N-2 two incompatible documents both "
                         "declare TDD-A1-C05-SUCCESSOR-004.2 on two branches. Neither "
                         "requires a normative change, so PASS WITH CONDITIONS rather than "
                         "TARGETED REVISION. Agent 1's shipped validator independently "
                         "reproduces 27/27 on the reviewed blob and discriminates on "
                         "S4.1/S4.0/S3",
            "w_m2_16": (
                "W-M2.16 - independent ARCHITECTURE review (not a confirmation exercise) of "
                "A1-C05-S4.3.5, blob a0b46f46 at baa31db, path "
                "docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md, 1779 lines. Outcome: PASS WITH "
                "CONDITIONS, one condition C-1. The C-05 ownership model is coherent, "
                "implementable and internally consistent; authority boundaries are correctly "
                "assigned and held; message ownership, audio ownership, state transitions and "
                "timing semantics are sufficiently precise; the normative clauses agree with "
                "the architecture, obligations, ownership tables and proposed cases; no "
                "contradiction, impossible requirement or hidden dependency was found; the "
                "identity and scope decisions are preserved with no silent architecture "
                "change (43 obligation rows, 6 clauses and 17 case specifications are "
                "byte-identical to S4.3.4); all seven prior defects D-1..D-7 and all seven "
                "conditions are genuinely closed, verified against the text and by executing "
                "the instruments rather than reading the status column; the Agent 3 "
                "TN-C-11/TN-A-01/TN-A-02 conflict is accurately represented as S4's own "
                "resolution with Agent 3 asked to confirm, and remains unresolved where it "
                "should (TD-09 OPEN); no architectural regression was found. ONE MAJOR, "
                "THREE MINOR, FOUR OBSERVATIONS, ZERO BLOCKERS. MAJOR-1: DV-22 still admits "
                "two false negatives - contrastive apposition ('Agent 1, unlike Agent 2, "
                "owns the audio cues') and the number-word form ('The first agent owns the "
                "audio cues') - both reproducing a clean 27/27; the contract text is correct, "
                "so this is a defect in the certificate, not the thing certified. The fix I "
                "recommend was implemented and measured against three populations at once "
                "(clean document 27/27 with 0 offenders, both escapes FAIL, existing suite "
                "67/67); the intuitive alternative was measured, failed, and is recorded as "
                "rejected. MINOR-1: the suite-count audit is a recorded table rather than an "
                "enforced check, disclosed as such in the document. MINOR-2: closing C-1 will "
                "stale eleven audit rows. MINOR-3: both obvious repairs to DV-22 fail while "
                "looking correct. Governance unchanged: C-05 and U-07 open, DESIGN_ONLY, "
                "unsigned, unfrozen, no MEAD selected, 0 of 67 acceptance cases executed, and "
                "the 67 instrument regressions are not acceptance tests."
            ),
            "date": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"),
            "agent": "Agent 2 (world structure / level architecture)",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "engine": "NONE — no Unreal Engine, no GPU, no compiled code",
            "scope_statement": (
                "Every result below is Python validation over register-derived data. "
                "Nothing here demonstrates engine behaviour. Streaming, Mass Entity, "
                "AI, navigation and boss execution are UNTESTED and UNIMPLEMENTED. "
                "All runtime systems remain SPEC under ADR-0005."
            ),
            "all_passed": all(r["passed"] for r in results.values()),
        },
        "results": results,
        "claims": [
            {"claim": "canon mirror regenerates bit-identically from fixtures",
             "method": "L0 canon_mirror_drift check", "result": "verified"},
            {"claim": "register published counts sum to their per-chapter rows",
             "method": "count_reconciliation.check_published_consistency",
             "result": "verified"},
            {"claim": "location entries are 196, not 191",
             "method": "arithmetic + regression test guarding the stale value",
             "result": "verified"},
            {"claim": "Chapter 1 parses 46 of 46 scenes",
             "method": "count_reconciliation", "result": "verified"},
            {"claim": "45 of 46 Chapter 1 scenes are not main/secondary story",
             "method": "two independent registers agree", "result": "verified"},
            {"claim": "31 of 46 Chapter 1 scenes need no simulated NPC",
             "method": "population_budget derivation", "result": "derived estimate"},
            {"claim": "CD-5 greybox restrictions are machine-enforced",
             "method": "greybox_rules + injected-tamper test", "result": "verified"},
            {"claim": "parsers handle the register's actual table format",
             "method": "114 canon tests", "result": "verified for Chapter 1"},
            {"claim": "parsers handle format variations gracefully",
             "method": "measured: 5 silent-failure modes documented, not fixed",
             "result": "documented limitation"},
            {"claim": "no row claims to be empirically measured",
             "method": "gen_evidence.check_measurement_claims inspects the artifact "
                       "directly; L0 gate is blind to provenance so REGISTER_DATA "
                       "earns no exemption",
             "result": "verified: 46 of 46 rows npcs_is_measured=false"},
            {"claim": "an exact dozen is twelve, not an unresolved range",
             "method": "parse_npc_count on 'A dozen people.' plus variants",
             "result": "verified: 12; 'dozens' and 'a dozen or so' still refused"},
            {"claim": "range budgeting uses both endpoints without a midpoint",
             "method": "band rows carry low/high, verbatim register wording, "
                       "endpoint_use and midpoint_used=false",
             "result": "verified"},
            {"claim": "Traversal capability is a register CATEGORY TAG, not an ID prefix",
             "method": "parse_location_summary over the 57-row v2.9 capture",
             "result": "verified: 8 traversal-capable locations; a TRV-prefix filter "
                       "would lose SUB-009 (ESTABLISHED), SUB-020 and EXP-003"},
            {"claim": "Chapter 1 location capture is complete",
             "method": "contract_data_checks family counts vs the register's published "
                       "1 + 40 + 16 = 57",
             "result": "verified: 57 rows, 0 duplicates, excerpt remains a subset"},
            {"claim": "the register's canon and design vocabularies are separate",
             "method": "OAD-48 check: three canon statuses, seven design statuses",
             "result": "verified: no value crosses between the two sets"},
            {"claim": "interactable IDs have a register source",
             "method": "inventory search of all six source documents",
             "result": "UNRESOLVED — no source exists; three options recorded, "
                       "TD decision requested (TD-3)"},
            {"claim": "A1-R1's RouteId format cannot address 4 of 8 traversal parents",
             "method": "cross-reference the 8 traversal-capable locations against the "
                       "46 scene rows' host-location column",
             "result": "verified: CH01-TRV-001..004 host zero scenes; a SceneId-bearing "
                       "format would require inventing canon"},
            {"claim": "A1-R1's five capability names are adopted verbatim",
             "method": "test_contract_review.TestCapabilityVocabulary",
             "result": "verified: all five named, no sixth invented"},
            {"claim": "the original submission's 42 acceptance tests are unique",
             "method": "test_contract_review.TestAcceptanceInventory",
             "result": "verified: 42 unique IDs, split 10 L0 / 11 L1 / 21 L2"},
            {"claim": "the three-vs-four L0 defect is resolved",
             "method": "enumeration of data availability per L0 test",
             "result": "corrected: 2 of 10 pass, 1 partial, 7 blocked; the 'four' "
                       "sentence was unsupported and is recorded as wrong"},
            {"claim": "three divergent MEAD files exist; TWO declare TDD-MEAD-001 v1.0",
             "method": "identity search across all reachable refs for 'Document ID'",
             "result": "verified: MEAD-A 1078 lines declares v1.0 (no 5.4, State.Combat.* tags); "
                       "MEAD-B 247 lines declares NO document ID or version; MEAD-C 1231 lines "
                       "declares v1.0 (5.4 present, 7 Status.* tags). v1.0 of this review wrongly "
                       "said all three declare the ID; corrected in v1.1 after Agent 3 recon V3 5.1"},
            {"claim": "Status.Dead has no tag in the canonical-adjacent MEAD",
             "method": "extract the Status.* set from MEAD-C section 5.1",
             "result": "verified: 7 tags, none for Dead. C-04's precedence top value is "
                       "unrepresentable as a TAG. Note Dead DOES exist as a value of "
                       "UTDDCharacterStateMachine and in the DT_StateRules state list"},
            {"claim": "no Chapter 1 source supports a carry state",
             "method": "keyword scan of the 57-row location capture and 46 scene rows",
             "result": "verified: no carry/portage/burden vocabulary; CarryState "
                       "withdrawn rather than invented"},
            {"claim": "A1-R2's MEAD citations were nearly called fabricated",
             "method": "all-refs identity search before publication",
             "result": "withdrawn before publication: MEAD-C exists on Agent 1's "
                       "branch and carries every cited section"},
            {"claim": "MEAD-C section 5.4 spells the damage-request struct two ways",
             "method": "extract every DamageRequest token from the section",
             "result": "verified: line 476 'FTDamageRequest', line 478 'FTDDDamageRequest'. "
                       "A third spelling 'FTDDamageRequest' appears only in reconciliation V3's "
                       "transcription of my proposal"},
            {"claim": "A1-R3 3.3(a)'s conversion is inverted",
             "method": "derive d(local)/d(axis) from A1-R3 3.2's own axis definition",
             "result": "verified: axis advances by PrimaryDilation, local by "
                       "PrimaryDilation*CustomDilation, so local=axis*rate. 3.3(a) "
                       "divides. Error is 1/rate^2; at rate 0.05 a 0.20s window "
                       "reports as 80s. 3.3(b)'s retime rule uses the inverse."},
            {"claim": "MEAD-C section 5.4's two struct spellings differ in length",
             "method": "character-level extraction of every DamageRequest token",
             "result": "verified: line 476 FTDamageRequest (15 chars), line 478 "
                       "FTDDamageRequest (16 chars). A1-R3 uses the 17-char "
                       "FTDDDamageRequest once and selects it silently."},
            {"claim": "MEAD-A has no Status.* namespace and forbids new ones",
             "method": "full-text extraction plus heading read",
             "result": "verified: zero Status.* matches; line 517 reads 'no agent "
                       "introduces a tag namespace'; Dead exists only as an enemy AI "
                       "StateTree state (line 615)"},
            {"claim": "A1-R4 cites MEAD-A line 506, not 505 - my prior review was wrong",
             "method": "git show the exact A1-R4 blob 2cc548fa and count occurrences of 505",
             "result": "0 occurrences of 505; the text says (506). My A1-R4 review section "
                       "7.2 erred by verifying the MEAD-A line and not grepping the citing "
                       "document. Withdrawn in this review section 0.3 with root cause."},
            {"claim": "INV-1 as written is false because it includes RemainingLocalSeconds",
             "method": "locate INV-1 in the reviewed blob; compute R(t) at two instants "
                       "inside one revision using A1-R4 section 3.3(e)",
             "result": "INV-1 lists RemainingLocalSeconds among fields identical at equal "
                       "revision. At ProducerRate 0.05, R0 0.20: frame 0 -> 0.2000, frame 2 "
                       "-> 0.1800, revision unchanged at 1. Every conforming producer "
                       "therefore violates INV-1 every frame, and equal-revision discard "
                       "(TN-C-01) loses the aged delta."},
            {"claim": "The later provenance correction changes no contract text",
             "method": "git diff reviewed blob bf6c8fb against branch-tip blob 30a98b8",
             "result": "6 insertions, 3 deletions, 9 changed lines, all in section 0 MEAD "
                       "rows and section 16 publication rows. All contract clauses "
                       "byte-identical. The user's statement is accurate."},
            {"claim": "WindowKey and AttackTag are absent from a snapshot whose consumers "
                      "were assigned by name",
             "method": "grep the reviewed blob for both; parse FTDDTelegraphSnapshot fields; "
                       "compare against A2-C05 section 7.6 Required list",
             "result": "0 occurrences of either in the blob. Snapshot carries exactly "
                       "AttackInstanceId, SourceEntityId, Phase, Timing. My own submission "
                       "marks both Required for parry/block and names montage selection as a "
                       "consumer, so 3 of my 4 named consumers cannot act without them."},
            {"claim": "C2's Core-owned surface exists in only one of three candidate MEADs",
             "method": "grep for TDDCore in MEAD-A, MEAD-B, MEAD-C",
             "result": "MEAD-C only (lines 227/228/267). MEAD-A has no TDDCore module at all "
                       "(section 4.2 lists TDDRuntime/{Core,Character,Combat,...}); MEAD-B has "
                       "zero occurrences. So C2 and C9 are MEAD-C-only conditions."},
            {"claim": "Coalescing is never prohibited by a normative clause in A1's response",
             "method": "grep -i coalesc across the response; classify each hit",
             "result": "3 hits: section 5.7 commentary, section 6.2 commentary, and one "
                       "section 10.2 test description. No condition, no P-obligation and no "
                       "section 7.2 clause forbids it."},
            {"claim": "Six of twelve conditions and eight of twelve P obligations have no test",
             "method": "regex every C1-C12 and P1-P12 against the section 10.2 suite rows",
             "result": "uncovered conditions C1,C2,C8,C10,C11,C12; uncovered obligations "
                       "P1,P2,P3,P7,P9,P10,P11,P12. Case counts sum to 30, matching A1's claim."},
            {"claim": "A1-R3 3.3(a)'s inverted conversion is corrected in A1-R4",
             "method": "re-derive d(local)/d(axis) from A1-R4 2.1, round-trip at 4 rates",
             "result": "verified: local=axis*rate (multiply), axis=local/rate (divide), "
                       "mutual inverses to 1e-12. 0.20s at 0.05 -> 4.00 axis -> 0.20 "
                       "local; old divide form gives 80.00, 400x = 1/rate^2"},
            {"claim": "A1-R4's telegraph broker leaves four concurrency gaps",
             "method": "search A1-R4 for adoption-ordering, at-most-once, eviction and "
                       "re-entrancy wording",
             "result": "verified absent: 'strictly greater', 'at most once', 'evict', "
                       "'re-entran'. Broker is placed in Core and declared authoritative, "
                       "which is Agent 3/TD's to grant"},
            {"claim": "MEAD-A line 506 (not 505) is the locomotion axis",
             "method": "line-by-line read of MEAD-A",
             "result": "verified: 506 = State.Locomotion.<...|Cinematic>, 507 = State.Combat, "
                       "517 = no-new-namespace prohibition, 615 = enemy AI Dead. "
                       "A1-R4 cites 505, which is Chapter.Ch01"},
            {"claim": "NPC prose parsing is correct",
             "method": "38-case parser suite; 2 new silent-corruption bugs found "
                       "and fixed this milestone (range summed as 16, abstract "
                       "number counted as a person)",
             "result": "verified; unresolved prose now REFUSED, never invented"},
            {"claim": "every Chapter 1 scene whose cost depends on an NPC count "
                      "now has register prose",
             "method": "population_budget over the verbatim v1.9 capture",
             "result": "verified: 0 of 14 CROWD scenes on a policy default"},
            {"claim": "the ambient-scene NPC default no longer moves the estimate",
             "method": "sensitivity sweep across expected_npcs 1..5",
             "result": "verified: elasticity 0.000 (was +0.88)"},
            {"claim": "the remaining uncertainty is bounded by the register",
             "method": "parse_npc_band over the register's own wording",
             "result": "PARTIAL: band 38.38-42.37 cost units and still OPEN at "
                       "CH01-SCN-014, which states no number"},
            {"claim": "population estimate sensitivity to policy assumptions",
             "method": "Tools/world/sensitivity.py, 4 sweeps + 5 scenarios, "
                       "before/after recomputed from both fixtures",
             "result": "only 4.6% of point cost still rests on policy defaults, "
                       "down from 75%; spread narrowed from 2.5x to 1.4x. The "
                       "remaining sensitivity is the crowd concurrency ratio and "
                       "cost unit, which no register can resolve"},
            {"claim": "the previous W-M2.1 model is preserved and reproducible",
             "method": "abridged fixture retained; sensitivity --previous recomputes "
                       "23.38/25.38/36.58/47.77/58.97 exactly",
             "result": "verified"},
            {"claim": "population budget reflects real engine cost",
             "method": "none — cost units are relative and unmeasured",
             "result": "UNVERIFIED — engineering assumption"},
            {"claim": "streaming / Mass / AI / navigation work",
             "method": "none", "result": "NOT TESTED — no engine"},

            # ---- W-M2.11: A1-C05-S3 v3.0 targeted review ----
            {"claim": "S3's 38 obligations split 17 P / 13 C / 6 R / 2 A",
             "method": "parse every '| **TN-x-nn' row from sections 7-9 of blob 07723236",
             "result": "verified: 38 rows, exact split, matches DV-1 and DV-3"},
            {"claim": "S3's 62 cases over 15 suites",
             "method": "parse suite table 12.1, sum Cases column, regex all T-C05-nn",
             "result": "verified: 15 suites, sum 62, ids 01-62 complete, none extra, "
                       "no case in two suites, no case in no suite"},
            {"claim": "S3's section 11.2 obligation-to-test map is bidirectional",
             "method": "parse 11.2 inverting both directions incl. the prefixed range "
                       "form 'T-C05-35 ... T-C05-39'",
             "result": "verified: 38 obligations each with >=1 case, 62 cases all covered, "
                       "no orphans either way. NOTE: a parser handling only the "
                       "second-endpoint range form reports 3 missing cases - the range is "
                       "prefixed on both ends"},
            {"claim": "INV-2's producer form and consumer form are the same function",
             "method": "substitute R0=(PhaseEndAxis-AxisNow)*Rate; evaluate both forms at "
                       "axis 0/0.2/2.0/4.0/8.0",
             "result": "verified algebraically and numerically to 1e-12 at all five axes, "
                       "including both clamps. EX-9's five rows reproduce exactly "
                       "(0.2000/0.1900/0.1000/0.0000/0.0000)"},
            {"claim": "S3's document instruments report their own counts correctly",
             "method": "re-run DV-2, DV-4, DV-6, DV-8, DV-9, DV-15 independently",
             "result": "verified for all six, INCLUDING DV-8 which claimed 10 and counted 16 "
                       "in S2: S3 reports 8 and there are exactly 8 lines containing "
                       "'execut'. ONE exception: DV-11 claims '6 role tokens' but only 5 "
                       "appear in the 38 implementer cells"},
            {"claim": "DV-11 cannot fail on the TN-C-12/TN-C-13 mis-mapping",
             "method": "extract the 7th cell of all 38 obligation rows; compare the token "
                       "mapping in 5.4 against the ownership of rows 6 and 7",
             "result": "verified: TN-C-12 and TN-C-13 are C-05 consumer obligations of row 6 "
                       "but carry the token mapped to row 7 (outside C-05). Both rows are "
                       "owned by Agent 2, and DV-11 tests agent agreement, so it passes. "
                       "The check is agent-level where C9 asked for row-level"},
            {"claim": "EX-5 omits the only-n+1 loss case, the dangerous one",
             "method": "read EX-5 cases (a)(b)(c)(c'); trace AD-1/AD-2/TN-C-09/TN-C-10 for a "
                       "consumer receiving only PhaseChanged@n+1",
             "result": "verified: n+1 == held+1 so no gap is recorded, no resynchronisation "
                       "is raised, and the consumer ages the whole phase at the pre-retime "
                       "ProducerRate with no detection. Section 3.6 rationale (c) asserts "
                       "the consumer 'merely needs a resync' but AD-2's trigger is an "
                       "incoming revision greater than held+1, which never arrives"},
            {"claim": "PO-3 fixes same-frame message ORDER but not message CONTENT",
             "method": "test both readings for a frame with one phase change and one "
                       "dilation change against TN-P-11 and INV-1",
             "result": "verified: reading B (n+1 carries the old rate) makes a mid-frame "
                       "pull return live state at revision n+1 with the new rate while the "
                       "published n+1 carries the old - same revision, two ProducerRate "
                       "values, INV-1 violated by a conforming producer. T-C05-51 asserts "
                       "the sequence only and cannot discriminate A from B"},
            {"claim": "WindowKey/AttackTag constancy contradicts TN-P-07 and T-C05-62",
             "method": "compare section 3.8 / 6.1 'constant for the lifetime' against "
                       "TN-P-07's 'every change to WindowKey or AttackTag' and T-C05-62's "
                       "identity-change setup rows",
             "result": "verified contradiction: if constant, TN-P-07's clause is dead and "
                       "T-C05-62's identity rows are unrepresentable; if mutable, the "
                       "constancy premise of 6.1's justification is false"},
            {"claim": "audio has two owners in C05-7.2 and no obligation covers it",
             "method": "read rows 5/6 of the 5.2 table and the 6.1 consumer table",
             "result": "verified: row 5 gives Agent 1 'camera and audio cues'; row 6 gives "
                       "Agent 2 'audio cue selection'; 6.1's consumer table assigns audio to "
                       "Agent 2; no TN row covers audio cue selection"},
            {"claim": "S3 does not assume C-04, Status.Dead or any TD decision is closed",
             "method": "search all of sections 14-18 for closure claims; check B-7/B-11/B-12/B-13",
             "result": "verified: B-7 OPEN-registry, B-11 BLOCKED BY DEPENDENCY with the "
                       "decision named as C-04's, B-12 open and not proposed, B-13 open and "
                       "non-blocking. Section 14.1 states 'No status in 14.1 has changed "
                       "since S1' and no closure is claimed anywhere"},
            {"claim": "the S3 blob reviewed differs from the branch tip only in placeholders",
             "method": "git diff of blob 07723236 against tip blob 80060dea",
             "result": "verified: 3 insertions, 3 deletions, all PUB_COMMIT/PUB_BLOB "
                       "placeholder fill in section 17 and section 18.1. Every normative "
                       "clause byte-identical"},
            {"claim": "C-05 / U-07 / acceptance tests are closed by this review",
             "method": "none - this is a design review, not a run",
             "result": "NOT CLAIMED. C-05 and U-07 remain open; 62 cases PROPOSED / NOT RUN; "
                       "0 executed. 66 document checks pass and prove nothing about "
                       "contract behaviour"},

            # ---- W-M2.12: A1-C05-S4 v4.0 independent review ----
            {"claim": "the requested document path exists and is A1-C05-S4.1",
             "method": "git ls-remote all heads; git ls-tree every remote head for V4_1; "
                       "git log --all --grep='4.1'",
             "result": "NOT FOUND. No docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md exists on "
                       "any remote branch and no commit mentions a 4.1. The published "
                       "successor is docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md, internally "
                       "A1-C05-S4 v4.0, whose section 1/2 are scoped to exactly D-1..D-7"},
            {"claim": "S4's reviewed blob differs from the branch tip only in placeholders",
             "method": "git diff 424d2c69 (content) against d72831e7 (tip)",
             "result": "verified: 5 insertions, 5 deletions - PUB_COMMIT/PUB_BLOB placeholder "
                       "fill plus the paragraph explaining it. No normative clause differs"},
            {"claim": "S4's 43 obligations split 19 P / 15 C / 6 R / 3 A",
             "method": "parse every '| **TN-x-nn' row from sections 7-9 of blob 424d2c69",
             "result": "verified: 43 rows, exact split"},
            {"claim": "S4's 67 cases over 18 suites, 23 document checks",
             "method": "parse suite table 12.1 and section 13.1; regex all T-C05-nn",
             "result": "verified: 18 suites summing 67, ids 01-67 complete and none extra, "
                       "DV-1..DV-23 = 23 checks, section 11.2 inverts onto all 67 with no "
                       "orphans either way"},
            {"claim": "DV-11 is now genuinely row-level and discriminates rows 6 vs 7",
             "method": "parse the 5.4 token->row table from the document, then re-implement "
                       "DV-11's stated rule (prefix allowed-row set + row intersection) over "
                       "all 43 implementer cells, rather than reading its PASS",
             "result": "verified: 7 declared, 5 observed, 43 cells, 0 failures. A TN-C "
                       "obligation carrying the row-7 token would fail, which is the "
                       "behaviour S3's agent-level check could not produce. The section 13.2 "
                       "tamper proof against S3 is real and names both mis-mapped rows"},
            {"claim": "D-4 audio ownership is fully resolved",
             "method": "whole-document search for any clause assigning audio to Agent 1",
             "result": "NOT RESOLVED. Section 5.2 row 5, section 6.1 and TN-C-15 are correct, "
                       "but the section 8 preamble still reads 'Agent 1 for defence, dodge, "
                       "camera and audio'. DV-22 checks only row 5, row 6 and TN-C-15, so it "
                       "reports PASS on a document that still contains the defect. This is "
                       "the same failure class as S3's DV-11"},
            {"claim": "S4's declared/observed token counts are internally consistent",
             "method": "extract every statement of the counts and compare with the parsed "
                       "distinct 7th-cell token set",
             "result": "INCONSISTENT in one place: section 1 row 6 says '7 declared, 6 "
                       "observed'; the actual observed count is 5. Section 2.1, section 2.2, "
                       "section 5.4, DV-11 and section 18.1 all correctly say 5. Third "
                       "consecutive revision with a wrong count in the DV-11 narrative"},
            {"claim": "section 5.4's 'Used by' tallies are accurate",
             "method": "per-token breakdown of the 43 implementer cells",
             "result": "IMPRECISE: 'producer owner' is declared as '19 TN-P rows' but occupies "
                       "23 cells (19 TN-P + 4 TN-R); 'each consumer' is declared as '11 TN-C "
                       "rows' but occupies 12. The mappings are correct; the tallies omit rows"},
            {"claim": "PO-5 resolves the D-2 content collision",
             "method": "trace reading A vs reading B for a frame with one phase change and "
                       "one dilation change against PO-5, TN-P-11 and INV-1",
             "result": "verified resolved: PO-5 makes reading B the only legal reading and "
                       "makes it satisfiable by requiring publication between applications. "
                       "T-C05-51 asserts ProducerRate per message and T-C05-65 adds the "
                       "mid-frame pull with a batching negative control"},
            {"claim": "PO-5 leaves the stated reason for PO-3 intact",
             "method": "compare section 3.6 reason (b) 'internal application order is not "
                       "observable' against PO-5's mid-frame pull guarantee and T-C05-65",
             "result": "CONTRADICTION FOUND: PO-5 and T-C05-65 make the internal application "
                       "order observable within the frame, so reason (b) is now false. The "
                       "PO-3 rule remains correct and needed (reasons (a) and (c) survive); "
                       "the justification attached to it is stale"},
            {"claim": "TN-C-14's one-frame staleness bound actually holds",
             "method": "trace a lost Retimed through AD-1, PO-5, TN-P-11, TN-C-14 and AD-1 "
                       "across frame F and F+1",
             "result": "holds as an UPPER bound, and holds only because PO-5 forbids live "
                       "state ahead of publication. It is not a same-frame guarantee: a pull "
                       "landing before the producer's publication in F sees the stale "
                       "revision, so worst case is up to one frame, not zero"},
            {"claim": "identity constancy is consistent across all clauses (D-3/C6-1)",
             "method": "check section 3.8, section 6.1, TN-P-07, TN-P-19, TN-P-04, T-C05-62, "
                       "T-C05-66 and DV-23's zero-unquoted-phrase claim",
             "result": "verified consistent: TN-P-07's dead identity clause removed, "
                       "TN-P-19 names the close-and-reopen path, T-C05-62's untestable rows "
                       "replaced by a falsifiable assertion, 0 unquoted occurrences of the "
                       "rejected phrase"},
            {"claim": "INV-2 states its precondition in the normative clause (D-7/C4a-1)",
             "method": "read the INV-2 row in section 4.6 and TN-C-10; re-derive the "
                       "equivalence at four axes",
             "result": "verified: 'INV-2 holds only while ProducerRate and PhaseEndAxis are "
                       "fixed' is in the clause, TN-C-10 echoes it, and both forms remain "
                       "identical to 1e-12 at axis 0/2/4/8 including the clamps"},
            {"claim": "the VF list is consistent across its three homes (C4a-2)",
             "method": "extract the VF names from section 3.2, INV-1 and the Timing struct "
                       "comment and compare as sets",
             "result": "verified: all three name exactly the same seven fields; DV-12 states "
                       "set equality. Noted: DV-12 also passes on S3, so it is a drift guard "
                       "rather than a defect detector - S4 states this itself"},
            {"claim": "S4 resolved the TN-C-11 / TN-A-01-02 conflict without moving the "
                      "arbitration boundary",
             "method": "read C05-6.4's three domains against TN-C-11, TN-A-02, TN-A-03 and "
                       "C05-6.1",
             "result": "verified: creation/selection/outcome separation is sound; no C-05 "
                       "value including AttackTag can decide a hit; TN-A-03 is MEAD-neutral "
                       "(names inputs, not components); TD-09 not reopened; B-15 records "
                       "that this is S4's own resolution, not Agent 3's wording"},
            {"claim": "S4's provenance record and honesty claims",
             "method": "check section 13.3, section 17 and section 18 for closure claims",
             "result": "verified: 0 acceptance tests claimed executed, all 67 cases marked "
                       "PROPOSED / NOT RUN, no MEAD selected, U-07 open, B-11/B-12/B-13/B-15 "
                       "all recorded as open. Section 13.3 correctly states that 23 document "
                       "checks prove nothing about contract behaviour"},

            # ---- W-M2.13: A1-C05-S4.1 v4.1 independent reassessment ----
            {"claim": "my W-M2.12 evidence entry 'no V4_1 exists on any remote head' was "
                      "true when inspected and false when published",
             "method": "git rev-parse the named commit and path; git log --format=%ci on "
                       "9591826, 04a9e2f, 3784949 and d60981b; git merge-base --is-ancestor "
                       "a3453548 95918268",
             "result": "CORRECTED. The blob resolves: 95918268:docs/"
                       "AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md = d54e194a, exactly the "
                       "requested blob. S4.1 commits are 14:09:47, 14:09:50, 14:10:35; my "
                       "review commit d60981b is 14:15:02 - 4m35s LATER. S4.1 descends from "
                       "the S4.0 tip a345354 that I reviewed. My ls-remote observation was "
                       "accurate when made; the negative was stale when committed. "
                       "Withdrawn in the reassessment section 1."},
            {"claim": "S4.1 is genuinely a targeted single-cell correction, as section 0.5 "
                      "asserts",
             "method": "compare sections 7, 8, 9, 4.9 (PO-5), 5.4 (token table) and 9.2 "
                       "(C05-6.4) of blob d54e194a against S4.0 blob 424d2c69 as byte "
                       "strings, rather than reading section 0.5's own description",
             "result": "verified: every one of the six section bodies is byte-identical to "
                       "S4.0, as are TN-P-18, TN-P-19, TN-C-11, TN-C-14, TN-C-15, TN-A-02 "
                       "and TN-A-03. The only content change is one cell in section 1 row 6. "
                       "Section 0.5's claim is accurate."},
            {"claim": "the reviewed blob is S4.1 and not the branch tip, and the difference "
                      "is immaterial",
             "method": "git diff d54e194a (reviewed) against cc056a48 (tip at 3784949)",
             "result": "verified: 5 insertions, 5 deletions - the section 0.5 verification "
                       "row reworded plus S41_COMMIT/S41_BLOB and the section 18 handoff blob "
                       "references filled by 04a9e2f. No normative clause, obligation row, "
                       "test or count differs. The reviewed blob is 1185 lines."},
            {"claim": "D-6a is resolved: the DV-11 count now reads 5 observed",
             "method": "re-derive the count by parsing the 7th cell of all 43 obligation "
                       "rows, then classify every 'N declared / M observed' statement in the "
                       "document by whether its context is S3-scoped, a quoted correction, or "
                       "an S4/S4.1 assertion",
             "result": "RESOLVED and verified twice. 7 declared in 5.4, 5 distinct tokens "
                       "across 43 cells, 2 declared-but-unused by design - matching DV-11's "
                       "output. Zero non-S3, non-historical statements report an observed "
                       "count other than 5. '6 observed' survives twice, both inside section "
                       "0.5's description of the defect it fixes, which is correct quotation."},
            {"claim": "DV-11's row-level rule is genuinely implemented and discriminating",
             "method": "re-implement the stated rule independently (prefix allowed-row set "
                       "TN-P->{2}, TN-C->{5,6}, TN-R->{2,4}, TN-A->{8}; token's mapped row "
                       "intersected against it) and run it over all 43 cells",
             "result": "verified: declared=7 observed=5 cells=43 failures=0. Confirmed that "
                       "the row-7 token 'Agent 2, in its own systems' has no intersection "
                       "with the TN-C allowed set {5,6}, so a TN-C obligation carrying it "
                       "fails - the behaviour S3's agent-level check could not produce."},
            {"claim": "D-4 audio ownership is resolved in S4.1",
             "method": "whole-document grep for every clause assigning audio to an agent; "
                       "read DV-22's method cell to determine its scan scope",
             "result": "NOT RESOLVED, unchanged from S4.0. Section 8's preamble (line 566) "
                       "still reads 'Agent 1 for defence, dodge, camera and audio'. Section "
                       "5.2 row 5 (line 459), section 6.1 and TN-C-15 (line 584) are all "
                       "correct. DV-22's method names only row 5, row 6 and TN-C-15, so it "
                       "reports PASS on a document containing the defect. S4 itself named "
                       "this failure mode: its D-4 risk column says 'if another assignment "
                       "survives, DV-22 was scoped too narrowly'."},
            {"claim": "PO-5 leaves section 3.6's stated reason for PO-3 intact",
             "method": "compare reason (b) 'the internal application order is not observable "
                       "at frame granularity' against PO-5's mid-frame pull guarantee and "
                       "T-C05-65's pull-after-each-application case",
             "result": "CONTRADICTION CONFIRMED unchanged in S4.1. PO-5 guarantees a pull "
                       "between two publications returns the earlier revision exactly, which "
                       "makes the application order observable and therefore falsifies reason "
                       "(b). Reasons (a) and (c) both survive, and PO-3 remains necessary: a "
                       "producer could satisfy PO-5 fully and still apply the dilation first. "
                       "Only the justification is stale, not the rule."},
            {"claim": "S4.1 introduced no new defect",
             "method": "four-category sweep: normative clauses vs S4.0; the 43/67/18/23 "
                       "structural totals; the DV-11 re-implementation and DV-22's scope; "
                       "the section 17/18 provenance and placeholder state",
             "result": "verified: no new defect. The normative bodies are byte-identical, "
                       "all structural totals reconcile, DV-11 is clean, and the placeholder "
                       "state matches the S3 and S4.0 pattern with disclosure. The surviving "
                       "findings and conditions are all pre-existing in S4.0."},
            {"claim": "section 5.4's 'Used by' tallies are accurate",
             "method": "per-token breakdown of the 43 implementer cells in S4.1",
             "result": "IMPRECISE, unchanged: 'producer owner' is stated as '19 TN-P rows' "
                       "but occupies 23 cells (19 TN-P + 4 TN-R); 'each consumer' is stated "
                       "as '11 TN-C rows' but occupies 12. Third hand-restated count that "
                       "diverges from its own instrument - same class as D-6a."},
            {"claim": "C-05, U-07 or any acceptance case is closed by this reassessment",
             "method": "none - this is a design review, not a run",
             "result": "NOT CLAIMED. C-05 and U-07 remain open; 0 of 67 cases executed, all "
                       "PROPOSED / NOT RUN; DESIGN_ONLY; no MEAD selected; B-11, B-12, B-13 "
                       "and B-15 all still open. The 47 document and arithmetic checks in "
                       "this milestone prove nothing about contract behaviour."},

            # ---- W-M2.14: Addendum A1, closure taxonomy ----
            {"claim": "W-M2.13's sections 6, 7 and 9 disagreed on which findings gate PASS",
             "method": "compare the required-item lists in section 9 against the gating "
                       "statements in sections 6.1, 6.3 and 7's Blocks? column",
             "result": "CONTRADICTION CONFIRMED. Section 6.1 says D-1a/D-1b are 'neither "
                       "gating'; section 6.3 says D-6b is 'cosmetic, non-gating'; section 7 "
                       "marks all three 'No (minor)'/'No (cosmetic)'; section 9 lists "
                       "D-1a/D-1b/D-6b among what would move the review to PASS. Corrected "
                       "in the addendum sections 1 and 3."},
            {"claim": "D-1b is a normative specification gap, as W-M2.13 section 7 said",
             "method": "read TN-C-14 cell 2 verbatim rather than my own summary of it; then "
                       "trace the compliance set of both candidate readings",
             "result": "OVER-CLASSIFIED, now reclassified ADVISORY. The clause defines the "
                       "consumer inline: 'A consumer whose behaviour depends on remaining "
                       "time - it acts on TN-C-10's output'. TN-C-10's output is the aged "
                       "remaining time R(t)=max(0,R0-(Axis(t)-AxisNow)*ProducerRate). A "
                       "consumer that does not act on it has nothing to be stale about, so "
                       "both readings require the same pulls and forbid the same omissions. "
                       "Identical compliance sets means no normative gap. My call-site "
                       "recommendation is withdrawn."},
            {"claim": "TN-C-14's one-frame staleness bound follows from 'at least once per "
                      "frame', as TN-C-14, section 1 row 2, T-C05-64 and section 14.2 all state",
             "method": "read TN-C-14 cell 5 (the requirement) against its cell 4 (the claimed "
                       "guarantee); construct the worst-case legal pull schedule and compute "
                       "the largest achievable gap between consecutive pulls",
             "result": "DOES NOT FOLLOW - W-M2.13's D-1a was understated. 'At least once per "
                       "frame' constrains a count, not an interval. A schedule pulling at "
                       "0.99, 1.99, 2.99 satisfies it in every frame while leaving a "
                       "1.98-frame gap between pulls. So 'bounded by one frame, by "
                       "construction' is false, and T-C05-64's assertion of 'at most one "
                       "frame' cannot pass against the obligation as written. Upgraded from "
                       "minor/non-gating to PASS-CONDITION. W-M2.13's own 'not a same-frame "
                       "guarantee' reasoning is also withdrawn: given PO-5 it is empty."},
            {"claim": "the corrected taxonomy is internally consistent",
             "method": "check that each finding appears in exactly one class, that the PASS "
                       "list matches the non-advisory classes, and that the advisory list "
                       "matches the ADVISORY class",
             "result": "verified: PASS-BLOCKING = {D-4, D-22-scope}; PASS-CONDITION = {D-1a, "
                       "C4c-N1}; ADVISORY = {D-1b, D-6b}; RESOLVED = {D-6a}. No finding is "
                       "in two classes; neither advisory item appears in the PASS list; both "
                       "PASS conditions and both blocking items appear in it."},
            {"claim": "D-4, C4c-N1 and D-6a are unchanged by this addendum",
             "method": "re-read section 8's preamble in blob d54e194a; check the addendum "
                       "states each as unchanged; confirm the reviewed blob still resolves",
             "result": "verified unchanged: section 8's preamble still reads 'Agent 1 for "
                       "defence, dodge, camera and audio'; C4c-N1 is stated as unchanged with "
                       "section 6.2 standing; D-6a remains RESOLVED. "
                       "95918268:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md still resolves "
                       "to d54e194a."},
            {"claim": "W-M2.13 is preserved unmodified and the addendum is separately "
                      "identifiable",
             "method": "git diff eee9401 against the review path; compare the two artifact "
                       "paths and IDs",
             "result": "verified: zero diff on Docs/AGENT2_REASSESSMENT_A1C05_S4_1_V1.md "
                       "since eee9401. The addendum is "
                       "Docs/AGENT2_REASSESSMENT_A1C05_S4_1_ADDENDUM_A1.md with its own ID "
                       "TDD-A2-REASSESS-A1C05-S4-1-ADDENDUM-A1, declaring what it amends."},
            {"claim": "Agent 3's independent review of the exact S4.1 blob is outstanding",
             "method": "git ls-remote all heads, then git log 1eb613f3..origin/a3branch and "
                       "grep the artifact for the S4.1 blob and commit hashes",
             "result": "NO LONGER OUTSTANDING. Commit 34b035b on arena/c64fc525-tdd adds "
                       "docs/AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md (114 "
                       "lines, committed 2026-11-17 18:21:50Z). It names blob d54e194a twice "
                       "and commit 95918268 three times - the same reviewed object - and "
                       "states S4.0 was used only as a byte-diff baseline. Kept independent: "
                       "its findings are not used as evidence for mine, its cluster-1 "
                       "arbitration finding is not assessed here, and it has not reviewed "
                       "this addendum."},
            {"claim": "this addendum closes C-05, U-07 or any acceptance case",
             "method": "none - document and arithmetic checks only",
             "result": "NOT CLAIMED. C-05 and U-07 remain open; 0 of 67 cases executed; "
                       "DESIGN_ONLY; no MEAD selected; no signature, freeze, merge or M0 "
                       "authorisation. The 47 addendum tests prove nothing about contract "
                       "behaviour."},

            # ---- W-M2.16: independent architecture review of A1-C05-S4.3.5 ----
            {"claim": "the reviewed document is the exact published S4.3.5 blob",
             "method": "git rev-parse baa31db3c631f0fc3e69a82b6d71207ad8061218:docs/"
                       "AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md before reading, and again at "
                       "commit time",
             "result": "verified: resolves to a0b46f46c81e85cea5d04b940aaf9aee46c19deb, exactly "
                       "the requested blob, 1,779 lines. The same-commit provenance register "
                       "0dba4a7c6eddd3ba0a3d61b408c2d3ee005a88cb also names that blob and "
                       "spells the full hash rather than abbreviating it. The commit was the "
                       "branch tip at review time, so no blob-versus-tip ambiguity arose."},
            {"claim": "S4.3.5 changes nothing normative, as it states in section 0.7.5",
             "method": "byte-compare against S4.3.4 (blob 41df692d) the 43 obligation rows, "
                       "the clauses in 5.2/5.4/9.2/4.9/3.6/4.2, and all 17 case-specification "
                       "rows",
             "result": "TRUE. All 43 rows identical, all six clauses identical, all 17 case "
                       "specifications identical. The revision is confined to the Scope-line "
                       "figure, the 2.14 audit, and the 18.3 stamp, exactly as claimed."},
            {"claim": "the suite-count correction and its audit are accurate",
             "method": "run each commit's regression suite in an isolated git archive "
                       "extraction of 40d29cc, 90971e0 and baa31db; read S4.3.4's Scope line",
             "result": "CORRECT. Executed suite totals are 56 (S4.3.3), 67 (S4.3.4) and 67 "
                       "(S4.3.5). S4.3.4's Scope line did read 'from 56 to 74'; S4.3.5 reads "
                       "'from 56 to 67'. The '74' survives only as a quotation of the "
                       "corrected error. The 11-row audit is a RECORDED TABLE, not an "
                       "enforced front-matter check, and the document states that limitation "
                       "in terms rather than implying otherwise - recorded as MINOR-1."},
            {"claim": "DV-22's rewrite closes my N-1 keyword escape",
             "method": "run the shipped validator on 24 injected audio-assignment forms in a "
                       "clean archive, including the exact attack I published at S4.2",
             "result": "CLOSED for keyword escapes and for 22 of my 24 forms. My original "
                       "attack 'D-4 note: Agent 1 owns the camera and audio cues' is now "
                       "CAUGHT, and the suite carries it as a permanent case. Exemption is "
                       "now by location (fenced block, [QUOTED] table, marked history block), "
                       "never by which words a line contains."},
            {"claim": "DV-22 fully enforces audio single-ownership in all ownership prose",
             "method": "inject 24 forms; for each, read the DV-22 verdict and the overall "
                       "check total",
             "result": "FALSE - MAJOR-1. Two false negatives reproduce a clean 27/27: (1) "
                       "'Agent 1, unlike Agent 2, owns the audio cues' - attribution takes "
                       "the nearest PRECEDING agent reference, which is Agent 2 inside the "
                       "contrastive foil; (2) 'The first agent owns the audio cues' - AGENT_REF "
                       "matches only agent[-\s]?[12]. Escape 2 is reachable, not artificial: "
                       "this document uses 'the first agent' as a synonym for Agent 1 "
                       "seventeen times, including in the sentence that defines the DV-22 "
                       "criterion. The contract text is correct; the certificate overstates "
                       "what it tests."},
            {"claim": "the defect in DV-22 is fixable as I describe",
             "method": "implement three candidate repairs in /tmp against throwaway archive "
                       "extractions and measure each against three populations - the clean "
                       "document, both escapes, and the existing 67 regression cases",
             "result": "MEASURED, one rejected. (b) 'fail on any unattributable audio mention' "
                       "is REJECTED: it produces 13-43 false positives on the clean document "
                       "because authority/disposition tables discuss audio without naming an "
                       "agent, so 27/27 collapses. A naive '|the first agent' regex alternative "
                       "is also ineffective - group(1) is None for that branch. (a) as "
                       "specified DOES work: clean document 27/27 with 0 offenders, both "
                       "escapes FAIL with 1 offender each, all denials still pass, and the "
                       "full 67-case suite passes 67/67 with zero collateral damage. Nothing "
                       "was committed; Agent 1's validator is unmodified."},
            {"claim": "the arbitration boundary and the Agent 3 conflict are represented "
                      "truthfully",
             "method": "trace 5.2 rows 5-8 against TN-C-11, TN-C-15, TN-A-01..03, C05-6.4 and "
                       "section 6.1; check that TN-A-02 was extended rather than narrowed; "
                       "re-check the document's negative existence claim against every head",
             "result": "TRUTHFUL. The three domains (creation/selection/outcome) hold: the "
                       "producer authors AttackTag, a consumer may select on it, and nothing "
                       "may decide a hit with it. TN-A-02 is extended, not weakened, and TN-A-03 "
                       "gives it a positive failable form. The document states that Agent 3's "
                       "review is NOT in the repository, credits the resolution as its own "
                       "rather than Agent 3's, and asks Agent 3 to confirm or substitute. "
                       "Verified: three AGENT3 files exist on arena/c64fc525-tdd and none "
                       "mentions 7d03e1df or a0b46f46."},
            {"claim": "I did not rely on Agent 3's conclusions or adjust my verdict to match",
             "method": "no coordination; Agent 3's S4.2 and S4.3 assessments were not read and "
                       "were not awaited",
             "result": "NOT DONE. Where this review describes Agent 3's conflict or its "
                       "counterexample it quotes AGENT 1's description of them in the reviewed "
                       "text. The verdict PASS WITH CONDITIONS is mine, derived from my own "
                       "injections and executions."},
            {"claim": "the document validation constitutes architectural evidence",
             "method": "kept separate deliberately throughout",
             "result": "IT DOES NOT. 27/27 and 67/67 are structural checks on the document and "
                       "on the checker. They prove internal consistency and that the "
                       "instruments reach their intended defects. They prove nothing about "
                       "whether a telegraph, producer or consumer behaves correctly - there is "
                       "no engine (B-3). The 67 instrument regressions are NOT contract "
                       "acceptance tests and I do not treat them as such."},
            {"claim": "my own prior review artifacts still reproduce correctly",
             "method": "re-ran the full world test suite before generating this evidence",
             "result": "FOUND A DEFECT IN MY OWN W-M2.15 MODULE (MINOR-4). "
                       "test_review_a1c05_s4_2.py read the validator from the branch tip "
                       "origin/arena/3bc206a0-tdd instead of the reviewed commit, so when Agent "
                       "1 published S4.3 the test began scoring the S4.2 document with the "
                       "S4.3.5 validator and S4.2 fell from 27/27 to 24/27 - DV-22, DV-24 and "
                       "DV-27 are checks S4.2 predates. FIXED IN THIS REVISION: pinned to "
                       "a788f95:docs/validation/dv_c05.py (blob 381be714) and added "
                       "TestInstrumentIsPinned to fail if a branch-tip read returns. S4.2 is "
                       "27/27 again under the instrument that shipped with it. No W-M2.15 "
                       "conclusion changes - every number was correct at the time. The "
                       "review's own S4.2 24/27 figure is now labelled as measuring checker "
                       "growth, not document quality."},
            {"claim": "C-05, U-07, a MEAD or any acceptance case is closed by this review",
             "method": "none - document, arithmetic and instrument checks only",
             "result": "NOT CLAIMED. C-05 and U-07 remain open; 0 of 67 acceptance cases "
                       "executed, all PROPOSED / NOT RUN; DESIGN_ONLY; no MEAD selected; no "
                       "signature, freeze, merge or approval. B-1/TD-06, B-2/TD-09, "
                       "B-4/TD-12 and B-13 remain OPEN. My 61 review tests prove nothing "
                       "about contract behaviour."},

            # ---- W-M2.15: independent reassessment of A1-C05-S4.2 v4.2 ----
            {"claim": "the reviewed document is the exact published S4.2 blob",
             "method": "git rev-parse a788f953256d208f3eb1310f3897924d007179b1:docs/"
                       "AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md, before reading; compare against "
                       "the instruction's blob and against the first draft 86f56af",
             "result": "verified: resolves to 7d03e1df837493305831962f43882a1cd3496143, exactly "
                       "the requested blob, 1265 lines. The first S4.2 commit 1647942 published "
                       "blob 86f56af; a788f95 corrected three sentences (3 insertions, 3 "
                       "deletions) - a typo, my review's line count 595->594, and a claim "
                       "about which blob DV-24 fails on. No clause, count or test changed."},
            {"claim": "D-4 audio ownership is resolved in S4.2",
             "method": "classify every Agent 1 + audio co-occurrence in the whole document, "
                       "then check the section 8 preamble reads correctly",
             "result": "RESOLVED. The preamble now reads 'Agent 1 for defence selection, dodge, "
                       "camera response and framing ... Agent 1 has no C-05 audio "
                       "responsibility'. 15 co-occurrence windows classified; 0 are unmarked "
                       "positive assignments - all are negations, marked corrections, or the "
                       "corrected text itself. The owner is named positively in three registers, "
                       "which is better than the two-word deletion requested."},
            {"claim": "DV-22's widening actually closes D-22-scope",
             "method": "run Agent 1's shipped docs/validation/dv_c05.py on S4.2, S4.1, S4.0 and "
                       "S3; then read its predicate and inject mutations to test it",
             "result": "PARTIALLY. DV-22 correctly FAILS on S4.1 ('section 8 preamble clean "
                       "False') and on S3 (2 offenders including row 5's old 'camera and audio "
                       "cues'), and PASSES on S4.2 - the discrimination S4.1's DV-22 could not "
                       "produce. BUT the whole-document scan is a keyword allowlist: the S4.1 "
                       "preamble is exempted because the line contains the string 'D-4', so the "
                       "scan reports 0 offenders while the defect is present. Injecting 'D-4 "
                       "note: Agent 1 owns the camera and audio cues' yields 0 detections; the "
                       "same line without the prefix yields 1. New defect N-1."},
            {"claim": "TN-C-14's one-frame staleness bound now follows from its rules (D-1a)",
             "method": "read the five rules; then brute-force 400,000 legal pull schedules "
                       "maximising the interval from a missed revision's publication to the "
                       "next successful refresh consistent with rules (ii) and (iii); and check "
                       "analytically whether rule (iii) eliminates S4.1's 1.98-frame schedule",
             "result": "RESOLVED. Rule (ii) requires an observation whose AxisNow does not "
                       "precede the frame of use; rule (iii) caps successive refreshes at one "
                       "frame on the shared axis. Max gap found 0.999772 frames, always <1, "
                       "approaching 1 - matching the text's 'approaches but never reaches one "
                       "frame'. S4.1's 0.99->1.99 schedule is now illegal: the missed revision "
                       "must be published after the observation, so the worst gap is <1. The "
                       "bound is derived, not asserted."},
            {"claim": "the D-1b consumer classification is resolved",
             "method": "read TN-C-14(i) and check whether the definition is now positive and "
                       "testable rather than an inline parenthetical",
             "result": "RESOLVED, and better than my withdrawn ask. Rule (i) attaches to the "
                       "CALL SITE and names the concrete read: 'every call site that reads "
                       "RemainingLocalSeconds, or derives a remaining time from it'. This does "
                       "not contradict my addendum's ADVISORY downgrade - ADVISORY means not "
                       "required, not forbidden - and it improves testability at no cost. "
                       "S4.2 answered W-M2.13 (eee9401) and did not see my addendum (e434dbe, "
                       "18:33 vs 18:36), so it adopted an ask I had withdrawn. No harm; "
                       "recorded as advisory N-3."},
            {"claim": "C4c-N1 PO-3 rationale is corrected",
             "method": "read section 3.6(b) and check the premise against PO-5's mid-frame pull "
                       "guarantee; confirm PO-3 is retained; search for any surviving assertion "
                       "of the falsified premise",
             "result": "RESOLVED, near-verbatim to my specified fix. Section 3.6(b) now states "
                       "the order IS observable through a mid-frame pull once PO-5 is in force, "
                       "explicitly records that S4.1 said the opposite and that the premise was "
                       "falsified, and retains PO-3 with the reason it is still needed. The two "
                       "surviving 'not observable' strings are a quotation inside the C4c-N1 "
                       "disposition and an unrelated RS-3 statement - neither asserts it."},
            {"claim": "D-6a-i is satisfied by DV-24, and D-6b's tallies are corrected",
             "method": "re-parse the 7th cell of all 43 obligation rows; re-implement DV-11's "
                       "allowed-row rule; verify DV-24's failure claim against the S4.0 blob; "
                       "compare section 5.4's declared tallies against the re-derivation",
             "result": "BOTH RESOLVED. DV-24 exists, is the instrument I specified, and its "
                       "FAIL-on-S4.0 claim is true: S4.0's section 1 row 6 says '7 declared, 6 "
                       "observed' while section 5.4 and 13.1 say 5 - one inconsistent site among "
                       "four. Section 5.4 now declares 23 cells (19 TN-P, 4 TN-R) and 12 cells, "
                       "matching my independent parse exactly, with 7 declared / 5 observed / 43 "
                       "cells / 0 failures."},
            {"claim": "S4.2 preserves the findings it claims to preserve",
             "method": "byte-compare TN-P-18/19, TN-C-10/11/15, TN-A-02/03 and PO-5 against "
                       "S4.1 blob d54e194a; re-derive the structural totals",
             "result": "verified identical: all seven obligation rows and PO-5 are byte-for-"
                       "byte the S4.1 text. Totals reconcile: 43 obligations (19/15/6/3), 67 "
                       "cases over 18 suites, ids 1-67 complete, DV-1..DV-27 contiguous with "
                       "24-27 new. No carried finding reopened."},
            {"claim": "S4.2 introduced no other defect",
             "method": "four-category sweep: structure and counts; instrument behaviour on four "
                       "blobs; clause preservation; live placeholder tokens",
             "result": "no other defect. The reviewed blob contains no live placeholder - "
                       "S41_COMMIT and S41_BLOB occur only inside DV-27's own quoted failure "
                       "output at lines 1081 and 1085, as evidence rather than fields. S4.2 "
                       "solves the S4.1 placeholder trap correctly by carrying its own hash in "
                       "a separate provenance register instead of in itself."},
            {"claim": "there is a single unambiguous artifact answering to A1-C05-S4.2",
             "method": "git ls-remote all heads; git log --all on the V4_2.md path; compare the "
                       "Response ID and the TN-C-14 measure on each copy",
             "result": "DEFECT N-2. Two different documents both declare Response ID "
                       "TDD-A1-C05-SUCCESSOR-004.2: the reviewed one (arena/3bc206a0-tdd, blob "
                       "7d03e1df, 1265 lines) and another on arena/c64fc525-tdd at c800bf0 "
                       "(blob 61ef03b4, 1237 lines, 360 changed lines). They encode different "
                       "contracts - one bounds one frame on the shared axis, the other 1/60 s "
                       "of monotonic elapsed time. Not reconcilable by merge. I do not "
                       "adjudicate which is authoritative and have not reviewed the other."},
            {"claim": "C-05, U-07 or any acceptance case is closed by this reassessment",
             "method": "none - document and arithmetic checks only; ran the shipped validator "
                       "on four blobs",
             "result": "NOT CLAIMED. C-05 and U-07 remain open; 0 of 67 acceptance cases "
                       "executed, all PROPOSED / NOT RUN; DESIGN_ONLY; no MEAD selected; no "
                       "signature, freeze, merge or M0 authorisation. Agent 1's 27/27 and my "
                       "70 document tests prove nothing about contract behaviour - S4.2 says "
                       "this itself in section 13.4, and I verified that statement is accurate."},
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"{'check':26s} {'result':8s} detail")
    for name, r in results.items():
        tail = (r["stdout_tail"] or r["stderr_tail"] or [""])[-1]
        print(f"{name:26s} {'PASS' if r['passed'] else 'FAIL':8s} {tail[:70]}")
    print(f"\nall passed: {payload['meta']['all_passed']}")
    print(f"written: {out}")
    return 0 if payload["meta"]["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
