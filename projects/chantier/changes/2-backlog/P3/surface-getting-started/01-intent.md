# Intent: getting started on a new, empty planning surface

From `intake/request.md` (the user, 2026-11-20, priority P3), and CR-404's decision on an unset
`origin/HEAD`. No grill was held: the user delegated tonight's spec questions ("plus de
question"); the open choices are listed as questions in `03-change-spec.md`, each with a
recommendation the specification is written on.

## Where it comes from

CR-404 (planning server, archived as
`5-archives/261120-1534-404-planning-server/`) settled that the surface's writer reads the
surface's default branch from `origin/HEAD` only. When `origin/HEAD` is unset (a hand-made remote,
a fresh `git init` pushed by hand: a `git clone` sets it, a `git remote add` does not), the writer
blocks as `not-a-branch` with the text "the default branch cannot be read (origin/HEAD is unset):
run `git remote set-head origin -a` in the surface's checkout"; no default branch is guessed
(settled by the Chief of Staff, PR body of CR-404, round 4).

That refusal is correct but a newcomer meets it on the first day, with nothing that walked them
there.

## What the user wants

1. **A getting-started guide** for turning chantier on for a new project on a new, empty planning
   surface: create the surface repository, its first commit and push, set the default branch,
   the project's folder and its `chantier.yaml`, the `planning:` line in the code repository's
   `AGENTS.md`, start the surface server (`chantier board --seat`) and check its `writer:` line,
   and what the first `open` needs.
2. **Where the surface's branch comes from.** Besides `origin/HEAD`, the branch the writer writes
   to can be stated explicitly (in the surface's `AGENTS.md` or its `chantier.yaml`), or read from
   the checkout's tracked branch (its upstream). These are explicit sources, not a fallback: with
   none of them set, the refusal stays, and its message names all three ways to fix it. The guide
   shows them.

## Bounds

- No guessed branch: no `main`/`master` default, no "the branch HEAD is on" unless a named source
  says so.
- The code repository's default branch (`opening_record`, `orders`, `batch.json`'s
  `default_branch`) is not this CR's subject.
