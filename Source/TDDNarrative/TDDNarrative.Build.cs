// Copyright (c) 2026. The Disobedient Daughter.
// TDDNarrative module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Quests, memories, endings, cinematics. Depends on TDDCore + TDDWorld only.

using UnrealBuildTool;

public class TDDNarrative : ModuleRules
{
	public TDDNarrative(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "TDDCore", "TDDWorld" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
