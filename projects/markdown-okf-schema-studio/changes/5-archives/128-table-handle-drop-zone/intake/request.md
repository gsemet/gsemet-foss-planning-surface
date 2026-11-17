# 128 — Table row and column handles drop anywhere over the table and its handle strip

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-table-handle-drop-zone`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- Follow the backlog item's expected behaviour (nearest gap by half of the column or row, marker follows the pointer, release outside cancels).
- Extend `test/integration/tableMoves.ts` with drops over the handle strip and mid-column/mid-row.
