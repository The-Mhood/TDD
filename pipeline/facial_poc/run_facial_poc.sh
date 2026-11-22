#!/usr/bin/env bash
# run_facial_poc.sh — Orchestrates the Adanna facial-likeness PoC on the owner Mac.
# The Disobedient Daughter · zero-budget facial likeness (TDD-IMPL-FACIAL-001)
#
# Run ON THE OWNER MAC (the only machine with Blender + UE). v2.2: STRICT error
# handling — Python exceptions and Blender non-zero exits cannot be reported as a
# successful run. The expected output files are verified after each step. Do NOT claim
# the face is reviewed/tested until this completes GREEN and the owner records the
# evidence bundle (see FACIAL_POC_RUNBOOK.md / FACIAL_POC_OWNER_EXECUTION_PROCEDURE.md).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/output"
EVID="$OUT/evidence"
mkdir -p "$OUT" "$EVID"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUNLOG="$EVID/RUN_${TS}.log"
: > "$RUNLOG"

BLENDER_BIN="${BLENDER_BIN:-blender}"
echo "[run] timestamp=$TS" | tee -a "$RUNLOG"
echo "[run] blender=$($BLENDER_BIN --version 2>/dev/null | head -1)" | tee -a "$RUNLOG"

# Verify a file exists and is non-empty.
require_file() {
  local f="$1" label="$2"
  if [ ! -s "$f" ]; then
    echo "[run] MISSING OUTPUT: $label -> $f" | tee -a "$RUNLOG"
    return 1
  fi
  echo "[run] ok: $label ($f)" | tee -a "$RUNLOG"
}

# Portable sha256 (Linux: sha256sum; macOS: shasum -a 256). Avoids `sha256`, which is not
# portable and would abort the script under `set -e` with exit 127.
hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" 2>/dev/null
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" 2>/dev/null
  elif command -v sha256 >/dev/null 2>&1; then
    sha256 "$1" 2>/dev/null
  else
    echo "[run] WARNING: no sha256 tool found; skipping hash for $1" | tee -a "$RUNLOG"
  fi
}

# STEP 1/4 — build
echo "[run] STEP 1/4 build facial PoC" | tee -a "$RUNLOG"
RC_BUILD=0
$BLENDER_BIN -b -P "$HERE/build_adanna_facial_poc.py" 2>&1 | tee -a "$RUNLOG" || RC_BUILD=$?
echo "[run] build exit=$RC_BUILD" | tee -a "$RUNLOG"

if [ "$RC_BUILD" -ne 0 ]; then
  echo "[run] BUILD FAILED (exit $RC_BUILD) — capture $RUNLOG, do not proceed" | tee -a "$RUNLOG"
  exit "$RC_BUILD"
fi

# Verify build produced its required artifacts.
for f in "$OUT/ADANNA_FACIAL_POC_V2.blend" "$OUT/ADANNA_FACIAL_POC_V2.fbx" \
         "$EVID/BUILD_MANIFEST.json"; do
  require_file "$f" "build output" || { echo "[run] BUILD ARTIFACTS INCOMPLETE" | tee -a "$RUNLOG"; exit 1; }
done

# STEP 2/4 — verify (qualification QC). The verifier exits non-zero on FAILED verdict.
echo "[run] STEP 2/4 verify (qualification QC)" | tee -a "$RUNLOG"
RC_QC=0
$BLENDER_BIN -b -P "$HERE/verify_facial_poc.py" 2>&1 | tee -a "$RUNLOG" || RC_QC=$?
echo "[run] verify exit=$RC_QC" | tee -a "$RUNLOG"

# QC must have produced its report AND exited 0 (QUALIFIED). A non-zero QC exit means FAILED.
if [ "$RC_QC" -ne 0 ]; then
  echo "[run] QC FAILED (exit $RC_QC) — see QC_RESULT.json; do not treat as success" | tee -a "$RUNLOG"
fi
require_file "$EVID/QC_RESULT.json" "QC report" || { echo "[run] QC REPORT MISSING" | tee -a "$RUNLOG"; exit 1; }

# STEP 3/4 — package evidence
echo "[run] STEP 3/4 package evidence" | tee -a "$RUNLOG"
{
  echo "run_timestamp=$TS"
  echo "build_exit=$RC_BUILD"
  echo "verify_exit=$RC_QC"
  echo "--- build manifest ---"
  cat "$EVID/BUILD_MANIFEST.json" 2>/dev/null
  echo
  echo "--- QC result ---"
  cat "$EVID/QC_RESULT.json" 2>/dev/null
  echo
  echo "--- artifact hashes ---"
  hash_file "$OUT/ADANNA_FACIAL_POC_V2.fbx"
  hash_file "$OUT/ADANNA_FACIAL_POC_V2.blend"
  echo "--- preview renders ---"
  ls -1 "$OUT/previews" 2>/dev/null
} > "$EVID/EVIDENCE_BUNDLE_${TS}.txt" 2>&1
echo "[run] evidence bundle -> $EVID/EVIDENCE_BUNDLE_${TS}.txt" | tee -a "$RUNLOG"

# STEP 4/4 — report. UE import is a SEPARATE owner step (see runbook).
echo "[run] STEP 4/4 — UE import is a SEPARATE owner step (see runbook). Blender pipeline done." | tee -a "$RUNLOG"

if [ "$RC_QC" -ne 0 ]; then
  echo "[run] DONE (QC FAILED) build=$RC_BUILD verify=$RC_QC — face NOT qualified" | tee -a "$RUNLOG"
  exit "$RC_QC"
fi
echo "[run] DONE (QC QUALIFIED) build=$RC_BUILD verify=$RC_QC" | tee -a "$RUNLOG"
exit 0
