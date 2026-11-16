# `cost` counts the steering session's own subagents on their own line

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`, point 9). Linked to the user's remark on the
orchestration ratio: "Attention je pense que tu as pris ta session entière alors qu'on a
enchaîné les batch dans la même session".

## What happened

The Chief of Staff's own `Explore` subagent, started with no CR, was counted under "Driver
Explore", which overstates the Drivers and understates the steering.

## Proposed fix (to grill)

An agent with no CR taken for it belongs to the steering session (or to grill and
specification, by the window CR-165 defined), on its own line.
