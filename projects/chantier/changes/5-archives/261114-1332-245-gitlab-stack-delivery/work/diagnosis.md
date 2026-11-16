# Diagnosis: GitLab `forge-stack show`, "merged into the branch below" case (CI run 43583196446)

Bug is in the CLI, not in the fake or the scenario. Found by reading, not by running a partial scenario.

## Cause
`forge_stack_gitlab.show()` (skills/chantier/scripts/cli/src/chantier/commands/forge_stack_gitlab.py, line 156) reads
the default branch from a fresh Repo:

    default = open_repo().config["default_branch"]

`open_repo()` returns a Repo whose `config` is `DEFAULT_CONFIG` (core/repo.py line 24: `"default_branch": None`).
The batch's settings (default_branch "main", written by `chantier open`) are copied into a Repo's config only by
`apply_batch_settings` (core/batch.py lines 54-61), which runs in `read_batch` (batch.py line 236) and in the `Batch`
context. `forge_stack._plan()` (forge_stack.py line 80) calls `read_batch` on ITS OWN Repo instance, so that
instance has "main", but `show()` opens a second Repo that never had the settings applied. So `default` is `None`.

The CI line shows it: `merged into chantier/batch-08/cr-114-forge-piece-a, not None: folded into CR-114`.
The text is otherwise right (cause, folded-into CR). The scenario expects `not main`
(scenario/run_scenario.py line 3740), so the check fails only on the word `None`.

Only this case uses `default`: `_check_1` compares `target != default` solely for a merged MR (lines 86-89). With
`default` None every merged MR would be reported as folded, even one merged into main. All other GitLab checks
(closed, wrong target, foreign MR, draft, check 5) never read it, which is why 690/691 pass. This would hit a real
GitLab too, so it is a product bug, not a test artifact. The GitHub path does not use this code.

## Files and lines to change
1. forge_stack_gitlab.py line 156 (`show`): stop calling `open_repo()` there.
2. Source the default from the batch-aware Repo. Simplest, with a small footprint: `_plan()` in forge_stack.py already
   computes each row's `base` with `stack_base(data, c, repo, planned=True)`, and the first row of the chain is on
   the default branch. Cleaner and explicit: have `_plan` also put the default in the data it returns, e.g. add
   `"default": repo.config["default_branch"]` to every row dict (forge_stack.py lines 96-107), and in `show()` use
   `default = rows[0]["default"]` (rows is never empty: `_plan` raises NoBottom otherwise).
   Alternative without touching `_plan`: thread `args` into `gitlab.show/make` and call `read_batch` there; heavier.

Keep `_check_1`'s signature (`default: str`) unchanged.

## Fix to apply
- forge_stack.py `_plan`: add `"default": repo.config["default_branch"],` to the row dict.
- forge_stack_gitlab.py `show`: replace line 156 with `default = rows[0]["default"]`; drop the now unused
  `open_repo` import (line 17) if nothing else uses it (ruff would flag it).
- No scenario or fake change. Optionally harden `_check_1` against a None default (it cannot be None once fixed).
- Rerun only section 13a GitLab leg (or `just scenario` in the queued gate): the case should print
  `!202 merged into <branch(a)>, not main: folded into <a>` and 691/691 pass.

## Not verified by running
Section 13a was not run here (the long gate is queued; I did not touch the lock). The cause is established from code:
the log's `not None` can only come from `config["default_branch"]` being the unset DEFAULT_CONFIG value, and the only
reader on that path is the fresh `open_repo()` in `show`.
