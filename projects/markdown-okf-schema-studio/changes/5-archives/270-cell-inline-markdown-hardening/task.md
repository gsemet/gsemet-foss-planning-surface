# Task

Specification: `03-change-spec.md`, findings in `01-intent.md`. Single CR, not a stack: the driver
pushes and opens the PR. Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/270`,
branch `change-requests/270-cell-inline-markdown-hardening`, based on `origin/main`.

Files: `src/page/modules/cellInlineMarkdown.ts`, a new test file in `test/page/` (keep
`runtimeTableCellEditor.test.ts` under its 1 500-line cap: the arrow-key loop may need to replace the
single ArrowRight case rather than add one), `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-035.md`
(verification notes), `requirements/tiers/log.md`, `CHANGELOG.md`.

Tests first: the new cases fail on the unchanged code where the spec says so. No assertion changes intent.

Gates: `just check`. No real-window test is needed (page-layer only); CI runs the full gate. No
screenshot needed unless the visible rendering changes (emphasis): then one before/after pair.
