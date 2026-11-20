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

protected:
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

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
    void UpdateLocomotionIntent();

    float ForwardInput = 0.0f;
    float RightInput = 0.0f;
    bool bSprintRequested = false;

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
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="TDD|Character")
    TSoftObjectPtr<USkeletalMesh> CharacterMeshAsset;
};
