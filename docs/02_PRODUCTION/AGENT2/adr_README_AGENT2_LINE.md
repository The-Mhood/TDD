# Architecture Decision Records — THE DISOBEDIENT DAUGHTER

Format: [ID] · Title · Status (PROPOSED / ACCEPTED / SUPERSEDED / REJECTED) · Context · Decision · Consequences.

Rules:
- One decision per record. A record is immutable once ACCEPTED; later changes are new records that supersede it.
- Every ADR names its **owner** and the **agents affected**.
- No agent may add a plugin, change the engine version, change an ID scheme, or change the save format
  without an ADR here.
- An ADR is not canon approval. It records engineering decisions only.

| ADR | Title | Status |
|---|---|---|
| 0001 | Unreal Automation framework as the only in-engine test harness | ACCEPTED |
| 0002 | Baseline engine: Unreal Engine 5.8 | ACCEPTED (Technical Director confirmation pending) |
| 0003 | GAS for combat abilities only; movement on CMC | ACCEPTED |
| 0004 | Binary asset storage policy (Git holds text only) | PROPOSED — blocked on CD/infra |
| 0005 | Engine-side verification requirement; sandbox verification limits | ACCEPTED |
| 0006 | Adopt the Drive registers' canonical ID scheme; maintain a validated mirror | ACCEPTED |
| 0007 | Declarative boss phase graphs instead of bespoke boss code | ACCEPTED |
| 0008 | Memories as staged fragment state machines, audio-first | ACCEPTED |
