// TDDWeatherSubsystem.h — Phase 1 wet/dry seasonal weather with observable
// gameplay consequences (path mud, river water level, visibility, vegetation,
// NPC outdoor-activity suppression). Not a sky-only model.
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TDDWorldLogic.h"
#include "TDDWeatherSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FTDDWeatherState
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    ESeason Season = ESeason::Rainy;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float RainIntensity = 0.0f;

    /** 0 (firm) .. 1 (deep mud) — affects path traversal speed. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float MudLevel = 0.0f;

    /** 0 (river low) .. 1 (river flooded; crossing may break) — water/culvert state. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float WaterLevel = 0.0f;

    /** 0 (clear) .. 1 (heavy cloud/haze). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float VisibilityFalloff = 0.0f;

    /** 0 (dry/brown) .. 1 (dense lush green). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float VegetationGreenness = 0.0f;

    /** 0 (full outdoor activity) .. 1 (activity suppressed; shelter). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float OutdoorActivitySuppression = 0.0f;
};

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API UTDDWeatherSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDWeatherSubsystem();

    // USubsystem lifecycle: world subsystems use Initialize/Deinitialize,
    // not BeginPlay/EndPlay (which exist only on AActor).
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    /** Recompute the weather state from the current world day. Called by the calendar tick. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Weather")
    void UpdateFromWorldDay(int64 WorldDay);

    UFUNCTION(BlueprintCallable, Category = "TDD|Weather")
    const FTDDWeatherState& GetCurrentWeather() const { return Current; }

    /** Traversal-speed penalty from mud (0 = no penalty, up to ~0.5 = half speed). */
    UFUNCTION(BlueprintCallable, Category = "TDD|Weather")
    float GetTraversalSlowdown() const;

    /** True when the river is high enough that a foot crossing is broken (canoe required). */
    UFUNCTION(BlueprintCallable, Category = "TDD|Weather")
    bool IsRiverCrossingBroken() const;

private:
    UPROPERTY(Transient)
    FTDDWeatherState Current;
};
