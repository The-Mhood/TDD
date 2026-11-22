#!/bin/bash
# Regression checks for ledger_update.py status logic (fixed 2026-11-20).
# A failed build, failed automation, missing results, or incomplete
# verification must never produce GREEN.
#
#   Tools/tests/ledger/run_ledger_tests.sh [--evidence-dir DIR]
#
# Emits one TDD_RESULT line and exits non-zero if any case fails.
set -u

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
TEST="$REPO/Tools/tests/ledger/test_ledger_status.py"
EVIDENCE_DIR="${EVIDENCE_DIR:-}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "NOT EXECUTED — python3 not found; nothing was run."
  exit 2
fi

if [ ! -f "$TEST" ]; then
  echo "TDD_RESULT TDD-Tool.LedgerStatusTests FAIL reason=missing_test"
  exit 1
fi

if [ -n "$EVIDENCE_DIR" ]; then
  mkdir -p "$EVIDENCE_DIR"
  python3 "$TEST" > "$EVIDENCE_DIR/ledger-status-tests.txt" 2>&1
  rc=$?
  cat "$EVIDENCE_DIR/ledger-status-tests.txt"
  exit "$rc"
fi

python3 "$TEST"
exit $?
