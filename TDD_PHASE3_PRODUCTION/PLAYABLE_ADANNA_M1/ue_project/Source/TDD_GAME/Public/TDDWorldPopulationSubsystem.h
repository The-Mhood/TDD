// TDDWorldPopulationSubsystem.h — Phase 1 world population simulation.
//
// Maintains the FULL LOGICAL population (every settlement's households,
// occupations, routines, destinations) as data + computation, INDEPENDENT of how
// many NPC actors are currently rendered. Render activation is a separate,
// distance/budget concern: this subsystem computes the target active tiers per
// settlement from the density model, and the level spawns actors toward them.
//
// This is the WORLD_ARCHITECTURE UTDDLocationRegistry + UTDDCrowdSubsystem
// population contract, implemented against the TDDWorldLogic density model.
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TDDWorldLogic.h"
#include "TDDWorldPopulationSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FTDDActiveTierCounts
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Named = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Crowd = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Scripted = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Background = 0;

    int32 Total() const { return Named + Crowd + Scripted + Background; }
};

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API UTDDWorldPopulationSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDWorldPopulationSubsystem();

    // USubsystem lifecycle: world subsystems use Initialize/Deinitialize,
    // not BeginPlay/EndPlay (which exist only on AActor).
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    /** The full regional logical population — exists whether or not actors render. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    int32 GetRegionalLogicalPopulation() const;

    /** Logical population (residential + economic) for one settlement id. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    int32 GetSettlementLogicalPopulation(const FName& SettlementId) const;

    /**
     * Compute the target active (rendered) tier counts for a settlement given
     * the current calendar day, time-of-day, market-day flag, festival flag and
     * weather. The level uses this to spawn/despawn actors. The logical
     * population behind it is never reduced by this.
     */
    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    FTDDActiveTierCounts ComputeActivePopulation(
        const FName& SettlementId,
        int64 WorldDay,
        float TimeOfDay,
        bool bIsMarketDay,
        bool bIsFestival) const;

    /**
     * Demonstration accessor: the logical population is queryable at full regional
     * scale even when no actors are spawned. Returns the full figure.
     */
    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    int32 GetLogicalPopulationSnapshot() const;

private:
    UPROPERTY(Transient)
    TArray<FName> SettlementIds;

    UPROPERTY(Transient)
    TMap<FName, int32> SettlementLogicalPopulation;
};
