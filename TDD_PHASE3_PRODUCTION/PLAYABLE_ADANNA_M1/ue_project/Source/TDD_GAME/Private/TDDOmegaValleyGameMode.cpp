// TDDOmegaValleyGameMode.cpp — Phase 1 Ọmà-valley core game mode.
#include "TDDOmegaValleyGameMode.h"

#include "TDDAdannaProxyCharacter.h"
#include "TDDOmegaValleyLevel.h"
#include "TDDCalendarSubsystem.h"
#include "TDDWeatherSubsystem.h"
#include "TDDWorldPopulationSubsystem.h"
#include "TDDMarketSubsystem.h"
#include "Engine/World.h"
#include "EngineUtils.h"

ATDDOmegaValleyGameMode::ATDDOmegaValleyGameMode()
{
    DefaultPawnClass = ATDDAdannaProxyCharacter::StaticClass();
    ValleyLevel = nullptr;
}

void ATDDOmegaValleyGameMode::BeginPlay()
{
    Super::BeginPlay();
    EnsureLevelSpawned();
    RefreshWorldForCurrentDay();
}

void ATDDOmegaValleyGameMode::EnsureLevelSpawned()
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }
    if (ValleyLevel)
    {
        return;
    }
    // TActorIterator's UE 5.8 constructor is (World, Class, Flags); the iterator's
    // operator bool reports whether a suitable actor exists and operator* returns it.
    // The iterator is declared on its own line: a variable declaration inside an
    // `if` condition cannot have a parenthesized initializer (Clang error).
    TActorIterator<ATDDOmegaValleyLevel> ValleyIt(
        World, ATDDOmegaValleyLevel::StaticClass(), EActorIteratorFlags::AllActors);
    if (ValleyIt)
    {
        ValleyLevel = *ValleyIt;
    }
    if (!ValleyLevel)
    {
        FActorSpawnParameters SpawnInfo;
        SpawnInfo.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
        ValleyLevel = World->SpawnActor<ATDDOmegaValleyLevel>(
            ATDDOmegaValleyLevel::StaticClass(),
            FVector::ZeroVector,
            FRotator::ZeroRotator,
            SpawnInfo);
    }
}

void ATDDOmegaValleyGameMode::RefreshWorldForCurrentDay()
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    const UTDDCalendarSubsystem* Calendar = World->GetSubsystem<UTDDCalendarSubsystem>();
    const int64 WorldDay = Calendar ? Calendar->GetWorldDay() : 0;
    const float TimeOfDay = 0.25f;

    // Weather consequences track the calendar.
    if (UTDDWeatherSubsystem* Weather = World->GetSubsystem<UTDDWeatherSubsystem>())
    {
        Weather->UpdateFromWorldDay(WorldDay);
    }

    // Refresh settlements when the market day changes.
    const EMarketDay Today = TDDWorld::MarketDayFromDay(WorldDay);
    if (ValleyLevel && Today != LastMarketDay)
    {
        ValleyLevel->RefreshSettlements(WorldDay, TimeOfDay);
        LastMarketDay = Today;
    }

    // Log the population/weather state so playable evidence is observable.
    if (UTDDWorldPopulationSubsystem* Population = World->GetSubsystem<UTDDWorldPopulationSubsystem>())
    {
        if (!bHasWarned)
        {
            UE_LOG(LogTemp, Display,
                   TEXT("TDD ValleyGameMode: logical population %d (rendered subset is budgeted per settlement). "
                        "Market today = %s, season = %s."),
                   Population->GetRegionalLogicalPopulation(),
                   *FString(TDDWorld::MarketDayName(Today)),
                   *FString(TDDWorld::SeasonName(TDDWorld::SeasonForDay(WorldDay))));
            bHasWarned = true;
        }
    }
}

void ATDDOmegaValleyGameMode::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    RefreshWorldForCurrentDay();
}
