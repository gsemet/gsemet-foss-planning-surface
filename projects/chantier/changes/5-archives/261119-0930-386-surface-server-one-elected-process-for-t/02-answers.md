# Answers

Settled by the Chief of Staff, 2026-11-18, under the user's standing word "plus de question"
(the Chief of Staff settles and informs).

1. **Scope.** A foundation only: one process, its election, one read interface. No index, no
   JSON API, no notification, no delegated action, no new wake: the drawing's dashed boxes are
   later CRs, each from measured cost.
2. **Rules kept.** The files stay the truth, in git; the server never edits a batch and never
   messages an agent; an order is always the Chief of Staff's. A delegated action, later, is an
   event the Chief of Staff records as an order, never a write by the server.
3. **The election.** The surface server holds the OS lock `<git>/chantier/hub.lock`, as the hub
   does today: one per surface and machine. A watcher that finds the lock held only reads its
   journal; with no server running, today's behaviour stays (the first watcher becomes the hub),
   so a session never depends on the server being up.
4. **One process.** `chantier board` starts the surface server: the board's pages, the forge hub
   loop and the one writer of the event journal, in one process. `board.json` and `hub.json`
   become one state file; the spec names it and what reads it (`status`, the pane).
5. **One read interface.** The board, the hub and `status` read the planning folder through one
   module (records, backlog, configuration, journal); today it reads the files on each call. No
   cache that could drift from the files in this CR; the index comes later behind the same
   interface, rebuilt from the files.
6. **AGENTS.md.** The board and forge hub exceptions become one named exception, the surface
   server, with the same limits (read-only forge reads at the same rates, the same writes). The
   PR names the change.
7. **Order.** After the addressed events CR (`addressed-events-one-typed-journal-that-`).
8. **`planning-server` (P3) stays open.** This CR takes none of its write path, sync or leases,
   and contradicts none of its answers: the server is the one HTTP server of the planning folder
   (the `remote-board` constraint), and the store stays Markdown and JSON.
9. **Proof.** A real run on the user's machine: the server up, a second `chantier board` refused
   or attached, a watcher woken by a forge merge through the server, the server killed and a
   watcher taking the hub back.

## The spec-writer's open questions, settled by the Chief of Staff, 2026-11-18

10. **Who writes the journal: the spec's reading is right.** Inside the server process the hub's
    and the board's lines go through the one append function; CLI commands keep appending through
    the same function in their own process. A server-only writer would need an API (excluded) and
    a second path when no server runs (a fallback, refused by AGENTS.md).
11. **One ask for both.** The board's ask in `session-start.md` names the forge reads; a yes
    starts the server with its hub loop. No option to run the board without the hub: no answer
    asks for it, and a user who wants no forge reads does not start the board.

## The spec critic's points, settled by the Chief of Staff, 2026-11-18

12. **The upgrade never runs two boards.** The move to `server.json` carries `board.json`'s
    `running` record over with the key, so a second board is still refused with the stop
    command; CR-384's readers of the board's version read the `server` entry.
13. **The read module leaves this CR.** The one-process election and the `store` refactor ship
    apart: `store` becomes its own CR (`one-read-interface-over-the-planning-fol`, P2 in the
    backlog, not in batch-28), whose reach is every planning-folder read the board, the hub and
    `status` reach, directly or through `commands/cost`, `autosync/reading`,
    `core/surface_batches`, `status/` and `Repo`, its structure test following those modules.
    This CR keeps the one process, the election and `server.json`; answer 5 moves to that CR.
14. **CR-375's watcher locks stay named.** The scenario's git-folder check and the AGENTS.md and
    CONTRIBUTING.md texts name `chantier/watch-<project>/<session>.lock` too.
15. **The start line as the stacked CRs leave it** (the addressed events CR and CR-384); the
    readers table adds CR-384's two readers of the board's version.
16. **A yielded watcher elects again.** It stops electing while `server.json` names a live
    server, and elects again once none is named.
17. **A failed `server.json` write.** At the server's start: a `board not started:` refusal; a
    hub entry not written: retried at the next cycle.
18. **No open question left:** answers 10 and 11 go into the spec's decisions.
