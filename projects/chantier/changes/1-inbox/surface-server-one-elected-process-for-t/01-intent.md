# Intent

The user, 2026-11-18, during batch-28 (drawing: `intake/architecture.svg`):

- One server in front of the watchers buffers, filters and limits their wakes. It is the one in
  an election to be the only owner of a planning surface, and routes to the right watchers by
  role and by project.
- It reads the files, and will soon get a persistence to be faster (Dolt?).
- It watches the PRs and messages the Chief of Staff, and could do the same to a Driver or the
  Foreman.
- It serves the HTML pages, and could serve an API too.
- It could notify the user of the events where they must act, and take delegated actions (answer
  some questions, change a batch's slots or budget).
- "Don't do all of that, but let us lay solid bases to allow it later: one or two foundation CRs."

This CR is the second foundation. It stacks on the first, the addressed events
(`addressed-events-one-typed-journal-that-`).

## What exists today

- `chantier board`: a web server behind a key, its own process, its PID in
  `<git>/chantier/board.json`; it edits the backlog and the roles' configuration; its PRs page
  reads the forge and appends `merged` lines.
- The forge hub: among the watchers of a surface on one machine, the one holding the OS lock
  `<git>/chantier/hub.lock` reads the forge every 20 s and appends to each project's journal;
  `<git>/chantier/hub.json` holds its PID and last reads.
- Both read the planning folder's JSON and Markdown on each request, each its own way.

## Related: `planning-server` (P3, 2026-11-10)

The older P3 item asks for a `chantier serve` that does every write of the surface, its commits,
rebases and pushes, with the Chief of Staff as its guarantor. Its answers keep everything in
Markdown browsable on the forge, set a database as the store aside ("on l'écarte pour
l'instant", on Dolt), and its constraint from `remote-board` says: one HTTP server per planning
folder, any page goes into `chantier board`. This CR is a first step toward it and keeps those
answers: the files stay the store; an index, if one comes, is a cache rebuilt from them. The
write path, the sync and the leases stay `planning-server`'s.

## The foundation asked

One elected process per surface and machine, the surface server, that holds `hub.lock` and runs
the board, the forge hub and the event writing in one place, and reads the planning folder
through one read interface, so an index (SQLite, Dolt) can come later behind it. Built now: the
one process, the election, the one read interface over the files. Not built: the index, the JSON
API, user notifications, delegated actions, new wakes.
