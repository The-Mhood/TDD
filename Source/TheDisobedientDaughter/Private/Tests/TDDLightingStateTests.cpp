#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
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

bool VerifyPresetApplied(ATDDLightingStateSwitcher* Switcher, const FPresetGoldenValues& Golden, const FString& Context)
{
    UDirectionalLightComponent* Sun = Switcher->GetSunLight();
    USkyLightComponent* Ambient = Switcher->GetAmbientLight();
    UPointLightComponent* Fire = Switcher->GetFireLight();
    if (Sun == nullptr || Ambient == nullptr || Fire == nullptr)
    {
        UE_LOG(LogTemp, Error, TEXT("TDD lighting preset %s: a light component is missing"), *Context);
        return false;
    }
    // Report actual vs expected for every property so a failure pinpoints the
    // exact cause instead of only the aggregate Boolean.
    bool Ok = true;
    const auto Report = [&Ok, &Context](bool Result, const FString& Property, const FString& Actual, const FString& Expected)
    {
        Ok = Ok && Result;
        if (!Result)
        {
            UE_LOG(LogTemp, Error, TEXT("TDD lighting preset %s: %s mismatch (actual %s, expected %s)"),
                *Context, *Property, *Actual, *Expected);
        }
    };

    const FLinearColor SunColorActual = FLinearColor(Sun->LightColor);
    Report(FMath::IsNearlyEqual(Sun->Intensity, Golden.SunIntensity, 0.001f), TEXT("SunIntensity"),
        FString::Printf(TEXT("%.4f"), Sun->Intensity),
        FString::Printf(TEXT("%.4f"), Golden.SunIntensity));
    Report(SunColorActual.Equals(Golden.SunColor, ColorTolerance), TEXT("SunColor"),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), SunColorActual.R, SunColorActual.G, SunColorActual.B),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), Golden.SunColor.R, Golden.SunColor.G, Golden.SunColor.B));
    Report(FMath::IsNearlyEqual(Sun->GetRelativeRotation().Pitch, Golden.SunElevationDeg, 0.01f), TEXT("SunPitchDeg"),
        FString::Printf(TEXT("%.4f"), Sun->GetRelativeRotation().Pitch),
        FString::Printf(TEXT("%.4f"), Golden.SunElevationDeg));
    // Azimuth is a circular angle: compare via the shortest angular distance
    // (a stored yaw of -160 is the same angle as the preset's 200).
    Report(FMath::Abs(FMath::FindDeltaAngleDegrees(Golden.SunAzimuthDeg, Sun->GetRelativeRotation().Yaw)) <= 0.01f,
        TEXT("SunAzimuthDeg"),
        FString::Printf(TEXT("%.4f"), Sun->GetRelativeRotation().Yaw),
        FString::Printf(TEXT("%.4f"), Golden.SunAzimuthDeg));
    const FLinearColor AmbientSkyActual = FLinearColor(Ambient->LightColor);
    Report(AmbientSkyActual.Equals(Golden.AmbientSky, ColorTolerance), TEXT("AmbientSkyColor"),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), AmbientSkyActual.R, AmbientSkyActual.G, AmbientSkyActual.B),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), Golden.AmbientSky.R, Golden.AmbientSky.G, Golden.AmbientSky.B));
    Report(Ambient->LowerHemisphereColor.Equals(Golden.AmbientGround, 0.001f), TEXT("AmbientGroundColor"),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), Ambient->LowerHemisphereColor.R, Ambient->LowerHemisphereColor.G, Ambient->LowerHemisphereColor.B),
        FString::Printf(TEXT("%.4f,%.4f,%.4f"), Golden.AmbientGround.R, Golden.AmbientGround.G, Golden.AmbientGround.B));
    Report(FMath::IsNearlyEqual(Fire->Intensity, Golden.FireIntensity, 0.001f), TEXT("FireIntensity"),
        FString::Printf(TEXT("%.4f"), Fire->Intensity),
        FString::Printf(TEXT("%.4f"), Golden.FireIntensity));
    return Ok;
}
}

bool FTDDM1LightingStateSwitcherTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, /*bInformEngineOfWorld=*/false,
        TEXT("TDDLightingState"), GetTransientPackage());
    TestNotNull(TEXT("Lighting test world created"), World);
    if (World == nullptr)
    {
        return false;
    }

    // Register the test world with the engine using the proven world-context
    // fixture (D-W1D8-018): UWorld::CreateWorld with bInformEngineOfWorld=false
    // leaves the world unregistered, so UWorld::Tick crashes in
    // UEngine::GetWorldContextFromWorldChecked() — the demonstrated failure of
    // the manual tick sequence below.
    FWorldContext& WorldContext = GEngine->CreateNewWorldContext(EWorldType::Game);
    WorldContext.SetCurrentWorld(World);
    World->InitializeActorsForPlay(FURL());
    if (IsValid(World->GetWorldSettings()))
    {
        // Mark the world as begun so the spawned switcher receives BeginPlay.
        World->GetWorldSettings()->NotifyBeginPlay();
        World->GetWorldSettings()->NotifyMatchStarted();
    }

    // The engine world context must exist and resolve to the exact test world.
    FWorldContext* Context = GEngine->GetWorldContextFromWorld(World);
    TestTrue(TEXT("Test world has a registered engine world context"), Context != nullptr);
    TestTrue(TEXT("World context resolves to the exact test world"),
             Context != nullptr && Context->World() == World);

    ATDDLightingStateSwitcher* Switcher = World->SpawnActor<ATDDLightingStateSwitcher>();
    TestNotNull(TEXT("Lighting switcher spawned"), Switcher);
    if (Switcher == nullptr)
    {
        // Teardown must still run: end play, destroy the world's actors and
        // the world, and release the engine world context.
        World->BeginTearingDown();
        for (TActorIterator<AActor> It(World, AActor::StaticClass(), EActorIteratorFlags::AllActors); It; ++It)
        {
            It->Destroy();
        }
        GEngine->DestroyWorldContext(World);
        World->DestroyWorld(false);
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
    TestTrue(TEXT("Dawn preset applied at construction"), VerifyPresetApplied(Switcher, DawnGolden, TEXT("Dawn at construction")));

    // Dusk: sun + ambient preset applied exactly, cooking fire off.
    Switcher->ApplyState(ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Dusk);
    TestTrue(TEXT("Dusk preset applied"), VerifyPresetApplied(Switcher, DuskGolden, TEXT("Dusk")));
    TestTrue(TEXT("Dusk firelight is off"),
             FMath::IsNearlyEqual(Switcher->GetFireLight()->Intensity, 0.0f, 0.001f));

    // Night: cooking fire on at the preset intensity, dim sun, deep ambient.
    Switcher->ApplyState(ETDDLightingState::Night);
    TestTrue(TEXT("Night is the current state"),
             Switcher->GetCurrentState() == ETDDLightingState::Night);
    TestTrue(TEXT("Night preset applied"), VerifyPresetApplied(Switcher, NightGolden, TEXT("Night")));

    // Cooking-fire flicker: the switcher's Tick modulates the night firelight
    // around the base intensity (0.925 + 0.075*sin(12t), spanning the
    // documented 0.85–1.0 envelope) without changing the preset. The switcher
    // declares PrimaryActorTick.bCanEverTick, so the genuine UE 5.8.4
    // mechanism to advance its lifecycle is the world tick (UWorld::Tick is
    // public; the engine calls it every frame) — the switcher's protected
    // Tick runs as part of it.
    const float NightFireBase = NightGolden.FireIntensity;
    World->Tick(LEVELTICK_All, 0.05f);
    const float FlickeredIntensity = Switcher->GetFireLight()->Intensity;
    TestTrue(TEXT("Night firelight flickers (changed from base)"),
             !FMath::IsNearlyEqual(FlickeredIntensity, NightFireBase, 0.001f));
    TestTrue(TEXT("Night firelight stays within the flicker envelope"),
             FlickeredIntensity >= 0.85f * NightFireBase - 0.001f &&
             FlickeredIntensity <= 1.0f * NightFireBase + 0.001f);
    bool AllStepsInEnvelope = true;
    for (int32 Step = 0; Step < 20; ++Step)
    {
        World->Tick(LEVELTICK_All, 0.05f);
        const float Intensity = Switcher->GetFireLight()->Intensity;
        if (!(Intensity >= 0.85f * NightFireBase - 0.001f &&
              Intensity <= 1.0f * NightFireBase + 0.001f))
        {
            AllStepsInEnvelope = false;
            break;
        }
    }
    TestTrue(TEXT("Night firelight stays within the flicker envelope over time"), AllStepsInEnvelope);

    // Back to dawn: firelight off again and dawn preset reapplied.
    Switcher->ApplyState(ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn is the current state again"),
             Switcher->GetCurrentState() == ETDDLightingState::Dawn);
    TestTrue(TEXT("Dawn preset reapplied"), VerifyPresetApplied(Switcher, DawnGolden, TEXT("Dawn reapplied")));

    // Teardown: end play first (CleanupWorld warns "missing call to EndPlay"
    // when a begun world is cleaned up), then destroy the world's actors and
    // the world, and release the engine world context (order matches the
    // proven encounter fixture). The assertion macros record failures
    // without aborting, so this always runs.
    World->EndPlay(EEndPlayReason::Destroyed);
    World->BeginTearingDown();
    for (TActorIterator<AActor> It(World, AActor::StaticClass(), EActorIteratorFlags::AllActors); It; ++It)
    {
        It->Destroy();
    }
    GEngine->DestroyWorldContext(World);
    World->DestroyWorld(false);

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
