#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Engine/Engine.h"
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
        PC->Possess(Player);
        TestTrue(TEXT("Player controller possesses the character"), PC->GetPawn() == Player);

        // Beyond the upper bound -> the character's Tick clamps to the maximum.
        PC->SetControlRotation(FRotator(90.0f, 0.0f, 0.0f));
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: pre-tick control=(%.2f,%.2f,%.2f) pawn=%d ctrl=%d"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll,
            PC->GetPawn() != nullptr, Player->GetController() == PC);
        World->Tick(LEVELTICK_All, 0.016f);
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: post-tick control=(%.2f,%.2f,%.2f)"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll);
        TestTrue(TEXT("Over-the-head pitch is clamped to the maximum"),
                 FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MaxCameraPitchDeg, 0.01f));

        // Below the lower bound -> clamped to the minimum.
        PC->SetControlRotation(FRotator(-90.0f, 0.0f, 0.0f));
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: pre-tick control=(%.2f,%.2f,%.2f) pawn=%d ctrl=%d"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll,
            PC->GetPawn() != nullptr, Player->GetController() == PC);
        World->Tick(LEVELTICK_All, 0.016f);
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: post-tick control=(%.2f,%.2f,%.2f)"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll);
        TestTrue(TEXT("Below-the-feet pitch is clamped to the minimum"),
                 FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MinCameraPitchDeg, 0.01f));

        // Within the range -> untouched.
        PC->SetControlRotation(FRotator(10.0f, 45.0f, 0.0f));
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: pre-tick control=(%.2f,%.2f,%.2f) pawn=%d ctrl=%d"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll,
            PC->GetPawn() != nullptr, Player->GetController() == PC);
        World->Tick(LEVELTICK_All, 0.016f);
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: post-tick control=(%.2f,%.2f,%.2f)"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll);
        TestTrue(TEXT("In-range pitch and yaw are preserved"),
                 FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, 10.0f, 0.01f) &&
                 FMath::IsNearlyEqual(PC->GetControlRotation().Yaw, 45.0f, 0.01f));

        // Exact lower boundary -> preserved, never over-clamped.
        PC->SetControlRotation(FRotator(MinCameraPitchDeg, 0.0f, 0.0f));
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: pre-tick control=(%.2f,%.2f,%.2f) pawn=%d ctrl=%d"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll,
            PC->GetPawn() != nullptr, Player->GetController() == PC);
        World->Tick(LEVELTICK_All, 0.016f);
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: post-tick control=(%.2f,%.2f,%.2f)"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll);
        TestTrue(TEXT("Exact lower-bound pitch is preserved"),
                 FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MinCameraPitchDeg, 0.01f));

        // Exact upper boundary -> preserved, never over-clamped.
        PC->SetControlRotation(FRotator(MaxCameraPitchDeg, 0.0f, 0.0f));
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: pre-tick control=(%.2f,%.2f,%.2f) pawn=%d ctrl=%d"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll,
            PC->GetPawn() != nullptr, Player->GetController() == PC);
        World->Tick(LEVELTICK_All, 0.016f);
        UE_LOG(LogTemp, Log, TEXT("TDD-CAM: post-tick control=(%.2f,%.2f,%.2f)"),
            PC->GetControlRotation().Pitch, PC->GetControlRotation().Yaw, PC->GetControlRotation().Roll);
        TestTrue(TEXT("Exact upper-bound pitch is preserved"),
                 FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MaxCameraPitchDeg, 0.01f));
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
