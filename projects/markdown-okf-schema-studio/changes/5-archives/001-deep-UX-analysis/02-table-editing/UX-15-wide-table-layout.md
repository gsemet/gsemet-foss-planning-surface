# UX-15 — Wide tables wrap short identifiers and hide the horizontal scrollbar far below

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Rendering (tables) |
| Evidence | [u10-table.jpg](../evidence/u10-table.jpg) |

## Observed

In a 16-column table rendered in a 540 px preview:

- the table scrolls horizontally, yet short identifiers still wrap inside narrow columns
  (`nw-` / `02`, `North` / `Pole`), doubling row heights;
- the header "Night intake" is cut at the right edge with no visual hint that more columns exist;
- the horizontal scrollbar sits under the last row, off screen when the table is taller than the
  viewport, so mouse users cannot discover the overflow.

## Suggested direction

When a table overflows, use `white-space: nowrap` for short cells (or a `min-width` per column
based on the longest word), add an edge fade or shadow on the overflow side, and consider a sticky
first column or a sticky horizontal scrollbar.

## Done when

The visual scenario "very wide table at 540 px" shows complete identifiers and an obvious
overflow cue.
