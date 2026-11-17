## Summary

Session titles that name a batch put the batch number in the middle (`Chantier 17 · Foreman`), which makes the project name look like a different project in the session list. The batch number now comes last, in parentheses, and the project name stands alone before the role.

## Deliverables

| Before | After |
| --- | --- |
| `[Battle] 💬 Chantier 17 · CoS` | `[Battle] 💬 Chantier · CoS (Batch 17)` |
| `[Battle] ⚙️ Chantier 17 · Foreman` | `[Battle] ⚙️ Chantier · Foreman (Batch 17)` |

Titles with no batch (`[<code>] 💬 Project · CoS`, `· Griller`) are unchanged, and so is when a session is renamed.

## Blast radius

Grade: 1

Card and doc text only; a plain `git revert` restores the previous titles.

## Autonomous decisions

None

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/session-start.md`: the Titles table, the batch-number and separator bullets, and the examples.
- `skills/chantier/references/concepts.md`: "Session title".
- `skills/chantier/references/chief-of-staff.md`: the Foreman prompt's title and example, and the direct-mode title.
- `evals/real-direct/RUNBOOK.md`: the quoted direct-mode title.

## Impacts

No visual change beyond the title text of the sessions.

## Test plan

- [x] No behaviour change: card and doc text only
- [x] Local gates at `91114fe`: `just check` pass (382 passed) (restacked; patch carried)
- [x] Evidence: none, text change
- [x] Review: approved at `91114fe` (restacked; patch carried)
- [x] Verified at `91114fe` (restacked; patch carried)
- [x] CI green at `91114fe` (restacked; patch carried)

## Internal references

CR-322 session-title-batch-suffix

</details>
