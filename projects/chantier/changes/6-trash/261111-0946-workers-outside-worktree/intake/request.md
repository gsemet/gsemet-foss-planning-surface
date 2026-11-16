# A worker cannot write outside its CR's worktree

Batch-09 retro, 2026-11-11 (`4-batch/retro.md`, point 5). The user asked for a fix strategy that
"fonctionne quand chantier sera déployé dans n importe quel type de projet", and worried that
fixes "rigidifie le process et ça augmente les coûts"; this one was kept as a zero-token guard.

## What happened

Workers wrote in the main checkout instead of their worktree: a stray edit of
`scenario/run_scenario.py`, empty `commands.py` and `state.py` at the repository's root, an
empty `chief-of-staff.md` created then deleted. Nobody saw it until a `git pull --ff-only` on
main was blocked.

## What main says today (fde3da8)

`worker.md` says a worker "works only in the CR's worktree"; nothing enforces it, and no role
checks the main checkout.

## Proposed fix (to grill)

- The plugin's Claude Code hook refuses a worker's Write or Edit outside the worktree its prompt
  names. It costs no token and holds in any project.
- The Driver checks the main checkout is untouched (`git status --porcelain` against its state
  at `take`) before its hand-back, and says so if not.
- Open: how the hook learns the worktree (the prompt, the CR record), and the Copilot host's
  equivalent.
