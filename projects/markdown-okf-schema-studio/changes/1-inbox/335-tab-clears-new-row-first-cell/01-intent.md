---
type: cr-intent
id: 335-tab-clears-new-row-first-cell
description: "Bug, Windows: Tab after typing in the first cell of a new table row shows that cell empty; likely display only, not reproduced yet."
generated: {by: "agent:claude-opus-5-5", at: "2026-11-09T14:00:00Z"}
sources: [{id: issue, resource: "https://github.com/gsemet/markdown-okf-schema-studio/issues/335", title: "Create row + edition + tab = content of first cell disapears", author: "github:gsemet", last_modified: "2026-11-09"}]
---

# Tab after editing the first cell of a new row empties that cell

## The request

In the rendered page, on Windows, the owner adds a row to a table, types in its first cell, then
presses Tab. The caret moves to the second cell as expected, but the first cell shows empty.

![New row, first cell empty, editor in the second cell](intake/attachments/01-new-row-empty-first-cell-7da383cf.png)

The screenshot is the `Projects` table of this planning surface's `README.md`: three rows, a new
fourth row whose first cell is empty, the cell editor open in the Description column (Done and
Cancel buttons).

## What we know

- **The text was probably saved.** Commit `5255bc1` of this planning surface (2026-11-09
  12:01:32Z, a minute after the issue was opened) added a fourth row `| dsfdsffsd | |` to that
  same `README.md`: the first cell's text reached the source. So the likely bug is that the page
  shows the cell empty, not that the text is lost. To confirm with the owner: that row is the one
  typed in the reproduction.
- **Where it happens:** Tab in a cell editor calls `tabThroughTableCells`, then `switchTableCell`
  ([tableCellEditor.ts](https://github.com/gsemet/markdown-okf-schema-studio/blob/ccaf35b8/src/page/features/tableCellEditor.ts#L63-L126),
  SwRS-MDOKFSTUDIO-TABLE-035). `switchTableCell` writes the field's value into the table model,
  posts a save without a re-render (`postBlockEditSave(false)`), then
  `restoreTableCellContent` puts back the cell's **rendered content captured when the editor
  opened**. For a cell of a new row, that captured content is empty, so the cell shows empty
  until the next render.
- Existing rows are probably affected too: their cell would show its old text, not the new one.
  Not checked.

## Open questions

1. Does the first cell show its text after a re-render (Escape, Done, or reopening the file)? If
   yes, this is a display bug only.
2. Does it happen on an existing row: edit a cell, Tab, does the old text come back?
3. Windows only, or also on macOS and Linux? Nothing in the code path is platform-specific.

## Next step

Reproduce it in the extension (or in a page-level test), answer questions 1 and 2, then file it
as a CR. It looks small and testable: a candidate for "automatable".
