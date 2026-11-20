#include "Lighting/TDDLightingStateSwitcher.h"

#include "Components/DirectionalLightComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/SkyLightComponent.h"

ATDDLightingStateSwitcher::ATDDLightingStateSwitcher()
{
    PrimaryActorTick.bCanEverTick = true;

    SunLight = CreateDefaultSubobject<UDirectionalLightComponent>(TEXT("SunLight"));
    AmbientLight = CreateDefaultSubobject<USkyLightComponent>(TEXT("AmbientLight"));
    FireLight = CreateDefaultSubobject<UPointLightComponent>(TEXT("FireLight"));

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
        // UE 5.8.4: ULightComponent::LightColor is FColor; SetLightColor takes
        // (FLinearColor, bSRGB). Preset values are authored linear, so
        // bSRGB=false stores them via the engine's sRGB byte encoding; the
        // engine's own read path FLinearColor(LightColor) round-trips them.
        SunLight->SetLightColor(Preset->SunColor, /*bSRGB=*/false);
        SunLight->SetRelativeRotation(FRotator(Preset->SunElevationDeg, Preset->SunAzimuthDeg, 0.0f));
    }
    if (AmbientLight != nullptr)
    {
        // UE 5.8.4 sky light ambient model: the sky/upper colour is the
        // inherited LightColor (FColor); the ground colour is
        // LowerHemisphereColor (FLinearColor). There is no
        // upper-hemisphere colour member exists in 5.8.4.
        AmbientLight->SetLightColor(Preset->AmbientSky, /*bSRGB=*/false);
        AmbientLight->SetLowerHemisphereColor(Preset->AmbientGround);
    }
    if (FireLight != nullptr)
    {
        FireLight->SetIntensity(Preset->FireIntensity);
    }
}
