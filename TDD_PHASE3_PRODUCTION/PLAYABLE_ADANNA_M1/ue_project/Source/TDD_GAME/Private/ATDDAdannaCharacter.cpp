#include "ATDDAdannaCharacter.h"

#include "Components/StaticMeshComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "Camera/CameraComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimInstance.h"

#include "TDDWorldData.h"
#include "Camera/PlayerCameraManager.h"
#include "Components/CapsuleComponent.h"
#include "Engine/Engine.h"
#include "Engine/StaticMesh.h"
#include "EngineUtils.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/Controller.h"
#include "GameFramework/PlayerController.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Materials/MaterialInterface.h"
#include "Math/RotationMatrix.h"
#include "UObject/UObjectGlobals.h"

namespace
{
    constexpr TCHAR AdannaProxyCubeMesh[] = TEXT("/Engine/BasicShapes/Cube.Cube");
    constexpr TCHAR AdannaProxyCylinderMesh[] = TEXT("/Engine/BasicShapes/Cylinder.Cylinder");
    constexpr TCHAR AdannaProxySphereMesh[] = TEXT("/Engine/BasicShapes/Sphere.Sphere");
    constexpr TCHAR AdannaProxyBasicShapeMaterial[] = TEXT("/Engine/BasicShapes/ProxyBasicShapeMaterial.ProxyBasicShapeMaterial");

    // Palette-derived technical colours; not calibrated final materials.
    const FLinearColor AdannaSkin(0.263f, 0.176f, 0.153f, 1.0f);
    const FLinearColor AdannaIndigo(0.075f, 0.090f, 0.135f, 1.0f);
    const FLinearColor AdannaLeather(0.180f, 0.105f, 0.075f, 1.0f);
    const FLinearColor AdannaAgedBronze(0.390f, 0.270f, 0.125f, 1.0f);
    const FLinearColor AdannaCoral(0.480f, 0.155f, 0.110f, 1.0f);
    const FLinearColor AdannaHair(0.025f, 0.026f, 0.030f, 1.0f);
    const FLinearColor AdannaScar(0.410f, 0.255f, 0.205f, 1.0f);

    // Dodge burst tuning. Dodge is a movement burst (no dedicated dodge animation asset
    // exists in the M1 set yet), so it uses the run locomotion and grants brief
    // invulnerability for future combat integration.
    constexpr float DodgeSpeedCmS = 1150.0f;
    constexpr float DodgeDurationS = 0.32f;
    constexpr float DodgeCooldownS = 0.75f;
}

ATDDAdannaCharacter::ATDDAdannaCharacter()
{
    PrimaryActorTick.bCanEverTick = true;

    GetCapsuleComponent()->InitCapsuleSize(
        TDDWorldData::CharacterRadiusCm,
        TDDWorldData::CharacterHalfHeightCm);
    GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));

    bUseControllerRotationYaw = true;
    bUseControllerRotationPitch = false;
    bUseControllerRotationRoll = false;

    UCharacterMovementComponent* Movement = GetCharacterMovement();
    Movement->bOrientRotationToMovement = false;
    Movement->MaxWalkSpeed = TDDWorldData::WalkSpeedCmS;
    Movement->JumpZVelocity = TDDWorldData::JumpVelocityCmS;
    Movement->GravityScale = 1.0f;
    Movement->AirControl = 0.28f;
    Movement->GroundFriction = 8.0f;
    Movement->BrakingDecelerationWalking = 900.0f;
    Movement->MaxAcceleration = 900.0f;

    // Skeletal mesh carries the integrated Adanna. SetAnimInstanceClass is called here so
    // the engine creates the C++ state machine when the component initializes (UE 5.8.4:
    // USkeletalMeshComponent exposes SetAnimInstanceClass; the AnimClass member is the
    // serialized form of the same setting).
    AdannaMesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("Mesh"));
    AdannaMesh->SetupAttachment(GetCapsuleComponent());
    AdannaMesh->SetMobility(EComponentMobility::Movable);
    AdannaMesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    AdannaMesh->SetGenerateOverlapEvents(false);
    AdannaMesh->SetCastShadow(true);
    AdannaMesh->SetAnimInstanceClass(UTDDAdannaAnimInstance::StaticClass());

    CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
    CameraBoom->SetupAttachment(RootComponent);
    CameraBoom->TargetArmLength = TDDWorldData::CameraDistanceCm;
    CameraBoom->TargetOffset = FVector(0.0f, 0.0f, 65.0f);
    CameraBoom->bUsePawnControlRotation = true;
    CameraBoom->bDoCollisionTest = true;
    CameraBoom->ProbeSize = 12.0f;
    CameraBoom->ProbeChannel = ECC_Camera;
    CameraBoom->bEnableCameraLag = true;
    CameraBoom->CameraLagSpeed = 12.0f;

    FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
    FollowCamera->SetupAttachment(CameraBoom, USpringArmComponent::SocketName);
    FollowCamera->bUsePawnControlRotation = false;

    ForestLevel = nullptr;
}

void ATDDAdannaCharacter::BeginPlay()
{
    Super::BeginPlay();

    IntegrateSkeletalMesh();
    if (!bUsingSkeletalMesh)
    {
        // Keep PIE playable before the Adanna asset is imported.
        BuildTechnicalProxy();
    }

    // Bind the animation state machine to this character.
    if (UTDDAdannaAnimInstance* Anim = Cast<UTDDAdannaAnimInstance>(AdannaMesh ? AdannaMesh->GetAnimInstance() : nullptr))
    {
        AnimInstance = Anim;
        Anim->SetCharacter(this);
    }

    SetActorLocation(
        FVector(TDDWorldData::SpawnXCm, TDDWorldData::SpawnYCm, TDDWorldData::SpawnZCm),
        false,
        nullptr,
        ETeleportType::TeleportPhysics);
    SetActorRotation(FRotator(0.0f, 90.0f, 0.0f));

    if (AController* OwningController = GetController())
    {
        OwningController->SetControlRotation(FRotator(0.0f, 90.0f, 0.0f));
        if (APlayerController* PC = Cast<APlayerController>(OwningController))
        {
            PC->bShowMouseCursor = false;
            if (PC->PlayerCameraManager)
            {
                PC->PlayerCameraManager->ViewPitchMin = -38.0f;
                PC->PlayerCameraManager->ViewPitchMax = -5.0f;
            }
        }
    }

    // Take the first matching level actor. Declared on its own line: a variable
    // declaration inside an `if` condition cannot have a parenthesized initializer.
    TActorIterator<ATDDForbiddenForestLevel> It(
        GetWorld(), ATDDForbiddenForestLevel::StaticClass(), EActorIteratorFlags::AllActors);
    if (It)
    {
        ForestLevel = *It;
    }

    UE_LOG(LogTemp, Display,
        TEXT("TDD M1: Adanna character ready (skeletal mesh: %s)."),
        bUsingSkeletalMesh ? TEXT("YES") : TEXT("NO — proxy fallback"));
}

void ATDDAdannaCharacter::IntegrateSkeletalMesh()
{
    if (!AdannaMesh)
    {
        return;
    }

    USkeletalMesh* SkeletalMesh = LoadObject<USkeletalMesh>(nullptr, *SkeletalMeshAssetPath.ToString());
    if (SkeletalMesh)
    {
        AdannaMesh->SetSkeletalMesh(SkeletalMesh);
        bUsingSkeletalMesh = true;
    }
    else
    {
        UE_LOG(LogTemp, Warning,
            TEXT("TDD M1: Adanna skeletal mesh not found at '%s'. Using technical proxy "
                 "fallback visuals. Run the M1 import script to import the character."),
            *SkeletalMeshAssetPath.ToString());
    }
}

UStaticMeshComponent* ATDDAdannaCharacter::CreatePart(
    const FName& Name,
    const TCHAR* MeshPath,
    const FVector& RelativeLocationCm,
    const FVector& Scale,
    const FLinearColor& Tint,
    const FRotator& RelativeRotation)
{
    UStaticMeshComponent* Part = NewObject<UStaticMeshComponent>(this, Name);
    Part->SetupAttachment(GetCapsuleComponent());
    Part->SetMobility(EComponentMobility::Movable);

    UStaticMesh* MeshAsset = LoadObject<UStaticMesh>(nullptr, MeshPath);
    if (MeshAsset)
    {
        Part->SetStaticMesh(MeshAsset);
    }

    UMaterialInterface* BaseMaterial = LoadObject<UMaterialInterface>(nullptr, AdannaProxyBasicShapeMaterial);
    if (BaseMaterial)
    {
        UMaterialInstanceDynamic* TintMaterial = UMaterialInstanceDynamic::Create(BaseMaterial, this);
        TintMaterial->SetVectorParameterValue(TEXT("Color"), Tint);
        Part->SetMaterial(0, TintMaterial);
    }

    Part->SetRelativeLocation(RelativeLocationCm);
    Part->SetRelativeRotation(RelativeRotation);
    Part->SetRelativeScale3D(Scale);
    Part->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    Part->SetGenerateOverlapEvents(false);
    Part->SetCastShadow(true);
    AddInstanceComponent(Part);
    Part->RegisterComponent();
    ProxyParts.Add(Part);
    return Part;
}

void ATDDAdannaCharacter::BuildTechnicalProxy()
{
    // Labelled rigid-part technical proxy fallback (identical to the proven proxy).
    // +Y is the character's anatomical left for this forward-X proxy.
    TObjectPtr<UStaticMeshComponent> Torso = CreatePart(TEXT("PROXY_TORSO_INDIGO"), AdannaProxyCubeMesh, FVector(0, 0, -8), FVector(0.48f, 0.27f, 0.70f), AdannaIndigo);
    CreatePart(TEXT("PROXY_LEATHER_CHEST_STRAP"), AdannaProxyCubeMesh, FVector(8, 0, 5), FVector(0.12f, 0.29f, 0.58f), AdannaLeather, FRotator(0, 0, 18));
    CreatePart(TEXT("PROXY_INDIGO_HANDWOVEN_WRAP"), AdannaProxyCubeMesh, FVector(0, 0, -42), FVector(0.48f, 0.28f, 0.34f), AdannaIndigo);

    TObjectPtr<UStaticMeshComponent> Head = CreatePart(TEXT("PROXY_HEAD"), AdannaProxySphereMesh, FVector(0, 0, 52), FVector(0.21f, 0.21f, 0.25f), AdannaSkin);
    CreatePart(TEXT("PROXY_THIN_BRAIDS_HIGH_KNOT"), AdannaProxySphereMesh, FVector(0, 0, 74), FVector(0.13f, 0.13f, 0.13f), AdannaHair);
    CreatePart(TEXT("PROXY_BRAID_CAP"), AdannaProxySphereMesh, FVector(0, 0, 64), FVector(0.22f, 0.22f, 0.11f), AdannaHair);

    TObjectPtr<UStaticMeshComponent> LeftArm = CreatePart(TEXT("PROXY_LEFT_ARM"), AdannaProxyCylinderMesh, FVector(0, 28, 0), FVector(0.14f, 0.14f, 0.55f), AdannaSkin);
    TObjectPtr<UStaticMeshComponent> RightArm = CreatePart(TEXT("PROXY_RIGHT_ARM"), AdannaProxyCylinderMesh, FVector(0, -28, 0), FVector(0.14f, 0.14f, 0.55f), AdannaSkin);
    CreatePart(TEXT("PROXY_COILED_BRONZE_ARMLET_LEFT_ONLY"), AdannaProxyCylinderMesh, FVector(0, 28, 19), FVector(0.16f, 0.16f, 0.085f), AdannaAgedBronze);

    TObjectPtr<UStaticMeshComponent> LeftLeg = CreatePart(TEXT("PROXY_LEFT_LEG"), AdannaProxyCylinderMesh, FVector(0, 10, -58), FVector(0.15f, 0.15f, 0.62f), AdannaSkin);
    TObjectPtr<UStaticMeshComponent> RightLeg = CreatePart(TEXT("PROXY_RIGHT_LEG"), AdannaProxyCylinderMesh, FVector(0, -10, -58), FVector(0.15f, 0.15f, 0.62f), AdannaSkin);
    CreatePart(TEXT("PROXY_LEFT_WRAP"), AdannaProxyCubeMesh, FVector(0, 10, -78), FVector(0.18f, 0.18f, 0.24f), AdannaIndigo);
    CreatePart(TEXT("PROXY_RIGHT_WRAP"), AdannaProxyCubeMesh, FVector(0, -10, -78), FVector(0.18f, 0.18f, 0.24f), AdannaIndigo);
    CreatePart(TEXT("PROXY_LEFT_FOOT"), AdannaProxyCubeMesh, FVector(8, 10, -87), FVector(0.25f, 0.16f, 0.09f), AdannaLeather);
    CreatePart(TEXT("PROXY_RIGHT_FOOT"), AdannaProxyCubeMesh, FVector(8, -10, -87), FVector(0.25f, 0.16f, 0.09f), AdannaLeather);
    CreatePart(TEXT("PROXY_LEFT_HIP_CROSS_DRAW_MOUNT_MARKER"), AdannaProxyCubeMesh, FVector(-5, 15, -40), FVector(0.05f, 0.07f, 0.16f), AdannaLeather, FRotator(0, 0, 16));

    AnimatedLimbs.Reset();
    LimbBaseLocations.Reset();
    AnimatedLimbs.Add(LeftArm);
    AnimatedLimbs.Add(RightArm);
    AnimatedLimbs.Add(LeftLeg);
    AnimatedLimbs.Add(RightLeg);
    LimbBaseLocations.Add(LeftArm->GetRelativeLocation());
    LimbBaseLocations.Add(RightArm->GetRelativeLocation());
    LimbBaseLocations.Add(LeftLeg->GetRelativeLocation());
    LimbBaseLocations.Add(RightLeg->GetRelativeLocation());
    TorsoBaseLocation = Torso->GetRelativeLocation();
}

// --- Animation state inputs -----------------------------------------------------------

bool ATDDAdannaCharacter::IsGrounded() const
{
    return GetCharacterMovement() && GetCharacterMovement()->IsMovingOnGround();
}

float ATDDAdannaCharacter::GetSpeedCmS() const
{
    return GetVelocity().Size2D();
}

float ATDDAdannaCharacter::GetVelocityZ() const
{
    return GetVelocity().Z;
}

bool ATDDAdannaCharacter::ConsumeJustLanded()
{
    if (bJustLanded)
    {
        bJustLanded = false;
        return true;
    }
    return false;
}

// --- Input ---------------------------------------------------------------------------

void ATDDAdannaCharacter::OnForwardPressed() { bForwardDown = true; }
void ATDDAdannaCharacter::OnForwardReleased() { bForwardDown = false; }
void ATDDAdannaCharacter::OnBackPressed() { bBackDown = true; }
void ATDDAdannaCharacter::OnBackReleased() { bBackDown = false; }
void ATDDAdannaCharacter::OnRightPressed() { bRightDown = true; }
void ATDDAdannaCharacter::OnRightReleased() { bRightDown = false; }
void ATDDAdannaCharacter::OnLeftPressed() { bLeftDown = true; }
void ATDDAdannaCharacter::OnLeftReleased() { bLeftDown = false; }

void ATDDAdannaCharacter::ApplyMovementInput()
{
    // During the dodge burst, normal input-driven locomotion is suppressed so the burst
    // velocity is not overridden.
    if (bDodgeing)
    {
        return;
    }
    const float Forward = (bForwardDown ? 1.0f : 0.0f) - (bBackDown ? 1.0f : 0.0f);
    const float Right = (bRightDown ? 1.0f : 0.0f) - (bLeftDown ? 1.0f : 0.0f);
    if (!FMath::IsNearlyZero(Forward))
    {
        MoveForward(Forward);
    }
    if (!FMath::IsNearlyZero(Right))
    {
        MoveRight(Right);
    }
}

void ATDDAdannaCharacter::BindDefaultInput(UInputComponent* PlayerInputComponent)
{
    PlayerInputComponent->BindKey(EKeys::W, IE_Pressed, this, &ATDDAdannaCharacter::OnForwardPressed);
    PlayerInputComponent->BindKey(EKeys::W, IE_Released, this, &ATDDAdannaCharacter::OnForwardReleased);
    PlayerInputComponent->BindKey(EKeys::S, IE_Pressed, this, &ATDDAdannaCharacter::OnBackPressed);
    PlayerInputComponent->BindKey(EKeys::S, IE_Released, this, &ATDDAdannaCharacter::OnBackReleased);
    PlayerInputComponent->BindKey(EKeys::D, IE_Pressed, this, &ATDDAdannaCharacter::OnRightPressed);
    PlayerInputComponent->BindKey(EKeys::D, IE_Released, this, &ATDDAdannaCharacter::OnRightReleased);
    PlayerInputComponent->BindKey(EKeys::A, IE_Pressed, this, &ATDDAdannaCharacter::OnLeftPressed);
    PlayerInputComponent->BindKey(EKeys::A, IE_Released, this, &ATDDAdannaCharacter::OnLeftReleased);

    PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ATDDAdannaCharacter::Turn);
    PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ATDDAdannaCharacter::LookUp);

    PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ATDDAdannaCharacter::JumpPressed);
    PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ATDDAdannaCharacter::JumpReleased);
    PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ATDDAdannaCharacter::SprintStart);
    PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ATDDAdannaCharacter::SprintStop);
    PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ATDDAdannaCharacter::Interact);
    PlayerInputComponent->BindKey(EKeys::LeftControl, IE_Pressed, this, &ATDDAdannaCharacter::Dodge);
}

void ATDDAdannaCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    check(PlayerInputComponent);
    BindDefaultInput(PlayerInputComponent);
}

void ATDDAdannaCharacter::MoveForward(float Value)
{
    if (!Controller || FMath::IsNearlyZero(Value)) return;
    const FRotator YawRotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
    AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X), Value);
}

void ATDDAdannaCharacter::MoveRight(float Value)
{
    if (!Controller || FMath::IsNearlyZero(Value)) return;
    const FRotator YawRotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
    AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y), Value);
}

void ATDDAdannaCharacter::Turn(float Value)
{
    AddControllerYawInput(Value);
}

void ATDDAdannaCharacter::LookUp(float Value)
{
    AddControllerPitchInput(Value);
}

void ATDDAdannaCharacter::SprintStart()
{
    bSprinting = true;
    GetCharacterMovement()->MaxWalkSpeed = TDDWorldData::RunSpeedCmS;
}

void ATDDAdannaCharacter::SprintStop()
{
    bSprinting = false;
    GetCharacterMovement()->MaxWalkSpeed = TDDWorldData::WalkSpeedCmS;
}

void ATDDAdannaCharacter::JumpPressed()
{
    Jump();
}

void ATDDAdannaCharacter::JumpReleased()
{
    StopJumping();
}

void ATDDAdannaCharacter::Interact()
{
    FString Message;
    if (ForestLevel && ForestLevel->TryGetNearbyInteraction(GetActorLocation(), Message))
    {
        ++InteractCount;
        NearbyInteraction = Message;
        UE_LOG(LogTemp, Display, TEXT("TDD M1 interaction: %s"), *Message);
        if (GEngine)
        {
            GEngine->AddOnScreenDebugMessage(2, 3.0f, FColor(232, 205, 157), Message);
        }
    }
}

void ATDDAdannaCharacter::Dodge()
{
    if (bDodgeing || !IsGrounded() || bInteracting)
    {
        return;
    }
    if (DodgeCooldownTimer > 0.0f)
    {
        return;
    }

    UCharacterMovementComponent* Movement = GetCharacterMovement();
    if (!Movement)
    {
        return;
    }

    // Dodge in the direction of current movement input; if no directional input is
    // held, dodge in the actor's facing direction.
    const float Forward = (bForwardDown ? 1.0f : 0.0f) - (bBackDown ? 1.0f : 0.0f);
    const float Right = (bRightDown ? 1.0f : 0.0f) - (bLeftDown ? 1.0f : 0.0f);

    FVector Direction(Forward, Right, 0.0f);
    if (Direction.IsNearlyZero())
    {
        const FRotator YawRotation(0.0f, GetActorRotation().Yaw, 0.0f);
        Direction = FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X);
    }
    Direction = Direction.GetSafeNormal();

    DodgeDirection = Direction;
    bDodgeing = true;
    bDodgeInvulnerable = true;
    DodgeTimer = DodgeDurationS;
    DodgeCooldownTimer = DodgeCooldownS;

    // Burst: apply the dodge velocity and cap the walk speed at the burst speed so the
    // burst is not overridden by the walk/run locomotion. UE 5.8.4 forces the burst speed
    // by setting Velocity directly (re-applied each tick while the burst is active, see
    // Tick) and capping MaxWalkSpeed at the burst speed.
    Movement->Velocity = DodgeDirection * DodgeSpeedCmS;
    Movement->MaxWalkSpeed = DodgeSpeedCmS;

    UE_LOG(LogTemp, Display,
        TEXT("TDD M1: dodge started (dir X=%.2f Y=%.2f)"),
        DodgeDirection.X, DodgeDirection.Y);
}

void ATDDAdannaCharacter::OnJumped_Implementation()
{
    ++JumpCount;
    Super::OnJumped_Implementation();
}

void ATDDAdannaCharacter::Landed(const FHitResult& Hit)
{
    ++LandCount;
    bJustLanded = true;
    Super::Landed(Hit);
}

void ATDDAdannaCharacter::AnimateProxy(float DeltaSeconds, float SpeedCmS, bool bFalling)
{
    // Only used by the proxy fallback when no skeletal mesh is available.
    const float NormalisedSpeed = FMath::Clamp(SpeedCmS / TDDWorldData::RunSpeedCmS, 0.0f, 1.0f);
    LocomotionPhase += DeltaSeconds * FMath::Lerp(2.0f, 11.0f, NormalisedSpeed);

    if (bFalling)
    {
        CurrentState = GetVelocity().Z > 0.0f ? TEXT("JUMP") : TEXT("LAND");
        if (AnimatedLimbs.Num() >= 4)
        {
            AnimatedLimbs[0]->SetRelativeRotation(FRotator(-18.0f, 0.0f, 0.0f));
            AnimatedLimbs[1]->SetRelativeRotation(FRotator(-18.0f, 0.0f, 0.0f));
            AnimatedLimbs[2]->SetRelativeRotation(FRotator(10.0f, 0.0f, 0.0f));
            AnimatedLimbs[3]->SetRelativeRotation(FRotator(-6.0f, 0.0f, 0.0f));
        }
    }
    else
    {
        CurrentState = SpeedCmS < 30.0f
            ? TEXT("IDLE")
            : (SpeedCmS > TDDWorldData::WalkSpeedCmS * 1.45f ? TEXT("RUN") : TEXT("WALK"));
        const float Swing = FMath::Sin(LocomotionPhase) * NormalisedSpeed * 28.0f;
        if (AnimatedLimbs.Num() >= 4)
        {
            AnimatedLimbs[0]->SetRelativeRotation(FRotator(Swing, 0.0f, 0.0f));
            AnimatedLimbs[1]->SetRelativeRotation(FRotator(-Swing, 0.0f, 0.0f));
            AnimatedLimbs[2]->SetRelativeRotation(FRotator(-Swing, 0.0f, 0.0f));
            AnimatedLimbs[3]->SetRelativeRotation(FRotator(Swing, 0.0f, 0.0f));
        }
    }
}

void ATDDAdannaCharacter::UpdateDebugHud(float SpeedCmS, bool bGrounded)
{
    NearbyInteraction.Empty();
    if (ForestLevel)
    {
        ForestLevel->TryGetNearbyInteraction(GetActorLocation(), NearbyInteraction);
    }

    const float RouteProgress = ForestLevel ? ForestLevel->GetRouteProgress(GetActorLocation()) : 0.0f;
    const float CameraDistanceM = FollowCamera && CameraBoom
        ? (FollowCamera->GetComponentLocation() - CameraBoom->GetComponentLocation()).Size() / 100.0f
        : TDDWorldData::CameraDistanceCm / 100.0f;
    const bool bCameraOccluded = CameraDistanceM < (TDDWorldData::CameraDistanceCm / 100.0f - 0.12f);

    FString Objective = ForestLevel
        ? ForestLevel->GetStagedObjective(RouteProgress)
        : FString(TDDWorldData::ObjectiveText);
    if (RouteProgress > 0.98f)
    {
        Objective = TEXT("ROUTE COMPLETE — Great Root Mother approach acknowledged");
    }

    const FString StateLine = bDodgeing
        ? TEXT("DODGE")
        : (bSprinting ? TEXT("RUN") : CurrentState);
    const int32 ObjectiveStage = ForestLevel ? ForestLevel->GetObjectiveStage(RouteProgress) : 0;
    const FString DodgeLine = bDodgeing
        ? TEXT("DODGE BURST")
        : (DodgeCooldownTimer > 0.0f
            ? FString::Printf(TEXT("DODGE CD %.1fs"), DodgeCooldownTimer)
            : TEXT("DODGE READY (Ctrl)"));

    if (GEngine)
    {
        const FString CharacterLine = bUsingSkeletalMesh
            ? TEXT("ADANNA (SKELETAL MESH)")
            : TEXT("ADANNA (PROXY FALLBACK)");
        const FString InteractionLine = NearbyInteraction.IsEmpty()
            ? TEXT("WASD move · Shift run · Space jump · E interact · Ctrl dodge · mouse look · Esc cursor")
            : FString::Printf(TEXT("E INTERACT — %s"), *NearbyInteraction);
        GEngine->AddOnScreenDebugMessage(
            1,
            0.0f,
            FColor(226, 214, 190),
            FString::Printf(
                TEXT("THE DISOBEDIENT DAUGHTER · PLAYABLE ADANNA M1\\n%s · FORBIDDEN FOREST\\n\\n"
                     "STATE %s    SPEED %.2f m/s    GROUNDED %s\\n"
                     "CAMERA %.2f m / %s    ROUTE %d%% (STAGE %d)    J/L/INT %d/%d/%d\\n\\n"
                     "OBJECTIVE %s\\n%s\\n%s"),
                *CharacterLine,
                *StateLine,
                SpeedCmS / 100.0f,
                bGrounded ? TEXT("YES") : TEXT("NO"),
                CameraDistanceM,
                bCameraOccluded ? TEXT("OCCLUDED") : TEXT("CLEAR"),
                FMath::RoundToInt(RouteProgress * 100.0f),
                ObjectiveStage,
                JumpCount,
                LandCount,
                InteractCount,
                *Objective,
                *InteractionLine,
                *DodgeLine));
    }
}

void ATDDAdannaCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    // Advance dodge timers and restore normal locomotion when the burst ends.
    if (bDodgeing)
    {
        DodgeTimer -= DeltaSeconds;
        UCharacterMovementComponent* Movement = GetCharacterMovement();
        if (Movement)
        {
            // Force the burst speed every tick: re-apply the burst velocity along the
            // dodge direction (direct Velocity assignment is the UE 5.8.4 mechanism that
            // keeps the burst from being overridden by input-driven locomotion; air
            // friction and braking decelerate naturally once the burst ends) and cap the
            // walk speed at the burst speed.
            if (DodgeTimer > 0.0f)
            {
                Movement->Velocity = DodgeDirection * DodgeSpeedCmS;
                Movement->MaxWalkSpeed = DodgeSpeedCmS;
            }
            else
            {
                bDodgeing = false;
                bDodgeInvulnerable = false;
                Movement->MaxWalkSpeed = bSprinting ? TDDWorldData::RunSpeedCmS : TDDWorldData::WalkSpeedCmS;
            }
        }
    }
    else if (DodgeCooldownTimer > 0.0f)
    {
        DodgeCooldownTimer -= DeltaSeconds;
    }

    ApplyMovementInput();
    const float SpeedCmS = GetVelocity().Size2D();
    const bool bGrounded = IsGrounded();

    // The skeletal mesh drives animation through UTDDAdannaAnimInstance; the proxy
    // fallback uses the manual limb animation.
    if (!bUsingSkeletalMesh)
    {
        AnimateProxy(DeltaSeconds, SpeedCmS, !bGrounded);
    }
    UpdateDebugHud(SpeedCmS, bGrounded);
}
