#pragma once

// Deterministic PRNG for test batteries (TR-19 T2: reproducibility within the
// same platform/build/test conditions). splitmix64: well-defined 64-bit
// arithmetic, identical results across compilers and optimisation levels.
// NOT a crypto RNG; used only for seeded test fuzzing and weighted picks.

#include <cstdint>

namespace TDD
{

class FTDDBatteryRng
{
public:
    explicit FTDDBatteryRng(const std::uint64_t InSeed) noexcept : State(InSeed) {}

    /** Next pseudo-random 64-bit value. */
    std::uint64_t NextUint64() noexcept
    {
        State += 0x9E3779B97F4A7C15ULL;
        std::uint64_t Z = State;
        Z = (Z ^ (Z >> 30)) * 0xBF58476D1CE4E5B9ULL;
        Z = (Z ^ (Z >> 27)) * 0x94D049BB133111EBULL;
        return Z ^ (Z >> 31);
    }

    /** Uniform float in [0, 1). */
    float NextFloat() noexcept
    {
        return static_cast<float>(NextUint64() >> 40) * (1.0f / 16777216.0f);
    }

    /** Uniform integer in [0, Bound). */
    std::uint64_t NextUInt(const std::uint64_t Bound) noexcept
    {
        return Bound == 0 ? 0 : NextUint64() % Bound;
    }

    /** Signed float in [-Range, Range]. */
    float NextBounded(const float Range) noexcept
    {
        return (NextFloat() * 2.0f - 1.0f) * Range;
    }

private:
    std::uint64_t State;
};

} // namespace TDD
