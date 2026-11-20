// TDD-Unit.AI.TokenPolicy (ADR-0006) + TDD-Unit.AI.PhaseSelectorWeights
// (ADR-0107) + target selection — pure AI cores, host + UE.

#include "AI/TDDAIPureCore.h"

#include <cstdlib>
#include <iostream>
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
} // namespace

namespace
{
using namespace TDD::AI;

std::vector<std::int32_t> RunTokenSim(const FTDDTokenPolicySettings& S, const int Frames)
{
    FTDDAttackTokenPolicy P(S);
    std::vector<FTDDEnemyCandidate> Roster;
    for (std::int32_t I = 0; I < 6; ++I)
    {
        FTDDEnemyCandidate E;
        E.Id = I;
        Roster.push_back(E);
    }
    P.SetRoster(Roster);

    std::vector<std::int32_t> Sequence;
    std::int32_t MaxConcurrent = 0;
    const float Dt = 0.016f;
    for (int F = 0; F < Frames; ++F)
    {
        const float Now = F * Dt;
        const std::int32_t G = P.GrantNext(Now);
        if (G >= 0)
        {
            Sequence.push_back(G);
            // a grantee must never already hold a token
            bool bHolder = false;
            for (const FTDDEnemyCandidate& E : P.Roster())
            {
                if (E.Id == G && E.bHoldingToken && E.TokenGrantedAt != Now)
                {
                    bHolder = true;
                }
            }
            Check(!bHolder, "token: no double-grant to a holder");
        }
        MaxConcurrent = std::max(MaxConcurrent, P.ActiveHolders());
        Sequence.push_back(MaxConcurrent); // interleaved for determinism compare
    }
    return Sequence;
}

FTDDBossPhaseGraph MakeRootMotherGraph()
{
    FTDDBossPhaseGraph G;
    FTDDPhaseDefinition P1;
    P1.PhaseName = "Roots";
    FTDDPhaseTransition T1;
    T1.Kind = ETDDTransitionKind::HealthPct;
    T1.Threshold = 0.55f;
    T1.TargetPhase = "Bloom";
    P1.Transitions.push_back(T1);
    FTDDPhaseTransition T2;
    T2.Kind = ETDDTransitionKind::ElapsedSec;
    T2.Threshold = 100.0f;
    T2.TargetPhase = "Bloom";
    P1.Transitions.push_back(T2);
    P1.MusicState = "Music.Boss.Ch01.Phase1";
    G.Phases.push_back(P1);

    FTDDPhaseDefinition P2;
    P2.PhaseName = "Bloom";
    FTDDPhaseTransition T3;
    T3.Kind = ETDDTransitionKind::PoiseBreak;
    T3.TargetPhase = "Rage";
    P2.Transitions.push_back(T3);
    G.Phases.push_back(P2);

    FTDDPhaseDefinition P3;
    P3.PhaseName = "Rage";
    FTDDPhaseTransition T4;
    T4.Kind = ETDDTransitionKind::HealthPct;
    T4.Threshold = 0.0f;
    T4.TargetPhase = "Defeat";
    P3.Transitions.push_back(T4);
    G.Phases.push_back(P3);

    FTDDPhaseDefinition P4;
    P4.PhaseName = "Defeat";
    G.Phases.push_back(P4);

    G.EntryPhase = "Roots";
    G.DefeatPhase = "Defeat";
    G.TerminalPhases.push_back("Defeat");
    return G;
}
} // namespace

int main()
{
    // ---- TDD-Unit.AI.TokenPolicy ----
    {
        FTDDTokenPolicySettings S;
        S.MaxConcurrentAttackers = 2;
        S.TokenTTL = 3.0f;
        S.PerEnemyCooldown = 2.5f;

        const int Frames = static_cast<int>(60.0f / 0.016f); // 60 s
        const std::vector<std::int32_t> A = RunTokenSim(S, Frames);
        const std::vector<std::int32_t> B = RunTokenSim(S, Frames);

        Check(A == B, "token: deterministic (identical runs -> identical sequences)");

        FTDDAttackTokenPolicy P(S);
        std::vector<FTDDEnemyCandidate> Roster;
        for (std::int32_t I = 0; I < 6; ++I)
        {
            FTDDEnemyCandidate E;
            E.Id = I;
            Roster.push_back(E);
        }
        P.SetRoster(Roster);
        std::int32_t MaxConcurrent = 0;
        for (int F = 0; F < Frames; ++F)
        {
            P.GrantNext(F * 0.016f);
            MaxConcurrent = std::max(MaxConcurrent, P.ActiveHolders());
        }
        Check(MaxConcurrent <= 2, "token: concurrent attackers never exceed the cap (60 s, 6 enemies)");
        Check(P.DistinctGrantees() == 6, "token: fairness — all 6 enemies granted over 60 s");

        // Explicit TTL/cooldown behavior with one enemy: expiry frees the cap,
        // but that enemy remains unavailable until its cooldown elapses.
        FTDDTokenPolicySettings One;
        One.MaxConcurrentAttackers = 1;
        One.TokenTTL = 1.0f;
        One.PerEnemyCooldown = 2.0f;
        FTDDAttackTokenPolicy Timed(One);
        FTDDEnemyCandidate Only; Only.Id = 91;
        Timed.SetRoster({ Only });
        Check(Timed.GrantNext(0.0f) == 91, "token: initial grant");
        Check(Timed.GrantNext(0.5f) == -1 && Timed.ActiveHolders() == 1,
              "token: holder remains active before TTL");
        Check(Timed.GrantNext(1.1f) == -1 && Timed.ActiveHolders() == 0,
              "token: TTL expires holder, cooldown still blocks grant");
        Check(Timed.GrantNext(2.1f) == 91,
              "token: per-enemy cooldown elapses and permits next grant");
        Timed.Reset();
        Check(Timed.Roster().size() == 1 && Timed.Roster()[0].Id == 91
              && Timed.ActiveHolders() == 0,
              "token: reset clears policy state but preserves roster identity");
    }

    // ---- TDD-Unit.AI.PhaseSelectorWeights / ADR-0107 ----
    {
        // Great Root Mother (ch.1 pilot boss)
        const FTDDBossPhaseGraph G = MakeRootMotherGraph();
        const FTDDGraphValidation V = ValidateBossGraph(G);
        Check(V.bOk, "graph: Root Mother validates (reachable, targets exist, no dead ends)");

        // first-satisfied-wins ordering
        FTDBossSnapshot S;
        S.HealthPct = 0.50f;
        S.ElapsedSec = 200.0f; // BOTH Roots transitions satisfied
        Check(SelectNextPhase(G, "Roots", S) == "Bloom", "graph: first satisfied transition wins (order, not priority)");

        // poise break fires Bloom -> Rage
        S.HealthPct = 0.40f;
        S.bPoiseBroken = true;
        Check(SelectNextPhase(G, "Bloom", S) == "Rage", "graph: PoiseBreak transition");

        // terminal lock: Defeat never transitions out
        S.HealthPct = 0.0f;
        Check(SelectNextPhase(G, "Rage", S) == "Defeat", "graph: HealthPct 0 -> Defeat");
        S.bPoiseBroken = true;
        S.ElapsedSec = 1.0e4f;
        Check(SelectNextPhase(G, "Defeat", S) == "Defeat", "graph: terminal phase locked");

        // validation catches a dead end
        FTDDBossPhaseGraph Bad = G;
        FTDDPhaseDefinition Trap;
        Trap.PhaseName = "Trap"; // no transitions, not terminal
        Bad.Phases.push_back(Trap);
        Check(ValidateBossGraph(Bad).Errors.size() == 2, "graph: dead-end + unreachable detected");

        // validation catches a missing target
        FTDDBossPhaseGraph Bad2 = G;
        FTDDPhaseTransition T;
        T.Kind = ETDDTransitionKind::Event;
        T.EventName = "x";
        T.TargetPhase = "Nowhere";
        Bad2.Phases[0].Transitions.push_back(T);
        Check(!ValidateBossGraph(Bad2).bOk, "graph: missing transition target detected");

        // Data-only second boss: Iron Elephant = NEW DATA, ZERO new code
        FTDDBossPhaseGraph Elephant;
        FTDDPhaseDefinition E1;
        E1.PhaseName = "Trunk";
        FTDDPhaseTransition ET;
        ET.Kind = ETDDTransitionKind::HealthPct;
        ET.Threshold = 0.66f;
        ET.TargetPhase = "Charge";
        E1.Transitions.push_back(ET);
        Elephant.Phases.push_back(E1);
        FTDDPhaseDefinition E2;
        E2.PhaseName = "Charge";
        FTDDPhaseTransition ET2;
        ET2.Kind = ETDDTransitionKind::MemoryFound;
        ET2.Threshold = 1.0f;
        ET2.TargetPhase = "Stomp";
        E2.Transitions.push_back(ET2);
        Elephant.Phases.push_back(E2);
        FTDDPhaseDefinition E3;
        E3.PhaseName = "Stomp";
        FTDDPhaseTransition ET3;
        ET3.Kind = ETDDTransitionKind::HealthPct;
        ET3.Threshold = 0.0f;
        ET3.TargetPhase = "Defeat";
        E3.Transitions.push_back(ET3);
        Elephant.Phases.push_back(E3);
        FTDDPhaseDefinition E4;
        E4.PhaseName = "Defeat";
        Elephant.Phases.push_back(E4);
        Elephant.EntryPhase = "Trunk";
        Elephant.DefeatPhase = "Defeat";
        Elephant.TerminalPhases.push_back("Defeat");
        Check(ValidateBossGraph(Elephant).bOk, "graph: Iron Elephant is data-only (same controller, new asset)");

        // MemoryFound transition
        FTDBossSnapshot S2;
        S2.MemoriesFound = 1;
        Check(SelectNextPhase(Elephant, "Charge", S2) == "Stomp", "graph: MemoryFound transition");

        // weighted deterministic selection
        std::vector<FTDDWeightedChoice> C;
        FTDDWeightedChoice W1; W1.Name = "A"; W1.Weight = 1.0f; C.push_back(W1);
        FTDDWeightedChoice W2; W2.Name = "B"; W2.Weight = 3.0f; C.push_back(W2);
        FTDDWeightedChoice W3; W3.Name = "C"; W3.Weight = 6.0f; C.push_back(W3);
        Check(PickWeighted(C, 42) == PickWeighted(C, 42), "weights: same seed -> same pick");
        std::int32_t Counts[3] = { 0, 0, 0 };
        const std::int32_t N = 30000;
        for (std::int32_t I = 0; I < N; ++I)
        {
            Counts[PickWeighted(C, static_cast<std::uint64_t>(I))] += 1;
        }
        const float A_ = Counts[0] / static_cast<float>(N);
        const float B_ = Counts[1] / static_cast<float>(N);
        const float C_ = Counts[2] / static_cast<float>(N);
        Check(std::fabs(A_ - 0.10f) < 0.025f, "weights: ~10% for weight 1");
        Check(std::fabs(B_ - 0.30f) < 0.025f, "weights: ~30% for weight 3");
        Check(std::fabs(C_ - 0.60f) < 0.025f, "weights: ~60% for weight 6");
    }

    // ---- Target selection (player/enemy boundary) ----
    {
        std::vector<FTDDTargetCandidate> C;
        FTDDTargetCandidate A; A.Id = 7; A.Distance = 500.0f; A.Threat = 1.0f; C.push_back(A);
        FTDDTargetCandidate B; B.Id = 3; B.Distance = 100.0f; B.Threat = 1.0f; C.push_back(B);
        FTDDTargetCandidate NoLos; NoLos.Id = 1; NoLos.Distance = 10.0f; NoLos.bHasLineOfSight = false; C.push_back(NoLos);
        Check(SelectTarget(C) == 3, "target: closest threat wins, LOS-gated");

        // tie -> lowest Id
        std::vector<FTDDTargetCandidate> T;
        FTDDTargetCandidate X; X.Id = 9; X.Distance = 100.0f; T.push_back(X);
        FTDDTargetCandidate Y; Y.Id = 2; Y.Distance = 100.0f; T.push_back(Y);
        Check(SelectTarget(T) == 2, "target: ties break by lowest Id");

        // no LOS at all -> none
        std::vector<FTDDTargetCandidate> L;
        FTDDTargetCandidate Z; Z.Id = 1; Z.bHasLineOfSight = false; L.push_back(Z);
        Check(SelectTarget(L) == -1, "target: no LOS -> no target");
        Check(SelectTarget({}) == -1, "target: empty roster -> no target");
    }

    if (Failures != 0)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; " << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
