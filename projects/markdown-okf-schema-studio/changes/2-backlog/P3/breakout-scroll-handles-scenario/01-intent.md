# Handles on a breakout table that scrolls sideways

Type: test · Priority: P3 (from P2, owner, 2026-11-04: a coverage gap, no known bug) · Filed
2026-11-03 from CR 242 (round 4 diagnosis).

Under CR 242's Auto width rule, a table of token columns wider than the page breaks out, is capped
at the page width and scrolls sideways. The row and column handles of a column outside the visible
area are clamped to the edge on purpose (`position()` in `src/page/features/tableRowMove.ts`).
No visual scenario covers this case: v26 and v27 now use prose cells (fixture 63) so their table
fits after breakout.

Add a simulated visual scenario (group `table-editing`) with a scrolling breakout table that checks:
the clamped handle of the last column, the handles after scrolling it into view, and a row move.
See `.agents/changes/04-archives/242-bug-margin-breaking/diagnosis-r4.md`.
