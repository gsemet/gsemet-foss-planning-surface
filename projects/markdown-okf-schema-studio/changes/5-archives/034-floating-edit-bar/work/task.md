# T1 — floating-edit-bar

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-034 (branch `fix/floating-edit-bar` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Decision: the bar sits just ABOVE the edited block, never covering its text. When the block's top scrolls out of view, the bar sticks to the top of the viewport (below the preview toolbar) as long as the block is visible; it never leaves the viewport.
- Keep keyboard focus and caret in the block when the bar moves; no layout shift of the block text (text never moves).
- Works for block, table-cell and frontmatter editors that show the bar; narrow pane (360/460 px) keeps the bar inside the pane (wraps or scrolls horizontally inside itself).

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: edited block at top, middle and scrolled so the block top is hidden; 900 and 460 px. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/034-floating-edit-bar/reports/T1-r<round>.md`.
