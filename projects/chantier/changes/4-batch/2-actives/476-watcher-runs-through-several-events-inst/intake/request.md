# Watcher runs through several events instead of exiting on each

Priority P1, next batch (the user, 2026-11-22). Seen in batch-30.

The session watcher exits after each event and prints the command to start it again (`watch --after N`); the Chief of Staff restarts it after every merge, about twenty times in batch-30. Intent: measure its cost and let one watcher run through several events while a batch runs, waking the session per event, within the AGENTS.md bounds (2 h without an event, seat lost).
