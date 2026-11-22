// TDDOmegaValleyLevel.cpp — Phase 1 Ọmà-valley core level.
#include "TDDOmegaValleyLevel.h"

#include "Components/SceneComponent.h"

#include "TDDWorldLogic.h"
#include "TDDOmegaValleyData.h"
#include "Engine/Engine.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Math/RandomStream.h"
#include "UObject/UObjectGlobals.h"
#include "EngineUtils.h"

namespace
{
    constexpr TCHAR ValleyCubeMesh[] = TEXT("/Engine/BasicShapes/Cube.Cube");
    constexpr TCHAR ValleyCylinderMesh[] = TEXT("/Engine/BasicShapes/Cylinder.Cylinder");
    constexpr TCHAR ValleyBasicShapeMaterial[] = TEXT("/Engine/BasicShapes/ValleyBasicShapeMaterial.ValleyBasicShapeMaterial");

    const FLinearColor Farmland(0.20f, 0.30f, 0.16f, 1.0f);
    const FLinearColor River(0.16f, 0.28f, 0.42f, 1.0f);
    const FLinearColor Road(0.42f, 0.34f, 0.22f, 1.0f);
    const FLinearColor ValleyForestFloor(0.12f, 0.18f, 0.12f, 1.0f);
    const FLinearColor ValleyCanopy(0.10f, 0.24f, 0.15f, 1.0f);
    const FLinearColor Settlement(0.45f, 0.36f, 0.24f, 1.0f);
}

ATDDOmegaValleyLevel::ATDDOmegaValleyLevel()
{
    PrimaryActorTick.bCanEverTick = false;
    LevelRoot = CreateDefaultSubobject<USceneComponent>(TEXT("LevelRoot"));
    SetRootComponent(LevelRoot);
}

UInstancedStaticMeshComponent* ATDDOmegaValleyLevel::CreateInstancePool(
    const FName& Name, const TCHAR* MeshPath, bool bCollide, const FLinearColor& Tint)
{
    UInstancedStaticMeshComponent* Pool = NewObject<UInstancedStaticMeshComponent>(this, Name);
    Pool->SetupAttachment(LevelRoot);
    Pool->SetMobility(EComponentMobility::Movable);

    UStaticMesh* Mesh = LoadObject<UStaticMesh>(nullptr, MeshPath);
    if (Mesh)
    {
        Pool->SetStaticMesh(Mesh);
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("TDD Valley: missing engine shape mesh %s for %s"), MeshPath, *Name.ToString());
    }

    UMaterialInterface* BaseMaterial = LoadObject<UMaterialInterface>(nullptr, ValleyBasicShapeMaterial);
    if (BaseMaterial)
    {
        UMaterialInstanceDynamic* TintMaterial = UMaterialInstanceDynamic::Create(BaseMaterial, this);
        TintMaterial->SetVectorParameterValue(TEXT("Color"), Tint);
        Pool->SetMaterial(0, TintMaterial);
    }

    if (bCollide)
    {
        Pool->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
        Pool->SetCollisionObjectType(ECC_WorldStatic);
        Pool->SetCollisionResponseToAllChannels(ECR_Block);
    }
    else
    {
        Pool->SetCollisionEnabled(ECollisionEnabled::NoCollision);
    }
    Pool->SetGenerateOverlapEvents(false);
    Pool->SetCastShadow(true);

    AddInstanceComponent(Pool);
    Pool->RegisterComponent();
    InstancePools.Add(Pool);
    return Pool;
}

void ATDDOmegaValleyLevel::AddBox(
    UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, const FVector& SizeCm, float YawDegrees) const
{
    if (!Pool) return;
    Pool->AddInstance(FTransform(
        FRotator(0.0f, YawDegrees, 0.0f),
        CentreCm,
        FVector(SizeCm.X / 100.0f, SizeCm.Y / 100.0f, SizeCm.Z / 100.0f)));
}

void ATDDOmegaValleyLevel::BuildGround()
{
    UInstancedStaticMeshComponent* Ground = CreateInstancePool(TEXT("VALLEY_GROUND"), ValleyCubeMesh, true, Farmland);
    // Region bounds are Design-editable data (omega_valley.json).
    const float CentreY = 0.5f * (TDDOmegaValleyData::RegionMinYCm + TDDOmegaValleyData::RegionMaxYCm);
    const float SizeX = TDDOmegaValleyData::RegionMaxXCm - TDDOmegaValleyData::RegionMinXCm;
    const float SizeY = TDDOmegaValleyData::RegionMaxYCm - TDDOmegaValleyData::RegionMinYCm;
    const float CentreX = 0.5f * (TDDOmegaValleyData::RegionMinXCm + TDDOmegaValleyData::RegionMaxXCm);
    AddBox(Ground, FVector(CentreX, CentreY, -10.0f), FVector(SizeX, SizeY, 20.0f), 0.0f);
}

void ATDDOmegaValleyLevel::BuildRiver()
{
    UInstancedStaticMeshComponent* RiverPool = CreateInstancePool(TEXT("OMA_RIVER"), ValleyCubeMesh, true, River);
    // The Ọmà runs north-south through the region along X=0 (metres), between
    // and beyond the settlements. A wide, navigable strip.
    AddBox(RiverPool, FVector(TDDOmegaValleyData::RiverXCm,
                              0.5f * (TDDOmegaValleyData::RiverTopYCm + TDDOmegaValleyData::RiverBottomYCm), 6.0f),
           FVector(TDDOmegaValleyData::RiverWidthCm,
                   FMath::Abs(TDDOmegaValleyData::RiverTopYCm - TDDOmegaValleyData::RiverBottomYCm), 12.0f), 0.0f);
}

void ATDDOmegaValleyLevel::BuildRoad()
{
    UInstancedStaticMeshComponent* RoadPool = CreateInstancePool(TEXT("ROAD"), ValleyCubeMesh, true, Road);
    // The road/canoe spine from Ahanwụ to Ọmà Ukwu along the river; width is
    // Design-editable data.
    const float RoadSpanX = TDDOmegaValleyData::Settlements[1].XCm - TDDOmegaValleyData::Settlements[0].XCm;
    const float RoadCentreX = 0.5f * (TDDOmegaValleyData::Settlements[0].XCm + TDDOmegaValleyData::Settlements[1].XCm);
    AddBox(RoadPool, FVector(RoadCentreX, 0.0f, 14.0f),
           FVector(RoadSpanX, TDDOmegaValleyData::RouteWidthCm, 28.0f), 0.0f);
}

void ATDDOmegaValleyLevel::BuildForest()
{
    // The local pool pointers must NOT shadow the anonymous-namespace tint
    // constants (ValleyForestFloor / ValleyCanopy): the tint arguments below
    // resolve to the FLinearColor constants, not to the component pointers.
    UInstancedStaticMeshComponent* ForestFloorPool = CreateInstancePool(TEXT("FOREST_FLOOR"), ValleyCubeMesh, true, ValleyForestFloor);
    UInstancedStaticMeshComponent* ForestCanopyPool = CreateInstancePool(TEXT("FOREST_CANOPY"), ValleyCylinderMesh, false, ValleyCanopy);

    // A forest patch at the Ezi-na-Oke edge of the Phase-1 core; data-driven.
    const float FX = TDDOmegaValleyData::ForestCentreXCm;
    const float FY = TDDOmegaValleyData::ForestCentreYCm;
    const float ForestHalf = TDDOmegaValleyData::ForestSizeCm * 0.5f;
    AddBox(ForestFloorPool, FVector(FX, FY, 6.0f),
           FVector(TDDOmegaValleyData::ForestSizeCm, TDDOmegaValleyData::ForestSizeCm, 12.0f), 0.0f);

    FRandomStream Stream(TDDOmegaValleyData::ForestSeed);
    int32 Placed = 0;
    int32 Tries = 0;
    while (Placed < TDDOmegaValleyData::ForestTreeCount && Tries < 500)
    {
        ++Tries;
        const float XCm = FMath::Abs(Stream.FRandRange(FX - ForestHalf * 0.46f, FX + ForestHalf * 0.46f));
        const float YCm = Stream.FRandRange(FY - ForestHalf * 0.42f, FY + ForestHalf * 0.42f);
        const float RadiusCm = Stream.FRandRange(30.0f, 70.0f);
        const float HeightCm = Stream.FRandRange(200.0f, 420.0f);
        // Engine cylinder radius is 50 cm.
        ForestCanopyPool->AddInstance(FTransform(FRotator::ZeroRotator, FVector(XCm, YCm, HeightCm * 0.5f),
                                       FVector(RadiusCm / 50.0f, RadiusCm / 50.0f, HeightCm / 100.0f)));
        ++Placed;
    }
}

void ATDDOmegaValleyLevel::PlaceSettlements()
{
    UWorld* World = GetWorld();
    if (!World)
    {
        return;
    }

    // Construct only the Phase-1 build target (Ahanwụ + Ọmà Ukwu). Ihiala is
    // regional registry data, not a Phase-1 construction.
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleyPhase1ConstructedSettlements())
    {
        const FVector Location = FVector(S.X * MetresToCm, S.Y * MetresToCm, 0.0f);
        FActorSpawnParameters Info;
        Info.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
        if (ATDDSettlementZone* Zone = World->SpawnActor<ATDDSettlementZone>(Location, FRotator::ZeroRotator, Info))
        {
            Zone->SetSettlementId(FName(S.Id.c_str()));
            Zone->SetSettlementName(S.Name.c_str());
            Settlements.Add(Zone);
        }
    }
}

void ATDDOmegaValleyLevel::BeginPlay()
{
    Super::BeginPlay();
    BuildGround();
    BuildRiver();
    BuildRoad();
    BuildForest();
    PlaceSettlements();

    UE_LOG(LogTemp, Display,
           TEXT("TDD OmegaValleyLevel: built Phase-1 core with %d constructed settlements (Ahanwụ, Ọmà Ukwu), "
                "Ọmà river, road spine and forest."),
           Settlements.Num());
}

void ATDDOmegaValleyLevel::RefreshSettlements(int64 WorldDay, float TimeOfDay)
{
    for (ATDDSettlementZone* Zone : Settlements)
    {
        if (Zone)
        {
            Zone->RefreshPopulation(WorldDay, TimeOfDay);
        }
    }
}
