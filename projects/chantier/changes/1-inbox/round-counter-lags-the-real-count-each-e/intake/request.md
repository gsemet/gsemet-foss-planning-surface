# Round counter lags the real count; each extra round needs its own grant


## Problem

In one stack batch, three change requests ran out of rounds; each needed a separate order from the Chief of Staff to grant more. The round counter was also wrong: the round event of one change request recorded round 4 while the Driver was running its sixth round.

## Proposed fix

- Count rounds exactly from the round events.
- Let a steering session apply a grant the owner gave as a standing word (for example "extra rounds are yours to decide") without one order per change request, while still recording it.

From the markdown-okf-schema-studio batch-09 retro (stack batch, 2026-11-24), chantier 0.15.1, Claude Code desktop app on Windows.
