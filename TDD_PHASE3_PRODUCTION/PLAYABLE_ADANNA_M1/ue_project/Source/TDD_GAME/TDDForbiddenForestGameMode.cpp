#include "TDDForbiddenForestGameMode.h"

#include "TDDAdannaProxyCharacter.h"
#include "TDDForbiddenForestLevel.h"
#include "Engine/World.h"
#include "EngineUtils.h"

ATDDForbiddenForestGameMode::ATDDForbiddenForestGameMode()
{
    DefaultPawnClass = ATDDAdannaProxyCharacter::StaticClass();
}

void ATDDForbiddenForestGameMode::StartPlay()
{
    if (UWorld* World = GetWorld())
    {
        bool bLevelAlreadyPresent = false;
        for (TActorIterator<ATDDForbiddenForestLevel> It(World); It; ++It)
        {
            bLevelAlreadyPresent = true;
            break;
        }
        if (!bLevelAlreadyPresent)
        {
            FActorSpawnParameters SpawnInfo;
            SpawnInfo.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
            World->SpawnActor<ATDDForbiddenForestLevel>(
                ATDDForbiddenForestLevel::StaticClass(),
                FVector::ZeroVector,
                FRotator::ZeroRotator,
                SpawnInfo);
        }
    }
    Super::StartPlay();
}
