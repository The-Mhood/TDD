#!/usr/bin/env python3
"""Regression tests for the two deny-by-default checks in dv_c05.py (DV-22, DV-24).

    python3 docs/validation/test_dv_c05_regressions.py
    python3 docs/validation/test_dv_c05_regressions.py --compare /path/to/older_dv_c05.py

Each case mutates a copy of the current C-05 document (or points at a predecessor blob)
and asserts the *verdict* of the named check. `--compare` runs the same cases against an
older validator as well, printing a before/after column: that is how the S4.3.1 correction
is demonstrated — the adversarial cases below FAIL against the S4.3 predicate and PASS
against the corrected one.

These are tests of the checker, not of the contract. They say nothing about contract
behaviour, and no acceptance test is executed by this file.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / 'docs/validation/dv_c05.py'
DOC = next((ROOT / f'docs/AGENT1_C05_CONTRACT_SUCCESSOR_{v}.md'
             for v in ('V4_3_2', 'V4_3_1', 'V4_3') if (ROOT / f'docs/AGENT1_C05_CONTRACT_SUCCESSOR_{v}.md').exists()),
            ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md')
PREDECESSORS = {
    'S4.3.1': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_1.md',
    'S4.3': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md',
    'S4.2': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md',
    'S4.1': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md',
    'S4.0': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md',
    'S3': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md',
}

BASE = DOC.read_text(encoding='utf-8')
TMP = pathlib.Path(tempfile.mkdtemp(prefix='dv_c05_regress_'))
COMPARE = None
if '--compare' in sys.argv:
    COMPARE = pathlib.Path(sys.argv[sys.argv.index('--compare') + 1]).resolve()
    assert COMPARE.exists(), COMPARE

# When comparing predicates, the injections are built from the *reviewed* S4.3 text, so the
# only variable between the two columns is the predicate itself. Without --compare-base the
# current document is used, exactly as in a normal run.
COMPARE_BASE = None
if '--compare-base' in sys.argv:
    COMPARE_BASE = pathlib.Path(sys.argv[sys.argv.index('--compare-base') + 1]).resolve()
    assert COMPARE_BASE.exists(), COMPARE_BASE
MUT = COMPARE_BASE.read_text(encoding='utf-8') if COMPARE_BASE else BASE

results, compared = [], []


def run(text_or_path, validator=VALIDATOR):
    """Run a validator; return (exit code, {check: (verdict, full line)})."""
    if isinstance(text_or_path, str) and text_or_path.endswith('.md') and pathlib.Path(text_or_path).exists():
        path = text_or_path
    else:
        name = 'case_%d.md' % len(compared + results)
        p = TMP / name
        p.write_text(text_or_path, encoding='utf-8')
        path = str(p)
    out = subprocess.run([sys.executable, str(validator), str(path)],
                         capture_output=True, text=True)
    verdicts = {}
    for line in out.stdout.split('\n'):
        m = re.match(r'(DV-\d+) (PASS|FAIL)', line)
        if m:
            verdicts[m.group(1)] = (m.group(2), line)
    return out.returncode, verdicts


def case(name, check, expect, text_or_path, note=''):
    code, verdicts = run(text_or_path)
    got = verdicts.get(check, ('MISSING', 'no line'))[0]
    ok = got == expect
    old = '-'
    if COMPARE:
        _c, old_verdicts = run(text_or_path, COMPARE)
        old = old_verdicts.get(check, ('MISSING', ''))[0]
        compared.append((name, check, old, got, expect))
        code, verdicts = run(text_or_path)
    results.append(ok)
    detail = verdicts.get(check, ('', ''))[1]
    print(f"{'PASS' if ok else 'FAIL'}  {name}"
          + (f"   [S4.3 predicate: {old} → corrected: {got}]" if COMPARE else '')
          + f"\n      {check} expected {expect}, got {got}{('  — ' + note) if note else ''}"
          f"\n      {detail[:170]}")


LIVE = '## 9. Shared read-surface and arbitration obligations'
QUIET = '## 10. Worked transitions'


def inject(line, anchor=LIVE):
    """Add an obligation-shaped line inside the live ownership area."""
    assert anchor in MUT
    return MUT.replace(anchor, line + '\n\n' + anchor, 1)


def inject_marked(line):
    """The same line, inside an authorised historical exemption, outside the live text."""
    block = '<!-- QUOTED-HISTORY-START -->\n' + line + '\n<!-- QUOTED-HISTORY-END -->\n\n' + QUIET
    return MUT.replace(QUIET, block, 1)


def inject_table(line):
    table = ('| Source [QUOTED] | Quoted defect as the review stated it |\n|---|---|\n| review | '
             + line + ' |\n\n' + QUIET)
    return MUT.replace(QUIET, table, 1)


# --------------------------------------------------------------------------- 0. baseline
print('== baseline ==')
case('the current document passes DV-22', 'DV-22', 'PASS', str(DOC))
case('the current document passes DV-24', 'DV-24', 'PASS', str(DOC))

# ------------------------------------ 1. S4.3.1: a negation may not launder a later assignment
print('\n== S4.3.1 — every assignment is evaluated separately (TD cases 1, 2, 5) ==')
case('TD-1  no audio, BUT owns audio cues — one clause, comma', 'DV-22', 'FAIL',
     inject('Agent 1 owns no audio, but Agent 1 owns audio cues for the player.'),
     'S4.3 read one negation per clause and passed this')
case('TD-2  no audio. Then owns audio cues — two sentences', 'DV-22', 'FAIL',
     inject('Agent 1 owns no audio. Agent 1 owns audio cues.'))
case('TD-5  three positive assignments, semicolons', 'DV-22', 'FAIL',
     inject('Agent 1 owns no audio; Agent 1 owns audio cues; Agent 1 owns audio banks.'))
case('TD-5b negation of another object does not cover audio', 'DV-22', 'FAIL',
     inject('Agent 1 owns no camera, but owns audio cues.'))
case('TD-5c negated responsibility, then a positive assignment joined by "and"', 'DV-22', 'FAIL',
     inject('Agent 1 has no C-05 audio responsibility and owns audio cues.'))
case('word order — passive attribution', 'DV-22', 'FAIL', inject('The audio cues are owned by Agent 1.'))
case('word order — possessive attribution', 'DV-22', 'FAIL', inject("Agent 1's audio cues drive the mixer."))
case('word order — colon attribution', 'DV-22', 'FAIL', inject('audio cue selection: Agent 1'))

# ------------------------------------------- 2. the pure negation must still pass (TD case 3)
print('\n== S4.3.1 — a genuine negation still passes (TD case 3) ==')
case('TD-3  "Agent 1 has no C-05 audio responsibility." alone', 'DV-22', 'PASS',
     inject('Agent 1 has no C-05 audio responsibility.'))
case('TD-3b "Agent 1 owns no audio cue of any kind." alone', 'DV-22', 'PASS',
     inject('Agent 1 owns no audio cue of any kind.'))

# ------------------------------- 3. historical quotation passes only inside an exemption (TD case 4)
print('\n== S4.3.1 — genuine history survives, but only by location (TD case 4) ==')
HIST = 'Agent 1 owns no audio, but Agent 1 owns audio cues for the player.'
case('TD-4a the contradictory text, unquoted, in live text', 'DV-22', 'FAIL', inject(HIST))
case('TD-4b the same text inside an authorised marked history block', 'DV-22', 'PASS', inject_marked(HIST))
case('TD-4c the same text inside a [QUOTED] review-disposition table', 'DV-22', 'PASS', inject_table(HIST))
case('TD-4d a [QUOTED] marker pasted into live §8/§9 text does not exempt it', 'DV-22', 'FAIL',
     inject('| a [QUOTED] | b |\n\n' + HIST))

# ------------------- 3b. S4.3.2: 'no <noun> audio' is not a denial of audio ownership
print('\n== S4.3.2 — only bounded denials count as negations (TD cases) ==')
case('TD-6  "has no problem owning audio cues"', 'DV-22', 'FAIL',
     inject('Agent 1 has no problem owning audio cues.'),
     'S4.3.1 read any "no ... audio" as a denial')
case('TD-7  "has no objection to owning audio cues"', 'DV-22', 'FAIL',
     inject('Agent 1 has no objection to owning audio cues.'))
case('TD-8  "has no restriction on owning audio cues"', 'DV-22', 'FAIL',
     inject('Agent 1 has no restriction on owning audio cues.'))
case('TD-9  "has no difficulty taking responsibility for audio cues"', 'DV-22', 'FAIL',
     inject('Agent 1 has no difficulty taking responsibility for audio cues.'))
case('TD-10 "no issue with owning" — same class, different noun', 'DV-22', 'FAIL',
     inject('Agent 1 has no issue with owning audio cues.'))
case('TD-11 a positive assertion following "no objection to owning"', 'DV-22', 'FAIL',
     inject('Agent 1 has no objection to owning audio cues, and Agent 1 owns audio cue selection.'))
case('TD-12 "has no C-05 audio responsibility" still passes', 'DV-22', 'PASS',
     inject('Agent 1 has no C-05 audio responsibility.'))
case('TD-13 "owns no audio cues" still passes', 'DV-22', 'PASS', inject('Agent 1 owns no audio cues.'))
case('TD-14 "has no responsibility for audio cue selection" still passes', 'DV-22', 'PASS',
     inject('Agent 1 has no responsibility for audio cue selection.'))
case('TD-15 "does not own any audio cues" passes (verbal denial)', 'DV-22', 'PASS',
     inject('Agent 1 does not own any audio cues.'))
case('TD-16 "is not responsible for audio cue selection" passes', 'DV-22', 'PASS',
     inject('Agent 1 is not responsible for audio cue selection.'))
case('TD-17 "has no ownership of audio cue selection" passes', 'DV-22', 'PASS',
     inject('Agent 1 has no ownership of audio cue selection.'))
case('TD-18 the same phrase inside an authorised historical block passes', 'DV-22', 'PASS',
     inject_marked('Reviewer wrote: Agent 1 has no objection to owning audio cues.'))

# ------------------- 3c. S4.3.3: a later denial cannot cancel an earlier positive assertion
print('\n== S4.3.3 — NEG_AFTER scope: a trailing denial answers only its own clause (TD cases) ==')
case('TD-19 "owns audio cues, but those cues are not assigned to Agent 1"', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues, but those cues are not assigned to Agent 1.'),
     'S4.3.2 read any post-mention denial as covering the mention')
case('TD-20 "owns audio, which is not a responsibility assigned to Agent 2"', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio, which is not a responsibility assigned to Agent 2.'))
case('TD-21 "owns audio cues and those cues are not owned by Agent 2"', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues and those cues are not owned by Agent 2.'))
case('TD-22 "owns audio cues which are not owned by anyone"', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues which are not owned by anyone.'))
case('TD-23 denial in the next sentence', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues. Audio is not owned by Agent 2.'))
case('TD-24 denial first, positive assertion second', 'DV-22', 'FAIL',
     inject('Audio is not owned by Agent 1. Agent 1 owns audio cues.'))
case('TD-25 semicolon-joined denial naming Agent 2', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues; audio is not owned by Agent 2.'))
case('TD-26 em-dash apposition, denial naming Agent 1', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues \u2014 a role that is not assigned to Agent 1.'))
case('TD-27 parenthesised denial naming Agent 2', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues (these are not owned by Agent 2).'))
case('TD-28 "Audio is not owned by Agent 1." still passes', 'DV-22', 'PASS',
     inject('Audio is not owned by Agent 1.'),
     'reversed clause order, genuine denial')
case('TD-29 "Audio is not a responsibility of Agent 1." still passes', 'DV-22', 'PASS',
     inject('Audio is not a responsibility of Agent 1.'))
case('TD-30 a genuine audio denial in a later clause still passes', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera; audio cues are not owned by Agent 1.'))

# ------------------- 3d. S4.3.4: an unnamed denial is not evidence of Agent 1's non-ownership
print('\n== S4.3.4 — unnamed and relative-clause denials (TD cases) ==')
case('TD-31 "owns audio cues that are not owned"', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues that are not owned.'),
     'S4.3.3 accepted any unnamed post-mention denial')
case('TD-32 positive assertion + unnamed denial in a relative clause', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues that are not claimed by the team.'))
case('TD-33 universal denial inside a "that" relative clause', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues that are not owned by anyone.'),
     'the relative clause is not the clause that carries the assertion')
case('TD-34 explicit denial naming Agent 1 still passes', 'DV-22', 'PASS',
     inject('Audio cues are not owned by Agent 1.'))
case('TD-35 genuine universal exclusion still passes', 'DV-22', 'PASS',
     inject('Agent 1 reported that audio cues are not owned by anyone.'),
     'nobody owns them, so the first agent does not')
case('TD-36 relative-clause denial naming another agent', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cues that are not assigned to Agent 2.'))
case('TD-37 a valid negative formulation still passes', 'DV-22', 'PASS',
     inject('Agent 1 has no authority over audio cue selection.'))
case('TD-38 a plain positive ownership violation still fails', 'DV-22', 'FAIL',
     inject('Agent 1 owns audio cue selection.'))
case('TD-39 the relative-clause form inside an authorised historical block passes', 'DV-22', 'PASS',
     inject_marked('Reviewer wrote: Agent 1 owns audio cues that are not owned.'))
case('TD-40 a universal denial that does not exclude Agent 1', 'DV-22', 'FAIL',
     inject('Audio cues are not owned by anyone and are owned by Agent 1.'))
case('TD-41 a universal denial beside a possessive ownership assertion', 'DV-22', 'FAIL',
     inject("Agent 1's audio cues are not owned by anyone."),
     'the possessive asserts the first agent owns them')

# ------------------------------------------------------- 4. N-1: the escape hatch is closed
print('\n== N-1 — DV-22, Agent 2\'s demonstrated injection ==')
INJ = 'Agent 1 owns the camera and audio cues for the player.'
case('bare injection is caught', 'DV-22', 'FAIL', inject(INJ))
case('keyword-prefixed injection is caught (the defect N-1 named)', 'DV-22', 'FAIL',
     inject('D-4 note: ' + INJ), 'S4.2 reported 0 offenders for exactly this line')
case('injection prefixed with a finding number and a heading word is caught', 'DV-22', 'FAIL',
     inject('§8 preamble, finding 1, row 5 also claimed: ' + INJ))

# ------------------------------------------------- 5. DV-24: the false negatives stay closed
print('\n== DV-24 — reproduced false negatives (probes P1, P2, P4, P5, P6) ==')
case('P1 wrong pair in prose outside the anchors is caught', 'DV-24', 'FAIL',
     MUT.replace(LIVE, 'The instrument reports 6 observed tokens against 7 declared.\n\n' + LIVE, 1))
case('P2 wrong pair in number words is caught', 'DV-24', 'FAIL',
     MUT.replace(LIVE, 'Seven declared, six observed.\n\n' + LIVE, 1))
_row6 = [l for l in MUT.split('\n') if l.startswith('| **6** |')][0]
case('P4 second contradictory pair on the anchor line is caught', 'DV-24', 'FAIL',
     MUT.replace(_row6, _row6.rstrip()[:-2] + ' Later drafts said 6 declared / 6 observed. |', 1))
case('P5 an anchor made wrong is caught (control)', 'DV-24', 'FAIL',
     MUT.replace(_row6, _row6.replace('7 declared, 5 observed', '6 declared, 5 observed', 1), 1))
case('P6 a dropped anchor is caught', 'DV-24', 'FAIL',
     MUT.replace(_row6, _row6.split('vs observed tokens separately')[0] + '| **D-6** | §5.4 |', 1))
case('a wrong historical count inside a marked block is exempt', 'DV-24', 'PASS',
     MUT.replace(QUIET, '<!-- QUOTED-HISTORY-START -->\nS4 said 7 declared, 6 observed.\n'
                         '<!-- QUOTED-HISTORY-END -->\n\n' + QUIET, 1))

# ------------------------------ 5b. S4.3.6: the attributed dialects (Agent 2's MAJOR-1)
print('\n== S4.3.6 — DV-22 attribution: the synonym and the contrastive foil (Agent 2 cases) ==')
case('TD-42 "Agent 1, unlike Agent 2, owns the audio cues"', 'DV-22', 'FAIL',
     inject('Agent 1, unlike Agent 2, owns the audio cues.'),
     'Agent 2 MAJOR-1, verbatim: the nearest reference was the foil')
case('TD-43 "The first agent owns the audio cues"', 'DV-22', 'FAIL',
     inject('The first agent owns the audio cues.'),
     'Agent 2 MAJOR-1, verbatim: the document\'s own synonym for Agent 1')
case('TD-44 "as opposed to"', 'DV-22', 'FAIL',
     inject('Agent 1, as opposed to Agent 2, owns the audio cues.'))
case('TD-45 "rather than"', 'DV-22', 'FAIL',
     inject('Agent 1 rather than Agent 2 owns the audio cues.'))
case('TD-46 "but not"', 'DV-22', 'FAIL',
     inject('Agent 1 but not Agent 2 owns the audio cues.'))
case('TD-47 a foil naming the first agent leaves Agent 2 the subject', 'DV-22', 'PASS',
     inject('Agent 2, unlike Agent 1, owns the audio cues.'),
     'the mention is Agent 2\'s; dropping it would be a false positive')
case('TD-48 "Agent 1, unlike Agent 2, owns no audio cues"', 'DV-22', 'PASS',
     inject('Agent 1, unlike Agent 2, owns no audio cues.'))
case('TD-49 "The first agent has no C-05 audio responsibility"', 'DV-22', 'PASS',
     inject('The first agent has no C-05 audio responsibility.'))
case('TD-50 object negation after the synonym ("not the audio cues")', 'DV-22', 'PASS',
     inject('The first agent owns the camera, not the audio cues.'),
     'found when the synonym became attributable: a genuine denial that must not fail')
case('TD-51 "whereas" is a clause, not a foil', 'DV-22', 'FAIL',
     inject('Agent 2 does not own them, whereas Agent 1 owns the audio cues.'),
     'measured deviation from Agent 2\'s recipe: dropping this reference loses a true positive')

# ------------------- 5c. S4.3.6: DV-24 forms that reached the prose without reaching the check
print('\n== S4.3.6 — DV-24: label-first, sentence-split and line-wrapped pairs ==')


def replace_in_doc(old, new):
    assert old in BASE, old[:60]
    return BASE.replace(old, new, 1)


case('TD-52 "declared: 6, observed: 5" — punctuation after the label', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: declared: 6, observed: 5.\n\n' + LIVE))
case('TD-53 the pair wrapped across a line break', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nand 5 observed.\n\n' + LIVE))
case('TD-54 the pair split by a sentence break', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'It said 6 declared. Then 5 observed.\n\n' + LIVE))
case('TD-55 the correct pair in the same forms still passes (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, 'Counts: declared: 7, observed: 5. Also 7 declared\nand 5 observed.\n\n' + LIVE))

# ---------------------------------- 5d. S4.3.6: DV-11 gaps (declaration parse, subset, counts)
print('\n== S4.3.6 — DV-11: declaration parse, subset rule and hand cell counts ==')
_ROW_PO = '| `producer owner` | Agent 2 on enemy producers; Agent 1 on the player producer | **row 2** (inside C-05: producer implementation) |'
_CNT_PO = '| **23 cells** (19 `TN-P`, 4 `TN-R`) |'
case('TD-56 a token declaring an extra disallowed row is caught', 'DV-11', 'FAIL',
     replace_in_doc(_ROW_PO, '| `producer owner` | Agent 2 on enemy producers; Agent 1 on the player producer | **rows 2 and 5** (inside C-05: producer implementation) |'),
     'an intersection test passed this on the strength of row 2 alone')
case('TD-57 a token declaring a disallowed range is caught', 'DV-11', 'FAIL',
     replace_in_doc(_ROW_PO, '| `producer owner` | Agent 2 on enemy producers; Agent 1 on the player producer | **rows 2–5** (inside C-05: producer implementation) |'))
case('TD-58 the §5.4 hand cell count is compared with the instrument', 'DV-11', 'FAIL',
     replace_in_doc(_CNT_PO, '| **22 cells** (19 `TN-P`, 3 `TN-R`) |'),
     "Agent 2's D-6b class: a hand-restated count drifting from the computed one")
case('TD-59 the unmodified §5.4 table still passes (control)', 'DV-11', 'PASS', str(DOC))
_ROW_C5 = '| `Agent 2, C-05 consumer` | Agent 2 | **row 6** (inside C-05: consumer integration) |'
case('TD-60 a row whose owner is the wrong agent is caught (the owner clause)', 'DV-11', 'FAIL',
     replace_in_doc(_ROW_C5, '| `Agent 2, C-05 consumer` | Agent 2 | **row 7** (outside C-05: placement, assets, tuning) |'),
     "row 7's owner is Agent 2 but outside C-05; the TN-C cells may only use rows 5-6")

# --------------- 5e. S4.3.7: DV-22 — the possessor synonym and the foil that outgrew a window
print('\n== S4.3.7 — DV-22: the synonym as possessor, and a foil longer than the old window ==')
case('TD-61 the possessive synonym (Agent 2 MAJOR-1)', 'DV-22', 'FAIL',
     inject("The audio cues are the first agent's."),
     "MAJOR-1 verbatim: AGENT_REF learned the synonym, FORWARD_OWNER still spelled the literal")
case('TD-62 a foil carrying a subordinate clause (Agent 2 MAJOR-2)', 'DV-22', 'FAIL',
     inject('Agent 1, unlike what the wargame community might generally assume about Agent 2, '
            'owns the audio cues.'),
     'MAJOR-2 verbatim: the marker fell outside the fixed 32-character window and the foil '
     'became the subject again')
case('TD-63 "belongs to" the synonym', 'DV-22', 'FAIL',
     inject('The audio cues belong to the first agent.'),
     'the class MAJOR-1 belongs to: a positive-ownership form taught to no attribution path')
case("TD-64 the cue's owner is the synonym", 'DV-22', 'FAIL',
     inject("The audio cue's owner is the first agent."))
case('TD-65 dash attribution to the synonym', 'DV-22', 'FAIL',
     inject('The audio cues -- the first agent.'))
case('TD-66 "do not belong to" is a denial, not an assignment (control)', 'DV-22', 'PASS',
     inject('The audio cues do not belong to the first agent.'),
     'the false positive the "belongs to" widening created before its denial was taught')
case('TD-67 the mention is the contrasted object, not the owned thing (control)', 'DV-22', 'PASS',
     inject('The camera, rather than the audio cues, is owned by Agent 1.'),
     'a contrast marker governs the mention only when it stands directly before it')
case('TD-68 a marker in the previous clause does not drop the subject (control)', 'DV-22', 'PASS',
     inject('Unlike the earlier draft, Agent 1 owns the camera.'),
     'clause-bounded foil detection must not discard a genuine subject')
case('TD-69 a short foil still fails (control)', 'DV-22', 'FAIL',
     inject('Agent 1, unlike Agent 2, owns the audio cues.'))
case('TD-70 the possessive denial is still accepted (control)', 'DV-22', 'PASS',
     inject("The audio cues are not the first agent's."),
     'teaching the possessor the synonym must not make its denial an assignment')

# ------------- 5f. S4.3.7: DV-24 — a three-line wrap, and the false joins that closing it risks
print('\n== S4.3.7 — DV-24: three-line wraps, with the false-join controls ==')
case('TD-71 the pair wrapped across three lines (Agent 2 MINOR-1 / the same class)', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nand then\n5 observed.\n\n' + LIVE),
     'joining only adjacent lines left this unassembled')
case('TD-72 a three-line wrap with an intervening continuation', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nin the audit\nand 5 observed.\n\n' + LIVE))
case('TD-73 the correct pair across three lines (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, 'Counts: 7 declared\nand then\n5 observed.\n\n' + LIVE))
case('TD-74 unrelated adjacent facts are not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, 'The camera pass declared 6 priorities.\nThe instrument observed 5 events.\n\n' + LIVE),
     'a sentence terminator ends a claim; a wrap does not cross one')
case('TD-75 a list boundary is not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, '- declared 6\n- observed 5\n\n' + LIVE),
     'block structure is a hard boundary for the join')
case('TD-76 two separate single-sided facts are not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, 'Line one declared 7 in full.\nLine two observed 5 in full.\n\n' + LIVE))

# ------------------- 5g. S4.3.7: DV-11 — the owner clause, enforced directly and not by accident
print('\n== S4.3.7 — DV-11: the owner-column clause, enforced as its own rule ==')
case('TD-77 the owner clause is violated with the allowed-row rule satisfied (the discriminator)',
     'DV-11', 'FAIL',
     replace_in_doc(_ROW_C5, '| `Agent 2, C-05 consumer` | Agent 2 | **row 5** (inside C-05: consumer integration) |'),
     'row 5 is inside TN-C\'s {5, 6}, so the subset rule passes; only ownership fails. '
     'Under the S4.3.6 validator this document PASSES, which is what makes it a discriminator')
case('TD-78 correct owner-column evidence: the unmodified table (control)', 'DV-11', 'PASS', str(DOC))
case('TD-79 a dual-owned row stays legal for Agent 1 (control)', 'DV-11', 'PASS',
     replace_in_doc('| `Agent 1, shared support` | Agent 1 | **row 4** |',
                    '| `Agent 1, shared support` | Agent 1 | **row 2** |'),
     'row 2 is owned by both agents and is inside TN-R\'s {2, 4}: the owner rule must not reject it')
case('TD-80 the allowed-row rule still fires on its own (row 7)', 'DV-11', 'FAIL',
     replace_in_doc(_ROW_C5, '| `Agent 2, C-05 consumer` | Agent 2 | **row 7** (outside C-05: placement, assets, tuning) |'),
     'TD-60 restated: row 7 fails the *allowed-row* rule under both validators, so it never '
     'isolated ownership — that is what TD-77 adds')

# ------- 5h. S4.3.8: the quantified denial (DV-22) and the capitalised continuation (DV-24)
print('\n== S4.3.8 — DV-22 quantified denial, and DV-24 two-line capitalised continuations ==')
case('TD-81 "No audio cue belongs to Agent 1" is not an assignment', 'DV-22', 'PASS',
     inject('No audio cue belongs to Agent 1.'),
     "Agent 2 CONDITION-1 verbatim: a determiner-quantified subject denies possession "
     "without negating the verb, so the 'belongs to' widening read it as ownership")
case('TD-82 "There is no audio cue that belongs to the first agent"', 'DV-22', 'PASS',
     inject('There is no audio cue that belongs to the first agent.'))
case('TD-83 "None of the audio cues belong to the first agent"', 'DV-22', 'PASS',
     inject('None of the audio cues belong to the first agent.'))
case('TD-84 a genuine "belongs to" assignment is still caught (control)', 'DV-22', 'FAIL',
     inject('The audio cues belong to the first agent.'),
     'the denial must not be bought by weakening the positive form')
case('TD-85 "No audio cue is owned by Agent 1" (same quantified family)', 'DV-22', 'PASS',
     inject('No audio cue is owned by Agent 1.'),
     'the same determiner-quantifier gap with the other possession predicates')
case('TD-86 the confirmed two-line capitalised wrap (Agent 2 CONDITION-2)', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nThe audit shows 5 observed.\n\n' + LIVE),
     'the confirmed Counts example: S4.3.7 gated two-line windows on a lowercase continuation '
     'and accepted it')
case('TD-87 a two-line wrap continued by "Then"', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nThen 5 observed.\n\n' + LIVE))
case('TD-88 a two-line wrap continued by "And"', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nAnd 5 observed.\n\n' + LIVE))
case('TD-89 a lowercase two-line wrap still fails (control)', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nand 5 observed.\n\n' + LIVE))
case('TD-90 a heading boundary is still not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, '# Heading declared 6\nThe row observed 5\n\n' + LIVE))
case('TD-91 a blockquote boundary is still not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, '> quote declared 6\n> quote observed 5\n\n' + LIVE))
case('TD-92 a table-row boundary is still not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, '| a declared 6\n| a observed 5\n\n' + LIVE))
case('TD-93 a fence boundary is still not joined (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, '```\ndeclared 6\nobserved 5\n```\n\n' + LIVE))
case('TD-94 the correct pair across a capitalised wrap passes (control)', 'DV-24', 'PASS',
     replace_in_doc(LIVE, 'Counts: 7 declared\nThe audit shows 5 observed.\n\n' + LIVE),
     'removing the continuation gate must not make a correct restatement fail')

# ------- 5i. S4.3.9: the quantified denial may not reach its verb across a clause boundary
print('\n== S4.3.9 — DV-22 quantified denial is confined to its own clause ==')
case('TD-95 Agent 2 F-1 verbatim: denial + "and" + contradicting ownership', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2 and the audio cue belongs to Agent 1.'),
     "S4.3.8's gap crossed the conjunction, so a line asserting Agent 1's ownership was "
     "excused by a denial that speaks about Agent 2 — the exact reproduced fail-open")
case('TD-96 denial + comma + "but" + contradicting ownership', 'DV-22', 'FAIL',
     inject('No audio cue is provided for Agent 2, but the audio cue belongs to Agent 1.'),
     'the second reproduced form')
case('TD-97 the same fail-open with "is owned by"', 'DV-22', 'FAIL',
     inject('No audio cue is provided for Agent 2 and the audio cue is owned by Agent 1.'),
     'the other possession predicate the quantified family covers')
case('TD-98 the same fail-open with the possessive predicate', 'DV-22', 'FAIL',
     inject("No audio cue is assigned to Agent 2 and the audio cue is Agent 1's."))
case('TD-99 the same fail-open naming the first agent by synonym', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2 and the audio cue belongs to the first agent.'))
case('TD-100 a positive ownership statement in the same shape is still caught (control)',
     'DV-22', 'FAIL',
     inject('The audio cue belongs to Agent 1.'),
     'the correction must not buy the denial by weakening the positive form')
case('TD-101 a restriction inside the quantified clause is still a denial (control)',
     'DV-22', 'PASS',
     inject('No audio cue in the shared read-surface registry belongs to Agent 1.'),
     'the gap still spans a clause-internal modifier: narrowing must not over-reject')
case('TD-102 semicolon-joined contradicting ownership (control)', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2; the audio cue belongs to Agent 1.'),
     "';' was already excluded in S4.3.8; this control isolates the gap class")
case('TD-103 sentence-joined contradicting ownership (control)', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2. The audio cue belongs to Agent 1.'))

# ------- 5j. S4.3.10: a bare comma is not a negation (Agent 2 F-1b, TD-authorised)
print('\n== S4.3.10 — the object negation must be stated, so a comma splice cannot excuse ownership ==')
case('TD-104 Agent 2 F-1b verbatim: comma splice, no negator anywhere', 'DV-22', 'FAIL',
     inject('No audio cue is provided for Agent 2, the audio cue belongs to Agent 1.'),
     "the S4.3.6 object-negation construction matched ', the audio' on its own and negated the "
     "object of a clause that asserts Agent 1's ownership; the comma alternative is gone")
case('TD-105 the same splice with "is owned by"', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2, the audio cue is owned by Agent 1.'))
case('TD-106 the same splice with the possessive predicate', 'DV-22', 'FAIL',
     inject("No audio cue is provided for Agent 2, the audio cue is Agent 1's."))
case('TD-107 the same splice naming the first agent by synonym', 'DV-22', 'FAIL',
     inject('No audio cue is provided for Agent 2, the audio cue belongs to the first agent.'))
case('TD-108 a comma-joined object list is an assertion, not a denial', 'DV-22', 'FAIL',
     inject('Agent 1 owns the camera, the audio cues.'),
     'the comma alone used to negate the second object')
case('TD-109 the legitimate object negation after the synonym still passes', 'DV-22', 'PASS',
     inject('The first agent owns the camera, not the audio cues.'),
     "TD-50's form: the negation is stated, so the mention is the object of it")
case('TD-110 the legitimate object negation naming Agent 1 still passes', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera, not the audio cues.'))
case('TD-111 the object negation with "any" still passes', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera, not any audio cues.'))
case('TD-112 the object negation after a longer object list still passes', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera and the montage, not the audio cues.'))
case('TD-113 "but not the audio cues" still passes', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera, but not the audio cues.'),
     'the negator may follow a conjunction: what the rule requires is the negator, not the comma')
case('TD-114 a positive ownership statement is still caught (control)', 'DV-22', 'FAIL',
     inject('The audio cue belongs to Agent 1.'),
     'the correction must not buy the denial by weakening the positive form')
case('TD-115 a positive and-list is still caught (control)', 'DV-22', 'FAIL',
     inject('Agent 1 owns the camera and audio cues for the player.'))
case('TD-116 the S4.3.9 F-1 case is still caught (control)', 'DV-22', 'FAIL',
     inject('No audio cue is assigned to Agent 2 and the audio cue belongs to Agent 1.'),
     'closing F-1b must not reopen the F-1 fail-open')
case('TD-117 the F-1 comma + "but" case is still caught (control)', 'DV-22', 'FAIL',
     inject('No audio cue is provided for Agent 2, but the audio cue belongs to Agent 1.'))
case('TD-118 CONDITION-1 control: the quantified denial still passes', 'DV-22', 'PASS',
     inject('No audio cue belongs to Agent 1.'))
case('TD-119 CONDITION-2 control: a capitalised two-line wrap still fails', 'DV-24', 'FAIL',
     replace_in_doc(LIVE, 'Counts: 6 declared\nThe audit shows 5 observed.\n\n' + LIVE))
NEWEST = ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10.md'
assert NEWEST.exists(), NEWEST
case('TD-120 the current document still passes DV-22 (MINOR-1 class)', 'DV-22', 'PASS',
     str(NEWEST),
     'MINOR-1 was a hand-restated figure drifting from its runner: the published text is '
     're-checked here, so a stale count cannot pass unnoticed')
case('TD-121 the current document still passes DV-24 (MINOR-1 class)', 'DV-24', 'PASS',
     str(NEWEST))

# ------- 5k. S4.3.11: D-a (the `never` object negation) and D-b (the passive auxiliary chain)
print('\n== S4.3.11 — D-a and D-b: the negator set and the passive chain (TD-authorised A+D) ==')
case('TD-122 Agent 2 R-1: a "never" object negation is not an assignment (D-a)', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera, never the audio cues.'),
     "a true denial the literal 'not' could not read; TN-C-15 gives audio to Agent 2 alone, so "
     'rejecting this sentence rejected the contract\'s own position')
case('TD-123 R-1b: "never any"', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera, never any audio cues.'))
case('TD-124 R-1c: "never" with no comma at all', 'DV-22', 'PASS',
     inject('Agent 1 owns the camera never the audio cues.'),
     'no comma is involved: the negator word is the mechanism, not the punctuation')
case('TD-125 Agent 2 R-3b: the perfect passive is attributed (D-b)', 'DV-22', 'FAIL',
     inject('The audio cues have been owned by Agent 1.'),
     'FORWARD_OWNER required is|are|was|were before the participle, so the auxiliary chain was invisible')
case('TD-126 D-b: the same with "had been"', 'DV-22', 'FAIL',
     inject('The audio cues had been owned by Agent 1.'))
case('TD-127 Agent 2 R-5: an appositive participle with no copula', 'DV-22', 'FAIL',
     inject('The audio cue, supplied by Agent 1, drives the mixer.'))
case('TD-128 R-5b: the same attribution with no commas', 'DV-22', 'FAIL',
     inject('The audio cue supplied by Agent 1 drives the mixer.'),
     "the comma plays no part: the missing copula does, which is why R-5 and R-3b are one family")
case('TD-129 R-5c: the same with "provided"', 'DV-22', 'FAIL',
     inject('The audio cue, provided by Agent 1, drives the mixer.'))
case('TD-130 D-b guard: a negated passive is not an assignment', 'DV-22', 'PASS',
     inject('The audio cues are not provided by Agent 1.'),
     "making the copula optional without this guard reads 'not provided by Agent 1' as ownership")
case('TD-131 D-b guard: "have never been owned by"', 'DV-22', 'PASS',
     inject('The audio cues have never been owned by Agent 1.'))
case('TD-132 D-b denial side: "No audio cue has been owned by Agent 1"', 'DV-22', 'PASS',
     inject('No audio cue has been owned by Agent 1.'),
     'the widened attribution needs its denial to read the same chain')
case('TD-133 D-b denial side: "None of the audio cues have been owned by"', 'DV-22', 'PASS',
     inject('None of the audio cues have been owned by Agent 1.'))
case('TD-134 D-b guard is narrow: a later positive assignment still fails', 'DV-22', 'FAIL',
     inject('Audio cues are not owned by anyone and are owned by Agent 1.'),
     'the guard must not stop the attribution reading a later clause (TD-40\'s shape)')
case('TD-135 D-b control: the copula form is unchanged', 'DV-22', 'FAIL',
     inject('The audio cue is supplied by Agent 1.'))
case('TD-136 D-b control: attribution to Agent 2 is still not an offence', 'DV-22', 'PASS',
     inject('The audio cues have been owned by Agent 2.'))
case('TD-137 R-4 DEFERRED (D-c): the appositive "not" foil is still missed', 'DV-22', 'PASS',
     inject('Agent 1, not Agent 2, owns the audio cues.'),
     'Agent 2 measured that the one-line fix to _FOIL_ANY re-opens "Not only does Agent 1 own the '
     'audio cues" and collides with D-b; this case pins today\'s verdict so a later cycle must move '
     'it deliberately, and marks it as a known open defect rather than a requirement')
case('TD-138 R-4b DEFERRED (D-c): the appositive "never" foil is still missed', 'DV-22', 'PASS',
     inject('Agent 1, never Agent 2, owns the audio cues.'))

# ------------------------------------------------------------- 6. the predecessors still fail# ------------------------------------------------------------- 6. the predecessors still fail
print('\n== predecessors — the checks still fail where the defects were ==')
for label, check, expect in (('S4.3.1', 'DV-22', 'PASS'), ('S4.3', 'DV-22', 'PASS'), ('S4.2', 'DV-22', 'FAIL'),
                             ('S4.1', 'DV-22', 'FAIL'), ('S3', 'DV-22', 'FAIL'),
                             ('S4.0', 'DV-24', 'FAIL')):
    path = PREDECESSORS[label]
    if path.exists():
        case(f'{label} on {check}', check, expect, str(path))
    else:
        print(f'SKIP  {label} not present at {path}')

if COMPARE:
    print(f'\n== before/after against {COMPARE.name} ==')
    print(f"{'case':60s} {'S4.3':>6s} {'S4.3.1':>7s} {'required':>9s}")
    for name, check, old, new, expect in compared:
        flag = '' if new == expect else '   <-- corrected predicate still wrong'
        print(f'{name[:60]:60s} {old:>6s} {new:>7s} {expect:>9s}{flag}')

print('\n' + f'{sum(results)}/{len(results)} regression cases behaved as required')
sys.exit(0 if all(results) else 1)
