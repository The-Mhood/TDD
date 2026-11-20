#include "TDDGameMode.h"

#include "AI/TDDTrainingEnemy.h"
#include "Combat/TDDCombatComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Kismet/GameplayStatics.h"
#include "Player/TDDAdannaCharacter.h"
#include "Player/TDDCharacterStateComponent.h"
#include "Player/TDDPlayerController.h"

namespace
{
// Unique to this translation unit: a plain anonymous-namespace identifier
// collides with the same name in TDDCombatComponent.cpp under Unreal's
// Unity compilation (merged translation units), so it is qualified here.
constexpr int32 TDDGameModeStateIdle = static_cast<int32>(TDD::State::ETDDPlayerState::Idle);
}

ATDDGameMode::ATDDGameMode()
{
    DefaultPawnClass = ATDDAdannaCharacter::StaticClass();
    PlayerControllerClass = ATDDPlayerController::StaticClass();
}

void ATDDGameMode::BeginPlay()
{
    Super::BeginPlay();
    CollectEncounterActors();
}

void ATDDGameMode::PostLogin(APlayerController* NewPlayer)
{
    Super::PostLogin(NewPlayer);
    if (EncounterState == ETDDEncounterState::NotStarted)
    {
        EncounterState = ETDDEncounterState::Active;
        UE_LOG(LogTemp, Log, TEXT("TDD encounter: active with %d rostered enemies"), EncounterEnemies.Num());
    }
}

void ATDDGameMode::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    EvaluateEncounter(DeltaSeconds);
}

void ATDDGameMode::CollectEncounterActors()
{
    EncounterEnemies.Reset();
    EncounterSpawnLocations.Reset();
    UWorld* World = GetWorld();
    if (World == nullptr)
    {
        return;
    }
    // UE 5.8.4: UWorld has no GetAllActorsOfClass member; the supported
    // actor-query mechanism is TActorIterator (EngineUtils.h).
    for (TActorIterator<ATDDTrainingEnemy> It(World); It; ++It)
    {
        ATDDTrainingEnemy* Enemy = *It;
        if (Enemy == nullptr)
        {
            continue;
        }
        EncounterEnemies.Add(Enemy);
        EncounterSpawnLocations.Add(Enemy->GetActorLocation());
    }
}

int32 ATDDGameMode::GetEncounterEnemiesRemaining() const
{
    int32 Remaining = 0;
    for (const TWeakObjectPtr<ATDDTrainingEnemy>& Weak : EncounterEnemies)
    {
        ATDDTrainingEnemy* Enemy = Weak.Get();
        if (Enemy == nullptr)
        {
            continue;
        }
        UTDDCombatComponent* Combat = Enemy->FindComponentByClass<UTDDCombatComponent>();
        if (Combat == nullptr || !Combat->IsDead())
        {
            ++Remaining;
        }
    }
    return Remaining;
}

void ATDDGameMode::EvaluateEncounter(float DeltaSeconds)
{
    UWorld* World = GetWorld();
    if (World == nullptr)
    {
        return;
    }

    // Lazy activation when a player exists but PostLogin was not routed
    // (e.g. a world created without the full login flow).
    if (EncounterState == ETDDEncounterState::NotStarted)
    {
        APlayerController* PC = World->GetFirstPlayerController();
        if (PC != nullptr && PC->GetPawn() != nullptr)
        {
            EncounterState = ETDDEncounterState::Active;
        }
    }

    if (EncounterState == ETDDEncounterState::Defeat)
    {
        DefeatTimer += DeltaSeconds;
        if (DefeatTimer >= DefeatRestartDelay)
        {
            RestartEncounter();
        }
        return;
    }

    if (EncounterState != ETDDEncounterState::Active)
    {
        return;
    }

    // Defeat: the player pawn's combat health is exhausted.
    APlayerController* PC = World->GetFirstPlayerController();
    APawn* PlayerPawn = (PC != nullptr) ? PC->GetPawn() : nullptr;
    if (PlayerPawn != nullptr)
    {
        UTDDCombatComponent* PlayerCombat = PlayerPawn->FindComponentByClass<UTDDCombatComponent>();
        if (PlayerCombat != nullptr && PlayerCombat->IsDead())
        {
            EncounterState = ETDDEncounterState::Defeat;
            DefeatTimer = 0.0f;
            UE_LOG(LogTemp, Log, TEXT("TDD encounter: player defeated"));
            return;
        }
    }

    // Victory: every rostered enemy is defeated (an empty roster stays Active).
    if (EncounterEnemies.Num() > 0 && GetEncounterEnemiesRemaining() == 0)
    {
        EncounterState = ETDDEncounterState::Victory;
        UE_LOG(LogTemp, Log, TEXT("TDD encounter: victory"));
    }
}

void ATDDGameMode::RestartEncounter()
{
    UWorld* World = GetWorld();
    if (World == nullptr)
    {
        return;
    }
    ResetPlayerForRestart();
    ResetEnemiesForRestart();
    EncounterState = ETDDEncounterState::Active;
    DefeatTimer = 0.0f;
    UE_LOG(LogTemp, Log, TEXT("TDD encounter: restarted"));
}

void ATDDGameMode::ResetPlayerForRestart()
{
    UWorld* World = GetWorld();
    APlayerController* PC = (World != nullptr) ? World->GetFirstPlayerController() : nullptr;
    APawn* PlayerPawn = (PC != nullptr) ? PC->GetPawn() : nullptr;
    if (PlayerPawn == nullptr)
    {
        return;
    }
    UTDDCombatComponent* Combat = PlayerPawn->FindComponentByClass<UTDDCombatComponent>();
    if (Combat != nullptr)
    {
        Combat->ResetForRestart();
    }
    UTDDCharacterStateComponent* State = PlayerPawn->FindComponentByClass<UTDDCharacterStateComponent>();
    if (State != nullptr)
    {
        State->ForceState(TDDGameModeStateIdle);
    }
    // Return the pawn to the level's PlayerStart so restarts are repeatable.
    // UE 5.8.4: UWorld has no GetAllActorsOfClass member; the supported
    // actor-query mechanism is TActorIterator (EngineUtils.h).
    APlayerStart* FirstStart = nullptr;
    if (World != nullptr)
    {
        for (TActorIterator<APlayerStart> It(World); It; ++It)
        {
            FirstStart = *It;
            break;
        }
    }
    if (FirstStart != nullptr)
    {
        PlayerPawn->SetActorLocation(FirstStart->GetActorLocation());
        PlayerPawn->SetActorRotation(FirstStart->GetActorRotation());
    }
}

void ATDDGameMode::ResetEnemiesForRestart()
{
    for (int32 I = 0; I < EncounterEnemies.Num(); ++I)
    {
        ATDDTrainingEnemy* Enemy = EncounterEnemies[I].Get();
        if (Enemy == nullptr)
        {
            continue;
        }
        UTDDCombatComponent* Combat = Enemy->FindComponentByClass<UTDDCombatComponent>();
        if (Combat != nullptr)
        {
            Combat->ResetForRestart();
        }
        UTDDCharacterStateComponent* State = Enemy->FindComponentByClass<UTDDCharacterStateComponent>();
        if (State != nullptr)
        {
            State->ForceState(TDDGameModeStateIdle);
        }
        if (I < EncounterSpawnLocations.Num())
        {
            Enemy->SetActorLocation(EncounterSpawnLocations[I]);
        }
    }
}
