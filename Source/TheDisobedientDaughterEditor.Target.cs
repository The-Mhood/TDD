using UnrealBuildTool;
using System.Collections.Generic;

public class TheDisobedientDaughterEditorTarget : TargetRules
{
    public TheDisobedientDaughterEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        ExtraModuleNames.Add("TheDisobedientDaughter");
    }
}
