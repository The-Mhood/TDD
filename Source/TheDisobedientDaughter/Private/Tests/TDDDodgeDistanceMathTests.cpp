#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "Movement/TDDDodgeDistanceMath.h"

#include <limits>

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDDodgeDistanceMathTest,
    "TDD.Movement.DodgeDistanceMath",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDDodgeDistanceMathTest::RunTest(const FString& Parameters)
{
    (void)Parameters;

    float ResolvedDistance = -1.0f;

    TestTrue(
        TEXT("An unobstructed sweep keeps the authored distance"),
        TDD::Movement::ResolveDodgeDistance(300.0f, false, 0.0f, 2.0f, ResolvedDistance));
    TestEqual(TEXT("Unobstructed distance"), ResolvedDistance, 300.0f);

    TestTrue(
        TEXT("A blocking capsule sweep resolves from centre contact minus margin"),
        TDD::Movement::ResolveDodgeDistance(300.0f, true, 120.0f, 2.0f, ResolvedDistance));
    TestEqual(TEXT("Capsule radius is not subtracted a second time"), ResolvedDistance, 118.0f);

    TestTrue(
        TEXT("A safety margin larger than contact distance clamps to zero"),
        TDD::Movement::ResolveDodgeDistance(300.0f, true, 1.0f, 2.0f, ResolvedDistance));
    TestEqual(TEXT("Resolved distance is non-negative"), ResolvedDistance, 0.0f);

    TestTrue(
        TEXT("Contact beyond the authored endpoint never extends the dodge"),
        TDD::Movement::ResolveDodgeDistance(100.0f, true, 200.0f, 2.0f, ResolvedDistance));
    TestEqual(TEXT("Resolved distance is capped at authored distance"), ResolvedDistance, 100.0f);

    TestFalse(
        TEXT("Negative authored distance is rejected"),
        TDD::Movement::ResolveDodgeDistance(-1.0f, false, 0.0f, 2.0f, ResolvedDistance));
    TestEqual(TEXT("Invalid input leaves a safe zero output"), ResolvedDistance, 0.0f);

    TestFalse(
        TEXT("NaN contact distance is rejected when a blocking hit is reported"),
        TDD::Movement::ResolveDodgeDistance(
            100.0f, true, std::numeric_limits<float>::quiet_NaN(), 2.0f, ResolvedDistance));
    TestEqual(TEXT("Invalid contact leaves a safe zero output"), ResolvedDistance, 0.0f);

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
