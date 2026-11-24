# Driver checkpoint and a ready restart brief on blocked context


## Problem

In one batch, Drivers handed back "blocked on context" nine times (one change request alone needed five Drivers). Each restart needed a hand-spliced brief and often a lease reclaim. The previous batch had the same problem.

## Proposed fix

- The Driver writes a checkpoint (state, next step, open runs) before its context fills, and hands back cleanly.
- `take` prints a ready brief file for the replacement Driver, rather than a block the steering session must splice by hand.
- Reclaiming the lease of the steering session's own ended Driver needs no ask.

This may partly belong upstream (host context limits). Related: `driver-context-second-cut` (cuts what a Driver reads); this one is about the restart when the cut is not enough.

From the markdown-okf-schema-studio batch-09 retro (stack batch, 2026-11-24), chantier 0.15.1, Claude Code desktop app on Windows.
