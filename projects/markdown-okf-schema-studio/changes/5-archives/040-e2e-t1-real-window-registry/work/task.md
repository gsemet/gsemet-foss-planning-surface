# T1 — e2e-t1-real-window-registry

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-040 (branch `test/real-window-registry` from origin/main; rebase on the latest origin/main before starting). Work ONLY there; `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read `00-request.md` (decisions = the spec), the `backlog-*` files and images here, and `rules.md`.

## Change

- Follow plan.md section 6 "T1" (archives/021-feature-session-007-020/p9-e2e/plan.md) restarted on current main; the parked patch (archives/021-.../p9-e2e/parked/T1-wip.patch) is a reference only, never applied as is.
- Decision: T1 includes run isolation so several real-window runs can run in parallel: unique user-data dir, extensions dir, CDP port, evidence folder and run id per run. Prove it by running two suites at the same time once (respect the WINDOW-TESTS lock otherwise; the proof run holds the lock for both).
- Keep LATEST pointers, INDEX.md, manifest fields and run folder prefixes as the plan requires; README images compared with --check.

## Tests (write first; they must fail on the unchanged code)

- Unit tests for the logic (test/webview/, test/unit style of the neighbours).
- Visual scenario(s) in test/visual/scenarios.ts with group, description, locks and content assertions (next free id per group on current main), and/or real-window scenario(s) when the behaviour needs a real editor.
- Existing scenarios: no unintended PNG change.

## Docs

CHANGELOG Unreleased bullet (user-facing). README / docs where the feature is documented.

## Gates (foreground)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`. Real-window tests (integration/e2e) are allowed TONIGHT only under the lock in rules.md, one run at a time.

## Screenshots for the PR

Real-window: the gallery/INDEX of a run; the counts before/after. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/040-e2e-t1-real-window-registry/reports/T1-r<round>.md`.
