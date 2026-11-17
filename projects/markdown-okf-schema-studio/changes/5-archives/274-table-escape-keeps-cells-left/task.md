# Task

Specification: `03-change-spec.md` with `02-answers.md`. Single CR, not a stack: the driver pushes and
opens the PR **as a draft** (`gh pr create --draft`), and runs `gh pr ready <n>` only at `ready`.
Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/274`, branch
`change-requests/274-table-escape-keeps-cells-left`, based on `origin/main`.

Start from: `src/page/features/tableCellEditor.ts` (the cancel path, `restoreTableCellContent`,
`switchTableCell`, `bindKeys`), `src/page/modules/cellInlineMarkdown.ts`, the session/host side that
restores the original table on cancel, the SwRS `TABLE-013`, `TABLE-025`, `TABLE-035`, and their tests
(`test/page/runtimeTableCellEditor.test.ts`, `test/integration/realInput/textEditing.ts`).

Layering (constitution, section 2). No new dependency.

Tests first (see the spec). Gates: `just check`; headless visual capture of the table-editing group;
no real VS Code window locally (CI runs them); a heavy CI run on the branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`). Before and after screenshots if the page
changes visibly (likely none: say so).
