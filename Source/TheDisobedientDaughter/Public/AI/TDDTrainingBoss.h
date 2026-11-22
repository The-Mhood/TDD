#pragma once

#include "CoreMinimal.h"
#include "AI/TDDTrainingEnemy.h"
#include "TDDTrainingBoss.generated.h"

class UTDDBossPhaseComponent;

/** Greybox boss actor using the same actor combat and AI path as the trainer. */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDTrainingBoss : public ATDDTrainingEnemy
{
    GENERATED_BODY()

public:
    ATDDTrainingBoss();

    UTDDBossPhaseComponent* GetBossPhaseComponent() const { return BossPhaseComponent; }

private:
    UPROPERTY(VisibleAnywhere, Category="TDD|Boss")
    TObjectPtr<UTDDBossPhaseComponent> BossPhaseComponent;
};
