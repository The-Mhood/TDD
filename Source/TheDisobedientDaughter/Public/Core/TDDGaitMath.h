#pragma once

// Pure gait/locomotion math (M1 spec v1.4 §4 gaits, §5 vertical, AC-02/03/05).
// All values in cm/s and cm/s^2 unless noted. No UE, no allocation.

#include <cmath>
#include <cstdint>

namespace TDD
{
namespace Movement
{

enum class ETDDGait : std::uint8_t { Walk = 0, Run = 1, Count = 2 };

struct FTDDGaitParams
{
    float Speed = 0.0f;          // cm/s
    float Acceleration = 0.0f;   // cm/s^2
    float Braking = 0.0f;        // cm/s^2
    float TurnRateDeg = 0.0f;    // deg/s
    float StrideLengthCm = 0.0f;
    float StrideTime = 0.0f;     // s
    float CameraPitchDeg = 0.0f;
};

inline const FTDDGaitParams& GaitParams(const ETDDGait G) noexcept
{
    static const FTDDGaitParams Walk = { 220.0f, 1200.0f, 1800.0f, 450.0f, 80.0f, 0.45f,  0.0f };
    static const FTDDGaitParams Run  = { 340.0f, 1000.0f, 1500.0f, 380.0f, 130.0f, 0.30f, -3.0f };
    static const FTDDGaitParams Tables[static_cast<std::int32_t>(ETDDGait::Count)] = { Walk, Run };
    return Tables[static_cast<std::uint8_t>(G)];
}

/** Vertical params (AC-05). */
inline float JumpInitialVy() noexcept { return 500.0f; }   // cm/s
inline float Gravity() noexcept       { return 1500.0f; }   // cm/s^2
inline float AirHorizontalSpeed() noexcept { return 220.0f; }
inline float AirAcceleration() noexcept    { return 300.0f; }
inline float AirTurnRateDeg() noexcept     { return 150.0f; }

/** Gait for current speed: <15 walk, else run profile (sprint raises the
 *  run-profile target speed; the Sprint state, not the gait, owns it). */
inline ETDDGait GaitForSpeed(const float SpeedCmPerS) noexcept
{
    return SpeedCmPerS < 15.0f ? ETDDGait::Walk : ETDDGait::Run;
}

inline ETDDGait GaitForTarget(const bool bSprintIntent) noexcept
{
    return bSprintIntent ? ETDDGait::Run : ETDDGait::Walk;
}

/** Slope speed factor: full on flat, cos-damped to 0 at 35 deg (AC-04:
 *  ±25% slope = ~14 deg must be climbable, i.e. factor > 0). */
inline float SlopeFactor(const float PitchDeg) noexcept
{
    const float Abs = std::fabs(PitchDeg);
    if (!std::isfinite(Abs))
    {
        return 0.0f;
    }
    const float Max = 35.0f;
    if (Abs >= Max)
    {
        return 0.0f;
    }
    return std::cos(Abs * 3.14159265358979f / 180.0f);
}

/** Time to reach target speed from 0 (linear accel). */
inline float TimeToSpeed(const ETDDGait G, const float TargetCmPerS) noexcept
{
    const FTDDGaitParams P = GaitParams(G);
    return TargetCmPerS <= 0.0f ? 0.0f : TargetCmPerS / P.Acceleration;
}

/** Time to stop from speed v (braking). */
inline float StopTime(const float SpeedCmPerS, const ETDDGait G) noexcept
{
    const FTDDGaitParams P = GaitParams(G);
    return SpeedCmPerS <= 0.0f ? 0.0f : SpeedCmPerS / P.Braking;
}

/** Time to rotate `AngleDeg` at the gait's turn rate (AC-03: 180 deg <= 1.2 s). */
inline float TurnTime(const float AngleDeg, const ETDDGait G) noexcept
{
    const FTDDGaitParams P = GaitParams(G);
    return AngleDeg <= 0.0f ? 0.0f : AngleDeg / P.TurnRateDeg;
}

/** One Euler integration of vertical velocity (AC-05: 500 -> 0 -> -500). */
inline float IntegrateVerticalVelocity(const float Vy, const float Dt) noexcept
{
    return Vy - Gravity() * Dt;
}

inline float IntegrateHeight(const float HeightCm, const float Vy, const float Dt) noexcept
{
    return HeightCm + Vy * Dt;
}

inline float StrideTimeFor(const ETDDGait G) noexcept { return GaitParams(G).StrideTime; }
inline float CameraPitchFor(const ETDDGait G, const bool bInAir) noexcept
{
    return bInAir ? -8.0f : GaitParams(G).CameraPitchDeg;
}

/** Speed after `Dt` of acceleration toward target (capped). */
inline float AccelerateToward(const float Current, const float Target, const float Accel, const float Dt) noexcept
{
    if (Current < Target)
    {
        const float Next = Current + Accel * Dt;
        return Next > Target ? Target : Next;
    }
    const float Next = Current - Accel * Dt;
    return Next < Target ? Target : Next;
}

} // namespace Movement
} // namespace TDD
