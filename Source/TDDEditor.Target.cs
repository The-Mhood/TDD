// Copyright (c) 2026. The Disobedient Daughter.
// Editor target. TDDEditor and TDDTests are Editor-type modules (MEAD §2.5, §3.2).

using UnrealBuildTool;
using System.Collections.Generic;

public class TDDEditorTarget : TargetRules
{
	public TDDEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.AddRange(new string[] { "TDD", "TDDEditor", "TDDTests" });
	}
}
