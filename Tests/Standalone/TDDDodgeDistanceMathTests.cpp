#include "Movement/TDDDodgeDistanceMath.h"

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>

namespace
{
int Failures = 0;
int Assertions = 0;

void Check(const bool bCondition, const char* const Description)
{
    ++Assertions;
    if (!bCondition)
    {
        ++Failures;
        std::cerr << "FAIL: " << Description << '\n';
    }
}

void CheckNear(const float Actual, const float Expected, const char* const Description)
{
    Check(std::fabs(Actual - Expected) <= 1.0e-5f, Description);
}
} // namespace

int main()
{
    using TDD::Movement::ResolveDodgeDistance;
    float Distance = -1.0f;

    Check(ResolveDodgeDistance(300.0f, false, 0.0f, 2.0f, Distance), "unobstructed input accepted");
    CheckNear(Distance, 300.0f, "unobstructed keeps authored distance");

    Check(ResolveDodgeDistance(300.0f, true, 120.0f, 2.0f, Distance), "blocked input accepted");
    CheckNear(Distance, 118.0f, "capsule contact subtracts only safety margin");

    Check(ResolveDodgeDistance(300.0f, true, 1.0f, 2.0f, Distance), "short contact accepted");
    CheckNear(Distance, 0.0f, "margin clamps resolved distance at zero");

    Check(ResolveDodgeDistance(100.0f, true, 200.0f, 2.0f, Distance), "late contact accepted");
    CheckNear(Distance, 100.0f, "resolved distance cannot exceed authored distance");

    Check(ResolveDodgeDistance(0.0f, false, 0.0f, 0.0f, Distance), "zero-length dodge accepted");
    CheckNear(Distance, 0.0f, "zero-length dodge remains zero");

    Check(!ResolveDodgeDistance(-1.0f, false, 0.0f, 2.0f, Distance), "negative authored distance rejected");
    CheckNear(Distance, 0.0f, "negative authored input yields safe zero output");

    Check(!ResolveDodgeDistance(100.0f, true, 20.0f, -1.0f, Distance), "negative margin rejected");
    CheckNear(Distance, 0.0f, "negative margin yields safe zero output");

    Check(!ResolveDodgeDistance(
              100.0f, true, std::numeric_limits<float>::quiet_NaN(), 2.0f, Distance),
          "NaN blocking contact rejected");
    CheckNear(Distance, 0.0f, "invalid contact yields safe zero output");

    Check(!ResolveDodgeDistance(
              std::numeric_limits<float>::infinity(), false, 0.0f, 2.0f, Distance),
          "infinite authored distance rejected");
    CheckNear(Distance, 0.0f, "non-finite authored input yields safe zero output");

    if (Failures != 0)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; "
                  << Failures << " failed\n";
        return EXIT_FAILURE;
    }

    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
