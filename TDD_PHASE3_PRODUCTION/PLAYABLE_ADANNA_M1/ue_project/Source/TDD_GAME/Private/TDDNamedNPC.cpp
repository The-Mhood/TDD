// TDDNamedNPC.cpp — Phase 1 Tier-1 named NPC actor.
#include "TDDNamedNPC.h"

ATDDNamedNPC::ATDDNamedNPC()
{
    PrimaryActorTick.bCanEverTick = true;
}

void ATDDNamedNPC::BeginPlay()
{
    Super::BeginPlay();
}

void ATDDNamedNPC::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    // Named tier runs full routine/animation. The market-day presence flag
    // (bAtMarket) is driven by the level when it spawns named actors on the
    // settlement's market day; the routine string reflects ordinary vs market
    // activity for dialogue/description consumers.
}
