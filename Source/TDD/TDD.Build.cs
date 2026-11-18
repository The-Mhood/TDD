// Copyright (c) 2026. The Disobedient Daughter.
// TDD — primary game module. Loads the runtime graph declared in TDD.uproject.

using UnrealBuildTool;

public class TDD : ModuleRules
{
	public TDD(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core", "CoreUObject", "Engine",
			"TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI"
		});
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
