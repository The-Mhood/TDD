#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "TDDAdannaCharacter.generated.h"

class UCameraComponent;
class USpringArmComponent;

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

protected:
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

private:
    void MoveForward(float Value);
    void MoveRight(float Value);
    void JumpPressed();
    void JumpReleased();

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<USpringArmComponent> CameraBoom;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<UCameraComponent> FollowCamera;
};
