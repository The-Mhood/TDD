// TDDNamedNPC.h — Phase 1 Tier-1 named NPC actor.
// Full-fidelity population actor with a routine and a dialogue/quest hook.
// The named tier is the small curated set per settlement; the bulk of the
// population is ATDDPopulationActor tiers.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TDDWorldLogic.h"
#include "TDDNamedNPC.generated.h"

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API ATDDNamedNPC : public ACharacter
{
    GENERATED_BODY()

public:
    ATDDNamedNPC();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UFUNCTION(BlueprintCallable, Category = "TDD|NPC")
    FString GetName() const { return NPCName; }

    UFUNCTION(BlueprintCallable, Category = "TDD|NPC")
    FString GetOccupation() const { return Occupation; }

    UFUNCTION(BlueprintCallable, Category = "TDD|NPC")
    FString GetRoutine() const { return Routine; }

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|NPC")
    FString NPCName = TEXT("NPC");

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|NPC")
    FString Occupation = TEXT("farmer");

    /** What this named NPC is doing on an ordinary day vs a market/festival day. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|NPC")
    FString Routine = TEXT("tends the yam plot");

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|NPC")
    FString MarketDayRoutine = TEXT("sets up a stall at the market");

    UPROPERTY(Transient)
    bool bAtMarket = false;
};
