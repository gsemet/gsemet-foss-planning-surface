## Summary

In a direct batch, `cost` counted an orchestrating-session turn that merely named a specification (for example in a worker's prompt) as grill work, so the budgeted "steering the batch" row was too low. On a real run the steering row read $1.18 where it was about $3.6, and the steering share looked like 50% instead of 61%. Now a turn is grill work only when it actually writes a CR's files or starts a spec-writer.

## Deliverables

Steering row of the real direct run, priced again with the old and the new rule (same claim window, same calls, none lost or counted twice):

| Rule | Steering row | Grill part |
|---|---|---|
| before | $0.987 (18 calls) | $2.573 (41 calls) |
| after | **$3.560 (59 calls)** | **$0.000 (0 calls)** |

Choices made:
- Inside the steering window, only a host write tool (`Write`, `Edit`, `MultiEdit`, `NotebookEdit`) whose target path ends in `01-intent.md`, `02-answers.md`, `03-change-spec.md` or `work/specifying`, or an `Agent` start of a spec-writer, makes a grill turn. Naming a path, reading it, a shell command, or a write to another file whose content names one is steering.
- A turn is still attributed whole; nothing changes outside the steering window (Foreman mode, before the claim, whole-session line).
- Same lines, same table shape, same budget; only the figures become true.

Release notes line: a direct batch's `cost` now counts the orchestrating session's steering turns on the steering row (a turn that only names or reads a specification is no longer a grill turn), so its steering share is higher, and true.

## Blast radius

Grade: 1. Only how `cost` splits an orchestrating-session transcript changes, in one module and two cards; no data format changes. A `git revert` restores the old split.

## Autonomous decisions

- The original diagnosis said a path in a `take` output moved the turns. A tool result is never read by the pricing code, so it cannot be; the tool uses that moved them were the five worker starts whose prompts name `03-change-spec.md` and one write of a retro file whose content names it. Writes made after the window ended also moved turns already priced, which is why the row drifted between readings.
- Each call is classified by the window its own record's `timestamp` falls in (strict inside the steering window, loose elsewhere, no time = loose), so the two prices the CLI sums agree on every call inside the window.
- The $3.560 is the window's own figure; the earlier report's $3.61 also held the calls between the batch's opening and the claim, which are outside the window and stay on the grill line (since the opening: steering $3.560, grill $0.090, 2 calls).

<details>
<summary>Details</summary>

## Changes

- `costs.py`: `_grill_use(block, strict)` and `usage(..., steering=(since, until))`; `session_costs` passes it through.
- `commands.py`: `_cost_rows` and `_chief_line` pass the claim window of each orchestrating-session transcript.
- Cards `chief-of-staff.md` and `status-layout.md` state the same rule, and tell that session to write those files with the host's Write or Edit tool, never a shell command.
- Tests: `test_costs.py` (strict cases, a Windows path, outside the window, a turn straddling the window end). Scenario: a steering turn that names and reads a specification stays on the row in a direct batch; a read stays on the grill line in Foreman mode.

## Human decisions

- Only a write of a CR's files, or a spec-writer start, is grill; a shell write counts as steering (the safe side: that spend stays in the budget).
- Nothing changes outside the steering window.
- The target is the window's own figure, about $3.56, not the report's $3.61.
- The old run's report and any new eval run are out of scope.

## Impacts

No visual change. A direct batch shows a higher, true steering share in `cost`, its reports and the budget rail.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_costs.py`, 58 pass at `373d347`
- [x] Local gates at `373d347`: `just check`; `just scenario` carried from `484b8a6`: patch unchanged; the long gate runs once at the top of the stack, PR 152 (recorded by the gate)
- [x] Evidence at `373d347`: the real run's transcript priced again, table above
- [x] Review: approved at `484b8a6` (the body fixed after the second review; carried to `373d347`: patch unchanged by the restack)
- [x] Verified at `373d347`
- [x] CI green at `373d347`

## Internal references

- CR-200 cost-steering-vs-grill (batch 15); evidence in `.agents/changes/4-batch/2-actives/200-cost-steering-vs-grill/evidence/` (`price-run1.py`, `price-run1-output.txt`); transcript session `bd7f6b12-6a6f-436b-b052-ba60efdf5909`.
- The specification's "rule 3" is the unchanged loose rule outside the steering window.

</details>
