// TDD-Unit.Movement.InputBuffer (AC-24/25), TDD-Unit.Movement.Gait (AC-02/03/05),
// TDD-Unit.Traversal.FallbackResolution (AC-10) — pure cores, host + UE.

#include "Core/TDDGaitMath.h"
#include "Core/TDDInputBuffer.h"
#include "Core/TDDTraversalFallback.h"

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>

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
template <typename T>
bool Nearly(const T A, const T B, const T Tol)
{
    return std::fabs(A - B) <= Tol;
}
} // namespace

int main()
{
    using namespace TDD;
    using I = Input::ETDDIntent;

    // ---- AC-24: input buffer ----
    {
        Input::FTDDInputBuffer B;
        // single consumption
        B.Press(I::Dodge, 0.0f);
        Check(B.Consume(I::Dodge, 0.05f), "buffer: consume once");
        Check(!B.Consume(I::Dodge, 0.06f), "buffer: NOT consumable a second time");

        // exact expiry: window 0.20 -> 0.20 ok, 0.21 dropped
        B.Press(I::Dodge, 0.0f);
        Check(B.Consume(I::Dodge, 0.20f), "buffer: consume at exact window edge");
        B.Press(I::Dodge, 0.0f);
        Check(!B.Consume(I::Dodge, 0.2001f), "buffer: expired press is dropped, not consumed");

        // replace-not-queue: a second press refreshes the timestamp; single slot
        B.Press(I::Jump, 0.0f);
        B.Press(I::Jump, 0.10f); // replaces
        Check(B.Consume(I::Jump, 0.25f), "buffer: replacement valid at 0.25 (original 0.0 press would have expired)");
        Check(!B.Consume(I::Jump, 0.26f), "buffer: single slot — nothing queued behind the replacement");

        // non-bufferable intents are immediate
        B.Press(I::Move2D, 0.0f);
        Check(B.Consume(I::Move2D, 999.0f), "buffer: non-bufferable consumed same frame");
        Check(!B.Consume(I::Move2D, 999.0f), "buffer: non-bufferable single use");

        // clear-on-lock: Stagger clears Dodge+attacks, not Jump; Cinematic clears Dodge
        B.Press(I::Dodge, 0.0f);
        B.Press(I::Jump, 0.0f);
        B.Press(I::LightAttack, 0.0f);
        B.ApplyClearOnLock(Input::CLR_Stagger, 0.0f);
        Check(!B.IsBuffered(I::Dodge, 0.0f), "buffer: Stagger clears Dodge");
        Check(!B.IsBuffered(I::LightAttack, 0.0f), "buffer: Stagger clears attacks");
        Check(B.IsBuffered(I::Jump, 0.0f), "buffer: Stagger does NOT clear Jump");
        B.ApplyClearOnLock(Input::CLR_Cinematic, 0.0f);
        Check(B.IsBuffered(I::Jump, 0.0f), "buffer: Cinematic leaves Jump");
        B.ApplyClearOnLock(Input::CLR_Dead, 0.0f);
        Check(!B.IsBuffered(I::Jump, 0.0f), "buffer: Dead clears Jump (matrix)");

        // state lock table: Sprint drops attack buffering; Locomotion keeps it
        Check(Input::StateBuffersIntent("Locomotion", I::LightAttack), "buffer: Locomotion buffers attacks");
        Check(!Input::StateBuffersIntent("Sprint", I::LightAttack), "buffer: Sprint drops attacks");
        Check(Input::StateBuffersIntent("Sprint", I::Dodge), "buffer: Sprint keeps Dodge");
        Check(!Input::StateBuffersIntent("Idle", I::Sprint), "buffer: Sprint intent not buffered (window 0)");
    }

    // ---- AC-25: coyote ----
    {
        Check(Input::FTDDInputBuffer::CanAcceptJumpByCoyote(0.11f), "coyote: accept at 0.11 s");
        Check(Input::FTDDInputBuffer::CanAcceptJumpByCoyote(0.12f), "coyote: accept at 0.12 s boundary");
        Check(!Input::FTDDInputBuffer::CanAcceptJumpByCoyote(0.13f), "coyote: reject at 0.13 s");
        Check(!Input::FTDDInputBuffer::CanAcceptJumpByCoyote(-0.01f), "coyote: reject negative");
        Check(Input::FTDDInputBuffer::CanAcceptJumpByCoyote(0.0f), "coyote: on-ground ok");
    }

    // ---- AC-02/03/05: gait + vertical ----
    {
        using namespace Movement;
        Check(Nearly(GaitParams(ETDDGait::Run).Speed, 340.0f, 1e-3f), "gait: run 340");
        Check(Nearly(GaitParams(ETDDGait::Walk).Speed, 220.0f, 1e-3f), "gait: walk 220");

        // reach run speed within 1.0 s and land in 340 +/- 10
        float v = 0.0f;
        for (float t = 0.0f; t < 1.0f; t += 0.016f)
        {
            v = AccelerateToward(v, 340.0f, GaitParams(ETDDGait::Run).Acceleration, 0.016f);
        }
        Check(Nearly(v, 340.0f, 10.0f), "AC-02: run speed 340 +/-10 within 1.0 s");

        // stop from 340 within 0.25 s
        const float TStop = StopTime(340.0f, ETDDGait::Run);
        Check(TStop <= 0.25f && TStop > 0.0f, "AC-02: stop within 0.25 s");

        // 180 deg turn within 1.2 s (run)
        Check(TurnTime(180.0f, ETDDGait::Run) <= 1.2f, "AC-03: 180 deg within 1.2 s");
        Check(TurnTime(180.0f, ETDDGait::Walk) <= 1.2f, "AC-03: 180 deg within 1.2 s (walk)");

        // vertical profile 500 -> 0 -> -500 (AC-05)
        float vy = JumpInitialVy();
        bool bSawZero = false, bSawNeg = false;
        float h = 0.0f;
        for (float t = 0.0f; t < 1.0f; t += 0.016f)
        {
            h = IntegrateHeight(h, vy, 0.016f);
            vy = IntegrateVerticalVelocity(vy, 0.016f);
            if (std::fabs(vy) < 20.0f) { bSawZero = true; }
            if (vy <= -500.0f) { bSawNeg = true; break; }
        }
        Check(bSawZero, "AC-05: vy reaches ~0 (apex)");
        Check(bSawNeg, "AC-05: vy reaches -500 (return)");

        // slope: 25% (~14 deg) climbable, 35 deg not
        Check(SlopeFactor(14.0f) > 0.9f, "AC-04: 25% slope factor > 0.9");
        Check(Nearly(SlopeFactor(0.0f), 1.0f, 1e-5f), "slope: flat = 1.0");
        Check(SlopeFactor(35.0f) == 0.0f, "slope: 35 deg = 0 (non-walkable)");
        Check(SlopeFactor(-14.0f) == SlopeFactor(14.0f), "slope: symmetric");

        // camera pitch targets
        Check(Nearly(CameraPitchFor(ETDDGait::Walk, false), 0.0f, 1e-3f), "camera: walk 0");
        Check(Nearly(CameraPitchFor(ETDDGait::Run, false), -3.0f, 1e-3f), "camera: run -3");
        Check(Nearly(CameraPitchFor(ETDDGait::Run, true), -8.0f, 1e-3f), "camera: airborne -8");
    }

    // ---- AC-10: fallback resolution ----
    {
        using namespace Traversal;
        // budget 3: phase 1 success within window
        FTDDFallbackInput In;
        In.bPhase1AttemptSucceeds = true;
        In.Phase1AttemptTime = 0.20f;
        FTDDFallbackOutput O = ResolveFallback(In);
        Check(O.bTraversed && O.bPhase1 && O.AttemptsUsed == 1, "fallback: phase1 success, 1 attempt");
        Check(O.bResolutionLogged, "fallback: resolution logged (5)");

        // budget 3: phase 1 fails, phase 2 alternate resolves
        In = FTDDFallbackInput{};
        In.bPhase1AttemptSucceeds = false;
        In.bPhase2OptionAvailable = true;
        In.Phase2AttemptTime = 0.10f;
        O = ResolveFallback(In);
        Check(O.bTraversed && !O.bPhase1 && O.AttemptsUsed == 2, "fallback: phase2 alternate, 2 attempts");
        Check(O.bPhase2EvaluatedAllOptions, "fallback: 4a all options evaluated");
        Check(!O.bZeroWrite, "fallback: writes performed when resolved");

        // budget 1: phase 1 fails, no option -> 4b zero-writes
        In = FTDDFallbackInput{};
        In.AttemptBudget = 1;
        In.bPhase2OptionAvailable = false;
        O = ResolveFallback(In);
        Check(!O.bTraversed && O.bZeroWrite && O.AttemptsUsed == 1, "fallback: 4b zero-write, budget 1");
        Check(O.Writes.empty(), "fallback: zero-write performs NO writes");
        Check(O.bResolutionLogged, "fallback: zero-write still logs (5)");

        // budget 0: no attempts allowed at all -> immediate zero-write even if an option exists
        In = FTDDFallbackInput{};
        In.AttemptBudget = 0;
        In.bPhase2OptionAvailable = true;
        O = ResolveFallback(In);
        Check(!O.bTraversed && O.bZeroWrite && O.AttemptsUsed == 0 && O.bPhase2EvaluatedAllOptions,
              "fallback: budget 0 -> no attempts allowed -> zero-write (option evaluated per 4a, unused)");

        // budget 0, no option -> immediate zero-write, 0 attempts
        In = FTDDFallbackInput{};
        In.AttemptBudget = 0;
        O = ResolveFallback(In);
        Check(!O.bTraversed && O.bZeroWrite && O.AttemptsUsed == 0, "fallback: budget 0 no option -> zero-write, 0 attempts");

        // budget 1 with an available option but attempt already spent on phase 1
        In = FTDDFallbackInput{};
        In.AttemptBudget = 1;
        In.bPhase2OptionAvailable = true;
        O = ResolveFallback(In);
        Check(O.bZeroWrite && O.AttemptsUsed == 1, "fallback: budget 1 exhausted by phase1 -> 4b zero-write");
    }

    if (Failures != 0)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; " << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
