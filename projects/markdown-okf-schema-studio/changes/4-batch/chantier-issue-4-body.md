## Problem

In a stack batch, the Foreman's own stack lease went stale three times while no stack Driver was running. Each time `take stack` was refused until `--reclaim`, and the first time needed an answer from the Chief of Staff.

## Proposed fix

Take the stack lease only when a stack Driver starts, or let the Foreman reclaim its own stale lease without an ask.

chantier 0.15.1, Claude Code desktop app (Windows). From a batch retro.
