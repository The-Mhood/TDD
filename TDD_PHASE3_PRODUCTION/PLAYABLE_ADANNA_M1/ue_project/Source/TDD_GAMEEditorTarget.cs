using UnrealBuildTool;

public class TDD_GAMEEditorTarget : TargetRules
{
    public TDD_GAMEEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("TDD_GAME");
    }
}
