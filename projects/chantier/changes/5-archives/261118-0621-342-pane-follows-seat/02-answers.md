# Answers: pane-follows-seat

## pane-Q1: how the pane picks its project on a planning surface
**Answer (option 1):** from the seat: on a surface root the pane keeps only the project whose
`changes/seat.json` names this session.

## Settled by the Chief of Staff
- With no seat naming this session (a Griller, a Foreman, a plain session), the pane shows every
  project as today, under one line saying no seat names this session.
- The stale in-project planning folder in Studio's repo is the user's to remove; this CR does not
  change the CLI's resolution (`repo.py`).
- A change to `hooks/` passes `just mod` before its PR (AGENTS.md); the PR carries a screenshot
  of the pane from a real session at its head.
- A Foreman's session is matched too: the project whose running batch names this session as its
  steering Foreman (the batch record's foreman id).
- ~~A session matches a project when its id equals either id field the record holds: the seat's
  Chief of Staff session (`seat.json`'s `session`), or the batch record's foreman id
  (`batch.json`'s `foreman`).~~ Superseded by the next point.
- A session matches on either form of id of each record, because the user's intent is that the
  pane follows the session that steers: `seat.json`'s `session` and `transcript`; `batch.json`'s
  `foreman`, `foreman_transcript` and `foreman_transcripts`.
- `batch.json`'s `chief_transcript` also matches, so a Chief of Staff known only by the batch
  record, with no seat, sees its own project.
- `batch.json`'s `chief_transcripts` also matches, the same way `foreman_transcripts` does (any
  entry of the list).
- When two projects match, the pane shows both.
