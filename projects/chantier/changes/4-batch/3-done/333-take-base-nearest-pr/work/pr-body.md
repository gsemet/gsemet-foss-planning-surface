## Summary

In a stack batch, the pull requests used to form a tree: later changes were based on branches with no pull request yet, merges moved those bases, and several restack runs were needed. `take` now bases a change on the nearest earlier change of the batch that already has a pull request, else on the default branch, and one stack-driver run at the end of the batch sets the final order of the stack.

## Deliverables

The base rule, before and after, for a change taken in a stack batch:

| Situation at the first `take` | Before | After |
| --- | --- | --- |
| Earlier change is a draft with a PR, no two changes ready yet | default branch | that change's branch |
| Change right before it has no PR, an earlier one has | default branch | the earlier change with the PR |
| No earlier change has a PR | default branch | default branch |
| Earlier change cancelled or merged | skipped | skipped |
| Fix, release, parallel or series batch | unchanged | unchanged |

```python
def start_on_for(b_data, c):
    # stack batch, not a release or a fix, no open dependency:
    # branch of the candidate with the highest order below c's that has a PR, else None
```

Choices: the rule applies to stack batches only; the in-batch stack-driver runs keep the stack current as before (a newly ready change is still moved below the drafts); only the run at the batch's end (the final-order take) may reorder freely, once every non-release change has handed back and before the release's take.

## Blast radius

Grade: 2

The start base of every new change in a stack batch changes, and the cards that drive the stack change with it. Rolling back is a revert; changes already started keep their recorded base.

## Autonomous decisions

- New scenario checks live in a new `stack_start_base` function called at the end of the existing stack case, so no new case is registered and the unit's budget is reused.
- `ready_top` was removed: no caller was left.

## Known gaps

- The full `just scenario` was run on the stack unit only (172 of 172 checks pass); the other units and the Windows run at the batch's top are still due.

<details>
<summary>Details</summary>

## Changes

- `stacks.py`: `start_on_for` returns the nearest earlier candidate's branch that has a PR; `ready_top` removed; docstrings rewritten. `records.py`: comment on `start_on`.
- Cards: `concepts.md` (Stack, Dependencies), `foreman.md` (take bases, new final-order take bullet), `driver.md` (CR driver base paragraph, stack driver Ordering sentence, new final-order take paragraph).
- `scenario/run_scenario.py` and `scenario/README.md`: the old check reworded, six new checks.

## Human decisions

- One linear stack on the forge: `take` bases on the nearest earlier change with a PR, and one run at the batch's end owns the final order.
- In-batch runs stay, a ready change above drafts is still moved below them during the batch.
- A queued change that cannot start (dependency blocked or cancelled) does not hold back the final-order take and goes into the ask to the user.

## Impacts

No visual change. Maintainers see stack PRs based on the nearest earlier PR.

## Test plan

- [x] New or changed tests: scenario checks 1 to 6 in the stack unit (no unit test asserted the old rule)
- [ ] Local gates at `f86dc23` (carried from f86dc23 over clean rebases to `fb66da3`): `just check`, `just scenario --unit stack`
- [ ] Evidence: none, no visible change
- [x] Review: approved at `f86dc23` (carried from f86dc23)
- [x] Verified at `47abe26` (carried from 47abe26)
- [x] CI green at `fb66da3`: all five jobs pass

## Internal references

- CR-333 take-base-nearest-pr
- `.agents/changes/` archive: not in the PR

</details>
