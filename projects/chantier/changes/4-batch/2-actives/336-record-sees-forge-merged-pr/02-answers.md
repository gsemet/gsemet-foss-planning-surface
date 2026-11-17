# Answers

No grill: a retro point of batch-24 that the user put straight into the batch.

- The user's word (2026-11-17): "remet les 5 dans le batch et on continue" (put the five retro
  points back in the batch and go on). This CR is one of the five; the user asked no question on
  it and set no behaviour.

The facts the choices rest on (batch-24):

- PR 288 (CR-330) merged at 2026-11-17T18:58:14Z into CR-329's branch
  (`chantier/batch-24/cr-329-cr`), as part of a stacked merge; its content landed on main as
  commit 75a748e8, with CR-329's PR 286. The Chief of Staff recorded CR-329 merged at 18:58:43Z.
- The board's PRs page wrote, at 21:04:28Z, the line
  `{"kind":"merged","batch":"batch-24","cr":"CR-330","into":"chantier/batch-24/cr-329-cr","into_cr":"CR-329",...}`
  in `board-seen.jsonl`, and `status` printed "board saw merged: CR-330 ... into CR-329's branch
  ...; for the Chief of Staff: not landed, tell the user, record nothing until CR-329 lands",
  though CR-329 had landed. The record kept CR-330 ready until the Chief of Staff's `order merged
  CR-330` at 21:25:26Z; meanwhile `forge-stack create` was refused (HTTP 422 on the merged PR).

Choices (no user answer covers them):

- A1 (what "landed" means): a PR merged into the branch of another CR of the batch has landed when
  that CR's PR is merged on the forge, at the same time or later, into a branch that is no CR's
  branch (the default branch), or into the branch of a third CR whose PR lands the same way
  (a chain, followed to its end). A base PR merged before the stacked PR went into its branch does
  not carry it: not landed. Settled by the Chief of Staff.
- A2 (who decides it): the board's PRs page, from the forge read it already makes (each row's
  state, base branch and merge time); no new forge call, no git read, no patch-id check. A merge
  that leaves no PR merged on the forge (a manual push to main) stays out. Settled by the Chief of
  Staff.
- A3 (the signal): the line in `board-seen.jsonl` carries what the board found (the CR the PR
  landed with, and when). A merge first seen not landed, then seen landed at a later read, writes
  one second line, once; `status` prints the landed line when there is one. Still at most one line
  per batch, CR and landed-or-not. Settled by the Chief of Staff.
- A4 (who records): unchanged. The board records nothing; `status` prints the line, and the Chief
  of Staff records it with `order merged <cr>` at the `status` that shows it, then tells the
  Foreman as for any order. The request's "tells the Foreman to record it" is read as this
  existing route (the Foreman does nothing with a `board saw merged` line). Settled by the Chief of
  Staff.
- A5 (scope): `forge-stack create` already skips a CR recorded merged; once the merge is recorded,
  its HTTP 422 goes away. No change to `forge-stack`. A stacked PR that never landed (its base
  merged first) keeps today's "not landed" line. Settled by the Chief of Staff.

- retro-Q2 (the user, 2026-11-17): the patch-id check on main stays out of scope: the forge read the board already makes, within AGENTS.md's limits; the Chief of Staff records.
