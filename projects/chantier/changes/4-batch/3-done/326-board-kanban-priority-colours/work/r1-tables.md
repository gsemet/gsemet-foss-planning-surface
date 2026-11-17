# Round 1 tables (CR-326)

Ratios are WCAG 2.x contrast ratios (script: `work/coder/colours.py`).

## Text on background

| Pair | Text | Background | Ratio |
| --- | --- | --- | --- |
| P1 chip | `#ffffff` | `#1d5c63` | 7.60:1 |
| P2 chip | `#ffffff` | `#4a7e83` | 4.56:1 |
| P3 chip | `#123d42` | `#88acb0` | 4.84:1 |
| P4 chip | `#123d42` | `#cfe2e3` | 8.83:1 |
| Active nav row (ink and icon) | `#123d42` | `#e9f1f1` | 10.34:1 |
| Active nav row on the sidebar tint (row bg vs side bg, not text) | `#e9f1f1` | `#f6f9f9` | 1.08:1 |
| mark 0 letter | `#a02e78` | `#f2e2ec` | 5.34:1 |
| mark 1 letter | `#1a6c88` | `#dfeaee` | 4.84:1 |
| mark 2 letter | `#3a7222` | `#e3ebe0` | 4.77:1 |
| mark 3 letter | `#8a3aa8` | `#efe3f3` | 5.21:1 |
| mark 4 letter | `#666c12` | `#eaeade` | 4.66:1 |
| mark 5 letter | `#1a736d` | `#dfebeb` | 4.63:1 |

(The row marked 'not text' is the active row's fill against the sidebar's; it is a shape, not text, and has no 4.5:1 requirement.)

Priorities: P1 `#1d5c63` (hue 186), P2 `#4a7e83` (185), P3 `#88acb0` (186), P4 `#cfe2e3` (183): one teal, no new hue.

State hues: blocked 351.5, working 221.5, ready 152.4, draft 30.0, local 257.6, waits 36.3, merged 152.2.

## The marks

| Mark | Old | New | New hue | Nearest state hue (gap) | Old hue / nearest gap |
| --- | --- | --- | --- | --- | --- |
| --mark-0 | `#c8401f` | `#a02e78` | 321.1 | blocked #d14b5e (30.4 deg) | 11.7 / draft 18.3 deg |
| --mark-1 | `#2f6f9f` | `#1a6c88` | 195.3 | working #4a76d9 (26.3 deg) | 205.7 / working 15.8 deg |
| --mark-2 | `#5b7a2a` | `#3a7222` | 102.0 | merged #2a7a55 (50.2 deg) | 83.3 / waits 47.0 deg |
| --mark-3 | `#7a4aa8` | `#8a3aa8` | 283.6 | local #8b6bd8 (26.0 deg) | 270.6 / local 13.0 deg |
| --mark-4 | `#a8691f` | `#666c12` | 64.0 | waits #d08a1f (27.7 deg) | 32.4 / draft 2.4 deg |
| --mark-5 | `#1f7a74` | `#1a736d` | 176.0 | ready #2f9e6b (23.5 deg) | 176.0 / ready 23.6 deg (kept hue family; darkened for 4.5:1) |

Mark 5 (`#1f7a74`, hue 176, 23.6 deg from ready) was not required to move (it matches no state's look); it is darkened only to reach 4.5:1 on its tint (hue unchanged, 23.5 deg). Mark 2 moved from hue 83 to 102 (more distinct from mark 4, now at hue 63). The new marks stay distinct: hues 321, 195, 102, 284, 63, 176 (marks 1 and 5 are 19 deg apart, told apart by the cyan-blue against the green-teal). None equals a `--pri-N`.

Tints: each mark mixed with white at 14%, written as literals: --mark-0-tint `#f2e2ec`, --mark-1-tint `#dfeaee`, --mark-2-tint `#e3ebe0`, --mark-3-tint `#efe3f3`, --mark-4-tint `#eaeade`, --mark-5-tint `#dfebeb`.
