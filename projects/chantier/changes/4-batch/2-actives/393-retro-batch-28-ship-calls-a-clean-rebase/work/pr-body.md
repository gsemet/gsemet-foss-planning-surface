## Summary

After a clean restack, `ship` could print `the rebase changed the patch` and refuse to carry the long gate and the verdict, although the patch-ids of the change's own commits were equal. The carry check counted the wrong commits as the change's own, because the base a head sits on was looked up among only three branch names. In a stack, none of them names the branch just under the head during a restack. This PR makes the base the nearest branch under the head among every branch of the batch and the default branch, and makes the refusal say why.

## Deliverables

Where the base of a head is read (`head_base`, `commands/carry.py`):

| | Before | After |
| --- | --- | --- |
| Candidates | start base, PR base as last read, planned place | those three, plus the default branch tip, plus each other non-cancelled batch branch (remote tip and local tip) |
| Rule | nearest candidate that is an ancestor of the head | unchanged |
| Restack of C onto B (on A), PR base still `main` | base `main`: range holds A and B commits, "changed" | base B: only C's own commits, carries |

Refusal texts (`commands/crs.py`):

- `the rebase changed the patch (own commits: 1 at <g7> above <gbase7>, 2 at <h7> above <hbase7>)` when the counts differ: a miscounted base shows at once.
- `the rebase changed the patch (commit <i> of <n> differs)` when the counts are equal.
- `git could not read the patch-ids of <base7>..<head7>: <git's first stderr line>` when a git call fails, instead of reading an empty list as "changed".

## Blast radius

Grade: 1. The change is local to the carry check and the base lookup; a plain `git revert` restores the previous behaviour, where a carry is refused and a new gate and review run.

## Autonomous decisions

None.

## Known gaps

- A head judged before this change merges, whose gate or verdict event recorded too low a base (the default branch instead of the branch below), still does not carry at its next move; it gets a new long gate and a review once. From the next judgment on, the recorded base is the nearest branch.

<details>
<summary>Details</summary>

## Changes

- `head_base` takes every non-cancelled batch branch (remote and local tip) and the default branch tip as candidates; `Base.branch` stays the branch name and the function stays read-only.
- `_patch_ids` checks both git processes; `carry_check` names a git failure and gives counts or the first differing commit when the patch changed.
- The Driver card's long gate paragraph states the base rule and that unequal counts are an anomaly to report, not a reason to verify again.
- Tests in `test_carry_ship.py` and `test_gate_carry.py`: the carry in the batch-28 shape (pushed, local only, three branches), the base recorded at judgment, a real change still refused with its counts, and a git failure named.

## Impacts

No visual change. A clean restack in a stack carries the gate and the verdict; a refused carry says whether a base was missed.

## Test plan

- [x] New or changed tests (they fail on the previous code): 8 of the 29 tests in `test_carry_ship.py` and `test_gate_carry.py` fail on the previous code and pass at `960cdb8`
- [x] Local gates at `960cdb8`: `just check` pass, `just eval-dry-run` pass (18 of 18)
- [x] Evidence: none, no visible change
- [x] Review: approved at `960cdb8` (carried from `d64a996`: same patch, clean rebase)
- [x] Verified at `960cdb8`
- [x] CI green at `960cdb8`: check, eval-dry-run and scenario pass (`scenario` is the long gate)

## Internal references

- CR-393 retro-batch-28-ship-calls-a-clean-rebase

</details>
