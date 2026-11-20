#!/bin/bash
# Windows CI runner — the reference PC (D-12, ordered Day 0) runs this on every
# integration push from W2 (F-04). It is the second verification surface that
# de-risks the single-Mac bottleneck: while the Mac does look-dev/editor work,
# the PC proves the primary shipping platform stays green.
#
#   Tools/engine/windows_ci.sh [BRANCH]     (default: origin/arena/553fb02d-tdd)
#
# Steps: pure suites (if g++ present in a dev shell) -> UBT builds (Win64 Editor
# Development + Game Shipping) -> headless automation -> evidence bundle -> ledger row ->
# one-line status. Trigger: run manually, or wire as a push hook on the PC
# (git config core.hooksPath / a scheduled task running this every 30 min).
#
# Environment: UE 5.8.4 at %UE_ROOT% (default C:\Program Files\Epic Games\UE_5.8).
set -u

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
BRANCH="${1:-arena/553fb02d-tdd}"
UTC="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE="$REPO/Saved/BuildEvidence/$UTC"
UE_ROOT="${UE_ROOT:-C:/Program Files/Epic Games/UE_5.8}"
PROJECT_NAME="TheDisobedientDaughter"

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) ;;
  *) echo "NOT EXECUTED — Windows CI must run in the Windows reference-PC shell (MINGW/MSYS/CYGWIN); host is $(uname -s). No checkout or build attempted."; exit 2 ;;
esac

mkdir -p "$EVIDENCE"
rc=0

echo "=== TDD Windows CI $UTC ==="
echo "commit: $(git -C "$REPO" rev-parse --short HEAD)  branch: $(git -C "$REPO" rev-parse --abbrev-ref HEAD)"

# 1. verify the checked-out integration branch without changing user state.
# Never checkout/reset --hard inside a CI helper: it can silently destroy local work.
current_branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
if [ "$current_branch" != "$BRANCH" ]; then
  echo "NOT EXECUTED — checked out branch is '$current_branch'; expected '$BRANCH'. No branch switch was attempted."
  exit 2
fi
if [ -n "$(git -C "$REPO" status --porcelain 2>/dev/null)" ]; then
  echo "NOT EXECUTED — working tree is not clean; refusing to build an ambiguous source state."
  exit 2
fi
if ! git -C "$REPO" fetch origin "$BRANCH" >>"$EVIDENCE/00-sync.log" 2>&1; then
  echo "NOT EXECUTED — git fetch failed (see 00-sync.log)"
  exit 2
fi
local_sha="$(git -C "$REPO" rev-parse HEAD)"
remote_sha="$(git -C "$REPO" rev-parse "refs/remotes/origin/$BRANCH" 2>/dev/null || echo missing)"
if [ "$local_sha" != "$remote_sha" ]; then
  echo "NOT EXECUTED — local HEAD $local_sha differs from origin/$BRANCH $remote_sha. Update the workspace explicitly, then rerun."
  exit 2
fi

# 2. pure core (needs a C++ toolchain in the dev shell; optional on the PC)
if command -v g++ >/dev/null 2>&1; then
  bash "$REPO/Tools/tests/pure/run_pure.sh" --evidence-dir "$EVIDENCE" >"$EVIDENCE/10-pure-results.txt" 2>&1 || rc=1
  bash "$REPO/Tools/tests/pure/test_runner_contract.sh" >"$EVIDENCE/11-runner-contract.txt" 2>&1 || rc=1
  bash "$REPO/Tools/tests/pure/test_ci_safety.sh" >"$EVIDENCE/12-windows-ci-safety.txt" 2>&1 || rc=1
else
  echo "TDD_RESULT TDD-Pure.SKIP reason=no_gpp_on_pc (pure suites run agent-side)" > "$EVIDENCE/10-pure-results.txt"
fi

# 3. build Win64 Development
BUILD_SH="$UE_ROOT/Engine/Build/BatchFiles/Build.bat"
if [ ! -f "$BUILD_SH" ]; then
  echo "NOT EXECUTED — UE not found at $UE_ROOT (set UE_ROOT). Nothing was built."
  exit 2
fi
"$BUILD_SH" "$PROJECT_NAMEEditor" Win64 Development -project="$REPO/TheDisobedientDaughter.uproject" -waitmutex >"$EVIDENCE/02-build-win64.log" 2>&1 || { echo "BUILD FAILED (see 02-build-win64.log)"; rc=1; }

# 3b. Compile the actual Win64 Shipping game target as a separate release gate.
# This validates compilation only; it is not a cook/package claim.
"$BUILD_SH" "$PROJECT_NAME" Win64 Shipping -project="$REPO/TheDisobedientDaughter.uproject" -waitmutex >"$EVIDENCE/02b-build-win64-shipping.log" 2>&1 || { echo "SHIPPING BUILD FAILED (see 02b-build-win64-shipping.log)"; rc=1; }

# 4. automation headless
EDITOR_CMD="$UE_ROOT/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
report="$EVIDENCE/automation-report"
"$EDITOR_CMD" "$REPO/TheDisobedientDaughter.uproject" \
  -ExecCmds="Automation RunTests TDD;Quit" \
  -TestExit="Automation Test Queue Empty" \
  -ReportExportPath="$report" \
  -unattended -nopause -nullrhi -nosplash -stdout -FullStdOutLogOutput -log \
  >"$EVIDENCE/03-automation-TDD.log" 2>&1 || rc=1

counts="$(python3 "$REPO/Tools/engine/parse_automation_report.py" --log "$EVIDENCE/03-automation-TDD.log" --report "$report/index.json" 2>/dev/null || echo 'discovered=? tested=? completed=? passed=? failed=? unclassified=?')"
echo "windows automation: $counts"

# 5. ledger + status line
python3 "$REPO/Tools/engine/ledger_update.py" --evidence-dir "$EVIDENCE" --platform windows --train ci --commit "$(git -C "$REPO" rev-parse HEAD)" --ledger "$REPO/docs/06_IMPLEMENTATION/QUALITY_LEDGER.md" || rc=1
status="PASS"; [ "$rc" -ne 0 ] && status="FAIL"
echo "WIN-CI $UTC $(git -C "$REPO" rev-parse --short HEAD) $status $counts evidence=Saved/BuildEvidence/$UTC"
exit "$rc"
