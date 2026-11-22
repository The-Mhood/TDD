// TDDOmegaValleyLevel.h — Phase 1 Ọmà-valley core level.
// Builds the explorable Phase-1 geography: Ahanwụ and Ọmà Ukwu settlements,
// the connecting Ọmà river and road, a forest patch and the surrounding
// natural environment, using the runtime instancing blockout pattern. Places
// one TDDSettlementZone per settlement; the zones drive population spawning.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SceneComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "TDDSettlementZone.h"
#include "TDDOmegaValleyLevel.generated.h"

UCLASS()
class TDD_GAME_API ATDDOmegaValleyLevel : public AActor
{
    GENERATED_BODY()

public:
    ATDDOmegaValleyLevel();
    virtual void BeginPlay() override;

    /** Refresh every settlement zone for the current calendar/weather state. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Level")
    void RefreshSettlements(int64 WorldDay, float TimeOfDay);

    UFUNCTION(BlueprintCallable, Category = "TDD|Level")
    TArray<ATDDSettlementZone*> GetSettlements() const { return Settlements; }

protected:
    UInstancedStaticMeshComponent* CreateInstancePool(
        const FName& Name, const TCHAR* MeshPath, bool bCollide, const FLinearColor& Tint);
    void AddBox(UInstancedStaticMeshComponent* Pool, const FVector& CentreCm,
                const FVector& SizeCm, float YawDegrees) const;
    void BuildGround();
    void BuildRiver();
    void BuildRoad();
    void BuildForest();
    void PlaceSettlements();

    UPROPERTY(VisibleAnywhere, Category = "TDD|Level")
    TObjectPtr<USceneComponent> LevelRoot;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Level")
    TArray<TObjectPtr<UInstancedStaticMeshComponent>> InstancePools;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level")
    float MetresToCm = 100.0f;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level")
    int32 DeterministicSeed = 20261121;

    // Runtime-spawned state, rebuilt on BeginPlay. Intentionally NOT exposed to
    // the editor or Blueprint property system: the array is repopulated every
    // play, so a visible/editable property would show stale or dangling actor
    // references. Blueprint consumers use the GetSettlements() UFUNCTION instead.
    // (No Category metadata: a Category without an exposure specifier is a UHT
    // "Category-without-exposure" warning and has no effect.)
    UPROPERTY(Transient)
    TArray<TObjectPtr<ATDDSettlementZone>> Settlements;
};
