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

# ------------------------------------------------------------- 6. the predecessors still fail
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
