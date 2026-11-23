#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Engine/EngineTypes.h"
#include "InputCoreTypes.h"
#include "UTDDAdannaAnimInstance.h"
#include "TDDForbiddenForestLevel.h"
#include "ATDDAdannaCharacter.generated.h"

/**
 * Integrated Adanna player character.
 *
 * Uses the imported Adanna skeletal mesh (rigged technical gameplay proxy, 21 joints,
 * idle/walk/run/jump/land animations) with a C++ animation state machine
 * (UTDDAdannaAnimInstance). Movement, camera, input, interaction and the objective HUD
 * are carried over from the proven proxy character. If the skeletal mesh asset is not yet
 * imported, the character falls back to the labelled rigid-part technical proxy visuals so
 * PIE remains playable; once the mesh is imported, the proxy parts are not built.
 *
 * The skeletal mesh and animation assets are loaded by SoftObjectPath at BeginPlay, so this
 * class has no compile-time asset dependency and compiles before the assets exist.
 */
UCLASS()
class TDD_GAME_API ATDDAdannaCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ATDDAdannaCharacter();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

    // --- Animation state inputs (read by UTDDAdannaAnimInstance) ---
    bool IsGrounded() const;
    float GetSpeedCmS() const;
    float GetVelocityZ() const;
    bool IsInteracting() const { return bInteracting; }
    void SetInteracting(bool bValue) { bInteracting = bValue; }
    bool IsDodgeing() const { return bDodgeing; }
    bool ConsumeJustLanded();

protected:
    UPROPERTY(VisibleAnywhere, Category = "TDD|Character")
    TObjectPtr<USkeletalMeshComponent> AdannaMesh;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Camera")
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Camera")
    TObjectPtr<UCameraComponent> FollowCamera;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Anim")
    TObjectPtr<UTDDAdannaAnimInstance> AnimInstance;

    // Proxy fallback visuals (only built when the skeletal mesh is unavailable).
    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TArray<TObjectPtr<UStaticMeshComponent>> ProxyParts;

    UPROPERTY()
    TObjectPtr<ATDDForbiddenForestLevel> ForestLevel;

    // Asset paths (resolved at BeginPlay). Override in the Default Properties panel or via
    // the M1 import script report; these defaults match the M1 asset integration spec.
    UPROPERTY(EditDefaultsOnly, Category = "TDD|Character")
    FName SkeletalMeshAssetPath = TEXT("/Game/TDD/Characters/Adanna/Adanna_M1");

    TArray<UStaticMeshComponent*> AnimatedLimbs;
    TArray<FVector> LimbBaseLocations;
    FVector TorsoBaseLocation;
    float LocomotionPhase = 0.0f;
    int32 JumpCount = 0;
    int32 LandCount = 0;
    int32 InteractCount = 0;
    bool bSprinting = false;
    bool bInteracting = false;
    bool bJustLanded = false;
    bool bDodgeing = false;
    bool bDodgeInvulnerable = false;
    float DodgeTimer = 0.0f;
    float DodgeCooldownTimer = 0.0f;
    FVector DodgeDirection = FVector::ZeroVector;
    bool bForwardDown = false;
    bool bBackDown = false;
    bool bRightDown = false;
    bool bLeftDown = false;
    bool bUsingSkeletalMesh = false;
    FString CurrentState = TEXT("IDLE");
    FString NearbyInteraction;

    UStaticMeshComponent* CreatePart(
        const FName& Name,
        const TCHAR* MeshPath,
        const FVector& RelativeLocationCm,
        const FVector& Scale,
        const FLinearColor& Tint,
        const FRotator& RelativeRotation = FRotator::ZeroRotator);

    void BuildTechnicalProxy();
    void IntegrateSkeletalMesh();
    void AnimateProxy(float DeltaSeconds, float SpeedCmS, bool bFalling);
    void UpdateDebugHud(float SpeedCmS, bool bGrounded);
    void BindDefaultInput(UInputComponent* PlayerInputComponent);
    void OnForwardPressed();
    void OnForwardReleased();
    void OnBackPressed();
    void OnBackReleased();
    void OnRightPressed();
    void OnRightReleased();
    void OnLeftPressed();
    void OnLeftReleased();
    void ApplyMovementInput();
    void MoveForward(float Value);
    void MoveRight(float Value);
    void Turn(float Value);
    void LookUp(float Value);
    void SprintStart();
    void SprintStop();
    void JumpPressed();
    void JumpReleased();
    void Interact();
    void Dodge();

    virtual void OnJumped_Implementation() override;
    virtual void Landed(const FHitResult& Hit) override;
};
