# REQUEST — AGENT 1 TRAVERSAL CONTRACT

**From:** Agent 2 (world structure / level architecture)
**To:** Agent 1 (player controller / movement / traversal)
**Date:** 2026-11-16
**Status:** REQUEST — nothing here is a decision. No identifier in this document may be frozen, promoted to canon, or implemented until Agent 1 replies and the TD approves.

---

## 1. Why this request exists

I own world structure, level architecture, streaming, environment interaction and exploration/traversal areas. Agent 1 owns the player controller, movement and the traversal *mechanics*. Climbing is explicitly joint.

The boundary is not negotiable: I must not define traversal mechanics, and Agent 1 must not define scene data formats. But they meet, and if we both invent the meeting point separately, we produce two incompatible schemas. The TD has explicitly prohibited me from freezing or inventing the traversal enum, and required me to request the contract, state the minimum fields scene data needs, use provisional identifiers only, and await cross-agent + TD approval.

So: this document states **what scene data needs from traversal**, using **provisional names** that carry no authority.

---

## 2. What I need from Agent 1

For each of the following, I need Agent 1's definition. Where I have a provisional guess, it is marked `PROVISIONAL` and is not a proposal — it exists only so we can see whether the shape is adequate.

### 2.1 The traversal capability enum

An ordered set of movement capabilities the player can perform, such that a level designer can declare "this route requires capability X" and the game can answer "can the player do X here yet?".

Minimum questions the enum must answer:

| # | Question | Why world structure needs it |
|---|---|---|
| Q1 | Can the player climb a surface of a given type? | Determines whether a route is a shortcut, a one-way drop, or a wall |
| Q2 | Can the player traverse while carrying/holding something? | Some routes must close once a carry is active |
| Q3 | Are route requirements **cumulative** (A then B) or **independent** (A or B)? | I cannot validate a route without knowing this |
| Q4 | Can a requirement be **revoked**? | Backtracking and gating depend on it |
| Q5 | Is there a concept of "traversal context" (e.g. in-water, on-rope) that changes the available set? | Exploration scenes include water and ravine content |

`PROVISIONAL` illustration of the *shape* only — do not implement, do not cite as agreed:

```
capability:      surface climb (low / mid / full)
requirement:     a single capability, or an AND/OR group of capabilities
route:           { entry_point, exit_point, requirement, one_way: bool }
```

### 2.2 Whether requirements are data or code

If route requirements live in level data, I can validate them offline and report unreachable content before anyone opens the editor. If they live in code, I need an interface to query them.

**This is the single most consequential answer for me.** It decides whether "is every exploration reward reachable?" is a build-time check or a playtest question.

### 2.3 Failure semantics

When the player attempts a route they cannot complete, what happens? Blocked silently, animation refusal, contextual hint? This affects whether a blocked route can be used as a legitimate signpost without a UI prompt, which in turn affects whether I need hint volumes in scene data.

---

## 3. Minimum fields scene data needs — provisional

These are the fields world data would have to carry to *express* traversal requirements, whatever the enum turns out to be. They are listed so Agent 1 can design an enum that these fields can hold. **None of these names is agreed.**

| Field | Type | Purpose | Provisional? |
|---|---|---|---|
| `route_id` | string | Stable identifier for a traversal route | yes |
| `from_anchor` | string | Where the route starts | yes |
| `to_anchor` | string | Where it ends | yes |
| `requirement` | cap-expr | What the player must be able to do | yes |
| `one_way` | bool | Whether it can be retraced | yes |
| `failure_mode` | enum | What happens when unmet | yes |
| `carry_compatible` | bool | Whether it works while carrying | yes |

Provisional anchor/route identifiers for Chapter 1's traversal content, marked so they cannot be mistaken for canon:

```
PROVISIONAL-CH01-TRV-001-ROUTE-A   The Threshold Path    (from register CH01-TRV-001)
PROVISIONAL-CH01-TRV-002-ROUTE-A   The Root Way          (from register CH01-TRV-002)
PROVISIONAL-CH01-TRV-003-ROUTE-A   The Stream Crossing   (from register CH01-TRV-003)
PROVISIONAL-CH01-TRV-004-ROUTE-A   The Ravine and Liana Bridge (from register CH01-TRV-004)
```

The `PROVISIONAL-` prefix is deliberate. It sorts away from real IDs, it is obvious in a diff, and it cannot be mistaken for a register value. `CH01-TRV-001..005` are real register location ids; the `-ROUTE-A` suffix and the prefix are **mine, not the register's**.

---

## 4. What I am NOT asking for, and what I will not do

I am **not** asking Agent 1 to adopt any of the names above. I am **not** designing climbing, mantling, swimming or rope mechanics.

I will **not**:

- add a traversal enum to canon or to any register
- create a second player controller or duplicate movement logic
- implement a route requirement system before the contract is agreed
- claim any traversal behaviour is functional — there is no Unreal project, so nothing here is executable

Everything in this document is `SPEC / PROVISIONAL`. Nothing has been run.

---

## 5. What I can offer Agent 1

- **Route validation, offline.** Once I know whether requirements are data, I can check that every exploration reward in a chapter is reachable from the chapter's entry point, and report unreachable content as a build failure rather than a playtest finding.
- **Scope data.** Chapter 1 contains 5 traversal areas and 2 exploration scenes; the full game has 135 scenes across 8 chapters. The traversal contract should not assume a small number of authored routes.
- **Blockout geometry** for spatial/navigation/streaming/sightline tests under CD-5 restrictions, clearly labelled, removable, establishing no story fact.

---

## 6. What I need back

1. The capability enum, or a statement that it is not yet defined.
2. Whether route requirements are data or code.
3. Failure semantics.
4. Whether any of the seven minimum fields in §3 is wrong or insufficient.
5. Anything in my provisional identifiers that would collide with Agent 1's scheme.

Until 1–5 are answered and the TD approves, I will use only `PROVISIONAL-` identifiers and I will not implement route requirements.

---

## 7. Change log

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-11-16 | First issue. Request only; no contract asserted, no identifier frozen. |
