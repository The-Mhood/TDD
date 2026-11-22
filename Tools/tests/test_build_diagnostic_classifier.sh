#!/usr/bin/env bash
# test_build_diagnostic_classifier.sh — regression test for the evidence-based
# failure classification of build_phase1_diagnostic.sh.
#
# Runs the REAL diagnostic script against a MOCK UE 5.8 tree (mock
# GenerateProjectFiles.sh / Build.sh) and asserts that every required state is
# classified correctly, that an upstream source failure is NEVER labelled an
# invocation failure, and that an unhandled .NET aggregate exception is NEVER
# reported as a confirmed UHT failure without UHT-specific error evidence —
# the underlying exception must be captured in the detail section.
#
# Usage: bash Tools/tests/test_build_diagnostic_classifier.sh
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIAG="$REPO_ROOT/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/build_phase1_diagnostic.sh"

MOCK="$(mktemp -d /tmp/tdd_diag_mock.XXXXXX)"
ENG="$MOCK/UE_5.8"
mkdir -p "$ENG/Engine/Build/BatchFiles/Mac"

# Mock engine: presence of the three batch scripts is all the diagnostic checks.
: > "$ENG/Engine/Build/BatchFiles/RunUAT.sh"
cat > "$ENG/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh" <<'MOCK'
#!/usr/bin/env bash
if [ "${MOCK_GPF_STATE:-ok}" = "fail" ]; then
  echo "Error: Unable to generate project files (mock)"
  exit 3
fi
echo "Project files generated (mock)"
exit 0
MOCK
cat > "$ENG/Engine/Build/BatchFiles/Mac/Build.sh" <<'MOCK'
#!/usr/bin/env bash
case "${MOCK_BUILD_STATE:-ok}" in
  uht)
    echo "UnrealHeaderTool error: Unable to find 'enum' with name 'EMarketDay'"
    echo "error: header parse failed (mock)"
    exit 1 ;;
  compile)
    echo "TDD_GAME.cpp:10:5: error: use of undeclared identifier 'Foo'"
    exit 1 ;;
  clang_uht_traces)
    # Real Clang failure whose output contains UHT-generated files in the
    # include traces (.gen.cpp, UObject/, GENERATED_BODY). This must be
    # classified as C++ COMPILATION FAILED, NOT UHT: the compiler errors prove
    # UHT already ran and succeeded.
    echo "In file included from /Users/x/TDD_GAME/Intermediate/Build/Mac/TDD_GAME/Development/TDD_GAME.gen.cpp:12:"
    echo "  from /Users/x/TDD_GAME/Source/TDD_GAME/Private/TDDLocationRegistry.cpp:3:"
    echo "    UObject/NameTypes.h:1:1: note: GENERATED_BODY include trace"
    echo "TDDLocationRegistry.cpp:25:5: error: no match for 'operator*'"
    exit 1 ;;
  link)
    echo "Undefined symbols for architecture arm64:"
    echo "  _TDD_Undefined_Symbol"
    exit 1 ;;
  invocation)
    echo "No platforms specified for target 'TDD_GAME'"
    exit 1 ;;
  aggregate_uht)
    # Real-world UHT-failure signature: UHT invocation line, then the error
    # line, then the .NET aggregate wrapper (verified against UBT output).
    echo "Running UnrealHeaderTool..."
    echo "TDDFoo.h(12): Error: Unterminated character constant"
    echo "Unhandled 1 aggregate exceptions"
    echo "Result: Failed (OtherCompilationError)"
    exit 1 ;;
  aggregate_unknown)
    # UBT-internal .NET exception: aggregate wrapper + exception + stack trace,
    # NO UHT-specific error evidence.
    echo "Unhandled 1 aggregate exceptions"
    echo "Unhandled exception: System.IO.IOException: Permission denied"
    echo "  at UnrealBuildTool.XcodeProjectXcconfig.XcodeProjectFile.WriteProjectFile(...)"
    exit 1 ;;
  uht_token_only)
    # A bare UHT mention in normal output must NOT be classified as UHT.
    echo "UHT version 1.0 (engine tool banner)"
    exit 1 ;;
  ok)
    echo "Build succeeded (mock)"
    exit 0 ;;
  *)
    echo "Unclassified failure output (mock)"
    exit 1 ;;
esac
MOCK
chmod +x "$ENG/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh" \
       "$ENG/Engine/Build/BatchFiles/Mac/Build.sh"

# Logs the real script writes into the project dir; remove them after the test.
CREATED_LOGS=()
cleanup() { rm -rf "$MOCK"; for f in "${CREATED_LOGS[@]}"; do [ -n "$f" ] && rm -f "$f"; done; }
trap cleanup EXIT

pass=0; fail=0
run_case() {
  local state="$1" expect_label="$2" expect_rc="$3" gpf_state="$4"
  local newlogs=""
  UE_ROOT="$ENG" MOCK_GPF_STATE="$gpf_state" MOCK_BUILD_STATE="$state" \
    bash "$DIAG" > "$MOCK/out.txt" 2>&1
  local rc=$?
  newlogs="$(ls -t "$REPO_ROOT"/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/BUILD_DIAGNOSTIC_*.log 2>/dev/null | head -1)"
  [ -n "$newlogs" ] && CREATED_LOGS+=("$newlogs")
  if [ "$rc" -ne "$expect_rc" ]; then
    echo "FAIL [$state] exit=$rc expected=$expect_rc"; fail=$((fail+1)); return
  fi
  if ! grep -q "$expect_label" "$newlogs"; then
    echo "FAIL [$state] log missing label '$expect_label'"
    echo "---- tail ----"; tail -12 "$newlogs"
    fail=$((fail+1)); return
  fi
  # The UHT case emits 'error:' text; it must NOT be classified as invocation.
  if [ "$state" = "uht" ] && grep -q "BUILD INVOCATION FAILED" "$newlogs"; then
    echo "FAIL [uht] misclassified as invocation"; fail=$((fail+1)); return
  fi
  # An aggregate exception without UHT evidence must NOT be labelled UHT.
  if [ "$state" = "aggregate_unknown" ] && grep -q "UHT / HEADER PARSE FAILED" "$newlogs"; then
    echo "FAIL [aggregate_unknown] misclassified as UHT without evidence"
    fail=$((fail+1)); return
  fi
  # A bare UHT token must NOT be labelled UHT.
  if [ "$state" = "uht_token_only" ] && grep -q "UHT / HEADER PARSE FAILED" "$newlogs"; then
    echo "FAIL [uht_token_only] bare UHT token misclassified as UHT failure"
    fail=$((fail+1)); return
  fi
  # A Clang failure whose output mentions UHT-generated files in include traces
  # must NOT be classified as UHT, and the first compiler error must be preserved.
  if [ "$state" = "clang_uht_traces" ]; then
    if grep -q "UHT / HEADER PARSE FAILED" "$newlogs"; then
      echo "FAIL [clang_uht_traces] Clang failure with UHT-generated include traces misclassified as UHT"
      fail=$((fail+1)); return
    fi
    if ! grep -q "TDDLocationRegistry.cpp:25:5: error:" "$newlogs"; then
      echo "FAIL [clang_uht_traces] first compiler error not preserved in the log"
      fail=$((fail+1)); return
    fi
  fi
  # The plain compile case must also preserve the first compiler error.
  if [ "$state" = "compile" ] && ! grep -q "TDD_GAME.cpp:10:5: error:" "$newlogs"; then
    echo "FAIL [compile] first compiler error not preserved in the log"
    fail=$((fail+1)); return
  fi
  # The underlying exception/error detail must be captured in the log.
  if [ "$state" = "aggregate_uht" ] && ! grep -q "Unterminated character constant" "$newlogs"; then
    echo "FAIL [aggregate_uht] underlying Error: line not captured in detail section"
    fail=$((fail+1)); return
  fi
  if [ "$state" = "aggregate_unknown" ]; then
    if ! grep -q "IOException" "$newlogs" || ! grep -q "at UnrealBuildTool" "$newlogs"; then
      echo "FAIL [aggregate_unknown] underlying .NET exception not captured in detail section"
      fail=$((fail+1)); return
    fi
  fi
  echo "PASS [$state] rc=$rc label='$expect_label'"
  pass=$((pass+1))
}

run_case gpf_fail         "PROJECT FILE GENERATION FAILED" 3 fail
run_case uht              "UHT / HEADER PARSE FAILED"      1 ok
run_case compile          "C++ COMPILATION FAILED"         1 ok
run_case clang_uht_traces  "C++ COMPILATION FAILED"         1 ok
run_case link             "LINKING FAILED"                 1 ok
run_case invocation       "BUILD INVOCATION FAILED"        1 ok
run_case aggregate_uht    "UHT / HEADER PARSE FAILED"      1 ok
run_case aggregate_unknown "UBT EXCEPTION"                 1 ok
run_case uht_token_only   "unclassified"                   1 ok
run_case ok               "SUCCESS"                        0 ok

echo
echo "classifier regression: $pass PASS / $fail FAIL"
[ "$fail" -eq 0 ]
