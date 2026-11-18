# One forge hub per surface and machine, and watchers that wake each session

The user (2026-11-18): the Chief of Staff should see on its own that a PR merged, with no word from
the user. A small buffer of about 20 s lets a stack that is merged in one go give one wake.

The design must hold when one planning surface carries several projects. Today that is chantier,
markdown-okf-schema-studio, okf-schema and agentic-planning-surface. Each project may have its own
Chief of Staff session and its own batches, and a surface may be shared between machines through
autosync. CRs added to a running batch, and new batches, must be followed with no relaunch.

## Today

Only the board's PRs page reads the forge, at most every 10 s, and only while it is open in a
browser and for the batch it shows. For a merge the record lacks, it appends one line to
`board-seen.jsonl`, and `status` prints that line. Nothing wakes the Chief of Staff.

## Chosen by the user: option 2, a hub per surface and machine

- **The hub.** One process per planning surface and machine is elected by a lock, on the model of
  the leader election that the surface's autosync already does. It is the only reader of the forge.
  It covers every project and every running batch of the surface, and it re-reads the record at
  each cycle, so CRs added mid-batch and new batches are covered. If it dies, the next watcher that
  starts takes the lock.
- **The journal.** The hub appends events to a local JSONL journal, ignored by git. This extends
  `board-seen.jsonl`.
- **The watchers.** Each session runs `chantier watch --project <p>` in the background. The watcher
  reads only the journal, from its own cursor, and never the forge. It ends at the first event of
  its project once 20 s have passed with no newer event. The end of the task wakes the session,
  which records, relays and starts the watcher again.
- **No coordination between machines.** For merges, the forge is the source of truth, and
  `order merged` already answers "already merged" to a merge recorded twice.

## Options set aside

- One watcher per session, each reading the forge: N reads of the forge, and nothing shared.
- The board's server as the hub: the board would have to run at all times, and its exception in
  `AGENTS.md` would need to grow.
- A store like beads (https://github.com/gastownhall/beads): SQLite or Dolt as the source of truth,
  with an `events:watch` stream. Dolt breaks "uv is the only tool", and it would replace the plain
  JSON and Markdown record. What option 2 takes from beads is one writer that holds the truth and an
  event stream that clients follow.

## To settle in the grill

- Which events the hub follows. Proposed: merges, plus CI turning red on a ready PR. Alternatives:
  merges only, or review comments as well.
- What the Chief of Staff records on its own after checking a merge on the forge. Proposed: a
  merge that landed on main. A merge into another CR's branch is only reported to the user, as
  today.
- Whether the buffer is 20 s with no new event, which grows while a stack keeps landing (proposed),
  or a fixed 20 s after the first event.
- The new exception in `AGENTS.md`, since today only the board reads the forge. The measured cost
  that justifies it is one round trip with the user per merge.

## Noted in passing

Beads uses hash IDs so that agents creating items at once never collide. CR-xxx numbers could
collide if two machines file CRs at the same time. This is a separate subject.
