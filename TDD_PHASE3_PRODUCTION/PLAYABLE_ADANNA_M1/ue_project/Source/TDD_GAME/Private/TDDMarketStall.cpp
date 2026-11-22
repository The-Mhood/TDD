// TDDMarketStall.cpp — Phase 1 market stall actor.
#include "TDDMarketStall.h"

ATDDMarketStall::ATDDMarketStall()
{
    PrimaryActorTick.bCanEverTick = false;
}

void ATDDMarketStall::BeginPlay()
{
    Super::BeginPlay();
    // Stalls start closed; the market subsystem/level opens them on market day.
    bOpen = false;
}
