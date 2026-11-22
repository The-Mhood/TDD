#pragma once

// Pure combat timing core — the player kit windows (MEAD §4.2, CD-tunable
// defaults), dodge spec (M1 spec v1.4 §3.5) and the deterministic case-battery
// primitives (QUALITY §4). All values are data; this file holds the rules.

#include <cmath>

#include "Core/TDDSeededRandom.h"

namespace TDD
{
namespace Combat
{

/** Dodge spec data (M1 spec §3.5 FTDDDodgeSpec, gameplay seconds). */
struct FTDDDodgeSpec
{
    float DistanceCm = 300.0f;      // authored
    float Duration = 0.35f;
    float InvulnStart = 0.10f;      // i-frame window (AC-20: true 0.11–0.44)
    float InvulnEnd = 0.45f;
    float Cooldown = 0.5f;
    bool bRootMotion = true;
};

/** One attack's timing data (MEAD §4.2 defaults; per-attack overrides). */
struct FTDDAttackTiming
{
    float ActiveStart = 0.15f;      // first active frame (s into the montage)
    float ActiveEnd = 0.25f;
    float TotalDuration = 0.5f;
    /** Light: cancel allowed from the frame after the active start (chain). Heavy: never (commit). */
    bool bCancellable = true;
    float ChainWindowStart = 0.15f; // chain-into-next window (s)
    float ChainWindowEnd = 0.45f;
    bool bInterruptibleByDamage = false;
    std::int32_t ChainPosition = 1;        // 1..4 for the light chain
    std::int32_t ChainMax = 4;
};

// MEAD §4.2 kit defaults — data, not magic numbers.
inline FTDDAttackTiming MakeLightAttack(const std::int32_t ChainPosition) noexcept
{
    FTDDAttackTiming T;
    T.ChainPosition = ChainPosition;
    T.ChainMax = 4;
    T.bCancellable = true; // cancel from the frame after active start, into chain window
    return T;
}

inline FTDDAttackTiming MakeHeavyAttack() noexcept
{
    FTDDAttackTiming T;
    T.ActiveStart = 0.35f;
    T.ActiveEnd = 0.5f;
    T.TotalDuration = 1.0f;
    T.bCancellable = false; // no cancel after commit
    return T;
}

/**
 * Can an attack in progress be cancelled at TimeInMontage into the given target?
 * Rule (MEAD §4.2): light cancels only from the frame after the active start,
 * only while inside the chain window; heavy never cancels.
 */
inline bool CanCancelAttack(const FTDDAttackTiming& From, const FTDDAttackTiming& To,
                            const float TimeInMontage) noexcept
{
    if (!From.bCancellable)
    {
        return false;
    }
    if (TimeInMontage < From.ActiveStart)
    {
        return false; // before the frame after active start
    }
    if (TimeInMontage < From.ChainWindowStart || TimeInMontage > From.ChainWindowEnd)
    {
        return false; // outside the chain window
    }
    if (From.ChainPosition >= From.ChainMax && To.ChainPosition <= From.ChainPosition)
    {
        return false; // chain cap: light-4 does not chain back into the light chain
    }
    return true;
}

/** Block guard-ready after 0.08 s held (MEAD §4.2). */
inline bool IsGuardReady(const float TimeSinceBlockHeld) noexcept
{
    return TimeSinceBlockHeld >= 0.08f;
}

/** Parry window: the 0.15 s following guard-ready (MEAD §4.2). */
inline bool IsInParryWindow(const float TimeSinceBlockHeld) noexcept
{
    return TimeSinceBlockHeld >= 0.08f && TimeSinceBlockHeld <= 0.08f + 0.15f;
}

/** Dodge i-frames in gameplay time (M1 spec §3.5; AC-20 boundary points). */
inline bool IsDodgeInvulnerable(const float TimeInDodge, const FTDDDodgeSpec& Spec) noexcept
{
    return std::isfinite(TimeInDodge) &&
           TimeInDodge >= Spec.InvulnStart && TimeInDodge <= Spec.InvulnEnd;
}

/** Bounded hit-stop: active strictly before expiry; simulation resumes at expiry (never after). */
inline bool IsHitstopActive(const float TimeSinceHit, const float HitstopDuration) noexcept
{
    return HitstopDuration > 0.0f && TimeSinceHit >= 0.0f && TimeSinceHit < HitstopDuration;
}

/** 10-case deterministic combat battery (QUALITY §4). Deterministic by construction:
 *  fixed cases + fixed seed; the result log hash is compared across runs. */
struct FTDDCombatBatteryResult
{
    std::int32_t Cases = 0;
    std::int32_t Assertions = 0;
    std::int32_t Failures = 0;
    std::uint64_t LogHash = 0;
};

} // namespace Combat
} // namespace TDD
