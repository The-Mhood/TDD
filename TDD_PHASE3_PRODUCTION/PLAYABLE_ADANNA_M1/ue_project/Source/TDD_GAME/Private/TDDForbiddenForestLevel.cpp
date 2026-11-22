#include "TDDForbiddenForestLevel.h"

#include "TDDWorldData.h"
#include "Components/SceneComponent.h"
#include "Engine/Engine.h"
#include "Engine/StaticMesh.h"
#include "Materials/MaterialInterface.h"
#include "Materials/MaterialInstanceDynamic.h"
#include "Math/RandomStream.h"
#include "UObject/UObjectGlobals.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerStart.h"

namespace
{
    constexpr TCHAR ForestCubeMesh[] = TEXT("/Engine/BasicShapes/Cube.Cube");
    constexpr TCHAR ForestCylinderMesh[] = TEXT("/Engine/BasicShapes/Cylinder.Cylinder");
    constexpr TCHAR ForestSphereMesh[] = TEXT("/Engine/BasicShapes/Sphere.Sphere");
    constexpr TCHAR ForestConeMesh[] = TEXT("/Engine/BasicShapes/Cone.Cone");
    constexpr TCHAR ForestBasicShapeMaterial[] = TEXT("/Engine/BasicShapes/ForestBasicShapeMaterial.ForestBasicShapeMaterial");

    const FLinearColor ForestFloor(0.105f, 0.120f, 0.098f, 1.0f);
    const FLinearColor PathShoulder(0.185f, 0.125f, 0.083f, 1.0f);
    const FLinearColor Laterite(0.372f, 0.220f, 0.115f, 1.0f);
    const FLinearColor Bark(0.145f, 0.150f, 0.145f, 1.0f);
    const FLinearColor GreatBark(0.125f, 0.110f, 0.095f, 1.0f);
    const FLinearColor Canopy(0.115f, 0.185f, 0.145f, 1.0f);
    const FLinearColor Rock(0.220f, 0.225f, 0.212f, 1.0f);
    const FLinearColor Vegetation(0.100f, 0.205f, 0.125f, 1.0f);
    const FLinearColor WhiteCloth(0.760f, 0.740f, 0.665f, 1.0f);
    const FLinearColor Post(0.230f, 0.170f, 0.110f, 1.0f);
    const FLinearColor Waymarker(0.610f, 0.450f, 0.185f, 1.0f);
    const FLinearColor Pot(0.260f, 0.170f, 0.115f, 1.0f);
}

ATDDForbiddenForestLevel::ATDDForbiddenForestLevel()
{
    PrimaryActorTick.bCanEverTick = false;
    LevelRoot = CreateDefaultSubobject<USceneComponent>(TEXT("LevelRoot"));
    SetRootComponent(LevelRoot);

    RouteWaypointsCm.Reserve(TDDWorldData::WaypointCount);
    RouteSegmentStartsCm.Reserve(TDDWorldData::WaypointCount - 1);
    for (int32 i = 0; i < TDDWorldData::WaypointCount; ++i)
    {
        const TDDWorldData::FWaypoint& Wp = TDDWorldData::Waypoints[i];
        RouteWaypointsCm.Add(FVector2D(Wp.XCm, Wp.YCm));
    }
    for (int32 i = 0; i < TDDWorldData::WaypointCount - 1; ++i)
    {
        const FVector2D A = RouteWaypointsCm[i];
        const FVector2D B = RouteWaypointsCm[i + 1];
        const float DX = B.X - A.X;
        const float DY = B.Y - A.Y;
        RouteSegmentStartsCm.Add(RouteLengthCm);
        RouteLengthCm += FMath::Sqrt(DX * DX + DY * DY);
    }

    InteractionPointsCm.Reserve(TDDWorldData::InteractionCount);
    InteractionMessages.Reserve(TDDWorldData::InteractionCount);
    for (int32 i = 0; i < TDDWorldData::InteractionCount; ++i)
    {
        const TDDWorldData::FInteraction& Interaction = TDDWorldData::Interactions[i];
        InteractionPointsCm.Add(FVector(Interaction.XCm, Interaction.YCm, 0.0f));
        InteractionMessages.Add(FString(Interaction.Message));
    }

    RouteWidthCm = TDDWorldData::RouteWidthCm;
    MetresToCm = TDDWorldData::MetresToCm;
    ObjectiveText = TDDWorldData::ObjectiveText;
}

UInstancedStaticMeshComponent* ATDDForbiddenForestLevel::CreateInstancePool(
    const FName& Name, const TCHAR* MeshPath, bool bCollide, const FLinearColor& Tint)
{
    // Created at runtime in BeginPlay. Registration happens at the end of this function,
    // after the mesh/collision setup but before any AddInstance call: a component that is
    // not registered yet builds no physics state, which silently removed collision from
    // every tree, root and boundary post.
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
        UE_LOG(LogTemp, Warning, TEXT("TDD M1: missing engine shape mesh %s for %s"), MeshPath, *Name.ToString());
    }

    UMaterialInterface* BaseMaterial = LoadObject<UMaterialInterface>(nullptr, ForestBasicShapeMaterial);
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

void ATDDForbiddenForestLevel::AddBox(
    UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, const FVector& SizeCm, float YawDegrees) const
{
    if (!Pool) return;
    Pool->AddInstance(FTransform(
        FRotator(0.0f, YawDegrees, 0.0f),
        CentreCm,
        FVector(SizeCm.X / 100.0f, SizeCm.Y / 100.0f, SizeCm.Z / 100.0f)));
}

void ATDDForbiddenForestLevel::AddCylinder(
    UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm, float HeightCm) const
{
    if (!Pool) return;
    Pool->AddInstance(FTransform(
        FRotator::ZeroRotator,
        CentreCm,
        FVector(RadiusCm / 50.0f, RadiusCm / 50.0f, HeightCm / 100.0f)));
}

void ATDDForbiddenForestLevel::AddSphere(
    UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm) const
{
    if (!Pool) return;
    const float S = RadiusCm / 50.0f;  // Engine sphere radius is 50 cm
    Pool->AddInstance(FTransform(FRotator::ZeroRotator, CentreCm, FVector(S, S, S)));
}

void ATDDForbiddenForestLevel::AddCone(
    UInstancedStaticMeshComponent* Pool, const FVector& CentreCm, float RadiusCm, float HeightCm) const
{
    if (!Pool) return;
    Pool->AddInstance(FTransform(
        FRotator::ZeroRotator,
        CentreCm,
        FVector(RadiusCm / 50.0f, RadiusCm / 50.0f, HeightCm / 100.0f)));
}

float ATDDForbiddenForestLevel::DistanceToRouteCm(float XCm, float YCm) const
{
    float BestSq = TNumericLimits<float>::Max();
    for (int32 i = 0; i < TDDWorldData::WaypointCount - 1; ++i)
    {
        const TDDWorldData::FWaypoint& A = TDDWorldData::Waypoints[i];
        const TDDWorldData::FWaypoint& B = TDDWorldData::Waypoints[i + 1];
        const float ABx = B.XCm - A.XCm;
        const float ABy = B.YCm - A.YCm;
        const float APx = XCm - A.XCm;
        const float APy = YCm - A.YCm;
        const float Denom = ABx * ABx + ABy * ABy;
        const float T = Denom > 0.0f ? FMath::Clamp((APx * ABx + APy * ABy) / Denom, 0.0f, 1.0f) : 0.0f;
        const float DX = APx - ABx * T;
        const float DY = APy - ABy * T;
        BestSq = FMath::Min(BestSq, DX * DX + DY * DY);
    }
    return FMath::Sqrt(BestSq);
}

void ATDDForbiddenForestLevel::BuildRouteAndBoundary()
{
    UInstancedStaticMeshComponent* Ground = CreateInstancePool(TEXT("FOREST_GROUND"), ForestCubeMesh, true, ForestFloor);
    const float CentreY = 0.5f * (TDDWorldData::BoundsMinYCm + TDDWorldData::BoundsMaxYCm);
    const float SizeX = TDDWorldData::BoundsMaxXCm - TDDWorldData::BoundsMinXCm;
    const float SizeY = TDDWorldData::BoundsMaxYCm - TDDWorldData::BoundsMinYCm;
    AddBox(Ground, FVector(0.0f, CentreY, -10.0f), FVector(SizeX, SizeY, 20.0f), 0.0f);

    UInstancedStaticMeshComponent* Shoulders = CreateInstancePool(TEXT("LATERITE_SHOULDERS"), ForestCubeMesh, false, PathShoulder);
    UInstancedStaticMeshComponent* Path = CreateInstancePool(TEXT("LATERITE_PATH"), ForestCubeMesh, false, Laterite);
    // Path strips: Engine cube is 100 cm, so X=along-route and Y=width in the instance
    // scale; yaw aligns local X with the segment direction.
    for (int32 i = 0; i < TDDWorldData::WaypointCount - 1; ++i)
    {
        const TDDWorldData::FWaypoint& A = TDDWorldData::Waypoints[i];
        const TDDWorldData::FWaypoint& B = TDDWorldData::Waypoints[i + 1];
        const float DX = B.XCm - A.XCm;
        const float DY = B.YCm - A.YCm;
        const float Length = FMath::Sqrt(DX * DX + DY * DY) + 12.0f;
        const float Yaw = FMath::RadiansToDegrees(FMath::Atan2(DY, DX));
        const FVector Centre(0.5f * (A.XCm + B.XCm), 0.5f * (A.YCm + B.YCm), 0.0f);
        AddBox(Shoulders, Centre + FVector(0.0f, 0.0f, 1.5f), FVector(Length, RouteWidthCm + 54.0f, 3.0f), Yaw);
        AddBox(Path, Centre + FVector(0.0f, 0.0f, 3.5f), FVector(Length, RouteWidthCm, 4.0f), Yaw);
    }

    // PlayerStart is required for PIE/game mode possession once this runs in a saved map;
    // the generated map has no authored player start, so place one at the world spawn.
    if (UWorld* World = GetWorld())
    {
        // Presence test only: TActorIterator is positioned on the first suitable actor
        // by its own constructor, so its bool operator already answers "does one exist?".
        // The previous `for` broke on its first iteration, leaving `++It` unreachable;
        // V7 raises UnreachableCodeWarningLevel to Error (-Wunreachable-code-loop-increment).
        // TActorIterator's UE 5.8 constructor is (World, Class, Flags); the iterator's
        // operator bool reports whether a suitable actor exists.
        const bool bHasPlayerStart = static_cast<bool>(TActorIterator<APlayerStart>(
            World, APlayerStart::StaticClass(), EActorIteratorFlags::AllActors));
        if (!bHasPlayerStart)
        {
            FActorSpawnParameters SpawnInfo;
            SpawnInfo.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
            World->SpawnActor<APlayerStart>(
                FVector(TDDWorldData::SpawnXCm, TDDWorldData::SpawnYCm, TDDWorldData::SpawnZCm),
                FRotator(0.0f, 90.0f, 0.0f),
                SpawnInfo);
        }
    }

    UInstancedStaticMeshComponent* Rings = CreateInstancePool(TEXT("INTERACTION_RINGS"), ForestCylinderMesh, false, Waymarker);
    for (int32 i = 0; i < TDDWorldData::InteractionCount; ++i)
    {
        const TDDWorldData::FInteraction& Interaction = TDDWorldData::Interactions[i];
        AddCylinder(Rings, FVector(Interaction.XCm, Interaction.YCm, 6.0f), Interaction.RadiusCm * 0.46f, 5.0f);
    }
}

void ATDDForbiddenForestLevel::BuildForest()
{
    UInstancedStaticMeshComponent* Trunks = CreateInstancePool(TEXT("TREE_TRUNKS"), ForestCylinderMesh, true, Bark);
    UInstancedStaticMeshComponent* GreatTrunks = CreateInstancePool(TEXT("GREAT_ROOT_MOTHER_TRUNK"), ForestCylinderMesh, true, GreatBark);
    UInstancedStaticMeshComponent* Buttresses = CreateInstancePool(TEXT("BUTTRESS_ROOTS"), ForestCubeMesh, true, Bark);
    UInstancedStaticMeshComponent* Canopies = CreateInstancePool(TEXT("CANOPY"), ForestSphereMesh, false, Canopy);
    UInstancedStaticMeshComponent* Rocks = CreateInstancePool(TEXT("ROCKS"), ForestSphereMesh, true, Rock);
    UInstancedStaticMeshComponent* Understory = CreateInstancePool(TEXT("VEGETATION"), ForestConeMesh, false, Vegetation);
    UInstancedStaticMeshComponent* Posts = CreateInstancePool(TEXT("BOUNDARY_POSTS"), ForestCylinderMesh, true, Post);

    for (int32 i = 0; i < TDDWorldData::ObstacleCount; ++i)
    {
        const TDDWorldData::FObstacle& O = TDDWorldData::Obstacles[i];
        const FString Type(O.Type);
        if (Type == TEXT("ROCK"))
        {
            AddSphere(Rocks, FVector(O.XCm, O.YCm, O.HeightCm * 0.38f), O.RadiusCm * 0.85f);
            continue;
        }
        if (Type == TEXT("POST"))
        {
            AddCylinder(Posts, FVector(O.XCm, O.YCm, O.HeightCm * 0.5f), O.TrunkRadiusCm, O.HeightCm);
            continue;
        }

        const bool bGreatTree = Type == TEXT("GREAT_TREE");
        UInstancedStaticMeshComponent* TrunkPool = bGreatTree ? GreatTrunks : Trunks;
        AddCylinder(TrunkPool, FVector(O.XCm, O.YCm, O.HeightCm * 0.5f), O.TrunkRadiusCm, O.HeightCm);
        if (O.CanopyRadiusCm > 0.0f)
        {
            AddSphere(Canopies, FVector(O.XCm, O.YCm, O.HeightCm + O.CanopyRadiusCm * 0.22f), O.CanopyRadiusCm);
        }

        FRandomStream Stream(O.Seed > 0 ? O.Seed : 20261119 + i);
        const int32 RootCount = bGreatTree ? 8 : 4;
        for (int32 Root = 0; Root < RootCount; ++Root)
        {
            const float Angle = 2.0f * PI * (static_cast<float>(Root) / static_cast<float>(RootCount)) + Stream.FRandRange(-0.12f, 0.12f);
            const float Reach = O.TrunkRadiusCm * (bGreatTree ? 2.5f : 1.8f);
            const FVector RootCentre(
                O.XCm + FMath::Cos(Angle) * Reach * 0.55f,
                O.YCm + FMath::Sin(Angle) * Reach * 0.55f,
                FMath::Max(18.0f, O.TrunkRadiusCm * 0.12f));
            AddBox(
                Buttresses,
                RootCentre,
                FVector(Reach, FMath::Max(28.0f, O.TrunkRadiusCm * 0.30f), FMath::Max(36.0f, O.TrunkRadiusCm * 0.55f)),
                FMath::RadiansToDegrees(Angle));
        }
    }

    FRandomStream Stream(DeterministicSeed);
    int32 Placed = 0;
    int32 Tries = 0;
    while (Placed < 64 && Tries < 800)
    {
        ++Tries;
        const float XCm = Stream.FRandRange(TDDWorldData::BoundsMinXCm + 150.0f, TDDWorldData::BoundsMaxXCm - 150.0f);
        const float YCm = Stream.FRandRange(TDDWorldData::BoundsMinYCm + 150.0f, TDDWorldData::BoundsMaxYCm - 250.0f);
        const float RadiusCm = Stream.FRandRange(22.0f, 58.0f);
        if (DistanceToRouteCm(XCm, YCm) < RouteWidthCm * 0.55f + RadiusCm + 80.0f) continue;
        const float HeightCm = Stream.FRandRange(35.0f, 92.0f);
        AddCone(Understory, FVector(XCm, YCm, HeightCm * 0.5f), RadiusCm, HeightCm);
        ++Placed;
    }
}

void ATDDForbiddenForestLevel::BuildLandmarks()
{
    UInstancedStaticMeshComponent* Cloth = CreateInstancePool(TEXT("WHITE_CLOTH"), ForestCubeMesh, false, WhiteCloth);
    UInstancedStaticMeshComponent* Pots = CreateInstancePool(TEXT("ABANDONED_POTS"), ForestCylinderMesh, false, Pot);

    // White cloth is an approved recurring wayfinding rule. These are route markers, not canon placement.
    AddBox(Cloth, FVector(0.0f, -1600.0f, 188.0f), FVector(400.0f, 12.0f, 24.0f), 0.0f);
    AddBox(Cloth, FVector(0.0f, -800.0f, 155.0f), FVector(240.0f, 10.0f, 18.0f), 0.0f);
    AddBox(Cloth, FVector(0.0f, 4900.0f, 188.0f), FVector(320.0f, 12.0f, 24.0f), 0.0f);

    // Abandoned pots/shrines show prior use; this is a neutral collision-free blockout detail.
    AddCylinder(Pots, FVector(-160.0f, 2400.0f, 26.0f), 30.0f, 52.0f);
    AddCylinder(Pots, FVector(-55.0f, 2440.0f, 22.0f), 24.0f, 44.0f);
    AddCylinder(Pots, FVector(-95.0f, 2320.0f, 18.0f), 20.0f, 36.0f);
}

void ATDDForbiddenForestLevel::BeginPlay()
{
    Super::BeginPlay();
    BuildRouteAndBoundary();
    BuildForest();
    BuildLandmarks();
    UE_LOG(
        LogTemp,
        Display,
        TEXT("TDD M1: Forbidden Forest source blockout built with %d obstacles, %d route waypoints and %d interactables."),
        TDDWorldData::ObstacleCount,
        TDDWorldData::WaypointCount,
        TDDWorldData::InteractionCount);
}

float ATDDForbiddenForestLevel::GetRouteProgress(const FVector& WorldLocationCm) const
{
    if (RouteLengthCm <= 0.0f) return 0.0f;
    float BestDistanceSq = TNumericLimits<float>::Max();
    float BestDistanceAlongRoute = 0.0f;
    for (int32 i = 0; i < TDDWorldData::WaypointCount - 1; ++i)
    {
        const TDDWorldData::FWaypoint& A = TDDWorldData::Waypoints[i];
        const TDDWorldData::FWaypoint& B = TDDWorldData::Waypoints[i + 1];
        const float ABx = B.XCm - A.XCm;
        const float ABy = B.YCm - A.YCm;
        const float APx = WorldLocationCm.X - A.XCm;
        const float APy = WorldLocationCm.Y - A.YCm;
        const float LengthSq = ABx * ABx + ABy * ABy;
        const float T = LengthSq > 0.0f ? FMath::Clamp((APx * ABx + APy * ABy) / LengthSq, 0.0f, 1.0f) : 0.0f;
        const float DX = APx - ABx * T;
        const float DY = APy - ABy * T;
        const float DistanceSq = DX * DX + DY * DY;
        if (DistanceSq < BestDistanceSq)
        {
            BestDistanceSq = DistanceSq;
            BestDistanceAlongRoute = RouteSegmentStartsCm[i] + T * FMath::Sqrt(LengthSq);
        }
    }
    return FMath::Clamp(BestDistanceAlongRoute / RouteLengthCm, 0.0f, 1.0f);
}

bool ATDDForbiddenForestLevel::TryGetNearbyInteraction(const FVector& WorldLocationCm, FString& OutMessage) const
{
    for (int32 i = 0; i < TDDWorldData::InteractionCount; ++i)
    {
        const TDDWorldData::FInteraction& Interaction = TDDWorldData::Interactions[i];
        const float DX = WorldLocationCm.X - Interaction.XCm;
        const float DY = WorldLocationCm.Y - Interaction.YCm;
        if (DX * DX + DY * DY <= Interaction.RadiusCm * Interaction.RadiusCm)
        {
            OutMessage = FString(Interaction.Message);
            return true;
        }
    }
    return false;
}
