# A Driver's checkpoint commit carries a real message

## The request

From the retro of batch-13 (2026-11-12): CR-189 reproducible-evals committed its round 2 as a
checkpoint, "wip(evals): judge, sandbox setup and audit (round 2, one review fix pending)",
and that commit stayed in `main`'s history once the PR merged by rebase.

## What changes

- The Driver's card (`skills/chantier/references/driver.md`) says: a commit a Driver makes
  mid-CR (a checkpoint after a FIX-REQUIRED round, a round's commit) has a message in the
  project's commit style that says what the commit holds, never a `wip` type or a "pending"
  note; before the first push of the CR's branch, the Driver may fold a checkpoint into the
  next round's commit; once the branch is pushed, it does not rewrite history for that alone.
- The PR template's or the cards' wording that mentions checkpoints, if any, follows.

## Out of scope

- A CLI check of commit messages (the CLI runs no git command that changes anything and gets
  no new tool from speculation).
- Rewriting the history already on `main`.
