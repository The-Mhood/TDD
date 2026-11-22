// TDDCalendarSubsystem.h — Phase 1 Igbo calendar (Ọgụàfọ̀).
// Advances the 4-day market week (Eke/Orie/Afo/Nkwo) and exposes the current
// market day, season and day-of-year. Single source of truth for world time.
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "TDDWorldLogic.h"
#include "TDDCalendarSubsystem.generated.h"

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API UTDDCalendarSubsystem : public UTickableWorldSubsystem
{
    GENERATED_BODY()

public:
    UTDDCalendarSubsystem();

    // USubsystem lifecycle: world subsystems use Initialize/Deinitialize,
    // not BeginPlay/EndPlay (which exist only on AActor).
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Tick(float DeltaSeconds) override;

    /** Advance the world clock by one market day. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    void AdvanceDay();

    /** Advance the world clock by N market days. */
    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    void AdvanceDays(int32 Days);

    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    int64 GetWorldDay() const { return WorldDay; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    EMarketDay GetCurrentMarketDay() const { return TDDWorld::MarketDayFromDay(WorldDay); }

    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    ESeason GetCurrentSeason() const { return TDDWorld::SeasonForDay(WorldDay); }

    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    FString GetCurrentMarketDayName() const;

    /** Is today the given settlement's market day? */
    UFUNCTION(BlueprintCallable, Category = "TDD|Calendar")
    bool IsMarketDayFor(const FName& SettlementId) const;

private:
    UPROPERTY(Transient)
    int64 WorldDay = 0;

    /** Seconds per market day (game-time compression; 60s = one 4-day-week day for playability). */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|Calendar", meta = (ClampMin = "1.0", AllowPrivateAccess = "true"))
    float SecondsPerMarketDay = 60.0f;

    float DayTimer = 0.0f;
};
