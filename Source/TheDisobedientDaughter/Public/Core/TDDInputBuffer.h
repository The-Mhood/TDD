#pragma once

// Pure input buffer core (M1 spec v1.4 §3.4 — "pure logic, FTDDInputBuffer,
// no world dependency"). AC-24: single consumption, exact expiry,
// replace-not-queue, clear-on-lock matrix. AC-25: coyote window (accept
// 0.11 s, reject 0.13 s after leaving ground).

#include <cmath>
#include <cstdint>
#include <cstring>
#include <string>

namespace TDD
{
namespace Input
{

enum class ETDDIntent : std::uint8_t
{
    Move2D = 0, Look2D, Sprint, Jump, Dodge,
    LightAttack, HeavyAttack, Block, Parry,
    LockOn, Interact, TraversalConfirm, Pause,
    Count = 13
};

/** Buffer windows in seconds (spec §3.4). 0 = not buffered. */
inline float WindowFor(const ETDDIntent I) noexcept
{
    switch (I)
    {
    case ETDDIntent::Dodge: return 0.20f;
    case ETDDIntent::Jump: return 0.15f;
    case ETDDIntent::LightAttack:
    case ETDDIntent::HeavyAttack: return 0.20f;
    case ETDDIntent::Parry: return 0.15f;
    case ETDDIntent::Block: return 0.10f; // release grace
    default: return 0.0f;
    }
}

inline bool IsBufferable(const ETDDIntent I) noexcept
{
    return WindowFor(I) > 0.0f;
}

// Clear-on-lock matrix (spec §3.4 "Cleared by"):
//   Dodge        -> expiry, Stagger, Dead, Cinematic
//   Jump         -> expiry, Dead
//   Light/Heavy  -> expiry, Stagger, Dead
//   Parry        -> expiry
//   Block        -> release beyond grace
// Encoded as which of {Stagger, Dead, Cinematic} clear each bufferable intent.
enum ETDDClearFlags : std::uint8_t
{
    CLR_None = 0,
    CLR_Stagger = 1u << 0,
    CLR_Dead = 1u << 1,
    CLR_Cinematic = 1u << 2,
};

inline std::uint8_t ClearFlagsFor(const ETDDIntent I) noexcept
{
    switch (I)
    {
    case ETDDIntent::Dodge: return CLR_Stagger | CLR_Dead | CLR_Cinematic;
    case ETDDIntent::Jump: return CLR_Dead;
    case ETDDIntent::LightAttack:
    case ETDDIntent::HeavyAttack: return CLR_Stagger | CLR_Dead;
    case ETDDIntent::Parry: return CLR_None;
    default: return CLR_None;
    }
}

// Which intents a state buffers while its transition requests are locked
// (spec §3.2 Table B "While locked").
inline bool StateBuffersIntent(const char* const StateName, const ETDDIntent I) noexcept
{
    // State names per spec Table B. (String keys keep this table trivially
    // diffable against the spec; the UE wrapper maps ETDDPlayerState -> name.)
    struct Row { const char* State; const ETDDIntent Intents[4]; int N; };
    static const Row Rows[] = {
        { "Idle",        { ETDDIntent::Dodge, ETDDIntent::LightAttack, ETDDIntent::HeavyAttack, ETDDIntent::Jump }, 4 }, // buffer Dodge/Attack; jump via coyote path
        { "Locomotion",  { ETDDIntent::Dodge, ETDDIntent::Jump, ETDDIntent::LightAttack, ETDDIntent::HeavyAttack }, 4 },
        { "Sprint",      { ETDDIntent::Dodge, ETDDIntent::Jump, ETDDIntent::Count, ETDDIntent::Count }, 2 }, // drop Attack
        { "Airborne",    { ETDDIntent::Jump, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 1 }, // drop Attack
        { "Land",        { ETDDIntent::Dodge, ETDDIntent::Jump, ETDDIntent::Count, ETDDIntent::Count }, 2 },
        { "Dodge",       { ETDDIntent::LightAttack, ETDDIntent::HeavyAttack, ETDDIntent::Count, ETDDIntent::Count }, 2 }, // Attack after 0.15 s; drop Dodge
        { "Attack",      { ETDDIntent::LightAttack, ETDDIntent::HeavyAttack, ETDDIntent::Dodge, ETDDIntent::Count }, 3 }, // drop Jump
        { "Block",       { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop Dodge while guard-raising
        { "Parry",       { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all
        { "Stagger",     { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all
        { "Traversal",   { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all except forced
        { "Interaction", { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all
        { "Cinematic",   { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all
        { "Dead",        { ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count, ETDDIntent::Count }, 0 }, // drop all
    };
    for (const Row& R : Rows)
    {
        if (StateName && R.State && std::strcmp(StateName, R.State) == 0)
        {
            for (int K = 0; K < 4; ++K)
            {
                if (K < R.N && R.Intents[K] == I)
                {
                    return true;
                }
            }
            return false;
        }
    }
    return false;
}

/**
 * The buffer itself. One slot per bufferable intent; a press either lands
 * immediately (consumed same frame) or is buffered until expiry/consumption.
 * Time is the game clock in seconds (monotonic).
 */
class FTDDInputBuffer
{
public:
    struct Slot
    {
        bool bActive = false;
        float TimePressed = 0.0f;
    };

    /** Press an intent now. If the slot holds an unexpired press of the same
     *  intent it is REPLACED (new timestamp), never queued behind it. */
    void Press(const ETDDIntent I, const float Now)
    {
        if (!IsBufferable(I))
        {
            bImmediate[static_cast<std::uint8_t>(I)] = true; // consumed by the current frame's processing
            return;
        }
        Slot& S = Slots[static_cast<std::uint8_t>(I)];
        S.bActive = true;
        S.TimePressed = Now;
    }

    void Release(const ETDDIntent I)
    {
        if (I == ETDDIntent::Block)
        {
            bBlockReleased = true; // cleared on the next grace-expiry
            return;
        }
        Slot& S = Slots[static_cast<std::uint8_t>(I)];
        S.bActive = false;
    }

    /**
     * Consume a buffered intent (single consumption). Returns true exactly
     * once per press; a second call after consumption returns false.
     * Expired presses are discarded, not consumed.
     */
    bool Consume(const ETDDIntent I, const float Now)
    {
        if (!IsBufferable(I))
        {
            const std::uint8_t Idx = static_cast<std::uint8_t>(I);
            const bool b = bImmediate[Idx];
            bImmediate[Idx] = false;
            return b;
        }
        Slot& S = Slots[static_cast<std::uint8_t>(I)];
        if (!S.bActive)
        {
            return false;
        }
        if (Now - S.TimePressed > WindowFor(I))
        {
            S.bActive = false; // expired: dropped, not consumed
            return false;
        }
        S.bActive = false;
        return true;
    }

    bool IsBuffered(const ETDDIntent I, const float Now) const
    {
        if (!IsBufferable(I))
        {
            return false;
        }
        const Slot& S = Slots[static_cast<std::uint8_t>(I)];
        return S.bActive && Now - S.TimePressed <= WindowFor(I);
    }

    /** Expire presses past their window (call each tick). */
    void Advance(const float Now)
    {
        for (std::uint8_t I = 0; I < static_cast<std::uint8_t>(ETDDIntent::Count); ++I)
        {
            Slot& S = Slots[I];
            if (S.bActive && Now - S.TimePressed > WindowFor(static_cast<ETDDIntent>(I)))
            {
                S.bActive = false;
            }
        }
    }

    /** Clear-on-lock: a state that locks input clears the intents its lock
     *  clears (spec §3.4 matrix). */
    void ApplyClearOnLock(const std::uint8_t Flags, const float Now)
    {
        for (std::uint8_t I = 0; I < static_cast<std::uint8_t>(ETDDIntent::Count); ++I)
        {
            const ETDDIntent Intent = static_cast<ETDDIntent>(I);
            if (IsBufferable(Intent) && (ClearFlagsFor(Intent) & Flags) != 0)
            {
                Slots[I].bActive = false;
            }
        }
        (void)Now;
    }

    void Reset()
    {
        for (Slot& S : Slots)
        {
            S = Slot{};
        }
        for (bool& B : bImmediate)
        {
            B = false;
        }
        bBlockReleased = false;
    }

    // --- Coyote (AC-25) ---
    /** Jump is accepted up to 0.12 s after leaving the ground (0.15 s window
     *  covers in-air; coyote is the post-grounding slice). AC-25 points:
     *  accept at 0.11 s, reject at 0.13 s. */
    static bool CanAcceptJumpByCoyote(const float TimeSinceLeftGround) noexcept
    {
        return std::isfinite(TimeSinceLeftGround) && TimeSinceLeftGround >= 0.0f &&
               TimeSinceLeftGround <= 0.12f;
    }

private:
    Slot Slots[static_cast<std::int32_t>(ETDDIntent::Count)]{};
    bool bImmediate[static_cast<std::int32_t>(ETDDIntent::Count)]{};
    bool bBlockReleased = false;
};

} // namespace Input
} // namespace TDD
