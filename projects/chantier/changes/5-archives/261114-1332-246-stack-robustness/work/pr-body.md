## Summary

A native stack of pull requests could break partway through in four ways, and the cards and the CLI had no answer for any of them: a change dropped from the middle of the stack, a merge of the bottom PRs with no heavy CI at their own head, a stack driver that ends or restarts in the middle of a restack, and sibling changes that conflict once they are put in a line. This PR gives each case a procedure and the few CLI facts it needs.

## Deliverables

What the reader gets, by case:

| Case | Before | After |
| --- | --- | --- |
| A change dropped from the stack | No removal procedure; its PR read as foreign to the stack | The PRs above go to draft, its commits leave the branches above (a rebase), the stack is rebuilt, its PR is closed and its branch kept; `forge-stack` names its PR apart (`dropped #n (<cr>): close it`) |
| A merge in the middle without heavy CI at its head | Not said | Heavy CI stays at the top; the user is told a merge below it is their choice, and may ask for a run at that head (`heavy CI: <cr>`, reported as a `heavy-ci` ask) |
| A stack driver that ends mid-restack | Nothing recorded how far it got | `stack` prints each row's `head` and last `restack:` note, and the recorded stack driver's context; a new stack driver resumes from the first change not done |
| Sibling conflicts | All surface at the end | A conflict that needs code at a join aborts that rebase, drafts the PR on top, goes on with the take and is reported (`conflict: stacked on <cr>: <files>`); the Foreman sends the change back to its Driver |

The rows printed by `stack` now carry the two new columns:

```text
<cr> ... head <head7> restack: <last restack note | none>
context: <n> tokens (agent <id>) | context: not measured (<reason>)
```

## Blast radius

Grade: 2. Cards that steer the stack driver and the Foreman, plus two printed lines of `stack` and a check of `forge-stack`; a `git revert` restores the previous text and output, but a stack already on the forge needs a `forge-stack rebuild` afterwards.

## Autonomous decisions

- `forge_stack.py` passed 400 lines, so its checks moved to a new `forge_stack_checks.py` (the file-size target).
- `_context_line` became the public `context_line(repo, d, agent)` so `note`, `round` and `stack` share it.
- `foreman.md` grew by about 19 lines to hold the four rules; it was not split.

## Known gaps

- The card changes reach a running batch only once merged into the main checkout and reloaded.
- A trial merge of sibling changes before they have a PR is not done, and a dropped change's PR is closed with no comment.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`, new `forge_stack_checks.py`: the plan returns the PRs of dropped changes; `unstack` names them (`it also held #n of <cr>, dropped: close it`); check 2 names them apart from a foreign PR.
- `commands/facts.py` (`stack_lines`): `head` and last `restack:` note per row. `commands/delivery.py` (`stack`): a final `context:` line. `commands/driver.py`: `context_line` takes the agent id.
- `skills/chantier/references/driver.md`, `foreman.md`, `chief-of-staff.md`, `concepts.md`: removing a dropped change, the optional heavy CI run, recording and resuming a restack, sibling conflicts at a join.
- `scenario/run_scenario.py` (section 13a) and `scenario/README.md`: steps for the dropped PR, the foreign PR, the `stack` rows and the context line.

## Human decisions

- A change dropped from the middle of the stack is removed cleanly, with no stop to ask the user.
- Heavy CI runs only on the top PR by default; merging in the middle without it is the user's choice.
- A restack's progress is recorded so a restarted stack driver resumes; sibling conflicts are handled as they come.

## Impacts

No visual change. The `stack` command prints two additions; `forge-stack show` has one new failure wording.

## Test plan

- [ ] New or changed tests: scenario section 13a steps (dropped PR, foreign PR, rows, context line)
- [ ] Reading pass: `rg -n "drop: |without <dropped" skills/chantier/references` finds the removal in `foreman.md`, `driver.md`, `chief-of-staff.md`; `rg -n "resume:|hand-back blocked context" skills/chantier/references` finds it in `foreman.md` and `driver.md`; `rg -n "heavy CI: |heavy-ci" skills/chantier/references` finds the optional run in the three cards; `rg -n "conflict: stacked on" skills/chantier/references` finds the stack driver's and the Foreman's rule; no card says every head must be green before a partial merge
- [ ] Local gates at `<sha7>`: `just check`, `just scenario`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-246 stack-robustness; depends on CR-233 and CR-244.

</details>
