# Rules (coder and reviewer)

- Worktree /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-048, branch `fix/local-undo-macos`. Do not commit, push, stash, or change branches (the driver commits).
- Never install or use the network: no `just dev`, `just update`, `npm ci/install`, `uv sync`,
  `fnm install`, pip. Exception only if `00-request.md` allows a named dependency.
- `node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them.
- Windowless gates: `npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`, foreground,
  leave nothing running.
- Real VS Code window tests (integration, `just ci-stress`): ONE run at a time across all CRs:
  `set -o noclobber; echo "CR 048 $(date +%H:%M)" > /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/WINDOW-TESTS.lock`;
  if it fails, wait (slices of at most 5 min) and retry; `\rm -f` the lock when done, even on
  failure. Run with `env -u ELECTRON_RUN_AS_NODE`. Never `just preflight`.
- Only touch files the task needs. Never touch `.agents/changes/` except your report/review file.
- Style through the stylesheet only, never inline `style=`. Light, dark, cream and current-theme
  stay readable.
- Never widen or weaken an existing test. New tests must fail on the unchanged code. No fixed sleeps.
- Coder report: `reports/T1-r<round>.md` (files, what, tests and their pre-fix failure, gate
  counts, screenshot paths, open points). Reply with a 5-line summary.
- Reviewer: read-only except `reviews/T1-r<round>.md`; first line exactly `Verdict: APPROVE` or
  `Verdict: FIX-REQUIRED`, then findings (severity, file:line, fix). Review the round diff.
- `rm`, `cp`, `mv` are aliased to `-i`: use `\rm`, `\cp`, `\mv`. Never let a command wait for input.
- Everything in the repo and on GitHub in English; PR for an external reader (no internal ids in
  the text; "Internal references" last section if needed); "Autonomous decisions" section.
