# Change Specification: run `just dev` first in a new worktree or a clean checkout

Type: docs. Written by the Spec-writer, 2026-11-13, from `intake/request.md`, `01-intent.md` and
`02-answers.md`.

## Owner's words

> Oui il faut faire un just dev quand on commence dans un worktree ou un checkout propre

## Why

In batch-03 the release driver's first gate in a new worktree failed with "tsc not found". A
worktree has no `node_modules` because it is gitignored. The guideline's symlink pointed at the
main checkout's `node_modules`, and the main checkout had none.

## The rule

Every agent or person who starts work in a new worktree or a clean checkout runs `just dev` there
first, before any build, check, test or gate (`just compile`, `just check`, `just preflight`,
`just ci-*`, `just e2e` and any `npm`/`uv run` command).

## Changes

### 1. `.agents/guidelines/local-worktree.guidelines.md`, section "One worktree per change"

- Replace the two dependency lines of the code block (`ln -s "$PWD/node_modules" ...` and
  `(cd ../<repo>.worktrees/<id> && uv sync --group requirements)`) with one line:
  `(cd ../<repo>.worktrees/<id> && just dev)`.
- Change the intro sentence "dependencies symlinked, never staged" so it says that each worktree
  gets its own dependencies from `just dev`, and that they are never staged.
- Replace the paragraph under the block (the `uv sync` paragraph) with a short one. It says:
  - `just dev` runs first in a new worktree or a clean checkout, before any build, check, test or
    gate;
  - it installs the worktree's own `node_modules` (`npm ci`) and Python environment (the
    `requirements` group included), so `uv run --no-sync --group requirements okfreq` still runs
    CI's okfreq there;
  - the worktree does not symlink `node_modules`, because `npm ci` would replace the main
    checkout's `node_modules` through the symlink.

**Why the symlink is removed (decided by the spec, recommended).** CONTRIBUTING.md says
`npm ci` replaces `node_modules`. If `just dev` ran through a symlink, it would wipe and reinstall
the main checkout's dependencies, and a main checkout without `node_modules` is the failure this CR
fixes. The coder lists this as an autonomous decision in the PR body.

### 2. `AGENTS.md`, section "Setup"

Add one bullet after the `just dev` bullet:
"In a new worktree or a clean checkout, run `just dev` first, before any build, check, test or
gate; see [local-worktree.guidelines.md](.agents/guidelines/local-worktree.guidelines.md)."
Do not change any other bullet.

## Out of scope

- No change in `src/`, `test/`, `tests/`, `scripts/`, `sphinx/`, the `justfile`, `package.json`,
  the lock files or `.github/`. `just dev` keeps its current recipe.
- No requirement change: no StRS or SwRS is added or edited, `requirements/tiers/log.md` gets no
  entry, and no `@implements_req`/`@tests_req` marker moves. This is process text with no product
  behaviour.
- CONTRIBUTING.md is not changed. Its Setup text already says to run `just dev`.

## Acceptance checks

1. `grep -n 'just dev' .agents/guidelines/local-worktree.guidelines.md` shows the rule (first, in
   a new worktree or a clean checkout, before any build, check, test or gate) and
   `(cd ../<repo>.worktrees/<id> && just dev)` in the code block.
2. `grep -n 'ln -s' .agents/guidelines/local-worktree.guidelines.md` returns nothing.
3. In `AGENTS.md`, `sed -n '/^## Setup/,/^## Main targets/p' AGENTS.md` shows the new bullet, and
   the bullet links to `.agents/guidelines/local-worktree.guidelines.md`.
4. `git diff --stat origin/main...HEAD` lists only `AGENTS.md`,
   `.agents/guidelines/local-worktree.guidelines.md` and this CR's own files under
   `.agents/changes/`.
5. `just preflight` passes, run in the change's worktree after `just dev` (this also tests the
   rule).
6. Evidence: "no visible change". The change is process text only.

## Commit

One commit of type `docs`, with no scope. Scopes are for `fix` and `feat` only, per
`.agents/guidelines/git-commit-allowed-scopes.md`. For example:
"docs: run just dev first in a new worktree or a clean checkout".
