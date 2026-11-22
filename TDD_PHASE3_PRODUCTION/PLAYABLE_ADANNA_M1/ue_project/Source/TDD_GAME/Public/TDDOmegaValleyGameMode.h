// TDDOmegaValleyGameMode.h — Phase 1 Ọmà-valley core game mode.
// Wires the world subsystems (location registry, population, calendar, market,
// weather), spawns the valley level, and on each market-day change refreshes the
// settlements so population, market stalls and weather consequences track the
// calendar. Reuses the playable proxy character.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "TDDWorldLogic.h"
#include "TDDOmegaValleyGameMode.generated.h"

class ATDDOmegaValleyLevel;

UCLASS()
class TDD_GAME_API ATDDOmegaValleyGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ATDDOmegaValleyGameMode();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

protected:
    void EnsureLevelSpawned();
    void RefreshWorldForCurrentDay();

    UPROPERTY(Transient)
    ATDDOmegaValleyLevel* ValleyLevel;

    EMarketDay LastMarketDay = EMarketDay::Eke;
    bool bHasWarned = false;
};
