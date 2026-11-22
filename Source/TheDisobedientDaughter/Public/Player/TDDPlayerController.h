#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerController.h"
#include "TDDPlayerController.generated.h"

/** Local, game-only controller setup for the first playable character. */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDPlayerController : public APlayerController
{
    GENERATED_BODY()

protected:
    virtual void BeginPlay() override;
};
