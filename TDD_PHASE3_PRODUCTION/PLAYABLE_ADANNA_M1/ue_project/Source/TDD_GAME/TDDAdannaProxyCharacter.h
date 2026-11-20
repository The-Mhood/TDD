#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "Components/StaticMeshComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Engine/EngineTypes.h"
#include "InputCoreTypes.h"
#include "TDDForbiddenForestLevel.h"
#include "TDDAdannaProxyCharacter.generated.h"

/**
 * RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER.
 *
 * This is a runtime rigid-part blockout using Unreal CharacterMovement, a capsule,
 * collision-tested spring arm, route progress and interaction. It is not an imported
 * skinned Adanna mesh or a final groom/costume/facial rig.
 */
UCLASS()
class TDD_GAME_API ATDDAdannaProxyCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    ATDDAdannaProxyCharacter();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

protected:
    UPROPERTY(VisibleAnywhere, Category = "TDD|Camera")
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Camera")
    TObjectPtr<UCameraComponent> FollowCamera;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TArray<TObjectPtr<UStaticMeshComponent>> ProxyParts;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> Torso;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> Head;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> LeftArm;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> RightArm;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> LeftLeg;

    UPROPERTY(VisibleAnywhere, Category = "TDD|Proxy")
    TObjectPtr<UStaticMeshComponent> RightLeg;

    UPROPERTY()
    TObjectPtr<ATDDForbiddenForestLevel> ForestLevel;

    TArray<UStaticMeshComponent*> AnimatedLimbs;
    TArray<FVector> LimbBaseLocations;
    FVector TorsoBaseLocation;
    float LocomotionPhase = 0.0f;
    int32 JumpCount = 0;
    int32 LandCount = 0;
    int32 InteractCount = 0;
    bool bSprinting = false;
    bool bForwardDown = false;
    bool bBackDown = false;
    bool bRightDown = false;
    bool bLeftDown = false;
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

    virtual void OnJumped_Implementation() override;
    virtual void Landed(const FHitResult& Hit) override;
};
