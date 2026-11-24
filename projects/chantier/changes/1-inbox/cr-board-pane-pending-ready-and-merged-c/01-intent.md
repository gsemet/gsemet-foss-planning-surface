# CR board pane: the running batch's states, links, services and stats

Merges two inbox items (user, 2026-11-24, Q1 A of `board-pane`): `cr-board-pane-pending-ready-and-merged-c` and `cr-board-pane-this-batch-s-merged-crs-bo`. Both texts are kept in `intake/` (the second as `intake-2-this-batch-merged.md`).

Wanted, in one CR, states first:
1. The pane shows the running batch's CRs by state (pending, working, ready to merge, merged), the `3-ready` CRs and the CRs merged in the running batch. A finished batch must not look empty.
2. Then, in the same CR: the web board's URLs when a board runs (the user only: they hold the key), the state of the watcher and the surface server (running or not, PID, build), a few stats of the batch.

The PR's Deliverables carry one screenshot of the pane from a real session at the PR's head (AGENTS.md).
