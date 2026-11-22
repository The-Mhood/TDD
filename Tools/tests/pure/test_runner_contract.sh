#!/bin/bash
# Regression checks for failure propagation and the documented evidence CLI.
set -u
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
RUNNER="$REPO/Tools/tests/pure/run_pure.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cat > "$TMP/failing-cxx" <<'EOF'
#!/bin/sh
echo "intentional compiler failure for runner contract test" >&2
exit 42
EOF
chmod +x "$TMP/failing-cxx"

if CXX="$TMP/failing-cxx" bash "$RUNNER" > "$TMP/failure-output" 2>&1; then
  echo "FAIL: runner returned success when all suite compiles failed" >&2
  exit 1
fi
expected="$(find "$REPO/Tests/Standalone" -name '*Tests.cpp' | wc -l | tr -d ' ')"
actual="$(grep -c 'TDD_RESULT .* FAIL reason=compile_error' "$TMP/failure-output" || true)"
if [ "$actual" -ne "$expected" ]; then
  echo "FAIL: expected $expected compile-failure results, got $actual" >&2
  exit 1
fi

if bash "$RUNNER" --evidence-dir > "$TMP/arg-output" 2>&1; then
  echo "FAIL: runner accepted --evidence-dir without a path" >&2
  exit 1
fi

echo "TDD_RESULT TDD-Tool.PureRunnerContract PASS failure_propagation=$actual evidence_arg=validated"
