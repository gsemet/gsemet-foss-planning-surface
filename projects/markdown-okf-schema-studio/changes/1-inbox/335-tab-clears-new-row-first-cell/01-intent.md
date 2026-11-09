---
id: 335-tab-clears-new-row-first-cell
project: markdown-okf-schema-studio
stage: inbox
kind: bug
source:
  forge: github
  repository: gsemet/markdown-okf-schema-studio
  issue: 335
  url: https://github.com/gsemet/markdown-okf-schema-studio/issues/335
  title: "Create row + edition + tab = content of first cell disapears"
  state: open
  reporter: gsemet
  reporter_role: owner
  opened: 2026-11-09T12:00:16Z
  comments: 0
  labels: []
  synced: 2026-11-09
platform: windows
area: table cell editor
requirements:
  - SwRS-MDOKFSTUDIO-TABLE-035
code:
  - src/page/features/tableCellEditor.ts
priority: null
understanding: hypothesis
reproduced: false
open_questions: 3
attachments:
  - path: intake/attachments/01-new-row-empty-first-cell-7da383cf.png
    shows: new table row, first cell rendered empty, cell editor open in the second cell
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

- **The text was probably saved.** The same `README.md`, read from disk right after the report,
  held a fourth row `| dsfdsffsd | |`: the first cell's text reached the source. So the likely
  bug is that the page shows the cell empty, not that the text is lost. To confirm: no reload
  happened in between, and nothing else wrote that row.
- **Where it happens:** Tab in a cell editor calls `tabThroughTableCells`, then `switchTableCell`
  ([tableCellEditor.ts](../../../../../../markdown-okf-schema-studio/src/page/features/tableCellEditor.ts),
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
