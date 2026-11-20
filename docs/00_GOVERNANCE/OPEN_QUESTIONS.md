# OPEN QUESTIONS — decisions needed

Each item states what it blocks, who decides, and what engineering does in the meantime. Engineering proceeds on the documented **default assumption** and must not build anything that depends on an unresolved answer being a particular way.

| # | Question | Blocks | Decides | Default assumption while open |
|---|---|---|---|---|
| Q-01 | Confirm engine pin **UE 5.8** (ADR-0001)? | Phase 0 start | Technical Director | 5.8; no project file created until confirmed |
| Q-02 | **Platforms:** PC (Windows) only, or console in scope? | Performance targets, input, cert planning | Creative Director | PC only; standard gamepad support still built |
| Q-03 | **Reference and minimum hardware** (MEAD §15.1 proposal) | Meaningful perf gates | Technical Director | RTX 3060 Ti / 16 GB class at 1440p→4K, 60 fps |
| Q-04 | Adopt **GAS** for attributes (ADR-0004)? | Phase 2 architecture; expensive to reverse later | Technical Director | Adopt; attributes behind an adapter |
| Q-05 | **Audio:** MetaSounds only, no middleware (ADR-0009)? | Audio implementation, licence budget | Creative Director / Technical Director | MetaSounds only |
| Q-06 | **Single-player only** (ADR-0011)? | Any networking work ever | Creative Director | Single-player |
| Q-07 | Confirm the **player combat kit** (MEAD §4.2) as the tuning baseline? | Phase 2 acceptance criteria | Creative Director | Kit as written; values tunable |
| Q-08 | **Progression model:** chapter-gated unlocks only / equipment tiers / skill tree? | Phase 6 scope; combat progression hooks | Creative Director | Hooks built; no economy, no currency, no tree; must be a valid config to ship with none |
| Q-09 | **Save policy:** manual saves allowed? save-scumming discouraged, blocked, or free? | Persistence slots, difficulty framing | Creative Director | 3 manual + auto + checkpoint; no restriction |
| Q-10 | Confirm **accessibility baseline** (MEAD §12) as requirement | UI scope, QA matrix | Creative Director | Built as requirement |
| Q-11 | **Difficulty options** — any? what dimensions? | Combat tuning, UI | Creative Director | None designed; all combat values data-driven so options can be added |
| Q-12 | **QTEs / scripted instants** permitted in cinematics? Accessible bypass required? | Cinematic implementation | Creative Director | None used; no QTE system built |
| Q-13 | **Localisation languages**? | Fonts, string tables, VO scope | Creative Director | All strings localisable; only English authored |
| Q-14 | **Boss mechanics** for the seven named bosses — none specified | Phase 4 (pilot boss), Phase 7 | Creative Director, with Technical Director | Framework + one pilot boss using a **placeholder** moveset, labelled `PENDING_CONTENT` |
| Q-15 | **Content of the seven memories** (OAD-32/34 detail) | Memory presentation assets | Creative Director, with Technical Director | Framework + seven `PENDING_CONTENT` anchors |
| Q-16 | **Content of the three ending sequences** (OAD-23) | Ending cinematics | Creative Director | Resolver only; sequence assets not created |
| Q-17 | **Cultural consultant** engaged for `CULTURAL_REFERENCE_GUIDE.md`, OAD-03/04/06? | Final character/lore content; cultural gate sign-off | Creative Director | Gate enforced; nothing relying on real Igbo practice ships without sign-off |
| Q-18 | **Animation content pipeline** — who produces locomotion/combat clips, and when? | Phase 1/3 realism; Motion Matching viability | Creative Director / production | Blend-space fallback (ADR-0005); placeholder mannequin clips for tests |
| Q-19 | **Art content pipeline** — who turns 7 approved concept boards into 3D assets? | Everything visual beyond blockout | Creative Director / production | Blockout geometry only, labelled as blockout |
| Q-20 | **Chapter 8 canon approval** (OAD-48: all five locations `PENDING APPROVAL`) | Chapter 8 narrative content | Creative Director | Design used for scale/mood only |
| Q-21 | **Chapter select / New Game+** — any? | Flow system scope | Creative Director | Chapter flow supports both; not exposed in UI |
| Q-22 | **Telemetry / crash reporting** permitted? | Release tooling | Creative Director | None implemented; no data leaves the machine |

## How engineering handles unanswered questions

1. Build the mechanism, not the content. Frameworks are content-agnostic where canon is unknown.
2. Name every placeholder (`PENDING_CONTENT_<domain>_<n>`) and surface it in the content audit and debug overlay.
3. Never convert an open question into an invented answer in code, dialogue, UI copy or documentation.
4. Re-check this list at every phase gate and update it; an item that stops being relevant is closed with a reason, not deleted.
