## Summary

In the table cell editor, "Col +" replaced the current column's title with an empty cell, and the
row and column delete buttons did nothing. The cause: a structural button changed the table but
left the cell editor sitting on the old cell, so the editor showed the new empty cell and later
cell switches used positions that no longer matched. Each structural button now saves the table
and reopens the editor in the target cell.

## Deliverables

The table bar now has seven buttons: `Row above`, `Row below`, `Row -`, `Col left`, `Col right`,
`Col -`, `List table`. Inserting never touches existing cells; the editor reopens in the new empty
cell.

Before (the title is gone) and after (title kept, new column added):

| | Cream | Dark |
| --- | --- | --- |
| Before | ![before cream](reports/shots/before-cream.png) | ![before dark](reports/shots/before-dark.png) |
| After | ![after cream](reports/shots/after-cream.png) | ![after dark](reports/shots/after-dark.png) |

```text
src/page/modules/tableStructure.ts   new: insertRowBefore, insertColumnBefore, parseListTable
src/page/features/tableCellEditor.ts 7 buttons; save + reopen after each structural press
src/page/features/blockSourceEditor.ts list-table model fallback
```

Plain `{list-table}` blocks (one header row, one-line cells, no other option) now open the same
cell editor and are written back as a list-table.

Tests: unit tests for each button (11 failed on the old code), plus a real-window end-to-end
scenario that presses all buttons on a pipe table and on a list-table and checks the text.

## Autonomous decisions

- Labels `Row above`/`Row below`/`Col left`/`Col right`; after an insert, the editor opens in the
  new empty cell.
- `Row above` is disabled on the header row; `Row -` on the header or last body row; `Col -` on a
  one-column table.
- List-table support is limited to plain ones; others still open the raw editor.
- Moving rows/columns, the list-table conversion and the cell-disappearing bug are left to a
  follow-up.

## Internal references

CR 114 (part 1/2 of backlog item bug-new-column); follow-up CR 115. Not run: full preflight and the
visual Python captures.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
