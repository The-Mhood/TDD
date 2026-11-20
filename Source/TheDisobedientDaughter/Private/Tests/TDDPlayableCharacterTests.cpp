#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "AI/TDDTrainingEnemy.h"
#include "Combat/TDDCombatComponent.h"
#include "Player/TDDCharacterStateComponent.h"
#include "Traversal/TDDTraversalComponent.h"
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

    TestNotNull(TEXT("Adanna has one project state authority"), Character->GetStateComponent());
    TestNotNull(TEXT("Adanna has actor-facing combat integration"), Character->GetCombatComponent());
    TestNotNull(TEXT("Adanna has runtime traversal component"), Character->GetTraversalComponent());
    if (Character->GetStateComponent() != nullptr)
    {
        TestEqual(TEXT("Default player state is Idle"), Character->GetStateComponent()->GetCurrentState(),
                  static_cast<int32>(TDD::State::ETDDPlayerState::Idle));
    }

    const UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
    TestNotNull(TEXT("Adanna has CharacterMovementComponent"), Movement);
    if (Movement != nullptr)
    {
        TestTrue(TEXT("Movement turns toward movement input"), Movement->bOrientRotationToMovement);
        TestFalse(TEXT("Character yaw is not hard-locked to controller rotation"), Character->bUseControllerRotationYaw);
        TestEqual(TEXT("Walk speed comes from the pure gait contract"), Movement->MaxWalkSpeed, 220.0f);
        TestEqual(TEXT("Walk acceleration comes from the pure gait contract"), Movement->MaxAcceleration, 1200.0f);
        TestEqual(TEXT("Jump velocity comes from the pure vertical contract"), Movement->JumpZVelocity, 500.0f);
        TestTrue(TEXT("Gravity scale adapts the 1500 cm/s^2 contract to UE default gravity"),
                 FMath::IsNearlyEqual(Movement->GravityScale * 980.0f, 1500.0f, 0.1f));
    }

    const ATDDTrainingEnemy* Enemy = GetDefault<ATDDTrainingEnemy>();
    TestNotNull(TEXT("Training enemy class is registered"), Enemy);
    if (Enemy != nullptr)
    {
        TestNotNull(TEXT("Training enemy has shared combat component"), Enemy->GetCombatComponent());
        TestNotNull(TEXT("Training enemy has shared player-state component"), Enemy->GetStateComponent());
        TestTrue(TEXT("Training enemy auto-possesses an AI controller"),
                 Enemy->AutoPossessAI == EAutoPossessAI::PlacedInWorldOrSpawned);
    }

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
