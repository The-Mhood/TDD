#if WITH_DEV_AUTOMATION_TESTS

#include "Misc/AutomationTest.h"
#include "GameFramework/GameModeBase.h"
#include "TDDGameMode.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
    FTDDProjectGameModeFoundationTest,
    "TDD.Foundation.GameModeClass",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDProjectGameModeFoundationTest::RunTest(const FString& Parameters)
{
    UClass* GameModeClass = ATDDGameMode::StaticClass();

    TestNotNull(TEXT("The project GameMode class is registered"), GameModeClass);
    TestTrue(
        TEXT("The project GameMode derives from AGameModeBase"),
        GameModeClass->IsChildOf(AGameModeBase::StaticClass()));

    return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
