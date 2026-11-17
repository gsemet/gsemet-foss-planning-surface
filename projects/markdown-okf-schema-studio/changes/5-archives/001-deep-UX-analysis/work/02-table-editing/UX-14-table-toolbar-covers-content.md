# UX-14 — The table toolbar covers the previous row, and its labels are ambiguous

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Table cell editing |
| Evidence | [u11-cell-click.jpg](../../evidence/u11-cell-click.jpg) |

## Observed

- The floating toolbar (insert/delete row, insert/delete column, "Row 3, column 2") is placed
  above the selected cell and hides the content of the row above it (row `nw-01` in the evidence).
- The four icons differ only by a small detail; their meaning appears only in a hover tooltip.
- "Row 3" counts the header as row 1; the user sees it as the second data row and the source line
  is 56. None of the three numbering systems is explained.
- The selected cell has no visible editing frame: "North" looks unchanged except for the caret.

## Suggested direction

Place the toolbar outside the table (above the table or in a sticky bar) or make it translucent
on hover; label actions with text in narrow menus; show "Header" / "Row 2 of 6" and highlight the
selected cell.

## Done when

The toolbar never hides cell content the user may need to read while editing.
