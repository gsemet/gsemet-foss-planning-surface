# CI flaky tests — make the e2e campaign rock solid (P1, 2026-10-22)

User: "il faut que les tests soient rocket solid". A test that passes and fails on the same code is
a bug (in the test or in the product), never a reason to re-run. Fix the root cause; never widen a
tolerance or add blind retries/sleeps.

Seen on Linux CI (xvfb), unrelated to the changes under test:

| # | Test | Message | Runs |
| --- | --- | --- | --- |
| F1 | visual `capture.py` first-gap check, `okf-schema*--light--sticky-3--default` | `[read:properties] 1 control(s) of #sphinx-myst-preview-content > [data-okf-properties] sit under the toolbar` | PR #11 run 4, PR #12 run 39779674653 (despite the 17c6122 settle loop) |
| F2 | `test/integration/previewEditing.test.ts:498` | `Timed out waiting for linked target metadata to refresh after a saved change` (3 writes × 10 s) | PR #12 run 39779674653 |
| F3 | `test/integration/realInput.test.ts:3863` | `the user's lock survived: Quick Open from the locked group opened elsewhere` | main push run 39756648675 (9b5ac08) |

Ideas to check:
- F1: the settle loop compares two readings; the properties table may still change after (link
  state, badge, font). Find which control and why it moves; measure after the page signals ready.
- F2: does the linked-file watcher react to an external write at all on Linux (inotify, debounce)?
  Product bug if a saved target never refreshes the excerpt.
- F3: race between Quick Open and the editor group lock; wait for a deterministic signal.

Also: a way to detect flakes before merge (for example run the integration suites N times in a
dedicated CI job, or locally windowless where possible).

## Decisions (2026-10-22)

- User: tests must be rock solid; run CR 023 in parallel with PR #12 using a git worktree.
- Defaults taken (no grill round, user asked to start): fix all three in one CR/PR; root cause first
  (product bug fixed in the product, test bug in the test); no wider tolerance, no blind retry or
  sleep; each fix explains the race it removes.
- Local VS Code integration runs stay forbidden (the user uses VS Code): integration fixes are
  proven by reasoning + unit tests where possible, then by CI (several green runs).
