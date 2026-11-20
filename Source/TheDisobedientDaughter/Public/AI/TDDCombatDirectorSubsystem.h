#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "AI/TDDAIPureCore.h"
#include "TDDCombatDirectorSubsystem.generated.h"

class UTDDCombatComponent;

/** World-scoped adapter enforcing the pure attack-token concurrency policy. */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API UTDDCombatDirectorSubsystem : public UTickableWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDCombatDirectorSubsystem();

    virtual void Tick(float DeltaTime) override;
    virtual TStatId GetStatId() const override;
    virtual bool IsTickable() const override { return !IsTemplate() && RegisteredEnemies.Num() > 0; }

    void RegisterEnemy(UTDDCombatComponent* Combatant);
    void UnregisterEnemy(UTDDCombatComponent* Combatant);

    int32 GetActiveTokenCount() const { return Policy.ActiveHolders(); }

private:
    void SynchronizeRoster();

    UPROPERTY(Transient)
    TArray<TWeakObjectPtr<UTDDCombatComponent>> RegisteredEnemies;

    TDD::AI::FTDDAttackTokenPolicy Policy = TDD::AI::FTDDAttackTokenPolicy(TDD::AI::FTDDTokenPolicySettings{});
};
