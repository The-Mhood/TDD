// TDDMarketStall.h — Phase 1 market stall actor.
// Represents one trader's stall with goods. Open on the settlement's market day;
// closed (collapsed) on ordinary days. Goods are data-driven per settlement
// product identity.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TDDMarketStall.generated.h"

UCLASS(ClassGroup=(TDD))
class TDD_GAME_API ATDDMarketStall : public AActor
{
    GENERATED_BODY()

public:
    ATDDMarketStall();

    virtual void BeginPlay() override;

    UFUNCTION(BlueprintCallable, Category = "TDD|Market")
    bool IsOpen() const { return bOpen; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Market")
    void SetOpen(bool bInOpen) { bOpen = bInOpen; }

    UFUNCTION(BlueprintCallable, Category = "TDD|Market")
    const FString& GetGoods() const { return Goods; }

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|Market")
    FString TraderName = TEXT("trader");

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "TDD|Market")
    FString Goods = TEXT("yam");

    UPROPERTY(Transient, BlueprintReadOnly, Category = "TDD|Market")
    bool bOpen = false;
};
