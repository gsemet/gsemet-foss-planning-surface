# Release v0.7.0

## Problem

`main` holds what batch-07 delivered since v0.6.0, and no version carries it yet.

## Change

Run the "Release" section of `CONTRIBUTING.md` for a minor version:

1. On the head of `main`, with green CI, run `just scenario` and the eval campaign `real`. A failure
   stops the release and goes to the user.
2. On a new branch, `just release minor`: the version becomes 0.7.0 and the commit is
   `release: v0.7.0`.
3. Open the PR. The user approves the merge, by rebase.
4. `just tag`, then `gh release create v0.7.0 --generate-notes`, each on the user's approval.

During the eval the main checkout does not change, neither its files nor its branch: the eval's
work and any other goes in a worktree or outside the repository.

## Depends on

Every other CR of batch-07: the release's `after` holds them.

## Out of scope

Any change of code or docs but the version; a fix goes through `order add --fix-for`.

## Done when

- `just scenario` and `real` passed on the head the version commit stands on.
- The tag v0.7.0 and its GitHub release exist, and `main` holds `release: v0.7.0`.
- `work/retro.md` is written in the CR's folder.
