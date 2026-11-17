# Task: table handles on the real table edges

## Files (start here)

- `src/page/features/tableRowMove.ts` (row move and its handles), `src/page/features/pageInput.ts`,
  `src/page/modules/widthMode.ts` (the breakout width).
- The column handles: same area, search `tableRowMove` neighbours for columns.

## Change

Compute handle positions from the table element's own box (and each row/column box), not from the
text column. Recompute after a row or column move and after a breakout width change.

## Tests first

- Page test that fails today: a table wider than the column (breakout), move a row → each row
  handle's vertical centre matches its row and its left edge sits at the table's left edge; same
  for column handles. Plus a table that stays in the column.
- e2e scenario in group `table-editing` (simulated), screenshot of a broken-out table in edit mode.

## Requirements

Update the table handle SwRS of scope `table-editing`, markers per `rules.md`.

## Gates (foreground)

- `just check`
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`
