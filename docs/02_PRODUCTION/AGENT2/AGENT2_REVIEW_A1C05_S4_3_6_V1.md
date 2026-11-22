# AGENT 2 — INDEPENDENT REVIEW OF `A1-C05-S4.3.6`

**Review ID:** `TDD-A2-REVIEW-A1C05-S4-3-6-001` · **Version:** 1.0
**Author:** Agent 2 — World Structure and Level Architecture
**Status:** `DESIGN_REVIEW_ONLY` — review only. Nothing signed, frozen, merged or approved.
**No MEAD selected. U-07 open. C-05 proposed.** **0 of 67 acceptance cases executed.**
**Outcome:** **`PASS WITH CONDITIONS`** (§9) — one MAJOR condition, confined to `DV-22`.

> **Scope note.** This is a review of **instruments**, not of contract behaviour. S4.3.6 changes no
> contract sentence; I verified that independently (§6) rather than accepting it. Every result below
> is a Python validator run over Markdown. **No telegraph, producer, consumer or engine was
> executed, and none exists in this workspace.** A validator that reports 27/27 says the *document*
> is self-consistent and that the *checker* reaches the defects it was built for. It says nothing
> about whether a C-05 implementation would behave correctly.

---

## 1. Exact target and provenance verification

**Establishment order.** I verified the commit and blob **before** reading the document, and
re-verified at commit time. `git fetch` was run first — the objects were not in the local clone, and
`git rev-parse 034d091` failed with *"unknown revision"* until I fetched. **I record that because an
abbreviated hash resolving is not the same as an object existing**, and the failure mode here is
silent substitution of whatever happens to resolve.

| Field | Verified value | Status |
|---|---|---|
| Repository | `The-Mhood/TDD` | — |
| Branch | `arena/3bc206a0-tdd` | — |
| **Target commit** | **`034d091e1abcb507fdba6df4a05318a15aa5d7a1`** | **VERIFIED** = stated `034d091`; branch head |
| **Successor document** | `docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md` | 1,931 lines |
| **Document blob** | **`e3a1fa85243a4749591363d4196bb5d65dad7c84`** | **VERIFIED** = stated blob, exact |
| **Provenance register** | `…V4_3_6_PROVENANCE.md`, blob **`ce1ebc8d079f83aa594ef222ff71a108def1e8a6`** | 92 lines, same commit |
| **Validator** | `docs/validation/dv_c05.py`, blob **`840fed6730a5b2e18a5f717f98c6de273b9c8721`** | **matches register exactly** |
| **Regression suite** | `…test_dv_c05_regressions.py`, blob **`ee69f549a5c684c211a3dc15878c69c6dc32afe8`** | **matches register exactly** |
| **Predecessor unchanged** | S4.3.5 at `baa31db`, blob `a0b46f46…` | **VERIFIED** — still `a0b46f46` at `034d091` |

### 1.3 S4.3.5 remains unchanged — checked two ways

```
$ git rev-parse 034d091:docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md
a0b46f46c81e85cea5d04b940aaf9aee46c19deb          # identical blob, same path, later commit

$ git diff --stat baa31db 034d091 -- docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_5.md
(empty)
```

The predecessor is byte-identical at both commits **and** the diff across the range is empty. Both
checks matter: a blob at a path can be unchanged while the file is deleted and re-added elsewhere.

### 1.4–1.6 Instrument pinning — the question that decided my last review

The register names the **validator blob `840fed67`** and the **suite blob `ee69f549`** as fields, and
both resolve to those exact values at `034d091`. Every result in §2 below was produced from a
**`git archive` extraction of `034d091`**, so the instruments are pinned by construction.

**This is the specific failure mode I found in my own W-M2.15 test module** (published in my S4.3.5
review as MINOR-4): a test that reads an instrument from `origin/arena/3bc206a0-tdd` silently
retargets when the branch tip moves. **Agent 1's suite is not exposed to it** — I confirmed by
extracting, not by inspecting. I also confirmed that **S4.3.5's own instruments are preserved at
`baa31db`** (validator `6927644f…`, suite `954588d3…`), which is what makes the before/after
comparison in §2.4 reproducible at all.

---

## 2. Reproduction — commands and actual output

**Method.** Clean extraction, no working tree contamination:
`git --git-dir=/home/user/TDD/.git archive 034d091 | tar -x` into `/tmp/s436`.

### 2.1 Successor validator — 27/27 `VERIFIED`

```
$ cd /tmp/s436 && python3 docs/validation/dv_c05.py docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_6.md
DV-24 PASS — computed 7 declared / 5 observed; anchor sites 3/3 []; pairs read 24; disagreeing pairs 0 []
DV-25 PASS — TN-C-14 rules 7/7, missing []; T-C05-64 extensions 4/4, missing []
DV-26 PASS — falsified premise absent True; 'observable through a mid-frame pull' present True; PO-3 and PO-5 both retained True
DV-27 PASS — placeholders found []; S4.1 and S4.2 commit+blob recorded in §17 True; …
27/27 checks passed
```

### 2.2 Regression suite — 86/86 `VERIFIED`

```
$ python3 docs/validation/test_dv_c05_regressions.py
86/86 regression cases behaved as required
```

I parsed all 86 rows and compared each row's actual verdict against its expected verdict:
**0 mismatches.** 86 is also the correct arithmetic: 67 carried forward + 19 added.

### 2.3 Predecessor baselines `VERIFIED` — including the reported DV-27 distinction

Each predecessor run against the **S4.3.6** checker:

| Document | Score | Failing checks |
|---|---|---|
| S4.3.5 (`a0b46f46`) | **26/27** | `DV-27` only |
| S4.3.4 (`41df692d`) | **26/27** | `DV-27` only |
| S4.3.3 (`d827e017`) | **26/27** | `DV-27` only |
| S4.3.2 (`74840d70`) | **26/27** | `DV-27` only |
| S4.3.1 (`c8708ef0`) | **26/27** | `DV-27` only |
| S4.3 (`74546027`) | **26/27** | `DV-27` only |
| **S4.2** (`7d03e1df`) | **24/27** | **`DV-22`, `DV-24`, `DV-27`** |
| S4.1 (`d54e194a`) | 21/27 | `DV-20`, `DV-22`, `DV-24`, `DV-25`, `DV-26`, `DV-27` |
| S4.0 (`424d2c69`) | 21/27 | same six |
| S3 (`07723236`) | **10/27** | — |

**The DV-27 distinction is real and correctly described.** Every 26/27 above fails on exactly one
check, `DV-27`, which pins **this** document's own register — the expected, non-defect failure.

**S4.2's 24/27 needs one clarification the register does not make.** Its three failures are `DV-22`,
`DV-24` and `DV-27`, not `DV-27` alone. That is **checker growth, not a regression in S4.2**: S4.2
scored **27/27 under the validator that shipped with it** (`a788f95`, blob `381be714…`) — I ran it,
and it still does. Same for S4.3.4 under its own validator (`90971e0`): **27/27**. **A predecessor
scoring lower under a later checker is the expected shape of a checker that got stricter.** I make
the distinction explicit because read quickly, "S4.2 → 24/27" invites the wrong inference.

### 2.4 The twelve verdict changes `VERIFIED` exactly

```
$ git show baa31db:docs/validation/dv_c05.py > /tmp/dv_s435.py   # 6927644f…
$ python3 docs/validation/test_dv_c05_regressions.py --compare /tmp/dv_s435.py
```

Mechanical count over all 86 rows: **12 rows move, 11 `PASS → FAIL`, 1 `FAIL → PASS`.**

| | Cases |
|---|---|
| **11 PASS → FAIL** | `TD-42`, `TD-43`, `TD-44`, `TD-45`, `TD-46` (`DV-22`) · `TD-52`, `TD-53`, `TD-54` (`DV-24`) · `TD-56`, `TD-57`, `TD-58` (`DV-11`) |
| **1 FAIL → PASS** | **`TD-47`** — a *false positive* being corrected, not a defect being introduced |
| **Stable** | `TD-48`…`TD-51`, `TD-55`, `TD-59`, `TD-60`, and every pre-existing `TD-01`…`TD-41` and probe row |

**No carried-forward case regressed.** Zero rows moved from an expected verdict they previously met.
The one `FAIL → PASS` is the correct direction and is the interesting one: the S4.3.5 predicate
flagged `Agent 2, unlike Agent 1, owns the audio cues` — a sentence in which **Agent 2 is the
subject** — as an Agent-1 assignment. The correction removes a false positive while adding five
false negatives' worth of true positives. That is a genuine improvement in discrimination, not a
relaxation; §3.6 tests whether the relaxation hid anything.

---

## 3. DV-22 — `TD-42` … `TD-51`

### 3.1 The mechanism

Two changes, both of which I checked against my own published recipe:

```python
# line 415 — synonym read through a NAMED group
AGENT_REF = re.compile(r'agent[-\s]?(?P<num>[12])\b|the\s+first\s+agent\b', re.I)

# line 421 — the foil marker must precede the reference
FOIL_BEFORE = re.compile(r'(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\s*$', re.I)

# line 553 — foils are dropped before "nearest prior" is taken
before = [m for m in AGENT_REF.finditer(ln, start, pos) if not is_foil(ln, m)]
```

**This is exactly the fix I specified and measured at W-M2.16** — including the named group, which I
had flagged as the trap that makes the naive patch silently ineffective (`group(1)` would be `None`).
Agent 1 implemented it correctly. `agent_of()` returns `'1'` for the synonym, so attribution works.

### 3.2 Published cases — all ten reproduce `VERIFIED`

| ID | Input | Expected | Actual | Correct? |
|---|---|---|---|---|
| `TD-42` | `Agent 1, unlike Agent 2, owns the audio cues.` | FAIL | **FAIL**, 1 offender | ✅ |
| `TD-43` | `The first agent owns the audio cues.` | FAIL | **FAIL**, 1 offender | ✅ |
| `TD-44` | `Agent 1, as opposed to Agent 2, owns the audio cues.` | FAIL | **FAIL**, 1 | ✅ |
| `TD-45` | `Agent 1 rather than Agent 2 owns the audio cues.` | FAIL | **FAIL**, 1 | ✅ |
| `TD-46` | `Agent 1, but not Agent 2, owns the audio cues.` | FAIL | **FAIL**, 1 | ✅ |
| `TD-47` | `Agent 2, unlike Agent 1, owns the audio cues.` | **PASS** | **PASS**, 0 | ✅ (was a false positive) |
| `TD-48` | `Agent 1, unlike Agent 2, owns no audio cues.` | PASS | **PASS**, 0 | ✅ |
| `TD-49` | `The first agent has no C-05 audio responsibility.` | PASS | **PASS**, 0 | ✅ |
| `TD-50` | `Agent 1 owns the camera, not the audio cues.` | PASS | **PASS**, 0 | ✅ |
| `TD-51` | `Agent 2 selects the camera, whereas Agent 1 owns the audio cues.` | FAIL | **FAIL**, 1 | ✅ |

### 3.3 The `whereas` departure — **assessed and ACCEPTED**

Agent 1 deliberately excludes `whereas` from the foil set, arguing it introduces a clause whose
subject is the reference that follows. **I tested the claim rather than the reasoning:**

| Probe | Expected | Actual | Correct? |
|---|---|---|---|
| `Agent 2 selects the camera, whereas Agent 1 owns the audio cues.` | FAIL | **FAIL** | ✅ |
| `Agent 1 selects the camera, whereas Agent 2 owns the audio cues.` | PASS | **PASS** | ✅ |
| `Agent 2 owns the audio cues, whereas Agent 1 owns the camera.` | PASS | **PASS** | ✅ |
| `Agent 1 owns the audio cues, whereas Agent 2 owns the camera.` | FAIL | **FAIL** | ✅ |
| `Agent 1 owns no audio cues, whereas Agent 2 owns the camera.` | PASS | **PASS** | ✅ |
| `Agent 1 owns the audio cues whereas Agent 2 owns the camera.` (no comma) | FAIL | **FAIL** | ✅ |

**The departure is sound.** `whereas` is a coordinating contrast joining two *independent clauses*,
so unlike `unlike` it does not make the following reference a foil — it makes it a new subject.
Treating it as a foil would have discarded a genuine subject and produced a false negative. **Agent
1's documented reason is correct, and I verified the behaviour rather than accepting the note.**

### 3.4 The object-negation departure — **assessed and ACCEPTED**

`Agent 1 owns the camera, not the audio cues.` passes. **Risk:** could object negation be used to
suppress a *genuine* audio assignment?

| Probe | Expected | Actual | Correct? |
|---|---|---|---|
| `Agent 1 owns the camera, not the audio cues.` | PASS | **PASS** | ✅ |
| `Agent 1 owns the audio cues, not the camera.` | FAIL | **FAIL** | ✅ |
| `Agent 1 owns the audio cues, not the audio selection rights.` | FAIL | **FAIL** | ✅ |
| `Agent 1 selects the camera, not the audio cues.` | PASS | **PASS** | ✅ |
| `Agent 1 owns the audio cues, and the first agent has no camera duty.` | FAIL | **FAIL** | ✅ |

**No hiding observed.** The negation is read per-mention and does not veil a second assignment on the
same line.

### 3.5 False-positive sweep — 13 probes, **0 failures**

Genuine denials (`owns no audio cues`, `does not own`, `not … responsibility`, `no ownership of audio
cue selection`, `has no responsibility for audio cue selection`) all PASS; benign co-occurrence
(`Agent 1 consumes the snapshot; Agent 2 owns the audio cues`, `Agent 1 owns the camera, Agent 2 owns
the audio cues`) all PASS; genuine assignments in four surface forms (`owns`, `is responsible for`,
`are owned by Agent 1`, `Audio cues: Agent 1.`) all FAIL. **The fix did not buy recall with
precision.**

### 3.6 Two false negatives remain — **MAJOR-1**

I found these by probing beyond Agent 1's published set. Both produce a **clean `27/27`** — no other
check catches them.

| # | Exact input | Expected | Actual | Correct? |
|---|---|---|---|---|
| **A** | `The audio cues are the first agent's.` | **FAIL** | **PASS**, 0 offenders | ❌ |
| **B** | `Agent 1, unlike what the wargame community might generally assume about Agent 2, owns the audio cues.` | **FAIL** | **PASS**, 0 offenders | ❌ |

**Root cause A — line 539.** The synonym was taught to `AGENT_REF` and to the *nearest-prior*
attribution path, but **not to `FORWARD_OWNER`**, whose possessive pattern is still hard-coded to the
literal:

```python
re.compile(r'\baudio\b[^.;|]{0,30}?\b(?:is|are)\s+agent[-\s]?1[\'\u2019]s\b', re.I)
```

The literal form works — `The audio cues are Agent 1's.` → **FAIL**, verified. The synonym does not.
**This is a partial fix**: `the first agent` is now a recognised *subject* but not a recognised
*possessor*. The same asymmetry will exist for every other attachment path that was not updated —
this is the recurring hazard of extending a lexicon in one place and not the others, and it is why I
recommended in W-M2.16 that the class be closed structurally rather than by widening recognition.

**Root cause B — line 421.** `FOIL_BEFORE` anchors `\s*$` within a **32-character** window before the
match. When a foil clause is longer than that, the marker falls outside the window, `is_foil` returns
`False`, the foil is retained, and "nearest prior reference" resolves to **Agent 2** — the identical
inversion `TD-42` was built to fix, just at a longer distance. Confirmed: the same sentence with a
short foil (`…unlike Agent 2,…`) is correctly caught.

**Severity assessment.** Both are **MAJOR on instrument correctness** and **not BLOCKER**, for the
reason I gave at S4.3.5 and which still holds: **the contract text is correct**, so this is a defect
in the certificate, not in the thing certified. Escape B is **artificial in length** but not in
*structure* — a competent writer producing a contrastive sentence with a subordinate clause will
reproduce it accidentally, which is exactly how `TD-42` arose in my own probing. Escape A is a
**one-word difference** from a form the checker already handles correctly, which makes it the more
likely of the two to be written by accident.

---

## 4. DV-24 — `TD-52` … `TD-55`

### 4.1 Published cases — all reproduce `VERIFIED`

| ID | Input (injected into live text) | Expected | Actual | Correct? |
|---|---|---|---|---|
| `TD-52` | `For the record: declared: 6, observed: 5.` | FAIL | **FAIL**, 3 disagreeing | ✅ |
| `TD-53` | `The tally reads 6 declared and\n5 observed in the instrument.` | FAIL | **FAIL**, 1 | ✅ |
| `TD-54` | `The tally reads 6 declared. Then 5 observed.` | FAIL | **FAIL**, 3 | ✅ |
| `TD-55` | correct pair in all four documented forms | PASS | **PASS**, 0 | ✅ |

### 4.2 Additional probes — 10 of 11 correct

Word numbers (`declared: six, observed: five`), reverse order (`6 observed of 7 declared`),
parenthetical (`declared (6) and observed (5)`), a second pair on one line, tab separators, and
label-first split across a sentence (`declared: 6. Later, observed: 5.`) are **all caught**. Valid
controls in the same forms all pass, so the widening did not over-trigger.

| # | Exact input | Expected | Actual | Correct? |
|---|---|---|---|---|
| **C** | `The tally reads 6 declared\nand then\n5 observed.` | **FAIL** | **PASS**, 0 disagreeing | ❌ |

**Root cause C — line 649.** The cross-line scan joins only **adjacent** pairs:

```python
for i in range(len(lines) - 1):
    scanned += [... pairs(lines[i].rstrip() + ' ' + lines[i + 1].lstrip())]
```

A restatement wrapped over **three** lines is never assembled. Confirmed boundaries: `6 declared\n5
observed` is caught (2 lines); `6 declared\nand then\n5 observed` is not (3 lines); `6 declared\n\n5
observed` is not (blank line). **Severity: MINOR.** This is a residual of the class `TD-53` closes,
the construction is unlikely in a table-heavy contract, and the error would be a *missed* count
rather than a wrong verdict on a real sentence.

---

## 5. DV-11 — `TD-56` … `TD-60`

### 5.1 Three genuine gaps, before and after `VERIFIED`

I mutated the actual §5.4 declaration cells and compared the **S4.3.5** validator (`6927644f`) with
the **S4.3.6** validator (`840fed67`) on the same document:

| Case | Mutation | S4.3.5 | S4.3.6 | Correct? |
|---|---|---|---|---|
| clean document | — | PASS | **PASS** | ✅ |
| **`TD-56`** extra row | `producer owner` → `rows 2 and 3` | **PASS** | **FAIL** | ✅ |
| **`TD-57`** disallowed range | `each consumer` → `rows 5–8` | **PASS** | **FAIL** | ✅ |
| **`TD-58`** falsified cell count | `**23 cells**` → `**99 cells**` | **PASS** | **FAIL** | ✅ |
| **`TD-60`** wrong-owner row | `row 6` → `row 7` | **FAIL** | **FAIL** | ✅ |

The failure messages are specific and correct, e.g.
`TN-C-01: token 'each consumer' maps to rows [5, 6, 7, 8], allowed for TN-C are [5, 6]`.

### 5.2 The three mechanisms

- **Every number and range parsed** (line ~243 region): `rows 2 and 5` was previously read as `{2}`,
  silently discarding the second declaration.
- **Subset, not intersection** (line 243): `elif not decl[tok] <= allowed[pref]:`. Under an
  intersection test, `rows 2 and 5` for a `TN-P` cell passed on row 2 alone. **This is the
  substantive fix** — it is what converts `TD-56`/`TD-57` from passes into failures.
- **Hand cell counts compared** (§5.4 `Used by` column) against the instrument's own tally, closing
  `TD-58`.

**Both departures behave correctly and no valid evidence broke:** the unmodified §5.4 table still
reports `7 declared / 5 observed tokens, 43 cells, 7 cell-count claims checked, 0 failures`.

### 5.3 `TD-60` — is "wrong owner still fails" the correct normative outcome?

**Yes, and I verified the claim rather than accepting it.** `TD-60` fails under **both** validators,
which is what Agent 1 reports. The reasoning in §2.17 is that the owner clause is enforced
**through the row, not through a separate owner map**: rows 3, 7 and 8 sit outside each prefix's
allowed set, so a token naming the wrong agent's row is rejected by the subset test. The only
token spanning two rows is `each consumer` (rows 5–6), whose agent is *per side by definition*.

**Assessment: the outcome is correct but the test is under-specified as a *test*.** It cannot
distinguish "the subset rule catches wrong owners" from "the checker already caught this for an
unrelated reason", because it passes for a reason it does not isolate. It is a valid **assertion** and
a weak **discriminator** — it will not detect a future regression that keeps rows 3/7/8 outside the
allowed sets while breaking owner semantics elsewhere. **MINOR**, and I note it without asking for a
change to S4.3.6, since `TD-60` asserts the right thing.

---

## 6. Normative contract preservation `VERIFIED`

Compared S4.3.6 (`e3a1fa85`) against S4.3.5 (`a0b46f46`).

| Item | Result |
|---|---|
| **All 43 obligation rows** | **identical** — 43 → 43, 0 lost, 0 gained, **0 changed** |
| **All 18 suites / case sum** | **identical** — `(18, 67)` → `(18, 67)` |
| **§5.2 / §5.4 / §9.2 / §4.9 / §3.6 / §4.2** | **identical**, byte for byte |
| **§8 preamble** | **identical**; contains `no C-05 audio responsibility`; `camera and audio` **absent** |
| **`TN-C-11`, `TN-C-14`, `TN-C-15`** | **identical** |
| **`TN-A-01`, `TN-A-02`, `TN-A-03`** | **identical** |
| **`T-C05-63`, `T-C05-64`** | **identical**; all 17 case specifications identical |
| **`PO-5`** | present (28 occurrences), unchanged |
| **`D-1` … `D-7`** | carried unchanged; **not reopened** |

**Substantive normative change: none found.** The document grew 1,779 → 1,931 lines (~196 added,
~44 removed). The additions are **two new administrative sections**, which I read:

- **§0.9** (line 278) — verifies that the Agent 3 S4.3.5 QA review named in the directive is absent.
- **§13.3.6** (line 1683) — the before/after instrument table for `TD-42`…`TD-60`.

The remaining deltas are the revision header, the §2.15–§2.17 disposition material, and the §18.3
stamp. **No obligation was weakened, no interpretation broadened, no scope accidentally changed.**
I found no omission.

**`TN-C-11` / `TN-C-14` / `TN-C-15` / the `TN-A` boundary: I do not resolve them.** I report only
that (a) all four are byte-identical to S4.3.5, (b) `TN-C-14` still bounds staleness at one frame on
the shared axis, and (c) `TN-A-01`…`TN-A-03` still decline to let a C-05 value decide a hit. **The
`TN-C-11`/`TN-A-01`/`TN-A-02` conflict remains unresolved**, TD-09 remains OPEN, and no sentence in
S4.3.6 claims otherwise.

---

## 7. False-positive / false-negative analysis

| | `DV-22` | `DV-24` | `DV-11` |
|---|---|---|---|
| **Probes run** | 33 | 15 | 8 |
| **Correct** | 31 | 14 | 8 |
| **False negatives (missed defect)** | **2** (`A`, `B`) | **1** (`C`) | 0 |
| **False positives (valid text flagged)** | **0** | **0** | **0** |
| **Net vs S4.3.5** | +5 true positives, −1 false positive | +3 true positives | +3 true positives |

**No false positives introduced in any of the three instruments.** That is the more important half
of the result: all three corrections widen detection, and widening is exactly the move that
reintroduces over-triggering. I could not make any of them fire on valid contract text.

**Failure shape.** `B` and `C` are both **distance/span boundaries** — a 32-character foil window, a
one-line join. `A` is a **partial lexical extension**. None is a conceptual error; all three are the
same class: *a rule expressed as a function of the local wording it recognises rather than of the
property it claims.*

---

## 8. Findings, conditions and unverified claims

### 8.1 Findings

| # | Finding | Severity | Where |
|---|---|---|---|
| **MAJOR-1** | `DV-22` possessive form of the synonym escapes (`The audio cues are the first agent's.`) | **MAJOR** | `dv_c05.py` line 539 |
| **MAJOR-2** | `DV-22` foil window is 32 chars — a long foil re-inverts attribution to Agent 2 | **MAJOR** | `dv_c05.py` line 421 |
| **MINOR-1** | `DV-24` joins only adjacent lines; 3-line or blank-separated wraps escape | MINOR | `dv_c05.py` line 649 |
| **MINOR-2** | `TD-60` asserts the right outcome but does not isolate the subset rule | MINOR | suite `TD-60` |
| **OBS-1** | §0.9's "Agent 3 artifact absent" claim is **true** — independently confirmed | OBSERVATION | doc line 278 |
| **OBS-2** | The register's "S4.2 → 24/27" would benefit from the DV-22/DV-24 clarification (§2.3) | OBSERVATION | register |

**MAJOR-1 and MAJOR-2 are one condition**, because they are one predicate and one fix surface.

### 8.2 Claims I checked and could not fault

- **Suite is 86** — not assumed; the runner printed `86/86` and 67 + 19 = 86.
- **12 verdicts move, 11 PASS→FAIL + 1 FAIL→PASS** — counted mechanically over all 86 rows.
- **Validator `+80 / −13`, suite `+64 / −0`** — `git diff --stat` agrees; the suite diff has **no
  `-` lines at all**, so no existing case was edited, renamed or removed. Confirmed independently.
- **19 new cases `TD-42`…`TD-60`** — parsed from the added lines; contiguous, no gaps.
- **§0.9's absence claim** — and this is the one I most wanted to break, because last time my own
  fetch was partial and silently reported "absent" for artifacts that existed. **I re-fetched
  `arena/c64fc525-tdd` explicitly, then re-ran the search.** Result: three `AGENT3` files exist; none
  is the named QA review; no commit among **77** reachable contains it; `DV-24` appears **0** times in
  all three. **Claim stands.**
- **"No invented examples"** — every `TD-42`…`TD-60` counterexample I could reconstruct corresponds
  to a real mutation with a real before/after, and none is attributed to Agent 3.

### 8.3 What is `UNABLE TO VERIFY`

| Item | Why |
|---|---|
| **Agent 3's original `DV-24` counterexamples** | **The artifact does not exist in this repository.** I confirmed this independently. I did **not** attempt to reconstruct them and **do not** attribute any example in this review to Agent 3. |
| **Agent 3's narrower `DV-11` gap** | Same — artifact absent. Its **published S4.1** review (`AGENT3_A1_C05_S4_1_INDEPENDENT_INTEGRATION_REVIEW_V1.md`) *does* contain a `DV-11` finding, and it **AGREES** with my 0-failure result. I note that for the record and make no claim about the missing S4.3.5 review. |
| **Any runtime/integration behaviour** | No engine, compiler or project (B-3). **0 of 67 acceptance cases run.** |

---

## 9. Overall verdict

# `PASS WITH CONDITIONS`

### Per-area findings, in the four categories the assignment asks for

| Area | Instrument correctness | Regression-test adequacy | Normative integrity | Reproducibility / provenance |
|---|---|---|---|---|
| **`DV-22`** | **PASS WITH CONDITIONS** — 2 escapes (`A`, `B`) | PASS — 10 cases, 0 false positives; coverage gaps named | PASS — unchanged | PASS — blobs pinned, clean-archive reproduced |
| **`DV-24`** | **PASS WITH CONDITIONS** — 1 escape (`C`) | PASS — 4 cases; `TD-53` covers the 2-line case only | PASS — unchanged | PASS |
| **`DV-11`** | **PASS** — no escape found in 8 probes | PASS WITH CONDITIONS — `TD-60` under-discriminates | PASS — unchanged | PASS |

### Why `PASS WITH CONDITIONS` and not `TARGETED REVISION`

The three escapes are **in one predicate's two constants and one loop bound**, plus one weak test.
They touch **no clause, no obligation, no ownership row, no count and no test specification**. The
contract is byte-identical. A revision does not need to reopen anything; it needs to finish one
predicate and tighten one test.

### Why not a clean `PASS`

`DV-22` is the instrument that certifies audio has exactly one owner. **Escape A is one word away
from a form the checker already handles**, and it reports a clean 27/27. I will not certify a check
as complete while a reachable counterexample passes it — that is the standard I applied to my own
`DV-11` result and to Agent 1's S4.3.5, and it does not change because the author got most of the fix
right.

### The single condition

> **C-1 (required) — `DV-22`.** All three of the following must produce `DV-22 FAIL`, and must be
> added as regression cases:
> 1. `The audio cues are the first agent's.` *(line 539 — teach `FORWARD_OWNER` the synonym, or
>    derive the possessive from `AGENT_REF` rather than re-spelling the literal)*
> 2. `Agent 1, unlike what the wargame community might generally assume about Agent 2, owns the audio
>    cues.` *(line 421 — bind the foil to the **reference** rather than a fixed character distance,
>    e.g. scan back to the segment boundary or the previous reference)*
> 3. `The tally reads 6 declared\nand then\n5 observed.` *(line 649 — `DV-24`; join a short run of
>    consecutive lines, not just pairs)*
>
> **Required closure evidence — the three-population test I specified at W-M2.16 and which Agent 1's
> existing corrections already pass:**
> - clean S4.3.6 document still scores **27/27 with 0 `DV-22` offenders** and the `DV-24` pair count
>   unchanged at 24;
> - all **86** existing cases still behave as required, and the suite total restated wherever it
>   appears;
> - the 13 valid-denial and 8 benign-co-occurrence probes in §3.5 still PASS, so recall is not bought
>   with precision.
>
> **Recommended, not required:** strengthen `TD-60` so it isolates the subset rule (MINOR-2), and add
> the `DV-22`/`DV-24`/`DV-27` breakdown of S4.2's 24/27 to the register (OBS-2).

**If C-1 is closed on that evidence I would move to `PASS` without re-reviewing the contract text.**
I would want to see only the changed predicate, the three new cases and the re-run suite.

---

## 10. Remaining blockers and recommended next action

### Blockers that are **not** mine to clear — all OPEN, unchanged

| ID | Blocker | Owner |
|---|---|---|
| **B-1** | TD-06 clock ownership / shared axis | TD |
| **B-2** | TD-09 parry authority; `TN-C-11` vs `TN-A-01`/`TN-A-02` **unresolved** | TD |
| **B-3** | No engine — **67 acceptance cases cannot run** | Phase 0 |
| **B-4** | TD-12 canonical MEAD / contract-layer owner | TD |
| **B-5** | U-07 global enumeration | OPEN |
| **B-13** | `AttackTag` ownership and registration | OPEN |

### Governance — unchanged and untouched by this review

C-05 `DESIGN_ONLY`, unsigned, unfrozen. U-07 **OPEN**. **0 of 67 acceptance cases executed**, all
`PROPOSED / NOT RUN`. No MEAD selected. No implementation authority. **The 86 regression cases are
tests of the checker, not of the contract, and I do not treat them as acceptance evidence.**

### Recommended next action

1. **Agent 1:** close **C-1** — three escapes, three new cases, three-population evidence.
2. **TD:** the blocking decisions are **TD-06, TD-09, TD-12 and B-13**, none of which any further
   validator revision can reach. **The instrument is close to done; the contract cannot be
   implemented until those are decided.**
3. **If Agent 3's S4.3.5 QA review exists outside this repository**, its `DV-24` and `DV-11` probes
   should be run against the corrected validator before either finding is called closed. **I could
   not test probes I have not seen, and I have not invented any.**

---

## 11. Provenance of this review

| Field | Value |
|---|---|
| Review ID | `TDD-A2-REVIEW-A1C05-S4-3-6-001` v1.0 |
| Branch | `arena/5dde91a4-tdd` |
| **Reviewed commit** | `034d091e1abcb507fdba6df4a05318a15aa5d7a1` |
| **Document blob** | `e3a1fa85243a4749591363d4196bb5d65dad7c84` |
| **Register blob** | `ce1ebc8d079f83aa594ef222ff71a108def1e8a6` |
| **Validator blob** | `840fed6730a5b2e18a5f717f98c6de273b9c8721` |
| **Suite blob** | `ee69f549a5c684c211a3dc15878c69c6dc32afe8` |
| Predecessor instruments | S4.3.5 validator `6927644f…`, suite `954588d3…` at `baa31db` |
| Prior Agent 2 artifacts | S4.1 review (`eee9401`) · Addendum (`e434dbe`) · S4.2 reassessment (`c8e9f2a`) · S4.3.5 architecture review (`659944b`) — **all preserved unmodified** |
| Test module | `Tools/world/tests/test_review_a1c05_s4_3_6.py` |
| Evidence | `Docs/evidence/agent2/W-M2.17_evidence.json` |
| Engine | **NONE** |
| Acceptance tests executed | **0 of 67** |

**What I did not do.** I did not edit or commit any Agent 1 file, publish a successor, change the
contract or validator, select a MEAD, freeze or sign C-05, close U-07, resolve `TN-C-11` or the
`TN-A` boundary, or authorise implementation. I did not reconstruct or attribute anything to Agent 3.
Every mutation described above was applied to a **copy** in `/tmp`; `034d091` is untouched.

**Pre-publication negative-existence re-check** (my standing rule): `git ls-remote` re-run
immediately before this report was committed; `arena/3bc206a0-tdd` still at `034d091`, blob still
`e3a1fa85`, and the named Agent 3 QA review still absent from all 77 reachable commits.

---

*End of review. `TDD-A2-REVIEW-A1C05-S4-3-6-001` v1.0. `PASS WITH CONDITIONS` — one condition, C-1,
confined to three escapes in two instrument predicates and one test.*
