#!/usr/bin/env bash
# Toolchain preflight for the TDD Unreal project.
# Reports what this machine can and cannot do. It never claims a build: it only measures.
# Exit 0 only if an Unreal Engine 5.8 installation and a working C++ toolchain are present.
set -u

ENGINE_PIN="5.8"
PROJECT="$(cd "$(dirname "$0")/../.." && pwd)/TDD.uproject"
fails=0
row() { printf '  %-42s %s\n' "$1" "$2"; }
need() { if [ "$1" = "1" ]; then return 0; else fails=$((fails+1)); return 1; fi; }

echo "TDD toolchain preflight"
echo "  host: $(uname -srm)"
echo "  date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

echo "Project"
if [ -f "$PROJECT" ]; then
  assoc=$(grep -o '"EngineAssociation"[^,]*' "$PROJECT" | head -1 | sed 's/.*: *//; s/"//g')
  row "TDD.uproject" "present"
  row "EngineAssociation" "$assoc (pin $ENGINE_PIN)"
  [ "$assoc" = "$ENGINE_PIN" ] || { row "association matches pin" "NO"; fails=$((fails+1)); }
else
  row "TDD.uproject" "MISSING"; fails=$((fails+1))
fi

echo
echo "Engine"
root="${UE_ROOT:-}"
for cand in "$root" /opt/UnrealEngine /opt/UnrealEngine-5.8 "$HOME/UnrealEngine"; do
  [ -n "$cand" ] && [ -d "$cand" ] && { root="$cand"; break; }
done
if [ -n "$root" ] && [ -d "$root" ]; then
  row "engine root" "$root"
  if [ -f "$root/Engine/Build/Build.version" ]; then
    row "build version" "$(tr -d '\n ' < "$root/Engine/Build/Build.version")"
  else
    row "build version" "Engine/Build/Build.version absent"; fails=$((fails+1))
  fi
  editor="$(ls "$root"/Engine/Binaries/Linux/UnrealEditor 2>/dev/null || true)"
  row "UnrealEditor" "${editor:-absent}"; [ -n "$editor" ] || fails=$((fails+1))
  row "GenerateProjectFiles" "$([ -f "$root/Engine/Build/BatchFiles/Linux/GenerateProjectFiles.sh" ] && echo present || echo absent)"
else
  row "engine root" "NOT FOUND (set UE_ROOT): checked \$UE_ROOT, /opt/UnrealEngine, /opt/UnrealEngine-5.8, ~/UnrealEngine"
  fails=$((fails+1))
fi

echo
echo "Toolchain"
for tool in clang clang++ dotnet mono cmake ninja g++ make; do
  p="$(command -v $tool 2>/dev/null || true)"
  row "$tool" "${p:-MISSING}"
done
# UE 5.8 Linux builds need Clang (bundled with the engine) and .NET; a system clang is a proxy signal.
[ -n "$(command -v clang 2>/dev/null || true)" ] || fails=$((fails+1))

echo
echo "Machine"
cpus=$(nproc 2>/dev/null || echo 0)
mem_gb=$(( $(awk '/MemTotal/ {print int($2/1024/1024)}' /proc/meminfo 2>/dev/null || echo 0) ))
disk_gb=$(df -BG --output=avail "$(dirname "$PROJECT")" 2>/dev/null | tail -1 | tr -dc '0-9')
row "logical CPUs" "$cpus (UE 5.8 source build: 8+ recommended)"
row "RAM" "${mem_gb} GB (UE 5.8 editor: 32 GB recommended, 16 GB minimum)"
row "free disk" "${disk_gb:-0} GB (UE 5.8 source + DDC: 200 GB+ recommended)"
[ "${mem_gb:-0}" -ge 16 ] || fails=$((fails+1))
[ "${disk_gb:-0}" -ge 200 ] || fails=$((fails+1))

echo
if [ "$fails" -eq 0 ]; then
  echo "RESULT: READY — no blocking gap found by this script. This is not a build result."
else
  echo "RESULT: NOT READY — $fails blocking gap(s) above. No build, no editor launch, no test execution is possible here."
fi
echo "This script does not build anything; see docs/06_IMPLEMENTATION/UNREAL_PROJECT_FOUNDATION_V1.md."
exit $([ "$fails" -eq 0 ] && echo 0 || echo 1)
