# `open` and `order add` take plain paths

## Change

- `chantier open <batch> <folder-or-specification>…` and `chantier order add --note
  <folder-or-specification>` take a plain path. The `@` prefix is gone from these two commands,
  with no transition: a path starting with `@` is simply a path that does not exist.
- `chantier file` keeps `@<file>`.
- The CLI's help and errors, the cards, `README.md`, `CONTRIBUTING.md`, the eval runbooks, the
  scenario and the tests all use the new form. Past reports under `evals/results/` stay as they are.

## Done when

- On Windows PowerShell, `open` with an unquoted path works, and a wrong path names the path.
- `just check` and `just scenario` pass, and CI is green at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
