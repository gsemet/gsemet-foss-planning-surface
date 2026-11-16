# The steering session fast-forwards a clean main checkout after each merge it records

## The request

Batch-14's retro: the price of `claude-fable-5-2` merged (commit `3dc912f`), but the main
checkout stayed at an older commit, so `chantier cost` went on leaving that model's calls
unpriced. The request: the steering session fast-forwards a clean main checkout after each merge
it records, never touching untracked files, and not during an eval, when the main checkout must
not change.

## The problem

- In this repository the plugin runs in place: the cards and the CLI are read live from the main
  checkout (AGENTS.md, CONTRIBUTING.md "Set up"). A merge on the forge changes nothing there
  until someone pulls, so a batch that fixes chantier keeps running the unfixed chantier.
- In any project, the main checkout falls behind the default branch as the batch merges: the
  user's files show old code, and whatever reads the project from there (its `AGENTS.md` through
  `chantier rules`, the user's own tools) reads the past.
- Nobody owns the step. The cards give the steering session one git duty in the main checkout,
  the cleanup of merged CRs before `pause` (`foreman.md`: "Never code, review, commit, rebase,
  push…"), and `concepts.md` rule 8 says the user's uncommitted changes are never touched. The
  CLI runs no git command that changes anything.

## What would fix it

After the steering session records a merge (`order merged`, the Foreman's or, in direct mode,
the Chief of Staff's), it brings the main checkout to the default branch's new head, by a
fast-forward only and only when that is safe: the checkout is on the default branch, has no
change to a tracked file, and git can move it without touching an untracked file. In any other
case it does nothing and says why in one line. A project's rule can forbid it; this repository's
rule already does during an eval.

## What it touches

- `foreman.md` (the list of what the Foreman never does, and its git duties) and
  `chief-of-staff.md` (direct mode, the reports, the table of what needs the main checkout).
- `concepts.md` if "the main checkout" needs the new duty named; `status-layout.md` if the
  report gains a line.
- `scenario/` (the batch's flow changes: `just scenario` must show it) and the eval kit's audit
  where it reads the main checkout.
- Not the CLI: the agent runs git.

## Out of scope

- Anything but a fast-forward: no reset, rebase, stash, checkout of another branch, or clean.
- Reloading the plugin or the session's cards after the fast-forward: a card loads at the next
  session or with `/reload-plugins`, as today.
- A planning surface's own checkout, which the cards already keep in step with its remote.
- A new CLI command for it.
