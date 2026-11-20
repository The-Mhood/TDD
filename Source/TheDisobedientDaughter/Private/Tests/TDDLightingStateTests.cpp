#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Engine/World.h"
#include "Lighting/TDDLightingStateSwitcher.h"

/**
 * CH01 provisional lighting states: the switcher owns sun/ambient/firelight
 * and applies each state's preset atomically (W1 D13 keys ST01/ST03/ST04).
 *
 * Test seam: a real switcher actor spawned in a created Game world. All
 * assertions observe the public component interface; no class-default
 * mutation, no const-cast and no private preset access. The golden values
 * below mirror the preset contract declared in FTDDLightingPreset.
 *
 * UE 5.8.4 API notes (verified against the 5.8.4 docs/engine source):
 *  - ULightComponent::LightColor is FColor (no Equals(Tolerance)); the
 *    engine's own read path is FLinearColor(LightColor), which round-trips
 *    the stored sRGB bytes to linear. Comparisons use that conversion with
 *    a tolerance covering 8-bit quantization (~1/255).
 *  - USkyLightComponent has LowerHemisphereColor (FLinearColor) for the
 *    ground; the sky/upper colour is the inherited LightColor. There is no
 *    upper-hemisphere colour member exists in 5.8.4.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1LightingStateSwitcherTest,
    "TDD.M1.Lighting.StateSwitcher",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

namespace
{
// Quantization-tolerant colour comparison: FColor stores 8-bit sRGB bytes,
// so a round-trip through FLinearColor(LightColor) is exact to ~1/255.
const float ColorTolerance = 0.01f;

struct FPresetGoldenValues
{
    float SunIntensity;
    FLinearColor SunColor;
    float SunElevationDeg;
    float SunAzimuthDeg;
    FLinearColor AmbientSky;
    FLinearColor AmbientGround;
    float FireIntensity;
};

// Golden contract mirrored from the switcher's preset defaults.
const FPresetGoldenValues DawnGolden =
{
    2.0f, FLinearColor(1.0f, 0.82f, 0.62f), 12.0f, 70.0f,
    FLinearColor(0.45f, 0.50f, 0.60f), FLinearColor(0.22f, 0.18f, 0.14f), 0.0f
};
const FPresetGoldenValues DuskGolden =
{
    1.6f, FLinearColor(1.0f, 0.55f, 0.28f), 6.0f, 285.0f,
    FLinearColor(0.40f, 0.32f, 0.42f), FLinearColor(0.20f, 0.14f, 0.12f), 0.0f
};
const FPresetGoldenValues NightGolden =
{
    0.35f, FLinearColor(0.55f, 0.62f, 0.80f), -24.0f, 200.0f,
    FLinearColor(0.06f, 0.08f, 0.14f), FLinearColor(0.04f, 0.04f, 0.05f), 8.0f
};

bool VerifyPresetApplied(ATDDLightingStateSwitcher* Switcher, const FPresetGoldenValues& Golden)
{
    UDirectionalLightComponent* Sun = Switcher->GetSunLight();
    USkyLightComponent* Ambient = Switcher->GetAmbientLight();
    UPointLightComponent* Fire = Switcher->GetFireLight();
    if (Sun == nullptr || Ambient == nullptr || Fire == nullptr)
    {
        return false;
    }
    bool Ok = true;
    Ok &= FMath::IsNearlyEqual(Sun->Intensity, Golden.SunIntensity, 0.001f);
    Ok &= FLinearColor(Sun->LightColor).Equals(Golden.SunColor, ColorTolerance);
    Ok &= FMath::IsNearlyEqual(Sun->GetRelativeRotation().Pitch, Golden.SunElevationDeg, 0.01f);
    Ok &= FMath::IsNearlyEqual(Sun->GetRelativeRotation().Yaw, Golden.SunAzimuthDeg, 0.01f);
    Ok &= FLinearColor(Ambient->LightColor).Equals(Golden.AmbientSky, ColorTolerance);
    Ok &= Ambient->LowerHemisphereColor.Equals(Golden.AmbientGround, 0.001f);
    Ok &= FMath::IsNearlyEqual(Fire->Intensity, Golden.FireIntensity, 0.001f);
    return Ok;
}
}

bool FTDDM1LightingStateSwitcherTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(TEXT("TDDLightingState"), EWorldType::Game, GetTransientPackage());
    TestNotNull(TEXT("Lighting test world created"), World);
    if (World == nullptr)
    {
        return false;
    }

    ATDDLightingStateSwitcher* Switcher = World->SpawnActor<ATDDLightingStateSwitcher>();
    TestNotNull(TEXT("Lighting switcher spawned"), Switcher);
    if (Switcher == nullptr)
    {
        return false;
    }

    TestNotNull(TEXT("Switcher owns a sun light"), Switcher->GetSunLight());
    TestNotNull(TEXT("Switcher owns an ambient sky light"), Switcher->GetAmbientLight());
    TestNotNull(TEXT("Switcher owns a firelight"), Switcher->GetFireLight());
    if (Switcher->GetSunLight() == nullptr || Switcher->GetAmbientLight() == nullptr || Switcher->GetFireLight() == nullptr)
    {
        return false;
    }

    // Initial state: dawn applied at construction.
    TestTrue(TEXT("Initial state is Dawn"),
             Switcher->GetCurrentState() == ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn preset applied at construction"), VerifyPresetApplied(Switcher, DawnGolden));

    // Dusk: sun + ambient preset applied exactly, cooking fire off.
    Switcher->ApplyState(ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk preset applied"), VerifyPresetApplied(Switcher, DuskGolden));
    TestTrue(TEXT("Dusk firelight is off"),
             FMath::IsNearlyEqual(Switcher->GetFireLight()->Intensity, 0.0f, 0.001f));

    // Night: cooking fire on at the preset intensity, dim sun, deep ambient.
    Switcher->ApplyState(ETDDLightingState::Night);
    TestTrue(TEXT("Night is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Night);
    TestTrue(TEXT("Night preset applied"), VerifyPresetApplied(Switcher, NightGolden));

    // Cooking-fire flicker: the switcher's Tick modulates the night firelight
    // around the base intensity (0.85 + 0.15*sin(12t)) without changing the
    // preset. The switcher declares PrimaryActorTick.bCanEverTick, so the
    // genuine UE 5.8.4 mechanism to advance its lifecycle is the world tick
    // (UWorld::Tick is public; the engine calls it every frame) — the
    // switcher's protected Tick runs as part of it.
    const float NightFireBase = NightGolden.FireIntensity;
    World->Tick(LEVELTICK_All, 0.05f);
    const float FlickeredIntensity = Switcher->GetFireLight()->Intensity;
    TestTrue(TEXT("Night firelight flickers (changed from base)"),
             !FMath::IsNearlyEqual(FlickeredIntensity, NightFireBase, 0.001f));
    TestTrue(TEXT("Night firelight stays within the flicker envelope"),
             FlickeredIntensity >= 0.85f * NightFireBase - 0.001f &&
             FlickeredIntensity <= 1.0f * NightFireBase + 0.001f);
    for (int32 Step = 0; Step < 20; ++Step)
    {
        World->Tick(LEVELTICK_All, 0.05f);
        const float Intensity = Switcher->GetFireLight()->Intensity;
        if (!(Intensity >= 0.85f * NightFireBase - 0.001f &&
              Intensity <= 1.0f * NightFireBase + 0.001f))
        {
            TestTrue(TEXT("Night firelight stays within the flicker envelope over time"), false);
            return false;
        }
    }
    TestTrue(TEXT("Night firelight stays within the flicker envelope over time"), true);

    // Back to dawn: firelight off again and dawn preset reapplied.
    Switcher->ApplyState(ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn is the current state again"),
             Switcher->GetCurrentState() == ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn preset reapplied"), VerifyPresetApplied(Switcher, DawnGolden));

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
