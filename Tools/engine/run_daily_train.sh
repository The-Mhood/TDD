#!/bin/bash
# The daily test train — the project's verification heartbeat (ROADMAP v2.0 §4.3).
# One command, ~60 min, on the owner's Mac:
#
#   Tools/engine/run_daily_train.sh
#
# Steps (each with real evidence; no step reports success without a log):
#   1. pure-core suites (host-compiled, seconds) — agent-side surface (ADR-0012 boundary)
#   2. full Mac build + automation (mac_build.sh) — the UE authority
#   3. evidence bundle consolidated under Saved/BuildEvidence/<UTC>/
#   4. quality ledger row appended (Tools/engine/ledger_update.py)
#   5. one-line status printed for the Issue (copy-paste, parser-generated)
#
# Exit: 0 = all green. Non-zero = the train failed; the next day's batch is
# pre-triaged and no new work merges until it is green (DA-01).
set -u

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
UTC="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE="$REPO/Saved/BuildEvidence/$UTC"
mkdir -p "$EVIDENCE"

say()  { printf '%s\n' "$*"; }
rc_total=0

say "=== TDD daily train $UTC ==="
say "commit: $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null)  branch: $(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null)"
say

# ---------- 1. pure core ----------------------------------------------------
say "1. pure-core suites (host-compiled)"
if out="$(bash "$REPO/Tools/tests/pure/run_pure.sh" --evidence-dir "$EVIDENCE" 2>&1)"; then
  say "  ok — all pure suites green"
else
  say "  FAILED — pure core is red; nothing new merges until fixed (DA-01)"
  rc_total=1
fi
printf '%s\n' "$out" > "$EVIDENCE/10-pure-results.txt"
grep '^TDD_RESULT' "$EVIDENCE/10-pure-results.txt" | sed 's/^/  /'
say

# ---------- 2. full UE build + automation -----------------------------------
say "2. Mac build + automation (mac_build.sh)"
if bash "$REPO/Tools/engine/mac_build.sh" --test-filter "TDD" > "$EVIDENCE/20-mac-build-train.log" 2>&1; then
  say "  ok — build + automation green (see 20-mac-build-train.log)"
else
  say "  FAILED — see 20-mac-build-train.log (tail follows)"
  tail -25 "$EVIDENCE/20-mac-build-train.log" | sed 's/^/      /'
  rc_total=1
fi
say

# ---------- 3. ledger --------------------------------------------------------
say "3. quality ledger"
python3 "$REPO/Tools/engine/ledger_update.py" \
  --evidence-dir "$EVIDENCE" \
  --platform mac \
  --train daily \
  --commit "$(git -C "$REPO" rev-parse HEAD 2>/dev/null || echo unknown)" \
  --ledger "$REPO/docs/06_IMPLEMENTATION/QUALITY_LEDGER.md" \
  > "$EVIDENCE/30-ledger-row.txt" 2>&1 \
  && { say "  ok — ledger row appended"; cat "$EVIDENCE/30-ledger-row.txt" | sed 's/^/  /'; } \
  || { say "  WARNING — ledger update failed (train evidence still complete)"; rc_total=1; }
say

# ---------- 4. one-line status ------------------------------------------------
pure_summary="$(grep -c '^TDD_RESULT .* PASS' "$EVIDENCE/10-pure-results.txt" 2>/dev/null || echo 0)/$(grep -c '^TDD_RESULT' "$EVIDENCE/10-pure-results.txt" 2>/dev/null || echo 0) pure"
mac_counts="$(tail -20 "$EVIDENCE/20-mac-build-train.log" | grep -oE 'passed=[0-9]+ failed=[0-9]+' | tail -1 || echo 'passed=? failed=?')"
status="PASS"
[ "$rc_total" -ne 0 ] && status="FAIL"
say "4. status line (post to Issue #1):"
say "  TRAIN $UTC $(git -C "$REPO" rev-parse --short HEAD 2>/dev/null) $status ${pure_summary:-0/0} ${mac_counts:-mac=?} evidence=Saved/BuildEvidence/$UTC"
say
exit "$rc_total"
