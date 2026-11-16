# The Foreman's cleanup works after a rebase merge

## Change

- `skills/chantier/references/foreman.md`: a merged CR's local branch is removed in a way that works
  when the project merges by rebase or squash. The Foreman first confirms on the forge that the
  CR's PR is merged, then deletes the branch with `git branch -D`. A dropped CR's branch still
  waits for the user's word at `close`.
- `skills/chantier/references/chief-of-staff.md` and any other card or doc that describes this
  cleanup agree with it.

## Done when

- No card still tells an agent to use `git branch -d` on a merged CR.
- A throwaway repository proves it: after a rebase merge, `-d` refuses and the card's steps remove
  the branch. The proof is in the CR's `evidence/`.
- `just check` passes, and CI is green at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
