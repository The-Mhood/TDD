#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Core/TDDStateRules.h"
#include "TDDCharacterStateComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FTDDPlayerStateChanged, int32, PreviousState, int32, NewState);

/**
 * Unreal-facing owner for the pure player-state contract. It is the single
 * runtime state authority for the owning character; gameplay components ask
 * it to transition instead of maintaining parallel state booleans.
 */
UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class THEDISOBEDIENTDAUGHTER_API UTDDCharacterStateComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTDDCharacterStateComponent();

    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category="TDD|State")
    bool RequestState(int32 TargetState, FName Reason);

    UFUNCTION(BlueprintCallable, Category="TDD|State")
    bool ForceState(int32 TargetState);

    UFUNCTION(BlueprintCallable, Category="TDD|State")
    int32 GetCurrentState() const;

    UFUNCTION(BlueprintCallable, Category="TDD|State")
    float GetTimeInState() const;

    UFUNCTION(BlueprintCallable, Category="TDD|State")
    void SetLocomotionIntent(bool bIsMoving, bool bWantsSprint);

    UPROPERTY(BlueprintAssignable, Category="TDD|State")
    FTDDPlayerStateChanged OnStateChanged;

private:
    void PublishIfChanged();

    TDD::State::FTDDPureStateMachine Machine;
    TDD::State::ETDDPlayerState LastPublishedState = TDD::State::ETDDPlayerState::Idle;
};
