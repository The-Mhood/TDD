#pragma once

#include <algorithm>
#include <cmath>

namespace TDD
{
namespace Movement
{

// Resolves the planar movement distance after a capsule sweep. The sweep's
// reported centre-at-contact distance already accounts for the capsule radius;
// only the safety margin is subtracted here.
inline bool ResolveDodgeDistance(
    const float AuthoredDistanceCm,
    const bool bBlocked,
    const float SweptCentreDistanceCm,
    const float SafetyMarginCm,
    float& OutResolvedDistanceCm) noexcept
{
    OutResolvedDistanceCm = 0.0f;

    if (!std::isfinite(AuthoredDistanceCm) || AuthoredDistanceCm < 0.0f ||
        !std::isfinite(SafetyMarginCm) || SafetyMarginCm < 0.0f)
    {
        return false;
    }

    if (!bBlocked)
    {
        OutResolvedDistanceCm = AuthoredDistanceCm;
        return true;
    }

    if (!std::isfinite(SweptCentreDistanceCm) || SweptCentreDistanceCm < 0.0f)
    {
        return false;
    }

    OutResolvedDistanceCm = std::clamp(
        SweptCentreDistanceCm - SafetyMarginCm,
        0.0f,
        AuthoredDistanceCm);
    return true;
}

} // namespace Movement
} // namespace TDD
