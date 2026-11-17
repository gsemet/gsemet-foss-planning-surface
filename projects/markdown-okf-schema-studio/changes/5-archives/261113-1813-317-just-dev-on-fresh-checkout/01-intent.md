# Run `just dev` first in a new worktree or a clean checkout

Type: docs. Filed 2026-11-13 by the Chief of Staff.

## Owner's words

> Oui il faut faire un just dev quand on commence dans un worktree ou un checkout propre

## Why

In batch-03 the release driver's first gate in a new worktree failed with "tsc not found": a
worktree has no `node_modules` (gitignored), and the main checkout had none to link.

## Scope

- `.agents/guidelines/local-worktree.guidelines.md` and "Setup" in `AGENTS.md`: run `just dev`
  first when starting work in a new worktree or a clean checkout, before any check or gate.
- No code change.
