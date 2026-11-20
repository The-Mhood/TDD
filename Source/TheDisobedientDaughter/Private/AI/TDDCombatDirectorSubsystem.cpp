#include "AI/TDDCombatDirectorSubsystem.h"

#include "Combat/TDDCombatComponent.h"

UTDDCombatDirectorSubsystem::UTDDCombatDirectorSubsystem()
    : Policy(TDD::AI::FTDDTokenPolicySettings{})
{
}

TStatId UTDDCombatDirectorSubsystem::GetStatId() const
{
    RETURN_QUICK_DECLARE_CYCLE_STAT(UTDDCombatDirectorSubsystem, STATGROUP_Tickables);
}

void UTDDCombatDirectorSubsystem::RegisterEnemy(UTDDCombatComponent* Combatant)
{
    if (Combatant == nullptr || RegisteredEnemies.Contains(TWeakObjectPtr<UTDDCombatComponent>(Combatant)))
    {
        return;
    }
    RegisteredEnemies.Add(TWeakObjectPtr<UTDDCombatComponent>(Combatant));
    SynchronizeRoster();
}

void UTDDCombatDirectorSubsystem::UnregisterEnemy(UTDDCombatComponent* Combatant)
{
    RegisteredEnemies.RemoveAll([Combatant](const TWeakObjectPtr<UTDDCombatComponent>& Item)
    {
        return !Item.IsValid() || Item.Get() == Combatant;
    });
    SynchronizeRoster();
}

void UTDDCombatDirectorSubsystem::SynchronizeRoster()
{
    const std::vector<TDD::AI::FTDDEnemyCandidate>& OldRoster = Policy.Roster();
    std::vector<TDD::AI::FTDDEnemyCandidate> NewRoster;
    NewRoster.reserve(static_cast<size_t>(RegisteredEnemies.Num()));
    for (const TWeakObjectPtr<UTDDCombatComponent>& Weak : RegisteredEnemies)
    {
        UTDDCombatComponent* Combatant = Weak.Get();
        if (Combatant == nullptr || Combatant->GetOwner() == nullptr)
        {
            continue;
        }
        const int32 Id = static_cast<int32>(Combatant->GetUniqueID());
        TDD::AI::FTDDEnemyCandidate Candidate;
        Candidate.Id = Id;
        for (const TDD::AI::FTDDEnemyCandidate& Previous : OldRoster)
        {
            if (Previous.Id == Id)
            {
                Candidate = Previous;
                break;
            }
        }
        NewRoster.push_back(Candidate);
    }
    Policy.SetRoster(NewRoster);
}

void UTDDCombatDirectorSubsystem::Tick(const float DeltaTime)
{
    (void)DeltaTime;
    const int32 OldCount = RegisteredEnemies.Num();
    RegisteredEnemies.RemoveAll([](const TWeakObjectPtr<UTDDCombatComponent>& Item)
    {
        return !Item.IsValid() || Item->GetOwner() == nullptr;
    });
    if (RegisteredEnemies.Num() != OldCount)
    {
        SynchronizeRoster();
    }

    if (GetWorld() == nullptr)
    {
        return;
    }
    const int32 GrantedId = Policy.GrantNext(GetWorld()->GetTimeSeconds());
    if (GrantedId < 0)
    {
        return;
    }
    for (const TWeakObjectPtr<UTDDCombatComponent>& Weak : RegisteredEnemies)
    {
        UTDDCombatComponent* Combatant = Weak.Get();
        if (Combatant != nullptr && static_cast<int32>(Combatant->GetUniqueID()) == GrantedId)
        {
            Combatant->PerformLightAttack();
            break;
        }
    }
}
