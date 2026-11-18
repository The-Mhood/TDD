#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Player/TDDAdannaCharacter.h"
#include "Player/TDDPlayerController.h"
#include "TDDGameMode.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDM1PlayableCharacterDefaultsTest,
    "TDD.M1.Player.PlayableCharacterDefaults",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDM1PlayableCharacterDefaultsTest::RunTest(const FString& Parameters)
{
    const ATDDGameMode* GameMode = GetDefault<ATDDGameMode>();
    TestTrue(
        TEXT("Canonical GameMode spawns the project Adanna character"),
        GameMode->DefaultPawnClass == ATDDAdannaCharacter::StaticClass());
    TestTrue(
        TEXT("Canonical GameMode uses the project player controller"),
        GameMode->PlayerControllerClass == ATDDPlayerController::StaticClass());

    const ATDDAdannaCharacter* Character = GetDefault<ATDDAdannaCharacter>();
    TestNotNull(TEXT("Adanna has a camera boom"), Character->GetCameraBoom());
    TestNotNull(TEXT("Adanna has a follow camera"), Character->GetFollowCamera());
    if (Character->GetCameraBoom() != nullptr && Character->GetFollowCamera() != nullptr)
    {
        TestTrue(
            TEXT("Camera boom has a positive follow distance"),
            Character->GetCameraBoom()->TargetArmLength > 0.0f);
        TestTrue(
            TEXT("Camera boom retains collision testing"),
            Character->GetCameraBoom()->bDoCollisionTest);
        TestTrue(
            TEXT("Follow camera is attached to the camera boom"),
            Character->GetFollowCamera()->GetAttachParent() == Character->GetCameraBoom());
    }

    const UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
    TestNotNull(TEXT("Adanna has CharacterMovementComponent"), Movement);
    if (Movement != nullptr)
    {
        TestTrue(TEXT("Movement turns toward movement input"), Movement->bOrientRotationToMovement);
        TestFalse(TEXT("Character yaw is not hard-locked to controller rotation"), Character->bUseControllerRotationYaw);
    }

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
