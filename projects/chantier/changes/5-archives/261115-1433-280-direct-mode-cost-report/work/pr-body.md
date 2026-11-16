## Summary

In a direct batch the Chief of Staff steers, yet `chantier cost` printed `foreman:` as the first line of `cost --by cr`, and its `Chief of Staff, whole session` line was smaller than the steering row printed just above it, because that line silently left the batch's own spend out. This PR names the steering role by the mode and makes the whole-session figure price the whole session, naming the part of it that is in the batch's spend.

## Deliverables

The whole-session line now covers the whole session and says which part of it is the batch's:

```text
Chief of Staff, whole session: $13.16 ($11.52 of it in the batch's spend), context 224,242 tokens; not counted: 0 compactions since the batch opened, which leave no record (about $0.12 each)
```

Read top to bottom: whole session = its part in the batch's spend + steering outside the budget + grill and specifications + what the session spent before the batch opened. The parenthesis is left out when the session has no call in the batch's spend (a Foreman batch the Chief of Staff never steered), and the figure is then unchanged.

`cost --by cr` labels the steering group by the mode (the internal group key stays `foreman`):

| Group holds | Printed label |
| --- | --- |
| no Chief of Staff steering row | `foreman` (unchanged) |
| only Chief of Staff steering rows | `Chief of Staff, steering the batch, and its own subagents` |
| both | `Chief of Staff, steering the batch, and the Foreman, with their own subagents` |

The cost errors about a missing transcript say "steering transcript" and "Chief of Staff" in a direct batch. The whole session stays outside the batch's spend and budget.

Captured from the scenario's direct batch at `315ff36` (fixture prices, not real spend):

```text
$ chantier cost --by cr
batch-01: $60.060 over 6 model calls
Chief of Staff, steering the batch, and its own subagents: $30.030 (3 calls)
CR-101: $30.030 (3 calls; Driver peak context 22,010 tokens, 0 compactions)
Chief of Staff, steering the batch (outside the budget): $10.01 since the batch opened (1 calls)
Chief of Staff, grill and specifications with the user (outside the budget): $20.02 since the batch opened (2 calls, 0 spec-writers, 0 spec critics)
Chief of Staff, whole session: $110.11 ($60.06 of it in the batch's spend), context 22,010 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each)
```

## Blast radius

Grade: **1**. Printing and wording only; the batch's spend, budget and the board's cost keys are untouched. A plain `git revert` restores the previous output.

## Autonomous decisions

- No pytest test asserted the old direct refusal text, so none was added.

## Known gaps

- The local `just scenario` run on Windows passed every check but flagged the `stack` and `series-deps` units as over their time budget (519 s and 283 s), which makes the recipe exit 1; the pipeline's `just scenario (ubuntu-latest)` job passed at the head, and the Windows overrun is machine speed, not a failed check.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/commands/cost/sessions.py`: the whole-session amount no longer subtracts the batch's spend; adds the parenthesis; the missing-transcript errors are worded by the mode.
- `skills/chantier/scripts/cli/src/chantier/commands/cost/command.py`: `_by_cr` printing and the `cost` error by mode.
- Cards and docs: `chief-of-staff.md`, `status-layout.md`, `docs/costs.md`, `docs/use-cases-direct.md`, `scenario/README.md`.
- `scenario/run_scenario.py`: the direct section's checks (whole minus parenthesis, parenthesis equals the headline spend, whole at least the steering row), and a `cost --by cr` check for the direct batch and the taken-over one.

## Human decisions

- The whole-session line prices the full session and names the part in the batch's spend (for instance `$13.16 ($11.52 of it in the batch's spend)`), rather than keeping the old figure and renaming the line.

## Impacts

Users of a direct batch read a cost report that adds up and names the Chief of Staff. No visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): scenario direct-batch checks
- [x] Local gates at `315ff36`: `just check` pass (190 passed)
- [x] Evidence: scenario `direct` unit at `315ff36`, captured output above
- [x] Review: approved at `9d4136c`, committed as `315ff36`
- [x] Verified at `315ff36`
- [x] CI green at `315ff36`

## Internal references

CR-280 direct-mode-cost-report. Round notes: `work/r1.md`.

</details>
