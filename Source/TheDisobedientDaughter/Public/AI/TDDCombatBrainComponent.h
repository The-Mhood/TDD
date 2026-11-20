#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "TDDCombatBrainComponent.generated.h"

class UTDDCharacterStateComponent;
class UTDDCombatComponent;

/** Small integration brain for the training enemy: acquire player, close distance,
 * face the target, and ask the world director for capped attack permission. */
UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class THEDISOBEDIENTDAUGHTER_API UTDDCombatBrainComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTDDCombatBrainComponent();
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|AI", meta=(ClampMin="0.0"))
    float StopDistance = 140.0f;

private:
    bool bRegisteredWithDirector = false;
};
