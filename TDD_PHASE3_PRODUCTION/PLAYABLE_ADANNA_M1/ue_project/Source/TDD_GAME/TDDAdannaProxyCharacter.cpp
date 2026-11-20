#include "TDDAdannaProxyCharacter.h"

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
    constexpr TCHAR CubeMesh[] = TEXT("/Engine/BasicShapes/Cube.Cube");
    constexpr TCHAR CylinderMesh[] = TEXT("/Engine/BasicShapes/Cylinder.Cylinder");
    constexpr TCHAR SphereMesh[] = TEXT("/Engine/BasicShapes/Sphere.Sphere");
    constexpr TCHAR BasicShapeMaterial[] = TEXT("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial");

    // Palette-derived technical colours; not calibrated final materials.
    const FLinearColor Skin(0.263f, 0.176f, 0.153f, 1.0f);
    const FLinearColor Indigo(0.075f, 0.090f, 0.135f, 1.0f);
    const FLinearColor Leather(0.180f, 0.105f, 0.075f, 1.0f);
    const FLinearColor AgedBronze(0.390f, 0.270f, 0.125f, 1.0f);
    const FLinearColor Coral(0.480f, 0.155f, 0.110f, 1.0f);
    const FLinearColor Hair(0.025f, 0.026f, 0.030f, 1.0f);
    const FLinearColor Scar(0.410f, 0.255f, 0.205f, 1.0f);
}

ATDDAdannaProxyCharacter::ATDDAdannaProxyCharacter()
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

UStaticMeshComponent* ATDDAdannaProxyCharacter::CreatePart(
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

    UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, MeshPath);
    if (Mesh)
    {
        Part->SetStaticMesh(Mesh);
    }

    UMaterialInterface* BaseMaterial = LoadObject<UMaterialInterface>(nullptr, BasicShapeMaterial);
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

void ATDDAdannaProxyCharacter::BuildTechnicalProxy()
{
    // Approved identity locks are represented only as labelled rigid-part technical markers.
    // +Y is the character's anatomical left for this forward-X proxy.
    Torso = CreatePart(TEXT("PROXY_TORSO_INDIGO"), CubeMesh, FVector(0, 0, -8), FVector(0.48f, 0.27f, 0.70f), Indigo);
    CreatePart(TEXT("PROXY_LEATHER_CHEST_STRAP"), CubeMesh, FVector(8, 0, 5), FVector(0.12f, 0.29f, 0.58f), Leather, FRotator(0, 0, 18));
    CreatePart(TEXT("PROXY_INDIGO_HANDWOVEN_WRAP"), CubeMesh, FVector(0, 0, -42), FVector(0.48f, 0.28f, 0.34f), Indigo);

    Head = CreatePart(TEXT("PROXY_HEAD"), SphereMesh, FVector(0, 0, 52), FVector(0.21f, 0.21f, 0.25f), Skin);
    CreatePart(TEXT("PROXY_THIN_BRAIDS_HIGH_KNOT"), SphereMesh, FVector(0, 0, 74), FVector(0.13f, 0.13f, 0.13f), Hair);
    CreatePart(TEXT("PROXY_BRAID_CAP"), SphereMesh, FVector(0, 0, 64), FVector(0.22f, 0.22f, 0.11f), Hair);

    for (int32 Bead = 0; Bead < 5; ++Bead)
    {
        const FLinearColor BeadTint = (Bead % 2 == 0) ? AgedBronze : Coral;
        CreatePart(
            FName(*FString::Printf(TEXT("PROXY_LEFT_TEMPLE_CUFF_OR_BEAD_%02d"), Bead + 1)),
            SphereMesh,
            FVector(7.5f, 10.5f, 54.0f + Bead * 3.2f),
            FVector(0.025f, 0.025f, 0.025f),
            BeadTint);
    }
    CreatePart(TEXT("PROXY_LEFT_CHEEKBONE_DIAGONAL_SCAR"), CubeMesh, FVector(10, 10, 50), FVector(0.020f, 0.140f, 0.025f), Scar, FRotator(0, 0, 35));
    CreatePart(TEXT("PROXY_SPIRAL_BRONZE_PENDANT_MARKER"), SphereMesh, FVector(11, 0, 10), FVector(0.070f, 0.070f, 0.045f), AgedBronze);

    LeftArm = CreatePart(TEXT("PROXY_LEFT_ARM"), CylinderMesh, FVector(0, 28, 0), FVector(0.14f, 0.14f, 0.55f), Skin);
    RightArm = CreatePart(TEXT("PROXY_RIGHT_ARM"), CylinderMesh, FVector(0, -28, 0), FVector(0.14f, 0.14f, 0.55f), Skin);
    CreatePart(TEXT("PROXY_COILED_BRONZE_ARMLET_LEFT_ONLY"), CylinderMesh, FVector(0, 28, 19), FVector(0.16f, 0.16f, 0.085f), AgedBronze);

    LeftLeg = CreatePart(TEXT("PROXY_LEFT_LEG"), CylinderMesh, FVector(0, 10, -58), FVector(0.15f, 0.15f, 0.62f), Skin);
    RightLeg = CreatePart(TEXT("PROXY_RIGHT_LEG"), CylinderMesh, FVector(0, -10, -58), FVector(0.15f, 0.15f, 0.62f), Skin);
    CreatePart(TEXT("PROXY_LEFT_WRAP"), CubeMesh, FVector(0, 10, -78), FVector(0.18f, 0.18f, 0.24f), Indigo);
    CreatePart(TEXT("PROXY_RIGHT_WRAP"), CubeMesh, FVector(0, -10, -78), FVector(0.18f, 0.18f, 0.24f), Indigo);
    CreatePart(TEXT("PROXY_LEFT_FOOT"), CubeMesh, FVector(8, 10, -87), FVector(0.25f, 0.16f, 0.09f), Leather);
    CreatePart(TEXT("PROXY_RIGHT_FOOT"), CubeMesh, FVector(8, -10, -87), FVector(0.25f, 0.16f, 0.09f), Leather);
    // Approved cross-draw position only: a leather mount marker at the LEFT hip.
    // No blade geometry is built. Phase 1 restrictions forbid inventing blade design,
    // so the earlier steel "blade" box was removed rather than kept as a visual guess.
    CreatePart(TEXT("PROXY_LEFT_HIP_CROSS_DRAW_MOUNT_MARKER"), CubeMesh, FVector(-5, 15, -40), FVector(0.05f, 0.07f, 0.16f), Leather, FRotator(0, 0, 16));

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

void ATDDAdannaProxyCharacter::BeginPlay()
{
    Super::BeginPlay();
    BuildTechnicalProxy();

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

    for (TActorIterator<ATDDForbiddenForestLevel> It(GetWorld()); It; ++It)
    {
        ForestLevel = *It;
        break;
    }

    UE_LOG(LogTemp, Display, TEXT("TDD M1: Adanna rigid-part technical proxy ready; NOT the final character."));
}

void ATDDAdannaProxyCharacter::OnForwardPressed() { bForwardDown = true; }
void ATDDAdannaProxyCharacter::OnForwardReleased() { bForwardDown = false; }
void ATDDAdannaProxyCharacter::OnBackPressed() { bBackDown = true; }
void ATDDAdannaProxyCharacter::OnBackReleased() { bBackDown = false; }
void ATDDAdannaProxyCharacter::OnRightPressed() { bRightDown = true; }
void ATDDAdannaProxyCharacter::OnRightReleased() { bRightDown = false; }
void ATDDAdannaProxyCharacter::OnLeftPressed() { bLeftDown = true; }
void ATDDAdannaProxyCharacter::OnLeftReleased() { bLeftDown = false; }

void ATDDAdannaProxyCharacter::ApplyMovementInput()
{
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

void ATDDAdannaProxyCharacter::BindDefaultInput(UInputComponent* PlayerInputComponent)
{
    // Digital keys drive movement, so W/S and A/D are bound as press/release pairs that
    // feed signed axis state. BindAxisKey only suits true analog axes, bound below.
    // BindKey handlers must take no parameters; BindAxis handlers take one float.
    PlayerInputComponent->BindKey(EKeys::W, IE_Pressed, this, &ATDDAdannaProxyCharacter::OnForwardPressed);
    PlayerInputComponent->BindKey(EKeys::W, IE_Released, this, &ATDDAdannaProxyCharacter::OnForwardReleased);
    PlayerInputComponent->BindKey(EKeys::S, IE_Pressed, this, &ATDDAdannaProxyCharacter::OnBackPressed);
    PlayerInputComponent->BindKey(EKeys::S, IE_Released, this, &ATDDAdannaProxyCharacter::OnBackReleased);
    PlayerInputComponent->BindKey(EKeys::D, IE_Pressed, this, &ATDDAdannaProxyCharacter::OnRightPressed);
    PlayerInputComponent->BindKey(EKeys::D, IE_Released, this, &ATDDAdannaProxyCharacter::OnRightReleased);
    PlayerInputComponent->BindKey(EKeys::A, IE_Pressed, this, &ATDDAdannaProxyCharacter::OnLeftPressed);
    PlayerInputComponent->BindKey(EKeys::A, IE_Released, this, &ATDDAdannaProxyCharacter::OnLeftReleased);

    PlayerInputComponent->BindAxisKey(EKeys::MouseX, this, &ATDDAdannaProxyCharacter::Turn);
    PlayerInputComponent->BindAxisKey(EKeys::MouseY, this, &ATDDAdannaProxyCharacter::LookUp);

    PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Pressed, this, &ATDDAdannaProxyCharacter::JumpPressed);
    PlayerInputComponent->BindKey(EKeys::SpaceBar, IE_Released, this, &ATDDAdannaProxyCharacter::JumpReleased);
    PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Pressed, this, &ATDDAdannaProxyCharacter::SprintStart);
    PlayerInputComponent->BindKey(EKeys::LeftShift, IE_Released, this, &ATDDAdannaProxyCharacter::SprintStop);
    PlayerInputComponent->BindKey(EKeys::E, IE_Pressed, this, &ATDDAdannaProxyCharacter::Interact);
}

void ATDDAdannaProxyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);
    check(PlayerInputComponent);
    BindDefaultInput(PlayerInputComponent);
}

void ATDDAdannaProxyCharacter::MoveForward(float Value)
{
    if (!Controller || FMath::IsNearlyZero(Value)) return;
    const FRotator YawRotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
    AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::X), Value);
}

void ATDDAdannaProxyCharacter::MoveRight(float Value)
{
    if (!Controller || FMath::IsNearlyZero(Value)) return;
    const FRotator YawRotation(0.0f, Controller->GetControlRotation().Yaw, 0.0f);
    AddMovementInput(FRotationMatrix(YawRotation).GetUnitAxis(EAxis::Y), Value);
}

void ATDDAdannaProxyCharacter::Turn(float Value)
{
    AddControllerYawInput(Value);
}

void ATDDAdannaProxyCharacter::LookUp(float Value)
{
    AddControllerPitchInput(Value);
}

void ATDDAdannaProxyCharacter::SprintStart()
{
    bSprinting = true;
    GetCharacterMovement()->MaxWalkSpeed = TDDWorldData::RunSpeedCmS;
}

void ATDDAdannaProxyCharacter::SprintStop()
{
    bSprinting = false;
    GetCharacterMovement()->MaxWalkSpeed = TDDWorldData::WalkSpeedCmS;
}

void ATDDAdannaProxyCharacter::JumpPressed()
{
    Jump();
}

void ATDDAdannaProxyCharacter::JumpReleased()
{
    StopJumping();
}

void ATDDAdannaProxyCharacter::Interact()
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

void ATDDAdannaProxyCharacter::OnJumped_Implementation()
{
    ++JumpCount;
    Super::OnJumped_Implementation();
}

void ATDDAdannaProxyCharacter::Landed(const FHitResult& Hit)
{
    ++LandCount;
    Super::Landed(Hit);
}

void ATDDAdannaProxyCharacter::AnimateProxy(float DeltaSeconds, float SpeedCmS, bool bFalling)
{
    const float NormalisedSpeed = FMath::Clamp(SpeedCmS / TDDWorldData::RunSpeedCmS, 0.0f, 1.0f);
    LocomotionPhase += DeltaSeconds * FMath::Lerp(2.0f, 11.0f, NormalisedSpeed);

    if (bFalling)
    {
        CurrentState = GetVelocity().Z > 0.0f ? TEXT("JUMP") : TEXT("LAND");
        if (LeftArm) LeftArm->SetRelativeRotation(FRotator(-18.0f, 0.0f, 0.0f));
        if (RightArm) RightArm->SetRelativeRotation(FRotator(-18.0f, 0.0f, 0.0f));
        if (LeftLeg) LeftLeg->SetRelativeRotation(FRotator(10.0f, 0.0f, 0.0f));
        if (RightLeg) RightLeg->SetRelativeRotation(FRotator(-6.0f, 0.0f, 0.0f));
    }
    else
    {
        CurrentState = SpeedCmS < 30.0f
            ? TEXT("IDLE")
            : (SpeedCmS > TDDWorldData::WalkSpeedCmS * 1.45f ? TEXT("RUN") : TEXT("WALK"));
        const float Swing = FMath::Sin(LocomotionPhase) * NormalisedSpeed * 28.0f;
        if (LeftArm) LeftArm->SetRelativeRotation(FRotator(Swing, 0.0f, 0.0f));
        if (RightArm) RightArm->SetRelativeRotation(FRotator(-Swing, 0.0f, 0.0f));
        if (LeftLeg) LeftLeg->SetRelativeRotation(FRotator(-Swing, 0.0f, 0.0f));
        if (RightLeg) RightLeg->SetRelativeRotation(FRotator(Swing, 0.0f, 0.0f));
    }

    if (Torso)
    {
        const float Bob = bFalling ? 0.0f : FMath::Abs(FMath::Sin(LocomotionPhase)) * NormalisedSpeed * 2.5f;
        Torso->SetRelativeLocation(TorsoBaseLocation + FVector(0.0f, 0.0f, Bob));
    }
}

void ATDDAdannaProxyCharacter::UpdateDebugHud(float SpeedCmS, bool bGrounded)
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

    FString Objective = ForestLevel ? ForestLevel->GetObjectiveText() : FString(TDDWorldData::ObjectiveText);
    if (RouteProgress > 0.98f)
    {
        Objective = TEXT("ROUTE COMPLETE — Great Root Mother approach acknowledged");
    }

    if (GEngine)
    {
        const FString InteractionLine = NearbyInteraction.IsEmpty()
            ? TEXT("WASD move · Shift run · Space jump · E interact · mouse look · Esc cursor")
            : FString::Printf(TEXT("E INTERACT — %s"), *NearbyInteraction);
        GEngine->AddOnScreenDebugMessage(
            1,
            0.0f,
            FColor(226, 214, 190),
            FString::Printf(
                TEXT("THE DISOBEDIENT DAUGHTER · PLAYABLE ADANNA M1\nREAL-TIME INTEGRATION · FORBIDDEN FOREST BLOCKOUT · RIGGED TECHNICAL PROXY\n\nSTATE %s    SPEED %.2f m/s    GROUNDED %s\nCAMERA %.2f m / %s    ROUTE %d%%    J/L/INT %d/%d/%d\n\nOBJECTIVE %s\n%s\n\nRIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER · UE compile/cook/package NOT verified in sandbox"),
                *CurrentState,
                SpeedCmS / 100.0f,
                bGrounded ? TEXT("YES") : TEXT("NO"),
                CameraDistanceM,
                bCameraOccluded ? TEXT("OCCLUDED") : TEXT("CLEAR"),
                FMath::RoundToInt(RouteProgress * 100.0f),
                JumpCount,
                LandCount,
                InteractCount,
                *Objective,
                *InteractionLine));
    }
}

void ATDDAdannaProxyCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    ApplyMovementInput();
    const float SpeedCmS = GetVelocity().Size2D();
    const bool bGrounded = GetCharacterMovement() && GetCharacterMovement()->IsMovingOnGround();
    AnimateProxy(DeltaSeconds, SpeedCmS, !bGrounded);
    UpdateDebugHud(SpeedCmS, bGrounded);
}
