# Intent: each CR carries a condensed JSON summary

2026-11-13, the user, in a Griller session: split from `visualization-backend` (CR 3 of 5).

## The request

Each CR folder gets a condensed JSON: its title, a short summary, its origin (a Jira, GitHub or
GitLab issue, or a verbal request; the user: "C'est le genre d'info que l'on peut mettre dans le
json rafraichi depuis l'agent"), its labels and its group (the user: labels link tickets, with a
filter at the top; groups are kept, both in the CRs' JSON). A checksum of the CR's Markdown tells
when the summary is late. The CLI gets a linter and the commands to write it; the cards say the
agent that edits a CR's Markdown runs the linter, the Chief of Staff at worst.

## The reference: the same thing at the end

On the board: the origin icon, the late-summary clock, the labels and their filter, as in
`1-inbox/visualization-backend/prototype/` and its screenshots `v6-18`, `v6-19`, `v6-22` to
`v6-24` (`visualization-backend/evidence/prototype/`). The specification names them; the PR
shows them beside the prototype's.

## Bounds

- The CLI and cards part stands alone. The board's display of it needs `board-read-views` (and,
  for the label filter in Triage, `board-backlog-edit`): the specification says whether it lands
  here after them or in those CRs. No `depends.json` for now, so the CLI part can start at once.
- The answers behind it: `visualization-backend/02-answers.md` (the md↔json sections, "Where a
  request comes from", "Labels and groups").
