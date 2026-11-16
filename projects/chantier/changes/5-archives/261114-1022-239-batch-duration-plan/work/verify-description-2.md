# Description check 2, PR 181 at af970ea

Result: VERIFIED

- CR numbers: the posted body holds "CR-239" only under Internal references; the card example uses placeholders (<first change> -> ... -> <last change>). Fixed.
- CI time: body says "a recent passed CI run 10.4 min (run on 8566cca)". gh run list: 8566cca success, 08:27:14Z to 08:37:38Z = 10.4 min. Arithmetic (6 x 34.4 = 206.4; lock 312) unchanged and right. Fixed.
- Quick check: head still af970ea, five checks pass, sections and content otherwise unchanged.
