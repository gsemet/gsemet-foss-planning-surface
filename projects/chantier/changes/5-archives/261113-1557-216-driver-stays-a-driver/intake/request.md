A Driver does work that belongs to its workers (edits through the shell, `git reset --hard`, a stray `round`) and runs out of context. Fix: the Driver delegates, keeps large outputs in files, its write guard covers the shell, a reset goes to a worker, `round` refuses an empty round.

Merged on 2026-11-13 from the batch-15 retro items below (the user's word: "regroupe en moins de CR").

## From `driver-context-exhaustion`

Batch-15 retro: the Drivers of CR-200 and CR-208 ran out of context with no hand-back, and 8 Drivers were restarted on a CR that already had one. Fix: measure a Driver's context and keep large outputs (gate logs, diffs) in files it reads in part.

## From `driver-no-shell-writes`

Batch-15: CR-200's Driver, out of context, patched costs.py itself through PowerShell and damaged a docstring. The Driver's no-edit rule also covers shell writes, and the write guard names it.

## From `driver-reset-hard`

Batch-15: CR-212's round-3 Driver ran 'git reset --hard' in its worktree after a coder's botched attempt (nothing pushed lost). The Driver card says whether a Driver may reset its worktree, and if not, that a dirty worktree after a failed coder goes to a new coder or a conflict-resolver.

## From `stray-round-call`

Batch-15 retro: a stray 'round' call spent a round of CR-211 before any work. Fix: 'round' refuses a new round with no commit or note since the previous one, or the Driver's card says when to call it.
