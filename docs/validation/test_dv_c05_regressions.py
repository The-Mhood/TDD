#!/usr/bin/env python3
"""Regression tests for the two deny-by-default checks in dv_c05.py (DV-22, DV-24).

    python3 docs/validation/test_dv_c05_regressions.py

Each case mutates a copy of the current C-05 document (or points at a predecessor blob)
and asserts the *verdict* of the named check. This is the evidence for the two closures
S4.3 claims:

  N-1   Agent 2's keyword-prefixed injection must not survive. A line that assigns audio
        to the first agent is an offender whether or not it mentions a finding number.
  DV-24 A wrong declared/observed count must not survive in prose, in number words, or as
        a second pair on an anchor line — and a legitimate historical quotation must.

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
DOC = ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3.md'
PREDECESSORS = {
    'S4.2': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md',
    'S4.1': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_1.md',
    'S4.0': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4.md',
    'S3': ROOT / 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V3.md',
}

BASE = DOC.read_text(encoding='utf-8')
TMP = pathlib.Path(tempfile.mkdtemp(prefix='dv_c05_regress_'))
results = []


def run(text_or_path):
    """Run the validator; return (exit code, {check: line})."""
    if isinstance(text_or_path, str) and text_or_path.endswith('.md') and pathlib.Path(text_or_path).exists():
        path = text_or_path
    else:
        p = TMP / 'case.md'
        p.write_text(text_or_path, encoding='utf-8')
        path = str(p)
    out = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
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
    results.append(ok)
    detail = verdicts.get(check, ('', ''))[1]
    print(f"{'PASS' if ok else 'FAIL'}  {name}\n      {check} expected {expect}, got {got}"
          f"{('  — ' + note) if note else ''}\n      {detail[:180]}")


def with_injection(line, before='## 9. Shared read-surface and arbitration obligations'):
    """Insert an extra obligation-shaped line inside the live ownership section (§8/§9)."""
    assert before in BASE
    return BASE.replace(before, line + '\n\n' + before, 1)


# The exemption cases are placed OUTSIDE the live ownership sections, because the check
# deliberately refuses to let those sections be exempted at all.
QUIET = '## 10. Worked transitions'


def with_marked(line):
    block = '<!-- QUOTED-HISTORY-START -->\n' + line + '\n<!-- QUOTED-HISTORY-END -->\n\n' + QUIET
    return BASE.replace(QUIET, block, 1)


def with_quoted_table(line):
    table = ('| Source [QUOTED] | Quoted defect as the review stated it |\n|---|---|\n| review | ' + line
             + ' |\n\n' + QUIET)
    return BASE.replace(QUIET, table, 1)


# --------------------------------------------------------------------------- 0. baseline
print('== baseline ==')
case('current document passes DV-22', 'DV-22', 'PASS', str(DOC))
case('current document passes DV-24', 'DV-24', 'PASS', str(DOC))

# ------------------------------------------------------- 1. N-1: the escape hatch is closed
print('\n== N-1 — DV-22, Agent 2\'s demonstrated injection ==')
INJ = 'Agent 1 owns the camera and audio cues for the player.'
case('bare injection is caught', 'DV-22', 'FAIL', with_injection(INJ))
case('keyword-prefixed injection is caught (this is the defect N-1 named)',
     'DV-22', 'FAIL', with_injection('D-4 note: ' + INJ),
     'S4.2 reported 0 offenders for exactly this line')
case('injection prefixed with a finding number and a heading word is caught',
     'DV-22', 'FAIL', with_injection('§8 preamble, finding 1, row 5 also claimed: ' + INJ))
case('injection inside a marked history block is exempt (narrow exemption still works)',
     'DV-22', 'PASS', with_marked('Reviewer wrote: ' + INJ))
case('injection inside a [QUOTED] table is exempt (narrow exemption still works)',
     'DV-22', 'PASS', with_quoted_table(INJ))
case('a [QUOTED] marker inside live §8 text does not exempt it',
     'DV-22', 'FAIL',
     with_injection('| a [QUOTED] | b |\n\nAgent 1 owns the camera and audio cues for the player.'))

# ------------------------------------------------- 2. DV-24: the false negatives are closed
print('\n== DV-24 — reproduced false negatives (probes P1, P2, P4, P5) ==')
case('P1 wrong pair in prose outside the anchors is caught', 'DV-24', 'FAIL',
     BASE.replace('## 9. Shared read-surface', 'The instrument reports 6 observed tokens against 7 declared.\n\n## 9. Shared read-surface', 1))
case('P2 wrong pair in number words is caught', 'DV-24', 'FAIL',
     BASE.replace('## 9. Shared read-surface', 'Seven declared, six observed.\n\n## 9. Shared read-surface', 1))
_row6 = [l for l in BASE.split('\n') if l.startswith('| **6** |')][0]
case('P4 second contradictory pair on the anchor line is caught', 'DV-24', 'FAIL',
     BASE.replace(_row6, _row6.rstrip()[:-2] + ' Later drafts said 6 declared / 6 observed. |', 1))
case('P5 an anchor made wrong is caught (control on the old behaviour)', 'DV-24', 'FAIL',
     BASE.replace(_row6, _row6.replace('7 declared, 5 observed', '6 declared, 5 observed', 1), 1))
case('P6 a dropped anchor is caught', 'DV-24', 'FAIL',
     BASE.replace(_row6, _row6.split('vs observed tokens separately')[0] + '| **D-6** | §5.4 |', 1))
case('a wrong historical count inside a marked block is exempt', 'DV-24', 'PASS',
     BASE.replace('## 9. Shared read-surface', '<!-- QUOTED-HISTORY-START -->\nS4 said 7 declared, 6 observed.\n<!-- QUOTED-HISTORY-END -->\n\n## 9. Shared read-surface', 1))

# ------------------------------------------------------------- 3. the predecessors still fail
print('\n== predecessors — the checks still fail where the defects were ==')
for label, check, expect in (('S4.1', 'DV-22', 'FAIL'), ('S3', 'DV-22', 'FAIL'),
                             ('S4.0', 'DV-24', 'FAIL'), ('S4.2', 'DV-22', 'FAIL')):
    path = PREDECESSORS[label]
    if path.exists():
        case(f'{label} on {check}', check, expect, str(path),
             'S4.2 fails the rewritten scan because S4.2 carries no exemption markers; '
             'its historical rows are marked only here' if label == 'S4.2' else '')
    else:
        print(f'SKIP  {label} not present at {path}')

print('\n' + f"{sum(results)}/{len(results)} regression cases behaved as required")
sys.exit(0 if all(results) else 1)
