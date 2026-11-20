#pragma once

// Pure traversal fallback resolution (M1 spec v1.4 §3.1 — "the fallback is a
// two-phase decision" + §6 E1/E2/E3). AC-10: budget 0/1/2/3 attempts; 4a all
// options always evaluated; 4b zero-writes when nothing resolves; 5 logged.

#include <cstdint>
#include <string>
#include <vector>

namespace TDD
{
namespace Traversal
{

constexpr float FallbackPhase1Budget = 0.25f; // s

struct FTDDFallbackInput
{
    std::int32_t AttemptBudget = 3;        // 0..3 total traversal attempts allowed
    bool bPhase1AttemptSucceeds = false;   // the primary traversal succeeds
    float Phase1AttemptTime = 0.5f;        // s needed for the primary attempt
    bool bPhase2OptionAvailable = false;   // an alternate route exists
    float Phase2AttemptTime = 0.10f;       // s needed for the alternate
    float FrameDt = 0.016f;
};

struct FTDDFallbackOutput
{
    bool bTraversed = false;
    bool bPhase1 = false;                 // succeeded during phase 1
    bool bPhase2EvaluatedAllOptions = false; // 4a
    bool bZeroWrite = false;              // 4b: no state/movement/audio writes
    std::int32_t AttemptsUsed = 0;
    float ResolveTime = 0.0f;
    bool bResolutionLogged = false;       // 5
    std::vector<std::string> Writes;      // observable writes the resolution performed
    std::string Log;
};

/**
 * Frame-stepped pure simulation of the fallback decision.
 *  Phase 1 (t <= 0.25 s): attempt the primary traversal (if budget allows).
 *  Phase 2 (t > 0.25 s): 4a evaluate ALL remaining options; if one resolves,
 *  take it; 4b otherwise perform ZERO writes (state, movement, audio all
 *  untouched) and resolve; 5 log ResolutionComplete either way.
 */
inline FTDDFallbackOutput ResolveFallback(const FTDDFallbackInput& In)
{
    FTDDFallbackOutput Out;
    const std::int32_t budget = In.AttemptBudget < 0 ? 0 : (In.AttemptBudget > 3 ? 3 : In.AttemptBudget);

    const auto Log = [&Out](const std::string Msg) {
        Out.Log += (Out.Log.empty() ? "" : "; ") + Msg;
    };

    // ---- Phase 1 ----
    if (budget > 0)
    {
        Out.AttemptsUsed = 1;
        if (In.bPhase1AttemptSucceeds && In.Phase1AttemptTime <= FallbackPhase1Budget)
        {
            Out.bTraversed = true;
            Out.bPhase1 = true;
            Out.ResolveTime = In.Phase1AttemptTime;
            Out.Writes.push_back("State->Traversal");
            Out.Writes.push_back("Montage.Play");
            Out.Writes.push_back("Audio.TraversalStart");
            Log("phase1 success at " + std::to_string(In.Phase1AttemptTime));
            Out.bResolutionLogged = true;
            Log("Fallback.ResolutionComplete");
            return Out;
        }
        // attempt failed or overran the 0.25 s budget -> phase 2
    }

    // ---- Phase 2 at budget expiry ----
    Out.bPhase2EvaluatedAllOptions = true; // 4a: ALWAYS evaluates all remaining options
    Log("phase2 at " + std::to_string(FallbackPhase1Budget) + " (all options evaluated)");

    if (In.bPhase2OptionAvailable && Out.AttemptsUsed < budget)
    {
        Out.AttemptsUsed += 1;
        Out.bTraversed = true;
        Out.ResolveTime = FallbackPhase1Budget + In.Phase2AttemptTime;
        Out.Writes.push_back("State->Traversal(alternate)");
        Out.Writes.push_back("Montage.Play");
        Out.Writes.push_back("Audio.TraversalStart");
        Log("phase2 alternate accepted");
    }
    else if (In.bPhase2OptionAvailable)
    {
        // budget exhausted on phase 1: 4b zero-writes
        Out.bZeroWrite = true;
        Out.ResolveTime = FallbackPhase1Budget;
        Log("4b zero-write (budget exhausted, option exists)");
    }
    else
    {
        // nothing resolves: 4b zero-writes
        Out.bZeroWrite = true;
        Out.ResolveTime = FallbackPhase1Budget;
        Log("4b zero-write (no resolving option)");
    }
    Out.bResolutionLogged = true; // 5
    Log("Fallback.ResolutionComplete");
    return Out;
}

} // namespace Traversal
} // namespace TDD
