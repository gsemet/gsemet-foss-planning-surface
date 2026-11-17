---
title: Tab clears the first cell of a new table row
description: After Tab, the cell just edited shows empty; the text is saved.
status: inbox
date: 2026-11-10
---

# Tab clears the first cell of a new table row

> [!NOTE]
> GitHub issue [#335](https://github.com/gsemet/markdown-okf-schema-studio/issues/335), screenshot
> in the issue. Owner order: first.

## The bug

1. Add a row to a table.
2. Type in the first cell of the new row.
3. Press <kbd>Tab</kbd>.

The caret moves to cell 2, but cell 1 shows empty. Owner (2026-11-10): the text is still in the
file. Display only, reproduces every time.

## Likely cause (code at `ccaf35b8`)

On Tab, `switchTableCell` (`src/page/features/tableCellEditor.ts` L63-85, called from
`tabThroughTableCells` L90-126) saves without re-rendering. It then puts back the rendered content
captured when the editor opened, which is empty for a new row. Requirement:
`SwRS-MDOKFSTUDIO-TABLE-035`.

## Open questions (recommendations, not decided)

| Question | Recommendation |
| --- | --- |
| Does an existing row also show its old text after Tab? | Check it, and fix the general case: same cause. |
| How is it tested? | A failing test first, then the fix; update TABLE-035 if its text misses this case. |
| Automatable (short spec the owner does not review)? | The owner's call. |
