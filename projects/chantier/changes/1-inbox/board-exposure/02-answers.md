Short name: `board-exposure`

# Answers

1. board-exposure-Q1 (2026-11-21): **Default address.** A. `127.0.0.1` by default; the local network only on the user's ask (`board.host` in `chantier.yaml`, or `--host`), and the board says it is open to the network.
2. board-exposure-Q2 (2026-11-21): **The key's life.** A. Stable, with a command to change it (`board --new-key`, which invalidates the old URL), and one rotation now (the key sits in 3 transcripts); the cookie lasts 30 days instead of a year.
3. board-exposure-Q3 (2026-11-21): **The key in the sessions' output.** B. Keep printing the full URL; rely on the rotation (Q2).
4. board-exposure-Q4 (2026-11-21): **Grilled enough.** A. Yes, specify now.
Spec critic: yes, it changes what the user sees and does (the board's access, its URL) and a security protection.
Spec critic run (2026-11-21), fixes that need no user, for the spec-writer's next run: (4) add README.md:231-232 and docs/web-board.md:8 to the Docs list (the board on this machine by default, the phone once opened to the network); (5) note the overlap with 2-backlog/P3/docs-sphinx-rtd (its "On a phone" section must say the phone first needs `board.host`/`--host`; the second to merge rebases the moved web-board.md). Findings 1, 2 and 3 go to the user.
