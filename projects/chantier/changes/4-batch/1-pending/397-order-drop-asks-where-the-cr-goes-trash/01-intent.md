# order drop asks where the CR goes: trash, inbox or backlog

Today the only way to take a CR out of a batch is `order drop`, which sends it to `6-trash/` with
its work. Seen at batch-28's end (2026-11-19): CR-381 and CR-382 were only postponed (the user
merges them a week later), yet they went to the trash and needed a `restore` and a `triage` to
reach the backlog, losing their CR number on the way.

Wanted: taking a CR out of a batch names its destination, and the Chief of Staff asks the user
which one when the user has not said it:
- trash: the CR is cancelled (today's drop);
- inbox: to be looked at again;
- backlog `P1`..`P4`: postponed or handed off, the usual case for delegated work.

The CR keeps its work (worktree, branch, open PR) whatever the destination, and its PR is closed
only for the trash.
