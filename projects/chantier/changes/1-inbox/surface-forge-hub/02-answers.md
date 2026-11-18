# Grill answers: surface-forge-hub (short name `hub`)

Grilled with the user on 2026-11-18. The design is option 2 of `intake/request.md`: one hub per
surface and machine, a local JSONL journal, one watcher per session.

- **hub-Q1, events followed:** A. Merges, plus CI turning red on a PR that is ready to merge. Review
  comments are not followed.
- **hub-Q2, what the Chief of Staff records on its own:** A. After checking it on the forge, a merge
  that landed on main is recorded with `order merged` with no word from the user (in Foreman mode
  its line is sent to the Foreman, as today). A merge into another CR's branch (a stack) is only
  reported to the user, as today.
- **hub-Q3, the buffer:** A. The watcher ends once 20 s have passed with no newer event of its
  project, so the wait grows while a stack keeps landing, and a stack merged in one go gives one
  wake.
- **hub-Q4, AGENTS.md:** A. A new named exception for the hub: it reads the forge, read-only, with
  the user's own `gh` or `glab`, justified by the measured cost of one round trip with the user per
  merge. The board's exception is left as it is.

## Settled by the Chief of Staff

- A red CI on a ready PR is told to the user and, in Foreman mode, relayed to the Foreman; the
  Chief of Staff records nothing for it.
- The Chief of Staff starts its watcher while its project has a running batch, and starts it again
  after each wake; with no running batch it starts none.
- The journal is local to the machine and ignored by git; `board-seen.jsonl` folds into it.
- A merge recorded twice (two machines, or the board and the hub) is harmless: `order merged`
  already answers "already merged".
