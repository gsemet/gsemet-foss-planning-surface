# Forge hub stays idle for a running batch: wake it for a subscribed watcher, and resubscribe after a restart

Scope narrowed by the user (pr-conflict-Q1 A, 2026-11-24): the hub and the watcher only. The detection of PRs left in conflict by a merge, with the order to rebase them, goes in a separate CR (inbox item `pr-conflict-detect-and-rebase-order`).

Seen (batch-31, 2026-11-24): `server.json` shows `hub.idle: true` and the project's `read_at` 14:33 UTC, nearly six hours old, with the same server (PID 29916, started 14:25) and two watchers of the Chief of Staff running since; a read-only board page opened in a browser, and a fresh watcher started at 20:08, did not wake it. `hub/loop.py` reads the forge only while `observed()` is true (a client subscribed to the server). The merges of CR-477, CR-479 and CR-483 were never journalled. `status` printed "watch: this session's watcher runs" next to "forge hub: idle (no client subscribed)".

Wanted: find why no client counts as observing; make the hub read the forge while a watcher of the session holds the seat; a watcher whose server restarted resubscribes, or says at once that it is no longer subscribed (never "runs" while it receives nothing); `status` tells the two apart. Earlier: a watcher ended after 2 h without events and missed CR-477's merge (CR-476 removes that limit while a batch runs).
