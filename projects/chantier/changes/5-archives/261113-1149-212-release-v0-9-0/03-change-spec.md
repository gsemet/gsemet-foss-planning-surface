# Version PR for chantier v0.9.0, at the top of the batch's stack

## Goal

One PR, the top of this batch's stack, that makes v0.9.0 ready to tag: the release folder
`docs/release-notes/<date>-v0.9.0/` and the commit `release: v0.9.0` made by `just release minor`.
Its base is the stack's top CR; it covers everything since v0.8.0 on `main` plus every CR of the
stack below it. The user merges the whole stack bottom-up; that merge is the go for
CONTRIBUTING.md "Release" steps 4 and 5, run by the steering session after the merge (not by this
CR's Driver).

## Shape in this batch (before `release-cr-in-batch` is on `main`)

- An ordinary CR of the batch (not `order add --release`): today's CLI refuses a kind-`release`
  CR before the others merge (`rails.py:112`, `203-206`) and bases it on `main`
  (`commands.py:1464-1547`).
- It waits for every other CR of the batch (`order after` with all their ids, in stack order) and
  starts when they are all ready; it is stacked last, so its PR is the top of the stack, a draft
  until its base is `main`.
- If a CR below changes after this PR is open (a new round, not a pure restack), the Driver redoes
  steps 1 to 3 below at the new top: the notes must still cite every `feat:` and `fix:` once.

## What the Driver does

1. Read CONTRIBUTING.md "Release" and docs/release-process.md (the rules), then the commits since
   `v0.8.0` on `main` and every CR below in the stack (each `03-change-spec.md`, PR description
   and evidence).
2. Write `docs/release-notes/<today>-v0.9.0/` as docs/release-process.md says: `release-notes.md`
   (header, links at `v0.9.0`, two to four highlights, Smaller changes, folded All fixes and For
   contributors; every `feat:` and `fix:` commit since v0.8.0 and of the stack exactly once; N
   counted on the stack's top before the version commit), `tweet.md` (three posts), and the images
   it cites. Images come from real runs or existing docs (the board screenshots of
   `boot-mode-by-surface`, the docs diagrams of the stack's CRs); none is invented. A highlight
   with no real capture uses a CLI call and its output instead.
3. Run `just release minor` (bumps 0.8.0 to 0.9.0, runs `just check`, commits `release: v0.9.0`;
   pushes nothing), then push and open the PR; its body shows `release-notes.md`, then `tweet.md`,
   each after a `---` rule, as docs/release-process.md says.
4. Hand back ready with the PR. The Driver never runs `just tag`, `gh release create` or anything
   after the merge.

## Out of scope

- Tag, forge release and the thread (CONTRIBUTING.md "Release" steps 4 to 6): after the user's
  merge, the steering session runs steps 4 and 5; step 6 is the user's.
- Any code or card change: the version PR changes only the version files `just release` touches
  and the release folder.

## Evidence

- `just check` passes at the PR's head (it runs `scripts/release_notes.py --check`).
- `git log --oneline -1` at the head is `release: v0.9.0`; `just version` files say 0.9.0.
- A list in the PR body (or `work/`) mapping each `feat:` and `fix:` commit since v0.8.0 and of
  the stack to its place in the notes.
- No `just scenario`: the PR changes no CLI, card or scenario.
