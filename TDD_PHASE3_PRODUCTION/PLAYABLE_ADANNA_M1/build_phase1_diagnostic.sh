#!/usr/bin/env bash
# build_phase1_diagnostic.sh — Robust Mac diagnostic procedure for the Phase-1
# Unreal build. Run this INSTEAD of ad-hoc commands when the build fails.
#
# The Disobedient Daughter · Phase 1 Ọmà-valley core (TDD-IMPL-PHASE1-002)
#
# What this script does (each step is isolated, logged, and PASS/FAIL-checked):
#   0. Locate the Unreal Engine 5.8 install path (env override + auto-detect).
#   1. Validate the engine, the THREE build scripts, and the project file.
#      Each tool is looked up INDEPENDENTLY — UE 5.8 does NOT put all three
#      in the same directory:
#        RunUAT.sh              -> Engine/Build/BatchFiles/RunUAT.sh          (cross-platform)
#        Build.sh               -> Engine/Build/BatchFiles/Mac/Build.sh      (Mac-specific)
#        GenerateProjectFiles.sh -> Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh (Mac-specific)
#   2. Generate project files (UBT must see the Phase-1 C++ sources).
#   3. Build TDD_GAME (Development / Mac) via the Mac Build.sh (UnrealBuildTool)
#      — the real C++ compile check. (UE 5.8 AutomationTool has no "BuildProject"
#      command; RunUAT.sh BuildProject fails with Error_Unknown.)
#   4. On failure, print the EXACT failing command and the compiler diagnostics.
#
# The final classification distinguishes SEVEN states (and never mislabels an
# upstream source failure as an invocation failure). Priority is STAGE-ACCURATE:
#   1. PROJECT FILE GENERATION FAILED  — GenerateProjectFiles.sh exited nonzero
#   2. C++ COMPILATION FAILED          — the Clang C++ compiler reported errors.
#                                        Compiler errors mean UHT already ran and
#                                        SUCCEEDED: UHT-generated .gen.cpp/.gen.h file
#                                        names in Clang include traces are normal and
#                                        are NOT evidence of UHT rejection.
#   3. LINKING FAILED                  — compilation succeeded, linker errors
#   4. UHT / HEADER PARSE FAILED       — Unreal Header Tool rejected reflection
#                                        (UHT's OWN error format only; a bare UHT
#                                        mention, or GENERATED_BODY / UObject/ tokens
#                                        in compiler output, do NOT count as UHT evidence)
#   5. BUILD INVOCATION FAILED         — command/args/environment; compiler never ran
#   6. UBT EXCEPTION                   — UBT .NET aggregate exception with no identified
#                                        upstream cause; underlying exception printed (NOT a
#                                        confirmed UHT failure without UHT evidence)
#   7. SUCCESS                         — Build.sh exited 0 (compile-verified only)
# The first meaningful compiler error is always preserved in the failure detail.
#
# ALL output is tee'd to a PERSISTENT log file so it survives a closed terminal.
# The log path is printed at the top and the tail is printed on any failure.
#
# Usage:
#   cd TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1
#   bash build_phase1_diagnostic.sh
#   # or, if UE is not in a default location (paths with spaces are fine):
#   UE_ROOT="/Users/Shared/Epic Games/UE_5.8" bash build_phase1_diagnostic.sh
#
# Owner role: run this, then send the LOG FILE (and the printed failure tail) back
# to Engineering. Do NOT attempt to fix C++ yourself — Engineering owns all fixes.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$HERE/ue_project/TDD_GAME.uproject"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$HERE/BUILD_DIAGNOSTIC_${TS}.log"
: > "$LOG"

# Everything echoes to stdout AND the persistent log.
exec > >(tee -a "$LOG") 2>&1

say()  { echo "[diag] $*"; }
pass() { echo "[diag] PASS  $*"; }
fail() { echo "[diag] FAIL  $*"; }

echo "================================================================"
echo " Phase-1 Unreal build diagnostic — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo " Persistent log: $LOG"
echo " (If the terminal closes, this log file remains — cat it any time.)"
echo "================================================================"

# --------------------------------------------------------------------------- #
# locate_tool <name> <reldir1> [reldir2 ...]
#   Sets GLOBAL FOUND_PATH to the first existing file and returns 0; else returns 1.
#   All paths are quoted, so UE_ROOT values containing spaces are safe.
#   The relative dirs are tried in order under $UE_ROOT_FOUND.
# --------------------------------------------------------------------------- #
find_tool() {
  local name="$1"; shift
  FOUND_PATH=""
  local rel
  for rel in "$@"; do
    local cand="$UE_ROOT_FOUND/$rel/$name"
    if [ -f "$cand" ]; then
      FOUND_PATH="$cand"
      return 0
    fi
  done
  return 1
}

# run_tool <script-path> <args...>
#   Runs the script directly if executable, else via `bash <script>`.
run_tool() {
  local script="$1"; shift
  if [ -x "$script" ]; then
    "$script" "$@"
  else
    bash "$script" "$@"
  fi
}

# --------------------------------------------------------------------------- #
# Step 0 — locate the Unreal Engine 5.8
# --------------------------------------------------------------------------- #
# Candidate engine roots. The Epic Games Launcher install on macOS commonly
# uses /Users/Shared/Epic Games/UE_5.8; older launches used ~/Library/Engines.
# A source build uses whatever path was cloned. UE_ROOT, if set, is tried first.
CANDIDATES=(
  "${UE_ROOT:-}"
  "/Users/Shared/Epic Games/UE_5.8"
  "/Users/Shared/Epic Games/UE_5.8.0"
  "$HOME/Library/Engines/UnrealEngine"
  "$HOME/Documents/Unreal Engine"
  "$HOME/Documents/UnrealEngine"
  "$HOME/UnrealEngine"
  "$HOME/Unreal Engine"
)

# Engine presence is detected via RunUAT.sh. UE 5.8 puts it at the canonical
# cross-platform location (Engine/Build/BatchFiles/RunUAT.sh); older/legacy
# layouts may place it under BatchFiles/Mac/. Accept EITHER so detection stays
# robust — each tool is still located independently in Step 1a below.
UE_ROOT_FOUND=""
for c in "${CANDIDATES[@]}"; do
  [ -z "$c" ] && continue
  if [ -f "$c/Engine/Build/BatchFiles/RunUAT.sh" ] || [ -f "$c/Engine/Build/BatchFiles/Mac/RunUAT.sh" ]; then
    UE_ROOT_FOUND="$c"
    break
  fi
done

if [ -z "$UE_ROOT_FOUND" ]; then
  fail "Could not locate Unreal Engine 5.8. RunUAT.sh not found under any candidate."
  echo "[diag] Candidates checked (looking for Engine/Build/BatchFiles/RunUAT.sh):"
  for c in "${CANDIDATES[@]}"; do [ -n "$c" ] && echo "    $c/Engine/Build/BatchFiles/RunUAT.sh"; done
  echo "[diag] ACTION: install UE 5.8 via the Epic Games Launcher, OR set UE_ROOT:"
  echo "        UE_ROOT=\"/path/to/UE_5.8\" bash build_phase1_diagnostic.sh"
  echo "[diag] Then re-run. Send this log to Engineering if the path is unexpected."
  exit 1
fi
pass "Engine found: UE_ROOT=$UE_ROOT_FOUND"

# --------------------------------------------------------------------------- #
# Step 1a — validate the THREE build scripts INDEPENDENTLY
# --------------------------------------------------------------------------- #
# UE 5.8 Mac layout (verified by owner with `find`):
#   RunUAT.sh               -> Engine/Build/BatchFiles/RunUAT.sh
#   Build.sh                -> Engine/Build/BatchFiles/Mac/Build.sh
#   GenerateProjectFiles.sh -> Engine/Build/BatchFiles/Mac/GenerateProjectFiles.sh
# We try both the canonical and Mac/ locations for every tool so the script
# stays correct across engine layouts, without assuming they share a directory.
UAT=""
BUILDSH=""
GPF=""

find_tool RunUAT.sh \
    Engine/Build/BatchFiles \
    Engine/Build/BatchFiles/Mac \
    && UAT="$FOUND_PATH" || true
find_tool Build.sh \
    Engine/Build/BatchFiles/Mac \
    Engine/Build/BatchFiles \
    && BUILDSH="$FOUND_PATH" || true
find_tool GenerateProjectFiles.sh \
    Engine/Build/BatchFiles/Mac \
    Engine/Build/BatchFiles \
    && GPF="$FOUND_PATH" || true

if [ -n "$UAT" ]; then
  pass "RunUAT.sh located: $UAT"
  [ -x "$UAT" ] || say "WARNING: RunUAT.sh is not executable — will invoke via 'bash'."
else
  fail "RunUAT.sh not found under $UE_ROOT_FOUND/Engine/Build/BatchFiles[/Mac]."
  echo "[diag] ACTION: verify the UE 5.8 install. Send this log to Engineering."
  exit 1
fi

if [ -n "$BUILDSH" ]; then
  pass "Build.sh located: $BUILDSH"
  [ -x "$BUILDSH" ] || say "WARNING: Build.sh is not executable (not used directly by this script)."
else
  # Build.sh is the actual compiler driver used in Step 3 (a wrapper around
  # UnrealBuildTool); a missing Build.sh means the Mac batch-scripts are incomplete.
  fail "Build.sh not found under $UE_ROOT_FOUND/Engine/Build/BatchFiles[/Mac]."
  echo "[diag] ACTION: verify the UE 5.8 Mac batch scripts. Send this log to Engineering."
  exit 1
fi

if [ -n "$GPF" ]; then
  pass "GenerateProjectFiles.sh located: $GPF"
  [ -x "$GPF" ] || say "WARNING: GenerateProjectFiles.sh is not executable — will invoke via 'bash'."
else
  fail "GenerateProjectFiles.sh not found under $UE_ROOT_FOUND/Engine/Build/BatchFiles[/Mac]."
  echo "[diag] ACTION: verify the UE 5.8 Mac batch scripts. Send this log to Engineering."
  exit 1
fi

# --------------------------------------------------------------------------- #
# Step 1b — validate the project file
# --------------------------------------------------------------------------- #
if [ ! -f "$PROJECT" ]; then
  fail "Project file not found: $PROJECT"
  echo "[diag] ACTION: confirm the repo path. Expected: .../PLAYABLE_ADANNA_M1/ue_project/TDD_GAME.uproject"
  exit 1
fi
pass "Project file present: $PROJECT"

# Confirm the target/module name in the .uproject is TDD_GAME.
if grep -q '"Name"[[:space:]]*:[[:space:]]*"TDD_GAME"' "$PROJECT"; then
  pass "Module TDD_GAME declared in .uproject"
else
  fail "Module TDD_GAME not found in .uproject — target name may have changed."
  exit 1
fi

# Confirm the data header exists (regenerate if missing — see §4.1 of the evidence doc).
DATA_H="$HERE/ue_project/Source/TDD_GAME/Public/TDDOmegaValleyData.h"
if [ ! -f "$DATA_H" ]; then
  say "Data header missing — regenerating from omega_valley.json..."
  python3 "$HERE/scripts/generate_omega_valley_data.py" || { fail "Data generation failed"; exit 1; }
  [ -f "$DATA_H" ] && pass "Data header regenerated: $DATA_H" || { fail "Data header still missing"; exit 1; }
else
  pass "Data header present: $DATA_H"
fi

# --------------------------------------------------------------------------- #
# Step 2 — Generate project files (REQUIRED so UBT sees the Phase-1 C++)
# --------------------------------------------------------------------------- #
say "Generating project files (UBT must see Source/TDD_GAME)..."
GPF_ARGS=("$PROJECT")
say "Exact command:"
printf '  %q' "$GPF" "${GPF_ARGS[@]}"; echo
RC_GPF=0
run_tool "$GPF" "${GPF_ARGS[@]}" 2>&1 || RC_GPF=$?
if [ "$RC_GPF" -eq 0 ]; then
  pass "GenerateProjectFiles.sh exited 0"
else
  fail "GenerateProjectFiles.sh exited $RC_GPF"
  CLASS="PROJECT FILE GENERATION FAILED — GenerateProjectFiles.sh exited $RC_GPF (the project files were not generated; UHT and UBT never ran). This is a project-file-generation failure, NOT an invocation or source failure."
  echo "[diag] ---- classification ----"
  echo "  $CLASS"
  echo "[diag] ---- last 40 lines of project-file generation ----"
  tail -n 40 "$LOG"
  echo "[diag] ACTION: send this log to Engineering. Do not edit .uproject/Build.cs yourself."
  exit "$RC_GPF"
fi

# --------------------------------------------------------------------------- #
# Step 3 — Build TDD_GAME (Development / Mac) via the Mac Build.sh (UnrealBuildTool)
# --------------------------------------------------------------------------- #
# UE 5.8 AutomationTool does NOT support the legacy "BuildProject" command:
#   RunUAT.sh BuildProject ... -> "Failed to find command BuildProject" (Error_Unknown)
# The real C++ build path is the platform Build.sh, which drives UnrealBuildTool
# (the actual compiler driver). The canonical Build.sh/Build.bat positional signature
# is:  Build.sh <TargetName> <Platform> <Configuration> -project=<uproject> [options]
# (equivalently: -Target="<Target> <Platform> <Configuration>" -project=<uproject>).
# The project path is NOT a positional argument — it is passed via -project=.
# Passing the .uproject path as a positional lands it in the PLATFORM slot, which
# makes UBT resolve an empty platform list -> "No platforms specified for target".
#   Target         = TDD_GAME  (game target; Type=Game in TDD_GAME.Target.cs)
#   Platform       = Mac       (.uproject TargetPlatforms: ["Mac"])
#   Configuration  = Development
#   -project       = absolute path to TDD_GAME.uproject
#   -WaitMutex     = wait for the build mutex (avoids mutex failures if editor runs)
#   -architecture  = arm64 (owner hardware is Apple Silicon M4)
# Build.sh is invoked from its own directory to be robust to cwd sensitivity.
say "Building TDD_GAME (Development / Mac) via Build.sh (UnrealBuildTool)..."
BUILD_ARGS=( TDD_GAME Mac Development -project="$PROJECT" -WaitMutex -architecture=arm64 )
BUILD_CMD=("$BUILDSH" "${BUILD_ARGS[@]}")   # display form
say "Exact build command:"
printf '  %q' "${BUILD_CMD[@]}"; echo

# Marker-delimited build output so failure classification scans ONLY the build's
# own output (not earlier [diag] lines).
BUILD_MARK_BEGIN="@@TDD_BUILD_OUTPUT_BEGIN@@"
BUILD_MARK_END="@@TDD_BUILD_OUTPUT_END@@"
echo "$BUILD_MARK_BEGIN"
RC_BUILD=0
BUILD_DIR="$(cd "$(dirname "$BUILDSH")" && pwd)"
if [ -x "$BUILDSH" ]; then
  ( cd "$BUILD_DIR" && "$BUILDSH" "${BUILD_ARGS[@]}" ) 2>&1 || RC_BUILD=$?
else
  ( cd "$BUILD_DIR" && bash "$BUILDSH" "${BUILD_ARGS[@]}" ) 2>&1 || RC_BUILD=$?
fi
echo "$BUILD_MARK_END"

# Classify the failure. Priority order is STAGE-ACCURATE: the compiler's own
# errors are checked FIRST, because a Clang error means UHT already ran and
# SUCCEEDED — the UHT-generated .gen.cpp/.gen.h sources are exactly what Clang
# is compiling, so UHT-generated file names appearing in Clang include traces
# are normal and are NOT evidence of UHT rejection. UHT evidence is restricted
# to UHT's OWN error format (a bare UHT mention, GENERATED_BODY or UObject/
# tokens in compiler output do NOT count).
#
#   1. C++ COMPILATION      — Clang error signature (file:line:col: error: ...)
#   2. LINKING              — unambiguous linker tokens
#   3. UHT / HEADER PARSE   — UHT's own error format ("File.h(N): Error: ...",
#                            "Unable to find 'class/enum/...' with name", ...)
#   4. BUILD INVOCATION     — command/args/environment; compiler never ran
#   5. UBT EXCEPTION        — UnrealBuildTool (.NET) terminated with an unhandled
#                            aggregate exception and no earlier evidence-based cause
#                            was identified. The underlying exception (type,
#                            message, "at UnrealBuildTool...." stack) is printed
#                            in the detail section below — this is NOT a confirmed
#                            UHT failure without UHT evidence.
#   6. UNCLASSIFIED
BUILD_OUTPUT="$(awk '/@@TDD_BUILD_OUTPUT_BEGIN@@/{f=1;next} /@@TDD_BUILD_OUTPUT_END@@/{f=0} f' "$LOG")"
if [ "$RC_BUILD" -eq 0 ]; then
  pass "SUCCESS — Build.sh exited 0: TDD_GAME COMPILED (compile-verified ONLY, not runtime)."
  echo "[diag] NEXT (owner): open TDD_GAME.uproject in the UE 5.8 editor, create"
  echo "        OMEGA_VALLEY_PHASE1.umap (empty level), set World Settings -> Game Mode"
  echo "        = TDD_GAME.TDDOmegaValleyGameMode, place a Player Start, PIE."
  echo "[diag] See docs/06_IMPLEMENTATION/WORLD/PHASE1_IMPLEMENTATION_EVIDENCE_AND_BUILD_PROCEDURE.md §4.4-4.5."
  exit 0
else
  # Evidence flags. CLANG_ERROR uses the compiler's own signature
  # (path:line[:col]: error:/fatal error:), which is distinct from UHT's
  # "File.h(N): Error:" format. UHT_EVIDENCE is restricted to UHT's own error
  # format: a bare UHT mention, GENERATED_BODY or UObject/ tokens (which appear
  # in Clang include traces of UHT-generated files) are NOT UHT rejection.
  CLANG_ERROR=0
  if grep -qE "[A-Za-z0-9_./\-]+\.(cpp|cc|cxx|c|h|hpp|hh|inl|ipp|m|mm):[0-9]+(:[0-9]+)?: (error|fatal error):|(clang|cc1plus)[: ].*(error|fatal error)" <<<"$BUILD_OUTPUT"; then
    CLANG_ERROR=1
  fi
  UHT_EVIDENCE=0
  if grep -qE "UnrealHeaderTool.*(error|Error|failed|Failed)|(error|Error|failed|Failed).*UnrealHeaderTool|HeaderTool.*(error|Error|failed|Failed)|\.h\([0-9]+\): Error:|Unable to find '(class|delegate|enum|struct)' with name|Invalid use of keyword UENUM|unknown UENUM specifier|unsupported enum underlying type" <<<"$BUILD_OUTPUT"; then
    UHT_EVIDENCE=1
  fi

  if [ "$CLANG_ERROR" -eq 1 ]; then
    CLASS="C++ COMPILATION FAILED — the Clang C++ compiler started and reported errors (UHT had already succeeded; UHT-generated .gen.cpp files appearing in the compiler output are normal include traces, NOT a UHT rejection). Fix C++ with Engineering."
  elif grep -qE "undefined reference|Undefined symbols|cannot find -l|ld:|UndefinedSymbol|linker error|UndefinedSymbols" <<<"$BUILD_OUTPUT"; then
    CLASS="LINKING FAILED — compilation succeeded but the linker reported unresolved symbols (fix C++/link dependencies with Engineering)."
  elif [ "$UHT_EVIDENCE" -eq 1 ]; then
    CLASS="UHT / HEADER PARSE FAILED — Unreal Header Tool rejected the reflected declarations (a reflection/metadata error, NOT a C++ compile error). Fix UENUM/USTRUCT/UCLASS annotations with Engineering."
  elif grep -qE "Failed to find command|Error_Unknown|Unrecognized|command not found|Usage:|No such file|cannot find|does not exist|Invalid|Unable to find|No platforms specified|No configuration specified|not specified for target|Unable to find target|Unknown platform|Invalid platform|Target not found|No target specified|Unsupported" <<<"$BUILD_OUTPUT"; then
    CLASS="BUILD INVOCATION FAILED — the build tool was invoked incorrectly (command/args/environment issue; the compiler never ran)."
  elif grep -qE "Unhandled [0-9]+ aggregate exceptions|Unhandled exception|at UnrealBuildTool" <<<"$BUILD_OUTPUT"; then
    CLASS="UBT EXCEPTION — UnrealBuildTool terminated with an unhandled .NET exception and no upstream cause was identified from the output. The underlying exception is printed in the detail section below. This is NOT a confirmed UHT failure (no UHT-specific error evidence)."
  else
    CLASS="BUILD FAILED — unclassified (see the log tail below)."
  fi
  fail "Build.sh exited $RC_BUILD — $CLASS"
  echo
  echo "================================================================"
  echo " BUILD FAILURE — $CLASS"
  echo " (exact command + diagnostics; also persisted in $LOG)"
  echo "================================================================"
  echo "Exact build command:"
  printf '  %q' "${BUILD_CMD[@]}"; echo
  echo
  echo "---- classification ----"
  echo "  $CLASS"
  echo
  echo "---- UHT activity (did UHT run?) ----"
  UHT_LINES=$(grep -cE "UnrealHeaderTool|UHT" <<<"$BUILD_OUTPUT")
  if [ "$UHT_LINES" -gt 0 ]; then
    echo "  UHT-related lines in build output: $UHT_LINES (UHT was invoked/mentioned by UBT)"
    grep -nE "UnrealHeaderTool|UHT" <<<"$BUILD_OUTPUT" | tail -n 10
  else
    echo "  No UHT invocation lines in the build output — UHT did not run (or its output was not captured)."
  fi
  echo
  echo "---- first meaningful compiler error (preserved) ----"
  FIRST_ERROR=$(grep -m1 -nE "[A-Za-z0-9_./\-]+\.(cpp|cc|cxx|c|h|hpp|hh|inl|ipp|m|mm):[0-9]+(:[0-9]+)?: (error|fatal error):|(clang|cc1plus)[: ].*(error|fatal error)" <<<"$BUILD_OUTPUT")
  if [ -n "$FIRST_ERROR" ]; then
    echo "$FIRST_ERROR"
  else
    echo "(no compiler error line found; the failing stage is reported above)"
  fi
  echo
  echo "---- underlying exception / error detail (full capture, not tail) ----"
  DETAIL=$(grep -nE "Unhandled exception|at UnrealBuildTool|Unhandled [0-9]+ aggregate|Error:|error:|fatal error:|Exception|Unable to find|Invalid use" <<<"$BUILD_OUTPUT" | tail -n 60)
  if [ -n "$DETAIL" ]; then
    echo "$DETAIL"
  else
    echo "(no exception/error detail lines found in the build output)"
  fi
  echo
  echo "---- last 60 lines of build output ----"
  tail -n 60 "$LOG"
  echo
  echo "[diag] ACTION: send the full log ($LOG) to Engineering. Do NOT fix C++ yourself."
  echo "[diag] Engineering owns all Phase-1 C++ fixes. Phase 1 remains IMPLEMENTED_UNVERIFIED."
  exit "$RC_BUILD"
fi
