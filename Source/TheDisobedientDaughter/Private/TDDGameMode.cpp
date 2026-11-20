#include "TDDGameMode.h"

#include "Player/TDDAdannaCharacter.h"
#include "Player/TDDPlayerController.h"

ATDDGameMode::ATDDGameMode()
{
    DefaultPawnClass = ATDDAdannaCharacter::StaticClass();
    PlayerControllerClass = ATDDPlayerController::StaticClass();
}
