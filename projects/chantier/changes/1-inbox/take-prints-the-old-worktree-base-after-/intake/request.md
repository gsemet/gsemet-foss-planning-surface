# take prints the old worktree base after a stack reorder


## Problem

After a stack reorder, `take` printed the change request's old worktree base instead of the new one. It was also seen in an earlier batch.

## Proposed fix

Recompute the base from the recorded stack order at each `take`.

From the markdown-okf-schema-studio batch-09 retro (stack batch, 2026-11-24), chantier 0.15.1, Claude Code desktop app on Windows.
