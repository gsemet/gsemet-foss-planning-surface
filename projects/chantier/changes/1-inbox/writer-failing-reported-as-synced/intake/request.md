# The writer fails every cycle while status and preflight say synced

## The owner's word (2026-11-27)

To the Chief of Staff's question "shall I note the writer's failure, while the status said synced, as a CR?": « Oui, note-la ».

## What happened (2026-11-27, local times)

Reported by the Chief of Staff of markdown-okf-schema-studio (its message to chantier's Chief of Staff and its session's own report):

- The surface's writer failed at every cycle from 09:10 to 09:34 (38 cycles), with: `…\projects\agentic-planning-surface is not inside a git repository (the surface)`.
- `status` said "synced" meanwhile.
- The failing board was PID 29916, started on 2026-11-24 by an earlier session. The same git check worked from that session's terminal. That the old process was the cause is its suspicion, not proved.
- It also saw that the board's last forge read for its project dated from 08:26.
- On the owner's word the board was restarted (new PID 6568); commit 6ea8c613 of the surface, at 09:34, published the pending changes, chantier's included.

Seen by chantier's Chief of Staff during the failure: `preflight` printed "P13 ok   the surface's writer runs: synced, pushed 09:07", and `sync` printed "writer: synced, pushed 09:07", while the surface held unpublished changes.

## What is asked

A writer that fails is reported as failing, by `sync`, `status` and `preflight`, and nothing says "synced" while changes stay unpublished. To settle in the grill, with the cause of the failure.

Not grilled.
