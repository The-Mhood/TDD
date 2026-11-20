# ADR-0007 — Declarative boss phase graphs

- **Status:** ACCEPTED
- **Date:** 2026-11-16
- **Owner:** Agent 2 (World, Systems, AI)
- **Affects:** Agent 1 (damage/feedback), Agent 3 (UI, telemetry, music state)

## Context

The game has eight boss encounters (Directive §2; encounter existence is ESTABLISHED per OAD-21):

| Ch | Boss |
|---|---|
| 1 | Great Root Mother |
| 2 | Iron Elephant |
| 3 | King Without a Face |
| 4 | Daughter of the Deep |
| 5 | Amadioha's Champion |
| 6 | Mother of Masks |
| 7 | Hollow King |
| 8 | Ezeani (three endings) |

If each boss is bespoke C++ (or a bespoke, sprawling Blueprint), the project pays the cost eight times:
eight debugging surfaces, eight integration surfaces for three agents, and every tuning pass requires an
engineer. Bosses are also the most iterated content in an action-adventure — thresholds, telegraphs and
arena states change constantly during playtesting.

Meanwhile arena layouts are **PROPOSED, not approved** (OAD-21), so the *logic* must not be welded to a
specific arena layout.

## Decision

Bosses are **data**, executed by a single controller.

```cpp
// TDD/Combat/TDDBossTypes.h — SPEC
USTRUCT(BlueprintType)
struct FTDDPhaseTransition
{
    /** Evaluated in order; first satisfied wins. */
    UPROPERTY(EditAnywhere) ETDDTransitionKind Kind;      // PoiseBreak, HealthPct, ElapsedSec, Distance,
                                                          // PlayerAbility, MemoryFound, Event
    UPROPERTY(EditAnywhere) float Threshold;
    UPROPERTY(EditAnywhere) FName TargetPhase;
};

USTRUCT(BlueprintType)
struct FTDDPhaseDefinition
{
    UPROPERTY(EditAnywhere) FName PhaseName;
    UPROPERTY(EditAnywhere) TArray<FTDDPhaseTransition> Transitions;
    UPROPERTY(EditAnywhere) FGameplayTag MusicState;
    UPROPERTY(EditAnywhere) FName CameraProfile;
    UPROPERTY(EditAnywhere) TArray<FName> AbilitySet;
    UPROPERTY(EditAnywhere) TArray<FName> ArenaStates;     // e.g. Env.Ch01.RootsOpen
    UPROPERTY(EditAnywhere) bool bInvulnerable;
};

UCLASS() class UTDDBossPhaseGraph : public UPrimaryDataAsset
{
    UPROPERTY(EditAnywhere) TArray<FTDDPhaseDefinition> Phases;
    UPROPERTY(EditAnywhere) FName EntryPhase;
    UPROPERTY(EditAnywhere) FName DefeatPhase;
    /** Must be reachable; validated. */
    UPROPERTY(EditAnywhere) TArray<FName> TerminalPhases;
};
```

`UTDDBossController` executes the graph. **It contains no boss-specific branching.** A boss is:
an actor + a `UTDDBossPhaseGraph` asset + ability set assets + an arena actor.

Two mandatory architecture tests:

1. **Graph reachability:** every phase is reachable from `EntryPhase`; no dead-end phase except terminals;
   every transition target exists; no cycles that prevent termination.
2. **Data-only second boss:** The Iron Elephant must be expressible as a *new asset* with **no new code**.
   If it cannot be, the graph schema is inadequate and must be fixed in Stage 5 — not worked around.

## Consequences

**Positive**
- Eight bosses for roughly the cost of one and a half, in engineering terms.
- Designers iterate phases/thresholds without an engineer or a compile.
- Arena-agnostic: arena layouts can change (they are only PROPOSED) without touching boss logic.
- Music state, camera profile and arena states are wired through the same data, so audio/UI/boss stay in step.
- Testable without a renderer: a pure function over a phase snapshot.

**Negative / risks**
- Some bosses will need behaviour a generic graph cannot express. Mitigation: the graph supports an `Event`
  transition and an ability set per phase; genuinely unique mechanics are implemented as *abilities*
  (reusable) rather than boss-specific controller code. If a boss still cannot fit, that is an ADR.
- Six of eight bosses are now "content-shaped", which can under-represent signature mechanics. Mitigation:
  the Creative Director reviews each boss's phase list before production.
- The schema will need extension (e.g. multi-target phases for the Hidden King). Versioned schema + migration.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Bespoke C++ per boss | 8× cost, 8× integration risk, tuning requires engineers |
| Blueprint-per-boss | Same cost problem plus review/merge difficulty across three agents |
| Behaviour-tree-per-boss with no phase concept | Loses explicit, authorable phase structure and music/camera coordination |
| Third-party boss framework plugin | Unvetted dependency; does not fit our state/tag architecture |
