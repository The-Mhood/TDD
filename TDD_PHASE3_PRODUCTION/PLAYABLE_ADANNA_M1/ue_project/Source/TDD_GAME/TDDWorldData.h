// GENERATED FILE — do not hand-edit. Source: PLAYABLE_ADANNA_M1/world.json
// Regenerate with: python3 scripts/generate_ue_world_data.py
// worldVersion: PLAYABLE_ADANNA_FOREST_M1_2026-11-19
// Classification: neutral gameplay/collision proxy; not approved story dimensions or final level art.
#pragma once

#include "CoreMinimal.h"

namespace TDDWorldData
{
struct FWaypoint { float XCm; float YCm; const TCHAR* Label; };
struct FObstacle
{
    const TCHAR* Id; const TCHAR* Type;
    float XCm; float YCm; float RadiusCm; float HeightCm;
    float TrunkRadiusCm; float CanopyRadiusCm; int32 Seed;
};
struct FInteraction { const TCHAR* Id; float XCm; float YCm; float RadiusCm; bool bFinal; const TCHAR* Message; };

static constexpr float MetresToCm = 100.0f;
static constexpr float BoundsMinXCm = -1800.000000f;
static constexpr float BoundsMaxXCm = 1800.000000f;
static constexpr float BoundsMinYCm = -2600.000000f;
static constexpr float BoundsMaxYCm = 6200.000000f;
static constexpr float SpawnXCm = 0.000000f;
static constexpr float SpawnYCm = -1800.000000f;
static constexpr float SpawnZCm = 92.0f; // capsule half-height above flat collision ground
static constexpr float RouteWidthCm = 340.000000f;
static constexpr float CharacterRadiusCm = 34.000000f;
static constexpr float CharacterHalfHeightCm = 88.0f; // neutral collision capsule half-height; NOT an approved character dimension
static constexpr float WalkSpeedCmS = 280.000000f;
static constexpr float RunSpeedCmS = 560.000000f;
static constexpr float JumpVelocityCmS = 640.000000f;
static constexpr float CameraDistanceCm = 440.000000f;
static constexpr float CameraCollisionPaddingCm = 35.000000f;

static const FWaypoint Waypoints[] = {
    { 0.000000f, -1800.000000f, TEXT("Threshold") },
    { 0.000000f, -800.000000f, TEXT("White-cloth boundary") },
    { -200.000000f, 200.000000f, TEXT("Root way") },
    { 100.000000f, 1200.000000f, TEXT("Stream crossing") },
    { -100.000000f, 2400.000000f, TEXT("Abandoned shrine") },
    { 200.000000f, 3600.000000f, TEXT("Duiker run") },
    { 0.000000f, 5000.000000f, TEXT("Great Root Mother approach") },
};
static constexpr int32 WaypointCount = 7;

static const FObstacle Obstacles[] = {
    { TEXT("CAMERA_PROBE_TREE"), TEXT("CAMERA_PROBE"), 0.000000f, -2100.000000f, 100.000000f, 850.000000f, 78.000000f, 220.000000f, 10 },
    { TEXT("BOUNDARY_POST_01"), TEXT("POST"), -200.000000f, -1600.000000f, 16.000000f, 220.000000f, 11.000000f, 0.000000f, 100 },
    { TEXT("BOUNDARY_POST_02"), TEXT("POST"), 200.000000f, -1600.000000f, 16.000000f, 220.000000f, 11.000000f, 0.000000f, 101 },
    { TEXT("BOUNDARY_POST_03"), TEXT("POST"), -160.000000f, 4900.000000f, 16.000000f, 220.000000f, 11.000000f, 0.000000f, 102 },
    { TEXT("BOUNDARY_POST_04"), TEXT("POST"), 160.000000f, 4900.000000f, 16.000000f, 220.000000f, 11.000000f, 0.000000f, 103 },
    { TEXT("GREAT_ROOT_MOTHER"), TEXT("GREAT_TREE"), 0.000000f, 5800.000000f, 320.000000f, 1800.000000f, 255.000000f, 700.000000f, 999 },
    { TEXT("FOREST_TREE_01"), TEXT("TREE"), -797.227811f, 2478.435216f, 64.622869f, 996.998583f, 52.497035f, 318.530027f, 759933 },
    { TEXT("FOREST_TREE_02"), TEXT("TREE"), -1543.559329f, -1174.632048f, 69.440204f, 1444.694432f, 50.468964f, 280.507644f, 615710 },
    { TEXT("FOREST_TREE_03"), TEXT("TREE"), 537.819382f, -69.799319f, 76.233413f, 892.040474f, 57.387905f, 280.902743f, 10936 },
    { TEXT("FOREST_TREE_04"), TEXT("TREE"), 1445.899957f, -1146.507435f, 56.963657f, 997.658902f, 49.658197f, 247.517129f, 278188 },
    { TEXT("FOREST_TREE_05"), TEXT("TREE"), -984.407101f, 4512.843537f, 59.758500f, 1231.718797f, 48.885958f, 207.298819f, 396275 },
    { TEXT("FOREST_TREE_06"), TEXT("TREE"), 1223.444203f, 2201.464370f, 83.553206f, 823.640138f, 76.559084f, 305.289253f, 246182 },
    { TEXT("FOREST_TREE_07"), TEXT("TREE"), 1308.197278f, 2813.432239f, 56.354669f, 1088.421590f, 48.839489f, 300.178857f, 205221 },
    { TEXT("FOREST_TREE_08"), TEXT("TREE"), -525.439449f, 3943.115059f, 83.411341f, 965.298337f, 59.237784f, 257.497587f, 43867 },
    { TEXT("FOREST_TREE_09"), TEXT("TREE"), -895.170848f, -1279.284214f, 59.547679f, 999.071537f, 42.904937f, 283.057543f, 836775 },
    { TEXT("FOREST_TREE_10"), TEXT("TREE"), -1564.548397f, 2427.727720f, 67.061021f, 1325.874136f, 50.060878f, 242.136752f, 672629 },
    { TEXT("FOREST_TREE_11"), TEXT("TREE"), 1506.487143f, 1751.730357f, 79.514813f, 1303.912971f, 72.531776f, 312.347195f, 578427 },
    { TEXT("FOREST_TREE_12"), TEXT("TREE"), -831.500001f, 1070.489732f, 66.882947f, 844.159604f, 51.201325f, 301.427096f, 687464 },
    { TEXT("FOREST_TREE_13"), TEXT("TREE"), -910.410182f, 5028.764105f, 62.121944f, 1015.949782f, 52.584628f, 289.313504f, 879938 },
    { TEXT("FOREST_TREE_14"), TEXT("TREE"), -1197.573369f, 1897.734811f, 92.411486f, 1322.067660f, 72.061563f, 317.657171f, 819541 },
    { TEXT("FOREST_TREE_15"), TEXT("TREE"), 1166.084418f, -583.720038f, 80.094586f, 990.089796f, 66.549444f, 229.834726f, 563892 },
    { TEXT("FOREST_TREE_16"), TEXT("TREE"), -1024.989989f, 2988.133334f, 93.412806f, 1189.458874f, 76.976099f, 290.149731f, 521827 },
    { TEXT("FOREST_TREE_17"), TEXT("TREE"), -519.820312f, 4815.015850f, 70.058387f, 1130.841354f, 52.232521f, 315.135708f, 553209 },
    { TEXT("FOREST_TREE_18"), TEXT("TREE"), 519.843109f, 2435.941073f, 77.839571f, 1203.628310f, 70.838194f, 207.695111f, 272202 },
    { TEXT("FOREST_TREE_19"), TEXT("TREE"), 1578.099624f, 2964.997608f, 72.043554f, 871.936073f, 52.242425f, 240.446803f, 334269 },
    { TEXT("FOREST_TREE_20"), TEXT("TREE"), 1069.598732f, 1942.865992f, 62.320622f, 868.941411f, 50.123620f, 237.170201f, 394529 },
    { TEXT("FOREST_TREE_21"), TEXT("TREE"), -777.839651f, -192.401542f, 56.468104f, 1391.548285f, 50.007556f, 313.519589f, 47501 },
    { TEXT("FOREST_TREE_22"), TEXT("TREE"), 909.984958f, 1579.404675f, 68.745503f, 1144.839744f, 61.941658f, 232.206713f, 484404 },
    { TEXT("FOREST_TREE_23"), TEXT("TREE"), 730.855792f, 2757.602091f, 82.320324f, 1403.797063f, 64.215930f, 260.283537f, 731405 },
    { TEXT("FOREST_TREE_24"), TEXT("TREE"), -1542.067489f, 3499.247861f, 55.502963f, 996.228738f, 43.309687f, 209.019843f, 352564 },
    { TEXT("FOREST_TREE_25"), TEXT("TREE"), -623.587118f, 122.086320f, 70.776892f, 1168.960813f, 52.385157f, 314.408953f, 839570 },
    { TEXT("FOREST_TREE_26"), TEXT("TREE"), 1552.537546f, -696.428797f, 57.033084f, 830.459558f, 40.456106f, 229.444987f, 879611 },
    { TEXT("FOREST_TREE_27"), TEXT("TREE"), -648.179767f, 5170.219002f, 71.715929f, 829.140140f, 57.492468f, 261.559541f, 36516 },
    { TEXT("FOREST_TREE_28"), TEXT("TREE"), -842.817438f, 4769.886774f, 66.534152f, 1366.032549f, 53.101692f, 187.676450f, 706830 },
    { TEXT("FOREST_ROCK_01"), TEXT("ROCK"), -285.287053f, 3550.398474f, 59.232861f, 81.214242f, 0.000000f, 0.000000f, 890828 },
    { TEXT("FOREST_ROCK_02"), TEXT("ROCK"), 261.564078f, 2444.102227f, 72.752043f, 90.147886f, 0.000000f, 0.000000f, 65244 },
    { TEXT("FOREST_ROCK_03"), TEXT("ROCK"), 346.419436f, -569.836285f, 82.242691f, 81.720003f, 0.000000f, 0.000000f, 652316 },
    { TEXT("FOREST_ROCK_04"), TEXT("ROCK"), -472.440623f, -220.919187f, 83.250969f, 50.880666f, 0.000000f, 0.000000f, 414879 },
    { TEXT("FOREST_ROCK_05"), TEXT("ROCK"), -941.887601f, -89.704649f, 49.973107f, 78.126963f, 0.000000f, 0.000000f, 836072 },
    { TEXT("FOREST_ROCK_06"), TEXT("ROCK"), 1365.223734f, 4268.840911f, 70.708286f, 81.340129f, 0.000000f, 0.000000f, 817766 },
    { TEXT("FOREST_ROCK_07"), TEXT("ROCK"), 568.391332f, -588.857963f, 67.039677f, 54.028108f, 0.000000f, 0.000000f, 174583 },
    { TEXT("FOREST_ROCK_08"), TEXT("ROCK"), -684.019577f, 1775.313855f, 73.302325f, 73.130205f, 0.000000f, 0.000000f, 11530 },
    { TEXT("FOREST_ROCK_09"), TEXT("ROCK"), -189.214798f, 3932.274991f, 73.642713f, 46.425658f, 0.000000f, 0.000000f, 576910 },
    { TEXT("FOREST_ROCK_10"), TEXT("ROCK"), 1210.787364f, 1386.598699f, 53.229108f, 68.260356f, 0.000000f, 0.000000f, 179457 },
    { TEXT("FOREST_ROCK_11"), TEXT("ROCK"), -334.041388f, 5003.051227f, 48.405170f, 53.901607f, 0.000000f, 0.000000f, 46471 },
    { TEXT("FOREST_ROCK_12"), TEXT("ROCK"), -1273.873321f, 2979.868453f, 52.413491f, 68.683283f, 0.000000f, 0.000000f, 34550 },
};
static constexpr int32 ObstacleCount = 46;

static const FInteraction Interactions[] = {
    { TEXT("boundary_waymarker"), 0.000000f, -1450.000000f, 160.000000f, false, TEXT("Boundary acknowledged. Follow the white cloth and laterite path.") },
    { TEXT("great_root_waymarker"), 0.000000f, 4900.000000f, 220.000000f, true, TEXT("Route complete: Great Root Mother approach acknowledged.") },
};
static constexpr int32 InteractionCount = 2;

static const TCHAR* ObjectiveText = TEXT("Follow the white cloth to the Great Root Mother");
} // namespace TDDWorldData
