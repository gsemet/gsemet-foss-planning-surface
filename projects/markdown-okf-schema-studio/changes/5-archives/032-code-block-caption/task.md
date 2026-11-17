# T1 — code-block-caption

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-032 (branch `fix/code-block-caption` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Code inside {code-block} is left-aligned like a plain fenced block (find the centering rule: likely a figure/caption container style).
- Decision: the :caption: becomes a title bar attached to the top of the code block: left-aligned, light monospace, same width and border as the block, square top joint (like the file name header on GitHub or Sphinx Book), readable in light, dark, cream and current theme.
- Keep line numbers, emphasize-lines and the copy button working; plain fences unchanged (byte-identical PNGs for existing scenarios that have no {code-block}).

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Visual: a {code-block} with caption, light and dark, 900 px (the backlog screenshot `image.png` shows the bug). List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/032-code-block-caption/reports/T1-r<round>.md`.
