# Task

Specification: `03-change-spec.md`. Single CR, not a stack: the driver pushes and opens the PR.
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/269`, branch
`change-requests/269-table-narrows-on-cell-edit`, based on `origin/main`.

Files to start from: `src/page/modules/widthMode.ts` (`eligibleWrappers`), `src/page/features/tableCellEditor.ts`
(`revealOpenCell`, how a cell editor marks its table: `data-sphinx-preview-table-cell-selected`, the
textarea), the block editor marking `data-sphinx-preview-editing`, the width-mode and table-cell tests in
`test/page/`, the requirements named in the spec.

Approach: tell a cell editor from a source editor in `eligibleWrappers`; a table whose only editor is
a cell editor stays eligible. Keep the sideways re-scroll of the open cell (TABLE-035) working when
the box really resizes. No new dependency-cruiser exception.

Tests first: a unit test that fails on the unchanged code (wide table in Auto, cell editor open → still
marked wide); keep or adapt the source-editor test (still column width), saying why an assertion changes.
Check the real-input/visual scenarios that assert the narrowing (for example `wideTableTab` in Auto)
and update them to the new rule.

Requirements: the approved StRS change sets `approved_by` and `approved_at` as the spec says; then
`just requirements-update` and a dated `requirements/tiers/log.md` entry. `CHANGELOG.md` line in user words.

Gates: `just check`; the layout-width and table-editing e2e groups through `just e2e` as far as the
machine allows (CI runs the full gate). Before and after screenshots, light and dark, in `out/`, named in the report.
