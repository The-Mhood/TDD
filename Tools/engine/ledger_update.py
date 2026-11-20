#!/usr/bin/env python3
"""Append a run row to the quality ledger from an evidence directory.

Counts TDD_RESULT lines (pure core) and UE automation counts (from the
mac_build.sh train log or the parser) and appends one markdown row to the
ledger's "## Run log" table. Never rewrites history — append-only.

Status semantics (fixed 2026-11-20): GREEN requires ALL of:
  - pure core has at least one result AND zero failures,
  - the mac build result is explicitly "ok",
  - the UE automation step actually executed,
  - UE automation reported zero failures,
  - UE automation actually ran at least one test.

A failed build, failed automation run, missing test results, or incomplete
verification is RED — never GREEN. A missing/unknown build result is RED.

Usage:
  ledger_update.py --evidence-dir DIR --platform mac --train daily
                   --commit HASH --ledger PATH [--mac-build-result ok|failed|not-executed]
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

RUN_LOG_HEADING = "## Run log"
VALID_MAC_RESULTS = {"ok", "failed", "not-executed"}


def count_tdd_results(evidence: Path) -> tuple[int, int]:
    passed = failed = 0
    for p in evidence.rglob("*.txt"):
        try:
            text = p.read_text("utf-8", errors="replace")
        except OSError:
            continue
        for line in text.splitlines():
            if line.startswith("TDD_RESULT"):
                if " FAIL" in line:
                    failed += 1
                elif " PASS" in line:
                    passed += 1
    return passed, failed


def count_ue_train(evidence: Path) -> tuple[str, int, int, bool]:
    """Return (display, passed, failed, executed).

    executed is True only when a real ``passed=N failed=M`` line was parsed
    from a UE log. "NOT EXECUTED" or no UE log yields executed=False.
    """
    for log in ("20-mac-build-train.log", "03-automation-TDD.log"):
        p = evidence / log
        if not p.exists():
            continue
        text = p.read_text("utf-8", errors="replace")
        if "NOT EXECUTED" in text:
            return ("NOT EXECUTED", 0, 0, False)
        m = re.findall(r"passed=(\d+)\s+failed=(\d+)", text)
        if m:
            passed, failed = int(m[-1][0]), int(m[-1][1])
            return (f"{passed}/{failed} pass/fail", passed, failed, True)
    return ("no UE step", 0, 0, False)


def infer_mac_result(evidence: Path) -> str:
    """Infer the mac build result from the train log when not passed explicitly."""
    p = evidence / "20-mac-build-train.log"
    if not p.exists():
        return "unknown"
    text = p.read_text("utf-8", errors="replace")
    if "RESULT: BUILD AND TESTS OK" in text:
        return "ok"
    if "RESULT: FAILED" in text:
        return "failed"
    if "NOT EXECUTED" in text:
        return "not-executed"
    return "unknown"


def decide_status(
    p_pass: int, p_fail: int,
    ue_display: str, ue_passed: int, ue_failed: int, ue_executed: bool,
    mac_result: str,
) -> tuple[str, str]:
    """Return (status, reason). GREEN only when every condition holds."""
    if p_fail > 0:
        return ("RED", f"pure failures ({p_fail})")
    if p_pass == 0:
        return ("RED", "no pure test results")
    if mac_result != "ok":
        return ("RED", f"mac build not ok ({mac_result})")
    if not ue_executed:
        return ("RED", "UE step not executed")
    if ue_failed > 0:
        return ("RED", f"UE automation failures ({ue_failed})")
    if ue_passed == 0:
        return ("RED", "UE ran zero tests (incomplete verification)")
    return ("GREEN", "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", required=True)
    ap.add_argument("--platform", required=True)
    ap.add_argument("--train", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--mac-build-result", choices=sorted(VALID_MAC_RESULTS),
                    default=None,
                    help="Explicit mac_build.sh result; inferred from the train "
                         "log when omitted. 'unknown' (no signal) is treated as not-ok.")
    args = ap.parse_args()

    evidence = Path(args.evidence_dir)
    if not evidence.exists():
        print(f"error: evidence dir missing: {evidence}", file=sys.stderr)
        return 1

    p_pass, p_fail = count_tdd_results(evidence)
    ue_display, ue_passed, ue_failed, ue_executed = count_ue_train(evidence)
    mac_result = args.mac_build_result or infer_mac_result(evidence)
    if mac_result not in VALID_MAC_RESULTS:
        mac_result = "unknown"

    status, reason = decide_status(
        p_pass, p_fail, ue_display, ue_passed, ue_failed, ue_executed, mac_result,
    )

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    ue_cell = ue_display
    if status == "RED" and reason and ue_display not in ("NOT EXECUTED", "no UE step"):
        ue_cell = f"{ue_display} ({reason})"
    elif status == "RED" and reason:
        ue_cell = f"{ue_display} ({reason})"
    row = (
        f"| {ts} | {args.train} | {args.platform} | `{args.commit[:9]}` | "
        f"{p_pass}/{p_pass + p_fail} | {ue_cell} | {status} | {evidence.name} |"
    )
    note = f" — {reason}" if reason else ""
    print(row)
    print(f"# ledger status={status}{note}", file=sys.stderr)

    ledger = Path(args.ledger)
    if not ledger.exists():
        print(f"error: ledger missing: {ledger}", file=sys.stderr)
        return 1
    text = ledger.read_text("utf-8")
    if RUN_LOG_HEADING not in text:
        print(f"error: '{RUN_LOG_HEADING}' heading not found in ledger", file=sys.stderr)
        return 1

    lines = text.splitlines()
    h = lines.index(RUN_LOG_HEADING)
    last_table = None
    for i in range(h + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        if lines[i].startswith("|"):
            last_table = i
    if last_table is None:
        print("error: no run-log table under heading", file=sys.stderr)
        return 1
    lines.insert(last_table + 1, row)
    ledger.write_text("\n".join(lines) + "\n", "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
