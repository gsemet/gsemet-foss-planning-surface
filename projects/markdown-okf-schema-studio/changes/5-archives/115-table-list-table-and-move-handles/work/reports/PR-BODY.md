## Summary

Table editing in the preview is made reliable for list-tables and gets drag handles for moving rows
and columns:

- Converting a pipe table to a `{list-table}` and back keeps every cell, including the header row.
- Clicking a list-table cell no longer makes the table vanish from the edit box; the raw directive
  editor stays in view.
- Row move handles (left of the table) now reorder rows even when a cell editor is open.
- New column move handles sit above the table, outside the cells, for pipe tables and list-tables
  (drag, or Alt+Left/Right).

## Deliverables

```text
pipe table      <-> {list-table}   all cells kept, table stays visible
row handles     (left)             drag or Alt+Up/Down, works with a cell editor open
column handles  (above, new)       drag or Alt+Left/Right, both table syntaxes
```

Before/after screenshots (cream and dark themes) are in the PR assets: handles, cell bar,
list-table conversion, list-table cell click, column drag.
(Local copies: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/03-requests/115-table-list-table-and-move-handles/reports/shots)

Tests: unit and webview tests for the editor frame, row and column moves; real-window scenarios
for conversion round trip, row move and column move on both syntaxes. Requirements (new column
handles requirement, updated row move and table requirements), user docs and changelog are updated.

## Autonomous decisions

- A click on a list-table cell keeps opening the whole directive in the raw editor, now in view;
  there is no cell editor for list-tables.
- A move with a cell editor open saves and closes that editor (one final edit); other open editors
  (block, frontmatter) still refuse a drag.
- Column handles hide when their header cell is scrolled out of a wide table and clamp inside its
  visible box.
- Insert before/after and delete row/column are left to the other part of the table fix.
- No visual-harness scenario for the column handles (the scenario file is at its size limit);
  coverage comes from webview and real-window tests.

## Internal references

- CR 115 (part 2 of the new-column bug), PRD folder 03-requests/115-table-list-table-and-move-handles

🤖 Generated with [Claude Code](https://claude.com/claude-code)
