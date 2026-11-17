## Summary

The stack driver (the chantier agent that builds one stack of pull requests from a batch's changes) read a stack row `PR in draft` as "this change is not handed back ready" and stopped before building the forge stack, so a second take was needed. The rows that `take stack` and `stack` print now carry one label that says the hand-back state and, apart from it, the PR's draft flag as last recorded, for example `ready, PR draft (#251)`. A change handed back ready reads `ready` whatever its PR's draft flag, and the stack-driver card says the stack is made from that state.

## Deliverables

One row label, before and after (the rest of each row is unchanged):

| State | Before | After |
| --- | --- | --- |
| Handed back ready, PR still a draft | `PR in draft` | `ready, PR draft (#251)` |
| Handed back ready, PR out of draft | `ready to merge` | `ready, PR out of draft (#250)` |
| Driver working, PR draft | `working` | `working, PR draft (#253)` |
| Draft flag never read, GitLab MR | `ready locally` | `ready, PR draft not read (!12)` |
| No PR recorded | the status | the status alone (`queued`, `working`, `ready`) |

Sample rows from a scenario run of the `stack` command (after, at `5e10b25`, carried from the pre-restack head; before, at the old base, these rows read the derived words of the table):

```text
ready, PR draft (#45) worktree ... branch ... base ... PR ... head ...
working, PR out of draft (#45) worktree ... branch ... base ... PR ... head ...
```

Choices: one combined label in one column; the stored status word `working` is used, never `running`; a PR out of draft reads `PR out of draft`, never `PR ready`. The derived words (`ready to merge`, `PR in draft`, `ready locally`) stay everywhere else (`status`, `handoff`, the board, the pane).

## Blast radius

Grade: **1**. Only the text of two commands' rows changes, plus card wording; a plain `git revert` restores it.

## Autonomous decisions

- The label helper `stack_label` lives in `commands/facts.py` next to `stack_lines`, its only caller, and reuses `pr_number` and `GITLAB_LINK` (no new parser).

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `commands/facts.py`: `stack_label` builds the row label; `stack_lines` uses it.
- `skills/chantier/references/driver.md` (Stack driver): rows are read as hand-back state plus draft flag; the stack is made from `ready`; the mergeable part is the run of `ready, PR out of draft` rows from the bottom; "Making the stack" and "Ordering" are written against the labels.
- `skills/chantier/references/concepts.md` (Words): the stack rows are the one place `ready` is shown, with the draft flag.
- `scenario/run_scenario.py` and `scenario/README.md`: checks of the rows (draft and out of draft, taken-back CR, no PR, GitLab `!<n>`).
- `skills/chantier/scripts/cli/tests/test_stack_label.py`: a small parametrized test of the label.

## Human decisions

- One combined label in one column, not two columns.
- A change with a live driver reads `working` (the stored status), never `running`.
- A PR out of draft reads `PR out of draft`, never `PR ready`, since `ready` is the ambiguous word this change removes.
- The stack-driver card says the stack is made from the hand-back state, whatever the PR's draft flag.

## Impacts

No visual change; no field of the status files, the pane or the board changes.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test_stack_label.py` and the scenario checks, carried to `5e10b25`
- [x] Local gates: judged before the restacks, carried over clean restacks to `5e10b25`
- [x] Evidence: before at the old base, after carried to `5e10b25`: the pasted rows above, from the scenario run
- [x] Review: approved before the restacks, carried over clean restacks to `5e10b25`
- [x] Verified before the restacks, carried over clean restacks to `5e10b25`
- [x] CI green at `5e10b25`: all 5 jobs pass, `just scenario (ubuntu-latest)` included

## Internal references

- CR-314 stack-handback-state-vs-draft
- Round report: work/r1.md

</details>
