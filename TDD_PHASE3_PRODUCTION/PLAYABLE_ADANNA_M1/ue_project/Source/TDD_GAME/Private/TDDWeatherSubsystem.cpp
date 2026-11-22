// TDDWeatherSubsystem.cpp — Phase 1 wet/dry weather with gameplay consequences.
#include "TDDWeatherSubsystem.h"

#include "Subsystems/WorldSubsystem.h"

UTDDWeatherSubsystem::UTDDWeatherSubsystem()
{
    // UWorldSubsystem has no PrimaryComponentTick toggle; this subsystem
    // does not override Tick, so the empty base Tick incurs no per-frame cost.
}

void UTDDWeatherSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    UpdateFromWorldDay(0);
    UE_LOG(LogTemp, Display,
           TEXT("TDD WeatherSubsystem: initial season %s, rain %.2f, mud %.2f, water %.2f."),
           *FString(TDDWorld::SeasonName(Current.Season)), Current.RainIntensity, Current.MudLevel, Current.WaterLevel);
}

void UTDDWeatherSubsystem::UpdateFromWorldDay(int64 WorldDay)
{
    const TDDWorld::FWeatherState W = TDDWorld::ComputeWeather(WorldDay);
    Current.Season = W.Season;
    Current.RainIntensity = W.RainIntensity;
    Current.MudLevel = W.MudLevel;
    Current.WaterLevel = W.WaterLevel;
    Current.VisibilityFalloff = W.VisibilityFalloff;
    Current.VegetationGreenness = W.VegetationGreenness;
    Current.OutdoorActivitySuppression = W.OutdoorActivitySuppression;
}

float UTDDWeatherSubsystem::GetTraversalSlowdown() const
{
    // Mud slows foot travel; the penalty is bounded so travel stays possible.
    return FMath::Clamp(Current.MudLevel * 0.5f, 0.0f, 0.5f);
}

bool UTDDWeatherSubsystem::IsRiverCrossingBroken() const
{
    // At high water the foot crossing below Ahanwụ is broken; a canoe is required.
    return Current.WaterLevel >= 0.75f;
}
