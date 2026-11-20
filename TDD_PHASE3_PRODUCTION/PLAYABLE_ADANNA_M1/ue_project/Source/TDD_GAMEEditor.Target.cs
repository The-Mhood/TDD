using UnrealBuildTool;
using System.Collections.Generic;

public class TDD_GAMEEditorTarget : TargetRules
{
    public TDD_GAMEEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_4;
        ExtraModuleNames.Add("TDD_GAME");
    }
}
