# Intent: the board's reading views, as in the prototype

2026-11-13, the user, in a Griller session: split from `visualization-backend` (CR 2 of 5).

## The request

The board served by `chantier board` shows the prototype's reading views: Home, Kanban, Batch
(the graph, the batch's mode, the PRs to review or still drafts), Costs, a CR's file panel, the
project picker with "All projects" (which hides the views tied to a project), and the phone
layout with its bottom bar.

## The reference: the same thing at the end

The user: "je veux la meme chose en fin d'implementation". The target is the prototype,
`1-inbox/visualization-backend/prototype/` (`index.html`, served with `snapshot.py`'s data), and
its screenshots `1-inbox/visualization-backend/evidence/prototype/v6-*`. The specification names
the views and screenshots it reproduces; the PR shows each view beside the prototype's, on PC and
on the phone. The chantier meanings the prototype follows are in
`visualization-backend/02-answers.md`, "Semantics fixed".

## Bounds

- Reading only: no write from these views (the backlog edit is `board-backlog-edit`).
- Needs `visualization-backend` (the server and its read API): `depends.json`.
- The origin and late-summary icons and the labels come from `cr-summaries`; the autosync pill
  from `surface-autosync`.
