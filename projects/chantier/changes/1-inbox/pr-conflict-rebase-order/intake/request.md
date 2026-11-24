# Server detects PRs left in conflict by a merge and orders the rebase

The server must detect a batch's PRs or MRs that a merge leaves in conflict, and send the order to rebase them.

From the user, 2026-11-24, after merging CR-479 and CR-483: a merge should trigger a scan of the batch's open PRs or MRs, so the server detects those now in conflict and sends the order to rebase them.

Seen (batch-31): after PR 459 and PR 460 merged (20:04 UTC), PR 457 (CR-481) became CONFLICTING/DIRTY on the forge, and nobody was told: the board's PR page reads the conflict state for display (board/prs.py) and no order follows; the hub's journal knows only git sync conflicts of the planning surface (sync-conflict@1), not PRs.

Second finding, to fix with it: the Chief of Staff's watcher received no merge event for CR-479 and CR-483. The hub reported "idle (no client subscribed)" after the server restarted (hub PID 18292 to 29916, after CR-478 `board-restart`); the watcher was still told running. A watcher whose server restarted must resubscribe, or say it is no longer subscribed; earlier, a watcher ended after 2 h without events and missed CR-477's merge (CR-476 removes that limit while a batch runs).

To grill: what the order is (a journal line the watcher carries, then the Foreman starts a rebase Driver, or an `order` the CLI applies); which PRs (the running batch's ready and open ones); the rebase voids the long gate and the Verifier's verdict, so what the Driver owes after it; how the forge's "mergeable" state, computed late by GitHub, is polled; the resubscription of a watcher.

Evidence added 2026-11-24 20:10 UTC, after restarting the watcher: server.json's `hub` entry shows `idle: true` and the project's `read_at` 2026-11-24T14:33:38Z, nearly six hours old, although two watchers of the Chief of Staff ran since 14:30 and the board page was opened in a browser meanwhile (read-only link). A fresh watcher started at 20:08 did not wake the hub within a minute either. So the forge hub does not read the forge for a running batch with open PRs, whatever client subscribes: merges of PR 459 and 460 (20:04) were never journalled. This is the first thing to find before any conflict scan: why the hub stays idle (same server since 14:25 UTC, PID 29916, started by a session that held the seat; the build is the other build of 0.15.1). Check at the same time `status`'s hub line ("idle (no client subscribed)").
