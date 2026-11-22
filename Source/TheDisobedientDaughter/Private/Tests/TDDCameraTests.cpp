#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "CoreGlobals.h"
#include "Engine/Engine.h"
#include "Engine/EngineBaseTypes.h"
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
 * D-W1D8-024 root cause (audit #3): the pawn's TickActor/Tick/ClampCameraPitch
 * runs on the first World::Tick then stops, because the fixture calls
 * UWorld::Tick synchronously several times within a single engine frame without
 * advancing the global GFrameCounter. The tick task manager's per-frame dedup
 * gate (FTickTaskSequencer::HasBeenVisited, keyed on GFrameCounter via
 * FTickFunction::TickVisitedGFrameCounter) queues a tick function only when
 * GFrameCounter has advanced since it last ran; with GFrameCounter frozen the
 * pawn's PrimaryActorTick is visited on tick 1 and never re-queued on ticks
 * 2-6. In gameplay the engine frame loop (FEngineLoop::Tick) increments
 * GFrameCounter once per frame before UWorld::Tick, so the gate is false every
 * frame and actors tick every frame. This fixture therefore advances
 * GFrameCounter before each World::Tick, exactly as the engine loop does.
 *
 * Possession (AController::SetPawn -> AddPawnTickDependency) also adds a tick
 * prerequisite making the pawn's PrimaryActorTick depend on the controller's
 * PrimaryActorTick (FTickFunction::AddPrerequisite, Controller.cpp). This
 * fixture keeps the real possession (so GetControlRotation() and the
 * controller/pawn lifecycle are genuine) and removes that tick prerequisite
 * (FTickFunction::RemovePrerequisite, the inverse of AddPawnTickDependency) so
 * the pawn's real Tick and the production clamp are not gated by the
 * controller. The character's TickCount / ClampExecutionCount counters are
 * asserted before/after each tick so the test proves the clamp actually
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
        // D-W1D8-024: possession (AController::SetPawn -> AddPawnTickDependency)
        // adds a tick prerequisite making the pawn's PrimaryActorTick depend on the
        // controller's PrimaryActorTick (FTickFunction::AddPrerequisite). In a real
        // game the controller's tick fires every frame (it owns a Player with a
        // viewport), so the prerequisite is satisfied and the pawn's Tick -- which
        // runs the production ClampCameraPitch -- executes every tick.
        //
        // A headless UWorld::CreateWorld automation fixture has no viewport and no
        // engine-managed local player. UGameInstance::CreateLocalPlayer is guarded by
        // `ensure(IsDedicatedServerInstance())` when there is no game viewport client
        // (GameInstance.cpp), so a standalone test cannot legitimately fabricate a
        // ULocalPlayer through that path (it fired "Ensure condition failed:
        // IsDedicatedServerInstance()" at GameInstance.cpp:856). Rather than replace
        // one invalid player lifecycle with another, this fixture keeps the real
        // possession (so GetControlRotation() and the controller/pawn lifecycle are
        // genuine) and removes the tick prerequisite that gates the pawn's Tick on
        // the controller's Tick.
        //
        // Audit #3: removing the prerequisite alone was insufficient -- the pawn
        // still ticked only on the first World::Tick. The actual blocker is that
        // UWorld::Tick does not advance the global GFrameCounter; the tick task
        // manager's per-frame dedup gate (HasBeenVisited, keyed on GFrameCounter)
        // therefore prevents the pawn's PrimaryActorTick from being re-queued on
        // subsequent ticks. Each World::Tick below is preceded by ++GFrameCounter,
        // exactly as the engine frame loop does, so the pawn's real Tick and the
        // production clamp run on every tick. The control rotation is set explicitly
        // before each tick (no input / PlayerTick involved). This is a
        // fixture-level tick-graph / frame-counter adjustment, not a production
        // change and not a weakened assertion.
        PC->Possess(Player);
        TestTrue(TEXT("Player controller possesses the character"), PC->GetPawn() == Player);

        // Decouple the pawn's Tick from the controller's Tick -- the exact inverse of
        // AController::AddPawnTickDependency (FTickFunction::RemovePrerequisite with
        // the same (controller, controller->PrimaryActorTick) pair). The pawn's
        // PrimaryActorTick then fires on every world tick, so the character's Tick and
        // the production clamp execute for every case below.
        Player->PrimaryActorTick.RemovePrerequisite(PC, PC->PrimaryActorTick);
        TestTrue(TEXT("Pawn tick is decoupled from the controller tick"),
                 !Player->PrimaryActorTick.GetPrerequisites().Contains(
                     FTickPrerequisite(PC, PC->PrimaryActorTick)));

        // Each case records the character's TickCount / ClampExecutionCount
        // before its tick and asserts both advanced after it, proving the
        // character ticked and the clamp executed for that case (so in-range
        // and boundary cases cannot pass merely because the clamp never ran).

        // Beyond the upper bound -> the character's Tick clamps to the maximum.
        {
            const int32 TickBefore = Player->GetTickCount();
            const int32 ClampBefore = Player->GetClampExecutionCount();
            PC->SetControlRotation(FRotator(90.0f, 0.0f, 0.0f));
            // Advance the engine frame counter (FEngineLoop::Tick does this once
            // per frame); without it the tick task manager's per-frame dedup gate
            // (HasBeenVisited, keyed on GFrameCounter) blocks re-ticking the pawn.
            ++GFrameCounter;
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
            ++GFrameCounter;
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
            ++GFrameCounter;
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
            ++GFrameCounter;
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
            ++GFrameCounter;
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
