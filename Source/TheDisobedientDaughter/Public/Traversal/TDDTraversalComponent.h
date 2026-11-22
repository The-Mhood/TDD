#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "TDDTraversalComponent.generated.h"

UENUM(BlueprintType)
enum class ETDDTraversalAttemptResult : uint8
{
    None,
    VaultStarted,
    DropStarted,
    RejectedNotCharacter,
    RejectedNotGrounded,
    RejectedCooldown,
    RejectedState,
    RejectedNoSafeRoute
};

/**
 * First runtime traversal slice. Performs capsule-safe forward/overhead/floor
 * queries, routes a vault/drop through the D1 two-phase fallback, and lets
 * CharacterMovementComponent execute the collision-resolved motion.
 */
UCLASS(ClassGroup=(TDD), meta=(BlueprintSpawnableComponent))
class THEDISOBEDIENTDAUGHTER_API UTDDTraversalComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UTDDTraversalComponent();

    UFUNCTION(BlueprintCallable, Category="TDD|Traversal")
    bool TryTraverse();

    UFUNCTION(BlueprintCallable, Category="TDD|Traversal")
    ETDDTraversalAttemptResult GetLastResult() const { return LastResult; }

protected:
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Traversal", meta=(ClampMin="80.0"))
    float ForwardReach = 165.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Traversal", meta=(ClampMin="40.0"))
    float MaxVaultHeight = 115.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Traversal", meta=(ClampMin="0.0"))
    float MaxDropHeight = 220.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category="TDD|Traversal", meta=(ClampMin="0.0"))
    float CooldownSeconds = 0.45f;

private:
    bool FindLandingFloor(class ACharacter* Character, const FVector& Direction,
                          FVector& OutFloorPoint, float& OutHeightDelta) const;
    bool IsVaultPathClear(class ACharacter* Character, const FVector& Direction,
                          const FVector& LandingCenter) const;

    ETDDTraversalAttemptResult LastResult = ETDDTraversalAttemptResult::None;
    float LastAttemptTime = -1.0e30f;
};
