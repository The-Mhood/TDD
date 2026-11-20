#include "Player/TDDAdannaCharacter.h"

#include "Camera/CameraComponent.h"
#include "Combat/TDDCombatComponent.h"
#include "Components/CapsuleComponent.h"
#include "Core/TDDGaitMath.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputCoreTypes.h"
#include "Engine/SkeletalMesh.h"
#include "Kismet/GameplayStatics.h"
#include "Traversal/TDDTraversalComponent.h"
#include "Player/TDDCharacterStateComponent.h"
#include "TDDGameMode.h"

ATDDAdannaCharacter::ATDDAdannaCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    bUseControllerRotationPitch = false;
    bUseControllerRotationRoll = false;
    bUseControllerRotationYaw = false;

    UCharacterMovementComponent* Movement = GetCharacterMovement();
    Movement->bOrientRotationToMovement = true;
    Movement->bUseControllerDesiredRotation = false;
    const TDD::Movement::FTDDGaitParams& Walk = TDD::Movement::GaitParams(TDD::Movement::ETDDGait::Walk);
    Movement->MaxWalkSpeed = Walk.Speed;
    Movement->MaxAcceleration = Walk.Acceleration;
    Movement->BrakingDecelerationWalking = Walk.Braking;
    Movement->RotationRate = FRotator(0.0f, Walk.TurnRateDeg, 0.0f);
    Movement->JumpZVelocity = TDD::Movement::JumpInitialVy();
    Movement->GravityScale = TDD::Movement::Gravity() / 980.0f;

    StateComponent = CreateDefaultSubobject<UTDDCharacterStateComponent>(TEXT("TDDState"));
    CombatComponent = CreateDefaultSubobject<UTDDCombatComponent>(TEXT("TDDCombat"));
    TraversalComponent = CreateDefaultSubobject<UTDDTraversalComponent>(TEXT("TDDTraversal"));

    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    CameraBoom->SetupAttachment(GetCapsuleComponent());
    CameraBoom->SetRelativeLocation(FVector(0.0f, 0.0f, 60.0f));
    CameraBoom->TargetArmLength = 350.0f;
    CameraBoom->bUsePawnControlRotation = true;
    CameraBoom->bDoCollisionTest = true;

    FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;
}

void ATDDAdannaCharacter::BeginPlay()
{
    Super::BeginPlay();
    if (!CharacterMeshAsset.IsNull())
    {
        if (USkeletalMesh* ImportedMesh = CharacterMeshAsset.LoadSynchronous())
        {
            GetMesh()->SetSkeletalMesh(ImportedMesh);
        }
    }
}

void ATDDAdannaCharacter::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    ClampCameraPitch();
}

void ATDDAdannaCharacter::ClampCameraPitch()
{
    AController* ControllerRef = GetController();
    if (ControllerRef == nullptr)
    {
        return;
    }
    const FRotator Control = ControllerRef->GetControlRotation();
    const float Clamped = FMath::Clamp(Control.Pitch, MinCameraPitchDeg, MaxCameraPitchDeg);
    if (!FMath::IsNearlyEqual(Clamped, Control.Pitch, 0.01f))
    {
        ControllerRef->SetControlRotation(FRotator(Clamped, Control.Yaw, 0.0f));
    }
}

void ATDDAdannaCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    check(PlayerInputComponent != nullptr);
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &ATDDAdannaCharacter::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &ATDDAdannaCharacter::MoveRight);
    PlayerInputComponent->BindAxis(TEXT("Turn"), this, &APawn::AddControllerYawInput);
    PlayerInputComponent->BindAxis(TEXT("LookUp"), this, &APawn::AddControllerPitchInput);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Pressed, this, &ATDDAdannaCharacter::JumpPressed);
    PlayerInputComponent->BindAction(TEXT("Jump"), IE_Released, this, &ATDDAdannaCharacter::JumpReleased);
    PlayerInputComponent->BindAction(TEXT("LightAttack"), IE_Pressed, this, &ATDDAdannaCharacter::LightAttackPressed);
    PlayerInputComponent->BindAction(TEXT("Guard"), IE_Pressed, this, &ATDDAdannaCharacter::GuardPressed);
    PlayerInputComponent->BindAction(TEXT("Guard"), IE_Released, this, &ATDDAdannaCharacter::GuardReleased);
    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Pressed, this, &ATDDAdannaCharacter::SprintPressed);
    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Released, this, &ATDDAdannaCharacter::SprintReleased);
    PlayerInputComponent->BindAction(TEXT("Traverse"), IE_Pressed, this, &ATDDAdannaCharacter::TraversePressed);
    PlayerInputComponent->BindAction(TEXT("Restart"), IE_Pressed, this, &ATDDAdannaCharacter::RestartPressed);
}

void ATDDAdannaCharacter::RestartPressed()
{
    // UE 5.8.4: AActor has no templated game-mode accessor member. The
    // supported access path is UGameplayStatics::GetGameMode(WorldContext)
    // (which reads UWorld::GetAuthGameMode()) followed by a cast; the world
    // pointer is checked first so a null context stays null-safe.
    UWorld* World = GetWorld();
    if (World == nullptr)
    {
        return;
    }
    if (ATDDGameMode* GameMode = Cast<ATDDGameMode>(UGameplayStatics::GetGameMode(World)))
    {
        GameMode->RestartEncounter();
    }
}

void ATDDAdannaCharacter::MoveForward(const float Value)
{
    if (!FMath::IsFinite(Value)) return;
    ForwardInput = Value;
    if (Controller != nullptr && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRotation = Controller->GetControlRotation();
        const FRotator YawRotation(0.0f, ControlRotation.Yaw, 0.0f);
        AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X), Value);
    }
    UpdateLocomotionIntent();
}

void ATDDAdannaCharacter::MoveRight(const float Value)
{
    if (!FMath::IsFinite(Value)) return;
    RightInput = Value;
    if (Controller != nullptr && !FMath::IsNearlyZero(Value))
    {
        const FRotator ControlRotation = Controller->GetControlRotation();
        const FRotator YawRotation(0.0f, ControlRotation.Yaw, 0.0f);
        AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y), Value);
    }
    UpdateLocomotionIntent();
}

void ATDDAdannaCharacter::JumpPressed()
{
    Jump();
}

void ATDDAdannaCharacter::JumpReleased()
{
    StopJumping();
}

void ATDDAdannaCharacter::LightAttackPressed()
{
    if (CombatComponent != nullptr)
    {
        CombatComponent->PerformLightAttack();
    }
}

void ATDDAdannaCharacter::GuardPressed()
{
    if (CombatComponent != nullptr)
    {
        CombatComponent->SetGuarding(true);
    }
}

void ATDDAdannaCharacter::GuardReleased()
{
    if (CombatComponent != nullptr)
    {
        CombatComponent->SetGuarding(false);
    }
}

void ATDDAdannaCharacter::SprintPressed()
{
    bSprintRequested = true;
    UpdateLocomotionIntent();
}

void ATDDAdannaCharacter::SprintReleased()
{
    bSprintRequested = false;
    UpdateLocomotionIntent();
}

void ATDDAdannaCharacter::TraversePressed()
{
    if (TraversalComponent != nullptr)
    {
        TraversalComponent->TryTraverse();
    }
}

void ATDDAdannaCharacter::UpdateLocomotionIntent()
{
    UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (Movement == nullptr || StateComponent == nullptr)
    {
        return;
    }
    const bool bMoving = FMath::Square(ForwardInput) + FMath::Square(RightInput) > 0.01f;
    const int32 Current = StateComponent->GetCurrentState();
    const int32 Idle = static_cast<int32>(TDD::State::ETDDPlayerState::Idle);
    const int32 Locomotion = static_cast<int32>(TDD::State::ETDDPlayerState::Locomotion);
    const int32 Sprint = static_cast<int32>(TDD::State::ETDDPlayerState::Sprint);
    if (Current == Idle || Current == Locomotion || Current == Sprint)
    {
        const TDD::Movement::FTDDGaitParams& Gait = TDD::Movement::GaitParams(
            bSprintRequested ? TDD::Movement::ETDDGait::Run : TDD::Movement::ETDDGait::Walk);
        Movement->MaxWalkSpeed = Gait.Speed;
        Movement->MaxAcceleration = Gait.Acceleration;
        Movement->BrakingDecelerationWalking = Gait.Braking;
        Movement->RotationRate = FRotator(0.0f, Gait.TurnRateDeg, 0.0f);
        StateComponent->SetLocomotionIntent(bMoving, bSprintRequested && bMoving);
    }
}
