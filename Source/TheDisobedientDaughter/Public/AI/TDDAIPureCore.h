#pragma once

// WS3 pure AI cores (ADR-0006 Proposed, ADR-0107 ACCEPTED).
// Host-compilable (std only) — no UE. The UE wrappers
// (UTDDCombatDirectorSubsystem / UTDDBossController) call these.

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

namespace TDD
{
namespace AI
{

// ============================================================================
// 1. Combat director token policy — ADR-0006: "pure-function token policy
//    (FTDDAttackTokenPolicy), unit-tested".
// ============================================================================

struct FTDDTokenPolicySettings
{
    std::int32_t MaxConcurrentAttackers = 2; // concurrent attackers in the encounter
    float TokenTTL = 3.0f;                   // s a held token lives
    float PerEnemyCooldown = 2.5f;           // s between two tokens of the same enemy
};

struct FTDDEnemyCandidate
{
    std::int32_t Id = 0;
    bool bHoldingToken = false;
    float TokenGrantedAt = -1.0e30f; // clock of the current token
    float CooldownRemaining = 0.0f;  // s until this enemy may be granted again
};

/**
 * Grants at most ONE attack token per director tick, to the next READY enemy
 * in cyclic (round-robin) order starting after the last grantee. Determinism:
 * identical state in -> identical grantee out. Fairness: ready enemies are
 * rotated, so no subset starves.
 */
class FTDDAttackTokenPolicy
{
public:
    explicit FTDDAttackTokenPolicy(FTDDTokenPolicySettings S) noexcept : Settings_(S) {}

    const FTDDTokenPolicySettings& Settings() const noexcept { return Settings_; }
    const std::vector<FTDDEnemyCandidate>& Roster() const noexcept { return Roster_; }

    /** (Re)load the encounter roster; resets policy state. */
    void SetRoster(const std::vector<FTDDEnemyCandidate>& Roster)
    {
        Roster_ = Roster;
        GrantCounts_.assign(Roster_.size(), 0);
        LastGranteeIdx_ = -1;
        // Now is an absolute world-time clock. Keep LastTick_ across roster
        // membership updates so existing cooldowns are not fast-forwarded.
    }

    /**
     * One director tick: expire tokens, tick cooldowns, grant at most ONE
     * token (cyclic round-robin over ready enemies). Returns grantee Id or -1.
     */
    std::int32_t GrantNext(const float Now)
    {
        // expire
        for (FTDDEnemyCandidate& E : Roster_)
        {
            if (E.bHoldingToken && Now - E.TokenGrantedAt > Settings_.TokenTTL)
            {
                E.bHoldingToken = false;
                E.TokenGrantedAt = -1.0e30f;
            }
        }
        // cooldowns
        const float Dt = std::max(0.0f, Now - LastTick_);
        LastTick_ = Now;
        for (FTDDEnemyCandidate& E : Roster_)
        {
            E.CooldownRemaining = std::max(0.0f, E.CooldownRemaining - Dt);
        }

        if (ActiveHolders() >= Settings_.MaxConcurrentAttackers || Roster_.empty())
        {
            return -1;
        }

        const std::int32_t N = static_cast<std::int32_t>(Roster_.size());
        for (std::int32_t Step = 0; Step < N; ++Step)
        {
            const std::int32_t Idx = (LastGranteeIdx_ + 1 + Step) % N;
            const FTDDEnemyCandidate& E = Roster_[static_cast<size_t>(Idx)];
            if (!E.bHoldingToken && E.CooldownRemaining <= 0.0f)
            {
                Roster_[static_cast<size_t>(Idx)].bHoldingToken = true;
                Roster_[static_cast<size_t>(Idx)].TokenGrantedAt = Now;
                Roster_[static_cast<size_t>(Idx)].CooldownRemaining = Settings_.PerEnemyCooldown;
                LastGranteeIdx_ = Idx;
                GrantCounts_[static_cast<size_t>(Idx)] += 1;
                return Roster_[static_cast<size_t>(Idx)].Id;
            }
        }
        return -1;
    }

    std::int32_t ActiveHolders() const noexcept
    {
        std::int32_t N = 0;
        for (const FTDDEnemyCandidate& E : Roster_)
        {
            if (E.bHoldingToken)
            {
                ++N;
            }
        }
        return N;
    }

    /** Distinct enemies granted at least one token (fairness measure). */
    std::int32_t DistinctGrantees() const noexcept
    {
        std::int32_t N = 0;
        for (const std::int32_t C : GrantCounts_)
        {
            if (C > 0)
            {
                ++N;
            }
        }
        return N;
    }

    const std::vector<std::int32_t>& GrantCounts() const noexcept { return GrantCounts_; }

    void Reset()
    {
        for (FTDDEnemyCandidate& E : Roster_)
        {
            E.bHoldingToken = false;
            E.TokenGrantedAt = -1.0e30f;
            E.CooldownRemaining = 0.0f;
        }
        std::fill(GrantCounts_.begin(), GrantCounts_.end(), 0);
        LastGranteeIdx_ = -1;
        LastTick_ = 0.0f;
    }

private:
    FTDDTokenPolicySettings Settings_;
    std::vector<FTDDEnemyCandidate> Roster_;
    std::vector<std::int32_t> GrantCounts_;
    std::int32_t LastGranteeIdx_ = -1;
    float LastTick_ = 0.0f;
};

// ============================================================================
// 2. Boss phase graph — ADR-0107: data-driven, no boss-specific branching;
//    pure selector over a snapshot.
// ============================================================================

enum class ETDDTransitionKind : std::uint8_t
{
    PoiseBreak = 0,
    HealthPct,
    ElapsedSec,
    Distance,
    PlayerAbility,
    MemoryFound,
    Event
};

struct FTDDPhaseTransition
{
    ETDDTransitionKind Kind = ETDDTransitionKind::HealthPct;
    float Threshold = 0.0f;
    std::string TargetPhase;
    std::string EventName; // for Kind == Event
};

struct FTDDPhaseDefinition
{
    std::string PhaseName;
    std::vector<FTDDPhaseTransition> Transitions; // evaluated in order; first satisfied wins
    std::string MusicState;
    std::string CameraProfile;
    std::vector<std::string> AbilitySet;
    std::vector<std::string> ArenaStates;
    bool bInvulnerable = false;
};

struct FTDDBossPhaseGraph
{
    std::vector<FTDDPhaseDefinition> Phases;
    std::string EntryPhase;
    std::string DefeatPhase;
    std::vector<std::string> TerminalPhases; // must be reachable; validated
};

struct FTDBossSnapshot
{
    float HealthPct = 1.0f;
    bool bPoiseBroken = false;
    float ElapsedSec = 0.0f;
    float DistanceToPlayer = 0.0f;
    bool bPlayerAbilityReady = false;
    std::int32_t MemoriesFound = 0;
    std::vector<std::string> Events;
};

inline const FTDDPhaseDefinition* FindPhase(const FTDDBossPhaseGraph& G, const std::string& Name) noexcept
{
    for (const FTDDPhaseDefinition& P : G.Phases)
    {
        if (P.PhaseName == Name)
        {
            return &P;
        }
    }
    return nullptr;
}

inline bool IsTerminal(const FTDDBossPhaseGraph& G, const std::string& Name) noexcept
{
    for (const std::string& T : G.TerminalPhases)
    {
        if (T == Name)
        {
            return true;
        }
    }
    return false;
}

inline bool TransitionSatisfied(const FTDDPhaseTransition& T, const FTDBossSnapshot& S) noexcept
{
    switch (T.Kind)
    {
    case ETDDTransitionKind::PoiseBreak: return S.bPoiseBroken;
    case ETDDTransitionKind::HealthPct: return S.HealthPct <= T.Threshold;
    case ETDDTransitionKind::ElapsedSec: return S.ElapsedSec >= T.Threshold;
    case ETDDTransitionKind::Distance: return S.DistanceToPlayer <= T.Threshold;
    case ETDDTransitionKind::PlayerAbility: return S.bPlayerAbilityReady;
    case ETDDTransitionKind::MemoryFound: return S.MemoriesFound >= static_cast<float>(T.Threshold);
    case ETDDTransitionKind::Event:
        for (const std::string& E : S.Events)
        {
            if (E == T.EventName)
            {
                return true;
            }
        }
        return false;
    }
    return false;
}

/** First-satisfied-wins selector. Returns target phase name, or the current
 *  name when no transition fires. Terminal phases never transition out. */
inline std::string SelectNextPhase(const FTDDBossPhaseGraph& G, const std::string& Current,
                            const FTDBossSnapshot& S)
{
    if (IsTerminal(G, Current))
    {
        return Current;
    }
    const FTDDPhaseDefinition* const P = FindPhase(G, Current);
    if (P == nullptr)
    {
        return Current;
    }
    for (const FTDDPhaseTransition& T : P->Transitions)
    {
        if (TransitionSatisfied(T, S))
        {
            return T.TargetPhase;
        }
    }
    return Current;
}

struct FTDDGraphValidation
{
    bool bOk = true;
    std::vector<std::string> Errors;
    void AddError(const std::string& M)
    {
        bOk = false;
        Errors.push_back(M);
    }
};

/** ADR-0107 mandatory test 1: reachability, no dead ends except terminals,
 *  all transition targets exist, terminal list non-empty, entry exists. */
inline FTDDGraphValidation ValidateBossGraph(const FTDDBossPhaseGraph& G)
{
    FTDDGraphValidation V;
    if (G.EntryPhase.empty())
    {
        V.AddError("EntryPhase empty");
    }
    if (FindPhase(G, G.EntryPhase) == nullptr)
    {
        V.AddError("EntryPhase '" + G.EntryPhase + "' not defined");
    }
    if (G.TerminalPhases.empty())
    {
        V.AddError("no terminal phases declared");
    }
    for (const std::string& T : G.TerminalPhases)
    {
        if (FindPhase(G, T) == nullptr)
        {
            V.AddError("terminal phase '" + T + "' not defined");
        }
    }
    if (G.DefeatPhase.empty())
    {
        V.AddError("DefeatPhase empty");
    }
    else if (FindPhase(G, G.DefeatPhase) == nullptr)
    {
        V.AddError("DefeatPhase '" + G.DefeatPhase + "' not defined");
    }
    else if (!IsTerminal(G, G.DefeatPhase))
    {
        V.AddError("DefeatPhase must be declared terminal");
    }
    // Phase names and terminal declarations must be unambiguous.
    for (size_t I = 0; I < G.Phases.size(); ++I)
    {
        if (G.Phases[I].PhaseName.empty())
        {
            V.AddError("phase name empty");
        }
        for (size_t J = 0; J < I; ++J)
        {
            if (G.Phases[I].PhaseName == G.Phases[J].PhaseName)
            {
                V.AddError("duplicate phase '" + G.Phases[I].PhaseName + "'");
                break;
            }
        }
    }
    // transition targets exist; terminal phases cannot contain exit edges.
    for (const FTDDPhaseDefinition& P : G.Phases)
    {
        if (IsTerminal(G, P.PhaseName) && !P.Transitions.empty())
        {
            V.AddError("terminal phase '" + P.PhaseName + "' must not declare transitions");
        }
        for (const FTDDPhaseTransition& T : P.Transitions)
        {
            if (FindPhase(G, T.TargetPhase) == nullptr)
            {
                V.AddError(P.PhaseName + " -> '" + T.TargetPhase + "' target does not exist");
            }
        }
    }
    // reachability from entry (BFS over transition edges)
    std::vector<std::string> Seen;
    Seen.push_back(G.EntryPhase);
    for (size_t I = 0; I < Seen.size(); ++I)
    {
        const FTDDPhaseDefinition* const P = FindPhase(G, Seen[I]);
        if (P == nullptr)
        {
            continue;
        }
        for (const FTDDPhaseTransition& T : P->Transitions)
        {
            bool bAlready = false;
            for (const std::string& S : Seen)
            {
                if (S == T.TargetPhase)
                {
                    bAlready = true;
                    break;
                }
            }
            if (!bAlready)
            {
                Seen.push_back(T.TargetPhase);
            }
        }
    }
    // Reverse reachability: every phase must have a path to some declared
    // terminal, so a closed non-terminal cycle cannot trap the encounter.
    std::vector<std::string> CanReachTerminal;
    for (const std::string& T : G.TerminalPhases)
    {
        if (FindPhase(G, T) != nullptr)
        {
            CanReachTerminal.push_back(T);
        }
    }
    bool bAdded = true;
    while (bAdded)
    {
        bAdded = false;
        for (const FTDDPhaseDefinition& P : G.Phases)
        {
            bool bCanReach = false;
            for (const std::string& N : CanReachTerminal)
            {
                if (P.PhaseName == N)
                {
                    bCanReach = true;
                    break;
                }
            }
            if (!bCanReach)
            {
                for (const FTDDPhaseTransition& T : P.Transitions)
                {
                    for (const std::string& N : CanReachTerminal)
                    {
                        if (T.TargetPhase == N)
                        {
                            CanReachTerminal.push_back(P.PhaseName);
                            bAdded = true;
                            bCanReach = true;
                            break;
                        }
                    }
                    if (bCanReach) break;
                }
            }
        }
    }

    for (const FTDDPhaseDefinition& P : G.Phases)
    {
        bool bReachable = false;
        for (const std::string& S : Seen)
        {
            if (S == P.PhaseName)
            {
                bReachable = true;
                break;
            }
        }
        if (!bReachable)
        {
            V.AddError("phase '" + P.PhaseName + "' unreachable from entry");
        }
        if (P.Transitions.empty() && !IsTerminal(G, P.PhaseName))
        {
            V.AddError("phase '" + P.PhaseName + "' is a dead end but not terminal");
        }
        bool bCanReachTerminal = false;
        for (const std::string& N : CanReachTerminal)
        {
            if (P.PhaseName == N)
            {
                bCanReachTerminal = true;
                break;
            }
        }
        if (!IsTerminal(G, P.PhaseName) && !bCanReachTerminal)
        {
            V.AddError("phase '" + P.PhaseName + "' has no path to a terminal (closed cycle)");
        }
    }
    return V;
}

// ---- Weighted deterministic selection (TDD-Unit.AI.PhaseSelectorWeights) ----

struct FTDDWeightedChoice
{
    std::string Name;
    float Weight = 1.0f;
};

/** Seeded weighted pick (splitmix64 stream). Same seed + choices -> same pick. */
inline std::int32_t PickWeighted(const std::vector<FTDDWeightedChoice>& Choices, const std::uint64_t Seed)
{
    // splitmix64 next
    std::uint64_t Z = Seed + 0x9E3779B97F4A7C15ULL;
    Z = (Z ^ (Z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    Z = (Z ^ (Z >> 27)) * 0x94D049BB133111EBULL;
    const std::uint64_t V = Z ^ (Z >> 31);

    float Total = 0.0f;
    for (const FTDDWeightedChoice& C : Choices)
    {
        Total += std::max(0.0f, C.Weight);
    }
    if (Total <= 0.0f || Choices.empty())
    {
        return -1;
    }
    const float R = static_cast<float>(V % 1000000ULL) / 1000000.0f * Total;
    float Acc = 0.0f;
    for (std::int32_t I = 0; I < static_cast<std::int32_t>(Choices.size()); ++I)
    {
        Acc += std::max(0.0f, Choices[static_cast<size_t>(I)].Weight);
        if (R < Acc)
        {
            return I;
        }
    }
    return static_cast<std::int32_t>(Choices.size()) - 1;
}

// ============================================================================
// 3. Target selection — player/enemy boundary (WS3 brief): enemies target the
//    player only; the player's lock targets enemies only; deterministic.
// ============================================================================

struct FTDDTargetCandidate
{
    std::int32_t Id = 0;
    float Distance = 0.0f;
    bool bHasLineOfSight = true;
    float Threat = 1.0f;
};

/** Highest score wins; ties broken by lowest Id (deterministic).
 *  Score = Threat / (1 + Distance) gated by line-of-sight. */
inline std::int32_t SelectTarget(const std::vector<FTDDTargetCandidate>& Candidates)
{
    std::int32_t BestId = -1;
    float BestScore = -1.0f;
    for (const FTDDTargetCandidate& C : Candidates)
    {
        if (!C.bHasLineOfSight)
        {
            continue;
        }
        const float Score = C.Threat / (1.0f + C.Distance);
        if (Score > BestScore || (Score == BestScore && (BestId == -1 || C.Id < BestId)))
        {
            BestScore = Score;
            BestId = C.Id;
        }
    }
    return BestId;
}

} // namespace AI
} // namespace TDD
