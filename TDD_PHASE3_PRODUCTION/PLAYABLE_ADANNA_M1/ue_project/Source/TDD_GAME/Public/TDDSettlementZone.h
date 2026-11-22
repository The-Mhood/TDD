// TDDSettlementZone.h — Phase 1 settlement anchor actor.
// One per settlement. Holds the settlement's world anchor and, on market-day
// changes, spawns a budgeted subset of population actors (tiers) and market
// stalls toward the density model. The FULL logical population is queried from
// the population subsystem and logged; only the budgeted subset is spawned —
// demonstrating that the simulation is independent of the render budget.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/SceneComponent.h"
#include "TDDWorldLogic.h"
#include "TDDSettlementZone.generated.h"

class ATDDPopulationActor;
class ATDDMarketStall;

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API ATDDSettlementZone : public AActor
{
    GENERATED_BODY()

public:
    ATDDSettlementZone();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    FName GetSettlementId() const { return SettlementId; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    void SetSettlementId(FName InId) { SettlementId = InId; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    FString GetSettlementName() const { return SettlementName; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    void SetSettlementName(const FString& InName) { SettlementName = InName; }

    /** Recompute spawned population for the current calendar state. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    void RefreshPopulation(int64 WorldDay, float TimeOfDay);

    /** Number of population actors currently spawned (rendered subset). */
    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    int32 GetSpawnedPopulationCount() const { return SpawnedPopulation.Num(); }

    /** The settlement's full logical population (independent of spawned actors). */
    UFUNCTION(BlueprintCallable, Category = "TDD|Settlement")
    int32 GetLogicalPopulation() const { return LogicalPopulation; }

protected:
    void SpawnPopulationTiers(const TDDWorld::FActiveTierCounts& Counts);
    void ClearPopulation();
    void SpawnMarketStalls(int32 Count);
    void ClearMarketStalls();

    UPROPERTY(VisibleAnywhere, Category = "TDD|Settlement")
    TObjectPtr<USceneComponent> ZoneRoot;

    UPROPERTY(EditAnywhere, Category = "TDD|Settlement")
    FName SettlementId;

    UPROPERTY(EditAnywhere, Category = "TDD|Settlement")
    FString SettlementName = TEXT("Settlement");

    UPROPERTY(Transient, BlueprintReadOnly, Category = "TDD|Settlement")
    int32 LogicalPopulation = 0;

    UPROPERTY(Transient, BlueprintReadOnly, Category = "TDD|Settlement")
    bool bMarketActive = false;

    TArray<TObjectPtr<ATDDPopulationActor>> SpawnedPopulation;
    TArray<TObjectPtr<ATDDMarketStall>> SpawnedStalls;

    UPROPERTY(EditAnywhere, Category = "TDD|Settlement")
    FVector PopulationSpawnOffsetsCm[8] = {};

    // How many market stalls to spawn on the settlement's market day.
    UPROPERTY(EditAnywhere, Category = "TDD|Settlement", meta=(ClampMin="0", ClampMax="40"))
    int32 MarketStallCount = 12;
};
