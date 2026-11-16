Driver liveness and restart (batch-11 retro; folds the inbox items drivers-killed-by-app-restart, dead-driver-slot and driver-context-exhaustion).

1. A dead Driver goes unseen. The desktop app was cut while four Drivers ran: their agents died with no signal, and only the Chief of Staff noticing that no worktree file had changed for 40 minutes revealed it. The Foreman's heartbeat should see that a taken CR's Driver is gone (a last-activity time in `status --refresh`, or its agent id gone) and restart it from `handoff` with `take --note "resume: ..."`, with no round counted.
2. A dead Driver keeps its slot. A `take` on a CR that already runs is accepted and only records the note, so the dead Driver holds its slot until the Foreman takes it again: `status` should flag a taken CR whose Driver is gone, and the restart must not need a second slot.
3. Context exhaustion has no name. CR-182's Driver ran out of context mid-flow and handed back "not ready, restart me": the card has no name for this end, so the Foreman applied the "second silent end is blocked" rule by judgement. A context-exhaustion hand-back should be a named case in the Driver and Foreman cards (state left in the CR folder, the Foreman restarts a fresh Driver, no round counted), distinct from a silent end.

Generic: must work for any project and host, no hard-coded host detail.
