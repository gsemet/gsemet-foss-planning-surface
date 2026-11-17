## Summary

A user choosing between a Foreman and direct steering had no figure on what each costs. The README now gives the measured spend of two real eval batches, says what they do and do not show, and tells the reader how to measure their own batches.

## Deliverables

- A new `## What a batch costs` section in `README.md`, between "Batch modes" and "Change Requests Lifecycle":
  a frame sentence, a four-row comparison table (batch spend, steering, the Chief of Staff's session, all in),
  what the two runs show, what they do not show, and how to measure one's own (`chantier cost`,
  `--by cr`, `--explain`) with a link to [Costs and budgets](https://github.com/gsemet/chantier/blob/main/docs/costs.md).
- The comparison table, as it reads in the README:

  | | Run 1: Foreman (Sonnet 5.5), stack | Run 2: direct (Opus 5.5), parallel |
  |---|---|---|
  | The batch (its budget's spend) | $10.28 | $11.52 ($11.91 once closed) |
  | Steering, inside that spend | $2.10 (20%) | $3.39 (30%) |
  | The Chief of Staff's session, outside the budget | about $4.67 | $0.05 |
  | All in | about $14.6-15.0 | about $11.5-11.9 |

## Blast radius

Grade: 1. A documentation section; a plain `git revert` removes it.

## Autonomous decisions

- The root `README.md` carries the section, not `evals/README.md`: the choice between the modes is the user's, and the root page already sells it.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `README.md`: one new section, no other edit.

## Impacts

Readers of the README see the cost comparison and the commands to measure their own batches. No code change.

## Test plan

- [x] New or changed tests (they fail on the previous code): No behaviour change
- [x] Local gates at `d7baadd`: `just check`: 190 tests passed
- [x] Evidence: none, a documentation change
- [x] Review: approved at `d7baadd`
- [x] Verified at `d7baadd`
- [x] CI green at `d7baadd`

## Internal references

CR-276 eval-cost-readme.

</details>
