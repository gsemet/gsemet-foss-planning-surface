# Conflicts, CR-435 restack onto CR-433 (Kanban merged)

- docs/web-board.md (Batch section): kept the merged Kanban paragraph (four tabs, Kanban default, batch-folder chip) and put CR-435's title-row sentence first; "The legend pill stays above the tabs" became "sits in the title row, on every tab"; tabs are "the first line above the central view".
- js/views/batch.js, header comment: merged (four tabs, mode and legend in `batch-head.js`).
- batch.js `recorded()`: kept the Kanban's `closed[...]` notes, dropped `${mode}` and `${legend()}` (CR-435 moved them to the title row).
- batch.js `render()`: kept the Kanban panel map (kanban/graph/lazy), dropped `modeBand` and `legend()` from the markup.
- tests/test_board_design.py: both sides appended different tests; kept both. The merged file passed 400 lines (`test_code_targets` refuses), so CR-435's title-row tests moved, unchanged, to the new `tests/test_board_title_row.py` (imports `CSS`, `WEB`, `rules` from `test_board_design`). Uncommitted: the Driver commits it (a fixup of cb58d84f's rebased commit 0562f8cd, or a new commit).
- Pictures commit (2004e521): replayed with no conflict.

Fast gate: `just check` in the worktree, run after the split: pass (1631 passed, 20 skipped; release-notes ok).
