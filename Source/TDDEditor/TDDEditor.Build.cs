// Copyright (c) 2026. The Disobedient Daughter.
// TDDEditor module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Editor-only: validators, commandlets, data audits, cook guards. Nothing may depend on this.

using UnrealBuildTool;

public class TDDEditor : ModuleRules
{
	public TDDEditor(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "UnrealEd", "TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
