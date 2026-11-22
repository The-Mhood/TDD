#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TDDLightingStateSwitcher.generated.h"

class UDirectionalLightComponent;
class USkyLightComponent;
class UPointLightComponent;

/**
 * Lighting state machine. Declared at GLOBAL scope with UENUM so UHT can
 * reflect the type for the CurrentState UPROPERTY and the ApplyState
 * UFUNCTION parameter (UENUM may only appear in global scopes); underlying
 * type unchanged (uint8).
 */
UENUM(BlueprintType)
enum class ETDDLightingState : uint8
{
    Dawn,
    Dusk,
    Night
};

/** One provisional CH01 lighting state preset (W1 D13 keys ST01/ST03/ST04). */
USTRUCT(BlueprintType)
struct FTDDLightingPreset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    float SunIntensity = 2.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    FLinearColor SunColor = FLinearColor(1.0f, 0.82f, 0.62f);

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    float SunElevationDeg = 12.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    float SunAzimuthDeg = 70.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    FLinearColor AmbientSky = FLinearColor(0.45f, 0.50f, 0.60f);

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    FLinearColor AmbientGround = FLinearColor(0.22f, 0.18f, 0.14f);

    /** Night cooking-fire point-light intensity (matches approved VFX direction). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting")
    float FireIntensity = 0.0f;
};

/**
 * Switches the level between the three provisional CH01 lighting states
 * (dawn/dusk/night). Owns the sun (directional), ambient (hemispherical) and
 * firelight (point, flickering) components so states are applied atomically
 * without touching architecture or dressing. No market/ritual/festival states.
 */
UCLASS(ClassGroup=(TDD))
class THEDISOBEDIENTDAUGHTER_API ATDDLightingStateSwitcher : public AActor
{
    GENERATED_BODY()

public:
    ATDDLightingStateSwitcher();

    /** Apply a state to every owned light component. */
    UFUNCTION(BlueprintCallable, Category="TDD|Lighting")
    void ApplyState(ETDDLightingState State);

    ETDDLightingState GetCurrentState() const { return CurrentState; }

    UDirectionalLightComponent* GetSunLight() const { return SunLight; }
    USkyLightComponent* GetAmbientLight() const { return AmbientLight; }
    UPointLightComponent* GetFireLight() const { return FireLight; }

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

private:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UDirectionalLightComponent> SunLight;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    TObjectPtr<USkyLightComponent> AmbientLight;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UPointLightComponent> FireLight;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    ETDDLightingState CurrentState = ETDDLightingState::Dawn;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    FTDDLightingPreset DawnPreset;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    FTDDLightingPreset DuskPreset;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Lighting", meta=(AllowPrivateAccess="true"))
    FTDDLightingPreset NightPreset;

    float FireFlickerTime = 0.0f;
};
