#!/bin/bash
# verify_toolchain.sh - deterministic toolchain gate for the Adanna M1 build.
#
# Answers, on the owner's Mac and without changing anything:
#   CAP-1 native C++ editor compile
#   CAP-2 editor launch + project open + M1 map generation
#   CAP-3 PIE (play-in-editor)
#   CAP-4 Mac ARM64 cook, package and launch
#
# Read-only by default. It never installs, downloads, downgrades or edits
# anything, and it needs elevated rights for nothing.
# --emit-workaround DIR writes the stdin/DEVELOPER_DIR shim described below
#   (only needed if CAP-4 reports FIX-NOT-PRESENT on this engine build).
# --build runs the real editor compile (slow; the only way to prove CAP-1).
#
# Status: PRODUCED - NOT YET VERIFIED (has never run on macOS).
# Written for bash 3.2, which is what /bin/bash is on macOS.

set -uo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPROJECT="$PROJECT_DIR/TDD_GAME.uproject"

MODE="check"
WORKAROUND_DIR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --build) MODE="build" ;;
    --emit-workaround) MODE="workaround"; WORKAROUND_DIR="${2:-}"; shift ;;
    -h|--help)
      sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) echo "unknown argument: $1 (try --help)" >&2; exit 2 ;;
  esac
  shift
done

say()  { printf '%s\n' "$*"; }
head_() { printf '\n== %s ==\n' "$*"; }

FAIL=0
note_fail() { FAIL=$((FAIL+1)); }

# ---------------------------------------------------------------- discovery
find_ue() {
  local c
  for c in "${UE_ROOT:-}" \
           "/Users/Shared/Epic Games/UE_5.8" \
           "/Users/Shared/Epic Games/UE_5.8.4" \
           "/Applications/Epic Games/UE_5.8" \
           "$HOME/Applications/UE_5.8"; do
    if [ -n "$c" ] && [ -f "$c/Engine/Build/Build.version" ]; then
      printf '%s' "$c"; return 0
    fi
  done
  return 1
}

version_ge() { # version_ge A B  -> true if A >= B (dotted, numeric)
  [ "$(printf '%s\n%s\n' "$1" "$2" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)" = "$1" ]
}

json_str() { # json_str FILE KEY  (flat JSON, string or number value)
  sed -n 's/.*"'"$2"'"[[:space:]]*:[[:space:]]*"\{0,1\}\([^",}]*\)"\{0,1\}.*/\1/p' "$1" | head -1 | tr -d ' '
}

# ---------------------------------------------------------------- 1. machine
head_ "1. Host"
OS_VER="$(sw_vers -productVersion 2>/dev/null || echo unknown)"
OS_BUILD="$(sw_vers -buildVersion 2>/dev/null || echo unknown)"
ARCH="$(uname -m 2>/dev/null || echo unknown)"
say "macOS            : $OS_VER ($OS_BUILD)"
say "architecture     : $ARCH"
if command -v sysctl >/dev/null 2>&1; then
  say "RAM              : $(( $(sysctl -n hw.memsize) / 1073741824 )) GB"
else
  say "RAM              : unknown"
fi

if [ "$ARCH" != "arm64" ]; then
  say "VERDICT: NO-GO - this is not an Apple silicon process. Run the script from a native arm64 terminal (not under Rosetta)."
  note_fail
fi
if version_ge "$OS_VER" "26.6"; then
  say "macOS vs Xcode 27: OK (Xcode 27 needs >= 26.6)"
else
  say "macOS vs Xcode 27: FAIL - Xcode 27 cannot run here."
  note_fail
fi

# ---------------------------------------------------------------- 2. Xcode
head_ "2. Xcode"
if command -v xcodebuild >/dev/null 2>&1; then
  XCODE_VER_FULL="$(xcodebuild -version 2>/dev/null | head -1)"
  XCODE_BUILD="$(xcodebuild -version 2>/dev/null | sed -n 's/^Build version //p')"
  XCODE_VER="$(printf '%s' "$XCODE_VER_FULL" | sed -n 's/^Xcode //p')"
  say "xcodebuild       : ${XCODE_VER:-unknown} (${XCODE_BUILD:-unknown})"
  say "developer dir    : $(xcode-select -p 2>/dev/null || echo unset)"
else
  XCODE_VER=""; say "xcodebuild       : NOT FOUND - install Xcode and run: sudo xcode-select -s /Applications/Xcode.app"; note_fail
fi

if xcrun -sdk macosx metal --version >/dev/null 2>&1; then
  METAL_OK=1; say "Metal toolchain  : present"
else
  METAL_OK=0
  say "Metal toolchain  : MISSING - run: xcodebuild -downloadComponent MetalToolchain"
  say "                   (shaders are compiled from source; without it the editor fails to render)"
  note_fail
fi

if [ -n "$XCODE_VER" ] && version_ge "$XCODE_VER" "27.0"; then
  say "Xcode 27+ note   : Mac targets default to arm64 only (no x86_64 slice). This project is arm64-only by design."
fi

# ---------------------------------------------------------------- 3. Engine
head_ "3. Unreal Engine"
UE_ROOT_FOUND="$(find_ue || true)"
if [ -z "$UE_ROOT_FOUND" ]; then
  say "engine           : NOT FOUND - set UE_ROOT=/path/to/UE_5.8 and re-run"
  note_fail
else
  say "engine root      : $UE_ROOT_FOUND"
  BV="$UE_ROOT_FOUND/Engine/Build/Build.version"
  UE_MAJOR="$(json_str "$BV" MajorVersion)"
  UE_MINOR="$(json_str "$BV" MinorVersion)"
  UE_PATCH="$(json_str "$BV" PatchVersion)"
  UE_CL="$(json_str "$BV" Changelist)"
  UE_BRANCH="$(json_str "$BV" BranchName)"
  UE_VER="$UE_MAJOR.$UE_MINOR.$UE_PATCH"
  say "engine version   : $UE_VER  changelist $UE_CL  branch '${UE_BRANCH}'"

  # The Mac finalize fix (UE-396802, stdio for the ApplePostBuildSync xcodebuild)
  # is in 5.8.4 by Epic's statement. The release-note text only names iOS, so
  # confirm the shipped binary instead of trusting either.
  SIX_OK=0
  if [ "$UE_MAJOR.$UE_MINOR" = "5.8" ] && [ "$UE_PATCH" -ge 4 ] 2>/dev/null; then SIX_OK=1; fi
  if [ "$UE_MAJOR.$UE_MINOR" = "5.8" ] && [ "$SIX_OK" = 0 ]; then
    say "VERDICT: NO-GO for CAP-4 only - Mac packaging with Xcode 27 needs 5.8.4 or"; 
    say "         newer; this is $UE_VER. Editor compile, open and PIE are unaffected."
  fi

  UBT="$UE_ROOT_FOUND/Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll"
  FIX_MARKER=0
  if [ -f "$UBT" ] && grep -qa "RedirectStandardInput" "$UBT" 2>/dev/null; then FIX_MARKER=1; fi

  # SDK gate: UBT refuses to build Mac when Xcode is outside Apple_SDK.json.
  SDK_JSON="$UE_ROOT_FOUND/Engine/Config/Apple/Apple_SDK.json"
  SDK_GATE="unknown"
  if [ -f "$SDK_JSON" ]; then
    MAXV="$(python3 - "$SDK_JSON" <<'PY' 2>/dev/null || true
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception:
    sys.exit(0)
def walk(o):
    if isinstance(o,dict):
        name=str(o.get("Platform") or o.get("Name") or o.get("SDK") or "")
        if "mac" in name.lower() or (o.get("MaxVersion") and "IOS" not in name.upper() and "TVOS" not in name.upper()):
            v=o.get("MaxVersion")
            if v: print(str(v)); raise SystemExit
        for v in o.values():
            walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
PY
)"
    MAXV="$(printf '%s' "${MAXV:-}" | head -1 | tr -d ' \r')"
    if [ -n "$MAXV" ] && [ -n "$XCODE_VER" ]; then
      MAXMAJ="${MAXV%%.*}"
      XMAJ="${XCODE_VER%%.*}"
      if [ "$XMAJ" -le "$MAXMAJ" ] 2>/dev/null; then
        SDK_GATE="ok (Xcode $XCODE_VER <= MaxVersion $MAXV)"
      else
        SDK_GATE="blocked (Xcode $XCODE_VER > MaxVersion $MAXV)"
      fi
    fi
    say "Apple SDK gate   : MaxVersion ${MAXV:-unread}; $SDK_GATE"
  fi
  if printf '%s' "$SDK_GATE" | grep -q '^blocked'; then
    say "VERDICT: NO-GO - UBT will report 'Platform Mac is not a valid platform to build'."
    note_fail
  fi

  if [ "$FIX_MARKER" = 1 ]; then
    say "finalize fix     : PRESENT (UBT references RedirectStandardInput)"
  else
    say "finalize fix     : NOT DETECTED - advisory only; if CAP-4 fails at"
    say "                   'Failed to finalize the .app with Xcode', run:"
    say "                   $0 --emit-workaround ~/xcode27-stdin-shim"
  fi
fi

# ---------------------------------------------------------------- 4. checkout
head_ "4. Checkout hygiene"
say "project          : $PROJECT_DIR"
if [ -f "$UPROJECT" ]; then
  say "uproject         : present ($(json_str "$UPROJECT" EngineAssociation))"
  FLAT="$(tr -d '[:space:]' < "$UPROJECT")"
  if printf '%s' "$FLAT" | grep -q '"Name":"PythonScriptPlugin","Enabled":true'; then
    say "Python plugin    : enabled (required by Tools/TDD_M1_Unreal_Setup_macOS.py)"
  else
    say "Python plugin    : not enabled - the M1 map helper will not run"
    note_fail
  fi
else
  say "uproject         : MISSING at $UPROJECT"; note_fail
fi

case "$PROJECT_DIR" in
  "$HOME/Documents"*|"$HOME/Desktop"*|"$HOME/Library/Mobile Documents"*)
    say "iCloud hazard    : FAIL - checkout sits in a Finder/iCloud-synced folder."
    say "                   com.apple.FinderInfo xattrs break codesign even on 5.8.4."
    say "                   Move it, e.g.: mv \"$PROJECT_DIR\" ~/Dev/"
    note_fail ;;
  *) say "iCloud hazard    : OK (outside ~/Documents, ~/Desktop, iCloud Drive)" ;;
esac
if xattr -p com.apple.FinderInfo "$UPROJECT" >/dev/null 2>&1; then
  say "xattrs           : FAIL - com.apple.FinderInfo present on the .uproject"
  say "                   fix: xattr -cr \"$PROJECT_DIR\""
  note_fail
else
  say "xattrs           : OK (no FinderInfo on the .uproject)"
fi
if [ -d "$PROJECT_DIR/Binaries" ] || [ -d "$PROJECT_DIR/Intermediate" ]; then
  say "stale build      : Binaries/ or Intermediate/ exists - for a first clean compile:"
  say "                   rm -rf \"$PROJECT_DIR/Binaries\" \"$PROJECT_DIR/Intermediate\" \"$PROJECT_DIR/Saved\""
else
  say "stale build      : clean tree (no Binaries/Intermediate)"
fi

# ---------------------------------------------------------------- 5. verdict
head_ "5. Verdict"
CAP1="GO"; CAP2="GO"; CAP3="GO"; CAP4="GO"; WHY4="fix present in this engine build"

[ "$FAIL" -gt 0 ] && { CAP1="NO-GO"; CAP2="NO-GO"; CAP3="NO-GO"; CAP4="NO-GO"; }
if [ "${METAL_OK:-0}" = 0 ]; then CAP2="NO-GO"; CAP3="NO-GO"; fi
if [ "${SIX_OK:-0}" = 0 ]; then CAP4="NO-GO"; WHY4="engine older than 5.8.4"; fi
if [ "${SIX_OK:-0}" = 1 ] && [ "${FIX_MARKER:-0}" = 0 ]; then
  CAP4="CONDITIONAL"; WHY4="5.8.4 present, finalize fix not detected in UBT; try --build first, then the stdin shim if it fails"
fi

say "CAP-1 native C++ editor compile ......... $CAP1"
say "CAP-2 editor launch, open project, map .. $CAP2"
say "CAP-3 PIE .............................. $CAP3"
say "CAP-4 cook + package + launch (arm64) .. $CAP4   [$WHY4]"
say ""
say "CAP-1..3 do not depend on the finalize fix: the .app finalize step sits at the"
say "very end of a *game target* build and does not affect editor modules or PIE."

if [ "$MODE" = "build" ]; then
  head_ "6. Real compile (this is the only proof of CAP-1)"
  if [ -n "${UE_ROOT_FOUND:-}" ]; then
    set -x
    "$UE_ROOT_FOUND/Engine/Build/BatchFiles/Mac/Build.sh" TDD_GAMEEditor Mac Development \
      -project="$UPROJECT" -architecture=arm64 -waitmutex
    RC=$?
    set +x
    say ""
    if [ $RC -eq 0 ]; then
      say "RESULT: editor target compiled and linked on this machine. CAP-1 = COMPLETED AND VERIFIED."
    else
      say "RESULT: exit $RC - this is the real first-compile answer. Send the last 40 lines of"
      say "        Engine/Programs/UnrealBuildTool/Log.txt (or the console tail) with the report."
    fi
    exit $RC
  fi
fi

if [ "$MODE" = "workaround" ]; then
  head_ "6. Xcode 27 stdin shim"
  if [ -z "$WORKAROUND_DIR" ]; then
    say "usage: $0 --emit-workaround DIR"; exit 2
  fi
  REAL_DEV="/Applications/Xcode.app/Contents/Developer"
  MIRROR="$WORKAROUND_DIR/XcodeShim.app/Contents/Developer"
  mkdir -p "$MIRROR/usr/bin" || exit 1
  # Symlink every real Developer entry except usr/bin/xcodebuild, which we replace.
  for entry in "$REAL_DEV"/*; do
    base="$(basename "$entry")"
    [ "$base" = "usr" ] && continue
    ln -sfn "$entry" "$MIRROR/$base"
  done
  mkdir -p "$MIRROR/usr"
  for entry in "$REAL_DEV/usr"/*; do
    base="$(basename "$entry")"
    [ "$base" = "bin" ] && continue
    ln -sfn "$entry" "$MIRROR/usr/$base"
  done
  mkdir -p "$MIRROR/usr/bin"
  for entry in "$REAL_DEV/usr/bin"/*; do
    base="$(basename "$entry")"
    [ "$base" = "xcodebuild" ] && continue
    ln -sfn "$entry" "$MIRROR/usr/bin/$base"
  done
  cat > "$MIRROR/usr/bin/xcodebuild" <<EOF
#!/bin/bash
# Give xcodebuild an explicit stdin. Xcode 27 cannot launch the
# "Touch UBT generated tiles" scheme pre-action when fd 0 is closed,
# which is how the UBA executor starts it.
DEVELOPER_DIR="$REAL_DEV" exec "$REAL_DEV/usr/bin/xcodebuild" "\$@" </dev/null
EOF
  chmod +x "$MIRROR/usr/bin/xcodebuild"
  say "shim written: $MIRROR"
  say ""
  say "Use it for one command only; nothing global is changed:"
  say "  DEVELOPER_DIR=\"$MIRROR\" \"\$UE_ROOT/Engine/Build/BatchFiles/RunUAT.sh\" BuildCookRun \\"
  say "    -project=\"$UPROJECT\" -platform=Mac -clientconfig=Development \\"
  say "    -build -cook -stage -pak -package -archive -archivedirectory=\"\$HOME/AdannaPackage\""
  say ""
  say "Keep -package: without it -archive copies the bare Binaries/Mac/TDD_GAME.app,"
  say "which lacks the cooked content."
  exit 0
fi

exit $FAIL
