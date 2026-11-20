#include "AI/TDDTrainingEnemy.h"

#include "AIController.h"
#include "AI/TDDCombatBrainComponent.h"
#include "Combat/TDDCombatComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Player/TDDCharacterStateComponent.h"

ATDDTrainingEnemy::ATDDTrainingEnemy()
{
    PrimaryActorTick.bCanEverTick = false;
    AIControllerClass = AAIController::StaticClass();
    AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
    bUseControllerRotationYaw = false;
    GetCharacterMovement()->bOrientRotationToMovement = true;
    GetCharacterMovement()->MaxWalkSpeed = 180.0f;

    StateComponent = CreateDefaultSubobject<UTDDCharacterStateComponent>(TEXT("TDDState"));
    CombatComponent = CreateDefaultSubobject<UTDDCombatComponent>(TEXT("TDDCombat"));
    CombatBrain = CreateDefaultSubobject<UTDDCombatBrainComponent>(TEXT("TDDCombatBrain"));

    static ConstructorHelpers::FObjectFinder<UStaticMesh> CylinderMesh(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
    if (CylinderMesh.Succeeded())
    {
        GreyboxVisual = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("GreyboxVisual"));
        GreyboxVisual->SetupAttachment(GetCapsuleComponent());
        GreyboxVisual->SetStaticMesh(CylinderMesh.Object);
        GreyboxVisual->SetRelativeScale3D(FVector(0.75f, 0.75f, 1.8f));
        GreyboxVisual->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }
}
