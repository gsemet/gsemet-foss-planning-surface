# Intent: the board edits the backlog

2026-11-13, the user, in a Griller session: split from `visualization-backend` (CR 4 of 5).

## The request

The board's Triage view as in the prototype: post-its, drag-and-drop between the inbox, P1 to P4
and `3-ready` (moving a folder is what changing a priority means), groups, labels and their
filter, "New" (a new idea filed in the inbox, nothing more; issue intake from GitHub or GitLab is
automatic and elsewhere), editing a CR's Markdown, the "next batch ready" marker. Every write goes
through the CLI's role-free commands, at once, with a toast; a journal lists what the board wrote
since the user last said "rescan" to the Chief of Staff. The board never messages the Chief of
Staff. No batch editing: the user, "edition = uniquement le backlog".

## The reference: the same thing at the end

`1-inbox/visualization-backend/prototype/` (the Triage view) and its screenshots
`visualization-backend/evidence/prototype/v6-*` (Triage, the journal, labels: `v6-22` to
`v6-24`). The specification names them; the PR shows each beside the prototype's, on PC and on
the phone.

## Bounds

- Needs the server (`visualization-backend`) and the views' frame (`board-read-views`):
  `depends.json`.
- The rules: `visualization-backend/02-answers.md`, "Scope answers", "Editing is the backlog
  only", "The "+ Intake" button becomes "New"", "The prototype as cleaned".
