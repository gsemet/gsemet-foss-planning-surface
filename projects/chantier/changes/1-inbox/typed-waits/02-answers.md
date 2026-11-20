# Answers: typed-waits (Part E)

The grill is planning-server's (`2-backlog/P3/planning-server/02-answers.md`, Q1-Q30). The
answers below settle the open questions of this CR's first specification.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

1. **Backlog waits and the hub (the reference's E.7):** no. The hub reads no forge for a
   backlog CR's waits; they are cleared by hand; AGENTS.md's query budget does not change.
2. **Order:** `plan-store-interface` (Part B) joins `depends.json`, since the backlog write goes
   through `repo.store`. `planning-server` (Part C) does not: its refusal applies through
   Part B's `check_publish` whenever it lands, with nothing to change here.
3. **A CR dropped back to the backlog:** `order drop` to the inbox or backlog writes its open
   waits to the folder's `waits.json`.
4. **The free-text `blocked waits: <what>` reason:** stays; `--wait` adds typed waits beside any
   reason.

The writer's own choices (`link` beside `ref`; a link in another repository recorded, not read,
cleared by hand; `open_waits` on the board; no pane change) are accepted.
