#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Engine/World.h"
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
    UWorld* World = UWorld::CreateWorld(TEXT("TDDCameraPitchClamp"), EWorldType::Game, GetTransientPackage());
    TestNotNull(TEXT("Camera test world created"), World);
    if (World == nullptr)
    {
        return false;
    }

    ATDDAdannaCharacter* Player = World->SpawnActor<ATDDAdannaCharacter>(FVector::ZeroVector, FRotator::ZeroRotator);
    TestNotNull(TEXT("Player character spawned in the test world"), Player);
    if (Player == nullptr)
    {
        return false;
    }
    APlayerController* PC = World->SpawnActor<APlayerController>();
    TestNotNull(TEXT("Player controller spawned in the test world"), PC);
    if (PC == nullptr)
    {
        return false;
    }
    PC->Possess(Player);

    TestTrue(TEXT("Camera pitch range is declared"), MaxCameraPitchDeg > MinCameraPitchDeg);

    // Beyond the upper bound -> the character's Tick clamps to the maximum.
    PC->SetControlRotation(FRotator(90.0f, 0.0f, 0.0f));
    World->Tick(LEVELTICK_All, 0.016f);
    TestTrue(TEXT("Over-the-head pitch is clamped to the maximum"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MaxCameraPitchDeg, 0.01f));

    // Below the lower bound -> clamped to the minimum.
    PC->SetControlRotation(FRotator(-90.0f, 0.0f, 0.0f));
    World->Tick(LEVELTICK_All, 0.016f);
    TestTrue(TEXT("Below-the-feet pitch is clamped to the minimum"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, MinCameraPitchDeg, 0.01f));

    // Within the range -> untouched.
    PC->SetControlRotation(FRotator(10.0f, 45.0f, 0.0f));
    World->Tick(LEVELTICK_All, 0.016f);
    TestTrue(TEXT("In-range pitch and yaw are preserved"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, 10.0f, 0.01f) &&
             FMath::IsNearlyEqual(PC->GetControlRotation().Yaw, 45.0f, 0.01f));

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
