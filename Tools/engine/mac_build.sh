#!/bin/bash
# Build and test the canonical project on the owner's Mac (Apple Silicon).
#
#   Tools/engine/mac_build.sh [--project PATH] [--engine PATH] [--test-filter REGEX] [--skip-tests]
#
# It does four things, in order, and stops reporting only what actually happened:
#   1. checks the environment (macOS, Xcode, UE 5.8, the descriptor)
#   2. generates project files
#   3. builds <Project>Editor and <Project> for Mac Development
#   4. runs the automation tests headless and reads the result out of the log
#
# Every step writes its log to Saved/BuildEvidence/<UTC timestamp>/ and the script
# prints a summary with the real exit status of each step. It never reports a build
# that did not run: if a prerequisite is missing it prints NOT EXECUTED and exits 2.
set -u

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
PROJECT=""
ENGINE="${UE_ROOT:-}"
TEST_FILTER="TDD"
SKIP_TESTS=0
MIN_XCODE_MAJOR="${MIN_XCODE_MAJOR:-16}"   # must match Epic's stated requirement for the installed 5.8 build

while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --engine)  ENGINE="$2";  shift 2 ;;
    --test-filter) TEST_FILTER="$2"; shift 2 ;;
    --skip-tests) SKIP_TESTS=1; shift ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 64 ;;
  esac
done

say()  { printf '%s\n' "$*"; }
step_fail() { say "  FAILED: $*"; SUMMARY_FAILED=1; }
SUMMARY_FAILED=0
EVIDENCE=""

# ---------- 1. environment -------------------------------------------------
say "1. environment"
if [ "$(uname -s)" != "Darwin" ]; then
  say "  NOT EXECUTED — this script must run on macOS (host is $(uname -s))."
  say "  Required: the owner's Apple Silicon Mac. Nothing was built."
  exit 2
fi
say "  host: $(uname -m) / $(sw_vers -productVersion 2>/dev/null)"
[ "$(uname -m)" = "arm64" ] || say "  WARNING: not arm64 — Unreal on Intel Mac is supported but slower to build"

if ! command -v xcodebuild >/dev/null 2>&1; then
  say "  NOT EXECUTED — Xcode command line tools not found."
  say "  Required: install Xcode from the App Store, then: sudo xcode-select -s /Applications/Xcode.app"
  exit 2
fi
XCODE_VER="$(xcodebuild -version 2>/dev/null | awk 'NR==1{print $2}')"
say "  Xcode: ${XCODE_VER:-unknown} (xcode-select: $(xcode-select -p 2>/dev/null))"
major="${XCODE_VER%%.*}"
if [ -n "${major:-}" ] && [ "$major" -lt "$MIN_XCODE_MAJOR" ] 2>/dev/null; then
  say "  WARNING: Xcode $XCODE_VER is below the $MIN_XCODE_MAJOR.x expected for this engine; UBT may refuse it"
fi

if [ -z "$PROJECT" ]; then
  PROJECT="$(ls "$REPO"/*.uproject 2>/dev/null | head -1)"
fi
if [ -z "$PROJECT" ] || [ ! -f "$PROJECT" ]; then
  say "  NOT EXECUTED — no .uproject found (looked for $REPO/*.uproject)."
  say "  Required: the canonical descriptor at the repository root. Nothing was built."
  exit 2
fi
PROJECT="$(cd "$(dirname "$PROJECT")" && pwd)/$(basename "$PROJECT")"
PROJECT_NAME="$(basename "$PROJECT" .uproject)"
say "  project: $PROJECT"
say "  targets: ${PROJECT_NAME}Editor (editor), ${PROJECT_NAME} (game)"

if [ -z "$ENGINE" ]; then
  for cand in "/Users/Shared/Epic Games/UE_5.8" "$HOME/UnrealEngine" "/Applications/UE_5.8"; do
    [ -d "$cand" ] && ENGINE="$cand" && break
  done
fi
if [ -z "$ENGINE" ] || [ ! -d "$ENGINE" ]; then
  say "  NOT EXECUTED — Unreal Engine 5.8 not found."
  say "  Required: install UE 5.8 via the Epic Games Launcher, then re-run with --engine \"/Users/Shared/Epic Games/UE_5.8\""
  exit 2
fi
BUILD_SH="$ENGINE/Engine/Build/BatchFiles/Mac/Build.sh"
GPF_SH="$ENGINE/Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh"
EDITOR_CMD="$ENGINE/Engine/Binaries/Mac/UnrealEditor-Cmd"
for f in "$BUILD_SH" "$GPF_SH" "$EDITOR_CMD"; do
  [ -x "$f" ] || { say "  NOT EXECUTED — missing in engine tree: $f"; exit 2; }
done
if [ -f "$ENGINE/Engine/Build/Build.version" ]; then
  say "  engine: $ENGINE ($(tr -d '\n ' < "$ENGINE/Engine/Build/Build.version"))"
else
  say "  engine: $ENGINE (Build.version unreadable)"
fi

mkdir -p "$REPO/Saved/BuildEvidence"
EVIDENCE="$REPO/Saved/BuildEvidence/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$EVIDENCE"
say "  evidence directory: $EVIDENCE"
say

# ---------- 2. project files ----------------------------------------------
say "2. generate project files"
if "$GPF_SH" -project="$PROJECT" -game -engine >"$EVIDENCE/01-generate-project-files.log" 2>&1; then
  say "  ok — see 01-generate-project-files.log"
else
  step_fail "project generation (see 01-generate-project-files.log)"
fi
say

# ---------- 3. build -------------------------------------------------------
say "3. build (Mac Development)"
for target in "${PROJECT_NAME}Editor" "${PROJECT_NAME}"; do
  log="$EVIDENCE/02-build-${target}.log"
  say "  building $target …"
  if "$BUILD_SH" "$target" Mac Development -project="$PROJECT" -waitmutex >"$log" 2>&1; then
    say "  ok — $target built (log: 02-build-${target}.log)"
  else
    step_fail "$target (tail of log follows)"
    tail -25 "$log" | sed 's/^/      /'
  fi
done
say

# ---------- 4. automation tests -------------------------------------------
if [ "$SKIP_TESTS" -eq 1 ]; then
  say "4. automation tests — SKIPPED by --skip-tests"
else
  say "4. automation tests (filter: $TEST_FILTER)"
  log="$EVIDENCE/03-automation-${TEST_FILTER}.log"
  "$EDITOR_CMD" "$PROJECT" \
      -ExecCmds="Automation RunTests ${TEST_FILTER};Quit" \
      -unattended -nopause -nullrhi -nosplash -stdout -FullStdOutLogOutput -log \
      >"$log" 2>&1
  rc=$?
  passed=$(grep -c "Result={Passed}" "$log" 2>/dev/null || true)
  failed=$(grep -c "Result={Failed}" "$log" 2>/dev/null || true)
  tested=$(grep -c "^LogAutomationController: Test Started" "$log" 2>/dev/null || true)
  say "  exit=$rc  tests started=${tested:-0}  passed=${passed:-0}  failed=${failed:-0}"
  if [ "${failed:-0}" -gt 0 ] || [ "$rc" -ne 0 ]; then
    step_fail "automation failures (see 03-automation-${TEST_FILTER}.log)"
    grep -m 10 "Result={Failed}\|Error:" "$log" | sed 's/^/      /'
  elif [ "${tested:-0}" -eq 0 ]; then
    step_fail "no test matched filter '${TEST_FILTER}' — the foundation test may not be compiled into the editor"
  else
    say "  ok — automation tests passed"
  fi
fi
say

# ---------- summary --------------------------------------------------------
say "summary"
say "  project:  $PROJECT_NAME  (engine $(basename "$ENGINE"))"
say "  evidence: $EVIDENCE"
if [ "$SUMMARY_FAILED" -eq 0 ]; then
  say "  RESULT: BUILD AND TESTS OK on this machine at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit 0
else
  say "  RESULT: FAILED — see the logs above. Do not report this run as a successful build."
  exit 1
fi
