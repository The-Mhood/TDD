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
 */
IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1CameraPitchClampTest,
    "TDD.M1.Player.CameraPitchClamp",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

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

    TestTrue(TEXT("Camera pitch range is declared"), Player->GetMaxCameraPitchDeg() > Player->GetMinCameraPitchDeg());

    // Beyond the upper bound -> clamped to the maximum.
    PC->SetControlRotation(FRotator(90.0f, 0.0f, 0.0f));
    Player->ClampCameraPitch();
    TestTrue(TEXT("Over-the-head pitch is clamped to the maximum"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, Player->GetMaxCameraPitchDeg(), 0.01f));

    // Below the lower bound -> clamped to the minimum.
    PC->SetControlRotation(FRotator(-90.0f, 0.0f, 0.0f));
    Player->ClampCameraPitch();
    TestTrue(TEXT("Below-the-feet pitch is clamped to the minimum"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, Player->GetMinCameraPitchDeg(), 0.01f));

    // Within the range -> untouched.
    PC->SetControlRotation(FRotator(10.0f, 45.0f, 0.0f));
    Player->ClampCameraPitch();
    TestTrue(TEXT("In-range pitch and yaw are preserved"),
             FMath::IsNearlyEqual(PC->GetControlRotation().Pitch, 10.0f, 0.01f) &&
             FMath::IsNearlyEqual(PC->GetControlRotation().Yaw, 45.0f, 0.01f));

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
