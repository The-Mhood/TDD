#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TDDTrainingEnemy.generated.h"

class UTDDCharacterStateComponent;
class UTDDCombatComponent;
class UTDDCombatBrainComponent;
class UStaticMeshComponent;

/** Placeholder combat actor for wiring and functional integration tests. */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDTrainingEnemy : public ACharacter
{
    GENERATED_BODY()

public:
    ATDDTrainingEnemy();

    UTDDCombatComponent* GetCombatComponent() const { return CombatComponent; }
    UTDDCharacterStateComponent* GetStateComponent() const { return StateComponent; }

private:
    UPROPERTY(VisibleAnywhere, Category="TDD")
    TObjectPtr<UTDDCharacterStateComponent> StateComponent;

    UPROPERTY(VisibleAnywhere, Category="TDD")
    TObjectPtr<UTDDCombatComponent> CombatComponent;

    UPROPERTY(VisibleAnywhere, Category="TDD")
    TObjectPtr<UTDDCombatBrainComponent> CombatBrain;

    UPROPERTY(VisibleAnywhere, Category="TDD")
    TObjectPtr<UStaticMeshComponent> GreyboxVisual;
};
