#pragma once

// Pure damage pipeline core — the single arbitration point for all damage
// (D-23: all damage through FTDDDamageRequest; outcomes rule-computed, never
// animation-computed). Contract: M1 spec v1.4 §3.2.1 (damage taxonomy),
// MEAD §5.4, D-03 (bCausesStagger, approved).
//
// The one evaluation rule that everything else hangs on (spec §3.2.1 fact 2):
// posture promotion happens BEFORE state resolution, and the pipeline is
// evaluated ONCE per hit — so a hit can never be both "abort" and "stagger"
// depending on evaluation order.

#include <cmath>
#include <cstdint>

namespace TDD
{
namespace Combat
{

enum class ETDDDamageClassification : std::uint8_t
{
    None,             // rejected / no-op (invalid request)
    NonStaggering,    // an abort REQUEST (ETDDCancelReason::Damaged) — the current state may accept or ignore it
    Staggering,       // FORCED transition to Stagger (priority 80) — cannot be refused, ignored or delayed
    Lethal,           // FORCED transition to Dead (priority 100)
    LethalStaggering  // Dead outranks Stagger: exactly one state change (Dead); stagger is superseded
};

/** One damage hit, classified as data, not as a hard-coded rule (spec §3.2.1). */
struct FTDDDamageRequest
{
    float HealthDamage = 0.0f;      // positive; applied regardless of control outcome
    float PostureDamage = 0.0f;     // positive; accumulates against MaxPosture
    bool bCausesStagger = false;    // set by attack data / damage class (D-03), never by the state machine
    bool bFromSuccessfulParry = false; // a successful parry against the victim makes the ATTACKER stagger

    bool IsValid() const noexcept
    {
        return std::isfinite(HealthDamage) && std::isfinite(PostureDamage) &&
               HealthDamage > 0.0f && PostureDamage >= 0.0f;
    }
};

struct FTDDDefenderState
{
    float Health = 100.0f;
    float Posture = 0.0f;
    float MaxPosture = 100.0f;
};

/** The complete, once-evaluated outcome of a single hit. */
struct FTDDDamageOutcome
{
    ETDDDamageClassification Classification = ETDDDamageClassification::None;
    float NewHealth = 0.0f;
    float NewPosture = 0.0f;
    bool bHealthReduced = false;     // independent of state (spec §3.2.1 fact 1)
    bool bPostureBroken = false;
    bool bEnteredDead = false;
    bool bEnteredStagger = false;    // false for LethalStaggering: Dead wins, stagger is superseded
    bool bControlLost = false;       // bEnteredDead || bEnteredStagger — the state machine must react
};

/**
 * Evaluates one hit exactly once.
 *  1. Health reduction (independent of control).
 *  2. Posture accumulation; a non-staggering hit that breaks posture is
 *     PROMOTED to staggering in the same frame (before state resolution).
 *  3. Classification: lethal > staggering > non-staggering.
 *  4. Dead > Stagger: when both apply, exactly one state change (Dead).
 */
inline FTDDDamageOutcome EvaluateDamage(const FTDDDamageRequest& Req, const FTDDDefenderState& Defender) noexcept
{
    FTDDDamageOutcome Out;
    Out.NewHealth = Defender.Health;
    Out.NewPosture = Defender.Posture;

    if (!Req.IsValid())
    {
        return Out; // None — rejected, nothing changes
    }

    Out.NewHealth = Defender.Health - Req.HealthDamage;
    if (Out.NewHealth < 0.0f)
    {
        Out.NewHealth = 0.0f;
    }
    Out.bHealthReduced = true;

    const float PostureAfter = Defender.Posture + Req.PostureDamage;
    Out.bPostureBroken = Defender.MaxPosture > 0.0f && PostureAfter >= Defender.MaxPosture && Req.PostureDamage > 0.0f;
    Out.NewPosture = Defender.MaxPosture > 0.0f ? (PostureAfter > Defender.MaxPosture ? Defender.MaxPosture : PostureAfter) : PostureAfter;

    const bool bLethal = Out.NewHealth <= 0.0f;
    const bool bStaggering = Req.bCausesStagger || Req.bFromSuccessfulParry || Out.bPostureBroken;

    if (bLethal && bStaggering)
    {
        // E5 outranks E4: lethal AND staggering enters Dead only.
        Out.Classification = ETDDDamageClassification::LethalStaggering;
        Out.bEnteredDead = true;
        Out.bEnteredStagger = false; // superseded by Dead (spec §3.2.3 invariant)
    }
    else if (bLethal)
    {
        Out.Classification = ETDDDamageClassification::Lethal;
        Out.bEnteredDead = true;
    }
    else if (bStaggering)
    {
        Out.Classification = ETDDDamageClassification::Staggering;
        Out.bEnteredStagger = true;
    }
    else
    {
        Out.Classification = ETDDDamageClassification::NonStaggering;
    }
    Out.bControlLost = Out.bEnteredDead || Out.bEnteredStagger;
    return Out;
}

} // namespace Combat
} // namespace TDD
