#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "TDDGameMode.generated.h"

/** Canonical game mode wires the first playable player controller and pawn. */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    ATDDGameMode();
};
