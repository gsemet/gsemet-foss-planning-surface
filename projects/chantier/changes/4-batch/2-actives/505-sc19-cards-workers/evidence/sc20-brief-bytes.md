# SC20 evidence: brief bytes, old and new

Run: `work/coder3/briefs_drivers.py` (`$CHANTIER brief <role> --batch batch-31 [--cards <staging>]`, bytes of the printed file with LF). Deviation: a Driver brief with a unit needs a live `--lease`, which this run has not got, so each brief is the role-only one (no unit, so no facts of a CR). The facts block of a real run is a little larger.

The staging step (until child 24): for each role, a folder holding `driver.md` (a copy of the card), `floor.md`, `topics/` and `topics.json` of `cards-next/`, refreshed before each run.

| role | old brief | old reading (the spec) | new brief | boot target | result |
| --- | --- | --- | --- | --- | --- |
| cr-driver | 59,216 | 44 KB for a CR Driver | 7,541 | 6 KB | over by about 1.4 KB |
| stack-driver | 59,216 | 56 KB | 7,493 | 6 KB | over by about 1.3 KB |
| release-driver | 59,216 | 28 KB | 7,317 | 5 KB | over by about 2.2 KB |
| qa-driver | 59,216 | "no run" | 5,598 | 4 KB | over by about 1.5 KB |

The old brief of each role is the same file (the whole old Driver card with its sections); the old readings are the spec's figures for what the role read in a run, not this table's.

Cause of the overshoot: the cards are within their targets (3,280, 3,232, 3,056, 1,337 bytes), and a brief is card + floor + facts + host rows + closing. The host rows block alone is 3,414 bytes and the floor and facts add about 1.4 KB, all set by `roles.yaml` and the floor, which this round may not change. With the cards at their targets (4,096, 4,096, 3,072, 2,048) the briefs would still be about 8.4, 8.4, 7.3 and 6.3 KB: the 6, 6, 5 and 4 KB targets cannot be met by the cards alone. Known gap, for child 25.

Real run not done (child 28): no Driver ran on these briefs.
