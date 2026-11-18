// Copyright (c) 2026. The Disobedient Daughter.
// Game target. Engine pin: UE 5.8 (ADR-0001). Build settings deliberately use the
// engine's own "Latest" values rather than a hard-coded enum, so the target stays valid
// across the pinned 5.8 patch stream.

using UnrealBuildTool;
using System.Collections.Generic;

public class TDDTarget : TargetRules
{
	public TDDTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.AddRange(new string[] { "TDD" });
	}
}
