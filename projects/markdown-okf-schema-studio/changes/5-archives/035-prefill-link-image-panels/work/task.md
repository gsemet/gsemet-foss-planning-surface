# T1 — prefill-link-image-panels

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-035 (branch `feat/prefill-link-image-panels` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Decision: with the caret (or selection) inside an existing Markdown link, the link panel opens pre-filled (text + URL + title if any) and Save REPLACES that link; same for images (alt + path + title) with the image panel.
- All block and cell editors that offer these panels (src/webview/linkPanel.ts, figurePanel.ts, editActions.ts...). Reference-style links: pre-fill from the definition when resolvable, else insert inline (note it).
- Undo restores the previous link in one step; no change when the caret is outside any link/image.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual or real-window: the pre-filled link panel and image panel. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/035-prefill-link-image-panels/reports/T1-r<round>.md`.
