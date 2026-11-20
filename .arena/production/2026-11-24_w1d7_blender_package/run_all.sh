#!/usr/bin/env bash
# W1 D7 Blender workstation package — single entry point (macOS, Apple Silicon).
# Usage:  ./run_all.sh            (from this folder, on the Mac)
# Optional: BLENDER=/path/to/Blender ./run_all.sh
set -euo pipefail

PKG_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$PKG_DIR/../../.." && pwd)"
D7="$REPO_ROOT/.arena/production/2026-11-23_w1d7_production"
D8="$REPO_ROOT/.arena/production/2026-11-25_w1d8_sculpt"
OUT="$PKG_DIR/output"
mkdir -p "$OUT"

# ---- 1. Locate Blender -----------------------------------------------------
BLENDER_BIN="${BLENDER:-}"
if [[ -z "$BLENDER_BIN" ]]; then
  for cand in "/Applications/Blender.app/Contents/MacOS/Blender" \
              "$HOME/Applications/Blender.app/Contents/MacOS/Blender" \
              "$(command -v blender 2>/dev/null || true)"; do
    if [[ -n "$cand" && -x "$cand" ]]; then BLENDER_BIN="$cand"; break; fi
  done
fi
if [[ -z "${BLENDER_BIN:-}" || ! -x "$BLENDER_BIN" ]]; then
  echo "ERROR: Blender not found. Install Blender 4.2 LTS (macOS Apple Silicon build)"
  echo "from https://www.blender.org/download/lts/ , drag Blender.app to /Applications,"
  echo "then re-run ./run_all.sh  (or: BLENDER=/path/to/Blender ./run_all.sh)"
  exit 3
fi
VER="$("$BLENDER_BIN" --version | head -1)"
echo "Using: $BLENDER_BIN"
echo "Version: $VER"
case "$VER" in
  *" 4."*) : ;;
  *) echo "ERROR: Blender 4.x required (package qualified on 4.2 LTS). Found: $VER"; exit 3 ;;
esac

# ---- 2. Verify inputs (fail fast with exact missing path) -------------------
for f in "$D8/out/ADANNA_AD03_V3.glb" "$D8/out/GUARD_CLASS_V2.glb" \
         "$PKG_DIR/blender/finish_character.py" "$D7/pipeline/test_deformation.py"; do
  if [[ ! -f "$f" ]]; then echo "ERROR: missing input: $f"; echo "Run from a full checkout of branch arena/6e649a9b-tdd."; exit 4; fi
done
if command -v shasum >/dev/null; then
  (cd "$REPO_ROOT" && shasum -a 256 -c "$PKG_DIR/INPUT_CHECKSUMS.sha256") || {
    echo "ERROR: input checksum mismatch — repo checkout differs from the qualified package."
    echo "Recovery: git fetch && git checkout arena/6e649a9b-tdd && git pull, then re-run."; exit 4; }
fi

# ---- 2b. Source-level joint-influence regression gate (catches dead bones) --
if command -v python3 >/dev/null; then
  echo "=== joint-influence regression test ==="
  (cd "$D7/pipeline" && python3 test_joint_influence.py "$D8/out/ADANNA_AD03_V3.glb" > "$OUT/ADANNA_AD03_V3_JOINT_INFLUENCE.json")
  (cd "$D7/pipeline" && python3 test_joint_influence.py "$D8/out/GUARD_CLASS_V2.glb"  > "$OUT/GUARD_CLASS_V2_JOINT_INFLUENCE.json")
fi

# ---- 3. Finish both characters ----------------------------------------------
run_char() {
  local name="$1" glb="$2"
  echo "=== $name ==="
  mkdir -p "$OUT/$name"
  "$BLENDER_BIN" -b --factory-startup --python "$PKG_DIR/blender/finish_character.py" \
    -- --input "$glb" --name "$name" --outdir "$OUT/$name"
  if [[ ! -f "$OUT/$name/${name}.blend" || ! -f "$OUT/$name/${name}.fbx" ]]; then
    echo "ERROR: $name outputs missing — see log above and $OUT/$name/${name}_BLENDER_QC.json"; exit 5
  fi
}
run_char "ADANNA_AD03_V3" "$D8/out/ADANNA_AD03_V3.glb"
run_char "GUARD_CLASS_V2" "$D8/out/GUARD_CLASS_V2.glb"

# ---- 4. Independent (non-Blender) validation --------------------------------
if command -v python3 >/dev/null; then
  echo "=== deformation re-check (pure Python, no Blender) ==="
  python3 "$D7/pipeline/test_deformation.py" "$D8/out/ADANNA_AD03_V3.glb" > "$OUT/ADANNA_AD03_V3_DEFORM_RECHECK.json"
  python3 "$D7/pipeline/test_deformation.py" "$D8/out/GUARD_CLASS_V2.glb"  > "$OUT/GUARD_CLASS_V2_DEFORM_RECHECK.json"
fi

echo ""
echo "DONE. Outputs in: $OUT"
find "$OUT" -type f | sort
echo ""
echo "Next: open the 8 PNGs in output/*/previews/, eyeball front/three-quarter/side/back,"
echo "then commit output/ back to branch arena/6e649a9b-tdd (or hand the folder to Design)."
