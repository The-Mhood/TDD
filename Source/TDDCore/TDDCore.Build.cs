// Copyright (c) 2026. The Disobedient Daughter.
// TDDCore module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Leaf module: types, interfaces, events, save contracts, canon refs, logging, RNG, math.

using UnrealBuildTool;

public class TDDCore : ModuleRules
{
	public TDDCore(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
