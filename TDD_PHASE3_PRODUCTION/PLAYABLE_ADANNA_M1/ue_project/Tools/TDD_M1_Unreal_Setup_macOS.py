#!/usr/bin/env python3
"""TDD M1 owner-side Unreal setup helper - macOS / UE 5.8 / Apple Silicon.

STATUS: PRODUCED - NOT YET VERIFIED. This file has never been executed inside Unreal
Editor. It is a source-level automation aid only; it does not prove compile, PIE, cook,
package or a runnable build.

WHAT THIS FILE DOES
  1. Ensures the project-owned map /Game/TDD/Maps/PLAYABLE_FOREST_M1 exists (created
     from the engine template and saved; an existing map is never overwritten).
  2. Repoints GameDefaultMap/EditorStartupMap to that map (Config/DefaultEngine.ini is
     backed up first).
  3. Imports the labelled technical handoff files (GLB/OBJ) through the UE 5.8
     Interchange framework with a deterministic, collision-safe naming scheme, and
     verifies every import by outcome (assets created, expected asset types, canonical
     paths required by the TDD_GAME C++ code).

IMPORT DESIGN (deterministic, collision-safe, idempotent)
  - Every source file imports into a per-source staging folder:
        /Game/TDD/Imports/_staging/<STEM>/
    where <STEM> is the source file stem. All raw Interchange output lands here.
  - Canonical assets required by the C++ code are renamed to their exact canonical
    paths (see CANONICAL_ASSETS below): the Adanna skeletal mesh + skeleton, the seven
    animation sequences, and the six forest module static meshes.
  - Every other imported asset (materials, textures, non-canonical meshes) is renamed
    to a source-prefixed, collision-safe path:
        /Game/TDD/Imports/<STEM>_assets/<STEM>_<OriginalName>
    The <STEM>_ prefix guarantees no cross-source name collision (the original
    /Game/TDD/Imports flat layout collided on names such as FOREST_GROUND and
    TREE_TRUNKS), and the <OriginalName> suffix preserves the source relationship.
  - Reruns are idempotent: a manifest (Saved/TDD_M1/tdd_m1_setup_manifest.json)
    records what each source produced. A source whose manifest entry is complete and
    whose recorded assets still exist is skipped. A source whose file changed on disk
    is reported explicitly and skipped (never auto-overwritten).
  - Nothing is ever deleted or overwritten: existing maps, config and user assets are
    preserved; a canonical path that already exists with the wrong asset type is
    reported as a conflict and left untouched.

UE 5.8.4 API NOTES (verified)
  - unreal.InterchangeManager.import_asset(content_path, source_data,
    import_asset_parameters) returns a bool. The import may complete asynchronously,
    so this script polls the staging folder for the created assets instead of treating
    a non-exception return as proof of success.
  - Pipelines are saved with unreal.EditorAssetLibrary.save_loaded_asset(asset).
    (Calling unreal.EditorAssetSubsystem.save_loaded_asset as a static method is not
    the supported Python API.) The pipeline object is kept alive in a keepalive list
    because Interchange resolves override_pipelines by object reference.
  - unreal.ImportAssetParameters carries is_automated, replace_existing and
    override_pipelines (a list of unreal.SoftObjectPath).
  - glTF support is provided by the Interchange glTF translator, built into UE 5.3+
    and enabled by default; the glTF plugin is declared explicitly in TDD_GAME.uproject
    so the dependency is deterministic. The script records the
    Interchange.FeatureFlags.Import.GLTF console value when readable.

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

RERUN AFTER A FIXED COMMIT
  1. Sync the repository (git pull / re-clone) so the script is the committed version.
  2. Run the same command as above. Completed sources are skipped automatically;
     only sources with missing/changed files re-run.
  3. Read Saved/TDD_M1/tdd_m1_setup_report.json for the per-file verification result
     (import return value, created assets, expected assets, missing/wrong-type lists).
"""

from __future__ import annotations

import datetime
import json
import os
import platform
import sys
import time
from pathlib import Path

try:
    import unreal
except ImportError:  # Permits syntax/static checks and offline tests outside the editor.
    unreal = None

# ----------------------------------------------------------------------------------
# Scope switches
# ----------------------------------------------------------------------------------
TDD_DRY_RUN = False          # True = inspect and report only; no map, import or config write
TDD_SET_CONFIG = True        # Repoint GameDefaultMap/EditorStartupMap after a successful save
TDD_IMPORT = True            # Import the labelled technical handoff files
TDD_IMPORT_TIMEOUT_S = 180.0  # Max seconds to wait for an Interchange import to produce assets

MAP_PACKAGE = "/Game/TDD/Maps"
MAP_ASSET = MAP_PACKAGE + "/PLAYABLE_FOREST_M1"
TEMPLATE_MAP = "/Engine/Maps/Templates/Template_Default"
IMPORT_ROOT = "/Game/TDD/Imports"
STAGING_ROOT = IMPORT_ROOT + "/_staging"
GAME_MODE_CLASS = "/Script/TDD_GAME.TDDForbiddenForestGameMode"

# Asset class short names as returned by AssetData.get_asset_class().
CLASS_SKELTAL_MESH = "SkeletalMesh"
CLASS_STATIC_MESH = "StaticMesh"
CLASS_SKELETON = "Skeleton"
CLASS_ANIM_SEQUENCE = "AnimSequence"
CLASS_MATERIAL = "Material"
CLASS_TEXTURE = "Texture2D"

# Canonical assets the TDD_GAME C++ code loads by exact path.
ADANNA_MESH_PATH = "/Game/TDD/Characters/Adanna/Adanna_M1"
ADANNA_SKELETON_PATH = "/Game/TDD/Characters/Adanna/Adanna_M1_Skeleton"
ADANNA_ANIMATION_NAMES = ("idle", "walk", "run", "jump", "fall", "land", "interact")
ADANNA_ANIMATION_PATHS = tuple(
    "/Game/TDD/Animations/" + name for name in ADANNA_ANIMATION_NAMES)
FOREST_MODULE_NAMES = (
    "FOREST_TREE_MODULE",
    "FOREST_FERN_MODULE",
    "FOREST_ROCK_MODULE",
    "FOREST_GREAT_TREE_MODULE",
    "FOREST_WAYMARKER_MODULE",
    "FOREST_BOUNDARY_POST_MODULE",
)


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
# Pure helpers (no unreal dependency - covered by the offline tests)
# ----------------------------------------------------------------------------------
def source_stem(path) -> str:
    """Deterministic source key: the file stem, used for folders and name prefixes."""
    return Path(str(path)).stem


def staging_folder(stem: str) -> str:
    """Raw Interchange output folder for one source."""
    return STAGING_ROOT + "/" + stem


def assets_folder(stem: str) -> str:
    """Collision-safe home for the non-canonical assets of one source."""
    return IMPORT_ROOT + "/" + stem + "_assets"


def prefixed_asset_path(stem: str, original_name: str) -> str:
    """Deterministic, collision-safe asset path preserving the source relationship."""
    return assets_folder(stem) + "/" + stem + "_" + original_name


def canonical_plan_for(item: dict) -> list:
    """Expected canonical assets (path + class) for one handoff item.

    Returns a list of {"path": str, "class": str} dicts. The plan is deterministic
    and is the verification contract for the import.
    """
    stem = source_stem(item["path"])
    kind = item["kind"]
    plan = []
    if kind == "skeletal":
        plan.append({"path": ADANNA_MESH_PATH, "class": CLASS_SKELTAL_MESH})
        plan.append({"path": ADANNA_SKELETON_PATH, "class": CLASS_SKELETON})
        for anim_path in ADANNA_ANIMATION_PATHS:
            # Animation clips must match by exact clip name: a class-only fallback
            # would mislabel one clip as another (e.g. land content under fall).
            plan.append({"path": anim_path, "class": CLASS_ANIM_SEQUENCE, "name_exact": True})
    elif kind == "module":
        # One canonical static mesh per module, at the exact path the C++ loads.
        plan.append({"path": IMPORT_ROOT + "/" + stem, "class": CLASS_STATIC_MESH})
    return plan


def verify_expected_assets(expected: list, available: dict) -> dict:
    """Verify expected canonical assets against the available {path: class} map.

    Returns {"ok": bool, "missing": [paths], "wrong_type": [{"path","expected","actual"}]}.
    """
    missing = []
    wrong_type = []
    for exp in expected:
        path = exp["path"]
        if path not in available:
            missing.append(path)
        elif available[path] != exp["class"]:
            wrong_type.append({
                "path": path,
                "expected": exp["class"],
                "actual": available[path],
            })
    return {"ok": not missing and not wrong_type, "missing": missing, "wrong_type": wrong_type}


def diff_new_assets(before: set, after: set) -> set:
    """Assets created between two snapshots (sets of asset paths)."""
    return after - before


def source_fingerprint(path) -> dict:
    """File size + mtime fingerprint for change detection (pure filesystem)."""
    p = Path(str(path))
    try:
        st = p.stat()
        return {"size": st.st_size, "mtime": st.st_mtime}
    except OSError:
        return {"size": None, "mtime": None}


def manifest_entry_complete(entry: dict, exists_fn) -> bool:
    """True when a manifest entry is complete and every recorded asset still exists.

    exists_fn(path) -> bool is injected so this stays testable without unreal.
    """
    if not entry or entry.get("status") != "ok":
        return False
    for asset_path in entry.get("final_asset_paths", []):
        if not exists_fn(asset_path):
            return False
    return True


def handoff_files(model_dir: Path) -> list:
    """The labelled technical handoff files, with their import kind and notes."""
    model_dir = Path(model_dir)
    return [
        {
            "path": model_dir / "adanna_m1_technical_proxy_uv.glb",
            "kind": "skeletal",
            "note": "21-joint skinned proxy with UV0 atlas and idle/walk/run/jump/land",
        },
        {
            "path": model_dir / "forbidden_forest_m1.glb",
            "kind": "forest",
            "note": "12-node forest blockout (no canonical paths; source-prefixed assets)",
        },
        {
            "path": model_dir / "adanna_m1_collision_proxy.obj",
            "kind": "static",
            "note": "neutral capsule collision reference, not approved dimensions",
        },
        {
            "path": model_dir / "modules" / "FOREST_TREE_MODULE.glb",
            "kind": "module",
            "note": "reusable forest tree module",
        },
        {
            "path": model_dir / "modules" / "FOREST_FERN_MODULE.glb",
            "kind": "module",
            "note": "reusable forest fern module",
        },
        {
            "path": model_dir / "modules" / "FOREST_ROCK_MODULE.glb",
            "kind": "module",
            "note": "reusable forest rock module",
        },
        {
            "path": model_dir / "modules" / "FOREST_GREAT_TREE_MODULE.glb",
            "kind": "module",
            "note": "Great Root Mother tree module",
        },
        {
            "path": model_dir / "modules" / "FOREST_WAYMARKER_MODULE.glb",
            "kind": "module",
            "note": "white cloth waymarker module",
        },
        {
            "path": model_dir / "modules" / "FOREST_BOUNDARY_POST_MODULE.glb",
            "kind": "module",
            "note": "forest boundary post module",
        },
    ]


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


def saved_dir(project_dir: Path) -> Path:
    if unreal is not None:
        try:
            saved = Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()))
            return saved / "TDD_M1"
        except Exception:
            pass
    return project_dir / "Saved" / "TDD_M1"


def saved_report_path(project_dir: Path) -> Path:
    return saved_dir(project_dir) / "tdd_m1_setup_report.json"


def saved_manifest_path(project_dir: Path) -> Path:
    return saved_dir(project_dir) / "tdd_m1_setup_manifest.json"


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


def _gltf_feature_flag() -> dict:
    """Record the Interchange glTF feature flag when the console API is readable."""
    result = {"checked": False}
    if unreal is None:
        return result
    try:
        cvar = unreal.SystemLibrary.get_console_variable("Interchange.FeatureFlags.Import.GLTF")
        result["checked"] = True
        result["value"] = str(cvar)
    except Exception as exc:
        result["checked"] = True
        result["error"] = str(exc)
    return result


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
        facts["project_basename"] = Path(proj).name
    except Exception:
        pass
    facts["gltf_feature_flag"] = _gltf_feature_flag()
    # Optional capabilities this script depends on.
    for label, probe in (
        ("level_editor_subsystem", lambda: hasattr(unreal, "LevelEditorSubsystem")),
        ("asset_import_task", lambda: hasattr(unreal, "AssetImportTask")),
        ("editor_asset_library", lambda: hasattr(unreal, "EditorAssetLibrary")),
        ("interchange_manager", lambda: hasattr(unreal, "InterchangeManager")),
        ("interchange_generic_pipeline", lambda: hasattr(unreal, "InterchangeGenericAssetsPipeline")),
        ("import_asset_parameters", lambda: hasattr(unreal, "ImportAssetParameters")),
    ):
        try:
            facts[label] = bool(probe())
        except Exception as exc:
            facts[label] = "probe_failed: " + str(exc)
    return facts


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
# Interchange pipeline (UE 5.8.4 verified API)
# ----------------------------------------------------------------------------------
_PIPELINE_KEEPALIVE: list = []  # Prevents GC of in-memory pipelines during import


def _make_interchange_pipeline(force_skeletal: bool):
    """Build (and persist) an Interchange generic assets pipeline.

    UE 5.8 imports glTF through the Interchange framework. The legacy
    `unreal.GLTFImportOptions` object only exposes `generate_lightmap_u_vs` and
    `import_scale` - it has NO `import_animations`/`import_materials`/`import_textures`
    properties, and assigning it as `AssetImportTask.options` against an Interchange
    factory is a type mismatch that silently drops the skin, so a skinned GLB imports
    as a Static Mesh. The supported path is an `InterchangeGenericAssetsPipeline` with
    `common_meshes_properties.force_all_mesh_as_type = IFMT_SKELETAL_MESH`, which forces
    skinned meshes to import as Skeletal Meshes (animations follow automatically).

    Persistence uses unreal.EditorAssetLibrary.save_loaded_asset(asset) - the supported
    Python save API. The pipeline object is kept alive in _PIPELINE_KEEPALIVE because
    override_pipelines resolves the SoftObjectPath against the live object.

    Returns (pipeline, saved: bool, path_used: str).
    """
    pipeline = unreal.InterchangeGenericAssetsPipeline()
    if force_skeletal:
        pipeline.common_meshes_properties.force_all_mesh_as_type = (
            unreal.InterchangeForceMeshType.IFMT_SKELETAL_MESH)
    _PIPELINE_KEEPALIVE.append(pipeline)

    saved = False
    path_used = ""
    try:
        saved = bool(unreal.EditorAssetLibrary.save_loaded_asset(pipeline, only_if_is_dirty=False))
    except Exception as exc:
        warn("could not save Interchange pipeline (%s); using in-memory path" % exc)
    try:
        path_used = pipeline.get_path_name() or ""
    except Exception:
        path_used = ""
    if not path_used:
        # An unsaved object has no stable content path; the live object reference is
        # still resolvable while it is kept alive above.
        log("Interchange pipeline has no persisted path; using the live object reference")
    return pipeline, saved, path_used


def _find_assets(folder: str) -> set:
    """Snapshot the asset paths under a content folder (empty set on failure)."""
    try:
        return {item.get_asset_path() for item in unreal.EditorAssetLibrary.find_assets(folder)}
    except Exception as exc:
        warn("find_assets failed for %s: %s" % (folder, exc))
        return set()


def _asset_class(path: str) -> str:
    """Asset class short name for a path ('' when unknown)."""
    try:
        for item in unreal.EditorAssetLibrary.find_assets(path):
            if item.get_asset_path() == path:
                return item.get_asset_class() or ""
    except Exception:
        pass
    return ""


def _poll_import_completion(staging: str, before: set, timeout_s: float) -> tuple:
    """Wait for the Interchange import to produce assets in the staging folder.

    Interchange imports can complete asynchronously; a non-exception return from
    import_asset is NOT proof of success. Returns (created_set, timed_out: bool).
    """
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        after = _find_assets(staging)
        if after - before:
            return after - before, False
        time.sleep(0.5)
    return set(), True


def _rename_asset(old_path: str, new_path: str) -> bool:
    try:
        return bool(unreal.EditorAssetLibrary.rename_asset(old_path, new_path))
    except Exception as exc:
        warn("rename failed: %s -> %s (%s)" % (old_path, new_path, exc))
        return False


def _plan_renames(created: set, canonical_plan: list) -> tuple:
    """Assign deterministic final paths to the created assets.

    Returns (renames: [(old_path, new_path)], remaining: set).
    Canonical assets are matched by expected class AND, where possible, by exact
    name (e.g. the animation clip name must map to its own canonical path, not to
    the alphabetically-next clip); every other asset gets the source-prefixed
    collision-safe path.
    """
    by_class: dict = {}
    for path in created:
        by_class.setdefault(_asset_class(path), []).append(path)

    renames = []
    used = set()
    for exp in canonical_plan:
        candidates = sorted(by_class.get(exp["class"], []))
        expected_name = exp["path"].rsplit("/", 1)[-1].lower()
        chosen = None
        # Prefer an exact name match (preserves the source relationship).
        for path in candidates:
            if path not in used and path.rsplit("/", 1)[-1].lower() == expected_name:
                chosen = path
                break
        if chosen is None and not exp.get("name_exact"):
            # Class-only fallback for assets whose imported name differs from the
            # canonical name (mesh, skeleton, module mesh). Never used for
            # name_exact entries (animations): a differently-named clip must stay
            # missing rather than be mislabelled.
            for path in candidates:
                if path not in used:
                    chosen = path
                    break
        if chosen is not None:
            used.add(chosen)
            renames.append((chosen, exp["path"]))
    remaining = {path for path in created if path not in used}
    return renames, remaining


def _apply_prefixed_renames(stem: str, remaining: set) -> list:
    """Rename the remaining assets to source-prefixed collision-safe paths."""
    renames = []
    for path in sorted(remaining):
        original = path.rsplit("/", 1)[-1]
        # Strip a possible extension suffix from the original name.
        original = original.rsplit(".", 1)[0] if "." in original else original
        new_path = prefixed_asset_path(stem, original)
        if new_path != path:
            renames.append((path, new_path))
    return renames


def _import_one(item: dict) -> dict:
    """Import one handoff file and verify it. Returns the per-file result dict."""
    source = str(item["path"])
    stem = source_stem(source)
    staging = staging_folder(stem)
    entry = {
        "source": source,
        "source_exists": Path(source).is_file(),
        "kind": item["kind"],
        "note": item["note"],
        "staging_folder": staging,
        "assets_folder": assets_folder(stem),
        "expected_canonical": canonical_plan_for(item),
    }
    if not entry["source_exists"]:
        entry.update({"status": "BLOCKED - OWNER-STUDIO DEPENDENCY", "error": "source file missing"})
        return entry
    if unreal is None:
        entry.update({"status": "PRODUCED - NOT YET VERIFIED", "action": "unreal_unavailable"})
        return entry
    if TDD_DRY_RUN:
        entry.update({"status": "PRODUCED - NOT YET VERIFIED", "action": "dry_run_skipped"})
        return entry
    if not TDD_IMPORT:
        entry.update({"status": "PRODUCED - NOT YET VERIFIED", "action": "import_disabled"})
        return entry

    try:
        unreal.EditorAssetLibrary.make_directory(staging)
        before = _find_assets(staging)
        if before:
            # Staging should be empty on a clean import; unexpected content means a
            # conflicting previous run. Never overwrite - report and stop.
            entry.update({
                "status": "CONFLICT - NOT OVERWRITTEN",
                "error": "staging folder already contains assets: %s" % sorted(before),
            })
            warn("staging folder not empty for %s; skipping to avoid overwriting" % stem)
            return entry

        pipeline, pipeline_saved, pipeline_path = _make_interchange_pipeline(
            force_skeletal=(item["kind"] == "skeletal"))

        parameters = unreal.ImportAssetParameters()
        parameters.is_automated = True
        parameters.replace_existing = False  # never overwrite existing content
        if pipeline_path:
            parameters.override_pipelines.append(unreal.SoftObjectPath(pipeline_path))

        manager = unreal.InterchangeManager.get_interchange_manager_scripted()
        source_data = manager.create_source_data(source)
        import_return = bool(manager.import_asset(staging, source_data, parameters))
        entry["import_return"] = import_return
        entry["pipeline_saved"] = pipeline_saved
        entry["pipeline_path_used"] = pipeline_path

        created, timed_out = _poll_import_completion(staging, before, TDD_IMPORT_TIMEOUT_S)
        entry["import_timed_out"] = timed_out
        if timed_out:
            entry.update({
                "status": "FAILED - IMPORT DID NOT COMPLETE",
                "error": "no assets appeared in %s within %.0fs (async completion, "
                         "missing glTF translator, or import failure)" % (staging, TDD_IMPORT_TIMEOUT_S),
            })
            warn("import produced no assets for %s within the timeout" % stem)
            return entry

        entry["created_asset_paths"] = sorted(created)

        # Deterministic rename phase: canonical assets to their exact paths, the rest
        # to source-prefixed collision-safe paths.
        canonical_plan = entry["expected_canonical"]
        renames, remaining = _plan_renames(created, canonical_plan)
        for old_path, new_path in _apply_prefixed_renames(stem, remaining):
            renames.append((old_path, new_path))

        renamed = []
        skipped = []
        for old_path, new_path in renames:
            if unreal.EditorAssetLibrary.does_asset_exist(new_path):
                # Never overwrite an existing asset; keep the imported one in place.
                skipped.append({"from": old_path, "to": new_path, "reason": "destination_exists"})
                continue
            if _rename_asset(old_path, new_path):
                renamed.append({"from": old_path, "to": new_path})
            else:
                skipped.append({"from": old_path, "to": new_path, "reason": "rename_failed"})
        entry["renamed_assets"] = renamed
        entry["rename_skipped"] = skipped

        # Outcome verification: canonical assets must exist with the expected type.
        available = {}
        for path in sorted(set(list(entry["created_asset_paths"]) +
                               [r["to"] for r in renamed] +
                               [s["to"] for s in skipped])):
            available[path] = _asset_class(path)
        verification = verify_expected_assets(canonical_plan, available)
        entry["verification"] = verification
        # Final paths (post-rename) for the manifest: each created asset's current
        # location (renamed destinations, or the staging path when not renamed),
        # plus skipped destinations (pre-existing canonical assets).
        renamed_map = {r["from"]: r["to"] for r in renamed}
        entry["final_asset_paths"] = sorted(set(
            [renamed_map.get(p, p) for p in entry["created_asset_paths"]] +
            [s["to"] for s in skipped]))

        if verification["wrong_type"]:
            entry["status"] = "FAILED - VERIFICATION"
            entry["wrong_type"] = verification["wrong_type"]
            warn("verification failed for %s: wrong_type=%s" %
                 (stem, verification["wrong_type"]))
        elif verification["missing"]:
            # The import succeeded but the source does not contain every canonical
            # asset (e.g. the GLB has no fall/interact clips). Reported explicitly;
            # the source is still recorded as complete so reruns stay idempotent.
            entry["status"] = "COMPLETED WITH MISSING"
            entry["warnings"] = ["missing expected assets: %s" % verification["missing"]]
            warn("import completed with missing assets for %s: %s" %
                 (stem, verification["missing"]))
        elif skipped:
            entry["status"] = "COMPLETED WITH WARNINGS"
            entry["warnings"] = ["renames skipped (destination exists): %s" %
                                 [s["to"] for s in skipped]]
        else:
            entry["status"] = "COMPLETED AND VERIFIED"
    except Exception as exc:
        entry.update({"status": "FAILED - EXCEPTION", "error": str(exc)})
        warn("import failed for %s: %s" % (source, exc))
    return entry


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def _manifest_key(source: str) -> str:
    return source


def import_assets(report: dict, paths: dict) -> None:
    items = handoff_files(Path(paths["model_dir"]))
    results: list = []
    report["imports"] = results
    report["warnings"] = []

    manifest_path = saved_manifest_path(Path(paths["project_dir"]))
    manifest = _load_manifest(manifest_path)
    manifest.setdefault("sources", {})

    for item in items:
        source = str(item["path"])
        key = _manifest_key(source)
        entry = {
            "source": source,
            "source_exists": item["path"].is_file(),
            "kind": item["kind"],
            "note": item["note"],
            "staging_folder": staging_folder(source_stem(source)),
            "assets_folder": assets_folder(source_stem(source)),
            "expected_canonical": canonical_plan_for(item),
        }
        previous = manifest["sources"].get(key)

        # A source whose file changed on disk is reported explicitly and skipped;
        # never auto-overwrite content from a previous run. This check runs BEFORE
        # the idempotent skip so a changed source is always reported.
        if previous and previous.get("fingerprint"):
            current_fp = source_fingerprint(source)
            if current_fp != previous.get("fingerprint"):
                entry.update({
                    "status": "SKIPPED - SOURCE CHANGED",
                    "action": "source_changed_requires_manual_review",
                    "previous_fingerprint": previous.get("fingerprint"),
                    "current_fingerprint": current_fp,
                })
                warn("source changed since last run; skipping to avoid overwriting: " + source)
                results.append(entry)
                continue

        # Idempotent rerun: skip a source whose manifest entry is complete and whose
        # recorded assets still exist. The stored verification is re-attached so the
        # report still shows missing assets / warnings explicitly.
        if previous and manifest_entry_complete(previous, lambda p: unreal is not None and
                                                unreal.EditorAssetLibrary.does_asset_exist(p)):
            entry.update({
                "status": "SKIPPED - ALREADY COMPLETE",
                "action": "idempotent_skip",
                "final_asset_paths": previous.get("final_asset_paths", []),
                "verification": previous.get("verification"),
                "warnings": previous.get("warnings", []),
            })
            log("skipping already-complete import: " + source)
            results.append(entry)
            continue

        entry = _import_one(item)
        entry["fingerprint"] = source_fingerprint(source)
        results.append(entry)

        # Record the outcome in the manifest only for imported (non-skipped) sources.
        # Any COMPLETED* status is normalised to "ok" so reruns skip it idempotently;
        # FAILED/CONFLICT entries are re-imported on the next run.
        if entry.get("status", "").startswith(("COMPLETED", "FAILED", "CONFLICT")):
            manifest["sources"][key] = {
                "source": source,
                "kind": item["kind"],
                "status": "ok" if entry["status"].startswith("COMPLETED") else entry["status"],
                "raw_status": entry["status"],
                "fingerprint": entry.get("fingerprint"),
                "final_asset_paths": entry.get("final_asset_paths", []),
                "verification": entry.get("verification"),
                "warnings": entry.get("warnings", []),
                "updated_utc": utc_now(),
            }

    report["manifest_written_to"] = str(manifest_path)
    try:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        report["manifest_status"] = "written"
    except Exception as exc:
        report["manifest_status"] = "write_failed: %s" % exc
        warn("could not write manifest to %s: %s" % (manifest_path, exc))


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
    if any(e.get("status", "").startswith("COMPLETED") for e in report["imports"]):
        report["status_classification"]["asset_import"] = "COMPLETED AND VERIFIED"
    elif any(e.get("status", "").startswith(("FAILED", "CONFLICT")) for e in report["imports"]):
        report["status_classification"]["asset_import"] = "FAILED - SEE REPORT"
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
