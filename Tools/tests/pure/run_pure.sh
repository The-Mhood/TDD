#!/bin/bash
# Compile and run every host-compiled (UE-independent) test suite under
# Tests/Standalone/**. No Unreal Engine, no GPU, no network — this is the
# agent-side verification surface for pure logic (ADR-0012 boundary; TR-19 T13).
#
#   Tools/tests/pure/run_pure.sh [--evidence-dir DIR]
#
# Emits one TDD_RESULT line per suite (greppable, D-07 format) and exits
# non-zero if any suite fails. A suite that fails to COMPILE is a failure,
# not a skip.
set -u

REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
PUBLIC="$REPO/Source/TheDisobedientDaughter/Public"
EVIDENCE_DIR="${EVIDENCE_DIR:-}"

if ! command -v g++ >/dev/null 2>&1; then
  echo "NOT EXECUTED — g++ not found in agent workspace; nothing was compiled."
  exit 2
fi

CXXFLAGS="-std=c++20 -O1 -Wall -Wextra -I$PUBLIC"
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

overall_rc=0
suites=0
passed=0
failed=0

# Find every standalone test (files whose name ends in Tests.cpp).
find "$REPO/Tests/Standalone" -name "*Tests.cpp" | sort | while read -r src; do
  name="$(basename "$src" .cpp)"
  exe="$BUILD_DIR/$name"
  log="$BUILD_DIR/$name.log"

  if ! g++ $CXXFLAGS "$src" -o "$exe" 2>"$log.compile"; then
    echo "TDD_RESULT TDD-Pure.$name FAIL reason=compile_error"
    echo "compile errors for $name:"
    head -15 "$log.compile" | sed 's/^/  /'
    overall_rc=1
    continue
  fi

  if out="$("$exe" 2>&1)"; then
    suites=$((suites+1)); passed=$((passed+1))
    assertions="$(printf '%s\n' "$out" | grep -oE '[0-9]+/[0-9]+ assertions passed' | tail -1)"
    echo "TDD_RESULT TDD-Pure.$name PASS ${assertions:-output=ok}"
  else
    overall_rc=1
    echo "TDD_RESULT TDD-Pure.$name FAIL $(printf '%s' "$out" | tail -1)"
    printf '%s\n' "$out" | tail -15 | sed 's/^/  /'
  fi
done

if [ -n "$EVIDENCE_DIR" ]; then
  mkdir -p "$EVIDENCE_DIR"
  {
    echo "# pure-core run $(date -u +%Y-%m-%dT%H:%M:%SZ) commit=$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    find "$REPO/Tests/Standalone" -name "*Tests.cpp" | sort | while read -r src; do
      name="$(basename "$src" .cpp)"
      [ -f "$BUILD_DIR/$name.log" ] && cat "$BUILD_DIR/$name.log" || true
    done
  } > "$EVIDENCE_DIR/pure-run.log" 2>/dev/null || true
fi

exit "$overall_rc"
