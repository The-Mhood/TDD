#include "Player/TDDPlayerController.h"

void ATDDPlayerController::BeginPlay()
{
    Super::BeginPlay();

    bShowMouseCursor = false;
    bEnableClickEvents = false;
    bEnableMouseOverEvents = false;
    SetInputMode(FInputModeGameOnly());
}
