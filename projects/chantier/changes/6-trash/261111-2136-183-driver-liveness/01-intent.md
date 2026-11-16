# Intent: driver-liveness

A Driver that dies (app cut, host crash, context exhausted) must be seen by the steering session
within one or two heartbeats on any host, and restarted from the CR's recorded state with no round
counted and no extra slot. The CLI states measured facts (last activity per working CR, whether a
Driver is recorded); the Foreman card judges death and restarts; context exhaustion becomes a
named hand-back, distinct from a silent end.

Source: batch-11 retro (`.agents/changes/4-batch/retro.md`), folding the inbox items
drivers-killed-by-app-restart, dead-driver-slot and driver-context-exhaustion.

Finding from the grill: a restart does not need a second slot today. Slots count `working` CRs,
not agents (rails.py:69-71), and `take` on a working CR skips the slot check (rails.py:180-181).
The real gap is that nothing flags a dead Driver and a bare `take` is silently accepted.
