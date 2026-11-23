#include "UTDDAdannaAnimInstance.h"

#include "ATDDAdannaCharacter.h"
#include "Engine/SkeletalMesh.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/AnimationSequence.h"

UTDDAdannaAnimInstance::UTDDAdannaAnimInstance()
{
    // Default animation paths match the M1 asset integration spec destination
    // (/Game/TDD/Animations/). The import script reports the exact imported asset
    // names; adjust these in the AnimInstance's Default Properties if the Interchange
    // import names differ from the glTF clip names (idle/walk/run/jump/land).
    IdleAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/idle"));
    WalkAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/walk"));
    RunAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/run"));
    JumpAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/jump"));
    FallAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/fall"));
    LandAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/land"));
    InteractAnim = FSoftObjectPath(TEXT("/Game/TDD/Animations/interact"));
}

void UTDDAdannaAnimInstance::NativeInitializeAnimation()
{
    Super::NativeInitializeAnimation();
    InitializeAnimationAssets();
}

void UTDDAdannaAnimInstance::InitializeAnimationAssets()
{
    LoadedIdle = ResolveAnimation(IdleAnim);
    LoadedWalk = ResolveAnimation(WalkAnim);
    LoadedRun = ResolveAnimation(RunAnim);
    LoadedJump = ResolveAnimation(JumpAnim);
    LoadedFall = ResolveAnimation(FallAnim);
    LoadedLand = ResolveAnimation(LandAnim);
    LoadedInteract = ResolveAnimation(InteractAnim);

    bAssetsLoaded =
        LoadedIdle != nullptr || LoadedWalk != nullptr || LoadedRun != nullptr ||
        LoadedJump != nullptr || LoadedFall != nullptr || LoadedLand != nullptr ||
        LoadedInteract != nullptr;

    if (!bAssetsLoaded)
    {
        UE_LOG(LogTemp, Warning,
            TEXT("TDD M1: no Adanna animation assets resolved. The character will render "
                 "without locomotion animation. Run the M1 import script and assign the "
                 "animation SoftObjectPaths on UTDDAdannaAnimInstance."));
    }
}

UAnimSequenceBase* UTDDAdannaAnimInstance::ResolveAnimation(const TSoftObjectPtr<UAnimSequenceBase>& Soft)
{
    if (Soft.IsNull())
    {
        return nullptr;
    }
    return Soft.LoadSynchronous();
}

EAdannaAnimState UTDDAdannaAnimInstance::ComputeState() const
{
    if (!Character)
    {
        return EAdannaAnimState::Idle;
    }

    if (Character->IsInteracting())
    {
        return EAdannaAnimState::Interact;
    }

    const bool bGrounded = Character->IsGrounded();
    const float SpeedCmS = Character->GetSpeedCmS();
    const float VelocityZ = Character->GetVelocityZ();

    if (!bGrounded)
    {
        if (Character->ConsumeJustLanded())
        {
            return EAdannaAnimState::Land;
        }
        return VelocityZ >= 0.0f ? EAdannaAnimState::Jump : EAdannaAnimState::Fall;
    }

    if (Character->ConsumeJustLanded())
    {
        return EAdannaAnimState::Land;
    }

    // Walk/run thresholds mirror the character's movement tuning.
    const float WalkThreshold = 30.0f;
    const float RunThreshold = 350.0f;
    if (SpeedCmS < WalkThreshold)
    {
        return EAdannaAnimState::Idle;
    }
    if (SpeedCmS >= RunThreshold)
    {
        return EAdannaAnimState::Run;
    }
    return EAdannaAnimState::Walk;
}

void UTDDAdannaAnimInstance::PlayStateAnimation()
{
    if (!bAssetsLoaded)
    {
        return;
    }

    UAnimSequenceBase* Target = nullptr;
    switch (CurrentState)
    {
    case EAdannaAnimState::Idle:      Target = LoadedIdle;      break;
    case EAdannaAnimState::Walk:      Target = LoadedWalk;      break;
    case EAdannaAnimState::Run:       Target = LoadedRun;       break;
    case EAdannaAnimState::Jump:      Target = LoadedJump;      break;
    case EAdannaAnimState::Fall:      Target = LoadedFall;      break;
    case EAdannaAnimState::Land:      Target = LoadedLand;      break;
    case EAdannaAnimState::Interact:  Target = LoadedInteract;  break;
    default:                          Target = LoadedIdle;      break;
    }

    if (Target)
    {
        // Play as a dynamic montage in a stable slot so state transitions blend cleanly.
        PlaySlotAnimationAsDynamicMontage(Target, TEXT("TDD_Adanna"), 1.0f, 0.0f, 0.15f);
    }
}

void UTDDAdannaAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeUpdateAnimation(DeltaSeconds);

    if (!bAssetsLoaded)
    {
        return;
    }

    const EAdannaAnimState NewState = ComputeState();
    if (NewState != CurrentState)
    {
        CurrentState = NewState;
        PlayStateAnimation();
    }
}
