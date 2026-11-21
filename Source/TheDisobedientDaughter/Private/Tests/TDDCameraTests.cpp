#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "Player/TDDAdannaCharacter.h"

/**
 * Third-person camera control side: the controller pitch is clamped to the
 * declared camera range so the spring-arm camera cannot flip over the head
 * (M1 spec S5, AC-14..18 control prerequisite).
 *
 * Test seam: the character's own Tick performs the clamp on the possessing
 * controller's control rotation, and the character enables
 * PrimaryActorTick.bCanEverTick in its constructor. The genuine UE 5.8.4
 * mechanism to advance that lifecycle is the world tick (UWorld::Tick is
 * public; the engine calls it every frame) — the clamp runs inside it.
 * The declared range is mirrored here from the production contract rather
 * than read from protected accessors, so production encapsulation is intact.
 *
 * D-W1D8-024 root cause: the APlayerController must own a Player for its tick
 * lifecycle to be valid. Possession (AController::SetPawn ->
 * AddPawnTickDependency) makes the pawn's PrimaryActorTick depend on the
 * controller's TickActor; a controller with no Player has an incomplete tick
 * lifecycle on UE 5.8.4, so its TickActor (and therefore the pawn's Tick and
 * the clamp) only ran on the first world tick. The controller is given a
 * ULocalPlayer via SetPlayer (SetAsLocalPlayerController + InitInputSystem)
 * before possession so its TickActor runs every tick and the clamp executes
 * for every case. The character's TickCount / ClampExecutionCount counters
 * are asserted before/after each tick so the test proves the clamp actually
 * executed (cases 3-6 cannot pass merely because the clamp never ran).
 *
 * The test world is registered with the engine (D-W1D8-020): UWorld::Tick
 * reaches UWorld::IsInSeamlessTravel -> UEngine::SeamlessTravelHandlerForWorld
 * -> UEngine::GetWorldContextFromWorldChecked, which crashes without a
 * registered engine world context.
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1CameraPitchClampTest,
    "TDD.M1.Player.CameraPitchClamp",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

namespace
{
// Declared third-person camera pitch range (degrees), mirroring the
// production clamp contract on ATDDAdannaCharacter (private static constexpr).
constexpr float MinCameraPitchDeg = -55.0f;
constexpr float MaxCameraPitchDeg = 25.0f;
}

bool FTDDM1CameraPitchClampTest::RunTest(const FString& Parameters)
{
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, /*bInformEngineOfWorld=*/false,
        TEXT("TDDCameraPitchClamp"), GetTransientPackage());
    TestNotNull(TEXT("Camera test world created"), World);
    if (World == nullptr)
    {
        return false;
    }

    // Register the test world with the engine using the proven world-context
    // fixture: UWorld::CreateWorld with bInformEngineOfWorld=false leaves the
    // world unregistered, so UWorld::Tick crashes in
    // UEngine::GetWorldContextFromWorldChecked() via IsInSeamlessTravel.
    FWorldContext& WorldContext = GEngine->CreateNewWorldContext(EWorldType::Game);
    WorldContext.SetCurrentWorld(World);
    World->InitializeActorsForPlay(FURL());
    if (IsValid(World->GetWorldSettings()))
    {
        // Mark the world as begun so the spawned actors receive BeginPlay.
        World->GetWorldSettings()->NotifyBeginPlay();
        World->GetWorldSettings()->NotifyMatchStarted();
    }

    // The engine world context must exist and resolve to the exact test world.
    FWorldContext* Context = GEngine->GetWorldContextFromWorld(World);
    TestTrue(TEXT("Test world has a registered engine world context"), Context != nullptr);
    TestTrue(TEXT("World context resolves to the exact test world"),
             Context != nullptr && Context->World() == World);

    ATDDAdannaCharacter* Player = World->SpawnActor<ATDDAdannaCharacter>(FVector::ZeroVector, FRotator::ZeroRotator);
    TestNotNull(TEXT("Player character spawned in the test world"), Player);
    APlayerController* PC = World->SpawnActor<APlayerController>();
    TestNotNull(TEXT("Player controller spawned in the test world"), PC);

    TestTrue(TEXT("Camera pitch range is declared"), MaxCameraPitchDeg > MinCameraPitchDeg);

    if (Player != nullptr && PC != nullptr)
    {
        // D-W1D8-024 fix: the APlayerController must own a Player for its tick
        // lifecycle to be valid on UE 5.8.4. Possession makes the pawn's tick
        // depend on the controller's TickActor (AController::AddPawnTickDependency);
        // without a Player the controller's TickActor did not run past the first
        // world tick, so the pawn's Tick (and the clamp) ran only once. Giving
        // the controller a ULocalPlayer (SetPlayer -> SetAsLocalPlayerController
        // + InitInputSystem) before possession makes the controller tick every
        // tick, so the clamp executes for every case below.
        // UE 5.8.4 lifecycle: a ULocalPlayer MUST be created through the
        // engine-supported UGameInstance::CreateLocalPlayer path so it gets a
        // valid Engine Outer (NewObject<ULocalPlayer>(GetEngine(), ...)) and is
        // registered with a game instance.  Constructing it via NewObject with
        // the transient package triggers "Object None of class
        // /Script/Engine.LocalPlayer ... was created in invalid Outer
        // /Script/CoreUObject.Package!" and the resulting controller/pawn
        // association is invalid, so the character's Tick does not run.
        //
        // A UWorld::CreateWorld test world may not own a UGameInstance, so bind
        // a default UGameInstance to this world with the engine as the (valid)
        // Outer, then create the local player through it with
        // bSpawnPlayerController=false (the test spawns its own APlayerController).
        // This satisfies the required order: valid Engine Outer -> player
        // created -> associated with the controller -> input init ->
        // possession -> pawn tick dependency, all headless with no real
        // viewport or user input.
        UGameInstance* GameInstance = World->GetGameInstance();
        if (GameInstance == nullptr)
        {
            // UGameInstance::GetEngine() returns CastChecked<UEngine>(GetOuter())
            // (GameInstance.cpp), so the game instance's Outer MUST be the engine.
            // GEngine is the global UEngine* (Engine/Engine.h). This is also the
            // valid Outer that CreateLocalPlayer gives the ULocalPlayer internally
            // (NewObject<ULocalPlayer>(GetEngine(), GetEngine()->LocalPlayerClass)).
            GameInstance = NewObject<UGameInstance>(GEngine);
            World->SetGameInstance(GameInstance);
            // SetGameInstance only sets World->OwningGameInstance; it does not bind
            // the game instance's world context. Bind it to this test world through
            // the engine's public OnWorldChanged callback, which explicitly handles
            // test/preview worlds that had no world context set before, so the game
            // instance's GetWorld() resolves to the test world.
            GameInstance->OnWorldChanged(nullptr, World);
        }

        FString PlayerError;
        ULocalPlayer* LocalPlayer = GameInstance->CreateLocalPlayer(0, PlayerError, false);
        TestNotNull(TEXT("Local player created for the test controller"), LocalPlayer);
        if (LocalPlayer != nullptr)
        {
            PC->SetPlayer(LocalPlayer);
        }
        TestTrue(TEXT("Player controller has a player assigned"), PC->Player != nullptr);

        PC->Possess(Player);
        TestTrue(TEXT("Player controller possesses the character"), PC->GetPawn() == Player);

        // Each case records the character's TickCount / ClampExecutionCount
        // before its tick and asserts both advanced after it, proving the
        // character ticked and the clamp executed for that case (so in-range
        // and boundary cases cannot pass merely because the clamp never ran).

        // Beyond the upper bound -> the character's Tick clamps to the maximum.
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(90.0f, 0.0f, 0.0f));
            World->Tick(LEVELTICK_All, 0.016f);
            TestTrue(TEXT("Over-the-head: character ticked"),
                     Player->GetTickCount() > TickBefore);
            TestTrue(TEXT("Over-the-head: clamp executed"),
                     Player->GetClampExecutionCount() > ClampBefore);
            TestTrue(TEXT("Over-the-head pitch is clamped to the maximum"),
                     FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MaxCameraPitchDeg, 0.01f));
        }

        // Below the lower bound -> clamped to the minimum.
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(-90.0f, 0.0f, 0.0f));
            World->Tick(LEVELTICK_All, 0.016f);
            TestTrue(TEXT("Below-the-feet: character ticked"),
                     Player->GetTickCount() > TickBefore);
            TestTrue(TEXT("Below-the-feet: clamp executed"),
                     Player->GetClampExecutionCount() > ClampBefore);
            TestTrue(TEXT("Below-the-feet pitch is clamped to the minimum"),
                     FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MinCameraPitchDeg, 0.01f));
        }

        // Within the range -> untouched (clamp still executes, value unchanged).
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(10.0f, 45.0f, 0.0f));
            World->Tick(LEVELTICK_All, 0.016f);
            TestTrue(TEXT("In-range: character ticked"),
                     Player->GetTickCount() > TickBefore);
            TestTrue(TEXT("In-range: clamp executed"),
                     Player->GetClampExecutionCount() > ClampBefore);
            TestTrue(TEXT("In-range pitch and yaw are preserved"),
                     FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, 10.0f, 0.01f) &&
                     FMath::IsNearlyEqual(PC->GetControlRotation().Yaw, 45.0f, 0.01f));
        }

        // Exact lower boundary -> preserved, never over-clamped (clamp executes).
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(MinCameraPitchDeg, 0.0f, 0.0f));
            World->Tick(LEVELTICK_All, 0.016f);
            TestTrue(TEXT("Lower-bound: character ticked"),
                     Player->GetTickCount() > TickBefore);
            TestTrue(TEXT("Lower-bound: clamp executed"),
                     Player->GetClampExecutionCount() > ClampBefore);
            TestTrue(TEXT("Exact lower-bound pitch is preserved"),
                     FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MinCameraPitchDeg, 0.01f));
        }

        // Exact upper boundary -> preserved, never over-clamped (clamp executes).
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(MaxCameraPitchDeg, 0.0f, 0.0f));
            World->Tick(LEVELTICK_All, 0.016f);
            TestTrue(TEXT("Upper-bound: character ticked"),
                     Player->GetTickCount() > TickBefore);
            TestTrue(TEXT("Upper-bound: clamp executed"),
                     Player->GetClampExecutionCount() > ClampBefore);
            TestTrue(TEXT("Exact upper-bound pitch is preserved"),
                     FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MaxCameraPitchDeg, 0.01f));
        }
    }

    // Teardown: UWorld::EndPlay performs the begin/end-play handshake itself
    // (verified in the engine source: it calls BeginTearingDown internally,
    // so calling BeginTearingDown again after EndPlay logs "BeginTearingDown
    // called twice"), routes EndPlay to the world's actors and clears the
    // begun-play state so CleanupWorld does not warn "missing call to
    // EndPlay". Then destroy the world's actors and the world, and release
    // the engine world context (order matches the proven fixture).
    TestTrue(TEXT("World EndPlay completes the teardown handshake"),
             World->EndPlay(EEndPlayReason::Destroyed));
    for (TActorIterator<AActor> It(World, AActor::StaticClass(), EActorIteratorFlags::AllActors); It; ++It)
    {
        It->Destroy();
    }
    GEngine->DestroyWorldContext(World);
    World->DestroyWorld(false);

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
