# `order qa` is refused once the budget is spent

## Change

- `skills/chantier/scripts/cli/src/chantier/commands.py`: `order qa` calls the existing
  `check_budget` before it creates anything. Past the budget it fails with that error and
  `EXIT_BUDGET`: no folder in the inbox, no order in the state, no event.
- Within the budget, or with no budget, `order qa` behaves as today.
- `skills/chantier/references/foreman.md` and `chief-of-staff.md` change only if a sentence becomes
  false. `CONTRIBUTING.md`, which lists what `rails.py` refuses, follows if needed.
- `scenario/run_scenario.py`: a check that a spent budget refuses `order qa` and leaves no folder,
  and that raising the budget (`order budget`) lets it through.

## Done when

- `just check` and `just scenario` pass, on GitHub and GitLab, and CI is green at the PR's head.

## This PR is never merged

This CR is an eval of chantier with the real tools. It stops at an open PR.

- Open the PR as a draft.
- The first line of its body is exactly: `**Eval run: do not merge.** The maintainer decides what happens to this PR.`
- Nobody merges it, marks it ready, or enables auto-merge: not a Driver, not the Foreman.
