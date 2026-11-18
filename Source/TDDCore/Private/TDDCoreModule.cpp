// Copyright (c) 2026. The Disobedient Daughter.

#include "TDDCoreModule.h"
#include "TDDEnginePin.h"
#include "TDDLog.h"
#include "Modules/ModuleManager.h"

void FTDDCoreModule::StartupModule()
{
	UE_LOG(LogTDD, Log, TEXT("TDDCore started. Engine pin %s (C++%d). Contract: C-05 successor A1-C05-S4.3.11, DESIGN_ONLY."),
		TDD::EnginePin::Association, TDD::EnginePin::CppStandard);
}

void FTDDCoreModule::ShutdownModule()
{
}

IMPLEMENT_MODULE(FTDDCoreModule, TDDCore)
