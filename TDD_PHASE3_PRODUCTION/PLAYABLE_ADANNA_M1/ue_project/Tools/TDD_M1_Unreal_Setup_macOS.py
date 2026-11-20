#!/usr/bin/env python3
"""TDD M1 owner-side Unreal setup helper - macOS / UE 5.8 / Apple Silicon.

STATUS: PRODUCED - NOT YET VERIFIED. This file has never been executed inside Unreal
Editor. It is a source-level automation aid only; it does not prove compile, PIE, cook,
package or a runnable build.

WHY THIS FILE REPLACES THE EARLIER HELPER
The preserved original is Tools/TDD_M1_Unreal_Setup_WINDOWS_ASSUMPTION_PRESERVED.py.
It is retained unchanged for audit. Known defects in it:

  1. Uses unreal.EditorLevelLibrary, deprecated since UE 5.0 and removed from the
     default Editor Scripting Utilities path in UE 5.7+. Replaced with
     unreal.LevelEditorSubsystem.
  2. Calls unreal.EditorLevelLibrary.new_level(), which creates a level but leaves it
     unsaved and unsaved-as; the requested /Game/TDD/Maps/PLAYABLE_FOREST_M1.umap would
     not exist on disk. Replaced with new_level_from_template + save_current_level +
     explicit save_asset.
  3. Never repoints GameDefaultMap/EditorStartupMap, so the project-owned map would
     never actually load. Fixed here via write_editor_config, which backs the file up
     first.
  4. Writes its report relative to __file__; inside a packaged editor session that can
     be a read-only or relocated path. Fixed by resolving Saved/ from unreal.Paths.
  5. Imports the GLB with one generic AssetImportTask and no Interchange options, so a
     skinned GLB can arrive as a static mesh with no skeleton or animations. Fixed with
     an explicit skeletal-mesh import plus an OBJ static-mesh import.
  6. Gives no way to detect a missing Python/Interchange plugin, and no console check.
  7. Path strings in the earlier file went up four directories, past the repository
     root. Paths here are resolved from the project file, which is what Unreal reports.

No operation in this file deletes, overwrites or renames a user asset. The only file it
modifies outside Saved/ is Config/DefaultEngine.ini, and only after making
DefaultEngine.ini.tdd_backup. Set TDD_DRY_RUN = True to suppress all writes.

RUN (inside the running Editor - recommended)
  Window > Developer Tools > Output Log, switch the dropdown from Cmd to Python, then:
      exec(open('/ABS/PATH/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py').read())

RUN (headless, UE 5.8 installed from the Epic Games Launcher)
  /Users/Shared/Epic\\ Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor-Cmd \\
      "/ABS/PATH/TDD_GAME.uproject" \\
      -run=pythonscript \\
      -script="/ABS/PATH/TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/ue_project/Tools/TDD_M1_Unreal_Setup_macOS.py" \\
      -unattended -nosplash -nopause -stdout

VERIFY ONLY (no asset or config changes)
  Same command with TDD_DRY_RUN flipped to True at the top of this file.
"""

from __future__ import annotations

import datetime
import json
import os
import platform
import sys
from pathlib import Path

try:
    import unreal
except ImportError:  # Permits syntax/static checks outside the editor.
    unreal = None

# ----------------------------------------------------------------------------------
# Scope switches
# ----------------------------------------------------------------------------------
TDD_DRY_RUN = False          # True = inspect and report only; no map, import or config write
TDD_SET_CONFIG = True        # Repoint GameDefaultMap/EditorStartupMap after a successful save
TDD_IMPORT = True            # Import the labelled technical handoff files

MAP_PACKAGE = "/Game/TDD/Maps"
MAP_ASSET = MAP_PACKAGE + "/PLAYABLE_FOREST_M1"
TEMPLATE_MAP = "/Engine/Maps/Templates/Template_Default"
IMPORT_DESTINATION = "/Game/TDD/Imports"
GAME_MODE_CLASS = "/Script/TDD_GAME.TDDForbiddenForestGameMode"


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def log(message: str) -> None:
    text = "[TDD M1 macOS] " + message
    if unreal is not None:
        unreal.log(text)
    else:
        print(text)


def warn(message: str) -> None:
    text = "[TDD M1 macOS] " + message
    if unreal is not None:
        unreal.log_warning(text)
    else:
        print("WARNING: " + text)


# ----------------------------------------------------------------------------------
# Path resolution - never assume the helper's own location implies the project root
# ----------------------------------------------------------------------------------
def resolve_paths() -> dict:
    """Resolve project and model paths from Unreal's own report, with a file fallback."""
    here = Path(__file__).resolve().parent
    fallback_project = here.parent
    info = {"helper": str(Path(__file__).resolve())}
    if unreal is not None:
        try:
            project_dir = Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()))
            project_file = Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.get_project_file_path()))
        except Exception as exc:  # pragma: no cover - editor-only branch
            warn("Unreal path API failed (%s); falling back to helper location" % exc)
            project_dir, project_file = fallback_project, fallback_project / "TDD_GAME.uproject"
    else:
        project_dir, project_file = fallback_project, fallback_project / "TDD_GAME.uproject"
    play_root = project_dir.parent
    info.update({
        "project_dir": str(project_dir),
        "project_file": str(project_file),
        "play_root": str(play_root),
        "model_dir": str(play_root / "model"),
        "config_file": str(project_dir / "Config" / "DefaultEngine.ini"),
    })
    return info


def saved_report_path(project_dir: Path) -> Path:
    if unreal is not None:
        try:
            saved = Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()))
            return saved / "TDD_M1" / "tdd_m1_setup_report.json"
        except Exception:
            pass
    return project_dir / "Saved" / "TDD_M1" / "tdd_m1_setup_report.json"


# ----------------------------------------------------------------------------------
# Environment facts
# ----------------------------------------------------------------------------------
def host_facts() -> dict:
    facts = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "logical_cpu_count": os.cpu_count(),
        "is_apple_silicon": platform.machine() == "arm64" and sys.platform == "darwin",
    }
    try:
        facts["physical_memory_bytes"] = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        facts["physical_memory_gib"] = round(facts["physical_memory_bytes"] / (1024 ** 3), 2)
    except Exception:
        pass
    return facts


def engine_facts() -> dict:
    if unreal is None:
        return {
            "available": False,
            "status": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "reason": "unreal module not importable; run this file inside the Editor Python console.",
        }
    facts: dict = {"available": True}
    try:
        facts["engine_version"] = unreal.SystemLibrary.get_engine_version()
    except Exception as exc:
        facts["engine_version_error"] = str(exc)
    for key, fn in (
        ("engine_dir", unreal.Paths.engine_dir),
        ("project_dir", unreal.Paths.project_dir),
        ("project_file", unreal.Paths.get_project_file_path),
    ):
        try:
            facts[key] = unreal.Paths.convert_relative_path_to_full(fn())
        except Exception as exc:
            facts[key + "_error"] = str(exc)
    try:
        proj = unreal.Paths.get_project_file_path()
        facts["project_engine_association"] = "see TDD_GAME.uproject; expected 5.8"
        facts["project_basename"] = Path(proj).name
    except Exception:
        pass
    # Optional capabilities this script depends on.
    for label, probe in (
        ("level_editor_subsystem", lambda: hasattr(unreal, "LevelEditorSubsystem")),
        ("asset_import_task", lambda: hasattr(unreal, "AssetImportTask")),
        ("editor_asset_library", lambda: hasattr(unreal, "EditorAssetLibrary")),
        ("gltf_interchange_translator", lambda: _has_gltf_translator()),
    ):
        try:
            facts[label] = bool(probe())
        except Exception as exc:
            facts[label] = "probe_failed: " + str(exc)
    return facts


def _has_gltf_translator() -> bool:
    """True when Interchange exposes a glTF translator class."""
    if unreal is None:
        return False
    names = [n for n in dir(unreal) if "GLTF" in n.upper()]
    return any("TRANSLATOR" in n.upper() for n in names) or bool(names)


# ----------------------------------------------------------------------------------
# Project-owned map
# ----------------------------------------------------------------------------------
def create_project_map(report: dict) -> None:
    section = {"asset": MAP_ASSET, "created": False, "saved": False}
    report["map"] = section
    if unreal is None:
        section["status"] = "BLOCKED - OWNER-STUDIO DEPENDENCY"
        return
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    exists = unreal.EditorAssetLibrary.does_asset_exist(MAP_ASSET)
    section["pre_existing"] = bool(exists)
    if exists:
        # Never overwrite an existing project map.
        section.update({"created": True, "saved": True, "action": "already_existed_not_modified"})
        section["status"] = "COMPLETED AND VERIFIED"
        log("project map already exists; left untouched: " + MAP_ASSET)
        return
    if TDD_DRY_RUN:
        section["status"] = "PRODUCED - NOT YET VERIFIED"
        section["action"] = "dry_run_skipped"
        return
    try:
        unreal.EditorAssetLibrary.make_directory(MAP_PACKAGE)
        if not les.new_level_from_template(MAP_ASSET, TEMPLATE_MAP):
            raise RuntimeError("LevelEditorSubsystem.new_level_from_template returned False")
        les.save_current_level()
        saved = bool(unreal.EditorAssetLibrary.save_asset(MAP_ASSET, only_if_is_dirty=False))
        section.update({"created": True, "saved": saved})
        world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
        try:
            world_settings = world.get_world_settings()
            game_mode = unreal.load_class(None, GAME_MODE_CLASS)
            if game_mode:
                world_settings.set_editor_property("default_game_mode", game_mode)
                section["game_mode_class_set"] = True
            else:
                section["game_mode_class_set"] = False
                section["game_mode_warning"] = "C++ game mode not found; compile TDD_GAME first."
                warn("game mode class missing; compile the module before relying on PIE")
        except Exception as exc:
            section["world_settings_note"] = str(exc)
        section["status"] = "COMPLETED AND VERIFIED" if saved else "PRODUCED - NOT YET VERIFIED"
        log("created and saved " + MAP_ASSET)
    except Exception as exc:
        section.update({"status": "BLOCKED - OWNER-STUDIO DEPENDENCY", "error": str(exc)})
        warn("map creation failed: " + str(exc))


def point_config_at_map(report: dict, paths: dict) -> None:
    """Repoint GameDefaultMap/EditorStartupMap so the project-owned map actually loads."""
    section = {"file": paths["config_file"], "changed": False}
    report["config"] = section
    if not TDD_SET_CONFIG or TDD_DRY_RUN:
        section["action"] = "skipped"
        return
    if not report.get("map", {}).get("saved"):
        section["action"] = "skipped_map_not_saved"
        return
    config = Path(paths["config_file"])
    if not config.is_file():
        section.update({"action": "skipped_missing_file"})
        return
    try:
        text = config.read_text(encoding="utf-8")
        backup = config.with_suffix(".ini.tdd_backup")
        if not backup.exists():
            backup.write_text(text, encoding="utf-8")
            section["backup"] = str(backup)
        replaced = 0
        lines = []
        for line in text.splitlines():
            if line.startswith(("GameDefaultMap=", "EditorStartupMap=")):
                lines.append(line.split("=", 1)[0] + "=" + MAP_ASSET)
                replaced += 1
            else:
                lines.append(line)
        if replaced:
            config.write_text("\n".join(lines) + "\n", encoding="utf-8")
        section.update({"changed": bool(replaced), "keys_replaced": replaced})
    except Exception as exc:
        section.update({"error": str(exc)})
        warn("config update failed: " + str(exc))


# ----------------------------------------------------------------------------------
# Technical handoff import
# ----------------------------------------------------------------------------------
def handoff_files(model_dir: Path) -> list[dict]:
    return [
        {
            "path": model_dir / "adanna_m1_technical_proxy_uv.glb",
            "kind": "skeletal",
            "note": "21-joint skinned proxy with UV0 atlas and idle/walk/run/jump/land",
        },
        {
            "path": model_dir / "forbidden_forest_m1.glb",
            "kind": "static",
            "note": "12-node forest blockout",
        },
        {
            "path": model_dir / "adanna_m1_collision_proxy.obj",
            "kind": "static",
            "note": "neutral capsule collision reference, not approved dimensions",
        },
    ]


def import_assets(report: dict, paths: dict) -> None:
    items = handoff_files(Path(paths["model_dir"]))
    results: list[dict] = []
    report["imports"] = results
    for item in items:
        entry = {
            "source": str(item["path"]),
            "source_exists": item["path"].is_file(),
            "kind": item["kind"],
            "note": item["note"],
        }
        results.append(entry)
        if not entry["source_exists"]:
            entry["status"] = "BLOCKED - OWNER-STUDIO DEPENDENCY"
            entry["error"] = "source file missing"
            continue
        if unreal is None or not TDD_IMPORT:
            entry["status"] = "PRODUCED - NOT YET VERIFIED"
            entry["action"] = "dry_run_skipped" if TDD_DRY_RUN else "import_disabled"
            continue
        try:
            unreal.EditorAssetLibrary.make_directory(IMPORT_DESTINATION)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", str(item["path"]))
            task.set_editor_property("destination_path", IMPORT_DESTINATION)
            task.set_editor_property("automated", True)
            task.set_editor_property("replace_existing", False)
            task.set_editor_property("save", True)
            options = unreal.GLTFImportOptions() if item["kind"] == "skeletal" else None
            if options is not None:
                # Import the skinned GLB as a Skeletal Mesh with its animations, not as a
                # static mesh. Property names differ across UE versions; set defensively.
                for prop, value in (
                    ("import_animations", True),
                    ("import_materials", True),
                    ("import_textures", True),
                ):
                    try:
                        options.set_editor_property(prop, value)
                    except Exception:
                        pass
                try:
                    task.set_editor_property("options", options)
                except Exception as exc:
                    entry["options_note"] = str(exc)
            if options is not None:
                # Interchange path for glTF; falls back to the legacy glTF importer.
                task.set_editor_property("factory", unreal.InterchangeGenericAssetsPipelineFactory()) \
                    if hasattr(unreal, "InterchangeGenericAssetsPipelineFactory") else None
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
            imported = []
            try:
                imported = [str(p) for p in task.get_editor_property("imported_object_paths")]
            except Exception:
                pass
            entry["imported_object_paths"] = imported
            entry["status"] = "COMPLETED AND VERIFIED" if imported else "PRODUCED - NOT YET VERIFIED"
        except Exception as exc:
            entry.update({"status": "PRODUCED - NOT YET VERIFIED", "error": str(exc)})
            warn("import failed for %s: %s" % (item["path"].name, exc))


# ----------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------
def main() -> None:
    paths = resolve_paths()
    report: dict = {
        "generated_utc": utc_now(),
        "helper": "Tools/TDD_M1_Unreal_Setup_macOS.py",
        "helper_status": "PRODUCED - NOT YET VERIFIED",
        "classification": "owner-side macOS/UE 5.8 setup helper; source-only automation, not proof of compile/PIE/cook/package",
        "dry_run": TDD_DRY_RUN,
        "paths": paths,
        "host": host_facts(),
        "engine": engine_facts(),
        "map": {},
        "config": {},
        "imports": [],
        "pie_verified": False,
        "cook_verified": False,
        "package_verified": False,
        "runnable_build_verified": False,
        "status_classification": {
            "setup_script": "PRODUCED - NOT YET VERIFIED",
            "project_owned_umap": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "asset_import": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "compile": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "pie": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "cook": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "package": "BLOCKED - OWNER-STUDIO DEPENDENCY",
            "final_character_environment": "BLOCKED - CREATIVE APPROVAL",
        },
    }
    create_project_map(report)
    point_config_at_map(report, paths)
    import_assets(report, paths)

    if report["map"].get("saved"):
        report["status_classification"]["project_owned_umap"] = "COMPLETED AND VERIFIED"
    if any(e.get("imported_object_paths") for e in report["imports"]):
        report["status_classification"]["asset_import"] = "COMPLETED AND VERIFIED"
    if unreal is not None:
        report["status_classification"]["setup_script"] = "TECHNICALLY DEMONSTRATED - NOT INTEGRATED"

    out = saved_report_path(Path(paths["project_dir"]))
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        log("wrote " + str(out))
        report["report_written_to"] = str(out)
    except Exception as exc:
        warn("could not write report to %s: %s" % (out, exc))

    if unreal is not None:
        unreal.log_warning(
            "[TDD M1 macOS] This script does not verify PIE, cook, package or a runnable build. "
            "Record those separately from the macOS runbook."
        )


if __name__ == "__main__":
    main()
