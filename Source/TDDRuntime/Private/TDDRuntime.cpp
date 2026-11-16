// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

#include "TDDRuntime.h"
#include "Modules/ModuleManager.h"

DEFINE_LOG_CATEGORY(LogTDD);
DEFINE_LOG_CATEGORY(LogTDDCombat);
DEFINE_LOG_CATEGORY(LogTDDMemory);
DEFINE_LOG_CATEGORY(LogTDDCanon);
DEFINE_LOG_CATEGORY(LogTDDBoss);
DEFINE_LOG_CATEGORY(LogTDDSave);

/**
 * Primary game module.
 *
 * STATUS: SPEC (Stage 1). Deliberately almost empty: it registers log
 * categories and nothing else. Gameplay systems are added per stage, each with
 * a test, so that no stage ships an untested subsystem.
 */
IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, TDDRuntime, "TDDRuntime");
