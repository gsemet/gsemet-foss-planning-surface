# Rules (implementer and reviewer)

- Worktree /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-040, branch `test/real-window-registry`. Do not commit, push, stash, or change branches (the CR driver commits).
- Never install or use the network: no `just dev`, `just update`, `npm ci/install`, `uv sync`,
  `fnm install`, pip.
- Windowless gates: `npx tsc -p .`, `npm run test:unit`, `just check`, `just visual`, foreground,
  leave nothing running.
- Real-window tests (integration, `test:e2e`) are allowed tonight, ONE run at a time across all CRs:
  take the lock with `set -o noclobber; echo "CR 040 $(date +%H:%M)" > /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/WINDOW-TESTS.lock`;
  if it fails, wait (slices of at most 5 min) and retry; `\rm -f` the lock when done, even on failure.
  Never `just preflight`.
- Only touch files the task needs. Never touch `.agents/changes/` except your report/review file.
- Style through the stylesheet only, never inline `style=`. Light, dark, cream and current-theme must
  all stay readable.
- Never widen or weaken an existing test to make it pass; an updated assertion keeps its intent.
  New tests must fail on the unchanged code.
- Implementer report: `reports/T1-r<round>.md` (files changed, what you did, tests added and their
  failure before the change, changed assertions and why, gate results with counts, screenshot paths,
  open points). Reply with a 5-line summary.
- Reviewer: read-only except `reviews/T1-r<round>.md`; first line exactly `Verdict: APPROVE` or
  `Verdict: FIX-REQUIRED`, then findings (severity, file:line, concrete fix). You may run
  `npx tsc -p .` and unit tests, and open screenshots with Read. Reply with the verdict + 3 lines.
- `rm`, `cp`, `mv` are aliased to `-i`: use `\rm`, `\cp`, `\mv`. Never let a command wait for input.
