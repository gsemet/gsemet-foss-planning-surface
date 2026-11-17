# T1 — rtl-paragraphs

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-031 (branch `fix/rtl-paragraphs` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Emit `dir="auto"` on block elements (paragraphs, headings, list items, blockquotes, table cells) so RTL text right-aligns like GitHub.
- Allow the `dir` attribute in the sanitizer allow-list (values `ltr`, `rtl`, `auto` only).
- Remove `knownIssue: "P9-B4-K2"` from rendering-core/v17, v18 (fixture 35-cjk-rtl) and add content assertions: RTL paragraphs right-aligned, LTR unchanged, no horizontal scroll.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: fixture 35-cjk-rtl at 900 and 460, light and dark. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/031-rtl-paragraphs/reports/T1-r<round>.md`.
