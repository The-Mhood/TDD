// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

using UnrealBuildTool;

/**
 * Editor-only module: canon validators, asset linters, bulk authoring tools.
 *
 * STATUS: SPEC (Stage 1). Nothing here may be referenced by TDDRuntime.
 */
public class TDDEditor : ModuleRules
{
    public TDDEditor(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "UnrealEd",
            "TDDRuntime",
            "GameplayTags",
            "DataValidation"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Slate",
            "SlateCore",
            "ToolMenus",
            "AssetRegistry",
            "Json",
            "JsonUtilities"
        });
    }
}
