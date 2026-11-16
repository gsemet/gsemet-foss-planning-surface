**Eval run: do not merge.** The maintainer decides what happens to this PR.

`order qa` now calls `check_budget` before it creates anything. Past the budget it fails with that error and `EXIT_BUDGET`: no folder in the inbox, no order in the state, no event. Within the budget, or with no budget, it behaves as before.

- `skills/chantier/scripts/cli/src/chantier/commands.py`: the budget check in the `qa` branch of `order`.
- `scenario/run_scenario.py`: `qa_on_head` checks that a spent budget refuses `order qa` and leaves no folder, and that `order budget` lets it through. That order takes O-1, so the QA order is now O-2.

`foreman.md`, `chief-of-staff.md` and `CONTRIBUTING.md` are unchanged: no sentence in them became false.

Checks at this head: `just check` (25 passed) and `just scenario` (GitHub and GitLab).
