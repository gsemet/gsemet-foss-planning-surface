## Summary

Inserting a table (Table, HTML table, Table with caption) while the caret is inside a pipe table,
a `{list-table}` or an HTML table no longer splits that table. The new table is placed on its own
lines after the last line of the table that holds the caret.

## Deliverable showcase

Before: caret in the row `| 1 | 2 |` of an existing table; the new table lands inside it.

```text
| A | B |
| --- | --- |
| 1 | 2 |        <- caret here, new table inserted at this point
```

After: the existing table stays whole and the new table follows it.

```text
| A | B |
| --- | --- |
| 1 | 2 |

| Column 1 |
| --- |
```

## Test plan

- New `tableInsertAfterTable.test.ts`: 2 tests covering the three table forms and the three actions.
- `just check` passes (compile, boundaries, limits, unit, contracts, security, requirements lint).
- okfreq validate, lint and update-coverage checks: 1010 requirements, 0 errors.

## Internal references

CR 071 (table-insert-splits-table).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
