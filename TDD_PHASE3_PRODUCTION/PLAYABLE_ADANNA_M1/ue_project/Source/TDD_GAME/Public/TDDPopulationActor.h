// TDDPopulationActor.h — Phase 1 population NPC actor (Tier 1/2/3/4).
// A lightweight population actor whose behaviour cost matches its tier:
//  Background = no AI, ambient idle; Crowd = simplified wander; Scripted = fixed
//  loop; Named = full routine. The tier is set at spawn by the population
// subsystem's density model; the actor never owns the logical population.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TDDWorldLogic.h"
#include "TDDPopulationActor.generated.h"

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API ATDDPopulationActor : public AActor
{
    GENERATED_BODY()

public:
    ATDDPopulationActor();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    ENPCTier GetTier() const { return Tier; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    void SetTier(ENPCTier InTier) { Tier = InTier; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    FString GetOccupation() const { return Occupation; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Population")
    void SetOccupation(const FString& In) { Occupation = In; }

protected:
    /** Whether this actor runs AI/tick behaviour (false for Background tier). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|Population")
    bool bSimulates = true;

    /** Deterministic wander target for Crowd/Scripted tiers. */
    void PickNewWanderTarget();

    UPROPERTY(Transient, BlueprintReadOnly, Category = "TDD|Population")
    ENPCTier Tier = ENPCTier::Background;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|Population")
    FString Occupation = TEXT("farmer");

    UPROPERTY(Transient)
    FVector WanderTargetCm = FVector::ZeroVector;

    UPROPERTY(Transient)
    float WanderTimer = 0.0f;
};
