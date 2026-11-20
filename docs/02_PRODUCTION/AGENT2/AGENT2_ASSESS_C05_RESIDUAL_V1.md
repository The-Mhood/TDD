# Assessment — the C-05 residual families (`R-1` … `R-7`)

**Assessment ID** `TDD-A2-ASSESS-C05-RESIDUAL-001` v1.0
**Responds to** `A1-C05-REQ-A2-001` v1.0 (Agent 1)
**Reviewer** Agent 2
**Assessed against** `7662926c4c3b7293daedcc393c0ec4d015cdd883` — document `857778e1…` (2441 lines), validator `353a2bff…`, suite `7ab55805…`
**Work performed from** `git archive 7662926` extracted to `/tmp/a310`; no branch tip, no working-copy file substituted
**Nature** Assessment only. **No validator, suite, contract, register or implementation file was modified.**

---

## 0. Bottom line

**All 14 probes reproduce exactly as Agent 1 states.** I found no discrepancy in the reported table — that
is worth saying plainly, because the point of publishing the probes was to make a disagreement about the
verdict rather than about what was probed, and there is none.

Three findings change the shape of the recommendation:

1. **The families are four distinct defects with three different root sites, not one.** Agent 1's hypothesis
   that `R-4`/`R-5` share a root in "a comma-delimited apposition read as a clause boundary" is **not
   correct**: `R-5b` contains **no commas at all** and still fails. The comma is not the mechanism; the
   missing copula is. Correct grouping is `R-3b` + `R-5` (copula), with `R-4` standing alone (foil marking).
2. **The obvious `R-4` fix is unsafe, but not for the reason it first appears.** Adding `not`/`never` to the
   foil-marker set (`C`) passes every existing check *on its own* — 27/27, 147/147, 26/26 — and still has to
   be refused: it re-opens a genuine hazard, `"Not only does Agent 1 own the audio cues."` goes FAIL → PASS,
   and it collides catastrophically with the copula fix, taking the document to **26/27** and breaking
   **eight of the 26 required controls**. A one-line fix cannot close `R-4`; it needs a structural change
   that recognises appositive position. **Defer it.**
3. **Seven of the nine close cleanly, together, with zero collateral damage** — `R-1`, `R-1b`, `R-1c`,
   `R-3b`, `R-5`, `R-5b`, `R-5c`; 27/27, 147/147, 26/26 controls, 5/14 → **12/14** probes correct. That is
   the cycle I recommend authorising **now**.

**Recommended next step:** authorise **one cycle for `R-1` + `R-3b` + `R-5`** (the `A+D` pair: two closed-set
widenings at two distinct sites, verified additive and safe). **Defer `R-4`/`R-4b`** to a separate item — they
are a foil-marking defect needing a structural fix, and the one-line form is measurably worse than doing
nothing. `R-4`/`R-4b` must stay **unchanged** in the `A+D` cycle; if they move, the cycle has over-reached.

---

## 1. Reproduction — all 14 probes, independently

Injected as an obligation-shaped line immediately before `## 9. Shared read-surface and arbitration
obligations`, reading the `DV-22` verdict of the pinned validator. **All 14 match Agent 1's table exactly.**

| # | Family | Verdict | Required | Direction | Agrees |
|---|---|---|---|---|---|
| `R-1` | appositive `never` | FAIL | PASS | fail-closed | ✅ |
| `R-1b` | appositive `never any` | FAIL | PASS | fail-closed | ✅ |
| `R-1c` | `never`, no comma | FAIL | PASS | fail-closed | ✅ |
| `R-2` | auxiliary / modal | FAIL | FAIL | **correct** | ✅ |
| `R-2b` | modal `must` | FAIL | FAIL | **correct** | ✅ |
| `R-3` | perfect aspect, active | FAIL | FAIL | **correct** | ✅ |
| `R-3b` | perfect aspect, passive | PASS | FAIL | **fail-open** | ✅ |
| `R-4` | appositive `not` foil | PASS | FAIL | **fail-open** | ✅ |
| `R-4b` | appositive `never` foil | PASS | FAIL | **fail-open** | ✅ |
| `R-5` | appositive attribution (`L-3`) | PASS | FAIL | **fail-open** | ✅ |
| `R-5b` | attribution, no commas | PASS | FAIL | **fail-open** | ✅ |
| `R-5c` | attribution, `provided` | PASS | FAIL | **fail-open** | ✅ |
| `R-6` | contrastive apposition | FAIL | FAIL | **correct** | ✅ |
| `R-7` | number-word possessor | FAIL | FAIL | **correct** | ✅ |

**Six fail-open** (`R-3b`, `R-4`, `R-4b`, `R-5`, `R-5b`, `R-5c`), **three fail-closed** (`R-1`, `R-1b`,
`R-1c`), **five correct** (`R-2`, `R-2b`, `R-3`, `R-6`, `R-7`). Counts confirmed.

---

## 2. Mechanism — instrumented, not inferred

I read `negated_mention`, `attributed_to_agent_1`, `segment_bounds`, every `NEG_BEFORE`/`NEG_AFTER`
span, `is_foil` per reference, and `FORWARD_OWNER` pattern indices for each probe.

### 2.1 The five "correct" probes share one path

`R-2`, `R-2b`, `R-3`, `R-6`, `R-7` all succeed because **the subject precedes the mention**, so
attribution comes from the nearest `AGENT_REF` before it and `FORWARD_OWNER` is never consulted:

| Probe | Governing reference | Falls to |
|---|---|---|
| `Agent 1 may own the audio cues.` | `Agent 1` | subject-before path |
| `Agent 1 must own the audio cues.` | `Agent 1` | subject-before path |
| `Agent 1 has owned the audio cues.` | `Agent 1` | subject-before path |
| `Agent 1, unlike Agent 2, owns the audio cues.` | `Agent 1` (`Agent 2` is a foil) | subject-before path |
| `The first agent owns the audio cues.` | `The first agent` | subject-before path |

**This is the important structural fact:** the modal and perfect families are *not* defective. Whatever is
wrong in `R-3b` and `R-4` lives in the **reversed word order** branch, not in the auxiliary or aspect.

### 2.2 `R-1` family — the object-negation tests the literal word `not`

`NEG_BEFORE[10]` (validator line 573):

```python
re.compile(r'\bnot\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),
```

`never` is not in the alternation, so no `NEG_BEFORE` entry spans the mention, `negated_mention=False`,
and the subject-before attribution (`Agent 1`) makes it an offence:

| Probe | `NEG_BEFORE` spanning | `negated` | `attributed` | Offence |
|---|---|---|---|---|
| `R-1` | **NONE** | False | True | True |
| `R-1b` | **NONE** | False | True | True |
| `R-1c` | **NONE** | False | True | True |

**Root: a closed negator set. One site.** Note `R-1c` has no comma and fails identically, which already
shows the comma plays no part in this family — it is the negator word, not the punctuation.

### 2.3 `R-3b` — `FORWARD_OWNER[0]` hard-codes a simple copula

`FORWARD_OWNER[0]` (lines 655–658) requires `is|are|was|were` immediately before the participle:

```python
re.compile(r'\baudio\b[^.;|]{0,40}?\b(?:is|are|was|were)\s+(?:owned|…|chosen)\s+by\s+<Agent 1>\b', re.I)
```

Measured across auxiliaries, same statement:

| Form | `attributed_to_agent_1` | `FORWARD_OWNER` hit |
|---|---|---|
| `is owned by` | True | `[0]` |
| `was owned by` | True | `[0]` |
| `has been owned by` | **False** | **NONE** |
| `have been owned by` | **False** | **NONE** |
| `had been owned by` | **False** | **NONE** |
| `will be owned by` | **False** | **NONE** |

**Root: a closed copula set. One site.** `R-3b` is not an "aspect" defect — it is that the passive
auxiliary chain is not matched. The perfect *active* form (`R-3`) works because it takes the
subject-before path.

### 2.4 `R-5` family — a bare participle carries no copula

`R-5`/`R-5b`/`R-5c` are the same statement with the copula absent. `FORWARD_OWNER[0]` insists on
`is|are|was|were`, so with no copula nothing spans the mention:

| Probe | Commas | `FORWARD_OWNER` spanning | `attributed` |
|---|---|---|---|
| `R-5` | 2 | **NONE** | False |
| `R-5b` | **0** | **NONE** | False |
| `R-5c` | 2 | **NONE** | False |
| control: `is supplied by` | 0 | `[0]` | True |

**`R-5b` has no commas and fails identically to `R-5`.** A minimum contrast pair — same sentence, added
`is` — flips False → True:

```
The audio cue, supplied by Agent 1, drives the mixer.     attributed=False
The audio cue, is supplied by Agent 1, drives the mixer.  attributed=True   <-- only 'is' added
```

**Root: the same closed copula set as `R-3b`, in its zero-copula form. One site, shared with `R-3b`.**

> **Correction to Agent 1's hypothesis.** The request offers, explicitly as unverified, that `R-4`/`R-5`
> share a root in "a comma-delimited apposition read as a clause boundary." **That is not so.** `R-5b`
> has no commas, and the `R-5` family's mechanism is the missing copula, not punctuation. `R-5` belongs
> with `R-3b` (copula/participle), not with `R-4` (foil marking). This matters because it changes the
> grouping: the natural pair is **`R-3b` + `R-5`**, and `R-4` stands alone.

### 2.5 `R-4` family — `not`/`never` are not foil markers

`is_foil` returns True when the clause a reference sits in opens with a contrastive marker, and
`_FOIL_ANY` (line 487) is:

```python
re.compile(r'\b(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\b', re.I)
```

`not` and `never` are absent. So in `Agent 1, not Agent 2, owns …` the appositive `Agent 2` is **not**
recognised as a foil, becomes the nearest governing reference, and `agent_of(...) == '2'` returns False:

| Probe | `AGENT_REF` before mention | Foil filter | Governing | `attributed` |
|---|---|---|---|---|
| `R-4` | `Agent 1`, `Agent 2` | both kept | **`Agent 2`** | False |
| `R-4b` | `Agent 1`, `Agent 2` | both kept | **`Agent 2`** | False |
| `R-6` (works) | `Agent 1`, `Agent 2` | `Agent 2` dropped | `Agent 1` | True |

**Root: a closed foil-marker set. One site — but see §4.2: the obvious fix is unsafe.**

### 2.6 Root summary — four defects, three sites

| Defect | Probes | Root site | Closed set |
|---|---|---|---|
| **D-a** object-negation negator set | `R-1`, `R-1b`, `R-1c` | `NEG_BEFORE[10]`, line 573 | `{not}` |
| **D-b** passive copula / participle | `R-3b`, `R-5`, `R-5b`, `R-5c` | `FORWARD_OWNER[0]`, lines 655–658 | `{is,are,was,were}` |
| **D-c** foil marker set | `R-4`, `R-4b` | `_FOIL_ANY`, line 487 | `{unlike, as opposed to, rather than, but not}` |
| **D-d** predicate verb list | *(not in the 14)* | `FORWARD_OWNER[0]` participle list | `{owned, claimed, …}` |

`D-b` and `D-d` share a site but are separable: `D-b` is the copula, `D-d` is the participle. `D-d` is
**not in Agent 1's 14 probes** — I record it only because it is at the same line and a correction touching
that line should not silently widen it (§5.3).

**So: Agent 1's "several, not one" instinct is right, but the grouping is not the one proposed.** It is
**3 families over 3 sites**, and `R-3b`/`R-5` are one family, not two.

---

## 3. Reachability in the contract's own voice

This is the test I applied to `CONDITION-2` and `F-2`, and it is decisive for severity.

**`TN-C-15` gives audio cue selection to Agent 2 alone.** An assertion that Agent 1 owns the audio cue
would therefore *contradict the contract*, not merely be unidiomatic in it. The contract's own voice for
audio ownership is:

- `TN-C-15`: "Audio cue selection is a C-05 consumer responsibility of **Agent 2 alone**"
- `TN-C-11`: cue selection keyed on `Phase`, `WindowKey`, `AttackTag`
- `D-4`: "Row 5 loses 'audio cues'; row 6 keeps cue selection"

I scanned all **165 live (non-exempt) audio mentions** in the document: **21** are attributed to Agent 1,
and **every one of the 21 is a quoted probe example inside meta-discussion** (§2.x, §13.3.x) — not a
contract-voice assertion. `DV-22` reports **0 offenders** on the live text.

| Family | Live occurrences in the document | Reachable in the contract's voice? |
|---|---|---|
| `R-1` (`never` object negation) | 2 lines, **both meta-discussion** | **No** — but see below |
| `R-3b`, `R-5` | 0 real instances | **No** |
| `R-4`, `R-4b` | 0 | **No** |
| `R-2`, `R-3`, `R-6`, `R-7` | n/a | correct already |

**Reachability verdict.** None of the six fail-open shapes appears as a live ownership assertion, and
none *can* while `TN-C-15` stands, because the shape would be contract-violating content. **All six are
non-blocking on reachability.** They matter as **escape-resistance**, not as live defects: `DV-22` is the
guard that would catch an author writing one, and a guard with a hole is weaker than its specification.

**`R-1` is the one with a real reachability path**, and it is the *opposite* direction: `never` is a
**legitimate** English object negation that the check rejects. If an author writes
`Agent 1 owns the camera, never the audio cues` — a true and contract-consistent statement — the check
fails the document. That is reachable in the contract's voice, because denying Agent 1 owns audio is
exactly what `TN-C-15` says.

---

## 4. Defect in the instrument or in the contract?

**All four defects are in the instrument. None is a contract defect.** I state this on the same basis as
`F-1`/`F-1b`:

- No obligation row, case specification, or normative sentence is implicated by any probe.
- `R-1` and `R-3b`/`R-5` are **under-matching** in the predicate: the grammar is correct English and the
  contract's ownership model is unambiguous; the regex simply does not read the form.
- `R-4` is a **foil-recognition** gap, not an ownership ambiguity: `Agent 1, not Agent 2, owns …` has one
  possible reading, and the contract already says who owns audio.
- The 43 obligation rows and 17 case specifications are untouched by every candidate in §5 (verified:
  byte-identical between `72d218a8` and `857778e1`, and no candidate changes the document at all).

**No contract-normative change is proposed, and none is needed.**

---

## 5. What would regress — measured, not guessed

I applied each candidate to a scratch copy of the validator and ran, every time: the **27-check document
validation**, the **full 147-case suite**, a **26-control required set** (4 object negations, 5 positive
ownership, 4 `CONDITION-1`, 3 `F-1`, 3 `CONDITION-2`, 7 `_joinable`), and the 4 residual probes.

**Baseline `7662926`: 27/27, 147/147, all 26 required controls correct.** Any movement is a regression.

### 5.1 The corrected matrix — every variant measured on four axes

Each variant is applied to a scratch copy of `dv_c05.py` by exact string replacement (the anchor is
asserted to be present first — a silent no-op replacement produced one wrong intermediate reading
during this assessment, see §5.4). Columns are: the 27-check document validation, the 147-case
regression suite, **how many of the 14 probes reach the correct verdict** (baseline is 5 — the five
that already behave correctly), and the **26-control required set**.

| Variant | Change | Document | Suite | Probes correct | Required controls |
|---|---|---|---|---|---|
| — | baseline `7662926` | 27/27 | 147/147 | **5/14** | 26/26 |
| `A` | object-negation negator set takes `not\|never` (line 573) | 27/27 | 147/147 | **8/14** | 26/26 |
| `D` | copula made optional in `FORWARD_OWNER[0]` (lines 655–658) | 27/27 | 147/147 | **9/14** | 26/26 |
| **`A+D`** | both | **27/27** | **147/147** | **12/14** | **26/26** |
| `C` | `not\|never` added to `_FOIL_ANY` (line 487) | 27/27 | 147/147 | 7/14 | 26/26 |
| `C+D` | both | **26/27** | 147/147 | 11/14 | **18/26** |

**`A+D` is the recommendation and it is clean on every axis I can measure:** it closes exactly
`R-1`, `R-1b`, `R-1c` (from `A`) and `R-3b`, `R-5`, `R-5b`, `R-5c` (from `D`) — seven of the nine — and
moves nothing else. `R-4`/`R-4b` stay exactly as they are today (still missed), the document stays
27/27, the suite stays 147/147, and all 26 controls keep their required verdicts.

The two changes are additive and do not interact: `A` alone closes 3, `D` alone closes 4, together 7.
That is the whole case for one cycle rather than two.

### 5.2 Why `C` is refused — and why my first reading of it was wrong

`C` is the tempting one-liner for `R-4`: add `not` and `never` to the foil set so that in
`Agent 1, not Agent 2, owns the audio cues` the second reference is recognised as a foil rather than
as the governing owner. On its face it closes `R-4` and `R-4b` and, measured alone, it breaks **no
existing check**: 27/27, 147/147, 26/26, and 7/14 probes.

**It is still wrong, and the probe count is what shows it.** `C` closes two probes and re-opens one
that was already correct, for a net gain of two — and the one it re-opens is a genuine hazard:

```
"Not only does Agent 1 own the audio cues."
  baseline: FAIL  (a positive ownership claim: correctly flagged)
  C:        PASS  <-- false negative
```

Making `not` a general foil marker means any negation-before-agent shape can disarm attribution, and
`not only` is the commonest such shape in English. That is a new fail-open channel bought to close a
fail-open channel.

Worse, `C` **collides with `D`**, and this is the interaction the one-line view hides:

```
"Audio is not owned by Agent 1"        (TD-28's control, required PASS)
  baseline : is_foil('Agent 1') = False -> negated=True,  attributed=False -> PASS
  D alone  : is_foil('Agent 1') = False -> negated=True,  attributed=True  -> still PASS (saved by 'negated')
  C+D      : is_foil('Agent 1') = True  -> negated=False, attributed=True  -> FAIL  <-- false alarm
```

`C+D` therefore **drops the clean document to 26/27 and breaks eight of the 26 required controls** —
the four object negations and all four `CONDITION-1` forms, which are exactly the sentences whose job
is to say Agent 1 does *not* own audio. `C` alone escapes this only because `D`'s copula widening is
what lets the passive frame match without `is`; the collision is latent, not absent.

**A correct `R-4` fix must recognise `not`/`never` as a foil marker only in appositive position
(between two agent references) and must not let it govern the preceding clause.** I did not design or
verify that, because designing the fix is Agent 1's work. What I can state with confidence is that
neither the one-line widening (`C`) nor `C` combined with anything is a safe route, and that `R-4`
should be deferred rather than bundled.

### 5.3 A caveat that `D` carries, stated so it is not mistaken for a clean win

`D` makes the copula optional, so `audio … owned by Agent 1` now matches with no copula present. That
widens attribution on passive denials too:

```
"Audio is not owned by Agent 1"
  baseline: negated=True,  attributed=False
  D:        negated=True,  attributed=True
```

The verdict stays correct (PASS) because `negated` is checked first, and every one of the 26 controls
plus all 147 cases confirms it. But the **predicate's intermediate state becomes less precise**: an
`attributed=True` on a denial is now only one ordering decision away from a false alarm — which is
precisely the ordering that `C` breaks. This is a reason to fix `R-4` deliberately and separately, not
a reason to withhold `D`.

### 5.4 What I would refuse to widen

- **`D-d` (the participle list).** `assigned`, `managed`, `controlled`, `authored`, `approved`,
  `commissioned`, `mixed`, `routed` also return `attributed=False` with a copula present. Adding them is a
  **content taxonomy expansion, not a grammar fix** — out of scope for any cycle here. I record it so it is
  a deliberate exclusion, not an oversight.
- **`never` as a general negator.** Only the object-negation site in this cycle; not into
  `NEG_AFTER`, not into `_FOIL_ANY`, and not as a global `not|never` substitution — §5.2 measures
  what that costs.
- **Any change to the positive-attribution predicates that would weaken them.** Five positive controls
  must keep failing.

---

## 6. Recommended scope for Agent 1

**Authorise one cycle: `R-1` + `R-3b` + `R-5`, i.e. `A+D`.** Justification:

1. **No interaction.** Verified together: 27/27, 147/147, all 26 required controls intact.
2. **Two sites, both closed sets.** `A` adds `never` to one alternation; `D` makes one copula optional.
   Neither touches the attribution predicates, the span rule, or the foil set.
3. **It removes the only fail-closed family** (`R-1`), which is the one with a genuine reachability path
   and the one that rejects a true statement.
4. **It leaves `R-4` for its own cycle**, which is correct discipline — `R-4` needs a structural fix whose
   safe form is not yet established, and bundling it would risk exactly the `C+D` regression above.

**Defer `R-4`/`R-4b` as a separate item.** Do not treat them as blocking. They are fail-open on a shape
that cannot appear while `TN-C-15` stands, and the naive fix is demonstrably worse than the defect.

**Acceptance conditions I would apply to the `A+D` cycle** (the set I will re-run):

| Must keep | Count | State at `7662926` |
|---|---|---|
| Object negations (`, not the audio`, `not any`, `but not`, longer list) | 4 | all PASS ✅ |
| Positive ownership controls | 5 | all FAIL ✅ |
| `CONDITION-1` forms (incl. `TD-82`, `TD-101`) | 4 | all PASS ✅ |
| `F-1` (and/but/semicolon) and `F-1b` | 3 | all FAIL ✅ |
| `CONDITION-2` + three-line + two-line connective | 3 | all FAIL ✅ |
| `_joinable` boundaries + cross-pairing | 7 | all PASS ✅ |
| Clean document | — | 27/27 |
| Full suite | — | 147/147 (plus the new cases) |

**`R-1`, `R-1b`, `R-1c`, `R-3b`, `R-5`, `R-5b`, `R-5c` must all reach PASS/FAIL as required.**
**`R-4` and `R-4b` must be *unchanged* by this cycle** — if they move, the cycle has over-reached.

---

## 7. Severity table

| Defect | Probes | Direction | Severity | Reachable in contract's voice | Recommendation |
|---|---|---|---|---|---|
| **D-a** negator set | `R-1`, `R-1b`, `R-1c` | fail-closed | **Low–Medium**: rejects a *true* statement; the only family with a real reachability path | **Yes** — denying Agent 1 owns audio is exactly `TN-C-15` | **Close now** (cycle `A+D`) |
| **D-b** copula/participle | `R-3b`, `R-5`, `R-5b`, `R-5c` | fail-open | **Low**: escape-resistance only; shape would be contract-violating content | **No** | **Close now** (cycle `A+D`) |
| **D-c** foil set | `R-4`, `R-4b` | fail-open | **Low** on reachability, **but the fix is high-risk** | **No** | **Defer**; one-line fix is unsafe |
| **D-d** predicate verbs | *(not probed)* | fail-open | Lowest | **No** | **Refuse** — taxonomy expansion |

**Nothing here is a material blocker**, and the `§3.6` record that these are non-blocking stands
uncontradicted. `D-a` is the only item I would call worth doing promptly, and only because it produces a
false alarm on a statement the contract endorses.

---

## 8. What this assessment does not do

- **Does not reopen `F-1b`.** `7662926` / `50578ed` remain `CLOSED`; no probe above touches the
  object-negation `not` requirement, and `F-1b`'s verdict is unchanged (re-verified: FAIL).
- **Does not modify any file.** Every mutation was applied to copies under `/tmp` (`/tmp/a310`,
  `/tmp/fixrun`); `7662926` and `50578ed` are untouched.
- **Does not design or implement the fix.** §5 reports what I *measured* when I applied candidate edits in
  a scratch copy, so that Agent 1 is not sent into the `C+D` trap. Agent 1 owns the implementation.
- **Does not propose contract-normative text**, and no contract sentence is implicated by any finding.
- **Does not touch `L-1`/`L-2`** (the parked documentation items) or investigate families beyond the 14
  probes, except `D-d`, which is recorded as a deliberate exclusion at the same line.
- **Does not execute acceptance cases.** **0 of 67** executed; the 147 regressions are tests of the checker.

**Status unchanged:** C-05 `DESIGN_ONLY`, unsigned, unfrozen. `U-07` `OPEN`. No MEAD. `TN-C-11` /
`TN-A-01` / `TN-A-02` unresolved and untouched. `B-15` stays `OPEN`. The residual families are
**`OPEN — assessment returned`**; `D-c` remains open by recommendation, not by neglect.

---

*End of assessment. `TDD-A2-ASSESS-C05-RESIDUAL-001` v1.0. Four distinct defects over three sites; all in
the instrument, none in the contract; `A+D` (`R-1`, `R-3b`, `R-5`) is safe and recommended now; `R-4` is
deferred because its obvious fix breaks eight required controls and re-opens a `not only` hazard.*
