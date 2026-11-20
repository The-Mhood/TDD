# CODING STANDARDS — THE DISOBEDIENT DAUGHTER

Mandatory for all agents. Deviations require a comment in code plus a note in the phase report. These exist because three agents write into one codebase with no compiler in the loop.

## 1. Language and structure

- C++20, Unreal coding style (PascalCase types, `b` prefix for bools, tabs, 120-col soft limit).
- **IWYU**: include exactly what you use. No `Engine.h`, no `CoreMinimal.h` where a narrower include exists (allowed only in module PCH via `PrivatePCHHeaderFile`).
- Forward-declare in headers; include in `.cpp`. Public headers must not pull in module-private headers.
- Every `UCLASS`/`USTRUCT` gets the correct export macro (`TDDGAMEPLAY_API`, `TDDAI_API`, …) — a missing macro is a linker error at a phase gate, not a style nit.
- Blueprints are for content wiring and data authoring. **Gameplay rules live in C++.** (ADR-0002)

## 2. Naming

| Kind | Pattern | Example |
|---|---|---|
| Actor | `ATDD<Thing>` | `ATDDPlayerCharacter` |
| Component | `UTDD<Thing>Component` | `UTDDCombatComponent` |
| Subsystem | `UTDD<Thing>Subsystem` | `UTDDMemorySubsystem` |
| Data asset | `UTDD<Thing>Definition` / `UTDD<Thing>Fragment` | `UTDDAttackDefinition` |
| Struct | `FTDD<Thing>` | `FTDDDamageRequest` |
| Enum | `ETDD<Thing>` | `ETDDCombatState` (values `PascalCase`, prefix-free) |
| Interface | `ITDD<Thing>` (`UINTERFACE` `UTDD<Thing>`) | `ITDDInteractable` |
| Anim notify | `AN_TDD<Thing>` / `ANS_TDD<Thing>` | `ANS_TDDHitWindow` |
| Log category | `LogTDD<Module>` | `LogTDDCombat` |
| Asset | `DA_`, `PDA_`, `DT_`, `BP_`, `L_`, `LS_`, `AM_`, `ABP_`, `ST_`, `EQS_`, `NS_`, `MS_`, `W_` | `DA_Attack_Light01` |

Gameplay tags: `Domain.Category.Item` (`State.Combat.Attacking`, `Damage.Physical.Slash`, `Narrative.Memory.03.Found`). Tags are **content-stable**: renaming a tag that is persisted requires a save-migration entry.

## 3. Tick and performance discipline

- `Tick` must be justified in a comment (`// Tick: required for X because Y`). Default to timers, delegates and event-driven updates.
- AI and NPC ticks are rate-limited per archetype. Player tick budget: ≤ 0.3 ms.
- No `GetAllActorsOfClass` / `TActorIterator` in runtime gameplay paths. Use registries (`UTDD*Registry`) populated on spawn/despawn.
- No `LoadObject`/synchronous load during gameplay. Soft references + `UAssetManager` async load, always with an error path.
- No string comparisons in hot paths; use tags, IDs and `FName`.
- Allocation: avoid per-frame `TArray` allocations in combat/AI; use reserved buffers owned by the component.

## 4. Error handling and logging

- Log with a named category, a verbosity appropriate to shipping, and enough context to identify the asset: `UE_LOG(LogTDDNarrative, Error, TEXT("Memory %d has no presentation asset (%s)"), Index, *GetName());`
- `check()` for programmer invariants; `ensure()`/`ensureMsgf()` for recoverable content errors that must surface in QA; **never** `check()` on anything a designer can author wrongly.
- No empty `if (!Ptr) return;` that hides a content error. Log, then degrade.
- Shipping builds must not log spam; Development/Test builds must be loud.

## 5. Data and canon

- Every content asset carries `FTDDCanonReference` (Art Bible asset ID, decision ID, canon status, cultural status).
- Never hard-code a character name, chapter name, location ID or lore fact in C++. Use the data asset.
- Never invent content to fill a gap. Use `PENDING_CONTENT_<domain>_<n>`, register it in the content audit request list, and surface it in the debug overlay.
- No named uli motif reproduction (OAD-06); no attributing invented mythology to real Igbo tradition in any string, tooltip or codex entry.

## 6. Contracts between modules

- Cross-module types live in `TDDCore`. Do not duplicate a struct "locally to avoid the dependency".
- Events carry IDs and values, never raw actor pointers.
- Adding a public method to an interface is a contract change: ADR + test + one commit.

## 7. Tests

- New logic ships with a test in the same commit. Bug fixes ship with a regression test that would have failed before.
- Test names follow `TDD-<Tier>.<Area>.<Behaviour>`, and the test name appears in the phase report.
- Tests must not depend on a specific map's content unless they own it; use dedicated `L_TDD_Test_*` maps.

## 8. Comments and documentation

- Comment **why**, not what. Document timing constants with their source ("0.15 s parry window — tuned with CD 2026-11-20, see TUNE-004").
- Any non-obvious tuning value must be data-driven, not a literal in code.
- Public headers carry a one-paragraph purpose comment naming the owning agent.

## 9. Commit hygiene

```
TDD-<area>: <imperative summary, ≤ 72 chars>

Status: <claim vocabulary>
Tests: <names or "none (no build in agent workspace)">
Refs: ADR-XXXX, CONTENT-REQ-00X, issue #N
```

One logical change per commit. Never commit `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, or generated test artefacts. Never commit a large binary without LFS.
