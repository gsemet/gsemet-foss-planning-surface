# T1 — myst-list-table

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-038 (branch `feat/myst-list-table` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Render {list-table} with :header-rows:, :widths:, :align: and a title argument, consistent with existing table styles.
- Decision: a button in the table-level toolbar converts pipe table → list-table and list-table → pipe table; a simple HTML table converts to either; never produce HTML. A conversion that would lose content (multi-line cells or block content to pipe) shows a message and changes nothing.
- Conversion is one undo step; round trip pipe → list-table → pipe is lossless for simple tables (unit tests with src/webview/markdownTable.ts helpers).

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: a list-table rendered, light and dark; real-window or visual: the conversion button. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/038-myst-list-table/reports/T1-r<round>.md`.
