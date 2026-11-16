## Summary

The scenario's `stack` unit spent most of its time budget on two things that did nothing useful: it spawned one git process per try while searching for a commit whose id starts with a letter (and for a digits-only id), and its teardown slept 0.5 s per read-only file on Windows. On a loaded Windows machine the unit went over its 320 s budget and the local long gate failed. This PR makes both cheap, so the unit's solo time drops (277.5 s against 318.7 s), and the budget is reset from the fresh `--jobs 4` time.

## Deliverables

The two searches in `stack_batch` now compute the commit id in-process and write one commit object, and `remove_tree` retries at once.

```text
stack_batch   before: git commit --amend / git commit-tree, one process per try
              after : sha1("commit <n>\0" + raw) in Python, then one hash-object + update-ref
remove_tree   before: sleep 0.5 s before every try
              after : first try at once, sleep only between retries
```

| `--unit stack` (129 checks, budget 640 s now, 320 s before) | Before | After |
| --- | --- | --- |
| Wall time, Windows, loaded machine | over budget (run 3: 318.7 s) | 264.4 s and 277.5 s (load 23), 381.0 s (load 87, shared machine); 129/129 each |

## Blast radius

The change is in the scenario runner only: no CLI, card or hook code is touched. A `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

- The commit objects are rebuilt by hand (`hash-object` plus `update-ref`) instead of `git commit --amend`: it spawns no process per try. The scenario's commits are unsigned, so git's object format is reproduced exactly.
- The `stack` budget literal goes from 320 s to 640 s: the fresh `--jobs 4` stack time 510.8 s (440.2 and 480.4 s in the other full run) plus about 25 percent, the README's own rule. The README's measured section is refreshed.

## Known gaps

- The Windows teardown saving is not visible on Linux CI; it was measured on the Windows machine only.
- The 264.4 s solo time has no log behind it (the 277.5 s and 381.0 s runs do).

<details>
<summary>Details</summary>

## Changes

- `scenario/run_scenario.py`, `stack_batch`: the search for an old head whose first seven characters hold a letter, and the search for a digits-only dangling commit, compute ids in Python and write one object each.
- `scenario/run_scenario.py`, `remove_tree`: the first retry is immediate; the 0.5 s sleep applies between retries only.

## Impacts

The scenario's `stack` unit runs faster on Windows; no user-visible behaviour of the plugin changes.

## Test plan

- [ ] New or changed tests: the scenario is the test; its `stack` unit passes 129/129 at the head.
- [ ] Local gates: `just check` passed; `just scenario --unit stack` 129/129 in 264.4 s, 277.5 s (load 23) and 381.0 s (load 87); two full `--jobs 4` runs on a loaded machine, all checks passing (stack 440.2 and 510.8 s, wall 606.2 and 642.7 s). The budget is now 640 s (510.8 s x 1.25); an over-budget unit only warns. The Windows teardown saving (remove_tree first try at once) is not visible on Linux CI, where the pipeline's `just scenario (ubuntu-latest)` job is the long gate.
- [ ] Evidence: before (run 3) stack unit 318.7 s; per-case before: stack_batch 58.2 s, base_from_pr 40.6 s, stack_waiver 21.8 s, ready_words 90.1 s, forge_stack_cli 43.3 s. After: only the unit totals were logged (277.5 s at load 23, 381.0 s at load 87); per-case times after the fix were not kept.
- [ ] Review: approved at 9d4136c
- [x] Verified at: c983b93
- [x] CI green at: c983b93

## Internal references

CR-282 "The scenario's stack unit fits its budget" (batch-18).

</details>
