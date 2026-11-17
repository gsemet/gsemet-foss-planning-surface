# 240 — Table row and column handles follow the table's real edges

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-240`, branch `change-requests/240-bug-row-anchors-in-margin-break`.
Part of a stacked run.

## Intent

From [01-intent.md](01-intent.md): after a row reorder in a table that breaks out of the margin,
the row handles are misplaced. Check columns too.

![Row handles stuck after a reorder](image.png)

## Owner decisions (2026-11-03)

See [02-decisions.md](02-decisions.md):

- Row handles sit on the table's real left edge (outside the table, centred on their row), and
  column handles on the top of each column, whether the table breaks out of the margin or not.
- They are placed again after a row or column move.
