// Copyright (c) 2026. The Disobedient Daughter.
// The engine pin, expressed once so code and tests read the same numbers.
// Authority: docs/03_DECISIONS/ADR-0001 (UE 5.8, C++20). ADR-0001 is Proposed and
// requires Technical Director confirmation; if the pin changes, this header and
// TDD.uproject's EngineAssociation change together, and the change is an ADR.

#pragma once

#include "CoreMinimal.h"

namespace TDD::EnginePin
{
	inline constexpr int32 MajorVersion = 5;
	inline constexpr int32 MinorVersion = 8;

	/** C++ standard required by the architecture (MEAD §2.5). */
	inline constexpr int32 CppStandard = 20;

	/** The association string TDD.uproject must carry. */
	inline constexpr TCHAR Association[] = TEXT("5.8");
}
