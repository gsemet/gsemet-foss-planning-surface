## Summary

A PR merged by rebase keeps every commit of its branch, so a mid-work commit such as `wip(evals): ... (round 2, one review fix pending)` stayed in the default branch's history. The Driver card now says that every commit a Driver makes carries a real message that says what it holds.

## Deliverables

The Driver card (`skills/chantier/references/driver.md`) gets a new "Commits" bullet in "Your means", shared by every Driver:

- every commit, a round's or a work-in-progress one, has a message in the project's commit style (Conventional Commit subject where the project gives none);
- no `wip` type, no "pending" or "checkpoint", no round or review state, no CR number, batch or role in the message;
- before the branch's first push, a work-in-progress commit that is the head may be folded into the next one with `git commit --amend`, and a `note` records it; once pushed, it stays as it is (no rewrite for a message alone);
- a commit that a procedure names (a release's `release: vX.Y.Z`) keeps that message.

The "CR driver" section's commit sentence points to this bullet.

## Blast radius

Grade: **1**. One card text changes; a plain `git revert` restores it.

## Autonomous decisions

- The rule is in the section shared by every Driver, not in "CR driver" alone, because a stack, release or QA Driver's commit lands in the default branch the same way.
- The fold uses `git commit --amend` only on the head of a never-pushed branch; no interactive rebase or reset.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the new "Commits" bullet and the pointer in "CR driver".

## Human decisions

- A Driver's mid-work commit must carry a real message, because it ends up in the default branch.

## Impacts

No visual change. Drivers write real commit messages from now on.

## Test plan

- [x] No behaviour change (card text only)
- [x] Local gates at `c9a772e`: `just check` and `just scenario` pass
- [x] Evidence: not applicable (card text)
- [x] Review: approved at `c9a772e`
- [x] Verified at `c9a772e`
- [x] CI green at `c9a772e`

## Internal references

CR-193 driver-checkpoint-commit-message.

</details>
