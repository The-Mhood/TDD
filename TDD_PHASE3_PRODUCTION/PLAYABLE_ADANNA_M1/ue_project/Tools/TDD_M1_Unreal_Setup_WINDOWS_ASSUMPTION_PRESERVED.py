"""PRESERVED AUDIT COPY - do not execute.

This is the original owner-side setup helper exactly as produced against the
provisional UE 5.4 / Windows-era assumption. It is retained unchanged for audit
and superseded by Tools/TDD_M1_Unreal_Setup_macOS.py.

Known defects (all confirmed by inspection, see scripts/audit_ue_macos.py):
  * uses unreal.EditorLevelLibrary, deprecated since UE 5.0 and removed from the
    default path in UE 5.7+
  * calls new_level(), which leaves no saved .umap file on disk
  * never repoints GameDefaultMap/EditorStartupMap
  * writes its report next to the script instead of under Saved/
  * imports a skinned GLB with no skeletal-mesh options
  * project paths resolved four levels up, past the repository root

"""TDD M1 owner-studio Unreal setup helper.

STATUS: PRODUCED — NOT YET VERIFIED.
This file is a source-only automation aid. It must be executed inside the
owner's Unreal Editor Python environment; this sandbox has no Unreal binary.
It does not itself prove compile, PIE, cook, package or a runnable build.

Suggested owner-side invocation after successful module compilation:
  UnrealEditor-Cmd TDD_GAME.uproject -ExecutePythonScript="Tools/TDD_M1_Unreal_Setup.py"
or run it from the Unreal Editor Python console. Read OWNER_STUDIO_UNREAL_REQUEST.md
for the exact installation, hardware and execution evidence still required.
"""

from __future__ import annotations

import datetime
import json
import os
import platform
from pathlib import Path

try:
    import unreal
except ImportError:  # Allows static syntax checking outside Unreal.
    unreal = None

HERE = Path(__file__).resolve().parent
UE_PROJECT = HERE.parent
PLAY = UE_PROJECT.parent
MODEL = PLAY / "model"
REPORT = HERE / "tdd_m1_setup_report.json"
MAP_ASSET = "/Game/TDD/Maps/PLAYABLE_FOREST_M1"
MAP_PACKAGE = "/Game/TDD/Maps"
IMPORT_DESTINATION = "/Game/TDD/Imports"
GAME_MODE_CLASS = "/Script/TDD_GAME.TDDForbiddenForestGameMode"

IMPORT_FILES = [
    MODEL / "adanna_m1_technical_proxy_uv.glb",
    MODEL / "forbidden_forest_m1.glb",
    MODEL / "adanna_m1_collision_proxy.obj",
]


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def basic_host() -> dict:
    host = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "processor": platform.processor(),
        "logical_cpu_count": os.cpu_count(),
    }
    try:
        if hasattr(os, "sysconf"):
            host["physical_memory_bytes"] = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except Exception:
        pass
    return host


def log(message: str) -> None:
    text = "[TDD M1] " + message
    if unreal:
        unreal.log(text)
    else:
        print(text)


def engine_facts() -> dict:
    if not unreal:
        return {
            "available": False,
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "reason": "Unreal Python module not available; run inside the owner's Unreal Editor.",
        }
    try:
        return {
            "available": True,
            "engine_version": unreal.SystemLibrary.get_engine_version(),
            "engine_dir": unreal.Paths.engine_dir(),
            "project_dir": unreal.Paths.project_dir(),
            "project_name": unreal.Paths.get_project_file_path(),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc), "status": "BLOCKED — OWNER-STUDIO DEPENDENCY"}


def create_project_map(report: dict) -> None:
    if not unreal:
        report["map"] = {
            "asset": MAP_ASSET,
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "created": False,
            "saved": False,
        }
        return
    try:
        unreal.EditorAssetLibrary.make_directory(MAP_PACKAGE)
        unreal.EditorLevelLibrary.new_level(MAP_ASSET)
        world = unreal.EditorLevelLibrary.get_editor_world()
        world_settings = world.get_world_settings()
        game_mode = unreal.load_class(None, GAME_MODE_CLASS)
        if game_mode:
            world_settings.set_editor_property("default_game_mode", game_mode)
            report["map"]["game_mode_class_set"] = True
        else:
            report["map"]["game_mode_class_set"] = False
            report["map"]["game_mode_warning"] = "C++ game mode class not found; compile TDD_GAME first."
        unreal.EditorLevelLibrary.save_current_level()
        exists = unreal.EditorAssetLibrary.does_asset_exist(MAP_ASSET)
        report["map"].update({
            "asset": MAP_ASSET,
            "created": bool(exists),
            "saved": bool(exists),
            "status": "COMPLETED AND VERIFIED" if exists else "PRODUCED — NOT YET VERIFIED",
        })
        log("project-owned map created/saved: " + MAP_ASSET)
    except Exception as exc:
        report["map"].update({
            "asset": MAP_ASSET,
            "created": False,
            "saved": False,
            "error": str(exc),
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
        })


def import_assets(report: dict) -> None:
    if not unreal:
        report["imports"] = [{
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "reason": "Unreal Python module not available.",
            "files": [str(p) for p in IMPORT_FILES],
        }]
        return
    try:
        unreal.EditorAssetLibrary.make_directory(IMPORT_DESTINATION)
        tasks = []
        for source in IMPORT_FILES:
            task = unreal.AssetImportTask()
            task.set_editor_property("automated", True)
            task.set_editor_property("destination_path", IMPORT_DESTINATION)
            task.set_editor_property("filename", str(source))
            task.set_editor_property("replace_existing", False)
            task.set_editor_property("save", True)
            tasks.append(task)
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks(tasks)
        results = []
        for source, task in zip(IMPORT_FILES, tasks):
            try:
                imported = list(task.get_editor_property("imported_object_paths"))
            except Exception:
                imported = []
            results.append({
                "source": str(source),
                "source_exists": source.is_file(),
                "imported_object_paths": imported,
                "status": "COMPLETED AND VERIFIED" if imported else "PRODUCED — NOT YET VERIFIED",
            })
        report["imports"] = results
        report["import_plugin_note"] = "Requires the owner's enabled glTF/Interchange/OBJ import pipeline; plugin availability must be recorded separately."
    except Exception as exc:
        report["imports"] = [{
            "status": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "error": str(exc),
            "files": [str(p) for p in IMPORT_FILES],
        }]


def main() -> None:
    report = {
        "generated_utc": utc_now(),
        "classification": "owner-studio Unreal setup helper; source-only automation, not proof of compile/PIE/cook/package",
        "host": basic_host(),
        "engine": engine_facts(),
        "map": {},
        "imports": [],
        "pie_verified": False,
        "cook_verified": False,
        "package_verified": False,
        "runnable_build_verified": False,
        "required_owner_request": "../../../../OWNER_STUDIO_UNREAL_REQUEST.md",
        "status_classification": {
            "setup_script": "PRODUCED — NOT YET VERIFIED",
            "project_owned_umap": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "asset_import": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "compile": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "pie": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "cook": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "package": "BLOCKED — OWNER-STUDIO DEPENDENCY",
            "final_character_environment": "BLOCKED — CREATIVE APPROVAL",
        },
    }
    if report["engine"].get("available"):
        report["status_classification"]["setup_script"] = "TECHNICALLY DEMONSTRATED — NOT INTEGRATED"
        create_project_map(report)
        import_assets(report)
        if report["map"].get("saved"):
            report["status_classification"]["project_owned_umap"] = "COMPLETED AND VERIFIED"
        if any(item.get("imported_object_paths") for item in report["imports"] if isinstance(item, dict)):
            report["status_classification"]["asset_import"] = "COMPLETED AND VERIFIED"
    else:
        create_project_map(report)
        import_assets(report)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    log("wrote " + str(REPORT))
    if unreal:
        unreal.log_warning("[TDD M1] This script does not verify PIE, cook, package or runnable build. Record those separately on owner hardware.")


if __name__ == "__main__":
    main()
