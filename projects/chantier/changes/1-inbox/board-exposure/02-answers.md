Short name: `board-exposure`

# Answers

1. board-exposure-Q1 (2026-11-21): **Default address.** A. `127.0.0.1` by default; the local network only on the user's ask (`board.host` in `chantier.yaml`, or `--host`), and the board says it is open to the network.
2. board-exposure-Q2 (2026-11-21): **The key's life.** A. Stable, with a command to change it (`board --new-key`, which invalidates the old URL), and one rotation now (the key sits in 3 transcripts); the cookie lasts 30 days instead of a year.
3. board-exposure-Q3 (2026-11-21): **The key in the sessions' output.** B. Keep printing the full URL; rely on the rotation (Q2).
4. board-exposure-Q4 (2026-11-21): **Grilled enough.** A. Yes, specify now.
Spec critic: yes, it changes what the user sees and does (the board's access, its URL) and a security protection.
Spec critic run (2026-11-21), fixes that need no user, for the spec-writer's next run: (4) add README.md:231-232 and docs/web-board.md:8 to the Docs list (the board on this machine by default, the phone once opened to the network); (5) note the overlap with 2-backlog/P3/docs-sphinx-rtd (its "On a phone" section must say the phone first needs `board.host`/`--host`; the second to merge rebases the moved web-board.md). Findings 1, 2 and 3 go to the user.
5. board-exposure-Q5 (2026-11-21, critic finding 1, the spec's open question 1): **When to rotate.** A. Now, on the current version: the Chief of Staff stops the board, starts it again with `--new-key` and gives the user the new link. The spec records it as done, not as part of the CR.
6. board-exposure-Q7 (2026-11-21, critic finding 3): **Where the board says it is open to the network.** A. In its start lines, which the Chief of Staff passes on; the web client does not change.
7. board-exposure-Q8 (2026-11-21, the spec's open question 3): **The cookie's `Secure` flag.** A. Out of this CR, and no inbox item for now; the spec says why (plain HTTP: a `Secure` cookie would not reach a phone on a LAN address).
8. board-exposure-Q6 (2026-11-21, critic finding 2, the spec's open question 2; asked again in plainer words after "Pas compris. Reformule"): **Keeping the board on the phone.** The user's words: "Met l'ip dynamiquement". Read as: the setting that opens the board to the network names no fixed address; the board finds this machine's local network address at each start and listens there (so a shared `chantier.yaml` never breaks another machine's board, and a DHCP change is followed). Opening stays the user's choice (Q1).
