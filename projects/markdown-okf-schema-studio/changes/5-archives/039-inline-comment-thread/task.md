# T1 — inline-comment-thread

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-039 (branch `feat/inline-comment-thread` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Format (from the backlog intent): `<!-- THREAD` / `User (YYYY-MM-DD HH:MM):` / indented lines / ... / `-->`.
- Decision: renders as a green chip with a speech-bubble icon; expanding it shows an admonition-like callout with the messages. Interactions: read, reply (author = git user.name, date in the same format), delete the thread. Created from the slash menu or palette at block level. Hidden with the other chips (chip toggle).
- Existing comment/TODO chips and review threads unchanged; parsing tolerant of CRLF and trailing spaces; replying preserves the rest of the file byte for byte.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: collapsed and expanded thread, light and dark; real-window or visual: reply. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/039-inline-comment-thread/reports/T1-r<round>.md`.
