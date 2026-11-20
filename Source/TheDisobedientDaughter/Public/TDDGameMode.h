#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "TDDGameMode.generated.h"

class ACharacter;
class APawn;
class APlayerController;
class ATDDTrainingEnemy;

/**
 * Canonical game mode: first playable player controller and pawn, plus the
 * greybox encounter flow (active -> victory/defeat -> restart) that makes the
 * M1 candidate repeatedly playable.
 *
 * The encounter roster is collected from the world at BeginPlay: every
 * ATDDTrainingEnemy (the training enemy and its boss subclass) placed in the
 * level is one encounter opponent. Victory requires every rostered enemy to
 * be defeated; defeat is the player's death. Defeat auto-restarts after
 * DefeatRestartDelay, and RestartEncounter() can also be triggered by input.
 */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ATDDGameMode();

    enum class ETDDEncounterState : uint8
    {
        NotStarted,
        Active,
        Victory,
        Defeat
    };

    virtual void BeginPlay() override;
    virtual void PostLogin(APlayerController* NewPlayer) override;
    virtual void Tick(float DeltaSeconds) override;

    /** Evaluate the encounter from current world state; called by Tick and by tests. */
    void EvaluateEncounter(float DeltaSeconds);

    /** Reset the player and restore every rostered enemy; returns to Active. */
    void RestartEncounter();

    /** Collect the encounter roster (ATDDTrainingEnemy actors) from the world. */
    void CollectEncounterActors();

    ETDDEncounterState GetEncounterState() const { return EncounterState; }
    int32 GetEncounterEnemiesRemaining() const;

protected:
    void ResetPlayerForRestart();
    void ResetEnemiesForRestart();

private:
    UPROPERTY(Transient)
    ETDDEncounterState EncounterState = ETDDEncounterState::NotStarted;

    TArray<TWeakObjectPtr<ATDDTrainingEnemy>> EncounterEnemies;
    TArray<FVector> EncounterSpawnLocations;

    float DefeatTimer = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Encounter", meta=(ClampMin="0.0"))
    float DefeatRestartDelay = 3.0f;
};
