# T1 — paste-rich-text-markdown

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-036 (branch `feat/paste-rich-text-markdown` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Decision: convert `text/html` clipboard content to Markdown with an in-repo converter based on parse5 (already a dependency; NO new dependency): headings, bold, italic, strikethrough, links, nested lists, inline code, code blocks (language from class when present), blockquotes, simple tables (GFM pipe), images as links. Everything else becomes plain text. Sanitize: drop scripts/styles/comments/event attributes.
- Decision: Cmd/Ctrl+Shift+V pastes plain text unchanged. Image paste (CR 018) unchanged.
- Unit tests: a table of HTML inputs (Google Docs, Word, a web page snippet, VS Code copy) → expected Markdown; undo is one step.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Real-window or visual: before/after of a pasted rich snippet. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/036-paste-rich-text-markdown/reports/T1-r<round>.md`.
