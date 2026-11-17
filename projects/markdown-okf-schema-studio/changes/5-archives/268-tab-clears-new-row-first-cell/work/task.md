# Task

Specification: `03-change-spec.md`. Single CR, not a stack: the driver pushes and opens the PR.
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/268`, branch
`change-requests/268-tab-clears-new-row-first-cell`, based on `origin/main` (`ccaf35b8`).

Files to start from: `src/page/features/tableCellEditor.ts` (`switchTableCell`,
`tabThroughTableCells`, the arrow-key handler), `restoreTableCellContent` / `hideTableCellContent`
in the block editor, `test/page/runtimeTableCellEditor.test.ts`,
`requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-035.md`.

Approach: when the editor leaves a cell without a re-render, the cell shows its current text, not
the content captured at open. Prefer the page's existing inline renderer for a cell, if one exists
in the page layer; otherwise state the choice in the report. Do not add a re-render per keystroke.

Tests first: a unit test that fails on the unchanged code (new row: Tab from a typed first cell;
existing row: changed text, then Tab; an arrow key). Add a real-input check if
`test/integration/realInput/markers.ts` covers TABLE-035 moves.

Docs: TABLE-035 gains a scenario; `just requirements-update`; a dated entry in
`requirements/tiers/log.md`; a `CHANGELOG.md` `## Unreleased` line (fix, user words).

Gates: `just check`; `just e2e` for the table-editing group as far as the machine allows (real-window
tests need an unlocked screen; CI runs the full gate). Before and after screenshots, light and dark,
in `out/`, named in the report.
