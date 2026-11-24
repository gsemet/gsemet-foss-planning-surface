# Diagnosis: two scenario checks red at f20227a

Reproduction: `just scenario` in the CR-477 worktree (units `stack` and `series-deps`, github).
Transcript: scenario/results/scenario-20261124-140458-276.md (stack check at line 7581, series-deps at 24659).

## Verdict
Both are caused by this CR, by design (spec section 2, D2: `base` on the `worktree:` line is now the
CR's place, `stack_base(..., planned=True)`, for any CR of the chain in a stack batch). Neither is a flake.
The code is right; two scenario assertions still expect the old `start_base` (`base origin/main`).
The CR already updated the sibling check 7903 for the same reason and missed these two.

## Evidence
1. stack (scenario/run_scenario.py ~7908): `handoff CR-107` printed
   `worktree: ... branch chantier/batch-06/cr-107-base-three base chantier/batch-06/cr-106-base-two`.
   CR-107 ("three") is placed by `w.chantier("stack", one, two, three)` above CR-106, so its place is
   CR-106's branch. The check wants `endswith("base origin/main")`. No PR, so no `; PR ...` suffix and no
   forge read (the `reads() == before` half is not what failed).
2. series-deps (~10430): after `stack CR-105 CR-106` and `order after CR-106 -` (a dependency removal, not a
   removal from the chain), `handoff CR-106` printed `... branch chantier/batch-06/cr-106-stack-second
   base chantier/batch-06/cr-105-stack-first` (transcript line 24623). CR-106 is still above CR-105 in
   `chain`, so the planned base is CR-105's branch. The check wants any line containing `base origin/main`.
   The first half of that check (after not in cr, order line, orders kind, 2 CRs) passed: the failure is
   only the last `and any("base origin/main" ...)` clause.
3. Diff: commands/facts.py `_base_of` now uses `_place_base` -> `stack_base(planned=True)` when
   `is_stacked(d, c)`; this is the only path that prints these lines. Other stack/series checks that
   use non-stack batches (e.g. "when the dependency is merged, the base is the default branch") pass.
Not run on origin/main: not needed, the printed lines match the new code path exactly.

## Fix (for a coder; scenario/run_scenario.py only, no source change)
1. Line ~7908-7910, check "a stacked CR with no PR prints today's line and makes no forge read":
   replace `worktree_line(out).endswith("base origin/main")` with
   `worktree_line(out).endswith(f"base {w.cr(two)['branch']}")` (keep `reads() == before`); reword the
   title, e.g. "a stacked CR with no PR prints its place's base alone and makes no forge read".
2. Line ~10433-10434, check "`order after` with `-` frees a queued CR...": replace
   `any("base origin/main" in ln for ln in w.chantier("handoff", y)[1])` with
   `any(f"base {w.cr(x)['branch']}" in ln for ln in w.chantier("handoff", y)[1])` (x is the CR below
   in the stack; the base follows the stack order, not the freed `after`).
Then rerun units stack and series-deps (`just scenario` or the unit filter the runner offers).
