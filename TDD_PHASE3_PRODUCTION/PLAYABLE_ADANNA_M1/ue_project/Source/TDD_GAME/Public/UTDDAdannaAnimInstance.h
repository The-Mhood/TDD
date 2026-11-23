#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "UTDDAdannaAnimInstance.generated.h"

class ATDDAdannaCharacter;

// Animation states for the integrated Adanna character. Driven by the character's
// movement state (speed, grounding, vertical velocity) and interaction flag; the
// anim instance selects the matching engine animation and plays it as a dynamic
// montage. Movement is never driven by animation (ACharacterMovementComponent remains
// authoritative), satisfying the "animation is not authoritative for movement" rule.
UENUM(BlueprintType)
enum class EAdannaAnimState : uint8
{
    Idle,
    Walk,
    Run,
    Jump,
    Fall,
    Land,
    Interact
};

/**
 * C++ animation state machine for the integrated Adanna skeletal mesh.
 *
 * Assign this AnimInstance to the character's skeletal mesh component. It resolves the
 * imported Anim Sequences by SoftObjectPath at BeginPlay and plays the correct clip when
 * the character's state changes. If an animation cannot be resolved, it logs a warning and
 * falls back to the idle clip (or no playback) without breaking the game.
 */
UCLASS(Abstract)
class TDD_GAME_API UTDDAdannaAnimInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    UTDDAdannaAnimInstance();

    virtual void NativeInitializeAnimation() override;
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;

    /** Bind the owning character so the state machine can read its movement state. */
    void SetCharacter(ATDDAdannaCharacter* InCharacter) { Character = InCharacter; }

    EAdannaAnimState GetCurrentState() const { return CurrentState; }

    /** Resolve the SoftObjectPath animation assets into concrete pointers (called at BeginPlay). */
    void InitializeAnimationAssets();

protected:
    UPROPERTY()
    TObjectPtr<ATDDAdannaCharacter> Character;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> IdleAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> WalkAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> RunAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> JumpAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> FallAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> LandAnim;

    UPROPERTY(EditDefaultsOnly, Category = "TDD|Anim")
    TSoftObjectPtr<UAnimSequenceBase> InteractAnim;

private:
    EAdannaAnimState CurrentState = EAdannaAnimState::Idle;
    bool bAssetsLoaded = false;

    UAnimSequenceBase* LoadedIdle = nullptr;
    UAnimSequenceBase* LoadedWalk = nullptr;
    UAnimSequenceBase* LoadedRun = nullptr;
    UAnimSequenceBase* LoadedJump = nullptr;
    UAnimSequenceBase* LoadedFall = nullptr;
    UAnimSequenceBase* LoadedLand = nullptr;
    UAnimSequenceBase* LoadedInteract = nullptr;

    EAdannaAnimState ComputeState() const;
    void PlayStateAnimation();
    UAnimSequenceBase* ResolveAnimation(const TSoftObjectPtr<UAnimSequenceBase>& Soft);
};
