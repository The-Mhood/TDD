"""Import and wire the existing Adanna technical GLB in Unreal Editor.

Requires UE glTF import support and a compiled project module. It creates
separately labelled technical Blueprint assets; it never replaces an existing
production character/map or upgrades the proxy's approval status.
"""
import hashlib
import json
from pathlib import Path
import unreal

REPO = Path(unreal.Paths.project_dir())
SOURCE = REPO / "TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/model/adanna_m1_technical_proxy.glb"
MANIFEST = REPO / "TDD_PHASE3_PRODUCTION/PLAYABLE_ADANNA_M1/model/adanna_m1_ue_import_manifest.json"
DESTINATION = "/Game/Characters/Adanna/TechnicalProxy"
PLAYER_BP = DESTINATION + "/BP_Adanna_TechnicalProxy"
GAMEMODE_BP = DESTINATION + "/BP_TDDGameMode_TechnicalProxy"
GREYBOX_MAP = "/Game/Maps/Ch01_Greybox"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def make_child_blueprint(asset_tools, name, package_path, parent_class):
    if unreal.EditorAssetLibrary.does_asset_exist(package_path):
        raise RuntimeError("Refusing to overwrite existing Blueprint: " + package_path)
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    blueprint = asset_tools.create_asset(name, str(Path(package_path).parent), unreal.Blueprint, factory)
    require(blueprint is not None, "Could not create Blueprint " + package_path)
    return blueprint


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected_hash = manifest.get("sha256", {}).get("preserved_source_glb")
    actual_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    require(expected_hash == actual_hash, "Source GLB SHA-256 does not match approved handoff manifest")

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(SOURCE))
    task.set_editor_property("destination_path", DESTINATION)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", False)
    task.set_editor_property("save", True)
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])

    imported = [unreal.EditorAssetLibrary.load_asset(path)
                for path in task.get_editor_property("imported_object_paths")]
    imported = [asset for asset in imported if asset is not None]
    classes = sorted(set(asset.get_class().get_name() for asset in imported))
    skeletal_meshes = [asset for asset in imported if asset.get_class().get_name() == "SkeletalMesh"]
    skeletons = [asset for asset in imported if asset.get_class().get_name() == "Skeleton"]
    animations = [asset for asset in imported if asset.get_class().get_name() == "AnimSequence"]
    player_blueprint_path = None
    game_mode_blueprint_path = None
    map_game_mode_assigned = False

    if skeletal_meshes:
        player_class = unreal.load_class(None, "/Script/TheDisobedientDaughter.TDDAdannaCharacter")
        game_mode_class = unreal.load_class(None, "/Script/TheDisobedientDaughter.TDDGameMode")
        require(player_class and game_mode_class, "Build project C++ classes before creating playable children")
        player_bp = make_child_blueprint(asset_tools, "BP_Adanna_TechnicalProxy", DESTINATION, player_class)
        unreal.KismetEditorUtilities.compile_blueprint(player_bp)
        player_defaults = unreal.get_default_object(player_bp.generated_class)
        player_defaults.set_editor_property("character_mesh_asset", skeletal_meshes[0])
        unreal.KismetEditorUtilities.compile_blueprint(player_bp)
        unreal.EditorAssetLibrary.save_loaded_asset(player_bp)
        player_blueprint_path = player_bp.get_path_name()

        gm_bp = make_child_blueprint(asset_tools, "BP_TDDGameMode_TechnicalProxy", DESTINATION, game_mode_class)
        gm_defaults = unreal.get_default_object(gm_bp.generated_class)
        gm_defaults.set_editor_property("default_pawn_class", player_bp.generated_class)
        unreal.KismetEditorUtilities.compile_blueprint(gm_bp)
        unreal.EditorAssetLibrary.save_loaded_asset(gm_bp)
        game_mode_blueprint_path = gm_bp.get_path_name()

        if unreal.EditorAssetLibrary.does_asset_exist(GREYBOX_MAP):
            if unreal.EditorLevelLibrary.load_level(GREYBOX_MAP):
                world = unreal.EditorLevelLibrary.get_editor_world()
                world.get_world_settings().set_editor_property("default_game_mode", gm_bp.generated_class)
                map_game_mode_assigned = unreal.EditorLevelLibrary.save_current_level()

    report = {
        "status": "IMPORTED_AND_PLAYER_BLUEPRINT_WIRED" if player_blueprint_path else
                  ("IMPORTED_NEEDS_SKELETAL_IMPORT_SUPPORT" if imported else "IMPORT_FAILED_OR_UNSUPPORTED"),
        "source": str(SOURCE.relative_to(REPO)),
        "source_sha256_verified": actual_hash == expected_hash,
        "destination": DESTINATION,
        "asset_paths": [asset.get_path_name() for asset in imported],
        "asset_classes": classes,
        "skeletal_mesh_count": len(skeletal_meshes),
        "skeleton_count": len(skeletons),
        "animation_sequence_count": len(animations),
        "player_blueprint": player_blueprint_path,
        "game_mode_blueprint": game_mode_blueprint_path,
        "greybox_map_game_mode_assigned": map_game_mode_assigned,
        "proxy_classification": "technical proxy; provisional; not creative-approved",
        "anim_blueprint_or_retarget_verified": False,
        "pie_compile_cook_package_verified": False,
        "next_step": "Run TDD automation, open Ch01_Greybox in PIE, record movement/camera/combat, and only then update verification status.",
    }
    out = REPO / "Saved/BuildEvidence/W1D2/adanna-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W1D2 Adanna import report: " + json.dumps(report))
    if not skeletal_meshes:
        unreal.log_error("No SkeletalMesh was imported. Check glTF importer plugin/options; do not treat this as integration success.")


try:
    main()
except Exception as exc:
    out = REPO / "Saved/BuildEvidence/W1D2/adanna-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "status": "FAILED",
        "error": str(exc),
        "proxy_classification": "technical proxy; provisional; not creative-approved",
        "pie_compile_cook_package_verified": False,
    }, indent=2) + "\n", encoding="utf-8")
    unreal.log_error("TDD W1D2 Adanna import failed: " + str(exc))
    raise
