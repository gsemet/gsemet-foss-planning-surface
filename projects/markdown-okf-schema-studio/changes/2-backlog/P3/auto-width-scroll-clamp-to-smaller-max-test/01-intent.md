# Test the clamp when an Auto re-measure shrinks a table's scroll range

Type: test · Priority: P3 · Filed 2026-10-31 from the final review of the Auto-width scroll fix

## Today

`widthMode.update()` restores the sideways scroll of each element it measures, clamped to the new maximum. No test
covers a clamp down to a SMALLER maximum:
- In the unit test "a layout pass in Auto keeps the sideways scroll of a wide table", the fake's `clientWidth` is 0,
  so `restoreScroll` never clamps.
- The visual scenario `layout-width/v91-auto-wide-table-keeps-scroll-light-656` narrows the pane, which raises the
  maximum.
- The restore also covers tables and code blocks nested in a measured element; no test covers that either.

## Expected

- A unit test where the box widens (the breakout grows), so the old offset exceeds the new maximum and ends at
  exactly that maximum.
- A unit test where an unchanged value is never written.
- A case for a nested table or code block.
