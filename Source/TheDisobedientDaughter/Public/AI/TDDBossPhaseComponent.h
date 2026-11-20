#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/DataAsset.h"
#include "AI/TDDAIPureCore.h"
#include "TDDBossPhaseComponent.generated.h"

UENUM(BlueprintType)
enum class ETDDBossTransition : uint8
{
    PoiseBreak,
    HealthPct,
    ElapsedSec,
    Distance,
    PlayerAbility,
    MemoryFound,
    Event
};

USTRUCT(BlueprintType)
struct FTDDBossPhaseTransitionData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    ETDDBossTransition Kind = ETDDBossTransition::HealthPct;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float Threshold = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName TargetPhase;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, meta=(EditCondition="Kind == ETDDBossTransition::Event"))
    FName EventName;
};

USTRUCT(BlueprintType)
struct FTDDBossPhaseData
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName PhaseName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    TArray<FTDDBossPhaseTransitionData> Transitions;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName MusicState;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    FName CameraProfile;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    TArray<FName> AbilitySet;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    TArray<FName> ArenaStates;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    bool bInvulnerable = false;
};

UCLASS(BlueprintType)
class THEDISOBEDIENTDAUGHTER_API UTDDBossPhaseGraphAsset : public UPrimaryDataAsset
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Boss Phase Graph")
    TArray<FTDDBossPhaseData> Phases;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Boss Phase Graph")
    FName EntryPhase;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Boss Phase Graph")
    FName DefeatPhase;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="Boss Phase Graph")
    TArray<FName> TerminalPhases;

    bool BuildPureGraph(TDD::AI::FTDDBossPhaseGraph& OutGraph, FString& OutError) const;
};

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FTDDBossPhaseChanged, FName, PreviousPhase, FName, NewPhase);

/**
 * Runtime adapter for a data-authored boss graph. Game systems feed snapshots
 * and events here; the pure selector remains authoritative for transitions.
 */
UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class THEDISOBEDIENTDAUGHTER_API UTDDBossPhaseComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTDDBossPhaseComponent();
    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void SetHealthPercent(float Value);

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void NotifyPoiseBreak();

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void SetDistanceToPlayer(float Distance);

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void SetPlayerAbilityReady(bool bReady);

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void SetMemoriesFound(int32 Count);

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    void NotifyBossEvent(FName EventName);

    UFUNCTION(BlueprintCallable, Category="TDD|Boss")
    FName GetCurrentPhase() const { return CurrentPhase; }

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Boss")
    TObjectPtr<UTDDBossPhaseGraphAsset> PhaseGraph;

    UPROPERTY(BlueprintAssignable, Category="TDD|Boss")
    FTDDBossPhaseChanged OnPhaseChanged;

private:
    void EvaluateTransitions();

    TDD::AI::FTDDBossPhaseGraph RuntimeGraph;
    TDD::AI::FTDBossSnapshot Snapshot;
    FName CurrentPhase;
    bool bGraphValid = false;
};
