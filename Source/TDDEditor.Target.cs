// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

using UnrealBuildTool;
using System.Collections.Generic;

public class TDDEditorTarget : TargetRules
{
    public TDDEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6;
        ExtraModuleNames.AddRange(new string[] { "TDDRuntime", "TDDEditor", "TDDTests" });
    }
}
