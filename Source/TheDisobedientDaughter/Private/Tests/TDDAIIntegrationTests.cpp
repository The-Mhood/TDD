#if WITH_DEV_AUTOMATION_TESTS

#include "AI/TDDBossPhaseComponent.h"
#include "Misc/AutomationTest.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDBossPhaseAssetAdapterTest,
    "TDD.W1D2.AI.BossPhaseAssetAdapter",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDBossPhaseAssetAdapterTest::RunTest(const FString& Parameters)
{
    UTDDBossPhaseGraphAsset* Asset = NewObject<UTDDBossPhaseGraphAsset>(GetTransientPackage());
    TestNotNull(TEXT("Transient authoring graph object created"), Asset);
    if (Asset == nullptr)
    {
        return false;
    }

    FTDDBossPhaseData Entry;
    Entry.PhaseName = TEXT("Entry");
    FTDDBossPhaseTransitionData EntryTransition;
    EntryTransition.Kind = ETDDBossTransition::HealthPct;
    EntryTransition.Threshold = 0.5f;
    EntryTransition.TargetPhase = TEXT("Defeat");
    Entry.Transitions.Add(EntryTransition);

    FTDDBossPhaseData Defeat;
    Defeat.PhaseName = TEXT("Defeat");
    Asset->Phases = { Entry, Defeat };
    Asset->EntryPhase = TEXT("Entry");
    Asset->DefeatPhase = TEXT("Defeat");
    Asset->TerminalPhases = { TEXT("Defeat") };

    TDD::AI::FTDDBossPhaseGraph PureGraph;
    FString Error;
    TestTrue(TEXT("Unreal data asset converts through the shared pure graph validator"),
             Asset->BuildPureGraph(PureGraph, Error));
    TestTrue(TEXT("Valid graph conversion has no error string"), Error.IsEmpty());

    TDD::AI::FTDBossSnapshot Snapshot;
    Snapshot.HealthPct = 0.4f;
    TestTrue(TEXT("Converted graph uses the same first-satisfied pure selector"),
             TDD::AI::SelectNextPhase(PureGraph, "Entry", Snapshot) == "Defeat");
    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
