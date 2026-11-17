## Summary

In edit mode, table cells could become too narrow to click or type in, for example a freshly
added column without a title. Cells now keep a usable minimum width while editing. The rendered
(read) view is unchanged.

## Deliverables

- Every table cell has `min-width: 8em` in edit mode, so an empty new column stays clickable.
- The cell being edited has `min-width: 300px`.
- Requirement TABLE-006 extended with the behaviour and a scenario.
- Unit test for the styles and a width assertion in the visual cell-editor check.

Before / after (dark, cell editor open): `reports/shots/before-v04-cell-editor-wraps-dark-900--open.png`
and `reports/shots/after-v04-cell-editor-wraps-dark-900--open.png`; cream:
`before-v08-row-handles-cream-900.png` / `after-v08-row-handles-cream-900.png`.

Reproduction of an added column with an empty header (real VS Code window, dark VS Code theme,
Cream preview, edit mode): the empty column collapsed to 23 px with the editor clipped before the
fix; it is now at least 8em wide and 300 px while edited. A new real-window test covers it and
fails on the old CSS.
Before:  ( variant: header opened);
after:  ( variant).

Reproduction of an added column with an empty header (real VS Code window, dark VS Code theme,
Cream preview, edit mode): the empty column collapsed to 23 px with the editor clipped before the
fix; it is now at least 8em wide and 300 px while edited. A new real-window test covers it and
fails on the old CSS.
Before: `reports/shots/before-r2-empty-column-cream.png` (`-open` variant: header opened);
after: `reports/shots/after-r2-empty-column-cream.png` (`-open` variant).

## Autonomous decisions

- Split the widths (8em for all cells, 300px for the edited cell) instead of 300px everywhere,
  which would push most tables into horizontal scroll.
- Visual checks "column width unchanged" / "cell did not shrink" now tolerate a cell that grows to
  300px (a wider cell wraps to fewer, shorter lines).

## Internal references

- CR 113, `.agents/changes/03-requests/113-table-edit-cell-min-width/00-request.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
