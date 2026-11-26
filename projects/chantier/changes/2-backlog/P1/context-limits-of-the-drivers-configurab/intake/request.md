# Context limits of the Drivers: configurable, 200k, one list

The Drivers hand back `blocked context` far too early, and the limits that decide it cannot be seen or set in one place. Owner's word (2026-11-25): "ça devrait être 200K pour être tranquilles; ces settings devraient être configurables, ou au moins documentés pour que je regarde facilement si elles sont cohérentes."

Today the numbers live only as prose in the cards, repeated in several places: `driver.md` (hand back `blocked context` at 130,000 tokens; the closing hand-off at 115,000 at `VERIFIED`, 130,000 otherwise; the closing adds about 15,000), the stack driver's rule (130,000), `foreman-lost-driver.md` (115,000). Nothing in `chantier.yaml`, no single list.

Wanted:
- The thresholds become settings in `chantier.yaml` (shipped defaults in `config/chantier.defaults.yml`, project override as for the other limits), default raised to 200,000 for the hand-back and a matching closing threshold (the closing margin stays a named value).
- `round`, `note` and the stack's `context:` line print the thresholds they use, so a Driver reads the number from the CLI and not from a card sentence; the cards say "the hand-back threshold" and name no figure.
- One place that lists every such limit with its value and source (a section of a doc, or `chantier config` output), so the owner can check them for coherence: context thresholds, rounds, slots, budget, lease and heartbeat times, watcher wake times, specifying.parallel.
- The Foreman's own thresholds and the watcher's `events.wake_every` are in the same list.
Out of scope: the model's real window; a measured cost is welcome in the PR (how often a Driver handed back `blocked context` in batch-31: five times by 2026-11-25, at 68k to 97k, under a 100k limit the Chief of Staff had asked for).
