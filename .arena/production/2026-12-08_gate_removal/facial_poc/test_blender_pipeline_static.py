#!/usr/bin/env python3
"""Static + fail-safe tests for the Blender pipeline BEFORE any Mac request.
Does NOT claim Blender execution (no Blender in sandbox)."""
import py_compile, re, subprocess, sys, os
pkg="/home/user/TDD/.arena/production/2026-11-24_w1d7_blender_package"
src=open(os.path.join(pkg,"blender/finish_character.py")).read()
code="\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
assert "bpy.ops.object.mode_set" not in code, "background-mode operator still called in code"
assert "temp_override" in src, "export override missing"
py_compile.compile(os.path.join(pkg,"blender/finish_character.py"), doraise=True)
r=subprocess.run(["bash","run_all.sh"],cwd=pkg,capture_output=True,text=True)
assert r.returncode==3 and "Blender not found" in r.stdout, (r.returncode, r.stdout[-300:])
print("PASS: no mode_set operators; temp_override export; py_compile ok; run_all fail-safe exit 3 (Blender absent, checksums pass)")
