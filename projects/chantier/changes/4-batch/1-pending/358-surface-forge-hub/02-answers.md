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

## The spec-writer's open questions, answered by the user (2026-11-18)

- **hub-Q5, the hub's cadence:** B. The hub reads the forge every 20 s, not 10 s: half the calls,
  a merge seen up to 20 s later. (The board's own PRs page keeps its 10 s limit.)
- **hub-Q6, the Foreman on `checks red`:** A. It records nothing and starts no Driver on it; a live
  Driver of that CR gets it as a `note`.
- **hub-Q7, paused batches:** A. The hub follows running batches only; a PR merged while the batch
  is paused is seen at the next `status` or on the board, with no wake.

## The spec-critic's questions, answered by the user (2026-11-18)

- **hub-Q8, the overlap with `session-events-board-griller`:** A. This CR replaces that item's
  forge and merge part (its `chantier watch`, its forge reads, its replacement of
  `board-seen.jsonl`). That item keeps only the board events (moves, notes, Configuration) and is
  specified again on top of the hub, with the same journal and the same `watch`.
- **hub-Q9, consent at start:** A. The Chief of Staff asks once per session before starting the
  watcher, as for the board, saying it runs on, reads the forge of every project on the surface
  every 20 s, and needs the network. A no starts nothing: merges go back to the user's word.
- **hub-Q10, hubs of different chantier versions:** A. `status` and the watcher's start line name
  the hub's version ("hub is chantier <v>") when it differs from the session's, and the session goes
  on. No hand-over, no hub per version.

## Settled by the Chief of Staff (after the spec critic)

- CR-354 (in batch-26) forbids background tasks that wait: the watcher is named as an exception
  next to the board, in concepts.md rule 8 and in foreman.md's new sentence (its start, its restart
  after each end, and that it stops itself). This CR rebases on CR-354.
- A `forge saw merged` line is checked on the forge before `order merged` by both paths: the
  watcher's end and the next `status`.
- The watcher also starts after a paused batch resumes and after the switch to direct mode, when no
  watcher of this session runs.
- References fixed: `stacks.ready_word`; "the `board_prs` checks inside `remote_board`". The Driver
  cites the forge documentation for `headRefOid` and `diffHeadSha` in the PR.

## Settled by the Chief of Staff

- A red CI on a ready PR is told to the user and, in Foreman mode, relayed to the Foreman; the
  Chief of Staff records nothing for it.
- The Chief of Staff starts its watcher while its project has a running batch, and starts it again
  after each wake; with no running batch it starts none.
- The journal is local to the machine and ignored by git; `board-seen.jsonl` folds into it.
- A merge recorded twice (two machines, or the board and the hub) is harmless: `order merged`
  already answers "already merged".
