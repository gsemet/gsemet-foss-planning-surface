# Intent: a planning surface stays in sync through its own autosync

2026-11-13, the user, in a Griller session: split from `visualization-backend` (CR 5 of 5). The
request came from the Chief of Staff's session; its full text is
`1-inbox/visualization-backend/intake/02-surface-autosync.md`.

## The request

Option A (the user's pick): chantier owns no autosync, the surface does. The Chief of Staff, the
Foreman and a Griller join the surface's group at session start; no session commits or pushes the
surface by hand while the group is enabled. A `blocked:` group is the Chief of Staff's: upstream
moved, it integrates (never a force push); an approval, the user gives it. The CLI checks, read
only: preflight warns, status shows one line. The user's answers in the Griller session: the board
server joins the group while it runs; the user approves an incident from the board; the board
shows a blocked upstream and the Chief of Staff fixes it; with no autosync the board shows
nothing; the board server is the named git exception in `AGENTS.md`.

## The reference: the same thing at the end

The pill at the foot of the sidebar (and beside the project button on the phone) and its panel,
as in `1-inbox/visualization-backend/prototype/` and its screenshots `v6-20`, `v6-21`
(`visualization-backend/evidence/prototype/`).

## Bounds

- Needs the server (`visualization-backend`): `depends.json`. The pill's display also needs
  `board-read-views`; the cards and CLI part does not.
- Out of scope: an autosync of the code repository, porting the autosync into the CLI.
- The answers: `visualization-backend/02-answers.md`, "Autosync merged in", "Autosync and access,
  answered".
