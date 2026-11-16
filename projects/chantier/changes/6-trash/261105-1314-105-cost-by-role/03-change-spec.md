# The batch's cost report splits by level

## Change

- `_cost_summary` in `skills/chantier/scripts/cli/src/chantier/commands.py`: the line `Orchestration
  ... work ...` becomes one line with three amounts and shares: the Foreman, the Drivers (any agent
  that started another one), and the workers (the rest). It comes from the transcripts' parent links
  as today, and the CLI still knows no role.
- `status`, `STATUS.md` and `cost` use that line wherever the old one appeared; the docs, cards,
  eval kit and scenario follow.

## Done when

- The three amounts add up to the total, and the scenario asserts it on its fake transcripts.
- `just check` and `just scenario` pass, and CI is green at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
