## Summary

In a stack batch, the native stack on the forge could only be made once every PR of the batch existed, so one slow change blocked the whole stack and the user could not merge anything meanwhile. The stack is now made as soon as two PRs are ready and grows from the bottom: each further change joins on top as a draft when it has its PR, the user may merge the ready PRs below while the drafts on top go on, and after a partial merge a new stack of what remains is made silently.

This PR is one commit on main (CR-234 is merged).

## Deliverables

The stack as it stands, and what `forge-stack show` now prints:

| Stack | `forge-stack show` |
| --- | --- |
| two ready PRs, the rest to come | `stack #N ready: open, 2 PRs in order, partial stack mergeable below <sha7> (#m, 2 PRs)` and `to come: ...` |
| a change joined as a draft | `... drafts on top #204` and `to come: ...` |
| everything ready | `stack complete, mergeable below <sha7> (#m)`, no `to come:` line |

- `stack <cr>...` accepts a partial order: the named changes take places 1..k, the others follow above in their order; a named change that depends on an unnamed open one is refused.
- `forge-stack create`/`rebuild` act on the stack as it stands (the bottom changes with a PR), drafts included; `rebuild` is the unstack-then-create for a change that joins.
- The five checks read against each change's status (a draft under a ready PR, a ready change still a draft, a non-ready change not a draft).
- The cards (stack driver, Foreman, Chief of Staff, concepts, status layout) say the same two `stack-ready` asks (first stack, complete stack), the silent restack, the partial-stack line of every progress report, and the "deliver by" rule.

## Blast radius

Grade: 2. The CLI's `stack` ordering and `forge-stack` behaviour change and four cards change; the revert is a plain `git revert`, the batches in flight keep their cards until reloaded.

## Autonomous decisions

- README.md and the docs still say the stack is made once every PR is ready: left to the docs follow-up the specification names.

## Known gaps

- README.md (line 105) and the docs diagrams still describe the stack as made once every PR is ready; the specification leaves them to a docs follow-up.
- No screenshot is due: the board pane is unchanged.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`: `stack` partial order and the new refusal.
- `skills/chantier/scripts/cli/src/chantier/commands/forge_stack.py`: `_plan`, `_unstack`, `_checks`, `show`, `rebuild` on the stack as it stands.
- `skills/chantier/references/driver.md`, `foreman.md`, `chief-of-staff.md`, `concepts.md`, `status-layout.md`: the cards.
- `scenario/run_scenario.py`, `scenario/README.md`: section 13a covers the new behaviour.

## Human decisions

- The first stack is made at two ready PRs; a further change joins on top as a draft as soon as it has its PR (unstack, then create again).
- Among independent changes the first ready goes lowest; a change always stays above the ones it depends on.
- The user may merge the ready PRs below while the drafts on top go on; once a draft turns ready, the stack is mergeable up to it.
- After a partial merge, a new stack of what remains is made silently, with no ask.
- Two `stack-ready` asks only: when the stack is first made (naming what is still to come) and when it is complete; none per addition.
- A change already in the stack that is handed back ready sends no ask: the next progress report says it, and its gaps come in the complete ask.
- Every progress report names the commit below which the stack is mergeable.
- A working change that joins is rebased by its own Driver; the stack driver never pushes a branch a live Driver holds.
- When a batch will not finish by the time the user gave, work goes toward the largest mergeable partial stack from the bottom by that time, and if the stack is not complete then, the `stack-ready ... to come:` ask of the stack as it stands is sent.

## Impacts

No visual change. A stack batch gets a stack on the forge earlier; a progress report names the commit below which the user may merge.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario section 13a
- [x] Local gates (at the pre-restack head, carried: the restack kept the patch; just check re-run by the Verifier at d97665f): `just check` pass; `just scenario` github 710/710, gitlab 679/679; mypy --strict on linux, darwin and win32 pass
- [x] Evidence: none (no visible change)
- [x] Review: approved at the pre-restack head, carried to d97665f (patch and tree unchanged; see the restack note)
- [x] Verified at `d97665f`
- [x] CI green at `d97665f`: `gh pr checks 180`, all five jobs pass

## Internal references

- CR-244 stack-grows-from-bottom; based on CR-234 forge-stack follow-ups; CR-233 is merged.

</details>
