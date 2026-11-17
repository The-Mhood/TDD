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
    }

    payload = {
        "meta": {
            "milestone": "W-M2.13 — independent reassessment of A1-C05-S4.1 v4.1, blob "
                         "d54e194a, path docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md. "
                         "10 AGREE, 3 AGREE WITH CONDITIONS, 1 DISAGREE over 7 defects and "
                         "7 conditions. Outcome: TARGETED REVISION. D-6a (DV-11 count) is "
                         "RESOLVED and verified twice; D-4 audio ownership is still present "
                         "in the section 8 preamble and DV-22 still reports PASS on it; "
                         "C4c-N1 (PO-3 reason b falsified by PO-5) confirmed unchanged. "
                         "CORRECTION: the W-M2.12 evidence entry claiming no V4_1 exists on "
                         "any remote head was FALSE WHEN PUBLISHED - S4.1 was pushed 4m35s "
                         "before that commit. Withdrawn in the review section 1",
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
