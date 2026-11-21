#include "Lighting/TDDLightingStateSwitcher.h"

#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SceneComponent.h"
#include "Components/SkyLightComponent.h"

ATDDLightingStateSwitcher::ATDDLightingStateSwitcher()
{
    PrimaryActorTick.bCanEverTick = true;

    // Explicit root: the switcher owns only light components, which attach
    // to the root. Without an explicit root the engine logs a missing
    // RootComponent warning at spawn — the actor genuinely has no root.
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    SunLight = CreateDefaultSubobject<UDirectionalLightComponent>(TEXT("SunLight"));
    AmbientLight = CreateDefaultSubobject<USkyLightComponent>(TEXT("AmbientLight"));
    FireLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("FireLight"));

    // Approved CH01 preset contract (W1 D13 keys ST01/ST03/ST04): the
    // preset defaults must carry the approved values so a spawned switcher
    // applies the real dawn/dusk/night states without editor configuration.
    // Previously the presets defaulted to the struct's dawn values, so the
    // dusk/night states silently applied dawn values and the night cooking
    // fire never activated (fire intensity defaulted to 0).
    DawnPreset.SunIntensity = 2.0f;
    DawnPreset.SunColor = FLinearColor(1.0f, 0.82f, 0.62f);
    DawnPreset.SunElevationDeg = 12.0f;
    DawnPreset.SunAzimuthDeg = 70.0f;
    DawnPreset.AmbientSky = FLinearColor(0.45f, 0.50f, 0.60f);
    DawnPreset.AmbientGround = FLinearColor(0.22f, 0.18f, 0.14f);
    DawnPreset.FireIntensity = 0.0f;

    DuskPreset.SunIntensity = 1.6f;
    DuskPreset.SunColor = FLinearColor(1.0f, 0.55f, 0.28f);
    DuskPreset.SunElevationDeg = 6.0f;
    DuskPreset.SunAzimuthDeg = 285.0f;
    DuskPreset.AmbientSky = FLinearColor(0.40f, 0.32f, 0.42f);
    DuskPreset.AmbientGround = FLinearColor(0.20f, 0.14f, 0.12f);
    DuskPreset.FireIntensity = 0.0f;

    NightPreset.SunIntensity = 0.35f;
    NightPreset.SunColor = FLinearColor(0.55f, 0.62f, 0.80f);
    NightPreset.SunElevationDeg = -24.0f;
    NightPreset.SunAzimuthDeg = 200.0f;
    NightPreset.AmbientSky = FLinearColor(0.06f, 0.08f, 0.14f);
    NightPreset.AmbientGround = FLinearColor(0.04f, 0.04f, 0.05f);
    NightPreset.FireIntensity = 8.0f;

    ApplyState(ETDDLightingState::Dawn);
}

void ATDDLightingStateSwitcher::BeginPlay()
{
    Super::BeginPlay();
    ApplyState(CurrentState);
}

void ATDDLightingStateSwitcher::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (CurrentState == ETDDLightingState::Night && FireLight != nullptr && NightPreset.FireIntensity > 0.0f)
    {
        FireFlickerTime += DeltaSeconds;
        const float Flicker = 0.85f + 0.15f * FMath::Sin(FireFlickerTime * 12.0f);
        FireLight->SetIntensity(NightPreset.FireIntensity * Flicker);
    }
}

void ATDDLightingStateSwitcher::ApplyState(ETDDLightingState State)
{
    CurrentState = State;
    const FTDDLightingPreset* Preset = nullptr;
    switch (State)
    {
    case ETDDLightingState::Dawn:
        Preset = &DawnPreset;
        break;
    case ETDDLightingState::Dusk:
        Preset = &DuskPreset;
        break;
    case ETDDLightingState::Night:
        Preset = &NightPreset;
        break;
    }
    if (Preset == nullptr)
    {
        return;
    }
    if (SunLight != nullptr)
    {
        SunLight->SetIntensity(Preset->SunIntensity);
        // UE 5.8.4: ULightComponent::LightColor is FColor; SetLightColor
        // encodes the authored-linear preset to sRGB bytes when bSRGB=true
        // (FLinearColor::ToFColor(true)). The engine's own read path
        // FLinearColor(LightColor) applies sRGBToLinear to the stored bytes,
        // so bSRGB=true round-trips the preset exactly. bSRGB=false would
        // store raw linear bytes and double-convert on read.
        SunLight->SetLightColor(Preset->SunColor, /*bSRGB=*/true);
        SunLight->SetRelativeRotation(FRotator(Preset->SunElevationDeg, Preset->SunAzimuthDeg, 0.0f));
    }
    if (AmbientLight != nullptr)
    {
        // UE 5.8.4 sky light ambient model: the sky/upper colour is the
        // inherited LightColor (FColor); the ground colour is
        // LowerHemisphereColor (FLinearColor). There is no
        // upper-hemisphere colour member exists in 5.8.4.
        // USkyLightComponent::SetLightColor takes a single FLinearColor
        // argument in 5.8.4 (it shadows the base ULightComponent
        // SetLightColor(FLinearColor, bSRGB) used by the sun light above)
        // and encodes with bSRGB=true (SkyLightComponent.cpp), so the sky
        // colour round-trips through the engine read path like the sun.
        AmbientLight->SetLightColor(Preset->AmbientSky);
        AmbientLight->SetLowerHemisphereColor(Preset->AmbientGround);
    }
    if (FireLight != nullptr)
    {
        FireLight->SetIntensity(Preset->FireIntensity);
    }
}
