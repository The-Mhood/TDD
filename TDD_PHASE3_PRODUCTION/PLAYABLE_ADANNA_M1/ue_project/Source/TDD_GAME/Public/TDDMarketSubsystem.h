// TDDMarketSubsystem.h — Phase 1 market-day system.
// On a settlement's assigned market day, the market activates: traders, stalls,
// goods and NPC activity surge. The correct settlement is activated by the
// calendar; this subsystem computes the market state and the density the level
// spawns toward. No market-day assignment is hard-coded in behaviour — it reads
// the settlement's assigned day from the shared logic core (flagged [A] adaptive
// for Story/Research confirmation in the source register).
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TDDWorldLogic.h"
#include "TDDMarketSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FTDDMarketState
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName SettlementId;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString SettlementName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool bActive = false;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    EMarketDay MarketDay = EMarketDay::Eke;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Traders = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 Stalls = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 CrowdPopulation = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 BackgroundPopulation = 0;
};

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API UTDDMarketSubsystem : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDMarketSubsystem();

    // USubsystem lifecycle: world subsystems use Initialize/Deinitialize,
    // not BeginPlay/EndPlay (which exist only on AActor).
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    /**
     * Compute the market state for a settlement on a given world day. The market
     * is active only when the day matches the settlement's assigned market day.
     * Stalls/traders/population derive from the density model.
     */
    UFUNCTION(BlueprintCallable, Category = "TDD|Market")
    FTDDMarketState ComputeMarketState(
        const FName& SettlementId,
        int64 WorldDay,
        float TimeOfDay) const;

    /** The settlement id whose market is active today, or Empty if none. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Market")
    FName GetActiveMarketToday(int64 WorldDay, float TimeOfDay) const;

private:
    UPROPERTY(Transient)
    TArray<FName> SettlementIds;
};
