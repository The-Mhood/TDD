# ADR-0002 — Baseline engine: Unreal Engine 5.8

- **Status:** ACCEPTED (pending Technical Director confirmation)
- **Date:** 2026-11-16
- **Owner:** Agent 3 (Integration / Technical Quality)
- **Affects:** all agents

## Context

The directive mandates Unreal Engine 5 but does not pin a version. As of 2026-11-16:

- **UE 5.8** shipped 2026-06-17 and is the **last planned major UE5 release**; Epic has reserved the option of
  a 5.9, and targets UE6 Early Access in late 2027.
- 5.8 makes **MegaLights production-ready**, adds a **Lumen Lite** path aimed at holding 60 fps on lower-tier
  hardware, and makes **PCG** and **Substrate** production-ready. It also improves PSO precaching.
- 5.7 and earlier remain available but are superseded and will receive fewer fixes.

Our art direction is unusually demanding of exactly these systems: dense rainforest with mist shafts
(Chapter 1), many small dynamic ember/crack lights (Chapter 7), volatile storm lighting (Chapter 5), and
volumetric wet environments (Chapter 4). Our content is foliage-heavy, which has historically been UE5's
greatest performance weakness.

## Decision

Pin the project to **Unreal Engine 5.8**.

- `.uproject` declares `"EngineAssociation": "5.8"`.
- All agents record the exact engine build in evidence metadata.
- Engine upgrades are gated by an ADR. **No incidental upgrades.**
- Deprecated-API usage is treated as a review defect, so a future 5.9/UE6 move is a rebuild, not a rewrite.

## Consequences

**Positive**
- A terminal minor release is the most stable target available for a multi-year production. Churn risk drops.
- Production-ready MegaLights and Lumen Lite give us a credible 60 fps scaling tier from day one rather than
  a retrofit.
- Production-ready PCG reduces hand-placed asset cost in eight chapters.

**Negative / risks**
- Any 5.9 fixes will arrive on a branch we are not tracking. Mitigation: A3 watches release notes; a 5.9
  upgrade is considered only at a stage boundary with a full regression run.
- UE6 (late 2027) will land inside this production. Mitigation: plugin/API hygiene and no engine-source
  modifications; migration assessed only during Stage 9 polish, never mid-feature.
- Some 5.8 features (Nanite Foliage, Mesh Terrain) are **experimental**. Policy: not a dependency of any
  milestone; may be evaluated in a labelled spike and recorded as EXPERIMENTAL, never assumed present.

## Alternatives rejected

| Alternative | Why rejected |
|---|---|
| UE 5.7 | Superseded; no advantage over 5.8, loses Lumen Lite and production MegaLights |
| UE 5.4 / 5.5 | Materially worse CPU/frame-time behaviour in foliage-heavy scenes; a dead end for an 8-chapter game |
| Wait for UE6 Early Access | 2027 + EA instability is unacceptable for a production that must ship a playable game first |
| Engine source fork | Unjustifiable maintenance cost for a three-agent team |
