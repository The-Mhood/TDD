// Copyright (c) 2026. The Disobedient Daughter.
// TDDUI module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// HUD, menus, prompts, journal, settings.

using UnrealBuildTool;

public class TDDUI : ModuleRules
{
	public TDDUI(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "UMG", "Slate", "SlateCore", "TDDCore", "TDDWorld" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
