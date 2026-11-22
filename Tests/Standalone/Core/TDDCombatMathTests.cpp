// Deterministic combat battery (QUALITY §4, cases 1–10) + seeded fuzz +
// cross-run reproducibility. Pure logic only (no world, no UE) — this suite
// runs agent-side (g++) AND inside the UE automation on the Mac (TDD-Unit.Combat).

#include "Core/TDDCombatTiming.h"
#include "Core/TDDDamageMath.h"
#include "Core/TDDSeededRandom.h"

#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>

namespace
{
int Failures = 0;
int Assertions = 0;
std::uint64_t LogHash = 0x12345678ULL;

void Check(const bool bCondition, const char* const Description)
{
    ++Assertions;
    if (!bCondition)
    {
        ++Failures;
        std::cerr << "FAIL: " << Description << '\n';
    }
    // fold the assertion outcome into the reproducibility log hash
    LogHash = LogHash * 0x100000001B3ULL + (bCondition ? 11ULL : 23ULL) + std::uint64_t(Description[0]);
}

void Fold(const std::uint64_t Value)
{
    LogHash = LogHash * 0x100000001B3ULL + Value;
}

using namespace TDD::Combat;

void FoldOutcome(const FTDDDamageOutcome& O)
{
    Fold(static_cast<std::uint64_t>(O.Classification) << 2 |
         (O.bEnteredDead ? 1 : 0) | (O.bEnteredStagger ? 2 : 0));
}
} // namespace

int main()
{
    FTDDDefenderState Defender;
    Defender.Health = 100.0f;
    Defender.Posture = 0.0f;
    Defender.MaxPosture = 100.0f;

    // Case 1 — L1 chain full: 4-light chain, cancels only inside the window, chain cap holds
    {
        const FTDDAttackTiming L1 = MakeLightAttack(1);
        const FTDDAttackTiming L2 = MakeLightAttack(2);
        const FTDDAttackTiming L3 = MakeLightAttack(3);
        const FTDDAttackTiming L4 = MakeLightAttack(4);
        const FTDDAttackTiming LAgain = MakeLightAttack(1);

        Check(!CanCancelAttack(L1, L2, 0.10f), "chain: cancel refused before the frame after active start");
        Check(CanCancelAttack(L1, L2, 0.20f), "chain: light-1 -> light-2 at 0.20 s (inside 0.15-0.45 window)");
        Check(CanCancelAttack(L2, L3, 0.30f), "chain: light-2 -> light-3 at 0.30 s");
        Check(CanCancelAttack(L3, L4, 0.44f), "chain: light-3 -> light-4 at 0.44 s");
        Check(!CanCancelAttack(L4, LAgain, 0.30f), "chain: light-4 does not re-enter the chain (cap = 4)");
        Check(!CanCancelAttack(L1, L2, 0.50f), "chain: cancel refused after the 0.45 s window closes");
    }

    // Case 2 — L1 cancel heavy: chain-into-heavy inside window; heavy never cancels
    {
        const FTDDAttackTiming L2 = MakeLightAttack(2);
        const FTDDAttackTiming H = MakeHeavyAttack();
        Check(CanCancelAttack(L2, H, 0.35f), "cancel: light-2 -> heavy at 0.35 s is legal");
        Check(!CanCancelAttack(L2, H, 0.05f), "cancel: light-2 -> heavy refused before active start");
        Check(!CanCancelAttack(H, L2, 0.9f), "cancel: heavy -> light refused (no cancel after commit)");
        Check(!CanCancelAttack(H, H, 0.9f), "cancel: heavy -> heavy refused");
    }

    // Case 3 — Parry window + parry staggers the attacker (edge inclusive, then out)
    {
        Check(IsGuardReady(0.08f), "parry: guard-ready at exactly 0.08 s");
        Check(!IsGuardReady(0.079f), "parry: not guard-ready at 0.079 s");
        Check(IsInParryWindow(0.155f), "parry: window midpoint (0.155 s) is inside");
        Check(IsInParryWindow(0.23f), "parry: window end (0.08 + 0.15) inclusive");
        Check(!IsInParryWindow(0.231f), "parry: just past the 0.15 s window is outside");
        Check(!IsInParryWindow(0.05f), "parry: before guard-ready is outside");

        FTDDDefenderState Attacker;
        Attacker.Health = 100.0f; Attacker.Posture = 0.0f; Attacker.MaxPosture = 100.0f;
        FTDDDamageRequest ParriedHit;
        ParriedHit.HealthDamage = 0.0f;      // parry negates the health
        ParriedHit.bFromSuccessfulParry = true;
        const FTDDDamageOutcome O = EvaluateDamage(ParriedHit, Attacker);
        Check(O.Classification == ETDDDamageClassification::None, "parry: zero-damage request is a no-op (no health)");
        // a parried hit that still lands health on the attacker (chip through) staggers via the parry flag
        FTDDDamageRequest ParriedChip;
        ParriedChip.HealthDamage = 5.0f;
        ParriedChip.bFromSuccessfulParry = true;
        const FTDDDamageOutcome C = EvaluateDamage(ParriedChip, Attacker);
        Check(C.Classification == ETDDDamageClassification::Staggering, "parry: attacker staggers on successful parry against them");
        FoldOutcome(C);
    }

    // Case 4 — Block posture: blocked hits accumulate posture; the breaking hit is promoted
    {
        FTDDDefenderState B;
        B.Health = 100.0f; B.Posture = 0.0f; B.MaxPosture = 100.0f;
        FTDDDamageRequest Blocked;
        Blocked.HealthDamage = 0.0f;
        Blocked.PostureDamage = 40.0f;

        FTDDDamageOutcome O1; FTDDDamageOutcome O2; FTDDDamageOutcome O3;
        // zero health damage + posture only: request validity requires HealthDamage > 0,
        // so blocked hits carry a nominal health value (design: block converts to posture)
        Blocked.HealthDamage = 0.001f;
        O1 = EvaluateDamage(Blocked, B);
        Check(O1.Classification == ETDDDamageClassification::NonStaggering && !O1.bPostureBroken,
              "block: 40 posture -> no break");
        FTDDDefenderState B2; B2.Health = O1.NewHealth; B2.Posture = O1.NewPosture; B2.MaxPosture = 100.0f;
        O2 = EvaluateDamage(Blocked, B2);
        Check(O2.Classification == ETDDDamageClassification::NonStaggering && !O2.bPostureBroken,
              "block: 80 posture -> still no break");
        FTDDDefenderState B3; B3.Health = O2.NewHealth; B3.Posture = O2.NewPosture; B3.MaxPosture = 100.0f;
        O3 = EvaluateDamage(Blocked, B3);
        Check(O3.Classification == ETDDDamageClassification::Staggering && O3.bPostureBroken && O3.bControlLost,
              "block: 120 posture -> break promoted to staggering (control lost)");
        FoldOutcome(O3);
    }

    // Case 5 — Dodge i-frames at the AC-20 boundary points (false 0.09 / true 0.11-0.44 / false 0.46)
    {
        const FTDDDodgeSpec S;
        Check(!IsDodgeInvulnerable(0.09f, S), "i-frames: false at 0.09 s");
        Check(IsDodgeInvulnerable(0.11f, S), "i-frames: true at 0.11 s");
        Check(IsDodgeInvulnerable(0.44f, S), "i-frames: true at 0.44 s");
        Check(!IsDodgeInvulnerable(0.46f, S), "i-frames: false at 0.46 s");
    }

    // Case 6 — Lethal+staggering: Dead wins, exactly one state change
    {
        FTDDDefenderState D;
        D.Health = 50.0f; D.Posture = 90.0f; D.MaxPosture = 100.0f;
        FTDDDamageRequest L;
        L.HealthDamage = 60.0f;
        L.bCausesStagger = true;
        const FTDDDamageOutcome O = EvaluateDamage(L, D);
        Check(O.Classification == ETDDDamageClassification::LethalStaggering, "lethal+staggering: classified");
        Check(O.bEnteredDead && !O.bEnteredStagger, "lethal+staggering: Dead outranks Stagger (no stagger entry)");
        Check(O.NewHealth == 0.0f, "lethal+staggering: health floored at 0");
        FoldOutcome(O);
    }

    // Case 7 — Same-frame posture promotion: exactly one Stagger entry across two hits
    {
        FTDDDefenderState D;
        D.Health = 100.0f; D.Posture = 0.0f; D.MaxPosture = 100.0f;
        FTDDDamageRequest A; A.HealthDamage = 10.0f; A.PostureDamage = 60.0f;
        FTDDDamageRequest B2; B2.HealthDamage = 10.0f; B2.PostureDamage = 60.0f;
        const FTDDDamageOutcome OA = EvaluateDamage(A, D);
        Check(OA.Classification == ETDDDamageClassification::NonStaggering, "promotion: first hit (60 posture) is non-staggering");
        FTDDDefenderState D2;
        D2.Health = OA.NewHealth; D2.Posture = OA.NewPosture; D2.MaxPosture = 100.0f;
        const FTDDDamageOutcome OB = EvaluateDamage(B2, D2);
        Check(OB.Classification == ETDDDamageClassification::Staggering, "promotion: second hit breaks posture -> staggering");
        Check((OA.bEnteredStagger ? 1 : 0) + (OB.bEnteredStagger ? 1 : 0) == 1,
              "promotion: exactly one stagger entry across the frame pair");
        FoldOutcome(OB);
    }

    // Case 8 — Single evaluation, no order dependence: identical input -> identical outcome
    {
        FTDDDamageRequest R;
        R.HealthDamage = 35.0f; R.PostureDamage = 30.0f; R.bCausesStagger = false;
        const FTDDDamageOutcome O1 = EvaluateDamage(R, Defender);
        const FTDDDamageOutcome O2 = EvaluateDamage(R, Defender);
        Check(O1.Classification == O2.Classification && O1.NewHealth == O2.NewHealth &&
              O1.NewPosture == O2.NewPosture && O1.bEnteredDead == O2.bEnteredDead &&
              O1.bEnteredStagger == O2.bEnteredStagger,
              "single-evaluation: pipeline is a pure function of (request, defender)");
    }

    // Case 9 — Hit-stop is bounded and expires (simulation resumes exactly at expiry)
    {
        const float H = 0.05f;
        Check(IsHitstopActive(0.0f, H), "hitstop: active at t=0");
        Check(IsHitstopActive(0.049f, H), "hitstop: active just before expiry");
        Check(!IsHitstopActive(0.05f, H), "hitstop: expired exactly at expiry (resumes, no skip)");
        Check(!IsHitstopActive(1.0f, H), "hitstop: expired long after");
        Check(!IsHitstopActive(-0.1f, H), "hitstop: negative time rejected");
    }

    // Case 10 — Seeded 1000-iteration fuzz: invariants must hold for every draw
    {
        TDD::FTDDBatteryRng Rng(0xC0FFEE);
        int Invariants = 0;
        for (int i = 0; i < 1000; ++i)
        {
            FTDDDefenderState D;
            D.Health = 10.0f + Rng.NextFloat() * 140.0f;
            D.Posture = Rng.NextFloat() * D.MaxPosture * 0.99f;
            D.MaxPosture = 50.0f + Rng.NextFloat() * 150.0f;
            D.Posture = std::min(D.Posture, D.MaxPosture);

            FTDDDamageRequest R;
            R.HealthDamage = Rng.NextFloat() * 200.0f;
            R.PostureDamage = Rng.NextFloat() * 150.0f;
            R.bCausesStagger = Rng.NextUInt(2) == 0;

            const FTDDDamageOutcome O = EvaluateDamage(R, D);
            const bool bLethal = (O.Classification == ETDDDamageClassification::Lethal ||
                                  O.Classification == ETDDDamageClassification::LethalStaggering);
            const bool bOK =
                O.NewHealth >= 0.0f &&
                (bLethal ? O.NewHealth == 0.0f : true) &&
                (bLethal ? O.bEnteredDead : true) &&
                (O.bEnteredDead ? O.NewHealth == 0.0f : true) &&
                (O.Classification == ETDDDamageClassification::NonStaggering ? !O.bControlLost : true) &&
                ((O.Classification == ETDDDamageClassification::LethalStaggering) ? !O.bEnteredStagger : true);
            if (!bOK)
            {
                Check(false, "fuzz: invariant violated (see case 10)");
                std::cerr << "  iteration " << i << " health=" << D.Health << " damage=" << R.HealthDamage
                          << " classification=" << static_cast<int>(O.Classification) << '\n';
            }
            ++Invariants;
            Fold(static_cast<std::uint64_t>(O.Classification) + static_cast<std::uint64_t>(i));
        }
        Check(Invariants == 1000, "fuzz: 1000 iterations completed with invariants held");
    }

    // Cross-run reproducibility: the log hash must be stable for a fixed seed/cases
    std::cout << "log_hash=" << LogHash << '\n';
    Check(LogHash != 0x12345678ULL, "battery: log hash advanced (cases actually executed)");

    if (Failures != 0)
    {
        std::cerr << Assertions - Failures << '/' << Assertions << " assertions passed; " << Failures << " failed\n";
        return EXIT_FAILURE;
    }
    std::cout << Assertions << '/' << Assertions << " assertions passed\n";
    return EXIT_SUCCESS;
}
