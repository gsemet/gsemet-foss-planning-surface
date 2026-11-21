Short name: `sync-lock`

# Answers

1. sync-lock-Q1 (2026-11-21): **What to do.** C. Both: dev mode only when the session's project is chantier itself (other projects run in plugin mode, their own copy of the code through `uvx --from`); and the sync names the processes that hold it and waits, for chantier's own processes (a gate, a watcher).
2. sync-lock-Q2 (2026-11-21): **A sync still blocked.** A. It waits, names the processes, never kills, and tells the user after a few minutes.
