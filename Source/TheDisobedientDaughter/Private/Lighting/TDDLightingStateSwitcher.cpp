#include "Lighting/TDDLightingStateSwitcher.h"

#include "Components/DirectionalLightComponent.h"
#include "Components/HemisphericalLightComponent.h"
#include "Components/PointLightComponent.h"

ATDDLightingStateSwitcher::ATDDLightingStateSwitcher()
{
    PrimaryActorTick.bCanEverTick = true;

    SunLight = CreateDefaultSubobject<UDirectionalLightComponent>(TEXT("SunLight"));
    AmbientLight = CreateDefaultSubobject<UHemisphericalLightComponent>(TEXT("AmbientLight"));
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
        SunLight->SetLightColor(Preset->SunColor);
        SunLight->SetRelativeRotation(FRotator(Preset->SunElevationDeg, Preset->SunAzimuthDeg, 0.0f));
    }
    if (AmbientLight != nullptr)
    {
        AmbientLight->SetSkyColor(Preset->AmbientSky);
        AmbientLight->SetGroundColor(Preset->AmbientGround);
    }
    if (FireLight != nullptr)
    {
        FireLight->SetIntensity(Preset->FireIntensity);
    }
}
