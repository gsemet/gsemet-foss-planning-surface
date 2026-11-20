# Driver context: a Driver reaches ready without a context hand-back

Priority P1. Batch-29 retro point, measured across the batch (2026-11-20).

Nearly every Driver of batch-29 handed back blocked on context near 100-120k tokens, before its CR closed (CR-401, 402, 404 three times, 405, 407, 409 twice, 410, 412): each hand-back costs a fresh Driver, a re-read and often a lost lease. The Foreman measures the first read of `driver.md` at about 100k tokens of the Driver's budget; the card alone is 124 KB (about 30k tokens), so the rest comes from the cards and files it pulls in with it.

Measure what a Driver reads before its first round (cards, references, the CR's files), then cut it: a short startup core for the Driver with the full card read only for the action that needs it (as the Chief of Staff's startup manifest does), and no card re-read after a hand-back. Done when a Driver takes a three-round CR to ready without a context hand-back, measured on a scenario CR.
