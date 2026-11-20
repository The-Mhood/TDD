#!/bin/bash
# Static guard: the Windows CI helper must never switch/reset a user's branch.
set -u
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
CI="$REPO/Tools/engine/windows_ci.sh"
active="$(sed '/^[[:space:]]*#/d' "$CI")"
if printf '%s\n' "$active" | grep -Eq 'git[^\n]*(checkout|reset[[:space:]]+--hard)'; then
  echo "FAIL: Windows CI contains a branch-switch or destructive reset command" >&2
  exit 1
fi
for required in 'git -C "$REPO" fetch origin "$BRANCH"' 'local_sha=' 'remote_sha=' 'MINGW*|MSYS*|CYGWIN*'; do
  if ! grep -Fq "$required" "$CI"; then
    echo "FAIL: Windows CI safety guard missing: $required" >&2
    exit 1
  fi
done
echo "TDD_RESULT TDD-Tool.WindowsCISafety PASS non_destructive_sync=verified windows_host_gate=present"
