## Summary

The eval campaigns had grown unevenly: a staged smoke and a staged full campaign that overlapped, a real campaign with no automatic check, and no way to compare two runs line by line. This PR redesigns them into four campaigns judged the same way: `real-foreman`, `real-direct`, `claude-planted` (the two staged Claude campaigns merged) and `copilot` (unchanged). Every report now carries one scorecard of chantier's rails, and the audit also runs on the real campaigns.

## Deliverables

Campaigns before and after:

| Before | After |
| --- | --- |
| `real` | `real-foreman` (renamed, real inbox items, nothing merges during the run) |
| none | `real-direct` (same campaign steered in direct mode) |
| `claude-smoke`, `claude-full` | `claude-planted` (one campaign, current CLI rules in each "Expected") |
| `copilot` | `copilot` (untouched) |

The scorecard (`evals/SCORECARD.md`) is one table of rails with stable ids (C* for the CLI's refusals, J* for the cards' judgements). Each run marks a rail `seen, right`, `seen, wrong` or `not seen`, and gives the cost and the steering share. The audit prints the table from that file:

```text
audit.py <checkout> [--real]   ->  PASS/FAIL lines with rail ids, then the scorecard table
unknown rail id or failed check ->  exit 1
```

## Blast radius

Grade: 1. Only `evals/` and the eval paragraphs of two docs change; the CLI, cards, agents, hooks and scenario are untouched. A plain `git revert` restores the old campaigns.

## Autonomous decisions

- Added scorecard rails C15 to C20 and J18 to J24 found in the code and cards, removing none.
- Added the missing `order confirm` turn to `claude-planted`: the CLI refuses to take a release that shares its batch without it.
- SCORECARD C4 follows the code (`round` is refused on the round limit, not on the budget), not the card's wording.
- A real CR still blocked at the report is kept through `order drop`, then put back in the inbox by hand: `pause` and `close` refuse a blocked CR and the CLI has no un-drop.

<details>
<summary>Details</summary>

## Changes

- `evals/real` moved to `evals/real-foreman`; new `evals/real-direct/RUNBOOK.md` and `evals/claude-planted/RUNBOOK.md`; `claude-smoke` and `claude-full` removed.
- `evals/kit/setup.py`: one `claude-planted` key; `copilot` kept; an unknown key is refused with the list.
- `evals/SCORECARD.md`: the single list of rails.
- `evals/kit/audit.py`: rail ids on every check, scorecard printed, `--real` mode (read-only `gh pr view`, the CLI's `cost`, the main checkout compared with its state at open, direct-mode transcripts).
- `evals/README.md`, `README.md` and `CONTRIBUTING.md` name the four campaigns and when to run each. Past reports in `evals/results/` are untouched.

## Human decisions

- Three runbooks plus the unchanged Copilot one; one scorecard per rail, with cost and steering share.
- An automatic audit for the real campaigns; the rest of the scorecard is read by hand.
- Real campaigns use small real items picked with the user's go, and each run's PRs are merged or closed within the day.

## Impacts

No product change; maintainers get new campaign names and a comparable report.

## Test plan

- [x] No behaviour change in the product; the audit and setup checked by hand at fb0d409
- [x] Local gates at fb0d409: `just check` passes
- [x] Evidence at fb0d409: links, old names, setup, audit staged and real, runbook commands; no before image (docs and eval kit only)
- [x] Review: approved at fb0d409
- [x] Verified at fb0d409
- [x] CI green at fb0d409 (just check on 3 systems, just scenario)

## Internal references

CR-176 evals-redesign. Evidence under the CR's `evidence/` folder.

</details>



