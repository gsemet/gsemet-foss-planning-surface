## Problem

In one batch, Drivers handed back "blocked on context" nine times (one change request alone needed five Drivers). Each restart needed a hand-spliced brief and often a lease reclaim. The previous batch had the same problem.

## Proposed fix

- The Driver writes a checkpoint (state, next step, open runs) before its context fills, and hands back cleanly.
- `take` prints a ready brief file for the replacement Driver, rather than a block the steering session must splice by hand.
- Reclaiming the lease of the steering session's own ended Driver needs no ask.

This may partly belong upstream (host context limits).

chantier 0.15.1, Claude Code desktop app (Windows). From a batch retro.
