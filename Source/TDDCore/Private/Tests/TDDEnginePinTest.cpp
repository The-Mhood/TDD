// Copyright (c) 2026. The Disobedient Daughter.
// First automation test in the project. It tests a fact the repository controls —
// the engine pin — so it is a genuine assertion, not a green placeholder. It is
// IMPLEMENTED_UNVERIFIED: no engine is installed in the authoring workspace, so this
// test has never been compiled or run (see docs/06_IMPLEMENTATION/UNREAL_PROJECT_FOUNDATION_V1.md).

#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "TDDEnginePin.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FTDDEnginePinTest,
	"TDD-Unit.Canon.EnginePin",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTDDEnginePinTest::RunTest(const FString& Parameters)
{
	TestEqual(TEXT("Engine major version is pinned by ADR-0001"), TDD::EnginePin::MajorVersion, 5);
	TestEqual(TEXT("Engine minor version is pinned by ADR-0001"), TDD::EnginePin::MinorVersion, 8);
	TestEqual(TEXT("Project requires C++20 (MEAD 2.5)"), TDD::EnginePin::CppStandard, 20);
	TestEqual(TEXT("Association string matches TDD.uproject"), FString(TDD::EnginePin::Association), FString(TEXT("5.8")));
	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
