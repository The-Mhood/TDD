// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

using UnrealBuildTool;

/**
 * Primary game module.
 *
 * STATUS: SPEC — authored 2026-11-16, not compiled (no engine in the authoring
 * environment; see Docs/adr/ADR-0005-engine-verification.md).
 *
 * DEPENDENCY POLICY (architecture doc section 4.1 / ADR-0001, ADR-0003):
 *   - Add a dependency only when a system in this module genuinely needs it.
 *   - Every new dependency requires a note in the PR explaining which feature
 *     needs it and why an existing module does not suffice.
 *   - Do not add editor-only modules here; that is TDDEditor's job.
 */
public class TDDRuntime : ModuleRules
{
    public TDDRuntime(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        // Public: types that TDDEditor and TDDTests must see.
        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "EnhancedInput",          // Stage 2: input abstraction
            "GameplayTags",           // Cross-agent vocabulary (architecture doc 6.6)
            "GameplayTasks",          // Required by GameplayAbilitySystem
            "GameplayAbilities",      // Stage 3: combat abilities only (ADR-0003)
            "AIModule",               // Stage 5: perception and navigation
            "NavigationSystem",
            "StateTreeModule",        // Stage 5: enemy and NPC behaviour
            "GameplayStateTreeModule",
            "Niagara",
            "UMG",
            "CommonUI",               // Stage 7: view-model driven UI
            "Slate",
            "SlateCore",
            "MediaAssets",            // Stage 7: cinematic playback paths
            "LevelSequence",          // Stage 7: memory playback
            "MovieScene",
            "AudioMixer",
            "MetasoundEngine"
        });

        // Private: implementation-only. Kept small on purpose.
        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "RenderCore",
            "RHI"
        });

        // Server-only code is not part of this project (single-player). If a
        // dedicated server target is ever added, gate it here explicitly rather
        // than adding unconditional defines.
    }
}
