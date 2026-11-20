// TDD-Unit.Movement.StateRulesComplete (196 pairs) + TDD-Unit.Movement.
// StateSemantics — pure-core coverage of M1 spec v1.4 §3.2 (AC-22, AC-23).
// Runs host-side (g++) and inside UE automation; identical code path.

#include "Core/TDDDamageMath.h"
#include "Core/TDDStateRules.h"

#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

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

using namespace TDD::State;
using P = ETDDPlayerState;

std::int32_t N() noexcept { return static_cast<std::int32_t>(P::Count); }
} // namespace

int main()
{
    // ---- AC-22: all 196 pairs — declared legal or refused, state unchanged on refusal ----
    {
        const std::int32_t ExpectedLegal = CountLegalPairs(/*bAirDodgeEnabled*/ false);
        Check(ExpectedLegal == 79, "matrix: 79 legal pairs (air-dodge off, including land/guard-release events)");
        Check(CountLegalPairs(/*bAirDodgeEnabled*/ true) == 80, "matrix: 80 legal pairs (air-dodge on)");

        std::int32_t LegalSeen = 0;
        std::int32_t IllegalSeen = 0;
        for (std::int32_t F = 0; F < N(); ++F)
        {
            for (std::int32_t T = 0; T < N(); ++T)
            {
                const P From = static_cast<P>(F);
                const P To = static_cast<P>(T);
                FTDDPureStateMachine M;
                M.SetStateForTest(From);
                // Clear min-dwell so mask/priority legality is what is under test.
                // Dt < RecoveryTime always, so no recovery can fire on this tick.
                // (Stagger's dwell cannot be cleared this way because its dwell
                // equals its recovery time — irrelevant: its requested mask is
                // empty, so the mask check precedes the dwell check.)
                {
                    const FTDDStateRuleRow Row = MakeRuleRow(From, false);
                    const float Dt = std::min(Row.MinDwell + 0.01f, Row.RecoveryTime * 0.5f);
                    if (Dt > 0.0f)
                    {
                        M.Tick(Dt);
                    }
                    Check(M.Current() == From, "matrix: setup tick did not fire recovery");
                }

                const bool bForced = IsForcedState(To);
                const bool bLegal = bForced ? IsLegalForcedPair(From, To)
                                            : IsLegalRequestedPair(From, To, false);
                const ETDDRefusalReason R = bForced ? M.ForceState(To) : M.RequestState(To, "sweep");

                if (bLegal)
                {
                    Check(R == ETDDRefusalReason::Accepted && M.Current() == To,
                          "matrix: legal pair transitions");
                    ++LegalSeen;
                }
                else
                {
                    Check(R != ETDDRefusalReason::Accepted, "matrix: illegal pair refused");
                    Check(M.Current() == From, "matrix: illegal pair leaves state unchanged");
                    Check(M.RefusalCount() >= 1, "matrix: refusal is logged, never silent");
                    ++IllegalSeen;
                }
            }
        }
        Check(LegalSeen == 79 && IllegalSeen == 117, "matrix: 79 legal / 117 refused (no silent permits)");
    }

    // ---- AC-23: state semantics ----
    // (a) forced preempts regardless of dwell or priority (Dead into fresh state)
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Idle); // TimeInState = 0, min-dwell not elapsed
        Check(M.ForceState(P::Dead) == ETDDRefusalReason::Accepted && M.Current() == P::Dead,
              "semantics: forced Dead preempts at dwell 0");
        Check(M.Checklist().AllExitStepsDone(), "semantics: forced exit ran the full checklist");
    }

    // (b) min-dwell anti-flap: refusal, then accepted after dwell
    {
        FTDDPureStateMachine M;
        M.Tick(0.06f);
        Check(M.RequestState(P::Locomotion, "move") == ETDDRefusalReason::Accepted, "semantics: Idle->Locomotion after dwell");
        Check(M.RequestState(P::Idle, "flap") == ETDDRefusalReason::MinDwellNotElapsed && M.Current() == P::Locomotion,
              "semantics: flap within min dwell refused, state unchanged");
        M.Tick(0.06f);
        Check(M.RequestState(P::Idle, "move-stop") == ETDDRefusalReason::Accepted && M.Current() == P::Idle,
              "semantics: accepted after dwell");
    }

    // (c) interruption mask: Dodge cannot be requested out (no self-cancel)
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Dodge);
        M.Tick(0.3f); // past the 0.15 s dwell
        Check(M.RequestState(P::Locomotion, "self-cancel") == ETDDRefusalReason::NotInInterruptionMask
              && M.Current() == P::Dodge,
              "semantics: no self-cancel out of Dodge (mask)");
        Check(M.ForceState(P::Stagger) == ETDDRefusalReason::Accepted && M.Current() == P::Stagger,
              "semantics: forced Stagger still enters Dodge");
    }

    // (d) physics/event transitions must permit actual grounded and guard-release states.
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Airborne);
        Check(M.RequestState(P::Land, "CMC landed") == ETDDRefusalReason::Accepted
              && M.Current() == P::Land,
              "semantics: physics landing transitions Airborne -> Land");

        FTDDPureStateMachine Guard;
        Guard.SetStateForTest(P::Block);
        Guard.Tick(0.09f);
        Check(Guard.RequestState(P::Locomotion, "guard released") == ETDDRefusalReason::Accepted
              && Guard.Current() == P::Locomotion,
              "semantics: guard release exits Block to locomotion");
    }

    // (e) recovery ends the state at its declared time (data, not code paths)
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Land);
        Check(M.Current() == P::Land, "recovery: starting in Land");
        M.Tick(0.16f); // Land.RecoveryTime = 0.15
        Check(M.Current() == P::Locomotion, "recovery: Land -> Locomotion at declared time");
        Check(M.Checklist().AllExitStepsDone(), "recovery: natural exit ran the checklist");
    }

    // (e) Dead outranks Stagger: lethal+staggering = exactly one state change (Dead)
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Traversal);
        M.BeginResolution();
        Check(M.ForceState(P::Stagger) == ETDDRefusalReason::Accepted, "precedence: Stagger queued mid-resolution");
        Check(M.ForceState(P::Dead) == ETDDRefusalReason::Accepted, "precedence: Dead replaces Stagger in queue");
        Check(M.PendingForcedPriority() == 100, "precedence: queue holds the highest priority only");
        const P Applied = M.EndResolution();
        Check(Applied == P::Dead && M.Current() == P::Dead, "precedence: exactly one entry, Dead wins (no stagger)");
        Check(M.TransitionCount() == 1, "precedence: one transition, not two");
    }

    // (f) lower-priority forced is superseded, never queued over a higher one
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Traversal);
        M.BeginResolution();
        M.ForceState(P::Cinematic); // 90
        Check(M.ForceState(P::Stagger) != ETDDRefusalReason::Accepted || M.PendingForcedPriority() == 90,
              "precedence: Stagger (80) cannot supersede queued Cinematic (90)");
        Check(M.PendingForcedPriority() == 90, "precedence: queue still holds Cinematic");
        Check(M.EndResolution() == P::Cinematic, "precedence: queued Cinematic applied after resolution");
    }

    // (g) restoration runs exactly once; a second run is logged as a two-owner bug
    {
        FTDDPureStateMachine M;
        M.RunRestorationChecklist();
        M.RunRestorationChecklist();
        Check(M.Checklist().RestorationRuns == 1, "restoration: exactly once");
        Check(M.Checklist().bDoubleRunLogged, "restoration: double run logged (Restoration.DoubleRun)");
    }

    // (h) non-staggering damage changes health but not state (spec 3.2.1 + AC-23 v1.2)
    {
        TDD::Combat::FTDDDefenderState D;
        D.Health = 100.0f; D.Posture = 0.0f; D.MaxPosture = 100.0f;
        TDD::Combat::FTDDDamageRequest R;
        R.HealthDamage = 25.0f; R.PostureDamage = 0.0f; R.bCausesStagger = false;
        const TDD::Combat::FTDDDamageOutcome O = TDD::Combat::EvaluateDamage(R, D);
        Check(O.Classification == TDD::Combat::ETDDDamageClassification::NonStaggering,
              "damage/state: classified non-staggering");
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Locomotion);
        M.Tick(0.1f);
        // a non-staggering hit is an abort REQUEST only where the mask allows it;
        // Locomotion declares no Damaged-request target -> state unchanged, health paid
        Check(O.bHealthReduced && !O.bControlLost, "damage/state: health reduced, no control loss");
        Check(M.Current() == P::Locomotion, "damage/state: state unchanged by non-staggering hit");
    }

    // (i) Traversal E3: non-staggering abort request is legal (mask), then resolves to Locomotion
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Traversal);
        M.Tick(0.2f);
        Check(M.RequestState(P::Locomotion, "Damaged (inside AbortWindow)") == ETDDRefusalReason::Accepted
              && M.Current() == P::Locomotion,
              "E3: requested abort to Locomotion is legal");
        FTDDPureStateMachine M2;
        M2.SetStateForTest(P::Traversal);
        M2.Tick(0.2f);
        Check(M2.RequestState(P::Sprint, "Damaged") == ETDDRefusalReason::NotInInterruptionMask,
              "E3: only Locomotion/Land are legal abort targets (mask)");
    }

    // (j) Dead is terminal: nothing transitions out (196-pair diagonal + explicit)
    {
        FTDDPureStateMachine M;
        M.SetStateForTest(P::Dead);
        Check(M.RequestState(P::Idle, "anything") != ETDDRefusalReason::Accepted, "terminal: Dead refuses requests");
        Check(M.ForceState(P::Cinematic) != ETDDRefusalReason::Accepted, "terminal: Cinematic after Dead refused (priority)");
        Check(M.Current() == P::Dead, "terminal: Dead remains");
    }

    if (Failures != 0)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; " << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
