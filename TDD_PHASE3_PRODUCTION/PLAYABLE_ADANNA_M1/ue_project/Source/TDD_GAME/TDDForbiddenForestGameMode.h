#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "TDDForbiddenForestGameMode.generated.h"

UCLASS()
class TDD_GAME_API ATDDForbiddenForestGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ATDDForbiddenForestGameMode();
    virtual void StartPlay() override;
};
