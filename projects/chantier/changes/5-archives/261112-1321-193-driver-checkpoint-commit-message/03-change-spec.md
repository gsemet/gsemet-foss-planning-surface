# Change Specification: a Driver's checkpoint commit carries a real message

## Goal

From the retro of batch-13 (2026-11-12): CR-189 reproducible-evals committed its round 2 as a
checkpoint, `wip(evals): judge, sandbox setup and audit (round 2, one review fix pending)`, and
that commit stayed in `main`'s history once its PR merged by rebase. A PR merged by rebase keeps
every commit of its branch, so every commit a Driver makes is a commit of `main`. The Driver's
card must say so: every commit a Driver makes mid-CR has a real message, in the project's commit
style, that says what the commit holds; a checkpoint may be folded into the next round's commit
only while the branch has never been pushed.

## Where things stand (origin/main, d6271d4)

- `skills/chantier/references/driver.md`, the section shared by every Driver (the bullets of
  "Your means"), already makes the Driver the owner of git: "Git and the forge are yours: the
  worktree, the commits, the rebase, the push, the PR". Its bullets cause mid-CR commits without
  saying anything about their message:
  - "Rebase first ... Never `git stash`: the stash is shared by every worktree, so set work aside
    with a commit."
  - "The long gate ... is refused (exit 2) on a dirty tree: a gate binds to a commit, so commit
    first."
  - "Push: a plain `git push -u <remote> <branch>` when the remote branch is an ancestor of your
    head, `git push --force-with-lease -u <remote> <branch>` only for a rewrite (a rebase)."
- The section "CR driver" commits each approved round ("All approved: commit with nothing
  changed since the review (stage the files the round changed by name, `git add -- <paths>`,
  never `git add -A` or `.`) and record `note <cr> "r<n> approved at <head from the JSON>,
  committed as <sha>"`, rebase, ...").
- `skills/chantier/references/pr-template.md` gives the PR title's style: "The title says what
  changes; where the project's rules give no style, a Conventional Commit subject (`feat: …`,
  `fix: …`)."
- No card, agent file, doc or scenario check on origin/main mentions "checkpoint" or "wip"
  (`git grep -n -i -E "checkpoint|wip" origin/main -- skills agents com.github.copilot scenario
  tests README.md CONTRIBUTING.md docs` matches only a binary PNG). So the PR template and the
  other cards have no checkpoint wording to follow; they are not changed (see Decisions taken).

## What changes

One file: `skills/chantier/references/driver.md`. The Driver edits no card itself: a `coder`
makes the change, as for any CR.

### 1. A new bullet in "Your means", right after the "Push:" bullet's paragraph

The bullet applies to every Driver (CR, stack, release, QA). Its content, to be written in the
card's style (short sentences, no new term), close to this wording:

> - Commits: a PR merges by rebase with every commit of its branch, so each commit you make is a
>   commit of the default branch. Every commit you make, a round's commit or a checkpoint (work set
>   aside before a rebase, a commit before a gate, a commit after a `FIX-REQUIRED` round), has a
>   message in the project's commit style (its rules; where they give none, a Conventional Commit
>   subject, as for the PR title in [pr-template](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/pr-template.md)) that says what the commit holds.
>   Never a `wip` type, never "pending", "checkpoint", a round or a review state, never a CR
>   number, a batch or a role. Before the branch's first push, a checkpoint that is your head may
>   be folded into the next round's commit: stage that round's files by name, then `git commit
>   --amend -m "<a message for both>"`, and note it (`note <cr> "r<n> folded into <sha>"`). Once
>   the branch is pushed, or when the checkpoint is not your head, it stays as it is, with its
>   real message: never a rewrite for a message alone (a rebase onto the base is still the
>   ordinary rule). A commit a procedure names (a release's `release: vX.Y.Z`) keeps the
>   procedure's message.

### 2. The "CR driver" section's commit sentence

In "All approved: commit with nothing changed since the review (stage the files the round
changed by name, ...)", add after "never `git add -A` or `.`" a short reference to the rule,
for instance: "with a message as in 'Commits' above". Nothing else in the sentence changes; the
`note <cr> "r<n> approved at <head from the JSON>, committed as <sha>"` stays, with the `<sha>`
of the folded commit when a fold happened.

### Not changed

- `skills/chantier/references/pr-template.md`, `worker.md`, `concepts.md`, `foreman.md`,
  `chief-of-staff.md`: no checkpoint wording there (see "Where things stand").
- `agents/*.md` and `com.github.copilot/agents/*.agent.md`: they hold no contract and do not
  mention commits' messages; their bodies stay identical on both hosts.
- `scenario/run_scenario.py`, `tests/test_structure.py`, the CLI (`skills/chantier/scripts/cli/`).

## Out of scope

- A CLI check of commit messages: the CLI runs no git command that changes anything and gets no
  new tool from speculation.
- Rewriting the history already on `main` (CR-189's commit stays).
- Squashing a CR's commits at the merge, or any change to the merge method (rebase).
- A review step (Inspector, Verifier) that judges commit messages.

## Evidence

At the pushed head of the CR's branch:

1. `git grep -n -E "Commits:|commit --amend|wip" -- skills/chantier/references/driver.md` shows
   the new bullet in "Your means", with the fold before the first push and the no-rewrite rule
   after it; `git grep -n -i "checkpoint" -- skills/chantier/references/driver.md` shows it named
   only in that bullet.
2. `git diff origin/main -- skills agents com.github.copilot scenario tests` touches
   `skills/chantier/references/driver.md` only.
3. `git log --format=%s origin/main..HEAD` on the CR's own branch: no subject with `wip`,
   "pending", "checkpoint", "round" or a CR number (the CR follows its own rule).
4. `just check` passes (Linux, macOS and Windows in CI).
5. The long gate: `just scenario` passes (the change touches a card, AGENTS.md).

## Decisions taken

The user decided nothing beyond `02-answers.md`; these points it left open are decided here.

1. The rule goes in the section shared by every Driver ("Your means"), not in "CR driver" alone:
   a stack, release or QA Driver's commit lands in `main` the same way. The "CR driver" section
   only points to it.
2. The message also carries no CR number, batch, round, review state or role: these are internal
   references, kept out of the PR's title and body text by `skills/chantier/references/concepts.md`
   ("A CR's name"), and a commit message outlives the PR in the same way. CR-189's "(round 2, one
   review fix pending)" is the case.
3. Where the project's rules give no commit style, the fallback is a Conventional Commit subject,
   the same as the PR title's in `pr-template.md`.
4. The fold is `git commit --amend`, only when the checkpoint is the head commit and the branch
   was never pushed; no interactive rebase (forbidden: it opens an editor) and no `git reset` to
   reach an older checkpoint. A checkpoint that cannot be folded this way keeps its real message.
5. A fold is recorded with a `note`, so the `committed as <sha>` of an earlier note that no longer
   exists is explained in the CR's record.
6. A commit whose message a procedure fixes (a release's `release: vX.Y.Z`) keeps it: the
   project's procedure ranks above the card.
7. No scenario assertion is added for the card text: the rule is the Driver's judgment, not a
   mechanic of the CLI; the evidence is the grep at the pushed head and the long gate.
8. `pr-template.md` and the other cards are not changed: they hold no checkpoint wording.
