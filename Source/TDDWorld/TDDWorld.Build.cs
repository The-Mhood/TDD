// Copyright (c) 2026. The Disobedient Daughter.
// TDDWorld module. Dependency direction is the MEAD §3.2 rule: depends only downward.
// Chapters, streaming, world state, time/weather data layers, checkpoints.

using UnrealBuildTool;

public class TDDWorld : ModuleRules
{
	public TDDWorld(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "TDDCore" });
		PrivateDependencyModuleNames.AddRange(new string[] { });
	}
}
