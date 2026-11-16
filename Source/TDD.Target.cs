// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class TDDTarget : TargetRules
{
    public TDDTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6;
        ExtraModuleNames.AddRange(new string[] { "TDDRuntime" });
    }
}
