using UnrealBuildTool;

public class TDD_GAMETarget : TargetRules
{
    public TDD_GAMETarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;

        // DefaultBuildSettings is part of the SHARED build environment: this target
        // reuses the launcher engine's precompiled UnrealEditor modules, so these
        // values must match the engine's or UBT refuses the build with
        // "... modifies the values of properties ... has build products in common
        // with UnrealEditor". V7 is the 5.8 default: V6/V7 raise
        // UndefinedIdentifier/UnreachableCode/ReturnType/DanglingWarningLevel to
        // Error, and a lower version leaves them Off.
        DefaultBuildSettings = BuildSettingsVersion.V7;

        // Include order is per-module and is NOT part of the shared environment.
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;

        ExtraModuleNames.Add("TDD_GAME");
    }
}
