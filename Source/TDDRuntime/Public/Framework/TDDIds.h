// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

#pragma once

#include "CoreMinimal.h"
#include "TDDIds.generated.h"

/**
 * Canonical identity types for THE DISOBEDIENT DAUGHTER.
 *
 * ARCHITECTURE: Docs/00_MASTER_ENGINEERING_ARCHITECTURE.md section 6.2
 * ADR:          Docs/adr/ADR-0006-canonical-id-scheme.md
 * STATUS:       SPEC — authored 2026-11-16, not yet compiled (no engine in the
 *               authoring environment). See ADR-0005. Do not report as working.
 *
 * WHY THESE EXIST
 * ---------------
 * The Google Drive Art Bible already assigns stable identifiers to every scene,
 * sublocation and interior (see Docs/CANON_INDEX.md):
 *
 *     CH01-SCN-046   scene
 *     CH01-SUB-018   sublocation / microlocation
 *     CH03-INT-001   interior
 *
 * Those identifiers are the primary key of the whole content pipeline. Levels,
 * quests, memory triggers, save records, telemetry events and evidence files all
 * key off them. They are NEVER keyed off display names, because display names
 * are localised and change.
 *
 * Adopting them verbatim (rather than inventing an engine-native scheme) is what
 * makes the published seven-memory table machine-verifiable and keeps save data
 * reconcilable with the Art Bible. See ADR-0006.
 *
 * INVARIANTS
 * ----------
 *  - An Id is an FName holding the canonical string. Never a display name.
 *  - Engineering-proposed ids carry the suffix "-P" and are NOT canon.
 *  - Never construct an id at runtime from concatenation of user-visible text.
 */

/** Three INDEPENDENT approval axes. OAD-47 / OAD-48. Never collapse these. */
UENUM(BlueprintType)
enum class ETDDApprovalState : uint8
{
    /** PROPOSED: exists as a proposal only. Not canon, may not ship. */
    Proposed UMETA(DisplayName = "Proposed"),

    /** Visual design accepted. Does NOT imply the place/person is canon. */
    DesignApproved UMETA(DisplayName = "Design Approved"),

    /** Established story element. Required before any shippable depiction. */
    CanonApproved UMETA(DisplayName = "Canon Approved"),

    /** Passes every gate, including cultural review. May appear in a release. */
    Shippable UMETA(DisplayName = "Shippable")
};

/** The eight chapters, in canon order. Names match the Art Bible registers. */
UENUM(BlueprintType)
enum class ETDDChapter : uint8
{
    None                        UMETA(Hidden),
    Ch01_ForbiddenForest        UMETA(DisplayName = "Ch01 Forbidden Forest"),
    Ch02_KingdomBeneathEarth    UMETA(DisplayName = "Ch02 Kingdom Beneath the Earth"),
    Ch03_CityOfLivingDead       UMETA(DisplayName = "Ch03 City of the Living Dead"),
    Ch04_RiverOfIdemili         UMETA(DisplayName = "Ch04 River of Idemili"),
    Ch05_MountainOfThunder      UMETA(DisplayName = "Ch05 Mountain of Thunder"),
    Ch06_KingdomOfMasks         UMETA(DisplayName = "Ch06 Kingdom of Masks"),
    Ch07_GatesOfTheDead         UMETA(DisplayName = "Ch07 Gates of the Dead"),
    Ch08_LastDaughter           UMETA(DisplayName = "Ch08 The Last Daughter")
};

/**
 * A canon location, scene or interior.
 *
 * The Id is the contract. DisplayName is for editor convenience and localisation
 * and must never be used as a key.
 */
USTRUCT(BlueprintType)
struct FTDDLocationId
{
    GENERATED_BODY()

    /** Canonical register identifier, e.g. "CH04-SUB-002". */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    FName Id;

    /** Engineering convenience only. Not an identity. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    ETDDChapter Chapter = ETDDChapter::None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    ETDDApprovalState Approval = ETDDApprovalState::Proposed;

    FORCEINLINE bool IsSet() const { return !Id.IsNone(); }

    FORCEINLINE bool operator==(const FTDDLocationId& Other) const { return Id == Other.Id; }

    friend FORCEINLINE uint32 GetTypeHash(const FTDDLocationId& Value)
    {
        return GetTypeHash(Value.Id);
    }

    FORCEINLINE FString ToString() const { return Id.ToString(); }
};

/**
 * One of the seven hidden memories of Nneka (Chapters 1-7).
 *
 * Canon: OPEN_ART_DECISIONS OAD-32 and NNEKA_MEMORIES_AND_TIMELINE section 1.
 * A memory is found where a place echoes it; it did not necessarily happen there.
 * Therefore SceneId (the memory scene, played back) and LocationId (where it is
 * discovered) are deliberately separate fields.
 */
USTRUCT(BlueprintType)
struct FTDDMemoryId
{
    GENERATED_BODY()

    /** 1..7, canon order. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon", meta = (ClampMin = "1", ClampMax = "7"))
    int32 Index = 0;

    /** Chapters 1-7 only. A memory in chapter 8 would break the ending gate. */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    ETDDChapter Chapter = ETDDChapter::None;

    /** Playback scene, e.g. "CH01-SCN-046". */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    FName SceneId;

    /** Discovery location, e.g. "CH01-SUB-018". */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Canon")
    FName LocationId;

    FORCEINLINE bool IsSet() const { return Index >= 1 && Index <= 7; }

    FORCEINLINE bool operator==(const FTDDMemoryId& Other) const
    {
        return Index == Other.Index && SceneId == Other.SceneId && LocationId == Other.LocationId;
    }

    friend FORCEINLINE uint32 GetTypeHash(const FTDDMemoryId& Value)
    {
        return HashCombine(GetTypeHash(Value.Index),
                           HashCombine(GetTypeHash(Value.SceneId), GetTypeHash(Value.LocationId)));
    }
};

/**
 * Static helpers for the canonical id scheme.
 *
 * These mirror the validators in Tools/canon/canon_index.py. Keep them in sync:
 * the L0 gate is the authority for what a valid id looks like, and this class
 * exists so runtime code can fail loudly instead of carrying a typo through to
 * the save file.
 */
class TDDRUNTIME_API FTDDCanonIds
{
public:
    static constexpr int32 NumChapters = 8;
    static constexpr int32 NumMemories = 7;

    /** "CH01".."CH08". Returns an empty string for None/out-of-range. */
    static FString ChapterId(ETDDChapter Chapter);

    /** "CH01" -> Ch01_..., otherwise None. */
    static ETDDChapter ParseChapter(const FString& Prefix);

    /** True if Id matches CHxx-SCN-yyy, CHxx-SUB-yyy or CHxx-INT-yyy. */
    static bool IsValidLocationId(const FString& Id);

    /** True if Id matches CHxx-BOSS-<Name>. */
    static bool IsValidBossId(const FString& Id);

    /** True if Id carries the engineering-proposal suffix "-P". */
    static bool IsEngineeringProposal(const FString& Id);

    /** The chapter prefix of a valid id, or an empty string. */
    static FString ChapterOf(const FString& Id);

    /**
     * Memories live in Chapters 1-7 only (OAD-32). Returns false for Ch08.
     * This is a canon rule, not a convenience check.
     */
    static bool IsValidMemoryChapter(ETDDChapter Chapter);

    /** Round-trip validation used by tests and by the import tool. */
    static bool ValidateMemoryId(const FTDDMemoryId& Memory);
};
