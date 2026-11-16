// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

using UnrealBuildTool;

/**
 * Automation tests (ADR-0001: Unreal Automation framework only).
 *
 * STATUS: SPEC (Stage 1).
 * Naming convention: TDD.<Area>.<Behaviour>
 *   e.g. TDD.Memory.Director.SecondGrantRejected
 */
public class TDDTests : ModuleRules
{
    public TDDTests(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "TDDRuntime",
            "GameplayTags",
            "GameplayAbilities",
            "AIModule",
            "StateTreeModule"
        });

        // Automation tests are editor-run only.
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UnrealEd",
            "Json",
            "JsonUtilities"
        });
    }
}
