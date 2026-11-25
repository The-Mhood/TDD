#!/usr/bin/env python3
"""Regression tests for the build_readiness enabled-plugin resolution audit.

UE 5.8.4 has no standalone "glTF" plugin (glTF import is provided by the
default-enabled Interchange Framework). A stale "glTF" plugin declaration makes
UBT fail with "Unable to find plugin 'glTF'". _audit_enabled_plugins must flag
such stale declarations while allowing known engine plugins and project-local
plugins.

Run:  python3 Tools/tests/test_build_readiness_plugins.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
READINESS_PATH = ROOT / "Tools" / "engine" / "build_readiness.py"


def load_readiness():
    spec = importlib.util.spec_from_file_location("build_readiness", READINESS_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PASSED = 0
FAILED = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print("  PASS  " + name)
    else:
        FAILED += 1
        print("  FAIL  " + name + (("  -> " + detail) if detail else ""))


def write_uproject(project_dir: Path, plugins: list) -> Path:
    project_dir.mkdir(parents=True, exist_ok=True)
    up = project_dir / "PROJ.uproject"
    up.write_text(json.dumps({
        "FileVersion": 3,
        "EngineAssociation": "5.8",
        "Modules": [{"Name": "PROJ", "Type": "Runtime"}],
        "Plugins": plugins,
    }), encoding="utf-8")
    return up


def test_stale_gltf_flagged(br):
    print("[test] stale glTF plugin is flagged")
    with tempfile.TemporaryDirectory() as td:
        proj = Path(td) / "proj"
        up = write_uproject(proj, [{"Name": "glTF", "Enabled": True}])
        issues = br._audit_enabled_plugins(up, proj)
        names = [n for n, _ in issues]
        check("stale glTF plugin reported", "glTF" in names, str(issues))
        check("glTF issue has a non-empty reason",
              any(n == "glTF" and r for n, r in issues), str(issues))


def test_known_engine_plugins_allowed(br):
    print("[test] known engine plugins are allowed")
    with tempfile.TemporaryDirectory() as td:
        proj = Path(td) / "proj"
        up = write_uproject(proj, [
            {"Name": "PythonScriptPlugin", "Enabled": True},
            {"Name": "Interchange", "Enabled": True},
            {"Name": "InterchangeFramework", "Enabled": True},
            {"Name": "Niagara", "Enabled": True},
        ])
        issues = br._audit_enabled_plugins(up, proj)
        check("known engine plugins produce no issues", issues == [], str(issues))


def test_project_local_plugin_allowed(br):
    print("[test] project-local plugin is allowed")
    with tempfile.TemporaryDirectory() as td:
        proj = Path(td) / "proj"
        (proj / "Plugins" / "MyLocalPlugin").mkdir(parents=True, exist_ok=True)
        up = write_uproject(proj, [{"Name": "MyLocalPlugin", "Enabled": True}])
        issues = br._audit_enabled_plugins(up, proj)
        check("project-local plugin produces no issues", issues == [], str(issues))


def test_disabled_plugin_ignored(br):
    print("[test] disabled plugin is ignored")
    with tempfile.TemporaryDirectory() as td:
        proj = Path(td) / "proj"
        up = write_uproject(proj, [{"Name": "glTF", "Enabled": False}])
        issues = br._audit_enabled_plugins(up, proj)
        check("disabled glTF plugin not flagged", issues == [], str(issues))


def test_real_projects_clean(br):
    print("[test] real project uprojects are clean")
    m1 = ROOT / "TDD_PHASE3_PRODUCTION" / "PLAYABLE_ADANNA_M1" / "ue_project" / "TDD_GAME.uproject"
    root_up = ROOT / "TheDisobedientDaughter.uproject"
    m1_issues = br._audit_enabled_plugins(m1, m1.parent) if m1.is_file() else ["missing"]
    root_issues = br._audit_enabled_plugins(root_up, root_up.parent) if root_up.is_file() else ["missing"]
    check("TDD_GAME.uproject has no stale plugin declarations",
          m1_issues == [], str(m1_issues))
    check("TheDisobedientDaughter.uproject has no stale plugin declarations",
          root_issues == [], str(root_issues))
    check("TDD_GAME.uproject no longer declares glTF",
          "glTF" not in [n for n, _ in m1_issues], str(m1_issues))


def test_gltf_not_in_known_plugins(br):
    print("[test] glTF is not a known UE 5.8.4 engine plugin")
    check("'glTF' not in KNOWN_UE_ENGINE_PLUGINS",
          "glTF" not in br.KNOWN_UE_ENGINE_PLUGINS)
    check("'Interchange' is a known UE 5.8.4 engine plugin",
          "Interchange" in br.KNOWN_UE_ENGINE_PLUGINS)
    check("'PythonScriptPlugin' is a known UE 5.8.4 engine plugin",
          "PythonScriptPlugin" in br.KNOWN_UE_ENGINE_PLUGINS)


def main():
    br = load_readiness()
    test_stale_gltf_flagged(br)
    test_known_engine_plugins_allowed(br)
    test_project_local_plugin_allowed(br)
    test_disabled_plugin_ignored(br)
    test_real_projects_clean(br)
    test_gltf_not_in_known_plugins(br)
    print()
    print("RESULT: %d passed, %d failed" % (PASSED, FAILED))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
