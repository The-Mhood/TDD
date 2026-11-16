// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

#pragma once

#include "CoreMinimal.h"

/**
 * Module log categories.
 *
 * Use a category, never LogTemp, so evidence logs can be filtered and so a
 * production build can strip verbose noise. Declared here, defined once.
 */
DECLARE_LOG_CATEGORY_EXTERN(LogTDD, Log, All);
DECLARE_LOG_CATEGORY_EXTERN(LogTDDCombat, Log, All);
DECLARE_LOG_CATEGORY_EXTERN(LogTDDMemory, Log, All);
DECLARE_LOG_CATEGORY_EXTERN(LogTDDCanon, Log, All);
DECLARE_LOG_CATEGORY_EXTERN(LogTDDBoss, Log, All);
DECLARE_LOG_CATEGORY_EXTERN(LogTDDSave, Log, All);
