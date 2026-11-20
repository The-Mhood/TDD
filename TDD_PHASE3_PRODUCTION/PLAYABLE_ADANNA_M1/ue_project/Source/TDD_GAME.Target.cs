using UnrealBuildTool;

public class TDD_GAMETarget : TargetRules
{
    public TDD_GAMETarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("TDD_GAME");
    }
}
