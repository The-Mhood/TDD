#!/usr/bin/env python3
"""C-05 document validator — 27 text checks over a C-05 successor document (v4.3).

    python3 docs/validation/dv_c05.py <path-to-document.md>

Prints one line per check and a final tally; exit 0 iff all checks pass.

These are checks on *document text*. They are not acceptance tests, they say nothing
about contract behaviour, and passing them is not evidence that any obligation holds.
Several of them are deliberately able to FAIL: each is shown failing on an earlier
blob in the document's §13.3 before it is shown passing on the current one.

DV-22 and DV-24 are deny-by-default as of v4.3. They no longer decide whether a line is
"about a finding" by looking for finding numbers: the only exemptions are *regions*
(fenced blocks, tables whose header carries [QUOTED], and QUOTED-HISTORY blocks). If a
line states an audio assignment, or a declared/observed pair, outside an exempt region, it
is a defect. See docs/validation/test_dv_c05_regressions.py for the negative tests.
"""
import hashlib
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_2.md'
s = open(path, encoding='utf-8').read()
lines = s.split('\n')
results, shown = [], []


def section(start, end=None):
    if start not in s:
        return ''
    i = s.index(start)
    j = s.index(end, i) if end and end in s[i:] else len(s)
    return s[i:j]


def table_rows(block):
    out = []
    for ln in block.split('\n'):
        t = ln.strip()
        if t.startswith('|') and t.endswith('|'):
            c = [x.strip() for x in t.strip('|').split('|')]
            if set(''.join(c)) <= set('-: '):
                continue
            out.append(c)
    return out


def check(cid, ok, detail):
    results.append((cid, ok, detail))
    shown.append(f"{cid} {'PASS' if ok else 'FAIL'} — {detail}")


S7 = section('## 7. Producer obligations', '## 8. Consumer obligations')
S8 = section('## 8. Consumer obligations', '## 9. Shared read-surface')
S9 = section('## 9. Shared read-surface', '## 10. Worked transitions')


def obl_rows():
    rows = []
    for blk in (S7, S8, S9):
        for c in table_rows(blk):
            if c and c[0].startswith('**TN-'):
                rows.append(c)
    return rows


ALL = obl_rows()


QUOTED_TABLE_TOKEN = '[QUOTED]'
QSTART, QEND = 'QUOTED-HISTORY-START', 'QUOTED-HISTORY-END'


def exempt_mask(ls):
    """Return (mask, counts). A line is exempt only by *location*:

      1. inside a fenced code block;
      2. inside a table whose header row carries the token [QUOTED];
      3. inside a <!-- QUOTED-HISTORY-START --> ... <!-- QUOTED-HISTORY-END --> block.

    Exemption is never a function of the words on the line. That is the N-1 correction:
    an author who mentions a finding number on the same line as a defect can no longer
    disable a check for that line.
    """
    mask = [False] * len(ls)
    counts = {'fenced': 0, 'quoted_table': 0, 'marked_block': 0}
    fence = False
    for i, ln in enumerate(ls):
        if ln.strip().startswith('```'):
            mask[i] = True
            counts['fenced'] += 1
            fence = not fence
            continue
        if fence:
            mask[i] = True
            counts['fenced'] += 1
    in_block = False
    for i, ln in enumerate(ls):
        # a marker only counts on a line of its own; a *mention* of the marker inside a
        # sentence (this document mentions it in §0.7 and §13.1) must not open a region.
        if ln.strip().startswith('<!--') and QSTART in ln:
            in_block = True
            mask[i] = True
            counts['marked_block'] += 1
            continue
        if ln.strip().startswith('<!--') and QEND in ln:
            mask[i] = True
            counts['marked_block'] += 1
            in_block = False
            continue
        if in_block:
            mask[i] = True
            counts['marked_block'] += 1
    i = 0
    while i < len(ls):
        if ls[i].lstrip().startswith('|') and QUOTED_TABLE_TOKEN in ls[i]:
            j = i
            while j < len(ls) and ls[j].lstrip().startswith('|'):
                mask[j] = True
                counts['quoted_table'] += 1
                j += 1
            i = j
        else:
            i += 1
    return mask, counts


def cells(prefix):
    return [r for r in ALL if r[0].strip('*').startswith(prefix)]


def req(oid):
    for r in ALL:
        if r[0].strip('*') == oid:
            return r[1]
    return ''


def imp(oid):
    for r in ALL:
        if r[0].strip('*') == oid:
            return r[6]
    return ''


# ---------------------------------------------------------------- DV-1
declared = {'TN-P': 19, 'TN-C': 15, 'TN-R': 6, 'TN-A': 3}
ids = [r[0].strip('*') for r in ALL]
counts = {p: len(set(i for i in ids if i.startswith(p))) for p in declared}
check('DV-1', counts == declared and sum(counts.values()) == 43,
      f"{sum(counts.values())} obligation rows; P{counts['TN-P']} C{counts['TN-C']} "
      f"R{counts['TN-R']} A{counts['TN-A']}")

# ---------------------------------------------------------------- DV-2
cases = set(int(m) for m in re.findall(r'T-C05-(\d+)', s))
missing = sorted(set(range(1, 68)) - cases)
extra = sorted(cases - set(range(1, 68)))
check('DV-2', not missing and not extra and 'T-C05-35 … 39' in s,
      f"{len(cases)} distinct case ids; missing {missing}; extra {extra}")

# ---------------------------------------------------------------- DV-3
bad = [r[0] for r in ALL if len(r) != 7 or not r[1] or not r[6]]
check('DV-3', not bad, f"{len(ALL)} rows, 7 cells each, implementer non-empty; bad {bad}")

# ---------------------------------------------------------------- DV-4
n4 = s.count('contract layer is Agent 1')
check('DV-4', n4 == 0, f"{n4} occurrences of the withdrawn ownership claim")

# ---------------------------------------------------------------- DV-5
refs = set(re.findall(r'`(C05-\d+\.\d+)`', s))
defs = set()
for ln in lines:
    if ln.startswith('### '):
        defs |= set(re.findall(r'C05-\d+\.\d+', ln))
for m in re.finditer(r'\| `(C05-\d+\.\d+)` \|', s):
    defs.add(m.group(1))
for m in re.finditer(r'> \*\*(C05-\d+\.\d+)', s):
    defs.add(m.group(1))
unresolved = sorted(r for r in refs if r not in defs)
check('DV-5', not unresolved, f"{len(refs)} referenced, {len(refs) - len(unresolved)} defined, unresolved {unresolved}")

# ---------------------------------------------------------------- DV-6
suite_rows = [r for r in table_rows(section('### 12.1 The suites', '### 12.2'))
              if len(r) == 5 and r[0].strip('*') and len(r[0].strip('*')) <= 2 and r[0].strip('*') != '#']
tots = sum(int(re.sub(r'\D', '', r[3]) or 0) for r in suite_rows)
check('DV-6', len(suite_rows) == 18 and tots == 67, f"{len(suite_rows)} suites, case sum {tots}")

# ---------------------------------------------------------------- DV-7
S14 = section('## 14. Dependencies', '## 15.')
check('DV-7', all(t in S14 and 'OPEN' in S14 for t in ('TD-06', 'TD-09', 'TD-12')),
      "TD-06, TD-09, TD-12 present in §14, each still OPEN")

# ---------------------------------------------------------------- DV-8
ex = [ln for ln in lines if 'execut' in ln.lower()]
ALLOW8 = ('document check', 'document validation', '0 executed', 'not run', 'never', 'cannot',
          'not prove', 'no acceptance', 'adr-0012', 'runnable specification', 'executing any of',
          'execution honesty')
ok8 = '0 executed' in s and all(any(a in ln.lower() for a in ALLOW8) for ln in ex)
check('DV-8', ok8, f"{len(ex)} lines contain 'execut'; every one concerns a document check or is negated; '0 executed' present")

# ---------------------------------------------------------------- DV-9
td = [ln for ln in lines if 'TDDCore' in ln]
check('DV-9', all('MEAD' in ln for ln in td), f"{len(td)} lines mention TDDCore, all MEAD-qualified")

# ---------------------------------------------------------------- DV-10
nb = bad10 = 0
for blk in s.split('\n\n'):
    tl = [l for l in blk.split('\n') if l.strip().startswith('|')]
    if len(tl) >= 2:
        nb += 1
        ns = {len(l.strip().strip('|').split('|')) for l in tl if not set(l.strip()) <= set('|-: ')}
        if len(ns) > 1:
            bad10 += 1
check('DV-10', bad10 == 0, f"{nb} tables, {bad10} malformed rows")

# ---------------------------------------------------------------- DV-11 row-level mapping
S54 = section('### 5.4', '## 6. Consumer information paths')
decl = {}
for c in table_rows(S54):
    if len(c) >= 3 and c[0].startswith('`'):
        tok = c[0].strip('`')
        m = re.search(r'rows?\s+(\d+)(?:[–-](\d+))?', c[2])
        if not m:
            continue
        a = int(m.group(1)); b = int(m.group(2)) if m.group(2) else a
        decl[tok] = set(range(a, b + 1))
allowed = {'TN-P': {2}, 'TN-C': {5, 6}, 'TN-R': {2, 4}, 'TN-A': {8}}
observed, fails = {}, []
for r in ALL:
    oid, tok = r[0].strip('*'), r[6]
    observed[tok] = observed.get(tok, 0) + 1
    pref = oid[:4]
    if tok not in decl:
        fails.append(f"{oid}: token '{tok}' not declared")
    elif not (decl[tok] & allowed[pref]):
        fails.append(f"{oid}: token '{tok}' maps to rows {sorted(decl[tok])}, allowed for {pref} are {sorted(allowed[pref])}")
check('DV-11', not fails and len(decl) == 7 and len(observed) == 5,
      f"{len(decl)} declared / {len(observed)} observed tokens, {len(ALL)} cells; "
      f"declared-unused {sorted(set(decl) - set(observed))}; failures {fails[:3]}")

# ---------------------------------------------------------------- DV-12 VF set across three homes
names7 = ['Phase', 'WindupEndAxis', 'ActiveEndAxis', 'RecoveryEndAxis', 'ProducerRate', 'WindowKey', 'AttackTag']
vf31 = set(n for n in names7 if n in section('> **VF — versioned fields', '> **OF — observation-instant'))
vf1 = set(n for n in names7 if n in section('> **INV-1 (corrected).** Two observations', '> **INV-2'))
i_struct = s.index('// ---- VF: versioned fields')
vfs = set(n for n in names7 if n in s[i_struct:i_struct + 1400])
old_phrase = s.count('identical in `RemainingLocalSeconds`')
check('DV-12', vf31 == vf1 == vfs and len(vf31) == 7 and old_phrase <= 1,
      f"VF homes equal: §3.2={len(vf31)} INV-1={len(vf1)} struct={len(vfs)}; sets equal {vf31 == vf1 == vfs}; "
      f"old equality phrase occurrences {old_phrase}")

# ---------------------------------------------------------------- DV-13 aging + precondition
t54 = section('| **T-C05-54**', '\n')
has_rt = {'INV-2': 'R(t) = max(0, R0' in section('> **INV-2', '> **AD-1'),
          'TN-C-10': 'R(t) = max(0, R0' in req('TN-C-10'),
          'T-C05-54': 'R(t) = max(0, R0' in t54}
ep = '(PhaseEndAxis − AxisNow) × ProducerRate' in section('> **INV-2', '> **AD-1')
precond = 'holds only while `ProducerRate` and `PhaseEndAxis` are fixed' in section('> **INV-2', '> **AD-1')
check('DV-13', all(has_rt.values()) and ep and precond,
      f"R(t) form in INV-2/TN-C-10/T-C05-54: {list(has_rt.values())}; endpoint form in INV-2 {ep}; "
      f"one-revision precondition stated {precond}")

# ---------------------------------------------------------------- DV-14 publication order + EX-5
S36 = section('### 3.6 Simultaneous', '### 3.7')
po3 = 'PhaseChanged` at `n+1`' in S36 and 'Retimed` at `n+2`' in S36
po5 = 'C05-2.9 `PO-5`' in S36 and 'C05-2.9 `PO-5`' in s
ex5 = section('### 10.5 EX-5', '### 10.6')
marks = all(m in ex5 for m in ('**(a)**', '**(b)**', '**(c)**', '**(d)**'))
marks2 = '**(cʹ)**' in ex5 and '**(e)**' in ex5
check('DV-14', po3 and po5 and marks and marks2 and 'canonical order' in req('TN-P-15'),
      f"PO-3 order phase→retime n+1→n+2 {po3}; PO-5 present {po5}; EX-5 cases (a)(b)(c)(d) {marks}, "
      f"(cʹ)(e) {marks2}; TN-P-15 canonical {'canonical order' in req('TN-P-15')}")

# ---------------------------------------------------------------- DV-15 bidirectional coverage
S112 = section('### 11.2 Obligation', '## 12.')
cov = {}
for c in table_rows(S112):
    if len(c) == 4 and c[0].startswith('TN-'):
        cov[c[0]] = c[1]
        cov[c[2]] = c[3]
allids = set(r[0].strip('*') for r in ALL)
missing_obl = sorted(i for i in allids if i not in cov or 'T-C05' not in cov[i])
covered = set()
for v in cov.values():
    covered |= set(int(x) for x in re.findall(r'T-C05-(\d+)', v))
    m = re.search(r'T-C05-(\d+) … T-C05-(\d+)', v)
    if m:
        covered |= set(range(int(m.group(1)), int(m.group(2)) + 1))
miss_cases = sorted(set(range(1, 68)) - covered)
check('DV-15', not missing_obl and not miss_cases,
      f"{len(allids)} obligations mapped; cases covered {len(covered)}; "
      f"missing obligations {missing_obl[:3]}; missing cases {miss_cases[:6]}")

# ---------------------------------------------------------------- DV-16 directory
dn1 = section('> **DN-1', '> **DN-1a') if '> **DN-1a' in s else section('> **DN-1', '> **RM-1')
tnr06 = req('TN-R-06')
check('DV-16', 'whichever occurs first' in dn1 and 'Closed' in dn1 and 'invalidation' in dn1
      and 'scheduling' in tnr06 and 'emits nothing' in tnr06,
      "DN-1 carries all three trigger strings; TN-R-06 forbids timing, scheduling and emission")

# ---------------------------------------------------------------- DV-17 consumer paths
S61 = section('### 6.1 `WindowKey`', '### 6.2')
S62 = section('### 6.2 What stays outside', '### 6.3')
four = sum(1 for k in ('AI reaction', 'Audio cue', 'Montage switch', 'VFX marker') if k in S61)
paths = 'VFX world placement' in S62 and 'Montage and cue asset selection' in S62
audio_owner = '**Agent 2** — the only owner' in S61
check('DV-17', four == 4 and paths and audio_owner,
      f"{four} consumer rows with verdicts; §6.2 VFX+montage rows {paths}; audio single owner stated {audio_owner}")

# ---------------------------------------------------------------- DV-18 resync
check('DV-18', 'struct FTDDTelegraphResynchronisation' in section('### 4.2', '### 4.3')
      and 'FTDDTelegraphResynchronisation' in section('> **EN-3', '> **TM-1')
      and 'FTDDTelegraphResynchronisation' in S8 and '### 6.3' in s,
      "struct in §4.2; referenced by EN-3, TN-C-09 and §6.3")

# ---------------------------------------------------------------- DV-19 reviewer-finding ledger
S2 = section('## 2. Finding-by-finding', '## 3.')
f7 = ['D-1', 'D-2', 'D-3', 'D-4', 'D-5', 'D-6', 'D-7']
conds = ['C4a-1', 'C4a-2', 'C4c-1', 'C4c-2', 'C6-1', 'C6-2', 'C9']
ok19 = all(('**%s**' % f) in S2 for f in f7) and all(k in S2 for k in conds)
check('DV-19', ok19, f"7 defect rows + 7 condition rows in §2; all present {ok19}")

# ---------------------------------------------------------------- DV-20 arbitration boundary
S92 = section('### 9.2 `C05-6.4`', '### 9.3')
three = all(k in S92 for k in ('**Creation**', '**Selection**', '**Outcome**'))
tnc11 = req('TN-C-11')
tna02 = req('TN-A-02')
tna03 = [r for r in cells('TN-A') if r[0].strip('*') == 'TN-A-03']
sel_only = 'selection' in tnc11.lower() and ('no authority over a hit' in tnc11 or 'grants no authority' in tnc11)
named = 'AttackTag` included' in tna02
row5 = [l for l in lines if 'Consumer integration (Agent 1)' in l][0]
row5_excl = 'does not own the hit outcome' in row5 and 'row 8' in row5 and 'TN-A-01' in row5
EX63 = ''.join(l for l in section('### 12.2', '### 12.3').split('\n') if l.startswith('| **T-C05-63**'))
t63 = all(k in EX63 for k in ('already holds', 'adversarially altered', 'input/use path'))
sel_assert = 'selection call site' in EX63
check('DV-20', three and sel_only and named and len(tna03) == 1 and row5_excl and t63 and sel_assert,
      f"three domains in §9.2 {three}; TN-C-11 selection-only {sel_only}; TN-A-02 names AttackTag {named}; "
      f"TN-A-03 present {len(tna03) == 1}; row 5 excludes the outcome {row5_excl}; "
      f"T-C05-63 combines held snapshot + altered tag + dataflow instrumentation {t63}; "
      f"separate selection assertion {sel_assert}")

# ---------------------------------------------------------------- DV-21 PO-5 in four places
places = {'§3.6': 'C05-2.9 `PO-5`' in S36,
          '§4.9': 'PO-5 (new)' in section('> **PO-4', '\n\n'),
          'TN-P-18': len([r for r in cells('TN-P') if r[0].strip('*') == 'TN-P-18']) == 1,
          'EX-11': 'EX-11' in section('### 10.11', '### 10.12')}
check('DV-21', all(places.values()) and 'interleaved' in S36,
      f"content rule present in {sum(places.values())}/4 places {places}; interleaving stated")

# ---------------------------------------------------------------- DV-22 audio single owner, whole document
MASK, EXEMPT = exempt_mask(lines)
EXEMPT_N = sum(MASK)
row5l = [l for l in lines if 'Consumer integration (Agent 1)' in l][0]
row6 = [l for l in lines if 'Consumer integration (Agent 2)' in l][0]
preamble8 = [l for l in lines if 'Each obligation is implemented by each consuming agent' in l]
no_audio_5 = 'Agent 1 owns no audio' in row5l and 'audio cues' not in row5l.split('|')[1]
audio_6 = 'audio cue selection' in row6
tnc15 = [r for r in cells('TN-C') if r[0].strip('*') == 'TN-C-15']
pre_ok = bool(preamble8) and 'no C-05 audio responsibility' in preamble8[0] and 'camera and audio' not in preamble8[0]

# Deny-by-default (N-1). The old implementation exempted a line if it contained one of
# fifteen finding-number/heading substrings; Agent 2 defeated it with a one-word prefix.
# Now: a line outside an exempt region that mentions both the audio token and the first
# agent must *negate* the assignment, and the negation must be attached to the mention
# (within 80 characters of it), so an unrelated negation elsewhere cannot launder it.
NEG22 = ('owns no audio', 'no c-05 audio responsibility', 'owns none of the audio',
         'not claimed by agent 1', 'no audio responsibility')


def negated_in_clause(ln):
    """True iff the clause that mentions audio also negates the assignment.

    The clause is the text between statement boundaries ('.', ';', '|'). A negation in
    a *different* clause cannot launder an assignment: 'Agent 1 owns audio. Agent 1 owns
    no audio.' is still an offender, and a one-word prefix such as 'D-4 note:' changes
    nothing at all.
    """
    low = ln.lower()
    k = low.find('audio')
    if k < 0:
        return True
    bounds = [m.start() for m in re.finditer(r'(?<!§)[.;|]', low)]
    start = max([b for b in bounds if b < k], default=-1) + 1
    end = min([b for b in bounds if b > k], default=len(low))
    return any(n in low[start:end] for n in NEG22)


bad_audio = [(i + 1, ln.strip()[:100]) for i, ln in enumerate(lines)
             if not MASK[i] and 'audio' in ln and 'Agent 1' in ln and not negated_in_clause(ln)]
# the live ownership text may never be exempted: no [QUOTED] table and no marked block
LIVE22 = (section('### 5.2', '### 5.3') + section('### 6.1', '### 6.2')
          + section('## 8. Consumer', '## 9.') + section('### 12.2', '### 12.3'))
live_unexempted = QUOTED_TABLE_TOKEN not in LIVE22 and QSTART not in LIVE22
check('DV-22', no_audio_5 and audio_6 and len(tnc15) == 1 and imp('TN-C-15') == 'Agent 2, C-05 consumer'
      and pre_ok and live_unexempted and not bad_audio,
      f"row 5 audio removed {no_audio_5}; row 6 owns audio {audio_6}; TN-C-15 present {len(tnc15) == 1}, "
      f"implementer {imp('TN-C-15') or '-'}; §8 preamble clean {pre_ok}; exempt lines {EXEMPT_N} "
      f"(fenced {EXEMPT['fenced']}, quoted table {EXEMPT['quoted_table']}, marked block {EXEMPT['marked_block']}); "
      f"live sections unexempted {live_unexempted}; scan offenders {len(bad_audio)} {bad_audio[:2]}")

# ---------------------------------------------------------------- DV-23 identity constancy
norm = section('## 3.', '## 15.')
constancy = re.findall(r"fixed for (?:the|that|this) instance's lifetime", norm)
unquoted_old = re.findall(r'''(?<!['"\u201c])constant for the lifetime(?!['"\u201d])''', norm)
check('DV-23', len(constancy) >= 2 and not unquoted_old
      and len([r for r in cells('TN-P') if r[0].strip('*') == 'TN-P-19']) == 1
      and 'attack identity' in req('TN-P-04').lower() and 'T-C05-66' in s,
      f"identity 'fixed for the instance's lifetime' in normative sections {len(constancy)}; "
      f"unquoted rejected phrase {len(unquoted_old)}; TN-P-19 present; "
      f"TN-P-04 names identity change; T-C05-66 present")

# ---------------------------------------------------------------- DV-24 declared/observed consistency
# Deny-by-default over the whole document. The S4.2 implementation read four hard-coded
# sites and took the *first* regex match per site; three probes on the reviewed blob passed
# a document containing a wrong count (P1 prose, P2 number words, P4 second pair on an
# anchor line). Now every pair, in either order, in digits or number words, on every
# non-exempt line, must equal the computed pair; all four anchors must still exist.
NUMW = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
        'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12}
NTOK = r'(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)'
# Separators are "any character that is not a digit", so a restatement may say
# "declared (7) and observed (5)" (words between the numbers) but may never skip over
# another number — a second pair on the same line cannot hide behind the first.
# 'declared' must not be the first half of 'declared-but-unused'.
DECL_OBS = re.compile(NTOK + r'[\s(]{0,3}declared(?!-)[^0-9;.]{0,24}?' + NTOK
                      + r'[\s(]{0,3}observed', re.I)
# Reverse order ('6 observed of 7 declared'). A comma in the separator means a list,
# not a restatement, so the reverse form is read only across a comma-free window.
OBS_DECL = re.compile(NTOK + r'[\s(]{0,3}observed[^0-9,;.]{0,24}?' + NTOK
                      + r'[\s(]{0,3}declared(?!-)', re.I)
# Parenthetical form: 'declared (7) ... observed (5)', number attached to the word.
DECL_PAREN = re.compile(r'declared(?!-)\s*\(?\s*' + NTOK + r'\s*\)?[^0-9]{0,24}?observed\s*\(?\s*'
                        + NTOK, re.I)

def num_of(tok):
    t = tok.strip().lower()
    return int(t) if t.isdigit() else NUMW[t]


def pairs(txt):
    """All (declared, observed) pairs in txt, either statement order."""
    out = [(m.start(), (num_of(m.group(1)), num_of(m.group(2)))) for m in DECL_OBS.finditer(txt)]
    out += [(m.start(), (num_of(m.group(2)), num_of(m.group(1)))) for m in OBS_DECL.finditer(txt)]
    out += [(m.start(), (num_of(m.group(1)), num_of(m.group(2)))) for m in DECL_PAREN.finditer(txt)]
    return sorted(set(out))


computed = (len(decl), len(observed))
row6c = [l for l in lines if l.startswith('| **6** |')]
# The three sites where the pair must be restated. S4.2 also named a fourth (§18.1's C9
# line) that never resolved — the string does not occur in any revision — so it silently
# read three sites and reported nothing missing. A missing anchor is now a failure.
anchors = {
    '§1 row 6': row6c[0] if row6c else '',
    '§5.4': section('**Declared versus observed', '\n\n'),
    '§13.1 DV-11': section('| **DV-11** |', '\n'),
}
anchors_present = {k: (computed in [v for _, v in pairs(t)] if t else False) for k, t in anchors.items()}
scanned = [(i + 1, pr) for i, ln in enumerate(lines) if not MASK[i] for _, pr in pairs(ln)]
bad_pairs = [(n, pr) for n, pr in scanned if pr != computed]
check('DV-24', all(anchors_present.values()) and len(scanned) >= 3 and not bad_pairs,
      f"computed {computed[0]} declared / {computed[1]} observed; anchor sites "
      f"{sum(anchors_present.values())}/{len(anchors)} {[k for k, v in anchors_present.items() if not v]}; "
      f"pairs read {len(scanned)}; disagreeing pairs {len(bad_pairs)} {bad_pairs[:2]}")

# ---------------------------------------------------------------- DV-25 staleness bound
t14 = req('TN-C-14')
bound = {'call-site scope': 'call site' in t14,
         'max one frame between refreshes': 'one frame apart' in t14,
         'measure = shared axis': 'shared axis' in t14 and 'not the measure' in t14,
         'refresh in the frame of use': 'frame boundary is not used' in t14,
         're-pull or suppress': 'must not perform the timing-dependent action on the aged value' in t14,
         'bound derived as at most one frame': 'at most one frame' in t14,
         'message-only residual kept': 'Message-only residual' in t14}
EX64 = ''.join(l for l in section('### 12.2', '### 12.3').split('\n') if l.startswith('| **T-C05-64**'))
test = {'A3 counterexample schedule': 'first instant of frame *k*' in EX64,
        'worst-case permitted placement': 'worst-case permitted' in EX64,
        'asserted in the stated measure': 'strictly less than one frame' in EX64,
        'negative controls': 'Negative controls' in EX64}
check('DV-25', all(bound.values()) and all(test.values()),
      f"TN-C-14 rules {sum(bound.values())}/7, missing {[k for k, v in bound.items() if not v]}; "
      f"T-C05-64 extensions {sum(test.values())}/4, missing {[k for k, v in test.items() if not v]}")

# ---------------------------------------------------------------- DV-26 PO-3 rationale
S36b = section('### 3.6 Simultaneous', '### 3.7')
stale = 'internal application order is **not observable**' in S36b
observ = 'observable through a mid-frame pull' in S36b
both = '`PO-3`' in S36b and 'PO-5' in S36b
check('DV-26', (not stale) and observ and both,
      f"falsified premise absent {not stale}; 'observable through a mid-frame pull' present {observ}; "
      f"PO-3 and PO-5 both retained {both}")

# ---------------------------------------------------------------- DV-27 provenance, no placeholders
REG = 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_PROVENANCE.md'
DECISION = 'docs/DECISION_C05_SUCCESSOR_IDENTITY_004_2_V1.md'
# fenced code blocks are evidence transcripts, not prose claims: strip them first
prose = re.sub(r'```.*?```', '', s, flags=re.S)
ph = [t for t in ('S41_COMMIT', 'S41_BLOB', 'PUB_COMMIT_PLACEHOLDER', 'PUB_BLOB_PLACEHOLDER',
                  '_PLACEHOLDER', 'TODO', 'TBD') if t in prose]
S17 = section('## 17. Publication', '## 18. Handoff')
S18 = section('## 18. Handoff')
pinned = ('95918268ed5b20b878fef3ee0a7855ad18e6eeb6' in S17
          and 'd54e194affeaee98b1030e2b83b4c34e234fa382' in S17
          and 'a788f953256d208f3eb1310f3897924d007179b1' in S17
          and '7d03e1df837493305831962f43882a1cd3496143' in S17)
reg = REG in S17 and REG in S18
# N-2: the identity decision is recorded, and the withdrawn copy carries a distinct identity
identity = DECISION in S17 and 'TDD-A1-C05-SUCCESSOR-004.2-D' in S17
# N-3: Agent 2's addendum is cited
addendum = 'e434dbe' in S17
check('DV-27', (not ph) and pinned and reg and identity and addendum,
      f"placeholders found {ph}; S4.1 and S4.2 commit+blob recorded in §17 {pinned}; "
      f"provenance register referenced in §17 and §18 {reg}; identity decision recorded with the withdrawn "
      f"identity in §17 {identity}; Agent 2's addendum cited in §17 {addendum}")

print('\n'.join(shown))
passed = sum(1 for _, ok, _ in results if ok)
print(f"\n{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
