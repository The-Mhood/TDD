#pragma once

// Pure player state machine core (M1 spec v1.4 §3.2 — the only writer of
// player state). Engine-independent: compiled and tested host-side (g++) and
// inside UE automation alike. The UE component (UTDDCharacterStateMachine)
// is a thin wrapper that calls this on the tick thread — no second logic.
//
// Contract points implemented here (spec §3.2):
//  * 7-step RequestState decision (priority, preconditions, min dwell,
//    exit actions, entry, broadcast)
//  * forced transitions (Dead 100 / Cinematic 90 / Stagger 80) preempt by
//    priority and are never refused while a lower-priority state is active
//    (§3.2.2d: the queue holds the highest priority only)
//  * min-dwell anti-flap, buffer policy (delegated to FTDDInputBuffer),
//    refusal logging (a refusal is never silent)
//  * exit checklist on EVERY exit, natural or forced (9 steps, recorded)
//  * restoration runs exactly once (double-run is logged, per §3.2.3)
//  * forced transitions arriving mid-resolution are queued, not interleaved,
//    and applied after restoration (highest priority only)

#include <cmath>
#include <cstdint>
#include <functional>
#include <string>

namespace TDD
{
namespace State
{

enum class ETDDPlayerState : std::uint8_t
{
    Idle = 0,
    Locomotion,
    Sprint,
    Airborne,
    Land,
    Dodge,
    Attack,
    Block,
    Parry,
    Stagger,
    Traversal,
    Interaction,
    Cinematic,
    Dead,
    Count = 14
};

/** Priority — higher wins, forced only (spec §3.2). */
inline std::int32_t StatePriority(const ETDDPlayerState S) noexcept
{
    switch (S)
    {
    case ETDDPlayerState::Dead: return 100;
    case ETDDPlayerState::Cinematic: return 90;
    case ETDDPlayerState::Stagger: return 80;
    case ETDDPlayerState::Attack:
    case ETDDPlayerState::Block:
    case ETDDPlayerState::Parry: return 60;
    case ETDDPlayerState::Dodge: return 50;
    case ETDDPlayerState::Traversal: return 40;
    case ETDDPlayerState::Land: return 30;
    default: return 10; // Idle / Locomotion / Sprint
    }
}

inline bool IsForcedState(const ETDDPlayerState S) noexcept
{
    return S == ETDDPlayerState::Dead || S == ETDDPlayerState::Cinematic || S == ETDDPlayerState::Stagger;
}

enum class ETDDRefusalReason : std::uint8_t
{
    Accepted = 0,
    ForcedPriorityRefused,      // lower/equal-priority forced into a higher-priority forced state
    NotInInterruptionMask,      // requested target not legal from the current state (Table B)
    MinDwellNotElapsed,         // anti-flap
    TerminalState,              // Dead: nothing transitions out
    AlreadyInState              // re-forcing the current forced state: no state change, logged
};

/** Per-state rule row (spec §3.2 Table A/B distilled; data, not code paths). */
struct FTDDStateRuleRow
{
    ETDDPlayerState State;
    std::int32_t Priority;
    bool bForced;
    float MinDwell;             // s; 0 = no dwell
    float RecoveryTime;         // s; inf = ends only by event (e.g. Airborne grounding)
    ETDDPlayerState RecoveryTarget;
    /** Requested-interruption mask: which non-forced targets may interrupt THIS state (Table B). */
    std::uint16_t InterruptibleByMask;

    bool AcceptsRequested(const ETDDPlayerState Target) const noexcept
    {
        if (IsForcedState(Target))
        {
            return false; // forced targets are never "requested"
        }
        return (InterruptibleByMask & (1u << static_cast<std::uint8_t>(Target))) != 0u;
    }
};

namespace Detail
{
constexpr std::uint16_t Bit(ETDDPlayerState S) noexcept
{
    return static_cast<std::uint16_t>(1u << static_cast<std::uint8_t>(S));
}

// Table B: which non-forced targets may interrupt each state (requested paths).
// Forced paths (Dead/Cinematic/Stagger) are governed purely by priority.
inline std::uint16_t InterruptionMask(const ETDDPlayerState S, const bool bAirDodgeEnabled) noexcept
{
    using P = ETDDPlayerState;
    switch (S)
    {
    case P::Idle:
    case P::Locomotion:
    case P::Sprint:
        // "any request": every non-forced state except the current one itself.
        // (Stop-to-Idle is a request, per Table A recovery "input below deadzone".)
        return (Detail::Bit(P::Idle) | Detail::Bit(P::Locomotion) | Detail::Bit(P::Sprint)
             | Detail::Bit(P::Airborne) | Detail::Bit(P::Land) | Detail::Bit(P::Dodge)
             | Detail::Bit(P::Attack) | Detail::Bit(P::Block) | Detail::Bit(P::Parry)
             | Detail::Bit(P::Traversal) | Detail::Bit(P::Interaction))
             & ~Detail::Bit(S);
    case P::Airborne:
        return bAirDodgeEnabled ? Detail::Bit(P::Dodge) : 0;
    case P::Land:
        return Detail::Bit(P::Dodge); // after landing frame, fall speed < threshold (data)
    case P::Dodge:
        return 0;                     // damage/parry/stagger/death only = forced; no self-cancel in dwell
    case P::Attack:
        return Detail::Bit(P::Dodge) | Detail::Bit(P::Parry); // + damage if declared interruptible (pipeline path)
    case P::Block:
        return Detail::Bit(P::Parry); // guard break -> Stagger is forced
    case P::Parry:
        return 0;
    case P::Stagger:
        return 0;                     // Dead only = forced
    case P::Traversal:
        return Detail::Bit(P::Locomotion) | Detail::Bit(P::Land); // E3 requested abort inside AbortWindow
    case P::Interaction:
        return Detail::Bit(P::Locomotion) | Detail::Bit(P::Sprint) | Detail::Bit(P::Idle); // cancel-on-move
    case P::Cinematic:
        return 0;
    case P::Dead:
        return 0;
    default:
        return 0;
    }
}
} // namespace Detail

/** The 14 default rule rows (spec §3.2 Table A). RecoveryTime = data. */
inline FTDDStateRuleRow MakeRuleRow(const ETDDPlayerState S, const bool bAirDodgeEnabled) noexcept
{
    using P = ETDDPlayerState;
    FTDDStateRuleRow R;
    R.State = S;
    R.Priority = StatePriority(S);
    R.bForced = IsForcedState(S);
    R.InterruptibleByMask = Detail::InterruptionMask(S, bAirDodgeEnabled);
    switch (S)
    {
    // RecoveryTime: intent/event-ended states use 1e30 (a huge sentinel, not a timer).
    case P::Idle:         R.MinDwell = 0.05f; R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break;
    case P::Locomotion:   R.MinDwell = 0.05f; R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break; // input below deadzone (intent)
    case P::Sprint:       R.MinDwell = 0.10f; R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Locomotion; break; // sprint released (intent)
    case P::Airborne:     R.MinDwell = 0.0f;  R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Land; break; // event-ended (grounding)
    case P::Land:         R.MinDwell = 0.0f;  R.RecoveryTime = 0.15f; R.RecoveryTarget = P::Locomotion; break; // landing timer (data)
    case P::Dodge:        R.MinDwell = 0.15f; R.RecoveryTime = 0.35f; R.RecoveryTarget = P::Locomotion; break; // montage end
    case P::Attack:       R.MinDwell = 0.20f; R.RecoveryTime = 0.50f; R.RecoveryTarget = P::Locomotion; break; // per-attack data
    case P::Block:        R.MinDwell = 0.08f; R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break; // guard released beyond grace (intent)
    case P::Parry:        R.MinDwell = 0.0f;  R.RecoveryTime = 0.15f; R.RecoveryTarget = P::Block; break; // window expiry
    case P::Stagger:      R.MinDwell = 0.40f; R.RecoveryTime = 0.40f; R.RecoveryTarget = P::Locomotion; break; // stagger duration
    case P::Traversal:    R.MinDwell = 0.0f;  R.RecoveryTime = 2.0f;  R.RecoveryTarget = P::Locomotion; break; // montage
    case P::Interaction:  R.MinDwell = 0.0f;  R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break; // hold complete / cancel (event)
    case P::Cinematic:    R.MinDwell = 0.0f;  R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break; // subsystem end
    case P::Dead:         R.MinDwell = 1.0e30f; R.RecoveryTime = 1.0e30f; R.RecoveryTarget = P::Idle; break; // respawn forced by flow
    default: break;
    }
    return R;
}

// ---------------------------------------------------------------------------
// Legality — the 196-pair contract (AC-22)
// ---------------------------------------------------------------------------

/** A forced target is legal from S iff it outranks S (§3.2.2d: highest priority only). */
inline bool IsLegalForcedPair(const ETDDPlayerState From, const ETDDPlayerState To) noexcept
{
    if (!IsForcedState(To))
    {
        return false;
    }
    return StatePriority(To) > StatePriority(From);
}

/** A requested target is legal iff the current state's mask admits it (Table B). */
inline bool IsLegalRequestedPair(const ETDDPlayerState From, const ETDDPlayerState To,
                                 const bool bAirDodgeEnabled) noexcept
{
    if (IsForcedState(To))
    {
        return false;
    }
    return MakeRuleRow(From, bAirDodgeEnabled).AcceptsRequested(To);
}

/** Total legal pairs over all 196 (forced + requested), for AC-22 bookkeeping. */
inline std::int32_t CountLegalPairs(const bool bAirDodgeEnabled) noexcept
{
    std::int32_t Legal = 0;
    for (std::uint8_t F = 0; F < static_cast<std::uint8_t>(ETDDPlayerState::Count); ++F)
    {
        for (std::uint8_t T = 0; T < static_cast<std::uint8_t>(ETDDPlayerState::Count); ++T)
        {
            const ETDDPlayerState From = static_cast<ETDDPlayerState>(F);
            const ETDDPlayerState To = static_cast<ETDDPlayerState>(T);
            if (IsLegalForcedPair(From, To) || IsLegalRequestedPair(From, To, bAirDodgeEnabled))
            {
                ++Legal;
            }
        }
    }
    return Legal;
}

// ---------------------------------------------------------------------------
// The machine
// ---------------------------------------------------------------------------

/** 9-step exit checklist (spec §3.2 exit actions + §3.2.2 restoration). */
struct FTDDChecklistRecord
{
    bool StopMontage = false;
    bool ClearStatusTags = false;
    bool RestoreMovementMode = false;   // skipped under HoldUnsupported 4b (logged exception)
    bool RestoreRotationMode = false;
    bool ReleaseInputLock = false;
    bool ClearMotionWarpTargets = false;
    bool PublishStateChanged = false;
    std::int32_t RestorationRuns = 0;   // must be exactly 1 when restoration is due
    bool bDoubleRunLogged = false;

    bool AllExitStepsDone() const noexcept
    {
        return StopMontage && ClearStatusTags && RestoreMovementMode && RestoreRotationMode
             && ReleaseInputLock && ClearMotionWarpTargets && PublishStateChanged;
    }
};

class FTDDPureStateMachine
{
public:
    using LogFn = std::function<void(const std::string&)>;

    explicit FTDDPureStateMachine(const bool bAirDodgeEnabled = false, LogFn InLog = nullptr) noexcept
        : Log(std::move(InLog))
    {
        for (std::uint8_t I = 0; I < static_cast<std::uint8_t>(ETDDPlayerState::Count); ++I)
        {
            Rules[I] = MakeRuleRow(static_cast<ETDDPlayerState>(I), bAirDodgeEnabled);
        }
        Current_ = ETDDPlayerState::Idle;
    }

    ETDDPlayerState Current() const noexcept { return Current_; }
    float TimeInCurrent() const noexcept { return TimeInState_; }
    const FTDDChecklistRecord& Checklist() const noexcept { return Checklist_; }
    std::int32_t TransitionCount() const noexcept { return Transitions_; }
    std::int32_t RefusalCount() const noexcept { return Refusals_; }
    const ETDDPlayerState* PendingForced() const noexcept { return PendingForced_; }
    bool bInResolution() const noexcept { return bResolutionInProgress_; }
    std::int32_t PendingForcedPriority() const noexcept
    {
        return PendingForced_ == nullptr ? 0 : StatePriority(*PendingForced_);
    }

    /** Advances the clock; ends states at their recovery time (data). */
    void Tick(const float Dt)
    {
        if (!std::isfinite(Dt) || Dt < 0.0f)
        {
            return;
        }
        TimeInState_ += Dt;
        const FTDDStateRuleRow& R = Rules[static_cast<std::uint8_t>(Current_)];
        if (R.RecoveryTime < 1.0e29f && TimeInState_ >= R.RecoveryTime)
        {
            const ETDDPlayerState Target = R.RecoveryTarget;
            if (Target != Current_)
            {
                const char* const FromName = Name(Current_);
                RunExitChecklist();
                Current_ = Target;
                TimeInState_ = 0.0f;
                ++Transitions_;
                Logf(std::string("recovery ") + FromName + " -> " + Name(Target));
            }
        }
    }

    /** Requested transition — the 7-step decision (spec §3.2). Refusals are logged. */
    ETDDRefusalReason RequestState(const ETDDPlayerState Target, const char* const Reason = "request")
    {
        if (IsForcedState(Target))
        {
            return ForceState(Target); // forced targets must not be "requested"
        }

        const FTDDStateRuleRow& Cur = Rules[static_cast<std::uint8_t>(Current_)];
        if (bResolutionInProgress_ && PendingForced_ != nullptr)
        {
            LogRefuse(Target, Reason, ETDDRefusalReason::ForcedPriorityRefused, "queued forced in progress");
            return ETDDRefusalReason::ForcedPriorityRefused;
        }
        if (!Cur.AcceptsRequested(Target))
        {
            LogRefuse(Target, Reason, ETDDRefusalReason::NotInInterruptionMask, "not in interruption mask");
            return ETDDRefusalReason::NotInInterruptionMask;
        }
        if (TimeInState_ < Cur.MinDwell)
        {
            LogRefuse(Target, Reason, ETDDRefusalReason::MinDwellNotElapsed, "min dwell not elapsed");
            return ETDDRefusalReason::MinDwellNotElapsed;
        }

        RunExitChecklist();
        Current_ = Target;
        TimeInState_ = 0.0f;
        ++Transitions_;
        Logf(std::string("request accepted -> ") + Name(Target));
        return ETDDRefusalReason::Accepted;
    }

    /**
     * Forced transition (spec §3.2 rule: cannot be refused while a
     * lower-priority state is active; §3.2.2d: highest priority only).
     * Mid-resolution: queued, not interleaved.
     */
    ETDDRefusalReason ForceState(const ETDDPlayerState Target)
    {
        if (!IsForcedState(Target))
        {
            return RequestState(Target, "misrouted forced");
        }
        if (Current_ == Target)
        {
            // AC-22: every pair is either a transition or a logged refusal.
            // Re-forcing the current state changes nothing and is logged as such.
            ++Refusals_;
            Logf(std::string("refused ") + Name(Current_) + " -> " + Name(Target) + " (already in state)");
            return ETDDRefusalReason::AlreadyInState;
        }
        if (StatePriority(Target) <= StatePriority(Current_))
        {
            LogRefuse(Target, "forced", ETDDRefusalReason::ForcedPriorityRefused,
                      "priority <= current (superseded, logged)");
            return ETDDRefusalReason::ForcedPriorityRefused;
        }

        if (bResolutionInProgress_)
        {
            // Queue (highest priority only, 3.2.2d); resolution never yields.
            if (PendingForced_ == nullptr || StatePriority(Target) > StatePriority(*PendingForced_))
            {
                PendingForcedStorage_ = Target;
                PendingForced_ = &PendingForcedStorage_;
                Logf(std::string("forced queued during resolution -> ") + Name(Target));
            }
            else
            {
                LogRefuse(Target, "forced", ETDDRefusalReason::ForcedPriorityRefused, "lower-priority forced superseded");
            }
            return ETDDRefusalReason::Accepted; // queued
        }

        RunExitChecklist();
        Current_ = Target;
        TimeInState_ = 0.0f;
        ++Transitions_;
        Logf(std::string("forced -> ") + Name(Target));
        return ETDDRefusalReason::Accepted;
    }

    /** Resolution (e.g. traversal fallback) begins: forced targets queue, no interleaving. */
    void BeginResolution() noexcept { bResolutionInProgress_ = true; }

    /** Resolution completes: restoration is owned by the caller, then the queued
     *  highest-priority forced target is applied (if any). */
    ETDDPlayerState EndResolution()
    {
        bResolutionInProgress_ = false;
        if (PendingForced_ != nullptr)
        {
            const ETDDPlayerState Target = *PendingForced_;
            PendingForced_ = nullptr;
            // The triggering resolution already ran its checklist; enter the forced target.
            Current_ = Target;
            TimeInState_ = 0.0f;
            ++Transitions_;
            Logf(std::string("queued forced applied after resolution -> ") + Name(Target));
            return Target;
        }
        return Current_;
    }

    /** The single restoration entry point — runs exactly once (double-run logged). */
    void RunRestorationChecklist()
    {
        if (Checklist_.RestorationRuns > 0)
        {
            Checklist_.bDoubleRunLogged = true;
            Logf("Restoration.DoubleRun — two owners (spec 3.2.3 invariant violated)");
            return;
        }
        ++Checklist_.RestorationRuns;
    }

    /** Test-only: place the machine in a state without running the rules. */
    void SetStateForTest(const ETDDPlayerState S) noexcept
    {
        Current_ = S;
        TimeInState_ = 0.0f;
    }

    /** Test hook: reset to Idle with a clean checklist (named transitions only). */
    void ResetForTest()
    {
        Current_ = ETDDPlayerState::Idle;
        TimeInState_ = 0.0f;
        Checklist_ = FTDDChecklistRecord{};
        Transitions_ = 0;
        Refusals_ = 0;
        bResolutionInProgress_ = false;
        PendingForced_ = nullptr;
    }

    static const char* Name(const ETDDPlayerState S) noexcept
    {
        switch (S)
        {
        case ETDDPlayerState::Idle: return "Idle";
        case ETDDPlayerState::Locomotion: return "Locomotion";
        case ETDDPlayerState::Sprint: return "Sprint";
        case ETDDPlayerState::Airborne: return "Airborne";
        case ETDDPlayerState::Land: return "Land";
        case ETDDPlayerState::Dodge: return "Dodge";
        case ETDDPlayerState::Attack: return "Attack";
        case ETDDPlayerState::Block: return "Block";
        case ETDDPlayerState::Parry: return "Parry";
        case ETDDPlayerState::Stagger: return "Stagger";
        case ETDDPlayerState::Traversal: return "Traversal";
        case ETDDPlayerState::Interaction: return "Interaction";
        case ETDDPlayerState::Cinematic: return "Cinematic";
        case ETDDPlayerState::Dead: return "Dead";
        default: return "?";
        }
    }

private:
    void RunExitChecklist()
    {
        Checklist_.StopMontage = true;
        Checklist_.ClearStatusTags = true;
        Checklist_.RestoreMovementMode = true;
        Checklist_.RestoreRotationMode = true;
        Checklist_.ReleaseInputLock = true;
        Checklist_.ClearMotionWarpTargets = true;
        Checklist_.PublishStateChanged = true;
    }

    void Logf(const std::string& Msg)
    {
        if (Log)
        {
            Log(Msg);
        }
    }

    void LogRefuse(const ETDDPlayerState Target, const char* const Reason,
                   const ETDDRefusalReason Why, const char* const Detail)
    {
        ++Refusals_;
        Logf(std::string("refused ") + Name(Current_) + " -> " + Name(Target)
             + " reason=" + Reason + " (" + Detail + ")");
    }

    FTDDStateRuleRow Rules[static_cast<std::int32_t>(ETDDPlayerState::Count)];
    FTDDChecklistRecord Checklist_;
    ETDDPlayerState Current_ = ETDDPlayerState::Idle;
    float TimeInState_ = 0.0f;
    std::int32_t Transitions_ = 0;
    std::int32_t Refusals_ = 0;
    bool bResolutionInProgress_ = false;
    const ETDDPlayerState* PendingForced_ = nullptr;
    ETDDPlayerState PendingForcedStorage_;
    LogFn Log;
};

} // namespace State
} // namespace TDD
