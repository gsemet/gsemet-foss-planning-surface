# Table move handles: no drop marker when the pointer is over a column or row

Type: fix · Priority: P1 · Reported 2026-10-27 during the demo tour of CR 115 (row and column move handles)

## Intent (user)

The row and column handles of a table work only when the pointer is placed exactly between two
columns. When I drag a column handle and move it over the next column (above that column, in the
handle strip), there is no event and no marker between the two columns, and nothing happens on
release. Same issue for row handles.

## Expected

- While a handle is dragged, the whole area of the table and of its handle strips is a drop zone:
  over any column (or row), the marker shows on the nearest gap (left or right half of the column,
  upper or lower half of the row), and releasing moves the column or row there.
- The marker follows the pointer continuously; releasing outside the table cancels the drag.

## Before starting the CR

Reproduce it in a real VS Code window on a pipe table and a `{list-table}`: drag a column handle
along the handle strip above the header and over the header cells; drag a row handle over the middle
of another row. Note where the marker appears and where it does not. The real-window e2e
(`test/integration/tableMoves.ts`) drops on the target cell itself; add drops over the handle strip
and mid-column, and make them fail on the current code.
