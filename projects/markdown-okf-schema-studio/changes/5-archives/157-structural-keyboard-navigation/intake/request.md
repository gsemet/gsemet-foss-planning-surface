# 157 — Keyboard navigation goes into and out of nested blocks (table cells, admonitions)

Type: feat · Priority: P2 · From backlog: `02-backlog/P2/right-on-table-selection-to-enter-edit-cell`
(second half; the first half is CR 156). Intent copied verbatim: [01-intent.md](../01-intent.md),
section "Right or left on table to enter cell edition", image [image-2.png](../evidence/image-2.png).

## Intent

In edit mode with no block editor open, Up/Down move from block to block but never one level down.
Wanted: Right goes down one level (table → its cells; admonition → its inner blocks; a whole-page
selection as in image-2 → its first child), Left and Escape go up one level. Inside a table, the
four arrows move cell to cell; Escape leaves the table (back to the table block). Enter on a
selected cell opens the cell editor as a click does.

## Autonomous decisions (orchestrator, 2026-10-28; list them in the PR body)

- Separate PR from the empty-document fix (CR 156); stacked right above it (same keyboard code).
- Right on a block without children does nothing; Left at top level does nothing; Escape at top
  level keeps today's behaviour.
- Arrow keys inside a table stop at the edges (no wrap).
