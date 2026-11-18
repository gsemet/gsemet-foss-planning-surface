## Summary

When a stack is merged on the forge, a PR merged into the branch of another PR of the batch lands on the default branch together with that other PR. The board's PRs page used to read the first merge as "into <branch>" and `status` kept telling the Chief of Staff "not landed, record nothing until <base> lands", even after the base had landed. The record then kept the PR's change as ready, and a later stack creation was refused (HTTP 422 on the merged PR). The PRs page now follows the chain of merged bases on the forge and `status` says when a stacked PR landed with its base, so it can be recorded.

## Deliverables

The signal and the `status` line for a stacked merge, before and after (made-up names):

| Case | Before | After |
|---|---|---|
| PR merged into `cr-0`'s branch, `cr-0` later merged into `main` | `... not landed, tell the user, record nothing until cr-0 lands` | `board saw merged: cr-1 #12 into cr-0's branch at <t>, landed with cr-0 at <t2>; for the Chief of Staff: order merged cr-1` |
| Chain: cr-2 into cr-1 into cr-0 into `main` | not landed | cr-2 landed with cr-0 |
| Base merged before the PR, or still open | not landed | not landed (unchanged) |

Choices: the judgment uses only the forge read the page already makes (state, base, merge time), with no git read and no new forge call; times are compared as instants, and a base merged at the same instant counts as landed.

## Blast radius

Grade: **1**. A read-only judgment in the board's PRs page and a text change in `status`; a plain `git revert` restores the previous behaviour. Old `board-seen.jsonl` lines stay readable.

## Autonomous decisions

- The line text and the choice of entry moved from `batch_status.py` into `board/seen.py` (one function), to keep `batch_status.py` well under 400 lines.

## Known gaps

- Same-second ordering of a stacked merge unproved; trial: the next stacked merge. The forge gives merge times to the second, and the tests use made-up times, so a base merged before the PR in the same second is not shown to be told apart.

<details>
<summary>Details</summary>

## Changes

- `board/prs.py`: a pure `landed_with(row, by_cr)` follows the chain of merged bases (a cycle, a missing row, a base merged earlier or a missing merge time is not landed); each row gets `landed_with`.
- `board/seen.py`: the signal entry carries `landed_with` and `landed_at` when landed, written once per (batch, CR, landed or not), so a merge first seen not landed then seen landed writes one second line; a new `lines()` builds the `status` lines, the landed entry winning over one without.
- `commands/batch_status.py`: reads the file and calls `seen.lines`.
- `chief-of-staff.md` and `docs/web-board.md`: a `landed with` line is a merge to record; only a `not landed` line is not (GitLab folds keep their own rule).

## Human decisions

None from the user beyond adding this change to the batch.

## Impacts

No visual change. `status` prints one more kind of line.

## Test plan

- [x] New or changed tests at `2a514cb` (they fail on the previous code): `test_board_prs.py`, a parametrized signal test (later, same instant, earlier, open then later, chain) and the `status` test extended with a not-landed then landed pair.
- [x] Evidence: no screenshot (the board pane is untouched); the tests show the `status` line before and after, at `2a514cb`.
- [x] Local gates at `2a514cb`: `just check` (477 passed), `just eval-dry-run` (17 of 17 as expected).
- [x] Review: approved at `2a514cb`
- [x] Verified at `2a514cb`
- [x] CI green at `2a514cb`: `just check` on Linux, macOS and Windows, `just eval-dry-run` and `just scenario` (ubuntu-latest) pass.

## Internal references

- CR-336, batch-24.
- Specification: `03-change-spec.md` and `02-answers.md` in the CR's planning folder.

</details>
