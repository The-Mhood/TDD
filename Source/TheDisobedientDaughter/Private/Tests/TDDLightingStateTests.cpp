#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/HemisphericalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Lighting/TDDLightingStateSwitcher.h"

/**
 * CH01 provisional lighting states: the switcher owns sun/ambient/firelight
 * and applies each state's preset atomically (W1 D13 keys ST01/ST03/ST04).
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1LightingStateSwitcherTest,
    "TDD.M1.Lighting.StateSwitcher",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDM1LightingStateSwitcherTest::RunTest(const FString& Parameters)
{
    ATDDLightingStateSwitcher* Switcher = GetDefault<ATDDLightingStateSwitcher>();
    TestNotNull(TEXT("Lighting switcher is registered"), Switcher);
    if (Switcher == nullptr)
    {
        return false;
    }

    TestNotNull(TEXT("Switcher owns a sun light"), Switcher->GetSunLight());
    TestNotNull(TEXT("Switcher owns an ambient light"), Switcher->GetAmbientLight());
    TestNotNull(TEXT("Switcher owns a firelight"), Switcher->GetFireLight());
    if (Switcher->GetSunLight() == nullptr || Switcher->GetAmbientLight() == nullptr || Switcher->GetFireLight() == nullptr)
    {
        return false;
    }

    // Dusk: sun preset applied exactly.
    Switcher->ApplyState(ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk sun intensity matches the preset"),
             FMath::IsNearlyEqual(Switcher->GetSunLight()->Intensity, Switcher->DuskPreset.SunIntensity, 0.001f));
    TestTrue(TEXT("Dusk sun colour matches the preset"),
             Switcher->GetSunLight()->LightColor.Equals(Switcher->DuskPreset.SunColor, 0.001f));
    TestTrue(TEXT("Dusk sun elevation matches the preset"),
             FMath::IsNearlyEqual(Switcher->GetSunLight()->GetRelativeRotation().Pitch,
                                  Switcher->DuskPreset.SunElevationDeg, 0.01f));
    TestTrue(TEXT("Dusk ambient sky matches the preset"),
             Switcher->GetAmbientLight()->SkyColor.Equals(Switcher->DuskPreset.AmbientSky, 0.001f));
    TestTrue(TEXT("Dusk firelight is off"),
             FMath::IsNearlyEqual(Switcher->GetFireLight()->Intensity, 0.0f, 0.001f));

    // Night: firelight on at the preset intensity.
    Switcher->ApplyState(ETDDLightingState::Night);
    TestTrue(TEXT("Night is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Night);
    TestTrue(TEXT("Night firelight is on at the preset intensity"),
             FMath::IsNearlyEqual(Switcher->GetFireLight()->Intensity,
                                  Switcher->NightPreset.FireIntensity, 0.001f));

    // Back to dawn: firelight off again.
    Switcher->ApplyState(ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn firelight is off"),
             FMath::IsNearlyEqual(Switcher->GetFireLight()->Intensity,
                                  Switcher->DawnPreset.FireIntensity, 0.001f));
    TestTrue(TEXT("Dawn sun intensity matches the preset"),
             FMath::IsNearlyEqual(Switcher->GetSunLight()->Intensity, Switcher->DawnPreset.SunIntensity, 0.001f));

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
