## Summary

In a stack batch, a new change request used to start on the nearest earlier request that had a pull request, even when that request was still being worked on and had rounds to come. The new one then built on code that could still change, and a manager had to correct the base by hand. Now `take` starts a request on an earlier one's branch only once that one is handed back `ready`; otherwise it starts on the default branch. A request that declares `after` starts on its highest open dependency's branch. The base `take` prints is where the worktree and the pull request really sit.

## Deliverables

The base `take` chooses for a new stack request:

| Situation | Before | After |
| --- | --- | --- |
| Nearest earlier request with a PR is `ready` | its branch | its branch |
| Nearest earlier request with a PR is working or blocked | its branch | default branch |
| A `ready` request sits below a working one | the working one's branch | default branch (the walk stops at the first PR) |
| Request has an open `after` | dependency's branch, unless a request with a PR sits above it | highest open dependency's branch, always |
| Taken request whose start branch's owner has ended | printed the branch of a request below | default branch, until the stack driver places it |

Impactful choices:

- A request that needs the code of one still working says so with `after`; otherwise requests start side by side on the default branch and the final-order take orders them. This narrows the earlier "nearest earlier PR, whatever its state" rule and keeps its two goals: one linear stack set at the batch's end, never a branch with no PR as a base.
- A taken request stays where it was put until placed: the printed base never claims a base the worktree was not put on.
- A request with several open dependencies not stacked on one another is left as today (the highest one's branch).

## Blast radius

Grade: **2**. The base rule is shared by `take`, the board's "on" column, off-place checks and the `base:` line; the rule is covered by parametrised tests and scenario steps, and a `git revert` restores the previous rule, but already-taken requests would then print their old bases.

## Autonomous decisions

- Scenario steps 13, 13-bis and 13-ter were rewritten, with a helper for the new layouts, to match the spec's checks; the layout choices are the agents'.
- The `base:` line recompute is a helper that builds the record-alone base per case (placed, taken with an ended owner, other).

## Known gaps

- Lines edited in `concepts.md`, `foreman.md` and `driver.md` are longer than the files' usual wrapping.
- Requests of the running batch already taken on a working request above their dependency will print their dependency's branch and show "not on its place" after the merge; the merge message to the batch's manager is owed.

<details>
<summary>Details</summary>

## Changes

- `stacks.py`: `_start_candidate` (the nearest earlier PR, only when `ready`); `start_on_for` uses it; `stack_start` rules: live start branch, taken-not-placed with no open dependency on the default branch, queued with no open dependency on the candidate or the default branch, open dependency on its highest open dependency, placed requests keep their rule.
- `commands/facts.py`: the `base:` line compares the real base with a record-alone base recomputed per case.
- `core/records.py`: comment on `start_on`.
- Cards: `concepts.md` (Stack, Dependencies), `foreman.md` (the first take), `driver.md` (CR driver).
- Tests: `test_stack_base.py` cases flipped and added, a parametrised `base:` line test.
- Scenario: steps 13, 13-bis, 13-ter, a `stack` placement after the unhold take in `stack_hold`, and `scenario/README.md`.

## Human decisions

- A new request starts on an earlier one's branch only when that one is handed back `ready`; otherwise on the default branch (narrows the earlier "nearest earlier PR, whatever its state" rule).
- A request that needs a working request's code says so with `after`; otherwise requests start side by side.

## Impacts

No visual change. Stack batches get different (safer) bases at `take`; the board's "on" and off-place reports follow the same rule.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `910cc44`: `just check`, `just eval-dry-run`
- [x] Evidence: scenario gate at `910cc44`
- [x] Review: approved at `910cc44`
- [x] Verified at `910cc44`
- [x] CI green at `910cc44`

## Internal references

- CR-455 take-draft; stacked after CR-442 (stack-git-chain) and CR-438 (stack-shape-guard).

</details>
