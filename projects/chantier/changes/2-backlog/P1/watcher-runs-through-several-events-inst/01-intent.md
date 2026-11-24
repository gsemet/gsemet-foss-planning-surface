# Watcher runs through several events instead of exiting on each

Short name: `watcher-limit`. The user's words of 2026-11-22 (P1, next batch), seen in batch-30.

The Chief of Staff's watcher (`chantier watch`) ends 20 s after each event and prints the command that starts it again; in batch-30 the Chief of Staff restarted it about twenty times, once per merge. It also ends 2 h after its start with no event, which takes the board it started down during a long CI wait or the owner's merge pause (four restarts by hand in Studio batch-09). Intent: one watcher runs through several events while a batch runs, waking the session at each, and has no 2 h limit while a batch runs or is paused with open PRs (2 h otherwise); it always ends when the project's seat is another session's. AGENTS.md's sentence on the watcher's end and its orphan guarantee are rewritten to match. Folds in the first half of the inbox item `watcher-ends-after-2-h-with-no-event-don`.
