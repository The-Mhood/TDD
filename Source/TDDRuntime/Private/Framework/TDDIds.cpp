// Copyright (c) THE DISOBEDIENT DAUGHTER. All rights reserved.

#include "Framework/TDDIds.h"

// STATUS: SPEC — authored 2026-11-16, not compiled. See ADR-0005.

namespace
{
    // Mirror of the patterns in Tools/canon/canon_index.py. If either changes,
    // the L0 gate in Tools/canon/tests must change with it.
    const TCHAR* LocationPattern = TEXT("^CH0[1-8]-(SCN|SUB|INT)-[0-9]{3}$");
    const TCHAR* BossPattern = TEXT("^CH0[1-8]-BOSS-[A-Z][A-Za-z0-9]*$");

    void CollectChapters(TArray<FString>& Out)
    {
        Out.Reset(FTDDCanonIds::NumChapters);
        for (int32 Index = 1; Index <= FTDDCanonIds::NumChapters; ++Index)
        {
            Out.Add(FString::Printf(TEXT("CH%02d"), Index));
        }
    }
}

FString FTDDCanonIds::ChapterId(ETDDChapter Chapter)
{
    const int32 Index = static_cast<int32>(Chapter);
    if (Index < static_cast<int32>(ETDDChapter::Ch01_ForbiddenForest) ||
        Index > static_cast<int32>(ETDDChapter::Ch08_LastDaughter))
    {
        return FString();
    }
    return FString::Printf(TEXT("CH%02d"), Index);
}

ETDDChapter FTDDCanonIds::ParseChapter(const FString& Prefix)
{
    for (int32 Index = 1; Index <= NumChapters; ++Index)
    {
        if (Prefix.Equals(FString::Printf(TEXT("CH%02d"), Index), ESearchCase::CaseSensitive))
        {
            return static_cast<ETDDChapter>(Index);
        }
    }
    return ETDDChapter::None;
}

bool FTDDCanonIds::IsValidLocationId(const FString& Id)
{
    FRegexPattern Pattern(LocationPattern);
    FRegexMatcher Matcher(Pattern, Id);
    return Matcher.FindNext();
}

bool FTDDCanonIds::IsValidBossId(const FString& Id)
{
    FRegexPattern Pattern(BossPattern);
    FRegexMatcher Matcher(Pattern, Id);
    return Matcher.FindNext();
}

bool FTDDCanonIds::IsEngineeringProposal(const FString& Id)
{
    return Id.EndsWith(TEXT("-P"), ESearchCase::CaseSensitive) && Id.Len() > 2;
}

FString FTDDCanonIds::ChapterOf(const FString& Id)
{
    // A valid id always begins with CHxx.
    return Id.Len() >= 4 ? Id.Left(4) : FString();
}

bool FTDDCanonIds::IsValidMemoryChapter(ETDDChapter Chapter)
{
    const int32 Index = static_cast<int32>(Chapter);
    return Index >= static_cast<int32>(ETDDChapter::Ch01_ForbiddenForest) &&
           Index <= static_cast<int32>(ETDDChapter::Ch07_GatesOfTheDead);
}

bool FTDDCanonIds::ValidateMemoryId(const FTDDMemoryId& Memory)
{
    if (!Memory.IsSet())
    {
        return false;
    }
    if (!IsValidMemoryChapter(Memory.Chapter))
    {
        // OAD-32: memories occupy Chapters 1-7 only.
        return false;
    }
    if (!IsValidLocationId(Memory.SceneId.ToString()) &&
        !IsValidBossId(Memory.SceneId.ToString()))
    {
        return false;
    }
    if (!IsValidLocationId(Memory.LocationId.ToString()))
    {
        return false;
    }
    // Both ids must live in the memory's declared chapter.
    const FString Expected = ChapterId(Memory.Chapter);
    if (!Expected.IsEmpty())
    {
        if (ChapterOf(Memory.SceneId.ToString()) != Expected ||
            ChapterOf(Memory.LocationId.ToString()) != Expected)
        {
            return false;
        }
    }
    return true;
}
