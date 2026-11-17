# T1 — CI stability

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-041 (branch `fix/ci-stability` from origin/main ebe7b2b). Work ONLY there;
`node_modules`/`.venv` are symlinks: never delete or stage them. Read `00-request.md` and `rules.md`.

## Change

- First collect the failures: the latest CI runs on main after ebe7b2b (gh run list --branch main),
  and the failing jobs of the 10 merged PRs' last runs; list each distinct failure with its log
  excerpt in the report.
- For each: find the root cause (race, missing wait on a real readiness signal, shared state between
  scenarios, ordering), fix the test harness or the product, never a bigger sleep/timeout.
- `.github/workflows/ci.yml`: `timeout-minutes` per job (decision 4); keep ci.guidelines.md rules.

## Tests

- Each fix explains why the test failed and why the new wait is deterministic.
- Integration/e2e cannot run locally now (the user is using VS Code): CI on the PR is the gate; a
  flaky test must pass 3 CI runs in a row (re-run the integration job twice after green) before
  "ready".

## Gates

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual` locally; CI for the rest.

## Docs

CHANGELOG only if user-visible (likely none). ci.guidelines.md: add the timeout rule if it is generic.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/041-ci-stability/reports/T1-r<round>.md`.
