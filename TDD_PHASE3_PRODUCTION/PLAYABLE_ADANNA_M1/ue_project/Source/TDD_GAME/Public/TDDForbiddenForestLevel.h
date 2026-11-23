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

    // Staged objective text derived from route progress and whether the final
    // interaction was acknowledged. Drives objective progression in the HUD.
    FString GetStagedObjective(float RouteProgress) const;
    int32 GetObjectiveStage(float RouteProgress) const;

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

    // Imported Forbidden Forest asset modules (set by the M1 import script to
    // /Game/TDD/Imports). When present, their meshes are instanced as the forest
    // visuals (white-cloth waymarkers, trees, ferns, rocks, Great Root Mother,
    // boundary posts) and the primitive blockout visuals are hidden while their
    // collision is retained. When absent, the primitive blockout is used unchanged.
    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestTreeModule;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestFernModule;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestRockModule;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestGreatTreeModule;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestWaymarkerModule;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Level|Modules")
    TSoftObjectPtr<UStaticMesh> ForestBoundaryPostModule;

    TArray<FVector2D> RouteWaypointsCm;
    TArray<float> RouteSegmentStartsCm;
    TArray<FVector> InteractionPointsCm;
    TArray<FString> InteractionMessages;
    float RouteLengthCm = 0.0f;
    FString ObjectiveText = TEXT("Follow the white cloth to the Great Root Mother");

    UStaticMesh* ForestTreeMesh = nullptr;
    UStaticMesh* ForestFernMesh = nullptr;
    UStaticMesh* ForestRockMesh = nullptr;
    UStaticMesh* ForestGreatTreeMesh = nullptr;
    UStaticMesh* ForestWaymarkerMesh = nullptr;
    UStaticMesh* ForestBoundaryPostMesh = nullptr;
    bool bUsingForestModules = false;

    void LoadForestModules();
    void PlaceForestModuleVisuals();
};
