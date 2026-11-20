// WS5 Chapter 1 blockout route/layout contract tests.
#include "Core/TDDChapterRoute.h"

#include <cmath>
#include <cstdlib>
#include <iostream>

namespace
{
int Assertions = 0;
int Failures = 0;
void Check(bool Condition, const char* Description)
{
    ++Assertions;
    if (!Condition)
    {
        ++Failures;
        std::cerr << "FAIL: " << Description << '\n';
    }
}

TDD::Content::FTDDChapterLayout MakeChapterOne()
{
    using TDD::Content::FTDDChapterLayout;
    using TDD::Content::FTDDRoutePoint;
    FTDDChapterLayout L;
    L.MinX = -18.0; L.MaxX = 18.0;
    L.MinY = -26.0; L.MaxY = 62.0;
    L.PathWidth = 3.4;
    L.Spawn = { "Spawn", 0.0, -18.0 };
    L.Route = {
        { "Threshold", 0.0, -18.0 },
        { "White-cloth boundary", 0.0, -8.0 },
        { "Root way", -2.0, 2.0 },
        { "Stream crossing", 1.0, 12.0 },
        { "Abandoned shrine", -1.0, 24.0 },
        { "Duiker run", 2.0, 36.0 },
        { "Great Root Mother approach", 0.0, 50.0 }
    };
    return L;
}
}

int main()
{
    using namespace TDD::Content;
    const FTDDChapterLayout L = MakeChapterOne();
    const FTDDLayoutValidation V = ValidateChapterLayout(L);
    Check(V.bOk, "Chapter 1 M1 route fixture validates against bounds");
    Check(L.Route.size() == 7, "route preserves the seven authored M1 waypoints");
    Check(L.Route.front().X == L.Spawn.X && L.Route.front().Y == L.Spawn.Y,
          "spawn joins the first route waypoint");
    Check(RouteLength(L) > 65.0 && RouteLength(L) < 75.0,
          "route length is derived from waypoint geometry");

    FTDDChapterLayout Bad = L;
    Bad.Route[2].Label = Bad.Route[1].Label;
    Check(!ValidateChapterLayout(Bad).bOk, "duplicate waypoint labels are rejected");
    Bad = L;
    Bad.Route[0].X = -17.0; // corridor extends past minX with half-width 1.7
    Check(!ValidateChapterLayout(Bad).bOk, "route corridor must remain inside bounds");
    Bad = L;
    Bad.PathWidth = 0.0;
    Check(!ValidateChapterLayout(Bad).bOk, "non-positive corridor width is rejected");
    Bad = L;
    Bad.Spawn.X = 100.0;
    Check(!ValidateChapterLayout(Bad).bOk, "spawn outside bounds is rejected");
    Bad = L;
    Bad.Route.clear();
    Check(!ValidateChapterLayout(Bad).bOk, "empty route is rejected");

    if (Failures)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; "
                  << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
