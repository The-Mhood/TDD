# ADR-0008 — Canon status and cultural status gating in data assets

- **Status:** Proposed
- **Date:** 2026-11-16
- **Owning agent:** 3 (validation), Creative Director (policy)

## Context
The Art Bible distinguishes approved designs, exploratory designs, rejected designs, and design approval from narrative-canon approval (OAD-48/OAD-53). It also requires that invented mythology never be presented as authentic Igbo tradition, and its cultural reference guide still needs consultant review. Nothing in an ordinary UE project prevents a `PROPOSED` environment from shipping, or an invented detail from being written as fact.

## Decision
Every content asset carries `FTDDCanonReference { ArtBibleAssetId, DecisionId, ETDDCanonStatus, ETDDCulturalStatus, CulturalSignoffId }`. Editor validators gate the cook:
- Shipping cook fails if a narrative-critical asset (chapter, memory, boss, character, weapon, location) is not `Approved`.
- Shipping cook fails if any `Inspired_RequiresConsultant` or `Documented_Real_RequiresSignoff` asset lacks a valid sign-off record.
- `Rejected`/`Exploratory` assets referenced by a shipping map fail the cook.
- Any asset without a canon reference fails the cook.

## Consequences
- **Positive:** canon and cultural constraints become mechanical, not remembered.
- **Positive:** the content audit report can state, per chapter, exactly what is unapproved.
- **Negative:** authoring overhead on every asset; a valid-but-incomplete asset blocks a cook (intended).
- **Negative:** the gate can only enforce declared status, not judgement — humans still decide what "approved" means.

## Verification
`TDD-Unit.Canon.ValidatorRules`, plus a deliberately mis-tagged test asset that must fail the cook, recorded as evidence.
