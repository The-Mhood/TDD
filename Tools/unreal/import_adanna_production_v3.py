"""Import and wire the qualified Adanna AD-03 V3 production FBX in Unreal Editor.

This is the production handoff for the sculpt-milestone-1 qualified asset
(Design gate CLOSED at 2a4a88e). It imports the V3 FBX as a Skeletal Mesh,
creates a player Blueprint wired to TDDAdannaCharacter, and assigns the
technical GameMode Blueprint to the greybox map.

The technical-proxy import script (import_adanna_proxy.py) is retained
unchanged as the rollback path; this script is the production target.

Requires: UE glTF/FBX import support, a compiled project module, and the
HUMAN_BASE_PROPOSED skeleton. It never overwrites existing assets.
"""
import hashlib
import json
from pathlib import Path
import unreal

REPO = Path(unreal.Paths.project_dir())
SOURCE = REPO / ".arena/production/2026-11-24_w1d7_blender_package/output/ADANNA_AD03_V3/ADANNA_AD03_V3.fbx"
# SHA-256 of the qualified V3 FBX (verified in sandbox, 2026-11-20).
EXPECTED_SHA256 = "40f1c83de4c8bf683787b315aa8bd8ab53fadfc4bd3a1dcf23fe55d8ad631d91"
DESTINATION = "/Game/Characters/Adanna/ProductionV3"
PLAYER_BP = DESTINATION + "/BP_Adanna_ProductionV3"
GAMEMODE_BP = DESTINATION + "/BP_TDDGameMode_ProductionV3"
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
    actual_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    require(actual_hash == EXPECTED_SHA256,
            "Adanna V3 FBX SHA-256 does not match the qualified deliverable")

    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(SOURCE))
    task.set_editor_property("destination_path", DESTINATION)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", False)
    task.set_editor_property("save", True)
    # FBX is metres->cm; import at scale 1.0 (UE interprets FBX units as cm).
    task.set_editor_property("scale", 1.0)
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
        player_bp = make_child_blueprint(asset_tools, "BP_Adanna_ProductionV3", DESTINATION, player_class)
        unreal.KismetEditorUtilities.compile_blueprint(player_bp)
        player_defaults = unreal.get_default_object(player_bp.generated_class)
        player_defaults.set_editor_property("character_mesh_asset", skeletal_meshes[0])
        unreal.KismetEditorUtilities.compile_blueprint(player_bp)
        unreal.EditorAssetLibrary.save_loaded_asset(player_bp)
        player_blueprint_path = player_bp.get_path_name()

        gm_bp = make_child_blueprint(asset_tools, "BP_TDDGameMode_ProductionV3", DESTINATION, game_mode_class)
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
        "source_sha256_verified": actual_hash == EXPECTED_SHA256,
        "source_sha256": actual_hash,
        "expected_sha256": EXPECTED_SHA256,
        "destination": DESTINATION,
        "asset_paths": [asset.get_path_name() for asset in imported],
        "asset_classes": classes,
        "skeletal_mesh_count": len(skeletal_meshes),
        "skeleton_count": len(skeletons),
        "animation_sequence_count": len(animations),
        "player_blueprint": player_blueprint_path,
        "game_mode_blueprint": game_mode_blueprint_path,
        "greybox_map_game_mode_assigned": map_game_mode_assigned,
        "classification": "production; sculpt-milestone-1 qualified (2a4a88e)",
        "texture_note": "FBX carries materials/slots; textures are packed in the .blend — supply separately for UE.",
        "pie_compile_cook_package_verified": False,
        "next_step": "Run TDD automation, open Ch01_Greybox in PIE, record movement/camera/combat, then update verification status.",
    }
    out = REPO / "Saved/BuildEvidence/W1D8/adanna-v3-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log("TDD W1D8 Adanna V3 import report: " + json.dumps(report))
    if not skeletal_meshes:
        unreal.log_error("No SkeletalMesh imported. Check FBX importer options; do not treat this as integration success.")


try:
    main()
except Exception as exc:
    out = REPO / "Saved/BuildEvidence/W1D8/adanna-v3-import-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "status": "FAILED",
        "error": str(exc),
        "classification": "production; sculpt-milestone-1 qualified (2a4a88e)",
        "pie_compile_cook_package_verified": False,
    }, indent=2) + "\n", encoding="utf-8")
    unreal.log_error("TDD W1D8 Adanna V3 import failed: " + str(exc))
    raise
