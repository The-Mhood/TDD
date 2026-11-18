// Copyright (c) 2026. The Disobedient Daughter.
// TDDTests module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Editor-only functional/integration tests. Unit tests live inside each module behind WITH_DEV_AUTOMATION_TESTS.

using UnrealBuildTool;

public class TDDTests : ModuleRules
{
	public TDDTests(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "TDDCore", "TDDWorld", "TDDGameplay", "TDDAI", "TDDNarrative", "TDDUI" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
