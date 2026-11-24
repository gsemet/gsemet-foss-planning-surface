## Problem

In a stack batch, change requests that were ready (verified, CI green, rebased on main) stayed in draft with no ask until the Chief of Staff pushed. `status` printed "alone asks: refused", while the owner's rule is: keep the ready change requests at the bottom of the stack and send a stack-ready-to-merge ask for that ready part at once, even for a single PR. Nothing in the CLI enforces it.

## Proposed fix

- Describe the one-PR partial-stack ask in the stack card.
- Drop the "alone asks: refused" wording.
- Have `status` flag a ready change request that has no ask.

chantier 0.15.1, Claude Code desktop app (Windows). From a batch retro.
