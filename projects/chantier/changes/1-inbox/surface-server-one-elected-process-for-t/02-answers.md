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
