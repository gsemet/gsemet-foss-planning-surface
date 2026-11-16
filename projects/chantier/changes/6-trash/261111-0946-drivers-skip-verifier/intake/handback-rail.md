# Addition, 2026-11-11: `handback ready` refuses without a passed gate and a verdict at the head

Batch-09 retro (`4-batch/retro.md`, point 6). The user, after hearing the cost concern: "Le 6
oui je le veux." Asked how it works: "Donc, le CLI donne les portes à passer comme des check
list c est ca ?", then "C'est traduis sous quelle forme dans un fichier ? Un json".

## New facts since the first request

CR-164's Driver skipped a second Inspector after a fix; CR-167's and CR-169's Drivers skipped
the last Verifier pass on the PR description. `handback ready` checks only that the CR has a PR.

## What main already records (fde3da8)

- `gate` appends to `events.jsonl` an event with `result` (pass or fail), `head` (the short SHA
  of the worktree's HEAD) and `command`.
- `ship` stores `pr` and `head` in the CR's record in `batch.json`.
- A Verifier's verdict is free text only (a note, `04-result.md`): the CLI cannot read it.

## What the user agreed to

- Two gates, no more: the project's long gate passed at the PR's head, and a verdict
  `VERIFIED` at the PR's head. Every other step stays the Driver's judgement.
- A new CLI command records a verdict as a structured event, e.g. `verdict CR-x VERIFIED`,
  reading the head from the worktree itself: `{"event": "verdict", "cr": ..., "result":
  "VERIFIED", "head": ...}`. The CLI knows a verdict, not a role.
- `handback CR-x ready` looks in `events.jsonl` for both at the head `ship` recorded and refuses,
  naming the missing one.
- `take` prints the gates up front, as a checklist.
- A project that declares no long gate has no gate 1. All of it stays plain JSON in the
  planning folder.
