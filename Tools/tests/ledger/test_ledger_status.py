#!/usr/bin/env python3
"""Regression tests for ledger_update.py status logic (fixed 2026-11-20).

A failed build, failed automation run, missing test results, or incomplete
verification must never produce GREEN. Each case builds a temp evidence dir
and a temp ledger, runs ledger_update.py as the real CLI, and asserts the
resulting status.

Run via run_ledger_tests.sh (emits TDD_RESULT lines).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LEDGER_UPDATE = REPO / "Tools/engine/ledger_update.py"
RUN_LOG_HEADING = "## Run log"
LEDGER_TEMPLATE = (
    "# Quality Ledger\n\n"
    f"{RUN_LOG_HEADING}\n\n"
    "| UTC | Train | Platform | Commit | Pure | UE | Status | Evidence |\n"
    "|---|---|---|---|---:|---|---|---|\n"
)


def run_ledger(evidence: Path, ledger: Path, mac_result=None):
    """Run ledger_update.py; return (returncode, status, stderr)."""
    cmd = [
        sys.executable, str(LEDGER_UPDATE),
        "--evidence-dir", str(evidence),
        "--platform", "mac",
        "--train", "daily",
        "--commit", "deadbeefc0ffee",
        "--ledger", str(ledger),
    ]
    if mac_result is not None:
        cmd += ["--mac-build-result", mac_result]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    status = None
    for line in proc.stderr.splitlines():
        if line.startswith("# ledger status="):
            status = line.split("=", 1)[1].split(" ", 1)[0]
    return proc.returncode, status, proc.stderr


def write_pure(evidence: Path, passed=6, failed=0):
    lines = [f"TDD_RESULT TDD-Pure.Suite{i} PASS {passed}/{passed} assertions passed"
             for i in range(passed)]
    lines += [f"TDD_RESULT TDD-Pure.SuiteF{i} FAIL reason=x" for i in range(failed)]
    (evidence / "10-pure-results.txt").write_text("\n".join(lines) + "\n")


def write_ue_log(evidence: Path, passed=6, failed=0, executed=True):
    name = "20-mac-build-train.log"
    body = ""
    if executed:
        body = f"  exit=0  tests discovered={passed} passed={passed} failed={failed}\n"
    elif passed == 0 and failed == 0 and not executed:
        body = "NOT EXECUTED\n"
    (evidence / name).write_text(body)


def write_build_log(evidence: Path, ok=True):
    verdict = "RESULT: BUILD AND TESTS OK" if ok else "RESULT: FAILED"
    (evidence / "20-mac-build-train.log").write_text(verdict + "\n")


def case(name, mutate, expected_status, mac_result=None, use_build_log=False):
    tmp = Path(tempfile.mkdtemp())
    try:
        evidence = tmp / "evidence"
        evidence.mkdir()
        ledger = tmp / "ledger.md"
        ledger.write_text(LEDGER_TEMPLATE)
        # default: healthy pure + healthy UE
        write_pure(evidence, 6, 0)
        if use_build_log:
            write_build_log(evidence, ok=(mac_result == "ok"))
        else:
            write_ue_log(evidence, 6, 0, True)
        mutate(evidence)
        rc, status, err = run_ledger(evidence, ledger, mac_result)
        if status is None:
            print(f"  {name}: FAIL (no status parsed; rc={rc})\n{err}", file=sys.stderr)
            return False
        if status != expected_status:
            print(f"  {name}: FAIL (expected {expected_status}, got {status})",
                  file=sys.stderr)
            return False
        print(f"  {name}: {status}")
        return True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    # (name, mutate, expected_status, mac_result, use_build_log)
    cases = [
        # --- GREEN case ---
        ("green_full", lambda e: None, "GREEN", "ok", False),
        # --- failed build (explicit) ---
        ("failed_build_explicit", lambda e: write_ue_log(e, 0, 0, True),
         "RED", "failed", False),
        # --- failed build (inferred from log, no explicit arg) ---
        ("failed_build_inferred", lambda e: write_ue_log(e, 0, 0, True),
         "RED", None, True),
        # --- failed automation run (UE failed>0) ---
        ("failed_automation", lambda e: write_ue_log(e, 4, 2, True),
         "RED", "ok", False),
        # --- missing pure results (0 pure) ---
        ("missing_pure", lambda e: write_pure(e, 0, 0),
         "RED", "ok", False),
        # --- pure failure ---
        ("pure_failure", lambda e: write_pure(e, 5, 1),
         "RED", "ok", False),
        # --- UE NOT EXECUTED ---
        ("ue_not_executed",
         lambda e: (e / "20-mac-build-train.log").write_text("NOT EXECUTED\n"),
         "RED", "ok", False),
        # --- UE ran zero tests (incomplete verification) ---
        ("ue_zero_tests", lambda e: write_ue_log(e, 0, 0, True),
         "RED", "ok", False),
        # --- no UE step at all ---
        ("no_ue_step",
         lambda e: (e / "20-mac-build-train.log").unlink(),
         "RED", "ok", False),
        # --- mac result unknown (no signal) ---
        ("mac_result_unknown",
         lambda e: (e / "20-mac-build-train.log").write_text("some unclassified output\n"),
         "RED", None, False),
    ]

    # For inferred cases, the build log must say FAILED.
    def _infer_failed(e):
        write_ue_log(e, 0, 0, True)
        write_build_log(e, ok=False)
    for i, c in enumerate(cases):
        if c[0] == "failed_build_inferred":
            cases[i] = (c[0], _infer_failed, c[2], c[3], c[4])

    passed = 0
    failed = 0
    for name, mutate, expected, mac, use_bl in cases:
        if case(name, mutate, expected, mac_result=mac, use_build_log=use_bl):
            passed += 1
        else:
            failed += 1

    print(f"TDD_RESULT TDD-Tool.LedgerStatusTests "
          f"{'PASS' if failed == 0 else 'FAIL'} "
          f"{passed}/{passed + failed} assertions passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
