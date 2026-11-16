## Summary

The budget rail checked the batch's recorded spend, which only `status --refresh`, `pause` and `close` wrote. In a short batch no refresh came between two `take`s, so a real spend of more than $11 could still show "$0.82 of $20" and never trip the budget. A reader of `status` also could not tell how old the figure was.

Now every command that checks the budget first refreshes the spend from the transcripts, and `status`, `STATUS.json` and the batch `STATUS.md` say how old the figure is.

## Deliverables

Where the spend is refreshed (only when the batch has a budget):

| Command | Check point |
| --- | --- |
| `take <cr>`, `take stack` | `commands/driver.py` |
| `round <cr>` | `commands/driver.py` |
| `order qa`, `order add --fix-for` (the Foreman's own) | `commands/orders.py` |
| `release go` | `commands/release.py` |

The age, as `status` prints it: `spent $0.82 of $20, 12 min old` (`, age unknown` for a record from before the change; nothing when the spend is unknown). `STATUS.json` gets a `spent_at` key, and the batch `STATUS.md` shows ` as of <spent_at>`.

Example: `spent $0.82 of $20, 12 min old`.

When the refresh itself fails (no Foreman transcript, no priced call, unreadable transcript), the check runs on the last recorded figure and a successful command prints `spend not refreshed: <error>; budget checked on <spent> (<age>)`.

Cost of the refresh, measured at `6dbb81d` on Windows: reading and recording the spend takes a median of 1.45 s (runs 1.45, 1.37, 1.50 s) on the transcripts of a long batch's own steering session and its subagents (the eval run's batch record is archived and cannot be run). Interpreter start is not included. It adds well under a few seconds to a command that checks a budget.

## Blast radius

Grade: **1**. Additive; with no budget nothing is refreshed. A plain `git revert` restores the old behaviour (an extra optional `spent_at` key in `batch.json` is ignored by older readers).

## Autonomous decisions

- Open question 1 took the specification's default: a failed refresh checks on the last recorded figure and says so, rather than refusing.
- On a refusal the `spend not refreshed` line is not added to the error message; it shows only when the command succeeds.
- The shared spend refresh is one function (`refresh_spend`) used by `status --refresh` and every check point.

## Known gaps

- The CR board pane and the web board do not show the age (out of scope by the specification).
- The other budget steps of the scenario that inject `spent_usd` were not rewritten: their worlds hold no priced Foreman transcript, so the refresh fails there and the stored figure is checked; the new parallel step and the unit tests prove the refresh.

<details>
<summary>Details</summary>

## Changes

- `commands/batch_status.py`: `refresh_spend`, `refresh_for_check`, `age_text`; `record_costs` sets `spent_at`; the batch line shows the age.
- `core/records.py`: `BatchRecord.spent_at`; `status/views.py`, `status/markdown.py`: the new field.
- Check points in `commands/driver.py`, `orders.py`, `release.py`.
- Cards `concepts.md` and `status-layout.md`; docstrings of `rails.check_budget` and `cost`.
- Tests: `tests/test_spend_check.py`; scenario: a new refusal step in the parallel unit.

## Impacts

No visual change beyond the age in `status` output.

## Test plan

- [x] New or changed tests (`test_spend_check.py`: six check points refused and passing, no budget, failed refresh, status age)
- [x] Local gates at `f263b56` (before the clean rebase): `just check` and the parallel scenario unit passed; the pipeline's `just scenario (ubuntu-latest)` passed at `6dbb81d`
- [x] Evidence: a scratch batch at `6dbb81d`: stored $0.01, budget $0.5, `take` refused with exit 5, `status` then shows `0 min old`
- [x] Review: approved at `f263b56` (carried from `f263b56` over a clean rebase to `6dbb81d`)
- [x] Verified at `6dbb81d`
- [x] CI green at `6dbb81d`: all five checks pass

## Internal references

CR-279 spend-fresh

</details>
