# T1 — myst-grid-toctree

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-037 (branch `feat/myst-grid-toctree` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Decision {grid}: responsive columns per the `1 1 2 2` breakpoints argument, with grid-item and grid-item-card (title, body, footer, link); both ``` and ::: fences, nesting with colon fences.
- Decision {toctree}: a list of clickable links to the referenced documents; label = the target's H1 when readable, else the file name; :caption: renders as a heading; :hidden: hides the list; globs: list matching files sorted; missing target: entry shown with a warning style. Links use the existing link navigation (open in preview).
- Readable in all themes; narrow pane collapses to one column.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: a grid of cards at 900 and 460 px; a toctree with caption, light and dark. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/037-myst-grid-toctree/reports/T1-r<round>.md`.
