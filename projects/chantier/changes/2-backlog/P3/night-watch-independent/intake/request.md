A batch running with the user away is watched by a wake that does not depend on a session being idle.

What happened (batch-17 night): the Chief of Staff's watch was a session cron, which fires only while the session is idle; it fired nothing from 04:20 to 07:41. The Foreman's own loop kept the batch moving, so nothing was lost that night; a stopped Foreman (context, a host error) would have stayed stopped until morning.

Wanted: a wake outside the sessions (a scheduled task of the host or the system running `status --refresh`): when the Foreman's heartbeat is older than 45 minutes and no Driver works, it wakes the Chief of Staff or sends the user a notification. Depends on what the host allows.
## After the critic's review (Fable, 2026-11-14)

A trial first, nothing built: find out why the session cron did not fire from 04:20 to 07:41 while the batch was active (124 events in the record), and whether `/loop`, the host's scheduled tasks (still "unproved", `hosts/claude-code.md:504`) or the Foreman's own heartbeat is enough as a safety net. Build only if the trial shows a real gap. Not a stack blocker; a watch outside the sessions must not write outside the planning folder (AGENTS.md).