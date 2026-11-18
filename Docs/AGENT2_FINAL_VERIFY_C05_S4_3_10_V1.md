# Independent Final Verification — S4.3.10 (F-1b)

**Review ID** `TDD-A2-FINAL-VERIFY-C05-003` v1.0
**Reviewer** Agent 2
**Target** `7662926c4c3b7293daedcc393c0ec4d015cdd883` — "S4.3.10: the object negation must be stated (F-1b)"
**Verdict** **PASS WITH UNRELATED LIMITATIONS**

---

## 1. Commit and clean-archive identity

`7662926` resolves on `refs/heads/arena/3bc206a0-tdd`, dated `2026-11-18 10:07:45 +0000`, parent
`83c24f9` (S4.3.9). All work below comes from `git archive 7662926 | tar -x -C /tmp/s4310` and from
`git archive 83c24f9 | tar -x -C /tmp/s439`; no branch tip and no working-copy file was substituted.

| Field | Register declares | `git rev-parse 7662926:…` | Match |
|---|---|---|---|
| Document `…_V4_3_10.md` | `857778e18a35b35b1a5420905ec5f1482fddf868` | `857778e18a35b35b1a5420905ec5f1482fddf868` | ✅ |
| Register `…_V4_3_10_PROVENANCE.md` | `675014ec84852d92ffe37769802ae97ac86796e3` | `675014ec84852d92ffe37769802ae97ac86796e3` | ✅ |
| Validator `dv_c05.py` | `353a2bff220d4daa4c176daafc941256098959ed` | `353a2bff220d4daa4c176daafc941256098959ed` | ✅ |
| Suite `test_dv_c05_regressions.py` | `7ab55805c27a271706f16e9295f1f503dc5a6c94` | `7ab55805c27a271706f16e9295f1f503dc5a6c94` | ✅ |

Document 2441 lines. Six files changed against `83c24f9`; **no `V4_3_11` exists** on any ref
(re-verified immediately before publishing).

**Predecessor integrity — all byte-identical, none silently modified:**

| Artifact | At `83c24f9` | At `7662926` |
|---|---|---|
| S4.3.9 doc | `72d218a8…` | `72d218a8…` ✅ |
| S4.3.8 doc | `3c6bab6c…` | `3c6bab6c…` ✅ |
| S4.3.7 doc | `0a0c36be…` | `0a0c36be…` ✅ |
| S4.3.6 doc | `e3a1fa85…` | `e3a1fa85…` ✅ |

**The change is exactly one alternation.** The validator diff is two hunks totalling `+11/−3`:
the object-negation construction loses its comma alternative, and `REG` advances to the S4.3.10
register path (mandatory, not substantive). Suite diff is `+50/−0` — **no deletions**, so no
carried case was edited or removed.

```diff
-    re.compile(r'(?:\bnot|,)\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),
+    re.compile(r'\bnot\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),
```

---

## 2. F-1b reproduction — **CLOSED**

Tested by injecting the statement as an obligation-shaped line immediately before
`## 9. Shared read-surface and arbitration obligations`, then reading the `DV-22` verdict.

| Input | S4.3.9 | S4.3.10 | Required |
|---|---|---|---|
| `No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.` | **PASS** ❌ | **FAIL** ✅ | FAIL |

**The FAIL is caused by the intended ownership logic, not by an unrelated rule or by formatting.**
I instrumented the predicate rather than inferring from the verdict:

| | S4.3.9 | S4.3.10 |
|---|---|---|
| mention @3 (`No audio cue…`) | negated=False, attributed=False | negated=False, attributed=False |
| mention @42 (`, the audio cue belongs to Agent 1.`) | **negated=True**, attributed=True → excused | **negated=False**, attributed=True → **offence** |
| `NEG_BEFORE` match spanning mention @42 | `[10] ', the audio' span=(36,47)` | **none** |

At S4.3.9 the S4.3.6 construction matched the literal string `', the audio'` with no negator in it,
and because a denial excuses a mention only when its match *spans* it, that bare comma excused the
second mention. At S4.3.10 no `NEG_BEFORE` entry spans it, `negated_mention` returns False, and
`attributed_to_agent_1` returns True — the `belongs to` attribution at work. `scan offenders 1`.
The mechanism is precisely the one Agent 1 describes.

**The four reported equivalent constructions**, all verified independently:

| Case | Statement | S4.3.9 | S4.3.10 | Required |
|---|---|---|---|---|
| `TD-104` | `…, the audio cue belongs to Agent 1.` | PASS | **FAIL** | FAIL ✅ |
| `TD-105` | `…, the audio cue is owned by Agent 1.` | PASS | **FAIL** | FAIL ✅ |
| `TD-106` | `…, the audio cue is Agent 1's.` | PASS | **FAIL** | FAIL ✅ |
| `TD-107` | `…, the audio cue belongs to the first agent.` | PASS | **FAIL** | FAIL ✅ |
| `TD-108` | `Agent 1 owns the camera, the audio cues.` *(comma-joined object list)* | PASS | **FAIL** | FAIL ✅ |

All five move in the closed direction. `TD-108` is the *"comma-joined object-list"* form, and it is
`Agent 1 owns the camera, the audio cues.` — a comma-separated list of objects, where the comma alone
used to negate the second object. It is not a passive construction; I initially probed a passive
appositive and it does not move, which is correct and is addressed in §7.

---

## 3. Legitimate statements protected — **ALL HOLD**

Eight legitimate object negations, each checked at both revisions; a regression would show as
S4.3.10 FAIL where S4.3.9 passed.

| Legitimate form | Input | S4.3.9 | S4.3.10 |
|---|---|---|---|
| camera, not audio | `Agent 1 owns the camera, not the audio cues.` | PASS | **PASS** ✅ |
| `not any` form | `Agent 1 owns the camera, not any audio cues.` | PASS | **PASS** ✅ |
| `but not` form | `Agent 1 owns the camera, but not the audio cues.` | PASS | **PASS** ✅ |
| `not any`, no comma | `Agent 1 owns the camera not any audio cues.` | PASS | **PASS** ✅ |
| comma, no space | `Agent 1 owns the camera,not the audio cues.` | PASS | **PASS** ✅ |
| **longer list control** | `Agent 1 owns the camera, the lighting rig, the montage track, and not the audio cues.` | PASS | **PASS** ✅ |
| longer list, `any` | `Agent 1 owns the camera, the lighting rig, and not any audio cues.` | PASS | **PASS** ✅ |
| modifier retained | `Agent 1 owns the camera, not the C-05 audio cues.` | PASS | **PASS** ✅ |

The `the`/`any` requirement, the modifier class and the noun are all intact. The comma is *not*
required, and a comma alone is no longer sufficient — the negator is what carries the rule. This is
the correct reading of TD's instruction not to assume every comma before an ownership phrase is
contradictory.

**Positive ownership controls — all still caught at both revisions:**

| Input | S4.3.9 | S4.3.10 |
|---|---|---|
| `The audio cues belong to Agent 1.` | FAIL | **FAIL** ✅ |
| `Agent 1 owns the audio cues.` | FAIL | **FAIL** ✅ |
| `Audio: Agent 1.` | FAIL | **FAIL** ✅ |
| `The audio cues are the first agent's.` | FAIL | **FAIL** ✅ |
| `Agent 1 owns the audio cue selection.` | FAIL | **FAIL** ✅ |
| `The audio cues are owned by Agent 1.` | FAIL | **FAIL** ✅ |

**The remedy is not bought by weakening the positive form.**

---

## 4. Preserved corrections — **ALL INTACT**

### 4.1 F-1 (S4.3.9, comma/conjunction boundary)

| Form | Input | S4.3.9 | S4.3.10 |
|---|---|---|---|
| conjunction `and` | `No audio cue is assigned to Agent 2 and the audio cue belongs to Agent 1.` | FAIL | **FAIL** ✅ |
| conjunction `but` | `…, but the audio cue belongs to Agent 1.` | FAIL | **FAIL** ✅ |
| semicolon | `No audio cue is assigned to Agent 2; the audio cue belongs to Agent 1.` | FAIL | **FAIL** ✅ |

F-1's clause-bounding held. Closing F-1b did not reopen it.

### 4.2 CONDITION-1 (quantified denials) — five forms

| Input | S4.3.9 | S4.3.10 |
|---|---|---|
| `No audio cue belongs to Agent 1.` | PASS | **PASS** ✅ |
| `There is no audio cue that belongs to the first agent.` | PASS | **PASS** ✅ |
| `None of the audio cues belong to the first agent.` | PASS | **PASS** ✅ |
| `No audio cue is owned by Agent 1.` | PASS | **PASS** ✅ |
| `No audio cue is the first agent's.` | PASS | **PASS** ✅ |

`TD-82` and `TD-101` — the two controls the assignment names — were verified both from the suite and
by direct injection: **PASS → PASS** in both, no movement.

### 4.3 CONDITION-2 and the continuation controls

| Input | S4.3.9 | S4.3.10 |
|---|---|---|
| `Counts: 6 declared` / `The audit shows 5 observed.` | FAIL | **FAIL** ✅ |
| `Counts: 6 declared` / `Then 5 observed.` | FAIL | **FAIL** ✅ |
| `Counts: 6 declared` / `And 5 observed.` | FAIL | **FAIL** ✅ |
| three-line wrap `… / and then / 5 observed.` | FAIL | **FAIL** ✅ |
| two-line connective `… declared and / 5 observed.` | FAIL | **FAIL** ✅ |
| lowercase wrap | FAIL | **FAIL** ✅ |

### 4.4 MINOR-1 and the seven `_joinable` boundaries

`DV-24` reports `pairs read 10` at both revisions — matching the runner, so MINOR-1's class holds.
All seven boundaries still **PASS** at both (no false join reintroduced):

| Boundary | S4.3.9 | S4.3.10 |
|---|---|---|
| list item | PASS | **PASS** ✅ |
| sentence terminator | PASS | **PASS** ✅ |
| heading | PASS | **PASS** ✅ |
| blockquote | PASS | **PASS** ✅ |
| table row | PASS | **PASS** ✅ |
| fence | PASS | **PASS** ✅ |
| blank line | PASS | **PASS** ✅ |
| cross-pairing (two labels each) | PASS | **PASS** ✅ |

---

## 5. Full suite and document validation

Both run from clean archives, on the documents that belong to each commit.

| | S4.3.9 (`/tmp/s439`) | S4.3.10 (`/tmp/s4310`) |
|---|---|---|
| Document validation | **27/27** | **27/27** |
| Regression suite | **129/129** | **147/147** |

**Case arithmetic derived, not read:** at S4.3.10 the suite holds **121 distinct `TD-` ids**
(`TD-01`…`TD-121`), of which **18 are new** (`TD-104`…`TD-121`, contiguous, no gaps), plus **20
non-`TD` cases** carried from S4.3 — total **147**. `147 − 18 = 129` carried, which equals S4.3.9's
own 129. The register's `129 carried + 18 added = 147` is arithmetically correct.

---

## 6. Comparison against S4.3.9 — only five changes

I ran the S4.3.10 suite with `--compare` against the S4.3.9 validator (`83c24f9:docs/validation/dv_c05.py`)
and parsed **all 147 result rows**, not a sample.

**Exactly five verdicts move, all `PASS → FAIL`, all in the `F-1b` family:**

| Case | Movement |
|---|---|
| `TD-104` | PASS → FAIL |
| `TD-105` | PASS → FAIL |
| `TD-106` | PASS → FAIL |
| `TD-107` | PASS → FAIL |
| `TD-108` | PASS → FAIL |

- **All 129 carried cases keep their expected verdicts.** Zero rows disagree with their own
  expectation (`0 of 147`).
- The **thirteen other new cases do not move** — `TD-109`…`TD-113` (legitimate negations, PASS both),
  `TD-114`/`TD-115` (positive ownership, FAIL both), `TD-116`/`TD-117` (F-1, FAIL both),
  `TD-118` (CONDITION-1, PASS both), `TD-119` (CONDITION-2, FAIL both), `TD-120`/`TD-121` (the
  document's own verdicts, PASS both). **No unexpected verdict change anywhere.**

### 6.1 The 25/27 → 27/27 figures are explained honestly, and nothing is suppressed

The task asks whether S4.3.10's 27/27 comes from suppressing an actual finding. **It does not.**
The two figures are *not* the same measurement, and conflating them is the trap here:

| Measurement | Result | Reproduced |
|---|---|---|
| S4.3.9 document under **S4.3.9** validator | 27/27 | ✅ |
| S4.3.9 document under **S4.3.10** validator | **25/27** | ✅ |
| S4.3.10 document under **S4.3.10** validator | 27/27 | ✅ |

The 25/27 is cross-application: S4.3.9's text scored by the corrected rule. Its two failures are
`DV-27` (it names the S4.3.9 register — unavoidable) and `DV-22` with **exactly one offender**:

```
DV-22 FAIL — … audio mentions evaluated 155; scan offenders 1
   [(964, '**One further same-line fail-open was found while testing this correction…')]
```

Line 964 of S4.3.9 is the §2.24 paragraph that **reports F-1b by quoting the failing sentence in
ordinary prose**. The corrected rule reads that quotation as it reads a real assertion. That is the
honest outcome, not a false positive to be engineered around.

**S4.3.10 does not delete the sentence — it relabels the reproduction.** The failing sentence still
appears **twice** in S4.3.10, and I verified both occurrences sit inside `[QUOTED]` tables:

| Revision | Occurrence | Region | Exempt? |
|---|---|---|---|
| S4.3.9 | line 964 | **unfenced prose** | no → offender |
| S4.3.10 | line 327 | `[QUOTED]` table | yes |
| S4.3.10 | line 1006 | `[QUOTED]` table | yes |

The finding remains fully reported — in the §0 change table and in a results table that shows
`PASS | PASS | FAIL` across the three revisions. **The evidence was not removed; it was labelled.**

**The mention count moves the opposite way from suppression:** S4.3.10 evaluates **165** audio
mentions against **0** offenders, versus S4.3.9's **155** mentions against **1** offender. The
corrected validator examines *more* of the document and finds *nothing*, which is the signature of a
real fix rather than a silenced check.

---

## 7. Remaining limitations — unrelated to F-1/F-1b

Three items. **None is a defect in F-1 or F-1b, none warrants another revision, and I record them
only because leaving them unstated would misrepresent what I checked.**

### L-1 (documentation, pre-existing class) — §13.1's `DV-22` result row is a stale snapshot

§13.1 is headed *"The twenty-seven checks and their actual output"*, and its `DV-22` row states:

```
exempt lines 343 (fenced 201, quoted table 139, marked block 3); …
audio mentions evaluated 146; scan offenders 0
```

The runner prints `exempt lines 401 (fenced 221, quoted table 177, marked block 3) … mentions
evaluated 165; scan offenders 0` for this document. **The row is byte-identical to S4.3.8's**, where
those values *were* correct (I verified: S4.3.8 runner → 343/201/139/146, matching its own row). So
the row was inherited verbatim while the prose grew from 2349 to 2441 lines — it was not introduced
by the F-1b change and it does not affect any verdict. It is the same class as the `MINOR-1` drift:
a hand-carried tally that stopped tracking its computed value. **Fix it by re-measuring that one
cell, or by heading §13.1 as a snapshot of the revision that produced it.** No re-review needed.

### L-2 (documentation) — the version block states the suite as 146, not 147

Line 331 states `129 → 147` (correct). Line 2353's version block states `the suite grows 129 → **146**`
(incorrect; the suite is 147). Internal contradiction, one digit, no verdict affected.

### L-3 (out of scope by directive) — the appositive `Agent 1` family remains open

`The audio cue, supplied by Agent 1, drives the mixer.` and the comma-appositive variants still pass
at **both** revisions. This is Agent 1's §3.6 residual family, which they explicitly declined to
widen to and which my directive excludes. **It is unchanged by this correction, it is not F-1 or
F-1b, and I did not investigate it further.**

---

## 8. Conclusion

# PASS WITH UNRELATED LIMITATIONS

**F-1b is genuinely closed, and closed in the right place.** The bare comma alternative is gone; the
original failing statement moves PASS → FAIL; the same movement repeats for the `is owned by`,
possessive, synonym and comma-joined object-list forms; and the FAIL is provably produced by the
intended `DV-22` ownership logic — I traced it to the disappearance of the `', the audio'` spanning
match, with `negated_mention` flipping False and the `belongs to` attribution firing.

**Nothing legitimate was sacrificed.** Eight object-negation forms including the longer-list control
still pass; six positive-ownership controls still fail; the `the`/`any` requirement, the modifier
class and the noun are untouched. One alternation was removed and nothing was added, which is the
smallest change that could close the defect.

**Nothing previously verified was weakened.** F-1, CONDITION-1, CONDITION-2, MINOR-1's class and all
seven `_joinable` boundaries hold; every predecessor document is byte-identical; every predecessor
tally is unchanged and I reproduced each one (S4.3.9 25/27, S4.3.8 → S4.3.4 each 26/27). Exactly five
verdicts move, all closed-direction, with zero expectation disagreements across all 147 cases.

**The 27/27 is not obtained by suppression.** It required relabelling a prose quotation as a
`[QUOTED]` reproduction, the finding is still reported twice in the new text, and the corrected
validator evaluates *more* mentions (165 vs 155) while finding *fewer* offenders (0 vs 1).

**The three limitations are unrelated to F-1/F-1b**, are documentary or explicitly out of scope, and
none of them affects a single verdict. **I request no further revision.**

---

## 9. Scope and governance

Verification only. **I modified no implementation and no documentation.** Every mutation was applied
to a copy under `/tmp`; `7662926` and `83c24f9` are untouched and the tree is clean.

- I did **not** widen validator coverage or introduce any rule.
- I did **not** investigate unrelated residual families (L-3 is recorded as excluded, not explored).
- I did **not** execute any of the 67 proposed acceptance cases.
- **C-05 remains `DESIGN_ONLY`, unsigned and unfrozen. U-07 remains OPEN.**
- No MEAD selected; no normative clause resolved; `TN-C-11` and the `TN-A` boundary untouched.

**43 obligation rows, `TN-C-11`/`TN-C-14`/`TN-C-15`, `TN-A-01`…`TN-A-03`, the 17 case specifications
and `D-1`…`D-7` were byte-compared between `72d218a8…` and `857778e1…`: all identical. 18 suites /
67 cases unchanged. `git diff 83c24f9 7662926 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_9.md` is
empty.**

**The 147 regression cases are tests of the checker, not acceptance evidence. 0 of 67 acceptance
cases executed.**

---

*End of verification. `TDD-A2-FINAL-VERIFY-C05-003` v1.0. **PASS WITH UNRELATED LIMITATIONS** — F-1b
is closed, every prior correction is intact, and no further revision is requested.*
