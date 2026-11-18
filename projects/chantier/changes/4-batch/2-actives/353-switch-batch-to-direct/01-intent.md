# Intent: switch a Foreman batch to direct mode, with CRs in flight

On the user's word, the Chief of Staff takes over a running or paused Foreman batch and steers it
directly, whether its Foreman is alive or not. Nothing in flight is lost: queued CRs stay queued,
working CRs restart by the existing restart path, and their PRs, branches and worktrees are kept.

The case that asks for it: the Foreman of Studio's batch-06 stopped at the usage limit, with its
heartbeat 9 hours old, 5 CRs in flight and 4 PRs open. Today the Chief of Staff can neither take
over nor close without dropping the work, because a Foreman batch never becomes direct.

The switch mirrors the existing switch to Foreman mode:

- A live Foreman gets a hand-over order: it starts no Driver, notes and stops each of its Drivers,
  answers that it is done, and stops.
- A Foreman that is not answering (its heartbeat older than the batch's limit and a ping
  unanswered for 5 minutes, or the user's word) has its session stopped by the user, or by the
  Chief of Staff on the user's yes. Its Drivers are then treated as stopped from outside.
- No Driver restarts while the old one runs: two Drivers never hold one CR.
- The Chief of Staff claims the next epoch, and that claim makes the batch direct, logged in the
  batch's journal. The old epoch becomes stale (exit 3).
- `cost`, `status` and the board say "direct" afterwards. The old Foreman's calls and its Drivers'
  calls stay counted, and a replaced Foreman never blocks `close`.
- A batch switched to direct can go back to Foreman mode by the existing switch.
