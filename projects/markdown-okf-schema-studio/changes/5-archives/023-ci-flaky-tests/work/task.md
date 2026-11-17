# T1 — Remove the root causes of flaky tests F1, F2, F3

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-023 (branch
`fix/ci-flaky-tests` from origin/main 9b5ac08). Work ONLY in this worktree. `node_modules` and
`.venv` there are symlinks to the main checkout: never delete, stage or replace them.
Read `00-request.md` (table of the three flakes + ideas) and `rules.md`.

Get the CI evidence yourself (read-only):
- `gh run view 39779674653 --log-failed | cut -c60-` (F1, F2), `gh run view 39756648675 --log-failed | cut -c60-` (F3).
- The CI workflow `.github/workflows/ci.yml`, the test harness `test/integration/run-tests.ts`,
  `scripts/run-e2e.mjs`.

For each flake:
1. Find the race: which events can happen in which order on a slow Linux runner, and which order
   makes the assertion fail. Read the product code involved (watchers, debounce, layout observers,
   editor-group lock handling), not only the test.
2. Decide: product bug (users can hit it: e.g. a saved linked target never refreshes) → fix the
   product and add a unit test that reproduces the ordering; test bug → make the test wait for a
   deterministic signal (an event, a state flag, a ready marker), not a longer timeout.
3. F1 (visual, windowless): reproduce locally if you can (`just visual`, or a focused run of the
   okf-schema sticky-3 pages; slow the page down / throttle CPU via Playwright CDP if useful) and
   prove the fix with repeated runs.

Do not change tolerances, counts or timeouts of existing assertions to get green. A retry loop
that already exists (previewEditing.test.ts ~line 492) is a symptom: replace it if you find the
real signal.

## Gates (foreground, windowless only, in the worktree)

`npx tsc -p .`, `just check`, `just visual` (repeat the F1 pages several times). No integration,
`test:e2e` or `just preflight` locally (VS Code windows): CI proves F2/F3.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/023-ci-flaky-tests/reports/T1-r<round>.md`:
per flake: root cause (with the event order), product or test bug, fix, proof; files changed; tests
added (failed before?); gate results; open risks.
