// TDDLocationRegistry.cpp — Phase 1 world location/settlement registry.
#include "TDDLocationRegistry.h"

#include "Subsystems/WorldSubsystem.h"

#include "EngineUtils.h"

UTDDLocationRegistry::UTDDLocationRegistry()
{
    // UWorldSubsystem has no PrimaryComponentTick toggle; this subsystem
    // does not override Tick, so the empty base Tick incurs no per-frame cost.
}

void UTDDLocationRegistry::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);

    // Load the Phase-1 Ọmà-valley core settlements from the shared logic core.
    // The logic core is the single source of truth; the registry mirrors it as
    // UE-reflectable records. Coordinates are metres in the logic core -> cm in UE.
    Locations.Reset();
    for (const TDDWorld::FSettlement& S : TDDWorld::OmegaValleySettlements())
    {
        FTDDLocationRecord Rec;
        Rec.Id = FName(S.Id.c_str());
        Rec.Name = S.Name.c_str();
        // ESettlementKind is a global-scope UENUM (UHT requirement), so it is
        // referenced unqualified — TDDWorld::ESettlementKind is not a valid name.
        Rec.Access = (S.Kind == ESettlementKind::Town ||
                      S.Kind == ESettlementKind::MarketTown)
                         ? ETDDLocationAccess::FullyEnterable
                         : ETDDLocationAccess::OpenExterior;
        Rec.MarketDay = S.MarketDay;
        Rec.WorldLocationCm = FVector(S.X * 100.0f, S.Y * 100.0f, 0.0f);
        Rec.ResidentialPopulation = S.Residential;
        Rec.EconomicPopulation = S.Economic;
        Locations.Add(Rec);
    }

    FString Error;
    if (!ValidateRegistry(Error))
    {
        UE_LOG(LogTemp, Error, TEXT("TDD LocationRegistry: invalid settlement set: %s"), *Error);
    }
    else
    {
        UE_LOG(LogTemp, Display,
               TEXT("TDD LocationRegistry: registered %d Ọmà-valley settlements (logical population %d)."),
               Locations.Num(), TDDWorld::RegionalLogicalPopulation());
    }
}

bool UTDDLocationRegistry::FindLocation(const FName& InId, FTDDLocationRecord& OutRecord) const
{
    for (const FTDDLocationRecord& Rec : Locations)
    {
        if (Rec.Id == InId)
        {
            OutRecord = Rec;
            return true;
        }
    }
    OutRecord = FTDDLocationRecord();
    return false;
}

bool UTDDLocationRegistry::ValidateRegistry(FString& OutError) const
{
    if (Locations.Num() == 0)
    {
        OutError = TEXT("registry is empty");
        return false;
    }

    TSet<FName> Seen;
    for (const FTDDLocationRecord& Rec : Locations)
    {
        // TSet::Add returns an FSetElementId (not a bool); the optional
        // out-param reports whether the element was already present.
        bool bAlreadyPresent = false;
        Seen.Add(Rec.Id, &bAlreadyPresent);
        if (bAlreadyPresent)
        {
            OutError = FString::Printf(TEXT("duplicate settlement id '%s'"), *Rec.Id.ToString());
            return false;
        }
        if (Rec.ResidentialPopulation < 0 || Rec.EconomicPopulation < 0)
        {
            OutError = FString::Printf(TEXT("settlement '%s' has negative population"), *Rec.Id.ToString());
            return false;
        }
        if (Rec.ResidentialPopulation + Rec.EconomicPopulation <= 0)
        {
            OutError = FString::Printf(TEXT("settlement '%s' has no population"), *Rec.Id.ToString());
            return false;
        }
    }
    OutError.Empty();
    return true;
}
