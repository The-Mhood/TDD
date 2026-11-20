"""Create a first, editable Great Root Mother phase graph in UE content.

Run after the project module has compiled and the Editor is open. This creates
new data only; it does not overwrite an existing asset or implement boss-
specific C++ behavior.
"""
import json
from pathlib import Path
import unreal

DEST = "/Game/Bosses/GreatRootMother/DA_GreatRootMother_Phases"


def phase(name, transitions=None, music="", camera="", abilities=None, arena=None, invulnerable=False):
    value = unreal.FTDDBossPhaseData()
    value.set_editor_property("phase_name", unreal.Name(name))
    value.set_editor_property("transitions", transitions or [])
    value.set_editor_property("music_state", unreal.Name(music) if music else unreal.Name())
    value.set_editor_property("camera_profile", unreal.Name(camera) if camera else unreal.Name())
    value.set_editor_property("ability_set", [unreal.Name(x) for x in (abilities or [])])
    value.set_editor_property("arena_states", [unreal.Name(x) for x in (arena or [])])
    value.set_editor_property("b_invulnerable", invulnerable)
    return value


def transition(kind, threshold, target, event=""):
    value = unreal.FTDDBossPhaseTransitionData()
    value.set_editor_property("kind", kind)
    value.set_editor_property("threshold", threshold)
    value.set_editor_property("target_phase", unreal.Name(target))
    if event:
        value.set_editor_property("event_name", unreal.Name(event))
    return value


def main():
    if unreal.EditorAssetLibrary.does_asset_exist(DEST):
        raise RuntimeError("Refusing to overwrite existing asset: " + DEST)
    asset_class = unreal.load_class(None, "/Script/TheDisobedientDaughter.TDDBossPhaseGraphAsset")
    require(asset_class is not None, "Compile TheDisobedientDaughter module before running this script")
    factory = unreal.DataAssetFactory()
    factory.set_editor_property("data_asset_class", asset_class)
    asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        "DA_GreatRootMother_Phases", "/Game/Bosses/GreatRootMother", asset_class, factory)
    require(asset is not None, "Failed to create boss phase data asset")

    health_kind = unreal.ETDDBossTransition.HEALTH_PCT
    poise_kind = unreal.ETDDBossTransition.POISE_BREAK
    elapsed_kind = unreal.ETDDBossTransition.ELAPSED_SEC
    root = phase("Roots", [transition(health_kind, 0.55, "Bloom"),
                            transition(elapsed_kind, 100.0, "Bloom")],
                 music="Music.Boss.Ch01.Phase1", camera="Boss.RootMother.Wide",
                 abilities=["Ability.RootSweep"], arena=["Arena.RootsClosed"])
    bloom = phase("Bloom", [transition(poise_kind, 0.0, "Rage")],
                  music="Music.Boss.Ch01.Phase2", camera="Boss.RootMother.Close",
                  abilities=["Ability.RootGrab"], arena=["Arena.RootsOpen"])
    rage = phase("Rage", [transition(health_kind, 0.0, "Defeat")],
                 music="Music.Boss.Ch01.Rage", abilities=["Ability.RootSlam"])
    defeat = phase("Defeat")
    asset.set_editor_property("phases", [root, bloom, rage, defeat])
    asset.set_editor_property("entry_phase", unreal.Name("Roots"))
    asset.set_editor_property("defeat_phase", unreal.Name("Defeat"))
    asset.set_editor_property("terminal_phases", [unreal.Name("Defeat")])
    unreal.EditorAssetLibrary.save_loaded_asset(asset)

    out = Path(unreal.Paths.project_dir()) / "Saved/BuildEvidence/W1D2/root-mother-asset-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "asset": DEST,
        "status": "CREATED_IN_EDITOR",
        "phase_names": ["Roots", "Bloom", "Rage", "Defeat"],
        "transition_order": "first satisfied wins",
        "asset_class": "UTDDBossPhaseGraphAsset",
        "runtime_graph_validation": "run TDD.W1D2.AI.BossPhaseAssetAdapter in UE automation",
        "boss_specific_code_added": False,
    }, indent=2) + "\n", encoding="utf-8")
    unreal.log("Created data-only boss graph asset " + DEST)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


main()
