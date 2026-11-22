using UnrealBuildTool;

public class TDD_GAMEEditorTarget : TargetRules
{
    public TDD_GAMEEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;

        // Must stay identical to TDD_GAME.Target.cs. The editor target shares
        // build products with the engine's precompiled UnrealEditor modules, so a
        // divergent BuildSettingsVersion is rejected outright by UBT. This file
        // previously carried V5 / Unreal5_4 and stopped the first compile.
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;

        ExtraModuleNames.Add("TDD_GAME");
    }
}
