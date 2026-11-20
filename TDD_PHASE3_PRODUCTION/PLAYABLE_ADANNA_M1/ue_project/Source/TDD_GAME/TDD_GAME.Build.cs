using UnrealBuildTool;

public class TDD_GAME : ModuleRules
{
    public TDD_GAME(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "InputCore"
        });
        PrivateDependencyModuleNames.AddRange(new string[] { });
    }
}
