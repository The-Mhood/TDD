#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "AI/TDDTrainingEnemy.h"
#include "Combat/TDDCombatComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Player/TDDAdannaCharacter.h"
#include "TDDGameMode.h"

/**
 * Greybox encounter flow: roster collection, activation, victory on enemy
 * defeat, defeat on player death, and restart (manual + timed auto-restart).
 * Drives a real created world so the GameMode sees actual actors.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1GameModeEncounterFlowTest,
    "TDD.M1.GameMode.EncounterFlow",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDM1GameModeEncounterFlowTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, /*bInformEngineOfWorld=*/false,
        TEXT("TDDEncounterFlow"), GetTransientPackage());
    TestNotNull(TEXT("Encounter test world created"), World);
    if (World == nullptr)
    {
        return false;
    }

    // A world from UWorld::CreateWorld is not playable until it is
    // registered with the engine and initialized for play. Without the
    // engine world context the world has no playable level: TActorIterator
    // enumeration yields no actors, spawned actors never receive BeginPlay
    // (so combat health is never initialised), and world-context lookups
    // fail with "WorldContext requested with invalid context object.".
    // This mirrors the canonical test-world fixture pattern.
    FWorldContext& WorldContext = GEngine->CreateNewWorldContext(EWorldType::Game);
    WorldContext.SetCurrentWorld(World);
    World->InitializeActorsForPlay(FURL());
    if (IsValid(World->GetWorldSettings()))
    {
        // The world has no GameMode, so begin-play dispatch is performed
        // manually; this also marks the world as begun so the actors spawned
        // below receive BeginPlay when they are spawned.
        World->GetWorldSettings()->NotifyBeginPlay();
        World->GetWorldSettings()->NotifyMatchStarted();
    }

    // UE 5.8.4: UWorld has no public assignable GameMode property (the
    // instance member AuthorityGameMode is protected and is set through
    // UWorld::SetGameMode(FURL) via a GameInstance). The GameMode is
    // therefore spawned as a real world actor via UWorld::SpawnActor (the
    // templated zero-argument overload SpawnActor(const FActorSpawnParameters&)
    // is valid). NewObject would only set the outer and never spawn the
    // actor: BeginPlay would not fire, roster collection would see no
    // world, and GameMode->GetWorld() would not be the test world — the
    // demonstrated D-W1D8-017 failure (gameModeWorldMatch=0).
    //
    // Spawn order matters: ATDDGameMode::BeginPlay collects the encounter
    // roster from the world, and an actor spawned into a world that has
    // already begun play receives BeginPlay at spawn time. The enemy,
    // player, controller and PlayerStart are therefore placed first and the
    // GameMode is spawned last, so its BeginPlay sees the complete actor
    // set. AActor::BeginPlay is protected, so it is not called directly.
    ATDDTrainingEnemy* Enemy = World->SpawnActor<ATDDTrainingEnemy>(FVector(0.0f, 600.0f, 100.0f), FRotator::ZeroRotator);
    TestNotNull(TEXT("Training enemy spawned in the test world"), Enemy);
    ATDDAdannaCharacter* Player = World->SpawnActor<ATDDAdannaCharacter>(FVector(0.0f, -600.0f, 100.0f), FRotator::ZeroRotator);
    TestNotNull(TEXT("Player character spawned in the test world"), Player);
    APlayerController* PC = World->SpawnActor<APlayerController>();
    TestNotNull(TEXT("Player controller spawned in the test world"), PC);
    if (PC != nullptr && Player != nullptr)
    {
        PC->Possess(Player);
    }
    TestTrue(TEXT("Player controller possesses the player before evaluation"),
             PC != nullptr && Player != nullptr && PC->GetPawn() == Player);
    APlayerStart* PlayerStart = World->SpawnActor<APlayerStart>(FVector(100.0f, 0.0f, 100.0f), FRotator::ZeroRotator);
    TestNotNull(TEXT("Player start placed in the test world"), PlayerStart);

    // Spawn the GameMode last: its BeginPlay runs at spawn and collects
    // the encounter roster from the fully populated world.
    ATDDGameMode* GameMode = World->SpawnActor<ATDDGameMode>();
    TestNotNull(TEXT("GameMode spawned into the test world"), GameMode);
    TestTrue(TEXT("Spawned GameMode belongs to the test world"),
             GameMode != nullptr && GameMode->GetWorld() == World);

    if (GameMode != nullptr)
    {
        GameMode->CollectEncounterActors();
        TestEqual(TEXT("Encounter roster collects the placed enemy"), GameMode->GetEncounterEnemiesRemaining(), 1);

        GameMode->EvaluateEncounter(0.016f);
        TestTrue(TEXT("Encounter activates once a player exists"),
                 GameMode->GetEncounterState() == ETDDEncounterState::Active);

        // Victory path: defeat the only rostered enemy.
        if (Enemy != nullptr)
        {
            UTDDCombatComponent* EnemyCombat = Enemy->GetCombatComponent();
            TestNotNull(TEXT("Training enemy has a combat component"), EnemyCombat);
            if (EnemyCombat != nullptr)
            {
                EnemyCombat->ReceiveAttack(EnemyCombat->GetHealth() + 10.0f, 0.0f, false, nullptr);
            }
        }
        GameMode->EvaluateEncounter(0.016f);
        TestTrue(TEXT("Defeating every rostered enemy yields victory"),
                 GameMode->GetEncounterState() == ETDDEncounterState::Victory);

        // Manual restart restores the encounter.
        GameMode->RestartEncounter();
        TestTrue(TEXT("Restart returns the encounter to active"),
                 GameMode->GetEncounterState() == ETDDEncounterState::Active);
        TestEqual(TEXT("Restart restores the enemy to the roster"), GameMode->GetEncounterEnemiesRemaining(), 1);
        if (Enemy != nullptr)
        {
            UTDDCombatComponent* EnemyCombat = Enemy->GetCombatComponent();
            TestTrue(TEXT("Restart restores the enemy's health"),
                     EnemyCombat != nullptr && !EnemyCombat->IsDead());
        }

        // The PlayerStart query (ResetPlayerForRestart) must find the placed
        // start and reposition the pawn — covers the second AllActors iterator.
        TestTrue(TEXT("Restart repositions the player to the level PlayerStart"),
                 PlayerStart != nullptr && Player != nullptr &&
                 FVector::Dist(Player->GetActorLocation(), PlayerStart->GetActorLocation()) < 1.0f);

        // Defeat path: the player dies, and the configured delay auto-restarts.
        if (Player != nullptr)
        {
            UTDDCombatComponent* PlayerCombat = Player->GetCombatComponent();
            TestNotNull(TEXT("Player has a combat component"), PlayerCombat);
            if (PlayerCombat != nullptr)
            {
                PlayerCombat->ReceiveAttack(PlayerCombat->GetHealth() + 10.0f, 0.0f, false, nullptr);
            }
        }
        GameMode->EvaluateEncounter(0.016f);
        TestTrue(TEXT("Player death yields defeat"),
                 GameMode->GetEncounterState() == ETDDEncounterState::Defeat);

        const float Step = 0.02f;
        int32 Steps = 0;
        while (Steps < 500 && GameMode->GetEncounterState() == ETDDEncounterState::Defeat)
        {
            GameMode->EvaluateEncounter(Step);
            ++Steps;
        }
        TestTrue(TEXT("Defeat auto-restarts after the configured delay"),
                 GameMode->GetEncounterState() == ETDDEncounterState::Active);
    }

    // Teardown: release the engine context and destroy the test world so
    // repeated runs do not leak worlds. The iterator passes explicit
    // AllActors flags (D-W1D8-015): the default OnlyActiveLevels gating
    // yields no actors on this created world, so the default flags would
    // skip every spawned actor. The assertion macros record failures
    // without aborting, so this teardown always runs even when an
    // assertion above failed.
    World->BeginTearingDown();
    for (TActorIterator<AActor> It(World, AActor::StaticClass(), EActorIteratorFlags::AllActors); It; ++It)
    {
        It->Destroy();
    }
    GEngine->DestroyWorldContext(World);
    World->DestroyWorld(false);

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
