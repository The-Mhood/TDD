#include "AI/TDDTrainingBoss.h"

#include "AI/TDDBossPhaseComponent.h"

ATDDTrainingBoss::ATDDTrainingBoss()
{
    BossPhaseComponent = CreateDefaultSubobject<UTDDBossPhaseComponent>(TEXT("BossPhaseGraph"));
}
