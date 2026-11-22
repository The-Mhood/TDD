// TDDLocationRegistry.h — Phase 1 world location/settlement registry.
// Implements the WORLD_ARCHITECTURE UTDDLocationRegistry contract: loads the
// Ọmà-valley settlement set, resolves ids to records, exposes access level and
// market-day, and validates the set at subsystem Initialize.
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TDDWorldLogic.h"
#include "TDDLocationRegistry.generated.h"

UENUM(BlueprintType)
enum class ETDDLocationAccess : uint8
{
    OpenExterior,
    FullyEnterable,
    BackgroundEnvironment
};

USTRUCT(BlueprintType)
struct FTDDLocationRecord
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName Id;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    ETDDLocationAccess Access = ETDDLocationAccess::FullyEnterable;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    EMarketDay MarketDay = EMarketDay::Eke;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FVector WorldLocationCm = FVector::ZeroVector;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 ResidentialPopulation = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    int32 EconomicPopulation = 0;
};

UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class TDD_GAME_API UTDDLocationRegistry : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDLocationRegistry();

    // USubsystem lifecycle: world subsystems use Initialize/Deinitialize,
    // not BeginPlay/EndPlay (which exist only on AActor).
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    /** Number of settlements registered for the current region. */
    UFUNCTION(BlueprintCallable, Category = "TDD|World")
    int32 GetLocationCount() const { return Locations.Num(); }

    /** Look up a settlement record by id. Returns true and fills OutRecord if found; false if absent. */
    UFUNCTION(BlueprintCallable, Category = "TDD|World")
    bool FindLocation(const FName& InId, FTDDLocationRecord& OutRecord) const;

    /** All registered settlement records. */
    UFUNCTION(BlueprintCallable, Category = "TDD|World")
    const TArray<FTDDLocationRecord>& GetLocations() const { return Locations; }

    /** Validate the registered set (ids unique, populations sane). Returns true if valid. */
    UFUNCTION(BlueprintCallable, Category = "TDD|World")
    bool ValidateRegistry(FString& OutError) const;

private:
    UPROPERTY(Transient)
    TArray<FTDDLocationRecord> Locations;
};
