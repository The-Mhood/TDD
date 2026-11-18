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
        m = re.search(r'rows?\s+([\d\s,–\-]*(?:and|&)?[\d\s,–\-]*)', c[2])
        if not m:
            continue
        # S4.3.6: read *every* number or range in the cell, not just the first. 'rows 2 and 5'
        # used to be read as {2}, silently discarding the row the declaration named second.
        rows = set()
        for a_, b_ in re.findall(r'(\d+)\s*(?:[–-]\s*(\d+))?', m.group(1)):
            lo = int(a_); hi = int(b_) if b_ else lo
            rows |= set(range(lo, hi + 1))
        if not rows:
            continue
        decl[tok] = rows
allowed = {'TN-P': {2}, 'TN-C': {5, 6}, 'TN-R': {2, 4}, 'TN-A': {8}}
observed, fails = {}, []
for r in ALL:
    oid, tok = r[0].strip('*'), r[6]
    observed[tok] = observed.get(tok, 0) + 1
    pref = oid[:4]
    if tok not in decl:
        fails.append(f"{oid}: token '{tok}' not declared")
    elif not decl[tok] <= allowed[pref]:
        # S4.3.6: subset, not intersection. 'rows 2 and 5' for a TN-P cell used to pass on
        # the strength of row 2 alone, leaving row 5 — a row the prefix may not use —
        # unexamined. The rule is that the token's row set lies inside the allowed set.
        fails.append(f"{oid}: token '{tok}' maps to rows {sorted(decl[tok])}, allowed for {pref} are {sorted(allowed[pref])}")

# The §5.4 'Used by' column states the cell counts the instrument finds (Agent 2's D-6b).
# S4.3.6: those hand-restated counts are compared with the computed ones instead of being
# left to drift — the same class of defect DV-24 closes for the declared/observed pair.
claims, claim_fails = {}, []
for c in table_rows(S54):
    if len(c) >= 4 and c[0].startswith('`'):
        ctok = c[0].strip('`')
        mcnt = re.search(r'\*\*(\d+)\s+cell', c[3])
        if not mcnt:
            continue
        claims[ctok] = int(mcnt.group(1))
        if claims[ctok] != observed.get(ctok, 0):
            claim_fails.append(f"'{ctok}': §5.4 says {claims[ctok]} cells, observed {observed.get(ctok, 0)}")
        for npi, pref_i in re.findall(r'(\d+)\s*`(TN-[A-Z])`', c[3]):
            real = sum(1 for r in ALL if r[6] == ctok and r[0].strip('*')[:4] == pref_i)
            if int(npi) != real:
                claim_fails.append(f"'{ctok}' {pref_i}: §5.4 says {npi} cells, observed {real}")
# The third clause of the §5.4 rule — "the row's owner must match the token's agent" — was
# enforced only *through* the row in S4.3.6: every row that belonged to the wrong agent also
# sat outside its prefix's allowed set, so the subset test caught it by accident. TD-60
# demonstrates exactly that weakness: it fails under both validators because row 7 is outside
# TN-C's {5, 6}, so it never exercises ownership at all. S4.3.7 enforces the clause directly.
#
# Row owners, as §5.2 states them (declared here and *verified against the document* below, so
# a change to §5.2 breaks the check rather than silently re-defining it):
#   1 gameplay production        Agent 2 on enemy attacks, Agent 1 on the player's   {1, 2}
#   2 producer-side implementation  the owner of that producer                      {1, 2}
#   3 shared contract artefacts  the contract layer, owner via TD-12                {contract}
#   4 shared read-surface support  Agent 1                                          {1}
#   5 consumer integration (Agent 1)                                                {1}
#   6 consumer integration (Agent 2)                                                {2}
#   7 resolved outside C-05 (Agent 2)                                               {2}
#   8 arbitration                                                                    {1}
ROW_OWNER = {1: {'1', '2'}, 2: {'1', '2'}, 3: {'contract'}, 4: {'1'},
             5: {'1'}, 6: {'2'}, 7: {'2'}, 8: {'1'}}
# §5.2's table is a blockquote ('> | Activity | Owner | Basis |'), so the quote markers come off
# before the rows are read.
S52 = '\n'.join(re.sub(r'^\s*>\s?', '', l)
                 for l in section('### 5.2 C05-7.2', '### 5.3').split('\n'))
rows52 = table_rows(S52)[1:]          # drop the header row
# verify the declared map against §5.2's own words, rather than trusting the constant
owner_map_ok = len(rows52) == 8
if owner_map_ok:
    owner_map_ok = ('(Agent 1)' in rows52[4][0] and '(Agent 2)' in rows52[5][0]
                    and 'Agent 2' in rows52[6][0] and 'contract layer' in rows52[2][1].lower()
                    and rows52[3][1].startswith('**Agent 1')
                    and rows52[7][1].startswith('**Agent 1')
                    and 'Agent 1' in rows52[0][1] and 'Agent 2' in rows52[0][1]
                    and 'Agent 1' in rows52[1][1] and 'Agent 2' in rows52[1][1])
# token -> the agent(s) that own its work, read from §5.4's own 'Agent' column
TOK_AGENT = {}
for c in table_rows(S54):
    if len(c) >= 3 and c[0].startswith('`'):
        t_ = c[0].strip('`')
        named = set(re.findall(r'agent\s*([12])', c[1], re.I))
        celly = (c[1] + ' ' + t_).lower()
        TOK_AGENT[t_] = named or ({'contract'} if 'contract layer' in celly else {'?'})
owner_fails = []
owner_checks = 0
for tok, rws in decl.items():
    for r_ in sorted(rws):
        owner_checks += 1
        own = ROW_OWNER.get(r_, set())
        who = TOK_AGENT.get(tok, set())
        if own and who and not (own & who):
            owner_fails.append(f"'{tok}' declares row {r_}, whose owner is "
                               f"{'/'.join(sorted(own))}, but the token's agent is {'/'.join(sorted(who))}")

check('DV-11', not fails and not claim_fails and not owner_fails and owner_map_ok
      and len(decl) == 7 and len(observed) == 5,
      f"{len(decl)} declared / {len(observed)} observed tokens, {len(ALL)} cells; "
      f"declared-unused {sorted(set(decl) - set(observed))}; failures {fails[:3]}; "
      f"cell-count claims {len(claims)} checked, failures {claim_fails[:3]}" + f"; owner checks {owner_checks} (map verified {owner_map_ok}), failures {owner_fails}")

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

# Deny-by-default (N-1), evaluated per assertion (S4.3.1).
#
# S4.3 accepted a line if a negation appeared anywhere in the clause that contained
# the *first* audio mention. That let a negation launder a later, positive assignment
# in the same clause: 'Agent 1 owns no audio, but Agent 1 owns audio cues.' passed.
# The predicate below evaluates *every* audio mention independently:
#
#   1. a mention is negated only if a negative construction covers that mention
#      ('owns no audio', 'no C-05 audio responsibility', 'audio ... is not claimed by Agent 1');
#   2. otherwise the mention is attributed to the nearest agent reference in its
#      segment — before the mention if there is one, after it if not;
#   3. if that agent is Agent 1, the mention is an offender.
#
# There is still no keyword allowlist: what exempts a line is where it is (a region),
# never which finding numbers it happens to contain. What decides *ownership* here is
# grammar and position, not a list of permitted phrases.
# S4.3.6 — Agent 2's MAJOR-1. Two attribution defects, one cause: the predicate recognised
# only the literal 'Agent <digit>' forms and took the nearest reference before the mention
# unconditionally. So 'The first agent owns the audio cues' matched nothing (the document
# itself uses 'the first agent' seventeen times, including to state this very rule), and in
# 'Agent 1, unlike Agent 2, owns the audio cues' the nearest reference was the *foil*
# 'Agent 2' inside the contrastive clause, so the predicate read the sentence backwards.
# The synonym is read from a named group (a bare alternative would leave group(1) as None),
# and a reference introduced by a contrastive marker is never the subject.
# S4.3.7 — Agent 2's MAJOR-1: extending AGENT_REF alone left every *other* attachment path
# re-spelling the literal 'agent 1', so 'The audio cues are the first agent's.' was accepted.
# The agent-1 name is now written once and every pattern below is derived from it.
AGENT1 = r'(?:agent[-\s]?1|the\s+first\s+agent)'
AGENT1_POSS = AGENT1 + r"\s*[\'\u2019]s"
AGENT_REF = re.compile(r'agent[-\s]?(?P<num>[12])\b|the\s+first\s+agent\b', re.I)
# The foil marker is what precedes the reference, so the test runs on the text in front of
# the match and only has to end with the marker.
# 'whereas' is deliberately NOT a foil: it introduces a clause whose subject is the
# reference that follows it, so 'A, whereas Agent 1 owns the audio cues' asserts Agent 1's
# ownership. Dropping that reference loses a true positive (measured: probe C7).
FOIL_BEFORE = re.compile(r'(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\s*$', re.I)


def agent_of(m):
    """Which agent a AGENT_REF match designates: '1' for 'Agent 1' and 'the first agent'."""
    return m.group('num') if m.group('num') else '1'


_CLAUSE_BREAK = re.compile(r'[,;(\u2014]')
_FOIL_ANY = re.compile(r'\b(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\b', re.I)


def is_foil(ln, m):
    """True when *m* is a contrastive foil ('unlike Agent 2') and not the subject.

    S4.3.7 — Agent 2's MAJOR-2: the S4.3.6 test looked at a fixed 32-character window ending
    at the reference, so a foil carrying a subordinate clause pushed its marker outside the
    window and the foil became the subject again — the same inversion TD-42 fixed, one clause
    further away. The foil is now bound to the clause the reference sits in: scan back to the
    nearest clause boundary (comma, semicolon, parenthesis, em dash) and ask whether *that*
    clause opens with a contrastive marker. A marker in an earlier clause does not count, so
    'Unlike the earlier draft, Agent 1 owns the audio cues' keeps Agent 1 as the subject.
    """
    head = ln[:m.start()]
    brk = [b.end() for b in _CLAUSE_BREAK.finditer(head)]
    clause = head[brk[-1]:] if brk else head
    if len(clause) > 120:
        return False
    return bool(_FOIL_ANY.search(clause))
# A negation must deny ownership or responsibility, not merely put 'no' before 'audio'.
# S4.3.1 accepted any 'no ... audio' within 28 characters, so 'has no problem owning audio
# cues' and 'has no objection to owning audio cues' read as denials when they are the
# opposite. The constructions below are the bounded set of grammatical *denials*; each has
# to contain the audio mention it denies, and anything outside the set is a positive
# statement. This list is not an exemption list: failing to match it makes a mention an
# offender, it does not make a line exempt.
_DENIAL_NOUN = r'(?:responsibility|ownership|authority|duty|obligation|mandate)'
_MODS = r'(?:(?:C-05|contract|cue|cues|of|any|the)\s+){0,2}?'
# A quantified denial ('no audio cue ... belongs to Agent 1') may not reach its possession verb
# across a clause boundary. S4.3.8 allowed any character except '.', ';' and '|' in that gap,
# so 'No audio cue is assigned to Agent 2 and the audio cue belongs to Agent 1' was read as one
# denial: the gap crossed the conjunction, and a line that *asserts* Agent 1's ownership passed.
# The gap below stops at a coordinating conjunction or a clause separator, so the denial can only
# cover its own clause.
#
# `_NOT_CROSS` (defined further down, for NEG_AFTER) is the same idea but not the same set: it
# also excludes the relative pronouns 'that', 'which', 'who' and 'whose', and a *restrictive*
# relative belongs inside the quantified subject — 'no audio cue **that** belongs to Agent 1' is
# one denial, not two clauses. Measured: applying _NOT_CROSS verbatim here turns TD-82 and TD-83
# from PASS into FAIL. Hence a narrower gap rather than the existing one.
_Q_GAP = (r'(?:(?!\b(?:and|but|yet)\b)'            # no coordinating conjunction
          r'[^.;|,\u2014\u2013])')                  # no clause punctuation

NEG_BEFORE = (
    # 'owns no audio cue', 'has no C-05 audio responsibility', 'carries no audio duty'
    re.compile(r'\b(?:owns?|owned|owning|has|have|had|holds?|carries|carry|claims?|exercises?)\s+no\s+'
               + _MODS + r'audio\b', re.I),
    # 'no audio responsibility', 'no C-05 audio ownership'
    re.compile(r'\bno\s+' + _MODS + r'audio\s+' + _DENIAL_NOUN + r'\b', re.I),
    # 'no responsibility for audio cue selection', 'no ownership of audio'
    re.compile(r'\bno\s+' + _DENIAL_NOUN + r'\s+(?:for|over|of)\s+' + _MODS + r'audio\b', re.I),
    # 'is not responsible for audio', 'is not the owner of audio'
    re.compile(r'\b(?:is|are|was|were)\s+not\s+(?:responsible|the\s+owner|an\s+owner)\s+(?:for|of)\s+'
               + _MODS + r'audio\b', re.I),
    # 'does not own audio', 'do not own any audio'
    re.compile(r'\b(?:does|do|did)\s+not\s+own\s+' + _MODS + r'audio\b', re.I),
    # 'owns none of the audio'
    re.compile(r'\bowns?\s+none\s+of\s+the\s+audio\b', re.I),
    # 'does not belong to the first agent' (S4.3.7, found by the same probe matrix that
    # widened the positive possessor: the new 'belongs to' form needed its denial)
    re.compile(r'\baudio\b[^.;|]{0,30}?\b(?:does|do|did)\s+not\s+belong\s+to\s+'
               + AGENT1 + r'\b', re.I),
    # 'No audio cue belongs to Agent 1', 'None of the audio cues belong to the first agent',
    # 'There is no audio cue that belongs to Agent 1' (S4.3.8, Agent 2's CONDITION-1).
    # A *determiner-quantified subject* denies possession without a negated verb, so the
    # 'belongs to' widening read it as an assignment. The quantifier governs the mention, so
    # the construction spans it — 'no ... audio ... belong(s) to <Agent 1>'.
    re.compile(r'\b(?:no|none\s+of\s+the)\s+' + _MODS + r'audio\b' + _Q_GAP + r'{0,50}?'
               r'\bbelong(?:s)?\s+to\s+' + AGENT1 + r'\b', re.I),
    # the same quantified subject with the other possession predicates the widening taught
    re.compile(r'\bno\s+' + _MODS + r'audio\b' + _Q_GAP + r'{0,50}?\b(?:is|are|was|were)\s+'
               r'(?:owned|claimed|carried|held|supplied|provided|selected|chosen)\s+by\s+'
               + AGENT1 + r'\b', re.I),
    re.compile(r'\bno\s+' + _MODS + r'audio\b' + _Q_GAP + r'{0,50}?\b(?:is|are|was|were)\s+'
               + AGENT1_POSS + r'\b', re.I),
    # 'owns the camera, not the audio cues' — the *object* is negated (S4.3.6, found when
    # 'the first agent' became attributable: the line is a genuine denial and must not fail).
    # S4.3.10: the negation must be *stated*. Until S4.3.9 this construction also accepted a bare
    # comma, `(?:\bnot|,)`, so it matched ', the audio' on its own — and in a comma splice that
    # carries no negation at all, it negated the object of a clause that asserts ownership:
    # 'No audio cue is provided for Agent 2, the audio cue belongs to Agent 1' passed DV-22
    # (Agent 2's F-1b). The comma alternative contributed no intended form — a comma followed by
    # 'not' is matched by 'not', with or without a space after the comma — so it is removed and
    # the negator is required. 'owns the camera, not the audio cues' and 'owns the camera, not
    # any audio cues' still pass, which TD-104…TD-107 assert.
    re.compile(r'\bnot\s+(?:the\s+|any\s+)' + _MODS + r'audio\b', re.I),
)
# The reversed form: the mention comes first and the denial follows it. Two scope rules
# (S4.3.3), because a later denial was cancelling an earlier positive assertion:
#   * the denial must sit in the *same clause and the same phrase* as the mention — the gap
#     may not cross a comma, a statement separator, or a conjunction / relative pronoun, so
#     'owns audio cues, but those cues are not assigned to Agent 1' cannot be read as a
#     denial of the first mention;
#   * if the denial names an agent at all, it must name the *first* agent: 'is not a
#     responsibility assigned to Agent 2' denies something about Agent 2 and says nothing
#     about Agent 1's ownership.
_NOT_CROSS = (r'(?:(?!\b(?:and|but|yet|while|although|whereas|which|who|whose|that)\b)'
              r'[^.;|,\u2014\u2013])')  # an em dash introduces an apposition, not a denial
NEG_AFTER = (
    re.compile(r'\baudio\b' + _NOT_CROSS + r'{0,40}?\b(?:is|are|was|were)\s+not\s+'
               r'(?:owned|claimed|carried|held|assigned|a\s+responsibility)\b', re.I),
    re.compile(r'\baudio\b' + _NOT_CROSS + r'{0,30}?\b(?:is|are)\s+(?:no|not\s+a)\s+'
               + _DENIAL_NOUN + r'\b', re.I),
)
# S4.3.4 adds the third scope rule. A trailing denial that names nobody used to excuse the
# mention outright, so 'Agent 1 owns audio cues that are not owned' was accepted: the line
# asserts ownership and the check called it a denial. An unnamed denial now counts only when
# it is an explicit *universal* exclusion (nobody / no one / anyone), and only when the same
# clause does not itself assert that the first agent owns the cues. 'Genuinely excludes
# Agent 1' is the test, not the presence of a negative word.
_UNIVERSAL = re.compile(r'\b(?:anyone|anybody|nobody|no[\s-]?one)\b', re.I)
_POS_OWNER_1 = re.compile(
    # a *positive* ownership phrase: 'not owned by Agent 1' is a denial, not an assertion
    r'(?<!\bnot\s)\b(?:owned|claimed|carried|held|supplied|provided|selected)\s+by\s+' + AGENT1 + r'\b'
    r'|' + AGENT1_POSS + r'\s+(?:audio|cues?|cue)\b'
    r'|\baudio\b[^.;|]{0,14}:\s*' + AGENT1 + r'\b'
    r'|\baudio\b[^.;|]{0,40}?\bbelongs?\s+to\s+' + AGENT1 + r'\b', re.I)
SEGMENT = re.compile(r'[.;|]')


def audio_mentions(ln):
    return [m.start() for m in re.finditer(r'\baudio\b', ln, re.I)]


def negated_mention(ln, pos):
    """True iff a bounded denial construction covers *this* mention and no other one.

    'Covers' is positional: the construction's own text must span the mention, so a denial
    of one thing can never be borrowed by another mention on the same line.
    """
    for pattern in NEG_BEFORE:
        if any(m.start() <= pos <= m.end() for m in pattern.finditer(ln)):
            return True
    for pattern in NEG_AFTER:
        for m in pattern.finditer(ln):
            if not (m.start() <= pos <= m.end()):
                continue
            # The agent a denial names usually follows the participle ('not owned by Agent 2'),
            # so read the rest of the clause as well: a denial that names another agent says
            # nothing about Agent 1's ownership and must not excuse the mention.
            tail = re.split(r'[.;|,]', ln[m.end():])[0][:30]
            # a contrastive foil is dropped here as well: in 'not assigned to Agent 2' the
            # named agent is the *excluded* party, which says nothing about the first agent
            frag = m.group(0) + tail
            named = [agent_of(r) for r in AGENT_REF.finditer(frag) if not is_foil(frag, r)]
            if named:
                if named[0] == '1':
                    return True
                continue
            # Unnamed (S4.3.4): only an explicit universal exclusion counts, and only when the
            # clause does not also assert that the first agent owns the cues. An unnamed
            # 'not owned' is not evidence that Agent 1 does not own them.
            start, end = segment_bounds(ln, pos)
            if _UNIVERSAL.search(m.group(0) + tail) and not _POS_OWNER_1.search(ln, start, end):
                return True
    return False


def segment_bounds(ln, pos):
    before = [m.start() for m in SEGMENT.finditer(ln) if m.start() < pos]
    after = [m.start() for m in SEGMENT.finditer(ln) if m.start() > pos]
    return (max(before) + 1 if before else 0), (min(after) if after else len(ln))


# S4.3.7 — every construction below is built from AGENT1/AGENT1_POSS rather than re-spelled, and
# the class is widened to the remaining positive-ownership forms the same probe matrix found:
# possession by the synonym, 'belongs to', and 'owner is' (A2 MAJOR-1 and the class it belongs to).
FORWARD_OWNER = (
    re.compile(r'\baudio\b[^.;|]{0,40}?\b(?:is|are|was|were)\s+'
               r'(?:owned|claimed|carried|held|supplied|provided|selected|chosen)\s+by\s+'
               + AGENT1 + r'\b', re.I),
    re.compile(r'\baudio\b[^.;|]{0,30}?\b(?:is|are|was|were)\s+' + AGENT1_POSS + r'\b', re.I),
    re.compile(r'\baudio\b[^.;|]{0,14}?(?::|\u2014|--)\s*' + AGENT1 + r'\b', re.I),
    re.compile(r'\baudio\b[^.;|]{0,40}?\bbelongs?\s+to\s+' + AGENT1 + r'\b', re.I),
    re.compile(r'\baudio\b[^.;|]{0,30}?\bown(?:er|ers|ership)\b[^.;|]{0,16}?'
               r'(?:is|are|:)\s*' + AGENT1 + r'\b', re.I))


_CONTRAST_OBJECT = re.compile(r'(?:unlike|as\s+opposed\s+to|rather\s+than|but\s+not)\s+'
                              r'(?:the\s+|any\s+|all\s+)?$', re.I)


def _mention_is_contrast(ln, pos):
    """True when the *mention* is the object of a contrast ('rather than the audio cues').

    The marker has to govern this mention directly — a marker earlier in the same clause
    governs whatever follows it, not a mention several words further on. Testing the text
    immediately in front of the mention is what separates
    'The camera, rather than the audio cues, is owned by Agent 1' (the audio is the excluded
    object) from 'Agent 1 rather than Agent 2 owns the audio cues' (the audio is the object
    the first agent owns, and the contrast governs only the agent reference).
    """
    head = ln[max(0, pos - 40):pos]
    cut = [b.end() for b in _CLAUSE_BREAK.finditer(head)]
    return bool(_CONTRAST_OBJECT.search(head[cut[-1]:] if cut else head))


def attributed_to_agent_1(ln, pos):
    """Is *this* mention owned by the first agent?

    Word order is read, not assumed: an agent reference that governs the mention from
    before it, or an explicit ownership construction that governs it from after it
    ('audio cues are owned by Agent 1', 'audio cues are Agent 1's', 'audio cues: Agent 1').
    A reference that merely appears later in the sentence does not attribute anything.
    """
    if _mention_is_contrast(ln, pos):
        # 'The camera, rather than the audio cues, is owned by Agent 1' — the mention is the
        # contrasted object, not the thing owned (S4.3.7; a false positive the widening created)
        return False
    start, _end = segment_bounds(ln, pos)
    before = [m for m in AGENT_REF.finditer(ln, start, pos) if not is_foil(ln, m)]
    if before and agent_of(before[-1]) == '1':
        return True
    return any(pat.search(ln, max(0, pos - 40), pos + 60) and
               any(m.start() <= pos <= m.end() for m in pat.finditer(ln)) for pat in FORWARD_OWNER)


def audio_offences(ln):
    """Every mention in the line that assigns the audio cue to the first agent."""
    return [m for m in audio_mentions(ln)
            if not negated_mention(ln, m) and attributed_to_agent_1(ln, m)]


bad_audio = []
mentions_evaluated = 0
for i, ln in enumerate(lines):
    if MASK[i] or 'audio' not in ln.lower():
        continue
    mentions_evaluated += len(audio_mentions(ln))
    if audio_offences(ln):
        bad_audio.append((i + 1, ln.strip()[:100]))

# the live ownership text may never be exempted: no [QUOTED] table and no marked block
LIVE22 = (section('### 5.2', '### 5.3') + section('### 6.1', '### 6.2')
          + section('## 8. Consumer', '## 9.') + section('### 12.2', '### 12.3'))
live_unexempted = QUOTED_TABLE_TOKEN not in LIVE22 and QSTART not in LIVE22
check('DV-22', no_audio_5 and audio_6 and len(tnc15) == 1 and imp('TN-C-15') == 'Agent 2, C-05 consumer'
      and pre_ok and live_unexempted and not bad_audio,
      f"row 5 audio removed {no_audio_5}; row 6 owns audio {audio_6}; TN-C-15 present {len(tnc15) == 1}, "
      f"implementer {imp('TN-C-15') or '-'}; §8 preamble clean {pre_ok}; exempt lines {EXEMPT_N} "
      f"(fenced {EXEMPT['fenced']}, quoted table {EXEMPT['quoted_table']}, marked block {EXEMPT['marked_block']}); "
      f"live sections unexempted {live_unexempted}; audio mentions evaluated {mentions_evaluated}; scan offenders {len(bad_audio)} {bad_audio[:2]}")

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
DECL_OBS = re.compile(NTOK + r'[\s(]{0,3}declared(?!-)[^0-9]{0,24}?' + NTOK
                      + r'[\s(]{0,3}observed', re.I)
# Reverse order ('6 observed of 7 declared'). A comma in the separator means a list,
# not a restatement, so the reverse form is read only across a comma-free window.
OBS_DECL = re.compile(NTOK + r'[\s(]{0,3}observed[^0-9,;.]{0,24}?' + NTOK
                      + r'[\s(]{0,3}declared(?!-)', re.I)
# Parenthetical form: 'declared (7) ... observed (5)', number attached to the word.
# S4.3.6 — three forms that were reaching the prose without reaching the check: a label
# followed by punctuation ('declared: 6, observed: 5'), a pair split by a sentence break
# ('6 declared. Then 5 observed.') and a pair wrapped across a line break (scanned below).
DECL_PAREN = re.compile(r'declared(?!-)[\s:(]{0,4}' + NTOK + r'\s*\)?[^0-9]{0,24}?observed[\s:(]{0,4}'
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
# A restatement wrapped across a line break is still a restatement. S4.3.6 joined adjacent
# pairs only, so a three-line wrap escaped (Agent 2's MINOR-1 and the same class reported
# separately). S4.3.7 joins runs of up to three lines, under guards that stop unrelated
# adjacent facts being welded into a pair that neither line states:
#   * never across a block boundary — table row, heading, blockquote, list item, fence, blank;
#   * never across a sentence terminator — a wrap is mid-sentence, a new fact is not;
#   * in a **three**-line window each internal boundary must continue the sentence (lowercase
#     or a connective/digit). S4.3.7 applied that gate to two-line windows as well, which
#     rejected every capitalised continuation ('Counts: 6 declared' / 'The audit shows 5
#     observed') and so *lost* detection of real hazards without buying safety: the block and
#     sentence guards carry the false-join defence, and 'one label each' rules out cross-pairing
#     (S4.3.8, Agent 2's CONDITION-2);
#   * the window may carry at most one 'declared' and one 'observed' label, so two separate
#     claims cannot be cross-paired into a contradiction.
_BLOCK_START = re.compile(r'\s*(?:\||#|>|[-*+]\s|\d+[.)]\s|`)')
_SENT_END = re.compile(r'[.!?]\s*$')
_CONT_START = re.compile(r'\s*(?:[a-z0-9]|and\b|or\b|then\b|with\b|versus\b|vs\.?\b|to\b|'
                         r'of\b|in\b|for\b|per\b|the\b|each\b)')


def _joinable(a, b, require_cont):
    """Can line b be a continuation of line a (same claim, same paragraph)?

    *require_cont* is set for the internal boundaries of a three-line window only. A two-line
    window is already made safe by the block and sentence guards plus 'one label each', and
    gating it on the continuation left every capitalised wrap unread (Agent 2's CONDITION-2).
    """
    if not a.strip() or not b.strip():
        return False
    if _BLOCK_START.match(a) or _BLOCK_START.match(b):
        return False
    if _SENT_END.search(a):
        return False
    return bool(_CONT_START.match(b)) if require_cont else True


def _one_each(txt):
    return len(re.findall(r'declared(?!-)', txt, re.I)) <= 1 and len(re.findall(r'observed', txt, re.I)) <= 1


for k in (1, 2):
    for i in range(len(lines) - k):
        window = list(range(i, i + k + 1))
        if any(MASK[j] for j in window):
            continue
        require_cont = k == 2          # three-line windows keep the stricter gate
        if not all(_joinable(lines[a], lines[a + 1], require_cont) for a in window[:-1]):
            continue
        joined = ' '.join(lines[j].strip() for j in window)
        if not _one_each(joined):
            continue
        scanned += [(i + 1, pr) for _, pr in pairs(joined)]
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
REG = 'docs/AGENT1_C05_CONTRACT_SUCCESSOR_V4_3_10_PROVENANCE.md'
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
