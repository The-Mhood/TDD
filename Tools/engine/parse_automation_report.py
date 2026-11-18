#!/usr/bin/env python3
"""Count discovered, started, passed, and failed Unreal automation tests.

The Unreal report is authoritative for terminal test states; the automation log
is used for discovery and start events. Some UE versions write a UTF-8 BOM in
index.json, so the report is read with utf-8-sig.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DISCOVERED_RE = re.compile(r"Found\s+(\d+)\s+automation tests?\s+based on\b", re.IGNORECASE)
STARTED_RE = re.compile(r"LogAutomationController:\s*Test Started(?:\b|[.:])", re.IGNORECASE)
PASSED_LOG_RE = re.compile(r"Result=\{(?:Passed|Success)\}", re.IGNORECASE)
FAILED_LOG_RE = re.compile(r"Result=\{(?:Failed|Fail|Error|Aborted)\}", re.IGNORECASE)


def test_items(data: Any) -> list[dict[str, Any]]:
    """Read test entries from the standard UE index or a keyed test mapping."""
    tests = data.get("tests", []) if isinstance(data, dict) else []
    if isinstance(tests, dict):
        tests = list(tests.values())
    if not isinstance(tests, list):
        raise ValueError("automation report 'tests' field must be a list or object")
    if not all(isinstance(item, dict) for item in tests):
        raise ValueError("automation report contains a non-object test entry")
    return tests


def outcome(test: dict[str, Any]) -> str:
    state = test.get("state", test.get("result", ""))
    if not state and test.get("succeeded") is True:
        state = "success"
    elif not state and test.get("succeeded") is False:
        state = "failed"
    normalized = re.sub(r"[^a-z]", "", str(state).lower())
    if normalized in {"success", "succeeded", "passed", "pass"}:
        return "passed"
    if normalized in {"fail", "failed", "failure", "error", "aborted", "cancelled", "canceled"}:
        return "failed"
    return "unclassified"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, help="Unreal automation-report/index.json")
    parser.add_argument("--log", required=True, type=Path, help="Unreal automation log")
    args = parser.parse_args()

    try:
        log_text = args.log.read_text(encoding="utf-8", errors="replace")
        report_tests: list[dict[str, Any]] = []
        if args.report and args.report.is_file():
            with args.report.open("r", encoding="utf-8-sig") as report_file:
                report_tests = test_items(json.load(report_file))

        discovered_matches = DISCOVERED_RE.findall(log_text)
        discovered = int(discovered_matches[-1]) if discovered_matches else len(report_tests)
        started = len(STARTED_RE.findall(log_text))

        states = [outcome(test) for test in report_tests]
        report_passed = states.count("passed")
        report_failed = states.count("failed")
        report_classified = report_passed + report_failed

        # If the JSON has terminal states, use it. Otherwise fall back to the
        # test-result events in the log; an all-unknown report is not treated as
        # an all-failed report or as a successful run.
        if report_classified:
            passed, failed = report_passed, report_failed
            unclassified = states.count("unclassified")
        else:
            passed = len(PASSED_LOG_RE.findall(log_text))
            failed = len(FAILED_LOG_RE.findall(log_text))
            unclassified = max(0, started - passed - failed)

        print(f"{discovered}\t{started}\t{passed}\t{failed}\t{unclassified}")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"automation report parsing failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
