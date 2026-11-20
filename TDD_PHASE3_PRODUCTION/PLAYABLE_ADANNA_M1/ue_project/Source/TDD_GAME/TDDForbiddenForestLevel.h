#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SceneComponent.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "TDDForbiddenForestLevel.generated.h"

UCLASS()
class TDD_GAME_API ATDDForbiddenForestLevel : public AActor
{
    GENERATED_BODY()

public:
    ATDDForbiddenForestLevel();
    virtual void BeginPlay() override;

    float GetRouteProgress(const FVector& WorldLocationCm) const;
    bool TryGetNearbyInteraction(const FVector& WorldLocationCm, FString& OutMessage) const;
    const FString& GetObjectiveText() const { return ObjectiveText; }

    UPROPERTY(VisibleAnywhere, Category = "TDD|Level")
    TObjectPtr<USceneComponent> LevelRoot;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Level")
    TArray<TObjectPtr<UInstancedStaticMeshComponent>> InstancePools;

protected:
    UInstancedStaticMeshComponent* CreateInstancePool(const FName& Name, const TCHAR* MeshPath, bool bCollide, const FLinearColor& Tint);
    void AddBox(UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, const FVector& SizeCm, float YawDegrees) const;
    void AddCylinder(UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm, float HeightCm) const;
    void AddSphere(UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm) const;
    void AddCone(UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm, float HeightCm) const;
    float DistanceToRouteCm(float XCm, float YCm) const;
    void BuildRouteAndBoundary();
    void BuildForest();
    void BuildLandmarks();

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level")
    float MetresToCm = 100.0f;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level")
    int32 DeterministicSeed = 20261119;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level")
    float RouteWidthCm = 340.0f;

    TArray<FVector2D> RouteWaypointsCm;
    TArray<float> RouteSegmentStartsCm;
    TArray<FVector> InteractionPointsCm;
    TArray<FString> InteractionMessages;
    float RouteLengthCm = 0.0f;
    FString ObjectiveText = TEXT("Follow the white cloth to the Great Root Mother");
};
