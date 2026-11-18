using UnrealBuildTool;
using System.Collections.Generic;

public class TheDisobedientDaughterTarget : TargetRules
{
    public TheDisobedientDaughterTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        ExtraModuleNames.Add("TheDisobedientDaughter");
    }
}
