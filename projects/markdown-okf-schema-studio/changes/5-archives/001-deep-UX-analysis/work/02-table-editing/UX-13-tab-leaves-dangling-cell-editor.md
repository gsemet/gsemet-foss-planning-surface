# UX-13 — Tab does not move to the next cell and leaves the cell editor dangling

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Table cell editing, keyboard |
| Evidence | [u13-cell-tab.jpg](../../evidence/u13-cell-tab.jpg) |

## Use case

An author fills a table row from the keyboard, pressing Tab to go to the next cell, as in every
spreadsheet and in most Markdown table editors.

## Steps to reproduce

1. Click a cell in `fixtures-visual/04-code-and-tables.md` (edit mode), type, press Tab.
2. Press Escape.

## Observed

- Tab moves browser focus to the next focusable element after the table (the "Deeply nested
  lists" heading, which gets a focus ring).
- The cell editor stays open: the toolbar still says "Row 3, column 2" and the cell textarea is
  still mounted, but nothing has focus inside it. The cell input has no blur handler, so nothing
  is committed or closed.
- Escape now does nothing (the keydown handler is on the cell input, which no longer has focus).
- Clicking another block finally commits the cell and opens the other block.

Arrow keys at the start or end of the cell text do navigate to neighbouring cells, but nothing
documents this.

## Expected

Tab / Shift+Tab move to the next / previous cell (adding a row after the last cell is a common
bonus). Escape works while the table editor is open, wherever focus is.

## Where it comes from

`src/webview/scrollSync.ts` `renderTableCellEditor` keydown (L1644-L1653) handles only Escape and
Enter; no `blur`/`focusout` handling for the cell editor.

## Done when

The table can be filled with Tab alone, and the cell editor never stays open without focus.
