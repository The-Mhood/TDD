// Copyright (c) 2026. The Disobedient Daughter.
// TDDGameplay module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Pawns, camera, combat, input, interaction. Must not include TDDAI/TDDNarrative/TDDUI headers.

using UnrealBuildTool;

public class TDDGameplay : ModuleRules
{
	public TDDGameplay(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput", "TDDCore", "TDDWorld" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
