#include "AI/TDDBossPhaseComponent.h"

namespace
{
TDD::AI::ETDDTransitionKind ToPureKind(const ETDDBossTransition Kind)
{
    return static_cast<TDD::AI::ETDDTransitionKind>(static_cast<uint8>(Kind));
}
}

bool UTDDBossPhaseGraphAsset::BuildPureGraph(TDD::AI::FTDDBossPhaseGraph& OutGraph, FString& OutError) const
{
    OutGraph = TDD::AI::FTDDBossPhaseGraph{};
    OutGraph.EntryPhase = TCHAR_TO_UTF8(*EntryPhase.ToString());
    OutGraph.DefeatPhase = TCHAR_TO_UTF8(*DefeatPhase.ToString());
    for (const FName& Terminal : TerminalPhases)
    {
        OutGraph.TerminalPhases.emplace_back(TCHAR_TO_UTF8(*Terminal.ToString()));
    }
    for (const FTDDBossPhaseData& Source : Phases)
    {
        TDD::AI::FTDDPhaseDefinition Phase;
        Phase.PhaseName = TCHAR_TO_UTF8(*Source.PhaseName.ToString());
        Phase.MusicState = TCHAR_TO_UTF8(*Source.MusicState.ToString());
        Phase.CameraProfile = TCHAR_TO_UTF8(*Source.CameraProfile.ToString());
        Phase.bInvulnerable = Source.bInvulnerable;
        for (const FName& Ability : Source.AbilitySet)
        {
            Phase.AbilitySet.emplace_back(TCHAR_TO_UTF8(*Ability.ToString()));
        }
        for (const FName& ArenaState : Source.ArenaStates)
        {
            Phase.ArenaStates.emplace_back(TCHAR_TO_UTF8(*ArenaState.ToString()));
        }
        for (const FTDDBossPhaseTransitionData& SourceTransition : Source.Transitions)
        {
            TDD::AI::FTDDPhaseTransition Transition;
            Transition.Kind = ToPureKind(SourceTransition.Kind);
            Transition.Threshold = SourceTransition.Threshold;
            Transition.TargetPhase = TCHAR_TO_UTF8(*SourceTransition.TargetPhase.ToString());
            Transition.EventName = TCHAR_TO_UTF8(*SourceTransition.EventName.ToString());
            Phase.Transitions.push_back(MoveTemp(Transition));
        }
        OutGraph.Phases.push_back(MoveTemp(Phase));
    }

    const TDD::AI::FTDDGraphValidation Validation = TDD::AI::ValidateBossGraph(OutGraph);
    if (!Validation.bOk)
    {
        OutError.Reset();
        for (const std::string& Error : Validation.Errors)
        {
            OutError += FString::Printf(TEXT("%s; "), UTF8_TO_TCHAR(Error.c_str()));
        }
        return false;
    }
    OutError.Reset();
    return true;
}

UTDDBossPhaseComponent::UTDDBossPhaseComponent()
{
    PrimaryComponentTick.bCanEverTick = true;
}

void UTDDBossPhaseComponent::BeginPlay()
{
    Super::BeginPlay();
    if (PhaseGraph == nullptr)
    {
        UE_LOG(LogTemp, Warning, TEXT("%s has no boss phase graph asset"), *GetNameSafe(GetOwner()));
        return;
    }
    FString Error;
    bGraphValid = PhaseGraph->BuildPureGraph(RuntimeGraph, Error);
    if (!bGraphValid)
    {
        UE_LOG(LogTemp, Error, TEXT("Invalid boss phase graph on %s: %s"),
            *GetNameSafe(GetOwner()), *Error);
        return;
    }
    CurrentPhase = PhaseGraph->EntryPhase;
}

void UTDDBossPhaseComponent::TickComponent(const float DeltaTime, const ELevelTick TickType,
                                            FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    if (!bGraphValid || !FMath::IsFinite(DeltaTime) || DeltaTime <= 0.0f)
    {
        return;
    }
    Snapshot.ElapsedSec += DeltaTime;
    EvaluateTransitions();
}

void UTDDBossPhaseComponent::SetHealthPercent(const float Value)
{
    if (FMath::IsFinite(Value))
    {
        Snapshot.HealthPct = FMath::Clamp(Value, 0.0f, 1.0f);
        EvaluateTransitions();
    }
}

void UTDDBossPhaseComponent::NotifyPoiseBreak()
{
    Snapshot.bPoiseBroken = true;
    EvaluateTransitions();
    Snapshot.bPoiseBroken = false;
}

void UTDDBossPhaseComponent::SetDistanceToPlayer(const float Distance)
{
    if (FMath::IsFinite(Distance) && Distance >= 0.0f)
    {
        Snapshot.DistanceToPlayer = Distance;
        EvaluateTransitions();
    }
}

void UTDDBossPhaseComponent::SetPlayerAbilityReady(const bool bReady)
{
    Snapshot.bPlayerAbilityReady = bReady;
    EvaluateTransitions();
}

void UTDDBossPhaseComponent::SetMemoriesFound(const int32 Count)
{
    Snapshot.MemoriesFound = FMath::Max(0, Count);
    EvaluateTransitions();
}

void UTDDBossPhaseComponent::NotifyBossEvent(const FName EventName)
{
    if (!EventName.IsNone())
    {
        Snapshot.Events.emplace_back(TCHAR_TO_UTF8(*EventName.ToString()));
        EvaluateTransitions();
        Snapshot.Events.clear();
    }
}

bool UTDDBossPhaseComponent::IsCurrentPhaseInvulnerable() const
{
    if (PhaseGraph == nullptr || CurrentPhase.IsNone())
    {
        return false;
    }
    for (const FTDDBossPhaseData& Phase : PhaseGraph->Phases)
    {
        if (Phase.PhaseName == CurrentPhase)
        {
            return Phase.bInvulnerable;
        }
    }
    return false;
}

void UTDDBossPhaseComponent::EvaluateTransitions()
{
    if (!bGraphValid || CurrentPhase.IsNone())
    {
        return;
    }
    const std::string Next = TDD::AI::SelectNextPhase(
        RuntimeGraph, TCHAR_TO_UTF8(*CurrentPhase.ToString()), Snapshot);
    const FName NextName(UTF8_TO_TCHAR(Next.c_str()));
    if (NextName != CurrentPhase)
    {
        const FName Previous = CurrentPhase;
        CurrentPhase = NextName;
        Snapshot.ElapsedSec = 0.0f;
        OnPhaseChanged.Broadcast(Previous, CurrentPhase);
    }
}
