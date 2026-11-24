Bug: round counter lags the real round count, and every extra round needs its own grant

## Problem

In one stack batch, three change requests ran out of rounds; each needed a separate order from the Chief of Staff to grant more. The round counter was also wrong: the round event of one change request recorded round 4 while the Driver was running its sixth round.

## Proposed fix

- Count rounds exactly from the round events.
- Let a steering session apply a grant the owner gave as a standing word (for example "extra rounds are yours to decide") without one order per change request, while still recording it.

chantier 0.15.1, Claude Code desktop app (Windows). From a batch retro.
