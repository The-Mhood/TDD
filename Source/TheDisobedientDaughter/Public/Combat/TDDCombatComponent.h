#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "TDDCombatComponent.generated.h"

namespace TDD
{
namespace Combat
{
struct FTDDDamageOutcome;
}
}

class UTDDCharacterStateComponent;

/** Minimal actor-facing combat surface: one light strike, guard/parry, health and posture. */
UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class THEDISOBEDIENTDAUGHTER_API UTDDCombatComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTDDCombatComponent();

    UFUNCTION(BlueprintCallable, Category="TDD|Combat")
    bool PerformLightAttack();

    UFUNCTION(BlueprintCallable, Category="TDD|Combat")
    bool SetGuarding(bool bGuarding);

    UFUNCTION(BlueprintCallable, Category="TDD|Combat")
    float GetHealth() const { return Health; }

    UFUNCTION(BlueprintCallable, Category="TDD|Combat")
    float GetPosture() const { return Posture; }

    UFUNCTION(BlueprintCallable, Category="TDD|Combat")
    bool IsDead() const { return Health <= 0.0f; }

    /** Apply one attack request; returns false when a parry completely negates it. */
    bool ReceiveAttack(float HealthDamage, float PostureDamage, bool bCausesStagger,
                       UTDDCombatComponent* Attacker);

    void ReceiveSuccessfulParry();

protected:
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Combat", meta=(ClampMin="1.0"))
    float MaxHealth = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Combat", meta=(ClampMin="1.0"))
    float MaxPosture = 100.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Combat", meta=(ClampMin="1.0"))
    float LightAttackRange = 180.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Combat", meta=(ClampMin="0.0"))
    float LightHealthDamage = 12.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Combat", meta=(ClampMin="0.0"))
    float LightPostureDamage = 18.0f;

private:
    void ApplyOutcome(const TDD::Combat::FTDDDamageOutcome& Outcome);
    UTDDCharacterStateComponent* FindStateComponent() const;

    float Health = 100.0f;
    float Posture = 0.0f;
    float GuardStartedAt = -1.0f;
    bool bGuarding = false;
    bool bGuardReleasePending = false;
};
