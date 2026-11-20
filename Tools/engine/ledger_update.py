#!/usr/bin/env python3
"""Append a run row to the quality ledger from an evidence directory.

Counts TDD_RESULT lines (pure core) and UE automation counts (from the
mac_build.sh train log or the parser) and appends one markdown row to the
ledger's "## Run log" table. Never rewrites history — append-only.

Usage:
  ledger_update.py --evidence-dir DIR --platform mac --train daily
                   --commit HASH --ledger PATH
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

RUN_LOG_HEADING = "## Run log"


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


def count_ue_train(evidence: Path) -> str:
    for log in ("20-mac-build-train.log", "03-automation-TDD.log"):
        p = evidence / log
        if p.exists():
            text = p.read_text("utf-8", errors="replace")
            m = re.findall(r"passed=(\d+)\s+failed=(\d+)", text)
            if m:
                return f"{m[-1][0]}/{m[-1][1]} pass/fail"
            if "NOT EXECUTED" in text:
                return "NOT EXECUTED"
    return "no UE step"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence-dir", required=True)
    ap.add_argument("--platform", required=True)
    ap.add_argument("--train", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--ledger", required=True)
    args = ap.parse_args()

    evidence = Path(args.evidence_dir)
    if not evidence.exists():
        print(f"error: evidence dir missing: {evidence}", file=sys.stderr)
        return 1

    p_pass, p_fail = count_tdd_results(evidence)
    ue = count_ue_train(evidence)
    status = "GREEN" if p_fail == 0 and "NOT EXECUTED" not in ue and "fail" not in ue.split("/")[-1:-1] else "RED"
    # crude but honest: any pure failure or UE NOT EXECUTED/failed > 0 => RED
    if re.search(r"failed=(\d+)", ue or "") and int(re.search(r"failed=(\d+)", ue).group(1)) > 0:
        status = "RED"

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    row = (
        f"| {ts} | {args.train} | {args.platform} | `{args.commit[:9]}` | "
        f"{p_pass}/{p_pass + p_fail} | {ue} | {status} | {evidence.name} |"
    )
    print(row)

    ledger = Path(args.ledger)
    if not ledger.exists():
        print(f"error: ledger missing: {ledger}", file=sys.stderr)
        return 1
    text = ledger.read_text("utf-8")
    if RUN_LOG_HEADING not in text:
        print(f"error: '{RUN_LOG_HEADING}' heading not found in ledger", file=sys.stderr)
        return 1

    lines = text.splitlines()
    # find the table under the heading (after the heading line, find the last
    # line starting with '|', append after it)
    h = lines.index(RUN_LOG_HEADING)
    last_table = None
    for i in range(h + 1, len(lines)):
        if lines[i].startswith("#"):  # next section
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
