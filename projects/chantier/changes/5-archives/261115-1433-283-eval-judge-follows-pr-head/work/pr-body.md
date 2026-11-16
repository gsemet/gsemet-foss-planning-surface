## Summary

In a stack sandbox run on GitHub, each bottom merge restacks the PRs above it and replaces their heads. The audit's judge judged the head the batch's record held, which was then on no ref of the origin, so 4 of 6 judge rows read `not run`. The judge now resolves each CR's PR on the forge and judges that PR's head (its head at merge once merged), and its row says which head it judged and where it came from.

## Deliverables

Before and after, for a restacked merged PR (judge table, `head judged` cell):

| | cell | result |
| --- | --- | --- |
| before | `3f60a08` (record's head) | `not run (head 3f60a08 not found on the origin)` |
| after | `93a906c, the PR's head at merge (the record holds 3f60a08)` | judged |

- The `head judged` cell names the head checked out and its source (`the PR's head at merge`, or `the PR's head` for an open PR), and the record's head when it differs.
- When the forge view of the PR is missing, the row is `not run (the PR's head could not be read from the forge: ...)`; the recorded head is never judged in its place.
- The dry run's clean world replays the restack (the PR branch moves to a new commit after the hand-back) and asserts the cell.

## Blast radius

Grade: 1. The eval kit and its README only; `git revert` restores the previous judge.

## Autonomous decisions

- The restack in the dry run is played with git plumbing on the local origin, outside any agent, so no transcript or rail sees it.
- `sandbox_checks` also returns a view per PR number, so the judge uses the view of the PR the record holds.

## Known gaps

- Only a live stack run of `real-foreman` on GitHub proves the real judge rows name the PRs' heads at merge; this PR proves it on the dry run and by hand on the four replaced heads.

<details>
<summary>Details</summary>

## Changes

- `evals/kit/audit.py`: `judge_rows` judges the `headRefOid` of the recorded PR's forge view; new cell wording; `not run` when the view is missing; the `no head` skip is gone.
- `evals/kit/dry_run.py`: `Batch.feature` restacks the PR branch on the local origin; `judge_rows(text, cell=-1)` can return the `head judged` cell; `case_clean` asserts it.
- `evals/README.md`: the judge paragraph says the hidden tests run on the PR head as the forge reports it.

## Impacts

No visual change; audit tables name the head judged.

## Test plan

- [x] New or changed tests (they fail on the previous code), judged at `7d1905b`: the clean dry-run case fails on the previous `audit.py` with `FAIL clean: the judge's feature row names the restacked head at merge and the head the record holds / "e2fb3e2 (the PR's head is 2518e60)", wanted 2518e60 / e2fb3e2`
- [x] Local gates at `7d1905b`: `just check` pass; `just eval-dry-run` pass, 8 of 8 cases as expected
- [x] Evidence (at `7d1905b`): by hand, `judge.py` on the four replaced heads of the stack run: `93a906c` edit-item, `59edd1f` status-filter, `1f29cde` json-api, `3900c46` stats-page, all `pass`
- [x] Review: approved at `9d4136c` (reviewed state, carried to `7d1905b` over a clean rebase)
- [x] Verified at `7d1905b`
- [x] CI green at `7d1905b`

## Internal references

- CR-283 judge-head
- `work/r1.md`

</details>
