# Foreman's stack lease goes stale with no stack Driver, needs --reclaim


## Problem

In a stack batch, the Foreman's own stack lease went stale three times while no stack Driver was running. Each time `take stack` was refused until `--reclaim`, and the first time needed an answer from the Chief of Staff.

## Proposed fix

Take the stack lease only when a stack Driver starts, or let the Foreman reclaim its own stale lease without an ask.

From the markdown-okf-schema-studio batch-09 retro (stack batch, 2026-11-24), chantier 0.15.1, Claude Code desktop app on Windows.
