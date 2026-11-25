P = ('C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/'
     '2-actives/507-sc21-cards-foreman/evidence/cards-inventory-chief-of-staff.md')
raw = open(P, 'rb').read().decode('utf-8')
eol = '\r\n' if '\r\n' in raw else '\n'
L = raw.split(eol)
OLD_CHECK = "grep -c 'help grill-series' chief-of-staff.md"


def table(n, ident, home, check):
    s = L[n - 1]
    assert s.startswith('| ' + ident + ' |'), (n, s[:30])
    old_tail = ' | card chief-of-staff.md:3 | ' + OLD_CHECK + ' |'
    assert s.endswith(old_tail), (n, s[-100:])
    L[n - 1] = s[: -len(old_tail)] + f' | {home} | {check} |'


table(81, 'C-063', 'card chief-of-staff.md:34', "grep -c 'Direct mode' chief-of-staff.md")
table(86, 'C-068', 'card chief-of-staff.md:3', "grep -c 'rank above' chief-of-staff.md")
table(87, 'C-069', 'card chief-of-staff.md:3', "grep -c 'rank above' chief-of-staff.md")
table(217, 'C-199', 'card chief-of-staff.md:29; floor 7', "grep -c 'failed preflight' chief-of-staff.md")
s = L[938]
assert s.startswith('| C-896 |') and 'card chief-of-staff.md:14; floor 10' in s
L[938] = s.replace('card chief-of-staff.md:14; floor 10', 'card chief-of-staff.md:16 (asks-first item 4); floor 10')


def closing(n, ident, rest):
    s = L[n - 1]
    assert s.startswith('| ' + ident + ' |'), (n, s[:30])
    cells = s.split(' | ', 2)
    L[n - 1] = f'{cells[0]} | {cells[1]} | {rest} |'


closing(1721, 'C-063', 'card chief-of-staff.md:34; `chief-of-staff.md:34` "Direct mode (after `open --direct` or a switch on the user\'s word)…"')
closing(1726, 'C-068', 'card chief-of-staff.md:3; `chief-of-staff.md:3` "…The project\'s rules rank above chantier\'s."')
closing(1727, 'C-069', 'card chief-of-staff.md:3; `chief-of-staff.md:3` "…in their language (repository and forge text in English)… The project\'s rules rank above chantier\'s."')
closing(1729, 'C-199', 'card chief-of-staff.md:29; `chief-of-staff.md:29` "Start anything after one failed preflight condition, or offer another way."; floor 7')
closing(1905, 'C-896', 'topic recovery; the rule it applies: card chief-of-staff.md:16 (asks-first item 4); floor 10')
open(P, 'wb').write(eol.join(L).encode('utf-8'))
for n in (81, 86, 87, 217, 939, 1721, 1726, 1727, 1729, 1905):
    print(n, L[n - 1][-220:])
