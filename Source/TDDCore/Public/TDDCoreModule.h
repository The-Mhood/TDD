// Copyright (c) 2026. The Disobedient Daughter.
#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleInterface.h"

/** TDDCore: the leaf module. Every other module may depend on it; it depends on nothing of ours. */
class TDDCORE_API FTDDCoreModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
