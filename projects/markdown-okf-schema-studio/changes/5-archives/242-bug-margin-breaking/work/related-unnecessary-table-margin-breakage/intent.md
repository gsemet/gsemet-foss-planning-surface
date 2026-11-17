In this case the margin breakage is not needed

![image.png](image.png)

## Owner review of the prototype (2026-10-31)

[prototype.html](prototype.html) shows 12 cases at a 720px column: A in column, B today's breakout
to the natural width, C a chosen width, D the proposed rule.

Owner verdicts:

- Cases 1, 2 (two columns, prose): B is wrong, they must stay in the column.
- Case 3 (ID, status, prose): A, B and C all squeeze the short columns; it fits in the column.
- Case 4 (task, owner, date, notes): A needs wider minimums for its short columns; breaking out is
  also acceptable if the minimums are wider.
- Case 5 (four prose columns): B (break out) is better; A is acceptable.
- Cases 6, 7, 10, 11, 12 (long code paths, URLs, tick matrix, mixed, long identifiers): B is best.
- Cases 8, 9 (numbers that fit): fine as they are.
- When a table breaks out, it takes its natural width, capped by the page (B), not a narrower
  compromise (C).

## Proposed rule (variant D, matches every verdict)

1. A **token column** never wraps: every cell is inline code, a number, a date, or at most three
   words. Its minimum width is its widest cell.
2. A **prose column** needs about 20 characters of the body font.
3. The table stays in the column when the sum of these minimums (plus cell padding) fits; token
   cells keep `white-space: nowrap`, prose wraps.
4. Otherwise it breaks out to its natural width, capped by the available page width (today's
   breakout width).

D's decisions at 720px: stays for 1, 2, 3, 4, 8, 9; breaks out for 5, 6, 7, 10, 11, 12.
Open points for the CR: token detection for a cell holding code plus a few words; the 20ch prose
minimum as a constant; behaviour in Full and Narrow width modes (rule applies to Auto only).

## Status (owner, 2026-10-31): set aside

Parked for now: no CR yet. Variant D above is the Chief of Staff's working hypothesis, to be
checked with the owner before any CR starts.
