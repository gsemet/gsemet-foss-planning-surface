# T1 — comment-chips

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-033 (branch `fix/comment-chips` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Fix the parsing/rendering so each HTML comment (TODO, comment, the kinds the extension already supports) renders as its real chip, never as a `<!--` label (backlog screenshot `image.png`: three `<!--` chips around a list). Write the failing fixture first from that pattern (comments before/after a list, consecutive comments).
- Decision: the chip show/hide button lives in the toolbar in BOTH preview and edit mode; its state is remembered (existing state store), chips visible by default.
- Decision: the comment box (compose/thread box) loses its rounded corners (square corners; buttons and text inputs may keep a small radius).

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: the okfkb-like list with comments (chips visible and hidden), light and dark; the comment box. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/033-comment-chips/reports/T1-r<round>.md`.
