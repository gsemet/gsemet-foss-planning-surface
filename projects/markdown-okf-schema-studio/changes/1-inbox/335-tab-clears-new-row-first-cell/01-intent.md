---
type: cr-intent
id: 335-tab-clears-new-row-first-cell
description: "Bug, Windows: Tab after typing in the first cell of a new table row shows that cell empty; likely display only, not reproduced yet."
generated: {by: "agent:claude-opus-5-5", at: "2026-11-09T14:30:00Z"}
sources: [{id: issue, resource: "https://github.com/gsemet/markdown-okf-schema-studio/issues/335", title: "Create row + edition + tab = content of first cell disapears", author: "github:gsemet", last_modified: "2026-11-09"}]
---

# Tab empties the first cell of a new table row

New table row, type in the first cell, Tab: the caret goes to the second cell, the first cell
shows empty.

![New row, first cell empty, editor in the second cell](intake/attachments/01-new-row-empty-first-cell-7da383cf.png)

## Known

- **The text is probably saved, only not shown.** The row typed in the reproduction,
  `| dsfdsffsd | |`, reached the `README.md` on disk (commit `5255bc1`, a minute later).
- **Likely cause:** on Tab, `switchTableCell` saves the value without re-rendering, then puts back
  the cell's content as it was when the editor opened: empty for a new row
  ([tableCellEditor.ts](https://github.com/gsemet/markdown-okf-schema-studio/blob/ccaf35b8/src/page/features/tableCellEditor.ts#L63-L126),
  SwRS-MDOKFSTUDIO-TABLE-035).

## Open

1. Does the text appear after a re-render (Done, Escape, reopen)?
2. Does an existing row show its old text after Tab?

## Next

Reproduce, answer 1 and 2. Small and testable: an "automatable" candidate.
