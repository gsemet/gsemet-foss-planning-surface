# Evidence 9: `just test` seconds

Same Windows machine, other work running on it at times.

| Run | Head | Tests | pytest seconds | wall seconds |
| --- | --- | --- | --- | --- |
| base | `88d9ab40` (same tree as `ea11a9e0`) | 2933 passed, 19 skipped | 157.82 | 165.0 |
| head, `just test`, first | `b85be4cb` | 2748 passed, 19 skipped | 265.01 | 267.6 |
| head, `just test`, second | `b85be4cb` | 2748 passed, 19 skipped | 162.47 | 167.2 |
| head, inside `just check` | `b85be4cb` | 2748 passed, 19 skipped | 138.63 | not timed |

Commands: `just --justfile <worktree>/justfile --working-directory <worktree> test` (and `check`).
Logs: `work/scratch/e9-test-head.log`, `e9-test-head-2.log`, `pre-push-check.log`.

Result: the second head run against the base run is +4.65 s (pytest) and +2.2 s (wall). Runs of the same head span 138.63 s to 265.01 s, so the expected net of at most +3 s is neither proved nor disproved by these runs.
