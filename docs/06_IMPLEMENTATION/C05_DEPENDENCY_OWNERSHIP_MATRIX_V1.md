# C-05 implementation dependency and ownership matrix — v1

**Document ID:** `TDD-IMPL-C05-DEPS-001`
**Date:** 2026-11-18 UTC
**Author:** Agent 1 (implementation lead), for TD adjudication
**Status:** `DESIGN_ONLY` for every item below. **No decision is invented here.** Each row states what decision is missing, who must make it, and what it blocks.

---

## 1. Rule this document follows

The directive requires *explicit, version-pinned decisions; do not silently invent or assume unresolved contract behaviour.* This matrix therefore records, for each outstanding dependency: the ID as the contract already numbers it (`A1-C05-S4.3.11` §14.1/§14.2), the owner as the repository already records it, the **exact decision required**, the **format** a version-pinned answer must take, and the engineering work it unblocks. Where the repository records a status, that status is quoted; where nothing is recorded, this matrix says so rather than supplying an answer.

## 2. Contract-level dependencies (B-1 … B-4)

| ID | Dependency | Owner | Status as recorded | The exact decision required | Version-pinned answer must state | Blocks |
|---|---|---|---|---|---|---|
| **B-1** | **TD-06** — clock ownership and the shared axis | **TD** | **OPEN** — TD (`S4.3.11` §14.1) | Who owns the gameplay clock that every timestamped C-05 value is expressed against, and what the shared axis is. One sentence of authority, not a design | Owner (Agent 1 / Agent 2 / a named subsystem), the axis (frame counter, seconds of gameplay time, or state revision), and the contract revision that will carry it | **Any code that stamps or ages timing**, the fixture clock, and `T-C05-01`; **`T-C05-11` is explicitly deferred until this resolves** |
| **B-2** | **TD-09** — parry authority and the MEAD-C/MEAD-A erratum | **TD** | **OPEN** — TD (§14.1) | Which layer decides a parry outcome (MEAD-C or MEAD-A), and the erratum that records it | The authoritative layer, the erratum ID, and the revision it lands in | The arbitration path; any parry-facing case; C-03/C-04 interface shape |
| **B-4** | **TD-12** — canonical MEAD and the contract-layer owner | **TD** | **OPEN** — TD (§14.1) | Which MEAD is canonical, and who owns the contract layer (the module and the agent) | MEAD document + version, owning agent, owning module | **Freezing the value types, the resynchronisation type and the read interface** — i.e. the C-05 public surface in `TDDCore` |
| **B-3** | No engine, compiler or project in the workspace | **Project Owner / Phase 0** | **PARTIALLY ADDRESSED at this commit** — project now exists (§`UNREAL_PROJECT_FOUNDATION_V1.md`); **engine and compiler still absent** | Provide a UE 5.8 build machine | Machine spec + engine build + date | **Executing any of the 67 cases.** Nothing in this matrix unblocks execution; only §5 of the foundation document does |

## 3. Implementation-visible dependencies (B-9 … B-15)

| ID | Dependency | Owner | Status as recorded | The exact decision required | Blocks |
|---|---|---|---|---|---|
| **B-9** | Agent 2's re-review of the **exact** S4.3.11 blob | **Agent 2** | **OPEN** — requested (§14.2) | Verify or contest the loop's two divergences from Agent 2's recommendation (`D-1`, `D-3`), plus the instrument changes at `06a4a8b` and `6ddc8ed` | Any claim that C-05 is independently verified; nothing in the code path |
| **B-10** | Agent 3's reassessment of S2 and S3 | **Agent 3** | **OPEN** — requested (§14.2) | Publish the missing reviews on `arena/c64fc525-tdd`, or state they will not be produced | Traceability of S2/S3 findings; **not** a code blocker |
| **B-11** | `C05-6.3`'s three carriers restated only in `A1-C05-S1` §6.3; clause proposed, coupled to `C-04-4` | **C-04 owner**, then **TD** | **`BLOCKED BY DEPENDENCY`** (§14.2) | Land or reject `C-04-4` (the `Status.Dead` grant), and say whether `C05-6.3` is frozen as written | `TN-C-07` (the `Dead > Cinematic > Staggered` evaluation) and therefore **tranche case work on status priority**; the carrier enum is *not* implemented until this resolves |
| **B-12** | Cross-agent routing of the resynchronisation signal | **TD** (via B-4) | **OPEN, not proposed** (§14.2) | Whether routing is in scope at all; the type is normatively declared but delivery is consumer-local | Any transport code; the resync type's placement in `TDDCore` is gated on B-4, not on this |
| **B-14** | Float comparison tolerance for `INV-2` assertions | **Agent 1** (test-fixture decision) | **OPEN** — implementation-time, non-blocking (§14.2) | **Decidable now by the implementer**, recorded as a fixture constant — this matrix proposes `1e-4` relative for derived time values and `0.0` exact for revision integers, and **flags the proposal as a proposal** | Only `T-C05-54`/`T-C05-55`, which are outside tranche 1 |
| **B-15** | Agent 3's S3 review is not in the repository | **Agent 3** | **OPEN** (§14.2) | Publish the S3 review wording; if it differs materially, `TN-C-11` and `§9.2` are re-opened | Nothing in tranche 1 **unless** the wording contradicts a tranche-1 obligation |

## 4. What this matrix deliberately does not do

- **It does not answer B-1, B-2, B-4 or B-11.** These are the four questions the directive says must not be silently assumed; guessing any of them would put invented contract behaviour into code, which is the one outcome the governance record treats as worse than a blocker.
- **It does not re-open `F-1b`**, does not touch `D-c`/`D-d`/`C`, and does not modify the contract. C-05 remains `DESIGN_ONLY`, unsigned, unfrozen; 43 obligations, 18 suites and 67 case identities are unchanged.
- **It does not claim any of these are closed.** B-3 is *partially* addressed only in the sense that the project now exists; execution remains impossible without an engine (foundation document §5).

## 5. Owners, restated as the single source for this cycle

| Agent | Owns, in this cycle | Must not do |
|---|---|---|
| **Agent 1** | Unreal project foundation (done, unverified), tranche-1 implementation, fixtures, traceability, the `Tools/engine` verifiers | Claim a build; invent a contract decision; modify S4.3.10 or the verified evidence |
| **Agent 2** | Independent technical verification of the foundation and of any build; contract validation (B-9); test evidence | Write implementation; adjudicate contract questions itself |
| **Agent 3** | Design/governance review (B-10, B-15), traceability verification of the module graph against MEAD §3.2 | Write implementation; alter the contract |
| **TD** | B-1 (TD-06), B-2 (TD-09), B-4 (TD-12); adjudication of B-9/B-11 disagreements; ratification of the engine pin (ADR-0001); the branch-ownership question raised in the foundation document §7 | — |
