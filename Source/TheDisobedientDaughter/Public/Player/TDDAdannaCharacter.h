#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TDDAdannaCharacter.generated.h"

class UCameraComponent;
class USpringArmComponent;
class UTDDCharacterStateComponent;
class UTDDCombatComponent;
class UTDDTraversalComponent;
class USkeletalMesh;

/**
 * Project-owned player character foundation for Adanna.
 *
 * The gameplay pawn, camera and input contract live here; the approved Adanna
 * skeletal mesh and animation assets are separate content dependencies and are
 * intentionally not replaced with an unapproved placeholder.
 */
UCLASS()
class THEDISOBEDIENTDAUGHTER_API ATDDAdannaCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ATDDAdannaCharacter();

    USpringArmComponent* GetCameraBoom() const { return CameraBoom; }
    UCameraComponent* GetFollowCamera() const { return FollowCamera; }
    UTDDCharacterStateComponent* GetStateComponent() const { return StateComponent; }
    UTDDCombatComponent* GetCombatComponent() const { return CombatComponent; }
    UTDDTraversalComponent* GetTraversalComponent() const { return TraversalComponent; }

    /**
     * D-W1D8-024 regression counters: the number of Tick executions and the
     * number of ClampCameraPitch executions on this character. These are the
     * production execution counters the camera automation test asserts on to
     * prove the clamp actually runs for each out-of-range input (rather than
     * the test passing because the clamp never executed).
     */
    int32 GetTickCount() const { return TickCount; }
    int32 GetClampExecutionCount() const { return ClampExecutionCount; }

protected:
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

    /** Clamp the controller pitch to the third-person camera range. */
    void ClampCameraPitch();

    float GetMinCameraPitchDeg() const { return MinCameraPitchDeg; }
    float GetMaxCameraPitchDeg() const { return MaxCameraPitchDeg; }

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void JumpPressed();
    void JumpReleased();
    void LightAttackPressed();
    void GuardPressed();
    void GuardReleased();
    void SprintPressed();
    void SprintReleased();
    void TraversePressed();
    void RestartPressed();
    void UpdateLocomotionIntent();

    float ForwardInput = 0.0f;
    float RightInput = 0.0f;
    bool bSprintRequested = false;

    // D-W1D8-024 regression counters (see public getters).
    int32 TickCount = 0;
    int32 ClampExecutionCount = 0;

    // Third-person camera pitch range (degrees). The spring arm follows the
    // controller rotation, so clamping the control pitch bounds the camera.
    static constexpr float MinCameraPitchDeg = -55.0f;
    static constexpr float MaxCameraPitchDeg = 25.0f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UCameraComponent> FollowCamera;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UTDDCharacterStateComponent> StateComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UTDDCombatComponent> CombatComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="TDD", meta=(AllowPrivateAccess="true"))
    TObjectPtr<UTDDTraversalComponent> TraversalComponent;

    /** Assign the imported, approved/labelled skeletal asset on an editor child. */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="TDD|Character", meta=(AllowPrivateAccess="true"))
    TSoftObjectPtr<USkeletalMesh> CharacterMeshAsset;
};
