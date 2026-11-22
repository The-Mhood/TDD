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
        // Presence test only: the iterator is positioned on the first match at
        // construction. A `for` that broke immediately made `++It` unreachable, which
        // V7 reports as -Werror,-Wunreachable-code-loop-increment.
        // TActorIterator's UE 5.8 constructor is (World, Class, Flags); the iterator's
        // operator bool reports whether a suitable actor exists.
        const bool bLevelAlreadyPresent =
            static_cast<bool>(TActorIterator<ATDDForbiddenForestLevel>(
                World, ATDDForbiddenForestLevel::StaticClass(), EActorIteratorFlags::AllActors));
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
