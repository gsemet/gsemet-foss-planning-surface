## Summary

The table editor had four rough edges. Col + and Col - rewrote the whole table in one fixed style, the
editor and the preview disagreed on a pipe inside a code span, the table bar drew a rule between Col +
and Col -, and the rule before the cell formatting group stayed behind when the group wrapped. They
now behave the way the rest of the table editor does: a small edit is a small diff, and the editor
shows the cells the preview shows.

## Deliverables

Col + on an indented, padded table (before and after):

```text
before                       after
| Name  | Qty |             | Name  |       | Qty |
| ----- | --- |     ->      | ----- | ----- | --- |
| brake | 1   |             | brake |       | 1   |
(everything rewritten as      (indentation, padding and outer pipes kept;
 "| a | b |")                 Col + then Col - gives back the original text)
```

An unescaped pipe inside a code span splits a cell, as in the preview (GFM):

| Row | Preview | Editor before | Editor now |
| --- | --- | --- | --- |
| `\| `x\|y` \| z \|` | three cells | two cells | three cells: not a pipe table of the editor |
| `\| `x\\\|y` \| z \|` | two cells | two cells | two cells |

A pipe typed inside a code span is written `\|` (the preview shows the plain pipe).

The table bar: one rule per group, and the cell formatting group carries its rule when it wraps.

```text
Row +  Row -  | Col +  Col -  | List table      (no rule between Col + and Col -)
| B  I  S  A  link  emoji ...                   (the rule starts the group's line)
```

Screenshots of the wrapped bar at 360 px, light and dark (visual scenarios `table-editing/v24` and
`v25`): rule before Col + and List table, none between Col + and Col -, the formatting group on its own
line with its rule.

A panel, popover or slash menu of the cell formatting group belongs to the cell it was opened in: it
closes when the editor moves to another cell (Tab, arrows, a click) or a row or column button is
pressed, because it acts on the text selected in that cell. The requirements now state this rule.

## Changes

- `src/page/modules/markdownTable.ts`: column operations track each column's source column, and the
  serializer writes every line from its own source segments (kept cells verbatim, a new cell in the
  style of its left neighbour, delimiter dashes to the column width); a line that cannot be edited in
  place falls back to the canonical form alone. The cell splitting and the pipe escaping no longer treat
  a code span as shelter for a pipe.
- `src/page/features/tableCellEditor.ts` with `editModeStyles.ts` and `editPaletteStyles.ts`: the rule
  and the cell formatting group are one flex item; the column rule applies to the first button of each
  group.
- Requirements and changelog updated; four "Known issue" lines are removed.

## Impacts

- Editing a table with the column buttons no longer reformats the other lines.
- A source table with an unescaped pipe in a code span in a body row (one more cell than its header) is
  no longer opened by the cell editor, matching the preview, which already dropped the extra cell. Write
  `\|` in the code span to keep the pipe in the cell.
- Existing assertions whose intent is unchanged but whose fixtures needed the escaped form: the code-span
  pipe in the round-trip, list-table conversion and HTML conversion tests is now written `\|`. One
  assertion changed expectation on purpose: after Col + a new row's empty cell keeps the width of the
  row it was copied from (`|   |` instead of `|  |`).
- Visual: the bar of the cell editor (new scenarios at 360 px, light and dark).

Further changed assertions, all following the new column model and markup: the insert/delete test in
`markdownTable.test.ts` now matches a new cell as `\| new \| cell \| +\|` (a new cell takes the
width of its neighbour); the T24 test builds an explicit model instead of passing `columnsChanged`
(the field is replaced by `columnOrigins`); the T35 tests in `runtimePaletteActions.test.ts` and
the selector in `capture_edit_checks.py` look inside the new `.sphinx-preview-table-menu-cell-group`
wrapper. Their intent is unchanged.

## Blast radius

Grade: **1**

Local to the pipe-table model and the table bar styles. A `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code, checked by stashing `src/`): column
      operations keep padding, indentation and outer pipes; Col + in the runtime keeps the style; a pipe
      in a code span splits the cell; the bar styles.
- [x] Requirements: SwRS updated, markers in code and tests, `okfreq update-coverage`, validate and lint
      pass.
- [x] Local gates: `just check` (unit 2659 passed, 0 failed), `just ci-visual` (357 scenarios, 246
      screenshots, passed).
- [ ] Review
- [ ] CI green

## Internal references

- Change request 099 (table editor polish); SwRS TABLE-048, TABLE-055, TABLE-091, TABLE-102, StRS TABLE-011.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
