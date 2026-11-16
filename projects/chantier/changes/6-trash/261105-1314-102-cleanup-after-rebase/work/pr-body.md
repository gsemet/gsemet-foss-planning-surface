**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Why

After a rebase or squash merge, the branch tip is not an ancestor of the base, so the
`git branch -d` the Foreman card asked for refuses every merged CR. Each batch would stop on it.

## Change

- `skills/chantier/references/foreman.md`: the merged CRs' cleanup first confirms on the forge
  that the CR's PR is merged, then runs `git worktree remove <path>` and `git branch -D <branch>`
  from the main checkout. A dropped CR's branch still waits for the user's word at `close`.
- `skills/chantier/references/chief-of-staff.md`: the "Never" line on `git worktree remove` and
  `git branch -D` is scoped to a dropped CR, so it no longer contradicts the Foreman's cleanup.
- `scenario/run_scenario.py`: `remove_merged` uses `-D` too, to stay in line with the card.

## Proof

`just check` passes. A throwaway repository with a bare remote shows `git branch -d` refusing
after a rebase merge and the card's steps removing the branch. That proof simulates the merge
locally: no real forge was used. `just scenario` was not run.
