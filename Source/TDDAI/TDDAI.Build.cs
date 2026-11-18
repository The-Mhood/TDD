// Copyright (c) 2026. The Disobedient Daughter.
// TDDAI module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Enemies, bosses, encounters, NPC. May depend on TDDGameplay; no private-internal access.

using UnrealBuildTool;

public class TDDAI : ModuleRules
{
	public TDDAI(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "AIModule", "TDDCore", "TDDWorld", "TDDGameplay" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
